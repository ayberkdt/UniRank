import typing
from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
import pandas as pd
import numpy as np
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QAbstractTableModel, QModelIndex

class RankedModel(QAbstractTableModel):
    """DataFrame -> QTableView adapter (stabil + formatlı + sıralanabilir)."""

    # Kolon bazlı format + hizalama
    _FMT: Dict[str, Tuple[str, Qt.AlignmentFlag]] = {
        "Skor": ("{:.3f}", Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight),
        "Semester fee (€)": ("{:.2f}", Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight),
        "Hedefe uyum": ("{:.2f}", Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight),
        # İstersen buraya yeni kolonlar da ekleyebilirsin:
        # "Tuition (€/yr)": ("{:.0f}", Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight),
    }

    # Kalın gösterilecek kolonlar
    _BOLD_COLS = {"Skor", "Üniversite"}

    # Tabloyu daha okunur yapmak için istediğimiz kolon sırası (varsa başa alınır)
    _PREFERRED_ORDER = [
        "Üniversite",
        "Şehir",
        "Ülke",
        "Skor",
        "Hedefe uyum",
        "Semester fee (€)",
        "Detay",
    ]

    def __init__(self) -> None:
        super().__init__()
        self._df = pd.DataFrame()
        self._cols: List[str] = []

    # -------------------------
    # Public API
    # -------------------------
    def set_df(self, df: Optional[pd.DataFrame]) -> None:
        """Modeli yeni DataFrame ile güncelle (reset)."""
        self.beginResetModel()

        self._df = df.copy() if isinstance(df, pd.DataFrame) else pd.DataFrame()

        # Kolonları deterministik sıraya koy:
        self._cols = self._build_column_order(self._df)

        # df kolon sırasını modelin kolon sırasına uydur (var olan kolonları seç)
        if not self._df.empty and self._cols:
            self._df = self._df.reindex(columns=self._cols)

        self.endResetModel()

    # -------------------------
    # Qt required
    # -------------------------
    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return 0 if parent.isValid() else int(len(self._df))

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return 0 if parent.isValid() else int(len(self._cols))


    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.ItemDataRole.DisplayRole):
        if role != Qt.ItemDataRole.DisplayRole:
            return None
        if orientation == Qt.Orientation.Horizontal:
            if 0 <= section < len(self._cols):
                return self._cols[section]
            return ""
        # Satır numarası
        return str(section + 1)

    # -------------------------
    # Sorting (QTableView.setSortingEnabled(True) için)
    # -------------------------
    def sort(self, column: int, order: Qt.SortOrder = Qt.SortOrder.AscendingOrder) -> None:
        if self._df.empty or not (0 <= column < len(self._cols)):
            return

        colname = self._cols[column]
        ascending = (order == Qt.SortOrder.AscendingOrder)

        # Detay kolonu sıralanmasın
        if colname == "Detay":
            return

        self.layoutAboutToBeChanged.emit()
        try:
            # Sayısal kolonlarda numeric sort, diğerlerinde string sort
            s = self._df[colname]
            if pd.api.types.is_numeric_dtype(s):
                self._df = self._df.sort_values(by=colname, ascending=ascending, kind="mergesort", na_position="last")
            else:
                self._df = self._df.assign(_k=s.astype("string").fillna(""))
                self._df = self._df.sort_values(by="_k", ascending=ascending, kind="mergesort").drop(columns=["_k"])
        finally:
            self.layoutChanged.emit()

    # -------------------------
    # Internal helpers
    # -------------------------
    @classmethod
    def _build_column_order(cls, df: pd.DataFrame) -> List[str]:
        """PREFERRED_ORDER + kalan kolonlar (alfabetik) şeklinde stabil kolon listesi üret."""
        if df is None or df.empty:
            return list(df.columns) if isinstance(df, pd.DataFrame) else []

        cols = list(df.columns)

        # Öncelikli kolonlar: df’de varsa başa
        preferred = [c for c in cls._PREFERRED_ORDER if c in cols]

        # Kalanlar: “Detay” zaten varsa yukarıda taşınır; burada tekrar etmeyelim
        rest = [c for c in cols if c not in set(preferred)]

        # Kalanları alfabetik yaparsak her yüklemede zıplamaz
        rest_sorted = sorted(rest, key=lambda x: str(x).lower())

        return preferred + rest_sorted


    @staticmethod
    def _is_missing(val) -> bool:
        if val is None:
            return True
        if isinstance(val, (float, np.floating)):
            return (not np.isfinite(val)) or np.isnan(val)
        # list/dict/tuple/set gibi yapılarda pd.isna problem çıkarabilir → NA değil kabul et
        if isinstance(val, (list, tuple, set, dict, np.ndarray)):
            return False
        try:
            na = pd.isna(val)
            return bool(na) if isinstance(na, (bool, np.bool_)) else False
        except Exception:
            return False

    @staticmethod
    def _to_text(val) -> str:
        if isinstance(val, (list, tuple, set)):
            return ", ".join(str(x) for x in val)
        if isinstance(val, dict):
            try:
                return json.dumps(val, ensure_ascii=False)
            except Exception:
                return str(val)
        if isinstance(val, np.ndarray):
            return ", ".join(str(x) for x in val.tolist())
        return str(val)

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None

        r, c = index.row(), index.column()
        if r < 0 or c < 0 or r >= len(self._df) or c >= len(self._cols):
            return None

        colname = self._cols[c]
        val = self._df.iat[r, c]

        if role == Qt.ItemDataRole.DisplayRole:
            if colname == "Detay":
                return ""

            if self._is_missing(val):
                return ""

            if colname in self._FMT and isinstance(val, (int, float, np.integer, np.floating)):
                fmt, _align = self._FMT[colname]
                try:
                    return fmt.format(float(val))
                except Exception:
                    return self._to_text(val)

            return self._to_text(val)

        if role == Qt.ItemDataRole.TextAlignmentRole:
            if colname in self._FMT:
                return int(self._FMT[colname][1])
            return int(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)

        if role == Qt.ItemDataRole.FontRole:
            if colname in self._BOLD_COLS:
                f = QFont()
                f.setBold(True)
                return f
            return None

        if role == Qt.ItemDataRole.ToolTipRole:
            if self._is_missing(val):
                return None
            s = self._to_text(val).strip()
            if not s:
                return None
            return s if len(s) > 60 else None

        return None



# ===================================================================
# 3.                          Main Window
# ===================================================================

@dataclass
class Weights:
    cost_city: float = 0.30
    semester_fee: float = 0.20
    focus_fit: float = 0.40
    pros_bonus: float = 0.07
    cons_penalty: float = 0.03

    def normalized(self) -> "Weights":
        # Sadece ana 3 ağırlığı normalize et
        s = float(self.cost_city + self.semester_fee + self.focus_fit)
        if s <= 1e-9:
            return self
        return Weights(
            cost_city=self.cost_city / s,
            semester_fee=self.semester_fee / s,
            focus_fit=self.focus_fit / s,
            pros_bonus=self.pros_bonus,
            cons_penalty=self.cons_penalty,
        )

    def clamp_nonneg(self) -> "Weights":
        # Negatif girilirse patlamasın
        return Weights(
            cost_city=max(0.0, float(self.cost_city)),
            semester_fee=max(0.0, float(self.semester_fee)),
            focus_fit=max(0.0, float(self.focus_fit)),
            pros_bonus=max(0.0, float(self.pros_bonus)),
            cons_penalty=max(0.0, float(self.cons_penalty)),
        )


