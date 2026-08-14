"""Upgrade BUT Aerospace Technology with official 2026/27 admission, funding and housing evidence."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from unirank.core.integrity import audit_record


PATH = ROOT / "data_base" / "cekya.json"
RECORD_ID = "cz-but-aerospace-technology-msc"
CHECKED = "2026-08-14"
PROGRAM = "https://www.vut.cz/en/students/programmes/programme/9318"
CURRENT_LIST = "https://www.fme.vutbr.cz/en/studuj/studia-en/programy"
ADMISSION_INFO = "https://www.fme.vutbr.cz/en/studuj/studia-en/informace"
ADMISSION_RULE = "https://www.vut.cz/en/board/internal-legislation-fme/-d294652/s-5-25-aj-p307841"
ADMISSION_RULE_INDEX = "https://www.vut.cz/en/board/internal-legislation-fme/guideline-no-5-2025-admission-procedure-rules-and-conditions-for-admission-to-study-in-bachelor-s-and-master-s-degree-study-programmes-taught-in-english-for-the-academic-year-2026-2027-d294652"
FAQ = "https://www.vut.cz/en/students/admission-office/faq"
HOUSING_DOCUMENTS = "https://www.kam.vut.cz/english/Default.aspx?p=documents"
HOUSING_FOREIGN = "https://www.kam.vut.cz/english/default.aspx?p=PPV"
HOUSING_REQUEST = "https://www.kam.vut.cz/english/default.aspx?p=request"
JCMM = "https://www.jcmm.cz/projekt/stipendia_en/about-project"
JCMM_APPLY = "https://www.jcmm.cz/projekt/stipendia_en/how-to-sign-up"


def bi(en: str, tr: str) -> dict[str, str]:
    return {"en": en, "tr": tr}


def source(url: str, title: str, source_type: str, fields: list[str], en: str, tr: str, *, access_status: str = "ok", confidence: str = "high") -> dict:
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


def upsert_sources(profile: dict, additions: list[dict]) -> None:
    log = profile.setdefault("source_log", [])
    by_key = {(item.get("url"), item.get("source_type")): i for i, item in enumerate(log) if isinstance(item, dict)}
    for item in additions:
        key = (item["url"], item["source_type"])
        if key in by_key:
            log[by_key[key]] = item
        else:
            by_key[key] = len(log)
            log.append(item)


def update(row: dict) -> None:
    row.update(
        {
            "program_url": PROGRAM,
            "program_status": "active",
            "teaching_language": ["English"],
            "duration_years": 2,
        }
    )

    row["eligibility_profile"].update(
        {
            "eligible_for_non_eu": True,
            "target_applicant_route": "non_eu_permanent_resident_applying_to_english_follow_up_masters_2026_27",
            "required_previous_degree": bi(
                "A completed university Bachelor's degree relevant to the follow-up Master's programme, documented by a certified degree copy and Diploma Supplement. Foreign education must be assessed/recognised through the published route.",
                "Devam yüksek lisansıyla ilgili tamamlanmış lisans derecesi; tasdikli diploma kopyası ve Diploma Supplement ile belgelenir. Yabancı eğitim yayımlanmış yoldan değerlendirilip/tanınmalıdır.",
            ),
            "accepted_backgrounds": ["Mechanical Engineering", "Aeronautical/Aerospace Engineering", "related engineering subject to faculty assessment"],
            "minimum_gpa": None,
            "admission_mode": bi(
                "Electronic application followed by a written 90-minute entrance examination in mathematics, physics and technical mechanics. The examination is scored out of 300 and requires at least 90 points.",
                "Elektronik başvuruyu matematik, fizik ve teknik mekanikten 90 dakikalık yazılı giriş sınavı izler. Sınav 300 puan üzerinden değerlendirilir ve en az 90 puan gerekir.",
            ),
            "admission_risk": "high",
            "ranking_or_selection": "written_entrance_exam_and_fulfilment_of_document_language_requirements",
            "entrance_exam": {
                "required_by_default": True,
                "date": "2026-04-28",
                "duration_minutes": 90,
                "subjects": ["mathematics", "physics", "technical mechanics"],
                "maximum_points": 300,
                "minimum_points": 90,
                "remote_option_published": False,
                "waiver_for_turkey_degree_applicant_verified": False,
                "waiver_notes": bi(
                    "Published waiver routes are narrow (including specified SCIO performance or a current Czech/Slovak Bachelor's record). A Turkey-degree applicant should plan to sit the written exam unless FME grants a documented waiver.",
                    "Yayımlanmış muafiyet yolları dardır (belirli SCIO sonucu veya mevcut Çek/Slovak lisans kaydı dâhil). Türkiye diplomalı aday, FME belgeli muafiyet vermedikçe yazılı sınava girmeyi planlamalıdır.",
                ),
            },
            "programme_activation_minimum_admitted": 8,
            "programme_activation_exception_possible_by_dean": True,
            "maximum_admitted_across_follow_up_masters": 120,
            "required_documents": [
                bi("Electronic application", "Elektronik başvuru"),
                bi("English-language proof at programme-specific B1 CEFR or higher", "Programa özgü B1 CEFR veya üzeri İngilizce kanıtı"),
                bi("Certified copy of the completed Bachelor's degree", "Tamamlanmış lisans diplomasının tasdikli kopyası"),
                bi("Diploma Supplement", "Diploma Supplement"),
                bi("Signed request for assessment of foreign education", "Yabancı eğitimin değerlendirilmesi için imzalı talep formu"),
                bi("Electronic upload followed by postal or in-person originals/certified documents", "Elektronik yüklemenin ardından posta veya şahsen asıl/tasdikli belgeler"),
            ],
            "application_fee_eur": 28,
            "foreign_education_assessment_fee_eur": 30,
            "notes_for_turkish_students": bi(
                "Turkey is listed in BUT's published Student Mode information. This may simplify university coordination after admission, but it is not admission, accommodation or visa approval. The applicant still needs the admission letter and proof of accommodation.",
                "Türkiye, BUT'un yayımlanmış Student Mode bilgisinde listelenir. Bu, kabul sonrası üniversite koordinasyonunu kolaylaştırabilir; ancak kabul, konut veya vize onayı değildir. Adayın yine kabul yazısı ve konut kanıtına ihtiyacı vardır.",
            ),
            "verification_notes": bi(
                "The entrance-test invitation line and alternative-date line in the English directive contain apparent old-year typographical dates; only the internally consistent 28 April 2026 regular exam date is retained.",
                "İngilizce yönergede sınav daveti ve telafi tarihi satırlarında eski yıla ait görünen yazım hataları vardır; yalnızca kendi içinde tutarlı 28 Nisan 2026 normal sınav tarihi tutulur.",
            ),
            "gre": {
                "policy": "not_listed_as_required_or_scored_in_checked_2026_27_programme_sources",
                "test_type": None,
                "minimum_scores": {},
                "recommended_scores": {},
                "validity_rule": None,
                "waiver_rules": [],
                "source_ids": [ADMISSION_RULE, ADMISSION_INFO],
            },
        }
    )

    row["language_profile"].update(
        {
            "teaching_language": ["English"],
            "teaching_languages": ["English"],
            "english_required": True,
            "english_level_required": "B1 CEFR minimum in the FME 2026/27 programme-specific directive",
            "accepted_english_tests": ["Cambridge B1 Preliminary", "Cambridge B2 First", "IELTS", "TOEFL"],
            "minimum_scores": {
                "IELTS": "published as level 5 or 6 without a single decimal minimum",
                "TOEFL": "published score bands 42–71 or 72–94; edition not specified",
            },
            "medium_of_instruction_accepted": True,
            "english_exemptions": ["Applicants from countries where English is an official language", "official prior-school/university English-medium statement"],
            "italian_required": False,
            "mixed_language_warning": bi(
                "The central BUT FAQ states B2 for English programmes, while the binding FME 2026/27 directive sets B1 for Aerospace Technology. The programme-specific directive is retained as the formal minimum; B2 is the prudent preparation target until the faculty resolves the public inconsistency.",
                "Merkezi BUT SSS sayfası İngilizce programlar için B2 derken bağlayıcı FME 2026/27 yönergesi Aerospace Technology için B1 belirler. Resmî taban olarak programa özgü yönerge tutulur; fakülte kamusal çelişkiyi giderene kadar B2 ihtiyatlı hazırlık hedefidir.",
            ),
            "language_risk": "medium",
            "verification_notes": bi("Do not convert the published IELTS/TOEFL bands into an invented single cut-off.", "Yayımlanmış IELTS/TOEFL bantları uydurma tek bir taban puana dönüştürülmez."),
        }
    )

    row["cost_profile"].update(
        {
            "academic_year": "2026/2027",
            "tuition_eur_per_year_min": 3000,
            "tuition_eur_per_year_max": 3000,
            "tuition_eur_per_year_estimated": 3000,
            "tuition_basis": "English-taught FME programme, EU and non-EU, per academic year",
            "application_fee_eur": 28,
            "foreign_education_assessment_fee_eur": 30,
            "total_academic_cost_eur_per_year_estimated": None,
            "tuition_items": [
                {"name": "annual English-programme tuition", "amount_eur": 3000, "period": "academic_year", "applicant_scope": "all", "mandatory": True},
                {"name": "application fee paid outside Czechia", "amount_eur": 28, "period": "application", "applicant_scope": "international", "mandatory": True},
                {"name": "foreign-education assessment fee paid outside Czechia", "amount_eur": 30, "period": "application", "applicant_scope": "foreign_qualification_if_using_internal_assessment", "mandatory": True},
            ],
            "source_notes": bi(
                "The current 2026/27 FME directive sets EUR 3,000 per academic year. Application and foreign-education assessment fees are additional and non-refundable where applicable.",
                "Güncel 2026/27 FME yönergesi akademik yıl başına 3.000 EUR belirler. Uygulanabildiği durumda başvuru ve yabancı eğitim değerlendirme ücretleri ek ve iade edilmez niteliktedir.",
            ),
        }
    )
    row["tuition_eur_per_year"] = 3000
    row["annual_fee_eur"] = 3000

    row["scholarship_profile"].update(
        {
            "regional_scholarship_available": True,
            "regional_scholarship_name": "JCMM Scholarships for Students of English Programmes 2026/27",
            "non_eu_eligible": True,
            "application_mode": "separate",
            "automatic_consideration": False,
            "separate_application_required": True,
            "scholarship_deadline": "2026-04-30",
            "available_types": ["JCMM half-tuition scholarship", "FME merit scholarship", "BUT accommodation scholarship"],
            "opportunities": [
                {
                    "name": "JCMM Scholarships for Students of English Programmes 2026/27",
                    "programme_eligible": "Aerospace Technology",
                    "non_eu_eligible": True,
                    "age_limit": 30,
                    "completed_bachelor_required": True,
                    "amount_eur_per_year_max": 1500,
                    "duration": "standard full Master's duration",
                    "total_awards_across_supported_programmes_max": 30,
                    "application_mode": "separate",
                    "application_window": {"opens": "2026-02-01", "closes": "2026-04-30"},
                    "status_as_of_last_checked": "closed",
                    "final_selection_date": "2026-06-30",
                    "automatic_consideration": False,
                },
                {
                    "name": "FME merit scholarship",
                    "amount_czk_per_month_min": 1000,
                    "amount_czk_per_month_max": 3000,
                    "earliest_timing": "second year",
                    "selection": "excellent study results",
                    "application_mode": "not_published_on_checked_page",
                },
                {
                    "name": "BUT accommodation scholarship",
                    "amount_czk_per_month": 550,
                    "application_mode": "not_published_on_checked_FME_page",
                },
            ],
            "funding_competitiveness": "high",
            "funding_notes": bi(
                "JCMM is a separate application and does not reduce the tuition automatically. The 2026/27 call has closed. The FME page also publishes smaller merit and accommodation awards without enough mechanics to label them automatic.",
                "JCMM ayrı başvurudur ve öğrenim ücretini otomatik düşürmez. 2026/27 çağrısı kapanmıştır. FME sayfası ayrıca daha küçük başarı ve konut destekleri yayımlar; bunları otomatik saymak için yeterli süreç bilgisi yoktur.",
            ),
        }
    )

    row["living_profile"].update(
        {
            "city_cost_level": "unknown",
            "housing_access": "not_guaranteed",
            "housing_allocation_mode": "available_by_separate_request",
            "housing_application_separate": True,
            "student_housing_available": True,
            "housing_difficulty": "medium",
            "living_risk": "medium",
            "average_room_rent_eur": None,
            "average_room_rent_eur_min": None,
            "average_room_rent_eur_max": None,
            "daily_dorm_rate_czk_min": 148,
            "daily_dorm_rate_czk_max": 157,
            "monthly_living_cost_eur_min": None,
            "monthly_living_cost_eur_max": None,
            "monthly_living_cost_eur_estimated": None,
            "housing_options": [
                {
                    "provider": "BUT Halls of Residence and Dining Services",
                    "eligible_scope": "foreign internal degree students in self-payer English programmes",
                    "contract_period": "2026-09-01 to 2027-06-30 winter-term request",
                    "application": "separate online request",
                    "visa_materials_supported": True,
                    "guaranteed": False,
                }
            ],
            "official_rent_items": [
                {"room": "one bed in a double room", "amount_czk_per_day_per_person": 157, "vat_included": True},
                {"room": "separate three-bed room with shower and toilet", "amount_czk_per_day_per_person": 148, "vat_included": True},
            ],
            "official_living_cost_items": [],
            "housing_notes": bi(
                "The current foreign-student residence page lists CZK 148–157 per person per day and explicitly includes self-paying foreign students in English programmes. The 2026/27 request is separate and asks for visa details. A bed is not guaranteed.",
                "Güncel yabancı öğrenci yurt sayfası kişi başına günlük 148–157 CZK listeler ve İngilizce programlardaki ücretli yabancı öğrencileri açıkça kapsar. 2026/27 talebi ayrıdır ve vize bilgilerini ister. Yatak garanti edilmez.",
            ),
            "verification_notes": bi(
                "Daily official dormitory rates are retained in CZK and are not converted into a monthly private-market average. No current complete Brno living-cost total is inferred.",
                "Resmî günlük yurt ücretleri CZK olarak tutulur ve aylık özel piyasa ortalamasına dönüştürülmez. Güncel tam Brno yaşam maliyeti toplamı türetilmez.",
            ),
        }
    )

    row["application_timeline_profile"] = {
        "academic_year": "2026/2027",
        "intake_terms": ["Autumn 2026"],
        "application_deadline": "2026-03-31",
        "non_eu_deadline": "2026-03-31",
        "timeline_risk": "high",
        "deadline_events": [
            {"event": "online_application", "opens": "2025-11-01", "date": "2026-03-31", "status": "closed", "applicant_scope": "all"},
            {"event": "application_fee_credit", "date": "2026-04-07", "status": "closed", "applicant_scope": "all"},
            {"event": "written_entrance_exam", "date": "2026-04-28", "status": "closed", "applicant_scope": "not_waived_applicants"},
            {"event": "jcmm_scholarship", "opens": "2026-02-01", "date": "2026-04-30", "status": "closed", "applicant_scope": "eligible_non_eu_under_31"},
            {"event": "non_eu_document_submission", "date": "2026-05-15", "status": "closed", "applicant_scope": "permanent_residence_outside_eu"},
            {"event": "dormitory_request", "opens": "2026-04", "date": None, "status": "request_page_active_as_of_last_checked", "applicant_scope": "students_seeking_but_housing"},
        ],
        "deadline_notes": bi(
            "The 2026/27 admission, fee, exam, non-EU document and JCMM deadlines have passed. No 2027/28 date is inferred from them.",
            "2026/27 kabul, ücret, sınav, AB-dışı belge ve JCMM son tarihleri geçmiştir. Bunlardan 2027/28 tarihi türetilmez.",
        ),
        "verification_notes": bi("Programme-specific FME dates override generic university FAQ timing.", "Programa özgü FME tarihleri genel üniversite SSS takvimine üstün gelir."),
    }

    profile = row["source_profile"]
    upsert_sources(
        profile,
        [
            source(PROGRAM, "BUT Aerospace Technology programme and course plan", "official_program_page", ["program", "language", "curriculum", "tuition"], "Official English programme page verifies accreditation, duration, tuition and the detailed 2025/26 course plan.", "Resmî İngilizce program sayfası akreditasyonu, süreyi, ücreti ve ayrıntılı 2025/26 ders planını doğrular."),
            source(CURRENT_LIST, "FME English Master's programme list", "official_program_page", ["program", "language", "scholarship"], "Current faculty list confirms Aerospace Technology remains an English Master's option and identifies JCMM funding.", "Güncel fakülte listesi Aerospace Technology'nin İngilizce yüksek lisans seçeneği olarak sürdüğünü ve JCMM desteğini doğrular."),
            source(ADMISSION_RULE, "FME English admission directive 2026/27", "official_admission_page", ["admission", "non_eu_eligibility", "language", "tuition", "deadline"], "Binding current call verifies eligibility, B1, exam, fees, dates, document route and activation rule.", "Bağlayıcı güncel çağrı uygunluğu, B1'i, sınavı, ücretleri, tarihleri, belge yolunu ve açılış kuralını doğrular.", access_status="pdf"),
            source(ADMISSION_RULE_INDEX, "FME guideline no. 5/2025 status page", "official_admission_page", ["admission", "deadline"], "Official index marks the 2026/27 directive up to date.", "Resmî dizin 2026/27 yönergesini güncel olarak işaretler."),
            source(ADMISSION_INFO, "FME degree studies in English — 2026/27 information", "official_admission_page", ["admission", "non_eu_eligibility", "language", "tuition", "scholarship", "deadline", "housing"], "Current faculty page corroborates dates, documents, B1 mechanics, fees, awards and April dormitory requests.", "Güncel fakülte sayfası tarihleri, belgeleri, B1 yöntemini, ücretleri, destekleri ve Nisan yurt taleplerini doğrular."),
            source(FAQ, "BUT international admission FAQ", "official_university_policy_page", ["language", "admission", "non_eu_eligibility", "tuition", "housing"], "Central FAQ corroborates non-EU/visa mechanics and records a public B2 conflict that is not allowed to override the FME directive.", "Merkezi SSS AB-dışı/vize yöntemlerini doğrular ve FME yönergesine üstün tutulmayan kamusal B2 çelişkisini kaydeder.", confidence="medium"),
            source(HOUSING_DOCUMENTS, "BUT 2026/27 residence documents", "official_housing_page", ["housing", "living"], "Current official index publishes the 2026/27 contract, rules and September 2026 foreign-student price list.", "Güncel resmî dizin 2026/27 sözleşmesini, kurallarını ve Eylül 2026 yabancı öğrenci tarifesini yayımlar."),
            source(HOUSING_FOREIGN, "BUT accommodation for foreign degree students", "official_housing_page", ["housing", "living"], "Current page verifies eligibility for self-paying English-degree students and daily bed rates.", "Güncel sayfa ücretli İngilizce derece öğrencilerinin uygunluğunu ve günlük yatak ücretlerini doğrular."),
            source(HOUSING_REQUEST, "BUT 2026/27 foreign-student dormitory request", "official_housing_page", ["housing", "deadline"], "Current request page verifies the separate 2026/27 winter-term application and visa-detail workflow.", "Güncel talep sayfası ayrı 2026/27 kış dönemi başvurusunu ve vize bilgi sürecini doğrular."),
            source(JCMM, "JCMM Scholarships for Students of English Programmes 2026/27", "official_scholarship_page", ["scholarship", "funding", "eligibility", "deadline"], "Official programme page explicitly includes Aerospace Technology and publishes non-EU, age, amount and award-count rules.", "Resmî program sayfası Aerospace Technology'yi açıkça içerir ve AB-dışı, yaş, tutar ve ödül sayısı kurallarını yayımlar."),
            source(JCMM_APPLY, "JCMM English-programme scholarship application", "official_scholarship_page", ["scholarship", "deadline"], "Official application page verifies the separate 1 February–30 April 2026 window.", "Resmî başvuru sayfası ayrı 1 Şubat–30 Nisan 2026 dönemini doğrular."),
        ],
    )
    profile.update({
        "official_program_page": PROGRAM,
        "official_admission_page": ADMISSION_RULE,
        "official_tuition_page": ADMISSION_RULE,
        "official_scholarship_page": JCMM,
        "official_curriculum_page": PROGRAM,
        "official_housing_page": HOUSING_DOCUMENTS,
        "last_verified": CHECKED,
    })
    profile.setdefault("field_confidence", {}).update({
        "program_basic_info": "high", "program": "high", "language": "high", "admission": "high", "non_eu_eligibility": "high",
        "tuition": "high", "scholarship": "high", "deadline": "high", "deadlines": "high", "curriculum": "high", "housing": "high", "living": "high",
    })

    row.setdefault("decision_summary", {}).update(
        {
            "main_strengths": [
                bi("Direct English aerospace curriculum with aircraft design, CFD, autonomous flight, space structures, space flight mechanics and spacecraft technologies", "Uçak tasarımı, CFD, otonom uçuş, uzay yapıları, uzay uçuş mekaniği ve uzay aracı teknolojileri içeren doğrudan İngilizce havacılık-uzay müfredatı"),
                bi("Moderate verified EUR 3,000 tuition and a separate JCMM half-tuition route", "Doğrulanmış makul 3.000 EUR ücret ve ayrı JCMM yarım ücret bursu yolu"),
                bi("Official residence route for foreign self-paying English-degree students", "Ücretli İngilizce derece öğrencileri için resmî yurt yolu"),
            ],
            "main_risks": [
                bi("All 2026/27 admission and JCMM deadlines are closed", "Tüm 2026/27 kabul ve JCMM son tarihleri kapalıdır"),
                bi("A written in-person-style technical entrance exam should be assumed unless a waiver is documented", "Belgeli muafiyet olmadıkça yazılı, yüz yüze tarz teknik giriş sınavı varsayılmalıdır"),
                bi("Public B1/B2 English guidance conflicts; B2 is the safer preparation target", "Kamusal B1/B2 İngilizce rehberi çelişir; B2 daha güvenli hazırlık hedefidir"),
                bi("Dormitory rates are verified but a bed is not guaranteed", "Yurt ücretleri doğrulanmıştır ancak yatak garanti edilmez"),
            ],
            "application_reality": bi(
                "A Turkey applicant should be ready before November with certified degree documents, B2-level practical English, the EUR 28 application and EUR 30 assessment fees, travel/exam planning and a separate JCMM submission.",
                "Türkiye'den aday Kasım öncesinde tasdikli diploma belgeleri, pratikte B2 İngilizce, 28 EUR başvuru ve 30 EUR değerlendirme ücretleri, seyahat/sınav planı ve ayrı JCMM başvurusuyla hazır olmalıdır.",
            ),
            "overall_recommendation": bi(
                "Strong technical-value option for an exam-ready applicant; not a current 2026/27 application route as of the verification date.",
                "Sınava hazır aday için teknik değer açısından güçlü seçenek; doğrulama tarihinde güncel 2026/27 başvuru yolu değildir.",
            ),
        }
    )
    row.setdefault("scoring_inputs", {}).setdefault("hard_filter_flags", {}).update(
        {
            "english_only_compatible": True,
            "requires_italian": False,
            "non_eu_eligible": True,
            "tuition_above_5000": False,
            "tuition_above_10000": False,
            "deadline_unclear": False,
            "deadline_closed_for_new_applicants": True,
            "housing_guaranteed": False,
            "needs_verification": False,
        }
    )

    quality = audit_record(row)
    quality["audited_at"] = CHECKED
    row["data_quality"] = quality
    complete = quality["status"] == "verified"
    row["quality_control"] = {
        "qc_status": "passed" if complete else "needs_revision",
        "checked_at": CHECKED,
        "failed_canary_tests": [] if complete else ["missing_or_unverified_critical_fields" if quality["unverified_critical_fields"] else "critical_field_confidence_below_high"],
        "remaining_verification_tasks": [],
        "qc_notes": bi(
            "All core decision fields have current official evidence. The old-year typos and central B2/faculty B1 discrepancy remain visible rather than being silently harmonised.",
            "Tüm temel karar alanlarında güncel resmî kanıt vardır. Eski yıl yazım hataları ile merkezi B2/fakülte B1 çelişkisi sessizce uyumlaştırılmadan görünür tutulur.",
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
