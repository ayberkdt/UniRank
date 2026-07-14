"""Fill TU Graz Space Sciences with source-checked student decision data."""

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
    rows: list[dict[str, Any]] = document["programs"]
    row = next(item for item in rows if item.get("id") == "austria_tugraz_msc_space_sciences")

    programme_url = "https://www.tugraz.at/en/studying-and-teaching/degree-and-certificate-programmes/masters-degree-programmes/space-sciences-and-earth-from-space"
    admission_url = "https://www.tugraz.at/en/studying-and-teaching/studying-at-tu-graz/prospective-students/registration-and-admission/masters-programme-without-admission-procedure-with-an-international-degree"
    language_url = "https://www.tugraz.at/en/studying-and-teaching/studying-at-tu-graz/prospective-students/registration-and-admission/admission-of-international-degree-programme-applicants/proof-of-german-language-competence/"
    tuition_url = "https://www.tugraz.at/en/studying-and-teaching/studying-at-tu-graz/prospective-students/financial-matters/tuition-fees-and-the-austrian-student-union-fee"
    scholarship_url = "https://www.tugraz.at/en/studying-and-teaching/studying-at-tu-graz/prospective-students/financial-matters/scholarships-for-students/application-masters-scholarships"
    scholarship_overview_url = "https://www.tugraz.at/en/studying-and-teaching/studying-at-tu-graz/prospective-students/financial-matters/scholarships-for-students/scholarships-tu-graz-high-potentials"
    living_url = "https://www.tugraz.at/en/studying-and-teaching/studying-internationally/international-students/faq-for-international-students"
    rent_url = "https://www.tugraz.at/en/news/blog/detail/article/which-austrian-technical-university-suits-you-best"
    factsheet_url = "https://www.tugraz.at/fileadmin/user_upload/tugrazInternal/Studium/International_studieren_und_lehren/Mobilitaetsprogramme/OverSEAs_Factsheet.pdf"

    row.update({
        "program_name": "Space Sciences and Earth from Space",
        "program_native_name": "Space Sciences and Earth from Space",
        "program_degree": "Diplom-Ingenieur (equivalent to MSc)",
        "degree_level": "Master",
        "degree_class": "Diplom-Ingenieur / MSc-equivalent",
        "duration_years": 2,
        "ects": 120,
        "teaching_language": ["German"],
        "program_url": programme_url,
        "department": "TU Graz / NAWI Graz Space Sciences",
        "campus": "Graz",
        "program_status": "active",
        "relevance_status": "strong",
    })
    row.setdefault("eligibility_profile", {}).update({
        "eligible_for_non_eu": True,
        "required_previous_degree": bi("Completed relevant Bachelor's degree. TU Graz lists Physics, Geodesy, Electrical Engineering, Information and Computer Engineering, and Electrical Engineering and Audio Engineering as direct-entry degrees without conditions.", "Tamamlanmış ilgili lisans diploması. TU Graz, koşulsuz doğrudan giriş için Fizik, Jeodezi, Elektrik Mühendisliği, Bilgi ve Bilgisayar Mühendisliği ile Elektrik Mühendisliği ve Ses Mühendisliği derecelerini listeler."),
        "accepted_backgrounds": ["Physics", "Geodesy", "Electrical Engineering", "Information and Computer Engineering", "Electrical Engineering and Audio Engineering", "Other national or international Bachelor/Master degree subject to curriculum assessment"],
        "minimum_gpa": None,
        "admission_mode": "relevant-degree check; other domestic/international degrees assessed against the curriculum",
        "admission_risk": "high",
        "required_documents": [bi("Complete international Master's application and required certified/translated academic documents", "Eksiksiz uluslararası yüksek lisans başvurusu ve gerekli onaylı/tercüme edilmiş akademik belgeler"), bi("German-language proof for regular enrolment", "Düzenli kayıt için Almanca yeterlik belgesi")],
        "verification_notes": bi("The programme page lists direct-entry TU Graz degrees and directs other domestic/international degree holders to exact curriculum requirements. The international Master's page makes clear that complete applications and both academic and language requirements are needed; it does not publish a universal GPA cut-off.", "Program sayfası doğrudan giriş yapan TU Graz derecelerini listeler ve diğer yerli/uluslararası diploma sahiplerini kesin müfredat koşullarına yönlendirir. Uluslararası yüksek lisans sayfası eksiksiz başvuru ile akademik ve dil koşullarının birlikte gerektiğini açıklar; evrensel GPA eşiği yayımlamaz."),
    })
    row.setdefault("language_profile", {}).update({
        "teaching_language": ["German"],
        "english_required": False,
        "german_required": True,
        "german_level_required": "C1 CEFR for regular enrolment. Examples include ÖSD, Goethe, DSH, DSD, telc German C1 and TestDaF at least TDN4 in all four sections; certificate must be no more than two years old.",
        "language_risk": "high",
        "additional_language_notes": bi("Applicants may obtain a conditional non-degree admission with at least German A2 while completing the University Preparation Programme, but they cannot start as regular students in this German-taught Master's until C1 is documented.", "Adaylar Üniversite Hazırlık Programını tamamlarken en az Almanca A2 ile koşullu özel öğrenci kabulü alabilir; ancak C1 belgelenmeden bu Almanca yüksek lisansa düzenli öğrenci olarak başlayamaz."),
    })
    row.setdefault("cost_profile", {}).update({
        "academic_year": "Fees current when checked 2026-07-14",
        "tuition_eur_per_year_min": 1453.44,
        "tuition_eur_per_year_max": 1453.44,
        "tuition_eur_per_year_estimated": 1453.44,
        "tuition_basis": "non_eu_foreign_national_standard_fee_unless_exempt",
        "student_contribution_eur": 52.4,
        "total_academic_cost_eur_per_year_estimated": 1505.84,
        "cost_notes": bi("TU Graz publishes EUR 726.72 tuition plus EUR 26.20 Austrian Student Union (ÖH) fee per semester for non-EU foreign nationals who are not exempt: EUR 1,453.44 tuition and EUR 52.40 ÖH per year. All students pay the ÖH fee; listed exemptions can change tuition liability.", "TU Graz, muaf olmayan AB dışı yabancı uyruklular için dönem başına 726,72 EUR öğrenim ücreti ve 26,20 EUR Avusturya Öğrenci Birliği (ÖH) ücreti yayımlar: yıllık 1.453,44 EUR öğrenim ücreti ve 52,40 EUR ÖH. Tüm öğrenciler ÖH ücretini öder; listelenen muafiyetler öğrenim ücreti yükümlülüğünü değiştirebilir."),
        "verification_notes": bi("This is the current published standard non-EU fee, not a claim that every third-country student is ineligible for a waiver.", "Bu, her üçüncü ülke öğrencisinin muafiyete uygun olmadığı iddiası değil, güncel yayımlanmış standart AB dışı ücrettir."),
    })
    row.setdefault("scholarship_profile", {}).update({
        "regional_scholarship_available": True,
        "regional_scholarship_name": "TU Graz High Potentials Master's scholarships",
        "merit_scholarships": [bi("TU Graz High Potentials supports talent from Austria and abroad with Master's scholarships of up to EUR 17,600 over two years. The next Master's application period starts 15 October 2026 for students admitted from winter semester 2027/28; individual scholarship requirements still apply.", "TU Graz High Potentials, Avusturya ve yurtdışından yetenekleri iki yıl boyunca yüksek lisans için 17.600 EUR'a kadar destekler. Sonraki yüksek lisans başvuru dönemi 2027/28 kış döneminden itibaren kabul edilen öğrenciler için 15 Ekim 2026'da başlar; burslara özgü koşullar yine uygulanır.")],
        "tuition_waivers": [],
        "non_eu_eligible": True,
        "scholarship_deadline": "2026-10-15 (opening date; current closing date not published on the checked page)",
        "scholarship_application_url": scholarship_url,
        "funding_competitiveness": "high",
        "funding_notes": bi("The Master's call requires good Bachelor's achievement, admission to a TU Graz Master's from winter 2027/28, motivation letter, CV, transcript, diploma if available, two teacher references and passport. Selection is first by a TU Graz expert jury and then scholarship providers. It is a competitive general Master's route, not a guaranteed programme-specific Space Sciences award.", "Yüksek lisans çağrısı iyi lisans başarısı, 2027/28 kış döneminden itibaren bir TU Graz yüksek lisansına kabul, niyet mektubu, CV, transkript, varsa diploma, iki öğretmen referansı ve pasaport ister. Seçim önce TU Graz uzman jürisi, sonra burs sağlayıcıları tarafından yapılır. Bu rekabetçi genel yüksek lisans rotasıdır; programa özgü garantili Space Sciences ödülü değildir."),
    })
    row.setdefault("living_profile", {}).update({
        "city_cost_level": "medium",
        "monthly_living_cost_eur_min": 800,
        "monthly_living_cost_eur_max": 1000,
        "monthly_living_cost_eur_estimated": None,
        "monthly_living_cost_scope_label": bi("TU Graz 2026/27 international-student planning guidance", "TU Graz 2026/27 uluslararası öğrenci planlama rehberi"),
        "monthly_living_cost_basis": bi("TU Graz's current 2026/27 international fact sheet advises EUR 800-1,000/month for rent, food and personal expenses, depending on housing and lifestyle. Its separate international FAQ cites just under EUR 1,300 as the 2025 Austria-wide Student Social Survey average; that national average is not presented as a Graz quote.", "TU Graz'ın güncel 2026/27 uluslararası bilgi notu, konaklama ve yaşam tarzına göre kira, yemek ve kişisel giderler için ayda 800-1.000 EUR önerir. Ayrı uluslararası SSS'si 2025 Avusturya geneli Öğrenci Sosyal Araştırması ortalamasını 1.300 EUR'un biraz altı olarak verir; bu ulusal ortalama Graz fiyatı olarak sunulmaz."),
        "average_room_rent_eur": None,
        "average_room_rent_eur_min": 400,
        "average_room_rent_eur_max": 600,
        "average_room_rent_scope_label": bi("TU Graz official Graz shared-flat room guidance", "TU Graz resmî Graz paylaşımlı daire oda rehberi"),
        "student_housing_available": True,
        "student_housing_competitiveness": "medium",
        "housing_difficulty": "medium",
        "living_risk": "medium",
        "housing_sentiment": None,
        "housing_notes": bi("TU Graz's current comparison guidance says a single room in a Graz shared flat typically costs EUR 400-600 depending on location and facilities. It is a planning range, not an offer or a guarantee of student-residence availability.", "TU Graz'ın güncel karşılaştırma rehberi, Graz'ta paylaşımlı dairede tek kişilik odanın konum ve olanaklara göre tipik olarak 400-600 EUR olduğunu söyler. Bu planlama aralığıdır; teklif veya öğrenci yurdu uygunluk garantisi değildir."),
    })
    row.setdefault("curriculum_profile", {}).update({
        "tracks": ["space_sciences", "earth_observation"],
        "specializations": ["satellite_components", "space_measurement_systems", "earth_observation", "satellite_communications", "micro_and_nanosatellites", "numerical_modelling"],
        "mandatory_courses": [],
        "elective_courses": ["Space technologies", "Earth observation", "Satellite communication", "Numerical modelling"],
        "thesis_required": True,
        "internship_required": None,
        "curriculum_url": programme_url,
        "curriculum_structure": bi("The official programme page identifies the focused technical spine: satellite components and measurement systems, space technologies, Earth observation, micro/nanosatellites, satellite communication and numerical modelling. It also says students can join research teams and use laboratory equipment; course-by-course mandatory modules are not inferred from the public summary.", "Resmî program sayfası odaklı teknik omurgayı tanımlar: uydu bileşenleri ve ölçüm sistemleri, uzay teknolojileri, Dünya gözlemi, mikro/nano uydular, uydu haberleşmesi ve sayısal modelleme. Ayrıca öğrencilerin araştırma ekiplerine katılıp laboratuvar ekipmanı kullanabileceğini söyler; ders-ders zorunlu modüller kamu özetinden çıkarılmaz."),
    })
    row.setdefault("category_profile", {}).update({
        "primary_categories": ["space_systems", "earth_observation"],
        "secondary_categories": ["satellite_systems", "satellite_communications", "remote_sensing", "space_measurement_systems", "micro_nanosatellites", "numerical_modelling"],
        "normalized_tags": ["spacecraft_systems", "earth_observation", "remote_sensing", "satellite_communications", "micro_nanosatellites", "space_measurement_systems", "numerical_modelling"],
    })
    row.setdefault("research_profile", {}).update({
        "department_research_areas": ["Micro- and nanosatellites", "Satellite components and measurement systems", "Numerical modelling", "Earth observation", "Satellite communication"],
        "labs": ["TU Graz space-science laboratories", "Space Research Institute of the Austrian Academy of Sciences"],
        "research_centers": ["Space Research Institute, Austrian Academy of Sciences", "Joanneum Research", "University of Graz"],
        "research_strength_summary": bi("This is unusually ecosystem-integrated rather than a generic space label: TU Graz, University of Graz, the Austrian Academy of Sciences' Space Research Institute and Joanneum Research jointly teach and research space science and technologies. TU Graz says Graz researchers have contributed to active space missions for more than 30 years and students can join research teams using modern methods and lab equipment.", "Bu, genel bir uzay etiketi yerine olağandışı derecede ekosistemle bütünleşmiş programdır: TU Graz, University of Graz, Avusturya Bilimler Akademisi'nin Space Research Institute'u ve Joanneum Research uzay bilimleri/teknolojilerinde birlikte eğitim ve araştırma yapar. TU Graz, Graz araştırmacılarının 30 yılı aşkın süredir aktif uzay görevlerine katkı verdiğini ve öğrencilerin modern yöntemlerle laboratuvar ekipmanı kullanan araştırma ekiplerine katılabileceğini söyler."),
        "research_strength_score": None,
        "research_sources": [programme_url],
    })
    row.setdefault("industry_ecosystem_profile", {}).update({
        "nearby_companies": [],
        "confirmed_partners": ["University of Graz", "Space Research Institute of the Austrian Academy of Sciences", "Joanneum Research"],
        "research_institutes": ["Space Research Institute, Austrian Academy of Sciences", "Joanneum Research"],
        "ecosystem_notes": bi("These are confirmed teaching/research collaborators named by the programme page. ESA and NASA are mentioned as missions for which Graz-built/co-developed components and measurement systems are used, but neither is presented as a guaranteed student placement or a degree-specific formal partnership.", "Bunlar program sayfasında isimle belirtilen doğrulanmış eğitim/araştırma işbirlikçileridir. ESA ve NASA, Graz'ta geliştirilen bileşen/ölçüm sistemlerinin kullanıldığı görevler olarak anılır; ancak hiçbiri garantili öğrenci yerleştirmesi veya dereceye özgü resmî ortaklık olarak sunulmaz."),
        "ecosystem_strength_score": None,
    })
    row["application_timeline_profile"] = {
        "academic_year": "Current annual international Master's deadlines",
        "intake_terms": ["winter semester", "summer semester"],
        "application_rounds": ["Third-country winter: 1 May-15 August", "Third-country summer: 1 December-15 January", "EU/EEA winter: 1 May-15 October", "EU/EEA summer: 1 December-15 March"],
        "non_eu_deadline": "2026-08-15 (winter; applications open 2026-05-01); 2027-01-15 (summer; applications open 2026-12-01)",
        "eu_deadline": "2026-10-15 (winter); 2027-03-15 (summer)",
        "winter_deadline": "2026-08-15 (third-country applicants); 2026-10-15 (EU/EEA)",
        "summer_deadline": "2027-01-15 (third-country applicants); 2027-03-15 (EU/EEA)",
        "application_deadline": "2026-08-15 for third-country winter applicants",
        "timeline_risk": "high",
        "deadline_notes": bi("The official international Master's page warns processing can take weeks to months and strongly recommends complete early submission; TU Graz accepts no responsibility for visa appointments or relocation planning. Treat the third-country 15 August winter deadline as a hard ceiling, not a safe visa-planning date.", "Resmî uluslararası yüksek lisans sayfası işlemenin haftalar-aylar sürebileceği uyarısını yapar ve eksiksiz erken başvuruyu şiddetle önerir; TU Graz vize randevuları veya taşınma planlaması için sorumluluk kabul etmez. Üçüncü ülke kış dönemi 15 Ağustos son tarihini güvenli vize planlama tarihi değil kesin üst sınır sayın."),
    }
    row["student_sentiment_profile"] = {"student_satisfaction_score": None, "sentiment_confidence": "unknown", "sample_size_estimate": None, "date_range": "", "student_sentiment_sources": [], "student_sentiment_summary": bi("No sufficiently documented, independent student-sentiment sample was retained; no sentiment score is shown.", "Yeterince belgelenmiş bağımsız öğrenci görüşü örneklemi tutulmadı; duygu puanı gösterilmez."), "verification_notes": bi("Student sentiment remains separate from official facts and is not fabricated to fill the card.", "Öğrenci görüşleri resmî bilgilerden ayrı tutulur ve kartı doldurmak için uydurulmaz.")}
    row["decision_summary"] = {
        "main_strengths": [bi("A genuinely space-specific German MSc: satellite components and measurement systems, Earth observation, micro/nanosatellites, satellite communication and numerical modelling—not a generic Mechanical Engineering degree with a space tag.", "Gerçekten uzaya özgü Almanca MSc: uydu bileşenleri ve ölçüm sistemleri, Dünya gözlemi, mikro/nano uydular, uydu haberleşmesi ve sayısal modelleme—uzay etiketi eklenmiş genel Makine Mühendisliği değildir."), bi("The programme's research ecosystem is unusually concrete: joint teaching/research with University of Graz, the Austrian Academy's Space Research Institute and Joanneum Research, alongside access to research teams and laboratories.", "Programın araştırma ekosistemi olağandışı derecede somuttur: University of Graz, Avusturya Bilimler Akademisi'nin Space Research Institute'u ve Joanneum Research ile ortak eğitim/araştırma, ayrıca araştırma ekipleri ve laboratuvarlara erişim."),
        ],
        "main_risks": [bi("German C1 is the real hard filter. A2 can only support temporary non-degree preparation; it does not let a student start the regular German Master's curriculum.", "Almanca C1 gerçek sert filtredir. A2 yalnızca geçici özel öğrenci hazırlığını destekleyebilir; düzenli Almanca yüksek lisans müfredatına başlamayı sağlamaz."), bi("For a non-exempt non-EU applicant, published annual study charges are EUR 1,453.44 tuition plus EUR 52.40 ÖH. Official Graz planning guidance is EUR 800-1,000/month and typical shared-flat rooms EUR 400-600/month.", "Muaf olmayan AB dışı aday için yayımlanmış yıllık eğitim ücretleri 1.453,44 EUR öğrenim ücreti artı 52,40 EUR ÖH'dir. Resmî Graz planlama rehberi ayda 800-1.000 EUR, tipik paylaşımlı daire odaları ise 400-600 EUR'dur."), bi("Third-country applications require early action: the winter 15 August date is not a safe visa timeline because TU Graz says processing can take weeks to months.", "Üçüncü ülke başvuruları erken hareket gerektirir: TU Graz işlemenin haftalar-aylar sürebileceğini söylediği için kış dönemi 15 Ağustos tarihi güvenli vize zaman çizelgesi değildir."),
        ],
        "best_for": [bi("German-proficient applicants targeting Earth observation, satellite instrumentation, nanosatellites or space-science research rather than aircraft design.", "Uçak tasarımı yerine Dünya gözlemi, uydu enstrümantasyonu, nanosatellitler veya uzay bilimi araştırmasını hedefleyen Almanca yeterlikli adaylar.")],
        "not_ideal_for": [bi("English-only applicants or candidates seeking a pure spacecraft-design/propulsion degree without an Earth-observation and research-science emphasis.", "Yalnızca İngilizce bilen adaylar veya Dünya gözlemi/araştırma-bilim vurgusu olmadan saf uzay aracı tasarımı/itki derecesi arayanlar.")],
    }
    row["financials"] = {"tuition_fee_per_year": None, "semester_fee": None}
    row["scholarships_info"] = []
    row["admission"] = {"requirements": {"minimum_gpa": None, "minimum_gpa_notes": "unknown", "required_ects": None, "language_requirements": "German C1 for regular enrolment; see language_profile."}}
    row["source_profile"] = {
        "official_program_page": programme_url, "official_admission_page": admission_url, "official_curriculum_page": programme_url, "official_tuition_page": tuition_url, "official_scholarship_page": scholarship_url, "official_housing_page": factsheet_url, "official_department_page": programme_url,
        "source_log": [
            source(programme_url, "TU Graz Space Sciences and Earth from Space MSc", "official_program_page", ["program", "degree", "duration", "language", "admission", "curriculum", "research", "industry"], "Current programme page confirms the German 120-ECTS/4-semester MSc-equivalent, relevant degree framework, technical focus and named Graz research ecosystem.", "Güncel program sayfası Almanca 120 AKTS/dört yarıyıllık MSc-denk dereceyi, ilgili diploma çerçevesini, teknik odağı ve isimli Graz araştırma ekosistemini doğrular."),
            source(admission_url, "TU Graz International Master's Admission", "official_admission_page", ["admission", "non_eu", "deadline"], "Current page publishes the separate EU/EEA and third-country winter/summer deadlines and warns that processing can take weeks to months.", "Güncel sayfa ayrı AB/AEA ve üçüncü ülke kış/yaz son tarihlerini yayımlar ve işlemenin haftalar-aylar sürebileceği uyarısını yapar."),
            source(language_url, "TU Graz Proof of German Language Competence", "official_admission_page", ["language", "admission"], "Current page documents C1 for regular German-degree enrolment, accepted examples and the A2 non-degree preparation path.", "Güncel sayfa düzenli Almanca derece kaydı için C1'i, kabul edilen örnekleri ve A2 özel öğrenci hazırlık yolunu belgeler."),
            source(tuition_url, "TU Graz Tuition Fees and Austrian Student Union Fee", "official_tuition_page", ["tuition", "fees"], "Current page publishes EUR 726.72 non-EU tuition and EUR 26.20 ÖH per semester, with exemptions explained separately.", "Güncel sayfa dönem başına 726,72 EUR AB dışı öğrenim ücreti ve 26,20 EUR ÖH yayımlar; muafiyetleri ayrıca açıklar."),
            source(scholarship_overview_url, "TU Graz High Potentials", "official_scholarship_page", ["scholarship", "funding"], "Current page says talent from Austria and abroad can receive up to EUR 17,600 for Master's study over two years and gives the 15 October 2026 opening date.", "Güncel sayfa Avusturya ve yurtdışından yeteneklerin iki yıllık yüksek lisans için 17.600 EUR'a kadar alabileceğini ve 15 Ekim 2026 açılış tarihini verir."),
            source(scholarship_url, "TU Graz Master's Scholarship Application", "official_scholarship_page", ["scholarship", "deadline", "non_eu"], "Current page gives winter 2027/28 admission and document requirements, a 15 October 2026 opening and two-stage selection by TU Graz experts and providers.", "Güncel sayfa 2027/28 kış kabulü ve belge koşullarını, 15 Ekim 2026 açılışını ve TU Graz uzmanları/sağlayıcılar tarafından iki aşamalı seçimi verir."),
            source(factsheet_url, "TU Graz Incoming Fact Sheet 2026/27", "official_cost_of_living_page", ["living", "housing"], "Current 2026/27 official fact sheet advises EUR 800-1,000/month for rent, food and personal expenses and clearly labels it approximate planning guidance.", "Güncel 2026/27 resmî bilgi notu kira, yemek ve kişisel giderler için aylık 800-1.000 EUR önerir ve bunu açıkça yaklaşık planlama rehberi olarak etiketler."),
            source(rent_url, "TU Graz Graz vs Vienna Student-Cost Guide", "official_cost_of_living_page", ["housing"], "Current TU Graz comparison guidance says a Graz single room in a shared flat typically ranges EUR 400-600 depending on location and facilities.", "Güncel TU Graz karşılaştırma rehberi Graz'ta paylaşımlı dairede tek kişilik odanın konum ve olanaklara göre tipik olarak 400-600 EUR olduğunu söyler."),
        ],
        "last_verified": CHECKED, "needs_verification": False,
        "verification_notes": bi("All displayed decision fields are tied to checked official sources. The scholarship is a competitive general Master's route and the room figure is scoped planning guidance; neither is portrayed as guaranteed support or housing.", "Gösterilen tüm karar alanları kontrol edilmiş resmî kaynaklara bağlıdır. Burs rekabetçi genel yüksek lisans rotası, oda tutarı ise kapsamı belirtilmiş planlama rehberidir; hiçbiri garantili destek veya konaklama olarak sunulmaz."),
        "field_confidence": {"program_basic_info": "high", "language": "high", "admission": "high", "tuition": "high", "scholarship": "high", "curriculum": "high", "research_profile": "high", "industry_ecosystem_profile": "high", "application_timeline_profile": "high", "living_profile": "high", "housing": "high", "deadlines": "high"},
    }
    newline = "\r\n" if "\r\n" in original else "\n"
    document["last_updated"] = CHECKED
    PATH.write_text(json.dumps(document, ensure_ascii=False, indent=2).replace("\n", newline) + newline, encoding="utf-8")
    print("Updated TU Graz Space Sciences and Earth from Space with current official evidence.")


if __name__ == "__main__":
    main()
