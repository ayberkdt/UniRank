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
  const acceptedStatuses = new Set(["ok", "redirects", "pdf", "requires_js"]);
  return sources.some((source) => acceptedStatuses.has(String(source?.access_status || "").toLowerCase()));
}

function calculateScore(record, preferences, weights) {
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

  const targetDegree = degreeKey(profile?.target_degree || preferences.degreeFilter || "All");
  const recordDegree = degreeKey(normalized?.degreeLevel || normalized?.degree || record.Program_Degree);
  if (targetDegree !== "all" && recordDegree !== targetDegree) passed = false;

  const languages = normalized?.teachingLanguage || [];
  const languageText = languages.join(" ").toLowerCase();
  const hasEnglishTeaching = /\benglish\b/.test(languageText);
  const hasOtherTeachingLanguage = /\b(german|french|dutch|italian|spanish|portuguese|swedish|japanese|korean|chinese|russian|turkish)\b/.test(languageText);
  const isEnglishOnlyPref = profile ? profile.language_filter === "english_only" : Boolean(preferences.onlyEnglish);
  if (isEnglishOnlyPref && (!hasEnglishTeaching || hasOtherTeachingLanguage)) {
    passed = false;
    profileMatch.profile_penalties.push({ type: "language", reason: "Teaching language is not verified as English-only." });
  }

  const annualCost = finiteNumber(normalized?.totalAcademicCost ?? normalized?.tuitionPerYear);
  const sliderCap = finiteNumber(preferences.maxTuition);
  const profileCap = finiteNumber(profile?.max_tuition_eur_per_year);
  const activeHardCap = sliderCap && sliderCap > 0
    ? sliderCap
    : (profile?.strict_budget && profileCap && profileCap > 0 ? profileCap : null);
  if (activeHardCap !== null && (annualCost === null || annualCost > activeHardCap)) {
    passed = false;
    profileMatch.profile_penalties.push({ type: "cost", reason: "Tuition is unknown or exceeds the selected hard limit." });
  }

  let academicFit = 50;
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

    academicFit = maxPossible > 0 ? Math.round((score / maxPossible) * 100) : 50;
    profileMatch.personal_field_fit = academicFit;
    explanation.push(academicFit >= 80
      ? "Strong personalized match with your interest graph."
      : academicFit >= 40
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
      academicFit = Math.min(100, Math.max(0, scoreSum / selectedCategories.length));
      explanation.push(academicFit >= 80
        ? "Strong academic match for your selected fields."
        : academicFit >= 40
          ? "Partial academic match for your selected fields."
          : "No strong match found for your selected fields.");
    }
  }
  if (preferences.minFieldFit && academicFit < preferences.minFieldFit) passed = false;

  let eligibilityFit = 55;
  if (languages.length > 0) {
    eligibilityFit += hasEnglishTeaching ? 20 : 0;
    eligibilityFit += hasOtherTeachingLanguage ? -10 : 10;
  } else {
    warnings.push("Teaching language is unknown.");
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

  const semesterFee = finiteNumber(normalized?.semesterFee);
  const tuitionScore = annualCost === null ? 45 : (1 - Math.min(1, annualCost / 20000)) * 100;
  const semesterFeeScore = semesterFee === null ? 50 : (1 - Math.min(1, semesterFee / 1000)) * 100;
  let scholarshipScore = 40;
  const scholarshipProfile = record.scholarship_profile || {};
  if (!normalized?.needsVerification && scholarshipProfile.non_eu_eligible === true) {
    scholarshipScore = 100;
    explanation.push("Scholarship eligibility is documented for non-EU students.");
  } else if (!normalized?.needsVerification && scholarshipProfile.regional_scholarship_available === true) {
    scholarshipScore = 80;
    explanation.push("Regional scholarship availability is documented.");
  } else if (normalized?.needsVerification && normalized?.scholarshipSummary) {
    warnings.push("Scholarship information needs verification.");
  }
  let costFit = (tuitionScore * 0.7) + (semesterFeeScore * 0.2) + (scholarshipScore * 0.1);
  if (annualCost === null) {
    warnings.push("Tuition is unknown, so the cost score is neutral.");
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

  let careerFit = 50;
  const partnerText = normalizeText((normalized?.confirmedPartners || []).map((partner) => typeof partner === "object" ? partner.name || partner.en || "" : partner).join(" "));
  const premiumPartners = ["esa", "dlr", "nasa", "jaxa", "airbus", "cern", "onera", "isae", "estec"];
  const partnerMatches = normalized?.needsVerification ? 0 : premiumPartners.filter((partner) => partnerText.includes(partner)).length;
  careerFit += partnerMatches * 15;
  if (normalized?.internshipMandatory === true && !normalized?.needsVerification) {
    careerFit += 10;
    explanation.push("A documented mandatory internship supports industry exposure.");
  }
  careerFit = Math.min(100, Math.max(0, careerFit));

  let livingFit = 50;
  const cityCost = String(normalized?.cityCostLevel || normalized?.livingRisk || "").toLowerCase();
  if (cityCost.includes("very_high")) livingFit -= 30;
  else if (cityCost.includes("high")) livingFit -= 15;
  else if (cityCost.includes("low")) livingFit += 20;
  const housing = String(normalized?.housingDifficulty || "").toLowerCase();
  if (housing.includes("nightmare")) {
    livingFit -= profileMatch.enabled && profile?.housing_risk_tolerance === "low" ? 50 : 30;
    warnings.push("Housing market is extremely difficult.");
  } else if (housing.includes("very hard")) {
    livingFit -= profileMatch.enabled && profile?.housing_risk_tolerance === "low" ? 40 : 20;
    warnings.push("Housing market is very difficult.");
  } else if (housing.includes("hard")) {
    livingFit -= 10;
  } else if (housing.includes("moderate") || housing.includes("easy")) {
    livingFit += 20;
    explanation.push("Housing is relatively accessible.");
  }
  livingFit = Math.min(100, Math.max(0, livingFit));

  const sourceVerified = hasAccessibleSource(normalized?.sources || []);
  let confidenceFit = sourceVerified ? 85 : 50;
  if (normalized?.needsVerification) {
    confidenceFit = Math.min(confidenceFit, 35);
    warnings.push("Critical data requires source verification.");
  } else if (sourceVerified) {
    explanation.push("The record includes accessible source evidence.");
  } else {
    warnings.push("No accessible source log is available for this record.");
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
    explanation,
    warnings,
    personalized_match: profileMatch
  };
}

export { calculateScore };
