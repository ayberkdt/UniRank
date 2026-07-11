import json
import os

with open("data_base/belcika.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for row in data:
    if row["Uni_ID"] == "ku-leuven":
        # Update KU Leuven Master of Space Studies
        # Deadlines
        row["Deadline_Winter_Open"] = "2024-11-01"
        row["Deadline_Winter_Close"] = "2025-03-01" # non-EEA
        row["Deadline_Winter_Note"] = "1 March for non-EEA, 1 June for EEA citizens."
        
        # Cost (We searched and found variable advanced master fee, null out and note)
        row["cost_profile"]["tuition_eur_per_year_estimated"] = None
        row["cost_profile"]["tuition_basis"] = "variable"
        row["cost_profile"]["verification_notes"] = "Tuition is variable (Advanced Master). Use official KU Leuven Tuition Fee calculator."
        
        row["Meta_Updated_At"] = "2026-07-12"
        row["Meta_Needs_Verification"] = False
        
        row["program_status"] = "active"
        
        # teaching_language
        row["language_profile"]["teaching_language"] = ["English"]
        row["teaching_language"] = ["English"]
        
    elif row["Uni_ID"] == "uliege":
        # Update ULiège Aerospace Engineering
        row["Program_Name"] = "Master in Aerospace Engineering"
        row["program_name"] = "Master in Aerospace Engineering"
        
        # Deadlines
        row["Deadline_Winter_Close"] = "2025-03-31"
        row["Deadline_Winter_Note"] = "March 31 for non-EU applicants."
        
        # Cost
        row["cost_profile"]["tuition_eur_per_year_estimated"] = 5369
        row["cost_profile"]["tuition_basis"] = "5369 EUR/year for non-EU (1194 + 4175 contribution)"
        row["cost_profile"]["verification_notes"] = "Verified 2025/2026 fee: 1194 base + 4175 non-EU contribution."
        
        row["program_degree"] = "MSc"
        row["degree_level"] = "Master"
        row["duration_years"] = 2
        row["ects"] = 120
        row["program_url"] = "https://www.uliege.be/"
        
        row["language_profile"]["teaching_language"] = ["English"]
        row["teaching_language"] = ["English"]

        row["Meta_Updated_At"] = "2026-07-12"
        row["Meta_Needs_Verification"] = False
        row["program_status"] = "active"

with open("data_base/belcika.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
