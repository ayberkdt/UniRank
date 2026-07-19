"""Add source-grounded Czech, Greek, and Turkish aerospace programmes.

The records intentionally keep unsupported cost, funding, deadline, and
international-admission values unknown. Running the script repeatedly is safe.
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


def src(
    url: str,
    source_type: str,
    title: str,
    fields: list[str],
    en: str,
    tr: str,
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
        "notes": bi(en, tr),
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
            "Yeterince belgelenmiş programa özgü öğrenci örneklemi bulunmadığı için puan gösterilmiyor.",
        ),
        "student_sentiment_sources": [],
    }


def make_record(spec: dict[str, Any]) -> dict[str, Any]:
    sources = spec["sources"]
    source_by_type = {item["source_type"]: item["url"] for item in sources}
    languages = spec["languages"]
    language_known = bool(languages) and all(str(language).lower() != "unknown" for language in languages)
    english_only = languages == ["English"]
    non_eu = spec.get("non_eu")
    tuition = spec.get("tuition", {})
    scholarship = spec.get("scholarship", {})
    deadline = spec.get("deadline")
    confidence = {
        "program_basic_info": "high",
        "language": spec.get("language_confidence", "high"),
        "admission": spec.get("admission_confidence", "high" if spec.get("admission") else "unknown"),
        "tuition": spec.get("tuition_confidence", "high" if any(s["source_type"] == "official_tuition_page" for s in sources) else "unknown"),
        "scholarship": spec.get("scholarship_confidence", "high" if any(s["source_type"] == "official_scholarship_page" for s in sources) else "unknown"),
        "curriculum": spec.get("curriculum_confidence", "high"),
        "research": "high" if any(s["source_type"] in {"official_department_page", "official_lab_page"} for s in sources) else "unknown",
        "industry": "unknown",
        "living": "unknown",
        "student_sentiment": "unknown",
    }

    record: dict[str, Any] = {
        "id": spec["id"],
        "country": spec["country"],
        "university": spec["university"],
        "university_native_name": spec.get("university_native", spec["university"]),
        "city": spec["city"],
        "region": spec.get("region", ""),
        "program_name": spec["program"],
        "program_native_name": spec.get("program_native", spec["program"]),
        "program_degree": spec.get("degree", "MSc"),
        "degree_level": spec.get("degree_level", "Master"),
        "degree_class": spec.get("degree_class", "Postgraduate taught"),
        "duration_years": spec.get("duration_years"),
        "ects": spec.get("ects"),
        "teaching_language": languages,
        "program_url": spec["program_url"],
        "department": spec.get("department", ""),
        "campus": spec.get("campus", spec["city"]),
        "program_status": "active",
        "relevance_status": "strong",
        "eligibility_profile": {
            "eligible_for_non_eu": non_eu,
            "required_previous_degree": bi(spec.get("previous_en", "Unknown."), spec.get("previous_tr", "Bilinmiyor.")),
            "accepted_backgrounds": spec.get("backgrounds", []),
            "minimum_gpa": None,
            "admission_mode": spec.get("admission_mode", "unknown"),
            "admission_risk": spec.get("admission_risk", "unknown"),
            "required_documents": spec.get("documents", []),
            "verification_notes": bi(spec.get("eligibility_note_en", ""), spec.get("eligibility_note_tr", "")),
        },
        "language_profile": {
            "teaching_language": languages,
            "english_required": "English" in languages,
            "english_level_required": spec.get("english_level"),
            "accepted_english_tests": spec.get("english_tests", []),
            "mixed_language_warning": spec.get("language_warning", ""),
            "language_risk": spec.get("language_risk", "low" if english_only else "high" if language_known else "unknown"),
        },
        "cost_profile": {
            "academic_year": spec.get("academic_year", "current official page checked 2026-07-19"),
            "tuition_eur_per_year_min": tuition.get("eur_year"),
            "tuition_eur_per_year_max": tuition.get("eur_year"),
            "tuition_eur_per_year_estimated": tuition.get("eur_year"),
            **({"tuition_czk_per_year": tuition["czk_year"]} if "czk_year" in tuition else {}),
            **({"tuition_eur_total": tuition["eur_total"]} if "eur_total" in tuition else {}),
            **({"tuition_usd_per_year": tuition["usd_year"]} if "usd_year" in tuition else {}),
            **({"tuition_usd_per_semester": tuition["usd_semester"]} if "usd_semester" in tuition else {}),
            **({"tuition_try_per_year": tuition["try_year"]} if "try_year" in tuition else {}),
            "tuition_basis": tuition.get("basis", "unknown"),
            "application_fee_eur": tuition.get("application_fee_eur"),
            "source_notes": bi(tuition.get("note_en", "Official current tuition was not verified."), tuition.get("note_tr", "Güncel resmî öğrenim ücreti doğrulanamadı.")),
        },
        "scholarship_profile": {
            "regional_scholarship_available": scholarship.get("available"),
            "regional_scholarship_name": scholarship.get("name"),
            "merit_scholarships": scholarship.get("merit", []),
            "tuition_waivers": scholarship.get("waivers", []),
            "non_eu_eligible": scholarship.get("non_eu"),
            "scholarship_deadline": scholarship.get("deadline"),
            "scholarship_application_url": scholarship.get("url"),
            "funding_competitiveness": scholarship.get("competitiveness", "unknown"),
            "funding_notes": bi(scholarship.get("note_en", "No current programme-specific funding was verified."), scholarship.get("note_tr", "Güncel programa özgü finansman doğrulanamadı.")),
        },
        "living_profile": {
            "city_cost_level": "unknown",
            "monthly_living_cost_eur_min": None,
            "monthly_living_cost_eur_max": None,
            "monthly_living_cost_eur_estimated": None,
            "housing_difficulty": "unknown",
            "student_housing_available": None,
            "average_room_rent_eur_min": None,
            "average_room_rent_eur_max": None,
            "living_risk": "unknown",
            "housing_notes": bi("No current official housing budget was retained.", "Güncel resmî konut bütçesi kaydedilmedi."),
        },
        "curriculum_profile": {
            "tracks": spec.get("tracks", []),
            "specializations": spec.get("specializations", []),
            "mandatory_courses": spec.get("mandatory", []),
            "elective_courses": spec.get("electives", []),
            "thesis_required": spec.get("thesis_required", True),
            "internship_required": spec.get("internship_required"),
            "project_based_courses": spec.get("projects", []),
            "curriculum_url": spec["curriculum_url"],
            "course_language_notes": bi(spec.get("course_note_en", ""), spec.get("course_note_tr", "")),
        },
        "category_profile": {
            "primary_categories": spec.get("primary_categories", ["Aeronautical Engineering"]),
            "secondary_categories": spec.get("secondary_categories", []),
            "subcategories": [],
            "normalized_tags": spec["tags"],
            "category_scores": {},
            "category_evidence": [bi(spec["fit_en"], spec["fit_tr"])],
        },
        "research_profile": {
            "department_research_areas": spec.get("research_areas", []),
            "labs": [],
            "research_centers": [],
            "space_or_aerospace_projects": [],
            "research_strength_summary": bi(spec.get("research_en", ""), spec.get("research_tr", "")),
            "research_strength_score": None,
            "research_sources": [s["url"] for s in sources if s["source_type"] in {"official_department_page", "official_lab_page"}],
        },
        "industry_ecosystem_profile": {
            "nearby_companies": [],
            "confirmed_partners": [],
            "space_agencies_or_public_bodies": [],
            "research_institutes": [],
            "internship_possibility": "unknown",
            "thesis_with_industry_possibility": "unknown",
            "career_relevance": bi("No partnership claim was retained without direct confirmation.", "Doğrudan doğrulama olmadan ortaklık iddiası kaydedilmedi."),
            "ecosystem_strength_score": None,
            "ecosystem_notes": bi("Industry proximity is not treated as a university partnership.", "Sektörel yakınlık üniversite ortaklığı sayılmadı."),
        },
        "application_timeline_profile": {
            "academic_year": spec.get("academic_year", "unknown"),
            "intake_terms": spec.get("intakes", []),
            "application_rounds": spec.get("rounds", []),
            "non_eu_deadline": deadline,
            "eu_deadline": deadline,
            "timeline_risk": "low" if deadline else "high",
            "deadline_notes": bi(spec.get("deadline_note_en", "No current deadline was verified."), spec.get("deadline_note_tr", "Güncel son başvuru tarihi doğrulanamadı.")),
        },
        "student_sentiment_profile": empty_sentiment(),
        "source_profile": {
            "official_program_page": source_by_type.get("official_program_page", spec["program_url"]),
            "official_admission_page": source_by_type.get("official_admission_page"),
            "official_tuition_page": source_by_type.get("official_tuition_page"),
            "official_scholarship_page": source_by_type.get("official_scholarship_page"),
            "official_curriculum_page": source_by_type.get("official_curriculum_page", spec["curriculum_url"]),
            "official_department_page": source_by_type.get("official_department_page"),
            "source_log": sources,
            "last_verified": CHECKED,
            "verification_notes": bi(spec.get("verification_en", "Unknown fields remain explicit."), spec.get("verification_tr", "Bilinmeyen alanlar açık bırakıldı.")),
            "field_confidence": confidence,
            "needs_verification": True,
        },
        "decision_summary": {
            "overall_recommendation": spec.get("recommendation", "conditional"),
            "main_strengths": bi(spec["fit_en"], spec["fit_tr"]),
            "main_risks": bi(spec["risk_en"], spec["risk_tr"]),
            "best_for": bi(spec["best_en"], spec["best_tr"]),
            "not_ideal_for": bi(spec["not_en"], spec["not_tr"]),
            "verification_priority": bi(spec.get("priority_en", "Verify the next admission call and personal eligibility before applying."), spec.get("priority_tr", "Başvurmadan önce yeni ilanı ve kişisel uygunluğu doğrulayın.")),
        },
        "scoring_inputs": {
            "academic_field_fit_score_seed": None,
            "eligibility_language_score_seed": None,
            "cost_funding_score_seed": None,
            "career_research_score_seed": None,
            "living_risk_score_seed": None,
            "data_confidence_score_seed": None,
            "student_satisfaction_score_seed": None,
            "hard_filter_flags": {
                "english_only_compatible": english_only,
                "requires_local_language": language_known and not english_only,
                "non_eu_eligible": non_eu,
                "tuition_above_5000": (
                    (tuition.get("eur_year") or tuition.get("eur_total")) > 5000
                    if tuition.get("eur_year") is not None or tuition.get("eur_total") is not None
                    else None
                ),
                "tuition_above_10000": (
                    (tuition.get("eur_year") or tuition.get("eur_total")) > 10000
                    if tuition.get("eur_year") is not None or tuition.get("eur_total") is not None
                    else None
                ),
                "deadline_unclear": deadline is None,
                "needs_verification": True,
            },
        },
    }

    quality = audit_record(record)
    record["data_quality"] = {**quality, "audited_at": CHECKED}
    verified = quality["status"] == "verified"
    record["source_profile"]["needs_verification"] = not verified
    record["scoring_inputs"]["hard_filter_flags"]["needs_verification"] = not verified
    record["quality_control"] = {
        "qc_status": "passed" if verified else "needs_revision",
        "checked_at": CHECKED,
        "failed_canary_tests": (
            []
            if verified
            else ["missing_or_unverified_critical_fields"]
            if quality["unverified_critical_fields"]
            else ["non_high_critical_confidence"]
        ),
        "remaining_verification_tasks": [
            bi(f"Add current official evidence for {field}.", f"{field} için güncel resmî kanıt ekleyin.")
            for field in quality["unverified_critical_fields"]
        ] + (
            []
            if verified or quality["unverified_critical_fields"]
            else [bi("Recheck the medium-confidence critical evidence before applying.", "Başvurmadan önce orta güvenli kritik kanıtı yeniden kontrol edin.")]
        ),
        "qc_notes": bi(
            "Source audit completed; unsupported decision fields remain unknown and sentiment is not scored.",
            "Kaynak denetimi tamamlandı; desteklenmeyen karar alanları bilinmiyor olarak kaldı ve öğrenci görüşü puanlanmadı.",
        ),
    }
    return record


CTU_PROGRAM = "https://aerospace.fel.cvut.cz/overview"
CTU_ADMISSION = "https://aerospace.fel.cvut.cz/admissionAN"
CTU_CURRICULUM = "https://fel.cvut.cz/en/admissions/study-options/study-programs/study-plans/27346-aerospace-engineering-avionics"
CTU_TUITION = "https://fel.cvut.cz/en/admissions/admission-procedures/tuition-fees"
BUT_PROGRAM = "https://www.vut.cz/en/students/programmes/programme/9318"
BUT_JOIN = "https://www.vut.cz/en/study-options/join-but"
AUTH_PROFILE = "https://qa.auth.gr/en/pms/395"
AUTH_GUIDE = "https://qa.auth.gr/en/studyguide/600000726/2025"
AUTH_CALL = "https://career.auth.gr/wp-content/uploads/2026/04/%CE%A0%CF%81%CE%BF%CE%BA%CE%AE%CF%81%CF%85%CE%BE%CE%B7-%CE%94%CE%A0%CE%9C%CE%A3-UAV-2026-27-3.pdf"
PATRAS_PROGRAM = "https://mead-ata.upatras.gr/"
PATRAS_CALL = "https://mead-ata.upatras.gr/prokirixi-2026-2027/"
PATRAS_CURRICULUM = "https://mead-ata.upatras.gr/m%CE%B1%CE%B8%CE%AE%CE%BC%CE%B1%CF%84%CE%B1/"
STAR_PROGRAM = "https://star.uoa.gr/odhgos_spoudwn_english.php"
STAR_DEPT = "https://en.phys.uoa.gr/postgraduate_studies"
THK_ACTIVE = "https://sci.thk.edu.tr/storage/public/documents/tiny/78/2025-2026%20G%C3%BCz%20D%C3%B6nemi%20Havac%C4%B1l%C4%B1k%20ve%20Uzay%20M%C3%BCh.%20M%C3%BClakat%20Sonu%C3%A7lar%C4%B1.pdf"
ERU_SPACE = "https://uzm.erciyes.edu.tr/"
ERU_CALL = "https://fbe.erciyes.edu.tr/tr/duyuru-detay/fen-bilimleri-enstitusu-lisansustu-program-basvurusu-hakkinda"
NEU_PROGRAMS = "https://erbakan.edu.tr/tr/programlar"
NEU_BOLOGNA = "https://obs.erbakan.edu.tr/oibs/bologna/progAbout.aspx?curSunit=305000732&lang=tr"
NEU_CALL = "https://erbakan.edu.tr/tr/birim/fen-bilimleri-enstitusu/duyuru/fen-bilimleri-enstitusu-2026-2027-egitim-ogretim-yili-guz-yariyili-lisansustu-ogrenci-alim-ilani-27255"


SPECS: list[dict[str, Any]] = [
    {
        "id": "cz-ctu-aerospace-engineering-avionics-msc", "country": "Czechia",
        "university": "Czech Technical University in Prague", "university_native": "České vysoké učení technické v Praze",
        "city": "Prague", "program": "Aerospace Engineering — Avionics", "degree": "Ing.",
        "duration_years": 2, "ects": 120, "languages": ["English"], "program_url": CTU_PROGRAM,
        "department": "Faculty of Electrical Engineering", "curriculum_url": CTU_CURRICULUM,
        "non_eu": True, "previous_en": "A relevant bachelor's degree and sufficient technical preparation; admission includes a remote technical interview.",
        "previous_tr": "İlgili bir lisans derecesi ve yeterli teknik hazırlık; kabul sürecinde uzaktan teknik mülakat bulunur.",
        "backgrounds": ["Electrical/electronic engineering", "Mechanical/aerospace engineering", "Control, robotics or related engineering"],
        "admission": True, "admission_mode": "online technical entrance interview", "admission_risk": "medium",
        "english_level": "B2 recommended by CTU FEE/FME guidance", "tuition": {"czk_year": 132000, "basis": "English-taught Master's programme; per academic year", "note_en": "CTU FEE publishes CZK 132,000 per academic year.", "note_tr": "CTU FEE akademik yıl başına 132.000 CZK yayımlar."},
        "scholarship": {"available": True, "name": "CTU foreign-master and merit scholarships", "non_eu": True, "url": CTU_TUITION, "competitiveness": "high", "note_en": "The official tuition page links foreign-student and merit scholarships; award amounts and eligibility require the linked calls.", "note_tr": "Resmî ücret sayfası yabancı öğrenci ve başarı burslarına bağlantı verir; tutar ve uygunluk ilgili ilanlardan kontrol edilmelidir."},
        "deadline": "end of April (official page wording; exact 2027 date not yet verified)", "academic_year": "2026/2027 reference",
        "tracks": ["Avionics"], "mandatory": ["Aircraft Avionics", "Space Engineering", "Integrated Modular Avionics", "Flight Control Systems", "Aircraft Propulsion", "Aircraft Structures and Materials", "Diploma Thesis"],
        "tags": ["avionics", "flight_control", "space_engineering", "unmanned_systems", "aerospace_electronics"],
        "fit_en": "A direct English aerospace master's combining avionics, space engineering, flight control, radio systems and aircraft fundamentals.",
        "fit_tr": "Aviyonik, uzay mühendisliği, uçuş kontrolü, radyo sistemleri ve uçak temellerini birleştiren doğrudan İngilizce yüksek lisans.",
        "risk_en": "The official admission page gives an end-of-April rule but not a verified exact next-cycle date; tuition is in CZK and scholarships are competitive.",
        "risk_tr": "Resmî kabul sayfası nisan sonu kuralını verir ancak sonraki dönem için kesin tarih doğrulanmadı; ücret CZK cinsinden ve burslar rekabetçidir.",
        "best_en": "Applicants targeting avionics, embedded aerospace systems, GNC and flight-control integration.",
        "best_tr": "Aviyonik, gömülü havacılık sistemleri, GNC ve uçuş kontrol entegrasyonu hedefleyen adaylar.",
        "not_en": "Students seeking a propulsion- or structures-dominant mechanical programme.", "not_tr": "İtki veya yapı ağırlıklı mekanik bir program arayan öğrenciler.",
        "sources": [
            src(CTU_PROGRAM, "official_program_page", "CTU Aerospace Engineering overview", ["program", "language"], "Confirms the parallel English master's and its aerospace scope.", "İngilizce yüksek lisansı ve havacılık-uzay kapsamını doğrular."),
            src(CTU_ADMISSION, "official_admission_page", "CTU Aerospace Engineering admission", ["admission", "non_eu_eligibility", "deadline"], "Publishes the English-applicant process, technical interview and end-of-April rule.", "İngilizce aday sürecini, teknik mülakatı ve nisan sonu kuralını yayımlar."),
            src(CTU_CURRICULUM, "official_curriculum_page", "CTU Avionics study plan", ["curriculum"], "Current 120-credit plan lists four semesters and the diploma thesis.", "Güncel 120 kredilik plan dört yarıyılı ve diploma tezini listeler."),
            src(CTU_TUITION, "official_tuition_page", "CTU FEE tuition fees", ["tuition"], "Publishes the Master's tuition in CZK.", "Yüksek lisans ücretini CZK cinsinden yayımlar."),
            src(CTU_TUITION, "official_scholarship_page", "CTU FEE scholarship links", ["scholarship"], "Official fee page links foreign-student and merit scholarships.", "Resmî ücret sayfası yabancı öğrenci ve başarı burslarına bağlantı verir."),
        ],
    },
    {
        "id": "cz-but-aerospace-technology-msc", "country": "Czechia", "university": "Brno University of Technology",
        "university_native": "Vysoké učení technické v Brně", "city": "Brno", "program": "Aerospace Technology", "degree": "Ing.",
        "duration_years": 2, "ects": 120, "languages": ["English"], "program_url": BUT_PROGRAM,
        "department": "Faculty of Mechanical Engineering", "curriculum_url": BUT_PROGRAM, "non_eu": True,
        "previous_en": "A relevant bachelor's degree; faculty-specific admission requirements and any entrance assessment apply.",
        "previous_tr": "İlgili bir lisans derecesi; fakülteye özgü kabul şartları ve varsa giriş değerlendirmesi uygulanır.",
        "backgrounds": ["Mechanical engineering", "Aeronautical/aerospace engineering", "Related engineering"], "admission": True,
        "admission_mode": "faculty admission procedure", "admission_risk": "medium", "english_level": "B2; BUT FAQ indicates IELTS-equivalent 5.5–6.5",
        "tuition": {"eur_year": 3000, "basis": "EU and non-EU students, per academic year", "application_fee_eur": 28, "note_en": "The 2025/26 programme page publishes EUR 3,000/year for both EU and non-EU students.", "note_tr": "2025/26 program sayfası AB ve AB dışı öğrenciler için yıllık 3.000 EUR yayımlar."},
        "scholarship": {"available": True, "name": "BUT non-EU Master's tuition scholarship and university scholarships", "non_eu": True, "url": BUT_JOIN, "competitiveness": "high", "note_en": "BUT states that non-EU Master's applicants may apply for a scholarship covering half the tuition; selection is not guaranteed.", "note_tr": "BUT, AB dışı yüksek lisans adaylarının öğrenim ücretinin yarısını karşılayan bursa başvurabileceğini belirtir; burs garanti değildir."},
        "deadline": None, "academic_year": "2025/2026 programme data; next application dates not verified",
        "mandatory": ["Aerodynamics I–II", "Aircraft Materials and Technology", "Aircraft Propulsion", "Aircraft Structure", "CFD for Aerospace", "Autonomous Flying Systems", "Flight Mechanics"],
        "tags": ["aircraft_design", "aerodynamics", "cfd", "flight_mechanics", "structures", "propulsion"],
        "fit_en": "A direct English aircraft-design programme with strong aerodynamics, CFD, structures, propulsion and autonomous-flight coverage.",
        "fit_tr": "Aerodinamik, HAD, yapılar, itki ve otonom uçuş kapsamı güçlü doğrudan İngilizce uçak tasarımı programı.",
        "risk_en": "The programme page is current for 2025/26, while the next application deadline and faculty-level selection details still require confirmation.",
        "risk_tr": "Program sayfası 2025/26 için güncel; sonraki başvuru tarihi ve fakülte düzeyi seçim ayrıntıları yine doğrulanmalıdır.",
        "best_en": "Students focused on aircraft design, aerodynamics, CFD and structural engineering.", "best_tr": "Uçak tasarımı, aerodinamik, HAD ve yapı mühendisliğine odaklanan öğrenciler.",
        "not_en": "Applicants seeking a space-systems-first curriculum.", "not_tr": "Önceliği uzay sistemleri olan bir müfredat arayan adaylar.",
        "sources": [
            src(BUT_PROGRAM, "official_program_page", "BUT Aerospace Technology", ["program", "language", "curriculum"], "Confirms the active English two-year programme, fee and technical scope.", "Aktif İngilizce iki yıllık programı, ücreti ve teknik kapsamı doğrular."),
            src(BUT_PROGRAM, "official_curriculum_page", "BUT Aerospace Technology course plan", ["curriculum"], "Lists the English course structure with credits.", "İngilizce ders yapısını kredileriyle listeler."),
            src(BUT_PROGRAM, "official_tuition_page", "BUT Aerospace Technology tuition", ["tuition"], "Publishes EUR 3,000 per academic year for EU and non-EU students.", "AB ve AB dışı öğrenciler için akademik yıl başına 3.000 EUR yayımlar."),
            src(BUT_JOIN, "official_admission_page", "Join BUT admissions", ["admission", "non_eu_eligibility"], "Publishes the international application route and programme listing.", "Uluslararası başvuru yolunu ve program listesini yayımlar."),
            src(BUT_JOIN, "official_scholarship_page", "BUT scholarships for international Master's students", ["scholarship"], "States the half-tuition scholarship possibility for non-EU Master's applicants.", "AB dışı yüksek lisans adayları için yarım ücret bursu olasılığını belirtir."),
        ],
    },
    {
        "id": "gr-auth-aerial-autonomous-systems-msc", "country": "Greece", "university": "Aristotle University of Thessaloniki",
        "university_native": "Αριστοτέλειο Πανεπιστήμιο Θεσσαλονίκης", "city": "Thessaloniki", "program": "MSc in Aerial Autonomous Systems",
        "duration_years": 1.5, "ects": 90, "languages": ["English"], "program_url": AUTH_PROFILE,
        "department": "Electrical and Computer Engineering with Mechanical and Rural & Surveying Engineering", "curriculum_url": AUTH_GUIDE, "non_eu": True,
        "previous_en": "A relevant university degree; candidates are assessed on degree performance, relevant courses/thesis, research or professional activity and English at B2 or above.",
        "previous_tr": "İlgili bir üniversite derecesi; adaylar diploma başarısı, ilgili ders/tez, araştırma veya mesleki faaliyet ve en az B2 İngilizce üzerinden değerlendirilir.",
        "backgrounds": ["Engineering", "Computer/electrical engineering", "Mechanical engineering", "Surveying/geoinformatics and related fields"],
        "admission": True, "admission_mode": "document evaluation and programme selection", "admission_risk": "medium", "english_level": "B2 minimum",
        "tuition": {"eur_total": 9000, "basis": "total programme tuition for third-country citizens", "note_en": "The 2026/27 call publishes EUR 9,000 total for third-country citizens and EUR 6,000 for EU citizens.", "note_tr": "2026/27 ilanı üçüncü ülke vatandaşları için toplam 9.000 EUR, AB vatandaşları için 6.000 EUR yayımlar."},
        "scholarship": {"available": True, "name": "Three 50% tuition reductions for EU citizens", "non_eu": False, "url": AUTH_CALL, "competitiveness": "high", "note_en": "The call limits its three 50% tuition reductions to EU citizens; a Turkish non-EU applicant should not assume eligibility.", "note_tr": "İlan üç adet %50 ücret indirimini AB vatandaşlarıyla sınırlar; AB dışı Türk aday uygun olduğunu varsaymamalıdır."},
        "deadline": "2026-08-31", "academic_year": "2026/2027 call", "rounds": ["Applications accepted through 2026-08-31"],
        "deadline_note_en": "The 2026/27 call gives 31 August 2026, although one sentence inside the PDF inconsistently says 2025/26; the date is retained with this warning.",
        "deadline_note_tr": "2026/27 ilanı 31 Ağustos 2026 tarihini verir; PDF içindeki bir cümle tutarsız biçimde 2025/26 dediğinden tarih bu uyarıyla kaydedildi.",
        "mandatory": ["Sensor Systems for Autonomous Vehicles", "Advanced Aerodynamics", "Intelligent Robotic Systems", "GNSS and Inertial Positioning"],
        "tags": ["uav", "autonomous_systems", "gnss", "inertial_navigation", "robotics", "aerodynamics"],
        "fit_en": "An English interdisciplinary UAV master's combining aerodynamics, sensing, GNSS/inertial navigation, robotics, communications and structural design.",
        "fit_tr": "Aerodinamik, algılama, GNSS/ataletsel seyrüsefer, robotik, haberleşme ve yapısal tasarımı birleştiren İngilizce disiplinlerarası İHA yüksek lisansı.",
        "risk_en": "The focus is aerial autonomous systems rather than broad aircraft or spacecraft design; the next usable deadline must be checked in the live call.",
        "risk_tr": "Odak genel uçak veya uzay aracı tasarımı değil, hava otonom sistemleridir; kullanılabilir son tarih canlı ilandan kontrol edilmelidir.",
        "best_en": "Applicants targeting UAV autonomy, navigation, sensing, communications and control.", "best_tr": "İHA otonomisi, seyrüsefer, algılama, haberleşme ve kontrol hedefleyen adaylar.",
        "not_en": "Students seeking a conventional propulsion- or spacecraft-heavy aerospace degree.", "not_tr": "Klasik itki veya uzay aracı ağırlıklı havacılık-uzay derecesi arayan öğrenciler.",
        "sources": [
            src(AUTH_PROFILE, "official_program_page", "AUTH Aerial Autonomous Systems profile", ["program", "language"], "Confirms active status, English delivery, 90 ECTS, duration and tuition.", "Aktif durumu, İngilizce eğitimi, 90 AKTS'yi, süreyi ve ücreti doğrular."),
            src(AUTH_CALL, "official_admission_page", "AUTH Aerial Autonomous Systems 2026/27 call", ["admission", "non_eu_eligibility", "deadline"], "Official 2026/27 English-programme call confirms a live international application route.", "Resmî 2026/27 İngilizce program ilanı uluslararası başvuru yolunu doğrular.", access_status="pdf"),
            src(AUTH_GUIDE, "official_curriculum_page", "AUTH Aerial Autonomous Systems study guide", ["curriculum"], "Lists current courses including aerodynamics, robotics, sensing and navigation.", "Aerodinamik, robotik, algılama ve seyrüsefer dahil güncel dersleri listeler."),
            src(AUTH_CALL, "official_tuition_page", "AUTH Aerial Autonomous Systems tuition", ["tuition"], "The call publishes EUR 9,000 total for third-country citizens and EUR 6,000 for EU citizens.", "İlan üçüncü ülke vatandaşları için toplam 9.000 EUR, AB vatandaşları için 6.000 EUR yayımlar.", access_status="pdf"),
            src(AUTH_CALL, "official_scholarship_page", "AUTH Aerial Autonomous Systems tuition reductions", ["scholarship"], "The three 50% tuition reductions are explicitly limited to EU citizens.", "Üç adet %50 ücret indirimi açıkça AB vatandaşlarıyla sınırlıdır.", access_status="pdf"),
        ],
    },
    {
        "id": "gr-patras-advanced-technologies-aeronautics-msc", "country": "Greece", "university": "University of Patras",
        "university_native": "Πανεπιστήμιο Πατρών", "city": "Patras", "program": "Advanced Technologies in Aeronautics",
        "duration_years": 1.5, "ects": 90, "languages": ["Greek"], "program_url": PATRAS_PROGRAM,
        "department": "Department of Mechanical Engineering and Aeronautics with the Hellenic Air Force Academy", "curriculum_url": PATRAS_CURRICULUM,
        "non_eu": True, "previous_en": "Graduates of recognised domestic or foreign universities, prioritising engineering and related science backgrounds; the official call also lists science, economics and management graduates.",
        "previous_tr": "Tanınan yerli veya yabancı üniversite mezunları; öncelik mühendislik ve ilgili fen alanlarında, resmî ilan ayrıca fen, ekonomi ve yönetim mezunlarını listeler.",
        "backgrounds": ["Engineering", "Natural sciences", "Economics or management", "Military higher education"], "admission": True,
        "admission_mode": "document evaluation and interview", "admission_risk": "medium", "english_level": "B2 evidence required although instruction is Greek",
        "language_warning": "Teaching and thesis language is Greek; the thesis may be written in English.", "language_risk": "high",
        "tuition": {"eur_total": 4000, "basis": "total tuition for students from outside the EEA", "note_en": "The 2026/27 call publishes EUR 4,000 total for non-EEA students (EUR 2,400 for EEA students).", "note_tr": "2026/27 ilanı AEA dışı öğrenciler için toplam 4.000 EUR (AEA öğrencileri için 2.400 EUR) yayımlar."},
        "deadline": "2026-07-17", "academic_year": "2026/2027", "rounds": ["2026-05-11 to 2026-07-17 (extended call)"],
        "mandatory": ["Subsonic Aerodynamics", "Flight Mechanics and Control", "Aircraft Materials, Structures and Manufacturing", "Propulsion Systems", "Master's Thesis"],
        "electives": ["Aircraft Design", "Transonic and Supersonic Aerodynamics", "Aeroelasticity", "UAV Design", "Flight Control", "Aerospace Telecommunications"],
        "tags": ["aerodynamics", "flight_control", "structures", "propulsion", "uav", "aeroelasticity"],
        "fit_en": "A new, technically broad aeronautics MSc covering aerodynamics, flight control, structures, propulsion, UAVs and aerospace electronics.",
        "fit_tr": "Aerodinamik, uçuş kontrolü, yapılar, itki, İHA'lar ve havacılık elektroniğini kapsayan yeni ve teknik açıdan geniş yüksek lisans.",
        "risk_en": "Teaching is Greek, the programme starts for the first time in 2026/27, and non-EEA tuition is higher than the EEA rate.",
        "risk_tr": "Eğitim dili Yunancadır, program ilk kez 2026/27'de başlayacaktır ve AEA dışı ücret AEA ücretinden yüksektir.",
        "best_en": "Greek-capable applicants seeking a broad aeronautics curriculum with mixed online/on-campus delivery.", "best_tr": "Karma çevrimiçi/kampüs eğitimiyle geniş havacılık müfredatı arayan Yunanca bilen adaylar.",
        "not_en": "English-only students or applicants seeking a mature programme with established graduate outcomes.", "not_tr": "Yalnız İngilizce okuyabilenler veya oturmuş mezun çıktıları olan köklü program arayanlar.",
        "sources": [
            src(PATRAS_PROGRAM, "official_program_page", "Patras Advanced Technologies in Aeronautics", ["program", "language"], "Confirms the new programme and its 2026/27 launch.", "Yeni programı ve 2026/27 başlangıcını doğrular."),
            src(PATRAS_CALL, "official_admission_page", "Patras 2026/27 admission call", ["admission", "non_eu_eligibility", "deadline"], "Publishes eligible degrees, documents, interview selection and the extended deadline.", "Uygun dereceleri, belgeleri, mülakatlı seçimi ve uzatılmış tarihi yayımlar."),
            src(PATRAS_CURRICULUM, "official_curriculum_page", "Patras aeronautics curriculum", ["curriculum"], "Lists 90 ECTS across core courses, electives and thesis.", "Temel dersler, seçmeliler ve tezden oluşan 90 AKTS'yi listeler."),
            src(PATRAS_CALL, "official_tuition_page", "Patras aeronautics tuition", ["tuition"], "Publishes EUR 4,000 total for non-EEA students.", "AEA dışı öğrenciler için toplam 4.000 EUR yayımlar."),
        ],
    },
    {
        "id": "gr-nkua-star-space-technologies-msc", "country": "Greece", "university": "National and Kapodistrian University of Athens",
        "university_native": "Εθνικό και Καποδιστριακό Πανεπιστήμιο Αθηνών", "city": "Athens", "program": "Space Technologies, Applications and Services (STAR)",
        "duration_years": 2, "ects": 120, "languages": ["English"], "program_url": STAR_PROGRAM,
        "department": "Inter-institutional programme led by NKUA", "curriculum_url": STAR_PROGRAM, "non_eu": True,
        "previous_en": "A bachelor's degree from a recognised Greek or foreign university; the programme is mainly aimed at science and engineering graduates.",
        "previous_tr": "Tanınan bir Yunan veya yabancı üniversiteden lisans derecesi; program esas olarak fen ve mühendislik mezunlarına yöneliktir.",
        "backgrounds": ["Engineering", "Physics and natural sciences", "Computer science and telecommunications"], "admission": True,
        "admission_mode": "application review", "admission_risk": "medium", "english_level": "Required for English-taught courses; exact current test threshold not verified",
        "tuition": {}, "scholarship": {}, "deadline": None, "academic_year": "current programme guide checked 2026-07-19; next call not verified",
        "tracks": ["Space Technology — Space Upstream", "Space Applications and Services — Space Downstream"],
        "mandatory": ["Fundamentals of Space Missions", "Fundamentals of Satellite Systems and Subsystems", "Physics of the Space Environment", "Fundamentals of Space Applications and Services", "Master's Thesis"],
        "tags": ["space_systems", "satellites", "space_missions", "earth_observation", "navigation", "telecommunications"],
        "primary_categories": ["Space Systems and Astronautics"],
        "fit_en": "A direct English space MSc with upstream and downstream tracks, satellite systems, missions, space environment, Earth observation, navigation and communications.",
        "fit_tr": "Upstream/downstream yolları, uydu sistemleri, görevler, uzay ortamı, Dünya gözlemi, seyrüsefer ve haberleşme içeren doğrudan İngilizce uzay yüksek lisansı.",
        "risk_en": "The checked official guide does not provide a verified current tuition, scholarship call or next application deadline.",
        "risk_tr": "Kontrol edilen resmî rehber güncel doğrulanmış ücret, burs ilanı veya sonraki başvuru tarihini vermiyor.",
        "best_en": "Applicants seeking satellite systems and space applications rather than conventional aircraft engineering.", "best_tr": "Klasik uçak mühendisliği yerine uydu sistemleri ve uzay uygulamaları arayan adaylar.",
        "not_en": "Students needing fully verified current cost and deadline information before shortlisting.", "not_tr": "Kısa listeye almadan önce tamamen doğrulanmış güncel ücret ve tarih bilgisine ihtiyaç duyan öğrenciler.",
        "sources": [
            src(STAR_PROGRAM, "official_program_page", "STAR official study guide", ["program", "language", "admission"], "Confirms the 120-ECTS English inter-institutional Master's and both tracks.", "120 AKTS İngilizce kurumlararası yüksek lisansı ve iki yolu doğrular."),
            src(STAR_PROGRAM, "official_admission_page", "STAR eligibility", ["admission", "non_eu_eligibility"], "States that recognised foreign bachelor's holders are eligible and gives the target backgrounds.", "Tanınan yabancı lisans mezunlarının uygun olduğunu ve hedef altyapıları belirtir."),
            src(STAR_PROGRAM, "official_curriculum_page", "STAR curriculum", ["curriculum"], "Publishes the four-semester, 120-ECTS structure and course lists.", "Dört yarıyıllık 120 AKTS yapıyı ve ders listelerini yayımlar."),
            src(STAR_DEPT, "official_department_page", "NKUA Physics postgraduate programmes", ["research", "department"], "Confirms STAR as an inter-institutional programme with Patras engineering departments.", "STAR'ı Patras mühendislik bölümleriyle kurumlararası program olarak doğrular."),
        ],
    },
    {
        "id": "tr-thku-aerospace-engineering-thesis-msc", "country": "Türkiye", "university": "University of Turkish Aeronautical Association",
        "university_native": "Türk Hava Kurumu Üniversitesi", "city": "Ankara", "program": "Aerospace Engineering (English) — Thesis Master's",
        "program_native": "Havacılık ve Uzay Mühendisliği (İngilizce) Tezli Yüksek Lisans", "duration_years": None, "ects": None,
        "languages": ["English"], "program_url": THK_ACTIVE, "department": "Graduate School / Aerospace Engineering", "curriculum_url": THK_ACTIVE,
        "non_eu": None, "previous_en": "Unknown in the retained current sources.", "previous_tr": "Tutulan güncel kaynaklarda bilinmiyor.",
        "admission": True, "admission_mode": "application review and interview", "admission_risk": "unknown", "english_level": None,
        "tuition": {}, "scholarship": {}, "deadline": None, "academic_year": "2025/2026 active-status evidence; next call not verified",
        "mandatory": [], "tags": ["aerospace_engineering", "thesis", "english_taught"],
        "fit_en": "A direct English thesis-based aerospace engineering Master's at Türkiye's aviation-specialised university.",
        "fit_tr": "Türkiye'nin havacılık temalı uzman üniversitesinde doğrudan İngilizce tezli havacılık ve uzay mühendisliği yüksek lisansı.",
        "risk_en": "The official result list confirms recent intake and language, but current curriculum, tuition, exact duration, non-EU rules and next deadline remain unverified.",
        "risk_tr": "Resmî sonuç listesi yakın dönem öğrenci alımını ve dili doğrular; güncel müfredat, ücret, kesin süre, yabancı öğrenci kuralları ve sonraki tarih doğrulanmadı.",
        "best_en": "Applicants who specifically want an English thesis route in Ankara and can verify the next call directly.", "best_tr": "Ankara'da İngilizce tezli yol isteyen ve sonraki ilanı doğrudan doğrulayabilen adaylar.",
        "not_en": "Applicants who need a fully documented cost and international-admission profile now.", "not_tr": "Şimdiden tam belgeli ücret ve uluslararası kabul profiline ihtiyaç duyan adaylar.",
        "sources": [
            src(THK_ACTIVE, "official_program_page", "THKU 2025/26 Aerospace Engineering Master's results", ["program", "language"], "Recent official results confirm the English thesis Master's admitted students.", "Yakın tarihli resmî sonuçlar İngilizce tezli yüksek lisansa öğrenci alındığını doğrular.", access_status="pdf"),
            src(THK_ACTIVE, "official_admission_page", "THKU Aerospace Engineering Master's selection results", ["admission"], "Confirms an active interview-based selection cycle in 2025/26.", "2025/26'da aktif mülakatlı seçim döngüsünü doğrular.", access_status="pdf"),
        ],
        "curriculum_url": THK_ACTIVE, "language_confidence": "high", "admission_confidence": "medium",
    },
    {
        "id": "tr-erciyes-space-engineering-msc", "country": "Türkiye", "university": "Erciyes University",
        "university_native": "Erciyes Üniversitesi", "city": "Kayseri", "program": "Space Engineering Thesis Master's",
        "program_native": "Uzay Mühendisliği Tezli Yüksek Lisans", "duration_years": None, "ects": None, "languages": ["Turkish"],
        "program_url": ERU_SPACE, "department": "Department of Space Engineering", "curriculum_url": ERU_SPACE, "non_eu": None,
        "previous_en": "Programme-specific eligible bachelor's fields must be checked in the current Graduate School quota document.",
        "previous_tr": "Programa özgü uygun lisans alanları güncel Fen Bilimleri Enstitüsü kontenjan belgesinden kontrol edilmelidir.",
        "admission": True, "admission_mode": "online application and programme interview", "admission_risk": "medium",
        "tuition": {}, "scholarship": {}, "deadline": "2026-06-21 (closed reference; next intake not verified)", "academic_year": "2026/2027 first autumn call",
        "rounds": ["2026-06-15 to 2026-06-21"], "mandatory": [], "tags": ["space_engineering", "satellites", "space_systems", "thesis"],
        "primary_categories": ["Space Systems and Astronautics"],
        "fit_en": "A direct Space Engineering thesis Master's with active 2025/26 coursework and a June 2026 interview cycle.",
        "fit_tr": "Aktif 2025/26 dersleri ve Haziran 2026 mülakat döngüsü bulunan doğrudan Uzay Mühendisliği tezli yüksek lisansı.",
        "risk_en": "Teaching is Turkish; exact ECTS, duration, tuition, scholarship and international-student quota were not verified in a current programme-specific source.",
        "risk_tr": "Eğitim dili Türkçedir; kesin AKTS, süre, ücret, burs ve yabancı öğrenci kontenjanı güncel programa özgü kaynakta doğrulanmadı.",
        "best_en": "Turkish-speaking applicants targeting spacecraft and satellite engineering research in Kayseri.", "best_tr": "Kayseri'de uzay aracı ve uydu mühendisliği araştırması hedefleyen Türkçe bilen adaylar.",
        "not_en": "English-only or cost-sensitive international applicants without direct confirmation from the Graduate School.", "not_tr": "Enstitüden doğrudan teyit almayan yalnız İngilizce bilen veya ücret hassasiyetli uluslararası adaylar.",
        "sources": [
            src(ERU_SPACE, "official_program_page", "Erciyes Space Engineering", ["program", "language"], "Current department page shows active Master's coursework and June 2026 interview announcements.", "Güncel bölüm sayfası aktif yüksek lisans derslerini ve Haziran 2026 mülakat duyurusunu gösterir."),
            src(ERU_CALL, "official_admission_page", "Erciyes 2026/27 graduate call", ["admission", "deadline"], "Publishes the June 15–21 application window and programme-specific condition warning.", "15–21 Haziran başvuru aralığını ve programa özgü şart uyarısını yayımlar."),
            src(ERU_SPACE, "official_curriculum_page", "Erciyes Space Engineering Master's activity", ["curriculum"], "The department shows active Master's course schedules; a complete current curriculum was not retained.", "Bölüm aktif yüksek lisans ders programlarını gösterir; tam güncel müfredat kaydedilmedi.", confidence="medium"),
            src(ERU_SPACE, "official_department_page", "Erciyes Space Engineering department", ["research", "department"], "Confirms the dedicated department and current space/satellite activities.", "Uzmanlaşmış bölümü ve güncel uzay/uydu faaliyetlerini doğrular."),
        ],
        "language_confidence": "medium", "admission_confidence": "high",
    },
    {
        "id": "tr-neu-aerospace-engineering-thesis-msc", "country": "Türkiye", "university": "Necmettin Erbakan University",
        "university_native": "Necmettin Erbakan Üniversitesi", "city": "Konya", "program": "Aerospace Engineering Thesis Master's",
        "program_native": "Havacılık ve Uzay Mühendisliği Tezli Yüksek Lisans", "duration_years": None, "ects": None,
        "languages": ["Turkish", "English (30%)"], "program_url": NEU_PROGRAMS, "department": "Interdisciplinary Aerospace Engineering Master's",
        "curriculum_url": NEU_BOLOGNA, "non_eu": None,
        "previous_en": "The programme accepts relevant engineering backgrounds; exact 2026/27 degree restrictions must be checked in the call attachment.",
        "previous_tr": "Program ilgili mühendislik altyapılarını kabul eder; 2026/27 kesin mezuniyet kısıtları ilan ekinden kontrol edilmelidir.",
        "backgrounds": ["Aerospace/space/aircraft engineering", "Mechanical engineering", "Related engineering subject to the call"],
        "admission": True, "admission_mode": "Graduate School application and programme evaluation", "admission_risk": "medium",
        "language_warning": "The official Bologna page states the programme began with 30% English; it is not an English-only degree.", "language_risk": "high",
        "tuition": {}, "scholarship": {}, "deadline": None, "academic_year": "2026/2027 call published; attachment deadline not retained",
        "mandatory": [], "tags": ["aerospace_engineering", "space_systems", "satellites", "propulsion", "control"],
        "fit_en": "An active interdisciplinary thesis Master's covering aerospace and space systems, with the official Bologna profile stating 30% English delivery.",
        "fit_tr": "Havacılık ve uzay sistemlerini kapsayan, resmî Bologna profilinde %30 İngilizce olarak belirtilen aktif disiplinlerarası tezli yüksek lisans.",
        "risk_en": "It is not English-only, and current tuition, scholarship, exact duration/ECTS, non-EU route and deadline remain unverified.",
        "risk_tr": "Yalnız İngilizce değildir; güncel ücret, burs, kesin süre/AKTS, yabancı öğrenci yolu ve son tarih doğrulanmadı.",
        "best_en": "Turkish-speaking applicants wanting an interdisciplinary aerospace/space thesis route in Konya.", "best_tr": "Konya'da disiplinlerarası havacılık/uzay tez yolu isteyen Türkçe bilen adaylar.",
        "not_en": "English-only applicants or students requiring a fully verified international fee profile.", "not_tr": "Yalnız İngilizce bilen veya tamamen doğrulanmış uluslararası ücret profili isteyen adaylar.",
        "sources": [
            src(NEU_PROGRAMS, "official_program_page", "NEU programme catalogue", ["program", "status"], "Lists the active interdisciplinary thesis Master's in Aerospace Engineering.", "Aktif disiplinlerarası Havacılık ve Uzay Mühendisliği tezli yüksek lisansını listeler."),
            src(NEU_CALL, "official_admission_page", "NEU 2026/27 graduate admission notice", ["admission", "deadline"], "Confirms the Graduate School published a 2026/27 thesis Master's call.", "Fen Bilimleri Enstitüsünün 2026/27 tezli yüksek lisans ilanını yayımladığını doğrular."),
            src(NEU_BOLOGNA, "official_university_policy_page", "NEU Aerospace Engineering language profile", ["language"], "The official Bologna profile states that the programme started with 30% English delivery.", "Resmî Bologna profili programın %30 İngilizce eğitimle başladığını belirtir."),
            src(NEU_BOLOGNA, "official_curriculum_page", "NEU Aerospace Engineering Bologna profile", ["curriculum", "language"], "States the programme began with 30% English and describes its aerospace/space scope.", "Programın %30 İngilizce başladığını ve havacılık/uzay kapsamını belirtir."),
            src(NEU_BOLOGNA, "official_department_page", "NEU Aerospace Engineering academic profile", ["research", "department"], "Describes satellite, launch, propulsion, control and space-system technology areas.", "Uydu, fırlatma, itki, kontrol ve uzay sistemleri teknoloji alanlarını açıklar."),
        ],
        "language_confidence": "high", "admission_confidence": "medium",
    },
]


TURKEY_EXCLUDED_IDS = {
    "tr-thku-aerospace-engineering-thesis-msc",
    "tr-erciyes-space-engineering-msc",
    "tr-neu-aerospace-engineering-thesis-msc",
    "tr-koc-mechanical-aerospace-track-bsc",
}

CURATED_TURKEY_SPECS: list[dict[str, Any]] = [
    {
        "id": "tr-itu-aerospace-msc",
        "country": "Turkey",
        "university": "Istanbul Technical University (ITU)",
        "university_native": "İstanbul Teknik Üniversitesi",
        "city": "Istanbul",
        "program": "M.Sc. Aeronautics and Astronautics Engineering",
        "program_native": "Uçak ve Uzay Mühendisliği Tezli Yüksek Lisans",
        "degree": "MSc",
        "degree_level": "Master",
        "duration_years": None,
        "ects": None,
        "languages": ["Unknown"],
        "language_confidence": "unknown",
        "program_url": "https://www.tyyc.itu.edu.tr/ProgramHakkinda.php?Dili=EN&Program=UUM_UU_YL",
        "department": "Interdisciplinary Aeronautics and Astronautics Engineering graduate programme",
        "curriculum_url": "https://www.tyyc.itu.edu.tr/ProgramHakkinda.php?Dili=EN&Program=UUM_UU_YL",
        "non_eu": True,
        "previous_en": "Applicants graduating from any engineering programme may apply. For 2026/27, the official conditions use GPA-dependent ALES/GRE thresholds.",
        "previous_tr": "Herhangi bir mühendislik programından mezun adaylar başvurabilir. 2026/27 resmî koşulları GNO'ya bağlı ALES/GRE eşikleri kullanır.",
        "backgrounds": ["All engineering programmes"],
        "admission": True,
        "admission_mode": "graduate application review under published GPA and ALES/GRE thresholds",
        "admission_risk": "high",
        "tuition": {
            "try_year": 33300,
            "basis": "2025/26 annual tuition for international postgraduate entrants in 2024/25 or 2025/26, paid in two equal instalments",
            "note_en": "The official 2025/26 table lists TRY 33,300 for international postgraduate entrants in 2024/25 or 2025/26; the 2026/27 amount must be rechecked.",
            "note_tr": "Resmî 2025/26 tablosu 2024/25 veya 2025/26 girişli uluslararası lisansüstü öğrenciler için 33.300 TL gösterir; 2026/27 tutarı yeniden kontrol edilmelidir.",
        },
        "tuition_confidence": "medium",
        "scholarship": {},
        "deadline": "2026-06-28 (closed reference; next cycle not verified)",
        "academic_year": "2026/2027 Fall admission; 2025/2026 tuition",
        "rounds": ["2026-04-24 09:00 to 2026-06-28 17:00 Turkey time"],
        "tracks": ["Aerodynamics and fluid dynamics", "Propulsion", "Structures and materials", "Flight and orbital dynamics", "Air and space vehicle control"],
        "mandatory": [],
        "electives": [],
        "thesis_required": True,
        "tags": ["aerodynamics", "propulsion", "aerospace_structures", "flight_dynamics", "orbital_mechanics", "control"],
        "primary_categories": ["Akışkanlar Mekaniği ve Aerodinamik", "İtki ve Enerji Sistemleri", "Yapılar ve Malzemeler"],
        "secondary_categories": ["Uçuş Dinamiği, GNC ve Otonomi", "Uzay Sistemleri ve Astronotik"],
        "research_areas": ["Aerodynamics", "Propulsion", "Aerospace structures and materials", "Flight mechanics", "Orbital mechanics", "Aircraft and spacecraft control"],
        "fit_en": "A broad interdisciplinary ITU master's spanning aircraft and spacecraft analysis, aerodynamics, propulsion, structures, flight/orbital dynamics and control.",
        "fit_tr": "Uçak ve uzay aracı analizi, aerodinamik, itki, yapılar, uçuş/yörünge dinamiği ve kontrolü kapsayan geniş disiplinlerarası İTÜ yüksek lisansı.",
        "risk_en": "The current official programme page does not state the teaching language clearly enough to retain it as verified; the 2026/27 admission window is already closed and the next tuition table is pending.",
        "risk_tr": "Güncel resmî program sayfası eğitim dilini doğrulanmış olarak kaydetmeye yetecek açıklıkta belirtmiyor; 2026/27 başvuru aralığı kapandı ve yeni ücret tablosu bekleniyor.",
        "best_en": "Applicants wanting a broad aircraft-and-space graduate route with several possible technical specializations.",
        "best_tr": "Birden fazla teknik uzmanlaşmaya açık geniş uçak ve uzay lisansüstü yolu isteyen adaylar.",
        "not_en": "Applicants who need a currently verified English-only programme or an open application round today.",
        "not_tr": "Bugün açık bir başvuru dönemi veya güncel olarak doğrulanmış yalnız İngilizce program isteyen adaylar.",
        "sources": [
            src("https://www.tyyc.itu.edu.tr/ProgramHakkinda.php?Dili=EN&Program=UUM_UU_YL", "official_program_page", "ITU Aeronautics and Astronautics Engineering MSc", ["program"], "Confirms the active interdisciplinary MSc and its aircraft/space scope.", "Aktif disiplinlerarası yüksek lisansı ve uçak/uzay kapsamını doğrular."),
            src("https://www.tyyc.itu.edu.tr/ProgramHakkinda.php?Dili=EN&Program=UUM_UU_YL", "official_curriculum_page", "ITU Aeronautics and Astronautics Engineering study areas", ["curriculum"], "Publishes the programme's aerodynamics, propulsion, structures, flight/orbital dynamics and control scope.", "Programın aerodinamik, itki, yapılar, uçuş/yörünge dinamiği ve kontrol kapsamını yayımlar."),
            src("https://www.tyyc.itu.edu.tr/ProgramHakkinda.php?Dili=EN&Program=UUM_UU_YL&SayfaBaslik=SKayitKabulSartlari-LU-Tum&sdonemkodu=202710", "official_admission_page", "ITU 2026/27 Aeronautics and Astronautics admission conditions", ["admission", "non_eu_eligibility", "deadline"], "Publishes international quotas, eligible backgrounds, GPA/ALES/GRE bands and the closed Fall 2026/27 dates.", "Uluslararası kontenjanı, uygun altyapıları, GNO/ALES/GRE aralıklarını ve kapanmış 2026/27 güz tarihlerini yayımlar."),
            src("https://www.sis.itu.edu.tr/EN/student/tuition-fee/fees/20261020/tutionfees.php", "official_tuition_page", "ITU 2025/26 tuition fees", ["tuition"], "Lists TRY 33,300 annual tuition for recent-entry international postgraduate students, paid in two instalments.", "Yakın dönem girişli uluslararası lisansüstü öğrenciler için iki taksitte yıllık 33.300 TL yayımlar."),
            src("https://www.tyyc.itu.edu.tr/ProgramHakkinda.php?Dili=EN&Program=UUM_UU_YL", "official_department_page", "ITU Aeronautics and Astronautics programme profile", ["research", "department"], "Documents the programme's theoretical, computational and experimental research domains.", "Programın kuramsal, hesaplamalı ve deneysel araştırma alanlarını belgeler."),
        ],
    },
    {
        "id": "tr-itu-astronautical-msc",
        "country": "Turkey",
        "university": "Istanbul Technical University (ITU)",
        "university_native": "İstanbul Teknik Üniversitesi",
        "city": "Istanbul",
        "program": "M.Sc. Astronautical Engineering",
        "program_native": "Uzay Mühendisliği Tezli Yüksek Lisans",
        "degree": "MSc",
        "degree_level": "Master",
        "duration_years": None,
        "ects": None,
        "languages": ["English"],
        "program_url": "https://www.tyyc.itu.edu.tr/ProgramHakkinda.php?Dili=EN&Program=UZM_UB_YL",
        "department": "Department of Astronautical Engineering",
        "curriculum_url": "https://www.tyyc.itu.edu.tr/ProgramHakkinda.php?Dili=EN&Program=UZM_UB_YL",
        "non_eu": True,
        "previous_en": "The official 2026/27 conditions accept specified engineering and science degrees and apply GPA-dependent ALES/GRE thresholds.",
        "previous_tr": "Resmî 2026/27 koşulları belirli mühendislik ve fen derecelerini kabul eder ve GNO'ya bağlı ALES/GRE eşikleri uygular.",
        "backgrounds": ["Astronautical/aerospace/aeronautical engineering", "Mechanical, control, electrical-electronics and related engineering", "Physics, mathematics and selected computing disciplines listed in the call"],
        "admission": True,
        "admission_mode": "graduate application review under published GPA, ALES/GRE and degree-field rules",
        "admission_risk": "high",
        "tuition": {
            "try_year": 33300,
            "basis": "2025/26 annual tuition for international postgraduate entrants in 2024/25 or 2025/26, paid in two equal instalments",
            "note_en": "The official 2025/26 table lists TRY 33,300 for recent-entry international postgraduate students; 2026/27 must be rechecked.",
            "note_tr": "Resmî 2025/26 tablosu yakın dönem girişli uluslararası lisansüstü öğrenciler için 33.300 TL gösterir; 2026/27 yeniden kontrol edilmelidir.",
        },
        "tuition_confidence": "medium",
        "scholarship": {},
        "deadline": "2026-06-28 (closed reference; next cycle not verified)",
        "academic_year": "2026/2027 Fall admission; 2025/2026 tuition",
        "rounds": ["2026-04-24 09:00 to 2026-06-28 17:00 Turkey time"],
        "tracks": ["Spacecraft systems", "Space propulsion", "Spacecraft dynamics and control", "Satellite technologies", "Space environment and physics"],
        "mandatory": ["Engineering Mathematics", "Spacecraft Dynamics", "Space Propulsion", "Spacecraft Architectures and Subsystems Design"],
        "electives": ["Space Structures and Mechanisms", "High Speed Flows", "Spacecraft Thermal Control", "Celestial and Applied Orbital Mechanics", "Spacecraft Navigation", "Space Physics"],
        "thesis_required": True,
        "tags": ["spacecraft_systems", "space_propulsion", "spacecraft_dynamics", "satellites", "orbital_mechanics", "spacecraft_navigation"],
        "primary_categories": ["Uzay Sistemleri ve Astronotik"],
        "secondary_categories": ["İtki ve Enerji Sistemleri", "Uçuş Dinamiği, GNC ve Otonomi"],
        "research_areas": ["Spacecraft architecture", "Launch vehicles", "Space propulsion", "Spacecraft dynamics and control", "Satellite systems", "Space environment"],
        "fit_en": "A direct 100% English astronautical engineering MSc centred on spacecraft, launch vehicles, satellites, propulsion, dynamics/control and the space environment.",
        "fit_tr": "Uzay araçları, fırlatma sistemleri, uydular, itki, dinamik/kontrol ve uzay ortamına odaklanan doğrudan %100 İngilizce uzay mühendisliği yüksek lisansı.",
        "risk_en": "The Fall 2026/27 application period is closed; current scholarship evidence and the 2026/27 tuition amount were not verified.",
        "risk_tr": "2026/27 güz başvuru dönemi kapandı; güncel burs kanıtı ve 2026/27 ücret tutarı doğrulanmadı.",
        "best_en": "Applicants targeting spacecraft systems, satellite technologies, orbital mechanics, space propulsion or spacecraft GNC.",
        "best_tr": "Uzay aracı sistemleri, uydu teknolojileri, yörünge mekaniği, uzay itkisi veya uzay aracı GNC alanlarını hedefleyen adaylar.",
        "not_en": "Applicants focused primarily on conventional aircraft design and low-speed aerodynamics.",
        "not_tr": "Öncelikle klasik uçak tasarımı ve düşük hızlı aerodinamiğe odaklanan adaylar.",
        "sources": [
            src("https://www.tyyc.itu.edu.tr/ProgramHakkinda.php?Dili=EN&Program=UZM_UB_YL", "official_program_page", "ITU Astronautical Engineering MSc", ["program", "language"], "Confirms the active thesis MSc, 100% English instruction and international availability.", "Aktif tezli yüksek lisansı, %100 İngilizce eğitimi ve uluslararası adaylara açıklığı doğrular."),
            src("https://www.tyyc.itu.edu.tr/ProgramHakkinda.php?Dili=EN&Program=UZM_UB_YL", "official_curriculum_page", "ITU Astronautical Engineering curriculum", ["curriculum"], "Lists spacecraft, propulsion, orbital mechanics, navigation, structures, thermal control and space-physics courses.", "Uzay aracı, itki, yörünge mekaniği, seyrüsefer, yapılar, ısıl kontrol ve uzay fiziği derslerini listeler."),
            src("https://www.tyyc.itu.edu.tr/ProgramHakkinda.php?Dili=EN&Program=UZM_UB_YL&SayfaBaslik=SKayitKabulSartlari-LU-Tum&sdonemkodu=202710", "official_admission_page", "ITU 2026/27 Astronautical Engineering admission conditions", ["admission", "non_eu_eligibility", "deadline"], "Publishes the international quota, eligible degree list, thresholds and closed Fall 2026/27 dates.", "Uluslararası kontenjanı, uygun derece listesini, eşikleri ve kapanmış 2026/27 güz tarihlerini yayımlar."),
            src("https://www.sis.itu.edu.tr/EN/student/tuition-fee/fees/20261020/tutionfees.php", "official_tuition_page", "ITU 2025/26 tuition fees", ["tuition"], "Lists TRY 33,300 annual tuition for recent-entry international postgraduate students.", "Yakın dönem girişli uluslararası lisansüstü öğrenciler için yıllık 33.300 TL yayımlar."),
            src("https://www.tyyc.itu.edu.tr/ProgramHakkinda.php?Dili=EN&Program=UZM_UB_YL", "official_department_page", "ITU Astronautical Engineering programme profile", ["research", "department"], "Documents spacecraft design, launch vehicles, satellites, propulsion, dynamics/control and space-environment research scope.", "Uzay aracı tasarımı, fırlatma araçları, uydular, itki, dinamik/kontrol ve uzay ortamı araştırma kapsamını belgeler."),
        ],
    },
    {
        "id": "tr-metu-aerospace-msc",
        "country": "Turkey",
        "university": "Middle East Technical University (METU)",
        "university_native": "Orta Doğu Teknik Üniversitesi (ODTÜ)",
        "city": "Ankara",
        "program": "M.Sc. Aerospace Engineering",
        "program_native": "Havacılık ve Uzay Mühendisliği Tezli Yüksek Lisans",
        "degree": "MSc",
        "degree_level": "Master",
        "duration_years": None,
        "ects": None,
        "languages": ["English"],
        "program_url": "https://ae.metu.edu.tr/grad/",
        "department": "Department of Aerospace Engineering",
        "curriculum_url": "https://ae.metu.edu.tr/grad/curriculum.shtml",
        "non_eu": True,
        "previous_en": "The department publishes minimum M.Sc. thresholds of METU EPE/TOEFL equivalent 65, ALES 75 and bachelor's GPA 2.50, plus prior contact with a prospective thesis advisor.",
        "previous_tr": "Bölüm yüksek lisans için ODTÜ İYS/TOEFL eşdeğeri 65, ALES 75 ve lisans GNO 2,50 alt sınırları ile önceden olası tez danışmanıyla iletişim şartını yayımlar.",
        "backgrounds": ["Aerospace engineering", "Aeronautical or astronautical engineering", "Related engineering subject to department evaluation"],
        "admission": True,
        "admission_mode": "departmental review with prospective-advisor approval",
        "admission_risk": "high",
        "english_level": "METU EPE 65 or official equivalent published by METU",
        "english_tests": ["METU EPE", "TOEFL or another officially accepted equivalent"],
        "tuition": {
            "usd_semester": 375,
            "basis": "per semester in 2025/26 for foreign-citizenship graduate students who started in Fall 2023/24 or later",
            "note_en": "The official 2025/26 table lists USD 375 per semester for foreign graduate students who started in Fall 2023/24 or later; 2026/27 must be rechecked.",
            "note_tr": "Resmî 2025/26 tablosu 2023/24 güz veya sonrasında başlayan yabancı lisansüstü öğrenciler için dönem başına 375 USD gösterir; 2026/27 yeniden kontrol edilmelidir.",
        },
        "tuition_confidence": "medium",
        "scholarship": {},
        "deadline": None,
        "academic_year": "2025/2026 programme and tuition evidence; next exact application date not verified",
        "tracks": ["Aerodynamics", "Structures and Materials", "Propulsion", "Flight Dynamics and Control", "Spacecraft Technologies"],
        "mandatory": ["Thesis Proposal", "Ethical Behavior in Engineering", "M.S. Thesis", "Special Studies"],
        "electives": ["Seven approved electives, including one advanced mathematics course"],
        "thesis_required": True,
        "tags": ["aerodynamics", "aerospace_structures", "propulsion", "flight_dynamics", "control", "spacecraft_technologies"],
        "primary_categories": ["Akışkanlar Mekaniği ve Aerodinamik", "Yapılar ve Malzemeler", "İtki ve Enerji Sistemleri"],
        "secondary_categories": ["Uçuş Dinamiği, GNC ve Otonomi", "Uzay Sistemleri ve Astronotik"],
        "research_areas": ["Aerodynamics", "Structures and materials", "Propulsion", "Flight dynamics and control", "Spacecraft technologies"],
        "fit_en": "A direct English aerospace engineering MSc with established research routes in aerodynamics, structures/materials, propulsion, flight dynamics/control and spacecraft technologies.",
        "fit_tr": "Aerodinamik, yapılar/malzemeler, itki, uçuş dinamiği/kontrol ve uzay aracı teknolojilerinde yerleşik araştırma yolları bulunan doğrudan İngilizce havacılık-uzay yüksek lisansı.",
        "risk_en": "Applicants must secure prospective-advisor approval; the next exact application deadline, current scholarship route and 2026/27 tuition are not verified.",
        "risk_tr": "Adayların olası danışman onayı alması gerekir; sonraki kesin başvuru tarihi, güncel burs yolu ve 2026/27 ücreti doğrulanmadı.",
        "best_en": "Research-oriented applicants who can align early with a METU faculty advisor in one of the department's five core areas.",
        "best_tr": "Bölümün beş temel alanından birinde erkenden ODTÜ öğretim üyesiyle eşleşebilen araştırma odaklı adaylar.",
        "not_en": "Applicants seeking a course-only degree or applying without first identifying a prospective thesis advisor.",
        "not_tr": "Yalnız ders ağırlıklı derece isteyen veya önceden olası tez danışmanı belirlemeden başvuran adaylar.",
        "sources": [
            src("https://ae.metu.edu.tr/grad/", "official_program_page", "METU Aerospace Engineering graduate programmes", ["program"], "Confirms the active MSc and five aerospace research fields.", "Aktif yüksek lisansı ve beş havacılık-uzay araştırma alanını doğrular."),
            src("https://www.metu.edu.tr/general-information", "official_university_policy_page", "METU language of instruction", ["language"], "States that METU's language of instruction is English.", "ODTÜ'nün eğitim dilinin İngilizce olduğunu belirtir."),
            src("https://ae.metu.edu.tr/grad/", "official_admission_page", "METU Aerospace Engineering graduate admission requirements", ["admission"], "Publishes the MSc English, ALES and GPA thresholds and prospective-advisor approval requirement.", "Yüksek lisans İngilizce, ALES ve GNO eşikleri ile olası danışman onayı şartını yayımlar."),
            src("https://oidb.metu.edu.tr/index.php/en/registrations-newly-admitted-international-students-graduate-programs", "official_admission_page", "METU international graduate registration", ["non_eu_eligibility"], "Confirms the active international graduate route and 2026 registration process.", "Aktif uluslararası lisansüstü yolunu ve 2026 kayıt sürecini doğrular."),
            src("https://ae.metu.edu.tr/grad/curriculum.shtml", "official_curriculum_page", "METU Aerospace Engineering MSc curriculum", ["curriculum"], "Lists the thesis proposal, ethics, seven electives, advanced mathematics requirement and thesis registration.", "Tez önerisi, etik, yedi seçmeli, ileri matematik şartı ve tez kaydını listeler."),
            src("https://iso.metu.edu.tr/tr/system/files/2025-2026_tuition_fee_11082025.pdf", "official_tuition_page", "METU 2025/26 foreign graduate tuition", ["tuition"], "Lists USD 375 per semester for recent-entry foreign graduate students.", "Yakın dönem girişli yabancı lisansüstü öğrenciler için dönem başına 375 USD yayımlar.", access_status="pdf"),
            src("https://ae.metu.edu.tr/grad/", "official_department_page", "METU Aerospace Engineering graduate research areas", ["research", "department"], "Documents aerodynamics, structures/materials, propulsion, flight dynamics/control and spacecraft technologies.", "Aerodinamik, yapılar/malzemeler, itki, uçuş dinamiği/kontrol ve uzay aracı teknolojilerini belgeler."),
        ],
    },
    {
        "id": "tr-bogazici-mechanical-fluid-mechanics-msc",
        "country": "Turkey",
        "university": "Boğaziçi University",
        "university_native": "Boğaziçi Üniversitesi",
        "city": "Istanbul",
        "program": "M.S. Mechanical Engineering — Fluid Mechanics Option",
        "program_native": "Makine Mühendisliği Tezli Yüksek Lisans — Akışkanlar Mekaniği Seçeneği",
        "degree": "MSc",
        "degree_level": "Master",
        "duration_years": 2,
        "ects": 132,
        "languages": ["English"],
        "program_url": "https://bogazici.edu.tr/en/pages/graduate-program-in-mechanical-engineering/466",
        "department": "Department of Mechanical Engineering",
        "curriculum_url": "https://bogazici.edu.tr/en/pages/graduate-program-in-mechanical-engineering/466",
        "non_eu": True,
        "previous_en": "A bachelor's degree; the department publishes a minimum 2.50/4.00 GPA together with ALES Quantitative 75 or GRE Quantitative 155 and an interview.",
        "previous_tr": "Lisans derecesi; bölüm en az 2,50/4,00 GNO ile birlikte ALES Sayısal 75 veya GRE Sayısal 155 ve mülakat şartı yayımlar.",
        "backgrounds": ["Mechanical engineering", "Aerospace engineering", "Related engineering subject to departmental evaluation"],
        "admission": True,
        "admission_mode": "document review and department interview",
        "admission_risk": "medium",
        "documents": ["Bachelor's diploma or expected-graduation document", "Transcript", "ALES or GRE score", "English proficiency result", "Graduate application documents required by the university"],
        "english_level": "BUEPT C/B/A, TOEFL iBT 79 with TWE 22, or IELTS 6.5 on the checked department page",
        "english_tests": ["BUEPT", "TOEFL iBT", "IELTS"],
        "tuition": {
            "usd_semester": 500,
            "basis": "per semester for graduate students with foreign citizenship enrolled in 2025/2026, within the expected study period",
            "note_en": "The official 2025/26 table lists USD 500 per semester for MA and PhD students with foreign citizenship; the 2026/27 amount must be rechecked.",
            "note_tr": "Resmî 2025/26 tablosu yabancı uyruklu yüksek lisans ve doktora öğrencileri için dönem başına 500 USD gösterir; 2026/27 tutarı yeniden kontrol edilmelidir.",
        },
        "tuition_confidence": "medium",
        "scholarship": {},
        "deadline": None,
        "academic_year": "2025/2026 tuition; standing admission timing checked 2026-07-19",
        "intakes": ["Fall", "Spring"],
        "tracks": ["Fluid Mechanics"],
        "mandatory": ["Advanced Engineering Mathematics I", "Advanced Fluid Mechanics or Conduction Heat Transfer", "Guided Research", "Graduate Seminar", "Master's Thesis"],
        "electives": ["Viscous Flow Theory", "Turbulent Flow Theory", "Gas Dynamics", "Computational Fluid Dynamics", "Convective Heat Transfer"],
        "thesis_required": True,
        "tags": ["fluid_mechanics", "computational_fluid_dynamics", "aerodynamics", "gas_dynamics", "transonic_flow", "turbulence"],
        "primary_categories": ["Akışkanlar Mekaniği ve Aerodinamik"],
        "secondary_categories": ["Bilimsel Hesaplama, Yapay Zekâ ve Dijital Mühendislik"],
        "research_areas": ["Computational fluid dynamics", "Aerodynamics", "Gas dynamics", "Transonic flow", "Turbulence", "Combustion"],
        "research_en": "The official FMS Laboratory profile explicitly covers aerodynamics, gas dynamics, transonic flow, turbulence, combustion and computational modelling.",
        "research_tr": "Resmî FMS Laboratuvarı profili aerodinamik, gaz dinamiği, transonik akış, türbülans, yanma ve hesaplamalı modellemeyi açıkça kapsar.",
        "fit_en": "A high-selectivity mechanical engineering MSc with a formally declared Fluid Mechanics option, graduate CFD/gas-dynamics courses and an aerospace-relevant flow simulation laboratory.",
        "fit_tr": "Resmen tanımlı Akışkanlar Mekaniği seçeneği, lisansüstü HAD/gaz dinamiği dersleri ve havacılıkla ilgili akış benzetimi laboratuvarı bulunan seçici bir makine mühendisliği yüksek lisansı.",
        "risk_en": "This is not a standalone aerospace degree; its aerospace value comes from the fluid-mechanics option, course selection and research group. The next exact deadline and 2026/27 tuition are not yet verified.",
        "risk_tr": "Bu, bağımsız bir havacılık-uzay derecesi değildir; alana uygunluğu akışkanlar seçeneği, ders seçimi ve araştırma grubundan gelir. Sonraki kesin tarih ve 2026/27 ücreti henüz doğrulanmadı.",
        "best_en": "Applicants targeting CFD, aerodynamics, gas dynamics, transonic flow and turbulence research.",
        "best_tr": "HAD, aerodinamik, gaz dinamiği, transonik akış ve türbülans araştırması hedefleyen adaylar.",
        "not_en": "Students who require the diploma title itself to be Aerospace or Astronautical Engineering.",
        "not_tr": "Diploma adının doğrudan Havacılık-Uzay veya Uzay Mühendisliği olmasını isteyen öğrenciler.",
        "deadline_note_en": "The department states that fall applications generally begin in early April and spring applications in mid-December, but no exact next-cycle date was retained.",
        "deadline_note_tr": "Bölüm güz başvurularının genellikle nisan başında, bahar başvurularının aralık ortasında başladığını belirtiyor; sonraki dönem için kesin tarih kaydedilmedi.",
        "priority_en": "Recheck the live application calendar and the foreign-graduate tuition table for the intended intake.",
        "priority_tr": "Hedef dönem için canlı başvuru takvimini ve yabancı lisansüstü öğrenci ücret tablosunu yeniden kontrol edin.",
        "sources": [
            src("https://bogazici.edu.tr/en/pages/graduate-program-in-mechanical-engineering/466", "official_program_page", "Boğaziçi Mechanical Engineering graduate programme", ["program", "curriculum"], "Confirms the thesis MSc, 132 ECTS and the formally declared Fluid Mechanics option.", "Tezli yüksek lisansı, 132 AKTS'yi ve resmen tanımlı Akışkanlar Mekaniği seçeneğini doğrular."),
            src("https://bogazici.edu.tr/en/pages/graduate-program-in-mechanical-engineering/466", "official_curriculum_page", "Boğaziçi Mechanical Engineering graduate curriculum", ["curriculum"], "Lists the Fluid Mechanics core and electives, including CFD, gas dynamics and turbulence.", "HAD, gaz dinamiği ve türbülans dahil Akışkanlar Mekaniği çekirdek ve seçmeli derslerini listeler."),
            src("https://me.bogazici.edu.tr/en/pages/graduate-applications/2641", "official_admission_page", "Boğaziçi Mechanical Engineering graduate applications", ["admission", "non_eu_eligibility", "deadline"], "Publishes GPA, ALES/GRE, English and interview requirements and explicitly addresses foreign applicants.", "GNO, ALES/GRE, İngilizce ve mülakat şartlarını yayımlar ve yabancı adayları açıkça ele alır."),
            src("https://bogazici.edu.tr/en/pages/the-university/567", "official_university_policy_page", "Boğaziçi University academic policy", ["language"], "States that the university's language of instruction is English and that MSc programmes normally span four semesters.", "Üniversitenin eğitim dilinin İngilizce olduğunu ve yüksek lisans programlarının normalde dört dönem sürdüğünü belirtir."),
            src("https://adaylar.bogazici.edu.tr/Content/Files/2025_2026_Academic_Year_Tuition_fees_for_undergraduate_students_enrolled_under_international_student_quota_and_graduate_students_with_foreign_citizenship_%281%29.pdf", "official_tuition_page", "Boğaziçi 2025/26 foreign graduate tuition table", ["tuition"], "Lists USD 500 per semester for MA and PhD students with foreign citizenship enrolled in 2025/26.", "2025/26'da kayıtlı yabancı uyruklu yüksek lisans ve doktora öğrencileri için dönem başına 500 USD yayımlar.", access_status="pdf"),
            src("https://me.bogazici.edu.tr/en/pages/laboratories/2617", "official_lab_page", "Boğaziçi Mechanical Engineering laboratories", ["research", "labs"], "The FMS Laboratory explicitly lists aerodynamics, gas dynamics, transonic flow, turbulence, combustion and computational modelling.", "FMS Laboratuvarı aerodinamik, gaz dinamiği, transonik akış, türbülans, yanma ve hesaplamalı modellemeyi açıkça listeler."),
        ],
    },
    {
        "id": "tr-koc-mechanical-aerospace-track-bsc",
        "country": "Turkey",
        "university": "Koç University",
        "university_native": "Koç Üniversitesi",
        "city": "Istanbul",
        "program": "B.Sc. Mechanical Engineering — Aerospace Engineering Track",
        "program_native": "Makine Mühendisliği Lisans — Havacılık ve Uzay Mühendisliği İzi",
        "degree": "BSc",
        "degree_level": "Bachelor",
        "degree_class": "Undergraduate",
        "duration_years": 4,
        "ects": 240,
        "languages": ["English"],
        "program_url": "https://apply.ku.edu.tr/courses/course/32-bsc-mechanical-engineering",
        "department": "Department of Mechanical Engineering",
        "curriculum_url": "https://apply.ku.edu.tr/courses/course/32-bsc-mechanical-engineering",
        "non_eu": True,
        "previous_en": "Completion of secondary education and an eligible international diploma or examination; the current application page also requires transcripts, English evidence, a personal statement and two recommendations.",
        "previous_tr": "Ortaöğretimin tamamlanması ve kabul edilen uluslararası diploma veya sınav; güncel başvuru sayfası ayrıca transkript, İngilizce kanıtı, niyet mektubu ve iki referans ister.",
        "backgrounds": ["High school or secondary education with the required international qualification"],
        "admission": True,
        "admission_mode": "international undergraduate application review",
        "admission_risk": "high",
        "documents": ["High school transcript", "Eligible diploma or examination result", "English proficiency result", "Personal statement", "Two recommendations", "Passport or national ID"],
        "english_level": "An eligible English proficiency result is required unless an official exemption applies; exact accepted-test thresholds must be checked on the live form",
        "english_tests": [],
        "tuition": {
            "usd_year": 38000,
            "basis": "per year for the Fall 2026/27 international undergraduate intake; application fee and deposit are separate",
            "note_en": "The official application page publishes USD 38,000 per year, a TRY 1,000 application fee and a USD 1,500 deposit for Fall 2026/27.",
            "note_tr": "Resmî başvuru sayfası 2026/27 güz dönemi için yıllık 38.000 USD, 1.000 TL başvuru ücreti ve 1.500 USD depozito yayımlar.",
        },
        "scholarship": {
            "available": True,
            "name": "Koç University academic scholarship for admitted international undergraduate students",
            "non_eu": True,
            "url": "https://cdn.ku.edu.tr/cdn/files/registrar/web/en/Admission-of-International-Students_.pdf",
            "competitiveness": "high",
            "waivers": ["Tuition-only academic scholarship; award and percentage are not guaranteed"],
            "note_en": "The official international-admission procedure permits tuition-only academic scholarships for admitted international undergraduates for up to eight semesters; it does not guarantee an award or publish a percentage here.",
            "note_tr": "Resmî uluslararası kabul prosedürü, kabul edilen uluslararası lisans öğrencileri için en fazla sekiz dönem yalnız öğrenim ücretini kapsayan akademik burslara izin verir; ödül veya oran garanti edilmez.",
        },
        "scholarship_confidence": "medium",
        "curriculum_confidence": "medium",
        "deadline": "2026-07-15",
        "academic_year": "2026/2027 Fall intake",
        "intakes": ["Fall"],
        "rounds": ["Fall 2026/27 application deadline: 2026-07-15 23:59 Turkey time"],
        "tracks": ["Aerospace Engineering"],
        "mandatory": [],
        "electives": [],
        "thesis_required": False,
        "internship_required": None,
        "tags": ["mechanical_engineering", "aerospace_engineering_track", "engineering_design"],
        "primary_categories": ["Sistem Mühendisliği, Tasarım ve Optimizasyon"],
        "secondary_categories": ["Uçak Tasarımı ve Entegrasyonu"],
        "fit_en": "A selective English mechanical-engineering bachelor's whose official programme page explicitly offers an Aerospace Engineering track.",
        "fit_tr": "Resmî program sayfasında Havacılık ve Uzay Mühendisliği izi açıkça sunulan seçici, İngilizce bir makine mühendisliği lisansı.",
        "risk_en": "This is a Mechanical Engineering BSc with an aerospace track, not a standalone Aerospace Engineering diploma. The official page does not expose the track's individual course list in the retained evidence, and the published international tuition is high.",
        "risk_tr": "Bu, havacılık-uzay izi bulunan Makine Mühendisliği lisansıdır; bağımsız Havacılık-Uzay Mühendisliği diploması değildir. Tutulan resmî kanıt izdeki tek tek dersleri göstermiyor ve yayımlanan uluslararası ücret yüksektir.",
        "best_en": "International undergraduate applicants who want a broad mechanical foundation with a formally named aerospace track at Koç.",
        "best_tr": "Koç'ta resmen adlandırılmış havacılık-uzay iziyle geniş makine mühendisliği temeli isteyen uluslararası lisans adayları.",
        "not_en": "Graduate applicants or students who require a dedicated aerospace department and degree title.",
        "not_tr": "Lisansüstü adaylar veya ayrı bir havacılık-uzay bölümü ve diploma adı isteyen öğrenciler.",
        "deadline_note_en": "The official application page gives 15 July 2026 at 23:59 Turkey time for the Fall 2026/27 international undergraduate intake.",
        "deadline_note_tr": "Resmî başvuru sayfası 2026/27 güz uluslararası lisans dönemi için 15 Temmuz 2026 saat 23.59 Türkiye saati son tarihini verir.",
        "priority_en": "Before paying, verify the track course list, scholarship offer and all additional charges in the live applicant portal.",
        "priority_tr": "Ödeme öncesinde iz derslerini, burs teklifini ve tüm ek ücretleri canlı aday portalında doğrulayın.",
        "sources": [
            src("https://apply.ku.edu.tr/courses/course/32-bsc-mechanical-engineering", "official_program_page", "Koç BSc Mechanical Engineering", ["program", "language", "curriculum"], "Confirms the four-year, 240-ECTS English BSc and explicitly lists Aerospace Engineering among five tracks.", "Dört yıllık 240 AKTS İngilizce lisansı doğrular ve beş iz arasında Havacılık ve Uzay Mühendisliğini açıkça listeler."),
            src("https://apply.ku.edu.tr/courses/course/32-bsc-mechanical-engineering", "official_curriculum_page", "Koç Mechanical Engineering programme structure", ["curriculum"], "The official programme overview explicitly identifies Aerospace Engineering as a track; individual track courses were not exposed in the checked page.", "Resmî program özeti Havacılık ve Uzay Mühendisliğini açıkça bir iz olarak tanımlar; izdeki tek tek dersler kontrol edilen sayfada yayımlanmamıştır."),
            src("https://apply.ku.edu.tr/courses/course/32-bsc-mechanical-engineering", "official_admission_page", "Koç 2026/27 international undergraduate application", ["admission", "non_eu_eligibility", "deadline"], "Publishes the international entry route, documents and 15 July 2026 deadline.", "Uluslararası kabul yolunu, belgeleri ve 15 Temmuz 2026 son tarihini yayımlar."),
            src("https://apply.ku.edu.tr/courses/course/32-bsc-mechanical-engineering", "official_tuition_page", "Koç 2026/27 Mechanical Engineering tuition", ["tuition"], "Publishes USD 38,000 per year plus the separate application fee and deposit.", "Yıllık 38.000 USD ile ayrı başvuru ücreti ve depozitoyu yayımlar."),
            src("https://cdn.ku.edu.tr/cdn/files/registrar/web/en/Admission-of-International-Students_.pdf", "official_scholarship_page", "Koç procedures for admission of international students", ["scholarship", "non_eu_eligibility"], "States that admitted international undergraduates may receive tuition-only academic scholarships for up to eight semesters.", "Kabul edilen uluslararası lisans öğrencilerinin en fazla sekiz dönem yalnız öğrenim ücretini kapsayan akademik burs alabileceğini belirtir.", access_status="pdf", confidence="medium"),
        ],
    },
]


def upsert_country(
    filename: str,
    country: str,
    records: list[dict[str, Any]],
    *,
    remove_ids: set[str] | None = None,
) -> None:
    path = DATA / filename
    if path.exists():
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
    else:
        payload = {"country": country, "last_updated": CHECKED, "programs": []}

    if isinstance(payload, list):
        rows = payload
    else:
        payload.setdefault("country", country)
        payload["last_updated"] = CHECKED
        rows = payload.setdefault("programs", [])

    if remove_ids:
        rows[:] = [row for row in rows if not isinstance(row, dict) or row.get("id") not in remove_ids]

    positions = {row.get("id"): i for i, row in enumerate(rows) if isinstance(row, dict)}
    for record in records:
        if record["id"] in positions:
            rows[positions[record["id"]]] = record
        else:
            rows.append(record)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    active_specs = [spec for spec in SPECS if spec["id"] not in TURKEY_EXCLUDED_IDS]
    selected_specs = [
        spec
        for spec in [*active_specs, *CURATED_TURKEY_SPECS]
        if spec["id"] not in TURKEY_EXCLUDED_IDS
    ]
    records = [make_record(spec) for spec in selected_specs]
    upsert_country("cekya.json", "Czechia", [r for r in records if r["country"] == "Czechia"])
    upsert_country("yunanistan.json", "Greece", [r for r in records if r["country"] == "Greece"])
    upsert_country(
        "turkiye.json",
        "Turkey",
        [r for r in records if r["country"] == "Turkey"],
        remove_ids=TURKEY_EXCLUDED_IDS,
    )
    for record in records:
        print(record["id"], record["data_quality"]["status"], record["data_quality"]["unverified_critical_fields"])


if __name__ == "__main__":
    main()
