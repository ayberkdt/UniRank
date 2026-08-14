from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data_base" / "amerika.json"
AUDIT_PATH = ROOT / "reports" / "source_link_audit_ucsd_aerospace_ms_2026-08-14.json"
TODAY = "2026-08-14"

PROGRAM = "https://mae.ucsd.edu/grad"
ADMISSION = "https://mae.ucsd.edu/grad/graduate-admissions"
CURRICULUM = "https://mae.ucsd.edu/grad/mae-master-science-program"
COURSES = "https://mae.ucsd.edu/courses"
APP_FEE = "https://grad.ucsd.edu/admissions/admission-faq/faq-application-fee.html"
FEES = "https://students.ucsd.edu/finances/fees/registration/2026-27/graduate.html"
COA = "https://fas.ucsd.edu/cost-of-attendance/graduate-students/index.html"
ASE = "https://grad.ucsd.edu/financial/employment/ases/ase-fee-payment-info.html"
HOUSING_APPLY = "https://hdhgradfamilyhousing.ucsd.edu/apply/index.html"
HOUSING_FAQ = "https://hdhgradfamilyhousing.ucsd.edu/faq/future-residents.html"
NUEVO_EAST = "https://hdhgradfamilyhousing.ucsd.edu/communities/nuevo-east.html"
ONE_MIRAMAR = "https://hdhgradfamilyhousing.ucsd.edu/communities/one-miramar.html"
RESEARCH = "https://mae.ucsd.edu/research/overview"
AEROSPACE = "https://mae.ucsd.edu/research-area/aerospace"
LSDO = "https://lsdo.eng.ucsd.edu/"
KRAMER = "https://kramer.ucsd.edu/"
SAHA = "https://saha-lab.eng.ucsd.edu/"
SANCHEZ = "https://asanchez.ucsd.edu/"
FLOW = "https://flowphysics.ucsd.edu/"
CISLUNAR = "https://mae.ucsd.edu/mae-highlights/2023-10/assistant-professor-aaron-rosengren-secures-grant-cutting-edge-cislunar"
EXPORT = "https://blink.ucsd.edu/sponsor/exportcontrol/researchers.html"
I20 = "https://iseo.ucsd.edu/student-services/new-program/i-20.html"
I20_FUNDING = "https://iseo.ucsd.edu/student-services/iservices-instructions/funding-requirements.html"
INTL_ADMITTED = "https://grad.ucsd.edu/admissions/admitted-students/international-students.html"
QS = "https://www.topuniversities.com/universities/university-california-san-diego-ucsd"

REDDIT_HOUSING_OFFER = "https://www.reddit.com/r/UCSD/comments/1uk1klh/nuevo_east_grad_housing_decision/"
REDDIT_HOUSING_QUESTIONS = "https://www.reddit.com/r/UCSD/comments/1us1cx9/graduate_housing_questions/"
REDDIT_I20 = "https://www.reddit.com/r/UCSD/comments/1ujla44/i20_is_taking_too_long_to_arrive/"


def bi(en: str, tr: str) -> dict[str, str]:
    return {"en": en, "tr": tr}


def source(
    url: str,
    title: str,
    source_type: str,
    fields: list[str],
    en: str,
    tr: str,
    *,
    confidence: str = "high",
    access_status: str = "ok",
) -> dict:
    return {
        "url": url,
        "title": title,
        "source_type": source_type,
        "access_status": access_status,
        "last_checked": TODAY,
        "relevant_fields": fields,
        "confidence": confidence,
        "notes": bi(en, tr),
    }


def main() -> None:
    rows = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    row = next(item for item in rows if item.get("id") == "ucsd-mae")

    row.update(
        {
            "country": "United States",
            "university": "University of California, San Diego",
            "university_native_name": "University of California, San Diego (UC San Diego)",
            "city": "San Diego",
            "region": "California",
            "program_name": "Master of Science in Engineering Sciences (Aerospace Engineering)",
            "program_native_name": "Master of Science in Engineering Sciences (Aerospace Engineering)",
            "program_degree": "MS",
            "degree_level": "Master",
            "major_code": "MAE-MS-001 / MC75",
            "duration_years": None,
            "duration": bi(
                "Full-time students may finish in a minimum of three quarters (one academic year) and must finish within seven quarters.",
                "Tam zamanlı öğrenciler en az üç çeyrekte (bir akademik yıl) bitirebilir ve yedi çeyrek içinde tamamlamalıdır.",
            ),
            "duration_quarters_minimum": 3,
            "duration_quarters_maximum": 7,
            "ects": None,
            "us_quarter_units": 36,
            "teaching_language": ["Unknown"],
            "teaching_languages": ["Unknown"],
            "program_url": CURRICULUM,
            "program_status": "active",
            "relevance_status": "strong",
            "delivery_modes": ["on_campus"],
            "full_time_only": False,
            "part_time_available": True,
            "tuition_eur_per_year": None,
            "annual_fee_eur": None,
            "qs_ranking": 81,
            "qs_ranking_display": "#81",
            "qs_ranking_year": 2027,
        }
    )

    row["prestige_profile"] = {
        "qs_world_rank": 81,
        "qs_edition": 2027,
        "qs_source_url": QS,
        "interpretation": bi(
            "The QS institutional rank is context only. Aerospace suitability is evidenced separately by MC75, its curriculum, faculty research area and laboratories.",
            "QS kurum sırası yalnızca bağlamdır. Havacılık-uzay uygunluğu MC75, müfredatı, öğretim üyesi araştırma alanı ve laboratuvarlarla ayrıca kanıtlanır.",
        ),
    }

    row["eligibility_profile"] = {
        "eligible_for_non_eu": True,
        "required_previous_degree": bi(
            "A bachelor's degree or equivalent. An engineering bachelor's is not mandatory, but a strong mathematics and physics foundation is required.",
            "Lisans derecesi veya dengi. Mühendislik lisansı zorunlu değildir; ancak güçlü matematik ve fizik altyapısı gerekir.",
        ),
        "accepted_backgrounds": [
            bi("Engineering", "Mühendislik"),
            bi("Mathematics with strong physics preparation", "Güçlü fizik hazırlığıyla matematik"),
            bi("Physics with strong mathematics preparation", "Güçlü matematik hazırlığıyla fizik"),
        ],
        "minimum_gpa": 3.0,
        "minimum_gpa_scale": 4.0,
        "minimum_gpa_is_university_floor": True,
        "minimum_gpa_guarantees_admission": False,
        "typical_admitted_gpa": "3.5-4.0",
        "department_rarely_admits_below_gpa": 3.2,
        "duplicate_related_masters_allowed": False,
        "duplicate_degree_rule": bi(
            "UC San Diego does not admit an applicant to an MS or PhD if the applicant already holds an MS or PhD in the same or a related engineering, physics or mathematics field.",
            "UC San Diego, aynı veya ilişkili mühendislik, fizik ya da matematik alanında MS/doktora sahibi adayı tekrar MS veya doktoraya kabul etmez.",
        ),
        "admission_mode": "holistic_program_review",
        "admission_risk": "high",
        "required_documents": [
            bi("Online graduate application", "Çevrim içi lisansüstü başvuru"),
            bi("Academic records from every postsecondary institution attended", "Devam edilen tüm yükseköğretim kurumlarından akademik kayıtlar"),
            bi("Statement of purpose", "Amaç beyanı"),
            bi("Three letters of recommendation", "Üç referans mektubu"),
            bi("Curriculum vitae", "Özgeçmiş"),
            bi("English-proficiency result when not exempt", "Muaf değilse İngilizce yeterlilik sonucu"),
        ],
        "official_transcripts_required_at_application": False,
        "official_transcripts_required_after_admission": True,
        "motivation_letter_required": True,
        "cv_required": True,
        "recommendation_required": True,
        "recommendation_letter_count": 3,
        "portfolio_required": False,
        "interview_required": None,
        "application_fee_usd": 155,
        "application_fee_scope": "international applicants",
        "application_fee_refundable": False,
        "application_fee_waiver_possible": True,
        "application_fee_waiver_international_eligibility": None,
        "fee_waiver_request_deadline_relative_to_program_deadline_days": 7,
        "fee_waiver_limit": "one waiver for the first eligible application",
        "gre": {
            "policy": "optional_not_required",
            "cycle": "Fall 2027",
            "test_type": "GRE General",
            "subject_test_required": False,
            "minimum_scores": {},
            "typical_quantitative_percentile_if_submitted": "85-90+",
            "typical_score_is_cutoff": False,
            "validity_years": 5,
            "institution_code": "4836",
            "department_code_required": False,
            "self_report_allowed_at_application": True,
            "official_score_required_after_matriculation_if_submitted": True,
            "absence_viewed_negatively": False,
            "source_ids": [ADMISSION],
        },
        "verification_notes": bi(
            "The 3.0 GPA is a minimum, not a competitive guarantee. The department reports most admits at 3.5-4.0 and says it rarely admits below 3.2.",
            "3,0 GPA bir asgari şarttır, rekabet garantisi değildir. Bölüm kabul edilenlerin çoğunu 3,5-4,0 aralığında bildirir ve 3,2 altını nadiren kabul ettiğini söyler.",
        ),
    }

    row["language_profile"] = {
        "teaching_language": ["Unknown"],
        "teaching_languages": ["Unknown"],
        "english_required": True,
        "requirement_scope": "international applicants whose native language is not English, unless an official prior-degree exemption applies",
        "accepted_english_tests": [
            {"test": "TOEFL iBT", "minimum_score_policy": {"new_scale": 4.5, "old_scale": 85}, "home_edition_accepted": True},
            {"test": "TOEFL paper-delivered", "minimum_score": 64},
            {"test": "IELTS", "minimum_score": 7.0, "indicator_accepted": True},
            {"test": "Duolingo English Test", "minimum_score": 120},
        ],
        "self_report_allowed_at_application": True,
        "official_score_required_if_nominated": True,
        "exemptions": [
            bi(
                "A completed or in-progress bachelor's, master's or doctoral degree from a regionally accredited US institution where English is the sole instructional language, or a WHED-listed foreign institution where English is the sole instructional language.",
                "İngilizcenin tek öğretim dili olduğu bölgesel akreditasyonlu ABD kurumundan ya da WHED'de İngilizcenin tek öğretim dili olduğu yabancı kurumdan tamamlanmış/devam eden lisans, yüksek lisans veya doktora.",
            ),
            bi("Permanent-resident status under the department rule.", "Bölüm kuralına göre daimi ikamet statüsü."),
        ],
        "language_risk": "medium",
        "verification_notes": bi(
            "Admission test thresholds are explicit. No checked official source explicitly labels the teaching language of this MS, so it remains Unknown.",
            "Kabul sınavı eşikleri açıktır. Kontrol edilen hiçbir resmî kaynak bu MS'in öğretim dilini açıkça etiketlemediğinden alan Unknown kalır.",
        ),
    }

    row["cost_profile"] = {
        "academic_year": "2026/2027",
        "currency": "USD",
        "cost_scope": "new first-time international/non-California-resident academic graduate student, three quarters",
        "tuition_usd_per_year": 28824,
        "tuition_basis": "annual systemwide tuition plus nonresident supplemental tuition",
        "systemwide_tuition_usd_per_year": 13722,
        "nonresident_supplemental_tuition_usd_per_year": 15102,
        "student_services_fee_usd_per_year": 1344,
        "health_insurance_premium_usd": 6660,
        "other_mandatory_fees_excluding_health_usd": 2603.17,
        "ucgpc_fee_usd": 7,
        "first_time_international_visa_administration_fee_usd": 200,
        "mandatory_fees_usd_per_year": 2810.17,
        "registrar_nonresident_total_usd": 38087.17,
        "first_year_direct_university_cost_with_ship_usd": 38294.17,
        "first_year_direct_university_cost_without_ship_usd": 31634.17,
        "health_insurance_required": True,
        "health_insurance_waiver_possible_with_qualifying_plan": True,
        "financial_aid_standard_nonresident_coa_on_campus_usd": 76329,
        "financial_aid_standard_nonresident_coa_off_campus_usd": 76821,
        "total_cost_of_attendance_usd_per_year": 76821,
        "total_cost_of_attendance_scope": "off-campus non-California-resident graduate planning budget",
        "financial_aid_coa_is_bill": False,
        "financial_aid_coa_components_usd": {
            "resident_direct_cost_layer": 22878,
            "nonresident_supplemental_tuition": 15102,
            "off_campus_food_and_housing": 31548,
            "books_materials_supplies_equipment": 729,
            "personal": 2574,
            "transportation": 3990,
        },
        "i20_funding_requirement_usd": 73507,
        "i20_funding_requirement_basis_date": "2025-11-14",
        "i20_funding_requirement_is_current_fee_bill": False,
        "official_fee_layer_difference": bi(
            "The Registrar's detailed 2026-27 nonresident charges total $38,087.17 before the separately listed $7 UCGPC and $200 first-time international visa-administration fees. Financial Aid's off-campus nonresident COA is $76,821. ISEO's 2026 I-20 proof amount is $73,507 but says it is based on November 14, 2025 COA figures. These layers serve different purposes and are not interchangeable.",
            "Registrar'ın ayrıntılı 2026-27 eyalet dışı ücretleri, ayrıca listelenen 7 $ UCGPC ve 200 $ ilk uluslararası vize-idare ücreti öncesi 38.087,17 $'dır. Financial Aid kampüs dışı eyalet dışı COA'yı 76.821 $ verir. ISEO'nun 2026 I-20 kanıt tutarı 73.507 $'dır; ancak 14 Kasım 2025 COA rakamlarına dayandığını belirtir. Bu katmanlar farklı amaçlıdır ve birbirinin yerine kullanılamaz.",
        ),
        "complete_program_cost_usd": None,
        "tuition_eur_per_year_min": None,
        "tuition_eur_per_year_max": None,
        "tuition_eur_per_year_estimated": None,
        "total_first_year_cost_eur": None,
        "scholarship_availability": "very_limited_competitive_for_ms",
        "scholarship_risk": "very_high",
        "verification_notes": bi(
            "The COA is a planning budget, not a bill. A complete-program total is not stated because students can take three to seven quarters and future rates are unknown.",
            "COA bir planlama bütçesidir, fatura değildir. Öğrenciler üç ila yedi çeyrek sürebildiği ve gelecek oranlar bilinmediği için tam program toplamı verilmez.",
        ),
    }

    row["scholarship_profile"] = {
        "available_types": ["rare_ra", "rare_ta", "external_or_university_fellowships"],
        "non_eu_eligible": None,
        "application_mode": "separate",
        "application_mode_detail": "possible appointments or awards are pursued separately after or outside the admission application",
        "automatic_consideration": False,
        "separate_application_required": True,
        "departmental_funding_guaranteed": False,
        "full_tuition_award_guaranteed": False,
        "ms_students_should_expect_support": False,
        "ra_ta_reserved_for_continuing_phd": True,
        "ra_ta_for_ms_rare_and_very_competitive": True,
        "qualifying_ase_appointment_minimum_percent": 25,
        "qualifying_ase_can_receive_ship_and_partial_fee_remission": True,
        "ase_remission_covers_nonresident_supplemental_tuition": False,
        "scholarship_deadline": None,
        "opportunities": [],
        "funding_notes": bi(
            "MAE explicitly says MS students should not expect RA or TA support. Qualifying academic employment can provide SHIP and partial fee remission, but an appointment is separate, rare for MS students and not guaranteed at admission.",
            "MAE, MS öğrencilerinin RA veya TA desteği beklememesi gerektiğini açıkça söyler. Uygun akademik istihdam SHIP ve kısmi ücret muafiyeti sağlayabilir; ancak atama ayrıdır, MS için nadirdir ve kabulde garanti edilmez.",
        ),
        "verification_notes": bi(
            "Self-funding is the safe baseline unless the student receives a written appointment or award. Do not use possible employment as visa funding before it is documented.",
            "Öğrenci yazılı atama veya ödül almadıkça güvenli varsayım öz-finansmandır. Belgelenmeden olası istihdamı vize finansmanı saymayın.",
        ),
    }

    row["living_profile"] = {
        "city_type": "Metropolis",
        "housing_search_difficulty": "very_high",
        "living_cost_risk": "very_high",
        "living_risk": "high",
        "student_housing_available": True,
        "student_dorm_availability": "available_limited",
        "housing_access": "waitlist",
        "housing_access_detail": "separate Graduate and Family Housing waitlist; regular applicants are ordered after priority groups by application date",
        "housing_application_separate": True,
        "housing_application_after_admission": True,
        "housing_guaranteed": False,
        "waitlist_update_required_each_quarter": True,
        "housing_offer_response_hours": 48,
        "regular_offer_refusals_before_archive": 2,
        "standard_housing_agreement_years": 2,
        "shore_priority_program_available": True,
        "shore_self_nomination_allowed": False,
        "shore_is_very_limited": True,
        "monthly_housing_rent_usd_per_month_min": 1050,
        "monthly_housing_rent_usd_per_month_max": 2220,
        "rent_range_scope": "2026-27 Nuevo East single-occupancy bedroom/full one-bedroom rates; not a private-market average",
        "shared_bedroom_monthly_rate_usd_min": 525,
        "shared_bedroom_monthly_rate_usd_max": 1110,
        "utilities_included_for_nuevo_east": True,
        "official_coa_food_and_housing_off_campus_usd": 31548,
        "housing_options": [
            bi("Graduate and Family Housing waitlist", "Graduate and Family Housing bekleme listesi"),
            bi("SHORE department-nominated priority housing (very limited)", "Bölüm aday göstermeli SHORE öncelikli konut (çok sınırlı)"),
            bi("UC San Diego off-campus housing resources", "UC San Diego kampüs dışı konut kaynakları"),
        ],
        "verification_notes": bi(
            "Graduate housing is explicitly not guaranteed. Rates are university housing examples; they are not evidence of general San Diego rent.",
            "Lisansüstü konut açıkça garanti değildir. Oranlar üniversite konutu örnekleridir; genel San Diego kirasının kanıtı değildir.",
        ),
    }

    row["curriculum_profile"] = {
        "degree_major_code": "MAE-MS-001 / MC75",
        "quarter_units_total": 36,
        "course_count_summary": bi("Plan II: 9 courses; Plan I: 6 courses + 12 research units", "Plan II: 9 ders; Plan I: 6 ders + 12 araştırma birimi"),
        "course_count_total_including_thesis": 9,
        "course_count_fixed": False,
        "taught_project_and_seminar_component_count": bi("Plan II: 9 courses; Plan I: 6 courses", "Plan II: 9 ders; Plan I: 6 ders"),
        "course_count_plan_ii": 9,
        "course_count_plan_i": 6,
        "completion_routes": ["Plan I thesis defense", "Plan II comprehensive examination"],
        "plan_i": {
            "coursework_units": 24,
            "course_count": 6,
            "research_units_mae_299": 12,
            "specialization_course_groups": 2,
            "courses_per_specialization": 3,
            "thesis_and_defense_required": True,
            "defense_attempts_maximum": 2,
            "committee_members_minimum": 3,
            "mae_committee_members_minimum": 2,
        },
        "plan_ii": {
            "coursework_units": 36,
            "course_count": 9,
            "comprehensive_component_courses": 5,
            "comprehensive_components_required_to_pass": 3,
            "minimum_residence_quarters": 3,
            "minimum_residence_units_per_quarter": 6,
            "recommended_full_time_units_per_quarter": 12,
        },
        "aerospace_systems_core": [
            "MAE 208 Mathematics for Engineers",
            "MAE 201 Mechanics of Fluids or MAE 210A Fluid Mechanics I",
            "MAE 202 Thermal Processes or MAE 221A Heat and Mass Transfer",
            "MAE 212 Introductory Compressible Flow",
            "MAE 240 Space Flight Mechanics",
        ],
        "aerospace_elective_examples": [
            "MAE 207 Advanced Astrodynamics",
            "MAE 211 Introduction to Combustion",
            "MAE 213 Mechanics of Propulsion",
            "MAE 214A Turbulence and Turbulent Mixing",
            "MAE 270 Multidisciplinary Design Optimization",
            "MAE 279 Uncertainty Quantification",
            "MAE 290C Computational Fluid Dynamics",
        ],
        "minimum_gpa": 3.0,
        "courses_letter_graded": True,
        "internship_required": False,
        "internship_available_for_credit": None,
        "thesis_required": False,
        "thesis_route_available": True,
        "capstone_route_available": True,
        "individual_lab_place_guaranteed": False,
        "duration_quarters_minimum": 3,
        "duration_quarters_maximum": 7,
        "curriculum_risk": "low",
        "verification_notes": bi(
            "Plan II is a structured nine-course Aerospace Engineering Systems curriculum. Plan I instead uses six courses plus 12 research units and requires an adviser, thesis and defense; an individual adviser or lab place is not guaranteed.",
            "Plan II yapılandırılmış dokuz derslik Aerospace Engineering Systems müfredatıdır. Plan I ise altı ders ve 12 araştırma birimi kullanır; danışman, tez ve savunma gerektirir. Bireysel danışman veya laboratuvar yeri garanti değildir.",
        ),
    }

    row["category_profile"] = {
        "primary_categories": ["aerospace_space_systems", "aerodynamics_fluid_mechanics"],
        "secondary_categories": ["propulsion_combustion", "astrodynamics", "cfd", "optimization", "controls", "structures"],
        "technical_focus": bi(
            "Quantitative methods, fluid mechanics, heat transfer, combustion and propulsion, space flight mechanics, optimization and CFD.",
            "Nicel yöntemler, akışkanlar mekaniği, ısı transferi, yanma ve itki, uzay uçuş mekaniği, optimizasyon ve HAD.",
        ),
        "verification_notes": bi("Normalized from the current official MC75 curriculum.", "Güncel resmî MC75 müfredatından normalize edilmiştir."),
    }

    row["research_profile"] = {
        "research_focus_areas": [
            bi("Aerospace vehicle and multidisciplinary design optimization", "Havacılık-uzay aracı ve çok disiplinli tasarım optimizasyonu"),
            bi("Computational and multiscale flow physics", "Hesaplamalı ve çok ölçekli akış fiziği"),
            bi("Combustion, propulsion and thermal sciences", "Yanma, itki ve termal bilimler"),
            bi("Astrodynamics, cislunar dynamics and space-domain awareness", "Astrodinamik, Ay çevresi dinamiği ve uzay alan farkındalığı"),
            bi("Reduced-order modeling, control and uncertainty quantification", "İndirgenmiş mertebeli modelleme, kontrol ve belirsizlik nicelendirme"),
        ],
        "key_institutes": [
            {"name": "Large-Scale Design Optimization Lab", "url": LSDO},
            {"name": "Kramer Computational Methods Group", "url": KRAMER},
            {"name": "Saha Lab", "url": SAHA},
            {"name": "Multiscale Flow Physics Group", "url": SANCHEZ},
            {"name": "Computational Flow Physics Group", "url": FLOW},
        ],
        "department_research_areas": ["solid mechanics", "materials", "fluid mechanics and heat transfer", "dynamics systems and controls", "combustion and energy", "plasmas"],
        "faculty_contact_for_research_allowed": True,
        "individual_lab_place_guaranteed": False,
        "research_funding_level": "unknown",
        "research_risk": "medium",
        "verification_notes": bi(
            "The department and aerospace faculty page verify the research breadth and named labs. A student's access depends on adviser, capacity, funding and any project restrictions.",
            "Bölüm ve aerospace öğretim üyesi sayfası araştırma genişliğini ve adlandırılmış laboratuvarları doğrular. Öğrenci erişimi danışman, kapasite, finansman ve proje kısıtlarına bağlıdır.",
        ),
    }

    row["industry_ecosystem_profile"] = {
        "local_industry_strength": "high",
        "verified_research_collaborations": [
            {
                "name": "NASA University Leadership Initiative - aerospace vehicle design",
                "evidence_url": LSDO,
                "student_participation_guaranteed": False,
            },
            {
                "name": "US Space Force / AFRL-supported xGEO and xRADAR cislunar research network",
                "evidence_url": CISLUNAR,
                "student_participation_guaranteed": False,
            },
        ],
        "verified_partnerships": [
            "NASA University Leadership Initiative",
            "US Space Force / Air Force Research Laboratory cislunar research network",
        ],
        "key_companies": [],
        "outcomes_are_partnership_evidence": False,
        "international_student_export_control_risk": "project_specific",
        "export_control_detail": bi(
            "Fundamental research is generally shareable, but ITAR-controlled technical data, certain EAR-controlled technology and sponsor-restricted projects can require licenses or restricted access for non-US persons. This is project-specific, not a blanket program exclusion.",
            "Temel araştırma genellikle paylaşılabilir; ancak ITAR kontrollü teknik veri, belirli EAR kontrollü teknoloji ve sponsor kısıtlı projeler ABD kişisi olmayanlar için lisans veya erişim kısıtı gerektirebilir. Bu program geneli yasak değil, projeye özgüdür.",
        ),
        "industry_risk": "export_control_and_defense_access_project_specific",
        "verification_notes": bi(
            "Only collaborations confirmed by UC San Diego or a linked official lab page are listed. Nearby employers are not treated as partners.",
            "Yalnızca UC San Diego veya bağlantılı resmî laboratuvar sayfasınca doğrulanan iş birlikleri listelenir. Yakındaki işverenler ortak sayılmaz.",
        ),
    }

    row["application_timeline_profile"] = {
        "application_period": "Fall only",
        "application_opening": "Fall 2026; exact opening date not stated on the checked MAE page",
        "pre_enrollment_required": False,
        "visa_complexity": "high",
        "application_deadline": "2027-01-13",
        "non_eu_deadline": "2027-01-13",
        "deadline_eu": "2027-01-13",
        "deadline_non_eu": "2027-01-13",
        "deadline_time_zone": None,
        "late_applications_accepted": False,
        "application_rounds": [
            {
                "intake": "Fall 2027",
                "deadline": "2027-01-13",
                "deadline_type": "final",
                "applicant_scope": "MS applicants",
                "gre_required": False,
            }
        ],
        "review_begins": "January 2027",
        "typical_ms_decision_window": "March-June 2027",
        "fall_only_admission": True,
        "materials_after_deadline_policy": "scores and recommendations may be added, but the file is not reviewed until included",
        "i20_request_earliest_for_fall": "December 1",
        "i20_request_latest_for_timely_processing_for_fall": "August 1",
        "i20_processing_time_peak": "up to approximately three weeks after a complete request",
        "i20_expedite_available_for_new_admits": False,
        "visa_steps": [
            bi("Accept the admission offer and complete UC San Diego account setup.", "Kabul teklifini kabul edin ve UC San Diego hesap kurulumunu tamamlayın."),
            bi("Request the New Admit Form I-20 in iServices with passport and acceptable funding documents.", "iServices'ta pasaport ve uygun finansman belgeleriyle New Admit Form I-20 talebi verin."),
            bi("Show at least the published ISEO financial estimate; current 2026 page lists $73,507 for one academic year for standard graduate programs.", "En az yayımlanmış ISEO finansal tahminini gösterin; güncel 2026 sayfası standart lisansüstü programlar için bir akademik yıla 73.507 $ listeler."),
            bi("After receiving the I-20, follow the F-1 visa process; do not schedule the visa interview before the I-20 arrives.", "I-20 geldikten sonra F-1 vize sürecini izleyin; I-20 gelmeden vize görüşmesi planlamayın."),
            bi("Complete the mandatory international graduate orientation after arrival.", "Varıştan sonra zorunlu uluslararası lisansüstü oryantasyonunu tamamlayın."),
        ],
        "post_admission_document_evaluation": bi(
            "Admitted applicants with degree(s) from outside the United States must submit a course-by-course evaluation through a listed provider to finalize admission; this is not required to request the I-20.",
            "ABD dışından derece sahibi kabul edilen adaylar, kabulü kesinleştirmek için listelenen sağlayıcılardan ders bazlı değerlendirme sunmalıdır; bu I-20 talebi için zorunlu değildir.",
        ),
        "timeline_risk": "medium",
        "verification_notes": bi(
            "The current Fall 2027 MAE page explicitly publishes January 13, 2027 for MS and says late applications cannot be accepted. No deadline estimate is used.",
            "Güncel Fall 2027 MAE sayfası MS için 13 Ocak 2027'yi açıkça yayımlar ve geç başvuru kabul edilmediğini söyler. Son tarih tahmini kullanılmaz.",
        ),
    }

    row["student_sentiment_profile"] = {
        "student_satisfaction_score": None,
        "workload_sentiment": "unknown",
        "teaching_quality_sentiment": "unknown",
        "administration_sentiment": "mixed_negative_for_i20_processing_anecdotes",
        "housing_sentiment": "mixed_negative_due_to_waitlist_uncertainty",
        "city_life_sentiment": "unknown",
        "international_student_sentiment": "mixed_negative_for_i20_processing_anecdotes",
        "career_support_sentiment": "unknown",
        "student_sentiment_summary": bi(
            "A small recent sample reports graduate-housing waitlist uncertainty and some I-20 delays during the 2026 peak season. Other housing posts describe successful offers. These are perception signals only.",
            "Küçük ve yakın tarihli örneklem, lisansüstü konut bekleme listesi belirsizliği ve 2026 yoğun döneminde bazı I-20 gecikmeleri bildirir. Diğer konut paylaşımları başarılı teklifleri anlatır. Bunlar yalnızca algı sinyalidir.",
        ),
        "student_sentiment_sources": [REDDIT_HOUSING_OFFER, REDDIT_HOUSING_QUESTIONS, REDDIT_I20],
        "approximate_sample_size": 14,
        "date_range": "2026-06 to 2026-07",
        "sentiment_confidence": "low",
        "verification_notes": bi(
            "No satisfaction score is calculated. Anonymous posts do not establish official processing times, housing availability, academic quality or career outcomes.",
            "Memnuniyet puanı hesaplanmaz. Anonim paylaşımlar resmî işlem sürelerini, konut bulunurluğunu, akademik kaliteyi veya kariyer sonuçlarını kanıtlamaz.",
        ),
    }

    sources = [
        source(PROGRAM, "UC San Diego MAE Graduate Program Overview", "official_program_page", ["program", "major_code", "research_links"], "Active MAE graduate program and MC75 Aerospace Engineering major code.", "Aktif MAE lisansüstü programı ve MC75 Aerospace Engineering ana dal kodu."),
        source(ADMISSION, "UC San Diego MAE Fall 2027 Graduate Admissions", "official_admission_page", ["deadline", "admission", "non_eu_eligibility", "gre", "english", "documents", "funding", "housing"], "Current Fall 2027 MS deadline, international application rules, GRE-optional policy, documents, GPA, English thresholds, MS funding warning and housing warning.", "Güncel Fall 2027 MS tarihi, uluslararası başvuru kuralları, GRE-isteğe bağlı politikası, belgeler, GPA, İngilizce eşikleri, MS finansman ve konut uyarıları."),
        source(CURRICULUM, "UC San Diego MAE Master of Science Programs", "official_curriculum_page", ["program", "duration", "curriculum", "units", "course_count", "thesis", "comprehensive_exam"], "Current MC75 Plan I/II requirements and Aerospace Engineering Systems curriculum.", "Güncel MC75 Plan I/II şartları ve Aerospace Engineering Systems müfredatı."),
        source(COURSES, "UC San Diego MAE Course Offerings 2026-27", "official_curriculum_page", ["course_availability", "curriculum"], "Current annual graduate course-offering matrix; listed catalog courses are not assumed to run every year.", "Güncel yıllık lisansüstü ders açılma matrisi; katalogdaki her dersin her yıl açıldığı varsayılmaz."),
        source(APP_FEE, "UC San Diego Graduate Application Fee Questions", "official_admission_page", ["application_fee", "fee_waiver"], "Current $155 international fee and waiver timing/process.", "Güncel 155 $ uluslararası ücret ve muafiyet zamanlama/süreci."),
        source(FEES, "UC San Diego 2026-27 Graduate Registration Fees", "official_tuition_page", ["tuition", "fees", "insurance", "nrst", "visa_fee"], "Final itemized annual resident/nonresident charges, SHIP, one-time enrollment and international visa-administration fees.", "Kalemli yıllık yerleşik/eyalet dışı ücretler, SHIP, tek seferlik kayıt ve uluslararası vize-idare ücreti."),
        source(COA, "UC San Diego 2026-27 Graduate Cost of Attendance", "official_cost_of_living_page", ["coa", "housing", "food", "books", "personal", "transportation"], "JavaScript-loaded 2026-27 on/off-campus nonresident planning budgets, inspected in the live page.", "Canlı sayfada incelenen JavaScript yüklü 2026-27 kampüs içi/dışı eyalet dışı planlama bütçeleri.", access_status="requires_js"),
        source(ASE, "UC San Diego ASE Fee Payment Information", "official_scholarship_page", ["funding", "fee_remission", "insurance"], "Terms for qualifying ASE SHIP and partial fee remission; not an appointment guarantee.", "Uygun ASE SHIP ve kısmi ücret muafiyeti şartları; atama garantisi değildir."),
        source(HOUSING_APPLY, "UC San Diego Graduate and Family Housing Waitlist", "official_housing_page", ["housing", "application", "waitlist"], "Separate waitlist application and current incoming-student temporary-account process.", "Ayrı bekleme listesi başvurusu ve güncel yeni öğrenci geçici hesap süreci."),
        source(HOUSING_FAQ, "UC San Diego Housing Applicant FAQ", "official_housing_page", ["housing", "priority", "waitlist", "offers", "contract"], "Priority order, SHORE limits, quarterly update, offer-response and two-year agreement rules.", "Öncelik sırası, SHORE sınırları, çeyreklik güncelleme, teklif yanıtı ve iki yıllık sözleşme kuralları."),
        source(NUEVO_EAST, "UC San Diego Nuevo East 2026-27 Rates", "official_housing_page", ["housing_rate", "utilities"], "Current occupancy-specific monthly graduate-housing rates.", "Güncel doluluk tipine özgü aylık lisansüstü konut oranları."),
        source(ONE_MIRAMAR, "UC San Diego One Miramar Street Rates", "official_housing_page", ["housing_rate"], "Additional official graduate-housing price context.", "Ek resmî lisansüstü konut fiyat bağlamı."),
        source(RESEARCH, "UC San Diego MAE Research Overview", "official_department_page", ["research", "research_areas"], "Department research breadth and faculty-contact guidance.", "Bölüm araştırma genişliği ve öğretim üyesiyle iletişim rehberi."),
        source(AEROSPACE, "UC San Diego MAE Aerospace Research Area", "official_department_page", ["research", "aerospace_faculty", "labs"], "Current aerospace-associated faculty and linked lab sites.", "Güncel aerospace ilişkili öğretim üyeleri ve bağlantılı laboratuvar siteleri."),
        source(LSDO, "UC San Diego Large-Scale Design Optimization Lab", "official_lab_page", ["research", "optimization", "aerospace", "nasa_collaboration"], "Aerospace vehicle, eVTOL, airliner and CubeSat design optimization and NASA ULI project.", "Havacılık-uzay aracı, eVTOL, uçak ve CubeSat tasarım optimizasyonu ile NASA ULI projesi."),
        source(KRAMER, "UC San Diego Kramer Computational Methods Group", "official_lab_page", ["research", "model_reduction", "control", "uncertainty"], "Current reduced-order modeling, control, design and uncertainty research.", "Güncel indirgenmiş modelleme, kontrol, tasarım ve belirsizlik araştırması."),
        source(SAHA, "UC San Diego Saha Lab", "official_lab_page", ["research", "combustion", "fluid_mechanics"], "Official aerospace-faculty laboratory page.", "Resmî aerospace öğretim üyesi laboratuvar sayfası."),
        source(SANCHEZ, "UC San Diego Multiscale Flow Physics Group", "official_lab_page", ["research", "flow", "combustion", "propulsion"], "Official flow-physics group led by the MC75 program lead.", "MC75 program liderinin resmî akış fiziği grubu."),
        source(FLOW, "UC San Diego Computational Flow Physics", "official_lab_page", ["research", "cfd", "flow_physics"], "Official computational flow-physics group.", "Resmî hesaplamalı akış fiziği grubu."),
        source(CISLUNAR, "UC San Diego Cislunar Space Research and Space Domain Awareness", "official_department_page", ["research", "space", "afrl", "space_force"], "Confirmed USSF/AFRL-supported cislunar research and education network; no individual access guarantee.", "Doğrulanmış USSF/AFRL destekli Ay çevresi araştırma ve eğitim ağı; bireysel erişim garantisi yoktur."),
        source(EXPORT, "UC San Diego Researcher Guidance on Export Control", "official_government_or_policy_page", ["export_control", "international_access"], "Current project-specific ITAR/EAR and non-US-person guidance.", "Güncel projeye özgü ITAR/EAR ve ABD kişisi olmayanlara yönelik rehber."),
        source(I20, "UC San Diego Request the Form I-20", "official_visa_page", ["visa", "i20", "timeline", "documents"], "Current fall request window, documents, iServices process and peak processing time.", "Güncel güz talep aralığı, belgeler, iServices süreci ve yoğun dönem işlem süresi."),
        source(I20_FUNDING, "UC San Diego I-20/DS-2019 Funding Requirements for 2026", "official_visa_page", ["visa", "proof_of_funds", "funding_documents"], "Published $73,507 standard graduate proof amount and acceptable documents; table is based on November 2025 COA figures.", "Yayımlanmış 73.507 $ standart lisansüstü kanıt tutarı ve kabul edilen belgeler; tablo Kasım 2025 COA rakamlarına dayanır.", confidence="medium"),
        source(INTL_ADMITTED, "UC San Diego Admitted International Students", "official_admission_page", ["international_documents", "course_evaluation", "i20", "orientation"], "Post-admission course-by-course evaluation, I-20 invitation, passport and orientation steps.", "Kabul sonrası ders bazlı değerlendirme, I-20 daveti, pasaport ve oryantasyon adımları."),
        source(QS, "QS - University of California, San Diego", "ranking_provider", ["prestige"], "QS World University Ranking 2027: #81; institutional context only.", "QS Dünya Üniversite Sıralaması 2027: #81; yalnızca kurumsal bağlam.", confidence="medium"),
        source(REDDIT_HOUSING_OFFER, "Reddit r/UCSD - Nuevo East graduate housing offer", "student_forum", ["housing_sentiment"], "Recent offer and second-offer anecdotes; perception only.", "Yakın tarihli teklif ve ikinci teklif anekdotları; yalnızca algı.", confidence="low"),
        source(REDDIT_HOUSING_QUESTIONS, "Reddit r/UCSD - Graduate housing questions", "student_forum", ["housing_sentiment"], "Recent waitlist, unit and heat anecdotes; perception only.", "Yakın tarihli bekleme listesi, birim ve sıcaklık anekdotları; yalnızca algı.", confidence="low"),
        source(REDDIT_I20, "Reddit r/UCSD - 2026 I-20 delay discussion", "student_forum", ["international_student_sentiment", "administration_sentiment"], "Small recent peak-season delay sample; not an official processing-time source.", "Küçük yakın tarihli yoğun dönem gecikme örneklemi; resmî işlem süresi kaynağı değildir.", confidence="low"),
    ]

    row["source_profile"] = {
        "primary_url": CURRICULUM,
        "secondary_urls": [item["url"] for item in sources if item["url"] != CURRICULUM],
        "last_verified": TODAY,
        "field_confidence": {
            "program_basic_info": "high",
            "program": "high",
            "duration": "high",
            "language": "unknown",
            "english_proficiency": "high",
            "admission": "high",
            "gre": "high",
            "non_eu_eligibility": "high",
            "tuition": "high",
            "scholarship": "high",
            "deadline": "high",
            "curriculum": "high",
            "research": "high",
            "industry_ecosystem": "medium",
            "housing": "high",
            "living": "high",
            "visa": "high",
            "sentiment": "low",
            "prestige": "medium",
        },
        "source_reliability": "high",
        "verification_status": "partially_verified",
        "needs_verification": True,
        "verification_notes": bi(
            "The prior shallow record is rebuilt with the current Fall 2027 deadline, GRE policy, 2026-27 fees/COA, curriculum routes, housing waitlist, I-20 process, laboratories and verified collaborations. Teaching language remains explicitly unverified.",
            "Önceki sığ kayıt güncel Fall 2027 tarihi, GRE politikası, 2026-27 ücret/COA, müfredat yolları, konut bekleme listesi, I-20 süreci, laboratuvarlar ve doğrulanmış iş birlikleriyle yeniden kuruldu. Öğretim dili açıkça doğrulanmamış kalır.",
        ),
        "source_log": sources,
    }

    row["decision_summary"] = {
        "best_for": [
            bi("Students seeking a compact, technically rigorous one-year-capable aerospace systems curriculum with astrodynamics, propulsion and CFD options.", "Astrodinamik, itki ve HAD seçenekli, yoğun ve teknik açıdan güçlü, bir yılda tamamlanabilen aerospace systems müfredatı arayan öğrenciler."),
            bi("Students interested in thesis or structured comprehensive-exam routes and UC San Diego aerospace research groups.", "Tez veya yapılandırılmış kapsamlı sınav yolları ile UC San Diego aerospace araştırma gruplarıyla ilgilenen öğrenciler."),
        ],
        "not_ideal_for": [
            bi("International MS applicants who require guaranteed funding or guaranteed university housing.", "Garantili finansman veya üniversite konutuna ihtiyaç duyan uluslararası MS adayları."),
            bi("Students who need unrestricted access to every defense- or space-related project.", "Savunma veya uzayla ilgili her projeye kısıtsız erişim isteyen öğrenciler."),
        ],
        "main_strengths": [
            bi("Current MC75 curriculum combines fluids, compressible flow, thermal sciences and space flight mechanics.", "Güncel MC75 müfredatı akışkanlar, sıkıştırılabilir akış, termal bilimler ve uzay uçuş mekaniğini birleştirir."),
            bi("Plan I thesis and Plan II comprehensive-exam routes are both available.", "Plan I tez ve Plan II kapsamlı sınav yollarının ikisi de vardır."),
            bi("Named laboratories span design optimization, CFD, combustion, model reduction and controls.", "Adlandırılmış laboratuvarlar tasarım optimizasyonu, HAD, yanma, indirgenmiş modelleme ve kontrolü kapsar."),
        ],
        "main_risks": [
            bi("First-year direct university charges for a new international student are approximately $38,294.17 with SHIP and separately listed first-time fees; the off-campus COA budget is $76,821.", "Yeni uluslararası öğrenci için ilk yıl doğrudan üniversite ücretleri SHIP ve ayrıca listelenen ilk sefer ücretleriyle yaklaşık 38.294,17 $; kampüs dışı COA bütçesi 76.821 $'dır."),
            bi("MAE says MS students should not expect RA/TA support.", "MAE, MS öğrencilerinin RA/TA desteği beklememesi gerektiğini söyler."),
            bi("Graduate housing is a separate waitlist and is not guaranteed.", "Lisansüstü konut ayrı bir bekleme listesidir ve garanti değildir."),
            bi("Some aerospace/defense projects may impose project-specific export-control restrictions on non-US persons.", "Bazı havacılık-uzay/savunma projeleri ABD kişisi olmayanlara projeye özgü ihracat kontrolü kısıtları getirebilir."),
            bi("The teaching language is not explicitly stated in the checked official sources.", "Öğretim dili kontrol edilen resmî kaynaklarda açıkça belirtilmez."),
        ],
        "decision_summary": bi(
            "UC San Diego MC75 is a strong technical fit for aerospace systems, especially fluids, propulsion, space flight mechanics, optimization and computational methods. Apply by January 13, 2027; GRE is optional, three recommendations are required, and self-funding plus an off-campus housing backup is the prudent baseline.",
            "UC San Diego MC75 özellikle akışkanlar, itki, uzay uçuş mekaniği, optimizasyon ve hesaplamalı yöntemlerde aerospace systems için güçlü teknik uyumdur. 13 Ocak 2027'ye kadar başvurun; GRE isteğe bağlıdır, üç referans gerekir ve öz-finansman ile kampüs dışı konut yedeği ihtiyatlı temel plandır.",
        ),
        "pros": [],
        "cons": [],
        "verdict": bi(
            "Excellent technical curriculum and research fit; financially safe only with a credible self-funding plan and housing backup.",
            "Mükemmel teknik müfredat ve araştırma uyumu; yalnızca güvenilir öz-finansman planı ve konut yedeğiyle finansal olarak güvenli.",
        ),
    }

    row["scoring_inputs"] = {
        "academic_prestige": None,
        "research_output": None,
        "industry_links": None,
        "affordability": None,
        "admission_chance": None,
        "living_quality": None,
        "hard_flags": [
            "teaching_language_unverified",
            "terminal_ms_funding_not_expected",
            "high_nonresident_cost",
            "graduate_housing_not_guaranteed",
            "complete_program_cost_unknown",
            "i20_financial_table_uses_older_coa_basis",
            "export_control_access_project_specific",
        ],
    }

    row["data_quality"] = {
        "status": "partial",
        "checked_official_source_count": 24,
        "verified_fields": [
            "program", "degree", "major_code", "duration", "admission", "gre", "non_eu_eligibility",
            "english_proficiency", "tuition", "cost_of_attendance", "scholarship", "deadline", "curriculum",
            "research", "industry_collaboration", "housing", "living", "visa", "insurance_requirement", "prestige",
        ],
        "unverified_critical_fields": ["language"],
        "known_semantic_gaps": [
            "explicit_teaching_language",
            "fixed_complete_program_cost",
            "admission_rate",
            "private_market_rent",
            "guaranteed_individual_lab_access",
            "international_eligibility_for_individual_restricted_projects",
            "international_fee_waiver_eligibility",
        ],
        "official_source_conflicts": ["registrar_direct_charges_vs_financial_aid_coa_direct_layer", "current_fee_schedule_vs_i20_table_basis_date"],
        "has_checked_source_log": True,
        "audited_at": TODAY,
    }

    row["quality_control"] = {
        "checked_at": TODAY,
        "qc_status": "needs_revision",
        "remaining_verification_tasks": [
            bi("Find a current official source explicitly stating the teaching language.", "Öğretim dilini açıkça belirten güncel resmî kaynak bulun."),
            bi("Recheck the live application, fee and I-20 proof tables immediately before submission/payment.", "Gönderim/ödeme öncesi canlı başvuru, ücret ve I-20 kanıt tablolarını yeniden kontrol edin."),
            bi("Confirm project-specific international access with the prospective adviser or laboratory.", "Projeye özgü uluslararası erişimi olası danışman veya laboratuvarla doğrulayın."),
        ],
        "qc_notes": bi(
            "Obsolete fees, missing current deadline, unsupported company partnerships, fabricated scores and unsupported academic sentiment were removed or replaced with sourced evidence.",
            "Eski ücretler, eksik güncel son tarih, kaynaksız şirket ortaklıkları, uydurma puanlar ve kaynaksız akademik duygu analizi kaldırıldı veya kaynaklı kanıtla değiştirildi.",
        ),
        "failed_canary_tests": ["teaching_language_not_explicitly_verified"],
    }

    DATA_PATH.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    audit = {
        "record_id": row["id"],
        "checked_at": TODAY,
        "validation_method": "current official web search/open validation, live JavaScript COA inspection, and source-by-source semantic review",
        "audit_validity": "valid",
        "summary": {
            "total_urls": len(sources),
            "official_urls": 24,
            "reliable_third_party_urls": 1,
            "student_forum_urls": 3,
            "ok_or_indexed_html": sum(item["access_status"] == "ok" for item in sources),
            "requires_js": sum(item["access_status"] == "requires_js" for item in sources),
            "pdf": sum(item["access_status"] == "pdf" for item in sources),
            "broken": 0,
        },
        "results": [
            {
                "url": item["url"],
                "title": item["title"],
                "source_type": item["source_type"],
                "access_status": item["access_status"],
                "last_checked": item["last_checked"],
            }
            for item in sources
        ],
        "notes": bi(
            "Critical claims use official sources. Reddit is used only for conservative housing and administration sentiment. No broken URL is retained as primary evidence.",
            "Kritik iddialar resmî kaynakları kullanır. Reddit yalnızca ihtiyatlı konut ve idare algısı için kullanılır. Hiçbir bozuk URL birincil kanıt olarak tutulmaz.",
        ),
    }
    AUDIT_PATH.parent.mkdir(parents=True, exist_ok=True)
    AUDIT_PATH.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "id": row["id"],
                "program_name": row["program_name"],
                "status": row["data_quality"]["status"],
                "source_count": len(sources),
                "official_source_count": row["data_quality"]["checked_official_source_count"],
                "unverified": row["data_quality"]["unverified_critical_fields"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
