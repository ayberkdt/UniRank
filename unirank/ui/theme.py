# assets/theme_updated.py
"""
Uygulama genelinde **tema (renk paleti + QSS) ve tipografi (font)** yönetimini tek bir noktadan sağlar.

Bu modülün amacı:
- Koyu tema renklerini `ThemeConfig` içinde merkezi olarak tanımlamak,
- Bu konfigürasyondan Qt Stylesheet (QSS) üretmek (`build_qss`),
- Uygulama paletini oluşturmak (`build_palette`),
- Uygulama başlangıcında temayı tek seferde uygulamak (`apply_theme`),
- Diğer modüllerin aktif temayı güvenle okuyabilmesini sağlamak (`get_active_theme`),
- Varsa `assets/fonts` altındaki fontları yükleyip uygulama geneline atamak (`load_fonts`).

Kullanım (özet):
    app = QApplication(sys.argv)
    cfg = ThemeConfig(accent="#7AA2F7", font_px=14)
    apply_theme(app, cfg)

Notlar:
- En iyi sonuç için `apply_theme(...)` çağrısını, ana pencere (MainWindow) oluşturulmadan önce yapın.
- QSS, bazı platformlarda palette göre daha baskın olabilir; bu nedenle palette + QSS birlikte uygulanır.
"""


# ===================================================================
# 0.                         IMPORTS
# ===================================================================

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Tuple, Optional, Iterable, Any
from PyQt6.QtGui import QColor, QPalette, QFontDatabase, QFont
from PyQt6.QtWidgets import QApplication, QGraphicsDropShadowEffect
from PyQt6.QtWidgets import (
    QLineEdit, QTextEdit, QPlainTextEdit, QComboBox,
    QSpinBox, QDoubleSpinBox
)

from PyQt6.QtCore import QEvent, QObject


# ===================================================================
# 1.                         HELPERS
# ===================================================================

def _hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """#RRGGBB / #RGB / RRGGBB / RGB → (r,g,b)."""
    # Baş/son boşlukları ve opsiyonel '#' işaretini temizle
    s = hex_color.strip().lstrip("#")

    # Kısa form (#RGB) gelirse #RRGGBB'ye genişlet
    if len(s) == 3:
        s = "".join(c * 2 for c in s)

    # Uzunluk kontrolü (artık sadece 6 hane bekliyoruz)
    if len(s) != 6:
        raise ValueError(f"Geçersiz hex renk (beklenen RGB/RRGGBB): {hex_color!r}")

    # Hex karakter kontrolü (hata mesajı daha anlaşılır olsun)
    try:
        return int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16)
    except ValueError as e:
        raise ValueError(f"Geçersiz hex karakteri: {hex_color!r}") from e


def _rgba(hex_color: str, a: float) -> str:
    # Hex rengi RGB'ye çevir
    r, g, b = _hex_to_rgb(hex_color)

    # Alfa değerini [0, 1] aralığına sıkıştır (QSS tarafı için güvenli)
    a = float(a)
    if a < 0.0:
        a = 0.0
    elif a > 1.0:
        a = 1.0

    # Qt stylesheet için rgba(...) string'i döndür
    return f"rgba({r},{g},{b},{a})"


def _scaled_int(x: int, s: float) -> int:
    # Ölçek çok küçükse bile UI tamamen çökmesin diye alt sınır uygula
    s = max(0.25, float(s))

    # px değerini ölçekle, en az 1 px olacak şekilde güvence altına al
    return max(1, int(round(int(x) * s)))



# ===================================================================
# 2.                        FONT CONFIG
# ===================================================================

def _iter_font_files(font_dir: Path) -> Iterable[Path]:
    # Font klasörü yoksa boş iterator dön (caller tarafı sorunsuz çalışsın)
    if not font_dir.exists():
        return iter(())

    # Desteklenen uzantılardaki fontları sırayla gez
    files: list[Path] = []
    for ext in ("*.ttf", "*.otf", "*.ttc"):
        files.extend(sorted(font_dir.glob(ext)))
    return iter(files)


def load_fonts(
    app: QApplication,
    font_dir: Optional[Path] = None,
    prefer_family: str = "Inter",
    pixel_size: int = 13,
    *,
    prefer_families: Optional[Iterable[str]] = None,
    require: bool = True,
) -> str:
    """assets/fonts içindeki fontları yükler ve uygulama geneli fontu ayarlar.

    Seçim sırası (deterministik):
      1) prefer_families verilmişse listedeki ilk mevcut family
      2) değilse prefer_family
      3) hiçbirisi yoksa ve require=True ise exception

    Not: "fallback yok" demek, yok sayıp sessizce devam etmek değil;
    konfigürde açıkça yazılan font ailesi / fallback listesi üzerinden
    deterministik seçim yapmak demek. Hiçbiri yoksa erken hata verilir.
    """
    font_dir = font_dir or (Path(__file__).resolve().parent / "fonts")

    loaded_families: list[str] = []
    seen: set[str] = set()

    for fp in _iter_font_files(font_dir):
        font_id = QFontDatabase.addApplicationFont(str(fp))
        if font_id < 0:
            continue
        for fam in QFontDatabase.applicationFontFamilies(font_id):
            if fam and fam not in seen:
                seen.add(fam)
                loaded_families.append(fam)

    # Aday listesi
    candidates: list[str] = []
    if prefer_families is not None:
        candidates = [str(x).strip() for x in prefer_families if str(x).strip()]
    else:
        pf = str(prefer_family).strip()
        if pf:
            candidates = [pf]

    if not candidates:
        if require:
            raise RuntimeError("Font seçimi için prefer_family/prefer_families boş olamaz")
        candidates = []

    # Mevcut family setleri
    sys_families = {f for f in QFontDatabase.families()}
    loaded_set = {f for f in loaded_families}

    chosen: Optional[str] = None
    for cand in candidates:
        # 1) önce yüklenenlerde ara
        for fam in loaded_families:
            if fam.lower() == cand.lower():
                chosen = fam
                break
        if chosen:
            break
        # 2) sonra sistemde ara
        for fam in sys_families:
            if fam.lower() == cand.lower():
                chosen = fam
                break
        if chosen:
            break

    if not chosen:
        if require:
            raise RuntimeError(f"İstenen font aileleri bulunamadı: {candidates!r}")
        # require=False ise Qt'nin default fontuna dokunma
        return ""

    f = QFont(chosen)
    f.setPixelSize(max(1, int(pixel_size)))
    app.setFont(f)
    return chosen




# ===================================================================
# 3.                        THEME CONFIG
# ===================================================================

# -------------------------
# STRICT THEME API (no fallback)
# -------------------------

_COLOR_FIELDS = (
    "bg", "surface", "surface2", "border", "border_soft",
    "text", "text_muted", "text_faint",
    "accent", "accent2", "danger", "warning",
)

def validate_theme(cfg: "ThemeConfig") -> None:
    """Tema konfigürasyonunu **strict** doğrular (fallback yok).

    - Renkler: #RGB/#RRGGBB (başında # opsiyonel) olmalı
    - Tipografi: font_family boş olamaz, font_px >= 8 olmalı
    - Geometri / yoğunluk: negatif/0 değerler kabul edilmez
    """
    # Font family
    if not str(cfg.font_family).strip():
        raise ValueError("ThemeConfig.font_family boş olamaz")

    # Colors: _hex_to_rgb aynı zamanda format doğrular
    for name in _COLOR_FIELDS:
        val = getattr(cfg, name, None)
        if val is None:
            raise ValueError(f"ThemeConfig.{name} eksik/None olamaz")
        try:
            _hex_to_rgb(str(val))
        except Exception as e:
            raise ValueError(f"ThemeConfig.{name} geçersiz hex renk: {val!r}") from e

    # Numeric constraints
    if int(cfg.font_px) < 8:
        raise ValueError("ThemeConfig.font_px en az 8 olmalı")
    if int(cfg.radius) < 1 or int(cfg.radius_sm) < 1:
        raise ValueError("ThemeConfig.radius/radius_sm en az 1 olmalı")
    if int(cfg.padding) < 0 or int(cfg.padding_sm) < 0:
        raise ValueError("ThemeConfig.padding/padding_sm negatif olamaz")
    if float(cfg.scale) <= 0.0:
        raise ValueError("ThemeConfig.scale 0'dan büyük olmalı")


def theme_tokens(cfg: "ThemeConfig") -> dict[str, Any]:
    """Widget katmanının kullanacağı token sözlüğü (STRICT)."""
    validate_theme(cfg)
    return {
        # required by widgets / utils
        "accent": cfg.accent,
        "accent2": cfg.accent2,
        "danger": cfg.danger,
        "bg": cfg.bg,
        "surface": cfg.surface,
        "surface2": cfg.surface2,
        "border": cfg.border,
        "text": cfg.text,
        "text_muted": cfg.text_muted,
        "font_family": cfg.font_family,
        "font_px": int(cfg.font_px),
        # extra (often useful)
        "border_soft": cfg.border_soft,
        "text_faint": cfg.text_faint,
        "warning": cfg.warning,
        "radius": int(cfg.radius),
        "radius_sm": int(cfg.radius_sm),
        "padding": int(cfg.padding),
        "padding_sm": int(cfg.padding_sm),
        "scale": float(cfg.scale),
    }


@dataclass(frozen=True)
class ThemeConfig:
    # Core colors
    bg: str = "#09090B"  # Zinc 950
    surface: str = "#0F0F12"  # Neutral dark surface
    surface2: str = "#141419"  # Elevated surface
    border: str = "#27272A"  # Zinc 800 (base)
    border_soft: str = "#18181B"  # Zinc 900

    text: str = "#F4F4F5"  # Zinc 100
    text_muted: str = "#A1A1AA"  # Zinc 400
    text_faint: str = "#71717A"  # Zinc 500

    accent: str = "#3B82F6"     # Blue 500 (vivid)
    accent2: str = "#22C55E"    # Green 500
    danger: str = "#EF4444"  # Red 500
    warning: str = "#F59E0B"  # Amber 500

    # Typography (single source of truth)
    font_family: str = "Inter"
    font_fallbacks: Tuple[str, ...] = ("SF Pro Display", "Segoe UI", "Arial")
    font_px: int = 13

    # Geometry
    radius: int = 12
    radius_sm: int = 10

    # Density
    padding: int = 10
    padding_sm: int = 8

    # Optional scaling multiplier (basic HiDPI tuning)
    scale: float = 1.0

    def validated(self) -> "ThemeConfig":
        """Strict sanity-check (fallback yok)."""
        validate_theme(self)
        return self


def _qss_font_stack(cfg: ThemeConfig) -> str:
    # QSS font-family listesinde her family'yi tırnaklamak daha az sürpriz üretir
    families = (cfg.font_family,) + tuple(cfg.font_fallbacks)
    return ", ".join(f'"{f}"' for f in families if str(f).strip())


def build_qss(cfg: ThemeConfig) -> str:
    cfg = cfg.validated()

    # Ölçeklenebilir değerler (HiDPI için)
    r  = _scaled_int(cfg.radius, cfg.scale)
    rs = _scaled_int(cfg.radius_sm, cfg.scale)
    p  = _scaled_int(cfg.padding, cfg.scale)
    ps = _scaled_int(cfg.padding_sm, cfg.scale)
    fp = _scaled_int(cfg.font_px, cfg.scale)  # font da ölçeklensin
    hp = max(10, fp - 2)  # header font size (smaller, premium dashboard)

    font_stack = _qss_font_stack(cfg)

    # Premium dark: borderları genelde rgba ile çok hafif tutuyoruz.
    # (Hex'ten türettiğimiz border rengi, QSS'te alpha ile "subtle" hale gelir.)
    # Hairline borders: "light hit" using white with low alpha (premium dashboards)
    b_subtle = _rgba("#FFFFFF", 0.14)
    b_ultra  = _rgba("#FFFFFF", 0.10)
    b_hair   = _rgba("#FFFFFF", 0.06)
    t_muted  = _rgba(cfg.text_muted, 0.95)
    t_faint  = _rgba(cfg.text_faint, 0.95)

    # Butonlarda çok hafif "top-down lighting" için gradient.
    btn_grad = f"qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 {_rgba(cfg.surface2,0.92)}, stop:1 {_rgba(cfg.surface2,0.72)})"
    btn_grad_h = f"qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 {_rgba(cfg.surface2,0.98)}, stop:1 {_rgba(cfg.surface2,0.78)})"
    btn_grad_p = f"qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 {_rgba(cfg.surface2,0.78)}, stop:1 {_rgba(cfg.surface2,0.62)})"

    pri_grad = f"qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 {_rgba(cfg.accent,0.34)}, stop:1 {_rgba(cfg.accent,0.18)})"
    pri_grad_h = f"qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 {_rgba(cfg.accent,0.42)}, stop:1 {_rgba(cfg.accent,0.22)})"
    pri_grad_p = f"qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 {_rgba(cfg.accent,0.28)}, stop:1 {_rgba(cfg.accent,0.16)})"

    dang_grad = f"qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 {_rgba(cfg.danger,0.30)}, stop:1 {_rgba(cfg.danger,0.16)})"
    dang_grad_h = f"qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 {_rgba(cfg.danger,0.38)}, stop:1 {_rgba(cfg.danger,0.20)})"

    return f"""
/* ==========================================================
   Premium Dark Theme (Qt QSS)
   - Tinted blacks + subtle borders
   - Micro-interactions (hover/focus/pressed)
   - Modern table + overlay-ish scrollbar
   ========================================================== */

/* -------------------------
   Global defaults
   -------------------------
   Not: QWidget background'ı genel olarak bg'ye çekilir.
   Card/panel hissi için surface/surface2 + rgba border kullanılır.
*/
* {{
  font-family: {font_stack};
  font-size: {fp}px;
  color: {cfg.text};
}}

QWidget {{
  background: {cfg.bg};
}}

QToolTip {{
  background: {_rgba(cfg.surface2, 0.96)};
  border: 1px solid {b_subtle};
  padding: {ps}px {p}px;
  border-radius: {rs}px;
  color: {cfg.text};
}}

/* -------------------------
   Menus / Status
   ------------------------- */
QMenuBar {{
  background: {_rgba(cfg.surface, 0.60)};
  border-bottom: 1px solid {b_hair};
}}
QMenuBar::item {{
  padding: 6px 10px;
  border-radius: {rs}px;
  color: {t_muted};
}}
QMenuBar::item:selected {{
  background: {_rgba(cfg.accent, 0.12)};
  color: {cfg.text};
}}

QMenu {{
  background: {_rgba(cfg.surface2, 0.98)};
  border: 1px solid {b_subtle};
  border-radius: {r}px;
  padding: 6px;
}}
QMenu::item {{
  padding: 8px 12px;
  border-radius: {rs}px;
  color: {t_muted};
}}
QMenu::item:selected {{
  background: {_rgba(cfg.accent, 0.14)};
  color: {cfg.text};
}}

QStatusBar {{
  background: {_rgba(cfg.surface, 0.58)};
  border-top: 1px solid {b_hair};
  color: {t_muted};
}}

/* -------------------------
   GroupBox / Panels
   -------------------------
   Kontrastı tonla değil lightness farkıyla veriyoruz.
*/
QGroupBox {{
  background: {_rgba(cfg.surface, 0.46)};
  border: 1px solid {b_ultra};
  border-radius: {r}px;
  margin-top: 14px;
  padding: 12px;
}}
QGroupBox::title {{
  subcontrol-origin: margin;
  left: 14px;
  padding: 0 8px;
  color: {t_muted};
  font-weight: 800;
}}

/* -------------------------
   Inputs
   -------------------------
   Focus halinde QSS ile 'halo' hissi:
   - border accent
   - background çok hafif açılır
   Not: gerçek glow, theme.py içinde eventFilter ile opsiyonel olarak verilir.
*/
QLineEdit, QTextEdit, QPlainTextEdit, QComboBox, QSpinBox, QDoubleSpinBox {{
  background: {_rgba(cfg.surface2, 0.58)};
  border: 1px solid {b_ultra};
  border-radius: {rs}px;
  padding: {ps}px;
  selection-background-color: {_rgba(cfg.accent, 0.26)};
}}

QLineEdit:hover, QTextEdit:hover, QPlainTextEdit:hover,
QComboBox:hover, QSpinBox:hover, QDoubleSpinBox:hover {{
  border: 1px solid {b_subtle};
  background: {_rgba(cfg.surface2, 0.62)};
}}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus,
QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus {{
  border: 1px solid {_rgba(cfg.accent, 0.90)};
  background: {_rgba(cfg.surface2, 0.68)};
}}

QLineEdit:disabled, QTextEdit:disabled, QPlainTextEdit:disabled,
QComboBox:disabled, QSpinBox:disabled, QDoubleSpinBox:disabled {{
  color: {t_faint};
  background: {_rgba(cfg.surface, 0.52)};
  border: 1px solid {_rgba(cfg.border_soft, 0.45)};
}}

QComboBox {{
  padding-right: 28px;
}}
QComboBox::drop-down {{
  width: 28px;
  border: 0px;
}}
QComboBox::down-arrow {{
  width: 10px;
  height: 10px;
  image: none;
}}
QComboBox QAbstractItemView {{
  background: {_rgba(cfg.surface2, 0.99)};
  border: 1px solid {b_subtle};
  border-radius: {r}px;
  padding: 6px;
  selection-background-color: {_rgba(cfg.accent, 0.14)};
  color: {t_muted};
}}

/* -------------------------
   Buttons
   -------------------------
   Butonlara çok hafif gradient ile hacim kazandır.
   Hover/Pressed alpha değişimleri yumuşak olmalı.
*/
QPushButton {{
  background: {btn_grad};
  border: 1px solid {b_ultra};
  border-radius: {r}px;
  padding: {p}px 12px;
  font-weight: 800;
}}
QPushButton:hover {{
  background: {btn_grad_h};
  border: 1px solid {b_subtle};
}}
QPushButton:pressed {{
  background: {btn_grad_p};
  border: 1px solid {b_subtle};
}}
QPushButton:disabled {{
  color: {t_faint};
  background: {_rgba(cfg.surface, 0.52)};
  border: 1px solid {_rgba(cfg.border_soft, 0.40)};
}}

QPushButton[class="primary"] {{
  background: {pri_grad};
  border: 1px solid {_rgba(cfg.accent, 0.55)};
}}
QPushButton[class="primary"]:hover {{
  background: {pri_grad_h};
  border: 1px solid {_rgba(cfg.accent, 0.72)};
}}
QPushButton[class="primary"]:pressed {{
  background: {pri_grad_p};
  border: 1px solid {_rgba(cfg.accent, 0.62)};
}}

QPushButton[class="danger"] {{
  background: {dang_grad};
  border: 1px solid {_rgba(cfg.danger, 0.55)};
}}
QPushButton[class="danger"]:hover {{
  background: {dang_grad_h};
  border: 1px solid {_rgba(cfg.danger, 0.72)};
}}

/* -------------------------
   CheckBox / Radio (basic)
   -------------------------
   Çok agresif custom çizim yerine sade modern dokunuş.
*/
QCheckBox {{
  spacing: 8px;
  color: {t_muted};
}}
QCheckBox::indicator {{
  width: 16px;
  height: 16px;
  border-radius: 4px;
  border: 1px solid {b_subtle};
  background: {_rgba(cfg.surface2, 0.55)};
}}
QCheckBox::indicator:hover {{
  border: 1px solid {_rgba(cfg.accent, 0.55)};
}}
QCheckBox::indicator:checked {{
  background: {_rgba(cfg.accent, 0.24)};
  border: 1px solid {_rgba(cfg.accent, 0.75)};
}}

/* -------------------------
   Tables
   -------------------------
   - Grid çizgileri silik (Excel hissi yok)
   - Seçim: soft fill + (mümkünse) sol accent bar
*/
QTableView {{
  background: {_rgba(cfg.surface, 0.42)};
  border: 1px solid {b_ultra};
  border-radius: {r}px;
  gridline-color: transparent;
  selection-background-color: transparent; /* item:selected ile kontrol edeceğiz */
  selection-color: {cfg.text};
  alternate-background-color: {_rgba("#FFFFFF", 0.02)};
}}

QTableView::item {{
  padding: 6px 10px;
  border: none;
}}

QTableView::item:hover {{
  background-color: {_rgba(cfg.accent, 0.06)};
}}

QTableView::item:selected {{
  background-color: {_rgba(cfg.accent, 0.14)};
  /* Sol accent bar hissi (Qt'de item başına uygulanır; bazı stillerde tüm hücrelerde görünebilir) */
  border-left: 3px solid {_rgba(cfg.accent, 0.85)};
}}

QHeaderView::section {{
  /* Premium table header: compact, slightly faint, uppercase-like */
  background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 {_rgba(cfg.surface2,0.55)}, stop:1 {_rgba(cfg.surface2,0.35)});
  color: {t_faint};
  border: 0px;
  border-bottom: 1px solid {b_hair};
  padding: 8px 10px;
  font-size: {hp}px;
  font-weight: 900;
  text-transform: uppercase;
}}
QTableCornerButton::section {{
  background: {_rgba(cfg.surface2, 0.62)};
  border: 0px;
  border-bottom: 1px solid {b_ultra};
}}

/* -------------------------
   Scrollbars (overlay-ish)
   -------------------------
   Track şeffaf; handle ince ve rounded.
*/
QScrollBar:vertical {{
  background: transparent;
  width: 8px;
  margin: 8px 6px 8px 6px;
}}
QScrollBar::handle:vertical {{
  background: {_rgba(cfg.text_faint, 0.18)};
  border-radius: 4px;
  min-height: 32px;
}}
QScrollBar::handle:vertical:hover {{
  background: {_rgba(cfg.text_faint, 0.28)};
}}
QScrollBar::handle:vertical:pressed {{
  background: {_rgba(cfg.text_faint, 0.34)};
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
  height: 0px;
}}
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
  background: transparent;
}}

QScrollBar:horizontal {{
  background: transparent;
  height: 8px;
  margin: 6px 8px 6px 8px;
}}
QScrollBar::handle:horizontal {{
  background: {_rgba(cfg.text_faint, 0.18)};
  border-radius: 4px;
  min-width: 32px;
}}
QScrollBar::handle:horizontal:hover {{
  background: {_rgba(cfg.text_faint, 0.28)};
}}
QScrollBar::handle:horizontal:pressed {{
  background: {_rgba(cfg.text_faint, 0.34)};
}}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
  width: 0px;
}}
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
  background: transparent;
}}

/* -------------------------
   Splitter
   ------------------------- */
QSplitter::handle {{
  background: transparent;
}}
QSplitter::handle:horizontal {{
  width: 10px;
}}
QSplitter::handle:vertical {{
  height: 10px;
}}
QSplitter::handle:hover {{
  background: {_rgba(cfg.accent, 0.10)};
  border-radius: 6px;
}}
"""


def build_palette(cfg: ThemeConfig) -> QPalette:
    cfg = cfg.validated()
    pal = QPalette()

    bg = QColor(cfg.bg)
    surface = QColor(cfg.surface)
    surface2 = QColor(cfg.surface2)
    text = QColor(cfg.text)
    muted = QColor(cfg.text_muted)
    accent = QColor(cfg.accent)

    # Temel roller
    pal.setColor(QPalette.ColorRole.Window, bg)
    pal.setColor(QPalette.ColorRole.Base, surface)
    pal.setColor(QPalette.ColorRole.AlternateBase, surface2)

    pal.setColor(QPalette.ColorRole.Text, text)
    pal.setColor(QPalette.ColorRole.WindowText, text)
    pal.setColor(QPalette.ColorRole.Button, surface)
    pal.setColor(QPalette.ColorRole.ButtonText, text)

    pal.setColor(QPalette.ColorRole.PlaceholderText, muted)
    pal.setColor(QPalette.ColorRole.Highlight, accent)
    pal.setColor(QPalette.ColorRole.HighlightedText, bg)

    # Tooltip ve link renkleri (bazı platformlarda fark yaratıyor)
    pal.setColor(QPalette.ColorRole.ToolTipBase, surface2)
    pal.setColor(QPalette.ColorRole.ToolTipText, text)
    pal.setColor(QPalette.ColorRole.Link, accent)
    pal.setColor(QPalette.ColorRole.BrightText, QColor(cfg.danger))

    # Kenar tonları (Fusion için faydalı)
    pal.setColor(QPalette.ColorRole.Mid, QColor(cfg.border))
    pal.setColor(QPalette.ColorRole.Dark, QColor(cfg.border_soft))

    return pal



# ===================================================================
# 3.5                OPTIONAL: FOCUS GLOW (MICRO-INTERACTION)
# ===================================================================

class _FocusGlowFilter(QObject):
    """Uygulama genelinde input focus durumunda hafif 'glow' efekti verir.

    Not:
    - QSS'te gerçek box-shadow / glow sınırlı olduğu için QGraphicsDropShadowEffect kullanılır.
    - Yalnızca FocusIn/FocusOut anında çalışır; sürekli repaint yapmaz (performans dostu).
    """

    def __init__(self, cfg: ThemeConfig):
        super().__init__()
        self.cfg = cfg.validated()

    def eventFilter(self, obj, event):  # type: ignore[override]
        try:
            et = event.type()
            if et not in (QEvent.Type.FocusIn, QEvent.Type.FocusOut):
                return False

            # Sadece input'lar
            if not isinstance(obj, (QLineEdit, QTextEdit, QPlainTextEdit, QComboBox, QSpinBox, QDoubleSpinBox)):
                return False

            if et == QEvent.Type.FocusIn and obj.isEnabled():
                # Mevcut bir efekt varsa (ör. card shadow), FocusOut'ta geri koyabilmek için sakla
                if not hasattr(obj, "_focus_glow_prev_effect"):
                    try:
                        setattr(obj, "_focus_glow_prev_effect", obj.graphicsEffect())
                    except Exception:
                        setattr(obj, "_focus_glow_prev_effect", None)

                eff = QGraphicsDropShadowEffect(obj)
                # Premium glow: küçük blur + accent rengi, çok düşük alpha
                blur = _scaled_int(18, self.cfg.scale)
                eff.setBlurRadius(float(blur))
                eff.setOffset(0.0, 0.0)
                c = QColor(self.cfg.accent)
                c.setAlphaF(0.30)  # subtle halo (slightly reduced for enterprise look)
                eff.setColor(c)
                obj.setGraphicsEffect(eff)
            else:
                # FocusOut veya disabled → önceki efekti geri yükle (yoksa None)
                prev = getattr(obj, "_focus_glow_prev_effect", None)
                try:
                    obj.setGraphicsEffect(prev)
                finally:
                    if hasattr(obj, "_focus_glow_prev_effect"):
                        delattr(obj, "_focus_glow_prev_effect")

        except Exception:
            # Robust: glow hatası UI'yi çökertmesin
            return False

        return False


def _install_focus_glow(app: QApplication, cfg: ThemeConfig) -> None:
    """App'e tek seferlik focus glow filter kurar (GC olmasın diye property'e koyar)."""
    try:
        if app.property("_focus_glow_filter") is not None:
            return
        flt = _FocusGlowFilter(cfg)
        app.installEventFilter(flt)
        app.setProperty("_focus_glow_filter", flt)
    except Exception:
        pass


def get_active_theme(app: Optional[QApplication] = None) -> ThemeConfig:
    """Aktif temayı döndürür (STRICT: fallback yok).

    apply_theme(...) çağrılmadan önce veya theme_cfg set edilmeden çağrılırsa exception fırlatır.
    """
    app = app or QApplication.instance()
    if app is None:
        raise RuntimeError("QApplication instance bulunamadı. get_active_theme() için önce QApplication oluşturmalısın.")
    cfg = app.property("theme_cfg")
    if not isinstance(cfg, ThemeConfig):
        raise RuntimeError("Aktif tema ayarlı değil. Uygulama başında apply_theme(app, cfg) çağırmalısın.")
    return cfg


def apply_theme(app: QApplication, cfg: Optional[ThemeConfig] = None) -> None:
    """
    Uygulama başında bir kez çağır:
        cfg = ThemeConfig(accent="#7AA2F7")
        apply_theme(app, cfg)
    """
    cfg = (cfg or ThemeConfig()).validated()

    # Diğer modüller için tema bilgisini app property olarak sakla
    app.setProperty("theme_cfg", cfg)

    # Style set etmek, palette/qss davranışını daha öngörülebilir yapar
    try:
        app.setStyle("Fusion")
    except Exception:
        pass

    # Tema geçişinde eski QSS kalıntıları bazen çakışabilir (önce temizle)
    app.setStyleSheet("")

    # Bundle fontları yükle (bulunmazsa sistem fontları ile devam eder)
    load_fonts(
        app,
        prefer_families=(cfg.font_family,) + tuple(cfg.font_fallbacks),
        pixel_size=_scaled_int(cfg.font_px, cfg.scale),
        require=True,
    )

    # Önce palette, sonra QSS (QSS bazı rolleri override edebilir)
    app.setPalette(build_palette(cfg))
    app.setStyleSheet(build_qss(cfg))

    # Opsiyonel: input focus glow (QSS limitleri için küçük bir premium dokunuş)
    _install_focus_glow(app, cfg)



# ===================================================================
# 4.                       TESTING THEME.PY
# ===================================================================

if __name__ == "__main__":
    import sys
    from PyQt6.QtCore import Qt
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QWidget,
        QVBoxLayout, QHBoxLayout, QGridLayout, QFormLayout,
        QLabel, QPushButton, QLineEdit, QComboBox,
        QProgressBar, QGroupBox, QSpinBox, QDoubleSpinBox,
        QSlider, QPlainTextEdit, QTextEdit,
        QScrollArea, QTableWidget, QTableWidgetItem,
        QTabWidget, QMenuBar, QMenu, QMessageBox,
        QListWidget, QListWidgetItem, QFrame, QToolTip
    )

    # Crash’te terminalde gör
    def _excepthook(exc_type, exc, tb):
        import traceback
        traceback.print_exception(exc_type, exc, tb)
        input("\n[theme_updated.py] Exception occurred. Press Enter to exit...")

    sys.excepthook = _excepthook

    class ThemePreviewWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("SimCode Theme Preview & Style Guide")
            self.resize(1180, 860)

            # Menü (QSS Menü / QAction hover vs. için)
            menubar = self.menuBar()
            m_file = menubar.addMenu("File")
            act_about = m_file.addAction("About…")
            act_quit = m_file.addAction("Quit")
            act_quit.triggered.connect(self.close)

            m_view = menubar.addMenu("View")
            act_dummy = m_view.addAction("Dummy Action")

            # Aksiyonlar: tooltip + disabled state
            act_dummy.setToolTip("QAction tooltip testi")
            act_dummy.setEnabled(True)

            def _show_about():
                QMessageBox.information(self, "About", "Theme preview window.\nMenus, tooltips, tables, scrollbars, inputs test edilir.")
            act_about.triggered.connect(_show_about)

            # ScrollArea: uzun sayfada tema davranışı
            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            self.setCentralWidget(scroll)

            central = QWidget()
            scroll.setWidget(central)

            root = QVBoxLayout(central)
            root.setSpacing(18)
            root.setContentsMargins(28, 28, 28, 28)

            # KESİN: tema uydurma yok — aktif temayı oku
            cfg = get_active_theme()

            # -------------------------
            # 1) Typography / Colors / Tooltip
            # -------------------------
            lbl_title = QLabel("Typography & Colors")
            lbl_title.setStyleSheet(f"font-size: 24px; font-weight: 800; color: {cfg.accent};")
            root.addWidget(lbl_title)

            lbl_sub = QLabel(
                "The quick brown fox jumps over the lazy dog.\n"
                "0123456789 — !@#$%^&*()_+\n"
                "Focus, hover, disabled, selection, scrollbars test."
            )
            lbl_sub.setStyleSheet(f"font-size: 15px; color: {_rgba(cfg.text, 0.84)};")
            root.addWidget(lbl_sub)

            tip = QLabel("Hover: Tooltip testi (üzerine gel)")
            tip.setToolTip("Bu bir tooltip. Border / radius / background kontrolü için.")
            root.addWidget(tip)

            # -------------------------
            # 2) Renk Paleti
            # -------------------------
            gb_colors = QGroupBox("Color Palette")
            grid = QGridLayout(gb_colors)
            grid.setHorizontalSpacing(16)
            grid.setVerticalSpacing(12)

            colors_to_show = [
                ("Background", cfg.bg),
                ("Surface", cfg.surface),
                ("Surface 2", cfg.surface2),
                ("Border", cfg.border),
                ("Border Soft", cfg.border_soft),
                ("Text", cfg.text),
                ("Muted", cfg.text_muted),
                ("Faint", cfg.text_faint),
                ("Accent", cfg.accent),
                ("Accent 2", cfg.accent2),
                ("Danger", cfg.danger),
                ("Warning", cfg.warning),
            ]

            row, col = 0, 0
            for name, hex_code in colors_to_show:
                swatch = QLabel()
                swatch.setFixedSize(86, 52)
                swatch.setStyleSheet(
                    f"background-color: {hex_code};"
                    f"border: 1px solid {_rgba(cfg.border, 0.75)};"
                    f"border-radius: 10px;"
                )

                lbl = QLabel(f"{name}\n{hex_code}")
                lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
                lbl.setStyleSheet(f"font-size: 11px; color: {_rgba(cfg.text_faint, 0.95)};")

                wrapper = QWidget()
                v = QVBoxLayout(wrapper)
                v.setContentsMargins(0, 0, 0, 0)
                v.setSpacing(6)
                v.addWidget(swatch, 0, Qt.AlignmentFlag.AlignCenter)
                v.addWidget(lbl, 0, Qt.AlignmentFlag.AlignCenter)

                grid.addWidget(wrapper, row, col)
                col += 1
                if col >= 6:
                    col = 0
                    row += 1

            root.addWidget(gb_colors)

            # -------------------------
            # 3) Inputs / Controls + Button states
            # -------------------------
            gb_controls = QGroupBox("Inputs & Controls")
            hb = QHBoxLayout(gb_controls)
            hb.setSpacing(18)

            left = QWidget()
            form = QFormLayout(left)
            form.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
            form.setFormAlignment(Qt.AlignmentFlag.AlignTop)
            form.setHorizontalSpacing(12)
            form.setVerticalSpacing(10)

            le = QLineEdit("Standart metin girişi")
            le.setPlaceholderText("Placeholder testi")
            le.setToolTip("Focus glow / border / bg test")
            form.addRow("QLineEdit:", le)

            dis_inp = QLineEdit("Disabled input")
            dis_inp.setDisabled(True)
            form.addRow("Disabled:", dis_inp)

            combo = QComboBox()
            combo.addItems(["Seçenek 1", "Seçenek 2", "Seçenek 3"])
            combo.setToolTip("ComboBox hover/focus test")
            form.addRow("QComboBox:", combo)

            sp = QSpinBox()
            sp.setRange(-10, 250)
            sp.setValue(42)
            form.addRow("QSpinBox:", sp)

            dsp = QDoubleSpinBox()
            dsp.setRange(-10.0, 250.0)
            dsp.setDecimals(3)
            dsp.setValue(3.141)
            form.addRow("QDoubleSpinBox:", dsp)

            slider = QSlider(Qt.Orientation.Horizontal)
            slider.setRange(0, 100)
            slider.setValue(65)
            form.addRow("QSlider:", slider)

            pb = QProgressBar()
            pb.setRange(0, 100)
            pb.setValue(72)
            form.addRow("QProgressBar:", pb)

            hb.addWidget(left, 1)

            right = QWidget()
            vr = QVBoxLayout(right)
            vr.setSpacing(10)

            btn_primary = QPushButton("Primary / Accent Button")
            btn_primary.setProperty("class", "primary")
            btn_primary.setToolTip("class='primary' QSS testi")

            btn_secondary = QPushButton("Secondary Button")
            btn_secondary.setToolTip("Normal QPushButton hover/pressed test")

            btn_danger = QPushButton("Danger Button")
            btn_danger.setProperty("class", "danger")

            btn_disabled = QPushButton("Disabled Button")
            btn_disabled.setDisabled(True)

            # checkbox istemiyorsun olabilir ama theme test için lazım.
            # Yine de standart QCheckBox burada sadece theme.py test amaçlı.
            from PyQt6.QtWidgets import QCheckBox
            chk = QCheckBox("Onay Kutusu (Checkbox)")
            chk.setChecked(True)

            # Property set edince polish iyi olur
            for b in (btn_primary, btn_danger):
                b.style().unpolish(b)
                b.style().polish(b)

            vr.addWidget(btn_primary)
            vr.addWidget(btn_secondary)
            vr.addWidget(btn_danger)
            vr.addWidget(btn_disabled)
            vr.addSpacing(6)
            vr.addWidget(chk)
            vr.addStretch(1)

            hb.addWidget(right, 1)
            root.addWidget(gb_controls)

            # -------------------------
            # 4) Tabs + Text areas (scrollbar/selection)
            # -------------------------
            gb_text = QGroupBox("Tabs + Text Areas (scrollbar / selection / focus)")
            vtxt = QVBoxLayout(gb_text)

            tabs = QTabWidget()
            vtxt.addWidget(tabs)

            # Tab 1: text edits
            tab1 = QWidget()
            htxt = QHBoxLayout(tab1)

            te = QTextEdit()
            te.setPlainText("QTextEdit\n\nSelection / focus / disabled görünümleri test edilir.\n\n" + ("Lorem ipsum " * 40))
            te.setMinimumHeight(150)

            pte = QPlainTextEdit()
            pte.setPlainText("QPlainTextEdit\n- daha düz metin\n- scrollbar testi\n\n" + ("Line\n" * 60))
            pte.setMinimumHeight(150)

            htxt.addWidget(te, 1)
            htxt.addWidget(pte, 1)
            tabs.addTab(tab1, "Editors")

            # Tab 2: long list (scrollbar overlay hissi)
            tab2 = QWidget()
            vlist = QVBoxLayout(tab2)
            lst = QListWidget()
            for i in range(80):
                item = QListWidgetItem(f"Item #{i+1} — hover/selection test")
                lst.addItem(item)
            vlist.addWidget(QLabel("QListWidget (scrollbar & selection)"))
            vlist.addWidget(lst)
            tabs.addTab(tab2, "Lists")

            root.addWidget(gb_text)

            # -------------------------
            # 5) Table (hover / selection / header / gridless)
            # -------------------------
            gb_table = QGroupBox("Table (hover / selection / header)")
            vtab = QVBoxLayout(gb_table)

            table = QTableWidget(10, 4)
            table.setHorizontalHeaderLabels(["Name", "Type", "Value", "Status"])
            table.setAlternatingRowColors(True)
            table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
            table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)

            sample = [
                ("Gravity Model", "SH", "1200", "ON"),
                ("Third Body", "Sun", "Enabled", "ON"),
                ("SRP", "Cannonball", "1.2", "OFF"),
                ("Albedo", "Simple", "0.3", "OFF"),
                ("Thermal", "N/A", "-", "OFF"),
                ("Relativity", "1PN", "Enabled", "ON"),
                ("Tides", "k2/k3", "0.024", "ON"),
                ("Integrator", "DOP853", "adaptive", "ON"),
                ("Output", "CSV", "enabled", "ON"),
                ("Logging", "Verbose", "off", "OFF"),
            ]
            for i, rowv in enumerate(sample):
                for j, val in enumerate(rowv):
                    item = QTableWidgetItem(str(val))
                    table.setItem(i, j, item)

            table.resizeColumnsToContents()
            vtab.addWidget(table)

            # küçük bir footer açıklama
            foot = QLabel("İpucu: tabloda satır seç, hover yap, header’a tıkla, scrollbar’ı sürükle.")
            foot.setStyleSheet(f"color: {_rgba(cfg.text_faint, 0.95)};")
            vtab.addWidget(foot)

            root.addWidget(gb_table)

            root.addStretch(1)

    # --- Uygulamayı Başlat ---
    app = QApplication(sys.argv)

    # Tema “uydurma” yok:
    # 1) Ya tamamen varsayılan ThemeConfig ile çalış:
    # my_cfg = ThemeConfig()
    #
    # 2) Ya da sadece küçük override (mevcut alanlar) ver:
    # (ÖNEMLİ: burada yeni renk icat etmiyoruz; ThemeConfig alanları zaten var.)
    my_cfg = ThemeConfig(
        # İstersen sadece scale/font_px gibi şeyleri değiştir:
        font_px=14,
        scale=1.0,
        # Renkleri boş bırakırsan theme_updated.py içindeki premium defaultlar kullanılır.
        # accent/bg/surface override etmiyorsan kaldırabilirsin.
    )

    # Temayı uygula (pencere oluşmadan önce)
    apply_theme(app, my_cfg)

    # Pencereyi göster
    win = ThemePreviewWindow()
    win.show()

    print(f"Theme loaded: {get_active_theme().font_family} | Accent: {get_active_theme().accent}")
    sys.exit(app.exec())
