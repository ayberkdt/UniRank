"""Apply current official decision evidence to the joint UniSalento/PoliBa Aerospace MSc."""

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
JOINT_ID = "it-unisalento-poliba-aerospace-engineering-msc"

MASTER = "https://international.unisalento.it/en/admission/masters-degree"
ENGLISH_DEGREES = "https://www.unisalento.it/didattica/cosa-studiare/corsi-di-studio-in-lingua-inglese"
CALL_INDEX = "https://international.unisalento.it/admission/the-new-admission-notices-for-international-students"
CALL_PDF = "https://international.unisalento.it/documents/970064/0/bando%2BStudenti%2Bstranieri%2B2026-2027_maggio.pdf/a832ae1e-c49a-3e37-1019-a36d50fd168c"
PRE_ENROLMENT = "https://international.unisalento.it/admission/pre-enrolment-and-visa-for-non-eu-students"
POLIBA_PROGRAM = "https://www.poliba.it/en/laurea-magistrale-aerospace-engineering"
JOINT_GOVERNANCE = "https://polibachronicle.poliba.it/politecnico-di-bari-e-universita-del-salento-patto-per-lingegneria-in-puglia/"
HISTORICAL_PROGRAM = "https://international.unisalento.it/studying/international-degree-programmes/-/dettaglio/corso/LM52/aerospace-engineering"
ELEARNING = "https://elearning.unisalento.it/course/index.php?categoryid=120&lang=en"
ADISU_UNISALENTO = "https://international.unisalento.it/admission/scholarships-grants/adisu-scholarships"
ADISU_AMOUNTS = "https://concorsi.regione.puglia.it/web/press-regione/-/diritto-allo-studio-regione-puglia-approva-gli-indirizzi-per-il-bando-adisu-2026-2027"
ADISU_DEADLINE = "https://www.adisupuglia.it/pagina106703_borse-di-studio.html"
ISUFI = "https://trasparenza.unisalento.it/page/5/details/27347/isufi-bando-di-selezione-per-lammissione-di-n-24-allievi-aa-20262027-n-18-posti-per-lammissione-al-1-anno-del-i-livello-n-6-posti-per-lammissione-al-1-anno-del-ii-livello-scadenza-25-agosto-2026-ore-1300.html"
ISUFI_PDF = "https://trasparenza.unisalento.it/download/2038338.html"
ADISU_RESIDENCES = "https://ammtrasparente.adisupuglia.it/index.php?esattamente=&gtp=1&id_cat=0&id_criterio=&id_doc=0&id_ente=348&id_oggetto=0&id_sez_ori=&id_sezione=734&id_sond=&inizio=0&limite=20&ordina_oggetto=55&ordine=indirizzo&purecontent=&senso=&template_ori="
ADISU_NO_RESIDENCE = "https://adisupuglia.it/area_letturaNotizia/392855/pagsistema.html"
ADISU_LEASE_ROUTE = "https://adisupuglia.it/area_letturaNotizia/573391/pagsistema.html"
ASSE = "https://asselab.unisalento.it/"
AIRMOB = "https://trasparenza.unisalento.it/page/75/details/19766/dii-bando-di-selezione-per-titoli-e-colloquio-lassegnazione-di-n-1-incarico-individuale-di-lavoro-autonomo-finanziato-nellambito-del-progetto-airmob-developing-skills-and-capabilities-for-innovative-air-mobility-call-erasmus-edu-2024-pex-cove-topic-erasmus-edu-2024-pex-cove-type-of-action-erasmus-ls-erasmus-lump-sum-grants-proposal-number-101194074-cup-f85e24000560006.html"
ACTIVE_RESEARCH = "https://trasparenza.unisalento.it/page/75/concorsi-attivi.html"


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
) -> dict:
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


def finish(row: dict) -> None:
    quality = audit_record(row)
    quality["audited_at"] = CHECKED
    row["data_quality"] = quality
    complete = quality["status"] == "verified"
    row["quality_control"] = {
        "checked_at": CHECKED,
        "qc_status": "passed" if complete else "needs_revision",
        "remaining_verification_tasks": [] if complete else [
            bi(
                "Resolve the remaining critical evidence or confidence gaps before treating the record as fully verified.",
                "Kaydı tamamen doğrulanmış saymadan önce kalan kritik kanıt veya güven boşluklarını giderin.",
            )
        ],
        "failed_canary_tests": [] if complete else [
            "missing_or_unverified_critical_fields"
            if quality["unverified_critical_fields"]
            else "critical_field_confidence_below_high"
        ],
        "qc_notes": bi(
            "All decision facts are current official-source facts. Exact 2026/27 course count and Brindisi private-rent costs remain unknown rather than being inferred; this does not invalidate the verified high-level curriculum and housing-access findings.",
            "Tüm karar bilgileri güncel resmî kaynaklara dayanır. 2026/27 kesin ders sayısı ve Brindisi özel kira maliyetleri tahmin edilmek yerine bilinmiyor bırakılmıştır; bu durum doğrulanmış üst düzey müfredat ve konuta erişim bulgularını geçersiz kılmaz.",
        ),
    }
    row["source_profile"]["needs_verification"] = not complete


def update_unisalento(row: dict) -> None:
    ranking = row.get("ranking_profile")
    row.update(
        {
            "country": "Italy",
            "university": "Università del Salento",
            "university_native_name": "Università del Salento",
            "city": "Brindisi",
            "region": "Apulia",
            "program_name": "Aerospace Engineering",
            "program_native_name": "Laurea Magistrale in Aerospace Engineering",
            "program_degree": "Master of Science",
            "degree_level": "Master",
            "degree_class": "LM-20 R — Aerospace and Astronautical Engineering",
            "duration_years": 2,
            "ects": 120,
            "teaching_language": ["English"],
            "program_url": MASTER,
            "department": "Department of Engineering for Innovation",
            "campus": "Brindisi (2026/27 UniSalento admission route; teaching-plan locations are in transition)",
            "program_status": "active",
            "relevance_status": "strong",
            "joint_program_id": JOINT_ID,
            "catalogue_relationship": {
                "role": "canonical_administrative_and_application_record",
                "canonical_record_id": "universita-del-salento",
                "partner_record_ids": ["poliba_aerospace_master"],
                "rankable_as_independent_choice": True,
                "joint_degree": True,
                "degree_awarding_institutions": ["Università del Salento", "Politecnico di Bari"],
                "administrative_seat": "Università del Salento",
                "verification_notes": bi(
                    "Official PoliBa governance information identifies UniSalento as the administrative seat and says the jointly awarded degree carries both university logos. The PoliBa record is a teaching-partner view of this same student choice.",
                    "Resmî PoliBa yönetişim bilgisi idari merkezi UniSalento olarak gösterir ve ortak verilen diplomada iki üniversitenin logosunun bulunduğunu belirtir. PoliBa kaydı aynı öğrenci seçeneğinin eğitim ortağı görünümüdür.",
                ),
            },
            "ranking_profile": ranking,
        }
    )

    row["eligibility_profile"] = {
        "eligible_for_non_eu": True,
        "target_applicant_route": "foreign_non_eu_student_resident_abroad_2026_27_second_call",
        "non_eu_quota": 30,
        "required_previous_degree": bi(
            "A completed Bachelor's degree in a relevant industrial-engineering field. The selection committee assesses the academic record and subject fit; the call does not publish a fixed foreign-credit matrix.",
            "İlgili bir endüstri mühendisliği alanında tamamlanmış lisans derecesi. Seçim komisyonu akademik kaydı ve alan uyumunu değerlendirir; çağrı yabancı diplomalar için sabit kredi matrisi yayımlamaz.",
        ),
        "accepted_backgrounds": ["relevant industrial-engineering Bachelor degrees assessed by the committee"],
        "required_ects": {"published_fixed_matrix_for_foreign_degrees": None},
        "minimum_gpa": {"percentage": 70, "rule": "at least 70% of the maximum grade"},
        "gpa_scale": "percentage of the home-system maximum",
        "ranking_or_selection": "academic-record screening plus mandatory Microsoft Teams oral interview",
        "admission_mode": bi(
            "Programme-specific competitive selection for 30 foreign non-EU places. Technical preparation and actual English ability are assessed from the dossier and a mandatory oral interview.",
            "30 yabancı AB-dışı kontenjan için programa özgü rekabetçi seçim. Teknik hazırlık ve gerçek İngilizce düzeyi dosya ile zorunlu sözlü mülakatta değerlendirilir.",
        ),
        "admission_risk": "high",
        "application_fee_eur": 23,
        "interview_required": True,
        "interview_mode": "Microsoft Teams",
        "test_required": True,
        "test_type": "mandatory oral technical and English-language interview",
        "required_documents": [
            bi("Passport", "Pasaport"),
            bi("Bachelor's degree/completion certificate", "Lisans diploması/mezuniyet belgesi"),
            bi("Transcript listing exams, credits, grades and final cumulative average", "Dersler, krediler, notlar ve nihai genel ortalamayı gösteren transkript"),
            bi("B2 English certificate or official Medium of Instruction statement", "B2 İngilizce belgesi veya resmî eğitim dili yazısı"),
            bi("Italian or English versions, with translations and originals where required", "Gerektiğinde çeviriler ve asıllarla birlikte İtalyanca veya İngilizce belgeler"),
        ],
        "motivation_letter_required": False,
        "cv_required": False,
        "recommendation_required": False,
        "portfolio_required": False,
        "notes_for_turkish_students": bi(
            "The university selection is only the academic stage. An admitted Turkey-resident applicant must then complete Universitaly pre-enrolment, obtain university validation and apply for the study visa; an eligibility letter does not guarantee a visa.",
            "Üniversite seçimi yalnızca akademik aşamadır. Kabul edilen Türkiye'de ikamet eden aday daha sonra Universitaly ön kaydını tamamlamalı, üniversite onayı almalı ve öğrenim vizesine başvurmalıdır; uygunluk yazısı vizeyi garanti etmez.",
        ),
        "verification_notes": bi(
            "The 70% average and B2 are minimum screening requirements in the 2026/27 programme call, not preferences. No GRE appears among the required or scored items.",
            "%70 ortalama ve B2, 2026/27 program çağrısındaki asgari eleme koşullarıdır; tercih ölçütü değildir. GRE zorunlu veya puanlanan unsurlar arasında yer almaz.",
        ),
        "gre": {
            "policy": "not_listed_as_required_or_scored_in_checked_2026_27_programme_sources",
            "test_type": None,
            "minimum_scores": {},
            "recommended_scores": {},
            "validity_rule": None,
            "waiver_rules": [],
            "source_ids": [CALL_PDF, CALL_INDEX],
        },
    }

    row["language_profile"] = {
        "teaching_language": ["English"],
        "teaching_languages": ["English"],
        "english_required": True,
        "english_level_required": "B2 CEFR",
        "accepted_english_tests": [],
        "minimum_scores": {},
        "medium_of_instruction_accepted": True,
        "english_exemptions": [bi("Official Medium of Instruction statement is accepted instead of a B2 certificate for application.", "Başvuruda B2 sertifikası yerine resmî eğitim dili yazısı kabul edilir.")],
        "english_interview_assessment_required": True,
        "italian_required": False,
        "italian_level_required": None,
        "italian_needed_for_life_or_internship": bi(
            "Not an entry requirement, but useful for housing, local administration and employment in Brindisi/Lecce/Taranto.",
            "Giriş koşulu değildir; ancak Brindisi/Lecce/Taranto'da konut, yerel işlemler ve çalışma için faydalıdır.",
        ),
        "mixed_language_warning": None,
        "language_risk": "medium",
        "verification_notes": bi(
            "The call publishes B2 or MOI but no programme-specific IELTS/TOEFL minimum table. Actual English is still checked in the mandatory interview.",
            "Çağrı B2 veya eğitim dili yazısını kabul eder; programa özgü IELTS/TOEFL taban puan tablosu yayımlamaz. Gerçek İngilizce düzeyi yine zorunlu mülakatta kontrol edilir.",
        ),
    }

    row["cost_profile"] = {
        "academic_year": "2026/2027",
        "tuition_eur_per_year_min": 1000,
        "tuition_eur_per_year_max": 1000,
        "tuition_eur_per_year_estimated": 1000,
        "tuition_basis": "international_student_flat_tax",
        "non_eu_flat_fee": 1000,
        "isee_or_income_based": False,
        "payment_installments": "3",
        "regional_tax_eur": None,
        "regional_tax_eur_approx": 190,
        "stamp_duty_eur": 16,
        "application_fee_eur": 23,
        "student_contribution_eur": 1000,
        "enrollment_fee_eur": None,
        "total_academic_cost_eur_per_year_estimated": None,
        "tuition_items": [
            {"name": "international flat tuition", "amount_eur": 1000, "period": "academic_year", "mandatory": True, "applicant_scope": "international"},
            {"name": "regional right-to-study tax", "amount_eur": None, "published_approximation_eur": 190, "period": "academic_year", "mandatory": True},
            {"name": "virtual stamp duty", "amount_eur": 16, "period": "first_instalment", "mandatory": True},
            {"name": "programme application fee", "amount_eur": 23, "period": "application", "mandatory": True},
        ],
        "payment_deadlines": {"first": "by the restricted-admission call/enrolment deadline", "second": "end of March", "third": "end of June"},
        "source_notes": bi(
            "The verified annual tuition is EUR 1,000. The university labels the regional charge as approximately EUR 190, so an exact annual total is not calculated.",
            "Doğrulanmış yıllık öğrenim ücreti 1.000 EUR'dur. Üniversite bölgesel harcı yaklaşık 190 EUR olarak verdiği için kesin yıllık toplam hesaplanmaz.",
        ),
        "verification_notes": bi(
            "The flat-tax rule is published for international students and does not require ISEE Parificato.",
            "Sabit vergi kuralı uluslararası öğrenciler için yayımlanmıştır ve ISEE Parificato gerektirmez.",
        ),
    }
    row["tuition_eur_per_year"] = 1000
    row["annual_fee_eur"] = 1000

    row["scholarship_profile"] = {
        "regional_scholarship_available": True,
        "regional_scholarship_name": "ADISU Puglia Benefits and Services 2026/27",
        "dsu_or_equivalent": "ADISU Puglia",
        "non_eu_eligible": True,
        "application_mode": "separate",
        "automatic_consideration": False,
        "separate_application_required": True,
        "scholarship_deadline": "2026-08-13T12:00:00+02:00",
        "available_types": ["ADISU Puglia", "ISUFI second-level admission"],
        "opportunities": [
            {
                "name": "ADISU Puglia Benefits and Services 2026/27",
                "application_mode": "separate",
                "deadline": "2026-08-13T12:00:00+02:00",
                "status_as_of_last_checked": "closed",
                "non_eu_eligible": True,
                "income_thresholds": {"isee_eur_max": 26000, "ispe_eur_max": 56000},
                "amounts_eur": {"off_site": 7172, "commuter": 4191, "on_site": 2891},
                "benefits": ["cash scholarship", "competitive accommodation/services", "meals"],
                "foreign_document_rule": bi("Foreign family income and asset documents require translation and legalisation/apostille under the call.", "Yabancı aile gelir ve mal varlığı belgeleri çağrı uyarınca çeviri ve tasdik/apostil gerektirir."),
            },
            {
                "name": "ISUFI second-level student admission 2026/27",
                "application_mode": "separate",
                "deadline": "2026-08-25T13:00:00+02:00",
                "status_as_of_last_checked": "open",
                "places_total_second_level": 6,
                "places_technical_scientific": 2,
                "non_eu_eligible": True,
                "minimum_record": {"weighted_average": "27/30", "minimum_single_exam": "24/30"},
                "selection_language": "Italian",
                "selection": {"written_test_date": "2026-09-07", "interview_date": "2026-09-21", "total_minimum": "70/100"},
                "benefits": ["tuition exemption", "free ISUFI College housing in Lecce when continuous use is requested", "annual teaching contribution of unpublished amount", "additional ISUFI courses"],
                "obligations": ["basic Italian", "60 extra teaching hours per year", "one study term abroad", "annual merit requirements"],
                "campus_mismatch_warning": bi("The verified free residence is in Lecce, not at the Brindisi programme location.", "Doğrulanan ücretsiz yurt Lecce'dedir; Brindisi program yerinde değildir."),
            },
        ],
        "merit_scholarships": ["ISUFI second-level student admission 2026/27"],
        "tuition_waivers": ["ISUFI winners: tuition exemption subject to the current call and continuing requirements"],
        "external_options": [],
        "funding_notes": bi(
            "ADISU and ISUFI are separate competitive applications. Invest Your Talent in Italy and UniSalento4Talents are named on the current university overview, but no 2026/27 Aerospace-specific eligibility or award is retained without a checked cycle-specific call.",
            "ADISU ve ISUFI ayrı ve rekabetçi başvurulardır. Güncel üniversite genel sayfası Invest Your Talent in Italy ile UniSalento4Talents'ı adlandırır; ancak 2026/27 Aerospace'e özgü uygunluk veya ödül, döneme özgü doğrulanmış çağrı olmadan tutulmaz.",
        ),
        "verification_notes": bi(
            "Funding is not automatic with programme admission. The ADISU deadline has passed; ISUFI remained open on the verification date but is highly selective and assessed in Italian.",
            "Program kabulüyle burs otomatik verilmez. ADISU son tarihi geçmiştir; ISUFI doğrulama tarihinde açık olmakla birlikte çok seçicidir ve İtalyanca değerlendirilir.",
        ),
    }

    row["living_profile"] = {
        "city_type": "medium",
        "housing_access": "not_guaranteed",
        "housing_application_separate": True,
        "student_dorm_availability": "no_current_operational_ADISU_Brindisi_residence_verified",
        "housing_search_difficulty": "high",
        "housing_difficulty": "high",
        "living_cost_risk": "high",
        "living_risk": "high",
        "average_room_rent_eur": None,
        "average_room_rent_eur_min": None,
        "average_room_rent_eur_max": None,
        "monthly_living_cost_eur_estimated": None,
        "monthly_living_cost_eur_min": None,
        "monthly_living_cost_eur_max": None,
        "housing_options": [
            {
                "name": "ADISU off-site lease-document route",
                "location": "campuses without an ADISU or contracted residence",
                "guaranteed": False,
                "notes": bi("Eligible students at an unserved campus can document a private lease under the published ADISU route; this is not a room offer.", "Yurtsuz kampüsteki uygun öğrenciler yayımlanmış ADISU yolu kapsamında özel kira sözleşmesini belgeleyebilir; bu bir oda teklifi değildir."),
            },
            {
                "name": "ISUFI College",
                "location": "Lecce",
                "guaranteed": False,
                "eligibility": "only successful ISUFI candidates who request continuous use",
            },
        ],
        "official_living_cost_items": [],
        "official_rent_items": [],
        "housing_notes": bi(
            "The current ADISU operational-residence register does not list Brindisi. An official ADISU notice describes Brindisi as a city without a residence; development projects are not treated as operational housing.",
            "Güncel ADISU faal yurt sicilinde Brindisi yer almaz. Resmî ADISU duyurusu Brindisi'yi yurdu olmayan şehir olarak tanımlar; geliştirme projeleri faal konut sayılmaz.",
        ),
        "verification_notes": bi(
            "No current official Brindisi private-room or total living-cost range was found. Legacy EUR 150–400 rent and EUR 600 monthly-cost claims were removed as unsupported.",
            "Güncel resmî Brindisi özel oda veya toplam yaşam maliyeti aralığı bulunamadı. Eski 150–400 EUR kira ve aylık 600 EUR yaşam maliyeti iddiaları kaynaksız olduğu için kaldırıldı.",
        ),
    }

    row["curriculum_profile"] = {
        "structure": "120 ECTS over 2 years",
        "tracks": ["Aerospace Design", "Aeronautics Design"],
        "current_high_level_domains": ["fluid dynamics", "propulsion", "aerospace structures", "on-board systems"],
        "teaching_locations_published_by_current_partner_page": {"Aerospace Design": "Lecce", "Aeronautics Design": "Taranto"},
        "admission_location_published_by_unisalento_2026_27": "Brindisi",
        "location_reconciliation_status": "needs_current_study_plan_confirmation_due_to_programme_reform",
        "exact_course_count": None,
        "mandatory_internship": None,
        "thesis_type": "unknown_for_current_reformed_plan",
        "flexibility": "unknown_for_current_reformed_plan",
        "historical_curriculum_snapshot": {
            "academic_year": "2024/2025",
            "use_as_current_guarantee": False,
            "historical_tracks": ["Aeronautics Design", "Space Technology"],
            "space_topics_observed": ["atmospheric and space flight dynamics", "space propulsion", "spacecraft architecture and systems engineering", "satellite communications", "space payload/on-board electronics"],
        },
        "delivery_continuity_evidence": ["Aerospace Structures", "Aircraft Design", "Atmospheric and Space Flight Dynamics", "Flight Mechanics", "Fluid Dynamics", "Gas Dynamics", "Propulsion Systems — New Concepts"],
        "curriculum_risk": "medium",
        "verification_notes": bi(
            "Current official sources verify the two-year English Aerospace degree and its core domains, but the exact 2026/27 reformed study plan/course count is not published in the checked sources. The older Space Technology list is retained only as a dated historical snapshot.",
            "Güncel resmî kaynaklar iki yıllık İngilizce Aerospace derecesini ve çekirdek alanlarını doğrular; ancak kontrol edilen kaynaklarda reform sonrası 2026/27 kesin çalışma planı/ders sayısı yayımlanmamıştır. Eski Space Technology listesi yalnızca tarihli geçmiş görünümü olarak tutulur.",
        ),
    }

    row["category_profile"] = {
        "primary_categories": ["aerospace_engineering"],
        "secondary_categories": ["space_systems", "propulsion", "structures", "fluid_dynamics", "onboard_systems"],
        "technical_focus": bi("Direct aerospace degree with aeronautical and space-relevant content.", "Havacılık ve uzayla ilgili içerik taşıyan doğrudan havacılık-uzay derecesi."),
        "normalized_tags": ["Aerodynamics", "Propulsion", "Aerospace Structures", "Flight Dynamics", "Space Systems", "On-board Systems"],
        "verification_notes": bi("Categories are based on checked curriculum/domain evidence, not on institutional prestige.", "Kategoriler kurumsal prestije değil, doğrulanmış müfredat/alan kanıtına dayanır."),
    }

    row["research_profile"] = {
        "research_strength": "medium_high",
        "research_areas": ["aerospace structures", "structural health monitoring", "advanced composites", "fluid dynamics and hypersonic interactions", "aerospace propulsion and microthrusters", "advanced air mobility"],
        "labs_and_groups": [
            {
                "name": "AeroSpace Structures Engineering Lab (ASSE)",
                "location": "Campus Ecotekne, Lecce",
                "verified_capabilities": ["structural health monitoring", "advanced composite materials", "hardware vibration/acoustic instrumentation", "Matlab-based analysis"],
                "student_access_guaranteed": False,
            }
        ],
        "current_activity_examples": ["TWEETERS hypersonic shock-wave/boundary-layer interaction research", "AIRMOB advanced air mobility skills project"],
        "space_research_fit": "medium",
        "verification_notes": bi(
            "Current official pages prove relevant groups and projects, not guaranteed Master's-student placement, thesis supervision or equipment access.",
            "Güncel resmî sayfalar ilgili grup ve projeleri kanıtlar; yüksek lisans öğrencisine yer, tez danışmanlığı veya ekipman erişimi garantisi vermez.",
        ),
    }

    row["industry_ecosystem_profile"] = {
        "ecosystem_strength": "high",
        "verified_links": ["DTA — Distretto Tecnologico Aerospaziale Pugliese", "Leonardo Aerostructures", "Leonardo Helicopters", "AVIO", "Airbus", "CETMA", "ENEA Brindisi"],
        "partnership_scope": "ASSE laboratory partners and collaborations",
        "internship_guaranteed": False,
        "employment_guaranteed": False,
        "verification_notes": bi(
            "The ASSE page lists these partners/collaborations. This is ecosystem evidence only and must not be read as a guaranteed programme internship or individual hiring path.",
            "ASSE sayfası bu ortak/iş birliklerini listeler. Bu yalnızca ekosistem kanıtıdır; garantili program stajı veya bireysel işe alım yolu olarak okunmamalıdır.",
        ),
    }

    row["application_timeline_profile"] = {
        "academic_year": "2026/2027",
        "application_deadline": "2026-06-12",
        "non_eu_deadline": "2026-06-12",
        "pre_enrolment_deadline": "2026-07-20",
        "visa_sensitive_deadline": "2026-11-30",
        "timeline_risk": "high",
        "deadline_events": [
            {"event": "aerospace_second_extraordinary_non_eu_call", "date": "2026-06-12", "status": "closed", "applicant_scope": "foreign_non_eu"},
            {"event": "mandatory_online_interview", "date": "2026-06-30T11:30:00+02:00", "status": "closed", "applicant_scope": "foreign_non_eu"},
            {"event": "universitaly_pre_enrolment", "date": "2026-07-20", "status": "closed", "applicant_scope": "non_eu_visa_applicants"},
            {"event": "adisu_scholarship_and_services", "date": "2026-08-13T12:00:00+02:00", "status": "closed", "applicant_scope": "eligible_students"},
            {"event": "isufi_second_level_selection", "date": "2026-08-25T13:00:00+02:00", "status": "open_as_of_last_checked", "applicant_scope": "eligible_first_time_second_level_students"},
            {"event": "study_visa_application", "date": "2026-11-30", "status": "future_general_university_deadline", "applicant_scope": "non_eu_visa_applicants"},
            {"event": "final_enrolment", "date": "2027-01-31", "status": "future_general_university_deadline", "applicant_scope": "non_eu_visa_applicants"},
        ],
        "deadline_notes": bi(
            "The programme-specific 2026/27 application route is closed. The university says English-taught early calls normally begin from February, but no future-cycle day is estimated until published.",
            "Programa özgü 2026/27 başvuru yolu kapanmıştır. Üniversite İngilizce erken çağrıların normalde Şubat'tan itibaren başladığını söyler; yayımlanana kadar gelecek dönem için gün tahmini yapılmaz.",
        ),
        "verification_notes": bi(
            "The July and November dates are current central visa-process deadlines; the June dates are Aerospace-specific.",
            "Temmuz ve Kasım tarihleri güncel merkezi vize süreci son tarihleridir; Haziran tarihleri Aerospace'e özgüdür.",
        ),
    }

    row["student_sentiment_profile"] = {
        "student_satisfaction_score": None,
        "workload_sentiment": "unknown",
        "teaching_quality_sentiment": "unknown",
        "administration_sentiment": "unknown",
        "housing_sentiment": "unknown",
        "city_life_sentiment": "unknown",
        "international_student_sentiment": "unknown",
        "career_support_sentiment": "unknown",
        "student_sentiment_summary": bi("Insufficient programme-specific independent evidence; no sentiment score is assigned.", "Programa özgü bağımsız kanıt yetersizdir; duygu/memnuniyet puanı verilmez."),
        "student_sentiment_sources": [],
        "sample_size_estimate": None,
        "date_range": None,
        "sentiment_confidence": "unknown",
    }

    row["source_profile"] = {
        "last_verified": CHECKED,
        "field_confidence": {
            "program": "high", "program_basic_info": "high", "language": "high", "admission": "high", "eligibility": "high", "non_eu_eligibility": "high",
            "tuition": "high", "scholarship": "high", "deadline": "high", "deadlines": "high", "curriculum": "high", "housing": "high", "living": "high",
            "research": "high", "industry": "medium", "student_sentiment": "unknown",
        },
        "source_log": [
            source(MASTER, "UniSalento Master's degree admission, fees and programme catalogue", "official_admission_page", ["program", "language", "admission", "non_eu_eligibility", "tuition", "deadline"], "Current central page verifies the programme, international route, documents, fees and visa timeline.", "Güncel merkezi sayfa programı, uluslararası yolu, belgeleri, ücretleri ve vize takvimini doğrular."),
            source(ENGLISH_DEGREES, "UniSalento degree programmes taught in English", "official_program_page", ["program", "language", "curriculum"], "Current catalogue verifies the two-year, 120-credit English Aerospace degree in Brindisi.", "Güncel katalog Brindisi'deki iki yıllık, 120 kredilik İngilizce Aerospace derecesini doğrular."),
            source(CALL_PDF, "DII second international engineering call 2026/27", "official_admission_page", ["program", "admission", "non_eu_eligibility", "language", "deadline"], "Programme-specific call verifies 30 places, 70%, B2/MOI, fee, documents and mandatory interview.", "Programa özgü çağrı 30 kontenjanı, %70'i, B2/eğitim dili yazısını, ücreti, belgeleri ve zorunlu mülakatı doğrular.", access_status="pdf"),
            source(CALL_INDEX, "UniSalento 2026/27 international admission notices", "official_admission_page", ["admission", "deadline"], "Current notice index corroborates the call deadline, interview and application fee.", "Güncel duyuru dizini çağrı son tarihini, mülakatı ve başvuru ücretini doğrular."),
            source(PRE_ENROLMENT, "UniSalento pre-enrolment and visa guidance", "official_visa_or_government_page", ["non_eu_eligibility", "admission", "deadline"], "Official guidance separates academic eligibility, Universitaly and visa decisions.", "Resmî rehber akademik uygunluk, Universitaly ve vize kararlarını ayırır."),
            source(POLIBA_PROGRAM, "PoliBa Aerospace Engineering MSc", "official_program_page", ["program", "language", "curriculum"], "Current partner page verifies the joint degree, English delivery, tracks and core technical domains.", "Güncel ortak sayfası ortak dereceyi, İngilizce eğitimi, müfredatları ve çekirdek teknik alanları doğrular."),
            source(JOINT_GOVERNANCE, "PoliBa-UniSalento engineering agreement", "official_university_policy_page", ["program", "admission"], "Official university report identifies UniSalento as the administrative seat and the award as joint.", "Resmî üniversite haberi UniSalento'yu idari merkez, diplomayı ortak olarak tanımlar."),
            source(HISTORICAL_PROGRAM, "UniSalento Aerospace Engineering historical course page", "official_curriculum_page", ["curriculum"], "Older course plan is retained only as a dated historical snapshot, not a current guarantee.", "Eski ders planı güncel garanti olarak değil, yalnızca tarihli geçmiş görünümü olarak tutulur.", confidence="medium"),
            source(ELEARNING, "UniSalento Aerospace Engineering e-learning catalogue", "official_curriculum_page", ["curriculum"], "Current and recent delivery examples corroborate aerospace teaching continuity but not a complete 2026/27 plan.", "Güncel ve yakın dönem ders örnekleri aerospace eğitiminin sürekliliğini doğrular; tam 2026/27 planını kanıtlamaz.", confidence="medium"),
            source(ADISU_UNISALENTO, "UniSalento ADISU scholarships", "official_scholarship_page", ["scholarship", "housing"], "Current page verifies international eligibility, separate application, documents, accommodation and meal services.", "Güncel sayfa uluslararası uygunluğu, ayrı başvuruyu, belgeleri, konut ve yemek hizmetlerini doğrular."),
            source(ADISU_AMOUNTS, "Puglia Region ADISU 2026/27 policy", "official_scholarship_page", ["scholarship"], "Official regional source publishes current amounts and financial thresholds.", "Resmî bölgesel kaynak güncel tutarları ve mali eşikleri yayımlar."),
            source(ADISU_DEADLINE, "ADISU Puglia 2026/27 benefit call", "official_scholarship_page", ["scholarship", "deadline"], "Official ADISU page verifies the current deadline.", "Resmî ADISU sayfası güncel son tarihi doğrular."),
            source(ISUFI, "ISUFI second-level selection 2026/27", "official_scholarship_page", ["scholarship", "deadline", "housing"], "Current official call index verifies places, dates and separate competitive selection.", "Güncel resmî çağrı dizini kontenjanları, tarihleri ve ayrı rekabetçi seçimi doğrular."),
            source(ISUFI_PDF, "ISUFI 2026/27 selection call", "official_scholarship_page", ["scholarship", "deadline", "housing"], "Call verifies eligibility, Italian tests, thresholds, benefits and continuing obligations.", "Çağrı uygunluğu, İtalyanca sınavları, eşikleri, yardımları ve devam koşullarını doğrular.", access_status="pdf"),
            source(ADISU_RESIDENCES, "ADISU Puglia operational property register", "official_housing_page", ["housing", "living"], "Current official register lists operational residences and does not list Brindisi.", "Güncel resmî sicil faal yurtları listeler ve Brindisi'yi içermez."),
            source(ADISU_NO_RESIDENCE, "ADISU Puglia residence development notice", "official_housing_page", ["housing"], "Official notice describes Brindisi as a city without a residence; future projects are not counted as available beds.", "Resmî duyuru Brindisi'yi yurdu olmayan şehir olarak tanımlar; gelecek projeler mevcut yatak sayılmaz."),
            source(ADISU_LEASE_ROUTE, "ADISU lease-document route for unserved campuses", "official_housing_page", ["housing"], "Official page verifies the private-lease documentation route for campuses without residences.", "Resmî sayfa yurdu olmayan kampüsler için özel kira sözleşmesi belgeleme yolunu doğrular."),
            source(ASSE, "AeroSpace Structures Engineering Lab", "official_lab_page", ["research", "industry", "curriculum"], "Official lab page verifies research lines, equipment, teaching and listed collaborations.", "Resmî laboratuvar sayfası araştırma alanlarını, ekipmanı, eğitimi ve listelenen iş birliklerini doğrular."),
            source(AIRMOB, "AIRMOB advanced air mobility project", "official_department_page", ["research", "industry"], "Current official project evidence supports advanced-air-mobility activity, not guaranteed student access.", "Güncel resmî proje kanıtı ileri hava hareketliliği faaliyetini destekler; öğrenci erişimini garanti etmez."),
            source(ACTIVE_RESEARCH, "UniSalento active research calls", "official_department_page", ["research"], "Current official listing corroborates active hypersonic-fluid-dynamics research.", "Güncel resmî liste aktif hipersonik akışkanlar dinamiği araştırmasını doğrular."),
        ],
    }

    row["decision_summary"] = {
        "main_strengths": [
            bi("Direct English Aerospace Engineering degree with aeronautical and space-relevant coverage", "Havacılık ve uzayla ilgili kapsam taşıyan doğrudan İngilizce Aerospace Engineering derecesi"),
            bi("Low verified EUR 1,000 international flat tuition", "Doğrulanmış düşük, yıllık 1.000 EUR uluslararası sabit öğrenim ücreti"),
            bi("Strong regional aerospace-structures and industrial ecosystem evidence", "Güçlü bölgesel havacılık yapıları ve sanayi ekosistemi kanıtı"),
            bi("Substantial separate ADISU and highly selective ISUFI funding routes", "Kayda değer ayrı ADISU ve çok seçici ISUFI destek yolları"),
        ],
        "main_risks": [
            bi("The 2026/27 non-EU Aerospace application and Universitaly deadlines have passed", "2026/27 AB-dışı Aerospace başvuru ve Universitaly son tarihleri geçmiştir"),
            bi("Mandatory interview plus a real 70% and B2/MOI screening floor", "Zorunlu mülakat ile gerçek %70 ve B2/eğitim dili yazısı eleme tabanı"),
            bi("Exact current course count and post-reform campus allocation remain unpublished/unclear", "Reform sonrası kesin güncel ders sayısı ve kampüs dağılımı yayımlanmamış/belirsizdir"),
            bi("No operational Brindisi ADISU residence or official private-rent range is verified", "Brindisi'de faal ADISU yurdu veya resmî özel kira aralığı doğrulanmamıştır"),
        ],
        "application_reality": bi(
            "A future Turkey-resident applicant should prepare B2/MOI, a transcript clearly showing the final cumulative percentage, translations and a visa-ready document set before early international calls begin. Programme admission, ADISU and ISUFI are three separate procedures.",
            "Gelecek dönemde Türkiye'de ikamet eden aday erken uluslararası çağrılar başlamadan B2/eğitim dili yazısını, nihai yüzdelik ortalamayı açık gösteren transkripti, çevirileri ve vizeye hazır belge setini hazırlamalıdır. Program kabulü, ADISU ve ISUFI üç ayrı süreçtir.",
        ),
        "overall_recommendation": bi(
            "A strong value-for-money direct aerospace option for an applicant who can tolerate deadline, interview and housing risk; not a viable new 2026/27 application as of the verification date.",
            "Son tarih, mülakat ve konut riskini kaldırabilecek aday için fiyat/teknik uyum açısından güçlü doğrudan havacılık-uzay seçeneği; doğrulama tarihi itibarıyla yeni 2026/27 başvurusu mümkün değildir.",
        ),
        "recommended_user_profile": bi(
            "Engineering graduate above the 70% floor with B2 English, strong aerospace fundamentals, early visa preparation and a private-housing fallback budget.",
            "%70 tabanının üzerinde, B2 İngilizceye ve güçlü havacılık-uzay temeline sahip; vizeye erken hazırlanan ve özel konut için yedek bütçesi bulunan mühendislik mezunu.",
        ),
    }

    row["scoring_inputs"] = {
        "academic_field_fit_score_seed": None,
        "eligibility_language_score_seed": None,
        "cost_funding_score_seed": None,
        "career_research_score_seed": None,
        "living_risk_score_seed": None,
        "data_confidence_score_seed": None,
        "hard_filter_flags": {
            "english_only_compatible": True,
            "requires_italian": False,
            "non_eu_eligible": True,
            "tuition_above_5000": False,
            "tuition_above_10000": False,
            "deadline_unclear": False,
            "deadline_closed_for_new_applicants": True,
            "housing_guaranteed": False,
            "needs_verification": False,
        },
    }
    finish(row)


def update_poliba_partner(row: dict) -> None:
    row["joint_program_id"] = JOINT_ID
    row["catalogue_relationship"] = {
        "role": "teaching_partner_manifestation",
        "canonical_record_id": "universita-del-salento",
        "rankable_as_independent_choice": False,
        "joint_degree": True,
        "degree_awarding_institutions": ["Università del Salento", "Politecnico di Bari"],
        "administrative_seat": "Università del Salento",
        "verification_notes": bi(
            "This is not a second independent degree choice. It is PoliBa's teaching-partner presentation of the same joint Aerospace Engineering MSc whose administrative seat and canonical application record are at UniSalento.",
            "Bu ikinci bir bağımsız derece seçeneği değildir. İdari merkezi ve kanonik başvuru kaydı UniSalento'da olan aynı ortak Aerospace Engineering yüksek lisansının PoliBa eğitim ortağı görünümüdür.",
        ),
    }
    row.setdefault("scoring_inputs", {}).setdefault("hard_filter_flags", {})["not_independent_catalogue_choice"] = True
    row.setdefault("source_profile", {}).setdefault("source_log", []).append(
        source(JOINT_GOVERNANCE, "PoliBa-UniSalento engineering agreement", "official_university_policy_page", ["program", "admission"], "Official governance evidence identifies UniSalento as the administrative seat and the award as joint.", "Resmî yönetişim kanıtı UniSalento'yu idari merkez, diplomayı ortak olarak tanımlar.")
    )
    row["source_profile"]["last_verified"] = CHECKED


def main() -> None:
    payload = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    rows = {row.get("id"): row for row in payload["universities"]}
    update_unisalento(rows["universita-del-salento"])
    update_poliba_partner(rows["poliba_aerospace_master"])
    payload["last_updated"] = CHECKED
    DATA_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(rows["universita-del-salento"]["data_quality"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
