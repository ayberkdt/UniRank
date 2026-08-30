"""Merge researched enrichment payloads into the UniRank database.

The repository previously grew one throw-away script per university update.
This applier replaces that pattern with a single, auditable path: research is
written as data under ``research_queue/enrichment/``, every payload carries the
official source it came from, and the merge refuses to run when a payload adds
a decision value without an accompanying source entry.

Payload shape::

    {
      "checked": "2026-08-29",
      "records": [
        {
          "id": "netherlands_delft_msc_aerospace",
          "research_profile": { ... },        # deep-merged into the record
          "sources": [ { "url": ..., "source_type": ..., "relevant_fields": [...] } ]
        }
      ]
    }

Dictionaries are deep-merged so an update never silently drops a sibling key.
Lists are replaced wholesale, because a researched list (faculty, labs,
scholarship steps) is always the complete current state of that list.

Usage::

    python scripts/apply_enrichment.py                 # validate and report
    python scripts/apply_enrichment.py --write         # merge into data_base/
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data_base"
PAYLOAD_DIR = ROOT / "research_queue" / "enrichment"
SKIP_FILES = {"taxonomy.json"}

# Profiles that carry decision values a student could act on.  A payload that
# touches one of these must also supply at least one source for it.
SOURCED_PROFILES = {
    "research_profile": "research",
    "scholarship_profile": "scholarship",
    "living_profile": "housing",
    "cost_profile": "tuition",
    "application_timeline_profile": "deadline",
    "curriculum_profile": "curriculum",
    "eligibility_profile": "admission",
    "language_profile": "language",
    "industry_ecosystem_profile": "industry",
}


def load_document(path: Path) -> tuple[Any, list[dict[str, Any]]]:
    document = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(document, list):
        return document, [r for r in document if isinstance(r, dict)]
    if isinstance(document, dict):
        for key in ("programs", "universities", "records"):
            value = document.get(key)
            if isinstance(value, list):
                return document, [r for r in value if isinstance(r, dict)]
    return document, []


def build_index() -> dict[str, tuple[Path, dict[str, Any], Any]]:
    index: dict[str, tuple[Path, dict[str, Any], Any]] = {}
    for path in sorted(DATA_DIR.glob("*.json")):
        if path.name in SKIP_FILES:
            continue
        document, records = load_document(path)
        for record in records:
            # The Japan, Korea and China files predate the current schema and
            # key their rows on Uni_ID rather than id, so both are addressable.
            for key in ("id", "Uni_ID"):
                identifier = record.get(key)
                if isinstance(identifier, str) and identifier:
                    index.setdefault(identifier, (path, record, document))
    return index


def deep_merge(target: dict[str, Any], patch: dict[str, Any]) -> None:
    for key, value in patch.items():
        if isinstance(value, dict) and isinstance(target.get(key), dict):
            deep_merge(target[key], value)
        else:
            target[key] = value


def merge_sources(record: dict[str, Any], entries: list[dict[str, Any]], checked: str) -> int:
    profile = record.setdefault("source_profile", {})
    existing = [item for item in profile.get("source_log", []) if isinstance(item, dict)]
    added = 0
    for entry in entries:
        url = entry.get("url")
        source_type = entry.get("source_type")
        if not url or not source_type:
            continue
        normalised = {
            "url": url,
            "title": entry.get("title") or url,
            "source_type": source_type,
            "access_status": entry.get("access_status", "ok"),
            "last_checked": entry.get("last_checked", checked),
            "relevant_fields": entry.get("relevant_fields", []),
            "confidence": entry.get("confidence", "high"),
        }
        if entry.get("notes"):
            normalised["notes"] = entry["notes"]
        existing = [item for item in existing if (item.get("url"), item.get("source_type")) != (url, source_type)]
        existing.append(normalised)
        added += 1
    profile["source_log"] = existing
    profile["last_verified"] = checked
    return added


def validate(entry: dict[str, Any], checked: str) -> list[str]:
    problems: list[str] = []
    sources = entry.get("sources") or []
    covered = {
        str(field)
        for source in sources
        if isinstance(source, dict)
        for field in source.get("relevant_fields", [])
    }
    for profile_key, required_field in SOURCED_PROFILES.items():
        if profile_key in entry and required_field not in covered:
            problems.append(f"{entry.get('id')}: {profile_key} changed without a source covering '{required_field}'")
    for source in sources:
        if not isinstance(source, dict):
            problems.append(f"{entry.get('id')}: source entry is not an object")
            continue
        if not str(source.get("url", "")).startswith("https://"):
            problems.append(f"{entry.get('id')}: source url is not https: {source.get('url')!r}")
        if not source.get("relevant_fields"):
            problems.append(f"{entry.get('id')}: source {source.get('url')} has no relevant_fields")
    if not checked:
        problems.append(f"{entry.get('id')}: payload has no 'checked' date")
    return problems


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="merge the payloads into data_base/")
    parser.add_argument("--payload", help="apply only this payload file name")
    args = parser.parse_args()

    if not PAYLOAD_DIR.exists():
        print(f"no payload directory at {PAYLOAD_DIR}")
        return

    index = build_index()
    payloads = sorted(PAYLOAD_DIR.glob("*.json"))
    if args.payload:
        payloads = [p for p in payloads if p.name == args.payload]

    problems: list[str] = []
    touched_documents: dict[Path, Any] = {}
    applied = 0
    source_count = 0

    for payload_path in payloads:
        payload = json.loads(payload_path.read_text(encoding="utf-8"))
        checked = payload.get("checked", "")
        for entry in payload.get("records", []):
            identifier = entry.get("id")
            if identifier not in index:
                problems.append(f"{payload_path.name}: unknown record id {identifier!r}")
                continue
            problems.extend(validate(entry, checked))
            path, record, document = index[identifier]
            patch = {k: v for k, v in entry.items() if k not in {"id", "sources", "note"}}
            deep_merge(record, patch)
            source_count += merge_sources(record, entry.get("sources") or [], checked)
            touched_documents[path] = document
            applied += 1

    for problem in problems:
        print(f"PROBLEM  {problem}")

    print(f"\npayloads: {len(payloads)}  records patched: {applied}  sources added: {source_count}")

    if problems:
        print("refusing to write while problems remain" if args.write else "validation only")
        return

    if args.write:
        for path, document in touched_documents.items():
            path.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            print(f"wrote {path.relative_to(ROOT)}")
    else:
        print("report only - pass --write to persist")


if __name__ == "__main__":
    main()
