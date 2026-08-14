"""Rebuild the UPM MUSE record from checked 2026/27 official evidence."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from unirank.core.integrity import audit_record


PATH = ROOT / "data_base" / "ispanya.json"
RECORD_ID = "spain_upm_muse_aerospace"
CHECKED = "2026-08-14"

PROGRAM = "https://www.upm.es/Estudiantes/Estudios_Titulaciones/Estudios_Master/Programas?fmt=detail&id=14.2"
MUSE_ADMISSION = "https://muse.idr.upm.es/es/master?catid=8&id=4%3Aadmision-al-muse&view=article"
UPM_ADMISSION = "https://www.upm.es/Estudiantes/Estudios_Titulaciones/Estudios_Master/preguntas_frecuentes"
CALENDAR = "https://www.upm.es/Estudiantes/Estudios_Titulaciones/Estudios_Master/Calendario?fmt=detail&id=CON03072"
TUITION = "https://www.upm.es/Estudiantes/Estudios_Titulaciones/Estudios_Master/Admision?fmt=detail&id=0f9a705e2b58d110VgnVCM10000009c7648a____&prefmt=articulo"
SCHOLARSHIP = "https://www.upm.es/Estudiantes/Practicas/COIE?fmt=detail&id=CON11140&prefmt=articulo"
HOUSING = "https://www.upm.es/Estudiantes/Movilidad/Programas_Internacionales/Erasmus?fmt=detail&id=CON24663&prefmt=articulo"
WELCOME_GUIDE = "https://web.upm.es/hrs4r/sites/default/files/2024-09/01_welcome_guide_upm_es.pdf"
MUSE_MASTER = "https://muse.idr.upm.es/index.php/es/master"
CURRENT_CURRICULUM = "https://muse.idr.upm.es/es/ordenacion-academica/general"
COMPLETE_PLAN = "https://muse.idr.upm.es/index.php/2021-2022?catid=11&id=17%3Aplan-14sa-2020-2021&view=article"
CASE_STUDY_2 = "https://muse.idr.upm.es/images/Guias%20Aprendizaje%20202526/GA_14SA_143000133_1S_2025-26.pdf"
MUSE_NEWS = "https://muse.idr.upm.es/es/ultimasnoticias"


def bi(en: str, tr: str) -> dict[str, str]:
    return {"en": en, "tr": tr}


def source(
    url: str,
    title: str,
    source_type: str,
    fields: list[str],
    en: str,
    tr: str,
    *,
    access_status: str = "ok",
    confidence: str = "high",
) -> dict:
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


COURSE_TR = {
    "Ampliación de matemáticas 1": "İleri Matematik 1",
    "Entorno espacial y análisis de misión": "Uzay Ortamı ve Görev Analizi",
    "Ingeniería de sistemas y gestión de proyectos": "Sistem Mühendisliği ve Proje Yönetimi",
    "Vibraciones y aeroacústica": "Titreşimler ve Aeroakustik",
    "Ingeniería gráfica para diseño mecánico aeroespacial": "Havacılık-Uzay Mekanik Tasarımı için Mühendislik Grafiği",
    "Propulsión espacial y lanzadores": "Uzay İtkisi ve Fırlatıcılar",
    "Ampliación de matemáticas 2": "İleri Matematik 2",
    "Aerodinámica de altas velocidades y fenómenos de reentrada": "Yüksek Hız Aerodinamiği ve Yeniden Giriş Olayları",
    "Transferencia de calor y control térmico": "Isı Transferi ve Isıl Kontrol",
    "Generación y gestión de potencia eléctrica": "Elektrik Gücü Üretimi ve Yönetimi",
    "Estructuras de uso espacial": "Uzay Yapıları",
    "Caso de estudio 1": "Vaka Çalışması 1",
    "Comunicaciones": "Haberleşme",
    "Gestión de datos": "Veri Yönetimi",
    "Dinámica orbital y control de actitud": "Yörünge Dinamiği ve Tutum Kontrolü",
    "Materiales de uso espacial": "Uzay Malzemeleri",
    "Garantía de calidad": "Kalite Güvencesi",
    "Tecnologías de producción": "Üretim Teknolojileri",
    "Integración y ensayos": "Entegrasyon ve Testler",
    "Caso de estudio 2": "Vaka Çalışması 2",
    "Seminario sobre industria e instituciones espaciales": "Uzay Endüstrisi ve Kurumları Semineri",
    "Caso de estudio 3": "Vaka Çalışması 3",
}


def course(en: str, es: str, ects: float, semester: int) -> dict:
    return {"name": bi(en, COURSE_TR[es]), "native_name": es, "ects": ects, "semester": semester, "required": True}


def upsert_sources(profile: dict, additions: list[dict]) -> None:
    existing = profile.setdefault("source_log", [])
    preserved = [
        item for item in existing
        if isinstance(item, dict)
        and item.get("source_type") in {"official_qs", "third_party_geocoding_reference"}
    ]
    profile["source_log"] = preserved + additions


def update(row: dict) -> None:
    row.update(
        {
            "program_url": PROGRAM,
            "department": "Instituto Universitario de Microgravedad Ignacio Da Riva (IDR/UPM)",
            "faculty_or_school": "Escuela Técnica Superior de Ingeniería Aeronáutica y del Espacio (ETSIAE)",
            "campus": "Moncloa, Madrid",
            "program_status": "active",
            "relevance_status": "strong",
        }
    )

    row["eligibility_profile"] = {
        "eligible_for_non_eu": True,
        "non_eu_quota": None,
        "required_previous_degree": bi(
            "A university degree that gives access to postgraduate study; MUSE only considers the listed engineering/science profiles.",
            "Lisansüstü eğitime erişim sağlayan bir üniversite derecesi; MUSE yalnızca listelenen mühendislik/fen profillerini değerlendirir.",
        ),
        "accepted_backgrounds": [
            bi("Aeronautical/Aerospace Engineering", "Havacılık/Uzay Mühendisliği"),
            bi("Industrial Technologies Engineering or Naval Engineering (no bridging courses stated)", "Endüstriyel Teknolojiler Mühendisliği veya Gemi Mühendisliği (tamamlama dersi belirtilmiyor)"),
            bi("Telecommunications Engineering, Mechanical Engineering, Physics or Mathematics (6–18 ECTS bridging courses may apply)", "Telekomünikasyon Mühendisliği, Makine Mühendisliği, Fizik veya Matematik (6–18 AKTS tamamlama dersi uygulanabilir)"),
        ],
        "excluded_backgrounds": [bi("Degrees outside the profiles listed by MUSE", "MUSE tarafından listelenen profiller dışındaki dereceler")],
        "required_ects": {"bridging_courses_ects_min": 6, "bridging_courses_ects_max": 18, "applies_to": "telecommunications, mechanical engineering, physics and mathematics profiles"},
        "minimum_gpa": bi("No numeric minimum is published.", "Sayısal bir asgari not ortalaması yayımlanmamıştır."),
        "gpa_scale": "",
        "ranking_or_selection": bi(
            "Selection considers prior academic fit, space-related academic/professional experience, grade average, motivation letter and recommendation letters. First-choice applicants receive preference; the 2026/27 first-round notice also mentions a video when requested.",
            "Seçimde önceki eğitimin uygunluğu, uzayla ilgili akademik/mesleki deneyim, not ortalaması, motivasyon mektubu ve referans mektupları değerlendirilir. Programı ilk tercih olarak yazanlara öncelik verilir; 2026/27 ilk tur duyurusu ayrıca talep edilmişse video değerlendirmesini belirtir.",
        ),
        "admission_mode": "selective",
        "admission_risk": "high",
        "cohort_size_max": 20,
        "required_documents": [
            bi("Passport, DNI or NIE", "Pasaport, DNI veya NIE"),
            bi("Curriculum vitae", "Özgeçmiş"),
            bi("Official university degree or proof that it has been requested", "Resmî üniversite diploması veya diploma talep belgesi"),
            bi("Official transcript showing credits and grades", "Kredileri ve notları gösteren resmî transkript"),
            bi("Final Spanish Ministry grade-average equivalence certificate for foreign degrees", "Yabancı diplomalar için İspanya Bakanlığı kesin not ortalaması eşdeğerlik belgesi"),
            bi("Legalisation/Apostille for non-EHEA academic documents, as applicable", "EEES dışı akademik belgeler için gerektiğinde tasdik/Apostil"),
            bi("Official translation when documents are not in Spanish or English", "Belgeler İspanyolca veya İngilizce değilse resmî tercüme"),
            bi("Motivation letter", "Motivasyon mektubu"),
            bi("Recommendation letter(s)", "Referans mektubu/mektupları"),
        ],
        "motivation_letter_required": True,
        "cv_required": True,
        "recommendation_required": True,
        "portfolio_required": False,
        "interview_required": False,
        "interview_policy": "optional_at_academic_committee_discretion",
        "test_required": False,
        "test_policy": bi(
            "A bachelor-level mathematics and physics entrance test may be convened if demand is far above available places.",
            "Talebin kontenjanın çok üzerine çıkması hâlinde lisans düzeyinde matematik ve fizik giriş sınavı düzenlenebilir.",
        ),
        "video_requirement": "only_if_requested_in_the_call",
        "notes_for_turkish_students": bi(
            "MUSE is a non-profession-qualifying official master's. The checked UPM route for non-EHEA degrees requires legalised academic documents, the final grade-average equivalence certificate and translations when needed; it does not list Spanish degree homologation as a normal MUSE application requirement. Apply early for visa time.",
            "MUSE mesleki yetki veren bir resmî yüksek lisans değildir. EEES dışı dereceler için kontrol edilen UPM yolu; tasdikli akademik belgeler, kesin not ortalaması eşdeğerlik belgesi ve gerektiğinde tercüme ister; İspanyol diploma homologasyonunu normal MUSE başvuru şartı olarak listelemez. Vize süresi için erken başvurun.",
        ),
        "verification_notes": bi(
            "Non-EHEA graduates may apply. MUSE states that applicants from non-EHEA universities with a UPM agreement receive preference; this is not an exclusion of other applicants.",
            "EEES dışı üniversite mezunları başvurabilir. MUSE, UPM anlaşması bulunan EEES dışı üniversitelerden gelenlere öncelik verildiğini belirtir; bu diğer adayların dışlandığı anlamına gelmez.",
        ),
        "gre": {
            "policy": "not_listed_as_required",
            "test_type": "none_specified",
            "minimum_scores": {},
            "recommended_scores": {},
            "validity_rule": "",
            "waiver_rules": [],
            "source_ids": [UPM_ADMISSION, MUSE_ADMISSION],
            "notes": bi(
                "GRE is not listed in the checked UPM or MUSE requirements. A separate MUSE mathematics/physics entrance test may be introduced under exceptional excess demand; it is not the GRE.",
                "Kontrol edilen UPM veya MUSE şartlarında GRE listelenmemiştir. Olağanüstü yoğun talepte ayrı bir MUSE matematik/fizik sınavı konabilir; bu GRE değildir.",
            ),
        },
    }

    row["language_profile"] = {
        "teaching_language": ["Spanish"],
        "english_required": False,
        "english_level_required": "",
        "accepted_english_tests": [],
        "english_exemptions": [],
        "spanish_required": True,
        "spanish_level_required": "B2",
        "spanish_requirement_scope": "applicants from non-Spanish-speaking countries",
        "accepted_spanish_tests": [],
        "mixed_language_warning": bi(
            "The official teaching language is Spanish. MUSE requires B2 Spanish from applicants coming from non-Spanish-speaking countries; the checked page does not publish a closed list of accepted certificates.",
            "Resmî eğitim dili İspanyolcadır. MUSE, İspanyolca konuşulmayan ülkelerden gelen adaylardan B2 İspanyolca ister; kontrol edilen sayfa kabul edilen sertifikaların kapalı bir listesini yayımlamaz.",
        ),
        "language_risk": "high",
        "verification_notes": bi(
            "UPM's general B2 English rule applies to Appendix-I professional master's degrees; MUSE is not in that category. No English test is listed for MUSE admission.",
            "UPM'nin genel B2 İngilizce kuralı Ek-I mesleki yetki veren yüksek lisanslara uygulanır; MUSE bu kategoride değildir. MUSE kabulü için İngilizce sınavı listelenmemiştir.",
        ),
    }

    row["cost_profile"].update(
        {
            "academic_year": "2026/2027",
            "tuition_eur_per_year_min": 2701.20,
            "tuition_eur_per_year_max": 5044.20,
            "tuition_eur_per_year_estimated": None,
            "tuition_eur_per_year_non_eu_nonresident": 5044.20,
            "tuition_basis": "official_first-enrolment_per-credit_rate_multiplied_by_the_standard_60_ECTS_year",
            "regional_tax_eur": None,
            "student_contribution_eur": None,
            "application_fee_eur": None,
            "enrollment_fee_eur": 33.65,
            "total_academic_cost_eur_per_year_estimated": None,
            "isee_or_income_based": False,
            "non_eu_flat_fee": None,
            "reservation_deposit_eur": 150,
            "reservation_deposit_deducted_from_tuition": True,
            "payment_installments": "unknown",
            "refund_policy": bi(
                "The €150 place reservation is deducted from enrolment but is not refunded if the admitted applicant does not enrol.",
                "150 € yer ayırma bedeli kayıttan düşülür; kabul edilen aday kayıt yaptırmazsa iade edilmez.",
            ),
            "source_notes": bi(
                "MUSE is classified under 'other official master's degrees': €45.02/ECTS for Spanish/EU students and €84.07/ECTS for non-EU adults without resident status or EU-regime coverage. A standard 60-ECTS year therefore gives €2,701.20 or €5,044.20 in first-enrolment tuition. Student stay authorisation is not treated as residence for this tariff.",
                "MUSE 'diğer resmî yüksek lisanslar' sınıfındadır: İspanyol/AB öğrencileri için 45,02 €/AKTS; ikamet statüsü veya AB rejimi kapsamı bulunmayan yetişkin AB dışı öğrenciler için 84,07 €/AKTS. Standart 60 AKTS yılın ilk kayıt öğrenim ücreti bu nedenle 2.701,20 € veya 5.044,20 € olur. Öğrenci kalış izni bu tarife bakımından ikamet sayılmaz.",
            ),
            "verification_notes": bi(
                "The annual figures are transparent arithmetic from the official per-credit rate and 60 ECTS per academic year, not a forecast. Repeated-subject rates and optional personal expenses are excluded.",
                "Yıllık rakamlar resmî kredi başı ücret ile yıllık 60 AKTS'nin şeffaf çarpımıdır; tahmin değildir. Tekrar alınan ders ücretleri ve kişisel giderler hariçtir.",
            ),
            "tuition_items": [
                {"student_category": "Spanish_or_EU", "enrolment_attempt": "first", "rate_eur_per_ects": 45.02, "standard_annual_ects": 60, "annual_tuition_eur": 2701.20},
                {"student_category": "non_EU_nonresident_not_under_EU_regime", "enrolment_attempt": "first", "rate_eur_per_ects": 84.07, "standard_annual_ects": 60, "annual_tuition_eur": 5044.20},
                {"item": "opening_academic_record", "amount_eur": 27.54},
                {"item": "secretariat_fee", "amount_eur": 6.11},
            ],
        }
    )
    row["tuition_eur_per_year"] = 5044.20
    row["annual_fee_eur"] = 33.65

    row["scholarship_profile"] = {
        "regional_scholarship_available": None,
        "regional_scholarship_name": None,
        "dsu_or_equivalent": "",
        "merit_scholarships": [],
        "tuition_waivers": [],
        "housing_support": None,
        "meal_support": None,
        "cash_grant_possible": True,
        "non_eu_eligible": None,
        "income_based": False,
        "scholarship_deadline": "2026-10-07",
        "scholarship_application_url": "https://app.santanderopenacademy.com/es/program/ayuda-economica-2026",
        "funding_competitiveness": "competitive",
        "funding_notes": bi(
            "The current verified opportunity is a post-enrolment €1,000 Santander economic-aid call, not automatic admission funding and not a tuition guarantee. The checked public summary does not establish eligibility for a newly arrived non-EU student on a study-stay permit.",
            "Doğrulanan güncel fırsat, kayıt sonrası 1.000 € Santander ekonomik destek çağrısıdır; otomatik kabul bursu veya öğrenim ücreti garantisi değildir. Kontrol edilen kamu özeti, öğrenci kalış izniyle yeni gelen AB dışı öğrencinin uygunluğunu kesinleştirmez.",
        ),
        "verification_notes": bi(
            "UPM directs master's applicants to its live calls and to the programme secretariat. No current MUSE-specific admission scholarship for 2026/27 was found on the official MUSE news page; the older 2023/24 MUSE prizes are not represented as active.",
            "UPM yüksek lisans adaylarını canlı çağrılar sayfasına ve program sekreterliğine yönlendirir. Resmî MUSE haberlerinde 2026/27 için güncel, MUSE'ye özgü kabul bursu bulunmadı; eski 2023/24 MUSE ödülleri aktifmiş gibi gösterilmez.",
        ),
        "application_mode": "separate",
        "automatic_consideration": False,
        "separate_application_required": True,
        "opportunities": [
            {
                "name": "Becas Santander Estudios / Ayuda Económica 2026",
                "academic_year": "2026/2027",
                "amount_eur": 1000,
                "total_awards": 465,
                "new_master_awards": 50,
                "continuing_master_awards": 30,
                "eligibility_summary": bi("Must be enrolled in an official UPM bachelor's or master's programme and meet the call conditions.", "Resmî bir UPM lisans veya yüksek lisans programına kayıtlı olmak ve çağrı koşullarını karşılamak gerekir."),
                "non_eu_eligibility": "needs_verification",
                "application_mode": "separate",
                "automatic": False,
                "requires_upm_email": True,
                "opens": "2026-04-21",
                "deadline": "2026-10-07",
                "url": "https://app.santanderopenacademy.com/es/program/ayuda-economica-2026",
            }
        ],
    }

    row["living_profile"].update(
        {
            "city_cost_level": "high",
            "monthly_living_cost_eur_min": None,
            "monthly_living_cost_eur_max": None,
            "monthly_living_cost_eur_estimated": None,
            "housing_difficulty": "high",
            "student_housing_available": False,
            "student_housing_competitiveness": "not_applicable",
            "average_room_rent_eur": None,
            "average_room_rent_eur_min": None,
            "average_room_rent_eur_max": None,
            "living_risk": "high",
            "housing_difficulty_score": None,
            "living_risk_score": None,
            "housing_access": "not_offered",
            "housing_allocation_mode": "external_market_and_independent_residences",
            "housing_application_separate": True,
            "housing_options": [
                {"provider": "External shared-flat platforms listed by UPM", "institution_owned": False, "guaranteed": False, "application_separate": True},
                {"provider": "External student residences listed by UPM", "institution_owned": False, "guaranteed": False, "application_separate": True},
            ],
            "official_rent_items": [],
            "official_living_cost_items": [
                {
                    "item": "UPM welcome-guide accommodation reference range",
                    "amount_eur_min": 650,
                    "amount_eur_max": 1000,
                    "period": "monthly",
                    "guide_date": "2024-09",
                    "scope": "general Madrid accommodation guidance; not a current private-room average or offer",
                    "confidence": "medium",
                }
            ],
            "housing_notes": bi(
                "UPM's current incoming-student page states that UPM has no student residences and only links to external shared-flat services and independent residences. No place is allocated with admission.",
                "UPM'nin güncel gelen öğrenci sayfası UPM'nin öğrenci yurdu olmadığını ve yalnızca harici ortak daire hizmetleri ile bağımsız yurtlara bağlantı verdiğini belirtir. Kabulle birlikte konut tahsis edilmez.",
            ),
            "verification_notes": bi(
                "The €650–1,000 figure is retained only as a dated September 2024 official welcome-guide reference. It is not treated as a 2026 market quote, room average or guaranteed budget; a current complete monthly living-cost total remains unknown.",
                "650–1.000 € rakamı yalnızca Eylül 2024 tarihli resmî karşılama rehberi referansı olarak tutulur. 2026 piyasa fiyatı, oda ortalaması veya garantili bütçe sayılmaz; güncel tam aylık yaşam maliyeti bilinmiyor.",
            ),
        }
    )

    mandatory = [
        course("Advanced Mathematics 1", "Ampliación de matemáticas 1", 6, 1),
        course("Space Environment and Mission Analysis", "Entorno espacial y análisis de misión", 3, 1),
        course("Systems Engineering and Project Management", "Ingeniería de sistemas y gestión de proyectos", 6, 1),
        course("Vibrations and Aeroacoustics", "Vibraciones y aeroacústica", 4.5, 1),
        course("Engineering Graphics for Aerospace Mechanical Design", "Ingeniería gráfica para diseño mecánico aeroespacial", 4.5, 1),
        course("Space Propulsion and Launchers", "Propulsión espacial y lanzadores", 4.5, 1),
        course("Advanced Mathematics 2", "Ampliación de matemáticas 2", 6, 2),
        course("High-Speed Aerodynamics and Re-entry Phenomena", "Aerodinámica de altas velocidades y fenómenos de reentrada", 3, 2),
        course("Heat Transfer and Thermal Control", "Transferencia de calor y control térmico", 6, 2),
        course("Electrical Power Generation and Management", "Generación y gestión de potencia eléctrica", 3, 2),
        course("Space Structures", "Estructuras de uso espacial", 4.5, 2),
        course("Case Study 1", "Caso de estudio 1", 1.5, 2),
        course("Communications", "Comunicaciones", 4.5, 2),
        course("Data Management", "Gestión de datos", 4.5, 2),
        course("Orbital Dynamics and Attitude Control", "Dinámica orbital y control de actitud", 4.5, 3),
        course("Space Materials", "Materiales de uso espacial", 4.5, 3),
        course("Quality Assurance", "Garantía de calidad", 4.5, 3),
        course("Production Technologies", "Tecnologías de producción", 4.5, 3),
        course("Integration and Testing", "Integración y ensayos", 4.5, 3),
        course("Case Study 2", "Caso de estudio 2", 7.5, 3),
        course("Seminar on Space Industry and Institutions", "Seminario sobre industria e instituciones espaciales", 1.5, 4),
        course("Case Study 3", "Caso de estudio 3", 9, 4),
    ]
    row["curriculum_profile"] = {
        "tracks": [],
        "specializations": [],
        "mandatory_courses": mandatory,
        "elective_courses": [],
        "course_count_total_including_thesis": 23,
        "taught_project_and_seminar_component_count": 22,
        "elective_course_count": 0,
        "course_count_basis": "complete published Plan 14SA table cross-checked against 2025/26 course guides",
        "course_language_notes": bi("The programme and checked 2025/26 guides state Spanish.", "Program ve kontrol edilen 2025/26 ders rehberleri İspanyolca belirtir."),
        "thesis_required": True,
        "thesis_ects": 18,
        "thesis_title": bi("Master's Thesis", "Yüksek Lisans Tezi"),
        "internship_required": False,
        "internship_notes": bi(
            "There is no separate compulsory internship module in the complete plan. Case Study 2 may be carried out with an external company in a practice-like arrangement, with an academic supervisor.",
            "Eksiksiz planda ayrı bir zorunlu staj modülü yoktur. Case Study 2, akademik danışman eşliğinde staj benzeri biçimde harici bir şirketle yürütülebilir.",
        ),
        "lab_courses": [bi("Integration and Testing", "Entegrasyon ve Test"), bi("Case Study 2", "Case Study 2")],
        "project_based_courses": [bi("Case Study 1", "Case Study 1"), bi("Case Study 2", "Case Study 2"), bi("Case Study 3", "Case Study 3")],
        "mobility_options": [],
        "double_degree_options": [],
        "curriculum_url": CURRENT_CURRICULUM,
        "study_plan_url": COMPLETE_PLAN,
        "verification_notes": bi(
            "The newest fully indexed tabular plan located is the 2020/21 Plan 14SA. Its course codes and structure are corroborated by the current 2025/26 learning-guide index and individual guides. Any 2026/27 timetable-level change should be rechecked when UPM publishes that cycle's guides.",
            "Bulunan en yeni eksiksiz ve dizinlenmiş tablo 2020/21 Plan 14SA'dır. Ders kodları ve yapı, güncel 2025/26 öğrenme rehberi dizini ve tekil rehberlerle doğrulanmıştır. 2026/27 ders programı düzeyindeki değişiklikler UPM o dönemin rehberlerini yayımladığında yeniden kontrol edilmelidir.",
        ),
    }

    row["category_profile"] = {
        "primary_categories": ["Space Systems & Astronautics"],
        "secondary_categories": [
            "Flight Mechanics, Control & Autonomy",
            "Propulsion, Energy & Thermal Systems",
            "Structures, Materials & Mechanical Design",
            "Systems Engineering, Design & Optimization",
            "Avionics, Software & Digital Technologies",
            "Manufacturing, Testing & Industrial Applications",
            "Fluid Mechanics & Aerodynamics",
        ],
        "subcategories": [
            "space_systems", "spacecraft_design", "astrodynamics", "mission_analysis", "space_environment",
            "gnc", "rocket_propulsion", "thermal_management", "energy_systems", "aerospace_structures",
            "materials", "systems_engineering", "verification_validation", "embedded_systems", "testing",
            "manufacturing", "industrial_projects", "internship_thesis", "aerothermodynamics", "aeroacoustics",
        ],
        "normalized_tags": [
            "space_systems", "spacecraft_design", "astrodynamics", "mission_analysis", "space_environment",
            "gnc", "rocket_propulsion", "thermal_management", "energy_systems", "aerospace_structures",
            "materials", "systems_engineering", "verification_validation", "embedded_systems", "testing",
            "manufacturing", "industrial_projects", "internship_thesis", "aerothermodynamics", "aeroacoustics",
        ],
        "category_scores": {},
        "category_evidence": [
            bi(
                "The official 120-ECTS plan directly covers mission analysis, orbital and attitude dynamics, propulsion/launchers, thermal and power subsystems, structures/materials, communications/data, systems engineering, production, integration and testing.",
                "Resmî 120 AKTS planı görev analizini, yörünge ve tutum dinamiğini, itki/fırlatıcıları, ısıl ve güç alt sistemlerini, yapı/malzemeyi, haberleşme/veriyi, sistem mühendisliğini, üretimi, entegrasyonu ve testi doğrudan kapsar.",
            )
        ],
    }

    row["research_profile"] = {
        "department_research_areas": [
            bi("Spacecraft and mission design", "Uzay aracı ve görev tasarımı"),
            bi("Space environment, orbital dynamics and attitude control", "Uzay ortamı, yörünge dinamiği ve tutum kontrolü"),
            bi("Thermal, power, communications and data subsystems", "Isıl, güç, haberleşme ve veri alt sistemleri"),
            bi("Spacecraft integration and environmental testing", "Uzay aracı entegrasyonu ve çevresel testler"),
        ],
        "labs": [
            {"name": "Concurrent Design Facility", "officially_described": True, "esa_supported": True, "student_access": "used in Case Study 2 according to the 2025/26 guide"},
            {"name": "Thermal-vacuum laboratory", "officially_described": True, "student_access": "used in Case Study 2 according to the 2025/26 guide"},
            {"name": "Prototype-modelling laboratory", "officially_described": True, "student_access": "used in Case Study 2 according to the 2025/26 guide"},
            {"name": "Space-environment integration and testing facility", "officially_described": True, "student_access": "programme page states availability; access conditions are not published"},
        ],
        "research_centers": ["Instituto Universitario de Microgravedad Ignacio Da Riva (IDR/UPM)"],
        "notable_professors": [],
        "space_or_aerospace_projects": ["UPMSat-2", "UPMSat-3", "OAPES"],
        "student_teams": ["Student Aerospace Challenge team (2024 ESA Grand Prix)"],
        "satellite_or_flight_projects": ["UPMSat-2", "UPMSat-3"],
        "research_strength_summary": bi(
            "MUSE is organised by the IDR/UPM research institute and explicitly gives students project-based work with concurrent-design and space-environment integration/testing facilities. The official page also states participation in IDR space projects; individual project placement is not guaranteed.",
            "MUSE, IDR/UPM araştırma enstitüsü tarafından düzenlenir ve öğrencilere eşzamanlı tasarım ile uzay ortamı entegrasyon/test tesisleriyle proje tabanlı çalışma sunar. Resmî sayfa ayrıca IDR uzay projelerine katılımı belirtir; tek tek projelere yerleştirme garanti değildir.",
        ),
        "research_strength_score": None,
        "research_sources": [MUSE_MASTER, CASE_STUDY_2, MUSE_NEWS],
    }

    row["industry_ecosystem_profile"] = {
        "nearby_companies": [],
        "confirmed_partners": [],
        "space_agencies_or_public_bodies": ["European Space Agency"],
        "research_institutes": ["IDR/UPM"],
        "startup_or_incubator_ecosystem": [],
        "internship_possibility": "optional_through_case_study_2",
        "thesis_with_industry_possibility": "unknown",
        "career_relevance": "strong",
        "ecosystem_strength_score": None,
        "ecosystem_notes": bi(
            "The verified industry-facing elements are the second-year industry/institutions seminar and the option to conduct Case Study 2 with an external company. No named employer is represented as a formal programme partner without an official partnership source.",
            "Doğrulanan sektör temasları ikinci yıl sektör/kurumlar semineri ve Case Study 2'yi harici bir şirketle yürütme seçeneğidir. Resmî ortaklık kaynağı olmadan hiçbir işveren resmî program ortağı olarak gösterilmez.",
        ),
    }

    row["application_timeline_profile"] = {
        "academic_year": "2026/2027",
        "intake_terms": ["September 2026"],
        "application_rounds": [
            {"round": 1, "opens": "2026-01-26", "deadline": "2026-03-12", "decision": "2026-03-20", "place_reservation": "2026-03-23/2026-04-08"},
            {"round": 2, "opens": "2026-03-13", "deadline": "2026-05-12", "decision": "2026-05-22", "place_reservation": "2026-05-25/2026-06-08"},
            {"round": 3, "opens": "2026-05-13", "deadline": "2026-07-01", "decision": "2026-07-17", "place_reservation": None},
            {"round": "extraordinary_if_places_remain", "opens": "2026-08-31", "deadline": "2026-09-04", "decision": "2026-09-09", "place_reservation": None},
        ],
        "non_eu_deadline": "2026-07-01",
        "eu_deadline": "2026-07-01",
        "scholarship_deadline": "2026-10-07",
        "pre_enrolment_required": True,
        "universitaly_required": False,
        "visa_sensitive_deadline": bi("UPM advises applicants outside the EHEA or EU to use the first application period and apply as early as possible for document and visa processing.", "UPM, EEES veya AB dışındaki adaylara belge ve vize işlemleri için ilk başvuru dönemini kullanmalarını ve mümkün olduğunca erken başvurmalarını önerir."),
        "application_result_timing": "2026-03-20; 2026-05-22; 2026-07-17; 2026-09-09 if extraordinary call opens",
        "enrollment_deadline": "2026-07-22/2026-07-30 or 2026-09-03/2026-09-11",
        "document_completion_deadline": "2026-09-30",
        "timeline_risk": "medium",
        "deadline_notes": bi(
            "The extraordinary call only exists for programmes with vacant places. MUSE has a small cohort and reported very high first-round demand in 2026, so it should not be treated as a dependable deadline.",
            "Olağanüstü çağrı yalnızca boş kontenjanı kalan programlarda açılır. MUSE'nin kontenjanı küçüktür ve 2026 ilk turunda çok yüksek talep bildirmiştir; bu tarih güvenilir ana son tarih sayılmamalıdır.",
        ),
        "winter_deadline": None,
        "application_deadline": "2026-07-01",
        "deadline_events": [
            {"event": "recommended_non_EU_action", "date": "2026-03-12", "notes": "Use first call where possible for documents and visa"},
            {"event": "regular_final_application_deadline", "date": "2026-07-01"},
            {"event": "ordinary_enrollment_window", "start": "2026-07-22", "end": "2026-07-30"},
            {"event": "extraordinary_application_if_places_remain", "start": "2026-08-31", "end": "2026-09-04"},
            {"event": "extraordinary_enrollment_window", "start": "2026-09-03", "end": "2026-09-11"},
            {"event": "foreign_document_completion", "date": "2026-09-30"},
            {"event": "Santander_economic_aid_deadline", "date": "2026-10-07"},
        ],
    }

    row["student_sentiment_profile"] = {
        "student_satisfaction_score": None,
        "sentiment_confidence": "low",
        "sample_size_estimate": 9,
        "date_range": "2021-2025",
        "teaching_quality_sentiment": "mixed",
        "workload_sentiment": "negative_high_workload",
        "administration_sentiment": "unknown",
        "housing_sentiment": "unknown",
        "city_life_sentiment": "mixed_positive",
        "international_student_support_sentiment": "unknown",
        "career_support_sentiment": "unknown",
        "positive_themes": [bi("Some comments value the people, Madrid and the theoretical foundation.", "Bazı yorumlar insanları, Madrid'i ve teorik temeli olumlu değerlendiriyor.")],
        "negative_themes": [bi("Repeated perception that aerospace/engineering study at UPM is unusually demanding, especially without strong Spanish.", "UPM'de havacılık-uzay/mühendislik eğitiminin, özellikle güçlü İspanyolca olmadan, olağandışı derecede zor olduğu yönünde tekrarlanan algı.")],
        "recurring_complaints": [bi("Heavy workload and difficult examinations are recurring institution/ETSIAE-level perceptions.", "Yoğun iş yükü ve zor sınavlar kurum/ETSIAE düzeyinde tekrarlanan algılardır.")],
        "recurring_strengths": [bi("Madrid location, peers and theoretical preparation receive some positive comments.", "Madrid konumu, öğrenci çevresi ve teorik hazırlık bazı olumlu yorumlar alır.")],
        "sentiment_summary": bi(
            "The available recent comments concern UPM/ETSIAE aerospace study broadly, not MUSE specifically. They consistently signal high workload and language sensitivity, while some praise Madrid, peers and theoretical depth. No MUSE satisfaction score is computed from this weak, non-program-specific sample.",
            "Bulunan güncel yorumlar doğrudan MUSE'yi değil, genel olarak UPM/ETSIAE havacılık-uzay eğitimini ele alır. Yüksek iş yükü ve dil hassasiyeti tutarlı biçimde belirtilirken bazıları Madrid'i, öğrenci çevresini ve teorik derinliği över. Bu zayıf ve program dışı örneklemden MUSE memnuniyet puanı hesaplanmaz.",
        ),
        "student_sentiment_sources": [
            {"source": "Reddit r/askspain", "url": "https://www.reddit.com/r/askspain/comments/1i1u3v7", "date": "2025-01-15", "scope": "UPM aerospace/Erasmus, not MUSE", "observations_used": 5},
            {"source": "Reddit r/AerospaceEngineering", "url": "https://www.reddit.com/r/AerospaceEngineering/comments/lgb9k6", "date": "2021-02-11", "scope": "UPM aerospace undergraduate, not MUSE", "observations_used": 1},
            {"source": "Reddit r/askspain", "url": "https://www.reddit.com/r/askspain/comments/13h3r94", "date": "2023-05-14", "scope": "UPM/ETSIAE graduate discussion, not MUSE", "observations_used": 3},
        ],
        "verification_notes": bi(
            "Sentiment is a low-confidence perception signal only. It does not prove MUSE workload, teaching quality, administration, housing or career outcomes.",
            "Duygu analizi yalnızca düşük güvenli bir algı sinyalidir. MUSE iş yükünü, öğretim kalitesini, idareyi, konutu veya kariyer sonuçlarını kanıtlamaz.",
        ),
    }

    profile = row["source_profile"]
    upsert_sources(
        profile,
        [
            source(PROGRAM, "Sistemas Espaciales — UPM official master's catalogue", "official_program_page", ["program", "program_status", "degree_level", "ects", "language", "curriculum"], "Current UPM catalogue identifies the active 120-ECTS, two-year, Spanish, on-campus MUSE programme.", "Güncel UPM kataloğu aktif, 120 AKTS, iki yıllık, İspanyolca ve yüz yüze MUSE programını tanımlar."),
            source(UPM_ADMISSION, "UPM official master's admission requirements and FAQ 2026/27", "official_admission_page", ["admission", "non_eu_eligibility", "required_documents", "deadline"], "Current rules for foreign degrees, translations, legalisation, grade equivalence, conditional admission, place reservation and document completion.", "Yabancı dereceler, tercüme, tasdik, not eşdeğerliği, şartlı kabul, yer ayırma ve belge tamamlama için güncel kurallar."),
            source(MUSE_ADMISSION, "Admission to MUSE — IDR/UPM", "official_admission_page", ["admission", "non_eu_eligibility", "language", "required_previous_degree"], "Programme-specific B2 Spanish rule, accepted backgrounds, 6–18 ECTS bridging courses, selection evidence and optional interview/test policy.", "Programa özgü B2 İspanyolca kuralı, kabul edilen geçmişler, 6–18 AKTS tamamlama dersleri, seçim kanıtları ve isteğe bağlı mülakat/sınav politikası."),
            source(CALENDAR, "UPM official master's calendar 2026/27", "official_admission_page", ["deadline", "application_timeline"], "Publishes four first-period calls, decisions, place-reservation windows, enrolment and foreign-document deadline.", "Dört ilk dönem çağrısını, kararları, yer ayırma pencerelerini, kaydı ve yabancı belge son tarihini yayımlar."),
            source(TUITION, "UPM 2026/27 official master's public prices", "official_tuition_page", ["tuition", "non_eu_eligibility"], "Publishes first-enrolment per-credit rates and administrative fees, including the non-EU nonresident tariff.", "AB dışı ikamet etmeyen öğrenci tarifesi dâhil ilk kayıt kredi başı ücretleri ve idari ücretleri yayımlar."),
            source(SCHOLARSHIP, "UPM Santander scholarships 2026/27", "official_scholarship_page", ["scholarship", "funding"], "Current €1,000 economic-aid call for enrolled UPM degree and master's students; 465 awards and a separate 21 April–7 October 2026 application.", "Kayıtlı UPM lisans ve yüksek lisans öğrencileri için güncel 1.000 € ekonomik destek çağrısı; 465 burs ve 21 Nisan–7 Ekim 2026 ayrı başvuru."),
            source(HOUSING, "UPM incoming students 2026/27 — accommodation", "official_housing_page", ["housing", "living"], "Current page states UPM has no student residences and lists external accommodation routes only.", "Güncel sayfa UPM'nin öğrenci yurdu olmadığını ve yalnızca harici konaklama yollarını listelediğini belirtir."),
            source(WELCOME_GUIDE, "UPM welcome guide — Madrid accommodation reference", "official_cost_of_living_page", ["housing", "living"], "September 2024 institutional guide gives a €650–1,000 accommodation reference; retained only as dated guidance, not a current market quote.", "Eylül 2024 kurumsal rehberi 650–1.000 € konaklama referansı verir; yalnızca tarihli rehberlik olarak tutulur, güncel piyasa fiyatı değildir.", access_status="pdf", confidence="medium"),
            source(CURRENT_CURRICULUM, "MUSE academic organisation and 2025/26 learning guides", "official_curriculum_page", ["curriculum", "courses", "language"], "Current academic page links the 2025/26 course list and learning guides.", "Güncel akademik sayfa 2025/26 ders listesine ve öğrenme rehberlerine bağlantı verir."),
            source(COMPLETE_PLAN, "MUSE Plan 14SA complete course table", "official_curriculum_page", ["curriculum", "courses"], "Most recent complete tabular plan located: 23 components totalling 120 ECTS; titles and codes are cross-checked against 2025/26 guides.", "Bulunan en yeni eksiksiz tablo: 120 AKTS toplamlı 23 bileşen; adlar ve kodlar 2025/26 rehberleriyle çapraz kontrol edildi.", confidence="medium"),
            source(MUSE_MASTER, "MUSE objectives, format and facilities — IDR/UPM", "official_department_page", ["research", "curriculum", "labs"], "Maximum 20 places, project-based learning, IDR project participation, ESA-supported concurrent design and space-environment test facilities.", "Azami 20 kontenjan, proje tabanlı öğrenme, IDR projelerine katılım, ESA destekli eşzamanlı tasarım ve uzay ortamı test tesisleri."),
            source(CASE_STUDY_2, "MUSE Case Study 2 learning guide 2025/26", "official_curriculum_page", ["curriculum", "courses", "industry_exposure", "research", "labs"], "Verifies optional external-company collaboration and student use of the ESA-agreement concurrent-design installation, thermal-vacuum lab, prototype lab and UPMSat harness; it does not name an employer as a formal programme partner.", "İsteğe bağlı harici şirket işbirliğini ve öğrencilerin ESA anlaşmalı eşzamanlı tasarım tesisi, termal-vakum laboratuvarı, prototip laboratuvarı ve UPMSat kablo sistemini kullandığını doğrular; herhangi bir işvereni resmî program ortağı olarak adlandırmaz.", access_status="pdf"),
            source(MUSE_NEWS, "MUSE official news and 2026/27 admission notice", "official_department_page", ["program_status", "admission", "research", "student_projects"], "Confirms active 2026/27 admissions, high first-round demand, current selection evidence and recent student space projects.", "Aktif 2026/27 kabulünü, yüksek ilk tur talebini, güncel seçim kanıtlarını ve yakın tarihli öğrenci uzay projelerini doğrular."),
        ],
    )
    profile.update(
        {
            "official_program_page": PROGRAM,
            "official_admission_page": MUSE_ADMISSION,
            "official_tuition_page": TUITION,
            "official_scholarship_page": SCHOLARSHIP,
            "official_curriculum_page": CURRENT_CURRICULUM,
            "official_department_page": MUSE_MASTER,
            "official_housing_page": HOUSING,
            "official_cost_of_living_page": WELCOME_GUIDE,
            "official_lab_pages": [CASE_STUDY_2],
            "student_sentiment_sources": [item["url"] for item in row["student_sentiment_profile"]["student_sentiment_sources"]],
            "last_verified": CHECKED,
            "needs_verification": False,
            "verification_notes": bi(
                "All decision-critical groups have checked official evidence. Deliberate unknowns remain where the university does not publish a value: numeric GPA floor, GRE score, accepted Spanish certificate list, automatic admission funding, newly arrived non-EU eligibility for the current Santander aid, and a current complete Madrid living-cost total.",
                "Tüm karar-kritik gruplarda kontrol edilmiş resmî kanıt vardır. Üniversitenin değer yayımlamadığı alanlar bilinçli olarak bilinmiyor bırakılmıştır: sayısal GNO alt sınırı, GRE puanı, kabul edilen İspanyolca sertifika listesi, otomatik kabul bursu, yeni gelen AB dışı öğrencinin güncel Santander desteğine uygunluğu ve Madrid için güncel tam yaşam maliyeti.",
            ),
            "field_confidence": {
                "program_basic_info": "high",
                "program": "high",
                "language": "high",
                "admission": "high",
                "non_eu_eligibility": "high",
                "tuition": "high",
                "scholarship": "high",
                "curriculum": "high",
                "research": "high",
                "industry": "high",
                "living": "medium",
                "housing": "high",
                "student_sentiment": "low",
                "location": "medium",
                "deadline": "high",
                "deadlines": "high",
            },
        }
    )

    row["decision_summary"] = {
        "best_for": [
            bi("Spanish-B2-or-stronger students seeking a direct, system-level spacecraft engineering master's.", "Doğrudan, sistem düzeyinde uzay aracı mühendisliği yüksek lisansı arayan B2 veya daha iyi İspanyolcalı öğrenciler."),
            bi("Applicants who value small cohorts, project-based work and access to concurrent-design and environmental-test facilities.", "Küçük sınıfı, proje tabanlı çalışmayı ve eşzamanlı tasarım/çevresel test tesislerine erişimi önemseyen adaylar."),
        ],
        "not_ideal_for": [
            bi("English-only applicants.", "Yalnızca İngilizce eğitim arayan adaylar."),
            bi("Students needing guaranteed university housing or automatic admission funding.", "Garantili üniversite yurdu veya otomatik kabul bursu gereken öğrenciler."),
        ],
        "main_strengths": [
            bi("A 120-ECTS curriculum dedicated to space systems, with 23 assessed components including three case studies and an 18-ECTS thesis.", "Üç case study ve 18 AKTS tez dâhil 23 değerlendirilen bileşenli, uzay sistemlerine adanmış 120 AKTS müfredat."),
            bi("IDR/UPM research setting with ESA-supported concurrent-design and integration/testing infrastructure.", "ESA destekli eşzamanlı tasarım ve entegrasyon/test altyapısına sahip IDR/UPM araştırma ortamı."),
            bi("Small advertised cohort (maximum 20 places) and verified project-based learning.", "İlan edilen küçük sınıf (azami 20 kontenjan) ve doğrulanmış proje tabanlı öğrenme."),
        ],
        "main_risks": [
            bi("Spanish B2 is required for applicants from non-Spanish-speaking countries; the programme is not English-taught.", "İspanyolca konuşulmayan ülkelerden gelenler için B2 İspanyolca gerekir; program İngilizce değildir."),
            bi("Non-EU students without resident/EU-regime status pay €84.07 per ECTS, and a study-stay permit does not count as residence for the fee tariff.", "İkamet/AB rejimi statüsü olmayan AB dışı öğrenciler AKTS başına 84,07 € öder; öğrenci kalış izni ücret tarifesinde ikamet sayılmaz."),
            bi("UPM does not allocate university housing; Madrid accommodation must be arranged independently.", "UPM üniversite yurdu tahsis etmez; Madrid konaklaması bağımsız olarak ayarlanmalıdır."),
            bi("Selective small-cohort admission; interview, requested video or a mathematics/physics test may enter the process.", "Küçük sınıf için seçici kabul; mülakat, talep edilen video veya matematik/fizik sınavı sürece girebilir."),
        ],
        "application_reality": bi(
            "For a Turkish applicant, the realistic path is: document legalisation/Apostille and grade-equivalence preparation, B2 Spanish evidence, a strong first-choice MUSE application with motivation and references, and an early first-round submission for visa time. Budget roughly €5,044.20 first-enrolment tuition for a 60-ECTS year plus published administrative charges if classified as a non-EU nonresident; do not assume a scholarship or UPM housing place.",
            "Türk bir aday için gerçekçi yol: belge tasdiki/Apostil ve not eşdeğerliği hazırlığı, B2 İspanyolca kanıtı, motivasyon ve referanslarla güçlü bir ilk-tercih MUSE başvurusu ve vize süresi için erken ilk tur başvurusu. AB dışı ikamet etmeyen olarak sınıflandırılırsanız 60 AKTS yıllık ilk kayıt öğrenim ücreti yaklaşık 5.044,20 € artı yayımlanan idari ücretleri bütçeleyin; burs veya UPM yurt yeri varsaymayın.",
        ),
        "overall_recommendation": bi(
            "A technically strong direct-space option for applicants who already meet the Spanish requirement and can carry the non-EU fee and independent-housing risk.",
            "İspanyolca şartını halihazırda karşılayan ve AB dışı ücret ile bağımsız konut riskini taşıyabilen adaylar için teknik olarak güçlü, doğrudan uzay odaklı bir seçenek.",
        ),
        "recommended_user_profile": bi("Spanish-capable aerospace/related engineering graduate targeting spacecraft systems and applied project work.", "Uzay aracı sistemleri ve uygulamalı proje çalışmasını hedefleyen, İspanyolca bilen havacılık-uzay/ilgili mühendislik mezunu."),
    }

    row["scoring_inputs"] = {
        "academic_field_fit_score_seed": None,
        "eligibility_language_score_seed": None,
        "cost_funding_score_seed": None,
        "career_research_score_seed": None,
        "living_risk_score_seed": None,
        "data_confidence_score_seed": None,
        "hard_filter_flags": {
            "english_only_compatible": False,
            "requires_spanish": True,
            "requires_italian": False,
            "non_eu_eligible": True,
            "tuition_above_5000": True,
            "tuition_above_10000": False,
            "deadline_unclear": False,
            "university_housing_offered": False,
            "automatic_admission_scholarship_verified": False,
            "needs_verification": False,
        },
    }

    quality = audit_record(row)
    quality["audited_at"] = CHECKED
    row["data_quality"] = quality
    complete = quality["status"] == "verified"
    row["quality_control"] = {
        "qc_status": "passed" if complete else "needs_revision",
        "checked_at": CHECKED,
        "failed_canary_tests": [] if complete else ["missing_or_unverified_critical_fields"],
        "remaining_verification_tasks": [],
        "qc_notes": bi(
            "Decision-critical official evidence is complete. Unknown values and the low-confidence, non-MUSE sentiment sample are displayed as uncertainty rather than inferred facts.",
            "Karar-kritik resmî kanıtlar tamamdır. Bilinmeyen değerler ve düşük güvenli, MUSE'ye özgü olmayan duygu örneklemi çıkarım yapılmış gerçekler yerine belirsizlik olarak gösterilir.",
        ),
    }
    profile["needs_verification"] = not complete


def main() -> None:
    payload = json.loads(PATH.read_text(encoding="utf-8"))
    rows = payload if isinstance(payload, list) else payload.get("universities", payload.get("programs", []))
    target = next(row for row in rows if row.get("id") == RECORD_ID)
    update(target)
    if isinstance(payload, dict):
        payload["last_updated"] = CHECKED
    PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(target["data_quality"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
