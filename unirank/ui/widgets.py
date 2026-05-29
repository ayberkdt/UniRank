# assets/widgets.py

"""
Reusable UI widgets + delegates.

Key design goal:
- Keep this module resilient to theme schema drift. If ThemeConfig gains/loses
  fields, widgets should degrade gracefully instead of crashing the whole app.

If you see a "white window flashes then closes", it's usually because an exception
is thrown during a paintEvent or delegate paint() right after the first show().
"""

# ===================================================================
# 0.                         IMPORTS
# ===================================================================

from __future__ import annotations

import re
import math
import pandas as pd
from dataclasses import dataclass
from typing import Any, Callable, Optional, Dict, List, Tuple, Iterable, Union, Literal, Final, Sequence, Mapping


from PyQt6.QtCore import (
    QEasingCurve,
    QModelIndex,
    QPointF,
    QRect,
    QSize,
    Qt,
    QVariantAnimation,
    QTimer,
    pyqtSignal,
    QEvent,
    QPropertyAnimation,
    QPoint,
    QSignalBlocker,
    QRectF
)
from PyQt6.QtGui import (
    QBrush,
    QColor,
    QFont,
    QPainter,
    QPalette,
    QPen,
    QPolygonF,
    QRadialGradient,
    QKeyEvent,
    QMouseEvent,
    QPainterPath
)
from PyQt6.QtWidgets import (
    QGraphicsDropShadowEffect,
    QLabel,
    QPushButton,
    QStyle,
    QStyleOptionViewItem,
    QStyledItemDelegate,
    QWidget,
    QHBoxLayout,
    QFrame,
    QScrollArea,
    QFormLayout,
    QTextEdit,
    QSlider,
    QVBoxLayout,
    QLayout,
    QSizePolicy,
    QToolButton,
    QApplication,
    QDialog,
    QTableView,
    QVBoxLayout,
    QSizePolicy,
    QToolButton,
    QSpacerItem,
    QLineEdit,
    QTextBrowser,
    QToolTip,
    QLayoutItem,
    QWidgetItem
)



from unirank.ui.theme import ThemeConfig, get_active_theme, theme_tokens


# ===================================================================
# 2.                         COLOR UTILITIES
# ===================================================================

Number = Union[int, float]
Offset = Union[Tuple[int, int], int, float]


def clamp01(x: Number) -> float:
    """Clamp to [0, 1]."""
    x = float(x)
    return 0.0 if x < 0.0 else 1.0 if x > 1.0 else x


def clamp_int(x: Number, lo: int, hi: int) -> int:
    """Clamp numeric to [lo, hi] and cast to int."""
    xi = int(x)
    if xi < lo:
        return lo
    if xi > hi:
        return hi
    return xi


def lerp_int(a: int, b: int, t: Number) -> int:
    """Linear interpolate integers with rounding, t in [0,1]."""
    t = clamp01(t)
    return int(round(a + (b - a) * t))


def mix_color(a: QColor, b: QColor, t: Number, *, mix_alpha: bool = True) -> QColor:
    """Interpolate between two QColor."""
    t = clamp01(t)
    r = lerp_int(a.red(), b.red(), t)
    g = lerp_int(a.green(), b.green(), t)
    bl = lerp_int(a.blue(), b.blue(), t)

    if mix_alpha:
        al = lerp_int(a.alpha(), b.alpha(), t)
        return QColor(r, g, bl, al)

    return QColor(r, g, bl)


def _get_toks(theme: "ThemeConfig", toks: Optional[dict[str, Any]]) -> dict[str, Any]:
    # STRICT: toks yoksa theme_tokens(theme) çağrılır; theme bozuksa exception.
    return toks if toks is not None else theme_tokens(theme)


def goodness_to_color(
    g: float,
    theme: "ThemeConfig",
    *,
    toks: Optional[dict[str, Any]] = None,
) -> QColor:
    """
    g ∈ [0,1]
      1 → accent2 (iyi)
      0 → danger  (kötü)
    """
    toks = _get_toks(theme, toks)
    g = clamp01(g)

    bad = QColor(toks["danger"])
    good = QColor(toks["accent2"])
    return mix_color(bad, good, g)


def goodness_to_bg(
    g: float,
    theme: "ThemeConfig",
    alpha_mix: float = 0.78,
    *,
    toks: Optional[dict[str, Any]] = None,
) -> QColor:
    """
    Arkaplanda hafif bir tint üretir.
    alpha_mix: base ile tint karışım oranı (0=base, 1=tint)
    """
    toks = _get_toks(theme, toks)
    g = clamp01(g)
    alpha_mix = clamp01(alpha_mix)

    base = QColor(toks["bg"])
    danger = QColor(toks["danger"])
    accent2 = QColor(toks["accent2"])

    # bg → danger/accent2 yönünde küçük bir tint
    tint_bad = mix_color(base, danger, 0.22, mix_alpha=False)
    tint_good = mix_color(base, accent2, 0.22, mix_alpha=False)

    # kötü → iyi arası (g)
    tint = mix_color(tint_bad, tint_good, g, mix_alpha=False)

    # base ile tint'i karıştır (çok baskın olmasın)
    return mix_color(base, tint, alpha_mix, mix_alpha=False)


def is_selected(opt: QStyleOptionViewItem) -> bool:
    return bool(opt.state & QStyle.StateFlag.State_Selected)


def is_hover(opt: QStyleOptionViewItem) -> bool:
    return bool(opt.state & QStyle.StateFlag.State_MouseOver)


def _parse_offset(offset: Offset, default: Tuple[float, float] = (0.0, 6.0)) -> Tuple[float, float]:
    if isinstance(offset, (int, float)):
        return 0.0, float(offset)

    try:
        ox, oy = float(offset[0]), float(offset[1])
        return ox, oy
    except Exception:
        return default


def apply_shadow(
    widget: Optional[QWidget],
    *,
    color: str = "#000000",
    blur: Number = 22,
    alpha: Number = 90,
    offset: Offset = (0, 6),
    max_blur: float = 128.0,
) -> None:
    """
    Widget'a yumuşak gölge uygular (QGraphicsDropShadowEffect).
    - alpha: 0..255
    - blur:  0..max_blur
    - offset: (x, y) veya tek sayı (y kabul edilir, x=0)
    """
    if widget is None:
        return

    ox, oy = _parse_offset(offset)
    a = clamp_int(alpha, 0, 255)

    b = float(blur)
    if b < 0.0:
        b = 0.0
    elif b > float(max_blur):
        b = float(max_blur)

    qc = QColor(color)
    if not qc.isValid():
        qc = QColor("#000000")
    qc.setAlpha(a)

    eff = widget.graphicsEffect()
    if isinstance(eff, QGraphicsDropShadowEffect):
        shadow = eff
    else:
        shadow = QGraphicsDropShadowEffect(widget)
        widget.setGraphicsEffect(shadow)

    shadow.setColor(qc)
    shadow.setBlurRadius(b)
    shadow.setOffset(ox, oy)



# ===================================================================
# 3.                          BUTTONS
# ===================================================================

ButtonKind = Literal["primary", "danger", "secondary"]

_BUTTON_CLASS_PROP: Final[str] = "class"
_ALLOWED_KINDS: Final[set[str]] = {"primary", "danger", "secondary"}


def _repolish(w: QWidget) -> None:
    st = w.style()
    st.unpolish(w)
    st.polish(w)
    w.update()


def _normalize_kind(kind: str) -> str:
    # STRICT: boş/None/yanlış değer kabul etmiyoruz
    if kind is None:  # type: ignore[truthy-bool]
        raise ValueError("Button kind cannot be None")

    k = str(kind).strip().lower()
    if not k:
        raise ValueError("Button kind cannot be empty")
    if k not in _ALLOWED_KINDS:
        raise ValueError(f"Invalid button kind: {k!r}. Allowed: {sorted(_ALLOWED_KINDS)}")
    return k


class BaseButton(QPushButton):
    """QSS class property üzerinden stillenen temel buton (STRICT kind)."""

    def __init__(
        self,
        text: str = "",
        kind: ButtonKind = "secondary",
        parent: Optional[QWidget] = None,
    ):
        super().__init__(text, parent)
        self._kind: str = ""
        self.set_kind(kind)

    @property
    def kind(self) -> str:
        return self._kind

    def set_kind(self, kind: ButtonKind) -> None:
        k = _normalize_kind(kind)

        if k == self._kind:
            return

        self._kind = k
        self.setProperty(_BUTTON_CLASS_PROP, k)
        _repolish(self)


class PrimaryButton(BaseButton):
    def __init__(self, text: str = "", parent: Optional[QWidget] = None):
        super().__init__(text=text, kind="primary", parent=parent)


class DangerButton(BaseButton):
    def __init__(self, text: str = "", parent: Optional[QWidget] = None):
        super().__init__(text=text, kind="danger", parent=parent)


class SecondaryButton(BaseButton):
    def __init__(self, text: str = "", parent: Optional[QWidget] = None):
        super().__init__(text=text, kind="secondary", parent=parent)



# ===================================================================
# 4.                            BADGES
# ===================================================================


BadgeVariant = Literal["neutral", "primary", "danger"]


class PillBadge(QLabel):
    """
    Modern 'pill' badge.
    - theme verilmezse get_active_theme() kullanır.
    - theme_tokens(theme) ile STRICT token alır (theme bozuksa burada patlar).
    - variant: neutral / primary / danger
    """

    def __init__(
        self,
        text: str,
        theme: Optional[ThemeConfig] = None,
        parent: Optional[QWidget] = None,
        *,
        variant: BadgeVariant = "neutral",
        pad_x: int = 10,
        pad_y: int = 4,
        radius: int = 12,
        min_h: int = 24,
    ):
        super().__init__(text, parent)

        self._theme: ThemeConfig = theme if theme is not None else get_active_theme()
        self._toks: dict[str, Any] = theme_tokens(self._theme)

        self._variant: BadgeVariant = variant
        self._pad_x = clamp_int(pad_x, 6, 20)
        self._pad_y = clamp_int(pad_y, 2, 12)
        self._radius = clamp_int(radius, 8, 24)
        self._min_h = clamp_int(min_h, 18, 40)

        self.setProperty("class", "pill-badge")
        self.setProperty("variant", self._variant)

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setContentsMargins(self._pad_x, self._pad_y, self._pad_x, self._pad_y)
        self.setMinimumHeight(self._min_h)

        # “badge” hissi için: tek satır, elips
        self.setWordWrap(False)
        self.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
        self.setTextFormat(Qt.TextFormat.PlainText)

        self._apply_style()

    # -------- public API --------

    def set_theme(self, theme: ThemeConfig) -> None:
        self._theme = theme
        self._toks = theme_tokens(theme)  # STRICT
        self._apply_style()

    def set_variant(self, variant: BadgeVariant) -> None:
        if variant not in ("neutral", "primary", "danger"):
            raise ValueError(f"Invalid badge variant: {variant!r}")
        if variant == self._variant:
            return
        self._variant = variant
        self.setProperty("variant", variant)
        self._apply_style()

    def set_padding(self, pad_x: int, pad_y: int) -> None:
        self._pad_x = clamp_int(pad_x, 6, 24)
        self._pad_y = clamp_int(pad_y, 2, 14)
        self.setContentsMargins(self._pad_x, self._pad_y, self._pad_x, self._pad_y)
        self._apply_style()

    def set_radius(self, radius: int) -> None:
        self._radius = clamp_int(radius, 6, 28)
        self._apply_style()

    # -------- styling --------

    def _apply_style(self) -> None:
        t = self._toks

        # Semantik renk seçimi
        if self._variant == "primary":
            accent = t["accent2"]
            fg = t["text"]
            # Accent’i hafif transparan “chip” gibi kullanmak zor; QSS alpha hex destekler ama her tema hex değilse risk.
            # O yüzden güvenli: surface2 taban + accent border
            bg = t["surface2"]
            border = accent
        elif self._variant == "danger":
            fg = t["text"]
            bg = t["surface2"]
            border = t["danger"]
        else:  # neutral
            fg = t["text_muted"] if "text_muted" in t else t["text"]
            bg = t["surface2"]
            border = t["border"]

        font_px = int(t.get("font_px", 12))

        # İpucu: “ürün kalitesi” için hafif letter-spacing + daha yumuşak border
        qss = f"""
        QLabel[class="pill-badge"] {{
            color: {fg};
            background-color: {bg};
            border: 1px solid {border};
            border-radius: {self._radius}px;
            padding: 0px; /* içerik margin ile yönetiliyor */
            font-weight: 700;
            font-size: {max(10, font_px - 1)}px;
            letter-spacing: 0.2px;
        }}

        /* Hover (çok hafif): özellikle tıklanabilir badge'lerde premium his verir */
        QLabel[class="pill-badge"]:hover {{
            border-width: 1px;
        }}
        """
        self.setStyleSheet(qss)
        _repolish(self)



# ===================================================================
# 5.                         RANKING WIDGETS
# ===================================================================

def _round_to_step(x: float, step: float) -> float:
    if step <= 0:
        raise ValueError("step must be > 0")
    return round(x / step) * step


class WeightSliderRow(QWidget):
    """
    0..1 aralığında yatay slider + sağda değer etiketi.

    - step: slider hassasiyeti (örn 0.01)
    - valueChanged: kullanıcı değiştirince yayınlar (programatik setValue spam yapmaz)
    - optional reset: tek tıkla varsayılan değere dönüş
    """
    valueChanged = pyqtSignal(float)

    def __init__(
        self,
        title: str,
        value: float = 0.5,
        *,
        step: float = 0.01,
        default: Optional[float] = None,
        show_reset: bool = True,
        parent: Optional[QWidget] = None,
    ):
        super().__init__(parent)

        self._step = float(step)
        if self._step <= 0:
            raise ValueError("step must be > 0")
        # çok küçük step UI’da anlamsız tick sayısı yaratır; strict ama mantıklı alt sınır:
        if self._step < 0.001:
            raise ValueError("step too small (min 0.001)")

        self._max_ticks = int(round(1.0 / self._step))
        if self._max_ticks <= 0:
            raise ValueError("invalid step; produced non-positive tick count")

        self._default = None if default is None else clamp01(float(default))

        lay = QHBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(10)

        # Sol başlık
        self.lbl = QLabel(title)
        self.lbl.setMinimumWidth(150)
        self.lbl.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        self.lbl.setToolTip(title)

        # Slider
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(0, self._max_ticks)
        self.slider.setSingleStep(1)
        self.slider.setPageStep(max(1, int(round(0.05 / self._step))))
        self.slider.setTracking(True)  # sürüklerken anlık güncelle

        # Sağ değer etiketi (monospace benzeri hizalı görünüm)
        self.value_lbl = QLabel("0.00")
        self.value_lbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.value_lbl.setFixedWidth(56)
        self.value_lbl.setToolTip("Current value")

        # Reset butonu (opsiyonel)
        self.btn_reset: Optional[QToolButton] = None
        if show_reset and self._default is not None:
            btn = QToolButton()
            btn.setText("↺")
            btn.setToolTip("Reset to default")
            btn.setAutoRaise(True)
            btn.clicked.connect(self._on_reset_clicked)
            self.btn_reset = btn

        lay.addWidget(self.lbl)
        lay.addWidget(self.slider, 1)
        lay.addWidget(self.value_lbl)
        if self.btn_reset is not None:
            lay.addWidget(self.btn_reset)

        # Sinyal
        self.slider.valueChanged.connect(self._on_slider_changed)

        # İlk değer set (programatik)
        self.setValue(value, emit=False)

        # Erişilebilirlik (küçük ama profesyonel dokunuş)
        self.setAccessibleName(f"Weight: {title}")
        self.slider.setAccessibleName(f"{title} slider")
        self.value_lbl.setAccessibleName(f"{title} value")

        self._apply_style()

    # ---- Public API ----

    def value(self) -> float:
        """Return current value in [0,1] snapped to step."""
        return self.slider.value() * self._step

    def setValue(self, v: float, *, emit: bool = False) -> None:
        """
        Set value in [0,1]. Value is snapped to step.
        emit=False by default to avoid signal spam on programmatic updates.
        """
        v = clamp01(float(v))
        v = clamp01(_round_to_step(v, self._step))

        ticks = int(round(v / self._step))
        ticks = max(0, min(self._max_ticks, ticks))

        # UI güncelle
        with QSignalBlocker(self.slider):
            self.slider.setValue(ticks)

        self._sync_label(ticks)

        if emit:
            self.valueChanged.emit(self.value())

    def setDefault(self, default: Optional[float]) -> None:
        self._default = None if default is None else clamp01(float(default))
        if self.btn_reset is not None:
            self.btn_reset.setVisible(self._default is not None)

    # ---- Internals ----

    def _sync_label(self, ticks: int) -> None:
        val = ticks * self._step
        self.value_lbl.setText(f"{val:.2f}")

    def _on_slider_changed(self, ticks: int) -> None:
        self._sync_label(ticks)
        self.valueChanged.emit(self.value())

    def _on_reset_clicked(self) -> None:
        if self._default is None:
            return
        # reset kullanıcı aksiyonu olduğu için emit=True
        self.setValue(self._default, emit=True)

    def _apply_style(self) -> None:
        # Minimal ve profesyonel: sadece spacing/typography hissi
        # Tema/QSS’in varsa bunu global QSS’e de taşıyabilirsin.
        self.setStyleSheet("""
            QLabel { font-weight: 600; }
        """)


def _mk_kv_value(text: str, *, muted: bool = False) -> QLabel:
    lbl = QLabel(text)
    lbl.setWordWrap(True)
    lbl.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
    lbl.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
    if muted:
        lbl.setProperty("muted", "1")
    return lbl


def _mk_text_block() -> QTextBrowser:
    tb = QTextBrowser()
    tb.setOpenExternalLinks(True)
    tb.setFrameShape(QFrame.Shape.NoFrame)
    tb.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    tb.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
    tb.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse | Qt.TextInteractionFlag.LinksAccessibleByMouse)
    tb.setMinimumHeight(66)
    tb.setProperty("block", "1")
    return tb


class DetailsDrawer(QFrame):
    """
    Premium sağ drawer:
    - Slide-in / slide-out animasyon
    - Kapanma gecikmesi (hover geçişinde flash yok)
    - Temadan token alır (strict)
    """

    def __init__(self, theme: Optional[ThemeConfig] = None, parent: Optional[QWidget] = None):
        super().__init__(parent)

        self._theme: ThemeConfig = theme if theme is not None else get_active_theme()
        self._toks = theme_tokens(self._theme)  # STRICT

        self.setObjectName("DetailsDrawer")
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setMouseTracking(True)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self._hovering = False
        self._pending_close = False

        # close delay
        self._close_timer = QTimer(self)
        self._close_timer.setSingleShot(True)
        self._close_timer.timeout.connect(self._maybe_close_after_delay)

        # animation
        self._anim = QPropertyAnimation(self, b"geometry", self)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._anim.setDuration(180)
        self._anim.finished.connect(self._on_anim_finished)
        self._hide_after_anim = False

        # ---------- UI ----------
        outer = QVBoxLayout(self)
        outer.setContentsMargins(14, 14, 14, 14)
        outer.setSpacing(12)

        # Header
        header = QHBoxLayout()
        header.setContentsMargins(0, 0, 0, 0)
        header.setSpacing(10)

        self.lbl_title = QLabel("Detay")
        self.lbl_title.setObjectName("DrawerTitle")
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        self.lbl_title.setFont(title_font)

        self.lbl_subtitle = QLabel("")
        self.lbl_subtitle.setObjectName("DrawerSubtitle")
        self.lbl_subtitle.setProperty("muted", "1")
        self.lbl_subtitle.setWordWrap(True)

        title_col = QVBoxLayout()
        title_col.setContentsMargins(0, 0, 0, 0)
        title_col.setSpacing(2)
        title_col.addWidget(self.lbl_title)
        title_col.addWidget(self.lbl_subtitle)

        header.addLayout(title_col, 1)

        # Premium close: icon-like tool button
        self.btn_close = QToolButton()
        self.btn_close.setText("✕")
        self.btn_close.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_close.setAutoRaise(True)
        self.btn_close.setObjectName("DrawerCloseBtn")
        self.btn_close.clicked.connect(self.request_hide)

        header.addWidget(self.btn_close)
        outer.addLayout(header)

        # Radar (centered card feel)
        self.radar = RadarChart(theme=self._theme)
        self.radar.setMinimumSize(280, 280)
        self.radar.setProperty("card", "1")
        outer.addWidget(self.radar, 0, Qt.AlignmentFlag.AlignHCenter)

        # Scroll body
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setObjectName("DrawerScroll")

        body = QWidget()
        body.setObjectName("DrawerBody")
        scroll.setWidget(body)

        form = QFormLayout(body)
        form.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        form.setFormAlignment(Qt.AlignmentFlag.AlignTop)
        form.setHorizontalSpacing(12)
        form.setVerticalSpacing(10)

        # KV labels
        self.lbl_uni = _mk_kv_value("-")
        self.lbl_city = _mk_kv_value("-")
        self.lbl_score = _mk_kv_value("-")
        self.lbl_src = _mk_kv_value("-", muted=True)

        # Text blocks (premium card-like)
        self.txt_strength = _mk_text_block()
        self.txt_pros = _mk_text_block()
        self.txt_cons = _mk_text_block()
        self.txt_focus = _mk_text_block()

        form.addRow(self._mk_field_label("Üniversite"), self.lbl_uni)
        form.addRow(self._mk_field_label("Şehir"), self.lbl_city)
        form.addRow(self._mk_field_label("Skor"), self.lbl_score)
        form.addRow(self._mk_field_label("Kaynak"), self.lbl_src)

        form.addRow(self._mk_section_label("Özet"), QWidget())
        form.addRow(self._mk_field_label("Güçlü tarafı"), self.txt_strength)
        form.addRow(self._mk_field_label("Avantaj"), self.txt_pros)
        form.addRow(self._mk_field_label("Dezavantaj"), self.txt_cons)
        form.addRow(self._mk_field_label("Güçlü alanlar"), self.txt_focus)

        outer.addWidget(scroll, 1)

        # Shadow (temaya uygun olsun)
        apply_shadow(self, color="#000000", alpha=110, blur=26, offset=(0, 10))

        self._apply_style()
        self.hide()

    # ---------- helpers ----------
    def _mk_field_label(self, text: str) -> QLabel:
        lbl = QLabel(text + ":")
        lbl.setProperty("fieldLabel", "1")
        lbl.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        return lbl

    def _mk_section_label(self, text: str) -> QLabel:
        lbl = QLabel(text)
        lbl.setProperty("sectionLabel", "1")
        lbl.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        return lbl

    def _apply_style(self) -> None:
        t = self._toks
        # Premium: yuvarlak köşe + surface + ince border
        # Text blocks: surface2 üstüne hafif border, padding, radius
        self.setStyleSheet(f"""
        QFrame#DetailsDrawer {{
            background-color: {t["surface"]};
            border: 1px solid {t["border"]};
            border-radius: 18px;
        }}

        QLabel#DrawerTitle {{
            color: {t["text"]};
        }}
        QLabel#DrawerSubtitle {{
            color: {t["text_muted"]};
        }}

        QLabel[fieldLabel="1"] {{
            color: {t["text_muted"]};
            font-weight: 600;
            padding-top: 2px;
        }}

        QLabel[sectionLabel="1"] {{
            color: {t["text"]};
            font-weight: 800;
            padding-top: 6px;
        }}

        QLabel[muted="1"] {{
            color: {t["text_muted"]};
        }}

        QToolButton#DrawerCloseBtn {{
            color: {t["text_muted"]};
            background: transparent;
            border-radius: 10px;
            padding: 6px 8px;
        }}
        QToolButton#DrawerCloseBtn:hover {{
            color: {t["text"]};
            background-color: {t["surface2"]};
        }}

        QTextBrowser[block="1"] {{
            color: {t["text"]};
            background-color: {t["surface2"]};
            border: 1px solid {t["border"]};
            border-radius: 14px;
            padding: 10px 10px;
        }}
        """)
        _repolish(self)

    # ---------- hover ----------
    def enterEvent(self, e):
        self._hovering = True
        self._pending_close = False
        self._close_timer.stop()
        return super().enterEvent(e)

    def leaveEvent(self, e):
        self._hovering = False
        self.request_close(delay_ms=220)
        return super().leaveEvent(e)

    def is_hovering(self) -> bool:
        return bool(self._hovering)

    # ---------- close orchestration ----------
    def request_close(self, delay_ms: int = 220) -> None:
        self._pending_close = True
        self._close_timer.start(max(0, int(delay_ms)))

    def cancel_close(self) -> None:
        self._pending_close = False
        self._close_timer.stop()

    def _maybe_close_after_delay(self) -> None:
        if self._pending_close and (not self.is_hovering()):
            self.request_hide()
        self._pending_close = False

    # ---------- show/hide with animation ----------
    def show_at_right(self, *, width: int = 440, margin: int = 18, animate: bool = True) -> None:
        parent = self.parentWidget()
        if parent is None:
            self.show()
            return

        w = int(width)
        m = int(margin)
        x = max(0, parent.width() - w - m)
        y = m
        h = max(160, parent.height() - 2 * m)

        target = self.geometry()
        target.setX(x)
        target.setY(y)
        target.setWidth(w)
        target.setHeight(h)

        # başlangıç: sağdan biraz dışarıda
        start = target
        start = start.adjusted(28, 0, 28, 0)

        self._hide_after_anim = False
        self.raise_()
        self.show()

        if not animate:
            self.setGeometry(target)
            return

        self._anim.stop()
        self._anim.setStartValue(start)
        self._anim.setEndValue(target)
        self._anim.start()

    def request_hide(self, *, animate: bool = True) -> None:
        if not self.isVisible():
            return
        if not animate:
            self.hide()
            return

        # hedef: sağa kaydırarak çık
        cur = self.geometry()
        end = cur.adjusted(28, 0, 28, 0)

        self._hide_after_anim = True
        self._anim.stop()
        self._anim.setStartValue(cur)
        self._anim.setEndValue(end)
        self._anim.start()

    def _on_anim_finished(self) -> None:
        if self._hide_after_anim:
            self.hide()
            self._hide_after_anim = False

    # ---------- data binding ----------
    def set_record(self, data: Dict[str, Any]) -> None:
        uni = str(data.get("university") or "-")
        city = str(data.get("city") or "-")
        score = data.get("score", "-")
        source = str(data.get("source") or "-")

        self.lbl_title.setText(uni if uni != "-" else "Detay")
        self.lbl_subtitle.setText(city if city != "-" else "")

        self.lbl_uni.setText(uni)
        self.lbl_city.setText(city)
        self.lbl_score.setText(str(score))
        self.lbl_src.setText(source)

        self.txt_strength.setPlainText(str(data.get("strength") or ""))
        self.txt_pros.setPlainText(str(data.get("pros") or ""))
        self.txt_cons.setPlainText(str(data.get("cons") or ""))
        self.txt_focus.setPlainText(str(data.get("focus") or ""))

        labels = data.get("radar_labels")
        values = data.get("radar_values")
        if isinstance(labels, list) and isinstance(values, list) and len(labels) == len(values) and len(labels) > 0:
            try:
                vals = [clamp01(float(v)) for v in values]
                self.radar.set_data([str(x) for x in labels], vals)
            except Exception:
                # Radar datası bozuksa: sessizce geç (UI kırılmasın)
                pass


class DetailHoverButton(SecondaryButton):
    """
    Premium hover button:
    - callback yerine Qt signal (daha profesyonel)
    - stillenebilir QSS property
    """
    hovered = pyqtSignal(int)
    unhovered = pyqtSignal()

    def __init__(self, row: int, parent: Optional[QWidget] = None):
        super().__init__("Detay", parent=parent)
        self._row = int(row)

        self.setProperty("class", "detail-hover")
        self.setFixedWidth(78)
        self.setFixedHeight(30)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMouseTracking(True)

    def row(self) -> int:
        return self._row

    def enterEvent(self, e):
        self.hovered.emit(self._row)
        return super().enterEvent(e)

    def leaveEvent(self, e):
        self.unhovered.emit()
        return super().leaveEvent(e)



# ===================================================================
# 6.                          DELEGATES
# ===================================================================

def _parse_float(x: Any) -> Optional[float]:
    try:
        v = float(x)
    except Exception:
        return None
    if not math.isfinite(v):
        return None
    return v


def _rounded_rect_path(rect, radius: float) -> QPainterPath:
    """
    QRect/QRectF kabul eder, içerde QRectF'e çevirip güvenli rounded path döndürür.
    """
    r = QRectF(rect)  # <-- KRİTİK: QRect -> QRectF dönüşümü
    rad = max(0.0, float(radius))
    rad = min(rad, min(r.width(), r.height()) * 0.5)

    path = QPainterPath()
    if r.isEmpty():
        return path

    path.addRoundedRect(r, rad, rad, Qt.SizeMode.AbsoluteSize)
    return path


def _overlay_fill(p: QPainter, rect: QRect, color: QColor, radius: int = 10) -> None:
    """Premium hover overlay: rounded + antialias."""
    p.save()
    p.setRenderHint(QPainter.RenderHint.Antialiasing, True)
    p.setPen(Qt.PenStyle.NoPen)
    p.setBrush(QBrush(color))
    p.drawPath(_rounded_rect_path(rect, float(radius)))
    p.restore()


class HeatmapDelegate(QStyledItemDelegate):
    """
    Satır bazlı goodness (0..1) değerine göre yazı/arkaplan renklendirir.
    - Native selection/hover/focus korunur.
    - Seçili değilse: opsiyonel background tint + text color mapping
    - Hover: yuvarlak overlay ile premium hissi
    """

    def __init__(
        self,
        goodness_getter: Callable[[QModelIndex], Optional[float]],
        theme: Optional[ThemeConfig] = None,
        parent: Optional[QWidget] = None,
        *,
        tint_background: bool = True,
        hover_overlay_alpha: int = 18,
        hover_radius: int = 10,
    ):
        super().__init__(parent)
        self.goodness_getter = goodness_getter

        self._theme = theme if theme is not None else get_active_theme()
        self._toks = theme_tokens(self._theme)  # STRICT

        self.tint_background = bool(tint_background)
        self.hover_overlay_alpha = max(0, min(255, int(hover_overlay_alpha)))
        self.hover_radius = max(0, int(hover_radius))

    def set_theme(self, theme: ThemeConfig) -> None:
        self._theme = theme
        self._toks = theme_tokens(theme)  # STRICT

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex) -> None:
        g = self.goodness_getter(index)
        if g is None:
            return super().paint(painter, option, index)

        g = clamp01(g)

        opt = QStyleOptionViewItem(option)
        self.initStyleOption(opt, index)

        selected = bool(opt.state & QStyle.StateFlag.State_Selected)
        hovered = bool(opt.state & QStyle.StateFlag.State_MouseOver)

        # Only adjust palette/background when NOT selected (selection color should win)
        if not selected:
            if self.tint_background:
                bg = goodness_to_bg(g, self._theme, alpha_mix=0.80, toks=self._toks)
                opt.backgroundBrush = QBrush(bg)

            fg = goodness_to_color(g, self._theme, toks=self._toks)
            opt.palette.setColor(QPalette.ColorRole.Text, fg)
            opt.palette.setColor(QPalette.ColorRole.WindowText, fg)

        # Native draw (keeps focus/selection/hover mechanics)
        widget = opt.widget
        style = widget.style() if widget else QApplication.style()  # type: ignore[name-defined]
        style.drawControl(QStyle.ControlElement.CE_ItemViewItem, opt, painter, widget)

        # Premium hover overlay (only if not selected)
        if hovered and not selected and self.hover_overlay_alpha > 0:
            overlay = QColor(self._toks["accent2"])
            overlay.setAlpha(self.hover_overlay_alpha)

            r = opt.rect.adjusted(2, 2, -2, -2)
            _overlay_fill(painter, r, overlay, radius=self.hover_radius)


class ScoreBarDelegate(QStyledItemDelegate):
    """
    Hücre arkasında pill progress bar çizer (0..1).
    - Native selection/hover paneli korunur.
    - Bar + text overlay ile premium görünüm.
    """

    def __init__(
        self,
        score_getter: Callable[[QModelIndex], Optional[float]],
        *,
        normalize: bool = True,
        theme: Optional[ThemeConfig] = None,
        parent: Optional[QWidget] = None,
        bg_alpha: int = 175,
        border_alpha: int = 175,
        pad_x: int = 10,
        pad_y: int = 8,
        radius: Optional[int] = None,
    ):
        super().__init__(parent)

        self.score_getter = score_getter
        self.normalize = bool(normalize)

        self._theme = theme if theme is not None else get_active_theme()
        self._toks = theme_tokens(self._theme)  # STRICT

        self.bg_alpha = max(0, min(255, int(bg_alpha)))
        self.border_alpha = max(0, min(255, int(border_alpha)))
        self.pad_x = max(0, int(pad_x))
        self.pad_y = max(0, int(pad_y))
        self.radius = radius  # None => auto

    def set_theme(self, theme: ThemeConfig) -> None:
        self._theme = theme
        self._toks = theme_tokens(theme)  # STRICT

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex) -> None:
        opt = QStyleOptionViewItem(option)
        self.initStyleOption(opt, index)

        widget = opt.widget
        style = widget.style() if widget else QApplication.style()  # type: ignore[name-defined]

        # First draw native item (selection/hover background, focus rect, etc.)
        style.drawControl(QStyle.ControlElement.CE_ItemViewItem, opt, painter, widget)

        raw = self.score_getter(index)
        if raw is None:
            return  # native draw already done

        s = _parse_float(raw)
        if s is None:
            s = 0.0
        if self.normalize:
            s = clamp01(s)

        # Geometry
        rect = opt.rect.adjusted(self.pad_x, self.pad_y, -self.pad_x, -self.pad_y)
        if rect.width() <= 4 or rect.height() <= 4:
            return

        bar_h = max(18, int(rect.height() * 0.58))
        bar_y = rect.y() + (rect.height() - bar_h) // 2
        bar = QRect(rect.x(), bar_y, rect.width(), bar_h)

        # Auto radius
        rad = int(bar_h // 2) if self.radius is None else max(0, int(self.radius))

        t = self._toks
        base_bg = QColor(t["surface2"])
        base_bg.setAlpha(self.bg_alpha)

        border = QColor(t["border"])
        border.setAlpha(self.border_alpha)

        selected = bool(opt.state & QStyle.StateFlag.State_Selected)

        # Paint bar capsule
        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

        # When selected, keep bar more subtle (selection should dominate)
        if selected:
            base_bg.setAlpha(min(self.bg_alpha, 120))
            border.setAlpha(min(self.border_alpha, 120))

        painter.setPen(QPen(border, 1))
        painter.setBrush(QBrush(base_bg))
        painter.drawPath(_rounded_rect_path(bar, float(rad)))

        # Fill
        fill_w = int(bar.width() * s)
        if fill_w > 0:
            fill_rect = QRect(bar.x(), bar.y(), fill_w, bar.height())
            fill_col = goodness_to_color(s, self._theme, toks=t)

            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(fill_col))
            painter.drawPath(_rounded_rect_path(fill_rect, float(rad)))

        painter.restore()

        # Text overlay (left aligned, bold)
        txt = index.data(Qt.ItemDataRole.DisplayRole)
        if txt is None:
            txt = f"{s:.3f}"

        painter.save()
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing, True)

        font = QFont(opt.font)
        font.setBold(True)
        painter.setFont(font)

        text_color = QColor(t["text"])
        if selected:
            # selection palette already used; keep readable
            text_color = opt.palette.color(QPalette.ColorRole.HighlightedText)

        painter.setPen(QPen(text_color))

        text_rect = opt.rect.adjusted(self.pad_x + 2, 0, -self.pad_x, 0)
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft, str(txt))

        painter.restore()

    def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex) -> QSize:
        sz = super().sizeHint(option, index)
        return QSize(sz.width(), max(36, sz.height()))


def apply_ranking_delegates(
    table: QWidget,  # QTableView
    col_map: dict[str, int],
    goodness_provider: Callable[[int, str], Optional[float]],
    theme: Optional[ThemeConfig] = None,
) -> None:
    """
    table: QTableView
    col_map: {"Masraf(şehir)": col_idx, "Semester fee (€)": col_idx, "Hedefe uyum": col_idx, "Skor": col_idx}
    goodness_provider(row, key) -> 0..1
      keys: "cost_good", "fee_good", "fit_good", "score_good"
    """
    theme = theme if theme is not None else get_active_theme()

    # Delegate cache (lifetime managed by parent=table)
    cache = getattr(table, "_ranking_delegates", None)
    if not isinstance(cache, dict):
        cache = {}
        setattr(table, "_ranking_delegates", cache)

    def get_heatmap(key: str) -> HeatmapDelegate:
        dkey = f"heatmap:{key}"
        d = cache.get(dkey)
        if isinstance(d, HeatmapDelegate):
            d.set_theme(theme)
            return d

        def getter(index: QModelIndex) -> Optional[float]:
            return goodness_provider(index.row(), key)

        d = HeatmapDelegate(
            getter,
            theme=theme,
            parent=table,
            tint_background=True,
            hover_overlay_alpha=18,
            hover_radius=10,
        )
        cache[dkey] = d
        return d

    def get_scorebar() -> ScoreBarDelegate:
        dkey = "scorebar"
        d = cache.get(dkey)
        if isinstance(d, ScoreBarDelegate):
            d.set_theme(theme)
            return d

        def score_getter(index: QModelIndex) -> Optional[float]:
            sg = goodness_provider(index.row(), "score_good")
            v = _parse_float(sg) if sg is not None else None
            if v is not None:
                return v
            return _parse_float(index.data(Qt.ItemDataRole.DisplayRole))

        d = ScoreBarDelegate(
            score_getter=score_getter,
            normalize=True,
            theme=theme,
            parent=table,
            bg_alpha=175,
            border_alpha=175,
            pad_x=10,
            pad_y=8,
            radius=None,
        )
        cache[dkey] = d
        return d

    # Column → goodness key mapping
    heatmap_cols = {
        "Masraf(şehir)": "cost_good",
        "Tuition & Fees (€)": "fee_good",
        "Hedefe uyum": "fit_good",
    }

    for col_name, key in heatmap_cols.items():
        col = col_map.get(col_name)
        if isinstance(col, int) and col >= 0:
            table.setItemDelegateForColumn(col, get_heatmap(key))  # type: ignore[attr-defined]

    col_score = col_map.get("Skor")
    if isinstance(col_score, int) and col_score >= 0:
        table.setItemDelegateForColumn(col_score, get_scorebar())  # type: ignore[attr-defined]



# ===================================================================
# 7.                          RADARCHART
# ===================================================================

@dataclass(frozen=True)
class Metric:
    key: str
    label: str
    value: float                  # 0..1
    hint: str = ""                # tooltip / short explanation
    unit: str = ""                # e.g. "%", "€", "score"
    fmt: str = "{:.0%}"           # display format for value label (0..1)


def _safe_float(x: Any, default: float = 0.0) -> float:
    try:
        v = float(x)
        if not math.isfinite(v):
            return default
        return v
    except Exception:
        return default


class RadarChart(QWidget):
    """
    Premium Radar Chart:
    - Metric tabanlı API (label + value + hint + format)
    - Legend (Main / Compare)
    - Ring ölçek etiketleri (0.2..1.0)
    - Eksen uçlarında değer etiketleri (örn. 0.78)
    - Hover: metrik highlight + tooltip
    - Animated transitions
    """

    def __init__(self, theme: Optional[ThemeConfig] = None, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._theme = theme if theme is not None else get_active_theme()
        self._toks = theme_tokens(self._theme)  # STRICT

        self.setMouseTracking(True)
        self.setMinimumSize(320, 320)

        # Data model
        self._metrics: list[Metric] = []
        self._compare_label: str = ""
        self._main_label: str = "Skor Profili"
        self._compare_values: list[float] = []

        # Animation state
        self._anim_main: list[float] = []
        self._anim_compare: list[float] = []
        self._start_main: list[float] = []
        self._start_compare: list[float] = []
        self._target_main: list[float] = []
        self._target_compare: list[float] = []

        # Hover state (index of metric)
        self._hover_idx: int = -1
        self._last_geom: dict[str, Any] = {}  # cache: positions for hover

        self.anim = QVariantAnimation(self)
        self.anim.setDuration(650)
        self.anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.anim.valueChanged.connect(self._on_anim_step)

    # -------------------------
    # Theme
    # -------------------------
    def set_theme(self, theme: ThemeConfig) -> None:
        self._theme = theme
        self._toks = theme_tokens(theme)  # STRICT
        self.update()

    # -------------------------
    # Public API (preferred)
    # -------------------------
    def set_metrics(
        self,
        metrics: Sequence[Metric],
        *,
        title: str = "Skor Profili",
        compare_values: Optional[Sequence[float]] = None,
        compare_label: str = "Karşılaştırma",
    ) -> None:
        if not metrics:
            self.clear()
            return

        m_list = list(metrics)
        main_vals = [clamp01(m.value) for m in m_list]

        cmp_vals: list[float] = []
        if compare_values is not None:
            cv = list(compare_values)
            if len(cv) == len(main_vals):
                cmp_vals = [clamp01(_safe_float(v, 0.0)) for v in cv]

        self._metrics = m_list
        self._main_label = str(title or "Skor Profili")
        self._compare_label = str(compare_label or "Karşılaştırma")
        self._set_targets(main_vals, cmp_vals)

    # -------------------------
    # Backward compatible API
    # -------------------------
    def set_data(self, labels: list[str], main_values: list[float], compare_values: Optional[list[float]] = None) -> None:
        if not labels or len(labels) != len(main_values):
            self.clear()
            return
        metrics = [
            Metric(key=f"m{i}", label=str(lbl), value=clamp01(v), fmt="{:.0%}")
            for i, (lbl, v) in enumerate(zip(labels, main_values))
        ]
        self.set_metrics(metrics, title="Skor Profili", compare_values=compare_values, compare_label="Karşılaştırma")

    def clear(self) -> None:
        self._metrics = []
        self._compare_values = []
        self._anim_main = []
        self._anim_compare = []
        self._target_main = []
        self._target_compare = []
        self.anim.stop()
        self.update()

    # -------------------------
    # Internals: animation target setup
    # -------------------------
    def _set_targets(self, target_main: list[float], target_compare: list[float]) -> None:
        # First-time or dimension change: jump
        if len(self._anim_main) != len(target_main):
            self._anim_main = list(target_main)
            self._anim_compare = list(target_compare) if target_compare else []
            self._target_main = list(target_main)
            self._target_compare = list(target_compare)
            self.anim.stop()
            self.update()
            return

        self._start_main = list(self._anim_main) if self._anim_main else [0.0] * len(target_main)
        self._target_main = list(target_main)

        if target_compare:
            if len(self._anim_compare) != len(target_compare):
                self._anim_compare = [0.0] * len(target_compare)
            self._start_compare = list(self._anim_compare)
            self._target_compare = list(target_compare)
        else:
            self._start_compare = list(self._anim_compare) if self._anim_compare else [0.0] * len(target_main)
            self._target_compare = []
            self._anim_compare = []

        self.anim.stop()
        self.anim.setStartValue(0.0)
        self.anim.setEndValue(1.0)
        self.anim.start()

    def _on_anim_step(self, value: Any) -> None:
        progress = clamp01(_safe_float(value, 1.0))

        self._anim_main = [s + (t - s) * progress for s, t in zip(self._start_main, self._target_main)]

        if self._target_compare:
            start_c = self._start_compare if len(self._start_compare) == len(self._target_compare) else [0.0] * len(self._target_compare)
            self._anim_compare = [s + (t - s) * progress for s, t in zip(start_c, self._target_compare)]
        else:
            self._anim_compare = []

        self.update()

    # -------------------------
    # Hover (premium clarity)
    # -------------------------
    def mouseMoveEvent(self, e) -> None:
        if not self._metrics or "points" not in self._last_geom:
            return super().mouseMoveEvent(e)

        pos = e.position()
        pts: list[QPointF] = self._last_geom["points"]

        # pick nearest vertex within threshold
        best = -1
        best_d2 = 1e18
        for i, p in enumerate(pts):
            dx = p.x() - pos.x()
            dy = p.y() - pos.y()
            d2 = dx * dx + dy * dy
            if d2 < best_d2:
                best_d2 = d2
                best = i

        threshold2 = 14.0 * 14.0
        new_idx = best if best_d2 <= threshold2 else -1

        if new_idx != self._hover_idx:
            self._hover_idx = new_idx
            if new_idx >= 0:
                m = self._metrics[new_idx]
                val = self._anim_main[new_idx] if new_idx < len(self._anim_main) else m.value
                try:
                    vtxt = m.fmt.format(val)
                except Exception:
                    vtxt = f"{val:.2f}"
                tip = f"{m.label}: {vtxt}"
                if m.unit:
                    tip = f"{m.label}: {vtxt} {m.unit}".strip()
                if m.hint:
                    tip += f"\n{m.hint}"
                QToolTip.showText(e.globalPosition().toPoint(), tip, self)
            else:
                QToolTip.hideText()
            self.update()

        return super().mouseMoveEvent(e)

    def leaveEvent(self, e) -> None:
        self._hover_idx = -1
        QToolTip.hideText()
        self.update()
        return super().leaveEvent(e)

    # -------------------------
    # Paint
    # -------------------------
    def paintEvent(self, event) -> None:
        if not self._anim_main:
            return

        try:
            t = self._toks
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

            w, h = self.width(), self.height()
            center = QPointF(w / 2, h / 2)

            # Layout regions
            top_pad = 34  # room for title + legend
            bottom_pad = 18
            left_pad = 18
            right_pad = 18

            # radius: leave room for labels around
            usable = min(w - left_pad - right_pad, h - top_pad - bottom_pad)
            radius = max(60.0, usable * 0.33)

            n = max(3, len(self._anim_main))
            angle_step = (2.0 * math.pi) / n
            start_angle = -math.pi / 2.0

            # Colors
            c_bg = QColor(t["bg"])
            c_surface = QColor(t["surface"])
            c_surface2 = QColor(t["surface2"])
            c_border = QColor(t["border"])
            c_text = QColor(t["text"])
            c_text_muted = QColor(t["text_muted"])
            c_accent = QColor(t["accent2"] if "accent2" in t else t["accent"])

            c_compare = QColor(c_text_muted)
            c_compare.setAlpha(110)

            # --- Title + Legend ---
            painter.save()
            font_title = QFont(str(t.get("font_family", QFont().family())), max(10, int(t.get("font_px", 12)) + 1))
            font_title.setBold(True)
            painter.setFont(font_title)
            painter.setPen(c_text)

            title_rect = QRect(0, 8, w, 20)
            painter.drawText(title_rect, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter, self._main_label)

            # Legend (right-aligned small)
            font_leg = QFont(font_title)
            font_leg.setBold(False)
            font_leg.setPointSize(max(9, font_title.pointSize() - 2))
            painter.setFont(font_leg)
            y_leg = 26

            # main swatch
            sw = 10
            x = w - 16
            def legend_item(label: str, col: QColor) -> int:
                nonlocal x
                if not label:
                    return x
                metrics = painter.fontMetrics()
                tw = metrics.horizontalAdvance(label)
                x -= tw
                painter.setPen(c_text_muted)
                painter.drawText(QRect(x, y_leg-8, tw, 16), Qt.AlignmentFlag.AlignVCenter, label)
                x -= (sw + 8)
                painter.setPen(Qt.PenStyle.NoPen)
                painter.setBrush(QBrush(col))
                painter.drawRoundedRect(QRect(x, y_leg-5, sw, sw), 3, 3)
                x -= 14
                return x

            legend_item("Ana", c_accent)
            if self._anim_compare:
                legend_item(self._compare_label or "Karşılaştırma", c_compare)

            painter.restore()

            # Shift center down a bit (due to title)
            center = QPointF(center.x(), center.y() + 10)

            # --- Rings with scale labels ---
            levels = (1.0, 0.8, 0.6, 0.4, 0.2)
            ring_pen = QPen(c_border, 1)
            ring_pen.setCosmetic(True)
            painter.setPen(ring_pen)

            # ring fills
            for i, scale in enumerate(levels):
                rr = radius * scale
                poly = QPolygonF()
                for j in range(n):
                    theta = start_angle + j * angle_step
                    poly.append(QPointF(center.x() + rr * math.cos(theta), center.y() + rr * math.sin(theta)))
                painter.setBrush(QBrush(c_surface if (i % 2 == 0) else c_surface2))
                painter.drawPolygon(poly)

            # ring labels (right side)
            painter.save()
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.setPen(c_text_muted)
            font_small = QFont(str(t.get("font_family", QFont().family())), max(8, int(t.get("font_px", 12)) - 2))
            painter.setFont(font_small)
            for scale in (0.2, 0.4, 0.6, 0.8, 1.0):
                rr = radius * scale
                label = f"{scale:.1f}"
                painter.drawText(
                    QRect(int(center.x() + rr + 6), int(center.y() - 8), 40, 16),
                    Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                    label
                )
            painter.restore()

            # --- Axis lines ---
            axis_pen = QPen(c_border, 1, Qt.PenStyle.DashLine)
            axis_pen.setCosmetic(True)
            painter.setPen(axis_pen)
            painter.setBrush(Qt.BrushStyle.NoBrush)

            for i in range(n):
                theta = start_angle + i * angle_step
                end_pt = QPointF(center.x() + radius * math.cos(theta), center.y() + radius * math.sin(theta))
                painter.drawLine(center, end_pt)

            # Helper: polygon from values
            def poly_from(vals: list[float]) -> QPolygonF:
                p = QPolygonF()
                for i, val in enumerate(vals):
                    rr = radius * clamp01(val)
                    theta = start_angle + i * angle_step
                    p.append(QPointF(center.x() + rr * math.cos(theta), center.y() + rr * math.sin(theta)))
                return p

            # --- Compare polygon ---
            if self._anim_compare and len(self._anim_compare) == len(self._anim_main):
                poly_cmp = poly_from(self._anim_compare)
                cmp_pen = QPen(c_compare, 2, Qt.PenStyle.DotLine)
                cmp_pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
                painter.setPen(cmp_pen)
                painter.setBrush(Qt.BrushStyle.NoBrush)
                painter.drawPolygon(poly_cmp)

            # --- Main polygon ---
            poly_main = poly_from(self._anim_main)

            # Glow outline
            painter.save()
            glow = QColor(c_accent)
            glow.setAlpha(42)
            glow_pen = QPen(glow, 9)
            glow_pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
            glow_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
            painter.setPen(glow_pen)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawPolygon(poly_main)
            painter.restore()

            # Gradient fill
            grad = QRadialGradient(center, radius)
            c_center = QColor(c_accent); c_center.setAlpha(120)
            c_edge = QColor(c_accent); c_edge.setAlpha(18)
            grad.setColorAt(0.0, c_center)
            grad.setColorAt(1.0, c_edge)

            painter.setBrush(QBrush(grad))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawPolygon(poly_main)

            # Main stroke
            line_pen = QPen(c_accent, 3)
            line_pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
            line_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
            painter.setPen(line_pen)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawPolygon(poly_main)

            # Vertex dots + hover highlight
            pts: list[QPointF] = []
            painter.save()
            painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
            for i in range(len(poly_main)):
                p = poly_main[i]
                pts.append(QPointF(p.x(), p.y()))

                # hover’d vertex gets larger + ring
                if i == self._hover_idx:
                    ring = QColor(c_accent); ring.setAlpha(220)
                    painter.setPen(QPen(ring, 2))
                    painter.setBrush(QBrush(c_bg))
                    painter.drawEllipse(p, 7, 7)
                    painter.setPen(QPen(c_accent, 2))
                    painter.setBrush(QBrush(c_bg))
                    painter.drawEllipse(p, 5, 5)
                else:
                    painter.setPen(QPen(c_accent, 2))
                    painter.setBrush(QBrush(c_bg))
                    painter.drawEllipse(p, 4, 4)
            painter.restore()

            # cache for hover picking
            self._last_geom = {"points": pts}

            # --- Labels + value labels on axis ends ---
            painter.save()
            font_size = max(9, int(t.get("font_px", 12)) - 1)
            font = QFont(str(t.get("font_family", QFont().family())), font_size)
            font.setBold(True)
            painter.setFont(font)

            metrics = painter.fontMetrics()
            pad = 6

            for i, m in enumerate(self._metrics[:n]):
                theta = start_angle + i * angle_step
                lbl_r = radius * 1.18

                pt = QPointF(center.x() + lbl_r * math.cos(theta), center.y() + lbl_r * math.sin(theta))

                # label text: "Name • 78%" (clarity!)
                v = self._anim_main[i] if i < len(self._anim_main) else m.value
                try:
                    vtxt = m.fmt.format(v)
                except Exception:
                    vtxt = f"{v:.2f}"

                label = f"{m.label} • {vtxt}"

                tw = metrics.horizontalAdvance(label)
                th = metrics.height()
                rect = QRect(0, 0, tw + 2 * pad, th + 2 * pad)

                cx = math.cos(theta)
                sy = math.sin(theta)

                if cx > 0.25:
                    rect.moveLeft(int(pt.x()) + 2)
                elif cx < -0.25:
                    rect.moveRight(int(pt.x()) - 2)
                else:
                    rect.moveCenter(pt.toPoint())

                if sy > 0.35:
                    rect.moveTop(int(pt.y()) + 2)
                elif sy < -0.35:
                    rect.moveBottom(int(pt.y()) - 2)

                # background pill for readability
                bg = QColor(c_surface2)
                bg.setAlpha(235)
                border = QColor(c_border)
                border.setAlpha(200)

                painter.setPen(QPen(border, 1))
                painter.setBrush(QBrush(bg))
                painter.drawRoundedRect(rect, 10, 10)

                # hovered label accent border
                if i == self._hover_idx:
                    hb = QColor(c_accent); hb.setAlpha(220)
                    painter.setPen(QPen(hb, 2))
                    painter.setBrush(Qt.BrushStyle.NoBrush)
                    painter.drawRoundedRect(rect.adjusted(-1, -1, 1, 1), 11, 11)

                painter.setPen(c_text)
                painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, label)

            painter.restore()

        except Exception:
            # crash-safe paint: fail silently (no white-window close)
            return
        

class FlowLayout(QLayout):
    """
    Wrap eden chip/tag layout (PyQt6 uyumlu, stabil).
    """
    def __init__(self, parent=None, margin: int = 0, spacing: int = 8):
        super().__init__(parent)
        self._items: list[QWidgetItem] = []
        self.setContentsMargins(margin, margin, margin, margin)
        self.setSpacing(spacing)

    def __del__(self):
        # Qt bazen item'ları bırakabiliyor; temizleyelim
        while self.count():
            self.takeAt(0)

    # ---- Qt required ----
    def addItem(self, item):
        self._items.append(item)

    def addWidget(self, w):
        # FlowLayout.addWidget(...) çağrılarını garantiye al
        self.addItem(QWidgetItem(w))

    def count(self):
        return len(self._items)

    def itemAt(self, index):
        return self._items[index] if 0 <= index < len(self._items) else None

    def takeAt(self, index):
        return self._items.pop(index) if 0 <= index < len(self._items) else None

    def clear_layout(self):
        """Remove all items/widgets from the layout."""
        while self.count():
            it = self.takeAt(0)
            if it is None:
                continue
            w = it.widget()
            if w is not None:
                w.setParent(None)
                w.deleteLater()

    def expandingDirections(self):
        # PyQt6: Qt.Orientations yok
        return Qt.Orientation(0)

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        return self._do_layout(QRect(0, 0, width, 0), test_only=True)

    def setGeometry(self, rect):
        super().setGeometry(rect)
        self._do_layout(rect, test_only=False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        s = QSize()
        for it in self._items:
            s = s.expandedTo(it.minimumSize())
        m = self.contentsMargins()
        s += QSize(m.left() + m.right(), m.top() + m.bottom())
        return s

    # ---- internal ----
    def _do_layout(self, rect: QRect, test_only: bool) -> int:
        x = rect.x()
        y = rect.y()
        line_h = 0
        space = self.spacing()

        # rect.right() inclusive; taşmayı düzgün yakalamak için width tabanlı kıyas daha stabil
        max_x = rect.x() + rect.width()

        for it in self._items:
            hint = it.sizeHint()
            w = hint.width()
            h = hint.height()

            next_x = x + w + space
            if (next_x - space) > max_x and line_h > 0:
                x = rect.x()
                y += line_h + space
                next_x = x + w + space
                line_h = 0

            if not test_only:
                it.setGeometry(QRect(x, y, w, h))

            x = next_x
            line_h = max(line_h, h)

        return (y + line_h) - rect.y()

def _repolish(w: QWidget) -> None:
    st = w.style()
    st.unpolish(w)
    st.polish(w)
    w.update()


class TagChipButton(QToolButton):
    """
    Premium tıklanabilir chip (multi-select):
    - checkable True
    - theme_tokens(theme) STRICT
    - checked/hover/pressed/focus stilleri
    """

    def __init__(self, text: str, theme: Optional[ThemeConfig] = None, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._theme = theme if theme is not None else get_active_theme()
        self._toks: dict[str, Any] = theme_tokens(self._theme)  # STRICT

        self.setText(text)
        self.setCheckable(True)
        self.setAutoRaise(False)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)

        # Typography
        f = QFont(self.font())
        f.setBold(True)
        self.setFont(f)

        # For hover state feel (Qt sometimes needs this for toolbuttons)
        self.setMouseTracking(True)

        self._apply_style()
        self.toggled.connect(lambda _: self._apply_style())

    def set_theme(self, theme: ThemeConfig) -> None:
        self._theme = theme
        self._toks = theme_tokens(theme)  # STRICT
        self._apply_style()

    def _apply_style(self) -> None:
        t = self._toks

        # Palette choices
        if self.isChecked():
            bg = t["accent2"]
            fg = t["bg"]
            border = t["accent2"]
            hover_border = t["accent"]
            focus_ring = t["accent"]
        else:
            bg = t["surface2"]
            fg = t["text"]
            border = t["border"]
            hover_border = t["accent2"]
            focus_ring = t["accent2"]

        # Premium chip geometry
        # - Slightly taller + more horizontal padding
        # - Rounded radius makes "pill"
        self.setStyleSheet(f"""
            QToolButton {{
                padding: 7px 12px;
                border-radius: 16px;
                border: 1px solid {border};
                background-color: {bg};
                color: {fg};
                font-weight: 800;
                letter-spacing: 0.2px;
            }}
            QToolButton:hover {{
                border: 1px solid {hover_border};
            }}
            QToolButton:pressed {{
                padding-top: 8px; /* micro tactile feel */
                padding-bottom: 6px;
            }}
            QToolButton:focus {{
                outline: none;
                border: 2px solid {focus_ring};
            }}
        """)
        _repolish(self)



# ===================================================================
# 7.                          HASHTAG FILTER
# ===================================================================


class _Section(QFrame):
    """Collapsible section: title row + chips host."""
    toggled = pyqtSignal(bool)

    def __init__(self, title: str, theme: ThemeConfig, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setObjectName("FilterSection")
        self._theme = theme
        self._toks = theme_tokens(theme)  # STRICT

        self._btns: Dict[str, TagChipButton] = {}

        lay = QVBoxLayout(self)
        lay.setContentsMargins(12, 12, 12, 12)
        lay.setSpacing(10)

        # header row
        head = QHBoxLayout()
        head.setContentsMargins(0, 0, 0, 0)
        head.setSpacing(8)

        self.btn_toggle = QToolButton()
        self.btn_toggle.setObjectName("SectionToggle")
        self.btn_toggle.setCheckable(True)
        self.btn_toggle.setChecked(True)
        self.btn_toggle.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_toggle.setAutoRaise(True)
        self.btn_toggle.clicked.connect(self._on_toggle)

        self.lbl_title = QLabel(title)
        ft = QFont()
        ft.setBold(True)
        ft.setPointSize(10)
        self.lbl_title.setFont(ft)

        self.lbl_count = QLabel("0")
        self.lbl_count.setProperty("muted", "1")
        self.lbl_count.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)

        head.addWidget(self.btn_toggle)
        head.addWidget(self.lbl_title)
        head.addStretch(1)
        head.addWidget(self.lbl_count)
        lay.addLayout(head)

        # chips host
        self.chips_host = QWidget()
        self.flow = FlowLayout(self.chips_host, margin=0, spacing=8)
        self.chips_host.setLayout(self.flow)
        lay.addWidget(self.chips_host)

        self._apply_style()
        self._sync_toggle_icon()

    def set_theme(self, theme: ThemeConfig) -> None:
        self._theme = theme
        self._toks = theme_tokens(theme)  # STRICT
        for b in self._btns.values():
            b.set_theme(theme)
        self._apply_style()
        self._sync_toggle_icon()

    def buttons(self) -> Dict[str, TagChipButton]:
        return self._btns

    def set_options(self, tags: Iterable[str], on_change) -> None:
        # Clear old chips
        self.flow.clear_layout()
        self._btns.clear()

        # Build new chips
        for raw in tags:
            if raw is None:
                continue
            s = str(raw).strip()
            if not s:
                continue
            chip_text = s if s.startswith("#") else f"#{s}"
            b = TagChipButton(chip_text, theme=self._theme)
            b.toggled.connect(on_change)  # no lambda capture bug
            self._btns[chip_text] = b
            self.flow.addWidget(b)

        self.lbl_count.setText(str(len(self._btns)))
        self._recompute_selected_badge()

    def clear_selection(self) -> None:
        for b in self._btns.values():
            b.blockSignals(True)
            b.setChecked(False)
            b.blockSignals(False)
            b._apply_style()
        self._recompute_selected_badge()

    def selected(self) -> List[str]:
        return [k for k, b in self._btns.items() if b.isChecked()]

    def _recompute_selected_badge(self) -> None:
        # show: "12 (3 seçili)"
        total = len(self._btns)
        sel = sum(1 for b in self._btns.values() if b.isChecked())
        self.lbl_count.setText(f"{total}" if sel == 0 else f"{total} ({sel} seçili)")

    def _on_toggle(self) -> None:
        expanded = bool(self.btn_toggle.isChecked())
        self.chips_host.setVisible(expanded)
        self._sync_toggle_icon()
        self.toggled.emit(expanded)

    def _sync_toggle_icon(self) -> None:
        # simple unicode arrows; can be replaced with icons later
        self.btn_toggle.setText("▾" if self.btn_toggle.isChecked() else "▸")

    def _apply_style(self) -> None:
        t = self._toks
        self.setStyleSheet(f"""
            QFrame#FilterSection {{
                background-color: {t["surface"]};
                border: 1px solid {t["border"]};
                border-radius: 16px;
            }}
            QLabel {{
                color: {t["text"]};
            }}
            QLabel[muted="1"] {{
                color: {t["text_muted"]};
                font-weight: 600;
            }}
            QToolButton#SectionToggle {{
                color: {t["text_muted"]};
                padding: 2px 6px;
                border-radius: 10px;
            }}
            QToolButton#SectionToggle:hover {{
                color: {t["text"]};
                background-color: {t["surface2"]};
            }}
        """)
        _repolish(self)


class HashtagFilterPanel(QFrame):
    """
    4 ana kategori:
      - Countries (OR)
      - Research Areas (focus + tags içinde arar)
      - Cost of Living bucket
      - Tuition fee bucket

    Dışarıya: filtersChanged(dict) sinyali verir.
    payload:
      {"countries": [...], "research": [...], "cost": [...], "fee": [...]}
    """
    filtersChanged = pyqtSignal(dict)

    def __init__(self, theme: Optional[ThemeConfig] = None, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setObjectName("HashtagFilterPanel")
        self.setFrameShape(QFrame.Shape.NoFrame)

        self._theme = theme if theme is not None else get_active_theme()
        self._toks = theme_tokens(self._theme)  # STRICT

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(10)

        # Header
        head = QHBoxLayout()
        head.setContentsMargins(0, 0, 0, 0)
        head.setSpacing(10)

        self.lbl = QLabel("Filtreler")
        f = QFont()
        f.setBold(True)
        f.setPointSize(11)
        self.lbl.setFont(f)

        self.lbl_state = QLabel("")  # "3 filtre aktif" gibi
        self.lbl_state.setProperty("muted", "1")

        self.btn_clear = SecondaryButton("Temizle")
        self.btn_clear.setFixedWidth(92)
        self.btn_clear.clicked.connect(self.clear_all)

        head.addWidget(self.lbl)
        head.addWidget(self.lbl_state)
        head.addStretch(1)
        head.addWidget(self.btn_clear)
        root.addLayout(head)

        # Sections (collapsible)
        self.sec_countries = _Section("Ülkeler", self._theme, parent=self)
        self.sec_research = _Section("Araştırma Alanları", self._theme, parent=self)
        self.sec_cost = _Section("Şehir Pahalılığı", self._theme, parent=self)
        self.sec_fee = _Section("Okul Ücreti", self._theme, parent=self)

        root.addWidget(self.sec_countries)
        root.addWidget(self.sec_research)
        root.addWidget(self.sec_cost)
        root.addWidget(self.sec_fee)

        self._apply_panel_style()
        self._sync_header_state()

    def set_theme(self, theme: ThemeConfig) -> None:
        self._theme = theme
        self._toks = theme_tokens(theme)  # STRICT
        self._apply_panel_style()

        for sec in (self.sec_countries, self.sec_research, self.sec_cost, self.sec_fee):
            sec.set_theme(theme)

        self._sync_header_state()

    def _apply_panel_style(self) -> None:
        t = self._toks
        self.setStyleSheet(f"""
            QFrame#HashtagFilterPanel {{
                background: transparent;
            }}
            QLabel {{
                color: {t["text"]};
            }}
            QLabel[muted="1"] {{
                color: {t["text_muted"]};
                font-weight: 600;
            }}
        """)
        _repolish(self)

    # ---------- options ----------
    def set_options(
        self,
        *,
        countries: Iterable[str],
        research_tags: Iterable[str],
        cost_buckets: Iterable[str] = ("#Ucuz", "#Orta", "#Pahalı"),
        fee_buckets: Iterable[str] = ("#Ücretsiz/Ucuz", "#Orta", "#Pahalı"),
    ) -> None:
        # Rebuild chips
        self.sec_countries.set_options(countries, self._on_any_changed)
        self.sec_research.set_options(research_tags, self._on_any_changed)
        self.sec_cost.set_options(cost_buckets, self._on_any_changed)
        self.sec_fee.set_options(fee_buckets, self._on_any_changed)

        self._emit_filters()

    # ---------- actions ----------
    def clear_all(self) -> None:
        for sec in (self.sec_countries, self.sec_research, self.sec_cost, self.sec_fee):
            sec.clear_selection()
        self._emit_filters()

    # ---------- selection ----------
    def selected_filters(self) -> dict:
        return {
            "countries": self.sec_countries.selected(),
            "research": self.sec_research.selected(),
            "cost": self.sec_cost.selected(),
            "fee": self.sec_fee.selected(),
        }

    def _on_any_changed(self, _checked: bool) -> None:
        # Update per-section counts (selected badges)
        for sec in (self.sec_countries, self.sec_research, self.sec_cost, self.sec_fee):
            sec._recompute_selected_badge()
        self._emit_filters()

    def _emit_filters(self) -> None:
        payload = self.selected_filters()
        self.filtersChanged.emit(payload)
        self._sync_header_state(payload)

    def _sync_header_state(self, payload: Optional[dict] = None) -> None:
        if payload is None:
            payload = self.selected_filters()

        active = sum(len(payload[k]) for k in ("countries", "research", "cost", "fee"))
        self.lbl_state.setText("" if active == 0 else f"• {active} filtre aktif")

        # disable clear if nothing selected
        self.btn_clear.setEnabled(active > 0)
        _repolish(self.btn_clear)


COST_BUCKET_MAP: Mapping[str, str] = {
    "very_high": "Pahalı",
    "high": "Pahalı",
    "medium": "Orta",
    "low": "Ucuz",
    "very_low": "Ucuz",
}

FEE_BUCKETS: Tuple[str, str, str] = ("Ücretsiz/Ucuz", "Orta", "Pahalı")


def _to_text_blob(x: Any) -> str:
    """
    focus/tags gibi alanlar list/tuple/set/string olabilir.
    Her durumda arama için bir string üretir (defansif).
    """
    if x is None:
        return ""
    if isinstance(x, (list, tuple, set)):
        return " ".join(str(i) for i in x if i is not None)
    return str(x)


def _derive_country_from_city_series(city: pd.Series) -> pd.Series:
    """
    "Berlin, Germany" -> "Germany"
    Boş/NaN => "Unknown"
    """
    s = city.fillna("").astype(str)
    out = s.str.split(",").str[-1].str.strip()
    return out.where(out.astype(bool), "Unknown")


def _normalize_filter_list(items: Any) -> list[str]:
    """
    UI’den gelen ["#Pahalı", " Orta ", None] gibi listeleri normalize eder:
    - None / boşları atar
    - baştaki # kaldırır
    - strip uygular
    """
    if not items:
        return []
    out: list[str] = []
    for x in items:
        if x is None:
            continue
        s = str(x).strip()
        if not s:
            continue
        if s.startswith("#"):
            s = s[1:].strip()
        if s:
            out.append(s)
    return out


def apply_hashtag_filters(df: pd.DataFrame, filters: Optional[Dict[str, Any]]) -> pd.DataFrame:
    """
    Kategori içinde OR, kategoriler arası AND.

    filters payload örneği:
      {"countries": [...], "research": [...], "cost": [...], "fee": [...]}

    Beklenen kolonlar:
      - country OR city (ülke çıkarımı için)
      - focus, tags (research araması için)
      - cost_city (very_high/high/medium/low/very_low)
      - semester_fee_eur (numeric)
    """
    if df is None or df.empty:
        return df

    f = filters or {}
    countries = _normalize_filter_list(f.get("countries"))
    research = _normalize_filter_list(f.get("research"))
    cost = _normalize_filter_list(f.get("cost"))
    fee = _normalize_filter_list(f.get("fee"))

    mask = pd.Series(True, index=df.index)

    # 1) Countries (OR)
    if countries:
        if "country" in df.columns:
            country_ser = df["country"].fillna("").astype(str).str.strip()
        elif "city" in df.columns:
            country_ser = _derive_country_from_city_series(df["city"])
        else:
            # column yoksa filtreyi efektif olarak "no match" yapma; ülke filtresi uygulanamaz
            # Bu yüzden mask’i False’a çekmek yerine filtreden vazgeçiyoruz.
            country_ser = None

        if country_ser is not None:
            mask &= country_ser.isin(countries)

    # 2) Research: focus + tags (OR search across selected tags)
    if research:
        if "focus" in df.columns:
            focus_ser = df["focus"].apply(_to_text_blob).astype(str)
        else:
            focus_ser = pd.Series("", index=df.index)

        if "tags" in df.columns:
            tags_ser = df["tags"].apply(_to_text_blob).astype(str)
        else:
            tags_ser = pd.Series("", index=df.index)

        blob = (focus_ser + " " + tags_ser).str.lower()

        # OR pattern (escaped)
        # "AI", "Signal Processing" => r"(ai|signal\ processing)"
        patt = "|".join(re.escape(t.lower()) for t in research if t)
        if patt:
            rx = re.compile(patt)
            mask &= blob.str.contains(rx, na=False)

    # 3) Cost bucket
    if cost and "cost_city" in df.columns:
        raw = df["cost_city"].fillna("").astype(str).str.strip().str.lower()
        bucket = raw.map(COST_BUCKET_MAP).fillna("")
        mask &= bucket.isin(cost)

    # 4) Tuition fee bucket
    if fee and "semester_fee_eur" in df.columns:
        fee_num = pd.to_numeric(df["semester_fee_eur"], errors="coerce")

        fee_bucket = pd.Series("", index=df.index, dtype="object")
        fee_bucket = fee_bucket.mask(fee_num < 300, FEE_BUCKETS[0])
        fee_bucket = fee_bucket.mask((fee_num >= 300) & (fee_num <= 1000), FEE_BUCKETS[1])
        fee_bucket = fee_bucket.mask(fee_num > 1000, FEE_BUCKETS[2])

        mask &= fee_bucket.isin(fee)

    return df.loc[mask]



# ===================================================================
# 9.                       TABLE SETTINGS
# ===================================================================

class ToggleSwitch(QWidget):
    """
    Premium toggle switch (paint-based).
    - No QCheckBox
    - toggled(bool) signal
    - Smooth animation (optional)
    - Hover/focus/disabled aware
    """
    toggled = pyqtSignal(bool)

    def __init__(
        self,
        parent: Optional[QWidget] = None,
        *,
        theme: Optional[ThemeConfig] = None,
        checked: bool = True,
        animated: bool = True,
        w: int = 46,
        h: int = 26,
    ):
        super().__init__(parent)
        self.setObjectName("ToggleSwitch")

        self._theme = theme if theme is not None else get_active_theme()
        self._toks = theme_tokens(self._theme)  # STRICT

        self._checked = bool(checked)
        self._animated = bool(animated)

        self._w = int(max(38, w))
        self._h = int(max(20, h))
        self.setFixedSize(self._w, self._h)

        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setMouseTracking(True)

        self._hover = False
        self._pos = 1.0 if self._checked else 0.0

        self._anim = QVariantAnimation(self)
        self._anim.setDuration(160)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._anim.valueChanged.connect(self._on_anim_value)

    # ---- theme ----
    def set_theme(self, theme: ThemeConfig) -> None:
        self._theme = theme
        self._toks = theme_tokens(theme)  # STRICT
        self.update()

    # ---- state ----
    def isChecked(self) -> bool:
        return bool(self._checked)

    def setChecked(self, checked: bool, *, emit_signal: bool = False) -> None:
        checked = bool(checked)
        if checked == self._checked:
            return
        self._checked = checked
        self._animate_to(1.0 if checked else 0.0)
        if emit_signal:
            self.toggled.emit(self._checked)

    def toggle(self) -> None:
        self.setChecked(not self._checked, emit_signal=True)

    def setAnimated(self, enabled: bool) -> None:
        self._animated = bool(enabled)

    def sizeHint(self) -> QSize:
        return QSize(self._w, self._h)

    # ---- events ----
    def enterEvent(self, e) -> None:
        self._hover = True
        self.update()
        return super().enterEvent(e)

    def leaveEvent(self, e) -> None:
        self._hover = False
        self.update()
        return super().leaveEvent(e)

    def mousePressEvent(self, e: QMouseEvent) -> None:
        if e.button() == Qt.MouseButton.LeftButton and self.isEnabled():
            self.toggle()
            e.accept()
            return
        super().mousePressEvent(e)

    def keyPressEvent(self, e: QKeyEvent) -> None:
        if self.isEnabled() and e.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter, Qt.Key.Key_Space):
            self.toggle()
            e.accept()
            return
        super().keyPressEvent(e)

    # ---- animation ----
    def _on_anim_value(self, v: Any) -> None:
        try:
            self._pos = clamp01(float(v))
        except Exception:
            self._pos = 1.0 if self._checked else 0.0
        self.update()

    def _animate_to(self, target: float) -> None:
        target = 1.0 if target >= 0.5 else 0.0
        if not self._animated:
            self._pos = target
            self.update()
            return
        try:
            self._anim.stop()
            self._anim.setStartValue(float(self._pos))
            self._anim.setEndValue(float(target))
            self._anim.start()
        except Exception:
            self._pos = target
            self.update()

    # ---- paint ----
    def paintEvent(self, e) -> None:
        try:
            t = self._toks
            p = QPainter(self)
            p.setRenderHint(QPainter.RenderHint.Antialiasing, True)

            r = self.rect()
            pad = 2
            track = r.adjusted(pad, pad, -pad, -pad)
            radius = track.height() / 2.0

            accent = QColor(t["accent"])
            accent2 = QColor(t["accent2"])
            border = QColor(t["border"])
            bg = QColor(t["bg"])
            surface2 = QColor(t["surface2"])
            text = QColor(t["text"])

            # Disabled soften
            if not self.isEnabled():
                for c in (accent, accent2, border, bg, surface2, text):
                    c.setAlpha(140)

            # Track colors
            on_col = QColor(accent2)
            off_col = QColor(surface2)
            pen_col = QColor(on_col if self._pos >= 0.5 else border)

            # Hover lift: subtle brighten
            if self._hover and self.isEnabled():
                pen_col = QColor(accent) if self._pos < 0.5 else QColor(accent)
                if self._pos < 0.5:
                    off_col = QColor(surface2)
                    off_col.setAlpha(255)
                on_col = QColor(accent2)

            track_col = on_col if self._pos >= 0.5 else off_col

            # Track
            pen = QPen(pen_col, 1.0)
            pen.setCosmetic(True)
            p.setPen(pen)
            p.setBrush(QBrush(track_col))
            p.drawRoundedRect(track, radius, radius)

            # Focus ring (outer)
            if self.hasFocus() and self.isEnabled():
                ring = QColor(accent)
                ring.setAlpha(90)
                ring_pen = QPen(ring, 2.0)
                ring_pen.setCosmetic(True)
                p.setPen(ring_pen)
                p.setBrush(Qt.BrushStyle.NoBrush)
                p.drawRoundedRect(track.adjusted(-1, -1, 1, 1), radius + 1, radius + 1)

            # Thumb geometry
            thumb_d = max(10, track.height() - 4)
            left_x = track.left() + 2
            right_x = track.right() - 2 - thumb_d
            x = left_x + (right_x - left_x) * float(self._pos)

            thumb = QRect(int(x), int(track.top() + 2), int(thumb_d), int(thumb_d))

            # Thumb fill + subtle highlight
            thumb_col = QColor(bg)
            p.setPen(Qt.PenStyle.NoPen)
            p.setBrush(QBrush(thumb_col))
            p.drawEllipse(thumb)

            hl = QColor(text)
            hl.setAlpha(18 if self.isEnabled() else 12)
            p.setBrush(QBrush(hl))
            p.drawEllipse(thumb.adjusted(2, 2, -2, -2))

            p.end()
        except Exception:
            super().paintEvent(e)


class ColumnSelectionDialog(QDialog):
    """
    Table column visibility settings dialog.
    - Live updates to table
    - Search/filter
    - Bulk actions (show all / hide all)
    """
    def __init__(
        self,
        table: Optional[QTableView],
        parent: Optional[QWidget] = None,
        *,
        theme: Optional[ThemeConfig] = None,
        title: str = "Sütun Ayarları",
    ):
        super().__init__(parent)
        self.setModal(True)
        self.setWindowTitle(str(title))
        self.setObjectName("ColumnSelectionDialog")

        self._table = table
        self._theme = theme if theme is not None else get_active_theme()
        self._toks = theme_tokens(self._theme)  # STRICT

        outer = QVBoxLayout(self)
        outer.setContentsMargins(16, 16, 16, 16)
        outer.setSpacing(10)

        # Card
        self._card = QFrame(self)
        self._card.setObjectName("ColumnDialogCard")
        card = QVBoxLayout(self._card)
        card.setContentsMargins(14, 14, 14, 14)
        card.setSpacing(10)

        # Header row
        hdr = QHBoxLayout()
        hdr.setContentsMargins(0, 0, 0, 0)
        hdr.setSpacing(10)

        self._lbl_title = QLabel(str(title))
        ff = QFont()
        ff.setBold(True)
        ff.setPointSize(12)
        self._lbl_title.setFont(ff)

        self._btn_show_all = SecondaryButton("Tümünü Göster")
        self._btn_hide_all = SecondaryButton("Tümünü Gizle")
        self._btn_show_all.clicked.connect(lambda: self._bulk_set(True))
        self._btn_hide_all.clicked.connect(lambda: self._bulk_set(False))

        hdr.addWidget(self._lbl_title)
        hdr.addStretch(1)
        hdr.addWidget(self._btn_hide_all)
        hdr.addWidget(self._btn_show_all)
        card.addLayout(hdr)

        # Search
        self._search = QLineEdit()
        self._search.setObjectName("ColumnSearch")
        self._search.setPlaceholderText("Sütun ara…")
        self._search.textChanged.connect(self._apply_search_filter)
        card.addWidget(self._search)

        # Scroll list
        self._scroll = QScrollArea(self._card)
        self._scroll.setWidgetResizable(True)
        self._scroll.setFrameShape(QFrame.Shape.NoFrame)

        self._list_host = QWidget()
        self._list_lay = QVBoxLayout(self._list_host)
        self._list_lay.setContentsMargins(0, 0, 0, 0)
        self._list_lay.setSpacing(8)

        self._scroll.setWidget(self._list_host)
        card.addWidget(self._scroll, 1)

        # Footer
        foot = QHBoxLayout()
        foot.setContentsMargins(0, 0, 0, 0)
        foot.addStretch(1)

        self._btn_close = SecondaryButton("Kapat")
        self._btn_close.clicked.connect(self.close)
        foot.addWidget(self._btn_close)
        card.addLayout(foot)

        outer.addWidget(self._card)

        # Shadow + style
        self._apply_style()
        apply_shadow(self._card, color="#000000", blur=26, alpha=120, offset=(0, 9))

        self._rows: Dict[int, ToggleSwitch] = {}
        self._row_frames: Dict[int, QFrame] = {}

        self.rebuild()
        self.resize(560, 600)

    def set_theme(self, theme: ThemeConfig) -> None:
        self._theme = theme
        self._toks = theme_tokens(theme)  # STRICT
        self._apply_style()

        for sw in self._rows.values():
            sw.set_theme(theme)

        _repolish(self)

    def _apply_style(self) -> None:
        t = self._toks
        self.setStyleSheet(f"""
            QDialog#ColumnSelectionDialog {{
                background: transparent;
            }}
            QFrame#ColumnDialogCard {{
                background-color: {t["surface"]};
                border: 1px solid {t["border"]};
                border-radius: 18px;
            }}
            QLabel {{
                color: {t["text"]};
            }}
            QLineEdit#ColumnSearch {{
                padding: 8px 10px;
                border-radius: 12px;
                background-color: {t["surface2"]};
                border: 1px solid {t["border"]};
                color: {t["text"]};
            }}
            QLineEdit#ColumnSearch:focus {{
                border: 1px solid {t["accent2"]};
            }}
        """)
        _repolish(self)

    def rebuild(self) -> None:
        # clear list
        while self._list_lay.count():
            it = self._list_lay.takeAt(0)
            if it is None:
                break
            w = it.widget()
            if w is not None:
                w.setParent(None)

        self._rows.clear()
        self._row_frames.clear()

        table = self._table
        if table is None or table.model() is None:
            self._list_lay.addWidget(QLabel("Tablo bulunamadı."))
            self._list_lay.addStretch(1)
            self._btn_show_all.setEnabled(False)
            self._btn_hide_all.setEnabled(False)
            return

        model = table.model()
        try:
            col_count = int(model.columnCount())
        except Exception:
            col_count = 0

        if col_count <= 0:
            self._list_lay.addWidget(QLabel("Gösterilecek sütun yok."))
            self._list_lay.addStretch(1)
            self._btn_show_all.setEnabled(False)
            self._btn_hide_all.setEnabled(False)
            return

        self._btn_show_all.setEnabled(True)
        self._btn_hide_all.setEnabled(True)

        t = self._toks

        for col in range(col_count):
            # column title
            try:
                name = model.headerData(col, Qt.Orientation.Horizontal, Qt.ItemDataRole.DisplayRole)
            except Exception:
                name = None
            title = str(name) if name is not None else f"Column {col}"

            row = QFrame()
            row.setObjectName("ColumnRow")
            rl = QHBoxLayout(row)
            rl.setContentsMargins(12, 10, 12, 10)
            rl.setSpacing(10)

            lbl = QLabel(title)
            lbl.setObjectName("ColumnName")
            lbl.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

            sw = ToggleSwitch(theme=self._theme, checked=(not table.isColumnHidden(col)), animated=True)

            def _on_toggle(checked: bool, c: int = col) -> None:
                try:
                    table.setColumnHidden(c, not bool(checked))
                except Exception:
                    pass

            sw.toggled.connect(_on_toggle)

            rl.addWidget(lbl)
            rl.addStretch(1)
            rl.addWidget(sw)

            # row style (premium card row)
            row.setStyleSheet(f"""
                QFrame#ColumnRow {{
                    background-color: {t["surface2"]};
                    border: 1px solid {t["border"]};
                    border-radius: 14px;
                }}
                QFrame#ColumnRow:hover {{
                    border: 1px solid {t["accent2"]};
                }}
            """)

            self._rows[col] = sw
            self._row_frames[col] = row
            self._list_lay.addWidget(row)

        self._list_lay.addItem(QSpacerItem(1, 1, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        self._apply_search_filter(self._search.text())

    def _apply_search_filter(self, text: str) -> None:
        q = (text or "").strip().lower()
        if not q:
            for fr in self._row_frames.values():
                fr.setVisible(True)
            return

        # filter by label text
        for col, fr in self._row_frames.items():
            lbl = fr.findChild(QLabel, "ColumnName")
            hay = (lbl.text() if lbl else "").lower()
            fr.setVisible(q in hay)

    def _bulk_set(self, visible: bool) -> None:
        table = self._table
        if table is None:
            return
        for col, sw in self._rows.items():
            sw.setChecked(bool(visible), emit_signal=False)
            try:
                table.setColumnHidden(col, not bool(visible))
            except Exception:
                pass

    def sync_from_table(self) -> None:
        table = self._table
        if table is None:
            return
        for col, sw in self._rows.items():
            try:
                is_visible = not table.isColumnHidden(col)
                sw.setChecked(is_visible, emit_signal=False)
            except Exception:
                pass


class TableSettingsButton(SecondaryButton):
    """
    Opens ColumnSelectionDialog for a given QTableView.
    Keeps a cached dialog instance (more responsive + consistent theme).
    """
    def __init__(
        self,
        table: Optional[QTableView],
        parent: Optional[QWidget] = None,
        *,
        theme: Optional[ThemeConfig] = None,
        text: str = "Ayarlar",
        dialog_title: str = "Sütun Ayarları",
    ):
        super().__init__(text=text, parent=parent)
        self._table = table
        self._theme = theme if theme is not None else get_active_theme()
        self._dialog_title = str(dialog_title)
        self._dlg: Optional[ColumnSelectionDialog] = None

        self.clicked.connect(self._open_dialog)

    def set_theme(self, theme: ThemeConfig) -> None:
        self._theme = theme
        if self._dlg is not None:
            self._dlg.set_theme(theme)

    def _open_dialog(self) -> None:
        try:
            if self._dlg is None:
                self._dlg = ColumnSelectionDialog(
                    self._table,
                    parent=self.window(),
                    theme=self._theme,
                    title=self._dialog_title,
                )
            else:
                # keep in sync if columns changed while dialog existed
                self._dlg._table = self._table
                self._dlg.set_theme(self._theme)
                self._dlg.rebuild()
                self._dlg.sync_from_table()

            self._dlg.exec()
        except Exception:
            pass




# ===================================================================
# MODERN DASHBOARD CONTAINERS (Sidebar & Header)
# ===================================================================

class ThemeAwareMixin:
    """
    Reusable theme plumbing:
    - keeps ThemeConfig
    - caches strict theme_tokens()
    - provides set_theme() and _apply_style() hook
    """
    def _init_theme(self, theme: Optional[ThemeConfig]) -> None:
        self._theme: ThemeConfig = theme if theme is not None else get_active_theme()
        self._toks = theme_tokens(self._theme)  # STRICT

    def set_theme(self, theme: ThemeConfig) -> None:
        self._theme = theme
        self._toks = theme_tokens(theme)  # STRICT
        if hasattr(self, "_apply_style"):
            self._apply_style()
        _repolish(self)  # type: ignore[arg-type]


class Sidebar(QFrame, ThemeAwareMixin):
    """
    Premium Sidebar container:
    - fixed width
    - subtle right divider
    - safe default layout
    """
    def __init__(
        self,
        parent: Optional[QWidget] = None,
        *,
        theme: Optional[ThemeConfig] = None,
        width: int = 280,
        padding: int = 14,
    ):
        super().__init__(parent)
        self._init_theme(theme)

        self.setObjectName("Sidebar")
        self.setFixedWidth(int(max(220, width)))

        self.layout_ = QVBoxLayout(self)
        self.layout_.setContentsMargins(padding, padding, padding, padding)
        self.layout_.setSpacing(10)

        self._apply_style()

    def _apply_style(self) -> None:
        t = self._toks
        self.setStyleSheet(f"""
            QFrame#Sidebar {{
                background-color: {t["surface"]};
                border-right: 1px solid {t["border"]};
            }}
        """)

    # Convenience forwarding
    def addWidget(self, widget: QWidget) -> None:
        self.layout_.addWidget(widget)

    def addLayout(self, layout: QLayout) -> None:
        self.layout_.addLayout(layout)

    def addStretch(self, stretch: int = 0) -> None:
        self.layout_.addStretch(stretch)


class Header(QFrame, ThemeAwareMixin):
    """
    Premium Header container:
    - fixed height
    - bottom divider
    """
    def __init__(
        self,
        parent: Optional[QWidget] = None,
        *,
        theme: Optional[ThemeConfig] = None,
        height: int = 80,
        padding_x: int = 24,
    ):
        super().__init__(parent)
        self._init_theme(theme)

        self.setObjectName("Header")
        self.setFixedHeight(int(max(56, height)))

        self.layout_ = QHBoxLayout(self)
        self.layout_.setContentsMargins(padding_x, 10, padding_x, 10)
        self.layout_.setSpacing(14)

        self._apply_style()

    def _apply_style(self) -> None:
        t = self._toks
        self.setStyleSheet(f"""
            QFrame#Header {{
                background-color: {t["surface"]};
                border-bottom: 1px solid {t["border"]};
            }}
        """)

    def addWidget(self, widget: QWidget) -> None:
        self.layout_.addWidget(widget)

    def addStretch(self, stretch: int = 0) -> None:
        self.layout_.addStretch(stretch)



# ===================================================================
# MODERN DASHBOARD WIDGETS (Cards & Inputs)
# ===================================================================

class ModernCard(QFrame, ThemeAwareMixin):
    """
    Premium card container with optional title header.
    Usage:
        card = ModernCard("Başlık")
        card.body_layout().addWidget(...)
    """
    def __init__(
        self,
        title: str = "",
        parent: Optional[QWidget] = None,
        *,
        theme: Optional[ThemeConfig] = None,
        padding: int = 14,
    ):
        super().__init__(parent)
        self._init_theme(theme)
        self.setObjectName("ModernCard")

        root = QVBoxLayout(self)
        root.setContentsMargins(padding, padding, padding, padding)
        root.setSpacing(10)

        self._header: Optional[QFrame] = None
        self._title_lbl: Optional[QLabel] = None

        if title:
            self._header = QFrame(self)
            self._header.setObjectName("CardHeader")
            hl = QHBoxLayout(self._header)
            hl.setContentsMargins(0, 0, 0, 0)
            hl.setSpacing(8)

            self._title_lbl = QLabel(title)
            self._title_lbl.setObjectName("CardTitle")
            f = QFont()
            f.setBold(True)
            f.setPointSize(11)
            self._title_lbl.setFont(f)

            hl.addWidget(self._title_lbl)
            hl.addStretch(1)
            root.addWidget(self._header)

        # Body container (real content goes here)
        self._body = QWidget(self)
        self._body.setObjectName("CardBody")
        self._body_lay = QVBoxLayout(self._body)
        self._body_lay.setContentsMargins(0, 0, 0, 0)
        self._body_lay.setSpacing(10)

        root.addWidget(self._body, 1)
        self._apply_style()

    def body_layout(self) -> QVBoxLayout:
        return self._body_lay

    def _apply_style(self) -> None:
        t = self._toks
        # Premium: slightly thicker radius, hover border accent
        self.setStyleSheet(f"""
            QFrame#ModernCard {{
                background-color: {t["surface"]};
                border: 1px solid {t["border"]};
                border-radius: 18px;
            }}
            QFrame#ModernCard:hover {{
                border: 1px solid {t["accent2"]};
            }}
            QLabel#CardTitle {{
                color: {t["text"]};
            }}
        """)


class KPICard(QFrame, ThemeAwareMixin):
    """
    KPI card: (icon) title + value
    """
    def __init__(
        self,
        title: str = "",
        value: Any = "",
        icon: str = "",
        parent: Optional[QWidget] = None,
        *,
        theme: Optional[ThemeConfig] = None
    ):
        super().__init__(parent)
        self._init_theme(theme)
        self.setObjectName("KPICard")

        lay = QVBoxLayout(self)
        lay.setContentsMargins(16, 14, 16, 14)
        lay.setSpacing(6)

        # Top row: icon + title
        top = QHBoxLayout()
        top.setContentsMargins(0, 0, 0, 0)
        top.setSpacing(8)

        self._icon = QLabel(icon)
        self._icon.setObjectName("KPIIcon")
        self._icon.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self._title = QLabel(title)
        self._title.setObjectName("KPITitle")
        self._title.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        top.addWidget(self._icon)
        top.addWidget(self._title)
        top.addStretch(1)

        self._value = QLabel(str(value))
        self._value.setObjectName("KPIValue")

        lay.addLayout(top)
        lay.addWidget(self._value)
        lay.addStretch(1)

        self._apply_style()

    def setValue(self, value: Any) -> None:
        self._value.setText(str(value))

    def _apply_style(self) -> None:
        t = self._toks
        self.setStyleSheet(f"""
            QFrame#KPICard {{
                background-color: {t["surface"]};
                border: 1px solid {t["border"]};
                border-radius: 18px;
            }}
            QFrame#KPICard:hover {{
                border: 1px solid {t["accent2"]};
            }}
            QLabel#KPIIcon {{
                color: {t["accent2"]};
                font-size: 16px;
                font-weight: 800;
            }}
            QLabel#KPITitle {{
                color: {t["text_muted"]};
                font-size: 13px;
                font-weight: 650;
            }}
            QLabel#KPIValue {{
                color: {t["text"]};
                font-size: 26px;
                font-weight: 800;
                margin-top: 2px;
            }}
        """)


class SearchBar(QLineEdit, ThemeAwareMixin):
    """
    Premium search input:
    - subtle hover
    - focus ring via accent2
    - good padding
    """
    def __init__(
        self,
        parent: Optional[QWidget] = None,
        *,
        theme: Optional[ThemeConfig] = None,
        placeholder: str = "Üniversite, program veya anahtar kelime ara…",
    ):
        super().__init__(parent)
        self._init_theme(theme)

        self.setObjectName("SearchBar")
        self.setPlaceholderText(str(placeholder))
        self.setClearButtonEnabled(True)
        self.setMinimumHeight(42)

        # Make it feel like a real control
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self._apply_style()

    def _apply_style(self) -> None:
        t = self._toks
        self.setStyleSheet(f"""
            QLineEdit#SearchBar {{
                padding: 10px 12px;
                border-radius: 14px;
                border: 1px solid {t["border"]};
                background-color: {t["surface2"]};
                color: {t["text"]};
                font-size: 14px;
                selection-background-color: {t["accent"]};
                selection-color: {t["bg"]};
            }}
            QLineEdit#SearchBar:hover {{
                border: 1px solid {t["text_muted"]};
            }}
            QLineEdit#SearchBar:focus {{
                border: 1px solid {t["accent2"]};
                background-color: {t["surface"]};
            }}
        """)



# ===================================================================
# 10.                          TESTING WIDGET.PY
# ===================================================================

if __name__ == "__main__":
    import sys
    import random
    from typing import Optional

    from PyQt6.QtCore import Qt
    from PyQt6.QtWidgets import (
        QApplication,
        QMainWindow,
        QWidget,
        QScrollArea,
        QVBoxLayout,
        QHBoxLayout,
        QGroupBox,
        QTableView,
        QHeaderView,
        QLabel,
    )
    from PyQt6.QtGui import QStandardItemModel, QStandardItem

    # Tema
    from unirank.ui.theme import ThemeConfig, apply_theme, get_active_theme, theme_tokens

    # Çift tıklayınca kapanma (flash & close) yerine hatayı terminalde/ekranda gör
    def _excepthook(exc_type, exc, tb):
        import traceback
        traceback.print_exception(exc_type, exc, tb)
        input("\n[widgets.py] Exception occurred. Press Enter to exit...")

    sys.excepthook = _excepthook

    print(">>> widgets.py showcase running...")

    random.seed(7)
    app = QApplication(sys.argv)

    # ---- Karanlık tema: test sırasında zorla uygula ----
    cfg = ThemeConfig(
        bg="#0B0F14",
        surface="#0E141B",
        surface2="#111A23",
        border="#253041",
        border_soft="#1B2432",
        text="#E6EAF2",
        text_muted="#B9C3D6",
        text_faint="#8FA0B8",
        accent="#7AA2F7",
        accent2="#2EE59D",
        danger="#FF4D6D",
        warning="#FFB86C",
        font_family="Inter",
        font_px=13,
        scale=1.0,
    )
    apply_theme(app, cfg)

    # Tokenlar temadan gelsin (STRICT)
    toks = theme_tokens(get_active_theme())

    class ShowcaseWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("SimCode Widgets Showcase")
            self.resize(1100, 900)

            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            self.setCentralWidget(scroll)

            root = QWidget()
            scroll.setWidget(root)

            main_layout = QVBoxLayout(root)
            main_layout.setSpacing(18)
            main_layout.setContentsMargins(18, 18, 18, 18)

            # -------------------------
            # 1) Buttons & badge
            # -------------------------
            gb_basic = QGroupBox("1) Temel Bileşenler")
            gb_basic.setStyleSheet(f"QGroupBox::title {{ color: {toks['accent']}; }}")
            layout_basic = QHBoxLayout(gb_basic)

            btn_p = PrimaryButton("Primary Action")
            btn_s = SecondaryButton("Secondary Action")
            btn_d = DangerButton("Danger Zone")

            badge = PillBadge("Status: ONAYLI", theme=cfg)

            layout_basic.addWidget(btn_p)
            layout_basic.addWidget(btn_s)
            layout_basic.addWidget(btn_d)
            layout_basic.addStretch(1)
            layout_basic.addWidget(badge)

            apply_shadow(gb_basic, color=toks["accent"], alpha=40, blur=20)
            main_layout.addWidget(gb_basic)

            # -------------------------
            # 2) Radar chart
            # -------------------------
            gb_radar = QGroupBox("2) Radar Chart (Animasyonlu)")
            gb_radar.setStyleSheet(f"QGroupBox::title {{ color: {toks['accent']}; }}")
            layout_radar = QHBoxLayout(gb_radar)

            radar = RadarChart(theme=cfg)
            layout_radar.addWidget(radar, 2)

            radar_controls = QVBoxLayout()
            btn_rnd = PrimaryButton("Rastgele Veri")
            btn_rnd.clicked.connect(
                lambda: radar.set_data(
                    ["Maliyet", "Uyum", "Skor", "Konfor", "Ar-Ge"],
                    [random.random() for _ in range(5)],
                )
            )

            btn_scn1 = SecondaryButton("Senaryo: Mühendislik")
            btn_scn1.clicked.connect(
                lambda: radar.set_data(
                    ["Maliyet", "Uyum", "Skor", "Konfor", "Ar-Ge"],
                    [0.30, 0.95, 0.85, 0.40, 0.90],
                )
            )

            btn_scn2 = SecondaryButton("Senaryo: Bütçe Odaklı")
            btn_scn2.clicked.connect(
                lambda: radar.set_data(
                    ["Maliyet", "Uyum", "Skor", "Konfor", "Ar-Ge"],
                    [0.90, 0.55, 0.70, 0.45, 0.40],
                )
            )

            radar_controls.addWidget(btn_rnd)
            radar_controls.addWidget(btn_scn1)
            radar_controls.addWidget(btn_scn2)
            radar_controls.addStretch(1)
            layout_radar.addLayout(radar_controls, 1)

            apply_shadow(gb_radar, color="#000000", alpha=80)
            main_layout.addWidget(gb_radar)

            # -------------------------
            # 3) Table delegates + Table Settings
            # -------------------------
            gb_table = QGroupBox("3) Table (Delegates) + Sütun Ayarları")
            gb_table.setStyleSheet(f"QGroupBox::title {{ color: {toks['accent']}; }}")
            layout_table = QVBoxLayout(gb_table)
            layout_table.setSpacing(10)

            topbar = QHBoxLayout()
            topbar.setContentsMargins(0, 0, 0, 0)

            hint = QLabel("Ayarlar ile sütunları anlık gizle/aç (Scroll’lu dialog).")
            hint.setStyleSheet(f"color: {toks['text_muted']};")
            topbar.addWidget(hint)
            topbar.addStretch(1)

            # Model & table
            model = QStandardItemModel(12, 4)
            headers = ["Üniversite", "Masraf(şehir)", "Hedefe uyum", "Skor"]
            model.setHorizontalHeaderLabels(headers)

            dummy_data: list[dict[str, float]] = []
            for r in range(model.rowCount()):
                uni_name = f"Univ-{r+1} Tech"
                cost = random.random()
                fit = random.random()
                score = random.random()
                dummy_data.append({"cost": cost, "fit": fit, "score": score})

                model.setItem(r, 0, QStandardItem(uni_name))
                model.setItem(r, 1, QStandardItem(f"{cost:.2f}"))
                model.setItem(r, 2, QStandardItem(f"{fit:.2f}"))
                model.setItem(r, 3, QStandardItem(f"{score:.2f}"))

            table = QTableView()
            table.setModel(model)
            table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
            table.setSelectionMode(QTableView.SelectionMode.SingleSelection)
            table.setAlternatingRowColors(True)
            table.setMinimumHeight(360)
            table.setSortingEnabled(False)

            # Delegates için demo goodness
            def demo_goodness(row: int, key: str) -> Optional[float]:
                if not (0 <= row < len(dummy_data)):
                    return None
                v = dummy_data[row]
                if key == "cost_good":
                    return v["cost"]
                if key == "fit_good":
                    return v["fit"]
                if key == "score_good":
                    return v["score"]
                return None

            col_map = {"Masraf(şehir)": 1, "Hedefe uyum": 2, "Skor": 3}
            apply_ranking_delegates(table, col_map, demo_goodness, theme=cfg)

            # demo: bir kolonu başlangıçta gizle
            table.setColumnHidden(1, True)

            btn_table_settings = TableSettingsButton(
                table,
                parent=gb_table,
                theme=cfg,
                text="Ayarlar",
                dialog_title="Sütun Ayarları",
            )
            topbar.addWidget(btn_table_settings)

            layout_table.addLayout(topbar)
            layout_table.addWidget(table)
            apply_shadow(gb_table, color="#000000", alpha=80)
            main_layout.addWidget(gb_table)

            # İlk radar datası
            radar.set_data(["Maliyet", "Uyum", "Skor", "Konfor", "Ar-Ge"], [0.7, 0.7, 0.7, 0.7, 0.7])

            # -------------------------
            # 4) ToggleSwitch (standalone demo)
            # -------------------------
            gb_switch = QGroupBox("4) ToggleSwitch (paintEvent tabanlı)")
            gb_switch.setStyleSheet(f"QGroupBox::title {{ color: {toks['accent']}; }}")
            lay_sw = QHBoxLayout(gb_switch)

            sw = ToggleSwitch(theme=cfg, checked=True, animated=True)
            sw_lbl = QLabel("Durum: ON")
            sw_lbl.setStyleSheet(f"color: {toks['text_muted']};")

            def _on_sw(v: bool):
                sw_lbl.setText("Durum: ON" if v else "Durum: OFF")

            sw.toggled.connect(_on_sw)

            lay_sw.addWidget(QLabel("Demo anahtar:"))
            lay_sw.addWidget(sw)
            lay_sw.addSpacing(10)
            lay_sw.addWidget(sw_lbl)
            lay_sw.addStretch(1)

            apply_shadow(gb_switch, color="#000000", alpha=70, blur=20)
            main_layout.addWidget(gb_switch)

            main_layout.addStretch(1)

    win = ShowcaseWindow()
    win.show()
    sys.exit(app.exec())
