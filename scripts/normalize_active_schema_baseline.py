"""Mechanically normalize active records without inventing research facts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data_base"
SCOPE = json.loads((ROOT / "config" / "catalog_scope.json").read_text(encoding="utf-8"))
ALIASES = SCOPE.get("country_aliases") or {}
EXCLUDED = {ALIASES.get(value, value) for value in SCOPE.get("excluded_countries", [])}
VALID_RISK = {"low", "medium", "high", "unknown"}
VALID_CONFIDENCE = {"high", "medium", "low", "unknown"}
STATUS_MAP = {
    "active_but_not_aerospace_path": "active",
    "active_low_relevance": "active",
    "upcoming_winter_2027_2028": "needs_verification",
}
RELEVANCE_MAP = {
    "highly_relevant": "strong",
    "high_relevance": "strong",
    "relevant": "strong",
    "relevant_with_caveats": "medium",
    "moderately_relevant": "medium",
    "moderate_relevance": "medium",
    "adjacent": "weak",
    "low_relevance": "weak",
    "weakly_relevant": "weak",
    "not_aerospace_specific": "weak",
}


def rows(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [row for row in payload if isinstance(row, dict)]
    if isinstance(payload, dict):
        for key in ("programs", "universities"):
            if isinstance(payload.get(key), list):
                return [row for row in payload[key] if isinstance(row, dict)]
    return []


def display(value: Any) -> str:
    if isinstance(value, dict):
        value = value.get("en") or value.get("tr") or ""
    return str(value or "").strip()


def record_country(record: dict[str, Any]) -> str:
    value = display(record.get("country") or record.get("Country"))
    return ALIASES.get(value, value)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    files_changed = records_changed = fields_changed = 0
    for path in sorted(DATA.glob("*.json")):
        if path.name == "taxonomy.json":
            continue
        source = path.read_text(encoding="utf-8-sig")
        payload = json.loads(source)
        file_changed = False
        for record in rows(payload):
            if record_country(record) in EXCLUDED:
                continue
            changed = 0

            canonical_country = record_country(record)
            if record.get("country") != canonical_country:
                record["country"] = canonical_country
                changed += 1
            location = record.get("location")
            if isinstance(location, dict) and location.get("country") != canonical_country:
                location["country"] = canonical_country
                changed += 1

            status = record.get("program_status")
            if status in STATUS_MAP:
                record["program_status"] = STATUS_MAP[status]
                changed += 1
            relevance = record.get("relevance_status")
            normalized_relevance = RELEVANCE_MAP.get(relevance, relevance)
            if normalized_relevance not in {"strong", "medium", "weak", "needs_review"}:
                normalized_relevance = "needs_review"
            if relevance != normalized_relevance:
                record["relevance_status"] = normalized_relevance
                changed += 1

            for profile_name, risk_key in (
                ("eligibility_profile", "admission_risk"),
                ("language_profile", "language_risk"),
                ("living_profile", "living_risk"),
                ("application_timeline_profile", "timeline_risk"),
            ):
                profile = record.setdefault(profile_name, {})
                if profile.get(risk_key) not in VALID_RISK:
                    profile[risk_key] = "unknown"
                    changed += 1

            eligibility = record.setdefault("eligibility_profile", {})
            if not isinstance(eligibility.get("gre"), dict):
                eligibility["gre"] = {
                    "policy": "unknown",
                    "test_type": "unknown",
                    "minimum_scores": {},
                    "recommended_scores": {},
                    "validity_rule": "",
                    "waiver_rules": [],
                    "source_ids": [],
                }
                changed += 1

            scholarships = record.setdefault("scholarship_profile", {})
            for key, default in (
                ("application_mode", "unknown"),
                ("automatic_consideration", None),
                ("separate_application_required", None),
            ):
                if key not in scholarships:
                    scholarships[key] = default
                    changed += 1

            living = record.setdefault("living_profile", {})
            for key, default in (
                ("housing_access", "unknown"),
                ("housing_application_separate", None),
            ):
                if key not in living:
                    living[key] = default
                    changed += 1

            confidence = record.setdefault("source_profile", {}).setdefault("field_confidence", {})
            for key, value in list(confidence.items()):
                if value not in VALID_CONFIDENCE:
                    confidence[key] = "unknown"
                    changed += 1

            quality = record.get("data_quality") or {}
            qc = record.setdefault("quality_control", {})
            missing = quality.get("unverified_critical_fields") or []
            expected_failed = [] if not missing else ["missing_or_unverified_critical_fields"]
            if qc.get("failed_canary_tests") != expected_failed:
                qc["failed_canary_tests"] = expected_failed
                changed += 1

            if changed:
                file_changed = True
                records_changed += 1
                fields_changed += changed

        if file_changed:
            files_changed += 1
            if args.write:
                indent = 2 if "\n  {" in source[:100] else 4
                path.write_text(json.dumps(payload, ensure_ascii=False, indent=indent) + "\n", encoding="utf-8")

    print(
        f"Baseline normalization {'applied' if args.write else 'preview'}: "
        f"{fields_changed} field changes across {records_changed} records in {files_changed} files."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
