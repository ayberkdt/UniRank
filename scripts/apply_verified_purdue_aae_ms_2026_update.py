from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data_base" / "amerika.json"
TODAY = "2026-08-14"

PROGRAM = "https://engineering.purdue.edu/AAE/academics/graduate/graduate"
QUICKREF = "https://engineering.purdue.edu/AAE/academics/graduate/quickref"
ADMISSION = "https://engineering.purdue.edu/AAE/academics/graduate/admproced"
FAQ = "https://engineering.purdue.edu/AAE/academics/graduate/gradadmFAQ"
OGSPS = "https://www.purdue.edu/academics/ogsps/admissions/how-to-apply/"
FUNDING = "https://engineering.purdue.edu/AAE/academics/graduate/Graduate-School-Funding"
TUITION = "https://www.purdue.edu/treasurer/finance/bursar-office/tuition/fee-rates-2026-2027/graduate-tuition-and-fees-2026-2027/"
INSURANCE = "https://www.purdue.edu/push/insurance-payment/index.php"
HOUSING_FAQ = "https://www.housing.purdue.edu/my-housing/info/general/faqs.html"
HOUSING_NEW = "https://www.housing.purdue.edu/my-housing/apply/new-undergrad-students.html"
WELCOME = "https://www.purdue.edu/academics/ogsps/documents/admissions/Graduate%20Student%20Welcome%20Packet%20April%202025.pdf"
OFFCAMPUS = "https://offcampushousing.purdue.edu/"
OVERVIEW = "https://engineering.purdue.edu/AAE/aboutus/overview"
ZUCROW = "https://engineering.purdue.edu/Zucrow"
ZUCROW_CAPABILITIES = "https://engineering.purdue.edu/Zucrow/capabilities/index_html"
ASTRODYNAMICS = "https://engineering.purdue.edu/AAE/research/astrodynamics"
AUTONOMY = "https://engineering.purdue.edu/AAE/research/dynamics"
ROLLS_ROYCE = "https://engineering.purdue.edu/Frontiers/2026/industry-partnerships/rolls-royce-purdue-safeguard-the-future"
RANKING = "https://engineering.purdue.edu/Engr/AboutUs/FactsFigures/Rankings/graduate"
QS = "https://www.topuniversities.com/universities/purdue-university"

REDDIT_HOUSING_1 = "https://www.reddit.com/r/PurdueHousing/comments/1t6yk22/incoming_purdue_grad_student_looking_for_housing/"
REDDIT_HOUSING_2 = "https://www.reddit.com/r/PurdueHousing/comments/1tviipp/incoming_msbaim_student_looking_for_housing/"
REDDIT_HOUSING_3 = "https://www.reddit.com/r/Purdue/comments/1rnqu5p/grad_student_housing_pointers/"


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
    row = next(item for item in rows if item.get("id") == "purdue-aae")

    row.update(
        {
            "country": "United States",
            "university": "Purdue University",
            "university_native_name": "Purdue University",
            "city": "West Lafayette",
            "program_name": "Master of Science in Aeronautics and Astronautics (on-campus)",
            "program_native_name": "Master of Science in Aeronautics and Astronautics (on-campus)",
            "program_degree": "MSAA",
            "degree_level": "Master",
            "duration": bi("Not explicitly published for the on-campus MSAA routes", "Kampüsteki MSAA yolları için açıkça yayımlanmamıştır"),
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
            "tuition_usd_per_year": 29194,
            "annual_fee_usd": 400,
            "qs_ranking": 100,
            "qs_ranking_display": "#=100",
            "qs_ranking_year": 2027,
        }
    )

    row["prestige_profile"] = {
        "qs_world_rank": 100,
        "qs_edition": 2027,
        "qs_source_url": QS,
        "current_us_news_graduate_engineering_rank": 4,
        "current_us_news_aerospace_rank": 5,
        "ranking_edition": "2026/2027",
        "official_ranking_source_url": RANKING,
        "interpretation": bi("University-wide and subject rankings are context only; technical fit is evidenced separately through curriculum, laboratories and current research.", "Üniversite geneli ve alan sıralamaları yalnızca bağlamdır; teknik uyum müfredat, laboratuvarlar ve güncel araştırmalarla ayrıca kanıtlanır."),
    }

    row["eligibility_profile"] = {
        "eligible_for_non_eu": True,
        "required_previous_degree": bi("A bachelor's degree or equivalent credential is required by Purdue Graduate School; AAE publishes a 3.25/4.0 GPA as strongly recommended for MS applicants.", "Purdue Graduate School lisans derecesi veya denk bir diploma ister; AAE, MS adayları için 4,0 üzerinden 3,25 GPA'i güçlü biçimde tavsiye eder."),
        "accepted_backgrounds": [],
        "minimum_gpa": None,
        "recommended_gpa": 3.25,
        "recommended_not_minimum": True,
        "admission_mode": "selective_holistic",
        "admission_risk": "high",
        "required_documents": [
            bi("Online graduate application", "Çevrimiçi lisansüstü başvuru"),
            bi("Academic statement of purpose", "Akademik amaç mektubu"),
            bi("Personal history statement", "Kişisel geçmiş beyanı"),
            bi("Transcripts; international credentials require original-language and English versions", "Transkriptler; uluslararası belgeler özgün dilde ve İngilizce sürümleriyle gerekir"),
            bi("International diploma or provisional certificate, when applicable", "Uygunsa uluslararası diploma veya geçici mezuniyet belgesi"),
            bi("Resume or curriculum vitae", "Özgeçmiş"),
            bi("Three references", "Üç referans"),
            bi("Official GRE General score unless an AAE waiver applies", "AAE muafiyeti yoksa resmî GRE General puanı"),
            bi("English-proficiency evidence unless an exemption applies", "Muafiyet yoksa İngilizce yeterlilik kanıtı"),
        ],
        "motivation_letter_required": True,
        "personal_statement_required": True,
        "cv_required": True,
        "recommendation_required": True,
        "recommendation_letter_count": 3,
        "portfolio_required": False,
        "interview_required": False,
        "interview_policy": "not_listed_in_checked_official_requirements",
        "application_fee_usd": 75,
        "application_fee_scope": "international applicant; up to two graduate programme selections",
        "application_fee_waiver": bi("A general international economic-hardship waiver is not published. Limited participation-based waivers may apply; applicants must verify eligibility before relying on one.", "Uluslararası adaylar için genel ekonomik güçlük muafiyeti yayımlanmamıştır. Sınırlı program-katılımı muafiyetleri olabilir; adaylar buna güvenmeden önce uygunluğu doğrulamalıdır."),
        "gre": {
            "policy": "required_with_waivers",
            "test_type": "GRE General",
            "minimum_scores": {},
            "recommended_scores": {"verbal": 156, "quantitative": 159, "analytical_writing": 4.0},
            "recommended_not_minimum": True,
            "validity_years": 5,
            "waiver_rules": [
                bi("Purdue AAE graduates and current Purdue AAE undergraduates", "Purdue AAE mezunları ve mevcut Purdue AAE lisans öğrencileri"),
                bi("At least three years of relevant professional experience; internships, co-ops and student research do not count", "En az üç yıl ilgili profesyonel deneyim; staj, co-op ve öğrenci araştırması sayılmaz"),
            ],
            "waiver_process": bi("Submit the application, then email the AAE graduate office to request the waiver.", "Başvuruyu gönderin, ardından muafiyet istemek için AAE lisansüstü ofisine e-posta gönderin."),
            "source_ids": [ADMISSION],
        },
        "notes_for_turkish_students": bi("Turkish applicants follow the international route. Upload both original-language and English credential versions; Purdue requests official credentials later according to the admission instructions.", "Türkiye'den başvuranlar uluslararası yolu izler. Belgelerin özgün dil ve İngilizce sürümlerini yükleyin; Purdue resmî belgeleri kabul talimatlarına göre daha sonra ister."),
        "verification_notes": bi("The published 3.25 GPA and GRE figures are recommendations, not guaranteed admission cutoffs. No eligible undergraduate-major list was invented.", "Yayımlanan 3,25 GPA ve GRE değerleri tavsiyedir; garantili kabul eşiği değildir. Uygun lisans alanları listesi uydurulmamıştır."),
    }

    row["language_profile"] = {
        "teaching_language": ["Unknown"],
        "teaching_languages": ["Unknown"],
        "english_required": True,
        "accepted_english_tests": [
            {"test": "TOEFL iBT", "minimum_score_policy": {"on_or_after_2026_01_21": {"overall": 4.0, "reading": 4.0, "listening": 3.5, "speaking": 3.5, "writing": 4.0}, "before_2026_01_21": {"overall": 80, "reading": 19, "listening": 14, "speaking": 18, "writing": 18}}, "mybest_accepted": False},
            {"test": "TOEFL Essentials", "minimum_overall": 8, "minimum_each_section": 8},
            {"test": "IELTS Academic", "minimum_overall": 6.5, "minimum_reading": 6.5, "minimum_listening": 6.0, "minimum_speaking": 6.0, "minimum_writing": 5.5, "one_skill_retake_accepted": False},
            {"test": "Duolingo English Test", "minimum_overall": 115, "minimum_each_integrated_subscore": 115},
        ],
        "score_validity_years": 2,
        "english_exemptions": [bi("Degree completed within the previous 36 months at an institution whose primary language of instruction is English and which is located in a country Purdue recognizes as native-English-speaking", "Son 36 ayda, ana öğretim dili İngilizce olan ve Purdue'nun ana dili İngilizce ülke olarak tanıdığı bir ülkedeki kurumdan tamamlanan derece")],
        "international_ta_spoken_english_note": bi("AAE's current FAQ lists TOEFL speaking 27 or Purdue's OEPT for TA eligibility; appointment still depends on department recommendation and current university rules.", "AAE'nin güncel SSS sayfası TA uygunluğu için TOEFL konuşma 27 veya Purdue OEPT'yi listeler; atama yine bölüm tavsiyesine ve güncel üniversite kurallarına bağlıdır."),
        "language_risk": "medium",
        "verification_notes": bi("Official sources verify English-proficiency admission requirements but do not explicitly state the on-campus MSAA teaching language. Teaching language therefore remains Unknown under the no-inference rule.", "Resmî kaynaklar İngilizce yeterlilik kabul şartlarını doğrular ancak kampüsteki MSAA öğretim dilini açıkça belirtmez. Çıkarım yapmama kuralı gereği öğretim dili Unknown kalır."),
    }

    row["cost_profile"] = {
        "academic_year": "2026/2027",
        "currency": "USD",
        "tuition_and_mandatory_fees_usd_per_semester": 14597,
        "tuition_usd_per_year": 29194,
        "tuition_year_definition": "two regular fall/spring semesters at 8+ credits, international rate",
        "academic_billed_baseline_usd_per_two_terms": 29194,
        "housing_and_food_allowance_usd_per_academic_year": 16734,
        "books_and_supplies_usd_per_academic_year": 750,
        "transportation_allowance_usd_per_academic_year": 570,
        "miscellaneous_and_federal_loan_fees_usd_per_academic_year": 2550,
        "total_cost_of_attendance_usd_per_academic_year": 49798,
        "application_fee_usd": 75,
        "health_insurance_required_for_international_students": True,
        "health_insurance_waiver_possible": True,
        "health_insurance_premium_usd": None,
        "health_insurance_premium_status": "needs_verification",
        "complete_program_cost_usd": None,
        "tuition_basis": "Purdue regular graduate Fall/Spring flat rate, international, 8+ credits",
        "tuition_items": [
            {"item": bi("General service", "Genel hizmet"), "amount_usd": 9718, "period": "academic_year"},
            {"item": bi("Student fitness and wellness fee", "Öğrenci spor ve sağlık ücreti"), "amount_usd": 234, "period": "academic_year"},
            {"item": bi("Student activity fee", "Öğrenci etkinlik ücreti"), "amount_usd": 40, "period": "academic_year"},
            {"item": bi("Nonresident tuition", "Eyalet dışı öğrenim ek ücreti"), "amount_usd": 18802, "period": "academic_year"},
            {"item": bi("International fee", "Uluslararası öğrenci ücreti"), "amount_usd": 400, "period": "academic_year"},
        ],
        "verification_notes": bi("The $49,798 official academic-year budget includes the published international flat-rate tuition, housing/food allowance and other estimates. The page is internally inconsistent about off-campus transportation ($285 in the table versus $550 in a note); the database preserves the table and official total without silently recalculating it. Insurance is mandatory but its 2026/27 premium was not verified, so full-program cost is not claimed.", "49.798 $ resmî akademik yıl bütçesi yayımlanan uluslararası sabit ücreti, konut/yemek payını ve diğer tahminleri içerir. Sayfa off-campus ulaşım konusunda kendi içinde tutarsızdır (tabloda 285 $, notta 550 $); veritabanı tabloyu ve resmî toplamı sessizce yeniden hesaplamadan korur. Sigorta zorunludur ancak 2026/27 primi doğrulanamadığı için tam program maliyeti iddia edilmez."),
    }

    row["scholarship_profile"] = {
        "available_types": ["research_assistantship", "teaching_assistantship", "external_fellowship", "current_student_scholarship"],
        "non_eu_eligible": "position_or_award_specific",
        "application_mode": "mixed",
        "application_mode_detail": "position_specific_faculty_outreach_or_nomination",
        "automatic_consideration": False,
        "separate_application_required": True,
        "admission_funding_guaranteed": False,
        "funding_priority_deadline": "December 1 for Fall",
        "opportunities": [
            {"name": "Research assistantship", "type": "competitive_employment", "amount": None, "currency": "USD", "automatic_consideration": False, "separate_application_required": True, "deadline": None, "eligibility_summary": bi("Faculty hire for funded research; applicants are encouraged to contact relevant faculty. No position is guaranteed by admission.", "Öğretim üyeleri fonlu araştırma için işe alır; adayların ilgili öğretim üyeleriyle iletişime geçmesi teşvik edilir. Kabul hiçbir pozisyonu garanti etmez."), "url": FUNDING},
            {"name": "AAE teaching assistantship", "type": "competitive_employment", "amount": None, "currency": "USD", "automatic_consideration": False, "separate_application_required": True, "deadline": None, "eligibility_summary": bi("Assigned by the Graduate Chair with faculty recommendations; published preference is PhD, thesis MS, then non-thesis MS.", "Graduate Chair tarafından öğretim üyesi tavsiyeleriyle atanır; yayımlanan tercih sırası PhD, tezli MS, ardından tezsiz MS'tir."), "url": FUNDING},
        ],
        "funding_notes": bi("Admission does not guarantee funding. December 1 gives Fall applicants the fullest funding consideration, but RA hiring requires faculty matching and TA consideration depends on faculty recommendation. Department scholarships may not be offered every year and are generally emailed to current students.", "Kabul finansmanı garanti etmez. 1 Aralık, Güz adaylarına en kapsamlı finansman değerlendirmesini sağlar; ancak RA için öğretim üyesi eşleşmesi, TA için öğretim üyesi tavsiyesi gerekir. Bölüm bursları her yıl sunulmayabilir ve genellikle mevcut öğrencilere e-postayla bildirilir."),
        "verification_notes": bi("Assistantships are employment/research appointments, not automatic admission scholarships. No award amount or international eligibility was generalized across position-specific opportunities.", "Asistanlıklar otomatik kabul bursu değil, çalışma/araştırma görevidir. Pozisyona özgü fırsatlarda tutar veya uluslararası uygunluk genellenmemiştir."),
    }

    row["living_profile"] = {
        "city_cost_level": "medium",
        "housing_difficulty": "medium",
        "living_risk": "medium",
        "housing_access": "not_offered",
        "housing_access_detail": "not_offered_as_general_graduate_option",
        "student_housing_available": False,
        "housing_application_separate": False,
        "housing_allocation_mode": "not_applicable_general_university_residences_are_undergraduate_facing",
        "monthly_housing_rent_usd_per_month_min": None,
        "monthly_housing_rent_usd_per_month_max": None,
        "average_room_rent_usd": None,
        "housing_options": [
            {"provider": "Purdue Off-Campus Housing portal", "institution_owned": False, "guaranteed": False, "price_verified_by_university": False, "url": OFFCAMPUS},
        ],
        "official_living_cost_items": [
            {"item": bi("Housing and food allowance", "Konut ve yemek bütçe payı"), "amount_usd": 16734, "period": "academic_year", "academic_year": "2026/2027"},
            {"item": bi("Books and course materials allowance", "Kitap ve ders malzemesi payı"), "amount_usd": 750, "period": "academic_year", "academic_year": "2026/2027"},
            {"item": bi("Transportation allowance in the official table", "Resmî tablodaki ulaşım payı"), "amount_usd": 570, "period": "academic_year", "academic_year": "2026/2027"},
            {"item": bi("Miscellaneous and federal-loan-fee allowance", "Çeşitli giderler ve federal kredi ücreti payı"), "amount_usd": 2550, "period": "academic_year", "academic_year": "2026/2027"},
        ],
        "housing_notes": bi("University Residences eligibility and new-housing application pages are undergraduate-facing. Purdue's graduate welcome packet instead directs graduate students to the off-campus portal and assistance service. The $16,734 figure is a combined housing/food budget allowance, not a verified rent, vacancy promise or graduate residence rate.", "University Residences uygunluk ve yeni konut başvuru sayfaları lisans öğrencilerine yöneliktir. Purdue'nun lisansüstü karşılama paketi lisansüstü öğrencileri off-campus portalına ve destek hizmetine yönlendirir. 16.734 $ değeri doğrulanmış kira, boş yer vaadi veya lisansüstü yurt ücreti değil; birleşik konut/yemek bütçe payıdır."),
        "verification_notes": bi("Private-market listing examples were not converted into an average rent. Housing difficulty is an interpretation based on the absence of a general graduate university-residence route and dependence on the private market.", "Özel piyasa ilan örnekleri ortalama kiraya dönüştürülmemiştir. Konut zorluğu, genel lisansüstü üniversite yurdu yolunun bulunmaması ve özel piyasaya bağımlılık temelinde yorumlanmıştır."),
    }

    row["curriculum_profile"] = {
        "credit_system": "US semester credit hours",
        "credit_hours_total": 30,
        "course_count_fixed": False,
        "course_count_summary": bi("Non-thesis route: exactly 10 three-credit graduate courses. Thesis route: 21 coursework credits plus at least 9 AAE 698 research credits.", "Tezsiz yol: tam olarak 10 adet üç kredilik lisansüstü ders. Tezli yol: 21 ders kredisi ve en az 9 AAE 698 araştırma kredisi."),
        "tracks": [
            bi("Aerodynamics", "Aerodinamik"),
            bi("Aerospace Systems", "Havacılık ve Uzay Sistemleri"),
            bi("Astrodynamics and Space Applications", "Astrodinamik ve Uzay Uygulamaları"),
            bi("Autonomy and Control", "Otonomi ve Kontrol"),
            bi("Propulsion", "İtki"),
            bi("Structures and Materials", "Yapılar ve Malzemeler"),
        ],
        "pathway_details": {
            "non_thesis": {"total_credit_hours": 30, "course_count": 10, "primary_area_courses": 4, "secondary_area_courses": 2, "mathematics_courses": 2, "technical_elective_courses": 2, "thesis_hours": 0, "major_professor_count": 1},
            "thesis": {"total_credit_hours": 30, "coursework_hours": 21, "research_hours_minimum": 9, "primary_area_courses": 3, "secondary_area_courses": 2, "mathematics_courses": 2, "advisory_committee_members": 3},
        },
        "requirement_components": [
            {"name": bi("Non-thesis primary focus", "Tezsiz ana odak"), "course_count": 4, "credit_hours": 12},
            {"name": bi("Non-thesis secondary focus", "Tezsiz ikincil odak"), "course_count": 2, "credit_hours": 6},
            {"name": bi("Non-thesis mathematics", "Tezsiz matematik"), "course_count": 2, "credit_hours": 6},
            {"name": bi("Non-thesis technical electives", "Tezsiz teknik seçmeliler"), "course_count": 2, "credit_hours": 6},
            {"name": bi("Thesis coursework and AAE 698 research", "Tezli dersler ve AAE 698 araştırması"), "credit_hours": bi("21 coursework + at least 9 research", "21 ders + en az 9 araştırma")},
        ],
        "minimum_cumulative_gpa": 3.0,
        "non_thesis_primary_course_minimum_grade": "B-",
        "plan_of_study_due": "end of first semester",
        "thesis_required": False,
        "thesis_route_available": True,
        "internship_required": False,
        "internship_notes": bi("No compulsory internship appears in either official MSAA route requirements.", "Resmî MSAA yollarının hiçbirinde zorunlu staj görünmez."),
        "space_systems_engineering_major_delivery": "online_only_not_part_of_this_on_campus_record",
        "verification_notes": bi("Thesis and non-thesis routes are kept distinct. The separately advertised Space Systems Engineering major is online-only and is not presented as an on-campus MSAA track.", "Tezli ve tezsiz yollar ayrı tutulur. Ayrı tanıtılan Space Systems Engineering ana dalı yalnızca çevrimiçidir ve kampüsteki MSAA izi gibi sunulmaz."),
    }

    row["category_profile"] = {
        "primary_categories": ["Aerospace Engineering", "Space Systems & Astronautics"],
        "secondary_categories": ["Aerodynamics & Fluid Mechanics", "Flight Mechanics & Control", "Propulsion & Energy", "Structures & Materials", "Systems & Design", "Scientific AI & Computational Engineering"],
        "subcategories": ["aerodynamics", "hypersonics", "astrodynamics", "mission_design", "gnc", "autonomy", "rocket_propulsion", "turbomachinery", "aerospace_structures", "materials", "space_systems", "remote_sensing"],
        "normalized_tags": ["aerodynamics", "hypersonics", "astrodynamics", "mission_design", "gnc", "autonomy", "rocket_propulsion", "turbomachinery", "aerospace_structures", "materials", "space_systems", "remote_sensing"],
        "category_scores": {},
        "category_evidence": [bi("The official six-area curriculum and current research pages directly cover aeronautical and space domains.", "Resmî altı alanlı müfredat ve güncel araştırma sayfaları havacılık ve uzay alanlarını doğrudan kapsar.")],
    }

    row["research_profile"] = {
        "department_research_areas": [bi("Aerodynamics", "Aerodinamik"), bi("Aerospace systems", "Havacılık ve uzay sistemleri"), bi("Astrodynamics and space applications", "Astrodinamik ve uzay uygulamaları"), bi("Autonomy and control", "Otonomi ve kontrol"), bi("Propulsion", "İtki"), bi("Structures and materials", "Yapılar ve malzemeler")],
        "labs": [
            {"name": "Maurice J. Zucrow Laboratories", "officially_listed": True, "student_access": bi("Research appointment and faculty supervision dependent", "Araştırma görevi ve öğretim üyesi danışmanlığına bağlı")},
            {"name": "Space Flight Projects Laboratory", "officially_listed": True, "student_access": bi("Research placement dependent", "Araştırma yerleştirmesine bağlı")},
            {"name": "Space Hardware Laboratory", "officially_listed": True, "student_access": bi("Research placement dependent", "Araştırma yerleştirmesine bağlı")},
            {"name": "Optical GNC Laboratory", "officially_listed": True, "student_access": bi("Research placement dependent", "Araştırma yerleştirmesine bağlı")},
            {"name": "Purdue Optical Ground Station", "officially_listed": True, "student_access": bi("Research placement dependent", "Araştırma yerleştirmesine bağlı")},
        ],
        "facilities": [bi("24-acre Zucrow propulsion complex with flight-scale and flight-condition testing", "Uçuş ölçeği ve uçuş koşulu testleri yapan 24 akrelik Zucrow itki kompleksi"), bi("ISO 8 space-hardware clean room, mission operations and tracking facilities", "ISO 8 uzay donanımı temiz odası, görev operasyonu ve takip tesisleri")],
        "research_strength_summary": bi("Purdue combines broad aerospace coverage with unusually deep propulsion and space-flight infrastructure. Access is not automatic with MS admission; it depends on the thesis route, faculty matching or a funded research appointment.", "Purdue geniş havacılık-uzay kapsamını sıra dışı derinlikte itki ve uzay uçuşu altyapısıyla birleştirir. Erişim MS kabulüyle otomatik değildir; tez yoluna, öğretim üyesi eşleşmesine veya fonlu araştırma görevine bağlıdır."),
        "research_strength_score": None,
        "research_sources": [OVERVIEW, ZUCROW, ZUCROW_CAPABILITIES, ASTRODYNAMICS, AUTONOMY],
    }

    row["industry_ecosystem_profile"] = {
        "nearby_companies": [],
        "confirmed_partners": [
            {"name": "Rolls-Royce", "relationship": bi("Purdue reports a 70+ year relationship, a US University Technology Center since 2003 and a 10-year $75 million strategic alliance signed in 2022.", "Purdue 70 yılı aşan ilişki, 2003'ten beri ABD University Technology Center ve 2022'de imzalanan 10 yıllık 75 milyon dolarlık stratejik ittifak bildirir."), "source_url": ROLLS_ROYCE},
        ],
        "space_agencies_or_public_bodies": ["FAA", "US Department of Defense", "NASA"],
        "internship_possibility": "possible_but_not_program_requirement",
        "thesis_with_industry_possibility": "not_guaranteed",
        "career_relevance": "high_but_not_scored",
        "ecosystem_strength_score": None,
        "international_student_constraints": [bi("The department explicitly reports ITAR-controlled research activity; international-student eligibility can therefore vary by project and employer.", "Bölüm ITAR kontrollü araştırma faaliyeti yürüttüğünü açıkça bildirir; bu nedenle uluslararası öğrenci uygunluğu projeye ve işverene göre değişebilir.")],
        "ecosystem_notes": bi("Only the current officially documented Rolls-Royce relationship is recorded as an industry partnership. Agency research activity and ITAR context are not converted into hiring guarantees.", "Yalnızca güncel ve resmî olarak belgelenen Rolls-Royce ilişkisi sanayi ortaklığı olarak kaydedilir. Kamu kurumu araştırmaları ve ITAR bağlamı işe alım garantisine dönüştürülmez."),
    }

    row["application_timeline_profile"] = {
        "academic_year": "current recurring deadlines; Spring 2027 explicitly confirmed",
        "intake_terms": ["Fall", "Spring"],
        "application_rounds": [
            {"round": bi("Fall on-campus — fullest funding consideration", "Güz kampüs — en kapsamlı finansman değerlendirmesi"), "opens": None, "deadline": "December 1 of the preceding year", "decision": bi("Usually about eight weeks for international applicants, but timing varies", "Uluslararası adaylar için genellikle yaklaşık sekiz hafta; süre değişebilir")},
            {"round": bi("Fall on-campus — final programme deadline", "Güz kampüs — nihai program tarihi"), "opens": None, "deadline": "March 30 of the same year", "decision": bi("Usually about eight weeks for international applicants, but timing varies", "Uluslararası adaylar için genellikle yaklaşık sekiz hafta; süre değişebilir")},
            {"round": bi("Spring on-campus", "Bahar kampüs"), "opens": None, "deadline": "September 15 of the preceding year", "decision": bi("Usually about eight weeks for international applicants, but timing varies", "Uluslararası adaylar için genellikle yaklaşık sekiz hafta; süre değişebilir")},
        ],
        "non_eu_deadline": bi("Programme deadlines are the same; international applicants should apply early enough for Purdue's international processing and visa sequence.", "Program tarihleri aynıdır; uluslararası adaylar Purdue'nun uluslararası işlem ve vize sırasına yetecek kadar erken başvurmalıdır."),
        "scholarship_deadline": bi("December 1 maximizes Fall funding consideration but is not a funding guarantee; RA/TA processes remain position-specific.", "1 Aralık Güz finansman değerlendirmesini en üst düzeye çıkarır ancak finansman garantisi değildir; RA/TA süreçleri pozisyona özgü kalır."),
        "pre_enrolment_required": False,
        "visa_sensitive_deadline": bi("After admission, international processing, proof-of-funds and immigration documents must be completed early enough for visa issuance. Graduate School internal forwarding cutoffs are not substituted for the AAE application deadlines.", "Kabulden sonra uluslararası işlem, mali yeterlilik ve göçmenlik belgeleri vize düzenlenmesine yetecek kadar erken tamamlanmalıdır. Graduate School iç yönlendirme tarihleri AAE başvuru tarihlerinin yerine kullanılmaz."),
        "offer_response_deadlines": {"fall": "June 1", "spring": "November 15"},
        "application_result_timing": bi("AAE reports roughly eight weeks for international and six weeks for domestic applicants, varying with completeness and review volume. AAE recommends admission and OGSPS issues the final decision.", "AAE, eksiksizlik ve inceleme yoğunluğuna göre değişmek üzere uluslararası adaylar için yaklaşık sekiz, yerli adaylar için altı hafta bildirir. AAE kabul önerir; nihai kararı OGSPS verir."),
        "timeline_risk": "medium",
        "deadline_notes": bi("Online-programme deadlines were deliberately excluded from this on-campus record. Incomplete or late applications are not reviewed.", "Çevrimiçi program tarihleri bu kampüs kaydından bilerek çıkarılmıştır. Eksik veya geç başvurular incelenmez."),
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
        "student_sentiment_summary": bi("The small recent sample is limited to graduate housing searches and perceptions of price, location and safety. It is insufficient for a programme satisfaction score and is not used as rent evidence.", "Küçük güncel örneklem lisansüstü konut arayışı ile fiyat, konum ve güvenlik algılarıyla sınırlıdır. Program memnuniyet puanı için yetersizdir ve kira kanıtı olarak kullanılmaz."),
        "student_sentiment_sources": [
            {"url": REDDIT_HOUSING_1, "platform": "Reddit r/PurdueHousing", "topic": "incoming graduate housing search", "date": "2026", "approx_observations": 4, "access_status": "ok", "last_checked": TODAY, "confidence": "low"},
            {"url": REDDIT_HOUSING_2, "platform": "Reddit r/PurdueHousing", "topic": "graduate housing options", "date": "2026", "approx_observations": 2, "access_status": "ok", "last_checked": TODAY, "confidence": "low"},
            {"url": REDDIT_HOUSING_3, "platform": "Reddit r/Purdue", "topic": "graduate housing pointers", "date": "2026", "approx_observations": 4, "access_status": "ok", "last_checked": TODAY, "confidence": "low"},
        ],
        "approximate_sample_size": 10,
        "date_range": "2026",
        "sentiment_confidence": "low",
        "verification_notes": bi("No teaching, workload, administration or career sentiment was generalized from unrelated Purdue discussions.", "İlgisiz Purdue tartışmalarından öğretim, iş yükü, idare veya kariyer algısı genellenmemiştir."),
    }

    sources = [
        source(PROGRAM, "Purdue AAE Graduate Program", "official_program_page", ["program", "program_status", "curriculum", "tracks"], "Current MSAA route and six-area programme overview.", "Güncel MSAA yolları ve altı alanlı program özeti."),
        source(QUICKREF, "Purdue AAE Graduate Quick Reference", "official_curriculum_page", ["curriculum", "courses", "tracks", "degree_requirements"], "Current 30-credit thesis/non-thesis requirements and exact non-thesis course count.", "Güncel 30 kredilik tezli/tezsiz şartlar ve kesin tezsiz ders sayısı."),
        source(ADMISSION, "Purdue AAE Graduate Admission Procedure", "official_admission_page", ["admission", "deadline", "gre", "language", "required_documents"], "Current on-campus deadlines, documents, GPA/GRE guidance and English-test rules.", "Güncel kampüs tarihleri, belgeler, GPA/GRE rehberi ve İngilizce sınav kuralları."),
        source(FAQ, "Purdue AAE Graduate Admission FAQs", "official_admission_page", ["admission", "funding", "deadline", "language", "visa"], "Decision timing, funding separation, adviser process, TA English rule and deferral policy.", "Karar süresi, finansman ayrımı, danışman süreci, TA İngilizce kuralı ve erteleme politikası."),
        source(OGSPS, "Purdue OGSPS How to Apply", "official_admission_page", ["non_eu_eligibility", "application_fee", "language", "admission", "visa"], "International application route, $75 fee, current test minimums and Graduate School process.", "Uluslararası başvuru yolu, 75 $ ücret, güncel sınav tabanları ve Graduate School süreci."),
        source(FUNDING, "Purdue AAE Graduate School Funding", "official_scholarship_page", ["scholarship", "funding", "non_eu_eligibility"], "Current RA outreach, TA nomination and PhD/thesis-MS/non-thesis-MS preference order.", "Güncel RA iletişimi, TA aday gösterme ve PhD/tezli MS/tezsiz MS tercih sırası."),
        source(TUITION, "Purdue Graduate Tuition and Fees 2026/27", "official_tuition_page", ["tuition", "fees", "living", "cost"], "Current international regular graduate flat rate and official academic-year budget.", "Güncel uluslararası normal lisansüstü sabit ücret ve resmî akademik yıl bütçesi."),
        source(INSURANCE, "Purdue PUSH Insurance and Payments", "official_cost_of_living_page", ["insurance", "cost", "non_eu_eligibility"], "Current mandatory-insurance or waiver rule for West Lafayette international students; no verified 2026/27 premium on the checked page.", "West Lafayette uluslararası öğrencileri için güncel zorunlu sigorta veya muafiyet kuralı; kontrol edilen sayfada doğrulanmış 2026/27 primi yok."),
        source(HOUSING_FAQ, "Purdue University Residences FAQs", "official_housing_page", ["housing", "eligibility"], "Current University Residences eligibility language is undergraduate-facing.", "Güncel University Residences uygunluk ifadesi lisans öğrencilerine yöneliktir."),
        source(HOUSING_NEW, "Purdue New Undergraduate Housing Application", "official_housing_page", ["housing", "application"], "Current new-resident application route is explicitly for undergraduates.", "Güncel yeni konut başvuru yolu açıkça lisans öğrencileri içindir."),
        source(WELCOME, "Purdue Graduate Student Welcome Packet", "official_housing_page", ["housing", "living", "international_support"], "Graduate students are directed to off-campus housing assistance.", "Lisansüstü öğrenciler off-campus konut desteğine yönlendirilir.", access_status="pdf"),
        source(OFFCAMPUS, "Purdue Off-Campus Housing Portal", "official_housing_page", ["housing", "living"], "Official referral portal; listing prices are not treated as university-verified averages or availability guarantees.", "Resmî yönlendirme portalı; ilan fiyatları üniversitece doğrulanmış ortalama veya yer garantisi sayılmaz."),
        source(OVERVIEW, "Purdue AAE Overview", "official_department_page", ["research", "department", "industry_ecosystem"], "Current six-discipline research profile, department scale, agency activity and ITAR context.", "Güncel altı disiplinli araştırma profili, bölüm ölçeği, kamu kurumu faaliyetleri ve ITAR bağlamı."),
        source(ZUCROW, "Maurice J. Zucrow Laboratories", "official_lab_page", ["research", "labs"], "Current propulsion-complex scale and research domains.", "Güncel itki kompleksi ölçeği ve araştırma alanları."),
        source(ZUCROW_CAPABILITIES, "Zucrow Laboratories Capabilities", "official_lab_page", ["research", "labs"], "Flight-scale and flight-condition test capabilities and controlled facilities.", "Uçuş ölçeği ve uçuş koşulu test yetenekleri ile kontrollü tesisler."),
        source(ASTRODYNAMICS, "Purdue AAE Astrodynamics and Space Applications", "official_department_page", ["research", "labs", "space_fit"], "Mission design, GNC, planetary defence and named space facilities.", "Görev tasarımı, GNC, gezegen savunması ve adlandırılmış uzay tesisleri."),
        source(AUTONOMY, "Purdue AAE Autonomy and Control", "official_department_page", ["research", "labs"], "Current aircraft, spacecraft and UAS control, robotics and optimisation research.", "Güncel hava aracı, uzay aracı ve İHA kontrolü, robotik ve optimizasyon araştırmaları."),
        source(ROLLS_ROYCE, "Purdue and Rolls-Royce Partnership 2026", "official_industry_partner_page", ["industry_ecosystem", "research", "career"], "Current official confirmation of the long-term research and education partnership.", "Uzun vadeli araştırma ve eğitim ortaklığının güncel resmî doğrulaması."),
        source(RANKING, "Purdue Engineering Graduate Rankings 2026/27", "official_ranking_page", ["prestige"], "Current institutional reporting of #4 graduate Engineering and #5 aerospace; kept separate from fit.", "#4 lisansüstü Engineering ve #5 aerospace için güncel kurumsal bildirim; teknik uyumdan ayrı tutulur."),
        source(QS, "QS World University Rankings 2027 — Purdue", "reliable_third_party_ranking", ["prestige"], "Current university-wide rank; not evidence of aerospace curriculum depth.", "Güncel üniversite geneli sıra; havacılık-uzay müfredat derinliği kanıtı değildir.", confidence="medium"),
        source(REDDIT_HOUSING_1, "Reddit — incoming Purdue graduate housing search", "student_forum", ["student_sentiment"], "Small housing-only anecdotal sample.", "Küçük, yalnızca konutla ilgili anekdotsal örneklem.", confidence="low"),
        source(REDDIT_HOUSING_2, "Reddit — Purdue graduate housing options", "student_forum", ["student_sentiment"], "Small housing-only anecdotal sample.", "Küçük, yalnızca konutla ilgili anekdotsal örneklem.", confidence="low"),
        source(REDDIT_HOUSING_3, "Reddit — Purdue graduate housing pointers", "student_forum", ["student_sentiment"], "Small housing-only perceptions of location, affordability and safety.", "Konum, karşılanabilirlik ve güvenlik algılarına ilişkin küçük konut örneklemi.", confidence="low"),
    ]

    row["source_profile"] = {
        "primary_url": PROGRAM,
        "secondary_urls": [item["url"] for item in sources[1:]],
        "last_verified": TODAY,
        "field_confidence": {"program_basic_info": "high", "program": "high", "language": "unknown", "admission": "high", "non_eu_eligibility": "high", "tuition": "high", "scholarship": "high", "deadline": "high", "curriculum": "high", "research": "high", "industry_ecosystem": "high", "housing": "high", "living": "high", "insurance_cost": "unknown", "sentiment": "low", "prestige": "high"},
        "source_reliability": "high",
        "verification_status": "partially_verified",
        "needs_verification": True,
        "verification_notes": bi("Every core decision field except explicit teaching language is supported by current official sources. The current insurance obligation is verified, but the 2026/27 premium remains unknown. Private-market rent and complete-program cost are deliberately not invented.", "Açık öğretim dili dışındaki tüm temel karar alanları güncel resmî kaynaklarla desteklenir. Güncel sigorta zorunluluğu doğrulanmıştır ancak 2026/27 primi bilinmemektedir. Özel piyasa kirası ve tam program maliyeti bilerek uydurulmamıştır."),
        "source_log": sources,
    }

    row["decision_summary"] = {
        "best_for": [bi("Students seeking either a structured 10-course non-thesis MS or a thesis route across aerodynamics, space, control, propulsion, structures and systems.", "Aerodinamik, uzay, kontrol, itki, yapılar ve sistemlerde yapılandırılmış 10 derslik tezsiz MS veya tezli yol arayan öğrenciler."), bi("Applicants targeting propulsion, hypersonics, astrodynamics, spacecraft GNC or hands-on experimental infrastructure.", "İtki, hipersonik, astrodinamik, uzay aracı GNC veya uygulamalı deney altyapısını hedefleyen adaylar.")],
        "not_ideal_for": [bi("Applicants who require guaranteed admission funding or automatic research placement.", "Garantili kabul finansmanı veya otomatik araştırma yerleştirmesi gereken adaylar."), bi("International students who need university-owned graduate housing or unrestricted access to every defence/ITAR project.", "Üniversiteye ait lisansüstü yurt veya her savunma/ITAR projesine sınırsız erişim gereken uluslararası öğrenciler.")],
        "main_strengths": [bi("Two clearly defined 30-credit MS routes and six technical focus areas.", "Açıkça tanımlanmış iki 30 kredilik MS yolu ve altı teknik odak alanı."), bi("Zucrow provides unusually large, flight-relevant propulsion infrastructure.", "Zucrow sıra dışı büyüklükte, uçuşla ilgili itki altyapısı sunar."), bi("Named astrodynamics and spacecraft facilities include mission operations, clean-room hardware, optical GNC and a ground station.", "Adlandırılmış astrodinamik ve uzay aracı tesisleri görev operasyonu, temiz oda donanımı, optik GNC ve yer istasyonunu içerir."), bi("A current, officially confirmed Rolls-Royce partnership links research, facilities and experiential education.", "Güncel ve resmî olarak doğrulanmış Rolls-Royce ortaklığı araştırma, tesis ve deneyimsel eğitimi bağlar.")],
        "main_risks": [bi("Admission does not guarantee funding; non-thesis MS has the lowest published TA preference among the listed degree groups.", "Kabul finansmanı garanti etmez; tezsiz MS, listelenen derece grupları arasında yayımlanan en düşük TA önceliğine sahiptir."), bi("The current official international academic-year budget is $49,798, while mandatory insurance has no verified 2026/27 premium in this record.", "Güncel resmî uluslararası akademik yıl bütçesi 49.798 $'dır; zorunlu sigortanın bu kayıtta doğrulanmış 2026/27 primi yoktur."), bi("Graduate students are directed to private/off-campus housing; no general university-residence route or rent guarantee was verified.", "Lisansüstü öğrenciler özel/off-campus konuta yönlendirilir; genel üniversite yurdu yolu veya kira garantisi doğrulanmamıştır."), bi("GRE is required unless a narrow AAE waiver applies.", "Dar kapsamlı AAE muafiyeti yoksa GRE zorunludur."), bi("ITAR-controlled research can restrict some projects for international students.", "ITAR kontrollü araştırma bazı projeleri uluslararası öğrenciler için kısıtlayabilir."), bi("Official pages checked do not explicitly state the on-campus MSAA teaching language.", "Kontrol edilen resmî sayfalar kampüsteki MSAA öğretim dilini açıkça belirtmez.")],
        "decision_summary": bi("One of the strongest verified technical fits in the US dataset for propulsion and space-flight research, with a valuable thesis option. The trade-off is substantial self-funding risk, private-market housing dependence, competitive research access and project-specific export-control constraints.", "İtki ve uzay uçuşu araştırması için ABD veri kümesindeki en güçlü doğrulanmış teknik uyumlardan biridir ve değerli bir tez seçeneği sunar. Karşılığında önemli öz finansman riski, özel konut piyasasına bağımlılık, rekabetçi araştırma erişimi ve projeye özgü ihracat kontrolü kısıtları vardır."),
        "pros": [],
        "cons": [],
        "verdict": bi("Exceptional verified technical depth; funding, housing and international project access require conservative planning.", "Olağanüstü doğrulanmış teknik derinlik; finansman, konut ve uluslararası proje erişimi temkinli planlama gerektirir."),
    }

    row["scoring_inputs"] = {"academic_prestige": None, "research_output": None, "industry_links": None, "affordability": None, "admission_chance": None, "living_quality": None, "hard_flags": ["teaching_language_unverified", "gre_required_with_limited_waivers", "funding_not_guaranteed", "graduate_housing_not_offered_as_general_residence", "health_insurance_premium_unverified", "itar_access_constraints_possible", "research_access_not_automatic"]}
    row["data_quality"] = {"status": "partial", "checked_official_source_count": 19, "verified_fields": ["program", "admission", "non_eu_eligibility", "tuition", "scholarship", "deadline", "curriculum", "research", "industry_ecosystem", "housing", "living", "insurance_requirement", "prestige"], "unverified_critical_fields": ["language"], "known_semantic_gaps": ["explicit_teaching_language", "2026_27_health_insurance_premium", "private_market_rent", "complete_program_cost"], "has_checked_source_log": True, "audited_at": TODAY}
    row["quality_control"] = {"checked_at": TODAY, "qc_status": "needs_revision", "remaining_verification_tasks": [bi("Find a current official source explicitly stating the on-campus MSAA teaching language; do not infer it from English-test requirements.", "Kampüsteki MSAA öğretim dilini açıkça belirten güncel resmî kaynak bulun; İngilizce sınav şartlarından çıkarım yapmayın."), bi("Add the 2026/27 international student health-insurance premium only if Purdue publishes an accessible official rate.", "2026/27 uluslararası öğrenci sağlık sigortası primini yalnızca Purdue erişilebilir resmî fiyat yayımlarsa ekleyin.")], "qc_notes": bi("All discoverable decision fields are source-backed. The record remains partial because teaching language is not explicit; insurance cost is a documented noncritical cost gap.", "Bulunabilen tüm karar alanları kaynaklıdır. Öğretim dili açık olmadığı için kayıt partial kalır; sigorta maliyeti belgelenmiş kritik olmayan bir maliyet boşluğudur."), "failed_canary_tests": ["teaching_language_not_explicitly_verified"]}

    DATA_PATH.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"id": row["id"], "status": row["data_quality"]["status"], "source_count": len(sources), "checked_official_source_count": row["data_quality"]["checked_official_source_count"], "unverified_critical_fields": row["data_quality"]["unverified_critical_fields"]}, indent=2))


if __name__ == "__main__":
    main()
