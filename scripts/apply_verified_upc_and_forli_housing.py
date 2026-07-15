"""Add current, scoped UPC and Forli housing/funding evidence without overclaiming eligibility."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CHECKED = "2026-07-15"


def bi(en: str, tr: str) -> dict[str, str]:
    return {"en": en, "tr": tr}


def source(url: str, title: str, source_type: str, fields: list[str], en: str, tr: str, confidence: str = "high") -> dict[str, Any]:
    return {
        "url": url,
        "title": title,
        "source_type": source_type,
        "access_status": "pdf" if url.endswith(".pdf") else "ok",
        "last_checked": CHECKED,
        "relevant_fields": fields,
        "confidence": confidence,
        "notes": bi(en, tr),
    }


def load(name: str) -> tuple[Path, str, Any]:
    path = ROOT / "data_base" / name
    raw = path.read_text(encoding="utf8")
    return path, raw, json.loads(raw)


def records(data: Any) -> list[dict[str, Any]]:
    if isinstance(data, list):
        return data
    return data.get("programs", data.get("universities", []))


def get(data: Any, ident: str) -> dict[str, Any]:
    return next(row for row in records(data) if row.get("id") == ident)


def append_source(profile: dict[str, Any], item: dict[str, Any]) -> None:
    profile["source_log"] = [
        old for old in profile.get("source_log", [])
        if not (isinstance(old, dict) and old.get("url") == item["url"] and old.get("source_type") == item["source_type"])
    ] + [item]


def save(path: Path, raw: str, data: Any) -> None:
    newline = "\r\n" if "\r\n" in raw else "\n"
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2).replace("\n", newline) + newline, encoding="utf8")


def update_forli(file_name: str, ident: str) -> None:
    path, raw, data = load(file_name)
    record = get(data, ident)
    rates = "https://www.er-go.it/cosa-fare-per/bandi-di-concorso/leggi-il-bando/bando-di-concorso-benefici-dsu-a-a-2026_2027.pdf/%40%40display-file/file/bando-di-concorso-benefici-dsu-a-a-2026_2027.pdf"
    housing = record.setdefault("living_profile", {})
    housing.update({
        "average_room_rent_eur_min": 219,
        "average_room_rent_eur_max": 310,
        "student_housing_available": True,
        "student_housing_competitiveness": "high",
        "housing_difficulty": "high",
        "living_risk": "medium",
        "housing_notes": bi(
            "Forli-specific, utilities-included ER.GO 2026/27 ranked-accommodation rates are EUR 219/month for an Ex ENAV double room up to EUR 310/month for a Palazzo Sassi Masini single studio. These are income/merit-ranked residence rates, not a private-market average or a room guarantee.",
            "Forli'ye özgü, faturalar dahil ER.GO 2026/27 sıralama usulü yurt ücretleri Ex ENAV çift kişilik oda için ayda 219 EUR ile Palazzo Sassi Masini tek kişilik stüdyo için ayda 310 EUR arasındadır. Bunlar gelir/başarı sıralamasına bağlı yurt ücretidir; özel piyasa ortalaması veya oda garantisi değildir.",
        ),
        "verification_notes": bi(
            "This replaces the former price gap with current, city-specific official residence prices. Total monthly living cost remains unknown because the source prices housing only.",
            "Bu güncelleme önceki fiyat boşluğunu güncel, şehre özgü resmî yurt ücretleriyle doldurur. Kaynak yalnızca konaklamayı fiyatladığı için toplam aylık yaşam gideri bilinmiyor kalır.",
        ),
    })
    profile = record.setdefault("source_profile", {})
    append_source(profile, source(
        rates,
        "ER.GO 2026/27 accommodation rates — Forli",
        "official_housing_page",
        ["housing", "housing_cost", "living"],
        "The official 2026/27 ER.GO call lists utilities-included Forli residence rates: EUR 219 double room to EUR 310 single studio under ranked access; eligibility and assignment are not guaranteed.",
        "Resmî 2026/27 ER.GO çağrısı, sıralama usulünde faturalar dahil Forli yurt ücretlerini 219 EUR çift kişilik odadan 310 EUR tek kişilik stüdyoya kadar listeler; uygunluk ve yerleşim garanti değildir.",
    ))
    profile.update({"official_housing_page": rates, "last_verified": CHECKED})
    profile.setdefault("field_confidence", {}).update({"living_profile": "high", "housing": "high", "living": "high"})
    summary = record.setdefault("decision_summary", {})
    risks = summary.setdefault("main_risks", [])
    risks = [item for item in risks if not (isinstance(item, dict) and "Forlì rent is unknown" in item.get("en", ""))]
    risks.append(bi(
        "The EUR 219-310/month figures are ER.GO ranked-residence prices with utilities, not an open-market rent prediction. Secure eligibility and an actual assignment before relying on them.",
        "Aylık 219-310 EUR tutarlar faturalar dahil ER.GO sıralama-yurt ücretleridir; serbest piyasa kira tahmini değildir. Bunlara güvenmeden önce uygunluğu ve gerçek yerleşimi güvenceye alın.",
    ))
    summary["main_risks"] = risks
    save(path, raw, data)


def update_upc() -> None:
    path, raw, data = load("ispanya.json")
    record = get(data, "spain_upc_aerospace")
    programme_pdf = "https://www.upc.edu/master/en/348/masters-degree-in-aerospace-engineering.pdf"
    scholarship = "https://www.upc.edu/sga/es/Becas/becas-para-estudios/otrasayudas/becasantanderayudaeconomica"
    living = "https://www.upc.edu/sri/en/mobility_office/students-mobility-office/incomings/studying-at-the-upc/copy_of_cost-of-living-and-prices"
    record["application_timeline_profile"].update({
        "academic_year": "2026/2027 reference cycle",
        "intake_terms": ["September 2026", "February 2027 (programme page lists both starts)"],
        "application_rounds": ["Pre-enrolment open; official programme sheet listed an expected 1 July 2026 deadline"],
        "application_deadline": "2026-07-01 (expected date in 2026/27 official programme sheet; passed)",
        "non_eu_deadline": "2026-07-01 (expected date in 2026/27 official programme sheet; passed)",
        "timeline_risk": "high",
        "deadline_notes": bi(
            "The current official 2026/27 programme sheet showed an expected 1 July 2026 pre-enrolment deadline. It is a cycle-specific, passed reference and not a prediction for the next cycle; verify the live application portal before acting.",
            "Güncel resmî 2026/27 program föyü beklenen ön kayıt son tarihini 1 Temmuz 2026 olarak gösterdi. Bu, döngüye özgü ve geçmiş bir referanstır; sonraki döngü için tahmin değildir. İşlem yapmadan önce canlı başvuru portalını doğrulayın.",
        ),
    })
    record["scholarship_profile"].update({
        "regional_scholarship_available": False,
        "regional_scholarship_name": "No general Turkish/non-EU entrant award verified in the checked UPC call",
        "non_eu_eligible": False,
        "scholarship_deadline": "2026-10-07 (named Santander call; not eligible for a standard Turkish/non-EU applicant)",
        "scholarship_application_url": scholarship,
        "funding_status": "no_general_non_eu_entrant_scholarship_verified",
        "funding_notes": bi(
            "The checked 2026/27 UPC Santander aid is EUR 1,000 and includes master's students, but requires Spanish or EU nationality plus a prior Ministry/Equitat award. It is therefore not a general scholarship route for a standard Turkish/non-EU entrant. No broad Turkish/non-EU entrant award was verified in this update.",
            "Kontrol edilen 2026/27 UPC Santander yardımı 1.000 EUR'dur ve yüksek lisans öğrencilerini kapsar; ancak İspanyol veya AB vatandaşı olmayı ve önceki Bakanlık/Equitat ödülünü gerektirir. Bu nedenle standart bir Türkiye/AB dışı giriş öğrencisi için genel burs yolu değildir. Bu güncellemede geniş kapsamlı Türkiye/AB dışı giriş bursu doğrulanmadı.",
        ),
        "verification_notes": bi(
            "A named scholarship call exists, but the record deliberately reports its nationality and prior-award exclusion instead of presenting it as available to all international applicants.",
            "İsimli bir burs çağrısı vardır; ancak kayıt bunu tüm uluslararası adaylara açıkmış gibi sunmak yerine uyruk ve önceki ödül dışlamasını açıkça raporlar.",
        ),
    })
    record["living_profile"].update({
        "monthly_living_cost_eur_min": 1300,
        "monthly_living_cost_eur_max": 1500,
        "average_room_rent_eur_min": 450,
        "average_room_rent_eur_max": 650,
        "housing_difficulty": "high",
        "living_risk": "high",
        "housing_notes": bi(
            "UPC's current international-student guidance recommends EUR 1,300-1,500/month total and gives EUR 450-650/month for a shared-flat room, plus a first-month deposit warning. It is UPC-wide guidance depending on city, not a Terrassa room offer.",
            "UPC'nin güncel uluslararası öğrenci rehberi toplam aylık 1.300-1.500 EUR ve paylaşımlı daire odası için 450-650 EUR önerir; ayrıca ilk ay depozito uyarısı verir. Bu, Terrassa oda teklifi değil, şehre göre değişen UPC-geneli rehberdir.",
        ),
        "verification_notes": bi(
            "The displayed range is an official planning budget that includes accommodation and living expenses. It must not be relabelled as a campus-residence price.",
            "Gösterilen aralık konaklama ve yaşam giderlerini kapsayan resmî bir planlama bütçesidir. Kampüs yurt fiyatı olarak yeniden etiketlenmemelidir.",
        ),
    })
    profile = record.setdefault("source_profile", {})
    append_source(profile, source(
        programme_pdf,
        "UPC Master's Degree in Aerospace Engineering 2026/27 sheet",
        "official_admission_page",
        ["admission", "deadline", "programme", "language", "tuition", "curriculum"],
        "Current official sheet lists the 120-ECTS programme, first-year Catalan/second-year English delivery, fees and expected 1 July 2026 deadline.",
        "Güncel resmî föy 120 AKTS programı, ilk yıl Katalanca/ikinci yıl İngilizce eğitimi, ücretleri ve beklenen 1 Temmuz 2026 son tarihini listeler.",
    ))
    append_source(profile, source(
        scholarship,
        "UPC Santander Financial Aid 2026/27",
        "official_scholarship_page",
        ["scholarship", "funding", "eligibility", "deadline"],
        "Official call gives EUR 1,000, 7 October 2026 deadline and its Spanish/EU nationality plus prior-award conditions; it is not a general non-EU entrant award.",
        "Resmî çağrı 1.000 EUR, 7 Ekim 2026 son tarihi ile İspanyol/AB vatandaşı ve önceki ödül koşullarını verir; genel AB dışı giriş öğrenci ödülü değildir.",
    ))
    append_source(profile, source(
        living,
        "UPC international student cost-of-living guidance",
        "official_cost_of_living_page",
        ["living", "housing"],
        "Official UPC guidance recommends EUR 1,300-1,500/month and EUR 450-650 shared-room rent, both expressly city-dependent planning information.",
        "Resmî UPC rehberi, ikisi de açıkça şehre bağlı planlama bilgisi olarak aylık 1.300-1.500 EUR ve 450-650 EUR paylaşımlı oda kirası önerir.",
        "medium",
    ))
    profile.update({
        "official_admission_page": programme_pdf,
        "official_scholarship_page": scholarship,
        "official_cost_of_living_page": living,
        "last_verified": CHECKED,
        "needs_verification": False,
        "verification_notes": bi(
            "Programme, language, fees, a cycle-specific deadline, living budget and the actual scope of the named scholarship are source-checked. The card does not turn an EU-only aid call into a Turkish/non-EU scholarship promise.",
            "Program, dil, ücretler, döngüye özgü son tarih, yaşam bütçesi ve isimli bursun gerçek kapsamı kaynakla kontrol edilmiştir. Kart, yalnızca AB'ye açık yardımı Türkiye/AB dışı burs vaadine dönüştürmez.",
        ),
    })
    profile.setdefault("field_confidence", {}).update({
        "scholarship": "high",
        "application_timeline_profile": "medium",
        "living_profile": "medium",
        "housing": "medium",
    })
    summary = record.setdefault("decision_summary", {})
    summary["main_risks"] = [
        bi(
            "Year one is Catalan and year two English; this is not a 100% English degree and non-Catalan/non-Spanish applicants should not treat it as one.",
            "İlk yıl Katalanca, ikinci yıl İngilizcedir; bu %100 İngilizce bir derece değildir ve Katalanca/İspanyolca bilmeyen adaylar onu öyle görmemelidir.",
        ),
        bi(
            "The named EUR 1,000 UPC Santander aid is not generally available to a Turkish/non-EU entrant, and the listed 2026 application date has passed. Funding and next-cycle timing must be rechecked.",
            "İsimli 1.000 EUR UPC Santander yardımı Türkiye/AB dışı giriş öğrencisi için genel olarak uygun değildir ve listelenen 2026 başvuru tarihi geçmiştir. Finansman ve sonraki döngü takvimi yeniden kontrol edilmelidir.",
        ),
    ]
    summary["main_strengths"] = [
        bi(
            "The programme makes its aerospace specialisations and its non-English first-year delivery explicit, preventing a costly language surprise.",
            "Program, havacılık-uzay uzmanlaşmalarını ve İngilizce olmayan ilk yıl eğitimini açıkça belirtir; böylece maliyetli bir dil sürprizini önler.",
        ),
        bi(
            "UPC's own planning guidance gives a visible total living budget and first-month deposit warning rather than showing tuition alone.",
            "UPC'nin kendi planlama rehberi yalnızca öğrenim ücretini değil, görünür bir toplam yaşam bütçesini ve ilk ay depozito uyarısını verir.",
        ),
    ]
    save(path, raw, data)


update_forli("italy.json", "unibo_aerospace_forli")
update_forli("italya.json", "it-bologna-aero-msc")
update_upc()
print("Updated both Forli record variants and UPC with current scoped housing, funding, living and timeline evidence.")
