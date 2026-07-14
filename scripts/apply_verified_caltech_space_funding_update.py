"""Correct Caltech Space Engineering funding and remove unsourced experience claims."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data_base" / "amerika.json"
CHECKED = "2026-07-14"
ADMISSIONS_URL = "https://aerospace.caltech.edu/academics/admissions"


def bi(en: str, tr: str) -> dict[str, str]:
    return {"en": en, "tr": tr}


def source() -> dict[str, Any]:
    return {
        "url": ADMISSIONS_URL,
        "title": "Caltech Aerospace: Fellowships and Financial Support",
        "source_type": "official_scholarship_page",
        "access_status": "ok",
        "last_checked": CHECKED,
        "relevant_fields": ["scholarship", "funding"],
        "confidence": "high",
        "notes": bi(
            "The Aerospace department states that it awards several fellowships each year, primarily to entering Master's candidates with doctoral potential; normally full tuition and a substantial living stipend for one academic year. It also warns that admission and aid are considered separately.",
            "Aerospace bölümü her yıl, ağırlıkla doktora potansiyeli bulunan yeni yüksek lisans adaylarına birkaç fellowship verdiğini; bunların normalde bir akademik yıl için tam öğrenim ücreti ve önemli yaşam bursu sağladığını belirtir. Ayrıca kabul ve mali yardımın ayrı değerlendirildiği uyarısını yapar.",
        ),
    }


def main() -> None:
    original = PATH.read_text(encoding="utf-8")
    rows: list[dict[str, Any]] = json.loads(original)
    row = next(item for item in rows if item.get("id") == "caltech-galcit")

    row["scholarship_profile"] = {
        "available_types": ["departmental graduate fellowship", "external fellowship"],
        "non_eu_eligible": None,
        "details": [
            bi("The Caltech Aerospace department awards several graduate fellowships each year, primarily to entering Master's candidates with potential for doctoral study. A normal award covers full tuition and a substantial living-expense stipend for one academic year (Fall, Winter and Spring).", "Caltech Aerospace bölümü her yıl, ağırlıkla doktora çalışma potansiyeli bulunan yeni yüksek lisans adaylarına birkaç lisansüstü fellowship verir. Normal bir ödül, bir akademik yıl (Güz, Kış ve Bahar) için tam öğrenim ücretini ve önemli bir yaşam gideri bursunu kapsar."),
            bi("Admission and financial aid are considered separately; some admitted students receive no aid. Applicants who want aid must select the financial-aid box and have a complete application by the department's aid deadline. No separate fellowship form is required for this internal consideration.", "Kabul ve mali yardım ayrı değerlendirilir; bazı kabul edilen öğrenciler yardım almaz. Yardım isteyen adaylar mali yardım kutusunu seçmeli ve başvuruyu bölümün yardım son tarihine kadar eksiksiz tamamlamalıdır. Bu iç değerlendirme için ayrı fellowship formu gerekmez."),
        ],
        "external_options": [
            bi("The department lists several U.S.-citizen external fellowships as examples; they must not be presented as generally available to international applicants.", "Bölüm, ABD vatandaşı dış burs örnekleri listeler; bunlar uluslararası adaylara genel olarak açıkmış gibi sunulmamalıdır."),
        ],
        "regional_scholarship_available": None,
        "regional_scholarship_name": None,
        "scholarship_deadline": None,
        "funding_notes": bi("The checked source does not publish the current aid-deadline date. It publishes award announcements generally by 15 March and a reply deadline of 15 April; those dates are outcomes, not an application deadline.", "Kontrol edilen kaynak güncel yardım son tarihini yayımlamaz. Ödül duyurularının genel olarak 15 Mart'a, yanıt son tarihinin ise 15 Nisan'a kadar olduğunu yayımlar; bu tarihler başvuru son tarihi değil sonuç tarihleridir."),
        "verification_notes": bi("Funding is real but competitive and distinct from admission. International eligibility for the internal fellowship is not asserted because the checked public page does not publish a nationality rule.", "Finansman gerçektir ancak rekabetçidir ve kabulden ayrıdır. Kontrol edilen kamuya açık sayfa vatandaşlık kuralı yayımlamadığı için iç fellowship için uluslararası uygunluk ileri sürülmez."),
    }

    row["student_sentiment_profile"] = {
        "student_satisfaction_score": None,
        "workload_sentiment": "unknown",
        "teaching_quality_sentiment": "unknown",
        "administration_sentiment": "unknown",
        "housing_sentiment": "unknown",
        "city_life_sentiment": "unknown",
        "international_student_sentiment": "unknown",
        "career_support_sentiment": "unknown",
        "student_sentiment_summary": bi("No sufficiently sourced multi-source student-sentiment sample has been added.", "Yeterli kaynaklı ve çoklu-kaynak öğrenci duygu örneklemi eklenmemiştir."),
        "student_sentiment_sources": [],
        "sentiment_confidence": "unknown",
        "verification_notes": bi("Student perception is intentionally unknown until multiple dated independent sources are reviewed.", "Öğrenci algısı, tarihli çoklu bağımsız kaynak incelenene kadar bilerek bilinmeyendir."),
    }

    row["decision_summary"] = {
        "pros": [
            bi("The official Space Engineering programme page documents a dedicated one-year master's route with stated unit requirements and specialisation choices.", "Resmî Space Engineering program sayfası, belirtilen birim gereklilikleri ve uzmanlık seçimleri olan özel bir yıllık yüksek lisans rotasını belgeler."),
            bi("Departmental fellowship support is explicitly real and can cover a full academic year's tuition plus substantial living support for selected entering master's candidates.", "Bölümsel fellowship desteği açıkça gerçektir ve seçilen yeni yüksek lisans adayları için tam bir akademik yılın öğrenim ücretini ve önemli yaşam desteğini karşılayabilir."),
        ],
        "cons": [
            bi("Admission and funding are separate; an offer does not imply funding, and the published fellowship is competitive.", "Kabul ve finansman ayrıdır; kabul teklifi finansman anlamına gelmez ve yayımlanan fellowship rekabetçidir."),
            bi("The checked official material does not explicitly label the Space Engineering teaching language. The card therefore retains language as unknown rather than inferring it from English-proficiency requirements.", "Kontrol edilen resmî materyal Space Engineering eğitim dilini açıkça etiketlemez. Bu nedenle kart, İngilizce yeterlik şartından çıkarım yapmak yerine dili bilinmeyen olarak tutar."),
            bi("No sourced student-experience or market-rent claim is displayed.", "Kaynaklı öğrenci deneyimi veya piyasa kira iddiası gösterilmez."),
        ],
        "verdict": bi("A promising space-focused option with real but non-guaranteed departmental funding. Verify the live teaching-language statement and current aid deadline before making it a primary application choice.", "Gerçek fakat garanti edilmeyen bölümsel finansmana sahip, uzay odaklı umut verici bir seçenektir. Birincil başvuru tercihi yapmadan önce canlı eğitim dili beyanını ve güncel yardım son tarihini doğrulayın."),
    }

    profile = row.setdefault("source_profile", {})
    logs = [item for item in profile.get("source_log", []) if not (isinstance(item, dict) and item.get("url") == ADMISSIONS_URL and item.get("source_type") == "official_scholarship_page")]
    logs.append(source())
    profile["source_log"] = logs
    profile["official_scholarship_page"] = ADMISSIONS_URL
    profile["last_verified"] = CHECKED
    profile.setdefault("field_confidence", {})["scholarship"] = "high"
    profile["needs_verification"] = True
    profile["verification_status"] = "partial"

    newline = "\r\n" if "\r\n" in original else "\n"
    PATH.write_text(json.dumps(rows, ensure_ascii=False, indent=2).replace("\n", newline) + newline, encoding="utf-8")
    print("Updated Caltech Space Engineering funding evidence and removed unsourced experience claims.")


if __name__ == "__main__":
    main()
