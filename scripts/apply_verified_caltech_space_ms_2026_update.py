from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data_base" / "amerika.json"
AUDIT_PATH = ROOT / "reports" / "source_link_audit_caltech_space_ms_2026-08-14.json"
TODAY = "2026-08-14"

PROGRAM = "https://aerospace.caltech.edu/academics/grad/grad_as"
CATALOG = "https://www.catalog.caltech.edu/current/information-for-graduate-students/special-regulations-for-graduate-options/aerospace-ae/"
AE105 = "https://catalog.caltech.edu/current/2025-26/ae-105-abc/"
SCHEDULE = "https://schedules.caltech.edu/FA2026-27.html"
DEPT_ADMISSION = "https://aerospace.caltech.edu/academics/admissions"
FAQ = "https://gradoffice.caltech.edu/admissions/faq-applicants"
APPLY = "https://gradoffice.caltech.edu/admissions/applyonline"
CHECKLIST = "https://gradoffice.caltech.edu/admissions/checklist"
TESTS = "https://gradoffice.caltech.edu/documents/32606/AppInstructions_Required_Tests_2025.pdf"
TRANSCRIPTS = "https://gradoffice.caltech.edu/documents/32516/AppInstructions_Transcripts_and_Recs.pdf"
BUDGET = "https://gradoffice.caltech.edu/financialsupport/budget"
NO_AID = "https://gradoffice.caltech.edu/financialsupport/nofinaid"
ADMITTED = "https://gradoffice.caltech.edu/admissions/frequently-asked-questions-for-admitted-students"
INCOMING = "https://gradoffice.caltech.edu/incoming"
HOUSING_NEW = "https://housing.caltech.edu/grads/newadmits/newstudent-housingoptions"
HOUSING_RATES = "https://housing.caltech.edu/grads/gradaute-housing-lottery-contract-rates"
HOUSING_LOTTERY = "https://housing.caltech.edu/grads/graduate-housing-lottery/lottery-process"
HOUSING_CONTRACT = "https://housing.caltech.edu/documents/34407/2026-2027_Graduate_Contract.pdf"
RESEARCH = "https://aerospace.caltech.edu/"
SPACE_TECH = "https://aerospace.caltech.edu/research/space-technology"
CENTERS = "https://aerospace.caltech.edu/research/centers"
FACILITIES = "https://aerospace.caltech.edu/research/facilities"
JPL = "https://www.catalog.caltech.edu/current/general-information/jet-propulsion-laboratory/"
ISP = "https://international.caltech.edu/about/isp"
ORIENTATION = "https://international.caltech.edu/Orientation"
EXPORT = "https://researchpolicy.caltech.edu/research-security/export-compliance/process"
QS = "https://www.topuniversities.com/universities/california-institute-technology-caltech"

REDDIT_TERMINAL_MS = "https://www.reddit.com/r/Caltech/comments/1acrlpr"
REDDIT_WORKLOAD = "https://www.reddit.com/r/Caltech/comments/caowbd"
REDDIT_HOUSING = "https://www.reddit.com/r/Caltech/comments/1rokv4m"


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
    confidence: str = "high",
    access_status: str = "ok",
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
    row = next(item for item in records if item.get("id") == "caltech-galcit")

    row.update({
        "country": "United States",
        "university": "California Institute of Technology",
        "university_native_name": "California Institute of Technology (Caltech)",
        "university_aliases": ["Caltech", "CIT"],
        "city": "Pasadena",
        "region": "California",
        "program_name": "Master of Science in Space Engineering",
        "program_native_name": "Master of Science in Space Engineering",
        "program_degree": "MS",
        "degree_level": "Master",
        "duration_years": 1,
        "duration": bi("One academic year; all degree courses must be completed within that year.", "Bir akademik yıl; derece derslerinin tamamı bu yıl içinde bitirilmelidir."),
        "ects": None,
        "caltech_units": 135,
        "teaching_language": ["English"],
        "program_url": PROGRAM,
        "program_status": "active",
        "relevance_status": "strong",
        "delivery_modes": ["on_campus"],
        "full_time_available": True,
        "part_time_available": False,
        "qs_ranking": 7,
        "qs_ranking_display": "#7",
        "qs_ranking_year": 2027,
    })

    row["prestige_profile"] = {
        "qs_world_rank": 7,
        "qs_edition": 2027,
        "qs_source_url": QS,
        "interpretation": bi(
            "The QS institutional rank is prestige context only. Technical fit is evidenced separately by the dedicated Space Engineering curriculum, active Ae 105 sequence, research themes, facilities and centres.",
            "QS kurum sırası yalnızca prestij bağlamıdır. Teknik uygunluk; özel Space Engineering müfredatı, aktif Ae 105 dizisi, araştırma temaları, tesisler ve merkezlerle ayrıca kanıtlanır.",
        ),
    }

    row["eligibility_profile"] = {
        "eligible_for_non_eu": True,
        "required_previous_degree": bi(
            "A baccalaureate degree equivalent to Caltech's bachelor's degree, completed before graduate study begins.",
            "Lisansüstü eğitim başlamadan tamamlanmış, Caltech lisans derecesine eşdeğer bir lisans derecesi.",
        ),
        "accepted_backgrounds": [
            bi("Strong undergraduate mathematics", "Güçlü lisans matematiği"),
            bi("Physics", "Fizik"),
            bi("Engineering science", "Mühendislik bilimi"),
        ],
        "minimum_gpa": None,
        "successful_applicant_context_not_requirement": bi(
            "Caltech publishes no minimum GPA; it says most successful applicants have at least a 3.5 US GPA and/or rank in the top 5–10%, but this is context rather than an eligibility threshold.",
            "Caltech asgari GNO yayımlamaz; başarılı adayların çoğunun ABD ölçeğinde en az 3,5 GNO'ya ve/veya sınıfın ilk %5–10'una sahip olduğunu söyler, ancak bu bir uygunluk eşiği değil bağlamdır.",
        ),
        "international_gpa_conversion_requested": False,
        "admission_mode": "direct_terminal_ms_application",
        "terminal_ms_direct_application_available": True,
        "one_academic_option_per_cycle": True,
        "admission_risk": "high",
        "galcit_priority": bi(
            "GALCIT is primarily PhD-focused and gives admission priority to applicants who ultimately plan PhD-level research.",
            "GALCIT öncelikle doktora odaklıdır ve nihai olarak doktora düzeyinde araştırma planlayan adaylara kabul önceliği verir.",
        ),
        "required_documents": [
            bi("Online graduate application", "Çevrim içi lisansüstü başvurusu"),
            bi("Transcript from every college or university attended; unofficial/scanned records are accepted for application", "Devam edilen her kolej veya üniversiteden transkript; başvuruda resmî olmayan/taranmış kayıt kabul edilir"),
            bi("Three recommendation letters", "Üç referans mektubu"),
            bi("Curriculum vitae", "Özgeçmiş"),
            bi("Application essays / statement materials", "Başvuru yazıları / amaç beyanı materyalleri"),
            bi("English-proficiency evidence under the applicable department/central rule", "Uygulanabilir bölüm/merkez kuralına göre İngilizce yeterlik kanıtı"),
        ],
        "recommendation_letter_count": 3,
        "maximum_recommendation_letter_count": 3,
        "official_transcripts_required_at_application": False,
        "official_transcripts_required_after_acceptance": True,
        "english_translation_required_for_non_english_transcripts": True,
        "application_fee_usd": 100,
        "application_fee_waiver_possible": True,
        "application_fee_waiver_limited": True,
        "application_fee_waiver_international_eligibility": None,
        "interview_required": False,
        "interview_policy": "may_be_invited_not_required_for_all",
        "gre": {
            "policy": "optional",
            "required": False,
            "considered_if_submitted": True,
            "test_type": "GRE General",
            "minimum_scores": {},
            "recommended_scores": {},
            "current_department_wording": "optional",
            "central_2025_table_wording": "recommended_without_disadvantage_if_missing",
            "policy_conflict": bi(
                "The live Aerospace page says optional. A central 2025 test-policy PDF marks Space Engineering as recommended and explicitly says applicants without scores are not disadvantaged. No score threshold is published.",
                "Canlı Aerospace sayfası isteğe bağlı der. Merkezî 2025 sınav politikası PDF'i Space Engineering'i önerilen olarak işaretler ve puanı olmayan adayların dezavantajlı olmayacağını açıkça söyler. Puan eşiği yayımlanmamıştır.",
            ),
            "source_ids": [DEPT_ADMISSION, TESTS],
        },
        "verification_notes": bi(
            "Non-EU applicants are eligible for this direct terminal-MS route, but eligibility does not imply admission, funding, visa issuance, JPL access or work authorisation.",
            "AB dışı adaylar bu doğrudan terminal-MS rotasına uygundur; ancak uygunluk kabul, finansman, vize, JPL erişimi veya çalışma izni anlamına gelmez.",
        ),
    }

    row["language_profile"] = {
        "teaching_language": ["English"],
        "teaching_languages": ["English"],
        "english_required": True,
        "teaching_language_evidence_type": "operational_requirement_not_separate_instruction_language_label",
        "accepted_english_tests": [
            {"test": "TOEFL", "minimum_score": None},
            {"test": "PTE", "minimum_score": None},
            {"test": "IELTS", "minimum_score": None},
            {"test": "Duolingo English Test or another certified examination", "minimum_score": None},
        ],
        "minimum_scores": {},
        "self_report_at_application_allowed": True,
        "ets_institution_code": "4034",
        "central_waiver_routes": [
            bi("Studied in the United States for two or more years", "ABD'de iki yıl veya daha uzun süre eğitim"),
            bi("Degree from a college or university whose primary instruction is English", "Birincil öğretim dili İngilizce olan kolej veya üniversiteden derece"),
        ],
        "post_admission_english_evaluation_possible": True,
        "esl_course_may_be_required": True,
        "policy_conflict": bi(
            "The live Aerospace page states a programme-specific TOEFL rule for applicants whose first or native language is not English. The current central FAQ says an English test is not required for admission, accepts several tests and publishes exemptions. Treat this as an unresolved official-source conflict and obtain written option guidance before relying on an exemption.",
            "Canlı Aerospace sayfası, ilk veya ana dili İngilizce olmayan adaylar için programa özgü TOEFL kuralı belirtir. Güncel merkezî SSS, İngilizce sınavının kabul için zorunlu olmadığını söyler, birden fazla sınavı kabul eder ve muafiyetler yayımlar. Bunu çözülmemiş resmî kaynak çelişkisi olarak ele alın ve muafiyete güvenmeden önce option'dan yazılı yönlendirme alın.",
        ),
        "language_risk": "high",
        "verification_notes": bi(
            "No official minimum English score is published. English is operationally established through application, evaluation and ESL rules, but the checked pages do not provide a separate programme instruction-language label; confidence remains medium.",
            "Resmî asgari İngilizce puanı yayımlanmamıştır. İngilizce başvuru, değerlendirme ve ESL kurallarıyla operasyonel olarak kanıtlanır; ancak kontrol edilen sayfalar ayrı bir program öğretim-dili etiketi vermediğinden güven orta düzeyde kalır.",
        ),
    }

    row["cost_profile"] = {
        "academic_year": "2026/2027",
        "currency": "USD",
        "tuition_usd_per_year": 68574,
        "mandatory_fees_usd_per_year": 2448,
        "total_tuition_and_mandatory_fees_usd_per_year": 71022,
        "first_year_tuition_and_mandatory_fees_usd_example": 71022,
        "tuition_usd_per_term": 22858,
        "mandatory_fees_usd_per_term": 816,
        "total_tuition_and_fees_usd_per_term": 23674,
        "tuition_basis": "official_institute_wide_three_term_graduate_rate",
        "health_insurance_required": True,
        "health_insurance_automatic_enrollment": True,
        "health_insurance_waiver_possible": True,
        "health_insurance_premium_usd": None,
        "health_insurance_rate_reason": bi(
            "The checked public pages do not publish a current 2026/27 terminal-MS graduate contribution. Older graduate and current undergraduate figures are not transferred into this field.",
            "Kontrol edilen kamuya açık sayfalar güncel 2026/27 terminal-MS lisansüstü öğrenci katkısını yayımlamaz. Eski lisansüstü ve güncel lisans rakamları bu alana taşınmaz.",
        ),
        "living_cost_source_academic_year": "2025/2026",
        "living_cost_usd_per_year_min": 31774,
        "living_cost_usd_per_year_max": 44554,
        "living_cost_scenarios": [
            {"housing": "on-campus four-bedroom, per bed", "amount_usd": 31774, "academic_year": "2025/2026"},
            {"housing": "on-campus two-bedroom, per bed", "amount_usd": 34174, "academic_year": "2025/2026"},
            {"housing": "on-campus one-bedroom, per unit", "amount_usd": 42034, "academic_year": "2025/2026"},
            {"housing": "Caltech-owned two-bedroom lease property, per unit", "amount_usd": 44554, "academic_year": "2025/2026"},
        ],
        "total_cost_of_attendance_usd_per_year": None,
        "complete_program_cost_usd": None,
        "mixed_year_planning_total_not_presented": True,
        "tuition_eur_per_year_min": None,
        "tuition_eur_per_year_max": None,
        "tuition_eur_per_year_estimated": None,
        "scholarship_availability": "competitive_not_guaranteed_terminal_ms_exception",
        "scholarship_risk": "very_high",
        "verification_notes": bi(
            "Current 2026/27 tuition and fees are not added to 2025/26 living estimates as though they formed a same-year official cost of attendance. A current total and current terminal-MS insurance contribution therefore remain null.",
            "Güncel 2026/27 öğrenim ve zorunlu ücretleri, aynı yılın resmî toplam maliyetiymiş gibi 2025/26 yaşam tahminlerine eklenmez. Bu nedenle güncel toplam ve terminal-MS sigorta katkısı null kalır.",
        ),
        "cost_notes": bi(
            "A self-funded terminal MS student should plan for the full USD 71,022 tuition-and-mandatory-fee bill plus insurance, housing, food, books, personal costs, relocation and travel.",
            "Kendi finansmanını sağlayan terminal MS öğrencisi, 71.022 USD öğrenim ve zorunlu ücret faturasına ek olarak sigorta, konut, yemek, kitap, kişisel gider, taşınma ve seyahati planlamalıdır.",
        ),
    }

    row["scholarship_profile"] = {
        "available_types": ["departmental graduate fellowship", "external fellowship", "limited assistantship possibility"],
        "non_eu_eligible": None,
        "application_mode": "automatic",
        "automatic_consideration": True,
        "separate_application_required": False,
        "automatic_consideration_conditions": bi(
            "Select yes for financial aid and submit a complete graduate application by the department's aid deadline. The public page does not state a separate aid-deadline date.",
            "Mali yardım için evet seçin ve eksiksiz lisansüstü başvuruyu bölümün yardım son tarihine kadar gönderin. Kamuya açık sayfa ayrı bir yardım son tarihi yayımlamaz.",
        ),
        "funding_guaranteed_at_admission": False,
        "terminal_ms_often_self_supported": True,
        "departmental_fellowship_typical_duration_academic_years": 1,
        "departmental_fellowship_full_tuition": True,
        "departmental_fellowship_living_stipend": True,
        "departmental_fellowship_primary_target": "entering_masters_candidates_with_doctoral_potential",
        "assistantships_limited_for_full_course_load_masters": True,
        "outside_part_time_employment_allowed": False,
        "award_notification_typical_by": "March 15",
        "award_reply_deadline": "April 15",
        "scholarship_deadline": None,
        "opportunities": [
            {"name": "Booth-Kresa Department of Aerospace graduate fellowship", "automatic": True, "separate_application": False, "international_eligibility": None, "deadline": None},
            {"name": "External fellowship or sponsorship", "automatic": False, "separate_application": True, "international_eligibility": None, "deadline": None},
        ],
        "phd_stipend_not_applicable": True,
        "verification_notes": bi(
            "Caltech's 98% graduate funding statistic and USD 50,000 PhD stipend must not be applied to this terminal MS. Central pages explicitly identify terminal master's students as the major funding exception; some are admitted without aid and must finance the whole degree.",
            "Caltech'nin %98 lisansüstü finansman istatistiği ve 50.000 USD doktora stipend'ı bu terminal MS'e uygulanamaz. Merkezî sayfalar terminal yüksek lisans öğrencilerini başlıca finansman istisnası olarak açıkça tanımlar; bazıları desteksiz kabul edilir ve tüm dereceyi finanse etmelidir.",
        ),
    }

    row["living_profile"] = {
        "city_type": "high_cost_los_angeles_metro",
        "city_cost_level": "very_high",
        "housing_difficulty": "medium_first_year_if_on_time_high_after_first_year",
        "living_risk": "high",
        "housing_access": "guaranteed",
        "housing_guarantee_type": "first_year_guarantee_if_deadline_met",
        "housing_application_separate": True,
        "housing_guaranteed": True,
        "housing_guarantee_conditions": bi(
            "Incoming graduate students are exempt from the lottery and guaranteed campus housing if the separate application is received by the deadline. The 2026/27 application required at least three eligible choices.",
            "Yeni lisansüstü öğrenciler kuradan muaftır ve ayrı başvuru son tarihe kadar ulaşırsa kampüs konutu garantilidir. 2026/27 başvurusu en az üç uygun seçenek gerektiriyordu.",
        ),
        "current_cycle_housing_deadline": None,
        "latest_published_housing_cycle": "2026/2027",
        "latest_published_housing_opens": "2026-04-15",
        "latest_published_housing_deadline": "2026-04-30",
        "latest_published_contract_period": "2026-09-01 to 2027-07-31",
        "after_first_year_lottery_required": True,
        "official_rent_items": [
            {"item": bi("Catalina furnished four-bedroom, per bed", "Catalina mobilyalı dört yatak odalı, yatak başına"), "amount_usd_min": 830, "amount_usd_max": 830, "period": "month", "academic_year": "2026/2027"},
            {"item": bi("Catalina furnished two-bedroom, per bed", "Catalina mobilyalı iki yatak odalı, yatak başına"), "amount_usd_min": 987, "amount_usd_max": 987, "period": "month", "academic_year": "2026/2027"},
            {"item": bi("Catalina furnished one-bedroom, per bed", "Catalina mobilyalı tek yatak odalı, yatak başına"), "amount_usd_min": 1664, "amount_usd_max": 1664, "period": "month", "academic_year": "2026/2027"},
            {"item": bi("Caltech-owned furnished studio, per apartment", "Caltech'e ait mobilyalı stüdyo, daire başına"), "amount_usd_min": 1255, "amount_usd_max": 1255, "period": "month", "academic_year": "2026/2027"},
            {"item": bi("Caltech-owned unfurnished one-bedroom, per apartment", "Caltech'e ait mobilyasız tek yatak odalı, daire başına"), "amount_usd_min": 1381, "amount_usd_max": 1381, "period": "month", "academic_year": "2026/2027"},
            {"item": bi("Caltech-owned unfurnished two-bedroom, per apartment", "Caltech'e ait mobilyasız iki yatak odalı, daire başına"), "amount_usd_min": 1853, "amount_usd_max": 1853, "period": "month", "academic_year": "2026/2027"},
        ],
        "catalina_internet_usd_per_month": 20,
        "utilities_extra": True,
        "catalina_estimated_gas_power_usd_per_month": {"four_bedroom_per_person": 100, "two_bedroom_per_person_min": 110, "two_bedroom_per_person_max": 150, "one_bedroom_min": 120, "one_bedroom_max": 160},
        "off_campus_caltech_owned_estimated_gas_power_usd_per_month": {"studio_min": 120, "studio_max": 160, "one_bedroom_min": 120, "one_bedroom_max": 160, "two_bedroom_min": 160, "two_bedroom_max": 210},
        "verification_notes": bi(
            "The first-year guarantee is deadline-dependent, not a claim that every preferred room type is available. Rates are scoped per bed or per apartment exactly as published; utilities and optional services can add cost.",
            "İlk yıl garantisi son tarihe bağlıdır; her tercih edilen oda tipinin mevcut olduğu anlamına gelmez. Ücretler yayımlandığı gibi yatak veya daire kapsamıyla verilir; faturalar ve isteğe bağlı hizmetler maliyeti artırabilir.",
        ),
    }

    row["curriculum_profile"] = {
        "total_units": 135,
        "unit_system": "Caltech units",
        "duration_academic_years": 1,
        "course_count_fixed": False,
        "course_count_summary": bi(
            "Official five-core-course framework; exact class count varies by the two chosen sequences, mathematics and electives.",
            "Resmî beş çekirdek-ders çerçevesi; kesin ders sayısı seçilen iki diziye, matematiğe ve seçmelilere göre değişir.",
        ),
        "official_total_units": 135,
        "listed_requirement_component_sum_units": 138,
        "official_arithmetic_discrepancy": True,
        "requirement_components": [
            {"name": bi("First selected technical sequence: fluids, solids/structures, or autonomy/control — 27 units", "İlk seçilen teknik dizi: akışkanlar, katılar/yapılar veya otonomi/kontrol — 27 birim"), "units": 27},
            {"name": bi("Second selected technical sequence: fluids, solids/structures, or autonomy/control — 27 units", "İkinci seçilen teknik dizi: akışkanlar, katılar/yapılar veya otonomi/kontrol — 27 birim"), "units": 27},
            {"name": bi("Ae 105abc Space Engineering — 27 units", "Ae 105abc Space Engineering — 27 birim"), "units": 27},
            {"name": bi("Adviser-approved mathematics sequence — 27 units", "Danışman onaylı matematik dizisi — 27 birim"), "units": 27},
            {"name": bi("Ae 150abc Aerospace Engineering Seminar — 3 units", "Ae 150abc Aerospace Engineering Seminar — 3 birim"), "units": 3},
            {"name": bi("Adviser-approved electives supporting programme goals — 27 units", "Program hedeflerini destekleyen danışman onaylı seçmeliler — 27 birim"), "units": 27},
        ],
        "tracks": [
            bi("Fluid mechanics sequence", "Akışkanlar mekaniği dizisi"),
            bi("Solid/structural mechanics sequence", "Katı/yapı mekaniği dizisi"),
            bi("Autonomy and control sequence", "Otonomi ve kontrol dizisi"),
        ],
        "space_engineering_sequence": {
            "course": "Ae 105abc",
            "units_each_term": 9,
            "total_units": 27,
            "terms": 3,
            "prerequisites": "ME 11abc and ME 12abc or equivalent",
            "topics": ["astrodynamics and mission design", "spacecraft systems and subsystems", "launch vehicles and space environments", "structures and thermal design", "communications and power", "team project with SRR, PDR and CDR"],
        },
        "fall_2026_ae105a_scheduled": True,
        "minimum_grade": "C or Pass when pass/fail only",
        "first_term_plan_adviser_approval_required": True,
        "thesis_required": False,
        "research_required": False,
        "mandatory_internship": False,
        "internship_required": False,
        "phd_continuation_automatic": False,
        "phd_continuation_requires_petition": True,
        "verification_notes": bi(
            "The current catalog states at least 135 units, but its listed 27+27+27+27+3+27 components total 138. The database preserves both official statements instead of silently changing either one. The terminal MS has no thesis or research requirement.",
            "Güncel katalog en az 135 birim der; ancak listelenen 27+27+27+27+3+27 bileşenleri 138 eder. Veri tabanı iki resmî ifadeyi de sessizce değiştirmeden korur. Terminal MS'te tez veya araştırma şartı yoktur.",
        ),
    }

    row["category_profile"] = {
        "primary_categories": ["space_systems_engineering", "space_mission_design"],
        "secondary_categories": ["gnc_autonomy_control", "structures_materials", "aerodynamics_fluid_mechanics", "propulsion_combustion", "hypersonics_entry", "scientific_ai_computational_digital"],
        "technical_focus": bi(
            "Space mission design, spacecraft systems, astrodynamics, structures, thermal design, autonomy/GNC, fluids, propulsion and extreme environments.",
            "Uzay görev tasarımı, uzay aracı sistemleri, astrodinamik, yapılar, termal tasarım, otonomi/GNC, akışkanlar, itki ve aşırı ortamlar.",
        ),
        "verification_notes": bi("Categories are mapped from the checked curriculum and department research pages, not from the programme title alone.", "Kategoriler yalnızca program adından değil, kontrol edilen müfredat ve bölüm araştırma sayfalarından eşlenmiştir."),
    }

    row["research_profile"] = {
        "research_fit_for_terminal_ms": "strong_ecosystem_but_no_degree_research_requirement",
        "research_requirement": False,
        "research_place_guaranteed": False,
        "research_focus_areas": [
            bi("Lightweight and deployable space structures", "Hafif ve açılır uzay yapıları"),
            bi("In-space manufacturing", "Uzayda üretim"),
            bi("Extreme-temperature, radiation and hypervelocity-impact behaviour", "Aşırı sıcaklık, radyasyon ve hiperhızlı çarpma davranışı"),
            bi("Hypersonic planetary entry", "Hipersesli gezegen atmosferine giriş"),
            bi("In-space propulsion and micropropulsion", "Uzay içi itki ve mikro-itki"),
            bi("Spacecraft autonomy, swarms, navigation, GNC and robotic assembly", "Uzay aracı otonomisi, sürüler, seyrüsefer, GNC ve robotik montaj"),
        ],
        "key_institutes": [
            {"name": "Graduate Aerospace Laboratories of the California Institute of Technology (GALCIT)", "type": "departmental_research_laboratories"},
            {"name": "Center for Autonomous Systems and Technologies (CAST)", "type": "interdisciplinary_center"},
            {"name": "Keck Institute for Space Studies (KISS)", "type": "space_mission_and_technology_institute"},
            {"name": "Space Solar Power Project (SSPP)", "type": "space_technology_initiative"},
        ],
        "named_labs_and_facilities": [
            "T5 Hypervelocity Shock Tunnel",
            "Explosion Dynamics and Detonation Physics laboratories",
            "Small Particle Hypervelocity Impact Facility",
            "Computational Fluid Dynamics Laboratory",
            "Computational Solid Mechanics Laboratory",
            "Aero Machine Shop",
        ],
        "jpl_collaboration_opportunities": True,
        "jpl_access_guaranteed": False,
        "research_strength_summary": bi(
            "Exceptional space-technology depth across structures, entry physics, autonomy, propulsion and mission systems, with official JPL collaboration opportunities; the one-year terminal MS itself remains coursework-only.",
            "Yapılar, giriş fiziği, otonomi, itki ve görev sistemlerinde olağanüstü uzay-teknolojisi derinliği ve resmî JPL işbirliği fırsatları vardır; bir yıllık terminal MS'in kendisi ise yalnızca ders temellidir.",
        ),
        "research_risk": "medium",
        "verification_notes": bi(
            "Named facilities and JPL opportunities prove ecosystem strength, not a guaranteed laboratory seat, project, adviser, internship or employment outcome for terminal-MS students.",
            "İsimli tesisler ve JPL fırsatları ekosistem gücünü kanıtlar; terminal-MS öğrencisi için garanti laboratuvar yeri, proje, danışman, staj veya iş sonucu kanıtlamaz.",
        ),
    }

    row["industry_ecosystem_profile"] = {
        "local_industry_strength": "very_high",
        "verified_partnerships": [
            {
                "partner": "NASA Jet Propulsion Laboratory (JPL)",
                "relationship": bi("JPL has been managed by Caltech for NASA since 1958; the Aerospace space-technology page separately states that research collaboration opportunities exist.", "JPL 1958'den beri NASA için Caltech tarafından yönetilir; Aerospace uzay-teknolojisi sayfası ayrıca araştırma işbirliği fırsatları bulunduğunu belirtir."),
                "student_access_guaranteed": False,
                "source_ids": [JPL, SPACE_TECH],
            }
        ],
        "nearby_companies": [],
        "company_presence_not_treated_as_partnership": True,
        "export_control_risk": "project_specific_high_for_some_space_and_defense_work",
        "international_student_note": bi(
            "Most open fundamental research is covered by the fundamental-research exclusion, but export-controlled ITAR/high-EAR student research requires formal Provost approval; JPL maintains a separate export policy. Nationality-dependent access must be checked project by project.",
            "Açık temel araştırmaların çoğu temel-araştırma istisnasındadır; ancak ihracat kontrollü ITAR/yüksek-EAR öğrenci araştırması resmî Provost onayı gerektirir ve JPL ayrı ihracat politikası uygular. Vatandaşlığa bağlı erişim proje bazında kontrol edilmelidir.",
        ),
        "industry_risk": "export_control_and_work_authorisation_constraints",
        "verification_notes": bi(
            "Only the officially documented Caltech–JPL relationship is listed. SpaceX, Northrop Grumman and other regional employers are not represented as programme partners without programme-specific evidence.",
            "Yalnızca resmî olarak belgelenen Caltech–JPL ilişkisi listelenir. SpaceX, Northrop Grumman ve diğer bölgesel işverenler programa özgü kanıt olmadan program ortağı olarak sunulmaz.",
        ),
    }

    row["application_timeline_profile"] = {
        "intake": "Fall only",
        "start_month": "September",
        "application_opens": None,
        "non_eu_deadline": "December 15 (standing annual deadline; cycle year not stated)",
        "deadline_non_eu": "December 15",
        "recurring_deadline_month_day": "12-15",
        "next_dated_deadline": None,
        "deadline_year_published": False,
        "application_system_closes": "12:01 a.m. on the day after the posted deadline",
        "late_application_possible": True,
        "late_application_disadvantage_possible": True,
        "decision_window": "From the programme deadline through April 1",
        "offer_reply_deadline": "April 15",
        "scholarship_deadline": None,
        "document_completion_deadline": None,
        "enrollment_deadline": None,
        "pre_enrollment_required": False,
        "visa_complexity": "high",
        "visa_document_request_system": bi("International Student Programs after the student accepts the official offer", "Öğrenci resmî teklifi kabul ettikten sonra International Student Programs"),
        "visa_document_processing_time_business_days_min": None,
        "visa_document_processing_time_business_days_max": None,
        "financial_proof_required_before_i20_or_ds2019": None,
        "financial_proof_amount_location": None,
        "international_orientation_mandatory": True,
        "immigration_check_in_after_us_arrival_required": True,
        "visa_sensitive_deadline": bi(
            "Caltech publishes no public current I-20/DS-2019 processing time or financial-proof amount on the checked pages. After accepting, obtain the personalised ISP checklist immediately and preserve visa lead time.",
            "Caltech kontrol edilen sayfalarda güncel I-20/DS-2019 işlem süresi veya mali kanıt tutarı yayımlamaz. Kabulden sonra kişisel ISP kontrol listesini hemen alın ve vize için yeterli süre bırakın.",
        ),
        "housing_application_separate": True,
        "latest_housing_benchmark_deadline": "2026-04-30",
        "deadline_notes": bi(
            "December 15 is a live standing departmental deadline without a cycle year, so the database does not fabricate a 2026 or 2027 date. Re-check the programme and central deadline document when the next application opens.",
            "15 Aralık, dönem yılı olmayan canlı ve sürekli bölüm son tarihidir; veri tabanı bu nedenle uydurma bir 2026 veya 2027 tarihi üretmez. Sonraki başvuru açıldığında program ve merkezî son-tarih belgesini yeniden kontrol edin.",
        ),
        "timeline_risk": "high",
    }

    row["student_sentiment_profile"] = {
        "student_satisfaction_score": None,
        "workload_sentiment": "negative_high_intensity_signal",
        "teaching_quality_sentiment": "mixed_insufficient_sample",
        "administration_sentiment": "unknown",
        "housing_sentiment": "mixed_insufficient_sample",
        "city_life_sentiment": "unknown",
        "international_student_sentiment": "unknown",
        "career_support_sentiment": "mixed_insufficient_sample",
        "student_sentiment_summary": bi(
            "A very small, self-selected forum sample repeatedly describes the one-year master's workload and cost as intense and stresses research orientation; recent housing discussion favours living near Pasadena and confirms that graduate housing is optional. This is perception evidence only.",
            "Çok küçük ve öz-seçimli forum örneklemi, bir yıllık yüksek lisansın iş yükünü ve maliyetini yoğun olarak tanımlar ve araştırma yönelimini vurgular; yakın tarihli konut tartışması Pasadena yakınında yaşamayı tercih eder ve lisansüstü konutun isteğe bağlı olduğunu belirtir. Bu yalnızca algı kanıtıdır.",
        ),
        "student_sentiment_sources": [
            {"url": REDDIT_TERMINAL_MS, "date": "2024-01-28", "topic": "terminal MS fit, cost and research orientation"},
            {"url": REDDIT_WORKLOAD, "date": "2019-07-08", "topic": "first-year GALCIT workload"},
            {"url": REDDIT_HOUSING, "date": "2026-03-09", "topic": "graduate housing location and commuting"},
        ],
        "approximate_sample_size": 3,
        "date_range": "2019-07 to 2026-03",
        "sentiment_confidence": "low",
        "verification_notes": bi(
            "The sample is too small, uneven in date and not independently verified, so no satisfaction score is calculated and no anecdote overrides official programme, cost or housing facts.",
            "Örneklem çok küçük, tarih bakımından dengesiz ve bağımsız doğrulanmamıştır; bu nedenle memnuniyet puanı hesaplanmaz ve hiçbir anekdot resmî program, maliyet veya konut bilgisinin önüne geçmez.",
        ),
    }

    source_log = [
        source(PROGRAM, "Caltech Aerospace — Graduate Degrees in Space Engineering", "official_program_page", ["program", "duration", "curriculum", "admission"], "Dedicated Space Engineering degree page.", "Özel Space Engineering derece sayfası."),
        source(CATALOG, "Caltech Academic Catalog — Aerospace graduate regulations", "official_curriculum_page", ["program", "duration", "units", "curriculum", "thesis", "admission"], "Current catalog gives the one-year, at-least-135-unit course-only MS and detailed track structure.", "Güncel katalog bir yıllık, en az 135 birimlik yalnızca ders temelli MS'i ve ayrıntılı iz yapısını verir."),
        source(AE105, "Caltech Catalog — Ae 105abc Space Engineering", "official_curriculum_page", ["curriculum", "course_content", "prerequisites"], "Current course entry gives 9 units per term, prerequisites and mission/spacecraft/team-design content.", "Güncel ders kaydı dönem başına 9 birimi, ön koşulları ve görev/uzay aracı/takım tasarımı içeriğini verir."),
        source(SCHEDULE, "Caltech Fall 2026 schedule", "official_curriculum_page", ["program_status", "curriculum"], "Fall 2026 schedule shows Ae 105A as an in-person scheduled course.", "Güz 2026 çizelgesi Ae 105A'yı yüz yüze planlanmış ders olarak gösterir."),
        source(DEPT_ADMISSION, "Caltech Aerospace — Graduate Admissions and Fellowships", "official_admission_page", ["deadline", "gre", "english_test", "specialization", "scholarship"], "Live department rules and fellowship process.", "Canlı bölüm kuralları ve fellowship süreci."),
        source(FAQ, "Caltech Graduate Studies — Applicant FAQ", "official_admission_page", ["admission", "non_eu", "language", "documents", "decision", "funding"], "Current central applicant procedures, including terminal-MS eligibility and the conflicting central English rule.", "Terminal-MS uygunluğu ve çelişen merkezî İngilizce kuralı dahil güncel merkezî aday prosedürleri."),
        source(APPLY, "Caltech Graduate Studies — Apply Online", "official_admission_page", ["application_fee", "fee_waiver", "deadline_system"], "Official USD 100 fee, limited waiver and portal-close rule.", "Resmî 100 USD ücret, sınırlı muafiyet ve portal kapanış kuralı."),
        source(CHECKLIST, "Caltech Graduate Studies — Application Requirements", "official_admission_page", ["documents", "degree_requirement"], "Bachelor-equivalent, transcripts, three letters, CV and essays.", "Lisans eşdeğeri, transkriptler, üç mektup, CV ve yazılar."),
        source(TESTS, "Caltech 2025 Required Tests instructions", "official_admission_page", ["gre", "language"], "PDF marks Space Engineering GRE as recommended without disadvantage when missing and states the central English policy.", "PDF, Space Engineering GRE'yi önerilen fakat yokluğunda dezavantajsız olarak işaretler ve merkezî İngilizce politikasını verir.", access_status="pdf", confidence="medium"),
        source(TRANSCRIPTS, "Caltech transcript and recommendation instructions", "official_admission_page", ["transcripts", "translations", "recommendations"], "Application-stage transcript and recommendation handling.", "Başvuru aşaması transkript ve referans işleyişi.", access_status="pdf"),
        source(BUDGET, "Caltech Graduate Studies — Estimated Budget", "official_tuition_page", ["tuition", "fees", "living_cost", "insurance", "housing_guarantee"], "Official 2026/27 tuition and fees with separately labelled 2025/26 living examples.", "Ayrı etiketlenmiş 2025/26 yaşam örnekleriyle resmî 2026/27 öğrenim ve zorunlu ücretleri."),
        source(NO_AID, "Caltech — Financing a Graduate Education", "official_scholarship_page", ["funding", "terminal_ms_funding", "employment", "assistantships"], "Explicit terminal-master self-funding exception and limited assistantship warning.", "Açık terminal-yüksek-lisans öz-finansman istisnası ve sınırlı asistanlık uyarısı."),
        source(ADMITTED, "Caltech — FAQ for Admitted Students", "official_admission_page", ["offer_reply", "insurance", "visa_support"], "April 15 reply rule, admitted-student support and insurance scope.", "15 Nisan yanıt kuralı, kabul edilen öğrenci desteği ve sigorta kapsamı."),
        source(INCOMING, "Caltech — New Students", "official_university_policy_page", ["insurance", "arrival", "orientation"], "Current incoming-student checklist confirms automatic medical-plan enrolment unless waived and September 2026 coverage start.", "Güncel yeni öğrenci listesi, muafiyet yoksa otomatik sağlık planı kaydını ve Eylül 2026 başlangıcını doğrular."),
        source(HOUSING_NEW, "Caltech Housing — New Graduate Student Options", "official_housing_page", ["housing", "housing_application", "deadline", "contract", "utilities"], "2026/27 separate housing application, dates, choices, contract and utility estimates.", "2026/27 ayrı konut başvurusu, tarihler, tercihler, sözleşme ve fatura tahminleri."),
        source(HOUSING_RATES, "Caltech Housing — Graduate Contracts and Rates", "official_housing_page", ["housing", "housing_rates", "utilities"], "Current 2026/27 monthly rates with per-bed/per-apartment scope.", "Yatak/daire kapsamıyla güncel 2026/27 aylık ücretleri."),
        source(HOUSING_LOTTERY, "Caltech Housing — Graduate Lottery Process", "official_housing_page", ["housing", "housing_guarantee", "housing_after_first_year"], "Incoming deadline-based guarantee and returning-student lottery rules.", "Yeni öğrenci son-tarih garantisi ve devam eden öğrenci kura kuralları."),
        source(HOUSING_CONTRACT, "Caltech 2026/27 Graduate Housing Contract", "official_housing_page", ["housing", "housing_contract"], "Current official graduate housing contract PDF.", "Güncel resmî lisansüstü konut sözleşmesi PDF'i.", access_status="pdf"),
        source(RESEARCH, "Caltech Aerospace", "official_department_page", ["research_areas", "program_status"], "Current department research-area overview.", "Güncel bölüm araştırma alanı özeti."),
        source(SPACE_TECH, "Caltech Aerospace — Space Technology", "official_department_page", ["research", "jpl_collaboration"], "Named space-technology themes and official JPL collaboration opportunity.", "İsimli uzay-teknolojisi temaları ve resmî JPL işbirliği fırsatı."),
        source(CENTERS, "Caltech Aerospace — Centers and Initiatives", "official_department_page", ["centers", "research"], "CAST, KISS and Space Solar Power descriptions.", "CAST, KISS ve Space Solar Power açıklamaları."),
        source(FACILITIES, "Caltech Aerospace — Research Labs and Facilities", "official_lab_page", ["labs", "facilities"], "Named fluids, combustion, impact, computational and manufacturing facilities.", "İsimli akışkan, yanma, çarpma, hesaplamalı ve üretim tesisleri."),
        source(JPL, "Caltech Catalog — Jet Propulsion Laboratory", "official_industry_partner_page", ["industry_ecosystem", "partnership"], "Current catalog confirms Caltech management of JPL for NASA since 1958.", "Güncel katalog Caltech'nin JPL'yi 1958'den beri NASA için yönettiğini doğrular."),
        source(ISP, "Caltech International Student Programs", "official_visa_or_government_page", ["visa", "international_support"], "ISP assists international students after they accept an official offer.", "ISP, uluslararası öğrencilere resmî teklifi kabul ettikten sonra yardım eder."),
        source(ORIENTATION, "Caltech ISP — Check-in and Orientation", "official_visa_or_government_page", ["arrival", "orientation", "check_in"], "Mandatory international orientation and post-arrival immigration check-in.", "Zorunlu uluslararası oryantasyon ve varış sonrası göçmenlik kaydı."),
        source(EXPORT, "Caltech Export Compliance Policy", "official_university_policy_page", ["export_control", "international_research_access"], "Fundamental-research scope and formal approval for controlled student work.", "Temel araştırma kapsamı ve kontrollü öğrenci çalışması için resmî onay."),
        source(QS, "QS — California Institute of Technology", "official_ranking_page", ["prestige"], "QS World University Rankings 2027 institutional rank #7; context only.", "QS Dünya Üniversite Sıralaması 2027 kurum sırası #7; yalnızca bağlam.", confidence="medium"),
        source(REDDIT_TERMINAL_MS, "Reddit — Caltech for a working engineer?", "student_forum", ["student_sentiment"], "Small anecdotal terminal-MS cost, pedagogy and research-orientation discussion.", "Küçük anekdotsal terminal-MS maliyet, pedagoji ve araştırma yönelimi tartışması.", confidence="low"),
        source(REDDIT_WORKLOAD, "Reddit — Research in GALCIT?", "student_forum", ["student_sentiment"], "Older direct anecdotal signal about first-year workload.", "Birinci yıl iş yüküne dair eski doğrudan anekdotsal sinyal.", confidence="low"),
        source(REDDIT_HOUSING, "Reddit — Caltech graduate students living off campus", "student_forum", ["student_sentiment"], "Recent anecdotal Pasadena/commute and graduate-housing discussion.", "Yakın tarihli anekdotsal Pasadena/ulaşım ve lisansüstü konut tartışması.", confidence="low"),
    ]

    official_count = sum(item["source_type"] != "student_forum" for item in source_log)
    critical_count = sum(item["source_type"] not in {"student_forum", "official_ranking_page"} for item in source_log)
    row["source_profile"] = {
        "primary_url": PROGRAM,
        "secondary_urls": [CATALOG, DEPT_ADMISSION, BUDGET, HOUSING_NEW, SPACE_TECH],
        "last_verified": TODAY,
        "field_confidence": {
            "program_basic_info": "high",
            "program_status": "high",
            "admission": "high",
            "non_eu_eligibility": "high",
            "deadlines": "medium",
            "curriculum": "medium",
            "tuition": "high",
            "scholarship": "high",
            "housing": "high",
            "research": "high",
            "industry_partnership": "high",
            "visa": "medium",
            "language": "medium",
            "sentiment": "low",
        },
        "source_reliability": "high",
        "verification_status": "partial",
        "needs_verification": True,
        "source_log": source_log,
        "verification_notes": bi(
            "Critical fields use current official evidence. The record remains partial because the official English rules conflict, the deadline page gives no cycle year, the catalog unit components do not reconcile to its stated total, and public current I-20/insurance details are incomplete.",
            "Kritik alanlar güncel resmî kanıt kullanır. Resmî İngilizce kuralları çeliştiği, son tarih sayfası dönem yılı vermediği, katalog birim bileşenleri belirtilen toplamla uyuşmadığı ve kamuya açık güncel I-20/sigorta ayrıntıları eksik olduğu için kayıt partial kalır.",
        ),
    }

    row["decision_summary"] = {
        "main_strengths": [
            bi("A dedicated, active one-year Space Engineering MS with deep spacecraft and mission-design content.", "Derin uzay aracı ve görev tasarımı içeriğine sahip özel, aktif bir yıllık Space Engineering MS."),
            bi("Exceptional structures, autonomy, entry, propulsion and space-technology ecosystem with documented JPL collaboration opportunities.", "Belgeli JPL işbirliği fırsatlarıyla olağanüstü yapılar, otonomi, giriş, itki ve uzay-teknolojisi ekosistemi."),
            bi("Deadline-compliant incoming graduate students receive first-year campus-housing assurance.", "Son tarihe uyan yeni lisansüstü öğrenciler ilk yıl kampüs konutu güvencesi alır."),
        ],
        "main_risks": [
            bi("Terminal MS funding is not guaranteed and many students are self-supported; the current direct academic bill is USD 71,022 before living and insurance.", "Terminal MS finansmanı garanti değildir ve birçok öğrenci kendi finansmanını sağlar; güncel doğrudan akademik fatura yaşam ve sigorta öncesi 71.022 USD'dir."),
            bi("The department prioritises PhD-oriented applicants even though the MS itself has no research or thesis requirement.", "MS'in kendisinde araştırma veya tez şartı olmamasına rağmen bölüm doktora yönelimli adaylara öncelik verir."),
            bi("English-test rules conflict across official pages, and some space/JPL projects can be constrained by export controls or work authorisation.", "İngilizce sınav kuralları resmî sayfalar arasında çelişir; bazı uzay/JPL projeleri ihracat kontrolü veya çalışma izniyle sınırlanabilir."),
            bi("The official curriculum's listed units sum to 138 while the stated programme minimum is 135; adviser confirmation is required.", "Resmî müfredatın listelenen birimleri 138 ederken belirtilen program asgarisi 135'tir; danışman teyidi gerekir."),
        ],
        "best_for": bi(
            "An exceptionally strong applicant seeking a fast, rigorous space-systems foundation, able to finance the programme if fellowship support does not materialise, and comfortable with a PhD-oriented research culture.",
            "Hızlı ve yoğun bir uzay-sistemleri temeli isteyen, fellowship çıkmazsa programı finanse edebilen ve doktora yönelimli araştırma kültürüne uyumlu olağanüstü güçlü aday.",
        ),
        "not_ideal_for": bi(
            "Applicants needing guaranteed funding, a part-time working-professional format, a required thesis, a guaranteed JPL project, or low-cost metropolitan living.",
            "Garantili finansman, çalışan profesyonele uygun yarı zamanlı format, zorunlu tez, garantili JPL projesi veya düşük maliyetli büyükşehir yaşamı gereken adaylar.",
        ),
        "verdict": bi(
            "Top-tier technical fit but a high financial and admission-risk terminal MS. Apply only with a credible self-funding fallback and written clarification of the live English rule; do not treat JPL access or fellowship funding as guaranteed.",
            "Üst düzey teknik uygunluğa sahip ancak finansal ve kabul riski yüksek bir terminal MS. Yalnızca güvenilir öz-finansman yedeğiyle ve canlı İngilizce kuralının yazılı açıklamasıyla başvurun; JPL erişimini veya fellowship finansmanını garanti saymayın.",
        ),
    }

    row["scoring_inputs"] = {
        "academic_prestige": None,
        "research_output": None,
        "industry_links": None,
        "affordability": None,
        "admission_chance": None,
        "living_quality": None,
        "scoring_disabled_reason": bi("No source-backed, programme-specific normalized inputs exist for a defensible numeric score.", "Savunulabilir sayısal puan için kaynaklı, programa özgü normalize girdiler yoktur."),
    }

    verified_fields = ["program", "program_status", "duration", "curriculum", "admission", "non_eu_eligibility", "language", "tuition", "scholarship", "deadline", "housing", "research", "industry_partnership", "visa"]
    row["data_quality"] = {
        "status": "partial",
        "checked_official_source_count": official_count,
        "critical_institutional_source_count": critical_count,
        "student_forum_source_count": 3,
        "verified_fields": verified_fields,
        "unverified_critical_fields": [],
        "has_checked_source_log": True,
        "audited_at": TODAY,
    }
    row["quality_control"] = {
        "checked_at": TODAY,
        "qc_status": "needs_revision",
        "remaining_verification_tasks": [
            bi("Obtain written Aerospace guidance resolving the department TOEFL wording against the central current English policy.", "Bölüm TOEFL ifadesiyle güncel merkezî İngilizce politikasını uzlaştıran yazılı Aerospace yönlendirmesi alın."),
            bi("When the next cycle opens, replace the standing December 15 rule with the dated deadline and add the current housing deadline.", "Sonraki dönem açıldığında sürekli 15 Aralık kuralını tarihli son tarihle değiştirin ve güncel konut son tarihini ekleyin."),
            bi("Add the current terminal-MS graduate insurance contribution and public ISP I-20 checklist only when official pages publish them.", "Güncel terminal-MS lisansüstü sigorta katkısını ve kamuya açık ISP I-20 listesini yalnızca resmî sayfalar yayımladığında ekleyin."),
            bi("Ask the option adviser to reconcile the official 135-unit total with the 138-unit listed component sum.", "Option danışmanından resmî 135 birim toplamını listelenen 138 birim bileşen toplamıyla uzlaştırmasını isteyin."),
        ],
        "failed_canary_tests": ["official_language_policy_conflict", "official_curriculum_unit_discrepancy"],
        "qc_notes": bi(
            "No unsupported numeric satisfaction, admission-chance or affordability score is emitted. Official conflicts and absent cycle-specific facts remain visible rather than being guessed.",
            "Desteksiz sayısal memnuniyet, kabul şansı veya karşılanabilirlik puanı üretilmez. Resmî çelişkiler ve eksik dönem-özel bilgiler tahmin edilmek yerine görünür kalır.",
        ),
    }

    DATA_PATH.write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    audit = {
        "record_id": row["id"],
        "checked_at": TODAY,
        "source_count": len(source_log),
        "official_source_count": official_count,
        "critical_institutional_source_count": critical_count,
        "student_forum_source_count": 3,
        "broken_or_unknown_count": sum(item["access_status"] in {"broken", "not_found", "unknown"} for item in source_log),
        "sources": [
            {key: item[key] for key in ("url", "source_type", "access_status", "last_checked")}
            for item in source_log
        ],
    }
    AUDIT_PATH.parent.mkdir(parents=True, exist_ok=True)
    AUDIT_PATH.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
