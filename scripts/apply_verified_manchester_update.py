"""Add checked 2026/27 cost and funding context to Manchester Aerospace MSc."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data_base" / "ingiltere.json"
CHECKED = "2026-07-14"


def bi(en: str, tr: str) -> dict[str, str]:
    return {"en": en, "tr": tr}


def source() -> dict[str, Any]:
    return {
        "url": "https://www.manchester.ac.uk/study/postgraduate-research/funding/living-costs/",
        "title": "University of Manchester: Cost of Living 2026/27",
        "source_type": "official_cost_of_living_page",
        "access_status": "ok",
        "last_checked": CHECKED,
        "relevant_fields": ["housing", "living"],
        "confidence": "high",
        "notes": bi(
            "The University publishes a 2026/27 guide for taught master's and postgraduate research students, including accommodation options and a total 52-week planning budget.",
            "Üniversite, konaklama seçenekleri ve 52 haftalık toplam planlama bütçesi dahil olmak üzere, okutulan yüksek lisans ve lisansüstü araştırma öğrencileri için 2026/27 rehberi yayımlar.",
        ),
    }


def main() -> None:
    original = PATH.read_text(encoding="utf-8")
    rows: list[dict[str, Any]] = json.loads(original)
    row = next(item for item in rows if item.get("id") == "university-of-manchester")

    row["cost_profile"].update({
        "living_cost_gbp_per_year": 18188,
        "living_cost_basis": bi(
            "University of Manchester 2026/27 guide: 52-week total planning budget for a full-time postgraduate, including GBP 10,000 private accommodation with utilities.",
            "Manchester Üniversitesi 2026/27 rehberi: faturalar dahil 10.000 GBP özel konaklama içeren, tam zamanlı lisansüstü öğrenci için 52 haftalık toplam planlama bütçesi.",
        ),
    })
    row["living_profile"].update({
        "monthly_housing_rent_gbp_per_month_min": 487,
        "monthly_housing_rent_gbp_per_month_max": 1060,
        "monthly_living_cost_gbp_per_month_min": 1510,
        "monthly_living_cost_gbp_per_month_max": 1510,
        "living_cost_risk": "medium",
        "housing_difficulty": None,
        "monthly_living_cost_basis": bi(
            "The University estimates GBP 1,510 per month over 52 weeks for a full-time postgraduate; it is a guide, not a personal spend guarantee.",
            "Üniversite, tam zamanlı lisansüstü öğrenci için 52 haftaya yayılmış aylık 1.510 GBP tahmin eder; bu bir rehberdir, kişisel harcama garantisi değildir.",
        ),
        "housing_notes": bi(
            "For 2026/27, the University's self-catered halls guide is GBP 487–1,060 per month, with some master's studios up to GBP 1,255. University-hall figures normally include utilities, contents insurance and internet; contract lengths vary.",
            "2026/27 için Üniversitenin kendi yemek hazırlamalı yurt rehberi aylık 487–1.060 GBP'dir; bazı yüksek lisans stüdyoları 1.255 GBP'ye kadar çıkar. Üniversite yurdu tutarları normalde faturaları, eşya sigortasını ve interneti içerir; sözleşme süreleri değişir.",
        ),
    })
    row["scholarship_profile"].update({
        "funding_notes": bi(
            "The 2026 Aerospace MSc page says Manchester offers postgraduate taught scholarships and awards to outstanding UK and international students and points applicants to its international master's scholarship range. Awards, eligibility and deadlines remain scheme-specific; none is guaranteed by the course offer.",
            "2026 Aerospace MSc sayfası, Manchester'ın başarılı Birleşik Krallık ve uluslararası öğrenciler için lisansüstü burslar ve ödüller sunduğunu, adayları uluslararası yüksek lisans burslarına yönlendirdiğini belirtir. Ödül, uygunluk ve son tarih her burs programına özeldir; ders teklifi bunları garanti etmez.",
        ),
        "regional_scholarship_available": None,
        "non_eu_eligible": None,
    })

    profile = row.setdefault("source_profile", {})
    log = [item for item in profile.get("source_log", []) if isinstance(item, dict)]
    living = source()
    log = [item for item in log if (item.get("url"), item.get("source_type")) != (living["url"], living["source_type"])]
    log.append(living)
    profile["source_log"] = log
    profile.setdefault("field_confidence", {}).update({"housing": "high", "scholarship": "medium"})
    profile["last_verified"] = CHECKED

    match = re.search(r"^\s*\[\r?\n( +)\{", original)
    indent = len(match.group(1)) if match else 2
    newline = "\r\n" if "\r\n" in original else "\n"
    PATH.write_text(json.dumps(rows, ensure_ascii=False, indent=indent).replace("\n", newline) + newline, encoding="utf-8")
    print("Updated University of Manchester cost, housing and funding context.")


if __name__ == "__main__":
    main()
