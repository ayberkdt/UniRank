/**
 * Profile UI Management
 */

window.openProfileModal = function() {
  const modal = document.getElementById('profile-modal');
  if (!modal) return;
  modal.style.display = 'block';
  populateProfileForm();
};

window.closeProfileModal = function() {
  const modal = document.getElementById('profile-modal');
  if (modal) modal.style.display = 'none';
};

window.openLoginModal = function() {
  const modal = document.getElementById('login-modal');
  if (!modal) return;
  modal.style.display = 'block';
  
  const demoWarning = document.getElementById('demo-auth-warning');
  if (demoWarning && window.AUTH_MODE === 'demo') {
      demoWarning.style.display = 'block';
  }
};

window.closeLoginModal = function() {
  const modal = document.getElementById('login-modal');
  if (modal) modal.style.display = 'none';
};

window.handleLoginSubmit = async function(e) {
  e.preventDefault();
  const email = document.getElementById('login-email').value;
  if (email) {
    await window.login(email, "demo-password");
    window.closeLoginModal();
    window.updateAuthUI();
  }
};

window.handleLogout = async function() {
  await window.logout();
  window.updateAuthUI();
  if (window.processAndRender) window.processAndRender();
};

function populateProfileForm() {
  if (!window.userProfile) return;
  
  const p = window.userProfile;
  
  // Background
  const targetDegree = document.getElementById('profile-target-degree');
  if (targetDegree) targetDegree.value = p.target_degree || '';
  
  // Budget
  const maxTuition = document.getElementById('profile-max-tuition');
  if (maxTuition) maxTuition.value = p.max_tuition_eur_per_year || '';
  
  const strictBudget = document.getElementById('profile-strict-budget');
  if (strictBudget) strictBudget.checked = p.strict_budget || false;
  
  // Language & Risk
  const langFilter = document.getElementById('profile-lang-filter');
  if (langFilter) langFilter.value = p.language_filter || 'any';
  
  const admissionRisk = document.getElementById('profile-admission-risk');
  if (admissionRisk) admissionRisk.value = p.admission_risk_tolerance || 'medium';

  const housingRisk = document.getElementById('profile-housing-risk');
  if (housingRisk) housingRisk.value = p.housing_risk_tolerance || 'medium';

  // Interests
  if (p.interests && Array.isArray(p.interests)) {
    // Re-render interest UI
    renderProfileInterests(p.interests);
  } else {
    renderProfileInterests([]);
  }
}

// Format: [{key: 'cfd', weight: 1.0}]
let currentInterests = [];

function renderProfileInterests(interests) {
  currentInterests = [...interests];
  const container = document.getElementById('profile-interests-list');
  if (!container) return;
  
  container.innerHTML = '';
  currentInterests.forEach((interest, index) => {
    const item = document.createElement('div');
    item.className = 'interest-item';
    
    // Label
    const label = window.INTEREST_GRAPH[interest.key] ? window.localizedValue(window.INTEREST_GRAPH[interest.key].label) : interest.key;
    
    // Weight Dropdown
    let wLabel = "Low";
    if (interest.weight >= 1.0) wLabel = window.t("core_interest");
    else if (interest.weight >= 0.8) wLabel = window.t("high_interest");
    else if (interest.weight >= 0.5) wLabel = window.t("medium_interest");
    else wLabel = window.t("low_interest");
    
    item.innerHTML = `
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 8px;">
        <span style="font-weight:600;">${label}</span>
        <button type="button" class="btn btn-sm btn-danger" onclick="window.removeProfileInterest(${index})">X</button>
      </div>
      <div style="display:flex; gap: 8px; align-items:center;">
        <input type="range" min="0.3" max="1.0" step="0.1" value="${interest.weight}" onchange="window.updateProfileInterestWeight(${index}, this.value)" style="flex:1">
        <span style="font-size:12px; min-width:80px; text-align:right;">${wLabel} (${interest.weight})</span>
      </div>
    `;
    container.appendChild(item);
  });
  
  updateRelatedFields();
}

window.addProfileInterest = function() {
  const select = document.getElementById('profile-interest-select');
  if (!select) return;
  const key = select.value;
  if (!key) return;
  
  if (!currentInterests.find(i => i.key === key)) {
    currentInterests.push({ key: key, weight: 0.8 });
    renderProfileInterests(currentInterests);
  }
  select.value = '';
};

window.removeProfileInterest = function(index) {
  currentInterests.splice(index, 1);
  renderProfileInterests(currentInterests);
};

window.updateProfileInterestWeight = function(index, val) {
  currentInterests[index].weight = parseFloat(val);
  renderProfileInterests(currentInterests);
};

function updateRelatedFields() {
  const relatedContainer = document.getElementById('profile-related-fields');
  if (!relatedContainer) return;
  
  if (currentInterests.length === 0) {
    relatedContainer.innerHTML = `<span style="font-size:12px; color:var(--text-muted);">${window.t('no_category_results')}</span>`;
    return;
  }
  
  const expanded = window.buildExpandedInterestProfile(currentInterests, window.INTEREST_GRAPH || {});
  
  // Filter out the ones directly selected by user to only show 'related'
  const selectedKeys = new Set(currentInterests.map(i => i.key));
  const related = Array.from(expanded.entries())
    .filter(([k, v]) => !selectedKeys.has(k) && v > 0.1)
    .sort((a, b) => b[1] - a[1]);
    
  if (related.length === 0) {
    relatedContainer.innerHTML = `<span style="font-size:12px; color:var(--text-muted);">None</span>`;
    return;
  }
  
  relatedContainer.innerHTML = '';
  related.forEach(([k, v]) => {
    const label = window.INTEREST_GRAPH[k] ? window.localizedValue(window.INTEREST_GRAPH[k].label) : k;
    const pct = Math.round(v * 100);
    const div = document.createElement('div');
    div.style = "display:flex; justify-content:space-between; font-size:12px; margin-bottom:4px;";
    div.innerHTML = `<span>${label}</span> <span style="color:var(--accent-primary);">${pct}%</span>`;
    
    const barWrap = document.createElement('div');
    barWrap.style = "width:100%; height:4px; background:rgba(255,255,255,0.1); border-radius:2px; margin-bottom:8px;";
    const bar = document.createElement('div');
    bar.style = `width:${pct}%; height:100%; background:var(--accent-primary); border-radius:2px;`;
    barWrap.appendChild(bar);
    
    relatedContainer.appendChild(div);
    relatedContainer.appendChild(barWrap);
  });
}

window.handleProfileSubmit = async function(e) {
  e.preventDefault();
  
  const profileData = {
    target_degree: document.getElementById('profile-target-degree')?.value,
    max_tuition_eur_per_year: parseFloat(document.getElementById('profile-max-tuition')?.value) || null,
    strict_budget: document.getElementById('profile-strict-budget')?.checked || false,
    language_filter: document.getElementById('profile-lang-filter')?.value || 'any',
    admission_risk_tolerance: document.getElementById('profile-admission-risk')?.value || 'medium',
    housing_risk_tolerance: document.getElementById('profile-housing-risk')?.value || 'medium',
    interests: currentInterests
  };
  
  await window.saveUserProfile(profileData);
  window.closeProfileModal();
  window.updateAuthUI();
};

document.addEventListener("DOMContentLoaded", () => {
  if (typeof window.populateProfileInterestOptions === 'function') {
      window.populateProfileInterestOptions();
  }
  const profileForm = document.getElementById('profile-form');
  if (profileForm) {
    profileForm.addEventListener('submit', window.handleProfileSubmit);
  }
});


window.populateProfileInterestOptions = function() {
    const select = document.getElementById('profile-interest-select');
    if (!select || !window.INTEREST_GRAPH) return;
    
    // Save current selected value if any
    const currentVal = select.value;
    
    select.innerHTML = `<option value="" disabled selected data-i18n="select_field_of_interest">${window.t ? window.t('select_field_of_interest') : 'Select a field of interest...'}</option>`;
    
    Object.entries(window.INTEREST_GRAPH).forEach(([key, data]) => {
        const opt = document.createElement('option');
        opt.value = key;
        opt.textContent = window.localizedValue ? window.localizedValue(data.label) : key;
        select.appendChild(opt);
    });
    
    if (currentVal && window.INTEREST_GRAPH[currentVal]) {
        select.value = currentVal;
    }
};
