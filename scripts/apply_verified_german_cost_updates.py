"""Apply source-checked cost updates for selected German aerospace records.

Zero means no general tuition during the normal study period; it never means
that studying or living in the city is free.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data_base" / "almanya.json"
CHECKED = "2026-07-14"


def bi(en: str, tr: str) -> dict[str, str]:
    return {"en": en, "tr": tr}


def src(url: str, title: str, kind: str, fields: list[str], en: str, tr: str, confidence: str = "high", access_status: str = "ok") -> dict[str, Any]:
    return {
        "url": url, "title": title, "source_type": kind,
        "access_status": access_status, "last_checked": CHECKED,
        "relevant_fields": fields, "confidence": confidence,
        "notes": bi(en, tr),
    }


def record(rows: list[dict[str, Any]], key: str) -> dict[str, Any]:
    return next(row for row in rows if row.get("id") == key)


def add_source(row: dict[str, Any], item: dict[str, Any]) -> None:
    profile = row.setdefault("source_profile", {})
    log = [entry for entry in profile.get("source_log", []) if isinstance(entry, dict)]
    log = [entry for entry in log if (entry.get("url"), entry.get("source_type")) != (item["url"], item["source_type"])]
    log.append(item)
    profile["source_log"] = log
    profile["last_verified"] = CHECKED


def confidence(row: dict[str, Any], **values: str) -> None:
    row.setdefault("source_profile", {}).setdefault("field_confidence", {}).update(values)


def main() -> None:
    original = PATH.read_text(encoding="utf-8")
    rows = json.loads(original)

    stuttgart = record(rows, "germany-stuttgart-msc-aerospace")
    stuttgart["cost_profile"].update({
        "academic_year": "current official pages checked 2026-07-14",
        "tuition_eur_per_year_min": 3000,
        "tuition_eur_per_year_max": 3000,
        "tuition_eur_per_year_estimated": 3000,
        "tuition_basis": "1500_eur_per_semester_non_eu_consecutive_master",
        "student_contribution_eur": 184,
        "cost_notes": bi(
            "Non-EU/EEA students in a consecutive Master's normally pay EUR 1,500 tuition plus the currently published EUR 184 semester fee. Statutory exemptions apply.",
            "Ardışık yüksek lisanslardaki AB/AEA dışı öğrenciler normalde dönem başına 1.500 EUR öğrenim ücreti ve yayımlanan 184 EUR dönem harcı öder. Kanuni muafiyetler uygulanabilir.",
        ),
    })
    stuttgart["living_profile"].update({
        "average_room_rent_eur_min": 350,
        "average_room_rent_eur_max": 600,
        "monthly_living_cost_eur_min": 992,
        "monthly_living_cost_eur_max": None,
        "monthly_living_cost_basis": bi(
            "University of Stuttgart says students need at least EUR 992 per month for living costs; its shared-flat room range excludes electricity, water and heating.",
            "Stuttgart Üniversitesi yaşam giderleri için ayda en az 992 EUR gerektiğini; paylaşımlı ev oda aralığının elektrik, su ve ısıtmayı içermediğini belirtir.",
        ),
        "housing_notes": bi(
            "Published shared-flat room guide: EUR 350–600 per month, plus electricity, water and heating. It is a planning range, not a room offer.",
            "Yayımlanan paylaşımlı ev oda rehberi: ayda 350–600 EUR; elektrik, su ve ısıtma hariçtir. Bu bir planlama aralığıdır, oda teklifi değildir.",
        ),
        "living_risk": "high",
        "housing_difficulty": None,
    })
    stuttgart["scholarship_profile"].update({
        "funding_notes": bi(
            "The University identifies DAAD as the principal scholarship provider for international degree students, warns that schemes and coverage vary, and says DAAD scholarships do not cover the EUR 1,500 non-EU tuition fee. This is not an eligibility guarantee.",
            "Üniversite, uluslararası tam derece öğrencileri için başlıca burs sağlayıcısı olarak DAAD'ı gösterir; program koşullarının ve kapsamının değiştiğini, DAAD burslarının 1.500 EUR'luk AB dışı öğrenim ücretini karşılamadığını belirtir. Bu uygunluk garantisi değildir.",
        ),
        "regional_scholarship_available": None,
        "non_eu_eligible": None,
    })
    stuttgart_tuition = "https://www.student.uni-stuttgart.de/en/organizing-studies/formalities/tuition-and-fees/tuition-fee/"
    stuttgart_finance = "https://www.uni-stuttgart.de/en/study/new-in-stuttgart/finances/international/"
    add_source(stuttgart, src(stuttgart_tuition, "University of Stuttgart: Tuition Fees for International Students", "official_tuition_page", ["tuition", "fees"], "Current page states EUR 1,500 tuition per semester for non-EU/EEA students in consecutive Master's programmes and a EUR 184 regular semester fee.", "Güncel sayfa, ardışık yüksek lisanslardaki AB/AEA dışı öğrenciler için dönem başına 1.500 EUR öğrenim ücreti ve 184 EUR normal dönem harcı belirtir."))
    add_source(stuttgart, src(stuttgart_finance, "University of Stuttgart: International Student Finances", "official_cost_of_living_page", ["housing", "living"], "Current university guide gives at least EUR 992 monthly living costs and a EUR 350–600 shared-flat room range excluding utilities.", "Güncel üniversite rehberi, ayda en az 992 EUR yaşam gideri ve faturalar hariç 350–600 EUR paylaşımlı ev oda aralığı verir."))
    add_source(stuttgart, src(stuttgart_finance, "University of Stuttgart: International Student Funding Information", "official_scholarship_page", ["scholarship", "funding"], "University guidance identifies DAAD as the principal provider, warns that conditions vary, and says DAAD scholarships do not cover the non-EU tuition fee.", "Üniversite rehberi DAAD'ı başlıca sağlayıcı olarak tanımlar, koşulların değiştiğini uyarır ve DAAD burslarının AB dışı öğrenim ücretini karşılamadığını söyler.", "medium"))
    confidence(stuttgart, tuition="high", housing="high", scholarship="medium")

    kit = record(rows, "germany-kit-msc-aerospace")
    kit["cost_profile"].update({
        "academic_year": "current official page checked 2026-07-14",
        "tuition_eur_per_year_min": 3000,
        "tuition_eur_per_year_max": 3000,
        "tuition_eur_per_year_estimated": 3000,
        "tuition_basis": "1500_eur_per_semester_non_eu_not_equal_status",
        "student_contribution_eur": 184,
        "cost_notes": bi(
            "KIT states that non-EU citizens who are not treated as equal to German students pay EUR 1,500 tuition per semester in Baden-Württemberg. Its listed Studierendenwerk, administration and student-union contributions total EUR 184 per semester. Exemptions/equal-status rules apply.",
            "KIT, Alman öğrencilerle eşdeğer sayılmayan AB dışı vatandaşların Baden-Württemberg'de dönem başına 1.500 EUR öğrenim ücreti ödediğini belirtir. Listelenen Studierendenwerk, idare ve öğrenci birliği katkılarının toplamı dönem başına 184 EUR'dur. Muafiyet ve eşdeğer statü kuralları geçerlidir.",
        ),
    })
    add_source(kit, src("https://www.studienstart.kit.edu/english/financing-part-time-job.php", "KIT: Financing and Part-time Job", "official_tuition_page", ["tuition", "fees"], "Current KIT page lists EUR 1,500 per semester for non-EU students not of equal status, plus EUR 92 student services, EUR 80 administration and EUR 12 student-union contributions.", "Güncel KIT sayfası, eşdeğer statüsü olmayan AB dışı öğrenciler için dönem başına 1.500 EUR ile 92 EUR öğrenci hizmeti, 80 EUR idare ve 12 EUR öğrenci birliği katkısı listeler."))
    kit["scholarship_profile"].update({
        "regional_scholarship_available": True,
        "regional_scholarship_name": "Deutschlandstipendium at KIT",
        "merit_scholarships": [bi(
            "Deutschlandstipendium at KIT: EUR 300 per month for one year. It is open to students and prospective students of all nationalities; awards consider academic performance alongside commitment and personal circumstances.",
            "KIT Deutschlandstipendium: bir yıl boyunca ayda 300 EUR. Tüm uyruklardan öğrencilere ve aday öğrencilere açıktır; akademik başarı yanında sosyal katkı ve kişisel koşullar da değerlendirilir.",
        )],
        "non_eu_eligible": True,
        "scholarship_deadline": "2027-04-12 to 2027-04-29 (published next application period)",
        "scholarship_application_url": "https://www.careerservice.kit.edu/en/studierende/foerderprogramme/deutschlandstipendium/",
        "funding_competitiveness": "high",
        "funding_notes": bi(
            "KIT publishes EUR 300 per month for one year. The published next application window is 12–29 April 2027. Applicants may be prospective students, but must be enrolled at KIT and have a German bank account when payment starts; this is competitive funding, not a tuition waiver.",
            "KIT, bir yıl için ayda 300 EUR yayımlar. Yayımlanmış sonraki başvuru dönemi 12–29 Nisan 2027'dir. Aday öğrenciler başvurabilir; ancak ödeme başladığında KIT'e kayıtlı ve Alman banka hesabına sahip olmalıdır. Bu rekabetçi bir destektir, öğrenim ücreti muafiyeti değildir.",
        ),
    })
    kit["living_profile"].update({
        "monthly_living_cost_eur_min": 800,
        "monthly_living_cost_eur_max": 900,
        "monthly_living_cost_eur_estimated": None,
        "monthly_living_cost_basis": bi(
            "KIT's current guide puts average student expenses in Karlsruhe, including fees and depending on personal situation, at EUR 800–900 per month.",
            "KIT'in güncel rehberi, Karlsruhe'de öğrenci giderlerini ücretler dahil ve kişisel duruma bağlı olarak ayda 800–900 EUR olarak verir.",
        ),
        "student_housing_available": True,
        "student_housing_competitiveness": "high",
        "housing_difficulty": "high",
        "living_risk": "medium",
        "housing_notes": bi(
            "KIT says Studierendenwerk rooms are regularly fully booked, especially near the semester start, and recommends applying as early as possible; applications can be submitted up to six months before the desired move-in date. No KIT-published room-rent figure is claimed here.",
            "KIT, özellikle dönem başlangıcında Studierendenwerk odalarının düzenli olarak tamamen dolduğunu ve mümkün olan en erken zamanda başvuru yapılmasını önerir; istenen taşınma tarihinden altı ay öncesine kadar başvuru yapılabilir. Burada KIT tarafından yayımlanmış bir oda kira tutarı iddia edilmez.",
        ),
        "verification_notes": bi(
            "The official monthly range is Karlsruhe-wide student expenditure, not a guaranteed personal cost or an accommodation offer.",
            "Resmî aylık aralık Karlsruhe geneli öğrenci harcamasıdır; kişisel maliyet ya da konaklama teklifi garantisi değildir.",
        ),
    })
    kit["application_timeline_profile"].update({
        "academic_year": "current programme page checked 2026-07-14",
        "intake_terms": ["winter term", "summer term"],
        "non_eu_deadline": "15 July (winter term) / 15 January (summer term; first semester)",
        "eu_deadline": "15 July (winter term) / 15 January (summer term; first semester)",
        "winter_deadline": "15 July (winter term; first semester)",
        "application_deadline": "15 July (winter term) / 15 January (summer term; first semester)",
        "timeline_risk": "medium",
        "deadline_notes": bi(
            "The checked KIT Electrical Engineering and Information Technology MSc page publishes the same first-semester deadlines for German/EU and non-EU applicants. It also confirms winter and summer starts; recheck the live page for a dated future cycle.",
            "Kontrol edilen KIT Elektrik ve Bilgi Teknolojileri yüksek lisans sayfası, Alman/AB ve AB dışı adaylar için ilk dönem aynı son tarihleri yayımlar. Ayrıca kış ve yaz başlangıçlarını doğrular; tarihli gelecek dönem için canlı sayfayı yeniden kontrol edin.",
        ),
    })
    kit_profile = kit.setdefault("source_profile", {})
    kit_profile.update({
        "official_admission_page": "https://www.sle.kit.edu/english/vorstudium/master-electrical-engineering-information-technology.php",
        "official_scholarship_page": "https://www.careerservice.kit.edu/en/studierende/foerderprogramme/deutschlandstipendium/",
        "official_housing_page": "https://www.kit.edu/study/living-in-karlsruhe.php",
        "needs_verification": False,
    })
    add_source(kit, src("https://www.sle.kit.edu/english/vorstudium/master-electrical-engineering-information-technology.php", "KIT Electrical Engineering and Information Technology M.Sc.", "official_admission_page", ["admission", "language", "deadline", "non_eu"], "Current programme page confirms a 120-ECTS English MSc, winter and summer first-semester entry, and the published 15 July/15 January deadlines for both German/EU and non-EU applicants.", "Güncel program sayfası 120 AKTS İngilizce yüksek lisansı, kış/yaz ilk dönem başlangıcını ve Alman/AB ile AB dışı adaylar için yayımlanmış 15 Temmuz/15 Ocak son tarihlerini doğrular."))
    add_source(kit, src("https://www.careerservice.kit.edu/en/studierende/foerderprogramme/deutschlandstipendium/", "KIT Deutschlandstipendium", "official_scholarship_page", ["scholarship", "funding"], "Current KIT page publishes EUR 300 monthly for one year, all-nationality eligibility for students and prospective students, and the 12–29 April 2027 next application period.", "Güncel KIT sayfası bir yıl için aylık 300 EUR'u, öğrenci ve aday öğrenciler için tüm uyruklara açık uygunluğu ve 12–29 Nisan 2027 sonraki başvuru dönemini yayımlar."))
    add_source(kit, src("https://www.studienstart.kit.edu/english/financing-part-time-job.php", "KIT Karlsruhe Student Living Costs", "official_cost_of_living_page", ["housing", "living"], "Current KIT guide gives average Karlsruhe student expenses of EUR 800–900 per month including fees, depending on personal circumstances.", "Güncel KIT rehberi, kişisel koşullara bağlı olarak ücretler dahil Karlsruhe öğrenci giderlerini ayda 800–900 EUR olarak verir."))
    add_source(kit, src("https://www.kit.edu/study/living-in-karlsruhe.php", "KIT Living in Karlsruhe", "official_housing_page", ["housing"], "Current KIT page says student-residence rooms are regularly fully booked, especially at semester start, and can be applied for up to six months ahead.", "Güncel KIT sayfası, özellikle dönem başlangıcında öğrenci yurdu odalarının düzenli olarak tamamen dolduğunu ve altı ay önceden başvuru yapılabildiğini belirtir."))
    confidence(kit, tuition="high", scholarship="high", housing="high", deadlines="high")

    braunschweig = record(rows, "germany-braunschweig-msc-aerospace")
    braunschweig["cost_profile"].update({
        "academic_year": "winter semester 2026/27",
        "tuition_eur_per_year_min": 0,
        "tuition_eur_per_year_max": 0,
        "tuition_eur_per_year_estimated": 0,
        "tuition_basis": "no_regular_tuition_within_standard_period",
        "student_contribution_eur": 472.50,
        "cost_notes": bi(
            "TU Braunschweig says its general tuition was abolished. The published EUR 472.50 is the winter 2026/27 semester contribution, not tuition. Long-term, continuing-education and special-case fees can still apply.",
            "TU Braunschweig genel öğrenim ücretinin kaldırıldığını belirtir. Yayımlanan 472,50 EUR, 2026/27 kış dönemi dönem katkısıdır; öğrenim ücreti değildir. Uzun süreli eğitim, sürekli eğitim ve özel durum ücretleri yine uygulanabilir.",
        ),
    })
    add_source(braunschweig, src("https://www.tu-braunschweig.de/en/study-teaching/during-your-studies/financing-and-costs", "TU Braunschweig: Financing and Costs", "official_tuition_page", ["tuition", "fees"], "Current page states general tuition was abolished and publishes a EUR 472.50 semester contribution for winter 2026/27, with separate long-term and special-programme fees.", "Güncel sayfa genel öğrenim ücretinin kaldırıldığını, 2026/27 kışı için 472,50 EUR dönem katkısını ve ayrı uzun süreli/özel program ücretlerini yayımlar."))
    braunschweig["eligibility_profile"].update({
        "eligible_for_non_eu": True,
        "verification_notes": bi(
            "The current application selector publishes a graduate-programme route for non-EU applicants with a foreign qualification. Aerospace Engineering is a German-taught, admission-free MSc with special admission requirements; applicants must still satisfy the programme regulations.",
            "Güncel başvuru seçicisi, yabancı diplomalı AB dışı adaylar için yüksek lisans başvuru yolunu yayımlar. Havacılık ve Uzay Mühendisliği Almanca yürütülen, özel kabul şartları olan ancak kontenjan kısıtlaması bulunmayan bir yüksek lisanstır; adayların yine de program yönetmeliğini karşılaması gerekir.",
        ),
    })
    braunschweig["scholarship_profile"].update({
        "regional_scholarship_available": True,
        "regional_scholarship_name": "Deutschlandstipendium at TU Braunschweig",
        "merit_scholarships": [bi(
            "Deutschlandstipendium at TU Braunschweig: EUR 300 per month for two semesters. International students are explicitly encouraged to apply; academic performance, engagement and personal circumstances are considered.",
            "TU Braunschweig Deutschlandstipendium: iki dönem boyunca ayda 300 EUR. Uluslararası öğrenciler açıkça başvurmaya teşvik edilir; akademik başarı, sosyal katkı ve kişisel koşullar değerlendirilir.",
        )],
        "non_eu_eligible": True,
        "scholarship_deadline": "June 1–30 annually (2026/27 window closed)",
        "scholarship_application_url": "https://www.tu-braunschweig.de/en/stipendien/deutschlandstipendien/bewerbung?lang=en",
        "funding_competitiveness": "high",
        "funding_notes": bi(
            "The official 2026/27 call offered EUR 300 per month for two semesters and closed on 30 June 2026. The university says the application phase takes place from 1–30 June each year, but individual award availability is not guaranteed for every programme.",
            "Resmî 2026/27 çağrısı iki dönem için ayda 300 EUR sundu ve 30 Haziran 2026'da kapandı. Üniversite başvuru döneminin her yıl 1–30 Haziran olduğunu belirtir; ancak her program için bireysel burs verileceği garanti edilmez.",
        ),
    })
    braunschweig["living_profile"].update({
        "city_cost_level": "medium",
        "monthly_living_cost_eur_min": 992,
        "monthly_living_cost_eur_max": 1135,
        "monthly_living_cost_eur_estimated": None,
        "monthly_living_cost_basis": bi(
            "TU Braunschweig says students need at least about EUR 992 monthly and publishes a current itemised planning total of EUR 1,135 per month. The amount varies with lifestyle and is separate from the semester fee.",
            "TU Braunschweig öğrencilerin ayda en az yaklaşık 992 EUR'a ihtiyacı olduğunu ve güncel kalemli planlama toplamını ayda 1.135 EUR olarak yayımlar. Tutar yaşam tarzına göre değişir ve dönem katkısından ayrıdır.",
        ),
        "average_room_rent_eur": None,
        "average_room_rent_eur_min": 300,
        "average_room_rent_eur_max": 500,
        "student_housing_available": True,
        "student_housing_competitiveness": "high",
        "housing_difficulty": "high",
        "living_risk": "medium",
        "housing_sentiment": None,
        "housing_notes": bi(
            "TU Braunschweig says it cannot provide accommodation. Its international-student housing page describes the market as very competitive at semester start, advises allowing four to six months for the search and gives a EUR 300–500 monthly shared-flat room range.",
            "TU Braunschweig konaklama sağlayamadığını belirtir. Uluslararası öğrenci konut sayfası dönem başlangıcında piyasanın çok rekabetçi olduğunu, arama için dört ila altı ay ayrılmasını önerir ve paylaşımlı ev odaları için ayda 300–500 EUR aralığı verir.",
        ),
        "verification_notes": bi(
            "The rent range is for a shared-flat room in Braunschweig, not a room offer or a university accommodation guarantee.",
            "Kira aralığı Braunschweig'de paylaşımlı ev odası içindir; oda teklifi ya da üniversite konaklama garantisi değildir.",
        ),
    })
    braunschweig["application_timeline_profile"].update({
        "academic_year": "current application rules checked 2026-07-14",
        "intake_terms": ["winter semester", "summer semester"],
        "non_eu_deadline": "June 1–July 15 (winter) / December 1–January 15 (summer; foreign qualification, non-EU graduate route)",
        "eu_deadline": "June 1–July 15 (winter) / December 1–January 15 (summer; graduate route)",
        "winter_deadline": "June 1–July 15 (graduate route)",
        "summer_deadline": "December 1–January 15 (graduate route)",
        "application_deadline": "June 1–July 15 (winter) / December 1–January 15 (summer; graduate route)",
        "timeline_risk": "medium",
        "deadline_notes": bi(
            "TU Braunschweig's current application selector publishes these dates for the graduate-programme route. The Aerospace programme is German-taught and not one of the English/bilingual international programmes to which the selector assigns special earlier deadlines; verify the live selector before applying.",
            "TU Braunschweig'in güncel başvuru seçicisi bu tarihleri yüksek lisans başvuru yolu için yayımlar. Havacılık ve Uzay Mühendisliği Almanca yürütülür ve seçicinin daha erken özel tarih atadığı İngilizce/çift dilli uluslararası programlardan değildir; başvuru öncesi canlı seçiciyi doğrulayın.",
        ),
    })
    braunschweig["decision_summary"].update({
        "main_strengths": [bi(
            "A German-taught aerospace MSc in the Campus Research Airport cluster, with official programme links to DLR and regional aeronautics research; it has a 13-CP research project and a six-month thesis.",
            "Campus Research Airport kümelenmesinde, DLR ve bölgesel havacılık araştırmalarına resmî program bağlantıları olan Almanca yürütülen bir havacılık ve uzay yüksek lisansıdır; 13 KP araştırma projesi ve altı aylık tez içerir.",
        )],
        "main_risks": [bi(
            "German is the language of instruction. Housing is not provided by the university and the official guidance advises a four- to six-month search.",
            "Eğitim dili Almancadır. Üniversite konaklama sağlamaz ve resmî rehber dört ila altı aylık arama süresi önerir.",
        )],
    })
    braunschweig_profile = braunschweig.setdefault("source_profile", {})
    braunschweig_profile.update({
        "official_admission_page": "https://www.tu-braunschweig.de/en/application",
        "official_scholarship_page": "https://www.tu-braunschweig.de/en/stipendien/deutschlandstipendien/bewerbung?lang=en",
        "official_housing_page": "https://www.tu-braunschweig.de/en/international-student-support/housing",
        "needs_verification": False,
    })
    add_source(braunschweig, src("https://www.tu-braunschweig.de/en/application", "TU Braunschweig Application Deadlines and Online Application", "official_admission_page", ["admission", "deadline", "non_eu"], "Current application selector gives the graduate-programme deadlines of 1 June–15 July for winter and 1 December–15 January for summer, including the foreign-qualification non-EU route. It distinguishes earlier deadlines for English/bilingual international Master's programmes.", "Güncel başvuru seçicisi, yabancı diplomalı AB dışı yol dahil yüksek lisans başvuru tarihlerini kış için 1 Haziran–15 Temmuz, yaz için 1 Aralık–15 Ocak olarak verir. İngilizce/çift dilli uluslararası yüksek lisanslar için daha erken tarihleri ayırır."))
    add_source(braunschweig, src("https://www.tu-braunschweig.de/en/stipendien/deutschlandstipendien/bewerbung?lang=en", "TU Braunschweig Deutschlandstipendium Application", "official_scholarship_page", ["scholarship", "funding"], "Current English page documents EUR 300 per month for two semesters in 2026/27, the closed 1–30 June 2026 window, annual June application timing and explicit encouragement for international students.", "Güncel İngilizce sayfa 2026/27 için iki dönem boyunca ayda 300 EUR'u, kapanmış 1–30 Haziran 2026 dönemini, yıllık Haziran başvuru zamanlamasını ve uluslararası öğrencilerin açıkça teşvik edildiğini belgeler."))
    add_source(braunschweig, src("https://www.tu-braunschweig.de/en/international-students/preparation", "TU Braunschweig: Before Admission for International Students", "official_cost_of_living_page", ["housing", "living"], "Current university page publishes a EUR 992 monthly minimum and an itemised EUR 1,135 monthly living-cost total for Braunschweig, plus a separate approximate semester fee.", "Güncel üniversite sayfası Braunschweig için 992 EUR aylık asgari tutarını ve kalemli 1.135 EUR aylık yaşam maliyeti toplamını, ayrıca ayrı yaklaşık dönem katkısını yayımlar."))
    add_source(braunschweig, src("https://www.tu-braunschweig.de/en/international-student-support/housing", "TU Braunschweig Housing for International Students", "official_housing_page", ["housing"], "Current page says TU Braunschweig cannot provide accommodation, calls the start-of-semester market very competitive, advises a four- to six-month search and gives a EUR 300–500 shared-flat room range.", "Güncel sayfa TU Braunschweig'in konaklama sağlayamadığını, dönem başlangıcı piyasasının çok rekabetçi olduğunu, dört ila altı aylık arama önerdiğini ve paylaşımlı ev odası için 300–500 EUR aralığını verir."))
    confidence(braunschweig, tuition="high", scholarship="high", housing="high", deadlines="high", admission="high", curriculum="high")

    tuhh = record(rows, "de_tuhh_aeronautics_msc")
    tuhh["cost_profile"].update({
        "academic_year": "summer semester 2026 fee; tuition policy checked 2026-07-14",
        "tuition_eur_per_year_min": 0,
        "tuition_eur_per_year_max": 0,
        "tuition_eur_per_year_estimated": 0,
        "tuition_basis": "no_general_tuition_regular_programme",
        "student_contribution_eur": 384,
        "cost_notes": bi(
            "TU Hamburg says it does not generally charge tuition. EUR 384 is the published summer-semester 2026 contribution, including the public-transport semester ticket; it is not an annual price and later terms may differ.",
            "TU Hamburg genel olarak öğrenim ücreti almadığını belirtir. 384 EUR, toplu taşıma dönem biletini içeren yayımlanmış 2026 yaz dönemi katkısıdır; yıllık fiyat değildir ve sonraki dönemler farklı olabilir.",
        ),
    })
    tuhh["scholarship_profile"].update({
        "funding_notes": bi(
            "TU Hamburg's funding page links international students to DAAD scholarships and other schemes. The page does not establish an award, amount or eligibility for an individual Aeronautics applicant.",
            "TU Hamburg'un finansman sayfası uluslararası öğrencileri DAAD burslarına ve diğer programlara yönlendirir. Sayfa, tek tek Aeronautics adayları için ödül, tutar veya uygunluk kanıtlamaz.",
        ),
        "regional_scholarship_available": None,
        "non_eu_eligible": None,
    })
    tuhh["application_timeline_profile"].update({
        "academic_year": "annual application periods published on the current programme page",
        "intake_terms": ["winter", "summer"],
        "non_eu_deadline": "July 15 (winter) / January 15 (summer; annual periods)",
        "application_deadline": "July 15 (winter) / January 15 (summer; annual periods)",
        "timeline_risk": "medium",
        "deadline_notes": bi(
            "TU Hamburg's current Aeronautics page publishes 1 June–15 July for winter entry and 1 December–15 January for summer entry. These are recurring period labels rather than a dated future-cycle guarantee; check the page before applying.",
            "TU Hamburg'un güncel Aeronautics sayfası kış başlangıcı için 1 Haziran–15 Temmuz, yaz başlangıcı için 1 Aralık–15 Ocak tarihlerini yayımlar. Bunlar tarihli gelecek dönem garantisi değil, yinelenen dönem etiketleridir; başvurmadan önce sayfayı kontrol edin.",
        ),
    })
    tuhh["living_profile"].update({
        "monthly_living_cost_eur_min": 950,
        "monthly_living_cost_eur_max": None,
        "housing_difficulty": "high",
        "living_risk": "high",
        "monthly_living_cost_basis": bi(
            "TU Hamburg's 2026 international-Master's guide advises at least EUR 950 per month including accommodation, health insurance and study material.",
            "TU Hamburg'un 2026 uluslararası yüksek lisans rehberi; konaklama, sağlık sigortası ve eğitim materyali dahil ayda en az 950 EUR önerir.",
        ),
        "housing_notes": bi(
            "TU Hamburg states that enrolment does not provide accommodation and that the student-housing situation is extremely difficult because inexpensive accommodation is hard to find.",
            "TU Hamburg, kayıtla birlikte konaklama verilmediğini ve uygun fiyatlı konaklama bulmanın zor olması nedeniyle öğrenci konaklama durumunun son derece zor olduğunu belirtir.",
        ),
    })
    tuhh_finance = "https://www.tuhh.de/tuhh/en/education/students/organisational-details-about-your-studies/financing-your-studies"
    add_source(tuhh, src(tuhh_finance, "TU Hamburg: Financing Your Studies", "official_tuition_page", ["tuition", "fees"], "Current TU Hamburg page says it does not generally demand tuition fees and links to programme pages for exceptions.", "Güncel TU Hamburg sayfası genel olarak öğrenim ücreti talep etmediğini ve istisnalar için program sayfalarına bakılması gerektiğini belirtir.", "medium"))
    add_source(tuhh, src("https://www.tuhh.de/tuhh/en/education/students/organisational-details-about-your-studies/financing-your-studies/costs/semester-contribution", "TU Hamburg: Semester Contribution for Summer Semester 2026", "official_tuition_page", ["fees"], "Current page itemises and totals the summer-semester 2026 contribution at EUR 384.", "Güncel sayfa 2026 yaz dönemi katkısını kalem kalem verip toplam 384 EUR olarak belirtir."))
    add_source(tuhh, src(tuhh_finance, "TU Hamburg: Scholarship Information", "official_scholarship_page", ["scholarship", "funding"], "Current university page lists scholarship information including DAAD for international students, without promising eligibility or an award.", "Güncel üniversite sayfası, uluslararası öğrenciler için DAAD dahil burs bilgilerini listeler; uygunluk veya ödül garantisi vermez.", "medium"))
    add_source(tuhh, src("https://www.tuhh.de/tuhh/en/studying/before-studying/degree-courses/masters-programs/aeronautics", "TU Hamburg: Aeronautics M.Sc.", "official_admission_page", ["admission", "language", "deadline"], "Current programme page gives the winter and summer application periods and B2.2 German requirement.", "Güncel program sayfası kış ve yaz başvuru dönemlerini ve B2.2 Almanca şartını verir."))
    add_source(tuhh, src("https://www.tuhh.de/t3resources/tuhh/download/studium/studieninteressierte/How-to-apply-at-TUHH-general-2026.pdf", "TU Hamburg: How to Apply for International Master's Programs 2026", "official_cost_of_living_page", ["housing", "living"], "The 2026 university guide gives a EUR 950 monthly minimum including accommodation, health insurance and study material, and warns that cheap accommodation is extremely difficult to find.", "2026 üniversite rehberi, konaklama, sağlık sigortası ve eğitim materyali dahil aylık 950 EUR asgari tutar verir ve uygun fiyatlı konaklama bulmanın son derece zor olduğu uyarısını yapar.", "high", "pdf"))
    confidence(tuhh, tuition="medium", scholarship="medium", housing="high", deadlines="high")

    match = re.search(r"^\s*\[\r?\n( +)\{", original)
    indent = len(match.group(1)) if match else 2
    newline = "\r\n" if "\r\n" in original else "\n"
    PATH.write_text(json.dumps(rows, ensure_ascii=False, indent=indent).replace("\n", newline) + newline, encoding="utf-8")
    print("Updated verified German cost, living and funding records.")


if __name__ == "__main__":
    main()
