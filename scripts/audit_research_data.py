"""Audit the JSON data store and optionally persist its source-safe state.

The API applies the same integrity gate at read time. The default command is a
safe dry run; pass ``--write`` to persist the gated state. Persisting prevents
raw JSON from retaining high-stakes values that have no checked official
evidence, so exports and future tooling cannot accidentally present them as
facts.
"""

from __future__ import annotations

import json
import re
import sys
from argparse import ArgumentParser
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from unirank.core.integrity import apply_integrity_gate, audit_record


DATABASE = ROOT / "data_base"
TODAY = date.today().isoformat()


def records_in(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [row for row in payload if isinstance(row, dict)]
    if isinstance(payload, dict):
        for key in ("programs", "universities"):
            if isinstance(payload.get(key), list):
                return [row for row in payload[key] if isinstance(row, dict)]
    return []


def detected_indent(source_text: str) -> int:
    """Keep the repository's existing 2- or 4-space JSON formatting."""
    if source_text.lstrip().startswith("["):
        match = re.search(r'^\s*\[\r?\n( +)\{', source_text)
    else:
        match = re.search(r'^\s*\{\r?\n( +)"', source_text)
    return len(match.group(1)) if match else 4


def main() -> None:
    parser = ArgumentParser(
        description="Audit research records without rewriting the database unless --write is supplied."
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Persist integrity-gated records and refreshed quality-control metadata.",
    )
    args = parser.parse_args()

    changed_files = 0
    audited_records = 0
    invalid_scores = 0
    for path in sorted(DATABASE.glob("*.json")):
        if path.name == "taxonomy.json":
            continue
        source_text = path.read_bytes().decode("utf-8")
        payload = json.loads(source_text)
        indent = detected_indent(source_text)
        newline = "\r\n" if "\r\n" in source_text else "\n"
        records = records_in(payload)
        if not records:
            continue
        for record in records:
            # Keep the stored database as honest as the public API: an
            # unsupported tuition, language, funding or housing value becomes
            # explicitly unknown rather than a tempting but unsafe raw fact.
            gated = apply_integrity_gate(record)
            record.clear()
            record.update(gated)
            quality = audit_record(record)
            quality["audited_at"] = TODAY
            record["data_quality"] = quality
            audited_records += 1

            sentiment = record.get("student_sentiment_profile") or {}
            score = sentiment.get("student_satisfaction_score")
            source_count = len(sentiment.get("student_sentiment_sources") or [])
            sample_size = sentiment.get("sample_size_estimate")
            if score is not None and (source_count < 1 or not isinstance(sample_size, (int, float)) or sample_size < 3 or not sentiment.get("date_range")):
                sentiment["student_satisfaction_score"] = None
                sentiment["sentiment_confidence"] = "unknown"
                sentiment["verification_notes"] = {
                    "en": "Score removed during evidence audit: sample size, date range, or cited sentiment sources are insufficient.",
                    "tr": "Kanıt denetiminde puan kaldırıldı: örneklem büyüklüğü, tarih aralığı veya atıflı duygu analizi kaynağı yetersiz.",
                }
                record["student_sentiment_profile"] = sentiment
                invalid_scores += 1

            qc = record.setdefault("quality_control", {})
            qc["checked_at"] = TODAY
            missing = quality["unverified_critical_fields"]
            qc["qc_status"] = "passed" if quality["status"] == "verified" else "needs_revision"
            qc["failed_canary_tests"] = [] if not missing else ["missing_or_unverified_critical_fields"]
            qc["remaining_verification_tasks"] = [
                {
                    "en": f"Add a checked official source for {field}.",
                    "tr": f"{field} için kontrol edilmiş resmî kaynak ekleyin.",
                }
                for field in missing
            ]
            qc["qc_notes"] = {
                "en": "Automated source-evidence audit. Values are only shown publicly when supported by checked source evidence.",
                "tr": "Otomatik kaynak-kanıt denetimi. Değerler, yalnızca kontrol edilmiş kaynak kanıtı varsa herkese açık olarak gösterilir.",
            }

        serialised = json.dumps(payload, ensure_ascii=False, indent=indent)
        rendered = (serialised.replace("\n", newline) + newline).encode("utf-8")
        if rendered != source_text.encode("utf-8"):
            changed_files += 1
            if args.write:
                path.write_bytes(rendered)

    action = "updated" if args.write else "would update"
    print(
        f"Audited {audited_records} records; {action} {changed_files} files; "
        f"removed {invalid_scores} unsupported sentiment scores in the audited view."
    )


if __name__ == "__main__":
    main()
