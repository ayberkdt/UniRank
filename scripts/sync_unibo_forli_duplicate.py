"""Keep the duplicated Bologna Aerospace record aligned with its checked source record."""

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = ROOT / "data_base" / "italy.json"
TARGET_PATH = ROOT / "data_base" / "italya.json"


def main() -> None:
    source_document = json.loads(SOURCE_PATH.read_text(encoding="utf-8"))
    source = next(item for item in source_document["universities"] if item.get("id") == "unibo_aerospace_forli")
    original = TARGET_PATH.read_text(encoding="utf-8")
    target_document = json.loads(original)
    target_rows = target_document if isinstance(target_document, list) else target_document["universities"]
    target = next(item for item in target_rows if item.get("id") == "it-bologna-aero-msc")
    fields = [
        "program_name", "program_native_name", "program_degree", "degree_level", "degree_class", "duration_years", "ects", "teaching_language", "program_url", "department", "campus", "program_status", "relevance_status",
        "eligibility_profile", "language_profile", "cost_profile", "scholarship_profile", "living_profile", "curriculum_profile", "category_profile", "research_profile", "industry_ecosystem_profile", "application_timeline_profile", "student_sentiment_profile", "decision_summary", "financials", "scholarships_info", "admission", "source_profile",
    ]
    for field in fields:
        if field in source:
            target[field] = deepcopy(source[field])
    newline = "\r\n" if "\r\n" in original else "\n"
    TARGET_PATH.write_text(json.dumps(target_document, ensure_ascii=False, indent=2).replace("\n", newline) + newline, encoding="utf-8")
    print("Synchronized duplicate Bologna Aerospace record with official source-grounded content.")


if __name__ == "__main__":
    print("Retired: Italy records were consolidated into data_base/italy.json.")
