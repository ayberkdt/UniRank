"""Add current, programme-specific cost and application evidence for TU Berlin MSE."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data_base" / "almanya.json"
CHECKED = "2026-07-14"


def bi(en: str, tr: str) -> dict[str, str]:
    return {"en": en, "tr": tr}


def source(url: str, title: str, source_type: str, fields: list[str], en: str, tr: str, confidence: str = "high") -> dict[str, Any]:
    return {
        "url": url,
        "title": title,
        "source_type": source_type,
        "access_status": "ok",
        "last_checked": CHECKED,
        "relevant_fields": fields,
        "confidence": confidence,
        "notes": bi(en, tr),
    }


def add_source(row: dict[str, Any], entry: dict[str, Any]) -> None:
    profile = row.setdefault("source_profile", {})
    log = [item for item in profile.get("source_log", []) if isinstance(item, dict)]
    log = [
        item
        for item in log
        if (item.get("url"), item.get("source_type"))
        != (entry["url"], entry["source_type"])
    ]
    log.append(entry)
    profile["source_log"] = log
    profile["last_verified"] = CHECKED


def main() -> None:
    original = PATH.read_text(encoding="utf-8")
    rows: list[dict[str, Any]] = json.loads(original)
    row = next(item for item in rows if item.get("id") == "germany-tuberlin-mse-space-engineering")

    mse_home = "https://mse.tu-berlin.de/"
    requirements_url = "https://mse.tu-berlin.de/admission/requirements/"
    procedure_url = "https://mse.tu-berlin.de/admission/application-procedure/"
    form_url = "https://mse.tu-berlin.de/admission/application-form/"
    fees_url = "https://mse.tu-berlin.de/admission/fees-funding/"
    housing_url = "https://mse.tu-berlin.de/plan-your-stay/housing/"
    faq_url = "https://mse.tu-berlin.de/faqs/"
    d_stipendium_url = "https://www.tu.berlin/en/careerservice/d-stipendium/application/call-for-applications"

    row["cost_profile"].update({
        "academic_year": "current programme page checked 2026-07-14",
        "tuition_eur_per_year_min": None,
        "tuition_eur_per_year_max": None,
        "tuition_eur_per_year_estimated": None,
        "tuition_non_eu_full_program": {
            "amount": 24900,
            "currency": "EUR",
            "basis": "full_program",
            "academic_year": "current programme page checked 2026-07-14",
        },
        "tuition_basis": "published_full_programme_fee",
        "student_contribution_eur": 379.06,
        "total_academic_cost_eur_per_year_estimated": None,
        "payment_installments": "One instalment: EUR 9,960; then three instalments of EUR 4,980 each (published full-programme schedule).",
        "source_notes": bi(
            "MSE publishes EUR 24,900 tuition for the complete two-year programme, plus an EUR 379.06 organisation fee each semester. The organisation fee includes the Germany-wide public-transport ticket. The tuition is deliberately shown as a full-programme amount, not an invented annual split.",
            "MSE iki yıllık programın tamamı için 24.900 EUR öğrenim ücreti, ayrıca her dönem 379,06 EUR organizasyon ücreti yayımlar. Organizasyon ücreti Almanya genelinde geçerli toplu taşıma biletini içerir. Öğrenim ücreti uydurma yıllık bölünme yerine bilinçli olarak tam program tutarıyla gösterilir.",
        ),
        "verification_notes": bi(
            "This continuing-education programme has a programme-specific tuition fee; it must not be confused with the standard TU Berlin semester contribution alone.",
            "Bu sürekli eğitim programının programa özgü öğrenim ücreti vardır; yalnızca standart TU Berlin dönem katkısıyla karıştırılmamalıdır.",
        ),
    })
    row["scholarship_profile"].update({
        "regional_scholarship_available": None,
        "regional_scholarship_name": None,
        "merit_scholarships": [bi(
            "TU Berlin's 2026/27 Deutschlandstipendium call lists Space Engineering among expected subject earmarks, but the MSE programme itself states that it offers no scholarships. Treat this as a possible university-level route requiring confirmation, not as MSE funding.",
            "TU Berlin'in 2026/27 Deutschlandstipendium çağrısı Uzay Mühendisliğini beklenen alan tahsisleri arasında listeler; ancak MSE programı kendisinin burs sunmadığını belirtir. Bunu MSE bursu değil, teyit gerektiren olası üniversite düzeyi bir yol olarak değerlendirin.",
        )],
        "non_eu_eligible": None,
        "scholarship_deadline": "2026-07-15 23:59 (TU Berlin Deutschlandstipendium 2026/27; programme eligibility must be confirmed)",
        "scholarship_application_url": d_stipendium_url,
        "funding_competitiveness": "high",
        "funding_notes": bi(
            "MSE's own current Fees & Funding page says the study programme offers no scholarships and directs applicants to external funding. Separately, TU Berlin's current Deutschlandstipendium call mentions Space Engineering as an expected earmark and EUR 300/month for at least one year; the two statements are not enough to promise MSE eligibility, so confirm with the scholarship office before relying on it.",
            "MSE'nin güncel Ücretler ve Finansman sayfası programın burs sunmadığını ve adayları dış finansmana yönlendirdiğini belirtir. Ayrı olarak, TU Berlin'in güncel Deutschlandstipendium çağrısı Uzay Mühendisliğini beklenen alan tahsisi olarak ve en az bir yıl için ayda 300 EUR olarak anmaktadır; iki açıklama MSE uygunluğunu garanti etmeye yetmediğinden bu desteğe güvenmeden önce burs ofisiyle teyit edin.",
        ),
        "verification_notes": bi(
            "Conflicting official wording is kept visible rather than resolved by assumption.",
            "Çelişen resmî ifadeler varsayımla çözülmek yerine görünür tutulur.",
        ),
    })
    row["living_profile"].update({
        "city_cost_level": "very_high",
        "monthly_living_cost_eur_min": None,
        "monthly_living_cost_eur_max": None,
        "monthly_living_cost_eur_estimated": 1000,
        "monthly_living_cost_basis": bi(
            "MSE's current Fees & Funding page advises approximately EUR 1,000 per month for living expenses in Berlin, separately from tuition and organisation fees.",
            "MSE'nin güncel Ücretler ve Finansman sayfası, öğrenim ücreti ve organizasyon ücretinden ayrı olarak Berlin yaşam giderleri için ayda yaklaşık 1.000 EUR önerir.",
        ),
        "average_room_rent_eur": None,
        "average_room_rent_eur_min": None,
        "average_room_rent_eur_max": None,
        "student_housing_available": None,
        "student_housing_competitiveness": "high",
        "housing_difficulty": "high",
        "living_risk": "high",
        "housing_sentiment": None,
        "housing_notes": bi(
            "The official MSE housing page says Berlin demand is high and applicants should begin the search in advance. It lists housing platforms but does not publish a MSE rent figure or promise accommodation.",
            "Resmî MSE konut sayfası Berlin'de talebin yüksek olduğunu ve adayların aramaya önceden başlaması gerektiğini belirtir. Konut platformlarını listeler ancak MSE'ye özgü kira tutarı yayımlamaz veya konaklama garantisi vermez.",
        ),
        "verification_notes": bi(
            "The living figure is a programme-published planning estimate, not a rent quote.",
            "Yaşam tutarı programın yayımladığı planlama tahminidir; kira teklifi değildir.",
        ),
    })
    row["application_timeline_profile"].update({
        "academic_year": "current MSE admission guidance checked 2026-07-14",
        "intake_terms": ["Spring", "Fall"],
        "non_eu_deadline": "1 October (priority for Spring intake) / 1 April (priority for Fall intake); applications accepted year-round subject to remaining capacity",
        "eu_deadline": "1 October (priority for Spring intake) / 1 April (priority for Fall intake); applications accepted year-round subject to remaining capacity",
        "winter_deadline": None,
        "summer_deadline": None,
        "application_deadline": "1 October (priority for Spring intake) / 1 April (priority for Fall intake); applications accepted year-round subject to remaining capacity",
        "deadline_non_eu": None,
        "timeline_risk": "medium",
        "deadline_notes": bi(
            "The current MSE application form and FAQ say applications are accepted throughout the year. 1 October (Spring) and 1 April (Fall) are recommended priority dates, not absolute cutoffs; late applications depend on capacity. This replaces the unrelated standard TU Berlin Master's dates previously stored in the record.",
            "Güncel MSE başvuru formu ve SSS sayfası başvuruların yıl boyunca kabul edildiğini belirtir. 1 Ekim (Bahar) ve 1 Nisan (Güz) önerilen öncelik tarihleridir, mutlak son tarih değildir; geç başvurular kontenjana bağlıdır. Bu bilgi kayıtta daha önce yer alan ve programla ilgisiz standart TU Berlin yüksek lisans tarihlerini değiştirir.",
        ),
    })
    row["eligibility_profile"].update({
        "required_previous_degree": bi(
            "Completed university degree equivalent to at least a Bachelor's degree, or sufficient relevant work experience demonstrating comparable skills.",
            "En az lisans derecesine denk tamamlanmış üniversite derecesi veya denk becerileri gösteren yeterli ilgili iş deneyimi.",
        ),
        "required_documents": [
            bi("Curriculum vitae", "Özgeçmiş"),
            bi("Motivation letter", "Motivasyon mektubu"),
            bi("Transcripts and certificates from all higher-education institutions attended", "Katılım sağlanan tüm yükseköğretim kurumlarının transkript ve belgeleri"),
            bi("Recommendation letter(s) from an employer and/or academic supervisor", "İşveren ve/veya akademik danışmandan tavsiye mektup/mektupları"),
            bi("English-language proof", "İngilizce yeterlik belgesi"),
        ],
        "motivation_letter_required": True,
        "cv_required": True,
        "recommendation_required": True,
        "test_required": True,
        "notes": bi(
            "At least one year of practical experience is required; relevant internships, a practical Bachelor's thesis or equivalent activities can count. Applicants who have not completed the experience should contact MSE before applying.",
            "En az bir yıl uygulamalı deneyim gerekir; ilgili stajlar, uygulamalı lisans tezi veya eşdeğer etkinlikler sayılabilir. Deneyimini henüz tamamlamamış adaylar başvurmadan önce MSE ile iletişime geçmelidir.",
        ),
    })
    row["decision_summary"].update({
        "main_strengths": [bi(
            "A purpose-built international Space Engineering programme with 120 ECTS, flexible on-campus/online/hybrid study, and applications considered year-round subject to capacity.",
            "120 AKTS'lik, kampüs/çevrim içi/hibrit esnekliği olan ve kontenjan kaldığı sürece yıl boyunca başvuruları değerlendiren, amaca yönelik uluslararası Uzay Mühendisliği programı.",
        )],
        "main_risks": [
            bi("This is not a low-fee German public-MSc case: the published two-year tuition is EUR 24,900, plus EUR 379.06 each semester and about EUR 1,000/month living costs.", "Bu, düşük ücretli Alman devlet yüksek lisansı örneği değildir: yayımlanan iki yıllık öğrenim ücreti 24.900 EUR, buna her dönem 379,06 EUR ve ayda yaklaşık 1.000 EUR yaşam gideri eklenir."),
            bi("MSE itself states that it offers no scholarships; a TU Berlin Deutschlandstipendium reference is not a funding promise for this programme.", "MSE kendisinin burs sunmadığını belirtir; TU Berlin Deutschlandstipendium atfı bu program için finansman vaadi değildir."),
        ],
    })

    profile = row.setdefault("source_profile", {})
    profile.update({
        "official_program_page": mse_home,
        "official_admission_page": form_url,
        "official_tuition_page": fees_url,
        "official_scholarship_page": fees_url,
        "official_housing_page": housing_url,
        "needs_verification": False,
    })
    profile.setdefault("field_confidence", {}).update({
        "program_basic_info": "high",
        "language": "high",
        "admission": "high",
        "tuition": "high",
        "scholarship": "medium",
        "curriculum": "high",
        "housing": "high",
        "deadlines": "high",
    })

    for entry in [
        source(requirements_url, "MSE Admission Requirements", "official_admission_page", ["admission", "language", "non_eu"], "Current MSE page gives the degree/work-experience requirement, English-test thresholds and at least one year of practical experience.", "Güncel MSE sayfası derece/iş deneyimi şartını, İngilizce sınav eşiklerini ve en az bir yıl uygulamalı deneyimi verir."),
        source(procedure_url, "MSE Application Procedure", "official_admission_page", ["admission"], "Current MSE page lists CV, motivation letter, education records, recommendation letters and English proof; a successful applicant is invited to an online interview and accepts the place after a EUR 500 deposit.", "Güncel MSE sayfası özgeçmiş, motivasyon mektubu, eğitim belgeleri, tavsiye mektupları ve İngilizce belgesini listeler; başarılı aday çevrim içi görüşmeye davet edilir ve 500 EUR depozito sonrası yerini kabul eder."),
        source(form_url, "MSE Application Form and Priority Dates", "official_admission_page", ["deadline"], "Current MSE form says applications are considered after 1 October for Spring or 1 April for Fall as capacity remains; FAQ confirms these are priority dates and applications are accepted year-round.", "Güncel MSE formu başvuruların kontenjan kaldıkça Bahar için 1 Ekim veya Güz için 1 Nisan sonrasında da değerlendirildiğini söyler; SSS bu tarihlerin öncelik tarihi olduğunu ve başvuruların yıl boyu kabul edildiğini doğrular."),
        source(fees_url, "MSE Fees and Funding", "official_tuition_page", ["tuition", "fees"], "Current page publishes EUR 24,900 full two-year tuition, four instalments, EUR 379.06 organisation fee per semester and a EUR 1,000 monthly Berlin living-cost estimate.", "Güncel sayfa iki yıl için toplam 24.900 EUR öğrenim ücretini, dört taksiti, dönem başına 379,06 EUR organizasyon ücretini ve Berlin için aylık 1.000 EUR yaşam gideri tahminini yayımlar."),
        source(fees_url, "MSE Funding Statement", "official_scholarship_page", ["scholarship", "funding"], "Current MSE page explicitly says the programme does not offer scholarships and directs applicants to external funding sources.", "Güncel MSE sayfası programın burs sunmadığını açıkça belirtir ve adayları dış finansman kaynaklarına yönlendirir.", "high"),
        source(housing_url, "MSE Housing in Berlin", "official_housing_page", ["housing"], "Current programme page says Berlin housing demand is high and students should start their search in advance; it offers sources, not accommodation or a rent guarantee.", "Güncel program sayfası Berlin'de konut talebinin yüksek olduğunu ve öğrencilerin aramaya önceden başlaması gerektiğini belirtir; konaklama veya kira garantisi yerine kaynaklar sunar."),
        source(d_stipendium_url, "TU Berlin Deutschlandstipendium Call 2026/27", "official_scholarship_page", ["scholarship", "funding"], "Current call lists Space Engineering as an expected subject earmark, EUR 300 monthly for at least one year, approximately 120 awards and a 15 June–15 July 2026 application period; it does not override MSE's own no-scholarship statement.", "Güncel çağrı Uzay Mühendisliğini beklenen alan tahsisi olarak, en az bir yıl için aylık 300 EUR'u, yaklaşık 120 ödülü ve 15 Haziran–15 Temmuz 2026 başvuru dönemini listeler; MSE'nin kendi burs yok açıklamasını geçersiz kılmaz.", "medium"),
        source(faq_url, "MSE FAQs", "official_program_page", ["program", "curriculum", "deadline"], "Current FAQ confirms applications are accepted year-round, priority dates, 120 ECTS, optional internship and flexible study mode.", "Güncel SSS, başvuruların yıl boyu kabul edildiğini, öncelik tarihlerini, 120 AKTS'yi, isteğe bağlı stajı ve esnek eğitim şeklini doğrular."),
    ]:
        add_source(row, entry)

    newline = "\r\n" if "\r\n" in original else "\n"
    PATH.write_text(json.dumps(rows, ensure_ascii=False, indent=2).replace("\n", newline) + newline, encoding="utf-8")
    print("Updated TU Berlin Master of Space Engineering with current programme evidence.")


if __name__ == "__main__":
    main()
