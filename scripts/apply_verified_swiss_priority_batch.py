"""Add current official decision data to two Swiss Master records."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CHECKED = "2026-07-15"


def bi(en: str, tr: str) -> dict[str, str]:
    return {"en": en, "tr": tr}


def note(url: str, title: str, kind: str, fields: list[str], en: str, tr: str, confidence: str = "high") -> dict[str, Any]:
    return {"url": url, "title": title, "source_type": kind, "access_status": "ok", "last_checked": CHECKED, "relevant_fields": fields, "confidence": confidence, "notes": bi(en, tr)}


def data(name: str) -> tuple[Path, str, list[dict[str, Any]]]:
    path = ROOT / "data_base" / name
    raw = path.read_text(encoding="utf-8")
    doc = json.loads(raw)
    return path, raw, doc if isinstance(doc, list) else doc.get("programs", doc.get("universities", []))


def save(path: Path, raw: str) -> None:
    # The in-memory list is the JSON document for isvicre.json.
    nl = "\r\n" if "\r\n" in raw else "\n"
    path.write_text(json.dumps(ROWS, ensure_ascii=False, indent=2).replace("\n", nl) + nl, encoding="utf-8")


def get(identifier: str) -> dict[str, Any]:
    return next(row for row in ROWS if row.get("id") == identifier)


def add_source(profile: dict[str, Any], item: dict[str, Any]) -> None:
    profile["source_log"] = [x for x in profile.get("source_log", []) if not (isinstance(x, dict) and x.get("url") == item["url"] and x.get("source_type") == item["source_type"])]
    profile["source_log"].append(item)


def epfl() -> None:
    row = get("ch-epfl-mech-msc")
    fellowship = "https://www.epfl.ch/education/master/master-excellence-fellowships/how-to-apply/"
    budget = "https://www.epfl.ch/education/studies/en/financing-study/"
    row["scholarship_profile"].update({
        "available_types": ["EPFL Excellence Fellowship (competitive)"],
        "regional_scholarship_available": True,
        "regional_scholarship_name": "EPFL Excellence Fellowship",
        "non_eu_eligible": True,
        "scholarship_deadline": "15 December or 31 March (external-candidate Master rounds; verify cycle year)",
        "scholarship_application_url": fellowship,
        "funding_amount_chf_per_semester": 10000,
        "funding_notes": bi("Eligible Master applicants can request consideration in the online admission application. EPFL publishes CHF 10,000 per semester for up to four semesters and a residence-room reservation for selected external candidates. It is competitive, not guaranteed.", "Uygun Master adaylari cevrim ici kabul basvurusunda degerlendirme isteyebilir. EPFL en fazla dort donem icin donem basina 10.000 CHF ve secilen dis adaylara yurt oda rezervasyonu yayimlar. Rekabetcidir, garanti degildir."),
        "verification_notes": bi("The fellowship does not remove the applicant's responsibility to budget for tuition and rent.", "Burs, adayın ogrenim ucreti ve kira butcesi sorumlulugunu ortadan kaldirmaz."),
    })
    row["application_timeline_profile"].update({
        "academic_year": "Recurring Master application rounds; confirm live-cycle dates before submission",
        "intake_terms": ["September"],
        "application_rounds": ["First round: 15 December", "Second round: 31 March"],
        "non_eu_deadline": "15 December or 31 March (external Master application rounds; EPFL advises visa applicants to use December)",
        "application_deadline": "31 March (second round; first round 15 December)",
        "scholarship_deadline": "15 December or 31 March (same Master application rounds)",
        "timeline_risk": "high",
        "deadline_notes": bi("All Master's programmes start mid-September. EPFL advises visa-needing candidates to apply in December for an earlier decision; no future-cycle date is inferred.", "Tum Master programlari Eylul ortasinda baslar. EPFL vize gereken adaylara daha erken karar icin Aralikta basvurmayi onerir; gelecek donem tarihi cikarimla uretilmez."),
    })
    row["living_profile"].update({
        "monthly_living_cost_chf_per_month_min": 2107,
        "monthly_living_cost_chf_per_month_max": 2107,
        "monthly_living_cost_chf_per_month": 2107,
        "average_room_rent_chf_per_month_min": 900,
        "average_room_rent_chf_per_month_max": 900,
        "official_student_total_budget_chf_per_year": 25219,
        "living_risk": "high",
        "housing_difficulty": "high",
        "housing_notes": bi("EPFL's current foreign-student planning budget is CHF 2,107/month excluding tuition, with CHF 900/month housing. It also flags lease deposits and blocked months; this is a budget, not a room offer.", "EPFL'nin guncel yabanci ogrenci planlama butcesi ogrenim ucreti haric aylik 2.107 CHF; konut icin aylik 900 CHF'dir. Kira depozitosu ve bloke aylar uyarisi da verir; bu oda teklifi degil butcedir."),
    })
    profile = row.setdefault("source_profile", {})
    add_source(profile, note(fellowship, "EPFL Master Excellence Fellowships", "official_scholarship_page", ["scholarship", "funding", "deadline"], "Official page gives eligibility, value, room-reservation benefit and Master application rounds.", "Resmi sayfa uygunluk, tutar, oda rezervasyonu avantaji ve Master basvuru turlarini verir."))
    add_source(profile, note(fellowship, "EPFL external Master application rounds", "official_admission_page", ["admission", "deadline", "non_eu_eligibility"], "Official page gives the 15 December and 31 March external-candidate rounds.", "Resmi sayfa dis adaylar icin 15 Aralik ve 31 Mart turlarini verir."))
    add_source(profile, note(budget, "EPFL foreign-student budget", "official_cost_of_living_page", ["housing", "living"], "Official foreign-student budget lists CHF 2,107/month excluding tuition and CHF 900 housing.", "Resmi yabanci ogrenci butcesi ogrenim ucreti haric aylik 2.107 CHF ve 900 CHF konut listeler."))
    profile.update({"official_scholarship_page": fellowship, "official_admission_page": fellowship, "official_cost_of_living_page": budget, "last_verified": CHECKED})
    profile.setdefault("field_confidence", {}).update({"scholarship": "high", "application_timeline_profile": "high", "living_profile": "high", "housing": "high"})


def zhaw() -> None:
    row = get("ch-zhaw-aviation-mse")
    mse = "https://www.zhaw.ch/en/engineering/study/masters-degree-programme?pk_kwd=MSE"
    living = "https://www.zhaw.ch/en/engineering/study/international-office/studying-in-switzerland/living-in-switzerland"
    row["teaching_language"] = ["English"]
    row["language_profile"].update({"teaching_language": ["English"], "english_required": True, "language_risk": "low", "verification_notes": bi("The official MSE page explicitly says language of instruction: English.", "Resmi MSE sayfasi egitim dilinin Ingilizce oldugunu acikca belirtir.")})
    row["cost_profile"].update({"tuition_chf_per_semester": 720, "tuition_chf_per_year_min": 1440, "tuition_chf_per_year_max": 1440, "tuition_basis": "published MSE base fee plus additional study costs", "verification_notes": bi("The MSE page publishes CHF 720 per semester plus additional study costs. It does not establish a separate non-EU surcharge, so this remains a published base fee rather than an assumed international total.", "MSE sayfasi donem basina 720 CHF ve ek ogrenim giderleri yayimlar. Ayrı bir AB disi ek ucret gostermedigi icin bu, varsayilan uluslararasi toplam degil yayimlanmis taban ucrettir.")})
    row["scholarship_profile"].update({"regional_scholarship_available": False, "funding_status": "No general ZHAW MSE degree scholarship verified", "funding_notes": bi("ZHAW MSE admission material says ZHAW does not grant scholarships. A separate School of Engineering exchange scholarship is not represented as funding for an enrolled MSE degree applicant.", "ZHAW MSE kabul materyali ZHAW'nin burs vermedigini belirtir. Ayrı School of Engineering degisim bursu, kayitli MSE derece adayi icin finansman sayilmaz."), "verification_notes": bi("A verified absence is shown rather than a fictional degree scholarship.", "Hayali derece bursu yerine dogrulanmis yokluk gosterilir.")})
    row["application_timeline_profile"].update({"academic_year": "Recurring MSE schedule; verify exact intake day in live form", "intake_terms": ["Autumn", "Spring"], "application_rounds": ["Autumn intake: end of April", "Spring intake: end of October"], "non_eu_deadline": "End of April (autumn) or end of October (spring), or as agreed", "application_deadline": "End of April (autumn) or end of October (spring), or as agreed", "timeline_risk": "medium", "deadline_notes": bi("ZHAW publishes only end-of-month timing, so no exact or future-cycle calendar day is invented.", "ZHAW yalnizca ay sonu zamanlamasi yayimlar; kesin veya gelecek donem takvim gunu uydurulmaz.")})
    row["living_profile"].update({"monthly_living_cost_chf_per_month_min": 1390, "monthly_living_cost_chf_per_month_max": 2280, "average_room_rent_chf_per_month_min": 500, "average_room_rent_chf_per_month_max": 800, "living_risk": "high", "housing_difficulty": "high", "housing_notes": bi("ZHAW School of Engineering publishes a CHF 1,390-2,280 monthly planning budget, including CHF 500-800 rent. It is incoming-student guidance, not a guaranteed MSE room price.", "ZHAW School of Engineering, 500-800 CHF kira dahil aylik 1.390-2.280 CHF planlama butcesi yayimlar. Gelen ogrenci rehberidir, garanti MSE oda fiyati degildir.")})
    profile = row.setdefault("source_profile", {})
    add_source(profile, note(mse, "ZHAW MSE programme", "official_program_page", ["program", "language", "tuition", "deadline"], "Official page gives English instruction, CHF 720 per semester and end-April/end-October timing.", "Resmi sayfa Ingilizce egitim, donem basina 720 CHF ve Nisan/Ekim sonu zamanlamasini verir."))
    add_source(profile, note(mse, "ZHAW MSE published base tuition", "official_tuition_page", ["tuition"], "Published base semester fee; no foreign surcharge is stated on the checked page.", "Yayimlanmis taban donem ucreti; kontrol edilen sayfada yabanci ek ucreti belirtilmez."))
    add_source(profile, note(living, "ZHAW School of Engineering living costs", "official_cost_of_living_page", ["housing", "living"], "Official planning range is CHF 1,390-2,280/month with CHF 500-800 rent.", "Resmi planlama araligi, 500-800 CHF kira ile aylik 1.390-2.280 CHF'dir."))
    profile.update({"official_program_page": mse, "official_tuition_page": mse, "official_cost_of_living_page": living, "last_verified": CHECKED})
    profile.setdefault("field_confidence", {}).update({"language": "high", "tuition": "medium", "scholarship": "high", "application_timeline_profile": "medium", "living_profile": "medium", "housing": "medium"})


PATH, RAW, ROWS = data("isvicre.json")
epfl()
zhaw()
save(PATH, RAW)
print("Updated EPFL Mechanical Engineering and ZHAW MSE Aviation with checked official sources.")
