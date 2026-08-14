# UniRank Research Data Standard v2

Status: normative for all new and revised records.

This standard defines a programme-centred decision-support database for a
non-EU Master's applicant. One record represents exactly one active or
historically identified university-programme pair. Institution prestige is
never a substitute for programme evidence.

## 1. Canonical artefacts

- `research_templates/program_record_v2.json`: programme record.
- `research_templates/country_record_v2.json`: country-wide policy record.
- `research_templates/source_claim_template.json`: source and claim linkage.
- `data_base/taxonomy.json`: approved technical taxonomy.
- `checklists/canary_tests.md`: mandatory final safety gate.

All internal keys are English. Every narrative shown to a user is a bilingual
object: `{ "en": "...", "tr": "..." }`.

## 2. Identity and scope

- `schema_version` is required and uses semantic versioning.
- `record_type` is `program` or `country`.
- A programme ID is stable and must not encode a changing academic year.
- One programme, degree award, campus and delivery mode form one record.
- Joint degrees are one record only when the universities jointly award the
  same programme; otherwise each admission route is separate.
- Candidate records may remain in the database with
  `program_status: needs_verification`, but cannot be marked QC-passed.
- The active catalogue currently exposes Europe, Turkey and the United States.
  Asian records remain excluded until migrated and re-audited; no compatibility
  fields may be added to new records for the sake of those excluded files.

## 3. Fact representation

Unknown numeric value: `null`. Unknown category: `unknown`. Unknown list: `[]`.
Never use a plausible number as a placeholder.

Money is recorded in the source currency:

```json
{
  "amount": null,
  "minimum": null,
  "maximum": null,
  "currency": "EUR",
  "period": "academic_year",
  "applicant_scope": "non_eu",
  "academic_cycle": "2026/2027",
  "mandatory": true,
  "basis": "published programme tuition",
  "source_ids": ["src_tuition_1"]
}
```

If conversion is needed for comparison, keep the original amount and record
the converted amount, exchange-rate provider and rate date separately. UI
conversions are display values, never research facts.

Dates are represented as structured deadline events. A future date may only be
shown as current when an official source publishes it. Older official dates use
`date_status: historical`. A recurring annual rule uses `recurring`. UniRank
does not manufacture an estimated deadline from last year's date. Historical
patterns may support bilingual planning advice, but not a fake date.

## 4. Required programme profiles

Every programme record includes:

1. identity, institution, campus and programme basics;
2. `eligibility_profile`, including previous degree, prerequisites, document
   list, non-EU route, selection method and explicit GRE policy;
3. `language_profile`, including teaching language, accepted tests, minimums,
   subscore rules and exemptions;
4. `cost_profile`, including tuition, mandatory fees, deposits, application
   fee, insurance and published cost-of-attendance items;
5. `scholarship_profile`, including applicant eligibility, coverage,
   competitiveness, whether consideration is automatic or separate, and its
   own deadline events;
6. `living_profile`, including university housing availability, guarantee or
   lottery status, separate housing application, official budget/rent facts,
   commute and housing risk;
7. `curriculum_profile`, including curriculum cycle, total course/module count
   when officially derivable, required/elective modules, tracks, thesis,
   internship, lab/project work and mobility;
8. `category_profile`, linked to curriculum/lab evidence rather than title;
9. `research_profile`, with labs, centres, projects, facilities and evidence;
10. `industry_ecosystem_profile`, separating nearby organisations from
    officially confirmed partners;
11. `application_timeline_profile`, with applicant-specific deadline events,
    result timing, enrolment, pre-enrolment and visa-sensitive steps;
12. `ranking_profile`, separating institutional global rank, subject rank,
    accreditation and programme reputation. Rankings never establish technical
    fit;
13. `outcomes_profile`, for official career, doctoral progression or graduate
    outcome evidence when available;
14. `student_sentiment_profile`, containing perception signals only;
15. `source_profile`, `decision_summary`, `scoring_inputs` and
    `quality_control`.

## 5. GRE and language policy

GRE is never stored as a generic boolean. `gre.policy` must be one of:

- `required`
- `optional`
- `recommended`
- `not_required`
- `not_accepted`
- `waived`
- `unknown`

Store General/Subject test, minimums, percentile guidance, validity rules and
waivers only when the official admission source states them.

For English, store each accepted test separately with overall and subscore
minimums. “Programme page is in English” is not language evidence. A medium-of-
instruction exemption is recorded only when the official policy states the
eligible countries/degrees and any time limit.

## 6. Scholarship and assistantship policy

`application_mode` is one of `automatic`, `separate`, `mixed`, `nomination`,
`invitation_only`, `not_available`, or `unknown`. Separate awards receive their
own deadline records. US assistantships must distinguish Master's and PhD
eligibility, RA/TA availability, tuition remission, stipend, guarantee status
and whether contacting faculty is expected. “Funding exists” never means an
incoming Master's student is guaranteed funding.

## 7. Housing policy

`housing_access` is one of `guaranteed`, `priority`, `lottery`, `waitlist`,
`first_come_first_served`, `not_guaranteed`, `not_offered`, or `unknown`.
University-owned housing, affiliated housing and private-market guidance are
separate. Official budgets do not prove room availability. Student reports may
describe search difficulty only in the sentiment profile.

## 8. Sources and claim linkage

Every source has a stable `source_id`, final URL, title, publisher, source type,
access status, checked date, applicable academic cycle, confidence and notes.
Critical source access must be `ok`, `redirects`, or `pdf`.

`source_profile.evidence_map` maps field groups or JSON paths to source IDs.
The source's `relevant_fields` must agree with the evidence map. A generic home
page or incorrectly labelled programme page cannot support tuition, funding or
housing claims.

Current critical evidence groups are:

- program
- language
- admission
- non_eu_eligibility
- tuition
- scholarship
- deadline
- curriculum
- housing

Research, industry, ranking and outcomes remain required for a professional
decision record, but honest absence does not permit an invented claim.

## 9. Student sentiment

Sentiment is isolated from official facts. Record source dates, approximate
sample size, programme/campus relevance and repeated themes. A 0-100 score is
allowed only with at least three documented observations, a date range and
cited sentiment sources; confidence is normally low unless sources are recent,
independent and consistent.

## 10. Quality states

- `candidate`: programme discovered but not decision-ready.
- `needs_revision`: at least one critical evidence group or decision value is
  missing, stale, contradictory or unsupported.
- `passed`: all critical evidence groups have accessible official sources, the
  record contains usable decision values or an explicitly verified absence,
  links were checked, no canary test fails and decision risks are bilingual.
- `stale`: a previously passed record is outside its review window or its cycle
  has ended.

Verification is cycle-sensitive. Tuition, deadlines, scholarship and housing
are reviewed at least once per admissions cycle; programme status and language
are rechecked annually. `last_verified` alone is insufficient: each source and
deadline/cost item carries its own cycle/date.

## 11. Research completion rule

A record is not complete merely because every JSON key exists. It is complete
when the student's practical questions can be answered from current official
sources, uncertainty is explicit, contradictory evidence is resolved or
documented, and observer, reviewer, auditor and student walkthroughs do not
identify a decision that still requires an external search.
