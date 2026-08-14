"""Close TU Hamburg Aeronautics' non-EU eligibility evidence gap."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data_base" / "almanya.json"
RECORD_ID = "de_tuhh_aeronautics_msc"
CHECKED_AT = "2026-08-14"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def save(path: Path, payload) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    records = load(DB_PATH)
    record = next(item for item in records if item.get("id") == RECORD_ID)

    eligibility = record["eligibility_profile"]
    eligibility.update(
        {
            "eligible_for_non_eu": True,
            "required_previous_degree": {
                "en": "A qualifying Bachelor of Science or equivalent degree in mechanical engineering or a related subject; TU Hamburg separately assesses foreign-degree equivalence and subject fit.",
                "tr": "Makine mühendisliği veya ilişkili bir alanda uygun Bachelor of Science ya da eşdeğer derece; TU Hamburg yabancı diploma eşdeğerliğini ve alan uygunluğunu ayrıca değerlendirir.",
            },
            "accepted_backgrounds": ["mechanical_engineering", "related_engineering_subjects_subject_to_assessment"],
            "admission_mode": "direct_online_application_to_tuhh_with_foreign_degree_assessment",
            "required_documents": [
                "complete_university_transcript_or_provisional_transcript",
                "degree_certificate_or_provisional_degree_certificate_with_final_grade",
                "module_manual_for_the_applicant_bachelor_cohort",
                "proof_of_required_german_language_proficiency",
                "certified_german_or_english_translations_if_originals_use_another_language",
                "aps_certificate_for_degrees_or_schooling_from_china_india_or_vietnam",
            ],
            "verification_notes": {
                "en": "Non-EU applicants are eligible to apply: TU Hamburg publishes a dedicated route for applicants with qualifications from abroad, evaluates degrees issued in other countries, and gives APS rules for China, India and Vietnam. Eligibility is conditional on degree recognition, programme-specific subject fit and the German-language requirement; it is not automatic admission.",
                "tr": "AB dışı adaylar başvurabilir: TU Hamburg, yurt dışı diplomalı adaylar için özel başvuru yolunu yayımlar, diğer ülkelerde verilen dereceleri değerlendirir ve Çin, Hindistan ile Vietnam için APS kurallarını açıklar. Uygunluk; diploma tanıma, programa özgü alan uyumu ve Almanca şartına bağlıdır; otomatik kabul anlamına gelmez.",
            },
        }
    )

    new_sources = [
        {
            "url": "https://www.tuhh.de/tuhh/en/studying/before-studying/application/master-in-german/applicants-from-abroad",
            "title": "TU Hamburg: Applicants with Qualifications from Abroad — German-taught Master's",
            "source_type": "official_admission_page",
            "access_status": "ok",
            "last_checked": CHECKED_AT,
            "relevant_fields": ["admission", "non_eu_eligibility", "documents", "foreign_degree_recognition", "language"],
            "confidence": "high",
            "notes": {
                "en": "Current official page establishes direct online applications for foreign qualifications, foreign-degree assessment, document and translation rules, and APS certificates for China, India and Vietnam.",
                "tr": "Güncel resmî sayfa yabancı diplomalar için doğrudan çevrim içi başvuruyu, diploma değerlendirmesini, belge ve çeviri kurallarını, ayrıca Çin, Hindistan ve Vietnam için APS belgesini açıklar.",
            },
        },
        {
            "url": "https://www.tuhh.de/tuhh/studium/vor-dem-studium/studienangebot/masterstudiengaenge/luftfahrttechnik",
            "title": "TU Hamburg: Luftfahrttechnik, Master of Science",
            "source_type": "official_program_page",
            "access_status": "ok",
            "last_checked": CHECKED_AT,
            "relevant_fields": ["program", "admission", "non_eu_eligibility", "language", "deadline"],
            "confidence": "high",
            "notes": {
                "en": "The current programme page explicitly addresses applicants without a German bachelor's degree, requires sufficient German, and confirms the direct online application periods.",
                "tr": "Güncel program sayfası Alman lisans derecesi olmayan adayları açıkça ele alır, yeterli Almanca ister ve doğrudan çevrim içi başvuru dönemlerini doğrular.",
            },
        },
    ]
    source_log = record["source_profile"]["source_log"]
    existing_urls = {item.get("url") for item in source_log}
    source_log.extend(item for item in new_sources if item["url"] not in existing_urls)

    source_profile = record["source_profile"]
    source_profile.update(
        {
            "official_admission_page": new_sources[0]["url"],
            "last_verified": CHECKED_AT,
            "needs_verification": True,
            "verification_notes": {
                "en": "The checked official sources now cover the record's critical decision fields. Non-EU application eligibility is distinct from admission: foreign-degree recognition, subject fit and German proficiency remain applicant-specific gates.",
                "tr": "Kontrol edilen resmî kaynaklar artık kaydın kritik karar alanlarını kapsar. AB dışı başvuru uygunluğu kabulden farklıdır: yabancı diploma tanıma, alan uyumu ve Almanca yeterliği adaya özgü eşiklerdir.",
            },
        }
    )
    source_profile["field_confidence"]["admission"] = "high"
    source_profile["field_confidence"]["non_eu_eligibility"] = "high"

    flags = record["scoring_inputs"]["hard_filter_flags"]
    flags["non_eu_eligible"] = True
    flags["needs_verification"] = True

    quality = record["data_quality"]
    quality.update(
        {
            "status": "partial",
            "checked_official_source_count": len(source_log),
            "verified_fields": list(dict.fromkeys(quality["verified_fields"] + ["non_eu_eligibility"])),
            "unverified_critical_fields": [],
            "has_checked_source_log": True,
            "audited_at": CHECKED_AT,
        }
    )
    record["quality_control"].update(
        {
            "qc_status": "needs_revision",
            "checked_at": CHECKED_AT,
            "failed_canary_tests": ["critical_field_confidence_below_high"],
            "remaining_verification_tasks": [
                {
                    "en": "Replace generic or interpreted tuition, scholarship and curriculum evidence with programme-specific high-confidence publications when TU Hamburg releases them.",
                    "tr": "TU Hamburg yayımladığında genel veya yorum gerektiren ücret, burs ve müfredat kanıtlarını programa özgü yüksek güvenli yayınlarla değiştirin.",
                }
            ],
        }
    )

    record["decision_summary"]["main_risks"] = [
        {
            "en": "The programme is German-taught and foreign-degree recognition plus subject fit are assessed individually. University enrolment does not provide housing; TU Hamburg describes inexpensive accommodation as extremely difficult to find.",
            "tr": "Program Almanca yürütülür; yabancı diploma tanıma ve alan uyumu bireysel değerlendirilir. Üniversite kaydı konaklama sağlamaz; TU Hamburg uygun fiyatlı konut bulmayı son derece zor olarak tanımlar.",
        }
    ]

    save(DB_PATH, records)
    print(f"Verified TUHH non-EU application eligibility with {len(source_log)} checked official sources.")


if __name__ == "__main__":
    main()
