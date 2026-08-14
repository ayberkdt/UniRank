from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data_base" / "amerika.json"
AUDIT_PATH = ROOT / "reports" / "source_link_audit_stanford_aa_ms_2026-08-14.json"
TODAY = "2026-08-14"

ADMISSION = "https://aa.stanford.edu/academics-admissions/graduate-admissions/masters-admissions"
FAQ = "https://aa.stanford.edu/academics-admissions/graduate-admissions/admissions-frequently-asked-questions"
CURRICULUM = "https://aa.stanford.edu/academics-admissions/graduate-programs/masters-program"
TESTS = "https://gradadmissions.stanford.edu/apply/test-scores"
GRAD_FAQ = "https://gradadmissions.stanford.edu/apply/faq"
FEE_WAIVER = "https://engineering.stanford.edu/prospective-graduate-programs/fee-waivers"
TUITION = "https://studentservices.stanford.edu/tuition-rates/2026-2027-graduate-and-professional-tuition-rates"
BUDGET = "https://financialaid.stanford.edu/grad/budget/index.html"
INSURANCE = "https://vaden.stanford.edu/news/cardinal-caredependent-care-premium-rates-2026-2027"
FUNDING = "https://aa.stanford.edu/academics-admissions/financial-aid"
ASSISTANTSHIPS = "https://aa.stanford.edu/academics-admissions/financial-aid/assistantships"
HOUSING_PRIORITY = "https://rde.stanford.edu/studenthousing/assignment-guarantee-and-priorities"
HOUSING_RATES = "https://rde.stanford.edu/studenthousing/graduate-housing-rates-and-billing-information"
HOUSING_SINGLE = "https://rde.stanford.edu/studenthousing/residences-single-graduates"
HOUSING_RANGE = "https://rde.stanford.edu/sites/default/files/2024-11/2025-26_2026-27_Grad_Rate-Ranges_Chart.pdf?t=20260306210842"
RESEARCH = "https://aa.stanford.edu/research-impact"
LABS = "https://aa.stanford.edu/research-impact/labs-and-centers"
EXPORT = "https://global.stanford.edu/plan-your-global-activity/legal/export-controls"
VISA = "https://bechtel.stanford.edu/navigate-international-life/visas/f-1-and-j-1-student-visas"
I20 = "https://bechtel.stanford.edu/navigate-international-life/visas/f-1-and-j-1-student-visas/how-request-initial-i-20-or-ds-2019"
QS = "https://www.topuniversities.com/universities/stanford-university"

REDDIT_AA = "https://www.reddit.com/r/stanford/comments/fzadb3"
REDDIT_HOUSING_2025 = "https://www.reddit.com/r/stanford/comments/1k6i32u"
REDDIT_HOUSING_2026 = "https://www.reddit.com/r/stanford/comments/1srdy4u"


def bi(en: str, tr: str) -> dict[str, str]:
    return {"en": en, "tr": tr}


def source(url: str, title: str, kind: str, fields: list[str], en: str, tr: str, *, confidence: str = "high", access_status: str = "ok") -> dict:
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
    row = next(item for item in records if item.get("id") == "stanford-aa")

    row.update({
        "country": "United States",
        "university": "Stanford University",
        "university_native_name": "Stanford University",
        "city": "Stanford",
        "region": "California",
        "program_name": "Master of Science in Aeronautics and Astronautics",
        "program_native_name": "Master of Science in Aeronautics and Astronautics",
        "program_degree": "MS",
        "degree_level": "Master",
        "duration_years": None,
        "duration": bi("Normally four to five academic quarters; Stanford does not express this variable duration as one fixed number of years.", "Normalde dört ila beş akademik çeyrek; Stanford bu değişken süreyi tek bir sabit yıl sayısı olarak ifade etmez."),
        "ects": None,
        "us_quarter_units": 45,
        "teaching_language": ["English"],
        "program_url": ADMISSION,
        "program_status": "active",
        "relevance_status": "strong",
        "delivery_modes": ["on_campus"],
        "full_time_available": True,
        "part_time_available": True,
        "qs_ranking": 2,
        "qs_ranking_display": "#=2",
        "qs_ranking_year": 2027,
    })

    row["prestige_profile"] = {
        "qs_world_rank": 2,
        "qs_rank_is_tied": True,
        "qs_edition": 2027,
        "qs_source_url": QS,
        "interpretation": bi("The QS institutional rank is prestige context only. Technical fit is evidenced separately through the AA curriculum, seven research themes, and named laboratories.", "QS kurum sırası yalnızca prestij bağlamıdır. Teknik uygunluk AA müfredatı, yedi araştırma teması ve isimli laboratuvarlarla ayrıca kanıtlanır."),
    }

    row["eligibility_profile"] = {
        "eligible_for_non_eu": True,
        "required_previous_degree": bi("A recognized US bachelor's degree or international equivalent completed before enrolment.", "Kayıttan önce tamamlanmış tanınan bir ABD lisans derecesi veya uluslararası eşdeğeri."),
        "accepted_backgrounds": [bi("Engineering", "Mühendislik"), bi("Physics", "Fizik"), bi("Comparable science discipline with strong technical preparation", "Güçlü teknik hazırlığa sahip karşılaştırılabilir bilim alanı")],
        "aerospace_or_mechanical_degree_required": False,
        "non_engineering_applicants_disadvantaged": True,
        "prior_related_masters_restriction": bi("Applicants who already hold an MS or equivalent advanced degree in AA or a closely related discipline are not eligible for another Stanford AA-MS; materially non-overlapping prior graduate work may be reviewed.", "AA veya çok yakın bir alanda zaten MS ya da eşdeğer ileri derece sahibi adaylar ikinci bir Stanford AA-MS için uygun değildir; önemli ölçüde örtüşmeyen önceki lisansüstü çalışma incelenebilir."),
        "minimum_gpa": None,
        "official_average_admitted_gpa_published": False,
        "admission_mode": "direct_department_application",
        "admission_risk": "high",
        "one_stanford_graduate_program_per_year": True,
        "interview_required": False,
        "interview_policy": "not_published_as_required",
        "required_documents": [
            bi("Online graduate application", "Çevrim içi lisansüstü başvurusu"),
            bi("Statement of purpose, no more than two single-spaced pages", "En fazla iki tek aralıklı sayfalık amaç beyanı"),
            bi("Unofficial transcript from every post-secondary degree institution", "Derece programına devam edilen her yükseköğretim kurumundan resmî olmayan transkript"),
            bi("Exactly three recommendation letters; at least one academic and preferably two", "Tam olarak üç referans mektubu; en az biri akademik, tercihen ikisi"),
            bi("TOEFL iBT or IELTS Academic when no exemption applies", "Muafiyet yoksa TOEFL iBT veya IELTS Academic"),
        ],
        "recommendation_letter_count": 3,
        "academic_recommendation_minimum": 1,
        "academic_recommendation_preferred": 2,
        "interfolio_accepted": False,
        "official_transcripts_required_at_application": False,
        "official_transcripts_required_after_acceptance": True,
        "english_translation_required_for_non_english_transcripts": True,
        "wes_required_at_application": False,
        "wes_may_be_required_after_acceptance": True,
        "application_fee_usd": 125,
        "application_fee_refundable": False,
        "application_fee_waiver_possible": True,
        "application_fee_waiver_safe_lead_time_business_days": 10,
        "application_fee_waiver_international_eligibility": None,
        "gre": {"policy": "not_required_and_not_considered", "test_type": "GRE General", "required": False, "considered_if_submitted": False, "minimum_scores": {}, "source_ids": [FAQ, TESTS]},
        "deferral_policy": "not_normally_permitted_case_by_case_extenuating_only",
        "verification_notes": bi("No minimum GPA, acceptance rate, interview rule, or international fee-waiver entitlement is published for AA-MS; these remain null rather than estimated.", "AA-MS için asgari GNO, kabul oranı, mülakat kuralı veya uluslararası ücret muafiyeti hakkı yayımlanmamıştır; tahmin edilmek yerine null bırakılır."),
    }

    row["language_profile"] = {
        "teaching_language": ["English"],
        "teaching_languages": ["English"],
        "english_required": True,
        "teaching_language_evidence_type": "operational_department_requirement_not_separate_instruction_language_label",
        "accepted_english_tests": [
            {"test": "TOEFL iBT", "minimum_score": 90, "minimum_score_2026_scale": 4.5, "minimum_score_policy": {"before_2026_01_21": 90, "on_or_after_2026_01_21": 4.5}, "mybest_accepted": True, "institution_code": "4704"},
            {"test": "IELTS Academic", "minimum_score": 7.0},
        ],
        "minimum_scores": {"toefl_before_2026_01_21": 90, "toefl_on_or_after_2026_01_21": 4.5, "ielts_academic": 7.0},
        "score_validity_years": 2,
        "fall_2027_earliest_valid_test_date": "2024-09-01",
        "placement_test_exemption_scores": {"toefl_before_2026_01_21": 109, "toefl_on_or_after_2026_01_21": 5.5, "ielts_academic": 8.0},
        "placement_test_possible_below_exemption_threshold": True,
        "waiver_automatic": True,
        "waiver_routes": [
            bi("US citizen or permanent resident", "ABD vatandaşı veya daimî oturum sahibi"),
            bi("First language is English", "İlk dil İngilizce"),
            bi("Recognized degree where all instruction was in English", "Tüm öğretimin İngilizce olduğu tanınan derece"),
            bi("At least 24 consecutive full-time months of professional or educational experience entirely in English within the past ten years", "Son on yılda bütünüyle İngilizce yürütülen en az 24 ardışık tam zamanlı aylık mesleki veya eğitim deneyimi"),
        ],
        "language_risk": "medium",
        "verification_notes": bi("The central 2026-scale TOEFL table supersedes the older score wording still visible in parts of the department FAQ. Stanford does not publish a separate AA-MS 'language of instruction' label, so teaching-language confidence remains medium.", "Merkezî 2026 ölçekli TOEFL tablosu bölüm SSS'sinin bazı kısımlarında kalan eski puan ifadesinin yerine geçer. Stanford ayrı bir AA-MS 'eğitim dili' etiketi yayımlamadığından eğitim dili güveni orta düzeyde kalır."),
    }

    row["cost_profile"] = {
        "academic_year": "2026/2027",
        "currency": "USD",
        "engineering_tuition_usd_per_quarter_11_to_18_units": 23239,
        "engineering_tuition_usd_per_quarter_8_to_10_units": 15100,
        "engineering_tuition_usd_per_unit_above_18": 1549,
        "summer_tuition_usd_per_unit_1_to_7": 1510,
        "three_quarter_standard_tuition_example_usd": 69717,
        "tuition_usd_per_year_at_three_quarters": 69717,
        "campus_health_service_fee_usd_per_quarter": 281,
        "campus_health_service_fee_usd_three_quarters": 843,
        "mandatory_fees_usd_per_year": 843,
        "cardinal_care_usd_per_year": 8808,
        "health_insurance_premium_usd": 8808,
        "health_insurance_required": True,
        "cardinal_care_automatic_enrollment": True,
        "cardinal_care_waiver_possible_with_qualifying_coverage": True,
        "first_academic_year_direct_charges_example_usd": 79368,
        "first_year_tuition_and_mandatory_fees_usd_example": 70560,
        "first_year_direct_university_cost_with_ship_usd": 79368,
        "non_tuition_standard_budget_usd_three_quarters": 49116,
        "non_tuition_standard_budget_usd_12_months": 61142,
        "total_coa_usd_three_quarters_example": 118833,
        "total_cost_of_attendance_usd_per_year": 118833,
        "coa_is_invoice": False,
        "coa_rent_usd_three_quarters": 20055,
        "coa_food_usd_three_quarters": 7710,
        "coa_personal_usd_three_quarters": 9135,
        "coa_transportation_usd_three_quarters": 1980,
        "coa_books_usd_three_quarters": 585,
        "off_campus_living_expected_percent_higher_min": 10,
        "off_campus_living_expected_percent_higher_max": 40,
        "complete_program_cost_usd": None,
        "complete_program_cost_reason": bi("Completion takes four or five quarters, and tuition category changes with assistantship load and summer enrolment; Stanford publishes no single AA-MS total.", "Tamamlama dört veya beş çeyrek sürer; asistanlık ders yükü ve yaz kaydıyla ücret kategorisi değişir. Stanford tek bir AA-MS toplamı yayımlamaz."),
        "tuition_eur_per_year_min": None,
        "tuition_eur_per_year_max": None,
        "tuition_eur_per_year_estimated": None,
        "scholarship_availability": "available_highly_competitive",
        "scholarship_risk": "high",
        "verification_notes": bi("The 118,833 USD example combines three standard 11–18-unit Engineering quarters with the official three-quarter non-tuition budget. It is a planning example before aid, not a programme invoice.", "118.833 USD örneği, 11–18 birimlik üç standart Mühendislik çeyreğini resmî üç çeyreklik öğrenim dışı bütçeyle birleştirir. Destek öncesi planlama örneğidir, program faturası değildir."),
    }

    row["scholarship_profile"] = {
        "available_types": ["departmental_fellowship", "research_assistantship", "course_or_teaching_assistantship", "Knight-Hennessy Scholars", "external_fellowship"],
        "non_eu_eligible": None,
        "application_mode": "mixed",
        "automatic_consideration": True,
        "separate_application_required": True,
        "automatic_consideration_scope": bi("Departmental entering fellowships use the completed graduate application; no extra form.", "Bölümün giriş fellowship'leri tamamlanmış lisansüstü başvurusunu kullanır; ek form yoktur."),
        "separate_application_scope": bi("Knight-Hennessy requires a separate application; current-student CA positions use posted applications and RAs are arranged with individual faculty.", "Knight-Hennessy ayrı başvuru ister; mevcut öğrenci CA pozisyonları ilanlı başvuru kullanır, RA'lar bireysel öğretim üyeleriyle ayarlanır."),
        "funding_guaranteed_at_admission": False,
        "ms_students_typically_department_funded": False,
        "first_year_ms_assistantship_rare": True,
        "self_funding_first_quarters_should_be_planned": True,
        "departmental_fellowship_notification_window": "March-April",
        "departmental_fellowship_typical_duration_academic_years": 1,
        "departmental_fellowship_tuition_scope": "8-10 unit rate",
        "departmental_fellowship_living_stipend": True,
        "assistantship_typical_fte_percent": 50,
        "assistantship_typical_hours_per_week": 20,
        "assistantship_tuition_coverage_units": "8-10",
        "assistantship_salary_included": True,
        "knight_hennessy_any_country": True,
        "knight_hennessy_deadline": "2026-10-06 13:00 PT",
        "knight_hennessy_max_funding_years": 3,
        "opportunities": [
            {"name": "Stanford AA entering fellowship", "automatic": True, "separate_application": False, "international_eligibility": None, "deadline": "2026-12-01"},
            {"name": "Knight-Hennessy Scholars", "automatic": False, "separate_application": True, "international_eligibility": True, "deadline": "2026-10-06 13:00 PT"},
            {"name": "Research assistantship", "automatic": False, "separate_application": True, "international_eligibility": None, "deadline": None},
            {"name": "Course/teaching assistantship", "automatic": False, "separate_application": True, "international_eligibility": None, "deadline": None},
        ],
        "verification_notes": bi("Automatic fellowship review does not mean an award is likely. AA explicitly says incoming RAs and first-year MS assistantships are rare; international eligibility is opportunity-specific and is null unless stated.", "Otomatik fellowship değerlendirmesi ödülün olası olduğu anlamına gelmez. AA giriş RA'larının ve birinci yıl MS asistanlıklarının nadir olduğunu açıkça belirtir; uluslararası uygunluk fırsata özeldir ve belirtilmedikçe null'dır."),
    }

    row["living_profile"] = {
        "city_type": "high_cost_university_region",
        "housing_search_difficulty": "high",
        "housing_access": "guaranteed",
        "housing_guarantee_type": "conditional_first_year_guarantee",
        "housing_application_separate": True,
        "housing_guaranteed": True,
        "housing_guarantee_conditions": bi("First-time Stanford graduate students must apply by the first-round/lottery deadline and be willing to accept any eligible option. Refusing an assignment forfeits the guaranteed year.", "Stanford'da ilk kez lisansüstü programa başlayanlar ilk tur/lotarya son tarihine kadar başvurmalı ve uygun herhangi bir seçeneği kabul etmeye istekli olmalıdır. Atamayı reddetmek garantili yılı kaybettirir."),
        "fall_2027_housing_deadline": None,
        "latest_published_benchmark_housing_deadline": "2026-04-30",
        "latest_published_benchmark_cycle": "2026/2027",
        "housing_notes": bi("The guarantee applies only to first-time graduate students who meet the separate first-round deadline and accept any eligible option; it is not automatic with admission.", "Garanti yalnızca ayrı ilk tur son tarihini karşılayan ve uygun herhangi bir seçeneği kabul eden ilk kez lisansüstü öğrencilere uygulanır; kabulle otomatik değildir."),
        "monthly_housing_rent_usd_per_month_min": 1203,
        "monthly_housing_rent_usd_per_month_max": 3014,
        "rent_scope": "2026/27 university housing range for single graduate students",
        "furnished": True,
        "utilities_included": ["water", "heat", "electricity", "garbage", "sewer", "internet"],
        "on_campus_laundry_included": True,
        "additional_house_mail_technology_fees_possible": True,
        "official_rent_budget_usd_three_quarters": 20055,
        "living_cost_risk": "high",
        "living_risk": "high",
        "verification_notes": bi("The first-year guarantee is conditional, not automatic with admission. The published rent range is not a promise of the applicant's preferred unit. Stanford estimates off-campus living at 10–40% above the standard allowance.", "İlk yıl garantisi kabulle otomatik değildir, koşulludur. Yayımlanan kira aralığı adayın tercih ettiği birimin garantisi değildir. Stanford kampüs dışı yaşamın standart ödenekten %10–40 daha yüksek olabileceğini belirtir."),
    }

    row["curriculum_profile"] = {
        "quarter_units_total": 45,
        "duration_quarters_minimum": 4,
        "duration_quarters_maximum": 5,
        "course_count_fixed": False,
        "course_count": None,
        "course_count_summary": bi("45 quarter units: 5 basic-core courses, 3 advanced AA-core courses, 2 mathematics courses, at least 4 technical electives (12+ units), and 3 other-elective units; the exact total course count varies.", "45 çeyrek birimi: 5 temel çekirdek ders, 3 ileri AA çekirdek ders, 2 matematik dersi, en az 4 teknik seçmeli (12+ birim) ve 3 diğer seçmeli birimi; kesin toplam ders sayısı değişir."),
        "course_count_reason": bi("Stanford fixes unit, breadth, mathematics and elective requirements, but variable-unit courses and research make one exact total course count invalid.", "Stanford birim, genişlik, matematik ve seçmeli şartlarını sabitler; değişken birimli dersler ve araştırma tek bir kesin ders sayısını geçersiz kılar."),
        "basic_core_breadth_course_count": 5,
        "basic_core_areas": ["fluids", "structures", "guidance_and_controls", "propulsion", "experimentation_or_design"],
        "advanced_aa_core_course_count": 3,
        "advanced_aa_core_minimum_units_each": 3,
        "mathematics_course_count": 2,
        "mathematics_units_minimum": 6,
        "technical_elective_course_count_minimum": 4,
        "technical_elective_units_minimum": 12,
        "other_elective_units": 3,
        "program_proposal_due": "last day of classes in first quarter",
        "minimum_graduation_gpa": 2.75,
        "courses_minimum_level": 100,
        "letter_grade_required_except": ["seminars", "free_elective"],
        "thesis_required": False,
        "thesis_route_available": False,
        "research_required": False,
        "research_optional": True,
        "standard_ms_research_units_maximum": 6,
        "distinction_in_research_available": True,
        "distinction_research_units_minimum": 9,
        "distinction_research_units_maximum": 12,
        "distinction_research_quarters_minimum": 3,
        "distinction_research_minimum_grade_each": "B+",
        "distinction_research_report_required": True,
        "distinction_shown_on_transcript_or_diploma": False,
        "internship_required": False,
        "full_online_completion_possible": False,
        "part_time_hcp_available": True,
        "part_time_hcp_local_employment_recommended": True,
        "international_minimum_units_per_quarter_typical": 8,
        "i20_or_ds2019_issued_timeframe_years": 2,
        "general_completion_limit_years": 3,
        "general_completion_limit_units": 60,
        "verification_notes": bi("The standard MS is course-based and has no thesis or research requirement. Distinction in Research is optional, requires a faculty arrangement, and produces a department certificate rather than a transcript/diploma notation.", "Standart MS ders temellidir ve tez ya da araştırma zorunluluğu yoktur. Research Distinction isteğe bağlıdır, öğretim üyesi düzenlemesi gerektirir ve transkript/diploma kaydı yerine bölüm sertifikası üretir."),
    }

    row["category_profile"] = {
        "primary_categories": ["aerospace_engineering", "space_engineering"],
        "secondary_categories": ["autonomous_systems_controls", "distributed_space_systems", "future_aircraft_design", "computational_aerosciences", "multifunctional_materials_structures", "planetary_exploration", "propulsion_energy_conversion"],
        "technical_focus": bi("Broad aerospace core with selectable depth across aircraft, autonomy, computation, structures, propulsion, space systems and planetary exploration.", "Uçak, otonomi, hesaplama, yapılar, itki, uzay sistemleri ve gezegen keşfinde seçilebilir derinliğe sahip geniş havacılık-uzay çekirdeği."),
        "verification_notes": bi("Categories are normalized from the department's seven official research groups and the published MS breadth structure; they are not inferred from university rank.", "Kategoriler bölümün yedi resmî araştırma grubu ve yayımlanan MS genişlik yapısından normalize edilmiştir; üniversite sırasından çıkarılmamıştır."),
    }

    row["research_profile"] = {
        "research_focus_areas": ["Autonomous Systems and Controls", "Cyber Safety for Transportation", "Distributed Space Systems", "Future Aircraft Design", "Multidisciplinary Computational Aerosciences", "Multifunctional Materials and Intelligent Structures", "Planetary Science and Exploration", "Propulsion and Energy Conversion Systems"],
        "key_institutes": [
            "Aerospace Design Laboratory",
            "Aerospace Planetary Exploration Laboratory (APEX)",
            "Autonomous Systems Lab",
            "Experimental and Computational Laboratory for Impacts, Plasmas and Space Environments (ECLIPSE)",
            "Flow Physics and Aeroacoustics Laboratory",
            "GPS Laboratory",
            "Space Rendezvous Laboratory",
            "Space Environment and Satellite Systems Laboratory",
        ],
        "individual_lab_place_guaranteed": False,
        "research_required_for_standard_ms": False,
        "faculty_arrangement_required_for_optional_research": True,
        "research_access_risk": "medium",
        "verification_notes": bi("Named labs establish capacity, not an individual place. Standard MS students must arrange optional AA 290 research with faculty; admission itself carries no lab guarantee.", "İsimli laboratuvarlar kapasiteyi kanıtlar, kişisel yeri değil. Standart MS öğrencileri isteğe bağlı AA 290 araştırmasını öğretim üyeleriyle ayarlamalıdır; kabul laboratuvar garantisi taşımaz."),
    }

    row["industry_ecosystem_profile"] = {
        "local_industry_strength": "high",
        "verified_partnerships": [],
        "key_companies": [],
        "hiring_culture": "competitive_and_project_dependent",
        "export_control_risk": "project_specific",
        "international_student_research_access_guaranteed": False,
        "verification_notes": bi("No company is recorded as a programme partnership without bilateral official confirmation. Stanford says most activity benefits from the fundamental-research exclusion, but EAR/ITAR compliance can still affect particular research, technology, travel or restricted-party situations.", "İki taraflı resmî teyit olmadan hiçbir şirket program ortaklığı olarak kaydedilmez. Stanford çoğu faaliyetin temel araştırma istisnasından yararlandığını belirtir; ancak EAR/ITAR belirli araştırma, teknoloji, seyahat veya kısıtlı taraf durumlarını etkileyebilir."),
    }

    row["application_timeline_profile"] = {
        "application_rounds": [{"intake": "Autumn 2027", "opens": "2026-09", "deadline": "2026-12-01", "deadline_time": None, "gre_required": False, "all_materials_due_by_deadline": True}],
        "application_period": "September 2026-December 1, 2026",
        "deadline_eu": "2026-12-01",
        "deadline_non_eu": "2026-12-01",
        "late_applications_accepted": False,
        "spring_admission_available": False,
        "decision_window": "February to mid-April 2027",
        "decision_timing_source_discrepancy": bi("The department FAQ says decisions begin in February and continue to mid-April; the admissions page says review begins in March.", "Bölüm SSS'si kararların Şubat'ta başlayıp Nisan ortasına sürdüğünü, kabul sayfası ise incelemenin Mart'ta başladığını belirtir."),
        "pre_enrollment_required": False,
        "scholarship_deadline": bi("Knight-Hennessy: 2026-10-06 13:00 PT; automatic AA entering-fellowship review: programme deadline 2026-12-01.", "Knight-Hennessy: 2026-10-06 13:00 PT; otomatik AA giriş fellowship değerlendirmesi: program son tarihi 2026-12-01."),
        "document_completion_deadline": "2026-12-01",
        "financial_proof_required_with_application": False,
        "financial_proof_required_after_acceptance_for_visa": True,
        "visa_document_route": "Bechtel Connect after accepting admission",
        "visa_document_request_system": "Bechtel Connect after accepting admission",
        "visa_documents": ["F-1 I-20", "J-1 DS-2019"],
        "f1_financial_proof_scope": "nine_months",
        "j1_financial_proof_scope": "entire_term_of_study",
        "financial_proof_required_before_i20_or_ds2019": True,
        "financial_proof_amount_location": bi("the Bechtel financial budget shown after admission", "kabul sonrası gösterilen Bechtel mali bütçesinde"),
        "visa_document_processing_time_business_days": None,
        "visa_document_processing_time_reason": bi("The current initial-document page publishes the workflow but no processing-time promise.", "Güncel ilk belge sayfası iş akışını yayımlar, ancak işlem süresi taahhüdü vermez."),
        "timeline_risk": "high",
        "verification_notes": bi("December 1 is a hard final deadline for the only full-time cycle. Housing and Knight-Hennessy have separate timelines; the Fall 2027 housing deadline is not yet published.", "1 Aralık tek tam zamanlı dönem için kesin son tarihtir. Konut ve Knight-Hennessy ayrı takvimlere sahiptir; 2027 Güz konut son tarihi henüz yayımlanmamıştır."),
    }

    row["student_sentiment_profile"] = {
        "student_satisfaction_score": None,
        "workload_sentiment": "unknown",
        "teaching_quality_sentiment": "unknown",
        "administration_sentiment": "mixed_low_sample",
        "housing_sentiment": "mixed_low_sample",
        "city_life_sentiment": "unknown",
        "international_student_sentiment": "unknown",
        "career_support_sentiment": "unknown",
        "student_sentiment_summary": bi("A very small, non-representative sample repeatedly mentions expensive or compact housing, variable residence atmosphere and scarce early MS funding, alongside positive comments about campus integration and research opportunity. These are perceptions only.", "Çok küçük ve temsil gücü olmayan örneklem; pahalı veya sıkışık konut, değişken yurt atmosferi ve erken MS finansman kıtlığını tekrar ederken kampüs bütünleşmesi ve araştırma fırsatları hakkında olumlu yorumlar da içerir. Bunlar yalnızca algıdır."),
        "student_sentiment_sources": [REDDIT_AA, REDDIT_HOUSING_2025, REDDIT_HOUSING_2026],
        "approximate_sample_size": "fewer_than_25_visible_comments_across_three_threads",
        "date_range": "2020-2026",
        "sentiment_confidence": "low",
        "verification_notes": bi("No score is calculated because the sample is small, self-selected and not AA-MS-specific enough across all dimensions.", "Örneklem küçük, kendi seçilmiş ve tüm boyutlarda yeterince AA-MS'e özgü olmadığından puan hesaplanmaz."),
    }

    sources = [
        source(ADMISSION, "Stanford AA Master's Admissions", "official_admission_page", ["program", "admission", "eligibility", "documents", "deadline", "funding"], "Current Autumn 2027 route, eligibility, documents, fee and deadline.", "Güncel 2027 Güz yolu, uygunluk, belgeler, ücret ve son tarih."),
        source(FAQ, "Stanford AA Admissions FAQ", "official_admission_page", ["admission", "eligibility", "gre", "decisions", "funding", "part_time"], "Current restrictions, GRE policy, decision window and rare first-year MS assistantships.", "Güncel kısıtlar, GRE politikası, karar aralığı ve nadir birinci yıl MS asistanlıkları."),
        source(CURRICULUM, "Stanford AA Master's Program", "official_curriculum_page", ["curriculum", "duration", "research", "part_time"], "Current 45-unit requirements, four-to-five-quarter duration and optional research distinction.", "Güncel 45 birim şartları, dört-beş çeyrek süre ve isteğe bağlı araştırma ayrımı."),
        source(TESTS, "Stanford Graduate Admissions Test Scores", "official_admission_page", ["language", "english_test", "gre"], "Current 2026 TOEFL scale, IELTS minimum, exemptions, validity and placement-test thresholds.", "Güncel 2026 TOEFL ölçeği, IELTS asgarisi, muafiyetler, geçerlilik ve yerleştirme sınavı eşikleri."),
        source(GRAD_FAQ, "Stanford Graduate Admissions FAQ", "official_admission_page", ["eligibility", "transcripts", "fee", "language", "funding", "visa"], "Current central application, fee, transcript, funding and post-admission financial-proof rules.", "Güncel merkezî başvuru, ücret, transkript, finansman ve kabul sonrası mali kanıt kuralları."),
        source(FEE_WAIVER, "Stanford Engineering Graduate Fee Waivers", "official_admission_page", ["application_fee_waiver"], "Official waiver routes and ten-business-day lead-time guidance.", "Resmî muafiyet yolları ve on iş günü önceden başvuru rehberi."),
        source(TUITION, "Stanford 2026-27 Graduate Engineering Tuition", "official_tuition_page", ["tuition", "fees"], "Current Engineering tuition bands and per-unit rates.", "Güncel Mühendislik ücret dilimleri ve birim başına fiyatlar."),
        source(BUDGET, "Stanford 2026-27 Graduate Student Budget", "official_cost_of_living_page", ["cost", "living", "housing", "insurance"], "Current three-quarter and twelve-month non-tuition planning budgets.", "Güncel üç çeyreklik ve on iki aylık öğrenim dışı planlama bütçeleri."),
        source(INSURANCE, "Stanford Cardinal Care 2026-27 Premium", "official_tuition_page", ["insurance", "fees"], "Current annual student premium.", "Güncel yıllık öğrenci primi."),
        source(FUNDING, "Stanford AA Financial Aid", "official_scholarship_page", ["scholarship", "assistantship", "funding"], "Department fellowships, automatic review, rare incoming RA and assistantship coverage.", "Bölüm fellowship'leri, otomatik değerlendirme, nadir giriş RA'sı ve asistanlık kapsamı."),
        source(ASSISTANTSHIPS, "Stanford AA Assistantships", "official_scholarship_page", ["assistantship", "tuition_coverage", "workload"], "Current RA/CA selection and tuition-grant mechanics.", "Güncel RA/CA seçimi ve öğrenim desteği mekanikleri."),
        source(HOUSING_PRIORITY, "Stanford Graduate Housing Guarantee and Priorities", "official_housing_page", ["housing", "guarantee", "deadline"], "Conditional first-year guarantee and priority rules.", "Koşullu ilk yıl garantisi ve öncelik kuralları."),
        source(HOUSING_RATES, "Stanford Graduate Housing 2026-27 Rates and Billing", "official_housing_page", ["housing", "rent", "utilities"], "Current billing periods and included services.", "Güncel faturalama dönemleri ve dâhil hizmetler."),
        source(HOUSING_SINGLE, "Stanford Residences for Single Graduates", "official_housing_page", ["housing", "eligibility", "rent"], "Current single-graduate options and rates.", "Güncel tek lisansüstü öğrenci seçenekleri ve fiyatları."),
        source(HOUSING_RANGE, "Stanford 2026-27 Graduate Housing Rate Ranges", "official_housing_page", ["housing", "rent"], "Official single-student minimum and maximum monthly ranges.", "Resmî tek öğrenci aylık alt ve üst fiyat aralıkları.", access_status="pdf"),
        source(RESEARCH, "Stanford AA Research and Impact", "official_department_page", ["research", "categories"], "Current department research themes.", "Güncel bölüm araştırma temaları."),
        source(LABS, "Stanford AA Labs and Centers", "official_lab_page", ["research", "labs"], "Current named laboratory and centre inventory.", "Güncel isimli laboratuvar ve merkez envanteri."),
        source(EXPORT, "Stanford Export Controls", "official_university_policy_page", ["export_control", "research_access"], "Institutional EAR/ITAR and fundamental-research guidance.", "Kurumsal EAR/ITAR ve temel araştırma rehberi."),
        source(VISA, "Stanford F-1 and J-1 Student Visas", "official_visa_or_government_page", ["visa", "financial_proof", "employment"], "Current visa-document, financial-proof and entry rules.", "Güncel vize belgesi, mali kanıt ve giriş kuralları."),
        source(I20, "Stanford Initial I-20 or DS-2019 Request", "official_visa_or_government_page", ["visa", "i20", "documents"], "Post-acceptance Bechtel Connect workflow and required uploads.", "Kabul sonrası Bechtel Connect iş akışı ve gerekli yüklemeler."),
        source(QS, "QS Stanford University 2027", "official_ranking_page", ["prestige"], "QS 2027 tied institutional rank; not evidence of AA technical fit.", "QS 2027 eşit kurum sırası; AA teknik uygunluğunun kanıtı değildir.", confidence="medium"),
        source(REDDIT_AA, "Reddit: Stanford AA funding discussion", "student_forum", ["student_sentiment"], "Older, small anecdotal AA funding and research-opportunity sample.", "Eski, küçük ve anekdotsal AA finansman ve araştırma fırsatı örneklemi.", confidence="low"),
        source(REDDIT_HOUSING_2025, "Reddit: Stanford graduate housing recommendations", "student_forum", ["student_sentiment"], "Small 2025 housing-perception sample.", "Küçük 2025 konut algısı örneklemi.", confidence="low"),
        source(REDDIT_HOUSING_2026, "Reddit: Stanford graduate housing discussion", "student_forum", ["student_sentiment"], "Small 2026 housing and campus-integration sample.", "Küçük 2026 konut ve kampüs bütünleşmesi örneklemi.", confidence="low"),
    ]

    field_confidence = {
        "program": "high", "degree": "high", "duration": "high", "ects": "unknown", "language": "medium",
        "eligibility": "high", "admission": "high", "gre": "high", "english_test": "high", "tuition": "high",
        "scholarship": "high", "living_profile": "high", "housing": "high", "curriculum": "high", "research": "high",
        "industry_ecosystem": "medium", "deadline": "high", "visa": "high", "student_sentiment": "low", "prestige": "medium",
    }
    row["source_profile"] = {
        "primary_url": ADMISSION,
        "official_admission_page": ADMISSION,
        "official_curriculum_page": CURRICULUM,
        "official_tuition_page": TUITION,
        "official_scholarship_page": FUNDING,
        "official_housing_page": HOUSING_PRIORITY,
        "official_research_page": RESEARCH,
        "official_visa_page": VISA,
        "secondary_urls": [item["url"] for item in sources[1:]],
        "last_verified": TODAY,
        "field_confidence": field_confidence,
        "source_reliability": "high",
        "verification_status": "partial",
        "needs_verification": True,
        "verification_notes": bi("Fall 2027 housing deadline, a direct language-of-instruction label, exact complete-program cost, programme-specific visa funding amount and universal international funding eligibility remain unpublished or variable.", "2027 Güz konut son tarihi, doğrudan eğitim dili etiketi, kesin tam program maliyeti, programa özgü vize mali kanıt tutarı ve evrensel uluslararası finansman uygunluğu yayımlanmamış veya değişkendir."),
        "source_log": sources,
    }

    row["decision_summary"] = {
        "pros": [
            bi("Exceptionally broad verified aerospace and space research infrastructure with a compact, flexible 45-unit curriculum.", "Kompakt ve esnek 45 birimlik müfredatla olağanüstü geniş, doğrulanmış havacılık ve uzay araştırma altyapısı."),
            bi("Conditional first-year university-housing guarantee can materially reduce arrival risk when its separate deadline and acceptance conditions are met.", "Ayrı son tarih ve kabul koşulları sağlanırsa koşullu ilk yıl üniversite konutu garantisi varış riskini önemli ölçüde azaltabilir."),
            bi("No GRE consideration; clear 2027 deadline and current English-test scale.", "GRE değerlendirmesi yok; 2027 son tarihi ve güncel İngilizce sınav ölçeği açık."),
        ],
        "cons": [
            bi("The verified three-quarter cost example is 118,833 USD before aid, and four-to-five-quarter total cost is not fixed.", "Doğrulanmış üç çeyreklik maliyet örneği destek öncesi 118.833 USD'dir; dört-beş çeyreklik toplam sabit değildir."),
            bi("AA warns that first-year MS assistantships and incoming RAs are rare; self-funding the first quarters is a realistic planning assumption.", "AA birinci yıl MS asistanlıklarının ve giriş RA'larının nadir olduğu uyarısını yapar; ilk çeyrekleri öz kaynakla finanse etmek gerçekçi planlama varsayımıdır."),
            bi("Standard MS research is optional and neither admission nor programme prestige guarantees a laboratory place.", "Standart MS araştırması isteğe bağlıdır; kabul veya program prestiji laboratuvar yeri garantilemez."),
        ],
        "verdict": bi("A premier technical-fit option for applicants who want breadth and can tolerate extreme admission and cost risk. Treat funding as upside, not as the base budget, unless it appears in the written offer.", "Genişlik isteyen ve çok yüksek kabul ile maliyet riskini kaldırabilen adaylar için üst düzey teknik uygunluk seçeneğidir. Yazılı teklifte yer almadıkça finansmanı temel bütçe değil ek avantaj sayın."),
    }

    row["scoring_inputs"] = {
        "academic_prestige": None, "research_output": None, "industry_links": None, "affordability": None, "admission_chance": None, "living_quality": None,
        "hard_filter_flags": {"active_program": True, "non_eu_eligible": True, "english_only_compatible": True, "gre_required": False, "housing_guaranteed_conditionally": True, "funding_guaranteed": False, "needs_verification": True},
        "verification_notes": bi("No composite score is generated until the scoring model is recalibrated for sourced cost, funding and uncertainty inputs.", "Puanlama modeli kaynaklı maliyet, finansman ve belirsizlik girdilerine göre yeniden kalibre edilene kadar bileşik puan üretilmez."),
    }

    official_count = sum(1 for item in sources if item["source_type"].startswith("official_"))
    critical_institutional_source_count = official_count - 1  # QS is context, not programme evidence.
    row["data_quality"] = {
        "status": "partial", "checked_official_source_count": official_count,
        "verified_fields": ["program", "degree", "duration", "language", "eligibility", "non_eu_eligibility", "admission", "gre", "english_test", "tuition", "scholarship", "housing", "curriculum", "research", "deadline", "visa"],
        "unverified_critical_fields": [], "has_checked_source_log": True, "audited_at": TODAY,
    }
    row["quality_control"] = {
        "checked_at": TODAY, "qc_status": "needs_revision", "failed_canary_tests": [],
        "remaining_verification_tasks": [
            bi("Monitor publication of Fall 2027 graduate-housing dates.", "2027 Güz lisansüstü konut tarihlerinin yayımlanmasını izle."),
            bi("Replace medium-confidence operational English evidence if Stanford publishes a direct instruction-language label.", "Stanford doğrudan eğitim dili etiketi yayımlarsa orta güvenli operasyonel İngilizce kanıtını değiştir."),
            bi("Recheck fee-waiver international eligibility in the live application because no universal entitlement is published.", "Evrensel hak yayımlanmadığından canlı başvuruda uluslararası ücret muafiyeti uygunluğunu yeniden kontrol et."),
        ],
        "qc_notes": bi("Known unknowns are explicit; no estimate is stored as a verified programme total or funding promise.", "Bilinen bilinmeyenler açıktır; hiçbir tahmin doğrulanmış program toplamı veya finansman vaadi olarak saklanmaz."),
    }

    DATA_PATH.write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    audit = {
        "record_id": row["id"], "checked_at": TODAY, "source_count": len(sources),
        "official_source_count": official_count, "critical_institutional_source_count": critical_institutional_source_count, "student_forum_source_count": 3,
        "broken_or_unknown_count": sum(1 for item in sources if item["access_status"] in {"broken", "not_found", "unknown"}),
        "sources": [{"url": item["url"], "source_type": item["source_type"], "access_status": item["access_status"], "last_checked": item["last_checked"]} for item in sources],
    }
    AUDIT_PATH.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Updated Stanford AA-MS with {len(sources)} checked sources ({official_count} official).")


if __name__ == "__main__":
    main()
