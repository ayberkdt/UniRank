"""Apply verified Glasgow Aerospace MSc language, timeline, funding and living data."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from unirank.core.integrity import audit_record


DATA_PATH = ROOT / "data_base" / "ingiltere.json"
RECORD_ID = "university-of-glasgow"
COURSE_URL = "https://www.gla.ac.uk/postgraduate/taught/aerospace-engineering/"
HOUSING_URL = "https://www.gla.ac.uk/postgraduate/accommodation/fees/"
LIVING_URL = (
    "https://www.gla.ac.uk/myglasgow/registry/finance/usloans/"
    "costofliving202627/"
)


def bi(en: str, tr: str) -> dict[str, str]:
    return {"en": en, "tr": tr}


def upsert_source(source_log: list[dict], source: dict) -> None:
    matches = [item for item in source_log if item.get("url") == source["url"]]
    if matches:
        if len(matches) != 1:
            raise RuntimeError(f"Duplicate source URL: {source['url']}")
        matches[0].update(source)
    else:
        source_log.append(source)


def main() -> None:
    rows = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    matches = [row for row in rows if row.get("id") == RECORD_ID]
    if len(matches) != 1:
        raise RuntimeError(f"Expected one {RECORD_ID!r} record; found {len(matches)}")
    row = matches[0]

    row["teaching_language"] = ["English"]
    language = row.setdefault("language_profile", {})
    language.update(
        {
            "teaching_language": ["English"],
            "teaching_languages": ["English"],
            "english_required": True,
            "english_level_required": "programme_specific",
            "minimum_scores": {
                "ielts_academic": {"overall": 6.5, "each_subtest": 6.0},
                "toefl_ibt_up_to_2026_01_20": {
                    "overall": 90,
                    "reading": 20,
                    "listening": 19,
                    "speaking": 19,
                    "writing": 21,
                },
                "toefl_ibt_from_2026_01_21": {
                    "overall": 92,
                    "reading": 22,
                    "listening": 20,
                    "speaking": 23,
                    "writing": 21,
                },
                "pte_academic": {
                    "overall": 65,
                    "reading": 60,
                    "listening": 60,
                    "speaking": 65,
                    "writing": 60,
                },
                "cambridge_cae_or_cpe": {"overall": 176, "each_subtest": 169},
                "oxford_english_test": {"overall": 7, "each_subtest": 6},
                "languagecert_academic": {"overall": 70, "each_subtest": 65},
                "password_skills_plus": {"overall": 6.5, "each_subtest": 6.0},
            },
            "test_validity": "2 years 5 months before programme start date",
            "ielts_one_skill_retake_accepted": True,
            "waiver_rules": [
                "Degree route from a UKVI-defined majority-English-speaking country, "
                "including Canada if taught in English, subject to the programme page's "
                "study-duration and six-year recency rules",
                "Successful approved pre-sessional course",
            ],
            "language_risk": "medium",
            "verification_notes": bi(
                "The programme page publishes programme-specific English proficiency "
                "requirements and delivery through lectures, seminars, tutorials, labs "
                "and projects. English is recorded as the operational study language "
                "with medium confidence because the live page does not expose a separate "
                "field labelled 'language of instruction'.",
                "Program sayfası programa özgü İngilizce yeterlilik şartlarını ve ders, "
                "seminer, uygulama, laboratuvar ile proje yoluyla eğitimi yayımlar. Canlı "
                "sayfa ayrı bir 'eğitim dili' alanı göstermediği için İngilizce, orta "
                "güvenle fiilî öğrenim dili olarak kaydedilir.",
            ),
        }
    )

    eligibility = row.setdefault("eligibility_profile", {})
    eligibility["required_documents"] = [
        "Official degree certificate(s), if completed",
        "Official academic transcript(s)",
        "Official English translations where needed",
        "One reference letter on headed paper",
        "English-language evidence if first language is not English",
        "Any programme-specific additional documents",
        "Passport photo page",
    ]
    eligibility["gre"] = {
        "policy": "not_listed_in_checked_official_required_documents",
        "test_type": "GRE",
        "minimum_scores": {},
        "recommended_scores": {},
        "validity_rule": "",
        "waiver_rules": [],
        "source_ids": [COURSE_URL],
    }

    timeline = row.setdefault("application_timeline_profile", {})
    timeline.update(
        {
            "academic_year": "2026/2027",
            "intake_terms": ["September"],
            "non_eu_deadline": "2026-08-24",
            "eu_deadline": "2026-08-24",
            "application_deadline": "2026-08-24",
            "winter_deadline": None,
            "timeline_risk": "medium",
            "deadline_events": [
                {
                    "event": "programme_application_deadline",
                    "date": "2026-08-24",
                    "date_status": "current",
                    "applicant_scope": "international_and_eu",
                    "source_url": COURSE_URL,
                },
                {
                    "event": "programme_start",
                    "date": "2026-09-14",
                    "date_status": "current",
                    "applicant_scope": "all",
                    "source_url": "https://www.gla.ac.uk/postgraduate/dates/scienceengineering/",
                },
            ],
            "deadline_notes": bi(
                "The live programme page lists 24 August 2026 for International and EU "
                "applicants. An ATAS certificate must be requested immediately after an "
                "offer unless the applicant's nationality is exempt.",
                "Canlı program sayfası Uluslararası ve AB adayları için 24 Ağustos 2026 "
                "tarihini listeler. Uyruk muaf değilse teklif sonrasında ATAS belgesine "
                "hemen başvurulmalıdır.",
            ),
        }
    )

    scholarship = row.setdefault("scholarship_profile", {})
    scholarship.update(
        {
            "application_mode": "mixed",
            "automatic_consideration": True,
            "separate_application_required": True,
            "non_eu_eligible": True,
            "funding_status": "multiple_scheme_specific_opportunities",
            "funding_notes": bi(
                "The course page lists multiple 2026/27 schemes with different country, "
                "offer, merit and application rules. World Changers is automatic for "
                "eligible nationalities; Global Leadership is open to International-fee "
                "PGT applicants and invites an application. Awards cannot be generalized "
                "to every non-EU student.",
                "Ders sayfası farklı ülke, teklif, başarı ve başvuru kuralları olan çok "
                "sayıda 2026/27 seçeneği listeler. World Changers uygun uyruklar için "
                "otomatiktir; Global Leadership uluslararası ücret statüsündeki PGT "
                "adaylarına açıktır ve başvuru ister. Ödüller tüm AB dışı öğrencilere "
                "genellenemez.",
            ),
            "opportunities": [
                {
                    "name": "World Changers Glasgow Scholarship",
                    "academic_year": "2026/2027",
                    "award": {"amount": 5000, "currency": "GBP", "type": "tuition_discount"},
                    "application_mode": "automatic",
                    "applicant_scope": "listed_eligible_nationalities",
                    "source_url": COURSE_URL,
                },
                {
                    "name": "Global Leadership Scholarship",
                    "academic_year": "2026/2027",
                    "award": {"amount": None, "currency": "GBP", "type": "one_year_tuition_discount"},
                    "application_mode": "separate",
                    "applicant_scope": "international_fee_postgraduate_taught_masters",
                    "deadline": None,
                    "deadline_status": "currently_no_closing_date_published",
                    "source_url": COURSE_URL,
                },
            ],
        }
    )

    living = row.setdefault("living_profile", {})
    living.update(
        {
            "city_cost_level": "unknown",
            "housing_difficulty": None,
            "living_risk": "medium",
            "housing_access": "unknown",
            "housing_application_separate": True,
            "housing_options": ["University postgraduate residences", "Family/partner accommodation"],
            "official_rent_items": [
                {
                    "item": "published_postgraduate_room_types",
                    "amount_min": 141.47,
                    "amount_max": 258.72,
                    "currency": "GBP",
                    "period": "week",
                    "academic_year": "2026/2027",
                    "contract_lengths_vary": True,
                    "includes": ["heating_and_utilities", "wifi", "possessions_insurance"],
                    "source_url": HOUSING_URL,
                },
                {
                    "item": "published_postgraduate_room_contract_totals",
                    "amount_min": 5517.33,
                    "amount_max": 13194.72,
                    "currency": "GBP",
                    "period": "contract",
                    "academic_year": "2026/2027",
                    "contract_lengths_vary": True,
                    "source_url": HOUSING_URL,
                },
            ],
            "official_living_cost_items": [
                {
                    "item": "year_1_pgt_masters_cost_of_attendance_borrowing_maximum",
                    "amount": 31958,
                    "currency": "GBP",
                    "period": "52_week_academic_year",
                    "academic_year": "2026/2027",
                    "applicant_scope": "new_US_federal_student_aid_borrower",
                    "includes": [
                        "rent", "utilities_and_mobile", "food", "daily_travel",
                        "books_and_computer", "personal_expenses", "visa", "IHS",
                        "two_flights_home_allowance",
                    ],
                    "source_url": LIVING_URL,
                }
            ],
            "housing_notes": bi(
                "Published postgraduate residence examples range from GBP 141.47 to "
                "GBP 258.72 per week in 2026/27; room type and contract length differ, "
                "and availability is not guaranteed by the fee table.",
                "Yayımlanan 2026/27 lisansüstü yurt örnekleri haftalık 141,47–258,72 "
                "GBP aralığındadır; oda türü ve sözleşme süresi değişir ve ücret tablosu "
                "yer garantisi vermez.",
            ),
            "verification_notes": bi(
                "The GBP 31,958 annual figure is retained only as the University's US "
                "federal-loan maximum cost-of-attendance example for a new first-year "
                "PGT master's student. It is not presented as a universal or required "
                "budget for all international students.",
                "Yıllık 31.958 GBP tutar yalnızca Üniversitenin yeni birinci sınıf PGT "
                "yüksek lisans öğrencisi için ABD federal kredi azami katılım maliyeti "
                "örneği olarak tutulur. Tüm uluslararası öğrenciler için evrensel veya "
                "zorunlu bütçe olarak sunulmaz.",
            ),
        }
    )

    source_profile = row.setdefault("source_profile", {})
    source_profile.update(
        {
            "official_housing_page": HOUSING_URL,
            "official_cost_of_living_page": LIVING_URL,
            "last_verified": "2026-08-14",
        }
    )
    confidence = source_profile.setdefault("field_confidence", {})
    confidence.update(
        {
            "language": "medium",
            "admission": "high",
            "non_eu_eligibility": "high",
            "scholarship": "high",
            "deadline": "high",
            "deadlines": "high",
            "application_timeline_profile": "high",
            "living_profile": "high",
            "housing": "high",
        }
    )

    source_log = source_profile.setdefault("source_log", [])
    programme_sources = [source for source in source_log if source.get("url") == COURSE_URL]
    if not programme_sources:
        raise RuntimeError("Glasgow programme sources are missing")
    for source in programme_sources:
        relevant = list(source.get("relevant_fields") or [])
        if source.get("source_type") == "official_program_page" and "language" not in relevant:
            relevant.append("language")
        source["relevant_fields"] = relevant
        source["last_checked"] = "2026-08-14"
        source["notes"] = bi(
            "Live official 2026/27 Aerospace Engineering MSc page checked directly for "
            "the fields mapped in this source entry.",
            "Canlı resmî 2026/27 Aerospace Engineering MSc sayfası bu kaynak kaydında "
            "eşlenen alanlar için doğrudan kontrol edildi.",
        )

    upsert_source(
        source_log,
        {
            "url": HOUSING_URL,
            "title": "University of Glasgow postgraduate accommodation fees 2026/27",
            "source_type": "official_housing_page",
            "access_status": "ok",
            "last_checked": "2026-08-14",
            "relevant_fields": ["housing", "living"],
            "confidence": "high",
            "notes": bi(
                "Official fee table publishes weekly and contract totals across named "
                "postgraduate residences, with inclusions and contract dates.",
                "Resmî ücret tablosu adlandırılmış lisansüstü yurtlar için haftalık ve "
                "sözleşme toplamlarını, kapsam ve sözleşme tarihleriyle yayımlar.",
            ),
        },
    )
    upsert_source(
        source_log,
        {
            "url": LIVING_URL,
            "title": "University of Glasgow cost of living 2026/27 — US loans",
            "source_type": "official_cost_of_living_page",
            "access_status": "ok",
            "last_checked": "2026-08-14",
            "relevant_fields": ["living", "housing"],
            "confidence": "high",
            "notes": bi(
                "Official US-loans cost-of-attendance page; values are stored with its "
                "borrower scope and must not be generalized to every student.",
                "Resmî ABD kredileri katılım maliyeti sayfasıdır; değerler borçlu kapsamıyla "
                "saklanır ve her öğrenciye genellenmemelidir.",
            ),
        },
    )

    quality = audit_record(row)
    quality["audited_at"] = "2026-08-14"
    row["data_quality"] = quality
    source_profile["needs_verification"] = quality["status"] != "verified"

    qc = row.setdefault("quality_control", {})
    qc.update(
        {
            "qc_status": "needs_revision" if quality["status"] != "verified" else "passed",
            "checked_at": "2026-08-14",
            "failed_canary_tests": [],
            "remaining_verification_tasks": [
                bi(
                    "Replace the medium-confidence operational English-language evidence "
                    "with a current programme specification explicitly labelling the "
                    "language of instruction, if Glasgow publishes one.",
                    "Glasgow yayımlarsa orta güvenli fiilî İngilizce kanıtını, eğitim "
                    "dilini açıkça etiketleyen güncel program spesifikasyonuyla değiştirin.",
                )
            ],
            "qc_notes": bi(
                "All decision-critical fields have checked official evidence; the record "
                "remains partial only because teaching language is supported operationally "
                "rather than by a dedicated current programme-specification label.",
                "Tüm karar-kritik alanlarda kontrol edilmiş resmî kanıt vardır; kayıt yalnızca "
                "eğitim dili güncel ayrı program-spesifikasyon etiketi yerine fiilî kanıtla "
                "desteklendiği için kısmi kalır.",
            ),
        }
    )

    DATA_PATH.write_text(
        json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
