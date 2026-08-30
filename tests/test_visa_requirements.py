"""Guard the permit, funds and clearance layer.

This layer answers questions the tool previously could not answer at all, which
means every one of them sent the reader to a search engine at the point where a
wrong answer costs an application cycle.  That makes an invented value here
worse than an absent one: "nothing required" and "not checked yet" look the same
to a reader, but only one of them is honest.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).parents[1]
VISA = json.loads((ROOT / "config" / "visa_requirements.json").read_text(encoding="utf-8"))
COUNTRIES = VISA["countries"]
VALID_STATUSES = {"verified", "needs_research", "not_applicable"}


def _bilingual(value) -> bool:
    return isinstance(value, dict) and bool(value.get("en")) and bool(value.get("tr"))


def test_the_layer_states_whose_nationality_it_is_written_for():
    # These rules change more with the passport than with anything else, so a
    # file that does not name the nationality is a trap.
    assert VISA["applicant_profile"]["nationality"] == "Turkey"
    assert _bilingual(VISA["applicant_profile"]["note"])


def test_every_country_declares_a_known_status():
    for name, entry in COUNTRIES.items():
        assert entry.get("status") in VALID_STATUSES, (name, entry.get("status"))


def test_unverified_countries_carry_no_figures():
    # The whole point of the status is that an unresearched country cannot
    # quietly present a number as if it had been checked.
    for name, entry in COUNTRIES.items():
        if entry.get("status") == "verified":
            continue
        assert "financial_requirement" not in entry, name
        assert "documents" not in entry, name
        assert entry.get("last_verified") in (None, "2026-08-30"), name


def test_verified_countries_carry_sources_for_what_they_claim():
    for name, entry in COUNTRIES.items():
        if entry.get("status") != "verified":
            continue
        sources = entry.get("sources") or []
        assert sources, name
        covered = {field for source in sources for field in source.get("relevant_fields", [])}
        for claim in ("financial_requirement", "special_clearance", "documents"):
            if claim in entry:
                assert claim in covered, (name, claim)
        assert entry.get("last_verified"), name


def test_every_source_is_https_and_dated():
    for name, entry in COUNTRIES.items():
        for source in entry.get("sources") or []:
            assert str(source.get("url", "")).startswith("https://"), (name, source.get("url"))
            assert source.get("last_checked"), (name, source.get("url"))


def test_reader_facing_prose_is_bilingual():
    for name, entry in COUNTRIES.items():
        for key in ("permit_name", "known_shape", "note", "blocked_source_note"):
            if key in entry:
                assert _bilingual(entry[key]), (name, key)
        financial = entry.get("financial_requirement") or {}
        for key in ("plus_course_fees", "holding_period", "turkish_citizen_note"):
            if key in financial:
                assert _bilingual(financial[key]), (name, key)
        for item in entry.get("documents") or []:
            assert _bilingual(item), name


def test_the_uk_entry_keeps_the_two_facts_that_decide_the_timeline():
    # Türkiye is on neither the differential-evidence list nor the ATAS
    # exemption list. Both were verified from gov.uk, and both change what a
    # Turkish applicant has to do relative to an exempt classmate.
    uk = COUNTRIES["United Kingdom"]
    assert uk["financial_requirement"]["applies_to_turkish_citizens"] is True
    assert uk["special_clearance"]["required_for_turkish_citizens"] is True
    amounts = {entry["scope"]: entry["amount_gbp_per_month"] for entry in uk["financial_requirement"]["amounts"]}
    assert amounts["Courses in London"] == 1529
    assert amounts["Courses outside London"] == 1171


def test_every_database_country_has_an_entry():
    # A country in the catalogue with no entry renders no panel at all, which
    # reads as "no permit needed".
    import glob

    seen = set()
    for path in sorted(glob.glob(str(ROOT / "data_base" / "*.json"))):
        if path.endswith("taxonomy.json"):
            continue
        document = json.loads(Path(path).read_text(encoding="utf-8"))
        rows = document if isinstance(document, list) else (
            document.get("programs") or document.get("universities") or document.get("records") or []
        )
        for row in rows:
            if isinstance(row, dict) and isinstance(row.get("country"), str) and row["country"].strip():
                seen.add(row["country"].strip())
    missing = sorted(seen - set(COUNTRIES))
    assert not missing, f"countries in the database with no visa entry: {missing}"
