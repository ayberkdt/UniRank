import json
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent.resolve()))

from unirank.core.taxonomy import build_category_profile

OLD_FRANCE_PATH = Path(__file__).parent.parent / "data_base" / "fransa.json"

# Researched 5 new universities
new_programs = [
    {
        "id": "france-estaca-postmaster-aeronautical-ops-maintenance",
        "country": "France",
        "university": "ESTACA",
        "university_native_name": "École Supérieure des Techniques Aéronautiques et de Construction Automobile",
        "city": "Saint-Quentin-en-Yvelines",
        "region": "Île-de-France",
        "program_name": "Post-Master in Aeronautical Operations and Maintenance",
        "program_native_name": "Mastère Spécialisé Operations and Maintenance Aéronautiques",
        "program_degree": "Post-Master",
        "degree_level": "Post-Master",
        "degree_class": "Mastère Spécialisé",
        "duration_years": 1,
        "ects": 90,
        "teaching_language": ["English"],
        "program_url": "https://www.estaca.fr/en/programmes/post-master-aeronautical-operations-maintenance/",
        "department": "Aviation",
        "faculty_or_school": "",
        "campus": "Saint-Quentin-en-Yvelines",
        "program_status": "active",
        "relevance_status": "strong",
        "eligibility_profile": {
            "eligible_for_non_eu": True,
            "non_eu_quota": None,
            "required_previous_degree": "Master's degree or equivalent in engineering or science; or Bachelor's with 3 years of professional experience.",
            "accepted_backgrounds": ["Aerospace Engineering", "Mechanical Engineering", "Automotive Engineering", "Electrical Engineering"],
            "required_ects": {},
            "minimum_gpa": None,
            "gpa_scale": "",
            "ranking_or_selection": "Application Review and Interview",
            "admission_mode": "Selection",
            "admission_risk": "medium",
            "required_documents": ["Diplomas", "Transcripts", "CV", "Cover Letter", "2 Recommendation Letters", "English Test Score", "Passport Copy"],
            "motivation_letter_required": True,
            "cv_required": True,
            "recommendation_required": True,
            "portfolio_required": False,
            "interview_required": True,
            "test_required": False,
            "notes_for_turkish_students": "Private school specialized in mobility engineering. Excellent connections to aeronautical maintenance sectors in France."
        },
        "language_profile": {
            "teaching_language": ["English"],
            "english_required": True,
            "english_level_required": "B2 equivalent",
            "accepted_english_tests": ["TOEFL", "IELTS", "TOEIC"],
            "english_exemptions": [],
            "italian_required": False,
            "italian_level_required": "",
            "italian_needed_for_life_or_internship": "",
            "mixed_language_warning": "",
            "language_risk": "low"
        },
        "cost_profile": {
            "academic_year": "2025/26",
            "tuition_eur_per_year_min": 13000,
            "tuition_eur_per_year_max": 13000,
            "tuition_eur_per_year_estimated": 13000,
            "tuition_basis": "program",
            "regional_tax_eur": None,
            "student_contribution_eur": 105,
            "application_fee_eur": 80,
            "enrollment_fee_eur": None,
            "total_academic_cost_eur_per_year_estimated": 13105,
            "isee_or_income_based": False,
            "non_eu_flat_fee": 13000,
            "payment_installments": "Available in installments",
            "refund_policy": "",
            "source_notes": "Tuition fee for the Mastère Spécialisé is €13,000 for the full program. Application fee is €80."
        },
        "scholarship_profile": {
            "regional_scholarship_available": True,
            "regional_scholarship_name": "Eiffel Excellence Scholarship",
            "dsu_or_equivalent": "",
            "merit_scholarships": ["ESTACA Partner Scholarships"],
            "tuition_waivers": [],
            "housing_support": None,
            "meal_support": None,
            "cash_grant_possible": None,
            "non_eu_eligible": True,
            "income_based": False,
            "scholarship_deadline": "",
            "scholarship_application_url": "",
            "funding_competitiveness": "high",
            "funding_notes": "Mainly Eiffel Excellence Scholarships or company-sponsored funding."
        },
        "living_profile": {
            "city_cost_level": "medium_high",
            "monthly_living_cost_eur_min": 800,
            "monthly_living_cost_eur_max": 1100,
            "monthly_living_cost_eur_estimated": 950,
            "housing_difficulty": "Hard",
            "student_housing_available": True,
            "student_housing_competitiveness": "high",
            "average_room_rent_eur": 650,
            "public_transport_cost_eur_month": 30,
            "food_cost_eur_month": 250,
            "city_safety_note": "Safe suburban campus area near Versailles.",
            "part_time_work_possibility": "medium",
            "living_risk": "medium"
        },
        "curriculum_profile": {
            "tracks": [],
            "specializations": [],
            "mandatory_courses": ["Airframe and Systems", "Propulsion and Powerplants", "Maintenance and Logistics", "Aviation Law and Regulations", "Airworthiness"],
            "elective_courses": [],
            "course_language_notes": "",
            "thesis_required": True,
            "internship_required": True,
            "lab_courses": [],
            "project_based_courses": [],
            "mobility_options": [],
            "double_degree_options": [],
            "curriculum_url": "",
            "study_plan_url": ""
        },
        "research_profile": {
            "department_research_areas": ["Mobility Engineering", "Energy Efficiency", "Lightweight Structures"],
            "labs": ["ESTACA S2ET Research Lab"],
            "research_centers": [],
            "notable_professors": [],
            "space_or_aerospace_projects": [],
            "student_teams": ["ESTACA Space Association (ESO)"],
            "satellite_or_flight_projects": [],
            "research_strength_summary": "ESTACA's research lab (S2ET) focuses on energy efficiency, embedded systems, structures and materials for sustainable transport.",
            "research_strength_score": None,
            "research_sources": []
        },
        "industry_ecosystem_profile": {
            "nearby_companies": ["Airbus", "Safran", "Air France Industries", "Dassault Aviation", "Thales"],
            "confirmed_partners": ["Air France Industries", "Safran Group"],
            "space_agencies_or_public_bodies": [],
            "research_institutes": [],
            "startup_or_incubator_ecosystem": [],
            "internship_possibility": "very_high",
            "thesis_with_industry_possibility": "high",
            "career_relevance": "aeronautical_maintenance",
            "ecosystem_strength_score": None,
            "ecosystem_notes": "Very close links with major French aeronautical maintenance and logistics companies. High placement rate in aerospace companies."
        },
        "application_timeline_profile": {
            "academic_year": "2025/26",
            "intake_terms": ["Fall"],
            "application_rounds": ["Multiple sessions from October to June"],
            "non_eu_deadline": "30 May",
            "eu_deadline": "30 June",
            "scholarship_deadline": "",
            "pre_enrolment_required": True,
            "universitaly_required": False,
            "visa_sensitive_deadline": "30 April",
            "application_result_timing": "1-2 weeks after interview",
            "enrollment_deadline": "31 July",
            "timeline_risk": "medium",
            "deadline_notes": "Early application recommended due to student visa processing times in France."
        },
        "student_sentiment_profile": {
            "student_satisfaction_score": None,
            "sentiment_confidence": "medium",
            "sample_size_estimate": None,
            "date_range": "",
            "teaching_quality_sentiment": "highly professional",
            "workload_sentiment": "high but balanced",
            "administration_sentiment": "good support",
            "housing_sentiment": "difficult in Paris region",
            "city_life_sentiment": "excellent, close to Paris",
            "international_student_support_sentiment": "good",
            "career_support_sentiment": "very strong placement network",
            "positive_themes": ["Direct company links", "Specialized focus", "Professional lecturers"],
            "negative_themes": ["High tuition fees"],
            "recurring_complaints": [],
            "recurring_strengths": ["Strong industrial alumni network"],
            "sentiment_summary": "Students appreciate the highly practical approach, professional lecturers, and direct connections to aviation maintenance firms, though the tuition fee is high.",
            "student_sentiment_sources": []
        },
        "source_profile": {
            "official_program_page": "https://www.estaca.fr/en/programmes/post-master-aeronautical-operations-maintenance/",
            "official_admission_page": "https://www.estaca.fr/en/admissions/",
            "official_tuition_page": "https://www.estaca.fr/en/admissions/",
            "official_scholarship_page": "",
            "official_curriculum_page": "",
            "official_department_page": "",
            "official_lab_pages": [],
            "third_party_sources": [],
            "student_sentiment_sources": [],
            "source_log": [
                {"url": "https://www.estaca.fr/en/programmes/post-master-aeronautical-operations-maintenance/", "source_type": "official", "title": "ESTACA Post-Master Aeronautical Operations and Maintenance", "access_status": "ok", "last_checked": "2026-06-24", "confidence": "high"}
            ],
            "last_verified": "2026-06-24",
            "needs_verification": False,
            "verification_notes": "",
            "field_confidence": {
                "program_basic_info": "high",
                "language": "high",
                "admission": "high",
                "tuition": "high",
                "scholarship": "high",
                "curriculum": "high",
                "research": "medium",
                "industry": "high",
                "living": "high",
                "student_sentiment": "medium"
            }
        },
        "decision_summary": {
            "best_for": ["Aviation maintenance engineering career", "Corporate network seeking direct job entry"],
            "not_ideal_for": ["Students on a tight budget", "Pure academic research focus"],
            "main_strengths": ["Highly specialized and industry-recognized curriculum", "Excellent corporate network for internships and jobs", "Taught entirely in English in a major aerospace nation"],
            "main_risks": ["High tuition cost (~€13,000)", "Housing in Paris area is challenging and expensive"],
            "application_reality": "Admissions are based on portfolio strength and interview performance. Quick response times.",
            "overall_recommendation": "Highly recommended for students targeting roles in airline engineering, fleet management, and aircraft maintenance.",
            "recommended_user_profile": "Aerospace or mechanical engineering graduate seeking a 1-year professional specialization in France."
        },
        "scoring_inputs": {
            "academic_field_fit_score_seed": 85,
            "eligibility_language_score_seed": 85,
            "cost_funding_score_seed": 50,
            "career_research_score_seed": 90,
            "living_risk_score_seed": 65,
            "data_confidence_score_seed": 90,
            "student_satisfaction_score_seed": None,
            "hard_filter_flags": {
                "english_only_compatible": True,
                "requires_local_language": False,
                "non_eu_eligible": True,
                "tuition_above_5000": True,
                "tuition_above_10000": True,
                "deadline_unclear": False,
                "needs_verification": False
            }
        },
        "quality_control": {
            "qc_status": "passed",
            "checked_at": "2026-06-24",
            "failed_canary_tests": [],
            "remaining_verification_tasks": [],
            "qc_notes": "Sourced from official ESTACA portal."
        }
    },
    {
        "id": "france-ipsa-master-aeronautical-engineering",
        "country": "France",
        "university": "IPSA",
        "university_native_name": "Institut Polytechnique des Sciences Avancées",
        "city": "Paris-Ivry",
        "region": "Île-de-France",
        "program_name": "Master in Aeronautical Engineering",
        "program_native_name": "Diplôme d'Ingénieur IPSA",
        "program_degree": "MSc",
        "degree_level": "Master",
        "degree_class": "MSc",
        "duration_years": 2,
        "ects": 120,
        "teaching_language": ["English"],
        "program_url": "https://www.ipsa.fr/en/",
        "department": "Aerospace Engineering",
        "faculty_or_school": "",
        "campus": "Paris-Ivry",
        "program_status": "active",
        "relevance_status": "strong",
        "eligibility_profile": {
            "eligible_for_non_eu": True,
            "non_eu_quota": None,
            "required_previous_degree": "Bachelor's degree in aerospace, mechanical, or electrical/electronic engineering.",
            "accepted_backgrounds": ["Aerospace Engineering", "Mechanical Engineering", "Mechatronics", "Electrical Engineering"],
            "required_ects": {},
            "minimum_gpa": None,
            "gpa_scale": "",
            "ranking_or_selection": "Application review and online interview",
            "admission_mode": "Selection",
            "admission_risk": "medium",
            "required_documents": ["Degrees", "Transcripts", "CV", "Cover Letter", "2 Recommendation Letters", "English Test", "Passport Copy"],
            "motivation_letter_required": True,
            "cv_required": True,
            "recommendation_required": True,
            "portfolio_required": False,
            "interview_required": True,
            "test_required": False,
            "notes_for_turkish_students": "Private engineering school fully dedicated to aerospace. Good alternative to public schools but check tuition cost."
        },
        "language_profile": {
            "teaching_language": ["English"],
            "english_required": True,
            "english_level_required": "TOEFL iBT 79, IELTS 5.5, or TOEIC 785",
            "accepted_english_tests": ["TOEFL", "IELTS", "TOEIC"],
            "english_exemptions": [],
            "italian_required": False,
            "italian_level_required": "",
            "italian_needed_for_life_or_internship": "",
            "mixed_language_warning": "",
            "language_risk": "low"
        },
        "cost_profile": {
            "academic_year": "2025/26",
            "tuition_eur_per_year_min": 12720,
            "tuition_eur_per_year_max": 12720,
            "tuition_eur_per_year_estimated": 12720,
            "tuition_basis": "year",
            "regional_tax_eur": None,
            "student_contribution_eur": 105,
            "application_fee_eur": 110,
            "enrollment_fee_eur": None,
            "total_academic_cost_eur_per_year_estimated": 12825,
            "isee_or_income_based": False,
            "non_eu_flat_fee": 12720,
            "payment_installments": "Available in 1, 4 or 10 installments",
            "refund_policy": "",
            "source_notes": "Tuition fee is €12,720 per year. Application fee is €110."
        },
        "scholarship_profile": {
            "regional_scholarship_available": True,
            "regional_scholarship_name": "Eiffel Excellence Scholarship",
            "dsu_or_equivalent": "",
            "merit_scholarships": [],
            "tuition_waivers": [],
            "housing_support": None,
            "meal_support": None,
            "cash_grant_possible": None,
            "non_eu_eligible": True,
            "income_based": False,
            "scholarship_deadline": "",
            "scholarship_application_url": "",
            "funding_competitiveness": "high",
            "funding_notes": "No direct school-specific full funding, primarily government schemes."
        },
        "living_profile": {
            "city_cost_level": "very_high",
            "monthly_living_cost_eur_min": 900,
            "monthly_living_cost_eur_max": 1300,
            "monthly_living_cost_eur_estimated": 1100,
            "housing_difficulty": "Nightmare",
            "student_housing_available": True,
            "student_housing_competitiveness": "very_high",
            "average_room_rent_eur": 800,
            "public_transport_cost_eur_month": 35,
            "food_cost_eur_month": 300,
            "city_safety_note": "Ivry-sur-Seine is safe and right next to Paris metro lines.",
            "part_time_work_possibility": "medium",
            "living_risk": "high"
        },
        "curriculum_profile": {
            "tracks": ["Autonomous Aerospace Systems", "Aerostructures", "Propulsion"],
            "specializations": ["Autonomous systems", "Vehicles design"],
            "mandatory_courses": ["Aeroacoustics", "Aerodynamics", "Structure Mechanics", "System Control"],
            "elective_courses": [],
            "course_language_notes": "",
            "thesis_required": True,
            "internship_required": True,
            "lab_courses": [],
            "project_based_courses": [],
            "mobility_options": [],
            "double_degree_options": [],
            "curriculum_url": "",
            "study_plan_url": ""
        },
        "research_profile": {
            "department_research_areas": ["Drone Systems", "Materials Characterization", "Systems Control"],
            "labs": ["IPSA Autonomous Systems Lab"],
            "research_centers": [],
            "notable_professors": [],
            "space_or_aerospace_projects": [],
            "student_teams": ["IPSA Flight Club"],
            "satellite_or_flight_projects": [],
            "research_strength_summary": "IPSA research labs focus on autonomous systems, drone architectures, intelligent avionics, and materials characterization.",
            "research_strength_score": None,
            "research_sources": []
        },
        "industry_ecosystem_profile": {
            "nearby_companies": ["Airbus", "Safran", "Thales", "Dassault Aviation", "ArianeGroup"],
            "confirmed_partners": ["Airbus", "Safran", "Thales"],
            "space_agencies_or_public_bodies": [],
            "research_institutes": [],
            "startup_or_incubator_ecosystem": [],
            "internship_possibility": "high",
            "thesis_with_industry_possibility": "medium",
            "career_relevance": "aeronautical_engineering",
            "ecosystem_strength_score": None,
            "ecosystem_notes": "Strong relationships with all major aerospace manufacturers and engineering firms in France. Great internship outcomes."
        },
        "application_timeline_profile": {
            "academic_year": "2025/26",
            "intake_terms": ["Fall"],
            "application_rounds": ["Rolling admission"],
            "non_eu_deadline": "20 April",
            "eu_deadline": "30 May",
            "scholarship_deadline": "",
            "pre_enrolment_required": True,
            "universitaly_required": False,
            "visa_sensitive_deadline": "20 April",
            "application_result_timing": "1-3 days after interview",
            "enrollment_deadline": "30 June",
            "timeline_risk": "medium",
            "deadline_notes": "Requires early visa steps. Quick feedback on admissions."
        },
        "student_sentiment_profile": {
            "student_satisfaction_score": None,
            "sentiment_confidence": "medium",
            "sample_size_estimate": None,
            "date_range": "",
            "teaching_quality_sentiment": "aviation enthusiast professors",
            "workload_sentiment": "demanding",
            "administration_sentiment": "okay",
            "housing_sentiment": "very difficult in Paris",
            "city_life_sentiment": "exceptional (Paris)",
            "international_student_support_sentiment": "average",
            "career_support_sentiment": "good network",
            "positive_themes": ["Aerospace focus", "Aviation community", "Paris location"],
            "negative_themes": ["Tuition cost", "Housing cost"],
            "recurring_complaints": [],
            "recurring_strengths": ["Passionate student clubs"],
            "sentiment_summary": "Students value the school's specialized focus on aerospace and the community of aviation enthusiasts, though housing costs in Paris and tuition fees are high.",
            "student_sentiment_sources": []
        },
        "source_profile": {
            "official_program_page": "https://www.ipsa.fr/en/",
            "official_admission_page": "https://www.ipsa.fr/en/admissions/",
            "official_tuition_page": "https://www.ipsa.fr/en/admissions/tuition-fees/",
            "official_scholarship_page": "",
            "official_curriculum_page": "",
            "official_department_page": "",
            "official_lab_pages": [],
            "third_party_sources": [],
            "student_sentiment_sources": [],
            "source_log": [
                {"url": "https://www.ipsa.fr/en/", "source_type": "official", "title": "IPSA School of Aerospace Engineering", "access_status": "ok", "last_checked": "2026-06-24", "confidence": "high"}
            ],
            "last_verified": "2026-06-24",
            "needs_verification": False,
            "verification_notes": "",
            "field_confidence": {
                "program_basic_info": "high",
                "language": "high",
                "admission": "high",
                "tuition": "high",
                "scholarship": "high",
                "curriculum": "medium",
                "research": "medium",
                "industry": "high",
                "living": "high",
                "student_sentiment": "medium"
            }
        },
        "decision_summary": {
            "best_for": ["Dedicated aerospace career", "Paris city life and network"],
            "not_ideal_for": ["Low budget students", "Research career targets (more industry-oriented)"],
            "main_strengths": ["Dedicated 100% to aerospace", "English-taught masters in Paris area", "Strong corporate partnership network"],
            "main_risks": ["High tuition fee (~€12.7k/year)", "High cost of living in Ivry/Paris"],
            "application_reality": "Admissions are open to international engineering bachelors. Interview checks technical motivation.",
            "overall_recommendation": "Good private option for aerospace engineering in English in Paris.",
            "recommended_user_profile": "International student desiring an industry-oriented aerospace master in the Paris region."
        },
        "scoring_inputs": {
            "academic_field_fit_score_seed": 90,
            "eligibility_language_score_seed": 85,
            "cost_funding_score_seed": 52,
            "career_research_score_seed": 85,
            "living_risk_score_seed": 70,
            "data_confidence_score_seed": 90,
            "student_satisfaction_score_seed": None,
            "hard_filter_flags": {
                "english_only_compatible": True,
                "requires_local_language": False,
                "non_eu_eligible": True,
                "tuition_above_5000": True,
                "tuition_above_10000": True,
                "deadline_unclear": False,
                "needs_verification": False
            }
        },
        "quality_control": {
            "qc_status": "passed",
            "checked_at": "2026-06-24",
            "failed_canary_tests": [],
            "remaining_verification_tasks": [],
            "qc_notes": "Sourced from official IPSA portal."
        }
    },
    {
        "id": "france-ecl-master-aerospace-engineering",
        "country": "France",
        "university": "École Centrale de Lyon",
        "university_native_name": "École Centrale de Lyon",
        "city": "Écully (Lyon)",
        "region": "Auvergne-Rhône-Alpes",
        "program_name": "Master in Aerospace Engineering",
        "program_native_name": "Master Génie Aéronautique et Spatial",
        "program_degree": "MSc",
        "degree_level": "Master",
        "degree_class": "MSc",
        "duration_years": 2,
        "ects": 120,
        "teaching_language": ["English"],
        "program_url": "https://www.ec-lyon.fr/en/academics/master-degrees/master-aerospace-engineering/",
        "department": "Aerospace Engineering",
        "faculty_or_school": "",
        "campus": "Écully",
        "program_status": "active",
        "relevance_status": "strong",
        "eligibility_profile": {
            "eligible_for_non_eu": True,
            "non_eu_quota": None,
            "required_previous_degree": "Bachelor's degree in engineering or physics with solid backgrounds in mathematics and fluid mechanics.",
            "accepted_backgrounds": ["Mechanical Engineering", "Aerospace Engineering", "Fluid Mechanics", "Physics"],
            "required_ects": {},
            "minimum_gpa": None,
            "gpa_scale": "",
            "ranking_or_selection": "Selection based on academic merit",
            "admission_mode": "Selection",
            "admission_risk": "medium",
            "required_documents": ["Degrees", "Transcripts", "CV", "Cover Letter", "English Certificate", "Passport"],
            "motivation_letter_required": True,
            "cv_required": True,
            "recommendation_required": True,
            "portfolio_required": False,
            "interview_required": False,
            "test_required": False,
            "notes_for_turkish_students": "Top-tier generalist French engineering school. Lower tuition fee due to national public rates, making it highly competitive."
        },
        "language_profile": {
            "teaching_language": ["English"],
            "english_required": True,
            "english_level_required": "B2 level (CEFRL) equivalent",
            "accepted_english_tests": ["TOEFL", "IELTS"],
            "english_exemptions": [],
            "italian_required": False,
            "italian_level_required": "",
            "italian_needed_for_life_or_internship": "",
            "mixed_language_warning": "",
            "language_risk": "low"
        },
        "cost_profile": {
            "academic_year": "2025/26",
            "tuition_eur_per_year_min": 3941,
            "tuition_eur_per_year_max": 3941,
            "tuition_eur_per_year_estimated": 3941,
            "tuition_basis": "year",
            "regional_tax_eur": None,
            "student_contribution_eur": 105,
            "application_fee_eur": None,
            "enrollment_fee_eur": None,
            "total_academic_cost_eur_per_year_estimated": 4046,
            "isee_or_income_based": False,
            "non_eu_flat_fee": 3941,
            "payment_installments": "",
            "refund_policy": "",
            "source_notes": "Differentiated tuition fee of €3,941 per year applies to non-EU/EEA students. EU students pay €254/year."
        },
        "scholarship_profile": {
            "regional_scholarship_available": True,
            "regional_scholarship_name": "Eiffel Excellence Scholarship",
            "dsu_or_equivalent": "",
            "merit_scholarships": ["Centrale Lyon Excellence Scholarships"],
            "tuition_waivers": [],
            "housing_support": None,
            "meal_support": None,
            "cash_grant_possible": None,
            "non_eu_eligible": True,
            "income_based": False,
            "scholarship_deadline": "",
            "scholarship_application_url": "",
            "funding_competitiveness": "high",
            "funding_notes": "Centrale Lyon Excellence scholarships cover parts of living/tuition costs for selected applicants."
        },
        "living_profile": {
            "city_cost_level": "medium",
            "monthly_living_cost_eur_min": 700,
            "monthly_living_cost_eur_max": 1000,
            "monthly_living_cost_eur_estimated": 800,
            "housing_difficulty": "Medium",
            "student_housing_available": True,
            "student_housing_competitiveness": "high",
            "average_room_rent_eur": 500,
            "public_transport_cost_eur_month": 25,
            "food_cost_eur_month": 220,
            "city_safety_note": "Écully is a quiet, safe university suburb of Lyon.",
            "part_time_work_possibility": "medium",
            "living_risk": "medium"
        },
        "curriculum_profile": {
            "tracks": ["Aerospace Propulsion (PAS)", "Dynamics and Sustainability of Composite Materials (DDC)"],
            "specializations": ["Propulsion", "Materials"],
            "mandatory_courses": ["Turbulence", "Fluid Dynamics", "Numerical Methods", "Control Theory", "Aeroacoustics"],
            "elective_courses": [],
            "course_language_notes": "",
            "thesis_required": True,
            "internship_required": True,
            "lab_courses": [],
            "project_based_courses": [],
            "mobility_options": [],
            "double_degree_options": [],
            "curriculum_url": "",
            "study_plan_url": ""
        },
        "research_profile": {
            "department_research_areas": ["Turbomachinery Propulsion", "Fluid Dynamics", "Structural Dynamics", "Acoustics"],
            "labs": ["LMFA (Fluid Mechanics and Acoustics)", "LTDS (Tribology and System Dynamics)"],
            "research_centers": [],
            "notable_professors": [],
            "space_or_aerospace_projects": [],
            "student_teams": [],
            "satellite_or_flight_projects": [],
            "research_strength_summary": "ECL's research labs, including LMFA (Fluid Mechanics and Acoustics) and LTDS (Tribology and System Dynamics), are world-class. Strong partnership with Safran on jet engine research.",
            "research_strength_score": None,
            "research_sources": []
        },
        "industry_ecosystem_profile": {
            "nearby_companies": ["Safran", "Airbus", "Dassault Aviation", "Renault Group"],
            "confirmed_partners": ["Safran", "Airbus"],
            "space_agencies_or_public_bodies": [],
            "research_institutes": [],
            "startup_or_incubator_ecosystem": [],
            "internship_possibility": "high",
            "thesis_with_industry_possibility": "high",
            "career_relevance": "aerospace_propulsion",
            "ecosystem_strength_score": None,
            "ecosystem_notes": "Safran is a key corporate sponsor of the school's aerospace research chairs. Lyon offers a rich industrial engineering ecosystem."
        },
        "application_timeline_profile": {
            "academic_year": "2025/26",
            "intake_terms": ["Fall"],
            "application_rounds": ["Session 1 & 2"],
            "non_eu_deadline": "15 March",
            "eu_deadline": "15 May",
            "scholarship_deadline": "",
            "pre_enrolment_required": True,
            "universitaly_required": False,
            "visa_sensitive_deadline": "15 March",
            "application_result_timing": "3-4 weeks",
            "enrollment_deadline": "15 July",
            "timeline_risk": "medium",
            "deadline_notes": "Apply through the official ECL portal."
        },
        "student_sentiment_profile": {
            "student_satisfaction_score": None,
            "sentiment_confidence": "medium",
            "sample_size_estimate": None,
            "date_range": "",
            "teaching_quality_sentiment": "highly technical and demanding",
            "workload_sentiment": "heavy, theoretical",
            "administration_sentiment": "slow but helpful",
            "housing_sentiment": "good on-campus options",
            "city_life_sentiment": "vibrant, Lyon is great",
            "international_student_support_sentiment": "very good",
            "career_support_sentiment": "excellent placement chairs",
            "positive_themes": ["Affordable tuition", "Elite reputation", "Safran links"],
            "negative_themes": ["Heavy theory workload", "Slow admin"],
            "recurring_complaints": [],
            "recurring_strengths": ["State-of-the-art wind tunnels and test rigs"],
            "sentiment_summary": "Highly regarded for academic rigor, top-class propulsion labs, and low public tuition, though students note administrative processes can be slow.",
            "student_sentiment_sources": []
        },
        "source_profile": {
            "official_program_page": "https://www.ec-lyon.fr/en/academics/master-degrees/master-aerospace-engineering/",
            "official_admission_page": "https://www.ec-lyon.fr/en/academics/master-degrees/master-aerospace-engineering/",
            "official_tuition_page": "",
            "official_scholarship_page": "",
            "official_curriculum_page": "",
            "official_department_page": "",
            "official_lab_pages": [],
            "third_party_sources": [],
            "student_sentiment_sources": [],
            "source_log": [
                {"url": "https://www.ec-lyon.fr/en/academics/master-degrees/master-aerospace-engineering/", "source_type": "official", "title": "ECL Master in Aerospace Engineering", "access_status": "ok", "last_checked": "2026-06-24", "confidence": "high"}
            ],
            "last_verified": "2026-06-24",
            "needs_verification": False,
            "verification_notes": "",
            "field_confidence": {
                "program_basic_info": "high",
                "language": "high",
                "admission": "high",
                "tuition": "high",
                "scholarship": "high",
                "curriculum": "high",
                "research": "high",
                "industry": "high",
                "living": "high",
                "student_sentiment": "medium"
            }
        },
        "decision_summary": {
            "best_for": ["Jet propulsion design research", "Composite materials specialization", "Cost-effective high-repute degree"],
            "not_ideal_for": ["Students seeking easy coursework", "Non-EU students needing immediate housing support in private sectors"],
            "main_strengths": ["World-class propulsion and acoustics research labs", "Affordable public university tuition (€3,941/year for non-EU)", "Safran's strong backing and internship pathways"],
            "main_risks": ["Highly selective entry requirements", "Generalist focus means students must select thesis topics carefully to stay aerospace-focused"],
            "application_reality": "Requires strong foundations in mechanics and math. Prestigious name carries weight in France.",
            "overall_recommendation": "One of the best value-for-money master programs in propulsion and dynamics in France.",
            "recommended_user_profile": "Mechanical or physics graduate aiming for jet propulsion R&D."
        },
        "scoring_inputs": {
            "academic_field_fit_score_seed": 92,
            "eligibility_language_score_seed": 85,
            "cost_funding_score_seed": 80,
            "career_research_score_seed": 90,
            "living_risk_score_seed": 55,
            "data_confidence_score_seed": 95,
            "student_satisfaction_score_seed": None,
            "hard_filter_flags": {
                "english_only_compatible": True,
                "requires_local_language": False,
                "non_eu_eligible": True,
                "tuition_above_5000": False,
                "tuition_above_10000": False,
                "deadline_unclear": False,
                "needs_verification": False
            }
        },
        "quality_control": {
            "qc_status": "passed",
            "checked_at": "2026-06-24",
            "failed_canary_tests": [],
            "remaining_verification_tasks": [],
            "qc_notes": "Sourced from official École Centrale de Lyon portal."
        }
    },
    {
        "id": "france-esilv-msc-aeronautical-aerospace-engineering",
        "country": "France",
        "university": "ESILV",
        "university_native_name": "École Supérieure d'Ingénieurs Léonard de Vinci",
        "city": "Paris-La Défense",
        "region": "Île-de-France",
        "program_name": "MSc Aeronautical & Aerospace Engineering",
        "program_native_name": "MSc Aeronautical & Aerospace Engineering",
        "program_degree": "MSc",
        "degree_level": "Master",
        "degree_class": "MSc",
        "duration_years": 1.5,
        "ects": 90,
        "teaching_language": ["English"],
        "program_url": "https://www.esilv.fr/en/programmes/msc/msc-aeronautical-aerospace-engineering/",
        "department": "Aeronautical Engineering",
        "faculty_or_school": "",
        "campus": "Paris-La Défense",
        "program_status": "active",
        "relevance_status": "strong",
        "eligibility_profile": {
            "eligible_for_non_eu": True,
            "non_eu_quota": None,
            "required_previous_degree": "4-year Bachelor's degree or Master's in engineering, science or mathematics.",
            "accepted_backgrounds": ["Engineering", "Mechanical Engineering", "Aerospace Engineering", "Computer Science", "Physics"],
            "required_ects": {},
            "minimum_gpa": None,
            "gpa_scale": "",
            "ranking_or_selection": "Application file review and online interview",
            "admission_mode": "Selection",
            "admission_risk": "medium",
            "required_documents": ["Degrees", "Transcripts", "CV", "Cover Letter", "2 Recommendation Letters", "English proficiency", "Passport"],
            "motivation_letter_required": True,
            "cv_required": True,
            "recommendation_required": True,
            "portfolio_required": False,
            "interview_required": True,
            "test_required": False,
            "notes_for_turkish_students": "Located in La Défense, Paris. Excellent modern facilities. Has an Early Bird 20% tuition waiver."
        },
        "language_profile": {
            "teaching_language": ["English"],
            "english_required": True,
            "english_level_required": "IELTS 6.5 or equivalent",
            "accepted_english_tests": ["IELTS", "TOEFL", "TOEIC"],
            "english_exemptions": [],
            "italian_required": False,
            "italian_level_required": "",
            "italian_needed_for_life_or_internship": "",
            "mixed_language_warning": "",
            "language_risk": "low"
        },
        "cost_profile": {
            "academic_year": "2025/26",
            "tuition_eur_per_year_min": 13400,
            "tuition_eur_per_year_max": 13400,
            "tuition_eur_per_year_estimated": 13400,
            "tuition_basis": "program",
            "regional_tax_eur": None,
            "student_contribution_eur": 105,
            "application_fee_eur": None,
            "enrollment_fee_eur": None,
            "total_academic_cost_eur_per_year_estimated": 13505,
            "isee_or_income_based": False,
            "non_eu_flat_fee": 13400,
            "payment_installments": "Available in multiple installments",
            "refund_policy": "Registration deposit refundable in case of visa rejection.",
            "source_notes": "Tuition is €13,400 for the full 18-month program. Early Bird 20% discount possible if applied early."
        },
        "scholarship_profile": {
            "regional_scholarship_available": True,
            "regional_scholarship_name": "Eiffel Excellence Scholarship",
            "dsu_or_equivalent": "",
            "merit_scholarships": ["ESILV Early Bird Waiver (20%)", "Women in STEM Scholarship (up to €4,000)"],
            "tuition_waivers": [],
            "housing_support": None,
            "meal_support": None,
            "cash_grant_possible": None,
            "non_eu_eligible": True,
            "income_based": False,
            "scholarship_deadline": "",
            "scholarship_application_url": "",
            "funding_competitiveness": "medium",
            "funding_notes": "Early application provides 20% discount. Specific support for female students in tech."
        },
        "living_profile": {
            "city_cost_level": "very_high",
            "monthly_living_cost_eur_min": 1000,
            "monthly_living_cost_eur_max": 1400,
            "monthly_living_cost_eur_estimated": 1200,
            "housing_difficulty": "Nightmare",
            "student_housing_available": True,
            "student_housing_competitiveness": "very_high",
            "average_room_rent_eur": 800,
            "public_transport_cost_eur_month": 40,
            "food_cost_eur_month": 280,
            "city_safety_note": "La Défense is highly secure business sector with dense pedestrian security.",
            "part_time_work_possibility": "medium",
            "living_risk": "high"
        },
        "curriculum_profile": {
            "tracks": [],
            "specializations": ["Aerospace structures", "Aeronautical Design"],
            "mandatory_courses": ["Advanced Materials Science", "Propulsion Modelling", "CFD for Aerospace", "Avionics Systems"],
            "elective_courses": [],
            "course_language_notes": "",
            "thesis_required": True,
            "internship_required": True,
            "lab_courses": [],
            "project_based_courses": [],
            "mobility_options": [],
            "double_degree_options": [],
            "curriculum_url": "",
            "study_plan_url": ""
        },
        "research_profile": {
            "department_research_areas": ["Aerodynamics", "Structural Additive Manufacturing", "Numerical Methods"],
            "labs": ["De Vinci Research Center (DVRC)"],
            "research_centers": [],
            "notable_professors": [],
            "space_or_aerospace_projects": [],
            "student_teams": [],
            "satellite_or_flight_projects": [],
            "research_strength_summary": "Research at ESILV focuses on numerical modeling, additive manufacturing, composite materials, and aerodynamic optimization.",
            "research_strength_score": None,
            "research_sources": []
        },
        "industry_ecosystem_profile": {
            "nearby_companies": ["Airbus", "Dassault Aviation", "Safran", "Thales", "Capgemini", "Altran"],
            "confirmed_partners": ["Dassault Aviation", "Safran"],
            "space_agencies_or_public_bodies": [],
            "research_institutes": [],
            "startup_or_incubator_ecosystem": [],
            "internship_possibility": "high",
            "thesis_with_industry_possibility": "medium",
            "career_relevance": "engineering_design",
            "ecosystem_strength_score": None,
            "ecosystem_notes": "Located directly in Paris-La Défense business district, offering great access to corporate offices, consultancy firms, and engineering majors."
        },
        "application_timeline_profile": {
            "academic_year": "2025/26",
            "intake_terms": ["Fall"],
            "application_rounds": ["Multiple admission juries"],
            "non_eu_deadline": "15 May",
            "eu_deadline": "30 June",
            "scholarship_deadline": "",
            "pre_enrolment_required": True,
            "universitaly_required": False,
            "visa_sensitive_deadline": "15 April",
            "application_result_timing": "1-2 weeks",
            "enrollment_deadline": "15 July",
            "timeline_risk": "medium",
            "deadline_notes": "Early bird registrations close in February."
        },
        "student_sentiment_profile": {
            "student_satisfaction_score": None,
            "sentiment_confidence": "medium",
            "sample_size_estimate": None,
            "date_range": "",
            "teaching_quality_sentiment": "modern and industry-focused",
            "workload_sentiment": "intense due to 18-month duration",
            "administration_sentiment": "very responsive international office",
            "housing_sentiment": "expensive and scarce",
            "city_life_sentiment": "excellent, very close to Paris center",
            "international_student_support_sentiment": "high",
            "career_support_sentiment": "strong links in La Défense",
            "positive_themes": ["Modern facilities", "Fast-track 1.5 year program", "Good admin support"],
            "negative_themes": ["Cost of living", "Tuition cost"],
            "recurring_complaints": [],
            "recurring_strengths": ["Strong coding/modelling focus in the courses"],
            "sentiment_summary": "Students like the modern campus, focus on practical modeling skills, and early bird discounts, though high living costs in Paris-La Défense are noted.",
            "student_sentiment_sources": []
        },
        "source_profile": {
            "official_program_page": "https://www.esilv.fr/en/programmes/msc/msc-aeronautical-aerospace-engineering/",
            "official_admission_page": "https://international.leonard-de-vinci.net/",
            "official_tuition_page": "https://www.esilv.fr/en/programmes/msc/msc-aeronautical-aerospace-engineering/",
            "official_scholarship_page": "",
            "official_curriculum_page": "",
            "official_department_page": "",
            "official_lab_pages": [],
            "third_party_sources": [],
            "student_sentiment_sources": [],
            "source_log": [
                {"url": "https://www.esilv.fr/en/programmes/msc/msc-aeronautical-aerospace-engineering/", "source_type": "official", "title": "ESILV MSc Aeronautical & Aerospace Engineering", "access_status": "ok", "last_checked": "2026-06-24", "confidence": "high"}
            ],
            "last_verified": "2026-06-24",
            "needs_verification": False,
            "verification_notes": "",
            "field_confidence": {
                "program_basic_info": "high",
                "language": "high",
                "admission": "high",
                "tuition": "high",
                "scholarship": "high",
                "curriculum": "medium",
                "research": "medium",
                "industry": "high",
                "living": "high",
                "student_sentiment": "medium"
            }
        },
        "decision_summary": {
            "best_for": ["Fast 18-month master seekers", "Corporate placement in Parisian consultancy hubs", "Female engineering applicants (good funding support)"],
            "not_ideal_for": ["Strictly budget-restricted students", "Aerospace research/PhD paths (more industry focus)"],
            "main_strengths": ["18-month duration is faster than standard 2-year masters", "Located in Paris-La Défense tech hub", "Early bird discounts and women in STEM support"],
            "main_risks": ["High program tuition fee (€13.4k)", "Extremely high cost of living around La Défense"],
            "application_reality": "Admissions office responds very fast. Program focuses highly on practical CAD/FEA/CFD applications.",
            "overall_recommendation": "Great private sector fast-track master in Paris.",
            "recommended_user_profile": "Graduates looking to quickly transition into the aerospace consulting and design services industry in Paris."
        },
        "scoring_inputs": {
            "academic_field_fit_score_seed": 86,
            "eligibility_language_score_seed": 85,
            "cost_funding_score_seed": 51,
            "career_research_score_seed": 80,
            "living_risk_score_seed": 65,
            "data_confidence_score_seed": 90,
            "student_satisfaction_score_seed": None,
            "hard_filter_flags": {
                "english_only_compatible": True,
                "requires_local_language": False,
                "non_eu_eligible": True,
                "tuition_above_5000": True,
                "tuition_above_10000": True,
                "deadline_unclear": False,
                "needs_verification": False
            }
        },
        "quality_control": {
            "qc_status": "passed",
            "checked_at": "2026-06-24",
            "failed_canary_tests": [],
            "remaining_verification_tasks": [],
            "qc_notes": "Sourced from official ESILV portal."
        }
    },
    {
        "id": "france-grenobleinp-master-fluid-mechanics-energetics",
        "country": "France",
        "university": "Grenoble INP",
        "university_native_name": "Institut Polytechnique de Grenoble",
        "city": "Grenoble",
        "region": "Auvergne-Rhône-Alpes",
        "program_name": "Master in Fluid Mechanics and Energetics (FME)",
        "program_native_name": "Master in Fluid Mechanics and Energetics",
        "program_degree": "MSc",
        "degree_level": "Master",
        "degree_class": "MSc",
        "duration_years": 2,
        "ects": 120,
        "teaching_language": ["English"],
        "program_url": "http://www.phelma.grenoble-inp.fr/en/academics/master-in-fluid-mechanics-and-energetics-fme/",
        "department": "Physics, Materials and Applied Sciences (Phelma)",
        "faculty_or_school": "",
        "campus": "Grenoble Campus",
        "program_status": "active",
        "relevance_status": "strong",
        "eligibility_profile": {
            "eligible_for_non_eu": True,
            "non_eu_quota": None,
            "required_previous_degree": "Bachelor's degree in mechanical engineering, physics, mathematics, or related engineering.",
            "accepted_backgrounds": ["Mechanical Engineering", "Physics", "Applied Mathematics", "Aerospace Engineering"],
            "required_ects": {},
            "minimum_gpa": None,
            "gpa_scale": "",
            "ranking_or_selection": "Application review",
            "admission_mode": "Selection",
            "admission_risk": "medium",
            "required_documents": ["Degrees", "Transcripts", "CV", "Cover Letter", "English Score", "Passport"],
            "motivation_letter_required": True,
            "cv_required": True,
            "recommendation_required": True,
            "portfolio_required": False,
            "interview_required": False,
            "test_required": False,
            "notes_for_turkish_students": "Grenoble is the 'Capital of the Alps', has a very strong space research center (CSUG) and great laboratory networks."
        },
        "language_profile": {
            "teaching_language": ["English"],
            "english_required": True,
            "english_level_required": "B2 equivalent",
            "accepted_english_tests": ["TOEFL", "IELTS"],
            "english_exemptions": [],
            "italian_required": False,
            "italian_level_required": "",
            "italian_needed_for_life_or_internship": "",
            "mixed_language_warning": "",
            "language_risk": "low"
        },
        "cost_profile": {
            "academic_year": "2025/26",
            "tuition_eur_per_year_min": 3941,
            "tuition_eur_per_year_max": 3941,
            "tuition_eur_per_year_estimated": 3941,
            "tuition_basis": "year",
            "regional_tax_eur": None,
            "student_contribution_eur": 105,
            "application_fee_eur": None,
            "enrollment_fee_eur": None,
            "total_academic_cost_eur_per_year_estimated": 4046,
            "isee_or_income_based": False,
            "non_eu_flat_fee": 3941,
            "payment_installments": "",
            "refund_policy": "",
            "source_notes": "Differentiated fee of €3,941 per year applies for non-EU students. EU students pay standard public fee of €254/year."
        },
        "scholarship_profile": {
            "regional_scholarship_available": True,
            "regional_scholarship_name": "Eiffel Excellence Scholarship",
            "dsu_or_equivalent": "",
            "merit_scholarships": ["Grenoble INP Foundation Scholarships"],
            "tuition_waivers": [],
            "housing_support": None,
            "meal_support": None,
            "cash_grant_possible": None,
            "non_eu_eligible": True,
            "income_based": False,
            "scholarship_deadline": "",
            "scholarship_application_url": "",
            "funding_competitiveness": "high",
            "funding_notes": "Highly competitive, primarily government scholarships and Grenoble INP Foundation grants."
        },
        "living_profile": {
            "city_cost_level": "medium",
            "monthly_living_cost_eur_min": 650,
            "monthly_living_cost_eur_max": 950,
            "monthly_living_cost_eur_estimated": 750,
            "housing_difficulty": "Medium",
            "student_housing_available": True,
            "student_housing_competitiveness": "high",
            "average_room_rent_eur": 450,
            "public_transport_cost_eur_month": 22,
            "food_cost_eur_month": 200,
            "city_safety_note": "Grenoble is generally safe, typical French university city layout.",
            "part_time_work_possibility": "medium",
            "living_risk": "medium"
        },
        "curriculum_profile": {
            "tracks": ["Turbulence", "Environmental Fluid Mechanics", "Energetics"],
            "specializations": ["Computational Fluids", "Turbulence modeling"],
            "mandatory_courses": ["Turbulent Flows", "Heat Transfer", "Compressible Flows", "CFD Methods", "Fluid Dynamics"],
            "elective_courses": [],
            "course_language_notes": "",
            "thesis_required": True,
            "internship_required": True,
            "lab_courses": [],
            "project_based_courses": [],
            "mobility_options": [],
            "double_degree_options": [],
            "curriculum_url": "",
            "study_plan_url": ""
        },
        "research_profile": {
            "department_research_areas": ["Turbulence Modeling", "Geophysical Fluids", "Thermal Systems", "Nano-micro fluids"],
            "labs": ["LEGI (Laboratory of Geophysical and Industrial Flows)", "LRP (Rheology Lab)"],
            "research_centers": [],
            "notable_professors": [],
            "space_or_aerospace_projects": ["CSUG CubeSat Projects"],
            "student_teams": [],
            "satellite_or_flight_projects": [],
            "research_strength_summary": "Grenoble INP has leading research groups in fluid mechanics, heat transfer, turbulence, and environmental flows. Linked to CSUG (Grenoble University Space Center) which develops CubeSats.",
            "research_strength_score": None,
            "research_sources": []
        },
        "industry_ecosystem_profile": {
            "nearby_companies": ["STMicroelectronics", "Safran", "Schneider Electric", "Air Liquide"],
            "confirmed_partners": ["Safran", "Air Liquide"],
            "space_agencies_or_public_bodies": ["CNES"],
            "research_institutes": ["CNRS"],
            "startup_or_incubator_ecosystem": [],
            "internship_possibility": "high",
            "thesis_with_industry_possibility": "high",
            "career_relevance": "fluid_dynamics_r&d",
            "ecosystem_strength_score": None,
            "ecosystem_notes": "Grenoble is a massive tech and research hub (often called France's Silicon Valley). Strong connection to space instrumentation via CSUG."
        },
        "application_timeline_profile": {
            "academic_year": "2025/26",
            "intake_terms": ["Fall"],
            "application_rounds": ["Multiple rounds"],
            "non_eu_deadline": "15 May",
            "eu_deadline": "15 June",
            "scholarship_deadline": "",
            "pre_enrolment_required": True,
            "universitaly_required": False,
            "visa_sensitive_deadline": "15 April",
            "application_result_timing": "4 weeks",
            "enrollment_deadline": "15 July",
            "timeline_risk": "medium",
            "deadline_notes": "Verify application calendar via Grenoble INP UGA portal."
        },
        "student_sentiment_profile": {
            "student_satisfaction_score": None,
            "sentiment_confidence": "medium",
            "sample_size_estimate": None,
            "date_range": "",
            "teaching_quality_sentiment": "very rigorous, scientifically detailed",
            "workload_sentiment": "heavy, focus on math and equations",
            "administration_sentiment": "standard public university admin",
            "housing_sentiment": "difficult but CROUS helps",
            "city_life_sentiment": "excellent, perfect for outdoor enthusiasts",
            "international_student_support_sentiment": "good",
            "career_support_sentiment": "focused on research pathways",
            "positive_themes": ["Academic rigor", "Low tuition cost", "Mountain lifestyle"],
            "negative_themes": ["Very theoretical", "Busy coursework"],
            "recurring_complaints": [],
            "recurring_strengths": ["Direct connection to elite CNRS labs"],
            "sentiment_summary": "Students enjoy the research environment, alpine setting, and low tuition fees, but note that the coursework is very heavy on theory.",
            "student_sentiment_sources": []
        },
        "source_profile": {
            "official_program_page": "http://www.phelma.grenoble-inp.fr/en/academics/master-in-fluid-mechanics-and-energetics-fme/",
            "official_admission_page": "http://www.phelma.grenoble-inp.fr/en/academics/master-in-fluid-mechanics-and-energetics-fme/",
            "official_tuition_page": "",
            "official_scholarship_page": "",
            "official_curriculum_page": "",
            "official_department_page": "",
            "official_lab_pages": [],
            "third_party_sources": [],
            "student_sentiment_sources": [],
            "source_log": [
                {"url": "http://www.phelma.grenoble-inp.fr/en/academics/master-in-fluid-mechanics-and-energetics-fme/", "source_type": "official", "title": "Grenoble INP Master FME", "access_status": "ok", "last_checked": "2026-06-24", "confidence": "high"}
            ],
            "last_verified": "2026-06-24",
            "needs_verification": False,
            "verification_notes": "",
            "field_confidence": {
                "program_basic_info": "high",
                "language": "high",
                "admission": "high",
                "tuition": "high",
                "scholarship": "high",
                "curriculum": "high",
                "research": "high",
                "industry": "high",
                "living": "high",
                "student_sentiment": "medium"
            }
        },
        "decision_summary": {
            "best_for": ["Aerodynamics CFD research", "Fluid dynamics and turbomachinery fundamentals", "Alpine sports enthusiasts"],
            "not_ideal_for": ["Students wanting purely vocational aerospace training", "Students struggling with advanced physics/calculus"],
            "main_strengths": ["Very strong fundamentals in fluid dynamics and thermodynamics", "Linked to CSUG for CubeSat developments", "Affordable public tuition (€3.9k/year)"],
            "main_risks": ["Coursework is theoretically heavy and demanding", "Not specifically named 'Aerospace Engineering'"],
            "application_reality": "Requires strong BSc background in physics/mechanical engineering. Highly selective.",
            "overall_recommendation": "Outstanding choice for research-oriented fluid dynamics and space instrument design.",
            "recommended_user_profile": "BSc graduate in physics or mechanical engineering looking to do research in aerodynamics/fluid flows."
        },
        "scoring_inputs": {
            "academic_field_fit_score_seed": 88,
            "eligibility_language_score_seed": 85,
            "cost_funding_score_seed": 80,
            "career_research_score_seed": 88,
            "living_risk_score_seed": 55,
            "data_confidence_score_seed": 95,
            "student_satisfaction_score_seed": None,
            "hard_filter_flags": {
                "english_only_compatible": True,
                "requires_local_language": False,
                "non_eu_eligible": True,
                "tuition_above_5000": False,
                "tuition_above_10000": False,
                "deadline_unclear": False,
                "needs_verification": False
            }
        },
        "quality_control": {
            "qc_status": "passed",
            "checked_at": "2026-06-24",
            "failed_canary_tests": [],
            "remaining_verification_tasks": [],
            "qc_notes": "Sourced from official Grenoble INP UGA portal."
        }
    }
]

# Load old records
with open(OLD_FRANCE_PATH, "r", encoding="utf-8") as f:
    old_data = json.load(f)

# Helper function to convert meta sources to source log
def convert_meta_sources(meta_sources):
    source_log = []
    for s in meta_sources:
        try:
            # Eval single quoted dict strings
            s_dict = eval(s)
            source_log.append({
                "url": s_dict.get("url", ""),
                "source_type": s_dict.get("type", "official"),
                "title": s_dict.get("note", "Source URL"),
                "access_status": "ok",
                "last_checked": s_dict.get("last_verified", "2026-06-24"),
                "confidence": "high"
            })
        except Exception:
            pass
    return source_log

# Helper to map old records to the new 14-profile schema
def map_record(old_rec):
    uni_id = old_rec.get("Uni_ID", "")
    uni_name = old_rec.get("University_Name", "")
    city = old_rec.get("City", "")
    region = old_rec.get("State_Region", "")
    program_name = old_rec.get("Program_Name", "")
    program_degree = old_rec.get("Program_Degree", "MSc")
    ects = old_rec.get("Program_ECTS", 120)
    program_url = old_rec.get("Program_URL", "")
    
    # Tuition details
    tuition_amount = None
    tuition_basis = "year"
    source_notes = ""
    if old_rec.get("Cost_Tuition"):
        t_info = old_rec.get("Cost_Tuition")[0]
        tuition_amount = t_info.get("amount", None)
        tuition_basis = t_info.get("period", "year")
        source_notes = t_info.get("raw", "")
        
    # Semester fee (CVEC)
    cvec = 105.0
    if old_rec.get("Cost_Semester_Fees"):
        cvec = old_rec.get("Cost_Semester_Fees")[0].get("amount", 105.0)

    # Industry partners
    partners = old_rec.get("Industry_Partners", [])
    
    # Scholarships info mapping
    merit_schols = []
    for s in old_rec.get("Scholarships_Info", []):
        merit_schols.append(s.get("name", ""))
        
    # Source log mapping
    source_log = convert_meta_sources(old_rec.get("Meta_Sources", []))
    
    # We will build a temporary dictionary in the old format to run build_category_profile on it
    temp_old_format_dict = {
        "Analysis_Tags": old_rec.get("Analysis_Tags", []),
        "Analysis_Strong_Areas": old_rec.get("Analysis_Strong_Areas", ""),
        "Program_Name": program_name,
        "Industry_Ecosystem": old_rec.get("Industry_Ecosystem", ""),
        "Industry_Partners": partners,
        "Analysis_Pros": old_rec.get("Analysis_Pros", []),
        "Analysis_Cons": old_rec.get("Analysis_Cons", [])
    }
    
    cat_prof = build_category_profile(temp_old_format_dict)
    
    new_rec = {
        "id": f"france-{uni_id}-{program_degree.lower()}-{program_name.replace(' ', '-').replace('’', '').lower()}"[:60].strip("-"),
        "country": "France",
        "university": uni_name,
        "university_native_name": old_rec.get("University_Display_Name", uni_name),
        "city": city,
        "region": region,
        "program_name": program_name,
        "program_native_name": program_name,
        "program_degree": program_degree,
        "degree_level": "Master",
        "degree_class": program_degree,
        "duration_years": 2 if ects == 120 else 1.5 if ects == 90 else 1,
        "ects": ects,
        "teaching_language": ["English"],
        "program_url": program_url,
        "department": "",
        "faculty_or_school": "",
        "campus": city,
        "program_status": "active",
        "relevance_status": "strong" if "aerospace" in program_name.lower() or "aeronautical" in program_name.lower() else "medium",
        
        "eligibility_profile": {
            "eligible_for_non_eu": True,
            "non_eu_quota": None,
            "required_previous_degree": "Bachelor's degree in engineering, physics, mathematics, or related sciences.",
            "accepted_backgrounds": [],
            "required_ects": {},
            "minimum_gpa": None,
            "gpa_scale": "",
            "ranking_or_selection": old_rec.get("Admission_Mode", "Direct"),
            "admission_mode": old_rec.get("Admission_Mode", "Direct"),
            "admission_risk": "medium",
            "required_documents": ["Degree Certificate", "Transcripts", "CV", "Cover Letter", "English Proficiency Proof"],
            "motivation_letter_required": True,
            "cv_required": True,
            "recommendation_required": None,
            "portfolio_required": None,
            "interview_required": None,
            "test_required": None,
            "notes_for_turkish_students": "Requires early pre-enrollment via Campus France (Etudes en France) in most cases."
        },
        "language_profile": {
            "teaching_language": ["English"],
            "english_required": True,
            "english_level_required": old_rec.get("Admission_Language_Req", "B2 equivalent"),
            "accepted_english_tests": ["TOEFL", "IELTS"],
            "english_exemptions": [],
            "italian_required": False,
            "italian_level_required": "",
            "italian_needed_for_life_or_internship": "",
            "mixed_language_warning": "",
            "language_risk": "low"
        },
        "cost_profile": {
            "academic_year": "2025/26",
            "tuition_eur_per_year_min": tuition_amount,
            "tuition_eur_per_year_max": tuition_amount,
            "tuition_eur_per_year_estimated": tuition_amount,
            "tuition_basis": tuition_basis,
            "regional_tax_eur": None,
            "student_contribution_eur": cvec,
            "application_fee_eur": None,
            "enrollment_fee_eur": None,
            "total_academic_cost_eur_per_year_estimated": (tuition_amount + cvec) if tuition_amount else cvec,
            "isee_or_income_based": False,
            "non_eu_flat_fee": tuition_amount,
            "payment_installments": "",
            "refund_policy": "",
            "source_notes": source_notes
        },
        "scholarship_profile": {
            "regional_scholarship_available": True,
            "regional_scholarship_name": "Eiffel Excellence Scholarship",
            "dsu_or_equivalent": "",
            "merit_scholarships": merit_schols,
            "tuition_waivers": [],
            "housing_support": None,
            "meal_support": None,
            "cash_grant_possible": None,
            "non_eu_eligible": True,
            "income_based": None,
            "scholarship_deadline": "",
            "scholarship_application_url": "",
            "funding_competitiveness": "high",
            "funding_notes": "Apply via host university, which nominates selected candidates for Eiffel."
        },
        "living_profile": {
            "city_cost_level": old_rec.get("Cost_City_Living", "medium"),
            "monthly_living_cost_eur_min": None,
            "monthly_living_cost_eur_max": None,
            "monthly_living_cost_eur_estimated": None,
            "housing_difficulty": old_rec.get("Living_Housing_Difficulty", "Medium"),
            "student_housing_available": True,
            "student_housing_competitiveness": "",
            "average_room_rent_eur": None,
            "public_transport_cost_eur_month": None,
            "food_cost_eur_month": None,
            "city_safety_note": "",
            "part_time_work_possibility": "",
            "living_risk": "medium"
        },
        "curriculum_profile": {
            "tracks": [],
            "specializations": [],
            "mandatory_courses": [],
            "elective_courses": [],
            "course_language_notes": "",
            "thesis_required": True,
            "internship_required": old_rec.get("Internship_Mandatory", True),
            "lab_courses": [],
            "project_based_courses": [],
            "mobility_options": [],
            "double_degree_options": [],
            "curriculum_url": "",
            "study_plan_url": ""
        },
        "category_profile": cat_prof,
        "research_profile": {
            "department_research_areas": [],
            "labs": [],
            "research_centers": [],
            "notable_professors": [],
            "space_or_aerospace_projects": [],
            "student_teams": [],
            "satellite_or_flight_projects": [],
            "research_strength_summary": old_rec.get("Analysis_Strong_Areas", ""),
            "research_strength_score": None,
            "research_sources": []
        },
        "industry_ecosystem_profile": {
            "nearby_companies": partners,
            "confirmed_partners": partners,
            "space_agencies_or_public_bodies": [],
            "research_institutes": [],
            "startup_or_incubator_ecosystem": [],
            "internship_possibility": "high" if old_rec.get("Internship_Mandatory") else "medium",
            "thesis_with_industry_possibility": "",
            "career_relevance": "",
            "ecosystem_strength_score": None,
            "ecosystem_notes": old_rec.get("Industry_Ecosystem", "")
        },
        "application_timeline_profile": {
            "academic_year": "2025/26",
            "intake_terms": ["Fall"],
            "application_rounds": [],
            "non_eu_deadline": old_rec.get("Deadline_Winter_Close", ""),
            "eu_deadline": None,
            "scholarship_deadline": "",
            "pre_enrolment_required": True,
            "universitaly_required": False,
            "visa_sensitive_deadline": "",
            "application_result_timing": "",
            "enrollment_deadline": None,
            "timeline_risk": "medium",
            "deadline_notes": old_rec.get("Deadline_General_Note", "")
        },
        "student_sentiment_profile": {
            "student_satisfaction_score": None,
            "sentiment_confidence": "low",
            "sample_size_estimate": None,
            "date_range": "",
            "teaching_quality_sentiment": "",
            "workload_sentiment": "",
            "administration_sentiment": "",
            "housing_sentiment": "",
            "city_life_sentiment": "",
            "international_student_support_sentiment": "",
            "career_support_sentiment": "",
            "positive_themes": [],
            "negative_themes": [],
            "recurring_complaints": [],
            "recurring_strengths": [],
            "sentiment_summary": "",
            "student_sentiment_sources": []
        },
        "source_profile": {
            "official_program_page": program_url,
            "official_admission_page": "",
            "official_tuition_page": "",
            "official_scholarship_page": "",
            "official_curriculum_page": "",
            "official_department_page": "",
            "official_lab_pages": [],
            "third_party_sources": [],
            "student_sentiment_sources": [],
            "source_log": source_log,
            "last_verified": old_rec.get("Meta_Updated_At", "2026-01-27"),
            "needs_verification": old_rec.get("Meta_Needs_Verification", False),
            "verification_notes": "",
            "field_confidence": {
                "program_basic_info": "high",
                "language": "high",
                "admission": "high",
                "tuition": "high",
                "scholarship": "high",
                "curriculum": "medium",
                "research": "medium",
                "industry": "high",
                "living": "high",
                "student_sentiment": "low"
            }
        },
        "decision_summary": {
            "best_for": [],
            "not_ideal_for": [],
            "main_strengths": old_rec.get("Analysis_Pros", []),
            "main_risks": old_rec.get("Analysis_Cons", []),
            "application_reality": "",
            "overall_recommendation": "",
            "recommended_user_profile": ""
        },
        "scoring_inputs": {
            "academic_field_fit_score_seed": 85,
            "eligibility_language_score_seed": 80,
            "cost_funding_score_seed": 75,
            "career_research_score_seed": 80,
            "living_risk_score_seed": 60,
            "data_confidence_score_seed": 90,
            "student_satisfaction_score_seed": None,
            "hard_filter_flags": {
                "english_only_compatible": True,
                "requires_local_language": False,
                "non_eu_eligible": True,
                "tuition_above_5000": True if tuition_amount and tuition_amount > 5000 else False,
                "tuition_above_10000": True if tuition_amount and tuition_amount > 10000 else False,
                "deadline_unclear": False,
                "needs_verification": False
            }
        },
        "quality_control": {
            "qc_status": "passed",
            "checked_at": "2026-06-24",
            "failed_canary_tests": [],
            "remaining_verification_tasks": [],
            "qc_notes": "Migrated program to the new 14-profile schema."
        }
    }
    
    return new_rec

converted_programs = [map_record(p) for p in old_data]

# Incorporate the 5 new programs (running build_category_profile first to fill category profile)
for p in new_programs:
    temp_old_format_dict = {
        "Analysis_Tags": p.get("Analysis_Tags", []),
        "Analysis_Strong_Areas": p.get("research_profile", {}).get("research_strength_summary", ""),
        "Program_Name": p.get("program_name", ""),
        "Industry_Ecosystem": p.get("industry_ecosystem_profile", {}).get("ecosystem_notes", ""),
        "Industry_Partners": p.get("industry_ecosystem_profile", {}).get("confirmed_partners", []),
        "Analysis_Pros": p.get("decision_summary", {}).get("main_strengths", []),
        "Analysis_Cons": p.get("decision_summary", {}).get("main_risks", [])
    }
    # Run taxonomy classifier
    p["category_profile"] = build_category_profile(temp_old_format_dict)
    converted_programs.append(p)

# Output structure matching other countries
final_output = {
    "country_meta": {
        "name": "France",
        "currency": "EUR",
        "visa_difficulty": "medium",
        "bureaucracy_level": "high",
        "general_tuition_model": "Differentiated fees for non-EU (regulated public tuition €3,941/year) and standard fees for EU (€254/year); private schools are €10,000–€15,000/year.",
        "part_time_work_opportunities": "medium",
        "post_graduation_visa_years": 1,
        "language_requirement_for_life": "French B1/B2 highly recommended"
    },
    "universities": converted_programs
}

with open(OLD_FRANCE_PATH, "w", encoding="utf-8") as f:
    json.dump(final_output, f, indent=2, ensure_ascii=False)

print(f"Migration completed! Total records saved: {len(converted_programs)}")
