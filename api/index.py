from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import sys
import os
from pathlib import Path
import pandas as pd
import numpy as np

# In Vercel, the root directory is automatically in PYTHONPATH.
# Do NOT use sys.path.append dynamically because it breaks Vercel's static analysis bundle.
from unirank.core.json_loader import load_database_folder

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
        
        records = df.to_dict(orient="records")
        return JSONResponse(
            {"status": "success", "data": records, "report": {"files_loaded": report.files_loaded}},
            headers=headers
        )
    except Exception as e:
        return JSONResponse(
            {"status": "error", "message": f"Python Error: {str(e)}", "data": []},
            headers=headers
        )

@app.get("/api/taxonomy")
def get_taxonomy():
    import json
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
    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)})
