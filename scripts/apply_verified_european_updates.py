"""Apply checked, first-party research updates collected on 2026-07-14.

Each update below is deliberately small: only facts supported by the cited
official page are written.  The general audit script can subsequently mark all
other unsupported fields as pending instead of making them look authoritative.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data_base"
CHECKED = "2026-07-14"


def source(url: str, title: str, source_type: str, fields: list[str], notes: str = "") -> dict[str, Any]:
    return {
        "url": url,
        "title": title,
        "source_type": source_type,
        "access_status": "ok",
        "last_checked": CHECKED,
        "relevant_fields": fields,
        "confidence": "high",
        "notes": notes,
    }


def find_record(payload: Any, record_id: str) -> dict[str, Any]:
    rows = payload if isinstance(payload, list) else payload.get("programs", payload.get("universities", []))
    for row in rows:
        if row.get("id") == record_id:
            return row
    raise KeyError(f"{record_id} not found")


def write_payload(path: Path, payload: Any) -> None:
    """Preserve the file's established JSON indentation."""
    source_text = path.read_bytes().decode("utf-8")
    if source_text.lstrip().startswith("["):
        match = re.search(r'^\s*\[\r?\n( +)\{', source_text)
    else:
        match = re.search(r'^\s*\{\r?\n( +)"', source_text)
    indent = len(match.group(1)) if match else 4
    newline = "\r\n" if "\r\n" in source_text else "\n"
    serialised = json.dumps(payload, ensure_ascii=False, indent=indent)
    path.write_bytes((serialised.replace("\n", newline) + newline).encode("utf-8"))


def update(record: dict[str, Any], values: dict[str, Any], sources: list[dict[str, Any]], confidence: dict[str, str]) -> None:
    for key, value in values.items():
        if isinstance(value, dict) and isinstance(record.get(key), dict):
            record[key].update(value)
        else:
            record[key] = value
    profile = record.setdefault("source_profile", {})
    existing = [item for item in profile.get("source_log", []) if isinstance(item, dict)]
    replacements = {
        (item.get("url"), item.get("source_type"), tuple(item.get("relevant_fields") or [])): item
        for item in sources
    }
    retained = [
        item for item in existing
        if (item.get("url"), item.get("source_type"), tuple(item.get("relevant_fields") or [])) not in replacements
    ]
    profile["source_log"] = retained + sources
    profile["last_verified"] = CHECKED
    profile.setdefault("field_confidence", {}).update(confidence)
    profile["needs_verification"] = True


def main() -> None:
    # KTH — programme, course tracks, 2027 cycle dates, fee and scholarship
    # eligibility checked directly at KTH.  We retain SEK instead of inventing
    # a volatile EUR conversion.
    path = DATA / "isvec.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    update(
        find_record(payload, "se-kth-aero-msc"),
        {
            "duration_years": 2,
            "ects": 120,
            "teaching_language": ["English"],
            "language_profile": {"teaching_language": ["English"], "language_risk": "low"},
            "eligibility_profile": {"eligible_for_non_eu": True},
            "cost_profile": {
                "tuition_eur_per_year_estimated": None,
                "tuition_eur_per_year_min": None,
                "tuition_eur_per_year_max": None,
                "total_academic_cost_eur_per_year_estimated": None,
                "tuition_non_eu_full_program": {"amount": 360000, "currency": "SEK", "basis": "full_program", "academic_year": "current page"},
                "application_fee": {"amount": 900, "currency": "SEK", "basis": "application"},
                "cost_notes": {"en": "KTH states the fee in SEK; no EUR conversion is stored.", "tr": "KTH ücreti SEK olarak yayımlar; EUR dönüşümü kaydedilmedi."},
            },
            "scholarship_profile": {
                "non_eu_eligible": True,
                "scholarship_names": ["KTH Scholarship", "Swedish Institute scholarship (eligible countries only)"],
                "funding_notes": {"en": "KTH Scholarship is open to fee-paying applicants and covers tuition for one or two years; SI eligibility is country-specific.", "tr": "KTH bursu ücret ödeyen adaylara açıktır ve bir veya iki yıl öğrenim ücretini kapsar; SI uygunluğu ülkeye özeldir."},
            },
            "application_timeline_profile": {
                "non_eu_deadline": "2027-01-15",
                "document_deadline": "2027-02-01",
                "deadline_notes": {"en": "For studies starting August 2027; verify the next cycle before applying.", "tr": "Ağustos 2027 başlangıcı içindir; başvuru öncesi sonraki dönemi doğrulayın."},
                "timeline_risk": "medium",
            },
            "curriculum_profile": {
                "tracks": ["Aeronautics", "Space", "Lightweight Structures", "Systems Engineering"],
                "curriculum_evidence": {"en": "All students take a mandatory course in each track before choosing a specialisation.", "tr": "Öğrenciler uzmanlık seçmeden önce her izden zorunlu ders alır."},
            },
            "category_profile": {
                "normalized_tags": ["aerodynamics", "space_systems", "aerospace_structures", "systems_engineering"],
                "evidence_basis": "Official KTH programme tracks, checked 2026-07-14.",
            },
        },
        [
            source("https://www.kth.se/en/studies/master/aerospace-engineering", "KTH MSc Aerospace Engineering", "official_program_page", ["program", "language", "deadline", "curriculum", "non_eu_eligibility"]),
            source("https://www.kth.se/en/2.985/aerospace-engineering/fees-aerospace-engineering-1.910116", "KTH fees and scholarships for Aerospace Engineering", "official_tuition_page", ["tuition"]),
            source("https://www.kth.se/en/2.985/aerospace-engineering/fees-aerospace-engineering-1.910116", "KTH fees and scholarships for Aerospace Engineering", "official_scholarship_page", ["scholarship"]),
            source("https://www.kth.se/en/studies/master/aerospace-engineering/courses-aerospace-engineering-1.412918", "KTH Aerospace Engineering courses", "official_curriculum_page", ["curriculum"]),
        ],
        {"program_basic_info": "high", "language": "high", "tuition": "high", "scholarship": "high", "curriculum": "high", "deadlines": "high"},
    )
    write_payload(path, payload)

    # Stuttgart — the English page is not evidence of English instruction: it
    # explicitly says German.  This correction is a key application-risk fix.
    path = DATA / "almanya.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    update(
        find_record(payload, "germany-stuttgart-msc-aerospace"),
        {
            "duration_years": 2,
            "ects": 120,
            "teaching_language": ["German"],
            "language_profile": {"teaching_language": ["German"], "language_risk": "high"},
            "application_timeline_profile": {"winter_deadline": "July 15", "summer_deadline": "January 15", "deadline_notes": {"en": "University page lists the application periods; verify the applicable cycle and applicant route.", "tr": "Üniversite sayfası başvuru dönemlerini listeler; geçerli dönemi ve aday rotasını doğrulayın."}},
            "curriculum_profile": {"tracks": ["Space flight technology and space utilization", "Experimental and numerical simulation methods", "System dynamics and automation engineering", "Drive and energy systems", "Artificial Intelligence in Aerospace Engineering"]},
            "research_profile": {"labs": ["Institute of Aerodynamics and Gas Dynamics (IAG)", "Institute of Flight Mechanics and Flight Control (IFR)", "Institute of Space Systems (IRS)", "Institute of Aircraft Propulsion Systems (ILA)", "Institute of Aerospace Thermodynamics (ITLR)"]},
            "category_profile": {"normalized_tags": ["aerodynamics", "flight_control", "space_systems", "propulsion", "aerospace_structures", "scientific_ai"]},
        },
        [source("https://www.uni-stuttgart.de/en/study/study-programs/Aerospace-Engineering-M.Sc-00001./", "University of Stuttgart Aerospace Engineering M.Sc.", "official_program_page", ["program", "language", "deadline", "curriculum", "research"]), source("https://www.uni-stuttgart.de/en/study/study-programs/Aerospace-Engineering-M.Sc-00001./", "University of Stuttgart Aerospace Engineering M.Sc.", "official_curriculum_page", ["curriculum"]), source("https://www.uni-stuttgart.de/en/study/study-programs/Aerospace-Engineering-M.Sc-00001./", "University of Stuttgart Aerospace Engineering M.Sc.", "official_department_page", ["research"])],
        {"program_basic_info": "high", "language": "high", "curriculum": "high", "research": "high", "deadlines": "medium"},
    )
    write_payload(path, payload)

    # ISAE-SUPAERO — official programme FAQ gives a useful all-in monthly
    # budget, explicitly separate from tuition.  Housing remains a capacity
    # risk, not a guessed room-rent figure.
    path = DATA / "fransa.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    update(
        find_record(payload, "france_isae_supaero_msc"),
        {
            "teaching_language": ["English"],
            "language_profile": {"teaching_language": ["English"], "language_risk": "low", "english_tests": ["TOEFL iBT 87", "TOEIC 785 (four skills) or 850 (listening/reading)", "IELTS Academic 6", "CAE/FCE 170", "Linguaskill 170"]},
            "eligibility_profile": {"required_previous_degree": ["Bachelor's degree or equivalent in mechanical engineering, mechatronics, aerospace, electronics, electrical engineering, computer science, telecommunications, or related science/engineering"], "required_documents": ["Diploma or enrolment certificate", "Three years of transcripts", "CV in English", "Cover letter in English", "English test result", "Two recommendation letters"], "application_fee": {"amount": 100, "currency": "EUR"}},
            "scholarship_profile": {"non_eu_eligible": None, "funding_notes": {"en": "Several excellence scholarships are offered to Master's candidates applying in the first application session; eligibility and current call must be checked.", "tr": "İlk başvuru oturumunda başvuran yüksek lisans adayları için çeşitli başarı bursları sunulur; uygunluk ve güncel çağrı doğrulanmalıdır."}},
            "living_profile": {"monthly_living_cost_eur_min": 900, "monthly_living_cost_eur_max": 1000, "monthly_living_cost_basis": "official all-in monthly budget: accommodation, food, transport, health insurance and miscellaneous", "housing_difficulty": "limited_on_campus_capacity", "housing_notes": {"en": "ISAE-SUPAERO prioritises international students for very limited on-campus housing and directs students to Toul'Box/Alteal options.", "tr": "ISAE-SUPAERO çok sınırlı kampüs konaklamasında uluslararası öğrencilere öncelik verir; Toul'Box/Alteal seçeneklerine yönlendirir."}},
            "application_timeline_profile": {"deadline_notes": {"en": "2026 intake is closed; the university says applications for 2027 open in October 2026.", "tr": "2026 dönemi kapalıdır; üniversite 2027 başvurularının Ekim 2026'da açılacağını belirtir."}, "timeline_risk": "medium"},
        },
        [source("https://www.isae-supaero.fr/en/programmes/masters-degree-in-aerospace-engineering/", "ISAE-SUPAERO Master's degree in Aerospace Engineering", "official_program_page", ["program", "language", "admission", "scholarship", "deadline", "housing"]), source("https://www.isae-supaero.fr/en/programmes/masters-degree-in-aerospace-engineering/", "ISAE-SUPAERO Master's degree in Aerospace Engineering", "official_admission_page", ["admission", "deadline"]), source("https://www.isae-supaero.fr/en/programmes/masters-degree-in-aerospace-engineering/", "ISAE-SUPAERO Master's degree in Aerospace Engineering", "official_scholarship_page", ["scholarship"]), source("https://www.isae-supaero.fr/en/programmes/masters-degree-in-aerospace-engineering/", "ISAE-SUPAERO Master's degree in Aerospace Engineering", "official_housing_page", ["housing"])],
        {"program_basic_info": "high", "language": "high", "admission": "high", "scholarship": "medium", "living": "high", "deadlines": "high"},
    )
    write_payload(path, payload)

    # Sapienza Space and Astronautical Engineering — active course catalogue.
    path = DATA / "italy.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    update(
        find_record(payload, "sapienza_space_astronautical_msc"),
        {"program_status": "active", "duration_years": 2, "ects": 120, "teaching_language": ["English"], "language_profile": {"teaching_language": ["English"], "language_risk": "low"}, "eligibility_profile": {"admission_mode": "Verification of requirements and personal preparation"}, "curriculum_profile": {"tracks": ["Space and astronautical engineering"]}},
        [source("https://corsidilaurea.uniroma1.it/en/corso/2022/31825/home", "Sapienza Space and astronautical engineering course catalogue", "official_program_page", ["program", "language", "admission", "curriculum"]), source("https://corsidilaurea.uniroma1.it/sites/default/files/offertaformativa/documenti_ufficiali/187/33484_e.pdf", "Sapienza 2025–26 admission procedures", "official_admission_page", ["admission"])],
        {"program_basic_info": "high", "language": "high", "admission": "high", "curriculum": "medium"},
    )
    # Politecnico di Torino — correction: its current Aerospace MSc is
    # Italian-taught despite an English-language web page.
    update(
        find_record(payload, "polito-msc-aerospace"),
        {"program_status": "active", "teaching_language": ["Italian"], "language_profile": {"teaching_language": ["Italian"], "language_risk": "high"}, "curriculum_profile": {"tracks": ["Aerostructures", "Propulsion systems", "Aeromechanics and systems", "Aero-gas dynamics", "Space"]}},
        [source("https://www.polito.it/en/education/master-s-degree-programmes/aerospace-engineering", "Politecnico di Torino Aerospace Engineering MSc", "official_program_page", ["program", "language", "admission", "curriculum"]), source("https://www.polito.it/en/education/master-s-degree-programmes/aerospace-engineering/programme-details", "Politecnico di Torino Aerospace Engineering programme details", "official_curriculum_page", ["curriculum"])],
        {"program_basic_info": "high", "language": "high", "admission": "medium", "curriculum": "high"},
    )
    write_payload(path, payload)

    # Padua — official 2025/26 PDF, therefore fee confidence is medium and the
    # card warns the student to check the next fee notice before applying.
    path = DATA / "italy.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    update(
        find_record(payload, "unipd_aerospace"),
        {"duration_years": 2, "ects": 120, "teaching_language": ["English"], "language_profile": {"teaching_language": ["English"], "english_level_required": "B2 CEFR or equivalent", "language_risk": "low"}, "eligibility_profile": {"required_previous_degree": ["Aerospace Engineering or related field with skills in mathematics, physics, industrial engineering, aerospace systems, aerodynamics and flight dynamics"]}, "cost_profile": {"tuition_eur_per_year_max": 2900, "tuition_eur_per_year_estimated": None, "cost_academic_year": "2025/26", "cost_notes": {"en": "Official brochure states annual fees up to €2,900 for 2025/26; confirm the new fee notice before applying.", "tr": "Resmi broşür 2025/26 için yıllık ücretin €2.900'a kadar olduğunu belirtir; başvuru öncesi yeni ücret duyurusunu doğrulayın."}}, "scholarship_profile": {"funding_notes": {"en": "International scholarships and fee waivers are advertised; eligibility is call-specific.", "tr": "Uluslararası burslar ve ücret muafiyetleri duyurulur; uygunluk çağrı bazındadır."}}, "curriculum_profile": {"tracks": ["Space", "Aeronautics"], "notable_courses": ["Advanced Aerodynamics", "Space Propulsion", "Astrodynamics", "Spacecraft Attitude Dynamics and Control", "Laboratory of Computational Fluid Dynamics", "Aerospace Structures Laboratory"]}, "category_profile": {"normalized_tags": ["space_systems", "orbital_mechanics", "spacecraft_gnc", "propulsion", "aerodynamics", "computational_fluid_dynamics", "aerospace_structures"]}},
        [source("https://web.unipd.it/international/wp-content/uploads/2025/01/Aerospace-Engineering_2526.pdf", "University of Padua Aerospace Engineering 2025/26 brochure", "official_program_page", ["program", "language", "admission", "curriculum"], "PDF is for academic year 2025/26; fee must be rechecked for the next cycle."), source("https://web.unipd.it/international/wp-content/uploads/2025/01/Aerospace-Engineering_2526.pdf", "University of Padua 2025/26 fees and funding brochure", "official_tuition_page", ["tuition"], "PDF is for academic year 2025/26; fee must be rechecked for the next cycle."), source("https://web.unipd.it/international/wp-content/uploads/2025/01/Aerospace-Engineering_2526.pdf", "University of Padua 2025/26 scholarships and fee-waivers brochure", "official_scholarship_page", ["scholarship"], "PDF is for academic year 2025/26; eligibility is call-specific."), source("https://academics.dii.unipd.it/aerospaceengineering/what-subjects-are-studied-and-how-msc/", "University of Padua Aerospace Engineering MSc curriculum", "official_curriculum_page", ["curriculum"])],
        {"program_basic_info": "high", "language": "high", "admission": "high", "tuition": "medium", "scholarship": "medium", "curriculum": "high"},
    )
    write_payload(path, payload)

    print("Applied checked European research updates to KTH, Stuttgart, ISAE-SUPAERO, Sapienza, Politecnico di Torino and Padua.")


if __name__ == "__main__":
    main()
