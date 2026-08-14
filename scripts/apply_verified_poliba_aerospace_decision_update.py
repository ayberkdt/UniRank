"""Apply current official 2026/27 decision evidence to PoliBa Aerospace Engineering."""

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

PROGRAM = "https://orientami.poliba.it/aerospace-engineering-laurea-magistrale-poliba/"
GENERAL_OVERVIEW = "https://develop.poliba.it/en/general-overview"
MASTER_ADMISSION = "https://develop.poliba.it/it/node/14994"
ENROLMENT = "https://develop.poliba.it/it/iscrizioni"
ADISU_SCHOLARSHIP = "https://www.adisupuglia.it/pagina106703_borse-di-studio.html"
REGION_SCHOLARSHIP = "https://concorsi.regione.puglia.it/web/press-regione/-/diritto-allo-studio-regione-puglia-approva-gli-indirizzi-per-il-bando-adisu-2026-2027"
ADISU_HOUSING = "https://adisupuglia.it/pagina116497_alloggi.html"
POLIBA_HOUSING = "https://orientami.poliba.it/relazioni-internazionali-poliba/"


def bi(en: str, tr: str) -> dict[str, str]:
    return {"en": en, "tr": tr}


def source(
    url: str,
    title: str,
    source_type: str,
    fields: list[str],
    *,
    confidence: str = "high",
) -> dict:
    return {
        "url": url,
        "title": title,
        "source_type": source_type,
        "access_status": "ok",
        "last_checked": CHECKED,
        "relevant_fields": fields,
        "confidence": confidence,
        "notes": bi(
            "Current official source checked for the listed fields; unpublished values are not inferred.",
            "Listelenen alanlar için güncel resmî kaynak kontrol edildi; yayımlanmayan değerler türetilmez.",
        ),
    }


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
                "Add the 2026/27 student-contribution regulation when published and replace the conditional residence-cost fact with current Taranto/Lecce private-rent evidence if the universities publish it.",
                "2026/27 öğrenci katkı yönetmeliği yayımlandığında ekleyin; üniversiteler yayımlarsa koşullu yurt maliyeti bilgisini güncel Taranto/Lecce özel kira kanıtıyla tamamlayın.",
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
            "All critical fields have accessible official evidence, but incomplete fee and private-rent publication remains explicitly qualified.",
            "Tüm kritik alanlarda erişilebilir resmî kanıt vardır; ancak eksik ücret ve özel kira yayını açıkça sınırlı tutulur.",
        ),
    }
    profile["needs_verification"] = not complete


def update(row: dict) -> None:
    row.update(
        {
            "city": "Taranto / Lecce",
            "campus": [
                "Taranto — Aeronautics Design curriculum",
                "Lecce — Aerospace Design curriculum",
            ],
            "teaching_language": ["English"],
            "program_url": PROGRAM,
        }
    )
    row["location"] = {
        "country": "Italy",
        "city": "Taranto / Lecce",
        "latitude": None,
        "longitude": None,
        "locationConfidence": "multi_campus",
        "notes": bi(
            "The degree has two delivery campuses; a single Bari point would be misleading.",
            "Derecenin iki eğitim kampüsü vardır; tek bir Bari noktası yanıltıcı olur.",
        ),
    }

    row["eligibility_profile"].update(
        {
            "eligible_for_non_eu": True,
            "required_previous_degree": bi(
                "A completed first-cycle degree or equivalent foreign academic qualification; the programme verifies curricular requirements, individual preparation and English competence.",
                "Tamamlanmış birinci kademe lisans veya eşdeğer yabancı akademik yeterlilik; program müfredat koşullarını, bireysel hazırlığı ve İngilizce yeterliliğini denetler.",
            ),
            "accepted_backgrounds": [
                "Aerospace engineering",
                "Other engineering first-cycle backgrounds subject to individual curriculum analysis",
            ],
            "admission_mode": bi(
                "The Esse3 evaluation request is the admission procedure. Only one second-cycle programme may be selected, and the Bachelor's degree must already have been awarded before applying.",
                "Esse3 değerlendirme talebi kabul prosedürünün kendisidir. Yalnızca bir ikinci kademe program seçilebilir ve başvurmadan önce lisans derecesi alınmış olmalıdır.",
            ),
            "ranking_or_selection": "curricular requirements, individual preparation and language-competence assessment",
            "admission_risk": "high",
            "required_documents": [
                bi("Passport", "Pasaport"),
                bi("Bachelor's degree certificate", "Lisans diploması"),
                bi("Transcript of records", "Transkript"),
                bi("English translation for documents used for the English-taught programme", "İngilizce yürütülen program için belgelerin İngilizce çevirisi"),
                bi("Proof of qualification authenticity: CIMEA verification, ENIC-NARIC statement, legalisation/apostille or direct institutional verification", "Yeterlilik özgünlük kanıtı: CIMEA doğrulama, ENIC-NARIC belgesi, tasdik/apostil veya kurumdan doğrudan doğrulama"),
                bi("At enrolment: visa, residence-permit documentation and CIMEA comparability/Declaration of Value or applicable Diploma Supplement route", "Kayıtta: vize, oturum izni belgeleri ve CIMEA karşılaştırılabilirlik/Değer Beyanı veya uygulanabilir Diploma Supplement yolu"),
                bi("B2 English evidence where required by the programme regulation", "Program yönetmeliğinin istediği durumda İngilizce B2 kanıtı"),
            ],
            "cv_required": False,
            "motivation_letter_required": False,
            "recommendation_required": False,
            "interview_required": None,
            "test_required": None,
            "gre": {
                "policy": "not_listed_as_required_in_checked_official_sources",
                "test_type": None,
                "minimum_scores": {},
                "recommended_scores": {},
                "validity_rule": None,
                "waiver_rules": [],
                "source_ids": [GENERAL_OVERVIEW, MASTER_ADMISSION],
            },
            "notes_for_turkish_students": bi(
                "A Turkey-resident applicant uses both Universitaly pre-enrolment and the PoliBa Esse3 admission evaluation. Universitaly does not replace the academic assessment. Qualification and transcript translations for this English-taught degree are in English during evaluation; legalised documents are required at enrolment.",
                "Türkiye'de ikamet eden aday hem Universitaly ön kaydını hem PoliBa Esse3 kabul değerlendirmesini kullanır. Universitaly akademik değerlendirmenin yerini almaz. İngilizce yürütülen bu derece için diploma ve transkript değerlendirme aşamasında İngilizceye çevrilir; kayıt aşamasında tasdikli belgeler gerekir.",
            ),
            "verification_notes": bi(
                "The programme accepts non-aerospace first-cycle preparation in principle, but the official page does not convert that statement into guaranteed eligibility or a fixed ECTS matrix for every foreign degree.",
                "Program ilke olarak havacılık-uzay dışı birinci kademe altyapıları kabul edebilir; ancak resmî sayfa bunu her yabancı diploma için garantili uygunluk veya sabit AKTS matrisine dönüştürmez.",
            ),
        }
    )

    row["language_profile"].update(
        {
            "teaching_language": ["English"],
            "teaching_languages": ["English"],
            "english_required": True,
            "english_level_required": "B2 CEFR",
            "accepted_english_tests": [],
            "english_exemptions": [],
            "italian_required": False,
            "italian_level_required": None,
            "italian_needed_for_life_or_internship": bi(
                "Not an admission language for this English-taught degree; useful for housing, administration and local work in Taranto/Lecce.",
                "İngilizce yürütülen bu derecenin kabul dili değildir; Taranto/Lecce'de konut, idare ve yerel çalışma için faydalıdır.",
            ),
            "mixed_language_warning": bi(
                "Both current curricula are stated to be taught in English. Exact accepted-certificate mechanics should still be checked against the programme regulation before enrolment.",
                "Güncel iki müfredatın da İngilizce yürütüldüğü belirtilir. Kesin kabul edilen sertifika yöntemi yine de kayıt öncesi program yönetmeliğinden kontrol edilmelidir.",
            ),
            "language_risk": "medium",
            "verification_notes": bi(
                "The university's 2026/27 foreign-qualification guide makes B2 evidence mandatory at enrolment when the English-taught master's regulation requires it. No programme-specific IELTS/TOEFL numeric table was retained without the current aerospace regulation text.",
                "Üniversitenin 2026/27 yabancı diploma rehberi, İngilizce yüksek lisans yönetmeliği istediğinde B2 kanıtını kayıtta zorunlu kılar. Güncel havacılık-uzay yönetmeliği metni olmadan programa özgü IELTS/TOEFL sayısal tablosu tutulmamıştır.",
            ),
        }
    )

    row["cost_profile"].update(
        {
            "academic_year": "2026/2027",
            "tuition_eur_per_year_min": None,
            "tuition_eur_per_year_max": None,
            "tuition_eur_per_year_estimated": None,
            "student_contribution_eur": None,
            "regional_tax_eur": 120,
            "stamp_duty_eur": 16,
            "enrollment_fee_eur": 136,
            "mandatory_first_installment_eur": 136,
            "tuition_basis": "income_based_full_contribution_not_yet_verified_for_2026_27",
            "total_academic_cost_eur_per_year_estimated": None,
            "tuition_items": [
                {
                    "name": "2026/27 first enrolment instalment",
                    "amount_eur": 136,
                    "components": {"ADISU_regional_tax_initial_amount_eur": 120, "stamp_duty_eur": 16},
                    "note": "A later ADISU adjustment and income/merit-based contribution instalments may apply",
                    "source_url": ENROLMENT,
                }
            ],
            "historical_full_contribution_reference": {
                "academic_year": "2025/2026",
                "maximum_eur": 2121,
                "use_for_2026_27": False,
            },
            "source_notes": bi(
                "The current enrolment page verifies only the EUR 136 first payment. The complete 2026/27 income-based contribution and the treatment of a Turkey-resident household are unknown until the current fee regulation is accessible; the 2025/26 maximum is not rolled forward.",
                "Güncel kayıt sayfası yalnızca 136 EUR ilk ödemeyi doğrular. 2026/27 gelir bazlı tam katkı ve Türkiye'de ikamet eden hanenin işlenişi, güncel ücret yönetmeliği erişilebilir olana kadar bilinmiyor; 2025/26 üst sınırı ileri taşınmaz.",
            ),
            "verification_notes": bi(
                "Do not display EUR 136 as the full annual tuition. It is an initial mandatory payment, not the complete personalised contribution.",
                "136 EUR tam yıllık öğrenim ücreti olarak gösterilmemelidir. Bu, kişiselleştirilmiş toplam katkı değil zorunlu ilk ödemedir.",
            ),
        }
    )

    row["scholarship_profile"].update(
        {
            "regional_scholarship_available": True,
            "regional_scholarship_name": "ADISU Puglia Benefits and Services 2026/27",
            "non_eu_eligible": True,
            "income_based": True,
            "application_mode": "separate",
            "automatic_consideration": False,
            "separate_application_required": True,
            "scholarship_deadline": "2026-08-13T12:00:00+02:00",
            "scholarship_application_url": ADISU_SCHOLARSHIP,
            "financial_thresholds": {"isee_eur_max": 26000, "ispe_eur_max": 56000},
            "opportunities": [
                {"name": "ADISU Puglia — off-campus base scholarship", "amount_eur": 7172, "source_url": REGION_SCHOLARSHIP},
                {"name": "ADISU Puglia — commuter base scholarship", "amount_eur": 4191, "source_url": REGION_SCHOLARSHIP},
                {"name": "ADISU Puglia — on-campus base scholarship", "amount_eur": 2891, "source_url": REGION_SCHOLARSHIP},
            ],
            "available_types": ["cash scholarship", "competitive accommodation", "canteen service"],
            "funding_competitiveness": "high",
            "funding_notes": bi(
                "The 2026/27 application was a separate online ADISU procedure from 14 July to 13 August 2026 and is now closed. The regional government publishes base amounts and economic ceilings; award and residence allocation remain conditional on the call, ranking, documents and available resources.",
                "2026/27 başvurusu 14 Temmuz-13 Ağustos 2026 arasında ayrı çevrim içi ADISU prosedürüydü ve artık kapalıdır. Bölgesel hükümet temel tutarları ve ekonomik eşikleri yayımlar; burs ve yurt tahsisi çağrı, sıralama, belgeler ve mevcut kaynağa bağlıdır.",
            ),
            "verification_notes": bi(
                "Foreign students can compete for ADISU accommodation and benefits. Exact foreign-income document mechanics must be followed from the English 2026/27 call; no automatic consideration is assumed.",
                "Yabancı öğrenciler ADISU konut ve yardımları için yarışabilir. Yabancı gelir belgelerinin kesin süreci İngilizce 2026/27 çağrısından izlenmelidir; otomatik değerlendirme varsayılmaz.",
            ),
        }
    )

    row["living_profile"].update(
        {
            "city_cost_level": "multi_campus_private_market_cost_not_officially_published",
            "monthly_living_cost_eur_min": None,
            "monthly_living_cost_eur_max": None,
            "monthly_living_cost_eur_estimated": None,
            "average_room_rent_eur": None,
            "average_room_rent_eur_min": None,
            "average_room_rent_eur_max": None,
            "housing_difficulty": "competitive_adisu_or_self_search",
            "housing_access": "not_guaranteed",
            "housing_application_separate": True,
            "student_housing_available": True,
            "student_housing_competitiveness": "high",
            "living_risk": "high",
            "housing_options": [
                {
                    "provider": "ADISU Puglia",
                    "access": "competitive for Italian and foreign off-campus students meeting merit, income and asset requirements",
                    "application": "preference indicated inside the annual scholarship application",
                    "locations_relevant_to_degree": ["Taranto", "Lecce"],
                    "source_url": ADISU_HOUSING,
                },
                {
                    "provider": "private market / university-listed support channels",
                    "access": "self-search; PoliBa does not reserve Student House places",
                    "source_url": POLIBA_HOUSING,
                },
            ],
            "official_rent_items": [
                {
                    "item": "ADISU residence monthly cash charge for a student winning both scholarship and accommodation",
                    "monthly_eur": 0,
                    "condition": "The residence value is deducted from the scholarship benefit; this is not a private-rent quote and allocation is competitive",
                    "source_url": ADISU_HOUSING,
                }
            ],
            "official_living_cost_items": [],
            "housing_notes": bi(
                "PoliBa explicitly says it does not provide reserved Student House places. ADISU places are obtained through competition; students select residence preferences in the separate annual benefits application.",
                "PoliBa öğrenci yurdunda ayrılmış yer sağlamadığını açıkça belirtir. ADISU yerleri yarışmayla alınır; öğrenci yurt tercihlerini ayrı yıllık yardım başvurusunda belirtir.",
            ),
            "verification_notes": bi(
                "No current official private-room range for Taranto or Lecce was found. Bari cost examples are not transferred to this two-campus record. The only stored cost is the conditional ADISU winner treatment.",
                "Taranto veya Lecce için güncel resmî özel oda aralığı bulunamadı. Bari maliyet örnekleri bu iki kampüslü kayda taşınmaz. Tutulan tek maliyet, koşullu ADISU kazananı uygulamasıdır.",
            ),
        }
    )

    row["curriculum_profile"].update(
        {
            "tracks": ["Aerospace Design", "Aeronautics Design"],
            "specializations": [
                "Aerospace Design — Lecce",
                "Aeronautics Design — Taranto",
            ],
            "technical_domains": ["fluid dynamics", "propulsion", "structures", "onboard systems", "flight mechanics", "numerical engineering methods"],
            "mandatory_courses": [],
            "elective_courses": [],
            "exact_course_count": None,
            "course_language_notes": bi("Both curricula are taught in English.", "Her iki müfredat da İngilizce yürütülür."),
            "curriculum_url": PROGRAM,
            "study_plan_url": PROGRAM,
            "verification_notes": bi(
                "The current official page verifies the two curricula and technical domains but does not expose a complete 2026/27 module table or exact course count. The stale Space Technology label is removed.",
                "Güncel resmî sayfa iki müfredatı ve teknik alanları doğrular; ancak tam 2026/27 ders tablosunu veya kesin ders sayısını yayımlamaz. Eski Space Technology etiketi kaldırılmıştır.",
            ),
        }
    )

    row["category_profile"].update(
        {
            "primary_categories": ["Aerospace Engineering"],
            "secondary_categories": ["Aeronautical Design", "Aerospace Systems"],
            "normalized_tags": ["aerodynamics", "propulsion", "structures_materials", "flight_mechanics", "onboard_systems", "numerical_methods"],
        }
    )

    row["application_timeline_profile"].update(
        {
            "academic_year": "2026/2027",
            "intake_terms": ["2026/27 academic year"],
            "application_rounds": [
                "2026-07-28 to 2026-09-15",
                "2026-10-01 to 2026-10-15",
                "2026-11-01 to 2026-11-15",
                "2026-12-01 to 2026-12-15",
                "2027-01-05 to 2027-01-20",
                "2027-02-01 to 2027-02-15",
                "2027-03-01 to 2027-03-15",
                "2027-04-01 to 2027-04-15",
                "2027-05-02 to 2027-05-10",
            ],
            "non_eu_deadline": None,
            "application_deadline": None,
            "pre_enrolment_required": True,
            "universitaly_required": True,
            "visa_sensitive_deadline": "2026-11-30",
            "enrollment_deadline": "2027-05-20",
            "scholarship_deadline": "2026-08-13T12:00:00+02:00",
            "timeline_risk": "high",
            "deadline_events": [
                {"event": "first_esse3_master_admission_window", "start": "2026-07-28", "date": "2026-09-15", "status": "open_as_of_last_checked"},
                {"event": "adisu_benefits_deadline", "date": "2026-08-13T12:00:00+02:00", "status": "closed"},
                {"event": "master_enrolment_window_opens", "date": "2026-09-22", "status": "future_published"},
                {"event": "visa_application_submission_target", "date": "2026-11-30", "status": "future_published"},
                {"event": "part_time_enrolment_becomes_mandatory", "date": "2027-02-01", "status": "future_published"},
                {"event": "last_esse3_master_admission_window", "start": "2027-05-02", "date": "2027-05-10", "status": "future_published"},
                {"event": "master_enrolment_window_closes", "date": "2027-05-20", "status": "future_published"},
            ],
            "deadline_notes": bi(
                "The first Esse3 evaluation window is open through 15 September 2026, but PoliBa publishes no single programme-specific overseas non-EU/Universitaly deadline. A visa applicant must start Universitaly separately and should not treat later spring rounds as visa-feasible. Enrolments from 1 February 2027 are compulsory part-time.",
                "İlk Esse3 değerlendirme penceresi 15 Eylül 2026'ya kadar açıktır; ancak PoliBa programa özgü tek bir yurt dışı non-EU/Universitaly son tarihi yayımlamaz. Vize adayı Universitaly'yi ayrıca başlatmalı ve sonraki bahar turlarını vize açısından uygulanabilir saymamalıdır. 1 Şubat 2027'den itibaren kayıtlar zorunlu yarı zamanlıdır.",
            ),
            "verification_notes": bi(
                "The application, enrolment, scholarship and visa clocks are separate. No 2027/28 date is inferred.",
                "Başvuru, üniversite kaydı, burs ve vize takvimleri ayrıdır. 2027/28 tarihi türetilmez.",
            ),
        }
    )

    row["decision_summary"] = bi(
        "Direct English-taught aerospace degree with current Aerospace Design (Lecce) and Aeronautics Design (Taranto) routes. A Turkey-resident applicant needs Universitaly plus Esse3 academic evaluation and B2-level English evidence. The first 2026/27 application window is still open, but the ADISU scholarship deadline has closed, housing is not guaranteed, and only the EUR 136 first payment—not the full personalised annual contribution—is currently verified.",
        "Güncel Aerospace Design (Lecce) ve Aeronautics Design (Taranto) yollarına sahip, doğrudan İngilizce havacılık-uzay derecesidir. Türkiye'de ikamet eden aday Universitaly yanında Esse3 akademik değerlendirmesi ve B2 düzeyi İngilizce kanıtı ister. İlk 2026/27 başvuru penceresi hâlâ açık; ancak ADISU burs tarihi kapanmıştır, konut garanti değildir ve kişiselleştirilmiş yıllık toplam katkı değil yalnızca 136 EUR ilk ödeme doğrulanmıştır.",
    )

    profile = row["source_profile"]
    profile.update(
        {
            "official_program_page": PROGRAM,
            "official_admission_page": MASTER_ADMISSION,
            "official_tuition_page": ENROLMENT,
            "official_scholarship_page": ADISU_SCHOLARSHIP,
            "official_curriculum_page": PROGRAM,
            "last_verified": CHECKED,
            "verification_notes": bi(
                "Accessible current official pages cover the active programme, English delivery, foreign-qualification route, admission windows, first fee, ADISU funding and competitive accommodation. Complete 2026/27 personalised contribution and private Taranto/Lecce rent remain unknown.",
                "Erişilebilir güncel resmî sayfalar aktif programı, İngilizce eğitimi, yabancı diploma yolunu, başvuru pencerelerini, ilk ücreti, ADISU finansmanını ve rekabetçi konutu kapsar. Tam 2026/27 kişiselleştirilmiş katkı ile özel Taranto/Lecce kirası bilinmiyor.",
            ),
        }
    )
    profile["field_confidence"].update(
        {
            "program_basic_info": "high",
            "language": "high",
            "admission": "high",
            "non_eu_eligibility": "high",
            "tuition": "medium",
            "scholarship": "high",
            "curriculum": "high",
            "living": "unknown",
            "housing": "high",
            "deadlines": "high",
            "deadline": "high",
            "location": "high",
        }
    )
    profile["source_log"] = [
        old
        for old in profile.get("source_log", [])
        if isinstance(old, dict)
        and old.get("access_status") not in {"blocked", "broken", "not_found", "unknown"}
        and old.get("url")
        not in {
            "https://orientami.poliba.it/aerospace-engineering-laurea-magistrale-poliba/",
            "https://www.poliba.it/en/laurea-magistrale-aerospace-engineering",
            "https://www.poliba.it/en/general-overview",
            "https://www.poliba.it/it/node/14994",
            "https://www.poliba.it/it/iscrizioni",
            "https://www.adisupuglia.it/pagina106703_borse-di-studio.html",
            "https://adisupuglia.it/pagina116497_alloggi.html",
            "https://adisupuglia.iswebcloud.it/pagina106703_borse-di-studio.html",
            "https://adisupuglia.iswebcloud.it/pagina116497_alloggi.html",
        }
    ]
    additions = [
        source(PROGRAM, "Master's Degree in Aerospace Engineering — PoliBa/UniSalento", "official_program_page", ["program", "language", "curriculum"]),
        source(GENERAL_OVERVIEW, "General Overview 2026/27 — foreign qualifications", "official_admission_page", ["admission", "non_eu_eligibility", "language", "deadline", "visa"]),
        source(MASTER_ADMISSION, "Second-cycle degree admission procedure 2026/27", "official_admission_page", ["admission", "deadline"]),
        source(ENROLMENT, "PoliBa enrolment and current first payment 2026/27", "official_tuition_page", ["tuition", "fees", "deadline"], confidence="medium"),
        source(ADISU_SCHOLARSHIP, "ADISU Puglia scholarship applications 2026/27", "official_scholarship_page", ["scholarship", "deadline"]),
        source(REGION_SCHOLARSHIP, "Puglia regional ADISU 2026/27 criteria and base amounts", "official_scholarship_page", ["scholarship"]),
        source(ADISU_HOUSING, "ADISU Puglia student accommodation", "official_housing_page", ["housing", "living"]),
        source(POLIBA_HOUSING, "PoliBa international relations — accommodation service", "official_housing_page", ["housing"]),
    ]
    by_url = {item.get("url"): i for i, item in enumerate(profile["source_log"])}
    for item in additions:
        if item["url"] in by_url:
            profile["source_log"][by_url[item["url"]]] = item
        else:
            by_url[item["url"]] = len(profile["source_log"])
            profile["source_log"].append(item)

    row["scoring_inputs"]["hard_filter_flags"].update(
        {
            "english_only_compatible": True,
            "requires_italian": False,
            "non_eu_eligible": True,
            "deadline_unclear": False,
            "needs_verification": True,
        }
    )
    finish(row)


def main() -> None:
    payload = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    row = next(item for item in payload["universities"] if item["id"] == "poliba_aerospace_master")
    update(row)
    payload["last_updated"] = CHECKED
    DATA_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Updated poliba_aerospace_master with current 2026/27 official evidence.")


if __name__ == "__main__":
    main()
