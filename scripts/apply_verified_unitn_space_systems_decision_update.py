"""Apply current official decision evidence to UniTrento Intelligent Mechatronics MSc."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from unirank.core.integrity import audit_record


DATA_PATH = ROOT / "data_base" / "italy.json"
RECORD_ID = "unitn_mechatronics_space"
CHECKED = "2026-08-14"

PROGRAM = "https://corsi.unitn.it/en/intelligent-mechatronics-engineering/programme/overview"
NON_EU = "https://corsi.unitn.it/en/intelligent-mechatronics-engineering/enrollment/admission-and-enrollment-non-europeans"
TRANSITION = "https://corsi.unitn.it/en/mechatronics-engineering"
ADMISSION_IT = "https://corsi.unitn.it/sites/cds/files/2025-12/bando-ammissione-lm-dii-non-eu-26-27.pdf"
ADMISSION_EN = "https://corsi.unitn.it/sites/cds/files/2025-12/admission-call-master-dii-26-27.pdf"
RANKING = "https://corsi.unitn.it/sites/cds/files/2026-05/ranking-eu-intelligent-mechatronics-engineering-26-27.pdf"
CURRICULUM = "https://corsi.unitn.it/sites/cds/files/2026-03/manifesto-lm-intelligent-mechatronics-engineering-26-27.pdf"
EU_ADMISSION = "https://corsi.unitn.it/en/intelligent-mechatronics-engineering/enrollment/admission-europeans-and-equivalents"
TUITION = "https://www.unitn.it/en/study/fees-scholarships-accommodation/tuition-fees"
SCHOLARSHIP = "https://www.unitn.it/en/study/fees-scholarships-accommodation/scholarships-and-awards/scholarships-international-students"
ADMISSION_POLICY = "https://www.unitn.it/en/international/coming-unitrento/admission-how-it-works"
HOUSING = "https://www.unitn.it/en/international/coming-unitrento/all-you-need-know/accommodation"
OPERA_RATES = "https://www.operauni.tn.it/en/alloggi-en/alloggi-on-campus-en/come-fare-per-en/tariffe-e-pagamenti-en/"
OPERA_2026_CALL = "https://www.operauni.tn.it/wp-content/uploads/Bando-2026-2027-2.pdf"
TRENT_FURLANI = "https://trent.operauni.tn.it/appartamenti/residenza-furlani-vela-trento-camere-per-studenti/"
TRENT_GRAZIOLI = "https://trent.operauni.tn.it/appartamenti/stanza-singola-in-posizione-strategica-per-studenti-disponibile-da-settembre/"
FACTSHEET = "https://www.unitn.it/sites/default/files/2026-03/Trento_Factsheet_26_27.pdf"
LAB = "https://www.disi.unitn.it/it/node/1533"
SPACE_PHD = "https://www.unitn.it/en/phd/space-science-and-technology"
SPACE_PHD_DII = "https://www.dii.unitn.it/en/news/1003"
SPACE_PHD_CALL = "https://www.unitn.it/sites/default/files/2026-06/SST_Call_42_ENG.pdf"


def bi(en: str, tr: str) -> dict[str, str]:
    return {"en": en, "tr": tr}


def source(
    url: str,
    title: str,
    source_type: str,
    fields: list[str],
    *,
    access_status: str = "ok",
    confidence: str = "high",
    notes: dict[str, str] | None = None,
) -> dict:
    return {
        "url": url,
        "title": title,
        "source_type": source_type,
        "access_status": access_status,
        "last_checked": CHECKED,
        "relevant_fields": fields,
        "confidence": confidence,
        "notes": notes
        or bi(
            "Current official source checked for the listed fields; unpublished values are not inferred.",
            "Listelenen alanlar için güncel resmî kaynak kontrol edildi; yayımlanmayan değerler türetilmez.",
        ),
    }


def update(row: dict) -> None:
    row.update(
        {
            "program_name": "Intelligent Mechatronics Engineering",
            "program_native_name": "Laurea magistrale in Intelligent Mechatronics Engineering",
            "program_degree": "Master of Science",
            "degree_level": "Master",
            "degree_class": "LM-33 R — Mechanical Engineering",
            "duration_years": 2,
            "ects": 120,
            "teaching_language": ["English"],
            "program_url": PROGRAM,
            "department": "Department of Industrial Engineering",
            "campus": "Povo, Trento",
            "program_status": "active",
            "relevance_status": "medium",
            "programme_fit_class": "adjacent_mechatronics_degree_with_space_systems_and_instruments_curriculum_not_aerospace_or_space_degree",
            "programme_transition": {
                "new_programme_first_intake": "2026/2027",
                "predecessor": "Mechatronics Engineering",
                "non_eu_transition_rule": "Successful 2026/27 applicants to the predecessor call are automatically enrolled in Intelligent Mechatronics Engineering.",
                "first_year_active_in_2026_27": True,
                "second_year_curricula_active_in_2026_27": False,
                "space_curriculum_delivery_status": "officially_planned_for_the_first_cohort_second_year_not_yet_delivered_in_2026_27",
            },
        }
    )

    row["eligibility_profile"].update(
        {
            "eligible_for_non_eu": True,
            "target_applicant_route": "non_eu_citizen_resident_outside_italy",
            "reserved_non_eu_places": 25,
            "required_previous_degree": bi(
                "A bachelor's degree of at least three years from an internationally recognised university in industrial engineering (including mechanical, mechatronics, chemical or materials), electronic/control/automation engineering, or a related industrial-engineering field, with basic mathematics and physics.",
                "Uluslararası tanınan bir üniversiteden en az üç yıllık; endüstri mühendisliği alanında (mekanik, mekatronik, kimya veya malzeme dâhil), elektronik/kontrol/otomasyon mühendisliğinde ya da ilgili bir endüstri mühendisliği alanında, temel matematik ve fizik içeren lisans derecesi.",
            ),
            "accepted_backgrounds": [
                "Mechanical Engineering",
                "Mechatronics Engineering",
                "Chemical Engineering",
                "Materials Engineering",
                "Electronic Engineering",
                "Control Engineering",
                "Automation Engineering",
                "related Industrial Engineering fields with mathematics and physics",
            ],
            "foreign_degree_assessment": "The committee compares foreign course content with the programme's disciplinary requirements; formal degree eligibility is verified after admission and pre-enrolment, and UniTrento may request verification/comparability statements.",
            "minimum_gpa": {
                "italian_equivalent_weighted_average": "23/30",
                "foreign_conversion": "Foreign averages are converted to the Italian 30-point scale by UniTrento; no Turkish 4.00-scale threshold is published.",
            },
            "degree_completion_deadline": "2026-06-30 for applicants graduating outside Italy",
            "ranking_or_selection": "limited_place_merit_ranking",
            "admission_mode": bi(
                "Document-based competitive selection for 25 non-EU places. Eligible applicants need at least 50/100; the committee may interview when the dossier is insufficient for assessment.",
                "25 AB-dışı kontenjan için belge temelli rekabetçi seçim. Uygun aday en az 50/100 almalıdır; dosya değerlendirme için yetersizse komite mülakat isteyebilir.",
            ),
            "selection_scoring": {
                "prior_degree_coherence_max": 30,
                "academic_record_and_activities_max": 60,
                "additional_languages_max": 10,
                "eligibility_threshold": 50,
                "total": 100,
            },
            "published_2026_27_competition_context": {
                "listed_application_entries": 129,
                "ranked_with_score": 113,
                "not_eligible_entries": 16,
                "initial_admitted": 25,
                "waiting_list": 35,
                "eligible_but_outside_initial_places": 35,
                "lowest_initially_admitted_score": 69,
                "scholarships_available": 2,
                "warning": "This is a descriptive result for the closed 2026/27 cycle, not a forecast or acceptance-rate guarantee for a later cycle.",
            },
            "application_fee_eur": 30,
            "place_confirmation_fee_eur": 100,
            "place_confirmation_fee_refundable": False,
            "place_confirmation_fee_counts_toward_tuition": False,
            "required_documents": [
                bi("Valid passport pages containing photo and personal data", "Fotoğraf ve kişisel bilgileri içeren geçerli pasaport sayfaları"),
                bi("Bachelor's certificate, or enrolment certificate with expected graduation date", "Lisans diploması veya beklenen mezuniyet tarihini içeren öğrenci belgesi"),
                bi("Transcript listing examinations, results and credits, including the grading scale", "Notlandırma ölçeği dâhil sınavları, sonuçları ve kredileri gösteren transkript"),
                bi("Official English or Italian translation when an original is in another language", "Belge başka dildeyse resmî İngilizce veya İtalyanca çeviri"),
                bi("Curriculum vitae et studiorum in English", "İngilizce akademik özgeçmiş"),
                bi("B2 English evidence covering the accepted route", "Kabul edilen yollardan B2 İngilizce kanıtı"),
                bi("If requested after admission: qualification verification and/or comparability statement", "Kabulden sonra istenirse yeterlilik doğrulama ve/veya karşılaştırılabilirlik belgesi"),
            ],
            "cv_required": True,
            "motivation_letter_required": False,
            "recommendation_required": False,
            "portfolio_required": False,
            "interview_required": "conditional_if_documents_are_insufficient",
            "test_required": False,
            "gre": {
                "policy": "not_listed_as_required_or_scored_in_checked_2026_27_programme_sources",
                "test_type": None,
                "minimum_scores": {},
                "recommended_scores": {},
                "validity_rule": None,
                "waiver_rules": [],
                "source_ids": [NON_EU, ADMISSION_IT],
            },
            "notes_for_turkish_students": bi(
                "A Turkish citizen resident in Turkey uses this non-EU route. UniTrento publishes no direct Turkish 4.00 GPA conversion; course content, the foreign average and degree eligibility are assessed by the university.",
                "Türkiye'de ikamet eden Türk vatandaşı bu AB-dışı yolu kullanır. UniTrento doğrudan 4,00 üzerinden Türkiye not dönüşümü yayımlamaz; ders içeriği, yabancı not ortalaması ve diploma uygunluğu üniversite tarafından değerlendirilir.",
            ),
            "admission_risk": "high",
        }
    )

    row["language_profile"].update(
        {
            "teaching_language": ["English"],
            "teaching_languages": ["English"],
            "primary_teaching_language": "English",
            "english_required": True,
            "english_required_at_entry": True,
            "english_level_required": "B2 CEFR in all four skills by the application deadline",
            "accepted_english_evidence": [
                "internationally recognised English certificate",
                "official statement that the entire bachelor's or master's programme was taught in English",
                "certified university B2-or-higher examination covering all four skills",
                "citizenship of a country where English is an official language",
                "self-declaration of graduation in an English-speaking country on the programme page",
            ],
            "medium_of_instruction_accepted": True,
            "accepted_english_tests": [],
            "minimum_scores": {},
            "italian_required": False,
            "italian_needed_for_life_or_internship": bi(
                "Italian is not an academic entry requirement in the checked route, but it can materially widen local internship, housing and daily-life options.",
                "Kontrol edilen yolda İtalyanca akademik giriş koşulu değildir; ancak yerel staj, konut ve günlük yaşam seçeneklerini önemli ölçüde genişletebilir.",
            ),
            "language_risk": "medium",
            "verification_notes": bi(
                "The official sources require B2 but do not publish programme-specific IELTS, TOEFL or PTE minimum scores. No score is inferred from B2.",
                "Resmî kaynaklar B2 ister ancak programa özgü IELTS, TOEFL veya PTE taban puanı yayımlamaz. B2 düzeyinden puan türetilmez.",
            ),
        }
    )

    row["cost_profile"].update(
        {
            "academic_year": "2026/2027",
            "currency": "EUR",
            "tuition_eur_per_year_min": 0,
            "tuition_eur_per_year_max": 4500,
            "tuition_eur_per_year_estimated": None,
            "maximum_non_eu_system_fee_eur": 6000,
            "total_academic_cost_eur_per_year_estimated": None,
            "tuition_basis": "first_year_admission_score_then_second_year_earned_ects",
            "first_year_tuition_bands": [
                {"score_min": 90, "score_max": 100, "tuition_eur": 0},
                {"score_min": 70, "score_max_exclusive": 90, "tuition_eur": 1000},
                {"score_min": 60, "score_max_exclusive": 70, "tuition_eur": 2000},
                {"score_min": 50, "score_max_exclusive": 60, "tuition_eur": 4500},
            ],
            "second_year_tuition_bands": [
                {"ects_by": "2027-08-10", "ects_min": 42, "tuition_eur": 0},
                {"ects_by": "2027-08-10", "ects_min": 36, "ects_max_exclusive": 42, "tuition_eur": 1000},
                {"ects_by": "2027-08-10", "ects_min": 24, "ects_max_exclusive": 36, "tuition_eur": 2000},
                {"ects_by": "2027-08-10", "ects_min": 6, "ects_max_exclusive": 24, "tuition_eur": 4500},
                {"ects_by": "2027-08-10", "ects_max_exclusive": 6, "tuition_eur": 6000},
            ],
            "application_fee_eur": 30,
            "place_confirmation_fee_eur": 100,
            "place_confirmation_fee_included_in_tuition": False,
            "tuition_items": [
                {"name": "First-year tuition", "amount_eur": None, "range_eur": [0, 4500], "basis": "final admission score for an admitted applicant", "source_url": ADMISSION_IT},
                {"name": "Second-year tuition", "amount_eur": None, "range_eur": [0, 6000], "basis": "ECTS earned by 10 August 2027", "source_url": ADMISSION_IT},
                {"name": "Application fee", "amount_eur": 30, "refundable": False, "source_url": ADMISSION_IT},
                {"name": "Place-confirmation fee", "amount_eur": 100, "refundable": False, "included_in_tuition": False, "source_url": ADMISSION_IT},
            ],
            "verification_notes": bi(
                "The binding Italian call contains a word-number typo beside the annual maximum, but its numeric maximum and both detailed tables consistently support EUR 6,000. For an initially admissible first-year score of at least 50, the published first-year range is EUR 0-4,500; EUR 6,000 is retained as the system/low-credit second-year ceiling, not invented as a normal first-year band.",
                "Bağlayıcı İtalyanca çağrıda yıllık azami tutarın yanında yazıyla sayı hatası vardır; ancak rakamsal azami tutar ve iki ayrıntılı tablo 6.000 EUR'yu tutarlı biçimde destekler. İlk yıl için kabul edilebilir en az 50 puanda yayımlanan aralık 0-4.500 EUR'dur; 6.000 EUR normal ilk yıl dilimi gibi eklenmez, sistem ve düşük kredili ikinci yıl tavanı olarak tutulur.",
            ),
        }
    )

    row["scholarship_profile"].update(
        {
            "regional_scholarship_available": False,
            "non_eu_eligible": True,
            "application_mode": "automatic",
            "automatic_consideration": True,
            "separate_application_required": False,
            "scholarship_deadline": None,
            "scholarship_trigger_deadline": "2026-03-04T12:00:00+01:00",
            "scholarship_application_url": NON_EU,
            "merit_scholarships": ["UniTrento scholarship for non-EU citizens living outside Italy"],
            "tuition_waivers": ["Scholarship holders are exempt from tuition for the same academic year"],
            "opportunities": [
                {
                    "name": "UniTrento scholarship for international students",
                    "target_group": "non-EU citizens living outside Italy",
                    "application_mode": "automatic_from_programme_ranking",
                    "separate_application_required": False,
                    "minimum_ranking_score_for_possible_award": 70,
                    "award_count_for_intelligent_mechatronics_2026_27": 2,
                    "award_eur_per_year": {"female_student_in_stem": 8500, "all_other_students": 7200},
                    "tuition_waiver": True,
                    "limited_number": True,
                    "payment": ["first instalment by December", "second instalment by May if the January-February credit condition is met; otherwise possible in October after 42 ECTS by 10 August"],
                    "maximum_duration_years_for_masters": 2,
                    "renewal": "Annual merit check; for an English-taught programme, more than 42 ECTS by 10 August confirms the scholarship and fee exemption.",
                    "incompatible_with": ["MAECI", "Università a colori / Unicolor", "Invest Your Talent in Italy"],
                    "source_urls": [NON_EU, ADMISSION_IT, RANKING, SCHOLARSHIP],
                }
            ],
            "funding_notes": bi(
                "No separate UniTrento scholarship form is required for this target route. The closed 2026/27 programme ranking had only two awards for 25 initial places, so a score above 70 created eligibility for possible reassignment but did not guarantee funding.",
                "Hedef yol için ayrı UniTrento burs formu gerekmez. Kapanan 2026/27 program sıralamasında 25 ilk kontenjana yalnızca iki burs vardı; bu nedenle 70 üzeri puan olası yeniden tahsis için uygunluk sağladı ancak bursu garanti etmedi.",
            ),
            "excluded_or_non_target_funding_routes": [
                {
                    "name": "Opera Universitaria 2026/27 income-based benefits call",
                    "reason": "The published recipient definition covers EU/associated-country citizens and non-EU citizens resident in Italy. It is not encoded as an application route for the target Turkey-resident non-EU applicant, whose UniTrento scholarship is instead automatic and merit-ranked.",
                    "source_url": OPERA_2026_CALL,
                }
            ],
        }
    )

    row["living_profile"].update(
        {
            "city_cost_level": "unknown",
            "average_room_rent_eur": None,
            "monthly_living_cost_eur_estimated": None,
            "monthly_living_cost_eur_min": None,
            "monthly_living_cost_eur_max": None,
            "housing_difficulty": "low_for_first_year_target_route_if_booking_instructions_are_followed;_unknown_after_first_year",
            "student_housing_available": True,
            "housing_access": "guaranteed",
            "housing_application_separate": False,
            "booking_required": True,
            "housing_guarantee": {
                "available": True,
                "scope": "first_academic_year_for_admitted_non_eu_degree_students",
                "free": False,
                "procedure": "The International Mobility Office sends a booking link before arrival.",
                "continuation_after_first_year": "not_guaranteed_in_checked_target_route_sources",
            },
            "living_risk": "medium",
            "official_rent_items": [
                {
                    "provider": "TRent — Opera Universitaria off-campus portal",
                    "residence": "Residenza Furlani, Vela",
                    "listing_snapshot_checked": CHECKED,
                    "room_examples": [
                        {"room_type": "shared room", "base_rent_eur_per_month": 280, "utilities_and_services_advance_eur_per_month": 100, "listed_total_before_semiannual_adjustment_eur_per_month": 380},
                        {"room_type": "shared room", "base_rent_eur_per_month": 320, "utilities_and_services_advance_eur_per_month": 100, "listed_total_before_semiannual_adjustment_eur_per_month": 420},
                        {"room_type": "single room", "base_rent_eur_per_month": 350, "utilities_and_services_advance_eur_per_month": 100, "listed_total_before_semiannual_adjustment_eur_per_month": 450},
                        {"room_type": "single room", "base_rent_eur_per_month": 420, "utilities_and_services_advance_eur_per_month": 100, "listed_total_before_semiannual_adjustment_eur_per_month": 520},
                    ],
                    "deposit_eur": 600,
                    "availability_status_on_page": "listed_as_available",
                    "source_url": TRENT_FURLANI,
                    "warning": "Current provider-hosted listing examples, not a market average, price guarantee or the reserved first-year on-campus rate.",
                },
                {
                    "provider": "TRent — Opera Universitaria off-campus portal",
                    "residence": "Via Grazioli private student listing",
                    "listing_snapshot_checked": CHECKED,
                    "room_type": "single room",
                    "base_rent_eur_per_month": 500,
                    "utilities_advance_eur_per_month": 100,
                    "listed_total_before_adjustment_eur_per_month": 600,
                    "deposit": "three monthly rents",
                    "minimum_stay_days": 365,
                    "availability_status_on_page": "listed_as_available",
                    "source_url": TRENT_GRAZIOLI,
                    "warning": "Current provider-hosted listing example, not a market average or guarantee.",
                },
                {
                    "provider": "Opera Universitaria",
                    "academic_year": "2026/2027",
                    "route": "income_and_merit_call_beneficiary_reduced_rate",
                    "double_room_eur_per_month": 190,
                    "single_room_eur_per_month": 230,
                    "security_deposit_eur": 360,
                    "checkout_fee_eur": 40,
                    "target_turkey_resident_route_applicable": False,
                    "reason_not_target_rate": "The 2026/27 call's recipient definition does not include a non-EU citizen resident outside Italy; the separate guaranteed international route does not publish its exact rent.",
                    "source_url": OPERA_2026_CALL,
                },
            ],
            "historical_provider_rate_reference": {
                "academic_year": "2025/2026",
                "reduced_call_beneficiary_double_eur_per_month": 190,
                "reduced_call_beneficiary_single_eur_per_month": 230,
                "other_student_collective_residence_double_eur_per_month": 330,
                "other_student_collective_residence_single_eur_per_month": 390,
                "security_deposit_eur": 360,
                "checkout_fee_eur": 40,
                "applicability_to_reserved_non_eu_first_year_route": "unknown",
                "use_as_current_2026_27_target_rent": False,
                "source_url": OPERA_RATES,
            },
            "housing_options": ["Opera Universitaria student housing reserved through the UniTrento international route", "private/off-campus housing found independently"],
            "housing_notes": bi(
                "The current programme page calls first-year on-campus accommodation guaranteed for admitted non-EU students, and central UniTrento pages say a place is reserved and a booking link is sent. It is paid housing. The exact 2026/27 rent for this reserved route is not published. Current official-provider off-campus examples span EUR 380-600 per month after listed utility advances, while the EUR 190/230 Opera reduced rates belong to a different income/merit call whose recipient definition does not cover the target applicant. None is converted into a market average or reserved-route price.",
                "Güncel program sayfası kabul edilen AB-dışı öğrenciye ilk yıl kampüs konutunu garantili olarak tanımlar; merkezi UniTrento sayfaları da yer ayrıldığını ve rezervasyon bağlantısı gönderildiğini söyler. Konut ücretlidir. Bu ayrılmış yolun kesin 2026/27 kirası yayımlanmamıştır. Resmî sağlayıcının güncel kampüs dışı örnekleri listelenen gider avanslarıyla aylık 380-600 EUR arasındadır; Opera'nın 190/230 EUR indirimli fiyatları ise alıcı tanımı hedef adayı kapsamayan farklı gelir/başarı çağrısına aittir. Hiçbiri piyasa ortalamasına veya ayrılmış yol fiyatına dönüştürülmez.",
            ),
            "private_housing_warning": bi(
                "UniTrento explicitly says it does not assist with finding private accommodation. No private-market average is stored from individual listings.",
                "UniTrento özel konut bulmaya yardım etmediğini açıkça belirtir. Tekil ilanlardan özel piyasa ortalaması tutulmaz.",
            ),
        }
    )

    first_year = [
        {"requirement": "Digital Manufacturing", "ects": 6},
        {"requirement": "AI and Embedded Systems", "ects": 15, "modules": ["Embedded Systems", "AI for Mechatronics"]},
        {"requirement": "Mechatronic Systems Analysis", "ects": 12, "modules": ["Dynamics and Vibration of Mechatronic Systems", "Modeling and Simulation of Mechatronic Systems"]},
        {"requirement": "Signal processing / optimisation choice", "ects": 6, "choose": 1, "options": ["Digital Signal Processing for Mechatronics", "Numerical Optimization and Optimal Control for Dynamical Systems"]},
        {"requirement": "Automatic Control", "ects": 6},
        {"requirement": "Mechanical Design for Mechatronics", "ects": 9},
        {"requirement": "Precision / industrial design choice", "ects": 6, "choose": 1, "options": ["Design of Precision Systems", "Design Methods for Industrial Engineering"]},
    ]
    space_options = [
        "Remote Sensing Systems and Image Analysis",
        "Spacecraft Sensors and Instrumentation",
        "Scientific Mission Design",
        "Space Structures and Advanced Applications",
        "AI and On-board Computing Design",
        "Space Mechanisms and Space Systems Engineering",
    ]
    row["curriculum_profile"].update(
        {
            "tracks": ["Mechanics", "Robotics and Intelligent Vehicles", "Space Systems and Instruments", "Electronics and Smart Energy Systems"],
            "specializations": ["Space Systems and Instruments"],
            "selected_track": "Space Systems and Instruments",
            "programme_structure": {
                "first_year_common_ects": 60,
                "first_year_top_level_requirement_count": 7,
                "first_year_selected_teaching_components_count": 9,
                "first_year_requirements": first_year,
                "second_year_space_curriculum_ects": 60,
                "second_year_space_subject_package_ects": 24,
                "second_year_space_subjects_choose": 4,
                "second_year_space_subject_options": space_options,
                "second_year_electives_count": 2,
                "second_year_electives_ects": 12,
                "second_year_internship_or_other_activities_ects": 6,
                "second_year_final_project_ects": 18,
                "planned_second_year_per_student_activity_count_including_thesis_and_internship": 8,
                "planned_total_top_level_requirement_count": 15,
                "exact_exam_count": None,
            },
            "mandatory_courses": ["Digital Manufacturing", "AI and Embedded Systems", "Mechatronic Systems Analysis", "Automatic Control", "Mechanical Design for Mechatronics"],
            "elective_courses": space_options,
            "space_course_options": space_options,
            "space_course_selection_count": 4,
            "space_curriculum_depth": "substantial_systems_instrumentation_remote_sensing_and_onboard_computing_but_no_verified_astrodynamics_or_propulsion_core",
            "thesis_required": True,
            "thesis_ects": 18,
            "internship_required": True,
            "internship_ects": 6,
            "lab_courses": [],
            "project_based_courses": ["Final Project"],
            "curriculum_url": CURRICULUM,
            "study_plan_url": CURRICULUM,
            "delivery_status": {
                "first_year_2026_27": "active",
                "second_year_2026_27": "inactive_for_the_new_programme_first_cohort",
                "space_track": "officially_defined_but_first_expected_delivery_when_the_2026_27_cohort_reaches_year_two",
            },
            "verification_notes": bi(
                "The official plan requires four of the six listed space subjects for 24 ECTS, not all six. Two additional electives, a 6-ECTS internship/other activity and an 18-ECTS final project complete year two. The document labels every second-year curriculum inactive in 2026/27 because this is a new programme; no claim of an already delivered Space Systems cohort is made.",
                "Resmî plan, listelenen altı uzay dersinin tamamını değil, 24 AKTS için dördünü ister. İki ek seçmeli, 6 AKTS staj/diğer etkinlik ve 18 AKTS bitirme projesi ikinci yılı tamamlar. Belge, program yeni olduğu için tüm ikinci yıl yollarını 2026/27'de pasif olarak işaretler; daha önce yürütülmüş Space Systems kohortu olduğu iddia edilmez.",
            ),
        }
    )

    row["category_profile"].update(
        {
            "primary_categories": ["mechatronics_engineering", "spacecraft_systems"],
            "secondary_categories": ["remote_sensing", "space_instrumentation", "onboard_computing", "space_mission_design"],
            "subcategories": ["space_sensors", "space_structures", "space_mechanisms", "embedded_systems", "artificial_intelligence"],
            "normalized_tags": ["mechatronics", "spacecraft systems", "remote sensing", "space instrumentation", "on-board AI", "space mechanisms", "space structures", "scientific mission design"],
            "category_scores": {},
        }
    )

    row["research_profile"].update(
        {
            "department_research_areas": [
                "mechatronic systems and instruments for space applications",
                "remote-sensing signal and image analysis",
                "Earth observation and planetary exploration data",
                "space sensors and instrumentation",
                "engineering and satellite platform technologies",
            ],
            "labs": [
                {
                    "name": "Sensing Technologies Educational Laboratory / Remote Sensing Laboratory",
                    "areas": ["multispectral and hyperspectral imaging", "SAR", "LiDAR", "radar sounding", "AI and machine learning for space-acquired data"],
                    "equipment": ["hyperspectral scanner", "LiDAR", "thermal camera", "radar sensors", "drone"],
                    "msc_access": "not_guaranteed_in_checked_sources",
                    "source_url": LAB,
                }
            ],
            "research_centers": ["National PhD Programme in Space Science and Technology coordinated by UniTrento"],
            "space_or_aerospace_projects": [
                "42nd-cycle PhD topic: Mechatronic systems and instruments for space applications",
                "42nd-cycle space engineering and satellite-platform research topics",
            ],
            "research_strength_summary": bi(
                "UniTrento has current, direct institutional space activity in sensing, Earth observation, instrumentation and satellite-platform technology, including a national Space Science and Technology PhD coordinated by the university. This strengthens the track's environment but does not guarantee an MSc thesis place, laboratory access or a specific supervisor.",
                "UniTrento; algılama, Dünya gözlemi, enstrümantasyon ve uydu platformu teknolojisinde güncel, doğrudan kurumsal uzay etkinliğine ve üniversitenin koordine ettiği ulusal Space Science and Technology doktorasına sahiptir. Bu ortam yolu güçlendirir; ancak yüksek lisans tez yeri, laboratuvar erişimi veya belirli danışmanı garanti etmez.",
            ),
            "research_strength_score": None,
            "research_sources": [LAB, SPACE_PHD, SPACE_PHD_DII, SPACE_PHD_CALL],
        }
    )

    row["industry_ecosystem_profile"].update(
        {
            "nearby_companies": [],
            "confirmed_partners": [
                {
                    "name": "Thales Alenia Space",
                    "scope": "Named in the current 42nd-cycle national Space Science and Technology PhD call for a UniTrento-linked space-mechatronics topic; this is research-ecosystem evidence, not a guaranteed MSc placement or programme-wide partnership benefit.",
                    "source_url": SPACE_PHD_CALL,
                }
            ],
            "research_institutes": ["Fondazione Bruno Kessler (FBK) — present in current UniTrento space-doctorate topics; MSc access not established"],
            "space_agencies_or_public_bodies": ["Italian Space Agency (ASI) — funds current doctorate topics; no MSc entitlement inferred"],
            "internship_possibility": "The degree reserves 6 ECTS for internship or other activities; placement and host are not guaranteed.",
            "thesis_with_industry_possibility": "possible_but_not_guaranteed",
            "career_relevance": "strong_for_space_instrumentation_sensors_embedded_and_systems_roles;weaker_for_astrodynamics_propulsion_and_classical_aerodynamics",
            "ecosystem_strength_score": None,
            "ecosystem_notes": bi(
                "Current official doctorate material proves an active space research network involving UniTrento, ASI, FBK and Thales Alenia Space. It does not prove automatic access for this master's cohort, so no internship or job-placement promise is encoded.",
                "Güncel resmî doktora materyali UniTrento, ASI, FBK ve Thales Alenia Space'i içeren etkin bir uzay araştırma ağını kanıtlar. Bu yüksek lisans kohortu için otomatik erişimi kanıtlamadığından staj veya işe yerleşme vaadi kodlanmaz.",
            ),
        }
    )

    row["application_timeline_profile"].update(
        {
            "academic_year": "2026/2027",
            "intake_terms": ["Autumn 2026"],
            "application_deadline": "2026-03-04T12:00:00+01:00",
            "non_eu_deadline": "2026-03-04T12:00:00+01:00",
            "eu_deadline": None,
            "scholarship_deadline": None,
            "ranking_publication_deadline": "2026-05-20",
            "degree_completion_deadline": "2026-06-30",
            "pre_enrolment_required": True,
            "universitaly_required": True,
            "universitaly_deadline": "within two weeks after place confirmation",
            "visa_sensitive_deadline": "2026-10-31",
            "enrollment_deadline": "communicated individually after ranking",
            "timeline_risk": "high",
            "deadline_events": [
                {"event": "non_eu_programme_and_automatic_scholarship_consideration", "deadline": "2026-03-04T12:00:00+01:00", "status": "closed", "source_url": NON_EU},
                {"event": "ranking_and_scholarship_assignment_publication", "deadline": "2026-05-20", "status": "published", "source_url": RANKING},
                {"event": "place_confirmation", "deadline": None, "status": "individual_email_deadline", "fee_eur": 100, "source_url": NON_EU},
                {"event": "universitaly_pre_enrolment", "deadline": "within two weeks after place confirmation", "status": "individual_relative_deadline", "source_url": NON_EU},
                {"event": "foreign_bachelor_completion", "deadline": "2026-06-30", "status": "closed", "source_url": ADMISSION_IT},
                {"event": "latest_visa_and_arrival_condition", "deadline": "2026-10-31", "status": "future_for_admitted_students", "source_url": RANKING},
            ],
            "deadline_notes": bi(
                "The 2026/27 application and automatic scholarship competition are closed. UniTrento has not published a next-cycle date in the checked sources, so no deadline is estimated from the previous March cycle.",
                "2026/27 başvurusu ve otomatik burs yarışması kapanmıştır. UniTrento kontrol edilen kaynaklarda sonraki dönem tarihini yayımlamadığından önceki Mart döngüsünden tahmin üretilmez.",
            ),
        }
    )

    row["student_sentiment_profile"].update(
        {
            "student_satisfaction_score": None,
            "sentiment_confidence": "unknown",
            "sample_size_estimate": None,
            "date_range": "",
            "positive_themes": [],
            "negative_themes": [],
            "recurring_complaints": [],
            "recurring_strengths": [],
            "student_sentiment_summary": bi(
                "No programme-specific student sentiment is scored because the degree begins in 2026/27 and has no completed cohort; predecessor-programme comments would not establish experience in the new space curriculum.",
                "Derece 2026/27'de başladığı ve tamamlanmış kohortu olmadığı için programa özgü öğrenci duygu puanı verilmez; önceki program yorumları yeni uzay yolundaki deneyimi kanıtlamaz.",
            ),
            "student_sentiment_sources": [],
        }
    )

    profile = row["source_profile"]
    profile.update(
        {
            "official_program_page": PROGRAM,
            "official_admission_page": NON_EU,
            "official_tuition_page": TUITION,
            "official_scholarship_page": SCHOLARSHIP,
            "official_curriculum_page": CURRICULUM,
            "official_housing_page": HOUSING,
            "official_department_page": SPACE_PHD_DII,
            "official_lab_pages": [LAB],
            "last_verified": CHECKED,
            "needs_verification": False,
            "verification_notes": bi(
                "The record separates the active first year, the officially planned but not yet delivered second-year space curriculum, the closed non-EU competition, automatic merit funding and first-year housing entitlement. Historical housing prices are not converted into a current target-route rent.",
                "Kayıt; etkin birinci yılı, resmen planlanmış ancak henüz yürütülmemiş ikinci yıl uzay yolunu, kapanmış AB-dışı yarışmayı, otomatik başarı bursunu ve ilk yıl konut hakkını ayırır. Tarihsel yurt fiyatları güncel hedef yol kirasına dönüştürülmez.",
            ),
            "field_confidence": {
                "program_basic_info": "high",
                "program": "high",
                "language": "high",
                "admission": "high",
                "non_eu_eligibility": "high",
                "tuition": "high",
                "scholarship": "high",
                "curriculum": "high",
                "research": "high",
                "industry": "medium",
                "living": "unknown",
                "housing": "high",
                "deadlines": "high",
                "deadline": "high",
            },
            "source_log": [
                source(PROGRAM, "Intelligent Mechatronics Engineering overview and four curricula — UniTrento", "official_program_page", ["program", "program_status", "language", "curriculum"]),
                source(NON_EU, "2026/27 Intelligent Mechatronics admission for non-Europeans — UniTrento", "official_admission_page", ["program", "language", "admission", "non_eu_eligibility", "deadline", "scholarship", "housing", "tuition"]),
                source(TRANSITION, "Mechatronics renewal and automatic transition to Intelligent Mechatronics — UniTrento", "official_program_page", ["program", "program_status", "non_eu_eligibility"]),
                source(ADMISSION_IT, "Binding 2026/27 DII non-European admission call — UniTrento", "official_admission_page", ["admission", "non_eu_eligibility", "language", "deadline", "tuition", "scholarship"], access_status="pdf"),
                source(ADMISSION_EN, "2026/27 DII non-European admission call courtesy translation — UniTrento", "official_admission_page", ["admission", "non_eu_eligibility", "language", "deadline", "tuition", "scholarship"], access_status="pdf", notes=bi("Courtesy translation used for accessibility; the Italian call is legally binding and resolves translation defects.", "Erişilebilirlik için yardımcı çeviri kullanılır; hukuken İtalyanca çağrı bağlayıcıdır ve çeviri kusurlarını çözer.")),
                source(RANKING, "2026/27 non-EU ranking and scholarship assignments — Intelligent Mechatronics", "official_admission_page", ["admission", "deadline", "scholarship", "tuition"], access_status="pdf"),
                source(CURRICULUM, "2026/27 educational offer — Intelligent Mechatronics Engineering", "official_curriculum_page", ["curriculum", "program", "language"], access_status="pdf"),
                source(EU_ADMISSION, "Current programme-specific academic requirements — Intelligent Mechatronics", "official_admission_page", ["admission", "language"], notes=bi("Used only to clarify the programme's disciplinary matrix and not to import EU deadlines or income-based fees into the Turkey-resident route.", "Yalnızca programın disiplin matrisini açıklamak için kullanılır; AB tarihleri veya gelir bazlı ücretler Türkiye'de ikamet eden aday yoluna taşınmaz.")),
                source(TUITION, "Current UniTrento tuition systems", "official_tuition_page", ["tuition", "non_eu_eligibility"]),
                source(SCHOLARSHIP, "Current UniTrento scholarships for international students", "official_scholarship_page", ["scholarship", "tuition", "non_eu_eligibility"]),
                source(ADMISSION_POLICY, "Current UniTrento non-EU admission, automatic scholarship and housing policy", "official_university_policy_page", ["non_eu_eligibility", "scholarship", "housing", "tuition"]),
                source(HOUSING, "Accommodation for international students — UniTrento", "official_housing_page", ["housing", "non_eu_eligibility"]),
                source(OPERA_RATES, "Opera Universitaria rates and payments", "official_student_housing_provider", ["housing", "living"], confidence="medium", notes=bi("Current page still displays 2025/26 rates. They are retained only as a labelled historical provider reference because applicability and the 2026/27 reserved-route price are not published.", "Güncel sayfa hâlâ 2025/26 fiyatlarını gösterir. Uygulanabilirlik ve ayrılmış yolun 2026/27 fiyatı yayımlanmadığından yalnızca etiketli tarihsel sağlayıcı referansı olarak tutulur.")),
                source(OPERA_2026_CALL, "Opera Universitaria 2026/27 benefits and accommodation call", "official_student_housing_provider", ["housing", "living", "scholarship", "non_eu_eligibility"], access_status="pdf", notes=bi("Publishes current reduced housing rates and recipient restrictions. The target Turkey-resident applicant is outside this call's stated non-EU-resident-in-Italy group, so these rates are not presented as the guaranteed international-route price.", "Güncel indirimli konut fiyatlarını ve alıcı kısıtlarını yayımlar. Türkiye'de ikamet eden hedef aday, çağrının İtalya'da ikamet eden AB-dışı grubunun dışında olduğundan bu fiyatlar garantili uluslararası yol fiyatı gibi sunulmaz.")),
                source(TRENT_FURLANI, "TRent off-campus listing — Residenza Furlani, Vela", "official_student_housing_provider", ["housing", "living"], notes=bi("Current Opera-hosted listing snapshot with four room examples, utility advances and deposit; not a market average or availability guarantee.", "Opera'nın barındırdığı güncel ilan anlık görüntüsü; dört oda örneği, gider avansı ve depozito içerir; piyasa ortalaması veya mevcudiyet garantisi değildir.")),
                source(TRENT_GRAZIOLI, "TRent off-campus listing — Via Grazioli", "official_student_housing_provider", ["housing", "living"], notes=bi("Current Opera-hosted single-room listing snapshot with rent, utility advance, deposit rule and minimum stay; not a market average or guarantee.", "Opera'nın barındırdığı güncel tek kişilik oda ilanı; kira, gider avansı, depozito kuralı ve asgari kalışı içerir; piyasa ortalaması veya garanti değildir.")),
                source(FACTSHEET, "UniTrento international factsheet 2026/27", "official_cost_of_living_page", ["housing", "living"], access_status="pdf", confidence="medium", notes=bi("Current general factsheet uses priority/upon-availability language; target-route programme and admission pages more specifically state first-year guaranteed/reserved housing. No unreadable cost graphic is transcribed.", "Güncel genel bilgi formu öncelik/mevcudiyet dili kullanır; hedef yol program ve kabul sayfaları ilk yıl için daha özel biçimde garantili/ayrılmış konut der. Okunamayan maliyet grafiği aktarılmaz.")),
                source(LAB, "Sensing Technologies Educational Laboratory — UniTrento DISI", "official_lab_page", ["research", "labs"]),
                source(SPACE_PHD, "National PhD Programme in Space Science and Technology — UniTrento", "official_program_page", ["research", "space_ecosystem"]),
                source(SPACE_PHD_DII, "42nd-cycle National Space Science and Technology PhD — Department of Industrial Engineering", "official_department_page", ["research", "department"]),
                source(SPACE_PHD_CALL, "42nd-cycle National Space Science and Technology PhD call and topics", "official_program_page", ["research", "industry", "space_ecosystem"], access_status="pdf"),
            ],
        }
    )

    row["decision_summary"] = {
        "best_for": [
            bi("Applicants targeting spacecraft sensors, payload/instrument hardware, remote sensing, on-board computing, space mechanisms or systems integration", "Uzay aracı sensörleri, faydalı yük/enstrüman donanımı, uzaktan algılama, araç üstü hesaplama, uzay mekanizmaları veya sistem entegrasyonu hedefleyen adaylar"),
            bi("Turkey-resident applicants who value automatic merit-scholarship consideration and first-year reserved housing", "Otomatik başarı bursu değerlendirmesine ve ilk yıl ayrılmış konuta önem veren Türkiye'de ikamet eden adaylar"),
        ],
        "not_ideal_for": [
            bi("Applicants who require a degree titled Aerospace or Space Engineering", "Derece adının Aerospace veya Space Engineering olmasını isteyen adaylar"),
            bi("Applicants prioritising astrodynamics, orbital mechanics, propulsion, classical aerodynamics or a flight-vehicle curriculum", "Astrodinamik, yörünge mekaniği, itki, klasik aerodinamik veya uçuş aracı müfredatını önceliklendiren adaylar"),
            bi("Applicants unwilling to accept delivery risk in a new programme whose space year has not yet run", "Uzay yılı henüz yürütülmemiş yeni bir programdaki teslim riskini kabul etmeyen adaylar"),
        ],
        "main_strengths": [
            bi("A coherent 24-ECTS space-subject package plus 18-ECTS final project and 6-ECTS internship/other activity", "Tutarlı 24 AKTS uzay ders paketi, 18 AKTS bitirme projesi ve 6 AKTS staj/diğer etkinlik"),
            bi("Direct institutional research environment in remote sensing, instrumentation and satellite-platform technologies", "Uzaktan algılama, enstrümantasyon ve uydu platformu teknolojilerinde doğrudan kurumsal araştırma ortamı"),
            bi("Automatic scholarship consideration and guaranteed paid first-year accommodation for the checked non-EU route", "Kontrol edilen AB-dışı yolda otomatik burs değerlendirmesi ve ücretli, garantili ilk yıl konutu"),
        ],
        "main_risks": [
            bi("The degree is LM-33 Mechanical Engineering / Intelligent Mechatronics, not a standalone aerospace or space degree", "Derece bağımsız havacılık-uzay veya uzay derecesi değil, LM-33 Mechanical Engineering / Intelligent Mechatronics'tir"),
            bi("The 2026/27 space curriculum is official but marked inactive until the new cohort reaches year two", "2026/27 uzay yolu resmîdir ancak yeni kohort ikinci yıla ulaşana kadar pasif işaretlenmiştir"),
            bi("Only two scholarships were available for 25 initial places in the closed 2026/27 ranking", "Kapanan 2026/27 sıralamasında 25 ilk kontenjan için yalnızca iki burs vardı"),
            bi("Exact IELTS/TOEFL thresholds, current reserved-housing rent and the next application date are not published", "Kesin IELTS/TOEFL tabanları, ayrılmış konutun güncel kirası ve sonraki başvuru tarihi yayımlanmamıştır"),
        ],
        "application_reality": bi(
            "The 2026/27 route closed on 4 March 2026 and the ranking is already published. A future applicant should prepare B2 evidence, an English CV, translated degree/transcript documents and course descriptions early, but must wait for UniTrento to publish the next call rather than treating March as an estimated deadline.",
            "2026/27 yolu 4 Mart 2026'da kapandı ve sıralama yayımlandı. Gelecek dönem adayı B2 kanıtını, İngilizce CV'yi, çevrilmiş diploma/transkripti ve ders açıklamalarını erken hazırlamalıdır; ancak Mart ayını tahmini tarih saymak yerine UniTrento'nun sonraki çağrısını beklemelidir.",
        ),
        "overall_recommendation": bi(
            "A strong adjacent option for space hardware, sensing and embedded systems, with unusually clear non-EU funding and housing mechanics; it is not a substitute for a mature, dedicated spacecraft/astrodynamics/propulsion MSc.",
            "Uzay donanımı, algılama ve gömülü sistemler için güçlü bir yan alan seçeneği; AB-dışı burs ve konut süreci alışılmadık ölçüde açıktır. Olgun, bağımsız uzay aracı/astrodinamik/itki yüksek lisansının yerine geçmez.",
        ),
        "recommended_user_profile": bi(
            "Mechanical, mechatronics, electronics, control or automation graduate with B2 English, strong mathematics/physics, interest in spacecraft hardware and a willingness to join the first cohort of a new space curriculum.",
            "B2 İngilizce, güçlü matematik/fizik temeli ve uzay aracı donanımı ilgisi olan; yeni uzay yolunun ilk kohortunda bulunmayı kabul eden mekanik, mekatronik, elektronik, kontrol veya otomasyon mezunu.",
        ),
    }

    row["scoring_inputs"].update(
        {
            "academic_field_fit_score_seed": None,
            "eligibility_language_score_seed": None,
            "cost_funding_score_seed": None,
            "career_research_score_seed": None,
            "living_risk_score_seed": None,
            "data_confidence_score_seed": None,
            "hard_filter_flags": {
                "english_only_compatible": True,
                "requires_italian": False,
                "non_eu_eligible": True,
                "standalone_aerospace_or_space_degree": False,
                "space_second_year_already_delivered": False,
                "tuition_above_5000_first_year_for_admitted_applicant": False,
                "tuition_above_10000": False,
                "deadline_unclear": False,
                "deadline_closed_for_new_applicants": True,
                "housing_guaranteed_first_year": True,
                "scholarship_separate_application_required": False,
                "needs_verification": False,
            },
        }
    )

    quality = audit_record(row)
    quality["audited_at"] = CHECKED
    row["data_quality"] = quality
    complete = quality["status"] == "verified"
    row["quality_control"] = {
        "qc_status": "passed" if complete else "needs_revision",
        "checked_at": CHECKED,
        "failed_canary_tests": [] if complete else ["missing_or_unverified_critical_fields"],
        "remaining_verification_tasks": [] if complete else [bi(f"Resolve: {', '.join(quality['unverified_critical_fields'])}.", f"Çözülmesi gerekenler: {', '.join(quality['unverified_critical_fields'])}.")],
        "monitoring_tasks": [
            bi("When published, replace the closed 2026/27 call with the next non-EU cycle rather than projecting its deadline.", "Yayımlandığında kapanmış 2026/27 çağrısını tarih tahmini yapmadan sonraki AB-dışı dönemle değiştirin."),
            bi("Verify actual second-year delivery, course availability and the reserved-route housing rent when the first cohort reaches 2027/28.", "İlk kohort 2027/28'e ulaştığında ikinci yılın fiilî yürütülmesini, ders mevcudiyetini ve ayrılmış yol konut kirasını doğrulayın."),
        ],
        "qc_notes": bi(
            "All decision-critical groups have accessible official evidence. Unknowns are explicit: test scores, current target-route rent, future deadline, exact assessment count and first-cohort delivery outcomes are not guessed.",
            "Tüm karar-kritik gruplarda erişilebilir resmî kanıt vardır. Bilinmeyenler açıktır: sınav puanları, hedef yolun güncel kirası, gelecek tarih, kesin değerlendirme sayısı ve ilk kohortun yürütme sonuçları tahmin edilmez.",
        ),
    }
    profile["needs_verification"] = not complete


def main() -> None:
    payload = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    matches = [row for row in payload["universities"] if row.get("id") == RECORD_ID]
    if len(matches) != 1:
        raise RuntimeError(f"Expected one {RECORD_ID!r} record; found {len(matches)}")
    update(matches[0])
    payload["last_updated"] = CHECKED
    DATA_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(matches[0]["data_quality"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
