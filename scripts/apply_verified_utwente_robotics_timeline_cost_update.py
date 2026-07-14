"""Surface the official UT Robotics fees and dual-intake deadlines already sourced."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data_base" / "hollanda.json"
CHECKED = "2026-07-14"
FACTSHEET_URL = "https://www.utwente.nl/en/education/master/programmes/robotics/masters-structure/factsheet/"


def bi(en: str, tr: str) -> dict[str, str]:
    return {"en": en, "tr": tr}


def source() -> dict[str, Any]:
    return {
        "url": FACTSHEET_URL,
        "title": "University of Twente Robotics factsheet: 2026/27 and February 2027 intake dates",
        "source_type": "official_admission_page",
        "access_status": "ok",
        "last_checked": CHECKED,
        "relevant_fields": ["program", "admission", "non_eu", "deadline", "tuition"],
        "confidence": "high",
        "notes": bi(
            "Official factsheet lists 1 September 2026 and 1 February 2027 starts; EU/non-EU deadlines for both intakes; and the 2026/27 statutory, institutional and non-EU/EEA fee categories.",
            "Resmî bilgi sayfası 1 Eylül 2026 ve 1 Şubat 2027 başlangıçlarını; iki giriş için AB/AB-dışı son tarihlerini; ayrıca 2026/27 yasal, kurumsal ve AB/AEA-dışı ücret kategorilerini listeler.",
        ),
    }


def main() -> None:
    original = PATH.read_text(encoding="utf-8")
    document: Any = json.loads(original)
    rows = document if isinstance(document, list) else document.get("programs", document.get("universities", []))
    row = next(item for item in rows if item.get("id") == "netherlands_utwente_msc_robotics")

    row["cost_profile"].update({
        "academic_year": "2026/2027",
        "tuition_eur_per_year_min": 2694,
        "tuition_eur_per_year_max": 21700,
        "tuition_eur_per_year_estimated": 21700,
        "non_eu_flat_fee": 21700,
        "tuition_basis": "official_2026_27_full_time_non_eu_eea_or_institutional_fee; statutory_fee_only_for_eligible_students",
        "total_academic_cost_eur_per_year_estimated": 21700,
        "tuition_non_eu_full_program": {"amount": 43400, "currency": "EUR", "basis": "two_years_tuition_only", "academic_year": "2026/2027"},
        "source_notes": bi("The current Robotics factsheet lists EUR 21,700 for full-time non-EU/EEA and institutional tuition in 2026/27. EUR 2,694 is the statutory category, not a universal international price.", "Güncel Robotics bilgi sayfası 2026/27 tam zamanlı AB/AEA-dışı ve kurumsal ücret için 21.700 EUR listeler. 2.694 EUR yasal kategoridir; evrensel uluslararası ücret değildir."),
        "verification_notes": bi("The displayed EUR 43,400 is only the arithmetic of two published annual EUR 21,700 fees. It excludes living costs, the application fee and any future fee change.", "Gösterilen 43.400 EUR yalnızca yayımlanmış iki yıllık 21.700 EUR ücretin aritmetiğidir. Yaşam maliyetini, başvuru ücretini ve gelecekteki ücret değişimini içermez."),
    })
    row["application_timeline_profile"] = {
        "academic_year": "2026/2027 published cycles",
        "intake_terms": ["1 September 2026", "1 February 2027"],
        "application_rounds": [
            "September 2026 intake: non-EU 1 May 2026; EU 1 July 2026 (both dates passed when checked)",
            "February 2027 intake: non-EU 1 October 2026; EU 1 December 2026",
        ],
        "non_eu_deadline": "2026-10-01 (February 2027 intake; September 2026 deadline was 2026-05-01)",
        "eu_deadline": "2026-12-01 (February 2027 intake; September 2026 deadline was 2026-07-01)",
        "application_deadline": "2026-10-01 for non-EU / 2026-12-01 for EU for February 2027 intake",
        "scholarship_deadline": None,
        "pre_enrolment_required": False,
        "universitaly_required": False,
        "visa_sensitive_deadline": "2026-10-01 (non-EU February 2027 intake deadline)",
        "application_result_timing": None,
        "enrollment_deadline": None,
        "timeline_risk": "medium",
        "deadline_notes": bi("The factsheet contains two distinct intakes. It is misleading to display the July EU date without the matching September 2026 start, or to project those closed/published dates to a later cycle. The February 2027 dates were future dates when checked.", "Bilgi sayfası iki ayrı giriş içerir. Temmuz AB tarihini eşleşen Eylül 2026 başlangıcı olmadan göstermek veya bu kapanmış/yayımlanmış tarihleri sonraki döneme taşımak yanıltıcıdır. Şubat 2027 tarihleri kontrol edildiğinde gelecekteydi."),
    }

    profile = row.setdefault("source_profile", {})
    logs = [item for item in profile.get("source_log", []) if not (isinstance(item, dict) and item.get("url") == FACTSHEET_URL and item.get("source_type") == "official_admission_page")]
    logs.append(source())
    profile["source_log"] = logs
    profile["official_admission_page"] = FACTSHEET_URL
    profile["last_verified"] = CHECKED
    profile["needs_verification"] = False
    profile["verification_status"] = "verified"
    profile.setdefault("field_confidence", {}).update({
        "program_basic_info": "high", "language": "high", "admission": "high", "tuition": "high", "scholarship": "high", "curriculum": "high", "deadlines": "high", "living": "high", "housing": "high",
    })

    newline = "\r\n" if "\r\n" in original else "\n"
    PATH.write_text(json.dumps(document, ensure_ascii=False, indent=2).replace("\n", newline) + newline, encoding="utf-8")
    print("Updated University of Twente Robotics with official dual-intake timeline and fee figures.")


if __name__ == "__main__":
    main()
