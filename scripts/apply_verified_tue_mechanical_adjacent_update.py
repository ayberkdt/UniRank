"""Apply source-grounded TU/e Mechanical Engineering adjacent-aerospace data."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from unirank.core.integrity import audit_record


DATA_PATH = ROOT / "data_base" / "hollanda.json"
RECORD_ID = "netherlands_tue_msc_mechanical_systems_control"
CHECKED = "2026-08-14"
PROGRAM_URL = "https://www.tue.nl/en/education/graduate-school/master-mechanical-engineering"
STUDY_NL_URL = "https://www.studyinnl.org/dutch-education/studies/mechanical-engineering-857-eindhoven-university-of-technology"
LIVING_URL = "https://www.studyinnl.org/finances/daily-student-expenses-and-cost-of-living-in-the-netherlands"
VESTIDE_URL = "https://rooms.vestide.nl/en/find-room/detail-accommodation/?detailId=13408"
DEPARTMENT_URL = "https://research.tue.nl/en/organisations/mechanical-engineering"
AEROSPACE_URL = "https://research.tue.nl/en/impacts/aerospace/"
HOFMAN_URL = "https://research.tue.nl/en/organisations/group-hofman/"
OOMEN_URL = "https://research.tue.nl/en/organisations/group-oomen/"
THESIS_URL = "https://research.tue.nl/en/organisations/autonomous-and-complex-systems/studentTheses/"
TUITION_CONTEXT_URL = "https://www.cursor.tue.nl/en/news/jaarmap-om-te-kopieren/januari/week-1-2-1/university-fund-launches-crowdfunding-for-students-in-need"
HOUSING_CONTEXT_URL = "https://www.cursor.tue.nl/en/background/2025/april/week-2/full-speed-ahead-on-recruiting-masters-students-beethoven"


def bi(en: str, tr: str) -> dict[str, str]:
    return {"en": en, "tr": tr}


def source(url: str, title: str, source_type: str, fields: list[str], note: str, confidence: str = "high", access_status: str = "ok") -> dict:
    return {
        "url": url,
        "title": title,
        "source_type": source_type,
        "access_status": access_status,
        "last_checked": CHECKED,
        "relevant_fields": fields,
        "confidence": confidence,
        "notes": bi(note, "Kaynak, belirtilen alanlar ve kapsam sÄ±nÄ±rlarÄ± iÃ§in kontrol edildi."),
    }


def main() -> None:
    payload = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    matches = [row for row in payload["programs"] if row.get("id") == RECORD_ID]
    if len(matches) != 1:
        raise RuntimeError(f"Expected one {RECORD_ID!r} record; found {len(matches)}")
    row = matches[0]

    row.update(
        {
            "program_name": "MSc Mechanical Engineering",
            "program_degree": "Master of Science",
            "duration_years": 2,
            "ects": 120,
            "teaching_language": ["English"],
            "program_url": PROGRAM_URL,
            "program_status": "active",
            "relevance_status": "weak",
            "programme_fit_class": "adjacent_mechanical_degree_with_aerospace_applications_not_aerospace_or_space_degree",
        }
    )

    row["eligibility_profile"].update(
        {
            "eligible_for_non_eu": True,
            "required_previous_degree": None,
            "accepted_backgrounds": [],
            "minimum_gpa": None,
            "ranking_or_selection": None,
            "admission_mode": "needs_official_programme_specific_check",
            "admission_risk": "unknown",
            "required_documents": [],
            "motivation_letter_required": None,
            "cv_required": None,
            "recommendation_required": None,
            "interview_required": None,
            "test_required": None,
            "notes_for_turkish_students": bi(
                "The current national catalogue publishes a non-EU application route but says programme admission requirements are unavailable. Do not infer Turkish degree equivalence, GPA, documents or GRE rules from scholarship pages.",
                "GÃ¼ncel ulusal katalog AB dÄ±ÅŸÄ± baÅŸvuru rotasÄ±nÄ± yayÄ±mlar ancak program kabul koÅŸullarÄ±nÄ± 'mevcut deÄŸil' gÃ¶sterir. TÃ¼rk diploma denkliÄŸi, GPA, belgeler veya GRE kurallarÄ±nÄ± burs sayfalarÄ±ndan Ã§Ä±karmayÄ±n.",
            ),
            "verification_notes": bi(
                "Non-EU application is explicitly supported by the official national catalogue. Academic prerequisite, equivalency and document details remain unknown because the linked TU/e admission page blocked research access and the catalogue does not reproduce them.",
                "AB dÄ±ÅŸÄ± baÅŸvuru resmÃ® ulusal katalogda aÃ§Ä±kÃ§a desteklenir. BaÄŸlÄ± TU/e kabul sayfasÄ± araÅŸtÄ±rma eriÅŸimini engellediÄŸi ve katalog bunlarÄ± aktarmadÄ±ÄŸÄ± iÃ§in akademik Ã¶nkoÅŸul, denklik ve belge ayrÄ±ntÄ±larÄ± bilinmiyor.",
            ),
            "gre": {
                "policy": "unknown_not_published_in_accessible_checked_requirements",
                "test_type": "unknown",
                "minimum_scores": {},
                "recommended_scores": {},
                "validity_rule": "",
                "waiver_rules": [],
                "source_ids": [STUDY_NL_URL, PROGRAM_URL],
            },
        }
    )

    row["language_profile"].update(
        {
            "teaching_language": ["English"],
            "english_required": True,
            "english_level_required": "IELTS 6.5 overall; TOEFL iBT 90; Cambridge C1 Advanced or C2 Proficiency",
            "accepted_english_tests": ["IELTS Academic", "TOEFL iBT", "Cambridge C1 Advanced", "Cambridge C2 Proficiency"],
            "minimum_scores": {"ielts_academic": {"overall": 6.5}, "toefl_ibt": {"overall": 90}},
            "english_exemptions": [],
            "language_risk": "medium",
            "verification_notes": bi(
                "The current national programme catalogue publishes the overall IELTS and TOEFL thresholds and Cambridge levels. It does not publish component minima or exemptions, so none are inferred.",
                "GÃ¼ncel ulusal program kataloÄŸu toplam IELTS ve TOEFL eÅŸiklerini ve Cambridge dÃ¼zeylerini yayÄ±mlar. BÃ¶lÃ¼m alt puanlarÄ± veya muafiyetler yayÄ±mlanmadÄ±ÄŸÄ±ndan bunlar Ã§Ä±karÄ±lmaz.",
            ),
        }
    )

    row["cost_profile"].update(
        {
            "academic_year": "2026/2027",
            "tuition_eur_per_year_min": None,
            "tuition_eur_per_year_max": None,
            "tuition_eur_per_year_estimated": None,
            "non_eu_flat_fee": None,
            "tuition_basis": "current_official_national_catalogue_reports_non_eu_amount_unavailable",
            "eu_eea_statutory_tuition_eur_per_year": 2694,
            "historical_non_eu_master_tuition_reference": {"amount": 21000, "currency": "EUR", "academic_year": "2025/2026", "use_for_2026_27": False},
            "source_notes": bi(
                "Study in NL publishes EUR 2,694 for EU/EEA students in 2026/27 but explicitly shows the non-EU amount as unavailable. TU/e university media reports EUR 21,000 for non-EU master's students in 2025/26; it is retained only as historical context and is not rolled forward.",
                "Study in NL 2026/27 AB/AEA iÃ§in 2.694 EUR yayÄ±mlar ancak AB dÄ±ÅŸÄ± tutarÄ± aÃ§Ä±kÃ§a mevcut deÄŸil gÃ¶sterir. TU/e Ã¼niversite medyasÄ± 2025/26 AB dÄ±ÅŸÄ± yÃ¼ksek lisans iÃ§in 21.000 EUR bildirir; yalnÄ±zca tarihsel baÄŸlam olarak tutulur ve ileri taÅŸÄ±nmaz.",
            ),
            "verification_notes": bi(
                "The decision-critical 2026/27 non-EU tuition remains unknown; no estimate is stored.",
                "Karar-kritik 2026/27 AB dÄ±ÅŸÄ± Ã¶ÄŸrenim Ã¼creti bilinmiyor; tahmin tutulmaz.",
            ),
        }
    )

    row["scholarship_profile"].update(
        {
            "regional_scholarship_available": True,
            "regional_scholarship_name": "Amandus H. Lundqvist Scholarship Program / NL Scholarship",
            "non_eu_eligible": True,
            "scholarship_deadline": None,
            "scholarship_application_url": "https://www.tue.nl/en/education/become-a-tue-student/scholarships-and-grants",
            "application_mode": "unknown",
            "automatic_consideration": None,
            "separate_application_required": None,
            "opportunities": [
                {"name": "Amandus H. Lundqvist Scholarship Program", "current_programme_catalogue_listing": True, "application_mode": "needs_current_official_verification", "deadline": None, "award": None, "source_url": STUDY_NL_URL},
                {"name": "NL Scholarship", "current_programme_catalogue_listing": True, "non_eea_target_group": True, "application_mode": "needs_current_official_verification", "deadline": None, "award": None, "source_url": STUDY_NL_URL},
            ],
            "funding_notes": bi(
                "The current national programme catalogue lists both scholarships for this programme and states that the NL Scholarship targets non-EEA students. The linked TU/e scholarship pages blocked access, so old claims about a 1 February deadline, automatic consideration or award values are not treated as current facts.",
                "GÃ¼ncel ulusal program kataloÄŸu iki bursu da bu program iÃ§in listeler ve NL Scholarship'ın AB/AEA dÄ±ÅŸÄ± Ã¶ÄŸrencileri hedeflediÄŸini belirtir. BaÄŸlÄ± TU/e burs sayfalarÄ± eriÅŸimi engellediÄŸinden eski 1 Åžubat tarihi, otomatik deÄŸerlendirme veya Ã¶dÃ¼l tutarÄ± iddialarÄ± gÃ¼ncel gerÃ§ek kabul edilmez.",
            ),
            "verification_notes": bi(
                "Scholarship existence and non-EEA targeting are current; mechanics, amounts and deadline need direct TU/e confirmation.",
                "BurslarÄ±n varlÄ±ÄŸÄ± ve AB/AEA dÄ±ÅŸÄ± hedefi gÃ¼nceldir; sÃ¼reÃ§, tutar ve son tarih doÄŸrudan TU/e doÄŸrulamasÄ± gerektirir.",
            ),
        }
    )

    row["living_profile"].update(
        {
            "city_cost_level": "high_national_budget_reference",
            "monthly_living_cost_eur_min": 1000,
            "monthly_living_cost_eur_max": 1500,
            "monthly_living_cost_eur_estimated": None,
            "housing_difficulty": "high_no_guarantee",
            "housing_access": "not_guaranteed",
            "housing_access_notes": "Eligible international full-time TU/e-campus students can respond to designated Vestide listings; eligibility is not an allocation guarantee.",
            "housing_application_separate": True,
            "student_housing_available": True,
            "student_housing_competitiveness": "high",
            "living_risk": "high",
            "housing_guarantee": {"available": False, "basis": "no guarantee found; current Vestide listing requires a separate response and documentation"},
            "official_rent_items": [
                {"provider": "Vestide", "residence": "Haven, TU/e campus", "room_type": "furnished private room with shared facilities", "area_sqm": 14.9, "monthly_total_eur": 606.33, "basic_rent_eur": 364.23, "service_costs_eur": 152.21, "other_costs_eur": 89.89, "listing_date_context": "tenancy entered 2026-07-22", "source_url": VESTIDE_URL}
            ],
            "housing_notes": bi(
                "A current Vestide example was restricted to international full-time TU/e-campus students and required an admission/confirmation statement; international students receive priority for this room type, but applicants still had to respond to the listing. It is an example, not a guarantee or market average.",
                "GÃ¼ncel Vestide Ã¶rneÄŸi uluslararasÄ± tam zamanlÄ± TU/e kampÃ¼sÃ¼ Ã¶ÄŸrencileriyle sÄ±nÄ±rlÄ±ydÄ± ve kabul/onay belgesi istiyordu; bu oda tipinde uluslararasÄ±lara Ã¶ncelik vardÄ± ancak adayÄ±n ilana ayrÄ±ca yanÄ±t vermesi gerekiyordu. Bu bir Ã¶rnek olup garanti veya piyasa ortalamasÄ± deÄŸildir.",
            ),
            "verification_notes": bi(
                "The EUR 1,000-1,500 monthly budget is an official Netherlands-wide planning range, not an Eindhoven quote. TU/e university media still described housing as a major problem in 2025.",
                "AylÄ±k 1.000-1.500 EUR bÃ¼tÃ§e resmÃ® Hollanda geneli planlama aralÄ±ÄŸÄ±dÄ±r; Eindhoven fiyatÄ± deÄŸildir. TU/e Ã¼niversite medyasÄ± 2025'te konutu hÃ¢lÃ¢ bÃ¼yÃ¼k bir sorun olarak tanÄ±mlÄ±yordu.",
            ),
        }
    )

    row["curriculum_profile"].update(
        {
            "tracks": [],
            "research_clusters": ["Dynamical Systems Design", "Computational and Experimental Mechanics", "Thermo Fluids Engineering"],
            "specializations": [],
            "programme_structure": {"year_1": ["core programme", "specialization courses", "professional skills", "electives"], "year_2": ["internship", "graduation project"]},
            "mandatory_courses": [],
            "elective_courses": [],
            "exact_course_count": None,
            "thesis_required": True,
            "internship_required": True,
            "curriculum_url": STUDY_NL_URL,
            "verification_notes": bi(
                "The official national catalogue verifies the three clusters and broad two-year structure. It does not publish an exact course list or number, so the old nine-track list is removed rather than presented as a current study plan.",
                "ResmÃ® ulusal katalog Ã¼Ã§ kÃ¼meyi ve genel iki yÄ±llÄ±k yapÄ±yÄ± doÄŸrular. Kesin ders listesi veya sayÄ±sÄ± yayÄ±mlanmadÄ±ÄŸÄ±ndan eski dokuz iz listesi gÃ¼ncel plan gibi sunulmak yerine kaldÄ±rÄ±lÄ±r.",
            ),
        }
    )

    row["category_profile"].update(
        {
            "primary_categories": ["Mechanical Engineering"],
            "secondary_categories": ["Systems and Control", "Thermo Fluids", "Mechanics and Materials"],
            "normalized_tags": ["control_systems", "robotics", "mechatronics", "cfd", "thermofluids", "structures_materials"],
            "category_scores": {"aerospace_engineering": 45, "space_engineering": 15, "guidance_navigation_control": 60, "cfd_fluid_dynamics": 50, "structures_materials": 55, "propulsion": 25},
        }
    )

    row["research_profile"].update(
        {
            "department_research_areas": ["Computational and Experimental Mechanics", "Dynamical Systems Design", "Thermo Fluids Engineering"],
            "labs": [],
            "research_centers": ["Control Systems Technology", "Mechanics of Materials", "Autonomous and Complex Systems"],
            "space_or_aerospace_projects": [
                "lightweight and high-strength aerospace materials, composite damage/failure, jet-engine high-temperature materials and landing-gear reliability",
                "integrated design and control methods applied to drones, aircraft and electric aircraft",
                "learning control collaborations spanning space and astronomy",
                "master's thesis example in free-space optical communication using iterative learning control",
            ],
            "research_strength_summary": bi(
                "TU/e has credible aerospace-adjacent research in structures/materials, controls, drones/e-aircraft and precision mechatronics for space/astronomy, but no dedicated space-engineering department or programme was verified.",
                "TU/e; yapÄ±lar/malzemeler, kontrol, Ä°HA/e-uÃ§ak ve uzay/astronomi iÃ§in hassas mekatronikte gÃ¼venilir havacÄ±lÄ±k-yan alan araÅŸtÄ±rmasÄ±na sahiptir; ancak Ã¶zel uzay mÃ¼hendisliÄŸi bÃ¶lÃ¼mÃ¼ veya programÄ± doÄŸrulanmadÄ±.",
            ),
            "research_strength_score": 70,
            "research_sources": [DEPARTMENT_URL, AEROSPACE_URL, HOFMAN_URL, OOMEN_URL, THESIS_URL],
        }
    )

    row["industry_ecosystem_profile"].update(
        {
            "nearby_companies": [],
            "confirmed_partners": [],
            "internship_possibility": "programme_structure_includes_internship",
            "thesis_with_industry_possibility": "possible_not_guaranteed",
            "career_relevance": "strong_for_high_tech_mechanical_and_control_roles",
            "ecosystem_strength_score": None,
            "ecosystem_notes": bi(
                "The programme catalogue says the department works intensively with many high-tech companies, but it does not name them. ASML, Philips or NXP are therefore not stored as programme partners without a direct current confirmation.",
                "Program kataloÄŸu bÃ¶lÃ¼mÃ¼n Ã§ok sayÄ±da yÃ¼ksek teknoloji ÅŸirketiyle yoÄŸun Ã§alÄ±ÅŸtÄ±ÄŸÄ±nÄ± belirtir ancak ad vermez. Bu nedenle ASML, Philips veya NXP doÄŸrudan gÃ¼ncel teyit olmadan program ortaÄŸÄ± olarak tutulmaz.",
            ),
        }
    )

    row["application_timeline_profile"].update(
        {
            "academic_year": "2027/2028 planning; 2026/2027 closed reference",
            "intake_terms": ["September 2027"],
            "non_eu_deadline": "2027-05-01",
            "eu_deadline": "2027-05-01",
            "application_deadline": "2027-05-01",
            "scholarship_deadline": None,
            "timeline_risk": "medium",
            "deadline_events": [
                {"event": "September 2026 programme application", "date": "2026-05-01", "status": "closed"},
                {"event": "September 2027 programme application", "date": "2027-05-01", "status": "future_published"},
            ],
            "deadline_notes": bi(
                "Study in NL currently publishes 1 May for both EU/EEA and non-EU/EEA applicants for the September 2027 start. Scholarship timing is not inferred from old ALSP cycles.",
                "Study in NL EylÃ¼l 2027 baÅŸlangÄ±cÄ± iÃ§in hem AB/AEA hem AB/AEA dÄ±ÅŸÄ± adaylara 1 MayÄ±s tarihini yayÄ±mlar. Burs takvimi eski ALSP dÃ¶nemlerinden Ã§Ä±karÄ±lmaz.",
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
            "sentiment_summary": bi("Insufficient programme-specific, attributable recent student evidence; no sentiment conclusion is stored.", "Programa Ã¶zgÃ¼, atfedilebilir gÃ¼ncel Ã¶ÄŸrenci kanÄ±tÄ± yetersizdir; duygu sonucu tutulmaz."),
            "student_sentiment_sources": [],
            "verification_notes": bi("Prior unattributed Reddit search-result quotations were removed.", "Ã–nceki atÄ±fsÄ±z Reddit arama-sonucu alÄ±ntÄ±larÄ± kaldÄ±rÄ±ldÄ±."),
        }
    )

    profile = row["source_profile"]
    profile.update(
        {
            "official_program_page": PROGRAM_URL,
            "official_admission_page": PROGRAM_URL,
            "official_tuition_page": STUDY_NL_URL,
            "official_scholarship_page": STUDY_NL_URL,
            "official_curriculum_page": STUDY_NL_URL,
            "official_department_page": DEPARTMENT_URL,
            "official_housing_page": VESTIDE_URL,
            "official_cost_of_living_page": LIVING_URL,
            "last_verified": CHECKED,
            "needs_verification": True,
            "verification_notes": bi(
                "Accessible national and provider sources support programme, language, dates, scholarship listing, structure and housing examples. Programme admission, 2026/27 non-EU tuition and scholarship mechanics remain unresolved because TU/e pages blocked access.",
                "EriÅŸilebilir ulusal ve saÄŸlayÄ±cÄ± kaynaklar program, dil, tarihler, burs listesi, yapÄ± ve konut Ã¶rneklerini destekler. TU/e sayfalarÄ± eriÅŸimi engellediÄŸinden program kabulÃ¼, 2026/27 AB dÄ±ÅŸÄ± Ã¼cret ve burs sÃ¼reci Ã§Ã¶zÃ¼msÃ¼z kalÄ±r.",
            ),
        }
    )
    profile["field_confidence"].update(
        {"program_basic_info": "high", "language": "high", "non_eu_eligibility": "high", "admission": "unknown", "tuition": "unknown", "scholarship": "medium", "curriculum": "medium", "deadline": "high", "deadlines": "high", "housing": "high", "living": "medium", "research": "high", "industry": "medium"}
    )
    profile["source_log"] = [
        source(STUDY_NL_URL, "Study in NL: Mechanical Engineering at Eindhoven University of Technology", "official_national_education_portal", ["program", "language", "non_eu_eligibility", "tuition", "scholarship", "deadline", "curriculum"], "Current Nuffic initiative page verifies 120 ECTS, two years, English, clusters, broad study structure, language scores, 2026/27 EU fee, non-EU fee unavailable, programme deadlines and scholarship listings."),
        source(LIVING_URL, "Study in NL: Daily student expenses and cost of living", "official_cost_of_living_page", ["living", "housing"], "Official Netherlands-wide monthly student budget and room-cost range; not Eindhoven-specific."),
        source(VESTIDE_URL, "Vestide furnished room on the TU/e campus", "official_student_housing_provider", ["housing", "living"], "Current room example with full cost breakdown, international eligibility, required documents and non-guaranteed response workflow."),
        source(DEPARTMENT_URL, "TU/e Research Portal: Mechanical Engineering", "official_department_page", ["research"], "Department divisions, active facilities and research structure."),
        source(AEROSPACE_URL, "TU/e Research Portal: Aerospace impact", "official_department_page", ["research"], "Direct aerospace materials, composites, jet-engine materials and landing-gear research evidence."),
        source(HOFMAN_URL, "TU/e Research Portal: Group Hofman", "official_department_page", ["research"], "Integrated design and control applications explicitly spanning drones, aircraft and e-aircraft."),
        source(OOMEN_URL, "TU/e Research Portal: Group Oomen", "official_department_page", ["research"], "Learning-control research and collaborations covering precision mechatronics, space and astronomy."),
        source(THESIS_URL, "TU/e Research Portal: Autonomous and Complex Systems student theses", "official_department_page", ["research", "curriculum"], "Search-indexed programme-level thesis evidence includes free-space optical communication control; direct link checking returned HTTP 403.", "medium", "blocked"),
        source(TUITION_CONTEXT_URL, "Cursor: University fund launches crowdfunding for students in need", "official_university_media", ["tuition"], "January 2026 university-media context for the 2025/26 EUR 21,000 non-EU master's fee; not used as a 2026/27 amount.", "medium"),
        source(HOUSING_CONTEXT_URL, "Cursor: Full speed ahead on recruiting master's students", "official_university_media", ["housing", "programme_context"], "April 2025 programme context explicitly calling housing a major problem.", "medium"),
    ]

    row["decision_summary"].update(
        {
            "main_strengths": [bi("A broad 120-ECTS Mechanical Engineering degree with control, mechanics/materials and thermofluid clusters plus a programme internship and graduation project.", "Kontrol, mekanik/malzemeler ve termofluid kÃ¼meleri ile program stajÄ± ve mezuniyet projesi iÃ§eren geniÅŸ 120 AKTS Mechanical Engineering derecesi."), bi("Official research evidence supports aerospace materials, aircraft/drone control applications and space/astronomy precision mechatronics.", "ResmÃ® araÅŸtÄ±rma kanÄ±tÄ± havacÄ±lÄ±k malzemeleri, uÃ§ak/Ä°HA kontrol uygulamalarÄ± ve uzay/astronomi hassas mekatroniÄŸini destekler.")],
            "main_risks": [bi("This is not an Aerospace or Space Engineering degree; no orbital mechanics, spacecraft systems, mission design or dedicated space track was verified.", "Bu bir Aerospace veya Space Engineering derecesi deÄŸildir; yÃ¶rÃ¼nge mekaniÄŸi, uzay aracÄ± sistemleri, gÃ¶rev tasarÄ±mÄ± veya Ã¶zel uzay izi doÄŸrulanmadÄ±."), bi("The 2026/27 non-EU tuition, academic admission rules and current scholarship mechanics remain unknown because TU/e's linked pages blocked research access.", "TU/e'nin baÄŸlÄ± sayfalarÄ± araÅŸtÄ±rma eriÅŸimini engellediÄŸinden 2026/27 AB dÄ±ÅŸÄ± Ã¼cret, akademik kabul kurallarÄ± ve gÃ¼ncel burs sÃ¼reci bilinmiyor."), bi("Housing is not guaranteed; the current room is a single Vestide example and university reporting still describes a serious shortage.", "Konut garantili deÄŸildir; gÃ¼ncel oda tek bir Vestide Ã¶rneÄŸidir ve Ã¼niversite haberciliÄŸi hÃ¢lÃ¢ ciddi eksiklik bildirir.")],
            "best_for": [bi("Students targeting control, mechatronics, CFD/thermofluids or aerospace structures/materials who accept a general Mechanical Engineering degree title.", "Genel Mechanical Engineering derece adÄ±nÄ± kabul ederek kontrol, mekatronik, HAD/termofluid veya havacÄ±lÄ±k yapÄ±larÄ±/malzemelerini hedefleyen Ã¶ÄŸrenciler.")],
            "not_ideal_for": [bi("Students seeking a dedicated spacecraft, satellite, orbital mechanics, astrodynamics, mission design or propulsion curriculum.", "Ã–zel uzay aracÄ±, uydu, yÃ¶rÃ¼nge mekaniÄŸi, astrodinamik, gÃ¶rev tasarÄ±mÄ± veya itki mÃ¼fredatÄ± arayan Ã¶ÄŸrenciler.")],
            "application_reality": bi("The next published programme deadline is 1 May 2027, but applicants need direct TU/e confirmation of academic eligibility, non-EU tuition and scholarship timing before spending money.", "YayÄ±mlanmÄ±ÅŸ sonraki program tarihi 1 MayÄ±s 2027'dir; ancak adaylar para harcamadan Ã¶nce akademik uygunluk, AB dÄ±ÅŸÄ± Ã¼cret ve burs takvimini doÄŸrudan TU/e'den doÄŸrulamalÄ±dÄ±r."),
            "overall_recommendation": bi("A credible adjacent option for control, fluids and structures, not a substitute for a dedicated aerospace/space master's.", "Kontrol, akÄ±ÅŸkanlar ve yapÄ±lar iÃ§in gÃ¼venilir yan alan seÃ§eneÄŸidir; Ã¶zel havacÄ±lÄ±k/uzay yÃ¼ksek lisansÄ±nÄ±n yerine geÃ§mez."),
        }
    )

    quality = audit_record(row)
    quality["audited_at"] = CHECKED
    row["data_quality"] = quality
    row["quality_control"].update(
        {
            "qc_status": "needs_revision",
            "checked_at": CHECKED,
            "failed_canary_tests": ["missing_or_unverified_critical_fields"],
            "remaining_verification_tasks": [bi("Obtain current programme-specific academic admission and document rules directly from TU/e.", "GÃ¼ncel programa Ã¶zgÃ¼ akademik kabul ve belge kurallarÄ±nÄ± doÄŸrudan TU/e'den alÄ±n."), bi("Verify the 2026/27 non-EU tuition and current ALSP/NL Scholarship amounts, process and deadline.", "2026/27 AB dÄ±ÅŸÄ± Ã¼creti ile gÃ¼ncel ALSP/NL Scholarship tutar, sÃ¼reÃ§ ve tarihlerini doÄŸrulayÄ±n."), bi("Replace the single housing example and national living range when TU/e publishes a current Eindhoven-specific budget or allocation policy.", "TU/e gÃ¼ncel Eindhoven'a Ã¶zgÃ¼ bÃ¼tÃ§e veya tahsis politikasÄ± yayÄ±mladÄ±ÄŸÄ±nda tek konut Ã¶rneÄŸi ve ulusal yaÅŸam aralÄ±ÄŸÄ±nÄ± yenileyin.")],
            "qc_notes": bi("The record deliberately remains incomplete rather than converting inaccessible or historical values into current facts.", "KayÄ±t, eriÅŸilemeyen veya tarihsel deÄŸerleri gÃ¼ncel gerÃ§eklere dÃ¶nÃ¼ÅŸtÃ¼rmek yerine bilinÃ§li olarak eksik kalÄ±r."),
        }
    )

    DATA_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
