"""Report record-level information that would make a student search elsewhere.

This is deliberately stricter than the integrity gate: a checked source alone
is not counted as complete when the decision card still has no usable value for
tuition, funding, curriculum, admissions, timeline, or living costs.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from unirank.core.integrity import audit_record


TARGET_FILES = (
    "almanya.json", "austria.json", "belcika.json", "danimarka.json",
    "fransa.json", "hollanda.json", "ingiltere.json", "isvec.json",
    "isvicre.json", "italy.json", "italya.json", "ispanya.json",
    "portekiz.json", "polonya.json", "finlandiya.json", "cekya.json",
    "yunanistan.json", "turkiye.json", "amerika.json",
)


def records(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [row for row in payload if isinstance(row, dict)]
    if isinstance(payload, dict):
        for key in ("programs", "universities"):
            if isinstance(payload.get(key), list):
                return [row for row in payload[key] if isinstance(row, dict)]
    return []


def present(value: Any) -> bool:
    if value is None or value == "":
        return False
    if isinstance(value, str) and value.strip().lower() in {"unknown", "needs_verification", "-", "—"}:
        return False
    if isinstance(value, (list, dict, tuple, set)):
        return bool(value)
    return True


def any_present(*values: Any) -> bool:
    return any(present(value) for value in values)


def decision_value_gaps(record: dict[str, Any]) -> list[str]:
    cost = record.get("cost_profile") or {}
    scholarships = record.get("scholarship_profile") or {}
    curriculum = record.get("curriculum_profile") or {}
    eligibility = record.get("eligibility_profile") or {}
    timeline = record.get("application_timeline_profile") or {}
    living = record.get("living_profile") or {}

    gaps: list[str] = []
    if not any_present(record.get("teaching_language"), (record.get("language_profile") or {}).get("teaching_language"), record.get("Admission_Language_Req")):
        gaps.append("teaching_language")
    if not any_present(
        cost.get("tuition_eur_per_year_estimated"), cost.get("tuition_eur_per_year_min"),
        cost.get("tuition_eur_per_year_max"), cost.get("tuition_non_eu_full_program"),
        cost.get("tuition_usd_per_year"), cost.get("tuition_usd_per_year_at_three_quarters"), cost.get("tuition_usd_per_quarter"),
        cost.get("tuition_gbp_per_year"), cost.get("tuition_chf_per_year"),
        cost.get("tuition_eur_total"), cost.get("tuition_czk_per_year"),
        cost.get("tuition_gbp_per_year_min"), cost.get("tuition_gbp_per_year_max"),
        cost.get("tuition_chf_per_year_min"), cost.get("tuition_chf_per_year_max"), cost.get("tuition_chf_per_semester"),
        cost.get("tuition_sek_per_year"), cost.get("tuition_dkk_per_year"), cost.get("tuition_sek_per_term"),
        record.get("tuition_eur_per_year"), record.get("Cost_Tuition"),
    ):
        gaps.append("tuition_or_fee")
    if not any_present(
        scholarships.get("scholarship_names"), scholarships.get("merit_scholarships"),
        scholarships.get("funding_notes"), scholarships.get("regional_scholarship_name"),
        scholarships.get("available_types"), scholarships.get("details"), scholarships.get("funding_status"),
        record.get("Scholarships"),
    ):
        gaps.append("scholarship_or_funding")
    if not any_present(
        curriculum.get("tracks"), curriculum.get("specializations"),
        curriculum.get("notable_courses"), curriculum.get("core_courses"),
        curriculum.get("mandatory_courses"), curriculum.get("elective_courses"),
        record.get("Curriculum"),
    ):
        gaps.append("curriculum_or_tracks")
    if not any_present(
        eligibility.get("required_previous_degree"), eligibility.get("required_documents"),
        eligibility.get("admission_mode"), eligibility.get("minimum_gpa"), record.get("Admission_Requirements"),
    ):
        gaps.append("admission_requirements")
    if not any_present(
        timeline.get("non_eu_deadline"), timeline.get("deadline_non_eu"), timeline.get("winter_deadline"),
        timeline.get("application_deadline"), record.get("deadline"), record.get("Deadline_Winter_Close"),
    ):
        gaps.append("application_timeline")
    if not any_present(
        living.get("monthly_living_cost_eur_min"), living.get("monthly_living_cost_eur_max"),
        living.get("monthly_living_cost_eur_estimated"), living.get("average_room_rent_eur"),
        # A sourced rent range is just as decision-useful as a single rent
        # quote. It is also safer for volatile housing markets, where the
        # university publishes a planning range rather than one average.
        living.get("average_room_rent_eur_min"), living.get("average_room_rent_eur_max"),
        living.get("average_room_rent_usd_per_month_min"), living.get("average_room_rent_usd_per_month_max"),
        living.get("average_room_rent_gbp_per_month_min"), living.get("average_room_rent_gbp_per_month_max"),
        living.get("average_room_rent_chf_per_month_min"), living.get("average_room_rent_chf_per_month_max"),
        living.get("average_room_rent_sek_per_month_min"), living.get("average_room_rent_sek_per_month_max"),
        living.get("average_room_rent_dkk_per_month_min"), living.get("average_room_rent_dkk_per_month_max"),
        living.get("housing_budget_usd_per_year"), living.get("housing_budget_gbp_per_year"),
        living.get("housing_budget_chf_per_year"), living.get("housing_budget_sek_per_year"),
        living.get("official_student_total_budget_usd_per_month_examples"),
        living.get("official_student_total_budget_gbp_per_month_examples"),
        living.get("official_student_total_budget_chf_per_month_examples"),
        living.get("official_student_total_budget_sek_per_month_examples"),
        living.get("official_student_total_budget_dkk_per_month_examples"),
        living.get("monthly_housing_rent_usd_per_month_min"), living.get("monthly_housing_rent_usd_per_month_max"),
        living.get("monthly_housing_rent_gbp_per_month_min"), living.get("monthly_housing_rent_gbp_per_month_max"),
        living.get("monthly_housing_rent_chf_per_month_min"), living.get("monthly_housing_rent_chf_per_month_max"),
        living.get("monthly_housing_rent_sek_per_month_min"), living.get("monthly_housing_rent_sek_per_month_max"),
        living.get("monthly_housing_rent_dkk_per_month_min"), living.get("monthly_housing_rent_dkk_per_month_max"),
        living.get("monthly_living_cost_usd_per_month_min"), living.get("monthly_living_cost_usd_per_month_max"),
        living.get("monthly_living_cost_gbp_per_month_min"), living.get("monthly_living_cost_gbp_per_month_max"),
        living.get("monthly_living_cost_chf_per_month_min"), living.get("monthly_living_cost_chf_per_month_max"), living.get("monthly_living_cost_chf_per_month"),
        living.get("monthly_living_cost_sek_per_month_min"), living.get("monthly_living_cost_sek_per_month_max"),
        living.get("monthly_living_cost_dkk_per_month_min"), living.get("monthly_living_cost_dkk_per_month_max"),
        cost.get("living_cost_usd_per_year_i20"), cost.get("living_cost_usd_per_year"), cost.get("living_cost_usd_per_year_min"), cost.get("living_cost_usd_per_year_max"),
        cost.get("living_cost_gbp_per_year"), cost.get("living_cost_gbp_per_year_min"), cost.get("living_cost_gbp_per_year_max"),
        cost.get("living_cost_chf_per_year"), cost.get("living_cost_chf_per_year_min"), cost.get("living_cost_chf_per_year_max"),
        cost.get("living_cost_sek_per_year"), cost.get("living_cost_sek_per_year_min"), cost.get("living_cost_sek_per_year_max"),
        cost.get("living_cost_dkk_per_year"), cost.get("living_cost_dkk_per_year_min"), cost.get("living_cost_dkk_per_year_max"),
        record.get("Living_Cost_EUR_Month"),
    ):
        gaps.append("living_or_housing_cost")
    return gaps


def label(record: dict[str, Any]) -> str:
    return str(record.get("id") or record.get("Uni_ID") or record.get("university") or record.get("University_Name") or "unknown")


def main() -> int:
    total = complete = 0
    file_reports: list[tuple[str, int, int, list[tuple[str, list[str]]]]] = []
    for filename in TARGET_FILES:
        payload = json.loads((ROOT / "data_base" / filename).read_text(encoding="utf-8"))
        report: list[tuple[str, list[str]]] = []
        for record in records(payload):
            total += 1
            evidence_gaps = audit_record(record)["unverified_critical_fields"]
            value_gaps = decision_value_gaps(record)
            blockers = list(dict.fromkeys(evidence_gaps + value_gaps))
            if not blockers:
                complete += 1
            else:
                report.append((label(record), blockers))
        file_reports.append((filename, len(records(payload)), len(report), report))

    print(f"Decision-gap report: {complete}/{total} records currently answer all core decision fields with evidence.")
    for filename, count, incomplete, report in file_reports:
        print(f"{filename}: {count - incomplete}/{count} complete; {incomplete} need research")
        for record_id, blockers in report[:8]:
            print(f"  - {record_id}: {', '.join(blockers)}")
        if len(report) > 8:
            print(f"  - … {len(report) - 8} more")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
