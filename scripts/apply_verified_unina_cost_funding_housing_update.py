"""Apply current official decision evidence to Federico II Aerospace Engineering MSc."""

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

PROGRAM = "https://www.corsi.unina.it/DF5"
INTERNATIONAL_ADMISSION = "https://www.international.unina.it/education/admission-regulation/"
ENROLMENT = "https://www.unina.it/en/w/immatricolarsi-alla-federico-ii-copia-1-"
FEE_GUIDE = "https://www.unina.it/documents/20117/4260320/Guida_Studente_rapidA_26-27_10.7.2026.pdf/e1b8b1ea-888f-bea9-07cb-2b0a447930cb?t=1783671923211&version=1.0"
ADISURC_LANDING = "https://adisurcampania.it/notizie/approvazione-bando-di-concorso-20262027"
ADISURC_CALL = "https://adisurcampania.it/sites/default/files/2026-07/Bando%20di%20Concorso%20a.a.%202026.27_ENG.pdf"
IWD_COSTS = "https://www.international.unina.it/wp-content/uploads/2026/03/7.-IWD_compressed.pdf"


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
            "Current official 2026/27 source checked for the listed fields.",
            "Listelenen alanlar için güncel resmî 2026/27 kaynak kontrol edildi.",
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
        remaining = [
            bi(
                f"Resolve remaining critical evidence gaps: {', '.join(quality['unverified_critical_fields'])}.",
                f"Kalan kritik kanıt boşluklarını giderin: {', '.join(quality['unverified_critical_fields'])}.",
            )
        ]
        failure = "missing_or_unverified_critical_fields"
    elif not complete:
        remaining = [
            bi(
                "Refresh the medium-confidence 2025/26 Naples cost examples when a newer university budget is published.",
                "Daha yeni üniversite bütçesi yayımlandığında orta güvenli 2025/26 Napoli maliyet örneklerini güncelleyin.",
            )
        ]
        failure = "critical_field_confidence_below_high"
    else:
        remaining = []
        failure = None
    row["quality_control"] = {
        "qc_status": "passed" if complete else "needs_revision",
        "checked_at": CHECKED,
        "failed_canary_tests": [] if complete else [failure],
        "remaining_verification_tasks": remaining,
        "qc_notes": bi(
            "All critical decision fields have checked official evidence; the older housing-price examples remain explicitly date-qualified.",
            "Tüm kritik karar alanlarında kontrol edilmiş resmî kanıt vardır; eski konut fiyatı örnekleri tarih bağlamıyla açıkça sınırlandırılmıştır.",
        ),
    }
    profile["needs_verification"] = not complete


def update_record(row: dict) -> None:
    row["teaching_language"] = ["Italian", "English"]

    row["eligibility_profile"].update(
        {
            "eligible_for_non_eu": True,
            "required_previous_degree": bi(
                "A Bachelor's degree or equivalent foreign qualification; programme curricular requirements and personal preparation are checked before admission.",
                "Lisans diploması veya eşdeğer yabancı yeterlilik; kabulden önce programa özgü müfredat koşulları ve kişisel hazırlık denetlenir.",
            ),
            "admission_mode": bi(
                "Open-admission master's degree subject to programme-level curricular and preparation checks; overseas non-EU applicants must also complete Universitaly pre-enrolment.",
                "Programa özgü müfredat ve hazırlık denetimine tabi açık kontenjanlı yüksek lisans; yurt dışındaki non-EU aday ayrıca Universitaly ön kaydını tamamlamalıdır.",
            ),
            "admission_risk": "high",
            "required_documents": [
                bi("Passport", "Pasaport"),
                bi("Bachelor's diploma or equivalent qualification", "Lisans diploması veya eşdeğer yeterlilik"),
                bi("Transcript/exam certificate", "Transkript/sınav dökümü"),
                bi("Official translations and legalisation where required", "Gerektiğinde resmî çeviri ve tasdik"),
                bi("Declaration of Value or a CIMEA/ENIC-NARIC comparability-validity document for enrolment", "Kayıt için Değer Beyanı veya CIMEA/ENIC-NARIC karşılaştırılabilirlik-geçerlilik belgesi"),
                bi("Italian B2 evidence or the university's language test for an Italian-taught degree", "İtalyanca yürütülen derece için İtalyanca B2 kanıtı veya üniversitenin dil sınavı"),
                bi("Tax code and residence-permit application receipt at enrolment", "Kayıtta vergi kodu ve oturum izni başvuru makbuzu"),
            ],
            "test_required": False,
            "gre": {
                "policy": "not_listed_as_required_in_checked_official_sources",
                "test_type": None,
                "minimum_scores": {},
                "recommended_scores": {},
                "validity_rule": None,
                "waiver_rules": [],
                "source_ids": [INTERNATIONAL_ADMISSION, PROGRAM],
            },
            "notes_for_turkish_students": bi(
                "A Turkey-resident applicant follows the overseas non-EU visa route. Universitaly pre-enrolment is mandatory but is not admission or enrolment, and Federico II states that it does not issue a separate admission letter for the visa process.",
                "Türkiye'de ikamet eden aday, yurt dışındaki non-EU vize yolunu izler. Universitaly ön kaydı zorunludur ancak kabul veya üniversite kaydı değildir; Federico II vize süreci için ayrıca kabul mektubu düzenlemediğini belirtir.",
            ),
            "verification_notes": bi(
                "The international route and document set are current. Exact programme-level curricular matching remains an academic committee decision and must not be converted into a guaranteed admission rule.",
                "Uluslararası yol ve belge seti günceldir. Programa özgü müfredat eşleşmesi akademik kurul kararıdır ve garantili kabul kuralına dönüştürülmemelidir.",
            ),
        }
    )

    row["language_profile"].update(
        {
            "teaching_language": ["Italian", "English"],
            "primary_teaching_language": "Italian",
            "italian_required": True,
            "italian_level_required": "B2 for overseas non-EU admission to this Italian-taught degree",
            "italian_evidence_modes": ["recognised B2 certificate", "Federico II language test"],
            "english_required": False,
            "english_required_at_entry": False,
            "english_level_required": None,
            "mixed_language_warning": bi(
                "The current catalogue lists Italian and English, but the degree is classified as Italian-taught. Some modules may be delivered in English; this does not replace the B2 Italian rule for an overseas non-EU applicant.",
                "Güncel katalog İtalyanca ve İngilizceyi listeler; ancak derece İtalyanca yürütülen program olarak sınıflandırılır. Bazı dersler İngilizce olabilir; bu durum yurt dışındaki non-EU aday için İtalyanca B2 kuralının yerini almaz.",
            ),
            "language_risk": "high",
            "verification_notes": bi(
                "Do not infer a fully English route from the bilingual catalogue label. No IELTS, TOEFL or other English-score threshold is listed as an entry condition in the checked official sources.",
                "İki dilli katalog etiketinden tamamen İngilizce bir yol çıkarılmamalıdır. Kontrol edilen resmî kaynaklarda giriş koşulu olarak IELTS, TOEFL veya başka İngilizce puan eşiği listelenmez.",
            ),
        }
    )

    row["cost_profile"].update(
        {
            "academic_year": "2026/2027",
            "tuition_eur_per_year_min": 0,
            "tuition_eur_per_year_max": 0,
            "tuition_eur_per_year_estimated": 0,
            "student_contribution_eur": 0,
            "tuition_basis": "non_eu_students_fully_exempt_from_university_contribution_current_2026_27_guide",
            "regional_tax_eur": None,
            "regional_tax_eur_min": 151,
            "regional_tax_eur_max": 173,
            "stamp_duty_eur": 16,
            "mandatory_fees_eur_per_year_min": 167,
            "mandatory_fees_eur_per_year_max": 189,
            "total_academic_cost_eur_per_year_estimated": None,
            "living_cost_eur_per_month": None,
            "tuition_items": [
                {
                    "name": "University contribution for non-EU citizens",
                    "amount_eur": 0,
                    "academic_year": "2026/2027",
                    "source_url": FEE_GUIDE,
                },
                {
                    "name": "Campania regional right-to-study tax for a family resident abroad",
                    "amount_eur": 151,
                    "condition": "Equivalent ISEE submitted; the guide assigns this band to students whose family resides abroad",
                    "source_url": FEE_GUIDE,
                },
                {
                    "name": "Campania regional right-to-study tax without an Equivalent ISEE",
                    "amount_eur": 173,
                    "condition": "No ISEEU/Equivalent ISEE",
                    "source_url": FEE_GUIDE,
                },
                {"name": "Stamp duty", "amount_eur": 16, "source_url": FEE_GUIDE},
            ],
            "source_notes": bi(
                "For planning, a student with family abroad pays EUR 167 with the relevant Equivalent ISEE band or EUR 189 without it. The exact total depends on the filed financial document. An older international page still mentions EUR 140 regional tax; the dated 2026/27 fee guide supersedes it.",
                "Planlama için ailesi yurt dışında olan öğrenci ilgili eşdeğer ISEE bandıyla 167 EUR, belge olmadan 189 EUR öder. Kesin toplam sunulan mali belgeye bağlıdır. Eski uluslararası sayfada hâlâ 140 EUR bölgesel vergi geçer; tarihli 2026/27 ücret rehberi bu bilgiyi geçersiz kılar.",
            ),
            "verification_notes": bi(
                "Tuition contribution is zero, but mandatory regional tax and stamp duty remain payable. No single exact total is asserted without the applicant's Equivalent ISEE status.",
                "Öğrenim katkısı sıfırdır; ancak zorunlu bölgesel vergi ve damga vergisi ödenir. Adayın eşdeğer ISEE durumu bilinmeden tek bir kesin toplam ileri sürülmez.",
            ),
        }
    )

    row["scholarship_profile"].update(
        {
            "available_types": ["ADISURC 2026/27 scholarship", "ADISURC accommodation", "ADISURC meal service"],
            "regional_scholarship_available": True,
            "regional_scholarship_name": "ADISURC Campania 2026/27 scholarship and services competition",
            "non_eu_eligible": True,
            "application_mode": "separate",
            "automatic_consideration": False,
            "separate_application_required": True,
            "scholarship_deadline": "2026-09-10T12:00:00+02:00",
            "equivalent_isee_deadline": "2027-03-31",
            "application_before_university_enrolment_allowed": True,
            "opportunities": [
                {
                    "name": "ADISURC scholarship — non-resident basic amount",
                    "amount_eur": 7171.11,
                    "condition": "Full basic amount at ISEE up to EUR 17,000; amount decreases with ISEE and requires non-resident status evidence",
                    "includes": ["cash award", "one free daily meal"],
                    "source_url": ADISURC_CALL,
                },
                {
                    "name": "ADISURC scholarship — commuter basic amount",
                    "amount_eur": 4190.71,
                    "condition": "Full basic amount at ISEE up to EUR 17,000; amount decreases with ISEE",
                    "source_url": ADISURC_CALL,
                },
                {
                    "name": "ADISURC scholarship — resident basic amount",
                    "amount_eur": 2890.16,
                    "condition": "Full basic amount at ISEE up to EUR 17,000; includes one free daily meal and is linked to residence-service status",
                    "source_url": ADISURC_CALL,
                },
            ],
            "award_adjustments": [
                "15% increase at ISEE up to EUR 12,750",
                "20% increase for women in STEM programmes",
                "40% increase for students with disabilities",
                "increases are not cumulative; the highest applicable increase is used",
            ],
            "funding_notes": bi(
                "This is a competitive benefits application, not an automatic university scholarship. A foreign household normally needs an Equivalent University ISEE/ISEEUP and supporting foreign income/assets documents translated into Italian; payment is suspended until the required financial evidence is received.",
                "Bu, otomatik üniversite bursu değil rekabetçi bir yardım başvurusudur. Yabancı hane genellikle Eşdeğer Üniversite ISEE/ISEEUP ile İtalyancaya çevrilmiş yabancı gelir/varlık belgeleri sunmalıdır; gerekli mali kanıt gelene kadar ödeme askıda kalır.",
            ),
            "verification_notes": bi(
                "Foreign nationals apply online with ADISURC-issued credentials and may apply before university enrolment. Eligibility never guarantees an award or a residence place when resources are insufficient.",
                "Yabancı uyruklular ADISURC'nin verdiği bilgilerle çevrim içi başvurur ve üniversite kaydından önce başvurabilir. Uygunluk, kaynaklar yetersizse bursu veya yurt yerini garanti etmez.",
            ),
        }
    )

    row["living_profile"].update(
        {
            "housing_search_difficulty": "high",
            "housing_difficulty": "high_competition_no_guarantee",
            "housing_access": "not_guaranteed",
            "housing_application_separate": True,
            "student_dorm_availability": "ADISURC competitive residence service",
            "living_risk": "high",
            "housing_cost_range_eur": {"min": None, "max": None},
            "average_room_rent_eur": None,
            "average_room_rent_eur_min": 250,
            "average_room_rent_eur_max": 500,
            "monthly_living_cost_eur_estimated": None,
            "monthly_living_cost_eur_min": None,
            "monthly_living_cost_eur_max": None,
            "housing_options": [
                {
                    "provider": "ADISURC Campania",
                    "access": "ranking-based competitive allocation for eligible non-resident students",
                    "normal_duration": "10 months, no later than 30 September 2027",
                    "examples_in_naples": ["Brin", "Parthenope", "Campus X", "Bagnoli", "Pietrarsa"],
                    "source_url": ADISURC_CALL,
                },
                {
                    "provider": "Federico II International Welcome Desk",
                    "service": "flat/room search support, negotiation and legal/mediation assistance",
                    "partners_listed": ["TricTrac Hostel", "CampusX"],
                    "allocation_guaranteed": False,
                    "source_url": IWD_COSTS,
                },
            ],
            "official_rent_items": [
                {
                    "item": "shared double room",
                    "monthly_eur_min": 250,
                    "monthly_eur_max": 350,
                    "utilities_included": False,
                    "date_context": "University International Welcome Desk 2025/26 presentation uploaded in March 2026",
                    "source_url": IWD_COSTS,
                },
                {
                    "item": "single room",
                    "monthly_eur_min": 380,
                    "monthly_eur_max": 500,
                    "utilities_included": False,
                    "date_context": "University International Welcome Desk 2025/26 presentation uploaded in March 2026",
                    "source_url": IWD_COSTS,
                },
                {
                    "item": "studio apartment",
                    "monthly_eur_min": 600,
                    "monthly_eur_max": 900,
                    "utilities_included": False,
                    "date_context": "University International Welcome Desk 2025/26 presentation uploaded in March 2026",
                    "source_url": IWD_COSTS,
                },
            ],
            "official_living_cost_items": [
                {"item": "basic utilities", "monthly_eur_min": 100, "monthly_eur_max": 150, "source_url": IWD_COSTS},
                {"item": "groceries", "monthly_eur_min": 200, "monthly_eur_max": 300, "source_url": IWD_COSTS},
                {"item": "transport", "monthly_eur_min": 40, "monthly_eur_max": 50, "source_url": IWD_COSTS},
                {"item": "mobile phone", "monthly_eur_min": 15, "monthly_eur_max": 30, "source_url": IWD_COSTS},
            ],
            "housing_notes": bi(
                "ADISURC accommodation requires a separate benefits application and is allocated by ranking when places are limited. A non-resident scholarship classification generally requires a registered ten-month lease when no university residence is assigned.",
                "ADISURC konutu ayrı yardım başvurusu ister ve yerler sınırlıysa sıralamayla tahsis edilir. Üniversite yurdu verilmezse şehir dışı burs statüsü genellikle on aylık kayıtlı kira sözleşmesi gerektirir.",
            ),
            "verification_notes": bi(
                "Residence availability is verified for 2026/27. Rent and day-to-day cost figures come from the university's 2025/26 welcome presentation and are planning examples, not a 2026/27 market average or a housing guarantee.",
                "Yurt erişimi 2026/27 için doğrulanmıştır. Kira ve günlük yaşam tutarları üniversitenin 2025/26 karşılama sunumundaki planlama örnekleridir; 2026/27 piyasa ortalaması veya konut garantisi değildir.",
            ),
        }
    )

    row["application_timeline_profile"].update(
        {
            "academic_year": "2026/2027 closed application cycle; current enrolment, visa and ADISURC milestones",
            "non_eu_deadline": "2026-06-15",
            "application_deadline": "2026-06-15",
            "pre_enrolment_deadline": "2026-06-15",
            "enrollment_window": "2026-07-16 to 2026-11-02",
            "visa_sensitive_deadline": "2026-11-30",
            "scholarship_deadline": "2026-09-10T12:00:00+02:00",
            "timeline_risk": "high",
            "deadline_events": [
                {"event": "universitaly_pre_enrolment_deadline_overseas_non_eu", "date": "2026-06-15", "status": "closed"},
                {"event": "ordinary_enrolment_window_opens", "date": "2026-07-16", "status": "open_as_of_last_checked"},
                {"event": "adisurc_scholarship_and_services_deadline", "date": "2026-09-10T12:00:00+02:00", "status": "open_as_of_last_checked"},
                {"event": "recommended_university_enrolment_for_adisurc_housing_priority", "date": "2026-09-20", "status": "future_published"},
                {"event": "ordinary_enrolment_window_closes", "date": "2026-11-02", "status": "future_published"},
                {"event": "visa_application_submission_deadline", "date": "2026-11-30", "status": "future_published"},
                {"event": "adisurc_equivalent_isee_and_absolute_competition_enrolment_deadline", "date": "2027-03-31", "status": "future_published"},
            ],
            "deadline_notes": bi(
                "The overseas non-EU programme/pre-enrolment step closed on 15 June 2026. This is separate from Federico II enrolment, the ADISURC application and the visa deadline. No 2027/28 date is extrapolated from this closed cycle.",
                "Yurt dışındaki non-EU program/ön kayıt adımı 15 Haziran 2026'da kapandı. Bu tarih Federico II kaydı, ADISURC başvurusu ve vize son tarihinden ayrıdır. Kapanmış dönemden 2027/28 tarihi türetilmez.",
            ),
            "verification_notes": bi(
                "International students complete university enrolment through the relevant student registry rather than relying on the standard online path.",
                "Uluslararası öğrenciler standart çevrim içi yola güvenmek yerine ilgili öğrenci işleri birimi üzerinden üniversite kaydını tamamlar.",
            ),
        }
    )

    row["decision_summary"] = bi(
        "Strong direct aerospace fit with Aeronautics, Fluid Dynamics/Propulsion and Space pathways. For a Turkey-resident applicant, the decisive constraints are Italian B2, a closed 15 June 2026 Universitaly cycle, academic curricular review and non-guaranteed housing. Non-EU university contribution is zero in 2026/27, but EUR 167-189 mandatory tax/stamp planning and a separate competitive ADISURC application remain.",
        "Havacılık, Akışkanlar Dinamiği/İtki ve Uzay yollarıyla doğrudan güçlü havacılık-uzay uyumu vardır. Türkiye'de ikamet eden aday için belirleyici kısıtlar İtalyanca B2, 15 Haziran 2026'da kapanan Universitaly dönemi, akademik müfredat değerlendirmesi ve garanti edilmeyen konuttur. 2026/27'de non-EU üniversite katkısı sıfırdır; ancak 167-189 EUR zorunlu vergi/damga planı ve ayrı, rekabetçi ADISURC başvurusu gerekir.",
    )

    profile = row["source_profile"]
    profile["field_confidence"].update(
        {
            "program_basic_info": "high",
            "language": "high",
            "admission": "high",
            "non_eu_eligibility": "high",
            "tuition": "high",
            "scholarship": "high",
            "curriculum": "high",
            "living": "medium",
            "housing": "high",
            "deadlines": "high",
            "deadline": "high",
        }
    )
    profile["verification_notes"] = bi(
        "Current official sources now cover programme access, non-EU procedure, Italian B2, tuition/mandatory fees, ADISURC scholarship mechanics, deadlines and housing access. The university's room and daily-cost examples are retained at medium confidence because their presentation is labelled 2025/26.",
        "Güncel resmî kaynaklar program erişimi, non-EU süreci, İtalyanca B2, öğrenim/zorunlu ücretler, ADISURC burs süreci, tarihler ve konut erişimini kapsar. Üniversitenin oda ve günlük maliyet örnekleri, sunum 2025/26 etiketli olduğu için orta güvenle tutulur.",
    )
    upsert_sources(
        profile,
        [
            source(PROGRAM, "Ingegneria Aerospaziale (DF5) — Federico II", "official_program_page", ["program", "language", "admission", "curriculum"]),
            source(INTERNATIONAL_ADMISSION, "International admission regulation — Federico II", "official_admission_page", ["admission", "non_eu_eligibility", "language", "deadline", "visa"]),
            source(ENROLMENT, "Enrol at Federico II — 2026/27", "official_admission_page", ["admission", "deadline"]),
            source(FEE_GUIDE, "Federico II quick student guide 2026/27", "official_tuition_page", ["tuition", "fees", "deadline", "scholarship"], access_status="pdf"),
            source(ADISURC_LANDING, "ADISURC 2026/27 competition call approval", "official_housing_page", ["housing", "deadline"]),
            source(ADISURC_CALL, "ADISURC 2026/27 scholarship and services call — English", "official_scholarship_page", ["scholarship", "deadline"], access_status="pdf"),
            source(
                IWD_COSTS,
                "Federico II International Welcome Desk — accommodation and living-cost examples",
                "official_cost_of_living_page",
                ["housing", "living"],
                access_status="pdf",
                confidence="medium",
                notes=bi(
                    "Official university presentation uploaded in March 2026 but labelled Welcome Day 2025/26; figures are date-qualified planning examples.",
                    "Mart 2026'da yüklenen ancak Welcome Day 2025/26 etiketli resmî üniversite sunumu; tutarlar tarih bağlamıyla sınırlı planlama örnekleridir.",
                ),
            ),
        ],
    )
    finish(row)


def main() -> None:
    payload = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    rows = {row["id"]: row for row in payload["universities"]}
    update_record(rows["unina_aerospace_master"])
    payload["last_updated"] = CHECKED
    DATA_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Updated unina_aerospace_master with current 2026/27 official decision evidence.")


if __name__ == "__main__":
    main()
