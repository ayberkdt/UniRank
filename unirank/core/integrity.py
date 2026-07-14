"""Source-aware quality gates for the UniRank research database.

The database intentionally keeps candidate programmes whose research is not
complete.  This module makes that uncertainty machine-readable: unsupported
high-stakes values are never surfaced as decision facts and every response
contains the reasons a student should verify a record further.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Iterable


CHECKED_ACCESS = {"ok", "redirects", "pdf"}
OFFICIAL_SOURCE_TYPES = {
    "official_program_page",
    "official_admission_page",
    "official_curriculum_page",
    "official_tuition_page",
    "official_scholarship_page",
    "official_department_page",
    "official_lab_page",
    "official_housing_page",
    "official_visa_or_government_page",
    "official_industry_partner_page",
    "official_university_policy_page",
    "official_cost_of_living_page",
}

# A source type can support a field even when the older source log did not
# include ``relevant_fields``.  It may *not* support unrelated fields.
FIELD_SOURCE_TYPES = {
    "program": {"official_program_page", "official_admission_page"},
    "language": {"official_program_page", "official_admission_page", "official_university_policy_page"},
    "admission": {"official_admission_page", "official_program_page"},
    "non_eu_eligibility": {"official_admission_page", "official_visa_or_government_page"},
    "tuition": {"official_tuition_page"},
    "scholarship": {"official_scholarship_page"},
    "deadline": {"official_admission_page", "official_program_page"},
    "curriculum": {"official_curriculum_page", "official_program_page"},
    "research": {"official_department_page", "official_lab_page"},
    "industry": {"official_industry_partner_page"},
    # An official cost-of-attendance/financial-aid page can directly publish a
    # housing allowance.  It is valid evidence for that budget figure, but
    # must not be mistaken for a rent quote or an availability guarantee.
    "housing": {"official_housing_page", "official_visa_or_government_page", "official_tuition_page", "official_cost_of_living_page"},
}

FIELD_ALIASES = {
    "program": {"program", "program_basic_info", "basic_info", "status"},
    "language": {"language", "teaching_language"},
    "admission": {"admission", "admission_requirements"},
    "non_eu_eligibility": {"non_eu", "non_eu_eligibility", "eligibility"},
    "tuition": {"tuition", "fees", "cost"},
    "scholarship": {"scholarship", "funding"},
    "deadline": {"deadline", "deadlines", "application_timeline"},
    "curriculum": {"curriculum", "study_plan", "courses"},
    "research": {"research", "research_profile", "labs", "department"},
    "industry": {"industry", "industry_ecosystem", "partnership"},
    "housing": {"housing", "living", "living_profile"},
}


def _normalise(value: Any) -> str:
    return str(value or "").strip().lower()


def _source_log(record: dict[str, Any]) -> list[dict[str, Any]]:
    profile = record.get("source_profile") or {}
    candidates = profile.get("source_log") or record.get("Meta_Sources") or record.get("sources") or []
    if not isinstance(candidates, list):
        candidates = [candidates]
    return [source for source in candidates if isinstance(source, dict)]


def _is_checked_official(source: dict[str, Any]) -> bool:
    return (
        _normalise(source.get("source_type")) in OFFICIAL_SOURCE_TYPES
        and _normalise(source.get("access_status")) in CHECKED_ACCESS
        and str(source.get("url") or "").startswith(("https://", "http://"))
    )


def has_checked_source(record: dict[str, Any], field: str) -> bool:
    """Return true only for an accessible official source relevant to ``field``."""
    allowed_types = FIELD_SOURCE_TYPES[field]
    aliases = FIELD_ALIASES[field]
    for source in _source_log(record):
        if not _is_checked_official(source):
            continue
        source_type = _normalise(source.get("source_type"))
        if source_type not in allowed_types:
            continue
        relevant = {_normalise(item) for item in (source.get("relevant_fields") or [])}
        # Older records frequently have a correctly typed source but an empty
        # relevant_fields list.  The type is sufficiently direct in that case.
        if not relevant or relevant.intersection(aliases):
            return True
    return False


def evidence_summary(record: dict[str, Any]) -> dict[str, Any]:
    checked_sources = [source for source in _source_log(record) if _is_checked_official(source)]
    verified_fields = [field for field in FIELD_SOURCE_TYPES if has_checked_source(record, field)]
    required = ["program", "language", "tuition", "scholarship", "curriculum", "admission"]
    missing = [field for field in required if field not in verified_fields]
    confidence = record.get("source_profile", {}).get("field_confidence", {})
    confidence_keys = {
        "program": "program_basic_info",
        "language": "language",
        "tuition": "tuition",
        "scholarship": "scholarship",
        "curriculum": "curriculum",
        "admission": "admission",
    }
    has_non_high_critical_confidence = any(
        confidence_keys[field] in confidence and _normalise(confidence.get(confidence_keys[field])) != "high"
        for field in required
        if field in verified_fields
    )
    status = "verified" if not missing and not has_non_high_critical_confidence else ("partial" if verified_fields else "needs_verification")
    return {
        "status": status,
        "checked_official_source_count": len(checked_sources),
        "verified_fields": verified_fields,
        "unverified_critical_fields": missing,
        "has_checked_source_log": bool(checked_sources),
    }


def _clear_unverified_values(record: dict[str, Any], quality: dict[str, Any]) -> None:
    """Remove only high-stakes *decision values* without checked evidence.

    Programme names remain as discoverable candidates.  The data that can make
    a student spend money or miss a deadline is removed until researchers add a
    checked official source.
    """
    profiles = {
        "language": record.get("language_profile") or {},
        "cost": record.get("cost_profile") or {},
        "scholarship": record.get("scholarship_profile") or {},
        "timeline": record.get("application_timeline_profile") or {},
        "eligibility": record.get("eligibility_profile") or {},
        "living": record.get("living_profile") or {},
    }

    if "language" not in quality["verified_fields"]:
        record["teaching_language"] = ["Unknown"]
        profiles["language"]["teaching_language"] = ["Unknown"]
        profiles["language"]["language_risk"] = "unknown"

    if "non_eu_eligibility" not in quality["verified_fields"]:
        profiles["eligibility"]["eligible_for_non_eu"] = None

    if "tuition" not in quality["verified_fields"]:
        for key in (
            "tuition_eur_per_year_estimated",
            "tuition_eur_per_year_min",
            "tuition_eur_per_year_max",
            "total_academic_cost_eur_per_year_estimated",
            "regional_tax_eur",
            "student_contribution_eur",
            "enrollment_fee_eur",
            "tuition_usd_per_year",
            "tuition_usd_per_year_at_three_quarters",
            "tuition_usd_per_quarter",
            "tuition_usd_per_quarter_nonresident_full_time",
            "tuition_gbp_per_year",
            "tuition_chf_per_year",
            "tuition_sek_per_year",
            "tuition_dkk_per_year",
            "mandatory_fees_usd_per_year",
            "total_cost_of_attendance_usd_per_year",
        ):
            profiles["cost"][key] = None
        record["tuition_eur_per_year"] = None
        record["annual_fee_eur"] = None

    if "scholarship" not in quality["verified_fields"]:
        for key in (
            "regional_scholarship_available",
            "regional_scholarship_name",
            "non_eu_eligible",
            "scholarship_deadline",
            "funding_notes",
        ):
            profiles["scholarship"][key] = None

    if "deadline" not in quality["verified_fields"]:
        for key in ("non_eu_deadline", "winter_deadline", "application_deadline", "deadline_notes"):
            profiles["timeline"][key] = None

    if "housing" not in quality["verified_fields"]:
        for key in (
            "average_room_rent_eur",
            "average_room_rent_eur_min",
            "average_room_rent_eur_max",
            "monthly_living_cost_eur_min",
            "monthly_living_cost_eur_max",
            "monthly_living_cost_eur_estimated",
            "living_cost_eur_per_month",
            "housing_difficulty",
            "housing_notes",
            "average_room_rent_usd_per_month_min",
            "average_room_rent_usd_per_month_max",
            "average_room_rent_gbp_per_month_min",
            "average_room_rent_gbp_per_month_max",
            "average_room_rent_chf_per_month_min",
            "average_room_rent_chf_per_month_max",
            "average_room_rent_sek_per_month_min",
            "average_room_rent_sek_per_month_max",
            "average_room_rent_dkk_per_month_min",
            "average_room_rent_dkk_per_month_max",
            "monthly_housing_rent_usd_per_month_min",
            "monthly_housing_rent_usd_per_month_max",
            "monthly_housing_rent_gbp_per_month_min",
            "monthly_housing_rent_gbp_per_month_max",
            "monthly_housing_rent_chf_per_month_min",
            "monthly_housing_rent_chf_per_month_max",
            "monthly_housing_rent_sek_per_month_min",
            "monthly_housing_rent_sek_per_month_max",
            "monthly_housing_rent_dkk_per_month_min",
            "monthly_housing_rent_dkk_per_month_max",
            "housing_budget_usd_per_year",
            "housing_budget_usd_per_year_min",
            "housing_budget_usd_per_year_max",
            "housing_budget_gbp_per_year",
            "housing_budget_gbp_per_year_min",
            "housing_budget_gbp_per_year_max",
            "housing_budget_chf_per_year",
            "housing_budget_chf_per_year_min",
            "housing_budget_chf_per_year_max",
            "housing_budget_sek_per_year",
            "housing_budget_sek_per_year_min",
            "housing_budget_sek_per_year_max",
            "housing_budget_dkk_per_year",
            "housing_budget_dkk_per_year_min",
            "housing_budget_dkk_per_year_max",
            "official_student_housing_budget_sek_per_month_examples",
            "official_student_total_budget_sek_per_month_examples",
        ):
            profiles["living"][key] = None
        for key in (
            "living_cost_usd_per_year_i20",
            "living_cost_usd_per_year",
            "living_cost_usd_per_year_min",
            "living_cost_usd_per_year_max",
            "living_cost_gbp_per_year",
            "living_cost_gbp_per_year_min",
            "living_cost_gbp_per_year_max",
            "living_cost_chf_per_year",
            "living_cost_chf_per_year_min",
            "living_cost_chf_per_year_max",
            "living_cost_sek_per_year",
            "living_cost_sek_per_year_min",
            "living_cost_sek_per_year_max",
            "living_cost_dkk_per_year",
            "living_cost_dkk_per_year_min",
            "living_cost_dkk_per_year_max",
        ):
            profiles["cost"][key] = None
        # Older imports sometimes stored an unsourced city-wide rent estimate
        # beside the actual programme record.  Keep the city name, but never
        # let this legacy estimate leak into a programme card or score.
        city = record.get("city")
        if isinstance(city, dict):
            city["estimated_housing_cost_eur"] = None
            city["housing_difficulty"] = None

    record["language_profile"] = profiles["language"]
    record["cost_profile"] = profiles["cost"]
    record["scholarship_profile"] = profiles["scholarship"]
    record["application_timeline_profile"] = profiles["timeline"]
    record["eligibility_profile"] = profiles["eligibility"]
    record["living_profile"] = profiles["living"]
    # Legacy imports sometimes stored unsourced city-wide housing claims next
    # to a programme.  They have no programme-level provenance, so retain the
    # city name but remove the decision values even if another housing budget
    # on the record is source-checked.
    city = record.get("city")
    if isinstance(city, dict):
        city["estimated_housing_cost_eur"] = None
        city["housing_difficulty"] = None


def apply_integrity_gate(record: dict[str, Any], *, strip_unverified: bool = True) -> dict[str, Any]:
    """Return a non-mutating, source-safe record with a quality profile.

    Sentiment scores are also withheld unless the record documents at least
    three independent observations, a date range, and one cited sentiment
    source.  This prevents decorative but unsupported 0–100 scores.
    """
    gated = deepcopy(record)
    quality = evidence_summary(gated)
    sentiment = gated.get("student_sentiment_profile") or {}
    sources = sentiment.get("student_sentiment_sources") or []
    sample_size = sentiment.get("sample_size_estimate")
    has_adequate_sentiment = (
        isinstance(sources, list)
        and len(sources) >= 1
        and isinstance(sample_size, (int, float))
        and sample_size >= 3
        and bool(sentiment.get("date_range"))
    )
    if sentiment.get("student_satisfaction_score") is not None and not has_adequate_sentiment:
        sentiment["student_satisfaction_score"] = None
        sentiment["sentiment_confidence"] = "unknown"
        sentiment["verification_notes"] = {
            "en": "Score hidden: the record does not document a sufficient, dated sentiment sample.",
            "tr": "Puan gizlendi: kayıtta yeterli ve tarihli bir öğrenci görüşü örneklemi belgelenmemiş.",
        }
    gated["student_sentiment_profile"] = sentiment

    source_profile = gated.setdefault("source_profile", {})
    # A confidence label must never remain "high" after the evidence audit has
    # found no checked official source for that field.  Keeping it would make a
    # raw export look more certain than the public decision card.
    confidence = source_profile.setdefault("field_confidence", {})
    confidence_keys = {
        "program": "program_basic_info",
        "language": "language",
        "admission": "admission",
        "tuition": "tuition",
        "scholarship": "scholarship",
        "curriculum": "curriculum",
        "deadline": "deadlines",
        "housing": "housing",
    }
    for field in quality["unverified_critical_fields"]:
        key = confidence_keys.get(field)
        if key:
            confidence[key] = "unknown"
    source_profile["needs_verification"] = quality["status"] != "verified"
    gated["data_quality"] = quality
    if strip_unverified:
        _clear_unverified_values(gated, quality)
    return gated


def audit_record(record: dict[str, Any]) -> dict[str, Any]:
    """Return the data-quality block without changing a record."""
    return evidence_summary(record)
