# Category Standards

Every categorical label UniRank shows a student — housing difficulty, the
basis of a cost figure, an academic-match tier, when to email a professor,
when a scholarship step is due — is defined once in
[`config/standards.json`](../config/standards.json) and served to the
interface at `GET /api/standards`.

The rule behind this file is simple: **a category is not a fact until the
criteria that produced it travel with it.** The interface never prints a
level on its own; it prints the level, the criteria text, the evidence that
scored each criterion, and a link to the official page that evidence came
from.

## Why the old values could not stay

| Field | What went wrong | What replaced it |
|---|---|---|
| `housing_difficulty` | Free text mixed a level with its reason — `high_no_guarantee`, `competitive_adisu_or_self_search`, `conditional_guarantee_if_deadline_met`. Fourteen distinct strings existed across 65 populated records; they could not be sorted, filtered or compared, and a genuine guarantee had no code at all. | A four-level ordinal scale plus `unknown`, scored from five evidenced dimensions. The reason now lives in `housing_difficulty_profile`, separately from the level. |
| `monthly_living_cost_eur_estimated` and its many currency twins | A bare number with no record of what it covered, how many months it applied to, which currency it was published in or which rate converted it. Two records could show the same figure while one meant rent for nine months and the other a twelve-month budget including insurance. | `cost_of_living_profile`, which carries `cost_basis`, `components`, `months_covered`, `currency` and an explicitly labelled euro conversion. |
| `relevance_status` | One adjective — `strong` on 80 of 177 records — collapsed five different questions into one. | `academic_match_profile`, which scores curriculum, research group, faculty, facility and industry evidence separately and only then produces a tier. |
| `notable_professors[].email` | Present on two records in the whole database, with no record of which page published the address. | An `email_source` URL is now required beside every stored address, and a test fails the build without it. |
| Deadlines | Stored as `2026-01-15 (23:59 CET; non-EU/EFTA with international BSc; closed)` — human-readable, machine-useless. A past cycle's date outranked the current open one. | `primary_deadline`, which parses the leading ISO date, prefers the next date a student can still act on, and marks a past recurring date `closed` beside its `next_expected_date`. |

## The six scales

### 1. Housing difficulty

`low` → `medium` → `high` → `very_high`, plus `unknown`.

The level is the banded sum of five dimensions:

| Dimension | Max | Question |
|---|---|---|
| `guarantee_status` | 4 | Is a room guaranteed to this applicant group? |
| `supply_pressure` | 4 | Does an official source document excess demand? |
| `market_affordability_gap` | 3 | How does median private rent compare with the official student housing budget? |
| `timing_sensitivity` | 2 | Does a separate, dated housing application gate access? |
| `arrival_risk` | 2 | Can a student arrive without a signed contract? |

Rules the code enforces and the tests guard:

- Fewer than three evidenced dimensions publishes `unknown`, never a level.
- A partial profile is rescaled onto 0–15 before banding, and confidence is
  capped at `medium`.
- `very_high` additionally requires the specific structural signal its written
  criteria name — an official statement that most internationals cannot be
  housed, or official advice not to travel without a contract. Arithmetic alone
  cannot reach the top band.
- A level may never be inferred from country reputation, QS rank or city size.
  Forum posts feed `housing_sentiment` only.

### 2. Cost model

`cost_of_living_profile` records the **basis** (`official_university_cost_of_attendance`,
`official_university_living_budget`, `official_visa_financial_requirement`,
`official_national_student_survey`, `official_housing_provider_rates`,
`unknown`), the **components** it covers, and the **period** it covers.

A visa financial requirement is a legal floor, not an observed average, and the
interface says so wherever that basis is used.

`normalized_cost.annual_total` is published only when tuition and a
component-checked living budget are both verified **in the same currency**.
Otherwise the parts are shown separately and `missing_mandatory_components`
names what is missing. Euro conversions carry `fx_rate`, `fx_rate_date` and
`fx_source` from [`config/fx_rates.json`](../config/fx_rates.json) and are
always labelled as conversions.

### 3. Application fee

`cost_profile.application_fee_standard` publishes the one-off charge that falls
due before every other amount on the cost card, with a status rather than a
silence when there is no number:

| Status | Meaning |
|---|---|
| `published` | A positive amount read from a key that names the application fee |
| `no_fee` | A zero on such a key, or a university that says in words it charges nothing |
| `not_published` | The official application pages were read on a recorded date and none of them charges — the pages travel with the value |
| `unknown` | Nobody has looked, or the figure failed a guard |

`not_published` is deliberately not the same answer as `no_fee`, and neither is
the same as `unknown`. An absent key is never read as a zero.

Rules the code enforces:

- A housing application fee, an enrolment or matriculation fee, a pre-enrolment
  portal step and a stamp duty are four charges that look like an application
  fee and are not one. Each is read only from its own field.
- The fee is never added into `normalized_cost.annual_total`. It is paid once,
  before there is a place to pay for, and folding a one-off charge into a
  per-year figure would make it recur for every year of the degree.
- Fee items are grouped by the applicant they name before anything is summed,
  and only one group is ever added up. Politehnica Bucharest publishes a
  RON 100 July route and a RON 50 early route and says of each that it is not
  the central non-EU route; summing them would invent a charge nobody pays.
- `charged_by` and `charged_by_name` record who takes the money. Many German
  programmes are applied for through uni-assist, which charges EUR 75 for the
  first course of study in a semester and EUR 30 for each further one and is
  not the university.
- `charged_per` records what the payment buys. Sweden charges SEK 900 once per
  semester through universityadmissions.se however many programmes are on the
  list, so calling it per-application would multiply one payment by the size of
  a shortlist.
- `early_amount` and `early_deadline` publish both prices and the date between
  them where a university charges less inside an early window, because that
  date costs money to miss and not only a place.

### 4. Academic match

Five weighted dimensions — curriculum (30), research group (25), faculty (25),
facility (10), industry outlet (10) — each scored `strong` / `moderate` /
`weak` / `none` / `unknown`. The score is normalised over the weights of the
**evidenced** dimensions, so an unverified dimension neither raises nor lowers
it. A tier is published only from three evidenced dimensions upward.

### 5. Faculty contact

`contact_timing` is an enum, and each value ships with guidance the interface
prints beside the professor's card, because "when do I email them" has a
different answer in Munich than in Atlanta.

An email address is stored only when an official university page publishes it,
and `email_source` must name that page. Addresses are never reconstructed from
a naming pattern. Where a department publishes phone numbers but hides emails
behind an image — TUM, RWTH — the record says so instead of guessing.

### 6. Scholarship playbook

Each opportunity carries `eligibility_gates` (fail one and you are out),
`selection_criteria` (what the committee actually scores) and ordered `steps`
with a `timing` enum, an owner and a `hard_requirement` flag. A step is written
only from an official scholarship or financial-aid page — generic advice does
not become a step unless the funder publishes it as a requirement.

## Working with the data

```bash
# See what the standards would produce, without writing
python scripts/standardize_categories.py

# Apply them to data_base/
python scripts/standardize_categories.py --write
```

Researched facts arrive as payloads under `research_queue/enrichment/`. The
applier deep-merges them and refuses to run when a payload changes a
decision profile without a source covering that field:

```bash
python scripts/apply_enrichment.py                              # validate
python scripts/apply_enrichment.py --payload italy_2026_08.json --write
```

The usual order after a research session:

```bash
python scripts/apply_enrichment.py --write
python scripts/refresh_data_quality.py --record-id <id> --write   # per touched record
python scripts/standardize_categories.py --write
python scripts/run_canary_checks.py
python -m pytest tests -q
```

### Supplying evidence the deriver cannot infer

Two escape hatches let a researcher state something the text heuristics cannot
work out, while keeping the quote and the URL attached to it:

```json
"living_profile": {
  "housing_difficulty_evidence": {
    "supply_pressure": {
      "value": "demand_exceeds_supply_stated",
      "source_url": "https://…",
      "quote": "It is very difficult to find a room in Delft and its surroundings."
    }
  },
  "cost_of_living_evidence": {
    "cost_basis": "official_university_living_budget",
    "currency": "EUR",
    "months_covered": 12,
    "components": { "rent": 550, "food": 175, "transport": 25, "personal": 165 },
    "source_url": "https://…"
  }
}
```

and, at record level:

```json
"academic_match_evidence": {
  "research_group_evidence": { "level": "strong", "basis": "…", "source_url": "https://…" }
}
```

Explicit evidence always wins over the derived value, and the quote is
rendered to the student inside the housing panel.

An application fee has a third hatch, for the answer no key can carry: the
university charges nothing, so there is no number to store. Recording which
pages were read is what separates that from nobody having looked.

```json
"cost_profile": {
  "application_fee_research": {
    "outcome": "no_fee_published",
    "checked_on": "2026-09-01",
    "pages_checked": ["https://…", "https://…"],
    "note": { "en": "…", "tr": "…" }
  }
}
```

## What the interface does with all this

`public/standards.js` fetches the definitions once per session;
`public/decisionPanels.js` renders seven panels from them:

- **Time left to apply** — days remaining, status, audience, cycle, and the
  next expected date when a recurring cycle has closed.
- **Academic match analysis** — tier, score, and each dimension with its
  evidence link.
- **Average expenses** — the monthly figure, its basis, the component
  breakdown, what is excluded, and the annual total with its inclusion list.
- **What to do to win the funding** — eligibility gates, what the committee
  scores, and numbered steps with timing chips.
- **Housing difficulty — how it was scored** — the level, the criteria text,
  the meter, and every dimension with its official quote.
- **Laboratories and research groups** — each unit with its topics, facilities,
  student access and a "why this fits you" note tied to taxonomy tags.
- **Faculty contacts** — name, role, focus, tags, unit, email with a copy
  button and its source, and the contact-timing guidance.

Each panel renders only when the record carries the evidence for it, so an
unresearched programme shows nothing rather than an empty shell.

`public/applicationFee.js` is the single reader of the application-fee block,
so nothing that shows the fee can disagree with anything else about it. It
reaches the reader in four places, each answering a different question:

- **A cell on every result card** — because a shortlist is drawn up on the
  list, not in the drawer, and what applying costs is part of whether the
  shortlist is affordable.
- **A panel in the drawer**, next to the countdown it shares a date with —
  the amount, who takes the money, what the payment buys, the waiver with its
  own deadline and lead time, the early window, and the pages that were read
  when no fee was found.
- **A chip on every calendar card**, and the amount beside each runway
  milestone.
- **One euro total for whatever the calendar is currently showing** — narrow
  it to your favourites and it answers what your shortlist costs to apply to.
  A payment covering several programmes is counted once, so four Swedish
  programmes add SEK 900 to that total rather than SEK 3,600.
