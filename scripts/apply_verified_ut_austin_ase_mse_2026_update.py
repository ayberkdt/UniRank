from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data_base" / "amerika.json"
TODAY = "2026-08-14"

PROGRAM = "https://ae.utexas.edu/academics/graduate/graduate-programs/ase-grad-program/"
ADMISSION = "https://ae.utexas.edu/academics/graduate/ase-grad-admissions/"
FAQ = "https://ae.utexas.edu/academics/graduate/graduate-faqs/"
GRAD_APPLY = "https://gradschool.utexas.edu/admissions/apply"
INTERNATIONAL = "https://gradschool.utexas.edu/admissions/apply/international"
FUNDING = "https://ae.utexas.edu/academics/graduate/funding/"
COA = "https://onestop.utexas.edu/managing-costs/cost-tuition-rates/cost-of-attendance/"
I20_COST = "https://global.utexas.edu/isss/immigration/f-1/financial-information"
INSURANCE = "https://global.utexas.edu/isss/advising-services/insurance/faqs"
ECGA_APPLICATION = "https://housing.utexas.edu/housing/east-campus-graduate-apartments/ecga-application"
ECGA_RATES = "https://housing.utexas.edu/housing/east-campus-graduate-apartments/ecga-rates"
UNIVERSITY_APARTMENTS = "https://housing.utexas.edu/housing/university-apartments"
UNIVERSITY_APARTMENT_RATES = "https://housing.utexas.edu/housing/university-apartments/university-apartments-rates"
RESEARCH = "https://ae.utexas.edu/research/"
RESEARCH_AREAS = "https://ae.utexas.edu/research/research-areas/"
SPACE = "https://www.ae.utexas.edu/research/orbital-mechanics"
CENTERS = "https://ae.utexas.edu/research/research-centers/"
FACILITIES = "https://ae.utexas.edu/about/facilities/"
RANKING = "https://cockrell.utexas.edu/about/facts-and-rankings/program-rankings/"
QS = "https://www.topuniversities.com/universities/university-texas-austin"

REDDIT_AVAILABILITY = "https://www.reddit.com/r/UTAustin/comments/1sk4v5q/east_graduate_student_apartments_availability/"
REDDIT_VALUE = "https://www.reddit.com/r/UTAustin/comments/1sa0ldg/are_the_east_campus_graduate_apartments_worth_it/"
REDDIT_CONDITIONS = "https://www.reddit.com/r/UTAustin/comments/1s7ty3x/repost_current_living_conditions_at_east_campus/"


def bi(en: str, tr: str) -> dict[str, str]:
    return {"en": en, "tr": tr}


def source(url: str, title: str, source_type: str, fields: list[str], en: str, tr: str, confidence: str = "high") -> dict:
    return {
        "url": url,
        "title": title,
        "source_type": source_type,
        "access_status": "ok",
        "last_checked": TODAY,
        "relevant_fields": fields,
        "confidence": confidence,
        "notes": bi(en, tr),
    }


def main() -> None:
    rows = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    row = next(item for item in rows if item.get("id") == "ut-austin-ase")

    row.update({
        "country": "United States",
        "university": "The University of Texas at Austin",
        "university_native_name": "The University of Texas at Austin",
        "city": "Austin",
        "program_name": "Master of Science in Engineering in Aerospace Engineering",
        "program_native_name": "Master of Science in Engineering in Aerospace Engineering",
        "program_degree": "MSE",
        "degree_level": "Master",
        "duration": bi("Typically 1.5–2 years", "Genellikle 1,5–2 yıl"),
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
        "tuition_usd_per_year": None,
        "annual_fee_usd": None,
        "qs_ranking": 72,
        "qs_ranking_display": "#72",
        "qs_ranking_year": 2027,
    })

    row["prestige_profile"] = {
        "qs_world_rank": 72,
        "qs_edition": 2027,
        "qs_source_url": QS,
        "current_us_news_graduate_engineering_rank": 6,
        "current_us_news_aerospace_rank": 8,
        "ranking_edition": "2026/2027",
        "official_ranking_source_url": RANKING,
        "interpretation": bi("Rankings are reported as context and not used as proof of space-engineering depth.", "Sıralamalar bağlam olarak verilir; uzay mühendisliği derinliğinin kanıtı sayılmaz."),
    }

    row["eligibility_profile"] = {
        "eligible_for_non_eu": True,
        "required_previous_degree": bi("Normally a BS in aerospace engineering, engineering mechanics or a closely related engineering field. Science or mathematics graduates may be admitted with additional undergraduate deficiencies.", "Normalde havacılık-uzay mühendisliği, mühendislik mekaniği veya yakından ilgili mühendislik alanında lisans gerekir. Fen veya matematik mezunları ek lisans eksikleriyle kabul edilebilir."),
        "accepted_backgrounds": [bi("Aerospace engineering", "Havacılık ve uzay mühendisliği"), bi("Engineering mechanics", "Mühendislik mekaniği"), bi("Closely related engineering", "Yakından ilgili mühendislik"), bi("Science or mathematics with required deficiency coursework", "Gerekli eksik derslerle fen veya matematik")],
        "minimum_gpa": 3.0,
        "minimum_gpa_scope": "junior_and_senior_level_and_completed_graduate_work",
        "admission_mode": "selective_holistic",
        "admission_risk": "high",
        "required_documents": [bi("Graduate application", "Lisansüstü başvuru"), bi("Copies of official transcripts", "Resmî transkript kopyaları"), bi("Statement of purpose", "Amaç mektubu"), bi("Resume or CV", "Özgeçmiş"), bi("At least three letters of recommendation", "En az üç referans mektubu"), bi("Official GRE General score", "Resmî GRE General puanı"), bi("Official English-proficiency score unless exempt", "Muafiyet yoksa resmî İngilizce yeterlilik puanı")],
        "motivation_letter_required": True,
        "cv_required": True,
        "recommendation_required": True,
        "recommendation_letter_count": 3,
        "recommendation_letter_count_minimum": True,
        "portfolio_required": False,
        "interview_required": False,
        "interview_policy": "not_listed_in_checked_official_requirements",
        "application_fee_usd": 90,
        "application_fee_waiver": bi("Graduate application fee waivers are not available to international citizens.", "Lisansüstü başvuru ücreti muafiyeti uluslararası vatandaşlara sunulmaz."),
        "gre": {
            "policy": "required",
            "test_type": "GRE General",
            "minimum_scores": {},
            "recommended_scores": {},
            "previously_admitted_averages": {"verbal": 160, "quantitative": 168, "analytical_writing": 4.5},
            "averages_not_minimums": True,
            "waiver_rules": [],
            "score_delivery_time": "approximately 10–15 business days",
            "source_ids": [ADMISSION, FAQ],
        },
        "background_deficiencies": {
            "aerothermodynamics_and_fluid_mechanics": ["ASE 320", "ASE 376K"],
            "controls_autonomy_robotics": ["ASE 330M", "ASE 370C"],
            "space_systems_and_astrodynamics": ["ASE 330M", "ASE 366K"],
            "solids_structures_materials": ["EM 319", "COE 321K", "ASE 365"],
            "minimum_grade_after_admission": "B",
        },
        "notes_for_turkish_students": bi("Turkey is not on UT Austin's English-test exemption list. A Turkish applicant normally follows the international process and submits official English-proficiency evidence.", "Türkiye UT Austin'ın İngilizce sınav muafiyet listesinde değildir. Türkiye'den bir aday normalde uluslararası süreci izler ve resmî İngilizce yeterlilik kanıtı sunar."),
        "verification_notes": bi("Meeting the 3.0 minimum does not guarantee admission. Prior-admit GRE averages are descriptive, not cutoffs.", "3,0 tabanını karşılamak kabul garantisi değildir. Önceki kabul GRE ortalamaları tanımlayıcıdır, eşik değildir."),
    }

    row["language_profile"] = {
        "teaching_language": ["Unknown"],
        "teaching_languages": ["Unknown"],
        "english_required": True,
        "accepted_english_tests": [
            {"test": "TOEFL iBT", "minimum_score": 79, "new_6_point_scale_minimum": 4},
            {"test": "IELTS Academic", "minimum_score": 6.5},
            {"test": "Duolingo English Test", "minimum_score": 115, "programme_cycle_note": "ASE FAQ says accepted beginning summer/fall 2027"},
        ],
        "english_exemptions": [bi("Citizenship in a qualifying country", "Uygun bir ülkenin vatandaşlığı"), bi("Bachelor's degree from a US institution or qualifying-country institution", "ABD'deki veya uygun ülkedeki bir kurumdan lisans derecesi")],
        "language_risk": "medium",
        "verification_notes": bi("The current Graduate School publishes TOEFL/IELTS/DET minimums. The ASE admissions page contains older contradictory wording about no English-test minimum, so the current central rule controls. No official page checked explicitly states the MSE teaching language; it remains Unknown.", "Güncel Graduate School TOEFL/IELTS/DET tabanlarını yayımlar. ASE kabul sayfasında İngilizce sınav tabanı olmadığına dair eski ve çelişkili ifade bulunur; bu nedenle güncel merkezî kural esas alınır. Kontrol edilen hiçbir resmî sayfa MSE öğretim dilini açıkça belirtmez; Unknown kalır."),
    }

    row["cost_profile"] = {
        "academic_year": "2026/2027",
        "currency": "USD",
        "tuition_usd_per_year": None,
        "tuition_usd_per_year_min": 17312,
        "tuition_usd_per_year_max": 19340,
        "tuition_basis": "official nonresident full-time graduate range for Fall and Spring, based on 9-hour enrollment",
        "housing_and_food_usd_per_year_min": 17052,
        "housing_and_food_usd_per_year_max": 17423,
        "transportation_usd_per_year": 1840,
        "books_and_supplies_usd_per_year": 776,
        "personal_miscellaneous_usd_per_year": 4900,
        "total_cost_of_attendance_usd_per_year": None,
        "total_cost_of_attendance_usd_per_year_min": 41880,
        "total_cost_of_attendance_usd_per_year_max": 44279,
        "international_i20_tuition_and_fees_usd": 23487,
        "international_i20_living_expenses_usd": 22000,
        "international_i20_total_usd": 45487,
        "application_fee_usd": 90,
        "health_insurance_required_for_f_or_j_students": True,
        "health_insurance_waiver_possible": True,
        "health_insurance_premium_usd": None,
        "health_insurance_premium_status": "needs_verification",
        "complete_program_cost_usd": None,
        "tuition_items": [
            {"item": bi("Nonresident graduate tuition range", "Eyalet dışı lisansüstü öğrenim ücreti aralığı"), "amount_usd_min": 17312, "amount_usd_max": 19340, "period": "fall_and_spring"},
            {"item": bi("International I-20 tuition and fees estimate", "Uluslararası I-20 öğrenim ve ücret tahmini"), "amount_usd": 23487, "period": "two_semesters"},
        ],
        "verification_notes": bi("Texas One Stop publishes a financial-aid COA range, while Texas Global publishes a higher fixed immigration-document estimate. They serve different purposes and are not merged. Neither is a guaranteed bill; actual Engineering tuition depends on enrollment. The 2026/27 international insurance premium was not verified separately.", "Texas One Stop mali yardım için bir COA aralığı, Texas Global ise göçmenlik belgesi için daha yüksek sabit tahmin yayımlar. Farklı amaçlara hizmet ederler ve birleştirilmezler. Hiçbiri garantili fatura değildir; gerçek Engineering ücreti ders yüküne bağlıdır. 2026/27 uluslararası sigorta primi ayrıca doğrulanamamıştır."),
    }

    row["scholarship_profile"] = {
        "available_types": ["graduate_research_assistantship", "teaching_assistantship", "fellowship"],
        "non_eu_eligible": "position_or_award_specific",
        "application_mode": "mixed",
        "application_mode_detail": "automatic_general_financial_aid_consideration_but_separate_post_admission_ta_process",
        "automatic_consideration": True,
        "separate_application_required": True,
        "admission_funding_guaranteed": False,
        "masters_fully_funded": False,
        "minimum_ta_gra_stipend_usd_per_year_2026_27": 34000,
        "opportunities": [
            {"name": "20-hour GRA or TA", "type": "competitive_employment", "amount": 34000, "currency": "USD", "amount_status": "department_minimum_annual_stipend_2026_27", "automatic_consideration": False, "separate_application_required": True, "deadline": bi("Fall TA applications for admitted students: April–May; Spring: September–October", "Kabul edilenler için Güz TA başvuruları Nisan–Mayıs; Bahar Eylül–Ekim"), "benefits": ["Texas resident tuition rate", "Tuition Reduction Benefit", "medical insurance"], "url": FAQ},
            {"name": "Faculty-funded GRA or fellowship", "type": "competitive_funding", "amount": None, "currency": "USD", "automatic_consideration": True, "separate_application_required": False, "deadline": None, "eligibility_summary": bi("All graduate applications are considered, but faculty recruiting and external-grant availability change by cycle.", "Tüm lisansüstü başvurular değerlendirilir; öğretim üyesi alımı ve dış hibe uygunluğu döneme göre değişir."), "url": FUNDING},
        ],
        "funding_notes": bi("All applications are considered for financial aid, but master's students are not fully funded. PhD students are the primary GRA group; MS students may apply for TA roles after admission. Appointments are not guaranteed from semester to semester.", "Tüm başvurular mali yardım için değerlendirilir ancak yüksek lisans öğrencileri tam fonlu değildir. GRA'nın ana grubu doktora öğrencileridir; MS öğrencileri kabulden sonra TA rollerine başvurabilir. Atamalar dönemden döneme garanti edilmez."),
        "verification_notes": bi("Automatic financial-aid consideration must not be read as an automatic award. The $34,000 figure applies only to students who secure a TA/GRA appointment.", "Otomatik mali yardım değerlendirmesi otomatik ödül sayılmamalıdır. 34.000 $ yalnızca TA/GRA görevi alan öğrencilere uygulanır."),
    }

    row["living_profile"] = {
        "city_cost_level": "high",
        "housing_difficulty": "high",
        "living_risk": "high",
        "housing_access": "not_guaranteed",
        "student_housing_available": True,
        "housing_application_separate": True,
        "housing_allocation_mode": "rolling_availability_with_priority_for_programmes_expected_to_offer_competitive_funding",
        "housing_application_opening": "August 1",
        "housing_application_fee_usd": 100,
        "housing_contract_prepaid_amount_usd": 500,
        "monthly_housing_rent_usd_per_month_min": 619.20,
        "monthly_housing_rent_usd_per_month_max": 1581,
        "average_room_rent_usd": None,
        "average_room_rent_scope_label": bi("Official UT graduate-eligible apartment examples; not a private-market average", "Resmî UT lisansüstü-uygun daire örnekleri; özel piyasa ortalaması değil"),
        "housing_options": [
            {"provider": "East Campus Graduate Apartments", "institution_owned": True, "guaranteed": False, "contract_months": 12, "utilities_included": True},
            {"provider": "Colorado and Gateway University Apartments", "institution_owned": True, "guaranteed": False, "utilities_included": True},
        ],
        "official_rent_items": [
            {"item": bi("ECGA two-bedroom, per person", "ECGA iki yatak odalı, kişi başı"), "amount_usd_min": 1199, "amount_usd_max": 1199, "period": "month", "academic_year": "2026/2027"},
            {"item": bi("ECGA studio or one-bedroom", "ECGA stüdyo veya tek yatak odalı"), "amount_usd_min": 1301, "amount_usd_max": 1581, "period": "month", "academic_year": "2026/2027"},
            {"item": bi("Colorado/Gateway shared two-bedroom share", "Colorado/Gateway paylaşımlı iki yatak odalı oda payı"), "amount_usd_min": 619.20, "amount_usd_max": 756.80, "period": "month", "academic_year": "2026/2027"},
            {"item": bi("Colorado/Gateway one-bedroom", "Colorado/Gateway tek yatak odalı"), "amount_usd_min": 1200, "amount_usd_max": 1338, "period": "month", "academic_year": "2026/2027"},
        ],
        "official_living_cost_items": [
            {"item": bi("Housing and food COA allowance", "Konut ve yemek COA payı"), "amount_usd_min": 17052, "amount_usd_max": 17423, "period": "academic_year", "academic_year": "2026/2027"},
            {"item": bi("International immigration living estimate", "Uluslararası göçmenlik yaşam tahmini"), "amount_usd": 22000, "period": "12_months", "academic_year": "2026/2027"},
        ],
        "housing_notes": bi("ECGA is exclusively for graduate students, but contracts are rolling and availability-dependent. Priority favors programmes expected to provide competitive funding, so an MS applicant should not assume priority or a contract. Earlier application improves chances.", "ECGA yalnızca lisansüstü öğrenciler içindir ancak sözleşmeler sürekli ve boşluğa bağlıdır. Öncelik rekabetçi finansman sağlaması beklenen programlara verildiğinden MS adayı öncelik veya sözleşme varsaymamalıdır. Erken başvuru şansı artırır."),
        "verification_notes": bi("The displayed range combines current university-owned options, not a city average. Private-market rent was not invented.", "Gösterilen aralık güncel üniversiteye ait seçenekleri birleştirir; şehir ortalaması değildir. Özel piyasa kirası uydurulmamıştır."),
    }

    row["curriculum_profile"] = {
        "credit_system": "US semester credit hours",
        "credit_hours_total": 30,
        "course_count_fixed": False,
        "course_count_summary": bi("Three 30-credit routes: thesis (24 coursework + 6 research), report (27 coursework + 3 report research), or coursework-only (30 coursework).", "Üç adet 30 kredilik yol: tez (24 ders + 6 araştırma), rapor (27 ders + 3 rapor araştırması) veya yalnız ders (30 ders)."),
        "tracks": [bi("Aerothermodynamics and Fluid Mechanics", "Aerotermodinamik ve Akışkanlar Mekaniği"), bi("Estimation, Decision-Making, Control, Autonomy and Robotics", "Kestirim, Karar Verme, Kontrol, Otonomi ve Robotik"), bi("Solids, Structures and Materials", "Katılar, Yapılar ve Malzemeler"), bi("Space Systems and Astrodynamics", "Uzay Sistemleri ve Astrodinamik")],
        "specializations": [bi("Space Tech Graduate Specialization", "Space Tech Lisansüstü Uzmanlaşması")],
        "pathway_details": {
            "thesis": {"total_credit_hours": 30, "coursework_hours": 24, "research_hours": 6, "research_courses": ["ASE/EM 698A", "ASE/EM 698B"], "two_consecutive_semesters_required": True},
            "report": {"total_credit_hours": 30, "coursework_hours": 27, "research_hours": 3, "research_course": "ASE/EM 398R"},
            "coursework": {"total_credit_hours": 30, "coursework_hours": 30, "organized_research_for_credit": False},
        },
        "requirement_components": [
            {"name": bi("Thesis route", "Tez yolu"), "credit_hours": bi("24 coursework + 6 research", "24 ders + 6 araştırma")},
            {"name": bi("Report route", "Rapor yolu"), "credit_hours": bi("27 coursework + 3 report research", "27 ders + 3 rapor araştırması")},
            {"name": bi("Coursework route", "Yalnız ders yolu"), "credit_hours": 30},
        ],
        "upper_division_undergraduate_credit_hours_max": 6,
        "thesis_required": False,
        "thesis_route_available": True,
        "report_route_available": True,
        "internship_required": False,
        "internship_notes": bi("No compulsory internship is listed in the official MSE degree routes.", "Resmî MSE derece yollarında zorunlu staj listelenmez."),
        "verification_notes": bi("Research access is built into the thesis/report routes only after a faculty advisor agrees. Coursework students do not receive organized research credit as part of the degree.", "Araştırma erişimi yalnızca bir öğretim üyesi danışmanlığı kabul ettikten sonra tez/rapor yollarına dâhildir. Yalnız ders öğrencileri derece içinde düzenli araştırma kredisi almaz."),
    }

    row["category_profile"] = {
        "primary_categories": ["Aerospace Engineering", "Space Systems & Astronautics"],
        "secondary_categories": ["Aerodynamics & Fluid Mechanics", "Flight Mechanics & Control", "Structures & Materials", "Systems & Design", "Scientific AI & Computational Engineering"],
        "subcategories": ["hypersonics", "aerothermodynamics", "gnc", "autonomy", "robotics", "astrodynamics", "mission_design", "space_domain_awareness", "orbit_determination", "remote_sensing", "space_geodesy", "digital_twin", "structures", "materials"],
        "normalized_tags": ["hypersonics", "aerothermodynamics", "gnc", "autonomy", "robotics", "astrodynamics", "mission_design", "space_domain_awareness", "orbit_determination", "remote_sensing", "space_geodesy", "digital_twin", "structures", "materials"],
        "category_scores": {},
        "category_evidence": [bi("Official areas and research pages directly document aerospace, spacecraft, autonomy, computational and structures depth.", "Resmî alan ve araştırma sayfaları havacılık-uzay, uzay aracı, otonomi, hesaplama ve yapı derinliğini doğrudan belgeler.")],
    }

    row["research_profile"] = {
        "department_research_areas": [bi("Aerothermodynamics and fluid mechanics", "Aerotermodinamik ve akışkanlar mekaniği"), bi("Computational engineering", "Hesaplamalı mühendislik"), bi("Estimation, decision-making and control", "Kestirim, karar verme ve kontrol"), bi("Space systems and astrodynamics", "Uzay sistemleri ve astrodinamik"), bi("Solids, structures and materials", "Katılar, yapılar ve malzemeler")],
        "labs": [
            {"name": "Texas Spacecraft Laboratory", "officially_listed": True, "student_access": bi("Research placement dependent", "Araştırma yerleştirmesine bağlı")},
            {"name": "Space Object Visualization Lab", "officially_listed": True, "student_access": bi("Research placement dependent", "Araştırma yerleştirmesine bağlı")},
            {"name": "Boeing Aircraft Systems and Integration Lab", "officially_listed": True, "student_access": bi("Research placement dependent", "Araştırma yerleştirmesine bağlı")},
            {"name": "Autonomous UAV and Human-Centered Robotics Labs", "officially_listed": True, "student_access": bi("Research placement dependent", "Araştırma yerleştirmesine bağlı")},
        ],
        "research_centers": ["Center for Space Research", "Center for Aeromechanics Research", "Center for Autonomy", "Oden Institute for Computational Engineering and Sciences", "Applied Research Laboratories"],
        "facilities": [bi("86,000-square-foot renovated Aerospace Engineering Building with wind tunnel, flight simulator and space/UAV/robotics labs", "Rüzgâr tüneli, uçuş simülatörü ve uzay/İHA/robotik laboratuvarları bulunan yenilenmiş 86.000 ft² Aerospace Engineering Building")],
        "research_strength_summary": bi("UT Austin is particularly deep in astrodynamics, orbit determination, space-domain awareness, GNSS, remote sensing and computational prediction. MS research access is possible through thesis/report supervision or a funded appointment, not automatic with admission.", "UT Austin özellikle astrodinamik, yörünge belirleme, uzay alanı farkındalığı, GNSS, uzaktan algılama ve hesaplamalı tahminde derindir. MS araştırma erişimi tez/rapor danışmanlığı veya fonlu görevle mümkündür; kabul ile otomatik değildir."),
        "research_strength_score": None,
        "research_sources": [RESEARCH, RESEARCH_AREAS, SPACE, CENTERS, FACILITIES],
    }

    row["industry_ecosystem_profile"] = {
        "nearby_companies": [],
        "confirmed_partners": [],
        "officially_documented_research_customers": ["NASA", "US Department of Defense", "other government agencies", "commercial space industry"],
        "space_agencies_or_public_bodies": ["NASA", "US Department of Defense"],
        "research_institutes": ["Center for Space Research", "Applied Research Laboratories", "Oden Institute"],
        "internship_possibility": "possible_but_not_program_requirement",
        "thesis_with_industry_possibility": "not_verified",
        "career_relevance": "high_but_not_scored",
        "ecosystem_strength_score": None,
        "international_student_constraints": [bi("Eligibility for defence-sponsored or export-controlled projects must be verified project by project; no universal access claim is made.", "Savunma sponsorlu veya ihracat kontrollü projelere uygunluk proje bazında doğrulanmalıdır; evrensel erişim iddia edilmez.")],
        "ecosystem_notes": bi("Legacy claims about direct proximity or partnerships with NASA JSC, SpaceX and Firefly were removed because programme-specific current partnership evidence was not established. Only officially documented research-customer categories are retained.", "NASA JSC, SpaceX ve Firefly ile doğrudan yakınlık veya ortaklık hakkındaki eski iddialar, güncel programa özgü ortaklık kanıtı kurulamadığı için kaldırıldı. Yalnızca resmî olarak belgelenen araştırma-müşteri kategorileri korundu."),
    }

    row["application_timeline_profile"] = {
        "academic_year": "recurring deadlines on current official pages",
        "intake_terms": ["Fall", "Spring", "Summer"],
        "application_rounds": [
            {"round": bi("Fall admission", "Güz kabulü"), "opens": None, "deadline": "December 1", "decision": bi("Faculty-offer notifications February–March; all other Fall decisions before April 15", "Öğretim üyesi teklifleri Şubat–Mart; diğer tüm Güz kararları 15 Nisan'dan önce")},
            {"round": bi("Spring admission", "Bahar kabulü"), "opens": None, "deadline": "October 1", "decision": bi("Faculty-offer notifications November–December; other decisions before mid-December winter break", "Öğretim üyesi teklifleri Kasım–Aralık; diğer kararlar Aralık ortası kış tatilinden önce")},
            {"round": bi("Summer admission", "Yaz kabulü"), "opens": None, "deadline": "December 1", "decision": None},
        ],
        "non_eu_deadline": bi("Same programme deadlines; fee and all materials should be completed early because MyStatus access may take up to 48 hours and GRE delivery about 10–15 business days.", "Aynı program tarihleri geçerlidir; MyStatus erişimi 48 saate, GRE iletimi yaklaşık 10–15 iş gününe uzayabildiğinden ücret ve tüm belgeler erken tamamlanmalıdır."),
        "scholarship_deadline": bi("No separate admission-funding deadline; all applications are considered. Admitted students apply separately for TA roles in April–May for Fall or September–October for Spring.", "Ayrı kabul finansmanı tarihi yoktur; tüm başvurular değerlendirilir. Kabul edilenler Güz TA için Nisan–Mayıs, Bahar TA için Eylül–Ekim döneminde ayrıca başvurur."),
        "pre_enrolment_required": False,
        "visa_sensitive_deadline": bi("After admission, F-1/J-1 students submit proof of funds for the immigration estimate and complete Texas Global document processing; no fabricated visa deadline is inserted.", "Kabulden sonra F-1/J-1 öğrencileri göçmenlik tahmini için mali yeterlilik sunar ve Texas Global belge işlemlerini tamamlar; uydurma vize tarihi eklenmez."),
        "application_result_timing": bi("Fall results by April 15; Spring results before mid-December, with some faculty offers earlier.", "Güz sonuçları 15 Nisan'a kadar, Bahar sonuçları Aralık ortasından önce; bazı öğretim üyesi teklifleri daha erken."),
        "timeline_risk": "medium",
        "deadline_notes": bi("The FAQ says late materials or changes are not accepted, while the admissions page says post-deadline applications may be considered if space remains. Treat the official deadline as firm and do not plan around space-available review.", "SSS geç belge veya değişiklik kabul edilmediğini, kabul sayfası ise tarih sonrası başvuruların yer kalırsa değerlendirilebileceğini söyler. Resmî tarihi kesin kabul edin ve yer kalırsa incelemeye güvenmeyin."),
    }

    row["student_sentiment_profile"] = {
        "student_satisfaction_score": None,
        "teaching_quality_sentiment": "unknown",
        "workload_sentiment": "unknown",
        "workload_balance_sentiment": "unknown",
        "administration_sentiment": "unknown",
        "housing_sentiment": "mixed_to_negative",
        "city_life_sentiment": "unknown",
        "international_student_sentiment": "unknown",
        "career_support_sentiment": "unknown",
        "student_sentiment_summary": bi("A small 2026 housing-only sample reports concern about ECGA price, management, noise and availability, while some residents describe it as workable and recent applicants report receiving contracts. These perceptions do not prove programme quality or citywide housing prices.", "Küçük 2026 konut örneklemi ECGA fiyatı, yönetimi, gürültüsü ve uygunluğu hakkında kaygı bildirirken bazı sakinler seçeneği idare edilebilir buluyor ve yakın dönem başvuranlar sözleşme aldığını söylüyor. Bu algılar program kalitesini veya şehir geneli kirayı kanıtlamaz."),
        "student_sentiment_sources": [
            {"url": REDDIT_AVAILABILITY, "platform": "Reddit r/UTAustin", "topic": "ECGA contract availability", "date": "2026-04", "approx_observations": 2, "access_status": "ok", "last_checked": TODAY, "confidence": "low"},
            {"url": REDDIT_VALUE, "platform": "Reddit r/UTAustin", "topic": "ECGA value and management", "date": "2026-04", "approx_observations": 4, "access_status": "ok", "last_checked": TODAY, "confidence": "low"},
            {"url": REDDIT_CONDITIONS, "platform": "Reddit r/UTAustin", "topic": "ECGA noise and administration", "date": "2026-03", "approx_observations": 3, "access_status": "ok", "last_checked": TODAY, "confidence": "low"},
        ],
        "approximate_sample_size": 9,
        "date_range": "2026",
        "sentiment_confidence": "low",
        "verification_notes": bi("No overall satisfaction score is computed and no unrelated undergraduate or other-department claims are generalized to ASE MSE.", "Genel memnuniyet puanı hesaplanmaz; ilgisiz lisans veya diğer bölüm iddiaları ASE MSE'ye genellenmez."),
    }

    sources = [
        source(PROGRAM, "UT Austin ASE Graduate Program", "official_program_page", ["program", "program_status", "duration", "curriculum", "tracks"], "Current MSE routes, prerequisites, areas and Space Tech specialization.", "Güncel MSE yolları, ön koşullar, alanlar ve Space Tech uzmanlaşması."),
        source(ADMISSION, "UT Austin ASE Graduate Admissions", "official_admission_page", ["admission", "deadline", "gre", "required_documents", "language"], "Current deadlines, 3.0 GPA, required GRE and application materials.", "Güncel tarihler, 3,0 GPA, zorunlu GRE ve başvuru belgeleri."),
        source(FAQ, "UT Austin ASE Graduate FAQs", "official_admission_page", ["duration", "admission", "deadline", "gre", "language", "funding"], "Current duration, decision timing, GRE averages, funding mechanics and 2026/27 stipend.", "Güncel süre, karar zamanı, GRE ortalamaları, finansman mekanikleri ve 2026/27 maaşı."),
        source(GRAD_APPLY, "UT Austin Graduate How to Apply", "official_admission_page", ["application_fee", "admission", "non_eu_eligibility"], "Current $90 international fee and no international fee waiver.", "Güncel 90 $ uluslararası ücret ve uluslararası ücret muafiyeti olmaması."),
        source(INTERNATIONAL, "UT Austin International Graduate Applicants", "official_admission_page", ["non_eu_eligibility", "language", "admission"], "Current international route, test minimums and exemptions.", "Güncel uluslararası yol, sınav tabanları ve muafiyetler."),
        source(FUNDING, "UT Austin ASE Graduate Funding", "official_scholarship_page", ["funding", "scholarship", "non_eu_eligibility"], "Automatic application consideration, non-guaranteed GRA/TA and employee benefits.", "Otomatik başvuru değerlendirmesi, garantisiz GRA/TA ve çalışan hakları."),
        source(COA, "UT Austin Cost of Attendance 2026/27", "official_tuition_page", ["tuition", "living", "cost"], "Current nonresident full-time graduate tuition and COA ranges.", "Güncel eyalet dışı tam zamanlı lisansüstü ücret ve COA aralıkları."),
        source(I20_COST, "UT Austin F-1/J-1 Financial Information 2026/27", "official_visa_or_government_page", ["visa", "tuition", "living", "cost"], "Current standard graduate proof-of-funds estimate.", "Güncel standart lisansüstü mali yeterlilik tahmini."),
        source(INSURANCE, "UT Austin International Insurance FAQs", "official_cost_of_living_page", ["insurance", "cost", "non_eu_eligibility"], "Current automatic F/J insurance enrollment and waiver rule; current premium remains unverified.", "Güncel otomatik F/J sigorta kaydı ve muafiyet kuralı; güncel prim doğrulanmamıştır."),
        source(ECGA_APPLICATION, "UT Austin ECGA Application Process", "official_housing_page", ["housing", "application", "eligibility"], "Graduate-only eligibility, August 1 opening, rolling offers, fees and priority policy.", "Yalnız lisansüstü uygunluğu, 1 Ağustos açılışı, sürekli teklifler, ücretler ve öncelik politikası."),
        source(ECGA_RATES, "UT Austin ECGA Rates 2026/27", "official_housing_page", ["housing", "living"], "Current graduate apartment monthly rates and included utilities.", "Güncel lisansüstü daire aylık ücretleri ve dâhil faturalar."),
        source(UNIVERSITY_APARTMENTS, "UT Austin University Apartments", "official_housing_page", ["housing", "eligibility"], "Additional graduate-eligible university-owned housing.", "Ek lisansüstü-uygun üniversite konutu."),
        source(UNIVERSITY_APARTMENT_RATES, "UT Austin University Apartment Rates 2026/27", "official_housing_page", ["housing", "living"], "Current Colorado, Gateway and family-housing rates.", "Güncel Colorado, Gateway ve aile konutu ücretleri."),
        source(RESEARCH, "UT Austin ASE Research", "official_department_page", ["research", "department"], "Current department research scale and projects.", "Güncel bölüm araştırma ölçeği ve projeleri."),
        source(RESEARCH_AREAS, "UT Austin ASE Research Areas", "official_department_page", ["research", "curriculum", "tracks"], "Current five-area research framework.", "Güncel beş alanlı araştırma çerçevesi."),
        source(SPACE, "UT Austin Space Systems and Astrodynamics", "official_department_page", ["research", "space_fit", "industry_ecosystem"], "Current mission design, SDA, orbit determination, GNSS and remote-sensing depth.", "Güncel görev tasarımı, SDA, yörünge belirleme, GNSS ve uzaktan algılama derinliği."),
        source(CENTERS, "UT Austin ASE Affiliated Research Centers", "official_department_page", ["research", "labs", "industry_ecosystem"], "Current named centers including CSR, CAR, Center for Autonomy, Oden and ARL.", "CSR, CAR, Center for Autonomy, Oden ve ARL dâhil güncel merkezler."),
        source(FACILITIES, "UT Austin ASE Facilities", "official_lab_page", ["research", "labs"], "Current spacecraft, visualization, UAV, robotics, wind-tunnel and simulator facilities.", "Güncel uzay aracı, görselleştirme, İHA, robotik, rüzgâr tüneli ve simülatör tesisleri."),
        source(RANKING, "Cockrell Graduate Program Rankings 2026/27", "official_ranking_page", ["prestige"], "Current official #6 Engineering and #8 aerospace reporting; separate from fit.", "Güncel resmî #6 Engineering ve #8 aerospace bildirimi; uyumdan ayrı."),
        source(QS, "QS World University Rankings 2027 — UT Austin", "reliable_third_party_ranking", ["prestige"], "Current university-wide rank; not technical-fit evidence.", "Güncel üniversite geneli sıra; teknik uyum kanıtı değil.", confidence="medium"),
        source(REDDIT_AVAILABILITY, "Reddit — ECGA availability", "student_forum", ["student_sentiment"], "Small housing availability anecdote.", "Küçük konut uygunluğu anekdotu.", confidence="low"),
        source(REDDIT_VALUE, "Reddit — ECGA value and management", "student_forum", ["student_sentiment"], "Small housing quality and management sample.", "Küçük konut kalitesi ve yönetim örneklemi.", confidence="low"),
        source(REDDIT_CONDITIONS, "Reddit — ECGA current conditions", "student_forum", ["student_sentiment"], "Small housing noise and administration sample.", "Küçük konut gürültüsü ve idare örneklemi.", confidence="low"),
    ]

    row["source_profile"] = {
        "primary_url": PROGRAM,
        "secondary_urls": [item["url"] for item in sources[1:]],
        "last_verified": TODAY,
        "field_confidence": {"program_basic_info": "high", "program": "high", "language": "unknown", "admission": "high", "non_eu_eligibility": "high", "tuition": "high", "scholarship": "high", "deadline": "high", "curriculum": "high", "research": "high", "industry_ecosystem": "medium", "housing": "high", "living": "high", "insurance_cost": "unknown", "sentiment": "low", "prestige": "high"},
        "source_reliability": "high",
        "verification_status": "partially_verified",
        "needs_verification": True,
        "verification_notes": bi("Every critical decision field except explicit teaching language is supported by current official sources. Insurance obligation is verified but the 2026/27 premium, private-market rent and exact full-program cost are deliberately not invented.", "Açık öğretim dili dışındaki tüm kritik karar alanları güncel resmî kaynaklarla desteklenir. Sigorta zorunluluğu doğrulanmıştır ancak 2026/27 primi, özel piyasa kirası ve kesin tam program maliyeti bilerek uydurulmamıştır."),
        "source_log": sources,
    }

    row["decision_summary"] = {
        "best_for": [bi("Students targeting astrodynamics, orbit determination, space-domain awareness, GNSS, remote sensing, autonomy or computational engineering.", "Astrodinamik, yörünge belirleme, uzay alanı farkındalığı, GNSS, uzaktan algılama, otonomi veya hesaplamalı mühendisliği hedefleyen öğrenciler."), bi("Applicants who want thesis, report and coursework-only pathways plus an optional Space Tech entrepreneurship specialization.", "Tez, rapor ve yalnız ders yollarıyla isteğe bağlı Space Tech girişimcilik uzmanlaşması isteyen adaylar.")],
        "not_ideal_for": [bi("Applicants who require guaranteed MS funding or automatic research placement.", "Garantili MS finansmanı veya otomatik araştırma yerleştirmesi gereken adaylar."), bi("Applicants who cannot tolerate high Austin housing costs or an availability-dependent housing process.", "Yüksek Austin konut maliyetini veya boşluğa bağlı konut sürecini karşılayamayan adaylar.")],
        "main_strengths": [bi("Three clearly documented 30-credit degree routes.", "Açıkça belgelenmiş üç adet 30 kredilik derece yolu."), bi("Exceptional official research depth in astrodynamics, SDA, GNSS and remote sensing.", "Astrodinamik, SDA, GNSS ve uzaktan algılamada olağanüstü resmî araştırma derinliği."), bi("Named facilities and centers include the Texas Spacecraft Laboratory and Center for Space Research.", "Adlandırılmış tesis ve merkezler Texas Spacecraft Laboratory ile Center for Space Research'ü içerir."), bi("Graduate-only university housing exists with published current rates.", "Yalnız lisansüstüne özel üniversite konutu ve yayımlanmış güncel ücretler vardır.")],
        "main_risks": [bi("MS students are not fully funded; TA/GRA awards are competitive and not guaranteed each semester.", "MS öğrencileri tam fonlu değildir; TA/GRA ödülleri rekabetçidir ve her dönem garanti edilmez."), bi("The official nonresident COA is $41,880–$44,279, while the immigration proof-of-funds estimate is $45,487.", "Resmî eyalet dışı COA 41.880–44.279 $, göçmenlik mali yeterlilik tahmini 45.487 $'dır."), bi("Graduate housing is not guaranteed, and ECGA priority favors programmes expected to provide competitive funding.", "Lisansüstü konut garanti değildir; ECGA önceliği rekabetçi finansman sunması beklenen programları destekler."), bi("GRE is required and prior-admit averages are high.", "GRE zorunludur ve önceki kabul ortalamaları yüksektir."), bi("Official pages checked do not explicitly state teaching language.", "Kontrol edilen resmî sayfalar öğretim dilini açıkça belirtmez.")],
        "decision_summary": bi("A premier US choice for astrodynamics, navigation, space-domain awareness and computational aerospace, with genuine thesis/report flexibility. International MS applicants should plan for self-funding, apply for housing early and treat research or assistantship access as competitive rather than automatic.", "Astrodinamik, seyrüsefer, uzay alanı farkındalığı ve hesaplamalı havacılık-uzay için ABD'nin önde gelen seçeneklerinden biridir; gerçek tez/rapor esnekliği sunar. Uluslararası MS adayları öz finansman planlamalı, konuta erken başvurmalı ve araştırma/asistanlık erişimini otomatik değil rekabetçi görmelidir."),
        "pros": [],
        "cons": [],
        "verdict": bi("Elite technical fit; funding and Austin housing require conservative planning.", "Seçkin teknik uyum; finansman ve Austin konutu temkinli planlama gerektirir."),
    }

    row["scoring_inputs"] = {"academic_prestige": None, "research_output": None, "industry_links": None, "affordability": None, "admission_chance": None, "living_quality": None, "hard_flags": ["teaching_language_unverified", "gre_required", "masters_not_fully_funded", "assistantship_not_guaranteed", "housing_not_guaranteed", "high_housing_cost", "insurance_premium_unverified", "research_access_not_automatic"]}
    row["data_quality"] = {"status": "partial", "checked_official_source_count": 19, "verified_fields": ["program", "duration", "admission", "non_eu_eligibility", "tuition", "scholarship", "deadline", "curriculum", "research", "industry_ecosystem", "housing", "living", "insurance_requirement", "prestige"], "unverified_critical_fields": ["language"], "known_semantic_gaps": ["explicit_teaching_language", "2026_27_health_insurance_premium", "private_market_rent", "complete_program_cost"], "has_checked_source_log": True, "audited_at": TODAY}
    row["quality_control"] = {"checked_at": TODAY, "qc_status": "needs_revision", "remaining_verification_tasks": [bi("Find a current official source explicitly stating the MSE teaching language; do not infer it from English-test requirements.", "MSE öğretim dilini açıkça belirten güncel resmî kaynak bulun; İngilizce sınav şartlarından çıkarım yapmayın."), bi("Add the 2026/27 international UT SHIP premium only if an accessible official rate is published.", "2026/27 uluslararası UT SHIP primini yalnızca erişilebilir resmî fiyat yayımlanırsa ekleyin.")], "qc_notes": bi("All discoverable critical decision fields are source-backed. The record remains partial solely because teaching language is not explicit.", "Bulunabilen tüm kritik karar alanları kaynaklıdır. Kayıt yalnızca öğretim dili açık olmadığı için partial kalır."), "failed_canary_tests": ["teaching_language_not_explicitly_verified"]}

    DATA_PATH.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"id": row["id"], "status": row["data_quality"]["status"], "source_count": len(sources), "checked_official_source_count": row["data_quality"]["checked_official_source_count"], "unverified_critical_fields": row["data_quality"]["unverified_critical_fields"]}, indent=2))


if __name__ == "__main__":
    main()
