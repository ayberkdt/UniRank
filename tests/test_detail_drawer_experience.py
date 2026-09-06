from pathlib import Path


ROOT = Path(__file__).parents[1]


def test_drawer_keeps_university_identity_visible():
    html = (ROOT / "public" / "index.html").read_text(encoding="utf-8")
    script = (ROOT / "public" / "script.js").read_text(encoding="utf-8")

    assert 'id="drawer-program-title"' in html
    assert "els.drawer.title.textContent" in script
    assert "els.drawer.programTitle.textContent" in script
    assert 'class="drawer-decision-hero__university"' in script


def test_decision_profile_is_live_and_uses_the_full_scoring_scale():
    html = (ROOT / "public" / "index.html").read_text(encoding="utf-8")
    script = (ROOT / "public" / "script.js").read_text(encoding="utf-8")

    assert '<canvas id="radarChart"' not in html
    assert 'class="drawer-fit-overview"' in script
    assert "decisionMetrics(data._scoringDetails?.components || {}, isTurkish)" in script
    assert "data: metrics.map(metric => metric.value)" in script
    assert "pointBackgroundColor: metrics.map(metric => metric.color)" in script
    assert "max: 100" in script
    assert "context.raw).toFixed(0)} / 100" in script


def test_long_form_detail_uses_progressive_disclosure():
    script = (ROOT / "public" / "script.js").read_text(encoding="utf-8")

    assert '<details class="drawer-priority-group' in script
    assert "applicationGroup" in script
    assert "academicGroup" in script
    assert "financeGroup" in script
    assert "evidenceGroup" in script
    assert "applicationFeeHTML + admissionsHTML + timelineHTML" in script


def test_homepage_uses_optimized_local_hero_art():
    html = (ROOT / "public" / "index.html").read_text(encoding="utf-8")
    styles = (ROOT / "public" / "redesign.css").read_text(encoding="utf-8")
    translations = (ROOT / "public" / "i18n.js").read_text(encoding="utf-8")
    asset = ROOT / "public" / "assets" / "unirank-orbital-hero.webp"

    assert asset.is_file()
    assert asset.stat().st_size < 100_000
    assert 'url("assets/unirank-orbital-hero.webp")' in styles
    assert 'class="hero-proof"' in html
    assert 'class="header-actions__intro"' in html
    assert ".header-actions__intro" in styles
    assert translations.count("hero_proof_sources:") == 2


def test_homepage_defers_heavy_optional_visual_libraries():
    html = (ROOT / "public" / "index.html").read_text(encoding="utf-8")
    script = (ROOT / "public" / "script.js").read_text(encoding="utf-8")

    head = html.split("</head>", 1)[0]
    assert "leaflet.js" not in head
    assert "leaflet.markercluster.js" not in head
    assert "chart.js" not in head
    assert 'media="print" onload="this.media=\'all\'"' in head
    assert "function ensureMapAssets()" in script
    assert "function ensureChartLibrary()" in script
    assert "ensureChartLibrary()" in script


def test_flags_do_not_depend_on_a_remote_image_service():
    country_visual = (ROOT / "public" / "countryVisual.js").read_text(encoding="utf-8")
    script = (ROOT / "public" / "script.js").read_text(encoding="utf-8")

    assert "flagcdn.com" not in country_visual
    assert "flagcdn.com" not in script
    for country in ("czechia", "greece", "norway", "portugal", "turkey", "united_kingdom", "usa"):
        assert f"{country}:" in country_visual

    for code in ("cn", "cz", "gr", "no", "pt", "kr", "tr", "gb", "us"):
        assert (ROOT / "public" / "assets" / "flags" / f"{code}.png").is_file()
        assert f'/assets/flags/{code}.png' in country_visual


def test_results_show_immediate_feedback_and_one_dominant_action():
    script = (ROOT / "public" / "script.js").read_text(encoding="utf-8")
    styles = (ROOT / "public" / "redesign.css").read_text(encoding="utf-8")

    assert "function showLoadingCards()" in script
    assert "program-card--skeleton" in script
    assert "els.tableBody.setAttribute('aria-busy', 'true')" in script
    assert ".program-card__actions .detail-btn" in styles
    assert "background: var(--ui-accent);" in styles


def test_catalogue_progressively_paints_before_full_hydration():
    html = (ROOT / "public" / "index.html").read_text(encoding="utf-8")
    script = (ROOT / "public" / "script.js").read_text(encoding="utf-8")
    server = (ROOT / "scripts" / "devServer.mjs").read_text(encoding="utf-8")

    assert 'id="catalog-progress"' in html
    assert "INITIAL_CATALOG_PAGE_SIZE = 8" in script
    assert "CATALOG_PAGE_SIZE = 60" in script
    assert "await publishUniversityBatch(json.data" in script
    assert "hydrateCatalogInBackground" in script
    assert "waitForBrowserIdle" in script
    assert "pendingRecords.push(...pageJson.data)" in script
    assert "visibleResultLimit" in script
    assert "filteredData.slice(0, visibleResultLimit)" in script
    assert "?offset=${offset}&limit=${CATALOG_PAGE_SIZE}" in script
    assert "let programsPromise = null" in server
    assert "paginatePrograms(records, url)" in server
    assert "max-age=31536000, immutable" in server
    assert "loadPrograms().catch" in server

    taxonomy = (ROOT / "public" / "taxonomy.js").read_text(encoding="utf-8")
    assert "let taxonomyPromise = null" in taxonomy
    assert "if (!taxonomyPromise)" in taxonomy


def test_sidebar_toggle_is_attached_and_cards_use_a_compact_footer():
    html = (ROOT / "public" / "index.html").read_text(encoding="utf-8")
    script = (ROOT / "public" / "script.js").read_text(encoding="utf-8")
    styles = (ROOT / "public" / "redesign.css").read_text(encoding="utf-8")

    assert 'class="sidebar-edge-toggle"' in html
    assert "setRailCollapsed(!document.body.classList.contains('rail-collapsed'))" in script
    assert 'class="program-card__footer"' in script
    assert ".program-card__footer .program-card__actions" in styles
    assert "contain-intrinsic-block-size: 250px" in styles
