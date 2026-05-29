# assets/json_loader

"""
Bu modül; proje içindeki üniversite verilerini içeren JSON dosyalarını güvenli şekilde
okuyup tek bir pandas DataFrame’e dönüştürür ve yükleme sürecine ait bir rapor üretir.

Öne çıkanlar:
- Farklı JSON şemalarını tolere eder (liste/dict/kapsayıcı anahtarlar).
- Alanları normalize eder (üniversite adı, şehir, şehir maliyeti, dönem ücreti vb.).
- Hataları ve uyarıları (dosya/kayıt bazında) LoadReport / LoadIssue ile raporlar.
- strict=True modunda kritik sorunlarda ValueError fırlatır, strict=False modunda
  sorunlu kayıtları atlayıp devam eder.

Dışarıya açık fonksiyonlar:
- load_database_folder(folder, strict=False)
- load_database(path, strict=False, include_siblings_if_file=True)
"""

# ===================================================================
# 0.                         IMPORTS
# ===================================================================

from __future__ import annotations


import re
import json
from pathlib import Path

import pandas as pd
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple, Literal, Iterable




# ===================================================================
# 1.                         DATACLASSES
# ===================================================================

# Issue seviyesini serbest string yerine kısıtlayalım
IssueLevel = Literal["warn", "error"]


@dataclass(frozen=True, slots=True)
class LoadIssue:
    """
    JSON yükleme sırasında oluşan tekil problem kaydı.
    """
    level: IssueLevel            # "warn" | "error"
    file: str                    # sorun hangi dosyada
    message: str                 # açıklama

    # Sorun bir kayda bağlıysa (liste içindeki index / id)
    record_index: Optional[int] = None
    record_id: Optional[str] = None

    def __post_init__(self) -> None:
        # Küçük doğrulamalar: hatalı veri raporu da bozmasın
        if not self.file:
            raise ValueError("LoadIssue.file boş olamaz.")
        if not self.message:
            raise ValueError("LoadIssue.message boş olamaz.")

    @property
    def is_error(self) -> bool:
        return self.level == "error"

    @property
    def is_warn(self) -> bool:
        return self.level == "warn"

    @staticmethod
    def warn(file: str, message: str, record_index: Optional[int] = None, record_id: Optional[str] = None) -> "LoadIssue":
        # Uyarı üretmek için kısa yol
        return LoadIssue("warn", file, message, record_index, record_id)

    @staticmethod
    def error(file: str, message: str, record_index: Optional[int] = None, record_id: Optional[str] = None) -> "LoadIssue":
        # Hata üretmek için kısa yol
        return LoadIssue("error", file, message, record_index, record_id)


@dataclass(slots=True)
class LoadReport:
    """
    Bir klasör (veya kaynak) için yükleme özeti + issue listesi.
    """
    folder: str
    files_seen: int
    files_loaded: int
    records_seen: int
    records_loaded: int

    # issues listesi default olarak boş başlasın
    issues: List[LoadIssue] = field(default_factory=list)

    def has_errors(self) -> bool:
        # En az bir error var mı?
        return any(i.is_error for i in self.issues)

    def error_count(self) -> int:
        return sum(1 for i in self.issues if i.is_error)

    def warn_count(self) -> int:
        return sum(1 for i in self.issues if i.is_warn)

    def add(self, issue: LoadIssue) -> None:
        # Tekil issue ekleme
        self.issues.append(issue)

    def extend(self, issues: Iterable[LoadIssue]) -> None:
        # Toplu issue ekleme
        self.issues.extend(list(issues))



# ===================================================================
# 2.                           HELPERS
# ===================================================================

def _as_list(x: Any) -> List[Any]:
    """None -> [], list -> list, diğer her şey -> [x]."""
    if x is None:
        return []
    if isinstance(x, list):
        return x
    return [x]


def _first_nonempty(*vals: Any) -> str:
    """Verilen değerler içinde ilk dolu (strip sonrası) string'i döndürür."""
    for v in vals:
        if v is None:
            continue
        s = str(v).strip()
        if s:
            return s
    return ""


def _join_list(x: Any, sep: str = "; ") -> str:
    """
    Listeyse elemanları birleştirir, değilse string'e çevirir.
    Boş/None elemanları filtreler.
    """
    if x is None:
        return ""
    if isinstance(x, list):
        items: List[str] = []
        for i in x:
            if i is None:
                continue
            s = str(i).strip()
            if s:
                items.append(s)
        return sep.join(items)
    return str(x).strip()


def parse_fee_to_eur(x: Any) -> Optional[float]:
    """
    Kabul edilen örnekler:
      - 350 / 350.0 -> 350.0
      - "€350–€425" / "350-425" / "350 to 425" -> ortalama
      - "≈€180" -> 180.0
      - "free" / "0" -> 0.0 (0 sayısını yakalayabiliyorsak)
    """
    # None / NaN kontrolü
    if x is None:
        return None
    if isinstance(x, float) and pd.isna(x):
        return None
    if isinstance(x, (int, float)):
        return float(x)

    # Metni normalize et
    s = str(x).strip().lower()

    # Bazı unicode tireleri normalize edelim (en az sürpriz)
    s = s.replace("—", "-").replace("–", "-").replace("−", "-")
    # Avrupa formatı 1.234,56 gibi gelebilir; basit yaklaşım:
    # Önce boşlukları kaldırıp virgülü noktaya çekiyoruz
    s = s.replace(" ", "").replace(",", ".")

    # Sayıları yakala
    nums = re.findall(r"\d+(?:\.\d+)?", s)
    if not nums:
        return None

    vals = [float(n) for n in nums]

    # Aralık ifadesi varsa (350-425, 350to425 vb.) ortalama al
    has_range = ("-" in s) or ("to" in s)
    if has_range and len(vals) >= 2:
        return (vals[0] + vals[1]) / 2.0

    # Tek sayı varsa onu döndür
    return vals[0]


def _extract_semester_fee(entry: Dict[str, Any]) -> Optional[float]:
    """
    Semester fee (dönem katkı payı) için hem eski hem yeni şemayı destekler.

    Yeni şema (clean):
      - Cost_Semester_Fees: list[dict]  (amount/raw/currency/term_code...)

    Eski şema:
      - semester_fees: list[dict]
      - semester_fee_eur / semester_fee / semester_fee_raw

    Strateji:
      - structured amount değerlerini topla
      - yoksa raw string parse etmeyi dene
      - birden çok kayıt varsa ortalama al (daha dengeli)
    """
    fees = _as_list(entry.get("Cost_Semester_Fees")) or _as_list(entry.get("semester_fees"))
    amounts: List[float] = []

    for f in fees:
        if not isinstance(f, dict):
            continue

        a = f.get("amount")
        if isinstance(a, (int, float)) and not (isinstance(a, float) and pd.isna(a)):
            amounts.append(float(a))
            continue

        raw = f.get("raw")
        parsed = parse_fee_to_eur(raw)
        if parsed is not None:
            amounts.append(float(parsed))

    if amounts:
        return sum(amounts) / float(len(amounts))

    # fallback alanlar
    for k in ("semester_fee_eur", "semester_fee", "semester_fee_raw"):
        parsed = parse_fee_to_eur(entry.get(k))
        if parsed is not None:
            return float(parsed)

    # bazı datasetlerde ücret string olarak tek yerde olabilir
    parsed = parse_fee_to_eur(entry.get("Cost_Semester_Fees_Raw"))
    if parsed is not None:
        return float(parsed)

    return None


def _normalize_container(obj: Any) -> List[Dict[str, Any]]:
    """
    Kabul edilen top-level JSON formatları:
      - list[dict]
      - dict (tek kayıt)
      - dict içinde 'universities' veya 'items' listesi
    """
    if isinstance(obj, list):
        return [x for x in obj if isinstance(x, dict)]

    if isinstance(obj, dict):
        # Yaygın kapsayıcı anahtarlar
        for key in ("universities", "items"):
            v = obj.get(key)
            if isinstance(v, list):
                return [x for x in v if isinstance(x, dict)]
        # Tek obje
        return [obj]

    return []


def _safe_read_json(path: Path) -> Tuple[Optional[Any], Optional[str]]:
    """
    JSON okumayı güvenli yapar.
    Hata olursa (None, hata_mesaji) döndürür.
    """
    try:
        return json.loads(path.read_text(encoding="utf-8")), None
    except Exception as e:
        return None, str(e)


def _normalize_cost(entry: Dict[str, Any]) -> Tuple[str, str]:
    """
    Returns (cost_key, cost_raw)

    Yeni şema (clean):
      - Cost_City_Living: "very_high" | "high" | "medium_high" | ...
    Eski şema:
      - city_cost / city_cost_raw / cost_city

    cost_key: lower + underscore normalize edilmiş anahtar
    cost_raw: kullanıcıya gösterilebilecek ham değer
    """
    raw = _first_nonempty(
        entry.get("Cost_City_Living"),
        entry.get("city_cost"),
        entry.get("city_cost_raw"),
        entry.get("cost_city"),
        "medium",
    )

    raw_s = str(raw).strip()
    key = raw_s.lower().replace(" ", "_")
    return key, raw_s


def _record_display_name(entry: Dict[str, Any]) -> str:
    """UI’da gösterilecek isim için en uygun alanı seçer (yeni + eski şema)."""
    return _first_nonempty(
        entry.get("University_Display_Name"),
        entry.get("University_Short_Name"),
        entry.get("University_Name"),
        entry.get("short"),
        entry.get("display_name"),
        entry.get("name"),
        entry.get("id"),
        entry.get("Uni_ID"),
    )


def _extract_city(entry: Dict[str, Any]) -> str:
    """location.city varsa onu, yoksa entry.city kullanır."""
    loc = entry.get("location")
    if isinstance(loc, dict):
        return _first_nonempty(loc.get("city"), entry.get("city"))
    return _first_nonempty(entry.get("city"), "")


def _extract_text_fields(entry: Dict[str, Any]) -> Tuple[str, str, str, str, str]:
    """
    Returns: strength, focus, pros, cons, tags_str

    Yeni şema (clean) alanları:
      - Analysis_Strong_Areas, Analysis_Pros, Analysis_Cons, Analysis_Tags
      - Industry_Ecosystem (ek bağlam)
    Eski şema alanları:
      - aerospace_ecosystem, strength, strong_areas_summary, pros, cons, tags, tags_raw

    Not: strength ve focus alanlarının birbirini tekrar etmesini azaltmak için
    öncelik sırası anlamlı tutulur.
    """
    strength = _first_nonempty(
        entry.get("Analysis_Strong_Areas"),
        entry.get("strong_areas_summary"),
        entry.get("aerospace_ecosystem"),
        entry.get("strength"),
        entry.get("Industry_Ecosystem"),
        "",
    )

    tags_clean = _join_list(entry.get("Analysis_Tags"))
    tags_old = _join_list(entry.get("tags"))

    focus = _first_nonempty(
        entry.get("focus"),
        tags_clean,
        entry.get("tags_raw"),
        tags_old,
        entry.get("strong_areas_summary"),
        entry.get("Analysis_Strong_Areas"),
        "",
    )

    pros = _join_list(entry.get("Analysis_Pros")) or _join_list(entry.get("pros"))
    cons = _join_list(entry.get("Analysis_Cons")) or _join_list(entry.get("cons"))
    tags_str = tags_clean or tags_old
    return strength, focus, pros, cons, tags_str


def _json_compact(x: Any) -> str:
    """dict/list -> compact JSON string (UTF-8 safe), diğerleri -> str."""
    if x is None:
        return ""
    if isinstance(x, (dict, list)):
        try:
            return json.dumps(x, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
        except Exception:
            # Fallback: son çare
            return str(x)
    return str(x).strip()


def _coerce_int(x: Any) -> Optional[int]:
    if x is None:
        return None
    if isinstance(x, int):
        return x
    if isinstance(x, float) and pd.isna(x):
        return None
    try:
        s = str(x).strip()
        if not s:
            return None
        return int(float(s))
    except Exception:
        return None


def _coerce_bool(x: Any) -> Optional[bool]:
    if x is None:
        return None
    if isinstance(x, bool):
        return x
    s = str(x).strip().lower()
    if s in ("true", "1", "yes", "y"):
        return True
    if s in ("false", "0", "no", "n"):
        return False
    return None


def _extract_location(entry: Dict[str, Any]) -> Tuple[str, str, str]:
    """Returns (city, state, country). Yeni + eski şema uyumlu."""
    # Yeni şema (clean): City / State_Region / Country
    city = _first_nonempty(entry.get("City"), "")
    state = _first_nonempty(entry.get("State_Region"), entry.get("State"), "")
    country = _first_nonempty(entry.get("Country"), "")

    # Eski şema: location dict'i
    loc = entry.get("location")
    if isinstance(loc, dict):
        city = _first_nonempty(city, loc.get("city"), entry.get("city"), "")
        state = _first_nonempty(state, loc.get("state"), entry.get("state"), "")
        country = _first_nonempty(country, loc.get("country"), entry.get("country"), "")
        return city, state, country

    # Eski düz alanlar
    city = _first_nonempty(city, entry.get("city"), "")
    state = _first_nonempty(state, entry.get("state"), "")
    country = _first_nonempty(country, entry.get("country"), "")
    return city, state, country


def _extract_target_program(entry: Dict[str, Any]) -> Tuple[str, str, Optional[int], str]:
    """Returns (name, degree, ects, url). Yeni + eski şema uyumlu."""
    # Yeni şema (clean)
    name = _first_nonempty(entry.get("Program_Name"), "")
    degree = _first_nonempty(entry.get("Program_Degree"), "")
    ects = _coerce_int(entry.get("Program_ECTS"))
    url = _first_nonempty(entry.get("Program_URL"), "")

    if name or degree or ects is not None or url:
        return name, degree, ects, url

    # Eski şema (target_program objesi)
    tp = entry.get("target_program")
    if isinstance(tp, dict):
        return (
            _first_nonempty(tp.get("name"), ""),
            _first_nonempty(tp.get("degree"), ""),
            _coerce_int(tp.get("ects")),
            _first_nonempty(tp.get("url"), ""),
        )

    return "", "", None, ""


def _extract_deadlines(entry: Dict[str, Any]) -> Tuple[str, str, str, str, str]:
    """Returns (winter_opens, winter_closes, summer_opens, summer_closes, note). Yeni + eski şema uyumlu."""
    # Yeni şema (clean) - flatten
    winter_opens = _first_nonempty(entry.get("Deadline_Winter_Open"), "")
    winter_closes = _first_nonempty(entry.get("Deadline_Winter_Close"), "")
    summer_opens = _first_nonempty(entry.get("Deadline_Summer_Open"), "")
    summer_closes = _first_nonempty(entry.get("Deadline_Summer_Close"), "")

    note = _first_nonempty(
        entry.get("Deadline_General_Note"),
        entry.get("Deadline_Winter_Note"),
        entry.get("Deadline_Summer_Note"),
        "",
    )

    if winter_opens or winter_closes or summer_opens or summer_closes or note:
        return winter_opens, winter_closes, summer_opens, summer_closes, note

    # Eski şema (deadlines dict)
    dl = entry.get("deadlines")
    if not isinstance(dl, dict):
        return "", "", "", "", ""

    w = dl.get("winter") if isinstance(dl.get("winter"), dict) else {}
    s = dl.get("summer") if isinstance(dl.get("summer"), dict) else {}

    winter_opens = _first_nonempty(w.get("opens"), "")
    winter_closes = _first_nonempty(w.get("closes"), "")
    summer_opens = _first_nonempty(s.get("opens"), "")
    summer_closes = _first_nonempty(s.get("closes"), "")
    note = _first_nonempty(dl.get("note"), "")
    return winter_opens, winter_closes, summer_opens, summer_closes, note


def _tuition_to_eur_per_year(amount: Any, period: Any) -> Optional[float]:
    """Amount + period -> annualized EUR (best-effort)."""
    if amount is None:
        return None
    if isinstance(amount, float) and pd.isna(amount):
        return None

    # amount
    if isinstance(amount, (int, float)):
        a = float(amount)
    else:
        a_parsed = parse_fee_to_eur(amount)
        if a_parsed is None:
            return None
        a = float(a_parsed)

    p = str(period).strip().lower() if period is not None else ""
    if p in ("year", "annual", "per_year", "yr"):
        return a
    if p in ("semester", "term"):
        return a * 2.0
    if p in ("month", "monthly"):
        return a * 12.0
    if p in ("quarter", "quarterly"):
        return a * 4.0
    # bilinmiyor: amount'ı olduğu gibi kullan
    return a


def _extract_tuition(entry: Dict[str, Any], prefer_scope: str = "non_eu") -> Tuple[Optional[float], str, str, str, str]:
    """Returns (tuition_eur_per_year, tuition_raw, tuition_program, tuition_period, tuition_scope)."""
    # Yeni şema (clean)
    items = [x for x in _as_list(entry.get("Cost_Tuition")) if isinstance(x, dict)]
    # Eski şema
    if not items:
        items = [x for x in _as_list(entry.get("tuition")) if isinstance(x, dict)]

    if not items:
        # eski şema fallback: tek değer gelebilir
        fallback = entry.get("tuition_fee") or entry.get("tuition") or entry.get("Cost_Tuition_Raw")
        parsed = _tuition_to_eur_per_year(fallback, "year")
        return parsed, _first_nonempty(fallback, ""), "", "year", ""

    scoped = [t for t in items if _first_nonempty(t.get("scope"), "").strip().lower() == prefer_scope]
    use = scoped if scoped else items

    annuals: List[float] = []
    raws: List[str] = []
    programs: List[str] = []
    periods: List[str] = []
    scopes: List[str] = []

    for t in use:
        annual = _tuition_to_eur_per_year(t.get("amount"), t.get("period"))
        if annual is not None:
            annuals.append(float(annual))
        raws.append(_first_nonempty(t.get("raw"), ""))
        programs.append(_first_nonempty(t.get("program"), ""))
        periods.append(_first_nonempty(t.get("period"), ""))
        scopes.append(_first_nonempty(t.get("scope"), ""))

    tuition_eur_per_year = min(annuals) if annuals else None  # kıyas için konservatif: min
    tuition_raw = _join_list([r for r in raws if r], sep=" | ")
    tuition_program = _join_list([p for p in programs if p], sep=" | ")
    tuition_period = _join_list([p for p in periods if p], sep=" | ")
    tuition_scope = _join_list([s for s in scopes if s], sep=" | ")
    return tuition_eur_per_year, tuition_raw, tuition_program, tuition_period, tuition_scope


def _extract_scholarships(entry: Dict[str, Any]) -> Tuple[str, str]:
    """Returns (scholarship_names, scholarships_json). Yeni + eski şema uyumlu."""
    sch = [x for x in _as_list(entry.get("Scholarships_Info")) if isinstance(x, dict)]
    if not sch:
        sch = [x for x in _as_list(entry.get("scholarships")) if isinstance(x, dict)]

    names = [_first_nonempty(s.get("name"), "") for s in sch]
    names = [n for n in names if n]
    return _join_list(names), _json_compact(sch)


def _extract_key_partners(entry: Dict[str, Any]) -> str:
    # Yeni şema (clean)
    partners = entry.get("Industry_Partners")
    if partners is not None:
        return _join_list(partners)
    # Eski şema
    return _join_list(entry.get("key_partners"))


def _validate_record_minimal(entry: Dict[str, Any]) -> Optional[str]:
    """
    Minimal validasyon:
      - display name (short/display_name/name/id) boş olmamalı
    """
    name = _record_display_name(entry)
    if not name:
        return "Missing university display name (short/display_name/name/id all empty)."
    return None



# ===================================================================
# 3.                     JSON FILE DISCOVERY
# ===================================================================

def _iter_json_files(folder: Path, recursive: bool = True) -> List[Path]:
    """Klasördeki *.json dosyalarını (case-insensitive) sıralı döndürür.

    recursive=True: alt klasörleri de tarar (rglob). Bu, UI'nin 'data_base' altında
    ülke klasörleri gibi yapıları desteklemesini sağlar.
    """
    folder = Path(folder)
    if not folder.exists() or not folder.is_dir():
        return []
    if recursive:
        files = [p for p in folder.rglob("*") if p.is_file() and p.suffix.lower() == ".json"]
    else:
        files = [p for p in folder.iterdir() if p.is_file() and p.suffix.lower() == ".json"]
    return sorted(files)


def _load_json_files(
    json_files: List[Path],
    folder_label: str,
    strict: bool = False,
) -> Tuple[pd.DataFrame, LoadReport]:
    """
    Klasör / dosya giriş noktalarının paylaştığı çekirdek yükleyici.

    strict=False:
      - hatalı kayıtları atlar, issues'a yazar

    strict=True:
      - JSON parse hatasında veya kayıt validasyonu fail olursa ValueError fırlatır
    """
    issues: List[LoadIssue] = []

    files_seen = len(json_files)
    files_loaded = 0
    records_seen = 0
    records_loaded = 0

    rows: List[Dict[str, Any]] = []

    # JSON dosyası yoksa erken uyarı/hata üretmek daha açıklayıcı olur
    if files_seen == 0:
        issues.append(LoadIssue.error(file="*", message="No JSON files found."))
        report = LoadReport(
            folder=str(folder_label),
            files_seen=0,
            files_loaded=0,
            records_seen=0,
            records_loaded=0,
            issues=issues,
        )
        return pd.DataFrame([]), report

    for fp in json_files:
        obj, err = _safe_read_json(fp)
        if err is not None:
            issues.append(LoadIssue.error(file=fp.name, message=f"JSON parse failed: {err}"))
            if strict:
                raise ValueError(f"{fp.name}: JSON parse failed: {err}")
            continue

        files_loaded += 1

        records = _normalize_container(obj)
        records_seen += len(records)

        # Kapsayıcı boşsa (ör. {} veya []), bunu da raporlamak faydalı
        if len(records) == 0:
            issues.append(LoadIssue.warn(file=fp.name, message="JSON contained no valid dict records (empty container)."))
            continue

        for i, entry in enumerate(records):
            # Kayıt id’sini raporlamak debug’da çok işe yarıyor
            rec_id = _first_nonempty(entry.get("Uni_ID"), entry.get("id"), entry.get("University_Short_Name"), entry.get("short"), entry.get("University_Name"), entry.get("name"))

            # Minimal validasyon
            v = _validate_record_minimal(entry)
            if v is not None:
                issues.append(LoadIssue.error(file=fp.name, message=v, record_index=i, record_id=rec_id))
                if strict:
                    raise ValueError(f"{fp.name}[{i}]: {v}")
                continue

            # Temel alanlar
            uni = _record_display_name(entry)
            city, state, country = _extract_location(entry)

            # scope filtresi: yeni şemada tek tarif non_eu
            rec_scope_raw = _first_nonempty(entry.get("Program_Scope"), entry.get("scope"), "")
            rec_scope = str(rec_scope_raw).strip().lower()
            if rec_scope and rec_scope not in ("non_eu", "non-eu", "noneu"):
                issues.append(
                    LoadIssue.warn(
                        file=fp.name,
                        message=f"Skipped record due to scope='{rec_scope_raw}' (expecting non_eu).",
                        record_index=i,
                        record_id=rec_id,
                    )
                )
                continue


            # City eksikse warn (strict değilse kayıt yine alınabilir)
            if not city:
                issues.append(
                    LoadIssue.warn(
                        file=fp.name,
                        message="Missing city (location.city/city).",
                        record_index=i,
                        record_id=rec_id,
                    )
                )

            cost_key, cost_raw = _normalize_cost(entry)

            semester_fee = _extract_semester_fee(entry)
            if semester_fee is None:
                issues.append(
                    LoadIssue.warn(
                        file=fp.name,
                        message="Missing semester fee (semester_fees/semester_fee).",
                        record_index=i,
                        record_id=rec_id,
                    )
                )

            strength, focus, pros, cons, tags_str = _extract_text_fields(entry)
            updated_at = _first_nonempty(entry.get("Meta_Updated_At"), entry.get("updated_at"), entry.get("updated"), "")


            # Yeni şema alanları (flatten)
            tuition_eur_per_year, tuition_raw, tuition_program, tuition_period, tuition_scope = _extract_tuition(entry, prefer_scope="non_eu")

            target_program_name, target_program_degree, target_program_ects, target_program_url = _extract_target_program(entry)
            winter_opens, winter_closes, summer_opens, summer_closes, deadlines_note = _extract_deadlines(entry)

            # Housing bilgisi hem root'ta hem logistics içinde gelebilir
            logistics_obj = entry.get("logistics") if isinstance(entry.get("logistics"), dict) else {}
            housing_difficulty = _first_nonempty(entry.get("Living_Housing_Difficulty"), entry.get("housing_difficulty"), logistics_obj.get("housing_difficulty"), "")
            housing_difficulty_score = _coerce_int(_first_nonempty(entry.get("Living_Housing_Score"), entry.get("housing_difficulty_score"), logistics_obj.get("housing_difficulty_score"), None))

            key_partners = _extract_key_partners(entry)
            scholarship_names, scholarships_json = _extract_scholarships(entry)

            # Not: source JSON'u istersen burada string olarak da saklayabilirsin
            # (UI'da “kaynak JSON göster” toggle'ı için işe yarar)
            rows.append(
                {
                    # Kimlik / isim
                    "id": _first_nonempty(entry.get("Uni_ID"), entry.get("id"), ""),
                    "name": _first_nonempty(entry.get("University_Name"), entry.get("name"), ""),
                    "display_name": _first_nonempty(entry.get("University_Display_Name"), entry.get("display_name"), ""),
                    "short": _first_nonempty(entry.get("University_Short_Name"), entry.get("short"), ""),
                    "university": uni,  # UI'da gösterilecek ana isim

                    # Konum
                    "city": city,
                    "state": state,
                    "country": country,

                    # Kapsam / doğrulama bayrakları
                    "scope": _first_nonempty(entry.get("Program_Scope"), entry.get("scope"), ""),
                    "needs_verification": _coerce_bool(_first_nonempty(entry.get("Meta_Needs_Verification"), entry.get("needs_verification"))),

                    # Şehir maliyeti
                    "cost_city": cost_key,          # normalize key
                    "cost_city_raw": cost_raw,      # gösterilebilir ham değer
                    "city_cost_rank": _coerce_int(_first_nonempty(entry.get("Cost_City_Rank"), entry.get("city_cost_rank"))),

                    # Dönem katkı / ücret
                    "semester_fee_eur": semester_fee,
                    "semester_fees_json": _json_compact(entry.get("Cost_Semester_Fees") or entry.get("semester_fees")),

                    # Tuition (yıllık eşdeğer)
                    "tuition_eur_per_year": tuition_eur_per_year,
                    "tuition_raw": tuition_raw,
                    "tuition_program": tuition_program,
                    "tuition_period": tuition_period,
                    "tuition_scope": tuition_scope,
                    "tuition_json": _json_compact(entry.get("Cost_Tuition") or entry.get("tuition")),

                    # Akademik / içerik alanları
                    "aerospace_ecosystem": _first_nonempty(entry.get("Industry_Ecosystem"), entry.get("aerospace_ecosystem"), ""),
                    "strong_areas_summary": _first_nonempty(entry.get("Analysis_Strong_Areas"), entry.get("strong_areas_summary"), ""),
                    "strength": strength,
                    "focus": focus,
                    "pros": pros,
                    "cons": cons,
                    "tags": tags_str,
                    "tags_raw": _first_nonempty(entry.get("tags_raw"), ""),

                    # Hedef program
                    "target_program_name": target_program_name,
                    "target_program_degree": target_program_degree,
                    "target_program_ects": target_program_ects,
                    "target_program_url": target_program_url,
                    "target_program_json": _json_compact(entry.get("target_program") or {
                        "name": entry.get("Program_Name"),
                        "degree": entry.get("Program_Degree"),
                        "ects": entry.get("Program_ECTS"),
                        "url": entry.get("Program_URL"),
                        "scope": entry.get("Program_Scope"),
                    }),

                    # Kabul / dil
                    "admission_mode": _first_nonempty(entry.get("Admission_Mode"), entry.get("admission_mode"), ""),
                    "language_req": _first_nonempty(entry.get("Admission_Language_Req"), entry.get("language_req"), ""),

                    # Internship (opsiyonel)
                    "internship_mandatory": _coerce_bool(_first_nonempty(entry.get("Internship_Mandatory"), entry.get("internship_mandatory"))),
                    "internship_notes": _first_nonempty(entry.get("Internship_Notes"), entry.get("internship_notes"), ""),

                    # Deadline (flatten)
                    "deadline_winter_opens": winter_opens,
                    "deadline_winter_closes": winter_closes,
                    "deadline_summer_opens": summer_opens,
                    "deadline_summer_closes": summer_closes,
                    "deadlines_note": deadlines_note,
                    "deadlines_json": _json_compact(
                        entry.get("deadlines")
                        or {
                            "winter": {
                                "opens": entry.get("Deadline_Winter_Open"),
                                "closes": entry.get("Deadline_Winter_Close"),
                                "note": entry.get("Deadline_Winter_Note"),
                            },
                            "summer": {
                                "opens": entry.get("Deadline_Summer_Open"),
                                "closes": entry.get("Deadline_Summer_Close"),
                                "note": entry.get("Deadline_Summer_Note"),
                            },
                            "note": entry.get("Deadline_General_Note"),
                        }
                    ),
                    "housing_difficulty": housing_difficulty,
                    "housing_difficulty_score": housing_difficulty_score,

                    # Partner / industry
                    "key_partners": key_partners,
                    "industry_focus_json": _json_compact(entry.get("industry_focus")),
                    "logistics_json": _json_compact(entry.get("logistics")),
                    "admission_details_json": _json_compact(entry.get("admission_details")),

                    # Burslar / kaynaklar
                    "scholarship_names": scholarship_names,
                    "scholarships_json": scholarships_json,
                    "sources_json": _json_compact(entry.get("Meta_Sources") or entry.get("sources")),

                    # Meta
                    "source_file": fp.name,
                    "updated_at": updated_at,
                }
            )
            records_loaded += 1

    df = pd.DataFrame(rows)

    # Hiç geçerli kayıt yoksa error üret
    if df.empty:
        issues.append(LoadIssue.error(file="*", message="No valid records loaded from any JSON."))
        if strict:
            raise ValueError("No valid records loaded from any JSON.")

    report = LoadReport(
        folder=str(folder_label),
        files_seen=files_seen,
        files_loaded=files_loaded,
        records_seen=records_seen,
        records_loaded=records_loaded,
        issues=issues,
    )
    return df, report



# ===================================================================
# 4.                          PUBLIC API
# ===================================================================

def load_database_folder(folder: Path, strict: bool = False) -> Tuple[pd.DataFrame, LoadReport]:
    """
    Klasör altındaki tüm *.json dosyalarını okur, tek bir DataFrame + rapor döndürür.

    strict=False:
      - hatalı kayıtları atlar, issues'a yazar

    strict=True:
      - JSON parse hatası veya kayıt validasyonu fail => ValueError
    """
    folder = Path(folder)
    if not folder.exists() or not folder.is_dir():
        raise FileNotFoundError(f"Folder not found: {folder}")

    json_files = _iter_json_files(folder)
    return _load_json_files(json_files=json_files, folder_label=str(folder), strict=strict)


def load_database(
    path: Path,
    strict: bool = False,
    include_siblings_if_file: bool = True,
) -> Tuple[pd.DataFrame, LoadReport]:
    """
    Kullanım kolaylığı wrapper'ı.

    - `path` bir klasörse: o klasördeki tüm JSON'ları yükler.
    - `path` bir JSON dosyasıysa:
        - include_siblings_if_file=True  -> aynı klasördeki TÜM JSON'lar yüklenir (UI dosya seçici senaryosu)
        - include_siblings_if_file=False -> sadece seçilen dosya yüklenir

    Not: Bu davranış, tek bir ülke dosyası seçilse bile yanındaki diğer ülke JSON'larının
    otomatik ingest edilmesini sağlar.
    """
    p = Path(path)

    if p.exists() and p.is_dir():
        return load_database_folder(p, strict=strict)

    if p.exists() and p.is_file() and p.suffix.lower() == ".json":
        if include_siblings_if_file:
            return load_database_folder(p.parent, strict=strict)
        return _load_json_files(json_files=[p], folder_label=str(p.parent), strict=strict)

    raise FileNotFoundError(f"Path not found or not a .json/.folder: {p}")



# ===================================================================
# 5.                 TESTING JSON_LOADER.PY (Diagnostics)
# ===================================================================

if __name__ == "__main__":
    import sys
    import argparse

    # Pandas çıktı ayarları (tablo terminalde kesilmesin)
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 1200)
    pd.set_option("display.max_rows", 30)

    def _hr(ch: str = "-", n: int = 72) -> str:
        return ch * n

    def _count_json(folder: Path, recursive: bool = False) -> int:
        """Klasördeki .json sayısını döndürür (opsiyonel recursive)."""
        if not folder.exists() or not folder.is_dir():
            return 0
        if recursive:
            return sum(1 for p in folder.rglob("*.json") if p.is_file())
        return sum(1 for p in folder.glob("*.json") if p.is_file())

    def _guess_data_folder() -> Optional[Path]:
        """
        Muhtemel veri klasörünü bulmaya çalışır.
        - Önce proje kökü civarında data_base / data gibi yerler
        - Sonra cwd
        """
        current_path = Path(__file__).resolve()
        candidates = [
            current_path.parent.parent / "clean_data_base",  # proje_root/data_base
            current_path.parent.parent / "data",       # proje_root/data
            current_path.parent.parent,                # proje_root (jsonlar buradaysa)
            current_path.parent / "data_base",         # assets/data_base
            Path.cwd(),                                # çalıştırılan yer
        ]

        best: Optional[Path] = None
        best_count = 0

        for cand in candidates:
            c = _count_json(cand, recursive=False)
            if c > best_count:
                best = cand
                best_count = c

        if best and best_count > 0:
            return best
        return None

    def _print_issue_block(title: str, issues: list, max_items: int = 12) -> None:
        """Issue listesini kontrollü basar (spami önler)."""
        if not issues:
            return
        print(f"\n{title} ({len(issues)}):")
        for j, it in enumerate(issues[:max_items]):
            rid = f" | ID={it.record_id}" if it.record_id else ""
            rix = f" | idx={it.record_index}" if it.record_index is not None else ""
            print(f"  - {it.file}{rix}{rid} :: {it.message}")
        if len(issues) > max_items:
            print(f"  ... ({len(issues) - max_items} daha)")

    # -------------------------
    # CLI argümanları
    # -------------------------
    ap = argparse.ArgumentParser(description="JSON Loader Diagnostics")
    ap.add_argument("--folder", type=str, default="", help="Veri klasörü yolu (boşsa otomatik bulunur)")
    ap.add_argument("--strict", action="store_true", help="Strict mod (ilk hatada ValueError)")
    ap.add_argument("--recursive", action="store_true", help="JSON aramasını alt klasörlere de genişlet")
    ap.add_argument("--max-issues", type=int, default=12, help="Her kategori için gösterilecek max issue sayısı")
    ap.add_argument("--head", type=int, default=10, help="DataFrame önizleme satır sayısı")
    args = ap.parse_args()

    print(_hr("="))
    print("JSON DATA LOADER DIAGNOSTICS")
    print(_hr("="))

    # -------------------------
    # 1) Veri klasörünü belirle
    # -------------------------
    target_folder: Optional[Path] = None

    if args.folder:
        cand = Path(args.folder).expanduser().resolve()
        if cand.exists() and cand.is_dir():
            target_folder = cand
        else:
            print(f"[ERROR] Verilen klasör geçersiz: {cand}")
            sys.exit(2)
    else:
        target_folder = _guess_data_folder()

    if not target_folder:
        print("[ERROR] Otomatik olarak JSON veri klasörü bulunamadı.")
        print("İpucu: --folder <path> ile klasör ver.")
        sys.exit(1)

    json_count = _count_json(target_folder, recursive=args.recursive)
    print(f"[INFO] Veri kaynağı: {target_folder}")
    print(f"[INFO] JSON sayısı: {json_count} (recursive={args.recursive})")

    if json_count == 0:
        print("[ERROR] Bu klasörde JSON bulunamadı.")
        sys.exit(1)

    # -------------------------
    # 2) Yükleme
    # -------------------------
    try:
        print(_hr())
        print(f"> Veriler yükleniyor... (strict={args.strict})")

        # Not: recursive açıksa load_database_folder değil, load_database kullanmak daha doğru olabilir.
        # Ama mevcut loader sadece bir klasördeki jsonları okuyor. Recursive isteniyorsa,
        # burada rglob ile dosya listesi toplayıp _load_json_files'e vermek gerekir.
        # Şimdilik recursive=False varsayıyoruz; recursive True ise uyarı verelim.
        if args.recursive:
            print("[WARN] recursive=True seçildi ama loader şu an sadece klasör içi JSON okuyor.")
            print("       İstersen recursive desteğini loader’a da ekleyebiliriz.")

        df, report = load_database_folder(target_folder, strict=args.strict)

    except Exception as e:
        print(_hr())
        print("[CRITICAL] Yükleme sırasında beklenmedik hata:")
        print(e)
        import traceback
        traceback.print_exc()
        sys.exit(3)

    # -------------------------
    # 3) Rapor özeti
    # -------------------------
    print(_hr())
    print("TARAMA RAPORU")
    print(_hr())
    print(f"Klasör          : {report.folder}")
    print(f"Dosyalar        : {report.files_loaded} / {report.files_seen} yüklendi")
    print(f"Kayıtlar        : {report.records_loaded} / {report.records_seen} işlendi")
    print(f"Issue sayısı    : {len(report.issues)}")

    warns = [i for i in report.issues if i.level == "warn"]
    errs = [i for i in report.issues if i.level == "error"]

    print(f"Hatalar (error) : {len(errs)}")
    print(f"Uyarılar (warn) : {len(warns)}")

    if errs:
        _print_issue_block("[!!!] KRİTİK HATALAR", errs, max_items=args.max_issues)

    if warns:
        _print_issue_block("[!] UYARILAR", warns, max_items=args.max_issues)
    else:
        print("\n[OK] Uyarı yok. Veri temiz görünüyor.")

    # -------------------------
    # 4) DataFrame inceleme
    # -------------------------
    print(_hr())
    print("DATAFRAME ÖZETİ")
    print(_hr())

    if df.empty:
        print("[WARN] DataFrame boş döndü.")
        sys.exit(0)

    print(f"Satır sayısı: {len(df)}")
    print(f"Sütun sayısı: {len(df.columns)}")

    # Kritik sütunlar
    cols = ["university", "city", "semester_fee_eur", "cost_city", "source_file", "updated_at"]
    cols = [c for c in cols if c in df.columns]

    print(_hr())
    print(f"ÖNİZLEME (ilk {args.head})")
    print(_hr())
    print(df[cols].head(args.head))

    # Basit istatistikler
    print(_hr())
    print("İSTATİSTİKLER")
    print(_hr())

    if "semester_fee_eur" in df.columns:
        fee = df["semester_fee_eur"]
        missing = fee.isna().sum()
        try:
            mean_fee = float(fee.mean())
            med_fee = float(fee.median())
            print(f"Semester fee ortalama : €{mean_fee:.2f}")
            print(f"Semester fee medyan   : €{med_fee:.2f}")
        except Exception:
            print("Semester fee istatistikleri hesaplanamadı (tip uyumsuzluğu olabilir).")
        print(f"Ücret eksik kayıt      : {missing}")

    if "cost_city" in df.columns:
        vc = df["cost_city"].value_counts(dropna=False).head(8)
        print("\nCost dağılımı (top 8):")
        print(vc)

    # Kaynak dosya dağılımı
    if "source_file" in df.columns:
        vc = df["source_file"].value_counts().head(10)
        print("\nKaynak dosyalar (top 10):")
        print(vc)

    print(_hr("="))
    print("DONE")
    print(_hr("="))

