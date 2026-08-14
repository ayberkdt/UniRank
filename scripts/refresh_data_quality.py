"""Refresh stored evidence-audit summaries for selected programme records.

The command is dry-run by default.  It updates only ``data_quality`` and does
not gate values or replace the human quality-control review.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from unirank.core.integrity import audit_record


def rows(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [row for row in payload if isinstance(row, dict)]
    if isinstance(payload, dict):
        for key in ("programs", "universities"):
            if isinstance(payload.get(key), list):
                return [row for row in payload[key] if isinstance(row, dict)]
    return []


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--record-id", action="append", required=True)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    targets = set(args.record_id)
    found: set[str] = set()
    changed_files = 0
    for path in sorted((ROOT / "data_base").glob("*.json")):
        if path.name == "taxonomy.json":
            continue
        source = path.read_text(encoding="utf-8-sig")
        payload = json.loads(source)
        changed = False
        for record in rows(payload):
            record_id = str(record.get("id") or record.get("Uni_ID") or "")
            if record_id not in targets:
                continue
            found.add(record_id)
            quality = {**audit_record(record), "audited_at": date.today().isoformat()}
            print(f"{path.name}:{record_id} -> {quality['status']} {quality['unverified_critical_fields']}")
            if record.get("data_quality") != quality:
                record["data_quality"] = quality
                changed = True
        if changed and args.write:
            indent = 2 if source.lstrip().startswith("[") else 4
            path.write_text(json.dumps(payload, ensure_ascii=False, indent=indent) + "\n", encoding="utf-8")
            changed_files += 1

    missing = sorted(targets - found)
    if missing:
        print("Missing record ids: " + ", ".join(missing), file=sys.stderr)
        return 1
    print(f"Mode={'write' if args.write else 'dry-run'}; changed files={changed_files}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
