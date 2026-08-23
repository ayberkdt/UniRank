from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).parents[1]
DATABASE = ROOT / "data_base"


def database_hashes() -> dict[str, str]:
    return {
        path.name: hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(DATABASE.glob("*.json"))
    }


def test_research_audit_is_read_only_without_write_flag() -> None:
    before = database_hashes()

    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "audit_research_data.py")],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    assert "would update" in result.stdout
    assert database_hashes() == before

