from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data_base" / "amerika.json"
AUDIT_PATH = ROOT / "reports" / "source_link_audit_usc_astronautical_ms_2026-08-14.json"
TODAY = "2026-08-14"

PROGRAM = "https://viterbigradadmission.usc.edu/programs/masters/msprograms/astronautical-engineering/ms-astronautical-engineering/"
DEPARTMENT_MS = "https://astronautics.usc.edu/academics/master-science-program/"
DEPARTMENT_ADMISSION = "https://astronautics.usc.edu/admission/"
VITERBI_APPLY = "https://viterbigradadmission.usc.edu/apply-masters-programs/"
INTERNATIONAL_APPLY = "https://gradadm.usc.edu/prospective-international-students/how-to-apply-as-an-international-student/"
ENGLISH = "https://gradadm.usc.edu/prospective-international-students/english-proficiency/"
COUNTRY = "https://gradadm.usc.edu/prospective-international-students/country-requirements/"
NEXT_STEPS = "https://gradadm.usc.edu/admitted-international-students/international-student-next-steps/"
FINANCIAL_DOCS = "https://gradadm.usc.edu/overview-of-student-visas/financial-documentation-requirements/"
TUITION = "https://viterbigradadmission.usc.edu/programs/masters/tuition-funding/tuition-funding-masters/"
COA_PDF = "https://viterbigradadmission.usc.edu/wp-content/uploads/2026/03/2026-2027-Tuition-and-Fees-27.pdf"
SCHOLARSHIPS = "https://viterbigradadmission.usc.edu/programs/masters/tuition-funding/gradscholarships/"
FAQ = "https://viterbigradadmission.usc.edu/programs/masters/faq/"
HEALTH = "https://studenthealth.usc.edu/fees-deadlines/"
HOUSING_APPLICATION = "https://housing.usc.edu/index.php/application-4/"
GRAD_HOUSING = "https://resed.usc.edu/residential-communities-2/new-graduate-family/"
TROY_EAST = "https://housing.usc.edu/index.php/buildings/troy-east/"
WINDSOR = "https://housing.usc.edu/index.php/buildings/windsor/"
STARDUST = "https://housing.usc.edu/index.php/buildings/stardust/"
RESEARCH = "https://astronautics.usc.edu/research/"
ABOUT = "https://astronautics.usc.edu/about/"
STUDENT_ORGS = "https://astronautics.usc.edu/student-organizations/"
EXPORT = "https://oec.usc.edu/compliance-programs/international-activity/research/"
QS = "https://www.topuniversities.com/universities/university-southern-california"

REDDIT_HOUSING_1 = "https://www.reddit.com/r/USC/comments/1i64oq6"
REDDIT_HOUSING_2 = "https://www.reddit.com/r/USC/comments/1koylxv/looking_for_graduate_housing/"
REDDIT_HOUSING_3 = "https://www.reddit.com/r/USC/comments/1i2nk5x/graduate_housing_options_everything_looks_so_bleak/"
REDDIT_HOUSING_4 = "https://www.reddit.com/r/USC/comments/1rdfca1/graduate_housing/"


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
    row = next(item for item in rows if item.get("id") == "usc-viterbi")

    row.update(
        {
            "country": "United States",
            "university": "University of Southern California",
            "university_native_name": "University of Southern California (USC)",
            "city": "Los Angeles",
            "region": "California",
            "program_name": "Master of Science in Astronautical Engineering",
            "program_native_name": "Master of Science in Astronautical Engineering",
            "program_degree": "MS",
            "degree_level": "Master",
            "duration_years": 2,
            "duration": bi(
                "Four semesters in USC's current typical 27-unit cost plan; individual pace may vary.",
                "USC'nin güncel tipik 27 birimlik maliyet planında dört dönem; bireysel tempo değişebilir.",
            ),
            "ects": None,
            "us_credit_hours": 27,
            "teaching_language": ["Unknown"],
            "teaching_languages": ["Unknown"],
            "program_url": PROGRAM,
            "program_status": "active",
            "relevance_status": "strong",
            "delivery_modes": ["on_campus", "online_den_viterbi"],
            "international_on_campus_stem_opt_eligible": True,
            "tuition_eur_per_year": None,
            "annual_fee_eur": None,
            "qs_ranking": 153,
            "qs_ranking_display": "#153",
            "qs_ranking_year": 2027,
        }
    )

    row["prestige_profile"] = {
        "qs_world_rank": 153,
        "qs_edition": 2027,
        "qs_source_url": QS,
        "interpretation": bi(
            "The QS institutional rank is context only. Technical fit is established independently from the dedicated astronautics curriculum, department, laboratories and research groups.",
            "QS kurum sırası yalnızca bağlamdır. Teknik uyum; özel astronotik müfredatı, bölüm, laboratuvarlar ve araştırma gruplarıyla bağımsız olarak belirlenir.",
        ),
    }

    row["eligibility_profile"] = {
        "eligible_for_non_eu": True,
        "international_f1_route": "on_campus_delivery",
        "stem_opt_extension_eligible": True,
        "required_previous_degree": bi(
            "A bachelor's degree, completed or in progress. Most applicants come from engineering or closely related sciences such as chemistry and physics.",
            "Tamamlanmış veya devam eden bir lisans derecesi. Adayların çoğu mühendislikten veya kimya ve fizik gibi yakın fen alanlarından gelir.",
        ),
        "accepted_backgrounds": [
            bi("Astronautical, aerospace, mechanical, electrical or other engineering", "Astronotik, havacılık-uzay, makine, elektrik veya diğer mühendislikler"),
            bi("Physics, astronomy, chemistry or another closely related science", "Fizik, astronomi, kimya veya başka bir yakın fen alanı"),
            bi("Other fields with strong demonstrated mathematics and physics preparation", "Güçlü ve belgelenmiş matematik-fizik hazırlığı bulunan diğer alanlar"),
        ],
        "expected_prerequisites": [
            bi("Strong proficiency in mathematics", "Matematikte güçlü yeterlilik"),
            bi("Strong proficiency in physics", "Fizikte güçlü yeterlilik"),
        ],
        "possible_deficiency_courses": bi(
            "The department may require one or two upper-division undergraduate deficiency courses in some cases.",
            "Bölüm bazı durumlarda bir veya iki üst düzey lisans tamamlama dersi isteyebilir.",
        ),
        "minimum_gpa": 3.0,
        "minimum_gpa_source_scope": "department_admission_page",
        "minimum_gpa_confidence": "medium",
        "admission_mode": "holistic_program_review",
        "admission_risk": "high",
        "required_documents": [
            bi("Online USC graduate application", "Çevrim içi USC lisansüstü başvurusu"),
            bi("Transcripts", "Transkriptler"),
            bi("Resume or CV", "Özgeçmiş"),
            bi("Personal statement", "Kişisel beyan"),
            bi("Two letters of recommendation", "İki referans mektubu"),
            bi("Official English-proficiency scores when required", "Gerektiğinde resmî İngilizce yeterlilik puanları"),
        ],
        "motivation_letter_required": True,
        "cv_required": True,
        "recommendation_required": True,
        "recommendation_letter_count": 2,
        "portfolio_required": False,
        "interview_required": None,
        "interview_policy": "not_listed_in_current_program_requirements",
        "application_fee_usd": 120,
        "application_fee_scope": "most USC graduate programs beginning after fall 2026; verify in application",
        "application_fee_waiver_possible": True,
        "application_fee_waiver_requires_documented_eligibility": True,
        "gre": {
            "policy": "not_required_but_encouraged",
            "cycle": 2027,
            "test_type": "GRE General",
            "minimum_scores": {},
            "recommended_scores": {},
            "validity_rule": None,
            "waiver_rules": [],
            "source_ids": [PROGRAM],
        },
        "official_source_conflicts": [
            bi(
                "The current 2027 program page requires two recommendations and says GRE is not required but encouraged. An older department-format admission page still says three recommendations and required GRE. The cycle-specific program page controls this record.",
                "Güncel 2027 program sayfası iki referans ister ve GRE'nin zorunlu olmadığını ancak teşvik edildiğini söyler. Eski biçimli bölüm kabul sayfası hâlâ üç referans ve zorunlu GRE yazar. Bu kayıtta döneme özgü program sayfası esas alınır.",
            )
        ],
        "verification_notes": bi(
            "Candidates from all countries are encouraged to apply, and the on-campus degree is STEM OPT eligible. This does not guarantee visa issuance, scholarship funding, research access or eligibility for export-controlled employment.",
            "Tüm ülkelerden adayların başvurması teşvik edilir ve kampüsteki derece STEM OPT için uygundur. Bu; vize, burs, araştırma erişimi veya ihracat kontrollü işlere uygunluk garantisi değildir.",
        ),
    }

    row["language_profile"] = {
        "teaching_language": ["Unknown"],
        "teaching_languages": ["Unknown"],
        "english_required": True,
        "requirement_scope": "international applicants according to USC country requirements; domestic applicants are exempt",
        "accepted_english_tests": [
            {
                "test": "TOEFL iBT",
                "score_purpose": "ISE placement exemption, not a university-wide admission minimum",
                "minimum_score_policy": {
                    "test_before_2026_01_21": {"overall": 90, "each_section": 20},
                    "test_on_or_after_2026_01_21": {"overall": 4.5, "each_section": 4},
                },
                "validity_years": 2,
            },
            {
                "test": "IELTS Academic",
                "score_purpose": "ISE placement exemption, not a university-wide admission minimum",
                "minimum_score": 6.5,
                "minimum_each_band": 6,
                "validity_years": 2,
            },
            {
                "test": "Cambridge C1 Advanced",
                "score_purpose": "ISE placement exemption, not a university-wide admission minimum",
                "minimum_score": 176,
                "minimum_each_skill": 169,
                "validity_years": 2,
            },
            {
                "test": "PTE Academic",
                "score_purpose": "ISE placement exemption, not a university-wide admission minimum",
                "minimum_score": 61,
                "minimum_each_band": 53,
                "validity_years": 2,
            },
        ],
        "university_wide_admission_minimum_published": False,
        "program_specific_higher_minimum_published_on_checked_page": False,
        "official_scores_required_for_complete_international_application": True,
        "ise_exam_may_be_required_after_admission": True,
        "exemptions": [
            bi("USC degree holder or current USC degree student", "USC derecesine sahip veya hâlen USC derece öğrencisi"),
            bi("A qualifying US or Anglophone-country bachelor's degree completed entirely in that country", "Tamamı nitelikli bir ABD veya Anglosfer ülkesinde tamamlanmış lisans derecesi"),
            bi("A completed graduate degree from a country where English is both the language of instruction and the only official language", "İngilizcenin hem eğitim dili hem tek resmî dil olduğu bir ülkeden tamamlanmış lisansüstü derece"),
            bi("Native English language under USC's stated country rule", "USC'nin belirttiği ülke kuralı kapsamında ana dili İngilizce olma"),
        ],
        "medium_of_instruction_only_from_non_anglophone_country_waives_requirement": False,
        "language_risk": "medium",
        "verification_notes": bi(
            "USC's English evidence and placement rules are verified, but no checked official source explicitly labels the MS teaching language. It remains Unknown rather than inferred from the English-language site and tests.",
            "USC'nin İngilizce kanıtı ve yerleştirme kuralları doğrulandı; ancak kontrol edilen hiçbir resmî kaynak MS eğitim dilini açıkça etiketlemiyor. İngilizce web sitesi ve sınavlardan çıkarım yapmak yerine Unknown bırakılır.",
        ),
    }

    row["cost_profile"] = {
        "academic_year": "2026/2027",
        "currency": "USD",
        "cost_scope": "27-unit Viterbi MS current-rate four-semester example",
        "tuition_usd_per_unit": 2742,
        "total_program_units": 27,
        "tuition_usd_complete_27_units_at_2026_27_rate": 74034,
        "tuition_usd_first_year_example": 41130,
        "mandatory_fees_usd_first_year_example": 1899,
        "mandatory_fees_usd_complete_four_semester_example": 3743,
        "tuition_and_mandatory_fees_usd_complete_program_example": 77777,
        "first_year_tuition_and_mandatory_fees_usd_example": 43029,
        "academic_billed_baseline_usd_per_two_terms": 43029,
        "official_program_housing_estimate_usd_per_month": 1300,
        "official_program_housing_estimate_usd_first_academic_year": 15600,
        "official_program_housing_estimate_usd_complete_four_semester_example": 31200,
        "complete_program_estimate_excluding_health_insurance_usd": 108977,
        "health_insurance_required": True,
        "health_insurance_waiver_possible_with_qualifying_plan": True,
        "health_insurance_current_2026_27_premium_usd": None,
        "health_insurance_sample_2025_26_usd_per_year": 3522,
        "health_insurance_sample_four_semester_addition_usd": 7044,
        "complete_program_estimate_with_old_health_sample_usd": 116021,
        "first_year_example_with_housing_and_old_health_sample_usd": 62151,
        "i20_2026_tuition_and_fees_requirement_usd": 56049,
        "i20_2026_living_expenses_requirement_usd": 28044,
        "i20_2026_total_requirement_usd": 84093,
        "i20_amount_is_bill": False,
        "tuition_basis": "official Viterbi 2026-27 per-unit rate and 27-unit four-semester sample",
        "tuition_eur_per_year_min": None,
        "tuition_eur_per_year_max": None,
        "tuition_eur_per_year_estimated": None,
        "total_first_year_cost_eur": None,
        "scholarship_availability": "competitive_partial",
        "scholarship_risk": "very_high",
        "verification_notes": bi(
            "The $77,777 tuition-and-fee and $108,977 tuition/fee/housing totals are USC's four-semester examples using the 2026-27 rate; future tuition is adjusted annually. The $116,021 figure only adds USC's older 2025-26 insurance sample and is not a fixed bill. The separate $84,093 I-20 amount is an immigration funding requirement, not the degree bill.",
            "77.777 $ öğrenim/harç ve 108.977 $ öğrenim/harç/konut toplamları, 2026-27 oranını kullanan USC dört dönem örnekleridir; sonraki yıl ücretleri yıllık güncellenir. 116.021 $ tutarı yalnızca USC'nin eski 2025-26 sigorta örneğini ekler ve sabit fatura değildir. Ayrı 84.093 $ I-20 tutarı, derece faturası değil göçmenlik finansman şartıdır.",
        ),
    }

    row["scholarship_profile"] = {
        "available_types": ["viterbi_deans_scholarship", "external_funding", "private_funding"],
        "non_eu_eligible": True,
        "application_mode": "automatic",
        "application_mode_detail": "admission_application_by_scholarship_deadline",
        "automatic_consideration": True,
        "separate_application_required": False,
        "scholarship_decision_separate_from_admission_decision": True,
        "deans_scholarship_award_usd_min": 10000,
        "deans_scholarship_award_usd_max": 30000,
        "deans_scholarship_full_time_on_campus_required": True,
        "fall_scholarship_deadline": "December 15",
        "spring_safe_scholarship_deadline": "September 1",
        "spring_deadline_source_conflict": bi(
            "The dedicated scholarship page says September 1 for spring, while Viterbi's general application/FAQ material uses September 15. Use the earlier September 1 date for a funding-dependent application.",
            "Özel burs sayfası bahar için 1 Eylül derken Viterbi genel başvuru/SSS materyali 15 Eylül kullanır. Finansmana bağlı başvuruda daha erken olan 1 Eylül tarihini kullanın.",
        ),
        "masters_research_assistantships_available": False,
        "masters_teaching_assistantships_available": False,
        "ra_ta_reserved_for_phd": True,
        "funding_guaranteed": False,
        "full_tuition_award_guaranteed": False,
        "funding_notes": bi(
            "Viterbi Dean's Scholarships are competitive $10,000-$30,000 awards open to international and US full-time on-campus master's students; consideration uses the admission application submitted by the scholarship deadline. MS RA/TA positions are unavailable.",
            "Viterbi Dean's Scholarships, uluslararası ve ABD'li tam zamanlı kampüs MS öğrencilerine açık rekabetçi 10.000-30.000 $ ödüllerdir; değerlendirme burs tarihine kadar gönderilen kabul başvurusunu kullanır. MS RA/TA pozisyonları mevcut değildir.",
        ),
        "opportunities": [
            {
                "name": "Viterbi Dean's Scholarship",
                "amount_usd_min": 10000,
                "amount_usd_max": 30000,
                "international_eligible": True,
                "separate_application": False,
                "decision_separate_from_admission": True,
            }
        ],
        "verification_notes": bi(
            "The verified standard MS route is a competitive partial merit scholarship through the timely admission application. USC Viterbi explicitly states that RA/TA positions are reserved for PhD students and unavailable to master's students; self-funding must therefore be the default plan unless a written award is received.",
            "Doğrulanan standart MS yolu, zamanında kabul başvurusu üzerinden rekabetçi kısmi başarı bursudur. USC Viterbi RA/TA pozisyonlarının doktora öğrencilerine ayrıldığını ve yüksek lisans öğrencilerine açık olmadığını açıkça belirtir; yazılı ödül alınmadıkça varsayılan plan öz-finansman olmalıdır.",
        ),
    }

    row["living_profile"] = {
        "city_type": "Metropolis",
        "housing_search_difficulty": "high",
        "living_cost_risk": "very_high",
        "living_risk": "high",
        "student_housing_available": True,
        "graduate_and_family_housing_capacity_approximate_spaces": 2000,
        "graduate_and_family_housing_community_count": 24,
        "housing_access": "not_guaranteed",
        "housing_application_separate": True,
        "housing_application_after_admission_and_usc_id": True,
        "housing_application_before_enrollment_deposit_allowed": True,
        "housing_application_fee_usd": 65,
        "housing_application_fee_refundable": False,
        "housing_application_fee_waiver_available": False,
        "fall_2026_new_student_application_opened": "2026-02-02",
        "graduate_academic_year_contract": "2026-08-10 to 2027-05-12",
        "graduate_full_year_contract": "2026-08-10 to 2027-07-31",
        "monthly_housing_rent_usd_per_month_min": 1110,
        "monthly_housing_rent_usd_per_month_max": 2000,
        "rent_range_scope": "selected official 2026-27 USC graduate examples, not the full inventory or private market",
        "official_housing_examples": [
            {"property": "Troy East", "room_type": "two-bedroom, four-person", "usd_per_person_per_month": 1110},
            {"property": "Troy East", "room_type": "one-bedroom, two-person", "usd_per_person_per_month": 1200},
            {"property": "Stardust", "room_type": "studio, one-person", "usd_per_person_per_month": 1675},
            {"property": "Stardust", "room_type": "two-bedroom, two-person", "usd_per_person_per_month": 1730},
            {"property": "Windsor", "room_type": "one-bedroom, one-person", "usd_per_person_per_month": 2000},
        ],
        "official_program_housing_budget_usd_per_month": 1300,
        "private_market_rent_usd_per_month": None,
        "verification_notes": bi(
            "USC has a separate graduate housing process and about 2,000 graduate/family spaces, but no checked source guarantees an individual assignment. Apply immediately after admission and maintain an off-campus backup. The displayed $1,110-$2,000 range consists only of named USC units.",
            "USC'nin ayrı bir lisansüstü konut süreci ve yaklaşık 2.000 lisansüstü/aile yeri vardır; ancak kontrol edilen hiçbir kaynak bireysel yer garantisi vermez. Kabulden hemen sonra başvurun ve kampüs dışı yedek plan tutun. Gösterilen 1.110-2.000 $ aralığı yalnızca adı verilen USC birimlerinden oluşur.",
        ),
    }

    row["curriculum_profile"] = {
        "credit_hours_total": 27,
        "typical_three_unit_course_equivalent": 9,
        "minimum_500_or_600_level_units": 21,
        "structure": bi(
            "12 units of core courses, 9 units of core electives and 6 units of technical electives.",
            "12 birim çekirdek ders, 9 birim çekirdek seçmeli ve 6 birim teknik seçmeli.",
        ),
        "core_units": 12,
        "core_elective_units": 9,
        "technical_elective_units": 6,
        "core_courses": [
            "ASTE 470/575 Spacecraft Propulsion",
            "ASTE 520 Spacecraft System Design",
            "ASTE 535 Spacecraft Environments and Spacecraft Interaction",
            "ASTE 580 Orbital Mechanics I",
        ],
        "core_elective_course_count": 3,
        "technical_elective_course_count": 2,
        "specializations": [
            "spacecraft_propulsion",
            "spacecraft_dynamics",
            "space_system_design",
            "spacecraft_systems_and_operations",
            "space_applications",
            "safety_of_space_systems",
        ],
        "thesis_required": False,
        "thesis_option_available_by_request": True,
        "thesis_option_request_timing": "after completing the first semester",
        "thesis_option_guaranteed": False,
        "directed_research_without_thesis_available_by_request": True,
        "mandatory_internship": False,
        "capstone_required": None,
        "typical_duration_semesters": 4,
        "typical_duration_is_binding": False,
        "flexibility": "high",
        "curriculum_risk": "medium",
        "verification_notes": bi(
            "This record is the 27-unit MS, not the separate graduate certificate or the broader MS Aerospace Engineering. Nine three-unit courses is the direct course equivalent. Thesis and directed research may be requested only after the first semester, and the thesis route is not guaranteed.",
            "Bu kayıt, ayrı lisansüstü sertifika veya daha geniş MS Aerospace Engineering değil, 27 birimlik MS'tir. Dokuz adet üç birimlik ders doğrudan ders karşılığıdır. Tez ve yönlendirilmiş araştırma yalnızca ilk dönemden sonra talep edilebilir; tez yolu garanti değildir.",
        ),
    }

    row["category_profile"] = {
        "primary_categories": ["space_systems", "astrodynamics", "gnc"],
        "secondary_categories": [
            "satellite_systems",
            "space_propulsion",
            "aerospace_structures",
            "space_environment",
            "sensors",
            "autonomy",
            "aerospace_general",
        ],
        "subcategories": [
            "spacecraft_design",
            "orbital_mechanics",
            "space_navigation",
            "attitude_dynamics_and_control",
            "human_spaceflight",
            "remote_sensing",
            "space_safety",
            "entry_and_landing",
        ],
        "technical_focus": bi(
            "Dedicated spacecraft engineering across propulsion, orbital mechanics, navigation/control, systems design, operations, structures, thermal, sensors and space environment.",
            "İtki, yörünge mekaniği, seyrüsefer/kontrol, sistem tasarımı, operasyon, yapılar, ısıl, sensörler ve uzay ortamını kapsayan özel uzay aracı mühendisliği.",
        ),
        "verification_notes": bi(
            "Tags are derived from the published course blocks and concentrations, not from institutional prestige or the program title alone.",
            "Etiketler kurum prestijinden veya yalnızca program adından değil, yayımlanmış ders blokları ve yoğunlaşmalardan türetilmiştir.",
        ),
    }

    row["research_profile"] = {
        "research_focus_areas": [
            bi("Human performance and human-AI interaction in deep-space habitats", "Derin uzay habitatlarında insan performansı ve insan-YZ etkileşimi"),
            bi("Space plasma physics, space weather, electric propulsion and atmospheric re-entry", "Uzay plazma fiziği, uzay havası, elektrikli itki ve atmosferik yeniden giriş"),
            bi("Spacecraft and satellite build, test and flight demonstrations", "Uzay aracı ve uydu yapım, test ve uçuş gösterimleri"),
            bi("Autonomous robotics for extreme and unstructured environments", "Aşırı ve yapılandırılmamış ortamlar için otonom robotik"),
            bi("Space science, technology and applications", "Uzay bilimi, teknolojisi ve uygulamaları"),
        ],
        "key_institutes": [
            "Astronaut Performance Lab (APL)",
            "Laboratory for Exploration and Astronautical Physics (LEAP)",
            "Space Engineering Research Center (SERC)",
            "Laboratory for Autonomous Systems in Exploration and Robotics (LASER)",
        ],
        "named_facilities": [
            "Space Engineering Research Center spacecraft and satellite build/test facilities",
            "Rocket Propulsion Laboratory",
            "Liquid Propulsion Laboratory",
            "LEAP vacuum chambers",
        ],
        "hands_on_build_test_flight_evidence": True,
        "masters_thesis_access": "request_after_first_semester_not_guaranteed",
        "individual_lab_place_guaranteed": False,
        "research_access_note": bi(
            "The department documents hands-on opportunities and several active research groups, but an admitted MS student is not promised a thesis, funded position or place in a particular lab. Access depends on faculty approval, project needs, skills, capacity and any compliance controls.",
            "Bölüm uygulamalı fırsatları ve çeşitli aktif araştırma gruplarını belgeler; ancak kabul edilen bir MS öğrencisine tez, fonlu pozisyon veya belirli laboratuvarda yer sözü verilmez. Erişim öğretim üyesi onayı, proje ihtiyacı, beceri, kapasite ve uyum kontrollerine bağlıdır.",
        ),
        "research_risk": "medium",
        "verification_notes": bi(
            "USC has a rare independent Astronautical Engineering department and directly named space laboratories. This is strong research infrastructure evidence, not guaranteed individual access.",
            "USC nadir bulunan bağımsız bir Astronautical Engineering bölümüne ve doğrudan adlandırılmış uzay laboratuvarlarına sahiptir. Bu güçlü araştırma altyapısı kanıtıdır; bireysel erişim garantisi değildir.",
        ),
    }

    row["industry_ecosystem_profile"] = {
        "local_industry_strength": None,
        "verified_partnerships": [],
        "industry_experienced_adjunct_teaching": True,
        "official_2025_top_employers_from_voluntary_survey": [
            "The Aerospace Corporation",
            "Blue Origin",
            "The Boeing Company",
            "Lockheed Martin",
            "Northrop Grumman Corporation",
        ],
        "official_2025_average_reported_salary_usd": 119513,
        "outcomes_sample_is_comprehensive": False,
        "outcomes_are_partnership_evidence": False,
        "international_access_risk": "high",
        "export_control_context": bi(
            "USC states that the vast majority of its research is fundamental research and not subject to export-control licensing. Restricted projects can nevertheless limit student or foreign-national participation and require compliance review.",
            "USC, araştırmalarının büyük çoğunluğunun temel araştırma olduğunu ve ihracat kontrolü lisansına tabi olmadığını belirtir. Bununla birlikte kısıtlı projeler öğrenci veya yabancı uyruklu katılımını sınırlayabilir ve uyum incelemesi gerektirebilir.",
        ),
        "verification_notes": bi(
            "The current program page verifies industry-specialist adjunct teaching and reports 2025 employers through a voluntary destination survey. Employer names and salary are outcome signals only; they are not converted into partnerships, placement guarantees or international eligibility claims.",
            "Güncel program sayfası sektör uzmanı ek öğretim üyelerini doğrular ve 2025 işverenlerini gönüllü varış anketiyle bildirir. İşveren adları ve maaş yalnızca sonuç sinyalidir; ortaklık, işe yerleşme garantisi veya uluslararası uygunluk iddiasına dönüştürülmez.",
        ),
    }

    row["application_timeline_profile"] = {
        "application_period": "Fall and Spring",
        "non_eu_deadline": bi(
            "2027-02-15 (Fall 2027, current program page; official Viterbi general pages conflict)",
            "2027-02-15 (Güz 2027, güncel program sayfası; resmî Viterbi genel sayfaları çelişiyor)",
        ),
        "scholarship_deadline": bi(
            "2026-12-15 (Fall 2027); use 2026-09-01 as the safest Spring 2027 funding date",
            "2026-12-15 (Güz 2027); Bahar 2027 finansmanı için en güvenli tarih olarak 2026-09-01'i kullanın",
        ),
        "deadline_notes": bi(
            "Current official USC pages conflict on the later fall deadline and the spring scholarship date. Funding-dependent applicants should use the earlier applicable date and recheck the live portal.",
            "Güncel resmî USC sayfaları daha sonraki güz tarihi ve bahar burs tarihinde çelişir. Finansmana bağlı adaylar daha erken uygulanabilir tarihi kullanmalı ve canlı portalı yeniden kontrol etmelidir.",
        ),
        "application_rounds": [
            {
                "intake": "Fall 2027 scholarship consideration",
                "round": bi("Fall 2027 scholarship consideration", "Güz 2027 burs değerlendirmesi"),
                "deadline": "2026-12-15",
                "deadline_time": "23:59 Pacific Time",
                "scholarship_consideration": True,
            },
            {
                "intake": "Fall 2027 final - program page",
                "round": bi("Fall 2027 final - program page", "Güz 2027 nihai - program sayfası"),
                "deadline": "2027-02-15",
                "scholarship_consideration": False,
            },
            {
                "intake": "Spring 2027 admission",
                "round": bi("Spring 2027 admission", "Bahar 2027 kabulü"),
                "deadline": "2026-09-15",
                "scholarship_consideration": "official scholarship pages conflict; use September 1 if funding-dependent",
            },
        ],
        "deadline_source_conflict": bi(
            "The current program page lists February 15 as the fall final deadline, while Viterbi's general application page and FAQ list January 15. This record preserves the program-specific February 15 date and flags the inconsistency; funding applicants must use December 15 regardless.",
            "Güncel program sayfası güz nihai son tarihi olarak 15 Şubat'ı, Viterbi genel başvuru sayfası ve SSS ise 15 Ocak'ı listeler. Bu kayıt programa özgü 15 Şubat tarihini korur ve tutarsızlığı işaretler; burs adayları her durumda 15 Aralık'ı kullanmalıdır.",
        ),
        "all_required_materials_due_by_deadline": True,
        "decision_timing": bi(
            "USC says most fall applicants receive a decision by June and most spring applicants by December; the program does not promise an individual decision date.",
            "USC, güz adaylarının çoğunun Haziran'a, bahar adaylarının çoğunun Aralık'a kadar karar aldığını söyler; program bireysel karar tarihi vaat etmez.",
        ),
        "pre_enrollment_required": True,
        "post_admission_steps": [
            bi("Submit the Intent to Enroll before course registration", "Ders kaydından önce Intent to Enroll formunu gönderin"),
            bi("Provide first-year financial documentation for I-20/DS-2019 processing", "I-20/DS-2019 işlemi için ilk yıl finansal belgelerini sunun"),
            bi("Complete Immigration Status Verification within 15 days of arrival and before registration", "Varıştan sonraki 15 gün içinde ve ders kaydından önce Immigration Status Verification işlemini tamamlayın"),
            bi("Take the ISE examination if the admission letter requires it", "Kabul mektubu gerektiriyorsa ISE sınavına girin"),
        ],
        "visa_complexity": "high",
        "timeline_risk": "high",
        "verification_notes": bi(
            "Apply by December 15 for fall scholarship consideration. Because USC's official pages conflict on later fall and spring-funding dates, a risk-averse applicant should use the earlier applicable date and verify the live application portal before submission.",
            "Güz burs değerlendirmesi için 15 Aralık'a kadar başvurun. USC'nin resmî sayfaları daha sonraki güz ve bahar finansman tarihlerinde çeliştiği için riskten kaçınan aday daha erken uygulanabilir tarihi kullanmalı ve göndermeden önce canlı başvuru portalını doğrulamalıdır.",
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
            "Recent USC graduate-housing threads repeatedly describe limited availability, difficult trade-offs among price, privacy, distance and safety, and frequent reliance on off-campus housing. The comments are not program-specific enough to rate teaching, workload or career support.",
            "Yakın tarihli USC lisansüstü konut başlıkları sınırlı yer, fiyat-mahremiyet-mesafe-güvenlik arasında zor tercihler ve kampüs dışı konuta sık başvuru sinyali verir. Yorumlar öğretim, iş yükü veya kariyer desteğini puanlayacak kadar programa özgü değildir.",
        ),
        "student_sentiment_sources": [
            {"url": REDDIT_HOUSING_1, "topic": "graduate housing availability"},
            {"url": REDDIT_HOUSING_2, "topic": "graduate housing cost and search"},
            {"url": REDDIT_HOUSING_3, "topic": "distance, safety and housing options"},
            {"url": REDDIT_HOUSING_4, "topic": "graduate housing experiences"},
        ],
        "approximate_comment_sample_size": 12,
        "sentiment_date_range": "2025-01 to 2026-03",
        "sentiment_confidence": "low",
        "verification_notes": bi(
            "No satisfaction score is calculated. Commercial sublet advertisements and isolated anecdotes were not treated as factual rent or safety evidence; only the repeated housing-search difficulty signal is retained.",
            "Memnuniyet puanı hesaplanmadı. Ticari alt-kiralama ilanları ve tekil anekdotlar kira veya güvenlik gerçeği sayılmadı; yalnızca tekrarlanan konut arama zorluğu sinyali korundu.",
        ),
    }

    sources = [
        source(PROGRAM, "USC Viterbi MS in Astronautical Engineering", "official_program_page", ["program", "curriculum", "admission", "deadline", "non_eu_eligibility", "industry_outcomes"], "Current 2027 application criteria, curriculum, deadlines, STEM OPT status and voluntary career outcomes.", "Güncel 2027 başvuru ölçütleri, müfredat, son tarihler, STEM OPT durumu ve gönüllü kariyer sonuçları."),
        source(DEPARTMENT_MS, "USC Astronautical Engineering MS Program", "official_program_page", ["program", "curriculum", "deficiency_courses"], "Department overview and 27-unit/upper-level requirements; cycle-specific admission claims are secondary to the current program page.", "Bölüm özeti ve 27 birim/üst düzey şartlar; döneme özgü kabul iddialarında güncel program sayfası önceliklidir.", confidence="medium"),
        source(DEPARTMENT_ADMISSION, "USC Astronautics Graduate Admission", "official_admission_page", ["admission", "gpa", "source_conflict"], "Official department page supplies the 3.0 GPA statement but conflicts with the current 2027 program page on GRE, letters and deadlines.", "Resmî bölüm sayfası 3,0 GPA bilgisini verir; ancak GRE, referans ve tarihlerde güncel 2027 program sayfasıyla çelişir.", confidence="medium"),
        source(VITERBI_APPLY, "USC Viterbi How to Apply - Master's", "official_admission_page", ["deadline", "application_materials", "decision"], "Viterbi application workflow, complete-material deadline rule and decision process.", "Viterbi başvuru akışı, tüm belgelerin son tarihe yetişmesi kuralı ve karar süreci."),
        source(INTERNATIONAL_APPLY, "USC How to Apply as an International Student", "official_admission_page", ["non_eu_eligibility", "application_fee", "documents", "visa"], "International application steps, application fee and waiver mechanism.", "Uluslararası başvuru adımları, başvuru ücreti ve muafiyet mekanizması."),
        source(ENGLISH, "USC Graduate English Proficiency", "official_admission_page", ["english_proficiency", "tests", "waivers"], "Current accepted tests, two-year validity, placement thresholds and narrowly defined waivers.", "Güncel kabul edilen sınavlar, iki yıllık geçerlilik, yerleştirme eşikleri ve dar tanımlı muafiyetler."),
        source(COUNTRY, "USC Graduate Country Requirements", "official_admission_page", ["non_eu_eligibility", "country_documents", "english_proficiency"], "Confirms candidates from all countries may apply and country-specific academic/English records apply.", "Tüm ülkelerden adayların başvurabileceğini ve ülkeye özgü akademik/İngilizce belgelerin geçerli olduğunu doğrular."),
        source(NEXT_STEPS, "USC International Student Next Steps", "official_visa_or_government_page", ["pre_enrollment", "visa", "ise"], "Intent to Enroll, immigration verification and possible ISE steps after admission.", "Kabul sonrası Intent to Enroll, göçmenlik doğrulaması ve olası ISE adımları."),
        source(FINANCIAL_DOCS, "USC Graduate Financial Documentation Requirements", "official_visa_or_government_page", ["visa_financial_requirement", "tuition", "living_cost"], "2026 Viterbi I-20 funding requirement, explicitly not a bill.", "2026 Viterbi I-20 finansman şartı; açıkça fatura değildir."),
        source(TUITION, "USC Viterbi Master's Tuition and Fees", "official_tuition_page", ["tuition", "mandatory_fees", "insurance"], "2026-27 per-unit tuition and mandatory fee schedule.", "2026-27 birim başına öğrenim ücreti ve zorunlu harç çizelgesi."),
        source(COA_PDF, "USC Viterbi 2026-27 Tuition and Fees for 27-Unit MS Programs", "official_tuition_page", ["duration", "tuition", "fees", "housing", "insurance", "complete_program_cost"], "Three-page official four-semester cost example for 27-unit programs.", "27 birimlik programlar için üç sayfalık resmî dört dönem maliyet örneği.", access_status="pdf"),
        source(SCHOLARSHIPS, "USC Viterbi Master's Scholarships", "official_scholarship_page", ["scholarship", "non_eu_eligibility", "scholarship_deadline"], "Dean's Scholarship amount, international eligibility and admission-application consideration route.", "Dean's Scholarship tutarı, uluslararası uygunluk ve kabul başvurusu üzerinden değerlendirme yolu."),
        source(FAQ, "USC Viterbi Master's Applicant FAQ", "official_admission_page", ["admission", "gre", "scholarship", "assistantships", "english_proficiency", "deadline"], "Current 2027 GRE guidance and explicit statement that MS RA/TA roles are unavailable and reserved for PhD students.", "Güncel 2027 GRE rehberi ve MS RA/TA rollerinin açık olmadığı, doktora öğrencilerine ayrıldığına ilişkin açık beyan."),
        source(HEALTH, "USC Student Health Fees and Deadlines", "official_university_policy_page", ["insurance", "waiver"], "Confirms automatic SHIP enrolment for full-time/international students and annual waiver deadlines; current premium is not exposed in indexed text.", "Tam zamanlı/uluslararası öğrenciler için otomatik SHIP kaydını ve yıllık muafiyet tarihlerini doğrular; güncel prim dizinli metinde görünmez.", confidence="medium"),
        source(HOUSING_APPLICATION, "USC Housing Application", "official_housing_page", ["housing", "application_fee", "contract_dates"], "Separate post-admission graduate application, $65 non-waivable fee and 2026-27 contract terms.", "Kabul sonrası ayrı lisansüstü başvurusu, muafiyetsiz 65 $ ücret ve 2026-27 sözleşme dönemleri."),
        source(GRAD_HOUSING, "USC Graduate and Family Housing", "official_housing_page", ["housing_capacity", "housing_types"], "Approximately 2,000 spaces across 24 graduate/family communities.", "24 lisansüstü/aile topluluğunda yaklaşık 2.000 yer."),
        source(TROY_EAST, "USC Housing - Troy East", "official_housing_page", ["housing", "housing_rate"], "Named 2026-27 shared graduate housing examples at $1,110-$1,200 per person per month.", "Kişi başı aylık 1.110-1.200 $ olan adlandırılmış 2026-27 paylaşımlı lisansüstü konut örnekleri."),
        source(WINDSOR, "USC Housing - Windsor", "official_housing_page", ["housing", "housing_rate"], "Named 2026-27 single-occupancy one-bedroom example at $2,000 per month.", "Aylık 2.000 $ olan adlandırılmış 2026-27 tek kişilik bir yatak odalı örnek."),
        source(STARDUST, "USC Housing - Stardust", "official_housing_page", ["housing", "housing_rate"], "Named 2026-27 graduate studio and apartment examples.", "Adlandırılmış 2026-27 lisansüstü stüdyo ve daire örnekleri."),
        source(RESEARCH, "USC Astronautical Engineering Research", "official_lab_page", ["research", "labs", "focus_areas"], "Current department research groups including APL, LEAP, SERC and LASER.", "APL, LEAP, SERC ve LASER dâhil güncel bölüm araştırma grupları."),
        source(ABOUT, "USC Astronautical Engineering About", "official_department_page", ["department", "facilities", "hands_on_research"], "Independent department status and hands-on SERC, Rocket Propulsion and Liquid Propulsion opportunities.", "Bağımsız bölüm statüsü ve uygulamalı SERC, Rocket Propulsion ve Liquid Propulsion fırsatları."),
        source(STUDENT_ORGS, "USC Astronautics Student Organizations", "official_department_page", ["hands_on_projects", "rocket_propulsion"], "Rocket and liquid propulsion student project context; not treated as guaranteed curricular access.", "Roket ve sıvı itki öğrenci projesi bağlamı; garantili müfredat erişimi sayılmaz."),
        source(EXPORT, "USC Export Controls", "official_university_policy_page", ["international_research_access", "export_control"], "Current USC fundamental-research policy and restricted-project participation risks.", "Güncel USC temel araştırma politikası ve kısıtlı proje katılım riskleri."),
        source(QS, "QS - University of Southern California", "ranking_provider", ["prestige"], "QS World University Ranking 2027: #153; context only.", "QS Dünya Üniversite Sıralaması 2027: #153; yalnızca bağlam.", confidence="medium"),
        source(REDDIT_HOUSING_1, "Reddit r/USC - On campus grad housing", "student_forum", ["housing_sentiment"], "Recent anecdotal graduate housing availability discussion; perception only.", "Yakın tarihli anekdotal lisansüstü konut uygunluğu tartışması; yalnızca algı.", confidence="low"),
        source(REDDIT_HOUSING_2, "Reddit r/USC - Looking for graduate housing", "student_forum", ["housing_sentiment"], "Recent anecdotal housing search and affordability discussion; advertisements excluded from facts.", "Yakın tarihli anekdotal konut arama ve karşılanabilirlik tartışması; ilanlar gerçeklerden hariç tutuldu.", confidence="low"),
        source(REDDIT_HOUSING_3, "Reddit r/USC - Graduate housing options", "student_forum", ["housing_sentiment"], "Anecdotal distance, safety and availability concerns; perception only.", "Anekdotal mesafe, güvenlik ve yer kaygıları; yalnızca algı.", confidence="low"),
        source(REDDIT_HOUSING_4, "Reddit r/USC - Graduate housing", "student_forum", ["housing_sentiment"], "Recent mixed individual graduate housing experiences; perception only.", "Yakın tarihli karışık bireysel lisansüstü konut deneyimleri; yalnızca algı.", confidence="low"),
    ]

    row["source_profile"] = {
        "primary_url": PROGRAM,
        "secondary_urls": [item["url"] for item in sources[1:]],
        "last_verified": TODAY,
        "field_confidence": {
            "program_basic_info": "high",
            "program": "high",
            "duration": "high",
            "language": "unknown",
            "english_proficiency": "high",
            "admission": "high",
            "gpa": "medium",
            "non_eu_eligibility": "high",
            "tuition": "high",
            "scholarship": "high",
            "deadline": "medium",
            "curriculum": "high",
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
            "All discoverable core decision fields except explicit teaching language are sourced. Official conflicts are preserved instead of silently choosing a favorable deadline or test policy. Private-market rent, admission rate, current 2026-27 SHIP premium, guaranteed lab access and guaranteed funding are not invented.",
            "Açık eğitim dili dışındaki bulunabilir tüm temel karar alanları kaynaklıdır. Resmî çelişkiler, elverişli bir tarih veya sınav politikası sessizce seçilmek yerine korunur. Özel piyasa kirası, kabul oranı, güncel 2026-27 SHIP primi, garantili laboratuvar erişimi ve garantili finansman uydurulmaz.",
        ),
        "source_log": sources,
    }

    row["decision_summary"] = {
        "best_for": [
            bi("Students seeking a rare, dedicated spacecraft-engineering MS rather than a broad aircraft-centered aerospace degree.", "Geniş ve uçak merkezli aerospace derecesi yerine nadir bulunan özel uzay aracı mühendisliği MS'i arayan öğrenciler."),
            bi("Applicants targeting space systems, propulsion, orbital mechanics, GNC, operations, space environment or spacecraft hardware.", "Uzay sistemleri, itki, yörünge mekaniği, GNC, operasyon, uzay ortamı veya uzay aracı donanımını hedefleyen adaylar."),
        ],
        "not_ideal_for": [
            bi("Applicants who need a standard RA/TA-funded master's offer.", "Standart RA/TA finansmanlı yüksek lisans teklifine ihtiyaç duyan adaylar."),
            bi("International applicants whose career plan depends exclusively on export-controlled US defence or space roles.", "Kariyer planı yalnızca ihracat kontrollü ABD savunma veya uzay rollerine bağlı uluslararası adaylar."),
        ],
        "main_strengths": [
            bi("A dedicated independent Astronautical Engineering department with a directly spacecraft-centered nine-course curriculum.", "Doğrudan uzay aracı merkezli dokuz derslik müfredata sahip bağımsız Astronautical Engineering bölümü."),
            bi("Strong breadth from propulsion and orbital mechanics to thermal, structures, sensors, navigation, autonomy and mission safety.", "İtki ve yörünge mekaniğinden ısıl, yapılar, sensörler, seyrüsefer, otonomi ve görev güvenliğine uzanan güçlü genişlik."),
            bi("Named hands-on spacecraft, satellite, plasma, autonomy and propulsion facilities and groups.", "Adlandırılmış uygulamalı uzay aracı, uydu, plazma, otonomi ve itki tesisleri ve grupları."),
        ],
        "main_risks": [
            bi("USC's current example is $77,777 in tuition/fees and $108,977 with estimated housing before health insurance.", "USC'nin güncel örneği öğrenim/harçta 77.777 $, tahmini konutla ve sağlık sigortası hariç 108.977 $'dır."),
            bi("MS RA/TA positions are explicitly unavailable; merit scholarships are competitive and partial.", "MS RA/TA pozisyonları açıkça mevcut değildir; başarı bursları rekabetçi ve kısmidir."),
            bi("Graduate housing requires a separate paid application and is not guaranteed.", "Lisansüstü konut ayrı ücretli başvuru gerektirir ve garanti değildir."),
            bi("Official pages conflict on GRE history, recommendation count and later deadlines; use the current cycle-specific page and earlier funding dates.", "Resmî sayfalar GRE geçmişi, referans sayısı ve sonraki tarihlerde çelişir; güncel döneme özgü sayfayı ve daha erken finansman tarihlerini kullanın."),
            bi("Teaching language is not explicitly stated on a checked official page.", "Eğitim dili kontrol edilmiş resmî bir sayfada açıkça belirtilmez."),
        ],
        "decision_summary": bi(
            "USC is one of the clearest US technical matches for a student who wants spacecraft engineering rather than generic aerospace: the curriculum is unusually direct and the department has credible hands-on space infrastructure. The financial model is the decisive weakness. Treat admission and scholarship as separate outcomes, plan for self-funding, apply by December 15 for fall aid, and do not assume an RA/TA or university housing place.",
            "USC, genel aerospace yerine uzay aracı mühendisliği isteyen öğrenci için ABD'deki en açık teknik eşleşmelerden biridir: müfredat olağanüstü doğrudandır ve bölüm güvenilir uygulamalı uzay altyapısına sahiptir. Belirleyici zayıflık finansal modeldir. Kabul ve bursu ayrı sonuçlar olarak görün, öz-finansman planlayın, güz yardımı için 15 Aralık'a kadar başvurun ve RA/TA veya üniversite konutunu varsaymayın.",
        ),
        "pros": [],
        "cons": [],
        "verdict": bi(
            "Exceptional dedicated astronautics fit, but financially safe only with a credible self-funding plan or a written scholarship.",
            "Olağanüstü özel astronotik uyumu; ancak yalnızca güvenilir öz-finansman planı veya yazılı bursla finansal olarak güvenli.",
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
            "high_complete_program_cost",
            "masters_ra_ta_unavailable",
            "scholarship_partial_not_guaranteed",
            "graduate_housing_not_guaranteed",
            "official_deadline_conflict",
            "export_control_access_project_specific",
        ],
    }

    row["data_quality"] = {
        "status": "partial",
        "checked_official_source_count": 23,
        "verified_fields": [
            "program",
            "duration",
            "admission",
            "non_eu_eligibility",
            "english_proficiency",
            "tuition",
            "complete_program_cost_example",
            "scholarship",
            "deadline",
            "curriculum",
            "research",
            "industry_outcomes",
            "housing",
            "living",
            "insurance_requirement",
            "prestige",
        ],
        "unverified_critical_fields": ["language"],
        "known_semantic_gaps": [
            "explicit_teaching_language",
            "private_market_rent",
            "admission_rate",
            "current_2026_27_ship_premium",
            "guaranteed_individual_lab_access",
            "guaranteed_ms_funding_package",
        ],
        "official_source_conflicts": ["gre_and_recommendation_history", "fall_final_deadline", "spring_scholarship_deadline"],
        "has_checked_source_log": True,
        "audited_at": TODAY,
    }

    row["quality_control"] = {
        "checked_at": TODAY,
        "qc_status": "needs_revision",
        "remaining_verification_tasks": [
            bi("Find a current official source explicitly stating the MS teaching language; do not infer it from English testing or the website language.", "MS eğitim dilini açıkça belirten güncel resmî kaynak bulun; İngilizce sınavından veya web sitesi dilinden çıkarım yapmayın."),
            bi("Recheck the live program and scholarship pages immediately before application because USC currently publishes conflicting later deadlines.", "USC şu anda çelişkili sonraki tarihler yayımladığı için başvurudan hemen önce canlı program ve burs sayfalarını yeniden kontrol edin."),
            bi("Replace the 2025-26 insurance sample when USC exposes a checked 2026-27 SHIP premium.", "USC kontrol edilebilir 2026-27 SHIP primini yayımladığında 2025-26 sigorta örneğini değiştirin."),
        ],
        "qc_notes": bi(
            "Every discoverable critical claim is source-backed and official conflicts are explicit. The record remains partial because teaching language is not explicitly verified; current insurance price and non-guaranteed outcomes are documented as semantic gaps rather than guessed.",
            "Bulunabilir her kritik iddia kaynaklıdır ve resmî çelişkiler açıktır. Eğitim dili açıkça doğrulanmadığı için kayıt partial kalır; güncel sigorta fiyatı ve garantisiz sonuçlar tahmin edilmek yerine anlamsal boşluk olarak belgelenir.",
        ),
        "failed_canary_tests": ["teaching_language_not_explicitly_verified"],
    }

    DATA_PATH.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    audit = {
        "record_id": row["id"],
        "checked_at": TODAY,
        "validation_method": "indexed web open/search validation; official 27-unit cost PDF opened and extracted",
        "audit_validity": "valid",
        "summary": {
            "total_urls": len(sources),
            "official_urls": 23,
            "reliable_third_party_urls": 1,
            "student_forum_urls": 4,
            "ok_or_indexed_html": sum(item["access_status"] == "ok" for item in sources),
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
            "All retained URLs returned accessible indexed content or an accessible PDF. The four Reddit sources are used only for conservative housing sentiment. Official page conflicts are retained in the record.",
            "Tutulan tüm URL'ler erişilebilir dizinli içerik veya erişilebilir PDF döndürdü. Dört Reddit kaynağı yalnızca ihtiyatlı konut algısı için kullanılır. Resmî sayfa çelişkileri kayıtta korunur.",
        ),
    }
    AUDIT_PATH.parent.mkdir(parents=True, exist_ok=True)
    AUDIT_PATH.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "id": row["id"],
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
