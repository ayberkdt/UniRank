"""Apply the UniRank categorical standards to every database record.

The database grew organically, so the same idea was stored in several
incompatible ways: housing difficulty as free text that mixed a level with
its reason, living costs as bare numbers with no period or currency basis,
and academic fit as a single adjective.  This script rewrites those into the
structures defined by ``config/standards.json``.

It is deliberately conservative.  Every derived value records the field it
came from, and anything that cannot be derived from data already present in
the record becomes ``unknown`` with a machine-readable reason instead of a
guess.  Nothing here invents a fact.

Usage::

    python scripts/standardize_categories.py            # report only
    python scripts/standardize_categories.py --write    # rewrite the JSON files
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data_base"
STANDARDS_PATH = ROOT / "config" / "standards.json"
FX_PATH = ROOT / "config" / "fx_rates.json"
SKIP_FILES = {"taxonomy.json"}

STANDARDS = json.loads(STANDARDS_PATH.read_text(encoding="utf-8"))
FX = json.loads(FX_PATH.read_text(encoding="utf-8"))
STANDARDS_VERSION = STANDARDS["standards_version"]
TODAY = date.today().isoformat()

CURRENCY_SUFFIXES = ("usd", "gbp", "chf", "sek", "dkk", "nok", "eur", "pln", "czk", "jpy", "krw", "cny", "ron", "try", "huf")


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------

def load_records(path: Path) -> tuple[Any, list[dict[str, Any]]]:
    """Return the parsed document and the list of programme records inside it."""
    document = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(document, list):
        return document, [r for r in document if isinstance(r, dict)]
    if isinstance(document, dict):
        for key in ("programs", "universities", "records"):
            value = document.get(key)
            if isinstance(value, list):
                return document, [r for r in value if isinstance(r, dict)]
    return document, []


def text_of(value: Any) -> str:
    """Flatten a bilingual object, list or scalar into searchable lowercase text."""
    if value is None:
        return ""
    if isinstance(value, str):
        return value.lower()
    if isinstance(value, dict):
        return " ".join(text_of(item) for item in value.values())
    if isinstance(value, (list, tuple)):
        return " ".join(text_of(item) for item in value)
    return str(value).lower()


def number(value: Any) -> float | None:
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    try:
        return float(str(value).replace(",", "").strip())
    except (TypeError, ValueError):
        return None


def verified_fields(record: dict[str, Any]) -> set[str]:
    quality = record.get("data_quality") or {}
    fields = quality.get("verified_fields")
    return {str(f) for f in fields} if isinstance(fields, list) else set()


def non_empty_list(value: Any) -> list:
    return [item for item in value if item] if isinstance(value, list) else []


def to_eur(amount: float | None, currency: str) -> dict[str, Any] | None:
    """Convert a published amount to a clearly labelled euro comparison."""
    rate = FX["rates"].get(currency.upper())
    if amount is None or not rate:
        return None
    return {
        "amount": round(amount / rate, 2),
        "currency": "EUR",
        "is_conversion": True,
        "fx_rate": rate,
        "fx_rate_date": FX["rate_date"],
        "fx_source": FX["source"],
    }


# --------------------------------------------------------------------------
# 1. housing difficulty
# --------------------------------------------------------------------------

HOUSING_SCALE = STANDARDS["housing_difficulty"]
HOUSING_DIMENSIONS = {d["key"]: d for d in HOUSING_SCALE["scoring_dimensions"]}
HOUSING_LEVELS = [level for level in HOUSING_SCALE["levels"] if level["rank"]]

GUARANTEE_FROM_ACCESS = {
    "guaranteed": "guaranteed",
    "priority": "priority",
    "lottery": "lottery",
    "first_come_first_served": "first_come_first_served",
    "waitlist": "waitlist",
    "not_guaranteed": "not_guaranteed",
    "not_offered": "not_offered",
}

# Legacy free-text values are mapped to a level only where the text states the
# level unambiguously.  Anything conditional keeps its text as the reason and
# is re-derived from the structured evidence instead.
LEGACY_LEVEL_PATTERNS = [
    (re.compile(r"^very[_ ]high$|cannot house|structural shortage"), "very_high"),
    (re.compile(r"^high$|^high[_ ]"), "high"),
    (re.compile(r"^medium$|^moderate$|^medium[_ ]"), "medium"),
    (re.compile(r"^low$|^low[_ ]"), "low"),
]

SHORTAGE_PATTERNS = [
    (re.compile(r"cannot (guarantee|house) (most|all|the majority)|not able to house"), "cannot_house_most_internationals_stated", 4),
    (re.compile(r"demand (far )?exceeds|more applicants than (rooms|places)|oversubscribed"), "demand_exceeds_supply_stated", 3),
    (re.compile(r"wait(ing)?[ _-]?list|queue days|waiting time"), "published_waiting_list", 2),
    (re.compile(r"apply (as )?early|start (your )?search early|book early|as soon as possible"), "early_application_advised", 1),
]

ARRIVAL_PATTERNS = [
    (re.compile(r"do not travel|not to travel|before you have (a )?(signed )?contract|do not come .* without"), "officially_advised_not_to_travel_without_contract", 2),
    (re.compile(r"temporary (housing|accommodation)|hostel|short[- ]term accommodation on arrival"), "temporary_housing_commonly_needed", 1),
]


def housing_evidence_text(record: dict[str, Any]) -> str:
    living = record.get("living_profile") or {}
    return " ".join(
        text_of(living.get(key))
        for key in ("housing_notes", "verification_notes", "housing_eligibility", "housing_selection_method", "student_housing_competitiveness")
    )


def derive_guarantee_status(living: dict[str, Any]) -> tuple[str | None, str | None]:
    access = str(living.get("housing_access") or "").strip().lower()
    if access in GUARANTEE_FROM_ACCESS:
        return GUARANTEE_FROM_ACCESS[access], "living_profile.housing_access"
    guaranteed = living.get("housing_guaranteed")
    if guaranteed is True:
        return "guaranteed", "living_profile.housing_guaranteed"
    if guaranteed is False:
        return "not_guaranteed", "living_profile.housing_guaranteed"
    options = non_empty_list(living.get("housing_options"))
    if options and all(option.get("guaranteed") is False for option in options if isinstance(option, dict)):
        return "not_guaranteed", "living_profile.housing_options[].guaranteed"
    if living.get("student_housing_available") is False:
        return "not_offered", "living_profile.student_housing_available"
    return None, None


def derive_supply_pressure(record: dict[str, Any]) -> tuple[str | None, str | None]:
    haystack = housing_evidence_text(record)
    for pattern, value, _points in SHORTAGE_PATTERNS:
        if pattern.search(haystack):
            return value, "official note text in living_profile"
    competitiveness = str((record.get("living_profile") or {}).get("student_housing_competitiveness") or "").strip().lower()
    if competitiveness in {"very high", "very_high"}:
        return "demand_exceeds_supply_stated", "living_profile.student_housing_competitiveness"
    if competitiveness == "high":
        return "published_waiting_list", "living_profile.student_housing_competitiveness"
    if competitiveness in {"medium", "low"}:
        return "early_application_advised" if competitiveness == "medium" else "no_documented_shortage", "living_profile.student_housing_competitiveness"
    return None, None


def derive_timing_sensitivity(living: dict[str, Any]) -> tuple[str | None, str | None]:
    separate = living.get("housing_application_separate")
    dated = any(
        living.get(key)
        for key in ("housing_deadline", "initial_selection_registration_2026", "initial_individual_selection_2026", "housing_application_deadline")
    )
    if separate is True and dated:
        return "separate_application_hard_deadline", "living_profile.housing_application_separate + published housing dates"
    if separate is True:
        return "separate_application_generous_window", "living_profile.housing_application_separate"
    if separate is False:
        return "no_separate_application", "living_profile.housing_application_separate"
    return None, None


def derive_arrival_risk(record: dict[str, Any]) -> tuple[str | None, str | None]:
    haystack = housing_evidence_text(record)
    for pattern, value, _points in ARRIVAL_PATTERNS:
        if pattern.search(haystack):
            return value, "official note text in living_profile"
    return None, None


def monthly_rent_range(living: dict[str, Any]) -> tuple[float | None, str | None]:
    """Return the highest published monthly rent and its currency."""
    for currency in CURRENCY_SUFFIXES:
        upper = number(living.get(f"monthly_housing_rent_{currency}_per_month_max")) or number(living.get(f"average_room_rent_{currency}_per_month_max"))
        if upper is not None:
            return upper, currency.upper()
    upper = number(living.get("average_room_rent_eur_max")) or number(living.get("average_room_rent_eur"))
    if upper is not None:
        return upper, "EUR"
    return None, None


def official_monthly_housing_budget(record: dict[str, Any]) -> tuple[float | None, str | None]:
    living = record.get("living_profile") or {}
    months = number(living.get("housing_budget_months")) or 12
    for currency in CURRENCY_SUFFIXES:
        annual = number(living.get(f"housing_budget_{currency}_per_year"))
        if annual is not None and months:
            return annual / months, currency.upper()
    annual = number((record.get("cost_profile") or {}).get("coa_housing_usd_9_month"))
    if annual is not None:
        return annual / 9, "USD"
    return None, None


def derive_affordability_gap(record: dict[str, Any]) -> tuple[str | None, str | None]:
    living = record.get("living_profile") or {}
    rent, rent_currency = monthly_rent_range(living)
    budget, budget_currency = official_monthly_housing_budget(record)
    if rent is None or budget is None or not budget or rent_currency != budget_currency:
        return None, None
    ratio = rent / budget
    if ratio <= 1.0:
        value = "at_or_below_budget"
    elif ratio <= 1.25:
        value = "up_to_25_percent_above"
    elif ratio <= 1.6:
        value = "25_to_60_percent_above"
    else:
        value = "more_than_60_percent_above"
    return value, f"published rent max vs official housing budget ({rent_currency})"


def build_housing_difficulty(record: dict[str, Any]) -> dict[str, Any]:
    living = record.setdefault("living_profile", {})
    legacy = living.get("housing_difficulty") or living.get("housing_search_difficulty")

    derivations = {
        "guarantee_status": derive_guarantee_status(living),
        "supply_pressure": derive_supply_pressure(record),
        "market_affordability_gap": derive_affordability_gap(record),
        "timing_sensitivity": derive_timing_sensitivity(living),
        "arrival_risk": derive_arrival_risk(record),
    }

    # Researched evidence carries a quote and a source url, so it always wins
    # over the text heuristics above.
    researched = living.get("housing_difficulty_evidence")
    if isinstance(researched, dict):
        for key, entry in researched.items():
            if key not in HOUSING_DIMENSIONS or not isinstance(entry, dict):
                continue
            value = entry.get("value")
            if value in HOUSING_DIMENSIONS[key]["values"]:
                derivations[key] = (value, entry.get("source_url") or "researched_official_source")

    dimensions: dict[str, Any] = {}
    score = 0
    evidenced_weight = 0
    evidenced = 0
    for key, (value, origin) in derivations.items():
        spec = HOUSING_DIMENSIONS[key]
        if value is None:
            dimensions[key] = {"value": None, "points": None, "derived_from": None, "reason": "not_published_in_record"}
            continue
        points = spec["values"][value]["points"]
        entry = {"value": value, "points": points, "derived_from": origin}
        quote = (researched or {}).get(key, {}).get("quote") if isinstance(researched, dict) else None
        if quote:
            entry["evidence_quote"] = quote
        dimensions[key] = entry
        score += points
        evidenced_weight += spec["weight_max"]
        evidenced += 1

    total_weight = sum(spec["weight_max"] for spec in HOUSING_DIMENSIONS.values())
    if evidenced < 3 or not evidenced_weight:
        level = "unknown"
        scaled = None
        confidence = "unknown"
        band_from_score = None
    else:
        scaled = round(score * total_weight / evidenced_weight)
        level = next(
            (band["code"] for band in HOUSING_LEVELS if band["score_range"][0] <= scaled <= band["score_range"][1]),
            "very_high",
        )
        # The written criteria reserve "very high" for a named structural
        # failure, not for a high arithmetic score.  Rescaling a partial
        # profile must not manufacture one, so the top band needs the specific
        # signal that defines it.
        structural = {
            dimensions["supply_pressure"].get("value") == "cannot_house_most_internationals_stated",
            dimensions["arrival_risk"].get("value") == "officially_advised_not_to_travel_without_contract",
        }
        band_from_score = level
        if level == "very_high" and True not in structural:
            level = "high"
        confidence = "high" if evidenced == 5 else "medium"

    living["housing_difficulty"] = level
    living["housing_search_difficulty"] = level
    living["housing_difficulty_profile"] = {
        "standard": f"housing_difficulty@{STANDARDS_VERSION}",
        "level": level,
        "raw_score": score if evidenced else None,
        "scaled_score": scaled,
        "score_max": total_weight,
        "evidenced_dimensions": evidenced,
        "dimensions_required_for_publication": 3,
        "dimensions": dimensions,
        "confidence": confidence,
        "band_from_score": band_from_score,
        "capped_from_very_high": band_from_score == "very_high" and level != band_from_score,
        "legacy_value": legacy if isinstance(legacy, str) and legacy else None,
        "evaluated_at": TODAY,
    }
    return living["housing_difficulty_profile"]


# --------------------------------------------------------------------------
# 2. cost of living
# --------------------------------------------------------------------------

MONTHS_BY_PERIOD = {"month": 1, "monthly": 1, "academic_year": 9, "year": 12, "annual": 12, "12_month_contract": 12, "semester": 6}

COMPONENT_PATTERNS = [
    (re.compile(r"hous|rent|room|accommodation|dorm|residence|apartment"), "rent"),
    (re.compile(r"food|meal|board|groceries"), "food"),
    (re.compile(r"transport|travel|commut|bus|metro"), "transport"),
    (re.compile(r"utilit|internet|electric|heating"), "utilities"),
    (re.compile(r"book|supplies|course material|study material"), "study_materials"),
    (re.compile(r"insurance|health"), "health_insurance"),
    (re.compile(r"personal|miscellaneous|leisure|other expense"), "personal"),
    (re.compile(r"semester (fee|contribution)|student union|studentenwerk"), "semester_contribution"),
]


def classify_component(label: str) -> str | None:
    for pattern, component in COMPONENT_PATTERNS:
        if pattern.search(label):
            return component
    return None


def item_currency_amount(item: dict[str, Any]) -> tuple[float | None, str | None]:
    for currency in CURRENCY_SUFFIXES:
        exact = number(item.get(f"amount_{currency}"))
        if exact is not None:
            return exact, currency.upper()
        low = number(item.get(f"amount_{currency}_min"))
        high = number(item.get(f"amount_{currency}_max"))
        if low is not None or high is not None:
            values = [v for v in (low, high) if v is not None]
            return sum(values) / len(values), currency.upper()
    amount = number(item.get("amount"))
    currency = item.get("currency")
    if amount is not None and isinstance(currency, str):
        return amount, currency.upper()
    return None, None


def build_cost_of_living_from_evidence(living: dict[str, Any], evidence: dict[str, Any]) -> dict[str, Any]:
    """Use a researched budget verbatim, with its basis and period attached."""
    currency = str(evidence.get("currency") or "EUR").upper()
    months = int(number(evidence.get("months_covered")) or 12)
    raw_components = evidence.get("components") if isinstance(evidence.get("components"), dict) else {}
    components = {
        name: {"monthly_amount": number(amount), "currency": currency}
        for name, amount in raw_components.items()
        if number(amount) is not None
    }
    monthly_total = number(evidence.get("monthly_total"))
    if monthly_total is None and components:
        monthly_total = round(sum(entry["monthly_amount"] for entry in components.values()), 2)

    mandatory = {c["key"] for c in STANDARDS["cost_model"]["components"] if c["mandatory_in_total"]}
    covered = set(components) & mandatory
    profile = {
        "standard": f"cost_model@{STANDARDS_VERSION}",
        "cost_basis": evidence.get("cost_basis") or "unknown",
        # A published lump-sum budget is honest but not itemised, so it is
        # labelled differently from a budget whose components were checked.
        "status": (
            "unknown" if monthly_total is None
            else "total_only" if not components
            else "complete" if covered == mandatory
            else "partial"
        ),
        "currency": currency,
        "months_covered": months,
        "components_included": sorted(components),
        "mandatory_components_missing": sorted(mandatory - covered) if components else [],
        "components": components,
        "monthly_total": monthly_total,
        "annual_total": round(monthly_total * months, 2) if monthly_total is not None else None,
        "monthly_total_eur_equivalent": to_eur(monthly_total, currency) if currency != "EUR" else None,
        "excludes": evidence.get("excludes") or ["tuition", "mandatory_university_fees", "one_off_visa_and_travel_costs"],
        "confidence": evidence.get("confidence") or "high",
        "source_url": evidence.get("source_url"),
        "note": evidence.get("note"),
        "evaluated_at": TODAY,
    }
    living["cost_of_living_profile"] = profile
    return profile


def build_cost_of_living(record: dict[str, Any]) -> dict[str, Any]:
    living = record.setdefault("living_profile", {})
    evidence = living.get("cost_of_living_evidence")
    if isinstance(evidence, dict) and evidence.get("source_url"):
        return build_cost_of_living_from_evidence(living, evidence)

    items = non_empty_list(living.get("official_living_cost_items"))
    fields_ok = "housing" in verified_fields(record)

    components: dict[str, dict[str, Any]] = {}
    currencies: set[str] = set()
    months_seen: set[int] = set()

    for item in items:
        if not isinstance(item, dict):
            continue
        label = text_of(item.get("item") or item.get("label") or item.get("name"))
        component = classify_component(label)
        amount, currency = item_currency_amount(item)
        if component is None or amount is None or currency is None:
            continue
        months = MONTHS_BY_PERIOD.get(str(item.get("period") or "").strip().lower())
        if not months:
            continue
        months_seen.add(months)
        currencies.add(currency)
        entry = components.setdefault(component, {"monthly_amount": 0.0, "currency": currency, "sources": []})
        if entry["currency"] != currency:
            continue
        entry["monthly_amount"] += amount / months
        entry["sources"].append({"label": item.get("item"), "published_amount": amount, "currency": currency, "period": item.get("period")})

    if not components or len(currencies) != 1 or not fields_ok:
        profile = {
            "standard": f"cost_model@{STANDARDS_VERSION}",
            "cost_basis": "unknown",
            "status": "unknown",
            "reason": (
                "no_official_living_cost_items" if not components
                else "housing_evidence_not_checked" if not fields_ok
                else "mixed_currencies_in_official_items"
            ),
            "components": {},
            "monthly_total": None,
            "evaluated_at": TODAY,
        }
        living["cost_of_living_profile"] = profile
        return profile

    currency = currencies.pop()
    months_covered = max(months_seen) if months_seen else 12
    mandatory = {c["key"] for c in STANDARDS["cost_model"]["components"] if c["mandatory_in_total"]}
    covered = set(components) & mandatory
    monthly_total = round(sum(entry["monthly_amount"] for entry in components.values()), 2)

    profile = {
        "standard": f"cost_model@{STANDARDS_VERSION}",
        "cost_basis": "official_university_cost_of_attendance" if "rent" in components and "food" in components else "official_university_living_budget",
        "status": "complete" if covered == mandatory else "partial",
        "currency": currency,
        "months_covered": months_covered,
        "components_included": sorted(components),
        "mandatory_components_missing": sorted(mandatory - covered),
        "components": {
            name: {
                "monthly_amount": round(entry["monthly_amount"], 2),
                "currency": entry["currency"],
                "published_items": entry["sources"],
            }
            for name, entry in sorted(components.items())
        },
        "monthly_total": monthly_total,
        "annual_total": round(monthly_total * months_covered, 2),
        "monthly_total_eur_equivalent": to_eur(monthly_total, currency),
        "excludes": ["tuition", "mandatory_university_fees", "one_off_visa_and_travel_costs"],
        "confidence": "high" if covered == mandatory else "medium",
        "evaluated_at": TODAY,
    }
    living["cost_of_living_profile"] = profile
    return profile


def build_normalized_cost(record: dict[str, Any]) -> dict[str, Any]:
    """Publish one annual total whose inclusion list travels with the number."""
    cost = record.setdefault("cost_profile", {})
    living = record.get("living_profile") or {}
    col = living.get("cost_of_living_profile") or {}
    tuition_verified = "tuition" in verified_fields(record)

    tuition = None
    tuition_currency = None
    if tuition_verified:
        for currency in CURRENCY_SUFFIXES:
            value = number(cost.get(f"tuition_{currency}_per_year"))
            if value is not None:
                tuition, tuition_currency = value, currency.upper()
                break
        if tuition is None:
            value = number(cost.get("tuition_eur_per_year_estimated"))
            if value is not None:
                tuition, tuition_currency = value, "EUR"

    included: list[str] = []
    missing: list[str] = []
    total = 0.0
    currency = tuition_currency or col.get("currency")

    if tuition is not None and tuition_currency == currency:
        total += tuition
        included.append("tuition")
    else:
        missing.append("tuition")

    fees = None
    if tuition_verified and currency:
        fees = number(cost.get(f"mandatory_fees_{currency.lower()}_per_year"))
    if fees is not None:
        total += fees
        included.append("mandatory_fees")

    insurance = number(cost.get("health_insurance_premium_usd")) if currency == "USD" else None
    if insurance is not None:
        total += insurance
        included.append("health_insurance")

    living_annual = number(col.get("annual_total")) if col.get("currency") == currency else None
    if living_annual is not None:
        total += living_annual
        included.append("living_costs")
    else:
        missing.append("living_costs")

    publishable = not missing and currency is not None
    normalized = {
        "standard": f"cost_model@{STANDARDS_VERSION}",
        "currency": currency,
        "annual_total": round(total, 2) if publishable else None,
        "annual_total_eur_equivalent": to_eur(round(total, 2), currency) if publishable and currency and currency != "EUR" else None,
        "includes": included,
        "missing_mandatory_components": missing,
        "months_of_living_cost": col.get("months_covered"),
        "status": "complete" if publishable else "incomplete",
        "note": {
            "en": "A total is published only when tuition and a component-checked living budget are both verified in the same currency; otherwise the parts are shown separately so no invented sum reaches a student.",
            "tr": "Toplam yalnızca öğrenim ücreti ve bileşenleri kontrol edilmiş yaşam bütçesi aynı para biriminde doğrulandığında yayımlanır; aksi hâlde parçalar ayrı gösterilir ve öğrenciye uydurma bir toplam ulaşmaz.",
        },
        "evaluated_at": TODAY,
    }
    cost["normalized_cost"] = normalized
    return normalized


# --------------------------------------------------------------------------
# 3. academic match
# --------------------------------------------------------------------------

MATCH_SPEC = STANDARDS["academic_match"]
MATCH_WEIGHTS = {d["key"]: d["weight"] for d in MATCH_SPEC["evidence_dimensions"]}
MATCH_LEVELS = MATCH_SPEC["dimension_levels"]
MATCH_TIERS = [t for t in MATCH_SPEC["tiers"] if t["min_score"] is not None]


def count_evidence(value: Any) -> int:
    return len(non_empty_list(value))


def build_academic_match(record: dict[str, Any]) -> dict[str, Any]:
    verified = verified_fields(record)
    curriculum = record.get("curriculum_profile") or {}
    research = record.get("research_profile") or {}
    industry = record.get("industry_ecosystem_profile") or {}
    category = record.get("category_profile") or {}

    def level(count: int, verified_field: str, strong_at: int = 3, moderate_at: int = 1) -> tuple[str, str]:
        if verified_field not in verified:
            return "unknown", f"{verified_field}_evidence_not_checked"
        if count >= strong_at:
            return "strong", f"{count}_named_items"
        if count >= moderate_at:
            return "moderate", f"{count}_named_items"
        return "none", "no_named_items"

    specialisations = count_evidence(curriculum.get("specializations")) + count_evidence(curriculum.get("tracks"))
    units = count_evidence(research.get("research_units")) or (count_evidence(research.get("labs")) + count_evidence(research.get("key_institutes")))
    faculty = count_evidence(research.get("notable_professors"))
    facilities = count_evidence(research.get("research_centers")) + sum(
        count_evidence(unit.get("facilities")) for unit in non_empty_list(research.get("research_units")) if isinstance(unit, dict)
    )
    partners = count_evidence(industry.get("verified_partnerships"))

    dimensions = {
        "curriculum_evidence": level(specialisations, "curriculum"),
        "research_group_evidence": level(units, "research", strong_at=3),
        "faculty_evidence": level(faculty, "research", strong_at=3),
        "facility_evidence": level(facilities, "research", strong_at=2),
        "industry_outlet_evidence": level(partners, "industry", strong_at=2),
    }

    # A researcher who has read the curriculum or the lab pages can state a
    # level directly; the count-based fallback above only approximates it.
    researched = record.get("academic_match_evidence")
    if isinstance(researched, dict):
        for key, entry in researched.items():
            if key in dimensions and isinstance(entry, dict) and entry.get("level") in MATCH_LEVELS:
                dimensions[key] = (entry["level"], entry.get("basis") or "researched_official_source")

    scored_weight = 0
    scored_value = 0.0
    detail: dict[str, Any] = {}
    for key, (value, reason) in dimensions.items():
        weight = MATCH_WEIGHTS[key]
        detail[key] = {"level": value, "basis": reason, "weight": weight}
        evidence = (researched or {}).get(key) if isinstance(researched, dict) else None
        if isinstance(evidence, dict) and evidence.get("source_url"):
            detail[key]["source_url"] = evidence["source_url"]
        multiplier = MATCH_LEVELS[value]
        if multiplier is None:
            continue
        scored_weight += weight
        scored_value += weight * multiplier

    evidenced = sum(1 for item in detail.values() if item["level"] != "unknown")
    if evidenced < 3 or not scored_weight:
        tier, score, confidence = "unknown", None, "unknown"
    else:
        score = round(scored_value / scored_weight * 100)
        tier = next((t["code"] for t in MATCH_TIERS if score >= t["min_score"]), "weak_match")
        confidence = "high" if evidenced == 5 else "medium"

    profile = {
        "standard": f"academic_match@{STANDARDS_VERSION}",
        "tier": tier,
        "score": score,
        "score_basis_weight": scored_weight,
        "evidenced_dimensions": evidenced,
        "dimensions_required_for_publication": 3,
        "dimensions": detail,
        "matched_tags": [tag for tag in non_empty_list(category.get("normalized_tags")) if isinstance(tag, str)],
        "confidence": confidence,
        "legacy_relevance_status": record.get("relevance_status"),
        "evaluated_at": TODAY,
    }
    record["academic_match_profile"] = profile
    return profile


# --------------------------------------------------------------------------
# 4. primary deadline
# --------------------------------------------------------------------------

# Many records store the date with its published qualifier attached, for
# example "2026-01-15 (23:59 CET; non-EU/EFTA with international BSc; closed)"
# or a full timestamp.  The leading calendar date is the machine-readable part.
ISO_DATE = re.compile(r"^(\d{4}-\d{2}-\d{2})(?:[T ]|$)")


def iso_date(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    match = ISO_DATE.match(value.strip())
    if not match:
        return None
    try:
        date.fromisoformat(match.group(1))
    except ValueError:
        return None
    return match.group(1)

DEADLINE_FIELDS = [
    ("deadline_non_eu", "non_eu"),
    ("non_eu_deadline", "non_eu"),
    ("international_deadline", "international"),
    ("application_deadline", "all_applicants"),
    ("final_application_deadline", "all_applicants"),
    ("deadline_eu", "eu_eea"),
]


def build_primary_deadline(record: dict[str, Any]) -> dict[str, Any]:
    timeline = record.setdefault("application_timeline_profile", {})
    verified = "deadline" in verified_fields(record)
    source = (record.get("source_profile") or {}).get("official_admission_page") or record.get("program_url")

    # Collect every published ISO date, then prefer the next one a student can
    # still act on.  A record often carries both last cycle's closed date and
    # this cycle's open one, and showing the closed date first is what makes a
    # live programme look shut.
    candidates: list[tuple[str, str, str]] = []
    for field, audience in DEADLINE_FIELDS:
        parsed = iso_date(timeline.get(field))
        if parsed:
            candidates.append((parsed, audience, f"application_timeline_profile.{field}"))
    for event in non_empty_list(timeline.get("deadline_events")):
        if not isinstance(event, dict):
            continue
        parsed = iso_date(event.get("date") or event.get("deadline"))
        if parsed:
            candidates.append((parsed, "all_applicants", "application_timeline_profile.deadline_events[]"))

    today = date.today()
    upcoming = sorted(c for c in candidates if date.fromisoformat(c[0]) >= today)
    if upcoming:
        chosen_date, applies_to, origin = upcoming[0]
    elif candidates:
        chosen_date, applies_to, origin = max(candidates)
    else:
        chosen_date, applies_to, origin = None, None, None

    if chosen_date is None:
        primary = {
            "standard": f"application_countdown@{STANDARDS_VERSION}",
            "date": None,
            "status": "not_published",
            "confidence": "unknown",
            "reason": "no_iso_dated_deadline_in_record",
            "evaluated_at": TODAY,
        }
    else:
        deadline_date = date.fromisoformat(chosen_date)
        days_left = (deadline_date - today).days
        if days_left < 0:
            status = "closed"
        elif days_left <= 30:
            status = "closing_soon"
        else:
            status = "open"
        recurring = bool(timeline.get("recurring_annual_deadline"))
        next_expected = None
        if status == "closed" and recurring:
            year = today.year
            while True:
                try:
                    candidate = deadline_date.replace(year=year)
                except ValueError:  # 29 February in a non-leap year
                    candidate = deadline_date.replace(year=year, day=28)
                if candidate >= today:
                    next_expected = candidate.isoformat()
                    break
                year += 1
        primary = {
            "standard": f"application_countdown@{STANDARDS_VERSION}",
            "date": chosen_date,
            "next_expected_date": next_expected,
            "time": timeline.get("deadline_time"),
            "timezone": timeline.get("deadline_timezone"),
            "applies_to": applies_to,
            "cycle_label": timeline.get("entry_term"),
            "is_recurring_annual": bool(timeline.get("recurring_annual_deadline")),
            "status": status,
            "days_remaining_at_evaluation": days_left,
            "derived_from": origin,
            "confidence": "high" if verified else "low",
            "source_url": source,
            "evaluated_at": TODAY,
        }
    timeline["primary_deadline"] = primary
    return primary


# --------------------------------------------------------------------------
# runner
# --------------------------------------------------------------------------

def standardize(record: dict[str, Any]) -> dict[str, Any]:
    housing = build_housing_difficulty(record)
    build_cost_of_living(record)
    cost = build_normalized_cost(record)
    match = build_academic_match(record)
    deadline = build_primary_deadline(record)
    return {
        "housing_level": housing["level"],
        "cost_status": cost["status"],
        "match_tier": match["tier"],
        "deadline_status": deadline["status"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="rewrite the JSON files in place")
    args = parser.parse_args()

    tally = {"housing_level": Counter(), "cost_status": Counter(), "match_tier": Counter(), "deadline_status": Counter()}
    total = 0

    for path in sorted(DATA_DIR.glob("*.json")):
        if path.name in SKIP_FILES:
            continue
        document, records = load_records(path)
        if not records:
            continue
        for record in records:
            for key, value in standardize(record).items():
                tally[key][value] += 1
            total += 1
        if args.write:
            path.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"records processed: {total}")
    for key, counter in tally.items():
        print(f"\n{key}")
        for value, count in counter.most_common():
            print(f"  {count:4}  {value}")
    if not args.write:
        print("\nreport only - pass --write to persist")


if __name__ == "__main__":
    main()
