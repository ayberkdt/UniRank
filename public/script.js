let rawData = [];
let filteredData = [];
let selectedCountries = new Set();
let selectedCategoryKeys = new Set();
let favorites = new Set(JSON.parse(localStorage.getItem('unirank_favorites') || '[]'));


function validateRecordShape(record) {
  const issues = [];
  if (!window.uniDataAdapter) return issues;
  const n = window.uniDataAdapter.normalizeUniversityRecord(record);

  if (!n.universityName) issues.push("Missing university name");
  if (!n.programName) issues.push("Missing program name");
  if (!n.country) issues.push("Missing country");
  if (!n.degree) issues.push("Missing degree");
  if (!n.tuitionPerYear && !n.totalAcademicCost) issues.push("Missing tuition/cost");

  return issues;
}

// Utility Functions
function formatMoney(amount) {
    const val = parseFloat(amount);
    if (isNaN(val)) return '—';
    if (val === 0) return window.t ? window.t('free') : 'Free';
    return '€' + val.toLocaleString('en-US');
}

function escapeHtml(value) {
    return String(value ?? '')
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}

function safeUrl(value) {
    if (!value) return '';
    try {
        const parsed = new URL(String(value));
        return ['http:', 'https:'].includes(parsed.protocol) ? parsed.href : '';
    } catch {
        return '';
    }
}

function getAnnualCost(record) {
    const normalized = window.uniDataAdapter ? window.uniDataAdapter.normalizeUniversityRecord(record) : null;
    const value = normalized?.totalAcademicCost ?? normalized?.tuitionPerYear;
    const number = value === null || value === undefined || value === '' ? null : Number(value);
    return Number.isFinite(number) ? number : null;
}

function displayValue(val) {
    if (val === null || val === undefined || val === '') return '—';
    if (window.localizedField) {
        const loc = window.localizedField(val);
        return loc ? loc : '—';
    }
    return String(val);
}

function formatRiskBadge(risk) {
    if (!risk || risk === 'unknown' || risk === '—') return `<span class="risk-badge risk-unknown">Unknown</span>`;
    let r = String(risk).toLowerCase();
    
    // Clean up backend variable names if they leaked to frontend
    let displayRisk = risk;
    if (r.includes('nightmare')) {
        displayRisk = 'Nightmare';
    } else if (r.includes('house_difficulty_') || r.includes('living_housing_difficulty_')) {
        displayRisk = risk.replace(/house_difficulty_|living_housing_difficulty_/gi, '');
        displayRisk = displayRisk.charAt(0).toUpperCase() + displayRisk.slice(1);
    }
    
    const safeRisk = escapeHtml(displayRisk);
    if (r.includes('nightmare') || r.includes('high') || r.includes('hard') || r.includes('difficult')) return `<span class="risk-badge risk-high">${safeRisk}</span>`;
    if (r.includes('medium') || r.includes('moderate')) return `<span class="risk-badge risk-medium">${safeRisk}</span>`;
    if (r.includes('low') || r.includes('safe')) return `<span class="risk-badge risk-low">${safeRisk}</span>`;
    return `<span class="risk-badge risk-unknown">${safeRisk}</span>`;
}

function scoreBand(score) {
    const value = Number(score) || 0;
    if (value >= 6) return { key: 'excellent', label: window.currentLanguage === 'tr' ? 'Yüksek uyum' : 'High fit' };
    if (value >= 5.5) return { key: 'strong', label: window.currentLanguage === 'tr' ? 'İyi uyum' : 'Good fit' };
    if (value >= 5) return { key: 'moderate', label: window.currentLanguage === 'tr' ? 'Orta uyum' : 'Moderate fit' };
    return { key: 'weak', label: window.currentLanguage === 'tr' ? 'Düşük uyum' : 'Lower fit' };
}

function compactList(value) {
    if (Array.isArray(value)) return value.map(displayValue).filter(Boolean).join(', ');
    return displayValue(value);
}

function riskLabel(value) {
    if (!value || ['unknown', 'needs_verification', '—'].includes(String(value).toLowerCase())) {
        return window.t ? window.t('unknown_value') : 'Unknown';
    }
    return displayValue(value).replaceAll('_', ' ');
}

function confidenceLabel(value) {
    const normalized = ['high', 'medium', 'low'].includes(String(value).toLowerCase())
        ? String(value).toLowerCase()
        : 'unknown';
    const key = `confidence_${normalized}`;
    return {
        key: normalized,
        label: window.t ? window.t(key) : normalized
    };
}

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
            rawData.slice(0, 20).forEach((r) => {
              const issues = validateRecordShape(r);
              if (issues.length) console.warn("Record shape issues:", r.id || r.name, issues);
            });

            
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
            els.tableBody.innerHTML = `<div class="empty-results-card" role="alert"><h3>${escapeHtml(json.message || 'API request failed.')}</h3></div>`;
        }
    } catch (err) {
        console.error("Fetch Error:", err);
        els.tableBody.innerHTML = `<div class="empty-results-card" role="alert"><h3>${escapeHtml(err.message || 'Network request failed.')}</h3></div>`;
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
                            } else {
                                valDisplay.textContent = `≤ €${Number(e.target.value).toLocaleString('en-US')}`;
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
            populateCountryFilter();
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

    const filterToggle = document.getElementById('filter-toggle');
    const sidebarClose = document.getElementById('sidebar-close');
    const sidebarScrim = document.getElementById('sidebar-scrim');
    if (filterToggle) filterToggle.addEventListener('click', () => setFilterSidebar(true));
    if (sidebarClose) sidebarClose.addEventListener('click', () => setFilterSidebar(false));
    if (sidebarScrim) sidebarScrim.addEventListener('click', () => setFilterSidebar(false));

    ['clear-filters-sidebar', 'clear-active-filters'].forEach(id => {
        const button = document.getElementById(id);
        if (button) button.addEventListener('click', clearAllFilters);
    });

    document.addEventListener('keydown', event => {
        if (event.key !== 'Escape') return;
        if (els.drawer.panel.classList.contains('active')) closeDrawer();
        else setFilterSidebar(false);
    });

    window.addEventListener('resize', () => {
        if (!window.matchMedia('(max-width: 1100px)').matches) setFilterSidebar(false);
    });
    setFilterSidebar(false);
}

function setFilterSidebar(open) {
    const isOpen = Boolean(open);
    const wasOpen = document.body.classList.contains('filters-open');
    if (isOpen && !wasOpen) window.lastFilterTrigger = document.activeElement;
    document.body.classList.toggle('filters-open', isOpen);
    const toggle = document.getElementById('filter-toggle');
    if (toggle) toggle.setAttribute('aria-expanded', String(isOpen));
    const sidebar = document.getElementById('filter-sidebar');
    if (sidebar) sidebar.setAttribute('aria-hidden', String(!isOpen && window.matchMedia('(max-width: 1100px)').matches));
    if (isOpen) document.getElementById('sidebar-close')?.focus();
    else if (wasOpen && window.lastFilterTrigger instanceof HTMLElement) window.lastFilterTrigger.focus();
}

function clearAllFilters() {
    selectedCountries.clear();
    selectedCategoryKeys.clear();
    if (els.searchInput) els.searchInput.value = '';
    if (els.categorySearchInput) els.categorySearchInput.value = '';
    if (els.categorySuggestions) els.categorySuggestions.innerHTML = '';
    if (els.hardFilters.degree) els.hardFilters.degree.value = 'All';
    if (els.hardFilters.englishOnly) els.hardFilters.englishOnly.checked = false;
    if (els.hardFilters.maxTuition) els.hardFilters.maxTuition.value = '25000';
    if (els.favFilter) els.favFilter.checked = false;
    const tuitionOutput = document.getElementById('tuition-val-display');
    if (tuitionOutput) tuitionOutput.textContent = 'Any';
    populateCountryFilter();
    renderCountryTags();
    renderSelectedCategories();
    renderPopularCategories();
    processAndRender();
}

function populateCountryFilter() {
    const previousValue = els.countryFilter.value;
    els.countryFilter.innerHTML = '';
    const defOpt = document.createElement('option');
    defOpt.value = '';
    defOpt.setAttribute('data-i18n', 'search_country');
    defOpt.textContent = window.t ? window.t('search_country') : 'Search country...';
    els.countryFilter.appendChild(defOpt);

    const countries = new Set();
    rawData.forEach(r => {
        const normalized = window.uniDataAdapter ? window.uniDataAdapter.normalizeUniversityRecord(r) : null;
        const country = normalized?.country || r.country || r.Country;
        if (country && !selectedCountries.has(country)) countries.add(country);
    });
    
    const sorted = Array.from(countries).sort();
    sorted.forEach(c => {
        const opt = document.createElement('option');
        opt.value = c;
        opt.textContent = window.getCountryName ? window.getCountryName(c) : c;
        els.countryFilter.appendChild(opt);
    });
    
    if (countries.has(previousValue)) {
        els.countryFilter.value = previousValue;
    }
}

function renderCountryTags() {
    els.countryTags.innerHTML = '';
    selectedCountries.forEach(c => {
        const button = document.createElement('button');
        const label = window.getCountryName ? window.getCountryName(c) : c;
        button.type = 'button';
        button.className = 'tag-removable';
        button.innerHTML = `${escapeHtml(label)} <span aria-hidden="true">×</span>`;
        button.setAttribute('aria-label', `${label} ${window.currentLanguage === 'tr' ? 'filtresini kaldır' : 'remove filter'}`);
        button.onclick = () => {
            selectedCountries.delete(c);
            populateCountryFilter();
            renderCountryTags();
            processAndRender();
        };
        els.countryTags.appendChild(button);
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
let categorySearchBound = false;

window.renderCategoryUI = async function() {
    if (!els.categorySearchInput) return;
    if (!categorySearchBound) {
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
            const button = document.createElement('button');
            button.type = 'button';
            button.className = 'category-suggestion';
            button.innerHTML = `<span class="category-suggestion-title">${escapeHtml(window.localizedValue(res.label))}</span>
                                <span class="category-suggestion-parent">${escapeHtml(window.localizedValue(res.parent))}</span>`;
            button.onclick = () => {
                selectedCategoryKeys.add(res.key);
                els.categorySearchInput.value = '';
                els.categorySuggestions.innerHTML = '';
                renderSelectedCategories();
                renderPopularCategories();
                processAndRender();
            };
            els.categorySuggestions.appendChild(button);
        });
      });
      categorySearchBound = true;
    }
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
        btn.type = 'button';
        btn.className = 'selected-category-chip';
        btn.innerHTML = `<span>${escapeHtml(window.localizedValue(info.label))}</span><span aria-hidden="true">×</span>`;
        btn.onclick = () => {
            selectedCategoryKeys.delete(key);
            renderSelectedCategories();
            renderPopularCategories();
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
        btn.type = 'button';
        btn.className = 'popular-category-chip';
        btn.innerHTML = `<span>${escapeHtml(window.localizedValue(info.label))}</span>`;
        btn.disabled = selectedCategoryKeys.has(key);
        btn.onclick = () => {
            selectedCategoryKeys.add(key);
            renderSelectedCategories();
            renderPopularCategories();
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
    const search = window.normalizeSearchText(els.searchInput.value);
    
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
        const n = window.uniDataAdapter ? window.uniDataAdapter.normalizeUniversityRecord(r) : null;
        const rid = n?.id || r.Uni_ID || r.id || r.name || r.university;
        if (showFavs && !favorites.has(rid)) return false;
        if (selectedCountries.size > 0 && !selectedCountries.has(n?.country || r.country)) return false;
        
        if (search) {
            const text = [
                n?.universityName,
                n?.programName,
                n?.city,
                n?.country,
                n?.degree,
                n?.researchSummary,
                n?.industrySummary,
                n?.strongAreas?.join(' '),
                r.tags_raw,
                r.focus
            ].filter(Boolean).join(' ');
            if (!window.normalizeSearchText(text).includes(search)) return false;
        }

        // Apply new scoring model and hard filters
        const scoringResult = window.unirankScoring.calculateScore(r, preferences, weights);
        if (!scoringResult.passed_hard_filters) {
            return false; // Skip if hard filters fail
        }

        // Inject scoring result into the record
        r._score = scoringResult.total_score / 10.0; // scale 0-10 for UI compatibility
        r._scoringDetails = scoringResult;
        
        r._costNum = getAnnualCost(r);
        
        return true;
    });

    const sortVal = els.sortSelect.value;
    filtered.sort((a, b) => {
        if (sortVal === 'score_desc') return b._score - a._score;
        if (sortVal === 'tuition_asc' || sortVal === 'cost_asc') {
            if (a._costNum === null) return b._costNum === null ? 0 : 1;
            if (b._costNum === null) return -1;
            return a._costNum - b._costNum;
        }
        if (sortVal === 'name_asc') {
            const nameA = window.uniDataAdapter?.normalizeUniversityRecord(a)?.universityName || a.display_name || a.name || '';
            const nameB = window.uniDataAdapter?.normalizeUniversityRecord(b)?.universityName || b.display_name || b.name || '';
            return String(nameA).localeCompare(String(nameB));
        }
        return 0;
    });

    filteredData = filtered;
    // Keep the filtered collection public for map popups and other view layers.
    // The map used to read window.filteredData while this variable stayed local,
    // so clicking a map result could never open its detail drawer.
    window.filteredData = filteredData;
    renderKPIs();
    renderTable();
    renderActiveFilters();
    window.dispatchEvent(new CustomEvent('unirank:dataUpdated', { detail: { filteredData } }));
}

function renderActiveFilters() {
    const bar = document.getElementById('active-filter-bar');
    const container = document.getElementById('active-filter-chips');
    const mobileCount = document.getElementById('mobile-filter-count');
    if (!bar || !container) return;

    const filters = [];
    selectedCountries.forEach(country => {
        filters.push({
            label: window.getCountryName ? window.getCountryName(country) : country,
            remove: () => {
                selectedCountries.delete(country);
                populateCountryFilter();
                renderCountryTags();
            }
        });
    });
    selectedCategoryKeys.forEach(key => {
        filters.push({
            label: window.getCategoryLabel ? window.getCategoryLabel(key) : key,
            remove: () => {
                selectedCategoryKeys.delete(key);
                renderSelectedCategories();
                renderPopularCategories();
            }
        });
    });

    const degree = els.hardFilters.degree?.value;
    if (degree && degree !== 'All') filters.push({ label: degree, remove: () => { els.hardFilters.degree.value = 'All'; } });
    if (els.hardFilters.englishOnly?.checked) {
        filters.push({ label: window.t ? window.t('only_english') : 'English only', remove: () => { els.hardFilters.englishOnly.checked = false; } });
    }
    const maxTuition = Number(els.hardFilters.maxTuition?.value || 25000);
    if (maxTuition < 25000) {
        filters.push({
            label: `≤ €${maxTuition.toLocaleString('en-US')}`,
            remove: () => {
                els.hardFilters.maxTuition.value = '25000';
                const output = document.getElementById('tuition-val-display');
                if (output) output.textContent = 'Any';
            }
        });
    }
    if (els.favFilter?.checked) filters.push({ label: window.t ? window.t('show_favorites') : 'Favorites', remove: () => { els.favFilter.checked = false; } });
    if (els.searchInput?.value.trim()) filters.push({ label: `“${els.searchInput.value.trim()}”`, remove: () => { els.searchInput.value = ''; } });

    container.innerHTML = '';
    filters.forEach(filter => {
        const button = document.createElement('button');
        button.type = 'button';
        button.className = 'active-filter-chip';
        button.innerHTML = `<span>${escapeHtml(filter.label)}</span><span aria-hidden="true">×</span>`;
        button.addEventListener('click', () => {
            filter.remove();
            processAndRender();
        });
        container.appendChild(button);
    });

    bar.hidden = filters.length === 0;
    if (mobileCount) mobileCount.textContent = String(filters.length);
}

window.switchView = function(view) {
    const listBtn = document.getElementById('btn-view-list');
    const mapBtn = document.getElementById('btn-view-map');
    const listContainer = document.getElementById('list-view-container');
    const mapContainer = document.getElementById('map-view-container');
    const showMap = view === 'map';
    window.currentView = showMap ? 'map' : 'list';

    listBtn.classList.toggle('active', !showMap);
    mapBtn.classList.toggle('active', showMap);
    listBtn.setAttribute('aria-pressed', String(!showMap));
    mapBtn.setAttribute('aria-pressed', String(showMap));
    listContainer.hidden = showMap;
    mapContainer.hidden = !showMap;
    document.body.dataset.view = showMap ? 'map' : 'list';

    if (showMap) {
        setTimeout(() => {
            if (window.unirankMap) window.unirankMap.invalidateSize();
            window.dispatchEvent(new Event('resize'));
        }, 80);
    }
}

function renderKPIs() {
    els.kpi.total.textContent = filteredData.length;
    const countriesSet = new Set();
    let totalTuition = 0;
    let validTuitionCount = 0;
    let totalScore = 0;

    filteredData.forEach(record => {
        const normalized = window.uniDataAdapter ? window.uniDataAdapter.normalizeUniversityRecord(record) : null;
        const country = normalized?.country || record.country;
        if (country) countriesSet.add(country);
        if (record._costNum !== null) {
            totalTuition += record._costNum;
            validTuitionCount += 1;
        }
        totalScore += Number(record._score) || 0;
    });

    els.kpi.tuition.textContent = validTuitionCount
        ? formatMoney(Math.round(totalTuition / validTuitionCount))
        : '—';
    els.kpi.score.textContent = filteredData.length
        ? (totalScore / filteredData.length).toFixed(2)
        : '0.0';

    const kpiCountries = document.getElementById('kpi-countries');
    if (kpiCountries) kpiCountries.textContent = countriesSet.size;
    const costCoverage = document.getElementById('kpi-cost-coverage');
    if (costCoverage) {
        costCoverage.textContent = filteredData.length
            ? `${Math.round((validTuitionCount / filteredData.length) * 100)}%`
            : '0%';
    }
}


function renderTable() {
    els.tableBody.innerHTML = '';
    if (filteredData.length === 0) {
        const title = window.t ? window.t('no_results_title') : 'No matching programs';
        const description = window.t ? window.t('no_results_desc') : 'Try removing one or two filters.';
        const resetLabel = window.t ? window.t('reset_filters') : 'Reset filters';
        els.tableBody.innerHTML = `
            <div class="empty-results-card" role="listitem">
                <span class="empty-results-card__icon" aria-hidden="true">⌁</span>
                <h3>${escapeHtml(title)}</h3>
                <p>${escapeHtml(description)}</p>
                <button class="btn btn-primary" type="button" data-reset-results>${escapeHtml(resetLabel)}</button>
            </div>`;
        els.tableBody.querySelector('[data-reset-results]')?.addEventListener('click', clearAllFilters);
        return;
    }

    filteredData.forEach((row, i) => {
        const n = window.uniDataAdapter ? window.uniDataAdapter.normalizeUniversityRecord(row) : null;
        if (!n) return;
        const rid = n ? n.id : (row.Uni_ID || row.id || row.name || row.university);
        const isFav = favorites.has(rid);
        const cleanCountry = n.country ? n.country.replace(/^[^a-zA-ZçğıöşüÇĞİÖŞÜ]+/, '').trim() : '—';
        const displayCountry = window.getCountryName ? window.getCountryName(cleanCountry) : cleanCountry;
        const band = scoreBand(row._score);
        const confidence = confidenceLabel(n.confidenceSummary);
        const language = compactList(n.teachingLanguage) || (window.t ? window.t('unknown_value') : 'Unknown');
        const annualCost = formatMoney(n.totalAcademicCost ?? n.tuitionPerYear);
        const city = displayValue(n.city);
        const degree = displayValue(n.degree);
        const admission = n.eligibleForNonEu === true
            ? (window.currentLanguage === 'tr' ? 'AB dışı uygun' : 'Non-EU eligible')
            : n.eligibleForNonEu === false
                ? (window.currentLanguage === 'tr' ? 'AB dışı uygun değil' : 'Not Non-EU eligible')
                : riskLabel(n.admissionRisk !== 'unknown' ? n.admissionRisk : n.admissionMode);
        const housing = riskLabel(n.housingDifficulty);
        const deadline = n.deadline ? displayValue(n.deadline) : '';
        const profileMatch = row._scoringDetails?.personalized_match?.personal_field_fit;
        const university = window.localizedField(n.universityName) || (window.currentLanguage === 'tr' ? 'Üniversite adı doğrulanmalı' : 'University name needs verification');
        const program = window.localizedField(n.programName) || (window.currentLanguage === 'tr' ? 'Program adı doğrulanmalı' : 'Program name needs verification');

        const article = document.createElement('article');
        article.className = 'program-card';
        article.setAttribute('role', 'listitem');
        article.dataset.programId = rid;
        article.innerHTML = `
            <div class="program-card__rank" aria-label="Rank ${i + 1}"><span>${String(i + 1).padStart(2, '0')}</span></div>
            <div class="program-card__content">
                <div class="program-card__eyebrow">
                    <span>${escapeHtml([city, displayCountry].filter(value => value && value !== '—').join(' · ') || '—')}</span>
                    <span class="confidence-badge confidence-badge--${confidence.key}">${escapeHtml(confidence.label)}</span>
                </div>
                <h3>${escapeHtml(university)}</h3>
                <p class="program-card__program">${escapeHtml(program)}</p>
                <div class="program-card__meta">
                    <span>${escapeHtml(degree)}</span>
                    ${n.ects ? `<span>${escapeHtml(n.ects)} ECTS</span>` : ''}
                    ${n.duration ? `<span>${escapeHtml(n.duration)}</span>` : ''}
                    ${deadline ? `<span>${escapeHtml(deadline)}</span>` : ''}
                </div>
                <dl class="decision-grid">
                    <div class="decision-item decision-item--score"><dt>${escapeHtml(window.t ? window.t('technical_match') : 'Technical match')}</dt><dd><span class="fit-score fit-score--${band.key}">${Number(row._score).toFixed(1)}</span><small>${escapeHtml(band.label)}</small>${window.personalizationEnabled && Number.isFinite(profileMatch) ? `<em>${Math.round(profileMatch)}% ${escapeHtml(window.t('profile_match'))}</em>` : ''}</dd></div>
                    <div class="decision-item"><dt>${escapeHtml(window.t ? window.t('teaching_language') : 'Teaching language')}</dt><dd>${escapeHtml(language)}</dd></div>
                    <div class="decision-item"><dt>${escapeHtml(window.t ? window.t('annual_cost') : 'Annual cost')}</dt><dd>${escapeHtml(annualCost)}</dd></div>
                    <div class="decision-item"><dt>${escapeHtml(window.t ? window.t('admission_reality') : 'Admission reality')}</dt><dd>${escapeHtml(admission)}</dd></div>
                    <div class="decision-item"><dt>${escapeHtml(window.t ? window.t('housing_risk') : 'Housing risk')}</dt><dd>${escapeHtml(housing)}</dd></div>
                </dl>
            </div>
            <div class="program-card__actions">
                <button class="favorite-button${isFav ? ' is-active' : ''}" type="button" aria-pressed="${String(isFav)}" aria-label="${escapeHtml(window.t ? window.t(isFav ? 'remove_favorite' : 'add_favorite') : 'Favorite')}">${isFav ? '★' : '☆'}</button>
                <button class="detail-btn" type="button">${escapeHtml(window.t ? window.t('view_program') : 'View program')} <span aria-hidden="true">→</span></button>
            </div>`;

        article.querySelector('.favorite-button').addEventListener('click', () => {
            toggleFavorite(rid);
        });
        article.querySelector('.detail-btn').addEventListener('click', () => openDrawer(row));
        els.tableBody.appendChild(article);
    });
}



function openDrawer(data) {
    try {
        window.lastDrawerTrigger = document.activeElement;
        const n = window.uniDataAdapter ? window.uniDataAdapter.normalizeUniversityRecord(data) : null;
        if (!n) return;
        n.programUrl = safeUrl(n.programUrl);
        n.admissionUrl = safeUrl(n.admissionUrl);
        n.tuitionUrl = safeUrl(n.tuitionUrl);
        n.scholarshipUrl = safeUrl(n.scholarshipUrl);

        const t = window.t || (k => k);
        els.drawer.title.textContent = window.localizedField(n.universityName) || 'Details';
        
        const rid = n.id;
        const isFav = favorites.has(rid);
        els.drawer.favBtn.innerHTML = isFav ? '★' : '☆';
        els.drawer.favBtn.setAttribute('aria-pressed', String(isFav));
        els.drawer.favBtn.setAttribute('aria-label', window.t ? window.t(isFav ? 'remove_favorite' : 'add_favorite') : 'Favorite');
        els.drawer.favBtn.onclick = () => {
            toggleFavorite(rid);
            const nowFavorite = favorites.has(rid);
            els.drawer.favBtn.innerHTML = nowFavorite ? '★' : '☆';
            els.drawer.favBtn.setAttribute('aria-pressed', String(nowFavorite));
            els.drawer.favBtn.setAttribute('aria-label', window.t ? window.t(nowFavorite ? 'remove_favorite' : 'add_favorite') : 'Favorite');
        };

        const scoreVal = data._score ? data._score.toFixed(2) : '0.00';
        const isTurkish = window.currentLanguage === 'tr';
        const band = scoreBand(data._score);
        const confidence = confidenceLabel(n.confidenceSummary);
        const languageText = compactList(n.teachingLanguage) || (window.t ? window.t('unknown_value') : 'Unknown');
        const decisionHeroHTML = `
            <section class="drawer-decision-hero">
                <div class="drawer-decision-hero__topline">
                    <span>${escapeHtml([displayValue(n.city), window.getCountryName ? window.getCountryName(n.country) : n.country].filter(Boolean).join(' · '))}</span>
                    <span class="confidence-badge confidence-badge--${confidence.key}">${escapeHtml(confidence.label)}</span>
                </div>
                <h3>${escapeHtml(displayValue(n.programName))}</h3>
                <div class="drawer-score-line"><strong class="fit-score fit-score--${band.key}">${escapeHtml(scoreVal)}</strong><span><b>${escapeHtml(band.label)}</b><small>${escapeHtml(window.t ? window.t('technical_match') : 'Technical match')}</small></span></div>
                <dl class="drawer-decision-grid">
                    <div><dt>${escapeHtml(window.t ? window.t('teaching_language') : 'Teaching language')}</dt><dd>${escapeHtml(languageText)}</dd></div>
                    <div><dt>${escapeHtml(window.t ? window.t('annual_cost') : 'Annual cost')}</dt><dd>${escapeHtml(formatMoney(n.totalAcademicCost ?? n.tuitionPerYear))}</dd></div>
                    <div><dt>ECTS / ${escapeHtml(window.t ? window.t('degree') : 'Degree')}</dt><dd>${escapeHtml([n.ects ? `${n.ects} ECTS` : '', displayValue(n.degree)].filter(Boolean).join(' · ') || '—')}</dd></div>
                    <div><dt>${escapeHtml(window.t ? window.t('winter_deadline') : 'Deadline')}</dt><dd>${escapeHtml(n.deadline ? displayValue(n.deadline) : '—')}</dd></div>
                </dl>
                ${n.lastVerified ? `<p class="drawer-verified">${escapeHtml(window.t ? window.t('last_verified') : 'Last verified')}: ${escapeHtml(n.lastVerified)}</p>` : ''}
            </section>`;
        const verificationBanner = n.needsVerification
            ? `<div class="verification-banner warning"><strong>${isTurkish ? 'Doğrulama gerekli' : 'Verification required'}</strong><span>${isTurkish ? 'Kritik kayıt alanları resmi kaynaklarla yeniden kontrol edilmelidir.' : 'Critical record fields should be rechecked against official sources.'}</span></div>`
            : `<div class="verification-banner"><strong>${isTurkish ? 'Kaynak durumu' : 'Source status'}</strong><span>${n.sources.length ? (isTurkish ? `${n.sources.length} kaynak kaydı mevcut.` : `${n.sources.length} source record(s) available.`) : (isTurkish ? 'Kaynak kaydı sınırlı.' : 'Source evidence is limited.')}</span></div>`;

        // 2. Temel Bilgiler (Basic Info)
        const qsBadge = n.qsRanking ? `<span class="rank-badge qs-rank">QS: #${n.qsRanking}</span>` : '';
        const engBadge = n.engineeringRanking ? `<span class="rank-badge eng-rank">Müh: #${n.engineeringRanking}</span>` : '';
        
        let basicInfoHTML = `
            <div class="drawer-section premium-card">
                <div class="premium-header">
                    <span class="premium-icon">🎓</span>
                    <h4 class="premium-title">${t('overview') || 'Temel Bilgiler'}</h4>
                </div>
                <div class="premium-grid">
                    <div class="premium-item full-span">
                        <label>Ülke / Şehir</label>
                        <span class="country-gradient" data-country="${n.country}">${window.getCountryName ? window.getCountryName(n.country) : n.country} - ${displayValue(n.city)}</span>
                    </div>
                    <div class="premium-item full-span">
                        <label>Üniversite & Program</label>
                        <span class="highlight-text">${displayValue(n.universityName)} - ${displayValue(n.programName)}</span>
                    </div>
                    <div class="premium-item">
                        <label>Derece</label>
                        <span>${displayValue(n.degree)}</span>
                    </div>
                    <div class="premium-item">
                        <label>Dil Gereksinimi</label>
                        <span>${Array.isArray(n.teachingLanguage) ? n.teachingLanguage.join(', ') : displayValue(n.teachingLanguage)}</span>
                    </div>
                    ${qsBadge || engBadge ? `
                    <div class="premium-item full-span ranking-container">
                        <label>Sıralamalar</label>
                        <div class="badges-wrapper">${qsBadge}${engBadge}</div>
                    </div>` : ''}
                </div>
            </div>
        `;

        // 3. Bölüm / Araştırma Bilgileri (Department Info)
        let strongAreasHTML = '';
        if (n.strongAreas && n.strongAreas.length > 0) {
            strongAreasHTML = n.strongAreas.map(a => `<li>${window.getCategoryLabel ? window.getCategoryLabel(a) : a}</li>`).join('');
        }
        let labsHTML = '';
        if (n.labs && n.labs.length > 0) {
            labsHTML = n.labs.map(l => `<span class="lab-chip">${typeof l === 'object' ? (l.name || JSON.stringify(l)) : l}</span>`).join('');
        }
        let profsHTML = '';
        if (n.professors && n.professors.length > 0) {
            profsHTML = n.professors.map(p => `
                <div class="prof-card">
                    <span class="prof-name">${typeof p === 'object' ? p.name : p}</span>
                    ${p.focus ? `<span class="prof-focus">${p.focus}</span>` : ''}
                </div>
            `).join('');
        }

        let deptHTML = `
            <div class="drawer-section premium-card">
                <div class="premium-header">
                    <span class="premium-icon">🔬</span>
                    <h4 class="premium-title">Bölüm & Araştırma Bilgileri</h4>
                </div>
                <div class="dept-content">
                    ${strongAreasHTML ? `
                    <div class="dept-block">
                        <label>Güçlü Alanlar</label>
                        <ul class="aesthetic-list">${strongAreasHTML}</ul>
                    </div>` : ''}
                    ${labsHTML ? `
                    <div class="dept-block">
                        <label>İlgili Laboratuvarlar</label>
                        <div class="chip-container">${labsHTML}</div>
                    </div>` : ''}
                    ${profsHTML ? `
                    <div class="dept-block">
                        <label>Önemli Profesörler</label>
                        <div class="prof-grid">${profsHTML}</div>
                    </div>` : ''}
                </div>
            </div>
        `;

        // 4. Finansallar (Financials)
        let financeHTML = `
            <div class="drawer-section premium-card financial-card">
                <div class="premium-header">
                    <span class="premium-icon">💰</span>
                    <h4 class="premium-title">Finansallar</h4>
                </div>
                <div class="premium-grid">
                    <div class="premium-item">
                        <label>Yıllık Okul Ücreti (Tuition)</label>
                        <span class="finance-val tuition">${formatMoney(n.tuitionPerYear)}</span>
                    </div>
                    <div class="premium-item">
                        <label>Harç / Ek Ücret (Fee)</label>
                        <span class="finance-val fee">${formatMoney(n.semesterFee)}</span>
                    </div>
                    <div class="premium-item full-span scholarship-box">
                        <label>Burs İmkânları</label>
                        <span class="scholarship-text">${displayValue(n.scholarshipSummary)}</span>
                    </div>
                </div>
            </div>
        `;

        // 5. Şehir / Ülke Bilgileri (Living)
        let livingHTML = `
            <div class="drawer-section premium-card">
                <div class="premium-header">
                    <span class="premium-icon">🏙️</span>
                    <h4 class="premium-title">Şehir & Yaşam</h4>
                </div>
                <div class="premium-grid">
                    <div class="premium-item">
                        <label>Ortalama Konut Masrafı</label>
                        <span class="finance-val">${n.housingCost ? '€' + n.housingCost + ' / ay' : 'Bilinmiyor'}</span>
                    </div>
                    <div class="premium-item">
                        <label>Konut Bulma Zorluğu</label>
                        ${formatRiskBadge(n.housingDifficulty)}
                    </div>
                </div>
            </div>
        `;

        // 6. Avantaj ve Dezavantajlar (Pros & Cons)
        let prosHTML = '';
        let consHTML = '';
        if (n.mainStrengths && n.mainStrengths.length) {
            prosHTML = n.mainStrengths.map(p => `<li><span class="icon">✅</span> <span class="text">${window.localizedField(p)}</span></li>`).join('');
        }
        if (n.mainRisks && n.mainRisks.length) {
            consHTML = n.mainRisks.map(c => `<li><span class="icon">⚠️</span> <span class="text">${window.localizedField(c)}</span></li>`).join('');
        }

        let prosConsHTML = '';
        if (prosHTML || consHTML) {
            prosConsHTML = `
            <div class="drawer-section premium-card pros-cons-card">
                <div class="premium-header">
                    <span class="premium-icon">⚖️</span>
                    <h4 class="premium-title">Avantaj & Dezavantaj Analizi</h4>
                </div>
                <div class="pros-cons-grid">
                    ${prosHTML ? `<div class="pros-col"><h5>Artılar</h5><ul class="clean-list">${prosHTML}</ul></div>` : ''}
                    ${consHTML ? `<div class="cons-col"><h5>Eksiler</h5><ul class="clean-list">${consHTML}</ul></div>` : ''}
                </div>
            </div>`;
        }

        // 7. Linkler (Links)
        let linksHTML = `
            <div class="drawer-section links-card">
                <div class="action-buttons">
                    ${n.programUrl && n.programUrl !== '—' ? `<a href="${n.programUrl}" target="_blank" class="premium-btn main-action">Programa Git ↗</a>` : ''}
                    ${n.admissionUrl && n.admissionUrl !== '—' ? `<a href="${n.admissionUrl}" target="_blank" class="premium-btn secondary-action">Kabul Sayfası ↗</a>` : ''}
                    ${n.tuitionUrl && n.tuitionUrl !== '—' ? `<a href="${n.tuitionUrl}" target="_blank" class="premium-btn secondary-action">Okul Ücreti ↗</a>` : ''}
                    ${n.scholarshipUrl && n.scholarshipUrl !== '—' ? `<a href="${n.scholarshipUrl}" target="_blank" class="premium-btn secondary-action">Burs Sayfası ↗</a>` : ''}
                </div>
            </div>
        `;

        document.getElementById('drawer-info').innerHTML =
            decisionHeroHTML +
            verificationBanner +
            basicInfoHTML +
            deptHTML +
            financeHTML +
            livingHTML +
            prosConsHTML +
            linksHTML;

        // 1. Radar Chart Setup
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
        els.drawer.panel.setAttribute('aria-hidden', 'false');
        document.body.classList.add('drawer-open');
        els.drawer.body.scrollTop = 0;
        setTimeout(() => els.drawer.closeBtn.focus(), 40);
    } catch (err) {
        console.error('Drawer Error:', err);
    }
}
function closeDrawer() {
    els.drawer.panel.classList.remove('active');
    els.drawer.overlay.classList.remove('active');
    els.drawer.panel.setAttribute('aria-hidden', 'true');
    document.body.classList.remove('drawer-open');
    if (window.lastDrawerTrigger instanceof HTMLElement) window.lastDrawerTrigger.focus();
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

window.processAndRender = processAndRender;
window.openDrawer = openDrawer;

function startApplication() {
    init().catch((error) => {
        console.error('Application initialization failed:', error);
        const message = window.currentLanguage === 'tr'
            ? 'Uygulama başlatılamadı. Lütfen sayfayı yenileyin.'
            : 'The application could not start. Please refresh the page.';
        els.tableBody.innerHTML = `<div class="empty-results-card" role="alert"><h3>${escapeHtml(message)}</h3></div>`;
    });
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', startApplication, { once: true });
} else {
    startApplication();
}



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
