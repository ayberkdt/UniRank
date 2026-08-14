"""Consolidate the duplicate Italy files into `data_base/italy.json`."""

from __future__ import annotations

import argparse
import json
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANONICAL_PATH = ROOT / "data_base" / "italy.json"
DUPLICATE_PATH = ROOT / "data_base" / "italya.json"

ALT_TO_CANONICAL = {
    "it-polimi-aero-msc": "polimi-msc-aeronautical",
    "it-polito-aero-msc": "polito-msc-aerospace",
    "it-sapienza-aero-msc": "sapienza_space_astronautical_msc",
    "it-bologna-aero-msc": "unibo_aerospace_forli",
    "it-padova-aero-msc": "unipd_aerospace",
    "it-pisa-aero-msc": "unipi_aerospace_master",
    "it-naples-aero-msc": "unina_aerospace_master",
    "politecnico-di-bari": "poliba_aerospace_master",
    "universita-degli-studi-di-palermo": "unipa_aerospace_master",
    "university-of-trento": "unitn_mechatronics_space",
}


def preference(record: dict) -> tuple[int, int, str]:
    quality = record.get("data_quality") or {}
    return (
        len(quality.get("verified_fields") or []),
        len((record.get("source_profile") or {}).get("source_log") or []),
        str((record.get("source_profile") or {}).get("last_verified") or ""),
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    canonical_payload = json.loads(CANONICAL_PATH.read_text(encoding="utf-8"))
    container_key = "programs" if isinstance(canonical_payload.get("programs"), list) else "universities"
    canonical_rows = canonical_payload.get(container_key) or []
    alternate_rows = json.loads(DUPLICATE_PATH.read_text(encoding="utf-8"))
    by_id = {record["id"]: record for record in canonical_rows}
    moved_unique = replaced = suppressed = 0

    for alternate in alternate_rows:
        alternate_id = alternate.get("id")
        canonical_id = ALT_TO_CANONICAL.get(alternate_id)
        if canonical_id is None:
            if alternate_id not in by_id:
                canonical_rows.append(alternate)
                by_id[alternate_id] = alternate
                moved_unique += 1
            continue
        canonical = by_id[canonical_id]
        if preference(alternate) > preference(canonical):
            preferred = deepcopy(alternate)
            preferred["id"] = canonical_id
            # Stable display identity comes from the canonical record; the
            # richer duplicate supplies profiles and source evidence.
            for key in (
                "country", "university", "university_native_name", "city",
                "region", "program_name", "program_native_name",
                "program_degree", "degree_level", "degree_class",
            ):
                if key in canonical:
                    preferred[key] = canonical[key]
            index = canonical_rows.index(canonical)
            canonical_rows[index] = preferred
            by_id[canonical_id] = preferred
            replaced += 1
        else:
            suppressed += 1

    print(
        f"Italy consolidation preview: {len(canonical_rows)} canonical programmes; "
        f"{moved_unique} unique moved, {replaced} richer duplicates adopted, "
        f"{suppressed} duplicates suppressed."
    )
    if args.write:
        canonical_payload[container_key] = canonical_rows
        CANONICAL_PATH.write_text(json.dumps(canonical_payload, ensure_ascii=False, indent=4) + "\n", encoding="utf-8")
        DUPLICATE_PATH.write_text("[]\n", encoding="utf-8")
        print("Italy consolidation applied; italya.json is now an empty retired input.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
