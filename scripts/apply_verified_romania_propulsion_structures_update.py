"""Promote two current Romanian-taught POLITEHNICA aerospace masters to native V2."""

from __future__ import annotations

import copy
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data_base" / "romania.json"
QUEUE_PATH = ROOT / "research_queue" / "program_candidates_v2.json"
DISCOVERY_PATH = ROOT / "reports" / "romania_programme_discovery_2026-08-14.json"
SCAN_PATH = ROOT / "research_queue" / "country_scan_log_v2.json"
TEMPLATE_ID = "ro-politehnica-bucharest-holistic-space-systems-msc"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path: Path, payload) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


PROGRAMMES = [
    {
        "id": "ro-politehnica-bucharest-aerospace-propulsion-environment-msc",
        "name": "Aerospace Propulsion and Environmental Protection",
        "native_name": "Propulsie aerospațială și protecția mediului",
        "url": "https://www.aero.pub.ro/wp-content/uploads/2025/10/2025_27_PLi_M_09_FIA_IA_PAPM.pdf",
        "source_prefix": "ro_upb_papm",
        "course_count": 17,
        "technical_count": 13,
        "mandatory_courses": [
            "Optimization Methods in Aerospace Engineering",
            "Transient Processes in Propulsion Systems",
            "Computational Aerodynamics",
            "Propellers and Wind Turbines",
            "Scientific Research Module I",
            "Computational Strength and Vibration Analysis of Aerojet Engines",
            "Acoustics and Noise Pollution",
            "Combustion and Chemical Pollution",
            "Nonlinear Finite Elements in Aeronautics",
            "Scientific Research Module II",
            "Nonconventional Transmissions",
            "Advanced Thermodynamics",
            "Space Propulsion Systems",
            "Advanced Structural Integrity Control Techniques",
            "Advanced Practices in University Ethics and Deontology",
            "Scientific Research Module III",
            "Scientific Research, Research Practice and Dissertation Preparation",
        ],
        "lab_courses": [
            "Optimization Methods in Aerospace Engineering",
            "Transient Processes in Propulsion Systems",
            "Computational Aerodynamics",
            "Computational Strength and Vibration Analysis of Aerojet Engines",
            "Acoustics and Noise Pollution",
            "Combustion and Chemical Pollution",
            "Nonlinear Finite Elements in Aeronautics",
            "Nonconventional Transmissions",
            "Advanced Thermodynamics",
            "Advanced Structural Integrity Control Techniques",
        ],
        "primary_categories": ["aerospace_propulsion", "aerospace_engineering"],
        "secondary_categories": ["combustion", "environmental_impact", "aero_engines", "space_propulsion", "aerodynamics_cfd", "acoustics_noise", "structural_integrity"],
        "subcategories": ["transient_propulsion", "aerojet_engine_vibration", "chemical_pollution", "space_propulsion_systems", "advanced_thermodynamics", "nonlinear_finite_elements"],
        "tags": ["propulsion", "combustion", "aero_engines", "space_propulsion", "cfd", "noise", "emissions", "structural_integrity"],
        "scores": {"space_systems": 52, "satellite_systems": 10, "gnc": 5, "propulsion": 94, "aerodynamics_cfd": 72, "structures_materials": 48, "space_science": 0},
        "category_evidence": "Current 120-ECTS curriculum is propulsion-led: transient propulsion, aerojet-engine strength and vibration, combustion, thermodynamics and space propulsion, with CFD plus noise and chemical-pollution control.",
        "research_areas": ["Aerospace propulsion", "Transient propulsion processes", "Combustion and chemical pollution", "Aerojet-engine strength and vibration", "Space propulsion", "Computational aerodynamics", "Acoustics and noise pollution", "Structural integrity"],
        "research_score": 81,
        "research_summary": {
            "en": "Research is structurally strong through 60 ECTS of research/practice/dissertation work and a propulsion-focused curriculum. The faculty CCAS publishes relevant expertise in hybrid launcher engines, rockets and space propulsion, but named equipment and guaranteed project placement were not verified.",
            "tr": "Araştırma, 60 AKTS araştırma/pratik/tez çalışması ve itki odaklı müfredatla yapısal olarak güçlüdür. Fakültenin CCAS merkezi hibrit fırlatıcı motorları, roketler ve uzay itkisi alanlarında ilgili uzmanlık yayımlar; ancak isimli ekipman ve garantili proje yerleştirmesi doğrulanmadı.",
        },
        "career_relevance": "very_high_for_propulsion_combustion_and_environmental_engineering",
        "industry_summary": {
            "en": "The curriculum is directly relevant to aircraft propulsion, combustion, aero-engine analysis, acoustics, emissions and some space propulsion. No current programme-specific employer partnership, guaranteed placement or placement rate was verified.",
            "tr": "Müfredat uçak itkisi, yanma, uçak motoru analizi, akustik, emisyonlar ve kısmen uzay itkisiyle doğrudan ilgilidir. Güncel programa özgü işveren ortaklığı, garantili yerleştirme veya yerleştirme oranı doğrulanmadı.",
        },
        "recommendation": "excellent_propulsion_fit_with_romanian_language_barrier_and_limited_breadth",
        "strengths": {
            "en": "A focused 120-ECTS propulsion curriculum combining aero-engine transients, combustion, thermodynamics, CFD, engine vibration, noise and pollution with one direct space-propulsion module and 60 ECTS of research/practice/dissertation work.",
            "tr": "Uçak motoru geçici rejimleri, yanma, termodinamik, HAD, motor titreşimi, gürültü ve kirliliği bir doğrudan uzay itkisi dersi ve 60 AKTS araştırma/pratik/tez çalışmasıyla birleştiren odaklı 120 AKTS itki müfredatı.",
        },
        "risks": {
            "en": "Romanian-only teaching, possible preparatory year, aircraft-engine-heavy coverage rather than a complete spacecraft curriculum, unknown GRE policy, visa-sensitive processing and no verified placement outcomes.",
            "tr": "Yalnız Rumence eğitim, olası hazırlık yılı, tam uzay aracı müfredatı yerine uçak motoru ağırlığı, bilinmeyen GRE politikası, vizeye duyarlı işlemler ve doğrulanmış yerleştirme sonuçlarının olmaması.",
        },
        "best_for": {
            "en": "Romanian-ready applicants targeting aircraft engines, combustion, thermodynamics, CFD, aero-engine structural/vibration analysis, acoustics, emissions or an introduction to space propulsion.",
            "tr": "Uçak motorları, yanma, termodinamik, HAD, uçak motoru yapı/titreşim analizi, akustik, emisyonlar veya uzay itkisine giriş hedefleyen, Rumenceye hazır adaylar.",
        },
        "not_ideal": {
            "en": "English-only applicants or students seeking broad spacecraft systems, satellites, GNC, orbital mechanics or a verified industry-placement pipeline.",
            "tr": "Yalnız İngilizce eğitim isteyenler veya geniş uzay aracı sistemleri, uydular, GNC, yörünge mekaniği ya da doğrulanmış sanayi yerleştirme hattı arayan öğrenciler.",
        },
        "academic_seed": 90,
        "career_seed": 78,
        "qc_note": {
            "en": "Propulsion, combustion and environmental-control curriculum evidence is current and strong; language, exact applicant route and career outcomes remain explicit uncertainties.",
            "tr": "İtki, yanma ve çevresel kontrol müfredatı kanıtı güncel ve güçlüdür; dil, kesin başvuru rotası ve kariyer sonuçları açık belirsizlikler olarak kalır.",
        },
        "queue_caution": {
            "en": "The current curriculum proves strong aircraft-propulsion and environmental depth plus one direct space-propulsion module; it does not justify treating the degree as a broad spacecraft-systems programme, and teaching is Romanian.",
            "tr": "Güncel müfredat güçlü uçak itkisi ve çevresel derinlik ile bir doğrudan uzay itkisi dersini kanıtlar; dereceyi geniş uzay aracı sistemleri programı saymayı haklı çıkarmaz ve eğitim dili Rumencedir.",
        },
    },
    {
        "id": "ro-politehnica-bucharest-aeronautical-space-structures-msc",
        "name": "Aeronautical and Space Structures",
        "native_name": "Structuri aeronautice și spațiale",
        "url": "https://www.aero.pub.ro/wp-content/uploads/2025/10/2025_27_PLi_M_09_FIA_IA_SAS.pdf",
        "source_prefix": "ro_upb_sas",
        "course_count": 17,
        "technical_count": 13,
        "mandatory_courses": [
            "Optimization Methods in Aerospace Engineering",
            "Conventional Aerospace Propulsion Systems - Rocket Engines",
            "Propellers and Wind Turbines",
            "Computational Aerodynamics",
            "Scientific Research Module I",
            "Computer-Aided Structural Design",
            "Nonlinear Finite Elements in Aeronautics",
            "Materials for Space Structures",
            "Space Propulsion and Correction Systems",
            "Scientific Research Module II",
            "Structures for Aerospace Vehicles",
            "Vibrations of Mechanical Systems",
            "Advanced Structural Integrity Control Techniques",
            "Launch Vehicles and Launch Systems",
            "Advanced Practices in University Ethics and Deontology",
            "Scientific Research Module III",
            "Scientific Research, Research Practice and Dissertation Preparation",
        ],
        "lab_courses": [
            "Optimization Methods in Aerospace Engineering",
            "Conventional Aerospace Propulsion Systems - Rocket Engines",
            "Computational Aerodynamics",
            "Computer-Aided Structural Design",
            "Nonlinear Finite Elements in Aeronautics",
            "Materials for Space Structures",
            "Space Propulsion and Correction Systems",
            "Advanced Structural Integrity Control Techniques",
            "Launch Vehicles and Launch Systems",
        ],
        "primary_categories": ["aerospace_structures", "space_structures", "aerospace_engineering"],
        "secondary_categories": ["finite_elements", "structural_integrity", "space_materials", "vibration", "launch_systems", "rocket_engines", "aerodynamics_cfd"],
        "subcategories": ["computer_aided_structural_design", "nonlinear_finite_elements", "materials_for_space_structures", "aerospace_vehicle_structures", "mechanical_vibration", "structural_health_integrity"],
        "tags": ["aerospace_structures", "space_structures", "finite_elements", "space_materials", "vibration", "structural_integrity", "launch_systems", "rocket_engines"],
        "scores": {"space_systems": 74, "satellite_systems": 38, "gnc": 5, "propulsion": 52, "aerodynamics_cfd": 62, "structures_materials": 96, "space_science": 0},
        "category_evidence": "Current 120-ECTS curriculum directly covers computer-aided structural design, nonlinear finite elements, materials for space structures, aerospace-vehicle structures, vibration and structural-integrity control, with rocket engines and launch systems.",
        "research_areas": ["Aeronautical and space structures", "Nonlinear finite elements", "Materials for space structures", "Aerospace vehicle structural design", "Mechanical vibration", "Structural integrity", "Launch vehicles", "Rocket propulsion"],
        "research_score": 83,
        "research_summary": {
            "en": "Research is structurally strong through 60 ECTS of research/practice/dissertation work and a space-structures curriculum. The faculty CCAS publishes relevant expertise in satellite structures, launchers, propulsion and aerospace structures, but named test equipment and guaranteed project placement were not verified.",
            "tr": "Araştırma, 60 AKTS araştırma/pratik/tez çalışması ve uzay yapıları müfredatıyla yapısal olarak güçlüdür. Fakültenin CCAS merkezi uydu yapıları, fırlatıcılar, itki ve havacılık-uzay yapılarında ilgili uzmanlık yayımlar; ancak isimli test ekipmanı ve garantili proje yerleştirmesi doğrulanmadı.",
        },
        "career_relevance": "very_high_for_aerospace_and_space_structures",
        "industry_summary": {
            "en": "The curriculum is directly relevant to aerospace structural design, finite-element analysis, space materials, vibration, integrity and launch vehicles. No current programme-specific employer partnership, guaranteed placement or placement rate was verified.",
            "tr": "Müfredat havacılık-uzay yapı tasarımı, sonlu eleman analizi, uzay malzemeleri, titreşim, bütünlük ve fırlatma araçlarıyla doğrudan ilgilidir. Güncel programa özgü işveren ortaklığı, garantili yerleştirme veya yerleştirme oranı doğrulanmadı.",
        },
        "recommendation": "excellent_aerospace_space_structures_fit_with_major_romanian_language_barrier",
        "strengths": {
            "en": "A direct 120-ECTS structures programme covering nonlinear finite elements, space-structure materials, aerospace-vehicle structures, vibration, integrity control, rocket engines and launch systems, with 60 ECTS of research/practice/dissertation work.",
            "tr": "Doğrusal olmayan sonlu elemanlar, uzay yapısı malzemeleri, havacılık-uzay aracı yapıları, titreşim, bütünlük kontrolü, roket motorları ve fırlatma sistemlerini 60 AKTS araştırma/pratik/tez çalışmasıyla kapsayan doğrudan 120 AKTS yapı programı.",
        },
        "risks": {
            "en": "Romanian-only teaching, possible preparatory year, no verified composite/test-facility inventory, unknown GRE policy, visa-sensitive processing and no verified employer-placement outcomes.",
            "tr": "Yalnız Rumence eğitim, olası hazırlık yılı, doğrulanmış kompozit/test tesisi envanterinin olmaması, bilinmeyen GRE politikası, vizeye duyarlı işlemler ve doğrulanmış işveren yerleştirme sonuçlarının bulunmaması.",
        },
        "best_for": {
            "en": "Romanian-ready applicants targeting aeronautical or space structures, finite elements, space materials, vibration, structural integrity, launch vehicles or structurally oriented research.",
            "tr": "Havacılık veya uzay yapıları, sonlu elemanlar, uzay malzemeleri, titreşim, yapısal bütünlük, fırlatma araçları veya yapı odaklı araştırmayı hedefleyen, Rumenceye hazır adaylar.",
        },
        "not_ideal": {
            "en": "English-only applicants or students primarily seeking GNC, satellite electronics, space science, orbital mechanics or a verified industry-placement pipeline.",
            "tr": "Yalnız İngilizce eğitim isteyenler veya öncelikle GNC, uydu elektroniği, uzay bilimi, yörünge mekaniği ya da doğrulanmış sanayi yerleştirme hattı arayan öğrenciler.",
        },
        "academic_seed": 93,
        "career_seed": 80,
        "qc_note": {
            "en": "Aeronautical and space-structures curriculum evidence is current and strong; language, named facilities, exact applicant route and career outcomes remain explicit uncertainties.",
            "tr": "Havacılık ve uzay yapıları müfredatı kanıtı güncel ve güçlüdür; dil, isimli tesisler, kesin başvuru rotası ve kariyer sonuçları açık belirsizlikler olarak kalır.",
        },
        "queue_caution": {
            "en": "The current curriculum proves direct aeronautical and space-structures depth, including space materials and launch systems, but teaching is Romanian and named composite/test facilities remain unverified.",
            "tr": "Güncel müfredat uzay malzemeleri ve fırlatma sistemleri dâhil doğrudan havacılık ve uzay yapıları derinliğini kanıtlar; ancak eğitim dili Rumencedir ve isimli kompozit/test tesisleri doğrulanmayı bekler.",
        },
    },
]


def replace_source_ids(value, source_prefix: str):
    if isinstance(value, list):
        return [replace_source_ids(item, source_prefix) for item in value]
    if value == "ro_upb_shs_master_page":
        return f"{source_prefix}_master_page"
    if value == "ro_upb_shs_curriculum":
        return f"{source_prefix}_curriculum"
    return value


def build_record(template: dict, spec: dict) -> dict:
    record = copy.deepcopy(template)
    record["id"] = spec["id"]
    record["program_profile"].update({
        "name": spec["name"],
        "native_name": spec["native_name"],
        "department": "Elie Carafoli Department of Aerospace Sciences",
        "relevance_status": "strong",
    })
    record["eligibility_profile"]["required_previous_degree"] = {
        "en": f"A completed bachelor's degree or equivalent is required. No exhaustive accepted-discipline list specific to {spec['name']} was published in the checked current sources.",
        "tr": f"Tamamlanmış lisans derecesi veya eşdeğeri gerekir. Kontrol edilen güncel kaynaklarda {spec['name']} programına özgü kapsamlı kabul edilen bölüm listesi yayımlanmamıştır.",
    }
    record["eligibility_profile"]["notes_for_turkish_students"] = {
        "en": "Türkiye applicants use the non-EU route and must plan for Romanian-language preparation. Begin document legalization and certified translations before the application window; no Turkish GPA conversion or GRE rule was inferred.",
        "tr": "Türkiye'den adaylar AB dışı rotayı kullanır ve Rumence hazırlığını planlamalıdır. Belge tasdiki ve yeminli tercümeleri başvuru penceresinden önce başlatın; Türk not dönüşümü veya GRE kuralı çıkarılmadı.",
    }
    record["curriculum_profile"] = {
        "academic_cycle": "2025-2027",
        "tracks": [],
        "specializations": [],
        "course_count": {
            "minimum": spec["course_count"],
            "maximum": spec["course_count"],
            "counting_rule": f"Seventeen mandatory curriculum line items: {spec['technical_count']} technical/ethics modules and four scientific-research/practice/dissertation blocks. Facultative teacher-training modules and their separate graduation exam are excluded.",
        },
        "credit_breakdown": [
            {"component": "Technical aerospace and ethics modules", "credits": 60},
            {"component": "Scientific Research Modules I-III", "credits": 30},
            {"component": "Scientific research, research practice and dissertation preparation", "credits": 30},
        ],
        "mandatory_courses": spec["mandatory_courses"],
        "elective_courses": [],
        "lab_courses": spec["lab_courses"],
        "project_based_courses": ["Scientific Research Module I", "Scientific Research Module II", "Scientific Research Module III", "Scientific Research, Research Practice and Dissertation Preparation"],
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
        "curriculum_urls": [spec["url"]],
    }
    record["category_profile"] = {
        "primary_categories": spec["primary_categories"],
        "secondary_categories": spec["secondary_categories"],
        "subcategories": spec["subcategories"],
        "normalized_tags": spec["tags"],
        "category_scores": spec["scores"],
        "category_evidence": [spec["category_evidence"]],
    }
    record["research_profile"] = {
        "research_areas": spec["research_areas"],
        "labs": [],
        "research_centers": ["Aeronautics and Space Research Centre (CCAS)"],
        "facilities": [],
        "projects": [],
        "student_teams": [],
        "research_opportunity_for_masters": "high_embedded_research",
        "research_strength_score": spec["research_score"],
        "summary": spec["research_summary"],
    }
    record["industry_ecosystem_profile"].update({
        "career_relevance": spec["career_relevance"],
        "summary": spec["industry_summary"],
    })
    funding = record["decision_summary"]["funding_reality"]
    housing = record["decision_summary"]["housing_reality"]
    record["decision_summary"] = {
        "overall_recommendation": spec["recommendation"],
        "main_strengths": spec["strengths"],
        "main_risks": spec["risks"],
        "best_for": spec["best_for"],
        "not_ideal_for": spec["not_ideal"],
        "application_reality": {
            "en": "For Türkiye applicants, Romanian readiness is the first hard gate. Confirm B1 certificate acceptance or the preparatory-year route in writing, then apply early in the February-July non-EU window and allow at least 60 days for processing.",
            "tr": "Türkiye'den adaylar için ilk kesin kapı Rumence hazırlığıdır. B1 belgesinin kabulünü veya hazırlık yılı rotasını yazılı teyit edin; ardından şubat-temmuz AB dışı penceresinde erken başvurup işlemler için en az 60 gün bırakın.",
        },
        "funding_reality": funding,
        "housing_reality": housing,
    }
    record["scoring_inputs"].update({
        "academic_field_fit_score_seed": spec["academic_seed"],
        "eligibility_language_score_seed": 32,
        "career_research_score_seed": spec["career_seed"],
        "data_confidence_score_seed": 89,
    })
    for source in record["source_profile"]["source_log"]:
        if source["source_id"] == "ro_upb_shs_master_page":
            source.update({
                "source_id": f"{spec['source_prefix']}_master_page",
                "title": f"Master Programs - {spec['name']}",
                "notes": {"en": "Current programme, Romanian language, department, 2 years, 120 ECTS and curriculum link.", "tr": "Güncel program, Rumence eğitim dili, bölüm, 2 yıl, 120 AKTS ve müfredat bağlantısı."},
            })
        elif source["source_id"] == "ro_upb_shs_curriculum":
            source.update({
                "source_id": f"{spec['source_prefix']}_curriculum",
                "url": spec["url"],
                "final_url": spec["url"],
                "title": f"{spec['name']} Curriculum 2025-2027",
                "notes": {"en": "All four pages were extracted, rendered and visually checked; 17 mandatory line items total 120 ECTS, excluding facultative teacher training.", "tr": "Dört sayfanın tümü çıkarıldı, render edildi ve görsel olarak kontrol edildi; fakültatif öğretmenlik eğitimi hariç 17 zorunlu satır 120 AKTS toplam verir."},
            })
    record["source_profile"]["evidence_map"] = {
        key: replace_source_ids(value, spec["source_prefix"])
        for key, value in record["source_profile"]["evidence_map"].items()
    }
    record["source_profile"]["verification_notes"] = {
        "en": "Critical decision fields are sourced. Open items: exact accepted Romanian certificate, preparatory-year 2026/27 fee and intake, non-EU exam format, GRE policy, next cycle dates/fees, scholarship current benefits, named lab/test equipment, industry partnerships, outcomes, rankings and sentiment.",
        "tr": "Kritik karar alanları kaynaklıdır. Açık kalanlar: kabul edilen kesin Rumence belgesi, 2026/27 hazırlık yılı ücreti ve dönemi, AB dışı sınav formatı, GRE politikası, sonraki dönem tarih/ücretleri, güncel burs kapsamı, isimli laboratuvar/test ekipmanı, sanayi ortaklıkları, sonuçlar, sıralamalar ve görüşler.",
    }
    record["quality_control"]["qc_notes"] = spec["qc_note"]
    record["quality_control"]["remaining_verification_tasks"][2] = {
        "en": "Verify named laboratory and test equipment, current projects available to master's students, industry partnerships and quantified outcomes.",
        "tr": "İsimli laboratuvar ve test ekipmanını, yüksek lisans öğrencilerine açık güncel projeleri, sanayi ortaklıklarını ve nicel sonuçları doğrulayın.",
    }
    return record


records = load(DB_PATH)
existing_ids = {record.get("id") for record in records}
for spec in PROGRAMMES:
    if spec["id"] in existing_ids:
        raise SystemExit(f"Record already exists: {spec['id']}")
template = next(record for record in records if record.get("id") == TEMPLATE_ID)
records.extend(build_record(template, spec) for spec in PROGRAMMES)
save(DB_PATH, records)

queue = load(QUEUE_PATH)
for spec in PROGRAMMES:
    candidate = next(item for item in queue["candidates"] if item.get("candidate_id") == spec["id"])
    candidate["discovery_status"] = "promoted_to_full_record"
    candidate["known_cautions"] = [spec["queue_caution"]]
save(QUEUE_PATH, queue)

discovery = load(DISCOVERY_PATH)
for spec in PROGRAMMES:
    candidate = next(item for item in discovery["included_candidates"] if item.get("candidate_id") == spec["id"])
    candidate["status"] = "promoted_to_full_record"
discovery["discovery_result"]["full_v2_records"] = 5
discovery["discovery_result"]["queued_for_full_research"] = 5
save(DISCOVERY_PATH, discovery)

scan_log = load(SCAN_PATH)
scan = next(item for item in scan_log["scans"] if item.get("country") == "Romania")
scan["full_records_added"] = 5
scan["notes"] = {
    "en": "The 2026/27 national accreditation list yielded nine direct aerospace master's candidates and one technical adjacent aviation-ICT candidate. Five POLITEHNICA programmes are now native V2: Air Transport Engineering, Holistic Space Systems, Avionics and Aerospace Navigation, Aerospace Propulsion and Environmental Protection, and Aeronautical and Space Structures. Five candidates remain queued; curriculum-led adjacent-programme discovery remains open.",
    "tr": "2026/27 ulusal akreditasyon listesi dokuz doğrudan havacılık-uzay yüksek lisansı ve bir teknik komşu havacılık-BT adayı verdi. Beş POLITEHNICA programı artık doğal V2'dir: Air Transport Engineering, Holistic Space Systems, Avionics and Aerospace Navigation, Aerospace Propulsion and Environmental Protection ve Aeronautical and Space Structures. Beş aday kuyrukta kaldı; müfredat odaklı komşu program keşfi açıktır.",
}
save(SCAN_PATH, scan_log)

print("Added PAPM and SAS native V2 records; Romania discovery is now 5/10 full records.")
