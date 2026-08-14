"""Apply checked replacements for the first broken-link research batch."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data_base"
CHECKED = "2026-08-14"


def bi(en: str, tr: str) -> dict[str, str]:
    return {"en": en, "tr": tr}


def load_record(filename: str, record_id: str):
    path = DATA / filename
    payload = json.loads(path.read_text(encoding="utf-8"))
    rows = payload.get("programs", payload.get("universities", payload)) if isinstance(payload, dict) else payload
    record = next(row for row in rows if row.get("id") == record_id)
    return path, payload, record


def write(path: Path, payload) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=4) + "\n", encoding="utf-8")


def replace_source(record: dict, old_url: str, *, url: str, title: str, source_type: str, fields: list[str], access: str = "ok", notes=None) -> None:
    source = next(item for item in record["source_profile"]["source_log"] if item.get("url") == old_url)
    source.update({
        "url": url,
        "title": title,
        "source_type": source_type,
        "access_status": access,
        "last_checked": CHECKED,
        "relevant_fields": fields,
        "confidence": "high",
        "notes": notes or bi("Current official source checked for the stated fields.", "Güncel resmî kaynak belirtilen alanlar için kontrol edildi."),
    })
    source.pop("final_url", None)


def append_source(record: dict, *, url: str, title: str, source_type: str, fields: list[str], access: str = "ok", notes=None) -> None:
    record["source_profile"].setdefault("source_log", []).append({
        "url": url,
        "title": title,
        "source_type": source_type,
        "access_status": access,
        "last_checked": CHECKED,
        "relevant_fields": fields,
        "confidence": "high",
        "notes": notes or bi("Current official source checked for the stated fields.", "Güncel resmî kaynak belirtilen alanlar için kontrol edildi."),
    })


# KU Leuven Master of Space Studies: replace archived 2025 admission route.
path, payload, row = load_record("belcika.json", "ku-leuven")
ku_admission = "https://onderwijsaanbod.kuleuven.be/opleidingen/e/SC_51016979/toelatingsvoorwaarden"
replace_source(
    row,
    "https://onderwijsaanbod.kuleuven.be/2025/opleidingen/e/SC_51016979/toelatingsvoorwaarden",
    url=ku_admission,
    title="KU Leuven Master of Space Studies admission requirements 2026-2027",
    source_type="official_admission_page",
    fields=["language", "admission", "non_eu_eligibility"],
    notes=bi(
        "The 2026-2027 programme guide states the prior-Master requirement, international admission route, CV and motivation-letter requirements, possible interview, English-test thresholds and listed exemption countries.",
        "2026-2027 program rehberi önceki yüksek lisans şartını, uluslararası kabul yolunu, CV ve motivasyon mektubu şartlarını, olası mülakatı, İngilizce sınav eşiklerini ve belirtilen muaf ülke listesini açıklar.",
    ),
)
row["teaching_language"] = ["English"]
row["language_profile"]["teaching_language"] = ["English"]
row["language_profile"]["language_risk"] = "low"
row["source_profile"]["official_admission_page"] = ku_admission
row["source_profile"]["field_confidence"].update({"language": "high", "admission": "high"})
write(path, payload)


# Sapienza: replace a dead 2022 catalogue URL with the live 33484 catalogue.
path, payload, row = load_record("italy.json", "sapienza_space_astronautical_msc")
sapienza_program = "https://corsidilaurea.uniroma1.it/en/course/33484"
replace_source(
    row,
    "https://corsidilaurea.uniroma1.it/en/corso/2022/31825/home",
    url=sapienza_program,
    title="Sapienza Space and Astronautical Engineering course catalogue 33484",
    source_type="official_program_page",
    fields=["program", "language"],
    notes=bi(
        "The live catalogue shows 2026-2027 announcements and identifies programme 33484 as a two-year, English-taught LM-20 Master's degree.",
        "Canlı katalog 2026-2027 duyurularını gösterir ve 33484 kodlu programı iki yıllık, İngilizce yürütülen LM-20 yüksek lisans derecesi olarak tanımlar.",
    ),
)
row["program_url"] = sapienza_program
row["program_status"] = "active"
row["duration_years"] = 2
row["teaching_language"] = ["English"]
row["language_profile"]["teaching_language"] = ["English"]
row["language_profile"]["language_risk"] = "low"
row["source_profile"]["official_program_page"] = sapienza_program
row["source_profile"]["field_confidence"].update({"program_basic_info": "high", "language": "high"})
write(path, payload)


# TU Darmstadt: current specific module handbook dated 1 March 2026.
path, payload, row = load_record("almanya.json", "de_darmstadt_aerospace_engineering_msc")
darmstadt_curriculum = "https://www.maschinenbau.tu-darmstadt.de/media/maschinenbau/dokumente_2/studieren_1/neue_pruefungsordnungen_2021/MHB_Master_AE_2503_01.pdf"
replace_source(
    row,
    "https://www.tu-darmstadt.de/media/daa_responsives_design/02_studium_medien/01_studieninteressierte_medien/02_studienangebot_medien/master_of_science_1/aerospace_engineering__msc/aerospace_engineering__msc.de.pdf",
    url=darmstadt_curriculum,
    title="TU Darmstadt Aerospace Engineering specific module handbook (1 March 2026)",
    source_type="official_curriculum_page",
    fields=["curriculum"],
    access="pdf",
    notes=bi(
        "The 97-page official handbook lists the thesis, compulsory project work and current aerospace elective modules including CFD, structures, avionics, flight mechanics, space systems and propulsion.",
        "97 sayfalık resmî el kitabı tezi, zorunlu proje çalışmasını ve HAD, yapılar, aviyonik, uçuş mekaniği, uzay sistemleri ve itki dâhil güncel havacılık-uzay seçmeli modüllerini listeler.",
    ),
)
row["curriculum_profile"]["curriculum_url"] = darmstadt_curriculum
row["source_profile"]["official_curriculum_page"] = darmstadt_curriculum
row["source_profile"]["field_confidence"]["curriculum"] = "high"
write(path, payload)


# Ghent: current programme brochure, deadline page, and explicit GRE rule.
path, payload, row = load_record("belcika.json", "ugent")
old_brochure = "https://studiekiezer.ugent.be/infobrochure/en/EMMECH/2025"
new_brochure = "https://studiekiezer.ugent.be/infobrochure/en/EMMECH/2026"
source_log = row["source_profile"]["source_log"]
# The old brochure was cloned as tuition/scholarship evidence even though it
# merely linked elsewhere. Remove those unsupported classifications.
source_log[:] = [
    source for source in source_log
    if not (source.get("url") == old_brochure and source.get("source_type") in {"official_tuition_page", "official_scholarship_page"})
]
for source in source_log:
    if source.get("url") == old_brochure:
        source["url"] = new_brochure
        source["access_status"] = "pdf"
        source["last_checked"] = CHECKED
        source["title"] = "Ghent University Mechanical and Electrical Systems Engineering brochure 2026-2027"
        source.pop("final_url", None)

ugent_deadline = "https://www.ugent.be/prospect/en/administration/application/application-degree/deadlines.htm"
replace_source(
    row,
    "https://www.ugent.be/en/education/degree/degree-student/application-deadline",
    url=ugent_deadline,
    title="Ghent University degree-student application deadlines",
    source_type="official_admission_page",
    fields=["deadline", "admission", "non_eu_eligibility"],
    notes=bi(
        "The current official rule requires a complete application before 1 April for applicants needing a visa and before 1 June for applicants not needing a visa.",
        "Güncel resmî kural vize gereken adaylarda eksiksiz başvuruyu 1 Nisan'dan, vize gerekmeyen adaylarda 1 Haziran'dan önce ister.",
    ),
)
ugent_apply = "https://www.ugent.be/plone_portal/prospect/en/administration/application/application-degree/apply.htm"
append_source(
    row,
    url=ugent_apply,
    title="Ghent University degree-student application documents and GRE policy",
    source_type="official_admission_page",
    fields=["admission", "non_eu_eligibility", "gre"],
    notes=bi(
        "The current application page states that a GRE valid for no more than five years is required for non-EEA diploma holders applying to Faculty of Engineering and Architecture Master's programmes.",
        "Güncel başvuru sayfası, Mühendislik ve Mimarlık Fakültesi yüksek lisanslarına başvuran AEA dışı diploma sahipleri için en fazla beş yıl geçerli GRE sonucu gerektiğini belirtir.",
    ),
)
row["application_timeline_profile"].update({
    "academic_year": "2026/2027",
    "application_rounds": ["Visa-required applicants: complete application before 1 April", "Applicants not requiring a visa: complete application before 1 June"],
    "non_eu_deadline": "Before 1 April for applicants who need a visa; before 1 June for applicants who do not need a visa",
    "winter_deadline": "Before 1 April (visa-required) / before 1 June (no visa required)",
    "application_deadline": "Before 1 April (visa-required) / before 1 June (no visa required)",
    "deadline_status": "recurring",
    "timeline_risk": "medium",
    "deadline_notes": bi(
        "The official page publishes a recurring applicant-group rule rather than a dated future-cycle estimate. Confirm the live page for the target cycle.",
        "Resmî sayfa tarih uydurulmuş gelecek dönem tahmini yerine aday grubuna göre tekrarlayan kural yayımlar. Hedef dönem için canlı sayfayı doğrulayın.",
    ),
})
row["eligibility_profile"]["gre"] = {
    "policy": "required",
    "test_type": "GRE General (official page does not publish a programme-specific minimum)",
    "minimum_scores": {},
    "recommended_scores": {},
    "validity_rule": "Maximum five years old",
    "waiver_rules": [],
    "source_ids": [],
}
if "GRE result (required for non-EEA diploma holders applying to the Faculty of Engineering and Architecture)" not in row["eligibility_profile"].setdefault("required_documents", []):
    row["eligibility_profile"]["required_documents"].append("GRE result (required for non-EEA diploma holders applying to the Faculty of Engineering and Architecture)")
row["source_profile"]["official_program_page"] = new_brochure
row["source_profile"]["official_admission_page"] = ugent_apply
row["source_profile"]["field_confidence"].update({"program_basic_info": "high", "language": "high", "admission": "high", "deadlines": "high"})
write(path, payload)

print("Applied replacement-source research batch 1: KU Leuven, Sapienza, TU Darmstadt, and Ghent University.")
