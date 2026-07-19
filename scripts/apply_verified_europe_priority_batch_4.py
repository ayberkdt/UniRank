"""Add four source-verified European programmes and refresh ISAE-SUPAERO timing.

The records deliberately retain unknowns where an official source did not
publish a programme-specific value.  Running this file repeatedly is safe.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from unirank.core.integrity import audit_record


CHECKED = "2026-07-19"
DATA = ROOT / "data_base"


def bi(en: str, tr: str) -> dict[str, str]:
    return {"en": en, "tr": tr}


def source(
    url: str,
    title: str,
    source_type: str,
    fields: list[str],
    notes_en: str,
    notes_tr: str,
    *,
    access_status: str = "ok",
    confidence: str = "high",
) -> dict[str, Any]:
    return {
        "url": url,
        "source_type": source_type,
        "title": title,
        "access_status": access_status,
        "last_checked": CHECKED,
        "relevant_fields": fields,
        "confidence": confidence,
        "notes": bi(notes_en, notes_tr),
    }


def empty_sentiment() -> dict[str, Any]:
    return {
        "student_satisfaction_score": None,
        "sentiment_confidence": "unknown",
        "sample_size_estimate": None,
        "date_range": "",
        "teaching_quality_sentiment": "",
        "workload_sentiment": "",
        "administration_sentiment": "",
        "housing_sentiment": "",
        "city_life_sentiment": "",
        "international_student_support_sentiment": "",
        "career_support_sentiment": "",
        "positive_themes": [],
        "negative_themes": [],
        "recurring_complaints": [],
        "recurring_strengths": [],
        "sentiment_summary": bi(
            "No sufficiently documented programme-specific student sample was retained; no score is shown.",
            "Yeterince belgelenmiş programa özgü öğrenci örneklemi tutulmadı; puan gösterilmiyor.",
        ),
        "student_sentiment_sources": [],
    }


def common_profiles() -> dict[str, Any]:
    return {
        "research_profile": {
            "department_research_areas": [],
            "labs": [],
            "research_centers": [],
            "space_or_aerospace_projects": [],
            "research_strength_summary": bi("", ""),
            "research_strength_score": None,
            "research_sources": [],
        },
        "industry_ecosystem_profile": {
            "nearby_companies": [],
            "confirmed_partners": [],
            "space_agencies_or_public_bodies": [],
            "research_institutes": [],
            "internship_possibility": "unknown",
            "thesis_with_industry_possibility": "unknown",
            "career_relevance": bi("", ""),
            "ecosystem_strength_score": None,
            "ecosystem_notes": bi("", ""),
        },
        "student_sentiment_profile": empty_sentiment(),
        "scoring_inputs": {
            "academic_field_fit_score_seed": None,
            "eligibility_language_score_seed": None,
            "cost_funding_score_seed": None,
            "career_research_score_seed": None,
            "living_risk_score_seed": None,
            "data_confidence_score_seed": None,
            "student_satisfaction_score_seed": None,
            "hard_filter_flags": {
                "english_only_compatible": True,
                "requires_local_language": False,
                "non_eu_eligible": True,
                "tuition_above_5000": None,
                "tuition_above_10000": None,
                "deadline_unclear": None,
                "needs_verification": False,
            },
        },
    }


def finalise(record: dict[str, Any]) -> dict[str, Any]:
    quality = audit_record(record)
    record["data_quality"] = {**quality, "audited_at": CHECKED}
    verified = quality["status"] == "verified"
    record["source_profile"]["needs_verification"] = not verified
    record["quality_control"] = {
        "qc_status": "passed" if verified else "needs_revision",
        "checked_at": CHECKED,
        "failed_canary_tests": [] if verified else ["missing_or_unverified_critical_fields"],
        "remaining_verification_tasks": [
            bi(f"Add checked official evidence for {field}.", f"{field} için kontrol edilmiş resmî kanıt ekleyin.")
            for field in quality["unverified_critical_fields"]
        ],
        "qc_notes": bi(
            "Source-evidence audit completed; unknown fields remain explicit and sentiment is not scored.",
            "Kaynak-kanıt denetimi tamamlandı; bilinmeyen alanlar açık bırakıldı ve öğrenci görüşü puanlanmadı.",
        ),
    }
    return record


def surrey() -> dict[str, Any]:
    programme = "https://www.surrey.ac.uk/postgraduate/astronautics-and-space-engineering-msc"
    housing = "https://www.surrey.ac.uk/sites/default/files/2026-01/Accommodation%20Tarriff%2026-27.pdf"
    visa_budget = "https://www.gov.uk/student-visa/money"
    record: dict[str, Any] = {
        "id": "uk-surrey-astronautics-space-engineering-msc",
        "country": "United Kingdom",
        "university": "University of Surrey",
        "university_native_name": "University of Surrey",
        "city": "Guildford",
        "region": "England",
        "program_name": "Astronautics and Space Engineering MSc",
        "program_native_name": "Astronautics and Space Engineering MSc",
        "program_degree": "MSc",
        "degree_level": "Master",
        "degree_class": "Postgraduate taught",
        "duration_years": 1,
        "ects": None,
        "teaching_language": ["English"],
        "program_url": programme,
        "department": "School of Computer Science and Electronic Engineering",
        "campus": "Guildford",
        "program_status": "active",
        "relevance_status": "strong",
        "eligibility_profile": {
            "eligible_for_non_eu": True,
            "required_previous_degree": bi(
                "At least a UK 2:2 honours degree, or recognised international equivalent, in one of the engineering, physics or communications fields listed by Surrey; relevant work experience may also be considered.",
                "Surrey'nin listelediği mühendislik, fizik veya haberleşme alanlarından birinde en az Birleşik Krallık 2:2 onur derecesi ya da tanınan uluslararası dengi; ilgili iş deneyimi de değerlendirilebilir.",
            ),
            "accepted_backgrounds": [
                "Aerospace engineering", "Mechanical engineering", "Electrical/electronic/computer engineering",
                "Communications/telecommunications", "Physics",
            ],
            "minimum_gpa": None,
            "admission_mode": "application review",
            "admission_risk": "medium",
            "required_documents": [],
            "verification_notes": bi(
                "The course page explicitly publishes overseas application routes; equivalence remains an individual admissions decision.",
                "Program sayfası yurtdışı başvuru yolunu açıkça yayımlar; denklik yine bireysel kabul kararıdır.",
            ),
        },
        "language_profile": {
            "teaching_language": ["English"],
            "english_required": True,
            "english_level_required": "IELTS Academic 6.5 overall; 6.0 writing and 5.5 in each other element",
            "accepted_english_tests": ["IELTS Academic", "Other Surrey-accepted equivalents"],
            "mixed_language_warning": "",
            "language_risk": "low",
        },
        "cost_profile": {
            "academic_year": "2026/2027",
            "tuition_eur_per_year_min": None,
            "tuition_eur_per_year_max": None,
            "tuition_eur_per_year_estimated": None,
            "tuition_gbp_per_year": 25900,
            "tuition_basis": "full-time overseas fee for September 2026 or February 2027 entry",
            "application_fee_eur": None,
            "source_notes": bi(
                "Surrey publishes GBP 25,900 for the one-year full-time overseas route; no EUR conversion is stored.",
                "Surrey bir yıllık tam zamanlı yurtdışı öğrenci yolu için 25.900 GBP yayımlar; EUR dönüşümü kaydedilmez.",
            ),
        },
        "scholarship_profile": {
            "regional_scholarship_available": True,
            "regional_scholarship_name": "Surrey postgraduate scholarships and programme-page awards",
            "merit_scholarships": ["Vietnam Merit Scholarship (nationality-specific, 2026 call)", "Surrey graduate discount"],
            "tuition_waivers": ["Vietnam Merit Scholarship: GBP 10,000 waiver, eligibility-specific"],
            "non_eu_eligible": True,
            "scholarship_deadline": "2026-07-20 (Vietnam Merit Scholarship only; other awards have separate rules)",
            "scholarship_application_url": programme,
            "funding_competitiveness": "high",
            "funding_notes": bi(
                "The course page lists funding routes, but the named GBP 10,000 waiver is nationality-specific and is not a general award for Turkish applicants.",
                "Program sayfası finansman yollarını listeler; ancak 10.000 GBP'lik muafiyet belirli uyruklara özeldir ve Türk adaylar için genel bir burs değildir.",
            ),
        },
        "living_profile": {
            "city_cost_level": "unknown",
            "monthly_living_cost_gbp_per_month_min": 1171,
            "housing_difficulty": "unknown",
            "student_housing_available": True,
            "housing_risk": "medium",
            "living_risk": "medium",
            "housing_notes": bi(
                "GBP 1,171/month is the current UK Student-visa maintenance requirement for study outside London, not a Guildford spending estimate. Surrey's 2026/27 long-stay student rooms run from GBP 89.50 to GBP 217 per week and availability/room band is not guaranteed.",
                "Aylık 1.171 GBP, Londra dışındaki eğitim için güncel Birleşik Krallık öğrenci vizesi geçim şartıdır; Guildford harcama tahmini değildir. Surrey'nin 2026/27 uzun süreli öğrenci odaları haftalık 89,50–217 GBP aralığındadır; bulunabilirlik ve oda bandı garanti değildir.",
            ),
        },
        "curriculum_profile": {
            "tracks": [],
            "specializations": [],
            "mandatory_courses": ["Space Dynamics and Missions", "Space System Design", "Research, Professionalism and Innovation", "60 Credit Standard Project"],
            "elective_courses": ["Advanced Guidance, Navigation and Control", "Launch Vehicles and Propulsion", "Space Environment and Protection", "Spacecraft Structures and Mechanisms", "Satellite Communications"],
            "thesis_required": True,
            "internship_required": False,
            "project_based_courses": ["60 Credit Standard Project"],
            "curriculum_url": programme,
        },
        "category_profile": {
            "primary_categories": ["Uzay Sistemleri ve Astronotik", "Sistem Mühendisliği, Tasarım ve Optimizasyon"],
            "secondary_categories": ["Uçuş Mekaniği, Kontrol ve Otonomi", "İtki, Enerji ve Termal Sistemler", "Aviyonik, Yazılım ve Sayısal Teknolojiler"],
            "subcategories": [],
            "normalized_tags": ["space_systems", "spacecraft_gnc", "orbital_mechanics", "space_propulsion", "satellite_communications", "spacecraft_structures"],
            "category_scores": {},
            "category_evidence": [bi("Official 2026 module list and course description.", "Resmî 2026 ders listesi ve program açıklaması.")],
        },
        "application_timeline_profile": {
            "academic_year": "2026/2027",
            "intake_terms": ["September 2026", "February 2027"],
            "application_rounds": [],
            "non_eu_deadline": "2026-07-24 (September 2026 overseas route); 2026-12-11 (February 2027 overseas route)",
            "eu_deadline": "2026-09-01 (September UK route); 2027-01-23 (February UK route)",
            "timeline_risk": "medium",
            "deadline_notes": bi(
                "Surrey may close applications earlier if the course fills; applicants needing a visa should use the overseas deadline.",
                "Program dolarsa Surrey başvuruları daha erken kapatabilir; vize gereken adaylar yurtdışı son tarihini kullanmalıdır.",
            ),
        },
        "source_profile": {
            "official_program_page": programme,
            "official_admission_page": programme,
            "official_tuition_page": programme,
            "official_scholarship_page": programme,
            "official_curriculum_page": programme,
            "official_housing_page": housing,
            "source_log": [
                source(programme, "Surrey Astronautics and Space Engineering MSc — 2026 entry", "official_program_page", ["program", "language", "curriculum", "deadline"], "Current course page confirms status, duration, English requirement, modules and application dates.", "Güncel program sayfası durum, süre, İngilizce koşulu, dersler ve başvuru tarihlerini doğrular."),
                source(programme, "Surrey Astronautics and Space Engineering entry requirements", "official_admission_page", ["admission", "non_eu_eligibility", "language", "deadline"], "The page lists recognised international qualifications and separate overseas application routes.", "Sayfa tanınan uluslararası yeterlilikleri ve ayrı yurtdışı başvuru yollarını listeler."),
                source(programme, "Surrey Astronautics and Space Engineering fees", "official_tuition_page", ["tuition"], "Programme-specific 2026/27 overseas fee is published in GBP.", "Programa özgü 2026/27 yurtdışı ücreti GBP olarak yayımlanır."),
                source(programme, "Surrey course scholarships and bursaries", "official_scholarship_page", ["scholarship", "funding"], "Awards shown on the course page are eligibility-specific and are not treated as universal.", "Program sayfasındaki ödüller uygunluk koşulludur ve herkese açık kabul edilmez."),
                source(programme, "Surrey Astronautics and Space Engineering course structure", "official_curriculum_page", ["curriculum", "courses"], "The page publishes compulsory and optional 2026 modules.", "Sayfa 2026 zorunlu ve seçmeli derslerini yayımlar."),
                source(housing, "University of Surrey accommodation price list 2026/27", "official_housing_page", ["housing"], "Official PDF gives weekly student room prices and inclusions; it does not guarantee a room.", "Resmî PDF haftalık öğrenci odası fiyatlarını ve kapsamı verir; oda garantisi sağlamaz.", access_status="pdf"),
                source(visa_budget, "UK Student visa maintenance funds", "official_visa_or_government_page", ["housing", "living", "visa"], "Government requirement is retained as a visa-planning floor, not as an actual Guildford budget.", "Hükümet şartı gerçek Guildford bütçesi değil, vize planlama alt sınırı olarak tutulur."),
            ],
            "last_verified": CHECKED,
            "verification_notes": bi("All critical decision values are tied to checked official sources; scholarship eligibility remains award-specific.", "Tüm kritik karar değerleri kontrol edilmiş resmî kaynaklara bağlıdır; burs uygunluğu ödüle özgüdür."),
            "field_confidence": {"program_basic_info": "high", "language": "high", "admission": "high", "tuition": "high", "scholarship": "high", "curriculum": "high", "research": "medium", "industry": "medium", "living": "high", "student_sentiment": "unknown"},
        },
        "decision_summary": {
            "overall_recommendation": "strong",
            "main_strengths": bi("Direct spacecraft-systems MSc with GNC, mission design, propulsion, structures and satellite communications, backed by Surrey Space Centre activity.", "GNC, görev tasarımı, itki, yapılar ve uydu haberleşmesini kapsayan; Surrey Space Centre faaliyetleriyle desteklenen doğrudan uzay aracı sistemleri MSc'si."),
            "main_risks": bi("High overseas tuition; scholarship routes are not universal and the September overseas deadline is visa-sensitive.", "Yüksek yurtdışı öğrenim ücreti; burs yolları herkese açık değil ve Eylül yurtdışı son tarihi vize açısından hassas."),
            "best_for": bi("Applicants targeting spacecraft systems, satellite engineering, mission design or GNC.", "Uzay aracı sistemleri, uydu mühendisliği, görev tasarımı veya GNC hedefleyen adaylar."),
            "not_ideal_for": bi("Applicants requiring a low-cost programme or a guaranteed broad scholarship.", "Düşük maliyetli program ya da garanti kapsamlı burs arayan adaylar."),
            "application_reality": bi("Academically accessible from several engineering/physics backgrounds, but funding and the overseas deadline require early planning.", "Çeşitli mühendislik/fizik altyapılarından akademik olarak erişilebilir; ancak finansman ve yurtdışı son tarihi erken planlama gerektirir."),
        },
        **common_profiles(),
    }
    record["research_profile"].update({
        "department_research_areas": ["Space mission design and operations", "Spacecraft and payload technologies"],
        "research_centers": ["Surrey Space Centre"],
        "research_strength_summary": bi("Applied space-engineering activity spans complete missions and spacecraft technologies.", "Uygulamalı uzay mühendisliği faaliyeti tam görevleri ve uzay aracı teknolojilerini kapsar."),
        "research_sources": [programme],
    })
    record["industry_ecosystem_profile"].update({
        "confirmed_partners": ["Surrey Satellite Technology Ltd", "Airbus"],
        "internship_possibility": "programme page confirms industry-linked student projects; no universal placement is promised",
        "thesis_with_industry_possibility": "many student projects are described as industry-collaborative",
        "career_relevance": bi("The official course page links projects and graduate outcomes to the UK space sector.", "Resmî program sayfası projeleri ve mezun sonuçlarını Birleşik Krallık uzay sektörüyle ilişkilendirir."),
    })
    return finalise(record)


def ensma() -> dict[str, Any]:
    programme = "https://www.ensma.fr/en/master-of-science-in-aeronautics-and-space/international-msc-ame-presentation/"
    admission = "https://www.ensma.fr/en/master-of-science-in-aeronautics-and-space/ame-admission/"
    housing = "https://www.univ-poitiers.fr/wp-content/uploads/sites/10/2026/04/2026_DESCRIPTION_CROUS_ENG_compressed1-1.pdf"
    record: dict[str, Any] = {
        "id": "fr-isae-ensma-msc-ame",
        "country": "France",
        "university": "ISAE-ENSMA",
        "university_native_name": "École Nationale Supérieure de Mécanique et d’Aérotechnique",
        "city": "Poitiers-Futuroscope",
        "region": "Nouvelle-Aquitaine",
        "program_name": "Master of Science in Aeronautics and Space — Aeronautical Mechanics and Energetics (AME)",
        "program_native_name": "Master of Science in Aeronautics and Space — Aeronautical Mechanics and Energetics",
        "program_degree": "MSc",
        "degree_level": "Master",
        "degree_class": "International Master of Science",
        "duration_years": 2,
        "ects": None,
        "teaching_language": ["English"],
        "program_url": programme,
        "department": "ISAE-ENSMA",
        "campus": "Futuroscope",
        "program_status": "active",
        "relevance_status": "strong",
        "eligibility_profile": {
            "eligible_for_non_eu": True,
            "required_previous_degree": bi("Bachelor's degree or equivalent in aerospace, mechanical or mechatronics engineering, or science and engineering.", "Havacılık-uzay, makine veya mekatronik mühendisliği ya da bilim ve mühendislik alanında lisans veya dengi."),
            "accepted_backgrounds": ["Aerospace engineering", "Mechanical engineering", "Mechatronics", "Science and engineering"],
            "minimum_gpa": None,
            "admission_mode": "application review in published selection rounds",
            "admission_risk": "medium",
            "required_documents": [],
            "verification_notes": bi("The official page explicitly lists non-European tuition and a freemover route.", "Resmî sayfa AB dışı öğrenim ücretini ve bağımsız başvuru yolunu açıkça listeler."),
        },
        "language_profile": {
            "teaching_language": ["English"],
            "english_required": True,
            "english_level_required": "TOEFL iBT 79 / TOEFL paper 550 / IELTS 6.0 / TOEIC 750; other accepted tests may apply",
            "accepted_english_tests": ["TOEFL", "IELTS", "TOEIC", "Cambridge CAE and other accepted tests"],
            "mixed_language_warning": "",
            "language_risk": "low",
        },
        "cost_profile": {
            "academic_year": "current official page; amount may be re-evaluated annually",
            "tuition_eur_per_year_min": 7000,
            "tuition_eur_per_year_max": 7000,
            "tuition_eur_per_year_estimated": 7000,
            "tuition_basis": "non-European students per academic year",
            "application_fee_eur": None,
            "source_notes": bi("ISAE-ENSMA warns that registration fees may be re-evaluated at the start of each academic year.", "ISAE-ENSMA kayıt ücretlerinin her akademik yıl başında yeniden değerlendirilebileceğini bildirir."),
        },
        "scholarship_profile": {
            "regional_scholarship_available": True,
            "regional_scholarship_name": "Eiffel Excellence and Campus France routes",
            "merit_scholarships": ["Eiffel Excellence Scholarship (institutional nomination and first-panel timing)"],
            "tuition_waivers": [],
            "non_eu_eligible": True,
            "scholarship_deadline": "First selection panel in December for Eiffel support; verify the next call",
            "scholarship_application_url": admission,
            "funding_competitiveness": "high",
            "funding_notes": bi("ISAE-ENSMA names Eiffel and Campus France routes but does not promise funding to every admitted student.", "ISAE-ENSMA Eiffel ve Campus France yollarını belirtir; her kabul edilen öğrenciye finansman sözü vermez."),
        },
        "living_profile": {
            "city_cost_level": "unknown",
            "average_room_rent_eur_min": 264.23,
            "average_room_rent_eur_max": 693.04,
            "housing_difficulty": "unknown",
            "student_housing_available": True,
            "living_risk": "medium",
            "housing_notes": bi("The 2026/27 University of Poitiers international CROUS guide lists room/studio options from EUR 264.23 to EUR 693.04 per month; allocation is subject to availability and is not guaranteed for ISAE-ENSMA students.", "Université de Poitiers'nin 2026/27 uluslararası CROUS rehberi aylık 264,23–693,04 EUR oda/stüdyo seçenekleri listeler; tahsis bulunabilirliğe bağlıdır ve ISAE-ENSMA öğrencileri için garanti değildir."),
        },
        "curriculum_profile": {
            "tracks": ["Energetics for Propulsion (EPROP)", "High Temperature Materials (HTM)"],
            "specializations": ["Propulsion and energetics", "High-temperature materials"],
            "mandatory_courses": [],
            "elective_courses": [],
            "thesis_required": True,
            "internship_required": True,
            "project_based_courses": ["Industrial/research graduation internship and Master's thesis"],
            "curriculum_url": programme,
        },
        "category_profile": {
            "primary_categories": ["İtki, Enerji ve Termal Sistemler", "Yapılar, Malzemeler ve Mekanik Tasarım"],
            "secondary_categories": ["Akışkanlar Mekaniği ve Aerodinamik", "Üretim, Test ve Endüstriyel Uygulamalar"],
            "subcategories": [],
            "normalized_tags": ["propulsion", "energetics", "thermal_systems", "high_temperature_materials", "aeronautical_mechanics"],
            "category_scores": {},
            "category_evidence": [bi("Official AME majors and programme description.", "Resmî AME ana dalları ve program açıklaması.")],
        },
        "application_timeline_profile": {
            "academic_year": "2026/2027 reference cycle",
            "intake_terms": ["Autumn"],
            "application_rounds": ["2025-11-17", "2026-01-12", "2026-03-02", "2026-05-04"],
            "non_eu_deadline": "2026-05-04 (last published freemover round; closed when checked)",
            "eu_deadline": "2026-05-04 (last published freemover round; closed when checked)",
            "timeline_risk": "high",
            "deadline_notes": bi("All published freemover rounds for the checked cycle are closed; do not reuse the dates for the next intake.", "Kontrol edilen dönem için yayımlanmış tüm bağımsız başvuru turları kapalıdır; tarihler sonraki alım için yeniden kullanılmamalıdır."),
        },
        "source_profile": {
            "official_program_page": programme,
            "official_admission_page": admission,
            "official_tuition_page": admission,
            "official_scholarship_page": admission,
            "official_curriculum_page": programme,
            "official_housing_page": housing,
            "source_log": [
                source(programme, "ISAE-ENSMA International MSc AME", "official_program_page", ["program", "language", "curriculum"], "Official presentation confirms the active two-year English programme, two majors, internship and thesis.", "Resmî tanıtım aktif iki yıllık İngilizce programı, iki ana dalı, stajı ve tezi doğrular."),
                source(admission, "ISAE-ENSMA MSc AME admission", "official_admission_page", ["admission", "non_eu_eligibility", "language", "deadline"], "Official page lists eligible backgrounds, English tests, freemover rounds and non-European applicants.", "Resmî sayfa uygun altyapıları, İngilizce sınavlarını, bağımsız başvuru turlarını ve AB dışı adayları listeler."),
                source(admission, "ISAE-ENSMA MSc AME tuition", "official_tuition_page", ["tuition"], "Official page publishes EUR 7,000/year for non-European students and warns of annual re-evaluation.", "Resmî sayfa AB dışı öğrenciler için yıllık 7.000 EUR yayımlar ve yıllık yeniden değerlendirme uyarısı yapar."),
                source(admission, "ISAE-ENSMA MSc AME scholarship routes", "official_scholarship_page", ["scholarship", "funding"], "Official page names Eiffel and Campus France routes; awards remain competitive and call-specific.", "Resmî sayfa Eiffel ve Campus France yollarını belirtir; ödüller rekabetçi ve çağrıya özgüdür."),
                source(programme, "ISAE-ENSMA MSc AME curriculum", "official_curriculum_page", ["curriculum", "tracks", "thesis"], "Official page directly identifies EPROP and HTM and the graduation internship/thesis.", "Resmî sayfa EPROP ve HTM ile mezuniyet stajı/tezini doğrudan tanımlar."),
                source(housing, "University of Poitiers CROUS accommodation 2026/27", "official_housing_page", ["housing", "living"], "Official PDF gives exact monthly rents and states allocation is subject to availability.", "Resmî PDF kesin aylık kiraları verir ve tahsisin bulunabilirliğe bağlı olduğunu belirtir.", access_status="pdf"),
            ],
            "last_verified": CHECKED,
            "verification_notes": bi("Programme status and critical decision fields are official; ECTS total and future-cycle deadlines remain unverified.", "Program durumu ve kritik karar alanları resmîdir; toplam AKTS ve gelecek dönem tarihleri doğrulanmamıştır."),
            "field_confidence": {"program_basic_info": "high", "language": "high", "admission": "high", "tuition": "high", "scholarship": "high", "curriculum": "high", "research": "unknown", "industry": "unknown", "living": "high", "student_sentiment": "unknown"},
        },
        "decision_summary": {
            "overall_recommendation": "strong",
            "main_strengths": bi("Highly focused English programme for propulsion/energetics or high-temperature materials, with an internship and thesis.", "İtki/enerjetik veya yüksek sıcaklık malzemelerine odaklanan; staj ve tez içeren güçlü İngilizce program."),
            "main_risks": bi("Published application rounds are closed, fees may be re-evaluated annually, and the programme is narrower than a broad aerospace-systems MSc.", "Yayımlanmış başvuru turları kapalıdır, ücretler yıllık değişebilir ve program geniş bir havacılık-uzay sistemleri MSc'sinden daha dardır."),
            "best_for": bi("Applicants targeting propulsion, thermal sciences or high-temperature aerospace materials.", "İtki, termal bilimler veya yüksek sıcaklık havacılık-uzay malzemelerini hedefleyen adaylar."),
            "not_ideal_for": bi("Applicants primarily seeking spacecraft GNC, orbital mechanics or a broad aircraft-design curriculum.", "Öncelikle uzay aracı GNC, yörünge mekaniği veya geniş uçak tasarımı müfredatı arayan adaylar."),
            "application_reality": bi("Academically open to several engineering/science backgrounds, but the next application cycle must be checked before planning.", "Çeşitli mühendislik/bilim altyapılarına akademik olarak açık; ancak planlamadan önce sonraki başvuru dönemi kontrol edilmelidir."),
        },
        **common_profiles(),
    }
    return finalise(record)


def lulea() -> dict[str, Any]:
    programme = "https://www.ltu.se/en/education/programme/tmrra-master-programme-in-space-science-and-technology"
    tuition = "https://www.ltu.se/en/education/tuition-and-application-fees"
    scholarship = "https://www.ltu.se/en/education/scholarship-opportunities"
    living = "https://www.ltu.se/en/education/exchange-studies/practical-guide-for-exchange-students"
    housing = "https://www.ltu.se/en/student-web/student-life/housing-tips"
    record: dict[str, Any] = {
        "id": "se-ltu-spacemaster-msc",
        "country": "Sweden",
        "university": "Luleå University of Technology",
        "university_native_name": "Luleå tekniska universitet",
        "city": "Kiruna",
        "region": "Norrbotten",
        "program_name": "Master Programme in Space Science and Technology (SpaceMaster)",
        "program_native_name": "Rymdvetenskap och rymdteknik — SpaceMaster",
        "program_degree": "MSc",
        "degree_level": "Master",
        "degree_class": "Joint double-degree Master's programme",
        "duration_years": 2,
        "ects": 120,
        "teaching_language": ["English"],
        "program_url": programme,
        "department": "Space Campus Kiruna",
        "campus": "Kiruna",
        "program_status": "active",
        "relevance_status": "strong",
        "eligibility_profile": {
            "eligible_for_non_eu": True,
            "required_previous_degree": bi("At least 180 higher-education credits in one of the published physics, space, engineering, robotics, electronics, communications or control fields, including at least 22.5 university credits in mathematics.", "Yayımlanan fizik, uzay, mühendislik, robotik, elektronik, haberleşme veya kontrol alanlarından birinde en az 180 yükseköğretim kredisi ve üniversite düzeyinde en az 22,5 matematik kredisi."),
            "accepted_backgrounds": ["Space/aerospace engineering", "Mechanical/electrical engineering", "Physics/space science", "Robotics/automation/control", "Communications/electronics/mechatronics"],
            "required_ects": {"mathematics": 22.5, "previous_degree_total": 180},
            "minimum_gpa": None,
            "ranking_or_selection": "academic qualifications; quality and quantity aspects",
            "admission_mode": "national application portal and academic selection",
            "admission_risk": "high",
            "required_documents": [],
        },
        "language_profile": {"teaching_language": ["English"], "english_required": True, "english_level_required": "English 6 / level 2 equivalent", "accepted_english_tests": [], "mixed_language_warning": "", "language_risk": "low"},
        "cost_profile": {
            "academic_year": "current fee list checked 2026-07-19",
            "tuition_eur_per_year_min": None,
            "tuition_eur_per_year_max": None,
            "tuition_eur_per_year_estimated": None,
            "tuition_sek_per_term": 70000,
            "tuition_sek_per_year": 140000,
            "tuition_non_eu_full_program": {"amount": 280000, "currency": "SEK", "basis": "four semesters at the published current rate"},
            "tuition_basis": "non-EU/EEA/Swiss fee-paying students; current fee per semester",
            "application_fee_eur": None,
            "source_notes": bi("LTU publishes SEK 70,000/semester; no EUR conversion is stored.", "LTU dönem başına 70.000 SEK yayımlar; EUR dönüşümü kaydedilmez."),
        },
        "scholarship_profile": {
            "regional_scholarship_available": True,
            "regional_scholarship_name": "LTU current-Master tuition waiver and Swedish Institute routes",
            "merit_scholarships": ["LTU partial/full tuition waiver for one forthcoming semester after first-year performance", "Swedish Institute Scholarship for Global Professionals (country-specific)"],
            "tuition_waivers": ["Second-year LTU waiver: full or partial for one semester, merit/progress based"],
            "non_eu_eligible": True,
            "scholarship_deadline": "Eligible current students are contacted in early May; SI has a separate annual call",
            "scholarship_application_url": scholarship,
            "funding_competitiveness": "high",
            "funding_notes": bi("LTU does not publish a general first-year SpaceMaster award; the university waiver is for current Master's students and covers at most one forthcoming semester.", "LTU genel bir birinci yıl SpaceMaster bursu yayımlamaz; üniversite muafiyeti mevcut yüksek lisans öğrencileri içindir ve en fazla sonraki bir dönemi kapsar."),
        },
        "living_profile": {
            "city_cost_level": "unknown",
            "monthly_living_cost_sek_per_month_min": 10000,
            "monthly_living_cost_sek_per_month_max": 10000,
            "average_room_rent_sek_per_month_min": 4000,
            "average_room_rent_sek_per_month_max": 4000,
            "housing_difficulty": "unknown",
            "student_housing_available": True,
            "living_risk": "medium",
            "housing_notes": bi("LTU's official exchange guide gives a sample Sweden budget of about SEK 10,000/month including SEK 4,000 accommodation. This is planning guidance, not a Kiruna rent guarantee; LTU points Kiruna students to Kirunabostäder.", "LTU'nun resmî değişim rehberi konaklama için 4.000 SEK dahil yaklaşık aylık 10.000 SEK İsveç örnek bütçesi verir. Bu Kiruna kira garantisi değil planlama rehberidir; LTU Kiruna öğrencilerini Kirunabostäder'e yönlendirir."),
        },
        "curriculum_profile": {
            "tracks": ["Space Technology and Instrumentation", "Atmospheric and Space Science"],
            "specializations": ["Space Robotics and Automation", "Space Technology", "Dynamics and Control of Systems and Structures", "Space Automation and Control", "Space Technique and Instrumentation", "Astrophysics, Space Science and Planetology"],
            "mandatory_courses": ["Space Communication", "Spacecraft Systems", "Space Physics", "Master Degree Project"],
            "elective_courses": [],
            "thesis_required": True,
            "internship_required": None,
            "mobility_options": ["Second year at consortium partner university"],
            "double_degree_options": ["LTU degree plus one partner-university degree"],
            "curriculum_url": programme,
        },
        "category_profile": {
            "primary_categories": ["Uzay Sistemleri ve Astronotik", "Uçuş Mekaniği, Kontrol ve Otonomi"],
            "secondary_categories": ["Aviyonik, Yazılım ve Sayısal Teknolojiler", "Sistem Mühendisliği, Tasarım ve Optimizasyon"],
            "subcategories": [],
            "normalized_tags": ["space_systems", "spacecraft_gnc", "space_robotics", "space_instrumentation", "satellite_communications", "space_physics"],
            "category_scores": {},
            "category_evidence": [bi("Official 2027 programme specialisations and course list.", "Resmî 2027 program uzmanlıkları ve ders listesi.")],
        },
        "application_timeline_profile": {
            "academic_year": "2027/2028",
            "intake_terms": ["Autumn 2027"],
            "application_rounds": ["Application opens 2026-10-16"],
            "non_eu_deadline": "2027-01-15",
            "eu_deadline": "2027-01-15",
            "timeline_risk": "medium",
            "deadline_notes": bi("The published date is for the 30 August 2027 start and application code LTU-97406.", "Yayımlanan tarih 30 Ağustos 2027 başlangıcı ve LTU-97406 başvuru kodu içindir."),
        },
        "source_profile": {
            "official_program_page": programme,
            "official_admission_page": programme,
            "official_tuition_page": tuition,
            "official_scholarship_page": scholarship,
            "official_curriculum_page": programme,
            "official_housing_page": housing,
            "source_log": [
                source(programme, "LTU SpaceMaster — Autumn 2027", "official_program_page", ["program", "language", "curriculum", "deadline"], "Current official page confirms 120 credits, two years, English, Kiruna first year and consortium specialisations.", "Güncel resmî sayfa 120 kredi, iki yıl, İngilizce, Kiruna'daki ilk yıl ve konsorsiyum uzmanlıklarını doğrular."),
                source(programme, "LTU SpaceMaster entry requirements", "official_admission_page", ["admission", "non_eu_eligibility", "language", "deadline"], "Programme page publishes the 2027 application code, deadline, backgrounds and mathematics requirement.", "Program sayfası 2027 başvuru kodunu, son tarihi, altyapıları ve matematik koşulunu yayımlar."),
                source(tuition, "LTU tuition and application fees", "official_tuition_page", ["tuition"], "Current LTU list gives Space Science & Technology at SEK 70,000 per semester.", "Güncel LTU listesi Space Science & Technology için dönem başına 70.000 SEK verir."),
                source(scholarship, "LTU scholarship opportunities", "official_scholarship_page", ["scholarship", "funding"], "Updated page distinguishes the current-student waiver from first-year and SI routes.", "Güncel sayfa mevcut öğrenci muafiyetini birinci yıl ve SI yollarından ayırır."),
                source(programme, "LTU SpaceMaster curriculum and mobility", "official_curriculum_page", ["curriculum", "tracks", "courses", "thesis"], "Programme page publishes tracks, partner profiles and core space-engineering courses.", "Program sayfası izleri, ortak profilleri ve çekirdek uzay mühendisliği derslerini yayımlar."),
                source(living, "LTU practical guide sample living budget", "official_cost_of_living_page", ["housing", "living"], "Official planning example is Sweden-wide and is not presented as a guaranteed Kiruna price.", "Resmî planlama örneği İsveç geneline aittir ve garantili Kiruna fiyatı olarak sunulmaz."),
                source(housing, "LTU housing tips — Kiruna", "official_housing_page", ["housing"], "Official page directs Kiruna students to the named housing provider without promising availability.", "Resmî sayfa bulunabilirlik sözü vermeden Kiruna öğrencilerini belirtilen konut sağlayıcısına yönlendirir."),
            ],
            "last_verified": CHECKED,
            "verification_notes": bi("Critical programme fields are current for the 2027 intake; consortium mobility makes second-year location and costs profile-dependent.", "Kritik program alanları 2027 alımı için günceldir; konsorsiyum hareketliliği ikinci yıl konumunu ve maliyetini profile bağlı kılar."),
            "field_confidence": {"program_basic_info": "high", "language": "high", "admission": "high", "tuition": "high", "scholarship": "high", "curriculum": "high", "research": "medium", "industry": "medium", "living": "medium", "student_sentiment": "unknown"},
        },
        "decision_summary": {
            "overall_recommendation": "strong",
            "main_strengths": bi("Direct, English, double-degree space programme with spacecraft systems, communications, instrumentation, control and partner-university specialisations.", "Uzay aracı sistemleri, haberleşme, enstrümantasyon, kontrol ve ortak üniversite uzmanlıkları sunan doğrudan, İngilizce, çift diplomalı uzay programı."),
            "main_risks": bi("Second-year country and costs vary by profile; first-year LTU funding is limited and Kiruna housing requires separate planning.", "İkinci yıl ülkesi ve maliyetleri profile göre değişir; birinci yıl LTU finansmanı sınırlıdır ve Kiruna konutu ayrı planlama gerektirir."),
            "best_for": bi("Applicants seeking space systems plus international mobility, controls, instrumentation or space science.", "Uzay sistemleriyle birlikte uluslararası hareketlilik, kontrol, enstrümantasyon veya uzay bilimi arayan adaylar."),
            "not_ideal_for": bi("Applicants who need a single-campus programme or guaranteed first-year tuition support.", "Tek kampüslü program ya da garanti birinci yıl öğrenim desteği gereken adaylar."),
            "application_reality": bi("Entry is broad but quantitatively explicit; 22.5 university credits in mathematics are required and selection is competitive.", "Giriş alanları geniştir fakat nicel koşul açıktır; üniversite düzeyinde 22,5 matematik kredisi gerekir ve seçim rekabetçidir."),
        },
        **common_profiles(),
    }
    record["research_profile"].update({"research_centers": ["Space Campus Kiruna"], "research_strength_summary": bi("Programme access is tied to Kiruna space research infrastructure and consortium partners.", "Program erişimi Kiruna uzay araştırma altyapısı ve konsorsiyum ortaklarıyla bağlantılıdır."), "research_sources": [programme]})
    record["industry_ecosystem_profile"].update({"confirmed_partners": ["Swedish Institute of Space Physics (IRF)", "EISCAT AB", "Swedish Space Corporation (SSC)"], "research_institutes": ["IRF", "EISCAT"], "internship_possibility": "summer research internship opportunities are described; placement is not guaranteed", "career_relevance": bi("Official programme material identifies collaboration with major Kiruna space actors.", "Resmî program materyali Kiruna'daki başlıca uzay aktörleriyle işbirliğini tanımlar.")})
    return finalise(record)


def aalto() -> dict[str, Any]:
    programme = "https://www.aalto.fi/en/study-options/electronics-and-nanotechnology-master-of-science-technology"
    living = "https://www.aalto.fi/en/international-students/moving-to-finland-and-financial-matters"
    housing = "https://www.aalto.fi/en/services/housing-for-students"
    record: dict[str, Any] = {
        "id": "fi-aalto-electronics-nanotechnology-space-major-msc",
        "country": "Finland",
        "university": "Aalto University",
        "university_native_name": "Aalto-yliopisto",
        "city": "Espoo",
        "region": "Uusimaa",
        "program_name": "Electronics and Nanotechnology MSc — Space Science and Technology major",
        "program_native_name": "Master's Programme in Electronics and Nanotechnology — Space Science and Technology",
        "program_degree": "MSc (Technology)",
        "degree_level": "Master",
        "degree_class": "Master of Science (Technology)",
        "duration_years": 2,
        "ects": 120,
        "teaching_language": ["English"],
        "program_url": programme,
        "department": "Department of Electronics and Nanoengineering",
        "faculty_or_school": "School of Electrical Engineering",
        "campus": "Otaniemi",
        "program_status": "active",
        "relevance_status": "strong",
        "eligibility_profile": {
            "eligible_for_non_eu": True,
            "required_previous_degree": bi("A high-quality Bachelor's degree in electrical engineering, physics or a related field; other engineering, natural-science, mathematics or information-systems backgrounds may be considered if sufficient knowledge is shown.", "Elektrik mühendisliği, fizik veya ilgili alanda güçlü bir lisans; yeterli bilgi gösterilirse diğer mühendislik, doğa bilimleri, matematik veya bilgi sistemleri altyapıları değerlendirilebilir."),
            "accepted_backgrounds": ["Electrical engineering", "Physics", "Related engineering", "Natural sciences", "Mathematics", "Information systems with sufficient prerequisites"],
            "minimum_gpa": None,
            "ranking_or_selection": "competitive holistic evaluation of relevance, grades, institution quality and suitability",
            "admission_mode": "ranked application review",
            "admission_risk": "high",
            "required_documents": ["Degree certificate", "Transcripts", "Motivation letter", "CV"],
            "motivation_letter_required": True,
            "cv_required": True,
        },
        "language_profile": {"teaching_language": ["English"], "english_required": True, "english_level_required": "Aalto general Master's language requirements; programme page does not restate test thresholds", "accepted_english_tests": [], "mixed_language_warning": "", "language_risk": "medium"},
        "cost_profile": {"academic_year": "rights to study beginning on or after 2025-08-01", "tuition_eur_per_year_min": 17000, "tuition_eur_per_year_max": 17000, "tuition_eur_per_year_estimated": 17000, "tuition_basis": "non-EU/EEA/Swiss citizens in an English-taught technology Master's programme", "application_fee_eur": None, "source_notes": bi("Programme-specific annual tuition is published directly by Aalto.", "Programa özgü yıllık öğrenim ücreti Aalto tarafından doğrudan yayımlanır.")},
        "scholarship_profile": {"regional_scholarship_available": True, "regional_scholarship_name": "Aalto tuition-fee waiver scholarships", "merit_scholarships": ["A limited number of tuition-fee waivers for the highest-achieving fee-paying applicants"], "tuition_waivers": ["Aalto tuition-fee waiver"], "housing_support": False, "cash_grant_possible": False, "non_eu_eligible": True, "income_based": False, "scholarship_deadline": "Same application process; verify the next intake", "scholarship_application_url": programme, "funding_competitiveness": "high", "funding_notes": bi("Aalto describes a small number of waivers and explicitly does not promise living-cost funding.", "Aalto az sayıda muafiyet tanımlar ve yaşam gideri finansmanı vaat etmez.")},
        "living_profile": {"city_cost_level": "high", "monthly_living_cost_eur_min": 800, "monthly_living_cost_eur_max": 1300, "monthly_living_cost_eur_estimated": None, "housing_difficulty": "high", "student_housing_available": True, "average_room_rent_eur_min": 300, "average_room_rent_eur_max": 500, "living_risk": "high", "housing_notes": bi("Aalto's March 2026 budget gives EUR 800–1,300+ per month and EUR 300–500 for student housing. Aalto does not own dormitories, and HOAS/AYY cannot guarantee housing for every student.", "Aalto'nun Mart 2026 bütçesi aylık 800–1.300+ EUR ve öğrenci konutu için 300–500 EUR verir. Aalto yurt sahibi değildir; HOAS/AYY her öğrenciye konut garanti edemez.")},
        "curriculum_profile": {"tracks": ["Space Science and Technology major"], "specializations": ["Space technology", "Earth observation", "Space physics", "Radio astronomy"], "mandatory_courses": [], "elective_courses": [], "thesis_required": True, "internship_required": False, "project_based_courses": [], "curriculum_url": programme, "course_language_notes": bi("The degree includes 65 ECTS major studies, 25 ECTS electives and a 30 ECTS thesis.", "Derece 65 AKTS ana dal, 25 AKTS seçmeli ve 30 AKTS tez içerir.")},
        "category_profile": {"primary_categories": ["Uzay Sistemleri ve Astronotik", "Aviyonik, Yazılım ve Sayısal Teknolojiler"], "secondary_categories": ["Sistem Mühendisliği, Tasarım ve Optimizasyon"], "subcategories": [], "normalized_tags": ["space_systems", "earth_observation", "space_instrumentation", "space_physics", "radio_astronomy", "remote_sensing"], "category_scores": {}, "category_evidence": [bi("Official major description lists satellite systems, instruments, Earth observation and space-weather analysis.", "Resmî ana dal açıklaması uydu sistemleri, enstrümanlar, Dünya gözlemi ve uzay hava analizi listeler.")]},
        "application_timeline_profile": {"academic_year": "2026/2027 reference", "intake_terms": ["Autumn 2026"], "application_rounds": ["Continuous application 2026-04-11 to 2026-05-28"], "non_eu_deadline": "2026-05-28 (closed reference; next intake not yet verified)", "eu_deadline": "2026-05-28 (closed reference; next intake not yet verified)", "timeline_risk": "high", "deadline_notes": bi("The checked page shows a closed continuous-admission period for autumn 2026. Do not infer the 2027 dates.", "Kontrol edilen sayfa 2026 güz dönemi için kapanmış sürekli başvuru aralığını gösterir. 2027 tarihleri çıkarılmamalıdır.")},
        "source_profile": {
            "official_program_page": programme, "official_admission_page": programme, "official_tuition_page": programme, "official_scholarship_page": programme, "official_curriculum_page": programme, "official_department_page": programme, "official_housing_page": housing,
            "source_log": [
                source(programme, "Aalto Electronics and Nanotechnology MSc — Space Science and Technology major", "official_program_page", ["program", "language", "curriculum", "deadline"], "Current page confirms the active English 120-ECTS programme and the Space Science and Technology major.", "Güncel sayfa aktif İngilizce 120 AKTS programı ve Space Science and Technology ana dalını doğrular."),
                source(programme, "Aalto Electronics and Nanotechnology admissions criteria", "official_admission_page", ["admission", "non_eu_eligibility", "deadline"], "Programme page publishes eligible backgrounds, evaluated documents, selection criteria and the checked application period.", "Program sayfası uygun altyapıları, değerlendirilen belgeleri, seçim ölçütlerini ve kontrol edilen başvuru aralığını yayımlar."),
                source(programme, "Aalto Electronics and Nanotechnology tuition", "official_tuition_page", ["tuition"], "Programme page publishes EUR 17,000/year for non-EU/EEA citizens.", "Program sayfası AB/AEA dışı vatandaşlar için yıllık 17.000 EUR yayımlar."),
                source(programme, "Aalto tuition-waiver scholarships", "official_scholarship_page", ["scholarship", "funding"], "Programme page states that only a small number of highest-achieving fee-paying applicants receive waivers.", "Program sayfası yalnızca en başarılı ücret yükümlüsü adaylardan az sayıda kişiye muafiyet verildiğini belirtir."),
                source(programme, "Aalto Space Science and Technology major curriculum", "official_curriculum_page", ["curriculum", "tracks", "thesis"], "Official major description gives four focus areas and the 65+25+30 ECTS structure.", "Resmî ana dal açıklaması dört odak alanını ve 65+25+30 AKTS yapısını verir."),
                source(programme, "Aalto Department of Electronics and Nanoengineering research", "official_department_page", ["research", "department"], "The official programme page identifies department research in space technology and related radio/electromagnetics fields.", "Resmî program sayfası bölüm araştırmalarında uzay teknolojisi ile ilgili radyo/elektromanyetik alanları tanımlar.", confidence="medium"),
                source(living, "Aalto monthly living expenses", "official_cost_of_living_page", ["housing", "living"], "March 2026 official student guide publishes a EUR 800–1,300+ total and component ranges.", "Mart 2026 resmî öğrenci rehberi toplam 800–1.300+ EUR ve bileşen aralıklarını yayımlar."),
                source(housing, "Aalto housing for students", "official_housing_page", ["housing"], "Official page states that housing is arranged through HOAS/AYY and cannot be guaranteed to all applicants.", "Resmî sayfa konutun HOAS/AYY üzerinden ayarlandığını ve tüm adaylara garanti edilemediğini belirtir."),
            ],
            "last_verified": CHECKED,
            "verification_notes": bi("The database record represents the separately applied-to Aalto MSc and its Space Science and Technology major, not a duplicate record for the joint SpaceMaster route.", "Veritabanı kaydı ortak SpaceMaster yolunun kopyası değil, ayrı başvurulan Aalto MSc ve içindeki Space Science and Technology ana dalıdır."),
            "field_confidence": {"program_basic_info": "high", "language": "high", "admission": "high", "tuition": "high", "scholarship": "high", "curriculum": "high", "research": "medium", "industry": "medium", "living": "high", "student_sentiment": "unknown"},
        },
        "decision_summary": {"overall_recommendation": "strong", "main_strengths": bi("A direct English space major combining satellite systems, instruments, Earth observation, space physics and radio astronomy within a flexible technology MSc.", "Esnek bir teknoloji MSc'si içinde uydu sistemleri, enstrümanlar, Dünya gözlemi, uzay fiziği ve radyo astronomiyi birleştiren doğrudan İngilizce uzay ana dalı."), "main_risks": bi("High non-EU tuition, very limited waivers, competitive holistic admission and no verified future-cycle deadline yet.", "Yüksek AB dışı ücret, çok sınırlı muafiyet, rekabetçi bütünsel kabul ve henüz doğrulanmamış gelecek dönem son tarihi."), "best_for": bi("Applicants interested in satellites, remote sensing, space instruments or space science with strong electronics/physics foundations.", "Güçlü elektronik/fizik altyapısıyla uydular, uzaktan algılama, uzay enstrümanları veya uzay bilimine ilgi duyan adaylar."), "not_ideal_for": bi("Applicants seeking a broad aircraft-aerodynamics/propulsion MSc or guaranteed funding.", "Geniş uçak aerodinamiği/itki MSc'si ya da garanti finansman arayan adaylar."), "application_reality": bi("Strong grades and a clearly justified major choice matter; the checked 2026 application window is already closed.", "Güçlü notlar ve açıkça gerekçelendirilmiş ana dal tercihi önemlidir; kontrol edilen 2026 başvuru aralığı kapanmıştır.")},
        **common_profiles(),
    }
    record["research_profile"].update({"department_research_areas": ["Space technology", "Electromagnetics", "Radio engineering"], "research_centers": ["Metsähovi Radio Observatory"], "research_strength_summary": bi("The major is tied to Aalto research in space technology, radio engineering and Earth observation.", "Ana dal Aalto'nun uzay teknolojisi, radyo mühendisliği ve Dünya gözlemi araştırmalarına bağlıdır."), "research_sources": [programme]})
    record["industry_ecosystem_profile"].update({"internship_possibility": "possible, but no placement is guaranteed", "thesis_with_industry_possibility": "programme-wide page states that about half of theses are written for a company; not guaranteed for the space major", "career_relevance": bi("Official material describes projects, guest lectures and company theses but does not identify formal space-company partners for every student.", "Resmî materyal projeleri, konuk dersleri ve şirket tezlerini açıklar; her öğrenci için resmî uzay şirketi ortaklığı tanımlamaz.")})
    return finalise(record)


def load(path: Path) -> tuple[str, Any]:
    raw = path.read_text(encoding="utf-8")
    return raw, json.loads(raw)


def save(path: Path, original: str | None, payload: Any) -> None:
    newline = "\r\n" if original and "\r\n" in original else "\n"
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2).replace("\n", newline) + newline, encoding="utf-8")


def rows(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return payload
    return payload.get("programs", payload.get("universities", []))


def upsert(filename: str, record: dict[str, Any], country: str) -> None:
    path = DATA / filename
    if path.exists():
        original, payload = load(path)
    else:
        original, payload = None, {"country": country, "last_updated": CHECKED, "programs": []}
    target = rows(payload)
    target[:] = [item for item in target if item.get("id") != record["id"]]
    target.append(record)
    if isinstance(payload, dict):
        payload["last_updated"] = CHECKED
    save(path, original, payload)


def update_isae_supaero() -> None:
    path = DATA / "fransa.json"
    original, payload = load(path)
    row = next(item for item in rows(payload) if item.get("id") == "france_isae_supaero_msc")
    programme = "https://www.isae-supaero.fr/en/programmes/masters-degree-in-aerospace-engineering/"
    timeline = row.setdefault("application_timeline_profile", {})
    timeline.update({
        "academic_year": "2027/2028 next cycle notice",
        "intake_terms": ["2027 intake — dates not yet published"],
        "non_eu_deadline": None,
        "eu_deadline": None,
        "timeline_risk": "high",
        "deadline_notes": bi(
            "The official page states that 2026 MAE applications are closed and that 2027 applications will open in October 2026. No new closing date was published when checked.",
            "Resmî sayfa 2026 MAE başvurularının kapalı olduğunu ve 2027 başvurularının Ekim 2026'da açılacağını belirtir. Kontrol tarihinde yeni kapanış tarihi yayımlanmamıştı.",
        ),
    })
    profile = row.setdefault("source_profile", {})
    log = profile.setdefault("source_log", [])
    log[:] = [item for item in log if not (isinstance(item, dict) and item.get("url") == programme and item.get("source_type") == "official_admission_page")]
    log.append(source(programme, "ISAE-SUPAERO MAE 2027 application notice", "official_admission_page", ["deadline", "admission"], "Official notice says the 2026 cycle is closed and the 2027 cycle opens in October 2026; it does not publish a closing date.", "Resmî duyuru 2026 döneminin kapalı ve 2027 döneminin Ekim 2026'da açılacağını söyler; kapanış tarihi yayımlamaz."))
    profile["official_admission_page"] = programme
    profile["last_verified"] = CHECKED
    profile.setdefault("field_confidence", {})["deadlines"] = "high"
    payload["last_updated"] = CHECKED
    quality = audit_record(row)
    row["data_quality"] = {**quality, "audited_at": CHECKED}
    qc = row.setdefault("quality_control", {})
    qc["checked_at"] = CHECKED
    qc["qc_status"] = "passed" if quality["status"] == "verified" else "needs_revision"
    qc["remaining_verification_tasks"] = [bi(f"Add checked official evidence for {field}.", f"{field} için kontrol edilmiş resmî kanıt ekleyin.") for field in quality["unverified_critical_fields"]]
    save(path, original, payload)


def main() -> None:
    upsert("ingiltere.json", surrey(), "United Kingdom")
    upsert("fransa.json", ensma(), "France")
    upsert("isvec.json", lulea(), "Sweden")
    upsert("finlandiya.json", aalto(), "Finland")
    update_isae_supaero()
    print("Added Surrey, ISAE-ENSMA, LTU SpaceMaster and Aalto Space Science; refreshed ISAE-SUPAERO timing.")


if __name__ == "__main__":
    main()
