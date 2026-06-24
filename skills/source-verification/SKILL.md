---
name: source-verification
description: Ensure that all database values are backed by accessible, relevant, and correctly classified sources.
---
# Skill: Source Verification

Use this skill whenever adding or updating sources in UniRank.

## Goal

Ensure that all database values are backed by accessible, relevant, and correctly classified sources.

## Source Types

Use the following source types:

- `official_program_page`
- `official_admission_page`
- `official_curriculum_page`
- `official_tuition_page`
- `official_scholarship_page`
- `official_department_page`
- `official_lab_page`
- `official_housing_page`
- `official_visa_or_government_page`
- `official_industry_partner_page`
- `third_party_database`
- `student_forum`
- `student_review`
- `news_article`
- `other`

## Access Status

Each source must have an access status:

- `ok`
- `redirects`
- `pdf`
- `requires_js`
- `blocked`
- `broken`
- `not_found`
- `unknown`

Sources with `broken`, `not_found`, or `unknown` cannot support critical fields.

## Source Log Format

For every source, record:

```json
{
  "url": "",
  "title": "",
  "source_type": "",
  "access_status": "",
  "last_checked": "",
  "relevant_fields": [],
  "confidence": "",
  "notes": ""
}
```

## Verification Rules

1. Open every URL before using it.
2. Confirm the page actually supports the field being filled.
3. Do not cite a general university homepage for a specific tuition value.
4. Do not cite a program page for scholarship unless scholarship is actually described there.
5. Do not cite a study portal page if the official program page is available.
6. Do not use old academic-year pages without marking date risk.
7. If the source is a PDF, record it as `pdf`.
8. If the source requires JavaScript and content cannot be verified, mark `requires_js`.
9. If access is blocked, do not treat it as verified.
10. If a page redirects, confirm the final page is still relevant.

## Critical Field Source Requirement

Critical fields require official sources:

* program status
* degree level
* language
* admission requirements
* tuition
* scholarships
* deadlines
* curriculum
* official partnerships
* visa/pre-enrolment rules

## Confidence Assignment

* `high`: official, current, direct.
* `medium`: official but indirect, ambiguous, or not fully detailed.
* `low`: third-party, forum, old, or weakly related.
* `unknown`: not verified.

## Broken Link Handling

If a link fails:

1. Do not delete the information immediately.
2. Mark the source `broken`.
3. Mark affected fields `needs_verification`.
4. Search for a replacement official source.
5. Add note: `Previous source no longer accessible as of YYYY-MM-DD`.
