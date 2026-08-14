"""Verify Stanford AA MS English and GRE policies from current official pages."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data_base" / "amerika.json"
RECORD_ID = "stanford-aa"
CHECKED_AT = "2026-08-14"
MS_ADMISSION_URL = "https://aa.stanford.edu/academics-admissions/graduate-admissions/masters-admissions"
FAQ_URL = "https://aa.stanford.edu/academics-admissions/graduate-admissions/admissions-frequently-asked-questions"
TEST_URL = "https://gradadmissions.stanford.edu/apply/test-scores"


def main() -> None:
    records = json.loads(DB_PATH.read_text(encoding="utf-8"))
    record = next(item for item in records if item.get("id") == RECORD_ID)

    record["teaching_language"] = ["English"]
    record["language_profile"].update(
        {
            "teaching_language": ["English"],
            "teaching_languages": ["English"],
            "english_required": True,
            "english_level_required": "TOEFL/IELTS minimum unless an official exemption criterion is met",
            "accepted_english_evidence": ["TOEFL iBT", "IELTS Academic"],
            "minimum_scores": {
                "toefl_before_2026_01_21": 90,
                "toefl_on_or_after_2026_01_21": 4.5,
                "ielts_academic": 7,
            },
            "placement_test_exemption_scores": {
                "toefl_before_2026_01_21": 109,
                "toefl_on_or_after_2026_01_21": 5.5,
                "ielts_academic": 8,
            },
            "english_waiver_rules": [
                "us_citizen_or_permanent_resident",
                "first_language_is_english",
                "us_degree_or_international_equivalent_from_a_university_where_all_instruction_was_in_english",
                "two_or_more_consecutive_years_of_professional_or_educational_experience_in_english_within_the_past_ten_years",
            ],
            "test_score_validity": "two_years",
            "ets_institution_code": "4704",
            "language_risk": "medium",
            "verification_notes": {
                "en": "Stanford AA requires adequate spoken and written English for lectures and group discussions and requires TOEFL iBT or IELTS Academic unless an exemption criterion is met. This establishes English as the programme's operational teaching language, although the programme page does not publish a separate 'language of instruction' label; confidence is therefore medium rather than high.",
                "tr": "Stanford AA, dersler ve grup tartışmaları için yeterli sözlü ve yazılı İngilizce ister ve muafiyet ölçütü karşılanmıyorsa TOEFL iBT veya IELTS Academic talep eder. Bu, İngilizceyi programın operasyonel eğitim dili olarak kanıtlar; ancak program sayfası ayrıca 'eğitim dili' etiketi yayımlamadığından güven yüksek değil orta düzeydedir.",
            },
        }
    )

    record["eligibility_profile"]["gre"] = {
        "policy": "not_required_and_not_considered",
        "test_type": "GRE General Test",
        "minimum_scores": {},
        "recommended_scores": {},
        "validity_rule": "not_applicable",
        "waiver_rules": [],
        "source_ids": [FAQ_URL],
        "notes": {
            "en": "The current Stanford AA admissions FAQ says GRE scores are no longer required and will not be considered.",
            "tr": "Güncel Stanford AA kabul SSS sayfası GRE puanlarının artık istenmediğini ve değerlendirmeye alınmayacağını belirtir.",
        },
    }

    source_log = record["source_profile"]["source_log"]
    ms_source = next(item for item in source_log if item.get("url") == MS_ADMISSION_URL)
    ms_source["relevant_fields"] = list(
        dict.fromkeys(ms_source.get("relevant_fields", []) + ["language", "english_test", "waiver_rules"])
    )
    ms_source["notes"] = {
        "en": "Current department page requires adequate English for lectures and discussions, gives the 2026-onward exemption criteria, accepts TOEFL iBT/IELTS Academic, and applies a two-year score-validity rule.",
        "tr": "Güncel bölüm sayfası dersler ve tartışmalar için yeterli İngilizce ister, 2026'dan itibaren muafiyet ölçütlerini verir, TOEFL iBT/IELTS Academic kabul eder ve iki yıllık puan geçerliliği uygular.",
    }

    new_sources = [
        {
            "url": TEST_URL,
            "title": "Stanford Graduate Admissions: Test Scores",
            "source_type": "official_admission_page",
            "access_status": "ok",
            "last_checked": CHECKED_AT,
            "relevant_fields": ["language", "english_test", "minimum_scores", "placement_test"],
            "confidence": "high",
            "notes": {
                "en": "Current central table publishes TOEFL minimums before and after the 21 January 2026 score-scale change, IELTS 7, and the higher English Placement Test exemption thresholds.",
                "tr": "Güncel merkezî tablo 21 Ocak 2026 TOEFL puan ölçeği değişiminden önceki ve sonraki asgari puanları, IELTS 7'yi ve daha yüksek English Placement Test muafiyet eşiklerini yayımlar.",
            },
        },
        {
            "url": FAQ_URL,
            "title": "Stanford AA Graduate Admissions Frequently Asked Questions",
            "source_type": "official_admission_page",
            "access_status": "ok",
            "last_checked": CHECKED_AT,
            "relevant_fields": ["admission", "language", "english_test", "gre"],
            "confidence": "high",
            "notes": {
                "en": "Current department FAQ confirms MS English-test minimums and states that GRE scores are neither required nor considered.",
                "tr": "Güncel bölüm SSS sayfası MS İngilizce sınavı asgari puanlarını doğrular ve GRE puanlarının ne istendiğini ne de değerlendirildiğini belirtir.",
            },
        },
    ]
    existing_urls = {item.get("url") for item in source_log}
    source_log.extend(item for item in new_sources if item["url"] not in existing_urls)

    source_profile = record["source_profile"]
    source_profile["last_verified"] = CHECKED_AT
    source_profile["needs_verification"] = True
    source_profile["field_confidence"]["language"] = "medium"
    source_profile["verification_notes"] = {
        "en": "All critical decision fields now have checked official evidence. English is operationally established through the department's lecture/discussion proficiency rule, but the absence of a separate instruction-language label keeps language confidence at medium.",
        "tr": "Tüm kritik karar alanları artık kontrol edilmiş resmî kanıta sahiptir. İngilizce, bölümün ders/tartışma yeterlik kuralıyla operasyonel olarak kanıtlanmıştır; ancak ayrı bir eğitim dili etiketi bulunmadığından dil güveni orta düzeyde kalır.",
    }

    quality = record["data_quality"]
    quality.update(
        {
            "status": "partial",
            "checked_official_source_count": len(source_log),
            "verified_fields": list(dict.fromkeys(quality["verified_fields"] + ["language"])),
            "unverified_critical_fields": [],
            "has_checked_source_log": True,
            "audited_at": CHECKED_AT,
        }
    )
    record["quality_control"].update(
        {
            "checked_at": CHECKED_AT,
            "qc_status": "needs_revision",
            "failed_canary_tests": ["critical_field_confidence_below_high"],
            "remaining_verification_tasks": [
                {
                    "en": "Replace the operational English-language inference with an explicit programme instruction-language statement if Stanford publishes one.",
                    "tr": "Stanford açık bir program eğitim dili beyanı yayımlarsa operasyonel İngilizce çıkarımını bu beyanla değiştirin.",
                }
            ],
        }
    )

    hard_flags = record.get("scoring_inputs", {}).get("hard_filter_flags")
    if isinstance(hard_flags, dict):
        hard_flags["english_only_compatible"] = True
        hard_flags["needs_verification"] = True

    DB_PATH.write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Verified Stanford AA English and GRE policies with {len(source_log)} checked official sources.")


if __name__ == "__main__":
    main()
