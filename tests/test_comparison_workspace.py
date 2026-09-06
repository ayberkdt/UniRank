from pathlib import Path


ROOT = Path(__file__).parents[1]


def test_comparison_workspace_has_accessible_dialog_contract():
    html = (ROOT / "public" / "index.html").read_text(encoding="utf-8")

    assert 'id="comparison-overlay"' in html
    assert 'id="comparison-workspace"' in html
    assert 'role="dialog"' in html
    assert 'aria-modal="true"' in html
    assert 'aria-labelledby="comparison-title"' in html
    assert 'id="comparison-close"' in html


def test_comparison_selection_is_bounded_persistent_and_card_driven():
    script = (ROOT / "public" / "script.js").read_text(encoding="utf-8")

    assert "readArray('unirank_comparison').slice(0, 3)" in script
    assert "comparisonIds.size >= 3" in script
    assert "writeJSON('unirank_comparison'" in script
    assert 'class="compare-button${isCompared' in script
    assert 'aria-pressed="${String(isCompared)}"' in script
    assert "comparisonIds.size < 2" in script


def test_comparison_actions_are_bilingual():
    translations = (ROOT / "public" / "i18n.js").read_text(encoding="utf-8")

    for key in (
        "compare_add",
        "compare_remove",
        "compare_open",
        "compare_title",
        "compare_funding",
        "compare_research",
    ):
        assert translations.count(f"{key}:") == 2


def test_programme_cards_keep_horizontal_country_identity():
    script = (ROOT / "public" / "script.js").read_text(encoding="utf-8")
    styles = (ROOT / "public" / "redesign.css").read_text(encoding="utf-8")

    assert '<div class="country-card__flag" aria-hidden="true"></div>' in script
    assert ".country-card__flag {" in styles
    assert "background: var(--country-flag);" in styles
    assert ".results-grid { grid-template-columns: repeat(2" not in styles
