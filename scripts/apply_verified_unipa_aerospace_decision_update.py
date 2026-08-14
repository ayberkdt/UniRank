"""Apply current official decision evidence to UniPa Aerospace Engineering MSc."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from unirank.core.integrity import audit_record


DATA_PATH = ROOT / "data_base" / "italy.json"
CHECKED = "2026-08-14"

PROGRAM = "https://www.unipa.it/dipartimenti/ingegneria/cds/ingegneriaaerospaziale2380"
OFFER = "https://www.unipa.it/Avvio-procedure-di-definizione-dellOfferta-Formativa-2026-2027/"
REGULATIONS = "https://www.unipa.it/dipartimenti/ingegneria/cds/ingegneriaaerospaziale2380/regolamenti.html"
COURSES = "https://www.unipa.it/dipartimenti/ingegneria/cds/ingegneriaaerospaziale2380/?pagina=insegnamenti"
EXTRA_EU = "https://www.unipa.it/mobilita/new-students/new-students---enrolment/enrolment-procedures-for-extra-eu-foreign-students/index.html"
LANGUAGE = "https://www.unipa.it/mobilita/new-students/admission-requirements/"
TUITION = "https://www.unipa.it/Tasse-universitarie-00001/"
ERSU = "https://www.ersusiciliani.it/notify/pagina-dedicata-al-concorso-benefici-per-la-a-2026-2027/"
ERSU_FAQ = "https://www.ersusiciliani.it/notify/faq-al-bando-di-concorso-per-lattribuzione-di-borse-di-studio-altri-contributi-economici-e-servizi-per-il-diritto-allo-studio-universitario-per-la-a-2026-2027/"
ERSU_CALL = "https://backoffice.lumsa.it/sites/default/files/file/4176/2026-06/Bando%20di%20Concorso%20dell%27ERSU%20di%20Palermo%20a.a.%202026_2027%20%281%29.pdf"
HOUSING_SERVICE = "https://www.unipa.it/target/studenti-iscritti/vivere-la-citta/servizio-alloggi-unipa/index.html"
RESEARCH = "https://www.unipa.it/dipartimenti/ingegneria/aerospace-manufacturing-mechanical-and-management-engineering/index.html"


def bi(en: str, tr: str) -> dict[str, str]:
    return {"en": en, "tr": tr}


def source(
    url: str,
    title: str,
    source_type: str,
    fields: list[str],
    *,
    access_status: str = "ok",
    confidence: str = "high",
    notes: dict[str, str] | None = None,
) -> dict:
    return {
        "url": url,
        "title": title,
        "source_type": source_type,
        "access_status": access_status,
        "last_checked": CHECKED,
        "relevant_fields": fields,
        "confidence": confidence,
        "notes": notes
        or bi(
            "Current official source checked for the listed fields; unpublished values are not inferred.",
            "Listelenen alanlar için güncel resmî kaynak kontrol edildi; yayımlanmayan değerler türetilmez.",
        ),
    }


def upsert_sources(profile: dict, additions: list[dict]) -> None:
    log = profile.setdefault("source_log", [])
    by_url = {item.get("url"): index for index, item in enumerate(log) if isinstance(item, dict)}
    for item in additions:
        index = by_url.get(item["url"])
        if index is None:
            by_url[item["url"]] = len(log)
            log.append(item)
        else:
            log[index] = item


def finish(row: dict) -> None:
    profile = row["source_profile"]
    profile["last_verified"] = CHECKED
    quality = audit_record(row)
    quality["audited_at"] = CHECKED
    row["data_quality"] = quality
    complete = quality["status"] == "verified"
    if quality["unverified_critical_fields"]:
        failure = "missing_or_unverified_critical_fields"
        remaining = [
            bi(
                f"Resolve remaining critical evidence gaps: {', '.join(quality['unverified_critical_fields'])}.",
                f"Kalan kritik kanıt boşluklarını giderin: {', '.join(quality['unverified_critical_fields'])}.",
            )
        ]
    elif not complete:
        failure = "critical_field_confidence_below_high"
        remaining = [
            bi(
                "Replace the 2025/26 programme regulation and its older linked admission annex when UniPa publishes the 2026/27 versions; add a current official private-rent planning range if published.",
                "UniPa 2026/27 sürümlerini yayımladığında 2025/26 program yönetmeliğini ve onun eski tarihli kabul ekini değiştirin; yayımlanırsa güncel resmî özel kira planlama aralığı ekleyin.",
            )
        ]
    else:
        failure = None
        remaining = []
    row["quality_control"] = {
        "qc_status": "passed" if complete else "needs_revision",
        "checked_at": CHECKED,
        "failed_canary_tests": [] if complete else [failure],
        "remaining_verification_tasks": remaining,
        "qc_notes": bi(
            "Every core decision field has accessible official evidence. Programme-specific admission uses the current regulation landing page but its linked requirements annex is dated 2021, so admission confidence remains medium.",
            "Her temel karar alanında erişilebilir resmî kanıt vardır. Programa özgü kabul için güncel yönetmelik sayfası kullanılır; ancak bağlantılı koşullar eki 2021 tarihli olduğundan kabul güveni orta düzeydedir.",
        ),
    }
    profile["needs_verification"] = not complete


def update(row: dict) -> None:
    row.update(
        {
            "teaching_language": ["Italian"],
            "program_url": PROGRAM,
            "program_status": "active",
            "relevance_status": "strong",
        }
    )

    row["eligibility_profile"].update(
        {
            "eligible_for_non_eu": True,
            "required_previous_degree": bi(
                "A completed first-cycle degree or an equivalent foreign qualification. The programme checks curricular requirements and individual preparation.",
                "Tamamlanmış birinci kademe lisans veya eşdeğer yabancı yeterlilik. Program, müfredat koşullarını ve bireysel hazırlığı denetler.",
            ),
            "accepted_backgrounds": [
                "Aerospace engineering",
                "Other degrees individually assessed against the programme's curricular requirements",
            ],
            "required_ects": {
                "total_subject_specific_cfu": 63,
                "groups": [
                    {"sector": "MAT/05", "cfu": 9},
                    {"sector": "ICAR/08", "cfu": 9},
                    {"sector": "FIS/01", "cfu": 9},
                    {"sector": "ING-IND/04", "cfu": 6},
                    {"sector": "ING-IND/06", "cfu": 9},
                    {"sector": "ING-IND/10", "cfu": 9},
                    {"sector": "ING-IND/15", "cfu": 6},
                    {"sector": "ING-IND/31", "cfu": 6},
                ],
                "foreign_degree_warning": "Italian SSD/CFU equivalence is decided by the programme; the matrix is not a self-certifying guarantee for a foreign transcript.",
            },
            "minimum_gpa": None,
            "ranking_or_selection": "open access with curricular and individual-preparation verification",
            "admission_mode": bi(
                "The UniPa application is first checked administratively and then evaluated by the programme coordinator. Overseas non-EU applicants register in the UniPa portal, await evaluation, and then complete Universitaly pre-enrolment.",
                "UniPa başvurusu önce idari olarak, ardından program koordinatörü tarafından değerlendirilir. Yurt dışındaki AB-dışı aday UniPa portalına kaydolur, değerlendirmeyi bekler ve sonra Universitaly ön kaydını tamamlar.",
            ),
            "admission_risk": "high",
            "required_documents": [
                bi("Valid passport and identity photograph", "Geçerli pasaport ve kimlik fotoğrafı"),
                bi("Bachelor's degree certificate", "Lisans diploması"),
                bi("Transcript of records", "Transkript"),
                bi("Official B2 language certificate or a Medium of Instruction certificate for the application dossier", "Başvuru dosyası için resmî B2 dil belgesi veya Öğretim Dili belgesi"),
                bi("Curriculum vitae", "Özgeçmiş"),
                bi("At arrival: legalised original degree translated into Italian or English", "Varışta: İtalyanca veya İngilizceye çevrilmiş, tasdikli diploma aslı"),
                bi("Declaration of Value, or CIMEA comparability and verification, or an applicable Diploma Supplement", "Değer Beyanı veya CIMEA karşılaştırılabilirlik ve doğrulama belgesi ya da uygulanabilir Diploma Supplement"),
                bi("Legalised and translated prior study plan/transcript for final enrolment", "Kesin kayıt için tasdikli ve çevrilmiş önceki ders planı/transkript"),
            ],
            "cv_required": True,
            "motivation_letter_required": False,
            "recommendation_required": False,
            "portfolio_required": False,
            "interview_required": "conditional",
            "test_required": "conditional_programme_preparation_and_language_checks",
            "gre": {
                "policy": "not_listed_as_required_in_checked_official_sources",
                "test_type": None,
                "minimum_scores": {},
                "recommended_scores": {},
                "validity_rule": None,
                "waiver_rules": [],
                "source_ids": [EXTRA_EU, REGULATIONS],
            },
            "notes_for_turkish_students": bi(
                "A Turkey-resident applicant is eligible through the overseas non-EU route. For the 2026/27 intake, the second and final new-application call closed on 20 July 2026; only applicants who had already opened a UniPa application could start Universitaly by 23 August 2026.",
                "Türkiye'de ikamet eden aday, yurt dışındaki AB-dışı başvuru yolundan uygundur. 2026/27 dönemi için ikinci ve son yeni başvuru çağrısı 20 Temmuz 2026'da kapandı; yalnızca UniPa başvurusunu daha önce açmış adaylar 23 Ağustos 2026'ya kadar Universitaly işlemini başlatabildi.",
            ),
            "verification_notes": bi(
                "The 2025/26 regulation still links an admission-requirements annex last updated in 2021. Its 63-CFU matrix and English-B2 rule are retained as the programme's currently linked rules, but they must be rechecked when a 2026/27 regulation appears. The annex text uses an inconsistent greater-than threshold around 90/110, so no automatic exemption is encoded here.",
                "2025/26 yönetmeliği, son güncellemesi 2021 olan kabul koşulları ekine hâlâ bağlantı verir. 63 CFU matrisi ve İngilizce B2 kuralı programın hâlen bağlantı verdiği kurallar olarak tutulur; 2026/27 yönetmeliği yayımlandığında yeniden kontrol edilmelidir. Ek metni 90/110 çevresinde tutarsız bir büyüktür eşiği kullandığından otomatik muafiyet kodlanmamıştır.",
            ),
        }
    )

    row["language_profile"].update(
        {
            "teaching_language": ["Italian"],
            "teaching_languages": ["Italian"],
            "primary_teaching_language": "Italian",
            "italian_required": True,
            "italian_level_required": "B2 CEFR for visa-requiring applicants to Italian-taught programmes",
            "italian_evidence_modes": ["recognised B2 certificate", "UniPa Italian-language test if required"],
            "english_required": True,
            "english_required_at_entry": True,
            "english_level_required": "B2 CEFR under the programme's currently linked access annex",
            "accepted_english_tests": [],
            "english_exemptions": [],
            "minimum_scores": {},
            "italian_needed_for_life_or_internship": bi(
                "Italian is the official teaching language and is therefore an academic admission requirement, not merely a city-life preference.",
                "İtalyanca resmî öğretim dilidir; bu nedenle yalnızca şehir yaşamı tercihi değil akademik kabul koşuludur.",
            ),
            "mixed_language_warning": bi(
                "Several course titles are in English and the programme separately checks English B2, but the regulation classifies the degree as Italian-taught. An English-only applicant is not compatible with this route.",
                "Bazı ders adları İngilizcedir ve program ayrıca İngilizce B2'yi denetler; ancak yönetmelik dereceyi İtalyanca yürütülen program olarak sınıflandırır. Yalnızca İngilizce bilen aday bu yola uygun değildir.",
            ),
            "language_risk": "high",
            "verification_notes": bi(
                "UniPa's central IELTS 5.5/TOEFL 72 table is explicitly for English-taught programmes, so it is not reused as proof of how this Italian-taught programme accepts its separate English-B2 requirement. Exact accepted English certificates remain unpublished in the checked programme-specific material.",
                "UniPa'nın IELTS 5.5/TOEFL 72 tablosu açıkça İngilizce yürütülen programlar içindir; bu nedenle İtalyanca yürütülen bu programın ayrı İngilizce B2 koşulunu nasıl kabul ettiğinin kanıtı olarak yeniden kullanılmaz. Kabul edilen kesin İngilizce belgeleri, kontrol edilen programa özgü materyalde yayımlanmamıştır.",
            ),
        }
    )

    row["cost_profile"].update(
        {
            "academic_year": "2026/2027",
            "tuition_eur_per_year_min": 356,
            "tuition_eur_per_year_max": 356,
            "tuition_eur_per_year_estimated": 356,
            "tuition_basis": "fixed_country_based_fee_for_non_eu_students_resident_abroad",
            "regional_tax_eur": 140,
            "stamp_duty_eur": 16,
            "student_contribution_eur": 200,
            "enrollment_fee_eur": 356,
            "total_academic_cost_eur_per_year_estimated": 356,
            "isee_or_income_based": False,
            "non_eu_flat_fee": 356,
            "payment_installments": "The current international page lists university-fee payment through 30 November 2026, or 22 December 2026 with a late charge.",
            "tuition_items": [
                {
                    "name": "Country-based flat fee for a Turkey-resident non-EU student",
                    "amount_eur": 356,
                    "academic_year": "2026/2027",
                    "components": {"regional_right_to_study_tax_eur": 140, "stamp_duty_eur": 16, "university_contribution_eur": 200},
                    "reason": "Turkey is not included in UniPa's current List A or List B and therefore falls in the 'other non-EU countries' band.",
                    "source_url": TUITION,
                },
                {
                    "name": "Alternative ISEE parificato route",
                    "amount_eur": None,
                    "components": {"fixed_regional_tax_and_stamp_eur": 156, "variable_income_based_component_eur": None},
                    "source_url": TUITION,
                },
            ],
            "source_notes": bi(
                "A non-EU student resident abroad may choose the country-based flat fee or the ISEE-parificato route. For Turkey, the verified flat option is EUR 356 including regional tax and stamp; the alternative income-based total cannot be known before the applicant's documents are assessed.",
                "Yurt dışında ikamet eden AB-dışı öğrenci ülke bazlı sabit ücreti veya eşdeğer ISEE yolunu seçebilir. Türkiye için doğrulanan sabit seçenek, bölgesel vergi ve damga dahil 356 EUR'dur; alternatif gelir bazlı toplam adayın belgeleri değerlendirilmeden bilinemez.",
            ),
            "verification_notes": bi(
                "EUR 356 is an exact current flat-fee option for the target Turkey-resident applicant, not a tuition estimate. It should not be combined with the EUR 156 fixed component of the alternative ISEE route.",
                "356 EUR, hedef Türkiye'de ikamet eden aday için kesin güncel sabit ücret seçeneğidir; tahmin değildir. Alternatif ISEE yolundaki 156 EUR sabit bileşenle toplanmamalıdır.",
            ),
        }
    )

    row["scholarship_profile"].update(
        {
            "regional_scholarship_available": True,
            "regional_scholarship_name": "ERSU Palermo 2026/27 scholarship, accommodation and catering benefits",
            "non_eu_eligible": True,
            "income_based": True,
            "application_mode": "separate",
            "automatic_consideration": False,
            "separate_application_required": True,
            "scholarship_deadline": "2026-07-22T14:00:00+02:00",
            "scholarship_application_url": "https://studenti.ersupalermo.it/",
            "financial_thresholds": {"isee_eur_max": 23000, "ispe_eur_max": 52500},
            "opportunities": [
                {"name": "ERSU off-campus base benefit", "amount_eur": 7171.11, "source_url": ERSU_CALL},
                {"name": "ERSU commuter base benefit", "amount_eur": 4190.71, "source_url": ERSU_CALL},
                {"name": "ERSU local base benefit", "amount_eur": 2890.16, "source_url": ERSU_CALL},
                {
                    "name": "ERSU off-campus benefit for ISEE below 50% of the ceiling",
                    "amount_eur": 8246.78,
                    "condition": "ISEE below EUR 11,500; service-value deductions can still apply",
                    "source_url": ERSU_CALL,
                },
            ],
            "available_types": ["cash scholarship", "competitive free bed", "canteen service", "regional-tax refund for awardees and eligible non-awardees"],
            "funding_competitiveness": "high",
            "international_document_rules": {
                "portal_access_without_spid": True,
                "isee_type": "ISEEU/ISPEU parificato calculated by an Italian CAF",
                "foreign_documents": "issued by competent authorities, translated into Italian and legalised where required",
                "housing_ranking_document_deadline": "2026-09-10T14:00:00+02:00",
                "final_scholarship_regularisation_deadline": "2026-11-30T14:00:00+01:00",
            },
            "funding_notes": bi(
                "The ERSU application was separate from UniPa admission and closed on 22 July 2026. International students without Italian residence could register with ERSU credentials. The off-campus base total includes service values: in Palermo, a free ERSU bed deducts EUR 1,700 and catering can deduct EUR 1,200 from cash, leaving services plus the applicable cash balance rather than the full total as cash.",
                "ERSU başvurusu UniPa kabulünden ayrıydı ve 22 Temmuz 2026'da kapandı. İtalya'da ikameti olmayan uluslararası öğrenciler ERSU kullanıcı bilgileriyle kayıt olabildi. Şehir dışı temel toplamı hizmet değerlerini içerir: Palermo'da ücretsiz ERSU yatağı nakit tutardan 1.700 EUR, yemek hizmeti 1.200 EUR düşebilir; bu nedenle toplamın tamamı nakit değil, hizmetler artı uygulanabilir nakit bakiyedir.",
            ),
            "verification_notes": bi(
                "The signed ERSU call is accessed through an institutional LUMSA mirror because the official procurement download returns HTTP 403; the current ERSU page links the same call. First-year academic merit is checked after award: 15 CFU by 10 August 2027 and 20 CFU by 30 November 2027 are required for the full balance/retention rules.",
                "İmzalı ERSU çağrısına, resmî ihale indirme bağlantısı HTTP 403 verdiği için kurumsal LUMSA aynası üzerinden erişilir; güncel ERSU sayfası aynı çağrıya bağlantı verir. İlk yıl akademik başarı ödül sonrasında denetlenir: tam bakiye/koruma kuralları için 10 Ağustos 2027'ye kadar 15 CFU ve 30 Kasım 2027'ye kadar 20 CFU gerekir.",
            ),
        }
    )

    row["living_profile"].update(
        {
            "city_cost_level": "unknown_without_current_official_private_rent_range",
            "monthly_living_cost_eur_min": None,
            "monthly_living_cost_eur_max": None,
            "monthly_living_cost_eur_estimated": None,
            "housing_difficulty": "competitive_ersu_ranking_private_market_price_not_verified",
            "student_housing_available": True,
            "student_housing_competitiveness": "high",
            "housing_access": "not_guaranteed",
            "housing_application_separate": True,
            "housing_difficulty_score": None,
            "living_risk": "high",
            "housing_options": [
                {
                    "provider": "ERSU Palermo",
                    "type": "free bed for ranked scholarship/housing applicants",
                    "palermo_beds_total": 913,
                    "ordinary_first_year_beds": 289,
                    "ordinary_later_year_beds": 580,
                    "reserved_palermo_beds": 44,
                    "allocation": "income-ranked for first-year applicants, with later scrolling rounds",
                    "guaranteed": False,
                    "source_url": ERSU_CALL,
                },
                {
                    "provider": "UniPa Housing Service",
                    "type": "free search and contract-support service for screened private housing",
                    "price_published": False,
                    "guaranteed": False,
                    "source_url": HOUSING_SERVICE,
                },
            ],
            "official_rent_items": [
                {
                    "scenario": "ERSU scholarship/housing winner assigned a bed",
                    "monthly_rent_eur": 0,
                    "service_value_deducted_from_total_scholarship_eur": 1700,
                    "deposit_eur_min": 0,
                    "deposit_eur_max": 100,
                    "warning": "Competitive benefit only; not a Palermo private-market rent estimate",
                    "source_url": ERSU_CALL,
                }
            ],
            "official_living_cost_items": [],
            "housing_notes": bi(
                "ERSU beds are free to assignees but are allocated by ranking and scrolling rounds. The call lists 913 Palermo beds, including 289 ordinary first-year beds, and residence-specific deposits of EUR 0, 50 or 100. A EUR 170 monthly charge applies only where a residence fee is due under the call; scholarship-benefit beds are described as free. Private Palermo rent is intentionally unknown because no current official planning range was verified.",
                "ERSU yatakları atanan öğrenci için ücretsizdir; ancak sıralama ve kaydırma turlarıyla dağıtılır. Çağrı Palermo için 289'u normal ilk yıl kontenjanı olmak üzere 913 yatak ve yurda göre 0, 50 veya 100 EUR depozito listeler. Aylık 170 EUR yalnızca çağrı kapsamında yurt ücreti doğan durumlarda geçerlidir; burs-hizmet yatakları ücretsiz olarak tanımlanır. Güncel resmî planlama aralığı doğrulanmadığından Palermo özel kira tutarı bilinmiyor bırakılır.",
            ),
            "verification_notes": bi(
                "Do not display the conditional zero-rent ERSU item as the city's normal housing cost. It is a competitive in-kind scholarship service, and private housing still requires a separate search and registered contract.",
                "Koşullu sıfır kiralı ERSU kalemi şehrin normal konut maliyeti olarak gösterilmemelidir. Bu, rekabetçi ayni burs hizmetidir; özel konut yine ayrı arama ve kayıtlı sözleşme gerektirir.",
            ),
        }
    )

    row["curriculum_profile"].update(
        {
            "tracks": ["Single Aerospace Engineering curriculum"],
            "specializations": [],
            "mandatory_courses": [
                "Aeroelasticity (6 CFU)",
                "Aerospace Propulsion (12 CFU)",
                "Automatic Control (9 CFU)",
                "Gas Dynamics (9 CFU)",
                "Aerospace Structures (12 CFU)",
                "Aeronautical Production Technologies (9 CFU)",
                "Aircraft Conceptual Design (9 CFU; displayed for the second-year 2025/26 cohort)",
                "Flight Dynamics (12 CFU; displayed for the second-year 2025/26 cohort)",
            ],
            "elective_courses": [
                "Additive Manufacturing",
                "Experimental Stress Analysis",
                "Numerical Analysis",
                "Computational Fluid Dynamics",
                "Corrosion and Protection of Aerospace Materials",
                "Estimation, Filtering and System Identification",
                "Machine Learning for Aerospace Engineering",
                "Mobile and Distributed Robotics",
                "Process Design",
                "Science and Technology of Composite Materials for Aerospace Engineering",
            ],
            "current_live_course_count": {
                "first_year_2026_27_mandatory_taught_courses": 6,
                "second_year_2025_26_top_level_taught_offerings": 12,
                "second_year_optional_top_level_offerings": 10,
                "warning": "This live delivery count spans two cohorts and is not every student's exam count; integrated-course child modules are excluded.",
            },
            "exact_course_count": None,
            "course_language_notes": bi(
                "The official regulation says Italian. English course titles do not establish a fully English pathway.",
                "Resmî yönetmelik öğretim dilini İtalyanca olarak belirtir. İngilizce ders adları tamamen İngilizce bir yol oluşturmaz.",
            ),
            "thesis_required": True,
            "thesis_ects": 15,
            "internship_required": None,
            "lab_courses": [],
            "project_based_courses": ["Final aerospace project or research thesis"],
            "curriculum_url": COURSES,
            "study_plan_url": REGULATIONS,
            "verification_notes": bi(
                "The live page is cohort-aware: it displays first-year 2026/27 teaching and second-year 2025/26 teaching. Therefore no false single exact exam count is asserted. The 2025/26 regulation assigns 15 CFU to the final thesis; a current study-plan annex should be checked for the remaining elective/stage allocation.",
                "Canlı sayfa kohortları ayırır: 2026/27 birinci yıl ile 2025/26 ikinci yıl derslerini birlikte gösterir. Bu nedenle yanıltıcı tek bir kesin sınav sayısı verilmez. 2025/26 yönetmeliği bitirme tezine 15 CFU ayırır; kalan seçmeli/staj dağılımı için güncel ders planı eki kontrol edilmelidir.",
            ),
        }
    )

    row["category_profile"].update(
        {
            "primary_categories": ["aerospace_engineering"],
            "secondary_categories": ["aeronautical_engineering", "space_engineering"],
            "subcategories": ["aerodynamics_and_cfd", "aerospace_structures", "propulsion", "flight_dynamics_and_control", "aerospace_manufacturing"],
            "normalized_tags": ["aeroelasticity", "CFD", "propulsion", "structures", "flight dynamics", "controls", "composites", "machine learning"],
            "category_scores": {},
        }
    )

    row["research_profile"].update(
        {
            "department_research_areas": [
                "aerospace structures and lightweight composite materials",
                "computational fluid dynamics and aeroacoustics",
                "aircraft engines and rocket propulsion",
                "structural health monitoring and smart structures",
                "advanced aerospace manufacturing",
            ],
            "labs": [
                "Aerospace Laboratory",
                "Virtual Reality Laboratory",
                "Materials and Biomaterials Mechanics Laboratory at ATeN Centre",
            ],
            "research_centers": ["ATeN Centre"],
            "space_or_aerospace_projects": [],
            "research_strength_summary": bi(
                "The current department explicitly covers aerospace structures, CFD, aircraft engines and rocket propulsion. The profile is technically direct but the checked sources do not prove a dedicated satellite programme or guaranteed MSc access to every laboratory.",
                "Güncel bölüm açıkça havacılık-uzay yapıları, HAD, uçak motorları ve roket itki araştırmalarını kapsar. Profil teknik olarak doğrudandır; ancak kontrol edilen kaynaklar özel bir uydu programını veya her laboratuvara garantili yüksek lisans erişimini kanıtlamaz.",
            ),
            "research_strength_score": None,
            "research_sources": [RESEARCH],
        }
    )

    row["industry_ecosystem_profile"].update(
        {
            "nearby_companies": [],
            "space_agencies_or_public_bodies": [],
            "research_institutes": [],
            "internship_possibility": "The regulation allows thesis work with collaborating public or private organisations; no named current partner is asserted here.",
            "thesis_with_industry_possibility": "possible_subject_to_a_verified_collaboration_not_guaranteed",
            "career_relevance": "direct aerospace curriculum",
            "ecosystem_strength_score": None,
            "ecosystem_notes": bi(
                "Current programme news advertises aerospace/engineering vacancies, but an advertised vacancy is not an official university partnership. Named company partnerships remain unverified.",
                "Güncel program haberleri havacılık-uzay/mühendislik ilanları yayımlar; ancak ilan yayımlanması resmî üniversite ortaklığı değildir. İsimli şirket ortaklıkları doğrulanmamıştır.",
            ),
            "confirmed_partners": [],
        }
    )

    row["application_timeline_profile"].update(
        {
            "academic_year": "2026/2027",
            "intake_terms": ["Autumn 2026"],
            "application_rounds": [
                {"name": "First overseas non-EU master's call", "opens": "2026-01-15", "closes": "2026-03-15", "status": "closed"},
                {"name": "Second overseas non-EU master's call", "opens": "2026-04-15", "closes": "2026-07-20", "status": "closed"},
            ],
            "non_eu_deadline": "2026-07-20T23:59:59+02:00",
            "eu_deadline": None,
            "scholarship_deadline": "2026-07-22T14:00:00+02:00",
            "pre_enrolment_required": True,
            "universitaly_required": True,
            "visa_sensitive_deadline": "2026-08-23",
            "application_result_timing": "Administrative screening followed by programme-coordinator evaluation; no fixed turnaround is published.",
            "enrollment_deadline": "2026-11-30; late university-fee payment through 2026-12-22 with a surcharge",
            "timeline_risk": "high",
            "application_deadline": "2026-07-20T23:59:59+02:00",
            "deadline_events": [
                {"event": "first_overseas_non_eu_master_call", "opens": "2026-01-15", "deadline": "2026-03-15", "status": "closed", "source_url": EXTRA_EU},
                {"event": "second_overseas_non_eu_master_call", "opens": "2026-04-15", "deadline": "2026-07-20", "status": "closed", "source_url": EXTRA_EU},
                {"event": "ersu_scholarship_and_housing_application", "opens": "2026-06-05", "deadline": "2026-07-22T14:00:00+02:00", "status": "closed", "source_url": ERSU_CALL},
                {"event": "universitaly_start_for_already_opened_unipa_applications", "opens": "2026-04", "deadline": "2026-08-23", "status": "closed_for_new_unipa_applicants", "source_url": EXTRA_EU},
                {"event": "ersu_isee_for_housing_ranking", "deadline": "2026-09-10T14:00:00+02:00", "status": "future_for_existing_applicants", "source_url": ERSU_CALL},
                {"event": "unipa_fee_payment", "deadline": "2026-11-30", "status": "future_for_admitted_applicants", "source_url": EXTRA_EU},
                {"event": "ersu_final_international_regularisation", "deadline": "2026-11-30T14:00:00+01:00", "status": "future_for_existing_applicants", "source_url": ERSU_CALL},
                {"event": "late_unipa_fee_payment_with_surcharge", "deadline": "2026-12-22", "status": "future_for_admitted_applicants", "source_url": EXTRA_EU},
            ],
            "deadline_notes": bi(
                "As of 14 August 2026, neither a new UniPa overseas application nor a new ERSU application can be started for this intake. The 23 August Universitaly step is only for applicants who had already started a UniPa application; it is not a third admission round.",
                "14 Ağustos 2026 itibarıyla bu dönem için ne yeni UniPa yurt dışı başvurusu ne de yeni ERSU başvurusu başlatılabilir. 23 Ağustos Universitaly adımı yalnızca UniPa başvurusunu daha önce başlatmış adaylar içindir; üçüncü bir kabul turu değildir.",
            ),
        }
    )

    profile = row["source_profile"]
    profile.update(
        {
            "official_program_page": PROGRAM,
            "official_admission_page": EXTRA_EU,
            "official_tuition_page": TUITION,
            "official_scholarship_page": ERSU,
            "official_curriculum_page": COURSES,
            "official_department_page": RESEARCH,
            "official_lab_pages": [RESEARCH],
            "verification_notes": bi(
                "The record separates current 2026/27 central admissions, tuition and ERSU facts from the 2025/26 programme regulation. No stale admission date, private-rent estimate or industry partnership is promoted as current fact.",
                "Kayıt, güncel 2026/27 merkezi kabul, ücret ve ERSU bilgilerini 2025/26 program yönetmeliğinden ayırır. Eski kabul tarihi, özel kira tahmini veya sektör ortaklığı güncel gerçek olarak sunulmaz.",
            ),
            "field_confidence": {
                "program_basic_info": "high",
                "language": "high",
                "admission": "medium",
                "non_eu_eligibility": "high",
                "tuition": "high",
                "scholarship": "high",
                "curriculum": "high",
                "research": "high",
                "industry": "unknown",
                "living": "unknown",
                "housing": "high",
                "deadlines": "high",
                "deadline": "high",
            },
        }
    )
    upsert_sources(
        profile,
        [
            source(PROGRAM, "Current LM-20 Aerospace Engineering programme page — UniPa", "official_program_page", ["program", "program_status"]),
            source(OFFER, "2026/27 UniPa study offer activation", "official_program_page", ["program", "program_status"]),
            source(
                REGULATIONS,
                "Aerospace Engineering 2025/26 regulation and annexes — UniPa",
                "official_admission_page",
                ["language", "admission", "curriculum"],
                confidence="medium",
                notes=bi(
                    "The current landing page links the 2025/26 regulation (Italian teaching language and 15-CFU thesis) and an access annex last updated in 2021 (63-CFU matrix and English B2).",
                    "Güncel sayfa; 2025/26 yönetmeliğine (İtalyanca öğretim dili ve 15 CFU tez) ve son güncellemesi 2021 olan kabul ekine (63 CFU matrisi ve İngilizce B2) bağlantı verir.",
                ),
            ),
            source(COURSES, "Live 2026/27 and 2025/26 course delivery — UniPa", "official_curriculum_page", ["curriculum", "courses"]),
            source(EXTRA_EU, "2026/27 overseas non-EU admission and enrolment — UniPa", "official_admission_page", ["admission", "non_eu_eligibility", "deadline", "tuition"]),
            source(LANGUAGE, "Current language admission requirements — UniPa", "official_university_policy_page", ["language", "admission", "non_eu_eligibility"]),
            source(TUITION, "Current tuition options for non-EU students resident abroad — UniPa", "official_tuition_page", ["tuition", "non_eu_eligibility"]),
            source(ERSU, "2026/27 ERSU Palermo benefits call landing page", "official_scholarship_page", ["scholarship", "housing", "deadline"]),
            source(ERSU_FAQ, "2026/27 ERSU Palermo benefits FAQ", "official_scholarship_page", ["scholarship", "housing"], notes=bi("Current ERSU FAQ confirms economic ceilings, international ISEE support and ranked accommodation treatment.", "Güncel ERSU SSS sayfası ekonomik eşikleri, uluslararası ISEE desteğini ve sıralamalı yurt uygulamasını doğrular.")),
            source(
                ERSU_CALL,
                "Signed ERSU Palermo 2026/27 scholarship and housing call — institutional LUMSA mirror",
                "official_scholarship_page",
                ["scholarship", "housing", "deadline", "non_eu_eligibility"],
                access_status="pdf",
                notes=bi(
                    "The signed ERSU document is mirrored by LUMSA, an institution covered by this ERSU call; the current ERSU landing page links the same call but its procurement download returns HTTP 403.",
                    "İmzalı ERSU belgesi, bu çağrı kapsamındaki LUMSA tarafından aynalanır; güncel ERSU sayfası aynı çağrıya bağlantı verir ancak ihale indirmesi HTTP 403 döndürür.",
                ),
            ),
            source(HOUSING_SERVICE, "UniPa Housing Service for off-campus and international students", "official_housing_page", ["housing"]),
            source(RESEARCH, "Aerospace, Manufacturing, Mechanical and Management Engineering research areas — UniPa", "official_department_page", ["research", "labs", "department"]),
        ],
    )

    row["decision_summary"] = {
        "best_for": [
            bi("Italian-speaking applicants seeking a direct LM-20 aerospace degree with strong structures, CFD, propulsion and manufacturing coverage", "Yapılar, HAD, itki ve üretim kapsamı güçlü, doğrudan LM-20 havacılık-uzay derecesi arayan İtalyanca bilen adaylar"),
            bi("Cost-sensitive Turkey-resident applicants who can use the verified EUR 356 flat-fee route", "Doğrulanmış 356 EUR sabit ücret yolunu kullanabilen, maliyet duyarlı Türkiye'de ikamet eden adaylar"),
        ],
        "not_ideal_for": [
            bi("English-only applicants", "Yalnızca İngilizce bilen adaylar"),
            bi("Applicants who missed the 20 July 2026 UniPa or 22 July 2026 ERSU deadlines", "20 Temmuz 2026 UniPa veya 22 Temmuz 2026 ERSU son tarihlerini kaçıran adaylar"),
            bi("Applicants who require guaranteed university housing", "Garantili üniversite yurdu isteyen adaylar"),
        ],
        "main_strengths": [
            bi("Direct aerospace curriculum across propulsion, gas dynamics, aeroelasticity, structures, flight dynamics, controls and manufacturing", "İtki, gaz dinamiği, aeroelastisite, yapılar, uçuş dinamiği, kontrol ve üretimi kapsayan doğrudan havacılık-uzay müfredatı"),
            bi("Low verified country-based fee for a Turkey-resident non-EU applicant", "Türkiye'de ikamet eden AB-dışı aday için düşük, doğrulanmış ülke bazlı ücret"),
            bi("Substantial separate ERSU need-based benefits, including competitive housing and meals", "Rekabetçi yurt ve yemek dahil kayda değer ayrı ERSU ihtiyaç temelli yardımları"),
        ],
        "main_risks": [
            bi("Both Italian B2 for the Italian-taught route and programme-level English B2 preparation are relevant", "İtalyanca yürütülen yol için İtalyanca B2 ve programa özgü İngilizce B2 hazırlığı birlikte önemlidir"),
            bi("The programme-specific access annex is older than the 2026/27 central admission cycle", "Programa özgü kabul eki 2026/27 merkezi kabul döneminden eskidir"),
            bi("ERSU funding and beds require a separate early application, financial documentation and ranking", "ERSU bursu ve yatağı ayrı erken başvuru, mali belgeler ve sıralama gerektirir"),
            bi("No current official Palermo private-rent planning range is retained", "Güncel resmî Palermo özel kira planlama aralığı tutulmamıştır"),
        ],
        "application_reality": bi(
            "For 2026/27 the route is closed to new applicants as of the verification date. A future applicant should prepare Italian B2, English B2, the degree/transcript/CV package and legalised financial records before the January admission and June ERSU cycles open.",
            "Doğrulama tarihi itibarıyla 2026/27 yolu yeni adaylara kapalıdır. Gelecek dönem adayı, Ocak kabul ve Haziran ERSU döngüleri açılmadan önce İtalyanca B2, İngilizce B2, diploma/transkript/CV paketini ve tasdikli mali belgeleri hazırlamalıdır.",
        ),
        "overall_recommendation": bi(
            "Strong technical-value option for an Italian-capable, deadline-disciplined applicant; unsuitable as an English-only fallback.",
            "İtalyanca bilen ve son tarih disiplinine sahip aday için teknik değer açısından güçlü seçenek; yalnızca İngilizceyle yedek plan olmaya uygun değil.",
        ),
        "recommended_user_profile": bi(
            "Turkey-resident engineering graduate with Italian B2, English B2, a transcript matching the 63-CFU matrix and financial documents ready well before ERSU closes.",
            "İtalyanca B2 ve İngilizce B2 sahibi, transkripti 63 CFU matrisine uyan ve mali belgeleri ERSU kapanmadan çok önce hazır Türkiye'de ikamet eden mühendislik mezunu.",
        ),
    }

    row["scoring_inputs"].update(
        {
            "academic_field_fit_score_seed": None,
            "eligibility_language_score_seed": None,
            "cost_funding_score_seed": None,
            "career_research_score_seed": None,
            "living_risk_score_seed": None,
            "data_confidence_score_seed": None,
            "hard_filter_flags": {
                "english_only_compatible": False,
                "requires_italian": True,
                "non_eu_eligible": True,
                "tuition_above_5000": False,
                "tuition_above_10000": False,
                "deadline_unclear": False,
                "deadline_closed_for_new_applicants": True,
                "housing_guaranteed": False,
                "needs_verification": True,
            },
        }
    )
    finish(row)


def main() -> None:
    payload = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    target = next(row for row in payload["universities"] if row.get("id") == "unipa_aerospace_master")
    update(target)
    payload["last_updated"] = CHECKED
    DATA_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(target["data_quality"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
