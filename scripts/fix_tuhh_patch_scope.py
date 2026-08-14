"""Repair two German records touched by an over-broad TUHH JSON patch."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data_base" / "almanya.json"


def main() -> None:
    records = json.loads(DB_PATH.read_text(encoding="utf-8"))
    by_id = {record["id"]: record for record in records}

    braunschweig = by_id["germany-braunschweig-msc-aerospace"]
    braunschweig["source_profile"]["needs_verification"] = False
    braunschweig["scoring_inputs"]["hard_filter_flags"]["needs_verification"] = False
    braunschweig["data_quality"]["status"] = "verified"

    bremen = by_id["de_bremen_space_engineering_msc"]
    bremen["quality_control"]["qc_status"] = "passed"
    bremen["quality_control"]["failed_canary_tests"] = []
    bremen["quality_control"]["remaining_verification_tasks"] = []

    DB_PATH.write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Restored Braunschweig and Bremen quality-state fields.")


if __name__ == "__main__":
    main()
