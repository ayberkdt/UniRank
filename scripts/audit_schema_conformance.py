"""Audit active UniRank records against the saved research standard.

This report is intentionally broader than the runtime integrity gate. It finds
schema drift, duplicated programmes, missing applicant-decision fields and
suspicious provenance patterns without mutating the database.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data_base"
SCOPE = json.loads((ROOT / "config" / "catalog_scope.json").read_text(encoding="utf-8"))
ALIASES = SCOPE.get("country_aliases") or {}
EXCLUDED = {ALIASES.get(value, value) for value in SCOPE.get("excluded_countries", [])}

LEGACY_KEYS = {
    "Country", "City", "State_Region", "Uni_ID", "University_Name",
    "University_Display_Name", "University_Short_Name", "Cost_Tuition",
    "Cost_Semester_Fees", "Scholarships_Info", "Program_Name",
    "Program_Degree", "Program_ECTS", "Program_URL", "Program_Scope",
    "Admission_Mode", "Admission_Language_Req", "Meta_Sources",
}
REQUIRED_TOP_LEVEL = {
    "id", "country", "university", "program_name", "program_degree",
    "degree_level", "program_url", "program_status", "eligibility_profile",
    "language_profile", "cost_profile", "scholarship_profile",
    "living_profile", "curriculum_profile", "application_timeline_profile",
    "student_sentiment_profile", "source_profile", "quality_control",
}
V2_REQUIRED_TOP_LEVEL = {
    "schema_version", "record_type", "id", "country", "institution_profile",
    "location", "program_profile", "eligibility_profile", "language_profile",
    "cost_profile", "scholarship_profile", "living_profile",
    "curriculum_profile", "category_profile", "research_profile",
    "industry_ecosystem_profile", "application_timeline_profile",
    "ranking_profile", "outcomes_profile", "student_sentiment_profile",
    "source_profile", "decision_summary", "scoring_inputs", "quality_control",
}
SOURCE_REQUIRED = {
    "url", "title", "source_type", "access_status", "last_checked",
    "relevant_fields", "confidence",
}
VALID_CONFIDENCE = {"high", "medium", "low", "unknown"}
VALID_RISK = {"low", "medium", "high", "unknown"}
VALID_STATUS = {"active", "inactive", "unclear", "needs_verification"}
VALID_RELEVANCE = {"strong", "medium", "weak", "needs_review"}


def rows(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [row for row in payload if isinstance(row, dict)]
    if isinstance(payload, dict):
        for key in ("programs", "universities"):
            if isinstance(payload.get(key), list):
                return [row for row in payload[key] if isinstance(row, dict)]
    return []


def text(value: Any) -> str:
    if isinstance(value, dict):
        value = value.get("en") or value.get("tr") or value.get("name") or ""
    return str(value or "").strip()


def country(record: dict[str, Any]) -> str:
    value = text(record.get("country") or record.get("Country"))
    return ALIASES.get(value, value)


def identity(value: Any) -> str:
    return re.sub(r"[^a-z0-9]+", "", text(value).lower())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true", help="Exit non-zero when safety/schema blockers exist.")
    args = parser.parse_args()

    records: list[tuple[Path, dict[str, Any]]] = []
    for path in sorted(DATA.glob("*.json")):
        if path.name == "taxonomy.json":
            continue
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
        for record in rows(payload):
            if country(record) not in EXCLUDED:
                records.append((path, record))

    counts = Counter()
    examples: dict[str, list[str]] = defaultdict(list)
    programme_keys: dict[tuple[str, str, str, str], list[str]] = defaultdict(list)
    source_url_types: dict[str, set[str]] = defaultdict(set)

    def issue(kind: str, label: str) -> None:
        counts[kind] += 1
        if len(examples[kind]) < 8:
            examples[kind].append(label)

    for path, record in records:
        label = f"{path.name}:{record.get('id') or record.get('Uni_ID') or 'unknown'}"
        is_v2 = str(record.get("schema_version") or "").startswith("2.")
        missing = sorted((V2_REQUIRED_TOP_LEVEL if is_v2 else REQUIRED_TOP_LEVEL).difference(record))
        if missing:
            issue("missing_required_top_level", f"{label} -> {', '.join(missing)}")
        legacy = sorted(LEGACY_KEYS.intersection(record))
        if legacy:
            issue("legacy_top_level_fields", f"{label} -> {', '.join(legacy)}")
        if text(record.get("country")) in ALIASES:
            issue("noncanonical_country_name", f"{label} -> {text(record.get('country'))}")
        programme = record.get("program_profile") or {}
        program_status = programme.get("program_status") if is_v2 else record.get("program_status")
        relevance_status = programme.get("relevance_status") if is_v2 else record.get("relevance_status")
        if program_status not in VALID_STATUS:
            issue("invalid_program_status", f"{label} -> {program_status}")
        if relevance_status not in VALID_RELEVANCE:
            issue("invalid_relevance_status", f"{label} -> {relevance_status}")

        eligibility = record.get("eligibility_profile") or {}
        if not isinstance(eligibility.get("gre"), dict):
            issue("missing_explicit_gre_policy", label)
        scholarships = record.get("scholarship_profile") or {}
        if scholarships.get("application_mode") not in {
            "automatic", "separate", "mixed", "nomination", "invitation_only",
            "not_available", "unknown",
        }:
            issue("missing_scholarship_application_mode", label)
        living = record.get("living_profile") or {}
        if living.get("housing_access") not in {
            "guaranteed", "priority", "lottery", "waitlist",
            "first_come_first_served", "not_guaranteed", "not_offered", "unknown",
        }:
            issue("missing_housing_access_mode", label)

        for profile_name, risk_key in (
            ("eligibility_profile", "admission_risk"),
            ("language_profile", "language_risk"),
            ("living_profile", "living_risk"),
            ("application_timeline_profile", "timeline_risk"),
        ):
            value = (record.get(profile_name) or {}).get(risk_key)
            if value not in VALID_RISK:
                issue("invalid_or_missing_risk_value", f"{label} -> {profile_name}.{risk_key}={value}")

        source_profile = record.get("source_profile") or {}
        confidence = source_profile.get("field_confidence") or {}
        for key, value in confidence.items():
            if value not in VALID_CONFIDENCE:
                issue("invalid_confidence_value", f"{label} -> {key}={value}")
        source_log = source_profile.get("source_log") or []
        for index, source in enumerate(source_log):
            if not isinstance(source, dict):
                issue("malformed_source", f"{label} source#{index}")
                continue
            source_missing = sorted(SOURCE_REQUIRED.difference(source))
            if source_missing:
                issue("incomplete_source_metadata", f"{label} source#{index} -> {', '.join(source_missing)}")
            url = text(source.get("url"))
            if url:
                source_url_types[url].add(text(source.get("source_type")))
            if source.get("access_status") in {"broken", "not_found", "unknown"}:
                issue("unusable_source_in_log", f"{label} source#{index} -> {source.get('access_status')}")
            checked = text(source.get("last_checked"))
            if checked:
                try:
                    if date.fromisoformat(checked) > date.today():
                        issue("future_source_check_date", f"{label} source#{index} -> {checked}")
                except ValueError:
                    issue("invalid_source_check_date", f"{label} source#{index} -> {checked}")

        quality = record.get("data_quality") or {}
        qc = record.get("quality_control") or {}
        if qc.get("qc_status") == "passed" and quality.get("status") != "verified":
            issue("false_qc_pass", label)
        if qc.get("qc_status") == "passed" and qc.get("failed_canary_tests"):
            issue("qc_pass_with_failed_canary", label)

        key = (
            identity(country(record)),
            identity(record.get("university") or (record.get("institution_profile") or {}).get("name")),
            identity(record.get("program_name") or programme.get("name")),
            identity(record.get("degree_level") or record.get("program_degree") or programme.get("degree_level") or programme.get("degree_award")),
        )
        if all(key):
            programme_keys[key].append(label)

    for labels in programme_keys.values():
        if len(labels) > 1:
            issue("duplicate_programme", " | ".join(labels))
    for url, types in source_url_types.items():
        if len(types) >= 4:
            issue("source_url_overclassified", f"{url} -> {', '.join(sorted(types))}")

    print(f"Active-scope schema audit: {len(records)} raw programme records")
    for kind, count in counts.most_common():
        print(f"{kind}: {count}")
        for value in examples[kind]:
            print(f"  - {value}")

    blockers = sum(counts[kind] for kind in (
        "missing_required_top_level", "legacy_top_level_fields", "malformed_source",
        "unusable_source_in_log", "future_source_check_date", "false_qc_pass",
        "qc_pass_with_failed_canary", "duplicate_programme",
    ))
    print(f"Blocking conformance findings: {blockers}")
    return 1 if args.strict and blockers else 0


if __name__ == "__main__":
    raise SystemExit(main())
