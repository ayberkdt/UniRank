"""Add checked 2026/27 decision data for four priority European programmes.

Values in this patch deliberately retain their original currencies and state the
published cycle/scope.  No exchange-rate conversion or future-cycle projection
is made.
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
    notes_en: str,
    notes_tr: str,
) -> dict[str, Any]:
    return {
        "url": url,
        "title": title,
        "source_type": source_type,
        "access_status": "pdf" if url.lower().endswith(".pdf") else "ok",
        "last_checked": CHECKED,
        "relevant_fields": fields,
        "confidence": "high",
        "notes": bi(notes_en, notes_tr),
    }


def rows(document: Any) -> list[dict[str, Any]]:
    if isinstance(document, list):
        return document
    if isinstance(document, dict):
        return document.get("programs", document.get("universities", []))
    raise TypeError("Unexpected database document shape")


def get_record(document: Any, identifier: str) -> dict[str, Any]:
    return next(row for row in rows(document) if row.get("id") == identifier)


def add_source(profile: dict[str, Any], item: dict[str, Any]) -> None:
    log = [
        current
        for current in profile.get("source_log", [])
        if not (
            isinstance(current, dict)
            and current.get("url") == item["url"]
            and current.get("source_type") == item["source_type"]
        )
    ]
    log.append(item)
    profile["source_log"] = log


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


def update_cambridge() -> None:
    path, original, document = load("ingiltere.json")
    row = get_record(document, "university-of-cambridge")
    living_url = "https://www.postgraduate.study.cam.ac.uk/finance/maintenance"
    funding_url = "https://www.postgraduate.study.cam.ac.uk/funding/applying-university-funding"

    row["cost_profile"].update({
        "living_cost_gbp_per_year": 19860,
        "verification_notes": bi(
            "Cambridge's 2026/27 published maintenance estimate for a full-time student without dependants is GBP 19,860 per year. It is a living-cost estimate, separate from programme fees and arrival/visa costs.",
            "Cambridge'in 2026/27 için bakmakla yükümlü kişisi olmayan tam zamanlı öğrenciye yönelik yayımladığı geçim gideri tahmini yıllık 19.860 GBP'dir. Bu, program ücretinden ve varış/vize maliyetlerinden ayrı bir yaşam gideri tahminidir.",
        ),
    })
    row["living_profile"].update({
        "monthly_living_cost_gbp_per_month_min": 1655,
        "monthly_living_cost_gbp_per_month_max": 1655,
        "monthly_housing_rent_gbp_per_month_min": 895,
        "monthly_housing_rent_gbp_per_month_max": 895,
        "housing_budget_gbp_per_year": 10740,
        "housing_notes": bi(
            "The GBP 895/month accommodation component is Cambridge's 2026/27 median student estimate and includes rent, utilities, furniture and routine maintenance. College and private-rental costs can differ.",
            "Aylık 895 GBP konaklama bileşeni, Cambridge'in 2026/27 medyan öğrenci tahminidir; kira, faturalar, mobilya ve rutin bakım dahildir. Kolej ve özel kira maliyetleri farklı olabilir.",
        ),
        "verification_notes": bi(
            "The official annual estimate is GBP 19,860 (GBP 1,655/month) for a full-time student without dependants. It is based on a postgraduate-spending survey and is not a price guarantee.",
            "Resmî yıllık tahmin, bakmakla yükümlü kişisi olmayan tam zamanlı öğrenci için 19.860 GBP (aylık 1.655 GBP)'dir. Lisansüstü öğrenci harcama anketine dayanır ve fiyat garantisi değildir.",
        ),
    })
    row["scholarship_profile"].update({
        "available_types": [
            "University postgraduate funding via Applicant Portal",
            "Course-/college-/department-specific funding found through Cambridge Funding Search",
        ],
        "scholarship_deadline": "2026-01-07 (2026/27 main University funding deadline; past published cycle)",
        "scholarship_application_url": funding_url,
        "funding_notes": bi(
            "Cambridge says eligible applicants can be considered for a range of funds by selecting funding in the Applicant Portal; some funds require separate applications. For 2026/27, the main University deadlines were 2 December 2025 and 7 January 2026, while specific funds can differ. Funding is not guaranteed.",
            "Cambridge, uygun adayların Applicant Portal'da finansman seçeneğini işaretleyerek çeşitli fonlar için değerlendirilebileceğini; bazı fonların ayrı başvuru gerektirdiğini belirtir. 2026/27 için ana Üniversite tarihleri 2 Aralık 2025 ve 7 Ocak 2026'ydı; belirli fonların tarihi farklı olabilir. Finansman garanti değildir.",
        ),
        "verification_notes": bi(
            "The card describes a funding route and dated published deadlines, not a programme-specific award or a promise of funding.",
            "Kart, programa özgü bir ödül veya finansman taahhüdü değil, finansman başvuru yolunu ve tarihli yayımlanmış son tarihleri açıklar.",
        ),
    })

    profile = row.setdefault("source_profile", {})
    add_source(profile, source(
        living_url,
        "University of Cambridge postgraduate living costs (2026/27)",
        "official_cost_of_living_page",
        ["housing", "living"],
        "Official 2026/27 maintenance page gives GBP 19,860/year and GBP 1,655/month for a full-time student without dependants, including a GBP 895/month accommodation component.",
        "Resmî 2026/27 geçim gideri sayfası, bakmakla yükümlü kişisi olmayan tam zamanlı öğrenci için yıllık 19.860 GBP ve aylık 1.655 GBP; bunun içinde aylık 895 GBP konaklama bileşeni verir.",
    ))
    add_source(profile, source(
        funding_url,
        "University of Cambridge: Applying for University funding",
        "official_scholarship_page",
        ["scholarship", "funding", "deadline"],
        "Official page explains Applicant Portal and separate-form funding routes and lists the published 2026/27 main University funding deadlines.",
        "Resmî sayfa Applicant Portal ve ayrı form finansman yollarını açıklar; yayımlanan 2026/27 ana Üniversite finansman son tarihlerini listeler.",
    ))
    profile["official_scholarship_page"] = funding_url
    profile["official_cost_of_living_page"] = living_url
    profile["last_verified"] = CHECKED
    profile.setdefault("field_confidence", {}).update({"scholarship": "high", "living_profile": "high", "housing": "high"})
    save(path, original, document)


def update_ku_leuven() -> None:
    path, original, document = load("belcika.json")
    row = get_record(document, "ku-leuven")
    admission_url = "https://onderwijsaanbod.kuleuven.be/2025/opleidingen/e/SC_51016979/toelatingsvoorwaarden"
    scholarship_url = "https://www.kuleuven.be/scholarships"
    living_url = "https://www.kuleuven.be/english/life-at-ku-leuven/money-matters/cost-of-living-in-belgium"

    row["teaching_language"] = ["English"]
    row["language_profile"].update({
        "teaching_language": ["English"],
        "english_required": True,
        "english_level_required": "IELTS Academic 6.5; TOEFL iBT 79; or Cambridge Advanced/Proficiency 185 (no subscore below 170)",
        "accepted_english_tests": ["IELTS Academic", "TOEFL iBT", "Cambridge Advanced", "Cambridge Proficiency"],
        "language_risk": "low",
        "verification_notes": bi(
            "KU Leuven's current programme record labels the Advanced Master's language as English and publishes the listed English-proficiency thresholds. Exemptions remain case-specific.",
            "KU Leuven'in güncel program kaydı ileri yüksek lisansın dilini İngilizce olarak etiketler ve belirtilen İngilizce yeterlilik eşiklerini yayımlar. Muafiyetler aday durumuna göre değişir.",
        ),
    })
    row["scholarship_profile"].update({
        "available_types": ["KU Leuven scholarship finder for Master of Space Studies (2026/27 filters)"],
        "scholarship_application_url": scholarship_url,
        "funding_notes": bi(
            "KU Leuven's official scholarship finder includes Master of Space Studies and academic-year/nationality filters. The finder must be checked for each applicant; this card does not claim that any one award is available to every nationality or that funding is guaranteed.",
            "KU Leuven'in resmî burs bulucusu Master of Space Studies ile akademik yıl ve uyruk filtrelerini içerir. Her aday için bulucu kontrol edilmelidir; bu kart belirli bir ödülün her uyruğa açık olduğunu veya finansmanın garanti edildiğini iddia etmez.",
        ),
        "verification_notes": bi(
            "Availability is intentionally recorded as a searchable official route rather than an unsourced programme-wide award claim.",
            "Uygunluk, kaynaksız bir program-geneli ödül iddiası yerine aranabilir resmî başvuru yolu olarak kaydedilir.",
        ),
    })
    row["living_profile"].update({
        "monthly_living_cost_eur_min": 1050,
        "monthly_living_cost_eur_max": 1400,
        "living_cost_eur_per_month": 1050,
        "housing_notes": bi(
            "KU Leuven's 13 February 2026 planning range is EUR 1,050–1,400/month and includes rent, utilities, food, study materials, insurance, transport and other expenses. It is a Belgium-wide planning estimate; individual Leuven costs vary.",
            "KU Leuven'in 13 Şubat 2026 planlama aralığı aylık 1.050–1.400 EUR'dur; kira, faturalar, yemek, öğrenim malzemeleri, sigorta, ulaşım ve diğer giderleri içerir. Bu Belçika geneli planlama tahminidir; Leuven'deki bireysel maliyetler değişir.",
        ),
        "verification_notes": bi(
            "This is an official total-living-cost planning range, not a claim that every Space Studies student will pay the same rent.",
            "Bu, her Space Studies öğrencisinin aynı kirayı ödeyeceği iddiası değil, resmî toplam yaşam maliyeti planlama aralığıdır.",
        ),
    })

    profile = row.setdefault("source_profile", {})
    add_source(profile, source(
        admission_url,
        "KU Leuven Master of Space Studies admission requirements (2026/27)",
        "official_admission_page",
        ["language", "admission", "non_eu_eligibility"],
        "Official programme record labels the 60-ECTS Advanced Master's language as English and gives the published English test thresholds.",
        "Resmî program kaydı 60 AKTS'lik ileri yüksek lisansın dilini İngilizce olarak etiketler ve yayımlanmış İngilizce sınav eşiklerini verir.",
    ))
    add_source(profile, source(
        scholarship_url,
        "KU Leuven Scholarships finder",
        "official_scholarship_page",
        ["scholarship", "funding"],
        "Official finder offers programme, nationality and 2026/27 academic-year filters and includes Master of Space Studies.",
        "Resmî bulucu program, uyruk ve 2026/27 akademik yılı filtreleri sunar; Master of Space Studies'i içerir.",
    ))
    add_source(profile, source(
        living_url,
        "KU Leuven cost of living in Belgium (updated 13 February 2026)",
        "official_cost_of_living_page",
        ["housing", "living"],
        "Official planning range is EUR 1,050–1,400/month including housing and core student expenses.",
        "Resmî planlama aralığı konaklama ve temel öğrenci giderleri dahil aylık 1.050–1.400 EUR'dur.",
    ))
    profile["official_admission_page"] = admission_url
    profile["official_scholarship_page"] = scholarship_url
    profile["official_cost_of_living_page"] = living_url
    profile["last_verified"] = CHECKED
    profile.setdefault("field_confidence", {}).update({"language": "high", "scholarship": "high", "living_profile": "high", "housing": "high"})
    save(path, original, document)


def update_tecnico_lisbon() -> None:
    path, original, document = load("portekiz.json")
    row = get_record(document, "ist-lisbon")
    admission_url = "https://tecnico.ulisboa.pt/en/education/study-at-tecnico/applications/international-students/"
    living_url = "https://aai.tecnico.ulisboa.pt/files/sites/52/brochura_estudantes_internacionais_26_27_set_25.pdf"
    housing_url = "https://aai.tecnico.ulisboa.pt/files/sites/52/housing-information-en.pdf"

    row["application_timeline_profile"] = {
        "academic_year": "2026/2027 published international-student cycle (all calls passed when checked)",
        "intake_terms": ["September 2026"],
        "application_rounds": [
            "1st call: 2 January–6 February 2026, 17:00 WET",
            "2nd call: 6 April–22 May 2026, 17:00 WET",
            "3rd call: 6–17 July 2026, 17:00 WET",
        ],
        "non_eu_deadline": "2026-07-17 (third 2026/27 international-student call, 17:00 WET; passed when checked)",
        "eu_deadline": None,
        "application_deadline": "2026-07-17 (third 2026/27 international-student call, 17:00 WET; passed when checked)",
        "scholarship_deadline": None,
        "pre_enrolment_required": True,
        "visa_sensitive_deadline": "2026-07-17 (published third international call; do not rely on it for a future cycle)",
        "application_result_timing": "Third-call results published by 28 July 2026",
        "enrollment_deadline": None,
        "timeline_risk": "high",
        "deadline_notes": bi(
            "The dates are for the Special Admission Regime for non-EU international students applying to 2026/27. They are recorded as a closed, dated reference only; Técnico has not yet published the next-cycle timetable. EU/national applicants use another admission route.",
            "Tarihler, 2026/27 için AB dışı uluslararası öğrencilerin Özel Kabul Rejimine aittir. Yalnızca kapanmış ve tarihli referans olarak kaydedilir; Técnico sonraki dönem takvimini henüz yayımlamamıştır. AB/ulusal adaylar başka bir kabul yolunu kullanır.",
        ),
    }
    row["living_profile"].update({
        "average_room_rent_eur_min": 350,
        "average_room_rent_eur_max": 550,
        "food_cost_eur_month": 200,
        "public_transport_cost_eur_month": 40,
        "housing_difficulty": "high",
        "housing_notes": bi(
            "Técnico's 2026/27 international-student brochure lists room rent at EUR 350–550/month, average monthly meals around EUR 200 and a monthly transport pass at EUR 40. A separate official housing notice warns that residences are extremely limited and a room can cost EUR 350–500 or more; deposit plus advance rent is normally required.",
            "Técnico'nun 2026/27 uluslararası öğrenci broşürü oda kirasını aylık 350–550 EUR, ortalama aylık yemek giderini yaklaşık 200 EUR ve aylık ulaşım kartını 40 EUR olarak listeler. Ayrı bir resmî konaklama duyurusu yurt kontenjanının son derece sınırlı olduğunu; bir odanın 350–500 EUR veya daha fazlasına mal olabileceğini ve genellikle depozito ile peşin kira gerektiğini belirtir.",
        ),
        "verification_notes": bi(
            "No all-in Lisbon total is calculated: the official brochure publishes component costs, and the housing notice warns that private-market pricing changes quickly.",
            "Tüm giderleri kapsayan Lizbon toplamı hesaplanmaz: resmî broşür bileşen maliyetlerini yayımlar, konaklama duyurusu ise özel piyasa fiyatlarının hızlı değiştiği uyarısını yapar.",
        ),
    })

    profile = row.setdefault("source_profile", {})
    add_source(profile, source(
        admission_url,
        "Técnico Lisboa: International Students applications 2026/27",
        "official_admission_page",
        ["admission", "non_eu_eligibility", "deadline", "tuition"],
        "Official page gives the three 2026/27 international-student application windows, required second-cycle documents, the EUR 100 application fee and EUR 7,000/year international fee.",
        "Resmî sayfa üç adet 2026/27 uluslararası öğrenci başvuru dönemini, ikinci döngü gerekli belgelerini, 100 EUR başvuru ücretini ve yıllık 7.000 EUR uluslararası öğrenci ücretini verir.",
    ))
    add_source(profile, source(
        admission_url,
        "Técnico Lisboa: International Students fees 2026/27",
        "official_tuition_page",
        ["tuition"],
        "Official page publishes EUR 7,000/year for international students in first and second study cycles, with EUR 2,000 due on vacancy reservation.",
        "Resmî sayfa birinci ve ikinci döngüdeki uluslararası öğrenciler için yıllık 7.000 EUR; kontenjan rezervasyonunda 2.000 EUR ödeme yayımlar.",
    ))
    add_source(profile, source(
        living_url,
        "Técnico Lisboa International Students 2026/27 brochure: Lisbon cost components",
        "official_cost_of_living_page",
        ["housing", "living"],
        "Official 2026/27 brochure gives room, flat and residence ranges plus average meals and transport costs.",
        "Resmî 2026/27 broşür oda, daire ve yurt aralıkları ile ortalama yemek ve ulaşım maliyetlerini verir.",
    ))
    add_source(profile, source(
        housing_url,
        "Técnico Lisboa Housing Information: private accommodation in Lisbon",
        "official_housing_page",
        ["housing", "living"],
        "Official notice says student residences are extremely limited and warns that rooms cost EUR 350–500 or more, usually with a deposit and advance rent.",
        "Resmî duyuru öğrenci yurtlarının son derece sınırlı olduğunu; odaların 350–500 EUR veya daha fazlasına mal olduğunu ve genellikle depozito ile peşin kira gerektiğini belirtir.",
    ))
    profile["official_admission_page"] = admission_url
    profile["official_tuition_page"] = admission_url
    profile["official_cost_of_living_page"] = living_url
    profile["official_housing_page"] = housing_url
    profile["last_verified"] = CHECKED
    profile.setdefault("field_confidence", {}).update({"admission": "high", "tuition": "high", "deadlines": "high", "application_timeline_profile": "high", "living_profile": "high", "housing": "high"})
    save(path, original, document)


def update_uc3m() -> None:
    path, original, document = load("ispanya.json")
    row = get_record(document, "spain_uc3m_space_aero")
    admission_url = "https://www.uc3m.es/postgraduate/admission/process"
    living_url = "https://www.uc3m.es/living-madrid/need-know/social-cost-life"

    row["application_timeline_profile"] = {
        "academic_year": "2026/2027 published cycle (closed when checked)",
        "intake_terms": ["September 2026"],
        "application_rounds": [
            "First period: 1 December 2025–31 January 2026",
            "Second period: 1 February–31 March 2026",
            "Third period: 1 April–31 May 2026",
            "Extended period: only for master's programmes with vacancies",
        ],
        "non_eu_deadline": "2026-05-31 (third regular 2026/27 period; published general master calendar, passed when checked)",
        "eu_deadline": "2026-05-31 (third regular 2026/27 period; published general master calendar, passed when checked)",
        "application_deadline": "2026-05-31 (third regular 2026/27 period; programme may close early if places fill)",
        "scholarship_deadline": "2026-10-07 (Santander Ayuda Económica 2026; separate from admission deadline)",
        "pre_enrolment_required": True,
        "visa_sensitive_deadline": "2026-05-31 (published regular calendar; applicants needing a visa should not wait for a later cycle)",
        "application_result_timing": "Third-period decisions from 23 June 2026",
        "enrollment_deadline": None,
        "timeline_risk": "high",
        "deadline_notes": bi(
            "UC3M's published general master calendar is recorded as a closed 2026/27 reference. The university states that programmes can close before the period end if places are filled; the extended period is only for programmes with vacancies. A future-cycle deadline is not inferred.",
            "UC3M'nin yayımladığı genel yüksek lisans takvimi kapanmış 2026/27 referansı olarak kaydedilir. Üniversite, kontenjanlar dolarsa programların dönem sonundan önce kapanabileceğini; uzatılmış dönemin yalnızca kontenjanı olan programlar için olduğunu belirtir. Gelecek dönem son tarihi çıkarım yoluyla üretilmez.",
        ),
    }
    row["living_profile"].update({
        "monthly_living_cost_eur_min": 600,
        "monthly_living_cost_eur_max": 1200,
        "average_room_rent_eur": 400,
        "average_room_rent_eur_min": 250,
        "average_room_rent_eur_max": 400,
        "food_cost_eur_month": 150,
        "public_transport_cost_eur_month": 20,
        "housing_notes": bi(
            "UC3M estimates total Madrid student living costs at EUR 600–1,200/month. It cites about EUR 400/month for a central shared-room and around EUR 250 in Getafe or Leganés; the Space Engineering campus is Leganés. The EUR 20 transport figure is specifically for people under 26.",
            "UC3M, Madrid'de toplam öğrenci yaşam maliyetini aylık 600–1.200 EUR olarak tahmin eder. Merkezde paylaşımlı oda için yaklaşık 400 EUR, Getafe veya Leganés'te yaklaşık 250 EUR verir; Space Engineering kampüsü Leganés'tedir. 20 EUR ulaşım tutarı özellikle 26 yaş altı içindir.",
        ),
        "verification_notes": bi(
            "These are official planning estimates whose housing component changes by district and housing type; they are not represented as a guaranteed room price.",
            "Bunlar bölgeye ve konut türüne göre değişen resmî planlama tahminleridir; garanti edilmiş oda fiyatı olarak sunulmaz.",
        ),
    })

    profile = row.setdefault("source_profile", {})
    add_source(profile, source(
        admission_url,
        "UC3M Master admission process 2026/27",
        "official_admission_page",
        ["admission", "deadline"],
        "Official general master calendar lists the three regular 2026/27 periods and says programmes can close early when places are filled.",
        "Resmî genel yüksek lisans takvimi üç düzenli 2026/27 dönemi listeler ve kontenjanlar dolduğunda programların erken kapanabileceğini belirtir.",
    ))
    add_source(profile, source(
        living_url,
        "UC3M: student cost of living in Madrid",
        "official_cost_of_living_page",
        ["housing", "living"],
        "Official UC3M page gives EUR 600–1,200/month total student costs, room examples for central Madrid and Getafe/Leganés, food and under-26 transport costs.",
        "Resmî UC3M sayfası aylık 600–1.200 EUR toplam öğrenci maliyeti, merkez Madrid ve Getafe/Leganés için oda örnekleri, yemek ve 26 yaş altı ulaşım maliyetleri verir.",
    ))
    profile["official_admission_page"] = admission_url
    profile["official_cost_of_living_page"] = living_url
    profile["last_verified"] = CHECKED
    profile.setdefault("field_confidence", {}).update({"deadlines": "high", "application_timeline_profile": "high", "living": "high", "living_profile": "high", "housing": "high"})
    save(path, original, document)


def main() -> None:
    update_cambridge()
    update_ku_leuven()
    update_tecnico_lisbon()
    update_uc3m()
    print("Updated Cambridge, KU Leuven, Técnico Lisboa and UC3M with checked official 2026/27 decision data.")


if __name__ == "__main__":
    main()
