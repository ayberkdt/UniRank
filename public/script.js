let rawData = [];
let filteredData = [];
let selectedCountries = new Set();
let selectedCategoryKeys = new Set();
let favorites = new Set(JSON.parse(localStorage.getItem('unirank_favorites') || '[]'));

// Global Boundaries for Normalization
let globalMaxTuition = 10000;
let globalMinTuition = 0;
let globalMaxRank = 1000;
let globalMinRank = 1;

// DOM Elements
const els = {
    countryFilter: document.getElementById('country-filter'),
    countryTags: document.getElementById('country-tags'),
    categorySearchInput: document.getElementById('categorySearchInput'),
    categorySuggestions: document.getElementById('categorySuggestions'),
    selectedCategoryChips: document.getElementById('selectedCategoryChips'),
    popularCategoryChips: document.getElementById('popularCategoryChips'),
    favFilter: document.getElementById('fav-filter'),
    searchInput: document.getElementById('search-input'),
    sortSelect: document.getElementById('sort-select'),
    hardFilters: {
        degree: document.getElementById('degree-filter'),
        englishOnly: document.getElementById('english-only-filter'),
        maxTuition: document.getElementById('max-tuition-filter')
    },
    preset: document.getElementById('preset-profile-select'),
    weights: {
        academic: document.getElementById('w-academic'),
        eligibility: document.getElementById('w-eligibility'),
        cost: document.getElementById('w-cost'),
        career: document.getElementById('w-career'),
        living: document.getElementById('w-living'),
        confidence: document.getElementById('w-confidence')
    },
    vals: {
        academic: document.getElementById('val-academic'),
        eligibility: document.getElementById('val-eligibility'),
        cost: document.getElementById('val-cost'),
        career: document.getElementById('val-career'),
        living: document.getElementById('val-living'),
        confidence: document.getElementById('val-confidence')
    },
    kpi: {
        total: document.getElementById('kpi-total'),
        tuition: document.getElementById('kpi-tuition'),
        score: document.getElementById('kpi-score')
    },
    tableBody: document.getElementById('table-body'),
    drawer: {
        overlay: document.getElementById('drawer-overlay'),
        panel: document.getElementById('detail-drawer'),
        title: document.getElementById('drawer-title'),
        body: document.getElementById('drawer-body'),
        closeBtn: document.getElementById('drawer-close'),
        favBtn: document.getElementById('drawer-fav-btn')
    }
};

function toggleFavorite(id) {
    if (favorites.has(id)) {
        favorites.delete(id);
        if (window.removeFavorite) window.removeFavorite(id);
    } else {
        favorites.add(id);
        if (window.addFavorite) window.addFavorite(id);
    }
localStorage.setItem('unirank_favorites', JSON.stringify(Array.from(favorites)));
    processAndRender();
}

// Initialize
async function init() {
    if (window.initAuth) await window.initAuth();

    if (window.currentUser) {
        const authFavs = JSON.parse(localStorage.getItem('unirank_demo_favs') || '[]');
        authFavs.forEach(id => favorites.add(id));
    }

    if (window.updateAuthUI) window.updateAuthUI();

    setupEventListeners();
    await fetchData();
    window.applyTranslations();
}

// Fetch Data
async function fetchData() {
    const loader = document.getElementById('loader');
    if (loader) loader.classList.add('active');
    try {
        const res = await fetch('/api/universities');
        const json = await res.json();
        
        if (json.status === 'success') {
            rawData = json.data;
            
            // Calculate Global Boundaries for Min-Max Normalization
            if (rawData.length > 0) {
                globalMaxTuition = Math.max(...rawData.map(r => parseFloat(r.tuition_eur_per_year) || 0));
                globalMinTuition = Math.min(...rawData.map(r => parseFloat(r.tuition_eur_per_year) || 0));
                if (globalMaxTuition === globalMinTuition) globalMaxTuition = globalMinTuition + 1; // Prevent division by zero
                
                const validRanks = rawData.map(r => r.qs_ranking).filter(r => r && r <= 1000);
                globalMaxRank = validRanks.length > 0 ? Math.max(...validRanks) : 1000;
                globalMinRank = validRanks.length > 0 ? Math.min(...validRanks) : 1;
                if (globalMaxRank === globalMinRank) globalMaxRank = globalMinRank + 1;
            }

            populateCountryFilter();
            if (window.renderCategoryUI) window.renderCategoryUI();
            
            // Pre-calculate category profiles synchronously for the UI
            for (let r of rawData) {
                if (!r.Category_Profile && typeof window.buildCategoryProfile === 'function') {
                    r.Category_Profile = await window.buildCategoryProfile(r);
                }
            }
            
            processAndRender();
        } else {
            console.error("API Error:", json.message);
            els.tableBody.innerHTML = `<tr><td colspan="7" style="text-align:center; color:var(--danger)">API Error: ${json.message}</td></tr>`;
        }
    } catch (err) {
        console.error("Fetch Error:", err);
        els.tableBody.innerHTML = `<tr><td colspan="7" style="text-align:center; color:var(--danger)">Network/Fetch Error: ${err.message}</td></tr>`;
    } finally {
        if (loader) loader.classList.remove('active');
    }
}

function setupEventListeners() {
    // Presets
    if (els.preset) {
        els.preset.addEventListener('change', (e) => {
            const p = e.target.value;
            let w = {};
            if (p === 'balanced') w = { academic: 30, eligibility: 20, cost: 20, career: 15, living: 10, confidence: 5 };
            else if (p === 'low_cost') w = { academic: 20, eligibility: 20, cost: 35, career: 10, living: 10, confidence: 5 };
            else if (p === 'best_fit') w = { academic: 45, eligibility: 15, cost: 10, career: 20, living: 5, confidence: 5 };
            else if (p === 'safe_choice') w = { academic: 25, eligibility: 35, cost: 15, career: 10, living: 10, confidence: 5 };
            else if (p === 'career') w = { academic: 25, eligibility: 15, cost: 10, career: 35, living: 10, confidence: 5 };
            
            if (p !== 'custom' && Object.keys(w).length > 0) {
                Object.keys(w).forEach(k => {
                    if (els.weights[k]) {
                        els.weights[k].value = w[k];
                        if (els.vals[k]) els.vals[k].textContent = w[k];
                    }
                });
                clearTimeout(window.renderTimeout);
                window.renderTimeout = setTimeout(processAndRender, 100);
            }
        });
    }

    // Weights
    Object.keys(els.weights).forEach(k => {
        if (els.weights[k]) {
            els.weights[k].addEventListener('input', (e) => {
                if (els.vals[k]) els.vals[k].textContent = Number(e.target.value);
                if (els.preset) els.preset.value = 'custom';
                // Debounce re-render slightly
                clearTimeout(window.renderTimeout);
                window.renderTimeout = setTimeout(processAndRender, 100);
            });
        }
    });

    // Hard Filters
    Object.keys(els.hardFilters).forEach(k => {
        if (els.hardFilters[k]) {
            els.hardFilters[k].addEventListener('change', processAndRender);
            if (els.hardFilters[k].type === 'number' || els.hardFilters[k].type === 'range') {
                els.hardFilters[k].addEventListener('input', (e) => {
                    if (k === 'maxTuition') {
                        const valDisplay = document.getElementById('tuition-val-display');
                        if (valDisplay) {
                            if (e.target.value >= 25000) {
                                valDisplay.textContent = 'Any';
                                valDisplay.style.color = 'var(--success)';
                                valDisplay.style.borderColor = 'rgba(16, 185, 129, 0.2)';
                                valDisplay.style.background = 'rgba(16, 185, 129, 0.1)';
                            } else {
                                valDisplay.textContent = `≤ €${e.target.value}`;
                                valDisplay.style.color = 'var(--text-main)';
                                valDisplay.style.borderColor = 'var(--border-color)';
                                valDisplay.style.background = 'rgba(255,255,255,0.05)';
                            }
                        }
                    }
                    clearTimeout(window.renderTimeout);
                    window.renderTimeout = setTimeout(processAndRender, 200);
                });
            }
        }
    });

    // Filters
    els.countryFilter.addEventListener('change', (e) => {
        const c = e.target.value;
        if (c && !selectedCountries.has(c)) {
            selectedCountries.add(c);
            e.target.value = '';
            renderCountryTags();
            processAndRender();
        }
    });

    // Category listener is attached inside populateCategoryTree
    
    // city filter listener removed
    els.favFilter.addEventListener('change', processAndRender);
    els.searchInput.addEventListener('input', () => {
        clearTimeout(window.searchTimeout);
        window.searchTimeout = setTimeout(processAndRender, 200);
    });
    
    // Sorting
    els.sortSelect.addEventListener('change', processAndRender);
    
    // Drawer close
    els.drawer.closeBtn.addEventListener('click', closeDrawer);
    els.drawer.overlay.addEventListener('click', closeDrawer);
}

function populateCountryFilter() {
    const countries = new Set();
    rawData.forEach(r => {
        if (r.country) countries.add(r.country);
    });
    
    const sorted = Array.from(countries).sort();
    sorted.forEach(c => {
        const opt = document.createElement('option');
        opt.value = c;
        opt.textContent = window.getCountryName ? window.getCountryName(c) : c;
        els.countryFilter.appendChild(opt);
    });
}

function renderCountryTags() {
    els.countryTags.innerHTML = '';
    selectedCountries.forEach(c => {
        const span = document.createElement('span');
        span.className = 'tag-removable';
        span.innerHTML = `${window.getCountryName ? window.getCountryName(c) : c} ✕`;
        span.onclick = () => {
            selectedCountries.delete(c);
            renderCountryTags();
            processAndRender();
        };
        els.countryTags.appendChild(span);
    });
}

// Normalize function for search
window.normalizeSearchText = function(value) {
  return String(value || "")
    .toLowerCase()
    .trim()
    .replaceAll("ı", "i")
    .replaceAll("ğ", "g")
    .replaceAll("ü", "u")
    .replaceAll("ş", "s")
    .replaceAll("ö", "o")
    .replaceAll("ç", "c");
};

// Popular categories
const POPULAR_CATEGORIES = [
    "space_systems", "gnc", "cfd", "jet_propulsion", "aerospace_structures",
    "scientific_ai", "surrogate_modeling", "digital_twin", "satellite_systems", "astrodynamics"
];

window.renderCategoryUI = async function() {
    if (!els.categorySearchInput) return;
    els.categorySearchInput.addEventListener('input', async (e) => {
        const val = e.target.value;
        if (!val) {
            els.categorySuggestions.innerHTML = '';
            return;
        }
        const taxonomy = await window.loadTaxonomy();
        const normVal = window.normalizeSearchText(val);
        const results = [];
        for (const [key, info] of Object.entries(taxonomy)) {
            let match = false;
            
            // Safe label check
            const lblEn = typeof info.label === 'object' ? info.label.en : info.label;
            const lblTr = typeof info.label === 'object' ? info.label.tr : info.label;
            
            if (window.normalizeSearchText(lblEn).includes(normVal) || window.normalizeSearchText(lblTr).includes(normVal)) match = true;
            for (const alias of info.aliases || []) {
                if (window.normalizeSearchText(alias).includes(normVal)) { match = true; break; }
            }
            if (match) {
                results.push({ key, ...info });
            }
        }
        
        els.categorySuggestions.innerHTML = '';
        if (results.length === 0) {
            els.categorySuggestions.innerHTML = `<div class="category-suggestion" style="cursor:default; opacity:0.6"><span class="category-suggestion-title">${window.t('no_category_results')}</span></div>`;
            return;
        }
        results.slice(0, 8).forEach(res => {
            const div = document.createElement('div');
            div.className = 'category-suggestion';
            div.innerHTML = `<span class="category-suggestion-title">${window.localizedValue(res.label)}</span>
                             <span class="category-suggestion-parent">${window.localizedValue(res.parent)}</span>`;
            div.onclick = () => {
                selectedCategoryKeys.add(res.key);
                els.categorySearchInput.value = '';
                els.categorySuggestions.innerHTML = '';
                renderSelectedCategories();
                processAndRender();
            };
            els.categorySuggestions.appendChild(div);
        });
    });
    renderSelectedCategories();
    renderPopularCategories();
};

async function renderSelectedCategories() {
    if (!els.selectedCategoryChips) return;
    els.selectedCategoryChips.innerHTML = '';
    const taxonomy = await window.loadTaxonomy();
    selectedCategoryKeys.forEach(key => {
        const info = taxonomy[key];
        if (!info) return;
        const btn = document.createElement('button');
        btn.className = 'selected-category-chip';
        btn.innerHTML = `<span>${window.localizedValue(info.label)}</span><span aria-hidden="true" style="margin-left:4px; font-weight:bold;">×</span>`;
        btn.onclick = () => {
            selectedCategoryKeys.delete(key);
            renderSelectedCategories();
            processAndRender();
        };
        els.selectedCategoryChips.appendChild(btn);
    });
}

async function renderPopularCategories() {
    if (!els.popularCategoryChips) return;
    els.popularCategoryChips.innerHTML = '';
    const taxonomy = await window.loadTaxonomy();
    POPULAR_CATEGORIES.forEach(key => {
        const info = taxonomy[key];
        if (!info) return;
        const btn = document.createElement('button');
        btn.className = 'popular-category-chip';
        btn.innerHTML = `<span>${window.localizedValue(info.label)}</span>`;
        btn.onclick = () => {
            selectedCategoryKeys.add(key);
            renderSelectedCategories();
            processAndRender();
        };
        els.popularCategoryChips.appendChild(btn);
    });
}
// Data Processing & Scoring
const COST_MAP = {
    'very_low': 1, 'low': 2, 'medium': 3, 'high': 4, 'very_high': 5
};

function processAndRender() {
    const city = 'All';
    const search = els.searchInput.value.toLowerCase();
    
    const showFavs = els.favFilter.checked;

    const weights = {
        academic_fit: parseFloat(els.weights.academic ? els.weights.academic.value : 30),
        eligibility_language: parseFloat(els.weights.eligibility ? els.weights.eligibility.value : 20),
        cost_funding: parseFloat(els.weights.cost ? els.weights.cost.value : 20),
        career_research: parseFloat(els.weights.career ? els.weights.career.value : 15),
        living_risk: parseFloat(els.weights.living ? els.weights.living.value : 10),
        confidence_deadline: parseFloat(els.weights.confidence ? els.weights.confidence.value : 5)
    };

    const preferences = {
        selectedCategoryKeys: Array.from(selectedCategoryKeys),
        degreeFilter: els.hardFilters.degree ? els.hardFilters.degree.value : 'All',
        onlyEnglish: els.hardFilters.englishOnly ? els.hardFilters.englishOnly.checked : false,
        maxTuition: (els.hardFilters.maxTuition && parseFloat(els.hardFilters.maxTuition.value) < 25000) ? parseFloat(els.hardFilters.maxTuition.value) : 0,
        minFieldFit: 0 // Could add UI for this later
    };

    let filtered = rawData.filter(r => {
        const rid = r.Uni_ID || r.id || r.name || r.university;
        if (showFavs && !favorites.has(rid)) return false;
        if (selectedCountries.size > 0 && !selectedCountries.has(r.country)) return false;
        
        if (search) {
            const text = `${r.name} ${r.university} ${r.tags_raw} ${r.focus} ${r.city} ${r.country} ${r.Analysis_Strong_Areas}`.toLowerCase();
            if (!text.includes(search)) return false;
        }

        // Apply new scoring model and hard filters
        const scoringResult = window.unirankScoring.calculateScore(r, preferences, weights);
        if (!scoringResult.passed_hard_filters) {
            return false; // Skip if hard filters fail
        }

        // Inject scoring result into the record
        r._score = scoringResult.total_score / 10.0; // scale 0-10 for UI compatibility
        r._scoringDetails = scoringResult;
        return true;
    });

    const sortVal = els.sortSelect.value;
    filtered.sort((a, b) => {
        if (sortVal === 'score_desc') return b._score - a._score;
        if (sortVal === 'tuition_asc') return (parseFloat(a.tuition_eur_per_year)||0) - (parseFloat(b.tuition_eur_per_year)||0);
        if (sortVal === 'cost_asc') return a._costNum - b._costNum;
        if (sortVal === 'name_asc') return (a.display_name || a.name).localeCompare(b.display_name || b.name);
        return 0;
    });

    filteredData = filtered;
    renderKPIs();
    renderTable();
}

function renderKPIs() {
    els.kpi.total.textContent = filteredData.length;
    const countriesSet = new Set();
    
    if (filteredData.length > 0) {
        let totalTuit = 0;
        let validTuitCount = 0;
        let totalScore = 0;
        
        filteredData.forEach(r => {
            if (r.country) countriesSet.add(r.country);
            const tuit = parseFloat(r.tuition_eur_per_year) || 0;
            if (tuit > 0) {
                totalTuit += tuit;
                validTuitCount++;
            }
            totalScore += r._score;
        });
        
        const avgTuition = validTuitCount > 0 ? totalTuit / validTuitCount : 0;
        const avgScore = totalScore / filteredData.length;
        
        els.kpi.tuition.textContent = `€${avgTuition.toFixed(0)}`;
        els.kpi.score.textContent = avgScore.toFixed(2);
    } else {
        els.kpi.tuition.textContent = "€0";
        els.kpi.score.textContent = "0.0";
    }
    
    const kpiCountries = document.getElementById('kpi-countries');
    if (kpiCountries) kpiCountries.textContent = countriesSet.size;
}

function renderTable() {
    els.tableBody.innerHTML = '';
    filteredData.forEach((row, i) => {
        const tr = document.createElement('tr');
        let scColor = "var(--success)";
        if (row._score < 5) scColor = "var(--danger)";
        else if (row._score < 7.5) scColor = "var(--warning)";
        
        const rid = row.Uni_ID || row.id || row.name || row.university;
        const isFav = favorites.has(rid);
        const favIcon = isFav ? '⭐' : '☆';
        
        const cleanCountry = row.country ? row.country.replace(/^[^a-zA-ZçğıöşüÇĞİÖŞÜ]+/, '').trim() : '-';
        const displayCountry = window.getCountryName ? window.getCountryName(cleanCountry) : cleanCountry;
        
        tr.innerHTML = `
            <td><span style="color:var(--text-muted); font-weight:700;">${i + 1}</span></td>
            <td class="fav-cell" style="cursor: pointer; font-size: 16px;">${favIcon}</td>
            <td>${window.localizedValue ? window.localizedValue(row.display_name || row.name) : (row.display_name || row.name)}</td>
            <td>${window.localizedValue ? window.localizedValue(row.city) || '-' : (row.city || '-')}</td>
            <td><span class="country-gradient" data-country="${cleanCountry}">${displayCountry}</span></td>
            <td><span class="score-badge" style="background: ${scColor}">${row._score.toFixed(2)}</span></td>
            <td>€${parseFloat(row.tuition_eur_per_year || 0).toFixed(0)}</td>
            <td><button class="detail-btn">${window.t ? window.t('btn_view') : 'View'} ↗</button></td>
        `;
        
        els.tableBody.appendChild(tr);
        
        tr.querySelector('.fav-cell').addEventListener('click', (e) => {
            e.stopPropagation();
            toggleFavorite(rid);
        });
        
        tr.addEventListener('click', () => openDrawer(row));
    });
}

function openDrawer(data) {
    try {
        els.drawer.title.textContent = data.display_name || data.name || data.university_name || 'Details';
        
        const rid = data.Uni_ID || data.id || data.name || data.university || data.university_name;
        const isFav = favorites.has(rid);
        els.drawer.favBtn.innerHTML = isFav ? '★' : '☆';
        els.drawer.favBtn.onclick = () => {
            toggleFavorite(rid);
            els.drawer.favBtn.innerHTML = favorites.has(rid) ? '★' : '☆';
        };

        let prosHTML = '';
        let consHTML = '';
        
        let localizedPros = window.localizedArray ? window.localizedArray(data.pros || []) : (data.pros || []);
        let localizedCons = window.localizedArray ? window.localizedArray(data.cons || []) : (data.cons || []);
        
        if (localizedPros && localizedPros.length) {
            prosHTML = localizedPros.map(p => `<li class="pro"><span class="pro-text">${p}</span></li>`).join('');
        }
        if (localizedCons && localizedCons.length) {
            consHTML = localizedCons.map(c => `<li class="con"><span class="con-text">${c}</span></li>`).join('');
        }
        
        let tagsHTML = '';
        if (data.tags && data.tags.length) {
            tagsHTML = data.tags.map(t => `<span class="tag">#${t}</span>`).join('');
        }

        const cleanCountry = data.country ? String(data.country).replace(/^[^a-zA-ZÀ-ɏ0-9]+/, '').trim() : '-';
        const displayCountry = window.getCountryName ? window.getCountryName(cleanCountry) : cleanCountry;

        const t = window.t || (k => k);
        const scoreVal = data._score ? data._score.toFixed(2) : '0.00';
        
        const explanations = (data._scoringDetails && data._scoringDetails.explanation) ? window.localizedArray(data._scoringDetails.explanation) : [];
        const warnings = (data._scoringDetails && data._scoringDetails.warnings) ? window.localizedArray(data._scoringDetails.warnings) : [];

        document.getElementById('drawer-info').innerHTML = `
            <div class="detail-section">
                <h4 class="heading-overview">${t('program_details')}</h4>
                <div class="detail-grid">
                    <div class="detail-item">
                        <label>${t('col_country')}</label>
                        <span class="country-gradient" data-country="${cleanCountry}">${displayCountry}</span>
                    </div>
                    <div class="detail-item">
                        <label>${t('col_city')}</label>
                        <span>${window.localizedValue(data.city) || '-'}</span>
                    </div>
                    <div class="detail-item">
                        <label>${t('col_score')}</label>
                        <span style="color: var(--text-highlight)">${scoreVal} / 10.0</span>
                    </div>
                    <div class="detail-item">
                        <label>${t('city_cost')}</label>
                        <span style="text-transform: capitalize">${t('risk_' + (data.cost_city_raw || 'unknown'))}</span>
                    </div>
                </div>
            </div>

            <div class="detail-section">
                <h4 class="heading-rankings">Rankings & Recognition</h4>
                <div class="detail-grid">
                    <div class="detail-item">
                        <label>QS Ranking</label>
                        <span>#${data.qs_ranking || 'N/A'}</span>
                    </div>
                    <div class="detail-item">
                        <label>Global Recognition</label>
                        <span>${window.localizedValue(data.global_recognition) || 'Unknown'}</span>
                    </div>
                    <div class="detail-item">
                        <label>Field Recognition</label>
                        <span>${window.localizedValue(data.field_recognition) || 'Unknown'}</span>
                    </div>
                </div>
            </div>

            <div class="detail-section">
                <h4 class="heading-financials">${t('cost_funding')}</h4>
                <div class="detail-grid">
                    <div class="detail-item">
                        <label>${t('semester_fee')}</label>
                        <span>€${parseFloat(data.semester_fee_eur || 0).toFixed(2)}</span>
                    </div>
                    <div class="detail-item">
                        <label>${t('yearly_tuition')}</label>
                        <span>€${parseFloat(data.tuition_eur_per_year || 0).toFixed(2)}</span>
                    </div>
                </div>
            </div>
            
            ${tagsHTML ? `
            <div class="detail-section">
                <h4 class="heading-tags">Tags</h4>
                <div class="tag-list">
                    ${tagsHTML}
                </div>
            </div>
            ` : ''}

            ${data._scoringDetails ? `
            <div class="detail-section">
                <h4 class="heading-analysis" style="color: var(--primary);">${t('why_this_score')}</h4>
                ${explanations.length > 0 ? `
                <div style="background: rgba(99, 102, 241, 0.05); padding: 16px; border-radius: 12px; border: 1px solid rgba(99, 102, 241, 0.2); margin-bottom: 12px;">
                    <ul class="pro-con-list" style="margin: 0; padding-left: 20px; color: var(--text);">
                        ${explanations.map(e => `<li style="margin-bottom: 6px;">${e}</li>`).join('')}
                    </ul>
                </div>
                ` : ''}
                ${warnings.length > 0 ? `
                <div style="background: rgba(239, 68, 68, 0.05); padding: 16px; border-radius: 12px; border: 1px solid rgba(239, 68, 68, 0.2);">
                    <ul class="pro-con-list" style="margin: 0; padding-left: 20px; color: var(--danger);">
                        ${warnings.map(w => `<li style="margin-bottom: 6px;"><strong>Warning:</strong> ${w}</li>`).join('')}
                    </ul>
                </div>
                ` : ''}
            </div>
            ` : ''}

            ${prosHTML || consHTML ? `
            <div class="detail-section">
                <h4 class="heading-analysis">Additional Notes</h4>
                <div style="display: flex; flex-direction: column; gap: 12px;">
                    ${prosHTML ? `
                    <div style="background: rgba(16, 185, 129, 0.04); padding: 24px; border-radius: 16px; border: 1px solid rgba(16, 185, 129, 0.25); box-shadow: inset 0 0 20px rgba(16, 185, 129, 0.02);">
                        <ul class="pro-con-list">${prosHTML}</ul>
                    </div>
                    ` : ''}
                    ${consHTML ? `
                    <div style="background: rgba(239, 68, 68, 0.04); padding: 24px; border-radius: 16px; border: 1px solid rgba(239, 68, 68, 0.25); box-shadow: inset 0 0 20px rgba(239, 68, 68, 0.02);">
                        <ul class="pro-con-list">${consHTML}</ul>
                    </div>
                    ` : ''}
                </div>
            </div>
            ` : ''}
            
            ${data.target_program_name ? `
            <div class="detail-section">
                <h4>Target Program</h4>
                <div class="detail-grid">
                    <div class="detail-item" style="grid-column: span 2">
                        <label>Name</label>
                        <span>${data.target_program_name}</span>
                    </div>
                    <div class="detail-item">
                        <label>Degree</label>
                        <span>${data.target_program_degree || '-'}</span>
                    </div>
                    <div class="detail-item">
                        <label>URL</label>
                        <span>${data.target_program_url ? `<a href="${data.target_program_url}" target="_blank" style="color:var(--text-highlight)">Visit Program ↗</a>` : '-'}</span>
                    </div>
                </div>
            </div>
            ` : ''}
        `;

        const ctx = document.getElementById('radarChart');
        if (ctx) {
            if (window.uniChart) {
                window.uniChart.destroy();
            }
            
            const sd = data._scoringDetails ? data._scoringDetails.components : {};
            const fitMetric = (sd.academic_fit || 0) / 10;
            const eligMetric = (sd.eligibility_language || 0) / 10;
            const costMetric = (sd.cost_funding || 0) / 10;
            const careerMetric = (sd.career_research || 0) / 10;
            const livingMetric = (sd.living_risk || 0) / 10;
            const confMetric = (sd.confidence_deadline || 0) / 10;

            window.uniChart = new Chart(ctx.getContext('2d'), {
                type: 'radar',
                data: {
                    labels: ['Academic Fit', 'Eligibility', 'Cost & Fund.', 'Career', 'Living Risk', 'Data Conf.'],
                    datasets: [{
                        data: [fitMetric, eligMetric, costMetric, careerMetric, livingMetric, confMetric],
                        backgroundColor: 'rgba(99, 102, 241, 0.25)',
                        borderColor: 'rgba(99, 102, 241, 1)',
                        pointBackgroundColor: 'rgba(139, 92, 246, 1)',
                        pointBorderColor: '#fff',
                        pointHoverBackgroundColor: '#fff',
                        pointHoverBorderColor: 'rgba(139, 92, 246, 1)'
                    }]
                },
                options: {
                    scales: {
                        r: {
                            angleLines: { color: 'rgba(255, 255, 255, 0.1)' },
                            grid: { color: 'rgba(255, 255, 255, 0.1)' },
                            pointLabels: { color: '#94a3b8', font: { family: 'Inter', size: 11 } },
                            ticks: { display: false, min: 0, max: 10 }
                        }
                    },
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    return context.raw.toFixed(2) + ' / 1.0';
                                }
                            }
                        }
                    },
                    maintainAspectRatio: false
                }
            });
        }

        els.drawer.panel.classList.add('active');
        els.drawer.overlay.classList.add('active');
    } catch (err) {
        console.error('Drawer Error:', err);
    }
}
function closeDrawer() {
    els.drawer.panel.classList.remove('active');
    els.drawer.overlay.classList.remove('active');
}

document.addEventListener('languageChanged', async () => {
    // Re-render components that depend on language
    if (rawData.length > 0) {
        els.countryFilter.innerHTML = '<option value="" data-i18n="search_country">Search country...</option>';
        
        populateCountryFilter();
        renderCountryTags();
        
        if (window.renderCategoryUI) window.renderCategoryUI();
        
        // Re-apply static translations inside dynamically updated selects
        if (window.applyTranslations) {
            // But applyTranslations triggers this event, so we just manually fix the default options.
            const allCountriesOpt = els.countryFilter.querySelector('option[value=""]');
            if (allCountriesOpt) allCountriesOpt.textContent = window.t('all_countries');
            

        }

        processAndRender();
        
        // If drawer is open, re-render it
        if (els.drawer.panel.classList.contains('active')) {
            const openId = els.drawer.title.textContent; // kinda hacky but we can just use the currently selected row or close it
            // It's safer to close drawer on language change, or we can just leave it to user
            closeDrawer();
        }
    }
});

// Start
init();



window.updateAuthUI = function() {
    const authLinks = document.getElementById('auth-links');
    const authProfile = document.getElementById('auth-profile');
    if (window.currentUser) {
        if (authLinks) authLinks.style.display = 'none';
        if (authProfile) {
            authProfile.style.display = 'flex';
            document.getElementById('auth-user-name').textContent = window.currentUser.display_name;
        }
    } else {
        if (authLinks) authLinks.style.display = 'flex';
        if (authProfile) authProfile.style.display = 'none';
    }
    
    // Update Use My Profile button state
    const useProfileBtn = document.getElementById('btn-use-profile');
    if (useProfileBtn) {
        if (window.personalizationEnabled) {
            useProfileBtn.classList.add('active');
            useProfileBtn.innerHTML = `<span class="icon">✨</span> ${window.t('profile_applied')}`;
        } else {
            useProfileBtn.classList.remove('active');
            useProfileBtn.innerHTML = `<span class="icon">⚙️</span> ${window.t('use_my_profile')}`;
        }
    }
};

window.togglePersonalization = function() {
    if (!window.currentUser) {
        window.openLoginModal();
        return;
    }
    if (!window.userProfile) {
        window.openProfileModal();
        return;
    }
    window.setPersonalization(!window.personalizationEnabled);
    window.updateAuthUI();
};
