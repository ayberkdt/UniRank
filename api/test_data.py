import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from unirank.core.json_loader import load_database_folder

db_path = Path(__file__).parent.parent / "data_base"
try:
    df, report = load_database_folder(db_path, strict=False)
    print(f"Loaded {report.files_loaded} files.")
    if df is None or df.empty:
        print("DF is empty")
    else:
        print(f"Rows: {len(df)}")
        df = df.where(df.notnull(), None)
        records = df.to_dict(orient="records")
        print(f"First record: {records[0]}")
except Exception as e:
    print(f"Error: {e}")
