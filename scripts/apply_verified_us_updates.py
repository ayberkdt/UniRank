"""Apply two source-checked United States programme updates.

This is intentionally a narrow, repeatable data migration.  It replaces
legacy estimates and unsourced claims only for the two records below.  The
subsequent audit is responsible for making remaining uncertainty visible.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data_base" / "amerika.json"
CHECKED = "2026-07-14"


def bilingual(en: str, tr: str) -> dict[str, str]:
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
        "title": title,
        "source_type": source_type,
        "access_status": access_status,
        "last_checked": CHECKED,
        "relevant_fields": fields,
        "confidence": confidence,
        "notes": bilingual(notes_en, notes_tr),
    }


def find_record(rows: list[dict[str, Any]], record_id: str) -> dict[str, Any]:
    for row in rows:
        if row.get("id") == record_id:
            return row
    raise KeyError(f"{record_id} not found")


def set_source_profile(record: dict[str, Any], *, primary: str, secondary: list[str], logs: list[dict[str, Any]], confidence: dict[str, str], notes_en: str, notes_tr: str) -> None:
    record["source_profile"] = {
        "primary_url": primary,
        "secondary_urls": secondary,
        "last_verified": CHECKED,
        "field_confidence": confidence,
        "source_reliability": "high",
        "verification_status": "partially_verified",
        "needs_verification": True,
        "verification_notes": bilingual(notes_en, notes_tr),
        "source_log": logs,
    }


def write(rows: list[dict[str, Any]], original: str) -> None:
    match = re.search(r"^\s*\[\r?\n( +)\{", original)
    indent = len(match.group(1)) if match else 4
    newline = "\r\n" if "\r\n" in original else "\n"
    serialised = json.dumps(rows, ensure_ascii=False, indent=indent)
    PATH.write_bytes((serialised.replace("\n", newline) + newline).encode("utf-8"))


def update_virginia_tech(record: dict[str, Any]) -> None:
    program_url = "https://www.aoe.vt.edu/graduate/degrees-and-certificates/master-of-science.html"
    curriculum_url = "https://www.aoe.vt.edu/graduate/courses.html"
    coa_url = "https://finaid.vt.edu/content/dam/finaid_vt_edu/Cost_of_Attendance/2627/GRNR_0.pdf"
    admission_url = "https://www.aoe.vt.edu/graduate/graduate-admissions.html"
    funding_url = "https://www.aoe.vt.edu/graduate/fellowships-and-assistantships.html"
    deadline_url = "https://graduateschool.vt.edu/admissions/how-to-apply/deadlines.html"

    record.update({
        "program_name": "Master of Science in Aerospace Engineering",
        "program_native_name": "Master of Science in Aerospace Engineering",
        "program_degree": "M.S.",
        "degree_level": "Master",
        "duration_years": None,
        "ects": None,
        "teaching_language": [],
        "program_url": program_url,
        "program_status": "active",
        "relevance_status": "highly_relevant",
        "eligibility_profile": {
            "eligible_for_non_eu": True,
            "required_previous_degree": None,
            "required_ects": {},
            "minimum_gpa": None,
            "admission_mode": "Graduate School application with department review",
            "admission_risk": "high",
            "accepted_backgrounds": [],
            "required_documents": [],
            "verification_notes": bilingual(
                "The checked AOE and Graduate School pages document the graduate application route and international deadlines. A programme-specific list of prior-degree and document requirements was not captured in this update.",
                "Kontrol edilen AOE ve Graduate School sayfaları lisansüstü başvuru yolunu ve uluslararası son tarihleri belgeliyor. Programa özgü önceki derece ve belge listesinin tamamı bu güncellemede doğrulanmadı.",
            ),
        },
        "language_profile": {
            "teaching_language": [],
            "english_required": None,
            "english_level_required": None,
            "mixed_language_warning": None,
            "language_risk": "unknown",
            "verification_notes": bilingual(
                "The checked official sources do not explicitly label the programme teaching language, so it is not inferred from the English-language website.",
                "Kontrol edilen resmî kaynaklar programın eğitim dilini açıkça etiketlemiyor; bu nedenle İngilizce web sitesinden çıkarım yapılmıyor.",
            ),
        },
        "cost_profile": {
            "academic_year": "2026/2027",
            "tuition_eur_per_year_min": None,
            "tuition_eur_per_year_max": None,
            "tuition_eur_per_year_estimated": None,
            "tuition_basis": "official_published_currency",
            "tuition_usd_per_year": 33582,
            "mandatory_fees_usd_per_year": 3754,
            "total_cost_of_attendance_usd_per_year": 62770,
            "non_eu_flat_fee": None,
            "regional_tax_eur": None,
            "student_union_fee_eur": None,
            "living_cost_eur_per_month": None,
            "total_first_year_cost_eur": None,
            "scholarship_availability": "competitive_assistantships",
            "scholarship_risk": "high",
            "source_notes": bilingual(
                "Virginia Tech's 2026–27 non-resident graduate cost-of-attendance PDF lists USD 33,582 tuition, USD 3,754 fees and USD 62,770 total annual cost of attendance. These are published USD budget figures, not an EUR conversion or a programme invoice.",
                "Virginia Tech'in 2026–27 eyalet dışı lisansüstü maliyet-belgesi 33.582 USD öğrenim ücreti, 3.754 USD harç ve 62.770 USD toplam yıllık devam maliyeti listeler. Bunlar EUR dönüşümü veya program faturası değil, yayımlanmış USD bütçe değerleridir.",
            ),
            "verification_notes": bilingual(
                "The old unsupported EUR estimate was removed. The PDF's USD 13,330 housing allowance is recorded as a housing budget below, not as a citywide rent quote.",
                "Önceki kaynaksız EUR tahmini kaldırıldı. PDF'deki 13.330 USD konut payı, şehir geneli kira teklifi olarak değil aşağıda konut bütçesi olarak kaydedildi.",
            ),
        },
        "scholarship_profile": {
            "available_types": ["graduate_research_assistantship", "graduate_teaching_assistantship", "fellowship"],
            "non_eu_eligible": None,
            "details": [],
            "external_options": [],
            "funding_notes": bilingual(
                "AOE says GRA support depends on a faculty member's research funding and GTA positions are limited. The department gives December 30 (fall) and September 1 (spring) as funding-consideration dates; neither is a funding guarantee or a confirmed programme admission deadline.",
                "AOE, GRA desteğinin öğretim üyesinin araştırma fonuna bağlı olduğunu ve GTA pozisyonlarının sınırlı olduğunu belirtir. Bölüm finansman değerlendirmesi için 30 Aralık (güz) ve 1 Eylül (bahar) tarihlerini verir; bunların hiçbiri finansman garantisi veya doğrulanmış program kabul son tarihi değildir.",
            ),
            "verification_notes": bilingual(
                "International eligibility for a particular assistantship or fellowship was not explicitly verified.",
                "Belirli bir asistanlık veya fellowship için uluslararası uygunluk açıkça doğrulanmadı.",
            ),
        },
        "living_profile": {
            "city_type": "small_town",
            "housing_search_difficulty": "unknown",
            "housing_cost_range_eur": None,
            "housing_budget_usd_per_year": 13330,
            "student_dorm_availability": "unknown",
            "living_cost_risk": "unknown",
            "housing_notes": bilingual(
                "The official 2026–27 non-resident graduate cost-of-attendance budget allocates USD 13,330 to housing. It is a budget allowance, not a room-rent range or a guarantee of availability.",
                "Resmî 2026–27 eyalet dışı lisansüstü devam maliyeti bütçesi konut için 13.330 USD ayırır. Bu bir bütçe payıdır; oda kira aralığı veya yer garantisi değildir.",
            ),
            "verification_notes": bilingual(
                "No comparable official housing availability or rent-range source was verified in this update.",
                "Bu güncellemede karşılaştırılabilir resmî konut müsaitliği veya kira aralığı kaynağı doğrulanmadı.",
            ),
        },
        "curriculum_profile": {
            "structure": "M.S. thesis or non-thesis option; both options include a final comprehensive oral examination.",
            "specializations": ["aerodynamics", "guidance_navigation_control", "structures"],
            "notable_courses": ["high_speed_aerodynamics", "vehicle_propulsion", "orbital_mechanics", "computational_fluid_dynamics", "vehicle_dynamics_and_control", "aeroelasticity"],
            "mandatory_internship": None,
            "thesis_type": "Thesis or non-thesis option",
            "flexibility": "specialization-based",
            "curriculum_risk": "low",
            "verification_notes": bilingual(
                "The official degree page lists aero-hydrodynamics, dynamics and control, and structures/structural dynamics. The current AOE course list includes high-speed aerodynamics, propulsion, orbital mechanics, computational fluid dynamics, dynamics/control and aeroelasticity; availability varies by term.",
                "Resmî derece sayfası aero-hidrodinamik, dinamik ve kontrol ile yapılar/yapısal dinamiği listeler. Güncel AOE ders listesi yüksek hızlı aerodinamik, itki, yörünge mekaniği, hesaplamalı akışkanlar dinamiği, dinamik/kontrol ve aeroelastisiteyi içerir; ders açılması döneme göre değişir.",
            ),
        },
        "category_profile": {
            "primary_categories": ["aerospace_general"],
            "secondary_categories": ["aerodynamics", "guidance_navigation_control", "structures", "propulsion", "orbital_mechanics", "computational_fluid_dynamics"],
            "technical_focus": bilingual(
                "Aerodynamics, GNC, structures, propulsion, orbital mechanics and CFD",
                "Aerodinamik, GNC, yapılar, itki, yörünge mekaniği ve HAD",
            ),
            "verification_notes": bilingual(
                "Categories are normalized from the checked specializations and course list.",
                "Kategoriler, kontrol edilen uzmanlaşmalardan ve ders listesinden normalize edildi.",
            ),
        },
        "research_profile": {
            "research_focus_areas": ["aero-hydrodynamics", "dynamics_and_control", "structures_and_structural_dynamics", "space_engineering"],
            "key_institutes": [],
            "research_funding_level": "unknown",
            "research_risk": "unknown",
            "verification_notes": bilingual(
                "The official MS page describes hands-on research across aero-hydrodynamics, dynamics/control, structures, space engineering and related areas. Specific lab funding and industry-project availability were not assessed here.",
                "Resmî MS sayfası aero-hidrodinamik, dinamik/kontrol, yapılar, uzay mühendisliği ve ilgili alanlarda uygulamalı araştırmayı açıklar. Belirli laboratuvar fonları ve sanayi projesi imkânları burada değerlendirilmedi.",
            ),
        },
        "industry_ecosystem_profile": {
            "local_industry_strength": "unknown",
            "key_companies": [],
            "hiring_culture": "unknown",
            "alumni_presence": "unknown",
            "industry_risk": "International students should independently check export-control and work-authorization constraints for each opportunity.",
            "verification_notes": bilingual(
                "Earlier company-partnership claims were not retained because this update did not verify an official partnership source.",
                "Bu güncellemede resmî ortaklık kaynağı doğrulanmadığı için önceki şirket-ortaklık iddiaları tutulmadı.",
            ),
        },
        "application_timeline_profile": {
            "application_period": "Fall or spring",
            "pre_enrollment_required": None,
            "visa_complexity": "high",
            "deadline_eu": None,
            "deadline_non_eu": "May 15 (fall); October 15 (spring)",
            "timeline_risk": "medium",
            "verification_notes": bilingual(
                "Virginia Tech Graduate School publishes May 15 for fall and October 15 for spring for international applicants. Confirm the target intake because departmental and funding dates are separate.",
                "Virginia Tech Graduate School, uluslararası adaylar için güz dönemi 15 Mayıs ve bahar dönemi 15 Ekim tarihlerini yayımlar. Bölüm ve finansman tarihleri ayrı olduğundan hedef dönemi mutlaka doğrulayın.",
            ),
        },
        "student_sentiment_profile": {
            "student_satisfaction_score": None,
            "workload_sentiment": "unknown",
            "teaching_quality_sentiment": "unknown",
            "administration_sentiment": "unknown",
            "housing_sentiment": "unknown",
            "city_life_sentiment": "unknown",
            "international_student_sentiment": "unknown",
            "career_support_sentiment": "unknown",
            "student_sentiment_summary": None,
            "student_sentiment_sources": [],
            "sentiment_confidence": "unknown",
            "verification_notes": bilingual(
                "No dated, sufficiently broad independent student-sentiment sample was verified in this update.",
                "Bu güncellemede tarihli ve yeterince geniş bağımsız öğrenci görüşü örneklemi doğrulanmadı.",
            ),
        },
        "decision_summary": {
            "pros": [
                bilingual("Dedicated active Aerospace Engineering M.S. with thesis and non-thesis routes.", "Tezli ve tezsiz yolları olan, aktif ve doğrudan Aerospace Engineering M.S."),
                bilingual("Official course list gives concrete options in high-speed aerodynamics, propulsion, orbital mechanics, CFD, controls and aeroelasticity.", "Resmî ders listesi yüksek hızlı aerodinamik, itki, yörünge mekaniği, HAD, kontrol ve aeroelastisite için somut seçenekler sunar."),
                bilingual("Published 2026–27 non-resident USD tuition, fees, total budget and housing allowance support transparent cost planning.", "Yayımlanmış 2026–27 eyalet dışı USD öğrenim ücreti, harç, toplam bütçe ve konut payı şeffaf maliyet planlamasını destekler."),
            ],
            "cons": [
                bilingual("The checked sources do not explicitly state the teaching language or a programme-specific prior-degree/document checklist.", "Kontrol edilen kaynaklar eğitim dilini veya programa özgü önceki derece/belge listesini açıkça belirtmez."),
                bilingual("Assistantships are competitive and faculty/position dependent; no individual funding guarantee or international eligibility statement is assumed.", "Asistanlıklar rekabetçidir; öğretim üyesi/pozisyon koşullarına bağlıdır. Bireysel finansman garantisi veya uluslararası uygunluk varsayılmaz."),
            ],
            "verdict": bilingual(
                "A well-documented aerospace MS for aerodynamics, controls, structures, propulsion and space-adjacent coursework; confirm language, admissions fit and funding before applying.",
                "Aerodinamik, kontrol, yapılar, itki ve uzay bağlantılı dersler için iyi belgelenmiş bir aerospace MS; başvuru öncesi eğitim dili, kabul uyumu ve finansmanı doğrulayın.",
            ),
        },
    })
    set_source_profile(
        record,
        primary=program_url,
        secondary=[curriculum_url, coa_url, admission_url, funding_url, deadline_url],
        confidence={"program_basic_info": "high", "admission": "high", "deadlines": "high", "curriculum": "high", "tuition": "high", "scholarship": "high", "housing": "high", "language": "unknown", "sentiment": "unknown"},
        notes_en="Official programme, course, financial-aid, graduate-admission, funding and deadline pages were checked. Teaching language and detailed programme-specific admissions requirements are intentionally left unknown where the checked pages do not state them.",
        notes_tr="Resmî program, ders, mali yardım, lisansüstü kabul, finansman ve son tarih sayfaları kontrol edildi. Kontrol edilen sayfaların belirtmediği eğitim dili ve ayrıntılı programa özgü kabul şartları bilinmiyor olarak bırakıldı.",
        logs=[
            source(program_url, "Virginia Tech Master of Science in Aerospace or Ocean Engineering", "official_program_page", ["program", "curriculum"], "Confirms the active MS, aerospace specializations, thesis/non-thesis routes and final oral examination.", "Aktif MS'i, aerospace uzmanlaşmalarını, tezli/tezsiz yolları ve final sözlü sınavını doğrular."),
            source(curriculum_url, "Virginia Tech AOE Graduate Courses", "official_curriculum_page", ["curriculum"], "Lists graduate AOE courses including high-speed aerodynamics, propulsion, orbital mechanics, CFD, controls and aeroelasticity.", "Yüksek hızlı aerodinamik, itki, yörünge mekaniği, HAD, kontrol ve aeroelastisite dâhil AOE lisansüstü derslerini listeler."),
            source(coa_url, "Virginia Tech 2026–27 Nonresident Graduate Cost of Attendance", "official_tuition_page", ["tuition", "housing"], "Published 2026–27 nonresident graduate tuition, fees, total cost of attendance and housing allowance.", "Yayımlanmış 2026–27 eyalet dışı lisansüstü öğrenim ücreti, harç, toplam devam maliyeti ve konut payı.", access_status="pdf"),
            source(admission_url, "Virginia Tech AOE Graduate Admissions", "official_admission_page", ["admission", "scholarship"], "Documents AOE graduate application and funding-consideration context.", "AOE lisansüstü başvurusunu ve finansman değerlendirmesi bağlamını belgeler."),
            source(funding_url, "Virginia Tech AOE Financial Support", "official_scholarship_page", ["scholarship"], "Explains that GRA funding depends on faculty support and GTA positions are limited.", "GRA finansmanının öğretim üyesi desteğine bağlı olduğunu ve GTA pozisyonlarının sınırlı olduğunu açıklar."),
            source(deadline_url, "Virginia Tech Graduate School Deadlines", "official_admission_page", ["deadline", "non_eu"], "Lists international graduate application deadlines for fall and spring.", "Güz ve bahar için uluslararası lisansüstü başvuru son tarihlerini listeler."),
        ],
    )


def update_penn_state(record: dict[str, Any]) -> None:
    program_url = "https://www.aero.psu.edu/academics/graduate/degrees-and-requirements.aspx"
    bulletin_url = "https://bulletins.psu.edu/graduate/programs/majors/aerospace-engineering/"
    tuition_url = "https://tuition.psu.edu/rates-effective-2026-fall-semester"
    admission_url = "https://www.aero.psu.edu/academics/graduate/how-to-apply.aspx"
    funding_url = "https://www.aero.psu.edu/academics/graduate/funding-opportunities.aspx"
    housing_url = "https://liveon.psu.edu/university-park/rates"
    curriculum_url = "https://www.aero.psu.edu/academics/graduate/core-courses-graduate-program.aspx"

    record.update({
        "program_name": "Master of Science in Aerospace Engineering",
        "program_native_name": "Master of Science in Aerospace Engineering",
        "program_degree": "M.S.",
        "degree_level": "Master",
        "duration_years": 2,
        "ects": None,
        "teaching_language": [],
        "program_url": program_url,
        "program_status": "active",
        "relevance_status": "highly_relevant",
        "eligibility_profile": {
            "eligible_for_non_eu": True,
            "required_previous_degree": "Bachelor's degree in engineering, physical science, or mathematics",
            "required_ects": {},
            "minimum_gpa": 3.0,
            "admission_mode": "Department and Graduate School application",
            "admission_risk": "high",
            "accepted_backgrounds": ["engineering", "physical_science", "mathematics"],
            "required_documents": ["English-proficiency test evidence when required"],
            "verification_notes": bilingual(
                "Penn State's official bulletin requires a bachelor's in engineering, physical science or mathematics and says a 3.0 junior/senior GPA will be considered, subject to possible waivers. The programme application page publishes deadlines and a TOEFL iBT minimum (80 overall, 19 speaking); a fuller document checklist remains unverified here.",
                "Penn State'in resmî bülteni mühendislik, fiziksel bilim veya matematikte lisans derecesi ister ve olası muafiyetlerle 3,0 junior/senior GPA'nın değerlendirileceğini belirtir. Program başvuru sayfası son tarihleri ve TOEFL iBT alt sınırını (toplam 80, konuşma 19) yayımlar; daha kapsamlı belge listesi burada doğrulanmamıştır.",
            ),
        },
        "language_profile": {
            "teaching_language": [],
            "english_required": True,
            "english_level_required": "TOEFL iBT 80 overall; 19 speaking (when required)",
            "mixed_language_warning": None,
            "language_risk": "unknown",
            "verification_notes": bilingual(
                "The application page gives an English-proficiency threshold but the checked sources do not explicitly label the programme teaching language. Teaching language is therefore left unverified.",
                "Başvuru sayfası İngilizce yeterlilik eşiği verir; ancak kontrol edilen kaynaklar programın eğitim dilini açıkça etiketlemez. Bu nedenle eğitim dili doğrulanmamış bırakılır.",
            ),
        },
        "cost_profile": {
            "academic_year": "2026/2027",
            "tuition_eur_per_year_min": None,
            "tuition_eur_per_year_max": None,
            "tuition_eur_per_year_estimated": None,
            "tuition_basis": "official_published_currency",
            "tuition_usd_per_year": 50608,
            "non_eu_flat_fee": None,
            "regional_tax_eur": None,
            "student_union_fee_eur": None,
            "living_cost_eur_per_month": None,
            "total_first_year_cost_eur": None,
            "scholarship_availability": "competitive_assistantships_and_amp",
            "scholarship_risk": "high",
            "source_notes": bilingual(
                "Penn State's 2026–27 University Park rate page lists USD 50,608 annual tuition for full-time nonresident graduate Engineering. It is a published tuition figure in USD, not an EUR conversion or a funding-adjusted personal bill.",
                "Penn State'in 2026–27 University Park ücret sayfası, tam zamanlı eyalet dışı lisansüstü Engineering için yıllık 50.608 USD öğrenim ücreti listeler. Bu, EUR dönüşümü veya finansmana göre düzeltilmiş kişisel fatura değil, USD cinsinden yayımlanmış öğrenim ücretidir.",
            ),
            "verification_notes": bilingual(
                "The old unsupported EUR estimate was removed. Fees and an all-in living budget were not asserted without a checked programme-relevant source.",
                "Önceki kaynaksız EUR tahmini kaldırıldı. Kontrol edilmiş programla ilgili kaynak olmadan harçlar ve toplam yaşam bütçesi iddia edilmedi.",
            ),
        },
        "scholarship_profile": {
            "available_types": ["research_assistantship", "teaching_assistantship", "graduate_assistantship", "aerospace_master_program_fellowship"],
            "non_eu_eligible": None,
            "details": [],
            "external_options": [],
            "funding_notes": bilingual(
                "The department describes competitive RA, TA and GA appointments that can include stipend, tuition remission and insurance. Its Aerospace Master Program Fellowship is described as up to USD 10,000 per year for up to two years for selected students; eligibility and award decisions must be checked for the individual applicant.",
                "Bölüm, maaş, öğrenim ücreti muafiyeti ve sigorta içerebilen rekabetçi RA, TA ve GA atamalarını açıklar. Aerospace Master Program Fellowship, seçilmiş öğrenciler için iki yıla kadar yılda en fazla 10.000 USD olarak tanımlanır; bireysel aday için uygunluk ve ödül kararı doğrulanmalıdır.",
            ),
            "verification_notes": bilingual(
                "No assistantship or fellowship is treated as guaranteed, and no blanket non-EU eligibility is inferred.",
                "Hiçbir asistanlık veya fellowship garantili sayılmaz; genel bir AB dışı uygunluk çıkarımı yapılmaz.",
            ),
        },
        "living_profile": {
            "city_type": "small_city",
            "housing_search_difficulty": "unknown",
            "housing_cost_range_eur": None,
            "average_room_rent_usd_per_month_min": 1168,
            "average_room_rent_usd_per_month_max": 1168,
            "student_dorm_availability": "available_limited",
            "living_cost_risk": "unknown",
            "housing_notes": bilingual(
                "Penn State's University Park housing rate page lists USD 1,168/month for a White Course unfurnished one-bedroom graduate/family apartment. This is a specific on-campus unit rate, not a shared-room price or an off-campus market average.",
                "Penn State'in University Park konut ücret sayfası, White Course mobilyasız tek yatak odalı lisansüstü/aile dairesi için aylık 1.168 USD listeler. Bu, belirli bir kampüs içi birim ücretidir; paylaşımlı oda fiyatı veya kampüs dışı piyasa ortalaması değildir.",
            ),
            "verification_notes": bilingual(
                "Availability and housing-search difficulty were not quantified by a comparable checked source.",
                "Müsaitlik ve konut arama zorluğu karşılaştırılabilir kontrol edilmiş bir kaynakla ölçülmedi.",
            ),
        },
        "curriculum_profile": {
            "structure": "Thesis-based M.S.; 32 credits including 9 credits of basic field theory, 3 credits of applied mathematics, 2 credits of AERSP 590 colloquium and 6 thesis-research credits.",
            "specializations": ["aerodynamics", "guidance_navigation_control", "structures", "applied_mathematics"],
            "core_courses": ["fluid_mechanics", "dynamics_and_control", "solid_mechanics", "applied_mathematics"],
            "mandatory_internship": None,
            "thesis_type": "Thesis-based M.S.",
            "flexibility": "core-and-thesis",
            "curriculum_risk": "low",
            "verification_notes": bilingual(
                "The official programme page describes a thesis-based MS designed for two years. Penn State's current official bulletin sets the MS at 32 credits, including basic field theory, applied mathematics, AERSP 590 colloquium and six thesis-research credits; the thesis and public presentation are required.",
                "Resmî program sayfası iki yıl için tasarlanmış tez temelli MS'i açıklar. Penn State'in güncel resmî bülteni MS'i, temel alan kuramı, uygulamalı matematik, AERSP 590 kolokyumu ve altı tez araştırması kredisi dâhil 32 kredi olarak belirler; tez ve herkese açık sunum zorunludur.",
            ),
        },
        "category_profile": {
            "primary_categories": ["aerospace_general"],
            "secondary_categories": ["aerodynamics", "guidance_navigation_control", "structures", "applied_mathematics"],
            "technical_focus": bilingual("Aerodynamics, GNC, structures and applied mathematics", "Aerodinamik, GNC, yapılar ve uygulamalı matematik"),
            "verification_notes": bilingual("Categories are normalized from the checked core-course areas.", "Kategoriler kontrol edilen çekirdek ders alanlarından normalize edildi."),
        },
        "research_profile": {
            "research_focus_areas": ["aerodynamics", "dynamics_and_control", "solid_mechanics", "applied_mathematics"],
            "key_institutes": [],
            "research_funding_level": "unknown",
            "research_risk": "unknown",
            "verification_notes": bilingual(
                "The source-backed profile reflects the programme's degree and core-course areas. Specific centre, company and lab claims were not retained without dedicated official evidence.",
                "Kaynak destekli profil programın derece ve çekirdek ders alanlarını yansıtır. Belirli merkez, şirket ve laboratuvar iddiaları özel resmî kanıt olmadan tutulmadı.",
            ),
        },
        "industry_ecosystem_profile": {
            "local_industry_strength": "unknown",
            "key_companies": [],
            "hiring_culture": "unknown",
            "alumni_presence": "unknown",
            "industry_risk": "International students should independently check export-control and work-authorization constraints for each opportunity.",
            "verification_notes": bilingual(
                "Earlier company-partnership claims were removed because this update did not verify an official partnership source.",
                "Bu güncellemede resmî ortaklık kaynağı doğrulanmadığı için önceki şirket-ortaklık iddiaları kaldırıldı.",
            ),
        },
        "application_timeline_profile": {
            "application_period": "Fall or spring",
            "pre_enrollment_required": None,
            "visa_complexity": "high",
            "deadline_eu": None,
            "deadline_non_eu": "December 15 (fall); August 15 (spring)",
            "timeline_risk": "medium",
            "verification_notes": bilingual(
                "The programme's official application page lists December 15 for fall and August 15 for spring. Check the target cycle before submitting because annual admissions guidance can change.",
                "Programın resmî başvuru sayfası güz için 15 Aralık, bahar için 15 Ağustos listeler. Yıllık kabul rehberi değişebileceği için başvurmadan önce hedef dönemi kontrol edin.",
            ),
        },
        "student_sentiment_profile": {
            "student_satisfaction_score": None,
            "workload_sentiment": "unknown",
            "teaching_quality_sentiment": "unknown",
            "administration_sentiment": "unknown",
            "housing_sentiment": "unknown",
            "city_life_sentiment": "unknown",
            "international_student_sentiment": "unknown",
            "career_support_sentiment": "unknown",
            "student_sentiment_summary": None,
            "student_sentiment_sources": [],
            "sentiment_confidence": "unknown",
            "verification_notes": bilingual("No dated, sufficiently broad independent student-sentiment sample was verified in this update.", "Bu güncellemede tarihli ve yeterince geniş bağımsız öğrenci görüşü örneklemi doğrulanmadı."),
        },
        "decision_summary": {
            "pros": [
                bilingual("Active two-year, thesis-based Aerospace Engineering MS with core work in fluids, controls, solid mechanics and applied mathematics.", "Akışkanlar, kontrol, katı mekaniği ve uygulamalı matematik çekirdeği olan aktif, iki yıllık, tez temelli Aerospace Engineering MS."),
                bilingual("Published 2026–27 University Park nonresident Engineering tuition and a concrete graduate/family on-campus housing rate improve cost planning.", "Yayımlanmış 2026–27 University Park eyalet dışı Engineering öğrenim ücreti ve somut lisansüstü/aile kampüs içi konut ücreti maliyet planlamasını iyileştirir."),
                bilingual("Officially described competitive RA/TA/GA routes and the Aerospace Master Program Fellowship provide funding avenues without being treated as guarantees.", "Resmî olarak tanımlanan rekabetçi RA/TA/GA yolları ve Aerospace Master Program Fellowship, garanti sayılmadan finansman seçenekleri sunar."),
            ],
            "cons": [
                bilingual("The checked sources do not explicitly label the teaching language or fully document programme-specific degree-background requirements.", "Kontrol edilen kaynaklar eğitim dilini açıkça etiketlemez veya programa özgü derece altyapısı şartlarını tam belgelemez."),
                bilingual("Funding is competitive; individual international eligibility and an award offer must be confirmed before budgeting.", "Finansman rekabetçidir; bireysel uluslararası uygunluk ve ödül teklifi bütçe yapmadan önce doğrulanmalıdır."),
            ],
            "verdict": bilingual(
                "A source-backed thesis MSc for aerodynamics, GNC and structures, with transparent published tuition; validate language, eligibility and funding at application time.",
                "Aerodinamik, GNC ve yapılar için kaynak destekli tezli bir MSc; yayımlanmış öğrenim ücreti şeffaftır. Başvuru sırasında eğitim dili, uygunluk ve finansmanı doğrulayın.",
            ),
        },
    })
    set_source_profile(
        record,
        primary=program_url,
        secondary=[bulletin_url, tuition_url, admission_url, funding_url, housing_url, curriculum_url],
        confidence={"program_basic_info": "high", "admission": "high", "deadlines": "high", "curriculum": "high", "tuition": "high", "scholarship": "high", "housing": "high", "language": "unknown", "sentiment": "unknown"},
        notes_en="Official programme, tuition, application, funding, housing and core-course pages were checked. Teaching language and programme-specific prior-degree requirements are left unknown where the checked pages do not state them.",
        notes_tr="Resmî program, öğrenim ücreti, başvuru, finansman, konut ve çekirdek ders sayfaları kontrol edildi. Kontrol edilen sayfaların belirtmediği eğitim dili ve programa özgü önceki derece şartları bilinmiyor olarak bırakıldı.",
        logs=[
            source(program_url, "Penn State Aerospace Engineering Graduate Degrees and Requirements", "official_program_page", ["program", "curriculum"], "Confirms the active thesis-based Aerospace Engineering MS and its intended two-year duration.", "Aktif tez temelli Aerospace Engineering MS'i ve hedeflenen iki yıllık süresini doğrular."),
            source(bulletin_url, "Penn State Graduate Bulletin: Aerospace Engineering", "official_program_page", ["program", "admission", "curriculum"], "Official bulletin gives MS admission backgrounds/GPA and current 32-credit thesis-MS requirements.", "Resmî bülten MS kabul altyapısı/GPA'sını ve güncel 32 kredilik tezli MS şartlarını verir."),
            source(tuition_url, "Penn State University Park Tuition Rates Effective Fall 2026", "official_tuition_page", ["tuition"], "Lists annual full-time nonresident graduate Engineering tuition for 2026–27.", "2026–27 için tam zamanlı eyalet dışı lisansüstü Engineering yıllık öğrenim ücretini listeler."),
            source(admission_url, "Penn State Aerospace Engineering Graduate Application Process", "official_admission_page", ["admission", "deadline", "non_eu"], "Lists fall and spring application deadlines and English-proficiency information.", "Güz ve bahar başvuru son tarihlerini ve İngilizce yeterlilik bilgisini listeler."),
            source(funding_url, "Penn State Aerospace Engineering Graduate Funding Opportunities", "official_scholarship_page", ["scholarship"], "Documents competitive assistantship and Aerospace Master Program Fellowship routes.", "Rekabetçi asistanlık ve Aerospace Master Program Fellowship yollarını belgeler."),
            source(housing_url, "Penn State University Park Housing Rates", "official_housing_page", ["housing"], "Lists the White Course graduate/family apartment rate used in this record.", "Bu kayıtta kullanılan White Course lisansüstü/aile dairesi ücretini listeler."),
            source(curriculum_url, "Penn State Aerospace Engineering Graduate Core Courses", "official_curriculum_page", ["curriculum"], "Identifies the programme's graduate core-course areas.", "Programın lisansüstü çekirdek ders alanlarını belirtir."),
        ],
    )


def update_mit_language(record: dict[str, Any]) -> None:
    """Add MIT's Institute-wide explicit teaching-language statement."""
    language_url = "https://oge.mit.edu/graduate-admissions/applications/international-applicants/"
    record["teaching_language"] = ["English"]
    profile = record.setdefault("language_profile", {})
    profile.update({
        "teaching_language": ["English"],
        "english_required": True,
        "language_risk": "low",
        "verification_notes": bilingual(
            "MIT's Office of Graduate Education explicitly states that English is the language of instruction in all subjects within the Institute. Its English-proficiency policy applies to international graduate applicants.",
            "MIT Office of Graduate Education, Enstitüdeki tüm derslerin eğitim dilinin İngilizce olduğunu açıkça belirtir. İngilizce yeterlilik politikası uluslararası lisansüstü adaylara uygulanır.",
        ),
    })
    source_profile = record.setdefault("source_profile", {})
    logs = [item for item in source_profile.get("source_log", []) if isinstance(item, dict)]
    logs = [
        item for item in logs
        if not (item.get("url") == language_url and item.get("source_type") == "official_admission_page")
    ]
    logs.append(source(
        language_url,
        "MIT Office of Graduate Education: International Applicants",
        "official_admission_page",
        ["language", "admission", "non_eu"],
        "Explicitly states that English is the language of instruction in all MIT subjects and gives international graduate English-proficiency requirements.",
        "MIT'teki tüm derslerin eğitim dilinin İngilizce olduğunu açıkça belirtir ve uluslararası lisansüstü İngilizce yeterlilik şartlarını verir.",
    ))
    source_profile["source_log"] = logs
    source_profile.setdefault("field_confidence", {})["language"] = "high"
    source_profile["last_verified"] = CHECKED


def main() -> None:
    original = PATH.read_bytes().decode("utf-8")
    rows = json.loads(original)
    update_virginia_tech(find_record(rows, "virginia-tech-aoe"))
    update_penn_state(find_record(rows, "penn-state-aero"))
    update_mit_language(find_record(rows, "mit-aeroastro"))
    write(rows, original)
    print("Updated Virginia Tech and Penn State from checked official sources.")


if __name__ == "__main__":
    main()
