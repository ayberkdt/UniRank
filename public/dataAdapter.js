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

function stringList(value) {
  const values = Array.isArray(value) ? value : (value == null || value === "" ? [] : [value]);
  return values.map(valueText).filter(Boolean);
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

  const sourceProfile = record.source_profile || {};
  const costProfile = record.cost_profile || {};
  const languageProfile = record.language_profile || {};
  const livingProfile = record.living_profile || {};
  const scholarshipProfile = record.scholarship_profile || {};
  const researchProfile = record.research_profile || {};
  const industryProfile = record.industry_ecosystem_profile || {};
  const curriculumProfile = record.curriculum_profile || {};
  const urls = record.urls || {};
  const categoryProfile = getCategoryProfile(record);

  const id = valueText(firstValue(record.Uni_ID, record.id, record.name, record.university));
  const universityName = firstValue(record.university, record.University, record.display_name, record.name) || "";
  const programName = firstValue(record.program_name, record.Program_Name, record.target_program_name, record.Target_Program_Name) || "";
  const city = valueText(firstValue(record.city, record.City));
  const country = valueText(firstValue(record.country, record.Country));
  const degree = firstValue(record.program_degree, record.Program_Degree, record.target_program_degree, record.degree_level, record.degree_class) || "";
  const degreeLevel = firstValue(record.degree_level, record.degree_class) || "";
  const teachingLanguage = stringList(firstKnownValue(
    record.teaching_language,
    languageProfile.teaching_language,
    record.Admission_Language_Req,
    record.admission_language_req,
    record.language_req
  ));
  const tuitionPerYear = firstFiniteNumber(
    costProfile.tuition_eur_per_year_estimated,
    costProfile.tuition_eur_per_year_min,
    record.tuition_eur_per_year,
    record.Tuition_EUR_Per_Year
  );
  const semesterFee = firstFiniteNumber(
    costProfile.regional_tax_eur,
    costProfile.student_contribution_eur,
    costProfile.enrollment_fee_eur,
    record.semester_fee_eur,
    record.Cost_Semester_Fees
  );
  const totalAcademicCost = firstFiniteNumber(
    costProfile.total_academic_cost_eur_per_year_estimated,
    record.annual_fee_eur,
    tuitionPerYear
  );
  const sources = normalizeSources(firstValue(
    sourceProfile.source_log,
    sourceProfile.official_program_page,
    record.Meta_Sources,
    record.sources
  ));
  const needsVerification = Boolean(firstValue(
    sourceProfile.needs_verification,
    record.needs_verification,
    record.Meta_Needs_Verification,
    false
  ));

  return {
    id,
    universityName,
    programName,
    city,
    country,
    degree,
    degreeLevel,
    teachingLanguage,
    programUrl: firstValue(record.program_url, record.target_program_url, urls.program, record.url) || "",
    tuitionPerYear,
    semesterFee,
    totalAcademicCost,
    hasKnownTuition: tuitionPerYear !== null || totalAcademicCost !== null,
    admissionMode: firstKnownValue(record.eligibility_profile?.admission_mode, record.Admission_Mode, record.admission_mode) || "unknown",
    admissionRisk: firstKnownValue(record.eligibility_profile?.admission_risk, record.admission_risk) || "unknown",
    languageRisk: firstKnownValue(languageProfile.language_risk, record.language_risk) || "unknown",
    housingDifficulty: firstKnownValue(livingProfile.housing_difficulty, record.Living_Housing_Difficulty, record.housing_difficulty) || "unknown",
    livingRisk: firstKnownValue(livingProfile.living_risk, record.living_risk, record.Cost_City_Living) || "unknown",
    cityCostLevel: firstKnownValue(livingProfile.cost_city_living, livingProfile.city_cost_level, record.cost_city_raw, record.Cost_City_Living) || "unknown",
    scholarshipSummary: firstValue(
      scholarshipProfile.funding_notes,
      scholarshipProfile.scholarship_names,
      scholarshipProfile.regional_scholarship_name,
      record.scholarship_names
    ) || "",
    researchSummary: firstValue(
      researchProfile.research_strength_summary,
      record.strong_areas_summary,
      record.research_strength,
      record.field_recognition
    ) || "",
    industrySummary: firstValue(
      industryProfile.ecosystem_notes,
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
    fieldConfidence: sourceProfile.field_confidence || {},
    needsVerification,
    lastVerified: sourceProfile.last_verified || record.updated_at || "",
    categoryProfile,
    location: normalizeLocation(record),
    qsRanking: firstFiniteNumber(record.qs_ranking),
    engineeringRanking: firstValue(record.engineering_ranking, record.field_recognition) || null,
    labs: Array.isArray(researchProfile.labs) ? researchProfile.labs : [],
    professors: Array.isArray(researchProfile.notable_professors) ? researchProfile.notable_professors : [],
    strongAreas: categoryProfile.normalized_tags,
    confirmedPartners: Array.isArray(industryProfile.confirmed_partners)
      ? industryProfile.confirmed_partners
      : (Array.isArray(record.Industry_Partners) ? record.Industry_Partners : []),
    internshipMandatory: firstValue(curriculumProfile.internship_required, record.internship_mandatory, record.Internship_Mandatory),
    housingCost: firstFiniteNumber(
      livingProfile.average_room_rent_eur,
      livingProfile.monthly_living_cost_eur_estimated,
      livingProfile.living_cost_eur_per_month
    ),
    scholarshipDetails: scholarshipProfile,
    admissionUrl: firstValue(sourceProfile.official_admission_page, urls.admission, record.admission_url) || "",
    tuitionUrl: firstValue(sourceProfile.official_tuition_page, urls.tuition, record.tuition_url) || "",
    scholarshipUrl: firstValue(sourceProfile.official_scholarship_page, scholarshipProfile.scholarship_application_url, record.scholarship_url) || "",
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
