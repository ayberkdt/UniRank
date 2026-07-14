"""Correct ISAE-SUPAERO MAE facts using current, direct official sources.

The total MAE tuition is deliberately left null: the checked programme page
publishes the application fee and confirmation deposit but not a current total.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from apply_verified_polimi_aero_update import bi, source


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data_base" / "fransa.json"
CHECKED = "2026-07-14"


def main() -> None:
    original = PATH.read_text(encoding="utf-8")
    document: dict[str, Any] = json.loads(original)
    row = next(item for item in document["programs"] if item.get("id") == "france_isae_supaero_msc")

    programme_url = "https://www.isae-supaero.fr/en/programmes/masters-degree-in-aerospace-engineering/"
    brochure_url = "https://www.isae-supaero.fr/wp-content/uploads/2025/12/202509_MAE-24PAGES-2025-26_WEB2.pdf"
    research_url = "https://www.isae-supaero.fr/en/research/"
    space_research_url = "https://www.isae-supaero.fr/en/electronics-optronics-and-signal-processing-department/space-systems-for-planetology-and-applications-sspa-scientific-group/"

    row.update({
        "program_name": "Master's Degree in Aerospace Engineering (MAE)",
        "program_native_name": "Master en Aéronautique et Espace — parcours Aerospace Engineering",
        "program_degree": "Master's degree",
        "degree_level": "Master",
        "degree_class": "French national Master's degree",
        "duration_years": 2,
        "ects": 120,
        "teaching_language": ["English"],
        "program_url": programme_url,
        "department": "ISAE-SUPAERO Master's Degree in Aerospace Engineering",
        "campus": "Toulouse",
        "program_status": "active",
        "relevance_status": "strong",
    })
    row.setdefault("eligibility_profile", {}).update({
        "eligible_for_non_eu": True,
        "required_previous_degree": bi("Bachelor's degree or equivalent obtained abroad; final-year students may apply with an enrolment certificate and provide the degree by the start of the academic year.", "Yurtdışından alınmış lisans diploması veya dengi; son sınıf öğrencileri kayıt belgesiyle başvurup diplomasını akademik yıl başlangıcında sunabilir."),
        "accepted_backgrounds": ["Aerospace or aeronautical engineering", "Mechanical engineering", "Mechatronics", "Electrical/electronics/telecommunications", "Computer science", "Science and engineering", "Strong mathematics or physics background"],
        "minimum_gpa": None,
        "admission_mode": "admissions-panel review of a complete online application; no interview planned",
        "admission_risk": "high",
        "required_documents": [
            bi("Diploma or enrolment certificate for final-year applicants", "Diploma veya son sınıf adayları için kayıt belgesi"),
            bi("Transcripts for the last three study years", "Son üç öğrenim yılının transkriptleri"),
            bi("CV and cover letter in English", "İngilizce CV ve niyet mektubu"),
            bi("English-test result meeting the published minimum", "Yayımlanmış asgari düzeyi karşılayan İngilizce sınav sonucu"),
            bi("Two recommendation letters submitted by referees through the system", "Referans verenlerin sistem üzerinden yüklediği iki tavsiye mektubu"),
            bi("EUR 100 application fee", "100 EUR başvuru ücreti"),
        ],
        "interview_required": False,
        "verification_notes": bi("The programme FAQ explicitly lists eligible degree areas, required documents, two recommendation letters and no planned admission interview. It also permits final-year applications but requires the degree by the academic-year start.", "Program SSS'si uygun derece alanlarını, gerekli belgeleri, iki tavsiye mektubunu ve planlanmış kabul mülakatı olmadığını açıkça listeler. Ayrıca son sınıf başvurusuna izin verir ancak diplomanın akademik yıl başlangıcında sunulmasını ister."),
    })
    row.setdefault("language_profile", {}).update({
        "teaching_language": ["English"],
        "english_required": True,
        "english_level_required": "TOEFL iBT 87; TOEIC 785 (four skills) or 850 (listening/reading); IELTS Academic 6; CAE/FCE 170; or Linguaskill 170. Test must be less than two years old.",
        "language_risk": "medium",
        "verification_notes": bi("These exact scores and the two-year test-age rule are on the current MAE FAQ. Applicants from specified anglophone citizenships are excepted from the English test; no broader waiver is inferred.", "Bu kesin puanlar ve sınavın iki yıldan eski olmaması kuralı güncel MAE SSS'sindedir. Belirtilen İngilizce konuşulan ülke vatandaşları sınavdan muaftır; daha geniş muafiyet çıkarımı yapılmaz."),
    })
    row.setdefault("cost_profile", {}).update({
        "academic_year": "2026 intake / pages checked 2026-07-14",
        "tuition_eur_per_year_min": None,
        "tuition_eur_per_year_max": None,
        "tuition_eur_per_year_estimated": None,
        "tuition_basis": "unknown_current_total_not_published_on_checked_MAE_page",
        "application_fee_eur": 100,
        "confirmation_deposit_eur": 1200,
        "confirmation_deposit_refundable": False,
        "student_contribution_eur": None,
        "total_academic_cost_eur_per_year_estimated": None,
        "cost_notes": bi("The checked MAE page publishes a EUR 100 application fee and a non-refundable EUR 1,200 deposit payable about three weeks after admission notification to confirm the place. It does not publish a current total MAE tuition amount; no total is invented or borrowed from ISAE-SUPAERO Advanced Master programmes.", "Kontrol edilen MAE sayfası 100 EUR başvuru ücreti ile kabul bildiriminden yaklaşık üç hafta sonra yeri onaylamak için ödenen iadesiz 1.200 EUR depozitoyu yayımlar. Güncel toplam MAE öğrenim ücreti yayımlanmadığı için toplam uydurulmaz veya ISAE-SUPAERO'nun Advanced Master programlarından alınmaz."),
        "verification_notes": bi("The absence of a total is intentional and visible. Deposit is part of tuition but is not presented as the programme's total price.", "Toplam tutarın olmaması kasıtlı ve görünürdür. Depozito öğrenim ücretinin parçasıdır ancak programın toplam fiyatı olarak sunulmaz."),
    })
    row.setdefault("scholarship_profile", {}).update({
        "regional_scholarship_available": True,
        "regional_scholarship_name": "ISAE-SUPAERO excellence scholarships (first application session)",
        "merit_scholarships": [bi("The current MAE FAQ says several excellence scholarships are offered to candidates applying in the first application session. The programme brochure describes Foundation, GIFAS, CEDAR, STAI, MBDA and ESA Academy routes, each with distinct scope; see funding rules before relying on any route.", "Güncel MAE SSS'si ilk başvuru oturumundaki adaylara çeşitli mükemmeliyet bursları sunulduğunu söyler. Program broşürü Foundation, GIFAS, CEDAR, STAI, MBDA ve ESA Academy rotalarını, her biri farklı kapsamla açıklar; herhangi bir rotaya güvenmeden önce finansman kurallarına bakın."),
        ],
        "tuition_waivers": [],
        "non_eu_eligible": None,
        "scholarship_deadline": None,
        "scholarship_application_url": programme_url,
        "funding_competitiveness": "high",
        "funding_notes": bi("The brochure says scholarship applications open in October and November, while the FAQ makes first-session application a condition. It does not publish a current universal deadline or a universal non-EU eligibility rule, so neither is guessed. The ESA Academy item in the brochure is space-major specific; its displayed 2025-2027 cohort must not be assumed to recur automatically.", "Broşür burs başvurularının Ekim ve Kasımda açıldığını, SSS ise ilk oturum başvurusunu koşul yaptığını söyler. Güncel evrensel son tarih veya evrensel AB dışı uygunluk kuralı yayımlamaz; ikisi de tahmin edilmez. Broşürdeki ESA Academy kalemi uzay uzmanlığına özgüdür; gösterilen 2025-2027 dönemi otomatik tekrar edecekmiş gibi varsayılmaz."),
        "verification_notes": bi("Scholarship existence and routes are source-backed, but applicant-specific eligibility, amount and current deadline remain unknown where not published.", "Burs varlığı ve rotaları kaynak desteklidir; ancak başvuru sahibine özgü uygunluk, tutar ve güncel son tarih yayımlanmadığı yerde bilinmiyor kalır."),
    })
    row.setdefault("living_profile", {}).update({
        "city_cost_level": "medium",
        "monthly_living_cost_eur_min": 900,
        "monthly_living_cost_eur_max": 1000,
        "monthly_living_cost_eur_estimated": None,
        "monthly_living_cost_scope_label": bi("ISAE-SUPAERO all-in monthly planning budget", "ISAE-SUPAERO tüm kalemleri içeren aylık planlama bütçesi"),
        "monthly_living_cost_basis": bi("Official MAE FAQ: accommodation, food, transport, health insurance and miscellaneous expenses.", "Resmî MAE SSS'si: konaklama, yemek, ulaşım, sağlık sigortası ve çeşitli giderler."),
        "average_room_rent_eur": None,
        "housing_difficulty": "high",
        "student_housing_available": True,
        "student_housing_competitiveness": "high",
        "living_risk": "medium",
        "housing_sentiment": None,
        "housing_notes": bi("The current MAE page says campus capacity is very limited and international students are prioritised; it does not guarantee a room. Its 2025/26 brochure describes six residences with 1,000 units, but this capacity statement is not used as a personal allocation promise. Campus rooms are individual, with shared kitchens/common areas.", "Güncel MAE sayfası kampüs kapasitesinin çok sınırlı olduğunu ve uluslararası öğrencilere öncelik verildiğini, ancak oda garantisi olmadığını belirtir. 2025/26 broşürü altı yurtta 1.000 birim tanımlar; bu kapasite ifadesi kişisel yer garantisi olarak kullanılmaz. Kampüs odaları bireyseldir, mutfaklar/ortak alanlar paylaşılır."),
        "verification_notes": bi("The EUR 900-1,000 range is an all-in planning budget, not a rent-only amount. No rent-only number is inferred.", "900-1.000 EUR aralığı tüm kalemleri içeren planlama bütçesidir; yalnızca kira tutarı değildir. Kira tutarı çıkarımı yapılmaz."),
    })
    row.setdefault("curriculum_profile", {}).update({
        "tracks": ["advanced_aerodynamics_and_propulsion", "aerospace_structures", "space_systems", "aerospace_systems_and_control", "embedded_systems", "systems_engineering", "space_imaging_navigation_and_communication"],
        "specializations": ["advanced_aerodynamics_and_propulsion", "aerospace_structures", "space_systems", "aerospace_systems_and_control", "embedded_systems", "systems_engineering", "space_imaging_navigation_and_communication"],
        "mandatory_courses": ["Multidisciplinary common core in engineering, management and foreign languages", "One-year part-time research project across semesters 2 and 3", "Final-semester aerospace internship with Master's thesis in a company or laboratory"],
        "elective_courses": ["19 aerospace-field electives in semester 2", "Major selection in semester 3"],
        "thesis_required": True,
        "internship_required": True,
        "curriculum_url": brochure_url,
        "curriculum_structure": bi("The December 2025 MAE brochure describes three taught semesters plus a final semester internship/thesis, 120 credits total, a one-year part-time research project across semesters 2-3, 19 semester-2 electives and seven semester-3 majors. It is programme-specific evidence, not a guarantee that every elective runs each year.", "Aralık 2025 MAE broşürü üç eğitim dönemi ile son dönemde staj/tez, toplam 120 AKTS, 2-3. yarıyıllara yayılan bir yıllık yarı zamanlı araştırma projesi, ikinci yarıyılda 19 seçmeli ve üçüncü yarıyılda yedi uzmanlaşma tanımlar. Bu programa özgü kanıttır; her seçmelinin her yıl açılacağı garantisi değildir."),
    })
    row.setdefault("category_profile", {}).update({
        "primary_categories": ["aerospace_engineering"],
        "secondary_categories": ["aerodynamics", "propulsion", "aerospace_structures", "space_systems", "gnc", "embedded_systems", "systems_engineering", "satellite_communications"],
        "normalized_tags": ["advanced_aerodynamics", "aerospace_propulsion", "aerospace_structures", "spacecraft_systems", "gnc", "embedded_systems", "systems_engineering", "satellite_imaging", "satellite_communications"],
    })
    row.setdefault("research_profile", {}).update({
        "department_research_areas": ["Integrated design and operational safety of aerospace systems", "Energy efficiency and aerospace-system optimisation", "Earth observation, environmental monitoring and space exploration", "Resilient telecommunications and connected cyber-physical systems", "Data analysis, decision sciences and complexity"],
        "labs": ["ISAE-SUPAERO Research", "ONERA Toulouse research centre (on campus)", "SSPA — Space Systems for Planetology and Applications", "DAEP — Aerodynamics, Energetics and Propulsion", "DISC — Complex Systems Engineering"],
        "research_centers": ["ONERA Toulouse research centre", "Institut Clément Ader (ICA)"],
        "research_strength_summary": bi("ISAE-SUPAERO's current research page documents six research departments, around 400 people in its laboratories and a 400-person ONERA Toulouse centre on campus. Its stated priorities include Earth observation, space exploration, resilient telecoms and aerospace systems. For direct space depth, SSPA develops missions and technologies for geophysical exploration of the solar system; this is concrete research evidence rather than a prestige-only label.", "ISAE-SUPAERO'nun güncel araştırma sayfası altı araştırma bölümü, laboratuvarlarında yaklaşık 400 kişi ve kampüste 400 kişilik ONERA Toulouse merkezini belgeler. Belirtilen öncelikleri Dünya gözlemi, uzay keşfi, dayanıklı haberleşme ve havacılık-uzay sistemleridir. Doğrudan uzay derinliği için SSPA, Güneş Sistemi'nin jeofizik keşfi için görevler ve teknolojiler geliştirir; bu, yalnızca itibar etiketi değil somut araştırma kanıtıdır."),
        "research_strength_score": None,
        "research_sources": [research_url, space_research_url],
    })
    row.setdefault("industry_ecosystem_profile", {}).update({
        "nearby_companies": [],
        "confirmed_partners": ["ISAE-SUPAERO's MAE brochure lists institutional partnerships including Airbus, Dassault Aviation, Safran, Thales, MBDA, ArianeGroup and Eutelsat"],
        "research_institutes": ["ONERA Toulouse research centre", "Institut Clément Ader (ICA)"],
        "ecosystem_notes": bi("The December 2025 MAE brochure lists 35 partnerships and named aerospace/technology organisations. This is recorded as institute-level ecosystem evidence, not a promise that every MAE student is placed with one of these organisations. The final internship/thesis is explicitly undertaken in an aerospace company or laboratory.", "Aralık 2025 MAE broşürü 35 ortaklığı ve isimli havacılık-uzay/teknoloji kuruluşlarını listeler. Bu, her MAE öğrencisinin bu kuruluşlardan birine yerleştirileceği sözü değil, enstitü düzeyinde ekosistem kanıtı olarak kaydedilir. Son staj/tez açıkça bir havacılık-uzay şirketinde veya laboratuvarda yapılır."),
        "ecosystem_strength_score": None,
    })
    row["application_timeline_profile"] = {
        "academic_year": "2027 intake",
        "intake_terms": ["late August / September"],
        "application_rounds": ["2027 academic-year applications open October 2026; closing date not published on checked page"],
        "non_eu_deadline": None,
        "eu_deadline": None,
        "winter_deadline": None,
        "summer_deadline": None,
        "application_deadline": None,
        "scholarship_deadline": None,
        "timeline_risk": "high",
        "deadline_notes": bi("The current MAE page says the 2026 intake is closed and applications open in October 2026 for the 2027 academic year. It does not publish an exact closing date, application-session dates, or a separate non-EU deadline; the record refuses to invent them.", "Güncel MAE sayfası 2026 girişinin kapandığını ve 2027 akademik yılı başvurularının Ekim 2026'da açılacağını belirtir. Kesin kapanış tarihi, başvuru oturumu tarihleri veya ayrı AB dışı son tarih yayımlamaz; kayıt bunları uydurmaz."),
    }
    row["student_sentiment_profile"] = {"student_satisfaction_score": None, "sentiment_confidence": "unknown", "sample_size_estimate": None, "date_range": "", "student_sentiment_sources": [], "student_sentiment_summary": bi("No sufficiently documented, independent student-sentiment sample was retained; no sentiment score is shown.", "Yeterince belgelenmiş bağımsız öğrenci görüşü örneklemi tutulmadı; duygu puanı gösterilmez."), "verification_notes": bi("Student sentiment remains separate from official facts and is not fabricated to fill the card.", "Öğrenci görüşleri resmî bilgilerden ayrı tutulur ve kartı doldurmak için uydurulmaz.")}
    row["decision_summary"] = {
        "main_strengths": [bi("A genuinely broad but structured aerospace MSc: seven named majors, 19 second-semester aerospace electives, a year-long part-time research project, then a final-semester company-or-lab internship/thesis.", "Gerçekten geniş ama yapılandırılmış bir havacılık-uzay MSc: yedi isimli uzmanlaşma, ikinci yarıyılda 19 havacılık-uzay seçmelisi, bir yıllık yarı zamanlı araştırma projesi ve ardından şirket veya laboratuvar stajı/tezi."), bi("Direct space value is unusually clear: Space Systems and Space Imaging Navigation and Communication majors, SSPA space-mission research, and an on-campus ONERA Toulouse research centre.", "Doğrudan uzay değeri olağanüstü nettir: Space Systems ile Space Imaging Navigation and Communication uzmanlaşmaları, SSPA uzay-görevi araştırması ve kampüste ONERA Toulouse araştırma merkezi."),
        ],
        "main_risks": [bi("This is selective: panel review, a EUR 100 application fee, two referee-submitted recommendations and exact English scores apply. The EUR 1,200 confirmation deposit is non-refundable.", "Bu seçici bir programdır: komite değerlendirmesi, 100 EUR başvuru ücreti, referans verenlerin yüklediği iki tavsiye ve kesin İngilizce puanları uygulanır. 1.200 EUR kayıt onay depozitosu iade edilmez."), bi("Do not budget a made-up tuition total. The official MAE page does not publish a current total fee; it only exposes the application fee and deposit. The all-in living budget is EUR 900-1,000/month and campus rooms are limited, though international students are prioritised.", "Uydurulmuş bir toplam öğrenim ücretiyle bütçe yapmayın. Resmî MAE sayfası güncel toplam ücreti yayımlamaz; yalnızca başvuru ücreti ve depozitoyu gösterir. Tüm kalemleri içeren yaşam bütçesi ayda 900-1.000 EUR'dur ve uluslararası öğrencilere öncelik verilse de kampüs odaları sınırlıdır."), bi("The 2027 application is only announced to open in October 2026; a closing date and scholarship deadline are not published yet. Treat these as an active monitoring item rather than an assumed November deadline.", "2027 başvurusunun yalnızca Ekim 2026'da açılacağı duyurulmuştur; kapanış tarihi ve burs son tarihi henüz yayımlanmamıştır. Bunları varsayılan Kasım son tarihi değil aktif takip kalemi olarak ele alın."),
        ],
        "best_for": [bi("Applicants wanting both aerospace breadth and an actual final-semester aerospace company/lab thesis placement, especially those considering Space Systems, GNC, imaging/navigation or propulsion.", "Özellikle Space Systems, GNC, görüntüleme/navigasyon veya itki düşünen; hem havacılık-uzay genişliği hem gerçek son dönem şirket/laboratuvar tezi isteyen adaylar.")],
        "not_ideal_for": [bi("Applicants who need a fully published current tuition total or a confirmed application closing date before October 2026.", "Ekim 2026'dan önce tam yayımlanmış güncel öğrenim ücreti toplamına veya onaylanmış başvuru kapanış tarihine ihtiyaç duyan adaylar.")],
    }
    row["financials"] = {"tuition_fee_per_year": None, "semester_fee": None, "application_fee": 100, "confirmation_deposit": 1200}
    row["scholarships_info"] = []
    row["admission"] = {"requirements": {"minimum_gpa": None, "minimum_gpa_notes": "unknown", "required_ects": None, "language_requirements": "See language_profile for current published MAE scores."}}
    row["source_profile"] = {
        "official_program_page": programme_url, "official_admission_page": programme_url, "official_curriculum_page": brochure_url, "official_tuition_page": programme_url, "official_scholarship_page": programme_url, "official_housing_page": programme_url, "official_department_page": research_url,
        "source_log": [
            source(programme_url, "ISAE-SUPAERO Master's Degree in Aerospace Engineering", "official_program_page", ["program", "language", "admission", "non_eu", "documents", "fees", "scholarship", "housing", "living", "deadline"], "Current programme page documents MAE's English delivery, active two-year degree, degree backgrounds, application documents, English tests, application fee, non-refundable deposit, scholarship existence, monthly living budget, limited housing and October 2026 opening for 2027 applications.", "Güncel program sayfası MAE'nin İngilizce eğitimini, aktif iki yıllık derecesini, kabul edilen diploma altyapılarını, başvuru belgelerini, İngilizce sınavlarını, başvuru ücretini, iadesiz depozitoyu, burs varlığını, aylık yaşam bütçesini, sınırlı konaklamayı ve 2027 başvuruları için Ekim 2026 açılışını belgeler."),
            source(programme_url, "ISAE-SUPAERO MAE living-cost guidance", "official_cost_of_living_page", ["living", "housing"], "The official MAE FAQ gives a EUR 900-1,000 monthly all-in planning budget covering accommodation, food, transport, health insurance and miscellaneous expenses. It is retained as a total living-cost range, not a rent estimate.", "Resmî MAE SSS'si konaklama, yemek, ulaşım, sağlık sigortası ve çeşitli giderleri kapsayan aylık 900-1.000 EUR tüm kalemleri içeren planlama bütçesi verir. Bu tutar kira tahmini değil, toplam yaşam gideri aralığı olarak tutulur."),
            source(programme_url, "ISAE-SUPAERO MAE campus accommodation", "official_housing_page", ["housing"], "The official MAE FAQ says campus capacity is very limited and international students are prioritised; it does not guarantee a room. Individual rooms have shared kitchens and common areas.", "Resmî MAE SSS'si kampüs kapasitesinin çok sınırlı olduğunu ve uluslararası öğrencilere öncelik verildiğini belirtir; oda garantisi vermez. Odalar bireyseldir; mutfak ve ortak alanlar paylaşılır."),
            source(programme_url, "ISAE-SUPAERO MAE Funding Assistance", "official_scholarship_page", ["scholarship"], "The official MAE funding section says several excellence scholarships are offered to candidates applying in the first application session. The record retains that existence only; it does not claim a universal amount, current deadline or non-EU eligibility where the page does not publish them.", "Resmî MAE finansman bölümü ilk başvuru oturumundaki adaylara çeşitli mükemmeliyet bursları sunulduğunu söyler. Kayıt yalnızca bu varlığı tutar; sayfanın yayımlamadığı evrensel tutar, güncel son tarih veya AB dışı uygunluğu ileri sürmez."),
            source(brochure_url, "ISAE-SUPAERO MAE 2026 Brochure", "official_curriculum_page", ["program", "curriculum", "research", "industry", "scholarship", "housing"], "Official December 2025 brochure gives the 120-credit/three-course-semester plus internship-thesis structure, seven majors, research project, partner ecosystem, residence capacity and scope of scholarship routes. It is used with its edition date, not as an unchanging future course guarantee.", "Resmî Aralık 2025 broşürü 120 AKTS/üç ders dönemi artı staj-tez yapısını, yedi uzmanlaşmayı, araştırma projesini, ortak ekosistemini, yurt kapasitesini ve burs rotalarının kapsamını verir. Baskı tarihiyle birlikte kullanılır; değişmeyecek gelecek ders garantisi olarak değil."),
            source(research_url, "ISAE-SUPAERO Research", "official_department_page", ["research"], "Current research page documents ISAE-SUPAERO's six research departments, on-campus ONERA Toulouse centre, strategic aerospace/space priorities and research-access statement for students.", "Güncel araştırma sayfası ISAE-SUPAERO'nun altı araştırma bölümünü, kampüsteki ONERA Toulouse merkezini, stratejik havacılık-uzay önceliklerini ve öğrenciler için araştırma erişimi ifadesini belgeler."),
            source(space_research_url, "ISAE-SUPAERO SSPA Space Systems Research Group", "official_lab_page", ["research"], "Current SSPA page documents mission and technology development for solar-system geophysical exploration, including future missions and instrument/data work.", "Güncel SSPA sayfası gelecek görevler ile araç/veri çalışmaları dahil Güneş Sistemi jeofizik keşfi için görev ve teknoloji geliştirmeyi belgeler."),
        ],
        "last_verified": CHECKED, "needs_verification": True,
        "verification_notes": bi("All displayed programme, admission, language, deposit, living, housing, curriculum, research and industry facts are official and checked. The current total tuition, exact 2027 closing date and scholarship deadline are not published in the checked sources and remain unknown rather than fabricated.", "Gösterilen program, kabul, dil, depozito, yaşam, konaklama, müfredat, araştırma ve sanayi bilgilerinin tümü resmî ve kontrol edilmiştir. Güncel toplam öğrenim ücreti, kesin 2027 kapanış tarihi ve burs son tarihi kontrol edilen kaynaklarda yayımlanmadığı için uydurulmak yerine bilinmiyor kalır."),
        "field_confidence": {"program_basic_info": "high", "language": "high", "admission": "high", "tuition": "unknown", "scholarship": "medium", "curriculum": "high", "research_profile": "high", "industry_ecosystem_profile": "high", "application_timeline_profile": "medium", "living_profile": "high", "housing": "high", "deadlines": "unknown"},
    }
    document["last_updated"] = CHECKED
    newline = "\r\n" if "\r\n" in original else "\n"
    PATH.write_text(json.dumps(document, ensure_ascii=False, indent=2).replace("\n", newline) + newline, encoding="utf-8")
    print("Updated ISAE-SUPAERO MAE with source-checked evidence and explicit unknowns.")


if __name__ == "__main__":
    main()
