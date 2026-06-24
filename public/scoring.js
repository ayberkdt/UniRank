/**
 * UniRank Scoring Engine (JS)
 * Centralized multi-dimensional scoring logic with personalization support.
 */

function normalizeText(text) {
    if (!text) return "";
    return String(text).toLowerCase().replace(/[^a-z0-9\s]/g, ' ');
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

    // Extract User Profile if personalization is enabled
    const profile = profileMatch.enabled ? window.userProfile : null;

    // --- HARD FILTERS ---
    let passed = true;

    // 1. Degree Filter
    const targetDegree = profile?.target_degree || preferences.degreeFilter || 'All';
    const recDegree = String(record.Program_Degree || record.program_degree || '').toLowerCase();
    if (targetDegree !== 'All' && recDegree) {
        if (!recDegree.includes(targetDegree.toLowerCase())) {
            passed = false;
        }
    }

    // 2. English Only Filter
    const langReq = String(record.Admission_Language_Req || record.admission_language_req || '').toLowerCase();
    const isEnglishOnlyPref = profile ? (profile.language_filter === 'english_only') : preferences.onlyEnglish;
    if (isEnglishOnlyPref) {
        if (langReq.includes('german') || langReq.includes('french') || langReq.includes('dutch') || langReq.includes('b1') || langReq.includes('c1') && !langReq.includes('english c1')) {
            if (langReq.includes('german') || langReq.includes('french') || langReq.includes('dutch')) {
                passed = false;
            }
        }
    }

    // 3. Max Tuition
    const tuit = parseFloat(record.tuition_eur_per_year) || 0;
    const maxTPref = profile?.max_tuition_eur_per_year || preferences.maxTuition;
    if (maxTPref && maxTPref > 0) {
        if (profile?.strict_budget && tuit > maxTPref) {
            passed = false;
        }
    }

    // --- SCORE COMPONENTS ---

    let catProfile = record.Category_Profile;
    if (!catProfile) {
        catProfile = { category_scores: {}, subcategories: [], normalized_tags: [] };
    }

    // 1. Academic / Field Fit (0-100)
    let academicFit = 0;
    
    if (profileMatch.enabled && profile?.interests?.length > 0 && window.buildExpandedInterestProfile) {
        // Personalized Field Fit
        const expandedInterests = window.buildExpandedInterestProfile(profile.interests, window.INTEREST_GRAPH || {});
        
        let score = 0;
        let maxPossible = 0;
        const recordTags = new Set(catProfile.normalized_tags || []);
        
        for (const [interestKey, userWeight] of expandedInterests.entries()) {
            maxPossible += userWeight;
            let matched = false;
            let matchType = '';
            
            // Get legacy label just in case the record hasn't been migrated yet
            const legacyLabel = window.INTEREST_GRAPH && window.INTEREST_GRAPH[interestKey] ? window.INTEREST_GRAPH[interestKey].label.en : interestKey;
            
            if (recordTags.has(interestKey) || recordTags.has(legacyLabel)) {
                score += userWeight;
                matched = true;
                matchType = 'direct';
            } else if (catProfile.subcategories.includes(interestKey) || catProfile.subcategories.includes(legacyLabel)) {
                score += userWeight;
                matched = true;
                matchType = 'direct';
            } else if (catProfile.category_scores[interestKey]) {
                const ratio = catProfile.category_scores[interestKey] / 100;
                score += userWeight * ratio;
                matched = true;
                matchType = 'partial';
            } else if (catProfile.category_scores[legacyLabel]) {
                const ratio = catProfile.category_scores[legacyLabel] / 100;
                score += userWeight * ratio;
                matched = true;
                matchType = 'partial';
            }
            
            if (matched) {
                const isDirectUserSelected = profile.interests.find(i => i.key === interestKey);
                profileMatch.matched_interests.push({
                    interest_key: interestKey,
                    match_strength: userWeight,
                    match_type: isDirectUserSelected ? 'direct' : 'graph_neighbor'
                });
            }
        }
        
        if (maxPossible > 0) {
            academicFit = Math.round((score / maxPossible) * 100);
            profileMatch.personal_field_fit = academicFit;
        } else {
            academicFit = 50;
        }
        
        if (academicFit >= 80) explanation.push("Strong personalized match with your interest graph.");
        else if (academicFit >= 40) explanation.push("Partial match with your expanded interest fields.");
        else explanation.push("Weak match with your stated academic interests.");

    } else {
        // Default Academic Fit
        const selectedCats = preferences.selectedCategoryKeys || preferences.selectedKeywords || [];
        if (selectedCats.length === 0) {
            academicFit = 50;
        } else {
            let scoreSum = 0;
            let matches = 0;
            for (const cat of selectedCats) {
                if (catProfile.category_scores[cat] !== undefined) {
                    const catScore = catProfile.category_scores[cat];
                    scoreSum += catScore;
                    if (catScore >= 30) matches++;
                }
                else if (catProfile.subcategories.includes(cat)) {
                    scoreSum += 100;
                    matches++;
                }
                else if (catProfile.normalized_tags.includes(cat)) {
                    scoreSum += 60;
                    matches++;
                }
            }
            if (selectedCats.length > 0) academicFit = scoreSum / selectedCats.length;
            academicFit = Math.min(100, Math.max(0, academicFit));
            if (academicFit >= 80) explanation.push("Strong academic match for your selected fields.");
            else if (academicFit >= 40) explanation.push("Partial academic match for your selected fields.");
            else explanation.push("No strong match found for your selected fields.");
        }
    }

    if (preferences.minFieldFit && academicFit < preferences.minFieldFit) {
        passed = false;
    }

    // 2. Eligibility & Language Fit (0-100)
    let eligFit = 70;
    const adMode = String(record.Admission_Mode || '').toLowerCase();
    
    if (langReq.includes('english')) {
        eligFit += 10;
        if (!langReq.includes('german') && !langReq.includes('french') && !langReq.includes('dutch')) {
            eligFit += 10;
            explanation.push(`Program is fully English-taught.`);
        } else {
            eligFit -= 20;
            warnings.push(`Requires an additional language (${langReq}).`);
            if (profileMatch.enabled && profile?.language_filter === 'english_only') {
                profileMatch.profile_penalties.push({ type: 'language', reason: 'Requires non-English language.' });
            }
        }
    }
    
    if (adMode.includes('direct')) {
        eligFit += 20;
        explanation.push(`Direct admission offers lower entry risk.`);
    } else if (adMode.includes('aptitude test') || adMode.includes('committee') || adMode.includes('portfolio') || adMode.includes('interview')) {
        if (profileMatch.enabled && profile?.admission_risk_tolerance === 'low') {
            eligFit -= 40;
            profileMatch.profile_penalties.push({ type: 'admission', reason: 'Competitive admission conflicts with low risk tolerance.' });
        } else {
            eligFit -= 20;
        }
        warnings.push(`Competitive admission process (${adMode}).`);
    }

    eligFit = Math.min(100, Math.max(0, eligFit));


    // 3. Cost & Funding (0-100)
    let costFit = 0;
    const maxT = 20000;
    const tuitionNorm = Math.min(1.0, tuit / maxT);
    let tuitionScore = (1.0 - tuitionNorm) * 100;
    
    const semFee = parseFloat(record.semester_fee_eur) || 0;
    const semFeeNorm = Math.min(1.0, semFee / 1000);
    let semFeeScore = (1.0 - semFeeNorm) * 100;

    let scholarshipScore = 0;
    const sp = record.scholarship_profile || {};
    if (sp.non_eu_eligible === true) {
        scholarshipScore = 100;
        explanation.push(`Scholarships are available for non-EU students.`);
    } else if (sp.regional_scholarship_available === true) {
        scholarshipScore = 80;
        explanation.push(`Regional/DSU scholarships available.`);
    } else if (sp.non_eu_eligible === false) {
        scholarshipScore = 0;
    } else if (record.Scholarships_Info && record.Scholarships_Info.length > 0) {
        // Fallback for legacy records
        scholarshipScore = 60;
        explanation.push(`Some scholarship information available (needs verification).`);
    }

    costFit = (tuitionScore * 0.7) + (semFeeScore * 0.2) + (scholarshipScore * 0.1);

    if (maxTPref && tuit > maxTPref && (!profile || !profile.strict_budget)) {
        costFit -= 30; // Soft penalty
        if (profileMatch.enabled) profileMatch.profile_penalties.push({ type: 'cost', reason: 'Tuition exceeds preferred maximum.' });
    }

    costFit = Math.min(100, Math.max(0, costFit));

    if (tuit > 10000) {
        warnings.push(`High yearly tuition (€${tuit.toFixed(0)}).`);
    } else if (tuit <= 2000) {
        explanation.push(`Very affordable tuition (€${tuit.toFixed(0)}/yr).`);
    }

    // 4. Career / Research Ecosystem (0-100)
    let careerFit = 50;
    const ecosystemStr = normalizeText([
        record.Industry_Ecosystem,
        record.Industry_Partners,
        record.Analysis_Pros,
        record.field_recognition
    ].join(' '));

    const premiumPartners = ['esa', 'dlr', 'nasa', 'jaxa', 'airbus', 'cern', 'onera', 'isae', 'estec'];
    let partnerMatches = 0;
    premiumPartners.forEach(p => {
        if (ecosystemStr.includes(p)) partnerMatches++;
    });

    careerFit += partnerMatches * 15;

    const compInt = String(record.Industry_Comp_Intensity || '').toLowerCase();
    if (compInt.includes('high')) careerFit += 10;
    if (record.Internship_Mandatory) {
        careerFit += 10;
        explanation.push(`Mandatory internship ensures industry exposure.`);
    }

    careerFit = Math.min(100, Math.max(0, careerFit));
    if (partnerMatches > 0) {
        explanation.push(`Strong aerospace/tech ecosystem (partners include major agencies/corps).`);
    }

    // 5. Living Risk (0-100)
    let livingFit = 50;
    
    const costCity = String(record.Cost_City_Living || '').toLowerCase();
    if (costCity.includes('very_high')) livingFit -= 30;
    else if (costCity.includes('high')) livingFit -= 15;
    else if (costCity.includes('low')) livingFit += 20;

    const housing = String(record.Living_Housing_Difficulty || '').toLowerCase();
    const housingTol = profile?.housing_risk_tolerance || 'medium';
    
    if (housing.includes('nightmare')) {
        if (profileMatch.enabled && housingTol === 'low') {
            livingFit -= 50;
            profileMatch.profile_penalties.push({ type: 'housing', reason: 'Nightmare housing conflicts with low risk tolerance.' });
        } else {
            livingFit -= 30;
        }
        warnings.push(`Housing market is extremely difficult (Nightmare).`);
    } else if (housing.includes('very hard')) {
        if (profileMatch.enabled && housingTol === 'low') {
            livingFit -= 40;
            profileMatch.profile_penalties.push({ type: 'housing', reason: 'Very hard housing conflicts with low risk tolerance.' });
        } else {
            livingFit -= 20;
        }
        warnings.push(`Housing market is very difficult.`);
    } else if (housing.includes('hard')) {
        livingFit -= 10;
    } else if (housing.includes('moderate') || housing.includes('easy')) {
        livingFit += 20;
        explanation.push(`Housing is relatively accessible.`);
    }

    livingFit = Math.min(100, Math.max(0, livingFit));

    // 6. Data Confidence / Deadline (0-100)
    let confFit = 80;
    if (record.Meta_Needs_Verification) {
        confFit -= 20;
        warnings.push(`Data needs manual verification.`);
    } else {
        explanation.push(`Data is verified.`);
    }

    if (record.Meta_Sources && record.Meta_Sources.length > 0) {
        confFit += 20;
    }

    confFit = Math.min(100, Math.max(0, confFit));

    // --- WEIGHTED SUM ---
    // If personalization is enabled, adjust weights slightly towards Academic Fit
    let effectiveWeights = { ...weights };
    if (profileMatch.enabled) {
        effectiveWeights.academic_fit = 35;
        effectiveWeights.eligibility_language = 20;
        effectiveWeights.cost_funding = 20;
        effectiveWeights.career_research = 15;
        effectiveWeights.living_risk = 7;
        effectiveWeights.confidence_deadline = 3;
    }

    const wTotal = (effectiveWeights.academic_fit + effectiveWeights.eligibility_language + effectiveWeights.cost_funding + effectiveWeights.career_research + effectiveWeights.living_risk + effectiveWeights.confidence_deadline) || 100;
    
    const nW = {
        ac: effectiveWeights.academic_fit / wTotal,
        el: effectiveWeights.eligibility_language / wTotal,
        co: effectiveWeights.cost_funding / wTotal,
        ca: effectiveWeights.career_research / wTotal,
        li: effectiveWeights.living_risk / wTotal,
        cf: effectiveWeights.confidence_deadline / wTotal
    };

    const finalScore = (
        (academicFit * nW.ac) +
        (eligFit * nW.el) +
        (costFit * nW.co) +
        (careerFit * nW.ca) +
        (livingFit * nW.li) +
        (confFit * nW.cf)
    );

    return {
        passed_hard_filters: passed,
        total_score: finalScore,
        components: {
            academic_fit: academicFit,
            eligibility_language: eligFit,
            cost_funding: costFit,
            career_research: careerFit,
            living_risk: livingFit,
            confidence_deadline: confFit
        },
        explanation: explanation,
        warnings: warnings,
        personalized_match: profileMatch
    };
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { calculateScore };
} else {
    window.unirankScoring = { calculateScore };
}
