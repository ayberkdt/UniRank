"""Attach checked university-wide teaching-language policies to UK programmes.

These updates are deliberately limited to programmes for which the university
has an explicit, accessible institutional instruction-language statement.  A
general policy is recorded separately from the programme page and carries a
conservative confidence level where the policy permits exceptions.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data_base" / "ingiltere.json"
CHECKED = "2026-07-14"


def bilingual(en: str, tr: str) -> dict[str, str]:
    return {"en": en, "tr": tr}


def find(rows: list[dict[str, Any]], record_id: str) -> dict[str, Any]:
    for row in rows:
        if row.get("id") == record_id:
            return row
    raise KeyError(record_id)


def policy_source(url: str, title: str, notes_en: str, notes_tr: str, *, access_status: str, confidence: str) -> dict[str, Any]:
    return {
        "url": url,
        "title": title,
        "source_type": "official_university_policy_page",
        "access_status": access_status,
        "last_checked": CHECKED,
        "relevant_fields": ["language"],
        "confidence": confidence,
        "notes": bilingual(notes_en, notes_tr),
    }


def living_source(url: str, title: str, notes_en: str, notes_tr: str) -> dict[str, Any]:
    return {
        "url": url,
        "title": title,
        "source_type": "official_cost_of_living_page",
        "access_status": "ok",
        "last_checked": CHECKED,
        "relevant_fields": ["housing", "living"],
        "confidence": "high",
        "notes": bilingual(notes_en, notes_tr),
    }


def apply(record: dict[str, Any], source: dict[str, Any], *, confidence: str, notes_en: str, notes_tr: str) -> None:
    record["teaching_language"] = ["English"]
    language = record.setdefault("language_profile", {})
    language.update({
        "teaching_language": ["English"],
        "english_required": True,
        "language_risk": "low" if confidence == "high" else "medium",
        "verification_notes": bilingual(notes_en, notes_tr),
    })
    profile = record.setdefault("source_profile", {})
    logs = [item for item in profile.get("source_log", []) if isinstance(item, dict)]
    logs = [item for item in logs if item.get("url") != source["url"]]
    logs.append(source)
    profile["source_log"] = logs
    profile.setdefault("field_confidence", {})["language"] = confidence
    profile["last_verified"] = CHECKED


def apply_living(record: dict[str, Any], source: dict[str, Any], *, cost_updates: dict[str, Any], living_updates: dict[str, Any]) -> None:
    record.setdefault("cost_profile", {}).update(cost_updates)
    record.setdefault("living_profile", {}).update(living_updates)
    profile = record.setdefault("source_profile", {})
    logs = [item for item in profile.get("source_log", []) if isinstance(item, dict)]
    logs = [item for item in logs if item.get("url") != source["url"]]
    logs.append(source)
    profile["source_log"] = logs
    profile.setdefault("field_confidence", {})["housing"] = "high"
    profile["last_verified"] = CHECKED


def write(rows: list[dict[str, Any]], original: str) -> None:
    match = re.search(r"^\s*\[\r?\n( +)\{", original)
    indent = len(match.group(1)) if match else 4
    newline = "\r\n" if "\r\n" in original else "\n"
    PATH.write_bytes((json.dumps(rows, ensure_ascii=False, indent=indent).replace("\n", newline) + newline).encode("utf-8"))


def main() -> None:
    original = PATH.read_bytes().decode("utf-8")
    rows = json.loads(original)

    apply(
        find(rows, "university-college-london"),
        policy_source(
            "https://www.ucl.ac.uk/library/about-us/policies/ucl-library-services-collection-management-policy",
            "UCL Library Services Collection Management Policy",
            "Updated May 2026. UCL's policy states that English is its language of instruction, except for disciplinary language-programme requirements. The recorded Space Science MSc is not a language degree.",
            "Mayıs 2026 güncellemeli UCL politikası, disipline özgü dil-programı istisnaları dışında eğitim dilinin İngilizce olduğunu belirtir. Kayıttaki Space Science MSc bir dil derecesi değildir.",
            access_status="ok",
            confidence="high",
        ),
        confidence="high",
        notes_en="UCL's current institutional policy identifies English as the language of instruction except for language-programme requirements; this Space Science MSc has no such language-degree designation on its programme page.",
        notes_tr="UCL'nin güncel kurumsal politikası, dil-programı şartları dışındaki eğitim dilini İngilizce olarak tanımlar; bu Space Science MSc'nin program sayfasında böyle bir dil derecesi tanımı yoktur.",
    )
    apply(
        find(rows, "university-of-oxford"),
        policy_source(
            "https://www.wrh.ox.ac.uk/faqs-1/how-strict-are-the-requirements-for-english-language-qualifications-for-overseas-students",
            "University of Oxford: English Language Qualifications FAQ",
            "Oxford states that English is the language of instruction for all courses, except a small minority where regulations provide otherwise. The checked MSc by Research page separately specifies a higher English requirement.",
            "Oxford, düzenlemelerin aksini belirttiği küçük bir azınlık dışında tüm derslerin eğitim dilinin İngilizce olduğunu belirtir. Kontrol edilen MSc by Research sayfası ayrıca yüksek İngilizce şartı belirtir.",
            access_status="ok",
            confidence="medium",
        ),
        confidence="medium",
        notes_en="Oxford's institutional statement covers all courses subject to a small regulatory-exception caveat; the MSc by Research course page requires Oxford's higher English level. The medium confidence preserves that caveat.",
        notes_tr="Oxford'un kurumsal beyanı, küçük düzenleme istisnası kaydıyla tüm dersleri kapsar; MSc by Research sayfası Oxford'un yüksek İngilizce düzeyini ister. Orta güven düzeyi bu kaydı korur.",
    )
    apply(
        find(rows, "university-of-manchester"),
        policy_source(
            "https://documents.manchester.ac.uk/display.aspx?DocID=39973",
            "University of Manchester General Regulation XII",
            "The regulation states that the University's language of instruction is English unless a particular programme regulation provides otherwise. No contrary provision was found in the checked Aerospace MSc programme record.",
            "Düzenleme, belirli bir program düzenlemesi aksini söylemedikçe Üniversitenin eğitim dilinin İngilizce olduğunu belirtir. Kontrol edilen Aerospace MSc program kaydında aksine bir hüküm bulunmadı.",
            access_status="pdf",
            confidence="medium",
        ),
        confidence="medium",
        notes_en="Manchester's official regulation makes English the default instruction language, subject to programme-specific exceptions. The medium confidence reflects that general-policy scope.",
        notes_tr="Manchester'ın resmî düzenlemesi, programa özgü istisnalara tabi olarak İngilizceyi varsayılan eğitim dili yapar. Orta güven düzeyi genel politika kapsamını yansıtır.",
    )
    apply_living(
        find(rows, "university-college-london"),
        living_source(
            "https://www.ucl.ac.uk/study/prospective-students/graduate/funding-your-masters/paying-your-degree?year=living-costs",
            "UCL: Paying for Your Degree and Living Costs",
            "For a graduate course, UCL gives an around GBP 20,000 living-cost guide covering accommodation, food, travel and daily costs; it is not rent alone or a guaranteed personal total.",
            "UCL, lisansüstü eğitim için konaklama, yiyecek, ulaşım ve günlük giderleri kapsayan yaklaşık 20.000 GBP yaşam maliyeti rehberi verir; bu yalnız kira veya garantili kişisel toplam değildir.",
        ),
        cost_updates={
            "living_cost_gbp_per_year": 20000,
            "living_cost_basis": bilingual("UCL graduate living-cost guide; accommodation, food, travel and daily costs included.", "UCL lisansüstü yaşam maliyeti rehberi; konaklama, yiyecek, ulaşım ve günlük giderler dâhil."),
        },
        living_updates={
            "living_cost_risk": "high",
            "verification_notes": bilingual("UCL's official guide gives an approximately GBP 20,000 annual graduate living-cost figure; it is a planning guide, not an accommodation offer.", "UCL'nin resmî rehberi lisansüstü için yaklaşık yıllık 20.000 GBP yaşam maliyeti verir; bu bir planlama rehberidir, konaklama teklifi değildir."),
        },
    )
    apply_living(
        find(rows, "university-of-oxford"),
        living_source(
            "https://www.ox.ac.uk/admissions/graduate/fees-and-funding/living-costs",
            "Oxford Graduate Living Costs 2026–27",
            "Oxford publishes GBP 1,405–2,105 monthly living costs for a single full-time graduate in 2026–27, including GBP 825–990 monthly accommodation.",
            "Oxford, 2026–27 için tek ve tam zamanlı bir lisansüstü öğrenciye aylık 1.405–2.105 GBP yaşam maliyeti, bunun içinde aylık 825–990 GBP konaklama yayımlar.",
        ),
        cost_updates={
            "living_cost_gbp_per_year": None,
        },
        living_updates={
            "average_room_rent_gbp_per_month_min": 825,
            "average_room_rent_gbp_per_month_max": 990,
            "monthly_living_cost_gbp_per_month_min": 1405,
            "monthly_living_cost_gbp_per_month_max": 2105,
            "living_cost_risk": "high",
            "housing_notes": bilingual("Oxford's 2026–27 accommodation range is part of its single full-time graduate living-cost budget; it is a planning range, not a room offer.", "Oxford'un 2026–27 konut aralığı, tek ve tam zamanlı lisansüstü yaşam maliyeti bütçesinin parçasıdır; oda teklifi değil, planlama aralığıdır."),
        },
    )
    write(rows, original)
    print("Updated UCL, Oxford and Manchester language policies.")


if __name__ == "__main__":
    main()
