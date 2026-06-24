---
name: university-research
description: Use this skill whenever researching universities, degree programs, admission requirements, tuition, scholarships, curriculum, research strength, industry ecosystem, or student experience for UniRank.
---
# Skill: University Research

Use this skill whenever researching universities, degree programs, admission requirements, tuition, scholarships, curriculum, research strength, industry ecosystem, or student experience for UniRank.

## Goal

Produce source-grounded, decision-support-ready university-program records.

## Required Inputs

- Country
- Target degree level: BSc, MSc, PhD, or any
- Target fields: aerospace, aeronautical, astronautical, space engineering, GNC, CFD, propulsion, structures, spacecraft systems, satellite systems, etc.
- Student profile assumptions if provided:
  - nationality
  - EU/non-EU status
  - language abilities
  - budget
  - preferred fields
  - preferred countries
  - degree background

## Research Sequence

For each university:

1. Find official university website.
2. Find official program page.
3. Confirm program is active.
4. Confirm program degree level.
5. Confirm duration and ECTS.
6. Confirm teaching language.
7. Confirm admission requirements.
8. Confirm non-EU eligibility.
9. Confirm tuition and additional fees.
10. Confirm scholarship/funding.
11. Confirm application deadlines.
12. Confirm curriculum, tracks, and courses.
13. Confirm labs, research groups, and departments.
14. Confirm industry partnerships only if official evidence exists.
15. Collect student sentiment separately.
16. Normalize categories using taxonomy.
17. Create source log.
18. Assign field-level confidence.
19. Create JSON record.
20. Run quality-control checklist.

## Mandatory Source Rules

- Use official sources for facts.
- Use student forums only for sentiment.
- Do not use marketing language as factual evidence.
- Do not infer teaching language from page language.
- Do not infer admission eligibility from program availability.
- Do not infer industry partnership from geographic proximity.
- Do not infer curriculum strength from program title.

## Required Official Sources

At minimum, try to find:

- official program page
- official admission page
- official curriculum/study plan
- official tuition/fees page
- official scholarship page
- official department or lab page

If one of these cannot be found, mark relevant confidence as `unknown` or `low`.

## Candidate Program Decision

Add a program if:

- The program directly targets aerospace, aeronautics, astronautics, space, satellite, aircraft, spacecraft, or related systems.

OR

- A general engineering program has clear aerospace/space specialization, track, lab, thesis route, or curriculum evidence.

Do not add a program only because the university is famous.

## Output Requirements

For each program, produce:

1. Human-readable summary.
2. JSON object.
3. Source log.
4. Confidence table.
5. Main risks.
6. Missing information list.
7. Follow-up questions for future verification.

## Refusal to Guess

If data cannot be verified:

- Use `null`, `unknown`, `[]`, or `needs_verification`.
- Add a verification note.
- Do not fill with plausible values.
