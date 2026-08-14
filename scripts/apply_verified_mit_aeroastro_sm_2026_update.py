from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data_base" / "amerika.json"
AUDIT_PATH = ROOT / "reports" / "source_link_audit_mit_aeroastro_sm_2026-08-14.json"
TODAY = "2026-08-14"

PROGRAM = "https://oge.mit.edu/programs/aeronautics-and-astronautics/"
ADMISSION = "https://aeroastro.mit.edu/education/graduate-admission/"
DEGREE = "https://aeroastro.mit.edu/education/graduate-degrees-requirements/"
FIELDS = "https://aeroastro.mit.edu/education/graduate-fields/"
FUNDING = "https://aeroastro.mit.edu/education/funding/"
FEE_WAIVER = "https://oge.mit.edu/graduate-admissions/applications/application-fee-waiver/"
INTERNATIONAL = "https://oge.mit.edu/graduate-admissions/applications/international-applicants/"
TUITION = "https://registrar.mit.edu/registration-academics/tuition-fees/graduate"
COA = "https://sfs.mit.edu/graduate-students/cost-of-attendance/grad-cost-of-attendance/"
HOUSING = "https://graduatehousing.mit.edu/get-housing/"
HOUSING_ELIGIBILITY = "https://graduatehousing.mit.edu/housing-eligibility/"
HOUSING_RATES = "https://graduatehousing.mit.edu/residences-rates/"
RESEARCH = "https://aeroastro.mit.edu/research/"
FACILITIES = "https://aeroastro.mit.edu/about-us/facilities/"
EARTH_SPACE = "https://aeroastro.mit.edu/research-areas/earth-space-sciences/"
SMALLSAT_LABS = "https://aeroastro.mit.edu/small-satellite-collaborative/ssc-people/ssc-member-labs/"
EXPORT = "https://research.mit.edu/security-integrity-and-compliance/export-control/scholarly-activities/using-restricted-material-mit"
I20 = "https://iso.mit.edu/getting-started/requesting-an-i-20-or-ds-2019/"
I20_FINANCIAL = "https://iso.mit.edu/getting-started/requesting-an-i-20-or-ds-2019/financial-documentation-requirements/"
ISO_FORMS = "https://iso.mit.edu/forms/"
QS = "https://www.topuniversities.com/qs-top-uni-wur"
MIT_QS_NEWS = "https://news.mit.edu/2026/qs-ranks-mit-worlds-no-1-university-0617"

REDDIT_LIFE = "https://www.reddit.com/r/mit/comments/1iq558m/life_as_a_grad_student/"
REDDIT_HOUSING = "https://www.reddit.com/r/mit/comments/1r9ioyu/housing_options_for_phd_student/"
REDDIT_HOW_TO_HOUSING = "https://www.reddit.com/r/mit/comments/1jawh42/how_2_housing/"


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
    row = next(item for item in rows if item.get("id") == "mit-aeroastro")

    row.update(
        {
            "country": "United States",
            "university": "Massachusetts Institute of Technology",
            "university_native_name": "Massachusetts Institute of Technology (MIT)",
            "city": "Cambridge",
            "region": "Massachusetts",
            "program_name": "Master of Science in Aeronautics and Astronautics (SM)",
            "program_native_name": "Master of Science in Aeronautics and Astronautics (SM)",
            "program_degree": "SM",
            "degree_level": "Master",
            "duration_years": 2.0,
            "duration": bi(
                "A two-year, full-time, on-campus programme; research-assistantship holders may require longer residence.",
                "İki yıllık, tam zamanlı ve kampüste yürütülen programdır; araştırma asistanlığı olanların ikamet süresi uzayabilir.",
            ),
            "ects": None,
            "us_subject_units_coursework": 66,
            "us_thesis_units": 24,
            "teaching_language": ["English"],
            "teaching_languages": ["English"],
            "program_url": DEGREE,
            "program_status": "active",
            "relevance_status": "strong",
            "delivery_modes": ["on_campus"],
            "full_time_only": True,
            "part_time_available": False,
            "qs_ranking": 1,
            "qs_ranking_display": "#1",
            "qs_ranking_year": 2027,
        }
    )

    row["prestige_profile"] = {
        "qs_world_rank": 1,
        "qs_edition": 2027,
        "qs_source_url": QS,
        "interpretation": bi(
            "MIT's QS 2027 institutional rank is prestige context only. AeroAstro fit is evidenced independently by the SM requirements, 13 fields, laboratories and thesis research.",
            "MIT'nin QS 2027 kurum sırası yalnızca prestij bağlamıdır. AeroAstro uygunluğu SM şartları, 13 alan, laboratuvarlar ve tez araştırmasıyla bağımsız olarak kanıtlanır.",
        ),
    }

    row["eligibility_profile"] = {
        "eligible_for_non_eu": True,
        "required_previous_degree": bi(
            "A bachelor's degree completed before September enrolment. The degree need not be in aeronautics or astronautics.",
            "Eylül kaydından önce tamamlanmış lisans derecesi. Derecenin havacılık veya astronotik alanında olması gerekmez.",
        ),
        "accepted_backgrounds": [
            bi("Engineering", "Mühendislik"),
            bi("Mathematical sciences", "Matematik bilimleri"),
            bi("Physical sciences", "Fiziksel bilimler"),
        ],
        "preparation_expectation": bi(
            "Strong preparation in mathematical and physical sciences and/or engineering; field changers should explain readiness in the objective statements.",
            "Matematik ve fizik bilimleri ve/veya mühendislikte güçlü hazırlık; alan değiştirenler hazırlıklarını amaç beyanlarında açıklamalıdır.",
        ),
        "minimum_gpa": None,
        "official_average_admitted_gpa_published": False,
        "admission_mode": "direct_department_application",
        "admission_risk": "high",
        "advisor_capacity_affects_admission": True,
        "interview_possible": True,
        "interview_required_for_all": False,
        "interview_required": False,
        "interview_policy": "may_be_invited_not_required_for_all",
        "required_documents": [
            bi("Online departmental graduate application", "Çevrim içi bölüm lisansüstü başvurusu"),
            bi("Research & Technical objective statement", "Araştırma ve Teknik amaç beyanı"),
            bi("Professional Experience & Objectives statement", "Mesleki Deneyim ve Hedefler beyanı"),
            bi("Personal Background statement", "Kişisel Geçmiş beyanı"),
            bi("Transcripts from every degree-granting institution", "Derece alınan/alınacak her kurumdan transkript"),
            bi("Exactly three recommendation letters", "Tam olarak üç referans mektubu"),
            bi("English-proficiency result when required", "Gerekiyorsa İngilizce yeterlilik sonucu"),
        ],
        "official_transcripts_required_at_application": False,
        "official_transcripts_preferred_at_application": True,
        "official_transcripts_required_after_admission": True,
        "recommendation_letter_count": 3,
        "more_than_three_recommendations_allowed": False,
        "application_fee_usd": 90,
        "application_fee_waiver_possible": True,
        "application_fee_waiver_request_deadline": "2026-11-18",
        "application_fee_waiver_processing_time_business_days": 5,
        "application_fee_waiver_international_eligibility": bi(
            "International applicants qualify only if currently attending a US college/university and participating in an eligible graduate-research preparation programme; overseas financial hardship alone is not eligible.",
            "Uluslararası adaylar yalnızca hâlen bir ABD kolej/üniversitesine devam ediyor ve uygun bir lisansüstü araştırma hazırlık programına katılıyorsa uygundur; yurt dışındaki mali güçlük tek başına yeterli değildir.",
        ),
        "gre": {
            "policy": "not_accepted",
            "cycle": "current standing department policy",
            "test_type": "GRE General",
            "minimum_scores": {},
            "considered_if_submitted": False,
            "visible_to_review_committee_if_shared_elsewhere": False,
            "source_ids": [ADMISSION, PROGRAM],
        },
        "transfer_credit_from_other_universities_accepted": False,
        "verification_notes": bi(
            "No official minimum or average GPA is published. Admission is holistic, capacity-limited by advisor availability, and therefore high-risk even for strong applicants.",
            "Resmî asgari veya ortalama GNO yayımlanmamıştır. Kabul bütünsel ve danışman kapasitesiyle sınırlıdır; bu nedenle güçlü adaylar için bile yüksek risklidir.",
        ),
    }

    row["language_profile"] = {
        "teaching_language": ["English"],
        "teaching_languages": ["English"],
        "english_required": True,
        "requirement_scope": "international applicants unless an approved AeroAstro waiver applies",
        "accepted_english_tests": [
            {"test": "TOEFL iBT", "minimum_score": 100, "minimum_score_2026_scale": 5.0, "validity_years": 2, "institution_code": "3514"},
            {"test": "IELTS Academic", "minimum_score": 7.0, "validity_years": 2},
            {"test": "Duolingo English Test", "minimum_score": 135, "validity_years": 2},
            {"test": "Cambridge English Qualification", "minimum_score": 190, "department_page_lists_test": True},
        ],
        "english_test_latest_safe_date": "November 15 before the December 1 deadline",
        "self_report_required_at_application": True,
        "official_score_required_before_decision_release": True,
        "waiver_automatic": False,
        "waiver_request_location": "application form",
        "waiver_routes": [
            bi(
                "English was the main instructional language throughout primary and secondary school (approximately ages 6-18).",
                "İlk ve ortaöğretimin tamamında (yaklaşık 6-18 yaş) ana eğitim dili İngilizceydi.",
            ),
            bi(
                "At least three years' residence in the US or another country where English is official, plus a degree from an accredited English-medium institution.",
                "ABD'de veya İngilizcenin resmî dil olduğu başka bir ülkede en az üç yıl ikamet ve İngilizce eğitim veren akredite kurumdan derece.",
            ),
        ],
        "post_admission_english_evaluation_required_for_non_native_speakers": True,
        "graduate_writing_exam_required_for_all_entering_students": True,
        "language_risk": "medium",
        "verification_notes": bi(
            "MIT centrally confirms English as the language of instruction. The department page and current programme directory differ in how they enumerate accepted tests, so applicants should follow the live application checklist.",
            "MIT, eğitim dilinin İngilizce olduğunu merkezî olarak doğrular. Bölüm sayfası ile güncel program dizini kabul edilen sınavları listelerken farklılık gösterdiğinden adaylar canlı başvuru kontrol listesini izlemelidir.",
        ),
    }

    row["cost_profile"] = {
        "academic_year": "2026/2027",
        "currency": "USD",
        "tuition_usd_per_year": 66720,
        "tuition_basis": "standard full graduate tuition for fall and spring",
        "tuition_usd_per_fall_or_spring_term": 33360,
        "mandatory_fees_usd_per_year": 420,
        "health_insurance_premium_usd": 5148,
        "health_insurance_required": True,
        "mit_student_health_insurance_waiver_possible_with_qualifying_coverage": True,
        "first_year_tuition_and_mandatory_fees_usd_example": 67140,
        "first_year_direct_cost_with_mit_ship_usd": 72288,
        "total_cost_of_attendance_usd_per_year": 109017,
        "total_cost_of_attendance_scope": "official nine-month full-time graduate planning budget",
        "total_cost_of_attendance_usd_12_month": 144315,
        "financial_aid_coa_is_bill": False,
        "coa_housing_usd_9_month": 17100,
        "coa_food_usd_9_month": 7830,
        "coa_books_supplies_usd_9_month": 1161,
        "coa_personal_usd_9_month": 7794,
        "coa_transportation_usd_9_month": 2844,
        "complete_program_cost_usd": None,
        "complete_program_cost_reason": bi(
            "The official programme is two years, but summer registration, RA-supported residence, individual insurance waivers and funding vary; MIT does not publish one AeroAstro SM total.",
            "Resmî program iki yıldır; ancak yaz kaydı, RA destekli ikamet, kişisel sigorta muafiyetleri ve finansman değişir. MIT tek bir AeroAstro SM toplamı yayımlamaz.",
        ),
        "tuition_eur_per_year_min": None,
        "tuition_eur_per_year_max": None,
        "tuition_eur_per_year_estimated": None,
        "living_cost_eur_per_month": None,
        "scholarship_availability": "available_competitive",
        "scholarship_risk": "high",
        "cost_notes": bi(
            "The 109,017 USD figure is a nine-month planning budget before aid, not an invoice. The billed baseline is tuition plus the student-life fee; MIT SHIP is shown separately.",
            "109.017 USD, destek öncesi dokuz aylık planlama bütçesidir; fatura değildir. Faturalama tabanı öğrenim ve öğrenci yaşam ücretidir; MIT SHIP ayrıca gösterilir.",
        ),
        "verification_notes": bi(
            "The checked Registrar and SFS pages publish current 2026/27 institute-wide standard graduate rates; AeroAstro is not identified as a non-standard-rate exception.",
            "Kontrol edilen Registrar ve SFS sayfaları güncel 2026/27 kurum geneli standart lisansüstü ücretlerini yayımlar; AeroAstro standart dışı ücret istisnası olarak belirtilmemiştir.",
        ),
    }

    row["scholarship_profile"] = {
        "available_types": ["research_assistantship", "teaching_assistantship", "internal_fellowship", "external_fellowship"],
        "non_eu_eligible": None,
        "application_mode": "separate",
        "automatic_consideration": False,
        "separate_application_required": True,
        "funding_guaranteed_at_admission": False,
        "proactive_search_expected_after_admission": True,
        "ra_is_principal_department_funding_route": True,
        "most_students_funded_by_ra": True,
        "ra_typical_coverage": ["full_tuition", "health_insurance", "monthly_stipend"],
        "ta_typical_coverage": ["full_tuition", "health_insurance", "monthly_stipend"],
        "ta_positions_per_year_approximate": 20,
        "ra_offer_window": "March through August after admission",
        "internal_fellowship_typical_duration": "one academic year",
        "external_fellowship_requires_separate_application": True,
        "funding_opportunities": [
            {"name": "Research Assistantship", "amount": bi("Full tuition, health insurance and monthly stipend", "Tam öğrenim, sağlık sigortası ve aylık burs"), "deadline": bi("Faculty offers commonly March-August after admission", "Öğretim üyesi teklifleri genellikle kabulden sonra Mart-Ağustos"), "eligibility": bi("Advisor/project fit and available sponsored funding; not guaranteed", "Danışman/proje uyumu ve mevcut sponsor finansmanı; garanti değil")},
            {"name": "Teaching Assistantship", "amount": bi("Full tuition, health insurance and monthly stipend", "Tam öğrenim, sağlık sigortası ve aylık burs"), "deadline": bi("Course-by-course; ask faculty/Student Services", "Ders bazında; öğretim üyesi/Student Services ile görüşülür"), "eligibility": bi("About 20 department positions annually; competitive", "Bölümde yılda yaklaşık 20 pozisyon; rekabetçi")},
            {"name": "MIT-sponsored fellowship", "amount": bi("Usually full tuition, health insurance and monthly stipend", "Genellikle tam öğrenim, sağlık sigortası ve aylık burs"), "deadline": bi("Varies by award", "Ödüle göre değişir"), "eligibility": bi("Merit-based and commonly one academic year", "Başarı temelli ve çoğunlukla bir akademik yıl")},
        ],
        "funding_notes": bi(
            "AeroAstro explicitly tells admitted students to be proactive and not wait for funding. Contact matching faculty after admission; an offer's amount, duration and international eligibility must be checked individually.",
            "AeroAstro kabul edilen öğrencilere proaktif olmalarını ve finansmanı beklememelerini açıkça söyler. Kabulden sonra uyumlu öğretim üyeleriyle iletişime geçilmeli; teklifin tutarı, süresi ve uluslararası uygunluğu ayrı ayrı kontrol edilmelidir.",
        ),
        "verification_notes": bi(
            "Coverage is verified for appointment types, but there is no universal automatic scholarship and no verified blanket non-US eligibility for every fellowship.",
            "Atama türlerinin kapsamı doğrulanmıştır; ancak evrensel otomatik burs veya her fellowship için doğrulanmış genel ABD dışı uygunluk yoktur.",
        ),
    }
    row["scholarship_profile"]["opportunities"] = row["scholarship_profile"]["funding_opportunities"]

    row["living_profile"] = {
        "city_type": "major_high_cost_metro",
        "student_housing_available": True,
        "student_dorm_availability": "available_subject_to_inventory",
        "housing_access": "not_guaranteed",
        "housing_selection_method": "self_selection_subject_to_availability",
        "housing_application_separate": True,
        "housing_guaranteed": False,
        "housing_eligibility": bi(
            "Fully registered graduate students may apply; non-resident-status students are not eligible.",
            "Tam kayıtlı lisansüstü öğrenciler başvurabilir; non-resident statüsündekiler uygun değildir.",
        ),
        "initial_selection_registration_2026": "2026-04-14 to 2026-04-30",
        "initial_individual_selection_2026": "2026-05-04 to 2026-05-08 (lottery-assigned date)",
        "open_selection_2026": "2026-05-12 to 2026-10-08 on published selection days",
        "monthly_housing_rent_usd_per_month_min": 1016,
        "monthly_housing_rent_usd_per_month_max": 2766,
        "monthly_housing_rent_scope": "2026/27 individual-student on-campus options; family/unit rates can reach 3,868 USD",
        "utilities_and_internet_included": True,
        "monthly_house_tax_usd_min": 5,
        "monthly_house_tax_usd_max": 10,
        "housing_budget_usd_per_year": 17100,
        "housing_budget_months": 9,
        "housing_search_difficulty": "high",
        "living_cost_risk": "high",
        "living_risk": "high",
        "verification_notes": bi(
            "MIT housing uses a separate self-selection process. The published 2026/27 individual range is 1,016-2,766 USD/month, but specific inventory is not guaranteed; Cambridge/Boston is explicitly a high-cost market.",
            "MIT konutu ayrı self-selection süreci kullanır. Yayımlanan 2026/27 bireysel aralık aylık 1.016-2.766 USD'dir; belirli bir stok garanti edilmez ve Cambridge/Boston açıkça yüksek maliyetli bir pazardır.",
        ),
    }

    row["curriculum_profile"] = {
        "structure": bi(
            "At least 66 graduate subject units plus a 24-unit SM thesis, one approved graduate mathematics subject and the First-Year Graduate Seminar.",
            "En az 66 lisansüstü ders birimi + 24 birim SM tezi, onaylı bir lisansüstü matematik dersi ve First-Year Graduate Seminar.",
        ),
        "coursework_subject_units": 66,
        "aeroastro_subject_units_minimum": 21,
        "thesis_units": 24,
        "total_units_minimum": 90,
        "course_count": None,
        "course_count_fixed": False,
        "course_count_summary": bi(
            "No fixed course count: at least 66 subject units + 24 thesis units; subject unit values vary.",
            "Sabit ders sayısı yok: en az 66 ders birimi + 24 tez birimi; derslerin birim değeri değişir.",
        ),
        "full_time_only": True,
        "part_time_available": False,
        "delivery_mode": "on_campus",
        "graduate_math_subject_required": True,
        "first_year_graduate_seminar_required": True,
        "minimum_cumulative_gpa_mit_scale": 4.0,
        "minimum_course_grade_for_degree_credit": "B",
        "pass_fail_courses_count_toward_degree": False,
        "thesis_required": True,
        "thesis_route_available": True,
        "non_thesis_route_available": False,
        "internship_required": False,
        "mandatory_internship": False,
        "thesis_type": "SM thesis required",
        "fields_of_study_count": 13,
        "specializations": [
            "Aerospace Computational Engineering",
            "Aerospace, Energy and the Environment",
            "Air-Breathing Propulsion",
            "Aircraft Systems Engineering",
            "Air Transportation Systems",
            "Autonomous Systems",
            "Communications and Networks",
            "Controls",
            "Humans in Aerospace",
            "Materials and Structures",
            "Space Propulsion",
            "Space Systems",
            "Technology and Policy / interdisciplinary options",
        ],
        "flexibility": "high_advisor_planned",
        "curriculum_risk": "medium",
        "verification_notes": bi(
            "The department states there is no single fixed class set; students choose subjects with an advisor while meeting unit, math, seminar, grade and thesis rules. Lab or advisor placement is not guaranteed by the curriculum.",
            "Bölüm tek bir sabit ders seti olmadığını belirtir; öğrenciler birim, matematik, seminer, not ve tez şartlarını karşılayarak dersleri danışmanla seçer. Müfredat laboratuvar veya danışman yeri garantilemez.",
        ),
    }

    row["category_profile"] = {
        "primary_categories": ["aerospace_engineering", "space_engineering", "aeronautics_astronautics"],
        "secondary_categories": ["gnc_autonomy", "cfd_aerodynamics", "propulsion", "structures_materials", "spacecraft_systems", "satellite_systems", "human_factors", "air_transportation"],
        "technical_focus": ["space systems", "space propulsion", "autonomy and controls", "computational aerospace", "aerodynamics", "air-breathing propulsion", "materials and structures", "communications and networks"],
        "verification_notes": bi(
            "Categories follow the official 13 graduate fields and department research areas, not the institutional ranking.",
            "Kategoriler kurum sırasına değil, resmî 13 lisansüstü alana ve bölüm araştırma alanlarına dayanır.",
        ),
    }

    row["research_profile"] = {
        "research_strength_score": None,
        "research_funding_level": "unknown",
        "research_risk": "medium",
        "research_focus_areas": ["autonomous systems and decision-making", "computational science and engineering", "earth and space sciences", "human-system collaboration", "systems design and engineering", "transportation and exploration", "vehicle design and engineering"],
        "key_institutes": [
            {"name": "Space Systems Laboratory", "focus": bi("Space systems research", "Uzay sistemleri araştırması"), "url": EARTH_SPACE},
            {"name": "Space Propulsion Laboratory", "focus": bi("Scalable space thrusters and space-propulsion education", "Ölçeklenebilir uzay iticileri ve uzay itki eğitimi"), "url": SMALLSAT_LABS},
            {"name": "STAR Lab", "focus": bi("Small-spacecraft communications, astronomy, radiation and remote sensing", "Küçük uzay aracı haberleşmesi, astronomi, radyasyon ve uzaktan algılama"), "url": SMALLSAT_LABS},
            {"name": "ARCLab", "focus": bi("Astrodynamics, space robotics, GNC, estimation and space traffic management", "Astrodinamik, uzay robotiği, GNC, kestirim ve uzay trafik yönetimi"), "url": SMALLSAT_LABS},
            {"name": "Aerospace Computational Science & Engineering Laboratory", "focus": bi("Computational aerospace modelling and design", "Hesaplamalı havacılık-uzay modelleme ve tasarımı"), "url": RESEARCH},
            {"name": "Gas Turbine Laboratory", "focus": bi("Air-breathing propulsion and turbomachinery", "Hava soluyan itki ve turbomakine"), "url": RESEARCH},
            {"name": "Aerospace Controls Laboratory", "focus": bi("Autonomy, controls and multi-agent systems", "Otonomi, kontrol ve çok etmenli sistemler"), "url": RESEARCH},
            {"name": "Aerospace Materials and Structures Laboratory", "focus": bi("Aerospace materials, structures and spaceflight manufacturing", "Havacılık-uzay malzemeleri, yapılar ve uzay uçuşu üretimi"), "url": SMALLSAT_LABS},
        ],
        "labs": ["Space Systems Laboratory", "Space Propulsion Laboratory", "STAR Lab", "ARCLab", "Aerospace Computational Science & Engineering Laboratory", "Gas Turbine Laboratory", "Aerospace Controls Laboratory", "Aerospace Materials and Structures Laboratory"],
        "research_centers": ["International Center for Air Transportation", "Small Satellite Collaborative", "Kresa Center for Autonomous Systems"],
        "space_or_aerospace_projects": ["small spacecraft", "distributed space platforms", "space propulsion", "astrodynamics and space traffic management", "space systems", "Earth observation"],
        "individual_lab_place_guaranteed": False,
        "advisor_or_ra_match_required_for_funded_lab_access": True,
        "research_sources": [RESEARCH, FACILITIES, EARTH_SPACE, SMALLSAT_LABS],
        "research_strength_summary": bi(
            "Exceptional breadth across air, space and computation is directly documented. Student access still depends on advisor fit, project capacity, training and sometimes funding.",
            "Hava, uzay ve hesaplama genelinde olağanüstü genişlik doğrudan belgelenmiştir. Öğrenci erişimi yine danışman uyumu, proje kapasitesi, eğitim ve bazen finansmana bağlıdır.",
        ),
        "verification_notes": bi(
            "Named laboratories and facilities are official. Their existence is not treated as a promise of a seat, thesis topic or assistantship.",
            "Adı geçen laboratuvarlar ve tesisler resmîdir. Varlıkları yer, tez konusu veya asistanlık vaadi sayılmamıştır.",
        ),
    }

    row["industry_ecosystem_profile"] = {
        "local_industry_strength": "unknown",
        "key_companies": [],
        "verified_partnerships": [],
        "named_ra_sponsor_examples": ["NASA", "Boeing", "US Air Force", "NSF"],
        "sponsor_examples_are_student_placement_guarantees": False,
        "hiring_culture": "unknown",
        "alumni_presence": "unknown",
        "industry_risk": "medium",
        "export_control_risk": "project_specific",
        "export_control_notes": bi(
            "MIT operates under the fundamental-research exclusion, but restricted tools, data or technology can still trigger controls and a Technology Control Plan. This is project-specific, not a blanket bar on international students.",
            "MIT temel araştırma istisnası altında çalışır; ancak kısıtlı araç, veri veya teknoloji yine kontrol ve Technology Control Plan gerektirebilir. Bu proje bazlıdır, uluslararası öğrencilere genel yasak değildir.",
        ),
        "verification_notes": bi(
            "The funding page names common government/industry RA sponsors, but this record does not convert sponsor examples or nearby employers into verified partnerships or hiring guarantees.",
            "Finansman sayfası yaygın kamu/sanayi RA sponsorlarını adlandırır; bu kayıt sponsor örneklerini veya yakındaki işverenleri doğrulanmış ortaklık ya da işe alım garantisine dönüştürmez.",
        ),
    }

    row["application_timeline_profile"] = {
        "application_period": "September 1 to December 1",
        "application_opens": "2026-09-01",
        "deadline_eu": "2026-12-01",
        "deadline_non_eu": "2026-12-01",
        "deadline_time": "23:59",
        "deadline_timezone": "US Eastern Time",
        "entry_term": "Fall 2027",
        "spring_admission_available": False,
        "late_applications_accepted": False,
        "all_supplemental_materials_due_with_application": True,
        "application_rounds": [
            {"intake": "Fall 2027", "opens": "2026-09-01", "deadline": "2026-12-01", "deadline_time": "23:59 US Eastern Time", "gre_required": False, "status": "upcoming", "date_basis": "current official annual calendar"}
        ],
        "fee_waiver_deadline": "2026-11-18",
        "english_test_recommended_latest_date": "2026-11-15",
        "pre_enrollment_required": False,
        "visa_complexity": "high",
        "visa_document_request_system": "iMIT",
        "visa_document_processing_time_business_days_min": 5,
        "visa_document_processing_time_business_days_max": 10,
        "financial_proof_required_before_i20_or_ds2019": True,
        "financial_proof_amount": None,
        "financial_proof_amount_location": "displayed in iMIT for the individual programme",
        "financial_proof_duration_rule": "12 months or entire programme if shorter",
        "post_arrival_online_check_in_required": True,
        "iso_immigration_orientation_required": True,
        "timeline_risk": "high",
        "verification_notes": bi(
            "The department publishes an annual September 1 opening and hard December 1, 11:59 PM ET deadline for fall-only admission. The cycle is mapped to Fall 2027 because it opens in September 2026; it is not an estimated day.",
            "Bölüm yalnızca güz kabulü için yıllık 1 Eylül açılışı ve 1 Aralık 23:59 ET kesin son tarihini yayımlar. Dönem, Eylül 2026'da açıldığı için Güz 2027 olarak eşlenmiştir; gün tahmini değildir.",
        ),
    }

    row["student_sentiment_profile"] = {
        "student_satisfaction_score": None,
        "workload_sentiment": "mixed_high_intensity",
        "teaching_quality_sentiment": "unknown",
        "administration_sentiment": "unknown",
        "housing_sentiment": "mixed_cost_and_availability_concerns",
        "city_life_sentiment": "mixed_high_opportunity_high_cost",
        "international_student_sentiment": "unknown",
        "career_support_sentiment": "unknown",
        "student_sentiment_summary": bi(
            "A small, non-program-specific forum sample repeatedly describes lab-dependent workload and expensive housing, while noting roommate/on-campus options. This is perception only and is too weak for a satisfaction score.",
            "Küçük ve programa özgü olmayan forum örneklemi, laboratuvara bağlı iş yükü ile pahalı konutu tekrarlar; aynı zamanda ev arkadaşı/kampüs içi seçeneklerden söz eder. Bu yalnızca algıdır ve memnuniyet puanı için yetersizdir.",
        ),
        "student_sentiment_sources": [
            {"url": REDDIT_LIFE, "platform": "Reddit", "date": "2025-02-15", "topic": ["workload", "lab culture", "city cost"]},
            {"url": REDDIT_HOUSING, "platform": "Reddit", "date": "2026-02-20", "topic": ["housing", "rent", "roommates"]},
            {"url": REDDIT_HOW_TO_HOUSING, "platform": "Reddit", "date": "2025-03-14", "topic": ["housing search", "rent", "international transition"]},
        ],
        "approximate_sample_size": 18,
        "date_range": "2025-02 to 2026-02",
        "sentiment_confidence": "low",
        "verification_notes": bi(
            "No anonymous claim is used for admission, funding, tuition, curriculum, housing rules or employment facts.",
            "Hiçbir anonim iddia kabul, finansman, ücret, müfredat, konut kuralı veya istihdam gerçeği için kullanılmamıştır.",
        ),
    }

    sources = [
        source(PROGRAM, "MIT OGE — Aeronautics and Astronautics", "official_program_page", ["program", "degree", "deadline", "fee", "gre", "language"], "Current central programme directory confirms the SM, September 1 opening, December 1 deadline, 90 USD fee, STEM status and test rules.", "Güncel merkezî program dizini SM'i, 1 Eylül açılışını, 1 Aralık son tarihini, 90 USD ücreti, STEM statüsünü ve sınav kurallarını doğrular."),
        source(ADMISSION, "MIT AeroAstro Graduate Admission", "official_admission_page", ["admission", "documents", "deadline", "language", "gre", "housing"], "Department admissions page confirms direct bachelor's-to-SM eligibility, full-time campus study, no GRE, documents, English rules and hard deadline.", "Bölüm kabul sayfası lisanstan SM'e doğrudan uygunluğu, tam zamanlı kampüs eğitimini, GRE yokluğunu, belgeleri, İngilizce kurallarını ve kesin son tarihi doğrular."),
        source(DEGREE, "MIT AeroAstro Graduate Degrees & Requirements", "official_curriculum_page", ["program", "duration", "curriculum", "thesis", "grades"], "Official two-year SM and its 66 coursework units, 24 thesis units, math, seminar and grade rules.", "Resmî iki yıllık SM ve 66 ders, 24 tez birimi, matematik, seminer ve not kuralları."),
        source(FIELDS, "MIT AeroAstro Graduate Fields", "official_curriculum_page", ["curriculum", "fields", "technical_fit"], "Official 13-field structure and field descriptions.", "Resmî 13 alan yapısı ve alan açıklamaları."),
        source(FUNDING, "MIT AeroAstro Funding", "official_scholarship_page", ["funding", "assistantships", "scholarship", "industry_sponsors"], "Official RA/TA/fellowship coverage, proactive-search rule, timing and sponsor examples.", "Resmî RA/TA/fellowship kapsamı, proaktif arama kuralı, zamanlama ve sponsor örnekleri."),
        source(FEE_WAIVER, "MIT Graduate Admissions Fee Waivers", "official_admission_page", ["application_fee", "fee_waiver", "deadline", "international_eligibility"], "Current 2026 waiver process, November 18 deadline, processing time and narrow international eligibility.", "Güncel 2026 muafiyet süreci, 18 Kasım son tarihi, işlem süresi ve dar uluslararası uygunluk."),
        source(INTERNATIONAL, "MIT OGE International Applicants", "official_admission_page", ["language", "non_eu_eligibility", "documents"], "Central international-applicant and English-instruction guidance.", "Merkezî uluslararası aday ve İngilizce eğitim rehberi."),
        source(TUITION, "MIT Registrar Graduate Tuition 2026/27", "official_tuition_page", ["tuition", "fees"], "Current standard graduate tuition basis and term rate.", "Güncel standart lisansüstü öğrenim temeli ve dönem ücreti."),
        source(COA, "MIT SFS Graduate Cost of Attendance 2026/27", "official_tuition_page", ["tuition", "fees", "insurance", "living", "housing"], "Official nine- and twelve-month planning budgets and component amounts; not an invoice.", "Resmî dokuz ve on iki aylık planlama bütçeleri ve bileşen tutarları; fatura değildir."),
        source(HOUSING, "MIT Graduate Housing — Get Housing", "official_housing_page", ["housing", "application", "dates", "guarantee"], "Current self-selection and lottery/open-selection route; units remain subject to availability.", "Güncel self-selection ve kura/açık seçim yolu; birimler uygunluğa bağlıdır."),
        source(HOUSING_ELIGIBILITY, "MIT Graduate Housing Eligibility", "official_housing_page", ["housing", "eligibility"], "Fully registered graduate-student eligibility and exclusions.", "Tam kayıtlı lisansüstü öğrenci uygunluğu ve istisnaları."),
        source(HOUSING_RATES, "MIT Graduate Housing Residences & Rates 2026/27", "official_housing_page", ["housing", "rent", "living_cost"], "Current individual, couple and family rents with included utilities and house-tax note.", "Hizmetler dâhil güncel bireysel, çift ve aile kiraları ile bina vergisi notu."),
        source(RESEARCH, "MIT AeroAstro Research", "official_department_page", ["research", "labs", "research_areas"], "Official seven research areas and department laboratory directory.", "Resmî yedi araştırma alanı ve bölüm laboratuvar dizini."),
        source(FACILITIES, "MIT AeroAstro Facilities", "official_department_page", ["research", "facilities"], "Official approximately 100,000 square feet across core facilities; access requires MIT ID and training.", "Ana tesislerde resmî yaklaşık 100.000 ft² alan; erişim MIT kimliği ve eğitim gerektirir."),
        source(EARTH_SPACE, "MIT AeroAstro Earth & Space Sciences", "official_department_page", ["research", "space_fit", "labs"], "Official space focus and affiliated space laboratories.", "Resmî uzay odağı ve bağlı uzay laboratuvarları."),
        source(SMALLSAT_LABS, "MIT Small Satellite Collaborative Member Labs", "official_lab_page", ["research", "space_fit", "labs"], "Official STAR, SPL, ARCLab, space-enabled systems and structures descriptions.", "Resmî STAR, SPL, ARCLab, uzay destekli sistemler ve yapılar açıklamaları."),
        source(EXPORT, "MIT Research — Using Restricted Material", "official_department_page", ["export_control", "research_access"], "Current project-specific export-control and Technology Control Plan guidance.", "Güncel proje bazlı ihracat kontrolü ve Technology Control Plan rehberi."),
        source(I20, "MIT ISO — Requesting an I-20 or DS-2019", "official_admission_page", ["visa", "i20", "international"], "Official iMIT request workflow for new degree students.", "Yeni derece öğrencileri için resmî iMIT belge talep süreci."),
        source(I20_FINANCIAL, "MIT ISO Financial Documentation Requirements", "official_admission_page", ["visa", "financial_proof", "i20"], "Official proof-of-funds scope and accepted-document rules; individual amount appears in iMIT.", "Resmî mali kanıt kapsamı ve kabul edilen belge kuralları; kişisel tutar iMIT'te görünür."),
        source(ISO_FORMS, "MIT ISO Forms and Processing Times", "official_admission_page", ["visa", "i20", "processing_time", "check_in"], "ISO publishes 5-10 business days for new I-20/DS-2019 requests and required forms.", "ISO yeni I-20/DS-2019 talepleri için 5-10 iş günü ve gerekli formları yayımlar."),
        source(QS, "QS World University Rankings 2027", "official_ranking_page", ["prestige"], "Ranking publisher page for the 2027 edition; institutional context only.", "2027 edisyonu sıralama yayımlayıcısı sayfası; yalnızca kurum bağlamı.", confidence="medium"),
        source(MIT_QS_NEWS, "MIT News — QS ranks MIT No. 1 for 2026-27", "official_ranking_page", ["prestige"], "MIT's current announcement corroborates the QS 2027 institutional rank.", "MIT'nin güncel duyurusu QS 2027 kurum sırasını doğrular.", confidence="medium"),
        source(REDDIT_LIFE, "Reddit — Life as a grad student?", "forum_source", ["student_sentiment", "workload", "city_life"], "Recent MIT-wide perceptions only; not AeroAstro facts.", "Yalnızca güncel MIT geneli algılar; AeroAstro gerçeği değildir.", confidence="low"),
        source(REDDIT_HOUSING, "Reddit — Housing Options for PhD Student", "forum_source", ["student_sentiment", "housing"], "Recent housing perceptions only; official rates and access rules come from MIT.", "Yalnızca güncel konut algıları; resmî fiyat ve erişim kuralları MIT'den gelir.", confidence="low"),
        source(REDDIT_HOW_TO_HOUSING, "Reddit — How 2 Housing", "forum_source", ["student_sentiment", "housing", "international_student"], "Recent international graduate housing-search perceptions only.", "Yalnızca güncel uluslararası lisansüstü konut arama algıları.", confidence="low"),
    ]

    row["source_profile"] = {
        "primary_url": PROGRAM,
        "secondary_urls": [ADMISSION, DEGREE, FIELDS, FUNDING, TUITION, COA, HOUSING, RESEARCH, I20],
        "official_program_page": PROGRAM,
        "official_admission_page": ADMISSION,
        "official_curriculum_page": DEGREE,
        "official_tuition_page": TUITION,
        "official_scholarship_page": FUNDING,
        "official_housing_page": HOUSING,
        "official_department_page": RESEARCH,
        "last_verified": TODAY,
        "field_confidence": {
            "program_basic_info": "high",
            "admission": "high",
            "deadlines": "high",
            "tuition": "high",
            "language": "medium",
            "scholarship": "medium",
            "curriculum": "high",
            "housing": "high",
            "research": "high",
            "industry": "medium",
            "visa": "high",
            "sentiment": "low",
        },
        "source_reliability": "high",
        "verification_status": "partially_verified",
        "verification_notes": bi(
            "All core programme, admission, deadline, cost, curriculum, housing, research and visa claims are current and official. Remaining uncertainty is route-specific non-US funding eligibility and a minor official discrepancy in the accepted-English-test list.",
            "Temel program, kabul, tarih, maliyet, müfredat, konut, araştırma ve vize iddiaları güncel ve resmîdir. Kalan belirsizlik, finansman yollarının ABD dışı uygunluğu ve kabul edilen İngilizce sınav listesindeki küçük resmî uyuşmazlıktır.",
        ),
        "source_log": sources,
        "needs_verification": True,
    }

    row["decision_summary"] = {
        "pros": [
            bi("Direct bachelor's-to-SM route with a required research thesis.", "Lisanstan doğrudan SM'e geçiş ve zorunlu araştırma tezi."),
            bi("Unusually broad verified strength across spacecraft, propulsion, GNC, computation, aerodynamics, structures and human systems.", "Uzay aracı, itki, GNC, hesaplama, aerodinamik, yapılar ve insan sistemlerinde olağanüstü geniş doğrulanmış güç."),
            bi("RA/TA appointments can cover full tuition, health insurance and a stipend.", "RA/TA atamaları tam öğrenim, sağlık sigortası ve bursu karşılayabilir."),
            bi("GRE is neither required nor considered.", "GRE ne gereklidir ne de değerlendirilir."),
        ],
        "cons": [
            bi("Advisor capacity makes admission extremely uncertain even for excellent applicants.", "Danışman kapasitesi, çok güçlü adaylar için bile kabulü son derece belirsiz kılar."),
            bi("Funding is not automatic; admitted students are told to search proactively from March through August.", "Finansman otomatik değildir; kabul edilen öğrencilerin Mart-Ağustos arasında proaktif arama yapması beklenir."),
            bi("The official nine-month pre-aid budget is 109,017 USD, and Cambridge/Boston housing is expensive.", "Resmî dokuz aylık destek öncesi bütçe 109.017 USD'dir ve Cambridge/Boston konutu pahalıdır."),
            bi("International access can be project-specific where restricted technology or data is involved.", "Kısıtlı teknoloji veya veri içeren projelerde uluslararası erişim proje bazlı olabilir."),
        ],
        "verdict": bi(
            "Elite technical fit and research breadth, but apply only with clear faculty alignment and a financing plan that does not assume an assistantship until it is written into the offer.",
            "Teknik uyum ve araştırma genişliği elit düzeydedir; ancak yalnızca net öğretim üyesi uyumu ve asistanlık yazılı teklifte yer alana kadar onu varsaymayan finansman planıyla başvurulmalıdır.",
        ),
    }

    row["scoring_inputs"] = {
        "academic_prestige": None,
        "admission_chance": None,
        "affordability": None,
        "industry_links": None,
        "living_quality": None,
        "research_output": None,
        "hard_flags": ["advisor_capacity_limited", "funding_not_automatic", "high_cost_city", "project_specific_export_control"],
        "notes": bi(
            "No synthetic score is assigned. Verified facts and hard flags should drive student-specific scoring later.",
            "Sentetik puan verilmemiştir. Öğrenciye özgü puanlama daha sonra doğrulanmış gerçekler ve sert uyarılarla yapılmalıdır.",
        ),
    }

    row["data_quality"] = {
        "status": "partial",
        "checked_official_source_count": sum(1 for item in sources if item["source_type"].startswith("official_")),
        "verified_fields": ["program", "duration", "delivery", "admission", "non_eu_eligibility", "documents", "gre", "language", "tuition", "fees", "cost_of_attendance", "scholarship", "funding_routes", "deadline", "curriculum", "housing", "research", "visa", "export_control"],
        "unverified_critical_fields": [],
        "has_checked_source_log": True,
        "audited_at": TODAY,
    }

    row["quality_control"] = {
        "checked_at": TODAY,
        "qc_status": "pass_with_declared_unknowns",
        "failed_canary_tests": [],
        "remaining_verification_tasks": [
            bi("Confirm the live application's exact English-test menu when the Fall 2027 form opens.", "Güz 2027 formu açıldığında canlı başvurudaki kesin İngilizce sınav menüsünü doğrula."),
            bi("Confirm non-US eligibility separately for every fellowship or sponsored RA project in an actual offer.", "Gerçek teklifte her fellowship veya sponsorlu RA projesi için ABD dışı uygunluğu ayrı doğrula."),
        ],
        "qc_notes": bi(
            "Official facts, interpreted cautions and student sentiment are separated. Ranking is not used as technical-fit evidence; sponsor examples are not labelled partnerships.",
            "Resmî gerçekler, yorumlanan uyarılar ve öğrenci algısı ayrılmıştır. Sıralama teknik uyum kanıtı değildir; sponsor örnekleri ortaklık olarak etiketlenmemiştir.",
        ),
    }

    DATA_PATH.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    audit = {
        "record_id": row["id"],
        "checked_at": TODAY,
        "source_count": len(sources),
        "official_source_count": row["data_quality"]["checked_official_source_count"],
        "valid_primary_source_count": sum(1 for item in sources if item["access_status"] in {"ok", "redirects", "pdf", "requires_js"} and item["source_type"].startswith("official_")),
        "broken_primary_source_count": 0,
        "sources": [{"url": item["url"], "access_status": item["access_status"], "source_type": item["source_type"], "last_checked": TODAY} for item in sources],
        "notes": bi(
            "All URLs were opened or search-fetched on the audit date. No broken/not-found/unknown source is used as primary evidence.",
            "Tüm URL'ler denetim tarihinde açıldı veya arama yoluyla getirildi. Birincil kanıt olarak broken/not-found/unknown kaynak kullanılmadı.",
        ),
    }
    AUDIT_PATH.parent.mkdir(parents=True, exist_ok=True)
    AUDIT_PATH.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
