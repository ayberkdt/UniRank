function firstValue(...values) {
  for (const value of values) {
    if (value === null || value === undefined) continue;
    if (typeof value === "string" && value.trim() === "") continue;
    if (Array.isArray(value) && value.length === 0) continue;
    return value;
  }
  return null;
}

function getPath(obj, path) {
  return path.split(".").reduce((acc, key) => {
    if (acc == null) return undefined;
    return acc[key];
  }, obj);
}

function localizedField(value) {
  if (window.localizedValue) return window.localizedValue(value);
  if (value == null) return "";
  if (typeof value === "string") return value;
  if (typeof value === "object") return value.en || value.tr || value.name || "";
  return String(value);
}

function valueText(value) {
  if (value == null) return "";
  if (Array.isArray(value)) return value.map(valueText).filter(Boolean).join(", ");
  if (typeof value === "object") {
    const namedValue = firstValue(value.name, value.city, value.label);
    return namedValue != null ? valueText(namedValue) : localizedField(value);
  }
  return String(value).trim();
}

function isUnknownValue(value) {
  if (typeof value !== "string") return false;
  return ["unknown", "needs_verification", "n/a", "na", "—", "-"].includes(value.trim().toLowerCase());
}

function firstKnownValue(...values) {
  for (const value of values) {
    const candidate = firstValue(value);
    if (candidate == null || isUnknownValue(candidate)) continue;
    return candidate;
  }
  return null;
}

function finiteNumber(value) {
  if (value === null || value === undefined || value === "") return null;
  const number = typeof value === "number" ? value : Number(String(value).trim());
  return Number.isFinite(number) ? number : null;
}

function firstFiniteNumber(...values) {
  for (const value of values) {
    const number = finiteNumber(value);
    if (number !== null) return number;
  }
  return null;
}

function foreignAnnualTuition(costProfile) {
  const exactFields = [
    ["tuition_and_program_fees_usd_nonresident", "USD", "academic_year"],
    ["tuition_usd_per_year", "USD", "year"],
    ["tuition_usd_per_year_at_three_quarters", "USD", "year"],
    ["tuition_usd_first_year_example", "USD", "year"],
    ["tuition_gbp_per_year", "GBP", "year"],
    ["tuition_chf_per_year", "CHF", "year"],
    ["tuition_sek_per_year", "SEK", "year"],
    ["tuition_dkk_per_year", "DKK", "year"],
    ["tuition_usd_per_quarter", "USD", "quarter"],
    ["tuition_usd_per_quarter_nonresident_full_time", "USD", "quarter"]
  ];
  for (const [key, currency, period] of exactFields) {
    const amount = finiteNumber(costProfile?.[key]);
    if (amount !== null) {
      return {
        amount,
        currency,
        period,
        academicYear: valueText(costProfile?.academic_year),
        isHistorical: costProfile?.current_for_fall_2027 === false
      };
    }
  }
  for (const currency of ["usd", "gbp", "chf", "sek", "dkk"]) {
    const min = finiteNumber(costProfile?.[`tuition_${currency}_per_year_min`]);
    const max = finiteNumber(costProfile?.[`tuition_${currency}_per_year_max`]);
    if (min !== null || max !== null) {
      return {
        min: min ?? max,
        max: max ?? min,
        currency: currency.toUpperCase(),
        period: "year",
        kind: "published_range",
        academicYear: valueText(costProfile?.academic_year),
        isHistorical: costProfile?.current_for_fall_2027 === false
      };
    }
  }
  return null;
}

function foreignMonthlyRoomRent(livingProfile) {
  for (const currency of ["usd", "gbp", "chf", "sek", "dkk"]) {
    const graduateMin = finiteNumber(livingProfile?.[`graduate_housing_rate_${currency}_per_person_month_min`]);
    const graduateMax = finiteNumber(livingProfile?.[`graduate_housing_rate_${currency}_per_person_month_max`]);
    if (graduateMin !== null || graduateMax !== null) {
      return {
        min: graduateMin ?? graduateMax,
        max: graduateMax ?? graduateMin,
        currency: currency.toUpperCase(),
        kind: "official_graduate_housing_rate",
        academicYear: valueText(livingProfile?.rates_academic_year)
      };
    }
    const min = finiteNumber(livingProfile?.[`average_room_rent_${currency}_per_month_min`]);
    const max = finiteNumber(livingProfile?.[`average_room_rent_${currency}_per_month_max`]);
    const exact = finiteNumber(livingProfile?.[`average_room_rent_${currency}_per_month`]);
    if (min !== null || max !== null || exact !== null) {
      return { min: min ?? exact, max: max ?? exact, currency: currency.toUpperCase(), kind: "room_rent" };
    }
    const housingMin = finiteNumber(livingProfile?.[`monthly_housing_rent_${currency}_per_month_min`]);
    const housingMax = finiteNumber(livingProfile?.[`monthly_housing_rent_${currency}_per_month_max`]);
    const housingExact = finiteNumber(livingProfile?.[`monthly_housing_rent_${currency}_per_month`]);
    if (housingMin !== null || housingMax !== null || housingExact !== null) {
      return { min: housingMin ?? housingExact, max: housingMax ?? housingExact, currency: currency.toUpperCase(), kind: "housing_estimate" };
    }
  }
  return null;
}

function euroMonthlyRoomRent(livingProfile, record) {
  const min = finiteNumber(livingProfile?.average_room_rent_eur_min);
  const max = finiteNumber(livingProfile?.average_room_rent_eur_max);
  const exact = firstFiniteNumber(
    livingProfile?.average_room_rent_eur
  );
  if (min !== null || max !== null || exact !== null) {
    return { min: min ?? exact ?? max, max: max ?? exact ?? min, currency: "EUR", kind: "room_rent" };
  }
  return null;
}

function foreignAnnualLivingBudget(costProfile) {
  for (const currency of ["usd", "gbp", "chf", "sek", "dkk"]) {
    const direct = finiteNumber(costProfile?.[`living_cost_${currency}_per_year_i20`]);
    const generic = finiteNumber(costProfile?.[`living_cost_${currency}_per_year`]);
    const amount = direct ?? generic;
    if (amount !== null) return { min: amount, max: amount, currency: currency.toUpperCase() };
    const min = finiteNumber(costProfile?.[`living_cost_${currency}_per_year_min`]);
    const max = finiteNumber(costProfile?.[`living_cost_${currency}_per_year_max`]);
    if (min !== null || max !== null) return { min: min ?? max, max: max ?? min, currency: currency.toUpperCase() };
  }
  return null;
}

function foreignAnnualHousingBudget(livingProfile) {
  for (const currency of ["usd", "gbp", "chf", "sek", "dkk"]) {
    const amount = finiteNumber(livingProfile?.[`housing_budget_${currency}_per_year`]);
    if (amount !== null) return { min: amount, max: amount, currency: currency.toUpperCase() };
    const min = finiteNumber(livingProfile?.[`housing_budget_${currency}_per_year_min`]);
    const max = finiteNumber(livingProfile?.[`housing_budget_${currency}_per_year_max`]);
    if (min !== null || max !== null) return { min: min ?? max, max: max ?? min, currency: currency.toUpperCase() };
  }
  return null;
}

function foreignCompulsoryFee(costProfile) {
  const exactFields = [
    ["institutional_resilience_enhancement_fee_usd", "USD", "academic_year"],
    ["mandatory_fees_usd_per_year", "USD", "year"],
    ["mandatory_fees_usd_first_year_example", "USD", "year"],
    ["mandatory_fees_gbp_per_year", "GBP", "year"],
    ["mandatory_fees_chf_per_year", "CHF", "year"],
    ["mandatory_fees_sek_per_year", "SEK", "year"],
    ["mandatory_fees_dkk_per_year", "DKK", "year"]
  ];
  for (const [key, currency, period] of exactFields) {
    const amount = finiteNumber(costProfile?.[key]);
    if (amount !== null) {
      return {
        amount,
        currency,
        period,
        academicYear: valueText(costProfile?.academic_year),
        isHistorical: costProfile?.current_for_fall_2027 === false
      };
    }
  }
  return null;
}

function foreignMonthlyLivingBudget(livingProfile) {
  for (const currency of ["usd", "gbp", "chf", "sek", "dkk"]) {
    const min = finiteNumber(livingProfile?.[`monthly_living_cost_${currency}_per_month_min`]);
    const max = finiteNumber(livingProfile?.[`monthly_living_cost_${currency}_per_month_max`]);
    const estimated = finiteNumber(livingProfile?.[`monthly_living_cost_${currency}_per_month_estimated`]);
    if (min !== null || max !== null || estimated !== null) {
      return { min: min ?? max ?? estimated, max: max ?? min ?? estimated, currency: currency.toUpperCase() };
    }
  }
  const structured = livingProfile?.monthly_living_cost;
  if (structured && typeof structured === "object") {
    const currency = String(structured.currency || "").toUpperCase();
    const min = finiteNumber(structured.min);
    const max = finiteNumber(structured.max);
    const estimated = finiteNumber(structured.estimated);
    if (currency && (min !== null || max !== null || estimated !== null)) {
      return { min: min ?? max ?? estimated, max: max ?? min ?? estimated, currency };
    }
  }
  return null;
}

function foreignMonthlyBudgetExamples(livingProfile) {
  for (const currency of ["usd", "gbp", "chf", "sek", "dkk"]) {
    const examples = livingProfile?.[`official_student_total_budget_${currency}_per_month_examples`];
    if (Array.isArray(examples)) {
      const values = examples.map(finiteNumber).filter((value) => value !== null);
      if (values.length) return { values, currency: currency.toUpperCase() };
    }
  }
  return null;
}

function stringList(value) {
  const values = Array.isArray(value) ? value : (value == null || value === "" ? [] : [value]);
  return values.map(valueText).filter(Boolean);
}

function firstObjectNumber(values, key = "amount") {
  if (!Array.isArray(values)) return null;
  for (const entry of values) {
    if (!entry || typeof entry !== "object") continue;
    const number = finiteNumber(entry[key]);
    if (number !== null) return number;
  }
  return null;
}

function legacyAnnualTuition(values) {
  if (!Array.isArray(values)) return null;
  for (const entry of values) {
    if (!entry || typeof entry !== "object") continue;
    const amount = finiteNumber(entry.amount);
    if (amount === null) continue;

    const period = String(entry.period || "").trim().toLowerCase();
    if (["year", "annual", "annually", "yr"].includes(period)) return amount;
    if (["semester", "term"].includes(period)) return amount * 2;
  }
  return null;
}

function normalizeDuration(record) {
  const direct = firstKnownValue(record.duration, record.program_duration, record.Program_Duration);
  if (direct !== null) return valueText(direct);

  const years = firstFiniteNumber(record.duration_years, record.durationYears);
  if (years !== null) return `${years} ${years === 1 ? "year" : "years"}`;

  const semesters = firstFiniteNumber(record.duration_semesters, record.durationSemesters);
  if (semesters !== null) return `${semesters} ${semesters === 1 ? "semester" : "semesters"}`;
  return null;
}

function normalizeDeadline(record, timelineProfile) {
  return firstKnownValue(
    timelineProfile.non_eu_deadline,
    timelineProfile.deadline_non_eu,
    timelineProfile.winter_deadline,
    timelineProfile.application_deadline,
    record.non_eu_deadline,
    record.deadline,
    record.deadline_winter_closes,
    record.Deadline_Winter_Close,
    record.deadline_summer_closes,
    record.Deadline_Summer_Close,
    timelineProfile.deadline_notes,
    record.deadlines_note,
    record.Deadline_General_Note
  );
}

function normalizeEligibleForNonEu(record, eligibilityProfile) {
  if (eligibilityProfile && Object.prototype.hasOwnProperty.call(eligibilityProfile, "eligible_for_non_eu")) {
    const value = eligibilityProfile.eligible_for_non_eu;
    return typeof value === "boolean" ? value : null;
  }

  for (const value of [record.eligibleForNonEu, record.eligible_for_non_eu]) {
    if (typeof value === "boolean") return value;
  }

  const flags = record.scoring_inputs?.hard_filter_flags || record._scoring_inputs?.hard_filter_flags || {};
  if (typeof flags.non_eu_eligible === "boolean") return flags.non_eu_eligible;

  const scope = firstValue(record.Program_Scope, record.scope);
  if (scope == null) return null;
  const normalizedScope = String(scope).trim().toLowerCase().replace(/[\s-]+/g, "_");
  if (["non_eu", "noneu"].includes(normalizedScope)) return true;
  if (["unknown", "needs_verification", "n/a", "na"].includes(normalizedScope)) return null;
  if (normalizedScope.includes("bilinmiyor") || normalizedScope.includes("resmi_veri_yok")) return null;
  return false;
}

function summarizeConfidence(fieldConfidence) {
  if (!fieldConfidence || typeof fieldConfidence !== "object" || Array.isArray(fieldConfidence)) return "unknown";

  const rank = { unknown: 0, low: 1, medium: 2, high: 3 };
  const levels = Object.entries(fieldConfidence)
    // Student sentiment is intentionally a separate perception signal. A
    // low-confidence forum sample must not downgrade verified official facts.
    .filter(([key]) => !["student_sentiment", "sentiment"].includes(key))
    .map(([, value]) => value)
    .map(value => String(value || "").trim().toLowerCase())
    .map(value => Object.prototype.hasOwnProperty.call(rank, value) ? value : "unknown");

  if (levels.length === 0) return "unknown";
  // This summary is only computed for records whose critical fields are all
  // verified. A single optional field without a source ("unknown") must not
  // drag the whole record's badge down to "unknown confidence"; the weakest
  // *known* level is the honest summary. All-unknown still reports unknown.
  const knownLevels = levels.filter(level => level !== "unknown");
  if (knownLevels.length === 0) return "unknown";
  return knownLevels.reduce((lowest, level) => rank[level] < rank[lowest] ? level : lowest, "high");
}

function getCategoryProfile(record) {
  const profile = record.category_profile || record.Category_Profile || {};
  return {
    primary_categories: Array.isArray(profile.primary_categories) ? profile.primary_categories : [],
    secondary_categories: Array.isArray(profile.secondary_categories) ? profile.secondary_categories : [],
    subcategories: Array.isArray(profile.subcategories) ? profile.subcategories : [],
    normalized_tags: Array.isArray(profile.normalized_tags) ? profile.normalized_tags : [],
    category_scores: profile.category_scores && typeof profile.category_scores === "object" ? profile.category_scores : {}
  };
}

function normalizeLocation(record) {
  const rawLocation = firstValue(record.location, record.Location, record.coordinates, record.Coordinates);
  const source = rawLocation && typeof rawLocation === "object" && !Array.isArray(rawLocation) ? rawLocation : {};
  const coordinatePair = Array.isArray(rawLocation)
    ? rawLocation
    : (Array.isArray(source.coordinates) ? source.coordinates : null);

  let latitude = firstFiniteNumber(source.latitude, source.lat, record.latitude, record.lat);
  let longitude = firstFiniteNumber(source.longitude, source.lng, source.lon, record.longitude, record.lng, record.lon);

  if ((latitude === null || longitude === null) && coordinatePair && coordinatePair.length >= 2) {
    const first = finiteNumber(coordinatePair[0]);
    const second = finiteNumber(coordinatePair[1]);
    longitude = longitude === null ? first : longitude;
    latitude = latitude === null ? second : latitude;
  }

  if (
    latitude === null || longitude === null ||
    latitude < -90 || latitude > 90 || longitude < -180 || longitude > 180
  ) {
    return null;
  }

  return {
    ...source,
    city: valueText(firstValue(source.city, source.City, record.city, record.City)),
    country: valueText(firstValue(source.country, source.Country, record.country, record.Country)),
    latitude,
    longitude
  };
}

function normalizeSources(value) {
  if (Array.isArray(value)) return value.filter(Boolean);
  if (typeof value === "string" && value.trim()) return [{ url: value }];
  if (value && typeof value === "object") return [value];
  return [];
}

function normalizeUniversityRecord(record) {
  if (!record) return {};

  const eligibilityProfile = record.eligibility_profile || {};
  const sourceProfile = record.source_profile || {};
  const rankingProfile = record.ranking_profile || {};
  const qsProfile = rankingProfile.qs_world_university_rankings || {};
  const costProfile = record.cost_profile || {};
  const languageProfile = record.language_profile || {};
  const livingProfile = record.living_profile || {};
  const scholarshipProfile = record.scholarship_profile || {};
  const researchProfile = record.research_profile || {};
  const industryProfile = record.industry_ecosystem_profile || {};
  const curriculumProfile = record.curriculum_profile || {};
  const timelineProfile = record.application_timeline_profile || {};
  const sentimentProfile = record.student_sentiment_profile || {};
  const dataQuality = record.data_quality || {};
  const financials = record.financials || {};
  const urls = record.urls || {};
  const categoryProfile = getCategoryProfile(record);
  const hasStructuredCostProfile = Boolean(
    record.cost_profile && typeof record.cost_profile === "object" && !Array.isArray(record.cost_profile)
  );

  const id = valueText(firstValue(record.Uni_ID, record.id, record.name, record.university));
  const universityName = firstValue(
    record.university,
    record.University_Display_Name,
    record.University_Name,
    record.University,
    record.display_name,
    record.name
  ) || "";
  const universityAliases = Array.from(new Set([
    ...stringList(record.institution_profile?.alternate_names),
    ...stringList(record.institution_profile?.aliases),
    ...stringList(record.institution_profile?.short_name),
    ...stringList(record.university_aliases),
    ...stringList(record.alternate_names),
    ...stringList(record.short_name),
    ...stringList(record.short),
    ...stringList(record.University_Short_Name)
  ]));
  const programName = firstValue(record.program_name, record.Program_Name, record.target_program_name, record.Target_Program_Name) || "";
  const city = valueText(firstValue(record.city, record.City));
  const country = valueText(firstValue(record.country, record.Country));
  const degree = firstValue(record.program_degree, record.Program_Degree, record.target_program_degree, record.degree_level, record.degree_class) || "";
  const degreeLevel = firstValue(record.degree_level, record.degree_class) || "";
  const ects = firstFiniteNumber(record.ects, record.Program_ECTS, record.target_program_ects);
  const duration = normalizeDuration(record);
  const teachingLanguage = stringList(firstKnownValue(
    record.teaching_languages,
    record.teaching_language,
    languageProfile.teaching_languages,
    languageProfile.teaching_language,
    record.Admission_Language_Req,
    record.admission_language_req,
    record.language_req,
    record.admission?.requirements?.language_requirements
  ));
  const legacyTuitionPerYear = hasStructuredCostProfile ? null : legacyAnnualTuition(record.Cost_Tuition);
  const legacySemesterFee = hasStructuredCostProfile ? null : firstObjectNumber(record.Cost_Semester_Fees);
  const explicitNonEuEuroTuition = firstFiniteNumber(
    costProfile.tuition_eur_per_year_non_eu_nonresident,
    Number(costProfile.non_eu_flat_fee) > 0 ? costProfile.non_eu_flat_fee : null
  );
  const tuitionPerYear = firstFiniteNumber(
    explicitNonEuEuroTuition,
    costProfile.tuition_eur_per_year_estimated,
    costProfile.tuition_eur_per_year_min,
    record.tuition_eur_per_year,
    record.Tuition_EUR_Per_Year,
    hasStructuredCostProfile ? null : financials.tuition_fee_per_year,
    legacyTuitionPerYear
  );
  const exactSemesterFee = firstFiniteNumber(
    costProfile.regional_tax_eur,
    costProfile.student_contribution_eur,
    costProfile.enrollment_fee_eur,
    record.semester_fee_eur,
    hasStructuredCostProfile ? null : financials.semester_fee,
    legacySemesterFee
  );
  const feeScope = finiteNumber(costProfile.enrollment_fee_eur) !== null
    && finiteNumber(costProfile.regional_tax_eur) === null
    && finiteNumber(costProfile.student_contribution_eur) === null
      ? "enrollment"
      : "term_or_published_period";
  // Some universities publish an explicitly approximate planning contribution
  // rather than an invoice. Keep that useful figure visible, but expose its
  // status so cards never make it look exact.
  const approximateSemesterFee = firstFiniteNumber(costProfile.student_contribution_eur_approximate);
  const semesterFee = exactSemesterFee ?? approximateSemesterFee;
  const semesterFeeApproximate = exactSemesterFee === null && approximateSemesterFee !== null;
  const legacyAcademicCost = legacyTuitionPerYear !== null
    ? legacyTuitionPerYear + ((legacySemesterFee || 0) * 2)
    : null;
  const totalAcademicCost = firstFiniteNumber(
    costProfile.total_academic_cost_eur_per_year_estimated,
    legacyAcademicCost,
    tuitionPerYear,
    hasStructuredCostProfile ? null : record.annual_fee_eur
  );
  const publishedForeignTuition = foreignAnnualTuition(costProfile);
  const publishedEuroRoomRent = euroMonthlyRoomRent(livingProfile, record);
  const publishedForeignRoomRent = foreignMonthlyRoomRent(livingProfile);
  const publishedForeignAnnualLivingBudget = foreignAnnualLivingBudget(costProfile);
  const publishedForeignAnnualHousingBudget = foreignAnnualHousingBudget(livingProfile);
  const publishedForeignCompulsoryFee = foreignCompulsoryFee(costProfile);
  const publishedForeignMonthlyLivingBudget = foreignMonthlyLivingBudget(livingProfile);
  const publishedForeignMonthlyBudgetExamples = foreignMonthlyBudgetExamples(livingProfile);
  const sources = normalizeSources(firstValue(
    sourceProfile.source_log,
    sourceProfile.official_program_page,
    record.Meta_Sources,
    record.sources
  ));
  const needsVerification = Boolean(firstValue(
    dataQuality.status && dataQuality.status !== "verified",
    sourceProfile.needs_verification,
    record.needs_verification,
    record.Meta_Needs_Verification,
    false
  ));
  const fieldConfidence = sourceProfile.field_confidence || record.field_confidence || {};
  const qualityStatus = ["verified", "partial", "needs_verification"].includes(String(dataQuality.status || ""))
    ? dataQuality.status
    : (needsVerification ? "needs_verification" : "partial");
  const confidenceSummary = qualityStatus === "verified"
    ? summarizeConfidence(fieldConfidence)
    : qualityStatus === "partial" ? "medium" : "unknown";
  const eligibleForNonEu = normalizeEligibleForNonEu(record, eligibilityProfile);
  const deadline = normalizeDeadline(record, timelineProfile);

  return {
    id,
    universityName,
    universityAliases,
    programName,
    city,
    country,
    degree,
    degreeLevel,
    ects,
    duration,
    teachingLanguage,
    programUrl: firstValue(record.program_url, record.Program_URL, record.target_program_url, urls.program, record.url) || "",
    tuitionPerYear,
    tuitionScope: explicitNonEuEuroTuition !== null ? "non_eu_target" : "general_or_lowest_published",
    semesterFee,
    feeScope,
    semesterFeeApproximate,
    totalAcademicCost,
    foreignTuition: publishedForeignTuition,
    hasKnownTuition: tuitionPerYear !== null || totalAcademicCost !== null || publishedForeignTuition !== null,
    admissionMode: firstKnownValue(eligibilityProfile.admission_mode, record.Admission_Mode, record.admission_mode, record.admission?.mode) || "unknown",
    admissionRisk: firstKnownValue(eligibilityProfile.admission_risk, record.admission_risk, record.admission?.risk) || "unknown",
    deadline,
    eligibleForNonEu,
    languageRisk: firstKnownValue(languageProfile.language_risk, record.language_risk) || "unknown",
    housingDifficulty: firstKnownValue(
      livingProfile.housing_difficulty,
      livingProfile.housing_search_difficulty,
      livingProfile.living_risk,
      record.living_risk
    ) || "unknown",
    livingRisk: firstKnownValue(livingProfile.living_risk, record.living_risk, record.Cost_City_Living) || "unknown",
    cityCostLevel: firstKnownValue(livingProfile.cost_city_living, livingProfile.city_cost_level, record.cost_city_raw, record.Cost_City_Living) || "unknown",
    scholarshipSummary: firstValue(
      scholarshipProfile.funding_notes,
      scholarshipProfile.scholarship_names,
      scholarshipProfile.regional_scholarship_name,
      record.scholarship_names,
      Array.isArray(record.Scholarships_Info) ? stringList(record.Scholarships_Info).join(", ") : record.Scholarships_Info
    ) || "",
    researchSummary: firstValue(
      researchProfile.research_strength_summary,
      researchProfile.research_access_note,
      researchProfile.verification_notes,
      record.strong_areas_summary,
      record.Analysis_Strong_Areas,
      record.research_strength,
      record.field_recognition
    ) || "",
    industrySummary: firstValue(
      industryProfile.ecosystem_notes,
      industryProfile.verification_notes,
      record.aerospace_ecosystem,
      record.Industry_Ecosystem,
      record.industry_ecosystem
    ) || "",
    decisionSummary: record.decision_summary || {},
    mainStrengths: stringList(firstValue(record.decision_summary?.main_strengths, record.Analysis_Pros, record.pros)),
    mainRisks: stringList(firstValue(record.decision_summary?.main_risks, record.Analysis_Cons, record.cons)),
    bestFor: stringList(record.decision_summary?.best_for),
    notIdealFor: stringList(record.decision_summary?.not_ideal_for),
    sources,
    fieldConfidence,
    confidenceSummary,
    needsVerification,
    lastVerified: sourceProfile.last_verified || record.updated_at || record.Meta_Updated_At || "",
    dataQuality: {
      status: qualityStatus,
      checkedOfficialSourceCount: firstFiniteNumber(dataQuality.checked_official_source_count) || 0,
      verifiedFields: Array.isArray(dataQuality.verified_fields) ? dataQuality.verified_fields : [],
      unverifiedCriticalFields: Array.isArray(dataQuality.unverified_critical_fields) ? dataQuality.unverified_critical_fields : [],
      auditedAt: dataQuality.audited_at || ""
    },
    categoryProfile,
    location: normalizeLocation(record),
    qsRanking: firstFiniteNumber(record.qs_ranking, qsProfile.rank),
    qsRankDisplay: firstValue(record.qs_ranking_display, qsProfile.display_rank, record.qs_ranking),
    qsRankYear: firstFiniteNumber(record.qs_ranking_year, qsProfile.edition),
    qsRankSource: firstValue(qsProfile.source_url),
    engineeringRanking: firstValue(record.engineering_ranking, record.field_recognition) || null,
    labs: Array.isArray(researchProfile.labs)
      ? researchProfile.labs
      : (Array.isArray(researchProfile.key_institutes) ? researchProfile.key_institutes : []),
    professors: Array.isArray(researchProfile.notable_professors) ? researchProfile.notable_professors : [],
    strongAreas: categoryProfile.normalized_tags.length
      ? categoryProfile.normalized_tags
      : stringList(firstValue(researchProfile.research_focus_areas, record.Analysis_Tags, record.tags)),
    confirmedPartners: Array.isArray(industryProfile.confirmed_partners)
      ? industryProfile.confirmed_partners
      : (Array.isArray(industryProfile.verified_partnerships)
        ? industryProfile.verified_partnerships
        : (Array.isArray(record.Industry_Partners) ? record.Industry_Partners : [])),
    internshipMandatory: firstValue(curriculumProfile.internship_required, record.internship_mandatory, record.Internship_Mandatory),
    averageRoomRent: firstFiniteNumber(livingProfile.average_room_rent_eur),
    euroRoomRent: publishedEuroRoomRent,
    foreignRoomRent: publishedForeignRoomRent,
    monthlyLivingCost: firstFiniteNumber(livingProfile.monthly_living_cost_eur_estimated, livingProfile.living_cost_eur_per_month),
    monthlyLivingCostMin: firstFiniteNumber(livingProfile.monthly_living_cost_eur_min),
    monthlyLivingCostMax: firstFiniteNumber(livingProfile.monthly_living_cost_eur_max),
    monthlyLivingCostBasis: firstValue(livingProfile.monthly_living_cost_basis, livingProfile.living_cost_notes),
    foreignAnnualLivingBudget: publishedForeignAnnualLivingBudget,
    foreignAnnualHousingBudget: publishedForeignAnnualHousingBudget,
    foreignCompulsoryFee: publishedForeignCompulsoryFee,
    foreignMonthlyLivingBudget: publishedForeignMonthlyLivingBudget,
    foreignMonthlyBudgetExamples: publishedForeignMonthlyBudgetExamples,
    housingCost: firstFiniteNumber(livingProfile.average_room_rent_eur, livingProfile.monthly_living_cost_eur_estimated, livingProfile.living_cost_eur_per_month),
    scholarshipDetails: scholarshipProfile,
    costDetails: costProfile,
    livingDetails: livingProfile,
    eligibilityDetails: eligibilityProfile,
    languageDetails: languageProfile,
    curriculumDetails: curriculumProfile,
    timelineDetails: timelineProfile,
    admissionUrl: firstValue(sourceProfile.official_admission_page, urls.admission, record.admission_url) || "",
    tuitionUrl: firstValue(sourceProfile.official_tuition_page, urls.tuition, record.tuition_url) || "",
    scholarshipUrl: firstValue(sourceProfile.official_scholarship_page, scholarshipProfile.scholarship_application_url, record.scholarship_url) || "",
    studentSentiment: sentimentProfile,
    studentReviews: Array.isArray(sentimentProfile.student_sentiment_sources) ? sentimentProfile.student_sentiment_sources : [],
    raw: record
  };
}

window.uniDataAdapter = {
  firstValue,
  getPath,
  localizedField,
  getCategoryProfile,
  normalizeLocation,
  normalizeUniversityRecord
};
