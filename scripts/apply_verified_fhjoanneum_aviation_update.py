"""Fill FH JOANNEUM Aviation's curriculum and Graz planning-cost gaps."""

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
    row = next(item for item in document["programs"] if item.get("id") == "austria_fhjoanneum_msc_aviation")

    programme_url = "https://www.fh-joanneum.at/luftfahrt/master/en/"
    curriculum_url = "https://www.fh-joanneum.at/luftfahrt/master/en/my-studies/curriculum/"
    degree_url = "https://www.fh-joanneum.at/luftfahrt/master/en/my-studies/degree-programme/"
    graduation_url = "https://www.fh-joanneum.at/luftfahrt/master/en/my-studies/graduation/"
    admission_url = "https://www.fh-joanneum.at/luftfahrt/master/en/admissions/application-requirements/"
    international_url = "https://www.fh-joanneum.at/en/international/international-degree-seeking-students/admissions/international-applicants-masters-degree-programme/"
    dates_url = "https://www.fh-joanneum.at/luftfahrt/master/en/admissions/dates-deadlines/"
    scholarship_url = "https://www.fh-joanneum.at/luftfahrt/master/en/admissions/international-applicants/"
    living_url = "https://cdn3.fh-joanneum.at/media/2025/11/Non-EU_Handout_2026-27.pdf"
    simulator_url = "https://www.fh-joanneum.at/en/labor/flight-simulation-laboratory/"

    row.update({
        "program_name": "Aviation",
        "program_native_name": "Luftfahrt / Aviation",
        "program_degree": "Master of Science in Engineering (MSc)",
        "degree_level": "Master",
        "degree_class": "MSc",
        "duration_years": 2,
        "ects": 120,
        "teaching_language": ["English"],
        "program_url": programme_url,
        "department": "FH JOANNEUM Institute of Aviation",
        "campus": "Graz",
        "program_status": "active",
        "relevance_status": "strong",
    })
    row["living_profile"] = {
        "city_cost_level": "medium",
        "monthly_living_cost_eur_min": 1000,
        "monthly_living_cost_eur_max": 1100,
        "monthly_living_cost_eur_estimated": None,
        "monthly_living_cost_scope_label": bi("FH JOANNEUM 2026/27 non-EU monthly planning budget for Graz", "FH JOANNEUM 2026/27 Graz için AB dışı aylık planlama bütçesi"),
        "monthly_living_cost_basis": bi("Official 2026/27 handout: accommodation including heating/electricity EUR 400-500, food EUR 300, and study/personal requirements, books, culture and recreation EUR 300.", "Resmî 2026/27 bilgi notu: ısınma/elektrik dahil konaklama 400-500 EUR, yemek 300 EUR, eğitim/kişisel gereksinimler, kitaplar, kültür ve eğlence 300 EUR."),
        "average_room_rent_eur": None,
        "average_room_rent_eur_min": 400,
        "average_room_rent_eur_max": 500,
        "average_room_rent_scope_label": bi("FH JOANNEUM 2026/27 Graz accommodation planning component, including heating and electricity", "FH JOANNEUM 2026/27 Graz konaklama planlama kalemi, ısınma ve elektrik dahil"),
        "student_housing_available": True,
        "student_housing_competitiveness": "high",
        "housing_difficulty": "high",
        "living_risk": "medium",
        "housing_sentiment": None,
        "housing_notes": bi("The official handout directs international degree-seeking students to apply online for Graz housing via OeAD and recommends applying early because visa procedures can be long. EUR 400-500 is its accommodation component, not a specific room offer or an availability guarantee.", "Resmî bilgi notu uluslararası derece öğrencilerini Graz konaklaması için OeAD üzerinden çevrimiçi başvuruya yönlendirir ve vize prosedürleri uzun olabileceğinden erken başvuruyu önerir. 400-500 EUR, belirli oda teklifi veya uygunluk garantisi değil, konaklama planlama kalemidir."),
        "verification_notes": bi("The displayed EUR 1,000-1,100 is a current official planning budget with stated components, not a student-review average or a rent-only quote.", "Gösterilen 1.000-1.100 EUR, belirtilmiş kalemleri olan güncel resmî planlama bütçesidir; öğrenci yorumu ortalaması veya yalnızca kira tutarı değildir."),
    }
    row["curriculum_profile"] = {
        "tracks": ["aeronautical_engineering", "aviation_management", "research_and_development"],
        "specializations": ["lightweight_aircraft_design", "aerodynamics", "cfd", "propulsion", "aircraft_systems", "flight_control", "uav", "avionics", "aviation_certification", "aviation_maintenance", "sustainable_aviation"],
        "mandatory_courses": ["Applied Mathematics and Simulation in Aerospace", "Systems Engineering", "Unmanned Aerial Systems", "Advanced Aerodynamics", "Aircraft Propulsion Technologies", "Aircraft Systems", "Flight Control Systems", "Regulations and Certification in Aerospace", "Technical Airport Operations", "Maintenance Management", "Management and Sustainability in Aerospace", "Scientific Writing and Speaking in Aeronautics", "Professional Internship"],
        "elective_courses": ["Electro-Mechanical Drive Systems", "Human Factors in Aerospace", "Numerical Simulations in Heat Transfer", "Military Maintenance Management", "Project 2"],
        "course_language_notes": bi("The programme page says all course content is taught in English. The detailed curriculum includes a German-language optional Language 2 course; this does not change the published programme teaching language.", "Program sayfası tüm ders içeriğinin İngilizce okutulduğunu söyler. Ayrıntılı müfredatta Almanca okutulan seçmeli Language 2 dersi bulunur; bu, yayımlanan program eğitim dilini değiştirmez."),
        "thesis_required": True,
        "internship_required": True,
        "internship_ects": 30,
        "lab_courses": ["Aerospace Engineering Lab", "Flight Simulation Laboratory"],
        "project_based_courses": ["Project 2", "JOANNEUM AERONAUTICS student aircraft team"],
        "curriculum_url": curriculum_url,
        "study_plan_url": curriculum_url,
        "curriculum_structure": bi("This is not a generic management degree. It offers two individual-focus semesters, then a 30-ECTS professional internship and a Master's thesis. The technical path combines aerodynamics/CFD, propulsion, aircraft systems, fly-by-wire and control, UAVs, avionics and certification; the alternative focus develops airport operations, maintenance, safety, supply chain and sustainable aviation management.", "Bu, genel bir yönetim derecesi değildir. İki bireysel odak yarıyılı, ardından 30 AKTS profesyonel staj ve yüksek lisans tezi sunar. Teknik yol aerodinamik/HAD, itki, uçak sistemleri, fly-by-wire ve kontrol, İHA'lar, aviyonik ve sertifikasyonu birleştirir; alternatif odak havalimanı operasyonları, bakım, emniyet, tedarik zinciri ve sürdürülebilir havacılık yönetimini geliştirir."),
        "verification_notes": bi("Course names, language indications and the internship requirement are taken from the public curriculum and graduation pages. A student selects technical or business electives, so the broad programme title alone does not guarantee the same depth for every individual plan.", "Ders adları, dil göstergeleri ve staj gereği kamuya açık müfredat ile mezuniyet sayfalarından alınmıştır. Öğrenci teknik veya işletme seçmelilerini seçer; bu nedenle geniş program adı her bireysel planda aynı derinliği garanti etmez."),
    }
    row["category_profile"] = {
        "primary_categories": ["aeronautics", "aviation_management"],
        "secondary_categories": ["aircraft_design", "cfd", "propulsion", "aircraft_systems", "gnc", "uav", "avionics", "aviation_maintenance", "aviation_certification", "sustainable_aviation"],
        "normalized_tags": ["aerospace_engineering", "aeronautics", "cfd", "flight_control", "uav", "aircraft_systems", "propulsion", "aviation_management", "maintenance", "certification"],
    }
    row["research_profile"] = {
        "department_research_areas": ["aircraft and drone construction", "aerodynamics", "avionics", "flight control", "flight simulation"],
        "labs": ["Aerospace Engineering Lab", "Flight Simulation Laboratory"],
        "research_centers": ["FH JOANNEUM Institute of Aviation"],
        "space_or_aerospace_projects": [],
        "student_teams": ["JOANNEUM AERONAUTICS"],
        "satellite_or_flight_projects": [],
        "research_strength_summary": bi("FH JOANNEUM explicitly makes first- and second-semester Institute research participation available through electives. Its flight-simulation lab has two research simulators developed with students in projects and theses; JFS² supports stability, fly-by-wire and autonomous-UAV control research, while the full-motion JFSM offers six degrees of freedom. This is concrete applied aviation infrastructure.", "FH JOANNEUM, ilk ve ikinci yarıyılda enstitü araştırmalarına seçmeliler yoluyla katılımı açıkça sunar. Uçuş simülasyon laboratuvarında projeler ve tezlerde öğrencilerle geliştirilen iki araştırma simülatörü vardır; JFS² kararlılık, fly-by-wire ve otonom İHA kontrol araştırmasını destekler, tam hareketli JFSM ise altı serbestlik derecesi sunar. Bu, somut uygulamalı havacılık altyapısıdır."),
        "research_strength_score": None,
        "research_sources": [programme_url, degree_url, simulator_url],
    }
    row["industry_ecosystem_profile"] = {
        "nearby_companies": [],
        "confirmed_partners": [],
        "research_institutes": [],
        "internship_possibility": "high",
        "thesis_with_industry_possibility": "high",
        "career_relevance": "strong",
        "ecosystem_strength_score": None,
        "ecosystem_notes": bi("The professional internship is compulsory (30 ECTS). The graduation page says Master's topics are mostly developed in collaboration with a company. This supports a real industry interface, but it does not name a partner or promise any particular placement.", "Profesyonel staj zorunludur (30 AKTS). Mezuniyet sayfası yüksek lisans tez konularının çoğunlukla bir şirketle işbirliği içinde geliştirildiğini söyler. Bu gerçek bir sanayi arayüzünü destekler, ancak ortak adı vermez veya belirli yerleştirme garantisi sunmaz."),
    }
    row["application_timeline_profile"] = {
        "academic_year": "2026/2027 published intake",
        "intake_terms": ["winter semester; studies start 28 September 2026"],
        "application_rounds": ["Programme rolling dates through 3 August 2026", "Third-country document deadline: 29 June 2026", "Pakistan/India/Bangladesh/Iran/Nigeria application deadline: 1 February 2026"],
        "non_eu_deadline": "2026-06-29 (all documents for most third-country applicants); 2026-02-01 for Pakistan, India, Bangladesh, Iran and Nigeria",
        "eu_deadline": "2026-08-03",
        "application_deadline": "2026-08-03 for the published programme cycle; earlier country-specific third-country deadlines apply",
        "scholarship_deadline": None,
        "timeline_risk": "high",
        "deadline_notes": bi("At verification on 14 July 2026, the third-country deadlines had passed while the published programme cycle still displayed 3 August 2026 for applicants not subject to those country-specific requirements. This must not be extrapolated to a future intake; document legalisation and residence-permit timing are explicit risks.", "14 Temmuz 2026 doğrulamasında üçüncü ülke tarihleri geçmişti; buna karşın yayımlanan program döngüsü bu ülkeye özgü koşullara tabi olmayan adaylar için hâlâ 3 Ağustos 2026 gösteriyordu. Bu gelecek girişe taşınmamalıdır; belge tasdiki ve oturma izni zamanlaması açık risklerdir."),
    }
    row["student_sentiment_profile"] = {
        "student_satisfaction_score": None,
        "sentiment_confidence": "unknown",
        "sample_size_estimate": None,
        "date_range": "",
        "student_sentiment_sources": [],
        "student_sentiment_summary": bi("No sufficiently documented, independent student-sentiment sample was retained; no satisfaction score is displayed.", "Yeterince belgelenmiş bağımsız öğrenci görüşü örneklemi tutulmadı; memnuniyet puanı gösterilmez."),
        "verification_notes": bi("Student sentiment remains separate from the official curriculum, cost and admission facts.", "Öğrenci görüşleri resmî müfredat, maliyet ve kabul bilgilerinden ayrı tutulur."),
    }
    row["decision_summary"] = {
        "main_strengths": [bi("A rare programme that lets the applicant distinguish an aeronautical-engineering path (CFD, propulsion, aircraft systems, control and UAVs) from an aviation-management path rather than treating both as the same course.", "HAD, itki, uçak sistemleri, kontrol ve İHA'ları içeren havacılık mühendisliği yolunu; havacılık yönetimi yolundan ayırmayı sağlayan nadir bir programdır; ikisini aynı ders gibi göstermez."), bi("The practical commitment is unusually transparent: 30 ECTS compulsory internship, company-collaborative thesis work in most cases, a student aircraft team, and research flight simulators built with students.", "Uygulama taahhüdü olağandışı derecede şeffaftır: 30 AKTS zorunlu staj, çoğu durumda şirket işbirlikli tez çalışması, öğrenci uçak ekibi ve öğrencilerle geliştirilen araştırma uçuş simülatörleri.")],
        "main_risks": [bi("The EUR 1,000-1,100/month Graz figure is an official non-EU planning budget, and its EUR 400-500 accommodation component is not a guaranteed room. Apply to OeAD housing early.", "Aylık 1.000-1.100 EUR Graz tutarı resmî AB dışı planlama bütçesidir; bunun 400-500 EUR konaklama kalemi garantili oda değildir. OeAD konaklamasına erken başvurun."), bi("Country-specific third-country deadlines can precede the visible programme date by months. The published 2026 dates are already partly past and cannot be reused for 2027.", "Ülkeye özgü üçüncü ülke son tarihleri görünür program tarihinden aylar önce olabilir. Yayımlanan 2026 tarihleri kısmen geçmiştir ve 2027 için yeniden kullanılamaz."), bi("Attendance is compulsory; normally more than 20% absence in a course prevents the first examination. That matters for applicants planning substantial parallel work or travel.", "Devam zorunludur; normalde bir derste %20'den fazla devamsızlık ilk sınava girmeyi engeller. Bu, önemli paralel çalışma veya seyahat planlayan adaylar için önemlidir.")],
        "best_for": [bi("Applicants who want applied aeronautical engineering with an elective-controlled technical path and a compulsory industry-facing internship, or who deliberately want aviation operations/maintenance/management alongside engineering.", "Seçmelilerle kontrol edilen teknik yol ve zorunlu, sanayiyle temaslı staj içeren uygulamalı havacılık mühendisliği; ya da mühendisliğin yanında bilinçli olarak havacılık operasyonu/bakım/yönetimi isteyen adaylar.")],
        "not_ideal_for": [bi("Applicants seeking a pure space-engineering degree, a fully fixed technical curriculum with no management choices, or a guaranteed company placement.", "Saf uzay mühendisliği derecesi, yönetim seçimi olmayan tamamen sabit teknik müfredat veya garantili şirket yerleştirmesi isteyen adaylar.")],
    }
    row["source_profile"] = {
        "official_program_page": programme_url,
        "official_admission_page": admission_url,
        "official_curriculum_page": curriculum_url,
        "official_tuition_page": international_url,
        "official_scholarship_page": scholarship_url,
        "official_housing_page": living_url,
        "official_department_page": degree_url,
        "official_lab_pages": [simulator_url],
        "source_log": [
            source(programme_url, "FH JOANNEUM Aviation MSc", "official_program_page", ["program", "language", "curriculum", "research"], "Current programme page confirms active English full-time MSc delivery, 120 ECTS/4 semesters, technical/research themes and the student aircraft team.", "Güncel program sayfası aktif İngilizce tam zamanlı MSc eğitimini, 120 AKTS/dört yarıyılı, teknik/araştırma temalarını ve öğrenci uçak ekibini doğrular."),
            source(curriculum_url, "FH JOANNEUM Aviation MSc curriculum", "official_curriculum_page", ["curriculum", "language"], "Current detailed curriculum publishes course titles, ECTS, teaching-language indications and the 30-ECTS professional internship.", "Güncel ayrıntılı müfredat ders adlarını, AKTS'leri, eğitim dili göstergelerini ve 30 AKTS profesyonel stajı yayımlar."),
            source(degree_url, "FH JOANNEUM Aviation MSc degree programme", "official_department_page", ["curriculum", "research"], "Current page describes the aeronautical engineering, aviation-management and research-and-development focus routes, elective choice and Institute research participation.", "Güncel sayfa havacılık mühendisliği, havacılık yönetimi ve araştırma-geliştirme odak rotalarını, seçmeli seçimini ve Enstitü araştırma katılımını açıklar."),
            source(graduation_url, "FH JOANNEUM Aviation MSc graduation", "official_curriculum_page", ["curriculum", "industry"], "Current graduation page confirms the compulsory internship and Master's thesis; it says thesis topics are mostly developed with a company.", "Güncel mezuniyet sayfası zorunlu stajı ve yüksek lisans tezini doğrular; tez konularının çoğunlukla bir şirketle geliştirildiğini söyler."),
            source(admission_url, "FH JOANNEUM Aviation admission requirements", "official_admission_page", ["admission", "language"], "Current page supports the retained admission and English-language requirements.", "Güncel sayfa korunan kabul ve İngilizce dil koşullarını destekler."),
            source(international_url, "FH JOANNEUM international Master's applicants", "official_admission_page", ["admission", "non_eu", "deadline"], "Current 2026/27 page publishes third-country document deadlines, deposit process, visa-funds requirements and the need to submit complete international documents early.", "Güncel 2026/27 sayfası üçüncü ülke belge son tarihlerini, depozito sürecini, vize fon koşullarını ve eksiksiz uluslararası belgelerin erken sunulması gereğini yayımlar."),
            source(international_url, "FH JOANNEUM international tuition 2026/27", "official_tuition_page", ["tuition", "fees"], "Current page publishes EUR 726.72 per semester for standard third-country students, EUR 363.36 for named exceptions, plus the Student Union fee and the EUR 250 deposit/EUR 10 processing-fee rules.", "Güncel sayfa standart üçüncü ülke öğrencileri için dönem başına 726,72 EUR, isimli istisnalar için 363,36 EUR ile Öğrenci Birliği ücretini ve 250 EUR depozito/10 EUR işlem ücreti kurallarını yayımlar."),
            source(scholarship_url, "FH JOANNEUM Aviation international applicants and TECH!Southeast", "official_scholarship_page", ["scholarship", "non_eu"], "Current Aviation page supports the retained nationality-limited TECH!Southeast scholarship; it is not treated as general non-EU funding.", "Güncel Aviation sayfası vatandaşlıkla sınırlı TECH!Southeast bursunu destekler; genel AB dışı finansman olarak gösterilmez."),
            source(dates_url, "FH JOANNEUM Aviation dates 2026", "official_admission_page", ["deadline"], "Current dates page publishes the rolling programme dates and 28 September 2026 start date.", "Güncel tarihler sayfası dönemsel program tarihlerini ve 28 Eylül 2026 başlangıç tarihini yayımlar."),
            source(living_url, "FH JOANNEUM non-EU handout 2026/27", "official_cost_of_living_page", ["living", "housing"], "Official 2026/27 handout publishes EUR 400-500 accommodation including heating/electricity and a EUR 1,000-1,100 monthly cost-of-living plan for Graz.", "Resmî 2026/27 bilgi notu ısınma/elektrik dahil 400-500 EUR konaklama ve Graz için aylık 1.000-1.100 EUR yaşam gideri planı yayımlar."),
            source(simulator_url, "FH JOANNEUM Flight Simulation Laboratory", "official_lab_page", ["research"], "Official laboratory page documents two research simulators, student development through projects/theses and use in flight-dynamics, fly-by-wire and autonomous-UAV control research.", "Resmî laboratuvar sayfası iki araştırma simülatörünü, projeler/tezler yoluyla öğrenci geliştirmesini ve uçuş dinamiği, fly-by-wire ve otonom İHA kontrol araştırmalarındaki kullanımını belgeler."),
        ],
        "last_verified": CHECKED,
        "needs_verification": False,
        "verification_notes": bi("All displayed decision fields are sourced from accessible official pages. Curriculum depth is shown as selectable routes, and all cost figures are labelled by scope rather than converted into unsupported estimates.", "Gösterilen tüm karar alanları erişilebilir resmî sayfalardan kaynaklanır. Müfredat derinliği seçilebilir rotalar olarak gösterilir; tüm maliyet tutarları kaynaksız tahmine dönüştürülmeden kapsamıyla etiketlenir."),
        "field_confidence": {"program_basic_info": "high", "language": "high", "admission": "high", "tuition": "high", "scholarship": "high", "curriculum": "high", "research_profile": "high", "industry_ecosystem_profile": "medium", "application_timeline_profile": "high", "living_profile": "high", "housing": "high", "deadlines": "high"},
    }
    document["last_updated"] = CHECKED
    newline = "\r\n" if "\r\n" in original else "\n"
    PATH.write_text(json.dumps(document, ensure_ascii=False, indent=2).replace("\n", newline) + newline, encoding="utf-8")
    print("Updated FH JOANNEUM Aviation with official curriculum and living-cost evidence.")


if __name__ == "__main__":
    main()
