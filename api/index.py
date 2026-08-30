from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import sys
import os
from pathlib import Path
import json
import pandas as pd
import numpy as np

# In Vercel, the root directory is automatically in PYTHONPATH.
# Do NOT use sys.path.append dynamically because it breaks Vercel's static analysis bundle.
from unirank.core.json_loader import load_database_folder


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


def _project_file(*parts):
    candidates = [
        Path(os.getcwd()).joinpath(*parts),
        Path(__file__).parent.parent.joinpath(*parts),
        Path("/var/task").joinpath(*parts),
    ]
    return next((path for path in candidates if path.exists() and path.is_file()), None)

@app.get("/api/universities")
def get_universities():
    # In Vercel serverless functions, the directory structure can be tricky
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

    headers = {"Cache-Control": "no-store, no-cache, must-revalidate, max-age=0"}

    if not db_path:
        searched = [str(p) for p in possible_paths]
        return JSONResponse(
            {"status": "error", "message": f"Database directory not found. Searched: {searched}", "data": []},
            headers=headers
        )
    
    try:
        df, report = load_database_folder(db_path, strict=False)
        if df is None or df.empty:
            return JSONResponse(
                {"status": "error", "message": f"No valid data found in {db_path}. Files loaded: {report.files_loaded}", "data": []},
                headers=headers
            )
        
        # Replace NaNs with None for safe JSON serialization
        df = df.replace({np.nan: None})
        
        records = _json_safe(df.to_dict(orient="records"))
        return JSONResponse(
            {"status": "success", "data": records, "report": {"files_loaded": report.files_loaded}},
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
