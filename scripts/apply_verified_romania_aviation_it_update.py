"""Promote Information Technologies Applied in Aviation to a native V2 record."""

from __future__ import annotations

import copy
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data_base" / "romania.json"
QUEUE_PATH = ROOT / "research_queue" / "program_candidates_v2.json"
DISCOVERY_PATH = ROOT / "reports" / "romania_programme_discovery_2026-08-14.json"
SCAN_PATH = ROOT / "research_queue" / "country_scan_log_v2.json"
TEMPLATE_ID = "ro-politehnica-bucharest-air-transport-engineering-msc"
RECORD_ID = "ro-politehnica-bucharest-information-technologies-aviation-msc"
PROGRAM_URL = "https://international.upb.ro/admission/study-offers/program/information-technologies-applied-in-aviation"
DEPARTMENT_URL = "https://www.unesco.chair.upb.ro/programe/"
CURRICULUM_URL = "https://international.upb.ro/curriculum/adf49f1afd9ee48b66f4b0b5dfb7f216.pdf"
ADMISSION_URL = "https://www.unesco.chair.upb.ro/admitere/"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path: Path, payload) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


records = load(DB_PATH)
if any(record.get("id") == RECORD_ID for record in records):
    raise SystemExit(f"Record already exists: {RECORD_ID}")
template = next(record for record in records if record.get("id") == TEMPLATE_ID)
record = copy.deepcopy(template)
record["id"] = RECORD_ID
record["program_profile"].update({
    "name": "Information Technologies Applied in Aviation",
    "native_name": "Tehnologii informatice aplicate în aviație",
    "degree_award": "Master's degree in Computers and Information Technology",
    "degree_class": "graduate_taught_with_research",
    "department": "UNESCO Chair Engineering for Society",
    "faculty_or_school": "Faculty of Automatic Control and Computer Science",
    "official_url": PROGRAM_URL,
    "relevance_status": "medium",
})
record["eligibility_profile"].update({
    "required_previous_degree": {
        "en": "A completed bachelor's degree or equivalent is required. The current official programme page welcomes Information Technology, Computer Science, Software Engineering, Cybersecurity, Electronics, Telecommunications, aviation and related engineering backgrounds.",
        "tr": "Tamamlanmış lisans derecesi veya eşdeğeri gerekir. Güncel resmî program sayfası Bilgi Teknolojileri, Bilgisayar Bilimleri, Yazılım Mühendisliği, Siber Güvenlik, Elektronik, Telekomünikasyon, havacılık ve ilgili mühendislik altyapılarını kabul eder.",
    },
    "accepted_backgrounds": [
        "Information Technology",
        "Computer Science",
        "Software Engineering",
        "Cybersecurity",
        "Electronics",
        "Telecommunications",
        "Aviation",
        "Related engineering fields subject to evaluation",
    ],
    "selection_criteria": [
        "Non-EU route: complete-file eligibility and academic evaluation under the international admission methodology",
        "General/EU route: programme interview or other faculty assessment under the master regulation",
        "Minimum general admission-exam average of 6.00/10 for the general route",
    ],
    "admission_risk": "medium",
    "other_standardized_tests": [],
    "notes_for_turkish_students": {
        "en": "Türkiye applicants use the non-EU route. The programme is a technical aviation-ICT degree, not an aerospace-design master. Begin legalization and certified translations early; no Turkish GPA conversion or GRE rule was inferred.",
        "tr": "Türkiye'den adaylar AB dışı rotayı kullanır. Program teknik bir havacılık-BT derecesidir; havacılık-uzay tasarım yüksek lisansı değildir. Tasdik ve yeminli tercümeleri erken başlatın; Türk not dönüşümü veya GRE kuralı çıkarılmadı.",
    },
})
record["eligibility_profile"]["interview"] = {
    "required": None,
    "notes": {
        "en": "The UNESCO Chair published a programme interview for the 11 May 2026 early-admission session. The exact interview format and whether it applies identically to the central non-EU route require route-specific confirmation.",
        "tr": "UNESCO Kürsüsü 11 Mayıs 2026 erken kabul oturumu için program mülakatı yayımladı. Kesin mülakat formatı ve merkezî AB dışı rotaya aynı biçimde uygulanıp uygulanmadığı rota bazında teyit edilmelidir.",
    },
}
record["language_profile"]["mixed_language_warning"] = {
    "en": "The programme is officially fully taught in English. The 2026 non-EU guide states minimum B1, while the 2026 general master regulation requires minimum B2 unless another listed proof route applies. Plan for B2 and obtain route-specific written confirmation.",
    "tr": "Program resmî olarak tamamen İngilizce yürütülür. 2026 AB dışı rehberi en az B1, 2026 genel yüksek lisans yönetmeliği ise alternatif kanıt yollarından biri yoksa en az B2 ister. B2 düzeyini hedefleyin ve başvuru rotasına özgü yazılı teyit alın.",
}
record["curriculum_profile"] = {
    "academic_cycle": "current undated curriculum linked by the official programme page; checked 2026-08-14",
    "tracks": [],
    "specializations": [],
    "course_count": {
        "minimum": 23,
        "maximum": 23,
        "counting_rule": "Twenty-three course selections are taken: semester 1 has three core rows plus one complete four-course package; semester 2 has six core rows plus one of two three-ECTS electives; semester 3 has seven rows; semester 4 has research/dissertation and Ethics. The PDF publishes 28 unique rows because both first-semester packages and both second-semester electives are displayed.",
    },
    "credit_breakdown": [
        {"component": "Taught aviation/ICT modules and Ethics", "credits": 62},
        {"component": "Student Research Projects in semesters 1-3", "credits": 30},
        {"component": "Student Research Project and Dissertation Preparation", "credits": 28},
    ],
    "mandatory_courses": [
        "Air Transport Economics",
        "Strategic Management in Aviation",
        "Student Research Project - Semester 1",
        "Aviation Operations Optimization Methods",
        "Modeling Theory and Tools in Aviation",
        "Specific Platforms and Tools for Aviation",
        "ATM Information Network Management",
        "Aviation Safety Management",
        "Student Research Project - Semester 2",
        "Data and Decision Support Management",
        "CAD/CAM Methodology",
        "Computer Vision",
        "Unmanned Air Vehicles and their IT Needs",
        "Cybersecurity Systems Management in Aviation",
        "Reliability of Hardware and Software in Aviation",
        "Student Research Project - Semester 3",
        "Student Research Project and Dissertation Preparation",
        "Ethics",
    ],
    "elective_courses": [
        "Aviation package: Aerodynamics and Flight Mechanics",
        "Aviation package: Airline Operations",
        "Aviation package: Airport Management and Infrastructure",
        "Aviation package: Air Traffic Management",
        "ICT package: Software Engineering",
        "ICT package: System Engineering Development",
        "ICT package: Data Center Architecture",
        "ICT package: Smart Data Processing",
        "Airworthiness",
        "Intelligent Interfaces",
    ],
    "lab_courses": [],
    "project_based_courses": [
        "Student Research Project - Semester 1",
        "Student Research Project - Semester 2",
        "Student Research Project - Semester 3",
        "Student Research Project and Dissertation Preparation",
    ],
    "thesis": {
        "required": True,
        "credits": 28,
        "options": ["The final curriculum row combines a student research project with dissertation preparation for 28 ECTS."],
    },
    "internship": {
        "required": None,
        "credits": None,
        "duration": None,
        "allocation": "not_published",
        "notes": {
            "en": "The current curriculum publishes research projects but no mandatory external internship or guaranteed employer placement.",
            "tr": "Güncel müfredat araştırma projeleri yayımlar; zorunlu dış staj veya garantili işveren yerleştirmesi yayımlamaz.",
        },
    },
    "mobility_options": ["Erasmus+ opportunities are stated by the UNESCO Chair; programme-specific places are not guaranteed"],
    "double_degree_options": [],
    "curriculum_urls": [CURRICULUM_URL],
}
record["category_profile"] = {
    "primary_categories": ["aviation_information_technology", "software_data_ai"],
    "secondary_categories": ["aviation_cybersecurity", "computer_vision", "unmanned_aircraft_systems", "atm_information_networks", "systems_engineering", "decision_support", "smart_data"],
    "subcategories": ["aviation_software_reliability", "data_center_architecture", "aviation_platforms", "cad_cam", "intelligent_interfaces", "air_transport_digitalization"],
    "normalized_tags": ["aviation_ict", "software_engineering", "systems_engineering", "data", "cybersecurity", "computer_vision", "uav", "atm_networks", "decision_support"],
    "category_scores": {"space_systems": 8, "satellite_systems": 2, "gnc": 18, "propulsion": 0, "aerodynamics_cfd": 12, "structures_materials": 0, "space_science": 0},
    "category_evidence": ["The current 120-ECTS curriculum is technically relevant to aviation ICT, software, systems, data, cybersecurity, computer vision, UAV needs and ATM networks; it does not publish spacecraft, satellite, orbital, propulsion or space-science modules."],
}
record["research_profile"] = {
    "research_areas": ["Aviation ICT", "Air-transport digitalization", "Aviation cybersecurity", "Computer vision", "Unmanned-aircraft IT", "ATM information networks", "Data and decision support", "Software and hardware reliability in aviation"],
    "labs": [],
    "research_centers": ["UNESCO Chair Engineering for Society"],
    "facilities": [],
    "projects": [],
    "student_teams": [],
    "research_opportunity_for_masters": "58_ects_embedded_research_project_sequence",
    "research_strength_score": 68,
    "summary": {
        "en": "Research is structurally substantial at 58 ECTS across four project/dissertation rows. The official programme page says students may cooperate with international professors and air-transport representatives, but no named current project allocation, laboratory equipment or guaranteed external placement was verified.",
        "tr": "Araştırma dört proje/tez satırında 58 AKTS ile yapısal olarak yüksektir. Resmî program sayfası öğrencilerin uluslararası öğretim üyeleri ve hava taşımacılığı temsilcileriyle çalışabileceğini söyler; ancak isimli güncel proje tahsisi, laboratuvar ekipmanı veya garantili dış yerleştirme doğrulanmadı.",
    },
}
record["industry_ecosystem_profile"] = {
    "confirmed_partners": [],
    "industry_supporters_named_by_university": ["International Civil Aviation Organization (ICAO)", "COMOTI", "Bucharest Airports National Company (CNAB)", "Menzies Aviation", "DB Systel", "Romanian Ministry of Transportation"],
    "nearby_organizations": [],
    "space_agencies_or_public_bodies": [],
    "research_institutes": [],
    "startup_or_incubator_ecosystem": [],
    "internship_access": "research_collaboration_possible_external_placement_not_published",
    "industry_thesis_access": "possible_not_guaranteed",
    "career_relevance": "high_for_aviation_ict_low_for_spacecraft_engineering",
    "ecosystem_strength_score": None,
    "summary": {
        "en": "The university names multiple aviation and IT supporters and international academic contributors, but no partner-side confirmation, placement guarantee or placement rate was checked. Treat this as a university-reported network, not proof of an employment pipeline or spacecraft-sector access.",
        "tr": "Üniversite birden fazla havacılık/BT destekçisi ve uluslararası akademik katkı sağlayıcı adı verir; ancak ortak tarafı teyidi, yerleştirme garantisi veya yerleştirme oranı kontrol edilmedi. Bunu istihdam hattı veya uzay aracı sektörüne erişim kanıtı değil, üniversite tarafından bildirilen ağ olarak değerlendirin.",
    },
}
record["ranking_profile"].update({
    "programme_reputation_evidence": ["The programme originated from the EU Erasmus+ Knowledge Alliance in Air Transport project according to POLITEHNICA; current outcome or ranking evidence was not inferred."],
    "prestige_summary": {
        "en": "No numerical ranking was added. Relevance is based on the current curriculum and official programme description; named networks and project origin are not treated as technical-space prestige or employment proof.",
        "tr": "Sayısal sıralama eklenmedi. Uygunluk güncel müfredat ve resmî program açıklamasına dayanır; isimli ağlar ve proje kökeni teknik uzay prestiji veya istihdam kanıtı sayılmaz.",
    },
})
record["decision_summary"] = {
    "overall_recommendation": "strong_aviation_ict_adjacent_option_low_direct_spacecraft_fit",
    "main_strengths": {
        "en": "English delivery, low published non-EU tuition, 58 ECTS of research, and a current curriculum spanning systems/software engineering, data, cybersecurity, computer vision, UAV IT and ATM networks.",
        "tr": "İngilizce eğitim, düşük yayımlanmış AB dışı ücret, 58 AKTS araştırma ve sistem/yazılım mühendisliği, veri, siber güvenlik, bilgisayarlı görü, İHA BT ve ATM ağlarını kapsayan güncel müfredat.",
    },
    "main_risks": {
        "en": "It is an aviation-ICT degree rather than aerospace or spacecraft engineering; no lab hours, mandatory external internship, GRE policy, partner-confirmed placement pipeline or quantified outcomes were verified.",
        "tr": "Havacılık-uzay veya uzay aracı mühendisliği değil, havacılık-BT derecesidir; laboratuvar saati, zorunlu dış staj, GRE politikası, ortak tarafından teyitli yerleştirme hattı veya nicel sonuç doğrulanmadı.",
    },
    "best_for": {
        "en": "Applicants targeting aviation software, cybersecurity, data science, computer vision, ATM information systems, smart airports or UAV-supporting IT roles.",
        "tr": "Havacılık yazılımı, siber güvenlik, veri bilimi, bilgisayarlı görü, ATM bilgi sistemleri, akıllı havalimanları veya İHA destekli BT rollerini hedefleyen adaylar.",
    },
    "not_ideal_for": {
        "en": "Students seeking spacecraft design, satellites, orbital mechanics, propulsion, structures, space science or a conventional aerospace-engineering credential.",
        "tr": "Uzay aracı tasarımı, uydular, yörünge mekaniği, itki, yapılar, uzay bilimi veya geleneksel havacılık-uzay mühendisliği derecesi arayan öğrenciler.",
    },
    "application_reality": {
        "en": "Türkiye applicants should use the February-July non-EU route, prepare legalized documents and B2-level English evidence early, allow at least 60 days for processing and obtain written confirmation of whether the programme interview applies to their route.",
        "tr": "Türkiye'den adaylar şubat-temmuz AB dışı rotasını kullanmalı, tasdikli belgeleri ve B2 düzeyi İngilizce kanıtını erken hazırlamalı, işlemler için en az 60 gün bırakmalı ve program mülakatının kendi rotalarına uygulanıp uygulanmadığını yazılı teyit etmelidir.",
    },
    "funding_reality": template["decision_summary"]["funding_reality"],
    "housing_reality": template["decision_summary"]["housing_reality"],
}
record["application_timeline_profile"]["deadline_events"].append({
    "event": "ITAA general/EU early-admission interview",
    "date": "2026-05-11",
    "date_status": "current_cycle_closed",
    "applicant_scope": "general_eu_domestic_route; non_eu applicability needs confirmation",
    "source_ids": ["ro_upb_itaa_admission"],
})
record["scoring_inputs"].update({
    "academic_field_fit_score_seed": 68,
    "eligibility_language_score_seed": 66,
    "career_research_score_seed": 68,
    "data_confidence_score_seed": 88,
})

replacement = {
    "ro_upb_program": "ro_upb_itaa_program",
    "ro_upb_faculty_masters": "ro_upb_itaa_department",
    "ro_upb_master_brochure": "ro_upb_itaa_curriculum",
    "ro_upb_faculty_admission": "ro_upb_itaa_admission",
}
for source in record["source_profile"]["source_log"]:
    source_id = source["source_id"]
    if source_id == "ro_upb_program":
        source.update({
            "source_id": replacement[source_id], "url": PROGRAM_URL, "final_url": PROGRAM_URL,
            "title": "Information Technologies Applied in Aviation",
            "relevant_fields": ["program", "language", "admission", "curriculum", "research", "industry"],
            "notes": {"en": "Current official programme description, English delivery, domain, faculty, industry-support statement and curriculum link.", "tr": "Güncel resmî program açıklaması, İngilizce eğitim, alan, fakülte, sanayi desteği beyanı ve müfredat bağlantısı."},
        })
    elif source_id == "ro_upb_faculty_masters":
        source.update({
            "source_id": replacement[source_id], "url": DEPARTMENT_URL, "final_url": DEPARTMENT_URL,
            "title": "UNESCO Chair Master Programmes - ITAA",
            "publisher": "UNESCO Chair Engineering for Society, POLITEHNICA Bucharest",
            "relevant_fields": ["program", "language", "curriculum"],
            "notes": {"en": "Current department page lists ITAA among English-taught interdisciplinary masters and links its curriculum.", "tr": "Güncel bölüm sayfası ITAA'yı İngilizce disiplinlerarası yüksek lisanslar arasında listeler ve müfredatına bağlanır."},
        })
    elif source_id == "ro_upb_master_brochure":
        source.update({
            "source_id": replacement[source_id], "url": CURRICULUM_URL, "final_url": CURRICULUM_URL,
            "title": "Information Technologies Applied in Aviation Curriculum",
            "published_or_effective_date": None,
            "applicable_academic_cycle": "current official link checked 2026-08-14; PDF itself is undated",
            "relevant_fields": ["program", "curriculum", "research"],
            "confidence": "high",
            "notes": {"en": "Both pages were extracted, rendered and visually checked; selection arithmetic totals 120 ECTS and 23 taken rows.", "tr": "İki sayfa da çıkarıldı, render edildi ve görsel olarak kontrol edildi; seçim aritmetiği 120 AKTS ve alınan 23 satır verir."},
        })
    elif source_id == "ro_upb_faculty_admission":
        source.update({
            "source_id": replacement[source_id], "url": ADMISSION_URL, "final_url": ADMISSION_URL,
            "title": "UNESCO Chair Master Admission 2026-2027",
            "publisher": "UNESCO Chair Engineering for Society, POLITEHNICA Bucharest",
            "relevant_fields": ["admission", "deadline"],
            "notes": {"en": "Current early-session dates and ITAA interview schedule; central non-EU applicability needs confirmation.", "tr": "Güncel erken oturum tarihleri ve ITAA mülakat programı; merkezî AB dışı rota uygulanabilirliği teyit bekler."},
        })

def replace_ids(value):
    if isinstance(value, list):
        return [replacement.get(item, item) for item in value]
    return replacement.get(value, value)


record["source_profile"]["evidence_map"] = {
    key: replace_ids(value) for key, value in record["source_profile"]["evidence_map"].items()
}
record["source_profile"]["evidence_map"]["industry"] = ["ro_upb_itaa_program"]
record["source_profile"]["evidence_map"]["research"] = ["ro_upb_itaa_curriculum", "ro_upb_itaa_program"]
record["source_profile"]["verification_notes"] = {
    "en": "Critical decision fields are sourced. Open items: exact accepted English threshold for the non-EU route, route-specific interview format, GRE policy, dated curriculum cycle, current scholarship benefits, lab/facility inventory, partner-side collaboration confirmation, internship access, outcomes, rankings and sentiment.",
    "tr": "Kritik karar alanları kaynaklıdır. Açık kalanlar: AB dışı rota için kesin İngilizce eşiği, rota bazlı mülakat formatı, GRE politikası, tarihli müfredat dönemi, güncel burs kapsamı, laboratuvar/tesis envanteri, ortak taraflı iş birliği teyidi, staj erişimi, sonuçlar, sıralamalar ve görüşler.",
}
record["source_profile"]["field_confidence"].update({"curriculum": "high", "research": "medium", "industry": "medium"})
record["data_quality"].update({"checked_official_source_count": 11})
record["quality_control"]["remaining_verification_tasks"] = [
    {"en": "Confirm the exact non-EU English threshold, accepted certificates, interview format and GRE policy in writing.", "tr": "Kesin AB dışı İngilizce eşiğini, kabul edilen belgeleri, mülakat formatını ve GRE politikasını yazılı teyit edin."},
    {"en": "Obtain a curriculum document with an explicit academic cycle and confirm the elective-package selection rule.", "tr": "Açık akademik dönem taşıyan müfredat belgesi edinin ve seçmeli paket seçim kuralını teyit edin."},
    {"en": "Verify partner-side collaboration, named facilities, mandatory/optional internship access and quantified graduate outcomes.", "tr": "Ortak taraflı iş birliğini, isimli tesisleri, zorunlu/isteğe bağlı staj erişimini ve nicel mezun sonuçlarını doğrulayın."},
    {"en": "Recheck 2027/28 tuition, deadlines and scholarship benefits and collect independent programme-specific sentiment.", "tr": "2027/28 ücretlerini, tarihlerini ve burs kapsamını yeniden kontrol edin; bağımsız programa özgü öğrenci görüşü toplayın."},
]
record["quality_control"]["qc_notes"] = {
    "en": "The programme is correctly retained as a medium-relevance technical aviation-ICT option; direct spacecraft fit remains low and industry claims remain one-sided where partner confirmation is absent.",
    "tr": "Program orta uygunlukta teknik havacılık-BT seçeneği olarak doğru biçimde tutulur; doğrudan uzay aracı uygunluğu düşük, ortak teyidi olmayan sanayi iddiaları tek taraflıdır.",
}

records.append(record)
save(DB_PATH, records)

queue = load(QUEUE_PATH)
candidate = next(item for item in queue["candidates"] if item.get("candidate_id") == RECORD_ID)
candidate["discovery_status"] = "promoted_to_full_record"
candidate["known_cautions"] = [{
    "en": "The current curriculum proves technical aviation-ICT depth in software, data, cybersecurity, computer vision, UAV needs and ATM networks, but direct spacecraft-engineering fit is low and the curriculum PDF is undated.",
    "tr": "Güncel müfredat yazılım, veri, siber güvenlik, bilgisayarlı görü, İHA ihtiyaçları ve ATM ağlarında teknik havacılık-BT derinliğini kanıtlar; ancak doğrudan uzay aracı mühendisliği uygunluğu düşüktür ve müfredat PDF'si tarihsizdir.",
}]
save(QUEUE_PATH, queue)

discovery = load(DISCOVERY_PATH)
candidate = next(item for item in discovery["included_candidates"] if item.get("candidate_id") == RECORD_ID)
candidate["status"] = "promoted_to_full_record"
discovery["discovery_result"]["full_v2_records"] = 8
discovery["discovery_result"]["queued_for_full_research"] = 2
save(DISCOVERY_PATH, discovery)

scan_log = load(SCAN_PATH)
scan = next(item for item in scan_log["scans"] if item.get("country") == "Romania")
scan["full_records_added"] = 8
scan["notes"] = {
    "en": "Eight of ten Romanian candidates are now native V2. Information Technologies Applied in Aviation was retained as a medium-relevance English-taught aviation-ICT option after its current curriculum proved software, data, cybersecurity, computer-vision, UAV and ATM-network depth but low direct spacecraft fit. University of Craiova and the Military Technical Academy remain queued.",
    "tr": "On Romanya adayının sekizi artık doğal V2'dir. Information Technologies Applied in Aviation, güncel müfredatı yazılım, veri, siber güvenlik, bilgisayarlı görü, İHA ve ATM ağı derinliği ancak düşük doğrudan uzay aracı uygunluğu gösterdikten sonra orta uygunlukta İngilizce havacılık-BT seçeneği olarak tutuldu. Craiova Üniversitesi ve Askerî Teknik Akademi kuyrukta kaldı.",
}
save(SCAN_PATH, scan_log)

print("Added ITAA native V2 record; Romania discovery is now 8/10 full records.")
