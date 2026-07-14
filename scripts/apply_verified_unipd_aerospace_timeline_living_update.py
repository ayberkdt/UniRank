"""Add current Padua application timing and scoped official living costs."""

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
    row = next(item for item in document["universities"] if item.get("id") == "unipd_aerospace")
    programme_url = "https://apply.unipd.it/courses/course/232-aerospace-engineering?search=2301888"
    living_url = "https://www.unipd.it/en/costo-vita-padova"
    housing_url = "https://www.unipd.it/en/alloggi-studenti"

    row["living_profile"] = {
        "city_cost_level": "medium",
        "monthly_living_cost_eur_min": None,
        "monthly_living_cost_eur_max": None,
        "monthly_living_cost_eur_estimated": None,
        "average_room_rent_eur": None,
        "average_room_rent_eur_min": 300,
        "average_room_rent_eur_max": 600,
        "average_room_rent_scope_label": bi("University of Padua indicative single-room price, plus expenses", "University of Padua gösterge niteliğinde tek kişilik oda fiyatı, giderler hariç"),
        "food_cost_eur_month": None,
        "student_housing_available": True,
        "student_housing_competitiveness": "high",
        "housing_difficulty": "high",
        "living_risk": "medium",
        "housing_sentiment": None,
        "housing_notes": bi("The University lists single rooms at EUR 300-600/month plus expenses as an indicative Padua price. ESU housing is competitive and assigned through an annual call based on income/merit; for 2026/27, first-year EU/international students had to apply by 25 August 2026 at 10:00. The International Housing Office supports enrolled international students and has private-residence agreements, but neither route guarantees a room.", "Üniversite, Padova'da tek kişilik odaları giderler hariç gösterge niteliğinde ayda 300-600 EUR olarak listeler. ESU konaklaması rekabetçidir ve gelir/başarıya göre yıllık çağrıyla tahsis edilir; 2026/27 için birinci sınıf AB/uluslararası öğrenciler 25 Ağustos 2026 saat 10:00'a kadar başvurmalıydı. International Housing Office kayıtlı uluslararası öğrencilere destek verir ve özel yurt anlaşmaları vardır; ancak iki yol da oda garantilemez."),
        "verification_notes": bi("The source calls these costs purely indicative and excludes utilities from the room range. No all-in monthly living figure is inferred.", "Kaynak bu maliyetleri tamamen gösterge niteliğinde tanımlar ve oda aralığından faturaları hariç tutar. Tüm kalemleri içeren aylık yaşam tutarı çıkarılmaz."),
    }
    row["application_timeline_profile"] = {
        "academic_year": "2026/2027 closed reference cycle",
        "intake_terms": ["autumn; studies commence 1 October 2026"],
        "application_rounds": ["Published Aerospace Engineering application deadline: 2 May 2026, 23:59:59 Central European Time"],
        "non_eu_deadline": "2026-05-02 23:59:59 CET (published 2026/27 course application page)",
        "eu_deadline": "2026-05-02 23:59:59 CET (published 2026/27 course application page)",
        "application_deadline": "2026-05-02 23:59:59 CET for the checked 2026/27 course page",
        "scholarship_deadline": None,
        "pre_enrolment_required": True,
        "universitaly_required": True,
        "timeline_risk": "high",
        "deadline_notes": bi("The checked 2026/27 course page shows the 2 May deadline and says the application period has ended. It does not publish a 2027/28 date, so it is retained only as a closed-cycle reference. Foreign-qualification applicants must also follow the relevant category-specific Unipd call/procedure.", "Kontrol edilen 2026/27 ders sayfası 2 Mayıs son tarihini gösterir ve başvuru döneminin kapandığını söyler. 2027/28 tarihi yayımlamaz; bu nedenle yalnızca kapanmış döngü referansı olarak tutulur. Yabancı diploma adayları ayrıca ilgili kategoriye özgü Unipd çağrısını/prosedürünü izlemelidir."),
    }
    row["curriculum_profile"] = {
        "tracks": ["space", "aeronautics"],
        "specializations": ["space_propulsion", "astrodynamics", "spacecraft_attitude_dynamics_and_control", "space_instrumentation", "spacecraft_thermal_control", "aircraft_propulsion", "atmospheric_flight_dynamics", "aeroelasticity", "aircraft_systems"],
        "mandatory_courses": ["Aerospace Structures", "Manufacturing Technologies of Aerospace Materials", "Advanced Aerodynamics"],
        "elective_courses": ["Space Robotic Systems", "Laboratory of Computational Fluid Dynamics", "Aerospace Structures Laboratory", "Space Propulsion Laboratory", "Laboratory of Aircraft Propulsion", "Space Systems Laboratory", "Space Optics Instrumentation", "Modelling and Control of Electric Drives", "Global Positioning and Navigation", "Composite Materials"],
        "course_language_notes": bi("The 2026/27 course page presents the programme as English-taught and lists both Space and Aeronautics technical curricula.", "2026/27 ders sayfası programı İngilizce okutulan olarak sunar ve hem Uzay hem Havacılık teknik müfredatını listeler."),
        "thesis_required": None,
        "internship_required": None,
        "lab_courses": ["Laboratory of Computational Fluid Dynamics", "Aerospace Structures Laboratory", "Space Propulsion Laboratory", "Laboratory of Aircraft Propulsion", "Space Systems Laboratory"],
        "project_based_courses": [],
        "curriculum_url": programme_url,
        "study_plan_url": programme_url,
        "curriculum_structure": bi("The current programme page makes the technical choice visible: all students share aerospace structures, aerospace-material manufacturing and advanced aerodynamics. The Space route adds measurement for space projects, space propulsion, astrodynamics, mechanical vibrations, attitude dynamics/control, instrumentation and thermal control; the Aeronautics route adds aircraft propulsion, flight dynamics, air conditioning, aeroelasticity, measurements and aircraft systems. Optional labs make CFD, propulsion, structures, space systems, optics, navigation and electric drives discoverable before application.", "Güncel program sayfası teknik seçimi görünür kılar: tüm öğrenciler uzay/havacılık yapıları, havacılık malzemeleri imalat teknolojileri ve ileri aerodinamik ortak çekirdeğini alır. Uzay rotası uzay projeleri ölçümleri, uzay itkisi, astrodinamik, mekanik titreşimler, tutum dinamiği/kontrolü, enstrümantasyon ve termal kontrol ekler; Havacılık rotası uçak itkisi, uçuş dinamiği, iklimlendirme, aeroelastisite, ölçümler ve uçak sistemleri ekler. Seçmeli laboratuvarlar başvuru öncesinde HAD, itki, yapılar, uzay sistemleri, optik, navigasyon ve elektrikli tahrikleri görünür kılar."),
        "verification_notes": bi("Technical course names are transcribed from the 2026/27 official course page. A thesis/internship requirement is not asserted where the checked page does not state it.", "Teknik ders adları 2026/27 resmî ders sayfasından aktarılmıştır. Kontrol edilen sayfa belirtmediği yerde tez/staj gereği ileri sürülmez."),
    }
    row["category_profile"] = {
        "primary_categories": ["space_systems", "aeronautics"],
        "secondary_categories": ["space_propulsion", "astrodynamics", "gnc", "spacecraft_thermal_control", "aircraft_propulsion", "flight_dynamics", "aeroelasticity", "aircraft_systems", "cfd"],
        "normalized_tags": ["aerospace_engineering", "spacecraft_systems", "space_propulsion", "orbital_mechanics", "spacecraft_attitude_control", "spacecraft_instrumentation", "aircraft_propulsion", "flight_dynamics", "cfd", "aeroelasticity"],
    }
    profile = row.setdefault("source_profile", {})
    logs = [item for item in profile.get("source_log", []) if isinstance(item, dict) and item.get("url") not in {programme_url, living_url, housing_url}]
    logs.extend([
        source(programme_url, "University of Padua Aerospace Engineering application 2026/27", "official_admission_page", ["program", "language", "admission", "non_eu", "deadline", "curriculum"], "Current course page confirms the active 2026/27 English Aerospace Engineering MSc, its 2 May 2026 application deadline, 1 October start, two curricula and core/optional technical course areas.", "Güncel ders sayfası aktif 2026/27 İngilizce Aerospace Engineering MSc'sini, 2 Mayıs 2026 başvuru son tarihini, 1 Ekim başlangıcını, iki müfredatı ve çekirdek/seçmeli teknik ders alanlarını doğrular."),
        source(living_url, "University of Padua cost of living", "official_cost_of_living_page", ["living", "housing"], "Official University page lists an indicative EUR 300-600/month single room plus expenses, weekly groceries about EUR 60, canteen meals EUR 2-8 and warns that the figures are indicative.", "Resmî Üniversite sayfası giderler hariç gösterge niteliğinde ayda 300-600 EUR tek kişilik oda, haftalık yaklaşık 60 EUR market, 2-8 EUR yemekhane öğünü listeler ve tutarların gösterge niteliğinde olduğu uyarısını yapar."),
        source(housing_url, "University of Padua accommodation for students", "official_housing_page", ["housing", "living", "deadline"], "Current 2026/27 page documents ESU competition eligibility and 25 August 2026 first-year EU/international deadline, International Housing Office support and the absence of a universal room guarantee.", "Güncel 2026/27 sayfa ESU yarışma uygunluğunu ve birinci sınıf AB/uluslararası için 25 Ağustos 2026 son tarihini, International Housing Office desteğini ve evrensel oda garantisinin bulunmadığını belgeler."),
    ])
    profile.update({"official_admission_page": programme_url, "official_housing_page": housing_url, "source_log": logs, "last_verified": CHECKED, "needs_verification": False})
    profile.setdefault("field_confidence", {}).update({"application_timeline_profile": "high", "living_profile": "high", "housing": "high", "deadlines": "high"})
    document["last_updated"] = CHECKED
    newline = "\r\n" if "\r\n" in original else "\n"
    PATH.write_text(json.dumps(document, ensure_ascii=False, indent=2).replace("\n", newline) + newline, encoding="utf-8")
    print("Updated Padua Aerospace with official timing and scoped living-cost evidence.")


if __name__ == "__main__":
    main()
