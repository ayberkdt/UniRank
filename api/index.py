from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import sys
from pathlib import Path
import os

# Add root to sys.path so 'unirank' can be imported
sys.path.append(str(Path(__file__).parent.parent))

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
    db_path = Path(__file__).parent.parent / "data_base"
    try:
        df, report = load_database_folder(db_path, strict=False)
        if df is None or df.empty:
            return JSONResponse({"status": "error", "message": "No data found", "data": []})
        
        # Replace NaNs with None for JSON serialization
        df = df.where(df.notnull(), None)
        
        # Return records
        records = df.to_dict(orient="records")
        return JSONResponse({"status": "success", "data": records, "report": {"files_loaded": report.files_loaded}})
    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e), "data": []})
