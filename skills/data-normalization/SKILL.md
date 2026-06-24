---
name: data-normalization
description: Keep all university records consistent, searchable, comparable, and compatible with scoring/filtering systems.
---
# Skill: Data Normalization

Use this skill when converting researched university information into UniRank JSON records.

## Goal

Keep all university records consistent, searchable, comparable, and compatible with scoring/filtering systems.

## General Rules

1. Use consistent field names.
2. Do not create random one-off fields unless necessary.
3. Use arrays for multi-value fields.
4. Use `null` for unknown numeric values.
5. Use `unknown` for unknown categorical values.
6. Use `[]` for unknown or empty lists.
7. Use ISO date format where possible: `YYYY-MM-DD`.
8. Use EUR for European cost fields unless otherwise required.
9. Do not mix display text and normalized values.
10. Keep raw source notes separate from normalized fields.

## Country Names

Use stable English country names:

- Italy
- Germany
- Netherlands
- France
- Sweden
- Switzerland
- Denmark
- Belgium
- Portugal
- Spain
- United Kingdom
- United States
- Japan
- South Korea
- China

Also support aliases in filtering:

- USA → United States
- US → United States
- UK → United Kingdom
- Türkiye → Turkey
- Korea → South Korea

## Language Values

Use arrays:

```json
"teaching_language": ["English"]
```

Allowed common values:

* English
* Italian
* German
* French
* Dutch
* Spanish
* Portuguese
* Swedish
* Danish
* Japanese
* Korean
* Chinese
* Mixed
* Unknown

## Risk Values

Allowed risk levels:

* low
* medium
* high
* unknown

Use these for:

* admission_risk
* language_risk
* living_risk
* timeline_risk
* data_risk

## Confidence Values

Allowed values:

* high
* medium
* low
* unknown

## Relevance Values

Allowed values:

* strong
* medium
* weak
* needs_review

## Program Status Values

Allowed values:

* active
* inactive
* unclear
* needs_verification

## Category Normalization

Use the approved taxonomy:

1. Akışkanlar Mekaniği ve Aerodinamik
2. Uçuş Mekaniği, Kontrol ve Otonomi
3. Uzay Sistemleri ve Astronotik
4. İtki, Enerji ve Termal Sistemler
5. Yapılar, Malzemeler ve Mekanik Tasarım
6. Sistem Mühendisliği, Tasarım ve Optimizasyon
7. Aviyonik, Yazılım ve Sayısal Teknolojiler
8. Üretim, Test ve Endüstriyel Uygulamalar

Do not create new top-level categories without explicit approval.

## Normalized Tags

Use snake_case:

Good:

* `orbital_mechanics`
* `spacecraft_gnc`
* `computational_fluid_dynamics`
* `aerospace_structures`

Bad:

* `Orbit Mechanics`
* `GNC stuff`
* `space things`

## Missing Data

Do not fill missing data with guesses.

Examples:

```json
"tuition_eur_per_year_estimated": null,
"language_risk": "unknown",
"verification_notes": "Official teaching language could not be verified."
```

## Source Mapping

Every major profile must map to source evidence:

* basic info → official program page
* language → official program/admission page
* tuition → official tuition page
* scholarship → official scholarship page
* curriculum → official curriculum page
* research → official department/lab page
* industry → official partnership/company/source
* sentiment → forum/review sources

## Output Validation

Before saving JSON:

1. Validate JSON syntax.
2. Check required fields.
3. Check source profile exists.
4. Check confidence values.
5. Check no invented numeric values.
6. Check no raw unsupported claims.
