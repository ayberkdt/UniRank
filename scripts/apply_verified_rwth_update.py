"""Add current, source-checked decision data for RWTH Aerospace Engineering MSc."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data_base" / "almanya.json"
CHECKED = "2026-07-14"


def bi(en: str, tr: str) -> dict[str, str]:
    return {"en": en, "tr": tr}


def src(url: str, title: str, kind: str, fields: list[str], en: str, tr: str, confidence: str = "high") -> dict[str, Any]:
    return {"url": url, "title": title, "source_type": kind, "access_status": "ok", "last_checked": CHECKED, "relevant_fields": fields, "confidence": confidence, "notes": bi(en, tr)}


def main() -> None:
    original = PATH.read_text(encoding="utf-8")
    rows: list[dict[str, Any]] = json.loads(original)
    row = next(item for item in rows if item.get("id") == "de_rwth_aachen_aerospace_msc")

    programme = "https://www.rwth-aachen.de/cms/root/Studium/Vor-dem-Studium/Studiengaenge/Liste-Aktuelle-Studiengaenge/Studiengangbeschreibung/~bkoe/Luft-und-Raumfahrttechnik-M-Sc-/"
    masters = "https://www.maschinenbau.rwth-aachen.de/cms/Maschinenbau/studium/Studieninteressierte/~basfwc/Masterbewerbung/"
    process = "https://www.maschinenbau.rwth-aachen.de/cms/Maschinenbau/studium/Studieninteressierte/Masterbewerbung/~baxuja/Der-Bewerbungsprozess/"
    non_eu = "https://www.maschinenbau.rwth-aachen.de/go/id/baxvgl"
    international = "https://www.rwth-aachen.de/cms/root/studium/vor-dem-studium/bewerbung-um-einen-studienplatz/master-bewerbung/~dqml/bewerbung-master-internationale/?lidx=1"
    costs = "https://www.rwth-aachen.de/cms/root/studium/vor-dem-studium/internationale-studieninteressierte/organisation-des-studienaufenthaltes/internationale-studierende/~bqmo/kosten/?lidx=1"
    asta_finance = "https://www.asta.rwth-aachen.de/ueber-uns/finanzen/"
    scholarship = "https://www.rwth-aachen.de/cms/root/transfer/spenden-sponsoring/deutschlandstipendium/~emd/bewerben/?lidx=1"
    housing = "https://www.studierendenwerk-aachen.de/de/wohnen.html"
    housing_support = "https://www.rwth-aachen.de/go/id/gbksm/lidx/1"
    ilr = "https://www.ilr.rwth-aachen.de/cms/ilr/Forschung/~dcnnn/Forschungsfelder/lidx/1/"
    ilr_facilities = "https://www.ilr.rwth-aachen.de/cms/ilr/Forschung/~lkfb/Ausstattung/lidx/1/"

    row["teaching_language"] = ["German"]
    row["eligibility_profile"].update({
        "eligible_for_non_eu": True,
        "required_previous_degree": bi("Recognised first university degree with the programme-specific academic background defined in the examination regulations.", "Sinav yonetmeliginde tanimlanan programa ozgu akademik altyapiya sahip, taninan ilk universite derecesi."),
        "accepted_backgrounds": ["Mechanical Engineering or an academically comparable degree"],
        "admission_mode": "subject-specific entrance assessment; no NC after requirements are met",
        "admission_risk": "high",
        "required_documents": [
            bi("Degree certificate and/or transcript", "Diploma belgesi ve/veya transkript"),
            bi("Module handbook excerpts or course descriptions for the previous degree", "Onceki dereceye ait modul el-kitabi bolumleri veya ders tanimlari"),
            bi("Faculty of Mechanical Engineering supplemental application form", "Makine Muhendisligi Fakultesi ek basvuru formu"),
            bi("German C1 proof (recommended at application; teaching-language proof required for enrolment)", "Almanca C1 kaniti (basvuruda onerilir; kayit icin egitim dili kaniti gerekir)"),
            bi("Engineering internship evidence, if available", "Varsa muhendislik staji kaniti"),
        ],
        "verification_notes": bi("For the Mechanical Engineering-based MSc group that includes Aerospace Engineering, RWTH checks 145 CP in engineering and maths/science fields, compares core subjects, rejects more than 30 CP of academic conditions, and handles a 16-week engineering internship as a condition to be completed before the Master's thesis rather than an automatic application exclusion.", "Aerospace Engineering'i iceren Makine Muhendisligi temelli yuksek lisans grubu icin RWTH 145 AKTS muhendislik ve matematik/fen alanini kontrol eder, temel dersleri karsilastirir, 30 AKTS'den fazla akademik eksikligi reddeder ve 16 haftalik muhendislik stajini otomatik basvuru engeli degil, yuksek lisans tezinden once tamamlanacak kosul olarak ele alir."),
    })
    row["language_profile"].update({
        "teaching_language": ["German"],
        "english_required": None,
        "english_level_required": None,
        "german_required": True,
        "german_level_required": "C1; accepted examples include Goethe C1, TestDaF level 4 in all four parts, DSH-2 and telc Deutsch C1 Hochschule.",
        "language_risk": "high",
        "verification_notes": bi("The official programme profile lists German as the language. The Faculty's third-country application process recommends C1 proof with named accepted evidence for German-taught Master's degrees; the programme profile says teaching-language proof is required for enrolment.", "Resmi program profili dili Almanca olarak listeler. Fakultenin ucuncu ulke basvuru sureci Almanca yuksek lisanslar icin adlari verilen kabul edilen kanitlarla C1 belgesini onerir; program profili kayit icin egitim dili kaniti gerektigini belirtir."),
    })
    row["cost_profile"].update({
        "academic_year": "Current pages checked 2026-07-14; semester components current for 2026",
        "tuition_eur_per_year_min": 0,
        "tuition_eur_per_year_max": 0,
        "tuition_eur_per_year_estimated": 0,
        "tuition_basis": "regular_RWTH_programme_no_general_tuition; source is dated 2024 and therefore confidence is medium",
        "student_contribution_eur": None,
        "student_contribution_calculated_eur": 318.06,
        "student_contribution_calculation": "EUR 128.00 Studierendenwerk social contribution (from summer 2026) + EUR 6.42 student-body contribution + EUR 183.64 mobility contribution. Components are published separately; verify the total on the current enrolment notice.",
        "total_academic_cost_eur_per_year_estimated": None,
        "source_notes": bi("An RWTH AStA page states that RWTH students pay no tuition but do pay a semester contribution. The current public component pages yield EUR 318.06 by calculation; this is an interpreted sum, not a single RWTH invoice, and must be rechecked for the enrolment term.", "RWTH AStA sayfasi RWTH ogrencilerinin ogrenim ucreti odemedigini ancak donem katkisi odedigini belirtir. Guncel kamuya acik bilesen sayfalari hesapla 318,06 EUR verir; bu tek bir RWTH faturasinin tutari degil, yorumlanmis toplama sonucudur ve kayit donemi icin yeniden kontrol edilmelidir."),
        "verification_notes": bi("No general tuition does not mean no study cost. The displayed semester-contribution total is clearly marked as a calculation from official components.", "Genel ogrenim ucretinin olmamasi egitim maliyetinin olmadigi anlamina gelmez. Gosterilen donem katkisi toplami resmi bilesenlerden hesaplama olarak acikca etiketlenir."),
    })
    row["scholarship_profile"].update({
        "regional_scholarship_available": True,
        "regional_scholarship_name": "RWTH Bildungsfonds Deutschlandstipendium",
        "merit_scholarships": [bi("RWTH Bildungsfonds Deutschlandstipendium: EUR 300/month, at least two semesters, awarded annually for the winter semester. The current page reports 379 recipients and says the application period is every June; the exact next window is announced separately.", "RWTH Bildungsfonds Deutschlandstipendium: ayda 300 EUR, en az iki donem, her yil kis donemi icin verilir. Guncel sayfa 379 bursiyer bildirir ve basvuru doneminin her Haziran oldugunu, kesin sonraki araligin ayri duyuruldugunu soyler.")],
        "tuition_waivers": [],
        "non_eu_eligible": None,
        "scholarship_deadline": "June annually; exact next application window not yet published on the checked page",
        "scholarship_application_url": scholarship,
        "funding_competitiveness": "high",
        "funding_notes": bi("The scholarship supports excellent students and first-semester students in regular study time. The checked page does not publish nationality eligibility, so a non-EU applicant must confirm before budgeting it as funding.", "Burs, normal ogrenim suresindeki basarili ogrencileri ve ilk donem ogrencilerini destekler. Kontrol edilen sayfa uyruk uygunlugunu yayimlamaz; bu nedenle AB disi aday bunu finansman saymadan once teyit etmelidir."),
    })
    row["living_profile"].update({
        "city_cost_level": "medium",
        "monthly_living_cost_eur_min": 1100,
        "monthly_living_cost_eur_max": None,
        "monthly_living_cost_eur_estimated": None,
        "monthly_living_cost_basis": bi("RWTH's 2026 cost guidance advises at least EUR 1,100/month. It itemises rent including utilities at EUR 400-600; EUR 992/month is stated as the residence-permit proof minimum, not the university's recommended budget.", "RWTH'nin 2026 maliyet rehberi ayda en az 1.100 EUR onerir. Kira ve yan giderleri 400-600 EUR olarak ayristirir; ayda 992 EUR oturum izni icin kanit asgarisidir, universitenin onerilen butcesi degildir."),
        "average_room_rent_eur": None,
        "average_room_rent_eur_min": 400,
        "average_room_rent_eur_max": 600,
        "average_room_rent_scope_label": bi("Aachen accommodation including utilities; RWTH planning range", "Aachen konaklamasi, yan giderler dahil; RWTH planlama araligi"),
        "student_housing_available": True,
        "student_housing_competitiveness": "high",
        "housing_difficulty": "high",
        "living_risk": "high",
        "housing_sentiment": None,
        "housing_notes": bi("Studierendenwerk Aachen offers about 5,000 places in 24 residences across Aachen and Juelich, but RWTH says finding accommodation is particularly difficult at the beginning of the semester. Its student-housing guidance says apply as early as possible; the cited brochure reports typical waits of around six months for a single room and more than a year for an apartment. Do not treat this as guaranteed availability.", "Studierendenwerk Aachen, Aachen ve Juelich'te 24 yerleskede yaklasik 5.000 yer sunar; ancak RWTH donem basinda konut bulmanin ozellikle zor oldugunu belirtir. Ogrenci konaklama rehberi mumkun oldugunca erken basvurmayi onerir; atifli brosur tek kisilik oda icin tipik yaklasik alti ay, apartman icin bir yildan fazla bekleme bildirir. Bu, uygunluk garantisi degildir."),
        "verification_notes": bi("The rent range is official RWTH cost planning and includes utilities; it is not a quote for a specific room or a dorm guarantee.", "Kira araligi resmi RWTH maliyet planlamasidir ve yan giderleri icerir; belirli bir oda teklifi veya yurt garantisi degildir."),
    })
    row["curriculum_profile"].update({
        "tracks": ["aerodynamics", "propulsion_systems", "structural_design_and_lightweight", "flight_system_dynamics", "aerospace_systems"],
        "specializations": ["aerodynamics", "propulsion_systems", "structural_design_and_lightweight", "flight_system_dynamics", "aerospace_systems"],
        "mandatory_courses": [],
        "elective_courses": ["Aerodynamics", "Propulsion systems", "Structural design and lightweight construction", "Flight-system dynamics", "Aerospace systems"],
        "thesis_required": True,
        "internship_required": False,
        "curriculum_url": programme,
        "curriculum_structure": bi("90 ECTS over three semesters: two semesters of required/elective modules followed by a final independent scientific Master's thesis semester. The programme page describes aerodynamics, propulsion, lightweight structures, flight-system dynamics and aerospace systems as the technical areas.", "Uc donemde 90 AKTS: iki donem zorunlu/secmeli modul, ardindan bagimsiz bilimsel yuksek lisans tezi donemi. Program sayfasi teknik alanlar olarak aerodinamik, itki, hafif yapilar, ucus sistemi dinamigi ve havacilik-uzay sistemlerini tanimlar."),
    })
    row["category_profile"].update({"primary_categories": ["aerospace_engineering"], "secondary_categories": ["aeronautics", "space_systems", "propulsion", "aerospace_structures", "fluid_dynamics", "flight_mechanics"], "normalized_tags": ["aerodynamics", "propulsion", "aerospace_structures", "flight_mechanics", "aerospace_systems", "space_systems"]})
    row["research_profile"].update({
        "department_research_areas": ["Flight physics", "Aircraft design", "Systems analysis", "Space flight"],
        "labs": ["Low-speed wind tunnel", "Three water-tunnel facilities", "Rotor and propeller test bench", "Acoustic laboratory", "RWTH high-performance computing for CFD"],
        "research_centers": ["Chair and Institute of Aerospace Systems (ILR)"],
        "research_strength_summary": bi("ILR's official research profile is specific: flight physics, aircraft design, systems analysis and space flight. Its facilities include low-speed and water tunnels, a rotor/propeller test bench, an acoustic lab and CFD on RWTH high-performance computing. This is direct infrastructure evidence, not a ranking inference.", "ILR'nin resmi arastirma profili somuttur: ucus fizigi, ucak tasarimi, sistem analizi ve uzay ucusu. Tesisleri dusuk hiz ve su tunellerini, rotor/pervane test duzenegini, akustik laboratuvari ve RWTH yuksek basarimli hesaplama ile HAD'i icerir. Bu siralama cikarimi degil, dogrudan altyapi kanitidir."),
        "research_strength_score": None,
        "research_sources": [ilr, ilr_facilities],
    })
    row["industry_ecosystem_profile"].update({
        "nearby_companies": [], "confirmed_partners": [], "research_institutes": ["Chair and Institute of Aerospace Systems (ILR)"],
        "ecosystem_notes": bi("ILR says much research is carried out with cooperation partners and that it has connections to industry and research institutions, but the checked pages do not identify a programme-specific partner. No company partnership is claimed.", "ILR arastirmanin buyuk bolumunun isbirligi ortaklariyla yapildigini ve sanayi/arastirma kurumlariyla baglari oldugunu belirtir; ancak kontrol edilen sayfalar programa ozgu bir ortak tanimlamaz. Sirket ortakligi iddia edilmez."),
        "ecosystem_strength_score": None,
    })
    row["application_timeline_profile"].update({
        "academic_year": "Recurring official deadline policy checked 2026-07-14",
        "intake_terms": ["winter semester", "summer semester"],
        "application_rounds": ["Third-country applicant: annual deadline 1 March for winter / 1 September for summer", "EU/EEA applicant: annual deadline 15 July for winter / 15 January for summer"],
        "non_eu_deadline": "1 March (winter semester) / 1 September (summer semester); annual deadlines for third-country applicants to unrestricted Master's programmes",
        "eu_deadline": "15 July (winter semester) / 15 January (summer semester); annual deadlines for EU/EEA applicants",
        "winter_deadline": "Third-country: 1 March; EU/EEA: 15 July",
        "summer_deadline": "Third-country: 1 September; EU/EEA: 15 January",
        "application_deadline": "See applicant group: third-country 1 March/1 September; EU/EEA 15 July/15 January",
        "timeline_risk": "high",
        "deadline_notes": bi("RWTH's Faculty of Mechanical Engineering states that the third-country application form opens annually until 1 March for winter and 1 September for summer. The central international Master's page confirms the 1 March/1 September third-country deadlines and 15 July/15 January EU/EEA deadlines for unrestricted Master's programmes. Confirm the live application portal before submitting because these are exclusion deadlines.", "RWTH Makine Muhendisligi Fakultesi ucuncu ulke basvuru formunun kis icin her yil 1 Mart'a, yaz icin 1 Eylul'e kadar acik oldugunu belirtir. Merkezi uluslararasi yuksek lisans sayfasi, serbest kontenjanli yuksek lisanslar icin ucuncu ulke 1 Mart/1 Eylul ve AB/AEA 15 Temmuz/15 Ocak tarihlerini dogrular. Bunlar kesin son tarih oldugu icin gondermeden once canli basvuru portalini teyit edin."),
    })
    row["student_sentiment_profile"] = {"student_satisfaction_score": None, "sentiment_confidence": "unknown", "sample_size_estimate": None, "date_range": "", "student_sentiment_sources": [], "student_sentiment_summary": bi("No sufficiently documented, independent student-sentiment sample was retained; no sentiment score is shown.", "Yeterince belgelenmis bagimsiz ogrenci gorusu orneklemi tutulmadi; duygu puani gosterilmez."), "verification_notes": bi("Student sentiment was not invented to complete the card.", "Ogrenci gorusu karti tamamlamak icin uydurulmadi.")}
    row["decision_summary"].update({
        "main_strengths": [bi("A genuinely dedicated 90-ECTS Aerospace Engineering MSc, with two taught semesters followed by a thesis semester, and technical coverage spanning aerodynamics, propulsion, lightweight structures, flight-system dynamics and aerospace systems.", "Iki ders donemi ardindan tez donemi olan, aerodinamik, itki, hafif yapilar, ucus sistemi dinamigi ve havacilik-uzay sistemlerini kapsayan, gercekten amaca yonelik 90 AKTS Aerospace Engineering yuksek lisansi."), bi("ILR supplies concrete aerospace infrastructure and research exposure, including tunnels, acoustic/rotor testing and HPC-backed CFD.", "ILR tuneller, akustik/rotor testleri ve HPC destekli HAD dahil somut havacilik-uzay altyapisi ve arastirma deneyimi sunar.")],
        "main_risks": [bi("This is German-taught. Treat C1 German as a hard practical requirement, not an optional advantage.", "Bu program Almanca okutulur. Almanca C1'i istege bagli avantaj degil, temel pratik gereklilik olarak gorun."), bi("The academic gate is stringent: only about one third of external Faculty of Mechanical Engineering applicants meet the Master's entry requirements, and more than 30 CP of academic conditions leads to rejection.", "Akademik esik katidir: Makine Muhendisligi Fakultesi dis adaylarinin yalnizca yaklasik ucte biri yuksek lisans giris kosullarini karsilar; 30 AKTS'den fazla akademik eksiklik redle sonuclanir."), bi("Housing is the main logistical risk: RWTH advises at least EUR 1,100/month and warns that early-semester accommodation is particularly difficult; dormitory waits can be long.", "Konut ana lojistik risktir: RWTH ayda en az 1.100 EUR onerir ve donem basinda konut bulmanin ozellikle zor oldugunu uyarir; yurt beklemeleri uzun olabilir.")],
    })
    row["financials"] = {"tuition_fee_per_year": None, "semester_fee": None}
    row["scholarships_info"] = []
    row["admission"] = {"requirements": {"minimum_gpa": None, "minimum_gpa_notes": "Grades are not used for the faculty's entry assessment according to the checked guidance.", "required_ects": "145 CP in engineering and mathematics/natural-science fields; conditions above 30 CP lead to rejection.", "language_requirements": "German C1; see language_profile and source log."}}

    profile = row.setdefault("source_profile", {})
    profile.update({"official_program_page": programme, "official_admission_page": non_eu, "official_curriculum_page": programme, "official_tuition_page": costs, "official_scholarship_page": scholarship, "official_housing_page": housing, "official_department_page": ilr, "source_log": [
        src(programme, "RWTH Aerospace Engineering M.Sc.", "official_program_page", ["program", "language", "admission", "curriculum", "deadline"], "Official programme profile verifies an active German-taught 90-ECTS, three-semester M.Sc. with winter and summer entry and the named aerospace technical areas.", "Resmi program profili aktif Almanca 90 AKTS, uc donem M.Sc.'yi, kis/yaz girisini ve adlari verilen havacilik-uzay teknik alanlarini dogrular."),
        src(masters, "RWTH Faculty of Mechanical Engineering Master's Application", "official_admission_page", ["admission", "curriculum"], "Official faculty page includes Aerospace Engineering in the Mechanical Engineering-based Master's group and gives the 145-CP, subject-comparison, 30-CP-condition and 16-week internship rules.", "Resmi fakult e sayfasi Aerospace Engineering'i Makine Muhendisligi temelli yuksek lisans grubuna dahil eder ve 145 AKTS, ders karsilastirma, 30 AKTS kosul ve 16 haftalik staj kurallarini verir."),
        src(process, "RWTH Faculty of Mechanical Engineering Application Process", "official_admission_page", ["admission", "deadline", "language"], "Official process page distinguishes applicant groups, lists document categories and C1 German evidence for German-taught Master's degrees.", "Resmi surec sayfasi aday gruplarini ayirir, belge kategorilerini ve Almanca okutulan yuksek lisanslar icin C1 Almanca kanitini listeler."),
        src(non_eu, "RWTH Faculty of Mechanical Engineering Applicants from Third Countries", "official_admission_page", ["admission", "non_eu", "deadline", "language"], "Official third-country page gives the online process, required faculty supplementary form, documents, C1 German evidence and annual 1 March/1 September cutoffs.", "Resmi ucuncu ulke sayfasi cevrim ici sureci, gereken fakult e ek formunu, belgeleri, C1 Almanca kanitini ve yillik 1 Mart/1 Eylul son tarihlerini verir."),
        src(international, "RWTH International Master's Application", "official_admission_page", ["admission", "non_eu", "deadline"], "Official central page states online submission, document requirements and annual deadlines for unrestricted Master's programmes by applicant group.", "Resmi merkezi sayfa cevrim ici gonderimi, belge gereksinimlerini ve aday grubuna gore serbest kontenjanli yuksek lisanslarin yillik son tarihlerini belirtir."),
        src(costs, "RWTH Aachen Costs of Studying in Aachen 2026", "official_cost_of_living_page", ["tuition", "housing", "living"], "Current RWTH cost guidance recommends at least EUR 1,100/month and lists EUR 400-600 accommodation including utilities plus the EUR 992 residence-permit proof minimum.", "Guncel RWTH maliyet rehberi ayda en az 1.100 EUR onerir; yan giderler dahil 400-600 EUR konaklama ve 992 EUR oturum izni kanit asgarisini listeler."),
        src(asta_finance, "RWTH AStA Finance and Semester-Fee Components", "official_tuition_page", ["tuition", "fees"], "Current AStA finance page gives EUR 6.42 student-body and EUR 183.64 mobility components; totals must be combined with the separately published social contribution and rechecked at enrolment.", "Guncel AStA finans sayfasi 6,42 EUR ogrenci toplulugu ve 183,64 EUR hareketlilik bilesenlerini verir; toplam, ayri yayimlanan sosyal katkiyla birlestirilmeli ve kayitta yeniden kontrol edilmelidir."),
        src(scholarship, "RWTH Bildungsfonds Deutschlandstipendium", "official_scholarship_page", ["scholarship", "funding"], "Current page states EUR 300/month, at least two semesters, annual winter-semester awards and June applications; it does not state nationality eligibility.", "Guncel sayfa ayda 300 EUR'u, en az iki donemi, yillik kis donemi odullerini ve Haziran basvurularini belirtir; uyruk uygunlugunu belirtmez."),
        src(housing, "Studierendenwerk Aachen Housing", "official_housing_page", ["housing"], "Current student-services page lists about 5,000 places across 24 residences in Aachen and Juelich, in varied room/apartment formats.", "Guncel ogrenci hizmetleri sayfasi Aachen ve Juelich'te 24 yerleskede farkli oda/apartman bicimlerinde yaklasik 5.000 yeri listeler."),
        src(housing_support, "RWTH Housing Support for International Students", "official_housing_page", ["housing"], "Current RWTH page says finding accommodation in Aachen is particularly difficult at the beginning of the semester.", "Guncel RWTH sayfasi Aachen'de donem basinda konut bulmanin ozellikle zor oldugunu belirtir."),
        src(ilr, "RWTH ILR Fields of Research", "official_department_page", ["research"], "Official ILR page names flight physics, aircraft design, systems analysis and space flight research, with aerospace systems-engineering context.", "Resmi ILR sayfasi havacilik-uzay sistem muhendisligi baglaminda ucus fizigi, ucak tasarimi, sistem analizi ve uzay ucusu arastirmalarini adlandirir."),
        src(ilr_facilities, "RWTH ILR Equipment and Research Infrastructure", "official_lab_page", ["research"], "Official ILR facilities page documents tunnels, rotor/propeller test bench, acoustic laboratory and CFD using RWTH high-performance computing.", "Resmi ILR tesis sayfasi tunelleri, rotor/pervane test duzenegini, akustik laboratuvarini ve RWTH yuksek basarimli hesaplama kullanan HAD'i belgeler."),
    ], "last_verified": CHECKED, "needs_verification": False, "verification_notes": bi("All shown programme, admissions, cost, living and research facts have checked official sources. The known limits remain visible: the tuition-source statement is older and the scholarship page does not state non-EU eligibility.", "Gosterilen tum program, kabul, maliyet, yasam ve arastirma bilgileri kontrol edilmis resmi kaynaklara sahiptir. Bilinen sinirlar gorunur tutulur: ogrenim-ucreti kaynak ifadesi daha eskidir ve burs sayfasi AB disi uygunlugu belirtmez.")})
    profile["field_confidence"] = {"program_basic_info": "high", "language": "high", "admission": "high", "tuition": "medium", "scholarship": "high", "curriculum": "high", "research_profile": "high", "industry_ecosystem_profile": "unknown", "application_timeline_profile": "high", "living_profile": "high", "housing": "high", "deadlines": "high"}
    newline = "\r\n" if "\r\n" in original else "\n"
    PATH.write_text(json.dumps(rows, ensure_ascii=False, indent=2).replace("\n", newline) + newline, encoding="utf-8")
    print("Updated RWTH Aerospace Engineering MSc with current official evidence.")


if __name__ == "__main__":
    main()
