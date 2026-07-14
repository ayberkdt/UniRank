"""Make the UniPi Space Engineering card explicit about fee year and course depth."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from apply_verified_polimi_aero_update import bi, source


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data_base" / "italy.json"
CHECKED = "2026-07-14"


def main() -> None:
    original = PATH.read_text(encoding="utf-8")
    document: dict[str, Any] = json.loads(original)
    row = next(item for item in document["universities"] if item.get("id") == "unipi_aerospace_master")

    programme_url = "https://msse.ing.unipi.it/"
    aerospace_url = "https://www.unipi.it/en/education/courses/master-degree/aerospace-engineering-wiar-lm-en/"
    plan_url = "https://msse.ing.unipi.it/plan-of-studies/"
    tuition_url = "https://msse.ing.unipi.it/tuition-and-expenses/"
    fee_rules_url = "https://www.unipi.it/en/education/registration/fees/tuition-fees-for-degree-courses/"

    row.update({
        "program_name": "Master of Science in Space Engineering (MSSE)",
        "program_native_name": "Laurea Magistrale in Ingegneria Aerospaziale, curriculum Space Engineering",
        "program_degree": "Master of Science in Aerospace Engineering, Space Engineering curriculum",
        "degree_level": "Master",
        "degree_class": "Laurea Magistrale / MSc",
        "duration_years": 2,
        "ects": 120,
        "teaching_language": ["English"],
        "program_url": programme_url,
        "department": "University of Pisa, Department of Civil and Industrial Engineering, Aerospace Engineering Section",
        "campus": "Pisa",
        "program_status": "active",
        "relevance_status": "strong",
    })
    row["cost_profile"] = {
        "academic_year": "2025/2026 official reference; 2026/2027 annual fees not yet published on the checked MSSE page",
        "tuition_eur_per_year_min": 390,
        "tuition_eur_per_year_max": 2900,
        "tuition_eur_per_year_estimated": None,
        "tuition_basis": "official_2025_26_country_of_origin_range_not_extrapolated",
        "isee_or_income_based": True,
        "regional_tax_eur": None,
        "student_contribution_eur": None,
        "application_fee_eur": None,
        "enrollment_fee_eur": None,
        "total_academic_cost_eur_per_year_estimated": None,
        "payment_installments": "The general University of Pisa fee page states that payment is divided into four instalments for the income/assets-abroad contribution.",
        "source_notes": bi("The MSSE page states that 2025/26 University fees ranged from EUR 390 to EUR 2,900/year depending on country of origin. It also says fees are set annually and usually announced in June for the following academic year. The current checked page has not published a 2026/27 range, so no current fee is fabricated.", "MSSE sayfası, 2025/26 Üniversite ücretlerinin ülke menşeine göre yıllık 390 EUR ile 2.900 EUR arasında olduğunu söyler. Ayrıca ücretlerin her yıl belirlendiğini ve genellikle sonraki akademik yıl için Haziran'da açıklandığını belirtir. Kontrol edilen güncel sayfa 2026/27 aralığını yayımlamadığı için güncel ücret uydurulmaz."),
        "verification_notes": bi("The card deliberately labels this as a prior published reference, not as a 2026/27 promise. International-income fee rules and exemptions are available on the University fee page; use the new annual table before paying or comparing affordability.", "Kart bunu 2026/27 taahhüdü değil, önceki yayımlanmış referans olarak açıkça etiketler. Uluslararası gelir ücreti kuralları ve muafiyetler Üniversite ücret sayfasındadır; ödeme veya karşılanabilirlik karşılaştırması öncesinde yeni yıllık tabloyu kullanın."),
    }
    row["living_profile"] = {
        "city_cost_level": "medium",
        "monthly_living_cost_eur_min": None,
        "monthly_living_cost_eur_max": None,
        "monthly_living_cost_eur_estimated": 567,
        "monthly_living_cost_scope_label": bi("UniPi MSSE official annual living budget divided by 12; not a current rent quote", "UniPi MSSE resmî yıllık yaşam bütçesinin 12'ye bölünmüş hâli; güncel kira teklifi değildir"),
        "monthly_living_cost_basis": bi("The MSSE page publishes a roughly EUR 6,800 yearly student budget (EUR 4,200 accommodation/utilities, EUR 1,800 food at student dining facilities, EUR 300 books/supplies and EUR 500 health/dental). EUR 567 is the transparent EUR 6,800/12 arithmetic, not a separately quoted monthly total.", "MSSE sayfası yaklaşık 6.800 EUR yıllık öğrenci bütçesi yayımlar (4.200 EUR konaklama/faturalar, öğrenci yemekhanelerinde 1.800 EUR yemek, 300 EUR kitap/malzeme ve 500 EUR sağlık/diş). 567 EUR, ayrı yayımlanmış aylık toplam değil, şeffaf 6.800/12 hesabıdır."),
        "average_room_rent_eur": 350,
        "average_room_rent_eur_min": None,
        "average_room_rent_eur_max": None,
        "average_room_rent_scope_label": bi("UniPi MSSE official single-room planning component, accommodation and utilities", "UniPi MSSE resmî tek kişilik oda planlama kalemi, konaklama ve faturalar"),
        "food_cost_eur_month": 150,
        "student_housing_available": None,
        "student_housing_competitiveness": "high",
        "housing_difficulty": "medium",
        "living_risk": "medium",
        "housing_sentiment": None,
        "housing_notes": bi("UniPi's MSSE page budgets EUR 350/month for a single room including utilities and says the University maintains a listing of available rooms, apartments and houses. It is an official planning figure and listing service, not a University-owned housing guarantee.", "UniPi'nin MSSE sayfası faturalar dahil tek kişilik oda için ayda 350 EUR bütçeler ve Üniversitenin mevcut oda, daire ve ev listesini tuttuğunu söyler. Bu resmî planlama tutarı ve liste hizmetidir; Üniversiteye ait konaklama garantisi değildir."),
        "verification_notes": bi("The all-in planning budget is published on the MSSE page but is explicitly described as rough and lifestyle-dependent. It is kept separate from the fee record and from a guaranteed housing price.", "Tüm kalemleri içeren planlama bütçesi MSSE sayfasında yayımlanır ancak açıkça yaklaşık ve yaşam tarzına bağlı olarak tanımlanır. Ücret kaydından ve garantili konaklama fiyatından ayrı tutulur."),
    }
    row["curriculum_profile"] = {
        "tracks": ["space_engineering"],
        "specializations": ["spacecraft_structures", "spaceflight_mechanics", "spacecraft_dynamics_and_control", "spacecraft_technology", "propulsion", "space_systems", "electric_propulsion", "earth_observation", "space_communications"],
        "mandatory_courses": ["Aerospace Structures", "Spaceflight Mechanics", "Aerospace Dynamic Systems Analysis", "Dinamica e controllo di veicoli aerospaziali", "Fundamentals of Spacecraft Technology", "Fluid Dynamics of Propulsion Systems I", "Spacecraft Structures and Mechanisms", "Rocket Propulsion", "Space Systems"],
        "elective_courses": ["Electric Propulsion I", "Electric Propulsion II", "Remote Sensing for Earth Observation", "Space Communication Systems"],
        "course_language_notes": bi("The MSSE curriculum is English-taught. One listed required course keeps its Italian title on the official plan; the programme's official home page states the programme is taught in English.", "MSSE müfredatı İngilizce okutulur. Listelenen zorunlu derslerden biri resmî planda İtalyanca başlığını korur; programın resmî ana sayfası programın İngilizce okutulduğunu belirtir."),
        "thesis_required": True,
        "thesis_ects": 24,
        "internship_required": None,
        "lab_courses": [],
        "project_based_courses": ["Final Project / substantial original research thesis"],
        "mobility_options": ["Erasmus+"],
        "double_degree_options": [],
        "curriculum_url": plan_url,
        "study_plan_url": plan_url,
        "curriculum_structure": bi("The published 2025/26 plan is unusually explicit: 84 ECTS required courses, 12 ECTS approved electives and 24 ECTS thesis. Its technical spine is structures, orbital/spaceflight mechanics, dynamics and control, spacecraft technology, propulsion and space systems. The elective choice lets a student tilt toward electric propulsion, Earth observation or space communications, subject to plan approval for non-standard selections.", "Yayımlanan 2025/26 planı olağandışı derecede açıktır: 84 AKTS zorunlu ders, 12 AKTS onaylı seçmeli ve 24 AKTS tez. Teknik omurga yapılar, yörünge/uzay uçuş mekaniği, dinamik ve kontrol, uzay aracı teknolojisi, itki ve uzay sistemleridir. Seçmeli seçim, standart dışı planlar için kurul onayına bağlı olarak öğrencinin elektrikli itki, Dünya gözlemi veya uzay haberleşmesine yönelmesini sağlar."),
        "verification_notes": bi("Course titles and ECTS are from the official 2025/26 plan. The 2026/27 detailed plan was not published on the checked page, so the card shows the plan year and does not pretend that every elective will recur unchanged.", "Ders adları ve AKTS'ler resmî 2025/26 planındandır. 2026/27 ayrıntılı planı kontrol edilen sayfada yayımlanmadığı için kart plan yılını gösterir ve her seçmelinin değişmeden tekrar açılacağını iddia etmez."),
    }
    row["category_profile"] = {
        "primary_categories": ["space_systems", "spacecraft_systems"],
        "secondary_categories": ["orbital_mechanics", "gnc", "spacecraft_structures", "rocket_propulsion", "electric_propulsion", "remote_sensing", "space_communications"],
        "normalized_tags": ["space_engineering", "spacecraft_systems", "orbital_mechanics", "spacecraft_control", "spacecraft_structures", "rocket_propulsion", "electric_propulsion", "earth_observation", "satellite_communications"],
    }
    row["decision_summary"] = {
        "main_strengths": [bi("This is a genuinely space-specific English MSc, not a generic aerospace label: the published core includes spaceflight mechanics, spacecraft dynamics/control, spacecraft technology, rocket propulsion and space systems, then permits a deliberate electric-propulsion, Earth-observation or communications tilt.", "Bu, genel bir havacılık/uzay etiketi değil, gerçekten uzaya özgü İngilizce MSc'dir: yayımlanan çekirdek uzay uçuş mekaniği, uzay aracı dinamiği/kontrolü, uzay aracı teknolojisi, roket itkisi ve uzay sistemlerini içerir; ardından bilinçli olarak elektrikli itki, Dünya gözlemi veya haberleşme yönelimine izin verir."), bi("The card distinguishes a specific official planning budget from vague city claims: roughly EUR 6,800/year is published with components, including EUR 350/month for a single room with utilities.", "Kart, belirli resmî planlama bütçesini belirsiz şehir iddialarından ayırır: bileşenleriyle yaklaşık 6.800 EUR/yıl yayımlanır; buna faturalar dahil tek kişilik oda için ayda 350 EUR dahildir.")],
        "main_risks": [bi("The only checked fee range is EUR 390-2,900 for 2025/26. UniPi says annual fees are set each year; do not use it as a 2026/27 quotation until the new table is published.", "Kontrol edilen tek ücret aralığı 2025/26 için 390-2.900 EUR'dur. UniPi, yıllık ücretlerin her yıl belirlendiğini söyler; yeni tablo yayımlanana kadar bunu 2026/27 teklifi olarak kullanmayın."), bi("The detailed plan is also 2025/26. It is excellent evidence of technical depth, but elective availability and the next-cycle plan must be checked before application or course choice.", "Ayrıntılı plan da 2025/26'ya aittir. Teknik derinliğin mükemmel kanıtıdır, ancak seçmeli uygunluğu ve sonraki döngü planı başvuru veya ders seçiminden önce kontrol edilmelidir."), bi("The 2026 non-EU application deadline (3 May) had already passed when checked. Future non-EU applicants should not rely on it as a standing May deadline.", "2026 AB dışı başvuru son tarihi (3 Mayıs) kontrol edildiğinde geçmişti. Gelecekteki AB dışı adaylar bunu sabit Mayıs son tarihi olarak görmemelidir.")],
        "best_for": [bi("English-speaking applicants targeting spacecraft systems, orbital mechanics, GNC, structures, chemical/electric propulsion, Earth observation or satellite communications, and who can verify the upcoming annual fees before committing.", "Uzay aracı sistemleri, yörünge mekaniği, GNC, yapılar, kimyasal/elektrikli itki, Dünya gözlemi veya uydu haberleşmesini hedefleyen ve taahhüt vermeden önce gelecek yıllık ücretleri doğrulayabilen İngilizce yeterlikli adaylar.")],
        "not_ideal_for": [bi("Applicants who need a guaranteed current tuition quote today, a fully fixed no-elective plan, or a programme centered on aircraft design rather than spacecraft engineering.", "Bugün garantili güncel öğrenim ücreti teklifi, seçmelisiz tamamen sabit plan veya uzay aracı mühendisliği yerine uçak tasarımı merkezli program isteyen adaylar.")],
    }
    profile = row.setdefault("source_profile", {})
    profile.update({
        "official_program_page": programme_url,
        "official_curriculum_page": plan_url,
        "official_tuition_page": tuition_url,
        "official_cost_of_living_page": tuition_url,
        "last_verified": CHECKED,
        "needs_verification": False,
        "verification_notes": bi("All displayed programme, curriculum, living-budget and fee-reference facts have accessible official sources. The currency range and course plan are explicitly scoped to their published academic years rather than silently upgraded to 2026/27.", "Gösterilen tüm program, müfredat, yaşam bütçesi ve ücret referansı bilgileri erişilebilir resmî kaynaklara sahiptir. Ücret aralığı ve ders planı 2026/27'ye sessizce yükseltilmek yerine yayımlandıkları akademik yıllarla açıkça sınırlandırılır."),
        "field_confidence": {"program_basic_info": "high", "language": "high", "admission": "medium", "tuition": "medium", "scholarship": "high", "curriculum": "high", "research_profile": "high", "industry_ecosystem_profile": "medium", "application_timeline_profile": "medium", "living_profile": "medium", "housing": "medium", "deadlines": "medium"},
    })
    logs = [item for item in profile.get("source_log", []) if isinstance(item, dict) and item.get("url") not in {programme_url, aerospace_url, plan_url, tuition_url, fee_rules_url}]
    logs.extend([
        source(programme_url, "UniPi Master of Science in Space Engineering", "official_program_page", ["program", "language", "admission", "non_eu", "deadline", "research"], "Current programme page confirms the active two-year/120-ECTS English space-engineering MSc, prerequisites, current 2026 cycle and the option to complete a thesis at University, research-centre or industry sites.", "Güncel program sayfası aktif iki yıllık/120 AKTS İngilizce uzay mühendisliği MSc'sini, ön koşulları, mevcut 2026 döngüsünü ve tezin Üniversite, araştırma merkezi veya sanayi tesislerinde yapılabilmesi seçeneğini doğrular."),
        source(aerospace_url, "University of Pisa Aerospace Engineering MSc", "official_program_page", ["program", "curriculum", "admission", "industry"], "Current University course page confirms that the Space Engineering curriculum is the English MSSE route within Aerospace Engineering and that thesis research can be carried out through collaboration agreements with external institutions.", "Güncel Üniversite ders sayfası, Space Engineering müfredatının Aerospace Engineering içindeki İngilizce MSSE rotası olduğunu ve tez araştırmasının dış kurumlarla işbirliği anlaşmaları yoluyla yapılabileceğini doğrular."),
        source(plan_url, "UniPi MSSE plan of studies", "official_curriculum_page", ["curriculum", "courses", "thesis"], "Official 2025/26 plan gives the 84 required / 12 elective / 24 thesis ECTS structure, core course titles, elective options and substantial original-research thesis requirement.", "Resmî 2025/26 planı 84 zorunlu / 12 seçmeli / 24 tez AKTS yapısını, çekirdek ders başlıklarını, seçmeli seçeneklerini ve önemli özgün araştırma tezi gereğini verir."),
        source(tuition_url, "UniPi MSSE tuition and expenses", "official_tuition_page", ["tuition", "fees"], "Official MSSE page gives the EUR 390-2,900 2025/26 annual fee range by country of origin and says fees are set annually, usually announced in June for the following year.", "Resmî MSSE sayfası ülke menşeine göre yıllık 390-2.900 EUR 2025/26 ücret aralığını verir ve ücretlerin her yıl belirlendiğini, genellikle sonraki yıl için Haziran'da duyurulduğunu söyler.", "medium"),
        source(tuition_url, "UniPi MSSE living expenses", "official_cost_of_living_page", ["living", "housing"], "Official MSSE page publishes a rough EUR 6,800 annual living budget with a EUR 350/month single-room-plus-utilities component; it labels the figures lifestyle-dependent.", "Resmî MSSE sayfası 350 EUR/ay tek kişilik oda+fatura kalemini içeren yaklaşık 6.800 EUR yıllık yaşam bütçesi yayımlar; tutarları yaşam tarzına bağlı olarak etiketler.", "medium"),
        source(fee_rules_url, "University of Pisa tuition fee rules", "official_tuition_page", ["tuition", "fees", "scholarship"], "Official University page documents the 2025/26 international-income/assets contribution framework, four instalments, maximum EUR 2,900 annual contribution, regional-tax context and named full exemptions.", "Resmî Üniversite sayfası 2025/26 uluslararası gelir/varlık katkı çerçevesini, dört taksiti, azami 2.900 EUR yıllık katkıyı, bölgesel vergi bağlamını ve isimli tam muafiyetleri belgeler.", "medium"),
    ])
    profile["source_log"] = logs
    document["last_updated"] = CHECKED
    newline = "\r\n" if "\r\n" in original else "\n"
    PATH.write_text(json.dumps(document, ensure_ascii=False, indent=2).replace("\n", newline) + newline, encoding="utf-8")
    print("Updated UniPi MSSE with scoped official fee, living-cost and curriculum evidence.")


if __name__ == "__main__":
    main()
