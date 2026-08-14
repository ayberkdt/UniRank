"""Add current 2026/27 official CTU Prague housing evidence to the Avionics MSc."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from unirank.core.integrity import audit_record


PATH = ROOT / "data_base" / "cekya.json"
RECORD_ID = "cz-ctu-aerospace-engineering-avionics-msc"
CHECKED = "2026-08-14"
PRICE_PAGE = "https://suz.cvut.cz/en/dormitory-accommodation/price-list-documents"
ESTIMATED_COST = "https://www.suz.cvut.cz/cz/media/file/students-estimated-financial-cost-valid-9-7-2026"
FAQ = "https://www.suz.cvut.cz/en/dormitory-accommodation/faq"
RESERVATION = "https://www.suz.cvut.cz/en/media/file/methodology-accommodation-reservations-ay-2026-2027"
FEE_LIFE = "https://fel.cvut.cz/en/admissions/life-at-fee-ctu"


def bi(en: str, tr: str) -> dict[str, str]:
    return {"en": en, "tr": tr}


def source(url: str, title: str, source_type: str, fields: list[str], en: str, tr: str, *, access_status: str = "ok") -> dict:
    return {
        "url": url,
        "source_type": source_type,
        "title": title,
        "access_status": access_status,
        "last_checked": CHECKED,
        "relevant_fields": fields,
        "confidence": "high",
        "notes": bi(en, tr),
    }


def upsert_sources(profile: dict, additions: list[dict]) -> None:
    log = profile.setdefault("source_log", [])
    by_key = {(item.get("url"), item.get("source_type")): i for i, item in enumerate(log) if isinstance(item, dict)}
    for item in additions:
        key = (item["url"], item["source_type"])
        if key in by_key:
            log[by_key[key]] = item
        else:
            by_key[key] = len(log)
            log.append(item)


def update(row: dict) -> None:
    row["living_profile"].update(
        {
            "city_cost_level": "medium_high",
            "monthly_living_cost_eur_min": None,
            "monthly_living_cost_eur_max": None,
            "monthly_living_cost_eur_estimated": None,
            "housing_difficulty": "high",
            "student_housing_available": True,
            "housing_access": "not_guaranteed",
            "housing_allocation_mode": "competitive_separate_reservation",
            "housing_application_separate": True,
            "housing_booking_system": "ISKAM4",
            "average_room_rent_eur": None,
            "average_room_rent_eur_min": None,
            "average_room_rent_eur_max": None,
            "average_room_rent_czk_min": 4180,
            "average_room_rent_czk_max": 7435,
            "rent_currency": "CZK",
            "rent_period": "October 2026 example including electricity advance",
            "living_risk": "high",
            "housing_options": [
                {
                    "provider": "SFA CTU in Prague",
                    "room_type": "bed in a double room",
                    "academic_year": "2026/2027",
                    "booking_system": "ISKAM4",
                    "guaranteed": False,
                    "visa_confirmation_available": True,
                }
            ],
            "official_rent_items": [
                {"dormitory": "Strahov", "monthly_example_czk": [4180, 5420, 6009], "month": "October 2026", "includes": "electricity advance"},
                {"dormitory": "Podolí", "monthly_example_czk": 5203, "month": "October 2026", "includes": "electricity advance"},
                {"dormitory": "Masarykova", "monthly_example_czk": 6629, "month": "October 2026", "includes": "electricity advance"},
                {"dormitory": "Bubeneč", "monthly_example_czk": 7435, "month": "October 2026", "includes": "electricity advance"},
                {"dormitory": "Sinkuleho", "monthly_example_czk": 4986, "month": "October 2026", "includes": "electricity advance"},
                {"dormitory": "Hlávkova", "monthly_example_czk": 5420, "month": "October 2026", "includes": "electricity advance"},
                {"dormitory": "Orlík", "monthly_example_czk": 7032, "month": "October 2026", "includes": "electricity advance"},
                {"dormitory": "Dejvická", "monthly_example_czk": 6009, "month": "October 2026", "includes": "electricity advance"},
            ],
            "official_living_cost_items": [
                {
                    "item": "initial September accommodation outlay example",
                    "amount_czk_min": 7330,
                    "amount_czk_max": 12895,
                    "components": ["September accommodation", "30-day accommodation deposit adjustment", "annual insurance", "electricity advance"],
                    "scope": "listed common double-room examples",
                }
            ],
            "housing_notes": bi(
                "CTU's 2026/27 examples show CZK 4,180–7,435 for October for a bed in a double room, including the electricity advance. The September start-outlay examples are CZK 7,330–12,895 because deposits and insurance are due. Availability and a specific dormitory are not guaranteed.",
                "CTU'nun 2026/27 örnekleri çift kişilik odada bir yatak için elektrik avansı dâhil Ekim ayında 4.180–7.435 CZK gösterir. Depozito ve sigorta nedeniyle Eylül başlangıç ödeme örnekleri 7.330–12.895 CZK'dır. Yer ve belirli bir yurt garanti edilmez.",
            ),
            "verification_notes": bi(
                "These are official 2026/27 dormitory examples in CZK, not a Prague private-market average and not converted to EUR. A complete monthly food/personal-expense total is not inferred.",
                "Bunlar CZK cinsinden resmî 2026/27 yurt örnekleridir; Prag özel piyasa ortalaması değildir ve EUR'ya çevrilmez. Tam aylık yemek/kişisel gider toplamı türetilmez.",
            ),
        }
    )

    profile = row["source_profile"]
    upsert_sources(
        profile,
        [
            source(PRICE_PAGE, "CTU SFA price lists and 2026/27 accommodation documents", "official_housing_page", ["housing", "living"], "Current official index links the September 2026 dormitory price list, cost tool and 2026/27 rules.", "Güncel resmî dizin Eylül 2026 yurt tarifesine, maliyet aracına ve 2026/27 kurallarına bağlantı verir."),
            source(ESTIMATED_COST, "CTU student estimated accommodation cost valid 7 September 2026", "official_housing_page", ["housing", "living"], "Publishes dormitory-specific double-room daily prices, October totals, deposits, insurance and September start costs.", "Yurda özgü çift kişilik oda günlük fiyatlarını, Ekim toplamlarını, depozitoyu, sigortayı ve Eylül başlangıç maliyetlerini yayımlar.", access_status="pdf"),
            source(FAQ, "CTU SFA dormitory FAQ", "official_housing_page", ["housing"], "Explains which tariff applies to students, variable daily billing and visa-confirmation contact mechanics.", "Öğrencilere hangi tarifenin uygulandığını, değişken günlük faturalamayı ve vize teyit iletişim yöntemini açıklar."),
            source(RESERVATION, "CTU 2026/27 dormitory reservation methodology", "official_housing_page", ["housing", "deadline"], "Current academic-year document verifies that accommodation is allocated through a separate reservation process.", "Güncel akademik yıl belgesi konutun ayrı bir rezervasyon süreciyle tahsis edildiğini doğrular.", access_status="pdf"),
            source(FEE_LIFE, "Life at FEE CTU", "official_cost_of_living_page", ["housing", "living", "scholarship"], "Faculty guidance corroborates dormitory/private-accommodation planning and the approximate automatic housing scholarship.", "Fakülte rehberi yurt/özel konut planlamasını ve yaklaşık otomatik konut bursunu doğrular."),
        ],
    )
    profile["official_housing_page"] = PRICE_PAGE
    profile["official_cost_of_living_page"] = FEE_LIFE
    profile["last_verified"] = CHECKED
    profile.setdefault("field_confidence", {}).update({"housing": "high", "living": "high"})

    row["scholarship_profile"]["automatic_housing_scholarship_czk_per_month_approx"] = 500
    row["scholarship_profile"]["automatic_housing_scholarship_scope"] = "all FEE students according to current faculty guidance"

    quality = audit_record(row)
    quality["audited_at"] = CHECKED
    row["data_quality"] = quality
    complete = quality["status"] == "verified"
    row["quality_control"] = {
        "qc_status": "passed" if complete else "needs_revision",
        "checked_at": CHECKED,
        "failed_canary_tests": [] if complete else ["missing_or_unverified_critical_fields"],
        "remaining_verification_tasks": [],
        "qc_notes": bi(
            "All core decision fields have checked official evidence; housing figures remain explicitly scoped to dormitory examples.",
            "Tüm temel karar alanlarında kontrol edilmiş resmî kanıt vardır; konut rakamlarının kapsamı açıkça yurt örnekleriyle sınırlıdır.",
        ),
    }
    profile["needs_verification"] = not complete


def main() -> None:
    payload = json.loads(PATH.read_text(encoding="utf-8"))
    rows = payload if isinstance(payload, list) else payload.get("universities", payload.get("programs", []))
    target = next(row for row in rows if row.get("id") == RECORD_ID)
    update(target)
    if isinstance(payload, dict):
        payload["last_updated"] = CHECKED
    PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(target["data_quality"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
