from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data_base" / "amerika.json"
TODAY = "2026-08-14"

CATALOG = "https://catalog.illinois.edu/graduate/engineering/aerospace-engineering-ms/"
ADMISSIONS = "https://aerospace.illinois.edu/admissions/graduate/admissions-requirements-and-process"
FAQ = "https://aerospace.illinois.edu/admissions/graduate/graduate-program-faqs"
DEADLINES = "https://aerospace.illinois.edu/admissions/graduate/dates-and-deadlines"
ENGLISH = "https://grad.illinois.edu/admissions/international-applicants"
LANGUAGE = "https://registrar.illinois.edu/"
TUITION = "https://registrar.illinois.edu/g-tuition-rates-2627/"
COST = "https://cost.illinois.edu/Home/Cost/I/G/Compare/12/120268/120268"
FUNDING = "https://aerospace.illinois.edu/admissions/graduate/appointments-faq"
HOUSING_COST = "https://housing.illinois.edu/cost"
HOUSING_OPTIONS = "https://housing.illinois.edu/living-communities/halls/gud"
RESEARCH = "https://aerospace.illinois.edu/research/research-areas"
ARL = "https://aerospace.illinois.edu/research/research-facilities/aerodynamics-research-lab"
ASTRODYNAMICS = "https://aerospace.illinois.edu/research/research-areas/astrodynamics"
PRESTIGE = "https://grainger.illinois.edu/about/facts-and-rankings"
QS = "https://www.topuniversities.com/universities/university-illinois-urbana-champaign"


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
    row = next(item for item in rows if item.get("id") == "uiuc-ae")

    row.update(
        {
            "country": "United States",
            "university": "University of Illinois Urbana-Champaign",
            "university_native_name": "University of Illinois Urbana-Champaign",
            "program_name": "Master of Science in Aerospace Engineering",
            "program_native_name": "Master of Science in Aerospace Engineering",
            "program_degree": "MS",
            "degree_level": "Master",
            "duration": bi("1 year for the non-thesis route; normally 2 years for the thesis route", "Tezsiz yol 1 yıl; tezli yol normalde 2 yıl"),
            "duration_years": None,
            "ects": None,
            "us_credit_hours": 32,
            "teaching_language": ["English"],
            "teaching_languages": ["English"],
            "program_url": CATALOG,
            "program_status": "active",
            "relevance_status": "strong",
            "tuition_eur_per_year": None,
            "annual_fee_eur": None,
            "tuition_usd_per_year": 40444,
            "annual_fee_usd": 5936,
            "qs_ranking": 74,
            "qs_ranking_display": "#74",
            "qs_ranking_year": 2027,
        }
    )

    row["prestige_profile"] = {
        "qs_world_rank": 74,
        "qs_edition": 2027,
        "qs_source_url": QS,
        "national_graduate_aerospace_rank": 7,
        "national_rank_publisher": "U.S. News & World Report",
        "national_rank_publication_date": "2026-04",
        "national_rank_source_url": PRESTIGE,
        "interpretation": bi(
            "Prestige is reported separately from technical fit: QS is university-wide, while Illinois reports a current US graduate aerospace specialty rank.",
            "Prestij teknik uyumdan ayrı raporlanır: QS üniversite geneline aittir; Illinois ise güncel ABD lisansüstü havacılık-uzay uzmanlık sırasını yayımlar.",
        ),
    }

    row["eligibility_profile"] = {
        "eligible_for_non_eu": True,
        "required_previous_degree": bi(
            "A BS in aerospace engineering or a closely related field such as mechanical or civil engineering from an accredited US institution or an approved institution abroad.",
            "Akredite bir ABD kurumundan veya onaylı bir yabancı yükseköğretim kurumundan havacılık-uzay mühendisliği ya da makine/inşaat gibi yakın bir alanda lisans derecesi.",
        ),
        "accepted_backgrounds": [
            bi("Aerospace engineering", "Havacılık-uzay mühendisliği"),
            bi("Closely related engineering, including mechanical or civil engineering", "Makine veya inşaat mühendisliği dâhil yakın mühendislik alanları"),
        ],
        "minimum_gpa": 3.0,
        "gpa_scale": 4.0,
        "gpa_scope": bi("Last two undergraduate years and any completed graduate work", "Lisansın son iki yılı ve tamamlanan lisansüstü çalışmalar"),
        "admission_mode": "selective",
        "admission_risk": "high",
        "required_documents": [
            bi("Online graduate application", "Çevrimiçi lisansüstü başvuru"),
            bi("Resume", "Özgeçmiş"),
            bi("Statement of purpose, approximately 1–2 single-spaced pages", "Yaklaşık 1–2 tek aralıklı sayfalık amaç mektubu"),
            bi("Scanned transcripts and degree certificates or diplomas", "Taranmış transkriptler ve derece belgeleri/diplomalar"),
            bi("Three online letters of reference", "Çevrimiçi üç referans mektubu"),
            bi("Official English-proficiency score where required", "Gerektiğinde resmî İngilizce yeterlilik puanı"),
            bi("Declaration of finances and evidence of funds after admission if no departmental funding is offered", "Bölüm finansmanı verilmezse kabulden sonra mali beyan ve fon kanıtı"),
        ],
        "motivation_letter_required": True,
        "cv_required": True,
        "recommendation_required": True,
        "recommendation_letter_count": 3,
        "portfolio_required": False,
        "interview_required": False,
        "interview_policy": "not_listed_in_official_requirements",
        "test_required": False,
        "test_policy": bi("No programme-specific entrance test is listed in the checked official requirements.", "Kontrol edilen resmî şartlarda programa özgü giriş sınavı listelenmemiştir."),
        "application_fee_usd": 90,
        "application_fee_waiver": bi(
            "AE lists no waiver except the university's McNair Scholar and eligible employee routes.",
            "AE, üniversitenin McNair Scholar ve uygun çalışan yolları dışında ücret muafiyeti listelemez.",
        ),
        "gre": {
            "policy": "optional_waived",
            "test_type": "GRE General",
            "minimum_scores": {},
            "recommended_scores": {},
            "validity_rule": "",
            "waiver_rules": [bi("The GRE requirement is waived; submitted scores are accepted and evaluated.", "GRE şartı kaldırılmıştır; gönderilen puanlar kabul edilir ve değerlendirilir.")],
            "source_ids": [ADMISSIONS, FAQ, CATALOG],
        },
        "notes_for_turkish_students": bi(
            "Applicants educated in Turkey are international applicants. AE asks for official English evidence where applicable; financial certification is requested after admission when departmental funding is not offered. Apply to the MS route if you do not already hold an MS.",
            "Türkiye'de eğitim almış adaylar uluslararası adaydır. AE gerektiğinde resmî İngilizce kanıtı ister; bölüm finansmanı verilmezse kabulden sonra mali yeterlilik belgesi talep edilir. Hâlihazırda MS dereceniz yoksa MS yoluna başvurun.",
        ),
        "verification_notes": bi(
            "The official AE page gives a 3.0/4.0 minimum but explicitly says a higher GPA does not guarantee admission.",
            "Resmî AE sayfası 3,0/4,0 asgari ortalama verir; daha yüksek ortalamanın kabul garantisi olmadığını açıkça belirtir.",
        ),
    }

    row["language_profile"] = {
        "teaching_language": ["English"],
        "teaching_languages": ["English"],
        "english_required": True,
        "english_level_required": bi(
            "AE publishes TOEFL iBT 103 on the former scale. Graduate College full-status minimums are TOEFL 5.0 for tests dated after 20 January 2026 (103 before 21 January 2026) or IELTS Academic 7.5; limited-status minimums are TOEFL 4.0/79 or IELTS 6.5.",
            "AE eski ölçekte TOEFL iBT 103 yayımlar. Graduate College tam statü asgarileri 20 Ocak 2026 sonrasında alınan TOEFL için 5,0 (21 Ocak 2026 öncesinde 103) veya IELTS Academic 7,5; sınırlı statü asgarileri TOEFL 4,0/79 ya da IELTS 6,5'tir.",
        ),
        "accepted_english_tests": [
            {"test": "TOEFL iBT", "full_status_min_after_2026_01_20": 5.0, "full_status_min_before_2026_01_21": 103, "limited_status_min_after_2026_01_20": 4.0, "limited_status_min_before_2026_01_21": 79},
            {"test": "IELTS Academic", "full_status_min": 7.5, "limited_status_min": 6.5},
        ],
        "duolingo_program_acceptance": "needs_verification",
        "english_exemptions": [
            bi("A qualifying recent post-secondary degree, two years of post-secondary study, or two years of professional work in the US or another Graduate College-approved English-primary country may qualify for exemption.", "ABD'de veya Graduate College tarafından onaylanan İngilizce ağırlıklı bir ülkede yakın tarihli uygun bir yükseköğretim derecesi, iki yıllık yükseköğretim ya da iki yıllık mesleki çalışma muafiyet sağlayabilir."),
        ],
        "score_validity_years": 2,
        "ta_spoken_english_requirement": bi(
            "For TA consideration, TOEFL speaking 5.0 after 20 January 2026 (24 before 21 January 2026) or IELTS speaking 8; Duolingo does not satisfy the TA spoken-English rule.",
            "TA değerlendirmesi için 20 Ocak 2026 sonrası TOEFL speaking 5,0 (21 Ocak 2026 öncesi 24) veya IELTS speaking 8 gerekir; Duolingo TA sözlü İngilizce şartını karşılamaz.",
        ),
        "language_risk": "medium",
        "verification_notes": bi(
            "The Registrar explicitly states that campus instruction is delivered in English except foreign-language courses. AE's page has not yet been rewritten for the new TOEFL scale, so the current Graduate College date-dependent table controls interpretation; applicants relying on an exemption or Duolingo should obtain AE confirmation.",
            "Registrar, yabancı dil dersleri dışında kampüs öğretiminin İngilizce verildiğini açıkça belirtir. AE sayfası yeni TOEFL ölçeğine henüz uyarlanmamıştır; bu nedenle güncel Graduate College tarih-bağımlı tablosu esas alınır. Muafiyete veya Duolingo'ya dayanacak adaylar AE'den teyit almalıdır.",
        ),
    }

    row["cost_profile"] = {
        "academic_year": "2026/2027",
        "currency": "USD",
        "tuition_usd_per_year": 40444,
        "tuition_usd_per_semester_full_time": 20222,
        "full_time_credit_range": "12+ credit hours per semester",
        "mandatory_fees_usd_per_year": 5936,
        "mandatory_fees_usd_per_semester": 2968,
        "food_and_housing_allowance_usd_per_year": 16512,
        "books_and_supplies_allowance_usd_per_year": 1200,
        "other_expenses_allowance_usd_per_year": 3090,
        "total_cost_of_attendance_usd_per_year": 67182,
        "tuition_basis": "2026/27 international graduate Grainger Engineering rate at 12+ credits per semester",
        "tuition_items": [
            {"item": bi("Grainger Engineering international graduate tuition", "Grainger Engineering uluslararası lisansüstü öğrenim ücreti"), "amount": 40444, "currency": "USD", "period": "academic_year"},
            {"item": bi("Estimated mandatory fees", "Tahmini zorunlu ücretler"), "amount": 5936, "currency": "USD", "period": "academic_year"},
        ],
        "verification_notes": bi(
            "The official calculator is an attendance-budget estimate for an international graduate taking 12 credits in Grainger Engineering. Housing, books and other allowances are not all billed by the university; actual charges depend on enrollment and choices.",
            "Resmî hesaplayıcı, Grainger Engineering'de 12 kredi alan uluslararası lisansüstü öğrenci için katılım bütçesi tahminidir. Konut, kitap ve diğer payların tümü üniversite tarafından faturalandırılmaz; gerçek tutar kayıt yüküne ve tercihlere bağlıdır.",
        ),
    }

    row["scholarship_profile"] = {
        "available_types": ["fellowship", "research_assistantship", "teaching_assistantship", "tuition_and_fee_waiver"],
        "non_eu_eligible": True,
        "application_mode": "automatic",
        "automatic_consideration": True,
        "separate_application_required": False,
        "deadline": bi("For full Fall thesis-MS funding consideration: December 1; Spring thesis-MS: October 1", "Güz tezli MS tam finansman değerlendirmesi: 1 Aralık; bahar tezli MS: 1 Ekim"),
        "opportunities": [
            {
                "name": "AE fellowships, research assistantships and teaching assistantships",
                "type": "departmental_competitive_funding",
                "amount": None,
                "currency": "USD",
                "automatic_consideration": True,
                "separate_application_required": False,
                "eligibility_summary": bi("Competitive support for thesis-path applicants; not guaranteed. The MS non-thesis path is excluded from departmental funding.", "Tezli yol adayları için rekabetçi destektir; garanti edilmez. Tezsiz MS yolu bölüm finansmanı dışındadır."),
                "deadline": bi("December 1 for Fall full consideration; October 1 for Spring thesis admission", "Güz tam değerlendirme için 1 Aralık; bahar tezli kabul için 1 Ekim"),
                "url": ADMISSIONS,
            },
            {
                "name": "25%–67% qualifying assistantship waiver",
                "type": "assistantship_tuition_and_fee_waiver",
                "amount": None,
                "currency": "USD",
                "automatic_consideration": False,
                "separate_application_required": False,
                "eligibility_summary": bi("A qualifying appointment carries the listed tuition and fee waiver. International students may not work above 50% while classes are in session.", "Uygun bir atama listelenen öğrenim ücreti ve harç muafiyetini taşır. Uluslararası öğrenciler ders döneminde %50'nin üzerinde çalışamaz."),
                "deadline": None,
                "url": FUNDING,
            },
        ],
        "funding_notes": bi(
            "All regular applicants are considered without a separate funding application, but RA decisions are made by individual faculty and proactive faculty contact is recommended. TA assignments depend on the advisor and are not guaranteed. Non-thesis MS students receive no AE departmental funding.",
            "Normal başvurular ayrı finansman başvurusu olmadan değerlendirilir; ancak RA kararlarını tek tek öğretim üyeleri verir ve proaktif iletişim önerilir. TA atamaları danışmana bağlıdır ve garanti edilmez. Tezsiz MS öğrencileri AE bölüm finansmanı alamaz.",
        ),
        "verification_notes": bi("Funding is pathway-dependent and competitive; admission is not a funding promise.", "Finansman program yoluna bağlı ve rekabetçidir; kabul finansman sözü değildir."),
    }

    row["living_profile"] = {
        "city_cost_level": "medium",
        "housing_difficulty": "medium",
        "housing_access": "not_guaranteed",
        "student_housing_available": True,
        "housing_application_separate": True,
        "housing_allocation_mode": "separate_housing_contract_subject_to_availability",
        "monthly_housing_rent_usd_per_month_min": 680,
        "monthly_housing_rent_usd_per_month_max": 1030,
        "average_room_rent_scope_label": bi("University apartment, whole unit", "Üniversite dairesi, bütün daire"),
        "average_room_rent_eur": None,
        "monthly_living_cost_eur_estimated": None,
        "living_risk": "medium",
        "housing_options": [
            {"provider": "Daniels Hall", "institution_owned": True, "guaranteed": False, "contract_options": ["academic_year", "12_month"]},
            {"provider": "Sherman Hall", "institution_owned": True, "guaranteed": False, "contract_options": ["academic_year", "12_month"]},
            {"provider": "Orchard Downs / Orchard South", "institution_owned": True, "guaranteed": False, "contract_options": ["apartment_lease"]},
            {"provider": "Goodwin-Green", "institution_owned": True, "guaranteed": False, "contract_options": ["apartment_lease"]},
            {"provider": "Ashton Woods", "institution_owned": True, "guaranteed": False, "contract_options": ["apartment_lease"]},
        ],
        "official_rent_items": [
            {"item": "Daniels/Sherman room-only academic-year contract", "amount_usd_min": 6906, "amount_usd_max": 9522, "period": "academic_year", "academic_year": "2026/2027"},
            {"item": "Daniels/Sherman 12-month room-only contract", "amount_usd_min": 10938, "amount_usd_max": 12480, "period": "12_month_contract", "academic_year": "2026/2027"},
            {"item": "University apartment whole-unit rent", "amount_usd_min": 680, "amount_usd_max": 1030, "period": "month", "academic_year": "2026/2027"},
            {"item": "Resident meal plan", "amount_usd_min": 2872, "amount_usd_max": 7446, "period": "academic_year", "academic_year": "2026/2027"},
        ],
        "official_living_cost_items": [
            {"item": "Official graduate food-and-housing allowance", "amount_usd": 16512, "period": "academic_year", "academic_year": "2026/2027"},
            {"item": "Official graduate books-and-supplies allowance", "amount_usd": 1200, "period": "academic_year", "academic_year": "2026/2027"},
            {"item": "Official graduate other-expenses allowance", "amount_usd": 3090, "period": "academic_year", "academic_year": "2026/2027"},
        ],
        "housing_notes": bi(
            "University-owned graduate housing exists, including Daniels and Sherman halls and several apartment communities. Housing requires a separate contract and is not stated as guaranteed; popular apartment options can be competitive. Whole-apartment rates are not per-person unless a co-tenant signs and shares the rent.",
            "Daniels ve Sherman salonları ile çeşitli apartman toplulukları dâhil üniversiteye ait lisansüstü konut vardır. Ayrı sözleşme gerekir ve garanti edildiği belirtilmez; popüler apartman seçenekleri rekabetçi olabilir. Daire fiyatları, ortak kiracı imzalayıp paylaşmadıkça kişi başı değil bütün daire içindir.",
        ),
        "verification_notes": bi("Official 2026/27 rates are used; no private-market average is inferred.", "Resmî 2026/27 fiyatları kullanılır; özel piyasa ortalaması çıkarılmaz."),
    }

    row["curriculum_profile"] = {
        "credit_system": "US semester credit hours",
        "credit_hours_total": 32,
        "course_count_fixed": False,
        "course_count_summary": bi("No fixed course count; both routes require 32 credit hours", "Sabit ders sayısı yok; iki yol da 32 kredi saati gerektirir"),
        "tracks": [
            bi("Aerodynamics, Fluid Mechanics, Combustion and Propulsion", "Aerodinamik, Akışkanlar Mekaniği, Yanma ve İtki"),
            bi("Astrodynamics, Controls and Dynamical Systems", "Astrodinamik, Kontrol ve Dinamik Sistemler"),
            bi("Structural Mechanics and Materials", "Yapı Mekaniği ve Malzemeler"),
        ],
        "specializations": [bi("Optional Computational Science and Engineering graduate concentration", "İsteğe bağlı Hesaplamalı Bilim ve Mühendislik lisansüstü uzmanlığı")],
        "requirement_components": [
            {"name": bi("AE 590 Departmental Seminar every on-campus semester", "Kampüste olunan her yarıyıl AE 590 Bölüm Semineri"), "credit_hours": 0},
            {"name": bi("Approved mathematics course", "Onaylı matematik dersi"), "credit_hours": "3–4"},
            {"name": bi("Aerospace Engineering breadth requirement", "Havacılık-Uzay Mühendisliği genişlik şartı"), "credit_hours": bi("6–8 thesis / 9–12 non-thesis", "Tezli 6–8 / tezsiz 9–12")},
            {"name": bi("Electives selected with an adviser", "Danışmanla seçilen seçmeli dersler"), "credit_hours": bi("12–15 thesis / 16–20 non-thesis", "Tezli 12–15 / tezsiz 16–20")},
        ],
        "mandatory_courses": [],
        "elective_courses": [],
        "thesis_required": None,
        "thesis_requirement_summary": bi("Required only for the thesis route: 8 hours of AE 599", "Yalnız tezli yolda zorunlu: 8 saat AE 599"),
        "thesis_credits_us": 8,
        "internship_required": False,
        "internship_notes": bi("No compulsory internship appears in the official 32-credit requirements.", "Resmî 32 kredilik şartlarda zorunlu staj yer almaz."),
        "pathway_details": {
            "thesis": {"mode": "on_campus_only", "technical_coursework_hours": 24, "thesis_hours": 8, "normal_duration": "2 years", "research_adviser_required": True},
            "non_thesis": {"mode": "on_campus_or_online", "coursework_hours": 32, "normal_duration": "1 year on campus", "research_adviser_required": False},
        },
        "verification_notes": bi(
            "The programme publishes credit-hour and breadth rules, not a universal course count. Course count varies with 3- or 4-credit choices and the selected route.",
            "Program evrensel bir ders sayısı değil, kredi saati ve genişlik kuralları yayımlar. Ders sayısı 3 veya 4 kredilik seçimlere ve seçilen yola göre değişir.",
        ),
    }

    row["category_profile"] = {
        "primary_categories": ["Aerospace Engineering", "Space Systems & Astronautics"],
        "secondary_categories": ["Aerodynamics & Fluid Mechanics", "Flight Mechanics & Control", "Propulsion & Energy", "Structures & Materials", "Systems & Design", "Scientific AI & Computational Engineering"],
        "subcategories": ["aerodynamics", "cfd", "astrodynamics", "gnc", "combustion", "rocket_propulsion", "aerospace_structures", "materials", "systems_engineering", "simulation_modelling", "space_systems", "satellite_systems"],
        "normalized_tags": ["aerodynamics", "cfd", "astrodynamics", "gnc", "combustion", "rocket_propulsion", "aerospace_structures", "materials", "systems_engineering", "simulation_modelling", "space_systems", "satellite_systems"],
        "category_scores": {},
        "category_evidence": [
            bi("The current catalog publishes three technical divisions and the department lists active research in astrodynamics, satellite design/manufacturing and space systems alongside aerodynamics, propulsion, controls and structures.", "Güncel katalog üç teknik bölümü yayımlar; bölüm aerodinamik, itki, kontrol ve yapıların yanında astrodinamik, uydu tasarım/üretimi ve uzay sistemlerinde aktif araştırma listeler."),
        ],
    }

    row["research_profile"] = {
        "department_research_areas": [
            bi("Astrodynamics, orbit determination and mission design", "Astrodinamik, yörünge belirleme ve görev tasarımı"),
            bi("Space systems and satellite design/manufacturing", "Uzay sistemleri ve uydu tasarım/üretimi"),
            bi("Aerodynamics, CFD, experimental fluids and hypersonics", "Aerodinamik, HAD, deneysel akışkanlar ve hipersonik"),
            bi("Combustion and propulsion", "Yanma ve itki"),
            bi("Controls, dynamical systems and estimation", "Kontrol, dinamik sistemler ve kestirim"),
            bi("Aerospace structures, materials and aeroelasticity", "Havacılık-uzay yapıları, malzemeler ve aeroelastisite"),
        ],
        "labs": [
            {"name": "Laboratory for Advanced Space Systems at Illinois (LASSI)", "officially_listed": True, "student_access": bi("Research placement dependent", "Araştırma yerleştirmesine bağlı")},
            {"name": "Aerodynamics Research Laboratory", "officially_listed": True, "student_access": bi("Research-student use and safety training are explicitly described", "Araştırma öğrencisi kullanımı ve güvenlik eğitimi açıkça tanımlanır")},
            {"name": "Combustion, Flow, and Plasma Interaction Laboratory", "officially_listed": True, "student_access": bi("Research placement dependent", "Araştırma yerleştirmesine bağlı")},
            {"name": "Computational Aeroacoustics Laboratory", "officially_listed": True, "student_access": bi("Research placement dependent", "Araştırma yerleştirmesine bağlı")},
            {"name": "Gas Dynamics Laboratory", "officially_listed": True, "student_access": bi("Research placement dependent", "Araştırma yerleştirmesine bağlı")},
            {"name": "Intelligent Robotics Laboratory", "officially_listed": True, "student_access": bi("Research placement dependent", "Araştırma yerleştirmesine bağlı")},
            {"name": "Laser and Optical Diagnostics Laboratory", "officially_listed": True, "student_access": bi("Research placement dependent", "Araştırma yerleştirmesine bağlı")},
        ],
        "research_centers": [],
        "notable_professors": [],
        "space_or_aerospace_projects": [],
        "student_teams": [],
        "satellite_or_flight_projects": [],
        "research_strength_summary": bi(
            "The department publishes broad, directly relevant research coverage and named facilities. Thesis students must secure a research adviser; facility or project access is not automatic with admission.",
            "Bölüm geniş ve doğrudan ilgili araştırma kapsamı ile adlandırılmış tesisler yayımlar. Tezli öğrenciler araştırma danışmanı bulmalıdır; tesis veya proje erişimi kabulle otomatik değildir.",
        ),
        "research_strength_score": None,
        "research_sources": [RESEARCH, ARL, ASTRODYNAMICS, CATALOG],
    }

    row["industry_ecosystem_profile"] = {
        "nearby_companies": [],
        "confirmed_partners": [],
        "officially_documented_research_sponsors": ["NASA", "DARPA", "Air Force Research Laboratory", "CU Aerospace", "KTi"],
        "space_agencies_or_public_bodies": ["NASA", "DARPA", "Air Force Research Laboratory"],
        "research_institutes": [],
        "startup_or_incubator_ecosystem": [],
        "internship_possibility": "unknown",
        "thesis_with_industry_possibility": "unknown",
        "career_relevance": "high_but_not_scored",
        "ecosystem_strength_score": None,
        "ecosystem_notes": bi(
            "The official astrodynamics page names current project sponsors; this is recorded as research sponsorship, not as a blanket programme partnership or hiring guarantee. Internship and employer-placement rates were not verified.",
            "Resmî astrodinamik sayfası güncel proje sponsorlarını adlandırır; bu, genel program ortaklığı veya işe alım garantisi değil araştırma sponsorluğu olarak kaydedilir. Staj ve işveren yerleştirme oranları doğrulanmamıştır.",
        ),
    }

    row["application_timeline_profile"] = {
        "academic_year": "recurring deadlines on current 2026/27 catalog",
        "intake_terms": ["Fall", "Spring"],
        "application_rounds": [
            {"round": bi("Fall MS thesis and full funding consideration", "Güz tezli MS ve tam finansman değerlendirmesi"), "opens": None, "deadline": "December 1", "decision": bi("Rolling after the deadline", "Son tarihten sonra kademeli")},
            {"round": bi("Fall MS non-thesis", "Güz tezsiz MS"), "opens": None, "deadline": "July 1", "decision": bi("Rolling after the deadline", "Son tarihten sonra kademeli")},
            {"round": bi("Spring MS thesis and full funding consideration", "Bahar tezli MS ve tam finansman değerlendirmesi"), "opens": None, "deadline": "October 1", "decision": bi("Rolling after the deadline", "Son tarihten sonra kademeli")},
            {"round": bi("Spring MS non-thesis", "Bahar tezsiz MS"), "opens": None, "deadline": "December 1", "decision": bi("Rolling after the deadline", "Son tarihten sonra kademeli")},
        ],
        "non_eu_deadline": bi("Same published pathway deadlines as other applicants; use the earlier thesis/funding deadline when seeking support", "Diğer adaylarla aynı yayımlanmış yol son tarihleri; finansman isteniyorsa daha erken tezli/finansman tarihini kullanın"),
        "eu_deadline": None,
        "scholarship_deadline": bi("Fall thesis full consideration: December 1; Spring thesis: October 1", "Güz tezli tam değerlendirme: 1 Aralık; bahar tezli: 1 Ekim"),
        "pre_enrolment_required": False,
        "visa_sensitive_deadline": bi("No separate international deadline is published. International applicants should not rely on the late July 1 non-thesis deadline without checking visa-document processing time.", "Ayrı uluslararası son tarih yayımlanmamıştır. Uluslararası adaylar vize belgesi işlem süresini kontrol etmeden geç 1 Temmuz tezsiz tarihine güvenmemelidir."),
        "application_result_timing": bi("Rolling after the relevant deadline; earlier complete files may receive decisions and funding offers earlier.", "İlgili son tarihten sonra kademeli; erken tamamlanan dosyalar karar ve finansman teklifini daha erken alabilir."),
        "timeline_risk": "medium",
        "deadline_notes": bi("The current official pages publish recurring month/day deadlines without a cycle year; no year has been invented in this record.", "Güncel resmî sayfalar dönem yılı olmadan yinelenen ay/gün tarihleri yayımlar; bu kayıtta yıl uydurulmamıştır."),
    }

    row["student_sentiment_profile"] = {
        "student_satisfaction_score": None,
        "teaching_quality_sentiment": "unknown",
        "workload_sentiment": "unknown",
        "workload_balance_sentiment": "unknown",
        "administration_sentiment": "unknown",
        "housing_sentiment": "mixed",
        "city_life_sentiment": "unknown",
        "international_student_sentiment": "unknown",
        "career_support_sentiment": "unknown",
        "funding_sentiment": "challenging_for_non_thesis_ms",
        "student_sentiment_summary": bi(
            "The small recent sample reinforces the official warning that non-thesis MS funding is scarce. Graduate-housing comments often value Orchard Downs for price and quiet, but also report uncertain assignment timing and strong demand. This is perception evidence, not a guarantee or market-price source.",
            "Küçük güncel örneklem, tezsiz MS finansmanının kıt olduğuna ilişkin resmî uyarıyı destekler. Lisansüstü konut yorumları Orchard Downs'ı fiyat ve sakinlik açısından sıkça olumlu bulurken atama zamanlamasının belirsiz ve talebin güçlü olduğunu bildirir. Bu algı kanıtıdır; garanti veya piyasa fiyatı kaynağı değildir.",
        ),
        "student_sentiment_sources": [
            {"url": "https://www.reddit.com/r/UIUC/comments/1rff8hn/admitted_to_uiuc_ae_ms_nonthesis_no_funding/", "platform": "Reddit r/UIUC", "topic": "AE MS non-thesis funding", "date": "2026-02-26", "approx_observations": 2, "access_status": "ok", "last_checked": TODAY, "confidence": "low"},
            {"url": "https://www.reddit.com/r/UIUC/comments/1cvflq0/incoming_graduate_student_housing_questions/", "platform": "Reddit r/UIUC", "topic": "graduate housing", "date": "2024-05-19", "approx_observations": 6, "access_status": "ok", "last_checked": TODAY, "confidence": "low"},
            {"url": "https://www.reddit.com/r/UIUC/comments/1is8ags/housing_question/", "platform": "Reddit r/UIUC", "topic": "Orchard Downs assignment uncertainty", "date": "2025-02-18", "approx_observations": 2, "access_status": "ok", "last_checked": TODAY, "confidence": "low"},
        ],
        "approximate_sample_size": 10,
        "date_range": "2024-2026",
        "sentiment_confidence": "low",
        "verification_notes": bi("No programme satisfaction score is computed from this small, partly housing-focused sample.", "Bu küçük ve kısmen konut odaklı örneklemden program memnuniyet puanı hesaplanmaz."),
    }

    sources = [
        source(CATALOG, "Aerospace Engineering, MS — 2026/27 Illinois Catalog", "official_program_page", ["program", "program_status", "curriculum", "admission", "deadline", "scholarship"], "Current official degree routes, 32-credit structures, technical divisions, admissions, deadlines and pathway-specific funding eligibility.", "Güncel resmî derece yolları, 32 kredilik yapılar, teknik bölümler, kabul, tarihler ve yola özgü finansman uygunluğu."),
        source(ADMISSIONS, "Illinois AE Admissions Requirements and Process", "official_admission_page", ["admission", "non_eu_eligibility", "required_documents", "language", "scholarship"], "Current GPA, prior-degree, GRE, TOEFL, document, international finance and automatic funding-consideration rules.", "Güncel ortalama, önceki derece, GRE, TOEFL, belge, uluslararası mali yeterlilik ve otomatik finansman değerlendirme kuralları."),
        source(FAQ, "Illinois AE Graduate Application FAQs", "official_admission_page", ["admission", "deadline", "scholarship", "language"], "Rolling decisions, early-file funding advantage, automatic funding consideration and pathway-duration explanation.", "Kademeli kararlar, erken dosyanın finansman avantajı, otomatik finansman değerlendirmesi ve yol süresi açıklaması."),
        source(DEADLINES, "Illinois AE Graduate Dates and Deadlines", "official_admission_page", ["deadline", "application_timeline", "scholarship"], "Current recurring pathway-specific deadlines.", "Güncel yinelenen program yolu son tarihleri."),
        source(ENGLISH, "Illinois Graduate College International Applicants", "official_admission_page", ["language", "admission", "non_eu_eligibility"], "Current date-dependent TOEFL scale, IELTS, exemptions, score validity and TA spoken-English rules.", "Güncel tarih-bağımlı TOEFL ölçeği, IELTS, muafiyet, puan geçerliliği ve TA sözlü İngilizce kuralları."),
        source(LANGUAGE, "Illinois Office of the Registrar — language of instruction", "official_program_page", ["language"], "The Registrar explicitly states that campus instruction is delivered in English except foreign-language courses.", "Registrar, yabancı dil dersleri dışında kampüs öğretiminin İngilizce olduğunu açıkça belirtir."),
        source(TUITION, "Illinois 2026/27 Graduate and Professional Tuition Rates", "official_tuition_page", ["tuition", "non_eu_eligibility"], "International Grainger Engineering annual and full-time semester tuition rates.", "Uluslararası Grainger Engineering yıllık ve tam zamanlı yarıyıl öğrenim ücretleri."),
        source(COST, "Illinois 2026/27 International Graduate Cost Calculator", "official_cost_of_living_page", ["tuition", "fees", "living", "housing"], "Official 12-credit international graduate Grainger estimate: tuition, fees, food/housing, books, other expenses and total.", "12 kredilik uluslararası Grainger lisansüstü resmî tahmini: öğrenim ücreti, harçlar, yiyecek/konut, kitap, diğer giderler ve toplam."),
        source(FUNDING, "Illinois AE Appointments and Funding", "official_scholarship_page", ["scholarship", "funding", "non_eu_eligibility"], "RA/TA assignment process, no guarantee, international workload cap and qualifying assistantship waiver coverage.", "RA/TA atama süreci, garanti olmaması, uluslararası çalışma sınırı ve uygun asistanlık muafiyet kapsamı."),
        source(HOUSING_COST, "Illinois University Housing Costs 2026/27", "official_housing_page", ["housing", "living"], "Current graduate hall, 12-month, meal-plan and university-apartment rates.", "Güncel lisansüstü salon, 12 aylık, yemek planı ve üniversite dairesi fiyatları."),
        source(HOUSING_OPTIONS, "Illinois Graduate Upper-Division Halls", "official_housing_page", ["housing"], "Official Daniels and Sherman graduate/upper-division housing routes and separate sign-up.", "Resmî Daniels ve Sherman lisansüstü/üst sınıf konut yolları ve ayrı başvuru."),
        source(RESEARCH, "Illinois Aerospace Engineering Research Areas", "official_department_page", ["research", "curriculum", "labs"], "Current department research-area and facility index including space systems, satellite design and astrodynamics.", "Uzay sistemleri, uydu tasarımı ve astrodinamik dâhil güncel bölüm araştırma alanı ve tesis dizini."),
        source(ARL, "Illinois Aerodynamics Research Laboratory", "official_department_page", ["research", "labs", "student_access"], "Named wind tunnels, diagnostics, research themes and explicit research-student shop access/training.", "Adlandırılmış rüzgâr tünelleri, ölçüm altyapısı, araştırma temaları ve araştırma öğrencisi atölye erişimi/eğitimi."),
        source(ASTRODYNAMICS, "Illinois Aerospace Astrodynamics Research", "official_department_page", ["research", "industry_ecosystem"], "Current astrodynamics topics and named research sponsors; sponsorship is not treated as a programme-wide partnership.", "Güncel astrodinamik konuları ve adlandırılmış araştırma sponsorları; sponsorluk program geneli ortaklık sayılmaz."),
        source(PRESTIGE, "Grainger Engineering Facts and Rankings", "official_ranking_page", ["prestige"], "Illinois reports the April 2026 national graduate aerospace specialty rank separately from fit.", "Illinois Nisan 2026 ulusal lisansüstü havacılık-uzay uzmanlık sırasını uyumdan ayrı raporlar."),
        source(QS, "QS World University Rankings 2027 — Illinois", "reliable_third_party_ranking", ["prestige"], "Current university-wide QS rank; not used as proof of aerospace technical fit.", "Güncel üniversite geneli QS sırası; havacılık-uzay teknik uyum kanıtı olarak kullanılmaz.", confidence="medium"),
        source("https://www.reddit.com/r/UIUC/comments/1rff8hn/admitted_to_uiuc_ae_ms_nonthesis_no_funding/", "Reddit r/UIUC — AE MS non-thesis funding discussion", "student_forum", ["student_sentiment"], "Small anecdotal sample about non-thesis funding; never used for an official programme fact.", "Tezsiz finansman hakkında küçük anekdotsal örneklem; hiçbir resmî program gerçeği için kullanılmaz.", confidence="low"),
        source("https://www.reddit.com/r/UIUC/comments/1cvflq0/incoming_graduate_student_housing_questions/", "Reddit r/UIUC — incoming graduate housing discussion", "student_forum", ["student_sentiment"], "Small anecdotal sample about graduate housing cost, quiet and demand.", "Lisansüstü konut fiyatı, sakinliği ve talebi hakkında küçük anekdotsal örneklem.", confidence="low"),
        source("https://www.reddit.com/r/UIUC/comments/1is8ags/housing_question/", "Reddit r/UIUC — Orchard Downs assignment discussion", "student_forum", ["student_sentiment"], "Small anecdotal sample about assignment timing uncertainty.", "Yerleştirme zamanı belirsizliği hakkında küçük anekdotsal örneklem.", confidence="low"),
    ]
    row["source_profile"] = {
        "primary_url": CATALOG,
        "secondary_urls": [item["url"] for item in sources[1:]],
        "last_verified": TODAY,
        "field_confidence": {
            "program_basic_info": "high",
            "program": "high",
            "language": "high",
            "admission": "high",
            "non_eu_eligibility": "high",
            "tuition": "high",
            "scholarship": "high",
            "deadline": "high",
            "curriculum": "high",
            "research": "high",
            "industry_ecosystem": "medium",
            "housing": "high",
            "living": "high",
            "sentiment": "low",
            "prestige": "high",
        },
        "source_reliability": "high",
        "verification_status": "verified",
        "needs_verification": False,
        "verification_notes": bi(
            "All core decision fields are supported by current official Illinois sources. Exact future-year application dates, private-market rent and placement outcomes remain deliberately unstated.",
            "Tüm temel karar alanları güncel resmî Illinois kaynaklarıyla desteklenir. Gelecek yıla ait kesin başvuru tarihleri, özel piyasa kirası ve yerleştirme sonuçları bilerek belirtilmez.",
        ),
        "source_log": sources,
    }

    row["decision_summary"] = {
        "best_for": [
            bi("Applicants seeking a broad, research-intensive aerospace MS with explicit space-systems and astrodynamics depth.", "Uzay sistemleri ve astrodinamik derinliği açık, geniş ve araştırma yoğun bir havacılık-uzay MS'i arayanlar."),
            bi("Students able to secure thesis supervision or competitively funded assistantship support.", "Tez danışmanı veya rekabetçi asistanlık finansmanı bulabilecek öğrenciler."),
        ],
        "not_ideal_for": [
            bi("Applicants who require guaranteed funding; non-thesis MS students receive no AE departmental funding.", "Garantili finansman gerekenler; tezsiz MS öğrencileri AE bölüm finansmanı alamaz."),
            bi("Applicants who need a fixed, prescriptive course list rather than a flexible 32-credit plan.", "Esnek 32 kredilik plan yerine sabit ve kuralcı ders listesi isteyenler."),
        ],
        "main_strengths": [
            bi("Current official research coverage includes astrodynamics, satellite design/manufacturing and space systems as well as major aeronautics domains.", "Güncel resmî araştırma kapsamı temel havacılık alanlarının yanında astrodinamik, uydu tasarım/üretimi ve uzay sistemlerini içerir."),
            bi("A flexible 32-credit MS with thesis and non-thesis routes and an optional computational science concentration.", "Tezli/tezsiz yolları ve isteğe bağlı hesaplamalı bilim uzmanlığı bulunan esnek 32 kredilik MS."),
            bi("Current official national graduate aerospace rank #7, kept separate from technical-fit evidence.", "Teknik uyum kanıtından ayrı tutulan güncel resmî ulusal lisansüstü havacılık-uzay sırası #7."),
        ],
        "main_risks": [
            bi("2026/27 international tuition and mandatory-fee estimate totals $46,380 before living costs.", "2026/27 uluslararası öğrenim ücreti ve zorunlu ücret tahmini yaşam giderlerinden önce toplam 46.380 $."),
            bi("Thesis funding is competitive and adviser-dependent; non-thesis MS is explicitly self-funded by the department.", "Tezli finansman rekabetçi ve danışmana bağlıdır; tezsiz MS bölüm tarafından açıkça öz finansmanlıdır."),
            bi("Graduate housing exists but requires a separate contract and is not guaranteed.", "Lisansüstü konut vardır ancak ayrı sözleşme gerekir ve garanti edilmez."),
            bi("English score rules are transitioning to the new TOEFL scale; exemption or Duolingo cases need programme confirmation.", "İngilizce puan kuralları yeni TOEFL ölçeğine geçmektedir; muafiyet veya Duolingo durumları program teyidi gerektirir."),
        ],
        "decision_summary": bi(
            "Technically broad and strong for both aeronautics and space, but the decision hinges on route: thesis applicants should apply by the funding deadline and seek an adviser; non-thesis applicants should budget for the full $67,182 official attendance estimate.",
            "Hem havacılık hem uzay için teknik olarak geniş ve güçlüdür; fakat karar seçilen yola bağlıdır: tezli adaylar finansman tarihine kadar başvurup danışman aramalı, tezsiz adaylar resmî 67.182 $ katılım bütçesinin tamamını planlamalıdır.",
        ),
        "pros": [],
        "cons": [],
        "verdict": bi("Strong direct aerospace/space fit with high cost and pathway-dependent funding risk.", "Yüksek maliyet ve yola bağlı finansman riskiyle güçlü doğrudan havacılık-uzay/uzay uyumu."),
    }

    row["scoring_inputs"] = {
        "academic_prestige": None,
        "research_output": None,
        "industry_links": None,
        "affordability": None,
        "admission_chance": None,
        "living_quality": None,
        "hard_flags": ["high_cost", "funding_not_guaranteed", "non_thesis_excluded_from_department_funding", "housing_not_guaranteed", "visa_timeline_sensitive"],
    }
    row["data_quality"] = {
        "status": "verified",
        "checked_official_source_count": 15,
        "verified_fields": ["program", "language", "admission", "non_eu_eligibility", "tuition", "scholarship", "deadline", "curriculum", "research", "housing", "living", "prestige"],
        "unverified_critical_fields": [],
        "has_checked_source_log": True,
        "audited_at": TODAY,
    }
    row["quality_control"] = {
        "checked_at": TODAY,
        "qc_status": "passed",
        "remaining_verification_tasks": [],
        "qc_notes": bi("Core claims use accessible current sources and pathway differences are explicit.", "Temel iddialar erişilebilir güncel kaynaklara dayanır ve program yolu farkları açıktır."),
        "failed_canary_tests": [],
    }

    DATA_PATH.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "id": row["id"],
                "status": row["data_quality"]["status"],
                "checked_official_source_count": row["data_quality"]["checked_official_source_count"],
                "verified_fields": row["data_quality"]["verified_fields"],
                "unverified_critical_fields": row["data_quality"]["unverified_critical_fields"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
