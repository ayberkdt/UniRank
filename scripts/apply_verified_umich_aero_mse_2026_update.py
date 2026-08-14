from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data_base" / "amerika.json"
TODAY = "2026-08-14"

PROGRAM = "https://aero.engin.umich.edu/graduate/master-of-science-in-engineering/"
ADMISSION = "https://aero.engin.umich.edu/graduate/admission-guidelines-planning/"
APPLICATION = "https://aero.engin.umich.edu/graduate/application-process/"
FAQ = "https://aero.engin.umich.edu/graduate/graduate-faqs/"
CURRENT = "https://aero.engin.umich.edu/graduate/current-graduate-students/"
COURSES = "https://aero.engin.umich.edu/graduate/current-graduate-students/grad-courses/"
FUNDING = "https://aero.engin.umich.edu/graduate/funding/"
RACKHAM_TESTS = "https://rackham.umich.edu/admissions/applying/tests/"
APP_FEE = "https://rackham.umich.edu/admissions/applying/application-fee-and-payment/"
IMMIGRATION = "https://rackham.umich.edu/admissions/applying/immigration-documents/"
TUITION = "https://ro.umich.edu/tuition-residency/tuition-fees/2026-2027/graduate/full-term/college-engineering-graduate-full-term"
FEES = "https://ro.umich.edu/tuition-residency/mandatory-fees"
GENERAL_COA = "https://finaid.umich.edu/getting-started/estimating-costs"
HOUSING = "https://housing.umich.edu/graduate-housing-basics/"
HOUSING_RATES = "https://housing.umich.edu/graduate-rates/"
RESEARCH = "https://aero.engin.umich.edu/research/"
SPACE = "https://aero.engin.umich.edu/research/research-areas/space-systems/"
FACILITIES = "https://aero.engin.umich.edu/research/shared-facilities/"
FACTS = "https://aero.engin.umich.edu/about/facts-figures/"
QS = "https://www.topuniversities.com/universities/university-michigan-ann-arbor"

REDDIT_FUNDING = "https://www.reddit.com/r/gradadmissions/comments/1p7d1wk/applied_for_phd_programme_received_an_mse_offer/"
REDDIT_HOUSING = "https://www.reddit.com/r/uofm/comments/1joyvdg/recommendations_for_grad_student_housing/"
REDDIT_ASSIGNMENT = "https://www.reddit.com/r/uofm/comments/1l9m2g9/northwood_ivv_updates/"


def bi(en: str, tr: str) -> dict[str, str]:
    return {"en": en, "tr": tr}


def source(url: str, title: str, source_type: str, fields: list[str], en: str, tr: str, confidence: str = "high") -> dict:
    return {
        "url": url,
        "title": title,
        "source_type": source_type,
        "access_status": "ok",
        "last_checked": TODAY,
        "relevant_fields": fields,
        "confidence": confidence,
        "notes": bi(en, tr),
    }


def main() -> None:
    rows = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    row = next(item for item in rows if item.get("id") == "umich-aero")

    row.update(
        {
            "country": "United States",
            "university": "University of Michigan—Ann Arbor",
            "university_native_name": "University of Michigan—Ann Arbor",
            "program_name": "Master of Science in Engineering in Aerospace Engineering",
            "program_native_name": "Master of Science in Engineering in Aerospace Engineering",
            "program_degree": "MSE",
            "degree_level": "Master",
            "duration": bi("Typically 3 academic terms; some students take 4 terms", "Genellikle 3 akademik dönem; bazı öğrenciler 4 dönemde tamamlar"),
            "duration_years": None,
            "ects": None,
            "us_credit_hours": 30,
            "teaching_language": ["Unknown"],
            "teaching_languages": ["Unknown"],
            "program_url": PROGRAM,
            "program_status": "active",
            "relevance_status": "strong",
            "tuition_eur_per_year": None,
            "annual_fee_eur": None,
            "tuition_usd_per_year": 68038,
            "annual_fee_usd": 1493.78,
            "qs_ranking": 51,
            "qs_ranking_display": "#51",
            "qs_ranking_year": 2027,
        }
    )

    row["prestige_profile"] = {
        "qs_world_rank": 51,
        "qs_edition": 2027,
        "qs_source_url": QS,
        "historical_distinction": bi("The department states that it is the oldest collegiate aeronautics programme in the United States, founded in 1914.", "Bölüm, 1914'te kurulan ABD'nin en eski üniversite düzeyindeki havacılık programı olduğunu belirtir."),
        "historical_source_url": FACTS,
        "interpretation": bi("University-wide QS prestige and departmental history are reported separately from current technical fit.", "Üniversite geneli QS prestiji ve bölüm tarihi güncel teknik uyumdan ayrı raporlanır."),
    }

    row["eligibility_profile"] = {
        "eligible_for_non_eu": True,
        "required_previous_degree": bi("An academic background equivalent to the University of Michigan Bachelor of Science in Engineering; strong mathematics and engineering preparation is essential.", "University of Michigan Mühendislik Lisansına denk akademik geçmiş; güçlü matematik ve mühendislik hazırlığı zorunludur."),
        "accepted_backgrounds": [
            bi("Engineering disciplines", "Mühendislik disiplinleri"),
            bi("Physics or applied physics with strong engineering preparation", "Güçlü mühendislik hazırlığıyla fizik veya uygulamalı fizik"),
            bi("Mathematics with strong engineering preparation", "Güçlü mühendislik hazırlığıyla matematik"),
        ],
        "non_engineering_background_advice": bi("Applicants without an engineering degree are advised to take the Mechanical Engineering discipline of the NCEES Fundamentals of Engineering exam and share the score.", "Mühendislik derecesi olmayan adaylara NCEES Fundamentals of Engineering sınavının Mechanical Engineering alanına girip puanı paylaşmaları tavsiye edilir."),
        "minimum_gpa": None,
        "recent_admit_gpa_benchmark": 3.6,
        "benchmark_not_minimum": True,
        "admission_mode": "selective_holistic",
        "admission_risk": "high",
        "required_documents": [
            bi("Rackham online graduate application and personal information", "Rackham çevrimiçi lisansüstü başvurusu ve kişisel bilgiler"),
            bi("Scanned official transcript for every completed or in-progress degree", "Tamamlanan veya sürmekte olan her derece için taranmış resmî transkript"),
            bi("Academic statement of purpose, typically no more than 2 pages", "Genellikle 2 sayfayı aşmayan akademik amaç mektubu"),
            bi("Personal statement, typically 500–700 words", "Genellikle 500–700 kelimelik kişisel beyan"),
            bi("Resume or curriculum vitae", "Özgeçmiş"),
            bi("Three recommendations; at least two from faculty able to discuss academic and research experience", "Üç referans; en az ikisi akademik ve araştırma deneyimini değerlendirebilen öğretim üyelerinden"),
            bi("Valid GRE General score", "Geçerli GRE General puanı"),
            bi("TOEFL or IELTS score unless a Rackham exemption applies", "Rackham muafiyeti yoksa TOEFL veya IELTS puanı"),
            bi("Non-US-citizen application fee", "ABD vatandaşı olmayan aday başvuru ücreti"),
        ],
        "motivation_letter_required": True,
        "personal_statement_required": True,
        "cv_required": True,
        "recommendation_required": True,
        "recommendation_letter_count": 3,
        "portfolio_required": False,
        "interview_required": False,
        "interview_policy": "not_listed_in_official_application_requirements",
        "test_required": True,
        "test_policy": bi("GRE General is required for regular MSE applicants; no separate departmental entrance examination is listed.", "Normal MSE adayları için GRE General zorunludur; ayrı bir bölüm giriş sınavı listelenmez."),
        "application_fee_usd": 90,
        "application_fee_waiver": bi("The department does not offer MSE fee waivers. Rackham's need-based waiver is limited to eligible US citizens/permanent residents; certain U-M preparatory-program participants may have separate routes.", "Bölüm MSE ücret muafiyeti sunmaz. Rackham'ın ihtiyaç temelli muafiyeti uygun ABD vatandaşları/kalıcı oturum sahipleriyle sınırlıdır; bazı U-M hazırlık programı katılımcılarının ayrı yolları olabilir."),
        "gre": {
            "policy": "required",
            "test_type": "GRE General",
            "minimum_scores": {},
            "recommended_scores": {},
            "recent_admit_benchmark": {"verbal_plus_quantitative": ">320", "analytical_writing": 4.0},
            "benchmark_not_minimum": True,
            "validity_rule": "Up to 5 years old as of the application deadline",
            "waiver_rules": [],
            "source_ids": [APPLICATION, ADMISSION, FAQ],
        },
        "notes_for_turkish_students": bi("A Turkish degree is evaluated for US equivalency after admission recommendation. Upload country-specific credentials and do not send final official originals until requested. Financial documents are requested after admission for immigration processing.", "Türkiye'den alınan derece, kabul önerisinden sonra ABD denkliği açısından değerlendirilir. Ülkeye özgü belgeleri yükleyin; nihai resmî asılları istenmeden göndermeyin. Göçmenlik işlemleri için mali belgeler kabulden sonra talep edilir."),
        "verification_notes": bi("No formal departmental GPA or GRE minimum is published. Recent-admit figures are descriptive benchmarks, not eligibility cutoffs or admission guarantees.", "Resmî bölüm GPA veya GRE tabanı yayımlanmaz. Son kabul edilenlere ait değerler tanımlayıcı göstergedir; uygunluk eşiği veya kabul garantisi değildir."),
    }

    row["language_profile"] = {
        "teaching_language": ["Unknown"],
        "teaching_languages": ["Unknown"],
        "english_required": True,
        "english_level_required": bi("TOEFL iBT minimum 84 or IELTS minimum 6.5 when an exemption does not apply", "Muafiyet yoksa TOEFL iBT en az 84 veya IELTS en az 6,5"),
        "accepted_english_tests": [
            {"test": "TOEFL iBT", "minimum_score": 84},
            {"test": "IELTS", "minimum_score": 6.5},
        ],
        "duolingo_accepted": False,
        "english_exemptions": [bi("Native English speaker", "Ana dili İngilizce olan aday"), bi("Completed an entire undergraduate or graduate degree where the only language of instruction was English, with formal documentation", "Öğretim dili yalnızca İngilizce olan bir kurumda lisans veya lisansüstü derecenin tamamını, resmî belgeyle bitiren aday"), bi("Current University of Michigan student", "Mevcut University of Michigan öğrencisi")],
        "score_validity_years": 2,
        "gsi_spoken_english_requirement": bi("Applicants educated at an undergraduate institution whose teaching language was not English must pass the GSI Oral English Test before a GSI appointment.", "Lisans kurumunun öğretim dili İngilizce olmayan GSI adayları atama öncesi GSI Oral English Test'i geçmelidir."),
        "language_risk": "medium",
        "verification_notes": bi("Official sources verify the English-proficiency admission rule but do not explicitly state the MSE teaching language. In accordance with the no-inference policy, teaching language remains Unknown rather than being inferred from the US location or English application pages.", "Resmî kaynaklar İngilizce yeterlilik kabul şartını doğrular ancak MSE öğretim dilini açıkça belirtmez. Çıkarım yapmama kuralı gereği öğretim dili ABD konumundan veya İngilizce başvuru sayfalarından çıkarılmayıp Unknown bırakılır."),
    }

    row["cost_profile"] = {
        "academic_year": "2026/2027",
        "currency": "USD",
        "tuition_usd_per_full_time_term_nonresident": 34019,
        "tuition_usd_per_year": 68038,
        "tuition_year_definition": "two full-time fall/winter terms at 9+ credits each",
        "mandatory_general_fee_usd_per_full_term": 246.89,
        "international_student_fee_usd_per_full_term": 500,
        "mandatory_fees_usd_per_year": 1493.78,
        "academic_billed_baseline_usd_per_two_terms": 69531.78,
        "academic_billed_baseline_status": "interpreted_sum_of_current_official_components",
        "living_cost_usd_per_year": 28250,
        "living_cost_scope": bi(
            "Rackham's general 12-month living-expense allowance; not housing-only and not Engineering-specific",
            "Rackham'ın genel 12 aylık yaşam gideri bütçesi; yalnızca konut değildir ve Engineering'e özgü değildir",
        ),
        "health_service_and_infrastructure_fees_included_in_tuition": True,
        "additional_course_or_program_fees_possible": True,
        "official_general_international_i20_estimate": {"tuition_and_fees_usd": 61000, "living_expenses_usd": 28250, "books_and_supplies_usd": 1380, "mandatory_health_insurance_usd": 3600, "total_usd": 94230},
        "program_specific_total_cost_of_attendance_usd_per_year": None,
        "tuition_basis": "2026/27 College of Engineering graduate nonresident rate, 9+ credits per full term",
        "tuition_items": [
            {"item": bi("College of Engineering nonresident graduate tuition", "College of Engineering eyalet dışı lisansüstü öğrenim ücreti"), "amount": 34019, "currency": "USD", "period": "full_term"},
            {"item": bi("General mandatory fees", "Genel zorunlu ücretler"), "amount": 246.89, "currency": "USD", "period": "full_term"},
            {"item": bi("International student fee for F/J status", "F/J statüsündeki uluslararası öğrenci ücreti"), "amount": 500, "currency": "USD", "period": "full_term"},
        ],
        "verification_notes": bi("The $68,038 two-term tuition is programme-specific and current. The separate $94,230 immigration estimate is a general Rackham international budget and explicitly says programme fees vary; it must not be presented as an Engineering-specific total. A typical three-term MSE crosses academic years, so complete-program tuition cannot be fixed from one current rate table.", "68.038 $ iki dönemlik öğrenim ücreti programa özgü ve günceldir. Ayrı 94.230 $ göçmenlik tahmini genel Rackham uluslararası bütçesidir ve program ücretlerinin değiştiğini açıkça söyler; mühendisliğe özgü toplam gibi sunulamaz. Tipik üç dönemlik MSE iki akademik yıla yayıldığından tam program ücreti tek güncel tarifeden sabitlenemez."),
    }

    row["scholarship_profile"] = {
        "available_types": ["graduate_student_research_assistant", "graduate_student_instructor", "graduate_student_staff_assistant", "grader", "external_fellowship"],
        "non_eu_eligible": True,
        "application_mode": "separate",
        "automatic_consideration": False,
        "separate_application_required": True,
        "admission_funding_offer": False,
        "mse_share_with_gsra_or_gsi_in_a_term": 0.06,
        "opportunities": [
            {"name": "AERO GSI/GSSA semester positions", "type": "competitive_employment", "amount": None, "currency": "USD", "automatic_consideration": False, "separate_application_required": True, "deadline": bi("Fall: May 31; Winter: November 1", "Güz: 31 Mayıs; Kış: 1 Kasım"), "eligibility_summary": bi("Incoming or current enrolled AERO graduate student; normally prior equivalent course with B or better and cumulative GPA at least 3.0. Positions are limited and mostly go to doctoral students.", "Kayıtlı veya yeni AERO lisansüstü öğrencisi; normalde eşdeğer dersten en az B ve toplamda en az 3,0 GPA. Pozisyonlar sınırlıdır ve çoğu doktora öğrencilerine gider."), "url": FUNDING},
            {"name": "External fellowships and scholarships", "type": "external_funding", "amount": None, "currency": "USD", "automatic_consideration": False, "separate_application_required": True, "deadline": None, "eligibility_summary": bi("Eligibility and deadlines depend on the external sponsor; listing by Michigan is not endorsement or a funding promise.", "Uygunluk ve tarihler dış sponsora bağlıdır; Michigan'ın listelemesi onay veya finansman sözü değildir."), "url": FUNDING},
        ],
        "funding_notes": bi("The department does not make financial-assistance offers to master's applicants. Students are expected to self-fund. Later GSRA/GSI roles are highly competitive; only about 6% of MSE students hold one during a term. Grader openings may be announced after the term starts.", "Bölüm yüksek lisans adaylarına mali yardım teklifi yapmaz; öğrencilerin öz finansman sağlaması beklenir. Sonraki GSRA/GSI rolleri çok rekabetçidir; MSE öğrencilerinin yalnızca yaklaşık %6'sı bir dönemde böyle bir görev alır. Değerlendirici pozisyonları dönem başladıktan sonra duyurulabilir."),
        "verification_notes": bi("A later employment appointment is not an admission scholarship and must not be budgeted as guaranteed income.", "Sonradan alınabilecek çalışma görevi kabul bursu değildir ve garantili gelir olarak bütçelenmemelidir."),
    }

    row["living_profile"] = {
        "city_cost_level": "high",
        "housing_difficulty": "high",
        "housing_access": "not_guaranteed",
        "student_housing_available": True,
        "housing_application_separate": True,
        "housing_allocation_mode": "offer_subject_to_vacancy_and_requested_space_dates_status",
        "monthly_housing_rent_usd_per_month_min": 861,
        "monthly_housing_rent_usd_per_month_max": 1486,
        "average_room_rent_scope_label": bi("University graduate housing, per person", "Üniversite lisansüstü konutu, kişi başı"),
        "housing_options": [
            {"provider": "Munger Graduate Residences", "institution_owned": True, "guaranteed": False, "utilities_included": True},
            {"provider": "Northwood Community Apartments", "institution_owned": True, "guaranteed": False, "utilities_included": True},
        ],
        "official_rent_items": [
            {"item": bi("Munger suite room, per person", "Munger süit odası, kişi başı"), "amount_usd_min": 1329, "amount_usd_max": 1486, "period": "month", "academic_year": "2026/2027"},
            {"item": bi("Northwood shared apartment, per person", "Northwood paylaşımlı daire, kişi başı"), "amount_usd_min": 861, "amount_usd_max": 959, "period": "month", "academic_year": "2026/2027"},
            {"item": bi("Northwood student apartment under one contract", "Tek sözleşmeli Northwood öğrenci dairesi"), "amount_usd_min": 1277, "amount_usd_max": 1865, "period": "month", "academic_year": "2026/2027"},
        ],
        "official_living_cost_items": [
            {"item": bi("General international immigration living allowance for 12 months", "12 aylık genel uluslararası göçmenlik yaşam payı"), "amount_usd": 28250, "period": "year", "academic_year": "current_on_2026-08-14"},
            {"item": bi("Books and supplies allowance", "Kitap ve malzeme payı"), "amount_usd": 1380, "period": "year", "academic_year": "current_on_2026-08-14"},
            {"item": bi("Mandatory international health-insurance estimate", "Zorunlu uluslararası sağlık sigortası tahmini"), "amount_usd": 3600, "period": "year", "academic_year": "current_on_2026-08-14"},
        ],
        "living_risk": "high",
        "housing_notes": bi("Newly admitted students apply after completing admission requirements and confirming enrollment. Housing sends an offer only if a suitable vacancy exists; eligibility or an application does not guarantee housing. Current rates include utilities.", "Yeni kabul edilen öğrenciler kabul şartlarını tamamlayıp kaydı onayladıktan sonra başvurur. Konut birimi yalnız uygun boşluk varsa teklif gönderir; uygunluk veya başvuru konutu garanti etmez. Güncel fiyatlara faturalar dahildir."),
        "verification_notes": bi("Official university-housing rates are used; no private-market average is inferred.", "Resmî üniversite konutu fiyatları kullanılır; özel piyasa ortalaması çıkarılmaz."),
    }

    row["curriculum_profile"] = {
        "credit_system": "US semester credit hours",
        "credit_hours_total": 30,
        "course_count_fixed": False,
        "course_count_summary": bi("No fixed total course count; 30 graded graduate credits with at least 5 qualifying AEROSP courses and 2 approved mathematics courses", "Sabit toplam ders sayısı yok; en az 5 uygun AEROSP ve 2 onaylı matematik dersiyle 30 notlu lisansüstü kredi"),
        "tracks": [
            bi("Aerodynamics and Propulsion", "Aerodinamik ve İtki"),
            bi("Autonomous Systems and Control", "Otonom Sistemler ve Kontrol"),
            bi("Computation", "Hesaplama"),
            bi("Space Systems", "Uzay Sistemleri"),
            bi("Structures and Materials", "Yapılar ve Malzemeler"),
        ],
        "track_selection_policy": bi("Applicants select a subplan, but it does not restrict course choice and can be changed during the degree.", "Adaylar bir alt plan seçer; bu seçim dersleri kısıtlamaz ve derece sırasında değiştirilebilir."),
        "requirement_components": [
            {"name": bi("Five AEROSP courses at 500 level or above, each with B or better", "Her birinden en az B alınan, 500 düzeyi veya üstünde beş AEROSP dersi"), "course_count": 5},
            {"name": bi("Two approved mathematics courses, each with B or better", "Her birinden en az B alınan iki onaylı matematik dersi"), "course_count": 2},
            {"name": bi("Remaining approved graded graduate coursework", "Kalan onaylı ve notlu lisansüstü dersler"), "credit_hours": bi("Enough to reach 30 total credits", "Toplam 30 krediye ulaşacak kadar")},
        ],
        "mandatory_courses": [],
        "elective_courses": [],
        "thesis_required": False,
        "thesis_requirement_summary": bi("No thesis, research or practicum is required", "Tez, araştırma veya uygulama zorunluluğu yoktur"),
        "internship_required": False,
        "internship_notes": bi("No compulsory internship or practicum is part of the official MSE requirements.", "Resmî MSE şartlarında zorunlu staj veya uygulama bulunmaz."),
        "directed_study_max_credit_hours": 6,
        "seminar_max_credit_hours": 3,
        "approved_nontechnical_max_credit_hours": 4,
        "summer_aerospace_courses_offered": False,
        "research_option": bi("Optional AEROSP 590 directed study requires a willing faculty supervisor and approval; availability is not guaranteed.", "İsteğe bağlı AEROSP 590 yönlendirilmiş çalışma, istekli öğretim üyesi ve onay gerektirir; erişim garanti değildir."),
        "verification_notes": bi("This is a terminal coursework-based MSE. The five published subplans help planning but are not binding course tracks.", "Bu, ders odaklı terminal bir MSE'dir. Yayımlanan beş alt plan planlamaya yardımcı olur ancak bağlayıcı ders yolları değildir."),
    }

    row["category_profile"] = {
        "primary_categories": ["Aerospace Engineering", "Space Systems & Astronautics"],
        "secondary_categories": ["Aerodynamics & Fluid Mechanics", "Flight Mechanics & Control", "Propulsion & Energy", "Structures & Materials", "Systems & Design", "Scientific AI & Computational Engineering"],
        "subcategories": ["aerodynamics", "cfd", "astrodynamics", "gnc", "electric_propulsion", "aerospace_structures", "materials", "autonomy", "simulation_modelling", "space_systems", "satellite_systems"],
        "normalized_tags": ["aerodynamics", "cfd", "astrodynamics", "gnc", "electric_propulsion", "aerospace_structures", "materials", "autonomy", "simulation_modelling", "space_systems", "satellite_systems"],
        "category_scores": {},
        "category_evidence": [bi("The official curriculum subplans and research pages cover atmospheric flight and spacecraft domains, including electric propulsion, satellites, astrodynamics, autonomy, computation and structures.", "Resmî müfredat alt planları ve araştırma sayfaları elektrikli itki, uydular, astrodinamik, otonomi, hesaplama ve yapılar dâhil atmosferik uçuş ve uzay aracı alanlarını kapsar.")],
    }

    row["research_profile"] = {
        "department_research_areas": [
            bi("Aerodynamics and propulsion", "Aerodinamik ve itki"),
            bi("Autonomous systems and control", "Otonom sistemler ve kontrol"),
            bi("Computation", "Hesaplama"),
            bi("Space systems", "Uzay sistemleri"),
            bi("Structures and materials", "Yapılar ve malzemeler"),
            bi("Sustainable aviation", "Sürdürülebilir havacılık"),
        ],
        "labs": [
            {"name": "Plasmadynamics and Electric Propulsion Laboratory (PEPL)", "officially_listed": True, "student_access": bi("Research appointment or directed-study supervision dependent", "Araştırma görevi veya yönlendirilmiş çalışma danışmanlığına bağlı")},
            {"name": "Michigan Exploration Laboratory (MXL)", "officially_listed": True, "student_access": bi("Research appointment or directed-study supervision dependent", "Araştırma görevi veya yönlendirilmiş çalışma danışmanlığına bağlı")},
            {"name": "Space-FALCON Lab", "officially_listed": True, "student_access": bi("Research placement dependent", "Araştırma yerleştirmesine bağlı")},
            {"name": "Space Systems Laboratory", "officially_listed": True, "student_access": bi("Research placement dependent", "Araştırma yerleştirmesine bağlı")},
            {"name": "Aerospace, Robotics and Controls Laboratory", "officially_listed": True, "student_access": bi("Research placement dependent", "Araştırma yerleştirmesine bağlı")},
            {"name": "Distributed Aerospace Systems and Control Laboratory", "officially_listed": True, "student_access": bi("Research placement dependent", "Araştırma yerleştirmesine bağlı")},
        ],
        "facilities": [bi("Ten instructional and research wind tunnels, spanning low speed to above Mach 4", "Düşük hızdan Mach 4 üstüne uzanan on eğitim ve araştırma rüzgâr tüneli"), bi("PEPL high-vacuum electric-propulsion facilities", "PEPL yüksek vakumlu elektrikli itki tesisleri")],
        "research_strength_summary": bi("Michigan publishes unusually deep space-systems infrastructure alongside broad aeronautics research. For MSE students, however, admission does not include a research post: original research is optional and depends on faculty availability, usually through AEROSP 590.", "Michigan geniş havacılık araştırmasının yanında alışılmadık derinlikte uzay sistemleri altyapısı yayımlar. Ancak MSE kabulü araştırma görevi içermez; özgün araştırma isteğe bağlıdır ve genellikle AEROSP 590 üzerinden öğretim üyesi uygunluğuna bağlıdır."),
        "research_strength_score": None,
        "research_sources": [RESEARCH, SPACE, FACILITIES, PROGRAM],
    }

    row["industry_ecosystem_profile"] = {
        "nearby_companies": [],
        "confirmed_partners": [],
        "officially_documented_research_sponsors": ["NASA"],
        "space_agencies_or_public_bodies": ["NASA"],
        "research_institutes": [],
        "startup_or_incubator_ecosystem": [],
        "internship_possibility": "possible_but_not_program_requirement",
        "thesis_with_industry_possibility": "not_applicable_no_thesis_route",
        "career_relevance": "high_but_not_scored",
        "ecosystem_strength_score": None,
        "ecosystem_notes": bi("The official space-systems page documents NASA sponsorship of a selected electric-propulsion project. This is not treated as a programme-wide partnership or hiring guarantee. The legacy Ford, GM and Boeing partnership claims were removed because programme-specific confirmation was not established.", "Resmî uzay sistemleri sayfası seçili bir elektrikli itki projesinde NASA sponsorluğunu belgeler. Bu, program geneli ortaklık veya işe alım garantisi sayılmaz. Programa özgü doğrulama kurulamadığı için eski Ford, GM ve Boeing ortaklık iddiaları kaldırılmıştır."),
    }

    row["application_timeline_profile"] = {
        "academic_year": "recurring deadlines on current official pages",
        "intake_terms": ["Fall", "Winter"],
        "application_rounds": [
            {"round": bi("Fall MSE", "Güz MSE"), "opens": None, "deadline": "January 15", "decision": bi("As soon as possible; the department warns that several months may pass", "Mümkün olan en kısa sürede; bölüm birkaç ay geçebileceğini belirtir")},
            {"round": bi("Winter MSE", "Kış MSE"), "opens": None, "deadline": "October 7", "decision": bi("As soon as possible; the department warns that several months may pass", "Mümkün olan en kısa sürede; bölüm birkaç ay geçebileceğini belirtir")},
        ],
        "non_eu_deadline": bi("Same Fall January 15 and Winter October 7 programme deadlines; all materials must arrive by the deadline", "Aynı Güz 15 Ocak ve Kış 7 Ekim program tarihleri; tüm materyaller son tarihe kadar ulaşmalıdır"),
        "scholarship_deadline": bi("No admission scholarship; separate GSI/GSSA applications: May 31 for Fall and November 1 for Winter", "Kabul bursu yoktur; ayrı GSI/GSSA başvuruları Güz için 31 Mayıs, Kış için 1 Kasım"),
        "pre_enrolment_required": False,
        "visa_document_deadlines": [{"intake": "Fall", "deadline": "May 15"}, {"intake": "Winter", "deadline": "November 15"}],
        "visa_sensitive_deadline": bi("After admission, Rackham requests financial documents for the I-20/DS-2019. Current withdrawal-trigger dates are May 15 for Fall and November 15 for Winter; document preparation normally takes 7–10 business days after a complete upload.", "Kabulden sonra Rackham I-20/DS-2019 için mali belgeleri ister. Güncel teklif geri çekme tarihleri Güz için 15 Mayıs, Kış için 15 Kasım'dır; eksiksiz yüklemeden sonra belge hazırlığı normalde 7–10 iş günü sürer."),
        "application_result_timing": bi("No fixed decision date; applicants may wait several months. AERO recommends admission, then Rackham confirms the official offer.", "Sabit karar tarihi yoktur; adaylar birkaç ay bekleyebilir. AERO kabul önerir, ardından Rackham resmî teklifi onaylar."),
        "timeline_risk": "medium",
        "deadline_notes": bi("The current department pages publish recurring month/day deadlines without a cycle year; no future year is invented here.", "Güncel bölüm sayfaları dönem yılı vermeden yinelenen ay/gün tarihleri yayımlar; burada gelecek yıl uydurulmaz."),
    }

    row["student_sentiment_profile"] = {
        "student_satisfaction_score": None,
        "teaching_quality_sentiment": "unknown",
        "workload_sentiment": "unknown",
        "workload_balance_sentiment": "unknown",
        "administration_sentiment": "unknown",
        "housing_sentiment": "mixed",
        "city_life_sentiment": "unknown",
        "international_student_sentiment": "unknown",
        "career_support_sentiment": "unknown",
        "funding_sentiment": "very_challenging_for_mse",
        "student_sentiment_summary": bi("The small recent sample is consistent with the official no-admission-funding policy and reports uncertainty around graduate-housing offers. Northwood is often valued for utilities-included pricing and community, while Munger draws mixed reactions because many bedrooms lack windows. These are perceptions, not programme facts or private-market price evidence.", "Küçük güncel örneklem resmî kabul finansmanı yok politikasına paraleldir ve lisansüstü konut tekliflerinde belirsizlik bildirir. Northwood faturalar dâhil fiyatı ve topluluğuyla sıkça olumlu görülürken Munger, birçok yatak odasında pencere olmaması nedeniyle karışık tepki alır. Bunlar algıdır; program gerçeği veya özel piyasa fiyat kanıtı değildir."),
        "student_sentiment_sources": [
            {"url": REDDIT_FUNDING, "platform": "Reddit r/gradadmissions", "topic": "Aerospace MSE funding", "date": "2025-11-26", "approx_observations": 4, "access_status": "ok", "last_checked": TODAY, "confidence": "low"},
            {"url": REDDIT_HOUSING, "platform": "Reddit r/uofm", "topic": "graduate housing experience", "date": "2025-04-01", "approx_observations": 10, "access_status": "ok", "last_checked": TODAY, "confidence": "low"},
            {"url": REDDIT_ASSIGNMENT, "platform": "Reddit r/uofm", "topic": "Northwood assignment timing", "date": "2025-06-12", "approx_observations": 6, "access_status": "ok", "last_checked": TODAY, "confidence": "low"},
        ],
        "approximate_sample_size": 20,
        "date_range": "2025-2026",
        "sentiment_confidence": "low",
        "verification_notes": bi("No satisfaction score is computed from this small, housing- and funding-heavy sample.", "Bu küçük, konut ve finansman ağırlıklı örneklemden memnuniyet puanı hesaplanmaz."),
    }

    sources = [
        source(PROGRAM, "Michigan Aerospace MSE", "official_program_page", ["program", "program_status", "duration", "curriculum", "research"], "Current degree status, coursework structure, typical completion time and optional directed study.", "Güncel derece durumu, ders yapısı, tipik tamamlama süresi ve isteğe bağlı yönlendirilmiş çalışma."),
        source(ADMISSION, "Michigan Aerospace Admission Guidelines and Planning", "official_admission_page", ["admission", "non_eu_eligibility", "deadline", "visa"], "Current background expectations, recurring deadlines, decision process and post-admission immigration sequence.", "Güncel geçmiş beklentileri, yinelenen tarihler, karar süreci ve kabul sonrası göçmenlik sırası."),
        source(APPLICATION, "Michigan Aerospace Application Process", "official_admission_page", ["admission", "required_documents", "gre", "language", "application_fee"], "Current MSE documents, GRE rule, TOEFL/IELTS minimums and application workflow.", "Güncel MSE belgeleri, GRE kuralı, TOEFL/IELTS tabanları ve başvuru akışı."),
        source(FAQ, "Michigan Aerospace Graduate FAQs", "official_admission_page", ["admission", "curriculum", "funding", "deadline"], "Current selectivity benchmarks, MSE fee-waiver policy, curriculum and no-thesis rule.", "Güncel seçicilik göstergeleri, MSE ücret muafiyeti politikası, müfredat ve tez yok kuralı."),
        source(CURRENT, "Michigan Aerospace Current Graduate Students", "official_curriculum_page", ["curriculum", "language", "gre"], "Current 30-credit explanations, GRE requirement, English exemption and explicit Duolingo exclusion.", "Güncel 30 kredi açıklamaları, GRE şartı, İngilizce muafiyeti ve açık Duolingo dışlaması."),
        source(COURSES, "Michigan Aerospace Graduate Courses", "official_curriculum_page", ["curriculum", "courses", "tracks"], "Current course planning by research area and warning that future offerings may change.", "Araştırma alanına göre güncel ders planlama ve gelecek derslerin değişebileceği uyarısı."),
        source(FUNDING, "Michigan Aerospace Graduate Funding", "official_scholarship_page", ["scholarship", "funding", "non_eu_eligibility", "language"], "No admission aid for MSE, 6% semester employment figure, separate deadlines and GSI qualifications.", "MSE için kabul yardımı olmaması, %6 dönemlik görev oranı, ayrı tarihler ve GSI nitelikleri."),
        source(RACKHAM_TESTS, "Rackham English Proficiency Tests and Exemptions", "official_admission_page", ["language", "admission"], "Current English exemptions, official-score and two-year-validity rules.", "Güncel İngilizce muafiyetleri, resmî puan ve iki yıl geçerlilik kuralları."),
        source(APP_FEE, "Rackham Application Fee and Payment", "official_admission_page", ["application_fee", "admission"], "Current $90 non-US-citizen fee and waiver eligibility.", "Güncel ABD vatandaşı olmayanlar için 90 $ ücret ve muafiyet uygunluğu."),
        source(IMMIGRATION, "Rackham Immigration Documents", "official_visa_or_government_page", ["visa", "living", "cost", "deadline"], "Current proof-of-funds estimate, financial-document deadlines and processing time.", "Güncel mali yeterlilik tahmini, mali belge tarihleri ve işlem süresi."),
        source(TUITION, "Michigan Engineering Graduate Tuition 2026/27", "official_tuition_page", ["tuition", "fees", "non_eu_eligibility"], "Current nonresident full-time Engineering graduate tuition per term.", "Güncel eyalet dışı tam zamanlı mühendislik lisansüstü dönem ücreti."),
        source(FEES, "Michigan Mandatory Fees 2026/27", "official_tuition_page", ["fees", "tuition"], "Current general mandatory and F/J international fees per full term; included fee components are explicit.", "Güncel genel zorunlu ve F/J uluslararası tam dönem ücretleri; dâhil kalemler açıktır."),
        source(GENERAL_COA, "Michigan Financial Aid Estimated Costs 2026/27", "official_cost_of_living_page", ["living", "cost"], "General nonresident graduate cost-of-attendance context; not treated as Engineering-specific.", "Genel eyalet dışı lisansüstü katılım maliyeti bağlamı; mühendisliğe özgü sayılmaz."),
        source(HOUSING, "Michigan Graduate Housing Basics", "official_housing_page", ["housing", "application"], "Graduate housing application sequence and offer-by-vacancy policy.", "Lisansüstü konut başvuru sırası ve boşluğa bağlı teklif politikası."),
        source(HOUSING_RATES, "Michigan Graduate Housing Rates 2026/27", "official_housing_page", ["housing", "living"], "Current per-person Munger and Northwood rates and utility inclusion.", "Güncel kişi başı Munger ve Northwood fiyatları ile fatura kapsamı."),
        source(RESEARCH, "Michigan Aerospace Research", "official_department_page", ["research", "curriculum"], "Current department research-area framework.", "Güncel bölüm araştırma alanı çerçevesi."),
        source(SPACE, "Michigan Aerospace Space Systems", "official_department_page", ["research", "labs", "industry_ecosystem"], "Named space labs, electric-propulsion facilities, satellite work and selected NASA-sponsored project.", "Adlandırılmış uzay laboratuvarları, elektrikli itki tesisleri, uydu çalışmaları ve seçili NASA sponsorlu proje."),
        source(FACILITIES, "Michigan Aerospace Shared Facilities", "official_department_page", ["research", "labs"], "Current wind-tunnel, vacuum and materials facilities.", "Güncel rüzgâr tüneli, vakum ve malzeme tesisleri."),
        source(FACTS, "Michigan Aerospace Facts and Figures", "official_department_page", ["prestige", "department"], "Official departmental history, kept separate from fit.", "Teknik uyumdan ayrı tutulan resmî bölüm tarihi."),
        source(QS, "QS World University Rankings 2027 — Michigan", "reliable_third_party_ranking", ["prestige"], "Current university-wide rank; not proof of aerospace technical strength.", "Güncel üniversite geneli sıra; havacılık-uzay teknik gücü kanıtı değildir.", confidence="medium"),
        source(REDDIT_FUNDING, "Reddit — Michigan Aerospace MSE funding discussion", "student_forum", ["student_sentiment"], "Small anecdotal funding sample; official policy remains controlling.", "Küçük anekdotsal finansman örneklemi; resmî politika belirleyicidir.", confidence="low"),
        source(REDDIT_HOUSING, "Reddit r/uofm — graduate housing recommendations", "student_forum", ["student_sentiment"], "Small anecdotal housing-quality and price-perception sample.", "Küçük anekdotsal konut kalitesi ve fiyat algısı örneklemi.", confidence="low"),
        source(REDDIT_ASSIGNMENT, "Reddit r/uofm — Northwood assignment timing", "student_forum", ["student_sentiment"], "Small anecdotal sample about offer timing and uncertainty.", "Teklif zamanı ve belirsizlik hakkında küçük anekdotsal örneklem.", confidence="low"),
    ]

    row["source_profile"] = {
        "primary_url": PROGRAM,
        "secondary_urls": [item["url"] for item in sources[1:]],
        "last_verified": TODAY,
        "field_confidence": {"program_basic_info": "high", "program": "high", "language": "unknown", "admission": "high", "non_eu_eligibility": "high", "tuition": "high", "scholarship": "high", "deadline": "high", "curriculum": "high", "research": "high", "industry_ecosystem": "medium", "housing": "high", "living": "high", "sentiment": "low", "prestige": "high"},
        "source_reliability": "high",
        "verification_status": "partially_verified",
        "needs_verification": True,
        "verification_notes": bi("Every core field except explicit teaching language is supported by current official sources. Teaching language remains Unknown under the no-inference rule. A programme-specific total cost of attendance and private-market rent are also deliberately not invented.", "Açık öğretim dili dışındaki tüm temel alanlar güncel resmî kaynaklarla desteklenir. Öğretim dili çıkarım yapmama kuralıyla Unknown kalır. Programa özgü toplam katılım maliyeti ve özel piyasa kirası da bilerek uydurulmaz."),
        "source_log": sources,
    }

    row["decision_summary"] = {
        "best_for": [bi("Students seeking flexible, coursework-based aerospace depth across aeronautics and space without a mandatory thesis.", "Zorunlu tez olmadan havacılık ve uzayda esnek, ders odaklı derinlik isteyen öğrenciler."), bi("Applicants especially interested in electric propulsion, spacecraft systems, satellites, autonomy or high-end experimental facilities.", "Özellikle elektrikli itki, uzay aracı sistemleri, uydular, otonomi veya ileri deney altyapısıyla ilgilenen adaylar.")],
        "not_ideal_for": [bi("Applicants who require admission-time funding or guaranteed research placement.", "Kabul sırasında finansman veya garantili araştırma yerleştirmesi gereken adaylar."), bi("Applicants seeking a thesis-centred research master's.", "Tez merkezli araştırma yüksek lisansı arayanlar.")],
        "main_strengths": [bi("Five flexible subplans and 30 credits spanning major aerospace and space domains.", "Temel havacılık-uzay ve uzay alanlarını kapsayan beş esnek alt plan ve 30 kredi."), bi("Named space laboratories include PEPL, MXL, Space-FALCON and the Space Systems Laboratory.", "Adlandırılmış uzay laboratuvarları PEPL, MXL, Space-FALCON ve Space Systems Laboratory'yi içerir."), bi("Current facilities include ten wind tunnels and major high-vacuum electric-propulsion infrastructure.", "Güncel tesisler on rüzgâr tüneli ve büyük yüksek-vakum elektrikli itki altyapısını içerir.")],
        "main_risks": [bi("The current two-full-term international academic billing baseline is $69,531.78 before living costs; the typical programme takes three terms.", "Güncel iki tam dönemlik uluslararası akademik fatura tabanı yaşam giderleri öncesi 69.531,78 $'dır; tipik program üç dönem sürer."), bi("No funding accompanies MSE admission; only about 6% of MSE students hold a GSRA/GSI role in any one term.", "MSE kabulüne finansman eşlik etmez; herhangi bir dönemde MSE öğrencilerinin yalnız yaklaşık %6'sı GSRA/GSI görevi alır."), bi("University graduate housing exists but is vacancy-dependent and not guaranteed.", "Üniversite lisansüstü konutu vardır ancak boşluğa bağlıdır ve garanti edilmez."), bi("GRE is mandatory for regular MSE applicants.", "Normal MSE adayları için GRE zorunludur."), bi("The official sources checked do not explicitly state teaching language, so the database does not infer it.", "Kontrol edilen resmî kaynaklar öğretim dilini açıkça belirtmediği için veritabanı çıkarım yapmaz.")],
        "decision_summary": bi("Technically excellent and unusually strong in space systems and electric propulsion, but financially high-risk for an international MSE student because admission is self-funded and a typical degree extends beyond the two-term annual rate table.", "Teknik açıdan çok güçlü, özellikle uzay sistemleri ve elektrikli itkide sıra dışıdır; ancak kabul öz finansmanlı olduğundan ve tipik derece iki dönemlik yıllık tarifenin ötesine uzandığından uluslararası MSE öğrencisi için mali riski yüksektir."),
        "pros": [],
        "cons": [],
        "verdict": bi("High technical fit, very high verified cost, no admission funding and optional—not guaranteed—research access.", "Yüksek teknik uyum, çok yüksek doğrulanmış maliyet, kabul finansmanı yok ve isteğe bağlı fakat garantisiz araştırma erişimi."),
    }

    row["scoring_inputs"] = {"academic_prestige": None, "research_output": None, "industry_links": None, "affordability": None, "admission_chance": None, "living_quality": None, "hard_flags": ["teaching_language_unverified", "gre_required", "high_cost", "no_admission_funding", "research_not_guaranteed", "housing_not_guaranteed", "visa_financial_documents_required"]}
    row["data_quality"] = {"status": "partial", "checked_official_source_count": 19, "verified_fields": ["program", "admission", "non_eu_eligibility", "tuition", "scholarship", "deadline", "curriculum", "research", "housing", "living", "prestige"], "unverified_critical_fields": ["language"], "known_semantic_gaps": ["explicit_teaching_language"], "has_checked_source_log": True, "audited_at": TODAY}
    row["quality_control"] = {"checked_at": TODAY, "qc_status": "needs_revision", "remaining_verification_tasks": [bi("Find a current official source that explicitly states the MSE teaching language; do not infer it from location or English-proficiency requirements.", "MSE öğretim dilini açıkça belirten güncel resmî kaynak bulun; konumdan veya İngilizce yeterlilik şartından çıkarım yapmayın.")], "qc_notes": bi("All discoverable decision fields are source-backed; the record remains partial solely because teaching language could not be explicitly verified.", "Bulunabilen tüm karar alanları kaynaklıdır; kayıt yalnızca öğretim dili açıkça doğrulanamadığı için partial kalır."), "failed_canary_tests": ["teaching_language_not_explicitly_verified"]}

    DATA_PATH.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"id": row["id"], "status": row["data_quality"]["status"], "checked_official_source_count": row["data_quality"]["checked_official_source_count"], "verified_fields": row["data_quality"]["verified_fields"], "unverified_critical_fields": row["data_quality"]["unverified_critical_fields"]}, indent=2))


if __name__ == "__main__":
    main()
