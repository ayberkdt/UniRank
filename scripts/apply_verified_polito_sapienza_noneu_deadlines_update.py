"""Apply current official 2026/27 non-EU and deadline evidence for two Italian MSc records."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from unirank.core.integrity import audit_record


DATA_PATH = ROOT / "data_base" / "italy.json"
CHECKED = "2026-08-14"

POLITO_ADMISSION = "https://www.polito.it/en/education/applying-studying-graduating/admissions-and-enrolment/master-s-degree-programmes/applicants-with-a-non-italian-qualification"
POLITO_REQUIREMENTS = "https://www.polito.it/sites/default/files/2025-12/A.%20Y.%2020262027%20COURSE%20SPECIFIC%20REQUIREMENTS.pdf"

SAPIENZA_ADMISSIONS = "https://www.uniroma1.it/it/pagina/international-admissions-2026-2027"
SAPIENZA_INTERNATIONAL_OFFICE = "https://www.uniroma1.it/en/node/24774"
SAPIENZA_MOVEIN_REQUIREMENTS = "https://www.uniroma1.it/sites/default/files/field_file_allegati/academic_requirements_movein_2026-2027_web_20260608.pdf"
SAPIENZA_PROGRAM_CALL = "https://corsidilaurea.uniroma1.it/sites/default/files/offertaformativa/documenti_ufficiali/187/33484_e_0.pdf"


def bi(en: str, tr: str) -> dict[str, str]:
    return {"en": en, "tr": tr}


def source(url: str, title: str, fields: list[str], access_status: str = "ok") -> dict:
    return {
        "url": url,
        "title": title,
        "source_type": "official_admission_page",
        "access_status": access_status,
        "last_checked": CHECKED,
        "relevant_fields": fields,
        "confidence": "high",
        "notes": bi(
            "Current official 2026/27 source checked for the listed fields; closed-cycle dates are not extrapolated to 2027/28.",
            "Listelenen alanlar için güncel resmî 2026/27 kaynak kontrol edildi; kapanmış dönem tarihleri 2027/28'e taşınmaz.",
        ),
    }


def upsert_sources(profile: dict, additions: list[dict]) -> None:
    log = profile.setdefault("source_log", [])
    by_url = {item.get("url"): index for index, item in enumerate(log) if isinstance(item, dict)}
    for item in additions:
        index = by_url.get(item["url"])
        if index is None:
            log.append(item)
        else:
            log[index] = item


def finish(row: dict, note: dict[str, str]) -> None:
    profile = row["source_profile"]
    profile["last_verified"] = CHECKED
    profile["verification_notes"] = note
    quality = audit_record(row)
    quality["audited_at"] = CHECKED
    row["data_quality"] = quality
    complete = quality["status"] == "verified"
    if quality["unverified_critical_fields"]:
        remaining = [
            bi(
                f"Resolve remaining critical evidence gaps: {', '.join(quality['unverified_critical_fields'])}.",
                f"Kalan kritik kanıt boşluklarını giderin: {', '.join(quality['unverified_critical_fields'])}.",
            )
        ]
        failure = "missing_or_unverified_critical_fields"
    elif not complete:
        remaining = [
            bi(
                "Raise every decision-critical field group to high confidence; existing medium-confidence fee, scholarship or housing evidence remains explicitly qualified.",
                "Tüm karar-kritik alan gruplarını yüksek güvene çıkarın; mevcut orta güvenli ücret, burs veya konut kanıtları açıkça sınırlı tutulur.",
            )
        ]
        failure = "critical_field_confidence_below_high"
    else:
        remaining = []
        failure = None
    row["quality_control"] = {
        "qc_status": "passed" if complete else "needs_revision",
        "checked_at": CHECKED,
        "failed_canary_tests": [] if complete else [failure],
        "remaining_verification_tasks": remaining,
        "qc_notes": bi(
            "Official-source evidence now covers the complete critical decision-field set for this record.",
            "Resmî kaynak kanıtı artık bu kaydın kritik karar alanlarının tamamını kapsıyor.",
        ) if complete else bi(
            "The record retains explicit unresolved critical fields; no unsupported value is treated as verified.",
            "Kayıt çözülemeyen kritik alanları açıkça korur; desteksiz hiçbir değer doğrulanmış sayılmaz.",
        ),
    }
    profile["needs_verification"] = not complete


def update_polito(row: dict) -> None:
    eligibility = row["eligibility_profile"]
    eligibility.update(
        {
            "eligible_for_non_eu": True,
            "required_previous_degree": bi(
                "An accredited foreign Bachelor's degree at EQF level 6, giving access to second-cycle study, plus programme-specific curricular and academic suitability.",
                "İkinci kademe eğitime erişim sağlayan, akredite bir kurumdan EQF 6 düzeyinde yabancı lisans diploması ile programa özgü müfredat ve akademik uygunluk gerekir.",
            ),
            "accepted_backgrounds": ["Industrial Engineering (recommended background; individual curricular assessment applies)"],
            "ranking_or_selection": "Two-step dossier review by the Recruitment and Admissions Unit and the Academic Committee",
            "admission_mode": bi(
                "Foreign-qualification dossier assessment; the offer is valid only for the applied academic year and cannot be deferred.",
                "Yabancı diploma dosya değerlendirmesi; teklif yalnız başvurulan akademik yıl için geçerlidir ve ertelenemez.",
            ),
            "required_documents": [
                bi("Passport", "Pasaport"),
                bi("Curriculum vitae", "Özgeçmiş"),
                bi("Bachelor's diploma or official provisional-graduation document", "Lisans diploması veya resmî geçici mezuniyet belgesi"),
                bi("Official transcript including grading and credit systems", "Notlandırma ve kredi sistemini içeren resmî transkript"),
                bi("Syllabus/course descriptions", "Ders içerikleri/müfredat açıklamaları"),
                bi("Italian B2 and English B2 evidence or a valid exemption", "İtalyanca B2 ve İngilizce B2 kanıtı veya geçerli muafiyet"),
                bi("Declaration of Value or CIMEA Statement of Comparability for enrolment", "Kayıt aşamasında Değer Beyanı veya CIMEA Karşılaştırılabilirlik Belgesi"),
            ],
            "motivation_letter_required": False,
            "cv_required": True,
            "recommendation_required": False,
            "portfolio_required": False,
            "interview_required": False,
            "test_required": False,
            "application_fee_eur": 50,
            "notes_for_turkish_students": bi(
                "A Turkey-based applicant follows the overseas non-EU visa route. Documents outside Italian, English, French or Spanish need an official Italian/English translation; the Italian-taught programme requires both Italian B2 and English B2 evidence.",
                "Türkiye'de yaşayan aday, yurt dışında ikamet eden vizeye tabi non‑EU yolunu izler. İtalyanca, İngilizce, Fransızca veya İspanyolca dışındaki belgeler resmî İtalyanca/İngilizce çeviri ister; İtalyanca yürütülen program hem İtalyanca B2 hem İngilizce B2 kanıtı gerektirir.",
            ),
            "verification_notes": bi(
                "The 2026/27 foreign-qualification route is open to overseas non-EU applicants. Aerospace Engineering recommends an Industrial Engineering background; suitability is decided from the dossier.",
                "2026/27 yabancı diploma yolu, yurt dışında yaşayan non‑EU adaylara açıktır. Aerospace Engineering için Industrial Engineering altyapısı önerilir; uygunluk dosya üzerinden kararlaştırılır.",
            ),
            "gre": {
                "policy": "optional_supporting_document_not_programme_requirement",
                "test_type": "GRE General Test",
                "minimum_scores": {},
                "recommended_scores": {},
                "validity_rule": "",
                "waiver_rules": [],
                "source_ids": [POLITO_ADMISSION, POLITO_REQUIREMENTS],
            },
        }
    )

    row["language_profile"].update(
        {
            "teaching_language": ["Italian"],
            "english_required": True,
            "english_level_required": "B2; 2026/27 course-specific table publishes IELTS 5.5 as the minimum score",
            "minimum_scores": {"ielts_academic": {"overall": 5.5}},
            "italian_required": True,
            "italian_level_required": "B2",
            "language_risk": "high",
            "verification_notes": bi(
                "The official 2026/27 table classifies the programme as Italian-taught and requires Italian B2 plus IELTS 5.5/accepted English-B2 equivalent. A Turkish English-medium degree is not assumed to waive Italian.",
                "Resmî 2026/27 tablosu programı İtalyanca olarak sınıflandırır ve İtalyanca B2 ile IELTS 5.5/kabul edilen İngilizce B2 eşdeğerini ister. Türkiye'deki İngilizce eğitimli bir diploma İtalyanca muafiyeti sayılmaz.",
            ),
        }
    )

    row["application_timeline_profile"] = {
        "academic_year": "2026/2027 foreign-qualification cycle",
        "intake_terms": ["First semester 2026/27 for overseas non-EU visa applicants"],
        "application_rounds": [
            "Call 1: 19 December 2025–13 February 2026, 14:00 Italian time (extended; closed)",
            "Call 2: 18 March–20 April 2026, 14:00 Italian time (extended/postponed; closed)",
        ],
        "non_eu_deadline": "2026-04-20T14:00:00+02:00",
        "eu_deadline": "2026-04-20T14:00:00+02:00 (foreign-qualification call)",
        "application_deadline": "2026-04-20T14:00:00+02:00 (last overseas non-EU application call; closed)",
        "pre_enrolment_required": True,
        "universitaly_required": True,
        "visa_sensitive_deadline": "2026-07-15 (indicative Universitaly target for eligible Call 2 applicants; Call 1 target 2026-06-30)",
        "enrollment_deadline": "2026-10-05 (first-semester online enrolment close)",
        "timeline_risk": "high",
        "deadline_events": [
            {"event": "call_1_application_close", "date": "2026-02-13T14:00:00+01:00", "status": "closed"},
            {"event": "call_1_result", "date": "2026-04-15", "status": "published_cycle"},
            {"event": "call_2_application_close", "date": "2026-04-20T14:00:00+02:00", "status": "closed"},
            {"event": "call_2_result", "date": "2026-06-22", "status": "published_cycle"},
            {"event": "universitaly_target_call_1", "date": "2026-06-30", "status": "closed_indicative_target"},
            {"event": "universitaly_target_call_2", "date": "2026-07-15", "status": "closed_indicative_target"},
            {"event": "online_enrolment_close", "date": "2026-10-05", "status": "published"},
            {"event": "study_visa_upload_deadline", "date": "2026-11-30", "status": "published"},
        ],
        "deadline_notes": bi(
            "All published 2026/27 application calls for foreign qualifications are closed. Overseas non-EU visa applicants cannot use the second-semester route, which is limited to EU applicants and non-EU applicants residing in Italy. No 2027/28 date is inferred.",
            "Yabancı diplomalar için yayımlanan tüm 2026/27 başvuru çağrıları kapanmıştır. Yurt dışında yaşayan vizeye tabi non‑EU adaylar, yalnız AB adayları ve İtalya'da ikamet eden non‑EU adaylara açık ikinci dönem yolunu kullanamaz. 2027/28 tarihi tahmin edilmez.",
        ),
    }

    profile = row["source_profile"]
    profile["official_admission_page"] = POLITO_ADMISSION
    profile["field_confidence"].update({"admission": "high", "language": "high", "non_eu_eligibility": "high", "deadline": "high", "deadlines": "high"})
    upsert_sources(
        profile,
        [
            source(POLITO_ADMISSION, "PoliTo applicants with a non-Italian qualification – Master's A.Y. 2026/27", ["admission", "non_eu_eligibility", "deadline", "language"]),
            source(POLITO_REQUIREMENTS, "PoliTo 2026/27 course-specific Master's requirements", ["admission", "language"], "pdf"),
        ],
    )
    finish(
        row,
        bi(
            "Critical facts are supported by current checked official sources. The 2026/27 admission cycle is closed; the record deliberately does not predict 2027/28 dates.",
            "Kritik bilgiler güncel ve kontrol edilmiş resmî kaynaklarla desteklenir. 2026/27 kabul dönemi kapanmıştır; kayıt 2027/28 tarihlerini özellikle tahmin etmez.",
        ),
    )


def update_sapienza(row: dict) -> None:
    eligibility = row["eligibility_profile"]
    eligibility.update(
        {
            "eligible_for_non_eu": True,
            "required_previous_degree": bi(
                "A recognized three-year Bachelor's degree or equivalent foreign qualification suitable for second-cycle admission.",
                "İkinci kademe kabulüne uygun, tanınan üç yıllık lisans diploması veya eşdeğer yabancı diploma gerekir.",
            ),
            "accepted_backgrounds": [
                "Aeronautical/Aerospace Engineering (preferred)",
                "Industrial Engineering, especially Mechanical or Energy Engineering",
                "Other Engineering or Physics only for outstanding candidates",
            ],
            "minimum_gpa": 75,
            "gpa_scale": "100 (MoveIN pre-selection); final programme call separately evaluates foreign qualifications",
            "ranking_or_selection": "MoveIN dossier screening followed by technical interview; final eligibility and personal-knowledge checks remain mandatory",
            "admission_mode": bi(
                "Visa-seeking non-EU applicants need a MoveIN pre-acceptance letter, Universitaly pre-enrolment and the programme's Infostud eligibility assessment.",
                "Vizeye tabi non‑EU adaylar MoveIN ön kabul mektubu, Universitaly ön kayıt ve programın Infostud uygunluk değerlendirmesini tamamlamalıdır.",
            ),
            "required_documents": [
                bi("Valid passport", "Geçerli pasaport"),
                bi("First-cycle university degree and official transcript", "Birinci kademe üniversite diploması ve resmî transkript"),
                bi("Official sworn translations in Italian or English when required", "Gerektiğinde İtalyanca veya İngilizce resmî yeminli çeviriler"),
                bi("CIMEA/ARDI documentation or the applicable Declaration of Value/Diploma Supplement route", "Uygun CIMEA/ARDI belgeleri veya ilgili Değer Beyanı/Diploma Eki yolu"),
                bi("Mandatory MoveIN pre-acceptance letter for overseas non-EU visa applicants", "Yurt dışında yaşayan vizeye tabi non‑EU adaylar için zorunlu MoveIN ön kabul mektubu"),
                bi("Study visa and residence-permit application receipts at enrolment", "Kayıt aşamasında öğrenci vizesi ve oturma izni başvuru makbuzları"),
            ],
            "motivation_letter_required": None,
            "motivation_evaluated": True,
            "cv_required": None,
            "cv_evaluated": True,
            "recommendation_required": False,
            "portfolio_required": False,
            "interview_required": True,
            "interview_policy": "MoveIN selection is described as dossier screening followed by an interview; the final programme call states foreign-degree applicants may be invited by the Admissions Committee.",
            "test_required": False,
            "preselection_fee_eur": 30,
            "infostud_eligibility_fee_eur": 10,
            "notes_for_turkish_students": bi(
                "A Turkey-based applicant is an overseas non-EU visa applicant: complete MoveIN by 15 May 2026, Universitaly by 30 June 2026 and the €10 Infostud eligibility step by 15 September 2026. An English-medium Turkish degree is not listed among the automatic MoveIN language waivers.",
                "Türkiye'de yaşayan aday, yurt dışında ikamet eden vizeye tabi non‑EU statüsündedir: MoveIN'i 15 Mayıs 2026'ya, Universitaly'yi 30 Haziran 2026'ya ve 10 EUR'luk Infostud uygunluk adımını 15 Eylül 2026'ya kadar tamamlamalıdır. Türkiye'deki İngilizce eğitimli diploma, otomatik MoveIN dil muafiyetleri arasında listelenmemiştir.",
            ),
            "verification_notes": bi(
                "The 2026/27 MoveIN document explicitly includes Space and Astronautical Engineering and publishes its academic, GPA, interview and English criteria. Final foreign-degree suitability is still decided individually.",
                "2026/27 MoveIN belgesi Space and Astronautical Engineering'i açıkça içerir ve akademik, GPA, mülakat ve İngilizce ölçütlerini yayımlar. Yabancı diplomanın nihai uygunluğu yine bireysel değerlendirilir.",
            ),
            "gre": {
                "policy": "not_listed_as_required_or_recommended_for_this_programme",
                "test_type": "GRE General Test",
                "minimum_scores": {},
                "recommended_scores": {},
                "validity_rule": "",
                "waiver_rules": [],
                "source_ids": [SAPIENZA_MOVEIN_REQUIREMENTS, SAPIENZA_PROGRAM_CALL],
            },
        }
    )

    row["language_profile"].update(
        {
            "teaching_language": ["English"],
            "english_required": True,
            "english_level_required": "CEFR B2",
            "accepted_english_tests": ["IELTS Academic", "TOEFL iBT", "Cambridge English B2 First", "Trinity ISE II"],
            "minimum_scores": {"ielts_academic": {"overall": 5.5}, "toefl_ibt": {"overall": 80}},
            "english_exemptions": [
                "Native English speaker",
                "English-taught degree from an accredited EU/EEA/Schengen institution or Australia, Canada, New Zealand, the United Kingdom or the United States",
                "International Baccalaureate, GCSE or comparable listed certificate",
            ],
            "italian_required": False,
            "language_risk": "medium",
            "verification_notes": bi(
                "MoveIN publishes B2, IELTS 5.5, TOEFL iBT 80, Cambridge B2 First and Trinity ISE II. Its medium-of-instruction waiver geography does not include Turkey, so a Turkish English-medium degree is not stored as an automatic waiver.",
                "MoveIN; B2, IELTS 5.5, TOEFL iBT 80, Cambridge B2 First ve Trinity ISE II eşiklerini yayımlar. Eğitim dili muafiyet coğrafyası Türkiye'yi içermediğinden Türkiye'deki İngilizce eğitimli diploma otomatik muafiyet olarak kaydedilmez.",
            ),
        }
    )

    row["application_timeline_profile"] = {
        "academic_year": "2026/2027",
        "intake_terms": ["Autumn 2026; classes begin 24 September 2026"],
        "application_rounds": [
            "MoveIN pre-selection for overseas non-EU visa applicants: 22 December 2025–15 May 2026 (closed)",
            "MoveIN pre-selection for EU/equivalent applicants: 22 December 2025–31 July 2026 (closed)",
        ],
        "non_eu_deadline": "2026-05-15",
        "eu_deadline": "2026-07-31",
        "application_deadline": "2026-05-15 (MoveIN pre-selection for overseas non-EU visa applicants; closed)",
        "pre_enrolment_required": True,
        "universitaly_required": True,
        "visa_sensitive_deadline": "2026-06-30T23:59:00+02:00",
        "enrollment_deadline": "2026-09-15 (Infostud eligibility check deadline for non-EU visa applicants; final fee deadline follows university regulations)",
        "timeline_risk": "high",
        "deadline_events": [
            {"event": "movein_open", "date": "2025-12-22", "status": "closed_cycle"},
            {"event": "movein_non_eu_visa_deadline", "date": "2026-05-15", "status": "closed"},
            {"event": "universitaly_deadline", "date": "2026-06-30T23:59:00+02:00", "status": "closed"},
            {"event": "infostud_eligibility_window_open", "date": "2026-07-02", "status": "published_cycle"},
            {"event": "infostud_non_eu_visa_deadline", "date": "2026-09-15", "status": "published"},
            {"event": "classes_begin", "date": "2026-09-24", "status": "published"},
        ],
        "deadline_notes": bi(
            "The visa-applicant process has three distinct deadlines: MoveIN pre-selection, Universitaly pre-enrolment, then the €10 Infostud eligibility assessment. The first two are already closed on the verification date; no 2027/28 date is inferred.",
            "Vizeye tabi aday sürecinde üç ayrı tarih vardır: MoveIN ön seçimi, Universitaly ön kaydı ve ardından 10 EUR'luk Infostud uygunluk değerlendirmesi. Doğrulama tarihinde ilk ikisi kapanmıştır; 2027/28 tarihi tahmin edilmez.",
        ),
    }

    profile = row["source_profile"]
    profile["official_admission_page"] = SAPIENZA_PROGRAM_CALL
    profile["field_confidence"].update({"admission": "high", "language": "high", "non_eu_eligibility": "high", "deadline": "high", "deadlines": "high"})
    upsert_sources(
        profile,
        [
            source(SAPIENZA_ADMISSIONS, "Sapienza international admissions 2026/27 – programmes in English", ["admission", "non_eu_eligibility", "deadline", "language"]),
            source(SAPIENZA_INTERNATIONAL_OFFICE, "Sapienza International Student Office A.Y. 2026/27", ["admission", "non_eu_eligibility", "deadline"]),
            source(SAPIENZA_MOVEIN_REQUIREMENTS, "Sapienza MoveIN academic requirements 2026/27", ["admission", "non_eu_eligibility", "deadline", "language"], "pdf"),
            source(SAPIENZA_PROGRAM_CALL, "Sapienza Space and Astronautical Engineering admission procedure 2026/27", ["admission", "non_eu_eligibility", "deadline", "language"], "pdf"),
        ],
    )
    finish(
        row,
        bi(
            "Current official 2026/27 sources now cover non-EU eligibility, the three-stage visa-applicant timeline, programme admission, English evidence and enrolment documents. Closed dates are not projected forward.",
            "Güncel resmî 2026/27 kaynakları artık non‑EU uygunluğu, vize adayının üç aşamalı takvimini, program kabulünü, İngilizce kanıtını ve kayıt belgelerini kapsar. Kapanmış tarihler ileri taşınmaz.",
        ),
    )


def main() -> None:
    payload = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    rows = {row.get("id"): row for row in payload["universities"]}
    update_polito(rows["polito-msc-aerospace"])
    update_sapienza(rows["sapienza_space_astronautical_msc"])
    DATA_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
