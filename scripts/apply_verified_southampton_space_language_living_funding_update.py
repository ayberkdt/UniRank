"""Apply verified 2026/27 Southampton Space Systems Engineering MSc data."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from unirank.core.integrity import audit_record


DATA_PATH = ROOT / "data_base" / "ingiltere.json"
RECORD_ID = "university-of-southampton"
CHECKED = "2026-08-14"
COURSE_URL = "https://www.southampton.ac.uk/courses/space-systems-engineering-masters-msc"
SCHOLARSHIP_URL = (
    "https://www.southampton.ac.uk/study/fees-funding/scholarships/"
    "excellence-scholarship"
)
HOUSING_URL = "https://www.southampton.ac.uk/student-life/accommodation/fees-contracts"
GUARANTEE_URL = "https://www.southampton.ac.uk/student-life/accommodation/guarantee"
LIVING_URL = (
    "https://www.southampton.ac.uk/student-life/support-money/student-living-costs"
)
RESEARCH_URL = "https://www.southampton.ac.uk/research/groups/astronautics-group"


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
    language = row.setdefault("language_profile", {})
    language.update(
        {
            "teaching_language": ["English"],
            "teaching_languages": ["English"],
            "english_required": True,
            "english_level_required": "programme_specific",
            "minimum_scores": {
                "ielts_academic": {
                    "overall": 6.5,
                    "reading": 6.0,
                    "writing": 6.0,
                    "speaking": 6.0,
                    "listening": 6.0,
                }
            },
            "pre_sessional_route_available": True,
            "language_risk": "medium",
            "verification_notes": bi(
                "The live course page gives an IELTS 6.5 overall/6.0 per-component "
                "requirement and an English pre-sessional route. English is stored as "
                "the operational study language with medium confidence because the page "
                "does not display a separately labelled language-of-instruction field.",
                "Canlı ders sayfası IELTS için toplam 6,5 ve her bileşende 6,0 şartı ile "
                "İngilizce hazırlık yolunu yayımlar. Sayfa ayrıca etiketlenmiş bir eğitim "
                "dili alanı göstermediği için İngilizce, fiilî öğrenim dili olarak orta "
                "güvenle saklanır.",
            ),
        }
    )

    eligibility = row.setdefault("eligibility_profile", {})
    eligibility.update(
        {
            "eligible_for_non_eu": True,
            "required_previous_degree": (
                "UK 2:1 in aeronautics and astronautics, or a 2:1 in mechanical "
                "engineering, applied mathematics, physics or physical sciences with "
                "good grades in advanced mathematics, computing (Python or MATLAB), "
                "and classical physics/mechanics or equivalent"
            ),
            "accepted_backgrounds": [
                "Aeronautics and astronautics",
                "Mechanical engineering with the specified module background",
                "Applied mathematics with the specified module background",
                "Physics with the specified module background",
                "Physical sciences with the specified module background",
            ],
            "required_documents": [
                "Personal statement",
                "First-degree qualification paperwork",
                "IELTS evidence if the applicant is a non-native English speaker",
            ],
            "references_required": False,
            "decision_target_after_complete_application": "6 weeks",
            "gre": {
                "policy": "not_listed_in_checked_official_required_documents",
                "test_type": "GRE",
                "minimum_scores": {},
                "recommended_scores": {},
                "validity_rule": "",
                "waiver_rules": [],
                "source_ids": [COURSE_URL],
            },
            "verification_notes": bi(
                "The course accepts overseas applicants and links country-specific "
                "qualification equivalencies. Final academic equivalence and applicants "
                "using significant professional experience remain individual review "
                "decisions. GRE is not listed in the checked required documents; this is "
                "not phrased as a universal University-wide prohibition.",
                "Ders yurtdışı adayları kabul eder ve ülkeye özgü denklikleri bağlar. "
                "Nihai akademik denklik ile önemli mesleki deneyim kullanan adaylar bireysel "
                "incelemeye tabidir. GRE kontrol edilen gerekli belgeler arasında "
                "listelenmez; bu, üniversite genelinde evrensel bir yasak olarak sunulmaz.",
            ),
        }
    )

    cost = row.setdefault("cost_profile", {})
    cost.update(
        {
            "academic_year": "2026/2027",
            "tuition_gbp_full_programme": 35000,
            "tuition_gbp_per_year": 35000,
            "international_tuition_deposit_gbp": 2000,
            "application_assessment_fee_gbp": 0,
            "tuition_non_eu_full_program": {
                "amount": 35000,
                "currency": "GBP",
                "basis": "one_year_programme",
                "academic_year": "2026/2027",
            },
            "verification_notes": bi(
                "The official 2026/27 course page publishes GBP 35,000 for EU and "
                "international students, a GBP 2,000 international tuition deposit and "
                "no application assessment fee for postgraduate courses starting in "
                "2026. Tuition covers teaching and examinations, not living costs.",
                "Resmî 2026/27 ders sayfası AB ve uluslararası öğrenciler için 35.000 GBP "
                "ücret, 2.000 GBP uluslararası öğrenim depozitosu ve 2026'da başlayan "
                "lisansüstü dersler için sıfır başvuru değerlendirme ücreti yayımlar. "
                "Öğrenim ücreti eğitim ve sınavları kapsar; yaşam giderlerini kapsamaz.",
            ),
        }
    )

    scholarship = row.setdefault("scholarship_profile", {})
    scholarship.update(
        {
            "regional_scholarship_available": True,
            "regional_scholarship_name": "Global Excellence Scholarship",
            "merit_scholarships": ["Global Excellence Scholarship"],
            "tuition_waivers": ["GBP 3,000 first-year tuition reduction"],
            "non_eu_eligible": True,
            "scholarship_deadline": "2026-01-15",
            "scholarship_application_url": SCHOLARSHIP_URL,
            "application_mode": "automatic",
            "automatic_consideration": True,
            "separate_application_required": False,
            "current_cycle_status": "awarded_closed",
            "opportunities": [
                {
                    "name": "Global Excellence Scholarship",
                    "academic_year": "2026/2027",
                    "status": "awarded_closed",
                    "number_of_awards": 83,
                    "award": {
                        "amount": 3000,
                        "currency": "GBP",
                        "type": "first_year_tuition_reduction",
                    },
                    "application_mode": "automatic",
                    "separate_application_required": False,
                    "selection_mode": "first_83_eligible_after_conditions_met",
                    "deposit_condition_date": "2026-01-15",
                    "applicant_scope": (
                        "new_international_overseas-fee in-person full-time postgraduate "
                        "master's offer holders, subject to listed residency exclusions"
                    ),
                    "excluded_residency_routes": [
                        "China",
                        "Vietnam",
                        "Nigeria",
                        "India",
                        "Thailand",
                    ],
                    "exclusion_note": (
                        "The page directs these residencies to country-specific "
                        "Excellence Scholarships; it does not establish their terms for "
                        "this record."
                    ),
                    "source_url": SCHOLARSHIP_URL,
                }
            ],
            "funding_notes": bi(
                "The MSc is within the stated full-time, in-person postgraduate master's "
                "scope of the Global Excellence Scholarship. The 2026 awards have "
                "already been made; 2027 details are due in autumn 2026. The similarly "
                "named Engineering Global Talent Scholarship was checked and excluded "
                "because it is undergraduate-only.",
                "Bu MSc, Global Excellence bursunun belirtilen tam zamanlı ve yüz yüze "
                "lisansüstü yüksek lisans kapsamındadır. 2026 ödülleri verilmiştir; 2027 "
                "bilgileri 2026 sonbaharında beklenmektedir. Benzer adlı Engineering "
                "Global Talent Scholarship yalnızca lisans düzeyinde olduğu için kontrol "
                "edilmiş ve bu kayda alınmamıştır.",
            ),
            "verification_notes": bi(
                "Eligibility is conditional and the award is limited; it must not be "
                "shown as guaranteed funding for every non-EU applicant.",
                "Uygunluk koşulludur ve ödül sayısı sınırlıdır; her AB dışı aday için "
                "garanti finansman olarak gösterilmemelidir.",
            ),
        }
    )

    living = row.setdefault("living_profile", {})
    living.update(
        {
            "city_cost_level": "medium",
            "housing_difficulty": "conditional_guarantee_if_deadline_met",
            "living_risk": "medium",
            "housing_access": "guaranteed",
            "housing_application_separate": True,
            "housing_application_deadline": "2026-08-01",
            "housing_options": [
                "University-managed halls",
                "University-listed private partner halls",
                "Private rented accommodation",
            ],
            "housing_guarantee": {
                "available": True,
                "scope": "new_full_time_postgraduate_single_occupancy_room_offer",
                "application_deadline": "2026-08-01",
                "conditions": [
                    "New postgraduate student",
                    "Full-time course",
                    "Over 16 years of age",
                    "Apply for an accommodation contract of at least 38 weeks",
                    "Meet academic-offer conditions by 2026-08-31",
                    "Accept the accommodation offer by the portal deadline",
                ],
                "limitations": [
                    "No guarantee of a preferred hall, room type or price",
                    "The offered room may be outside the advertised residences",
                    "Late applicants are not covered",
                    "Accompanying family members are not guaranteed accommodation",
                ],
                "source_url": GUARANTEE_URL,
            },
            "official_rent_items": [
                {
                    "item": "all_published_single_occupancy_room_examples",
                    "amount_min": 118.50,
                    "amount_max": 281.12,
                    "currency": "GBP",
                    "period": "week",
                    "academic_year": "2026/2027",
                    "scope": (
                        "University and listed private-partner halls; varied room, "
                        "catering and 38/41/51-week contract types; couple flat excluded"
                    ),
                    "source_url": HOUSING_URL,
                },
                {
                    "item": "typical_university_halls_planning_range",
                    "amount_min": 155,
                    "amount_max": 236,
                    "currency": "GBP",
                    "period": "week",
                    "scope": "University-published typical-cost table",
                    "source_url": LIVING_URL,
                },
                {
                    "item": "typical_private_rent",
                    "amount": 115,
                    "currency": "GBP",
                    "period": "week",
                    "scope": "University-published typical-cost table; extras may apply",
                    "source_url": LIVING_URL,
                },
            ],
            "official_living_cost_items": [
                {"item": "utilities", "amount": 30, "currency": "GBP", "period": "week"},
                {"item": "wifi", "amount": 4, "currency": "GBP", "period": "week"},
                {"item": "phone", "amount": 10, "currency": "GBP", "period": "week"},
                {"item": "unilink_bus_pass", "amount": 9, "currency": "GBP", "period": "week"},
                {"item": "other_transport", "amount": 15, "currency": "GBP", "period": "week"},
                {"item": "food_shopping", "amount": 50, "currency": "GBP", "period": "week"},
                {"item": "social_and_wellbeing", "amount": 30, "currency": "GBP", "period": "week"},
                {"item": "clothing_and_personal_care", "amount": 20, "currency": "GBP", "period": "week"},
                {"item": "trips_and_opportunities", "amount": 25, "currency": "GBP", "period": "week"},
                {"item": "books_and_course_costs", "amount": 14, "currency": "GBP", "period": "week"},
                {"item": "laundry", "amount": 5, "currency": "GBP", "period": "week"},
            ],
            "official_living_cost_items_source_url": LIVING_URL,
            "university_halls_inclusions": [
                "gas_electricity_and_water",
                "wifi_and_high_speed_internet",
                "Unilink_bus_pass_for_university_owned_Southampton_halls",
                "laundry_with_some_private_hall_exceptions",
                "24_hour_support_and_security",
                "on_site_facilities",
                "contents_insurance_with_listed_exceptions",
            ],
            "typical_postgraduate_contract_length_weeks": 51,
            "housing_notes": bi(
                "Most postgraduates need a 51-week contract. The complete 2026/27 "
                "published single-room table spans GBP 118.50-281.12 per week, while the "
                "University's separate typical-cost table gives GBP 155-236 for halls. "
                "These are different scopes and are therefore stored separately.",
                "Lisansüstü öğrencilerin çoğu 51 haftalık sözleşmeye ihtiyaç duyar. "
                "Yayımlanmış tüm 2026/27 tek kişilik oda tablosu haftalık 118,50-281,12 "
                "GBP aralığındayken üniversitenin ayrı tipik maliyet tablosu yurtlar için "
                "155-236 GBP verir. Kapsamları farklı olduğu için ayrı saklanırlar.",
            ),
            "verification_notes": bi(
                "Weekly living items are the University's approximate planning examples, "
                "not mandatory spend. Utilities, Wi-Fi, Unilink and laundry are included "
                "in University-managed Southampton halls; private accommodation can add "
                "these costs. No EUR conversion or unsourced all-in total is stored.",
                "Haftalık yaşam kalemleri üniversitenin yaklaşık planlama örnekleridir; "
                "zorunlu harcama değildir. Üniversite yönetimindeki Southampton yurtlarında "
                "fatura, Wi-Fi, Unilink ve çamaşır maliyetleri dahildir; özel konutta bu "
                "giderler eklenebilir. EUR dönüşümü veya kaynaksız toplam saklanmaz.",
            ),
        }
    )
    for item in living["official_living_cost_items"]:
        item["source_url"] = LIVING_URL

    curriculum = row.setdefault("curriculum_profile", {})
    curriculum.update(
        {
            "mandatory_courses": [
                "Advanced Astronautics",
                "Concurrent Space Systems Design",
                "MSc Research Project",
                "Spacecraft Instrumentation",
                "Spacecraft Orbital Mechanics",
                "Spacecraft Propulsion",
                "Spacecraft Structural Design",
            ],
            "elective_courses": [
                "Applications of CFD",
                "Hypersonic & High Temperature Gas Dynamics",
                "Intelligent Mobile Robotics",
                "Principles of Photovoltaics, Fuel Cells and Batteries",
                "Turbulence",
            ],
            "mandatory_course_count": 7,
            "published_elective_option_count": 5,
            "elective_selection_count": None,
            "course_count_basis": "official_2026_2027_module_list",
            "thesis_required": True,
            "research_project_duration_months": 4,
            "taught_phase_duration_months": 8,
            "internship_required": None,
            "curriculum_url": COURSE_URL,
            "verification_notes": bi(
                "The official 2026/27 page lists seven mandatory modules and five "
                "published elective options but does not state the elective selection "
                "count in the captured page. Module availability may change. The final "
                "four months are a full-time research project with dissertation.",
                "Resmî 2026/27 sayfası yedi zorunlu modül ve yayımlanmış beş seçmeli "
                "seçenek listeler; ancak yakalanan sayfada kaç seçmeli alınacağı yazmaz. "
                "Modül erişimi değişebilir. Son dört ay tezli tam zamanlı araştırma "
                "projesidir.",
            ),
        }
    )

    row["category_profile"] = {
        "primary_categories": ["space_systems_engineering", "spacecraft_engineering"],
        "secondary_categories": [
            "orbital_mechanics",
            "spacecraft_propulsion",
            "spacecraft_structures",
            "spacecraft_instrumentation",
        ],
        "subcategories": [
            "autonomy_and_control",
            "computational_fluid_dynamics_optional",
            "hypersonics_optional",
            "space_power_optional",
        ],
        "normalized_tags": [
            "space_systems",
            "orbital_mechanics",
            "propulsion",
            "aerospace_structures",
            "spacecraft_instrumentation",
            "autonomy_control",
            "computational_fluid_dynamics",
            "hypersonics",
        ],
        "category_scores": {},
        "verification_notes": bi(
            "Tags map only to the verified 2026/27 mandatory or optional module list; "
            "optional subjects are labelled as such.",
            "Etiketler yalnızca doğrulanmış 2026/27 zorunlu veya seçmeli modül listesine "
            "dayanır; seçmeli konular bu şekilde işaretlenmiştir.",
        ),
    }

    research = row.setdefault("research_profile", {})
    research.update(
        {
            "department_research_areas": [
                "Space environment",
                "Remote sensing",
                "Spacecraft structures",
                "Space systems engineering",
                "Artificial intelligence, spacecraft autonomy and control",
            ],
            "labs": [
                "Spacecraft propulsion laboratory",
                "Autonomous systems test bed",
                "Shaker table",
            ],
            "research_centers": ["Astronautics Group"],
            "research_strength_summary": bi(
                "The Astronautics Group combines theoretical modelling and physical "
                "experimentation across space physics and spacecraft engineering, with "
                "computational and experimental facilities. The MSc includes a four-month "
                "individual research project.",
                "Astronautics Group uzay fiziği ve uzay aracı mühendisliğinde teorik "
                "modelleme ile fiziksel deneyi, hesaplamalı ve deneysel altyapıyla "
                "birleştirir. MSc dört aylık bireysel araştırma projesi içerir.",
            ),
            "research_strength_score": None,
            "research_sources": [RESEARCH_URL, COURSE_URL],
        }
    )

    ecosystem = row.setdefault("industry_ecosystem_profile", {})
    ecosystem.update(
        {
            "confirmed_partners": [
                {"name": "EADS Astrium", "relationship": "Astronautics Group industry partnership"},
                {"name": "Surrey Satellite Technology Ltd", "relationship": "Astronautics Group industry partnership"},
                {"name": "QinetiQ", "relationship": "Astronautics Group industry partnership"},
                {"name": "Thales Alenia Space", "relationship": "Astronautics Group industry partnership"},
                {"name": "Satellite Services Ltd", "relationship": "Astronautics Group industry partnership"},
            ],
            "research_institutes": ["Astronautics Group"],
            "sponsors_named_by_group": ["European Space Agency", "European Union", "EPSRC"],
            "programme_endorsement": "UK Space Agency endorsement stated by the University",
            "ecosystem_notes": bi(
                "The University explicitly names the listed Astronautics Group industry "
                "partnerships and sponsors. The course page separately states UK Space "
                "Agency endorsement and content drawn from professional courses run for "
                "ESA and the spacecraft industry. These exact relationship types are "
                "preserved and are not converted into placement guarantees.",
                "Üniversite listelenen Astronautics Group sanayi ortaklarını ve sponsorları "
                "açıkça adlandırır. Ders sayfası ayrıca UK Space Agency onayını ve ESA ile "
                "uzay aracı sanayisi için yürütülen profesyonel derslerden alınan içeriği "
                "belirtir. Bu ilişki türleri aynen korunur ve staj/iş garantisine çevrilmez.",
            ),
            "ecosystem_strength_score": None,
            "career_outcomes": {
                "average_professional_salary_gbp": 30000,
                "skilled_profession_or_further_study_percent": 95,
                "graduate_employment_rate_percent": 95,
                "measurement_timing": "15 months after course completion",
                "source_basis": "Graduate Outcomes Survey as presented on the course page",
                "caveat": (
                    "The live page does not expose the underlying cohort year or sample "
                    "size next to these figures."
                ),
                "source_url": COURSE_URL,
            },
        }
    )

    timeline = row.setdefault("application_timeline_profile", {})
    timeline.update(
        {
            "academic_year": "2026/2027",
            "intake_terms": ["September"],
            "non_eu_deadline": "2026-07-21",
            "eu_deadline": "2026-08-19",
            "international_latest_deadline_if_atas_not_required": "2026-08-19",
            "uk_deadline": "2026-09-02",
            "application_deadline": None,
            "timeline_risk": "high",
            "deadline_events": [
                {
                    "event": "programme_application_deadline",
                    "date": "2026-07-21",
                    "time": "12:00 UK time",
                    "date_status": "current",
                    "status_as_of_last_checked": "closed",
                    "applicant_scope": "international_nationals_requiring_ATAS",
                    "source_url": COURSE_URL,
                },
                {
                    "event": "programme_application_deadline",
                    "date": "2026-08-19",
                    "time": "12:00 UK time",
                    "date_status": "current",
                    "status_as_of_last_checked": "open",
                    "applicant_scope": "other_international_nationalities",
                    "source_url": COURSE_URL,
                },
                {
                    "event": "programme_application_deadline",
                    "date": "2026-09-02",
                    "time": "12:00 UK time",
                    "date_status": "current",
                    "status_as_of_last_checked": "open",
                    "applicant_scope": "UK",
                    "source_url": COURSE_URL,
                },
                {
                    "event": "postgraduate_accommodation_guarantee_application_deadline",
                    "date": "2026-08-01",
                    "date_status": "current",
                    "status_as_of_last_checked": "closed",
                    "applicant_scope": "eligible_new_full_time_postgraduates",
                    "source_url": GUARANTEE_URL,
                },
            ],
            "deadline_notes": bi(
                "The conservative non-EU date is 21 July because ATAS need depends on "
                "nationality; applicants not requiring ATAS had until 19 August. The "
                "University warns that the course can close earlier if filled. No date "
                "is estimated from a prior year.",
                "ATAS gereksinimi uyruğa bağlı olduğundan temkinli AB dışı tarih 21 "
                "Temmuz'dur; ATAS gerekmeyen uluslararası adayların son tarihi 19 "
                "Ağustos'tur. Üniversite kontenjan dolarsa dersin daha erken kapanabileceğini "
                "belirtir. Önceki yıldan tahmini tarih üretilmez.",
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
            "official_scholarship_page": SCHOLARSHIP_URL,
            "official_housing_page": HOUSING_URL,
            "official_cost_of_living_page": LIVING_URL,
            "official_department_page": RESEARCH_URL,
            "last_verified": CHECKED,
        }
    )
    confidence = source_profile.setdefault("field_confidence", {})
    confidence.update(
        {
            "program_basic_info": "high",
            "language": "medium",
            "admission": "high",
            "non_eu_eligibility": "high",
            "tuition": "high",
            "scholarship": "high",
            "curriculum": "high",
            "research_profile": "high",
            "industry_ecosystem_profile": "high",
            "application_timeline_profile": "high",
            "deadline": "high",
            "deadlines": "high",
            "living_profile": "high",
            "housing": "high",
        }
    )

    source_log = source_profile.setdefault("source_log", [])
    programme_sources = [source for source in source_log if source.get("url") == COURSE_URL]
    if not programme_sources:
        raise RuntimeError("Southampton programme sources are missing")
    for source in programme_sources:
        relevant = list(source.get("relevant_fields") or [])
        for field in [
            "program",
            "language",
            "admission",
            "non_eu_eligibility",
            "tuition",
            "curriculum",
            "deadline",
        ]:
            if field not in relevant:
                relevant.append(field)
        source["relevant_fields"] = relevant
        source["last_checked"] = CHECKED
        source["access_status"] = "ok"
        source["notes"] = bi(
            "Live official 2026/27 course page checked directly for the mapped fields, "
            "including module counts, application documents, fees and deadlines.",
            "Canlı resmî 2026/27 ders sayfası modül sayıları, başvuru belgeleri, ücretler "
            "ve tarihler dâhil eşlenen alanlar için doğrudan kontrol edildi.",
        )

    upsert_source(
        source_log,
        {
            "url": SCHOLARSHIP_URL,
            "title": "University of Southampton Global Excellence Scholarship",
            "source_type": "official_scholarship_page",
            "access_status": "ok",
            "last_checked": CHECKED,
            "relevant_fields": ["scholarship", "funding"],
            "confidence": "high",
            "notes": bi(
                "Official page gives the 2026 award count, GBP 3,000 reduction, eligible "
                "master's scope, automatic mode, deposit condition and closed status.",
                "Resmî sayfa 2026 ödül sayısını, 3.000 GBP indirimi, uygun yüksek lisans "
                "kapsamını, otomatik yöntemi, depozito koşulunu ve kapanmış durumu verir.",
            ),
        },
    )
    upsert_source(
        source_log,
        {
            "url": HOUSING_URL,
            "title": "University of Southampton accommodation fees and contracts 2026/27",
            "source_type": "official_housing_page",
            "access_status": "ok",
            "last_checked": CHECKED,
            "relevant_fields": ["housing", "living"],
            "confidence": "high",
            "notes": bi(
                "Official table gives room prices, contract lengths, payment dates and "
                "fee inclusions; private-partner rooms are retained with their scope.",
                "Resmî tablo oda fiyatlarını, sözleşme sürelerini, ödeme tarihlerini ve "
                "ücrete dâhil kalemleri verir; özel ortak yurtları kendi kapsamıyla tutulur.",
            ),
        },
    )
    upsert_source(
        source_log,
        {
            "url": GUARANTEE_URL,
            "title": "University of Southampton accommodation guarantee 2026",
            "source_type": "official_housing_page",
            "access_status": "ok",
            "last_checked": CHECKED,
            "relevant_fields": ["housing", "deadline"],
            "confidence": "high",
            "notes": bi(
                "Official guarantee page gives the postgraduate deadline, eligibility "
                "conditions and limitations of the guaranteed room offer.",
                "Resmî garanti sayfası lisansüstü son tarihini, uygunluk koşullarını ve "
                "garanti edilen oda teklifinin sınırlarını verir.",
            ),
        },
    )
    upsert_source(
        source_log,
        {
            "url": LIVING_URL,
            "title": "University of Southampton student living costs",
            "source_type": "official_cost_of_living_page",
            "access_status": "ok",
            "last_checked": CHECKED,
            "relevant_fields": ["living", "housing"],
            "confidence": "high",
            "notes": bi(
                "University planning page publishes approximate weekly housing and "
                "non-housing expense items and identifies costs included in managed halls.",
                "Üniversitenin planlama sayfası yaklaşık haftalık konut ve konut dışı "
                "giderleri yayımlar ve yönetilen yurtlara dâhil maliyetleri belirtir.",
            ),
        },
    )
    upsert_source(
        source_log,
        {
            "url": RESEARCH_URL,
            "title": "University of Southampton Astronautics Group",
            "source_type": "official_department_page",
            "access_status": "ok",
            "last_checked": CHECKED,
            "relevant_fields": ["research", "research_profile", "labs", "industry"],
            "confidence": "high",
            "notes": bi(
                "Official group page lists research areas, industry partnerships, sponsors, "
                "facilities context, people, projects and publications.",
                "Resmî grup sayfası araştırma alanlarını, sanayi ortaklarını, sponsorları, "
                "altyapı bağlamını, kişileri, projeleri ve yayınları listeler.",
            ),
        },
    )

    decision = row.setdefault("decision_summary", {})
    decision.update(
        {
            "main_strengths": [
                bi(
                    "Direct space-systems curriculum with seven current mandatory modules, "
                    "a four-month research project and verified spacecraft facilities.",
                    "Yedi güncel zorunlu modül, dört aylık araştırma projesi ve doğrulanmış "
                    "uzay aracı altyapısıyla doğrudan uzay sistemleri müfredatı.",
                ),
                bi(
                    "The Astronautics Group publishes relevant research areas and named "
                    "space-industry partnerships; the course is stated to be endorsed by "
                    "the UK Space Agency.",
                    "Astronautics Group ilgili araştırma alanlarını ve adlandırılmış uzay "
                    "sanayisi ortaklarını yayımlar; dersin UK Space Agency tarafından "
                    "onaylandığı belirtilir.",
                ),
                bi(
                    "New full-time postgraduates can receive a single-room accommodation "
                    "offer guarantee when all published conditions and the deadline are met.",
                    "Yeni tam zamanlı lisansüstüler yayımlanmış tüm koşulları ve son tarihi "
                    "karşılarsa tek kişilik oda teklifi garantisi alabilir.",
                ),
            ],
            "main_risks": [
                bi(
                    "The GBP 35,000 tuition is high and the GBP 3,000 Global Excellence "
                    "award is limited, conditional and already allocated for 2026.",
                    "35.000 GBP öğrenim ücreti yüksektir; 3.000 GBP Global Excellence ödülü "
                    "sınırlı, koşullu ve 2026 için zaten tahsis edilmiştir.",
                ),
                bi(
                    "ATAS-dependent applicants had an earlier 21 July deadline; the course "
                    "can close early, so the later international date is not safe for all.",
                    "ATAS'a tabi adayların 21 Temmuz gibi daha erken bir son tarihi vardır; "
                    "ders erken kapanabildiğinden sonraki uluslararası tarih herkes için "
                    "güvenli değildir.",
                ),
                bi(
                    "The 2026 postgraduate accommodation-guarantee deadline has passed as "
                    "of the verification date; late applications are not guaranteed.",
                    "Doğrulama tarihi itibarıyla 2026 lisansüstü yurt garantisi son tarihi "
                    "geçmiştir; geç başvurular garanti kapsamında değildir.",
                ),
            ],
            "best_for": [
                bi(
                    "Applicants targeting spacecraft systems, orbital mechanics, propulsion, "
                    "structures or instrumentation with a substantial research project.",
                    "Önemli bir araştırma projesiyle uzay aracı sistemleri, yörünge mekaniği, "
                    "itki, yapılar veya enstrümantasyon hedefleyen adaylar.",
                )
            ],
            "not_ideal_for": [
                bi(
                    "Applicants needing a currently open guaranteed scholarship or those "
                    "who cannot meet the advanced mathematics, computing and mechanics "
                    "background requirements.",
                    "Hâlen açık garanti burs gereken veya ileri matematik, programlama ve "
                    "mekanik altyapı koşullarını karşılamayan adaylar.",
                )
            ],
        }
    )

    quality = audit_record(row)
    quality["audited_at"] = CHECKED
    row["data_quality"] = quality
    source_profile["needs_verification"] = quality["status"] != "verified"

    qc = row.setdefault("quality_control", {})
    qc.update(
        {
            "qc_status": "needs_revision" if quality["status"] != "verified" else "passed",
            "checked_at": CHECKED,
            "failed_canary_tests": [],
            "remaining_verification_tasks": [
                bi(
                    "Check the scholarship page again when Southampton publishes 2027 "
                    "entry details in autumn 2026.",
                    "Southampton 2027 giriş bilgilerini 2026 sonbaharında yayımladığında "
                    "burs sayfasını yeniden kontrol edin.",
                ),
                bi(
                    "Replace the medium-confidence operational English evidence with a "
                    "current specification explicitly labelling the instruction language "
                    "if one is published.",
                    "Yayımlanırsa orta güvenli fiilî İngilizce kanıtını, eğitim dilini açıkça "
                    "etiketleyen güncel bir spesifikasyonla değiştirin.",
                ),
            ],
            "qc_notes": bi(
                "All decision-critical evidence groups have checked official sources. "
                "The record remains partial because teaching language is operationally "
                "rather than explicitly labelled and the next scholarship cycle is not "
                "yet published.",
                "Tüm karar-kritik kanıt gruplarında kontrol edilmiş resmî kaynak vardır. "
                "Eğitim dili açık etiket yerine fiilî kanıtla desteklendiği ve sonraki burs "
                "döngüsü henüz yayımlanmadığı için kayıt kısmi kalır.",
            ),
        }
    )

    DATA_PATH.write_text(
        json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
