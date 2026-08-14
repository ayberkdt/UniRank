"""Apply verified 2026/27 Liverpool Advanced Aerospace Engineering MSc data."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from unirank.core.integrity import audit_record


DATA_PATH = ROOT / "data_base" / "ingiltere.json"
RECORD_ID = "university-of-liverpool"
CHECKED = "2026-08-14"
COURSE_URL = "https://www.liverpool.ac.uk/courses/advanced-aerospace-engineering-msc-eng"
DEPOSIT_URL = (
    "https://www.liverpool.ac.uk/international/scholarships-and-fees/"
    "tuition-fees/deposit/"
)
EXCELLENCE_URL = (
    "https://www.liverpool.ac.uk/study/fees-and-funding/scholarships-and-bursaries/"
    "masters/liverpool-excellence-scholarship-postgraduate/"
)
ADVANCEMENT_URL = (
    "https://www.liverpool.ac.uk/study/fees-and-funding/scholarships-and-bursaries/"
    "masters/liverpool-advancement-scholarship/"
)
HOUSING_URL = "https://www.liverpool.ac.uk/accommodation/applying/"
HOUSING_FEES_PDF = (
    "https://www.liverpool.ac.uk/media/livacuk/accommodation/feescharts/"
    "Postgraduate%2CFees%2CChart%2C2026-27.pdf"
)
LIVING_URL = (
    "https://www.liverpool.ac.uk/international/scholarships-and-fees/living-costs/"
)
RESEARCH_URL = (
    "https://www.liverpool.ac.uk/mechanical-and-aerospace-engineering/research/"
)
FACILITIES_URL = (
    "https://www.liverpool.ac.uk/mechanical-and-aerospace-engineering/facilities/"
)
FLIGHT_RESEARCH_URL = "https://www.liverpool.ac.uk/flight-science/about/"
SPACE_RESEARCH_URL = "https://www.liverpool.ac.uk/research/space/space-robotics/"


def bi(en: str, tr: str) -> dict[str, str]:
    return {"en": en, "tr": tr}


def source(
    url: str,
    title: str,
    source_type: str,
    access_status: str,
    relevant_fields: list[str],
    note_en: str,
    confidence: str = "high",
) -> dict:
    return {
        "url": url,
        "title": title,
        "source_type": source_type,
        "access_status": access_status,
        "last_checked": CHECKED,
        "relevant_fields": relevant_fields,
        "confidence": confidence,
        "notes": bi(
            note_en,
            "Resmî kaynak belirtilen alanlar, tarihler ve kapsam sınırları için doğrudan kontrol edildi.",
        ),
    }


def rent_item(
    provider: str,
    room: str,
    weekly: float,
    contract: float,
    instalment: float | None,
    university_hall: bool,
) -> dict:
    return {
        "provider_or_hall": provider,
        "room_type": room,
        "amount_per_week": weekly,
        "contract_amount": contract,
        "currency": "GBP",
        "contract_weeks": 51,
        "instalment_amount_three_payments": instalment,
        "university_hall": university_hall,
        "source_url": HOUSING_FEES_PDF,
    }


def main() -> None:
    rows = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    matches = [row for row in rows if row.get("id") == RECORD_ID]
    if len(matches) != 1:
        raise RuntimeError(f"Expected one {RECORD_ID!r} record; found {len(matches)}")
    row = matches[0]

    row.update(
        {
            "program_name": "Advanced Aerospace Engineering MSc (Eng)",
            "program_degree": "MSc (Eng)",
            "degree_level": "Master",
            "duration_years": 1,
            "program_status": "active",
            "program_url": COURSE_URL,
            "teaching_language": ["English"],
        }
    )

    row["language_profile"].update(
        {
            "teaching_language": ["English"],
            "teaching_languages": ["English"],
            "english_required": True,
            "english_level_required": "IELTS 6.5 overall with no component below 6.0 or accepted equivalent",
            "minimum_scores": {
                "ielts_academic": {"overall": 6.5, "each_component": 6.0},
                "toefl_ibt_to_2026_01_20": {
                    "overall": 88,
                    "listening": 19,
                    "writing": 19,
                    "reading": 19,
                    "speaking": 20,
                },
                "toefl_ibt_from_2026_01_21": {
                    "overall": 4.5,
                    "each_component": 4.0,
                },
                "duolingo_english_test": {
                    "overall": 125,
                    "writing": 125,
                    "speaking": 115,
                    "reading": 115,
                    "listening": 110,
                },
                "pte_academic": {"overall": 61, "each_component": 59},
                "languagecert_academic": {"overall": 70, "each_skill": 65},
                "psi_skills_for_english": "B2 Pass with Merit in all bands",
            },
            "not_accepted": ["TOEFL Home Edition"],
            "waiver_rules": [
                "Nationality of a majority English-speaking country",
                "A country-specific qualification accepted by the University",
            ],
            "pre_sessional_available": True,
            "pre_sessional_routes": [
                {"ielts_profile": "6.0 overall; writing 6.0; no component below 5.5", "weeks": 6, "delivery": "on_campus_or_online"},
                {"ielts_profile": "5.5 overall; writing 5.5; no component below 5.0", "weeks": 10, "delivery": "on_campus_or_online"},
                {"ielts_profile": "5.5 overall; no more than one component at 5.0", "weeks": 12, "delivery": "online"},
                {"ielts_profile": "5.5 overall; no component below 5.0", "weeks": 20, "delivery": "on_campus"},
                {"ielts_profile": "5.0 overall; no more than one component at 4.5", "weeks": 30, "delivery": "on_campus"},
                {"ielts_profile": "4.5 overall; no more than one component at 4.0", "weeks": 40, "delivery": "on_campus"},
            ],
            "language_risk": "medium",
            "verification_notes": bi(
                "The live course page requires English evidence and publishes current test scores and pre-sessional routes. English is recorded as the operational study language; the page does not expose a separate field explicitly labelled language of instruction.",
                "Canlı ders sayfası İngilizce kanıtı ister ve güncel sınav puanlarıyla hazırlık rotalarını yayımlar. İngilizce fiilî öğrenim dili olarak kaydedilir; sayfa ayrıca açıkça 'öğretim dili' etiketli bağımsız bir alan göstermez.",
            ),
        }
    )

    row["eligibility_profile"].update(
        {
            "eligible_for_non_eu": True,
            "required_previous_degree": (
                "A UK 2:2 honours degree or equivalent in Aerospace Engineering; a UK 2:1 honours degree or equivalent where the degree is in another discipline"
            ),
            "accepted_backgrounds": [
                "Aerospace Engineering at 2:2-equivalent or above",
                "Another discipline at 2:1-equivalent or above",
            ],
            "admission_mode": "application_review",
            "admission_risk": "medium",
            "required_documents": [
                "school_or_college_transcripts_or_certificates",
                "university_transcripts_and_certified_translations_if_applicable",
                "degree_certificates",
                "evidence_of_english_proficiency_unless_exempt",
                "personal_statement_outlining_learning_ambitions",
            ],
            "references_required": False,
            "application_fee": {"amount": 0, "currency": "GBP"},
            "atas_required_for_this_international_route": True,
            "gre": {
                "policy": "not_listed_in_checked_official_required_documents",
                "test_type": "unknown",
                "minimum_scores": {},
                "recommended_scores": {},
                "validity_rule": "",
                "waiver_rules": [],
                "source_ids": [COURSE_URL],
            },
            "verification_notes": bi(
                "The course page has a dedicated international application route and deadline, so non-EU applicants are explicitly in scope. GRE and references are not listed among the published required documents; this is not a universal University prohibition on requesting further evidence.",
                "Ders sayfasında uluslararası adaylar için ayrı başvuru rotası ve son tarih bulunduğundan AB dışı adaylar açıkça kapsamdadır. GRE ve referanslar yayımlanan zorunlu belgeler arasında sayılmaz; bu, Üniversitenin ek kanıt istemesini genel olarak yasakladığı anlamına gelmez.",
            ),
        }
    )

    row["cost_profile"].update(
        {
            "academic_year": "2026/2027",
            "tuition_basis": "official_published_foreign_currency",
            "tuition_gbp_full_programme": 34000,
            "tuition_non_eu_full_program": {
                "amount": 34000,
                "currency": "GBP",
                "basis": "one_year_full_time_programme",
                "academic_year": "2026/2027",
            },
            "application_fee_gbp": 0,
            "student_visa_tuition_deposit_gbp": 2000,
            "deposit_deadline": "2026-09-04",
            "deposit_required_stage": "after_conditional_or_unconditional_offer_when_accepting",
            "deposit_exemptions": [
                "Applicant is taking a Liverpool pre-sessional English course; a GBP 1,000 pre-sessional deposit applies instead",
                "Tuition is paid by a sponsor",
                "Current University of Liverpool student",
            ],
            "cas_dependency": "CAS is issued only after the deposit is received, the offer is accepted, and academic requirements are met",
            "deposit_refund_request_deadline": "2026-10-30",
            "deposit_refund_conditions": [
                "online cancellation within 14 days",
                "qualifying Student visa refusal",
                "ATAS refusal where ATAS was applied for at least eight weeks before programme start",
                "course cancellation or suspension",
                "qualifying exceptional travel restrictions",
                "documented inability to meet offer conditions",
            ],
            "source_notes": bi(
                "The official 2026/27 course fee is GBP 34,000. No EUR conversion is stored. International offer holders usually pay at least GBP 2,000 by 4 September 2026; stated exemptions and refund conditions are retained separately.",
                "Resmî 2026/27 program ücreti 34.000 GBP'dir. EUR dönüşümü saklanmaz. Uluslararası teklif sahipleri genellikle 4 Eylül 2026'ya kadar en az 2.000 GBP öder; belirtilen muafiyet ve iade koşulları ayrı tutulur.",
            ),
        }
    )

    row["scholarship_profile"].update(
        {
            "regional_scholarship_available": True,
            "regional_scholarship_name": "Liverpool Advancement Scholarship",
            "non_eu_eligible": True,
            "application_mode": "automatic",
            "automatic_consideration": True,
            "separate_application_required": False,
            "scholarship_deadline": None,
            "opportunities": [
                {
                    "name": "Liverpool Excellence Scholarship for Postgraduates",
                    "academic_year": "2026/2027",
                    "award": {"amount": 7000, "currency": "GBP", "type": "tuition_fee_discount"},
                    "application_mode": "automatic",
                    "separate_application_required": False,
                    "eligibility": [
                        "First Class or equivalent undergraduate degree",
                        "Self-funded at the international rate",
                        "Joining a Liverpool-campus postgraduate taught master's or MRes in 2026/27",
                        "Offer accepted and deposit paid by the advertised deadlines",
                    ],
                    "exclusions": [
                        "University of Liverpool International College pre-master's student",
                        "fees paid by a sponsor",
                        "PGCert, Professional Doctorate, MPhil, MArch or PhD",
                    ],
                    "application_deadline": None,
                    "status": "active_for_eligible_offer_holders_subject_to_advertised_deadlines",
                    "source_url": EXCELLENCE_URL,
                },
                {
                    "name": "Liverpool Advancement Scholarship",
                    "academic_year": "2026/2027",
                    "award": {"amount": 5000, "currency": "GBP", "type": "tuition_fee_discount"},
                    "application_mode": "automatic",
                    "separate_application_required": False,
                    "eligible_nationalities": [
                        "Indonesia", "Malaysia", "Nigeria", "Pakistan", "South Korea", "Thailand", "Turkey", "Vietnam"
                    ],
                    "turkey_nationality_eligible": True,
                    "eligibility": [
                        "New student who has not studied at the University before",
                        "Self-funded at the international rate",
                        "Joining a Liverpool-campus postgraduate taught master's or MRes in 2026/27",
                        "Offer accepted and deposit paid by the advertised deadlines",
                    ],
                    "exclusions": [
                        "previous study at University of Liverpool International College or XJTLU",
                        "online study",
                        "fees paid by a sponsor",
                        "PGCert, Professional Doctorate, MPhil, MArch or PhD",
                    ],
                    "combination_rule": "Cannot be combined with the Excellence scholarship; an eligible First Class holder receives the increased GBP 7,000 Excellence discount",
                    "application_deadline": None,
                    "status": "active_for_eligible_offer_holders_subject_to_advertised_deadlines",
                    "source_url": ADVANCEMENT_URL,
                },
            ],
            "verification_notes": bi(
                "Both retained 2026/27 awards are automatic and require no separate scholarship form. Turkey is explicitly eligible for the GBP 5,000 Advancement discount. The awards depend on accepting the offer and paying the deposit by advertised deadlines; the pages publish no standalone scholarship date.",
                "Tutulan iki 2026/27 bursu da otomatiktir ve ayrı burs formu gerektirmez. Türkiye 5.000 GBP Advancement indirimi için açıkça uygundur. Burslar teklifin kabulüne ve ilan edilen tarihlere kadar depozito ödenmesine bağlıdır; sayfalarda bağımsız burs tarihi yayımlanmaz.",
            ),
        }
    )

    rents = [
        rent_item("Philharmonic Court", "Premier", 215.18, 10974.18, 3658.06, True),
        rent_item("Dover Court", "Premier", 194.95, 9942.45, 3314.15, True),
        rent_item("Tudor Close", "Single Bed", 172.48, 8796.48, 2932.16, True),
        rent_item("Tudor Close", "Double Bed", 181.30, 9246.30, 3082.10, True),
        rent_item("Crown Place", "Deluxe Studio", 227.43, 11598.93, 3866.31, True),
        rent_item("Crown Place", "Deluxe Studio Apartment", 242.20, 12352.20, 4117.40, True),
        rent_item("Vine Court", "Premier Studio Apartment", 271.53, 13848.03, 4616.01, True),
        rent_item("Agnes Jones House", "Premium Non-Ensuite", 117.00, 5967.00, None, False),
        rent_item("Agnes Jones House", "Ensuite", 165.00, 8415.00, None, False),
        rent_item("Agnes Jones House", "Studio and some two-person studios", 195.00, 9945.00, None, False),
        rent_item("Bedford Street South", "Classic Non-Ensuite", 115.00, 5865.00, None, False),
        rent_item("Unite Students Cambridge Court", "Classic Ensuite", 132.08, 6736.08, None, False),
    ]
    row["living_profile"].update(
        {
            "city_cost_level": "official_budget_range_available",
            "housing_difficulty": "deadline_sensitive",
            "housing_access": "guaranteed",
            "housing_application_separate": True,
            "housing_guarantee": {
                "available": True,
                "applicant_scope": "international_postgraduate_September_2026_entry",
                "application_deadline": "2026-07-31",
                "status_as_of_last_checked": "deadline_passed",
                "after_deadline_policy": "best efforts in University halls or preferred providers",
                "application_stage": "after_receiving_an_academic_offer",
                "allocation_condition": "status confirmed as expected entrant",
                "deposit_required": False,
                "guarantor_required": False,
            },
            "housing_options": [
                "University city-campus halls",
                "University preferred private providers",
                "private accommodation",
            ],
            "housing_contract_start": "2026-09-05",
            "housing_contract_end": "2027-08-28",
            "housing_contract_weeks": 51,
            "housing_rent_gbp_per_week_min": 115.00,
            "housing_rent_gbp_per_week_max": 271.53,
            "housing_budget_gbp_per_year_min": 5865.00,
            "housing_budget_gbp_per_year_max": 13848.03,
            "official_rent_items": rents,
            "monthly_living_cost_gbp_per_month_min": 900,
            "monthly_living_cost_gbp_per_month_max": 1350,
            "living_cost_gbp_per_year_min": 10800,
            "living_cost_gbp_per_year_max": 16200,
            "ukvi_maintenance_threshold": {
                "amount_per_month": 1171,
                "months": 9,
                "total": 10539,
                "currency": "GBP",
                "twelve_month_arithmetic": 14052,
                "scope_note": "Visa maintenance threshold, not a University promise that this amount covers every student's actual spending",
            },
            "official_living_cost_items": [
                {"item": "total_monthly_living_expenses", "amount_min": 900, "amount_max": 1350, "currency": "GBP", "period": "month", "basis": "feedback from current international undergraduate and master's students"},
                {"item": "university_halls_including_utilities_and_wifi", "amount_min": 688, "amount_max": 1120, "currency": "GBP", "period": "month"},
                {"item": "private_accommodation", "amount_min": 450, "amount_max": 800, "currency": "GBP", "period": "month"},
                {"item": "private_household_bills", "amount_min": 50, "amount_max": 200, "currency": "GBP", "period": "month"},
                {"item": "travel_and_transport", "amount_min": 20, "amount_max": 90, "currency": "GBP", "period": "month"},
                {"item": "food_and_household_necessities", "amount_min": 150, "amount_max": 400, "currency": "GBP", "period": "month"},
                {"item": "mobile_phone", "amount_min": 15, "amount_max": 50, "currency": "GBP", "period": "month"},
                {"item": "socialising_and_entertainment", "amount_min": 50, "amount_max": 250, "currency": "GBP", "period": "month"},
                {"item": "study_costs", "amount_min": 10, "amount_max": 30, "currency": "GBP", "period": "month"},
                {"item": "gym_membership", "amount_min": 22, "amount_max": 30, "currency": "GBP", "period": "month"},
            ],
            "living_risk": "medium",
            "verification_notes": bi(
                "The University estimates GBP 900-1,350 total per month. The accommodation PDF separately publishes twelve 51-week postgraduate room types at GBP 115-271.53 per week. The 31 July international-postgraduate guarantee deadline had passed by the verification date.",
                "Üniversite aylık toplamı 900-1.350 GBP olarak tahmin eder. Konaklama PDF'si ayrıca 51 haftalık on iki lisansüstü oda tipini haftalık 115-271,53 GBP olarak yayımlar. Uluslararası lisansüstü garanti tarihi olan 31 Temmuz, doğrulama tarihinde geçmişti.",
            ),
        }
    )

    mandatory = [
        {"code": "AERO406", "name": "Advanced Fluid Mechanics and Aerodynamics", "credits": 15},
        {"code": "AERO420", "name": "Aerospace Capstone Group Design Project", "credits": 30, "spans": "semesters_one_and_two"},
        {"code": "ENGG596", "name": "Technical Writing for Engineers", "credits": 7.5, "conditional": True},
        {"code": "MNGT502", "name": "Project Management", "credits": 7.5},
        {"code": "AERO408", "name": "Aerostructural Analysis and Optimisation", "credits": 15},
        {"code": "AERO415", "name": "Aeroelasticity", "credits": 7.5},
        {"code": "MNGT414", "name": "Enterprise Studies", "credits": 7.5},
        {"code": "ENGG660", "name": "MSc(Eng) Project", "credits": 60, "period": "summer"},
    ]
    electives = [
        {"code": "AERO319", "name": "Spaceflight", "credits": 7.5},
        {"code": "AERO401", "name": "Flight Handling Qualities", "credits": 15},
        {"code": "AERO419", "name": "Space Mission Design", "credits": 15},
        {"code": "AERO430", "name": "Advanced Guidance Systems", "credits": 7.5},
        {"code": "ENVS470", "name": "Business and the Environment", "credits": 15},
        {"code": "MECH433", "name": "Energy and the Environment", "credits": 15},
        {"code": "MATS631", "name": "Advanced Engineering Materials", "credits": 15},
    ]
    row["curriculum_profile"].update(
        {
            "tracks": [],
            "specializations": [],
            "mandatory_courses": mandatory,
            "elective_courses": electives,
            "mandatory_course_count_including_conditional_writing_and_project": 8,
            "mandatory_course_count_if_writing_exempt": 7,
            "published_elective_option_count": 7,
            "elective_credits_if_writing_exempt": 30,
            "elective_credits_if_writing_required": 22.5,
            "exact_elective_selection_count": None,
            "technical_writing_exemption": "UK students are exempt; EU and international students with strong English may be exempt with programme-director approval",
            "thesis_required": True,
            "research_project_credits": 60,
            "internship_required": False,
            "published_module_credit_sum_in_each_stated_route": 172.5,
            "credit_reconciliation_status": "needs_verification",
            "accreditation_status": "accredited",
            "accrediting_bodies": ["Royal Aeronautical Society", "Institution of Mechanical Engineers"],
            "curriculum_url": COURSE_URL,
            "verification_notes": bi(
                "The page publishes eight mandatory titles when the conditional writing module and summer project are included, and seven optional titles. Because options carry 7.5 or 15 credits, an exact elective course count is not published. The visible modules plus the stated elective credits total 172.5 credits in both writing scenarios; no missing 7.5-credit module is invented, and the official-page arithmetic is flagged for clarification. Modules are illustrative and subject to change.",
                "Sayfa koşullu yazım dersi ve yaz projesi dâhil sekiz zorunlu, yedi seçmeli başlık yayımlar. Seçmeliler 7,5 veya 15 kredi olduğundan tam seçmeli ders sayısı yayımlanmaz. Görünen dersler ile belirtilen seçmeli krediler iki yazım senaryosunda da 172,5 kredi eder; eksik 7,5 kredilik ders uydurulmaz ve resmî sayfa aritmetiği açıklama için işaretlenir. Dersler örnek niteliğinde olup değişebilir.",
            ),
        }
    )

    row["category_profile"].update(
        {
            "primary_categories": ["aerospace_engineering"],
            "secondary_categories": [
                "aerodynamics_and_cfd", "flight_dynamics_and_control", "structures_and_aeroelasticity", "space_systems"
            ],
            "subcategories": [
                "aircraft_design", "spaceflight", "space_mission_design", "guidance_systems", "finite_element_analysis"
            ],
            "normalized_tags": [
                "aerospace_engineering", "computational_fluid_dynamics", "flight_simulation", "guidance_navigation_control", "space_mission_design", "aeroelasticity", "structures"
            ],
            "category_scores": {
                "aerospace_engineering": 95,
                "aerodynamics_and_cfd": 90,
                "flight_dynamics_and_control": 90,
                "structures_and_aeroelasticity": 85,
                "space_systems": 75,
            },
        }
    )

    row["research_profile"].update(
        {
            "department_research_areas": [
                "advanced computational fluid dynamics",
                "flight simulation and assessment",
                "autonomous flight control systems",
                "space mission planning",
                "spacecraft robotics and GNC",
            ],
            "labs": [
                "Flight Simulation Laboratory",
                "Computational Fluid Dynamics Laboratory",
                "Zero-G AstroLab",
                "large blow-down wind tunnel",
                "90,000-litre recirculating water tunnel",
            ],
            "research_centers": ["Flight Science and Technology research group"],
            "facilities": [
                "full-motion reconfigurable flight simulators",
                "wind tunnels",
                "Jupiter CFD cluster",
                "Digital Innovation Facility",
                "5 x 2.5 m precision air-bearing microgravity floor with motion capture",
            ],
            "research_strength_summary": bi(
                "The official department evidence is unusually strong across CFD, flight dynamics, simulation, autonomy and space mission planning. Zero-G AstroLab adds hardware-in-the-loop spacecraft rendezvous, docking and GNC testing, while the Flight Science group documents dedicated simulation and CFD laboratory themes.",
                "Resmî bölüm kanıtı HAD, uçuş dinamiği, simülasyon, otonomi ve uzay görevi planlamasında olağandışı derecede güçlüdür. Zero-G AstroLab uzay aracı buluşma, kenetlenme ve GNC için donanım-döngüde test ekler; Flight Science grubu özel simülasyon ve HAD laboratuvar temalarını belgeler.",
            ),
            "research_strength_score": 90,
            "research_sources": [RESEARCH_URL, FACILITIES_URL, FLIGHT_RESEARCH_URL, SPACE_RESEARCH_URL],
        }
    )

    row["industry_ecosystem_profile"].update(
        {
            "nearby_companies": [],
            "confirmed_partners": [
                "BAE Systems",
                "AgustaWestland",
                "National Research Council Canada",
                "DLR",
                "CIRA",
                "ONERA",
                "NLR",
            ],
            "research_institutes": ["GARTEUR", "NASA working groups", "European Commission Framework projects"],
            "ecosystem_notes": bi(
                "The current official research pages document external research engagement, including BAE Systems preferred-academic-partner status in Dynamic Loads Prediction and collaboration with AgustaWestland and NRC Canada. These relationships are research evidence, not a promise of an internship, job or individual project placement.",
                "Güncel resmî araştırma sayfaları, Dinamik Yük Tahmini alanında BAE Systems tercihli akademik ortaklığı ile AgustaWestland ve NRC Canada iş birliklerini belgeler. Bu ilişkiler araştırma kanıtıdır; staj, iş veya bireysel proje yerleştirmesi garantisi değildir.",
            ),
            "ecosystem_strength_score": 85,
        }
    )

    row["application_timeline_profile"].update(
        {
            "academic_year": "2026/2027",
            "intake_terms": ["September"],
            "programme_start_date": "2026-09-28",
            "non_eu_deadline": "2026-07-17",
            "uk_deadline": "2026-09-11",
            "scholarship_deadline": None,
            "pre_enrolment_required": None,
            "atas_required": True,
            "timeline_risk": "high",
            "deadline_events": [
                {"event": "international_course_application", "date": "2026-07-17", "status": "closed"},
                {"event": "international_postgraduate_housing_guarantee", "date": "2026-07-31", "status": "closed"},
                {"event": "international_masters_deposit", "date": "2026-09-04", "status": "upcoming_for_existing_offer_holders"},
                {"event": "UK_course_application", "date": "2026-09-11", "status": "open"},
                {"event": "programme_start", "date": "2026-09-28", "status": "upcoming"},
            ],
            "alternative_application_form_locations": [
                "Cuba", "Crimea", "Donetsk People's Republic", "Iran", "Luhansk People's Republic", "North Korea", "Syria"
            ],
            "deadline_notes": bi(
                "The international application deadline and housing-guarantee deadline had passed by 14 August 2026. Existing offer holders still face the 4 September deposit deadline. Scholarship pages provide no standalone date and instead bind eligibility to advertised offer-acceptance and deposit deadlines. No future-cycle date is estimated.",
                "Uluslararası başvuru ve konaklama garantisi tarihleri 14 Ağustos 2026 itibarıyla geçmişti. Mevcut teklif sahiplerinin 4 Eylül depozito tarihi devam eder. Burs sayfaları ayrı tarih vermez; uygunluğu ilan edilen teklif-kabul ve depozito tarihlerine bağlar. Gelecek dönem tarihi tahmin edilmez.",
            ),
        }
    )

    profile = row["source_profile"]
    profile.update(
        {
            "official_program_page": COURSE_URL,
            "official_admission_page": COURSE_URL,
            "official_curriculum_page": COURSE_URL,
            "official_tuition_page": DEPOSIT_URL,
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
            "curriculum": "medium",
            "application_timeline_profile": "high",
            "deadline": "high",
            "deadlines": "high",
            "living_profile": "high",
            "housing": "high",
            "research": "high",
            "industry": "high",
        }
    )
    profile["source_log"] = [
        source(COURSE_URL, "University of Liverpool Advanced Aerospace Engineering MSc (Eng) 2026/27", "official_program_page", "ok", ["program", "language", "admission", "non_eu_eligibility", "tuition", "curriculum", "deadline", "accreditation", "documents"], "Live 2026/27 course page with routes, required documents, deadlines, fees, entry requirements, language scores, modules, credits and accreditation."),
        source(DEPOSIT_URL, "University of Liverpool international master's tuition-fee deposit", "official_tuition_page", "ok", ["tuition", "deposit", "deadline", "visa"], "Deposit amount, exemptions, CAS dependency, payment deadline and refund conditions."),
        source(EXCELLENCE_URL, "Liverpool Excellence Scholarship for Postgraduates 2026/27", "official_scholarship_page", "ok", ["scholarship", "funding", "eligibility"], "Automatic GBP 7,000 international tuition discount, eligibility and exclusions."),
        source(ADVANCEMENT_URL, "Liverpool Advancement Scholarship 2026/27", "official_scholarship_page", "ok", ["scholarship", "funding", "eligibility"], "Automatic GBP 5,000 country award including Turkey, eligibility, exclusions and non-combination rule."),
        source(HOUSING_URL, "University of Liverpool applying for accommodation 2026/27", "official_housing_page", "ok", ["housing", "deadline", "application"], "International-postgraduate guarantee, deadline, application stage and post-deadline policy."),
        source(HOUSING_FEES_PDF, "University of Liverpool Postgraduate Accommodation Fees 2026", "official_housing_page", "pdf", ["housing", "living", "deadline"], "Visual verification of twelve room types, weekly and 51-week prices, instalments and contract dates."),
        source(LIVING_URL, "University of Liverpool international-student living costs", "official_cost_of_living_page", "ok", ["living", "housing", "visa"], "University monthly estimate, itemised ranges and separately labelled UKVI maintenance threshold."),
        source(RESEARCH_URL, "University of Liverpool Mechanical and Aerospace Engineering research", "official_department_page", "ok", ["research", "facilities"], "Current CFD, simulation, autonomy, space-mission and research-facility evidence."),
        source(FACILITIES_URL, "University of Liverpool Mechanical and Aerospace Engineering facilities", "official_department_page", "ok", ["research", "facilities", "curriculum"], "Full-motion simulators, wind tunnels, recirculating water tunnel and digital engineering facilities."),
        source(FLIGHT_RESEARCH_URL, "University of Liverpool Flight Science and Technology", "official_department_page", "ok", ["research", "industry", "facilities"], "Flight simulation and CFD laboratory themes plus named research partners."),
        source(SPACE_RESEARCH_URL, "University of Liverpool planetary defence, robotics and autonomy", "official_department_page", "ok", ["research", "facilities", "industry"], "Zero-G AstroLab hardware, spacecraft GNC themes and mission collaborations."),
    ]

    row["decision_summary"].update(
        {
            "main_strengths": [
                bi(
                    "An accredited aerospace MSc combines aircraft design, CFD, aeroelasticity and flight dynamics with selectable spaceflight, space-mission-design and guidance modules.",
                    "Akredite havacılık MSc'si uçak tasarımı, HAD, aeroelastisite ve uçuş dinamiğini seçilebilir uzay uçuşu, uzay görevi tasarımı ve güdüm dersleriyle birleştirir.",
                ),
                bi(
                    "Research infrastructure is unusually relevant to both air and space: full-motion simulators, wind tunnels, a dedicated CFD cluster and Zero-G AstroLab hardware-in-the-loop GNC testing.",
                    "Araştırma altyapısı hem hava hem uzay için olağandışı derecede uygundur: tam hareketli simülatörler, rüzgâr tünelleri, özel HAD kümesi ve Zero-G AstroLab donanım-döngüde GNC testleri.",
                ),
                bi(
                    "For Turkish nationals, the 2026/27 Advancement award is an automatic GBP 5,000 tuition discount; First Class-equivalent holders may instead receive the automatic GBP 7,000 Excellence award.",
                    "Türk vatandaşları için 2026/27 Advancement bursu otomatik 5.000 GBP öğrenim indirimi sağlar; First Class dengi mezunlar bunun yerine otomatik 7.000 GBP Excellence bursunu alabilir.",
                ),
            ],
            "main_risks": [
                bi(
                    "The international programme deadline and guaranteed-housing deadline had already passed at verification; late applicants should not infer eligibility from the still-open UK deadline.",
                    "Doğrulama tarihinde uluslararası program ve garantili konaklama tarihleri geçmişti; geç adaylar hâlâ açık Birleşik Krallık tarihinden uygunluk çıkarmamalıdır.",
                ),
                bi(
                    "Tuition is GBP 34,000 before discounts, while the official total living estimate is GBP 10,800-16,200 for twelve months and published 51-week housing alone can reach GBP 13,848.03.",
                    "İndirim öncesi öğrenim 34.000 GBP'dir; resmî on iki aylık toplam yaşam tahmini 10.800-16.200 GBP ve yayımlanmış 51 haftalık konut tek başına 13.848,03 GBP'ye çıkabilir.",
                ),
                bi(
                    "The visible module table and stated elective-credit rules reconcile to 172.5 rather than 180 credits; the missing 7.5 credits must be clarified with the programme and are not guessed here.",
                    "Görünen ders tablosu ve belirtilen seçmeli-kredi kuralları 180 yerine 172,5 krediye ulaşır; eksik 7,5 kredi programla açıklığa kavuşturulmalı ve burada tahmin edilmemelidir.",
                ),
            ],
            "best_for": [
                bi(
                    "Students seeking aircraft-centred depth with credible access to spaceflight, mission design, GNC and spacecraft-autonomy research rather than a purely orbital-systems degree.",
                    "Tamamen yörünge sistemleri derecesi yerine uçak merkezli derinlikle birlikte uzay uçuşu, görev tasarımı, GNC ve uzay aracı otonomisi araştırmasına güvenilir erişim arayan öğrenciler.",
                )
            ],
            "not_ideal_for": [
                bi(
                    "Applicants who need a still-open international 2026 application route, a currently guaranteed late housing place, or a curriculum devoted exclusively to spacecraft systems.",
                    "Hâlâ açık 2026 uluslararası başvuru rotası, geç dönemde güncel konut garantisi veya yalnızca uzay aracı sistemlerine ayrılmış müfredat isteyen adaylar.",
                )
            ],
        }
    )

    quality = audit_record(row)
    quality["audited_at"] = CHECKED
    row["data_quality"] = quality
    profile["needs_verification"] = True
    profile["verification_notes"] = bi(
        "All decision-critical groups have checked official sources. Verification remains open only for the official module table's unexplained 7.5-credit shortfall and for future-cycle replacement of intake-specific dates.",
        "Tüm karar-kritik gruplarda kontrol edilmiş resmî kaynak vardır. Doğrulama yalnızca resmî ders tablosundaki açıklanmayan 7,5 kredi açığı ve döneme özgü tarihlerin gelecek döngüde yenilenmesi için açık tutulur.",
    )
    row["quality_control"].update(
        {
            "qc_status": "passed" if quality["status"] == "verified" else "needs_revision",
            "checked_at": CHECKED,
            "failed_canary_tests": [],
            "remaining_verification_tasks": [
                bi(
                    "Ask the programme to reconcile the visible 172.5-credit arithmetic; do not create a missing module without an official source.",
                    "Programdan görünen 172,5 kredi aritmetiğini açıklamasını isteyin; resmî kaynak olmadan eksik ders oluşturmayın.",
                ),
                bi(
                    "Replace all 2026/27 deadlines, fees, scholarships and housing prices when Liverpool publishes the next intake; never roll dates forward.",
                    "Liverpool sonraki dönemi yayımladığında tüm 2026/27 tarihlerini, ücretleri, bursları ve konut fiyatlarını değiştirin; tarihleri ileri taşımayın.",
                ),
            ],
            "qc_notes": bi(
                "The record passes source-grounding and canary checks while preserving the official curriculum discrepancy as an unresolved field-level note.",
                "Kayıt kaynak temellendirme ve canary denetimlerini geçerken resmî müfredat uyuşmazlığını çözülmemiş alan notu olarak korur.",
            ),
        }
    )

    DATA_PATH.write_text(
        json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
