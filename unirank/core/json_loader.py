from __future__ import annotations
import json
from pathlib import Path
import pandas as pd
from typing import Any, Dict, List, Optional, Tuple, Iterable
from dataclasses import dataclass, field
from pydantic import ValidationError

from unirank.core.schema import UniversityRecord

@dataclass(frozen=True, slots=True)
class LoadIssue:
    level: str
    file: str
    message: str
    record_index: Optional[int] = None
    record_id: Optional[str] = None

    @property
    def is_error(self) -> bool: return self.level == "error"
    @property
    def is_warn(self) -> bool: return self.level == "warn"

    @staticmethod
    def warn(file: str, message: str, record_index: Optional[int] = None, record_id: Optional[str] = None) -> "LoadIssue":
        return LoadIssue("warn", file, message, record_index, record_id)

    @staticmethod
    def error(file: str, message: str, record_index: Optional[int] = None, record_id: Optional[str] = None) -> "LoadIssue":
        return LoadIssue("error", file, message, record_index, record_id)


@dataclass(slots=True)
class LoadReport:
    folder: str
    files_seen: int
    files_loaded: int
    records_seen: int
    records_loaded: int
    issues: List[LoadIssue] = field(default_factory=list)

    def has_errors(self) -> bool: return any(i.is_error for i in self.issues)
    def error_count(self) -> int: return sum(1 for i in self.issues if i.is_error)
    def warn_count(self) -> int: return sum(1 for i in self.issues if i.is_warn)
    def add(self, issue: LoadIssue) -> None: self.issues.append(issue)
    def extend(self, issues: Iterable[LoadIssue]) -> None: self.issues.extend(list(issues))


def _json_compact(obj: Any) -> str:
    if not obj:
        return "[]" if isinstance(obj, list) else "{}"
    try:
        return json.dumps(obj, ensure_ascii=False)
    except (TypeError, ValueError):
        return "[]"


def load_database_folder(folder: str | Path, strict: bool = False) -> Tuple[pd.DataFrame, LoadReport]:
    folder_path = Path(folder)
    if not folder_path.is_dir():
        if strict: raise ValueError(f"Folder not found: {folder_path}")
        return pd.DataFrame(), LoadReport(str(folder), 0, 0, 0, 0)

    json_files = sorted(folder_path.rglob("*.json"))
    report = LoadReport(str(folder), len(json_files), 0, 0, 0)
    
    rows = []
    
    for file in json_files:
        try:
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            report.add(LoadIssue.error(file.name, f"JSON parse error: {e}"))
            if strict: raise ValueError(f"Error parsing {file}: {e}")
            continue
            
        if file.name == "taxonomy.json" or file.name.startswith("taxonomy"):
            continue

        if isinstance(data, dict) and "universities" in data:
            data = data["universities"]

        if not isinstance(data, list):
            data = [data]
            
        report.files_loaded += 1
        
        for i, entry in enumerate(data):
            report.records_seen += 1
            
            # Intercept new 14-profile schema without Pydantic validation
            if "eligibility_profile" in entry and "cost_profile" in entry:
                if not entry.get("eligibility_profile", {}).get("eligible_for_non_eu", True):
                    report.add(LoadIssue.warn(file.name, "Skipped record due to non-EU ineligibility", record_index=i, record_id=entry.get("id")))
                    continue
                
                cat_prof = entry.get("category_profile", {})
                categories = cat_prof.get("primary_categories", []) + cat_prof.get("secondary_categories", [])
                
                tuit_eur = entry.get("cost_profile", {}).get("tuition_eur_per_year_estimated", 0.0)
                
                row = {
                    "id": entry.get("id", ""),
                    "name": entry.get("university", ""),
                    "display_name": entry.get("university_native_name") or entry.get("university", ""),
                    "short": "",
                    "university": entry.get("university", ""),
                    "city": entry.get("city", ""),
                    "state": entry.get("region", ""),
                    "country": entry.get("country", ""),
                    "scope": "non_eu",
                    "needs_verification": entry.get("source_profile", {}).get("needs_verification", False),
                    "cost_city": entry.get("living_profile", {}).get("city_cost_level", ""),
                    "cost_city_raw": entry.get("living_profile", {}).get("city_cost_level", ""),
                    "city_cost_rank": 0.0,
                    "semester_fee_eur": entry.get("cost_profile", {}).get("enrollment_fee_eur"),
                    "semester_fees_json": "[]",
                    "tuition_eur_per_year": tuit_eur,
                    "annual_fee_eur": tuit_eur,
                    "tuition_raw": str(tuit_eur),
                    "tuition_program": "",
                    "tuition_period": "year",
                    "tuition_scope": "non_eu",
                    "tuition_json": "[]",
                    "aerospace_ecosystem": entry.get("industry_ecosystem_profile", {}).get("ecosystem_notes", ""),
                    "strong_areas_summary": entry.get("research_profile", {}).get("research_strength_summary", ""),
                    "strength": entry.get("research_profile", {}).get("research_strength_summary", ""),
                    "focus": ", ".join(categories),
                    "pros": entry.get("decision_summary", {}).get("main_strengths", []),
                    "cons": entry.get("decision_summary", {}).get("main_risks", []),
                    "tags": categories,
                    "tags_raw": ", ".join(categories),
                    "target_program_name": entry.get("program_name", ""),
                    "target_program_degree": entry.get("program_degree", ""),
                    "target_program_ects": entry.get("ects"),
                    "target_program_url": entry.get("program_url", ""),
                    "target_program_json": "{}",
                    "admission_mode": entry.get("eligibility_profile", {}).get("admission_mode", ""),
                    "language_req": entry.get("language_profile", {}).get("english_level_required", ""),
                    "internship_mandatory": entry.get("curriculum_profile", {}).get("internship_required", False),
                    "internship_notes": "",
                    "deadline_winter_opens": "",
                    "deadline_winter_closes": entry.get("application_timeline_profile", {}).get("non_eu_deadline", ""),
                    "deadline_summer_opens": "",
                    "deadline_summer_closes": "",
                    "deadlines_note": "",
                    "deadlines_json": "{}",
                    "housing_difficulty": entry.get("living_profile", {}).get("housing_difficulty", ""),
                    "housing_difficulty_score": 0.0,
                    "key_partners": entry.get("industry_ecosystem_profile", {}).get("nearby_companies", []),
                    "industry_focus_json": "{}",
                    "logistics_json": "{}",
                    "admission_details_json": "{}",
                    "scholarship_names": entry.get("scholarship_profile", {}).get("regional_scholarship_name", ""),
                    "scholarships_json": "[]",
                    "sources_json": "[]",
                    "qs_ranking": None,
                    "global_recognition": "",
                    "field_recognition": "",
                    "source_file": file.name,
                    "updated_at": entry.get("source_profile", {}).get("last_verified", "")
                }
                
                # Dynamic scoring inputs directly mapped from new schema
                scoring_inputs = entry.get("scoring_inputs", {})
                if scoring_inputs:
                    row["_scoring_inputs"] = scoring_inputs
                    
                rows.append(row)
                report.records_loaded += 1
                continue

            try:
                model = UniversityRecord.model_validate(entry)
            except ValidationError as e:
                report.add(LoadIssue.error(file.name, f"Pydantic Validation Error: {e}", record_index=i))
                if strict: raise
                continue
                
            # Filter non-eu scope
            if model.Program_Scope and model.Program_Scope.lower() not in ["non_eu", "non-eu", "noneu"]:
                report.add(LoadIssue.warn(file.name, f"Skipped record due to scope: {model.Program_Scope}", record_index=i, record_id=model.Uni_ID))
                continue
                
            dump = model.model_dump(exclude_none=False)
            
            # Extract main tuition float value heuristically for sorting
            tuition_eur = 0.0
            if model.Cost_Tuition and len(model.Cost_Tuition) > 0:
                t = model.Cost_Tuition[0]
                if t.amount:
                    tuition_eur = t.amount
                    if t.period == "semester":
                        tuition_eur *= 2  # Approx per year
                        
            # Map Pydantic model back to the EXACT DataFrame columns the UI expects
            row = {
                "id": model.Uni_ID,
                "name": model.University_Name,
                "display_name": model.University_Display_Name or model.University_Name,
                "short": model.University_Short_Name or "",
                "university": model.University_Display_Name or model.University_Name,
                "city": model.City,
                "state": model.State_Region or "",
                "country": model.Country,
                
                "scope": model.Program_Scope,
                "needs_verification": model.Meta_Needs_Verification or False,
                
                "cost_city": model.Cost_City_Living or "",
                "cost_city_raw": model.Cost_City_Living or "",
                "city_cost_rank": model.Cost_City_Rank,
                
                "semester_fee_eur": model.Cost_Semester_Fees[0].amount if model.Cost_Semester_Fees and model.Cost_Semester_Fees[0].amount else None,
                "semester_fees_json": _json_compact(dump.get("Cost_Semester_Fees", [])),
                
                "tuition_eur_per_year": tuition_eur,
                "annual_fee_eur": (
                    (model.Cost_Semester_Fees[0].amount * 2 if model.Cost_Semester_Fees and model.Cost_Semester_Fees[0].amount else 0.0)
                    + tuition_eur
                ) if ((model.Cost_Semester_Fees and model.Cost_Semester_Fees[0].amount) or tuition_eur > 0) else None,
                "tuition_raw": model.Cost_Tuition[0].raw if model.Cost_Tuition else "",
                "tuition_program": model.Cost_Tuition[0].program if model.Cost_Tuition else "",
                "tuition_period": model.Cost_Tuition[0].period if model.Cost_Tuition else "",
                "tuition_scope": model.Cost_Tuition[0].scope if model.Cost_Tuition else "",
                "tuition_json": _json_compact(dump.get("Cost_Tuition", [])),
                
                "aerospace_ecosystem": model.Industry_Ecosystem or "",
                "strong_areas_summary": model.Analysis_Strong_Areas or "",
                "strength": model.Analysis_Strong_Areas or "",
                "focus": ", ".join(model.Analysis_Tags),
                "pros": model.Analysis_Pros,
                "cons": model.Analysis_Cons,
                "tags": model.Analysis_Tags,
                "tags_raw": ", ".join(model.Analysis_Tags),
                
                "target_program_name": model.Program_Name or "",
                "target_program_degree": model.Program_Degree or "",
                "target_program_ects": model.Program_ECTS,
                "target_program_url": model.Program_URL or "",
                "target_program_json": _json_compact({
                    "name": model.Program_Name,
                    "degree": model.Program_Degree,
                    "ects": model.Program_ECTS,
                    "url": model.Program_URL
                }),
                
                "admission_mode": model.Admission_Mode or "",
                "language_req": model.Admission_Language_Req or "",
                
                "internship_mandatory": model.Internship_Mandatory or False,
                "internship_notes": model.Internship_Notes or "",
                
                "deadline_winter_opens": model.Deadline_Winter_Open or "",
                "deadline_winter_closes": model.Deadline_Winter_Close or "",
                "deadline_summer_opens": model.Deadline_Summer_Open or "",
                "deadline_summer_closes": model.Deadline_Summer_Close or "",
                "deadlines_note": model.Deadline_General_Note or "",
                "deadlines_json": _json_compact({
                    "winter": {
                        "opens": model.Deadline_Winter_Open,
                        "closes": model.Deadline_Winter_Close,
                        "note": model.Deadline_Winter_Note
                    },
                    "summer": {
                        "opens": model.Deadline_Summer_Open,
                        "closes": model.Deadline_Summer_Close,
                        "note": model.Deadline_Summer_Note
                    },
                    "note": model.Deadline_General_Note
                }),
                
                "housing_difficulty": model.Living_Housing_Difficulty or "",
                "housing_difficulty_score": model.Living_Housing_Score,
                "key_partners": model.Industry_Partners,
                "industry_focus_json": _json_compact({"computational_intensity": model.Industry_Comp_Intensity}),
                "logistics_json": _json_compact({
                    "housing_difficulty": model.Living_Housing_Difficulty,
                    "housing_difficulty_score": model.Living_Housing_Score,
                    "internship_mandatory": model.Internship_Mandatory,
                    "internship_notes": model.Internship_Notes
                }),
                "admission_details_json": "{}",
                
                "scholarship_names": ", ".join([s.name for s in model.Scholarships_Info if s.name]),
                "scholarships_json": _json_compact(dump.get("Scholarships_Info", [])),
                "sources_json": _json_compact(model.Meta_Sources),
                
                "qs_ranking": model.qs_ranking,
                "global_recognition": model.global_recognition,
                "field_recognition": model.field_recognition,

                "source_file": file.name,
                "updated_at": model.Meta_Updated_At or ""
            }
            rows.append(row)
            report.records_loaded += 1
            
    df = pd.DataFrame(rows)
    
    # Check if empty
    if df.empty:
        # Guarantee columns exist to prevent KeyError downstream
        cols = [
            "id", "name", "display_name", "short", "university", "city", "state", "country",
            "scope", "needs_verification", "cost_city", "cost_city_raw", "city_cost_rank",
            "semester_fee_eur", "semester_fees_json", "tuition_eur_per_year", "tuition_raw",
            "tuition_program", "tuition_period", "tuition_scope", "tuition_json",
            "aerospace_ecosystem", "strong_areas_summary", "strength", "focus", "pros", "cons",
            "tags", "tags_raw", "target_program_name", "target_program_degree", "target_program_ects",
            "target_program_url", "target_program_json", "admission_mode", "language_req",
            "internship_mandatory", "internship_notes", "deadline_winter_opens", "deadline_winter_closes",
            "deadline_summer_opens", "deadline_summer_closes", "deadlines_note", "deadlines_json",
            "housing_difficulty", "housing_difficulty_score", "key_partners", "industry_focus_json",
            "logistics_json", "admission_details_json", "scholarship_names", "scholarships_json",
            "sources_json", "qs_ranking", "global_recognition", "field_recognition", "source_file", "updated_at"
        ]
        df = pd.DataFrame(columns=cols)
        
    return df, report

def load_database(path: str | Path, strict: bool = False, include_siblings_if_file: bool = True) -> Tuple[pd.DataFrame, LoadReport]:
    return load_database_folder(path, strict)
