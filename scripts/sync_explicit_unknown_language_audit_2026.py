"""Synchronise records whose sources do not explicitly establish teaching language.

This migration changes only the data-quality audit metadata.  It does not infer
or add a teaching language.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data_base" / "austria.json"
TARGET_IDS = {
    "austria_tugraz_msc_mechanical",
    "austria_tuwien_msc_mechanical",
    "AT-TUW-INFOCOM-EN",
    "AT-JKU-MECH-DE",
    "AT-LEOBEN-ADVMAT-EN",
    "AT-FHOO-MECH-DE",
}


def main() -> None:
    payload = json.loads(PATH.read_text(encoding="utf-8"))
    changed: list[str] = []
    for record in payload["programs"]:
        if record.get("id") not in TARGET_IDS:
            continue
        quality = record.setdefault("data_quality", {})
        missing = list(quality.get("unverified_critical_fields") or [])
        if "language" not in missing:
            missing.insert(0, "language")
        quality["unverified_critical_fields"] = missing
        quality["status"] = "partial"
        record.setdefault("quality_control", {})["qc_status"] = "needs_revision"
        changed.append(record["id"])

    if set(changed) != TARGET_IDS:
        raise RuntimeError(f"Target mismatch: updated {sorted(changed)}")
    PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"updated": sorted(changed)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
