let taxonomyData = null;

async function loadTaxonomy() {
    if (taxonomyData !== null) return taxonomyData;
    
    try {
        const response = await fetch('/api/taxonomy');
        taxonomyData = await response.json();
        window.CATEGORY_LABELS = Object.fromEntries(
            Object.entries(taxonomyData || {}).map(([key, value]) => [key, value?.label || {}])
        );
    } catch (e) {
        console.error("Failed to load taxonomy.json", e);
        taxonomyData = {};
    }
    return taxonomyData;
}

function normalizeText(text) {
    if (typeof text !== 'string') return "";
    text = text.toLowerCase();
    text = text.replace(/[^a-z0-9\s]/g, ' ');
    return " " + text.replace(/\s+/g, ' ').trim() + " ";
}

async function buildCategoryProfile(record) {
    const taxonomy = await loadTaxonomy();
    
    const fields = {
        'Analysis_Tags': Array.isArray(record.Analysis_Tags) ? record.Analysis_Tags : [record.Analysis_Tags || ''],
        'Analysis_Strong_Areas': record.Analysis_Strong_Areas || '',
        'Program_Name': record.Program_Name || record.target_program_name || '',
        'Industry_Ecosystem': record.Industry_Ecosystem || '',
        'Industry_Partners': record.Industry_Partners || '',
        'Analysis_Pros': Array.isArray(record.Analysis_Pros) ? record.Analysis_Pros : [record.Analysis_Pros || record.pros || ''],
        'Analysis_Cons': Array.isArray(record.Analysis_Cons) ? record.Analysis_Cons : [record.Analysis_Cons || record.cons || '']
    };
    
    const texts = {
        'tags': normalizeText(fields.Analysis_Tags.join(" ")),
        'strong_areas': normalizeText(fields.Analysis_Strong_Areas),
        'program': normalizeText(fields.Program_Name),
        'ecosystem': normalizeText(fields.Industry_Ecosystem),
        'partners': normalizeText(fields.Industry_Partners),
        'pros': normalizeText(fields.Analysis_Pros.join(" ")),
        'cons': normalizeText(fields.Analysis_Cons.join(" "))
    };
    
    const weights = {
        'tags': 4.0,
        'strong_areas': 3.0,
        'program': 3.0,
        'ecosystem': 2.0,
        'partners': 2.0,
        'pros': 1.0,
        'cons': 0.5
    };
    
    const subcategoryScores = {};
    const parentScores = {};
    const matchedSubcats = new Set();
    const normalizedTags = new Set();
    
    for (const [subcatId, subcatInfo] of Object.entries(taxonomy)) {
        const parent = typeof subcatInfo.parent === 'object' ? subcatInfo.parent.en : subcatInfo.parent;
        const label = typeof subcatInfo.label === 'object' ? subcatInfo.label.en : subcatInfo.label;
        const aliases = subcatInfo.aliases || [];
        
        let subcatScore = 0.0;
        
        for (const alias of aliases) {
            const normAlias = normalizeText(alias).trim();
            if (!normAlias) continue;
            
            if (['engineering', 'technology', 'research', 'science', 'program', 'master'].includes(normAlias)) {
                continue;
            }
            
            const aliasPattern = ` ${normAlias} `;
            
            if (normAlias === "control") {
                const contextWords = ["aerospace", "aircraft", "spacecraft", "flight", "satellite", "aero"];
                let contextFound = false;
                for (const ctx of contextWords) {
                    if (texts.tags.includes(` ${ctx} `) || texts.program.includes(` ${ctx} `) || texts.strong_areas.includes(` ${ctx} `)) {
                        contextFound = true;
                        break;
                    }
                }
                if (!contextFound) continue;
            }
            
            for (const [fieldName, textVal] of Object.entries(texts)) {
                if (textVal.includes(aliasPattern)) {
                    subcatScore += weights[fieldName];
                    normalizedTags.add(subcatId);
                }
            }
        }
        
        if (subcatScore > 0) {
            subcategoryScores[label] = (subcategoryScores[label] || 0) + subcatScore;
            parentScores[parent] = (parentScores[parent] || 0) + subcatScore;
            
            if (subcatScore >= 3.0) {
                matchedSubcats.add(label);
            }
        }
    }
    
    const MAX_SCORE = 20.0;
    const categoryScores100 = {};
    for (const [parent, score] of Object.entries(parentScores)) {
        categoryScores100[parent] = Math.min(100, Math.floor((score / MAX_SCORE) * 100));
    }
    
    const sortedParents = Object.entries(parentScores).sort((a, b) => b[1] - a[1]);
    const primaryCategories = [];
    const secondaryCategories = [];
    
    for (let i = 0; i < sortedParents.length; i++) {
        const [parent, score] = sortedParents[i];
        if (score >= 3.0) {
            if (i < 3) {
                primaryCategories.push(parent);
            } else {
                secondaryCategories.push(parent);
            }
        }
    }
    
    const sortedSubcats = Object.entries(subcategoryScores).sort((a, b) => b[1] - a[1]);
    const finalSubcats = sortedSubcats.filter(s => s[1] >= 3.0).map(s => s[0]).slice(0, 8);
    
    if (primaryCategories.length === 0) {
        primaryCategories.push("Uncategorized / Needs Review");
    }
    
    return {
        primary_categories: primaryCategories,
        secondary_categories: secondaryCategories,
        subcategories: finalSubcats,
        normalized_tags: Array.from(normalizedTags),
        category_scores: categoryScores100
    };
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { loadTaxonomy, buildCategoryProfile };
}
