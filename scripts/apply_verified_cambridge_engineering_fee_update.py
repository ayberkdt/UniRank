"""Apply the verified 2026/27 Cambridge MPhil Engineering fee update."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from unirank.core.integrity import audit_record


DATA_PATH = ROOT / "data_base" / "ingiltere.json"
RECORD_ID = "university-of-cambridge"
FINANCE_URL = (
    "https://www.postgraduate.study.cam.ac.uk/courses/directory/"
    "egegmpmeg/finance"
)
WIDGET_URL = (
    "https://2026.gaobase.admin.cam.ac.uk/api/courses/"
    "EGEGMPMEG/financial_tracker.html?fee_status=O"
)


def bi(en: str, tr: str) -> dict[str, str]:
    return {"en": en, "tr": tr}


def main() -> None:
    rows = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    matches = [row for row in rows if row.get("id") == RECORD_ID]
    if len(matches) != 1:
        raise RuntimeError(f"Expected one {RECORD_ID!r} record; found {len(matches)}")

    row = matches[0]
    cost = row.setdefault("cost_profile", {})
    cost.update(
        {
            "academic_year": "2026/2027",
            "tuition_gbp_per_year": 41304,
            "tuition_gbp_per_year_min": 41304,
            "tuition_gbp_per_year_max": 41304,
            "tuition_basis": (
                "official_2026_27_overseas_full_time_university_composition_fee"
            ),
            "living_cost_gbp_per_year": 19860,
            "total_academic_and_living_cost_gbp_per_year": 61164,
            "verification_notes": bi(
                "Cambridge's official 2026/27 course finance widget lists a GBP "
                "41,304 University Composition Fee for an overseas, full-time MPhil "
                "in Engineering student and GBP 19,860 maintenance, for a GBP 61,164 "
                "estimated annual commitment. The widget does not display a separate "
                "College fee; this record therefore does not infer either that an "
                "additional College fee is due or that it is waived.",
                "Cambridge'in resmî 2026/27 ders finans hesaplayıcısı, yurtdışı ücret "
                "statüsündeki tam zamanlı MPhil in Engineering öğrencisi için 41.304 "
                "GBP University Composition Fee ve 19.860 GBP geçim gideri; toplamda "
                "61.164 GBP tahmini yıllık finansal taahhüt gösterir. Hesaplayıcı ayrı "
                "bir College fee kalemi göstermediğinden bu kayıt, ek College fee "
                "ödeneceğini veya muaf tutulduğunu varsaymaz.",
            ),
            "source_notes": bi(
                "The published overseas amount is for the 12-month full-time route. "
                "No currency conversion or multiplication beyond the official widget "
                "is used.",
                "Yayımlanan yurtdışı tutarı 12 aylık tam zamanlı yol içindir. Resmî "
                "hesaplayıcının ötesinde kur dönüşümü veya çarpım kullanılmamıştır.",
            ),
        }
    )

    source_profile = row.setdefault("source_profile", {})
    source_profile["official_tuition_page"] = FINANCE_URL
    source_profile["last_verified"] = "2026-08-14"
    source_profile.setdefault("field_confidence", {})["tuition"] = "high"

    source_log = source_profile.setdefault("source_log", [])
    old_tuition_entries = [
        source
        for source in source_log
        if source.get("url") == FINANCE_URL
    ]
    if len(old_tuition_entries) != 1:
        raise RuntimeError(
            "Expected exactly one existing official_tuition_page source for Cambridge; "
            f"found {len(old_tuition_entries)}"
        )
    old_tuition_entries[0].update(
        {
            "url": FINANCE_URL,
            "title": "MPhil in Engineering — Finance",
            "access_status": "requires_js",
            "last_checked": "2026-08-14",
            "relevant_fields": ["tuition", "living"],
            "confidence": "high",
            "notes": bi(
                "Official course-finance page embeds the 2026/27 fee-status widget. "
                "The overseas selection returns UCF GBP 41,304, maintenance GBP "
                "19,860, and total annual commitment GBP 61,164.",
                "Resmî ders finans sayfası 2026/27 ücret statüsü hesaplayıcısını gömer. "
                "Yurtdışı seçeneği 41.304 GBP UCF, 19.860 GBP geçim gideri ve 61.164 "
                "GBP toplam yıllık taahhüt verir.",
            ),
        }
    )

    widget_entries = [source for source in source_log if source.get("url") == WIDGET_URL]
    widget_source = {
        "url": WIDGET_URL,
        "title": "Cambridge 2026/27 course financial tracker — Overseas",
        "source_type": "official_tuition_page",
        "access_status": "ok",
        "last_checked": "2026-08-14",
        "relevant_fields": ["tuition", "living"],
        "confidence": "high",
        "notes": bi(
            "Official Cambridge admissions-system response for course EGEGMPMEG with "
            "overseas fee status. It supplies the exact values rendered by the Finance "
            "tab.",
            "EGEGMPMEG dersi ve yurtdışı ücret statüsü için Cambridge'in resmî kabul "
            "sistemi yanıtıdır. Finans sekmesinde gösterilen kesin değerleri sağlar.",
        ),
    }
    if widget_entries:
        if len(widget_entries) != 1:
            raise RuntimeError(f"Duplicate Cambridge finance widget sources: {len(widget_entries)}")
        widget_entries[0].update(widget_source)
    else:
        source_log.append(widget_source)

    data_quality = audit_record(row)
    data_quality["audited_at"] = "2026-08-14"
    row["data_quality"] = data_quality

    qc = row.setdefault("quality_control", {})
    remaining = qc.setdefault("remaining_verification_tasks", [])
    qc["remaining_verification_tasks"] = [
        task
        for task in remaining
        if "tuition" not in str(task).lower() and "fee" not in str(task).lower()
    ]
    qc["checked_at"] = "2026-08-14"

    DATA_PATH.write_text(
        json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
