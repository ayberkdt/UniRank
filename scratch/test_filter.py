import sys
from pathlib import Path
sys.path.insert(0, str(Path("c:/Users/ayber/Desktop/Custom Apps/UniRank").resolve()))
from unirank.core.json_loader import load_database_folder
from unirank.core.scoring import calculate_score

df, report = load_database_folder("c:/Users/ayber/Desktop/Custom Apps/UniRank/data_base", strict=False)
records = df.to_dict('records')

preferences = {
    "selectedKeywords": [],
    "degreeFilter": "All",
    "onlyEnglish": False,
    "maxTuition": 0,
    "minFieldFit": 0
}

weights = {
    "academic_fit": 30,
    "eligibility_language": 20,
    "cost_funding": 20,
    "career_research": 15,
    "living_risk": 10,
    "confidence_deadline": 5
}

passed_count = 0
for r in records:
    score = calculate_score(r, preferences, weights)
    if score['passed_hard_filters']:
        passed_count += 1

print(f"Total records: {len(records)}")
print(f"Passed filters: {passed_count}")
