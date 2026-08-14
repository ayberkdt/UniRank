"""Promote two Romanian aviation-management masters as low-space-fit adjacent V2 records."""

from __future__ import annotations

import copy
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data_base" / "romania.json"
QUEUE_PATH = ROOT / "research_queue" / "program_candidates_v2.json"
DISCOVERY_PATH = ROOT / "reports" / "romania_programme_discovery_2026-08-14.json"
SCAN_PATH = ROOT / "research_queue" / "country_scan_log_v2.json"
TEMPLATE_ID = "ro-politehnica-bucharest-avionics-aerospace-navigation-msc"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path: Path, payload) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


COMMON_LATER_COURSES = [
    "Airline Management",
    "Airport Infrastructure",
    "Aeronautical Meteorology",
    "Security, Quality and Audit",
    "Air Transport Systems",
    "Scientific Research Module II",
    "Airspace Organization and CNS Service System (Communications, Navigation, Surveillance)",
    "Simulators and Information/Communication Techniques in Air Transport",
    "Aeronautical Safety Systems and Investigations",
    "Human Factors in Aviation and Risk Management",
    "Project Management",
    "Air Traffic Management",
    "Advanced Practices in University Ethics and Deontology",
    "Scientific Research Module III",
    "Scientific Research, Research Practice and Dissertation Preparation",
]


PROGRAMMES = [
    {
        "id": "ro-politehnica-bucharest-aerospace-engineering-management-msc",
        "name": "Engineering and Aerospace Management",
        "native_name": "Inginerie și management aerospațial",
        "url": "https://www.aero.pub.ro/wp-content/uploads/2025/10/2025_27_PLi_M_09_FIA_IA_IMA.pdf",
        "prefix": "ro_upb_ima",
        "first_courses": [
            "Airport Management 2",
            "Optimization Methods for Air Transport",
            "European and International Air Law",
            "Financial Management",
            "Artificial Intelligence in Aviation",
            "Scientific Research Module I",
        ],
        "extra_tag": "artificial_intelligence_in_aviation",
        "category_evidence": "The current curriculum is aviation-systems and management oriented: airport and airline management, air-transport optimization, CNS, simulators, safety, human factors and ATM. It contains no spacecraft, satellite, propulsion, structures or orbital-mechanics module.",
        "strengths": {
            "en": "A coherent aviation-systems management curriculum with air-transport optimization, AI in aviation, CNS, simulators, safety, human factors, ATM and 60 ECTS of research/practice/dissertation work.",
            "tr": "Hava taşımacılığı optimizasyonu, havacılıkta yapay zekâ, CNS, benzeticiler, emniyet, insan faktörleri, ATM ve 60 AKTS araştırma/pratik/tez çalışması içeren tutarlı havacılık sistemleri yönetimi müfredatı.",
        },
        "best_for": {
            "en": "Romanian-ready applicants targeting aviation operations, airport/airline management, air-traffic systems, safety, CNS or aviation digitalization rather than spacecraft engineering.",
            "tr": "Uzay aracı mühendisliği yerine havacılık operasyonları, havalimanı/havayolu yönetimi, hava trafik sistemleri, emniyet, CNS veya havacılık dijitalleşmesini hedefleyen, Rumenceye hazır adaylar.",
        },
        "recommendation": "useful_aviation_systems_management_adjacent_degree_not_space_engineering",
        "academic_seed": 42,
    },
    {
        "id": "ro-politehnica-bucharest-aeronautical-management-msc",
        "name": "Aeronautical Management",
        "native_name": "Management aeronautic",
        "url": "https://www.aero.pub.ro/wp-content/uploads/2025/10/2025_27_PLi_M_09_FIA_IA_MA.pdf",
        "prefix": "ro_upb_ma",
        "first_courses": [
            "Airport Management",
            "Optimization Methods for Air Transport",
            "European and International Air Law",
            "Financial Management",
            "Aviation and the Environment",
            "Scientific Research Module I",
        ],
        "extra_tag": "aviation_environment",
        "category_evidence": "The current curriculum is aeronautical management oriented: airport and airline management, aviation environment, CNS, simulators, safety, human factors and ATM. It contains no spacecraft, satellite, propulsion, structures or orbital-mechanics module.",
        "strengths": {
            "en": "A coherent aeronautical-management curriculum with airport and airline management, aviation environment, CNS, simulators, safety, human factors, ATM and 60 ECTS of research/practice/dissertation work.",
            "tr": "Havalimanı ve havayolu yönetimi, havacılık ve çevre, CNS, benzeticiler, emniyet, insan faktörleri, ATM ve 60 AKTS araştırma/pratik/tez çalışması içeren tutarlı havacılık yönetimi müfredatı.",
        },
        "best_for": {
            "en": "Romanian-ready applicants targeting airport/airline operations, aviation safety, human factors, ATM, CNS or regulated aviation management rather than technical spacecraft design.",
            "tr": "Teknik uzay aracı tasarımı yerine havalimanı/havayolu operasyonları, havacılık emniyeti, insan faktörleri, ATM, CNS veya düzenlemeye tabi havacılık yönetimini hedefleyen, Rumenceye hazır adaylar.",
        },
        "recommendation": "aviation_management_adjacent_degree_with_very_low_space_engineering_fit",
        "academic_seed": 36,
    },
]


def replace_ids(value, prefix: str):
    if isinstance(value, list):
        return [replace_ids(item, prefix) for item in value]
    if value == "ro_upb_ana_master_page":
        return f"{prefix}_master_page"
    if value == "ro_upb_ana_curriculum":
        return f"{prefix}_curriculum"
    return value


def build_record(template: dict, spec: dict) -> dict:
    record = copy.deepcopy(template)
    record["id"] = spec["id"]
    record["program_profile"].update({
        "name": spec["name"],
        "native_name": spec["native_name"],
        "department": "Nicolae Tipei Department of Aeronautical Systems Engineering and Aeronautical Management",
        "relevance_status": "weak",
    })
    record["eligibility_profile"]["required_previous_degree"] = {
        "en": f"A completed bachelor's degree or equivalent is required. No exhaustive accepted-discipline list specific to {spec['name']} was published in the checked current sources.",
        "tr": f"Tamamlanmış lisans derecesi veya eşdeğeri gerekir. Kontrol edilen güncel kaynaklarda {spec['name']} programına özgü kapsamlı kabul edilen bölüm listesi yayımlanmamıştır.",
    }
    record["curriculum_profile"] = {
        "academic_cycle": "2025-2027",
        "tracks": [],
        "specializations": [],
        "course_count": {
            "minimum": 21,
            "maximum": 21,
            "counting_rule": "Twenty-one mandatory curriculum line items: seventeen aviation/management/ethics modules and four scientific-research/practice/dissertation blocks. Facultative teacher-training modules and their separate graduation exam are excluded.",
        },
        "credit_breakdown": [
            {"component": "Aviation systems, management, law, safety, human factors and ethics modules", "credits": 60},
            {"component": "Scientific Research Modules I-III", "credits": 30},
            {"component": "Scientific research, research practice and dissertation preparation", "credits": 30},
        ],
        "mandatory_courses": spec["first_courses"] + COMMON_LATER_COURSES,
        "elective_courses": [],
        "lab_courses": [
            "Airspace Organization and CNS Service System (Communications, Navigation, Surveillance)",
            "Simulators and Information/Communication Techniques in Air Transport",
        ],
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
        "primary_categories": ["aviation_management", "air_transport_systems"],
        "secondary_categories": ["air_traffic_management", "cns", "aviation_safety", "human_factors", "airport_management", "airline_management", spec["extra_tag"]],
        "subcategories": ["air_transport_optimization", "airport_infrastructure", "aeronautical_meteorology", "aviation_risk_management", "aviation_law"],
        "normalized_tags": ["aviation_management", "air_transport", "atm", "cns", "aviation_safety", "human_factors", "simulators", spec["extra_tag"]],
        "category_scores": {"space_systems": 4, "satellite_systems": 0, "gnc": 16, "propulsion": 0, "aerodynamics_cfd": 0, "structures_materials": 0, "space_science": 0},
        "category_evidence": [spec["category_evidence"]],
    }
    record["research_profile"] = {
        "research_areas": ["Air transport optimization", "Airport and airline management", "Air traffic management", "CNS services", "Aviation safety and investigations", "Human factors and risk management", spec["extra_tag"].replace("_", " ")],
        "labs": [],
        "research_centers": [],
        "facilities": [],
        "projects": [],
        "student_teams": [],
        "research_opportunity_for_masters": "embedded_research_topic_and_supervisor_not_verified",
        "research_strength_score": 52,
        "summary": {
            "en": "The curriculum embeds 60 ECTS of research/practice/dissertation work, but no programme-specific laboratory, current funded project, named research centre or guaranteed external placement was verified.",
            "tr": "Müfredat 60 AKTS araştırma/pratik/tez çalışması içerir; ancak programa özgü laboratuvar, güncel fonlu proje, isimli araştırma merkezi veya garantili dış yerleştirme doğrulanmadı.",
        },
    }
    record["industry_ecosystem_profile"].update({
        "internship_access": "research_practice_required_external_host_not_guaranteed",
        "career_relevance": "high_for_aviation_operations_low_for_space_engineering",
        "summary": {
            "en": "The curriculum is relevant to aviation operations, ATM, CNS, safety and airport/airline management, but no current programme-specific employer partnership, guaranteed placement or placement rate was verified. It should not be treated as a spacecraft-industry pipeline.",
            "tr": "Müfredat havacılık operasyonları, ATM, CNS, emniyet ve havalimanı/havayolu yönetimiyle ilgilidir; ancak güncel programa özgü işveren ortaklığı, garantili yerleştirme veya yerleştirme oranı doğrulanmadı. Uzay aracı sanayisine geçiş hattı olarak değerlendirilmemelidir.",
        },
    })
    record["ranking_profile"]["programme_reputation_evidence"] = []
    funding = record["decision_summary"]["funding_reality"]
    housing = record["decision_summary"]["housing_reality"]
    record["decision_summary"] = {
        "overall_recommendation": spec["recommendation"],
        "main_strengths": spec["strengths"],
        "main_risks": {
            "en": "Romanian-only teaching, possible preparatory year, management/operations emphasis rather than spacecraft engineering, unknown GRE policy, visa-sensitive processing and no verified placement outcomes.",
            "tr": "Yalnız Rumence eğitim, olası hazırlık yılı, uzay aracı mühendisliği yerine yönetim/operasyon ağırlığı, bilinmeyen GRE politikası, vizeye duyarlı işlemler ve doğrulanmış yerleştirme sonuçlarının olmaması.",
        },
        "best_for": spec["best_for"],
        "not_ideal_for": {
            "en": "Students seeking spacecraft design, satellites, orbital mechanics, propulsion, structures, CFD, space science or an English-taught technical engineering degree.",
            "tr": "Uzay aracı tasarımı, uydular, yörünge mekaniği, itki, yapılar, HAD, uzay bilimi veya İngilizce teknik mühendislik derecesi arayan öğrenciler.",
        },
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
        "career_research_score_seed": 48,
        "data_confidence_score_seed": 88,
    })
    record["source_profile"]["source_log"] = [
        source for source in record["source_profile"]["source_log"]
        if source["source_id"] != "ro_upb_ccas"
    ]
    for source in record["source_profile"]["source_log"]:
        if source["source_id"] == "ro_upb_ana_master_page":
            source.update({
                "source_id": f"{spec['prefix']}_master_page",
                "title": f"Master Programs - {spec['name']}",
            })
        elif source["source_id"] == "ro_upb_ana_curriculum":
            source.update({
                "source_id": f"{spec['prefix']}_curriculum",
                "url": spec["url"],
                "final_url": spec["url"],
                "title": f"{spec['name']} Curriculum 2025-2027",
                "notes": {"en": "All four pages were extracted, rendered and visually checked; 21 mandatory line items total 120 ECTS, excluding facultative teacher training.", "tr": "Dört sayfanın tümü çıkarıldı, render edildi ve görsel olarak kontrol edildi; fakültatif öğretmenlik eğitimi hariç 21 zorunlu satır 120 AKTS toplam verir."},
            })
    record["source_profile"]["evidence_map"] = {
        key: [item for item in replace_ids(value, spec["prefix"]) if item != "ro_upb_ccas"]
        for key, value in record["source_profile"]["evidence_map"].items()
    }
    record["source_profile"]["verification_notes"] = {
        "en": "Critical decision fields are sourced. Open items: exact Romanian certificate/preparatory-year terms, non-EU exam format, GRE policy, next-cycle dates and fees, current scholarship benefits, programme-specific research projects, employer partnerships, outcomes, rankings and sentiment.",
        "tr": "Kritik karar alanları kaynaklıdır. Açık kalanlar: kesin Rumence belgesi/hazırlık yılı koşulları, AB dışı sınav formatı, GRE politikası, sonraki dönem tarih ve ücretleri, güncel burs kapsamı, programa özgü araştırma projeleri, işveren ortaklıkları, sonuçlar, sıralamalar ve görüşler.",
    }
    record["source_profile"]["field_confidence"]["research"] = "medium"
    record["data_quality"]["checked_official_source_count"] = 12
    record["quality_control"]["qc_notes"] = {
        "en": "Current curriculum is fully verified and explicitly classified as aviation-management adjacent, not technical space engineering; language and outcome uncertainties remain open.",
        "tr": "Güncel müfredat tamamen doğrulandı ve teknik uzay mühendisliği değil, havacılık-yönetim komşu alanı olarak açıkça sınıflandırıldı; dil ve sonuç belirsizlikleri açık kaldı.",
    }
    record["quality_control"]["remaining_verification_tasks"][2] = {
        "en": "Verify programme-specific research projects, aviation employer partnerships, external placement arrangements and quantified outcomes.",
        "tr": "Programa özgü araştırma projelerini, havacılık işveren ortaklıklarını, dış yerleştirme düzenlemelerini ve nicel sonuçları doğrulayın.",
    }
    return record


records = load(DB_PATH)
existing = {record.get("id") for record in records}
for spec in PROGRAMMES:
    if spec["id"] in existing:
        raise SystemExit(f"Record already exists: {spec['id']}")
template = next(record for record in records if record.get("id") == TEMPLATE_ID)
records.extend(build_record(template, spec) for spec in PROGRAMMES)
save(DB_PATH, records)

queue = load(QUEUE_PATH)
for spec in PROGRAMMES:
    candidate = next(item for item in queue["candidates"] if item.get("candidate_id") == spec["id"])
    candidate["program_name"] = spec["name"]
    candidate["discovery_status"] = "promoted_to_full_record"
    candidate["known_cautions"] = [{
        "en": "The current curriculum is aviation-management and operations oriented; it has very low spacecraft-engineering fit and is Romanian-taught.",
        "tr": "Güncel müfredat havacılık yönetimi ve operasyon odaklıdır; uzay aracı mühendisliği uygunluğu çok düşüktür ve eğitim dili Rumencedir.",
    }]
save(QUEUE_PATH, queue)

discovery = load(DISCOVERY_PATH)
for spec in PROGRAMMES:
    candidate = next(item for item in discovery["included_candidates"] if item.get("candidate_id") == spec["id"])
    candidate["programme"] = spec["name"]
    candidate["status"] = "promoted_to_full_record"
discovery["discovery_result"]["full_v2_records"] = 7
discovery["discovery_result"]["queued_for_full_research"] = 3
save(DISCOVERY_PATH, discovery)

scan_log = load(SCAN_PATH)
scan = next(item for item in scan_log["scans"] if item.get("country") == "Romania")
scan["full_records_added"] = 7
scan["notes"] = {
    "en": "Seven of ten Romanian candidates are now native V2. Engineering and Aerospace Management and Aeronautical Management were retained as aviation-management adjacent records after current curricula proved very low spacecraft-engineering fit. Three candidates remain queued; curriculum-led adjacent-programme discovery remains open.",
    "tr": "On Romanya adayının yedisi artık doğal V2'dir. Engineering and Aerospace Management ile Aeronautical Management, güncel müfredatları çok düşük uzay aracı mühendisliği uygunluğu gösterdikten sonra havacılık-yönetim komşu kayıtları olarak tutuldu. Üç aday kuyrukta kaldı; müfredat odaklı komşu program keşfi açıktır.",
}
save(SCAN_PATH, scan_log)

print("Added two adjacent aviation-management V2 records; Romania discovery is now 7/10 full records.")
