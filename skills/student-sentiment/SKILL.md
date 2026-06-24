---
name: student-sentiment
description: Standardize collection of informal student experience, satisfaction, workload, housing, administration, and city-life information.
---
# Skill: Student Sentiment Research

Use this skill when collecting informal student experience, satisfaction, workload, housing, administration, and city-life information.

## Important Rule

Student sentiment is not official fact. It is a perception signal.

Never use student forums to verify:

- tuition
- admission requirements
- official language requirements
- official deadlines
- program status
- degree recognition
- scholarship eligibility
- visa rules

## Allowed Uses

Student forums and reviews may be used for:

- student satisfaction
- teaching quality perception
- workload perception
- administration experience
- housing difficulty
- city life
- international student support
- social integration
- internship/career support perception
- complaints and recurring issues
- positive recurring experiences

## Suggested Sources

Search multiple independent sources when possible:

- Reddit
- The Student Room
- GradCafe
- Studyportals reviews
- Mastersportal reviews
- Google reviews
- Facebook groups
- Discord community mirrors, if accessible
- university subreddit
- Erasmus forums
- international student blogs
- YouTube comments only as very weak anecdotal signal

## Sentiment Collection Rules

1. Collect recent comments first.
2. Prefer comments from the last 3–5 years.
3. Record date range.
4. Record approximate number of comments reviewed.
5. Separate program-specific sentiment from university-wide sentiment.
6. Separate city/housing sentiment from academic sentiment.
7. Do not overreact to isolated comments.
8. Look for repeated patterns.
9. Record both positive and negative themes.
10. Mark confidence low if sample size is small.

## Student Sentiment Profile

Add this object to each program:

```json
"student_sentiment_profile": {
  "student_satisfaction_score": null,
  "sentiment_confidence": "unknown",
  "sample_size_estimate": null,
  "date_range": "",
  "teaching_quality_sentiment": "",
  "workload_sentiment": "",
  "administration_sentiment": "",
  "housing_sentiment": "",
  "city_life_sentiment": "",
  "international_student_support_sentiment": "",
  "career_support_sentiment": "",
  "positive_themes": [],
  "negative_themes": [],
  "recurring_complaints": [],
  "recurring_strengths": [],
  "sentiment_summary": "",
  "student_sentiment_sources": []
}
```

## Student Satisfaction Score

Only assign a score if there is enough evidence.

Suggested scoring:

* teaching quality: 20%
* workload balance: 15%
* administration: 15%
* housing: 15%
* international student support: 15%
* career support: 10%
* city life: 10%

Score range: 0–100.

If the evidence is weak, do not assign a score.

Use:

```json
"student_satisfaction_score": null,
"sentiment_confidence": "low"
```

## Sentiment Confidence

* `high`: many recent, independent, consistent sources.
* `medium`: several sources with recurring themes.
* `low`: few sources, mixed relevance, or anecdotal.
* `unknown`: insufficient sources.

## Reporting Format

When reporting sentiment, use cautious language:

Good:
“Several recent student comments mention difficulty finding housing in Milan. This is treated as a low-confidence but recurring sentiment signal.”

Bad:
“Students hate housing in Milan.”

Good:
“Teaching quality sentiment appears mixed based on a small number of reviews.”

Bad:
“The teaching quality is bad.”
