"""Apply verified 2026/27 Leeds Aerospace Engineering MSc decision data."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from unirank.core.integrity import audit_record


DATA_PATH = ROOT / "data_base" / "ingiltere.json"
RECORD_ID = "university-of-leeds"
CHECKED = "2026-08-14"

COURSE_URL = "https://courses.leeds.ac.uk/g600/aerospace-engineering-msc"
APPLY_URL = "https://www.leeds.ac.uk/study/doc/apply-masters-courses"
DEPOSIT_URL = (
    "https://www.leeds.ac.uk/masters-fees/doc/"
    "tuition-fee-deposits-masters-applicants"
)
EXCELLENCE_URL = (
    "https://www.leeds.ac.uk/masters-scholarships-bursaries/doc/"
    "international-excellence-scholarships"
)
REGIONAL_URL = (
    "https://www.leeds.ac.uk/masters-scholarships-bursaries/doc/"
    "international-regional-scholarships-2026"
)
SCHOOL_SCHOLARSHIP_URL = (
    "https://eps.leeds.ac.uk/mechanical-engineering/dir/scholarships"
)
HOUSING_URL = "https://www.leeds.ac.uk/masters-offer/doc/offer-accommodation"
HOUSING_COST_URL = "https://accommodation.leeds.ac.uk/compare-residences/"
LIVING_URL = "https://www.leeds.ac.uk/masters-fees/doc/living-expenses"
RESEARCH_URL = (
    "https://eps.leeds.ac.uk/mechanical-engineering-research-innovation"
)
FACILITIES_URL = (
    "https://eps.leeds.ac.uk/mechanical-engineering-undergraduate/doc/"
    "learning-teaching-facilities-2"
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
            "english_level_required": "IELTS 6.5 overall with 6.0 in every component",
            "minimum_scores": {
                "ielts_academic": {"overall": 6.5, "each_component": 6.0}
            },
            "accepted_alternatives": "See the University's current English-language equivalents policy; exact alternative scores were not copied into this programme record.",
            "pre_sessional_routes": [
                "Language for Engineering (6 weeks)",
                "Language for Science: Engineering (10 weeks)",
                "Longer postgraduate pre-sessional English routes",
                "Six- and ten-week online pre-sessionals",
            ],
            "language_risk": "medium",
            "verification_notes": bi(
                "The course page publishes an IELTS threshold and English pre-sessional routes. "
                "English is recorded as the operational teaching medium from the live English "
                "course specification and its English-entry regime; the page does not expose a "
                "separate explicit 'language of instruction' label, so confidence is medium.",
                "Ders sayfası IELTS eşiğini ve İngilizce hazırlık yollarını yayımlar. İngilizce, "
                "canlı İngilizce ders tanımı ve İngilizce giriş rejiminden fiilî öğretim dili "
                "olarak kaydedilmiştir; sayfa ayrıca açık bir 'öğretim dili' etiketi sunmadığı "
                "için güven düzeyi ortadır.",
            ),
        }
    )

    row["eligibility_profile"].update(
        {
            "eligible_for_non_eu": True,
            "required_previous_degree": (
                "Normally a 2:1 honours bachelor's in Aeronautical, Aerospace, Mechanical, "
                "Civil or General Engineering"
            ),
            "accepted_backgrounds": [
                "Aeronautical Engineering",
                "Aerospace Engineering",
                "Mechanical Engineering",
                "Civil Engineering",
                "General Engineering",
            ],
            "prerequisite_modules": [
                "Advanced mathematics",
                "Strength of materials",
                "Dynamics",
                "Fluid mechanics",
            ],
            "alternative_entry_routes": [
                "A 2:2 honours degree in a listed subject plus at least three years of relevant experience, considered case by case",
                "Relevant professional qualifications and experience, considered case by case",
            ],
            "required_documents": [
                "official_degree_certificate",
                "official_transcripts_with_unit_grades_and_grading_scale",
                "certified_english_translations_if_documents_are_not_in_english",
                "english_language_evidence_if_already_held",
                "previous_UK_student_visa_documents_if_applicable",
            ],
            "conditional_additional_documents": [
                "Detailed module information if prerequisite coverage is unclear on the transcript",
                "CV, references or evidence of professional qualifications only where the course/admissions team requests them",
            ],
            "application_portal": "University of Leeds applicant portal",
            "decision_time_guidance": "Three to five weeks when all necessary documents have been received",
            "admission_risk": "medium",
            "gre": {
                "policy": "not_listed_in_checked_official_required_documents",
                "test_type": "GRE General",
                "minimum_scores": {},
                "recommended_scores": {},
                "validity_rule": "",
                "waiver_rules": [],
                "source_ids": [APPLY_URL, COURSE_URL],
                "verification_notes": bi(
                    "GRE does not appear in the checked 2026 University baseline document list "
                    "or the programme-specific entry requirements. This is a bounded 'not "
                    "listed' finding, not a universal institutional prohibition.",
                    "GRE, kontrol edilen 2026 Üniversite temel belge listesinde veya programa "
                    "özgü giriş koşullarında yer almaz. Bu, kurum çapında yasak değil, sınırları "
                    "belirli bir 'listelenmedi' bulgusudur.",
                ),
            },
            "atas": {
                "may_be_required": True,
                "cah_code": "CAH10-01-04",
                "descriptor": "Aeronautical and Aerospace Engineering",
                "supervisor_contact": "Dr Eric Lo",
                "verification_notes": bi(
                    "The course page says ATAS may be required depending on nationality and "
                    "publishes the CAH code and contact; this is not a claim that every "
                    "international applicant needs ATAS.",
                    "Ders sayfası uyruğa bağlı olarak ATAS gerekebileceğini söyler ve CAH kodu "
                    "ile irtibat kişisini yayımlar; bu, her uluslararası adayın ATAS'a ihtiyaç "
                    "duyduğu anlamına gelmez.",
                ),
            },
            "verification_notes": bi(
                "Overseas qualifications are accepted through equivalency review. Academic "
                "fit depends on both degree field and the four named prerequisite areas; the "
                "University may request detailed module evidence.",
                "Yurtdışı diplomalar denklik incelemesiyle kabul edilir. Akademik uyum hem "
                "diploma alanına hem de belirtilen dört önkoşul alanına bağlıdır; Üniversite "
                "ayrıntılı ders kanıtı isteyebilir.",
            ),
        }
    )

    row["cost_profile"].update(
        {
            "academic_year": "2026/2027",
            "tuition_non_eu_full_program": {
                "amount": 33500,
                "currency": "GBP",
                "basis": "one_year_programme",
                "academic_year": "2026/2027",
            },
            "tuition_gbp_full_programme": 33500,
            "tuition_gbp_per_year": 33500,
            "student_visa_tuition_deposit_gbp": 2000,
            "deposit_required_for": "taught postgraduate applicants requiring a Student visa",
            "deposit_request_stage": (
                "after academic and English conditions are met and an unconditional offer is accepted"
            ),
            "deposit_deadline": "2026-08-21",
            "deposit_exemptions": [
                "Full funding from a University-recognised sponsor with final evidence",
                "US Federal Loan recipient",
                "Specified Leeds pre-sessional routes",
                "Applicant who does not require a CAS or Student visa",
                "Online or distance-learning applicant who does not require a CAS",
            ],
            "deposit_refund_policy": "typically_non_refundable_with_limited_published_exceptions",
            "deposit_notes": bi(
                "The GBP 2,000 payment is a CAS-related tuition deposit, deducted from tuition. "
                "It should be paid only after Leeds requests it. An unsuccessful funding "
                "application is not by itself a refund ground.",
                "2.000 GBP ödeme, öğrenim ücretinden düşülen CAS bağlantılı öğrenim "
                "depozitosudur. Yalnız Leeds talep ettikten sonra ödenmelidir. Finansman "
                "başvurusunun başarısız olması tek başına iade gerekçesi değildir.",
            ),
            "source_notes": bi(
                "The programme publishes GBP 33,500 total international tuition for 2026/27. "
                "No EUR conversion is stored. The separate deposit policy is applicant- and "
                "visa-status-specific.",
                "Program 2026/27 için toplam 33.500 GBP uluslararası öğrenim ücreti yayımlar. "
                "EUR dönüşümü saklanmaz. Ayrı depozito politikası adaya ve vize statüsüne özgüdür.",
            ),
        }
    )

    row["scholarship_profile"].update(
        {
            "regional_scholarship_available": True,
            "regional_scholarship_name": "International Masters Regional Scholarship 2026",
            "non_eu_eligible": True,
            "application_mode": "mixed",
            "automatic_consideration": True,
            "separate_application_required": True,
            "current_cycle_status": "mixed_automatic_route_available_and_competitive_route_closed",
            "scholarship_deadline": "2026-05-29",
            "scholarship_application_url": EXCELLENCE_URL,
            "opportunities": [
                {
                    "name": "International Masters Regional Scholarship 2026",
                    "academic_year": "2026/2027",
                    "status": "available_for_eligible_offer_holders",
                    "award": {
                        "amount": 6000,
                        "currency": "GBP",
                        "type": "first_year_tuition_fee_reduction",
                    },
                    "application_mode": "automatic",
                    "separate_application_required": False,
                    "turkey_passport_eligible": True,
                    "eligibility_summary": bi(
                        "Eligible passport countries include Turkey and the United States. "
                        "The applicant must be an international fee payer, self- or partly "
                        "funded, and hold a conditional or unconditional September 2026 "
                        "Masters offer. Aerospace Engineering MSc is not among the exclusions.",
                        "Uygun pasaport ülkeleri Türkiye ve ABD'yi içerir. Aday uluslararası "
                        "ücret statüsünde, öz veya kısmi finansmanlı olmalı ve Eylül 2026 için "
                        "koşullu ya da koşulsuz yüksek lisans teklifi almalıdır. Aerospace "
                        "Engineering MSc istisnalar arasında değildir.",
                    ),
                    "source_url": REGIONAL_URL,
                },
                {
                    "name": "International Excellence Scholarships 2026",
                    "academic_year": "2026/2027",
                    "status": "closed",
                    "award_amounts_gbp": [3000, 6000, 16000],
                    "number_of_scholarships": 500,
                    "award_type": "first_year_tuition_fee_reduction",
                    "application_mode": "separate_competitive_application",
                    "separate_application_required": True,
                    "application_deadline": "2026-05-29",
                    "outcome_by": "2026-06-26",
                    "eligibility_summary": bi(
                        "International fee status, an eligible September 2026 taught Masters "
                        "offer, self or partial funding, at least a 2:1-equivalent academic "
                        "record, and strong professional or personal evidence were required.",
                        "Uluslararası ücret statüsü, uygun Eylül 2026 örgün yüksek lisans "
                        "teklifi, öz veya kısmi finansman, en az 2:1 dengi akademik başarı ve "
                        "güçlü mesleki ya da kişisel kanıt gerekiyordu.",
                    ),
                    "source_url": EXCELLENCE_URL,
                },
            ],
            "funding_notes": bi(
                "For a Turkish passport holder who meets the published conditions, the GBP "
                "6,000 Regional award is automatic. The Excellence award required a separate "
                "competitive application and its 2026 deadline has passed. The two may be "
                "combined subject to the published 100% tuition cap and other award terms.",
                "Yayımlanan koşulları karşılayan Türkiye pasaportu sahibi için 6.000 GBP "
                "Regional ödül otomatiktir. Excellence ödülü ayrı ve rekabetçi başvuru "
                "gerektiriyordu; 2026 son tarihi geçmiştir. İki ödül, yayımlanan %100 öğrenim "
                "ücreti üst sınırı ve diğer ödül koşullarına bağlı olarak birleştirilebilir.",
            ),
            "verification_notes": bi(
                "Both routes are University-wide 2026 schemes, but Mechanical Engineering's "
                "current scholarship directory lists them and neither scheme excludes this "
                "campus-taught MSc. Awards are tuition reductions, not living-cost cash.",
                "Her iki yol 2026 kurum çapı programıdır; ancak Mechanical Engineering'in "
                "güncel burs dizini bunları listeler ve hiçbir program bu kampüste yürütülen "
                "MSc'yi dışlamaz. Ödüller yaşam gideri nakdi değil öğrenim indirimi niteliğindedir.",
            ),
        }
    )

    row["living_profile"].update(
        {
            "city_cost_level": "medium_to_high",
            "housing_difficulty": "guarantee_deadline_passed_for_2026",
            "living_risk": "high",
            "housing_access": "guaranteed",
            "housing_application_separate": True,
            "housing_application_deadline": "2026-07-31",
            "housing_options": [
                "University self-catered postgraduate residence",
                "Private self-catered accommodation",
                "Family accommodation where available",
            ],
            "housing_guarantee": {
                "available": True,
                "scope": "single_University_accommodation_offer_for_eligible_new_single_international_postgraduates",
                "application_deadline": "2026-07-31",
                "status_as_of_last_checked": "deadline_passed",
                "conditions": [
                    "New international postgraduate student",
                    "Single accommodation required",
                    "Apply by 31 July for a September or October start",
                    "Restrictions on residence, fee status and level of study apply",
                ],
                "limitations": [
                    "The guarantee is an offer of single University accommodation, not a chosen residence or room type",
                    "UK postgraduate students are not guaranteed University accommodation",
                    "Applications after 31 July are assisted but not guaranteed",
                ],
                "source_url": HOUSING_URL,
            },
            "official_rent_items": [
                {
                    "item": "published_University_postgraduate_room_examples",
                    "amount_min": 125,
                    "amount_max": 221,
                    "currency": "GBP",
                    "period": "week",
                    "academic_year": "2026/2027",
                    "typical_contract_length_weeks": 51,
                    "scope": "PG-labelled University residence examples; provisional prices",
                    "source_url": HOUSING_COST_URL,
                },
                {
                    "item": "published_University_postgraduate_contract_totals",
                    "amount_min": 6357,
                    "amount_max": 11247,
                    "currency": "GBP",
                    "period": "contract",
                    "academic_year": "2026/2027",
                    "scope": "PG-labelled 51-week examples; provisional prices",
                    "source_url": HOUSING_COST_URL,
                },
            ],
            "living_cost_gbp_per_week_min": 199,
            "living_cost_gbp_per_week_max": 423,
            "living_cost_sample_year": 2025,
            "official_living_cost_items": [
                {"item": "estimated_total_budget", "amount_min": 199, "amount_max": 423, "currency": "GBP", "period": "week"},
                {"item": "University_accommodation_self_catered", "amount_min": 117, "amount_max": 265, "currency": "GBP", "period": "week"},
                {"item": "University_accommodation_catered", "amount_min": 205, "amount_max": 273, "currency": "GBP", "period": "week"},
                {"item": "private_accommodation_self_catered", "amount_min": 110, "amount_max": 300, "currency": "GBP", "period": "week"},
                {"item": "groceries_toiletries_and_cleaning", "amount_min": 31, "amount_max": 38, "currency": "GBP", "period": "week"},
                {"item": "household_bills_when_not_included", "amount_min": 14, "amount_max": 17, "currency": "GBP", "period": "week"},
                {"item": "personal_costs", "amount_min": 44, "amount_max": 68, "currency": "GBP", "period": "week"},
            ],
            "housing_notes": bi(
                "The 2026/27 comparison table labels University PG examples at GBP 125-221 "
                "per week and GBP 6,357-11,247 over the listed 51-week contracts. Prices are "
                "provisional and include energy, Wi-Fi, contents insurance and, except family "
                "housing, premium sports membership.",
                "2026/27 karşılaştırma tablosu Üniversite lisansüstü örneklerini haftalık "
                "125-221 GBP ve listelenen 51 haftalık sözleşmelerde 6.357-11.247 GBP olarak "
                "gösterir. Fiyatlar geçicidir; enerji, Wi-Fi, eşya sigortası ve aile konutu "
                "hariç premium spor üyeliğini içerir.",
            ),
            "verification_notes": bi(
                "The GBP 199-423 weekly total is the University's 2025 guideline for one "
                "student, excludes tuition, and varies by housing availability and lifestyle. "
                "It is neither a guaranteed future bill nor a visa-maintenance figure.",
                "Haftalık 199-423 GBP toplam, Üniversitenin tek öğrenci için 2025 rehberidir; "
                "öğrenim ücretini içermez ve konut bulunabilirliği ile yaşam tarzına göre "
                "değişir. Garanti gelecek fatura veya vize geçim tutarı değildir.",
            ),
        }
    )
    for item in row["living_profile"]["official_living_cost_items"]:
        item["source_url"] = LIVING_URL

    row["curriculum_profile"].update(
        {
            "tracks": ["student-tailored aerospace route through optional modules"],
            "specializations": [],
            "mandatory_courses": [
                "Advanced Aerodynamics (15 credits)",
                "Aerospace Structures (15 credits)",
                "Professional Project (60 credits)",
                "Team Design Project (15 credits)",
            ],
            "elective_courses": [
                "Computational Fluid Dynamics Analysis (15 credits)",
                "Engineering Computational Methods (15 credits)",
                "Fundamentals of Tribology (15 credits)",
                "Surface Engineering and Coatings (15 credits)",
                "Experimental Methods and Analysis (15 credits)",
                "Engineering Psychology and Human Factors (15 credits)",
                "Advanced Finite Element Analysis (15 credits)",
                "Aerospace Systems Engineering (15 credits)",
                "Rotary-wing Aircraft (15 credits)",
                "Advanced Manufacturing (15 credits)",
                "Design Optimisation (15 credits)",
                "Spacecraft Dynamics and Control (15 credits)",
            ],
            "mandatory_course_count": 4,
            "published_elective_option_count": 12,
            "published_compulsory_credits": 105,
            "exact_elective_selection_count": None,
            "research_project_required": True,
            "team_design_project_required": True,
            "thesis_required": None,
            "internship_required": None,
            "industry_linked_project_possible": True,
            "curriculum_url": COURSE_URL,
            "verification_notes": bi(
                "The live 2026 page publishes four compulsory components totalling 105 "
                "credits and 12 indicative 15-credit optional modules. It says choices depend "
                "on background but does not publish a reliable exact option count to take, so "
                "that count remains null. The required 60-credit Professional Project is not "
                "relabeled as a thesis without explicit wording.",
                "Canlı 2026 sayfası toplam 105 kredilik dört zorunlu bileşen ve 12 adet "
                "gösterge niteliğinde 15 kredilik seçmeli ders yayımlar. Seçimlerin geçmişe "
                "bağlı olduğunu söyler ancak alınacak kesin seçmeli sayısını güvenilir biçimde "
                "vermez; bu sayı null kalır. Zorunlu 60 kredilik Professional Project, açık "
                "ifade olmadan tez olarak yeniden etiketlenmez.",
            ),
        }
    )

    row["category_profile"].update(
        {
            "primary_categories": [
                "aerodynamics",
                "cfd",
                "structures",
                "space_systems",
            ],
            "secondary_categories": [
                "flight_mechanics",
                "stability_control",
                "wind_tunnel",
                "manufacturing",
            ],
            "subcategories": [
                "computational_fluid_dynamics",
                "finite_element_analysis",
                "aerospace_systems_engineering",
                "spacecraft_dynamics",
                "design_optimisation",
                "rotary_wing_aircraft",
            ],
            "normalized_tags": [
                "aerodynamics",
                "cfd",
                "structures",
                "space_systems",
                "flight_mechanics",
                "stability_control",
                "wind_tunnel",
                "manufacturing",
            ],
        }
    )

    row["research_profile"].update(
        {
            "department_research_areas": [
                "Engineering systems and design",
                "Thermofluids",
                "Surfaces and interfaces",
                "Aerospace engineering",
            ],
            "labs": [
                "Thermofluids Lab",
                "Wind tunnels",
                "Engine testbeds",
                "Prototyping workshops",
            ],
            "research_centers": [
                "Leeds Institute for Fluid Dynamics",
                "Robotics Leeds",
            ],
            "research_strength_summary": bi(
                "The School documents department-level strengths in thermofluids and design, "
                "links to the Leeds Institute for Fluid Dynamics, and teaching facilities "
                "including wind tunnels and engine testbeds. The MSc page says research feeds "
                "teaching and some projects are formally industry-linked; none of this "
                "guarantees a particular laboratory placement.",
                "School, termoakışkanlar ve tasarımda bölüm düzeyi güçlü alanları, Leeds "
                "Institute for Fluid Dynamics bağlantısını ve rüzgâr tünelleri ile motor test "
                "düzeneklerini içeren öğretim altyapısını belgeler. MSc sayfası araştırmanın "
                "öğretime aktarıldığını ve bazı projelerin resmen sanayi bağlantılı olduğunu "
                "söyler; bunların hiçbiri belirli bir laboratuvar yerini garanti etmez.",
            ),
            "research_strength_score": None,
            "research_sources": [RESEARCH_URL, FACILITIES_URL, COURSE_URL],
        }
    )

    row["industry_ecosystem_profile"].update(
        {
            "nearby_companies": [],
            "confirmed_partners": [],
            "research_institutes": ["Leeds Institute for Fluid Dynamics"],
            "ecosystem_notes": bi(
                "The School's Industrial Advisory Board contributes to course relevance, "
                "talks and project work. A proportion of projects are formally linked to "
                "industry and may include time at a collaborator site. Company names shown as "
                "sector examples or graduate employers are not converted into partnerships.",
                "School'un Industrial Advisory Board'u dersin güncelliğine, konuşmalara ve "
                "proje çalışmalarına katkı verir. Projelerin bir bölümü resmen sanayi "
                "bağlantılıdır ve işbirlikçi sahasında zaman içerebilir. Sektör örneği veya "
                "mezun işvereni olarak gösterilen şirket adları ortaklığa dönüştürülmez.",
            ),
            "ecosystem_strength_score": None,
        }
    )

    row["application_timeline_profile"].update(
        {
            "academic_year": "2026/2027",
            "intake_terms": ["September"],
            "application_opened": "2025-10-01",
            "non_eu_deadline": "2026-07-31",
            "eu_deadline": "2026-07-31",
            "home_deadline": "2026-09-11",
            "scholarship_deadline": "2026-05-29",
            "timeline_risk": "high",
            "deadline_events": [
                {"event": "applications_opened", "date": "2025-10-01", "status_as_of_last_checked": "past", "source_url": APPLY_URL},
                {"event": "International_Excellence_scholarship_deadline", "date": "2026-05-29", "status_as_of_last_checked": "closed", "source_url": EXCELLENCE_URL},
                {"event": "international_programme_application_deadline", "date": "2026-07-31", "status_as_of_last_checked": "published_deadline_passed", "source_url": COURSE_URL},
                {"event": "international_postgraduate_housing_guarantee_deadline", "date": "2026-07-31", "status_as_of_last_checked": "closed", "source_url": HOUSING_URL},
                {"event": "international_offer_conditions_deadline", "date": "2026-08-07", "status_as_of_last_checked": "passed", "source_url": APPLY_URL},
                {"event": "Student_visa_tuition_deposit_or_exemption_deadline", "date": "2026-08-21", "status_as_of_last_checked": "not_yet_passed", "source_url": DEPOSIT_URL},
                {"event": "UK_programme_application_deadline", "date": "2026-09-11", "status_as_of_last_checked": "not_yet_passed", "source_url": COURSE_URL},
            ],
            "deadline_notes": bi(
                "The international programme deadline, Excellence scholarship deadline, "
                "offer-condition deadline and housing-guarantee deadline had all passed when "
                "checked. The automatic Regional scholarship has no separate application "
                "deadline, but still requires an eligible September 2026 offer.",
                "Kontrol tarihinde uluslararası program, Excellence bursu, teklif koşulu ve "
                "yurt garantisi son tarihleri geçmişti. Otomatik Regional bursun ayrı başvuru "
                "son tarihi yoktur; yine de uygun Eylül 2026 teklifini gerektirir.",
            ),
        }
    )

    profile = row["source_profile"]
    profile.update(
        {
            "official_admission_page": APPLY_URL,
            "official_curriculum_page": COURSE_URL,
            "official_tuition_page": COURSE_URL,
            "official_scholarship_page": EXCELLENCE_URL,
            "official_language_policy_page": COURSE_URL,
            "official_housing_page": HOUSING_URL,
            "official_cost_of_living_page": LIVING_URL,
            "official_department_page": RESEARCH_URL,
            "last_verified": CHECKED,
        }
    )
    profile["field_confidence"].update(
        {
            "program_basic_info": "high",
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
            "research": "high",
            "industry": "medium",
        }
    )

    log = profile["source_log"]
    log[:] = [
        source
        for source in log
        if not (
            source.get("url") == COURSE_URL
            and source.get("source_type")
            in {
                "official_admission_page",
                "official_curriculum_page",
                "official_scholarship_page",
            }
        )
    ]
    course_sources = [source for source in log if source.get("url") == COURSE_URL]
    if not course_sources:
        raise RuntimeError("Leeds programme sources are missing")
    for source in course_sources:
        source["access_status"] = "ok"
        source["last_checked"] = CHECKED
        relevant = list(source.get("relevant_fields") or [])
        for field in [
            "program",
            "language",
            "admission",
            "non_eu_eligibility",
            "tuition",
            "curriculum",
            "deadline",
            "industry",
        ]:
            if field not in relevant:
                relevant.append(field)
        source["relevant_fields"] = relevant
        source["confidence"] = "high"
        source["notes"] = bi(
            "Live official 2026 course page checked for programme status, academic entry, "
            "IELTS, modules, fees, deadlines, ATAS and scoped industry engagement.",
            "Canlı resmî 2026 ders sayfası program durumu, akademik giriş, IELTS, dersler, "
            "ücretler, son tarihler, ATAS ve kapsamı belirli sanayi etkileşimi için kontrol edildi.",
        )

    sources = [
        (APPLY_URL, "University of Leeds Masters application guidance 2026", "official_admission_page", ["admission", "documents", "deadline"], "Required baseline documents, portal, decision timing and offer-condition date."),
        (DEPOSIT_URL, "University of Leeds Masters tuition-deposit guidance 2026/27", "official_tuition_page", ["tuition", "deposit", "deadline", "visa"], "Visa-linked deposit amount, trigger, exemptions, deadline and refund limits."),
        (EXCELLENCE_URL, "University of Leeds International Excellence Scholarships 2026", "official_scholarship_page", ["scholarship", "funding", "deadline"], "Competitive award values, eligibility, exclusions and closed deadline."),
        (REGIONAL_URL, "University of Leeds International Masters Regional Scholarships 2026", "official_scholarship_page", ["scholarship", "funding"], "Automatic GBP 6,000 award, country list including Turkey, eligibility and exclusions."),
        (SCHOOL_SCHOLARSHIP_URL, "University of Leeds Mechanical Engineering scholarships 2026/27", "official_scholarship_page", ["scholarship", "funding"], "School directory confirms both international Masters routes for the relevant School."),
        (HOUSING_URL, "University of Leeds postgraduate accommodation", "official_housing_page", ["housing", "deadline"], "Conditional international postgraduate guarantee and late-application limitation."),
        (HOUSING_COST_URL, "University of Leeds residence comparison 2026/27", "official_housing_page", ["housing", "living"], "PG-labelled provisional weekly and contract prices plus included services."),
        (LIVING_URL, "University of Leeds living costs and budgeting", "official_cost_of_living_page", ["living", "housing"], "Official 2025 weekly guideline and component ranges for a single student."),
        (RESEARCH_URL, "University of Leeds Mechanical Engineering research and innovation", "official_department_page", ["research", "facilities"], "Department research themes, institute links and external-collaboration facility scope."),
        (FACILITIES_URL, "University of Leeds Mechanical Engineering facilities", "official_department_page", ["research", "facilities", "curriculum"], "Thermofluids Lab, wind tunnels, engine testbeds and prototyping workshops."),
    ]
    for url, title, source_type, fields, note in sources:
        upsert_source(
            log,
            {
                "url": url,
                "title": title,
                "source_type": source_type,
                "access_status": "ok",
                "last_checked": CHECKED,
                "relevant_fields": fields,
                "confidence": "high",
                "notes": bi(
                    note,
                    "Resmî kaynak belirtilen alanlar ve kapsam sınırları için doğrudan kontrol edildi.",
                ),
            },
        )

    row["decision_summary"].update(
        {
            "main_strengths": [
                bi(
                    "A dedicated aerospace MSc with explicit aerodynamics, structures, CFD, "
                    "finite elements, systems engineering and spacecraft dynamics/control "
                    "options, plus individual and team projects.",
                    "Aerodinamik, yapılar, HAD, sonlu elemanlar, sistem mühendisliği ve uzay "
                    "aracı dinamiği/kontrolü seçenekleri ile bireysel ve takım projeleri sunan "
                    "özel bir havacılık-uzay MSc programıdır.",
                ),
                bi(
                    "For an eligible Turkish passport holder, the verified GBP 6,000 Regional "
                    "tuition reduction is automatic rather than a separate scholarship form.",
                    "Uygun Türkiye pasaportu sahibi için doğrulanmış 6.000 GBP Regional öğrenim "
                    "indirimi ayrı burs formu yerine otomatiktir.",
                ),
                bi(
                    "Eligible new single international postgraduates had a conditional offer "
                    "of University accommodation, and the official residence table exposes a "
                    "wide PG price range.",
                    "Uygun yeni ve tek gelen uluslararası lisansüstüler için koşullu Üniversite "
                    "konaklama teklifi vardı; resmî yurt tablosu geniş bir lisansüstü fiyat "
                    "aralığını görünür kılar.",
                ),
            ],
            "main_risks": [
                bi(
                    "The international programme, Excellence scholarship, offer-condition and "
                    "housing-guarantee deadlines have passed for the checked 2026 cycle.",
                    "Kontrol edilen 2026 döngüsünde uluslararası program, Excellence bursu, "
                    "teklif koşulu ve yurt garantisi son tarihleri geçmiştir.",
                ),
                bi(
                    "GBP 33,500 tuition and the University's GBP 199-423 weekly living-cost "
                    "guideline create a high gross funding requirement even after a GBP 6,000 "
                    "Regional discount.",
                    "33.500 GBP öğrenim ücreti ve Üniversitenin haftalık 199-423 GBP yaşam "
                    "rehberi, 6.000 GBP Regional indirim sonrasında dahi yüksek brüt finansman "
                    "gereksinimi yaratır.",
                ),
                bi(
                    "Space content is elective and limited to systems engineering and "
                    "spacecraft dynamics/control on the published list; this is broader "
                    "aerospace rather than a deeply space-specialist degree.",
                    "Yayımlanan listede uzay içeriği seçmelidir ve sistem mühendisliği ile uzay "
                    "aracı dinamiği/kontrolüyle sınırlıdır; bu, derin uzay uzmanlığından ziyade "
                    "geniş havacılık-uzay derecesidir.",
                ),
            ],
            "best_for": [
                bi(
                    "Engineering graduates seeking aircraft-focused aerodynamics, structures "
                    "and computation with some optional spacecraft-control exposure.",
                    "Bir miktar seçmeli uzay aracı kontrolü deneyimiyle uçak odaklı aerodinamik, "
                    "yapılar ve hesaplama arayan mühendislik mezunları.",
                )
            ],
            "not_ideal_for": [
                bi(
                    "Late 2026 international applicants, students needing guaranteed low cost, "
                    "or candidates seeking a propulsion-heavy or fully space-systems curriculum.",
                    "Geç kalan 2026 uluslararası adayları, garantili düşük maliyet arayanlar veya "
                    "itki ağırlıklı ya da tamamen uzay sistemleri müfredatı isteyen adaylar.",
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
                    "Replace all 2026 programme, scholarship, deposit and accommodation dates "
                    "when Leeds publishes the next intake; never roll these dates forward.",
                    "Leeds sonraki giriş dönemini yayımladığında tüm 2026 program, burs, "
                    "depozito ve konaklama tarihlerini değiştirin; bu tarihleri ileri taşımayın.",
                ),
                bi(
                    "Confirm the exact number of optional modules each student must take if a "
                    "current catalogue rule becomes explicit.",
                    "Güncel katalog kuralı açık hâle gelirse her öğrencinin alması gereken kesin "
                    "seçmeli ders sayısını doğrulayın.",
                ),
            ],
            "qc_notes": bi(
                "All current decision-critical groups have checked official sources. The record "
                "keeps medium confidence for teaching language because the live page provides "
                "operational English evidence rather than a separate explicit language label.",
                "Tüm güncel karar-kritik gruplarda kontrol edilmiş resmî kaynak vardır. Canlı "
                "sayfa ayrı açık dil etiketi yerine fiilî İngilizce kanıt sunduğu için öğretim "
                "dili güveni orta tutulur.",
            ),
        }
    )

    DATA_PATH.write_text(
        json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
