import sys
from pathlib import Path
sys.path.insert(0, str(Path("c:/Users/ayber/Desktop/Custom Apps/UniRank").resolve()))
from unirank.core.json_loader import load_database_folder

df, report = load_database_folder("c:/Users/ayber/Desktop/Custom Apps/UniRank/data_base", strict=False)
print("Records Loaded:", report.records_loaded)
print("Errors:", [str(e) for e in report.issues if e.is_error])
print("Warnings:", len([w for w in report.issues if w.is_warn]))
if not df.empty:
    print("Countries in DataFrame:", df["country"].unique())
    print("Records per country:\n", df["country"].value_counts())

