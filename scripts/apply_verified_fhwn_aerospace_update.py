"""Replace FHWN Aerospace's legacy estimates with checked official evidence."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from apply_verified_polimi_aero_update import bi, source


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data_base" / "austria.json"
CHECKED = "2026-07-14"


def main() -> None:
    original = PATH.read_text(encoding="utf-8")
    document: dict[str, Any] = json.loads(original)
    row = next(item for item in document["programs"] if item.get("id") == "austria_fhwn_msc_aerospace")

    programme_url = "https://www.fhwn.ac.at/en/studyprogramme/master-aerospace-engineering"
    costs_url = "https://www.fhwn.ac.at/en/information-for/prospective-students/costs"
    housing_url = "https://www.fhwn.ac.at/en/information-for/prospective-students/accommodation"
    mobility_url = "https://www.fhwn.ac.at/en/international/outgoings/semester-abroad"
    scholarships_url = "https://oead.at/en/study-research-teaching/overview-grants-and-scholarships"
    research_url = "https://www.fhwn.ac.at/en/news/neue-studiengangsleitung-fuer-aerospace-engineering"

    row.update({
        "program_name": "Aerospace Engineering",
        "program_native_name": "Aerospace Engineering",
        "program_degree": "Master of Science in Engineering (MSc)",
        "degree_level": "Master",
        "degree_class": "MSc",
        "duration_years": 2,
        "ects": 120,
        "teaching_language": ["English"],
        "program_url": programme_url,
        "department": "FHWN Department of Aerospace Engineering",
        "campus": "Campus 1, Wiener Neustadt",
        "program_status": "active",
        "relevance_status": "strong",
    })
    row["eligibility_profile"] = {
        "eligible_for_non_eu": True,
        "required_previous_degree": bi("A relevant engineering degree is required. The programme specifically requires at least 30 ECTS in core engineering topics such as mathematics, mechanics, thermo- and fluid dynamics.", "İlgili bir mühendislik diploması gerekir. Program özellikle matematik, mekanik, termo- ve akışkanlar dinamiği gibi temel mühendislik konularında en az 30 AKTS ister."),
        "accepted_backgrounds": ["Aerospace engineering", "Applied engineering", "Relevant engineering degree with at least 30 ECTS in core engineering topics"],
        "minimum_gpa": None,
        "admission_mode": "online application followed by an English interview online or on campus; written feedback within two weeks after the interview",
        "admission_risk": "medium",
        "required_documents": [bi("Proof of eligibility, for example Bachelor's degree certificate; it may be submitted later", "Uygunluk kanıtı, örneğin lisans diploması; daha sonra sunulabilir."), bi("English-language proof unless the relevant degree was entirely taught in English", "İlgili diploma tamamen İngilizce okutulmadıysa İngilizce yeterlik belgesi")],
        "verification_notes": bi("The official programme page does not publish a universal GPA cut-off. It does publish the engineering-ECTS threshold, English proof routes and interview process.", "Resmî program sayfası evrensel bir GPA eşiği yayımlamaz. Buna karşılık mühendislik-AKTS eşiğini, İngilizce kanıt yollarını ve mülakat sürecini yayımlar."),
    }
    row["language_profile"] = {
        "teaching_language": ["English"],
        "english_required": True,
        "english_level_required": "IELTS Academic 7.0, TOEFL iBT 95, Cambridge C1 Advanced, or Duolingo English Test 130; an eligible prior degree taught entirely in English is also accepted.",
        "accepted_english_tests": ["IELTS Academic", "TOEFL iBT", "Cambridge C1 Advanced", "Duolingo English Test"],
        "english_exemptions": ["Relevant prior academic degree taught entirely in English"],
        "german_required": False,
        "language_risk": "low",
        "verification_notes": bi("The degree is taught entirely in English. The published proof threshold is C1-level in practice; an English page or campus location is not used as a substitute for this requirement.", "Derece tamamen İngilizce okutulur. Yayımlanan kanıt eşiği uygulamada C1 düzeyindedir; İngilizce bir sayfa veya kampüs konumu bu koşulun yerine geçirilmez."),
    }
    row["cost_profile"] = {
        "academic_year": "2026/2027",
        "tuition_eur_per_year_min": 1700,
        "tuition_eur_per_year_max": 1700,
        "tuition_eur_per_year_estimated": 1700,
        "tuition_basis": "standard_third_country_fee_unless_exempt",
        "non_eu_flat_fee": 1700,
        "student_contribution_eur": 52.4,
        "application_fee_eur": None,
        "document_verification_deposit_eur": 250,
        "total_academic_cost_eur_per_year_estimated": 1752.4,
        "payment_installments": "EUR 850 tuition plus EUR 26.20 Austrian Student Union (ÖH) fee each semester; a one-time EUR 250 document-verification deposit is listed for third-country students.",
        "cost_notes": bi("For 2026/27, FHWN publishes EUR 850 tuition per semester for third-country students plus EUR 26.20 ÖH each semester. This is EUR 1,700 tuition plus EUR 52.40 ÖH for a standard year. The page also lists a one-time EUR 250 document-verification deposit; it is kept separate from the annual tuition figure. EU/EEA/Swiss tuition is EUR 363.36 per semester plus ÖH.", "FHWN, 2026/27 için üçüncü ülke öğrencilerine dönem başına 850 EUR öğrenim ücreti ve 26,20 EUR ÖH yayımlar. Bu, standart bir yılda 1.700 EUR öğrenim ücreti artı 52,40 EUR ÖH demektir. Sayfa ayrıca tek seferlik 250 EUR belge doğrulama depozitosu listeler; bu tutar yıllık öğrenim ücreti hesabından ayrı tutulur. AB/AEA/İsviçre ücreti dönem başına 363,36 EUR artı ÖH'dir."),
        "verification_notes": bi("The displayed annual tuition is the current standard third-country rate, not a claim that every applicant lacks a statutory exemption.", "Gösterilen yıllık öğrenim ücreti güncel standart üçüncü ülke tarifesidir; her adayın yasal bir muafiyetten yararlanamayacağı iddiası değildir."),
    }
    row["scholarship_profile"] = {
        "regional_scholarship_available": True,
        "regional_scholarship_name": "Erasmus+ mobility grant for an FHWN exchange semester",
        "merit_scholarships": [bi("FHWN lists Aerospace Engineering in its third-semester mobility window and says selected Erasmus+ exchange students receive EUR 470-520 per month while paying their normal FHWN tuition. This is mobility funding after enrolment, not a tuition scholarship for every incoming applicant.", "FHWN, Aerospace Engineering'i üçüncü yarıyıl hareketlilik penceresinde listeler ve seçilen Erasmus+ değişim öğrencilerinin normal FHWN ücretlerini öderken ayda 470-520 EUR alacağını söyler. Bu, kayıt sonrasında hareketlilik finansmanıdır; her yeni aday için öğrenim ücreti bursu değildir.")],
        "tuition_waivers": [],
        "housing_support": None,
        "cash_grant_possible": True,
        "non_eu_eligible": None,
        "income_based": None,
        "scholarship_deadline": None,
        "scholarship_application_url": mobility_url,
        "funding_competitiveness": "high",
        "funding_notes": bi("FHWN's costs page states that students may be entitled to grants, support and scholarships under conditions and refers them to the Austrian Study Grant Authority. OeAD's official overview directs international students to grants.at, where eligibility depends on the particular award and nationality. No universal pre-admission scholarship or exact deadline is claimed.", "FHWN'nin maliyet sayfası, öğrencilerin koşullara bağlı olarak hibe, destek ve burslara hak kazanabileceğini belirtip Avusturya Öğrenim Desteği Kurumuna yönlendirir. OeAD'nin resmî özeti, uluslararası öğrencileri uygunluğun burs ve uyruğa göre değiştiği grants.at'e yönlendirir. Evrensel bir kabul öncesi burs veya kesin son tarih ileri sürülmez."),
        "verification_notes": bi("Funding is presented with its actual scope. Programme-specific tuition support and individual third-country eligibility remain unknown until a named call is checked.", "Finansman gerçek kapsamıyla sunulur. Programa özgü öğrenim ücreti desteği ve bireysel üçüncü ülke uygunluğu, isimli bir çağrı kontrol edilene kadar bilinmiyor kalır."),
    }
    row["living_profile"] = {
        "city_cost_level": "medium",
        "monthly_living_cost_eur_min": None,
        "monthly_living_cost_eur_max": None,
        "monthly_living_cost_eur_estimated": None,
        "average_room_rent_eur": None,
        "average_room_rent_eur_min": 310,
        "average_room_rent_eur_max": 404,
        "average_room_rent_scope_label": bi("FHWN FHI student-residence single room, monthly rent including running costs and VAT", "FHWN FHI öğrenci yurdu tek kişilik oda; aylık kira, işletme giderleri ve KDV dahil"),
        "student_housing_available": True,
        "student_housing_competitiveness": "medium",
        "housing_difficulty": "medium",
        "living_risk": "medium",
        "housing_sentiment": None,
        "housing_notes": bi("FHWN's FHI residence is a five-minute walk from Campus 1. Its official listed single-room rents are EUR 310-345 (10-15 m²), EUR 346-380 (15-19 m²), and EUR 381-404 (19+ m² with underground parking), including running costs and VAT; one month's rent is required as a deposit. This is a named residence price, not a city-wide market-rent estimate or a guarantee of a room.", "FHWN'nin FHI yurdu Campus 1'e beş dakika yürüme mesafesindedir. Resmî listelenen tek kişilik oda kiraları işletme giderleri ve KDV dahil 310-345 EUR (10-15 m²), 346-380 EUR (15-19 m²) ve 381-404 EUR'dur (19+ m², kapalı otoparklı); bir aylık kira depozito istenir. Bu, isimli yurdun fiyatıdır; şehir geneli piyasa kira tahmini veya oda garantisi değildir."),
        "verification_notes": bi("No official all-in monthly living budget was found, so the card shows only the checked residence rent range and does not turn it into a total cost estimate.", "Resmî, tüm kalemleri içeren aylık yaşam bütçesi bulunmadığından kart yalnızca doğrulanmış yurt kira aralığını gösterir; bunu toplam maliyet tahminine dönüştürmez."),
    }
    row["curriculum_profile"] = {
        "tracks": ["aeronautics", "space_systems"],
        "specializations": ["computational_fluid_dynamics", "aerothermodynamics", "aircraft_design", "aircraft_systems", "autonomous_uav", "space_propulsion", "space_mission_analysis", "flight_control", "satellite_technologies", "space_applications"],
        "mandatory_courses": ["Advanced Mathematics, Statistics & Optimisation", "Advanced Finite Element Computation", "Physics of Flight", "Computational Fluid Dynamics", "Aerothermodynamics 1 and 2", "Satellite Technologies", "Aircraft Design", "Aircraft Systems & Technologies", "Autonomy & Unmanned Aerial Vehicles", "Space Propulsion", "Space Mission Analysis and Design", "Dynamics of Flight & Flight Control", "Spacecraft Environment & Interactions"],
        "elective_courses": [],
        "thesis_required": True,
        "internship_required": False,
        "lab_courses": ["Advanced Mathematics, Statistics & Optimisation practical/laboratory sessions", "Advanced Finite Element Computation practical/laboratory sessions", "Aircraft Design practical/laboratory sessions", "Space Mission Analysis and Design practical/laboratory sessions"],
        "project_based_courses": ["Junior Team Project", "Senior Team Project"],
        "curriculum_url": programme_url,
        "study_plan_url": programme_url,
        "curriculum_structure": bi("This is a technically explicit four-semester curriculum rather than a prestige proxy. The early spine is FEA, flight physics and CFD; the second and third semesters add aircraft design/systems, UAV autonomy, satellite technologies, space propulsion, space mission analysis, flight control and spacecraft environment. The final semester is a 27-ECTS Master's thesis plus a 3-ECTS thesis seminar.", "Bu, prestij vekili değil teknik olarak açık dört yarıyıllık bir müfredattır. İlk omurga FEA, uçuş fiziği ve HAD'dir; ikinci ve üçüncü yarıyıllar uçak tasarımı/sistemleri, İHA otonomisi, uydu teknolojileri, uzay itkisi, uzay görevi analizi, uçuş kontrolü ve uzay aracı ortamını ekler. Son yarıyıl 27 AKTS yüksek lisans tezi ve 3 AKTS tez semineridir."),
        "verification_notes": bi("Course titles and ECTS are transcribed from the current official programme page; no unlisted lab, internship or specialisation is inferred.", "Ders başlıkları ve AKTS'ler güncel resmî program sayfasından aktarılmıştır; listelenmeyen laboratuvar, staj veya uzmanlaşma çıkarımı yapılmaz."),
    }
    row["category_profile"] = {
        "primary_categories": ["aeronautics", "space_systems"],
        "secondary_categories": ["computational_fluid_dynamics", "aerothermodynamics", "aircraft_design", "aircraft_systems", "uav", "space_propulsion", "space_mission_analysis", "flight_control", "satellite_technologies", "spacecraft_environment"],
        "normalized_tags": ["aerospace_engineering", "aircraft_design", "cfd", "finite_element_analysis", "propulsion", "spacecraft_systems", "space_mission_design", "satellite_systems", "gnc", "uav"],
    }
    row["research_profile"] = {
        "department_research_areas": ["satellite systems", "space instrumentation", "aircraft conceptual design", "aeronautics", "high-performance computing"],
        "labs": ["FHWN Aerospace Engineering research facilities"],
        "research_centers": ["FHWN Aerospace Engineering", "FOTEC research company (institutional research connection)"],
        "space_or_aerospace_projects": ["CLIMB research satellite", "TROGON autonomous transport drone"],
        "student_teams": [],
        "satellite_or_flight_projects": ["CLIMB research satellite", "TROGON autonomous transport drone"],
        "research_strength_summary": bi("FHWN publishes student participation in international projects, high-performance computing and its research satellite CLIMB. Its 2026 programme-lead announcement says students working on satellite systems and space components engage directly with current research. These are concrete applied research signals, not a claim of a large research-university lab portfolio.", "FHWN, uluslararası projelere öğrenci katılımını, yüksek başarımlı hesaplamayı ve CLIMB araştırma uydusunu yayımlar. 2026 program yöneticisi duyurusu, uydu sistemleri ve uzay bileşenleri üzerinde çalışan öğrencilerin güncel araştırmayla doğrudan ilgilendiğini söyler. Bunlar büyük araştırma üniversitesi laboratuvar portföyü iddiası değil, somut uygulamalı araştırma sinyalleridir."),
        "research_strength_score": None,
        "research_sources": [programme_url, research_url],
    }
    row["industry_ecosystem_profile"] = {
        "nearby_companies": [],
        "confirmed_partners": [],
        "research_institutes": ["FOTEC research company (FHWN institutional research connection)"],
        "internship_possibility": None,
        "thesis_with_industry_possibility": None,
        "career_relevance": "strong",
        "ecosystem_strength_score": None,
        "ecosystem_notes": bi("The programme page lists alumni employment examples including aerospace and engineering companies, but alumni destinations are not stored as partnerships or placement guarantees. No programme-specific company partnership, internship guarantee or thesis guarantee is claimed without a separate confirmation.", "Program sayfası havacılık/uzay ve mühendislik şirketlerinde mezun istihdamı örnekleri verir; ancak mezun destinasyonları ortaklık veya yerleştirme garantisi olarak saklanmaz. Ayrı bir onay olmadan programa özgü şirket ortaklığı, staj garantisi veya tez garantisi ileri sürülmez."),
    }
    row["application_timeline_profile"] = {
        "academic_year": "2026/2027 published intake",
        "intake_terms": ["September 2026"],
        "application_rounds": ["EU/EEA/Swiss: deadline 15 June 2026", "Third-country: deadline 31 March 2026"],
        "non_eu_deadline": "2026-03-31",
        "eu_deadline": "2026-06-15",
        "application_deadline": "2026-03-31 for third-country applicants; 2026-06-15 for EU/EEA/Swiss applicants",
        "scholarship_deadline": None,
        "timeline_risk": "high",
        "deadline_notes": bi("These are the official 2026/27 dates displayed on the programme page and both had passed when the record was checked on 14 July 2026. They must not be silently reused as 2027 dates; a future applicant should monitor the official programme page and allow visa time.", "Bunlar program sayfasında gösterilen resmî 2026/27 tarihleridir ve kayıt 14 Temmuz 2026'da kontrol edildiğinde ikisi de geçmişti. 2027 tarihleri olarak sessizce yeniden kullanılmamalıdır; gelecek aday resmî program sayfasını izlemeli ve vize süresi bırakmalıdır."),
    }
    row["student_sentiment_profile"] = {
        "student_satisfaction_score": None,
        "sentiment_confidence": "unknown",
        "sample_size_estimate": None,
        "date_range": "",
        "teaching_quality_sentiment": None,
        "workload_sentiment": None,
        "administration_sentiment": None,
        "housing_sentiment": None,
        "city_life_sentiment": None,
        "international_student_support_sentiment": None,
        "career_support_sentiment": None,
        "student_sentiment_sources": [],
        "student_sentiment_summary": bi("No sufficiently documented, independent student-sentiment sample was retained. No satisfaction score is displayed.", "Yeterince belgelenmiş bağımsız öğrenci görüşü örneklemi tutulmadı. Memnuniyet puanı gösterilmez."),
        "verification_notes": bi("Student sentiment is intentionally not fabricated from promotional copy or unverified snippets.", "Öğrenci görüşleri tanıtım metninden veya doğrulanmamış parçalardan kasıtlı olarak üretilmez."),
    }
    row["decision_summary"] = {
        "main_strengths": [
            bi("One of the clearest applied aerospace curricula in the data: it pairs CFD/FEA and flight physics with aircraft design, satellite technologies, space propulsion, mission analysis, flight control and spacecraft environment.", "Veri kümesindeki en net uygulamalı havacılık/uzay müfredatlarından biridir: HAD/FEA ve uçuş fiziğini uçak tasarımı, uydu teknolojileri, uzay itkisi, görev analizi, uçuş kontrolü ve uzay aracı ortamıyla birleştirir."),
            bi("The card exposes a useful, non-obvious cost signal: current official FHWN residence rooms are EUR 310-404/month including running costs and VAT, rather than an unsourced city estimate.", "Kart yararlı ve kolay bulunmayan bir maliyet sinyalini açıklar: güncel resmî FHWN yurt odaları, kaynaksız şehir tahmini yerine işletme giderleri ve KDV dahil ayda 310-404 EUR'dur."),
        ],
        "main_risks": [
            bi("The English requirement is genuinely demanding (IELTS 7.0 / TOEFL 95 / C1 Advanced / Duolingo 130 unless a relevant degree was entirely English-taught), and admission includes an English interview.", "İngilizce koşulu gerçekten yüksektir (ilgili diploma tamamen İngilizce değilse IELTS 7.0 / TOEFL 95 / C1 Advanced / Duolingo 130) ve kabul İngilizce mülakat içerir."),
            bi("For a standard non-exempt third-country student, the published academic charge is EUR 1,700 tuition plus EUR 52.40 ÖH per year, plus a one-time EUR 250 document-verification deposit. The verified Erasmus funding is for a later exchange semester, not an entry scholarship.", "Standart, muaf olmayan üçüncü ülke öğrencisi için yayımlanan akademik tutar yıllık 1.700 EUR öğrenim ücreti artı 52,40 EUR ÖH ve tek seferlik 250 EUR belge doğrulama depozitosudur. Doğrulanan Erasmus finansmanı giriş bursu değil, sonraki değişim yarıyılı içindir."),
            bi("The published 2026 deadlines had already passed at verification. Do not assume the same dates for a future cycle.", "Yayımlanan 2026 son tarihleri doğrulama sırasında geçmişti. Gelecek döngü için aynı tarihleri varsaymayın."),
        ],
        "best_for": [bi("Applicants who want an English-taught, applied master's with visible aerospace and space course depth, especially CFD/FEA, aircraft design, satellite technologies, mission analysis or flight control.", "İngilizce okutulan, uygulamalı ve görünür havacılık/uzay ders derinliği olan; özellikle HAD/FEA, uçak tasarımı, uydu teknolojileri, görev analizi veya uçuş kontrolünü isteyen adaylar.")],
        "not_ideal_for": [bi("Applicants needing a guaranteed pre-enrolment scholarship, an English score below the published threshold, or a research-intensive PhD-style environment inferred solely from company names.", "Kayıt öncesi garantili burs, yayımlanan eşiğin altında İngilizce puanı veya yalnızca şirket adlarından çıkarılmış araştırma yoğun PhD tarzı ortam bekleyen adaylar.")],
    }
    row["financials"] = {"tuition_fee_per_year": None, "semester_fee": None, "application_fee": None}
    row["scholarships_info"] = []
    row["admission"] = {"requirements": {"minimum_gpa": None, "minimum_gpa_notes": "unknown", "required_ects": 30, "language_requirements": "See language_profile for the published English proof routes."}}
    row["source_profile"] = {
        "official_program_page": programme_url,
        "official_admission_page": programme_url,
        "official_curriculum_page": programme_url,
        "official_tuition_page": costs_url,
        "official_scholarship_page": mobility_url,
        "official_housing_page": housing_url,
        "official_department_page": research_url,
        "source_log": [
            source(programme_url, "FHWN Master Aerospace Engineering", "official_program_page", ["program", "language", "admission", "non_eu", "deadline", "curriculum"], "Current programme page confirms active English MSc delivery, 120 ECTS/4 semesters, the engineering-ECTS threshold, language proofs, interview, 2026 deadlines and detailed course list.", "Güncel program sayfası aktif İngilizce MSc eğitimini, 120 AKTS/dört yarıyılı, mühendislik-AKTS eşiğini, dil kanıtlarını, mülakatı, 2026 son tarihlerini ve ayrıntılı ders listesini doğrular."),
            source(costs_url, "FHWN Costs for Prospective Students", "official_tuition_page", ["tuition", "fees"], "Current costs page publishes 2026/27 EU/EEA/Swiss and third-country rates, ÖH fee, the third-country document-verification deposit and statutory-exemption caution.", "Güncel maliyet sayfası 2026/27 AB/AEA/İsviçre ve üçüncü ülke tarifelerini, ÖH ücretini, üçüncü ülke belge doğrulama depozitosunu ve yasal muafiyet uyarısını yayımlar."),
            source(housing_url, "FHWN Accommodation", "official_housing_page", ["housing", "living"], "Current FHWN accommodation page publishes the FHI residence location, room sizes, EUR 310-404 monthly rents including running costs and VAT, and one-month deposit.", "Güncel FHWN konaklama sayfası FHI yurdunun konumunu, oda boyutlarını, işletme giderleri ve KDV dahil aylık 310-404 EUR kirayı ve bir aylık depozitoyu yayımlar."),
            source(mobility_url, "FHWN Semester Abroad", "official_scholarship_page", ["scholarship", "funding"], "Current page lists Aerospace Engineering in the third-semester mobility window and says selected Erasmus+ exchange students receive EUR 470-520 per month.", "Güncel sayfa Aerospace Engineering'i üçüncü yarıyıl hareketlilik penceresinde listeler ve seçilen Erasmus+ değişim öğrencilerinin ayda 470-520 EUR aldığını söyler."),
            source(scholarships_url, "OeAD Grants and Scholarships", "official_scholarship_page", ["scholarship", "funding"], "Official Austrian agency overview explains that international students can search grants.at and that awards have programme- and origin-specific eligibility.", "Resmî Avusturya kurumu özeti, uluslararası öğrencilerin grants.at'te arama yapabileceğini ve ödüllerin programa/uyruğa özgü uygunluğu olduğunu açıklar."),
            source(research_url, "FHWN Aerospace Engineering research and teaching announcement", "official_department_page", ["research"], "FHWN's April 2026 announcement says students working on satellite systems and space components engage directly with current research; it identifies the programme head's space-instrumentation background.", "FHWN'nin Nisan 2026 duyurusu, uydu sistemleri ve uzay bileşenleri üzerinde çalışan öğrencilerin güncel araştırmayla doğrudan ilgilendiğini söyler ve program yöneticisinin uzay enstrümantasyonu geçmişini belirtir."),
        ],
        "last_verified": CHECKED,
        "needs_verification": False,
        "verification_notes": bi("All displayed critical decision facts have an accessible official source. Scholarship eligibility is intentionally scoped rather than universal, and no unverified student sentiment is shown.", "Gösterilen tüm kritik karar bilgileri erişilebilir resmî kaynağa sahiptir. Burs uygunluğu evrensel değil, kasıtlı olarak kapsamıyla sunulur; doğrulanmamış öğrenci görüşü gösterilmez."),
        "field_confidence": {"program_basic_info": "high", "language": "high", "admission": "high", "tuition": "high", "scholarship": "medium", "curriculum": "high", "research_profile": "high", "industry_ecosystem_profile": "unknown", "application_timeline_profile": "high", "living_profile": "high", "housing": "high", "deadlines": "high"},
    }
    document["last_updated"] = CHECKED
    newline = "\r\n" if "\r\n" in original else "\n"
    PATH.write_text(json.dumps(document, ensure_ascii=False, indent=2).replace("\n", newline) + newline, encoding="utf-8")
    print("Updated FHWN Aerospace Engineering with current official decision evidence.")


if __name__ == "__main__":
    main()
