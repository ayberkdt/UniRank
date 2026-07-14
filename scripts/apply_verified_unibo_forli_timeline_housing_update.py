"""Add checked Bologna Aerospace dates and honest Forlì housing information."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from apply_verified_polimi_aero_update import bi, source


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data_base" / "italy.json"
CHECKED = "2026-07-14"


def main() -> None:
    original = PATH.read_text(encoding="utf-8")
    document: dict[str, Any] = json.loads(original)
    row = next(item for item in document["universities"] if item.get("id") == "unibo_aerospace_forli")

    programme_url = "https://www.unibo.it/en/study/second-cycle-degree/programme/2026/6704"
    admission_url = "https://corsi.unibo.it/2cycle/AerospaceEngineering/how-to-enrol"
    call_url = "https://corsi.unibo.it/s/3427/p/en/programma-enrolment-new/bando-lm-aerospace_ita_2025-26-def-1.pdf/%40%40download/file/Bando%2520LM%2520MES%252026-27_ENG.pdf"
    housing_url = "https://www.unibo.it/en/study/life-at-university-and-in-the-city/housing-and-residences/housing?scope=Current"

    row["living_profile"] = {
        "city_cost_level": "unknown",
        "monthly_living_cost_eur_min": None,
        "monthly_living_cost_eur_max": None,
        "monthly_living_cost_eur_estimated": None,
        "average_room_rent_eur": None,
        "average_room_rent_eur_min": None,
        "average_room_rent_eur_max": None,
        "student_housing_available": True,
        "student_housing_competitiveness": "unknown",
        "housing_difficulty": "unknown",
        "living_risk": "high",
        "housing_sentiment": None,
        "housing_notes": bi("Forlì has two ER.GO residence options identified by the University: Sassi Masini in the city centre (120 beds) and Ex-ENAV near the Engineering campus (64 beds, including eight accessible beds). Places require an ER.GO application and are not guaranteed. The University also points students to a checked Accommodation Showcase and local search services. No current official Forlì rent range was found, so the card does not substitute a Bologna price.", "Üniversitenin belirttiği üzere Forlì'de iki ER.GO yurt seçeneği vardır: şehir merkezindeki Sassi Masini (120 yatak) ve Mühendislik kampüsü yakınındaki Ex-ENAV (sekizi erişilebilir olmak üzere 64 yatak). Yerler ER.GO başvurusu gerektirir ve garantili değildir. Üniversite ayrıca kontrol edilen Accommodation Showcase'e ve yerel arama hizmetlerine yönlendirir. Güncel resmî Forlì kira aralığı bulunmadığı için kart Bologna fiyatı yerine bunu koymaz."),
        "verification_notes": bi("Housing availability and services are official, but no official Forlì room-rent or all-in monthly budget was located. Keeping the price null is intentional rather than an omission filled with a city-level estimate.", "Konaklama uygunluğu ve hizmetleri resmîdir; ancak resmî Forlì oda kirası veya tüm kalemleri içeren aylık bütçe bulunamadı. Fiyatın null tutulması kasıtlıdır; şehir düzeyi tahminle doldurulmaz."),
    }
    row["application_timeline_profile"] = {
        "academic_year": "2026/2027 published restricted-access cycle",
        "intake_terms": ["autumn 2026"],
        "application_rounds": ["Intake I, non-EU citizens residing abroad: 11 December 2025–27 January 2026 13:00 CET; remote interviews 16–19 February; results 3 March", "Intake II, EU/equivalent non-EU and non-EU abroad: 2 February–1 April 2026 13:00 CEST; remote interviews 21–24 April; results 5 May", "Intake III, EU/equivalent non-EU and non-EU abroad: 1 June–10 September 2026 13:00 CEST"],
        "non_eu_deadline": "2026-01-27 13:00 CET (Intake I); 2026-04-01 13:00 CEST (Intake II); 2026-09-10 13:00 CEST (Intake III)",
        "eu_deadline": "2026-04-01 13:00 CEST (Intake II); 2026-09-10 13:00 CEST (Intake III)",
        "application_deadline": "2026-09-10 13:00 CEST for the published final Intake III",
        "scholarship_deadline": None,
        "pre_enrolment_required": True,
        "universitaly_required": True,
        "timeline_risk": "high",
        "deadline_notes": bi("All dates are from the 2026/27 call and had either passed or were approaching when checked on 14 July 2026. The three rounds are not a visa guarantee: selected non-EU students must complete Universitaly pre-enrolment before their visa, and the programme warns that University offices may be closed in August, delaying validation. Do not reuse these dates for 2027/28.", "Tüm tarihler 2026/27 çağrısındandır ve 14 Temmuz 2026'da kontrol edildiğinde geçmiş veya yakındı. Üç tur vize garantisi değildir: seçilen AB dışı öğrenciler vizeden önce Universitaly ön kaydını tamamlamalıdır; program Ağustos'ta Üniversite ofislerinin kapanıp doğrulamayı geciktirebileceği uyarısını yapar. Bu tarihleri 2027/28 için yeniden kullanmayın."),
    }
    row["decision_summary"] = {
        "main_strengths": [bi("A 2026/27 English LM-20 in Forlì with separate Aeronautics and Space curricula, restricted to 80 places (up to 15 non-EU residents abroad) and an explicit selection/interview process rather than a vague open-admission label.", "Forlì'de Havacılık ve Uzay için ayrı müfredatları olan 2026/27 İngilizce LM-20'dir; belirsiz açık kabul etiketi yerine 80 kontenjanla (yurt dışında ikamet eden AB dışı adaylar için en fazla 15) ve açık seçme/mülakat süreciyle sınırlıdır."), bi("Forlì housing support is concrete even though price data are not: two ER.GO residences, including one near Engineering, plus University housing-search support and an Accommodation Showcase.", "Forlì konaklama desteği, fiyat verisi olmasa da somuttur: biri Mühendislik yakınında iki ER.GO yurdu, ayrıca Üniversite konaklama arama desteği ve Accommodation Showcase vardır.")],
        "main_risks": [bi("Forlì rent is unknown from the official sources checked. Do not use the University of Bologna city-centre price examples for this Romagna-campus programme; budget independently until a Forlì offer is secured.", "Kontrol edilen resmî kaynaklarda Forlì kirası bilinmiyor. Bologna merkez fiyat örneklerini bu Romagna kampüsü programı için kullanmayın; Forlì teklifi güvenceye alınana kadar bağımsız bütçe yapın."), bi("The final 2026 Intake III deadline is 10 September, but a non-EU applicant should not treat the final round as a safe visa schedule because Universitaly validation and August office closures create timing risk.", "Son 2026 Intake III son tarihi 10 Eylül'dür; ancak AB dışı aday Universitaly doğrulaması ve Ağustos ofis kapanışları zamanlama riski yarattığından son turu güvenli vize takvimi saymamalıdır."), bi("Italian B2 is a meaningful requirement or study-plan obligation despite English delivery. It must not be hidden by the English programme label.", "Program İngilizce yürütülse de İtalyanca B2 anlamlı bir koşul veya ders planı yükümlülüğüdür. İngilizce program etiketiyle gizlenmemelidir.")],
        "best_for": [bi("Applicants who can meet both English delivery and the programme's Italian-language condition, want a selective Aeronautics/Space choice, and can plan visas early rather than rely on the final intake.", "Hem İngilizce eğitimi hem programın İtalyanca dil koşulunu karşılayabilen, seçici Havacılık/Uzay tercihi isteyen ve son tura güvenmek yerine vizeyi erken planlayabilen adaylar.")],
        "not_ideal_for": [bi("Applicants who need an official Forlì rent quote before applying, who cannot meet the Italian B2 condition, or who require a late non-EU admission round to function as a visa guarantee.", "Başvurmadan önce resmî Forlì kira teklifi, İtalyanca B2 koşulunu karşılayamama veya geç AB dışı kabul turunun vize garantisi olmasını isteyen adaylar.")],
    }
    profile = row.setdefault("source_profile", {})
    logs = [item for item in profile.get("source_log", []) if isinstance(item, dict) and item.get("url") not in {programme_url, admission_url, call_url, housing_url}]
    logs.extend([
        source(programme_url, "University of Bologna Aerospace Engineering 2026/27", "official_program_page", ["program", "language", "curriculum"], "Current page confirms an active 120-ECTS English LM-20 in Forlì, 80 places, and Aeronautics/Space curricula.", "Güncel sayfa Forlì'de aktif 120 AKTS İngilizce LM-20'yi, 80 kontenjanı ve Havacılık/Uzay müfredatlarını doğrular."),
        source(admission_url, "Bologna Aerospace Engineering enrolment requirements", "official_admission_page", ["admission", "non_eu", "language", "deadline"], "Current page confirms the restricted 2026/27 selection, maximum 15 non-EU residents abroad, Italian B2 requirement/obligation, remote interview, Universitaly and document requirements.", "Güncel sayfa sınırlı 2026/27 seçimini, yurt dışında ikamet eden en fazla 15 AB dışı adayı, İtalyanca B2 koşulu/yükümlülüğünü, uzaktan mülakatı, Universitaly ve belge koşullarını doğrular."),
        source(call_url, "University of Bologna Aerospace Engineering call 2026/27", "official_admission_page", ["admission", "non_eu", "deadline"], "Official 2026/27 call gives three dated intakes, strict closing times, remote interview dates, result dates and enrolment windows. It is a cycle-specific PDF, not a future-cycle prediction.", "Resmî 2026/27 çağrısı üç tarihli turu, kesin kapanış saatlerini, uzaktan mülakat tarihlerini, sonuç tarihlerini ve kayıt pencerelerini verir. Bu gelecek döngü tahmini değil, döngüye özgü PDF'dir."),
        source(housing_url, "University of Bologna housing and residences", "official_housing_page", ["housing"], "Current University housing page identifies Forlì's Sassi Masini and Ex-ENAV residences, ER.GO application route, Accommodation Showcase and local search support, but does not publish a Forlì rent amount.", "Güncel Üniversite konaklama sayfası Forlì'nin Sassi Masini ve Ex-ENAV yurtlarını, ER.GO başvuru yolunu, Accommodation Showcase'i ve yerel arama desteğini tanımlar; ancak Forlì kira tutarı yayımlamaz."),
    ])
    profile.update({
        "official_program_page": programme_url,
        "official_admission_page": admission_url,
        "official_housing_page": housing_url,
        "source_log": logs,
        "last_verified": CHECKED,
        "needs_verification": False,
        "verification_notes": bi("Application dates and housing access are source-checked. The card retains the Forlì price gap as unknown instead of filling it with Bologna-city estimates.", "Başvuru tarihleri ve konaklama erişimi kaynakla doğrulanmıştır. Kart, Forlì fiyat boşluğunu Bologna şehir tahminleriyle doldurmak yerine bilinmiyor olarak korur."),
    })
    profile.setdefault("field_confidence", {}).update({"application_timeline_profile": "high", "housing": "high", "living_profile": "unknown", "deadlines": "high"})
    document["last_updated"] = CHECKED
    newline = "\r\n" if "\r\n" in original else "\n"
    PATH.write_text(json.dumps(document, ensure_ascii=False, indent=2).replace("\n", newline) + newline, encoding="utf-8")
    print("Updated Bologna Aerospace with official 2026/27 intake dates and honest Forlì housing evidence.")


if __name__ == "__main__":
    main()
