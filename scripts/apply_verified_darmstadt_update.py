"""Add current, source-checked decision data for TU Darmstadt Aerospace MSc.

This script is idempotent.  It intentionally retains uncertainty where a
source does not establish a programme-specific fact (for example, scholarship
eligibility by nationality).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data_base" / "almanya.json"
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


def main() -> None:
    original = PATH.read_text(encoding="utf-8")
    rows: list[dict[str, Any]] = json.loads(original)
    row = next(item for item in rows if item.get("id") == "de_darmstadt_aerospace_engineering_msc")

    programme_url = "https://www.tu-darmstadt.de/studieren/studieninteressierte/studienangebot_studiengaenge/studiengang_277056.en.jsp"
    curriculum_url = "https://www.tu-darmstadt.de/media/daa_responsives_design/02_studium_medien/01_studieninteressierte_medien/02_studienangebot_medien/master_of_science_1/aerospace_engineering__msc/aerospace_engineering__msc.de.pdf"
    international_admission_url = "https://www.tu-darmstadt.de/studieren/studieninteressierte/internationale_studieninteressierte/bewerbung_und_zulassung_international/index.en.jsp"
    deadline_url = "https://www.tu-darmstadt.de/studieren/studieninteressierte/bewerbung_zulassung_tu/bewerbungsfristen/bachelor_studiengaenge_2/index.de.jsp"
    fee_url = "https://www.tu-darmstadt.de/studieren/studieren_von_a_bis_z/artikel_details_de_en_286144.en.jsp"
    tuition_policy_url = "https://www.tu-darmstadt.de/studentsoftudarmstadt/home/studileben/studienkosten_und_finanzierung.en.jsp"
    scholarship_url = "https://www.tu-darmstadt.de/deutschlandstipendium/index.en.jsp"
    living_url = "https://www.tu-darmstadt.de/studieren/studieninteressierte/internationale_studieninteressierte/organisation_des_aufenthalts_inbound/artikel_details_de_en_56836.en.jsp"
    housing_url = "https://studierendenwerkdarmstadt.de/en/accomodation-service/"
    housing_faq_url = "https://studierendenwerkdarmstadt.de/en/counseling-and-social-affairs/information-living-studying-darmstadt/accommodation/"
    fsr_url = "https://www.fsr.tu-darmstadt.de/index.en.jsp"
    celab_url = "https://www.fsr.tu-darmstadt.de/forschung_und_dienstleistung/ausstattung/standardseite_20.en.jsp"
    propulsion_url = "https://www.maschinenbau.tu-darmstadt.de/gla/index.en.jsp"

    row["teaching_language"] = ["English"]
    row["eligibility_profile"].update({
        "eligible_for_non_eu": True,
        "required_previous_degree": bi(
            "TU Darmstadt's BSc Mechanical Engineering - Sustainable Engineering reference degree, or an equivalent degree.",
            "TU Darmstadt BSc Mechanical Engineering - Sustainable Engineering referans derecesi veya buna denk bir derece.",
        ),
        "accepted_backgrounds": ["Mechanical Engineering or an equivalent degree"],
        "admission_mode": "entrance-requirements verification; no numerical admission restriction after requirements are met",
        "admission_risk": "medium",
        "required_documents": [
            bi("Degree certificate or prospective-graduation certificate", "Diploma belgesi veya beklenen mezuniyet belgesi"),
            bi("Transcript(s) for each semester", "Her donem icin transkript"),
            bi("English-language evidence", "Ingilizce yeterlik belgesi"),
            bi("Passport ID-page copy", "Pasaport kimlik sayfasi kopyasi"),
            bi("TUCaN cover sheet and any programme-specific documents shown in the application checklist", "TUCaN kapak sayfasi ve basvuru kontrol listesinde gorunen programa ozgu belgeler"),
        ],
        "verification_notes": bi(
            "The official programme page requires an equivalent reference degree, English C1 and a passed entrance-requirements verification. The international-admission page confirms an international Master's application route and its document workflow; the TUCaN checklist can require further programme-specific documents.",
            "Resmi program sayfasi denk referans derece, Ingilizce C1 ve basarili giris yeterlilik kontrolu ister. Uluslararasi kabul sayfasi uluslararasi yuksek lisans basvuru yolunu ve belge akisini dogrular; TUCaN kontrol listesi ek programa ozgu belge isteyebilir.",
        ),
    })
    row["language_profile"].update({
        "teaching_language": ["English"],
        "english_required": True,
        "english_level_required": "C1 (GER); programme page. TU Darmstadt lists examples for English-taught Master's degrees including IELTS 7.0 and TOEFL iBT 95.",
        "language_risk": "medium",
        "additional_language_notes": bi(
            "The degree is taught in English, but individual courses may be offered in German and scientific literature is also read and edited in German. This is a practical language risk, not a German admission requirement stated on the programme page.",
            "Derece Ingilizce okutulur; ancak bazi dersler Almanca sunulabilir ve bilimsel literatur Almanca da okunup islenir. Bu, program sayfasinda belirtilen bir Almanca kabul kosulu degil, pratik bir dil riskidir.",
        ),
    })
    row["cost_profile"].update({
        "academic_year": "Winter semester 2026/27 fee; pages checked 2026-07-14",
        "tuition_eur_per_year_min": 0,
        "tuition_eur_per_year_max": 0,
        "tuition_eur_per_year_estimated": 0,
        "tuition_basis": "regular_state_funded_TU_Darmstadt_programme",
        "student_contribution_eur": 402.68,
        "total_academic_cost_eur_per_year_estimated": None,
        "source_notes": bi(
            "TU Darmstadt says most programmes are tuition-free; Aerospace Engineering is listed as a regular TU Darmstadt MSc. The published normal student fee for winter semester 2026/27 is EUR 402.68, including the Germany semester ticket and a EUR 50 administration fee. It is not tuition and it is re-determined each semester.",
            "TU Darmstadt programlarin cogunun ogrenim ucretinden muaf oldugunu belirtir; Aerospace Engineering duzenli bir TU Darmstadt yuksek lisansi olarak listelenir. 2026/27 kis donemi icin yayimlanan normal ogrenci ucreti, Almanya donem bileti ve 50 EUR idari ucret dahil 402,68 EUR'dur. Bu ogrenim ucreti degildir ve her donem yeniden belirlenir.",
        ),
        "verification_notes": bi(
            "Zero means no published general tuition for this regular programme; it does not mean a zero-cost degree. The semester fee and living costs remain payable.",
            "Sifir, bu duzenli program icin yayimlanmis genel ogrenim ucreti olmadigi anlamina gelir; sifir maliyetli derece anlamina gelmez. Donem ucreti ve yasam giderleri ayrica odenir.",
        ),
    })
    row["scholarship_profile"].update({
        "regional_scholarship_available": True,
        "regional_scholarship_name": "Deutschlandstipendium at TU Darmstadt",
        "merit_scholarships": [bi(
            "TU Darmstadt's 2026/27 Deutschlandstipendium: EUR 300 per month for at least two semesters; the university says 377 students receive it for one year in the 2026/27 funding period. The 2026 application period is 21 September-18 October 2026 for students and first-semester students.",
            "TU Darmstadt 2026/27 Deutschlandstipendium: en az iki donem boyunca ayda 300 EUR; universite 2026/27 finansman doneminde 377 ogrencinin bir yil destek aldigini belirtir. 2026 basvuru donemi ogrenciler ve ilk donem ogrencileri icin 21 Eylul-18 Ekim 2026'dur.",
        )],
        "tuition_waivers": [],
        "non_eu_eligible": None,
        "scholarship_deadline": "2026-10-18 (TU Darmstadt Deutschlandstipendium 2026 call)",
        "scholarship_application_url": scholarship_url,
        "funding_competitiveness": "high",
        "funding_notes": bi(
            "This is a merit scholarship, not a tuition waiver. The current call is explicitly open to enrolled and first-semester TU Darmstadt students, but the checked page does not state a nationality rule; a non-EU applicant should confirm eligibility with the scholarship office before relying on it.",
            "Bu bir basari bursudur, ogrenim ucreti muafiyeti degildir. Guncel cagrida TU Darmstadt kayitli ve ilk donem ogrencileri acikca kapsanir; ancak kontrol edilen sayfa uyruk kuralini belirtmez. AB disi aday bu destege guvenmeden once burs ofisinden uygunlugunu teyit etmelidir.",
        ),
        "verification_notes": bi(
            "Scholarship availability, amount, duration and current deadline are verified. Non-EU eligibility is deliberately left unknown because the source checked does not state it.",
            "Bursun varligi, tutari, suresi ve guncel son tarihi dogrulandi. Kontrol edilen kaynak bunu belirtmedigi icin AB disi uygunluk bilinmiyor olarak birakildi.",
        ),
    })
    row["living_profile"].update({
        "city_cost_level": "high",
        "monthly_living_cost_eur_min": 875,
        "monthly_living_cost_eur_max": 1300,
        "monthly_living_cost_eur_estimated": None,
        "monthly_living_cost_basis": bi(
            "Studierendenwerk Darmstadt's current guidance gives EUR 875-1,300/month depending on lifestyle. TU Darmstadt separately cites a EUR 992/month BAfoeG planning figure; both are planning guidance rather than a personal quote.",
            "Studierendenwerk Darmstadt'in guncel rehberi yasam tarzina gore ayda 875-1.300 EUR verir. TU Darmstadt ayri olarak ayda 992 EUR BAfoeG planlama tutari belirtir; ikisi de kisisel teklif degil planlama rehberidir.",
        ),
        "average_room_rent_eur": None,
        "average_room_rent_eur_min": 350,
        "average_room_rent_eur_max": 650,
        "average_room_rent_scope_label": bi("Darmstadt shared-room guidance; costs can vary", "Darmstadt paylasimli oda rehberi; maliyet degisebilir"),
        "student_housing_available": True,
        "student_housing_competitiveness": "high",
        "housing_difficulty": "high",
        "living_risk": "high",
        "housing_sentiment": None,
        "housing_notes": bi(
            "Studierendenwerk Darmstadt operates eight residences with about 2,765 rooms. Applications can be made before admission, but a room is not automatic, supply is limited and waiting time depends on demand. Its accommodation FAQ says several weeks are not uncommon and advises applying early while searching for other options simultaneously.",
            "Studierendenwerk Darmstadt sekiz yurtta yaklasik 2.765 oda isletir. Kabulden once basvuru yapilabilir; ancak oda otomatik degildir, kapasite sinirlidir ve bekleme suresi talebe baglidir. Konaklama SSS'si birkac haftanin siradisi olmadigini belirtir ve erken basvurup ayni anda diger secenekleri aramayi onerir.",
        ),
        "verification_notes": bi(
            "The EUR 350-650 range is an official planning range for a shared-flat room, not a guaranteed rent or student-residence price.",
            "350-650 EUR araligi, paylasimli daire odasi icin resmi planlama araligidir; garanti kira veya yurt fiyati degildir.",
        ),
    })
    row["curriculum_profile"].update({
        "tracks": ["structural_mechanics", "fluid_dynamics", "flight_mechanics", "additive_manufacturing", "cockpit_design"],
        "specializations": ["structural_mechanics", "fluid_dynamics", "flight_mechanics", "additive_manufacturing", "cockpit_design"],
        "mandatory_courses": [
            "Tutorial (4 CP)",
            "Advanced Design Projects or Advanced Design Project plus External Project (12 CP total; at least one Aerospace Engineering topic)",
        ],
        "elective_courses": [
            "Fundamentals (6-18 CP)",
            "Digitalisation (6-18 CP)",
            "Core Aerospace Engineering electives (minimum 24 CP)",
            "Natural-science and engineering electives (minimum 12 CP in Aerospace Engineering)",
            "Studium Generale (6-12 CP)",
        ],
        "thesis_required": True,
        "internship_required": False,
        "curriculum_url": curriculum_url,
        "curriculum_structure": bi(
            "120 CP total: 16 CP compulsory tutorial/projects, 74 CP electives, and 30 CP research/thesis. An external project in industry is an option, not a compulsory internship.",
            "Toplam 120 AKTS: 16 AKTS zorunlu tutorial/proje, 74 AKTS secmeli ve 30 AKTS arastirma/tez. Sanayide dis proje secenektir; zorunlu staj degildir.",
        ),
        "verification_notes": bi(
            "The programme page and the current official course-schedule PDF support this structure. Course availability should still be checked in the catalogue for the chosen semester.",
            "Program sayfasi ve guncel resmi ders-plani PDF'i bu yapıyı destekler. Secilen donem icin ders uygunlugu yine katalogdan kontrol edilmelidir.",
        ),
    })
    row["category_profile"].update({
        "primary_categories": ["aerospace_engineering"],
        "secondary_categories": ["aeronautics", "space_systems", "propulsion", "aerospace_structures", "fluid_dynamics", "flight_mechanics"],
        "normalized_tags": ["aerospace_structures", "fluid_dynamics", "flight_mechanics", "additive_manufacturing", "cockpit_design", "propulsion", "space_systems"],
    })
    row["research_profile"].update({
        "department_research_areas": [
            "Aerospace systems engineering",
            "Concurrent and digital engineering for space systems",
            "Gas turbines and flight propulsion",
        ],
        "labs": ["Concurrent Engineering Lab (CELab)", "Institute of Flight Systems and Automatic Control (FSR)"],
        "research_centers": [],
        "research_strength_summary": bi(
            "The FSR conducts application-oriented aerospace systems-engineering research. Its CELab was established with ESA as a joint research laboratory for concurrent engineering, ground segment/operations and student practical experience. The GLA institute develops and tests turbomachine components using test rigs; these are specific research assets, not a generic prestige claim.",
            "FSR uygulama odakli havacilik ve uzay sistem muhendisligi arastirmasi yapar. CELab, eszamanli muhendislik, yer segmenti/operasyonlar ve ogrenci uygulamasi icin ESA ile ortak arastirma laboratuvari olarak kuruldu. GLA enstitusu test duzenekleriyle turbomakine bilesenleri gelistirip test eder; bunlar genel itibar iddiasi degil, somut arastirma varliklaridir.",
        ),
        "research_strength_score": None,
        "research_sources": [fsr_url, celab_url, propulsion_url],
    })
    row["industry_ecosystem_profile"].update({
        "nearby_companies": [],
        "confirmed_partners": ["European Space Agency (ESA): CELab joint research laboratory with TU Darmstadt FSR"],
        "research_institutes": ["Institute of Flight Systems and Automatic Control (FSR)", "Institute of Gas Turbines and Flight Propulsion (GLA)"],
        "ecosystem_notes": bi(
            "The ESA relationship is recorded because the official CELab page explicitly calls it a joint FSR-ESA research laboratory. No company partnership is inferred from geography or career examples.",
            "ESA iliskisi, resmi CELab sayfasi bunu FSR-ESA ortak arastirma laboratuvari olarak acikca tanimladigi icin kaydedilir. Cografi konumdan veya kariyer orneklerinden sirket ortakligi cikarilmaz.",
        ),
        "ecosystem_strength_score": None,
    })
    row["application_timeline_profile"].update({
        "academic_year": "Winter semester 2026/27",
        "intake_terms": ["winter semester", "summer semester"],
        "application_rounds": ["Winter semester 2026/27: 1 June 2026-15 July 2026 (final deadline)"],
        "non_eu_deadline": "2026-07-15 (winter semester 2026/27; final deadline; same deadline for external and internal applicants)",
        "eu_deadline": "2026-07-15 (winter semester 2026/27; final deadline; same deadline for external and internal applicants)",
        "winter_deadline": "2026-07-15 (winter semester 2026/27; applications open 2026-06-01)",
        "summer_deadline": None,
        "application_deadline": "2026-07-15 (winter semester 2026/27; final deadline)",
        "timeline_risk": "medium",
        "deadline_notes": bi(
            "The current master-deadline page lists Aerospace Engineering for winter 2026/27 from 1 June to 15 July 2026, with 15 July a final deadline for external and internal applicants. The programme also starts in summer, but the current summer-cycle dates were not published on the checked page; do not extrapolate them.",
            "Guncel yuksek lisans son-tarih sayfasi Aerospace Engineering icin 2026/27 kis doneminde 1 Haziran-15 Temmuz 2026 araligini listeler; 15 Temmuz dis ve ic adaylar icin kesin son tarihtir. Program yaz doneminde de baslar, ancak guncel yaz donemi tarihleri kontrol edilen sayfada yayimlanmamistir; tahmin edilmez.",
        ),
    })
    row["student_sentiment_profile"] = {
        "student_satisfaction_score": None,
        "sentiment_confidence": "unknown",
        "sample_size_estimate": None,
        "date_range": "",
        "student_sentiment_sources": [],
        "student_sentiment_summary": bi(
            "No sufficiently documented, independent student-sentiment sample was retained; no sentiment score is shown.",
            "Yeterince belgelenmis bagimsiz ogrenci gorusu orneklemi tutulmadi; duygu puani gosterilmez.",
        ),
        "verification_notes": bi(
            "Student sentiment remains separate from official facts and is not fabricated to fill the card.",
            "Ogrenci gorusleri resmi bilgilerden ayri tutulur ve karti doldurmak icin uydurulmaz.",
        ),
    }
    row["decision_summary"].update({
        "main_strengths": [
            bi(
                "A dedicated English Aerospace Engineering MSc with 120 CP, a 30-CP thesis, strong choice across structures, fluid dynamics, flight mechanics, additive manufacturing and cockpit design, and no compulsory internship.",
                "120 AKTS, 30 AKTS tez, yapilar, akiskanlar dinamigi, ucus mekanigi, eklemeli imalat ve kokpit tasariminda genis secim sunan, zorunlu staji olmayan, amaca yonelik Ingilizce Aerospace Engineering yuksek lisansi.",
            ),
            bi(
                "The research evidence is specific: FSR's CELab is a joint ESA research laboratory, and GLA provides aircraft-propulsion test-rig research.",
                "Arastirma kaniti somuttur: FSR'nin CELab'i ESA ile ortak arastirma laboratuvaridir ve GLA ucak itki test duzenegi arastirmasi sunar.",
            ),
        ],
        "main_risks": [
            bi(
                "English C1 and entrance-requirements verification are mandatory. Although English is the teaching language, some courses and scientific literature may involve German.",
                "Ingilizce C1 ve giris yeterlilik kontrolu zorunludur. Egitim dili Ingilizce olsa da bazi dersler ve bilimsel literatur Almanca icerebilir.",
            ),
            bi(
                "No general tuition does not remove the cost risk: the current normal semester fee is EUR 402.68 and official Darmstadt planning guidance is EUR 875-1,300/month. Student housing is limited and not automatic.",
                "Genel ogrenim ucretinin olmamasi maliyet riskini kaldirmaz: guncel normal donem ucreti 402,68 EUR ve resmi Darmstadt planlama rehberi ayda 875-1.300 EUR'dur. Ogrenci konaklamasi sinirlidir ve otomatik degildir.",
            ),
            bi(
                "The Deutschlandstipendium is real and current, but the checked call does not state non-EU eligibility. Confirm it before treating the scholarship as available funding.",
                "Deutschlandstipendium gercek ve gunceldir; ancak kontrol edilen cagrida AB disi uygunluk belirtilmez. Bursu mevcut finansman saymadan once teyit edin.",
            ),
        ],
    })

    # Legacy fields are not used by the card when profiles are present.  Clear
    # them nevertheless so raw exports cannot revive unsupported old claims.
    row["financials"] = {"tuition_fee_per_year": None, "semester_fee": 402.68}
    row["scholarships_info"] = []
    row["admission"] = {"requirements": {"minimum_gpa": None, "minimum_gpa_notes": "unknown", "required_ects": None, "language_requirements": "English C1 (GER); see language_profile and source log."}}

    log = [
        source(programme_url, "TU Darmstadt Aerospace Engineering M.Sc.", "official_program_page", ["program", "language", "admission", "curriculum", "deadline"], "Current programme page verifies an active English MSc, four semesters, winter/summer start, C1 English, equivalent degree and entrance-requirements verification. It also states that internship is optional and individual courses/literature can involve German.", "Guncel program sayfasi aktif Ingilizce yuksek lisansi, dort donemi, kis/yaz baslangicini, C1 Ingilizceyi, denk dereceyi ve giris yeterlilik kontrolunu dogrular. Ayrica stajin istege bagli oldugunu ve bazi ders/literaturun Almanca olabilecegini belirtir."),
        source(curriculum_url, "TU Darmstadt Aerospace Engineering M.Sc. Course Schedule", "official_curriculum_page", ["curriculum"], "Official current course-schedule PDF gives 120 CP: 16 CP tutorial/projects, 74 CP electives and 30 CP research/thesis, plus Aerospace Engineering minimums for core-elective and engineering elective areas.", "Resmi guncel ders-plani PDF'i 120 AKTS'yi verir: 16 AKTS tutorial/proje, 74 AKTS secmeli ve 30 AKTS arastirma/tez; ayrica ana secmeli ve muhendislik secmeli alanlari icin Aerospace Engineering asgarilarini belirtir."),
        source(international_admission_url, "TU Darmstadt Application for International Students", "official_admission_page", ["admission", "non_eu", "language"], "Official international-admission guidance says the same deadlines apply to prospective students with foreign qualifications and documents the Master's application workflow, including the TUCaN checklist and required supporting documents. It publishes English proof examples for English-taught Master's degrees.", "Resmi uluslararasi kabul rehberi yabanci nitelikli adaylar icin ayni son tarihlerin gecerli oldugunu belirtir ve TUCaN kontrol listesi ile gerekli destekleyici belgeler dahil yuksek lisans basvuru akisini belgeler. Ingilizce yurutilen yuksek lisanslar icin Ingilizce kanit orneklerini yayimlar."),
        source(deadline_url, "TU Darmstadt Master Application Deadlines", "official_admission_page", ["deadline"], "Current master-deadline page lists Aerospace Engineering for winter 2026/27 from 1 June to 15 July 2026, identifies 15 July as a final deadline and says final deadlines apply equally to external and internal applicants.", "Guncel yuksek lisans son-tarih sayfasi Aerospace Engineering'i 2026/27 kis donemi icin 1 Haziran-15 Temmuz 2026 olarak listeler, 15 Temmuz'u kesin son tarih diye belirtir ve kesin son tarihlerin dis ve ic adaylara esit uygulandigini soyler."),
        source(tuition_policy_url, "TU Darmstadt Study Costs and Funding", "official_tuition_page", ["tuition"], "TU Darmstadt states that most programmes are tuition-free in the state-funded higher-education system while students still need to budget for everyday costs and the semester fee. This supports the regular-programme no-general-tuition interpretation, not a zero-cost claim.", "TU Darmstadt devlet destekli yuksekogretim sistemi icinde programlarin cogunun ogrenim ucretinden muaf oldugunu, ancak ogrencilerin gunluk giderler ve donem ucreti icin butce ayirmasi gerektigini belirtir. Bu, duzenli program icin genel ogrenim ucreti olmadigi yorumunu destekler; sifir maliyet iddiasini degil."),
        source(fee_url, "TU Darmstadt Semester Fee and Re-Registration", "official_tuition_page", ["tuition", "fees"], "Current fee page publishes the normal winter 2026/27 student fee of EUR 402.68 and its components, and says the fee is re-determined each semester.", "Guncel ucret sayfasi 2026/27 kis donemi normal ogrenci ucreti olan 402,68 EUR'u ve bilesenlerini yayimlar; ucretin her donem yeniden belirlendigini soyler."),
        source(scholarship_url, "TU Darmstadt Deutschlandstipendium", "official_scholarship_page", ["scholarship", "funding"], "Current page publishes EUR 300/month for at least two semesters, 377 awards for the 2026/27 funding period and a 21 September-18 October 2026 window for students and first-semester students. It does not state a nationality rule.", "Guncel sayfa en az iki donem ayda 300 EUR'u, 2026/27 finansman donemi icin 377 odulu ve ogrenciler ile ilk donem ogrencileri icin 21 Eylul-18 Ekim 2026 basvuru araligini yayimlar. Uyruk kurali belirtmez."),
        source(living_url, "TU Darmstadt Costs and Budgeting", "official_cost_of_living_page", ["housing", "living"], "Current official international-student guidance gives a EUR 350-650 shared-room planning range and an approximately EUR 992/month BAfoeG living-cost figure, explicitly as general planning guidance.", "Guncel resmi uluslararasi ogrenci rehberi paylasimli oda icin 350-650 EUR planlama araligini ve yaklasik 992 EUR/ay BAfoeG yasam maliyeti tutarini, acikca genel planlama rehberi olarak verir."),
        source(housing_url, "Studierendenwerk Darmstadt Accommodation Service", "official_housing_page", ["housing"], "Current student-services page lists eight Darmstadt residences with about 2,765 rooms, allows an application before admission and warns that waiting time depends on demand and preferred room.", "Guncel ogrenci hizmetleri sayfasi Darmstadt'ta yaklasik 2.765 odali sekiz yurdu listeler, kabulden once basvuruya izin verir ve bekleme suresinin talep ile tercih edilen odaya bagli oldugu uyarisi yapar."),
        source(housing_faq_url, "Studierendenwerk Darmstadt Accommodation FAQ", "official_housing_page", ["housing", "living"], "Current FAQ says a room is not automatically included with admission, rooms are very limited, several weeks are not uncommon, and students should search early and in parallel. It also gives a EUR 875-1,300 monthly planning range.", "Guncel SSS kabul ile odanin otomatik gelmedigini, odalarin cok sinirli oldugunu, birkac haftanin siradisi olmadigini ve ogrencilerin erken, paralel arama yapmasi gerektigini belirtir. Ayrica aylik 875-1.300 EUR planlama araligi verir."),
        source(fsr_url, "TU Darmstadt Institute of Flight Systems and Automatic Control", "official_department_page", ["research"], "Official institute page describes application-oriented aerospace systems-engineering research and student thesis/project opportunities in aviation and space topics.", "Resmi enstitu sayfasi uygulama odakli havacilik ve uzay sistem muhendisligi arastirmasini ve havacilik/uzay konularinda ogrenci tez-proje imkanlarini tanimlar."),
        source(propulsion_url, "TU Darmstadt Institute of Gas Turbines and Flight Propulsion", "official_department_page", ["research"], "Official institute page says it specialises in developing and testing turbomachine components using model test rigs and gives students routes into turbomachinery and propulsion work.", "Resmi enstitu sayfasi model test duzenekleriyle turbomakine bilesenleri gelistirme ve testte uzman oldugunu, ogrencilere turbomakine ve itki alaninda imkan sundugunu belirtir."),
        source(celab_url, "TU Darmstadt Concurrent Engineering Lab", "official_industry_partner_page", ["research", "industry"], "Official CELab page says it was established in 2019 as a joint FSR-European Space Agency ESA research laboratory for concurrent engineering, ground segment/operations and student practical experience.", "Resmi CELab sayfasi laboratuvarin 2019'da eszamanli muhendislik, yer segmenti/operasyonlar ve ogrenci uygulamasi icin FSR-Avrupa Uzay Ajansi ESA ortak arastirma laboratuvari olarak kuruldugunu belirtir."),
    ]
    profile = row.setdefault("source_profile", {})
    profile.update({
        "official_program_page": programme_url,
        "official_admission_page": international_admission_url,
        "official_curriculum_page": curriculum_url,
        "official_tuition_page": fee_url,
        "official_scholarship_page": scholarship_url,
        "official_housing_page": housing_url,
        "official_department_page": fsr_url,
        "official_industry_partner_page": celab_url,
        "source_log": log,
        "last_verified": CHECKED,
        "needs_verification": False,
        "verification_notes": bi(
            "All decision fields shown above are tied to checked official sources. The remaining uncertainty is explicit: non-EU eligibility for the Deutschlandstipendium is not stated by the checked call, and the next summer application dates are not extrapolated.",
            "Yukarida gosterilen tum karar alanlari kontrol edilmis resmi kaynaklara baglidir. Kalan belirsizlik aciktir: Deutschlandstipendium icin AB disi uygunluk kontrol edilen cagrida belirtilmez ve sonraki yaz basvuru tarihleri tahmin edilmez.",
        ),
    })
    profile["field_confidence"] = {
        "program_basic_info": "high",
        "language": "high",
        "admission": "high",
        "tuition": "high",
        "scholarship": "high",
        "curriculum": "high",
        "research_profile": "high",
        "industry_ecosystem_profile": "high",
        "application_timeline_profile": "high",
        "living_profile": "high",
        "housing": "high",
        "deadlines": "high",
    }

    newline = "\r\n" if "\r\n" in original else "\n"
    PATH.write_text(json.dumps(rows, ensure_ascii=False, indent=2).replace("\n", newline) + newline, encoding="utf-8")
    print("Updated TU Darmstadt Aerospace Engineering MSc with current official evidence.")


if __name__ == "__main__":
    main()
