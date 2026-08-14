from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data_base" / "amerika.json"
AUDIT_PATH = ROOT / "reports" / "source_link_audit_cu_boulder_aes_ms_2026-08-14.json"
TODAY = "2026-08-14"

PROGRAM = "https://www.colorado.edu/aerospace/admissions/graduates/degree-programs/master-science"
OVERVIEW = "https://www.colorado.edu/engineering/academics/graduate-programs/aerospace-engineering-masters-program"
CATALOG = "https://catalog.colorado.edu/graduate/colleges-schools/engineering-applied-science/programs-study/aerospace-engineering-sciences/aerospace-engineering-sciences-master-science-ms/"
APPLY = "https://www.colorado.edu/aerospace/admissions/graduates/how-apply"
DEADLINES = "https://www.colorado.edu/aerospace/admissions/graduates/deadlines-fees"
ENGLISH = "https://www.colorado.edu/graduateschool/admissions/where-begin/international-students/english-proficiency-requirements"
INTERNATIONAL = "https://www.colorado.edu/graduateschool/admissions/where-begin/international-students"
FUNDING = "https://www.colorado.edu/aerospace/admissions/graduates/funding-your-mastersphd"
TUITION = "https://www.colorado.edu/bursar/media/1122"
COA = "https://www.colorado.edu/financialaid/cost/example-aid"
INSURANCE = "https://www.colorado.edu/health/cu-gold-ship"
HOUSING_APPLICATION = "https://www.colorado.edu/living/housing/graduate-and-family-housing/graduate-family-housing-apartment-application"
HOUSING_RATES = "https://www.colorado.edu/living/rates-contracts-GFH-2026-2027"
FOCUS_AREAS = "https://www.colorado.edu/aerospace/academics/graduates/focus-areas"
RESEARCH = "https://www.colorado.edu/aerospace/research"
RESEARCH_ENTITIES = "https://www.colorado.edu/research/focus/aerospace/institutes-entities"
LASP = "https://lasp.colorado.edu/our-legacy/labs-and-facilities/"
INDUSTRY = "https://www.colorado.edu/research/focus/aerospace/industry-partnerships"
EXPORT = "https://www.colorado.edu/researchinnovation/node/8496/office-export-controls/research-and-export-controls/technology-deemed-exports"
RANKING = "https://www.colorado.edu/engineering/facts-figures"
QS = "https://www.topuniversities.com/universities/university-colorado-boulder"

REDDIT_FUNDING = "https://www.reddit.com/r/cuboulder/comments/1jobk4b"
REDDIT_HOUSING = "https://www.reddit.com/r/cuboulder/comments/1jn8a1f"
REDDIT_PROGRAM = "https://www.reddit.com/r/cuboulder/comments/gyhaup"


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
    row = next(item for item in rows if item.get("id") == "cu-boulder-aes")

    row.update(
        {
            "country": "United States",
            "university": "University of Colorado Boulder",
            "university_native_name": "University of Colorado Boulder",
            "city": "Boulder",
            "region": "Colorado",
            "program_name": "Master of Science in Aerospace Engineering Sciences (Traditional MS)",
            "program_native_name": "Master of Science in Aerospace Engineering Sciences (Traditional MS)",
            "program_degree": "MS",
            "degree_level": "Master",
            "duration_years": 2,
            "duration": bi("Approximately two years", "Yaklaşık iki yıl"),
            "ects": None,
            "us_credit_hours": 30,
            "teaching_language": ["Unknown"],
            "teaching_languages": ["Unknown"],
            "program_url": PROGRAM,
            "program_status": "active",
            "relevance_status": "strong",
            "tuition_eur_per_year": None,
            "annual_fee_eur": None,
            "tuition_usd_per_year": 42000,
            "annual_fee_usd": 970.66,
            "qs_ranking": 320,
            "qs_ranking_display": "#=320",
            "qs_ranking_year": 2027,
        }
    )

    row["prestige_profile"] = {
        "qs_world_rank": 320,
        "qs_rank_is_tied": True,
        "qs_edition": 2027,
        "qs_source_url": QS,
        "us_news_public_graduate_engineering_rank": 10,
        "us_news_public_graduate_aerospace_rank": 5,
        "us_news_edition": "2026-27",
        "official_ranking_source_url": RANKING,
        "interpretation": bi(
            "Rankings are contextual only. The technical-fit assessment below is based on curriculum, focus areas, centres and facilities.",
            "Sıralamalar yalnızca bağlamdır. Aşağıdaki teknik uyum değerlendirmesi müfredat, odak alanları, merkezler ve tesislere dayanır.",
        ),
    }

    row["eligibility_profile"] = {
        "eligible_for_non_eu": True,
        "required_previous_degree": bi(
            "A bachelor's degree from an accredited institution in engineering, mathematics, physics, chemistry or another physical science.",
            "Akredite bir kurumdan mühendislik, matematik, fizik, kimya veya başka bir fizik bilimi alanında lisans derecesi.",
        ),
        "accepted_backgrounds": [
            bi("Engineering", "Mühendislik"),
            bi("Mathematics", "Matematik"),
            bi("Physics", "Fizik"),
            bi("Chemistry or another physical science", "Kimya veya başka bir fizik bilimi"),
        ],
        "expected_prerequisites": [
            bi("Calculus, linear algebra and differential equations", "Kalkülüs, doğrusal cebir ve diferansiyel denklemler"),
            bi("Two semesters of calculus-based physics", "İki dönem kalkülüs tabanlı fizik"),
            bi("At least two upper-division semesters in engineering or physics", "Mühendislik veya fizikte en az iki üst düzey dönem"),
        ],
        "minimum_gpa": None,
        "minimum_gpa_policy": "not_published_on_checked_department_requirements",
        "admission_mode": "faculty_committee_review",
        "admission_risk": "high",
        "required_documents": [
            bi("Online graduate application", "Çevrim içi lisansüstü başvurusu"),
            bi("Unofficial transcript from every attended institution; official records after admission", "Devam edilen her kurumdan resmî olmayan transkript; kabulden sonra resmî kayıtlar"),
            bi("Personal statement / statement of purpose", "Kişisel beyan / amaç mektubu"),
            bi("Three letters of recommendation", "Üç referans mektubu"),
            bi("Resume or CV", "Özgeçmiş"),
            bi("Official English-proficiency evidence when applicable", "Gerektiğinde resmî İngilizce yeterlilik kanıtı"),
        ],
        "motivation_letter_required": True,
        "cv_required": True,
        "recommendation_required": True,
        "recommendation_letter_count": 3,
        "portfolio_required": False,
        "interview_required": None,
        "interview_policy": "not_listed_for_ms_in_checked_official_requirements",
        "international_application_fee_usd": 80,
        "international_application_fee_waiver_available_from_department": False,
        "gre": {
            "policy": "not_accepted",
            "test_type": "GRE General",
            "minimum_scores": {},
            "recommended_scores": {},
            "waiver_rules": [],
            "source_ids": [APPLY],
        },
        "verification_notes": bi(
            "The same published MS deadlines apply to domestic and international applicants. Non-EU eligibility does not imply access to every controlled project or external fellowship.",
            "Yayımlanan aynı MS son tarihleri yerli ve uluslararası adaylara uygulanır. AB dışı uygunluk, her kontrollü projeye veya dış bursa erişim anlamına gelmez.",
        ),
    }

    row["language_profile"] = {
        "teaching_language": ["Unknown"],
        "teaching_languages": ["Unknown"],
        "english_required": True,
        "accepted_english_tests": [
            {"test": "TOEFL iBT", "minimum_score": 80, "validity_years": 2},
            {"test": "TOEFL iBT26", "minimum_score": 4.0, "validity_years": 2},
            {"test": "IELTS Academic", "minimum_score": 6.5, "validity_years": 2},
            {"test": "Duolingo English Test", "minimum_score": 115, "validity_years": 2},
            {"test": "PTE Academic", "minimum_score": 58, "validity_years": 2},
            {"test": "Cambridge English", "minimum_score": 180, "validity_years": 2},
        ],
        "score_source_scope": "graduate_school_default_for_programs_not_separately_listed",
        "proof_required_before_application_review": True,
        "medium_of_instruction_letter_accepted": False,
        "exemptions": [
            bi("Citizenship of a qualifying country", "Nitelikli bir ülkenin vatandaşlığı"),
            bi("At least one year of recent full-time university study in the US or a qualifying country, with official transcripts", "ABD veya nitelikli bir ülkede yakın dönemde en az bir yıl tam zamanlı üniversite eğitimi ve resmî transkript"),
            bi("Qualifying recent OPT history with required evidence", "Gerekli kanıtlarla nitelikli yakın dönem OPT geçmişi"),
        ],
        "language_risk": "medium",
        "verification_notes": bi(
            "English-test requirements are verified, but no checked official source explicitly states the programme's teaching language. It therefore remains Unknown.",
            "İngilizce sınav şartları doğrulandı; ancak kontrol edilen hiçbir resmî kaynak programın eğitim dilini açıkça belirtmez. Bu nedenle alan Unknown kalır.",
        ),
    }

    row["cost_profile"] = {
        "academic_year": "2026/2027",
        "currency": "USD",
        "cost_scope": "international_nonresident_traditional_engineering_ms_two_regular_semesters",
        "tuition_usd_per_semester_full_time_9_or_more_credits": 21000,
        "tuition_usd_per_year": 42000,
        "mandatory_fees_usd_per_semester_full_time": 445.33,
        "mandatory_fees_usd_per_year": 890.66,
        "immigration_compliance_fee_usd_per_semester": 40,
        "immigration_compliance_fee_usd_per_year": 80,
        "international_new_student_fee_usd_one_time": 145,
        "health_insurance_required": True,
        "health_insurance_waiver_possible_with_qualifying_private_plan": True,
        "anthem_gold_ship_usd_per_semester": 2648,
        "anthem_gold_ship_usd_per_year_fall_and_spring": 5296,
        "first_year_direct_university_cost_with_ship_usd": 48411.66,
        "first_year_direct_university_cost_formula": "42000 tuition + 890.66 mandatory fees + 80 immigration compliance + 145 new-student fee + 5296 SHIP",
        "official_nonresident_graduate_coa_housing_and_food_usd_two_semesters": 18684,
        "official_nonresident_graduate_coa_books_usd_two_semesters": 1200,
        "official_nonresident_graduate_coa_personal_usd_two_semesters": 1782,
        "official_nonresident_graduate_coa_transportation_usd_two_semesters": 2062,
        "official_nonresident_graduate_coa_medical_usd_two_semesters": 8136,
        "complete_program_cost_usd": None,
        "tuition_basis": "official 2026-27 out-of-state/international Graduate Status A Engineering schedule",
        "tuition_eur_per_year_min": None,
        "tuition_eur_per_year_max": None,
        "tuition_eur_per_year_estimated": None,
        "total_first_year_cost_eur": None,
        "scholarship_availability": "limited_not_guaranteed",
        "scholarship_risk": "very_high",
        "verification_notes": bi(
            "The $48,411.66 figure is a transparent sum of current direct university charges for a full-time first-year international Engineering MS student using CU SHIP; it excludes housing, food, books, transport and personal spending. The university's general graduate COA uses Arts & Sciences tuition, so it is not misreported as an Aerospace total.",
            "48.411,66 $ tutarı, CU SHIP kullanan tam zamanlı birinci yıl uluslararası Engineering MS öğrencisi için güncel doğrudan üniversite kalemlerinin şeffaf toplamıdır; konut, yemek, kitap, ulaşım ve kişisel harcamaları içermez. Üniversitenin genel lisansüstü COA'sı Arts & Sciences öğrenim ücretini kullandığından Aerospace toplamı olarak sunulmaz.",
        ),
    }

    row["scholarship_profile"] = {
        "available_types": ["teaching_facilitator", "faculty_research_position", "external_fellowship", "student_employment"],
        "non_eu_eligible": "position_or_award_specific",
        "application_mode": "separate",
        "automatic_consideration": False,
        "separate_application_required": True,
        "department_funding_for_masters_provided": False,
        "ta_reserved_for_phd_students": True,
        "teaching_facilitator_open_to_ms": True,
        "teaching_facilitator_stipend": True,
        "teaching_facilitator_tuition_remission": False,
        "research_positions_centrally_managed": False,
        "faculty_outreach_required_for_research_positions": True,
        "funding_guaranteed": False,
        "opportunities": [
            {
                "name": "Teaching Facilitator (TF)",
                "type": "hourly_or_stipend_teaching_support",
                "automatic_consideration": False,
                "separate_application_required": True,
                "tuition_remission": False,
                "eligibility": bi("MS and ProMS students may apply", "MS ve ProMS öğrencileri başvurabilir"),
                "url": FUNDING,
            },
            {
                "name": "Faculty research position",
                "type": "faculty_managed_research_employment",
                "automatic_consideration": False,
                "separate_application_required": True,
                "funding_guaranteed": False,
                "eligibility": bi("Project, skills, funding and export-control specific", "Projeye, beceriye, finansmana ve ihracat kontrolüne özgü"),
                "url": FUNDING,
            },
            {
                "name": "External fellowships",
                "type": "external_competitive_awards",
                "automatic_consideration": False,
                "separate_application_required": True,
                "deadline": bi("Often in fall before the CU application deadline; award-specific", "Çoğu kez CU başvuru tarihinden önce sonbaharda; ödüle özgü"),
                "eligibility": bi("Many named awards restrict citizenship or degree level; verify individually", "Listelenen birçok ödül vatandaşlığı veya derece düzeyini sınırlar; tek tek doğrulayın"),
                "url": FUNDING,
            },
        ],
        "funding_notes": bi(
            "The department explicitly tells master's students to plan on private funds or their own fellowships. Rare faculty support must not be budgeted before a written appointment.",
            "Bölüm yüksek lisans öğrencilerine özel kaynak veya kendi burslarıyla plan yapmalarını açıkça söyler. Nadir öğretim üyesi desteği yazılı atama olmadan bütçelenmemelidir.",
        ),
        "verification_notes": bi(
            "There is no automatic departmental scholarship application for this MS. TF, faculty research and external fellowships follow separate, opportunity-specific processes.",
            "Bu MS için otomatik bölüm burs başvurusu yoktur. TF, öğretim üyesi araştırması ve dış burslar ayrı ve fırsata özgü süreçler izler.",
        ),
    }

    row["living_profile"] = {
        "city_type": "small_high_cost_technology_and_aerospace_hub",
        "city_cost_level": "very_high",
        "housing_difficulty": "high",
        "living_risk": "high",
        "housing_access": "waitlist",
        "student_housing_available": True,
        "housing_application_separate": True,
        "housing_application_fee_usd": 50,
        "housing_offer_security_deposit_usd": 1000,
        "admission_confirmation_deposit_before_housing_access_usd": 200,
        "fall_2026_waitlist_opened": "2026-03-09",
        "fall_offer_start_date": "2026-06-02",
        "housing_allocation_mode": "timestamped_waitlist_subject_to_eligibility_preferences_and_availability",
        "move_in_date_guaranteed": False,
        "offer_before_classes_guaranteed": False,
        "monthly_housing_rent_usd_per_month_min": 1119,
        "monthly_housing_rent_usd_per_month_max": 2163,
        "average_room_rent_usd": None,
        "average_room_rent_scope_label": bi("Official Graduate & Family Housing unit examples, not a city/private-market average", "Resmî Graduate & Family Housing birim örnekleri; şehir/özel piyasa ortalaması değil"),
        "housing_options": [
            {"name": "Athens Court", "studio_usd_per_month": 1119, "one_bedroom_usd_per_month": 1331, "two_bedroom_usd_per_month": 1548, "utilities_included": True},
            {"name": "Marine Court", "one_bedroom_usd_per_month_min": 1331, "one_bedroom_usd_per_month_max": 1403, "two_bedroom_usd_per_month_min": 1548, "two_bedroom_usd_per_month_max": 1638, "three_bedroom_usd_per_month": 1950, "utilities_included": True},
            {"name": "Athens North", "two_bedroom_rate_usd_per_semester_per_bedroom": 4915, "first_year_graduate_eligible": True, "utilities_included": True},
            {"name": "Smiley Court", "one_bedroom_usd_per_month_min": 1396, "one_bedroom_usd_per_month_max": 1463, "two_bedroom_usd_per_month_min": 1611, "two_bedroom_usd_per_month_max": 1706, "three_bedroom_usd_per_month": 2034, "utilities_included": True},
            {"name": "Newton Court", "one_bedroom_usd_per_month": 1472, "two_bedroom_usd_per_month_min": 1761, "two_bedroom_usd_per_month_max": 1848, "three_bedroom_usd_per_month": 2163, "utilities_included": True},
        ],
        "official_living_cost_items": [
            {"item": bi("Housing and food", "Konut ve yemek"), "amount_usd": 18684, "period": "two_semesters", "scope": "official_nonresident_graduate_coa"},
            {"item": bi("Books and supplies", "Kitap ve malzeme"), "amount_usd": 1200, "period": "two_semesters", "scope": "official_nonresident_graduate_coa"},
            {"item": bi("Personal expenses", "Kişisel giderler"), "amount_usd": 1782, "period": "two_semesters", "scope": "official_nonresident_graduate_coa"},
            {"item": bi("Transportation", "Ulaşım"), "amount_usd": 2062, "period": "two_semesters", "scope": "official_nonresident_graduate_coa"},
        ],
        "verification_notes": bi(
            "All graduate-family applications enter a waitlist and housing is explicitly not guaranteed. Rates are institution-owned examples with utilities; they are not private-market rent statistics.",
            "Tüm graduate-family başvuruları bekleme listesine girer ve konut açıkça garanti edilmez. Fiyatlar kamuya ait, hizmetler dâhil kurum örnekleridir; özel piyasa kira istatistiği değildir.",
        ),
    }

    row["curriculum_profile"] = {
        "total_credit_hours": 30,
        "typical_course_equivalent": 10,
        "typical_course_equivalent_caveat": bi("The handbook says 30 credits are equivalent to 10 classes for most focus areas; thesis credits and individual course credit values can change the actual count.", "El kitabı 30 kredinin çoğu odak alanı için 10 derse eşdeğer olduğunu söyler; tez kredileri ve derslerin kredi değerleri gerçek sayıyı değiştirebilir."),
        "minimum_5000_level_or_above_credits": 24,
        "minimum_asen_credits": 18,
        "maximum_approved_4000_level_credits": 6,
        "average_completion_years": 2,
        "maximum_completion_years": 4,
        "tracks": ["thesis", "non_thesis"],
        "thesis_required": False,
        "thesis_type": "optional_six_credit_thesis_with_defense",
        "thesis_credits": 6,
        "thesis_advisor_must_be_secured_by_student": True,
        "non_thesis_completion_routes": [
            bi("Two semesters of graduate projects", "İki dönem lisansüstü proje"),
            bi("Approved certificate", "Onaylı sertifika"),
            bi("Focus-area-defined course-only route where available", "Mevcutsa odak alanının tanımladığı yalnız ders yolu"),
        ],
        "mandatory_internship": False,
        "focus_area_requirements": [
            {"name": "Astrodynamics and Satellite Navigation Systems", "code": "ASN", "requirements": bi("Choose three ASN core classes plus one ASEN graduate class outside ASN.", "Üç ASN çekirdek dersi ve ASN dışından bir ASEN lisansüstü dersi seçilir."), "named_core_options": ["ASEN 5010 Spacecraft Attitude Dynamics and Control", "ASEN 5044 Statistical Estimation for Dynamical Systems", "ASEN 5050 Space Flight Dynamics or ASEN 5052 Analytical Astrodynamics", "ASEN 5090 Introduction to GNSS"]},
            {"name": "Autonomous Systems", "code": "AUT", "requirements": bi("One course from three of five topic areas; course-only route adds two topic-area courses.", "Beş konu alanının üçünden birer ders; yalnız ders yolu iki konu dersi daha ekler.")},
            {"name": "Bioastronautics", "code": "BIO", "requirements": bi("ASEN 5016 and ASEN 5158, one BIO elective, one non-BIO course and one approved mathematics course.", "ASEN 5016 ve ASEN 5158, bir BIO seçmelisi, bir BIO dışı ders ve bir onaylı matematik dersi.")},
            {"name": "Fluids, Structures and Materials", "code": "FSM", "requirements": bi("Two core classes in the chosen track, one core in the other FSM track, and two FSM electives; at least one elective in the chosen track.", "Seçilen hatta iki çekirdek, diğer FSM hattında bir çekirdek ve ikisi FSM seçmelisi; seçmelilerden en az biri seçilen hatta.")},
            {"name": "Remote Sensing, Earth and Space Sciences", "code": "RSESS", "requirements": bi("One course each in data/numerical analysis, instrumentation, physical science, and astrodynamics/aerospace systems.", "Veri/sayısal analiz, enstrümantasyon, fizik bilimi ve astrodinamik/aerospace sistemlerinden birer ders.")},
        ],
        "curriculum_url": CATALOG,
        "study_plan_url": FOCUS_AREAS,
        "verification_notes": bi(
            "The Traditional MS must not be compressed with the separate Professional MS. Both award an MS, but the Traditional MS is focus-area based and offers thesis and non-thesis routes.",
            "Traditional MS ayrı Professional MS ile birleştirilmemelidir. İkisi de MS verir; ancak Traditional MS odak alanı temellidir ve tezli/tezsiz yollar sunar.",
        ),
    }

    row["category_profile"] = {
        "primary_categories": ["space_systems", "astrodynamics", "gnc"],
        "secondary_categories": ["satellite_systems", "autonomy", "aerospace_general", "cfd", "aerospace_structures", "materials", "space_environment", "sensors"],
        "technical_focus": bi("Astrodynamics, satellite navigation, autonomous systems, bioastronautics, fluids/structures/materials, and remote sensing/Earth-space science.", "Astrodinamik, uydu navigasyonu, otonom sistemler, biyoastronotik, akışkanlar/yapılar/malzemeler ve uzaktan algılama/Dünya-uzay bilimi."),
        "verification_notes": bi("Categories are mapped from the five official focus areas and verified curriculum, not inferred from the programme name.", "Kategoriler program adından çıkarılmamış, beş resmî odak alanı ve doğrulanmış müfredattan eşlenmiştir."),
    }

    row["application_timeline_profile"] = {
        "academic_year": "2026/2027",
        "intake_terms": ["Fall", "Spring"],
        "application_rounds": [
            {"intake": "Fall", "deadline": "December 1", "international_deadline": "December 1", "late_applications_accepted": False, "decision_timing": bi("By the end of February / early March", "Şubat sonuna / Mart başına kadar")},
            {"intake": "Spring", "deadline": "October 1", "international_deadline": "October 1", "late_applications_accepted": False, "decision_timing": bi("By mid-November", "Kasım ortasına kadar")},
        ],
        "application_deadline": bi("Fall: December 1; Spring: October 1", "Güz: 1 Aralık; Bahar: 1 Ekim"),
        "non_eu_deadline": bi("Fall: December 1; Spring: October 1", "Güz: 1 Aralık; Bahar: 1 Ekim"),
        "recommended_submission_buffer": bi("Submit at least two weeks early so recommendation links and letters can be completed before the deadline.", "Referans bağlantıları ve mektupları son tarihten önce tamamlanabilsin diye en az iki hafta erken gönderin."),
        "all_materials_due_by_deadline": True,
        "scholarship_deadline": None,
        "pre_enrolment_required": False,
        "visa_complexity": "high",
        "timeline_risk": "high",
        "verification_notes": bi("Deadlines are current department deadlines, not estimates. External fellowship deadlines are separate and often earlier.", "Tarihler tahmin değil, güncel bölüm tarihleridir. Dış burs tarihleri ayrıdır ve çoğu kez daha erkendir."),
    }

    row["research_profile"] = {
        "research_focus_areas": [
            bi("Astrodynamics and satellite navigation", "Astrodinamik ve uydu navigasyonu"),
            bi("Autonomous systems", "Otonom sistemler"),
            bi("Bioastronautics", "Biyoastronotik"),
            bi("Fluids, structures and materials", "Akışkanlar, yapılar ve malzemeler"),
            bi("Remote sensing, Earth and space sciences", "Uzaktan algılama, Dünya ve uzay bilimleri"),
        ],
        "key_institutes": ["Aerospace Mechanics Research Center (AMReC)", "BioServe Space Technologies", "Colorado Center for Astrodynamics Research (CCAR)", "Research and Engineering Center for Unmanned Vehicles (RECUV)", "Laboratory for Atmospheric and Space Physics (LASP)"],
        "named_facilities": ["LASP spacecraft engineering and mission-operations facilities", "LASP calibration laboratories", "LASP Astrophysical Research Lab and Rick Kohnert SmallSat Laboratory", "LASP IMPACT Dust Accelerator Laboratory", "180,000-square-foot Smead Aerospace Engineering Sciences Building"],
        "department_research_awards_fy2025_usd": 37300000,
        "department_patents_2015_2025": 36,
        "nasa_research_funds_public_university_position": 1,
        "research_funding_level": "very_high",
        "research_risk": "medium_for_international_project_access",
        "research_access_note": bi("Graduate-student participation is real but position, advisor, funding, skills and export-control dependent; admission alone does not guarantee a lab place.", "Lisansüstü katılım gerçektir ancak pozisyona, danışmana, finansmana, beceriye ve ihracat kontrolüne bağlıdır; kabul tek başına laboratuvar yeri garantilemez."),
        "verification_notes": bi("The department reports $37.3M in FY2025 research awards and four main aerospace centres. LASP adds end-to-end spacecraft, instrument, test and mission-operations capability.", "Bölüm FY2025 için 37,3 milyon $ araştırma ödülü ve dört ana aerospace merkezi bildirir. LASP uçtan uca uzay aracı, enstrüman, test ve görev operasyon yeteneği ekler."),
    }

    row["industry_ecosystem_profile"] = {
        "local_industry_strength": "very_high",
        "verified_partnerships": ["Lockheed Martin", "BAE Systems (formerly Ball Aerospace)", "Northrop Grumman", "Sierra Space", "Oakman Aerospace", "L3Harris / Harris"],
        "key_companies": ["Lockheed Martin Space", "BAE Systems", "Northrop Grumman", "Sierra Space", "United Launch Alliance", "Blue Canyon Technologies", "L3Harris"],
        "government_and_research_ecosystem": ["NASA", "NOAA", "National Center for Atmospheric Research", "National Institute of Standards and Technology", "National Laboratory of the Rockies", "U.S. Space Command"],
        "hiring_culture": bi("Dense aerospace cluster with research sponsorship, projects, internships and recruiting, but many defence/space roles are citizenship or export-control sensitive.", "Araştırma sponsorluğu, projeler, stajlar ve işe alımla yoğun aerospace kümesi; ancak birçok savunma/uzay rolü vatandaşlığa veya ihracat kontrolüne duyarlıdır."),
        "alumni_presence": "very_high",
        "industry_risk": "high_for_non_us_persons_in_controlled_roles",
        "export_control_policy": bi("CU states that most research qualifies for exclusions, but controlled projects can require citizenship review, licenses or laboratory/data access controls.", "CU çoğu araştırmanın istisnalara uyduğunu belirtir; ancak kontrollü projeler vatandaşlık incelemesi, lisans veya laboratuvar/veri erişim kontrolü gerektirebilir."),
        "verification_notes": bi("Named partners are taken from CU's official aerospace partnership page. Local company presence is not treated as a programme partnership unless CU confirms it.", "Adlandırılmış ortaklar CU'nun resmî aerospace ortaklık sayfasından alınmıştır. CU doğrulamadıkça yerel şirket varlığı program ortaklığı sayılmaz."),
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
        "funding_sentiment": "negative_risk_signal",
        "student_sentiment_summary": bi("A small self-selected sample consistently flags scarce first-year MS funding and uncertainty in the graduate-housing waitlist. It is insufficient for an overall satisfaction score.", "Küçük ve öz-seçimli örneklem, ilk yıl MS finansmanının kıtlığını ve lisansüstü konut bekleme listesindeki belirsizliği tutarlı biçimde işaretler. Genel memnuniyet puanı için yetersizdir."),
        "student_sentiment_sources": [REDDIT_FUNDING, REDDIT_HOUSING, REDDIT_PROGRAM],
        "sample_size_approx": 12,
        "date_range": "2020-06 to 2025-04",
        "sentiment_confidence": "low",
        "verification_notes": bi("Forum comments are used only as perceptions. Current official pages independently establish that MS funding and housing are not guaranteed.", "Forum yorumları yalnızca algı olarak kullanılır. Güncel resmî sayfalar MS finansmanı ve konutun garanti olmadığını bağımsız olarak doğrular."),
    }

    sources = [
        source(PROGRAM, "CU Boulder Smead Aerospace Traditional MS", "official_program_page", ["program", "duration", "curriculum", "funding"], "Current 30-credit, two-year, thesis/non-thesis programme structure.", "Güncel 30 kredi, iki yıl, tezli/tezsiz program yapısı."),
        source(OVERVIEW, "CU Boulder Aerospace Engineering Master's Programme", "official_program_page", ["program", "admission", "deadline", "research", "career"], "Traditional/Professional MS separation, requirements, deadlines and focus areas.", "Traditional/Professional MS ayrımı, şartlar, tarihler ve odak alanları."),
        source(CATALOG, "CU Boulder Catalog — Aerospace Engineering Sciences MS", "official_curriculum_page", ["curriculum", "courses", "duration"], "Current detailed focus-area curriculum and course options.", "Güncel ayrıntılı odak alanı müfredatı ve ders seçenekleri."),
        source(APPLY, "Smead Aerospace — How to Apply", "official_admission_page", ["admission", "documents", "gre", "decision_timeline"], "Academic background, application materials and GRE-not-accepted policy.", "Akademik geçmiş, başvuru belgeleri ve GRE kabul edilmiyor politikası."),
        source(DEADLINES, "Smead Aerospace — Deadlines and Fees", "official_admission_page", ["deadline", "application_fee", "non_eu_eligibility"], "Same Fall/Spring dates for international applicants, $80 fee and no late applications.", "Uluslararası adaylar için aynı Güz/Bahar tarihleri, 80 $ ücret ve geç başvuru yokluğu."),
        source(ENGLISH, "CU Boulder Graduate English Proficiency Requirements", "official_admission_page", ["language", "english_tests", "exemptions"], "Current tests, default thresholds, validity and exemption rules.", "Güncel sınavlar, varsayılan eşikler, geçerlilik ve muafiyet kuralları."),
        source(INTERNATIONAL, "CU Boulder Graduate International Students", "official_admission_page", ["non_eu_eligibility", "documents", "visa"], "International graduate application and immigration-document context.", "Uluslararası lisansüstü başvuru ve göçmenlik belgesi bağlamı."),
        source(FUNDING, "Smead Aerospace — Funding Your Master's/PhD", "official_scholarship_page", ["scholarship", "funding", "assistantships"], "No departmental MS funding; TF and faculty-research pathways and restrictions.", "Bölüm MS finansmanı yokluğu; TF ve öğretim üyesi araştırma yolları ve sınırları."),
        source(TUITION, "CU Boulder 2026-27 Graduate Out-of-State/International Tuition and Fees", "official_tuition_page", ["tuition", "fees", "insurance"], "Engineering tuition, mandatory fees and international/new-student charges.", "Engineering öğrenim ücreti, zorunlu ücretler ve uluslararası/yeni öğrenci kalemleri.", access_status="pdf"),
        source(COA, "CU Boulder 2026-27 Example Financial Aid Budget", "official_cost_of_living_page", ["living", "housing", "books", "transport", "medical"], "Official two-semester nonresident graduate living allowances, with Arts & Sciences tuition caveat.", "Arts & Sciences öğrenim ücreti çekincesiyle resmî iki dönem eyalet dışı lisansüstü yaşam payları."),
        source(INSURANCE, "CU Boulder Anthem Gold SHIP 2026-27", "official_university_policy_page", ["insurance", "cost"], "$2,648 per semester and current coverage/enrolment rules.", "Dönem başına 2.648 $ ve güncel kapsam/kayıt kuralları."),
        source(HOUSING_APPLICATION, "CU Boulder Graduate & Family Housing Application", "official_housing_page", ["housing", "housing_application", "fees", "guarantee"], "Timestamped waitlist, eligibility, deposits, dates and explicit non-guarantee.", "Zaman damgalı bekleme listesi, uygunluk, depozitolar, tarihler ve açık garanti yokluğu."),
        source(HOUSING_RATES, "CU Boulder Graduate & Family Housing 2026-27 Rates", "official_housing_page", ["housing", "rent"], "Current institution-owned unit and per-bedroom rates with included utilities.", "Hizmetler dâhil güncel kurum birimi ve oda başı fiyatları."),
        source(FOCUS_AREAS, "Smead Aerospace Graduate Focus Areas", "official_curriculum_page", ["curriculum", "tracks", "courses"], "Five official focus areas and their programme-role context.", "Beş resmî odak alanı ve program rolü bağlamı."),
        source(RESEARCH, "Smead Aerospace Research", "official_department_page", ["research", "labs", "funding"], "Five research areas, four centres, FY2025 awards and patents.", "Beş araştırma alanı, dört merkez, FY2025 ödülleri ve patentler."),
        source(RESEARCH_ENTITIES, "CU Boulder Aerospace Research Institutes and Entities", "official_lab_page", ["research", "labs"], "CCAR, BioServe, RECUV, LASP and broader institute mapping.", "CCAR, BioServe, RECUV, LASP ve daha geniş enstitü eşlemesi."),
        source(LASP, "LASP Labs and Facilities", "official_lab_page", ["research", "labs", "space_fit"], "Spacecraft engineering, calibration, environmental test and mission facilities.", "Uzay aracı mühendisliği, kalibrasyon, çevresel test ve görev tesisleri."),
        source(INDUSTRY, "CU Boulder Aerospace Industry Partnerships", "official_industry_partner_page", ["industry_ecosystem", "partnerships"], "Named officially confirmed aerospace partners.", "Resmen doğrulanmış adlandırılmış aerospace ortakları."),
        source(EXPORT, "CU Boulder Technology and Deemed Exports", "official_university_policy_page", ["international_risk", "research_access"], "Project-specific foreign-national review and possible access controls.", "Projeye özgü yabancı uyruklu incelemesi ve olası erişim kontrolleri."),
        source(RANKING, "CU Engineering Facts and Figures", "official_ranking_page", ["prestige", "outcomes"], "Current reported 2026-27 public graduate Engineering and aerospace ranks.", "Bildirilen güncel 2026-27 kamu lisansüstü Engineering ve aerospace sıraları."),
        source(QS, "QS World University Rankings 2027 — CU Boulder", "reliable_third_party_ranking", ["prestige"], "University-wide context only, not evidence of technical fit.", "Yalnızca üniversite geneli bağlam; teknik uyum kanıtı değil.", confidence="medium"),
        source(REDDIT_FUNDING, "Reddit — CU Boulder MS GRA availability", "student_forum", ["student_sentiment"], "Small recent anecdotal funding sample.", "Küçük ve yakın tarihli anekdotsal finansman örneklemi.", confidence="low"),
        source(REDDIT_HOUSING, "Reddit — CU Boulder graduate housing waitlist", "student_forum", ["student_sentiment"], "Small recent anecdotal housing-waitlist sample.", "Küçük ve yakın tarihli anekdotsal konut bekleme listesi örneklemi.", confidence="low"),
        source(REDDIT_PROGRAM, "Reddit — CU Boulder Aerospace MS funding experiences", "student_forum", ["student_sentiment"], "Older, larger anecdotal sample used only to contextualise funding perceptions.", "Yalnızca finansman algısını bağlamlandırmak için kullanılan eski ve daha büyük anekdotsal örneklem.", confidence="low"),
    ]

    row["source_profile"] = {
        "primary_url": PROGRAM,
        "secondary_urls": [item["url"] for item in sources[1:]],
        "last_verified": TODAY,
        "field_confidence": {
            "program_basic_info": "high",
            "program": "high",
            "language": "unknown",
            "admission": "high",
            "non_eu_eligibility": "high",
            "tuition": "high",
            "scholarship": "high",
            "deadline": "high",
            "curriculum": "high",
            "research": "high",
            "industry_ecosystem": "high",
            "housing": "high",
            "living": "high",
            "sentiment": "low",
            "prestige": "high",
        },
        "source_reliability": "high",
        "verification_status": "partially_verified",
        "needs_verification": True,
        "verification_notes": bi(
            "All core decision fields except explicit teaching language are supported by current sources. A universal private-market rent, complete-program cost, admission rate, fixed lab access and guaranteed funding are deliberately not invented.",
            "Açık eğitim dili dışındaki tüm temel karar alanları güncel kaynaklarla desteklenir. Evrensel özel piyasa kirası, tam program maliyeti, kabul oranı, sabit laboratuvar erişimi ve garantili finansman bilerek uydurulmamıştır.",
        ),
        "source_log": sources,
    }

    row["decision_summary"] = {
        "best_for": [
            bi("Students targeting astrodynamics/GNSS, space systems, bioastronautics, autonomy or Earth-space remote sensing.", "Astrodinamik/GNSS, uzay sistemleri, biyoastronotik, otonomi veya Dünya-uzay uzaktan algılamayı hedefleyen öğrenciler."),
            bi("Applicants who value LASP, CCAR, BioServe and a dense Colorado space ecosystem enough to accept a high self-funding risk.", "Yüksek öz-finansman riskini kabul edecek kadar LASP, CCAR, BioServe ve yoğun Colorado uzay ekosistemine değer veren adaylar."),
        ],
        "not_ideal_for": [
            bi("Applicants who need guaranteed MS funding before enrolment.", "Kayıttan önce garantili MS finansmanına ihtiyaç duyan adaylar."),
            bi("International applicants whose career plan depends only on export-controlled US defence/space roles.", "Kariyer planı yalnızca ihracat kontrollü ABD savunma/uzay rollerine bağlı uluslararası adaylar."),
        ],
        "main_strengths": [
            bi("Five unusually deep official focus areas with clear course requirements.", "Açık ders şartlarına sahip olağanüstü derin beş resmî odak alanı."),
            bi("LASP provides end-to-end spacecraft, instrument, test and mission-operations experience.", "LASP uçtan uca uzay aracı, enstrüman, test ve görev operasyon deneyimi sağlar."),
            bi("Top-five public graduate aerospace context and an officially verified industry cluster.", "Kamu lisansüstü aerospace alanında ilk beş bağlamı ve resmen doğrulanmış endüstri kümesi."),
        ],
        "main_risks": [
            bi("The department does not fund master's students as a standard practice; TF roles do not include tuition remission.", "Bölüm standart uygulama olarak yüksek lisans öğrencilerini finanse etmez; TF rolleri öğrenim ücreti muafiyeti içermez."),
            bi("First-year direct university charges with CU SHIP are $48,411.66 before living costs.", "CU SHIP ile birinci yıl doğrudan üniversite kalemleri yaşam giderlerinden önce 48.411,66 $'dır."),
            bi("Graduate housing is waitlist-only, requires separate fees/deposits and is not guaranteed.", "Lisansüstü konut yalnızca bekleme listelidir, ayrı ücret/depozito gerektirir ve garanti değildir."),
            bi("Export-control rules can limit foreign-national access to particular aerospace projects and roles.", "İhracat kontrolü kuralları yabancı uyrukluların belirli aerospace proje ve rollerine erişimini sınırlayabilir."),
            bi("No checked official source explicitly states the teaching language.", "Kontrol edilen hiçbir resmî kaynak eğitim dilini açıkça belirtmez."),
        ],
        "decision_summary": bi(
            "Technically, CU Boulder is one of the strongest US choices for space-oriented aerospace study, especially astrodynamics/GNSS, LASP-linked space systems, bioastronautics and remote sensing. Financially it is a high-risk MS: the correct default plan is self-funding, not an assumed RA/TA. Apply early, build a faculty/lab shortlist, submit separate funding applications and secure parallel off-campus housing options.",
            "Teknik açıdan CU Boulder, özellikle astrodinamik/GNSS, LASP bağlantılı uzay sistemleri, biyoastronotik ve uzaktan algılama için ABD'nin en güçlü uzay odaklı aerospace seçeneklerinden biridir. Finansal açıdan yüksek riskli bir MS'tir: doğru varsayılan plan RA/TA varsayımı değil öz-finansmandır. Erken başvurun, öğretim üyesi/laboratuvar kısa listesi oluşturun, ayrı finansman başvurularını yapın ve paralel kampüs dışı konut seçeneklerini güvenceye alın.",
        ),
        "pros": [],
        "cons": [],
        "verdict": bi("Exceptional space/aerospace fit, but only financially safe with a credible self-funding plan or written external/faculty support.", "Olağanüstü uzay/aerospace uyumu; ancak yalnızca güvenilir öz-finansman planı veya yazılı dış/öğretim üyesi desteğiyle finansal olarak güvenli."),
    }

    row["scoring_inputs"] = {
        "academic_prestige": None,
        "research_output": None,
        "industry_links": None,
        "affordability": None,
        "admission_chance": None,
        "living_quality": None,
        "hard_flags": ["teaching_language_unverified", "masters_funding_not_provided_by_department", "tf_has_no_tuition_remission", "housing_waitlist_not_guaranteed", "high_first_year_direct_cost", "export_control_access_project_specific"],
    }
    row["data_quality"] = {
        "status": "partial",
        "checked_official_source_count": 20,
        "verified_fields": ["program", "duration", "admission", "non_eu_eligibility", "tuition", "scholarship", "deadline", "curriculum", "research", "industry_ecosystem", "housing", "living", "insurance", "prestige"],
        "unverified_critical_fields": ["language"],
        "known_semantic_gaps": ["explicit_teaching_language", "complete_program_cost", "private_market_rent", "admission_rate", "guaranteed_individual_lab_access", "standard_ms_funding_package"],
        "has_checked_source_log": True,
        "audited_at": TODAY,
    }
    row["quality_control"] = {
        "checked_at": TODAY,
        "qc_status": "needs_revision",
        "remaining_verification_tasks": [
            bi("Find a current official source explicitly stating the Traditional MS teaching language; do not infer it from English-test rules.", "Traditional MS eğitim dilini açıkça belirten güncel resmî kaynak bulun; İngilizce sınav kurallarından çıkarım yapmayın."),
            bi("Add a complete-program cost only if CU publishes a programme-specific standard schedule including summer and completion pathway.", "Tam program maliyetini yalnızca CU yaz ve tamamlama yolunu içeren programa özgü standart çizelge yayımlarsa ekleyin."),
        ],
        "qc_notes": bi("Every discoverable core field is source-backed. The record remains partial solely because teaching language is not explicit; the other items are documented semantic gaps.", "Bulunabilen her temel alan kaynaklıdır. Kayıt yalnızca eğitim dili açık olmadığından partial kalır; diğer öğeler belgelenmiş anlamsal boşluklardır."),
        "failed_canary_tests": ["teaching_language_not_explicitly_verified"],
    }

    DATA_PATH.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    audit = {
        "record_id": row["id"],
        "checked_at": TODAY,
        "validation_method": "indexed web open/search validation; PDF content extracted for the tuition sheet",
        "audit_validity": "valid",
        "summary": {
            "total_urls": len(sources),
            "official_urls": 20,
            "reliable_third_party_urls": 1,
            "student_forum_urls": 3,
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
            "All URLs retained in the record returned accessible indexed content or an accessible PDF during this research pass. Forum URLs remain perception-only sources.",
            "Kayıtta tutulan tüm URL'ler bu araştırma turunda erişilebilir dizinlenmiş içerik veya erişilebilir PDF döndürdü. Forum URL'leri yalnızca algı kaynağıdır.",
        ),
    }
    AUDIT_PATH.parent.mkdir(parents=True, exist_ok=True)
    AUDIT_PATH.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"id": row["id"], "status": row["data_quality"]["status"], "source_count": len(sources), "official_source_count": row["data_quality"]["checked_official_source_count"], "unverified": row["data_quality"]["unverified_critical_fields"]}, indent=2))


if __name__ == "__main__":
    main()
