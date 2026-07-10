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
  if (typeof value === "object") return value.en || value.tr || "";
  return String(value);
}

function getCategoryProfile(record) {
  return record.category_profile || record.Category_Profile || {
    primary_categories: [],
    secondary_categories: [],
    subcategories: [],
    normalized_tags: [],
    category_scores: {}
  };
}

function normalizeUniversityRecord(record) {
  if (!record) return {};

  const id = firstValue(record.Uni_ID, record.id, record.name, record.university) || "";
  const universityName = firstValue(record.university, record.University, record.display_name, record.name) || "";
  const programName = firstValue(record.program_name, record.Program_Name, record.target_program_name, record.Target_Program_Name) || "";
  const city = firstValue(record.city, record.City) || "";
  const country = firstValue(record.country, record.Country) || "";
  const degree = firstValue(record.program_degree, record.Program_Degree, record.target_program_degree, record.degree_level, record.degree_class) || "";
  const degreeLevel = firstValue(record.degree_level, record.degree_class) || "";
  
  let teachingLanguage = firstValue(
    record.teaching_language,
    record.language_profile?.teaching_language,
    record.language_profile?.teaching_language,
    record.Admission_Language_Req,
    record.admission_language_req,
    record.language_req
  ) || [];
  if (typeof teachingLanguage === "string") {
    teachingLanguage = [teachingLanguage];
  }

  const programUrl = firstValue(record.program_url, record.target_program_url, record.url) || "";
  
  const tuitionPerYear = firstValue(
    record.cost_profile?.tuition_eur_per_year_estimated,
    record.cost_profile?.tuition_eur_per_year_min,
    record.tuition_eur_per_year,
    record.Tuition_EUR_Per_Year
  );

  const semesterFee = firstValue(
    record.cost_profile?.regional_tax_eur,
    record.cost_profile?.student_contribution_eur,
    record.semester_fee_eur,
    record.Cost_Semester_Fees
  );

  const totalAcademicCost = firstValue(
    record.cost_profile?.total_academic_cost_eur_per_year_estimated,
    record.annual_fee_eur,
    record.tuition_eur_per_year
  );

  const admissionMode = firstValue(
    record.eligibility_profile?.admission_mode,
    record.Admission_Mode,
    record.admission_mode
  ) || "";

  const admissionRisk = firstValue(
    record.eligibility_profile?.admission_risk,
    record.admission_risk
  ) || "unknown";

  const languageRisk = firstValue(
    record.language_profile?.language_risk,
    record.language_risk
  ) || "unknown";

  const housingDifficulty = firstValue(
    record.living_profile?.housing_difficulty,
    record.Living_Housing_Difficulty,
    record.housing_difficulty
  ) || "unknown";

  const livingRisk = firstValue(
    record.living_profile?.living_risk,
    record.living_risk,
    record.cost_city_raw,
    record.Cost_City_Living
  ) || "unknown";

  const researchSummary = firstValue(
    record.research_profile?.research_strength_summary,
    record.strong_areas_summary,
    record.research_strength,
    record.field_recognition
  ) || "";

  const industrySummary = firstValue(
    record.industry_ecosystem_profile?.ecosystem_notes,
    record.aerospace_ecosystem,
    record.Industry_Ecosystem,
    record.industry_ecosystem
  ) || "";

  const decisionSummary = record.decision_summary || {};
  
  function normalizeArrayObj(arr) {
    if (!arr) return [];
    if (Array.isArray(arr)) return arr;
    if (typeof arr === 'object') {
        // Handle format: {"en": ["A", "B"], "tr": ["X", "Y"]}
        const enArr = Array.isArray(arr.en) ? arr.en : [];
        const trArr = Array.isArray(arr.tr) ? arr.tr : [];
        const length = Math.max(enArr.length, trArr.length);
        const result = [];
        for (let i = 0; i < length; i++) {
            result.push({
                en: enArr[i] || '',
                tr: trArr[i] || enArr[i] || ''
            });
        }
        return result;
    }
    return [];
  }

  const mainStrengths = normalizeArrayObj(firstValue(
    record.decision_summary?.main_strengths,
    record.Analysis_Pros,
    record.pros
  ) || []);

  const mainRisks = normalizeArrayObj(firstValue(
    record.decision_summary?.main_risks,
    record.Analysis_Cons,
    record.cons
  ) || []);

  const bestFor = normalizeArrayObj(record.decision_summary?.best_for || []);
  const notIdealFor = normalizeArrayObj(record.decision_summary?.not_ideal_for || []);
  
  const pros = firstValue(record.pros, record.Analysis_Pros) || [];
  const cons = firstValue(record.cons, record.Analysis_Cons) || [];

  let sources = firstValue(
    record.source_profile?.source_log,
    record.source_profile?.official_program_page,
    record.Meta_Sources,
    record.sources
  ) || [];

  if (!Array.isArray(sources)) {
    if (typeof sources === "string") {
      sources = [{ url: sources }];
    } else if (typeof sources === "object") {
      sources = [sources];
    } else {
      sources = [];
    }
  }

  const fieldConfidence = record.source_profile?.field_confidence || {};
  
  const categoryProfile = getCategoryProfile(record);

  return {
    id,
    universityName,
    programName,
    city,
    country,
    degree,
    degreeLevel,
    teachingLanguage,
    programUrl,
    tuitionPerYear,
    semesterFee,
    totalAcademicCost,
    admissionMode,
    admissionRisk,
    languageRisk,
    housingDifficulty,
    livingRisk,
    scholarshipSummary: firstValue(record.scholarship_profile?.scholarship_names, record.scholarship_names) || "",
    researchSummary,
    industrySummary,
    decisionSummary,
    mainStrengths,
    mainRisks,
    bestFor,
    notIdealFor,
    pros,
    cons,
    sources,
    fieldConfidence,
    categoryProfile,
    location: record.location || null,
    raw: record
  };
}

window.uniDataAdapter = {
  firstValue,
  getPath,
  localizedField,
  getCategoryProfile,
  normalizeUniversityRecord
};
