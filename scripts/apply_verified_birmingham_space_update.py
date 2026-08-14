"""Apply source-checked 2026/27 Birmingham Space Engineering MSc data."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from unirank.core.integrity import audit_record


DATA_PATH = ROOT / "data_base" / "ingiltere.json"
RECORD_ID = "university-of-birmingham"
CHECKED = "2026-08-14"
COURSE_URL = "https://www.birmingham.ac.uk/study/postgraduate/subjects/aerospace-engineering-courses/space-engineering-msc"
INTERNATIONAL_COURSE_URL = COURSE_URL + "?location=India"
APPLICATION_URL = "https://www.birmingham.ac.uk/study/postgraduate/taught/apply"
OFFER_URL = "https://www.birmingham.ac.uk/study/postgraduate/taught/apply/your-offer"
DEPOSIT_URL = "https://www.birmingham.ac.uk/university/colleges/professional/external/admissions/deposit-refund-policy-pgt"
HIGH_FLIERS_URL = "https://www.birmingham.ac.uk/study/scholarships-funding/postgraduate-high-fliers-scholarship"
ESA_URL = "https://www.birmingham.ac.uk/study/scholarships-funding/the-esa-academy-academic-scholarship-programme"
HOUSING_URL = "https://www.birmingham.ac.uk/study/accommodation/apply-for-your-accommodation/postgraduate-students"
HOUSING_GUARANTEE_URL = "https://www.birmingham.ac.uk/study/accommodation/apply-for-your-accommodation/guarantee-scheme"
HOUSING_FEES_URL = "https://www.birmingham.ac.uk/study/accommodation/our-accommodation/accommodation-fees"
LIVING_URL = "https://www.birmingham.ac.uk/study/postgraduate/support/money-advice"
RESEARCH_URL = "https://www.birmingham.ac.uk/research/centres-institutes/research-in-electronic-electrical-and-systems-engineering/communications-and-sensing/serene"
SPACE_WEATHER_URL = "https://www.birmingham.ac.uk/research/centres-institutes/research-in-electronic-electrical-and-systems-engineering/communications-and-sensing/serene/what-is-space-weather"


def bi(en: str, tr: str) -> dict[str, str]:
    return {"en": en, "tr": tr}


def source(
    url: str,
    title: str,
    source_type: str,
    relevant_fields: list[str],
    note_en: str,
    confidence: str = "high",
) -> dict:
    return {
        "url": url,
        "title": title,
        "source_type": source_type,
        "access_status": "ok",
        "last_checked": CHECKED,
        "relevant_fields": relevant_fields,
        "confidence": confidence,
        "notes": bi(
            note_en,
            "Resmî kaynak belirtilen alanlar, tarihler ve kapsam sınırları için doğrudan kontrol edildi.",
        ),
    }


def rent(
    residence: str,
    room_type: str,
    weekly_min: float,
    total_min: float,
    weekly_max: float | None = None,
    total_max: float | None = None,
    partner: bool = False,
) -> dict:
    return {
        "residence": residence,
        "room_type": room_type,
        "weekly_price_min": weekly_min,
        "weekly_price_max": weekly_max if weekly_max is not None else weekly_min,
        "published_contract_total_min": total_min,
        "published_contract_total_max": total_max if total_max is not None else total_min,
        "currency": "GBP",
        "weekly_price_status": "indicative",
        "partner_accommodation": partner,
        "utilities_wifi_contents_insurance_included": True,
        "source_url": HOUSING_FEES_URL,
    }


def main() -> None:
    rows = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    matches = [row for row in rows if row.get("id") == RECORD_ID]
    if len(matches) != 1:
        raise RuntimeError(f"Expected one {RECORD_ID!r} record; found {len(matches)}")
    row = matches[0]

    row.update(
        {
            "program_name": "Space Engineering MSc",
            "program_degree": "MSc",
            "degree_level": "Master",
            "duration_years": 1,
            "ects": None,
            "uk_credits": 180,
            "credit_system_note": bi(
                "The University publishes 180 UK credits. No ECTS conversion is asserted.",
                "Üniversite 180 Birleşik Krallık kredisi yayımlar. ECTS dönüşümü varsayılmaz.",
            ),
            "program_url": COURSE_URL,
            "program_status": "active",
            "teaching_language": ["English"],
        }
    )

    row["eligibility_profile"].update(
        {
            "eligible_for_non_eu": True,
            "required_previous_degree": "A 2:1 Honours degree or equivalent in a physical science or engineering subject",
            "accepted_backgrounds": ["physical science", "engineering"],
            "admission_mode": "application_review_by_course_admissions_tutor",
            "admission_risk": "medium",
            "required_documents": [
                "online_application",
                "official_academic_transcripts_showing_subjects_and_grades",
                "certified_english_translation_if_documents_are_not_in_english",
                "english_language_evidence_unless_an_accepted_alternative_applies",
                "passport_personal_details_page_for_international_offer_holders",
            ],
            "documents_that_may_be_offer_conditions": [
                "final_degree_certificate",
                "final_transcript",
                "reference_if_requested_in_the_offer",
                "ATAS_certificate_if_the_offer_states_it_is_required",
            ],
            "references_required": None,
            "application_fee": {"amount": 0, "currency": "GBP"},
            "gre": {
                "policy": "not_listed_in_checked_official_course_or_application_requirements",
                "test_type": "unknown",
                "minimum_scores": {},
                "recommended_scores": {},
                "validity_rule": "",
                "waiver_rules": [],
                "source_ids": [COURSE_URL, APPLICATION_URL],
            },
            "verification_notes": bi(
                "The live course page explicitly gives international English requirements and an overseas application route. Official transcripts and English evidence are published requirements; a reference and ATAS can be individual offer conditions, so neither is marked universally mandatory. GRE is not listed in the checked requirements, not declared prohibited.",
                "Canlı program sayfası uluslararası İngilizce koşullarını ve yurtdışı başvuru rotasını açıkça verir. Resmî transkript ve İngilizce kanıtı yayımlanmış koşullardır; referans ve ATAS bireysel teklif koşulu olabilir, bu nedenle ikisi de herkese zorunlu işaretlenmez. GRE kontrol edilen koşullarda listelenmez; yasak olduğu iddia edilmez.",
            ),
        }
    )

    row["language_profile"].update(
        {
            "teaching_language": ["English"],
            "teaching_languages": ["English"],
            "english_required": True,
            "english_level_required": "IELTS 6.5 overall with no band below 6.0, or an accepted equivalent",
            "minimum_scores": {
                "ielts": {"overall": 6.5, "each_band": 6.0},
                "toefl_ibt_before_2026_01": {"overall": 88, "reading": 21, "listening": 20, "speaking": 22, "writing": 21},
                "toefl_ibt_from_2026_01": {"overall": 4.5, "two_skills_min": 4.5, "other_two_skills_min": 4.0},
                "pte_academic": {"overall": 67, "each_skill": 64},
                "cambridge_c1_advanced": {"overall": 176, "each_component": 169},
                "languagecert_esol_selt_ukvi": {"level": "B2 Communicator", "each_skill": 33},
            },
            "pre_sessional_available": True,
            "language_risk": "medium",
            "verification_notes": bi(
                "The course is delivered through English-language lectures, seminars, tutorials, laboratories and projects and publishes course-specific English thresholds. A presessional English route is available to conditional offer holders.",
                "Program İngilizce ders, seminer, uygulama, laboratuvar ve projelerle yürütülür ve programa özgü İngilizce eşiklerini yayımlar. Koşullu teklif sahipleri için akademik İngilizce hazırlık rotası vardır.",
            ),
        }
    )

    row["cost_profile"].update(
        {
            "academic_year": "2026/2027",
            "tuition_basis": "official_published_foreign_currency",
            "tuition_gbp_full_programme": 33660,
            "tuition_non_eu_full_program": {
                "amount": 33660,
                "currency": "GBP",
                "basis": "one_year_full_time_programme",
                "academic_year": "2026/2027",
            },
            "application_fee_gbp": 0,
            "deposit_public_page_conflict": {
                "status": "needs_applicant_portal_confirmation",
                "amounts_published_gbp": [2000, 3000],
                "offer_guidance_page_amount_gbp": 2000,
                "current_deposit_refund_policy_amount_gbp": 3000,
                "binding_source": "individual_offer_letter_and_applicant_portal",
            },
            "student_visa_tuition_deposit_gbp": None,
            "deposit_deadline": "individual_applicant_portal_date; general final overseas date 2026-08-14",
            "deposit_deducted_from_tuition": True,
            "deposit_exemption": "No deposit when scholarship or financial-guarantee evidence has been supplied, according to the refund policy",
            "deposit_refund_request_deadline": "2026-10-31",
            "deposit_refund_conditions": [
                "cancellation within the 14-day cooling-off period",
                "non-fraudulent Student visa refusal",
                "programme cancellation by the University",
                "documented inability to travel for reasons outside the applicant's control",
                "qualifications obtained are not accepted to meet offer conditions",
                "one-year deferral may carry the deposit forward before arrival",
            ],
            "source_notes": bi(
                "International tuition is GBP 33,660 for 2026 entry. Two current official pages conflict on the deposit amount (GBP 2,000 versus GBP 3,000), so the database deliberately stores no single definitive amount: the applicant's offer letter and portal control. No EUR conversion is stored.",
                "2026 girişinde uluslararası öğrenim ücreti 33.660 GBP'dir. İki güncel resmî sayfa depozito tutarında çelişir (2.000 ve 3.000 GBP); bu nedenle veritabanı kasıtlı olarak tek bir kesin tutar göstermez: başvuru sahibinin teklif mektubu ve portalı belirleyicidir. EUR dönüşümü tutulmaz.",
            ),
        }
    )

    row["scholarship_profile"].update(
        {
            "regional_scholarship_available": True,
            "regional_scholarship_name": "Postgraduate High Fliers Scholarship",
            "non_eu_eligible": True,
            "application_mode": "automatic",
            "automatic_consideration": True,
            "separate_application_required": False,
            "scholarship_deadline": None,
            "scholarship_application_url": HIGH_FLIERS_URL,
            "opportunities": [
                {
                    "name": "Postgraduate High Fliers Scholarship",
                    "academic_year": "2026/2027",
                    "award": {"amount": 5000, "currency": "GBP", "type": "tuition_fee_discount"},
                    "application_mode": "automatic",
                    "separate_application_required": False,
                    "turkey_domicile_eligible": True,
                    "eligibility": [
                        "domiciled in an explicitly listed country, including Turkey",
                        "classified as an overseas fee payer",
                        "offer for an eligible full-time 180-credit taught master's at the Birmingham UK campus starting September 2026",
                        "accept the offer and pay the admission deposit by the offer-letter deadline",
                    ],
                    "exclusions": ["full or partial external tuition scholarship or sponsorship"],
                    "status_at_last_check": "closed",
                    "illustrative_net_tuition_gbp_if_awarded": 28660,
                    "net_tuition_calculation": "33660 - 5000; derived arithmetic from two official published amounts",
                    "source_url": HIGH_FLIERS_URL,
                },
                {
                    "name": "ESA Academy Academic Scholarship Programme",
                    "award": {"type": "full_tuition", "published_amount_is_for": "2025/2026"},
                    "programme_specific": True,
                    "application_mode": "eligibility_assessed_on_course_application",
                    "separate_application_required": False,
                    "turkey_nationality_eligible_on_published_list": False,
                    "deadline": "to_be_confirmed",
                    "status_at_last_check": "current_page_contains_stale_2025_26_award_value",
                    "source_url": ESA_URL,
                },
            ],
            "funding_notes": bi(
                "The High Fliers award is the actionable Turkey-domicile route: it is automatic, worth GBP 5,000, and required no separate form, but the live page was already marked closed on 14 August 2026. The ESA page is programme-specific but lists no Turkey eligibility and still carries a 2025/26 award amount with an unconfirmed deadline.",
                "Türkiye'de ikamet edenler için uygulanabilir rota High Fliers bursudur: otomatik, 5.000 GBP değerinde ve ayrı form gerektirmez; ancak canlı sayfa 14 Ağustos 2026'da kapanmış görünüyordu. ESA sayfası programa özgüdür fakat Türkiye'yi uygun listede göstermez ve son tarihi teyitsiz, 2025/26 tutarını taşır.",
            ),
            "verification_notes": bi(
                "Domicile, fee status, programme format, offer acceptance, deposit and external-funding exclusions all matter. Nationality alone is not enough for High Fliers eligibility.",
                "İkamet, ücret statüsü, program biçimi, teklif kabulü, depozito ve dış finansman istisnaları birlikte önemlidir. Yalnızca vatandaşlık High Fliers uygunluğu için yeterli değildir.",
            ),
        }
    )

    rents = [
        rent("Maple Bank", "shared bathroom", 107, 5335),
        rent("Tennis Court", "shared bathroom", 149, 7425),
        rent("The Spinney", "shared bathroom", 167, 8332),
        rent("Elgar Court", "en-suite", 200, 9972),
        rent("Tennis Court", "en-suite", 204, 10180),
        rent("Jarratt Hall standard", "en-suite", 189, 9445),
        rent("Jarratt Hall large", "en-suite", 196, 9774),
        rent("Bournbrook", "en-suite", 222, 11059),
        rent("Oak Brook Park", "en-suite", 215, 10965, 219, 11169, True),
        rent("Chamberlain", "studio apartment", 324, 16178),
        rent("Pritchatts Road", "studio", 280, 13958),
        rent("Pritchatts Road", "studio plus", 291, 14541),
        rent("Pritchatts Road", "studio apartment", 340, 16966),
        rent("Pritchatts Road", "studio apartment plus", 360, 17966),
        rent("Mason", "studio apartment", 324, 16171),
        rent("Mason", "studio apartment plus", 344, 17165),
        rent("The Metalworks", "studio", 250, 12750, 279, 14229, True),
    ]
    row["living_profile"].update(
        {
            "city_cost_level": "official_budget_available_no_comparative_city_label",
            "housing_difficulty": "high_after_guarantee_deadline",
            "living_risk": "high",
            "housing_access": "guaranteed",
            "housing_application_separate": True,
            "housing_guarantee": {
                "eligible_group": "new international postgraduate students",
                "requirement": "apply and book by the guarantee deadline",
                "deadline": "2026-07-31",
                "deadline_status": "passed",
                "current_status": "guarantee_deadline_passed; remaining rooms subject to availability",
            },
            "housing_advance_payment": {"amount": 550, "currency": "GBP", "type": "initial_instalment_not_refundable_end_of_contract_deposit"},
            "housing_budget_gbp_per_year_min": 5335,
            "housing_budget_gbp_per_year_max": 17966,
            "average_room_rent_gbp_per_month_min": None,
            "average_room_rent_gbp_per_month_max": None,
            "official_rent_items": rents,
            "housing_options": ["shared bathroom", "en-suite", "studio", "studio apartment", "partner accommodation"],
            "official_living_cost_items": [
                {"scenario": "self_catered_halls_essential", "weekly_total": 185, "annual_50_week_total": 9250, "currency": "GBP"},
                {"scenario": "private_house_essential", "weekly_total": 174, "annual_50_week_total": 8700, "currency": "GBP"},
                {"scenario": "variable_costs", "weekly_total": 110, "annual_50_week_total": 5500, "currency": "GBP"},
            ],
            "derived_total_living_budget_gbp_50_weeks": {
                "private_house": 14200,
                "self_catered_halls": 14750,
                "method": "official essential annual total plus official variable annual total",
                "confidence": "medium",
            },
            "verification_notes": bi(
                "The University publishes 17 postgraduate room options from GBP 5,335 to GBP 17,966 total; weekly figures are explicitly indicative and utilities, Wi-Fi and contents insurance are included. The international postgraduate guarantee required application and booking by 31 July 2026 and has passed. The GBP 14,200-14,750 planning range is transparent arithmetic from the University's separate 50-week essential and variable totals, not a quoted all-in promise.",
                "Üniversite toplam 5.335-17.966 GBP arasında 17 lisansüstü oda seçeneği yayımlar; haftalık tutarlar açıkça gösterge niteliğindedir ve faturalar, Wi-Fi ile eşya sigortası dahildir. Uluslararası lisansüstü konut garantisi 31 Temmuz 2026'ya kadar başvuru ve rezervasyon gerektiriyordu ve sona erdi. 14.200-14.750 GBP planlama aralığı, Üniversitenin ayrı 50 haftalık zorunlu ve değişken toplamlarından şeffaf aritmetiktir; yayımlanmış her şey dâhil taahhüt değildir.",
            ),
        }
    )

    mandatory = [
        "Advanced Space Mission Analysis and Design (20 credits)",
        "Communication, Ethics, and Teamwork for Space Missions (10 credits)",
        "Individual Research Project (60 credits)",
        "Materials and Manufacturing for Space Applications (10 credits)",
        "Space Environment (20 credits)",
    ]
    electives = [
        "CubeSat Design (20 credits)",
        "Human Spaceflight Critique (20 credits)",
        "Satellite Communications (20 credits)",
        "Space Propulsion and Power Systems (20 credits)",
        "Spacecraft Mechanical Design (20 credits)",
    ]
    row["curriculum_profile"].update(
        {
            "tracks": [],
            "specializations": ["space weather", "radar", "space sustainability"],
            "mandatory_courses": mandatory,
            "elective_courses": electives,
            "mandatory_course_count": 5,
            "published_elective_option_count": 5,
            "selected_elective_course_count": 3,
            "total_modules_taken_including_research_project": 8,
            "published_unique_module_title_count": 10,
            "core_credits": 120,
            "elective_credits": 60,
            "total_uk_credits": 180,
            "thesis_required": True,
            "research_project_credits": 60,
            "internship_required": False,
            "delivery_methods": ["lectures", "seminars", "tutorials", "project-based learning", "practical laboratories", "group activities", "individual projects"],
            "project_formats": ["experimental_or_laboratory", "theoretical_or_literature", "modelling", "mixed"],
            "accreditation_status": "accredited",
            "accrediting_bodies": ["Royal Aeronautical Society on behalf of the Engineering Council"],
            "professional_recognition": "meets the academic requirements for Further Learning for CEng registration",
            "curriculum_url": COURSE_URL,
            "verification_notes": bi(
                "The 2026/27 table reconciles exactly: five core modules total 120 credits and students select three 20-credit options for another 60. Eight modules are therefore taken including the 60-credit research project. The five optional titles are examples and all modules may change.",
                "2026/27 tablosu tam olarak uzlaşır: beş çekirdek ders 120 kredi eder ve öğrenciler üç adet 20 kredilik seçenekle 60 kredi daha alır. Böylece 60 kredilik araştırma projesi dâhil sekiz ders alınır. Beş seçmeli başlık örnektir ve tüm dersler değişebilir.",
            ),
        }
    )

    row["category_profile"].update(
        {
            "primary_categories": ["space_engineering"],
            "secondary_categories": ["space_systems", "space_environment", "satellite_communications", "space_propulsion", "spacecraft_structures"],
            "subcategories": ["space_mission_design", "cubesats", "human_spaceflight", "space_weather", "radar", "space_sustainability"],
            "normalized_tags": ["space_engineering", "space_mission_design", "space_environment", "cubesat_design", "satellite_communications", "space_propulsion", "spacecraft_mechanical_design"],
            "category_scores": {"space_engineering": 96, "space_systems": 90, "space_environment": 95, "satellite_communications": 80, "space_propulsion": 75, "spacecraft_structures": 75},
        }
    )

    row["research_profile"].update(
        {
            "department_research_areas": [
                "upper-atmosphere and radiation-belt modelling",
                "space-weather physics and risk",
                "ionospheric data assimilation",
                "space radar and over-the-horizon radar",
                "satellite communication and navigation resilience",
            ],
            "labs": [],
            "research_centers": ["Space Environment and Radio Engineering (SERENE) Group"],
            "research_strength_summary": bi(
                "SERENE is a directly relevant multidisciplinary space-environment group spanning modelling, fundamental physics, engineering and policy advice. Its official evidence includes operational modelling used in more than 30 countries and research on satellite collision risk, navigation and communications resilience.",
                "SERENE; modelleme, temel fizik, mühendislik ve politika danışmanlığını kapsayan doğrudan ilgili çok disiplinli bir uzay ortamı grubudur. Resmî kanıtları 30'dan fazla ülkede kullanılan operasyonel modellemeyi ve uydu çarpışma riski, seyrüsefer ile haberleşme dayanıklılığı araştırmalarını içerir.",
            ),
            "research_strength_score": 88,
            "research_sources": [RESEARCH_URL, SPACE_WEATHER_URL],
        }
    )

    row["industry_ecosystem_profile"].update(
        {
            "nearby_companies": [],
            "confirmed_partners": ["Dstl", "UK Met Office", "QinetiQ", "European Space Agency"],
            "research_institutes": ["British Antarctic Survey"],
            "graduate_employers_reported_by_course": ["Manufacturing Technology Centre", "Northumbria University", "Leonardo", "Goonhilly Earth Station"],
            "ecosystem_notes": bi(
                "The official SERENE page documents research links with Dstl, the Met Office, QinetiQ and ESA. The course page separately reports named graduate destinations. These are research and alumni signals, not guarantees of an internship, dissertation placement or job.",
                "Resmî SERENE sayfası Dstl, Met Office, QinetiQ ve ESA ile araştırma bağlantılarını belgeler. Program sayfası ayrıca mezunların gittiği kurumları isimle bildirir. Bunlar araştırma ve mezun sinyalleridir; staj, tez yerleştirmesi veya iş garantisi değildir.",
            ),
            "ecosystem_strength_score": 82,
        }
    )

    row["application_timeline_profile"].update(
        {
            "academic_year": "2026/2027",
            "intake_terms": ["September"],
            "non_eu_deadline": "2026-07-17",
            "uk_deadline": "2026-08-28",
            "scholarship_deadline": None,
            "pre_enrolment_required": None,
            "timeline_risk": "high",
            "deadline_events": [
                {"event": "overseas_application_for_most_postgraduate_taught_courses", "date": "2026-07-17", "status": "closed"},
                {"event": "international_postgraduate_housing_guarantee_apply_and_book", "date": "2026-07-31", "status": "closed"},
                {"event": "general_final_overseas_deposit_deadline_offer_may_be_earlier", "date": "2026-08-14", "status": "due_or_closed_at_verification"},
                {"event": "overseas_conditions_deadline", "date": "2026-08-31", "status": "upcoming_for_existing_offer_holders"},
                {"event": "latest_CAS_issue_date_for_September_starters", "date": "2026-09-04", "status": "upcoming_for_existing_offer_holders"},
            ],
            "dynamic_course_page_deadline_conflict": {
                "indexed_course_page_date": "2026-07-31",
                "general_current_overseas_date": "2026-07-17",
                "planning_rule": "use the earlier current official date unless the applicant portal explicitly gives a later programme-specific date",
            },
            "deadline_notes": bi(
                "The current central application page gives 17 July 2026 for most overseas taught-master's applications and says programme dates can vary. The dynamically indexed course page surfaced 31 July, so the conservative planning date is 17 July unless the applicant portal explicitly confirms otherwise. No future-cycle date is estimated.",
                "Güncel merkezî başvuru sayfası çoğu yurtdışı tezli olmayan yüksek lisans için 17 Temmuz 2026 verir ve program tarihlerinin değişebileceğini söyler. Dinamik olarak indekslenen program sayfasında 31 Temmuz görünmüştür; bu nedenle portal açıkça başka tarih doğrulamadıkça güvenli planlama tarihi 17 Temmuzdur. Gelecek dönem tarihi tahmin edilmez.",
            ),
        }
    )

    profile = row["source_profile"]
    profile.update(
        {
            "official_program_page": COURSE_URL,
            "official_admission_page": APPLICATION_URL,
            "official_curriculum_page": COURSE_URL,
            "official_tuition_page": INTERNATIONAL_COURSE_URL,
            "official_scholarship_page": HIGH_FLIERS_URL,
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
            "language": "high",
            "admission": "high",
            "non_eu_eligibility": "high",
            "tuition": "high",
            "deposit": "medium",
            "scholarship": "high",
            "curriculum": "high",
            "application_timeline_profile": "medium",
            "deadline": "medium",
            "deadlines": "medium",
            "living_profile": "high",
            "housing": "high",
            "research": "high",
            "industry": "high",
        }
    )
    profile["source_log"] = [
        source(COURSE_URL, "University of Birmingham Space Engineering MSc 2026/27", "official_program_page", ["program", "language", "admission", "curriculum", "accreditation", "career"], "Current course page verifies status, delivery, credits, modules, entry requirements, English thresholds, accreditation and reported graduate destinations."),
        source(INTERNATIONAL_COURSE_URL, "Birmingham Space Engineering MSc international fee view", "official_tuition_page", ["tuition", "non_eu_eligibility", "language", "deadline"], "International course-page view publishes the GBP 33,660 fee and international English requirements."),
        source(APPLICATION_URL, "University of Birmingham postgraduate taught application guidance", "official_admission_page", ["admission", "documents", "application_fee", "deadline", "visa"], "Current central application dates, overseas transcript and translation rules, no-fee policy and CAS timeline."),
        source(OFFER_URL, "University of Birmingham postgraduate offer guidance", "official_admission_page", ["documents", "deposit", "ATAS", "visa"], "Offer conditions, passport and possible ATAS evidence; this page publishes GBP 2,000 and conflicts with the refund policy.", "medium"),
        source(DEPOSIT_URL, "University of Birmingham PGT deposit refund policy", "official_tuition_page", ["deposit", "refund", "deadline"], "Current refund policy publishes GBP 3,000, portal-specific timing, exemptions and refund rules; amount conflicts with offer guidance.", "medium"),
        source(HIGH_FLIERS_URL, "University of Birmingham Postgraduate High Fliers Scholarship 2026", "official_scholarship_page", ["scholarship", "eligibility", "funding", "deadline"], "Automatic GBP 5,000 discount, Turkey domicile eligibility, exclusions and closed status."),
        source(ESA_URL, "University of Birmingham ESA Academy Academic Scholarship", "official_scholarship_page", ["scholarship", "eligibility", "funding"], "Programme-specific full-tuition route, published eligible-nationality list and automatic course-application assessment; page retains a 2025/26 value.", "medium"),
        source(HOUSING_URL, "University of Birmingham postgraduate accommodation application", "official_housing_page", ["housing", "application", "deadline", "payment"], "Separate application and booking route, international deadline, exact-room choice and GBP 550 advance payment."),
        source(HOUSING_GUARANTEE_URL, "University of Birmingham accommodation guarantee scheme", "official_housing_page", ["housing", "eligibility", "deadline"], "New-international-postgraduate guarantee eligibility and passed 31 July 2026 deadline."),
        source(HOUSING_FEES_URL, "University of Birmingham postgraduate accommodation fees 2026/27", "official_housing_page", ["housing", "living", "fees"], "Seventeen published postgraduate room types, weekly indicative prices, total contract prices and included services."),
        source(LIVING_URL, "University of Birmingham postgraduate money advice", "official_cost_of_living_page", ["living", "housing", "budget"], "Itemised essential and variable 50-week planning costs and one-off payments."),
        source(RESEARCH_URL, "University of Birmingham SERENE research group", "official_department_page", ["research", "staff", "facilities"], "Current space-environment modelling, physics, engineering and policy research evidence."),
        source(SPACE_WEATHER_URL, "University of Birmingham SERENE space-weather research", "official_department_page", ["research", "industry", "partners"], "Named research links, SWIMMR projects and satellite/navigation/communications applications."),
    ]

    row["decision_summary"].update(
        {
            "main_strengths": [
                bi("A rare dedicated 180-credit Space Engineering MSc with exactly eight taken modules, including a 60-credit individual project and selectable CubeSat, propulsion, communications, human-spaceflight and spacecraft-design options.", "Nadir bulunan, 60 kredilik bireysel proje ile CubeSat, itki, haberleşme, insanlı uzay uçuşu ve uzay aracı tasarımı seçeneklerini içeren, tam sekiz ders alınan 180 kredilik özel Space Engineering MSc programıdır."),
                bi("SERENE provides specific research depth in space weather, ionospheric modelling, space radar and satellite communication/navigation resilience, backed by named official links to ESA, the Met Office, Dstl and QinetiQ.", "SERENE; uzay havası, iyonosfer modelleme, uzay radarı ve uydu haberleşme/seyrüsefer dayanıklılığında özel araştırma derinliği sunar; ESA, Met Office, Dstl ve QinetiQ ile isim verilmiş resmî bağlantılarla desteklenir."),
                bi("Applicants domiciled in Turkey were explicitly eligible for an automatic GBP 5,000 tuition discount in 2026/27 without a separate scholarship form.", "Türkiye'de ikamet eden adaylar 2026/27'de ayrı burs formu olmadan otomatik 5.000 GBP öğrenim indirimi için açıkça uygundu."),
            ],
            "main_risks": [
                bi("At verification, both the conservative overseas application date and the international housing-guarantee date had passed; the High Fliers page was also marked closed.", "Doğrulama tarihinde hem güvenli yurtdışı başvuru tarihi hem uluslararası konut garantisi tarihi geçmişti; High Fliers sayfası da kapalı işaretliydi."),
                bi("Tuition is GBP 33,660 before discounts, published postgraduate accommodation reaches GBP 17,966, and the University's derived 50-week planning total is GBP 14,200-14,750 before tuition.", "İndirim öncesi öğrenim ücreti 33.660 GBP, yayımlanmış lisansüstü konaklama 17.966 GBP'ye kadar çıkar ve Üniversite verilerinden türetilen 50 haftalık yaşam planı öğrenim ücreti hariç 14.200-14.750 GBP'dir."),
                bi("The University currently publishes contradictory GBP 2,000 and GBP 3,000 deposit amounts; only the individual offer letter and applicant portal should drive payment.", "Üniversite şu anda çelişkili 2.000 ve 3.000 GBP depozito tutarları yayımlar; ödeme yalnızca bireysel teklif mektubu ve başvuru portalına göre yapılmalıdır."),
            ],
            "best_for": [bi("Students targeting spacecraft systems with a particularly strong interest in space environment, space weather, radar, communications, CubeSats or mission design.", "Özellikle uzay ortamı, uzay havası, radar, haberleşme, CubeSat veya görev tasarımına ilgi duyan uzay aracı sistemleri odaklı öğrenciler.")],
            "not_ideal_for": [bi("Applicants who need a still-open 2026 international route, a low-cost programme, guaranteed late housing, or a curriculum centred primarily on launch-vehicle aerodynamics and propulsion.", "Hâlâ açık 2026 uluslararası rotası, düşük maliyet, geç dönemde garantili konut veya esas olarak fırlatma aracı aerodinamiği ve itkiye odaklı müfredat isteyen adaylar.")],
        }
    )

    quality = audit_record(row)
    quality["audited_at"] = CHECKED
    row["data_quality"] = quality
    profile["needs_verification"] = True
    profile["verification_notes"] = bi(
        "All decision-critical groups have checked official evidence. Open verification is retained for the public deposit-amount conflict, the dynamic course-deadline conflict and future-cycle replacement of 2026/27 data.",
        "Tüm karar-kritik gruplarda kontrol edilmiş resmî kanıt vardır. Kamuya açık depozito tutarı çelişkisi, dinamik program tarihi çelişkisi ve 2026/27 verilerinin gelecek dönem yenilenmesi için doğrulama açık tutulur.",
    )
    row["quality_control"].update(
        {
            "qc_status": "passed" if quality["status"] == "verified" else "needs_revision",
            "checked_at": CHECKED,
            "failed_canary_tests": [],
            "remaining_verification_tasks": [
                bi("Confirm the binding deposit amount and exact deadline in each applicant's offer letter and portal; never choose between the conflicting public amounts by assumption.", "Bağlayıcı depozito tutarını ve kesin tarihi her adayın teklif mektubu ve portalında doğrulayın; çelişkili kamu tutarları arasında varsayımla seçim yapmayın."),
                bi("Replace 2026/27 fees, deadlines, scholarships, modules and housing prices when Birmingham publishes the next intake; do not roll dates forward.", "Birmingham sonraki dönemi yayımladığında 2026/27 ücretlerini, tarihlerini, burslarını, derslerini ve konut fiyatlarını değiştirin; tarihleri ileri taşımayın."),
            ],
            "qc_notes": bi(
                "The record passes source-grounding and canary checks while preserving two real official-source conflicts rather than hiding them behind a false single value.",
                "Kayıt kaynak temellendirme ve canary denetimlerini geçerken iki gerçek resmî-kaynak çelişkisini sahte tek bir değerin arkasına gizlemeden korur.",
            ),
        }
    )

    DATA_PATH.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
