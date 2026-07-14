"""Add source-checked decision data for Politecnico di Milano Space Engineering MSc."""

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
    row = next(item for item in document["universities"] if item.get("id") == "polimi-msc-space")

    programme_url = "https://www.polimi.it/en/education/laurea-programmes/programme-detail/space-engineering"
    curriculum_url = "https://onlineservices.polimi.it/manifesti/manifesti/controller/ManifestoPublic.do?aa=2025&codDescr=057080&k_cf=225&k_corso_la=559&k_indir=%2A&lang=EN&semestre=1"
    foreign_admission_url = "https://www.polimi.it/en/prospective-students/how-to-apply/admission-to-laurea-magistrale/foreign-qualification/application/list-of-documents-required-by-the-admissions-office"
    deadline_url = "https://www.polimi.it/en/prospective-students/how-to-apply/admission-to-laurea-magistrale/foreign-qualification/deadlines"
    language_url = "https://www.polimi.it/en/students/language-requirements/students-of-laurea-magistrale-study-programmes"
    tuition_url = "https://www.polimi.it/en/prospective-students/how-much-does-it-cost/laurea-laurea-magistrale-and-single-cycle-programmes"
    scholarship_url = "https://www.polimi.it/en/prospective-students/how-much-does-it-cost/scholarships"
    living_url = "https://www.polimi.it/en/prospective-students/how-to-apply/on-arrival-information/useful-information"
    housing_url = "https://www.residenze.polimi.it/en/prenotare-tariffa-agevolata/"
    research_url = "https://www.aero.polimi.it/en/research-lines"
    labs_url = "https://www.aero.polimi.it/en/research-labs"
    spire_url = "https://www.aero.polimi.it/en/research-labs/spire-lab-surveillance-and-proximity-operations-research-lab"

    row.update({
        "program_name": "Space Engineering",
        "program_native_name": "Laurea Magistrale in Ingegneria Spaziale",
        "program_degree": "MSc",
        "degree_level": "Master",
        "degree_class": "Laurea Magistrale (LM-20; Master of Science)",
        "duration_years": 2,
        "ects": 120,
        "teaching_language": ["English"],
        "program_url": programme_url,
        "department": "Department of Aerospace Science and Technology (DAER)",
        "faculty_or_school": "School of Industrial and Information Engineering",
        "campus": "Milano Bovisa",
        "program_status": "active",
        "relevance_status": "strong",
    })
    row.setdefault("eligibility_profile", {}).update({
        "eligible_for_non_eu": True,
        "required_previous_degree": bi("A foreign Bachelor's degree comparable to a first-cycle degree.", "Birinci döngü dereceye denk yabancı lisans diploması."),
        "accepted_backgrounds": ["Aerospace Engineering", "Mechanical Engineering", "Closely related engineering degree with adequate mathematics and physics"],
        "required_ects": {"total": None, "note": "No programme-specific ECTS threshold for foreign degrees is published in the checked programme page."},
        "minimum_gpa": None,
        "admission_mode": "International Admissions Office screening followed by programme Department committee evaluation",
        "admission_risk": "medium",
        "required_documents": [
            bi("Bachelor's degree and academic transcript; official translations when originals are not in Italian, English, French or Spanish", "Lisans diploması ve transkript; asıllar İtalyanca, İngilizce, Fransızca veya İspanyolca değilse resmî çeviriler"),
            bi("English-language evidence meeting Polimi's current Master's standard", "Polimi'nin güncel yüksek lisans standardını karşılayan İngilizce yeterlik belgesi"),
        ],
        "verification_notes": bi("The official Space Engineering page requires a comparable foreign Bachelor's degree and evaluates mathematical, physical and aerospace/mechanical preparation. It does not publish a universal numerical CGPA cut-off.", "Resmî Space Engineering sayfası denk yabancı lisans diploması ister ve matematik, fizik ile havacılık/makine altyapısını değerlendirir. Evrensel sayısal CGPA eşiği yayımlamaz."),
    })
    row.setdefault("language_profile", {}).update({
        "teaching_language": ["English"],
        "english_required": True,
        "english_level_required": "B2; current examples include IELTS Academic or General Training ≥ 6.0, subject to Polimi's full accepted-certificates list.",
        "italian_required_for_entry": False,
        "language_risk": "medium",
        "additional_language_notes": bi("Italian is not an entry requirement, but Polimi requires international students in English Master's programmes to demonstrate Italian proficiency before graduation; a free course and exit-test route is offered when a B2 certificate is absent.", "İtalyanca giriş şartı değildir, ancak Polimi İngilizce yüksek lisanslardaki uluslararası öğrencilerin mezuniyet öncesi İtalyanca yeterlik göstermesini ister; B2 belgesi yoksa ücretsiz kurs ve çıkış sınavı yolu sunulur."),
    })
    row.setdefault("cost_profile", {}).update({
        "academic_year": "2026/27",
        "tuition_eur_per_year_min": 880.04,
        "tuition_eur_per_year_max": 3883.04,
        "tuition_eur_per_year_estimated": 3883.04,
        "tuition_basis": "official_non_eu_with_foreign_degree_no_scholarship_maximum",
        "first_installment_eur": 880.04,
        "second_installment_eur_min": 0,
        "second_installment_eur_max": 3003,
        "total_academic_cost_eur_per_year_estimated": 3883.04,
        "cost_notes": bi("For 2026/27, Polimi publishes EUR 880.04 first instalment plus EUR 0-3,003 second instalment for a standard 46-74 ECTS annual plan. Reserved non-EU MSc students with a foreign first-cycle degree pay the maximum unless they are scholarship candidates/recipients; this is not a universal price for every applicant.", "2026/27'de Polimi standart 46-74 AKTS yıllık plan için 880,04 EUR ilk taksit ve 0-3.003 EUR ikinci taksit yayımlar. Yabancı birinci döngü diplomalı ayrılmış kontenjanlı AB dışı MSc öğrencileri burs adayı/alıcı değilse azami tutarı öder; bu her aday için evrensel fiyat değildir."),
        "verification_notes": bi("The amount and non-EU condition are current official tuition evidence; housing and daily costs are separate.", "Tutar ve AB dışı koşul güncel resmî ücret kanıtıdır; konaklama ve günlük giderler ayrıdır."),
    })
    row.setdefault("scholarship_profile", {}).update({
        "regional_scholarship_available": True,
        "regional_scholarship_name": "Politecnico di Milano merit-based international scholarships / DSU financial aid routes",
        "dsu_or_equivalent": "University Financial Aid (DSU); applicant-specific eligibility is not assumed from admission.",
        "merit_scholarships": [bi("Polimi's 2026/27 international merit call: all awards include a full tuition-fee waiver; selected awards add a gross allowance up to EUR 10,000/year.", "Polimi'nin 2026/27 uluslararası başarı çağrısı: tüm ödüller tam öğrenim ücreti muafiyeti içerir; seçilen ödüllerde yılda brüt 10.000 EUR'a kadar ek destek vardır.")],
        "tuition_waivers": ["Full tuition-fee waiver for 2026/27 international merit scholarship awardees"],
        "non_eu_eligible": True,
        "scholarship_deadline": "2026-02-21 (English evidence for 2026/27 merit consideration; Early Bird admission application/payment was 2025-10-01 to 2025-12-01)",
        "scholarship_application_url": scholarship_url,
        "funding_competitiveness": "high",
        "funding_notes": bi("The 2026/27 merit call was for first-year applicants to English MSc programmes who used the 1 October-1 December 2025 Early Bird window. It is closed as of the verification date. DSU aid exists but its current individual eligibility and amount must be checked in the call.", "2026/27 başarı çağrısı, 1 Ekim-1 Aralık 2025 Erken Başvuru penceresini kullanan İngilizce MSc ilk yıl adayları içindi. Doğrulama tarihi itibarıyla kapanmıştır. DSU yardımı vardır, ancak güncel bireysel uygunluk ve tutar çağrıdan kontrol edilmelidir."),
    })
    row.setdefault("living_profile", {}).update({
        "city_cost_level": "high",
        "monthly_living_cost_eur_min": None,
        "monthly_living_cost_eur_max": None,
        "monthly_living_cost_eur_estimated": None,
        "average_room_rent_eur": None,
        "average_room_rent_eur_min": 400,
        "average_room_rent_eur_max": 700,
        "average_room_rent_scope_label": bi("Polimi official Milan accommodation planning guidance", "Polimi resmî Milano konaklama planlama rehberi"),
        "student_housing_available": True,
        "student_housing_competitiveness": "high",
        "housing_difficulty": "high",
        "living_risk": "high",
        "housing_sentiment": None,
        "monthly_living_cost_basis": bi("Polimi publishes approximate component guidance—EUR 400-700/month accommodation, EUR 150-200 food and EUR 100-200 social life—but not one complete monthly total. No incomplete-category total is fabricated.", "Polimi yaklaşık kalem rehberi—ayda 400-700 EUR konaklama, 150-200 EUR yiyecek ve 100-200 EUR sosyal yaşam—yayımlar ancak tek eksiksiz aylık toplam vermez. Eksik kalemlerden toplam uydurulmaz."),
        "housing_notes": bi("The subsidised DSU residence route has 1,349 places across Milan, Lecco, Como and Cremona through an annual call; a place at Milano Bovisa is not guaranteed. Full-rate rooms are a separate availability-based route, so keep a parallel housing plan.", "İndirimli DSU yurt rotasında yıllık çağrıyla Milano, Lecco, Como ve Cremona genelinde 1.349 yer bulunur; Milano Bovisa'da yer garanti değildir. Tam ücretli odalar uygunluğa bağlı ayrı rotadır; paralel konaklama planı tutun."),
        "verification_notes": bi("The official EUR 400-700 figure is scoped accommodation guidance, not a guaranteed rent. An unrelated older programme budget and uncited housing sentiment were removed.", "Resmî 400-700 EUR tutarı kapsamı belirtilmiş konaklama rehberidir, garanti kira değildir. İlgisiz eski program bütçesi ve atıfsız konaklama görüşü kaldırıldı."),
    })
    row.setdefault("curriculum_profile", {}).update({
        "tracks": ["space_engineering"],
        "specializations": ["orbital_mechanics", "spacecraft_attitude_dynamics", "spacecraft_systems", "space_propulsion", "space_structures", "mission_analysis", "satellite_communications", "space_navigation"],
        "mandatory_courses": ["Orbital Mechanics (10 CFU; 2025/26 plan)", "Spacecraft Attitude Dynamics (10 CFU; 2025/26 plan)", "Space Structures (10 CFU; 2025/26 plan)", "Space Propulsion (10 CFU; 2025/26 plan)", "Space Systems Engineering and Operations (8 CFU; 2025/26 plan)"],
        "elective_courses": ["Two complementary first-year electives", "Second-year pathways: platform design/integration, attitude control and advanced orbital dynamics, chemical/electric propulsion, structures/materials, mission analysis/operations, satellite communication/navigation"],
        "thesis_required": True,
        "internship_required": None,
        "curriculum_url": curriculum_url,
        "curriculum_structure": bi("The current 2025/26 official study-plan page names the first-year compulsory Space modules and shows a 20-CFU thesis/final exam. The public 2025/26 programme description gives the second-year technical pathways. Because the next 2026/27 course plan is not published in the checked sources, module-level availability is not extrapolated.", "Güncel 2025/26 resmî ders-planı sayfası ilk yıl zorunlu Uzay modüllerini isimle verir ve 20 AKTS tez/bitirme sınavını gösterir. Kamuya açık 2025/26 program açıklaması ikinci yıl teknik yollarını verir. Sonraki 2026/27 ders planı kontrol edilen kaynaklarda yayımlanmadığı için modül düzeyinde uygunluk tahmin edilmez."),
    })
    row.setdefault("category_profile", {}).update({
        "primary_categories": ["space_systems", "aerospace_engineering"],
        "secondary_categories": ["spacecraft_systems", "orbital_mechanics", "space_propulsion", "gnc", "spacecraft_structures", "satellite_communications"],
        "subcategories": ["space_mission_analysis", "space_operations", "space_surveillance", "in_orbit_servicing"],
        "normalized_tags": ["spacecraft_systems", "orbital_mechanics", "space_propulsion", "spacecraft_attitude_dynamics", "space_structures", "space_mission_analysis", "satellite_communications", "space_navigation"],
    })
    row.setdefault("research_profile", {}).update({
        "department_research_areas": ["Space science and engineering", "Mission analysis and design", "Astrodynamics and trajectory optimisation", "Space debris management and space sustainability", "Autonomous spacecraft guidance/navigation", "Primary and secondary thermochemical propulsion"],
        "labs": ["DART Lab — Deep-space Astrodynamics Research & Technology", "SPIRE Lab — Surveillance and Proximity Operations Research", "ASCL — Aerospace Systems and Control Laboratory", "SPLab — Space Propulsion Laboratory"],
        "research_centers": ["Department of Aerospace Science and Technology (DAER)"],
        "research_strength_summary": bi("DAER's official research lines name mission analysis/design, astrodynamics, space-debris management, autonomous spacecraft guidance/navigation, interplanetary CubeSats and chemical propulsion. The department's lab catalogue includes DART, SPIRE, ASCL and SPLab; SPIRE explicitly works on space-traffic monitoring and in-orbit servicing. These are concrete departmental research signals, not a thesis or lab-placement guarantee.", "DAER'in resmî araştırma alanları görev analizi/tasarımı, astrodinamik, uzay enkazı yönetimi, otonom uzay aracı yönlendirme/navigasyonu, gezegenlerarası CubeSat'ler ve kimyasal itkiyi sayar. Bölümün laboratuvar kataloğu DART, SPIRE, ASCL ve SPLab'ı içerir; SPIRE açıkça uzay trafiği izleme ve yörüngede hizmet çalışmalarını yürütür. Bunlar tez veya laboratuvar yer garantisi değil somut bölüm araştırma sinyalleridir."),
        "research_strength_score": None,
        "research_sources": [research_url, labs_url, spire_url],
    })
    row.setdefault("industry_ecosystem_profile", {}).update({
        "nearby_companies": [], "confirmed_partners": [], "research_institutes": [],
        "ecosystem_notes": bi("The programme permits a thesis with aerospace companies, research centres or international institutions but the checked sources do not establish a named programme partnership or automatic placement. None is claimed.", "Program havacılık-uzay şirketleri, araştırma merkezleri veya uluslararası kurumlarla tez olasılığı verir; ancak kontrol edilen kaynaklar isimli programa özgü ortaklık veya otomatik yerleştirme göstermez. Bu nedenle ileri sürülmez."),
        "ecosystem_strength_score": None,
    })
    row["application_timeline_profile"] = {
        "academic_year": "2026/27 foreign-qualification call cycle",
        "intake_terms": ["September 2026 (first semester)", "February 2027 (second semester; Engineering)"],
        "application_rounds": ["September 2026 Engineering general call 1: 1 October-1 December 2025 (closed)", "September 2026 Engineering general call 2: 13 January-26 February 2026 (closed)", "September 2026 additional call: 27 February-31 March 2026, only EEA and eligible non-EEA residents in Italy (closed)", "February 2027 Engineering general call: 18 May-18 June 2026 (closed)"],
        "non_eu_deadline": "2026-06-18 (February 2027 Engineering general call; closed as of 2026-07-14)",
        "eu_deadline": "2026-06-18 (February 2027 Engineering general call; closed as of 2026-07-14)",
        "winter_deadline": "2026-02-26 (September 2026 Engineering general call 2; closed as of 2026-07-14)",
        "summer_deadline": "2026-06-18 (February 2027 Engineering general call; closed as of 2026-07-14)",
        "application_deadline": "2026-06-18 (last published 2026/27 Engineering general call; closed)",
        "timeline_risk": "high",
        "deadline_notes": bi("All published 2026/27 foreign-degree Engineering calls were closed on the verification date. The 31 March additional call is only for EEA applicants and specified non-EEA residents in Italy, not the normal overseas non-EU route. Future 2027/28 dates are not extrapolated.", "Yayımlanan tüm 2026/27 yabancı diplomalı Mühendislik çağrıları doğrulama tarihinde kapanmıştır. 31 Mart ek çağrısı yalnızca AEA adayları ve İtalya'da belirtilmiş statüde ikamet eden AB dışı adaylar içindir; normal yurtdışı AB dışı rota değildir. Gelecek 2027/28 tarihleri tahmin edilmez."),
    }
    row["student_sentiment_profile"] = {"student_satisfaction_score": None, "sentiment_confidence": "unknown", "sample_size_estimate": None, "date_range": "", "student_sentiment_sources": [], "student_sentiment_summary": bi("No sufficiently documented, independent student-sentiment sample was retained; no sentiment score is shown.", "Yeterince belgelenmiş bağımsız öğrenci görüşü örneklemi tutulmadı; duygu puanı gösterilmez."), "verification_notes": bi("Student sentiment remains separate from official facts and is not fabricated to fill the card.", "Öğrenci görüşleri resmî bilgilerden ayrı tutulur ve kartı doldurmak için uydurulmaz.")}
    row["decision_summary"] = {
        "main_strengths": [bi("A rare dedicated English Space Engineering MSc with an explicitly space-specific first-year core: orbital mechanics, spacecraft attitude dynamics, space structures, propulsion and systems operations.", "Nadir, amaca yönelik İngilizce Space Engineering MSc: açıkça uzaya özgü ilk yıl çekirdeğinde yörünge mekaniği, uzay aracı tutum dinamiği, uzay yapıları, itki ve sistem operasyonları bulunur."), bi("Research depth is specific: DAER lists astrodynamics, space-debris management, spacecraft autonomy, interplanetary CubeSats and propulsion, with DART, SPIRE, ASCL and SPLab as named labs.", "Araştırma derinliği somuttur: DAER astrodinamik, uzay enkazı yönetimi, uzay aracı otonomisi, gezegenlerarası CubeSat'ler ve itkiyi; DART, SPIRE, ASCL ve SPLab'ı isimle listeler.")],
        "main_risks": [bi("Foreign-degree admission is committee-evaluated and no universal numerical CGPA threshold is published. The visible detailed course plan is 2025/26; do not assume each listed module will be unchanged in 2026/27.", "Yabancı diploma kabulü komite değerlendirmelidir ve evrensel sayısal CGPA eşiği yayımlanmamıştır. Görünen ayrıntılı ders planı 2025/26'dır; listelenen her modülün 2026/27'de değişmeden kalacağını varsaymayın."), bi("The published non-EU planning maximum is EUR 3,883.04/year in 2026/27 without scholarship, and official Milan accommodation guidance is EUR 400-700/month. A complete monthly total is not published, so the card does not invent one.", "Burs olmadan yayımlanmış AB dışı planlama azamisi 2026/27'de yıllık 3.883,04 EUR'dur ve resmî Milano konaklama rehberi ayda 400-700 EUR'dur. Eksiksiz aylık toplam yayımlanmadığı için kart bunu uydurmaz."), bi("All published 2026/27 foreign-degree Engineering calls are closed as of the verification date; the international merit scholarship was tied to an earlier Early Bird window.", "Yayımlanan tüm 2026/27 yabancı diplomalı Mühendislik çağrıları doğrulama tarihinde kapanmıştır; uluslararası başarı bursu daha erken Erken Başvuru penceresine bağlıydı.")],
        "best_for": [bi("Applicants seeking spacecraft systems, mission analysis, GNC/attitude dynamics and propulsion in one dedicated English MSc.", "Tek bir İngilizce MSc'de uzay aracı sistemleri, görev analizi, GNC/tutum dinamiği ve itki arayan adaylar.")],
        "not_ideal_for": [bi("Applicants who need a currently open call, an exact all-in monthly Milan budget, or a named guaranteed industry placement.", "Hâlen açık çağrı, kesin toplam aylık Milano bütçesi veya isimli garantili sanayi yerleştirmesi isteyen adaylar.")],
    }
    row["financials"] = {"tuition_fee_per_year": None, "semester_fee": None}
    row["scholarships_info"] = []
    row["admission"] = {"requirements": {"minimum_gpa": None, "minimum_gpa_notes": "unknown", "required_ects": None, "language_requirements": "English B2; see language_profile and checked source log."}}
    row["urls"] = {"program": programme_url, "admission": foreign_admission_url, "tuition": tuition_url, "scholarship": scholarship_url}
    row["source_profile"] = {
        "official_program_page": programme_url, "official_admission_page": foreign_admission_url, "official_curriculum_page": curriculum_url, "official_tuition_page": tuition_url, "official_scholarship_page": scholarship_url, "official_housing_page": housing_url, "official_department_page": research_url,
        "source_log": [
            source(programme_url, "Politecnico di Milano Space Engineering MSc", "official_program_page", ["program", "degree", "duration", "language", "admission", "curriculum"], "Current public programme page verifies a two-year English MSc at Milano Bovisa, its foreign-degree entry framework, space-systems curriculum themes and thesis model.", "Güncel kamuya açık program sayfası Milano Bovisa'da iki yıllık İngilizce MSc'yi, yabancı diplomalı giriş çerçevesini, uzay-sistemleri müfredat temalarını ve tez modelini doğrular."),
            source(curriculum_url, "Polimi Space Engineering 2025/26 Study Plan", "official_curriculum_page", ["curriculum"], "Current 2025/26 official study-plan page names the first-year core modules and the 20-CFU thesis/final exam. It is not used to extrapolate a future 2026/27 module guarantee.", "Güncel 2025/26 resmî ders-planı sayfası ilk yıl çekirdek modüllerini ve 20 AKTS tez/bitirme sınavını isimle verir. Gelecek 2026/27 modül garantisini tahmin etmek için kullanılmaz.", "medium"),
            source(foreign_admission_url, "Polimi Foreign-Qualification Admissions Documents", "official_admission_page", ["admission", "non_eu", "documents", "language"], "Current foreign-admissions page documents qualification comparability, translation rules and English evidence requirements.", "Güncel yabancı kabul sayfası derece denkliğini, çeviri kurallarını ve İngilizce kanıt gerekliliklerini belgeler."),
            source(deadline_url, "Polimi Foreign-Qualification Master Deadlines", "official_admission_page", ["deadline", "non_eu"], "Current Engineering call page publishes each closed 2026/27 September/February window and the restricted additional-call rule.", "Güncel Mühendislik çağrı sayfası kapanmış 2026/27 Eylül/Şubat pencerelerinin her birini ve sınırlı ek çağrı kuralını yayımlar."),
            source(language_url, "Polimi Laurea Magistrale Language Requirements", "official_admission_page", ["language"], "Current 2026/27 Master's page lists B2-equivalent English evidence including IELTS ≥ 6.0 and related current certificate rules.", "Güncel 2026/27 yüksek lisans sayfası IELTS ≥ 6.0 dahil B2 düzeyi İngilizce kanıtını ve ilişkili güncel belge kurallarını listeler."),
            source(tuition_url, "Politecnico di Milano Tuition 2026/27", "official_tuition_page", ["tuition", "fees"], "Current fee page publishes the 2026/27 instalments and reserved non-EU Master's maximum-fee rule used in this record.", "Güncel ücret sayfası bu kayıtta kullanılan 2026/27 taksitleri ve ayrılmış kontenjanlı AB dışı yüksek lisans azami ücret kuralını yayımlar."),
            source(scholarship_url, "Politecnico di Milano International Scholarships 2026/27", "official_scholarship_page", ["scholarship", "funding", "deadline"], "Current scholarship page states full fee waivers, possible gross allowance up to EUR 10,000/year and the closed Early Bird time gate.", "Güncel burs sayfası tam ücret muafiyetini, yılda brüt 10.000 EUR'a kadar olası ek desteği ve kapanmış Erken Başvuru zaman koşulunu belirtir."),
            source(living_url, "Polimi Useful Information: Cost of Living", "official_cost_of_living_page", ["living", "housing"], "Official planning guide publishes approximate component ranges but not a complete monthly total.", "Resmî planlama rehberi yaklaşık kalem aralıklarını yayımlar ancak eksiksiz aylık toplam vermez."),
            source(housing_url, "Polimi Preferential-rate DSU Accommodation", "official_housing_page", ["housing", "scholarship"], "Official residence page states the 1,349 cross-campus subsidised places and annual-call allocation model.", "Resmî yurt sayfası kampüsler arası 1.349 indirimli yeri ve yıllık çağrı atama modelini belirtir."),
            source(research_url, "Polimi DAER Research Lines", "official_department_page", ["research"], "Official DAER page names astrodynamics, space sustainability/debris, autonomous spacecraft guidance/navigation, CubeSats and propulsion research.", "Resmî DAER sayfası astrodinamik, uzay sürdürülebilirliği/enkazı, otonom uzay aracı yönlendirme/navigasyonu, CubeSat ve itki araştırmasını isimle verir."),
            source(labs_url, "Polimi DAER Research Labs", "official_lab_page", ["research"], "Official department lab list identifies DART, SPIRE, ASCL and SPLab among its specific research environments.", "Resmî bölüm laboratuvar listesi somut araştırma ortamları arasında DART, SPIRE, ASCL ve SPLab'ı tanımlar."),
            source(spire_url, "Polimi SPIRE Lab", "official_lab_page", ["research"], "Official SPIRE page describes work on space-traffic monitoring and in-orbit satellite servicing.", "Resmî SPIRE sayfası uzay trafiği izleme ve yörüngede uydu hizmeti çalışmalarını açıklar."),
        ],
        "last_verified": CHECKED, "needs_verification": False,
        "verification_notes": bi("All shown critical decision fields have checked official sources. The next 2026/27 course-by-course plan, a complete monthly budget and a named programme-specific industry placement are not claimed where not published.", "Gösterilen kritik karar alanlarının tümü kontrol edilmiş resmî kaynaklara sahiptir. Sonraki 2026/27 ders-ders planı, eksiksiz aylık bütçe ve isimli programa özgü sanayi yerleştirmesi yayımlanmadığı yerde ileri sürülmez."),
        "field_confidence": {"program_basic_info": "high", "language": "high", "admission": "high", "tuition": "high", "scholarship": "high", "curriculum": "medium", "research_profile": "high", "industry_ecosystem_profile": "unknown", "application_timeline_profile": "high", "living_profile": "high", "housing": "high", "deadlines": "high"},
    }
    document["last_updated"] = CHECKED
    newline = "\r\n" if "\r\n" in original else "\n"
    PATH.write_text(json.dumps(document, ensure_ascii=False, indent=2).replace("\n", newline) + newline, encoding="utf-8")
    print("Updated Politecnico di Milano Space Engineering MSc with current official evidence.")


if __name__ == "__main__":
    main()
