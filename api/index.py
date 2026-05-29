from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import sys
import os
from pathlib import Path
import numpy as np

# Add root to sys.path so 'unirank' can be imported robustly on Vercel
sys.path.append(os.getcwd())

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
    # In Vercel serverless functions, the current working directory is the project root
    db_path = Path(os.getcwd()) / "data_base"
    
    try:
        df, report = load_database_folder(db_path, strict=False)
        if df is None or df.empty:
            # Check if directory exists to provide better error messages
            if not db_path.exists():
                return JSONResponse({"status": "error", "message": f"Database directory {db_path} does not exist.", "data": []})
            return JSONResponse({"status": "error", "message": f"No valid data found. Files loaded: {report.files_loaded}", "data": []})
        
        # Replace NaNs with None for safe JSON serialization
        df = df.replace({np.nan: None})
        
        records = df.to_dict(orient="records")
        return JSONResponse({"status": "success", "data": records, "report": {"files_loaded": report.files_loaded}})
    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e), "data": []})
