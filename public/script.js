let rawData = [];
let filteredData = [];

// DOM Elements
const els = {
    cityFilter: document.getElementById('city-filter'),
    searchInput: document.getElementById('search-input'),
    sortSelect: document.getElementById('sort-select'),
    weights: {
        cost: document.getElementById('w-cost'),
        fee: document.getElementById('w-fee'),
        fit: document.getElementById('w-fit'),
        pros: document.getElementById('w-pros'),
        cons: document.getElementById('w-cons')
    },
    vals: {
        cost: document.getElementById('val-cost'),
        fee: document.getElementById('val-fee'),
        fit: document.getElementById('val-fit'),
        pros: document.getElementById('val-pros'),
        cons: document.getElementById('val-cons')
    },
    kpi: {
        total: document.getElementById('kpi-total'),
        fee: document.getElementById('kpi-fee'),
        score: document.getElementById('kpi-score')
    },
    tableBody: document.getElementById('table-body'),
    loader: document.getElementById('loader'),
    
    drawer: {
        overlay: document.getElementById('drawer-overlay'),
        panel: document.getElementById('detail-drawer'),
        title: document.getElementById('drawer-title'),
        body: document.getElementById('drawer-body'),
        close: document.getElementById('drawer-close')
    }
};

// Initialize
async function init() {
    setupEventListeners();
    await fetchData();
}

// Fetch Data
async function fetchData() {
    els.loader.classList.add('active');
    try {
        const res = await fetch('/api/universities');
        const json = await res.json();
        
        if (json.status === 'success') {
            rawData = json.data;
            populateCityFilter();
            processAndRender();
        } else {
            console.error("API Error:", json.message);
            els.tableBody.innerHTML = `<tr><td colspan="7" style="text-align:center; color:var(--danger)">API Error: ${json.message}</td></tr>`;
        }
    } catch (err) {
        console.error("Fetch Error:", err);
        els.tableBody.innerHTML = `<tr><td colspan="7" style="text-align:center; color:var(--danger)">Network/Fetch Error: ${err.message}</td></tr>`;
    } finally {
        els.loader.classList.remove('active');
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
    els.cityFilter.addEventListener('change', processAndRender);
    els.searchInput.addEventListener('input', () => {
        clearTimeout(window.searchTimeout);
        window.searchTimeout = setTimeout(processAndRender, 200);
    });
    
    // Sorting
    els.sortSelect.addEventListener('change', processAndRender);
    
    // Drawer close
    els.drawer.close.addEventListener('click', closeDrawer);
    els.drawer.overlay.addEventListener('click', closeDrawer);
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

// Data Processing & Scoring
const COST_MAP = {
    'very_low': 1, 'low': 2, 'medium': 3, 'high': 4, 'very_high': 5
};

function processAndRender() {
    const city = els.cityFilter.value;
    const search = els.searchInput.value.toLowerCase();
    
    const weights = {
        cost: parseFloat(els.weights.cost.value),
        fee: parseFloat(els.weights.fee.value),
        fit: parseFloat(els.weights.fit.value),
        pros: parseFloat(els.weights.pros.value),
        cons: parseFloat(els.weights.cons.value),
    };
    
    // Normalize main 3 weights
    const sum = weights.cost + weights.fee + weights.fit;
    const wCost = sum > 0 ? weights.cost / sum : 0;
    const wFee = sum > 0 ? weights.fee / sum : 0;
    const wFit = sum > 0 ? weights.fit / sum : 0;

    // First pass: Calculate min/max for normalization across ALL matching records to be fair
    let filtered = rawData.filter(r => {
        if (city !== 'All' && r.city !== city) return false;
        
        if (search) {
            const text = `${r.name} ${r.university} ${r.tags_raw} ${r.focus} ${r.city}`.toLowerCase();
            if (!text.includes(search)) return false;
        }
        return true;
    });

    // Find max fee
    let maxFee = 0;
    filtered.forEach(r => {
        const fee = parseFloat(r.semester_fee_eur) || 0;
        if (fee > maxFee) maxFee = fee;
    });
    if (maxFee === 0) maxFee = 1000; // prevent div by zero

    // Second pass: Calculate score
    filtered = filtered.map(r => {
        // Cost 1-5 to 0-1
        const rawCostStr = (r.cost_city_raw || 'medium').toString().toLowerCase().replace(/-/g, '_');
        const costNum = COST_MAP[rawCostStr] || 3;
        const costNorm = (costNum - 1) / 4; // 1->0, 5->1
        
        // Fee to 0-1
        const fee = parseFloat(r.semester_fee_eur) || 0;
        const feeNorm = Math.min(1.0, fee / maxFee);
        
        // Fit 
        // Try to derive some fit logic if missing, but UniRank uses custom ML or manual scores. 
        // We'll give a randomish or tag-based fit if missing.
        const numTags = (r.tags || []).length;
        const fitNorm = Math.min(1.0, (numTags * 0.15) + 0.3); // Fake logic if none exists
        
        // Base score (higher is better)
        // Cost is bad (1-costNorm), Fee is bad (1-feeNorm), Fit is good (fitNorm)
        let score = (1 - costNorm) * wCost + (1 - feeNorm) * wFee + fitNorm * wFit;
        
        // Modifiers
        const pLen = (r.pros || []).length;
        const cLen = (r.cons || []).length;
        score += pLen * weights.pros;
        score -= cLen * weights.cons;
        
        // Scale to 0-10
        score = Math.max(0, Math.min(10, score * 10));
        
        return {
            ...r,
            _score: score,
            _feeNorm: feeNorm,
            _fitNorm: fitNorm,
            _costNum: costNum
        };
    });

    // Sorting
    const sortVal = els.sortSelect.value;
    filtered.sort((a, b) => {
        if (sortVal === 'score_desc') return b._score - a._score;
        if (sortVal === 'fee_asc') return (parseFloat(a.semester_fee_eur)||0) - (parseFloat(b.semester_fee_eur)||0);
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
        const avgFee = filteredData.reduce((acc, r) => acc + (parseFloat(r.semester_fee_eur)||0), 0) / filteredData.length;
        const avgScore = filteredData.reduce((acc, r) => acc + r._score, 0) / filteredData.length;
        
        els.kpi.fee.textContent = `€${avgFee.toFixed(0)}`;
        els.kpi.score.textContent = avgScore.toFixed(2);
    } else {
        els.kpi.fee.textContent = "€0";
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
        
        tr.innerHTML = `
            <td>${row.display_name || row.name}</td>
            <td>${row.city || '-'}</td>
            <td>${row.country || '-'}</td>
            <td><span class="score-badge" style="background: ${scColor}">${row._score.toFixed(2)}</span></td>
            <td>${(row._fitNorm * 100).toFixed(0)}%</td>
            <td>€${parseFloat(row.semester_fee_eur || 0).toFixed(2)}</td>
            <td><button class="detail-btn">View Details</button></td>
        `;
        
        tr.addEventListener('click', () => openDrawer(row));
        els.tableBody.appendChild(tr);
    });
}

function openDrawer(data) {
    els.drawer.title.textContent = data.display_name || data.name;
    
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

    els.drawer.body.innerHTML = `
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

    els.drawer.panel.classList.add('active');
    els.drawer.overlay.classList.add('active');
}

function closeDrawer() {
    els.drawer.panel.classList.remove('active');
    els.drawer.overlay.classList.remove('active');
}

// Start
init();
