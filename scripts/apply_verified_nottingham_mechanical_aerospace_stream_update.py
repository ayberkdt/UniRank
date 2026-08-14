"""Apply verified 2026/27 Nottingham Mechanical Engineering MSc data."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from unirank.core.integrity import audit_record


DATA_PATH = ROOT / "data_base" / "ingiltere.json"
RECORD_ID = "university-of-nottingham"
CHECKED = "2026-08-14"
COURSE_URL = "https://www.nottingham.ac.uk/pgstudy/course/taught/2026/mechanical-engineering-msc"
FEE_URL = "https://www.nottingham.ac.uk/pgstudy/course/taught/mechanical-engineering-msc"
APPLICATION_URL = "https://www.nottingham.ac.uk/pgstudy/how-to-apply/taught.aspx"
TURKEY_URL = "https://www.nottingham.ac.uk/studywithus/international-applicants/country-info/countryinformation/turkey.aspx"
DEPOSIT_URL = "https://www.nottingham.ac.uk/fabs/finance/frequentlyaskedquestions/cas-deposits.aspx"
SCHOLARSHIP_URL = "https://www.nottingham.ac.uk/studywithus/international-applicants/scholarships-funding-finance/international-postgraduate-scholarships.aspx"
HOUSING_URL = "https://www.nottingham.ac.uk/student-living/terms-and-conditions.aspx"
HOUSING_OPTIONS_URL = "https://www.nottingham.ac.uk/student-living/options/index.aspx"
RIVERSIDE_URL = "https://www.nottingham.ac.uk/accommodation/options/riverside-point"
DAGFA_URL = "https://www.nottingham.ac.uk/accommodation/options/dagfa-hall"
VISA_FUNDING_URL = "https://www.nottingham.ac.uk/studywithus/international-applicants/visa-help/student-route/funding.aspx"
IAT_URL = "https://www.nottingham.ac.uk/aerospace/"
PROPULSION_URL = "https://www.nottingham.ac.uk/aerospace/research/futurepropulsion/index.aspx"
UTC_URL = "https://www.nottingham.ac.uk/utc/"


def bi(en: str, tr: str) -> dict[str, str]:
    return {"en": en, "tr": tr}


def source(
    url: str,
    title: str,
    source_type: str,
    fields: list[str],
    note: str,
    confidence: str = "high",
) -> dict:
    return {
        "url": url,
        "title": title,
        "source_type": source_type,
        "access_status": "ok",
        "last_checked": CHECKED,
        "relevant_fields": fields,
        "confidence": confidence,
        "notes": bi(
            note,
            "Resmî kaynak belirtilen alanlar, tarihler ve kapsam sınırları için doğrudan kontrol edildi.",
        ),
    }


def main() -> None:
    rows = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    matches = [row for row in rows if row.get("id") == RECORD_ID]
    if len(matches) != 1:
        raise RuntimeError(f"Expected one {RECORD_ID!r} record; found {len(matches)}")
    row = matches[0]

    row.update(
        {
            "program_name": "Mechanical Engineering MSc",
            "program_degree": "MSc",
            "degree_level": "Master",
            "duration_years": 1,
            "ects": None,
            "uk_credits": 180,
            "programme_stream": "Aerospace",
            "programme_fit_class": "adjacent_aerospace_stream_not_dedicated_space_degree",
            "program_url": COURSE_URL,
            "program_status": "active",
            "teaching_language": ["English"],
            "relevance_status": "weak",
        }
    )

    row["eligibility_profile"].update(
        {
            "eligible_for_non_eu": True,
            "required_previous_degree": "A 2:1 BEng, BSc or international equivalent in a relevant subject",
            "accepted_backgrounds": ["mechanical engineering", "automotive engineering", "manufacturing engineering", "aerospace engineering", "other relevant engineering"],
            "alternative_background_policy": "Non-engineering applicants may be considered individually with at least a high 2:1 (65% or international equivalent), strong academic credentials and motivation",
            "turkey_degree_guidance": {
                "qualification": "Lisans Diplomasi",
                "typical_2_1_equivalent_gpa_out_of_4": 3.0,
                "status": "country_guidance_not_an_individual_admission_guarantee",
                "possible_flexibility": "requirements vary by university and course; higher grades may be required and prestigious-university flexibility may apply",
            },
            "admission_mode": "individual_application_review",
            "admission_risk": "medium",
            "required_documents": ["online_application", "degree_certificate_if_completed", "final_or_current_transcript"],
            "conditionally_requested_documents": ["two_references_including_one_academic", "personal_statement", "CV", "education_clarifications"],
            "references_required": None,
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
                "The course explicitly accepts international equivalents and gives a Student-route path for full-time study. Degree certificate and transcript are always listed; references, a statement and CV depend on the course or an admissions follow-up and are not marked universally compulsory. GRE is absent from the checked requirements, not declared prohibited.",
                "Program uluslararası denklikleri açıkça kabul eder ve tam zamanlı eğitim için Student-route yolu verir. Diploma ve transkript her zaman listelenir; referans, niyet metni ve CV programa veya ek kabul talebine bağlıdır ve herkese zorunlu işaretlenmez. GRE kontrol edilen koşullarda yoktur; yasak olduğu iddia edilmez.",
            ),
        }
    )

    row["language_profile"].update(
        {
            "teaching_language": ["English"],
            "teaching_languages": ["English"],
            "english_required": True,
            "english_level_required": "IELTS 6.0 overall with no element below 5.5, or an accepted equivalent",
            "minimum_scores": {"ielts": {"overall": 6.0, "each_element": 5.5}},
            "accepted_equivalents_named_without_course_specific_scores": ["TOEFL iBT", "Pearson PTE", "GCSE English", "IB English", "O level English"],
            "academic_qualification_may_be_accepted_as_evidence": True,
            "pre_sessional_available": True,
            "language_risk": "medium",
            "verification_notes": bi(
                "The course publishes an IELTS threshold and names accepted alternatives without publishing their course-specific scores on the course page. Successful presessional completion can meet the condition; no unstated equivalent scores are invented.",
                "Program IELTS eşiğini ve program sayfasında puanlarını vermeden kabul edilen alternatifleri yayımlar. Başarılı akademik İngilizce hazırlığı koşulu karşılayabilir; belirtilmeyen eşdeğer puanlar uydurulmaz.",
            ),
        }
    )

    row["cost_profile"].update(
        {
            "academic_year": "2026/2027",
            "tuition_basis": "official_published_foreign_currency",
            "tuition_gbp_full_programme": 33000,
            "tuition_non_eu_full_program": {"amount": 33000, "currency": "GBP", "basis": "full_time_12_month_programme", "academic_year": "2026/2027"},
            "student_visa_cas_deposit_gbp": 4500,
            "deposit_stage": "after_firmly_accepting_an_unconditional_offer",
            "deposit_deducted_from_tuition": True,
            "deposit_exemptions": ["full University scholarship", "full recognised sponsorship", "full-fee US Federal Student Aid loan", "eligible integrated CELE-plus-master's CAS route"],
            "programme_additional_costs": "No course-specific additional costs beyond tuition and living expenses; department provides lab and safety equipment and funds field trips",
            "source_notes": bi(
                "The 2026 international fee is GBP 33,000. Student-visa applicants starting from August 2026 pay a GBP 4,500 CAS deposit after an unconditional accepted offer unless an official exemption applies. No EUR conversion is stored.",
                "2026 uluslararası ücreti 33.000 GBP'dir. Ağustos 2026'dan sonra başlayan Student vizesi adayları, resmî muafiyet yoksa koşulsuz kabul edilmiş tekliften sonra 4.500 GBP CAS depozitosu öder. EUR dönüşümü tutulmaz.",
            ),
        }
    )

    row["scholarship_profile"].update(
        {
            "regional_scholarship_available": True,
            "regional_scholarship_name": "International Postgraduate Masters Scholarship",
            "non_eu_eligible": True,
            "scholarship_deadline": None,
            "scholarship_application_url": SCHOLARSHIP_URL,
            "application_mode": "automatic",
            "automatic_consideration": True,
            "separate_application_required": False,
            "opportunities": [
                {
                    "name": "International Postgraduate Masters Scholarship",
                    "academic_year": "2026/2027",
                    "award": {"amount": 3000, "currency": "GBP", "type": "tuition_fee_discount"},
                    "application_mode": "automatic_on_enrolment",
                    "separate_application_required": False,
                    "turkey_eligible": True,
                    "eligibility": ["international fee payer", "first year of a full-time UK-campus postgraduate taught MSc", "self-funded", "no other University award or external sponsorship"],
                    "exclusions": ["Kaplan University of Nottingham International College progression", "Digital Pathways progression", "another University award", "external sponsorship"],
                    "application_deadline": None,
                    "status": "active_for_2026_eligible_enrolments",
                    "illustrative_net_tuition_gbp": 30000,
                    "net_tuition_calculation": "33000 - 3000; derived arithmetic from official published amounts",
                    "source_url": SCHOLARSHIP_URL,
                }
            ],
            "funding_notes": bi(
                "The 2026 GBP 3,000 award is automatic on enrolment for eligible international, self-funded UK-campus taught-master's students and requires no scholarship form. It replaces the old regional awards, so the obsolete Middle East and Turkey award is not presented as a separate current opportunity.",
                "2026'daki 3.000 GBP ödül, uygun uluslararası, kendi finansmanını sağlayan Birleşik Krallık kampüsü tezli olmayan yüksek lisans öğrencilerine kayıtta otomatik verilir ve burs formu gerektirmez. Eski bölgesel ödüllerin yerini aldığı için eski Middle East and Turkey bursu ayrı güncel fırsat gibi gösterilmez.",
            ),
            "verification_notes": bi(
                "Turkey is covered through the all-international-students route, subject to fee status, study mode and funding exclusions; nationality alone does not override those conditions.",
                "Türkiye, tüm uluslararası öğrenciler rotasıyla kapsanır; ücret statüsü, eğitim biçimi ve finansman istisnaları geçerlidir. Yalnız vatandaşlık bu koşulları geçersiz kılmaz.",
            ),
        }
    )

    row["living_profile"].update(
        {
            "city_cost_level": "official_student_budget_available",
            "monthly_living_cost_gbp_per_month_min": 800,
            "monthly_living_cost_gbp_per_month_max": 1200,
            "living_cost_gbp_per_year_min": 9600,
            "living_cost_gbp_per_year_max": 14400,
            "living_cost_period_months": 12,
            "living_cost_scope": "typical student spending including accommodation, food and transport",
            "housing_difficulty": "low_if_guarantee_conditions_are_met",
            "living_risk": "medium",
            "housing_access": "guaranteed",
            "housing_application_separate": True,
            "housing_guarantee": {
                "available": True,
                "scope": "first year in University-arranged accommodation; international students can retain a course-duration guarantee through annual returner applications",
                "conditions": ["accept the course offer", "accept the accommodation licence or tenancy and terms by the residential-offer-letter deadline"],
                "application_deadline": None,
                "deadline_basis": "individual residential offer letter",
            },
            "housing_options": ["catered halls", "self-catered halls", "shared bathroom", "en-suite", "studio", "University-arranged partner accommodation"],
            "official_rent_items": [
                {"residence": "Riverside Point", "room_type": "Large Standard Double En-suite", "weekly_from_gbp": 158, "contract_weeks": 51, "published_total_gbp": 7803, "source_url": RIVERSIDE_URL},
                {"residence": "Dagfa House", "room_type": "Studio", "weekly_from_gbp": 291, "contract_weeks": 51, "published_total_gbp": 14591.57, "source_url": DAGFA_URL},
            ],
            "housing_budget_gbp_per_year_min": 7803,
            "housing_budget_gbp_per_year_max": 14591.57,
            "ukvi_maintenance_requirement": {"amount_per_month_gbp": 1171, "months": 9, "total_gbp": 10539, "scope": "visa financial evidence, not an actual-spending forecast"},
            "verification_notes": bi(
                "The University estimates GBP 800-1,200 per month including accommodation, food and transport. First-year University-arranged housing is guaranteed when offer and residential-contract conditions are met; no universal public application date is stated, so the individual residential offer controls. Two current 51-week room examples are retained rather than implying every hall is postgraduate-available.",
                "Üniversite konaklama, yemek ve ulaşım dâhil ayda 800-1.200 GBP tahmin eder. Teklif ve konut sözleşmesi koşulları karşılanırsa ilk yıl Üniversite aracılı konut garantilidir; herkese açık tek tarih yayımlanmadığından bireysel konut teklifi belirleyicidir. Her yurdun lisansüstüne açık olduğunu varsaymak yerine iki güncel 51 haftalık oda örneği tutulur.",
            ),
        }
    )

    row["curriculum_profile"].update(
        {
            "tracks": ["Advanced Mechanical Engineering", "Aerospace", "Automotive", "Manufacturing"],
            "selected_track": "Aerospace",
            "mandatory_courses": [
                "Masters Engineering Research and Communication (20 credits)",
                "Integrated Systems Analysis (10 credits)",
                "Engineering Design (20 credits)",
                "Individual Postgraduate Project (60 credits)",
                "one of Finite Element Analysis or Computational Fluid Dynamics (20 credits)",
                "Fundamentals of Aerospace Engineering (10 credits)",
                "Aerodynamics (10 credits)",
                "Aerospace Manufacturing: Airframes and Aeroengines (10 credits)",
            ],
            "elective_courses": [
                "Turbulence and Turbulent Flows (10)", "Fundamentals of Aerospace Engineering (10)", "Advanced Powertrain Engineering (10)", "Automotive Technology (10)", "Computer Modelling Techniques (20)", "Fibre Reinforced Composites Manufacturing (10)", "Computational Fluid Dynamics (20)", "Finite Element Analysis (20)", "Technologies for the Hydrogen Economy (10)", "Additive Manufacturing and 3D Printing (10)", "Aerospace Manufacturing: Airframes and Aeroengines (10)", "Materials for Low Carbon Transport (10)", "Digital Manufacturing (10)", "Flexible Manufacturing Systems (10)",
            ],
            "common_core_credits": 110,
            "selected_analysis_module_credits": 20,
            "aerospace_stream_compulsory_credits": 30,
            "elective_credits": 20,
            "total_uk_credits": 180,
            "mandatory_course_count_including_one_selected_analysis_module": 8,
            "published_elective_option_count": 14,
            "exact_elective_selection_count": None,
            "elective_selection_course_count_min": 1,
            "elective_selection_course_count_max": 2,
            "total_modules_taken_min": 9,
            "total_modules_taken_max": 10,
            "thesis_required": True,
            "research_project_credits": 60,
            "internship_required": False,
            "space_curriculum_depth": "introductory_only_within_fundamentals_module",
            "explicit_space_content": "brief overview of Astronauts and Space",
            "accreditation_status": "accredited",
            "accrediting_bodies": ["Engineering Accreditation Board", "Institution of Mechanical Engineers", "Royal Aeronautical Society", "Institution of Engineering and Technology", "Institution of Engineering Designers on behalf of the Engineering Council"],
            "professional_recognition": "fully meets the academic requirement for Chartered Engineer registration",
            "curriculum_url": COURSE_URL,
            "verification_notes": bi(
                "The Aerospace stream totals 180 UK credits: 110 common core, one 20-credit analysis choice, 30 aerospace-stream credits and 20 elective credits. Students take nine or ten modules because the 20 elective credits can be one 20-credit or two 10-credit modules. The published elective list is indicative and subject to timetable restrictions. Space content is only a brief introductory topic; this is not a spacecraft-systems MSc.",
                "Aerospace akışı 180 UK kredisine ulaşır: 110 ortak çekirdek, bir 20 kredilik analiz seçimi, 30 havacılık akış kredisi ve 20 seçmeli kredi. Seçmeli 20 kredi bir 20 kredilik veya iki 10 kredilik ders olabildiğinden öğrenci dokuz ya da on ders alır. Yayımlanan seçmeli liste gösterge niteliğindedir ve program çakışmalarına tabidir. Uzay içeriği yalnızca kısa bir giriş konusudur; bu bir uzay aracı sistemleri MSc'si değildir.",
            ),
        }
    )

    row["category_profile"].update(
        {
            "primary_categories": ["mechanical_engineering", "aerospace_engineering"],
            "secondary_categories": ["aerodynamics_and_cfd", "aerospace_manufacturing", "structures_and_fea", "propulsion"],
            "subcategories": ["airframes", "aeroengines", "turbulence", "composites", "finite_element_analysis"],
            "normalized_tags": ["mechanical_engineering", "aerospace_stream", "aerodynamics", "computational_fluid_dynamics", "finite_element_analysis", "aerospace_manufacturing", "airframes", "aeroengines"],
            "category_scores": {"mechanical_engineering": 95, "aerospace_engineering": 78, "aerodynamics_and_cfd": 85, "aerospace_manufacturing": 90, "structures_and_fea": 80, "propulsion": 65, "space_engineering": 20},
        }
    )

    row["research_profile"].update(
        {
            "department_research_areas": ["aerospace manufacturing", "aerospace materials and structures", "whole aircraft", "future propulsion and systems", "space", "aerospace operations"],
            "labs": ["Aerospace Technology Centre", "large closed-return wind tunnel", "Hydrogen Propulsion Systems Lab", "power electronics and electrical machines test facilities", "Rolls-Royce UTC laboratories"],
            "research_centers": ["Institute for Aerospace Technology", "Rolls-Royce UTC in Gas Turbine Transmission Systems", "Rolls-Royce UTC in Manufacturing and On-Wing Technology"],
            "research_strength_summary": bi(
                "The institution has substantial aerospace and some space research capacity: IAT reports more than 70 externally funded projects worth over GBP 75 million, while Future Propulsion covers aircraft and satellite propulsion, CFD, electrical systems and a large wind tunnel. This research strength does not turn the MSc's brief space topic into a dedicated space curriculum.",
                "Kurum önemli havacılık ve kısmen uzay araştırma kapasitesine sahiptir: IAT 75 milyon GBP üzeri değerde 70'ten fazla dış finansmanlı proje bildirir; Future Propulsion uçak ve uydu itkisi, HAD, elektrik sistemleri ve büyük rüzgâr tünelini kapsar. Bu araştırma gücü MSc'deki kısa uzay konusunu özel uzay müfredatına dönüştürmez.",
            ),
            "research_strength_score": 90,
            "research_sources": [IAT_URL, PROPULSION_URL, UTC_URL],
        }
    )

    row["industry_ecosystem_profile"].update(
        {
            "nearby_companies": [],
            "confirmed_partners": ["Rolls-Royce"],
            "research_institutes": ["Institute for Aerospace Technology", "Aerospace Technology Centre"],
            "graduate_employers_reported_by_course": ["Airbus", "Rolls-Royce", "BAE Systems", "Jaguar Land Rover", "Tata Steel", "Ford"],
            "ecosystem_notes": bi(
                "Rolls-Royce collaboration is directly verified through two long-running University Technology Centres. Course-page graduate destinations are kept separately from partnerships. Neither is a promise of an internship, project allocation or job.",
                "Rolls-Royce iş birliği iki uzun süreli University Technology Centre üzerinden doğrudan doğrulanır. Program sayfasındaki mezun işverenleri ortaklıklardan ayrı tutulur. Hiçbiri staj, proje tahsisi veya iş vaadi değildir.",
            ),
            "ecosystem_strength_score": 90,
        }
    )

    row["application_timeline_profile"].update(
        {
            "academic_year": "2026/2027",
            "intake_terms": ["September"],
            "programme_start_date": "2026-09-21",
            "non_eu_deadline": "programme-specific date not published; official general window is usually 6-7 weeks before a standard late-September start",
            "application_deadline": "needs_confirmation_in_NottinghamHub_or_with_admissions",
            "scholarship_deadline": None,
            "pre_enrolment_required": None,
            "timeline_risk": "high",
            "deadline_events": [
                {"event": "international_application", "date": None, "status": "needs_confirmation", "official_rule": "usually 6-7 weeks before standard late-September start"},
                {"event": "meet_all_offer_conditions_and_receive_unconditional_offer", "date": "2026-09-07", "status": "upcoming_for_existing_applicants"},
                {"event": "pay_CAS_deposit", "date": "2026-09-11", "status": "upcoming_for_unconditional_offer_holders"},
                {"event": "latest_overseas_CAS_issue", "date": "2026-09-16", "status": "upcoming_for_eligible_offer_holders"},
                {"event": "programme_start", "date": "2026-09-21", "status": "upcoming"},
            ],
            "deadline_notes": bi(
                "No exact programme-specific application date was published on the checked course page. The University only gives a general six-to-seven-week window for standard late-September starts, so no calendar deadline is invented. The exact current application state must be confirmed in NottinghamHub or with admissions; the September conditions, deposit and CAS cut-offs apply only to existing applicants and offer holders.",
                "Kontrol edilen program sayfasında programa özgü kesin başvuru tarihi yayımlanmadı. Üniversite standart eylül sonu başlangıçları için yalnız altı-yedi haftalık genel pencere verir; bu nedenle takvim tarihi uydurulmaz. Güncel başvuru durumu NottinghamHub veya kabul biriminden doğrulanmalıdır; eylül koşul, depozito ve CAS tarihleri yalnız mevcut aday ve teklif sahipleri içindir.",
            ),
        }
    )

    profile = row["source_profile"]
    profile.update(
        {
            "official_program_page": COURSE_URL,
            "official_admission_page": APPLICATION_URL,
            "official_curriculum_page": COURSE_URL,
            "official_tuition_page": FEE_URL,
            "official_scholarship_page": SCHOLARSHIP_URL,
            "official_language_policy_page": COURSE_URL,
            "official_housing_page": HOUSING_URL,
            "official_cost_of_living_page": SCHOLARSHIP_URL,
            "official_department_page": IAT_URL,
            "last_verified": CHECKED,
        }
    )
    profile["field_confidence"].update(
        {
            "program_basic_info": "high", "language": "high", "admission": "high", "non_eu_eligibility": "high", "tuition": "high", "deposit": "high", "scholarship": "high", "curriculum": "high", "research_profile": "high", "industry_ecosystem_profile": "high", "application_timeline_profile": "medium", "deadline": "medium", "deadlines": "medium", "living_profile": "high", "housing": "high",
        }
    )
    profile["source_log"] = [
        source(COURSE_URL, "University of Nottingham Mechanical Engineering MSc 2026", "official_program_page", ["program", "language", "admission", "tuition", "curriculum", "accreditation", "career"], "Current 2026 course page verifies the Aerospace stream, duration, fee, entry and English requirements, full module structure, accreditation and graduate destinations."),
        source(FEE_URL, "University of Nottingham Mechanical Engineering MSc fee view", "official_tuition_page", ["tuition", "fees"], "Current evergreen course view directly publishes the GBP 33,000 international fee."),
        source(APPLICATION_URL, "University of Nottingham postgraduate taught application guidance", "official_admission_page", ["admission", "documents", "deadline", "deposit"], "Required core documents, conditionally requested evidence, official relative application window and deposit framework."),
        source(TURKEY_URL, "University of Nottingham Turkey entry guidance", "official_admission_page", ["admission", "non_eu_eligibility", "country_equivalence"], "Turkey-specific Lisans Diplomasi guidance and limits on interpreting the GPA table."),
        source(DEPOSIT_URL, "University of Nottingham taught-master's CAS deposit FAQ", "official_tuition_page", ["deposit", "deadline", "visa", "refund"], "GBP 4,500 amount, payment stage, exemptions and 2026 conditions/deposit/CAS dates."),
        source(SCHOLARSHIP_URL, "University of Nottingham International Postgraduate Masters Scholarship 2026", "official_scholarship_page", ["scholarship", "funding", "eligibility", "living"], "Automatic GBP 3,000 award, eligibility and exclusions plus the University's typical monthly student-spending range."),
        source(HOUSING_URL, "University of Nottingham accommodation guarantee terms 2026", "official_housing_page", ["housing", "eligibility", "deadline", "refund"], "First-year and international-student guarantee conditions and 2026 book-with-confidence cancellation date."),
        source(HOUSING_OPTIONS_URL, "University of Nottingham halls of residence", "official_housing_page", ["housing", "living", "options"], "Current arranged-accommodation inventory and published from-prices."),
        source(RIVERSIDE_URL, "University of Nottingham Riverside Point", "official_housing_page", ["housing", "living", "fees"], "Concrete 51-week en-suite example and total."),
        source(DAGFA_URL, "University of Nottingham Dagfa House", "official_housing_page", ["housing", "living", "fees"], "Concrete 51-week studio example and total."),
        source(VISA_FUNDING_URL, "University of Nottingham Student-visa funding requirements", "official_government_or_visa_page", ["visa", "living", "funding"], "Current GBP 1,171 monthly maintenance threshold, explicitly separated from actual spending."),
        source(IAT_URL, "University of Nottingham Institute for Aerospace Technology", "official_department_page", ["research", "facilities", "industry"], "Current aerospace and space research themes, project scale and institutional capacity."),
        source(PROPULSION_URL, "University of Nottingham Future Propulsion and Systems", "official_department_page", ["research", "facilities", "industry"], "Aircraft and satellite propulsion, CFD, wind-tunnel, hydrogen and electrical-system capabilities."),
        source(UTC_URL, "University of Nottingham Rolls-Royce University Technology Centres", "official_department_page", ["research", "industry", "partners"], "Direct evidence of the long-term Rolls-Royce research partnership and two UTC themes."),
    ]

    row["decision_summary"].update(
        {
            "main_strengths": [
                bi("The Aerospace stream provides a coherent aircraft-oriented route in aerodynamics, CFD or FEA, airframes, aeroengines and aerospace manufacturing, backed by a 60-credit project.", "Aerospace akışı aerodinamik, HAD veya FEA, hava aracı gövdeleri, uçak motorları ve havacılık üretiminde 60 kredilik projeyle desteklenen tutarlı uçak odaklı rota sunar."),
                bi("Nottingham has unusually strong aerospace research infrastructure and industry connectivity through IAT, dedicated propulsion and electrical facilities, and two Rolls-Royce UTCs.", "Nottingham; IAT, özel itki ve elektrik tesisleri ile iki Rolls-Royce UTC üzerinden olağandışı güçlü havacılık araştırma altyapısına ve sanayi bağlantısına sahiptir."),
                bi("Eligible Turkish/international self-funded MSc students receive an automatic GBP 3,000 tuition discount in 2026 with no separate scholarship application, and first-year arranged accommodation is guaranteed subject to contract conditions.", "Uygun Türk/uluslararası kendi finansmanını sağlayan MSc öğrencileri 2026'da ayrı burs başvurusu olmadan otomatik 3.000 GBP indirim alır; sözleşme koşullarına bağlı ilk yıl konut garantisi vardır."),
            ],
            "main_risks": [
                bi("This is officially a Mechanical Engineering MSc with an Aerospace stream, not a dedicated Aerospace or Space Engineering degree; explicit space teaching is only a brief introductory topic.", "Bu resmî olarak Aerospace akışlı Mechanical Engineering MSc'dir; özel Aerospace veya Space Engineering derecesi değildir ve açık uzay eğitimi yalnız kısa bir giriş konusudur."),
                bi("The programme-specific international application date is not published; only a general six-to-seven-week window exists, so current availability requires direct confirmation.", "Programa özgü uluslararası başvuru tarihi yayımlanmaz; yalnız genel altı-yedi haftalık pencere vardır, bu nedenle güncel açıklık doğrudan doğrulanmalıdır."),
                bi("Tuition is GBP 33,000 before the automatic discount and typical University-published living costs add GBP 9,600-14,400 over twelve months.", "Otomatik indirimden önce öğrenim 33.000 GBP'dir ve Üniversitenin yayımladığı tipik yaşam maliyeti on iki ayda 9.600-14.400 GBP ekler."),
            ],
            "best_for": [bi("Students seeking aircraft aerodynamics, CFD/FEA, structures, propulsion or aerospace manufacturing with excellent research and Rolls-Royce links, while accepting a general Mechanical Engineering degree title.", "Genel Mechanical Engineering derece adını kabul ederek güçlü araştırma ve Rolls-Royce bağlantılarıyla uçak aerodinamiği, HAD/FEA, yapılar, itki veya havacılık üretimi arayan öğrenciler.")],
            "not_ideal_for": [bi("Students prioritising orbital mechanics, GNC, spacecraft systems, mission design, satellite engineering or a degree title explicitly in space engineering.", "Yörünge mekaniği, GNC, uzay aracı sistemleri, görev tasarımı, uydu mühendisliği veya açıkça uzay mühendisliği derece adını önceliklendiren öğrenciler.")],
        }
    )

    quality = audit_record(row)
    quality["audited_at"] = CHECKED
    row["data_quality"] = quality
    profile["needs_verification"] = True
    profile["verification_notes"] = bi(
        "All decision-critical groups have checked official evidence. Verification remains open for the unpublished programme-specific application date, individual residential-offer deadline and future-cycle replacement of 2026/27 values.",
        "Tüm karar-kritik gruplarda kontrol edilmiş resmî kanıt vardır. Yayımlanmayan programa özgü başvuru tarihi, bireysel konut-teklif tarihi ve 2026/27 değerlerinin gelecek dönem yenilenmesi için doğrulama açık tutulur.",
    )
    row["quality_control"].update(
        {
            "qc_status": "passed" if quality["status"] == "verified" else "needs_revision",
            "checked_at": CHECKED,
            "failed_canary_tests": [],
            "remaining_verification_tasks": [
                bi("Confirm whether 2026 international applications remain open in NottinghamHub or with admissions; do not convert the relative window into an invented date.", "2026 uluslararası başvurularının açık olup olmadığını NottinghamHub veya kabul biriminden doğrulayın; göreli pencereyi uydurma tarihe çevirmeyin."),
                bi("Replace 2026/27 fees, modules, scholarship, deposit and housing data when the next intake is published.", "Sonraki dönem yayımlandığında 2026/27 ücret, ders, burs, depozito ve konut verilerini değiştirin."),
            ],
            "qc_notes": bi(
                "The record passes source-grounding while explicitly preventing strong institutional space research from being misread as a strong space curriculum.",
                "Kayıt kaynak temellendirmeyi geçerken güçlü kurumsal uzay araştırmasının güçlü uzay müfredatı olarak yanlış okunmasını açıkça önler.",
            ),
        }
    )

    DATA_PATH.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
