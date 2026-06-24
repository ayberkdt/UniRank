let rawData = [];
let filteredData = [];
let selectedCountries = new Set();
let excludedCountries = new Set();
let selectedKeywords = new Set();
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
    countryExcludeFilter: document.getElementById('country-exclude-filter'),
    countryExcludeTags: document.getElementById('country-exclude-tags'),
    categoryTree: document.getElementById('category-tree'),
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
    } else {
        favorites.add(id);
    }
    localStorage.setItem('unirank_favorites', JSON.stringify(Array.from(favorites)));
    processAndRender();
}

// Initialize
async function init() {
    setupEventListeners();
    await fetchData();
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
            populateCountryExcludeFilter();
            await populateCategoryTree();
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
            if (els.hardFilters[k].type === 'number') {
                els.hardFilters[k].addEventListener('input', () => {
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
    els.countryExcludeFilter.addEventListener('change', (e) => {
        const c = e.target.value;
        if (c && !excludedCountries.has(c)) {
            excludedCountries.add(c);
            e.target.value = '';
            renderCountryExcludeTags();
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
        opt.textContent = c;
        els.countryFilter.appendChild(opt);
    });
}

function renderCountryTags() {
    els.countryTags.innerHTML = '';
    selectedCountries.forEach(c => {
        const span = document.createElement('span');
        span.className = 'tag-removable';
        span.innerHTML = `${c} ✕`;
        span.onclick = () => {
            selectedCountries.delete(c);
            renderCountryTags();
            processAndRender();
        };
        els.countryTags.appendChild(span);
    });
}

function populateCountryExcludeFilter() {
    const countries = new Set();
    rawData.forEach(r => {
        if (r.country) countries.add(r.country);
    });
    
    const sorted = Array.from(countries).sort();
    sorted.forEach(c => {
        const opt = document.createElement('option');
        opt.value = c;
        opt.textContent = c;
        els.countryExcludeFilter.appendChild(opt);
    });
}

function renderCountryExcludeTags() {
    els.countryExcludeTags.innerHTML = '';
    excludedCountries.forEach(c => {
        const span = document.createElement('span');
        span.className = 'tag-removable';
        span.innerHTML = `${c} ✕`;
        span.style.background = 'rgba(239, 68, 68, 0.15)';
        span.style.color = '#fca5a5';
        span.style.borderColor = 'rgba(239, 68, 68, 0.3)';
        span.onclick = () => {
            excludedCountries.delete(c);
            renderCountryExcludeTags();
            processAndRender();
        };
        els.countryExcludeTags.appendChild(span);
    });
}

async function populateCategoryTree() {
    const taxonomy = await window.loadTaxonomy();
    const parents = {};
    for (const [id, info] of Object.entries(taxonomy)) {
        if (!parents[info.parent]) parents[info.parent] = [];
        parents[info.parent].push(info.label);
    }
    
    let html = '';
    for (const [pName, subs] of Object.entries(parents)) {
        html += `<div class="cat-parent" style="margin-bottom: 6px;">`;
        html += `<label style="font-weight: 600; display: flex; align-items: center; gap: 6px; font-size: 13px; cursor: pointer; color: var(--text-color);">
                   <input type="checkbox" value="${pName}" class="cat-checkbox p-cat"> ${pName}
                 </label>`;
        html += `<div class="cat-subs" style="margin-left: 20px; margin-top: 4px; display: flex; flex-direction: column; gap: 4px;">`;
        for (const sub of subs) {
            html += `<label style="display: flex; align-items: center; gap: 6px; font-size: 12px; color: var(--text-muted); cursor: pointer;">
                       <input type="checkbox" value="${sub}" class="cat-checkbox c-cat"> ${sub}
                     </label>`;
        }
        html += `</div></div>`;
    }
    els.categoryTree.innerHTML = html;
    
    els.categoryTree.querySelectorAll('.cat-checkbox').forEach(cb => {
        cb.addEventListener('change', (e) => {
            const val = e.target.value;
            if (e.target.checked) {
                selectedKeywords.add(val);
            } else {
                selectedKeywords.delete(val);
            }
            processAndRender();
        });
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
        selectedKeywords: Array.from(selectedKeywords),
        degreeFilter: els.hardFilters.degree ? els.hardFilters.degree.value : 'All',
        onlyEnglish: els.hardFilters.englishOnly ? els.hardFilters.englishOnly.checked : false,
        maxTuition: els.hardFilters.maxTuition ? parseFloat(els.hardFilters.maxTuition.value) : 0,
        minFieldFit: 0 // Could add UI for this later
    };

    let filtered = rawData.filter(r => {
        const rid = r.Uni_ID || r.id || r.name || r.university;
        if (showFavs && !favorites.has(rid)) return false;
        if (excludedCountries.size > 0 && excludedCountries.has(r.country)) return false;
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
    if (filteredData.length > 0) {
        const avgTuition = filteredData.reduce((acc, r) => acc + (parseFloat(r.tuition_eur_per_year)||0), 0) / filteredData.length;
        const avgScore = filteredData.reduce((acc, r) => acc + r._score, 0) / filteredData.length;
        els.kpi.tuition.textContent = `€${avgTuition.toFixed(0)}`;
        els.kpi.score.textContent = avgScore.toFixed(2);
    } else {
        els.kpi.tuition.textContent = "€0";
        els.kpi.score.textContent = "0.0";
    }
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
        
        // Clean country name (remove emojis like flags and any weird prefix symbols)
        const cleanCountry = row.country ? row.country.replace(/^[^a-zA-ZçğıöşüÇĞİÖŞÜ]+/, '').trim() : '-';
        
        tr.innerHTML = `
            <td><span style="color:var(--text-muted); font-weight:700;">${i + 1}</span></td>
            <td class="fav-cell" style="cursor: pointer; font-size: 16px;">${favIcon}</td>
            <td>${row.display_name || row.name}</td>
            <td>${row.city || '-'}</td>
            <td><span class="country-gradient" data-country="${cleanCountry}">${cleanCountry}</span></td>
            <td><span class="score-badge" style="background: ${scColor}">${row._score.toFixed(2)}</span></td>
            <td>€${parseFloat(row.tuition_eur_per_year || 0).toFixed(0)}</td>
            <td><button class="detail-btn">Details ↗</button></td>
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
    els.drawer.title.textContent = data.display_name || data.name;
    
    const rid = data.Uni_ID || data.id || data.name || data.university;
    const isFav = favorites.has(rid);
    els.drawer.favBtn.innerHTML = isFav ? '⭐' : '☆';
    els.drawer.favBtn.onclick = () => {
        toggleFavorite(rid);
        els.drawer.favBtn.innerHTML = favorites.has(rid) ? '⭐' : '☆';
    };

    // Generate Pros / Cons HTML
    let prosHTML = '';
    let consHTML = '';
    
    if (data.pros && data.pros.length) {
        prosHTML = data.pros.map(p => `<li class="pro"><span class="pro-text">${p}</span></li>`).join('');
    }
    if (data.cons && data.cons.length) {
        consHTML = data.cons.map(c => `<li class="con"><span class="con-text">${c}</span></li>`).join('');
    }
    
    // Generate Tags HTML
    let tagsHTML = '';
    if (data.tags && data.tags.length) {
        tagsHTML = data.tags.map(t => `<span class="tag">#${t}</span>`).join('');
    }

    const cleanCountry = data.country ? data.country.replace(/^[^a-zA-ZçğıöşüÇĞİÖŞÜ]+/, '').trim() : '-';

    document.getElementById('drawer-info').innerHTML = `
        <div class="detail-section">
            <h4 class="heading-overview">Overview</h4>
            <div class="detail-grid">
                <div class="detail-item">
                    <label>Country</label>
                    <span class="country-gradient" data-country="${cleanCountry}">${cleanCountry}</span>
                </div>
                <div class="detail-item">
                    <label>City</label>
                    <span>${data.city}</span>
                </div>
                <div class="detail-item">
                    <label>Score</label>
                    <span style="color: var(--text-highlight)">${data._score.toFixed(2)} / 10.0</span>
                </div>
                <div class="detail-item">
                    <label>City Cost</label>
                    <span style="text-transform: capitalize">${(data.cost_city_raw || 'Unknown').replace(/_/g, ' ')}</span>
                </div>
            </div>
        </div>

        <div class="detail-section">
            <h4 class="heading-rankings">Rankings & Recognition</h4>
            <div class="detail-grid">
                <div class="detail-item">
                    <label>QS Ranking (Global)</label>
                    <span>#${data.qs_ranking || 'N/A'}</span>
                </div>
                <div class="detail-item">
                    <label>Global Recognition</label>
                    <span>${data.global_recognition || 'Unknown'}</span>
                </div>
                <div class="detail-item">
                    <label>Field Recognition</label>
                    <span>${data.field_recognition || 'Unknown'}</span>
                </div>
            </div>
        </div>

        <div class="detail-section">
            <h4 class="heading-financials">Financials</h4>
            <div class="detail-grid">
                <div class="detail-item">
                    <label>Semester Fee</label>
                    <span>€${parseFloat(data.semester_fee_eur || 0).toFixed(2)}</span>
                </div>
                <div class="detail-item">
                    <label>Tuition (Per Year)</label>
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
            <h4 class="heading-analysis" style="color: var(--primary);">Score Explanation</h4>
            <div style="background: rgba(99, 102, 241, 0.05); padding: 16px; border-radius: 12px; border: 1px solid rgba(99, 102, 241, 0.2); margin-bottom: 12px;">
                <ul class="pro-con-list" style="margin: 0; padding-left: 20px; color: var(--text);">
                    ${data._scoringDetails.explanation.map(e => `<li style="margin-bottom: 6px;">${e}</li>`).join('')}
                </ul>
            </div>
            ${data._scoringDetails.warnings.length > 0 ? `
            <div style="background: rgba(239, 68, 68, 0.05); padding: 16px; border-radius: 12px; border: 1px solid rgba(239, 68, 68, 0.2);">
                <ul class="pro-con-list" style="margin: 0; padding-left: 20px; color: var(--danger);">
                    ${data._scoringDetails.warnings.map(w => `<li style="margin-bottom: 6px;"><strong>Warning:</strong> ${w}</li>`).join('')}
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

    // Render Chart
    const ctx = document.getElementById('radarChart');
    if (ctx) {
        if (window.uniChart) {
            window.uniChart.destroy();
        }
        
        // Calculate radar metrics out of 10 based on new scoring components
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
                                return ` Score: ${context.raw.toFixed(1)} / 10`;
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
}

function closeDrawer() {
    els.drawer.panel.classList.remove('active');
    els.drawer.overlay.classList.remove('active');
}

// Start
init();
