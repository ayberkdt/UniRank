"""Measure geographic and programme coverage without mistaking candidates for records."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data_base"
COVERAGE = ROOT / "config" / "research_coverage_v2.json"
CATALOG_SCOPE = ROOT / "config" / "catalog_scope.json"


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
        value = value.get("en") or value.get("tr") or ""
    return str(value or "").strip()


def programme_name(record: dict[str, Any]) -> str:
    return text(
        record.get("program_name")
        or record.get("target_program_name")
        or record.get("Program_Name")
        or (record.get("program_profile") or {}).get("name")
    )


def main() -> int:
    manifest = json.loads(COVERAGE.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG_SCOPE.read_text(encoding="utf-8"))
    aliases = catalog.get("country_aliases") or {}
    included = manifest["included_countries"]
    counts: Counter[str] = Counter()
    candidates: Counter[str] = Counter()

    for path in sorted(DATA.glob("*.json")):
        if path.name == "taxonomy.json":
            continue
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
        for record in rows(payload):
            country = text(record.get("country") or record.get("Country"))
            country = aliases.get(country, country)
            if country not in included:
                continue
            if programme_name(record):
                counts[country] += 1
            else:
                candidates[country] += 1

    represented = [country for country in included if counts[country]]
    unrepresented = [country for country in included if not counts[country]]
    print(f"Research coverage: {sum(counts.values())} named programme records across {len(represented)}/{len(included)} in-scope countries.")
    print(f"Institution-only discovery candidates kept outside the product catalogue: {sum(candidates.values())}.")
    print("Countries with named programmes:")
    for country in represented:
        suffix = f" (+{candidates[country]} discovery candidates)" if candidates[country] else ""
        print(f"  - {country}: {counts[country]}{suffix}")
    print("Countries requiring discovery or a sourced no-program conclusion:")
    for country in unrepresented:
        suffix = f" ({candidates[country]} discovery candidates)" if candidates[country] else ""
        print(f"  - {country}{suffix}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
