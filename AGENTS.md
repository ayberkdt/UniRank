# AGENTS.md — UniRank Research & Data Integrity Rules

## Project Purpose

UniRank is a decision-support database for students who want to evaluate universities and degree programs, especially in aerospace engineering, space engineering, aeronautics, astronautics, GNC, CFD, propulsion, structures, spacecraft systems, satellite systems, and related technical fields.

The goal is not to create a shallow university ranking list. The goal is to help a student answer:

- Can I realistically apply to this program?
- Is the program technically relevant to my target field?
- Is the program actually taught in a language I can study in?
- What is the real cost and scholarship possibility?
- Are the sources official and up to date?
- What are the risks: admission, language, cost, housing, visa, deadline, data uncertainty?
- What do students generally report about satisfaction, workload, housing, administration, and career outcomes?

## Absolute Research Rules

The following rules are mandatory.

1. Never invent facts.
2. Never estimate tuition, deadlines, language requirements, scholarship availability, admission requirements, or program status without a source.
3. If a value cannot be verified, write `unknown`, `null`, `[]`, or `needs_verification`.
4. Every critical data field must be linked to at least one source.
5. Official sources have priority over third-party sources.
6. Forum and student-review sources must never override official sources.
7. Forum and student-review sources may only be used for student sentiment, satisfaction, housing difficulty, workload perception, administrative experience, social experience, and informal employability impressions.
8. Every URL added to the database must be checked for accessibility.
9. Broken links must not be used as valid sources.
10. If a page is accessible but unclear, stale, archived, or not official, mark the relevant field confidence as `medium`, `low`, or `unknown`.
11. Do not compress multiple programs into one record. Each university-program pair must be its own record.
12. Do not treat university prestige as technical fit.
13. Do not treat QS rank as evidence of aerospace/space strength.
14. Do not treat the existence of a company in the same country as a university partnership.
15. Do not treat a program name as proof of curriculum depth. Curriculum, tracks, courses, labs, or research groups must be checked.
16. Do not treat “English page exists” as proof that the program is taught in English. Teaching language must be verified.
17. Do not treat “scholarship exists” as proof that non-EU students are eligible. Eligibility must be verified.
18. Do not treat “low tuition” as total affordability. Housing, living cost, regional fees, scholarship, and visa timeline must be checked.
19. Always distinguish official data, interpreted data, and student sentiment.
20. Always include `last_verified` date for newly researched records.

## Source Priority

Use sources in this order:

1. Official university program page
2. Official admission page
3. Official curriculum/study plan/course catalogue
4. Official tuition/fees page
5. Official scholarship/financial aid/DSU page
6. Official department/research group/lab page
7. Official government, ministry, migration, visa, or national admission portal
8. Official university housing/student services page
9. Official partner/company/institute page confirming collaboration
10. Reliable third-party databases only as secondary checks
11. Student forums, Reddit, The Student Room, GradCafe, Quora, Discord mirrors, Facebook groups, Google reviews, Studyportals reviews, Mastersportal reviews, etc. only for sentiment and informal experience

## Critical Fields That Require Official Sources

The following fields require official or highly authoritative sources:

- program name
- degree level
- duration
- ECTS
- teaching language
- admission requirements
- non-EU eligibility
- required previous degree
- required documents
- tuition
- scholarship eligibility
- scholarship deadline
- curriculum
- tracks/specializations
- application deadline
- pre-enrolment requirement
- visa-related official steps
- official program status
- department/lab existence
- official industry partnership

If official sources cannot be found, mark the field as `unknown` or `needs_verification`.

## Student Sentiment Fields

Student forums and review sources may be used only for the following fields:

- student_satisfaction_score
- workload_sentiment
- teaching_quality_sentiment
- administration_sentiment
- housing_sentiment
- city_life_sentiment
- international_student_sentiment
- career_support_sentiment
- student_sentiment_summary
- student_sentiment_sources
- sentiment_confidence

Student sentiment must never be treated as a fact. It is only a perception signal.

## Confidence Levels

Every major field group must receive a confidence level:

- `high`: official source, current, clear, directly relevant.
- `medium`: official source exists but is incomplete, ambiguous, or requires interpretation.
- `low`: third-party source, forum source, old source, weak evidence, or indirect evidence.
- `unknown`: no reliable source found.

Use field-level confidence in `source_profile.field_confidence`.

## Required Research Workflow

For each country:

1. Create or update country-level metadata.
2. Identify candidate universities.
3. Verify each candidate program exists and is active.
4. Verify degree level, duration, ECTS, language, and curriculum.
5. Verify admission requirements and non-EU applicability.
6. Verify tuition and fee structure.
7. Verify scholarship and funding opportunities.
8. Verify deadlines and application timeline.
9. Verify research/lab/department strength.
10. Verify industry ecosystem using official or reliable sources.
11. Collect student sentiment from forums/reviews separately.
12. Normalize categories using the taxonomy.
13. Assign source confidence.
14. Generate decision summary.
15. Run quality-control checklist.
16. Run canary tests.
17. Only then update JSON database.

## Required Output for Each Program

Each program entry must include:

- basic program info
- eligibility_profile
- language_profile
- cost_profile
- scholarship_profile
- living_profile
- curriculum_profile
- category_profile
- research_profile
- industry_ecosystem_profile
- application_timeline_profile
- student_sentiment_profile
- source_profile
- decision_summary
- scoring_inputs

## No Guessing Policy

If the researcher cannot verify a value, they must not guess.

Bad:
`tuition_eur_per_year_estimated: 3000`

Good:
`tuition_eur_per_year_estimated: null`
`source_profile.field_confidence.tuition: "unknown"`
`verification_notes: "Official tuition value for non-EU MSc students could not be verified."`

## Link Validation Policy

Every source URL must be checked.

For each source, record:

- url
- source_type
- title
- access_status
- last_checked
- relevant_fields
- confidence
- notes

Valid `access_status` values:

- `ok`
- `redirects`
- `pdf`
- `requires_js`
- `blocked`
- `broken`
- `not_found`
- `unknown`

Do not use sources with `broken`, `not_found`, or `unknown` access status as primary sources.

## Forum / Sentiment Policy

When using forums:

1. Search multiple independent sources if possible.
2. Separate repeated complaints from isolated anecdotes.
3. Record approximate sample size.
4. Record date range.
5. Do not overfit to one negative or positive comment.
6. Do not use anonymous sentiment to prove official facts.
7. Score sentiment conservatively.
8. Mark confidence low unless many recent, consistent, independent comments exist.

## Student Satisfaction Score

Add a student sentiment score from 0 to 100 when enough sources exist.

Suggested components:

- teaching_quality_sentiment: 20%
- workload_balance_sentiment: 15%
- administration_sentiment: 15%
- housing_sentiment: 15%
- international_student_support_sentiment: 15%
- career_support_sentiment: 10%
- city_life_sentiment: 10%

If sources are weak or insufficient, set:

`student_satisfaction_score: null`
`sentiment_confidence: "low"` or `"unknown"`

Never fabricate a score.

## Canary Tests

Before committing data, run the canary tests in `checklists/canary_tests.md`.

If any canary test fails, do not finalize the record.

## Final Rule

The database must be useful, source-grounded, and honest about uncertainty. Missing data is acceptable. Invented data is not.

## Bilingual Data Rule

Internal keys must be English (e.g. `scientific_ai_computational_digital`), while user-facing text must be bilingual:
```json
{
  "en": "Strong research output in CFD.",
  "tr": "HAD alanında güçlü araştırma çıktısı."
}
```
