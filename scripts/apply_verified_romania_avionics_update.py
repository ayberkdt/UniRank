"""Promote POLITEHNICA Bucharest Avionics and Aerospace Navigation to native V2."""

from __future__ import annotations

import copy
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data_base" / "romania.json"
QUEUE_PATH = ROOT / "research_queue" / "program_candidates_v2.json"
DISCOVERY_PATH = ROOT / "reports" / "romania_programme_discovery_2026-08-14.json"
SCAN_PATH = ROOT / "research_queue" / "country_scan_log_v2.json"
RECORD_ID = "ro-politehnica-bucharest-avionics-aerospace-navigation-msc"
CURRICULUM_URL = "https://www.aero.pub.ro/wp-content/uploads/2025/10/2025_27_PLi_M_09_FIA_IA_ANA.pdf"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path: Path, payload) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


records = load(DB_PATH)
if any(record.get("id") == RECORD_ID for record in records):
    raise SystemExit(f"Record already exists: {RECORD_ID}")

template = next(record for record in records if record.get("id") == "ro-politehnica-bucharest-holistic-space-systems-msc")
record = copy.deepcopy(template)
record["id"] = RECORD_ID
record["program_profile"].update({
    "name": "Avionics and Aerospace Navigation",
    "native_name": "Avionică și navigație aerospațială",
    "department": "Nicolae Tipei Department of Aeronautical Systems Engineering and Aeronautical Management",
    "relevance_status": "strong",
})
record["eligibility_profile"]["required_previous_degree"] = {
    "en": "A completed bachelor's degree or equivalent is required. No exhaustive accepted-discipline list specific to Avionics and Aerospace Navigation was published in the checked current sources.",
    "tr": "Tamamlanmış lisans derecesi veya eşdeğeri gerekir. Kontrol edilen güncel kaynaklarda Avionics and Aerospace Navigation'a özgü kapsamlı kabul edilen bölüm listesi yayımlanmamıştır.",
}
record["eligibility_profile"]["notes_for_turkish_students"] = {
    "en": "Türkiye applicants use the non-EU route and must plan for Romanian-language preparation. The curriculum is especially relevant to control, guidance, simulation and aerospace navigation; no Turkish GPA conversion or GRE rule was inferred.",
    "tr": "Türkiye'den adaylar AB dışı rotayı kullanır ve Rumence hazırlığını planlamalıdır. Müfredat özellikle kontrol, güdüm, benzetim ve havacılık-uzay seyrüseferiyle ilgilidir; Türk not dönüşümü veya GRE kuralı çıkarılmadı.",
}
record["curriculum_profile"] = {
    "academic_cycle": "2025-2027",
    "tracks": [],
    "specializations": [],
    "course_count": {
        "minimum": 18,
        "maximum": 18,
        "counting_rule": "Eighteen mandatory curriculum line items: fourteen technical/ethics modules and four scientific-research/practice/dissertation blocks. Facultative teacher-training modules and their separate graduation exam are excluded.",
    },
    "credit_breakdown": [
        {"component": "Technical avionics, navigation, control, space and ethics modules", "credits": 60},
        {"component": "Scientific Research Modules I-III", "credits": 30},
        {"component": "Scientific research, research practice and dissertation preparation", "credits": 30},
    ],
    "mandatory_courses": [
        "Launch Vehicles and Launch Systems",
        "Optimal Control and Filtering",
        "Modelling and Optimization Techniques in Air Traffic Control",
        "Optimization Methods in Aerospace Engineering",
        "Scientific Research Module I",
        "Nonlinear Analysis and Synthesis of Automatic Flight Control Systems",
        "Aerospace Vehicle Simulators",
        "Artificial Intelligence in Aviation",
        "Space Vehicle Dynamics",
        "Complex Air Navigation Systems",
        "Scientific Research Module II",
        "Optimal Synthesis of Guidance Laws",
        "Flight Vehicle Guidance",
        "Space Energy Systems",
        "Automatic Control of Space Vehicles",
        "Advanced Practices in University Ethics and Deontology",
        "Scientific Research Module III",
        "Scientific Research, Research Practice and Dissertation Preparation",
    ],
    "elective_courses": [],
    "lab_courses": [
        "Launch Vehicles and Launch Systems",
        "Optimal Control and Filtering",
        "Optimization Methods in Aerospace Engineering",
        "Nonlinear Analysis and Synthesis of Automatic Flight Control Systems",
        "Aerospace Vehicle Simulators",
        "Artificial Intelligence in Aviation",
        "Space Vehicle Dynamics",
        "Complex Air Navigation Systems",
        "Optimal Synthesis of Guidance Laws",
        "Flight Vehicle Guidance",
        "Space Energy Systems",
        "Automatic Control of Space Vehicles",
    ],
    "project_based_courses": [
        "Scientific Research Module I",
        "Scientific Research Module II",
        "Scientific Research Module III",
        "Scientific Research, Research Practice and Dissertation Preparation",
    ],
    "thesis": {
        "required": True,
        "credits": 30,
        "options": ["Final 30-ECTS combined scientific research, research practice and dissertation-preparation block; the plan separately labels the dissertation examination as 10 ECTS without adding it to the 120-ECTS programme total."],
    },
    "internship": {
        "required": True,
        "credits": 30,
        "duration": None,
        "allocation": "research_practice_embedded_external_host_not_stated",
        "notes": {
            "en": "The final block includes research practice, but the curriculum does not establish a guaranteed external-company placement.",
            "tr": "Son blok araştırma pratiğini içerir; ancak müfredat garantili dış şirket yerleştirmesi kurmaz.",
        },
    },
    "mobility_options": [],
    "double_degree_options": [],
    "curriculum_urls": [CURRICULUM_URL],
}
record["category_profile"] = {
    "primary_categories": ["avionics_navigation", "gnc_control_autonomy", "aerospace_engineering"],
    "secondary_categories": ["flight_control", "spacecraft_control", "guidance", "air_navigation", "simulation", "artificial_intelligence", "launch_systems"],
    "subcategories": ["optimal_control", "control_filtering", "automatic_flight_control", "space_vehicle_dynamics", "guidance_laws", "air_traffic_control_optimization"],
    "normalized_tags": ["avionics", "aerospace_navigation", "gnc", "optimal_control", "flight_control", "spacecraft_control", "simulation", "artificial_intelligence", "launch_systems"],
    "category_scores": {
        "space_systems": 72,
        "satellite_systems": 48,
        "gnc": 96,
        "propulsion": 10,
        "aerodynamics_cfd": 12,
        "structures_materials": 5,
        "space_science": 0,
    },
    "category_evidence": ["Current 120-ECTS curriculum directly covers optimal control and filtering, automatic flight control, guidance-law synthesis, aerospace navigation, space-vehicle dynamics and automatic control, plus launch systems and AI in aviation."],
}
record["research_profile"] = {
    "research_areas": [
        "Optimal control and filtering",
        "Automatic flight control",
        "Guidance laws",
        "Aerospace vehicle simulation",
        "Air navigation",
        "Space vehicle dynamics and control",
        "Artificial intelligence in aviation",
        "Launch systems",
    ],
    "labs": [],
    "research_centers": ["Aeronautics and Space Research Centre (CCAS)"],
    "facilities": [],
    "projects": [],
    "student_teams": [],
    "research_opportunity_for_masters": "high_embedded_research",
    "research_strength_score": 80,
    "summary": {
        "en": "Research is structurally strong through 60 ECTS of research/practice/dissertation work and a control-heavy technical curriculum. The faculty's CCAS publishes relevant satellite attitude-control expertise, but named equipment and guaranteed project placement were not verified.",
        "tr": "Araştırma, 60 AKTS araştırma/pratik/tez çalışması ve kontrol ağırlıklı teknik müfredatla yapısal olarak güçlüdür. Fakültenin CCAS merkezi ilgili uydu tutum-kontrol uzmanlığı yayımlar; ancak isimli ekipman ve garantili proje yerleştirmesi doğrulanmadı.",
    },
}
record["industry_ecosystem_profile"].update({
    "career_relevance": "very_high_for_avionics_gnc_and_aerospace_control",
    "summary": {
        "en": "The curriculum is directly relevant to avionics, navigation, flight control, simulation and spacecraft GNC. No current programme-specific employer partnership, guaranteed placement, security-clearance pathway or placement rate was verified.",
        "tr": "Müfredat aviyonik, seyrüsefer, uçuş kontrolü, benzetim ve uzay aracı GNC alanlarıyla doğrudan ilgilidir. Güncel programa özgü işveren ortaklığı, garantili yerleştirme, güvenlik izni rotası veya yerleştirme oranı doğrulanmadı.",
    },
})
record["decision_summary"] = {
    "overall_recommendation": "excellent_gnc_avionics_fit_with_major_romanian_language_barrier",
    "main_strengths": {
        "en": "A current, unusually focused GNC/avionics curriculum spanning optimal control, flight-control synthesis, guidance laws, navigation, simulators, space-vehicle dynamics and 60 ECTS of research/practice/dissertation work at low published non-EU tuition.",
        "tr": "Optimal kontrol, uçuş-kontrol sentezi, güdüm yasaları, seyrüsefer, benzeticiler, uzay aracı dinamiği ve 60 AKTS araştırma/pratik/tez çalışmasını kapsayan, düşük yayımlanmış AB dışı ücretli güncel ve olağandışı derecede odaklı GNC/aviyonik müfredatı.",
    },
    "main_risks": {
        "en": "Romanian-only teaching, possible preparatory year, no verified GRE policy, unclear route-specific non-EU exam format, visa-sensitive processing and no verified employer-placement outcomes.",
        "tr": "Yalnız Rumence eğitim, olası hazırlık yılı, doğrulanmış GRE politikasının olmaması, rota bazında belirsiz AB dışı sınav formatı, vizeye duyarlı işlemler ve doğrulanmış işveren yerleştirme sonuçlarının bulunmaması.",
    },
    "best_for": {
        "en": "Romanian-ready applicants targeting avionics, flight control, aerospace navigation, GNC, simulators, AI in aviation or spacecraft dynamics and control.",
        "tr": "Aviyonik, uçuş kontrolü, havacılık-uzay seyrüseferi, GNC, benzeticiler, havacılıkta yapay zekâ veya uzay aracı dinamiği ve kontrolünü hedefleyen, Rumenceye hazır adaylar.",
    },
    "not_ideal_for": {
        "en": "English-only applicants, candidates focused on propulsion/structures/space science, or students requiring a documented international placement pipeline.",
        "tr": "Yalnız İngilizce eğitim isteyenler, itki/yapılar/uzay bilimine odaklananlar veya belgeli uluslararası yerleştirme hattı gereken öğrenciler.",
    },
    "application_reality": {
        "en": "For Türkiye applicants, Romanian readiness is the first hard gate. Confirm B1 certificate acceptance or the preparatory-year route in writing, then apply early in the February-July non-EU window and allow at least 60 days for processing.",
        "tr": "Türkiye'den adaylar için ilk kesin kapı Rumence hazırlığıdır. B1 belgesinin kabulünü veya hazırlık yılı rotasını yazılı teyit edin; ardından şubat-temmuz AB dışı penceresinde erken başvurup işlemler için en az 60 gün bırakın.",
    },
    "funding_reality": record["decision_summary"]["funding_reality"],
    "housing_reality": record["decision_summary"]["housing_reality"],
}
record["scoring_inputs"].update({
    "academic_field_fit_score_seed": 92,
    "eligibility_language_score_seed": 32,
    "career_research_score_seed": 79,
    "data_confidence_score_seed": 89,
})

source_log = record["source_profile"]["source_log"]
for source in source_log:
    if source["source_id"] == "ro_upb_shs_master_page":
        source.update({
            "source_id": "ro_upb_ana_master_page",
            "title": "Master Programs — Avionics and Aerospace Navigation",
            "notes": {"en": "Current programme, Romanian language, department, 2 years, 120 ECTS and curriculum link.", "tr": "Güncel program, Rumence eğitim dili, bölüm, 2 yıl, 120 AKTS ve müfredat bağlantısı."},
        })
    elif source["source_id"] == "ro_upb_shs_curriculum":
        source.update({
            "source_id": "ro_upb_ana_curriculum",
            "url": CURRICULUM_URL,
            "final_url": CURRICULUM_URL,
            "title": "Avionics and Aerospace Navigation Curriculum 2025-2027",
            "notes": {"en": "All four pages were extracted, rendered and visually checked; 18 mandatory line items total 120 ECTS, excluding facultative teacher training.", "tr": "Dört sayfanın tümü çıkarıldı, render edildi ve görsel olarak kontrol edildi; fakültatif öğretmenlik eğitimi hariç 18 zorunlu satır 120 AKTS toplam verir."},
        })

def replace_source_id(value):
    if isinstance(value, list):
        return [replace_source_id(item) for item in value]
    if value == "ro_upb_shs_master_page":
        return "ro_upb_ana_master_page"
    if value == "ro_upb_shs_curriculum":
        return "ro_upb_ana_curriculum"
    return value


record["source_profile"]["evidence_map"] = {
    key: replace_source_id(value) for key, value in record["source_profile"]["evidence_map"].items()
}
record["source_profile"]["verification_notes"] = {
    "en": "Critical decision fields are sourced. Open items: exact accepted Romanian certificate, preparatory-year 2026/27 fee and intake, non-EU exam format, GRE policy, next cycle dates/fees, scholarship current benefits, named avionics/control lab equipment, industry partnerships, outcomes, rankings and sentiment.",
    "tr": "Kritik karar alanları kaynaklıdır. Açık kalanlar: kabul edilen kesin Rumence belgesi, 2026/27 hazırlık yılı ücreti ve dönemi, AB dışı sınav formatı, GRE politikası, sonraki dönem tarih/ücretleri, güncel burs kapsamı, isimli aviyonik/kontrol laboratuvar ekipmanı, sanayi ortaklıkları, sonuçlar, sıralamalar ve görüşler.",
}
record["quality_control"]["qc_notes"] = {
    "en": "Curriculum fit for avionics and GNC is unusually strong and fully current; language, exact applicant-route and career-outcome uncertainties remain explicit.",
    "tr": "Aviyonik ve GNC müfredat uygunluğu olağandışı derecede güçlü ve tamamen günceldir; dil, kesin başvuru rotası ve kariyer sonucu belirsizlikleri açık tutulur.",
}
record["quality_control"]["remaining_verification_tasks"][2] = {
    "en": "Verify named avionics/control lab equipment, current projects available to master's students, industry partnerships, security restrictions and quantified outcomes.",
    "tr": "İsimli aviyonik/kontrol laboratuvar ekipmanını, yüksek lisans öğrencilerine açık güncel projeleri, sanayi ortaklıklarını, güvenlik kısıtlarını ve nicel sonuçları doğrulayın.",
}

records.append(record)
save(DB_PATH, records)

queue = load(QUEUE_PATH)
candidate = next(item for item in queue["candidates"] if item.get("candidate_id") == RECORD_ID)
candidate["discovery_status"] = "promoted_to_full_record"
candidate["known_cautions"] = [{
    "en": "The current curriculum proves exceptional GNC/avionics and meaningful spacecraft-control depth, but the programme is Romanian-taught and no English-completable route was found.",
    "tr": "Güncel müfredat olağanüstü GNC/aviyonik ve anlamlı uzay aracı kontrol derinliğini kanıtlar; ancak program Rumencedir ve İngilizce tamamlanabilir rota bulunmadı.",
}]
save(QUEUE_PATH, queue)

discovery = load(DISCOVERY_PATH)
candidate = next(item for item in discovery["included_candidates"] if item.get("candidate_id") == RECORD_ID)
candidate["status"] = "promoted_to_full_record"
discovery["discovery_result"]["full_v2_records"] = 3
discovery["discovery_result"]["queued_for_full_research"] = 7
save(DISCOVERY_PATH, discovery)

scan_log = load(SCAN_PATH)
scan = next(item for item in scan_log["scans"] if item.get("country") == "Romania")
scan["full_records_added"] = 3
scan["notes"] = {
    "en": "The 2026/27 national accreditation list yielded nine direct aerospace master's candidates and one technical adjacent aviation-ICT candidate. Air Transport Engineering, Holistic Space Systems, and Avionics and Aerospace Navigation were promoted to native V2; seven candidates remain queued. Current curriculum arithmetic resolves all three at 120 ECTS. Curriculum-led adjacent-programme discovery remains open.",
    "tr": "2026/27 ulusal akreditasyon listesi dokuz doğrudan havacılık-uzay yüksek lisansı ve bir teknik komşu havacılık-BT adayı verdi. Air Transport Engineering, Holistic Space Systems ve Avionics and Aerospace Navigation doğal V2'ye dönüştürüldü; yedi aday kuyrukta kaldı. Güncel müfredat aritmetiği üçünü de 120 AKTS olarak doğrular. Müfredat odaklı komşu program keşfi açıktır.",
}
save(SCAN_PATH, scan_log)

print(f"Added {RECORD_ID} and promoted the Romania queue/discovery state to 3/10 full records.")
