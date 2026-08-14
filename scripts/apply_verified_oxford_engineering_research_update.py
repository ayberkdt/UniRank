"""Apply the verified 2026/27 Oxford Engineering Science research MSc update."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from unirank.core.integrity import audit_record


DATA_PATH = ROOT / "data_base" / "ingiltere.json"
RECORD_ID = "university-of-oxford"
COURSE_URL = (
    "https://www.ox.ac.uk/admissions/graduate/courses/"
    "msc-research-engineering-science"
)


def bi(en: str, tr: str) -> dict[str, str]:
    return {"en": en, "tr": tr}


def main() -> None:
    rows = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    matches = [row for row in rows if row.get("id") == RECORD_ID]
    if len(matches) != 1:
        raise RuntimeError(f"Expected one {RECORD_ID!r} record; found {len(matches)}")
    row = matches[0]

    row["teaching_language"] = ["English"]

    eligibility = row.setdefault("eligibility_profile", {})
    eligibility.update(
        {
            "eligible_for_non_eu": True,
            "required_previous_degree": (
                "First-class or strong upper-second-class honours degree, or "
                "international equivalent, in engineering or a related discipline "
                "relevant to the proposed research"
            ),
            "accepted_backgrounds": [
                "Engineering",
                "Physics",
                "Materials science",
                "Computer science",
                "Applied mathematics",
                "Chemistry",
                "Medical sciences",
            ],
            "admission_mode": "research_application_with_supervisor_fit_review",
            "admission_risk": "high",
            "required_documents": [
                "Proposed field and title of research project",
                "Proposed supervisor name(s), up to four",
                "Three referees, at least one academic",
                "Official transcript(s)",
                "Certified English translation for any non-English transcript",
                "CV/resume",
                "Research proposal in English, 1,000-1,500 words",
                "English-language evidence if required",
            ],
            "verification_notes": bi(
                "The live 2026/27 course page gives international-equivalence guidance "
                "and an overseas fee category, so non-UK applicants may apply subject "
                "to meeting the course and country-equivalence requirements. Admission "
                "also depends on suitable supervision and support capacity.",
                "Canlı 2026/27 ders sayfası uluslararası denklik yönlendirmesi ve "
                "yurtdışı ücret kategorisi verir; dolayısıyla Birleşik Krallık dışı "
                "adaylar ders ve ülke denklik şartlarını karşılamak kaydıyla başvurabilir. "
                "Kabul ayrıca uygun danışman ve destek kapasitesine bağlıdır.",
            ),
            "gre": {
                "policy": "not_sought",
                "test_type": "GRE_or_GMAT",
                "minimum_scores": {},
                "recommended_scores": {},
                "validity_rule": "",
                "waiver_rules": [],
                "source_ids": [COURSE_URL],
            },
        }
    )

    language = row.setdefault("language_profile", {})
    language.update(
        {
            "teaching_language": ["English"],
            "english_required": True,
            "english_level_required": "Oxford higher level",
            "minimum_scores": {
                "ielts_academic": {"overall": 7.5, "each_component": 7.0},
                "toefl_ibt_before_2026_01_21": {
                    "overall": 110,
                    "listening": 22,
                    "reading": 24,
                    "speaking": 25,
                    "writing": 24,
                },
                "c1_advanced": {"overall": 191, "each_component": 185},
                "c2_proficiency": {"overall": 191, "each_component": 185},
                "oxford_test_of_english_advanced": {
                    "overall": 165,
                    "each_component": 155,
                },
            },
            "test_validity": "No more than two years before the course start date",
            "toefl_2026_transition": bi(
                "Oxford states that TOEFL tests taken from 21 January 2026 are not "
                "accepted until its review of the revised test is complete.",
                "Oxford, 21 Ocak 2026'dan itibaren alınan TOEFL sınavlarının yenilenen "
                "sınav incelemesi tamamlanana kadar kabul edilmediğini belirtir.",
            ),
            "language_risk": "medium",
            "verification_notes": bi(
                "The course page requires Oxford's higher English level. English is "
                "the University's stated language of instruction subject to rare "
                "regulatory exceptions; no exception is shown for this course.",
                "Ders sayfası Oxford'un yüksek İngilizce düzeyini ister. İngilizce, "
                "nadiren görülen düzenleyici istisnalar saklı kalmak üzere Üniversitenin "
                "belirttiği eğitim dilidir; bu ders için bir istisna gösterilmemiştir.",
            ),
        }
    )

    cost = row.setdefault("cost_profile", {})
    cost.update(
        {
            "academic_year": "2026/2027",
            "tuition_gbp_per_year": 34700,
            "tuition_gbp_per_year_min": 34700,
            "tuition_gbp_per_year_max": 34700,
            "tuition_basis": "official_2026_27_overseas_annual_course_fee",
            "application_fee": {
                "amount": 20,
                "currency": "GBP",
                "waiver_possible": True,
                "waiver_categories": [
                    "eligible applicants from low-income countries",
                    "eligible refugees and displaced persons",
                    "eligible UK applicants from low-income backgrounds",
                    "eligible recent Graduate Access Programme applicants",
                ],
            },
            "verification_notes": bi(
                "Oxford publishes GBP 34,700 per year for overseas fee status in "
                "2026/27. Fees are annual and usually increase for later years; the "
                "2-3 year programme total is therefore not calculated. No compulsory "
                "course element beyond fees and living costs is listed, but the research "
                "topic may create travel, research, or field-trip expenses.",
                "Oxford 2026/27 yurtdışı ücret statüsü için yıllık 34.700 GBP yayımlar. "
                "Ücretler yıllıktır ve sonraki yıllarda genellikle artar; bu nedenle "
                "2-3 yıllık program toplamı hesaplanmaz. Ücretler ve yaşam giderleri "
                "ötesinde zorunlu ders kalemi listelenmez; ancak araştırma konusu seyahat, "
                "araştırma veya saha gezisi gideri doğurabilir.",
            ),
        }
    )

    scholarship = row.setdefault("scholarship_profile", {})
    scholarship.update(
        {
            "non_eu_eligible": None,
            "application_mode": "mixed",
            "automatic_consideration": True,
            "separate_application_required": True,
            "funding_status": "available_but_not_guaranteed_and_scheme_specific",
            "funding_notes": bi(
                "For 2026/27 Oxford expected more than 1,100 full or partial graduate "
                "scholarships across many courses. Applicants who apply by this course's "
                "December deadline and receive an offer are automatically assessed for "
                "the majority of Oxford scholarships; some scholarships require a "
                "separate application or extra eligibility conditions. This does not "
                "establish eligibility for any named award.",
                "Oxford 2026/27 için birçok ders genelinde 1.100'den fazla tam veya "
                "kısmi lisansüstü burs beklediğini belirtir. Bu dersin Aralık son "
                "tarihine kadar başvurup teklif alanlar Oxford burslarının çoğu için "
                "otomatik değerlendirilir; bazı burslar ayrı başvuru veya ek uygunluk "
                "şartı ister. Bu bilgi herhangi bir adlandırılmış burs için uygunluk "
                "kanıtlamaz.",
            ),
            "opportunities": [
                {
                    "name": "Oxford graduate scholarships (general pool)",
                    "award_status": "scheme_specific",
                    "coverage": "full_or_partial",
                    "automatic_consideration": "majority_if_course_deadline_and_offer_conditions_met",
                    "separate_application": "required_for_some_schemes",
                    "non_eu_eligibility": None,
                    "source_url": COURSE_URL,
                }
            ],
        }
    )

    timeline = row.setdefault("application_timeline_profile", {})
    timeline.update(
        {
            "academic_year": "2026/2027",
            "intake_terms": ["October"],
            "non_eu_deadline": None,
            "application_deadline": None,
            "winter_deadline": None,
            "timeline_risk": "high",
            "deadline_events": [
                {
                    "event": "course_application_deadline",
                    "cycle": "2026/2027",
                    "date": None,
                    "date_status": "not_displayed_after_cycle_closed",
                    "applicant_scope": "all",
                    "status": "closed",
                    "notes": bi(
                        "The live page says the course is closed for 2026/27 and offers "
                        "registration for a 2027/28 opening alert. It refers to a December "
                        "course deadline for scholarship consideration but does not show "
                        "the exact calendar day on the closed page.",
                        "Canlı sayfa programın 2026/27 için kapalı olduğunu ve 2027/28 "
                        "açılış bildirimi kaydı sunduğunu belirtir. Burs değerlendirmesi "
                        "için Aralık ders son tarihine atıf yapar ancak kapalı sayfada "
                        "kesin takvim gününü göstermez.",
                    ),
                }
            ],
            "deadline_notes": bi(
                "Do not infer or reuse an exact date. Verify the 2027/28 deadline when "
                "the next cycle opens.",
                "Kesin tarih çıkarımı yapmayın veya eski tarihi yeniden kullanmayın. "
                "Bir sonraki dönem açıldığında 2027/28 son tarihini doğrulayın.",
            ),
        }
    )

    source_profile = row.setdefault("source_profile", {})
    source_profile.update(
        {
            "official_program_page": COURSE_URL,
            "official_admission_page": COURSE_URL,
            "official_curriculum_page": COURSE_URL,
            "official_tuition_page": COURSE_URL,
            "official_scholarship_page": COURSE_URL,
            "last_verified": "2026-08-14",
        }
    )
    confidence = source_profile.setdefault("field_confidence", {})
    confidence.update(
        {
            "program_basic_info": "high",
            "program": "high",
            "language": "medium",
            "admission": "high",
            "non_eu_eligibility": "high",
            "tuition": "high",
            "scholarship": "high",
            "curriculum": "high",
            "deadline": "high",
            "deadlines": "high",
            "application_timeline_profile": "medium",
            "living_profile": "high",
            "housing": "high",
        }
    )
    source_profile["needs_verification"] = True

    course_sources = [
        source
        for source in source_profile.setdefault("source_log", [])
        if source.get("url") == COURSE_URL
    ]
    if not course_sources:
        raise RuntimeError("Oxford course source entries were not found")
    for source in course_sources:
        source.update(
            {
                "access_status": "ok",
                "last_checked": "2026-08-14",
                "confidence": "high",
                "notes": bi(
                    "Live official 2026/27 course page was opened and checked directly "
                    "for the fields mapped in this source entry.",
                    "Canlı resmî 2026/27 ders sayfası, bu kaynak kaydında eşlenen alanlar "
                    "için doğrudan açılıp kontrol edildi.",
                ),
            }
        )

    quality = audit_record(row)
    quality["audited_at"] = "2026-08-14"
    row["data_quality"] = quality

    qc = row.setdefault("quality_control", {})
    qc.update(
        {
            "qc_status": "needs_revision",
            "checked_at": "2026-08-14",
            "failed_canary_tests": [],
            "remaining_verification_tasks": [
                bi(
                    "Verify the exact 2027/28 application and funding deadline when the "
                    "next cycle opens; the closed 2026/27 page no longer displays a day.",
                    "Bir sonraki dönem açıldığında kesin 2027/28 başvuru ve finansman "
                    "son tarihini doğrulayın; kapalı 2026/27 sayfası günü artık göstermiyor.",
                )
            ],
            "qc_notes": bi(
                "All currently published decision fields are tied to the live official "
                "course page. The record remains partial because the next-cycle exact "
                "deadline is not yet published and the teaching-language inference keeps "
                "a regulatory-exception caveat.",
                "Şu anda yayımlanan tüm karar alanları canlı resmî ders sayfasına bağlıdır. "
                "Bir sonraki dönemin kesin son tarihi henüz yayımlanmadığı ve eğitim dili "
                "çıkarımı düzenleyici istisna kaydını koruduğu için kayıt kısmi kalır.",
            ),
        }
    )

    DATA_PATH.write_text(
        json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
