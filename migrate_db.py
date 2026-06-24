import json
import re
from pathlib import Path
from pydantic import ValidationError
from unirank.core.schema import UniversityRecord

# Kapsamlı temizleme szl
REPLACEMENTS = {
    "MǬnih": "Münih",
    "Mnih": "Münih",
    "gǬlǬ": "güçlü",
    "gǬlǬ": "güçlü",
    "gl": "güçlü",
    "araYtrma": "araştırma",
    "araYtrma": "araştırma",
    "dǬYǬk": "düşük",
    "dǬYǬk": "düşük",
    "bǬyǬk": "büyük",
    "yǬksek": "yüksek",
    "kǬǬk": "küçük",
    "kǬǬk": "küçük",
    "geniY": "geniş",
    "yaklaYk": "yaklaşık",
    "yaklaYk": "yaklaşık",
    "iin": "için",
    "iin": "için",
    "alYma": "çalışma",
    "rnek": "örnek",
    "niversite": "üniversite",
    "Yrenci": "öğrenci",
    "cret": "ücret",
    "oY": "çoğu",
    "eYit": "çeşit",
    "zm": "çözüm",
    "Y": "ş",
    "Ǭ": "ü",
    "C": "°C",
    "?ts": "'s",
    "?'": "-",
    "?\"": "-",
    "?o": '"',
    "??": '"',
    "?~": "-",
    "'": "€",
    "%^'": "~€"
}

def clean_text(text: str) -> str:
    if not isinstance(text, str):
        return text
    # Fix currency quote issues manually
    text = re.sub(r"'(\d[\d,\.]*)", r"€\1", text)
    
    for k, v in REPLACEMENTS.items():
        text = text.replace(k, v)
        
    # Edge case cleanup for stray  or \ufffd
    text = text.replace("", "")
    text = text.replace("\ufffd", "")
    
    # Date normalizations if we match simple formats
    # e.g., 31 Mar -> 2026-03-31
    # This might be too aggressive, but let's try some safe ones:
    date_map = {
        "31 Mar": "2026-03-31",
        "15 Jan": "2026-01-15",
        "01 Mar": "2026-03-01"
    }
    for k, v in date_map.items():
        if text.strip() == k:
            return v
            
    return text.strip()

def clean_dict(d):
    if isinstance(d, dict):
        return {k: clean_dict(v) for k, v in d.items()}
    elif isinstance(d, list):
        return [clean_dict(v) for v in d]
    elif isinstance(d, str):
        return clean_text(d)
    return d

def migrate():
    db_dir = Path("data_base")
    total_records = 0
    errors = 0
    
    for file in db_dir.glob("*.json"):
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        cleaned_data = []
        for i, u in enumerate(data):
            try:
                # 1. String temizliYi
                u_clean = clean_dict(u)
                
                # 2. Pydantic DoYrulaması
                record = UniversityRecord.model_validate(u_clean)
                
                # 3. Dump
                cleaned_data.append(record.model_dump(exclude_none=False))
                total_records += 1
            except ValidationError as e:
                print(f"[{file.name}] Validasyon hatası (Kayıt #{i} - {u.get('University_Name')}):")
                print(e)
                errors += 1
                
        # Dosyay Gncelle
        with open(file, "w", encoding="utf-8") as f:
            json.dump(cleaned_data, f, ensure_ascii=False, indent=4)
            
    print(f"\nMigration tamamland! Başarıyla işlenen kayıt sayısı: {total_records}")
    print(f"Toplam validasyon hatası: {errors}")

if __name__ == "__main__":
    migrate()
