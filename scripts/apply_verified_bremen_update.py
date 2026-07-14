"""Add current decision data for the University of Bremen Space Engineering MSc."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data_base" / "almanya.json"
CHECKED = "2026-07-14"


def bi(en: str, tr: str) -> dict[str, str]:
    return {"en": en, "tr": tr}


def source(url: str, title: str, source_type: str, fields: list[str], en: str, tr: str, confidence: str = "high") -> dict[str, Any]:
    return {
        "url": url,
        "title": title,
        "source_type": source_type,
        "access_status": "ok",
        "last_checked": CHECKED,
        "relevant_fields": fields,
        "confidence": confidence,
        "notes": bi(en, tr),
    }


def add_source(row: dict[str, Any], entry: dict[str, Any]) -> None:
    profile = row.setdefault("source_profile", {})
    log = [item for item in profile.get("source_log", []) if isinstance(item, dict)]
    log = [item for item in log if (item.get("url"), item.get("source_type")) != (entry["url"], entry["source_type"])]
    log.append(entry)
    profile["source_log"] = log
    profile["last_verified"] = CHECKED


def main() -> None:
    original = PATH.read_text(encoding="utf-8")
    rows: list[dict[str, Any]] = json.loads(original)
    row = next(item for item in rows if item.get("id") == "de_bremen_space_engineering_msc")

    programme_url = "https://www.uni-bremen.de/en/studies/orientation-application/offered-study-program/dbs/study/space-engineering-master"
    preparation_url = "https://www.uni-bremen.de/en/studies/starting-your-studies/international-students/offers-for-international-students/preparation-from-abroad"
    scholarship_url = "https://www.uni-bremen.de/en/deutschlandstipendiat/"
    scholarship_faq_url = "https://www.uni-bremen.de/en/deutschlandstipendiat/faq"
    housing_url = "https://www.stw-bremen.de/en/accommodation/"
    housing_faq_url = "https://www.stw-bremen.de/en/faqs/accommodation/"
    non_eu_application_url = "https://www.uni-bremen.de/en/studies/orientation-application/applying-for-studies/applications-from-abroad/applications-non-eu"

    row["cost_profile"].update({
        "academic_year": "current official pages checked 2026-07-14",
        "tuition_eur_per_year_min": 0,
        "tuition_eur_per_year_max": 0,
        "tuition_eur_per_year_estimated": 0,
        "tuition_basis": "no_general_tuition_regular_programme",
        "student_contribution_eur": 425,
        "total_academic_cost_eur_per_year_estimated": None,
        "source_notes": bi(
            "The University of Bremen states that it does not charge tuition fees. The Space Engineering programme page lists an approximate EUR 425 semester fee including the semester ticket; this is not tuition and can change.",
            "Bremen Üniversitesi öğrenim ücreti almadığını belirtir. Uzay Mühendisliği program sayfası dönem bileti dahil yaklaşık 425 EUR dönem ücreti listeler; bu öğrenim ücreti değildir ve değişebilir.",
        ),
        "verification_notes": bi(
            "Zero means no general tuition, not a zero-cost degree: the semester fee and living costs remain separate.",
            "Sıfır, genel öğrenim ücreti olmadığı anlamına gelir; sıfır maliyetli derece anlamına gelmez: dönem ücreti ve yaşam giderleri ayrıdır.",
        ),
    })
    row["scholarship_profile"].update({
        "regional_scholarship_available": True,
        "regional_scholarship_name": "Deutschlandstipendium at the University of Bremen",
        "merit_scholarships": [bi(
            "Deutschlandstipendium at the University of Bremen: EUR 300 per month, about 100 awards each winter semester. The 2026/27 application window is 1 July–15 August 2026; applicants for a Master's place may submit admission/enrolment confirmation by 15 September.",
            "Bremen Üniversitesi Deutschlandstipendium: her kış döneminde yaklaşık 100 ödül, ayda 300 EUR. 2026/27 başvuru dönemi 1 Temmuz–15 Ağustos 2026'dır; yüksek lisans yeri adayları kabul/kayıt belgesini 15 Eylül'e kadar sunabilir.",
        )],
        "non_eu_eligible": True,
        "scholarship_deadline": "2026-08-15 (Deutschlandstipendium 2026/27)",
        "scholarship_application_url": scholarship_url,
        "funding_competitiveness": "high",
        "funding_notes": bi(
            "The University administers a current Deutschlandstipendium call for regular students and prospective Bachelor's, Master's and law students. All nationalities may apply, but selection is competitive and other talent/performance support above EUR 30/month can exclude simultaneous funding.",
            "Üniversite düzenli öğrenciler ile lisans, yüksek lisans ve hukuk programı adayları için güncel Deutschlandstipendium çağrısı yürütür. Tüm uyruklar başvurabilir; ancak seçim rekabetçidir ve ayda 30 EUR üzerindeki başka yetenek/başarı destekleri eşzamanlı finansmanı engelleyebilir.",
        ),
    })
    row["eligibility_profile"].update({
        "eligible_for_non_eu": True,
        "verification_notes": bi(
            "The current University of Bremen non-EU application page confirms a graduate-programme application route for non-EU applicants and directs Master's applicants to the programme-specific master's application pages.",
            "Güncel Bremen Üniversitesi AB dışı başvuru sayfası, AB dışı adaylar için yüksek lisans başvuru yolunu doğrular ve yüksek lisans adaylarını programa özgü yüksek lisans başvuru sayfalarına yönlendirir.",
        ),
    })
    row["living_profile"].update({
        "city_cost_level": "medium",
        "monthly_living_cost_eur_min": 992,
        "monthly_living_cost_eur_max": None,
        "monthly_living_cost_eur_estimated": None,
        "monthly_living_cost_basis": bi(
            "University of Bremen's current international-student guidance says at least EUR 992 per month is required for regular student life in Germany, including rent, food, insurance, leisure and study costs. This is a planning minimum, not a Bremen-specific rent quote.",
            "Bremen Üniversitesi'nin güncel uluslararası öğrenci rehberi, kira, yemek, sigorta, boş zaman ve eğitim giderleri dahil Almanya'da normal öğrenci hayatı için ayda en az 992 EUR gerektiğini belirtir. Bu bir planlama asgarisidir, Bremen'e özgü kira teklifi değildir.",
        ),
        "average_room_rent_eur": None,
        "average_room_rent_eur_min": None,
        "average_room_rent_eur_max": None,
        "student_housing_available": True,
        "student_housing_competitiveness": "high",
        "housing_difficulty": "high",
        "living_risk": "medium",
        "public_transport_cost_eur_month": None,
        "food_cost_eur_month": None,
        "part_time_work_possibility": "unknown",
        "housing_sentiment": None,
        "housing_notes": bi(
            "The University of Bremen says finding a flat can take three to six months. Studierendenwerk Bremen has 2,139 places across 11 Bremen residences, but an application can be made at any time and a place is not promised; it requires the requested documents after admission.",
            "Bremen Üniversitesi daire bulmanın üç ila altı ay sürebileceğini belirtir. Studierendenwerk Bremen'in Bremen'de 11 yurtta 2.139 yeri vardır; ancak başvuru her zaman yapılabilse de yer garantisi yoktur ve kabulden sonra istenen belgelerin sunulması gerekir.",
        ),
        "verification_notes": bi(
            "No current official Bremen room-rent range was found, so no rent estimate is displayed.",
            "Güncel, resmî Bremen oda kira aralığı bulunamadığından kira tahmini gösterilmez.",
        ),
    })
    row["application_timeline_profile"].update({
        "academic_year": "current programme page checked 2026-07-14",
        "intake_terms": ["winter semester", "summer semester"],
        "non_eu_deadline": "March 1–April 30 (winter) / August 1–October 15 (summer; programme application periods)",
        "eu_deadline": "March 1–April 30 (winter) / August 1–October 15 (summer; programme application periods)",
        "winter_deadline": "March 1–April 30 (winter; programme application period)",
        "summer_deadline": "August 1–October 15 (summer; programme application period)",
        "application_deadline": "March 1–April 30 (winter) / August 1–October 15 (summer; programme application periods)",
        "timeline_risk": "medium",
        "deadline_notes": bi(
            "The current Space Engineering programme page publishes the same application periods for beginners and advanced applicants. It also says the online entrance exam takes place one to two weeks after the application deadline; verify the current admissions regulation before applying.",
            "Güncel Uzay Mühendisliği program sayfası başlangıç ve ileri düzey adaylar için aynı başvuru dönemlerini yayımlar. Ayrıca çevrim içi giriş sınavının başvuru son tarihinden bir ila iki hafta sonra yapıldığını belirtir; başvuru öncesinde güncel kabul yönetmeliğini doğrulayın.",
        ),
    })
    row["decision_summary"].update({
        "main_strengths": [bi(
            "An English 120-ECTS Space Engineering MSc with an entrance exam in engineering mechanics, fluid mechanics and thermodynamics, plus a third/fourth-semester project and thesis.",
            "Mühendislik mekaniği, akışkanlar mekaniği ve termodinamik giriş sınavı ile üçüncü/dördüncü dönem proje ve tez içeren İngilizce 120 AKTS Uzay Mühendisliği yüksek lisansı.",
        )],
        "main_risks": [bi(
            "No general tuition does not solve affordability: the programme lists about EUR 425 each semester and the University advises at least EUR 992/month living budget. Housing searches can take three to six months.",
            "Genel öğrenim ücreti olmaması bütçe sorununu çözmez: program her dönem yaklaşık 425 EUR listeler ve Üniversite ayda en az 992 EUR yaşam bütçesi önerir. Konut araması üç ila altı ay sürebilir.",
        )],
    })

    profile = row.setdefault("source_profile", {})
    profile.update({
        "official_program_page": programme_url,
        "official_tuition_page": preparation_url,
        "official_scholarship_page": scholarship_url,
        "official_housing_page": housing_url,
        "needs_verification": False,
    })
    profile.setdefault("field_confidence", {}).update({
        "program_basic_info": "high",
        "language": "high",
        "admission": "high",
        "tuition": "high",
        "scholarship": "high",
        "curriculum": "high",
        "housing": "high",
        "deadlines": "high",
    })

    for entry in [
        source(programme_url, "University of Bremen Space Engineering M.Sc.", "official_program_page", ["program", "language", "admission", "deadline", "curriculum"], "Current programme page confirms English instruction, 120 ECTS, restricted admission, 1 March–30 April / 1 August–15 October application periods, entrance exam content, semester fee and programme structure.", "Güncel program sayfası İngilizce eğitimi, 120 AKTS'yi, kısıtlı kabulü, 1 Mart–30 Nisan / 1 Ağustos–15 Ekim başvuru dönemlerini, giriş sınavı içeriğini, dönem ücretini ve program yapısını doğrular."),
        source(non_eu_application_url, "University of Bremen Applications from Non-EU Citizens", "official_admission_page", ["admission", "non_eu"], "Current University page confirms a direct Master's application route for applicants from outside the EU and directs them to Master's application requirements and deadlines.", "Güncel Üniversite sayfası AB dışındaki adaylar için doğrudan yüksek lisans başvuru yolunu doğrular ve onları yüksek lisans başvuru şartları ile son tarihlerine yönlendirir."),
        source(preparation_url, "University of Bremen: Preparation from Abroad", "official_tuition_page", ["tuition", "fees"], "Current international-student guidance says the University of Bremen does not charge tuition fees and that a semester fee still applies.", "Güncel uluslararası öğrenci rehberi Bremen Üniversitesinin öğrenim ücreti almadığını ve yine de dönem ücreti uygulandığını belirtir."),
        source(preparation_url, "University of Bremen: International Student Living Costs", "official_cost_of_living_page", ["housing", "living"], "Current guidance states a EUR 992 monthly planning minimum including rent, food, insurance, leisure and study costs, and warns that finding a flat can take three to six months.", "Güncel rehber kira, yemek, sigorta, boş zaman ve eğitim giderleri dahil aylık 992 EUR planlama asgarisini belirtir ve daire bulmanın üç ila altı ay sürebileceğini uyarır."),
        source(scholarship_url, "University of Bremen Deutschlandstipendium", "official_scholarship_page", ["scholarship", "funding"], "Current page publishes approximately 100 winter-semester awards at EUR 300/month, the 1 July–15 August 2026 application period, and access for prospective Master's students.", "Güncel sayfa yaklaşık 100 kış dönemi ödülünü ayda 300 EUR olarak, 1 Temmuz–15 Ağustos 2026 başvuru dönemini ve yüksek lisans adaylarının erişimini yayımlar."),
        source(scholarship_faq_url, "University of Bremen Deutschlandstipendium FAQ", "official_scholarship_page", ["scholarship", "funding"], "Current FAQ says nationality and residence do not matter for regular University of Bremen students, and English applications are accepted for applicants to English-taught degrees.", "Güncel SSS, Bremen Üniversitesi düzenli öğrencileri için uyruk ve ikametin önemli olmadığını; İngilizce yürütülen derecelerin adayları için İngilizce başvuruların kabul edildiğini belirtir."),
        source(housing_url, "Studierendenwerk Bremen Accommodation", "official_housing_page", ["housing"], "Current student-services page lists 2,139 Bremen places in 11 residences, furnished rooms/apartments and inclusive rents, but does not promise availability.", "Güncel öğrenci hizmetleri sayfası 11 yurtta 2.139 Bremen yerini, mobilyalı oda/apartmanları ve her şey dahil kiraları listeler; ancak uygunluk garantisi vermez."),
        source(housing_faq_url, "Studierendenwerk Bremen Accommodation FAQ", "official_housing_page", ["housing"], "Current FAQ says housing applications are possible at any time but a place is only possible after all required documents are supplied, including enrolment evidence after acceptance.", "Güncel SSS konut başvurularının her zaman yapılabildiğini, ancak kabulden sonra kayıt belgesi dahil tüm gerekli belgeler sunulduktan sonra yer verilebileceğini belirtir."),
    ]:
        add_source(row, entry)

    newline = "\r\n" if "\r\n" in original else "\n"
    PATH.write_text(json.dumps(rows, ensure_ascii=False, indent=2).replace("\n", newline) + newline, encoding="utf-8")
    print("Updated University of Bremen Space Engineering with current official evidence.")


if __name__ == "__main__":
    main()
