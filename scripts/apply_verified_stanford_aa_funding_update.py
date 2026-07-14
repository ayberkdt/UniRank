"""Add qualified Stanford Engineering master's funding evidence and clear legacy claims."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data_base" / "amerika.json"
CHECKED = "2026-07-14"
FUNDING_URL = "https://engineering.stanford.edu/students-academics/student-success-and-engagement/funding-and-financial-aid/funding-your-masters"


def bi(en: str, tr: str) -> dict[str, str]:
    return {"en": en, "tr": tr}


def main() -> None:
    original = PATH.read_text(encoding="utf-8")
    rows: list[dict[str, Any]] = json.loads(original)
    row = next(item for item in rows if item.get("id") == "stanford-aa")

    row["scholarship_profile"] = {
        "available_types": ["School of Engineering master’s fellowships", "teaching or research assistantships", "external funding programmes"],
        "non_eu_eligible": None,
        "details": [
            bi("Stanford Engineering states that most departments do not guarantee master's funding. Master’s students who are not funded in an admission package may seek teaching and research assistantships.", "Stanford Engineering, çoğu bölümün yüksek lisans finansmanı garanti etmediğini belirtir. Kabul paketiyle finansman almayan yüksek lisans öğrencileri öğretim ve araştırma asistanlığı arayabilir."),
            bi("The School lists funding routes including fellowships, teaching assistantships and the Knight-Hennessy Scholars Program; each has its own eligibility and process. Do not treat a listed programme as an AA-MS award guarantee.", "Okul; fellowship'ler, öğretim asistanlıkları ve Knight-Hennessy Scholars Programı dahil finansman yolları listeler; her birinin kendi uygunluk ve süreci vardır. Listelenen bir programı AA-MS ödül garantisi olarak görmeyin."),
        ],
        "external_options": [],
        "regional_scholarship_available": None,
        "regional_scholarship_name": None,
        "scholarship_deadline": None,
        "funding_notes": bi("No AA-specific funding quantity, eligibility rule, award amount or deadline is claimed because the checked source is School-wide. Verify the live AA and individual programme pages before building a funding plan.", "Kontrol edilen kaynak okul geneli olduğu için AA'ya özgü finansman sayısı, uygunluk kuralı, ödül tutarı veya son tarih ileri sürülmez. Finansman planı yapmadan önce canlı AA ve tekil program sayfalarını doğrulayın."),
        "verification_notes": bi("Funding availability is documented; certainty of funding is explicitly not. International eligibility is left unknown unless a particular funding programme publishes it.", "Finansman olanağı belgelenmiştir; finansman kesinliği açıkça belgelenmemiştir. Belirli bir finansman programı yayımlamadıkça uluslararası uygunluk bilinmeyen bırakılır."),
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
            bi("The existing official curriculum source defines a 45-unit AA master's structure and the existing cost source supplies a 2026/27 planning budget.", "Mevcut resmî müfredat kaynağı 45 birimlik AA yüksek lisans yapısını tanımlar; mevcut maliyet kaynağı 2026/27 planlama bütçesini sunar."),
            bi("School-level pathways to fellowships and teaching/research assistantships are documented for master's students.", "Yüksek lisans öğrencileri için okul düzeyinde fellowship ile öğretim/araştırma asistanlığı yolları belgelenmiştir."),
        ],
        "cons": [
            bi("Most departments do not guarantee master's funding; an assistantship search is not an award.", "Çoğu bölüm yüksek lisans finansmanı garanti etmez; asistanlık araması ödül değildir."),
            bi("The current 2026/27 official non-tuition graduate budget is substantial, and the on-campus rent allowance is a budget figure rather than an available-room quote.", "Güncel 2026/27 resmî öğrenim ücreti dışı lisansüstü bütçesi yüksektir; kampüs içi kira ödeneği mevcut oda fiyatı değil bütçe tutarıdır."),
            bi("The checked official AA material does not expressly label teaching language, so it remains unknown rather than inferred from English-proficiency policy.", "Kontrol edilen resmî AA materyali eğitim dilini açıkça etiketlemez; bu nedenle İngilizce yeterlik politikasından çıkarım yapmak yerine bilinmeyen kalır."),
        ],
        "verdict": bi("A source-grounded choice when the published curriculum and high verified budget fit your plan, but master’s funding must be treated as competitive and programme-specific until an actual offer is received.", "Yayımlanmış müfredat ve yüksek doğrulanmış bütçe planınıza uyuyorsa kaynak temelli bir tercihtir; ancak yüksek lisans finansmanı gerçek bir teklif alınana kadar rekabetçi ve programa özgü kabul edilmelidir."),
    }

    profile = row.setdefault("source_profile", {})
    logs = [item for item in profile.get("source_log", []) if not (isinstance(item, dict) and item.get("url") == FUNDING_URL and item.get("source_type") == "official_scholarship_page")]
    logs.append({
        "url": FUNDING_URL,
        "title": "Stanford School of Engineering: Funding Your Master's Degree",
        "source_type": "official_scholarship_page",
        "access_status": "ok",
        "last_checked": CHECKED,
        "relevant_fields": ["scholarship", "funding"],
        "confidence": "high",
        "notes": bi("Official School-wide master's funding page explains that most departments do not guarantee funding and lists fellowship plus teaching/research-assistantship pathways.", "Resmî okul geneli yüksek lisans finansman sayfası, çoğu bölümün finansmanı garanti etmediğini açıklar ve fellowship ile öğretim/araştırma asistanlığı yollarını listeler."),
    })
    profile["source_log"] = logs
    profile["official_scholarship_page"] = FUNDING_URL
    profile["last_verified"] = CHECKED
    profile.setdefault("field_confidence", {})["scholarship"] = "high"
    profile["needs_verification"] = True
    profile["verification_status"] = "partial"

    newline = "\r\n" if "\r\n" in original else "\n"
    PATH.write_text(json.dumps(rows, ensure_ascii=False, indent=2).replace("\n", newline) + newline, encoding="utf-8")
    print("Updated Stanford AA funding evidence and removed unsourced experience claims.")


if __name__ == "__main__":
    main()
