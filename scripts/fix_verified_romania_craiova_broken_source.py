"""Remove an inaccessible Craiova scholarship notice and dependent claims."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data_base" / "romania.json"
RECORD_ID = "ro-university-craiova-complex-systems-aerospace-engineering-msc"
SOURCE_ID = "ro_ucv_performance_scholarship_2025_26"


def main() -> None:
    records = json.loads(DB_PATH.read_text(encoding="utf-8"))
    record = next(item for item in records if item.get("id") == RECORD_ID)

    source_profile = record["source_profile"]
    source_profile["source_log"] = [
        source
        for source in source_profile["source_log"]
        if source.get("source_id") != SOURCE_ID
    ]
    source_profile["checked_source_count"] = len(source_profile["source_log"])
    source_profile["checked_official_source_count"] = sum(
        1 for source in source_profile["source_log"] if source.get("official") is True
    )

    # Restore the two sourced tuition rows if an earlier compatibility pass
    # removed them. These amounts are explicitly published on the current
    # official non-EU admission page.
    record["cost_profile"]["tuition_items"] = [
        {
            "amount": 3500,
            "minimum": None,
            "maximum": None,
            "currency": "EUR",
            "period": "academic_year",
            "applicant_scope": "non_eu_self_funded_aerospace_engineering_master",
            "academic_cycle": "2026/2027",
            "mandatory": True,
            "basis": "UCV non-EU technical-field fee table",
            "source_ids": ["ro_ucv_noneu_admission_2026"],
        },
        {
            "amount": 2500,
            "minimum": None,
            "maximum": None,
            "currency": "EUR",
            "period": "one_academic_year",
            "applicant_scope": "non_eu_candidate_requiring_romanian_preparatory_year",
            "academic_cycle": "2026/2027",
            "mandatory": False,
            "basis": "UCV non-EU technical-field Romanian preparatory-year fee",
            "source_ids": [
                "ro_ucv_noneu_admission_2026",
                "ro_ucv_preparatory_year_2026",
            ],
        },
    ]

    scholarship_sources = source_profile["evidence_map"]["scholarship"]
    source_profile["evidence_map"]["scholarship"] = [
        source_id for source_id in scholarship_sources if source_id != SOURCE_ID
    ]

    record["scholarship_profile"]["notes"] = {
        "en": (
            "The published non-EU admission route is self-funded and requires tuition payment. "
            "No accessible current official source was found that establishes eligibility for a "
            "UCV institutional award, so the applicant should budget as unfunded unless a separate "
            "award is formally secured."
        ),
        "tr": (
            "Yayımlanan AB dışı kabul rotası kendi hesabına ücretlidir ve öğrenim ücreti ödemesi "
            "gerektirir. UCV kurum-içi bursuna uygunluğu kanıtlayan erişilebilir güncel resmî kaynak "
            "bulunamadığından aday, ayrı bir bursu resmen kazanmadıkça finansmansız bütçe yapmalıdır."
        ),
    }

    record["scholarship_profile"]["non_eu_eligibility_summary"] = {
        "en": (
            "The standard UCV non-EU route is self-funded; its published admission instructions do "
            "not describe automatic scholarship consideration. The MFA scholarship is a separate "
            "national competition and may assign an alternative institution in the same field if "
            "the preferred option cannot be honoured."
        ),
        "tr": (
            "Standart UCV AB dışı rotası kendi hesabına ücretlidir; yayımlanan kabul talimatları "
            "otomatik burs değerlendirmesi tanımlamaz. Dışişleri bursu ayrı bir ulusal yarışmadır; "
            "tercih karşılanamazsa aynı alanda alternatif kurum atanabilir."
        ),
    }
    record["scholarship_profile"]["application_mode"] = "separate"
    record["living_profile"]["housing_access"] = "not_guaranteed"
    record["language_profile"]["language_risk"] = "high"
    record["decision_summary"]["funding_reality"] = {
        "en": (
            "Standard admission is self-funded, and the published route does not describe automatic "
            "scholarship consideration. The meaningful full-funding route is the separate, highly "
            "competitive Romanian MFA scholarship, whose 2026 deadline was 31 March and whose final "
            "institution assignment is not guaranteed."
        ),
        "tr": (
            "Standart kabul kendi hesabına ücretlidir ve yayımlanan rota otomatik burs değerlendirmesi "
            "tanımlamaz. Anlamlı tam finansman rotası ayrı ve çok rekabetçi Romanya Dışişleri bursudur; "
            "2026 son tarihi 31 Mart'tı ve nihai kurum ataması garanti değildir."
        ),
    }
    record["data_quality"]["checked_official_source_count"] = source_profile[
        "checked_official_source_count"
    ]

    if any(
        SOURCE_ID in json.dumps(source, ensure_ascii=False)
        for source in source_profile["source_log"]
    ):
        raise RuntimeError("Broken source survived source-log cleanup")
    if SOURCE_ID in json.dumps(record, ensure_ascii=False):
        raise RuntimeError("Broken source survived record cleanup")

    DB_PATH.write_text(
        json.dumps(records, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        f"Removed {SOURCE_ID}; Craiova now has "
        f"{source_profile['checked_source_count']} checked sources."
    )


if __name__ == "__main__":
    main()
