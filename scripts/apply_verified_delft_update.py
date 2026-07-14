"""Add source-checked 2026/27 decision data for TU Delft Aerospace."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data_base" / "hollanda.json"
CHECKED = "2026-07-14"


def bi(en: str, tr: str) -> dict[str, str]:
    return {"en": en, "tr": tr}


def source(
    url: str,
    title: str,
    source_type: str,
    fields: list[str],
    en: str,
    tr: str,
    confidence: str = "high",
) -> dict[str, Any]:
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
    entries = [item for item in profile.get("source_log", []) if isinstance(item, dict)]
    entries = [
        item
        for item in entries
        if (item.get("url"), item.get("source_type"))
        != (entry["url"], entry["source_type"])
    ]
    entries.append(entry)
    profile["source_log"] = entries
    profile["last_verified"] = CHECKED


def main() -> None:
    original = PATH.read_text(encoding="utf-8")
    payload = json.loads(original)
    row = next(item for item in payload["programs"] if item.get("id") == "netherlands_delft_msc_aerospace")

    programme_url = "https://www.tudelft.nl/en/education/programmes/masters/ae/msc-aerospace-engineering"
    programme_admission_url = f"{programme_url}/admission-and-application"
    general_admission_url = "https://www.tudelft.nl/en/education/admission-and-application/msc-international-diploma/admission-requirements"
    documents_url = "https://www.tudelft.nl/en/education/admission-and-application/msc-international-diploma/required-documents"
    deadlines_url = "https://www.tudelft.nl/en/education/admission-and-application/msc-international-diploma/dates-deadlines"
    tuition_url = "https://www.tudelft.nl/en/education/study-programme-orientation/practical-matters/tuition-fee-finances"
    scholarship_url = "https://www.tudelft.nl/en/education/study-programme-orientation/practical-matters/scholarships/justus-louise-van-effen-excellence-scholarships"
    structure_url = f"{programme_url}/programme-structure"
    tracks_url = f"{programme_url}/master-tracks"
    housing_url = "https://www.tudelft.nl/en/education/study-programme-orientation/practical-matters/housing"
    cost_of_living_url = "https://www.studyinnl.org/finances/daily-student-expenses-and-cost-of-living-in-the-netherlands"
    space_department_url = "https://research.tudelft.nl/en/organisations/space-engineering/"
    cleanroom_url = "https://research.tudelft.nl/en/equipments/the-aerospace-engineering-cleanroom/"
    aircraft_url = "https://research.tudelft.nl/en/equipments/the-cessna-citation-ii-ph-lab/"

    row.update({
        "teaching_language": ["English"],
        "program_status": "active",
        "duration_years": 2,
        "ects": 120,
    })
    row["language_profile"].update({
        "teaching_language": ["English"],
        "english_required": True,
        "english_level_required": "IELTS Academic 7.0 overall (minimum 6.5 each); TOEFL iBT score requirements depend on the test-report date.",
        "accepted_english_tests": ["IELTS Academic", "TOEFL iBT", "Cambridge C1 Advanced", "Cambridge C2 Proficiency"],
        "language_risk": "low",
        "verification_notes": bi(
            "TU Delft states that all MSc programmes are taught in English. Its current general international-admission page publishes the accepted English tests and thresholds; TOEFL reporting changed on 21 January 2026.",
            "TU Delft tüm yüksek lisans programlarının İngilizce yürütüldüğünü belirtir. Güncel uluslararası kabul sayfası kabul edilen İngilizce sınavlarını ve eşikleri yayımlar; TOEFL raporlama ölçeği 21 Ocak 2026'da değişmiştir.",
        ),
    })
    row["eligibility_profile"].update({
        "eligible_for_non_eu": True,
        "required_previous_degree": bi(
            "A research-university bachelor's degree closely related to the chosen MSc programme.",
            "Seçilen yüksek lisans programıyla yakından ilişkili, araştırma üniversitesi düzeyinde lisans derecesi.",
        ),
        "accepted_backgrounds": [],
        "minimum_gpa": bi("At least 75% of the scale maximum, unless programme-specific requirements apply.", "Programa özgü şartlar aksi belirtmedikçe, ölçek üst sınırının en az %75'i."),
        "ranking_or_selection": bi(
            "For international BSc holders applying to Aerospace Engineering in 2026/27: GRE minimums are 154 Verbal, 163 Quantitative and 4.0 Analytical Writing; TU Delft states that candidates below a minimum are not eligible.",
            "2026/27 için Havacılık ve Uzay Mühendisliğine uluslararası lisans diplomasıyla başvuranlar: GRE asgari puanları Sözel 154, Sayısal 163 ve Analitik Yazma 4,0'dır; TU Delft bu barajların altındaki adayların uygun olmadığını belirtir.",
        ),
        "required_documents": [
            bi("Bachelor's diploma or certified statement of expected degree", "Lisans diploması veya beklenen dereceye ilişkin onaylı belge"),
            bi("Official academic transcript including the grading system", "Notlandırma sistemini içeren resmî transkript"),
            bi("Curriculum vitae", "Özgeçmiş"),
            bi("Motivation letter", "Niyet/motivasyon mektubu"),
            bi("Proof of identity", "Kimlik belgesi"),
            bi("English-language certificate when required", "Gerektiğinde İngilizce yeterlik belgesi"),
            bi("GRE score report for the international-BSc Aerospace Engineering rule", "Uluslararası lisans diploması ile Havacılık ve Uzay Mühendisliği başvurusu için GRE sonuç belgesi"),
        ],
        "motivation_letter_required": True,
        "cv_required": True,
        "recommendation_required": None,
        "test_required": True,
        "verification_notes": bi(
            "General MSc requirements, documents and the Aerospace-specific GRE rule are separately published by TU Delft. The programme-specific page is for the 2026/27 intake; check the next intake before applying.",
            "Genel yüksek lisans şartları, belgeler ve Havacılık ve Uzay Mühendisliğine özgü GRE kuralı TU Delft tarafından ayrı sayfalarda yayımlanır. Programa özgü sayfa 2026/27 alımına aittir; başvuru öncesinde sonraki alımı kontrol edin.",
        ),
    })
    row["cost_profile"].update({
        "academic_year": "2026/2027",
        "tuition_eur_per_year_min": 25633,
        "tuition_eur_per_year_max": 25633,
        "tuition_eur_per_year_estimated": None,
        "tuition_basis": "2026/27 institutional MSc rate for students who do not qualify for the statutory rate",
        "non_eu_flat_fee": 25633,
        "total_academic_cost_eur_per_year_estimated": 25633,
        "source_notes": bi(
            "TU Delft publishes an institutional MSc rate of EUR 25,633 for 2026/27. This is the published rate for students who do not qualify for the statutory rate; nationality and residence status determine which rate applies.",
            "TU Delft 2026/27 için 25.633 EUR kurumsal yüksek lisans ücreti yayımlar. Bu, kanuni ücrete uygun olmayan öğrenciler için yayımlanmış ücrettir; hangi oranın geçerli olduğunu uyruk ve ikamet statüsü belirler.",
        ),
        "verification_notes": bi(
            "Published 2026/27 institutional MSc tuition; it is not an estimate and does not include living costs.",
            "Yayımlanmış 2026/27 kurumsal yüksek lisans ücreti; tahmin değildir ve yaşam giderlerini içermez.",
        ),
    })
    row["scholarship_profile"].update({
        "regional_scholarship_available": True,
        "regional_scholarship_name": "Justus & Louise van Effen Excellence Scholarship",
        "merit_scholarships": [bi(
            "Justus & Louise van Effen Excellence Scholarship: two awards per faculty for excellent international applicants to regular two-year TU Delft MSc programmes; it covers full tuition and contributes to living expenses.",
            "Justus & Louise van Effen Excellence Bursu: normal iki yıllık TU Delft yüksek lisanslarına başvuran başarılı uluslararası adaylar için fakülte başına iki ödül; tam öğrenim ücretini karşılar ve yaşam giderlerine katkı sağlar.",
        )],
        "non_eu_eligible": True,
        "scholarship_deadline": "2025-12-01 (2026–2028 cycle; closed)",
        "scholarship_application_url": scholarship_url,
        "funding_competitiveness": "extremely_high",
        "funding_notes": bi(
            "The 2026–2028 Justus & Louise van Effen cycle has already been awarded. Its official page listed a 1 December 2025 deadline, two awards per faculty and an indicative top-10% academic standard. The next-cycle deadline is not yet verified, so do not infer it from the past cycle.",
            "2026–2028 Justus & Louise van Effen dönemi zaten sonuçlandırılmıştır. Resmî sayfa 1 Aralık 2025 son tarihini, fakülte başına iki ödülü ve gösterge niteliğinde ilk %10 başarı standardını yayımlamıştır. Sonraki dönemin son tarihi henüz doğrulanmadığından geçmiş dönemden çıkarım yapılmamalıdır.",
        ),
        "verification_notes": bi(
            "Eligibility and award scope are official; this record deliberately labels the published deadline as a closed past cycle.",
            "Uygunluk ve burs kapsamı resmîdir; bu kayıt yayımlanmış son tarihi bilinçli olarak kapanmış geçmiş dönem şeklinde etiketler.",
        ),
    })
    row["living_profile"].update({
        "monthly_living_cost_eur_min": 1000,
        "monthly_living_cost_eur_max": 1500,
        "monthly_living_cost_eur_estimated": None,
        "monthly_living_cost_basis": bi(
            "Study in NL's current Netherlands-wide student estimate: EUR 1,000–1,500 per month. It is a national planning range, not a Delft-specific quote.",
            "Study in NL'nin güncel Hollanda geneli öğrenci tahmini: ayda 1.000–1.500 EUR. Bu, Delft'e özgü bir fiyat değil, ulusal planlama aralığıdır.",
        ),
        "monthly_living_cost_scope_label": bi("Netherlands-wide average", "Hollanda geneli ortalama"),
        "average_room_rent_eur": None,
        "average_room_rent_eur_min": 450,
        "average_room_rent_eur_max": 1000,
        "average_room_rent_scope_label": bi("Netherlands-wide average, not Delft-specific", "Hollanda geneli ortalama, Delft'e özgü değil"),
        "student_housing_available": True,
        "student_housing_competitiveness": "high",
        "housing_difficulty": "high",
        "living_risk": "high",
        "housing_difficulty_score": None,
        "living_risk_score": None,
        "housing_notes": bi(
            "TU Delft says it is very difficult to find a room in Delft and nearby because of the student-room shortage, and strongly advises students not to travel without housing arranged. The displayed EUR 450–1,000 room range is the official Netherlands-wide average, not a Delft rent quote.",
            "TU Delft, öğrenci odası eksikliği nedeniyle Delft ve çevresinde oda bulmanın çok zor olduğunu belirtir ve konaklama ayarlanmadan seyahat edilmemesini güçlü biçimde tavsiye eder. Gösterilen 450–1.000 EUR oda aralığı Delft kirası değil, resmî Hollanda geneli ortalamadır.",
        ),
        "verification_notes": bi(
            "No current Delft-specific official rent was found. The card shows the national official range with its scope and keeps the Delft availability warning separate.",
            "Güncel, Delft'e özgü resmî kira tutarı bulunamadı. Kart ulusal resmî aralığı kapsam etiketiyle gösterir ve Delft'teki erişim uyarısını ayrı tutar.",
        ),
    })
    row["curriculum_profile"].update({
        "tracks": [
            "Aerodynamics & Wind Energy",
            "Aerospace Structures & Materials",
            "Control & Operations",
            "Flight Performance & Propulsion",
            "Space",
        ],
        "mandatory_courses": [
            "Core, profile and elective courses (60 ECTS)",
            "Interdisciplinarity block (15 ECTS)",
            "Master's thesis including integrated literature study (45 ECTS)",
        ],
        "thesis_required": True,
        "internship_required": None,
        "project_based_courses": [
            "Choice of approximately three-month company/institute internship, Joint Interdisciplinary Project, or Technology Venture Development",
        ],
        "curriculum_url": structure_url,
        "study_plan_url": tracks_url,
        "verification_notes": bi(
            "The official structure gives 60 ECTS of courses, a 15 ECTS interdisciplinarity block and a 45 ECTS thesis. Students choose one of five tracks; internship is an option rather than a universal requirement in the published structure.",
            "Resmî yapı 60 AKTS ders, 15 AKTS disiplinlerarasılık bloğu ve 45 AKTS tez içerir. Öğrenciler beş izden birini seçer; yayımlanan yapıda staj herkes için zorunlu değil, seçeneklerden biridir.",
        ),
    })
    row["research_profile"].update({
        "department_research_areas": [
            "Space Engineering",
            "Space Systems Engineering",
            "Planetary Exploration",
            "Spaceborne Instrumentation",
        ],
        "labs": [
            "Aerospace Engineering Cleanroom (space-systems hardware, CubeSat ACS testing)",
            "Cessna Citation II PH-LAB research aircraft",
        ],
        "research_centers": ["TU Delft Space Engineering"],
        "space_or_aerospace_projects": [
            "Delfi-C3 and Delfi-N3xt CubeSats were built and tested in the Aerospace Engineering Cleanroom.",
        ],
        "research_strength_summary": bi(
            "The programme offers a dedicated Space track. Official TU Delft research sources document Space Engineering groups and an aerospace cleanroom used to build and test Delft CubeSats; this is stronger evidence than a prestige-only claim.",
            "Programda ayrı bir Uzay izi bulunur. Resmî TU Delft araştırma kaynakları Uzay Mühendisliği gruplarını ve Delft CubeSat'lerinin üretim/testinde kullanılan havacılık temiz odasını belgeler; bu, yalnızca prestij iddiasından daha güçlü kanıttır.",
        ),
        "research_strength_score": None,
        "research_sources": [space_department_url, cleanroom_url, aircraft_url],
    })
    row["industry_ecosystem_profile"].update({
        "confirmed_partners": ["European Space Agency (programme page states an established relationship)", "Airbus (programme page states an established relationship)", "KLM (programme page states an established relationship)", "Schiphol Airport (programme page states an established relationship)"],
        "internship_possibility": "available",
        "thesis_with_industry_possibility": "available",
        "career_relevance": "strong",
        "ecosystem_strength_score": None,
        "ecosystem_notes": bi(
            "The official programme page states established relationships with Schiphol Airport, ESA, KLM, Airbus and other aerospace industries and research institutes. It also says students can pursue projects and internships globally; this is not a guarantee of an individual placement.",
            "Resmî program sayfası Schiphol Havalimanı, ESA, KLM, Airbus ve diğer havacılık endüstrileri/araştırma kurumlarıyla yerleşik ilişkiler bulunduğunu belirtir. Ayrıca öğrencilerin küresel proje ve staj olanaklarını kullanabileceğini söyler; bu, bireysel yerleştirme garantisi değildir.",
        ),
    })
    row["application_timeline_profile"].update({
        "academic_year": "2026/2027 (closed intake)",
        "intake_terms": ["September 2026 (closed)"],
        "non_eu_deadline": "2026-01-15 (23:59 CET; non-EU/EFTA with international BSc; closed)",
        "eu_deadline": "2026-04-01 (23:59 CEST; EU/EFTA with international BSc; closed)",
        "winter_deadline": "2026-01-15 (23:59 CET; non-EU/EFTA with international BSc; closed)",
        "application_deadline": "2026-01-15 (23:59 CET; non-EU/EFTA with international BSc; closed)",
        "visa_sensitive_deadline": "2026-07-01 request / 2026-07-11 payment for applicants without a valid Dutch residence permit (September start; closed)",
        "timeline_risk": "high",
        "deadline_notes": bi(
            "These are the official dates for the 2026/27 Aerospace intake and are explicitly marked closed. TU Delft has not yet published a next-intake Aerospace deadline on the checked page; applicants must not reuse these dates.",
            "Bunlar 2026/27 Havacılık ve Uzay Mühendisliği alımının resmî tarihleri olup açıkça kapanmış olarak işaretlenmiştir. Kontrol edilen sayfada sonraki alım için tarih yayımlanmamıştır; adaylar bu tarihleri yeniden kullanmamalıdır.",
        ),
    })
    row["student_sentiment_profile"] = {
        "student_satisfaction_score": None,
        "sentiment_confidence": "unknown",
        "sample_size_estimate": None,
        "date_range": "",
        "teaching_quality_sentiment": "unknown",
        "workload_sentiment": "unknown",
        "administration_sentiment": "unknown",
        "housing_sentiment": "unknown",
        "city_life_sentiment": "unknown",
        "international_student_sentiment": "unknown",
        "career_support_sentiment": "unknown",
        "positive_themes": [],
        "negative_themes": [],
        "recurring_complaints": [],
        "recurring_strengths": [],
        "student_sentiment_summary": bi(
            "No dated, adequately sampled student-review set has been verified for this record. The official housing warning is presented as an institutional risk, not as student sentiment.",
            "Bu kayıt için tarihli ve yeterli örneklem içeren öğrenci yorumu kümesi doğrulanmadı. Resmî konut uyarısı öğrenci duygusu olarak değil, kurumsal risk olarak sunulur.",
        ),
        "student_sentiment_sources": [],
        "verification_notes": bi(
            "Unverified Reddit search links and attributed quotations were removed rather than presented as reviews.",
            "Doğrulanmamış Reddit arama bağlantıları ve atfedilmiş alıntılar, yorum olarak sunulmak yerine kaldırıldı.",
        ),
    }
    row["decision_summary"].update({
        "best_for": [bi(
            "Students seeking a structured aerospace MSc with a dedicated Space track, 45 ECTS thesis and documented CubeSat/space-systems facilities.",
            "Ayrı Uzay izi, 45 AKTS tez ve belgelenmiş CubeSat/uzay sistemleri altyapısı olan yapılandırılmış bir havacılık ve uzay yüksek lisansı arayan öğrenciler.",
        )],
        "not_ideal_for": [bi(
            "Applicants who need a guaranteed room in Delft or must rely on an unverified future scholarship deadline.",
            "Delft'te garantili odaya ihtiyaç duyan veya doğrulanmamış gelecek burs son tarihine güvenmek zorunda olan adaylar.",
        )],
        "main_strengths": [bi(
            "Five technical tracks, including Space, with a 45 ECTS thesis and a documented aerospace cleanroom for spacecraft hardware work.",
            "Uzay dahil beş teknik iz, 45 AKTS tez ve uzay aracı donanımı çalışmaları için belgelenmiş havacılık temiz odası.",
        )],
        "main_risks": [
            bi("For an international BSc holder in the checked 2026/27 intake, the Aerospace GRE thresholds were strict; next-cycle rules must be rechecked.", "Kontrol edilen 2026/27 alımında uluslararası lisans diploması sahipleri için Havacılık ve Uzay Mühendisliği GRE eşikleri katıydı; sonraki dönem kuralları yeniden doğrulanmalıdır."),
            bi("TU Delft warns that finding a room in Delft and nearby is very difficult; the EUR rent range shown is only a Netherlands-wide average.", "TU Delft, Delft ve çevresinde oda bulmanın çok zor olduğu uyarısını yapar; gösterilen EUR kira aralığı yalnızca Hollanda geneli ortalamadır."),
        ],
        "application_reality": bi(
            "The published 2026/27 Aerospace and scholarship dates are closed. Keep this record for eligibility and planning, then verify the next intake before applying.",
            "Yayımlanan 2026/27 Havacılık ve Uzay Mühendisliği ve burs tarihleri kapanmıştır. Kaydı uygunluk ve planlama için kullanın; başvuru öncesinde sonraki alımı doğrulayın.",
        ),
        "overall_recommendation": bi(
            "A source-backed space/aerospace choice with unusually visible technical infrastructure, but affordability and housing need early, independent planning.",
            "Teknik altyapısı alışılmadık derecede görünür, kaynak destekli bir uzay/havacılık seçeneğidir; ancak bütçe ve konaklama erken ve bağımsız planlama gerektirir.",
        ),
    })

    profile = row.setdefault("source_profile", {})
    profile.update({
        "official_program_page": programme_url,
        "official_admission_page": programme_admission_url,
        "official_tuition_page": tuition_url,
        "official_scholarship_page": scholarship_url,
        "official_curriculum_page": structure_url,
        "official_department_page": space_department_url,
        "official_lab_pages": [cleanroom_url, aircraft_url],
        "official_housing_page": housing_url,
        "needs_verification": False,
    })
    profile.setdefault("field_confidence", {}).update({
        "program_basic_info": "high",
        "language": "high",
        "admission": "high",
        "tuition": "high",
        "scholarship": "high",
        "curriculum": "high",
        "housing": "high",
        "research": "high",
        "industry": "high",
        "deadlines": "high",
    })

    for entry in [
        source(programme_url, "TU Delft MSc Aerospace Engineering", "official_program_page", ["program", "language", "industry"], "Programme page confirms a full-time English MSc, 120 ECTS over 24 months, its Space track and stated relationships with ESA, Airbus, KLM and Schiphol Airport.", "Program sayfası tam zamanlı İngilizce yüksek lisansı, 24 ayda 120 AKTS'yi, Uzay izini ve ESA, Airbus, KLM ile Schiphol Havalimanı ile belirtilen ilişkileri doğrular."),
        source(programme_admission_url, "TU Delft Aerospace Engineering: Admission and application", "official_admission_page", ["admission", "deadline", "non_eu"], "Programme page publishes the 2026/27 international-BSc GRE thresholds and the closed 15 January 2026 non-EU/EFTA deadline.", "Program sayfası 2026/27 uluslararası lisans diploması GRE eşiklerini ve kapanmış 15 Ocak 2026 AB dışı/EFTA dışı son tarihini yayımlar."),
        source(general_admission_url, "TU Delft MSc International Diploma: Admission Requirements", "official_admission_page", ["admission", "language", "non_eu"], "Current page says all nationalities are welcome, requires a related research-university bachelor's degree with CGPA at least 75% unless a programme rule differs, and publishes English-test rules.", "Güncel sayfa tüm uyrukların başvurabileceğini, program kuralı farklı değilse ilgili araştırma üniversitesi lisans derecesi ve en az %75 genel not ortalaması gerektiğini, ayrıca İngilizce sınav kurallarını yayımlar."),
        source(documents_url, "TU Delft MSc International Diploma: Required Documents", "official_admission_page", ["admission"], "Current page lists diploma/degree statement, transcript, CV, motivation letter, identity proof and language certificate among the required-document workflow; programme-specific items can apply.", "Güncel sayfa gerekli belge sürecinde diploma/derece belgesi, transkript, özgeçmiş, motivasyon mektubu, kimlik belgesi ve dil sertifikasını listeler; programa özgü belgeler de istenebilir."),
        source(deadlines_url, "TU Delft MSc International Diploma: Dates and Deadlines", "official_admission_page", ["deadline"], "Current page lists the 2026 general MSc calendar and confirms 15 January 2026 for non-EU/EFTA Aerospace applicants with an international BSc, plus 1 April for EU/EFTA international-BSc applicants.", "Güncel sayfa 2026 genel yüksek lisans takvimini listeler; uluslararası lisans diplomasıyla Havacılık ve Uzay Mühendisliği başvuran AB dışı/EFTA dışı adaylar için 15 Ocak 2026'yı ve AB/EFTA adayları için 1 Nisan'ı doğrular."),
        source(tuition_url, "TU Delft Tuition Fee & Finances", "official_tuition_page", ["tuition"], "Current page publishes the 2026/27 institutional MSc rate of EUR 25,633 and explains statutory-rate eligibility.", "Güncel sayfa 2026/27 kurumsal yüksek lisans ücretini 25.633 EUR olarak yayımlar ve kanuni ücret uygunluğunu açıklar."),
        source(scholarship_url, "TU Delft Justus & Louise van Effen Excellence Scholarships", "official_scholarship_page", ["scholarship"], "Current page says the 2026–2028 awards have been made, and documents two awards per faculty, international eligibility, the 1 December 2025 past deadline, full tuition and a living-expense contribution.", "Güncel sayfa 2026–2028 ödüllerinin verildiğini belirtir; fakülte başına iki ödülü, uluslararası uygunluğu, geçmiş 1 Aralık 2025 son tarihini, tam öğrenim ücretini ve yaşam gideri katkısını belgeler."),
        source(structure_url, "TU Delft Aerospace Engineering: Programme Structure", "official_curriculum_page", ["curriculum"], "Current page documents 60 ECTS courses, a 15 ECTS interdisciplinarity block, a 45 ECTS thesis and the internship/JIP/venture-development options.", "Güncel sayfa 60 AKTS ders, 15 AKTS disiplinlerarasılık bloğu, 45 AKTS tez ve staj/JIP/girişim geliştirme seçeneklerini belgeler."),
        source(tracks_url, "TU Delft Aerospace Engineering: Master Tracks", "official_curriculum_page", ["curriculum"], "Current page lists the five tracks: Aerodynamics & Wind Energy, Aerospace Structures & Materials, Control & Operations, Flight Performance & Propulsion and Space.", "Güncel sayfa beş izi listeler: Aerodinamik ve Rüzgâr Enerjisi, Havacılık Yapıları ve Malzemeleri, Kontrol ve Operasyonlar, Uçuş Performansı ve İtki, Uzay."),
        source(housing_url, "TU Delft Housing for Incoming International Students", "official_housing_page", ["housing"], "Current page says finding a room in Delft and nearby is very difficult due to a shortage of student rooms and strongly advises against travel before housing is arranged.", "Güncel sayfa öğrenci odası eksikliği nedeniyle Delft ve çevresinde oda bulmanın çok zor olduğunu belirtir ve konaklama ayarlanmadan seyahat edilmemesini güçlü biçimde tavsiye eder."),
        source(cost_of_living_url, "Study in NL: Daily Student Expenses and Cost of Living", "official_cost_of_living_page", ["housing", "living"], "The official national information portal publishes a Netherlands-wide EUR 1,000–1,500 monthly student budget and EUR 450–1,000 monthly average room range; neither is Delft-specific.", "Resmî ulusal bilgi portalı Hollanda geneli öğrenci bütçesini ayda 1.000–1.500 EUR, ortalama oda aralığını ayda 450–1.000 EUR olarak yayımlar; ikisi de Delft'e özgü değildir."),
        source(space_department_url, "TU Delft Research Portal: Space Engineering", "official_department_page", ["research"], "TU Delft's research portal documents Space Engineering within Aerospace Engineering, including Space Systems Engineering, Planetary Exploration and Spaceborne Instrumentation groups.", "TU Delft araştırma portalı Havacılık ve Uzay Mühendisliği içinde Uzay Mühendisliğini; Uzay Sistemleri Mühendisliği, Gezegen Keşfi ve Uzay Tabanlı Enstrümantasyon gruplarıyla belgeler."),
        source(cleanroom_url, "TU Delft Research Portal: Aerospace Engineering Cleanroom", "official_lab_page", ["research"], "Official facility page says the cleanroom supports space-systems research and student training, includes nanosatellite ACS test equipment, and was used to build and test Delfi-C3 and Delfi-N3xt CubeSats.", "Resmî tesis sayfası temiz odanın uzay sistemleri araştırması ve öğrenci eğitimini desteklediğini, nanosatellit ACS test ekipmanı içerdiğini ve Delfi-C3 ile Delfi-N3xt CubeSat'lerinin burada üretim/testten geçtiğini belirtir."),
        source(aircraft_url, "TU Delft Research Portal: Cessna Citation II PH-LAB", "official_lab_page", ["research"], "Official facility page documents the jointly operated Cessna Citation II PH-LAB as an Aerospace Engineering research aircraft and airborne research platform.", "Resmî tesis sayfası ortak işletilen Cessna Citation II PH-LAB'i Havacılık ve Uzay Mühendisliği araştırma uçağı ve havadan araştırma platformu olarak belgeler."),
    ]:
        add_source(row, entry)

    newline = "\r\n" if "\r\n" in original else "\n"
    PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2).replace("\n", newline) + newline, encoding="utf-8")
    print("Updated TU Delft Aerospace with checked 2026/27 evidence.")


if __name__ == "__main__":
    main()
