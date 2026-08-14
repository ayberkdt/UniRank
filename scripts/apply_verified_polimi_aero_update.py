"""Synchronise both Politecnico di Milano Aeronautical MSc records with official evidence.

The repository currently carries one record in each of two Italy datasets.  The
same checked facts are applied to both, avoiding two conflicting answers for a
single university-programme pair.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PATHS = (
    (ROOT / "data_base" / "italy.json", "polimi-msc-aeronautical", True),
)
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


def update_row(row: dict[str, Any]) -> None:
    programme_url = "https://www.polimi.it/en/education/laurea-programmes/programme-detail/aeronautical-engineering"
    regulation_url = "https://onlineservices.polimi.it/manifesti/manifesti/controller/extra/RegolamentoPublic.do?EVN_DEFAULT=evento&aa=2026&jaf_currentWFID=main&k_corso_la=536&lang=EN"
    foreign_admission_url = "https://www.polimi.it/en/prospective-students/how-to-apply/admission-to-laurea-magistrale/foreign-qualification/application/list-of-documents-required-by-the-admissions-office"
    deadline_url = "https://www.polimi.it/en/prospective-students/how-to-apply/admission-to-laurea-magistrale/foreign-qualification/deadlines"
    language_url = "https://www.polimi.it/en/students/language-requirements/students-of-laurea-magistrale-study-programmes"
    tuition_url = "https://www.polimi.it/en/prospective-students/how-much-does-it-cost/laurea-laurea-magistrale-and-single-cycle-programmes"
    scholarship_url = "https://www.polimi.it/en/prospective-students/how-much-does-it-cost/scholarships"
    living_url = "https://www.polimi.it/en/prospective-students/how-to-apply/on-arrival-information/useful-information"
    housing_url = "https://www.residenze.polimi.it/en/prenotare-tariffa-agevolata/"
    research_url = "https://www.aero.polimi.it/en/research-lines"
    labs_url = "https://www.aero.polimi.it/en/research-labs"

    row.update({
        "program_name": "Aeronautical Engineering",
        "program_native_name": "Laurea Magistrale in Ingegneria Aeronautica",
        "program_degree": "MSc",
        "degree_level": "Master",
        "degree_class": "Laurea Magistrale (Master of Science)",
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
        "required_previous_degree": bi(
            "A foreign Bachelor's degree comparable to a first-cycle degree is required.",
            "Birinci döngü dereceye denk yabancı bir lisans diploması gereklidir.",
        ),
        "accepted_backgrounds": ["Aerospace Engineering", "Mechanical Engineering", "Closely related engineering degree with adequate mathematics and physics"],
        "required_ects": {"total": None, "note": "No programme-specific ECTS threshold for foreign degrees is published in the checked programme page."},
        "minimum_gpa": None,
        "admission_mode": "International Admissions Office screening followed by programme Department committee evaluation",
        "admission_risk": "medium",
        "required_documents": [
            bi("Bachelor's degree and academic transcript; official translations when the originals are not in Italian, English, French or Spanish", "Lisans diploması ve transkript; asıllar İtalyanca, İngilizce, Fransızca veya İspanyolca değilse resmî çeviriler"),
            bi("English-language evidence meeting Polimi's current Master's standard", "Polimi'nin güncel yüksek lisans standardını karşılayan İngilizce yeterlik belgesi"),
        ],
        "verification_notes": bi(
            "For a non-Italian degree, Polimi requires a Bachelor's degree comparable to a first-cycle degree and evaluates both qualification comparability and the fit of mathematics, physics and aerospace/mechanical-engineering preparation. The programme committee reviews the academic curriculum and performance; no universal numerical CGPA cut-off is claimed.",
            "İtalyan olmayan diploma için Polimi, birinci döngü dereceye denk lisans diploması ister ve hem denklik hem de matematik, fizik ve havacılık/makine mühendisliği altyapısının uyumunu değerlendirir. Program komitesi akademik özgeçmişi ve başarıyı inceler; evrensel sayısal CGPA eşiği ileri sürülmez.",
        ),
    })
    row.setdefault("language_profile", {}).update({
        "teaching_language": ["English"],
        "english_required": True,
        "english_level_required": "B2; current examples include IELTS Academic or General Training ≥ 6.0, subject to Polimi's full accepted-certificates list.",
        "italian_required_for_entry": False,
        "language_risk": "medium",
        "additional_language_notes": bi(
            "Italian is not an entry requirement for this English MSc. However, Polimi says international students on English Laurea Magistrale programmes must demonstrate Italian proficiency before graduation; students without a B2 certificate may use the university's free course and exit test route.",
            "İtalyanca bu İngilizce MSc için giriş şartı değildir. Ancak Polimi, İngilizce Laurea Magistrale programlarındaki uluslararası öğrencilerin mezuniyetten önce İtalyanca yeterlik göstermesi gerektiğini söyler; B2 belgesi olmayanlar üniversitenin ücretsiz kursu ve çıkış sınavı yolunu kullanabilir.",
        ),
        "verification_notes": bi(
            "The current 2026/27 Master's language page directly lists B2-equivalent English evidence. A Bachelor's degree taught at least 75% in English for at least three years is also listed as a possible certificate exemption; applicants should check the full current rule.",
            "Güncel 2026/27 yüksek lisans dil sayfası B2 düzeyine denk İngilizce kanıtını doğrudan listeler. En az üç yıl boyunca en az %75 İngilizce yürütülen lisans diploması da olası belge muafiyeti olarak listelenir; adaylar tam güncel kuralı kontrol etmelidir.",
        ),
    })
    # The checked 2026/27 Polimi fee page supplies the figures already present
    # in these records. Re-state their scope instead of treating the maximum as
    # a generic EU/EEA price.
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
        "cost_notes": bi(
            "For 2026/27, Polimi publishes a EUR 880.04 first instalment and a EUR 0-3,003 second instalment for a standard 46-74 ECTS annual study plan. The page says reserved non-EU MSc students with a foreign first-cycle degree pay the maximum unless they are scholarship candidates/recipients. This maximum is a current non-EU planning amount, not a universal price for every applicant.",
            "2026/27 için Polimi, standart 46-74 AKTS yıllık öğrenim planında 880,04 EUR ilk taksit ve 0-3.003 EUR ikinci taksit yayımlar. Sayfa, yabancı birinci döngü diplomalı ayrılmış kontenjanlı AB dışı MSc öğrencilerinin burs adayı/alıcı olmadıkça azami tutarı ödediğini söyler. Bu azami tutar, her aday için evrensel fiyat değil güncel AB dışı planlama tutarıdır.",
        ),
        "verification_notes": bi(
            "The amounts, academic year and the specific reserved non-EU rule come from Polimi's checked 2026/27 tuition page. Housing and everyday costs are shown separately.",
            "Tutarlar, akademik yıl ve ayrılmış kontenjanlı AB dışı kuralı Polimi'nin kontrol edilmiş 2026/27 ücret sayfasından gelir. Konaklama ve günlük giderler ayrı gösterilir.",
        ),
    })
    row.setdefault("scholarship_profile", {}).update({
        "regional_scholarship_available": True,
        "regional_scholarship_name": "Politecnico di Milano merit-based international scholarships / DSU financial aid routes",
        "dsu_or_equivalent": "University Financial Aid (DSU); eligibility is application-specific and not assumed from admission.",
        "merit_scholarships": [bi(
            "Polimi's 2026/27 international merit call: all awards include a full tuition-fee waiver; selected awards also include a gross allowance up to EUR 10,000/year.",
            "Polimi'nin 2026/27 uluslararası başarı çağrısı: tüm ödüller tam öğrenim ücreti muafiyeti içerir; seçilen ödüllerde yılda brüt 10.000 EUR'a kadar ek destek de bulunur.",
        )],
        "tuition_waivers": ["Full tuition-fee waiver for the 2026/27 international merit scholarship awardees"],
        "non_eu_eligible": True,
        "scholarship_deadline": "2026-02-21 (English evidence for 2026/27 merit-scholarship consideration; Early Bird admission application/payment was 2025-10-01 to 2025-12-01)",
        "scholarship_application_url": scholarship_url,
        "funding_competitiveness": "high",
        "funding_notes": bi(
            "For the 2026/27 merit call, eligibility was limited to first-year applicants to English-taught MSc programmes who applied and paid the Early Bird fee between 1 October and 1 December 2025; valid English proof was due by 21 February 2026. As of the verification date this route is closed for 2026/27. DSU support exists, but its individual eligibility and benefit level must be checked in the current call.",
            "2026/27 başarı çağrısında uygunluk, 1 Ekim-1 Aralık 2025 arasında Erken Başvuru yapıp ücret ödemiş İngilizce MSc ilk yıl adaylarıyla sınırlıydı; geçerli İngilizce belgesi 21 Şubat 2026'da gerekliydi. Doğrulama tarihi itibarıyla bu rota 2026/27 için kapanmıştır. DSU desteği vardır, ancak bireysel uygunluk ve destek tutarı güncel çağrıdan kontrol edilmelidir.",
        ),
        "verification_notes": bi(
            "The scholarship page explicitly publishes the scope, fee waiver, possible allowance and time gate. It does not make every admitted student a scholarship recipient.",
            "Burs sayfası kapsamı, ücret muafiyetini, olası ek desteği ve zaman koşulunu açıkça yayımlar. Bu, kabul alan her öğrencinin burs alacağı anlamına gelmez.",
        ),
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
        "monthly_living_cost_basis": bi(
            "Polimi does not publish one complete monthly total on the checked page. It publishes EUR 400-700/month accommodation, EUR 150-200/month food and EUR 100-200/month social-life guidance, all explicitly approximate; no misleading total is calculated from incomplete categories.",
            "Polimi kontrol edilen sayfada tek bir eksiksiz aylık toplam yayımlamaz. Açıkça yaklaşık olmak üzere 400-700 EUR/ay konaklama, 150-200 EUR/ay yiyecek ve 100-200 EUR/ay sosyal yaşam rehberi yayımlar; eksik kalemlerden yanıltıcı toplam hesaplanmaz.",
        ),
        "housing_notes": bi(
            "Polimi's subsidised DSU residence route has 1,349 places across Milan, Lecco, Como and Cremona; places are assigned through an annual public call and are not a Milan-Bovisa guarantee. Full-rate rooms are separately bookable subject to availability. Budget for a private/shared room and keep a parallel housing plan.",
            "Polimi'nin indirimli DSU yurt rotasında Milano, Lecco, Como ve Cremona genelinde 1.349 yer bulunur; yerler yıllık kamu çağrısıyla atanır ve Milano-Bovisa garantisi değildir. Tam ücretli odalar da uygunluğa bağlı olarak ayrı rezerve edilir. Özel/paylaşımlı oda için bütçe ayırın ve paralel konaklama planı yürütün.",
        ),
        "verification_notes": bi(
            "The published EUR 400-700 amount is accommodation guidance rather than a guaranteed rent. It is displayed as a scoped range; the missing complete monthly budget remains unknown.",
            "Yayımlanan 400-700 EUR tutarı, garanti kira değil konaklama rehberidir. Kapsamı belirtilmiş aralık olarak gösterilir; eksik olan tam aylık bütçe bilinmiyor kalır.",
        ),
    })
    row.setdefault("curriculum_profile", {}).update({
        "tracks": ["aeronautical_engineering"],
        "specializations": ["aerodynamics", "aerospace_structures", "aeroelasticity", "flight_dynamics", "aircraft_systems", "aerospace_propulsion"],
        "mandatory_courses": ["Atmospheric flight dynamics", "Aerodynamics", "Aerospace structures", "Aeroelasticity"],
        "elective_courses": ["One aeronautical core module and two complementary modules in the first year", "Second-year individual pathway across core and multidisciplinary subjects", "Technical writing, presentation and aeronautics research-methodology modules"],
        "thesis_required": True,
        "internship_required": None,
        "curriculum_url": regulation_url,
        "curriculum_structure": bi(
            "The official programme description gives a two-year MSc with four first-year compulsory modules (atmospheric flight dynamics, aerodynamics, aerospace structures and aeroelasticity), then a more individual second-year pathway. It concludes with a design-oriented or research-based Master's thesis; collaboration with a company, research centre or institution is possible, not stated as compulsory.",
            "Resmî program açıklaması, ilk yılda dört zorunlu modül (atmosferik uçuş dinamiği, aerodinamik, havacılık-uzay yapıları ve aeroelastisite) içeren iki yıllık MSc'yi; ardından daha bireysel ikinci yıl yolunu verir. Tasarım odaklı veya araştırma temelli yüksek lisans teziyle biter; şirket, araştırma merkezi veya kurumla iş birliği mümkündür ancak zorunlu olarak belirtilmez.",
        ),
        "verification_notes": bi(
            "The main programme page and the 2026/27 regulation support these course-structure statements. Individual second-year availability must still be checked in the current study plan.",
            "Ana program sayfası ve 2026/27 yönetmeliği bu ders-yapısı ifadelerini destekler. Bireysel ikinci yıl ders uygunluğu yine güncel çalışma planından kontrol edilmelidir.",
        ),
    })
    row.setdefault("category_profile", {}).update({
        "primary_categories": ["aerospace_engineering", "aeronautics"],
        "secondary_categories": ["aerodynamics", "aerospace_structures", "flight_mechanics", "propulsion", "aircraft_systems"],
        "subcategories": ["aeroelasticity", "flight_dynamics", "aircraft_design"],
        "normalized_tags": ["aerodynamics", "aerospace_structures", "aeroelasticity", "flight_mechanics", "aircraft_systems", "aerospace_propulsion", "aircraft_design"],
    })
    row.setdefault("research_profile", {}).update({
        "department_research_areas": [
            "Aerospace structures, materials and technologies",
            "Aircraft and rotorcraft design, aerodynamics, dynamics and control",
            "Fluid dynamics, computational engineering and energy conversion",
            "Space science and engineering",
        ],
        "labs": ["Aerodynamic Laboratory", "ASDL — Aero-Structural Design Laboratory", "AVLab — Aeroelasticity and Vibroacoustic Laboratory", "FMSlab — Flight Mechanics & Flight Systems Laboratory", "SPLab — Space Propulsion Laboratory"],
        "research_centers": ["Department of Aerospace Science and Technology (DAER)"],
        "research_strength_summary": bi(
            "DAER's checked research taxonomy includes structures/materials, aircraft and rotorcraft design, aerodynamics, flight dynamics/control, CFD and energy conversion, and space science. Its lab list specifically identifies aerostructures, aeroelasticity/vibroacoustics, flight mechanics/systems and space propulsion. This is department-level research access, not a promise of a place in a particular lab.",
            "DAER'in kontrol edilen araştırma sınıflandırması yapılar/malzemeler, uçak ve rotorcraft tasarımı, aerodinamik, uçuş dinamiği/kontrolü, HAD ve enerji dönüşümü ile uzay bilimini içerir. Laboratuvar listesi özellikle havacılık yapıları, aeroelastisite/vibroakustik, uçuş mekaniği/sistemleri ve uzay itkisini tanımlar. Bu, belirli bir laboratuvarda yer garantisi değil bölüm düzeyinde araştırma erişimidir.",
        ),
        "research_strength_score": None,
        "research_sources": [research_url, labs_url],
    })
    row.setdefault("industry_ecosystem_profile", {}).update({
        "nearby_companies": [],
        "confirmed_partners": [],
        "research_institutes": [],
        "ecosystem_notes": bi(
            "The programme page permits a thesis in collaboration with aerospace companies, research centres or international institutions, but the checked sources do not establish a named programme partnership or an automatic placement. No company is presented as a guaranteed partner.",
            "Program sayfası havacılık-uzay şirketleri, araştırma merkezleri veya uluslararası kurumlarla ortak tez olasılığı verir; ancak kontrol edilen kaynaklar isimli programa özgü ortaklık veya otomatik yerleştirme göstermez. Hiçbir şirket garantili ortak olarak sunulmaz.",
        ),
        "ecosystem_strength_score": None,
    })
    row["application_timeline_profile"] = {
        "academic_year": "2026/27 foreign-qualification call cycle",
        "intake_terms": ["September 2026 (first semester)", "February 2027 (second semester; Engineering)"] ,
        "application_rounds": [
            "September 2026 Engineering general call 1: 1 October-1 December 2025 (closed)",
            "September 2026 Engineering general call 2: 13 January-26 February 2026 (closed)",
            "September 2026 additional call: 27 February-31 March 2026, only EEA and eligible non-EEA residents in Italy (closed)",
            "February 2027 Engineering general call: 18 May-18 June 2026 (closed)",
        ],
        "non_eu_deadline": "2026-06-18 (February 2027 Engineering general call; closed as of 2026-07-14)",
        "eu_deadline": "2026-06-18 (February 2027 Engineering general call; closed as of 2026-07-14)",
        "winter_deadline": "2026-02-26 (September 2026 Engineering general call 2; closed as of 2026-07-14)",
        "summer_deadline": "2026-06-18 (February 2027 Engineering general call; closed as of 2026-07-14)",
        "application_deadline": "2026-06-18 (last published 2026/27 Engineering general call; closed)",
        "timeline_risk": "high",
        "deadline_notes": bi(
            "These are the official published 2026/27 foreign-degree Engineering calls, all already closed on the verification date. The 31 March additional September call is not a normal non-EU route: it is limited to EEA applicants and specified non-EEA residents in Italy. Future 2027/28 dates are not yet inferred. Admitted visa applicants must also complete the Italian-government visa request by 30 November 2026 for this academic year.",
            "Bunlar resmî yayımlanmış 2026/27 yabancı diplomalı Mühendislik çağrılarıdır ve doğrulama tarihinde hepsi kapanmıştır. 31 Mart ek Eylül çağrısı normal AB dışı rota değildir: AEA adayları ve İtalya'da belirtilmiş statüde ikamet eden AB dışı adaylarla sınırlıdır. Gelecek 2027/28 tarihleri tahmin edilmez. Kabul alan vize adayları bu akademik yıl için İtalyan devletinin vize talebini ayrıca 30 Kasım 2026'ya kadar tamamlamalıdır.",
        ),
    }
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
    row["decision_summary"] = {
        "main_strengths": [
            bi("A dedicated, English two-year Aeronautical Engineering MSc with explicit core work in flight dynamics, aerodynamics, structures and aeroelasticity before a flexible second year and thesis.", "Uçuş dinamiği, aerodinamik, yapılar ve aeroelastisite alanlarında açık çekirdek içeriği olan; esnek ikinci yıl ve tezle tamamlanan, amaca yönelik İngilizce iki yıllık Aeronautical Engineering MSc."),
            bi("DAER research evidence is concrete: aerostructures, aeroelasticity/vibroacoustics, flight mechanics/systems, CFD and space-propulsion labs are named in the official department sources.", "DAER araştırma kanıtı somuttur: resmî bölüm kaynakları havacılık yapıları, aeroelastisite/vibroakustik, uçuş mekaniği/sistemleri, HAD ve uzay itkisi laboratuvarlarını isimle verir."),
        ],
        "main_risks": [
            bi("Admission is committee-evaluated. A foreign Bachelor's degree must be comparable and the mathematical, physical and aerospace/mechanical foundation must fit; no universal CGPA threshold is published.", "Kabul komite değerlendirmelidir. Yabancı lisans diploması denk olmalı ve matematik, fizik ile havacılık/makine altyapısı uyum göstermelidir; evrensel CGPA eşiği yayımlanmamıştır."),
            bi("For a reserved non-EU MSc applicant with a foreign first-cycle degree and no scholarship, the published 2026/27 planning maximum is EUR 3,883.04/year. Milan accommodation alone is officially guided at EUR 400-700/month, while Polimi does not publish one complete monthly total.", "Yabancı birinci döngü diplomalı ve bursu olmayan ayrılmış kontenjanlı AB dışı MSc adayı için yayımlanmış 2026/27 planlama azamisi yıllık 3.883,04 EUR'dur. Polimi tek eksiksiz aylık toplam yayımlamazken Milano konaklaması tek başına resmî rehberde ayda 400-700 EUR'dur."),
            bi("All published 2026/27 foreign-degree Engineering calls are closed at the verification date. The attractive international merit scholarship was also tied to a much earlier Early Bird window; do not budget it as still open.", "Yayımlanmış tüm 2026/27 yabancı diplomalı Mühendislik çağrıları doğrulama tarihinde kapanmıştır. Cazip uluslararası başarı bursu da çok daha erken Erken Başvuru penceresine bağlıydı; hâlâ açıkmış gibi bütçelenmemelidir."),
        ],
        "best_for": [bi("Applicants with a strong aerospace/mechanical Bachelor's background seeking aircraft-focused MSc depth in English.", "İngilizce uçak odaklı MSc derinliği arayan, güçlü havacılık/makine lisans altyapılı adaylar.")],
        "not_ideal_for": [bi("Applicants who need a guaranteed current open call, a low Milan housing budget, or a named guaranteed industry placement.", "Hâlen açık garantili başvuru çağrısı, düşük Milano konaklama bütçesi veya isimli garantili sanayi yerleştirmesi isteyen adaylar.")],
    }
    row["financials"] = {"tuition_fee_per_year": None, "semester_fee": None}
    row["scholarships_info"] = []
    row["admission"] = {"requirements": {"minimum_gpa": None, "minimum_gpa_notes": "unknown", "required_ects": None, "language_requirements": "English B2; see language_profile and the checked source log."}}
    row["urls"] = {"program": programme_url, "admission": foreign_admission_url, "tuition": tuition_url, "scholarship": scholarship_url}

    log = [
        source(programme_url, "Politecnico di Milano Aeronautical Engineering MSc", "official_program_page", ["program", "degree", "duration", "language", "admission", "curriculum"], "Current programme page verifies a two-year English MSc at Milano Bovisa; its academic scope, foreign-degree entry framework, compulsory first-year subjects, second-year flexibility and thesis options.", "Güncel program sayfası Milano Bovisa'da iki yıllık İngilizce MSc'yi; akademik kapsamını, yabancı diplomalı giriş çerçevesini, zorunlu ilk yıl derslerini, ikinci yıl esnekliğini ve tez seçeneklerini doğrular."),
        source(regulation_url, "Politecnico di Milano Aeronautical Engineering 2026/27 Academic Regulation", "official_curriculum_page", ["curriculum", "admission"], "The checked 2026/27 regulation supports the programme's 120-CFU two-year structure, curriculum rules and degree-evaluation framework.", "Kontrol edilen 2026/27 yönetmeliği programın 120 AKTS'lik iki yıllık yapısını, müfredat kurallarını ve derece değerlendirme çerçevesini destekler."),
        source(foreign_admission_url, "Polimi Foreign-Qualification Admissions Documents", "official_admission_page", ["admission", "non_eu", "documents", "language"], "Current international-admissions page describes foreign degree comparability, document/translation requirements and current English evidence rules for Master's applicants.", "Güncel uluslararası kabul sayfası yabancı diploma denkliğini, belge/çeviri gerekliliklerini ve yüksek lisans adayları için güncel İngilizce kanıt kurallarını açıklar."),
        source(deadline_url, "Polimi Foreign-Qualification Master Deadlines", "official_admission_page", ["deadline", "non_eu"], "Current Engineering call page publishes the closed 2026/27 September and February windows and distinguishes the EEA/eligible-resident additional call from general calls.", "Güncel Mühendislik çağrı sayfası kapanmış 2026/27 Eylül ve Şubat pencerelerini yayımlar; AEA/uygun ikametli ek çağrısını genel çağrılardan ayırır."),
        source(language_url, "Polimi Laurea Magistrale Language Requirements", "official_admission_page", ["language"], "Current 2026/27 Master's language page lists B2-equivalent English evidence, including IELTS ≥ 6.0, and the associated accepted-certificate rules.", "Güncel 2026/27 yüksek lisans dil sayfası IELTS ≥ 6.0 dahil B2 düzeyi İngilizce kanıtını ve ilişkili kabul edilen belge kurallarını listeler."),
        source(tuition_url, "Politecnico di Milano Tuition 2026/27", "official_tuition_page", ["tuition", "fees"], "The current page publishes the EUR 880.04 first instalment, EUR 0-3,003 second instalment for a standard annual plan and the maximum-fee rule for reserved non-EU MSc students with a foreign first-cycle degree who are not scholarship candidates/recipients.", "Güncel sayfa 880,04 EUR ilk taksiti, standart yıllık plan için 0-3.003 EUR ikinci taksiti ve burs adayı/alıcı olmayan yabancı birinci döngü diplomalı ayrılmış kontenjanlı AB dışı MSc öğrencileri için azami ücret kuralını yayımlar."),
        source(scholarship_url, "Politecnico di Milano International Scholarships 2026/27", "official_scholarship_page", ["scholarship", "funding", "deadline"], "Current scholarship page states that all merit awards include a full fee waiver, selected awards can add up to EUR 10,000/year gross, and records the Early Bird and language-evidence time conditions.", "Güncel burs sayfası tüm başarı ödüllerinin tam ücret muafiyeti içerdiğini, seçilen ödüllerde yılda brüt 10.000 EUR'a kadar ek destek olabileceğini ve Erken Başvuru/dil kanıtı zaman koşullarını belirtir."),
        source(living_url, "Polimi Useful Information: Cost of Living", "official_cost_of_living_page", ["living", "housing"], "Official guidance labels the figures approximate and gives EUR 400-700/month accommodation, EUR 150-200 food and EUR 100-200 social-life planning ranges; it does not publish one complete total.", "Resmî rehber tutarları yaklaşık olarak etiketler ve ayda 400-700 EUR konaklama, 150-200 EUR yiyecek ve 100-200 EUR sosyal yaşam planlama aralıklarını verir; tek eksiksiz toplam yayımlamaz."),
        source(housing_url, "Polimi Preferential-rate DSU Accommodation", "official_housing_page", ["housing", "scholarship"], "Official residence page says 1,349 subsidised places are available across the university's campuses through an annual public call; allocation is competitive and campus-specific availability is not guaranteed.", "Resmî yurt sayfası yıllık kamu çağrısıyla üniversitenin kampüsleri genelinde 1.349 indirimli yer olduğunu belirtir; yerleştirme rekabetçidir ve kampüse özgü uygunluk garanti değildir."),
        source(research_url, "Polimi DAER Research Lines", "official_department_page", ["research"], "Official DAER research taxonomy identifies aerospace structures/materials, aircraft/rotorcraft design, aerodynamics, dynamics/control, CFD/energy conversion and space science/engineering.", "Resmî DAER araştırma sınıflandırması havacılık-uzay yapıları/malzemeleri, uçak/rotorcraft tasarımı, aerodinamik, dinamik/kontrol, HAD/enerji dönüşümü ve uzay bilimi/mühendisliğini tanımlar."),
        source(labs_url, "Polimi DAER Research Labs", "official_lab_page", ["research"], "Official department page lists 18 scientific labs, including ASDL, AVLab, FMSlab and SPLab, which are specific research signals rather than a generic ranking claim.", "Resmî bölüm sayfası ASDL, AVLab, FMSlab ve SPLab dahil 18 bilimsel laboratuvarı listeler; bunlar genel sıralama iddiası değil somut araştırma sinyalleridir."),
    ]
    row["source_profile"] = {
        "official_program_page": programme_url,
        "official_admission_page": foreign_admission_url,
        "official_curriculum_page": regulation_url,
        "official_tuition_page": tuition_url,
        "official_scholarship_page": scholarship_url,
        "official_housing_page": housing_url,
        "official_department_page": research_url,
        "source_log": log,
        "last_verified": CHECKED,
        "needs_verification": False,
        "verification_notes": bi(
            "All displayed programme, admission, language, current fee, scholarship, deadline, housing and research facts are grounded in checked official sources. The complete monthly living budget and a named programme-specific industry placement are not published by these sources and are left unclaimed.",
            "Gösterilen program, kabul, dil, güncel ücret, burs, son tarih, konaklama ve araştırma bilgilerinin tümü kontrol edilmiş resmî kaynaklara dayanır. Bu kaynaklarda tam aylık yaşam bütçesi ve isimli programa özgü sanayi yerleştirmesi yayımlanmadığı için ileri sürülmez.",
        ),
        "field_confidence": {
            "program_basic_info": "high", "language": "high", "admission": "high", "tuition": "high", "scholarship": "high", "curriculum": "high", "research_profile": "high", "industry_ecosystem_profile": "unknown", "application_timeline_profile": "high", "living_profile": "high", "housing": "high", "deadlines": "high",
        },
    }


def main() -> None:
    for path, record_id, is_wrapped in PATHS:
        original = path.read_text(encoding="utf-8")
        document: Any = json.loads(original)
        rows = document["universities"] if is_wrapped else document
        update_row(next(item for item in rows if item.get("id") == record_id))
        if is_wrapped:
            document["last_updated"] = CHECKED
        newline = "\r\n" if "\r\n" in original else "\n"
        path.write_text(json.dumps(document, ensure_ascii=False, indent=2).replace("\n", newline) + newline, encoding="utf-8")
    print("Updated both Politecnico di Milano Aeronautical Engineering MSc records with current official evidence.")


if __name__ == "__main__":
    main()
