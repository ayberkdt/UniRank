from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.gzip import GZipMiddleware
from functools import lru_cache
import sys
import os
from pathlib import Path
import json
import pandas as pd
import numpy as np

# In Vercel, the root directory is automatically in PYTHONPATH.
# Do NOT use sys.path.append dynamically because it breaks Vercel's static analysis bundle.
from unirank.core.json_loader import load_database_folder


FEATURED_RESEARCH_PROGRAM_IDS = [
    "mit-aeroastro",
    "stanford-aa",
    "caltech-galcit",
    "university-of-cambridge",
    "imperial-college-london",
    "netherlands_delft_msc_aerospace",
    "se-kth-aero-msc",
    "germany-tum-msc-aerospace",
    "germany-stuttgart-msc-aerospace",
    "purdue-aae",
    "uiuc-ae",
    "georgia-tech-ae",
    "umich-aero",
]


def _json_safe(value):
    if isinstance(value, dict):
        return {key: _json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(item) for item in value]
    if isinstance(value, np.generic):
        value = value.item()
    if value is pd.NA or value is pd.NaT:
        return None
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if isinstance(value, float) and np.isnan(value):
        return None
    return value

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=1024, compresslevel=6)


def _project_file(*parts):
    candidates = [
        Path(os.getcwd()).joinpath(*parts),
        Path(__file__).parent.parent.joinpath(*parts),
        Path("/var/task").joinpath(*parts),
    ]
    return next((path for path in candidates if path.exists() and path.is_file()), None)


def _database_directory():
    candidates = [
        Path(os.getcwd()) / "data_base",
        Path(__file__).parent.parent / "data_base",
        Path("/var/task/data_base"),
    ]
    return next((path for path in candidates if path.exists() and path.is_dir()), None)


@lru_cache(maxsize=1)
def _database_bundle():
    """Load and normalize the programme database once per server process.

    The catalogues remain useful editorial entry points, but scholarship
    playbooks and faculty/lab evidence live on programme records.  Loading the
    same canonical rows as /api/universities keeps those pages from drifting
    into separate, manually copied databases.
    """
    database_path = _database_directory()
    if not database_path:
        return [], {"files_loaded": 0}
    dataframe, report = load_database_folder(database_path, strict=False)
    if dataframe is None or dataframe.empty:
        return [], {"files_loaded": report.files_loaded}
    dataframe = dataframe.replace({np.nan: None})
    records = _json_safe(dataframe.to_dict(orient="records"))
    return records, {"files_loaded": report.files_loaded}


def _database_records():
    return _database_bundle()[0]


def _latest_verified(current, profiles):
    dates = [current] if isinstance(current, str) else []
    dates.extend(
        profile.get("last_verified")
        for profile in profiles
        if isinstance(profile.get("last_verified"), str)
    )
    return max(dates) if dates else None


def _official_source_count(catalog_sources, records, relevant_terms):
    urls = {
        source.get("url")
        for source in catalog_sources or []
        if isinstance(source, dict) and source.get("url")
    }
    accepted_statuses = {"ok", "redirects", "pdf", "requires_js"}
    for record in records:
        source_profile = record.get("source_profile") or {}
        for source in source_profile.get("source_log") or []:
            if not isinstance(source, dict) or not str(source.get("source_type", "")).startswith("official_"):
                continue
            if source.get("access_status") not in accepted_statuses or not source.get("url"):
                continue
            fields = " ".join(str(field).lower() for field in source.get("relevant_fields") or [])
            if any(term in fields for term in relevant_terms):
                urls.add(source["url"])
    return len(urls)


def _programme_identity(record):
    return {
        "programme_id": record.get("id") or record.get("Uni_ID"),
        "university": record.get("University") or record.get("university") or "",
        "programme": record.get("program_name") or record.get("Program") or record.get("programme_name") or "",
        "country": record.get("country") or record.get("Country") or "",
        "degree_level": record.get("degree_level") or record.get("Degree") or "",
    }


def _institutional_funding(records):
    opportunities = []
    featured_order = {programme_id: index for index, programme_id in enumerate(FEATURED_RESEARCH_PROGRAM_IDS)}
    for record in records:
        profile = record.get("scholarship_profile") or {}
        playbook = profile.get("playbook") or []
        if not isinstance(playbook, list) or not playbook:
            continue
        identity = _programme_identity(record)
        programme_id = identity["programme_id"]
        if not programme_id:
            continue
        source_profile = record.get("source_profile") or {}
        opportunities.append({
            **identity,
            "featured": programme_id in featured_order,
            "application_mode": profile.get("application_mode"),
            "scholarship_deadline": profile.get("scholarship_deadline"),
            "deadline_notes": profile.get("notes") or profile.get("verification_notes"),
            "funding_status": profile.get("funding_status"),
            "playbook": playbook,
            "last_verified": source_profile.get("last_verified") or record.get("last_verified"),
        })
    opportunities.sort(key=lambda item: (
        0 if item["featured"] else 1,
        featured_order.get(item["programme_id"], 999),
        item["university"],
    ))
    return opportunities


def _programme_research_details(records):
    details = []
    featured_order = {programme_id: index for index, programme_id in enumerate(FEATURED_RESEARCH_PROGRAM_IDS)}
    for record in records:
        profile = record.get("research_profile") or {}
        professors = profile.get("notable_professors") or []
        units = profile.get("research_units") or []
        if not isinstance(professors, list) or not isinstance(units, list) or not (professors or units):
            continue
        identity = _programme_identity(record)
        programme_id = identity["programme_id"]
        if not programme_id:
            continue
        source_profile = record.get("source_profile") or {}
        details.append({
            **identity,
            "featured": programme_id in featured_order,
            "faculty_contact_policy": profile.get("faculty_contact_policy"),
            "faculty_contact_note": profile.get("faculty_contact_note"),
            "faculty_email_availability": profile.get("faculty_email_availability"),
            "notable_professors": professors,
            "research_units": units,
            "verification_notes": profile.get("verification_notes"),
            "last_verified": source_profile.get("last_verified") or record.get("last_verified"),
        })
    details.sort(key=lambda item: (
        0 if item["featured"] else 1,
        featured_order.get(item["programme_id"], 999),
        -(len(item["notable_professors"]) + len(item["research_units"])),
        item["university"],
    ))
    return details

@app.get("/api/universities")
def get_universities(limit: int = None, offset: int = 0):
    # In Vercel serverless functions, the directory structure can be tricky
    db_path = _database_directory()

    headers = {"Cache-Control": "public, max-age=300, stale-while-revalidate=600"}

    if not db_path:
        searched = [
            str(Path(os.getcwd()) / "data_base"),
            str(Path(__file__).parent.parent / "data_base"),
            "/var/task/data_base",
        ]
        return JSONResponse(
            {"status": "error", "message": f"Database directory not found. Searched: {searched}", "data": []},
            headers=headers
        )
    
    try:
        records, report = _database_bundle()
        if not records:
            return JSONResponse(
                {"status": "error", "message": f"No valid data found in {db_path}. Files loaded: {report['files_loaded']}", "data": []},
                headers=headers
            )
        total = len(records)
        start = max(0, offset)
        if limit is None:
            page_records = records[start:]
            page_limit = total
        else:
            page_limit = max(1, min(limit, 100))
            page_records = records[start:start + page_limit]
        next_offset = start + len(page_records)
        return JSONResponse(
            {
                "status": "success",
                "data": page_records,
                "report": report,
                "page": {
                    "offset": start,
                    "limit": page_limit,
                    "returned": len(page_records),
                    "total": total,
                    "has_more": next_offset < total,
                    "next_offset": next_offset if next_offset < total else None,
                },
            },
            headers=headers
        )
    except Exception:
        return JSONResponse(
            {"status": "error", "message": "The university data could not be loaded.", "data": []},
            headers=headers
        )

@app.get("/api/taxonomy")
def get_taxonomy():
    possible_paths = [
        Path(os.getcwd()) / "data_base",
        Path(__file__).parent.parent / "data_base",
        Path("/var/task/data_base")
    ]
    
    db_path = None
    for p in possible_paths:
        if p.exists() and p.is_dir():
            db_path = p
            break
            
    if not db_path:
        return JSONResponse({"status": "error", "message": "Database directory not found"})
        
    tax_path = db_path / "taxonomy.json"
    if not tax_path.exists():
        return JSONResponse({"status": "error", "message": "taxonomy.json not found"})
        
    try:
        with open(tax_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return JSONResponse(data)
    except Exception:
        return JSONResponse({"status": "error", "message": "The taxonomy data could not be loaded."})


@app.get("/api/scholarships")
def get_scholarships():
    catalog_path = _project_file("scholarships", "catalog.json")
    headers = {"Cache-Control": "no-store, no-cache, must-revalidate, max-age=0"}
    if not catalog_path:
        return JSONResponse({"status": "error", "message": "Scholarship catalog not found.", "data": {}}, status_code=404, headers=headers)
    try:
        with open(catalog_path, "r", encoding="utf-8") as catalog_file:
            catalog = json.load(catalog_file)
        records = _database_records()
        opportunities = _institutional_funding(records)
        catalog["institutional_opportunities"] = opportunities
        catalog["last_verified"] = _latest_verified(catalog.get("last_verified"), opportunities)
        return JSONResponse({"status": "success", "data": catalog}, headers=headers)
    except (OSError, json.JSONDecodeError):
        return JSONResponse({"status": "error", "message": "Scholarship catalog could not be loaded.", "data": {}}, status_code=500, headers=headers)


@app.get("/api/research-pathways")
def get_research_pathways():
    catalog_path = _project_file("research_fields", "catalog.json")
    headers = {"Cache-Control": "no-store, no-cache, must-revalidate, max-age=0"}
    if not catalog_path:
        return JSONResponse({"status": "error", "message": "Research pathway catalog not found.", "data": {}}, status_code=404, headers=headers)
    try:
        with open(catalog_path, "r", encoding="utf-8") as catalog_file:
            catalog = json.load(catalog_file)
        records = _database_records()
        details = _programme_research_details(records)
        catalog["programme_research_details"] = details
        catalog["last_verified"] = _latest_verified(catalog.get("last_verified"), details)
        catalog["official_source_count"] = _official_source_count(
            catalog.get("sources"), records, ("research", "faculty", "professor", "lab", "facilit")
        )
        return JSONResponse({"status": "success", "data": catalog}, headers=headers)
    except (OSError, json.JSONDecodeError):
        return JSONResponse({"status": "error", "message": "Research pathway catalog could not be loaded.", "data": {}}, status_code=500, headers=headers)


@app.get("/api/visa-requirements")
def get_visa_requirements():
    """Serve the permit, funds and clearance rules a Turkish applicant faces.

    This was the only decision field with zero coverage: nothing in the
    database said which permit a country issues, how much money has to be
    proven, or which clearances gate the visa.  Those questions sent the
    reader to a search engine at the point where a wrong answer costs an
    application cycle.
    """
    visa_path = _project_file("config", "visa_requirements.json")
    headers = {"Cache-Control": "no-store, no-cache, must-revalidate, max-age=0"}
    if not visa_path:
        return JSONResponse({"status": "error", "message": "Visa requirements file not found.", "data": {}}, status_code=404, headers=headers)
    try:
        with open(visa_path, "r", encoding="utf-8") as visa_file:
            requirements = json.load(visa_file)
        return JSONResponse({"status": "success", "data": requirements}, headers=headers)
    except (OSError, json.JSONDecodeError):
        return JSONResponse({"status": "error", "message": "Visa requirements could not be loaded.", "data": {}}, status_code=500, headers=headers)

@app.get("/api/standards")
def get_standards():
    """Serve the categorical-scale definitions used across the database.

    Every category shown to a student (housing difficulty, cost basis,
    academic-match tier, faculty contact timing, scholarship step timing)
    is defined once in config/standards.json so the interface can explain
    what a label means instead of asserting it.
    """
    standards_path = _project_file("config", "standards.json")
    headers = {"Cache-Control": "no-store, no-cache, must-revalidate, max-age=0"}
    if not standards_path:
        return JSONResponse({"status": "error", "message": "Standards file not found.", "data": {}}, status_code=404, headers=headers)
    try:
        with open(standards_path, "r", encoding="utf-8") as standards_file:
            standards = json.load(standards_file)
        return JSONResponse({"status": "success", "data": standards}, headers=headers)
    except (OSError, json.JSONDecodeError):
        return JSONResponse({"status": "error", "message": "Standards could not be loaded.", "data": {}}, status_code=500, headers=headers)
