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


UNUSABLE_ACCESS = {"broken", "not_found", "unknown"}


def sourced_fields(record: dict[str, Any]) -> set[str]:
    """Fields covered by a source that was checked and found reachable.

    ``verified_fields`` records what a researcher concluded; this records what
    the source log can still show for it.  A derivation needs both, so that a
    number left behind by a source that has since gone dead is never promoted
    into the published shape.
    """
    covered: set[str] = set()
    for source in (record.get("source_profile") or {}).get("source_log") or []:
        if not isinstance(source, dict):
            continue
        if str(source.get("access_status") or "unknown").lower() in UNUSABLE_ACCESS:
            continue
        for field in source.get("relevant_fields") or []:
            covered.add(str(field).lower())
    return covered


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

MONTHS_BY_PERIOD = {"month": 1, "monthly": 1, "week": 12 / 52, "weekly": 12 / 52, "52_week_academic_year": 12, "academic_year": 9, "year": 12, "annual": 12, "12_month_contract": 12, "semester": 6}

COMPONENT_PATTERNS = [
    # Order matters.  A line that already covers several components has to be
    # recognised before the narrower patterns claim it: "food and housing
    # allowance" would otherwise be filed as rent alone, hiding the food inside
    # it and then reporting food as unpublished, and a whole-budget line such
    # as Michigan's "living allowance for 12 months" would match nothing at all
    # and be dropped, leaving books and insurance as the entire living cost.
    (re.compile(r"living (allowance|expenses?|costs?)|cost of living"), "living_allowance"),
    (re.compile(r"(food|meals?).{0,5}(and|&|/).{0,5}(hous|accommodation|rent|room)|"
                r"(hous|accommodation|rent|room).{0,12}(and|&|/).{0,5}(food|meals?|board)|"
                r"room and board"), "rent_and_food"),
    (re.compile(r"hous|rent|room|accommodation|dorm|residence|apartment"), "rent"),
    (re.compile(r"food|meal|board|groceries"), "food"),
    (re.compile(r"transport|travel|commut|bus|metro"), "transport"),
    (re.compile(r"utilit|internet|electric|heating|wifi|broadband|phone|mobile"), "utilities"),
    (re.compile(r"book|supplies|course material|study material"), "study_materials"),
    (re.compile(r"insurance|health"), "health_insurance"),
    # Universities itemise discretionary spending under many names.  Every one
    # of these that goes unmatched is silently dropped from the total, which is
    # how Sheffield's published budget lost GBP 165 of its GBP 378.
    (re.compile(r"personal|miscellaneous|leisure|other expense|going out|eating out|"
                r"takeaway|clothes|shopping|social|wellbeing|trips|entertainment|"
                r"laundry|sport|gym|hobb"), "personal"),
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
    # A source often folds one component into another - utilities inside the
    # rent line, for instance.  Without this the component would be reported as
    # unpublished, which tells a reader to budget for it twice.
    absorbed = evidence.get("components_absorbed") if isinstance(evidence.get("components_absorbed"), dict) else {}
    absorbed = {key: host for key, host in absorbed.items() if host in components}
    covered = (set(components) | set(absorbed)) & mandatory
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
        "components_absorbed": absorbed,
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


def derive_living_total(record: dict[str, Any], living: dict[str, Any]) -> dict[str, Any] | None:
    """Publish a checked monthly range that was never itemised.

    Most records hold a monthly living figure that a researcher read from an
    official page and logged a source for, but stored as a bare min/max with no
    component list and no period.  The itemised path cannot see it, so the cost
    card showed nothing at all — the least useful of the three honest answers.
    This publishes it as an explicitly total-only figure: the midpoint for
    comparison, the range beside it, and a basis that says the components were
    never itemised.
    """
    if not (verified_fields(record) & {"living", "housing"}):
        return None
    if not (sourced_fields(record) & {"living", "housing", "cost", "costs", "rent"}):
        return None

    # The same fact was written under several key spellings as the database
    # grew.  All of them are read, monthly first, so a record is not treated as
    # having no living cost because of the shape of a field name.
    annual_months = number(living.get("living_cost_period_months")) or 12
    # UCL's annual living budget sits in the cost profile rather than the
    # living profile, so both are searched as one namespace.  The profile is
    # still written back to ``living`` alone.
    fields = {**(record.get("cost_profile") or {}), **living}
    for currency in CURRENCY_SUFFIXES:
        shapes = (
            (f"monthly_living_cost_{currency}_min", f"monthly_living_cost_{currency}_max",
             f"monthly_living_cost_{currency}_estimated", 1.0, "verified_range_midpoint"),
            (f"monthly_living_cost_{currency}_per_month_min", f"monthly_living_cost_{currency}_per_month_max",
             f"monthly_living_cost_{currency}_per_month_estimated", 1.0, "verified_range_midpoint"),
            (f"living_cost_{currency}_per_year_min", f"living_cost_{currency}_per_year_max",
             f"living_cost_{currency}_per_year", 1.0 / annual_months, "published_annual_living_budget"),
            # A weekly rate covers a 52-week year, so twelve months of it is
            # the annual figure divided by twelve, not the weekly rate times
            # four, which would lose most of a month every year.
            (f"living_cost_{currency}_per_week_min", f"living_cost_{currency}_per_week_max",
             f"living_cost_{currency}_per_week", 52.0 / 12.0, "published_annual_living_budget"),
        )
        low = high = estimated = None
        factor = 1.0
        rule = "verified_range_midpoint"
        for min_key, max_key, single_key, shape_factor, shape_rule in shapes:
            low = number(fields.get(min_key))
            high = number(fields.get(max_key))
            estimated = number(fields.get(single_key))
            if currency == "eur" and estimated is None and shape_factor == 1.0:
                estimated = number(fields.get("living_cost_eur_per_month"))
            if low is not None or high is not None or estimated is not None:
                factor, rule = shape_factor, shape_rule
                break

        values = [v for v in (low, high) if v is not None]
        if values:
            monthly_total = round(sum(values) / len(values) * factor, 2)
        elif estimated is not None:
            monthly_total = round(estimated * factor, 2)
        else:
            continue
        if monthly_total <= 0:
            continue

        published_range = {"min": low, "max": high} if values else None
        # Surrey's GBP 1,171 is the Home Office maintenance requirement, and
        # its own note says so.  Publishing that as a spending estimate would
        # tell a reader the legal minimum is what living there costs, so the
        # record's prose is read to pick the right basis.
        prose = " ".join(text_of(fields.get(key)) for key in
                         ("monthly_living_cost_basis", "housing_notes", "living_cost_notes", "verification_notes"))
        is_visa_floor = bool(re.search(r"maintenance requirement|visa maintenance|ukvi|student-visa maintenance", prose))
        profile = {
            "standard": f"cost_model@{STANDARDS_VERSION}",
            "cost_basis": "official_visa_financial_requirement" if is_visa_floor
            else "official_source_range_basis_not_itemised",
            "status": "total_only",
            "currency": currency.upper(),
            # The stored figure is a monthly rate, so twelve months is the
            # period it was written for.  A nine-month academic year is only
            # ever assumed when the source itself says so, which is what the
            # itemised path reads from each item's period.
            "months_covered": 12,
            "components_included": [],
            "mandatory_components_missing": [],
            "components": {},
            "monthly_total": monthly_total,
            "published_range": published_range,
            "annual_total": round(monthly_total * 12, 2),
            "monthly_total_eur_equivalent": to_eur(monthly_total, currency.upper()) if currency != "eur" else None,
            "excludes": ["tuition", "mandatory_university_fees", "one_off_visa_and_travel_costs"],
            "confidence": "medium",
            "derivation": {
                "rule": rule,
                "derived_from": {k: v for k, v in {
                    f"monthly_living_cost_{currency}_min": low,
                    f"monthly_living_cost_{currency}_max": high,
                    f"monthly_living_cost_{currency}_estimated": estimated,
                }.items() if v is not None},
                "derived_at": TODAY,
            },
            "source_url": fields.get("living_cost_source_url"),
            "note": fields.get("monthly_living_cost_basis") or fields.get("living_cost_notes"),
            "evaluated_at": TODAY,
        }
        living["cost_of_living_profile"] = profile
        return profile
    return None


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

    # A combined line is stored under the component a reader looks for first,
    # and the components it swallowed are recorded so they are reported as
    # included rather than as missing.
    combined_absorbed: dict[str, str] = {}
    if "rent_and_food" in components:
        merged = components.pop("rent_and_food")
        host = components.setdefault("rent", {"monthly_amount": 0.0, "currency": merged["currency"], "sources": []})
        host["monthly_amount"] += merged["monthly_amount"]
        host["sources"].extend(merged["sources"])
        combined_absorbed["food"] = "rent"
    if "living_allowance" in components:
        for swallowed in ("rent", "utilities", "food", "transport"):
            if swallowed not in components:
                combined_absorbed[swallowed] = "living_allowance"

    if not components or len(currencies) != 1 or not fields_ok:
        derived = derive_living_total(record, living)
        if derived:
            return derived
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
    covered = (set(components) | set(combined_absorbed)) & mandatory
    monthly_total = round(sum(entry["monthly_amount"] for entry in components.values()), 2)

    profile = {
        "standard": f"cost_model@{STANDARDS_VERSION}",
        "cost_basis": "official_university_cost_of_attendance" if "rent" in components and "food" in components else "official_university_living_budget",
        "status": "complete" if covered == mandatory else "partial",
        "currency": currency,
        "months_covered": months_covered,
        "components_included": sorted(components),
        "components_absorbed": combined_absorbed,
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


# Keys that name tuition and can be turned into an annual figure.  A mandatory
# fee, an enrolment fee, a regional tax or an application fee is deliberately
# absent: promoting one of those to tuition would understate a cost by an order
# of magnitude, which is the single most damaging error this file could make.
TUITION_DERIVATIONS = (
    ("tuition_{c}_per_year_at_three_quarters", "published_annual_figure", 1.0),
    ("tuition_and_program_fees_{c}_nonresident", "published_annual_figure", 1.0),
    ("tuition_{c}_first_year_example", "published_annual_figure", 1.0),
    ("tuition_{c}_per_semester", "two_semesters_per_academic_year", 2.0),
    ("tuition_{c}_per_term", "two_semesters_per_academic_year", 2.0),
    # Legacy key name.  Where these are still set they mirror the published
    # annual rate exactly rather than holding an estimate, and the EU-only and
    # zero guards above still apply to them.
    ("tuition_{c}_per_year_estimated", "published_annual_figure", 1.0),
)

TUITION_PROGRAMME_KEYS = ("tuition_{c}_full_programme", "tuition_{c}_total")

# A basis that names EU/EEA/Swiss citizens is describing a rate the reader of
# this database cannot use.  Several records store that rate in the same field
# a non-EU rate would occupy and explain the mismatch only in prose, so the
# basis string is read before the number is promoted to a headline figure.
EU_ONLY_BASIS = re.compile(r"eu[_ ]?eea|eu/eea|for_eu|eu_citizens|eea_swiss", re.IGNORECASE)

# German and Nordic public universities charge no tuition at all.  Their
# records store that as a 0/0 band, which the zero guard above would otherwise
# reject as an unfilled field, leaving the most affordable programmes in the
# database showing "tuition unknown".  A zero is published only when the basis
# says in words that no tuition is charged.
NO_TUITION_BASIS = re.compile(
    r"no_general_tuition|no_regular_tuition|no_tuition|tuition_free|abolished|"
    r"state_funded|fully_exempt",
    re.IGNORECASE,
)


def _positive(value: Any) -> float | None:
    """A tuition of zero is almost always an unfilled field, not a free degree.

    Publishing it would place the record at the top of every cost comparison.
    Where a programme genuinely charges nothing, the record says so through the
    fee-status fields rather than through a numeric zero.
    """
    amount = number(value)
    return amount if amount is not None and amount > 0 else None


def _tuition_band(cost: dict[str, Any], currency: str, income_based: bool) -> tuple[tuple[float, str, dict] | None, bool]:
    """Return the band-derived figure, and whether a min-only band was refused."""
    low = _positive(cost.get(f"tuition_{currency}_per_year_min"))
    high = _positive(cost.get(f"tuition_{currency}_per_year_max"))
    if high is not None:
        return (high, "non_eu_planning_maximum", {f"tuition_{currency}_per_year_min": low,
                                                  f"tuition_{currency}_per_year_max": high}), False
    if low is None:
        return None, False
    if income_based:
        # An Italian ISEE band published without its ceiling: the lowest
        # bracket is what a local family on a low income pays, and printing it
        # as "the tuition" would be the most flattering number in the record.
        return None, True
    return (low, "non_eu_planning_maximum", {f"tuition_{currency}_per_year_min": low}), False


def derive_mandatory_semester_fees(cost: dict[str, Any], currency: str) -> None:
    """Turn a per-semester student contribution into the annual cost it is.

    Where tuition is zero the semester contribution is the whole of what a
    student is billed, so leaving it out of the annual total would publish a
    cost of exactly nothing for the cheapest programmes in the database.
    """
    if number(cost.get(f"mandatory_fees_{currency}_per_year")) is not None:
        return

    # Some records publish the annual mandatory charge directly as a band.
    annual_band = _positive(cost.get(f"mandatory_fees_{currency}_per_year_max")) \
        or _positive(cost.get(f"mandatory_fees_{currency}_per_year_min"))
    if annual_band is not None:
        cost[f"mandatory_fees_{currency}_per_year"] = annual_band
        cost["mandatory_fees_derivation"] = {
            "standard": f"cost_model@{STANDARDS_VERSION}",
            "field": f"mandatory_fees_{currency}_per_year",
            "rule": "non_eu_planning_maximum",
            "derived_from": {f"mandatory_fees_{currency}_per_year_max": annual_band},
            "derived_at": TODAY,
        }
        return

    per_semester = _positive(cost.get(f"student_contribution_{currency}")) \
        or _positive(cost.get("student_contribution_eur") if currency == "eur" else None) \
        or _positive(cost.get(f"student_contribution_calculated_{currency}")) \
        or _positive(cost.get("student_contribution_calculated_eur") if currency == "eur" else None)
    if per_semester is None:
        return
    cost[f"mandatory_fees_{currency}_per_year"] = round(per_semester * 2, 2)
    cost["mandatory_fees_derivation"] = {
        "standard": f"cost_model@{STANDARDS_VERSION}",
        "field": f"mandatory_fees_{currency}_per_year",
        "rule": "two_semesters_per_academic_year",
        "derived_from": {"student_contribution_per_semester": per_semester},
        "derived_at": TODAY,
    }


def derive_annual_tuition(record: dict[str, Any]) -> dict[str, Any] | None:
    """Fill the canonical annual tuition field from another verified figure.

    Records were written by many hands, so the same fact arrived as a
    per-semester rate, a whole-programme fee or a bespoke example key.  The
    figure was checked, but nothing downstream could read it, so the annual
    total and the cost card both behaved as though tuition were unknown.  This
    moves such a figure into ``tuition_<currency>_per_year`` and records how.
    """
    cost = record.setdefault("cost_profile", {})
    if "tuition" not in verified_fields(record):
        return None
    if not sourced_fields(record) & {"tuition", "fee", "fees", "cost", "costs"}:
        return None

    income_based = bool(cost.get("isee_or_income_based"))
    duration = number(record.get("duration_years"))

    # Separators vary between records ("non_eu", "non-EU", "non EU"), so they
    # are flattened before the basis is matched.
    basis = str(cost.get("tuition_basis") or "")
    flat_basis = re.sub(r"[^a-z]+", "_", basis.lower())
    if EU_ONLY_BASIS.search(basis) and "non_eu" not in flat_basis:
        cost["tuition_derivation"] = {
            "standard": f"cost_model@{STANDARDS_VERSION}",
            "rule": "not_derivable",
            "reason": "published_rate_is_eu_eea_only",
            "derived_from": {"tuition_basis": basis},
            "derived_at": TODAY,
        }
        return None

    for currency in CURRENCY_SUFFIXES:
        if _positive(cost.get(f"tuition_{currency}_per_year")) is not None:
            return None  # already published in the canonical field

    # A stated no-tuition policy publishes a zero only when the record also
    # holds no positive tuition figure anywhere.  A basis phrase alone is not
    # enough: a record can say "state funded" and still charge non-EU students.
    any_positive_tuition = any(
        _positive(value) is not None
        for key, value in cost.items()
        if isinstance(key, str) and key.startswith("tuition_")
    )
    if NO_TUITION_BASIS.search(flat_basis) and not any_positive_tuition:
        currency = str(cost.get("currency") or "EUR").lower()
        if currency not in CURRENCY_SUFFIXES:
            currency = "eur"
        cost[f"tuition_{currency}_per_year"] = 0
        derivation = {
            "standard": f"cost_model@{STANDARDS_VERSION}",
            "field": f"tuition_{currency}_per_year",
            "rule": "no_tuition_charged",
            "derived_from": {"tuition_basis": basis},
            "currency": currency.upper(),
            "includes_mandatory_fees": False,
            "derived_at": TODAY,
        }
        cost["tuition_derivation"] = derivation
        derive_mandatory_semester_fees(cost, currency)
        return derivation

    refused_income_band = False
    for currency in CURRENCY_SUFFIXES:
        candidates: list[tuple[float, str, dict]] = []

        band, refused = _tuition_band(cost, currency, income_based)
        refused_income_band = refused_income_band or refused
        if band:
            candidates.append(band)

        for template, rule, factor in TUITION_DERIVATIONS:
            key = template.format(c=currency)
            value = _positive(cost.get(key))
            if value is not None:
                candidates.append((value * factor, rule, {key: value}))

        # A record that names its currency once can carry the figure in a key
        # with no currency in it at all.
        original_currency = str(cost.get("tuition_original_currency") or cost.get("currency") or "").lower()
        if original_currency == currency:
            value = _positive(cost.get("tuition_original_amount"))
            if value is not None:
                candidates.append((value, "published_annual_figure",
                                   {"tuition_original_amount": value, "tuition_original_currency": currency.upper()}))

        # Some UK records store the fee as an object carrying its own basis.
        full = cost.get("tuition_non_eu_full_program")
        if isinstance(full, dict) and str(full.get("currency") or "").lower() == currency:
            value = _positive(full.get("amount"))
            if value is not None and str(full.get("basis")) == "one_year_programme":
                candidates.append((value, "published_annual_figure",
                                   {"tuition_non_eu_full_program": full}))
            elif value is not None and duration and duration > 0:
                candidates.append((value / duration, "programme_fee_divided_by_duration",
                                   {"tuition_non_eu_full_program": full, "duration_years": duration}))

        if duration and duration > 0:
            for template in TUITION_PROGRAMME_KEYS:
                key = template.format(c=currency)
                value = _positive(cost.get(key))
                if value is not None:
                    candidates.append((value / duration, "programme_fee_divided_by_duration",
                                       {key: value, "duration_years": duration}))

        if not candidates:
            continue

        amount, rule, origin = candidates[0]
        cost[f"tuition_{currency}_per_year"] = round(amount, 2)
        derivation = {
            "standard": f"cost_model@{STANDARDS_VERSION}",
            "field": f"tuition_{currency}_per_year",
            "rule": rule,
            "derived_from": origin,
            "currency": currency.upper(),
            "includes_mandatory_fees": "tuition_and_program_fees" in next(iter(origin)),
            "derived_at": TODAY,
        }
        cost["tuition_derivation"] = derivation
        return derivation

    # The record's tuition is marked verified but no key this rule set can read
    # holds a number.  Say so, rather than leaving the reader to guess whether
    # the fee is zero or simply unrecorded.
    cost["tuition_derivation"] = {
        "standard": f"cost_model@{STANDARDS_VERSION}",
        "rule": "not_derivable",
        "reason": "income_based_range_without_upper_bound" if refused_income_band else "no_readable_tuition_figure",
        "derived_at": TODAY,
    }
    return None


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

    # Several American cost-of-attendance budgets already carry the health
    # plan as a living-cost line.  Adding the separately stored premium on top
    # would bill the same policy twice, which on the Stanford record was worth
    # USD 8,808 a year.
    insurance_in_living = "health_insurance" in set(col.get("components_included") or []) \
        | set(col.get("components_absorbed") or {})
    insurance = number(cost.get("health_insurance_premium_usd")) if currency == "USD" else None
    if insurance is not None and insurance_in_living:
        insurance = None
        included.append("health_insurance_within_living_costs")
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
# 2b. application fee
# --------------------------------------------------------------------------

# Only a key that names the application fee is ever read.  A housing
# application fee books a room, an enrolment fee falls due after an offer, and
# a stamp duty is part of the annual bill; none of them is the cost of
# applying, and each is filed under its own field.
APPLICATION_FEE_KEY = re.compile(r"(?:^|_)application_fee(?:_|$)", re.IGNORECASE)
FORBIDDEN_FEE_KEY = re.compile(
    r"housing|accommodation|residence|dorm|enrol|enroll|matricul|immatricul|"
    r"registration|deposit|tuition|stamp|regional|waiver|refund|scope|"
    r"breakdown|items|credit|payment_due|processing_time|lead_time|requires|"
    r"limited|possible|eligibility|request_deadline|"
    # This rule's own output and bookkeeping.  application_fee_standard carries
    # an amount and a currency, so without this the second run of the
    # standardizer would happily re-derive a fee from the first run's answer
    # and keep republishing it after the source key was removed.
    r"standard|research|verification|charged_|covers_|early_|additional_",
    re.IGNORECASE,
)
# The scope is stored as free text on the records that carry one at all, so it
# is matched rather than looked up.
FEE_SCOPE_PATTERNS = (
    (re.compile(r"non[ _-]?eu|non[ _-]?eea|third[ _-]?country", re.IGNORECASE), "non_eu_applicants"),
    (re.compile(r"international|overseas|other than us citizens|foreign", re.IGNORECASE), "international_applicants"),
    # Only an explicit statement about applicants.  "Most graduate programs"
    # says which programmes charge the fee, not who pays it.
    (re.compile(r"all applicants|every applicant|regardless of (?:nationality|citizenship)", re.IGNORECASE), "all_applicants"),
)

# A waiver that exists but is closed to anyone applying from abroad is not a
# waiver for this reader.  These are the ways the records say so in prose.
WAIVER_CLOSED_TO_INTERNATIONAL = re.compile(
    r"not available to international|are not available to international|"
    r"limited to eligible us|us citizens/permanent residents|us citizens and permanent residents|"
    r"only if currently attending a us|does not offer|is not published|are not published",
    re.IGNORECASE,
)


def _fee_currency_from_key(key: str) -> str | None:
    """Read the currency out of the key name itself, e.g. application_fee_gbp."""
    for currency in CURRENCY_SUFFIXES:
        if re.search(rf"(?:^|_){currency}(?:_|$)", key, re.IGNORECASE):
            return currency.upper()
    return None


def _fee_candidate_keys(profile: dict[str, Any]) -> list[tuple[str, Any]]:
    return [
        (key, value)
        for key, value in profile.items()
        if isinstance(key, str)
        and APPLICATION_FEE_KEY.search(key)
        and not FORBIDDEN_FEE_KEY.search(key)
    ]


# An item aimed at the domestic or EU route is not a fee this reader pays, and
# several records say so in the item's own basis rather than in its scope.
FEE_ITEM_NOT_FOR_THIS_READER = re.compile(
    r"not the central non[ _-]?eu|not for non[ _-]?eu|eu[ _-]?domestic|"
    r"(?:^|_)domestic(?:_|$)|home_applicant|eu_eea_only|(?:^|_)eu_only(?:_|$)",
    re.IGNORECASE,
)
# Ranked from the most specific description of this reader downwards.
FEE_ITEM_SCOPE_RANK = (
    (re.compile(r"non[ _-]?eu|third[ _-]?country", re.IGNORECASE), 3),
    (re.compile(r"international|overseas|foreign", re.IGNORECASE), 2),
    (re.compile(r"^(all|applicant|any)", re.IGNORECASE), 1),
)


def _fee_item_applies(item: dict[str, Any]) -> bool:
    text = f"{item.get('applicant_scope') or ''} {item.get('basis') or ''}"
    if FEE_ITEM_NOT_FOR_THIS_READER.search(text):
        return False
    return number(item.get("amount")) is not None and bool(item.get("currency"))


def _best_fee_item_group(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """The items that make up one bill, not two alternative routes.

    Items are grouped by the applicant they name; the group describing this
    reader most specifically wins, and only items inside that one group are
    added together.
    """
    groups: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for item in items:
        key = (str(item.get("applicant_scope") or ""), str(item.get("currency")).upper())
        groups.setdefault(key, []).append(item)

    def rank(key: tuple[str, str]) -> tuple[int, int]:
        scope = key[0]
        for pattern, score in FEE_ITEM_SCOPE_RANK:
            if pattern.search(scope):
                return (score, len(groups[key]))
        return (0, len(groups[key]))

    if not groups:
        return []
    return groups[max(groups, key=rank)]


def _charged_per(eligibility: dict[str, Any], origin: dict[str, Any], cost: dict[str, Any] | None = None) -> str:
    """Whether the fee buys one application, one programme choice, or a portal account."""
    researched = (cost or {}).get("application_fee_charged_per")
    if researched in {"application", "programme_choice", "admission_portal_account"}:
        return researched
    text = text_of(eligibility.get("application_fee_scope")) + " " + text_of(origin)
    if re.search(r"programme selections|program selections|per programme choice", text):
        return "programme_choice"
    if re.search(r"permits multiple programme applications|multiple applications|one fee.*multiple", text):
        return "admission_portal_account"
    return "application"


def _fee_scope(record: dict[str, Any], eligibility: dict[str, Any], cost: dict[str, Any],
               origin: dict[str, Any] | None = None) -> str:
    scope_text = " ".join(
        str(value)
        for key, value in list(eligibility.items()) + list(cost.items())
        if isinstance(key, str) and "application_fee" in key and "scope" in key and isinstance(value, str)
    )
    # An itemised fee names its applicant on the item that was chosen.
    for value in (origin or {}).values():
        if isinstance(value, list):
            scope_text += " " + " ".join(
                str(item.get("applicant_scope")) for item in value
                if isinstance(item, dict) and item.get("applicant_scope")
            )
    # A key that says "international" in its own name carries the same fact.
    scope_text += " " + " ".join(
        key for key in list(eligibility) + list(cost)
        if isinstance(key, str) and "application_fee" in key and "international" in key
    )
    for pattern, code in FEE_SCOPE_PATTERNS:
        if pattern.search(scope_text):
            return code
    return "unknown"


def _fee_waiver(eligibility: dict[str, Any]) -> dict[str, Any]:
    """Collect what the record says about getting the fee waived.

    ``available`` is read only from a stored boolean, never inferred from
    prose - a sentence can say a waiver exists and in the same breath close it
    to everyone this database is written for.  The prose answers the narrower
    question the reader actually has: can *I* use it.  Where neither is
    recorded the answer stays null, and the university's own wording is
    carried through so nothing is paraphrased into a claim.
    """
    available = eligibility.get("application_fee_waiver_possible")
    note = eligibility.get("application_fee_waiver") or eligibility.get(
        "application_fee_waiver_international_eligibility"
    )

    open_to_international = None
    prose = " ".join(
        text_of(eligibility.get(key))
        for key in ("application_fee_waiver", "application_fee_waiver_international_eligibility")
    ).strip()
    if prose:
        open_to_international = not WAIVER_CLOSED_TO_INTERNATIONAL.search(prose)
    if eligibility.get("international_application_fee_waiver_available_from_department") is False:
        open_to_international = False

    waiver = {
        "available": available if isinstance(available, bool) else None,
        "open_to_international": open_to_international,
        "request_deadline": iso_date(eligibility.get("application_fee_waiver_request_deadline")),
        "processing_days": eligibility.get("application_fee_waiver_processing_time_business_days")
        or eligibility.get("application_fee_waiver_safe_lead_time_business_days"),
    }
    if isinstance(note, dict):
        waiver["note"] = note
    return waiver


def build_application_fee(record: dict[str, Any]) -> dict[str, Any]:
    """Publish the one-off charge that falls due before anything else does.

    The figure was already researched for a third of the catalogue, but it was
    stored under seven different key names across two profiles and five
    currencies, so nothing downstream could read it.  This moves whichever key
    the record actually used into one shape and records which key that was.
    """
    cost = record.setdefault("cost_profile", {})
    eligibility = record.get("eligibility_profile") or {}
    financials = record.get("financials") or {}

    def unknown(reason: str) -> dict[str, Any]:
        published = {
            "standard": f"application_fee@{STANDARDS_VERSION}",
            "status": "unknown",
            "amount": None,
            "currency": None,
            "reason": reason,
            "evaluated_at": TODAY,
        }
        cost["application_fee_standard"] = published
        return published

    if not (verified_fields(record) & {"admission", "tuition", "cost", "costs", "fees"}):
        return unknown("record_does_not_verify_admission_or_cost")
    if not (sourced_fields(record) & {"admission", "tuition", "fee", "fees", "cost", "costs", "application_fee"}):
        return unknown("no_reachable_source_covering_admission_or_cost")

    amount: float | None = None
    currency: str | None = None
    rule: str | None = None
    origin: dict[str, Any] = {}
    components: list[dict[str, Any]] = []

    # 1. an itemised list.  Items are grouped by the applicant they are for
    # before anything is summed: a record can carry two fees that are
    # alternative routes rather than two halves of one bill, and Politehnica
    # Bucharest carries exactly that - a RON 100 July route and a RON 50 early
    # route, both of which its own basis marks as not the non-EU route.
    # Summing them would invent a RON 150 charge that nobody pays.
    items = [item for item in non_empty_list(cost.get("application_fee_items")) if isinstance(item, dict)]
    refused_items: list[dict[str, Any]] = []
    academic_cycle = None
    if items:
        applicable = [item for item in items if _fee_item_applies(item)]
        refused_items = [item for item in items if item not in applicable]
        group = _best_fee_item_group(applicable)
        if group:
            item_currency = str(group[0].get("currency")).upper()
            totals = [number(item.get("amount")) for item in group]
            totals = [value for value in totals if value is not None]
        else:
            item_currency, totals = None, []
        if item_currency and totals:
            amount = round(sum(totals), 2)
            currency = item_currency
            rule = "published_no_fee" if amount == 0 else (
                "sum_of_published_components" if len(totals) > 1 else "published_application_fee"
            )
            origin = {"application_fee_items": group}
            academic_cycle = next((item.get("academic_cycle") for item in group if item.get("academic_cycle")), None)
            components = [
                {
                    "label": item.get("basis") or item.get("applicant_scope") or item.get("period"),
                    "amount": number(item.get("amount")),
                    "currency": item_currency,
                }
                for item in group
            ] if len(group) > 1 else []
            refundable_item = next((item.get("refundable") for item in group if "refundable" in item), None)
            if isinstance(refundable_item, bool):
                cost.setdefault("application_fee_refundable", refundable_item)

    breakdown = eligibility.get("application_fee_breakdown")
    if amount is None and isinstance(breakdown, dict):
        parts = [(key, number(value)) for key, value in breakdown.items() if number(value) is not None]
        breakdown_currency = next(
            (_fee_currency_from_key(key) for key, _ in parts if _fee_currency_from_key(key)), None
        )
        if parts and breakdown_currency:
            amount = round(sum(value for _, value in parts), 2)
            currency, rule = breakdown_currency, "sum_of_published_components"
            origin = {"application_fee_breakdown": breakdown}
            components = [{"label": key, "amount": value, "currency": breakdown_currency} for key, value in parts]

    # 2. a scalar or object key naming the fee, wherever it was filed.
    if amount is None:
        for profile_name, profile in (
            ("cost_profile", cost),
            ("eligibility_profile", eligibility),
            ("financials", financials),
        ):
            if not isinstance(profile, dict):
                continue
            for key, value in _fee_candidate_keys(profile):
                if isinstance(value, dict):
                    candidate = number(value.get("amount"))
                    candidate_currency = str(value.get("currency") or "").upper() or None
                else:
                    candidate = number(value)
                    candidate_currency = _fee_currency_from_key(key)
                if candidate is None or not candidate_currency:
                    continue
                amount, currency = candidate, candidate_currency
                rule = "published_no_fee" if candidate == 0 else "published_application_fee"
                origin = {f"{profile_name}.{key}": value}
                break
            if amount is not None:
                break

    if amount is None:
        # A researcher who read the official application pages and found no
        # charge has answered the question; that is a different answer from
        # nobody having looked, and the pages travel with it so the reader can
        # check the same ones.
        research = cost.get("application_fee_research")
        if isinstance(research, dict) and research.get("outcome") == "no_fee_published":
            pages = [str(url) for url in non_empty_list(research.get("pages_checked"))]
            published = {
                "standard": f"application_fee@{STANDARDS_VERSION}",
                "status": "not_published",
                "amount": None,
                "currency": None,
                "rule": "researched_absence",
                "pages_checked": pages,
                "checked_on": research.get("checked_on"),
                "note": research.get("note"),
                "evaluated_at": TODAY,
            }
            if refused_items:
                published["refused_items"] = refused_items
            cost["application_fee_standard"] = published
            return published
        # Every published item names a route this reader cannot use, and no
        # researcher has read the pages for the route they can.  Say which
        # routes were priced rather than leaving the fee simply blank.
        if refused_items:
            published = unknown("published_fees_are_for_routes_a_non_eu_applicant_cannot_use")
            published["refused_items"] = refused_items
            return published
        return unknown("no_readable_application_fee_key")

    waiver_source = eligibility if isinstance(eligibility, dict) else {}
    fee_object = next((value for value in origin.values() if isinstance(value, dict) and "waiver_possible" in value), None)
    waiver = _fee_waiver(waiver_source)
    if isinstance(fee_object, dict) and waiver["available"] is None:
        waiver["available"] = fee_object.get("waiver_possible")
    # Oxford stores the waiver categories on the fee object itself.
    for value in origin.values():
        if isinstance(value, dict) and value.get("waiver_categories"):
            waiver["available"] = True
            waiver["categories"] = value["waiver_categories"]

    refundable = eligibility.get("application_fee_refundable")
    if refundable is None:
        refundable = cost.get("application_fee_refundable")

    published = {
        "standard": f"application_fee@{STANDARDS_VERSION}",
        "status": "no_fee" if amount == 0 else "published",
        "amount": amount,
        "currency": currency,
        "amount_eur_equivalent": to_eur(amount, currency) if currency != "EUR" and amount else None,
        "scope": _fee_scope(record, eligibility, cost, origin),
        "charged_per": _charged_per(eligibility, origin, cost),
        "charged_by": cost.get("application_fee_charged_by") or "university",
        "charged_by_name": cost.get("application_fee_charged_by_name"),
        "additional_application_amount": number(cost.get("application_fee_additional_amount")),
        "academic_cycle": academic_cycle or cost.get("application_fee_academic_cycle"),
        # An early window that costs less is a deadline with a price on it, so
        # both amounts and the date between them travel with the fee.
        "early_amount": number(cost.get("application_fee_early_amount")),
        "early_deadline": iso_date(cost.get("application_fee_early_deadline")),
        "covers_programmes": number(cost.get("application_fee_covers_programmes")),
        "refundable": refundable if isinstance(refundable, bool) else None,
        "components": components,
        "waiver": waiver,
        "payment_due_days_after_deadline": eligibility.get("application_fee_payment_due_days_after_deadline"),
        "rule": rule,
        "derived_from": origin,
        "note": {
            "en": "Paid once, when you apply. It is never added to the annual total, because a one-off charge folded into a per-year figure would recur for every year of the degree.",
            "tr": "Basvuru sirasinda bir kez odenir. Yillik toplama hicbir zaman eklenmez; tek seferlik bir kalem yillik bir rakamin icine katilsaydi diplomanin her yili icin tekrarlardi.",
        },
        "evaluated_at": TODAY,
    }
    cost["application_fee_standard"] = published
    return published


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

# A record's deadline_events[] mixes three different kinds of date: dates a new
# applicant can still act on, dates that only bind someone who already holds an
# offer, and dates that are simply the calendar of the term.  Treating them
# alike is what makes a closed programme advertise a countdown - a deposit due
# date or the first day of teaching is not an invitation to apply.
#
# An event has to look like an application step AND not be aimed at someone
# already admitted before it can become the headline countdown.
APPLICATION_EVENT_WORDS = re.compile(
    # "applica" is the common prefix of application and applicant; separators
    # are normalised to spaces by event_text, so patterns are space-separated.
    r"applica|apply|admission|call for|intake|round|selection|competition|"
    r"scholarship|funding|bursary|fellowship|fee waiver",
    re.IGNORECASE,
)
# Checked after the words above, so "application" in "housing application" or
# "scholarship application" does not smuggle a non-application step through.
NON_APPLICATION_EVENT_WORDS = re.compile(
    # Deliberately narrow: only steps that cannot exist before an offer.
    # "visa required applicant ..." names who may apply rather than a visa
    # milestone, so only a visa step about the visa itself is excluded.  A
    # scholarship or funding deadline stays eligible - an applicant acts on it.
    r"deposit|conditions?\s+deadline|\bcas\b|atas|visa(?!\s+required)|"
    r"pre ?enrol|enrol|enroll|matricul|immatricul|"
    r"commence|begin|start|teaching|induction|orientation|arrival|"
    r"housing|accommodation|residence|"
    r"deferral|verification|verify|offer reply|offer acceptance|opened|opens",
    re.IGNORECASE,
)
# Explicit audience markers some records carry alongside the event.
ADMITTED_SCOPE_WORDS = re.compile(
    r"admitted|offer_holder|offer holders|existing_offer|enrolled|matriculated",
    re.IGNORECASE,
)


def event_text(event: dict[str, Any]) -> str:
    """Every field that could name the event or its audience, as one string."""
    parts = [
        event.get("event"),
        event.get("name"),
        event.get("label"),
        event.get("applicant_scope"),
        event.get("audience"),
        event.get("status"),
        event.get("status_as_of_last_checked"),
        event.get("date_status"),
    ]
    joined = " ".join(str(p) for p in parts if isinstance(p, str))
    # Event names are snake_case, and "_" counts as a word character, so a
    # pattern like \bUK\b would never match inside "UK_course_application".
    return re.sub(r"[_\-]+", " ", joined)


def event_is_new_applicant_deadline(event: dict[str, Any]) -> bool:
    """True when a person who has not applied yet could still act on this date."""
    text = event_text(event)
    if not text.strip():
        return False
    if ADMITTED_SCOPE_WORDS.search(text):
        return False
    if not APPLICATION_EVENT_WORDS.search(text):
        return False
    if NON_APPLICATION_EVENT_WORDS.search(text):
        return False
    return True


def event_audience(event: dict[str, Any]) -> str:
    text = event_text(event)
    if ADMITTED_SCOPE_WORDS.search(text):
        return "admitted_or_offer_holders"
    if re.search(r"non ?eu|overseas|international|visa required", text, re.IGNORECASE):
        return "non_eu"
    if re.search(r"\beu\b|eea|home|\buk\b|domestic", text, re.IGNORECASE):
        return "eu_eea"
    return "all_applicants"


def event_label(event: dict[str, Any]) -> str | None:
    for key in ("event", "name", "label"):
        value = event.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


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

    today = date.today()

    # Events are split rather than pooled: only the ones a new applicant could
    # act on may set the countdown, and the rest are kept as milestones so the
    # dates stay available to somebody who is already admitted.
    other_milestones: list[dict[str, Any]] = []
    for event in non_empty_list(timeline.get("deadline_events")):
        if not isinstance(event, dict):
            continue
        parsed = iso_date(event.get("date") or event.get("deadline"))
        if not parsed:
            continue
        label = event_label(event)
        if event_is_new_applicant_deadline(event):
            origin = "application_timeline_profile.deadline_events[]"
            if label:
                origin += f" ({label})"
            candidates.append((parsed, event_audience(event), origin))
        elif date.fromisoformat(parsed) >= today:
            other_milestones.append(
                {
                    "date": parsed,
                    "event": label,
                    "audience": event_audience(event),
                    "source_url": event.get("source_url"),
                }
            )

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
    # Kept on every record, including the ones with no application date left, so
    # a closed cycle can still explain what the remaining published dates are
    # instead of silently borrowing one of them for the countdown.
    primary["audience"] = "new_applicants"
    primary["other_milestones"] = sorted(other_milestones, key=lambda item: item["date"])
    timeline["primary_deadline"] = primary
    return primary


# --------------------------------------------------------------------------
# runner
# --------------------------------------------------------------------------

def standardize(record: dict[str, Any]) -> dict[str, Any]:
    housing = build_housing_difficulty(record)
    # Both derivations run before the total, because the total is assembled
    # from the canonical fields they populate.
    derive_annual_tuition(record)
    build_cost_of_living(record)
    cost = build_normalized_cost(record)
    application_fee = build_application_fee(record)
    match = build_academic_match(record)
    deadline = build_primary_deadline(record)
    return {
        "housing_level": housing["level"],
        "cost_status": cost["status"],
        "application_fee_status": application_fee["status"],
        "match_tier": match["tier"],
        "deadline_status": deadline["status"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="rewrite the JSON files in place")
    args = parser.parse_args()

    tally = {
        "housing_level": Counter(),
        "cost_status": Counter(),
        "application_fee_status": Counter(),
        "match_tier": Counter(),
        "deadline_status": Counter(),
    }
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
