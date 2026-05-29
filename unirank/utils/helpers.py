import typing
from typing import Any, Dict, List, Optional, Tuple, Union, Set, Sequence
import re
import numpy as np
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
LOG_PATH = BASE_DIR / "unirank.log"

# ---------------------------------------------------------------------
# Theme & Widget Loader (assets.* varsa onu kullan; yoksa local)
# ---------------------------------------------------------------------

# Package layout: assets/theme.py, assets/widgets.py, assets/json_loader.py
from unirank.ui.theme import apply_theme, ThemeConfig
from unirank.ui.widgets import (
    Sidebar,
    PrimaryButton,
    SecondaryButton,
    TableSettingsButton,
    DetailsDrawer,
    DetailHoverButton,
    WeightSliderRow,
    HashtagFilterPanel,
    apply_hashtag_filters,
    apply_ranking_delegates,
    apply_shadow,
    clamp01 as clamp01,
    ModernCard,
    KPICard,
    SearchBar,
)
from unirank.core.json_loader import load_database, parse_fee_to_eur, LoadReport, LoadIssue


# ===================================================================
# 1.                          HELPERS
# ===================================================================

# ------------------------------------------------------------
# Yaşam maliyeti etiketlerini sayısala çevirme haritası
# Not: Bu değerler "rank" gibi davranır. DÜŞÜK daha iyidir.
# Sonrasında normalize_inverse ile "goodness" (0..1) üretiriz.
# ------------------------------------------------------------
COST_MAP: Dict[str, float] = {
    # EN
    "very_low": 1.0,
    "low": 2.0,
    "medium_low": 2.5,
    "medium": 3.0,
    "medium_high": 4.0,
    "high": 5.0,
    "very_high": 6.0,
    # TR (farklı yazımlar)
    "çok_düşük": 1.0,
    "düşük": 2.0,
    "orta-düşük": 2.5,
    "orta_düşük": 2.5,
    "orta": 3.0,
    "orta-yüksek": 4.0,
    "orta_yüksek": 4.0,
    "yüksek": 5.0,
    "çok_yüksek": 6.0,
}



_SEARCH_HASHTAG_RE = re.compile(r"#([\w\-]+)", flags=re.UNICODE)
_SEARCH_QUOTE_RE = re.compile(r'"([^"]+)"|\'([^\']+)\'', flags=re.UNICODE)

def normalize_keywords(
    keywords: Sequence[str],
    *,
    min_len: int = 2,
    max_terms: int = 25,
) -> List[str]:
    out: List[str] = []
    seen: set[str] = set()

    if not keywords:
        return out

    for k in keywords:
        s = str(k or "").strip().casefold()  # lower() yerine casefold(): TR için daha doğru
        if len(s) < int(min_len):
            continue
        if s in seen:
            continue
        seen.add(s)
        out.append(s)
        if len(out) >= int(max_terms):
            break
    return out


def parse_search_query(q: str) -> Tuple[List[str], List[str]]:
    """Arama alanı: (terms, hashtags) döndürür."""
    if not q:
        return [], []

    q = str(q).strip()
    if not q:
        return [], []

    hashtags = [
        (m.group(1) or "").strip().casefold()
        for m in _SEARCH_HASHTAG_RE.finditer(q)
        if (m.group(1) or "").strip()
    ]
    q_wo_hash = _SEARCH_HASHTAG_RE.sub(" ", q)

    phrases: List[str] = []
    for m in _SEARCH_QUOTE_RE.finditer(q_wo_hash):
        ph = (m.group(1) or m.group(2) or "").strip()
        if ph:
            phrases.append(ph.casefold())
    q_wo_quotes = _SEARCH_QUOTE_RE.sub(" ", q_wo_hash)

    words = [w.strip().casefold() for w in re.split(r"[\s,;]+", q_wo_quotes) if w.strip()]

    terms = normalize_keywords(phrases + words, min_len=1, max_terms=40)
    hashtags = normalize_keywords(hashtags, min_len=1, max_terms=40)
    return terms, hashtags


def vectorized_text_match_score(
    series: pd.Series,
    keywords: Sequence[str],
    *,
    case: bool = False,
    regex: bool = False,
    default_if_no_keywords: float = 0.5,
) -> pd.Series:
    keys = normalize_keywords(keywords, min_len=1, max_terms=40)

    n = int(len(series))
    if not keys:
        return pd.Series(np.full(n, float(default_if_no_keywords)), index=series.index)

    s = series.astype("string").fillna("")

    # TR + unicode için: case-insensitive arama yapacaksak casefold ederek hız + stabilite kazanırız.
    # regex=True ise dokunmayalım (regex semantiği bozulmasın).
    if (not case) and (not regex):
        s = s.str.casefold()
        keys = [k.casefold() for k in keys]
        case = True  # artık case-sensitive bakıyoruz çünkü zaten casefold yaptık

    hits = np.zeros(n, dtype=np.float32)
    for k in keys:
        try:
            m = s.str.contains(k, case=case, regex=regex, na=False)
        except re.error:
            # Kullanıcı regex bozacak şey yazarsa çökmesin: literal'e düş
            m = s.str.contains(re.escape(k), case=True, regex=True, na=False)
        hits += m.to_numpy(dtype=np.float32)

    denom = float(len(keys))
    return pd.Series(hits / denom, index=series.index)


def vectorized_text_match_multi(
    df: pd.DataFrame,
    columns: Sequence[str],
    keywords: Sequence[str],
    *,
    case: bool = False,
    regex: bool = False,
    default_if_no_keywords: float = 0.5,
) -> pd.Series:
    cols = [c for c in (columns or []) if c in df.columns]
    if not cols:
        return pd.Series(np.full(len(df), float(default_if_no_keywords)), index=df.index)

    s = df[cols].astype("string").fillna("")

    combined = s.iloc[:, 0]
    for c in cols[1:]:
        combined = combined + " | " + s[c]

    return vectorized_text_match_score(
        combined,
        keywords,
        case=case,
        regex=regex,
        default_if_no_keywords=default_if_no_keywords,
    )


def _series(df: pd.DataFrame, col: str) -> pd.Series:
    """Text-match için güvenli seri."""
    if col in df.columns:
        return df[col]
    return pd.Series([""] * len(df), index=df.index, dtype="string")


# ------------------------------------------------------------
# Normalize yardımcıları:
# normalize01: vmin..vmax -> 0..1
# normalize_inverse: "küçük daha iyi" metrikler için 1 - normalize01
# Not: clamp01 widgets.py içinde var, import ediliyor.
# ------------------------------------------------------------
def normalize01(v: float, vmin: float, vmax: float, *, default: float = 0.5) -> float:
    try:
        v = float(v)
        vmin = float(vmin)
        vmax = float(vmax)
    except Exception:
        return float(default)

    if (not np.isfinite(v)) or (not np.isfinite(vmin)) or (not np.isfinite(vmax)) or (vmax <= vmin):
        return float(default)

    t = (v - vmin) / (vmax - vmin)
    return float(clamp01(t))

def normalize_inverse(v: float, vmin: float, vmax: float, *, default: float = 0.5) -> float:
    return float(1.0 - normalize01(v, vmin, vmax, default=default))



# ===================================================================
# 2.                          Ranked Model
# ===================================================================

