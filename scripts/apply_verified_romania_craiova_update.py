"""Promote University of Craiova Complex Systems for Aerospace Engineering to native V2."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data_base" / "romania.json"
QUEUE_PATH = ROOT / "research_queue" / "program_candidates_v2.json"
DISCOVERY_PATH = ROOT / "reports" / "romania_programme_discovery_2026-08-14.json"
SCAN_PATH = ROOT / "research_queue" / "country_scan_log_v2.json"

RECORD_ID = "ro-university-craiova-complex-systems-aerospace-engineering-msc"
PROGRAM_URL = "https://elth.ucv.ro/invatamant/studii-master/"
OFFER_URL = "https://www.ucv.ro/pdf/admitere/2026/UCv-Oferta-educationala-MASTER-2026-2027-rev-12-martie.pdf"
NON_EU_PLACES_URL = "https://www.ucv.ro/pdf/admitere/2026/cpv/Locuri_disponibile_MASTER-CPV_A.pdf"
FOREIGN_LANGUAGES_URL = "https://www.ucv.ro/pdf/admitere/2026/cpv/Study_Programms_Taught_in_Foreign_Languages.pdf"
ADMISSION_CONDITIONS_URL = "https://www.ucv.ro/pdf/admitere/2026/traduceri/UCv_Conditii_admitere%20MASTER_2026-2027_rev-20-aprilie.pdf"
NON_EU_ADMISSION_URL = "https://www.ucv.ro/en/admitere/foreign_students/Non_EU_Citizens.php"
PREPARATORY_YEAR_URL = "https://www.ucv.ro/en/admitere/foreign_students/romanian_language_preparatory_year.php"
CURRICULUM_URL = "https://cis01.ucv.ro/en/relatii_internationale/studyplans.html/elth_ma_3_500482.html"
LABS_URL = "https://elth.ucv.ro/structura-facultatii/laboratoare/"
SCIA_LAB_URL = "https://elth.ucv.ro/catedrele/avionica/laboratoare/scia.pdf"
AVIONICS_LAB_URL = "https://elth.ucv.ro/catedrele/avionica/laboratoare/avionica.pdf"
HOUSING_2026_URL = "https://www.ucv.ro/en/media/det.php?id=612"
HOUSING_DESCRIPTION_URL = "https://www.ucv.ro/en/campus/camine_cantine/descriere.php"
MFA_SCHOLARSHIP_URL = "https://scholarships.studyinromania.gov.ro/scholarship-about"
PERFORMANCE_SCHOLARSHIP_URL = "https://www.ie.ucv.ro/index.php/ro/studenti/link-uri-utile/avizier-secretariat/533-acordarea-burselor-de-performanta-pe-semestrul-ii-2025-2026"
GOV_MASTER_URL = "https://www.edu.ro/sites/default/files/fisiere%20articole/HG_192_2026_Anexe_domenii_master.pdf"
THE_RANKING_URL = "https://www.timeshighereducation.com/world-university-rankings/university-craiova"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path: Path, payload) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def src(
    source_id: str,
    url: str,
    title: str,
    publisher: str,
    source_type: str,
    access_status: str,
    relevant_fields: list[str],
    confidence: str,
    notes_en: str,
    notes_tr: str,
    *,
    official: bool = True,
    effective_date: str | None = None,
    cycle: str | None = None,
):
    return {
        "source_id": source_id,
        "url": url,
        "final_url": url,
        "title": title,
        "publisher": publisher,
        "source_type": source_type,
        "official": official,
        "access_status": access_status,
        "published_or_effective_date": effective_date,
        "applicable_academic_cycle": cycle,
        "last_checked": "2026-08-14",
        "relevant_fields": relevant_fields,
        "confidence": confidence,
        "notes": {"en": notes_en, "tr": notes_tr},
    }


records = load(DB_PATH)
if any(record.get("id") == RECORD_ID for record in records):
    raise SystemExit(f"Record already exists: {RECORD_ID}")

record = {
    "schema_version": "2.0.0",
    "record_type": "university_program",
    "id": RECORD_ID,
    "catalog_status": "active",
    "country_code": "RO",
    "country": "Romania",
    "institution_profile": {
        "institution_id": "ro-university-craiova",
        "name": "University of Craiova",
        "native_name": "Universitatea din Craiova",
        "short_name": "UCV",
        "institution_type": "public_university",
        "official_url": "https://www.ucv.ro/",
    },
    "location": {
        "campus": "Faculty of Electrical Engineering",
        "city": "Craiova",
        "region": "Dolj",
        "country": "Romania",
        "latitude": None,
        "longitude": None,
        "location_confidence": "high",
    },
    "program_profile": {
        "name": "Complex Systems for Aerospace Engineering",
        "native_name": "Sisteme complexe pentru ingineria aerospațială",
        "degree_award": "Master's degree in Aerospace Engineering",
        "degree_level": "Master",
        "degree_class": "graduate_taught_with_research",
        "delivery_mode": "on_campus",
        "attendance_mode": "full_time",
        "duration": {"value": 2, "unit": "year", "terms": 4},
        "credits": {"value": 120, "system": "ECTS"},
        "department": "Department of Electrical, Energy and Aerospace Engineering",
        "faculty_or_school": "Faculty of Electrical Engineering",
        "official_url": PROGRAM_URL,
        "program_status": "active",
        "relevance_status": "strong",
    },
    "eligibility_profile": {
        "eligible_for_non_eu": True,
        "required_previous_degree": {
            "en": "A completed bachelor's degree or equivalent is required. The checked 2026/27 sources do not publish a programme-specific exhaustive list of accepted prior disciplines.",
            "tr": "Tamamlanmış lisans derecesi veya eşdeğeri gerekir. Kontrol edilen 2026/27 kaynakları programa özgü kapsamlı bir kabul edilen önceki bölüm listesi yayımlamaz.",
        },
        "accepted_backgrounds": [],
        "prerequisites": [],
        "minimum_gpa": None,
        "gpa_scale": None,
        "selection_method": "oral_admission_examination_plus_bachelors_degree_examination_average",
        "selection_criteria": [
            "Oral admission examination graded numerically",
            "Bachelor's degree examination average",
            "Final admission average is the arithmetic mean of the two components",
            "Oral examination grade is the first tie-breaker",
            "Non-EU file eligibility and Romanian Ministry Letter of Acceptance",
        ],
        "admission_risk": "medium",
        "required_documents": [
            "Birth certificate with certified copy or certified translation when required",
            "Passport valid for at least six months after programme start",
            "Proof of permanent residence abroad",
            "Marriage certificate and certified translation when applicable",
            "Signed application form with a recent photo",
            "Authenticated high-school diploma and certified translation when required",
            "Authenticated bachelor's diploma or equivalent and certified translation when required",
            "Authenticated transcripts and certified translations when required",
            "Medical certificate in Romanian, English or French",
            "Romanian preparatory-year certificate or Romanian B1 proficiency proof/test result",
            "Proof of the file-processing fee",
        ],
        "application_portals": ["https://evstud.ucv.ro/"],
        "interview": {
            "required": True,
            "notes": {
                "en": "The 2026/27 faculty table specifies a graded oral admission examination. Non-EU applicants should confirm the online/in-person format and scheduling with the faculty before travel.",
                "tr": "2026/27 fakülte tablosu notlandırılan sözlü kabul sınavını belirtir. AB dışı adaylar seyahatten önce çevrim içi/yüz yüze formatı ve programlamayı fakülteden teyit etmelidir.",
            },
        },
        "gre": {
            "policy": "not_listed_in_current_official_requirements",
            "test_type": "unknown",
            "minimum_scores": {},
            "recommended_scores": {},
            "validity_rule": None,
            "waiver_rules": [],
            "source_ids": ["ro_ucv_admission_conditions_2026", "ro_ucv_noneu_admission_2026"],
        },
        "other_standardized_tests": ["University of Craiova Romanian-language proficiency test at minimum B1 when no accepted exemption applies"],
        "notes_for_turkish_students": {
            "en": "Türkiye applicants use the non-EU self-funded route unless they win a separate government scholarship. Romanian B1 or the preparatory year is the first hard gate; no English certificate or GRE is listed in the current official requirements.",
            "tr": "Türkiye'den adaylar ayrı bir devlet bursu kazanmadıkça AB dışı kendi imkânıyla ödeme rotasını kullanır. Rumence B1 veya hazırlık yılı ilk kesin kapıdır; güncel resmî şartlarda İngilizce belgesi ya da GRE listelenmez.",
        },
    },
    "language_profile": {
        "teaching_languages": ["Romanian"],
        "english_required": False,
        "accepted_tests": [],
        "exemptions": [
            {
                "en": "Romanian preparation is not required for candidates with at least three consecutive years of Romanian-medium study, an accredited Romanian preparatory-year certificate, or a University of Craiova Romanian test result of B1 or higher.",
                "tr": "En az üç yıl art arda Rumence eğitim görenler, akredite Rumence hazırlık yılı belgesi olanlar veya Craiova Üniversitesi Rumence sınavından en az B1 alanlar için Rumence hazırlık gerekmez.",
            }
        ],
        "local_language_entry_requirement": "romanian_b1_or_preparatory_year",
        "local_language_for_curriculum": "required",
        "local_language_for_life_or_internship": {
            "en": "Romanian is the verified teaching language and therefore essential both academically and for most local opportunities.",
            "tr": "Rumence doğrulanmış eğitim dilidir; bu nedenle hem akademik yaşamda hem de yerel fırsatların çoğunda zorunlu düzeyde önemlidir.",
        },
        "mixed_language_warning": {
            "en": "An English programme title and English-language study-plan page do not make the degree English-taught. The 2026 non-EU place table explicitly labels it Romanian, and it is absent from UCV's 2026 foreign-language programme list.",
            "tr": "İngilizce program adı ve İngilizce ders-planı sayfası dereceyi İngilizce yapmaz. 2026 AB dışı kontenjan tablosu dili açıkça Rumence gösterir ve program UCV'nin 2026 yabancı dil programları listesinde yer almaz.",
        },
        "language_risk": "very_high",
    },
    "cost_profile": {
        "academic_cycle": "2026/2027",
        "tuition_items": [
            {
                "amount": 3500,
                "minimum": None,
                "maximum": None,
                "currency": "EUR",
                "period": "academic_year",
                "applicant_scope": "non_eu_self_funded_aerospace_engineering_master",
                "academic_cycle": "2026/2027",
                "mandatory": True,
                "basis": "UCV non-EU technical-field fee table",
                "source_ids": ["ro_ucv_noneu_admission_2026"],
            },
            {
                "amount": 2500,
                "minimum": None,
                "maximum": None,
                "currency": "EUR",
                "period": "one_academic_year",
                "applicant_scope": "non_eu_candidate_requiring_romanian_preparatory_year",
                "academic_cycle": "2026/2027",
                "mandatory": False,
                "basis": "UCV non-EU technical-field Romanian preparatory-year fee",
                "source_ids": ["ro_ucv_noneu_admission_2026", "ro_ucv_preparatory_year_2026"],
            },
        ],
        "mandatory_fee_items": [],
        "application_fee_items": [
            {
                "amount": 200,
                "currency": "EUR",
                "period": "one_time",
                "applicant_scope": "non_eu_applicant",
                "academic_cycle": "2026/2027",
                "mandatory": True,
                "basis": "Non-refundable file-processing fee; UCV alternatively publishes 1000 RON",
                "source_ids": ["ro_ucv_noneu_admission_2026"],
            }
        ],
        "deposit_items": [
            {
                "amount": 1750,
                "currency": "EUR",
                "period": "one_time_first_year_confirmation",
                "applicant_scope": "accepted_non_eu_candidate",
                "academic_cycle": "2026/2027",
                "mandatory": True,
                "basis": "Non-refundable confirmation payment equal to 50% of first-year tuition; it is part of tuition, not an additional charge",
                "source_ids": ["ro_ucv_noneu_admission_2026"],
            }
        ],
        "insurance_items": [],
        "published_cost_of_attendance_items": [],
        "payment_schedule": {
            "en": "UCV states that accepted non-EU candidates pay a non-refundable 50% tuition confirmation within 15 days. After the Ministry Letter of Acceptance is emailed, the full first-year tuition must be completed within a maximum of 15 calendar days.",
            "tr": "UCV, kabul edilen AB dışı adayların 15 gün içinde iade edilmeyen %50 öğrenim ücreti teyit ödemesi yapacağını belirtir. Bakanlık Kabul Mektubu e-postayla geldikten sonra ilk yıl ücretinin tamamı en çok 15 takvim günü içinde tamamlanmalıdır.",
        },
        "refund_policy": {
            "en": "The 50% confirmation payment and the file-processing fee are explicitly non-refundable. Other withdrawal or visa-refusal refund cases were not verified.",
            "tr": "%50 teyit ödemesi ve dosya işlem bedeli açıkça iade edilmez. Diğer ayrılma veya vize reddi iade durumları doğrulanmadı.",
        },
        "cost_risk": "medium",
        "notes": {
            "en": "The verified two-year degree tuition is EUR 7,000 before housing and living costs. Candidates needing Romanian preparation should budget an additional EUR 2,500 and one academic year; no current official total cost-of-attendance figure was published.",
            "tr": "Doğrulanmış iki yıllık derece ücreti konut ve yaşam giderleri hariç 7.000 EUR'dur. Rumence hazırlık gerekenler ek 2.500 EUR ve bir akademik yıl planlamalıdır; güncel resmî toplam katılım maliyeti yayımlanmamıştır.",
        },
    },
    "scholarship_profile": {
        "application_mode": "separate_external_government_competition",
        "automatic_consideration": False,
        "separate_application_required": True,
        "opportunities": [
            {
                "name": "Romanian Government Ministry of Foreign Affairs Scholarship for non-EU citizens",
                "award": "Application-fee exemption, Romanian preparatory-year tuition, degree tuition, monthly scholarship and dormitory-cost financing within the allocated subsidy and available places",
                "applicant_scope": "eligible_non_eu_citizens_applying_to_romanian_taught_bachelor_or_master_programmes",
                "eligibility_note": "Competitive file review; at least 7/10 or Good in the last completed study cycle, complete recognized documents and published exclusions apply. University placement is not guaranteed if the preferred option cannot be honoured.",
                "deadline": "2026-03-31",
                "deadline_status": "current_cycle_closed",
                "source_ids": ["ro_mfa_scholarship_2026"],
            }
        ],
        "assistantships": [],
        "non_eu_eligibility_summary": {
            "en": "The standard UCV non-EU route is self-funded and does not automatically consider applicants for scholarships. The MFA scholarship is a separate national competition and may assign an alternative institution in the same field if the preferred option cannot be honoured.",
            "tr": "Standart UCV AB dışı rotası kendi imkânıyla ücretlidir ve adayları otomatik burs değerlendirmesine almaz. Dışişleri bursu ayrı bir ulusal yarışmadır; tercih karşılanamazsa aynı alanda alternatif kurum atanabilir.",
        },
        "funding_competitiveness": "very_high",
        "funding_risk": "very_high",
        "notes": {
            "en": "UCV's current faculty performance-scholarship notice restricts that award to full-time students on state-funded places and requires a form submission. A self-funded CPV student should therefore budget as unfunded unless a separate award is formally secured.",
            "tr": "UCV'nin güncel fakülte başarı bursu duyurusu bu bursu devlet bütçeli tam zamanlı öğrencilere sınırlar ve form başvurusu ister. Bu nedenle kendi ücretini ödeyen CPV öğrencisi ayrı bir ödülü resmen kazanmadıkça finansmansız bütçe yapmalıdır.",
        },
    },
    "living_profile": {
        "housing_access": "competitive_not_guaranteed",
        "student_housing_available": True,
        "housing_application_separate": True,
        "housing_deadline_events": [
            {
                "event": "UCV 2026/27 dormitory application deadline",
                "date": "2026-08-01",
                "date_status": "current_cycle_closed",
                "applicant_scope": "non_resident_students_including_admitted_candidates",
                "source_ids": ["ro_ucv_housing_2026"],
            }
        ],
        "housing_options": [
            {
                "name": "University of Craiova student halls",
                "type": "university_residence",
                "allocation": "About 3,100 places across 11 halls; places are allocated electronically to faculties according to non-resident demand and are not guaranteed",
                "source_ids": ["ro_ucv_housing_2026", "ro_ucv_housing_description"],
            }
        ],
        "official_living_cost_items": [],
        "official_rent_items": [],
        "commute_notes": {
            "en": "The university lists a residence hall at the Electrical Engineering campus, but it does not guarantee programme-specific allocation. Confirm the actual teaching building and residence route after allocation.",
            "tr": "Üniversite Elektrik Mühendisliği kampüsünde bir yurt listeler; ancak programa özgü tahsis garantisi vermez. Tahsisten sonra gerçek ders binasını ve yurt ulaşım rotasını doğrulayın.",
        },
        "housing_risk": "medium",
        "living_risk": "medium",
        "notes": {
            "en": "A separate online request by 1 August is mandatory for normal consideration. Missing, incomplete or unattended requests are considered only if places remain. A current 2026/27 self-funded non-EU monthly dormitory rate and official total living budget were not verified.",
            "tr": "Normal değerlendirme için 1 Ağustos'a kadar ayrı çevrim içi talep zorunludur. Eksik, tamamlanmamış veya zamanında kullanılmayan talepler yalnız yer kalırsa değerlendirilir. 2026/27 kendi ücretini ödeyen AB dışı öğrenci için güncel aylık yurt ücreti ve resmî toplam yaşam bütçesi doğrulanmadı.",
        },
    },
    "curriculum_profile": {
        "academic_cycle": "official study-plan page is undated; checked 2026-08-14",
        "tracks": [],
        "specializations": [],
        "course_count": {
            "minimum": 21,
            "maximum": 21,
            "counting_rule": "Twenty-one published line items: 16 credit-bearing modules totaling 120 ECTS plus five linked zero-ECTS project/research rows. No electives are shown.",
        },
        "credit_breakdown": [
            {"component": "Semester 1: five 6-ECTS modules plus a linked zero-ECTS navigation project", "credits": 30},
            {"component": "Semester 2: five 6-ECTS modules plus three linked zero-ECTS project/research rows", "credits": 30},
            {"component": "Semester 3: four technical modules plus a linked zero-ECTS project", "credits": 30},
            {"component": "Semester 4 dissertation", "credits": 20},
            {"component": "Semester 4 scientific research stage", "credits": 10},
        ],
        "mandatory_courses": [
            "3D Engineering Graphics",
            "Quantitative Methods for Aeronautical Engineering and Management",
            "National and International Aeronautical Regulations",
            "Nonlinear Synthesis of Autopilots",
            "Integrated Aerospace Navigation Systems",
            "Integrated Aerospace Navigation Systems - Project",
            "Analysis and Synthesis of Gyroscopic Systems for Aerospace Stabilization, Navigation and Guidance",
            "Gyroscopic Systems Analysis and Synthesis - Project",
            "Special Problems of Flight Dynamics",
            "Scientific Research",
            "Special Problems of Aerospace Structures",
            "Automatic Control of Aerospace Propulsion Systems",
            "Aerospace Structure Design and Construction - Project",
            "Special Problems of Aerospace Propulsion",
            "On-board Electromagnetic Compatibility of Aerospace Vehicles",
            "Adaptive Systems with Neural Networks for Flight Control",
            "On-board Complex Systems for Electrical Energy Conversion",
            "Optimal Systems for Flight Control",
            "Optimal Systems for Flight Control - Project",
            "Dissertation",
            "Scientific Research Stage",
        ],
        "elective_courses": [],
        "lab_courses": [
            "3D Engineering Graphics",
            "Quantitative Methods for Aeronautical Engineering and Management",
            "National and International Aeronautical Regulations",
            "Nonlinear Synthesis of Autopilots",
            "Integrated Aerospace Navigation Systems",
            "Analysis and Synthesis of Gyroscopic Systems for Aerospace Stabilization, Navigation and Guidance",
            "Special Problems of Flight Dynamics",
            "Automatic Control of Aerospace Propulsion Systems",
            "Adaptive Systems with Neural Networks for Flight Control",
            "On-board Complex Systems for Electrical Energy Conversion",
            "Optimal Systems for Flight Control",
        ],
        "project_based_courses": [
            "Integrated Aerospace Navigation Systems - Project",
            "Gyroscopic Systems Analysis and Synthesis - Project",
            "Scientific Research",
            "Aerospace Structure Design and Construction - Project",
            "Optimal Systems for Flight Control - Project",
            "Dissertation",
            "Scientific Research Stage",
        ],
        "thesis": {
            "required": True,
            "credits": 20,
            "options": ["A 20-ECTS dissertation is paired with a separate 10-ECTS scientific-research stage in semester 4."],
        },
        "internship": {
            "required": None,
            "credits": None,
            "duration": None,
            "allocation": "not_published",
            "notes": {
                "en": "The official study plan includes a research stage but does not identify a mandatory external-company internship or a guaranteed placement host.",
                "tr": "Resmî ders planı araştırma aşaması içerir; zorunlu dış şirket stajı veya garantili yerleştirme kurumu belirtmez.",
            },
        },
        "mobility_options": [],
        "double_degree_options": [],
        "curriculum_urls": [CURRICULUM_URL],
    },
    "category_profile": {
        "primary_categories": ["aerospace_engineering", "avionics_navigation", "gnc_control_autonomy"],
        "secondary_categories": ["flight_control", "aerospace_propulsion", "aerospace_structures", "electromagnetic_compatibility", "onboard_energy_systems"],
        "subcategories": ["autopilots", "integrated_navigation", "gyroscopic_guidance", "flight_dynamics", "propulsion_control", "neural_network_control", "optimal_flight_control"],
        "normalized_tags": ["aerospace", "avionics", "navigation", "gnc", "autopilot", "flight_dynamics", "propulsion_control", "structures", "emc", "onboard_power"],
        "category_scores": {
            "space_systems": 42,
            "satellite_systems": 12,
            "gnc": 88,
            "propulsion": 56,
            "aerodynamics_cfd": 15,
            "structures_materials": 35,
            "space_science": 0,
        },
        "category_evidence": [
            "The official study plan is strongest in avionics/GNC: autopilots, integrated navigation, gyroscopic guidance, flight dynamics, neural-network control and optimal flight control. It also covers propulsion control, structures, EMC and on-board energy, but publishes no explicit satellite, orbital-mechanics or space-science module."
        ],
    },
    "research_profile": {
        "research_areas": [
            "Aerospace navigation and guidance",
            "Autopilots and flight control",
            "Flight dynamics",
            "Aerospace propulsion control",
            "Aerospace structures",
            "On-board electromagnetic compatibility",
            "On-board energy conversion",
            "Adaptive and optimal control",
        ],
        "labs": ["Complex Systems for Aerospace Engineering Laboratory", "Avionics Laboratory"],
        "research_centers": [],
        "facilities": [
            "SCIA laboratory: 40 m² and nine workstations",
            "SCIA computing inventory: 9+6 computers, acquisition boards, printers, scanner and specialist software",
            "Matlab/Simulink, LabVIEW, QuickField, Spice, Pro/Engineering and Visual C listed for simulation, data acquisition, signal processing, fields, circuits and finite elements",
        ],
        "projects": [],
        "student_teams": [],
        "research_opportunity_for_masters": "30_ects_dissertation_and_research_stage_plus_embedded_projects",
        "research_strength_score": 74,
        "summary": {
            "en": "The degree dedicates 30 ECTS to dissertation and scientific research and embeds several project rows. UCV publishes a programme-named computational laboratory and a broad avionics laboratory; however, both detailed inventory PDFs are undated, so current equipment availability and access must be reconfirmed.",
            "tr": "Derece tez ve bilimsel araştırmaya 30 AKTS ayırır ve birden fazla proje satırı içerir. UCV program adını taşıyan hesaplamalı laboratuvar ile geniş bir aviyonik laboratuvar yayımlar; ancak iki ayrıntılı envanter PDF'si de tarihsiz olduğundan güncel ekipman erişimi yeniden teyit edilmelidir.",
        },
    },
    "industry_ecosystem_profile": {
        "confirmed_partners": [],
        "nearby_organizations": [],
        "space_agencies_or_public_bodies": [],
        "research_institutes": [],
        "startup_or_incubator_ecosystem": [],
        "internship_access": "not_published",
        "industry_thesis_access": "unknown",
        "career_relevance": "high_for_aircraft_avionics_navigation_and_control_medium_for_broad_space_systems",
        "ecosystem_strength_score": None,
        "summary": {
            "en": "Curricular relevance to avionics, navigation, flight control, on-board systems and propulsion control is clear. No current programme-specific employer partnership, partner-side confirmation, guaranteed internship, security-clearance pathway or placement rate was verified.",
            "tr": "Aviyonik, seyrüsefer, uçuş kontrolü, uçuş sistemleri ve itki kontrolüne müfredat uygunluğu açıktır. Güncel programa özgü işveren ortaklığı, ortak tarafı teyidi, garantili staj, güvenlik izni rotası veya yerleştirme oranı doğrulanmadı.",
        },
    },
    "application_timeline_profile": {
        "target_academic_cycle": "2026/2027",
        "intake_terms": ["Autumn"],
        "deadline_events": [
            {
                "event": "Non-EU degree application session 1",
                "date": "2026-04-01/2026-05-21",
                "date_status": "current_cycle_closed",
                "applicant_scope": "non_eu",
                "source_ids": ["ro_ucv_noneu_admission_2026"],
            },
            {
                "event": "Non-EU degree application session 2",
                "date": "2026-06-08/2026-07-20",
                "date_status": "current_cycle_closed",
                "applicant_scope": "non_eu",
                "source_ids": ["ro_ucv_noneu_admission_2026"],
            },
            {
                "event": "Romanian-language evaluation for non-EU degree applicants",
                "date": "2026-05-25 or 2026-07-22",
                "date_status": "current_cycle_closed",
                "applicant_scope": "non_eu_without_exemption",
                "source_ids": ["ro_ucv_noneu_admission_2026"],
            },
            {
                "event": "Romanian preparatory-year application session 1",
                "date": "2026-04-01/2026-04-19",
                "date_status": "current_cycle_closed",
                "applicant_scope": "foreign_candidate_needing_preparatory_year",
                "source_ids": ["ro_ucv_preparatory_year_2026"],
            },
            {
                "event": "Romanian preparatory-year application session 2",
                "date": "2026-06-01/2026-06-29",
                "date_status": "current_cycle_closed",
                "applicant_scope": "foreign_candidate_needing_preparatory_year",
                "source_ids": ["ro_ucv_preparatory_year_2026"],
            },
            {
                "event": "Romanian MFA scholarship application window",
                "date": "2026-02-16/2026-03-31",
                "date_status": "current_cycle_closed",
                "applicant_scope": "eligible_non_eu_scholarship_candidate",
                "source_ids": ["ro_mfa_scholarship_2026"],
            },
            {
                "event": "UCV dormitory application deadline",
                "date": "2026-08-01",
                "date_status": "current_cycle_closed",
                "applicant_scope": "non_resident_students_and_admitted_candidates",
                "source_ids": ["ro_ucv_housing_2026"],
            },
        ],
        "historical_deadline_patterns": [],
        "result_timing": {
            "en": "Non-EU preliminary results were scheduled for 26 May and 23 July 2026, with final university results on 29 May and 27 July. The Ministry then reviews accepted files and issues the Letter of Acceptance; no guaranteed ministry turnaround was published on the checked page.",
            "tr": "AB dışı ön sonuçlar 26 Mayıs ve 23 Temmuz 2026, üniversite nihai sonuçları 29 Mayıs ve 27 Temmuz için planlandı. Ardından Bakanlık kabul edilen dosyaları inceler ve Kabul Mektubu düzenler; kontrol edilen sayfada garantili Bakanlık işlem süresi yayımlanmadı.",
        },
        "enrollment_events": [
            {
                "event": "Upload non-EU confirmation form",
                "timing": "27-28 May 2026 or 24-26 July 2026",
                "source_ids": ["ro_ucv_noneu_admission_2026"],
            },
            {
                "event": "Pay non-refundable 50% tuition confirmation",
                "timing": "Within 15 days of acceptance under the published fee procedure",
                "source_ids": ["ro_ucv_noneu_admission_2026"],
            },
            {
                "event": "Complete first-year tuition payment",
                "timing": "Within 15 calendar days of the emailed Ministry Letter of Acceptance",
                "source_ids": ["ro_ucv_noneu_admission_2026"],
            },
        ],
        "pre_enrolment_required": True,
        "visa_sensitive_steps": [
            "Secure Romanian B1 evidence or preparatory-year admission",
            "Complete authenticated documents and translations",
            "Obtain final UCV acceptance and Ministry Letter of Acceptance",
            "Pay first-year tuition within the 15-day window",
            "Apply for the Romanian long-stay study visa immediately after the Letter of Acceptance",
            "Submit original authenticated documents on enrolment",
        ],
        "timeline_risk": "high",
        "planning_advice": {
            "en": "For a Türkiye applicant without Romanian B1, treat the route as a three-year academic journey and apply first to the preparatory year. Scholarship applications close earlier than UCV admission, while housing requires a separate request by 1 August.",
            "tr": "Rumence B1'i olmayan Türkiye adayı rotayı üç yıllık akademik yolculuk olarak görmeli ve önce hazırlık yılına başvurmalıdır. Burs başvuruları UCV kabulünden daha erken kapanır; yurt içinse 1 Ağustos'a kadar ayrı talep gerekir.",
        },
    },
    "ranking_profile": {
        "institutional_rankings": [
            {"provider": "Times Higher Education", "ranking": "World University Rankings 2026", "band": "1501+", "source_ids": ["the_ucv_2026"]}
        ],
        "subject_rankings": [
            {"provider": "Times Higher Education", "ranking": "Engineering 2026", "band": "1251+", "source_ids": ["the_ucv_2026"]}
        ],
        "accreditations": ["Listed in Romanian Government Decision 192/2026 as a Romanian-language, full-time, 120-ECTS research master's for 2026/2027"],
        "programme_reputation_evidence": [],
        "prestige_summary": {
            "en": "UCV is in THE's 1501+ global and 1251+ engineering bands for 2026. These are institutional context only and are not evidence of aerospace depth; technical fit is assessed from the programme curriculum and laboratories.",
            "tr": "UCV 2026'da THE dünya sıralamasında 1501+, mühendislikte 1251+ bandındadır. Bunlar yalnız kurumsal bağlamdır ve havacılık-uzay derinliği kanıtı değildir; teknik uygunluk program müfredatı ve laboratuvarlarından değerlendirilir.",
        },
        "technical_fit_use": False,
    },
    "outcomes_profile": {
        "official_employment_outcomes": [],
        "doctoral_progression": [],
        "career_services": [],
        "alumni_evidence": [],
        "outcomes_confidence": "unknown",
        "summary": {
            "en": "No current programme-level employment rate, salary, employer distribution, internship conversion or doctoral-progression rate was verified.",
            "tr": "Güncel program düzeyinde istihdam oranı, maaş, işveren dağılımı, stajdan işe geçiş veya doktora geçiş oranı doğrulanmadı.",
        },
    },
    "student_sentiment_profile": {
        "student_satisfaction_score": None,
        "sentiment_confidence": "unknown",
        "sample_size_estimate": None,
        "date_range": "",
        "programme_specific_sample": None,
        "teaching_quality_sentiment": "unknown",
        "workload_sentiment": "unknown",
        "administration_sentiment": "unknown",
        "housing_sentiment": "unknown",
        "city_life_sentiment": "unknown",
        "international_student_support_sentiment": "unknown",
        "career_support_sentiment": "unknown",
        "positive_themes": [],
        "negative_themes": [],
        "summary": {
            "en": "No adequate, recent, independent programme-specific student sample was collected; no satisfaction score was fabricated.",
            "tr": "Yeterli, güncel ve bağımsız programa özgü öğrenci örneklemi toplanmadı; memnuniyet puanı üretilmedi.",
        },
        "source_ids": [],
    },
    "source_profile": {
        "source_log": [
            src("ro_ucv_master_overview", PROGRAM_URL, "Studii master", "University of Craiova Faculty of Electrical Engineering", "official_program_page", "ok", ["program", "duration", "credits"], "high", "Current faculty page lists the aerospace master's and states 2 years, 120 ECTS and full-time study.", "Güncel fakülte sayfası havacılık-uzay yüksek lisansını listeler; 2 yıl, 120 AKTS ve tam zamanlı eğitimi belirtir.", cycle="current page checked 2026-08-14"),
            src("ro_ucv_master_offer_2026", OFFER_URL, "UCV Master's Educational Offer 2026-2027", "University of Craiova", "official_program_page", "pdf", ["program", "status", "capacity"], "high", "Rendered page 7 visually checked; programme, field, full-time status and capacity 30 confirmed.", "7. sayfa render edilip görsel olarak kontrol edildi; program, alan, tam zamanlı statü ve 30 kapasite doğrulandı.", effective_date="2026-03-12", cycle="2026/2027"),
            src("ro_ucv_noneu_places_2026", NON_EU_PLACES_URL, "Places Available for Non-EU Master's Candidates 2026-2027", "University of Craiova", "official_admission_page", "pdf", ["program", "language", "non_eu_eligibility", "capacity"], "high", "Rendered page 3 visually checked; programme is Romanian, full-time and has two non-EU self-funded places.", "3. sayfa render edilip görsel olarak kontrol edildi; program Rumence, tam zamanlı ve kendi ücretini ödeyen AB dışı adaylar için iki yere sahiptir.", effective_date="2026", cycle="2026/2027"),
            src("ro_ucv_foreign_languages_2026", FOREIGN_LANGUAGES_URL, "Study Programmes Taught in Foreign Languages", "University of Craiova", "official_program_page", "pdf", ["language"], "high", "The single page was rendered and visually checked; SCIA is absent while the faculty's English-taught Sustainable Energy programme is listed.", "Tek sayfa render edilip görsel olarak kontrol edildi; SCIA yer almazken fakültenin İngilizce Sustainable Energy programı listelenir.", effective_date="2026", cycle="2026/2027"),
            src("ro_ucv_admission_conditions_2026", ADMISSION_CONDITIONS_URL, "Master's Admission Conditions 2026-2027", "University of Craiova", "official_admission_page", "pdf", ["program", "admission", "capacity"], "high", "Rendered page 8 visually checked; oral examination, arithmetic admission average and tie-breaker confirmed.", "8. sayfa render edilip görsel olarak kontrol edildi; sözlü sınav, aritmetik kabul ortalaması ve eşitlik bozma kuralı doğrulandı.", effective_date="2026-04-20", cycle="2026/2027"),
            src("ro_ucv_noneu_admission_2026", NON_EU_ADMISSION_URL, "Non-EU Citizens 2026-2027", "University of Craiova", "official_admission_page", "ok", ["admission", "non_eu_eligibility", "documents", "language", "deadline", "tuition", "payment", "visa"], "high", "Current non-EU calendar, documents, Romanian B1 rule, EUR 200 processing fee, EUR 3,500 technical master's tuition and payment sequence.", "Güncel AB dışı takvim, belgeler, Rumence B1 kuralı, 200 EUR işlem bedeli, 3.500 EUR teknik yüksek lisans ücreti ve ödeme sırası.", effective_date="2026", cycle="2026/2027"),
            src("ro_ucv_preparatory_year_2026", PREPARATORY_YEAR_URL, "Romanian Language Preparatory Year 2026-2027", "University of Craiova", "official_admission_page", "ok", ["language", "admission", "deadline", "tuition"], "high", "Current one-year/10-month preparatory route, automatic routing when proof is absent, 55 places and two application sessions.", "Güncel bir yıllık/10 aylık hazırlık rotası, kanıt yoksa otomatik yönlendirme, 55 yer ve iki başvuru oturumu.", effective_date="2026", cycle="2026/2027"),
            src("ro_ucv_study_plan", CURRICULUM_URL, "Study Plan for Master's Studies - Aerospace Engineering", "University of Craiova", "official_curriculum_page", "ok", ["curriculum", "research"], "medium", "Official undated study-plan page checked live; 21 rows, 16 credit-bearing modules and 120 ECTS were extracted. Currency must be reconfirmed because no academic cycle is printed.", "Resmî tarihsiz ders-planı sayfası canlı kontrol edildi; 21 satır, 16 kredili modül ve 120 AKTS çıkarıldı. Akademik dönem basılmadığından güncellik yeniden teyit edilmelidir.", cycle="undated official page checked 2026-08-14"),
            src("ro_ucv_labs", LABS_URL, "Faculty Laboratories", "University of Craiova Faculty of Electrical Engineering", "official_department_page", "ok", ["research"], "high", "Current faculty page lists both the Avionics Laboratory and the Complex Systems for Aerospace Engineering Laboratory.", "Güncel fakülte sayfası hem Aviyonik Laboratuvarını hem de Complex Systems for Aerospace Engineering Laboratuvarını listeler.", cycle="current page checked 2026-08-14"),
            src("ro_ucv_scia_lab", SCIA_LAB_URL, "Complex Systems for Aerospace Engineering Laboratory", "University of Craiova Faculty of Electrical Engineering", "official_department_page", "pdf", ["research", "facilities"], "medium", "The one-page inventory was rendered and visually checked; it is detailed but undated, so present-day equipment access is not assumed.", "Tek sayfalık envanter render edilip görsel olarak kontrol edildi; ayrıntılı fakat tarihsiz olduğundan güncel ekipman erişimi varsayılmaz.", cycle="undated inventory checked 2026-08-14"),
            src("ro_ucv_avionics_lab", AVIONICS_LAB_URL, "Avionics Laboratory", "University of Craiova Faculty of Electrical Engineering", "official_department_page", "pdf", ["research", "facilities"], "medium", "Official detailed avionics inventory identifies SCIA master's beneficiaries, but the document is undated and no current access guarantee is inferred.", "Resmî ayrıntılı aviyonik envanteri SCIA yüksek lisansını yararlanıcı olarak belirtir; ancak belge tarihsizdir ve güncel erişim garantisi çıkarılmaz.", cycle="undated inventory checked 2026-08-14"),
            src("ro_ucv_housing_2026", HOUSING_2026_URL, "Accommodation in Student Dormitories 2026-2027", "University of Craiova", "official_housing_page", "ok", ["housing", "deadline"], "high", "Current separate online request, 1 August deadline, electronic allocation, no-guarantee warning and appeal window.", "Güncel ayrı çevrim içi talep, 1 Ağustos tarihi, elektronik tahsis, garanti yok uyarısı ve itiraz süresi.", effective_date="2026-07-16", cycle="2026/2027"),
            src("ro_ucv_housing_description", HOUSING_DESCRIPTION_URL, "Student Halls and Cafeterias - General Description", "University of Craiova", "official_housing_page", "ok", ["housing", "living"], "medium", "Current university page states about 3,100 places in 11 halls and describes facilities; hall-specific figures contain an internal wording inconsistency and were not used as precise capacity.", "Güncel üniversite sayfası 11 yurtta yaklaşık 3.100 yer ve tesisleri açıklar; yurt bazlı rakamlarda iç ifade tutarsızlığı olduğundan kesin kapasite olarak kullanılmadı.", cycle="current page checked 2026-08-14"),
            src("ro_mfa_scholarship_2026", MFA_SCHOLARSHIP_URL, "Romanian Government MFA Scholarships for Non-EU Citizens", "Romanian Ministry of Foreign Affairs / Study in Romania", "official_scholarship_page", "ok", ["scholarship", "non_eu_eligibility", "deadline", "language", "housing"], "high", "Current 2026 eligibility, separate portal, 16 February-31 March window, Romanian-only master's rule and benefits.", "Güncel 2026 uygunluğu, ayrı portal, 16 Şubat-31 Mart penceresi, yalnız Rumence yüksek lisans kuralı ve kapsam.", effective_date="2026", cycle="2026/2027"),
            src("ro_ucv_performance_scholarship_2025_26", PERFORMANCE_SCHOLARSHIP_URL, "Performance Scholarships - Semester II 2025-2026", "University of Craiova Faculty of Electrical Engineering", "official_scholarship_page", "ok", ["scholarship"], "high", "Current faculty notice restricts performance scholarships to full-time students on state-funded places and requires Appendix 3 submission.", "Güncel fakülte duyurusu başarı burslarını devlet bütçeli tam zamanlı öğrencilere sınırlar ve Ek 3 başvurusu ister.", effective_date="2026-02-17", cycle="2025/2026"),
            src("ro_gov_master_2026", GOV_MASTER_URL, "Government Decision 192/2026 - Accredited Master's Programmes", "Romanian Ministry of Education and Research", "official_visa_or_government_page", "pdf", ["program", "language", "credits", "accreditation"], "high", "Current national list confirms Romanian, full-time research master and 120 ECTS.", "Güncel ulusal liste Rumence, tam zamanlı araştırma yüksek lisansı ve 120 AKTS'yi doğrular.", effective_date="2026-04-15", cycle="2026/2027"),
            src("the_ucv_2026", THE_RANKING_URL, "University of Craiova - World University Rankings 2026", "Times Higher Education", "other", "ok", ["ranking"], "high", "Provider page gives 1501+ overall and 1251+ engineering bands; neither is treated as aerospace-programme evidence.", "Sağlayıcı sayfası genel 1501+ ve mühendislik 1251+ bantlarını verir; hiçbiri havacılık-uzay programı kanıtı sayılmaz.", official=False, effective_date="2026", cycle="2026"),
        ],
        "evidence_map": {
            "program": ["ro_ucv_master_overview", "ro_ucv_master_offer_2026", "ro_ucv_admission_conditions_2026", "ro_gov_master_2026"],
            "language": ["ro_ucv_noneu_places_2026", "ro_ucv_foreign_languages_2026", "ro_ucv_noneu_admission_2026", "ro_gov_master_2026"],
            "admission": ["ro_ucv_admission_conditions_2026", "ro_ucv_noneu_admission_2026"],
            "non_eu_eligibility": ["ro_ucv_noneu_places_2026", "ro_ucv_noneu_admission_2026"],
            "tuition": ["ro_ucv_noneu_admission_2026", "ro_ucv_preparatory_year_2026"],
            "scholarship": ["ro_mfa_scholarship_2026", "ro_ucv_performance_scholarship_2025_26"],
            "deadline": ["ro_ucv_noneu_admission_2026", "ro_ucv_preparatory_year_2026", "ro_mfa_scholarship_2026", "ro_ucv_housing_2026"],
            "curriculum": ["ro_ucv_study_plan"],
            "housing": ["ro_ucv_housing_2026", "ro_ucv_housing_description"],
            "research": ["ro_ucv_study_plan", "ro_ucv_labs", "ro_ucv_scia_lab", "ro_ucv_avionics_lab"],
            "ranking": ["the_ucv_2026"],
        },
        "last_verified": "2026-08-14",
        "next_review_due": "2027-01-15",
        "needs_verification": True,
        "verification_notes": {
            "en": "Critical decision fields are sourced. Open items: programme-specific accepted bachelor disciplines, explicit GRE policy, dated current curriculum, exact oral-exam delivery for non-EU applicants, current lab access, mandatory external internship status, 2026/27 self-funded non-EU dormitory price, private living budget, programme-specific industry partnerships, outcomes and sentiment.",
            "tr": "Kritik karar alanları kaynaklıdır. Açık kalanlar: programa özgü kabul edilen lisans bölümleri, açık GRE politikası, tarihli güncel müfredat, AB dışı aday için sözlü sınavın kesin uygulama biçimi, güncel laboratuvar erişimi, zorunlu dış staj durumu, 2026/27 kendi ücretini ödeyen AB dışı yurt fiyatı, özel yaşam bütçesi, programa özgü sanayi ortaklıkları, sonuçlar ve öğrenci görüşleri.",
        },
        "field_confidence": {
            "program": "high",
            "language": "high",
            "admission": "high",
            "non_eu_eligibility": "high",
            "tuition": "high",
            "scholarship": "high",
            "deadline": "high",
            "curriculum": "medium",
            "housing": "high",
            "research": "medium",
            "industry": "unknown",
            "ranking": "high",
            "outcomes": "unknown",
            "student_sentiment": "unknown",
        },
    },
    "decision_summary": {
        "overall_recommendation": "strong_aircraft_avionics_and_control_option_with_major_romanian_barrier_and_limited_direct_space_breadth",
        "main_strengths": {
            "en": "A genuine 120-ECTS aerospace-engineering master's with strong avionics/GNC depth, 30 ECTS of dissertation/research, a programme-named laboratory, two verified non-EU places and comparatively low EUR 3,500 annual tuition.",
            "tr": "Güçlü aviyonik/GNC derinliği, 30 AKTS tez/araştırma, program adını taşıyan laboratuvar, doğrulanmış iki AB dışı yer ve görece düşük yıllık 3.500 EUR ücret sunan gerçek bir 120 AKTS havacılık-uzay mühendisliği yüksek lisansı.",
        },
        "main_risks": {
            "en": "Romanian-only teaching and possible preparatory year; undated curriculum and lab inventories; aircraft/avionics emphasis rather than explicit satellites or orbital mechanics; no verified external internship, employer pipeline, outcomes, current dorm price or student-sentiment sample.",
            "tr": "Yalnız Rumence eğitim ve olası hazırlık yılı; tarihsiz müfredat ve laboratuvar envanterleri; açık uydu veya yörünge mekaniği yerine uçak/aviyonik ağırlığı; doğrulanmış dış staj, işveren hattı, sonuçlar, güncel yurt fiyatı veya öğrenci görüşü örnekleminin olmaması.",
        },
        "best_for": {
            "en": "Romanian-ready applicants targeting avionics, integrated navigation, flight control, autopilots, GNC, flight dynamics, propulsion control, on-board power/EMC or applied aerospace research.",
            "tr": "Aviyonik, entegre seyrüsefer, uçuş kontrolü, otopilotlar, GNC, uçuş dinamiği, itki kontrolü, uçuş güç/EMC sistemleri veya uygulamalı havacılık-uzay araştırmasını hedefleyen Rumenceye hazır adaylar.",
        },
        "not_ideal_for": {
            "en": "English-only students; candidates primarily seeking satellites, orbital mechanics, space science, deep spacecraft systems engineering or a documented international employer-placement pipeline.",
            "tr": "Yalnız İngilizce eğitim isteyenler; esas olarak uydular, yörünge mekaniği, uzay bilimi, derin uzay aracı sistem mühendisliği veya belgeli uluslararası işveren yerleştirme hattı arayanlar.",
        },
        "application_reality": {
            "en": "A Türkiye applicant should first solve Romanian B1 or enter the separate 10-month preparatory year, then apply through EvStud in one of the April-May or June-July non-EU sessions, sit the oral examination, confirm rapidly and pay the first-year tuition within 15 days of the Ministry Letter of Acceptance.",
            "tr": "Türkiye'den aday önce Rumence B1'i çözmeli veya ayrı 10 aylık hazırlık yılına girmeli; ardından Nisan-Mayıs ya da Haziran-Temmuz AB dışı oturumlarından birinde EvStud üzerinden başvurmalı, sözlü sınava girmeli, hızla teyit vermeli ve Bakanlık Kabul Mektubundan sonra 15 gün içinde ilk yıl ücretini ödemelidir.",
        },
        "funding_reality": {
            "en": "Standard admission is self-funded and has no automatic scholarship. The meaningful full-funding route is the separate, highly competitive Romanian MFA scholarship, whose 2026 deadline was 31 March and whose final institution assignment is not guaranteed.",
            "tr": "Standart kabul kendi imkânıyla ücretlidir ve otomatik burs yoktur. Anlamlı tam finansman rotası ayrı ve çok rekabetçi Romanya Dışişleri bursudur; 2026 son tarihi 31 Mart'tı ve nihai kurum ataması garanti değildir.",
        },
        "housing_reality": {
            "en": "UCV has student halls but no guaranteed room. The 2026/27 request was separate and due 1 August; keep a private-market fallback because the current self-funded non-EU room price was not published clearly.",
            "tr": "UCV'nin öğrenci yurtları vardır ancak oda garantisi yoktur. 2026/27 talebi ayrıydı ve 1 Ağustos'ta kapanıyordu; kendi ücretini ödeyen AB dışı öğrenci için güncel oda fiyatı açık yayımlanmadığından özel piyasa yedeği tutun.",
        },
    },
    "scoring_inputs": {
        "academic_field_fit_score_seed": 84,
        "eligibility_language_score_seed": 28,
        "cost_funding_score_seed": 57,
        "career_research_score_seed": 72,
        "living_risk_score_seed": 56,
        "data_confidence_score_seed": 88,
        "student_satisfaction_score_seed": None,
        "hard_filter_flags": {
            "english_only_compatible": False,
            "requires_local_language": True,
            "non_eu_eligible": True,
            "gre_required": None,
            "funding_separate_application": True,
            "housing_not_guaranteed": True,
            "deadline_unknown_or_historical": False,
            "needs_verification": True,
        },
    },
    "data_quality": {
        "status": "partial",
        "checked_official_source_count": 16,
        "verified_fields": ["program", "language", "admission", "non_eu_eligibility", "tuition", "scholarship", "deadline", "curriculum", "research", "housing", "ranking"],
        "unverified_critical_fields": ["programme-specific accepted prior disciplines", "explicit GRE policy", "dated current curriculum", "current non-EU dormitory price", "mandatory external internship status"],
        "has_checked_source_log": True,
        "audited_at": "2026-08-14",
    },
    "quality_control": {
        "qc_status": "needs_revision",
        "checked_at": "2026-08-14",
        "failed_canary_tests": [],
        "remaining_verification_tasks": [
            {"en": "Obtain written confirmation of accepted prior-degree disciplines, explicit GRE policy and whether the oral examination is online for non-EU applicants.", "tr": "Kabul edilen önceki lisans bölümlerini, açık GRE politikasını ve AB dışı aday için sözlü sınavın çevrim içi olup olmadığını yazılı teyit edin."},
            {"en": "Obtain a curriculum with an explicit academic cycle and reconfirm all SCIA/Avionics laboratory equipment and master's access.", "tr": "Açık akademik dönem taşıyan müfredat edinin ve tüm SCIA/Aviyonik laboratuvar ekipmanını ve yüksek lisans erişimini yeniden teyit edin."},
            {"en": "Verify mandatory/optional external internship status, programme-specific partners, placement outcomes and security restrictions.", "tr": "Zorunlu/isteğe bağlı dış staj durumunu, programa özgü ortakları, yerleştirme sonuçlarını ve güvenlik kısıtlarını doğrulayın."},
            {"en": "Obtain the 2026/27 self-funded non-EU dormitory tariff and a current official Craiova living-cost budget.", "tr": "2026/27 kendi ücretini ödeyen AB dışı yurt tarifesini ve güncel resmî Craiova yaşam bütçesini edinin."},
            {"en": "Recheck 2027/28 admission, tuition, scholarship and housing dates and collect independent programme-specific student sentiment.", "tr": "2027/28 kabul, ücret, burs ve yurt tarihlerini yeniden kontrol edin; bağımsız programa özgü öğrenci görüşü toplayın."},
        ],
        "perspective_reviews": {"observer": None, "reviewer": None, "auditor": None, "student": None},
        "qc_notes": {
            "en": "Program status, non-EU access, language, price and admission process are current and high-confidence. Technical curriculum and lab fit are useful but deliberately medium-confidence because the detailed pages are undated; missing career and sentiment evidence remains explicit.",
            "tr": "Program statüsü, AB dışı erişim, dil, fiyat ve kabul süreci güncel ve yüksek güvenlidir. Teknik müfredat ve laboratuvar uygunluğu yararlıdır ancak ayrıntılı sayfalar tarihsiz olduğundan bilinçli biçimde orta güvenlidir; eksik kariyer ve öğrenci görüşü kanıtı açık tutulur.",
        },
    },
}

serialized = json.dumps(record, ensure_ascii=False)
for forbidden in ("POLITEHNICA", "Bucharest", "upb.ro"):
    if forbidden in serialized:
        raise AssertionError(f"Stale template data found: {forbidden}")

records.append(record)
save(DB_PATH, records)

queue = load(QUEUE_PATH)
candidate = next(item for item in queue["candidates"] if item.get("candidate_id") == RECORD_ID)
candidate["discovery_status"] = "promoted_to_full_record"
candidate["known_cautions"] = [{
    "en": "Current 2026/27 sources confirm Romanian-only teaching, 120 ECTS, oral admission, capacity 30, two non-EU self-funded places and EUR 3,500 tuition. The official study plan and detailed lab inventories are undated, so their current availability remains medium-confidence.",
    "tr": "Güncel 2026/27 kaynakları yalnız Rumence eğitimi, 120 AKTS'yi, sözlü kabulü, 30 kapasiteyi, kendi ücretini ödeyen iki AB dışı yeri ve 3.500 EUR ücreti doğrular. Resmî ders planı ile ayrıntılı laboratuvar envanterleri tarihsizdir; bu nedenle güncel erişimleri orta güven düzeyindedir.",
}]
save(QUEUE_PATH, queue)

discovery = load(DISCOVERY_PATH)
candidate = next(item for item in discovery["included_candidates"] if item.get("candidate_id") == RECORD_ID)
candidate["status"] = "promoted_to_full_record"
discovery["discovery_result"]["full_v2_records"] = 9
discovery["discovery_result"]["queued_for_full_research"] = 1
save(DISCOVERY_PATH, discovery)

scan_log = load(SCAN_PATH)
scan = next(item for item in scan_log["scans"] if item.get("country") == "Romania")
scan["full_records_added"] = 9
scan["notes"] = {
    "en": "Nine of ten Romanian candidates are now native V2. University of Craiova's Complex Systems for Aerospace Engineering was promoted after current sources confirmed Romanian delivery, 120 ECTS, oral admission, 30 total places, two non-EU places and EUR 3,500 annual tuition. Its avionics/GNC-heavy undated curriculum and lab inventories remain medium-confidence. The Military Technical Academy candidate remains queued.",
    "tr": "On Romanya adayının dokuzu artık doğal V2'dir. Craiova Üniversitesi Complex Systems for Aerospace Engineering; güncel kaynaklar Rumence eğitimi, 120 AKTS'yi, sözlü kabulü, toplam 30 yeri, iki AB dışı yeri ve yıllık 3.500 EUR ücreti doğruladıktan sonra tam kayda taşındı. Aviyonik/GNC ağırlıklı tarihsiz müfredatı ve laboratuvar envanterleri orta güven düzeyinde kalır. Askerî Teknik Akademi adayı kuyruktadır.",
}
save(SCAN_PATH, scan_log)

print("Added University of Craiova native V2 record; Romania discovery is now 9/10 full records.")
