"""Apply the source-checked 2026 UC Berkeley ME MEng Aerospace update.

The target is the professional MEng in Mechanical Engineering with the
Aerospace Engineering concentration.  It is not Berkeley's research MS and
does not inherit guarantees from the undergraduate Aerospace programme.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data_base" / "amerika.json"
AUDIT_PATH = ROOT / "reports" / "source_link_audit_uc_berkeley_me_meng_2026-08-14.json"
TODAY = "2026-08-14"

PROGRAM = "https://me.berkeley.edu/graduate/meng/"
ME_ADMISSIONS = "https://me.berkeley.edu/graduate/admissions/"
MENG_APPLICATION = "https://me.berkeley.edu/graduate/meng-admissions/"
CENTRAL_REQUIREMENTS = "https://grad.berkeley.edu/admissions/application-process/requirements/"
CENTRAL_FAQ = "https://grad.berkeley.edu/admissions/application-process/faq/"
CONCENTRATIONS = "https://me.berkeley.edu/graduate/meng-concentrations/"
DEGREE_REQUIREMENTS = "https://me.berkeley.edu/graduate/meng/meng-degree-requirements/"
CANDIDACY_FORM = "https://me.berkeley.edu/wp-content/uploads/2019/01/Candidacy_M.Eng_.pdf"
TUITION_FUNDING = "https://funginstitute.berkeley.edu/programs-centers/full-time-program/learn-more/tuition-financial-aid/"
NEW_ADMIT_COST = "https://funginstitute.berkeley.edu/newadmit/resources/"
MENG_FAQ = "https://funginstitute.berkeley.edu/programs-centers/full-time-program/learn-more/application-faq/"
CAPSTONE = "https://funginstitute.berkeley.edu/programs-centers/full-time-program/capstone-experience/"
CAPSTONE_FORMAT = "https://funginstitute.berkeley.edu/programs-centers/full-time-program/capstone-experience/project-format/"
CAREER = "https://funginstitute.berkeley.edu/career/programming/"
EMPLOYMENT = "https://funginstitute.berkeley.edu/career/employment-data/"
HOUSING_APPLY = "https://housing.berkeley.edu/apply/"
HOUSING_GRAD = "https://housing.berkeley.edu/apply/how-to-apply-for-graduate-housing/"
HOUSING_DATES = "https://housing.berkeley.edu/apply/dates-deadlines/"
HOUSING_ASSIGNMENT = "https://housing.berkeley.edu/apply/how-to-apply-for-graduate-housing/graduate-housing-assignment-process-and-offers/"
HOUSING_RATES = "https://housing.berkeley.edu/rates-contracts-policies/rates/"
NIF = "https://internationaloffice.berkeley.edu/students/nif"
F1_WORK = "https://internationaloffice.berkeley.edu/students/employment/oncampus"
EXPORT = "https://rac.berkeley.edu/ec/visitor.html"
CONTROLS = "https://me.berkeley.edu/research-areas-and-major-fields/controls/"
FLUID_LAB = "https://me.berkeley.edu/laboratories/fluid-mechanics-laboratory/"
MECHANICS = "https://me.berkeley.edu/research-areas-and-major-fields/mechanics/"
MATERIALS = "https://me.berkeley.edu/research-areas-and-major-fields/materials/"
ENERGY = "https://me.berkeley.edu/research-areas-and-major-fields/energy-science-and-technology/"
AIRSPACE = "https://airspacecenter.berkeley.edu/academic-engagement/research-clusters"
AIRSPACE_FAQ = "https://airspacecenter.berkeley.edu/Faq-page"
QS = "https://www.topuniversities.com/universities/university-california-berkeley-ucb"
REDDIT_ME = "https://www.reddit.com/r/berkeley/comments/1dw94m3"
REDDIT_CAPSTONE = "https://www.reddit.com/r/berkeley/comments/1vcszfp/any_advice_on_meng_capstone_choice/"
REDDIT_EXPERIENCE = "https://www.reddit.com/r/gradadmissions/comments/1rtaqj8/any_uc_berkeley_meng_student_here/"


def bi(en: str, tr: str) -> dict[str, str]:
    return {"en": en, "tr": tr}


def source(
    url: str,
    title: str,
    kind: str,
    fields: list[str],
    en: str,
    tr: str,
    *,
    access_status: str = "ok",
    confidence: str = "high",
) -> dict:
    return {
        "url": url,
        "title": title,
        "source_type": kind,
        "access_status": access_status,
        "last_checked": TODAY,
        "relevant_fields": fields,
        "confidence": confidence,
        "notes": bi(en, tr),
    }


def main() -> None:
    records = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    row = next(item for item in records if item.get("id") == "uc-berkeley-me")

    row.update({
        "country": "United States",
        "university": "University of California, Berkeley",
        "university_native_name": "University of California, Berkeley (UC Berkeley)",
        "university_aliases": ["UC Berkeley", "Berkeley", "UCB", "Cal"],
        "city": "Berkeley",
        "region": "California",
        "program_name": "Master of Engineering in Mechanical Engineering — Aerospace Engineering concentration",
        "program_native_name": "Master of Engineering in Mechanical Engineering — Aerospace Engineering concentration",
        "program_degree": "MEng",
        "degree_level": "Master",
        "duration_years": 1,
        "duration": bi(
            "Full-time route: nine months, fall and spring, with August and January leadership boot camps.",
            "Tam zamanlı yol: dokuz ay, güz ve bahar; Ağustos ve Ocak liderlik boot camp'leriyle.",
        ),
        "ects": None,
        "berkeley_semester_units": 25,
        "teaching_language": ["Unknown"],
        "program_url": PROGRAM,
        "program_status": "active",
        "relevance_status": "strong",
        "delivery_modes": ["on_campus"],
        "full_time_available": True,
        "part_time_route_available": True,
        "part_time_duration_years_min": 2,
        "part_time_duration_years_max": 4,
        "part_time_international_student_visa_compatibility": None,
        "qs_ranking": 20,
        "qs_ranking_display": "=20",
        "qs_ranking_year": 2027,
    })

    row["prestige_profile"] = {
        "qs_world_rank": 20,
        "qs_display_rank": "=20",
        "qs_edition": 2027,
        "qs_source_url": QS,
        "interpretation": bi(
            "The institutional QS rank is context only. Aerospace fit is established separately from the concentration, course requirements, capstone and relevant ME research areas.",
            "Kurumsal QS sırası yalnızca bağlamdır. Havacılık-uzay uygunluğu concentration, ders şartları, capstone ve ilgili ME araştırma alanlarıyla ayrıca kanıtlanır.",
        ),
    }

    row["eligibility_profile"] = {
        "eligible_for_non_eu": True,
        "eligible_for_international_applicants": True,
        "international_evidence": bi(
            "The MEng application publishes international transcript and English-test rules, and the programme FAQ reports a 68% international-by-passport Class of 2024.",
            "MEng başvurusu uluslararası transkript ve İngilizce sınav kurallarını yayımlar; program SSS'si 2024 sınıfının pasaporta göre %68 uluslararası olduğunu bildirir.",
        ),
        "required_previous_degree": bi(
            "A bachelor's degree or recognised equivalent from an accredited institution.",
            "Akredite bir kurumdan lisans derecesi veya tanınmış eşdeğeri.",
        ),
        "required_preparation": bi(
            "Enough undergraduate preparation for graduate work and a strong technical background equivalent to an engineering bachelor's degree.",
            "Lisansüstü çalışma için yeterli lisans hazırlığı ve mühendislik lisansına eşdeğer güçlü teknik altyapı.",
        ),
        "accepted_backgrounds": [
            bi("Engineering", "Mühendislik"),
            bi("Related quantitative science with adequate engineering preparation", "Yeterli mühendislik hazırlığı olan ilgili nicel bilim"),
        ],
        "minimum_gpa_us_4_scale": 3.0,
        "minimum_gpa_context": bi(
            "Berkeley describes 3.0 (B) as the usual minimum. Meeting the minimum does not guarantee admission; the department says qualified applicants exceed available places.",
            "Berkeley 3,0 (B) değerini olağan asgari olarak tanımlar. Asgariyi sağlamak kabul garantisi değildir; bölüm nitelikli adayların kontenjandan fazla olduğunu belirtir.",
        ),
        "admission_mode": "direct_professional_meng",
        "admission_risk": "high",
        "selection_method": "holistic_competitive",
        "spring_entry_available": False,
        "one_program_per_admission_cycle": True,
        "work_experience_required": False,
        "interview_required": None,
        "application_fee_usd_international": 155,
        "application_fee_payment_due_days_after_deadline": 3,
        "international_fee_waiver_available": False,
        "fee_waiver_scope": bi(
            "Graduate Division fee waivers are limited to eligible US citizens/current permanent residents and certain undocumented applicants; ME does not waive the fee. UC Berkeley undergraduates have a programme waiver.",
            "Graduate Division ücret muafiyetleri uygun ABD vatandaşları/mevcut kalıcı oturum sahipleri ve belirli belgesiz adaylarla sınırlıdır; ME ücreti kaldırmaz. UC Berkeley lisans öğrencileri için program muafiyeti vardır.",
        ),
        "required_documents": [
            bi("Online graduate application", "Çevrim içi lisansüstü başvuru"),
            bi("Unofficial transcript/academic record from every higher-education institution", "Her yükseköğretim kurumundan resmî olmayan transkript/akademik kayıt"),
            bi("English translations plus original-language academic records when applicable", "Gerektiğinde İngilizce çeviriler ve özgün dilde akademik kayıtlar"),
            bi("Two letters of recommendation", "İki referans mektubu"),
            bi("Statement of purpose", "Niyet mektubu"),
            bi("Personal history statement", "Kişisel geçmiş beyanı"),
            bi("MEng programme-page GPA fields", "MEng program sayfası GNO alanları"),
        ],
        "optional_documents": [bi("CV/resume is preferred but optional", "CV/özgeçmiş tercih edilir ancak isteğe bağlıdır")],
        "writing_sample_required": False,
        "official_transcripts_at_application": False,
        "post_submission_transcript_updates_accepted": False,
        "gre": {
            "policy": "not_required",
            "cycle": "Fall 2027",
            "minimum_scores": {},
            "source_ids": [MENG_APPLICATION, ME_ADMISSIONS],
            "verification_notes": bi(
                "The current ME application and department admissions pages state that GRE scores are not required for Fall 2027. Older programme-page percentile context is not treated as a current recommendation or threshold.",
                "Güncel ME başvuru ve bölüm kabul sayfaları 2027 güz dönemi için GRE puanının gerekmediğini belirtir. Eski program sayfasındaki yüzdelik bağlam güncel öneri veya eşik sayılmaz.",
            ),
        },
    }

    row["language_profile"] = {
        "teaching_language": ["Unknown"],
        "teaching_languages": ["Unknown"],
        "english_proficiency_required_conditionally": True,
        "english_requirement_scope": bi(
            "Required unless a Graduate Division exemption applies; the rule is based mainly on the country/institution of the bachelor's degree.",
            "Graduate Division muafiyeti yoksa gerekir; kural temel olarak lisans derecesinin ülke/kurumuna dayanır.",
        ),
        "accepted_english_tests": [
            {"test": "TOEFL iBT or iBT Home Edition", "minimum_score_old_scale": 90, "minimum_score_new_scale": 5.0, "minimum_speaking_new_scale": 4.5, "minimum_writing_new_scale": 4.5},
            {"test": "IELTS Academic or IELTS Online", "minimum_score": 7.0, "minimum_speaking_from_2026_01_21": 6.5, "minimum_writing_from_2026_01_21": 6.5},
        ],
        "not_accepted": ["Duolingo English Test", "TOEFL ITP", "TOEFL MyBest Scores", "IELTS Indicator", "IELTS One Skill Retake"],
        "score_scale_transition": {
            "toefl_tests_2025_06_01_to_2026_01_20": "90 total",
            "toefl_tests_on_or_after_2026_01_21": "5 total; 4.5 speaking and writing",
            "ielts_tests_2025_06_01_to_2026_01_20": "7 overall",
            "ielts_tests_on_or_after_2026_01_21": "7 total; 6.5 speaking and writing",
        },
        "fall_2027_oldest_accepted_test_date": "2025-06-01",
        "fall_2027_score_deadline": "2026-12-01T20:59:00-08:00",
        "toefl_institution_code": "4833",
        "ielts_electronic_delivery_required": True,
        "exemption_routes": [
            bi("Basic degree from a recognised institution in a country where English is primary in daily life and academic instruction", "İngilizcenin günlük yaşamda ve akademik öğretimde birincil olduğu ülkedeki tanınmış kurumdan temel derece"),
            bi("Degree from a regionally accredited US institution where instruction is English", "Öğretimin İngilizce olduğu bölgesel akreditasyonlu ABD kurumundan derece"),
            bi("At least one year of full-time graded academic work with B or better at a regionally accredited US institution", "B veya üzeri notlarla bölgesel akreditasyonlu ABD kurumunda en az bir yıllık tam zamanlı notlu akademik çalışma"),
        ],
        "teaching_language_evidence_type": "not_explicitly_published",
        "language_risk": "high",
        "verification_notes": bi(
            "The official pages verify English-proficiency evidence and exact Fall 2027 thresholds, but none of the checked pages explicitly labels the programme's teaching language. Under UniRank's no-inference rule, teaching language remains unknown.",
            "Resmî sayfalar İngilizce yeterlilik belgesini ve 2027 güz dönemi kesin eşiklerini doğrular; ancak kontrol edilen sayfaların hiçbiri program öğretim dilini açıkça etiketlemez. UniRank'in çıkarım yapmama kuralıyla öğretim dili bilinmiyor kalır.",
        ),
    }

    row["curriculum_profile"] = {
        "total_units": 25,
        "unit_system": "UC Berkeley semester units",
        "duration_months_full_time": 9,
        "full_time_terms": ["Fall", "Spring"],
        "minimum_enrollment_units_each_term": 12,
        "course_count_fixed": False,
        "course_count_summary": bi(
            "The degree is 25 units; exact class count varies with the unit values of the four-ish technical selections and leadership electives.",
            "Derece 25 birimdir; kesin ders sayısı yaklaşık dört teknik seçimin ve liderlik seçmelilerinin birim değerlerine göre değişir.",
        ),
        "requirement_components": [
            {"name": bi("ME 200-level coursework in the concentration", "Concentration içindeki ME 200-seviye dersler"), "units": 12},
            {"name": bi("Fung Institute business and leadership curriculum", "Fung Institute işletme ve liderlik müfredatı"), "units": 8},
            {"name": bi("ENGIN 296MA/296MB two-semester capstone", "ENGIN 296MA/296MB iki dönemlik capstone"), "units": 5},
        ],
        "aerospace_concentration_minimum_listed_courses": 2,
        "aerospace_concentration_offering_warning": bi(
            "Students must take at least two courses from the published Aerospace list; the page explicitly says offerings vary by year.",
            "Öğrenciler yayımlanan Aerospace listesinden en az iki ders almalıdır; sayfa açılan derslerin yıla göre değiştiğini açıkça belirtir.",
        ),
        "highly_recommended_aerospace_courses": [
            "ME 236U Control and Dynamics of Unmanned Aerial Vehicles",
            "ME 260A Advanced Fluid Mechanics",
            "ME 285A Continuum Mechanics",
            "ME 280A Introduction to the Finite Element Method",
            "ME 263 Turbulence",
            "ME 275 Advanced Dynamics",
            "ME 287 Introduction to Continuum Mechanics",
        ],
        "optional_aerospace_course_themes": [
            bi("Composite materials, elasticity, shells and nonlinear continua", "Kompozit malzemeler, elastisite, kabuklar ve doğrusal olmayan sürekli ortamlar"),
            bi("Vibrations and dynamics", "Titreşim ve dinamik"),
            bi("Combustion", "Yanma"),
            bi("Experiential control design", "Deneyimsel kontrol tasarımı"),
            bi("Advanced, geophysical and astrophysical fluid dynamics", "İleri, jeofiziksel ve astrofiziksel akışkanlar dinamiği"),
            bi("Finite-difference and spectral methods for fluid dynamics", "Akışkanlar dinamiği için sonlu fark ve spektral yöntemler"),
        ],
        "leadership_components_published": [
            "August leadership boot camp",
            "January leadership boot camp",
            "leadership electives",
            "ENGIN 295 communications",
            "ENGIN 270C teaming and project management",
            "ENGIN 270K coaching for high-performing teams",
        ],
        "capstone_units": 5,
        "capstone_terms": 2,
        "capstone_team_size_min": 3,
        "capstone_team_size_max": 5,
        "capstone_expected_hours_per_week_fall": 6,
        "capstone_expected_hours_per_week_spring": 9,
        "capstone_project_guaranteed_specific_partner": False,
        "capstone_industry_project_guaranteed": False,
        "comprehensive_exam_required": True,
        "comprehensive_exam_parts": ["leadership", "technical"],
        "usual_exam_attempts_per_part": 2,
        "thesis_required": False,
        "research_required": False,
        "internship_required": False,
        "mandatory_internship": False,
        "verification_notes": bi(
            "The official candidacy structure is 12 technical + 8 leadership + 5 capstone = 25 units. The programme's '12 units each semester' statement describes the full-time term load, not a conflicting 24-unit degree total. This is a professional Plan II MEng with a comprehensive exam and capstone, not a thesis MS.",
            "Resmî adaylık yapısı 12 teknik + 8 liderlik + 5 capstone = 25 birimdir. Programdaki 'her dönem 12 birim' ifadesi tam zamanlı dönem yükünü anlatır; çelişkili 24 birimlik derece toplamı değildir. Bu, kapsamlı sınav ve capstone içeren profesyonel Plan II MEng'dir; tezli MS değildir.",
        ),
    }

    row["cost_profile"] = {
        "academic_year": "2025/2026",
        "currency": "USD",
        "current_for_fall_2027": False,
        "fall_2027_cost_published": False,
        "tuition_and_program_fees_usd_nonresident": 63305.50,
        "ship_health_insurance_usd": 7848.00,
        "institutional_resilience_enhancement_fee_usd": 282.00,
        "total_tuition_and_required_fees_usd_nonresident": 71435.50,
        "official_personal_expenses_usd": 36774,
        "official_personal_expense_components_usd": {
            "housing_and_utilities": 19432,
            "food": 9576,
            "books_and_supplies": 752,
            "personal": 3246,
            "transportation": 3768,
        },
        "derived_same_year_total_budget_usd": 108209.50,
        "derived_same_year_total_formula": "71435.50 + 36774",
        "derived_total_is_official_single_line_item": False,
        "tuition_eur_per_year_min": None,
        "tuition_eur_per_year_max": None,
        "tuition_eur_per_year_estimated": None,
        "complete_program_cost_usd_fall_2027": None,
        "health_insurance_required": True,
        "health_insurance_automatic_enrollment": True,
        "health_insurance_waiver_possible": True,
        "part_time_2025_26_tuition_usd_per_unit": 2200,
        "scholarship_availability": "competitive_mixed_application",
        "scholarship_risk": "high",
        "cost_risk": "very_high",
        "verification_notes": bi(
            "The last published full-time table is explicitly 2025/26. It is retained as a historical planning benchmark and must not be presented as the Fall 2027 bill. The USD 108,209.50 figure is transparent arithmetic from same-year official totals, not a separate university-published total. Fall 2027 cost remains unknown until Berkeley updates the table.",
            "Yayımlanmış son tam zamanlı tablo açıkça 2025/26 dönemine aittir. Tarihsel planlama ölçütü olarak tutulur ve 2027 güz faturası gibi sunulamaz. 108.209,50 USD rakamı aynı yılın resmî toplamlarından şeffaf aritmetiktir; üniversitenin ayrı yayımladığı toplam değildir. Berkeley tabloyu güncelleyene kadar 2027 güz maliyeti bilinmiyor kalır.",
        ),
        "cost_notes": bi(
            "An international applicant should plan for a six-figure one-year budget and should not rely on the historical table or a competitive award as a guaranteed ceiling.",
            "Uluslararası aday altı haneli bir yıllık bütçe planlamalı; tarihsel tabloyu veya rekabetçi ödülü garanti üst sınır saymamalıdır.",
        ),
    }

    row["scholarship_profile"] = {
        "application_mode": "mixed",
        "funding_notes": bi(
            "Fung Excellence is automatic for full-time applicants; the international-eligible Opportunity Grant requires its section inside the admission application. Awards are competitive and not guaranteed.",
            "Fung Excellence tam zamanlı adaylar için otomatik değerlendirilir; uluslararası adaylara açık Opportunity Grant kabul başvurusu içindeki kendi bölümünün doldurulmasını ister. Ödüller rekabetçidir ve garanti değildir.",
        ),
        "separate_external_scholarship_application_required": False,
        "automatic_consideration": False,
        "automatic_consideration_for_some_awards": True,
        "admission_and_funding_decisions_separate": True,
        "funding_deadline": "2027-01-06T20:59:00-08:00",
        "funding_deadline_basis": "admission_application_and_grant_section",
        "opportunities": [
            {
                "name": "Fung Excellence Scholarship",
                "international_eligible": True,
                "automatic_consideration": True,
                "separate_form_required": False,
                "coverage": bi("Approximately 25–50% of full-time MEng tuition and fees; competitive and variable", "Tam zamanlı MEng öğrenim ve ücretlerinin yaklaşık %25–50'si; rekabetçi ve değişken"),
            },
            {
                "name": "MEng Opportunity Grant",
                "international_eligible": True,
                "automatic_consideration": False,
                "separate_form_required": False,
                "admission_application_grant_section_required": True,
                "need_based": True,
                "coverage": bi("Approximately 25–30% of full-time MEng tuition and fees; competitive and variable", "Tam zamanlı MEng öğrenim ve ücretlerinin yaklaşık %25–30'u; rekabetçi ve değişken"),
            },
            {
                "name": "Dean's Full Scholarship",
                "international_eligible": False,
                "eligibility_scope": "California tuition residents with a UC or CSU undergraduate degree",
                "automatic_consideration": True,
                "coverage": bi("Full two-semester tuition and fees for a subset of eligible candidates", "Uygun adayların bir alt kümesi için iki dönemin öğrenim ve ücretlerinin tamamı"),
            },
            {
                "name": "Dean's Grant",
                "international_eligible": False,
                "eligibility_scope": "California tuition residents with a UC or CSU undergraduate degree",
                "automatic_consideration": True,
                "coverage": bi("Approximately 25–50% for a subset of eligible candidates", "Uygun adayların bir alt kümesi için yaklaşık %25–50"),
            },
        ],
        "academic_employment_available": True,
        "academic_employment_guaranteed": False,
        "academic_employment_note": bi(
            "GSI, GSR, Reader and Tutor work can carry remission when eligibility and appointment thresholds are met, but no MEng appointment or remission is guaranteed. F-1 students may work on campus while fully enrolled under BIO rules.",
            "Uygunluk ve atama eşikleri sağlandığında GSI, GSR, Reader ve Tutor işleri ücret indirimi sağlayabilir; ancak MEng ataması veya indirimi garanti değildir. F-1 öğrencileri BIO kuralları altında tam kayıtlıyken kampüste çalışabilir.",
        ),
        "federal_loans_international_eligible": False,
        "private_loan_us_cosigner_usually_needed": True,
        "student_primary_financing_responsibility": True,
        "verification_notes": bi(
            "Funding is not simply 'automatic'. Fung Excellence is automatic for all full-time applications; Opportunity Grant requires completion of the grant section inside the admission application; Dean awards exclude ordinary international applicants. The programme says financing usually rests primarily with the student.",
            "Finansman basitçe 'otomatik' değildir. Fung Excellence tüm tam zamanlı başvurular için otomatiktir; Opportunity Grant kabul başvurusu içindeki grant bölümünün doldurulmasını ister; Dean ödülleri olağan uluslararası adayları dışlar. Program finansman sorumluluğunun genellikle esas olarak öğrencide olduğunu söyler.",
        ),
    }

    row["living_profile"] = {
        "city_type": "high_cost_bay_area",
        "city_cost_level": "very_high",
        "living_risk": "high",
        "housing_difficulty": "high",
        "housing_access": "first_come_first_served",
        "housing_guaranteed": False,
        "housing_application_separate": True,
        "housing_application_fee_usd": 45,
        "housing_application_opens": bi("Typically mid-February for the upcoming academic year", "Yaklaşan akademik yıl için genellikle Şubat ortası"),
        "housing_application_deadline": None,
        "housing_application_continuously_open": True,
        "housing_priority_rule": "earliest_applicants_first",
        "admission_offer_acceptance_required_before_housing_application": True,
        "calnet_required": True,
        "graduate_offer_response_days_typical": 7,
        "rolling_offers_start_month": "February",
        "full_occupancy_common_after_august": True,
        "contract_move_in": "2026-08-15",
        "contract_move_out": "2027-07-31",
        "rates_academic_year": "2026/2027",
        "graduate_housing_rate_usd_per_person_month_min": 1530,
        "graduate_housing_rate_usd_per_person_month_max": 2495,
        "graduate_housing_one_time_student_experience_fee_usd": 25,
        "meal_plan_included": False,
        "official_rent_items": [
            {"item": bi("Intersection furnished four-bedroom, shared baths, per person", "Intersection mobilyalı dört yatak odalı, ortak banyolar, kişi başına"), "amount_usd_min": 1530, "amount_usd_max": 1530, "period": "month", "academic_year": "2026/2027"},
            {"item": bi("Jackson House furnished six-bedroom share, per person", "Jackson House mobilyalı altı yatak odalı paylaşım, kişi başına"), "amount_usd_min": 1570, "amount_usd_max": 1570, "period": "month", "academic_year": "2026/2027"},
            {"item": bi("Manville unfurnished studio, per person", "Manville mobilyasız stüdyo, kişi başına"), "amount_usd_min": 1715, "amount_usd_max": 1760, "period": "month", "academic_year": "2026/2027"},
            {"item": bi("Intersection furnished studio/one-bedroom range, per person", "Intersection mobilyalı stüdyo/tek yatak odalı aralığı, kişi başına"), "amount_usd_min": 1670, "amount_usd_max": 2465, "period": "month", "academic_year": "2026/2027"},
            {"item": bi("xučyun ruwway furnished shared room to one-bedroom range, per person", "xučyun ruwway mobilyalı paylaşımlı oda ile tek yatak odalı aralığı, kişi başına"), "amount_usd_min": 1531, "amount_usd_max": 2495, "period": "month", "academic_year": "2026/2027"},
        ],
        "official_2025_26_housing_and_utilities_budget_usd": 19432,
        "verification_notes": bi(
            "Graduate housing has no deadline because applications stay open, but early applications have priority and no offer is guaranteed. Rates are per person per month and do not include a meal plan; the 2026/27 range is not a citywide rent estimate.",
            "Lisansüstü konut başvurusu sürekli açık olduğundan son tarih yoktur; ancak erken başvuru önceliklidir ve teklif garanti değildir. Ücretler kişi başı aylıktır ve yemek planını içermez; 2026/27 aralığı şehir geneli kira tahmini değildir.",
        ),
    }

    row["application_timeline_profile"] = {
        "intake": "Fall 2027",
        "spring_intake_available": False,
        "application_opens": bi("September (annual programme FAQ; exact 2026 date not published)", "Eylül (yıllık program SSS'si; 2026 kesin tarihi yayımlanmadı)"),
        "application_deadline": "2027-01-06T20:59:00-08:00",
        "deadline_non_eu": "2027-01-06T20:59:00-08:00",
        "supplemental_material_deadline": "2027-01-06T20:59:00-08:00",
        "scholarship_deadline": "2027-01-06T20:59:00-08:00",
        "english_score_deadline_if_required": "2026-12-01T20:59:00-08:00",
        "recommendation_deadline": "2027-01-06T20:59:00-08:00",
        "late_applications_accepted": False,
        "rolling_admission": False,
        "decision_timing": bi("Most admitted students are notified by early April", "Kabul edilen öğrencilerin çoğu Nisan başına kadar bilgilendirilir"),
        "offer_reply_deadline": None,
        "deferral_available": "programme_recommendation_case_by_case_not_applicant_entitlement",
        "deferral_request_deadline_if_supported": "2027-06-01",
        "pre_enrollment_required": False,
        "visa_document_path": bi("Accept offer → wait up to two weeks for CalCentral NIF task → submit passport and sufficient proof of funding → BIO issues I-20/DS-2019", "Teklifi kabul et → CalCentral NIF görevi için iki haftaya kadar bekle → pasaport ve yeterli mali kanıtı gönder → BIO I-20/DS-2019 düzenler"),
        "nif_task_appearance_after_acceptance_days_max": 14,
        "i20_ds2019_processing_complete_nif_weeks_min": 2,
        "i20_ds2019_processing_complete_nif_weeks_max": 3,
        "fall_2026_onward_nif_processing_fee_usd": 0,
        "financial_proof_required": True,
        "financial_proof_amount_usd": None,
        "visa_notes": bi(
            "BIO processes complete NIFs first-come, first-served in roughly two to three weeks during high season. The checked page requires sufficient funding evidence but does not publish a Fall 2027 MEng amount, so that amount remains null.",
            "BIO tam NIF başvurularını yoğun dönemde ilk gelen ilk işlenir biçiminde yaklaşık iki ila üç haftada işler. Kontrol edilen sayfa yeterli mali kanıt ister ancak 2027 güz MEng tutarını yayımlamaz; bu tutar null kalır.",
        ),
        "timeline_risk": "high",
        "verification_notes": bi(
            "The English-score deadline is more than a month earlier than the MEng application deadline. Applicants needing a test must plan to the December 1 deadline, not January 6.",
            "İngilizce puanı son tarihi MEng başvuru son tarihinden bir aydan fazla erkendir. Sınav gereken adaylar 6 Ocak'a değil 1 Aralık'a göre plan yapmalıdır.",
        ),
    }

    row["research_profile"] = {
        "degree_is_research_masters": False,
        "research_required": False,
        "individual_lab_place_guaranteed": False,
        "research_access_note": bi(
            "The professional MEng has a two-semester applied capstone, not a thesis. Relevant ME research exists in controls, UAV autonomy, fluids/aerodynamics, mechanics, composites and combustion, but admission to this MEng does not guarantee a lab position or research assistantship.",
            "Profesyonel MEng'de tez yerine iki dönemlik uygulamalı capstone vardır. Kontrol, İHA otonomisi, akışkanlar/aerodinamik, mekanik, kompozit ve yanma alanlarında ilgili ME araştırması bulunur; ancak bu MEng'e kabul laboratuvar yeri veya araştırma asistanlığı garantilemez.",
        ),
        "research_focus_areas": [
            bi("UAV dynamics, motion planning, state estimation and control", "İHA dinamiği, hareket planlama, durum kestirimi ve kontrol"),
            bi("Aircraft wake vortices, aerodynamics and turbulence", "Uçak iz girdapları, aerodinamik ve türbülans"),
            bi("Linear/nonlinear dynamics and vibrations", "Doğrusal/doğrusal olmayan dinamik ve titreşim"),
            bi("Composite and lightweight aerospace materials", "Kompozit ve hafif havacılık-uzay malzemeleri"),
            bi("Combustion and reacting-flow modelling", "Yanma ve tepkimeli akış modelleme"),
        ],
        "key_institutes": [
            "High Performance Robotics Laboratory",
            "Autonomy, Robotics, and Controls Lab",
            "Model Predictive Control Lab",
            "Fluid Mechanics Laboratory",
            "Dynamics Lab",
            "Computational Solid Mechanics Laboratory",
            "Combustion Laboratory",
        ],
        "berkeley_air_space_center_clusters": ["Advanced Aviation", "Robotics & Autonomy", "Materials in Extreme Environments"],
        "air_space_center_stage": bi(
            "Joint clusters are active, but the centre FAQ says construction was expected to begin in 2026 with occupancy potentially as early as 2029.",
            "Ortak kümeler aktiftir; ancak merkez SSS'si inşaatın 2026'da başlamasının ve kullanımın en erken 2029'da olmasının beklendiğini söyler.",
        ),
        "air_space_center_student_access_guaranteed": False,
        "research_risk": "medium_professional_degree",
    }

    row["industry_ecosystem_profile"] = {
        "local_industry_strength": "very_high",
        "confirmed_partners": [
            {
                "name": "NASA",
                "scope": bi("Current MEng-wide 2026 capstone partnership example", "Güncel MEng geneli 2026 capstone işbirliği örneği"),
                "individual_student_access_guaranteed": False,
            },
            {
                "name": "NASA Ames Research Center",
                "scope": bi("UC Berkeley Space Act/air-and-space research collaboration and joint research clusters", "UC Berkeley Space Act/hava-uzay araştırma işbirliği ve ortak araştırma kümeleri"),
                "individual_student_access_guaranteed": False,
            },
        ],
        "capstone_partner_project_guaranteed": False,
        "historical_me_meng_aerospace_employers_not_partners": ["Lockheed Martin", "BAE Systems", "Space Systems/Loral"],
        "career_support": bi(
            "Dedicated MEng career advising, workshops, individual coaching, employer events, job fairs and alumni networking are published; the latest public employment dashboard covers the Class of 2025 but does not expose programme-specific figures in the accessible page text.",
            "Özel MEng kariyer danışmanlığı, atölyeler, bireysel koçluk, işveren etkinlikleri, kariyer fuarları ve mezun ağı yayımlanır; en güncel kamuya açık istihdam paneli 2025 sınıfını kapsar ancak erişilebilir sayfa metninde programa özgü rakam vermez.",
        ),
        "stem_degree": True,
        "opt_eligible": True,
        "stem_opt_extension_eligible": True,
        "export_control_risk": "project_specific",
        "international_access_note": bi(
            "Berkeley states that international students may generally join fundamental research without a licence, but ITAR equipment, restricted technical data, NDAs and controlled projects can restrict access. This is project-specific, not a blanket ban or guarantee.",
            "Berkeley, uluslararası öğrencilerin genel olarak lisans olmadan temel araştırmaya katılabileceğini; ancak ITAR ekipmanı, kısıtlı teknik veri, NDA ve kontrollü projelerin erişimi sınırlayabileceğini belirtir. Bu proje özeldir; genel yasak veya garanti değildir.",
        ),
        "verification_notes": bi(
            "Only documented MEng/NASA and UC Berkeley–NASA Ames relationships are listed as partnerships. Prior aerospace employers are retained as outcome context and are explicitly not relabelled as programme partners.",
            "Yalnızca belgeli MEng/NASA ve UC Berkeley–NASA Ames ilişkileri işbirliği olarak listelenir. Önceki havacılık-uzay işverenleri sonuç bağlamı olarak tutulur ve program ortağı diye yeniden etiketlenmez.",
        ),
    }

    row["student_sentiment_profile"] = {
        "student_satisfaction_score": None,
        "workload_sentiment": "intense",
        "teaching_quality_sentiment": "insufficient_evidence",
        "administration_sentiment": "insufficient_evidence",
        "housing_sentiment": "insufficient_program_specific_evidence",
        "city_life_sentiment": "insufficient_evidence",
        "international_student_sentiment": "mixed_limited",
        "career_support_sentiment": "mixed_positive_limited",
        "student_sentiment_summary": bi(
            "A very small self-selected sample repeatedly describes the nine-month format and capstone as intensive. One 2026 international alumnus says even a non-industry capstone supported interviews and employment, while warning that industry projects can be more demanding; another ME-adjacent discussion values the framework but flags tuition and the compressed job search. This is perception evidence only.",
            "Çok küçük ve öz-seçimli örneklem dokuz aylık formatı ve capstone'u tekrar tekrar yoğun olarak tanımlar. 2026'da bir uluslararası mezun, endüstri dışı capstone'un bile mülakat ve işe yerleşmeyi desteklediğini; endüstri projelerinin daha yorucu olabileceğini söyler. ME'ye yakın başka bir tartışma yapıyı değerli bulurken öğrenim maliyeti ve sıkışık iş aramayı vurgular. Bu yalnızca algı kanıtıdır.",
        ),
        "student_sentiment_sources": [
            {"url": REDDIT_ME, "source_type": "student_forum", "access_status": "ok", "last_checked": TODAY, "date_range": "2024-07 to 2025-08"},
            {"url": REDDIT_CAPSTONE, "source_type": "student_forum", "access_status": "ok", "last_checked": TODAY, "date_range": "2026-08"},
            {"url": REDDIT_EXPERIENCE, "source_type": "student_forum", "access_status": "ok", "last_checked": TODAY, "date_range": "2026-03"},
        ],
        "approximate_sample_size": 3,
        "date_range": "2024-07 to 2026-08",
        "sentiment_confidence": "low",
        "verification_notes": bi(
            "No 0–100 satisfaction score is produced because the sample is small, self-selected and not specific enough across all requested dimensions.",
            "Örneklem küçük, öz-seçimli ve istenen tüm boyutlarda yeterince programa özgü olmadığından 0–100 memnuniyet puanı üretilmez.",
        ),
    }

    row["category_profile"] = {
        "primary_categories": ["aerospace_engineering", "professional_engineering_leadership"],
        "secondary_categories": ["controls", "autonomous_systems", "fluid_mechanics", "aerodynamics", "structures", "materials", "combustion", "dynamics", "capstone"],
        "technical_focus": bi(
            "Aerospace systems through ME depth in UAV control, fluids, structures, materials, dynamics and combustion, combined with leadership and capstone.",
            "Liderlik ve capstone ile birleşen İHA kontrolü, akışkanlar, yapılar, malzemeler, dinamik ve yanma alanlarında ME derinliği üzerinden havacılık-uzay sistemleri.",
        ),
        "fit_warning": bi(
            "A strong professional aerospace concentration, but not a dedicated research MSc in aerospace or space engineering.",
            "Güçlü bir profesyonel havacılık-uzay concentration'ıdır; ancak havacılık veya uzay mühendisliğinde özel araştırma MSc'si değildir.",
        ),
    }

    sources = [
        source(PROGRAM, "UC Berkeley ME — Master of Engineering", "official_program_page", ["program", "duration", "admission", "curriculum", "career"], "Active professional MEng, full-time and part-time formats, concentration list and career context.", "Etkin profesyonel MEng, tam/yarı zamanlı biçimler, concentration listesi ve kariyer bağlamı."),
        source(ME_ADMISSIONS, "UC Berkeley ME — Graduate Admissions", "official_admission_page", ["program", "admission", "deadline", "program_status", "gre"], "Fall 2027 routes, deadline, minimum preparation and no terminal MS warning.", "2027 güz yolları, son tarih, asgari hazırlık ve terminal MS sunulmaması uyarısı."),
        source(MENG_APPLICATION, "UC Berkeley ME — MEng Application", "official_admission_page", ["admission", "non_eu", "language", "deadline", "documents", "gre"], "Current Fall 2027 MEng application, two letters, essays, transcript rules and test deadlines.", "Güncel 2027 güz MEng başvurusu, iki referans, yazılar, transkript kuralları ve sınav son tarihleri."),
        source(CENTRAL_REQUIREMENTS, "Berkeley Graduate Division — Admissions Requirements", "official_admission_page", ["admission", "language", "non_eu"], "Current English-test rules, exact scale transition, accepted tests and exemptions.", "Güncel İngilizce sınav kuralları, kesin ölçek geçişi, kabul edilen sınavlar ve muafiyetler."),
        source(CENTRAL_FAQ, "Berkeley Graduate Division — Admissions FAQ", "official_admission_page", ["admission", "application_fee", "fee_waiver", "application_limit"], "Current USD 155 non-US fee, three-day payment rule, waiver scope and one-program-per-cycle rule.", "Güncel ABD dışı 155 USD ücret, üç günlük ödeme kuralı, muafiyet kapsamı ve dönem başına tek program kuralı."),
        source(CONCENTRATIONS, "UC Berkeley ME — MEng Concentrations", "official_curriculum_page", ["curriculum", "program"], "Active Aerospace concentration, at-least-two-course rule and current course menu.", "Etkin Aerospace concentration, en az iki ders kuralı ve güncel ders menüsü."),
        source(DEGREE_REQUIREMENTS, "UC Berkeley ME — MEng Degree Requirements", "official_curriculum_page", ["curriculum", "units", "comprehensive_exam"], "Technical, leadership, capstone and mandatory comprehensive-exam requirements.", "Teknik, liderlik, capstone ve zorunlu kapsamlı sınav şartları."),
        source(CANDIDACY_FORM, "UC Berkeley ME — MEng Candidacy Form", "official_curriculum_page", ["curriculum", "units"], "Official 12+8+5 unit candidacy structure.", "Resmî 12+8+5 birim adaylık yapısı.", access_status="pdf"),
        source(NEW_ADMIT_COST, "Fung Institute — New Admit Resources and Cost Table", "official_tuition_page", ["tuition", "fees", "living", "insurance", "visa"], "Last published full-time nonresident table and personal-expense components; page flags later-year rates as not final/published.", "Yayımlanmış son tam zamanlı eyalet dışı tablo ve kişisel gider bileşenleri; sayfa sonraki yıl oranlarının kesin/yayımlanmış olmadığını belirtir.", confidence="medium"),
        source(TUITION_FUNDING, "Fung Institute — MEng Tuition and Financial Aid", "official_scholarship_page", ["scholarship", "funding", "insurance", "living_cost"], "Automatic and application-section funding routes, eligibility scope, coverage ranges and student-responsibility warning.", "Otomatik ve başvuru-bölümü finansman yolları, uygunluk kapsamı, karşılama aralıkları ve öğrenci sorumluluğu uyarısı."),
        source(MENG_FAQ, "Fung Institute — MEng FAQ", "official_program_page", ["program", "admission", "decision", "international", "career", "opt"], "Programme timing, international cohort evidence, decision timing, STEM/OPT and career support.", "Program takvimi, uluslararası kohort kanıtı, karar zamanı, STEM/OPT ve kariyer desteği."),
        source(CAPSTONE, "Fung Institute — MEng Capstone Experience", "official_industry_partner_page", ["curriculum", "partnership", "industry"], "Two-semester project model and current 2026 NASA capstone example; no individual placement guarantee.", "İki dönemlik proje modeli ve güncel 2026 NASA capstone örneği; bireysel yer garantisi yok."),
        source(CAPSTONE_FORMAT, "Fung Institute — Capstone Project Format", "official_curriculum_page", ["curriculum", "capstone", "industry"], "Five-unit project format, partner types and deliverables.", "Beş birimlik proje biçimi, ortak türleri ve çıktılar."),
        source(CAREER, "Fung Institute — MEng Career Programming", "official_department_page", ["career", "industry_ecosystem"], "Dedicated career coaching, employer programming and recruiting calendar.", "Özel kariyer koçluğu, işveren programları ve işe alım takvimi."),
        source(EMPLOYMENT, "Fung Institute — MEng Employment Data", "official_department_page", ["career", "outcomes"], "Latest public dashboard scope is Class of 2025; accessible text does not expose ME Aerospace-specific figures.", "En güncel kamu paneli 2025 sınıfını kapsar; erişilebilir metin ME Aerospace'e özgü rakam yayımlamaz.", confidence="medium"),
        source(HOUSING_APPLY, "UC Berkeley Housing — Apply", "official_housing_page", ["housing", "housing_application", "fee"], "Separate application, CalNet/admission prerequisites, USD 45 fee and seven-day graduate offer response.", "Ayrı başvuru, CalNet/kabul önkoşulları, 45 USD ücret ve lisansüstü teklifine yedi günlük yanıt."),
        source(HOUSING_GRAD, "UC Berkeley Housing — How to Apply for Graduate Housing", "official_housing_page", ["housing", "housing_application", "deadline"], "Mid-February typical opening, continuously open process and earliest-applicant priority.", "Şubat ortası olağan açılış, sürekli açık süreç ve en erken başvurana öncelik."),
        source(HOUSING_DATES, "UC Berkeley Housing — Dates and Deadlines", "official_housing_page", ["housing", "deadline", "contract"], "Continuous graduate applications, rolling offers and 2026/27 move dates.", "Sürekli lisansüstü başvuruları, dönemsel teklifler ve 2026/27 taşınma tarihleri."),
        source(HOUSING_ASSIGNMENT, "UC Berkeley Housing — Graduate Assignment and Offers", "official_housing_page", ["housing", "housing_guarantee", "availability"], "Explicit no-guarantee rule, wait list, priority and occupancy warning.", "Açık garanti-yok kuralı, bekleme listesi, öncelik ve doluluk uyarısı."),
        source(HOUSING_RATES, "UC Berkeley Housing — 2026/27 Graduate Rates", "official_housing_page", ["housing", "housing_rates"], "Per-person monthly graduate housing range and one-time fee.", "Kişi başı aylık lisansüstü konut aralığı ve tek seferlik ücret."),
        source(NIF, "Berkeley International Office — Nonimmigrant Information Form", "official_visa_or_government_page", ["non_eu", "visa", "financial_proof", "processing_time"], "Post-acceptance NIF path, proof-of-funding requirement and two-to-three-week high-season processing.", "Kabul sonrası NIF yolu, mali kanıt şartı ve yoğun dönemde iki-üç haftalık işlem."),
        source(F1_WORK, "Berkeley International Office — On-Campus Employment", "official_visa_or_government_page", ["employment", "international"], "F-1 on-campus work eligibility while fully enrolled; not a job guarantee.", "Tam kayıtlı F-1 öğrencisinin kampüste çalışma uygunluğu; iş garantisi değildir."),
        source(EXPORT, "UC Berkeley Research Compliance — International Students and Export Control", "official_university_policy_page", ["export_control", "international_research_access"], "Fundamental-research access and project-specific ITAR/restricted-data exceptions.", "Temel araştırma erişimi ve projeye özgü ITAR/kısıtlı veri istisnaları."),
        source(CONTROLS, "UC Berkeley ME — Controls Research", "official_department_page", ["research", "labs"], "Current controls themes and named laboratories relevant to UAV/autonomy work.", "İHA/otonomi çalışmasına ilgili güncel kontrol temaları ve adlandırılmış laboratuvarlar."),
        source(FLUID_LAB, "UC Berkeley ME — Fluid Mechanics Laboratory", "official_lab_page", ["research", "labs"], "Aircraft wakes, aerodynamics, vortices and turbulence.", "Uçak izleri, aerodinamik, girdaplar ve türbülans."),
        source(MECHANICS, "UC Berkeley ME — Mechanics", "official_department_page", ["research", "labs"], "Continuum mechanics, dynamics, composites and computational solids.", "Sürekli ortam mekaniği, dinamik, kompozitler ve hesaplamalı katılar."),
        source(MATERIALS, "UC Berkeley ME — Materials", "official_department_page", ["research", "labs"], "Lightweight composite and spacecraft-material relevance.", "Hafif kompozit ve uzay aracı malzemesi ilgisi."),
        source(ENERGY, "UC Berkeley ME — Energy Science and Technology", "official_department_page", ["research", "labs"], "Combustion, reacting flows and microgravity fire research context.", "Yanma, tepkimeli akışlar ve mikro yerçekimi yangın araştırması bağlamı."),
        source(AIRSPACE, "Berkeley Air & Space Center — Research Clusters", "official_industry_partner_page", ["partnership", "industry", "research"], "Active UC Berkeley–NASA clusters in aviation, autonomy and extreme-environment materials.", "Havacılık, otonomi ve aşırı ortam malzemelerinde aktif UC Berkeley–NASA kümeleri."),
        source(AIRSPACE_FAQ, "Berkeley Air & Space Center — FAQ", "official_industry_partner_page", ["partnership", "industry", "timeline"], "Space Act relationship and construction/occupancy stage; prevents portraying a future facility as current guaranteed access.", "Space Act ilişkisi ve inşaat/kullanım aşaması; gelecekteki tesisi güncel garantili erişim gibi sunmayı önler."),
        source(QS, "QS — University of California, Berkeley", "official_ranking_page", ["prestige"], "QS World University Rankings 2027 institutional rank =20; context only.", "QS Dünya Üniversite Sıralaması 2027 kurum sırası =20; yalnızca bağlam.", confidence="medium"),
        source(REDDIT_ME, "Reddit — Thoughts on MEng Mechanical Engineering", "student_forum", ["student_sentiment"], "Small discussion on technical electives, capstone, compressed schedule, cost and job search.", "Teknik seçmeliler, capstone, sıkışık takvim, maliyet ve iş arama üzerine küçük tartışma.", confidence="low"),
        source(REDDIT_CAPSTONE, "Reddit — Advice on MEng Capstone Choice", "student_forum", ["student_sentiment"], "Recent international-student/alumnus perceptions of industry versus academic capstones.", "Endüstri ve akademik capstone üzerine yakın tarihli uluslararası öğrenci/mezun algıları.", confidence="low"),
        source(REDDIT_EXPERIENCE, "Reddit — UC Berkeley MEng Student Experience", "student_forum", ["student_sentiment"], "Small 2026 discussion of nine-month intensity and general ME experience.", "Dokuz aylık yoğunluk ve genel ME deneyimi üzerine küçük 2026 tartışması.", confidence="low"),
    ]

    official_count = sum(1 for item in sources if item["source_type"].startswith("official_"))
    forum_count = sum(1 for item in sources if item["source_type"] == "student_forum")
    critical_count = sum(
        1 for item in sources
        if item["source_type"] in {
            "official_program_page", "official_admission_page", "official_curriculum_page",
            "official_tuition_page", "official_scholarship_page", "official_department_page",
            "official_lab_page", "official_housing_page", "official_visa_or_government_page",
            "official_industry_partner_page", "official_university_policy_page",
        }
    )

    row["source_profile"] = {
        "primary_url": PROGRAM,
        "official_program_page": PROGRAM,
        "official_admission_page": MENG_APPLICATION,
        "official_tuition_page": NEW_ADMIT_COST,
        "official_scholarship_page": TUITION_FUNDING,
        "last_verified": TODAY,
        "source_log": sources,
        "source_count": len(sources),
        "checked_official_source_count": official_count,
        "critical_institutional_source_count": critical_count,
        "student_forum_source_count": forum_count,
        "field_confidence": {
            "program_basic_info": "high",
            "program_status": "high",
            "admission": "high",
            "non_eu_eligibility": "high",
            "english_proficiency": "high",
            "teaching_language": "unknown",
            "gre": "high",
            "deadlines": "high",
            "curriculum": "high",
            "tuition_historical_2025_26": "high",
            "tuition_fall_2027": "unknown",
            "scholarship": "high",
            "housing": "high",
            "visa": "high",
            "research": "high",
            "industry": "high",
            "sentiment": "low",
            "prestige": "medium",
        },
        "source_reliability": "high",
        "verification_status": "partially_verified",
        "needs_verification": True,
        "verification_notes": bi(
            "The critical unresolved fields are the explicitly labelled teaching language and the Fall 2027 price/financial-proof amount. Historical costs are date-scoped; no partner, lab, funding or housing access is converted into a guarantee.",
            "Kritik çözülmemiş alanlar açıkça etiketlenmiş öğretim dili ile 2027 güz fiyatı/mali kanıt tutarıdır. Tarihsel maliyetler tarihle sınırlandırılır; hiçbir ortak, laboratuvar, finansman veya konut erişimi garantiye çevrilmez.",
        ),
    }

    row["decision_summary"] = {
        "main_strengths": [
            bi("A current professional Aerospace concentration with an explicit technical-course rule and 25-unit degree structure.", "Açık teknik ders kuralı ve 25 birimlik derece yapısına sahip güncel profesyonel Aerospace concentration."),
            bi("Deep Berkeley ME options in UAV control, fluids, structures, composites, dynamics and combustion.", "İHA kontrolü, akışkanlar, yapılar, kompozitler, dinamik ve yanmada derin Berkeley ME seçenekleri."),
            bi("A two-semester capstone, dedicated career services and documented NASA/NASA Ames collaboration context.", "İki dönemlik capstone, özel kariyer hizmetleri ve belgeli NASA/NASA Ames işbirliği bağlamı."),
        ],
        "main_risks": [
            bi("The last published international planning benchmark is USD 108,209.50 for 2025/26; Fall 2027 cost is not yet published and funding is competitive.", "Uluslararası son planlama ölçütü 2025/26 için 108.209,50 USD'dir; 2027 güz maliyeti henüz yayımlanmamıştır ve finansman rekabetçidir."),
            bi("The nine-month professional degree has no thesis or research requirement and does not guarantee a lab, NASA project or aerospace employer.", "Dokuz aylık profesyonel derecede tez veya araştırma şartı yoktur; laboratuvar, NASA projesi veya havacılık-uzay işvereni garantilemez."),
            bi("Graduate housing is expensive, rolling, wait-list based and not guaranteed.", "Lisansüstü konut pahalı, sürekli değerlendirmeli, bekleme listeli ve garantisizdir."),
            bi("The English evidence deadline is December 1, earlier than the January 6 application deadline; teaching language itself remains officially unlabelled.", "İngilizce kanıtı son tarihi 1 Aralık olup 6 Ocak başvuru son tarihinden erkendir; öğretim dilinin kendisi resmen etiketlenmemiştir."),
            bi("Project-specific export controls can restrict some international-student access even though fundamental research is generally open.", "Temel araştırma genel olarak açık olsa da projeye özgü ihracat kontrolleri bazı uluslararası öğrenci erişimini sınırlayabilir."),
        ],
        "best_for": bi(
            "Applicants targeting a rapid industry-facing aerospace/controls/fluids/structures credential who value leadership and capstone work and can sustain the programme without assuming an award.",
            "Liderlik ve capstone'u önemseyen, hızlı ve endüstri yönelimli havacılık-uzay/kontrol/akışkanlar/yapılar derecesi isteyen ve burs varsaymadan programı finanse edebilen adaylar.",
        ),
        "not_ideal_for": bi(
            "Applicants needing a funded thesis MSc, guaranteed research placement, a low-cost city, guaranteed housing, or a two-year timeline for internships and US job search.",
            "Finansmanlı tezli MSc, garantili araştırma yeri, düşük maliyetli şehir, garantili konut veya staj ve ABD iş araması için iki yıllık süre isteyen adaylar.",
        ),
        "verdict": bi(
            "Excellent professional aerospace fit, but financially and temporally high-risk. Treat it as a nine-month Berkeley ME leadership-and-capstone degree—not as a funded research MS—and wait for the Fall 2027 cost table before fixing the budget.",
            "Profesyonel havacılık-uzay uyumu mükemmel, ancak mali ve zamanlama riski yüksektir. Bunu finansmanlı araştırma MS'i değil, dokuz aylık Berkeley ME liderlik ve capstone derecesi olarak değerlendirin; bütçeyi sabitlemeden önce 2027 güz maliyet tablosunu bekleyin.",
        ),
    }

    row["scoring_inputs"] = {
        "academic_prestige": None,
        "technical_fit": None,
        "research_output": None,
        "industry_links": None,
        "affordability": None,
        "admission_chance": None,
        "living_quality": None,
        "student_satisfaction": None,
        "verification_notes": bi(
            "No programme score is manually fabricated; the application computes presentation scores only from source-backed normalized fields.",
            "Programa elle puan uydurulmaz; uygulama sunum puanlarını yalnızca kaynaklı normalleştirilmiş alanlardan hesaplar.",
        ),
    }

    row["data_quality"] = {
        "status": "partial",
        "checked_official_source_count": official_count,
        "verified_fields": [
            "program", "admission", "non_eu_eligibility", "tuition", "scholarship",
            "deadline", "curriculum", "research", "industry", "housing",
        ],
        "verification_scope_notes": [
            "tuition evidence is the historical 2025/26 benchmark, not a Fall 2027 bill",
            "English-proficiency requirements are verified but teaching language is not",
            "visa workflow is verified but the Fall 2027 proof-of-funding amount is not",
        ],
        "unverified_critical_fields": ["language"],
        "has_checked_source_log": True,
        "audited_at": TODAY,
    }

    row["quality_control"] = {
        "checked_at": TODAY,
        "qc_status": "needs_revision",
        "remaining_verification_tasks": [
            bi("Obtain an explicit official teaching-language label.", "Açık bir resmî öğretim-dili etiketi edinin."),
            bi("Recheck the Fung cost table when Fall 2027 rates are published.", "2027 güz oranları yayımlandığında Fung maliyet tablosunu yeniden kontrol edin."),
            bi("Record the programme-specific Fall 2027 proof-of-funding amount when BIO publishes it.", "BIO yayımladığında programa özgü 2027 güz mali kanıt tutarını kaydedin."),
        ],
        "qc_notes": bi(
            "The record is decision-useful but intentionally partial. Historical cost, uncertain language label and future-facility access are visibly scoped.",
            "Kayıt karar için yararlıdır ancak bilinçli olarak kısmidir. Tarihsel maliyet, belirsiz öğretim-dili etiketi ve gelecekteki tesis erişimi görünür biçimde sınırlandırılmıştır.",
        ),
        "failed_canary_tests": ["explicit_teaching_language_not_found", "fall_2027_cost_not_published"],
    }

    row["last_verified"] = TODAY

    DATA_PATH.write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    audit = {
        "record_id": row["id"],
        "checked_at": TODAY,
        "source_count": len(sources),
        "checked_official_source_count": official_count,
        "critical_institutional_source_count": critical_count,
        "student_forum_source_count": forum_count,
        "broken_or_unknown_count": sum(1 for item in sources if item["access_status"] in {"broken", "not_found", "unknown"}),
        "sources": sources,
        "notes": bi(
            "All URLs were opened or returned accessible indexed content on 2026-08-14. No broken/not-found/unknown source is used. Future publication gaps remain null.",
            "Tüm URL'ler 2026-08-14 tarihinde açıldı veya erişilebilir indekslenmiş içerik döndürdü. Broken/not-found/unknown kaynak kullanılmaz. Gelecek yayın boşlukları null kalır.",
        ),
    }
    AUDIT_PATH.parent.mkdir(parents=True, exist_ok=True)
    AUDIT_PATH.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        f"Updated {row['id']} with {len(sources)} sources "
        f"({official_count} official, {forum_count} forum)."
    )


if __name__ == "__main__":
    main()
