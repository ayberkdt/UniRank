"""Add current TUM Aerospace funding and Munich living-cost evidence."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data_base" / "almanya.json"
CHECKED = "2026-07-14"


def bi(en: str, tr: str) -> dict[str, str]:
    return {"en": en, "tr": tr}


def item(url: str, title: str, kind: str, fields: list[str], en: str, tr: str, confidence: str = "high") -> dict[str, Any]:
    return {"url": url, "title": title, "source_type": kind, "access_status": "ok", "last_checked": CHECKED, "relevant_fields": fields, "confidence": confidence, "notes": bi(en, tr)}


def add(row: dict[str, Any], entry: dict[str, Any]) -> None:
    profile = row.setdefault("source_profile", {})
    log = [source for source in profile.get("source_log", []) if isinstance(source, dict)]
    log = [source for source in log if (source.get("url"), source.get("source_type")) != (entry["url"], entry["source_type"])]
    log.append(entry)
    profile["source_log"] = log
    profile["last_verified"] = CHECKED


def main() -> None:
    original = PATH.read_text(encoding="utf-8")
    rows: list[dict[str, Any]] = json.loads(original)
    row = next(record for record in rows if record.get("id") == "germany-tum-msc-aerospace")

    row["scholarship_profile"].update({
        "regional_scholarship_available": True,
        "regional_scholarship_name": "TUM tuition-fee waiver scholarship",
        "non_eu_eligible": True,
        "merit_scholarships": [bi(
            "TUM tuition-fee waiver scholarship for high-achieving Master's applicants: normally waives the non-EU tuition fee for two semesters; places are limited and an official ranking certificate is required.",
            "Başarılı yüksek lisans adayları için TUM öğrenim ücreti muafiyet bursu: normalde iki dönem AB dışı öğrenim ücretini kaldırır; kontenjan sınırlıdır ve resmî başarı sıralaması belgesi gerekir.",
        )],
        "funding_notes": bi(
            "For a winter intake, the current waiver-scholarship window is 1 January–31 May; it is not automatic. Separately, TUM's international-student scholarship is one-time EUR 500–1,800 per semester and normally starts from the second Master's semester (first only for a TUM bachelor's graduate). Neither award provides a living-cost guarantee.",
            "Kış başlangıcı için güncel muafiyet bursu penceresi 1 Ocak–31 Mayıs'tır; otomatik değildir. Ayrı olarak TUM uluslararası öğrenci bursu dönem başına tek seferlik 500–1.800 EUR'dur ve normalde yüksek lisansın ikinci döneminden itibaren başlar (yalnızca TUM lisans mezunu için ilk dönem). Hiçbir ödül yaşam gideri garantisi sağlamaz.",
        ),
        "scholarship_deadline": "2026-05-31 (winter 2026/27 tuition-fee waiver; verify the next cycle)",
        "scholarship_application_url": "https://www.tum.de/en/studies/fees/tuition/scholarships-and-waivers",
    })
    row["living_profile"].update({
        "average_room_rent_eur": 400.60,
        "monthly_living_cost_eur_min": 1200,
        "monthly_living_cost_eur_max": None,
        "housing_difficulty": "high",
        "living_risk": "high",
        "monthly_living_cost_basis": bi(
            "TUM's Munich guidance says at least EUR 1,200 per month is needed, including rent but excluding leisure activities. It is a planning minimum, not a personal guarantee.",
            "TUM'un Münih rehberi, kira dahil ancak boş zaman aktiviteleri hariç ayda en az 1.200 EUR gerektiğini belirtir. Bu bir planlama asgarisidir, kişisel garanti değildir.",
        ),
        "housing_notes": bi(
            "Studierendenwerk München publishes an average single-place rent of about EUR 400.60 and warns that affordable housing is scarce, with waits of one to seven semesters depending on residence. This is an average for its own rooms/apartments, not an availability promise.",
            "Studierendenwerk München tek kişilik yer için yaklaşık 400,60 EUR ortalama kira yayımlar ve uygun fiyatlı konutun kıt olduğunu, yurda göre bir ila yedi dönem bekleme süresi bulunduğunu uyarır. Bu, kendi oda/apartmanları için ortalamadır; yer garantisi değildir.",
        ),
    })

    waiver = "https://www.tum.de/en/studies/fees/tuition/scholarships-and-waivers"
    add(row, item(waiver, "TUM: Scholarships and Waivers for International Students", "official_scholarship_page", ["scholarship", "funding"], "Current page defines limited tuition-fee waivers for high-achieving or financially needy non-EU Master's students and its application windows.", "Güncel sayfa, başarılı veya maddi ihtiyacı bulunan AB dışı yüksek lisans öğrencileri için sınırlı öğrenim ücreti muafiyetlerini ve başvuru tarihlerini tanımlar."))
    add(row, item("https://www.tum.de/en/studies/fees-and-financial-aid/scholarships/tum-scholarships/scholarship-for-international-students-of-tum", "TUM Scholarship for International Students", "official_scholarship_page", ["scholarship", "funding"], "Current page publishes a one-time EUR 500–1,800 per-semester aid range, eligibility after enrolment and the 2026/27 winter application window.", "Güncel sayfa, dönem başına tek seferlik 500–1.800 EUR yardım aralığını, kayıttan sonraki uygunluğu ve 2026/27 kışı başvuru dönemini yayımlar."))
    add(row, item("https://www.international.tum.de/en/global/exchangestudents/general-information-for-international-students/preparing-your-stay/", "TUM: Preparing for Your Stay", "official_cost_of_living_page", ["housing", "living"], "Current TUM Munich guidance advises at least EUR 1,200 monthly living costs including rent and excluding leisure activities.", "Güncel TUM Münih rehberi, kira dahil ve boş zaman aktiviteleri hariç aylık en az 1.200 EUR yaşam maliyeti önerir."))
    add(row, item("https://www.studierendenwerk-muenchen-oberbayern.de/en/accommodation/", "Studierendenwerk München: Student Accommodation", "official_housing_page", ["housing"], "Current student-services page gives an approximately EUR 400.60 average single-place rent and one- to seven-semester waits due to demand.", "Güncel öğrenci hizmetleri sayfası yaklaşık 400,60 EUR ortalama tek kişilik kira ve talep nedeniyle bir ila yedi dönem bekleme süresi verir."))
    row.setdefault("source_profile", {}).setdefault("field_confidence", {}).update({"scholarship": "high", "housing": "high"})

    match = re.search(r"^\s*\[\r?\n( +)\{", original)
    indent = len(match.group(1)) if match else 2
    newline = "\r\n" if "\r\n" in original else "\n"
    PATH.write_text(json.dumps(rows, ensure_ascii=False, indent=indent).replace("\n", newline) + newline, encoding="utf-8")
    print("Updated TUM Aerospace funding and Munich housing evidence.")


if __name__ == "__main__":
    main()
