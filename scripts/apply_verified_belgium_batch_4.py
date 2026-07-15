"""Apply current official evidence for UGent and the TFMASA joint master.

The two records deliberately retain scope limits: UGent's Ghent budget is a
university planning range, while TFMASA's Belgium budget applies to its
Louvain-la-Neuve semester rather than to all three mobility locations.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CHECKED = "2026-07-15"


def bi(en: str, tr: str) -> dict[str, str]:
    return {"en": en, "tr": tr}


def src(url: str, title: str, kind: str, fields: list[str], en: str, tr: str, confidence: str = "high") -> dict[str, Any]:
    return {
        "url": url,
        "title": title,
        "source_type": kind,
        "access_status": "ok",
        "last_checked": CHECKED,
        "relevant_fields": fields,
        "confidence": confidence,
        "notes": bi(en, tr),
    }


def add(profile: dict[str, Any], item: dict[str, Any]) -> None:
    profile["source_log"] = [
        old for old in profile.get("source_log", [])
        if not (isinstance(old, dict) and old.get("url") == item["url"] and old.get("source_type") == item["source_type"])
    ] + [item]


def load() -> tuple[Path, str, list[dict[str, Any]]]:
    path = ROOT / "data_base" / "belcika.json"
    raw = path.read_text(encoding="utf8")
    return path, raw, json.loads(raw)


def get(rows: list[dict[str, Any]], ident: str) -> dict[str, Any]:
    return next(row for row in rows if row.get("id") == ident)


def ugent(record: dict[str, Any]) -> None:
    study = "https://studiekiezer.ugent.be/2026/studiekosten/Opleiding/en/EMMECH/2"
    funding = "https://www.ugent.be/prospect/en/administration/fees-funding/funding-studies.htm"
    master_mind = "https://www.ugent.be/plone_portal/en/research/funding/globalsouth/master-mind"
    living = "https://www.ugent.be/en/work/talent/welcoming-new-staff/costoflivingghent.html"
    admission = "https://www.ugent.be/en/education/degree/degree-student/application-deadline"

    record["curriculum_profile"].update({
        "core_courses": [
            "Fluid Machines (6 ECTS)", "Linear Systems (6 ECTS)",
            "Electrical Drives (6 ECTS)", "Kinematics and Dynamics of Mechanisms (6 ECTS)",
            "Numerical Modelling and Design of Electrical and Mechanical Systems (6 ECTS)",
        ],
        "curriculum_url": study,
        "verification_notes": bi(
            "The current 2026/27 UGent study programme lists English delivery and the named core courses. This is an electromechanical systems degree; the card does not relabel it as an aerospace degree.",
            "Güncel 2026/27 UGent programı İngilizce eğitimi ve belirtilen çekirdek dersleri listeler. Bu elektromekanik sistemler derecesidir; kart bunu havacılık-uzay derecesi diye yeniden etiketlemez.",
        ),
    })
    record["scholarship_profile"].update({
        "regional_scholarship_available": True,
        "regional_scholarship_name": "Flemish Master Mind scholarship",
        "merit_scholarships": ["Flemish Master Mind scholarship"],
        "non_eu_eligible": True,
        "scholarship_deadline": "2026-04-01 (admission deadline for the cited Master Mind cycle; passed)",
        "scholarship_application_url": master_mind,
        "funding_notes": bi(
            "UGent lists Master Mind for academically outstanding international master's students of all nationalities. The cited cycle required academic admission by 1 April and coordinator preselection; it is competitive, not automatic funding.",
            "UGent, tüm uyruklardan akademik olarak üstün uluslararası yüksek lisans öğrencileri için Master Mind bursunu listeler. Atıf yapılan döngü 1 Nisan'a kadar akademik kabul ve koordinatör ön seçimi gerektiriyordu; rekabetçidir, otomatik finansman değildir.",
        ),
    })
    record["application_timeline_profile"].update({
        "academic_year": "2026/2027",
        "intake_terms": ["September 2026"],
        "non_eu_deadline": "2026-04-01 (visa-required degree applicants; passed)",
        "eu_deadline": "2026-06-01 (applicants not requiring a visa; passed)",
        "application_deadline": "2026-04-01 or 2026-06-01 depending on visa requirement; passed",
        "timeline_risk": "high",
        "deadline_notes": bi(
            "UGent's published 2026/27 deadlines distinguish visa-required (1 April) and no-visa (1 June) applicants. They are passed reference dates, not a forecast for the next intake.",
            "UGent'in yayımlanmış 2026/27 son tarihleri vize gereken (1 Nisan) ve gerekmeyen (1 Haziran) adayları ayırır. Bunlar geçmiş referans tarihlerdir; sonraki kabul dönemi tahmini değildir.",
        ),
    })
    record["living_profile"].update({
        "monthly_living_cost_eur_min": 1200,
        "monthly_living_cost_eur_max": 1800,
        "average_room_rent_eur_min": 400,
        "average_room_rent_eur_max": 650,
        "housing_difficulty": "high",
        "living_risk": "high",
        "housing_notes": bi(
            "UGent's current Ghent guidance gives a EUR 1,200-1,800 indicative monthly single-person budget and EUR 400-650 for shared room/student housing. It warns that rent is usually the biggest expense and that the first month adds deposit, furniture and utility-start costs.",
            "UGent'in güncel Ghent rehberi tek kişi için aylık gösterge bütçeyi 1.200-1.800 EUR, paylaşımlı oda/öğrenci konutunu 400-650 EUR verir. Kiranın genellikle en büyük gider olduğunu ve ilk ayın depozito, mobilya ile tesisat başlangıç masrafları eklediğini uyarır.",
        ),
        "verification_notes": bi(
            "This is university planning guidance for Ghent, not a guaranteed room offer. UGent also says accommodation is scarce and its halls prioritise particular applicant groups.",
            "Bu, Ghent için üniversitenin planlama rehberidir; garantili oda teklifi değildir. UGent ayrıca konutun kıt olduğunu ve yurtlarında belirli başvuru gruplarına öncelik verdiğini söyler.",
        ),
    })
    profile = record["source_profile"]
    for item in [
        src(study, "UGent MSc Mechanical and Electrical Systems Engineering 2026/27 study programme", "official_curriculum_page", ["curriculum", "courses", "language"], "Current programme lists English delivery and named 6-ECTS systems, fluid-machinery, drive and modelling courses.", "Güncel program İngilizce eğitimi ile isimlendirilmiş 6 AKTS'lik sistem, akış makineleri, tahrik ve modelleme derslerini listeler."),
        src(funding, "UGent funding your studies", "official_scholarship_page", ["scholarship", "funding", "non_eu_eligibility"], "UGent lists the Flemish Master Mind scholarship for academically outstanding international master's students of all nationalities.", "UGent, akademik olarak üstün tüm uyruklardan uluslararası yüksek lisans öğrencileri için Flaman Master Mind bursunu listeler."),
        src(master_mind, "UGent Master Mind scholarships", "official_scholarship_page", ["scholarship", "funding", "deadline", "eligibility"], "The official page gives the competitive coordinator-preselection route, academic-admission requirement and cited 1 April deadline.", "Resmî sayfa rekabetçi koordinatör ön seçimi yolunu, akademik kabul şartını ve atıf yapılan 1 Nisan son tarihini verir."),
        src(admission, "UGent application deadlines for degree students", "official_admission_page", ["admission", "deadline", "application_timeline"], "Official degree-student guidance distinguishes the 2026/27 visa-required and no-visa application deadlines.", "Resmî derece öğrencisi rehberi 2026/27 vize gereken ve gerekmeyen başvuru son tarihlerini ayırır."),
        src(living, "UGent cost of living in Ghent", "official_housing_page", ["housing", "living", "living_profile"], "UGent publishes a EUR 1,200-1,800 monthly planning range and EUR 400-650 shared room/student-housing range for Ghent.", "UGent, Ghent için aylık 1.200-1.800 EUR planlama aralığı ile 400-650 EUR paylaşımlı oda/öğrenci konutu aralığını yayımlar."),
    ]:
        add(profile, item)
    profile.update({"official_curriculum_page": study, "official_scholarship_page": funding, "official_admission_page": admission, "official_housing_page": living, "last_verified": CHECKED, "needs_verification": False})
    profile.setdefault("field_confidence", {}).update({"curriculum": "high", "scholarship": "high", "admission": "high", "deadlines": "high", "housing": "high", "living_profile": "high"})


def uclouvain(record: dict[str, Any]) -> None:
    application = "https://tfmasa.com/application/"
    costs = "https://tfmasa.com/costs-funding/"
    mobility = "https://tfmasa.com/mobility/"
    living = "https://www.studyinbelgium.be/en/practical-guide-canadian-students/funding"

    record["cost_profile"].update({
        "academic_year": "2026/2027 entry cohort",
        "tuition_eur_per_year_min": 4500,
        "tuition_eur_per_year_max": 9000,
        "tuition_basis": "TFMASA participation cost: Erasmus+ programme-country/EU category EUR 4,500; non-Erasmus+ programme-country category EUR 9,000 per academic year",
        "tuition_non_eu_full_program": 18000,
        "verification_notes": bi(
            "The official joint-programme page publishes EUR 4,500/year for EU/Erasmus+ programme-country students and EUR 9,000/year for non-Erasmus+ programme-country students. This record presents the category split rather than guessing a Turkish applicant's category.",
            "Resmî ortak program sayfası AB/Erasmus+ program ülkesi öğrencileri için yıllık 4.500 EUR, Erasmus+ program ülkesi dışındaki öğrenciler için yıllık 9.000 EUR yayımlar. Bu kayıt, Türkiye'den bir adayın kategorisini tahmin etmek yerine kategori ayrımını gösterir.",
        ),
    })
    record["scholarship_profile"].update({
        "regional_scholarship_available": True,
        "regional_scholarship_name": "Erasmus Mundus Joint Masters (EMJM) scholarship",
        "merit_scholarships": ["EMJM scholarship: EUR 1,400/month for two years plus participation-cost coverage"],
        "non_eu_eligible": True,
        "scholarship_application_url": costs,
        "funding_notes": bi(
            "For the 2026-2028 intake onward, the TFMASA consortium says EMJM scholarships go to a select group with the highest written and oral assessment scores. Recipients pay no participation fees and receive EUR 1,400/month for the two-year programme; it is not guaranteed to every admitted applicant.",
            "2026-2028 kabulünden itibaren TFMASA konsorsiyumu, EMJM burslarının yazılı ve sözlü değerlendirmede en yüksek puanlı seçilmiş gruba verileceğini belirtir. Alanlar katılım ücreti ödemez ve iki yıllık program boyunca ayda 1.400 EUR alır; her kabul edilen adaya garanti değildir.",
        ),
    })
    record["application_timeline_profile"].update({
        "academic_year": "2026/2028 cohort reference",
        "intake_terms": ["September 2026 reference cohort"],
        "application_rounds": ["Online E-Mundus application; scholarship and self-funded candidates use the same form"],
        "application_deadline": "1 March (year not displayed by current official page; verify live portal before applying)",
        "non_eu_deadline": "1 March (same online route for candidates from all countries; year not displayed)",
        "timeline_risk": "medium",
        "deadline_notes": bi(
            "The live programme page says applications are open, opens the online period from 10 December and closes on 1 March, but does not display a year beside the timeline. The card intentionally preserves that limitation instead of inventing an intake year.",
            "Canlı program sayfası başvuruların açık olduğunu, çevrimiçi dönemin 10 Aralık'ta başladığını ve 1 Mart'ta kapandığını söyler; ancak takvimin yanında yıl göstermez. Kart, kabul yılı uydurmak yerine bu sınırlamayı korur.",
        ),
    })
    record["living_profile"].update({
        "monthly_living_cost_eur_min": 1000,
        "monthly_living_cost_eur_max": 1200,
        "average_room_rent_eur_min": 300,
        "average_room_rent_eur_max": 500,
        "housing_difficulty": "high",
        "living_risk": "medium",
        "housing_notes": bi(
            "Wallonie-Bruxelles Campus gives a EUR 1,000-1,200/month student planning range and EUR 300-500/month accommodation component for French-speaking Belgium, explicitly noting town-to-town variation. TFMASA separately lists UCLouvain kots and the first-come, first-served LOGE private-market portal for the Louvain-la-Neuve semester.",
            "Wallonie-Bruxelles Campus, Fransızca konuşulan Belçika için aylık 1.000-1.200 EUR öğrenci planlama aralığı ve 300-500 EUR konaklama bileşeni verir; şehirden şehre değiştiğini açıkça belirtir. TFMASA ayrıca Louvain-la-Neuve dönemi için UCLouvain kotlarını ve ilk gelen alır LOGE özel piyasa portalını listeler.",
        ),
        "verification_notes": bi(
            "These are regional planning values for the Louvain-la-Neuve mobility semester, not a guaranteed kot price and not a total cost for the France/Germany semesters.",
            "Bunlar Louvain-la-Neuve hareketlilik dönemi için bölgesel planlama değerleridir; garantili kot fiyatı veya Fransa/Almanya dönemlerinin toplam maliyeti değildir.",
        ),
    })
    profile = record["source_profile"]
    for item in [
        src(application, "TFMASA application and timeline", "official_admission_page", ["admission", "non_eu_eligibility", "deadline", "application_timeline"], "Consortium page says applications are open to all countries, gives required documents and shows the online period from 10 December to 1 March without a displayed year.", "Konsorsiyum sayfası başvuruların tüm ülkelere açık olduğunu, gerekli belgeleri ve yıl gösterilmeden 10 Aralık-1 Mart çevrimiçi dönemini verir."),
        src(costs, "TFMASA costs and funding", "official_tuition_page", ["tuition", "fees", "funding"], "Official joint-master page publishes EUR 4,500/year EU/Erasmus+ and EUR 9,000/year non-Erasmus+ participation categories.", "Resmî ortak yüksek lisans sayfası yıllık 4.500 EUR AB/Erasmus+ ve 9.000 EUR Erasmus+ dışı katılım kategorilerini yayımlar."),
        src(costs, "TFMASA EMJM scholarship funding", "official_scholarship_page", ["scholarship", "funding", "eligibility"], "The page specifies competitive EMJM awards from 2026-2028, fee coverage and EUR 1,400/month for two years.", "Sayfa 2026-2028'den itibaren rekabetçi EMJM ödüllerini, ücret karşılamayı ve iki yıl boyunca aylık 1.400 EUR'u belirtir."),
        src(mobility, "TFMASA practical information", "official_housing_page", ["housing", "living"], "Official programme guidance lists UCLouvain kots and the first-come, first-served LOGE portal for its Louvain-la-Neuve semester.", "Resmî program rehberi Louvain-la-Neuve dönemi için UCLouvain kotlarını ve ilk gelen alır LOGE portalını listeler."),
        src(living, "Wallonie-Bruxelles Campus living-cost guidance", "official_housing_page", ["housing", "living", "living_profile"], "Official regional guidance gives EUR 1,000-1,200 monthly student planning cost and EUR 300-500 accommodation, explicitly varying by town.", "Resmî bölgesel rehber şehirden şehre değişmek üzere aylık 1.000-1.200 EUR öğrenci planlama maliyeti ve 300-500 EUR konaklama verir."),
    ]:
        add(profile, item)
    profile.update({"official_admission_page": application, "official_tuition_page": costs, "official_scholarship_page": costs, "official_housing_page": mobility, "last_verified": CHECKED, "needs_verification": False})
    profile.setdefault("field_confidence", {}).update({"tuition": "high", "scholarship": "high", "admission": "high", "deadlines": "medium", "housing": "medium", "living_profile": "medium"})


def vub(record: dict[str, Any]) -> None:
    programme = "https://www.vub.be/en/studying-vub/all-study-programmes-vub/bachelors-and-masters-programmes-vub/master-electromechanical-engineering/program/master/master-electromechanical-engineering-aeronautics"
    scholarship = "https://www.vub.be/en/studying-vub/practical-info-for-students/how-much-does-studying-cost/financial-support/master-mind-scholarship-programme-vub"
    deadlines = "https://www.vub.be/en/studying-vub/apply-and-enrol-vub/admission-requirements-and-deadlines/when-can-you-apply"
    living = "https://www.vub.be/en/studying-vub/practical-info-for-students/how-much-does-studying-cost"
    record["curriculum_profile"].update({
        "tracks": ["Aeronautics"],
        "specializations": ["Aeronautics"],
        "thesis_required": True,
        "curriculum_url": programme,
        "verification_notes": bi(
            "VUB's official Aeronautics-track page describes a 120-ECTS English Electromechanical Engineering master with a common core, track-specific courses and a thesis. Course titles were not inserted where the checked page did not publish them.",
            "VUB'nin resmî Havacılık yolu sayfası, ortak çekirdek, yola özgü dersler ve tez içeren 120 AKTS İngilizce Elektromekanik Mühendisliği yüksek lisansını tanımlar. Kontrol edilen sayfa yayımlamadığı için ders adları eklenmemiştir.",
        ),
    })
    record["scholarship_profile"].update({
        "regional_scholarship_available": True,
        "regional_scholarship_name": "Flemish Master Mind scholarship",
        "merit_scholarships": ["Flemish Master Mind scholarship: EUR 10,020/year plus reduced tuition"],
        "non_eu_eligible": True,
        "scholarship_deadline": "2026-03-26 23:59 GMT+1 (passed)",
        "scholarship_application_url": scholarship,
        "funding_notes": bi(
            "VUB's current Master Mind call is open to all nationalities except Russian applicants, but requires an official VUB acceptance letter, minimum CGPA 3.5/4 and higher English scores than admission. It is a competitive nomination route, not a general fee waiver.",
            "VUB'nin güncel Master Mind çağrısı Rusya başvuruları hariç tüm uyruklara açıktır; ancak resmî VUB kabul mektubu, en az 3,5/4 genel not ortalaması ve kabulden daha yüksek İngilizce puanı ister. Rekabetçi bir aday gösterme yoludur, genel ücret muafiyeti değildir.",
        ),
    })
    record["application_timeline_profile"].update({
        "academic_year": "2026/2027",
        "intake_terms": ["September 2026"],
        "non_eu_deadline": "2026-04-01 (last day 31 March; passed)",
        "eu_deadline": "2026-08-01 (last day 31 July; passed)",
        "application_deadline": "2026-04-01 for non-EEA or 2026-08-01 for EEA applicants with foreign diplomas; passed",
        "timeline_risk": "high",
        "deadline_notes": bi(
            "VUB's 2026/27 foreign-diploma deadlines are 1 April for non-EEA applicants and 1 August for EEA applicants. The dates have passed and must not be reused as next-cycle predictions.",
            "VUB'nin 2026/27 yabancı diploma son tarihleri AEA dışı adaylar için 1 Nisan, AEA adayları için 1 Ağustos'tur. Tarihler geçmiştir ve sonraki dönem tahmini olarak yeniden kullanılmamalıdır.",
        ),
    })
    record["living_profile"].update({
        "monthly_living_cost_eur_estimated": 1000,
        "average_room_rent_eur_min": 500,
        "average_room_rent_eur_max": 650,
        "housing_difficulty": "high",
        "living_risk": "high",
        "housing_notes": bi(
            "VUB advises foreign students to provide about EUR 1,000/month excluding tuition and course materials, and lists EUR 500-650/month accommodation among its cost examples. First-month registration, document, temporary-accommodation and housing-guarantee costs can be extra.",
            "VUB, yabancı öğrencilerin öğrenim ücreti ve ders materyalleri hariç ayda yaklaşık 1.000 EUR ayırmasını önerir; maliyet örneklerinde konaklamayı ayda 500-650 EUR olarak listeler. İlk ay kayıt, belge, geçici konaklama ve konut teminatı masrafları ek olabilir.",
        ),
    })
    profile = record["source_profile"]
    for item in [
        src(programme, "VUB MSc Electromechanical Engineering: Aeronautics track", "official_curriculum_page", ["curriculum", "tracks", "courses"], "Official track page describes the English 120-ECTS Aeronautics route with common core, track courses and thesis.", "Resmî yol sayfası ortak çekirdek, yola özgü dersler ve tez içeren İngilizce 120 AKTS Havacılık yolunu tanımlar."),
        src(scholarship, "VUB Master Mind scholarship programme", "official_scholarship_page", ["scholarship", "funding", "eligibility", "deadline"], "Current VUB call gives EUR 10,020/year, reduced tuition, acceptance/GPA/English conditions and 26 March 2026 deadline.", "Güncel VUB çağrısı yıllık 10.020 EUR, indirilmiş ücret, kabul/GNO/İngilizce koşulları ve 26 Mart 2026 son tarihini verir."),
        src(deadlines, "VUB application deadlines for foreign diplomas", "official_admission_page", ["admission", "deadline", "application_timeline", "non_eu_eligibility"], "VUB publishes 2026/27 1 April non-EEA and 1 August EEA foreign-diploma deadlines.", "VUB 2026/27 için yabancı diplomalarda 1 Nisan AEA dışı ve 1 Ağustos AEA son tarihlerini yayımlar."),
        src(living, "VUB estimated costs for foreign students", "official_housing_page", ["housing", "living", "living_profile"], "VUB advises a EUR 1,000 monthly foreign-student budget and lists EUR 500-650 monthly accommodation examples.", "VUB aylık 1.000 EUR yabancı öğrenci bütçesi önerir ve aylık 500-650 EUR konaklama örnekleri listeler."),
    ]:
        add(profile, item)
    profile.update({"official_curriculum_page": programme, "official_scholarship_page": scholarship, "official_admission_page": deadlines, "official_housing_page": living, "last_verified": CHECKED, "needs_verification": False})
    profile.setdefault("field_confidence", {}).update({"curriculum": "high", "scholarship": "high", "admission": "high", "deadlines": "high", "housing": "high", "living_profile": "high"})


path, raw, rows = load()
ugent(get(rows, "ugent"))
uclouvain(get(rows, "uclouvain"))
vub(get(rows, "vub-brussels"))
newline = "\r\n" if "\r\n" in raw else "\n"
path.write_text(json.dumps(rows, ensure_ascii=False, indent=2).replace("\n", newline) + newline, encoding="utf8")
print("Updated UGent, UCLouvain TFMASA and VUB with current official 2026 evidence.")
