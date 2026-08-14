from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data_base" / "amerika.json"
TODAY = "2026-08-14"

PROGRAM = "https://engineering.tamu.edu/aerospace/academics/degrees/graduate/ms.html"
ADMISSION = "https://engineering.tamu.edu/aerospace/admissions-and-aid/graduate-admissions/index.html"
COLLEGE_ADMISSION = "https://engineering.tamu.edu/admissions-and-aid/graduate-admissions/index.html"
INTERNATIONAL_ADMISSION = "https://admissions.tamu.edu/apply/international/international-graduate.html"
CATALOG = "https://catalog.tamu.edu/graduate/colleges-schools-interdisciplinary/engineering/aerospace/ms/"
GRAD_POLICY = "https://engineering.tamu.edu/aerospace/admissions-and-aid/graduate-admissions/graduate-policy.html"
COSTS = "https://global.tamu.edu/isss/student-scholar-resources/costs.html"
COST_TABLE = "https://global.tamu.edu/_files/_documents/isss-documents/2026-ecoa-12m-no-su.pdf"
ASSISTANTSHIPS = "https://grad.tamu.edu/funding/assistantships/index.html"
GA_SUPPORT = "https://grad.tamu.edu/funding/assistantships/ga-tuition-and-stipend-support.html"
GA_MINIMUM = "https://grad.tamu.edu/funding/university-minimum-graduate-assistant-stipend-rates.html"
HOUSING_ELIGIBILITY = "https://reslife.tamu.edu/housing-eligibility/"
HOUSING_RATES = "https://reslife.tamu.edu/rates/"
GARDENS = "https://reslife.tamu.edu/the-gardens-apartments/"
GARDENS_APPLICATION = "https://reslife.tamu.edu/gardens-application/"
HOUSING_APPLICATION = "https://reslife.tamu.edu/before-you-apply/"
RESEARCH = "https://engineering.tamu.edu/aerospace/research/index.html"
CENTERS = "https://engineering.tamu.edu/aerospace/research/centers-and-laboratories.html"
AUTONOMY = "https://engineering.tamu.edu/aerospace/research/autonomous-and-intelligent-systems.html"
HYPERSONICS = "https://engineering.tamu.edu/aerospace/research/hypersonics.html"
PROPULSION = "https://engineering.tamu.edu/aerospace/research/reacting-flows-and-propulsion.html"
SPACE_DOMAIN = "https://engineering.tamu.edu/aerospace/research/space-domain-awareness.html"
SPACE_OPERATIONS = "https://engineering.tamu.edu/aerospace/research/space-flight-and-operations.html"
TAMU_SPIRIT = "https://engineering.tamu.edu/research/tamu-spirit.html"
EXPORT_CONTROLS = "https://research.tamu.edu/research-compliance/export-controls/"
RANKING = "https://engineering.tamu.edu/about/facts-and-figures/rankings.html"
QS = "https://www.topuniversities.com/universities/texas-am-university"

REDDIT_GARDENS = "https://www.reddit.com/r/aggies/comments/1vjs50f/the_gardens_apartments/"
REDDIT_GARDENS_VS_PRIVATE = "https://www.reddit.com/r/aggies/comments/1jdqe8g"
REDDIT_GRAD_HOUSING = "https://www.reddit.com/r/aggies/comments/1rrzh8u/housing_for_phd_students/"


def bi(en: str, tr: str) -> dict[str, str]:
    return {"en": en, "tr": tr}


def source(
    url: str,
    title: str,
    source_type: str,
    fields: list[str],
    en: str,
    tr: str,
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
    row = next(item for item in rows if item.get("id") == "tamu-aero")

    row.update({
        "country": "United States",
        "university": "Texas A&M University",
        "university_native_name": "Texas A&M University",
        "city": "College Station",
        "program_name": "Master of Science in Aerospace Engineering (Thesis Option)",
        "program_native_name": "Master of Science in Aerospace Engineering (Thesis Option)",
        "program_degree": "MS",
        "degree_level": "Master",
        "duration": bi("Official programme duration not published", "Resmî program süresi yayımlanmamış"),
        "duration_years": None,
        "ects": None,
        "us_credit_hours": 30,
        "teaching_language": ["Unknown"],
        "teaching_languages": ["Unknown"],
        "program_url": PROGRAM,
        "program_status": "active",
        "relevance_status": "strong",
        "tuition_eur_per_year": None,
        "annual_fee_eur": None,
        "tuition_usd_per_year": 14641,
        "annual_fee_usd": 8356,
        "qs_ranking": 169,
        "qs_ranking_display": "#169",
        "qs_ranking_year": 2027,
    })

    row["prestige_profile"] = {
        "qs_world_rank": 169,
        "qs_edition": 2027,
        "qs_source_url": QS,
        "current_us_news_public_graduate_engineering_rank": 8,
        "current_us_news_public_aerospace_rank": 5,
        "ranking_edition": "2026",
        "official_ranking_source_url": RANKING,
        "interpretation": bi(
            "Rankings are context only. Technical fit is established separately through curriculum, faculty areas and named facilities.",
            "Sıralamalar yalnızca bağlamdır. Teknik uyum müfredat, öğretim üyesi alanları ve adlandırılmış tesislerle ayrıca kanıtlanır.",
        ),
    }

    row["eligibility_profile"] = {
        "eligible_for_non_eu": True,
        "required_previous_degree": bi(
            "A bachelor's degree in aerospace engineering or an equivalent field. A non-engineering degree may require leveling courses and possibly an additional undergraduate degree.",
            "Havacılık ve uzay mühendisliği veya eşdeğer bir alanda lisans. Mühendislik dışı bir derece dengeleme dersleri ve muhtemelen ek bir lisans derecesi gerektirebilir.",
        ),
        "accepted_backgrounds": [
            bi("Aerospace engineering", "Havacılık ve uzay mühendisliği"),
            bi("Equivalent engineering field", "Eşdeğer mühendislik alanı"),
            bi("Non-engineering background only with programme-assigned leveling", "Yalnızca programın belirlediği dengeleme ile mühendislik dışı geçmiş"),
        ],
        "three_year_international_bachelor_equivalent": False,
        "three_year_bachelor_remedy": bi(
            "Complete an additional one-year master's programme before eligibility can be considered.",
            "Uygunluk değerlendirilmeden önce ek bir yıllık yüksek lisans programı tamamlanmalıdır.",
        ),
        "minimum_gpa": 3.25,
        "minimum_gpa_scale": 4.0,
        "minimum_gpa_scope": "undergraduate_gpa_for_consideration",
        "admission_mode": "selective_research_match",
        "admission_risk": "high",
        "faculty_advisor_confirmation_required_before_admission": True,
        "faculty_funding_confirmation_required_before_admission": True,
        "faculty_contact_recommended_during_application": True,
        "required_documents": [
            bi("EngineeringCAS application", "EngineeringCAS başvurusu"),
            bi("Unofficial transcripts at application; official records after admission", "Başvuruda resmî olmayan transkriptler; kabulden sonra resmî kayıtlar"),
            bi("Statement of purpose (college guidance: 1–1.5 pages)", "Amaç mektubu (fakülte yönlendirmesi: 1–1,5 sayfa)"),
            bi("Resume or CV", "Özgeçmiş"),
            bi("Three letters of recommendation/evaluation", "Üç referans/değerlendirme mektubu"),
            bi("Official English-proficiency evidence unless exempt", "Muafiyet yoksa resmî İngilizce yeterlilik kanıtı"),
        ],
        "motivation_letter_required": True,
        "cv_required": True,
        "recommendation_required": True,
        "recommendation_letter_count": 3,
        "portfolio_required": False,
        "interview_required": None,
        "interview_policy": "not_listed_in_checked_official_requirements",
        "application_fee_usd": 148,
        "application_fee_breakdown": {
            "texas_am_international_fee_usd": 90,
            "engineeringcas_processing_fee_usd": 58,
        },
        "international_university_fee_waiver_available": False,
        "gre": {
            "policy": "not_required",
            "test_type": "GRE General",
            "minimum_scores": {},
            "recommended_scores": {},
            "waiver_rules": [],
            "policy_duration": "for_the_foreseeable_future",
            "source_ids": [ADMISSION],
        },
        "verification_notes": bi(
            "The 3.25 GPA is a minimum for consideration, not an admission guarantee. The MS cannot be admitted until an eligible faculty member confirms advising and funding support.",
            "3,25 GPA değerlendirme tabanıdır, kabul garantisi değildir. Uygun bir öğretim üyesi danışmanlık ve finansman desteğini onaylamadan MS kabulü verilemez.",
        ),
    }

    row["language_profile"] = {
        "teaching_language": ["Unknown"],
        "teaching_languages": ["Unknown"],
        "english_required": True,
        "accepted_english_tests": [
            {
                "test": "TOEFL iBT",
                "minimum_score_policy": {
                    "test_before_2026_01_21": {"overall": 80},
                    "test_on_or_after_2026_01_21": {"overall": 4.5, "each_skill": 4.0},
                },
                "validity_years": 2,
                "mybest_accepted": False,
                "engineeringcas_reporting_code": "B887",
            },
            {
                "test": "IELTS Academic",
                "minimum_score": 6.0,
                "validity_years": 2,
                "general_training_accepted": False,
                "one_skill_retake_for_admission_accepted": False,
            },
            {
                "test": "TOEFL Essentials",
                "minimum_score": 8.5,
                "validity_years": 2,
                "policy_scope": "central_university_policy_department_confirmation_recommended",
            },
        ],
        "department_alternative_verification": bi(
            "A master's degree from an accredited US institution may qualify through a departmental request.",
            "Akredite bir ABD kurumundan yüksek lisans, bölüm talebi yoluyla alternatif doğrulamaya uygun olabilir.",
        ),
        "central_degree_exemption": bi(
            "A completed bachelor's or master's degree entirely at an accredited US institution can meet admission ELP, with alternative verification required for registration.",
            "Akredite bir ABD kurumunda tamamen tamamlanan lisans veya yüksek lisans kabul ELP şartını karşılayabilir; kayıt için alternatif doğrulama gerekir.",
        ),
        "test_timing_recommendation": "at_least_eight_weeks_before_deadline",
        "teaching_assistant_elp_certification_separate": True,
        "language_risk": "medium",
        "verification_notes": bi(
            "Current central policy supplies the post-21 January 2026 TOEFL scale. The department page still prints the legacy TOEFL 80 and IELTS 6.0 thresholds. No checked official page explicitly states the programme teaching language, so it remains Unknown; an English-test rule is not treated as language-of-instruction proof.",
            "21 Ocak 2026 sonrası TOEFL ölçeğini güncel merkezî politika verir. Bölüm sayfası hâlâ eski TOEFL 80 ve IELTS 6,0 eşiklerini yayımlar. Kontrol edilen hiçbir resmî sayfa programın öğretim dilini açıkça belirtmediğinden alan Unknown kalır; İngilizce sınav şartı öğretim dili kanıtı sayılmaz.",
        ),
    }

    row["cost_profile"] = {
        "academic_year": "2026",
        "currency": "USD",
        "cost_scope": "international_i20_estimate_one_year_starting_fall_or_spring_no_summer_enrollment",
        "tuition_usd_per_year": 14641,
        "mandatory_fees_usd_per_year": 8356,
        "tuition_and_fees_usd_per_year": 22997,
        "health_insurance_required_for_f_or_j_students": True,
        "health_insurance_waiver_possible_with_equivalent_coverage": True,
        "health_insurance_usd_per_year": 3023,
        "tuition_fees_and_insurance_usd_per_year": 26020,
        "living_cost_usd_per_year_i20": 19995,
        "total_cost_of_attendance_usd_per_year": 46015,
        "out_of_state_tuition_waiver_value_usd": 9477,
        "international_student_services_fee_usd_per_semester": 150,
        "international_orientation_fee_usd_one_time": 70,
        "orientation_fee_included_in_i20_estimate": False,
        "application_fee_usd": 148,
        "complete_program_cost_usd": None,
        "tuition_basis": "official 2026 ISSS estimate for College of Engineering graduate students at nonresident rate",
        "tuition_items": [
            {"item": bi("Tuition", "Öğrenim ücreti"), "amount_usd": 14641, "period": "two_major_semesters"},
            {"item": bi("Required fees", "Zorunlu ücretler"), "amount_usd": 8356, "period": "two_major_semesters"},
            {"item": bi("Required F-1/J-1 health insurance", "Zorunlu F-1/J-1 sağlık sigortası"), "amount_usd": 3023, "period": "12_months"},
            {"item": bi("Living-expense allowance", "Yaşam gideri payı"), "amount_usd": 19995, "period": "12_months"},
        ],
        "verification_notes": bi(
            "The $46,015 amount is an immigration-document estimate, not a guaranteed bill. It assumes nonresident Engineering rates, two major semesters and 12 months of living and insurance; summer tuition is excluded. A fully funded departmental offer must be read line by line because the programme page does not publish a universal package breakdown.",
            "46.015 $ göçmenlik belgesi tahminidir, garantili fatura değildir. Eyalet dışı Engineering oranlarını, iki ana dönemi ve 12 aylık yaşam ile sigortayı varsayar; yaz öğrenim ücreti hariçtir. Program sayfası evrensel paket dökümü yayımlamadığından tam finansman teklifi kalem kalem okunmalıdır.",
        ),
    }

    row["scholarship_profile"] = {
        "available_types": ["graduate_research_assistantship", "graduate_teaching_assistantship", "aerospace_graduate_student_fellow", "fellowship"],
        "non_eu_eligible": "position_or_award_specific",
        "application_mode": "automatic",
        "application_mode_detail": "integrated_with_ms_admission_and_required_faculty_match",
        "automatic_consideration": True,
        "separate_application_required": False,
        "faculty_outreach_recommended": True,
        "funding_confirmation_required_before_admission": True,
        "published_thesis_track_fully_funded_rate_percent": 100,
        "funding_package_breakdown_standardized_on_program_page": False,
        "assistantship_work_hours_per_week": 20,
        "initial_ms_assistantship_appointment_usually_years": 2,
        "continued_support_guaranteed": False,
        "continuation_conditions": ["satisfactory academic progress", "satisfactory assistantship performance", "availability of support funds"],
        "university_minimum_gat_gar_gal_stipend_usd_per_month_50_fte": 1826,
        "minimum_stipend_effective_date": "2025-09-01",
        "nonresident_tuition_waiver_requires_request_each_semester": True,
        "masters_tuition_and_fee_payment_university_mandated": False,
        "health_insurance_employee_plan_eligibility": "50_percent_FTE_for_at_least_4_5_months",
        "opportunities": [
            {
                "name": "Faculty or department graduate assistantship / AGSF",
                "type": "admission-linked competitive employment or fellowship support",
                "amount": None,
                "currency": "USD",
                "automatic_consideration": True,
                "separate_application_required": False,
                "deadline": bi("Fall priority: December 1; Spring priority: September 1", "Güz öncelik: 1 Aralık; Bahar öncelik: 1 Eylül"),
                "benefits": ["stipend", "funding support specified in individual offer", "possible nonresident tuition waiver", "health-plan eligibility when appointment rules are met"],
                "url": ADMISSION,
            },
        ],
        "funding_notes": bi(
            "The department states that all thesis-track students are fully funded and requires a faculty member to confirm advising and funding before admission. This is stronger than ordinary automatic consideration, but the exact tuition, fee, insurance, stipend and summer coverage remains offer-specific. University-wide tuition-payment mandates explicitly cover PhD GAT/GAR/GAL appointments, not every master's appointment.",
            "Bölüm tüm tez hattı öğrencilerinin tam finanse edildiğini belirtir ve kabulden önce bir öğretim üyesinin danışmanlık ile finansmanı onaylamasını ister. Bu, sıradan otomatik değerlendirmeden daha güçlüdür; ancak öğrenim, ücret, sigorta, stipend ve yaz kapsamı teklif özeldir. Üniversite geneli öğrenim ödeme zorunluluğu açıkça PhD GAT/GAR/GAL atamalarını kapsar, her yüksek lisans atamasını değil.",
        ),
        "verification_notes": bi(
            "Do not convert the published 100% rate into an assumed dollar package. The appointment letter must confirm every covered item and term.",
            "Yayımlanan %100 oranını varsayımsal bir dolar paketine çevirmeyin. Atama mektubu kapsanan her kalemi ve dönemi doğrulamalıdır.",
        ),
    }

    row["living_profile"] = {
        "city_cost_level": "medium",
        "housing_difficulty": "medium",
        "living_risk": "medium",
        "housing_access": "not_guaranteed",
        "student_housing_available": True,
        "housing_application_separate": True,
        "housing_allocation_mode": "first_come_first_served_with_gardens_priority_for_graduate_international_and_other_eligible_groups",
        "typical_waitlist_timing": bi("Residence Life says capacity typically moves to wait list in February for Fall and December for Spring.", "Residence Life kapasitenin genellikle Güz için Şubat'ta, Bahar için Aralık'ta bekleme listesine geçtiğini belirtir."),
        "housing_application_fee_usd": 75,
        "monthly_housing_rent_usd_per_month_min": 931,
        "monthly_housing_rent_usd_per_month_max": 1863,
        "average_room_rent_usd": None,
        "average_room_rent_scope_label": bi("Official Gardens examples; not a city or private-market average", "Resmî Gardens örnekleri; şehir veya özel piyasa ortalaması değil"),
        "housing_options": [
            {
                "provider": "The Gardens Apartments",
                "institution_owned": True,
                "graduate_eligible": True,
                "international_eligible": True,
                "assignment_priority_for_graduate_and_international": True,
                "guaranteed": False,
                "furnished": True,
                "utilities_included_subject_to_electricity_cap": True,
            }
        ],
        "official_rent_items": [
            {"item": bi("Gardens shared two-bedroom, per bedroom", "Gardens paylaşımlı iki yatak odalı, oda başı"), "amount_usd_min": 931, "amount_usd_max": 1212, "period": "month", "academic_year": "2026/2027"},
            {"item": bi("Gardens one-bedroom whole apartment", "Gardens tek yatak odalı tüm daire"), "amount_usd_min": 1262, "amount_usd_max": 1385, "period": "month", "academic_year": "2026/2027"},
            {"item": bi("Gardens two-bedroom whole apartment", "Gardens iki yatak odalı tüm daire"), "amount_usd_min": 1574, "amount_usd_max": 1863, "period": "month", "academic_year": "2026/2027"},
        ],
        "official_living_cost_items": [
            {"item": bi("ISSS 12-month living allowance", "ISSS 12 aylık yaşam payı"), "amount_usd": 19995, "period": "12_months", "academic_year": "2026"}
        ],
        "housing_notes": bi(
            "The Gardens is explicitly open to graduate and international students, and those groups receive assignment priority. Housing remains availability-dependent and first-come-first-served; eligibility and priority are not a guarantee. The application is separate from academic admission.",
            "The Gardens açıkça lisansüstü ve uluslararası öğrencilere açıktır ve bu gruplar yerleştirme önceliği alır. Konut yine boşluğa bağlı ve ilk gelene ilk hizmet esaslıdır; uygunluk ve öncelik garanti değildir. Başvuru akademik kabulden ayrıdır.",
        ),
        "verification_notes": bi(
            "The displayed range combines current university-owned Gardens configurations. No private-market average is asserted.",
            "Gösterilen aralık üniversiteye ait güncel Gardens düzenlerini birleştirir. Özel piyasa ortalaması iddia edilmez.",
        ),
    }

    row["curriculum_profile"] = {
        "credit_system": "US semester credit hours",
        "credit_hours_total": 30,
        "course_count_fixed": False,
        "formal_coursework_credit_hours": 21,
        "formal_course_count": None,
        "seminar_credit_hours": 2,
        "research_credit_hours": 7,
        "thesis_route_available": True,
        "thesis_required": True,
        "thesis_defense_required": True,
        "advisory_committee_minimum_members": 3,
        "primary_advisor_required": True,
        "non_thesis_route_in_this_record": False,
        "related_non_thesis_degree": "Master of Engineering in Aerospace Engineering",
        "internship_required": False,
        "internship_requirement_status": "not_listed_in_checked_ms_degree_requirements",
        "course_count_summary": bi(
            "30 credits: 21 formal coursework, 2 AERO 681 Seminar and 7 AERO 691 Research. A fixed number of courses is not published because credit values and the approved degree plan can vary.",
            "30 kredi: 21 resmî ders, 2 AERO 681 Seminer ve 7 AERO 691 Araştırma. Kredi değerleri ve onaylı derece planı değişebildiğinden sabit ders sayısı yayımlanmamıştır.",
        ),
        "tracks": [
            bi("Dynamics and Control", "Dinamik ve Kontrol"),
            bi("Aerodynamics and Propulsion", "Aerodinamik ve İtki"),
            bi("Materials and Structures", "Malzemeler ve Yapılar"),
            bi("Systems, Design and Human Integration", "Sistemler, Tasarım ve İnsan Entegrasyonu"),
        ],
        "research_area_choices": [
            bi("Autonomous and Intelligent Systems", "Otonom ve Akıllı Sistemler"),
            bi("Hypersonics", "Hipersonik"),
            bi("Multi-Functional and Extreme Environment Materials", "Çok İşlevli ve Aşırı Ortam Malzemeleri"),
            bi("Optical, Remote and Quantum Sensing", "Optik, Uzaktan ve Kuantum Algılama"),
            bi("Reacting Flows and Propulsion", "Tepkimeli Akışlar ve İtki"),
            bi("Space Domain Awareness", "Uzay Alan Farkındalığı"),
            bi("Space Flight and Operations: Human and Robotic", "Uzay Uçuşu ve Operasyonları: İnsanlı ve Robotik"),
        ],
        "seminar_requirements": {
            "aero_681_hours": 2,
            "required_sections": ["Communication", "Professional Development"],
            "aess_special_seminars_per_fall_and_spring": 5,
        },
        "degree_plan_due": "before_end_of_second_semester",
        "minimum_gpa_to_remain_in_good_standing": 3.0,
        "verification_notes": bi(
            "This record is only the research-based MS thesis option. The self-funded 30-credit non-thesis MEng is a distinct programme and is not compressed into this record.",
            "Bu kayıt yalnızca araştırma temelli tezli MS seçeneğidir. Öz finansmanlı 30 kredilik tezsiz MEng ayrı bir programdır ve bu kayda sıkıştırılmamıştır.",
        ),
    }

    row["category_profile"] = {
        "primary_categories": ["aerospace_engineering", "space_engineering"],
        "technical_fit": {
            "space_systems_astrodynamics_sda": "very_strong",
            "gnc_autonomy_robotics": "very_strong",
            "hypersonics_aerothermodynamics": "very_strong",
            "reacting_flows_propulsion": "very_strong",
            "structures_extreme_environment_materials": "very_strong",
            "human_spaceflight_bioastronautics": "very_strong",
            "optical_remote_quantum_sensing": "strong",
        },
        "evidence_basis": bi(
            "Fit labels are based on current official research-area pages and named laboratories, not university rank or programme title.",
            "Uyum etiketleri üniversite sırası veya program adına değil, güncel resmî araştırma alanı sayfalarına ve adlandırılmış laboratuvarlara dayanır.",
        ),
    }

    row["research_profile"] = {
        "research_focus_areas": [
            "Autonomous and Intelligent Systems",
            "Hypersonics",
            "Multi-Functional and Extreme Environment Materials",
            "Optical, Remote and Quantum Sensing",
            "Reacting Flows and Propulsion",
            "Space Domain Awareness",
            "Space Flight and Operations: Human and Robotic",
        ],
        "key_institutes": [
            "National Aerothermochemistry and Hypersonic Flight Laboratory (NAHL)",
            "Ballistic, Aero-optics, and Materials (BAM) Range",
            "Detonation Research Test Facility",
            "Land Air & Space Robotics (LASR) Laboratory",
            "Vehicle Systems & Control Laboratory",
            "Systems Engineering, Architecture and Knowledge (SEAK) Lab",
            "Aerospace Human Systems Laboratory",
            "AeroSpace Technology Research and Operations (ASTRO) Center",
            "TAMU-SPIRIT Flight Facility",
        ],
        "space_specific_facilities": [
            {"name": "LASR Laboratory", "capabilities": ["spacecraft proximity operations", "robotic sensing and control", "swarm robotics", "realistic optical sensing arena"]},
            {"name": "SEAK Lab", "capabilities": ["space mission design", "systems engineering", "artificial intelligence", "Earth-observation mission cognitive assistants"]},
            {"name": "Aerospace Human Systems Laboratory", "capabilities": ["spacesuits", "habitats", "environmental systems", "artificial-gravity research"]},
            {"name": "TAMU-SPIRIT", "capabilities": ["ISS external research", "in-space testing", "advanced materials", "robotics", "space surveillance and tracking"], "planned_first_mission": "SpaceX-37, August–October 2027"},
        ],
        "hypersonics_propulsion_facilities": [
            {"name": "NAHL", "capabilities": ["nonequilibrium hypersonic flows", "surface interactions", "aerodynamics", "propulsion"]},
            {"name": "BAM Range", "capabilities": ["hypersonic aerothermodynamics", "hypervelocity impact", "aero-optics"], "operational_phase_length_m": 565},
            {"name": "Detonation Research Test Facility", "capabilities": ["reactive flows", "detonations", "at-scale experiments"], "tube_length_m": 150, "tube_diameter_m": 2},
        ],
        "research_expenditures_fy23_usd_millions": 43.1,
        "research_funding_level": "very_high",
        "research_risk": "medium_for_international_project_access",
        "advisor_match_required": True,
        "verification_notes": bi(
            "The infrastructure is unusually broad across flight, space and high-speed flow. Access is advisor-, project-, training- and availability-dependent; listing a facility does not promise an individual student a place or unrestricted access.",
            "Altyapı uçuş, uzay ve yüksek hızlı akış genelinde sıra dışı ölçüde geniştir. Erişim danışman, proje, eğitim ve boşluğa bağlıdır; bir tesisin listelenmesi bireysel öğrenciye yer veya sınırsız erişim vadetmez.",
        ),
    }

    row["industry_ecosystem_profile"] = {
        "local_industry_strength": "research_ecosystem_strong_but_not_a_direct_employment_guarantee",
        "key_companies": ["Aegis Aerospace"],
        "verified_partnerships": [
            {
                "partner": "Aegis Aerospace",
                "initiative": "TAMU-SPIRIT",
                "status": "active_development_and_experiment_selection",
                "scope": bi(
                    "A Texas A&M-dedicated external ISS research platform for in-space testing, materials, robotics and space-surveillance experiments.",
                    "Uzay içi test, malzeme, robotik ve uzay gözetleme deneyleri için Texas A&M'e ayrılmış haricî ISS araştırma platformu.",
                ),
                "source_url": TAMU_SPIRIT,
            }
        ],
        "hiring_culture": "project_and_citizenship_dependent",
        "export_control_risk": "project_specific",
        "export_control_notes": bi(
            "Texas A&M states that EAR/ITAR and other controls can apply to research and to releases of controlled technology or information to foreign persons in the US. This is a project-level risk, not a claim that all aerospace research is closed to international students.",
            "Texas A&M, EAR/ITAR ve diğer kontrollerin araştırmaya ve ABD içindeki yabancı kişilere kontrollü teknoloji veya bilgi aktarımına uygulanabileceğini belirtir. Bu proje düzeyi bir risktir; tüm havacılık-uzay araştırmasının uluslararası öğrencilere kapalı olduğu iddiası değildir.",
        ),
        "alumni_presence": "not_quantified",
        "industry_risk": "medium",
        "verification_notes": bi(
            "Only the current, officially confirmed Aegis partnership is named. Legacy lists of nearby employers or alleged partnerships were removed because location and reputation do not prove a programme relationship.",
            "Yalnızca güncel ve resmî olarak doğrulanmış Aegis ortaklığı adlandırılır. Konum ve itibar program ilişkisini kanıtlamadığından eski yakındaki işveren veya iddia edilen ortaklık listeleri kaldırılmıştır.",
        ),
    }

    row["application_timeline_profile"] = {
        "application_system": "EngineeringCAS",
        "rolling_review": True,
        "summer_entry": None,
        "summer_entry_status": "not_listed_for_ms_in_checked_department_deadline_table",
        "pre_enrollment_required": False,
        "visa_complexity": "high",
        "application_rounds": [
            {
                "round": bi("Fall MS funding priority", "Güz MS finansman önceliği"),
                "deadline": "December 1 of the preceding year",
                "deadline_type": "priority_not_final",
                "recommended_submission_timing": bi("Three weeks to one month before the deadline", "Son tarihten üç hafta ile bir ay önce"),
            },
            {
                "round": bi("Spring MS funding priority", "Bahar MS finansman önceliği"),
                "deadline": "September 1 of the preceding year",
                "deadline_type": "priority_not_final",
                "recommended_submission_timing": bi("Three weeks to one month before the deadline", "Son tarihten üç hafta ile bir ay önce"),
            },
        ],
        "final_application_deadline": None,
        "final_deadline_status": "not_published_on_checked_department_page",
        "funding_priority_deadline_fall": "December 1",
        "funding_priority_deadline_spring": "September 1",
        "faculty_contact_timing": "during_application_process",
        "offer_acceptance_context": "April 15 Council of Graduate Schools resolution applies to covered financial-support offers",
        "i20_or_ds2019_after_admission": True,
        "proof_of_funds_required_if_offer_does_not_cover_full_i20_estimate": True,
        "timeline_risk": "medium",
        "verification_notes": bi(
            "The department labels December 1 and September 1 as priority deadlines and says materials may continue afterward. A final closing date is therefore left unknown rather than invented. International applicants should treat the priority date as the operational deadline because advisor and funding confirmation are admission conditions.",
            "Bölüm 1 Aralık ve 1 Eylül'ü öncelik tarihleri olarak etiketler ve belgelerin sonrasında da gönderilebileceğini belirtir. Bu nedenle nihai kapanış tarihi uydurulmaz ve bilinmiyor bırakılır. Danışman ile finansman onayı kabul koşulu olduğundan uluslararası adaylar öncelik tarihini fiilî son tarih saymalıdır.",
        ),
    }

    row["student_sentiment_profile"] = {
        "student_satisfaction_score": None,
        "teaching_quality_sentiment": "unknown",
        "workload_sentiment": "unknown",
        "administration_sentiment": "unknown",
        "housing_sentiment": "mixed",
        "city_life_sentiment": "unknown",
        "international_student_sentiment": "unknown",
        "career_support_sentiment": "unknown",
        "student_sentiment_summary": bi(
            "The small recent sample is housing-focused. Gardens is described as convenient and close to engineering, with mixed comments on amenities, noise and building conditions; other graduate students value quieter condo/townhome options. This sample cannot support a programme-satisfaction score.",
            "Küçük güncel örneklem konut odaklıdır. Gardens, Engineering'e yakın ve kullanışlı olarak anlatılır; imkânlar, gürültü ve bina koşulları konusunda görüşler karışıktır. Diğer lisansüstü öğrenciler daha sessiz condo/townhome seçeneklerine değer verir. Bu örneklem program memnuniyet puanını desteklemez.",
        ),
        "sample_size_approx": 10,
        "date_range": "2025-03 to 2026-08",
        "sentiment_confidence": "low",
        "student_sentiment_sources": [REDDIT_GARDENS, REDDIT_GARDENS_VS_PRIVATE, REDDIT_GRAD_HOUSING],
        "verification_notes": bi(
            "Sentiment is anecdotal, self-selected and limited to housing; it is never used to prove admissions, funding, cost or programme quality.",
            "Duygu verisi anekdotsal, öz-seçimli ve konutla sınırlıdır; kabul, finansman, maliyet veya program kalitesini kanıtlamak için kullanılmaz.",
        ),
    }

    sources = [
        source(PROGRAM, "Texas A&M MS in Aerospace Engineering", "official_program_page", ["program", "curriculum", "admission", "funding", "research"], "Current degree structure, GPA, advisor/funding condition and published thesis-track funding rate.", "Güncel derece yapısı, GPA, danışman/finansman koşulu ve yayımlanan tez hattı finansman oranı."),
        source(ADMISSION, "Texas A&M Aerospace Graduate Admissions", "official_admission_page", ["admission", "deadline", "gre", "language", "funding"], "Department-specific priority deadlines, GRE policy, materials and international guidance.", "Bölüme özgü öncelik tarihleri, GRE politikası, belgeler ve uluslararası yönlendirme."),
        source(COLLEGE_ADMISSION, "Texas A&M Engineering Graduate Admissions", "official_admission_page", ["application", "documents", "fees"], "EngineeringCAS, three recommendations and the $148 international application total.", "EngineeringCAS, üç referans ve 148 $ uluslararası başvuru toplamı."),
        source(INTERNATIONAL_ADMISSION, "Texas A&M International Graduate Admissions", "official_admission_page", ["non_eu_eligibility", "language", "fees", "transcripts"], "Current international eligibility, fee, transcript and post-January-2026 English rules.", "Güncel uluslararası uygunluk, ücret, transkript ve Ocak 2026 sonrası İngilizce kuralları."),
        source(CATALOG, "Texas A&M Catalog — MS Aerospace Engineering", "official_curriculum_page", ["degree_status", "thesis", "completion"], "Current catalog confirmation of the MS thesis degree and graduate requirements.", "MS tez derecesi ve lisansüstü şartların güncel katalog teyidi."),
        source(GRAD_POLICY, "Texas A&M Aerospace Graduate Policy", "official_department_page", ["funding", "course_load", "seminar", "duration_context"], "Assistantship duties, typical initial MS appointment term, seminar and degree-plan rules.", "Asistanlık görevleri, tipik ilk MS atama süresi, seminer ve derece planı kuralları."),
        source(COSTS, "Texas A&M ISSS Costs and Financial Documents", "official_visa_or_government_page", ["cost", "insurance", "visa", "fees"], "Purpose and limitations of the I-20 estimate plus current insurance and ISSS fees.", "I-20 tahmininin amacı ve sınırları ile güncel sigorta ve ISSS ücretleri."),
        source(COST_TABLE, "Texas A&M 2026 ISSS Engineering Graduate Cost Table", "official_tuition_page", ["tuition", "fees", "insurance", "living", "total_cost"], "Accessible official 2026 Engineering graduate cost breakdown.", "Erişilebilir resmî 2026 Engineering lisansüstü maliyet dökümü.", access_status="pdf"),
        source(ASSISTANTSHIPS, "Texas A&M Graduate Assistantships", "official_scholarship_page", ["funding", "insurance", "waiver"], "Assistantship types and general benefits, with eligibility caveats.", "Uygunluk çekinceleriyle asistanlık türleri ve genel haklar."),
        source(GA_SUPPORT, "Texas A&M GA Tuition and Stipend Support", "official_scholarship_page", ["funding", "tuition", "waiver"], "Clarifies the PhD tuition mandate and semester-specific nonresident waiver rules.", "PhD öğrenim ödeme zorunluluğunu ve dönemlik eyalet dışı muafiyet kurallarını açıklar."),
        source(GA_MINIMUM, "Texas A&M Minimum GA Stipend Rates", "official_scholarship_page", ["funding", "stipend", "insurance"], "Current $1,826 monthly minimum at 50% FTE and insurance eligibility threshold.", "%50 FTE için güncel aylık 1.826 $ taban ve sigorta uygunluk eşiği."),
        source(HOUSING_ELIGIBILITY, "Texas A&M Housing Eligibility", "official_housing_page", ["housing", "availability"], "First-come-first-served policy, typical waitlist timing and Gardens eligibility.", "İlk gelene ilk hizmet, tipik bekleme listesi zamanı ve Gardens uygunluğu."),
        source(HOUSING_RATES, "Texas A&M Residence Life 2026/27 Rates", "official_housing_page", ["housing", "rent"], "Current Gardens per-bedroom and whole-apartment rates.", "Güncel Gardens oda ve tüm daire fiyatları."),
        source(GARDENS, "Texas A&M Gardens Apartments", "official_housing_page", ["housing", "eligibility", "amenities"], "Graduate/international priority, unit types and amenities.", "Lisansüstü/uluslararası önceliği, birim türleri ve imkânlar."),
        source(GARDENS_APPLICATION, "Texas A&M Gardens Application", "official_housing_page", ["housing_application", "contract"], "Separate application process and availability-dependent assignment.", "Ayrı başvuru süreci ve boşluğa bağlı yerleştirme."),
        source(HOUSING_APPLICATION, "Texas A&M Before You Apply for Housing", "official_housing_page", ["housing_application", "fee", "guarantee"], "$75 fee and explicit non-guarantee for waitlist applicants.", "75 $ ücret ve bekleme listesi adayları için açık garanti yokluğu."),
        source(RESEARCH, "Texas A&M Aerospace Research", "official_department_page", ["research_areas"], "Current department research taxonomy.", "Güncel bölüm araştırma taksonomisi."),
        source(CENTERS, "Texas A&M Aerospace Centers and Laboratories", "official_lab_page", ["research", "labs"], "Named aerospace and space systems facilities.", "Adlandırılmış havacılık-uzay ve uzay sistemleri tesisleri."),
        source(AUTONOMY, "Texas A&M Autonomous and Intelligent Systems", "official_department_page", ["research", "labs"], "Astrodynamics, controls, estimation, uncertainty and autonomous systems.", "Astrodinamik, kontrol, kestirim, belirsizlik ve otonom sistemler."),
        source(HYPERSONICS, "Texas A&M Hypersonics", "official_department_page", ["research", "labs"], "NAHL and BAM capabilities with current facility details.", "Güncel tesis ayrıntılarıyla NAHL ve BAM yetenekleri."),
        source(PROPULSION, "Texas A&M Reacting Flows and Propulsion", "official_department_page", ["research", "labs"], "Combustion, detonation, reactive-flow and at-scale test facilities.", "Yanma, detonasyon, tepkimeli akış ve tam ölçekli test tesisleri."),
        source(SPACE_DOMAIN, "Texas A&M Space Domain Awareness", "official_department_page", ["research", "labs", "space_fit"], "Astrodynamics, cislunar dynamics, tracking, debris and robotics facilities.", "Astrodinamik, cislunar dinamik, izleme, enkaz ve robotik tesisleri."),
        source(SPACE_OPERATIONS, "Texas A&M Space Flight and Operations", "official_department_page", ["research", "labs", "space_fit"], "Human spaceflight, habitats, spacesuits, mission design and human-robot systems.", "İnsanlı uzay uçuşu, habitatlar, uzay giysileri, görev tasarımı ve insan-robot sistemleri."),
        source(TAMU_SPIRIT, "Texas A&M TAMU-SPIRIT", "official_industry_partner_page", ["industry_ecosystem", "research", "space_fit"], "Current Aegis partnership and planned dedicated ISS platform.", "Güncel Aegis ortaklığı ve planlanan özel ISS platformu."),
        source(EXPORT_CONTROLS, "Texas A&M Export Controls", "official_university_policy_page", ["international_risk", "research_access"], "Project-specific EAR/ITAR implications for controlled research and foreign persons.", "Kontrollü araştırma ve yabancı kişiler için projeye özgü EAR/ITAR etkileri."),
        source(RANKING, "Texas A&M Engineering Rankings", "official_ranking_page", ["prestige"], "Current institution-reported 2026 public graduate Engineering and aerospace ranks.", "Kurumun bildirdiği güncel 2026 kamu lisansüstü Engineering ve aerospace sıraları."),
        source(QS, "QS World University Rankings 2027 — Texas A&M", "reliable_third_party_ranking", ["prestige"], "University-wide context only; not evidence of aerospace fit.", "Yalnızca üniversite geneli bağlam; havacılık-uzay uyumu kanıtı değildir.", confidence="medium"),
        source(REDDIT_GARDENS, "Reddit — Gardens Apartments 2026", "student_forum", ["student_sentiment"], "Small recent anecdotal housing sample.", "Küçük ve güncel anekdotsal konut örneklemi.", confidence="low"),
        source(REDDIT_GARDENS_VS_PRIVATE, "Reddit — Gardens versus private housing", "student_forum", ["student_sentiment"], "Small housing-only comparison sample.", "Küçük, yalnızca konuta ilişkin karşılaştırma örneklemi.", confidence="low"),
        source(REDDIT_GRAD_HOUSING, "Reddit — graduate housing preferences", "student_forum", ["student_sentiment"], "Small graduate housing preference sample.", "Küçük lisansüstü konut tercihi örneklemi.", confidence="low"),
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
            "Every core decision field except explicit teaching language is supported by current official sources. A final deadline beyond the published priority dates, a fixed formal course count, private-market rent, complete-program cost and the exact standard funding package are deliberately not invented.",
            "Açık öğretim dili dışındaki tüm temel karar alanları güncel resmî kaynaklarla desteklenir. Yayımlanan öncelik tarihlerinin ötesindeki nihai son tarih, sabit resmî ders sayısı, özel piyasa kirası, tam program maliyeti ve kesin standart finansman paketi bilerek uydurulmamıştır.",
        ),
        "source_log": sources,
    }

    row["decision_summary"] = {
        "best_for": [
            bi("Research-oriented applicants who want a funded thesis MS and can secure a faculty match.", "Finanse edilen tezli MS isteyen ve öğretim üyesi eşleşmesi kurabilen araştırma odaklı adaylar."),
            bi("Students targeting space domain awareness, astrodynamics, autonomous systems, human spaceflight, hypersonics, propulsion or extreme-environment materials.", "Uzay alan farkındalığı, astrodinamik, otonom sistemler, insanlı uzay uçuşu, hipersonik, itki veya aşırı ortam malzemelerini hedefleyen öğrenciler."),
        ],
        "not_ideal_for": [
            bi("Applicants who want a coursework-only master's; that is the separate self-funded MEng.", "Yalnız ders temelli yüksek lisans isteyenler; bu ayrı ve öz finansmanlı MEng programıdır."),
            bi("Applicants unwilling to contact faculty early or whose plans depend on guaranteed unrestricted access to export-controlled projects.", "Öğretim üyeleriyle erken iletişim kurmak istemeyen veya planı ihracat kontrollü projelere garantili sınırsız erişime bağlı adaylar."),
        ],
        "main_strengths": [
            bi("The department publishes 100% funding for thesis-track students and makes advisor/funding confirmation an admission condition.", "Bölüm tez hattı öğrencileri için %100 finansman yayımlar ve danışman/finansman onayını kabul koşulu yapar."),
            bi("Clear 30-credit thesis structure with 21 coursework, 2 seminar and 7 research credits.", "21 ders, 2 seminer ve 7 araştırma kredisinden oluşan açık 30 kredilik tez yapısı."),
            bi("Exceptional verified breadth from SDA and human spaceflight to hypersonics, detonation and autonomous systems.", "SDA ve insanlı uzay uçuşundan hipersonik, detonasyon ve otonom sistemlere olağanüstü doğrulanmış genişlik."),
            bi("TAMU-SPIRIT creates an officially confirmed route to a Texas A&M-dedicated ISS research platform.", "TAMU-SPIRIT, Texas A&M'e ayrılmış ISS araştırma platformuna resmî olarak doğrulanmış bir yol oluşturur."),
        ],
        "main_risks": [
            bi("Admission requires a faculty advisor willing to provide funding; research fit is therefore a hard gate.", "Kabul, finansman sağlamaya istekli öğretim üyesi danışmanı gerektirir; araştırma uyumu bu nedenle kesin bir eşiktir."),
            bi("The published 'fully funded' rate does not disclose one universal package; coverage and summer terms must be checked in the offer letter.", "Yayımlanan 'tam finanse' oranı tek bir evrensel paket açıklamaz; kapsam ve yaz dönemleri teklif mektubunda kontrol edilmelidir."),
            bi("Unfunded 2026 international I-20 budget is $46,015 for one year, excluding summer tuition and the one-time orientation fee.", "Finansmansız 2026 uluslararası I-20 bütçesi bir yıl için 46.015 $'dır; yaz öğrenimi ve tek seferlik oryantasyon ücreti hariçtir."),
            bi("University housing is available and prioritized for graduate/international students but remains first-come-first-served and not guaranteed.", "Üniversite konutu vardır ve lisansüstü/uluslararası öğrencilere öncelik verir ancak ilk gelene ilk hizmet esaslı ve garantisizdir."),
            bi("Some research can be subject to project-specific EAR/ITAR controls affecting foreign-person access.", "Bazı araştırmalar yabancı kişi erişimini etkileyen projeye özgü EAR/ITAR kontrollerine tabi olabilir."),
            bi("No checked official source explicitly states the programme teaching language.", "Kontrol edilen hiçbir resmî kaynak programın öğretim dilini açıkça belirtmez."),
        ],
        "decision_summary": bi(
            "A top-tier technical fit for a research-focused space/aerospace applicant: the thesis MS is structurally clear, funding-linked and backed by unusually broad laboratories. The decisive application task is not GRE preparation but early faculty matching. Treat funding details, housing and export-controlled project access conservatively until written offers and project assignments are known.",
            "Araştırma odaklı uzay/havacılık-uzay adayı için üst düzey teknik uyum: tezli MS açık yapılı, finansman bağlantılı ve sıra dışı geniş laboratuvarlarla desteklenir. Başvurunun belirleyici işi GRE hazırlığı değil, erken öğretim üyesi eşleşmesidir. Yazılı teklifler ve proje atamaları bilinmeden finansman ayrıntıları, konut ve ihracat kontrollü proje erişimini temkinli değerlendirin.",
        ),
        "pros": [],
        "cons": [],
        "verdict": bi(
            "Exceptional funded thesis opportunity for a strong faculty match; package details and project access still require written verification.",
            "Güçlü öğretim üyesi eşleşmesi için olağanüstü finanse tez fırsatı; paket ayrıntıları ve proje erişimi yine yazılı doğrulama gerektirir.",
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
            "faculty_advisor_and_funding_confirmation_required",
            "funding_package_details_offer_specific",
            "housing_not_guaranteed",
            "export_control_access_project_specific",
            "final_deadline_not_published",
        ],
    }
    row["data_quality"] = {
        "status": "partial",
        "checked_official_source_count": 26,
        "verified_fields": ["program", "admission", "non_eu_eligibility", "tuition", "scholarship", "deadline", "curriculum", "research", "industry_ecosystem", "housing", "living", "insurance", "prestige"],
        "unverified_critical_fields": ["language"],
        "known_semantic_gaps": ["explicit_teaching_language", "final_application_deadline_after_priority_date", "fixed_formal_course_count", "universal_funding_package_breakdown", "private_market_rent", "complete_program_cost"],
        "has_checked_source_log": True,
        "audited_at": TODAY,
    }
    row["quality_control"] = {
        "checked_at": TODAY,
        "qc_status": "needs_revision",
        "remaining_verification_tasks": [
            bi("Find a current official source explicitly stating the MS teaching language; do not infer it from English-test requirements.", "MS öğretim dilini açıkça belirten güncel resmî kaynak bulun; İngilizce sınav şartlarından çıkarım yapmayın."),
            bi("Add a final post-priority application closing date only if the Aerospace department publishes one.", "Öncelik sonrası nihai başvuru kapanış tarihini yalnızca Aerospace bölümü yayımlarsa ekleyin."),
            bi("Record the exact stipend, tuition, fee, insurance and summer coverage from a current individual offer template if the department makes one public.", "Bölüm güncel bireysel teklif şablonunu yayımlarsa kesin stipend, öğrenim, ücret, sigorta ve yaz kapsamını kaydedin."),
        ],
        "qc_notes": bi(
            "All discoverable decision fields are source-backed. The record remains partial solely because teaching language is not explicit; the other listed items are documented semantic gaps rather than guessed facts.",
            "Bulunabilen tüm karar alanları kaynaklıdır. Kayıt yalnızca öğretim dili açık olmadığı için partial kalır; diğer listelenen öğeler tahmin edilmiş gerçekler değil belgelenmiş anlamsal boşluklardır.",
        ),
        "failed_canary_tests": ["teaching_language_not_explicitly_verified"],
    }

    DATA_PATH.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "id": row["id"],
        "status": row["data_quality"]["status"],
        "source_count": len(sources),
        "checked_official_source_count": row["data_quality"]["checked_official_source_count"],
        "unverified_critical_fields": row["data_quality"]["unverified_critical_fields"],
    }, indent=2))


if __name__ == "__main__":
    main()
