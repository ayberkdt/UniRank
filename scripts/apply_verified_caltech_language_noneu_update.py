"""Verify Caltech Space Engineering MS language and international eligibility."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data_base" / "amerika.json"
RECORD_ID = "caltech-galcit"
CHECKED_AT = "2026-08-14"
DEPARTMENT_URL = "https://aerospace.caltech.edu/academics/admissions"
FAQ_URL = "https://gradoffice.caltech.edu/admissions/faq-applicants"


def main() -> None:
    records = json.loads(DB_PATH.read_text(encoding="utf-8"))
    record = next(item for item in records if item.get("id") == RECORD_ID)

    eligibility = record["eligibility_profile"]
    eligibility["eligible_for_non_eu"] = True
    eligibility["gre"] = {
        "policy": "optional",
        "test_type": "GRE General Test",
        "minimum_scores": {},
        "recommended_scores": {},
        "validity_rule": "not_published",
        "waiver_rules": [],
        "source_ids": [DEPARTMENT_URL],
        "notes": {
            "en": "The current Aerospace admissions page says GRE submission is optional; it publishes no minimum or recommended score.",
            "tr": "Güncel Aerospace kabul sayfası GRE gönderiminin isteğe bağlı olduğunu belirtir; asgari veya önerilen puan yayımlamaz.",
        },
    }
    eligibility["verification_notes"] = {
        "en": "International applicants may apply to the terminal Space Engineering MS. Caltech's central applicant FAQ explicitly discusses international applicants and identifies Space Engineering as one of the few options accepting direct terminal-MS applications. Eligibility does not guarantee admission, funding, visa issuance or work authorisation.",
        "tr": "Uluslararası adaylar terminal Space Engineering MS programına başvurabilir. Caltech'in merkezî aday SSS sayfası uluslararası adayları açıkça ele alır ve Space Engineering'i doğrudan terminal MS başvurusu kabul eden az sayıdaki seçenekten biri olarak tanımlar. Uygunluk; kabul, finansman, vize veya çalışma izni garantisi değildir.",
    }

    record["teaching_language"] = ["English"]
    record["language_profile"].update(
        {
            "teaching_language": ["English"],
            "teaching_languages": ["English"],
            "english_required": True,
            "english_level_required": "TOEFL required by the programme page for applicants whose first or native language is not English; no minimum score published",
            "accepted_english_evidence": ["TOEFL on the Aerospace programme page", "TOEFL", "PTE", "IELTS", "Duolingo or another certified examination on the central FAQ"],
            "minimum_scores": {},
            "english_waiver_rules_from_central_faq": [
                "studied_in_the_united_states_for_two_or_more_years",
                "degree_from_a_college_or_university_whose_primary_instruction_is_english",
            ],
            "ets_institution_code": "4034",
            "post_admission_evaluation": "International admits without an English-primary university degree are evaluated before the academic year and may be assigned ESL coursework",
            "policy_conflict": {
                "en": "The Aerospace page is stricter and says non-native-English applicants must submit TOEFL. The central 2026 FAQ says an English test is not required for admission but is important, and publishes broader exemptions. Treat the programme-specific TOEFL rule as controlling and ask the department whether a central exemption applies before relying on it.",
                "tr": "Aerospace sayfası daha katıdır ve ana dili İngilizce olmayan adayların TOEFL göndermesini ister. Merkezî 2026 SSS sayfası İngilizce sınavını kabul için zorunlu saymaz, önemli bulur ve daha geniş muafiyetler yayımlar. Programa özgü TOEFL kuralını esas alın; merkezî muafiyete güvenmeden önce bölüme uygulanıp uygulanmadığını sorun.",
            },
            "language_risk": "high",
            "verification_notes": {
                "en": "Caltech requires applicants to read, write and speak English and comprehend spoken English, while the Aerospace page imposes a TOEFL rule for non-native speakers. This establishes English as the programme's operational teaching language, but no separate instruction-language label was found; confidence is medium.",
                "tr": "Caltech adayların İngilizce okumasını, yazmasını, konuşmasını ve sözlü İngilizceyi anlamasını ister; Aerospace sayfası da ana dili İngilizce olmayanlara TOEFL kuralı uygular. Bu, İngilizceyi programın operasyonel eğitim dili olarak kanıtlar; ancak ayrı bir eğitim dili etiketi bulunmadığından güven orta düzeydedir.",
            },
        }
    )

    source_log = record["source_profile"]["source_log"]
    department_source = next(item for item in source_log if item.get("url") == DEPARTMENT_URL and item.get("source_type") == "official_admission_page")
    department_source["relevant_fields"] = list(
        dict.fromkeys(
            department_source.get("relevant_fields", [])
            + ["language", "teaching_language", "gre", "english_test"]
        )
    )
    department_source["notes"] = {
        "en": "Current programme page gives the 15 December deadline, optional GRE policy, TOEFL rule for non-native-English applicants, Space Engineering specialization, and automatic fellowship consideration via the application aid checkbox.",
        "tr": "Güncel program sayfası 15 Aralık son tarihini, isteğe bağlı GRE politikasını, ana dili İngilizce olmayanlara TOEFL kuralını, Space Engineering uzmanlığını ve başvurudaki mali yardım kutusuyla otomatik fellowship değerlendirmesini verir.",
    }

    faq_source = {
        "url": FAQ_URL,
        "title": "Caltech Graduate Studies: Frequently Asked Questions for Applicants",
        "source_type": "official_admission_page",
        "access_status": "ok",
        "last_checked": CHECKED_AT,
        "relevant_fields": ["admission", "non_eu_eligibility", "language", "english_test", "international_applicants"],
        "confidence": "high",
        "notes": {
            "en": "Current central FAQ covers international applicant GPA and English procedures, confirms direct terminal-MS applications in Space Engineering, publishes English-test exemptions and states that no central minimum score applies.",
            "tr": "Güncel merkezî SSS uluslararası adayların not ve İngilizce süreçlerini kapsar, Space Engineering'e doğrudan terminal MS başvurusunu doğrular, İngilizce sınav muafiyetlerini yayımlar ve merkezî asgari puan olmadığını belirtir.",
        },
    }
    if not any(item.get("url") == FAQ_URL for item in source_log):
        source_log.append(faq_source)

    source_profile = record["source_profile"]
    source_profile["last_verified"] = CHECKED_AT
    source_profile["needs_verification"] = True
    source_profile["field_confidence"]["admission"] = "high"
    source_profile["field_confidence"]["non_eu_eligibility"] = "high"
    source_profile["field_confidence"]["language"] = "medium"
    source_profile["verification_notes"] = {
        "en": "All critical decision fields have checked official evidence. The record remains partial because the instruction language is operationally established rather than explicitly labelled, and the programme-specific TOEFL rule conflicts with the broader central FAQ.",
        "tr": "Tüm kritik karar alanlarında kontrol edilmiş resmî kanıt vardır. Eğitim dili açıkça etiketlenmek yerine operasyonel olarak kanıtlandığı ve programa özgü TOEFL kuralı daha geniş merkezî SSS ile çeliştiği için kayıt kısmi kalır.",
    }

    quality = record["data_quality"]
    quality.update(
        {
            "status": "partial",
            "checked_official_source_count": len(source_log),
            "verified_fields": list(dict.fromkeys(quality["verified_fields"] + ["language", "non_eu_eligibility"])),
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
                    "en": "Ask Aerospace whether the central English-test exemptions override the programme page's non-native-speaker TOEFL rule, and replace the operational language inference if an explicit instruction-language statement is published.",
                    "tr": "Merkezî İngilizce sınav muafiyetlerinin program sayfasındaki ana dili İngilizce olmayanlara TOEFL kuralını geçersiz kılıp kılmadığını Aerospace bölümüne sorun; açık bir eğitim dili beyanı yayımlanırsa operasyonel dil çıkarımını bununla değiştirin.",
                }
            ],
        }
    )

    hard_flags = record.get("scoring_inputs", {}).get("hard_filter_flags")
    if isinstance(hard_flags, dict):
        hard_flags["english_only_compatible"] = True
        hard_flags["non_eu_eligible"] = True
        hard_flags["needs_verification"] = True

    DB_PATH.write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Verified Caltech Space Engineering language and non-EU route with {len(source_log)} official sources.")


if __name__ == "__main__":
    main()
