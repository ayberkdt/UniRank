"""Remove duplicated legacy top-level fields from active catalogue records.

The migration is intentionally conservative: it only touches records that are
inside `config/catalog_scope.json` and already contain the canonical identity
fields. Excluded Asian records remain byte-for-byte outside this migration.
Run without `--write` for a report, then use `--write` for the mechanical edit.
"""

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

CANONICAL_IDENTITY = {"id", "country", "university", "program_name"}
LEGACY_TOP_LEVEL_FIELDS = {
    "Country", "City", "State_Region", "Uni_ID", "University_Name",
    "University_Display_Name", "University_Short_Name", "Cost_Tuition",
    "Cost_Semester_Fees", "Scholarships_Info", "Cost_City_Living",
    "Cost_City_Rank", "Living_Housing_Difficulty", "Living_Housing_Score",
    "Program_Name", "Program_Degree", "Program_ECTS", "Program_URL",
    "Program_Scope", "Admission_Mode", "Admission_Language_Req",
    "Analysis_Strong_Areas", "Analysis_Pros", "Analysis_Cons",
    "Analysis_Tags", "Industry_Ecosystem", "Industry_Comp_Intensity",
    "Industry_Partners", "Internship_Mandatory", "Internship_Notes",
    "Deadline_Winter_Open", "Deadline_Winter_Close", "Deadline_Winter_Note",
    "Deadline_Summer_Open", "Deadline_Summer_Close", "Deadline_Summer_Note",
    "Deadline_General_Note", "Meta_Sources", "Meta_Updated_At",
    "Meta_Needs_Verification", "global_recognition", "field_recognition",
}


def records(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [row for row in payload if isinstance(row, dict)]
    if isinstance(payload, dict):
        for key in ("programs", "universities"):
            if isinstance(payload.get(key), list):
                return [row for row in payload[key] if isinstance(row, dict)]
    return []


def country(record: dict[str, Any]) -> str:
    value = record.get("country") or record.get("Country") or ""
    if isinstance(value, dict):
        value = value.get("en") or value.get("tr") or ""
    text = str(value).strip()
    return ALIASES.get(text, text)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    changed_files = changed_records = removed_fields = 0
    blocked: list[str] = []
    for path in sorted(DATA.glob("*.json")):
        if path.name == "taxonomy.json":
            continue
        source = path.read_text(encoding="utf-8-sig")
        payload = json.loads(source)
        file_changed = False
        for record in records(payload):
            if country(record) in EXCLUDED:
                continue
            present_legacy = LEGACY_TOP_LEVEL_FIELDS.intersection(record)
            if not present_legacy:
                continue
            if not CANONICAL_IDENTITY.issubset(record):
                blocked.append(f"{path.name}:{record.get('Uni_ID') or record.get('id') or 'unknown'}")
                continue
            for key in present_legacy:
                record.pop(key, None)
            changed_records += 1
            removed_fields += len(present_legacy)
            file_changed = True
        if file_changed:
            changed_files += 1
            if args.write:
                indent = 2 if "\n  {" in source[:100] else 4
                path.write_text(json.dumps(payload, ensure_ascii=False, indent=indent) + "\n", encoding="utf-8")

    print(
        f"Legacy migration {'applied' if args.write else 'preview'}: "
        f"{removed_fields} fields from {changed_records} active records in {changed_files} files."
    )
    if blocked:
        print("Blocked records missing canonical identity:")
        for value in blocked:
            print(f"- {value}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
