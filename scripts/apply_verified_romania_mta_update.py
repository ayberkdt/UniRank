"""Promote the final Romanian discovery candidate to a source-grounded V2 record."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data_base" / "romania.json"
TEMPLATE_PATH = ROOT / "research_templates" / "program_record_v2.json"
QUEUE_PATH = ROOT / "research_queue" / "program_candidates_v2.json"
DISCOVERY_PATH = ROOT / "reports" / "romania_programme_discovery_2026-08-14.json"
SCAN_PATH = ROOT / "research_queue" / "country_scan_log_v2.json"
RECORD_ID = "ro-military-technical-academy-aerospace-systems-engineering-msc"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def save(path: Path, payload) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def source(
    source_id: str,
    url: str,
    title: str,
    publisher: str,
    source_type: str,
    access_status: str,
    date: str,
    cycle: str,
    fields: list[str],
    confidence: str,
    note_en: str,
    note_tr: str,
) -> dict:
    return {
        "source_id": source_id,
        "url": url,
        "final_url": url,
        "title": title,
        "publisher": publisher,
        "source_type": source_type,
        "official": True,
        "access_status": access_status,
        "published_or_effective_date": date,
        "applicable_academic_cycle": cycle,
        "last_checked": "2026-08-14",
        "relevant_fields": fields,
        "confidence": confidence,
        "notes": {"en": note_en, "tr": note_tr},
    }


def main() -> None:
    records = load(DB_PATH)
    if any(item.get("id") == RECORD_ID for item in records):
        raise RuntimeError(f"Record already exists: {RECORD_ID}")

    record = load(TEMPLATE_PATH)
    record.update(
        {
            "id": RECORD_ID,
            "catalog_status": "researched_with_critical_unknowns",
            "country_code": "RO",
            "country": "Romania",
        }
    )
    record["institution_profile"].update(
        {
            "institution_id": "ro-military-technical-academy-ferdinand-i",
            "name": "Military Technical Academy Ferdinand I",
            "native_name": "Academia Tehnică Militară Ferdinand I",
            "short_name": "ATM Ferdinand I",
            "institution_type": "public_military_higher_education_institution",
            "official_url": "https://mta.ro/",
        }
    )
    record["location"].update(
        {
            "campus": "Bulevardul George Coșbuc 39-49",
            "city": "Bucharest",
            "region": "Bucharest",
            "country": "Romania",
            "location_confidence": "high",
        }
    )
    record["program_profile"].update(
        {
            "name": "Aeronautical Systems Engineering",
            "native_name": "Ingineria sistemelor aeronautice",
            "degree_award": "Master's degree",
            "degree_class": "research_master",
            "duration": {"value": 1.5, "unit": "years"},
            "credits": {"value": 90, "system": "ECTS"},
            "department": "Department of Integrated Aviation and Mechanics Systems",
            "faculty_or_school": "Faculty of Aircraft and Military Vehicles",
            "official_url": "https://www.edu.ro/sites/default/files/fisiere%20articole/HG_192_2026_Anexe_domenii_master.pdf",
            "program_status": "active",
            "relevance_status": "strong",
        }
    )

    record["eligibility_profile"].update(
        {
            "eligible_for_non_eu": None,
            "required_previous_degree": {
                "en": "The 2025/26 rules allowed applicants with a bachelor's degree or equivalent to apply regardless of the bachelor field; the 2026/27 rule has not been published.",
                "tr": "2025/26 kuralları lisans diploması veya eşdeğeri bulunan adayların lisans alanından bağımsız başvurmasına izin verdi; 2026/27 kuralı yayımlanmadı.",
            },
            "selection_method": "historical_on_campus_specialty_interview",
            "selection_criteria": [
                {"criterion": "specialty_interview", "weight_percent": 80, "minimum_grade": 6, "cycle": "2025/2026"},
                {"criterion": "bachelor_graduation_average", "weight_percent": 20, "cycle": "2025/2026"},
            ],
            "admission_risk": "high",
            "required_documents": [
                "application_form",
                "birth_certificate",
                "bachelor_diploma_and_supplements",
                "upper_secondary_diploma",
                "curriculum_vitae",
                "authenticity_and_gdpr_declaration",
                "proof_of_application_fee_or_exemption",
                "name_change_document_if_applicable",
                "defence_employer_approval_only_for_state_funded_route",
            ],
            "application_portals": [
                {
                    "mode": "historical_email_application",
                    "address": "secretariat.facultatea.B@mta.ro",
                    "cycle": "2025/2026",
                    "source_ids": ["ro_mta_master_admission_2025"],
                }
            ],
            "interview": {
                "required": True,
                "format": "on_campus_specialty_interview_historical_cycle",
                "notes": {
                    "en": "The ISA-specific 2025 schedule required attendance at the academy and an interview on 10 September 2025. The 2026/27 format is unknown.",
                    "tr": "ISA'ya özgü 2025 takvimi akademide hazır bulunmayı ve 10 Eylül 2025'te mülakatı gerektiriyordu. 2026/27 biçimi bilinmiyor.",
                },
            },
            "gre": {
                "policy": "not_listed_in_2025_official_requirements",
                "test_type": "unknown",
                "minimum_scores": {},
                "recommended_scores": {},
                "validity_rule": "",
                "waiver_rules": [],
                "source_ids": ["ro_mta_master_admission_2025"],
            },
            "admission_mode": "historical_fee_or_defence_budget_route",
            "notes_for_turkish_students": {
                "en": "Do not treat the historical civilian fee route as proof that a Turkish citizen is eligible. Obtain written confirmation covering citizenship, diploma recognition, Romanian-language proof, security access and the 2026/27 fee before applying.",
                "tr": "Geçmiş sivil ücretli rotayı Türkiye vatandaşının uygun olduğunun kanıtı saymayın. Başvurmadan önce vatandaşlık, diploma tanıma, Rumence belgesi, güvenlik erişimi ve 2026/27 ücretini kapsayan yazılı teyit alın.",
            },
        }
    )

    record["language_profile"].update(
        {
            "teaching_languages": ["Romanian"],
            "teaching_language": ["Romanian"],
            "english_required": False,
            "local_language_entry_requirement": "not_published_for_foreign_applicants",
            "local_language_for_curriculum": "required",
            "local_language_for_life_or_internship": {
                "en": "Romanian is the verified teaching language and is operationally essential in this defence-oriented environment.",
                "tr": "Rumence doğrulanmış eğitim dilidir ve savunma odaklı bu ortamda operasyonel olarak zorunludur.",
            },
            "mixed_language_warning": {
                "en": "English-language bibliographic items do not make the programme English-taught. The 2026 government list explicitly states Romanian.",
                "tr": "İngilizce kaynak kitaplar programı İngilizce eğitimli yapmaz. 2026 devlet listesi dili açıkça Rumence gösterir.",
            },
            "language_risk": "high",
        }
    )

    record["cost_profile"].update(
        {
            "academic_cycle": "2026/2027",
            "application_fee_items": [
                {
                    "amount": 200,
                    "currency": "RON",
                    "period": "one_time",
                    "applicant_scope": "2025_2026_master_applicant",
                    "academic_cycle": "2025/2026",
                    "mandatory": True,
                    "basis": "Historical official master-admission regulation; exemptions were listed",
                    "source_ids": ["ro_mta_master_admission_2025"],
                }
            ],
            "cost_risk": "high",
            "notes": {
                "en": "A fee-paying civilian route operated in 2025, but neither the 2026/27 annual tuition nor payment/refund rules were found. The RON 200 figure is only the historical application fee, not tuition.",
                "tr": "2025'te ücretli sivil rota işledi; ancak 2026/27 yıllık öğrenim ücreti ile ödeme/iade kuralları bulunamadı. 200 RON yalnız geçmiş başvuru bedelidir, öğrenim ücreti değildir.",
            },
        }
    )
    record["scholarship_profile"].update(
        {
            "application_mode": "unknown",
            "funding_risk": "high",
            "notes": {
                "en": "No current official source established an institutional award or Romanian MFA scholarship eligibility for this programme. Budget-funded places in the historical rules were restricted to personnel already employed in the national defence, public-order or security system.",
                "tr": "Güncel resmî kaynak bu program için kurum bursunu veya Romanya Dışişleri bursu uygunluğunu kanıtlamadı. Geçmiş kurallardaki devlet bütçeli yerler, ulusal savunma, kamu düzeni veya güvenlik sisteminde hâlihazırda çalışan personelle sınırlıydı.",
            },
        }
    )
    record["living_profile"].update(
        {
            "housing_access": "unknown",
            "student_housing_available": True,
            "housing_options": [
                {
                    "name": "Military Technical Academy student accommodation",
                    "type": "institution_level_dormitory_stock",
                    "capacity": 849,
                    "access_for_fee_or_international_students": "unknown",
                    "source_ids": ["ro_study_in_romania_mta_2025"],
                }
            ],
            "official_living_cost_items": [
                {
                    "amount": 680,
                    "currency": "EUR",
                    "period": "month",
                    "applicant_scope": "general_bucharest_resident_context",
                    "academic_cycle": "website_checked_2026_08_14",
                    "mandatory": False,
                    "basis": "Study in Romania Bucharest city figure explicitly excluding rent; not an MTA student budget",
                    "source_ids": ["ro_study_in_romania_bucharest"],
                }
            ],
            "housing_risk": "high",
            "living_risk": "high",
            "notes": {
                "en": "The national portal reports 849 institution-level dormitory places and EUR 680/month for Bucharest excluding rent, but it publishes no MTA allocation right, fee or guarantee for civilian/international students.",
                "tr": "Ulusal portal kurum düzeyinde 849 yurt yeri ve Bükreş için kira hariç aylık 680 EUR bildirir; ancak sivil/uluslararası öğrenci için MTA tahsis hakkı, ücret veya garanti yayımlamaz.",
            },
        }
    )

    themes = [
        "communication_navigation_surveillance_and_airspace_organization",
        "digital_systems_onboard_computers_and_flight_simulators",
        "advanced_modelling_and_simulation_of_aircraft_structures",
        "advanced_flight_dynamics_stability_and_aircraft_control",
        "advanced_propulsion_systems_for_air_vehicles",
        "artificial_intelligence_in_aeronautical_systems",
        "data_processing_and_computer_aided_design",
    ]
    record["curriculum_profile"].update(
        {
            "academic_cycle": "programme_themes_from_2022_brochure_current_programme_status_2026_2027",
            "specializations": themes,
            "course_count": {"minimum": None, "maximum": None, "counting_rule": "official_course_level_plan_not_found"},
            "thesis": {"required": True, "credits": None, "options": []},
            "internship": {
                "required": None,
                "credits": None,
                "notes": {
                    "en": "No programme-level study plan was found to establish internship requirements.",
                    "tr": "Staj zorunluluğunu kanıtlayan program düzeyinde ders planı bulunamadı.",
                },
            },
            "curriculum_urls": ["https://mta.ro/wp-content/uploads/2025/05/Brosura-ATM.pdf"],
        }
    )
    record["category_profile"].update(
        {
            "primary_categories": ["aerospace_engineering", "avionics_navigation", "flight_dynamics_control"],
            "secondary_categories": ["aerospace_propulsion", "aerospace_structures", "artificial_intelligence", "uav_systems"],
            "subcategories": ["aircraft_navigation", "onboard_computers", "flight_simulation", "aircraft_stability", "aircraft_control", "jet_propulsion"],
            "normalized_tags": ["aerospace", "aeronautical_systems", "avionics", "navigation", "flight_dynamics", "control", "propulsion", "structures", "uav", "ai"],
            "category_scores": {
                "space_systems": 20,
                "satellite_systems": 0,
                "gnc": 78,
                "propulsion": 72,
                "aerodynamics_cfd": 55,
                "structures_materials": 62,
                "space_science": 0,
            },
            "category_evidence": [
                "The programme-specific brochure and 2025 admission syllabus support aircraft navigation, avionics, flight dynamics/control, propulsion and structures. No official source found an orbital, satellite or space-science component."
            ],
        }
    )
    record["research_profile"].update(
        {
            "research_areas": ["aerospace systems", "UAV command and control", "aircraft aerodynamics", "aircraft structures", "propulsion", "avionics"],
            "labs": [
                {"name": "Aerospace Systems and Technologies Laboratory", "source_ids": ["ro_mta_cesatas"]},
                {"name": "Fluid Mechanics and Hydraulic Systems Laboratory", "source_ids": ["ro_mta_cesatas"]},
                {"name": "Thermotechnics Laboratory", "source_ids": ["ro_mta_cesatas"]},
            ],
            "research_centers": [
                {"name": "CESATAS - Centre of Excellence in Self-Propelled Systems and Defence and Security Technologies", "source_ids": ["ro_mta_cesatas"]}
            ],
            "research_opportunity_for_masters": "plausible_but_programme_specific_access_not_published",
            "research_strength_score": 76,
            "summary": {
                "en": "CESATAS explicitly supports the Faculty of Aircraft and Military Vehicles with fundamental and applied aerospace research, an aerospace-systems laboratory and UAV command/control work. Programme-specific thesis access and civilian security restrictions remain unverified.",
                "tr": "CESATAS, Uçak ve Askerî Araçlar Fakültesini temel ve uygulamalı havacılık-uzay araştırması, havacılık-uzay sistemleri laboratuvarı ve İHA komuta/kontrol çalışmalarıyla açıkça destekler. Programa özgü tez erişimi ve sivil güvenlik kısıtları doğrulanmadı.",
            },
        }
    )
    record["industry_ecosystem_profile"].update(
        {
            "internship_access": "unknown",
            "industry_thesis_access": "unknown",
            "career_relevance": {
                "en": "The technical themes are relevant to aircraft, avionics, propulsion and UAV roles, but no programme-specific civilian employer pipeline or placement outcome was verified.",
                "tr": "Teknik temalar uçak, aviyonik, itki ve İHA rollerine uygundur; ancak programa özgü sivil işveren hattı veya yerleşim sonucu doğrulanmadı.",
            },
            "summary": {
                "en": "Do not convert the academy's defence status or Erasmus military-academy partners into an employment promise. Security, nationality and export-control constraints require direct confirmation.",
                "tr": "Akademinin savunma statüsünü veya Erasmus askerî akademi ortaklarını iş garantisine çevirmeyin. Güvenlik, vatandaşlık ve ihracat kontrolü kısıtları doğrudan teyit gerektirir.",
            },
        }
    )
    record["application_timeline_profile"].update(
        {
            "target_academic_cycle": "2026/2027",
            "intake_terms": ["autumn"],
            "historical_deadline_patterns": [
                {
                    "cycle": "2025/2026",
                    "application_window": "2025-08-25/2025-09-05T12:00",
                    "programme_interview": "2025-09-10T09:00/14:00",
                    "source_ids": ["ro_mta_master_admission_2025", "ro_mta_isa_schedule_2025"],
                }
            ],
            "result_timing": {
                "en": "The 2025 programme schedule published final results at 15:00 on the interview day; no 2026/27 result schedule is published.",
                "tr": "2025 program takvimi nihai sonuçları mülakat günü 15.00'te yayımladı; 2026/27 sonuç takvimi yayımlanmadı.",
            },
            "pre_enrolment_required": None,
            "timeline_risk": "high",
            "planning_advice": {
                "en": "Use the 2025 dates only as historical evidence, not as a forecast. Ask the faculty for the 2026/27 master regulation and non-EU route before preparing travel for an on-campus interview.",
                "tr": "2025 tarihlerini tahmin olarak değil yalnız geçmiş kanıt olarak kullanın. Yüz yüze mülakat seyahatini planlamadan önce fakülteden 2026/27 yüksek lisans yönetmeliğini ve AB dışı rotayı isteyin.",
            },
        }
    )
    record["ranking_profile"].update(
        {
            "prestige_summary": {
                "en": "No current major institutional or aerospace subject ranking was verified. Military specialization and technical fit must be evaluated from the authorised programme and research evidence, not inferred prestige.",
                "tr": "Güncel büyük kurum veya havacılık-uzay alan sıralaması doğrulanmadı. Askerî uzmanlaşma ve teknik uygunluk, varsayılan prestijden değil yetkili program ve araştırma kanıtından değerlendirilmelidir.",
            }
        }
    )
    record["outcomes_profile"].update(
        {
            "summary": {
                "en": "No official ISA-specific employment, salary, doctoral-progression or civilian international placement data was found.",
                "tr": "ISA'ya özgü resmî istihdam, maaş, doktora geçişi veya sivil uluslararası yerleşim verisi bulunamadı.",
            }
        }
    )
    record["student_sentiment_profile"].update(
        {
            "summary": {
                "en": "No sufficient recent, independent, programme-specific student sample was found; no satisfaction score is assigned.",
                "tr": "Yeterli, güncel, bağımsız ve programa özgü öğrenci örneklemi bulunamadı; memnuniyet puanı verilmedi.",
            }
        }
    )

    source_log = [
        source("ro_mta_gov_master_2026", "https://www.edu.ro/sites/default/files/fisiere%20articole/HG_192_2026_Anexe_domenii_master.pdf", "Government Decision 192/2026 - authorised master's fields and programmes", "Romanian Ministry of Education / Official Gazette", "official_program_page", "pdf", "2026-04-15", "2026/2027", ["program", "language", "credits", "capacity", "status"], "high", "Rendered pages 113-114 visually checked: ISA is Romanian, full-time, research type, 90 ECTS, maximum capacity 50.", "113-114. sayfalar render edilip görsel kontrol edildi: ISA Rumence, tam zamanlı, araştırma türü, 90 AKTS ve azami 50 kapasitelidir."),
        source("ro_mta_master_admission_2025", "https://mta.ro/wp-content/uploads/2025/04/Regulament-admitere-Master-2025-_site.pdf", "Master Admission Regulation 2025/2026", "Military Technical Academy Ferdinand I", "official_admission_page", "pdf", "2025-01-23", "2025/2026", ["admission", "deadline", "documents", "application_fee", "civilian_fee_route"], "medium", "All seven pages rendered and checked; current-cycle rules are not yet published.", "Yedi sayfanın tamamı render edilip kontrol edildi; güncel dönem kuralları henüz yayımlanmadı."),
        source("ro_mta_isa_schedule_2025", "https://mta.ro/wp-content/uploads/2025/06/GRAFIC-ADMITERE-MASTER.pdf", "ISA Master Admission Commission and Schedule - September 2025", "Military Technical Academy Ferdinand I", "official_admission_page", "pdf", "2025-06-20", "2025/2026", ["admission", "deadline", "interview", "result_timing"], "medium", "Rendered and checked; confirms an on-campus interview on 10 September 2025.", "Render edilip kontrol edildi; 10 Eylül 2025'te yüz yüze mülakatı doğrular."),
        source("ro_mta_isa_results_2025", "https://mta.ro/wp-content/uploads/2025/09/REZULTATE-ADMITERE-MASTER-ISA-2025.pdf", "ISA Master Admission Results - September 2025", "Military Technical Academy Ferdinand I", "official_admission_page", "pdf", "2025-09", "2025/2026", ["admission", "civilian_fee_route", "selection"], "medium", "Rendered and checked; separate fee-paying and state-funded result tables prove the historical civilian fee route.", "Render edilip kontrol edildi; ayrı ücretli ve devlet bütçeli sonuç tabloları geçmiş sivil ücretli rotayı kanıtlar."),
        source("ro_mta_isa_syllabus_2025", "https://mta.ro/wp-content/uploads/2025/03/Tematica_bibliografie_admitere_master_ISA-2025.pdf", "ISA Master Admission Topics and Bibliography 2025/2026", "Military Technical Academy Ferdinand I", "official_admission_page", "pdf", "2025-03-31", "2025/2026", ["admission", "technical_fit"], "medium", "Rendered and checked; this is an admission syllabus, not the degree curriculum.", "Render edilip kontrol edildi; bu belge derece müfredatı değil kabul konu listesidir."),
        source("ro_mta_brochure_2022", "https://mta.ro/wp-content/uploads/2025/05/Brosura-ATM.pdf", "ATM Ferdinand I Presentation Brochure", "Military Technical Academy Ferdinand I", "official_program_page", "pdf", "2022-05-05", "undated_currentness_recheck", ["program", "duration", "curriculum", "research"], "medium", "Rendered page 10 visually checked; programme themes and 1.5-year/90-credit format are useful but the brochure is dated 2022 and contains an adjacent acronym typo.", "10. sayfa render edilip görsel kontrol edildi; program temaları ve 1,5 yıl/90 kredi biçimi yararlıdır ancak broşür 2022 tarihlidir ve komşu bir kısaltma yazım hatası içerir."),
        source("ro_mta_academic_calendar_2026", "https://mta.ro/wp-content/uploads/2026/05/Structura-2026-2027.pdf", "Educational Activities Calendar 2026/2027", "Military Technical Academy Ferdinand I", "official_university_policy_page", "pdf", "2026-05-07", "2026/2027", ["program", "academic_calendar"], "medium", "Rendered and checked; confirms active master teaching structures but does not identify ISA's group code.", "Render edilip kontrol edildi; aktif yüksek lisans öğretim yapısını doğrular ancak ISA grup kodunu belirlemez."),
        source("ro_mta_cesatas", "https://mta.ro/cesatas", "CESATAS Centre of Excellence", "Military Technical Academy Ferdinand I", "official_lab_page", "ok", "2023-12-05", "current_page_checked_2026", ["research", "labs", "facilities"], "medium", "Accessible current page names aerospace research and laboratories; programme-specific civilian access is not stated.", "Erişilebilir güncel sayfa havacılık-uzay araştırması ve laboratuvarları adlandırır; programa özgü sivil erişim belirtilmez."),
        source("ro_study_in_romania_mta_2025", "https://studyinromania.gov.ro/atm", "Military Technical Academy Ferdinand I - institution profile", "Study in Romania / Romanian government", "official_housing_page", "ok", "2025", "institution_profile", ["housing", "international_students", "institution_type"], "medium", "Government portal reports 849 dormitory places and zero international students in its 2025 key details; access rights and prices are absent.", "Devlet portalı 2025 temel bilgilerinde 849 yurt yeri ve sıfır uluslararası öğrenci bildirir; erişim hakkı ve fiyat yoktur."),
        source("ro_study_in_romania_bucharest", "https://studyinromania.gov.ro/pickcity/bucharest", "Study in Bucharest", "Study in Romania / Romanian government", "official_cost_of_living_page", "ok", "2026_snapshot", "current_context", ["housing", "living_cost"], "medium", "Publishes EUR 680/month excluding rent as a Bucharest city context, not an MTA student budget.", "Bükreş şehir bağlamı için kira hariç aylık 680 EUR yayımlar; bu MTA öğrenci bütçesi değildir."),
    ]
    record["source_profile"].update(
        {
            "source_log": source_log,
            "evidence_map": {
                "program": ["ro_mta_gov_master_2026", "ro_mta_brochure_2022", "ro_mta_academic_calendar_2026"],
                "language": ["ro_mta_gov_master_2026"],
                "admission": ["ro_mta_master_admission_2025", "ro_mta_isa_schedule_2025", "ro_mta_isa_results_2025", "ro_mta_isa_syllabus_2025"],
                "non_eu_eligibility": [],
                "tuition": [],
                "scholarship": [],
                "deadline": ["ro_mta_master_admission_2025", "ro_mta_isa_schedule_2025"],
                "curriculum": ["ro_mta_brochure_2022"],
                "housing": ["ro_study_in_romania_mta_2025", "ro_study_in_romania_bucharest"],
                "research": ["ro_mta_cesatas", "ro_mta_brochure_2022"],
            },
            "last_verified": "2026-08-14",
            "next_review_due": "2026-09-01",
            "needs_verification": True,
            "verification_notes": {
                "en": "Current programme status, language, credits and capacity are high-confidence. Current non-EU eligibility, tuition, scholarship, admission dates, Romanian proof, detailed course plan, housing entitlement, security restrictions, outcomes and sentiment remain unknown.",
                "tr": "Güncel program statüsü, dil, kredi ve kapasite yüksek güvenlidir. Güncel AB dışı uygunluk, öğrenim ücreti, burs, kabul tarihleri, Rumence belgesi, ayrıntılı ders planı, yurt hakkı, güvenlik kısıtları, sonuçlar ve öğrenci görüşleri bilinmiyor.",
            },
            "field_confidence": {
                "program": "high",
                "language": "high",
                "admission": "medium",
                "non_eu_eligibility": "unknown",
                "tuition": "unknown",
                "scholarship": "unknown",
                "deadline": "medium",
                "curriculum": "medium",
                "housing": "medium",
                "research": "medium",
                "industry": "unknown",
                "ranking": "unknown",
                "outcomes": "unknown",
                "student_sentiment": "unknown",
            },
        }
    )
    record["decision_summary"].update(
        {
            "overall_recommendation": "conditional_high_risk_until_noneu_access_is_confirmed",
            "main_strengths": {
                "en": "A current authorised 90-ECTS research master's with concentrated aircraft-systems coverage in navigation/avionics, flight dynamics and control, propulsion, structures, AI and UAV-related research infrastructure.",
                "tr": "Seyrüsefer/aviyonik, uçuş dinamiği ve kontrolü, itki, yapılar, yapay zekâ ve İHA bağlantılı araştırma altyapısında yoğun uçak-sistemleri kapsamı sunan, güncel yetkili 90 AKTS araştırma yüksek lisansı.",
            },
            "main_risks": {
                "en": "Romanian-only teaching; no published 2026/27 non-EU route, tuition or deadline; a military-security environment with unverified nationality/access restrictions; no course-level plan, programme outcomes or student sample.",
                "tr": "Yalnız Rumence eğitim; yayımlanmış 2026/27 AB dışı rota, ücret veya son tarih yok; vatandaşlık/erişim kısıtları doğrulanmamış askerî güvenlik ortamı; ders düzeyi plan, program sonucu veya öğrenci örneklemi yok.",
            },
            "best_for": {
                "en": "Romanian-ready candidates whose citizenship and security eligibility are confirmed in writing and who target aircraft systems, avionics/navigation, flight control, propulsion, structures or UAV R&D.",
                "tr": "Vatandaşlık ve güvenlik uygunluğu yazılı teyit edilmiş, Rumenceye hazır ve uçak sistemleri, aviyonik/seyrüsefer, uçuş kontrolü, itki, yapılar veya İHA AR-GE hedefleyen adaylar.",
            },
            "not_ideal_for": {
                "en": "English-only applicants, satellite/orbital/space-science seekers, or anyone needing predictable non-EU admission, tuition, scholarships, housing or civilian placement evidence.",
                "tr": "Yalnız İngilizce isteyenler, uydu/yörünge/uzay bilimi arayanlar veya öngörülebilir AB dışı kabul, ücret, burs, yurt ya da sivil yerleşim kanıtına ihtiyaç duyanlar.",
            },
            "application_reality": {
                "en": "The 2025 route used email filing, a RON 200 application fee and an on-campus specialty interview weighted 80%. A Turkish applicant must not reuse those dates or assume eligibility; written 2026/27 confirmation is a hard gate.",
                "tr": "2025 rotası e-posta dosyalama, 200 RON başvuru bedeli ve %80 ağırlıklı yüz yüze uzmanlık mülakatı kullandı. Türkiye'den aday bu tarihleri yeniden kullanmamalı veya uygunluğu varsaymamalı; yazılı 2026/27 teyidi kesin eşiktir.",
            },
            "funding_reality": {
                "en": "Budget as fully self-funded until the academy confirms both tuition and an award in writing. Historical state-funded places were for personnel already inside Romania's defence/public-order/security system.",
                "tr": "Akademi hem ücreti hem de bursu yazılı teyit edene kadar tamamen kendi finansmanınızla planlayın. Geçmiş devlet bütçeli yerler Romanya savunma/kamu düzeni/güvenlik sistemi içinde çalışan personel içindi.",
            },
            "housing_reality": {
                "en": "Dormitory stock exists at institution level, but no source grants a civilian or international ISA student a room or publishes a price. Treat private Bucharest housing as the fallback.",
                "tr": "Kurum düzeyinde yurt stoku vardır; ancak hiçbir kaynak sivil veya uluslararası ISA öğrencisine oda hakkı vermez ya da fiyat yayımlamaz. Özel Bükreş konutunu yedek plan sayın.",
            },
        }
    )
    record["scoring_inputs"].update(
        {
            "academic_field_fit_score_seed": 86,
            "eligibility_language_score_seed": 18,
            "cost_funding_score_seed": 24,
            "career_research_score_seed": 68,
            "living_risk_score_seed": 38,
            "data_confidence_score_seed": 62,
            "hard_filter_flags": {
                "english_only_compatible": False,
                "requires_local_language": True,
                "non_eu_eligible": None,
                "gre_required": None,
                "funding_separate_application": None,
                "housing_not_guaranteed": True,
                "deadline_unknown_or_historical": True,
                "needs_verification": True,
            },
        }
    )
    record["data_quality"] = {
        "status": "partial",
        "checked_official_source_count": len(source_log),
        "verified_fields": ["program", "language", "admission", "deadline", "curriculum", "research", "housing"],
        "unverified_critical_fields": ["non_eu_eligibility", "tuition", "scholarship", "current_2026_2027_deadline", "romanian_language_proof", "course_level_curriculum", "housing_entitlement_and_price", "security_restrictions"],
        "has_checked_source_log": True,
        "audited_at": "2026-08-14",
    }
    record["quality_control"].update(
        {
            "qc_status": "needs_revision",
            "checked_at": "2026-08-14",
            "remaining_verification_tasks": [
                {"en": "Obtain written 2026/27 confirmation of Turkish/non-EU eligibility, diploma recognition, Romanian proof and security restrictions.", "tr": "Türkiye/AB dışı uygunluğu, diploma tanıma, Rumence belgesi ve güvenlik kısıtları için yazılı 2026/27 teyidi alın."},
                {"en": "Obtain the 2026/27 master regulation, annual tuition, payment/refund rules and current fee-seat count.", "tr": "2026/27 yüksek lisans yönetmeliğini, yıllık ücreti, ödeme/iade kurallarını ve güncel ücretli yer sayısını alın."},
                {"en": "Obtain a dated course-level study plan with course count, credits, thesis and internship requirements.", "tr": "Ders sayısı, krediler, tez ve staj koşullarını içeren tarihli ders düzeyi planı alın."},
                {"en": "Confirm civilian/international access to CESATAS, dormitories, Erasmus mobility and employer-facing projects.", "tr": "Sivil/uluslararası öğrencinin CESATAS, yurt, Erasmus hareketliliği ve işveren bağlantılı projelere erişimini teyit edin."},
            ],
            "qc_notes": {
                "en": "The record is useful as a high-risk option, not as an application-ready recommendation. All unknowns are deliberate; no 2026 deadline or tuition was estimated from 2025.",
                "tr": "Kayıt başvuruya hazır öneri değil, yüksek riskli seçenek olarak yararlıdır. Tüm bilinmeyenler bilinçlidir; 2025'ten 2026 son tarihi veya ücret tahmin edilmedi.",
            },
        }
    )

    serialized = json.dumps(record, ensure_ascii=False)
    forbidden_claims = ["eligible_for_non_eu\": true", "tuition_eur_per_year_estimated\": 0"]
    if any(claim in serialized.lower() for claim in forbidden_claims):
        raise AssertionError("Unsupported MTA claim survived record construction")

    records.append(record)
    save(DB_PATH, records)

    queue = load(QUEUE_PATH)
    candidate = next(item for item in queue["candidates"] if item.get("candidate_id") == RECORD_ID)
    candidate["program_name"] = "Aeronautical Systems Engineering"
    candidate["discovery_status"] = "promoted_to_full_record_with_critical_unknowns"
    candidate["known_cautions"] = [record["decision_summary"]["main_risks"]]
    save(QUEUE_PATH, queue)

    discovery = load(DISCOVERY_PATH)
    candidate = next(item for item in discovery["included_candidates"] if item.get("candidate_id") == RECORD_ID)
    candidate["programme"] = "Aeronautical Systems Engineering"
    candidate["status"] = "promoted_to_full_record_with_critical_unknowns"
    result = discovery["discovery_result"]
    result["full_v2_records"] = 10
    result["queued_for_full_research"] = 0
    result["country_complete"] = False
    result["open_work"] = {
        "en": "All ten named Romanian candidates now have V2 records. Country research remains open because the Military Technical Academy has not published 2026/27 non-EU eligibility, tuition, scholarship, deadline, detailed curriculum or housing access, and adjacent-programme discovery must be re-run each cycle.",
        "tr": "Adlandırılmış on Romanya adayının tamamı artık V2 kaydına sahiptir. Askerî Teknik Akademi 2026/27 AB dışı uygunluk, ücret, burs, son tarih, ayrıntılı müfredat veya yurt erişimini yayımlamadığı ve komşu program keşfi her dönem yeniden çalıştırılması gerektiği için ülke araştırması açık kalır.",
    }
    save(DISCOVERY_PATH, discovery)

    scan_log = load(SCAN_PATH)
    scan = next(item for item in scan_log["scans"] if item.get("country") == "Romania")
    scan["status"] = "named_candidate_discovery_complete_research_gaps_open"
    scan["full_records_added"] = 10
    scan["notes"] = result["open_work"]
    save(SCAN_PATH, scan_log)

    print("Added MTA Ferdinand I ISA as Romania record 10/10 with critical unknowns preserved.")


if __name__ == "__main__":
    main()
