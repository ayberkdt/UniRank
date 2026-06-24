---
name: quality-control
description: Prevent hallucinated, stale, inconsistent, or misleading university records from entering the database. Use before committing.
---
# Skill: Quality Control

Use this skill before committing any university research data.

## Goal

Prevent hallucinated, stale, inconsistent, or misleading university records from entering the database.

## Required Checks

Before finalizing a record, check:

1. Is the program official and active?
2. Is the degree level verified?
3. Is the teaching language verified?
4. Is non-EU eligibility checked?
5. Are tuition and fees sourced?
6. Are scholarship claims sourced?
7. Are deadlines sourced?
8. Is curriculum/course evidence available?
9. Are category assignments evidence-based?
10. Are research/lab claims sourced?
11. Are industry partnership claims sourced?
12. Is student sentiment separated from official facts?
13. Are all links checked?
14. Are broken links marked?
15. Are confidence levels assigned?
16. Are missing fields marked honestly?
17. Does JSON validate?
18. Does the record avoid marketing language?
19. Does the decision summary mention risks?
20. Are canary tests passed?

## Canary Tests

If any answer is yes, stop and fix the record:

1. Is there a tuition number without an official tuition source?
2. Is there a deadline without an official deadline source?
3. Is there a language claim without official evidence?
4. Is there a scholarship claim without eligibility confirmation?
5. Is a forum source used as proof of an official fact?
6. Is a company listed as partner only because it is nearby?
7. Is a program called strong only because of university reputation?
8. Is QS ranking used as evidence of field strength?
9. Is a program added without checking curriculum?
10. Is a link broken but still used as a source?
11. Is a non-EU eligibility claim inferred instead of verified?
12. Is housing difficulty stated as fact from one anecdotal post?
13. Is a student satisfaction score assigned from fewer than 3 weak sources?
14. Is there a field marked high confidence without official evidence?
15. Is a program language inferred from the language of the website page?
16. Is an old page used without date warning?
17. Are multiple programs merged into one record?
18. Are unknown values filled with plausible guesses?
19. Are category tags created from generic words like engineering/research/science?
20. Is the final recommendation missing major risks?

## Pass / Fail Output

Every finalized record must include a QC result:

```json
"quality_control": {
  "qc_status": "passed",
  "checked_at": "",
  "failed_canary_tests": [],
  "remaining_verification_tasks": [],
  "qc_notes": ""
}
```

If any major issue remains:

```json
"qc_status": "needs_revision"
```
