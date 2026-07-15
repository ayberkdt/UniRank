from __future__ import annotations
import json
import re
from pathlib import Path
import pandas as pd
from typing import Any, Dict, List, Optional, Tuple, Iterable
from dataclasses import dataclass, field
from pydantic import ValidationError

from unirank.core.schema import UniversityRecord
from unirank.core.integrity import apply_integrity_gate

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


def _city_name(value: Any) -> str:
    """Return a displayable city name without discarding the original record."""
    if isinstance(value, dict):
        for key in ("name", "city", "City", "label"):
            candidate = value.get(key)
            if isinstance(candidate, str) and candidate.strip():
                return candidate.strip()
        return ""
    return value.strip() if isinstance(value, str) else ""


def _identity_text(value: Any) -> str:
    """Normalize a display value for exact programme-duplicate detection.

    The key deliberately includes the programme and degree.  A university can
    legitimately have several programmes, so institution-only de-duplication
    would hide real choices from students.
    """
    return re.sub(r"[^a-z0-9]+", " ", str(value or "").lower()).strip()


def _programme_identity(row: Dict[str, Any]) -> tuple[str, str, str, str]:
    return (
        _identity_text(row.get("country")),
        _identity_text(row.get("university") or row.get("name")),
        _identity_text(row.get("program_name") or row.get("target_program_name")),
        _identity_text(row.get("degree_level") or row.get("program_degree") or row.get("target_program_degree")),
    )


def _is_undergraduate_programme(row: Dict[str, Any]) -> bool:
    """Exclude first-cycle choices from the Master's decision dataset.

    This is intentionally an exclusion check rather than a guess that every
    unknown degree is a Master's.  It catches explicit Bachelor's/BSc labels
    and direct-entry Diplom programmes, while leaving unverified degree levels
    available for source review instead of silently relabelling them.
    """
    degree_text = " ".join(str(row.get(key) or "") for key in (
        "degree_level", "program_degree", "target_program_degree", "Program_Degree", "degree", "level"
    )).lower()
    return bool(re.search(r"\b(bachelor|b\.\s*sc\.?|bsc|undergraduate|first[- ]cycle|lisans)\b", degree_text)) or (
        "diplom" in degree_text and "direct" in degree_text
    )


def _record_preference(row: Dict[str, Any]) -> tuple[int, int, int, str]:
    """Prefer the most complete source-grounded representation of one programme."""
    quality = row.get("data_quality") or {}
    status = str(quality.get("status") or "").lower()
    status_rank = {"verified": 3, "partial": 2, "needs_verification": 1}.get(status, 0)
    verified_count = len(quality.get("verified_fields") or [])
    source_count = len((row.get("source_profile") or {}).get("source_log") or [])
    return status_rank, verified_count, source_count, str(row.get("updated_at") or "")


def _deduplicate_programme_rows(rows: List[Dict[str, Any]], report: LoadReport) -> List[Dict[str, Any]]:
    """Keep one record only for an exact country/university/programme/degree clone."""
    grouped: Dict[tuple[str, str, str, str], List[Dict[str, Any]]] = {}
    for row in rows:
        if _is_undergraduate_programme(row):
            report.add(LoadIssue.warn(
                str(row.get("source_file") or "data_base"),
                "Suppressed undergraduate programme from the Master's-only dataset.",
                record_id=str(row.get("id") or "") or None,
            ))
            continue
        key = _programme_identity(row)
        # Do not merge incomplete legacy rows that lack the identifying fields.
        if not all(key):
            key = (*key, str(row.get("id") or ""))
        grouped.setdefault(key, []).append(row)

    unique: List[Dict[str, Any]] = []
    for group in grouped.values():
        selected = max(group, key=_record_preference)
        unique.append(selected)
        if len(group) > 1:
            dropped = [str(row.get("id") or "unknown") for row in group if row is not selected]
            report.add(LoadIssue.warn(
                str(selected.get("source_file") or "data_base"),
                f"Suppressed exact duplicate programme record(s): {', '.join(dropped)}; retained {selected.get('id') or 'unknown'}.",
                record_id=str(selected.get("id") or "") or None,
            ))
    return unique


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

        if isinstance(data, dict):
            if "universities" in data:
                data = data["universities"]
            elif "programs" in data:
                data = data["programs"]

        if not isinstance(data, list):
            data = [data]
            
        report.files_loaded += 1
        
        for i, entry in enumerate(data):
            report.records_seen += 1
            
            # Intercept new 14-profile schema without Pydantic validation
            if "eligibility_profile" in entry and "cost_profile" in entry:
                # Candidate records are useful for discovery, but costs,
                # language and other high-stakes fields must be source-safe
                # before reaching any UI or scoring path.
                entry = apply_integrity_gate(entry)
                # Unknown eligibility must remain visible and be marked for
                # verification; only an explicit official false excludes a row.
                if entry.get("eligibility_profile", {}).get("eligible_for_non_eu", True) is False:
                    report.add(LoadIssue.warn(file.name, "Skipped record due to non-EU ineligibility", record_index=i, record_id=entry.get("id")))
                    continue
                
                cat_prof = entry.get("category_profile", {})
                language_profile = entry.get("language_profile", {})
                cost_profile = entry.get("cost_profile", {})
                living_profile = entry.get("living_profile", {})
                source_profile = entry.get("source_profile", {})
                categories = cat_prof.get("primary_categories", []) + cat_prof.get("secondary_categories", [])
                
                tuit_eur = cost_profile.get("tuition_eur_per_year_estimated")
                
                row = {
                    "id": entry.get("id", ""),
                    "name": entry.get("university", ""),
                    "display_name": entry.get("university_native_name") or entry.get("university", ""),
                    "short": "",
                    "university": entry.get("university", ""),
                    "city": _city_name(entry.get("city", "")),
                    "state": entry.get("region", ""),
                    "country": entry.get("country", ""),
                    # Keep the source location object intact for map consumers.
                    # The web API serializes this DataFrame row, so dropping it
                    # here makes every otherwise valid coordinate disappear.
                    "location": entry.get("location"),
                    "scope": "non_eu",
                    "needs_verification": source_profile.get("needs_verification", False),
                    "cost_city": living_profile.get("cost_city_living") or living_profile.get("city_cost_level", ""),
                    "cost_city_raw": living_profile.get("cost_city_living") or living_profile.get("city_cost_level", ""),
                    "city_cost_rank": 0.0,
                    "semester_fee_eur": cost_profile.get("enrollment_fee_eur"),
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
                    "language_req": language_profile.get("english_level_required", ""),
                    "internship_mandatory": entry.get("curriculum_profile", {}).get("internship_required", False),
                    "internship_notes": "",
                    "deadline_winter_opens": "",
                    "deadline_winter_closes": entry.get("application_timeline_profile", {}).get("non_eu_deadline", ""),
                    "deadline_summer_opens": "",
                    "deadline_summer_closes": "",
                    "deadlines_note": "",
                    "deadlines_json": "{}",
                    "housing_difficulty": living_profile.get("housing_difficulty", ""),
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
                    "updated_at": source_profile.get("last_verified", ""),
                    "program_name": entry.get("program_name", ""),
                    "program_degree": entry.get("program_degree", ""),
                    "degree_level": entry.get("degree_level", ""),
                    "duration_years": entry.get("duration_years"),
                    "ects": entry.get("ects"),
                    "teaching_language": entry.get("teaching_language") or language_profile.get("teaching_language", []),
                    "program_url": entry.get("program_url", ""),
                    "program_status": entry.get("program_status", ""),
                    "eligibility_profile": entry.get("eligibility_profile", {}),
                    "language_profile": language_profile,
                    "cost_profile": cost_profile,
                    "scholarship_profile": entry.get("scholarship_profile", {}),
                    "living_profile": living_profile,
                    "curriculum_profile": entry.get("curriculum_profile", {}),
                    "category_profile": cat_prof,
                    "research_profile": entry.get("research_profile", {}),
                    "industry_ecosystem_profile": entry.get("industry_ecosystem_profile", {}),
                    "application_timeline_profile": entry.get("application_timeline_profile", {}),
                    "student_sentiment_profile": entry.get("student_sentiment_profile", {}),
                    "source_profile": source_profile,
                    "decision_summary": entry.get("decision_summary", {}),
                    "scoring_inputs": entry.get("scoring_inputs", {}),
                    "quality_control": entry.get("quality_control", {}),
                    "data_quality": entry.get("data_quality", {}),
                    "urls": entry.get("urls", {}),
                    "financials": entry.get("financials", {}),
                    "admission": entry.get("admission", {})
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
            integrity = apply_integrity_gate(entry)
            quality = integrity.get("data_quality", {})
            
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
                # Legacy records may also carry a location object even though
                # the Pydantic compatibility model intentionally ignores it.
                "location": entry.get("location"),
                
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
            # Legacy records cannot establish a checked field source merely by
            # carrying a URL.  Keep them searchable as candidates while
            # suppressing unsupported decision values in the public payload.
            if "tuition" not in quality.get("verified_fields", []):
                row["tuition_eur_per_year"] = None
                row["annual_fee_eur"] = None
                row["semester_fee_eur"] = None
            if "language" not in quality.get("verified_fields", []):
                row["language_req"] = ""
            if "deadline" not in quality.get("verified_fields", []):
                row["deadline_winter_closes"] = ""
                row["deadline_summer_closes"] = ""
                row["deadlines_note"] = ""
            row["needs_verification"] = True
            row["source_profile"] = integrity.get("source_profile", {})
            row["student_sentiment_profile"] = integrity.get("student_sentiment_profile", {})
            row["data_quality"] = quality
            rows.append(row)
            report.records_loaded += 1
            
    rows = _deduplicate_programme_rows(rows, report)
    report.records_loaded = len(rows)
    df = pd.DataFrame(rows)
    
    # Check if empty
    if df.empty:
        # Guarantee columns exist to prevent KeyError downstream
        cols = [
            "id", "name", "display_name", "short", "university", "city", "state", "country", "location",
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
