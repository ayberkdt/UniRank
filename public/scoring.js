function normalizeText(text) {
  if (!text) return "";
  return String(text).toLowerCase().replace(/[^a-z0-9\s]/g, " ");
}

function finiteNumber(value) {
  if (value === null || value === undefined || value === "") return null;
  const number = typeof value === "number" ? value : Number(value);
  return Number.isFinite(number) ? number : null;
}

function degreeKey(value) {
  const text = String(value || "").toLowerCase();
  if (!text || text === "all") return "all";
  if (text.includes("doctor") || text.includes("phd")) return "phd";
  if (text.includes("master") || text.includes("msc") || text.includes("m.sc")) return "msc";
  if (text.includes("bachelor") || text.includes("bsc") || text.includes("b.sc")) return "bsc";
  return "unknown";
}

function hasAccessibleSource(sources) {
  const acceptedStatuses = new Set(["ok", "redirects", "pdf"]);
  const officialTypes = new Set([
    "official_program_page", "official_admission_page", "official_curriculum_page",
    "official_tuition_page", "official_scholarship_page", "official_department_page",
    "official_lab_page", "official_housing_page", "official_visa_or_government_page",
    "official_industry_partner_page"
  ]);
  return sources.some((source) => (
    officialTypes.has(String(source?.source_type || "").toLowerCase()) &&
    acceptedStatuses.has(String(source?.access_status || "").toLowerCase())
  ));
}

function hasVerifiedField(normalized, field) {
  return Array.isArray(normalized?.dataQuality?.verifiedFields) && normalized.dataQuality.verifiedFields.includes(field);
}

function hasVerifiedEnglishStudyOption(record, normalized) {
  if (!hasVerifiedField(normalized, "language")) return false;

  const languages = normalized?.teachingLanguage || [];
  const languageText = languages.join(" ").toLowerCase();
  if (/\benglish\b/.test(languageText)) return true;

  const languageProfile = record?.language_profile || {};
  const flags = record?.scoring_inputs?.hard_filter_flags || record?._scoring_inputs?.hard_filter_flags || {};
  if (languageProfile.english_study_option_available === true || flags.english_study_option_available === true) return true;

  // Legacy records used this flag for programmes such as TUM where an
  // English-completable specialisation exists even though the top-level
  // language value is "Mixed". A false value must not reject bilingual
  // records whose explicit language list contains English.
  if (languageText.includes("mixed") && flags.english_only_compatible === true) return true;
  return languageText.includes("mixed") && languageProfile.english_required === true;
}

function bounded(value, fallback = 50) {
  const number = finiteNumber(value);
  return number === null ? fallback : Math.min(100, Math.max(0, number));
}

const DEFAULT_SCORE_WEIGHTS = {
  academic_fit: 30,
  eligibility_language: 20,
  cost_funding: 20,
  career_research: 15,
  living_risk: 10,
  confidence_deadline: 5
};

function normalizeWeights(input = {}) {
  const sanitized = Object.fromEntries(Object.keys(DEFAULT_SCORE_WEIGHTS).map((key) => {
    const value = finiteNumber(input?.[key]);
    return [key, value === null ? 0 : Math.max(0, value)];
  }));
  const total = Object.values(sanitized).reduce((sum, value) => sum + value, 0);
  const basis = total > 0 ? sanitized : DEFAULT_SCORE_WEIGHTS;
  const basisTotal = Object.values(basis).reduce((sum, value) => sum + value, 0);
  return Object.fromEntries(Object.entries(basis).map(([key, value]) => [key, (value / basisTotal) * 100]));
}

function annualTuitionScore(value) {
  if (value === null) return 50;
  if (value <= 0) return 95;
  if (value <= 2000) return 85;
  if (value <= 5000) return 70;
  if (value <= 10000) return 55;
  if (value <= 20000) return 35;
  return 15;
}

function stringEntries(value) {
  if (Array.isArray(value)) {
    return value.map((item) => {
      if (typeof item === "string") return item.trim();
      if (!item || typeof item !== "object") return "";
      const candidate = item.en
        ?? item.name?.en
        ?? item.name
        ?? item.label?.en
        ?? item.label
        ?? item.title?.en
        ?? item.title;
      return typeof candidate === "string" ? candidate.trim() : "";
    }).filter(Boolean);
  }
  return typeof value === "string" && value.trim() ? [value] : [];
}

function uniqueDocumentedEntries(...values) {
  return [...new Set(values.flatMap(stringEntries).map((item) => normalizeText(item)).filter(Boolean))];
}

function documentedAcademicStrength(record, normalized, hasCurriculumEvidence, hasResearchEvidence) {
  const research = record?.research_profile || {};
  const curriculum = record?.curriculum_profile || {};
  const categories = normalized?.categoryProfile || {};
  const documentedTopics = new Set([
    ...stringEntries(categories.primary_categories),
    ...stringEntries(categories.secondary_categories),
    ...stringEntries(categories.subcategories),
    ...stringEntries(categories.normalized_tags),
    ...stringEntries(curriculum.specializations),
    ...stringEntries(research.research_focus_areas),
    ...stringEntries(research.department_research_areas)
  ].map((item) => normalizeText(item)).filter(Boolean));

  // A high result must be traceable to checked curriculum/research evidence.
  // Legacy prestige, ranking and self-entered numeric seeds are intentionally excluded.
  // The multipliers below are deliberately steep: two labs and eight labs are
  // very different research environments and must not land on the same score.
  let score = hasCurriculumEvidence ? 42 : 25;
  score += Math.min(12, documentedTopics.size * 1.5);
  if (!hasResearchEvidence) return bounded(score);

  const labs = uniqueDocumentedEntries(research.labs, research.named_facilities).length;
  const centers = uniqueDocumentedEntries(research.research_centers, research.key_institutes).length;
  const projects = stringEntries(research.space_or_aerospace_projects).length
    + stringEntries(research.satellite_or_flight_projects).length;
  const teams = stringEntries(research.student_teams).length;

  score += 10;
  score += Math.min(24, labs * 3);
  score += Math.min(6, centers * 2);
  score += Math.min(12, projects * 4);
  score += Math.min(4, teams * 1.5);
  return bounded(score);
}

function calculateScore(record, preferences, weights) {
  weights = normalizeWeights(weights);
  const explanation = [];
  const warnings = [];
  const profileMatch = {
    enabled: window.personalizationEnabled || false,
    personal_field_fit: null,
    matched_interests: [],
    profile_penalties: [],
    profile_boosts: []
  };
  const normalized = window.uniDataAdapter ? window.uniDataAdapter.normalizeUniversityRecord(record) : null;
  const profile = profileMatch.enabled ? window.userProfile : null;
  const categoryProfile = normalized?.categoryProfile || record.Category_Profile || {
    category_scores: {},
    subcategories: [],
    normalized_tags: []
  };
  const categoryScores = categoryProfile.category_scores || {};
  const subcategories = Array.isArray(categoryProfile.subcategories) ? categoryProfile.subcategories : [];
  const normalizedTags = Array.isArray(categoryProfile.normalized_tags) ? categoryProfile.normalized_tags : [];
  let passed = true;

  const requestedDegree = degreeKey(profile?.target_degree || preferences.degreeFilter || "All");
  const targetDegree = requestedDegree === "bsc" ? "msc" : requestedDegree;
  const recordDegree = degreeKey(normalized?.degreeLevel || normalized?.degree || record.Program_Degree);
  if (targetDegree !== "all" && recordDegree !== targetDegree) passed = false;

  const languages = normalized?.teachingLanguage || [];
  const languageText = languages.join(" ").toLowerCase();
  const hasEnglishStudyOption = hasVerifiedEnglishStudyOption(record, normalized);
  const hasOtherTeachingLanguage = /\b(german|french|dutch|italian|spanish|portuguese|swedish|japanese|korean|chinese|russian|turkish)\b/.test(languageText);
  const requiresEnglishOption = Boolean(preferences.onlyEnglish)
    || Boolean(profile && ["english_available", "english_only"].includes(profile.language_filter));
  if (requiresEnglishOption && !hasEnglishStudyOption) {
    passed = false;
    profileMatch.profile_penalties.push({ type: "language", reason: "No verified English-taught route or option is available." });
  }

  // Only a verified annual tuition value enters the affordability score and
  // hard cap. Semester fees, one-off enrolment fees and full-program totals
  // stay visible in details but are never mixed into the same numeric scale.
  const annualCost = hasVerifiedField(normalized, "tuition")
    ? finiteNumber(normalized?.tuitionPerYear)
    : null;
  const sliderCap = finiteNumber(preferences.maxTuition);
  const profileCap = finiteNumber(profile?.max_tuition_eur_per_year);
  const activeHardCap = sliderCap && sliderCap > 0
    ? sliderCap
    : (profile?.strict_budget && profileCap && profileCap > 0 ? profileCap : null);
  if (activeHardCap !== null && (annualCost === null || annualCost > activeHardCap)) {
    passed = false;
    profileMatch.profile_penalties.push({ type: "cost", reason: "Tuition is unknown or exceeds the selected hard limit." });
  }

  const hasCurriculumEvidence = hasVerifiedField(normalized, "curriculum");
  const hasResearchEvidence = hasVerifiedField(normalized, "research");
  const academicStrength = documentedAcademicStrength(record, normalized, hasCurriculumEvidence, hasResearchEvidence);
  let technicalMatch = hasCurriculumEvidence ? 60 : 40;
  if (profileMatch.enabled && Array.isArray(profile?.interests) && profile.interests.length > 0 && window.buildExpandedInterestProfile) {
    const expandedInterests = window.buildExpandedInterestProfile(profile.interests, window.INTEREST_GRAPH || {});
    let score = 0;
    let maxPossible = 0;
    const recordTags = new Set(normalizedTags);

    for (const [interestKey, userWeight] of expandedInterests.entries()) {
      maxPossible += userWeight;
      let matched = false;
      const legacyLabel = window.INTEREST_GRAPH?.[interestKey]?.label?.en || interestKey;
      if (recordTags.has(interestKey) || recordTags.has(legacyLabel) || subcategories.includes(interestKey) || subcategories.includes(legacyLabel)) {
        score += userWeight;
        matched = true;
      } else if (categoryScores[interestKey] !== undefined || categoryScores[legacyLabel] !== undefined) {
        const categoryScore = finiteNumber(categoryScores[interestKey] ?? categoryScores[legacyLabel]) || 0;
        score += userWeight * Math.max(0, Math.min(1, categoryScore / 100));
        matched = true;
      }
      if (matched) {
        profileMatch.matched_interests.push({
          interest_key: interestKey,
          match_strength: userWeight,
          match_type: profile.interests.some((interest) => interest.key === interestKey) ? "direct" : "graph_neighbor"
        });
      }
    }

    technicalMatch = maxPossible > 0 ? Math.round((score / maxPossible) * 100) : 40;
    if (!hasCurriculumEvidence) {
      technicalMatch = Math.min(technicalMatch, 40);
      warnings.push("Technical tags are not yet backed by a checked curriculum source.");
    }
    profileMatch.personal_field_fit = technicalMatch;
    explanation.push(technicalMatch >= 80
      ? "Strong personalized match with your interest graph."
      : technicalMatch >= 40
        ? "Partial match with your expanded interest fields."
        : "Weak match with your stated academic interests.");
  } else {
    const selectedCategories = preferences.selectedCategoryKeys || preferences.selectedKeywords || [];
    if (selectedCategories.length > 0) {
      let scoreSum = 0;
      for (const category of selectedCategories) {
        if (categoryScores[category] !== undefined) scoreSum += finiteNumber(categoryScores[category]) || 0;
        else if (subcategories.includes(category)) scoreSum += 100;
        else if (normalizedTags.includes(category)) scoreSum += 60;
      }
      technicalMatch = Math.min(100, Math.max(0, scoreSum / selectedCategories.length));
      if (!hasCurriculumEvidence) {
        technicalMatch = Math.min(technicalMatch, 40);
        warnings.push("Technical match is capped until the curriculum source is checked.");
      }
      explanation.push(technicalMatch >= 80
        ? "Strong academic match for your selected fields."
        : technicalMatch >= 40
          ? "Partial academic match for your selected fields."
          : "No strong match found for your selected fields.");
    } else {
      if (!hasCurriculumEvidence) warnings.push("Academic strength is conservative because curriculum evidence is incomplete.");
    }
  }
  // Programme-level relevance is an evidence-backed scope judgement. A well
  // documented aviation-management curriculum must not outrank direct space
  // engineering merely because it has many checked courses and research credits.
  const relevanceStatus = String(
    record?.program_profile?.relevance_status || record?.relevance_status || ""
  ).toLowerCase();
  const technicalRelevanceCaps = { strong: 100, medium: 70, weak: 25, needs_review: 100 };
  const academicRelevanceCaps = { strong: 100, medium: 78, weak: 45, needs_review: 100 };
  const technicalRelevanceCap = technicalRelevanceCaps[relevanceStatus] ?? 100;
  const academicRelevanceCap = academicRelevanceCaps[relevanceStatus] ?? 100;
  if (technicalMatch > technicalRelevanceCap) {
    technicalMatch = technicalRelevanceCap;
    warnings.push(`Technical fit is capped because programme relevance is classified as ${relevanceStatus}.`);
  }
  if (profileMatch.enabled) profileMatch.personal_field_fit = technicalMatch;
  // This slider is deliberately academic strength first. A selected technical
  // field can refine it, but cannot make an undocumented prestige claim win.
  const academicFit = Math.min(
    academicRelevanceCap,
    Math.round((academicStrength * 0.8) + (technicalMatch * 0.2))
  );
  explanation.push(`Academic strength ${academicStrength}/100 is based on checked curriculum and research evidence.`);
  if (preferences.minFieldFit && technicalMatch < preferences.minFieldFit) passed = false;

  let eligibilityFit = 55;
  if (hasEnglishStudyOption) {
    eligibilityFit += 30;
  } else if (hasOtherTeachingLanguage) {
    eligibilityFit -= 10;
  } else {
    warnings.push("No verified English study option is documented.");
  }
  const admissionMode = String(normalized?.admissionMode || "").toLowerCase();
  if (admissionMode.includes("direct")) {
    eligibilityFit += 20;
    explanation.push("Direct admission offers lower entry risk.");
  } else if (/(aptitude|committee|portfolio|interview|competitive)/.test(admissionMode)) {
    eligibilityFit -= profileMatch.enabled && profile?.admission_risk_tolerance === "low" ? 40 : 20;
    warnings.push(`Competitive admission process (${normalized.admissionMode}).`);
  }
  eligibilityFit = Math.min(100, Math.max(0, eligibilityFit));

  const tuitionScore = annualTuitionScore(annualCost);
  let scholarshipScore = 50;
  const scholarshipProfile = record.scholarship_profile || {};
  const scholarshipVerified = hasVerifiedField(normalized, "scholarship");
  if (scholarshipVerified && scholarshipProfile.non_eu_eligible === true) {
    scholarshipScore = 100;
    explanation.push("Scholarship eligibility is documented for non-EU students.");
  } else if (scholarshipVerified && scholarshipProfile.regional_scholarship_available === true) {
    scholarshipScore = 80;
    explanation.push("Regional scholarship availability is documented.");
  } else if (normalized?.scholarshipSummary) {
    warnings.push("Scholarship information needs verification.");
  }
  let costFit = (tuitionScore * 0.75) + (scholarshipScore * 0.25);
  if (annualCost === null) {
    warnings.push("Comparable verified annual tuition is unavailable, so tuition is neutral in the cost score.");
  } else if (annualCost > 10000) {
    warnings.push(`High yearly tuition (€${annualCost.toFixed(0)}).`);
  } else if (annualCost <= 2000) {
    explanation.push(`Low documented tuition (€${annualCost.toFixed(0)}/yr).`);
  }
  if (profileCap && annualCost !== null && annualCost > profileCap && !profile?.strict_budget) {
    costFit -= 30;
    if (profileMatch.enabled) profileMatch.profile_penalties.push({ type: "cost", reason: "Tuition exceeds the preferred maximum." });
  }
  costFit = Math.min(100, Math.max(0, costFit));

  let careerFit = hasResearchEvidence ? 50 : 40;
  const confirmedPartners = normalized?.confirmedPartners || [];
  const partnerText = normalizeText(confirmedPartners.map((partner) => typeof partner === "object" ? partner.name || partner.en || "" : partner).join(" "));
  const premiumPartners = ["esa", "dlr", "nasa", "jaxa", "airbus", "cern", "onera", "isae", "estec", "boeing", "safran", "thales", "leonardo", "ohb"];
  // Curated partner lists on a fully verified record are usable evidence even
  // when the dedicated "industry" flag was never set by the research pipeline.
  const partnersUsable = hasVerifiedField(normalized, "industry")
    || (normalized?.dataQuality?.status === "verified" && confirmedPartners.length > 0);
  if (partnersUsable) {
    const premiumMatches = premiumPartners.filter((partner) => partnerText.includes(partner)).length;
    careerFit += Math.min(12, confirmedPartners.length * 3);
    careerFit += Math.min(24, premiumMatches * 8);
    if (premiumMatches > 0) explanation.push("Documented partnerships with major aerospace organisations.");
  }
  if (hasResearchEvidence) {
    const careerProjects = stringEntries(record?.research_profile?.space_or_aerospace_projects).length
      + stringEntries(record?.research_profile?.satellite_or_flight_projects).length;
    careerFit += Math.min(10, careerProjects * 3);
  }
  if (normalized?.internshipMandatory === true && hasCurriculumEvidence) {
    careerFit += 8;
    explanation.push("A documented mandatory internship supports industry exposure.");
  }
  careerFit = Math.min(100, Math.max(0, careerFit));

  const housingVerified = hasVerifiedField(normalized, "housing");
  let livingFit = housingVerified ? 50 : 45;
  const cityCost = String(normalized?.cityCostLevel || normalized?.livingRisk || "").toLowerCase();
  if (housingVerified && cityCost.includes("very_high")) livingFit -= 30;
  else if (housingVerified && cityCost.includes("high")) livingFit -= 15;
  else if (housingVerified && cityCost.includes("low")) livingFit += 20;
  const housing = String(normalized?.housingDifficulty || "").toLowerCase();
  if (housingVerified && housing.includes("nightmare")) {
    livingFit -= profileMatch.enabled && profile?.housing_risk_tolerance === "low" ? 50 : 30;
    warnings.push("Housing market is extremely difficult.");
  } else if (housingVerified && housing.includes("very hard")) {
    livingFit -= profileMatch.enabled && profile?.housing_risk_tolerance === "low" ? 40 : 20;
    warnings.push("Housing market is very difficult.");
  } else if (housingVerified && housing.includes("hard")) {
    livingFit -= 10;
  } else if (housingVerified && (housing.includes("moderate") || housing.includes("easy"))) {
    livingFit += 20;
    explanation.push("Housing is relatively accessible.");
  }
  livingFit = Math.min(100, Math.max(0, livingFit));

  const sourceVerified = hasAccessibleSource(normalized?.sources || []);
  const qualityStatus = normalized?.dataQuality?.status || (normalized?.needsVerification ? "needs_verification" : "partial");
  const verifiedCount = normalized?.dataQuality?.verifiedFields?.length || 0;
  let confidenceFit = qualityStatus === "verified" ? 90 : qualityStatus === "partial" ? Math.min(75, 42 + (verifiedCount * 6)) : 20;
  if (!sourceVerified) confidenceFit = Math.min(confidenceFit, 20);
  if (qualityStatus !== "verified") {
    warnings.push("Critical data requires source verification.");
  } else {
    explanation.push("The record has checked official source evidence for all critical fields.");
  }

  const totalWeight = (
    weights.academic_fit + weights.eligibility_language + weights.cost_funding +
    weights.career_research + weights.living_risk + weights.confidence_deadline
  ) || 100;
  const finalScore = (
    academicFit * (weights.academic_fit / totalWeight) +
    eligibilityFit * (weights.eligibility_language / totalWeight) +
    costFit * (weights.cost_funding / totalWeight) +
    careerFit * (weights.career_research / totalWeight) +
    livingFit * (weights.living_risk / totalWeight) +
    confidenceFit * (weights.confidence_deadline / totalWeight)
  );

  const weightedComponents = {
    academic_fit: academicFit * (weights.academic_fit / totalWeight),
    eligibility_language: eligibilityFit * (weights.eligibility_language / totalWeight),
    cost_funding: costFit * (weights.cost_funding / totalWeight),
    career_research: careerFit * (weights.career_research / totalWeight),
    living_risk: livingFit * (weights.living_risk / totalWeight),
    confidence_deadline: confidenceFit * (weights.confidence_deadline / totalWeight)
  };

  return {
    passed_hard_filters: passed,
    total_score: finalScore,
    components: {
      academic_fit: academicFit,
      eligibility_language: eligibilityFit,
      cost_funding: costFit,
      career_research: careerFit,
      living_risk: livingFit,
      confidence_deadline: confidenceFit
    },
    weighted_components: weightedComponents,
    normalized_weights: weights,
    explanation,
    warnings,
    personalized_match: profileMatch
  };
}

if (typeof module !== "undefined" && module.exports) {
  module.exports = { calculateScore, normalizeWeights };
} else {
  window.unirankScoring = { calculateScore, normalizeWeights };
}
