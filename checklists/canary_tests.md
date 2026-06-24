# Canary Tests for UniRank Research

Run these before finalizing any program record.

If any test fails, stop and revise the record.

## Hallucination / Guessing Tests

- [ ] No tuition value exists without source.
- [ ] No deadline exists without source.
- [ ] No language claim exists without source.
- [ ] No admission requirement exists without source.
- [ ] No scholarship eligibility claim exists without source.
- [ ] No non-EU eligibility claim exists without source.
- [ ] No numeric value is guessed.
- [ ] Unknown values are marked as `unknown` or `null`.

## Source Tests

- [ ] All URLs were opened or checked.
- [ ] Broken URLs are not used as valid sources.
- [ ] Redirecting URLs were checked after redirect.
- [ ] PDF sources are marked as PDF.
- [ ] Third-party sources do not override official sources.
- [ ] Student forum sources are only used for sentiment.

## Program Relevance Tests

- [ ] Program relevance is supported by curriculum, track, lab, or official program description.
- [ ] Program is not added only because the university is prestigious.
- [ ] QS ranking is not used as technical field evidence.
- [ ] Generic words did not create category tags.
- [ ] Multiple programs are not merged.

## Language Tests

- [ ] Teaching language is verified from official source.
- [ ] Website language is not treated as teaching language.
- [ ] Mixed-language risks are documented.
- [ ] Local language requirement is checked.

## Cost / Funding Tests

- [ ] Tuition basis is clear.
- [ ] Academic year is recorded.
- [ ] Additional fees are checked.
- [ ] Scholarship deadline is checked.
- [ ] Scholarship eligibility for non-EU students is checked.
- [ ] Housing/meal/cash support claims are sourced.

## Sentiment Tests

- [ ] Student sentiment sample size is recorded.
- [ ] Sentiment date range is recorded.
- [ ] Isolated anecdotes are not overgeneralized.
- [ ] Satisfaction score is null if evidence is insufficient.
- [ ] Sentiment confidence is not higher than evidence allows.

## Final Recommendation Tests

- [ ] Decision summary includes strengths.
- [ ] Decision summary includes risks.
- [ ] Application reality is honest.
- [ ] Missing verification tasks are listed.
- [ ] QC status is `passed` only if major checks are satisfied.
