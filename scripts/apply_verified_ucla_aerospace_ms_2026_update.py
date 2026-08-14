from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data_base" / "amerika.json"
AUDIT_PATH = ROOT / "reports" / "source_link_audit_ucla_aerospace_ms_2026-08-14.json"
TODAY = "2026-08-14"

PROGRAM = "https://grad.ucla.edu/programs/school-of-engineering-and-applied-science/mechanical-aerospace-engineering-department/aerospace-engineering/"
ADMISSION_2026 = "https://grad.ucla.edu/gasaa/deptinfo/deptinfo.asp?academicyear=20262027&code=0279"
MAE_ADMISSION = "https://www.mae.ucla.edu/graduate-admissions-2/"
GENERAL_APPLY = "https://grad.ucla.edu/admissions/research-requirements/"
INTERNATIONAL = "https://grad.ucla.edu/admissions/international-applicants/"
ENGLISH = "https://grad.ucla.edu/admissions/english-requirements/"
CURRICULUM_INDEX = "https://grad.ucla.edu/page/13/?gd_program_reqs_year=2025-2026"
MS_CHECKLIST = "https://www.mae.ucla.edu/ms-graduation-checklist/"
MS_PROGRAM_PDF = "https://www.mae.ucla.edu/wp-content/uploads/mae/program-of-study-for-the-ms-degree-v4.pdf"
CAPSTONE_EXAMS = "https://www.mae.ucla.edu/take-and-pass-three-extra-written-exams-at-the-end-of-a-mae-graduate-course/"
FEES = "https://sa.ucla.edu/RO/Fees/Public/public-fees?degree=Academic+Master&term=Annual&year=2025-2026"
COA = "https://financialaid.ucla.edu/graduate-aid/cost-of-attendance"
CATALOG_FEES = "https://catalog.registrar.ucla.edu/Graduate-Study/Registration/Fees-and-Payment"
FINANCIAL_SUPPORT = "https://catalog.registrar.ucla.edu/Graduate-Study/Financial-Support"
HOUSING_APPLICATION = "https://housing.ucla.edu/content/housing-application-process-single-graduate-students-and-students-families"
HOUSING_RATES = "https://housing.ucla.edu/2026-2027-single-graduate-housing-contract-rates"
LABS = "https://www.mae.ucla.edu/laboratories/"
AIR_SPACE = "https://www.mae.ucla.edu/air-space/"
RESEARCH_AREAS = "https://www.mae.ucla.edu/graduate-programs-and-preliminary-exams/"
QS = "https://www.topuniversities.com/universities/university-california-los-angeles-ucla"

REDDIT_1 = "https://www.reddit.com/r/ucla/comments/1rbp69l/likelihood_of_getting_ucla_grad_housing/"
REDDIT_2 = "https://www.reddit.com/r/ucla/comments/1sybwwg/grad_housing/"
REDDIT_3 = "https://www.reddit.com/r/ucla/comments/1upai2i/whats_a_good_waitlist_for_ucla_graduate_housing/"


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
    row = next(item for item in rows if item.get("id") == "ucla-mae")

    row.update(
        {
            "country": "United States",
            "university": "University of California, Los Angeles",
            "university_native_name": "University of California, Los Angeles (UCLA)",
            "city": "Los Angeles",
            "region": "California",
            "program_name": "Master of Science in Aerospace Engineering",
            "program_native_name": "Master of Science in Aerospace Engineering",
            "program_degree": "MS",
            "degree_level": "Master",
            "major_code": "0279",
            "duration_years": None,
            "duration": bi(
                "The current degree requirements report an average of five quarters and a maximum of nine quarters; the department FAQ separately says the MS is typically completed in four quarters.",
                "Güncel derece şartları ortalama beş çeyrek ve en fazla dokuz çeyrek bildirir; bölüm SSS'si ayrıca MS'in tipik olarak dört çeyrekte tamamlandığını söyler.",
            ),
            "duration_quarters_average": 5,
            "duration_quarters_department_typical": 4,
            "duration_quarters_maximum": 9,
            "duration_source_conflict": True,
            "ects": None,
            "us_quarter_units": 36,
            "teaching_language": ["Unknown"],
            "teaching_languages": ["Unknown"],
            "program_url": PROGRAM,
            "program_status": "active",
            "relevance_status": "strong",
            "delivery_modes": ["on_campus"],
            "full_time_only": True,
            "distance_learning_in_this_record": False,
            "part_time_available": False,
            "tuition_eur_per_year": None,
            "annual_fee_eur": None,
            "qs_ranking": 49,
            "qs_ranking_display": "#49",
            "qs_ranking_year": 2027,
        }
    )

    row["prestige_profile"] = {
        "qs_world_rank": 49,
        "qs_edition": 2027,
        "qs_source_url": QS,
        "interpretation": bi(
            "The institutional rank is context only. Aerospace fit is evidenced separately by the degree, curriculum, aerospace laboratories and research areas.",
            "Kurum sırası yalnızca bağlamdır. Havacılık-uzay uyumu derece, müfredat, havacılık-uzay laboratuvarları ve araştırma alanlarıyla ayrıca kanıtlanır.",
        ),
    }

    row["eligibility_profile"] = {
        "eligible_for_non_eu": True,
        "required_previous_degree": bi(
            "A bachelor's degree comparable to a four-year US degree. UCLA's department says most applicants have mechanical/aerospace backgrounds, but suitably prepared electrical engineering, bioengineering and physics applicants can be competitive.",
            "Dört yıllık ABD derecesine denk bir lisans derecesi. Bölüm, adayların çoğunun makine/havacılık-uzay geçmişinden geldiğini; uygun hazırlığa sahip elektrik mühendisliği, biyomühendislik ve fizik adaylarının da rekabetçi olabileceğini belirtir.",
        ),
        "accepted_backgrounds": [
            bi("Aerospace engineering", "Havacılık ve uzay mühendisliği"),
            bi("Mechanical engineering", "Makine mühendisliği"),
            bi("Electrical engineering with relevant preparation", "İlgili hazırlığa sahip elektrik mühendisliği"),
            bi("Bioengineering with relevant preparation", "İlgili hazırlığa sahip biyomühendislik"),
            bi("Physics with relevant preparation", "İlgili hazırlığa sahip fizik"),
        ],
        "minimum_gpa": 3.0,
        "minimum_gpa_scale": 4.0,
        "minimum_gpa_is_university_floor": True,
        "minimum_gpa_guarantees_admission": False,
        "duplicate_related_masters_allowed": False,
        "duplicate_degree_rule": bi(
            "Applicants who already hold an MS or PhD in mechanical engineering, aerospace engineering or a closely related area are not admitted for a duplicate degree at the same level.",
            "Makine mühendisliği, havacılık-uzay mühendisliği veya yakın bir alanda zaten MS ya da doktora sahibi adaylar aynı düzeyde tekrar dereceye kabul edilmez.",
        ),
        "admission_mode": "holistic_program_review",
        "admission_risk": "high",
        "required_documents": [
            bi("UCLA online graduate application", "UCLA çevrim içi lisansüstü başvurusu"),
            bi("Unofficial transcript from each postsecondary institution at application", "Başvuruda her yükseköğretim kurumundan resmî olmayan transkript"),
            bi("Statement of purpose", "Amaç beyanı"),
            bi("Personal statement", "Kişisel beyan"),
            bi("Resume or CV", "Özgeçmiş"),
            bi("Three letters of recommendation", "Üç referans mektubu"),
            bi("Official GRE General score", "Resmî GRE General puanı"),
            bi("TOEFL iBT or IELTS Academic score when not exempt", "Muaf değilse TOEFL iBT veya IELTS Academic puanı"),
        ],
        "official_transcripts_required_at_application": False,
        "official_transcripts_required_after_accepting_admission": True,
        "english_translation_required_when_records_not_issued_in_english": True,
        "motivation_letter_required": True,
        "personal_statement_required": True,
        "cv_required": True,
        "recommendation_required": True,
        "recommendation_letter_count": 3,
        "portfolio_required": False,
        "interview_required": None,
        "interview_policy": "not_listed_in_checked_current_requirements",
        "application_fee_usd": 155,
        "application_fee_scope": "all applicants other than US citizens and permanent residents",
        "application_fee_refundable": False,
        "application_fee_waiver_possible": True,
        "application_fee_waiver_requires_named_program_or_documented_eligibility": True,
        "general_international_need_waiver_guaranteed": False,
        "gre": {
            "policy": "required",
            "cycle": "2026/2027",
            "test_type": "GRE General",
            "subject_test_required": False,
            "minimum_scores": {},
            "recommended_scores": {
                "verbal_percentile_above": 79,
                "quantitative_percentile_above": 92,
                "analytical_writing_above": 4.0,
            },
            "recommended_scores_are_cutoffs": False,
            "validity_years": 5,
            "institution_code": "4837",
            "aerospace_department_code": "1601",
            "must_take_by_deadline": True,
            "recommended_latest_test_date": "October 31",
            "source_ids": [ADMISSION_2026, MAE_ADMISSION],
        },
        "cycle_change_note": bi(
            "The official 2024-25 Aerospace listing said GRE optional; the current 2026-27 listing explicitly says GRE General required. This record follows the current cycle.",
            "Resmî 2024-25 Aerospace kaydı GRE'yi isteğe bağlı gösteriyordu; güncel 2026-27 kaydı GRE General'ı açıkça zorunlu kılıyor. Bu kayıt güncel dönemi izler.",
        ),
        "verification_notes": bi(
            "Meeting the 3.0 university floor does not guarantee admission. The department describes a comprehensive review and says qualified applicants substantially exceed available places.",
            "Üniversitenin 3,0 tabanını karşılamak kabul garantisi değildir. Bölüm kapsamlı değerlendirme yaptığını ve nitelikli aday sayısının mevcut yerleri önemli ölçüde aştığını belirtir.",
        ),
    }

    row["language_profile"] = {
        "teaching_language": ["Unknown"],
        "teaching_languages": ["Unknown"],
        "english_required": True,
        "requirement_scope": "all graduate applicants unless qualifying prior education meets the official exemption",
        "accepted_english_tests": [
            {
                "test": "TOEFL iBT",
                "minimum_score_policy": {
                    "test_before_2026_01_21": {"overall": 87},
                    "test_on_or_after_2026_01_21": {"overall": 4.5},
                },
                "mybest_accepted": False,
                "home_edition_accepted": True,
                "validity_years": 2,
            },
            {
                "test": "IELTS Academic",
                "minimum_score": 7.0,
                "online_test_accepted": True,
                "validity_years": 2,
            },
        ],
        "only_most_recent_score_considered": True,
        "exemptions": [
            bi(
                "A bachelor's degree or higher from an accredited US university or from a WHED-listed institution/country where English is the sole language of instruction.",
                "Akredite bir ABD üniversitesinden veya WHED'e göre İngilizcenin tek öğretim dili olduğu kurum/ülkeden lisans ya da daha yüksek derece.",
            )
        ],
        "citizenship_or_work_experience_alone_waives_requirement": False,
        "eslpe_after_admission_thresholds": {
            "toefl_before_2026_01_21_below": 100,
            "toefl_on_or_after_2026_01_21_below": 5,
            "ielts_below": 7.5,
        },
        "ta_oral_exemption_thresholds": {
            "toefl_speaking_before_2026_01_21": 28,
            "toefl_speaking_on_or_after_2026_01_21": 6,
            "ielts_speaking": 8.5,
            "ucla_top_clear_pass": 7.1,
        },
        "language_risk": "medium",
        "verification_notes": bi(
            "English testing and post-admission placement rules are verified, but no checked official page explicitly labels the MS teaching language. It remains Unknown rather than inferred.",
            "İngilizce sınav ve kabul sonrası yerleştirme kuralları doğrulandı; ancak kontrol edilen hiçbir resmî sayfa MS öğretim dilini açıkça etiketlemiyor. Çıkarım yapmak yerine Unknown bırakılır.",
        ),
    }

    row["cost_profile"] = {
        "academic_year": "2026/2027",
        "currency": "USD",
        "cost_scope": "new nonresident Academic Master student",
        "tuition_usd_per_year": 28242,
        "tuition_basis": "2026-27 Academic Master tuition plus Nonresident Supplemental Tuition for the international/nonresident target applicant",
        "mandatory_fees_usd_per_year": 1861.40,
        "registrar_final_direct_mandatory_charges_usd": 36985.40,
        "registrar_tuition_usd": 13140,
        "registrar_nonresident_supplemental_tuition_usd": 15102,
        "registrar_ucship_usd": 6882,
        "registrar_other_mandatory_fees_usd": 1861.40,
        "registrar_direct_charges_without_ucship_usd": 30103.40,
        "document_fee_new_student_usd": 94.32,
        "financial_aid_standard_nonresident_coa_usd": 76034,
        "total_cost_of_attendance_usd_per_year": 76034,
        "financial_aid_coa_is_bill": False,
        "financial_aid_coa_components_usd": {
            "university_fees": 15608,
            "nonresident_supplemental_tuition": 15102,
            "housing": 18221,
            "food": 10546,
            "books_materials_supplies_equipment": 2004,
            "transportation": 3819,
            "personal": 3219,
            "health_insurance": 7515,
        },
        "official_fee_layer_difference": bi(
            "The Registrar's final itemized charge table totals $36,985.40 for a new nonresident Academic Master student, while Financial Aid's standard COA uses preliminary fee and insurance figures and totals $76,034 including indirect expenses. The two figures have different purposes and are preserved separately.",
            "Registrar'ın nihai kalemli ücret tablosu yeni bir eyalet dışı Academic Master öğrencisi için 36.985,40 $ toplar; Financial Aid standart katılım maliyeti ise ön ücret ve sigorta rakamlarını kullanarak dolaylı giderlerle 76.034 $ toplar. İki rakam farklı amaçlara sahiptir ve ayrı tutulur.",
        ),
        "health_insurance_required": True,
        "health_insurance_premium_usd": 6882,
        "health_insurance_waiver_possible_with_qualifying_plan": True,
        "first_year_direct_university_cost_with_ship_usd": 36985.40,
        "complete_program_cost_usd": None,
        "tuition_eur_per_year_min": None,
        "tuition_eur_per_year_max": None,
        "tuition_eur_per_year_estimated": None,
        "total_first_year_cost_eur": None,
        "scholarship_availability": "very_limited_for_terminal_ms",
        "scholarship_risk": "very_high",
        "verification_notes": bi(
            "The $76,034 COA is a planning budget, not a bill. A complete-program total is not stated because time-to-degree varies and future fee levels are unknown.",
            "76.034 $ katılım maliyeti bir planlama bütçesidir, fatura değildir. Süre değiştiği ve gelecek ücretler bilinmediği için tam program toplamı verilmez.",
        ),
    }

    row["scholarship_profile"] = {
        "available_types": ["limited_gsr_after_enrollment", "limited_ta", "university_wide_or_external_funding"],
        "non_eu_eligible": None,
        "application_mode": "not_available",
        "application_mode_detail": "departmental financial support is not available to MS applicants; later TA/GSR searches are separate employment processes",
        "automatic_consideration": False,
        "separate_application_required": True,
        "departmental_financial_support_for_ms_available": False,
        "departmental_funding_guaranteed": False,
        "full_tuition_award_guaranteed": False,
        "teaching_assistantship_open_to_ms": True,
        "teaching_assistantship_timing": "incoming students during summer; current students in April",
        "teaching_assistantship_phd_priority": True,
        "phd_students_fill_nearly_all_ta_positions": True,
        "limited_mae_gsr_positions_for_ms": True,
        "gsr_typically_secured_after_enrollment": True,
        "gsr_faculty_contact_allowed": True,
        "federal_need_aid_available_to_typical_international_student": False,
        "scholarship_deadline": None,
        "opportunities": [],
        "funding_notes": bi(
            "UCLA MAE explicitly says MS applicants are not eligible for departmental financial support. A limited number of GSR positions may be secured after enrollment; PhD students fill nearly all TA positions. University-wide or external awards must be checked separately and are not promised here.",
            "UCLA MAE, MS adaylarının bölüm finansal desteğine uygun olmadığını açıkça belirtir. Sınırlı sayıdaki GSR pozisyonu kayıt sonrasında bulunabilir; TA pozisyonlarının neredeyse tamamını doktora öğrencileri doldurur. Üniversite geneli veya dış ödüller ayrıca kontrol edilmelidir ve burada vaat edilmez.",
        ),
        "verification_notes": bi(
            "Self-funding is the safe baseline for a terminal international MS unless the student receives a written appointment or external award.",
            "Öğrenci yazılı bir görevlendirme veya dış ödül almadıkça uluslararası terminal MS için güvenli varsayım öz-finansmandır.",
        ),
    }

    row["living_profile"] = {
        "city_type": "Metropolis",
        "housing_search_difficulty": "very_high",
        "living_cost_risk": "very_high",
        "living_risk": "high",
        "student_housing_available": True,
        "student_dorm_availability": "available_limited",
        "housing_access": "lottery",
        "housing_access_detail": "lottery numbers determine offers; unsuccessful applicants remain on a wait list and no offer is guaranteed",
        "housing_application_separate": True,
        "housing_application_after_admission": True,
        "housing_application_fee_usd": None,
        "housing_guaranteed": False,
        "lottery_cutoff_for_equal_number_assignment": "July 1",
        "lottery_numbers_assigned": "early July",
        "offers_begin": "early July",
        "offers_may_continue_until": "mid-April of the following year",
        "incoming_single_graduate_housing_eligibility_cap_years": 3,
        "monthly_housing_rent_usd_per_month_min": 1146,
        "monthly_housing_rent_usd_per_month_max": 3269,
        "rent_range_scope": "named 2026-27 UCLA single-graduate units, per person; not a citywide market average",
        "official_coa_housing_usd": 18221,
        "official_coa_food_usd": 10546,
        "housing_notes": bi(
            "Current university units range from $1,146 per person in a listed shared unit to $3,269 for a listed single-occupancy loft configuration. Availability is assigned by lottery and wait list, not guaranteed.",
            "Güncel üniversite birimleri listelenmiş paylaşımlı birimde kişi başı 1.146 $ ile listelenmiş tek kişilik loft düzeninde 3.269 $ arasında değişir. Yerleştirme kura ve bekleme listesiyle yapılır; garanti değildir.",
        ),
        "verification_notes": bi(
            "The published range is property- and occupancy-specific. It is not used as a claim about the Los Angeles private rental market.",
            "Yayımlanan aralık mülk ve doluluk tipine özgüdür. Los Angeles özel kiralama piyasası hakkında iddia olarak kullanılmaz.",
        ),
    }

    row["curriculum_profile"] = {
        "structure": bi(
            "Nine courses / 36 quarter units with thesis and capstone routes; at least five courses / 20 units must be graduate level.",
            "Tezli ve bitirme seçenekleriyle dokuz ders / 36 çeyrek birim; en az beş ders / 20 birim lisansüstü düzeyde olmalıdır.",
        ),
        "credit_hours_total": 36,
        "quarter_units_total": 36,
        "course_count": 9,
        "course_count_summary": bi("9 courses / 36 quarter units", "9 ders / 36 çeyrek birim"),
        "taught_project_and_seminar_component_count": 9,
        "graduate_course_count_minimum": 5,
        "graduate_units_minimum": 20,
        "thesis_required": False,
        "thesis_route_available": True,
        "capstone_route_available": True,
        "thesis_route_formal_courses": 7,
        "thesis_route_200_series_courses_minimum": 4,
        "thesis_route_598_courses_maximum": 2,
        "thesis_original_independent_research_required": True,
        "thesis_exam_required": False,
        "thesis_planning_recommended_lead_time": "approximately one year before degree award",
        "capstone_500_series_units_allowed": False,
        "capstone_formats": [
            bi("First part of the doctoral written qualifying examination", "Doktora yazılı yeterlik sınavının ilk bölümü"),
            bi("Research or design project with a final report", "Nihai raporlu araştırma veya tasarım projesi"),
            bi("Three extra examination questions in three graduate courses", "Üç lisansüstü derste üç ek sınav sorusu"),
            bi("Oral examination administered by the MS committee", "MS komitesi tarafından yürütülen sözlü sınav"),
        ],
        "capstone_reexamination_once_possible_with_consent": True,
        "breadth_requirement_applies_without_abet_aerospace_or_mechanical_bs": True,
        "breadth_courses_required_minimum": 3,
        "breadth_categories": [
            ["MAE 162A", "MAE 169A", "MAE 171A"],
            ["MAE 150A", "MAE 150B"],
            ["MAE 131A", "MAE 133A"],
            ["MAE 156A"],
            ["MAE 162B"],
        ],
        "areas_of_study": [
            bi("Dynamics", "Dinamik"),
            bi("Fluid mechanics", "Akışkanlar mekaniği"),
            bi("Heat and mass transfer", "Isı ve kütle transferi"),
            bi("Structural and solid mechanics", "Yapı ve katı mekaniği"),
            bi("Systems and control", "Sistemler ve kontrol"),
        ],
        "mandatory_internship": False,
        "internship_required": False,
        "teaching_experience_required": False,
        "field_experience_required": False,
        "foreign_language_requirement": "none",
        "full_time_minimum_units_per_quarter": 12,
        "duration_quarters_average": 5,
        "duration_quarters_maximum": 9,
        "flexibility": "high_between_thesis_and_capstone_routes",
        "curriculum_risk": "medium",
        "verification_notes": bi(
            "This record is the on-campus MS in Aerospace Engineering, not UCLA's separate online MS in Engineering-Aerospace. The detailed 2025-26 requirement is retained with medium confidence because UCLA's indexed current requirement page is unstable; the department's live checklist and capstone pages independently confirm nine courses and 36 units.",
            "Bu kayıt kampüsteki Aerospace Engineering MS'idir; UCLA'nın ayrı çevrim içi MS in Engineering-Aerospace programı değildir. UCLA'nın dizinlenmiş güncel şart sayfası kararsız olduğundan ayrıntılı 2025-26 şart orta güvenle tutulur; bölümün canlı kontrol listesi ve bitirme sayfaları dokuz ders ile 36 birimi bağımsız olarak doğrular.",
        ),
    }

    row["category_profile"] = {
        "primary_categories": ["aerospace_engineering", "air_and_space"],
        "secondary_categories": [
            "spacecraft_propulsion",
            "rocket_propulsion",
            "hypersonics",
            "cfd",
            "aerodynamics",
            "structures",
            "gnc_controls",
            "spacecraft_systems",
            "orbital_dynamics",
        ],
        "technical_focus": bi(
            "Air and space systems, propulsion, hypersonics, CFD, structures, spacecraft dynamics and controls.",
            "Hava ve uzay sistemleri, itki, hipersonik, HAD, yapılar, uzay aracı dinamiği ve kontrol.",
        ),
        "verification_notes": bi(
            "Categories are normalized from the official curriculum areas, Air & Space page and named laboratories.",
            "Kategoriler resmî müfredat alanları, Air & Space sayfası ve adlandırılmış laboratuvarlardan normalize edilmiştir.",
        ),
    }

    row["research_profile"] = {
        "research_focus_areas": [
            bi("Advanced space systems and propulsion", "İleri uzay sistemleri ve itki"),
            bi("Rocket and air-breathing propulsion", "Roket ve hava soluyan itki"),
            bi("Hypersonics and computational aerodynamics", "Hipersonik ve hesaplamalı aerodinamik"),
            bi("CFD, flow control and unsteady aerodynamics", "HAD, akış kontrolü ve kararsız aerodinamik"),
            bi("Formation flight, autonomous vehicles and controls", "Formasyon uçuşu, otonom araçlar ve kontrol"),
            bi("Aircraft/spacecraft structures and aeroelasticity", "Uçak/uzay aracı yapıları ve aeroelastisite"),
        ],
        "key_institutes": [
            "Advanced Space Systems and Propulsion Laboratory",
            "Autonomous Vehicle Systems Instrumentation Laboratory",
            "Collaborative Center for Aerospace Sciences",
            "Computational Fluid Dynamics Laboratory",
            "Energy and Propulsion Research Laboratory",
            "Hypersonics and Computational Aerodynamics Group",
            "Laser Spectroscopy and Gas Dynamics Laboratory",
        ],
        "hands_on_facilities_verified": True,
        "individual_lab_place_guaranteed": False,
        "thesis_adviser_guaranteed": False,
        "research_funding_level": "unknown",
        "research_risk": "medium",
        "verification_notes": bi(
            "UCLA documents substantial aerospace research infrastructure across spacecraft propulsion, HIL formation-control testing, combustion, CFD and hypersonics. A named lab does not guarantee an MS position, thesis adviser or funding.",
            "UCLA; uzay aracı itki, HIL formasyon kontrol testleri, yanma, HAD ve hipersonik alanlarında güçlü havacılık-uzay araştırma altyapısı belgeler. Adlandırılmış laboratuvar MS pozisyonu, tez danışmanı veya finansman garantisi değildir.",
        ),
    }

    row["industry_ecosystem_profile"] = {
        "local_industry_strength": "high",
        "verified_partnerships": [
            "Collaborative Center for Aerospace Sciences collaboration with AFRL/RQR at Edwards Air Force Base"
        ],
        "key_companies": [],
        "placement_rate": None,
        "alumni_presence": None,
        "international_access_risk": "high",
        "export_control_context": bi(
            "The checked sources do not establish blanket international access to defence- or export-controlled projects. Eligibility must be assessed for each laboratory, sponsor, internship and employer.",
            "Kontrol edilen kaynaklar savunma veya ihracat kontrollü projelere uluslararası öğrenciler için genel erişim kanıtlamaz. Uygunluk her laboratuvar, sponsor, staj ve işveren için ayrı değerlendirilmelidir.",
        ),
        "verification_notes": bi(
            "The AFRL collaboration is verified by UCLA's laboratory page. The prior unsourced claims of partnerships with Aerospace Corporation, JPL and Raytheon were removed.",
            "AFRL iş birliği UCLA laboratuvar sayfasıyla doğrulandı. Aerospace Corporation, JPL ve Raytheon ile ortaklık olduğuna dair önceki kaynaksız iddialar kaldırıldı.",
        ),
    }

    row["application_timeline_profile"] = {
        "application_period": "Fall only",
        "non_eu_deadline": bi("2026-12-01 for Fall 2027", "2027 Güz için 2026-12-01"),
        "deadline_non_eu": "2026-12-01",
        "submission_opens_approximately": "mid-September 2026",
        "application_rounds": [
            {
                "intake": "Fall 2027",
                "round": bi("Fall 2027 admission", "2027 Güz kabulü"),
                "deadline": "2026-12-01",
                "gre_required": True,
            }
        ],
        "all_required_materials_due_by_deadline": True,
        "late_complete_file_review_guaranteed": False,
        "faculty_review_begins": "primarily January",
        "department_decision_target": "no later than April 15 for completed applications according to MAE page",
        "funded_offer_response_deadline": "April 15",
        "other_admitted_student_sir_deadline": "June 15",
        "pre_enrollment_required": True,
        "post_admission_steps": [
            bi("Submit the Statement of Intent to Register", "Statement of Intent to Register belgesini gönderin"),
            bi("Submit the Statement of Legal Residence", "Statement of Legal Residence belgesini gönderin"),
            bi("Provide official final academic records", "Resmî nihai akademik belgeleri sunun"),
            bi("Provide financial documentation before I-20/DS-2019 issuance", "I-20/DS-2019 düzenlenmeden önce finansal belge sunun"),
            bi("Apply separately for graduate housing and plan a private-market backup", "Lisansüstü konuta ayrıca başvurun ve özel piyasa yedek planı hazırlayın"),
        ],
        "visa_financial_documentation_required": True,
        "current_i20_financial_amount_usd": None,
        "visa_complexity": "high",
        "timeline_risk": "medium",
        "verification_notes": bi(
            "The current cycle-specific Aerospace page controls the date and GRE rule. The live application should still be rechecked before submission.",
            "Tarih ve GRE kuralında güncel döneme özgü Aerospace sayfası esas alınır. Göndermeden önce canlı başvuru yine kontrol edilmelidir.",
        ),
    }

    row["student_sentiment_profile"] = {
        "student_satisfaction_score": None,
        "workload_sentiment": "unknown",
        "teaching_quality_sentiment": "unknown",
        "administration_sentiment": "unknown",
        "housing_sentiment": "negative_risk_signal",
        "city_life_sentiment": "unknown",
        "international_student_sentiment": "unknown",
        "career_support_sentiment": "unknown",
        "student_sentiment_summary": bi(
            "Recent graduate-housing discussions repeatedly describe uncertainty about lottery position, late offers and the need for a backup search. These anecdotes support only a conservative housing-risk signal; they do not rate Aerospace teaching or careers.",
            "Yakın tarihli lisansüstü konut tartışmaları kura sırası, geç teklifler ve yedek arama gereksinimi konusunda tekrarlanan belirsizlik bildirir. Bu anekdotlar yalnızca ihtiyatlı konut riski sinyalini destekler; Aerospace öğretimi veya kariyerini puanlamaz.",
        ),
        "student_sentiment_sources": [
            {"url": REDDIT_1, "topic": "graduate housing likelihood and backup planning"},
            {"url": REDDIT_2, "topic": "graduate housing wait-list uncertainty"},
            {"url": REDDIT_3, "topic": "2026 graduate housing lottery positions and offers"},
        ],
        "approximate_comment_sample_size": 18,
        "sentiment_date_range": "2026-02 to 2026-07",
        "sentiment_confidence": "low",
        "verification_notes": bi(
            "No satisfaction score is calculated; anonymous anecdotes are not used as rent, safety, admission or academic facts.",
            "Memnuniyet puanı hesaplanmaz; anonim anekdotlar kira, güvenlik, kabul veya akademik gerçek olarak kullanılmaz.",
        ),
    }

    sources = [
        source(PROGRAM, "UCLA Aerospace Engineering Graduate Program", "official_program_page", ["program", "degree", "major_code"], "Separate active Aerospace Engineering MS/PhD program and major code 0279.", "Ayrı ve aktif Aerospace Engineering MS/PhD programı ile 0279 ana dal kodu."),
        source(ADMISSION_2026, "UCLA 2026-27 Aerospace Engineering Admission Requirements", "official_admission_page", ["program", "deadline", "gre", "recommendations", "documents"], "Current cycle-specific December 1, 2026 deadline, required GRE General, three recommendations and application materials.", "Güncel döneme özgü 1 Aralık 2026 tarihi, zorunlu GRE General, üç referans ve başvuru belgeleri."),
        source(MAE_ADMISSION, "UCLA MAE Graduate Admissions and FAQ", "official_admission_page", ["admission", "gre", "deadline", "documents", "duration", "funding", "housing"], "Department eligibility, test, timing, full-time and MS funding guidance; obsolete dollar examples are not used.", "Bölüm uygunluk, sınav, zamanlama, tam zamanlılık ve MS finansman rehberi; eski dolar örnekleri kullanılmaz."),
        source(GENERAL_APPLY, "UCLA Graduate Application Process and Requirements", "official_admission_page", ["application_fee", "fee_waiver", "gpa", "documents", "non_eu_eligibility"], "Current central application fee, waiver categories, minimum preparation and essay rules.", "Güncel merkezî başvuru ücreti, muafiyet kategorileri, asgari hazırlık ve beyan kuralları."),
        source(INTERNATIONAL, "UCLA International Applicants", "official_admission_page", ["non_eu_eligibility", "documents", "visa"], "International academic records and post-admission official-document process.", "Uluslararası akademik belgeler ve kabul sonrası resmî belge süreci."),
        source(ENGLISH, "UCLA Graduate English Requirements", "official_admission_page", ["english_proficiency", "tests", "exemptions", "eslpe", "ta_oral"], "Current TOEFL/IELTS admission, validity, exemption, ESLPE and TA oral-proficiency rules.", "Güncel TOEFL/IELTS kabul, geçerlilik, muafiyet, ESLPE ve TA sözlü yeterlik kuralları."),
        source(CURRICULUM_INDEX, "UCLA 2025-26 Graduate Program Requirements Index", "official_curriculum_page", ["curriculum", "duration", "thesis", "capstone", "breadth"], "Current-year official requirements index; the direct indexed detail URL is unstable, so detailed claims are cross-checked with department sources.", "Güncel yıl resmî şartlar dizini; doğrudan ayrıntı URL'si kararsız olduğundan ayrıntılı iddialar bölüm kaynaklarıyla çapraz kontrol edilir.", confidence="medium"),
        source(MS_CHECKLIST, "UCLA MAE MS Graduation Checklist", "official_curriculum_page", ["curriculum", "course_count", "units", "gpa"], "Live department checklist for MS completion requirements.", "MS tamamlama şartları için canlı bölüm kontrol listesi."),
        source(MS_PROGRAM_PDF, "UCLA MAE Guidelines for MS Program of Study", "official_curriculum_page", ["curriculum", "course_count", "units", "thesis", "capstone"], "Official department PDF confirming nine courses, graduate-level minimum and thesis/comprehensive rules; older supporting document.", "Dokuz ders, lisansüstü asgari sayı ve tez/kapsamlı sınav kurallarını doğrulayan resmî bölüm PDF'si; eski destek belgesi.", confidence="medium", access_status="pdf"),
        source(CAPSTONE_EXAMS, "UCLA MAE Three Extra Written Exams MS Route", "official_curriculum_page", ["curriculum", "capstone", "course_count", "units"], "Current department procedure independently confirming nine courses and 36 units for this capstone route.", "Bu bitirme yolu için dokuz ders ve 36 birimi bağımsız doğrulayan güncel bölüm prosedürü."),
        source(FEES, "UCLA Annual and Term Student Fees - Academic Master", "official_tuition_page", ["tuition", "fees", "insurance"], "Final itemized 2026-27 new/nonresident Academic Master charges.", "Kalemli nihai 2026-27 yeni/eyalet dışı Academic Master ücretleri.", access_status="requires_js"),
        source(COA, "UCLA 2026-27 Graduate Cost of Attendance", "official_cost_of_living_page", ["tuition", "living_cost", "housing", "food", "insurance", "coa"], "Standard nonresident planning budget and direct/indirect components; explicitly not a bill.", "Standart eyalet dışı planlama bütçesi ve doğrudan/dolaylı bileşenler; açıkça fatura değildir."),
        source(CATALOG_FEES, "UCLA Graduate Fees and Payment", "official_tuition_page", ["tuition", "nrst", "insurance"], "Policy context for NRST and automatic health-insurance assessment.", "NRST ve otomatik sağlık sigortası tahakkuku için politika bağlamı."),
        source(FINANCIAL_SUPPORT, "UCLA Graduate Financial Support", "official_scholarship_page", ["funding", "fellowship", "assistantships", "nonresident_awards"], "University-wide funding types; department rules control terminal-MS availability.", "Üniversite geneli finansman türleri; terminal MS uygunluğunda bölüm kuralları esas alınır."),
        source(HOUSING_APPLICATION, "UCLA Graduate Housing Application Process", "official_housing_page", ["housing", "application", "lottery", "waitlist", "guarantee"], "Current 2026-27 application, lottery, wait-list, offer and eligibility-cap rules.", "Güncel 2026-27 başvuru, kura, bekleme listesi, teklif ve uygunluk süresi kuralları."),
        source(HOUSING_RATES, "UCLA 2026-27 Single Graduate Housing Rates", "official_housing_page", ["housing", "housing_rate"], "Current property- and occupancy-specific per-person monthly rates.", "Güncel mülk ve doluluk tipine özgü kişi başı aylık ücretler."),
        source(LABS, "UCLA MAE Laboratories", "official_lab_page", ["research", "labs", "facilities", "industry_partnership"], "Named spacecraft, propulsion, HIL controls, CFD, hypersonics and AFRL-collaboration facilities.", "Adlandırılmış uzay aracı, itki, HIL kontrol, HAD, hipersonik ve AFRL iş birliği tesisleri."),
        source(AIR_SPACE, "UCLA MAE Air & Space Research", "official_department_page", ["research", "technical_fit"], "Current air/space topics spanning propulsion, controls, spacecraft design, CFD and hypersonics.", "İtki, kontrol, uzay aracı tasarımı, HAD ve hipersoniği kapsayan güncel hava/uzay konuları."),
        source(RESEARCH_AREAS, "UCLA MAE Graduate Research Areas", "official_department_page", ["research", "structures", "controls", "thermal"], "Graduate research breadth including aircraft/spacecraft structures, aeroelasticity and control systems.", "Uçak/uzay aracı yapıları, aeroelastisite ve kontrol sistemleri dâhil lisansüstü araştırma genişliği."),
        source(QS, "QS - University of California, Los Angeles", "ranking_provider", ["prestige"], "QS World University Ranking 2027: #49; institutional context only.", "QS Dünya Üniversite Sıralaması 2027: #49; yalnızca kurumsal bağlam.", confidence="medium"),
        source(REDDIT_1, "Reddit r/ucla - Likelihood of graduate housing", "student_forum", ["housing_sentiment"], "Recent anecdotal concern about timing and backup housing; perception only.", "Zamanlama ve yedek konut hakkında yakın tarihli anekdotal kaygı; yalnızca algı.", confidence="low"),
        source(REDDIT_2, "Reddit r/ucla - Graduate housing", "student_forum", ["housing_sentiment"], "Recent wait-list uncertainty and backup-search discussion; perception only.", "Yakın tarihli bekleme listesi belirsizliği ve yedek arama tartışması; yalnızca algı.", confidence="low"),
        source(REDDIT_3, "Reddit r/ucla - 2026 graduate housing wait list", "student_forum", ["housing_sentiment"], "Multiple 2026 lottery-position and offer anecdotes; perception only.", "Birden fazla 2026 kura sırası ve teklif anekdotu; yalnızca algı.", confidence="low"),
    ]

    row["source_profile"] = {
        "primary_url": PROGRAM,
        "secondary_urls": [item["url"] for item in sources[1:]],
        "last_verified": TODAY,
        "field_confidence": {
            "program_basic_info": "high",
            "program": "high",
            "duration": "medium",
            "language": "unknown",
            "english_proficiency": "high",
            "admission": "high",
            "gre": "high",
            "non_eu_eligibility": "high",
            "tuition": "high",
            "scholarship": "high",
            "deadline": "high",
            "curriculum": "medium",
            "research": "high",
            "industry_ecosystem": "medium",
            "housing": "high",
            "living": "high",
            "sentiment": "low",
            "prestige": "medium",
        },
        "source_reliability": "high",
        "verification_status": "partially_verified",
        "needs_verification": True,
        "verification_notes": bi(
            "The prior combined Mechanical/Aerospace record is corrected to the separate Aerospace Engineering MS. Current admissions, English rules, direct charges, COA, funding limits, housing and research are sourced. Explicit teaching language and a fixed complete-program cost remain unverified.",
            "Önceki birleşik Mechanical/Aerospace kaydı ayrı Aerospace Engineering MS olarak düzeltildi. Güncel kabul, İngilizce kuralları, doğrudan ücretler, katılım maliyeti, finansman sınırları, konut ve araştırma kaynaklıdır. Açık öğretim dili ve sabit tam program maliyeti doğrulanmamış kalır.",
        ),
        "source_log": sources,
    }

    row["decision_summary"] = {
        "best_for": [
            bi("Students seeking an on-campus aerospace MS with strong propulsion, hypersonics, CFD, structures and controls research options.", "İtki, hipersonik, HAD, yapılar ve kontrolde güçlü araştırma seçenekli kampüs Aerospace MS'i arayan öğrenciler."),
            bi("Applicants who can self-fund and want thesis/capstone flexibility in a major aerospace metropolitan ecosystem.", "Öz-finansman sağlayabilen ve büyük bir havacılık-uzay metropol ekosisteminde tez/bitirme esnekliği isteyen adaylar."),
        ],
        "not_ideal_for": [
            bi("Terminal-MS applicants who require guaranteed departmental funding.", "Garantili bölüm finansmanına ihtiyaç duyan terminal MS adayları."),
            bi("Applicants who cannot tolerate a high-cost city and uncertain university housing.", "Yüksek maliyetli şehir ve belirsiz üniversite konutunu karşılayamayan adaylar."),
        ],
        "main_strengths": [
            bi("A separate Aerospace Engineering degree with thesis and four capstone completion formats.", "Tez ve dört bitirme formatına sahip ayrı Aerospace Engineering derecesi."),
            bi("Named laboratories in spacecraft propulsion, hypersonics, CFD, HIL formation control and rocket combustion.", "Uzay aracı itki, hipersonik, HAD, HIL formasyon kontrolü ve roket yanmasında adlandırılmış laboratuvarlar."),
            bi("Verified UCLA-AFRL aerospace research collaboration.", "Doğrulanmış UCLA-AFRL havacılık-uzay araştırma iş birliği."),
        ],
        "main_risks": [
            bi("The Registrar's current new-nonresident direct charges are $36,985.40; UCLA's standard nonresident COA budget is $76,034.", "Registrar'ın güncel yeni eyalet dışı doğrudan ücretleri 36.985,40 $; UCLA standart eyalet dışı katılım maliyeti bütçesi 76.034 $'dır."),
            bi("MS applicants are not eligible for departmental financial support; TA/GSR opportunities are limited and not admission funding.", "MS adayları bölüm finansal desteğine uygun değildir; TA/GSR olanakları sınırlıdır ve kabul finansmanı değildir."),
            bi("Graduate housing is a separate lottery/wait-list process and is not guaranteed.", "Lisansüstü konut ayrı kura/bekleme listesi sürecidir ve garanti değildir."),
            bi("GRE General is required for the current 2026-27 cycle, despite an older cycle listing it as optional.", "Eski bir dönem GRE'yi isteğe bağlı göstermesine rağmen güncel 2026-27 döneminde GRE General zorunludur."),
            bi("Teaching language is not explicitly stated in the checked official sources.", "Öğretim dili kontrol edilen resmî kaynaklarda açıkça belirtilmez."),
        ],
        "decision_summary": bi(
            "UCLA is a technically strong, research-rich aerospace option with real depth across air and space topics and flexible MS completion routes. The deciding weakness is financial: a terminal international MS should be planned as self-funded, with university housing treated as a lottery rather than an entitlement. Apply by December 1, 2026 with GRE, three recommendations, both statements and a CV.",
            "UCLA, hava ve uzay konularında gerçek derinliğe ve esnek MS tamamlama yollarına sahip teknik olarak güçlü, araştırma zengini bir Aerospace seçeneğidir. Belirleyici zayıflık finansmandır: uluslararası terminal MS öz-finansmanlı planlanmalı, üniversite konutu hak değil kura olarak görülmelidir. GRE, üç referans, iki beyan ve CV ile 1 Aralık 2026'ya kadar başvurun.",
        ),
        "pros": [],
        "cons": [],
        "verdict": bi(
            "Excellent technical fit and research breadth; financially safe only with a credible self-funding plan or written appointment.",
            "Mükemmel teknik uyum ve araştırma genişliği; yalnızca güvenilir öz-finansman planı veya yazılı görevlendirmeyle finansal olarak güvenli.",
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
            "gre_required_current_cycle",
            "terminal_ms_department_funding_unavailable",
            "high_nonresident_cost",
            "graduate_housing_not_guaranteed",
            "complete_program_cost_unknown",
            "export_control_access_project_specific",
        ],
    }

    row["data_quality"] = {
        "status": "partial",
        "checked_official_source_count": 18,
        "verified_fields": [
            "program",
            "degree",
            "major_code",
            "admission",
            "gre",
            "non_eu_eligibility",
            "english_proficiency",
            "tuition",
            "cost_of_attendance",
            "scholarship",
            "deadline",
            "curriculum_core_structure",
            "research",
            "industry_partnership",
            "housing",
            "living",
            "insurance_requirement",
            "prestige",
        ],
        "unverified_critical_fields": ["language"],
        "known_semantic_gaps": [
            "explicit_teaching_language",
            "fixed_complete_program_cost",
            "current_i20_financial_amount",
            "admission_rate",
            "private_market_rent",
            "guaranteed_individual_lab_access",
            "international_eligibility_for_individual_restricted_projects",
        ],
        "official_source_conflicts": ["duration_four_vs_five_quarters", "registrar_direct_charges_vs_preliminary_financial_aid_fee_layer"],
        "has_checked_source_log": True,
        "audited_at": TODAY,
    }

    row["quality_control"] = {
        "checked_at": TODAY,
        "qc_status": "needs_revision",
        "remaining_verification_tasks": [
            bi("Find a current official source explicitly stating the on-campus MS teaching language.", "Kampüsteki MS öğretim dilini açıkça belirten güncel resmî kaynak bulun."),
            bi("Recheck the live application and fee tables immediately before submission/payment.", "Gönderim/ödeme öncesinde canlı başvuru ve ücret tablolarını yeniden kontrol edin."),
            bi("Confirm project-specific international access directly with a prospective laboratory or adviser.", "Projeye özgü uluslararası erişimi doğrudan olası laboratuvar veya danışmanla doğrulayın."),
        ],
        "qc_notes": bi(
            "The merged-degree error, obsolete GRE policy, unsupported partnerships, unsupported sentiment and invented scoring were removed. Remaining unknowns are explicit rather than estimated.",
            "Birleştirilmiş derece hatası, eski GRE politikası, kaynaksız ortaklıklar, kaynaksız duygu analizi ve uydurma puanlama kaldırıldı. Kalan bilinmeyenler tahmin edilmek yerine açıkça belirtilir.",
        ),
        "failed_canary_tests": ["teaching_language_not_explicitly_verified"],
    }

    DATA_PATH.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    audit = {
        "record_id": row["id"],
        "checked_at": TODAY,
        "validation_method": "indexed web search/open validation and official page cross-check",
        "audit_validity": "valid",
        "summary": {
            "total_urls": len(sources),
            "official_urls": 19,
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
            "Critical claims use official sources. The three Reddit sources are used only for conservative housing sentiment. No broken URL is retained as primary evidence.",
            "Kritik iddialar resmî kaynakları kullanır. Üç Reddit kaynağı yalnızca ihtiyatlı konut algısı için kullanılır. Hiçbir bozuk URL birincil kanıt olarak tutulmaz.",
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
