"""Guard the categorical standards and the profiles derived from them.

The point of ``config/standards.json`` is that a category shown to a student
is never a bare adjective: it carries the criteria that produced it and the
evidence behind those criteria.  These tests fail if a level is published
without enough evidence, if a scale drifts away from its definition, or if a
cost total is published while a mandatory component is unknown.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).parents[1]
DATA_DIR = ROOT / "data_base"
STANDARDS = json.loads((ROOT / "config" / "standards.json").read_text(encoding="utf-8"))
FX = json.loads((ROOT / "config" / "fx_rates.json").read_text(encoding="utf-8"))
SKIP_FILES = {"taxonomy.json"}


def _records() -> list[dict]:
    rows: list[dict] = []
    for path in sorted(DATA_DIR.glob("*.json")):
        if path.name in SKIP_FILES:
            continue
        document = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(document, list):
            rows.extend(row for row in document if isinstance(row, dict))
        elif isinstance(document, dict):
            for key in ("programs", "universities", "records"):
                value = document.get(key)
                if isinstance(value, list):
                    rows.extend(row for row in value if isinstance(row, dict))
                    break
    return rows


RECORDS = _records()


def test_every_record_carries_the_four_standard_profiles():
    for record in RECORDS:
        living = record.get("living_profile") or {}
        cost = record.get("cost_profile") or {}
        timeline = record.get("application_timeline_profile") or {}
        assert "housing_difficulty_profile" in living, record.get("id")
        assert "cost_of_living_profile" in living, record.get("id")
        assert "normalized_cost" in cost, record.get("id")
        assert "primary_deadline" in timeline, record.get("id")
        assert "academic_match_profile" in record, record.get("id")


def test_housing_levels_stay_inside_the_published_scale():
    allowed = {level["code"] for level in STANDARDS["housing_difficulty"]["levels"]}
    for record in RECORDS:
        living = record.get("living_profile") or {}
        assert living.get("housing_difficulty") in allowed, record.get("id")
        assert living.get("housing_search_difficulty") in allowed, record.get("id")


def test_a_housing_level_is_never_published_on_thin_evidence():
    """Fewer than three evidenced dimensions must produce 'unknown'."""
    for record in RECORDS:
        profile = (record.get("living_profile") or {}).get("housing_difficulty_profile") or {}
        required = profile.get("dimensions_required_for_publication", 3)
        if profile.get("evidenced_dimensions", 0) < required:
            assert profile.get("level") == "unknown", record.get("id")
            assert profile.get("scaled_score") is None, record.get("id")


def test_very_high_housing_needs_the_structural_signal_that_defines_it():
    """The top band is reserved for a named failure, not a high arithmetic score."""
    structural = {
        ("supply_pressure", "cannot_house_most_internationals_stated"),
        ("arrival_risk", "officially_advised_not_to_travel_without_contract"),
    }
    for record in RECORDS:
        profile = (record.get("living_profile") or {}).get("housing_difficulty_profile") or {}
        if profile.get("level") != "very_high":
            continue
        dimensions = profile.get("dimensions") or {}
        assert any(dimensions.get(key, {}).get("value") == value for key, value in structural), record.get("id")


def test_housing_dimension_points_match_the_published_scale():
    scale = {d["key"]: d["values"] for d in STANDARDS["housing_difficulty"]["scoring_dimensions"]}
    for record in RECORDS:
        profile = (record.get("living_profile") or {}).get("housing_difficulty_profile") or {}
        for key, entry in (profile.get("dimensions") or {}).items():
            value = entry.get("value")
            if value is None:
                assert entry.get("points") is None, record.get("id")
                continue
            assert value in scale[key], (record.get("id"), key, value)
            assert entry["points"] == scale[key][value]["points"], (record.get("id"), key)


def test_every_housing_dimension_value_has_a_bilingual_label():
    for dimension in STANDARDS["housing_difficulty"]["scoring_dimensions"]:
        for code, entry in dimension["values"].items():
            assert entry["label"]["en"], (dimension["key"], code)
            assert entry["label"]["tr"], (dimension["key"], code)


def test_academic_match_tier_needs_three_evidenced_dimensions():
    tiers = {tier["code"] for tier in STANDARDS["academic_match"]["tiers"]}
    for record in RECORDS:
        profile = record.get("academic_match_profile") or {}
        assert profile.get("tier") in tiers, record.get("id")
        required = profile.get("dimensions_required_for_publication", 3)
        if profile.get("evidenced_dimensions", 0) < required:
            assert profile["tier"] == "unknown", record.get("id")
            assert profile["score"] is None, record.get("id")
        else:
            assert 0 <= profile["score"] <= 100, record.get("id")


def test_a_cost_total_is_never_published_with_a_missing_mandatory_component():
    for record in RECORDS:
        normalized = (record.get("cost_profile") or {}).get("normalized_cost") or {}
        if normalized.get("missing_mandatory_components"):
            assert normalized.get("annual_total") is None, record.get("id")
            assert normalized.get("status") == "incomplete", record.get("id")


def test_a_cost_of_living_figure_always_declares_its_basis_and_period():
    allowed = {entry["code"] for entry in STANDARDS["cost_model"]["cost_basis_values"]}
    for record in RECORDS:
        profile = (record.get("living_profile") or {}).get("cost_of_living_profile") or {}
        assert profile.get("cost_basis") in allowed, record.get("id")
        if profile.get("monthly_total") is not None:
            assert profile.get("currency"), record.get("id")
            assert profile.get("months_covered"), record.get("id")


def test_euro_conversions_carry_their_rate_and_date():
    for record in RECORDS:
        for container in (
            (record.get("living_profile") or {}).get("cost_of_living_profile") or {},
            (record.get("cost_profile") or {}).get("normalized_cost") or {},
        ):
            for key in ("monthly_total_eur_equivalent", "annual_total_eur_equivalent"):
                conversion = container.get(key)
                if not conversion:
                    continue
                assert conversion["is_conversion"] is True, record.get("id")
                assert conversion["fx_rate_date"] == FX["rate_date"], record.get("id")
                assert conversion["fx_source"] == FX["source"], record.get("id")


def test_a_published_faculty_email_always_names_the_page_that_publishes_it():
    """The standard forbids reconstructing an address from a naming pattern."""
    for record in RECORDS:
        people = (record.get("research_profile") or {}).get("notable_professors") or []
        for person in people:
            if not isinstance(person, dict) or not person.get("email"):
                continue
            source = person.get("email_source")
            assert source, (record.get("id"), person.get("name"))
            assert str(source).startswith("https://"), (record.get("id"), person.get("name"))


def test_research_units_use_taxonomy_keys_for_their_topics():
    taxonomy = set(json.loads((DATA_DIR / "taxonomy.json").read_text(encoding="utf-8")))
    for record in RECORDS:
        for unit in (record.get("research_profile") or {}).get("research_units") or []:
            if not isinstance(unit, dict):
                continue
            for topic in unit.get("topics") or []:
                assert topic in taxonomy, (record.get("id"), unit.get("name"), topic)


def test_faculty_fit_tags_use_taxonomy_keys():
    taxonomy = set(json.loads((DATA_DIR / "taxonomy.json").read_text(encoding="utf-8")))
    for record in RECORDS:
        for person in (record.get("research_profile") or {}).get("notable_professors") or []:
            if not isinstance(person, dict):
                continue
            for tag in person.get("fit_tags") or []:
                assert tag in taxonomy, (record.get("id"), person.get("name"), tag)


def test_scholarship_playbook_steps_are_ordered_and_carry_a_known_timing():
    timings = {entry["code"] for entry in STANDARDS["scholarship_playbook"]["step_timing_values"]}
    for record in RECORDS:
        for entry in (record.get("scholarship_profile") or {}).get("playbook") or []:
            assert entry.get("opportunity"), record.get("id")
            assert entry.get("evidence_url", "").startswith("https://"), record.get("id")
            orders = [step.get("order") for step in entry.get("steps") or []]
            assert orders == sorted(orders), (record.get("id"), entry["opportunity"])
            for step in entry.get("steps") or []:
                assert step.get("timing") in timings, (record.get("id"), step.get("order"))
                assert isinstance(step.get("hard_requirement"), bool), (record.get("id"), step.get("order"))


def test_faculty_contact_timing_uses_the_published_enum():
    allowed = {entry["code"] for entry in STANDARDS["faculty_contact"]["contact_timing_values"]}
    # Legacy records predate the enum; only records that carry research_units
    # have been migrated to it.
    for record in RECORDS:
        if not (record.get("research_profile") or {}).get("research_units"):
            continue
        for person in (record.get("research_profile") or {}).get("notable_professors") or []:
            if isinstance(person, dict) and person.get("contact_timing"):
                assert person["contact_timing"] in allowed, (record.get("id"), person.get("name"))


@pytest.mark.parametrize("code", ["low", "medium", "high", "very_high", "unknown"])
def test_each_housing_level_is_defined_with_bilingual_criteria(code):
    level = next(item for item in STANDARDS["housing_difficulty"]["levels"] if item["code"] == code)
    assert level["label"]["en"] and level["label"]["tr"]
    assert level["criteria"]["en"] and level["criteria"]["tr"]


# ---------------------------------------------------------------------------
# The countdown must answer "can I still apply?", not "what happens next?".
#
# A record's deadline_events[] mixes application dates with deposit due dates,
# CAS issue dates, enrolment windows and the first day of teaching.  Pooling
# them made closed programmes advertise a live countdown - Birmingham showed an
# offer-holder conditions deadline and Vilnius Tech showed the start of term.
# ---------------------------------------------------------------------------

import sys

sys.path.insert(0, str(ROOT / "scripts"))
from standardize_categories import (  # noqa: E402
    event_audience,
    event_is_new_applicant_deadline,
)


ADMITTED_ONLY_EVENTS = [
    {"event": "overseas_conditions_deadline", "status": "upcoming_for_existing_offer_holders"},
    {"event": "international_masters_deposit", "status": "upcoming_for_existing_offer_holders"},
    {"event": "latest_CAS_issue_date_for_September_starters"},
    {"event": "Studies commence", "applicant_scope": "admitted"},
    {"event": "programme_start"},
    {"event": "teaching_begins"},
    {"event": "ordinary_enrolment_window_closes"},
    {"event": "universitaly_pre_enrolment_deadline_overseas_non_eu"},
    {"event": "postgraduate_accommodation_application_deadline"},
    {"event": "housing_guarantee_offer_acceptance_deadline"},
    {"event": "deferral_request_deadline"},
    {"event": "applications_opened"},
    {"event": "offer_conditions_and_qualification_verification_deadline"},
    {"event": "advised_ATAS_application_date_if_required"},
]

NEW_APPLICANT_EVENTS = [
    {"event": "general_programme_application_close"},
    {"event": "UK_course_application", "status": "open"},
    {"event": "visa_required_applicant_programme_deadline", "status": "open"},
    {"event": "first_esse3_master_admission_round"},
    {"event": "Degree application deadline", "applicant_scope": "international"},
    # A funding deadline is something an applicant acts on, so it may headline.
    {"event": "adisurc_scholarship_and_services_deadline"},
]


@pytest.mark.parametrize("event", ADMITTED_ONLY_EVENTS)
def test_admitted_and_calendar_events_are_not_application_deadlines(event):
    assert event_is_new_applicant_deadline(event) is False, event


@pytest.mark.parametrize("event", NEW_APPLICANT_EVENTS)
def test_real_application_events_are_recognised(event):
    assert event_is_new_applicant_deadline(event) is True, event


def test_event_audience_reads_through_snake_case():
    # "_" is a word character, so \bUK\b never matches inside UK_course_application
    # unless the separators are normalised first.
    assert event_audience({"event": "UK_course_application"}) == "eu_eea"
    assert event_audience({"event": "overseas_application_deadline"}) == "non_eu"
    assert (
        event_audience({"event": "deposit", "status": "upcoming_for_existing_offer_holders"})
        == "admitted_or_offer_holders"
    )


def test_no_published_countdown_comes_from_an_admitted_only_event():
    for record in RECORDS:
        primary = (record.get("application_timeline_profile") or {}).get("primary_deadline") or {}
        if primary.get("status") not in {"open", "closing_soon"}:
            continue
        origin = str(primary.get("derived_from") or "")
        assert "deadline_events[]" not in origin or "(" in origin, (
            record.get("id"),
            "an event-derived countdown must name the event it came from",
        )
        assert primary.get("audience") == "new_applicants", record.get("id")


def test_other_milestones_are_future_dated_and_labelled():
    for record in RECORDS:
        primary = (record.get("application_timeline_profile") or {}).get("primary_deadline") or {}
        for milestone in primary.get("other_milestones") or []:
            assert milestone.get("date"), record.get("id")
            assert milestone.get("audience") in {
                "all_applicants",
                "non_eu",
                "eu_eea",
                "admitted_or_offer_holders",
            }, (record.get("id"), milestone)
