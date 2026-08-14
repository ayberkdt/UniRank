"""Apply checked replacements for Austrian, UBI, and Russian candidate URLs."""

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


def save(path: Path, payload) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def source(url: str, title: str, source_type: str, fields: list[str], *, access="ok", confidence="high", notes=None) -> dict:
    return {
        "url": url,
        "title": title,
        "source_type": source_type,
        "access_status": access,
        "last_checked": CHECKED,
        "relevant_fields": fields,
        "confidence": confidence,
        "notes": notes or bi("Current official source checked for the stated fields.", "Güncel resmî kaynak belirtilen alanlar için kontrol edildi."),
    }


def remove_url(record: dict, url: str) -> None:
    log = record["source_profile"].setdefault("source_log", [])
    log[:] = [item for item in log if item.get("url") != url]


def upsert_sources(record: dict, items: list[dict]) -> None:
    log = record["source_profile"].setdefault("source_log", [])
    for replacement in items:
        key = (replacement.get("url"), replacement.get("source_type"))
        log[:] = [item for item in log if (item.get("url"), item.get("source_type")) != key]
        log.append(replacement)


# FHWN: replace dead department news and add direct non-EU evidence.
path, payload, row = load_record("austria.json", "austria_fhwn_msc_aerospace")
fhwn = "https://www.fhwn.ac.at/en/studyprogramme/master-aerospace-engineering"
remove_url(row, "https://www.fhwn.ac.at/en/news/neue-studiengangsleitung-fuer-aerospace-engineering")
upsert_sources(row, [
    source(
        fhwn,
        "FHWN Aerospace Engineering 2026/27 admission and non-EU route",
        "official_admission_page",
        ["admission", "non_eu_eligibility", "language", "deadline"],
        notes=bi(
            "The programme page publishes the third-country fee and deadline, English thresholds, engineering prerequisites and interview route, establishing a direct non-EU application path.",
            "Program sayfası üçüncü ülke ücretini ve son tarihini, İngilizce eşiklerini, mühendislik ön koşullarını ve mülakat yolunu yayımlayarak doğrudan AB dışı başvuru yolunu doğrular.",
        ),
    ),
    source(
        fhwn,
        "FHWN Aerospace Engineering curriculum, laboratories and projects 2026/27",
        "official_department_page",
        ["research", "department", "labs", "industry"],
        notes=bi(
            "The current page lists the complete 120-ECTS curriculum, laboratories, CubeSat/aircraft projects and named FOTEC/ESA-linked activity. Company employment examples are not treated as partnership proof beyond explicitly described cooperation.",
            "Güncel sayfa 120 AKTS'lik tam ders planını, laboratuvarları, CubeSat/uçak projelerini ve adı verilen FOTEC/ESA bağlantılı faaliyeti listeler. Şirket istihdam örnekleri, açıkça açıklanan iş birliğinin ötesinde ortaklık kanıtı sayılmaz.",
        ),
    ),
])
row["eligibility_profile"]["eligible_for_non_eu"] = True
row["source_profile"]["field_confidence"].update({"admission": "high", "deadlines": "high", "research": "high"})
row["source_profile"]["official_admission_page"] = fhwn
write_notes = row["decision_summary"].setdefault("application_reality", bi("", ""))
if isinstance(write_notes, dict):
    write_notes.update(bi(
        "A third-country applicant is eligible through the published route, but the 31 March 2026 deadline has passed and must not be reused for a later intake.",
        "Üçüncü ülke adayı yayımlanmış yoldan uygundur; ancak 31 Mart 2026 son tarihi geçmiştir ve sonraki dönem için yeniden kullanılamaz.",
    ))
save(path, payload)


# Austrian adjacent programmes already have current replacement pages; remove
# only the dead predecessor URLs so they cannot remain primary evidence.
for record_id, dead_url, current_url in (
    ("AT-TUW-INFOCOM-EN", "https://www.tuwien.at/en/studies/studies/master-programmes/information-and-communication-engineering", "https://www.tuwien.at/en/studies/studies/master-programmes/electrical-engineering/information-and-communication-engineering"),
    ("AT-LEOBEN-ADVMAT-EN", "https://www.unileoben.ac.at/en/studies/master-programmes/advanced-materials-science/", "https://www.unileoben.ac.at/en/studying/graduate-studies/materials/advanced-materials-science-and-engineering-en/"),
    ("AT-FHOO-MECH-DE", "https://www.fh-ooe.at/en/wels-campus/degree-programmes/master/mechanical-engineering/", "https://fh-ooe.at/en/degree-programs/mechanical-engineering-master"),
):
    path, payload, row = load_record("austria.json", record_id)
    remove_url(row, dead_url)
    row["program_url"] = current_url
    row["source_profile"]["official_program_page"] = current_url
    save(path, payload)


# UBI Aeronautical Engineering: current programme, curriculum, language, and housing.
path, payload, row = load_record("portekiz.json", "ubi-covilha")
ubi_program = "https://www.ubi.pt/curso/1103"
ubi_curriculum = "https://www.ubi.pt/PlanoDeEstudos/1103/1686/2025"
ubi_language = "https://www.ubi.pt/Disciplina/10412/2025/"
ubi_housing = "https://www.ubi.pt/Entidade/living_covilha"
remove_url(row, "https://www.ubi.pt/en/course/1103")
remove_url(row, "https://www.ubi.pt/en/page/living_covilha")
upsert_sources(row, [
    source(
        ubi_program,
        "UBI Aeronautical Engineering second-cycle programme 2026",
        "official_program_page",
        ["program", "admission", "non_eu_eligibility"],
        notes=bi(
            "The current official programme identifies the second-cycle Aeronautical Engineering degree, 60 places for 2026, its aerospace department and laboratories. UBI's current programme catalogue states that holders of a national or foreign first-cycle equivalent may apply.",
            "Güncel resmî program ikinci kademe Aeronautical Engineering derecesini, 2026 için 60 kontenjanı, havacılık-uzay bölümünü ve laboratuvarlarını tanımlar. UBI'nin güncel program kataloğu ulusal veya yabancı birinci kademe eşdeğer diploma sahiplerinin başvurabileceğini belirtir.",
        ),
    ),
    source(
        ubi_curriculum,
        "UBI Aeronautical Engineering second-cycle study plan 2025/26",
        "official_curriculum_page",
        ["curriculum"],
        notes=bi(
            "The official 120-ECTS study plan lists CFD, astrodynamics, navigation and avionics, gas dynamics, a 42-ECTS dissertation/project and optional space systems, propulsion, structures and trajectory control.",
            "Resmî 120 AKTS çalışma planı HAD, astrodinamik, seyrüsefer ve aviyonik, gaz dinamiği, 42 AKTS tez/proje ile uzay sistemleri, itki, yapılar ve yörünge kontrolü seçeneklerini listeler.",
        ),
    ),
    source(
        ubi_language,
        "UBI Aeronautical Engineering dissertation/project language 2025/26 (Portuguese)",
        "official_curriculum_page",
        ["language", "curriculum"],
        notes=bi(
            "The current required dissertation/project module states Portuguese delivery. This does not establish an English-taught degree.",
            "Güncel zorunlu tez/proje modülü Portekizce yürütümü belirtir. Bu, İngilizce yürütülen bir derece anlamına gelmez.",
        ),
    ),
    source(
        ubi_housing,
        "UBI living in Covilhã and student residences",
        "official_housing_page",
        ["housing", "living"],
        notes=bi(
            "The current page lists seven residences, 808 beds and published student price examples. Availability must be requested; the figures do not guarantee a room.",
            "Güncel sayfa yedi yurdu, 808 yatağı ve yayımlanmış öğrenci fiyat örneklerini listeler. Müsaitlik ayrıca sorulmalıdır; rakamlar oda garantisi değildir.",
        ),
    ),
])
row["program_url"] = ubi_program
row["program_status"] = "active"
row["duration_years"] = 2
row["ects"] = 120
row["teaching_language"] = ["Portuguese"]
row["language_profile"].update({
    "teaching_language": ["Portuguese"],
    "english_required": None,
    "english_level_required": None,
    "language_risk": "high",
    "mixed_language_warning": bi(
        "A current required-module record shows Portuguese teaching; do not treat an English catalogue interface as proof of an English-taught programme.",
        "Güncel bir zorunlu modül kaydı Portekizce öğretimi gösterir; İngilizce katalog arayüzünü İngilizce programın kanıtı saymayın.",
    ),
})
row["eligibility_profile"]["eligible_for_non_eu"] = True
row["curriculum_profile"].update({
    "curriculum_url": ubi_curriculum,
    "thesis_required": True,
    "mandatory_courses": ["Engineering Optimisation", "Aerospace Materials", "Aircraft Operations and Flight Safety", "Computational Fluid Dynamics", "Astrodynamics", "Navigation and Avionics", "Rotorcraft Devices", "Gas Dynamics", "Air Transport Economics and Management", "Dissertation or Project (42 ECTS)"],
    "elective_courses": ["Space Systems Engineering", "Propulsion III", "Flight Identification and Control", "Advanced Structural Analysis", "Trajectory Optimisation and Control", "Turbulence and Combustion"],
})
row["living_profile"].update({
    "student_housing_available": True,
    "housing_access": "priority",
    "housing_application_separate": True,
    "student_housing_competitiveness": "Availability must be confirmed with UBI accommodation services; preference rules apply.",
    "housing_difficulty": "unknown",
    "housing_notes": bi(
        "UBI lists seven residences and 808 beds. Published examples include EUR 100/month for a double room, EUR 125 for a single room and EUR 220 for a one-bedroom apartment; some utilities vary by unit. These are residence prices, not a guarantee of allocation.",
        "UBI yedi yurt ve 808 yatak listeler. Yayımlanan örnekler çift kişilik oda için aylık 100 EUR, tek kişilik oda için 125 EUR ve tek yatak odalı daire için 220 EUR'dur; bazı birimlerde faturalar değişir. Bunlar yurt fiyatıdır, tahsis garantisi değildir.",
    ),
    "average_room_rent_eur_min": 100,
    "average_room_rent_eur_max": 125,
    "average_room_rent_scope_label": "UBI residence room examples; not private-market rent",
})
row["source_profile"].update({
    "official_program_page": ubi_program,
    "official_curriculum_page": ubi_curriculum,
    "official_housing_page": ubi_housing,
})
row["source_profile"]["field_confidence"].update({"program_basic_info": "high", "language": "medium", "admission": "medium", "curriculum": "high", "housing": "high"})
row["scoring_inputs"].setdefault("hard_filter_flags", {})["english_only_compatible"] = False
row["scoring_inputs"]["hard_filter_flags"]["requires_local_language"] = True
save(path, payload)


# Replace two dead Russian candidate-level admissions links. These records are
# still not programme records and remain needs_revision; no programme facts are inferred.
for filename, record_id, dead, replacement, title, access in (
    ("rusya.json", "tomsk-polytechnic-tpu", "https://tpu.ru/en/admissions", "https://tpu.ru/en/education/admission/", "Tomsk Polytechnic University international admission policy", "ok"),
    ("rusya.json", "kazan-federal-kfu", "https://eng.kpfu.ru/admission/", "https://admissions.kpfu.ru/wp-content/uploads/2026/06/guideline-on-admission-kfu_eng.pdf", "Kazan Federal University 2026 international admission guideline", "pdf"),
):
    path, payload, row = load_record(filename, record_id)
    item = next(
        item
        for item in row["source_profile"]["source_log"]
        if item.get("url") in {dead, replacement}
    )
    item.update(source(replacement, title, "official_admission_page", ["admission", "non_eu_eligibility", "visa"], access=access, confidence="medium", notes=bi(
        "This is a university-level international-admission source only. It does not prove that a specific aerospace/space Master's programme exists.",
        "Bu yalnızca üniversite düzeyinde uluslararası kabul kaynağıdır. Belirli bir havacılık/uzay yüksek lisans programının varlığını kanıtlamaz.",
    )))
    item.pop("final_url", None)
    save(path, payload)

print("Applied replacement-source research batch 2: Austria, UBI, TPU, and KFU.")
