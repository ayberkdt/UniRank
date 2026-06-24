import json
import re
from pathlib import Path
from collections import defaultdict
from typing import Dict, Any, List

TAXONOMY_PATH = Path(__file__).parent.parent.parent / "data_base" / "taxonomy.json"

_taxonomy_data = None

def load_taxonomy() -> Dict[str, Any]:
    global _taxonomy_data
    if _taxonomy_data is None:
        try:
            with open(TAXONOMY_PATH, "r", encoding="utf-8") as f:
                _taxonomy_data = json.load(f)
        except Exception as e:
            print(f"Error loading taxonomy: {e}")
            _taxonomy_data = {}
    return _taxonomy_data

def normalize_text(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    return " " + " ".join(text.split()) + " "

def build_category_profile(record: Dict[str, Any]) -> Dict[str, Any]:
    taxonomy = load_taxonomy()
    
    # Extract fields
    fields = {
        'Analysis_Tags': (record.get('Analysis_Tags', []) if isinstance(record.get('Analysis_Tags'), list) else [record.get('Analysis_Tags', '')]),
        'Analysis_Strong_Areas': record.get('Analysis_Strong_Areas', ''),
        'Program_Name': record.get('Program_Name', ''),
        'Industry_Ecosystem': record.get('Industry_Ecosystem', ''),
        'Industry_Partners': record.get('Industry_Partners', ''),
        'Analysis_Pros': (record.get('Analysis_Pros', []) if isinstance(record.get('Analysis_Pros'), list) else [record.get('Analysis_Pros', '')]),
        'Analysis_Cons': (record.get('Analysis_Cons', []) if isinstance(record.get('Analysis_Cons'), list) else [record.get('Analysis_Cons', '')]),
    }
    
    # Normalize texts for searching
    texts = {
        'tags': normalize_text(" ".join([str(t) for t in fields['Analysis_Tags']])),
        'strong_areas': normalize_text(str(fields['Analysis_Strong_Areas'])),
        'program': normalize_text(str(fields['Program_Name'])),
        'ecosystem': normalize_text(str(fields['Industry_Ecosystem'])),
        'partners': normalize_text(str(fields['Industry_Partners'])),
        'pros': normalize_text(" ".join([str(p) for p in fields['Analysis_Pros']])),
        'cons': normalize_text(" ".join([str(c) for c in fields['Analysis_Cons']])),
    }
    
    # Weights based on where the alias is found
    weights = {
        'tags': 4.0,
        'strong_areas': 3.0,
        'program': 3.0,
        'ecosystem': 2.0,
        'partners': 2.0,
        'pros': 1.0,
        'cons': 0.5
    }
    
    subcategory_scores = defaultdict(float)
    parent_scores = defaultdict(float)
    matched_subcats = set()
    normalized_tags = set()
    
    # Matching
    for subcat_id, subcat_info in taxonomy.items():
        parent = subcat_info['parent']
        label = subcat_info['label']
        aliases = subcat_info.get('aliases', [])
        
        subcat_score = 0.0
        
        for alias in aliases:
            norm_alias = normalize_text(alias).strip()
            if not norm_alias:
                continue
            
            # Very general words check
            if norm_alias in ['engineering', 'technology', 'research', 'science', 'program', 'master']:
                continue
                
            alias_pattern = f" {norm_alias} "
            
            # Special case for "control"
            if norm_alias == "control":
                # Only match if aerospace context exists
                context_words = ["aerospace", "aircraft", "spacecraft", "flight", "satellite", "aero"]
                context_found = False
                for ctx in context_words:
                    if f" {ctx} " in texts['tags'] or f" {ctx} " in texts['program'] or f" {ctx} " in texts['strong_areas']:
                        context_found = True
                        break
                if not context_found:
                    continue
            
            # Check fields
            for field_name, text_val in texts.items():
                if alias_pattern in text_val:
                    subcat_score += weights[field_name]
                    normalized_tags.add(subcat_id)
        
        if subcat_score > 0:
            subcategory_scores[label] += subcat_score
            parent_scores[parent] += subcat_score
            if subcat_score >= 3.0: # Minimum threshold to be considered a strong subcategory
                matched_subcats.add(label)
                
    # Normalize parent scores to 0-100 (Max theoretical could be anything, let's say 20 points is 100)
    MAX_SCORE = 20.0
    category_scores_100 = {}
    for parent, score in parent_scores.items():
        category_scores_100[parent] = min(100, int((score / MAX_SCORE) * 100))
        
    # Sort parents by score
    sorted_parents = sorted(parent_scores.items(), key=lambda x: x[1], reverse=True)
    
    primary_categories = []
    secondary_categories = []
    
    for i, (parent, score) in enumerate(sorted_parents):
        if score >= 3.0:
            if i < 3:
                primary_categories.append(parent)
            else:
                secondary_categories.append(parent)
                
    # Sort subcategories by score
    sorted_subcats = sorted(subcategory_scores.items(), key=lambda x: x[1], reverse=True)
    final_subcats = [s[0] for s in sorted_subcats if s[1] >= 3.0][:8]
    
    if not primary_categories:
        primary_categories = ["Uncategorized / Needs Review"]
        
    return {
        "primary_categories": primary_categories,
        "secondary_categories": secondary_categories,
        "subcategories": final_subcats,
        "normalized_tags": list(normalized_tags),
        "category_scores": category_scores_100
    }
