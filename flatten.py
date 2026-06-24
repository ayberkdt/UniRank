import json
import re

def fix_encoding(text: str) -> str:
    if not isinstance(text, str):
        return text
    replacements = {
        "MǬnih": "Münih",
        "gǬlǬ": "güçlü",
        "araYtrma": "araştırma",
        "dǬYǬk": "düşük",
        "bǬyǬk": "büyük",
        "yǬksek": "yüksek",
        "kǬǬk": "küçük",
        "": "ü",
        "'": "€",
        "%^'": "~€",
        "?ts": "'s",
        "?'": "-",
        "?\"": "-",
        "?o": '"',
        "??": '"',
        "?~": "-",
        "C": "°C",
        "Y": "ş",
        "Ǭ": "ü",
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    text = text.replace("\ufffd", "ü") # Usually ü or ö, let's just use ü. 
    # Let's fix specific common ones like "Politcnica", "Valncia", "Autnoma", "Pas", "Lule", "Ume", "rebro", "Mlardalen"
    text = text.replace("Politücnica", "Politècnica")
    text = text.replace("Valüncia", "València")
    text = text.replace("Autünoma", "Autònoma")
    text = text.replace("Paüs", "País")
    text = text.replace("Luleü", "Luleå")
    text = text.replace("Umeü", "Umeå")
    text = text.replace("ürebro", "Örebro")
    text = text.replace("Mülardalen", "Mälardalen")
    
    return text

def fix_dict_encoding(obj):
    if isinstance(obj, str):
        return fix_encoding(obj)
    elif isinstance(obj, list):
        return [fix_dict_encoding(x) for x in obj]
    elif isinstance(obj, dict):
        return {k: fix_dict_encoding(v) for k, v in obj.items()}
    return obj

def transform_record(row):
    def safe_json(val):
        if val is None:
            return []
        return val

    # Convert tuition list
    tuition = safe_json(row.get("tuition", []))
    sem_fees = safe_json(row.get("semester_fees", []))
    schol = safe_json(row.get("scholarships", []))
    
    deadlines = row.get("deadlines", {})
    winter = deadlines.get("winter", {})
    summer = deadlines.get("summer", {})
    
    industry_focus = row.get("industry_focus", {})
    logistics = row.get("logistics", {})
    target_program = row.get("target_program", {})
    location = row.get("location", {})
    
    rec = {
        "Country": location.get("country", ""),
        "City": location.get("city", ""),
        "State_Region": location.get("state", ""),
        "Uni_ID": row.get("id", ""),
        "University_Name": row.get("name", ""),
        "University_Display_Name": row.get("display_name", ""),
        "University_Short_Name": row.get("short", ""),
        
        "Cost_Tuition": tuition,
        "Cost_Semester_Fees": sem_fees,
        "Scholarships_Info": schol,
        
        "Cost_City_Living": row.get("city_cost", ""),
        "Cost_City_Rank": row.get("city_cost_rank", None),
        
        "Living_Housing_Difficulty": row.get("housing_difficulty", ""),
        "Living_Housing_Score": row.get("housing_difficulty_score", None),
        
        "Program_Name": target_program.get("name", ""),
        "Program_Degree": target_program.get("degree", ""),
        "Program_ECTS": target_program.get("ects", None),
        "Program_URL": target_program.get("url", ""),
        "Program_Scope": row.get("scope", "non_eu"),
        
        "Admission_Mode": row.get("admission_mode", ""),
        "Admission_Language_Req": row.get("language_req", ""),
        
        "Analysis_Strong_Areas": row.get("strong_areas_summary", ""),
        "Analysis_Pros": row.get("pros", []),
        "Analysis_Cons": row.get("cons", []),
        "Analysis_Tags": row.get("tags", []),
        
        "Industry_Ecosystem": row.get("aerospace_ecosystem", ""),
        "Industry_Comp_Intensity": industry_focus.get("computational_intensity", ""),
        "Industry_Partners": row.get("key_partners", []),
        
        "Internship_Mandatory": logistics.get("internship_mandatory", False),
        "Internship_Notes": logistics.get("internship_notes", ""),
        
        "Deadline_Winter_Open": winter.get("opens", None),
        "Deadline_Winter_Close": winter.get("closes", None),
        "Deadline_Winter_Note": winter.get("source_note", None),
        "Deadline_Summer_Open": summer.get("opens", None),
        "Deadline_Summer_Close": summer.get("closes", None),
        "Deadline_Summer_Note": summer.get("source_note", None),
        "Deadline_Summer_Avail": summer.get("availability_note", None),
        "Deadline_General_Note": deadlines.get("note", None),
        
        "Meta_Sources": row.get("sources", []),
        "Meta_Updated_At": row.get("updated_at", ""),
        "Meta_Needs_Verification": row.get("needs_verification", False)
    }
    
    return fix_dict_encoding(rec)

files = ["data_base/ispanya.json", "data_base/isvec.json"]
for fpath in files:
    with open(fpath, "r", encoding="utf-8") as f:
        data = json.load(f)
    new_data = [transform_record(row) for row in data]
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(new_data, f, ensure_ascii=False, indent=4)
print("Done.")
