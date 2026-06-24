# ranking_app.py
# -*- coding: utf-8 -*-
"""

UniRank – Modern Dashboard (PyQt6)

Üniversiteleri tek bir arayüzde incelemek, filtrelemek ve kişisel önceliklere göre puanlayıp
sıralamak için geliştirilmiş masaüstü uygulaması.

Uygulama; tek bir JSON dosyasını veya JSON dosyaları içeren bir klasörü yükler, temel alanları
(normalizasyon/ön-hazırlık) düzenler ve kullanıcı tarafından belirlenen ağırlıklara göre toplam
bir “Skor” hesaplayarak sonuçları tablo halinde gösterir.

Öne çıkan özellikler
- Etkileşimli filtreler (şehir seçimi, anahtar kelime arama, isteğe bağlı hashtag filtreleri)
- Ağırlık ayarlarıyla sıralama modelini anında değiştirme (masraf, ücret, uyum, artı/eksi etkisi)
- Sıralama seçenekleri ve dışa aktarma (CSV / JSON)
- Tablo görünümü + seçilen kayıt için detay çekmecesi (drawer)
- Tema tabanlı stil (mümkün olduğunca hardcode renk kullanılmaz; görünüm tema modülünden gelir)
- Debug loglama ve SAFE_MODE ile daha hafif/uyumlu çalışma modu

Beklenen veri şeması (kanonik; back-alias yok)
- university, city, cost_city, semester_fee_eur
İsteğe bağlı alanlar arama/uyum ve detayları zenginleştirir (ör. focus, strength, tags, program, pros, cons).

Bu dosya; ana arayüzü (MainWindow), sıralama hesaplarını ve uygulamanın başlangıç (entry point)
kodunu içerir.
"""

# ===================================================================
# 0.                         IMPORTS
# ===================================================================

from __future__ import annotations

import json
import logging
import os
import re
import sys
import time
import traceback
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd

from unirank.core.scoring import calculate_score

from PyQt6.QtCore import (
    QAbstractTableModel,
    QEvent,
    QModelIndex,
    QRect,
    Qt,
    QTimer,
)
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QComboBox,
    QTableView,
    QVBoxLayout,
    QWidget,
    QScrollArea,
    QTreeWidget,
    QTreeWidgetItem,
)

# ---------------------------------------------------------------------
# Path hygiene (project root + this file dir)
# ---------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR  # gerekirse BASE_DIR.parent yaparsın

for p in (PROJECT_ROOT, BASE_DIR):
    sp = str(p)
    if sp not in sys.path:
        sys.path.insert(0, sp)

# Log file (used by debug hooks + error dialogs)
from unirank.core.models import RankedModel, Weights
from unirank.utils.helpers import *
from unirank.utils.helpers import _series
from unirank.ui.theme import *
from unirank.ui.widgets import *
from unirank.core.json_loader import load_database

class MainWindow(QMainWindow):
    def __init__(self, theme: ThemeConfig):
        super().__init__()
        self.logger = logging.getLogger("UniRank")
        self.theme = theme

        # Window setup
        self.setWindowTitle("UniRank – Modern University Dashboard")
        self.resize(1600, 1000)

        # -------------------------
        # Database path (deterministik)
        # -------------------------
        default_folder = BASE_DIR / "data_base"
        cand_file = BASE_DIR / "almanya.json"

        if default_folder.exists():
            self.db_path = default_folder
        elif cand_file.exists():
            self.db_path = cand_file
        else:
            has_json = any(p.is_file() and p.suffix.lower() == ".json" for p in BASE_DIR.iterdir())
            self.db_path = BASE_DIR if has_json else default_folder  # folder yoksa bile path tutulur

        # Data storage
        self.df_raw: Optional[pd.DataFrame] = None
        self.df_ranked: Optional[pd.DataFrame] = None
        self.good_meta: Optional[pd.DataFrame] = None
        self._hashtag_filters: Dict[str, List[str]] = {}

        # Weights and model
        self.weights = Weights()
        self.model = RankedModel()
        self._colvis_initialized = False

        # Timers
        self._detail_hide_timer = QTimer(self)
        self._detail_hide_timer.setSingleShot(True)
        self._detail_hide_timer.timeout.connect(self._maybe_hide_drawer)
        self._hovering_detail_button = False

        self._recompute_timer = QTimer(self)
        self._recompute_timer.setSingleShot(True)
        self._recompute_timer.timeout.connect(self.recompute)

        # Build UI
        self._build_modern_ui()

        # Load database
        QTimer.singleShot(0, lambda: self.reload_db(auto=True))

    # -----------------------------------------------------------------
    # Modern UI Building
    # -----------------------------------------------------------------
    def _build_modern_ui(self) -> None:
        """Build modern dashboard interface (theme-friendly)."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(18, 18, 18, 18)
        main_layout.setSpacing(18)

        # =============================================================
        # 1) Sidebar
        # =============================================================
        self.sidebar = Sidebar()
        self.sidebar.setMinimumWidth(420)
        self.sidebar.setMaximumWidth(560)

        # Sidebar kendi layout'unu tutuyorsa onu kullan
        sidebar_layout = getattr(self.sidebar, "layout_", None)
        if sidebar_layout is None:
            sidebar_layout = QVBoxLayout(self.sidebar)
            self.sidebar.layout_ = sidebar_layout
        sidebar_layout.setContentsMargins(24, 24, 24, 24)
        sidebar_layout.setSpacing(22)

        sidebar_scroll = QScrollArea()
        sidebar_scroll.setWidgetResizable(True)
        sidebar_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        sidebar_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        sidebar_content = QWidget()
        sidebar_content_layout = QVBoxLayout(sidebar_content)
        sidebar_content_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_content_layout.setSpacing(24)

        # Database controls
        db_group = ModernCard("Database")
        db_layout = db_group.body_layout()
        db_layout.setContentsMargins(18, 18, 18, 18)
        db_layout.setSpacing(14)

        self.btn_load_folder = PrimaryButton("📁 Open Folder")
        self.btn_load_file = SecondaryButton("📄 Open JSON")
        self.btn_reload = SecondaryButton("🔄 Refresh")

        db_layout.addWidget(self.btn_load_folder)
        db_layout.addWidget(self.btn_load_file)
        db_layout.addWidget(self.btn_reload)

        # Filters
        filter_group = ModernCard("Filters")
        filter_layout = filter_group.body_layout()
        filter_layout.setContentsMargins(18, 18, 18, 18)
        filter_layout.setSpacing(18)

        # City filter
        city_layout = QHBoxLayout()
        city_layout.addWidget(QLabel("City:"))
        self.cb_city = QComboBox()
        self.cb_city.addItem("All Cities")
        city_layout.addWidget(self.cb_city)
        filter_layout.addLayout(city_layout)

        # Hashtag filter panel
        self.filter_panel = None
        try:
            self.filter_panel = HashtagFilterPanel(theme=self.theme)
            self.filter_panel.filtersChanged.connect(self.on_hashtag_filters_changed)
            filter_layout.addWidget(self.filter_panel)
        except Exception:
            logging.exception("HashtagFilterPanel init failed")
            self.filter_panel = None

        # Hard Filters
        self.cb_degree = QComboBox()
        self.cb_degree.addItems(["All", "BSc", "MSc", "PhD"])
        
        from PyQt6.QtWidgets import QCheckBox
        self.chk_english_only = QCheckBox("Only English-taught")
        
        self.in_max_tuition = QLineEdit()
        self.in_max_tuition.setPlaceholderText("Max Tuition (€/yr)")
        
        hf_layout = QVBoxLayout()
        hf_layout.addWidget(QLabel("Degree Level:"))
        hf_layout.addWidget(self.cb_degree)
        hf_layout.addWidget(self.chk_english_only)
        hf_layout.addWidget(QLabel("Max Tuition:"))
        hf_layout.addWidget(self.in_max_tuition)
        filter_layout.addLayout(hf_layout)

        # Categories
        search_layout = QVBoxLayout()
        search_layout.addWidget(QLabel("Academic/Field Categories:"))
        self.tree_categories = QTreeWidget()
        self.tree_categories.setHeaderHidden(True)
        self.tree_categories.setSelectionMode(QTreeWidget.SelectionMode.NoSelection)
        self.tree_categories.setMaximumHeight(200)
        
        from unirank.core.taxonomy import load_taxonomy
        taxonomy = load_taxonomy()
        
        parents = {}
        parent_tr_map = {}
        for subcat_id, info in taxonomy.items():
            p_val = info['parent']
            p_en = p_val['en'] if isinstance(p_val, dict) else p_val
            p_tr = p_val['tr'] if isinstance(p_val, dict) and 'tr' in p_val else p_en
            
            l_val = info['label']
            l_en = l_val['en'] if isinstance(l_val, dict) else l_val
            l_tr = l_val['tr'] if isinstance(l_val, dict) and 'tr' in l_val else l_en
            
            if p_en not in parents:
                parents[p_en] = []
                parent_tr_map[p_en] = p_tr
            parents[p_en].append((l_en, l_tr))
            
        for p_en, subs in parents.items():
            parent_item = QTreeWidgetItem(self.tree_categories)
            parent_item.setText(0, parent_tr_map[p_en])
            parent_item.setData(0, Qt.ItemDataRole.UserRole, p_en)
            parent_item.setFlags(parent_item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            parent_item.setCheckState(0, Qt.CheckState.Unchecked)
            
            for l_en, l_tr in subs:
                child_item = QTreeWidgetItem(parent_item)
                child_item.setText(0, l_tr)
                child_item.setData(0, Qt.ItemDataRole.UserRole, l_en)
                child_item.setFlags(child_item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
                child_item.setCheckState(0, Qt.CheckState.Unchecked)
                
        search_layout.addWidget(self.tree_categories)
        filter_layout.addLayout(search_layout)

        # Weights
        weights_group = ModernCard("Ranking Weights")
        weights_layout = weights_group.body_layout()
        weights_layout.setContentsMargins(18, 18, 18, 18)
        weights_layout.setSpacing(14)

        self.cb_preset = QComboBox()
        self.cb_preset.addItems(["Balanced", "Low Cost Priority", "Best Aerospace / Space Fit", "English-Only Safe Choice", "Career-Oriented", "Custom"])
        weights_layout.addWidget(QLabel("Preset Profile:"))
        weights_layout.addWidget(self.cb_preset)
        self.cb_preset.currentIndexChanged.connect(self.on_preset_changed)

        self.ws_academic = WeightSliderRow("Academic Fit", self.weights.academic_fit / 100.0, step=0.01)
        self.ws_eligibility = WeightSliderRow("Eligibility", self.weights.eligibility_language / 100.0, step=0.01)
        self.ws_cost = WeightSliderRow("Cost & Funding", self.weights.cost_funding / 100.0, step=0.01)
        self.ws_career = WeightSliderRow("Career / Research", self.weights.career_research / 100.0, step=0.01)
        self.ws_living = WeightSliderRow("Living Risk", self.weights.living_risk / 100.0, step=0.01)
        self.ws_confidence = WeightSliderRow("Data Confidence", self.weights.confidence_deadline / 100.0, step=0.01)

        for ws in (self.ws_academic, self.ws_eligibility, self.ws_cost, self.ws_career, self.ws_living, self.ws_confidence):
            ws.valueChanged.connect(lambda *_: self.on_weights_changed())
            weights_layout.addWidget(ws)

        # Sorting
        sort_group = ModernCard("Sorting")
        sort_layout = sort_group.body_layout()
        sort_layout.setContentsMargins(18, 18, 18, 18)
        sort_layout.setSpacing(12)

        self.cb_sort = QComboBox()
        self.cb_sort.addItems([
            "Score (High → Low)",
            "Tuition & Fees (Low → High)",
            "Cost (Low → High)",
            "University (A → Z)",
        ])
        sort_layout.addWidget(self.cb_sort)

        # Export
        export_group = ModernCard("Export")
        export_layout = export_group.body_layout()
        export_layout.setContentsMargins(18, 18, 18, 18)
        export_layout.setSpacing(12)

        self.btn_export_csv = SecondaryButton("📊 Export CSV")
        self.btn_export_json = SecondaryButton("📝 Export JSON")
        export_layout.addWidget(self.btn_export_csv)
        export_layout.addWidget(self.btn_export_json)

        # Sidebar content
        sidebar_content_layout.addWidget(db_group)
        sidebar_content_layout.addWidget(filter_group)
        sidebar_content_layout.addWidget(weights_group)
        sidebar_content_layout.addWidget(sort_group)
        sidebar_content_layout.addWidget(export_group)
        sidebar_content_layout.addStretch()

        sidebar_scroll.setWidget(sidebar_content)
        sidebar_layout.addWidget(sidebar_scroll)

        # =============================================================
        # 2) Main Panel
        # =============================================================
        main_panel = QWidget()
        main_panel.setObjectName("MainPanel")
        main_panel_layout = QVBoxLayout(main_panel)
        main_panel_layout.setContentsMargins(34, 34, 34, 34)
        main_panel_layout.setSpacing(28)

        header = QWidget()
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(18)

        title_layout = QHBoxLayout()
        title_widget = QWidget()
        title_inner = QVBoxLayout(title_widget)
        title_inner.setContentsMargins(0, 0, 0, 0)
        title_inner.setSpacing(6)

        title_label = QLabel("University Ranking Dashboard")
        title_label.setStyleSheet("font-size: 28px; font-weight: 800;")
        subtitle_label = QLabel("Analyze and compare universities based on your criteria")
        subtitle_label.setStyleSheet("font-size: 14px;")

        title_inner.addWidget(title_label)
        title_inner.addWidget(subtitle_label)

        title_layout.addWidget(title_widget)
        title_layout.addStretch()

        self.search_bar = SearchBar(theme=self.theme)
        self.search_bar.setMinimumWidth(320)
        title_layout.addWidget(self.search_bar)

        header_layout.addLayout(title_layout)

        # KPI Cards
        kpi_container = QWidget()
        kpi_layout = QHBoxLayout(kpi_container)
        kpi_layout.setContentsMargins(0, 0, 0, 0)
        kpi_layout.setSpacing(18)

        self.kpi_total = KPICard("Total Schools", "0", "🏛️")
        self.kpi_avg_fee = KPICard("Avg. Tuition & Fees", "0€", "💰")
        self.kpi_avg_score = KPICard("Avg. Score", "0.0", "⭐")
        self.kpi_avg_cost = KPICard("Avg. Cost", "Medium", "🏙️")

        kpi_layout.addWidget(self.kpi_total)
        kpi_layout.addWidget(self.kpi_avg_fee)
        kpi_layout.addWidget(self.kpi_avg_score)
        kpi_layout.addWidget(self.kpi_avg_cost)

        header_layout.addWidget(kpi_container)
        main_panel_layout.addWidget(header)

        # Table Card
        table_card = ModernCard("Ranking Results")
        table_card_layout = table_card.body_layout()
        table_card_layout.setContentsMargins(22, 22, 22, 22)
        table_card_layout.setSpacing(18)

        table_header = QHBoxLayout()
        table_header.addWidget(QLabel("Ranked Universities"))
        table_header.addStretch()
        self.btn_table_settings = None
        table_card_layout.addLayout(table_header)

        self.table = QTableView()
        self.table.setModel(self.model)
        self.table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        self.table.setAlternatingRowColors(True)

        try:
            self.table.viewport().setMouseTracking(True)
        except Exception:
            pass

        try:
            self.btn_table_settings = TableSettingsButton(
                self.table, parent=self, theme=self.theme, text="Columns", dialog_title="Table Settings"
            )
            table_header.addWidget(self.btn_table_settings)
        except Exception:
            self.btn_table_settings = None

        table_card_layout.addWidget(self.table)
        main_panel_layout.addWidget(table_card, 1)

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(main_panel, 1)

        # Details drawer
        self.drawer = DetailsDrawer(theme=self.theme, parent=main_panel)
        self.drawer.hide()
        if hasattr(self.drawer, "btn_close"):
            self.drawer.btn_close.clicked.connect(self.hide_details_drawer)

        try:
            self.drawer.installEventFilter(self)
            self.table.viewport().installEventFilter(self)
        except Exception:
            pass

        self._connect_signals()

        # Shadows (best-effort)
        try:
            for card in [db_group, filter_group, weights_group, sort_group, export_group, table_card]:
                apply_shadow(card)
            for kpi in [self.kpi_total, self.kpi_avg_fee, self.kpi_avg_score, self.kpi_avg_cost]:
                apply_shadow(kpi)
        except Exception:
            logging.exception("apply_shadow failed")

    def _connect_signals(self) -> None:
        # Database
        self.btn_reload.clicked.connect(lambda: self.reload_db(auto=False))
        self.btn_load_folder.clicked.connect(self.select_db_folder)
        self.btn_load_file.clicked.connect(self.select_db_file)

        # Export
        self.btn_export_csv.clicked.connect(self.on_export_csv)
        self.btn_export_json.clicked.connect(self.on_export_json)

        # Filters
        self.cb_city.currentIndexChanged.connect(lambda *_: self.schedule_recompute(30))
        self.tree_categories.itemChanged.connect(lambda *_: self.schedule_recompute(160))
        self.cb_sort.currentIndexChanged.connect(lambda *_: self.schedule_recompute(30))
        
        # Hard Filters
        self.cb_degree.currentIndexChanged.connect(lambda *_: self.schedule_recompute(30))
        self.chk_english_only.stateChanged.connect(lambda *_: self.schedule_recompute(30))
        self.in_max_tuition.textChanged.connect(lambda *_: self.schedule_recompute(160))

        # Search bar mirrors keywords
        self.search_bar.textChanged.connect(self.on_search_changed)

        # Table selection
        sel = self.table.selectionModel()
        if sel is not None:
            sel.selectionChanged.connect(self.on_row_selected)

    def on_search_changed(self, text: str) -> None:
        self.schedule_recompute(160)

    # -----------------------------------------------------------------
    # Drawer positioning and hover handling
    # -----------------------------------------------------------------
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._position_drawer()

    def _position_drawer(self) -> None:
        if not getattr(self, "drawer", None) or not self.centralWidget():
            return
        layout = self.centralWidget().layout()
        if layout is None or layout.count() < 2:
            return
        main_panel = layout.itemAt(1).widget()
        if not main_panel:
            return

        margin = 20
        w = 420
        h = main_panel.height() - margin * 2
        x = main_panel.width() - w - margin
        y = margin

        self.drawer.setGeometry(QRect(x, y, w, h))
        self.drawer.raise_()

    def eventFilter(self, obj, event):
        if obj is self.drawer:
            if event.type() == QEvent.Type.Enter:
                self._cancel_hide_drawer()
            elif event.type() == QEvent.Type.Leave:
                self._schedule_hide_drawer()

        if obj is self.table.viewport():
            if event.type() == QEvent.Type.Leave:
                self._hovering_detail_button = False
                self._schedule_hide_drawer()

        return super().eventFilter(obj, event)

    def show_details_drawer(self, row: int, *, force: bool = False) -> None:
        self._cancel_hide_drawer()
        self._show_details(row)
        self._position_drawer()

        self.drawer.show()
        self.drawer.raise_()

        if force:
            try:
                self.drawer.setFocus(Qt.FocusReason.MouseFocusReason)
            except Exception:
                pass

    def hide_details_drawer(self) -> None:
        self._cancel_hide_drawer()
        self.drawer.hide()

    def _schedule_hide_drawer(self, delay_ms: int = 220) -> None:
        self._detail_hide_timer.start(max(60, int(delay_ms)))

    def _cancel_hide_drawer(self) -> None:
        if self._detail_hide_timer.isActive():
            self._detail_hide_timer.stop()

    def _maybe_hide_drawer(self) -> None:
        if not self.drawer.isVisible():
            return
        if self.drawer.underMouse():
            return
        if self._hovering_detail_button:
            return
        self.drawer.hide()

    # -----------------------------------------------------------------
    # Database controls
    # -----------------------------------------------------------------
    def select_db_folder(self) -> None:
        start_dir = self.db_path if self.db_path.is_dir() else self.db_path.parent
        folder = QFileDialog.getExistingDirectory(self, "Select Database Folder", str(start_dir))
        if not folder:
            return
        self.db_path = Path(folder)
        self.reload_db(auto=False)

    def select_db_file(self) -> None:
        start_dir = self.db_path if self.db_path.is_dir() else self.db_path.parent
        path, _ = QFileDialog.getOpenFileName(self, "Select JSON File", str(start_dir), "JSON (*.json *.JSON)")
        if not path:
            return
        self.db_path = Path(path)
        self.reload_db(auto=False)

    def reload_db(self, *, auto: bool) -> None:
        t0 = time.perf_counter()
        try:
            logging.info("reload_db | auto=%s | db_path=%s", auto, self.db_path)

            # Loader: json_loader.load_database
            df, report = load_database(self.db_path, strict=False, include_siblings_if_file=False)
            logging.info("load_database: seen=%s loaded=%s files_loaded=%s files_seen=%s folder=%s", report.records_seen, report.records_loaded, report.files_loaded, report.files_seen, report.folder)
            if df is None:
                logging.info("load_database returned df=None")
            else:
                logging.info("load_database df shape=%s cols=%s", df.shape, list(df.columns))
            self.df_raw = self._prepare_raw_df(df)

            warn_n = sum(1 for i in report.issues if i.level == "warn")
            err_n = sum(1 for i in report.issues if i.level == "error")

            src_name = self.db_path.name if self.db_path.is_file() else Path(report.folder).name
            self.statusBar().showMessage(
                f"Source: {src_name} | Records: {report.records_loaded}/{report.records_seen} | "
                f"Files: {report.files_loaded}/{max(report.files_seen, report.files_loaded)} | "
                f"{warn_n} warnings, {err_n} errors | {time.perf_counter() - t0:.2f}s"
            )

            if df is None or df.empty:
                QMessageBox.warning(self, "Empty Database", "No valid records found.\n\nCheck that the folder contains *.json files (also in subfolders) and that records validate.")
                self.model.set_df(pd.DataFrame())
                self.df_ranked = None
                self.good_meta = None
                self._update_kpis()
                return

            self._refresh_city_combo()
            self._refresh_hashtag_filter_options()
            self.recompute()

        except Exception as e:
            logging.exception("reload_db failed")
            msg = (
                "Failed to load database.\n\n"
                f"Expected: {self.db_path} (folder or .json file)\n"
                f"Error: {e}\n\n"
                "Solutions:\n"
                "• Select a folder containing *.json files\n"
                "• Select a single .json file\n"
                "• Click Refresh\n"
                f"• Details in: {LOG_PATH.name}"
            )
            QMessageBox.warning(self, "Database Error", msg)
            self.statusBar().showMessage("Failed to load database")

    def _prepare_raw_df(self, df: pd.DataFrame) -> pd.DataFrame:
        """Pre-processing so recompute() stays fast and consistent."""
        if df is None:
            return pd.DataFrame()

        out = df.copy()

        # Keep raw cost category (for scoring) and normalize cost_city for UI bucket filters.
        # widgets.apply_hashtag_filters maps only {very_high/high/medium/low/very_low} buckets.
        if "cost_city" in out.columns and "cost_city_raw" not in out.columns:
            out["cost_city_raw"] = out["cost_city"]
        if "cost_city" in out.columns:
            _cc = (
                out["cost_city"]
                .astype("string")
                .fillna("medium")
                .str.strip()
                .str.lower()
                .str.replace(" ", "_", regex=False)
                .str.replace("-", "_", regex=False)
            )
            out["cost_city"] = _cc.replace({"medium_low": "low", "medium_high": "high"})


        # Cost numeric cache
        cost_src = "cost_city_raw" if "cost_city_raw" in out.columns else ("cost_city" if "cost_city" in out.columns else None)
        if cost_src is None:
            out["_cost_num"] = 3.0
        else:
            cost_txt = out.get(cost_src, pd.Series(["medium"] * len(out), index=out.index))
            cost_norm = (
                cost_txt.astype("string")
                .fillna("medium")
                .str.strip()
                .str.lower()
                .str.replace(" ", "_", regex=False)
                .str.replace("-", "_", regex=False)
            )
            out["_cost_num"] = cost_norm.map(COST_MAP).fillna(3.0).astype(float)

        # Fee numeric cache (semester fee)
        fee_src = None
        for cand in ("annual_fee_eur", "semester_fee_eur", "Cost_Semester_Fees", "semester_fee", "semester_fee_raw", "fee_eur"):
            if cand in out.columns:
                fee_src = cand
                break
        if fee_src is None:
            out["_fee"] = np.nan
        else:
            out["_fee"] = pd.to_numeric(out[fee_src], errors="coerce")

        # Optional: tuition annual cache
        if "tuition_eur_per_year" in out.columns:
            out["_tuition"] = pd.to_numeric(out["tuition_eur_per_year"], errors="coerce")
        else:
            out["_tuition"] = np.nan

        return out

    def _refresh_city_combo(self) -> None:
        prev = self.cb_city.currentText()
        self.cb_city.blockSignals(True)
        self.cb_city.clear()
        self.cb_city.addItem("All Cities")

        if self.df_raw is not None and (not self.df_raw.empty) and ("city" in self.df_raw.columns):
            cities = sorted({str(x).strip() for x in self.df_raw["city"].dropna().unique() if str(x).strip()})
            for c in cities:
                self.cb_city.addItem(c)

        if prev and prev != "All Cities":
            idx = self.cb_city.findText(prev)
            if idx >= 0:
                self.cb_city.setCurrentIndex(idx)

        self.cb_city.blockSignals(False)

    def _refresh_hashtag_filter_options(self) -> None:
        """Refresh hashtag filter panel options (best-effort)."""
        if getattr(self, "filter_panel", None) is None:
            return
        if self.df_raw is None or self.df_raw.empty:
            try:
                self.filter_panel.set_options(countries=[], research_tags=[])
            except Exception:
                pass
            return

        df = self.df_raw

        # Countries
        countries: List[str] = []
        if "country" in df.columns:
            countries = sorted({str(x).strip() for x in df["country"].dropna().unique() if str(x).strip()})

        # Research tags
        def _split_tokens(val: Any) -> List[str]:
            if val is None or (isinstance(val, float) and np.isnan(val)):
                return []
            if isinstance(val, (list, tuple, set)):
                out = []
                for x in val:
                    out.extend(_split_tokens(x))
                return out
            s = str(val).strip()
            if not s:
                return []
            raw_parts = re.split(r"[\n,;/\|]+", s)
            toks: List[str] = []
            for p in raw_parts:
                t = p.strip()
                if not t:
                    continue
                if t.startswith("#"):
                    t = t[1:].strip()
                if len(t) < 2:
                    continue
                toks.append(t)
            return toks

        tokens: List[str] = []
        for col in ("tags", "focus"):
            if col in df.columns:
                for v in df[col].tolist():
                    tokens.extend(_split_tokens(v))

        research_tags: List[str] = []
        if tokens:
            vc = pd.Series(tokens).value_counts()
            research_tags = vc.index.tolist()[:80]

        try:
            self.filter_panel.set_options(countries=countries, research_tags=research_tags)
        except Exception:
            logging.exception("filter_panel.set_options failed")

    # -----------------------------------------------------------------
    # Hashtag filter panel
    # -----------------------------------------------------------------
    def on_hashtag_filters_changed(self, filters: Dict[str, List[str]]) -> None:
        self._hashtag_filters = filters or {}
        self.schedule_recompute(60)

    # -----------------------------------------------------------------
    # Export
    # -----------------------------------------------------------------
    def on_export_csv(self) -> None:
        if self.df_ranked is None or self.df_ranked.empty:
            QMessageBox.information(self, "Info", "No data to export.")
            return
        path, _ = QFileDialog.getSaveFileName(self, "Export CSV", "ranked_universities.csv", "CSV (*.csv)")
        if not path:
            return
        try:
            self.df_ranked.to_csv(path, index=False, encoding="utf-8-sig")
            QMessageBox.information(self, "Success", "CSV exported successfully.")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to export CSV:\n{e}")

    def on_export_json(self) -> None:
        if self.df_ranked is None or self.df_ranked.empty:
            QMessageBox.information(self, "Info", "No data to export.")
            return
        path, _ = QFileDialog.getSaveFileName(self, "Export JSON", "ranked_universities.json", "JSON (*.json)")
        if not path:
            return
        try:
            out = self.df_ranked.to_dict(orient="records")
            Path(path).write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
            QMessageBox.information(self, "Success", "JSON exported successfully.")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to export JSON:\n{e}")

    # -----------------------------------------------------------------
    # KPI
    # -----------------------------------------------------------------
    def _update_kpis(self) -> None:
        if self.df_ranked is None or self.df_ranked.empty:
            self.kpi_total.setValue("0")
            self.kpi_avg_fee.setValue("0€")
            self.kpi_avg_score.setValue("0.0")
            self.kpi_avg_cost.setValue("N/A")
            return

        df = self.df_ranked

        # Total schools
        self.kpi_total.setValue(str(len(df)))

        # Avg fee
        fee_col = "Tuition & Fees (€)"
        if fee_col in df.columns:
            fees = pd.to_numeric(df[fee_col], errors="coerce")
            m = fees.mean()
            self.kpi_avg_fee.setValue(f"{m:.0f}€" if pd.notna(m) else "N/A")
        else:
            self.kpi_avg_fee.setValue("N/A")

        # Avg score
        score_col = "Skor"
        if score_col in df.columns:
            scores = pd.to_numeric(df[score_col], errors="coerce")
            m = scores.mean()
            self.kpi_avg_score.setValue(f"{m:.2f}" if pd.notna(m) else "0.0")
        else:
            self.kpi_avg_score.setValue("0.0")

        # Avg cost (best-effort)
        cost_col = "Masraf(şehir)" if "Masraf(şehir)" in df.columns else None
        if cost_col:
            s = df[cost_col].astype("string").fillna("").str.strip().str.lower()
            s = s.str.replace(" ", "_", regex=False).str.replace("-", "_", regex=False)
            num = pd.to_numeric(s.map(COST_MAP), errors="coerce")
            m = num.mean()
            if pd.isna(m):
                self.kpi_avg_cost.setValue("N/A")
            elif m <= 2.2:
                self.kpi_avg_cost.setValue("Low")
            elif m <= 3.2:
                self.kpi_avg_cost.setValue("Medium")
            elif m <= 4.2:
                self.kpi_avg_cost.setValue("High")
            else:
                self.kpi_avg_cost.setValue("Very High")
        else:
            self.kpi_avg_cost.setValue("N/A")

    # -----------------------------------------------------------------
    # Recompute orchestration
    # -----------------------------------------------------------------
    def schedule_recompute(self, delay_ms: int = 120) -> None:
        self._recompute_timer.start(max(0, int(delay_ms)))

    def on_preset_changed(self) -> None:
        p = self.cb_preset.currentText()
        w = {}
        if p == "Balanced": w = {'ac': 30, 'el': 20, 'co': 20, 'ca': 15, 'li': 10, 'cf': 5}
        elif p == "Low Cost Priority": w = {'ac': 20, 'el': 20, 'co': 35, 'ca': 10, 'li': 10, 'cf': 5}
        elif p == "Best Aerospace / Space Fit": w = {'ac': 45, 'el': 15, 'co': 10, 'ca': 20, 'li': 5, 'cf': 5}
        elif p == "English-Only Safe Choice": w = {'ac': 25, 'el': 35, 'co': 15, 'ca': 10, 'li': 10, 'cf': 5}
        elif p == "Career-Oriented": w = {'ac': 25, 'el': 15, 'co': 10, 'ca': 35, 'li': 10, 'cf': 5}
        
        if w:
            for slider, val in [
                (self.ws_academic, w['ac']),
                (self.ws_eligibility, w['el']),
                (self.ws_cost, w['co']),
                (self.ws_career, w['ca']),
                (self.ws_living, w['li']),
                (self.ws_confidence, w['cf']),
            ]:
                slider.blockSignals(True)
                slider.setValue(val / 100.0, emit=False)
                slider.blockSignals(False)
            
            self.on_weights_changed(custom=False)

    def on_weights_changed(self, custom=True) -> None:
        if custom:
            self.cb_preset.blockSignals(True)
            self.cb_preset.setCurrentText("Custom")
            self.cb_preset.blockSignals(False)
            
        self.weights = Weights(
            academic_fit=float(self.ws_academic.value()) * 100.0,
            eligibility_language=float(self.ws_eligibility.value()) * 100.0,
            cost_funding=float(self.ws_cost.value()) * 100.0,
            career_research=float(self.ws_career.value()) * 100.0,
            living_risk=float(self.ws_living.value()) * 100.0,
            confidence_deadline=float(self.ws_confidence.value()) * 100.0,
        )
        self.schedule_recompute(60)

    def recompute(self) -> None:
        try:
            if self.df_raw is None or self.df_raw.empty:
                self.model.set_df(pd.DataFrame())
                self.df_ranked = None
                self.good_meta = None
                self._update_kpis()
                return

            df = self.df_raw.copy()

            # City filter
            city = self.cb_city.currentText()
            if city and city != "All Cities" and "city" in df.columns:
                df = df[df["city"].astype(str) == city]

            # Hashtag filters
            filters = getattr(self, "_hashtag_filters", {})
            if filters:
                try:
                    df = apply_hashtag_filters(df, filters)
                except Exception:
                    logging.exception("apply_hashtag_filters failed")

            search_query = self.search_bar.text().strip().lower()
            if search_query:
                # filter dataframe based on raw text match across program/university
                mask = df.apply(lambda row: search_query in str(row.get('Program_Name', '')).lower() or search_query in str(row.get('university', '')).lower(), axis=1)
                df = df[mask]

            selected_cats = []
            for i in range(self.tree_categories.topLevelItemCount()):
                p_item = self.tree_categories.topLevelItem(i)
                if p_item.checkState(0) in (Qt.CheckState.Checked, Qt.CheckState.PartiallyChecked):
                    p_en = p_item.data(0, Qt.ItemDataRole.UserRole)
                    selected_cats.append(p_en if p_en else p_item.text(0))
                for j in range(p_item.childCount()):
                    c_item = p_item.child(j)
                    if c_item.checkState(0) == Qt.CheckState.Checked:
                        c_en = c_item.data(0, Qt.ItemDataRole.UserRole)
                        selected_cats.append(c_en if c_en else c_item.text(0))
            
            keywords = selected_cats

            if df.empty:
                self.model.set_df(pd.DataFrame())
                self.df_ranked = None
                self.good_meta = None
                self._update_kpis()
                return

            # Ranges & Preparations
            
            # Use calculate_score for each record
            weights_dict = self.weights.as_dict()
            
            try:
                max_t = float(self.in_max_tuition.text()) if self.in_max_tuition.text() else 0.0
            except ValueError:
                max_t = 0.0
                
            preferences = {
                'selectedKeywords': keywords,
                'degreeFilter': self.cb_degree.currentText(),
                'onlyEnglish': self.chk_english_only.isChecked(),
                'maxTuition': max_t,
                'minFieldFit': 0
            }

            records = df.to_dict(orient="records")
            results = []
            valid_indices = []
            
            for i, r in enumerate(records):
                res = calculate_score(r, preferences, weights_dict)
                if res['passed_hard_filters']:
                    valid_indices.append(i)
                    results.append(res)
                    
            if not valid_indices:
                self.model.set_df(pd.DataFrame())
                self.df_ranked = None
                self.good_meta = None
                self._update_kpis()
                return
                
            df = df.iloc[valid_indices].copy()
            df["score"] = [res['total_score'] / 10.0 for res in results] # 0-10 scale
            df["_scoringDetails"] = results

            # Sort
            mode = self.cb_sort.currentText()
            if mode.startswith("Score"):
                df = df.sort_values("score", ascending=False)
            elif mode.startswith("Tuition & Fees"):
                df = df.sort_values("_fee", ascending=True)
            elif mode.startswith("Cost"):
                df = df.sort_values("_cost_num", ascending=True)
            else:
                df = df.sort_values("university", ascending=True)

            # Display columns
            out = df.copy()
            cost_display_col = "cost_city_raw" if "cost_city_raw" in out.columns else ("cost_city" if "cost_city" in out.columns else None)

            col_pairs: List[Tuple[Optional[str], str]] = [
                ("university", "Üniversite"),
                ("city", "Şehir"),
                ("country", "Ülke"),
                (cost_display_col, "Masraf(şehir)"),
                ("_fee", "Tuition & Fees (€)"),
                ("tuition_eur_per_year", "Tuition (€/yr)"),
                ("_score_fit", "Hedefe uyum"),
                ("score", "Skor"),
                ("target_program_name", "Program"),
                ("target_program_degree", "Derece"),
                ("scholarship_names", "Burs"),
                ("admission_mode", "Kabul Modu"),
                ("language_req", "Dil"),
                ("strength", "Güçlü tarafı"),
                ("pros", "Avantaj"),
                ("cons", "Dezavantaj"),
                ("focus", "Güçlü alanlar"),
                ("source_file", "Kaynak JSON"),
            ]

            selected_cols: List[str] = []
            rename_map: Dict[str, str] = {}
            for src, dst in col_pairs:
                if not src:
                    continue
                if src not in out.columns:
                    out[src] = ""
                selected_cols.append(src)
                rename_map[src] = dst

            out = out[selected_cols].rename(columns=rename_map)
            out.insert(1, "Detay", "")

            for col in ("Skor", "Hedefe uyum", "Tuition & Fees (€)", "Tuition (€/yr)"):
                if col in out.columns:
                    try:
                        out[col] = pd.to_numeric(out[col], errors="coerce")
                    except Exception:
                        pass

            for col in ("Skor", "Hedefe uyum"):
                if col in out.columns:
                    try:
                        out[col] = out[col].astype(float).round(4)
                    except Exception:
                        pass

            self.df_ranked = out.reset_index(drop=True)

            # Ensure 'Detay' column exists (required for indexWidget buttons)
            if "Detay" not in self.df_ranked.columns:
                self.df_ranked["Detay"] = ""

            # Goodness meta (drawer radar)
            comps_list = [res['components'] for res in results]
            good = pd.DataFrame({
                "cost_good": [c['cost_funding'] / 100.0 for c in comps_list],
                "fee_good": [c['eligibility_language'] / 100.0 for c in comps_list],
                "fit_good": [c['academic_fit'] / 100.0 for c in comps_list],
                "pros_good": [c['career_research'] / 100.0 for c in comps_list],
                "cons_bad": [c['living_risk'] / 100.0 for c in comps_list],
            })

            smin, smax = float(df["score"].min()), float(df["score"].max())
            good["score_good"] = (
                ((df["score"] - smin) / (smax - smin)).astype(float).reset_index(drop=True)
                if smax > smin else 0.5
            )
            self.good_meta = good

            # Apply to view
            self.model.set_df(self.df_ranked)
            try:
                self.table.resizeColumnsToContents()
            except Exception:
                pass

            try:
                self.table.verticalHeader().setDefaultSectionSize(44)
            except Exception:
                pass

            # UI kolon indeksleri model'e göre belirlenmeli (df_ranked ile birebir aynı sıra olmayabilir)
            col_map = self._get_view_col_map()
            if "Detay" in col_map:
                c_det = col_map["Detay"]
                try:
                    from PyQt6.QtWidgets import QHeaderView
                    hh = self.table.horizontalHeader()
                    hh.setSectionResizeMode(c_det, QHeaderView.ResizeMode.Fixed)
                except Exception:
                    pass
                self.table.setColumnWidth(c_det, 96)

            def goodness_provider(row: int, key: str):
                if self.good_meta is None or self.good_meta.empty:
                    return None
                try:
                    return float(self.good_meta.iloc[row][key])
                except Exception:
                    return None

            # Delegates (best-effort)
            try:
                apply_ranking_delegates(self.table, col_map, goodness_provider, theme=self.theme)
            except Exception:
                logging.exception("apply_ranking_delegates failed")

            # Detail buttons + initial col vis
            self._install_detail_buttons()
            self._apply_initial_column_visibility()

            # KPIs
            self._update_kpis()

            # Select first row
            if len(self.df_ranked) > 0:
                try:
                    self.table.selectRow(0)
                except Exception:
                    pass
                if self.drawer.isVisible():
                    self.show_details_drawer(0)
                else:
                    self._show_details(0)

            self.statusBar().showMessage(f"Ranked {len(self.df_ranked)} universities")

        except Exception as e:
            logging.exception("recompute failed")
            try:
                QMessageBox.warning(self, "Error", f"Error during computation:\n\n{e}")
            except Exception:
                pass
            self.statusBar().showMessage("Computation error")

    # -----------------------------------------------------------------
    # Details wiring
    # -----------------------------------------------------------------
    def _apply_initial_column_visibility(self) -> None:
        if getattr(self, "_colvis_initialized", False):
            return
        if self.df_ranked is None or self.df_ranked.empty:
            return

        hide_by_default = {
            "Kaynak JSON",
            "Güçlü tarafı",
            "Avantaj",
            "Dezavantaj",
            "Güçlü alanlar",
            "Tuition (€/yr)",  # istersen kapalı gelsin
        }
        col_map = {name: i for i, name in enumerate(self.df_ranked.columns)}
        for name in hide_by_default:
            if name in col_map:
                try:
                    self.table.setColumnHidden(col_map[name], True)
                except Exception:
                    pass

        self._colvis_initialized = True

    
    def _get_view_col_map(self) -> Dict[str, int]:
        """QTableView üzerindeki *model kolon indekslerini* döndürür (header text -> index).
        Not: df_ranked kolon sırası ile model kolon sırası farklı olabilir; UI işlemleri model'e göre yapılmalı.
        """
        m = self.model
        cols: Dict[str, int] = {}
        try:
            n = int(m.columnCount())
        except Exception:
            n = 0
        for i in range(n):
            try:
                name = m.headerData(i, Qt.Orientation.Horizontal, Qt.ItemDataRole.DisplayRole)
                if name is None:
                    continue
                cols[str(name)] = i
            except Exception:
                continue
        return cols

    def _install_detail_buttons(self) -> None:
        # Not: Detay butonunu *model kolon indeksine* göre yerleştiriyoruz.
        # df_ranked kolon sırası modelin tercih ettiği sıradan farklı olabilir.
        if self.df_ranked is None or self.df_ranked.empty:
            return
        col_map = self._get_view_col_map()
        if "Detay" not in col_map:
            return
        c = col_map["Detay"]

        try:
            row_count = int(self.model.rowCount())
        except Exception:
            row_count = len(self.df_ranked)

        # Clear old widgets
        for rr in range(row_count):
            idx = self.model.index(rr, c)
            old = self.table.indexWidget(idx)
            if old is not None:
                try:
                    old.deleteLater()
                except Exception:
                    pass
                self.table.setIndexWidget(idx, None)

        for r in range(row_count):
            idx = self.model.index(r, c)
            btn = DetailHoverButton(row=r, parent=self.table)
            btn.clicked.connect(lambda _=False, rr=r: self.show_details_drawer(rr, force=True))

            def _on_enter(rr: int):
                self._hovering_detail_button = True
                self.show_details_drawer(rr, force=False)

            def _on_leave():
                self._hovering_detail_button = False
                self._schedule_hide_drawer()

            # widgets.DetailHoverButton uses hovered/unhovered signals; older variants may expose set_hover_handlers()
            if hasattr(btn, "hovered") and hasattr(btn, "unhovered"):
                try:
                    from functools import partial
                    btn.hovered.connect(partial(_on_enter, r))
                    btn.unhovered.connect(_on_leave)
                except Exception:
                    pass
            else:
                try:
                    btn.set_hover_handlers(_on_enter, _on_leave)
                except Exception:
                    pass

            self.table.setIndexWidget(idx, btn)

    def on_row_selected(self, *args) -> None:
        idx = self.table.currentIndex()
        if idx.isValid():
            row = idx.row()
            if self.drawer.isVisible():
                self.show_details_drawer(row)
            else:
                self._show_details(row)

    def _show_details(self, row: int) -> None:
        if self.df_ranked is None or row < 0 or row >= len(self.df_ranked):
            return

        r = self.df_ranked.iloc[row]

        # Extra information
        extra_lines: List[str] = []
        for key in ("Program", "Derece", "Kabul Modu", "Dil", "Burs"):
            if key in self.df_ranked.columns:
                v = str(r.get(key, "") or "").strip()
                if v:
                    extra_lines.append(f"{key}: {v}")

        strength = str(r.get("Güçlü tarafı", "") or "")
        if extra_lines:
            strength = (strength + "\n\n" if strength.strip() else "") + "\n".join(extra_lines)

        # Radar values
        labels = ["Cost & Fund", "Elig & Lang", "Academic", "Career", "Skor"]
        if self.good_meta is not None and 0 <= row < len(self.good_meta):
            g = self.good_meta.iloc[row]
            vals = [
                clamp01(float(g.get("cost_good", 0.5))),
                clamp01(float(g.get("fee_good", 0.5))),
                clamp01(float(g.get("fit_good", 0.5))),
                clamp01(float(g.get("pros_good", 0.5))),
                clamp01(float(g.get("score_good", 0.5))),
            ]
        else:
            vals = [0.5] * 5

        sd = r.get("_scoringDetails", {})
        explanations = "\n".join([f"• {e}" for e in sd.get("explanation", [])])
        warnings_str = "\n".join([f"⚠ {w}" for w in sd.get("warnings", [])])
        if warnings_str:
            explanations += "\n\n" + warnings_str

        strength = str(r.get("Güçlü tarafı", "") or "")
        if explanations:
            strength = f"**Score Explanation:**\n{explanations}\n\n" + strength

        try:
            self.drawer.set_record({
                "university": str(r.get("Üniversite", "Details")),
                "city": str(r.get("Şehir", "-")),
                "score": r.get("Skor", "-"),
                "source": str(r.get("Kaynak JSON", "-")),
                "strength": strength,
                "pros": str(r.get("Avantaj", "")),
                "cons": str(r.get("Dezavantaj", "")),
                "focus": str(r.get("Güçlü alanlar", "")),
                "radar_labels": labels,
                "radar_values": vals,
            })
        except Exception:
            logging.exception("drawer.set_record failed")

    def closeEvent(self, event):
        try:
            logging.info("MainWindow.closeEvent (accepted=%s)", event.isAccepted())
        except Exception:
            pass
        return super().closeEvent(event)


# ===================================================================
# 4.                          Entry Point
# ===================================================================

def _install_debug_hooks() -> None:
    """
    - File + console logging
    - Uncaught exception hook -> log + QMessageBox
    """
    # Root logger: hem dosya hem stdout
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Duplicate handler eklenmesin
    if not getattr(_install_debug_hooks, "_installed", False):
        # File handler
        fh = logging.FileHandler(str(LOG_PATH), mode="a", encoding="utf-8")
        fh.setLevel(logging.INFO)

        # Console handler
        sh = logging.StreamHandler(sys.stdout)
        sh.setLevel(logging.INFO)

        fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
        fh.setFormatter(fmt)
        sh.setFormatter(fmt)

        logger.addHandler(fh)
        logger.addHandler(sh)

        _install_debug_hooks._installed = True  # type: ignore[attr-defined]

    logging.info("=== UniRank Modern Dashboard starting ===")
    logging.info("Python: %s", sys.version.replace("\n", " "))
    logging.info("Platform: %s", sys.platform)
    try:
        logging.info("CWD: %s", os.getcwd())
    except Exception:
        pass
    try:
        logging.info("__file__: %s", Path(__file__).resolve())
    except Exception:
        pass

    def _excepthook(exc_type, exc, tb):
        logging.error("UNCAUGHT EXCEPTION: %s", exc, exc_info=(exc_type, exc, tb))
        try:
            app = QApplication.instance()
            # App yoksa messagebox göstermeye çalışma
            if app is None:
                return
            QMessageBox.critical(
                None,
                "Unexpected Error",
                "".join(traceback.format_exception(exc_type, exc, tb)),
            )
        except Exception:
            # messagebox bile patlarsa sadece log ile yetin
            pass

    sys.excepthook = _excepthook


