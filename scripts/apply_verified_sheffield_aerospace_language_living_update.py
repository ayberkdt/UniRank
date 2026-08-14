"""Apply verified 2026/27 Sheffield Aerospace Engineering MSc decision data."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from unirank.core.integrity import audit_record


DATA_PATH = ROOT / "data_base" / "ingiltere.json"
RECORD_ID = "university-of-sheffield"
CHECKED = "2026-08-14"
COURSE_URL = (
    "https://sheffield.ac.uk/postgraduate/taught/courses/2026/"
    "aerospace-engineering-msc"
)
LANGUAGE_URL = "https://sheffield.ac.uk/postgraduate/english-language"
DOCUMENTS_URL = "https://sheffield.ac.uk/postgraduate/supporting"
DEADLINES_URL = "https://sheffield.ac.uk/postgraduate/deadlines"
DEPOSIT_URL = "https://sheffield.ac.uk/fees/fee-deposits"
SCHOLARSHIP_URL = (
    "https://sheffield.ac.uk/international/fees-and-funding/scholarships/"
    "postgraduate/international-postgraduate-scholarship"
)
HOUSING_GUARANTEE_PDF = (
    "https://sheffield.ac.uk/media/117846/download?attachment="
)
HOUSING_RENTS_URL = "https://sheffield.ac.uk/accommodation/rents"
LIVING_URL = "https://sheffield.ac.uk/money-matters/living-costs"
FACILITIES_URL = "https://www.sheffield.ac.uk/mac/school/facilities"
THERMOFLUIDS_URL = "https://sheffield.ac.uk/mac/research/groups/thermofluids"


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
            "english_level_required": "Standard",
            "minimum_scores": {
                "ielts_academic": {"overall": 6.5, "each_component": 6.0},
                "cambridge_c1_advanced": {"overall": 176, "each_component": 169},
                "languagecert_academic_selt": {"overall": 70, "each_component": 65},
                "oxford_test_of_english_advanced": {"overall": 136, "each_component": 126},
                "pte_academic": {"overall": 61, "each_component": 56},
                "toefl_ibt_to_january_2026": {
                    "overall": 88,
                    "listening": 19,
                    "reading": 20,
                    "speaking": 22,
                    "writing": 19,
                },
                "toefl_ibt_from_january_2026": {
                    "overall": 4.5,
                    "listening": 4.5,
                    "speaking": 4.5,
                    "reading": 4.0,
                    "writing": 4.0,
                },
            },
            "trinity_ise_iii": "Pass or above in each component",
            "test_validity": "no more than two years before the course start",
            "accepted_ielts_formats": [
                "IELTS Academic paper-based",
                "IELTS Academic computer-based",
                "IELTS for UKVI Academic",
                "IELTS Online",
                "IELTS One Skill Retake",
            ],
            "not_accepted": [
                "IELTS Life Skills",
                "IELTS General Training",
                "PTE Academic Online",
                "TOEFL MyBest scores",
                "discontinued TOEFL paper-based test",
            ],
            "waiver_rules": [
                "A first degree or postgraduate diploma taught in person in English in a majority native English-speaking country, normally awarded within five years",
                "A recent qualifying English-taught degree in a non-majority English-speaking country plus the additional test or B1 evidence and official medium-of-instruction letter specified by the policy",
                "An appropriate Sheffield ELTC pre-sessional completed within two years",
                "A Sheffield International College Pre-Masters completed within two years",
            ],
            "pre_sessional_available": True,
            "language_risk": "medium",
            "verification_notes": bi(
                "The programme requires Sheffield's Standard level and publishes IELTS 6.5 "
                "with 6.0 in every component. The postgraduate policy supplies current test "
                "equivalents, time limits and bounded waiver routes. English is recorded as "
                "the operational study language; the course page does not show a separate "
                "field explicitly labelled 'language of instruction'.",
                "Program Sheffield'in Standard düzeyini ve her bileşende 6,0 olmak üzere "
                "IELTS 6,5 şartını yayımlar. Lisansüstü politika güncel test denkliklerini, "
                "süre sınırlarını ve sınırları belirli muafiyet yollarını verir. İngilizce "
                "fiilî öğrenim dili olarak kaydedilir; ders sayfası ayrıca açıkça 'öğretim "
                "dili' etiketli bir alan göstermez.",
            ),
        }
    )

    row["eligibility_profile"].update(
        {
            "eligible_for_non_eu": True,
            "required_previous_degree": (
                "Minimum 2:1 undergraduate honours degree in a relevant subject with at "
                "least one accepted mathematics module"
            ),
            "accepted_backgrounds": [
                "Aeronautical or Aeronautics Engineering",
                "Aerospace",
                "Aircraft Design and Engineering",
                "Automotive Engineering",
                "Aviation Propulsion Engineering",
                "Chemical Engineering",
                "Civil or Structural Engineering",
                "Computer Science",
                "Control Systems Engineering",
                "Electrical Engineering",
                "Energy and Power Engineering",
                "Engineering Mechanics",
                "Materials Science and Engineering",
                "Mechanical Engineering",
                "Mechatronics Engineering",
                "Metallurgy",
            ],
            "prerequisite_modules": [
                "At least one module in Calculus, Linear Algebra, Mathematics, or another module with Mathematics in its title"
            ],
            "holistic_review": True,
            "required_documents": [
                "academic_transcript_and_degree_certificate_or_latest_transcript",
                "marking_scheme_for_non_UK_qualifications",
                "official_authenticated_english_translations_if_needed",
                "english_language_certificate_if_required",
            ],
            "optional_documents": [
                "CV or resume, especially where relevant professional experience supports the application"
            ],
            "references_required": False,
            "supporting_statement_required": False,
            "overseas_qualification_verification": (
                "Qualification Check after offer where instructed; the applicant is not charged"
            ),
            "decision_time_guidance": "around four weeks for most taught courses, longer at busy times",
            "admission_risk": "medium",
            "gre": {
                "policy": "not_listed_in_checked_official_required_documents",
                "test_type": "GRE General",
                "minimum_scores": {},
                "recommended_scores": {},
                "validity_rule": "",
                "waiver_rules": [],
                "source_ids": [COURSE_URL, DOCUMENTS_URL],
                "verification_notes": bi(
                    "GRE is absent from both the programme-specific requirements and the "
                    "checked University supporting-document policy. This is a bounded "
                    "'not listed' finding, not a claim about every Sheffield programme.",
                    "GRE hem programa özgü koşullarda hem de kontrol edilen Üniversite destek "
                    "belgesi politikasında yoktur. Bu, tüm Sheffield programları hakkında "
                    "iddia değil, sınırları belirli bir 'listelenmedi' bulgusudur.",
                ),
            },
            "atas": {
                "may_be_required": True,
                "applicant_scope": "only applicants whose offer letter requires ATAS",
                "advised_application_date": "2026-08-17",
                "verification_notes": bi(
                    "The course page exposes an ATAS module-title tool and the University "
                    "publishes an advised date for applicants whose course/offer requires "
                    "clearance. ATAS is not marked as universal for every applicant.",
                    "Ders sayfası ATAS ders başlığı aracını gösterir ve Üniversite, programı "
                    "veya teklifi izin gerektiren adaylar için tavsiye edilen tarih yayımlar. "
                    "ATAS her aday için zorunlu olarak işaretlenmez.",
                ),
            },
            "verification_notes": bi(
                "The published subject list is broad, but every applicant still needs a "
                "mathematics module and is assessed on preparation and achievement as a whole. "
                "Listed subjects and modules are indicative, not automatic admission.",
                "Yayımlanan alan listesi geniştir; ancak her aday yine bir matematik dersi "
                "sunmalı ve hazırlığı ile başarısı bütün olarak değerlendirilmelidir. Listelenen "
                "alanlar ve dersler otomatik kabul anlamına gelmez.",
            ),
        }
    )

    row["cost_profile"].update(
        {
            "academic_year": "2026/2027",
            "tuition_basis": "official_published_foreign_currency",
            "tuition_non_eu_full_program": {
                "amount": 32905,
                "currency": "GBP",
                "basis": "one_year_full_time_programme",
                "academic_year": "2026/2027",
            },
            "tuition_gbp_full_programme": 32905,
            "tuition_gbp_per_year": 32905,
            "fixed_fee_guarantee": True,
            "application_fee_gbp": None,
            "student_visa_tuition_deposit_gbp": 2000,
            "deposit_required_for": (
                "international fee-paying students on campus-based taught postgraduate courses"
            ),
            "deposit_request_stage": (
                "normally when accepting an Unconditional offer for this course"
            ),
            "deposit_deadline": None,
            "deposit_deadline_basis": "offer_letter_controls; no Aerospace-specific fixed date published",
            "deposit_exemptions": [
                "At least half of tuition sponsored by a University-recognised body, with evidence"
            ],
            "deposit_refund_request_deadline": "2026-11-01",
            "deposit_notes": bi(
                "The GBP 2,000 deposit is deducted from tuition and must be paid before Sheffield "
                "will arrange a CAS. Aerospace Engineering is not in the published list that "
                "requires payment with a Conditional offer; the individual offer letter controls "
                "the actual request and deadline.",
                "2.000 GBP depozito öğrenim ücretinden düşülür ve Sheffield CAS düzenlemeden "
                "önce ödenmelidir. Aerospace Engineering, Koşullu teklifle ödeme isteyen "
                "yayımlanmış listede değildir; gerçek talep ve son tarihi bireysel teklif "
                "mektubu belirler.",
            ),
            "source_notes": bi(
                "The live 2026/27 course page publishes GBP 32,905 for overseas students and a "
                "fixed-fee guarantee. No EUR conversion or unverified application fee is stored.",
                "Canlı 2026/27 ders sayfası yurtdışı öğrenciler için 32.905 GBP ve sabit ücret "
                "garantisi yayımlar. EUR dönüşümü veya doğrulanmamış başvuru ücreti saklanmaz.",
            ),
        }
    )

    row["scholarship_profile"].update(
        {
            "regional_scholarship_available": False,
            "regional_scholarship_name": None,
            "non_eu_eligible": True,
            "application_mode": "automatic",
            "automatic_consideration": True,
            "separate_application_required": False,
            "current_cycle_status": "closed",
            "scholarship_deadline": "2026-07-07",
            "scholarship_application_url": SCHOLARSHIP_URL,
            "opportunities": [
                {
                    "name": "International Postgraduate Scholarship 2026",
                    "academic_year": "2026/2027",
                    "status": "closed",
                    "award": {
                        "amount": 3000,
                        "currency": "GBP",
                        "type": "tuition_fee_reduction",
                    },
                    "application_mode": "automatic_after_eligible_offer_acceptance",
                    "separate_application_required": False,
                    "offer_acceptance_deadline": "2026-07-07T16:00:00+01:00",
                    "eligibility_summary": bi(
                        "The applicant had to be self-funded, overseas-fee, starting an "
                        "eligible postgraduate taught degree in September 2026, studying the "
                        "course in full at Sheffield, and accept the offer by the deadline.",
                        "Aday öz finansmanlı ve yurtdışı ücret statüsünde olmalı, Eylül 2026'da "
                        "uygun bir lisansüstü programa başlamalı, programın tamamını Sheffield'da "
                        "okumalı ve teklifi son tarihe kadar kabul etmeliydi.",
                    ),
                    "combination_limit": (
                        "not normally combinable with other University scholarships, discounts, "
                        "or external sponsorship unless explicitly stated"
                    ),
                    "source_url": SCHOLARSHIP_URL,
                }
            ],
            "funding_notes": bi(
                "The award required no scholarship form, but it was not unconditional: the "
                "study offer had to be accepted by 4pm UK time on 7 July 2026. That deadline "
                "has passed, so a new late applicant must not be shown as currently funded.",
                "Ödül ayrı burs formu gerektirmiyordu ancak koşulsuz değildi: eğitim teklifinin "
                "7 Temmuz 2026 saat 16.00 UK zamanına kadar kabul edilmesi gerekiyordu. Bu tarih "
                "geçti; yeni ve geç bir aday güncel olarak finanse edilmiş gösterilmemelidir.",
            ),
            "verification_notes": bi(
                "Aerospace Engineering MSc is a full-time campus postgraduate taught degree and "
                "is not among the published exclusions. Award eligibility still depends on the "
                "individual's fee and funding status.",
                "Aerospace Engineering MSc tam zamanlı, kampüste yürütülen lisansüstü programdır "
                "ve yayımlanan istisnalar arasında değildir. Ödül uygunluğu yine bireyin ücret "
                "ve finansman statüsüne bağlıdır.",
            ),
        }
    )

    row["living_profile"].update(
        {
            "city_cost_level": "medium",
            "housing_difficulty": "conditional_guarantee_offer_acceptance_deadline_passed",
            "living_risk": "high",
            "housing_access": "guaranteed",
            "housing_application_separate": True,
            "housing_application_deadline": "2026-09-03",
            "housing_options": [
                "University postgraduate City accommodation",
                "University postgraduate Ranmoor and Endcliffe accommodation",
                "Private rented accommodation",
                "Limited family accommodation",
            ],
            "housing_guarantee": {
                "available": True,
                "scope": "single_occupancy_study_bedroom_for_eligible_postgraduate_students",
                "offer_acceptance_deadline": "2026-07-26",
                "application_deadline": "2026-09-03",
                "status_as_of_last_checked": (
                    "offer_acceptance_deadline_passed; application_window_open_only_for_already_eligible_students"
                ),
                "conditions": [
                    "Accept an offer on an award-bearing course by 26 July 2026",
                    "Meet all offer conditions",
                    "Use the CAS number if applicable",
                    "Submit the accommodation application by 3 September 2026",
                ],
                "limitations": [
                    "Guarantee is for a study bedroom, not a preferred residence or room type",
                    "Family accommodation is not guaranteed",
                    "This one-year MSc does not qualify for the subsequent-year postgraduate guarantee",
                ],
                "source_url": HOUSING_GUARANTEE_PDF,
            },
            "official_rent_items": [
                {
                    "item": "published_postgraduate_room_examples",
                    "amount_min": 155.68,
                    "amount_max": 240.38,
                    "currency": "GBP",
                    "period": "week",
                    "academic_year": "2026/2027",
                    "contract_lengths_weeks": [42, 51],
                    "source_url": HOUSING_RENTS_URL,
                },
                {
                    "item": "published_postgraduate_contract_totals",
                    "amount_min": 6538.56,
                    "amount_max": 12259.39,
                    "currency": "GBP",
                    "period": "contract",
                    "academic_year": "2026/2027",
                    "contract_lengths_weeks": [42, 51],
                    "source_url": HOUSING_RENTS_URL,
                },
            ],
            "rent_includes": [
                "utility bills",
                "contents insurance",
                "internet access",
                "Residence Life events",
                "sports activities",
            ],
            "official_living_cost_items": [
                {"item": "groceries", "amount": 146, "currency": "GBP", "period": "month"},
                {"item": "transport", "amount": 67, "currency": "GBP", "period": "month"},
                {"item": "going_out", "amount": 61, "currency": "GBP", "period": "month"},
                {"item": "takeaways_and_eating_out", "amount": 49, "currency": "GBP", "period": "month"},
                {"item": "clothes_and_shopping", "amount": 40, "currency": "GBP", "period": "month"},
                {"item": "mobile_phone", "amount": 15, "currency": "GBP", "period": "month"},
            ],
            "living_cost_component_provenance": (
                "University guidance page reproducing selected Save the Student 2025 survey averages"
            ),
            "housing_notes": bi(
                "The official 2026/27 PG table spans GBP 155.68-240.38 per week and GBP "
                "6,538.56-12,259.39 per listed contract. Contracts are self-catered and 42 or "
                "51 weeks; most 51-week contracts are reserved for postgraduates.",
                "Resmî 2026/27 lisansüstü tablosu haftalık 155,68-240,38 GBP ve listelenen "
                "sözleşme başına 6.538,56-12.259,39 GBP aralığındadır. Sözleşmeler yemeksiz "
                "42 veya 51 haftadır; 51 haftalıkların çoğu lisansüstülere ayrılır.",
            ),
            "verification_notes": bi(
                "Rent figures are current University amounts. The non-housing monthly items are "
                "secondary survey averages reproduced by Sheffield, not a complete official "
                "budget, a visa-maintenance figure or a guarantee of personal spending.",
                "Kira rakamları güncel Üniversite tutarlarıdır. Konut dışı aylık kalemler "
                "Sheffield'ın aktardığı ikincil anket ortalamalarıdır; tam resmî bütçe, vize "
                "geçim tutarı veya kişisel harcama garantisi değildir.",
            ),
        }
    )
    for item in row["living_profile"]["official_living_cost_items"]:
        item["source_url"] = LIVING_URL
        item["confidence"] = "medium"

    optional_modules = [
        "Advanced Aerospace Propulsion Technology (15 credits)",
        "Advanced Control (15 credits)",
        "Advanced Engineering Fluid Dynamics (15 credits)",
        "Advanced Dynamics (15 credits)",
        "Advanced Materials Manufacturing (15 credits)",
        "Aviation Safety and Aeroelasticity (15 credits)",
        "Design and Manufacture of Composites (15 credits)",
        "Energy Storage Management (15 credits)",
        "Engineering Alloys (15 credits)",
        "Industrial Applications of Finite Element Analysis (15 credits)",
        "Motion Control and Servo Drives (15 credits)",
        "Multisensor and Decision Systems (15 credits)",
        "Real-Time Embedded Systems (15 credits)",
        "Modelling of Concurrent Systems (15 credits)",
        "Testing and Verification in Safety-Critical Systems (15 credits)",
        "Mobile Robotics and Autonomous Systems (15 credits)",
        "Modern Control and System Identification (15 credits)",
        "Managing Innovation and Change in Engineering Contexts (15 credits)",
    ]
    row["curriculum_profile"].update(
        {
            "tracks": [
                "Conversion strand for graduates from another discipline",
                "Advanced strand for graduates with a strong Aerospace Engineering background",
            ],
            "specializations": ["Aeromechanics", "Avionics", "Broad tailored route"],
            "mandatory_courses": [
                "Advanced Aerospace Design and Prototype Testing (20 credits; both strands)",
                "Aerospace Individual Investigative Project (60 credits; both strands)",
            ],
            "conversion_strand_core_courses": [
                "Advanced Aerospace Design and Prototype Testing (20 credits)",
                "Aerospace Individual Investigative Project (60 credits)",
                "Aircraft Dynamics and Control (10 credits)",
                "Aero Propulsion (10 credits)",
                "Aircraft Design (10 credits)",
                "Aerodynamic Design (10 credits)",
            ],
            "advanced_strand_core_courses": [
                "Advanced Aerospace Design and Prototype Testing (20 credits)",
                "Aerospace Individual Investigative Project (60 credits)",
                "Advanced Aerospace Propulsion Technology (15 credits)",
                "Aviation Safety and Aeroelasticity (15 credits)",
                "One of Finite Element Techniques or Computational Fluid Dynamics (10 credits)",
            ],
            "advanced_strand_required_choice": [
                "Finite Element Techniques (10 credits)",
                "Computational Fluid Dynamics (10 credits)",
            ],
            "elective_courses": optional_modules,
            "published_elective_option_count": len(optional_modules),
            "elective_selection_count": 4,
            "elective_credits_each": 15,
            "published_route_credit_total": 180,
            "published_route_credit_total_basis": "sum_of_published_route_requirements",
            "research_project_required": True,
            "group_design_build_fly_project_required": True,
            "thesis_required": None,
            "internship_required": False,
            "accreditation_status": "not_currently_accredited",
            "accreditation_notes": bi(
                "The University says the curriculum aligns with Royal Aeronautical Society "
                "professional standards and is working toward review, but the MSc is not "
                "currently accredited. Anticipated accreditation is not treated as current.",
                "Üniversite müfredatın Royal Aeronautical Society mesleki standartlarıyla "
                "uyumlu olduğunu ve inceleme için çalıştığını söyler; ancak MSc şu anda "
                "akredite değildir. Beklenen akreditasyon güncel sayılmaz.",
            ),
            "curriculum_url": COURSE_URL,
            "verification_notes": bi(
                "Both published routes total 180 Sheffield credits when the stated four "
                "15-credit options are added. The page calls the module list examples and "
                "warns availability can change; duplicate titles that are core in one route "
                "must not be assumed available again to the same student.",
                "Belirtilen dört adet 15 kredilik seçmeli eklendiğinde yayımlanan iki rota da "
                "180 Sheffield kredisine ulaşır. Sayfa ders listesini örnek olarak niteler ve "
                "bulunabilirliğin değişebileceğini söyler; bir rotada çekirdek olan tekrar eden "
                "başlıkların aynı öğrenciye yeniden açık olduğu varsayılmaz.",
            ),
        }
    )

    row["category_profile"].update(
        {
            "primary_categories": [
                "aerodynamics",
                "propulsion",
                "flight_mechanics",
                "structures",
                "avionics",
            ],
            "secondary_categories": [
                "cfd",
                "stability_control",
                "autonomy",
                "uav",
                "manufacturing",
            ],
            "subcategories": [
                "rocket_propulsion",
                "aeroelasticity",
                "finite_element_analysis",
                "multisensor_decision_systems",
                "real_time_embedded_systems",
                "safety_critical_software",
                "mobile_robotics",
            ],
            "normalized_tags": [
                "aerodynamics",
                "propulsion",
                "flight_mechanics",
                "structures",
                "avionics",
                "cfd",
                "stability_control",
                "autonomy",
                "uav",
                "manufacturing",
            ],
        }
    )

    row["research_profile"].update(
        {
            "department_research_areas": [
                "Computational aerodynamics and CFD",
                "Active flow control and laminar-flow wings",
                "Blended-wing-body aircraft",
                "Low-Reynolds-number micro air vehicles",
                "Combustion and propulsion",
                "Aerospace materials and structural dynamics",
            ],
            "labs": [
                "Aerospace Simulation and Propulsion Lab",
                "Jet Propulsion Lab",
                "Structures and Dynamics Laboratory",
                "Thermodynamics and Mechanics Laboratory",
                "iForge makerspace",
                "Four Armfield C15 subsonic wind tunnels",
                "GUNT ET796 jet engine test bench",
                "Flight simulators and drone systems",
            ],
            "research_centers": ["Thermofluids Research Group"],
            "research_strength_summary": bi(
                "The MSc is backed by unusually concrete teaching hardware in simulation, "
                "jet propulsion, wind tunnels, structures and prototyping. The Thermofluids "
                "group documents current aerospace research in CFD, flow control, laminar "
                "wings, blended-wing bodies and micro air vehicles. Facility access supports "
                "learning but does not guarantee a particular funded research placement.",
                "MSc; simülasyon, jet itki, rüzgâr tünelleri, yapılar ve prototiplemede somut "
                "öğretim donanımıyla desteklenir. Thermofluids grubu HAD, akış kontrolü, laminer "
                "kanatlar, bütünleşik kanat-gövde ve mikro hava araçlarında güncel araştırmayı "
                "belgeler. Altyapı erişimi öğrenimi destekler ancak belirli finanse edilmiş "
                "araştırma yerini garanti etmez.",
            ),
            "research_strength_score": None,
            "research_sources": [COURSE_URL, FACILITIES_URL, THERMOFLUIDS_URL],
        }
    )

    row["industry_ecosystem_profile"].update(
        {
            "nearby_companies": [],
            "confirmed_partners": [
                "Airbus UK",
                "BAE Systems",
                "Boeing",
                "EADS",
                "QinetiQ",
                "Rolls-Royce",
            ],
            "research_institutes": [],
            "ecosystem_notes": bi(
                "The current MSc page explicitly calls these organisations strong partnerships "
                "that help shape Sheffield aerospace work. They are recorded as institutional "
                "relationships, not as a promise of an internship, project or job for each MSc "
                "student.",
                "Güncel MSc sayfası bu kuruluşları Sheffield havacılık çalışmalarını "
                "şekillendiren güçlü ortaklıklar olarak açıkça tanımlar. Bunlar kurumsal ilişki "
                "olarak kaydedilir; her MSc öğrencisine staj, proje veya iş vaadi değildir.",
            ),
            "ecosystem_strength_score": None,
        }
    )

    row["application_timeline_profile"].update(
        {
            "academic_year": "2026/2027",
            "intake_terms": ["September"],
            "application_opened": "2025-09-15",
            "non_eu_deadline": "2026-09-01",
            "eu_deadline": "2026-09-01",
            "general_application_deadline": "2026-09-04T17:00:00+01:00",
            "scholarship_deadline": "2026-07-07",
            "timeline_risk": "high",
            "deadline_events": [
                {"event": "applications_opened", "date": "2025-09-15", "status_as_of_last_checked": "past", "source_url": DEADLINES_URL},
                {"event": "automatic_scholarship_offer_acceptance_deadline", "date": "2026-07-07", "time": "16:00 UK time", "status_as_of_last_checked": "closed", "source_url": SCHOLARSHIP_URL},
                {"event": "housing_guarantee_offer_acceptance_deadline", "date": "2026-07-26", "status_as_of_last_checked": "closed", "source_url": HOUSING_GUARANTEE_PDF},
                {"event": "advised_ATAS_application_date_if_required", "date": "2026-08-17", "status_as_of_last_checked": "imminent", "source_url": DEADLINES_URL},
                {"event": "visa_required_applicant_programme_deadline", "date": "2026-09-01", "status_as_of_last_checked": "open", "source_url": DEADLINES_URL},
                {"event": "deferral_request_deadline", "date": "2026-09-01", "status_as_of_last_checked": "open", "source_url": DEADLINES_URL},
                {"event": "postgraduate_accommodation_application_deadline", "date": "2026-09-03", "status_as_of_last_checked": "open_for_previously_eligible_students", "source_url": HOUSING_GUARANTEE_PDF},
                {"event": "general_programme_application_close", "date": "2026-09-04", "time": "17:00 BST", "status_as_of_last_checked": "open", "source_url": DEADLINES_URL},
                {"event": "advised_CAS_application_date", "date": "2026-09-07", "status_as_of_last_checked": "future", "source_url": DEADLINES_URL},
                {"event": "offer_conditions_and_qualification_verification_deadline", "date": "2026-09-21", "status_as_of_last_checked": "future", "source_url": DEADLINES_URL},
                {"event": "teaching_begins", "date": "2026-09-28", "status_as_of_last_checked": "future", "source_url": DEADLINES_URL},
            ],
            "deadline_notes": bi(
                "The course remained open to visa-requiring applicants until 1 September when "
                "checked, but the funding and housing-offer-acceptance cutoffs had passed and "
                "the advised ATAS date was only three days away. Applying at the published "
                "final deadline is therefore not a low-risk visa strategy.",
                "Kontrol tarihinde program vize gereken adaylar için 1 Eylül'e kadar açıktı; "
                "ancak burs ve yurt için teklif-kabul kesimleri geçmiş, tavsiye edilen ATAS "
                "tarihine yalnız üç gün kalmıştı. Bu nedenle yayımlanan son tarihte başvurmak "
                "düşük riskli bir vize stratejisi değildir.",
            ),
        }
    )

    profile = row["source_profile"]
    profile.update(
        {
            "official_admission_page": DOCUMENTS_URL,
            "official_curriculum_page": COURSE_URL,
            "official_tuition_page": COURSE_URL,
            "official_scholarship_page": SCHOLARSHIP_URL,
            "official_language_policy_page": LANGUAGE_URL,
            "official_housing_page": HOUSING_GUARANTEE_PDF,
            "official_cost_of_living_page": LIVING_URL,
            "official_department_page": THERMOFLUIDS_URL,
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
            "living_profile": "medium",
            "housing": "high",
            "research": "high",
            "industry": "high",
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
        raise RuntimeError("Sheffield programme sources are missing")
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
            "research",
            "industry",
        ]:
            if field not in relevant:
                relevant.append(field)
        source["relevant_fields"] = relevant
        source["confidence"] = "high"
        source["notes"] = bi(
            "Live official 2026/27 course page checked for status, routes, modules, credits, "
            "entry requirements, IELTS, fees, accreditation, facilities and named partnerships.",
            "Canlı resmî 2026/27 ders sayfası durum, rotalar, dersler, krediler, giriş şartları, "
            "IELTS, ücret, akreditasyon, altyapı ve adlandırılmış ortaklıklar için kontrol edildi.",
        )

    sources = [
        (LANGUAGE_URL, "University of Sheffield postgraduate English requirements", "official_university_policy_page", "ok", ["language"], "Current Standard-level equivalents, validity, exclusions and waiver routes."),
        (DOCUMENTS_URL, "University of Sheffield postgraduate supporting documents", "official_admission_page", "ok", ["admission", "documents", "non_eu_eligibility"], "Degree evidence, marking scheme, translations, English evidence and qualification verification."),
        (DEADLINES_URL, "University of Sheffield postgraduate key dates 2026", "official_admission_page", "ok", ["deadline", "admission", "visa"], "Application, ATAS, CAS, condition, verification and teaching dates."),
        (DEPOSIT_URL, "University of Sheffield postgraduate taught tuition deposits", "official_tuition_page", "ok", ["tuition", "deposit", "visa"], "GBP 2,000 amount, offer stage, sponsor exemption, CAS dependency and refund rules."),
        (SCHOLARSHIP_URL, "University of Sheffield International Postgraduate Scholarship 2026", "official_scholarship_page", "ok", ["scholarship", "funding", "deadline"], "Automatic GBP 3,000 discount, acceptance deadline, eligibility and exclusions."),
        (HOUSING_GUARANTEE_PDF, "University of Sheffield Accommodation Guarantee 2026/27", "official_housing_page", "pdf", ["housing", "deadline"], "Postgraduate guarantee conditions, acceptance date, application date and exclusions."),
        (HOUSING_RENTS_URL, "University of Sheffield accommodation rents 2026/27", "official_housing_page", "ok", ["housing", "living"], "PG room and contract prices, lengths and included services."),
        (LIVING_URL, "University of Sheffield living-cost guidance", "official_cost_of_living_page", "ok", ["living", "housing"], "University guidance plus clearly scoped secondary 2025 survey components."),
        (FACILITIES_URL, "University of Sheffield MAC learning and teaching facilities", "official_department_page", "redirects", ["research", "facilities", "curriculum"], "Named aerospace simulation, propulsion, structures, fluids and materials facilities; the www URL redirects to the canonical non-www page."),
        (THERMOFLUIDS_URL, "University of Sheffield Thermofluids research group", "official_department_page", "ok", ["research"], "Current aerospace research themes and named academic expertise."),
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
                "confidence": "medium" if url == LIVING_URL else "high",
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
                    "Two explicit 180-credit routes let conversion students build foundations "
                    "while aerospace graduates move into advanced propulsion, aeroelasticity "
                    "and CFD/FEA, with every student completing four options and two projects.",
                    "İki açık 180 kredilik rota, alan değiştirenlere temel kazandırırken havacılık "
                    "mezunlarını ileri itki, aeroelastisite ve HAD/SEA'ya taşır; her öğrenci dört "
                    "seçmeli ve iki proje tamamlar.",
                ),
                bi(
                    "Hands-on infrastructure is unusually concrete: UAV design-build-fly, jet "
                    "engines, subsonic wind tunnels, simulators, structures labs and iForge.",
                    "Uygulamalı altyapı olağandışı derecede somuttur: İHA tasarla-üret-uçur, jet "
                    "motorları, sesaltı rüzgâr tünelleri, simülatörler, yapı laboratuvarları ve iForge.",
                ),
                bi(
                    "The University explicitly documents strong aerospace partnerships with "
                    "Airbus UK, BAE Systems, Boeing, EADS, QinetiQ and Rolls-Royce.",
                    "Üniversite Airbus UK, BAE Systems, Boeing, EADS, QinetiQ ve Rolls-Royce ile "
                    "güçlü havacılık ortaklıklarını açıkça belgeler.",
                ),
            ],
            "main_risks": [
                bi(
                    "The MSc is not currently accredited; alignment with RAeS standards and an "
                    "anticipated future review are not equivalent to current accreditation.",
                    "MSc şu anda akredite değildir; RAeS standartlarıyla uyum ve beklenen gelecek "
                    "incelemesi güncel akreditasyona eşdeğer değildir.",
                ),
                bi(
                    "The automatic GBP 3,000 scholarship and the housing-guarantee offer-acceptance "
                    "cutoff have passed, even though the programme itself remains briefly open.",
                    "Program kısa süre daha açık olsa da otomatik 3.000 GBP burs ve yurt garantisi "
                    "için teklif-kabul kesim tarihi geçmiştir.",
                ),
                bi(
                    "GBP 32,905 tuition plus published housing of GBP 6,538.56-12,259.39 creates "
                    "a high financing burden; the living-cost page does not publish a complete "
                    "University total budget.",
                    "32.905 GBP öğrenim ücreti ve yayımlanan 6.538,56-12.259,39 GBP konut tutarı "
                    "yüksek finansman yükü yaratır; yaşam gideri sayfası tam Üniversite toplam "
                    "bütçesi yayımlamaz.",
                ),
            ],
            "best_for": [
                bi(
                    "Applicants wanting a broad, practical aircraft-focused MSc with conversion "
                    "and advanced routes across aeromechanics, avionics, propulsion and autonomy.",
                    "Aeromekanik, aviyonik, itki ve otonomide alan değiştirme ve ileri rotalar "
                    "sunan geniş, uygulamalı, uçak odaklı MSc isteyen adaylar.",
                )
            ],
            "not_ideal_for": [
                bi(
                    "Students requiring current professional accreditation, guaranteed late-cycle "
                    "funding, or a curriculum centred primarily on spacecraft and orbital systems.",
                    "Güncel mesleki akreditasyon, geç döngüde garantili finansman veya ağırlıkla "
                    "uzay aracı ve yörünge sistemleri merkezli müfredat isteyen öğrenciler.",
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
                    "Replace all cycle-specific programme, scholarship, ATAS, CAS and housing "
                    "dates when Sheffield publishes the next intake; never roll dates forward.",
                    "Sheffield sonraki giriş dönemini yayımladığında döngüye özgü tüm program, "
                    "burs, ATAS, CAS ve konut tarihlerini değiştirin; tarihleri ileri taşımayın.",
                ),
                bi(
                    "Recheck accreditation status before every counselling cycle and do not "
                    "convert an anticipated review into an accredited status.",
                    "Her danışmanlık döngüsünden önce akreditasyon durumunu yeniden kontrol edin "
                    "ve beklenen incelemeyi akredite statüsüne dönüştürmeyin.",
                ),
            ],
            "qc_notes": bi(
                "Every current decision-critical group has checked official evidence. Medium "
                "confidence is retained for operational teaching language and for non-housing "
                "living items whose underlying figures are from a secondary survey.",
                "Her güncel karar-kritik grupta kontrol edilmiş resmî kanıt vardır. Fiilî öğretim "
                "dili ve temel rakamları ikincil ankete dayanan konut dışı yaşam kalemleri için "
                "orta güven korunur.",
            ),
        }
    )

    DATA_PATH.write_text(
        json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
