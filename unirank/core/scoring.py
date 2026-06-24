# unirank/core/scoring.py
import re
from typing import Dict, Any, List, Tuple
from unirank.core.taxonomy import build_category_profile

def normalize_text(text: Any) -> str:
    if not text or str(text).lower() == 'nan':
        return ""
    # Remove non-alphanumeric and replace with space
    s = str(text).lower()
    s = re.sub(r'[^a-z0-9\s]', ' ', s)
    return s

def calculate_score(record: Dict[str, Any], preferences: Dict[str, Any], weights: Dict[str, float]) -> Dict[str, Any]:
    explanation = []
    warnings = []
    passed = True

    # Safely get values, handling pandas NaN or dict missing keys
    def get_val(keys):
        if isinstance(keys, str):
            keys = [keys]
        for k in keys:
            if k in record:
                v = record[k]
                if v is not None and str(v).lower() != 'nan':
                    return v
        return ""

    cat_profile = record.get('Category_Profile')
    if not cat_profile:
        cat_profile = build_category_profile(record)
        record['Category_Profile'] = cat_profile

    # --- HARD FILTERS ---
    
    # 1. Degree Filter
    target_degree = preferences.get('degreeFilter', 'All')
    rec_degree = str(get_val(['Program_Degree', 'program_degree'])).lower()
    if target_degree != 'All' and rec_degree:
        if target_degree.lower() not in rec_degree:
            passed = False

    # 2. English Only Filter
    lang_req = str(get_val(['Admission_Language_Req', 'admission_language_req'])).lower()
    if preferences.get('onlyEnglish', False):
        if 'german' in lang_req or 'french' in lang_req or 'dutch' in lang_req:
            passed = False

    # 3. Max Tuition
    tuit_raw = get_val(['tuition_eur_per_year', 'Tuition_Fee'])
    try:
        tuit = float(tuit_raw) if tuit_raw else 0.0
    except (ValueError, TypeError):
        tuit = 0.0
        
    max_tuit = preferences.get('maxTuition', 0)
    if max_tuit > 0:
        if tuit > max_tuit:
            passed = False

    # --- SCORE COMPONENTS ---
    
    # 1. Academic / Field Fit (0-100)
    academic_fit = 0.0
    selected_cats = preferences.get('selectedKeywords', [])
    
    if not selected_cats:
        academic_fit = 50.0
    else:
        score_sum = 0.0
        matches = 0
        for cat in selected_cats:
            # Is it a top category?
            if cat in cat_profile['category_scores']:
                cat_score = cat_profile['category_scores'][cat]
                score_sum += cat_score
                if cat_score >= 30:
                    matches += 1
            # Is it a subcategory?
            elif cat in cat_profile['subcategories']:
                score_sum += 100.0  # Perfect match for subcategory
                matches += 1
            elif cat in cat_profile['normalized_tags']:
                score_sum += 60.0 # Partial match
                matches += 1
        
        if len(selected_cats) > 0:
            academic_fit = score_sum / len(selected_cats)
            
        academic_fit = min(100.0, max(0.0, academic_fit))
        
        if academic_fit >= 80:
            explanation.append("Strong academic match for your selected fields.")
        elif academic_fit >= 40:
            explanation.append("Partial academic match for your selected fields.")
        else:
            explanation.append("No strong match found for your selected fields.")

    min_field_fit = preferences.get('minFieldFit', 0)
    if min_field_fit and academic_fit < min_field_fit:
        passed = False

    # 2. Eligibility & Language Fit (0-100)
    elig_fit = 70.0
    ad_mode = str(get_val(['Admission_Mode', 'admission_mode'])).lower()
    
    if 'english' in lang_req:
        elig_fit += 10.0
        if 'german' not in lang_req and 'french' not in lang_req and 'dutch' not in lang_req:
            elig_fit += 10.0
            explanation.append("Program is fully English-taught.")
        else:
            elig_fit -= 20.0
            warnings.append(f"Requires an additional language ({lang_req}).")
            
    if 'direct' in ad_mode:
        elig_fit += 20.0
        explanation.append("Direct admission offers lower entry risk.")
    elif any(x in ad_mode for x in ['aptitude test', 'committee', 'portfolio', 'interview']):
        elig_fit -= 20.0
        warnings.append(f"Competitive admission process ({ad_mode}).")
        
    elig_fit = min(100.0, max(0.0, elig_fit))

    # 3. Cost & Funding (0-100)
    max_t = 20000.0
    tuition_norm = min(1.0, tuit / max_t)
    tuition_score = (1.0 - tuition_norm) * 100.0
    
    sem_fee_raw = get_val(['semester_fee_eur', 'semester_fee'])
    try:
        sem_fee = float(sem_fee_raw) if sem_fee_raw else 0.0
    except (ValueError, TypeError):
        sem_fee = 0.0
        
    sem_fee_norm = min(1.0, sem_fee / 1000.0)
    sem_fee_score = (1.0 - sem_fee_norm) * 100.0
    
    scholarship_score = 0.0
    schol_info = get_val(['Scholarships_Info', 'scholarships_info'])
    if schol_info and len(schol_info) > 0:
        scholarship_score = 100.0
        explanation.append("Scholarships are available for non-EU students.")
        
    cost_fit = (tuition_score * 0.7) + (sem_fee_score * 0.2) + (scholarship_score * 0.1)
    cost_fit = min(100.0, max(0.0, cost_fit))
    
    if tuit > 10000:
        warnings.append(f"High yearly tuition (€{tuit:.0f}).")
    elif tuit <= 2000:
        explanation.append(f"Very affordable tuition (€{tuit:.0f}/yr).")

    # 4. Career / Research Ecosystem (0-100)
    career_fit = 50.0
    ecosystem_str = normalize_text(" ".join(str(x) for x in [
        get_val('Industry_Ecosystem'),
        get_val('Industry_Partners'),
        get_val('Analysis_Pros'),
        get_val('field_recognition')
    ]))
    
    premium_partners = ['esa', 'dlr', 'nasa', 'jaxa', 'airbus', 'cern', 'onera', 'isae', 'estec']
    partner_matches = sum(1 for p in premium_partners if p in ecosystem_str)
    
    career_fit += partner_matches * 15.0
    
    comp_int = str(get_val('Industry_Comp_Intensity')).lower()
    if 'high' in comp_int:
        career_fit += 10.0
        
    if get_val('Internship_Mandatory'):
        career_fit += 10.0
        explanation.append("Mandatory internship ensures industry exposure.")
        
    career_fit = min(100.0, max(0.0, career_fit))
    if partner_matches > 0:
        explanation.append("Strong aerospace/tech ecosystem (partners include major agencies/corps).")

    # 5. Living Risk (0-100)
    living_fit = 50.0
    cost_city = str(get_val('Cost_City_Living')).lower()
    
    if 'very_high' in cost_city:
        living_fit -= 30.0
    elif 'high' in cost_city:
        living_fit -= 15.0
    elif 'low' in cost_city:
        living_fit += 20.0
        
    housing = str(get_val('Living_Housing_Difficulty')).lower()
    if 'nightmare' in housing:
        living_fit -= 30.0
        warnings.append("Housing market is extremely difficult (Nightmare).")
    elif 'very hard' in housing:
        living_fit -= 20.0
        warnings.append("Housing market is very difficult.")
    elif 'hard' in housing:
        living_fit -= 10.0
    elif 'moderate' in housing or 'easy' in housing:
        living_fit += 20.0
        explanation.append("Housing is relatively accessible.")
        
    living_fit = min(100.0, max(0.0, living_fit))

    # 6. Data Confidence / Deadline (0-100)
    conf_fit = 80.0
    if get_val('Meta_Needs_Verification'):
        conf_fit -= 20.0
        warnings.append("Data needs manual verification.")
    else:
        explanation.append("Data is verified.")
        
    sources = get_val('Meta_Sources')
    if sources and len(sources) > 0:
        conf_fit += 20.0
        
    conf_fit = min(100.0, max(0.0, conf_fit))

    # --- WEIGHTED SUM ---
    w_total = sum([
        weights.get('academic_fit', 30),
        weights.get('eligibility_language', 20),
        weights.get('cost_funding', 20),
        weights.get('career_research', 15),
        weights.get('living_risk', 10),
        weights.get('confidence_deadline', 5)
    ]) or 100.0
    
    n_w = {
        'ac': weights.get('academic_fit', 30) / w_total,
        'el': weights.get('eligibility_language', 20) / w_total,
        'co': weights.get('cost_funding', 20) / w_total,
        'ca': weights.get('career_research', 15) / w_total,
        'li': weights.get('living_risk', 10) / w_total,
        'cf': weights.get('confidence_deadline', 5) / w_total
    }
    
    final_score = (
        (academic_fit * n_w['ac']) +
        (elig_fit * n_w['el']) +
        (cost_fit * n_w['co']) +
        (career_fit * n_w['ca']) +
        (living_fit * n_w['li']) +
        (conf_fit * n_w['cf'])
    )

    return {
        'passed_hard_filters': passed,
        'total_score': final_score,
        'components': {
            'academic_fit': academic_fit,
            'eligibility_language': elig_fit,
            'cost_funding': cost_fit,
            'career_research': career_fit,
            'living_risk': living_fit,
            'confidence_deadline': conf_fit
        },
        'explanation': explanation,
        'warnings': warnings
    }
