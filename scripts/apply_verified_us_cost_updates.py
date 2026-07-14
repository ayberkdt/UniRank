"""Attach current official budget evidence to Stanford AA and Caltech Space."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data_base" / "amerika.json"
CHECKED = "2026-07-14"


def bi(en: str, tr: str) -> dict[str, str]:
    return {"en": en, "tr": tr}


def add_source(row: dict[str, Any], item: dict[str, Any]) -> None:
    profile = row.setdefault("source_profile", {})
    log = [entry for entry in profile.get("source_log", []) if isinstance(entry, dict)]
    log = [entry for entry in log if (entry.get("url"), entry.get("source_type")) != (item["url"], item["source_type"])]
    log.append(item)
    profile["source_log"] = log
    profile["last_verified"] = CHECKED


def source(url: str, title: str, notes_en: str, notes_tr: str) -> dict[str, Any]:
    return {
        "url": url,
        "title": title,
        "source_type": "official_cost_of_living_page",
        "access_status": "ok",
        "last_checked": CHECKED,
        "relevant_fields": ["housing", "living"],
        "confidence": "high",
        "notes": bi(notes_en, notes_tr),
    }


def main() -> None:
    original = PATH.read_text(encoding="utf-8")
    rows: list[dict[str, Any]] = json.loads(original)

    stanford = next(row for row in rows if row.get("id") == "stanford-aa")
    stanford["cost_profile"].update({
        "living_cost_usd_per_year": 49116,
        "living_cost_basis": bi(
            "Stanford's 2026/27 standard academic-year non-tuition budget for a typical single graduate living on campus with no dependents. It includes rent, food, personal expenses, transport, books, campus health and Cardinal Care.",
            "Stanford'ın kampüste yaşayan, bakmakla yükümlü olduğu kişi bulunmayan tipik tek lisansüstü öğrenci için 2026/27 akademik yılı öğrenim ücreti dışı standart bütçesi. Kira, yiyecek, kişisel harcamalar, ulaşım, kitaplar, kampüs sağlık hizmeti ve Cardinal Care içerir.",
        ),
    })
    stanford["living_profile"].update({
        "housing_budget_usd_per_year": 20055,
        "living_risk": "high",
        "housing_difficulty": None,
        "housing_notes": bi(
            "Stanford's 2026/27 academic-year on-campus rent allowance is USD 20,055 for a typical single graduate. The University says off-campus living expenses can be 10%–40% higher; this is a budget allowance, not a housing offer.",
            "Stanford'ın 2026/27 akademik yılı kampüs içi kira ödeneği tipik tek lisansüstü öğrenci için 20.055 USD'dir. Üniversite, kampüs dışı yaşam giderlerinin %10–%40 daha yüksek olabileceğini belirtir; bu bir bütçe ödeneğidir, konaklama teklifi değildir.",
        ),
    })
    add_source(stanford, source(
        "https://financialaid.stanford.edu/grad/budget/index.html",
        "Stanford Financial Aid: Graduate Student Budget 2026/27",
        "Current official academic-year budget lists USD 20,055 rent and USD 49,116 total non-tuition expenses for a typical single graduate living on campus.",
        "Güncel resmî akademik yıl bütçesi, kampüste yaşayan tipik tek lisansüstü öğrenci için 20.055 USD kira ve 49.116 USD toplam öğrenim ücreti dışı gider listeler.",
    ))
    stanford.setdefault("source_profile", {}).setdefault("field_confidence", {})["housing"] = "high"

    caltech = next(row for row in rows if row.get("id") == "caltech-galcit")
    caltech["living_profile"].update({
        "housing_difficulty": None,
        "housing_search_difficulty": None,
        "housing_notes": bi(
            "Caltech's official 2025/26 examples range from USD 10,920 for an on-campus four-bedroom per bed to USD 23,700 for a Caltech-owned two-bedroom lease unit, each including housing and utilities. Incoming graduate students are guaranteed housing only in their first year.",
            "Caltech'nin resmî 2025/26 örnekleri, konut ve faturalar dahil kampüs içi dört yatak odalı kişi başı 10.920 USD ile Caltech'e ait iki yatak odalı kiralık birim için 23.700 USD arasında değişir. Yeni lisansüstü öğrencilere yalnızca ilk yılları için konut garantisi verilir.",
        ),
    })
    add_source(caltech, source(
        "https://gradoffice.caltech.edu/financialsupport/budget",
        "Caltech Graduate Studies: Estimated Budget",
        "Official page supplies 2026/27 tuition/mandatory fees and labelled 2025/26 living and housing examples, including the first-year graduate-housing guarantee.",
        "Resmî sayfa 2026/27 öğrenim ücreti/zorunlu ücretlerini ve ilk yıl lisansüstü konut garantisi dahil, yılı belirtilmiş 2025/26 yaşam ve konut örneklerini sunar.",
    ))
    caltech.setdefault("source_profile", {}).setdefault("field_confidence", {})["housing"] = "high"

    match = re.search(r"^\s*\[\r?\n( +)\{", original)
    indent = len(match.group(1)) if match else 2
    newline = "\r\n" if "\r\n" in original else "\n"
    PATH.write_text(json.dumps(rows, ensure_ascii=False, indent=indent).replace("\n", newline) + newline, encoding="utf-8")
    print("Updated Stanford and Caltech official budget evidence.")


if __name__ == "__main__":
    main()
