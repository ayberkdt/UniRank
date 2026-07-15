"""Add only source-backed decision data to four priority European records.

This patch deliberately preserves uncertainty: ULB financial aid is not presented
as a general incoming non-EU scholarship, and VKI's visa proof-of-funds threshold
is kept separate from an actual Brussels living-cost estimate.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CHECKED = "2026-07-15"


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
) -> dict[str, Any]:
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


def rows(document: Any) -> list[dict[str, Any]]:
    if isinstance(document, list):
        return document
    return document.get("programs", document.get("universities", []))


def load(filename: str) -> tuple[Path, str, Any]:
    path = ROOT / "data_base" / filename
    original = path.read_text(encoding="utf-8")
    return path, original, json.loads(original)


def save(path: Path, original: str, document: Any) -> None:
    newline = "\r\n" if "\r\n" in original else "\n"
    path.write_text(
        json.dumps(document, ensure_ascii=False, indent=2).replace("\n", newline) + newline,
        encoding="utf-8",
    )


def record(document: Any, identifier: str) -> dict[str, Any]:
    return next(row for row in rows(document) if row.get("id") == identifier)


def add_source(profile: dict[str, Any], item: dict[str, Any]) -> None:
    profile["source_log"] = [
        current
        for current in profile.get("source_log", [])
        if not (
            isinstance(current, dict)
            and current.get("url") == item["url"]
            and current.get("source_type") == item["source_type"]
        )
    ]
    profile["source_log"].append(item)


def update_uliege() -> None:
    path, original, document = load("belcika.json")
    row = record(document, "uliege")
    programme_url = "https://www.programmes.uliege.be/cocoon/20262027/formations/condac/A2SAER01.html"
    funding_url = "https://www.international.uliege.be/cms/c_19399082/en/faq-master-in-wbi-scholarships"
    living_url = "https://www.international.uliege.be/books/ErasmusGuideEn/11/"

    row["eligibility_profile"].update({
        "eligible_for_non_eu": True,
        "required_previous_degree": bi(
            "A foreign degree judged equivalent/comparable by the admission jury to the specified 180-ECTS engineering Bachelor's route; the programme lists civil engineering sciences directly and identifies possible bridging for some other backgrounds.",
            "Kabul jürisinin belirtilen 180 AKTS'lik mühendislik lisans yoluna eşdeğer/karşılaştırılabilir bulduğu yabancı derece; program sivil mühendislik bilimlerini doğrudan listeler ve bazı diğer altyapılar için tamamlama dersleri öngörür.",
        ),
        "required_ects": {"total": "180 ECTS (foreign-degree equivalency assessed by jury)"},
        "accepted_backgrounds": [
            "Civil engineering sciences / engineering",
            "Comparable foreign engineering degree subject to jury assessment",
        ],
        "admission_mode": "foreign-degree equivalency and jury assessment",
        "admission_risk": "medium",
        "verification_notes": bi(
            "ULiège's 2026/27 programme page states the 120-credit Aerospace Engineering Master's entry route and that a foreign degree must be recognised as equivalent/comparable by the jury. It also requires B2 English; final admission remains an individual jury decision.",
            "ULiège'in 2026/27 program sayfası 120 kredilik Aerospace Engineering yüksek lisansına giriş yolunu ve yabancı derecenin jüri tarafından eşdeğer/karşılaştırılabilir bulunması gerektiğini belirtir. B2 İngilizce de gerekir; nihai kabul aday bazında jüri kararıdır.",
        ),
    })
    row["scholarship_profile"].update({
        "available_types": ["Master.IN WBI scholarship (competitive; published 2026 call closed)"],
        "regional_scholarship_available": True,
        "regional_scholarship_name": "Master.IN WBI",
        "non_eu_eligible": True,
        "scholarship_deadline": "2026-03-31 (published Master.IN WBI call; closed when checked)",
        "scholarship_application_url": funding_url,
        "funding_notes": bi(
            "ULiège states that admitted non-EU candidates may apply to Master.IN WBI, subject to the published conditions, including a recent entrance degree and two academic support letters. It is competitive, not automatic, and the checked 2026 call is closed.",
            "ULiège, kabul edilen AB dışı adayların yakın tarihli giriş derecesi ve iki akademik destek mektubu dahil yayımlanan koşullarla Master.IN WBI'ye başvurabileceğini belirtir. Burs rekabetçidir, otomatik değildir ve kontrol edilen 2026 çağrısı kapanmıştır.",
        ),
        "verification_notes": bi(
            "The record describes eligibility for a competitive official funding route, not a grant guarantee or an assumed next-cycle deadline.",
            "Kayıt, hibe garantisi veya varsayımsal sonraki dönem son tarihi değil; rekabetçi resmî bir finansman yoluna uygunluğu açıklar.",
        ),
    })
    row["living_profile"].update({
        "monthly_living_cost_eur_min": 700,
        "monthly_living_cost_eur_max": 1000,
        "living_cost_eur_per_month": 700,
        "living_risk": "medium",
        "housing_notes": bi(
            "ULiège's international guide estimates student living costs in Liège at EUR 700–1,000/month, excluding the typically higher first month and study-related costs such as books. It is a planning estimate, not a rent offer.",
            "ULiège'in uluslararası rehberi Liège'de öğrenciler için yaşam maliyetini, genellikle daha yüksek olan ilk ay ve kitap gibi öğrenim giderleri hariç, aylık 700–1.000 EUR olarak tahmin eder. Bu planlama tahminidir, kira teklifi değildir.",
        ),
        "verification_notes": bi(
            "The range is an official ULiège international-guide planning amount; it should not be treated as an all-in first-month or guaranteed-housing cost.",
            "Aralık, ULiège uluslararası rehberindeki resmî planlama tutarıdır; ilk ayın tüm gideri veya garanti konaklama maliyeti olarak ele alınmamalıdır.",
        ),
    })

    profile = row.setdefault("source_profile", {})
    add_source(profile, source(
        programme_url, "ULiège MSc Aerospace Engineering programme 2026/27", "official_admission_page",
        ["program", "admission", "language", "non_eu_eligibility"],
        "Official programme page confirms the 120-credit Master's route, English requirement and jury assessment of comparable foreign degrees.",
        "Resmî program sayfası 120 kredilik yüksek lisans yolunu, İngilizce koşulunu ve karşılaştırılabilir yabancı derecelerin jüri tarafından değerlendirilmesini doğrular.",
    ))
    add_source(profile, source(
        funding_url, "ULiège FAQ: Master.IN WBI scholarships", "official_scholarship_page",
        ["scholarship", "funding", "deadline", "non_eu_eligibility"],
        "Official FAQ describes the closed 2026 call, conditions and admitted non-EU eligibility; it does not guarantee funding.",
        "Resmî SSS kapalı 2026 çağrısını, koşulları ve kabul edilmiş AB dışı aday uygunluğunu açıklar; finansman garantisi vermez.",
    ))
    add_source(profile, source(
        living_url, "ULiège Erasmus Guide: estimated Liège student living costs", "official_cost_of_living_page",
        ["housing", "living"],
        "Official international guide gives EUR 700–1,000/month for Liège students except the first month, plus separate study-related costs.",
        "Resmî uluslararası rehber ilk ay hariç Liège öğrencileri için aylık 700–1.000 EUR; ayrıca öğrenimle ilgili giderler belirtir.",
    ))
    profile.update({
        "official_admission_page": programme_url,
        "official_scholarship_page": funding_url,
        "official_cost_of_living_page": living_url,
        "last_verified": CHECKED,
    })
    profile.setdefault("field_confidence", {}).update({
        "admission": "high", "non_eu_eligibility": "medium", "scholarship": "high", "living_profile": "high", "housing": "high",
    })
    save(path, original, document)


def update_chalmers() -> None:
    path, original, document = load("isvec.json")
    row = record(document, "se-chalmers-mobility-msc")
    university_tuition_url = "https://www.chalmers.se/en/education/application-and-admission/tuition-fees/"
    si_course_url = "https://apply-scholarships.si.se/courses/course/715"
    row["cost_profile"].update({
        "tuition_sek_per_year_min": 160000,
        "tuition_sek_per_year_max": 160000,
        "tuition_sek_per_term": 80000,
        "tuition_non_eu_full_program": {
            "amount": 320000,
            "currency": "SEK",
            "basis": "four semesters at SEK 80,000; published programme price",
        },
        "tuition_basis": "published programme price for fee-paying students",
        "verification_notes": bi(
            "Chalmers confirms that non-EU/EEA/Swiss students normally pay tuition. The official Swedish Institute course listing for this specific 120-ECTS Mobility Engineering programme states SEK 80,000 per semester; the two-year total is shown only as four published semester charges, with no currency conversion.",
            "Chalmers, AB/AEA/İsviçre dışı öğrencilerin normalde öğrenim ücreti ödediğini doğrular. Bu belirli 120 AKTS Mobility Engineering programı için resmî Swedish Institute ders kaydı dönem başına 80.000 SEK belirtir; iki yıllık toplam, kur dönüşümü olmadan yalnızca dört yayımlanmış dönem ücreti olarak gösterilir.",
        ),
    })
    profile = row.setdefault("source_profile", {})
    add_source(profile, source(
        university_tuition_url, "Chalmers tuition fees", "official_tuition_page",
        ["tuition", "non_eu_eligibility"],
        "Chalmers confirms that fee-paying students are normally from outside the EU/EEA/Switzerland, but the page does not publish this programme's numeric price.",
        "Chalmers, ücret ödeyen öğrencilerin normalde AB/AEA/İsviçre dışından olduğunu doğrular; ancak sayfa bu programın sayısal fiyatını yayımlamaz.",
    ))
    add_source(profile, source(
        si_course_url, "Swedish Institute official course listing: Mobility Engineering at Chalmers", "official_tuition_page",
        ["tuition"],
        "The official Swedish Institute course listing gives SEK 80,000 per semester for this 120-ECTS English-taught programme. It is an official government course listing rather than Chalmers' own price table.",
        "Resmî Swedish Institute ders kaydı, bu 120 AKTS ve İngilizce program için dönem başına 80.000 SEK verir. Chalmers'ın kendi fiyat tablosu değil, resmî bir devlet ders kaydıdır.",
        "medium",
    ))
    profile.update({"official_tuition_page": university_tuition_url, "last_verified": CHECKED})
    profile.setdefault("field_confidence", {})["tuition"] = "medium"
    save(path, original, document)


def update_oxford() -> None:
    path, original, document = load("ingiltere.json")
    row = record(document, "university-of-oxford")
    course_url = "https://www.ox.ac.uk/admissions/graduate/courses/msc-research-engineering-science"
    row["cost_profile"].update({
        "tuition_gbp_per_year_min": 34700,
        "tuition_gbp_per_year_max": 34700,
        "tuition_basis": "2026/27 published overseas annual fee; course has 2–3 year expected duration",
        "verification_notes": bi(
            "Oxford's live 2026/27 course page lists GBP 34,700 overseas tuition per year and GBP 10,470 home tuition per year. The degree is expected to last two to three years, so the card does not multiply this into an assumed programme total.",
            "Oxford'un canlı 2026/27 ders sayfası yurtdışı için yıllık 34.700 GBP, ev ücreti için yıllık 10.470 GBP listeler. Derecenin iki ila üç yıl sürmesi beklendiğinden kart bunu varsayımsal bir program toplamına çarpmaz.",
        ),
    })
    row["application_timeline_profile"].update({
        "application_deadline": "December deadline (2026/27 course funding deadline; exact calendar day is not displayed on the live closed course page)",
        "non_eu_deadline": "December deadline (same course deadline applies to Oxford scholarship consideration; exact calendar day not displayed on live closed page)",
        "scholarship_deadline": "December deadline (course page; exact calendar day not displayed; 2026/27 entry closed)",
        "timeline_risk": "high",
        "deadline_notes": bi(
            "The 2026/27 course is closed. Oxford explicitly says applicants who meet this course's December deadline and receive an offer are considered for Oxford scholarships, but the live closed page does not show a calendar date. The record deliberately preserves that precision limit and does not project a 2027/28 date.",
            "2026/27 programı başvurulara kapalıdır. Oxford, bu dersin Aralık son tarihine uyan ve teklif alan adayların Oxford bursları için değerlendirildiğini açıkça belirtir; ancak canlı kapalı sayfa takvim gününü göstermez. Kayıt bu hassasiyet sınırını korur ve 2027/28 tarihi tahmin etmez.",
        ),
    })
    profile = row.setdefault("source_profile", {})
    add_source(profile, source(
        course_url, "University of Oxford MSc by Research in Engineering Science 2026/27", "official_program_page",
        ["program", "tuition", "deadline", "scholarship", "housing", "living"],
        "Live course page confirms the course is closed for 2026/27, publishes annual home/overseas fees and living costs, and refers to the course's December funding deadline without a calendar day.",
        "Canlı ders sayfası programın 2026/27 için kapalı olduğunu doğrular; yıllık ev/yurtdışı ücretlerini ve yaşam maliyetlerini yayımlar, fakat dersin Aralık finansman son tarihi için takvim günü belirtmez.",
    ))
    profile.update({"official_program_page": course_url, "last_verified": CHECKED})
    profile.setdefault("field_confidence", {}).update({"tuition": "high", "deadline": "medium", "application_timeline_profile": "medium"})
    save(path, original, document)


def update_brussels_planning_context() -> None:
    path, original, document = load("belcika.json")
    ulb = record(document, "ulb-brussels")
    vki = record(document, "vki-von-karman")
    ulb_living_url = "https://www.ulb.be/en/incoming-mobility/practical-information-for-incoming-students"
    ulb_blocked_url = "https://www.ulb.be/en/non-exchange-international-students/information-about-blocked-accounts-for-visa-or-residence-permit-renewal"
    visa_url = "https://dofi.ibz.be/en/themes/ressortissants-dun-pays-tiers/etudes/favoris/sufficient-means-subsistence"

    ulb["living_profile"].update({
        "monthly_living_cost_eur_min": 800,
        "monthly_living_cost_eur_max": 800,
        "average_room_rent_eur_min": 400,
        "average_room_rent_eur_max": 400,
        "living_risk": "high",
        "housing_difficulty": "high",
        "housing_notes": bi(
            "ULB's current international practical-information page estimates a Brussels student budget at about EUR 800/month, with roughly half for housing. The page warns its exchange students that no hall rooms are available this academic year and they must use the private market; use this as a Brussels planning signal, not a room guarantee.",
            "ULB'nin güncel uluslararası pratik bilgiler sayfası Brüksel'de öğrenci bütçesini aylık yaklaşık 800 EUR; bunun yaklaşık yarısını konut olarak tahmin eder. Sayfa değişim öğrencilerine bu akademik yılda yurt odası bulunmadığını ve özel piyasayı kullanmaları gerektiğini bildirir; bunu oda garantisi değil, Brüksel planlama sinyali olarak kullanın.",
        ),
        "verification_notes": bi(
            "This current ULB estimate is published for incoming exchange students, so the scope is stated rather than silently generalised. ULB also says the EUR 1,062/month 2026/27 visa proof-of-funds minimum can be below actual Brussels costs.",
            "Bu güncel ULB tahmini gelen değişim öğrencileri için yayımlandığından, kapsamı sessizce genellenmek yerine açıkça belirtilir. ULB ayrıca 2026/27 için aylık 1.062 EUR vize mali yeterlilik asgarisinin gerçek Brüksel maliyetlerinin altında kalabileceğini söyler.",
        ),
        "visa_financial_requirement_eur_per_month": 1062,
    })
    ulb_profile = ulb.setdefault("source_profile", {})
    add_source(ulb_profile, source(
        ulb_living_url, "ULB practical information for incoming students: Brussels cost of living", "official_cost_of_living_page",
        ["housing", "living"],
        "Current ULB page estimates EUR 800/month, with roughly half for housing, and reports no hall rooms for its exchange students this academic year.",
        "Güncel ULB sayfası aylık 800 EUR tahmin eder; bunun yaklaşık yarısı konuttur ve bu akademik yılda değişim öğrencileri için yurt odası bulunmadığını belirtir.",
    ))
    add_source(ulb_profile, source(
        ulb_blocked_url, "ULB blocked accounts: 2026/27 financial means", "official_visa_or_government_page",
        ["visa", "living"],
        "ULB publishes the EUR 1,062/month 2026/27 visa proof-of-funds minimum and warns actual Brussels living costs can be higher.",
        "ULB, 2026/27 için aylık 1.062 EUR vize mali yeterlilik asgarisini yayımlar ve gerçek Brüksel yaşam maliyetlerinin daha yüksek olabileceği uyarısını yapar.",
    ))
    ulb_profile.update({"official_cost_of_living_page": ulb_living_url, "last_verified": CHECKED})
    ulb_profile.setdefault("field_confidence", {}).update({"living_profile": "medium", "housing": "medium"})

    vki["living_profile"].update({
        "visa_financial_requirement_eur_per_month": 1062,
        "verification_notes": bi(
            "Belgium's 2026/27 visa proof-of-subsistence threshold is EUR 1,062/month. It is a legal financial-means minimum, not an observed Brussels living-cost or VKI housing price, so it is kept separate and the actual local cost remains unknown.",
            "Belçika'nın 2026/27 vize geçim yeterliliği eşiği aylık 1.062 EUR'dur. Bu hukuki mali yeterlilik asgarisidir; gözlemlenmiş Brüksel yaşam maliyeti veya VKI konut fiyatı değildir. Bu nedenle ayrı tutulur ve gerçek yerel maliyet bilinmiyor olarak kalır.",
        ),
    })
    vki_profile = vki.setdefault("source_profile", {})
    add_source(vki_profile, source(
        visa_url, "Belgian Immigration Office: sufficient means of subsistence for students", "official_visa_or_government_page",
        ["visa"],
        "Official Belgian Immigration Office page gives EUR 1,062/month for the 2026/27 academic year; it is not represented as a living-cost estimate.",
        "Resmî Belçika Göçmenlik Ofisi sayfası 2026/27 akademik yılı için aylık 1.062 EUR verir; yaşam maliyeti tahmini olarak sunulmaz.",
    ))
    vki_profile["last_verified"] = CHECKED
    save(path, original, document)


def main() -> None:
    update_uliege()
    update_chalmers()
    update_oxford()
    update_brussels_planning_context()
    print("Updated ULi\u00e8ge, Chalmers, Oxford and Brussels planning context with checked official sources.")


if __name__ == "__main__":
    main()
