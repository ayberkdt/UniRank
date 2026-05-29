let rawData = [];
let filteredData = [];
let selectedCountries = new Set();
let selectedKeywords = new Set();
let favorites = new Set(JSON.parse(localStorage.getItem('unirank_favorites') || '[]'));

// DOM Elements
const els = {
    countryFilter: document.getElementById('country-filter'),
    countryTags: document.getElementById('country-tags'),
    cityFilter: document.getElementById('city-filter'),
    keywordFilter: document.getElementById('keyword-filter'),
    keywordTags: document.getElementById('keyword-tags'),
    favFilter: document.getElementById('fav-filter'),
    searchInput: document.getElementById('search-input'),
    sortSelect: document.getElementById('sort-select'),
    weights: {
        cost: document.getElementById('w-cost'),
        tuition: document.getElementById('w-tuition'),
        fit: document.getElementById('w-fit'),
        pros: document.getElementById('w-pros'),
        cons: document.getElementById('w-cons')
    },
    vals: {
        cost: document.getElementById('val-cost'),
        tuition: document.getElementById('val-tuition'),
        fit: document.getElementById('val-fit'),
        pros: document.getElementById('val-pros'),
        cons: document.getElementById('val-cons')
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
            populateCountryFilter();
            populateCityFilter();
            populateKeywordFilter();
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

// Setup Listeners
function setupEventListeners() {
    // Weights
    Object.keys(els.weights).forEach(k => {
        els.weights[k].addEventListener('input', (e) => {
            els.vals[k].textContent = Number(e.target.value).toFixed(2);
            // Debounce re-render slightly
            clearTimeout(window.renderTimeout);
            window.renderTimeout = setTimeout(processAndRender, 100);
        });
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
    els.keywordFilter.addEventListener('change', (e) => {
        const k = e.target.value;
        if (k && !selectedKeywords.has(k)) {
            selectedKeywords.add(k);
            e.target.value = '';
            renderKeywordTags();
            processAndRender();
        }
    });
    els.cityFilter.addEventListener('change', processAndRender);
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

function populateCityFilter() {
    const cities = new Set();
    rawData.forEach(r => {
        if (r.city) cities.add(r.city);
    });
    
    const sorted = Array.from(cities).sort();
    sorted.forEach(c => {
        const opt = document.createElement('option');
        opt.value = c;
        opt.textContent = c;
        els.cityFilter.appendChild(opt);
    });
}

function populateKeywordFilter() {
    const keywords = new Set();
    rawData.forEach(r => {
        if (r.tags && Array.isArray(r.tags)) {
            r.tags.forEach(t => keywords.add(t));
        }
    });
    
    const sorted = Array.from(keywords).sort();
    sorted.forEach(k => {
        const opt = document.createElement('option');
        opt.value = k;
        opt.textContent = k;
        els.keywordFilter.appendChild(opt);
    });
}

function renderKeywordTags() {
    els.keywordTags.innerHTML = '';
    selectedKeywords.forEach(k => {
        const span = document.createElement('span');
        span.className = 'tag-removable';
        span.innerHTML = `#${k} ✕`;
        span.onclick = () => {
            selectedKeywords.delete(k);
            renderKeywordTags();
            processAndRender();
        };
        els.keywordTags.appendChild(span);
    });
}

// Data Processing & Scoring
const COST_MAP = {
    'very_low': 1, 'low': 2, 'medium': 3, 'high': 4, 'very_high': 5
};

function processAndRender() {
    const city = els.cityFilter.value;
    const search = els.searchInput.value.toLowerCase();
    
    const weights = {
        cost: parseFloat(els.weights.cost.value),
        tuition: parseFloat(els.weights.tuition.value),
        fit: parseFloat(els.weights.fit.value),
        pros: parseFloat(els.weights.pros.value),
        cons: parseFloat(els.weights.cons.value),
    };
    
    const wCost = weights.cost;
    const wTuition = weights.tuition;
    const wFit = weights.fit;
    const wPros = weights.pros;
    const wCons = weights.cons;
    
    const showFavs = els.favFilter.checked;

    // First pass: Calculate min/max for normalization across ALL matching records to be fair
    let filtered = rawData.filter(r => {
        const rid = r.Uni_ID || r.id || r.name || r.university;
        if (showFavs && !favorites.has(rid)) return false;
        if (selectedCountries.size > 0 && !selectedCountries.has(r.country)) return false;
        if (city !== 'All' && r.city !== city) return false;
        
        if (selectedKeywords.size > 0) {
            const rTags = r.tags || [];
            for (let sk of selectedKeywords) {
                if (!rTags.includes(sk)) return false;
            }
        }
        
        if (search) {
            const text = `${r.name} ${r.university} ${r.tags_raw} ${r.focus} ${r.city}`.toLowerCase();
            if (!text.includes(search)) return false;
        }
        return true;
    });

    // Find max tuition
    let maxTuition = 0;
    filtered.forEach(r => {
        const t = parseFloat(r.tuition_eur_per_year) || 0;
        if (t > maxTuition) maxTuition = t;
    });
    if (maxTuition === 0) maxTuition = 10000; // prevent div by zero

    // Second pass: Calculate score
    filtered = filtered.map(r => {
        // Cost 1-5 to 0-1
        const rawCostStr = (r.cost_city_raw || 'medium').toString().toLowerCase().replace(/-/g, '_');
        const costNum = COST_MAP[rawCostStr] || 3;
        const costNorm = (costNum - 1) / 4; // 1->0, 5->1
        
        // Tuition to 0-1
        const t = parseFloat(r.tuition_eur_per_year) || 0;
        const tuitionNorm = Math.min(1.0, t / maxTuition);
        
        // Fit 
        // Try to derive some fit logic if missing, but UniRank uses custom ML or manual scores. 
        // We'll give a randomish or tag-based fit if missing.
        const numTags = (r.tags || []).length;
        const fitNorm = Math.min(1.0, (numTags * 0.15) + 0.3); // Fake logic if none exists
        
        // Base score (higher is better)
        let baseScore = (1 - costNorm) * wCost + (1 - tuitionNorm) * wTuition + fitNorm * wFit;
        
        let maxPossibleBase = wCost + wTuition + wFit;
        if (maxPossibleBase === 0) maxPossibleBase = 1;
        
        let normalizedBase = baseScore / maxPossibleBase; // 0 to 1
        let score = normalizedBase * 10;
        
        // Stronger Modifiers (absolute points based on weights)
        const pLen = (r.pros || []).length;
        const cLen = (r.cons || []).length;
        score += pLen * wPros * 8; // If pros weight is high, huge bonus
        score -= cLen * wCons * 8; // If cons weight is high, huge penalty
        
        // Scale to 0-10
        score = Math.max(0, Math.min(10, score));
        
        return {
            ...r,
            _score: score,
            _tuitionNorm: tuitionNorm,
            _fitNorm: fitNorm,
            _costNum: costNum
        };
    });

    // Sorting
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
        
        // Score color logic
        let scColor = "var(--success)";
        if (row._score < 5) scColor = "var(--danger)";
        else if (row._score < 7.5) scColor = "var(--warning)";
        
        const rid = row.Uni_ID || row.id || row.name || row.university;
        const isFav = favorites.has(rid);
        const favIcon = isFav ? '⭐' : '☆';
        
        tr.innerHTML = `
            <td><span style="color:var(--text-muted); font-weight:700;">#${i + 1}</span></td>
            <td class="fav-cell" style="cursor: pointer; font-size: 16px;">${favIcon}</td>
            <td>${row.display_name || row.name}</td>
            <td>${row.city || '-'}</td>
            <td>${row.country || '-'}</td>
            <td><span class="score-badge" style="background: ${scColor}">${row._score.toFixed(2)}</span></td>
            <td>${(row._fitNorm * 100).toFixed(0)}%</td>
            <td>€${parseFloat(row.tuition_eur_per_year || 0).toFixed(0)}</td>
            <td><button class="detail-btn">View Details</button></td>
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
        prosHTML = data.pros.map(p => `<li class="pro">${p}</li>`).join('');
    }
    if (data.cons && data.cons.length) {
        consHTML = data.cons.map(c => `<li class="con">${c}</li>`).join('');
    }
    
    // Generate Tags HTML
    let tagsHTML = '';
    if (data.tags && data.tags.length) {
        tagsHTML = data.tags.map(t => `<span class="tag">#${t}</span>`).join('');
    }

    document.getElementById('drawer-info').innerHTML = `
        <div class="detail-section">
            <h4>Overview</h4>
            <div class="detail-grid">
                <div class="detail-item">
                    <label>Country</label>
                    <span>${data.country}</span>
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
            <h4>Financials</h4>
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
            <h4>Tags</h4>
            <div class="tag-list">
                ${tagsHTML}
            </div>
        </div>
        ` : ''}

        ${prosHTML || consHTML ? `
        <div class="detail-section">
            <h4>Analysis</h4>
            <div style="display: flex; flex-direction: column; gap: 16px;">
                ${prosHTML ? `
                <div style="background: rgba(16, 185, 129, 0.1); padding: 16px; border-radius: 8px;">
                    <ul class="pro-con-list">${prosHTML}</ul>
                </div>
                ` : ''}
                ${consHTML ? `
                <div style="background: rgba(239, 68, 68, 0.1); padding: 16px; border-radius: 8px;">
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
        
        // Calculate radar metrics out of 10
        const fitMetric = (data._fitNorm || 0) * 10;
        const affordabilityMetric = (1 - ((data._costNum - 1) / 4)) * 10; // Cost 5 -> 0, Cost 1 -> 10
        const tuitionMetric = (1 - (data._tuitionNorm || 0)) * 10;
        const prosMetric = Math.min(10, ((data.pros || []).length / 5) * 10);
        const consMetric = Math.max(0, 10 - ((data.cons || []).length / 3) * 10); // More cons = lower score

        window.uniChart = new Chart(ctx.getContext('2d'), {
            type: 'radar',
            data: {
                labels: ['Focus Fit', 'Affordability', 'Tuition Value', 'Pros Bonus', 'Cons Score'],
                datasets: [{
                    data: [fitMetric, affordabilityMetric, tuitionMetric, prosMetric, consMetric],
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
