/**
 * UniRank Scoring Engine (JS)
 * Centralized multi-dimensional scoring logic.
 */

function normalizeText(text) {
    if (!text) return "";
    return String(text).toLowerCase().replace(/[^a-z0-9\s]/g, ' ');
}

// In the browser context, buildCategoryProfile is expected to be available globally (loaded from taxonomy.js).

function calculateScore(record, preferences, weights) {
    const explanation = [];
    const warnings = [];

    // --- HARD FILTERS ---
    let passed = true;

    // 1. Degree Filter
    const targetDegree = preferences.degreeFilter || 'All';
    const recDegree = String(record.Program_Degree || record.program_degree || '').toLowerCase();
    if (targetDegree !== 'All' && recDegree) {
        if (!recDegree.includes(targetDegree.toLowerCase())) {
            passed = false;
        }
    }

    // 2. English Only Filter
    const langReq = String(record.Admission_Language_Req || record.admission_language_req || '').toLowerCase();
    if (preferences.onlyEnglish) {
        if (langReq.includes('german') || langReq.includes('french') || langReq.includes('dutch') || langReq.includes('b1') || langReq.includes('c1') && !langReq.includes('english c1')) {
            // Very simplistic check: if it mentions german/french/dutch, it might require it.
            // If it explicitly says "English C1 / German A2", it requires German.
            if (langReq.includes('german') || langReq.includes('french') || langReq.includes('dutch')) {
                passed = false;
            }
        }
    }

    // 3. Max Tuition
    const tuit = parseFloat(record.tuition_eur_per_year) || 0;
    if (preferences.maxTuition && preferences.maxTuition > 0) {
        if (tuit > preferences.maxTuition) {
            passed = false;
        }
    }

    // 4. Closed Deadline (Simplified check: if closed, drop it if preference is set)
    // Note: Date parsing can be tricky, this assumes if a deadline passed, we filter it.
    // For now, we'll skip complex date parsing for hard filter unless requested.

    // --- SCORE COMPONENTS ---

    // Ensure we have a category profile
    let catProfile = record.Category_Profile;
    if (!catProfile) {
        catProfile = { category_scores: {}, subcategories: [], normalized_tags: [] };
    }

    // 1. Academic / Field Fit (0-100)
    let academicFit = 0;
    const selectedCats = preferences.selectedCategoryKeys || preferences.selectedKeywords || [];
    
    if (selectedCats.length === 0) {
        academicFit = 50; // Default if no preference
    } else {
        let scoreSum = 0;
        let matches = 0;
        
        for (const cat of selectedCats) {
            // Is it a top category?
            if (catProfile.category_scores[cat] !== undefined) {
                const catScore = catProfile.category_scores[cat];
                scoreSum += catScore;
                if (catScore >= 30) matches++;
            }
            // Is it a subcategory?
            else if (catProfile.subcategories.includes(cat)) {
                scoreSum += 100;
                matches++;
            }
            else if (catProfile.normalized_tags.includes(cat)) {
                scoreSum += 60;
                matches++;
            }
        }
        
        if (selectedCats.length > 0) {
            academicFit = scoreSum / selectedCats.length;
        }
        
        academicFit = Math.min(100, Math.max(0, academicFit));
        
        if (academicFit >= 80) {
            explanation.push("Strong academic match for your selected fields.");
        } else if (academicFit >= 40) {
            explanation.push("Partial academic match for your selected fields.");
        } else {
            explanation.push("No strong match found for your selected fields.");
        }
    }

    if (preferences.minFieldFit && academicFit < preferences.minFieldFit) {
        passed = false;
    }


    // 2. Eligibility & Language Fit (0-100)
    let eligFit = 70; // Baseline
    const adMode = String(record.Admission_Mode || '').toLowerCase();
    
    if (langReq.includes('english')) {
        eligFit += 10;
        if (!langReq.includes('german') && !langReq.includes('french') && !langReq.includes('dutch')) {
            eligFit += 10; // purely English
            explanation.push(`Program is fully English-taught.`);
        } else {
            eligFit -= 20; // requires additional language
            warnings.push(`Requires an additional language (${langReq}).`);
        }
    }
    
    if (adMode.includes('direct')) {
        eligFit += 20;
        explanation.push(`Direct admission offers lower entry risk.`);
    } else if (adMode.includes('aptitude test') || adMode.includes('committee') || adMode.includes('portfolio') || adMode.includes('interview')) {
        eligFit -= 20;
        warnings.push(`Competitive admission process (${adMode}).`);
    }

    eligFit = Math.min(100, Math.max(0, eligFit));


    // 3. Cost & Funding (0-100)
    let costFit = 0;
    const maxT = 20000; // Expected max tuition boundary for scoring
    const tuitionNorm = Math.min(1.0, tuit / maxT);
    let tuitionScore = (1.0 - tuitionNorm) * 100; // 0 tuition = 100 score, 20k tuition = 0 score
    
    const semFee = parseFloat(record.semester_fee_eur) || 0;
    const semFeeNorm = Math.min(1.0, semFee / 1000);
    let semFeeScore = (1.0 - semFeeNorm) * 100;

    let scholarshipScore = 0;
    if (record.Scholarships_Info && record.Scholarships_Info.length > 0) {
        scholarshipScore = 100;
        explanation.push(`Scholarships are available for non-EU students.`);
    }

    costFit = (tuitionScore * 0.7) + (semFeeScore * 0.2) + (scholarshipScore * 0.1);
    costFit = Math.min(100, Math.max(0, costFit));

    if (tuit > 10000) {
        warnings.push(`High yearly tuition (€${tuit.toFixed(0)}).`);
    } else if (tuit <= 2000) {
        explanation.push(`Very affordable tuition (€${tuit.toFixed(0)}/yr).`);
    }


    // 4. Career / Research Ecosystem (0-100)
    let careerFit = 50; // Baseline
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
    let livingFit = 50; // Baseline
    
    const costCity = String(record.Cost_City_Living || '').toLowerCase();
    if (costCity.includes('very_high')) livingFit -= 30;
    else if (costCity.includes('high')) livingFit -= 15;
    else if (costCity.includes('low')) livingFit += 20;

    const housing = String(record.Living_Housing_Difficulty || '').toLowerCase();
    if (housing.includes('nightmare')) {
        livingFit -= 30;
        warnings.push(`Housing market is extremely difficult (Nightmare).`);
    } else if (housing.includes('very hard')) {
        livingFit -= 20;
        warnings.push(`Housing market is very difficult.`);
    } else if (housing.includes('hard')) {
        livingFit -= 10;
    } else if (housing.includes('moderate') || housing.includes('easy')) {
        livingFit += 20;
        explanation.push(`Housing is relatively accessible.`);
    }

    livingFit = Math.min(100, Math.max(0, livingFit));


    // 6. Data Confidence / Deadline (0-100)
    let confFit = 80; // Baseline
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
    // Normalize weights if they don't sum to 100
    const wTotal = (weights.academic_fit + weights.eligibility_language + weights.cost_funding + weights.career_research + weights.living_risk + weights.confidence_deadline) || 100;
    
    const nW = {
        ac: weights.academic_fit / wTotal,
        el: weights.eligibility_language / wTotal,
        co: weights.cost_funding / wTotal,
        ca: weights.career_research / wTotal,
        li: weights.living_risk / wTotal,
        cf: weights.confidence_deadline / wTotal
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
        warnings: warnings
    };
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { calculateScore };
} else {
    window.unirankScoring = { calculateScore };
}
