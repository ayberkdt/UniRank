"""Structure TU Delft Aerospace scholarship and GRE evidence without overstating access."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from unirank.core.integrity import audit_record


DATA_PATH = ROOT / "data_base" / "hollanda.json"
RECORD_ID = "netherlands_delft_msc_aerospace"
CHECKED = "2026-08-14"
PROGRAM_URL = "https://www.tudelft.nl/en/education/programmes/masters/ae/msc-aerospace-engineering/admission-and-application"
SCHOLARSHIP_URL = "https://www.tudelft.nl/en/education/study-programme-orientation/practical-matters/scholarships/justus-louise-van-effen-excellence-scholarships"
SECONDARY_URL = "https://www.mastersportal.com/scholarships/10291/justus-louise-van-effen-excellence-scholarships.html"


def bi(en: str, tr: str) -> dict[str, str]:
    return {"en": en, "tr": tr}


def main() -> None:
    payload = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    rows = payload["programs"]
    matches = [row for row in rows if row.get("id") == RECORD_ID]
    if len(matches) != 1:
        raise RuntimeError(f"Expected one {RECORD_ID!r} record; found {len(matches)}")
    row = matches[0]

    row["eligibility_profile"]["gre"] = {
        "policy": "required_for_international_bsc_applicants_to_aerospace_engineering_in_the_2026_27_cycle",
        "test_type": "GRE General Test",
        "minimum_scores": {
            "verbal_reasoning": 154,
            "quantitative_reasoning": 163,
            "analytical_writing": 4.0,
        },
        "recommended_scores": {},
        "validity_rule": "unknown",
        "waiver_rules": [],
        "cycle_status": "closed_past_cycle_recheck_next_intake",
        "source_ids": [PROGRAM_URL],
    }

    row["scholarship_profile"].update(
        {
            "regional_scholarship_available": True,
            "regional_scholarship_name": "Justus & Louise van Effen Excellence Scholarship",
            "non_eu_eligible": True,
            "scholarship_deadline": "2025-12-01T23:59:00+01:00",
            "scholarship_application_url": SCHOLARSHIP_URL,
            "funding_competitiveness": "extremely_high",
            "application_mode": "separate",
            "automatic_consideration": False,
            "separate_application_required": True,
            "opportunities": [
                {
                    "name": "Justus & Louise van Effen Excellence Scholarship",
                    "academic_year": "2026/2027",
                    "award_period": "2026-2028 MSc cohort",
                    "status": "closed_awards_made",
                    "number_of_awards": "two per TU Delft faculty",
                    "award": {
                        "type": "full_tuition_plus_living_expense_contribution",
                        "tuition_scope": "full annual MSc tuition at the statutory or institutional rate according to registered nationality",
                        "living_expense_amount": None,
                        "living_expense_amount_status": "not_published_in_accessible_current_official_evidence",
                    },
                    "international_applicants_eligible": True,
                    "turkey_nationality_eligible": True,
                    "programme_scope": "regular two-year TU Delft MSc; Joint Education Programmes excluded",
                    "academic_competitiveness_indicator": "approximately top 10% of graduates in the relevant previous programme; proof of ranking not required",
                    "application_mode": "scholarship_materials_submitted_with_complete_msc_application",
                    "separate_application_required": True,
                    "automatic_consideration": False,
                    "required_scholarship_materials": [
                        "Scholarship Application Form",
                        "two reference letters",
                        "English-language certificate with the MSc application for non-EU/EFTA applicants when required",
                    ],
                    "submission_warning": "Scholarship materials and the complete MSc application had to be submitted before the scholarship deadline; late reference letters were not accepted.",
                    "deadline": "2025-12-01T23:59:00+01:00",
                    "deadline_status": "closed_past_cycle_do_not_reuse_for_next_intake",
                    "official_source_url": SCHOLARSHIP_URL,
                    "secondary_cross_check_url": SECONDARY_URL,
                }
            ],
            "funding_notes": bi(
                "This was not automatic consideration. The applicant had to add a scholarship form and two references to the complete MSc application before 1 December 2025 at 23:59 CET. The page now says the 2026-2028 awards have been made; no future deadline is inferred.",
                "Bu burs otomatik deÄŸerlendirme deÄŸildi. AdayÄ±n 1 AralÄ±k 2025 saat 23.59 CET'ten Ã¶nce eksiksiz MSc baÅŸvurusuna burs formu ve iki referans eklemesi gerekiyordu. Sayfa artÄ±k 2026-2028 Ã¶dÃ¼llerinin verildiÄŸini belirtiyor; gelecek dÃ¶nem tarihi Ã§Ä±karÄ±lmÄ±yor.",
            ),
            "verification_notes": bi(
                "The current official URL was checked but returned 403 to both automated and interactive research access. Its indexed current text supports the award scope, international eligibility, two-per-faculty count and closed 2025 deadline; an accessible secondary listing corroborates the embedded scholarship form and two-reference workflow. Confidence is therefore medium, not high.",
                "GÃ¼ncel resmÃ® URL kontrol edildi ancak hem otomatik hem etkileÅŸimli araÅŸtÄ±rma eriÅŸimine 403 verdi. Dizine alÄ±nmÄ±ÅŸ gÃ¼ncel metin Ã¶dÃ¼l kapsamÄ±nÄ±, uluslararasÄ± uygunluÄŸu, fakÃ¼lte baÅŸÄ±na iki kontenjanÄ± ve kapanmÄ±ÅŸ 2025 tarihini; eriÅŸilebilir ikincil liste ise baÅŸvuruya eklenen burs formu ve iki referans sÃ¼recini destekliyor. Bu nedenle gÃ¼ven yÃ¼ksek deÄŸil, ortadÄ±r.",
            ),
        }
    )

    row["application_timeline_profile"].update(
        {
            "scholarship_deadline": "2025-12-01T23:59:00+01:00 (closed; 2026-2028 award cohort)",
            "scholarship_deadline_status": "closed_awards_made",
            "future_scholarship_deadline": None,
        }
    )

    profile = row["source_profile"]
    profile["last_verified"] = CHECKED
    profile["needs_verification"] = True
    profile["field_confidence"].update(
        {
            "scholarship": "medium",
            "living": "medium",
            "housing": "high",
        }
    )
    profile["verification_notes"] = bi(
        "Critical fields have current checked evidence except that the official scholarship page blocks research access. Keep scholarship confidence at medium and recheck the next intake directly before advice or application.",
        "Kritik alanlarda gÃ¼ncel kontrol edilmiÅŸ kanÄ±t vardÄ±r; ancak resmÃ® burs sayfasÄ± araÅŸtÄ±rma eriÅŸimini engeller. Burs gÃ¼venini orta tutun ve tavsiye ya da baÅŸvuru Ã¶ncesi sonraki alÄ±mÄ± doÄŸrudan yeniden kontrol edin.",
    )

    for item in profile["source_log"]:
        if item.get("url") == SCHOLARSHIP_URL:
            item.update(
                {
                    "access_status": "blocked",
                    "last_checked": CHECKED,
                    "confidence": "medium",
                    "relevant_fields": ["scholarship", "funding", "eligibility", "deadline"],
                    "notes": bi(
                        "The URL returned 403 to automated and interactive access. Indexed current text says the 2026-2028 awards have been made and supports international eligibility, two awards per faculty, full tuition plus a living contribution, and the past 1 December 2025 deadline.",
                        "URL otomatik ve etkileÅŸimli eriÅŸime 403 verdi. Dizine alÄ±nmÄ±ÅŸ gÃ¼ncel metin 2026-2028 Ã¶dÃ¼llerinin verildiÄŸini belirtir; uluslararasÄ± uygunluk, fakÃ¼lte baÅŸÄ±na iki Ã¶dÃ¼l, tam Ã¶ÄŸrenim artÄ± yaÅŸam katkÄ±sÄ± ve geÃ§miÅŸ 1 AralÄ±k 2025 tarihini destekler.",
                    ),
                }
            )
            break
    else:
        raise RuntimeError("Official scholarship source log entry is missing")

    if not any(item.get("url") == SECONDARY_URL for item in profile["source_log"]):
        profile["source_log"].append(
            {
                "url": SECONDARY_URL,
                "title": "Mastersportal: Justus & Louise van Effen Excellence Scholarships",
                "source_type": "reliable_secondary_scholarship_page",
                "access_status": "ok",
                "last_checked": CHECKED,
                "relevant_fields": ["scholarship", "application_process", "deadline"],
                "confidence": "medium",
                "notes": bi(
                    "Accessible secondary cross-check for the scholarship form, two-reference submission workflow, international scope, award coverage and 1 December 2025 deadline. It does not replace the blocked official source.",
                    "Burs formu, iki referanslÄ± teslim sÃ¼reci, uluslararasÄ± kapsam, Ã¶dÃ¼l iÃ§eriÄŸi ve 1 AralÄ±k 2025 tarihi iÃ§in eriÅŸilebilir ikincil Ã§apraz kontroldÃ¼r. Engellenen resmÃ® kaynaÄŸÄ±n yerini almaz.",
                ),
            }
        )

    quality = audit_record(row)
    quality["audited_at"] = CHECKED
    row["data_quality"] = quality
    row["quality_control"].update(
        {
            "qc_status": "needs_revision",
            "checked_at": CHECKED,
            "failed_canary_tests": ["official_scholarship_source_not_accessible"],
            "remaining_verification_tasks": [
                bi(
                    "Recheck the official scholarship page when it becomes accessible and replace the closed 2026-2028 cycle with the next published cycle; never roll the 1 December date forward by assumption.",
                    "ResmÃ® burs sayfasÄ± eriÅŸilebilir olduÄŸunda yeniden kontrol edin ve kapanmÄ±ÅŸ 2026-2028 dÃ¶nemini yayÄ±mlanan sonraki dÃ¶nemle deÄŸiÅŸtirin; 1 AralÄ±k tarihini varsayÄ±mla ileri taÅŸÄ±mayÄ±n.",
                )
            ],
            "qc_notes": bi(
                "The record now answers eligibility, amount scope, application mode, documents and deadline without falsely treating a blocked official page as accessible evidence.",
                "KayÄ±t artÄ±k uygunluk, kapsam, baÅŸvuru biÃ§imi, belgeler ve tarihi yanÄ±tlarken engellenen resmÃ® sayfayÄ± eriÅŸilebilir kanÄ±t gibi gÃ¶stermez.",
            ),
        }
    )

    DATA_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
