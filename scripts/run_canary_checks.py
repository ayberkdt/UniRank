"""Automated version of the research canary checklist.

The checks reject only unsafe *claims*, not honest missing data.  It is safe
for the database to contain candidate programmes marked needs_revision.
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


def rows(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [row for row in payload if isinstance(row, dict)]
    if isinstance(payload, dict):
        return [row for row in payload.get("programs", payload.get("universities", [])) if isinstance(row, dict)]
    return []


def main() -> int:
    failures: list[str] = []
    audited = 0
    for path in sorted((ROOT / "data_base").glob("*.json")):
        if path.name == "taxonomy.json":
            continue
        payload = json.loads(path.read_text(encoding="utf-8"))
        for index, record in enumerate(rows(payload)):
            audited += 1
            label = f"{path.name}#{index} ({record.get('id') or record.get('Uni_ID') or 'unknown'})"
            quality = audit_record(record)
            if record.get("data_quality", {}).get("unverified_critical_fields") != quality["unverified_critical_fields"]:
                failures.append(f"{label}: stale or missing data_quality audit")
            qc = record.get("quality_control", {})
            if qc.get("qc_status") == "passed" and quality["status"] != "verified":
                failures.append(f"{label}: QC passed despite unverified critical fields")
            sentiment = record.get("student_sentiment_profile", {})
            if sentiment.get("student_satisfaction_score") is not None:
                if not sentiment.get("student_sentiment_sources") or not sentiment.get("date_range") or not isinstance(sentiment.get("sample_size_estimate"), (int, float)) or sentiment["sample_size_estimate"] < 3:
                    failures.append(f"{label}: unsupported student satisfaction score")
            for source in (record.get("source_profile", {}).get("source_log") or []):
                if not isinstance(source, dict):
                    failures.append(f"{label}: malformed source log entry")
                    continue
                if source.get("url") and not source.get("access_status"):
                    failures.append(f"{label}: source has URL but no access status")

    if failures:
        print(f"Canary checks failed ({len(failures)}/{audited} records):")
        for failure in failures[:50]:
            print(f"- {failure}")
        return 1
    print(f"Canary checks passed for {audited} records: no unsupported satisfaction scores or false QC passes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
