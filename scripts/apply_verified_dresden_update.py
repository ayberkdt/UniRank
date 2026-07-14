"""Replace the misleading TU Dresden aerospace record with checked official evidence.

The record is deliberately modelled as a direct-entry Mechanical Engineering
Diplom with an Aerospace specialisation.  It is not represented as a standalone
Master's degree merely because the later study profile is aerospace-focused.
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
    row = next(item for item in rows if item.get("id") == "de_dresden_luft_raumfahrttechnik_diplom")

    programme_url = "https://tu-dresden.de/studium/vor-dem-studium/studienangebot/sins/sins_studiengang?autoid=291"
    language_url = "https://tu-dresden.de/studium/vor-dem-studium/bewerbung/studienvoraussetzungen/sprachkenntnisse"
    tuition_url = "https://tu-dresden.de/studium/im-studium/studienorganisation/semesterbeitrag-studiengebuehren?set_language=en"
    scholarship_url = "https://tu-dresden.de/studium/rund-ums-studium/foerderung-und-finanzierung/deutschlandstipendium/bewerben/index?set_language=en"
    living_url = "https://tu-dresden.de/studium/im-studium/ressourcen/dateien/akademisches-auslandsamt/infomaterialien/Factsheet_TUD_weltweit?lang=en"
    housing_url = "https://www.studentenwerk-dresden.de/english/wohnen/faq-40.html"
    curriculum_url = "https://tu-dresden.de/ing/maschinenwesen/ilr/studium/startseite/?set_language=de"
    research_url = "https://tu-dresden.de/ing/maschinenwesen/ilr/forschung?set_language=de"
    facilities_url = "https://tu-dresden.de/ing/maschinenwesen/ilr/lft/die-professur/einrichtungen"

    row.update({
        "program_name": "Mechanical Engineering Diplom — Aerospace Engineering specialisation (direct-entry)",
        "program_native_name": "Maschinenbau — Vertiefung Luft- und Raumfahrttechnik (Diplom)",
        "program_degree": "Diplom-Ingenieur",
        "degree_level": "Diplom (direct undergraduate degree)",
        "degree_class": "direct-entry integrated degree",
        "duration_years": 5,
        "ects": 300,
        "teaching_language": ["German"],
        "program_url": programme_url,
        "department": "Faculty of Mechanical Science and Engineering / Institute of Aerospace Engineering",
        "faculty_or_school": "Faculty of Mechanical Science and Engineering",
        "campus": "Dresden",
        "program_status": "active",
        "relevance_status": "strong",
    })
    row["eligibility_profile"].update({
        "eligible_for_non_eu": True,
        "required_previous_degree": bi(
            "No previous Bachelor's degree: this is a direct-entry degree. Applicants need a German higher-education entrance qualification (HZB) or a recognised equivalent.",
            "Önceden lisans diploması gerekmez: bu doğrudan girişli bir derecedir. Adayların Alman yükseköğretime giriş yeterliliğine (HZB) veya tanınmış dengine sahip olması gerekir.",
        ),
        "accepted_backgrounds": ["Higher-education entrance qualification (HZB) or recognised foreign equivalent"],
        "admission_mode": "open admission; direct-entry degree (no numerical admission restriction stated)",
        "admission_risk": "high",
        "required_documents": [
            bi("Higher-education entrance qualification evidence (HZB or recognised equivalent)", "Yükseköğretime giriş yeterliliği belgesi (HZB veya tanınmış denkliği)"),
            bi("German-language evidence meeting TU Dresden's university-entry standard", "TU Dresden üniversiteye giriş standardını karşılayan Almanca yeterlilik belgesi"),
        ],
        "verification_notes": bi(
            "This is not an Aerospace MSc and it is not a post-Bachelor programme. The official programme page lists a ten-semester, open-admission Diplom that starts in the first semester in winter; international applicants have a dedicated first-semester application window.",
            "Bu bir Aerospace MSc değildir ve lisans sonrası bir program da değildir. Resmî program sayfası, ilk yarıyılda kış döneminde başlayan, on yarıyıllık ve açık kabulü olan bir Diplom programı listeler; uluslararası adaylar için ilk yarıyıla özel başvuru dönemi bulunur.",
        ),
    })
    row["language_profile"].update({
        "teaching_language": ["German"],
        "english_required": False,
        "english_level_required": None,
        "german_required": True,
        "german_level_required": "University-entry German: DSH-2 overall, TestDaF 4 in every section, or another listed equivalent.",
        "language_risk": "high",
        "verification_notes": bi(
            "The programme page lists German as the teaching language. TU Dresden says international applicants to German-taught degrees need university-entry German evidence with the application; listed examples include DSH-2 and TestDaF 4 in all sections.",
            "Program sayfası eğitim dilini Almanca olarak listeler. TU Dresden, Almanca yürütülen derecelere uluslararası başvurularda üniversiteye giriş düzeyinde Almanca belgesini başvuruyla ister; listelenen örnekler arasında DSH-2 ve tüm bölümlerde TestDaF 4 bulunur.",
        ),
    })
    row["cost_profile"].update({
        "academic_year": "2026/27 planning information; pages checked 2026-07-14",
        "tuition_eur_per_year_min": 0,
        "tuition_eur_per_year_max": 0,
        "tuition_eur_per_year_estimated": 0,
        "tuition_basis": "no_general_tuition_regular_programme",
        "student_contribution_eur": None,
        "student_contribution_eur_approximate": 350,
        "student_contribution_scope_label": bi("TU Dresden 2026/27 exchange fact-sheet planning figure; actual contribution is set per semester", "TU Dresden 2026/27 değişim bilgi notu planlama tutarı; gerçek katkı her dönem belirlenir"),
        "total_academic_cost_eur_per_year_estimated": None,
        "cost_notes": bi(
            "TU Dresden's current fee policy lists tuition only for defined exceptions such as second degrees, long-term study and distance study. The programme page says this regular degree has a semester contribution and may have statutory second-degree/long-term fees. Its current 2026/27 fact sheet gives approximately EUR 350 per semester for planning, not a personal invoice.",
            "TU Dresden'in güncel ücret politikası öğrenim ücretini ikinci derece, uzun süreli öğrenim ve uzaktan eğitim gibi tanımlı istisnalar için listeler. Program sayfası bu düzenli derecede dönem katkısı ve kanuni ikinci derece/uzun süre istisnaları olabileceğini söyler. Güncel 2026/27 bilgi notu planlama için dönem başına yaklaşık 350 EUR verir; bu kişisel fatura değildir.",
        ),
        "verification_notes": bi(
            "Zero means no published general tuition for the regular degree, not a zero-cost study plan. The student contribution and living costs remain payable.",
            "Sıfır, düzenli derece için yayımlanmış genel öğrenim ücreti olmadığı anlamına gelir; sıfır maliyetli eğitim planı anlamına gelmez. Dönem katkısı ve yaşam giderleri yine ödenir.",
        ),
    })
    row["scholarship_profile"].update({
        "regional_scholarship_available": True,
        "regional_scholarship_name": "Deutschlandstipendium at TU Dresden",
        "merit_scholarships": [bi(
            "TU Dresden Deutschlandstipendium: EUR 300 per month for a full academic year. The 2026/27 call says applicants and enrolled students of all nationalities may apply from 1 to 15 July 2026, subject to its enrolment and standard-period conditions.",
            "TU Dresden Deutschlandstipendium: tam akademik yıl boyunca ayda 300 EUR. 2026/27 çağrısı, kayıt ve standart öğrenim süresi koşullarına tabi olarak tüm uyruklardan adayların ve kayıtlı öğrencilerin 1-15 Temmuz 2026 arasında başvurabileceğini söyler.",
        )],
        "tuition_waivers": [],
        "non_eu_eligible": True,
        "scholarship_deadline": "2026-07-15 (TU Dresden Deutschlandstipendium 2026/27 call)",
        "scholarship_application_url": scholarship_url,
        "funding_competitiveness": "high",
        "funding_notes": bi(
            "The official call explicitly allows all nationalities, including applicants who will enrol by the start of winter semester. It is a competitive merit scholarship, not a tuition waiver or guaranteed support.",
            "Resmî çağrı, kış dönemi başlangıcına kadar kayıt olacak adaylar dahil tüm uyruklara açık olduğunu belirtir. Rekabetçi bir başarı bursudur; öğrenim ücreti muafiyeti veya garantili destek değildir.",
        ),
        "verification_notes": bi(
            "Amount, duration, deadline and all-nationalities eligibility are directly stated by TU Dresden's current call.",
            "Tutar, süre, son tarih ve tüm uyruklara uygunluk TU Dresden'in güncel çağrısında doğrudan belirtilir.",
        ),
    })
    row["living_profile"].update({
        "city_cost_level": "medium",
        "monthly_living_cost_eur_min": 900,
        "monthly_living_cost_eur_max": 900,
        "monthly_living_cost_eur_estimated": None,
        "monthly_living_cost_scope_label": bi("TU Dresden 2026/27 general student planning guidance", "TU Dresden 2026/27 genel öğrenci planlama rehberi"),
        "monthly_living_cost_basis": bi(
            "TU Dresden's current 2026/27 fact sheet describes approximately EUR 900/month as the expected cost of living. It is planning guidance, not a guaranteed individual budget.",
            "TU Dresden'in güncel 2026/27 bilgi notu beklenen yaşam maliyetini yaklaşık ayda 900 EUR olarak tanımlar. Bu, garantili kişisel bütçe değil planlama rehberidir.",
        ),
        "average_room_rent_eur": None,
        "average_room_rent_eur_min": 230,
        "average_room_rent_eur_max": 500,
        "average_room_rent_scope_label": bi("TU Dresden 2026/27 accommodation planning guidance", "TU Dresden 2026/27 konaklama planlama rehberi"),
        "student_housing_available": True,
        "student_housing_competitiveness": "high",
        "housing_difficulty": "high",
        "living_risk": "medium",
        "housing_sentiment": None,
        "housing_notes": bi(
            "The official student-services FAQ says applicants can face waiting times of several months, especially for single apartments and at the start of winter semester. It advises applying as early as possible and says no residence place is guaranteed.",
            "Resmî öğrenci hizmetleri SSS'si özellikle tek kişilik dairelerde ve kış dönemi başlangıcında birkaç aylık bekleme süreleri olabileceğini söyler. Mümkün olduğunca erken başvuru önerir ve yurt yerinin garanti edilmediğini belirtir.",
        ),
        "verification_notes": bi(
            "The EUR 230-500 accommodation range and EUR 900 total are current official planning figures. They are shown with their scope and must not be read as a guaranteed dorm price or personal quote.",
            "230-500 EUR konaklama aralığı ve 900 EUR toplam, güncel resmî planlama tutarlarıdır. Kapsamlarıyla gösterilir; garanti yurt fiyatı veya kişisel teklif olarak okunmamalıdır.",
        ),
    })
    row["curriculum_profile"].update({
        "tracks": ["aerospace_engineering"],
        "specializations": ["aerospace_engineering", "spacecraft_systems", "aircraft_design", "space_propulsion", "flight_propulsion", "flight_mechanics"],
        "mandatory_courses": [
            "Mechanical Engineering fundamentals (first two years)",
            "Subject-relevant internship (seventh semester)",
            "Diplom thesis (tenth semester)",
        ],
        "elective_courses": [
            "Aerospace Engineering specialisation after the basic study phase",
            "Space engineering, aircraft engineering and propulsion specialisation content",
            "Aircraft sizing and design, electric propulsion, orbital mechanics and satellite communications foundations",
        ],
        "thesis_required": True,
        "internship_required": True,
        "curriculum_url": curriculum_url,
        "curriculum_structure": bi(
            "This is a five-year continuous degree, not a three-semester MSc. Students complete two years of Mechanical Engineering fundamentals before choosing an Aerospace Engineering specialisation; the programme page places the subject-relevant internship in semester 7 and the Diplom thesis in semester 10.",
            "Bu, üç dönemlik bir MSc değil beş yıllık kesintisiz derecedir. Öğrenciler Havacılık ve Uzay uzmanlaşmasını seçmeden önce iki yıl Makine Mühendisliği temeli tamamlar; program sayfası alanla ilgili stajı 7. yarıyıla, Diplom tezini 10. yarıyıla yerleştirir.",
        ),
        "verification_notes": bi(
            "ILR's official study page explains both the two-year basic-study sequence and the Aerospace specialisation topics. It is not evidence that every topic is compulsory in every individual study plan.",
            "ILR'nin resmî eğitim sayfası hem iki yıllık temel eğitim sırasını hem Havacılık ve Uzay uzmanlaşma konularını açıklar. Bu, her konunun her bireysel öğrenim planında zorunlu olduğunun kanıtı değildir.",
        ),
    })
    row["category_profile"].update({
        "primary_categories": ["aerospace_engineering"],
        "secondary_categories": ["aeronautics", "space_systems", "propulsion", "flight_mechanics", "aircraft_design"],
        "subcategories": ["spacecraft_systems", "space_propulsion", "flight_propulsion", "orbital_mechanics", "satellite_communications"],
        "normalized_tags": ["aircraft_design", "spacecraft_systems", "space_propulsion", "flight_propulsion", "flight_mechanics", "orbital_mechanics", "satellite_communications"],
    })
    row["research_profile"].update({
        "department_research_areas": [
            "Space systems: miniature ion propulsion, altitude-adaptive nozzles, energy and miniaturised gas-sensor systems",
            "Aircraft structures simulation, optimisation and damage tolerance",
            "Flight mechanics, robust control, space-system control and experimental aerodynamics",
            "Planetary infrastructure and habitats for Moon/Mars missions",
        ],
        "labs": ["Institute of Aerospace Engineering (ILR)", "Space Systems Chair", "Aircraft Engineering Chair", "Flight Mechanics and Flight Control Chair", "TU Dresden Cessna 172N research aircraft"],
        "research_centers": [],
        "research_strength_summary": bi(
            "The programme's host ILR has three chairs plus a planetary-infrastructure honorary chair. Its checked research page documents space propulsion and miniaturised systems, aircraft-structure simulation/damage tolerance, flight and space-system control, experimental aerodynamics, and Moon/Mars habitat technologies. The Aircraft Engineering chair also documents a Cessna 172N research aircraft available for research and teaching since May 2023.",
            "Programın bağlı olduğu ILR, üç kürsü ve gezegensel altyapı alanında fahri bir kürsü içerir. Kontrol edilen araştırma sayfası uzay itkisi ve minyatür sistemleri, uçak yapısı simülasyonu/hasar toleransını, uçuş ve uzay sistemi kontrolünü, deneysel aerodinamiği ve Ay/Mars habitat teknolojilerini belgeler. Uçak Mühendisliği kürsüsü ayrıca Mayıs 2023'ten beri araştırma ve eğitim için kullanılabilen Cessna 172N araştırma uçağını belgeliyor.",
        ),
        "research_strength_score": None,
        "research_sources": [research_url, facilities_url],
    })
    row["industry_ecosystem_profile"].update({
        "nearby_companies": [],
        "confirmed_partners": [],
        "research_institutes": [],
        "ecosystem_notes": bi(
            "No programme-specific company or institute partnership is asserted: the checked sources establish research capacity, not a named partnership for this degree.",
            "Programa özgü şirket veya enstitü ortaklığı ileri sürülmez: kontrol edilen kaynaklar bu derece için isimli ortaklık değil araştırma kapasitesi gösterir.",
        ),
        "ecosystem_strength_score": None,
    })
    row["application_timeline_profile"].update({
        "academic_year": "Winter semester 2026/27 application cycle",
        "intake_terms": ["winter semester (first-semester entry)", "winter or summer semester (higher-semester entry only)"],
        "application_rounds": [
            "Non-EU / non-EU-and-non-EEA first semester: 1 April-15 July 2026",
            "EU/EEA with German proof: 1 April-15 September 2026",
            "EU/EEA without German proof: 1 April-15 July 2026",
        ],
        "non_eu_deadline": "2026-07-15 (first-semester winter entry; applications open 2026-04-01)",
        "eu_deadline": "2026-09-15 with German proof; 2026-07-15 without German proof (first-semester winter entry)",
        "winter_deadline": "2026-07-15 for non-EU/non-EEA first-semester applicants (applications open 2026-04-01)",
        "summer_deadline": None,
        "application_deadline": "2026-07-15 (non-EU/non-EEA first-semester winter entry)",
        "timeline_risk": "high",
        "deadline_notes": bi(
            "The published dates apply to first-semester winter entry. The programme page allows higher-semester entry in winter or summer but does not provide a separate current higher-semester date in the checked record; no date is inferred. Non-EU applicants should treat 15 July as a hard deadline.",
            "Yayımlanan tarihler ilk yarıyıl kış dönemi girişi içindir. Program sayfası daha yüksek yarıyıla kış veya yaz girişine izin verir ancak kontrol edilen kayıtta buna özel güncel tarih vermez; tarih tahmin edilmez. AB dışı adaylar 15 Temmuz'u kesin son tarih olarak ele almalıdır.",
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
            "Yeterince belgelenmiş bağımsız öğrenci görüşü örneklemi tutulmadı; duygu puanı gösterilmez.",
        ),
        "verification_notes": bi(
            "Student sentiment remains separate from official facts and is not fabricated to fill the card.",
            "Öğrenci görüşleri resmî bilgilerden ayrı tutulur ve kartı doldurmak için uydurulmaz.",
        ),
    }
    row["decision_summary"].update({
        "main_strengths": [
            bi(
                "A real aerospace route inside a five-year Mechanical Engineering Diplom: two years of engineering fundamentals followed by an Aerospace specialisation, with documented aircraft design, space systems, propulsion, orbital mechanics and satellite-communications content.",
                "Beş yıllık Makine Mühendisliği Diplom içindeki gerçek bir havacılık-uzay rotası: iki yıl mühendislik temeli sonrasında Havacılık ve Uzay uzmanlaşması; uçak tasarımı, uzay sistemleri, itki, yörünge mekaniği ve uydu haberleşmesi içeriği belgelenmiştir.",
            ),
            bi(
                "Research evidence is specific rather than prestige-based: ILR documents space-propulsion and spacecraft-system work, aircraft-structure research, space-system control and experimental aerodynamics; a Cessna research aircraft is available for research and teaching.",
                "Araştırma kanıtı itibara değil somut çalışmaya dayanır: ILR uzay itkisi ve uzay aracı sistemleri, uçak yapıları, uzay sistemi kontrolü ve deneysel aerodinamiği belgeliyor; araştırma ve eğitim için Cessna araştırma uçağı mevcut.",
            ),
        ],
        "main_risks": [
            bi(
                "Do not select this as a Master's applicant: it is a direct-entry ten-semester German Diplom, not a post-Bachelor Aerospace MSc. The full university-entry German standard is a hard practical gate.",
                "Bunu yüksek lisans adayı olarak seçmeyin: lisans sonrası Aerospace MSc değil, doğrudan girişli on yarıyıllık Almanca Diplom'dur. Üniversiteye giriş düzeyindeki Almanca standardı sert bir pratik engeldir.",
            ),
            bi(
                "No general tuition does not make it cost-free. Official 2026/27 planning guidance is about EUR 350 per semester contribution, EUR 230-500 accommodation and about EUR 900 total monthly living cost; accommodation is not guaranteed and waits can take months.",
                "Genel öğrenim ücretinin olmaması programı ücretsiz yapmaz. Resmî 2026/27 planlama rehberi yaklaşık dönem başına 350 EUR katkı, 230-500 EUR konaklama ve toplam ayda yaklaşık 900 EUR yaşam maliyeti verir; konaklama garanti değildir ve bekleme aylar sürebilir.",
            ),
            bi(
                "The quoted first-semester 2026 deadline is 15 July for non-EU/non-EEA applicants. Higher-semester summer entry is possible in principle, but its current date was not published in the checked programme record.",
                "AB dışı/AEA dışı adaylar için belirtilen ilk yarıyıl 2026 son tarihi 15 Temmuz'dur. Daha yüksek yarıyıla yaz girişine ilke olarak izin verilir, ancak güncel tarihi kontrol edilen program kaydında yayımlanmamıştır.",
            ),
        ],
        "best_for": [bi("Applicants seeking a direct, German-taught five-year engineering degree with a later aerospace specialisation.", "Daha sonra havacılık-uzay uzmanlaşması sunan, doğrudan girişli Almanca beş yıllık mühendislik derecesi arayan adaylar.")],
        "not_ideal_for": [bi("Applicants who already hold a Bachelor's degree and need an English-taught Aerospace MSc.", "Halihazırda lisans diploması olan ve İngilizce yürütülen Aerospace MSc arayan adaylar.")],
    })

    # Clear unsupported legacy exports so they cannot resurface outside the card.
    row["financials"] = {"tuition_fee_per_year": None, "semester_fee": None}
    row["scholarships_info"] = []
    row["admission"] = {
        "requirements": {
            "minimum_gpa": None,
            "minimum_gpa_notes": "unknown",
            "required_ects": None,
            "language_requirements": "German university-entry standard: DSH-2, TestDaF 4 in all sections, or listed equivalent.",
        }
    }
    row["urls"] = {"program": programme_url, "admission": programme_url, "tuition": tuition_url, "scholarship": scholarship_url}

    log = [
        source(programme_url, "TU Dresden SINS: Mechanical Engineering Diploma", "official_program_page", ["program", "degree", "language", "admission", "non_eu", "deadline", "curriculum", "fees"], "Current SINS programme record verifies a ten-semester German, open-admission Diplom; first-semester winter entry; Aerospace specialisation; HZB requirement; the 2026 first-semester application windows; a seventh-semester internship; a tenth-semester thesis; and semester contribution/exceptional fee wording.", "Güncel SINS program kaydı on yarıyıllık, Almanca ve açık kabulü olan Diplom'u; ilk yarıyıl kış girişini; Havacılık ve Uzay uzmanlaşmasını; HZB koşulunu; 2026 ilk yarıyıl başvuru aralıklarını; 7. yarıyıl stajını; 10. yarıyıl tezini ve dönem katkısı/istisnai ücret ifadesini doğrular."),
        source(language_url, "TU Dresden German Skills for Studying", "official_admission_page", ["language", "admission"], "Official language guidance requires university-entry German for German-taught degrees and lists DSH-2, TestDaF 4 in every section and stated equivalents; it says an application is not possible without German evidence unless the Master's degree is taught in English.", "Resmî dil rehberi Almanca yürütülen dereceler için üniversiteye giriş düzeyinde Almanca ister ve DSH-2, tüm bölümlerde TestDaF 4 ile belirtilen denklikleri listeler; İngilizce yürütülen bir yüksek lisans istisnası dışında Almanca belgesi olmadan başvurunun mümkün olmadığını söyler."),
        source(tuition_url, "TU Dresden Semester Contribution and Tuition Fees", "official_tuition_page", ["tuition", "fees"], "Current fee policy lists tuition for defined cases including distance study, second degrees and long-term study, supporting the no-general-tuition interpretation for the regular degree while retaining its statutory exceptions.", "Güncel ücret politikası uzaktan eğitim, ikinci derece ve uzun süreli öğrenim gibi tanımlı durumlar için öğrenim ücreti listeler; bu, düzenli derece için genel öğrenim ücreti olmadığı yorumunu desteklerken kanuni istisnaları korur."),
        source(scholarship_url, "TU Dresden Deutschlandstipendium Application", "official_scholarship_page", ["scholarship", "non_eu", "deadline"], "The current 2026/27 call states EUR 300/month for a full academic year, a 1-15 July 2026 window, and eligibility for applicants and enrolled students of all nationalities subject to its conditions.", "Güncel 2026/27 çağrısı tam akademik yıl boyunca ayda 300 EUR'u, 1-15 Temmuz 2026 aralığını ve koşullarına tabi olarak tüm uyruklardan aday/kayıtlı öğrenci uygunluğunu belirtir."),
        source(living_url, "TU Dresden Fact Sheet 2026/27", "official_cost_of_living_page", ["living", "housing", "fees"], "Current official fact sheet gives planning guidance of approximately EUR 900/month living cost, EUR 230-500 accommodation and approximately EUR 350 semester contribution. These are not individual price quotes.", "Güncel resmî bilgi notu yaklaşık 900 EUR/ay yaşam maliyeti, 230-500 EUR konaklama ve yaklaşık 350 EUR dönem katkısı için planlama rehberi verir. Bunlar kişisel fiyat teklifi değildir.", "medium"),
        source(housing_url, "Studentenwerk Dresden Housing FAQ", "official_housing_page", ["housing"], "Official student-services FAQ warns of waiting times of several months, especially for single apartments and at the beginning of winter semester, recommends early application and says a place is not guaranteed.", "Resmî öğrenci hizmetleri SSS'si özellikle tek kişilik dairelerde ve kış dönemi başlangıcında birkaç aylık bekleme olabileceği uyarısını yapar, erken başvuru önerir ve yerin garanti olmadığını belirtir."),
        source(curriculum_url, "TU Dresden ILR Study: Aerospace Engineering Profile", "official_curriculum_page", ["curriculum", "specialisations"], "Official ILR study page states that Mechanical Engineering is a continuous five-year Diplom, with an aerospace specialisation chosen after two years of basics. It names aircraft sizing/design, electric propulsion, orbital mechanics and satellite communications among the knowledge foundations.", "Resmî ILR eğitim sayfası Makine Mühendisliğinin beş yıllık kesintisiz Diplom olduğunu, iki yıllık temelden sonra havacılık-uzay uzmanlaşmasının seçildiğini belirtir. Bilgi temelleri arasında uçak boyutlandırma/tasarım, elektrikli itki, yörünge mekaniği ve uydu haberleşmesini sayar."),
        source(research_url, "TU Dresden Institute of Aerospace Engineering Research", "official_department_page", ["research"], "Official ILR research page documents space-propulsion and miniaturised space systems, aircraft-structure simulation/damage tolerance, flight and space-system control, experimental aerodynamics and planetary-infrastructure research.", "Resmî ILR araştırma sayfası uzay itkisi ve minyatür uzay sistemlerini, uçak yapısı simülasyonu/hasar toleransını, uçuş ve uzay sistemi kontrolünü, deneysel aerodinamiği ve gezegensel altyapı araştırmasını belgeler."),
        source(facilities_url, "TU Dresden Aircraft Engineering Facilities", "official_lab_page", ["research"], "Official facilities page says the Cessna 172N research aircraft has been available for research and teaching since May 2023 and documents other experimental infrastructure.", "Resmî tesis sayfası Cessna 172N araştırma uçağının Mayıs 2023'ten beri araştırma ve eğitim için mevcut olduğunu ve diğer deneysel altyapıyı belgeler."),
    ]
    profile = row.setdefault("source_profile", {})
    profile.update({
        "official_program_page": programme_url,
        "official_admission_page": language_url,
        "official_curriculum_page": curriculum_url,
        "official_tuition_page": tuition_url,
        "official_scholarship_page": scholarship_url,
        "official_housing_page": housing_url,
        "official_department_page": research_url,
        "source_log": log,
        "last_verified": CHECKED,
        "needs_verification": False,
        "verification_notes": bi(
            "All displayed programme, language, admission, fee, scholarship, housing, curriculum and research facts have checked official sources. Living figures are explicitly marked as general planning guidance, and no programme-specific industry partnership is claimed without evidence.",
            "Gösterilen program, dil, kabul, ücret, burs, konaklama, müfredat ve araştırma bilgilerinin tümü kontrol edilmiş resmî kaynaklara sahiptir. Yaşam tutarları açıkça genel planlama rehberi olarak işaretlenir; kanıt olmadan programa özgü sanayi ortaklığı ileri sürülmez.",
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
        "industry_ecosystem_profile": "unknown",
        "application_timeline_profile": "high",
        "living_profile": "medium",
        "housing": "high",
        "deadlines": "high",
    }

    newline = "\r\n" if "\r\n" in original else "\n"
    PATH.write_text(json.dumps(rows, ensure_ascii=False, indent=2).replace("\n", newline) + newline, encoding="utf-8")
    print("Updated TU Dresden direct-entry Aerospace specialisation with current official evidence.")


if __name__ == "__main__":
    main()
