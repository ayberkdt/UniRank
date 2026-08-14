"""Apply a reviewed transport audit to matching active source-log entries."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data_base"


def rows(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [row for row in payload if isinstance(row, dict)]
    if isinstance(payload, dict):
        for key in ("programs", "universities"):
            if isinstance(payload.get(key), list):
                return [row for row in payload[key] if isinstance(row, dict)]
    return []


def normalized_status(result: dict[str, Any]) -> str:
    status = result.get("access_status") or "unknown"
    if status != "broken":
        return status
    error = str(result.get("error") or "").lower()
    # Timeout, TLS verification and method protection show that the page may
    # exist but could not be safely machine-verified. They are blocked rather
    # than asserted to be nonexistent.
    if result.get("status_code") == 405 or any(token in error for token in ("timed out", "timeout", "ssl", "certificate")):
        return "blocked"
    return "broken"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("report", type=Path)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    report_path = args.report if args.report.is_absolute() else ROOT / args.report
    report = json.loads(report_path.read_text(encoding="utf-8"))
    by_url = {result["url"]: result for result in report.get("results", [])}
    changed_files = changed_sources = 0

    for path in sorted(DATA.glob("*.json")):
        if path.name == "taxonomy.json":
            continue
        source_text = path.read_text(encoding="utf-8-sig")
        payload = json.loads(source_text)
        file_changed = False
        for record in rows(payload):
            for source in (record.get("source_profile") or {}).get("source_log") or []:
                if not isinstance(source, dict):
                    continue
                result = by_url.get(source.get("url"))
                if not result:
                    continue
                status = normalized_status(result)
                final_url = result.get("final_url") or source.get("url")
                before = (source.get("access_status"), source.get("last_checked"), source.get("final_url"))
                source["access_status"] = status
                source["last_checked"] = report.get("checked_at")
                if final_url and final_url.rstrip("/") != str(source.get("url") or "").rstrip("/"):
                    source["final_url"] = final_url
                else:
                    source.pop("final_url", None)
                after = (source.get("access_status"), source.get("last_checked"), source.get("final_url"))
                if before != after:
                    file_changed = True
                    changed_sources += 1
        if file_changed:
            changed_files += 1
            if args.write:
                indent = 2 if "\n  {" in source_text[:100] else 4
                path.write_text(json.dumps(payload, ensure_ascii=False, indent=indent) + "\n", encoding="utf-8")

    print(
        f"Source link audit {'applied' if args.write else 'preview'}: "
        f"{changed_sources} source entries in {changed_files} files."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
