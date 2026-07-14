"""Replace legacy Georgia Tech AE claims with current official evidence."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data_base" / "amerika.json"
CHECKED = "2026-07-14"


def bi(en: str, tr: str) -> dict[str, str]:
    return {"en": en, "tr": tr}


def source(
    url: str,
    title: str,
    source_type: str,
    fields: list[str],
    notes_en: str,
    notes_tr: str,
    *,
    access_status: str = "ok",
) -> dict[str, Any]:
    return {
        "url": url,
        "title": title,
        "source_type": source_type,
        "access_status": access_status,
        "last_checked": CHECKED,
        "relevant_fields": fields,
        "confidence": "high",
        "notes": bi(notes_en, notes_tr),
    }


def main() -> None:
    original = PATH.read_text(encoding="utf-8")
    rows: list[dict[str, Any]] = json.loads(original)
    row = next(item for item in rows if item.get("id") == "georgia-tech-ae")

    catalog_url = "https://catalog.gatech.edu/programs/aerospace-engineering-ms/"
    apply_url = "https://ae.gatech.edu/ae-graduate-apply"
    language_url = "https://pe.gatech.edu/degrees/aerospace-engineering"
    international_url = "https://grad.gatech.edu/admissions/international/before-you-apply"
    tuition_url = "https://bursar.gatech.edu/student/tuition/fa26/fa26_totals_page.pdf"
    living_url = "https://finaid.gatech.edu/costs/graduate-costs"
    funding_url = "https://grad.gatech.edu/paying-for-grad-school"
    lab_url = "https://www.asdl.gatech.edu/academics/master_science/"

    row.update({
        "program_name": "Master of Science in Aerospace Engineering",
        "program_native_name": "Master of Science in Aerospace Engineering",
        "program_degree": "MSAE",
        "degree_level": "Master",
        "degree_class": "Master of Science",
        "duration_years": None,
        "ects": None,
        "teaching_language": ["English"],
        "program_url": catalog_url,
        "department": "Daniel Guggenheim School of Aerospace Engineering",
        "faculty_or_school": "College of Engineering",
        "campus": "Atlanta campus",
        "program_status": "active",
        "relevance_status": "strong",
    })

    row["eligibility_profile"] = {
        "eligible_for_non_eu": True,
        "non_eu_quota": None,
        "required_previous_degree": bi(
            "Georgia Tech's international-applicant process requires applicants educated outside the United States to meet the relevant country-specific minimum qualification. The checked AE page does not state a programme-wide numerical GPA or prerequisite-credit threshold, so neither is inferred.",
            "Georgia Tech'nin uluslararası aday süreci, ABD dışında eğitim alan adayların ilgili ülkeye özgü asgari yeterliği karşılamasını ister. Kontrol edilen AE sayfası program genelinde sayısal GPA veya önkoşul kredi eşiği belirtmez; bu nedenle ikisi de çıkarılmaz.",
        ),
        "accepted_backgrounds": [],
        "required_ects": {},
        "minimum_gpa": None,
        "admission_mode": bi(
            "AE states that MS applications receive holistic review; GRE scores are optional and may be considered if submitted.",
            "AE, MS başvurularını bütüncül değerlendirdiğini; GRE puanının isteğe bağlı olduğunu ve sunulursa dikkate alınabileceğini belirtir.",
        ),
        "admission_risk": "high",
        "required_documents": [
            bi("Recommendation letters and proof of English proficiency/test scores are supplemental materials; the school deadline for those materials is four weeks after the term application deadline.", "Referans mektupları ile İngilizce yeterlik/test puanları ek belgelerdir; okulun bu belgeler için son tarihi dönem başvuru tarihinden dört hafta sonradır."),
            bi("International applicants must follow Georgia Tech's country-specific qualification guidance and provide English translations of non-English academic documents.", "Uluslararası adaylar Georgia Tech'nin ülkeye özgü yeterlik rehberini izlemeli ve İngilizce olmayan akademik belgeler için İngilizce çeviri sunmalıdır."),
        ],
        "verification_notes": bi(
            "This card deliberately does not claim a universal admission GPA, an Aerospace-specific prior-degree list, or an acceptance rate, because the checked official pages do not publish them.",
            "Kontrol edilen resmî sayfalar bunları yayımlamadığı için bu kart evrensel kabul GPA'sı, Havacılık-Mühendisliği'ne özgü önceki diploma listesi veya kabul oranı ileri sürmez.",
        ),
    }

    row["language_profile"] = {
        "teaching_language": ["English"],
        "english_required": True,
        "english_level_required": None,
        "mixed_language_warning": None,
        "language_risk": "low",
        "verification_notes": bi(
            "Georgia Tech's official MSAE information states that the language of instruction at Georgia Tech is English. Graduate Education also requires English-proficiency proof at application; use the live policy page for the currently accepted tests and exemptions.",
            "Georgia Tech'nin resmî MSAE bilgisi Georgia Tech'de eğitim dilinin İngilizce olduğunu belirtir. Graduate Education ayrıca başvuruda İngilizce yeterlik kanıtı ister; güncel kabul edilen sınavlar ve muafiyetler için canlı politika sayfası kullanılmalıdır.",
        ),
    }

    row["cost_profile"] = {
        "academic_year": "2026/2027",
        "tuition_usd_per_term_out_of_country_full_time": 16540,
        "tuition_usd_per_year": 33080,
        "mandatory_fees_usd_per_term_full_time": 758,
        "mandatory_fees_usd_per_year": 1516,
        "international_student_fee_usd_per_term": 100,
        "total_academic_cost_usd_per_year": 34596,
        "tuition_eur_per_year_min": None,
        "tuition_eur_per_year_max": None,
        "tuition_eur_per_year_estimated": None,
        "tuition_basis": "official_2026_27_out_of_country_master_full_time_two_regular_terms",
        "non_eu_flat_fee": None,
        "student_union_fee_eur": None,
        "living_cost_eur_per_month": None,
        "total_first_year_cost_eur": None,
        "scholarship_availability": "competitive_assistantships_only_no_guarantee",
        "scholarship_risk": "high",
        "verification_notes": bi(
            "For a new out-of-country Master/PhD student registered for 12+ credits, the official Fall 2026 and Spring 2027 rate charts each list USD 16,540 tuition and USD 758 mandatory student fees. This card multiplies those two identical regular-term figures for a USD 34,596 academic-year planning figure, excluding the USD 100 F/J international-student fee per term, health insurance, course fees and any summer enrollment. Rates and classifications can change.",
            "12+ kredi alan yeni out-of-country Master/PhD öğrencisi için resmî Güz 2026 ve Bahar 2027 ücret tabloları dönem başına 16.540 USD öğrenim ücreti ve 758 USD zorunlu öğrenci ücreti listeler. Bu kart, birbirine eşit iki normal dönem tutarını 34.596 USD akademik yıl planlama tutarı için çarpar; dönem başına 100 USD F/J uluslararası öğrenci ücreti, sağlık sigortası, ders ücretleri ve yaz dönemi bu tutara dahil değildir. Ücretler ve sınıflandırmalar değişebilir.",
        ),
        "source_notes": bi(
            "USD values are retained in their official currency. No EUR conversion is presented because it would require a time-sensitive exchange-rate assumption.",
            "USD tutarları resmî para biriminde tutulur. Zaman duyarlı döviz kuru varsayımı gerektireceği için EUR dönüşümü sunulmaz.",
        ),
    }

    row["scholarship_profile"] = {
        "available_types": ["Graduate Research Assistantship (GRA)", "Graduate Teaching Assistantship (GTA)"],
        "non_eu_eligible": None,
        "details": [
            bi("AE gives Fall 2027 applicants full research-assistantship consideration when the application is submitted by 1 December 2026; this is consideration, not an offer guarantee.", "AE, Güz 2027 adaylarına başvuru 1 Aralık 2026'ya kadar sunulursa araştırma asistanlığı için tam değerlendirme verir; bu değerlendirmedir, teklif garantisi değildir."),
            bi("Georgia Tech says assistantships are awarded through departments and provide a tuition waiver plus a modest stipend. Students on an eligible GRA/GTA waiver have USD 25 tuition responsibility, subject to the appointment and policy conditions.", "Georgia Tech, asistanlıkların bölümler aracılığıyla verildiğini ve öğrenim muafiyeti ile mütevazı burs sağladığını belirtir. Uygun GRA/GTA muafiyetindeki öğrencilerin öğrenim ücreti sorumluluğu, atama ve politika koşullarına tabi olarak 25 USD'dir."),
        ],
        "external_options": [],
        "regional_scholarship_available": None,
        "regional_scholarship_name": None,
        "scholarship_deadline": "2026-12-01 (Fall 2027 AE research-assistantship priority consideration)",
        "funding_notes": bi(
            "Do not budget as if an assistantship is assured. The official AE deadline only secures full consideration; funding depends on the department and an actual appointment.",
            "Asistanlık kesinmiş gibi bütçe yapmayın. Resmî AE son tarihi yalnızca tam değerlendirme sağlar; finansman bölüme ve gerçek bir atamaya bağlıdır.",
        ),
        "verification_notes": bi(
            "The record distinguishes an assistantship job/waiver from a general admission scholarship. International eligibility is not asserted because the checked public pages do not publish an AE-specific eligibility guarantee.",
            "Kayıt, asistanlık işi/muafiyetini genel kabul bursundan ayırır. Kontrol edilen kamuya açık sayfalar AE'ye özgü uygunluk garantisi yayımlamadığı için uluslararası uygunluk ileri sürülmez.",
        ),
    }

    row["living_profile"] = {
        "city_type": "large_city",
        "student_housing_available": None,
        "housing_difficulty": "unknown",
        "living_risk": "high",
        "housing_budget_usd_per_year": 11736,
        "living_cost_usd_per_year": 22612,
        "living_cost_usd_per_year_i20": None,
        "average_room_rent_usd_per_month_min": None,
        "average_room_rent_usd_per_month_max": None,
        "monthly_living_cost_eur_estimated": None,
        "average_room_rent_eur": None,
        "housing_notes": bi(
            "Georgia Tech's 2026/27 financial-aid cost of attendance uses an on-campus housing allowance of USD 11,736/year. Its out-of-country graduate non-tuition on-campus budget is USD 22,612/year: housing 11,736, food 6,310, books/supplies 800, personal expenses 2,800 and transport 966. These are planning allowances, not a rent quote or a housing guarantee.",
            "Georgia Tech'nin 2026/27 mali yardım devam maliyeti kampüs içi konaklama ödeneği olarak yılda 11.736 USD kullanır. Out-of-country lisansüstü öğrenci için öğrenim ücreti dışı kampüs içi bütçe yılda 22.612 USD'dir: konaklama 11.736, yemek 6.310, kitap/malzeme 800, kişisel giderler 2.800 ve ulaşım 966 USD. Bunlar planlama ödenekleridir; kira teklifi veya konaklama garantisi değildir.",
        ),
        "verification_notes": bi(
            "No market room-rent range is invented. The official allowance is useful for first-pass budgeting but must not be presented as a quoted available room price.",
            "Piyasa oda kira aralığı uydurulmaz. Resmî ödenek ilk bütçe planı için kullanışlıdır ancak mevcut oda fiyat teklifi olarak sunulmamalıdır.",
        ),
    }

    row["application_timeline_profile"] = {
        "academic_year": "2027 entry",
        "intake_terms": ["Spring 2027", "Summer 2027", "Fall 2027"],
        "application_rounds": [
            "Spring 2027: 1 September 2026",
            "Summer 2027: 1 December 2026 for full financial-aid consideration; final deadline 1 February 2027",
            "Fall 2027: 1 December 2026 for full financial-aid consideration; final deadline 1 March 2027",
        ],
        "non_eu_deadline": "2027-03-01 (Fall 2027 final AE deadline; funding-priority date is 2026-12-01)",
        "eu_deadline": "2027-03-01 (Fall 2027 final AE deadline; funding-priority date is 2026-12-01)",
        "application_deadline": "2027-03-01 (Fall 2027 final AE deadline)",
        "scholarship_deadline": "2026-12-01 (Fall 2027 research-assistantship full-consideration date)",
        "pre_enrolment_required": None,
        "visa_complexity": "high",
        "timeline_risk": "high",
        "deadline_notes": bi(
            "The School says recommendation letters and language-proficiency materials are due four weeks after the relevant application deadline. For funding, the December date—not the March final date—is the decision-critical target. Check the live page before applying.",
            "Okul, referans mektupları ve dil yeterlik belgelerinin ilgili başvuru tarihinden dört hafta sonra teslim edileceğini belirtir. Finansman için karar açısından kritik tarih Marttaki nihai tarih değil Aralık tarihidir. Başvuru öncesinde canlı sayfayı kontrol edin.",
        ),
    }

    row["curriculum_profile"] = {
        "tracks": ["aerodynamics_and_fluid_mechanics", "aeroelasticity_and_structural_dynamics", "flight_mechanics_and_control", "propulsion_and_combustion", "structural_mechanics_and_materials_behavior", "system_design_and_optimization"],
        "specializations": ["aerodynamics_and_fluid_mechanics", "aeroelasticity_and_structural_dynamics", "flight_mechanics_and_control", "propulsion_and_combustion", "structural_mechanics_and_materials_behavior", "system_design_and_optimization"],
        "mandatory_courses": ["AE 8002 AE Graduate Seminar", "6 semester hours of Mathematics"],
        "elective_courses": [],
        "course_language_notes": bi("The programme is taught in English. Course choice is flexible under the advisor-approved programme of study.", "Program İngilizce yürütülür. Ders seçimi, danışmanın onayladığı eğitim planı altında esnektir."),
        "thesis_required": False,
        "thesis_type": bi("Thesis option: 24 credit hours of coursework plus 9 thesis hours, including proposal, thesis and defence; non-thesis option: 33 credit hours of coursework.", "Tez seçeneği: öneri, tez ve savunma dahil 24 kredi ders + 9 kredi tez; tezsiz seçenek: 33 kredi ders."),
        "internship_required": None,
        "lab_courses": [],
        "project_based_courses": [],
        "curriculum_url": catalog_url,
        "study_plan_url": catalog_url,
        "curriculum_structure": bi(
            "This is not a one-track aerospace MSc. The official catalogue makes six technical directions visible and allows either a flexible 33-credit non-thesis route or 24 credits plus a 9-credit defended thesis. At least 24 credits in the non-thesis route (15 in the thesis route) must be 6000 level or above; the first-year graduate seminar and 6 mathematics credits are explicit requirements.",
            "Bu tek rotalı bir havacılık MSc'si değildir. Resmî katalog altı teknik yönü görünür kılar ve esnek 33 kredilik tezsiz rota veya 24 kredi + 9 kredilik savunmalı tez rotası sunar. Tezsiz rotada en az 24 kredi (tezli rotada 15 kredi) 6000 seviyesi veya üzeri olmalıdır; birinci yıl lisansüstü semineri ve 6 matematik kredisi açık gerekliliklerdir.",
        ),
        "verification_notes": bi("Only structure and specializations stated in the current catalogue are listed; a generic internship requirement is not asserted.", "Yalnızca güncel katalogda belirtilen yapı ve uzmanlıklar listelenir; genel bir staj zorunluluğu ileri sürülmez."),
    }

    row["category_profile"] = {
        "primary_categories": ["aerospace_engineering"],
        "secondary_categories": ["aerodynamics", "cfd", "aeroelasticity", "structures", "gnc", "propulsion", "combustion", "systems_engineering"],
        "normalized_tags": ["aerospace_engineering", "aerodynamics", "fluid_mechanics", "aeroelasticity", "structural_dynamics", "flight_dynamics", "guidance_navigation_control", "propulsion", "combustion", "aerospace_system_design"],
    }

    row["research_profile"] = {
        "research_focus_areas": ["aerodynamics and fluid mechanics", "aeroelasticity and structural dynamics", "flight mechanics and control", "propulsion and combustion", "structural mechanics and materials behavior", "system design and optimization"],
        "key_institutes": ["Aerospace Systems Design Laboratory (ASDL)"],
        "research_funding_level": "unknown",
        "research_risk": "low",
        "verification_notes": bi(
            "The catalogue identifies the six AE graduate specializations. ASDL's official MSAE page documents a four-term practice-oriented systems-design/research route; this is an available specialised route, not a claim that every MSAE student joins ASDL.",
            "Katalog altı AE lisansüstü uzmanlığını tanımlar. ASDL'nin resmî MSAE sayfası dört dönemli, uygulama odaklı sistem tasarımı/araştırma rotasını belgeler; bu, her MSAE öğrencisinin ASDL'ye katıldığı iddiası değil, mevcut uzmanlaşmış bir rotadır.",
        ),
    }

    row["industry_ecosystem_profile"] = {
        "local_industry_strength": "unknown",
        "key_companies": [],
        "hiring_culture": "unknown",
        "alumni_presence": "unknown",
        "industry_risk": bi("Employment and internship eligibility can depend on role-specific export-control, citizenship, clearance and employer rules. No company partnership is inferred from company presence or employer examples.", "İş ve staj uygunluğu role özgü ihracat kontrolü, vatandaşlık, güvenlik izni ve işveren kurallarına bağlı olabilir. Şirketin varlığından veya işveren örneklerinden şirket ortaklığı çıkarılmaz."),
        "verification_notes": bi("The legacy company list was removed: the checked ASDL page lists examples of graduate employers, not a verified list of university partnerships.", "Eski şirket listesi kaldırıldı: kontrol edilen ASDL sayfası, doğrulanmış üniversite ortaklıkları değil, mezun işveren örnekleri listeler."),
    }

    row["student_sentiment_profile"] = {
        "student_satisfaction_score": None,
        "workload_sentiment": "unknown",
        "teaching_quality_sentiment": "unknown",
        "administration_sentiment": "unknown",
        "housing_sentiment": "unknown",
        "city_life_sentiment": "unknown",
        "international_student_sentiment": "unknown",
        "career_support_sentiment": "unknown",
        "student_sentiment_summary": bi("No sufficiently sourced multi-source student-sentiment sample has been added.", "Yeterli kaynaklı ve çoklu-kaynak öğrenci duygu örneklemi eklenmemiştir."),
        "student_sentiment_sources": [],
        "sentiment_confidence": "unknown",
        "verification_notes": bi("Student perception is intentionally left unknown until multiple dated independent sources are reviewed under the sentiment policy.", "Öğrenci algısı, duygu politikası kapsamında tarihli çoklu bağımsız kaynak incelenene kadar bilerek bilinmeyen bırakılır."),
    }

    row["decision_summary"] = {
        "pros": [
            bi("Six explicit graduate technical directions span aerodynamics, structures/aeroelasticity, flight mechanics/control, propulsion/combustion and systems design.", "Altı açık lisansüstü teknik yön; aerodinamik, yapılar/aeroelastisite, uçuş mekaniği/kontrol, itki/yanma ve sistem tasarımını kapsar."),
            bi("Thesis and non-thesis routes are both formally defined; the structure makes research depth and flexibility visible before application.", "Tezli ve tezsiz rotaların ikisi de resmen tanımlıdır; yapı, başvuru öncesinde araştırma derinliği ile esnekliği görünür kılar."),
            bi("A December funding-priority date is explicitly published, avoiding the common mistake of treating the March final deadline as funding-safe.", "Aralık finansman öncelik tarihi açıkça yayımlanır; böylece Marttaki nihai tarihi finansman açısından güvenli sanma hatası önlenir."),
        ],
        "cons": [
            bi("For a new out-of-country student at 12+ credits, the published two-term tuition plus mandatory-fee planning total is USD 34,596 before health insurance, international-student fees, course fees, summer enrollment and living costs.", "12+ kredi alan yeni out-of-country öğrenci için yayımlanan iki dönemlik öğrenim ücreti + zorunlu ücret planlama toplamı; sağlık sigortası, uluslararası öğrenci ücretleri, ders ücretleri, yaz dönemi ve yaşam maliyetlerinden önce 34.596 USD'dir."),
            bi("Assistantships are competitive and not guaranteed; a student should not treat the priority date as funding confirmation.", "Asistanlıklar rekabetçidir ve garanti edilmez; öğrenci öncelik tarihini finansman onayı olarak görmemelidir."),
            bi("The official cost-of-attendance housing figure is a budget allowance, not a current available-room price or housing guarantee.", "Resmî devam maliyetindeki konaklama tutarı bütçe ödeneğidir; güncel mevcut oda fiyatı veya konaklama garantisi değildir."),
        ],
        "verdict": bi("A source-backed option for students who want configurable depth across major aerospace subfields and can fund the high US cost or secure a real assistantship. The information card separates published costs and funding rules from unverified career and student-experience claims.", "Büyük havacılık alt alanlarında yapılandırılabilir derinlik isteyen ve yüksek ABD maliyetini karşılayabilen ya da gerçek bir asistanlık alabilen öğrenciler için kaynak destekli bir seçenektir. Bilgi kartı yayımlanmış maliyet ve finansman kurallarını doğrulanmamış kariyer ve öğrenci deneyimi iddialarından ayırır."),
    }

    row["scoring_inputs"] = {
        "academic_prestige": 85,
        "research_output": 85,
        "industry_links": 60,
        "affordability": 20,
        "admission_chance": 50,
        "living_quality": 50,
        "interpretation_notes": bi(
            "These are transparent comparison-model inputs, not official rankings or acceptance statistics. Academic/research strength reflects the documented breadth of six graduate specializations and thesis route; industry, admission and living are deliberately conservative because the checked sources do not publish a verified partnership set, acceptance rate or room-availability rate.",
            "Bunlar resmî sıralama veya kabul istatistiği değil, şeffaf karşılaştırma modeli girdileridir. Akademik/araştırma gücü, belgelenmiş altı lisansüstü uzmanlık ve tez rotasının genişliğini yansıtır; kontrol edilen kaynaklar doğrulanmış ortaklık kümesi, kabul oranı veya oda bulunabilirlik oranı yayımlamadığı için sektör, kabul ve yaşam bileşenleri bilerek temkinlidir.",
        ),
    }

    profile = row.setdefault("source_profile", {})
    replace_urls = {catalog_url, apply_url, language_url, international_url, tuition_url, living_url, funding_url, lab_url}
    logs = [item for item in profile.get("source_log", []) if isinstance(item, dict) and item.get("url") not in replace_urls]
    logs.extend([
        source(catalog_url, "Georgia Tech Catalog: Master of Science in Aerospace Engineering", "official_program_page", ["program", "curriculum"], "Current official catalogue confirms the active MSAE, 33-credit thesis/non-thesis structures and six graduate specializations.", "Güncel resmî katalog aktif MSAE'yi, 33 kredilik tezli/tezsiz yapıları ve altı lisansüstü uzmanlığı doğrular."),
        source(apply_url, "Georgia Tech AE Graduate Apply", "official_admission_page", ["program", "admission", "deadline", "scholarship"], "Official AE page publishes 2027 term deadlines, the financial-aid priority dates, supplemental-material timing and optional GRE policy.", "Resmî AE sayfası 2027 dönem son tarihlerini, mali yardım öncelik tarihlerini, ek belge zamanlamasını ve isteğe bağlı GRE politikasını yayımlar."),
        source(language_url, "Georgia Tech Professional Education: MSAE", "official_university_policy_page", ["language"], "Official MSAE information states that Georgia Tech's language of instruction is English.", "Resmî MSAE bilgisi Georgia Tech'de eğitim dilinin İngilizce olduğunu belirtir."),
        source(international_url, "Georgia Tech Graduate Education: Before You Apply", "official_admission_page", ["admission", "non_eu", "language"], "Official international guidance requires country-specific qualification review, English proof and English translations for non-English academic documents.", "Resmî uluslararası rehber, ülkeye özgü yeterlik incelemesi, İngilizce kanıtı ve İngilizce olmayan akademik belgeler için İngilizce çeviri ister."),
        source(tuition_url, "Georgia Tech Fall 2026 Tuition and Fee Rates", "official_tuition_page", ["tuition", "fees"], "Official rate chart lists USD 16,540 out-of-country Master/PhD tuition and USD 758 mandatory student fees for 12+ credits; Spring 2027 is the same for the checked regular-term amounts.", "Resmî ücret tablosu 12+ kredi için 16.540 USD out-of-country Master/PhD öğrenim ücreti ve 758 USD zorunlu öğrenci ücreti listeler; kontrol edilen normal dönem tutarları için Bahar 2027 aynıdır.", access_status="pdf"),
        source(living_url, "Georgia Tech Financial Aid: Graduate Costs 2026/27", "official_cost_of_living_page", ["housing", "living"], "Official out-of-country graduate budget lists USD 11,736 on-campus housing allowance and USD 22,612 total non-tuition on-campus cost of attendance.", "Resmî out-of-country lisansüstü bütçesi 11.736 USD kampüs içi konaklama ödeneği ve 22.612 USD toplam öğrenim ücreti dışı kampüs içi devam maliyeti listeler."),
        source(funding_url, "Georgia Tech Graduate Education: Paying for Grad School", "official_scholarship_page", ["scholarship", "funding"], "Official funding page says department-awarded assistantships provide a tuition waiver and modest stipend, but are not an admission guarantee.", "Resmî finansman sayfası, bölüm tarafından verilen asistanlıkların öğrenim muafiyeti ve mütevazı burs sağladığını; ancak kabul garantisi olmadığını belirtir."),
        source(lab_url, "Georgia Tech ASDL Master of Science Program", "official_lab_page", ["research", "curriculum"], "Official ASDL page documents a four-term practice-oriented MSAE systems-design/research route and does not establish company partnerships for the general programme.", "Resmî ASDL sayfası dört dönemli, uygulama odaklı MSAE sistem tasarımı/araştırma rotasını belgeler ve genel program için şirket ortaklığı oluşturmaz."),
    ])
    profile.update({
        "primary_url": catalog_url,
        "official_program_page": catalog_url,
        "official_admission_page": apply_url,
        "official_curriculum_page": catalog_url,
        "official_tuition_page": tuition_url,
        "official_scholarship_page": funding_url,
        "official_department_page": None,
        "official_housing_page": living_url,
        "source_log": logs,
        "last_verified": CHECKED,
        "needs_verification": False,
        "verification_status": "verified",
        "verification_notes": bi("Current official records support programme, language, admission, tuition, assistantship funding, deadlines, curriculum and a cost-of-attendance budget. Unpublished acceptance, market-rent, partnership and student-sentiment claims are intentionally left unknown.", "Güncel resmî kayıtlar program, dil, kabul, öğrenim ücreti, asistanlık finansmanı, son tarihler, müfredat ve devam maliyeti bütçesini destekler. Yayımlanmamış kabul, piyasa kirası, ortaklık ve öğrenci duygu iddiaları bilerek bilinmeyen bırakılır."),
    })
    profile["field_confidence"] = {
        "program_basic_info": "high",
        "language": "high",
        "admission": "high",
        "tuition": "high",
        "scholarship": "high",
        "curriculum": "high",
        "deadlines": "high",
        "living": "high",
        "housing": "high",
        "research": "high",
        "industry": "unknown",
        "sentiment": "unknown",
    }

    newline = "\r\n" if "\r\n" in original else "\n"
    PATH.write_text(json.dumps(rows, ensure_ascii=False, indent=2).replace("\n", newline) + newline, encoding="utf-8")
    print("Updated Georgia Tech MSAE with current official decision evidence.")


if __name__ == "__main__":
    main()
