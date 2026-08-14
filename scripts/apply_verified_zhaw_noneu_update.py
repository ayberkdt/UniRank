"""Close the ZHAW MSE Aviation non-EU eligibility gap with official evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data_base" / "isvicre.json"
RECORD_ID = "ch-zhaw-aviation-mse"
CHECKED_AT = "2026-08-14"
FOREIGN_REQUIREMENTS_URL = (
    "https://www.zhaw.ch/en/engineering/study/masters-degree-programme/"
    "admission-requirements/requirements"
)
ADMISSION_URL = (
    "https://www.zhaw.ch/en/engineering/study/masters-degree-programme/"
    "admission-requirements?L=1"
)


def main() -> None:
    records = json.loads(DB_PATH.read_text(encoding="utf-8"))
    record = next(item for item in records if item.get("id") == RECORD_ID)

    eligibility = record["eligibility_profile"]
    eligibility.update(
        {
            "eligible_for_non_eu": True,
            "required_documents": [
                "bachelor_diploma_and_official_transcripts",
                "grading_system_and_final_grade",
                "certified_translation_into_english_french_or_german_if_needed",
                "curriculum_vitae",
                "statement_of_purpose_maximum_500_words_with_preferred_institute_or_centre",
                "c1_english_language_proof_or_documented_waiver",
                "two_academic_or_supervisor_recommendation_letters",
                "bachelor_thesis_copy_if_requested",
            ],
            "verification_notes": {
                "en": "Applicants with foreign bachelor's degrees, including degrees outside the EU/EFTA, are eligible for the admission procedure. ZHAW expects a recognised relevant engineering degree, normally top 35% / CGPA 80%, then conducts a formal review and institute/centre selection; admission is competitive and not guaranteed.",
                "tr": "AB/EFTA dışındaki dereceler dahil yabancı lisans derecesi sahipleri kabul sürecine başvurabilir. ZHAW, genellikle ilk %35 / CGPA %80 düzeyinde tanınmış ve ilgili bir mühendislik derecesi bekler; ardından biçimsel inceleme ve enstitü/merkez seçimi yapar. Kabul rekabetçidir ve garanti değildir.",
            },
            "gre": {
                "policy": "recommended_for_bachelor_degrees_outside_eu_efta",
                "test_type": "GRE General Test",
                "minimum_scores": {},
                "recommended_scores": {},
                "validity_rule": "not_published",
                "waiver_rules": [],
                "source_ids": [FOREIGN_REQUIREMENTS_URL],
                "notes": {
                    "en": "ZHAW says the GRE General Test is considered an advantage for applicants with a bachelor's degree outside the EU/EFTA; it does not call it mandatory or publish a minimum score.",
                    "tr": "ZHAW, AB/EFTA dışından lisans derecesi bulunan adaylar için GRE General Test'in avantaj sayıldığını belirtir; sınavı zorunlu tutmaz veya asgari puan yayımlamaz.",
                },
            },
        }
    )

    record["language_profile"].update(
        {
            "english_level_required": "C1",
            "accepted_english_evidence": [
                "Cambridge Advanced (CAE)",
                "BEC Higher",
                "IELTS 7",
                "TOEFL 95",
            ],
            "english_waiver_rules": [
                "native_english_speaker",
                "completed_bachelor_degree_in_an_english_taught_undergraduate_programme",
            ],
            "verification_notes": {
                "en": "The foreign-degree requirements page requires C1 English and lists CAE, BEC Higher, IELTS 7 and TOEFL 95 as examples. Native English speakers and applicants who completed an English-taught bachelor's programme do not need an English certificate.",
                "tr": "Yabancı derece şartları sayfası C1 İngilizce ister ve CAE, BEC Higher, IELTS 7 ile TOEFL 95'i örnek olarak listeler. Ana dili İngilizce olanlar ve İngilizce yürütülen bir lisans programını tamamlayanlar İngilizce belgesinden muaftır.",
            },
        }
    )

    record["cost_profile"]["application_fee_items"] = [
        {
            "amount": 100,
            "currency": "CHF",
            "period": "one_time",
            "applicant_scope": "mse_applicant",
            "mandatory": True,
            "basis": "Application is processed only after the admission processing fee is paid",
            "source_ids": [ADMISSION_URL],
        }
    ]

    source_log = record["source_profile"]["source_log"]
    foreign_source = next(item for item in source_log if item.get("url") == FOREIGN_REQUIREMENTS_URL)
    foreign_source["relevant_fields"] = list(
        dict.fromkeys(
            foreign_source.get("relevant_fields", [])
            + ["non_eu_eligibility", "gre", "language", "documents"]
        )
    )
    foreign_source["notes"] = {
        "en": "Current official requirements explicitly cover foreign bachelor's degrees, including the outside-EU/EFTA GRE guidance, C1 English evidence and waivers, and the full application document list.",
        "tr": "Güncel resmî şartlar yabancı lisans derecelerini, AB/EFTA dışı GRE rehberini, C1 İngilizce kanıtı ve muafiyetlerini ve tam başvuru belge listesini açıkça kapsar.",
    }

    admission_source = {
        "url": ADMISSION_URL,
        "title": "ZHAW MSE admission process for Swiss and foreign bachelor's degrees",
        "source_type": "official_admission_page",
        "access_status": "ok",
        "last_checked": CHECKED_AT,
        "relevant_fields": ["admission", "non_eu_eligibility", "application_fee", "deadline", "scholarship"],
        "confidence": "high",
        "notes": {
            "en": "The current page admits foreign-degree applicants to review, describes competitive institute/centre selection, publishes the CHF 100 processing fee and recurring application windows, and states that ZHAW does not grant scholarships.",
            "tr": "Güncel sayfa yabancı derece sahiplerini değerlendirmeye kabul eder, rekabetçi enstitü/merkez seçimini açıklar, 100 CHF işlem bedelini ve yinelenen başvuru dönemlerini yayımlar ve ZHAW'nin burs vermediğini belirtir.",
        },
    }
    if not any(
        item.get("url") == ADMISSION_URL and item.get("source_type") == "official_admission_page"
        for item in source_log
    ):
        source_log.append(admission_source)

    source_profile = record["source_profile"]
    source_profile["official_admission_page"] = ADMISSION_URL
    source_profile["last_verified"] = CHECKED_AT
    source_profile["needs_verification"] = True
    source_profile["field_confidence"]["admission"] = "high"
    source_profile["field_confidence"]["non_eu_eligibility"] = "high"
    source_profile["verification_notes"] = {
        "en": "All critical decision fields now have checked official evidence. The record remains partial because tuition, curriculum and housing/living evidence still includes medium-confidence interpretation or non-programme-specific guidance.",
        "tr": "Tüm kritik karar alanları artık kontrol edilmiş resmî kanıta sahiptir. Ücret, müfredat ve konut/yaşam kanıtlarında orta güvenli yorum veya programa özgü olmayan rehber bulunduğu için kayıt yine de kısmi kalır.",
    }

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
            "checked_at": CHECKED_AT,
            "qc_status": "needs_revision",
            "failed_canary_tests": ["critical_field_confidence_below_high"],
            "remaining_verification_tasks": [
                {
                    "en": "Obtain programme-specific confirmation of the complete foreign-student fee total and Aviation-profile housing access; replace interpreted curriculum evidence with a dated course-level plan if published.",
                    "tr": "Yabancı öğrenci için tam ücret toplamını ve Aviation profili konut erişimini programa özgü olarak teyit edin; yayımlanırsa yorum gerektiren müfredat kanıtını tarihli ders düzeyi planla değiştirin.",
                }
            ],
        }
    )

    DB_PATH.write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Verified ZHAW non-EU route, GRE guidance and C1 English rules with {len(source_log)} sources.")


if __name__ == "__main__":
    main()
