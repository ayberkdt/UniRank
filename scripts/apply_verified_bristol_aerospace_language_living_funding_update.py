"""Apply verified 2026/27 Bristol Aerospace Engineering MSc decision data."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from unirank.core.integrity import audit_record


DATA_PATH = ROOT / "data_base" / "ingiltere.json"
RECORD_ID = "university-of-bristol"
CHECKED = "2026-08-14"
COURSE_URL = "https://www.bristol.ac.uk/study/postgraduate/taught/msc-aerospace-engineering/"
ADMISSION_PDF = (
    "https://www.bristol.ac.uk/study/media/postgraduate/admissions-statements/2026/"
    "msc-aerospace-engineering.pdf"
)
LANGUAGE_URL = "https://www.bristol.ac.uk/study/language-requirements/profile-e/"
SCHOLARSHIP_URL = "https://www.bristol.ac.uk/international/fees-finance/scholarships/"
HOUSING_COST_URL = "https://www.bristol.ac.uk/accommodation/about/costs/cost-by-residence/"
HOUSING_GUARANTEE_URL = "https://www.bristol.ac.uk/accommodation/apply/guarantee/"
LIVING_URL = "https://www.bristol.ac.uk/students/support/finances/advice/living-expenses/"
CATALOGUE_URL = (
    "https://www.bris.ac.uk/unit-programme-catalogue/RouteStructure.jsa?"
    "ayrCode=26%2F27&byCohort=N&programmeCode=4CADE004T"
)


def bi(en: str, tr: str) -> dict[str, str]:
    return {"en": en, "tr": tr}


def upsert_source(source_log: list[dict], source: dict) -> None:
    matches = [
        item
        for item in source_log
        if item.get("url") == source["url"]
        and item.get("source_type") == source["source_type"]
    ]
    if len(matches) > 1:
        raise RuntimeError(
            f"Duplicate source key: {source['url']} / {source['source_type']}"
        )
    if matches:
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
    row["language_profile"].update(
        {
            "teaching_language": ["English"],
            "teaching_languages": ["English"],
            "english_required": True,
            "english_level_required": "Bristol Profile E",
            "minimum_scores": {
                "ielts_academic": {"overall": 6.5, "each_skill": 6.0},
                "toefl_ibt_up_to_2026_01_20": {
                    "overall": 88,
                    "reading": 20,
                    "listening": 19,
                    "speaking": 22,
                    "writing": 22,
                },
                "toefl_ibt_from_2026_01_21": {"overall": 4.5, "each_skill": 4.5},
                "pte_academic": {"overall": 67, "each_skill": 64},
                "languagecert_academic": {"overall": 70, "each_skill": 65},
                "trinity_ise": {"overall": 96, "other_skills": 88},
                "oxford_international_ellt": {"overall": 7, "each_skill": 6},
            },
            "cambridge_c2_proficiency": "Grade C or Level C1",
            "cambridge_c1_advanced": "Grade B, or Grade C with no skill below 168",
            "test_validity": "no more than two years before programme start",
            "component_combination_policy": "all component scores in one test sitting",
            "ielts_one_skill_retake_accepted": True,
            "waiver_rules": [
                "Listed English-speaking nationality, subject to University discretion",
                "Eligible English-speaking-country study within the seven-year rule",
                "Qualifying English-medium university study evidenced by an official MOI letter",
                "ECCTIS English Language Proficiency Statement at B2 or above",
                "Specified recent professional English-use route after English-medium study",
            ],
            "language_risk": "medium",
            "verification_notes": bi(
                "The programme requires Profile E and the official profile page publishes "
                "test scores, validity and exemption routes. English is retained as the "
                "operational teaching language with medium confidence because the live "
                "programme page does not show a separate language-of-instruction label.",
                "Program Profile E ister; resmî profil sayfası sınav puanlarını, geçerliliği "
                "ve muafiyet yollarını yayımlar. Canlı program sayfası ayrı bir eğitim dili "
                "etiketi göstermediği için İngilizce fiilî eğitim dili olarak orta güvenle "
                "tutulur.",
            ),
        }
    )

    eligibility = row["eligibility_profile"]
    eligibility.update(
        {
            "eligible_for_non_eu": True,
            "required_previous_degree": (
                "Upper second-class honours degree or international equivalent in "
                "Aerospace Engineering or Mechanical Engineering; another Engineering "
                "degree can qualify with Aerodynamics, Aeronautics and Aerospace "
                "Structures units at 40% or international equivalent in each"
            ),
            "accepted_backgrounds": [
                "Aerospace Engineering",
                "Mechanical Engineering",
                "Other Engineering with the three specified aerospace subject units",
            ],
            "required_documents": [
                "Degree certificate(s) from first and subsequent degrees",
                "Academic transcript(s) from first and subsequent degrees",
                "English-language certificate or other accepted evidence",
            ],
            "optional_documents": [
                "Personal statement",
                "Curriculum vitae",
                "Extenuating-circumstances form where relevant",
            ],
            "personal_statement_policy": "optional_for_routine_assessment",
            "interview_policy": "not_part_of_selection_process",
            "atas_required": "required_for_non_exempt_nationalities_subject_to_UK_immigration_control",
            "gre": {
                "policy": "not_listed_in_checked_official_required_documents",
                "test_type": "GRE",
                "minimum_scores": {},
                "recommended_scores": {},
                "validity_rule": "",
                "waiver_rules": [],
                "source_ids": [ADMISSION_PDF],
            },
            "verification_notes": bi(
                "The programme-specific admissions statement lists the complete required "
                "and optional document groups and does not list GRE or references. This is "
                "stored as a programme-document finding, not a University-wide ban.",
                "Programa özgü kabul bildirimi gerekli ve isteğe bağlı belge gruplarını "
                "listeler; GRE veya referans listelemez. Bu, üniversite genelinde yasak "
                "değil programa ait belge bulgusu olarak saklanır.",
            ),
        }
    )

    row["cost_profile"].update(
        {
            "academic_year": "2026/2027",
            "tuition_basis": "official_published_foreign_currency",
            "tuition_gbp_per_year": 34900,
            "tuition_gbp_full_programme": 34900,
            "tuition_non_eu_full_program": {
                "amount": 34900,
                "currency": "GBP",
                "basis": "one_year_full_time_programme",
                "academic_year": "2026/2027",
            },
            "international_deposit_policy": {
                "typical_deposit_gbp": 2000,
                "increased_deposit_for_certain_regions": {
                    "amount_gbp": 15000,
                    "alternative": "50% of first-year tuition",
                },
                "fully_sponsored_exemption": True,
                "exact_amount_source": "official_offer_letter",
            },
            "verification_notes": bi(
                "The programme page publishes GBP 34,900 for one year in 2026/27. Most "
                "self-funded international taught-postgraduate offer holders pay a GBP "
                "2,000 deposit, but certain regions face GBP 15,000 or 50% of first-year "
                "tuition; only the offer letter establishes the applicant's exact amount.",
                "Program sayfası 2026/27'de bir yıl için 34.900 GBP yayımlar. Kendi "
                "finansmanını sağlayan uluslararası lisansüstü dersli program teklif "
                "sahiplerinin çoğu 2.000 GBP depozito öder; belirli bölgelerde 15.000 GBP "
                "veya ilk yıl ücretinin %50'si uygulanır. Adayın kesin tutarını yalnızca "
                "teklif mektubu belirler.",
            ),
        }
    )

    row["scholarship_profile"].update(
        {
            "regional_scholarship_available": True,
            "regional_scholarship_name": "Think Big Postgraduate Scholarships",
            "merit_scholarships": [
                "Think Big Postgraduate Scholarship",
                "Think Big about Science and Engineering Postgraduate Scholarship",
                "Think Big Career Accelerator",
            ],
            "tuition_waivers": ["GBP 6,500, GBP 13,000 or GBP 26,000 first-year tuition discount"],
            "non_eu_eligible": True,
            "scholarship_deadline": "2026-04-10T10:00:00+01:00",
            "scholarship_application_url": SCHOLARSHIP_URL,
            "application_mode": "separate",
            "automatic_consideration": False,
            "separate_application_required": True,
            "current_cycle_status": "closed",
            "opportunities": [
                {
                    "name": "Think Big Postgraduate Scholarship",
                    "academic_year": "2026/2027",
                    "status": "closed",
                    "award_amounts_gbp": [6500, 13000, 26000],
                    "award_type": "first_year_tuition_discount",
                    "application_mode": "separate_single_scholarship_form",
                    "deadline": "2026-04-10T10:00:00+01:00",
                    "eligibility": (
                        "Overseas-fee applicant to a full-time, in-person master's, with "
                        "an offer by 24 April 2026 and University entry requirements met"
                    ),
                    "source_url": SCHOLARSHIP_URL,
                },
                {
                    "name": "Think Big about Science and Engineering Postgraduate Scholarship",
                    "academic_year": "2026/2027",
                    "status": "closed",
                    "award_amounts_gbp": [6500],
                    "award_type": "first_year_tuition_discount",
                    "application_mode": "same_separate_Think_Big_form",
                    "course_scope": "eligible taught master's in Faculty of Science and Engineering",
                    "source_url": SCHOLARSHIP_URL,
                },
                {
                    "name": "Think Big Career Accelerator",
                    "academic_year": "2026/2027",
                    "status": "closed",
                    "award_amounts_gbp": [3000],
                    "award_type": "tuition_discount_plus_year_long_career_programme",
                    "application_mode": "same_separate_Think_Big_form",
                    "source_url": SCHOLARSHIP_URL,
                },
            ],
            "funding_notes": bi(
                "A single separate Think Big form considered applicants for every scheme "
                "whose criteria they met. The 2026 application closed on 10 April at "
                "10:00 UK time. Awards are competitive discounts, not guaranteed cash, "
                "and standard postgraduate tuition awards apply for the first year only.",
                "Tek bir ayrı Think Big formu, adayları koşullarını karşıladıkları tüm "
                "programlar için değerlendirdi. 2026 başvurusu 10 Nisan saat 10.00 UK "
                "zamanında kapandı. Ödüller garanti nakit değil rekabetçi indirimlerdir; "
                "standart lisansüstü öğrenim ödülleri yalnızca ilk yıl içindir.",
            ),
        }
    )

    row["living_profile"].update(
        {
            "city_cost_level": "high",
            "housing_difficulty": "guarantee_deadline_passed_for_2026",
            "living_risk": "high",
            "housing_access": "guaranteed",
            "housing_application_separate": True,
            "housing_application_deadline": "2026-06-30",
            "housing_options": [
                "University postgraduate accommodation",
                "University-listed residences managed by external companies",
                "Private rented accommodation",
            ],
            "housing_guarantee": {
                "available": True,
                "scope": "new_first_year_overseas_fee_postgraduate_room_offer",
                "application_deadline": "2026-06-30",
                "status_as_of_last_checked": "deadline_passed",
                "conditions": [
                    "Apply by 30 June 2026",
                    "Firmly accept the study offer",
                    "Be a new full-time student studying at Bristol for the first time",
                    "Accept the accommodation offer by its deadline",
                    "Be unaccompanied by a partner or dependent family members",
                ],
                "limitations": [
                    "Room may be outside advertised residences",
                    "Home-fee postgraduates are not guaranteed",
                    "Late overseas postgraduate applicants are not guaranteed",
                ],
                "source_url": HOUSING_GUARANTEE_URL,
            },
            "official_rent_items": [
                {
                    "item": "published_postgraduate_room_examples_including_twin_rooms",
                    "amount_min": 147.00,
                    "amount_max": 339.50,
                    "currency": "GBP",
                    "period": "week",
                    "academic_year": "2026/2027",
                    "contract_lengths_weeks": [38, 50, 51],
                    "scope": "postgraduate-labelled rooms; couple/family flats excluded",
                    "source_url": HOUSING_COST_URL,
                },
                {
                    "item": "published_postgraduate_contract_totals",
                    "amount_min": 5985.00,
                    "amount_max": 17314.50,
                    "currency": "GBP",
                    "period": "contract",
                    "academic_year": "2026/2027",
                    "scope": "single-occupancy postgraduate-labelled examples; food excluded",
                    "source_url": HOUSING_COST_URL,
                },
            ],
            "monthly_living_cost_gbp_per_month_estimated": 1862,
            "average_room_rent_gbp_per_month_estimated": 871.47,
            "official_living_cost_items": [
                {"item": "postgraduate_average_total_spend", "amount": 1862, "currency": "GBP", "period": "month"},
                {"item": "rent_or_mortgage", "amount": 871.47, "currency": "GBP", "period": "month"},
                {"item": "electricity_gas_and_water", "amount": 74.83, "currency": "GBP", "period": "month"},
                {"item": "internet_landline_and_mobile", "amount": 24.99, "currency": "GBP", "period": "month"},
                {"item": "household_shop", "amount": 271.86, "currency": "GBP", "period": "month"},
                {"item": "public_transport", "amount": 34.68, "currency": "GBP", "period": "month"},
                {"item": "private_transport_monthly", "amount": 21.90, "currency": "GBP", "period": "month"},
                {"item": "medical_expenses", "amount": 21.83, "currency": "GBP", "period": "month"},
                {"item": "meals_out", "amount": 52.87, "currency": "GBP", "period": "month"},
                {"item": "clothes_and_personal_grooming", "amount": 45.63, "currency": "GBP", "period": "month"},
                {"item": "gym_fitness_and_wellness", "amount": 28.98, "currency": "GBP", "period": "month"},
            ],
            "living_cost_sample_academic_year": "2025/2026",
            "housing_notes": bi(
                "The official 2026/27 residence table spans GBP 147-339.50 per week for "
                "postgraduate-labelled rooms; food is excluded and contract lengths vary. "
                "The overseas-postgraduate guarantee deadline had already passed when "
                "checked, so the guarantee is not a current fallback for a late applicant.",
                "Resmî 2026/27 yurt tablosunda lisansüstü etiketli odalar haftalık "
                "147-339,50 GBP aralığındadır; yemek hariçtir ve sözleşme süreleri değişir. "
                "Kontrol tarihinde yurtdışı lisansüstü yurt garantisi son tarihi geçmişti; "
                "bu nedenle garanti geç aday için güncel bir çözüm değildir.",
            ),
            "verification_notes": bi(
                "The GBP 1,862 monthly figure is an official University survey average "
                "reported by undergraduate and postgraduate students in 2025/26, not a "
                "minimum visa budget or guaranteed future spend. Individual costs vary.",
                "Aylık 1.862 GBP, 2025/26'da lisans ve lisansüstü öğrencilerden alınan "
                "üniversitenin resmî anket ortalamasıdır; asgari vize bütçesi veya garanti "
                "gelecek harcama değildir. Bireysel maliyetler değişir.",
            ),
        }
    )
    for item in row["living_profile"]["official_living_cost_items"]:
        item["source_url"] = LIVING_URL

    row["curriculum_profile"].update(
        {
            "tracks": ["student-tailored aerospace pathway through unit choices"],
            "mandatory_courses": [
                "Group multidisciplinary aircraft conceptual-design project",
                "Individual research project within a Bristol research team",
            ],
            "elective_courses": [
                "One foundational unit chosen in term 1",
                "Two advanced aerospace optional units chosen in term 1",
                "One final optional unit chosen in term 2",
            ],
            "planned_unit_selection_count": 6,
            "selection_count_breakdown": {
                "foundational_choice": 1,
                "advanced_optional_choices": 3,
                "group_design_project": 1,
                "individual_research_project": 1,
            },
            "thesis_required": True,
            "internship_required": None,
            "curriculum_url": CATALOGUE_URL,
            "verification_notes": bi(
                "The live programme page establishes six planned selections/components: "
                "one foundational choice, three optional choices, a group aircraft-design "
                "project and an individual research project. The dynamic catalogue did "
                "not expose a reliable captured list of unit titles, so titles are not "
                "invented.",
                "Canlı program sayfası altı planlı seçim/bileşen tanımlar: bir temel ders "
                "seçimi, üç seçmeli ders, grup uçak tasarım projesi ve bireysel araştırma "
                "projesi. Dinamik katalog güvenilir yakalanmış ders başlığı listesi "
                "sunmadığı için başlık uydurulmaz.",
            ),
        }
    )

    row["application_timeline_profile"].update(
        {
            "academic_year": "2026/2027",
            "non_eu_deadline": "2026-08-13",
            "eu_deadline": "2026-08-13",
            "home_deadline": "2026-09-10",
            "timeline_risk": "high",
            "deadline_events": [
                {
                    "event": "programme_application_deadline",
                    "date": "2026-08-13",
                    "date_status": "current",
                    "status_as_of_last_checked": "published_deadline_passed_portal_status_not_verified",
                    "applicant_scope": "overseas",
                    "source_url": COURSE_URL,
                },
                {
                    "event": "programme_application_deadline",
                    "date": "2026-09-10",
                    "date_status": "current",
                    "status_as_of_last_checked": "not_yet_passed",
                    "applicant_scope": "home",
                    "source_url": COURSE_URL,
                },
                {
                    "event": "Think_Big_scholarship_deadline",
                    "date": "2026-04-10",
                    "time": "10:00 UK time",
                    "date_status": "current",
                    "status_as_of_last_checked": "closed",
                    "applicant_scope": "eligible_overseas_fee_applicants",
                    "source_url": SCHOLARSHIP_URL,
                },
                {
                    "event": "postgraduate_accommodation_guarantee_deadline",
                    "date": "2026-06-30",
                    "date_status": "current",
                    "status_as_of_last_checked": "closed",
                    "applicant_scope": "eligible_new_overseas_fee_postgraduates",
                    "source_url": HOUSING_GUARANTEE_URL,
                },
            ],
            "deadline_notes": bi(
                "The published overseas deadline passed one day before verification. The "
                "visible apply control is not treated as proof that late overseas "
                "applications remain accepted. Bristol can also close high-demand "
                "programmes earlier than advertised.",
                "Yayımlanan yurtdışı son tarihi doğrulamadan bir gün önce geçti. Görünen "
                "başvuru düğmesi, geç yurtdışı başvuruların kabul edildiğinin kanıtı "
                "sayılmaz. Bristol yüksek talepli programları duyurulandan önce de "
                "kapatabilir.",
            ),
        }
    )

    profile = row["source_profile"]
    profile.update(
        {
            "official_admission_page": ADMISSION_PDF,
            "official_curriculum_page": COURSE_URL,
            "official_tuition_page": COURSE_URL,
            "official_scholarship_page": SCHOLARSHIP_URL,
            "official_language_policy_page": LANGUAGE_URL,
            "official_housing_page": HOUSING_COST_URL,
            "official_cost_of_living_page": LIVING_URL,
            "last_verified": CHECKED,
        }
    )
    profile["field_confidence"].update(
        {
            "language": "medium",
            "admission": "high",
            "non_eu_eligibility": "high",
            "tuition": "high",
            "scholarship": "high",
            "curriculum": "high",
            "application_timeline_profile": "high",
            "deadline": "high",
            "deadlines": "high",
            "living_profile": "high",
            "housing": "high",
        }
    )

    log = profile["source_log"]
    log[:] = [
        source
        for source in log
        if not (
            source.get("url") == COURSE_URL
            and source.get("source_type")
            in {"official_admission_page", "official_curriculum_page", "official_scholarship_page"}
        )
    ]
    course_sources = [source for source in log if source.get("url") == COURSE_URL]
    if not course_sources:
        raise RuntimeError("Bristol programme sources are missing")
    for source in course_sources:
        source["access_status"] = "ok"
        source["last_checked"] = CHECKED
        relevant = list(source.get("relevant_fields") or [])
        for field in ["program", "language", "admission", "non_eu_eligibility", "tuition", "curriculum", "deadline"]:
            if field not in relevant:
                relevant.append(field)
        source["relevant_fields"] = relevant
        source["notes"] = bi(
            "Live official 2026/27 course page checked for programme, academic entry, "
            "structure, tuition and deadline claims.",
            "Canlı resmî 2026/27 ders sayfası program, akademik giriş, yapı, ücret ve son "
            "tarih iddiaları için kontrol edildi.",
        )

    sources = [
        (ADMISSION_PDF, "Bristol Aerospace Engineering MSc admissions statement 2026", "official_admission_page", "pdf", ["admission", "non_eu_eligibility"], "Programme-specific PDF lists documents, selection, ATAS and conditional deposit rules."),
        (LANGUAGE_URL, "University of Bristol English Profile E", "official_university_policy_page", "ok", ["language"], "Official Profile E publishes current scores, validity, one-sitting and exemption rules."),
        (SCHOLARSHIP_URL, "University of Bristol international scholarships 2026", "official_scholarship_page", "ok", ["scholarship", "funding", "deadline"], "Official page gives Think Big scope, award values, single separate application and closed deadline."),
        (HOUSING_COST_URL, "University of Bristol accommodation costs by residence 2026/27", "official_housing_page", "ok", ["housing", "living"], "Official residence table publishes postgraduate room, contract and price examples."),
        (HOUSING_GUARANTEE_URL, "University of Bristol accommodation guarantee 2026", "official_housing_page", "ok", ["housing", "deadline"], "Official guarantee page gives overseas postgraduate scope, deadline, conditions and exclusions."),
        (LIVING_URL, "University of Bristol budgeting and living expenses", "official_cost_of_living_page", "ok", ["living", "housing"], "Official page publishes 2025/26 postgraduate survey averages and component spending."),
    ]
    for url, title, source_type, status, fields, note in sources:
        upsert_source(
            log,
            {
                "url": url,
                "title": title,
                "source_type": source_type,
                "access_status": status,
                "last_checked": CHECKED,
                "relevant_fields": fields,
                "confidence": "high",
                "notes": bi(note, "Resmî kaynak belirtilen alanlar ve kapsam sınırları için doğrudan kontrol edildi."),
            },
        )

    row["decision_summary"].update(
        {
            "main_strengths": [
                bi(
                    "Flexible advanced aerospace structure with three optional choices, "
                    "an industry-style group aircraft design and an individual research "
                    "project embedded in a Bristol research team.",
                    "Üç seçmeli ders, sanayi tarzı grup uçak tasarımı ve Bristol araştırma "
                    "ekibine gömülü bireysel araştırma projesiyle esnek ileri havacılık yapısı.",
                ),
                bi(
                    "Overseas-fee applicants had verified Think Big tuition-discount "
                    "routes and a conditional first-year accommodation guarantee.",
                    "Yurtdışı ücret statüsündeki adaylar için doğrulanmış Think Big öğrenim "
                    "indirimi yolları ve koşullu ilk yıl yurt garantisi vardı.",
                ),
            ],
            "main_risks": [
                bi(
                    "The overseas programme, scholarship and accommodation-guarantee "
                    "deadlines have all passed for the checked 2026 cycle.",
                    "Kontrol edilen 2026 döngüsünde yurtdışı program, burs ve yurt garantisi "
                    "son tarihlerinin tamamı geçmiştir.",
                ),
                bi(
                    "GBP 34,900 tuition plus a surveyed GBP 1,862 average monthly "
                    "postgraduate spend creates a high funding burden; Think Big was "
                    "competitive and not automatic.",
                    "34.900 GBP öğrenim ücreti ve ankette aylık ortalama 1.862 GBP lisansüstü "
                    "harcama yüksek finansman yükü yaratır; Think Big rekabetçi ve otomatik "
                    "değildi.",
                ),
                bi(
                    "Applicants from some regions can face a much larger tuition deposit "
                    "than the typical GBP 2,000; only the offer letter confirms it.",
                    "Bazı bölgelerden adaylar tipik 2.000 GBP'den çok daha yüksek öğrenim "
                    "depozitosuyla karşılaşabilir; bunu yalnızca teklif mektubu doğrular.",
                ),
            ],
            "best_for": [
                bi(
                    "Aerospace or mechanical engineering graduates seeking a flexible "
                    "aircraft-focused MSc with design and research components.",
                    "Tasarım ve araştırma bileşenli, esnek ve uçak odaklı MSc arayan "
                    "havacılık veya makine mühendisliği mezunları.",
                )
            ],
            "not_ideal_for": [
                bi(
                    "Late 2026 overseas applicants or students who need guaranteed current "
                    "funding and low living costs.",
                    "Geç kalan 2026 yurtdışı adayları veya güncel garanti finansman ile düşük "
                    "yaşam maliyetine ihtiyaç duyan öğrenciler.",
                )
            ],
        }
    )

    quality = audit_record(row)
    quality["audited_at"] = CHECKED
    row["data_quality"] = quality
    profile["needs_verification"] = quality["status"] != "verified"
    row["quality_control"].update(
        {
            "qc_status": "needs_revision" if quality["status"] != "verified" else "passed",
            "checked_at": CHECKED,
            "failed_canary_tests": [],
            "remaining_verification_tasks": [
                bi(
                    "Check the next intake's programme, scholarship and accommodation "
                    "deadlines when Bristol publishes them; do not reuse 2026 dates.",
                    "Bristol yayımladığında sonraki girişin program, burs ve yurt son "
                    "tarihlerini kontrol edin; 2026 tarihlerini yeniden kullanmayın.",
                ),
                bi(
                    "Capture the dynamic 2026/27 catalogue's exact unit-title list if it "
                    "becomes reliably accessible.",
                    "Dinamik 2026/27 kataloğun kesin ders başlığı listesini güvenilir şekilde "
                    "erişilebilir olursa yakalayın.",
                ),
            ],
            "qc_notes": bi(
                "Every decision-critical field has checked official evidence. The record "
                "remains partial because language is operational rather than explicitly "
                "labelled and the exact dynamic unit-title list was not captured.",
                "Her karar-kritik alanda kontrol edilmiş resmî kanıt vardır. Eğitim dili "
                "açık etiketten ziyade fiilî kanıta dayandığı ve dinamik kesin ders başlığı "
                "listesi yakalanmadığı için kayıt kısmi kalır.",
            ),
        }
    )

    DATA_PATH.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
