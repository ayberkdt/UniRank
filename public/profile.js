/**
 * Profile UI Management
 */

let modalReturnFocus = null;

function showModal(modal, focusSelector, displayMode = 'block') {
  modalReturnFocus = document.activeElement;
  modal.style.display = displayMode;
  modal.setAttribute('aria-hidden', 'false');
  document.body.classList.add('modal-open');
  requestAnimationFrame(() => modal.querySelector(focusSelector)?.focus());
}

function hideModal(modal) {
  modal.style.display = 'none';
  modal.setAttribute('aria-hidden', 'true');
  document.body.classList.remove('modal-open');
  if (modalReturnFocus instanceof HTMLElement) modalReturnFocus.focus();
}

window.openProfileModal = function() {
  const modal = document.getElementById('profile-modal');
  if (!modal) return;
  showModal(modal, '[data-modal-close]');
  populateProfileForm();
};

window.closeProfileModal = function() {
  const modal = document.getElementById('profile-modal');
  if (modal) hideModal(modal);
};

window.openLoginModal = function() {
  const modal = document.getElementById('login-modal');
  if (!modal) return;
  showModal(modal, '#login-email', 'flex');
  
  const demoWarning = document.getElementById('demo-auth-warning');
  if (demoWarning) demoWarning.hidden = window.AUTH_MODE !== 'demo';
};

window.closeLoginModal = function() {
  const modal = document.getElementById('login-modal');
  if (modal) hideModal(modal);
};

document.addEventListener('keydown', event => {
  if (event.key !== 'Escape') return;
  const profileModal = document.getElementById('profile-modal');
  const loginModal = document.getElementById('login-modal');
  if (profileModal?.getAttribute('aria-hidden') === 'false') window.closeProfileModal();
  else if (loginModal?.getAttribute('aria-hidden') === 'false') window.closeLoginModal();
});

document.addEventListener('click', event => {
  if (event.target?.id === 'profile-modal') window.closeProfileModal();
  if (event.target?.id === 'login-modal') window.closeLoginModal();
});

window.handleLoginSubmit = async function(e) {
  e.preventDefault();
  const email = document.getElementById('login-email').value;
  if (email) {
    await window.login(email, "demo-password");
    const storedFavorites = window.uniStorage.readArray('unirank_demo_favs');
    storedFavorites.forEach((id) => favorites.add(id));
    window.closeLoginModal();
    window.updateAuthUI();
    if (window.processAndRender) window.processAndRender();
  }
};

window.handleLogout = async function() {
  await window.logout();
  window.updateAuthUI();
  if (window.processAndRender) window.processAndRender();
};

function populateProfileForm() {
  if (!window.userProfile) {
    currentInterests = [];
    renderProfileInterests([]);
    return;
  }
  
  const p = window.userProfile;
  
  // Background
  const targetDegree = document.getElementById('profile-target-degree');
  if (targetDegree) targetDegree.value = String(p.target_degree || '').toLowerCase() === 'bsc' ? 'MSc' : (p.target_degree || 'MSc');
  
  // Budget
  const maxTuition = document.getElementById('profile-max-tuition');
  if (maxTuition) maxTuition.value = p.max_tuition_eur_per_year || '';
  
  const strictBudget = document.getElementById('profile-strict-budget');
  if (strictBudget) strictBudget.checked = p.strict_budget || false;
  
  // Language & Risk
  const langFilter = document.getElementById('profile-lang-filter');
  if (langFilter) langFilter.value = p.language_filter === 'english_only' ? 'english_available' : (p.language_filter || 'any');
  
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

function normalizeInterestWeight(value, fallback = 0.8) {
  const numeric = Number(value);
  const safe = Number.isFinite(numeric) ? numeric : fallback;
  return Math.min(1, Math.max(0.3, Math.round(safe * 10) / 10));
}

function parseNonNegativeNumber(value) {
  if (value === '' || value == null) return null;
  const numeric = Number(value);
  return Number.isFinite(numeric) && numeric >= 0 ? numeric : null;
}

function interestLabel(key) {
  const graphItem = window.INTEREST_GRAPH?.[key];
  return graphItem ? window.localizedValue(graphItem.label) : String(key || '');
}

function interestWeightLabel(weight) {
  if (weight >= 1.0) return window.t('core_interest');
  if (weight >= 0.8) return window.t('high_interest');
  if (weight >= 0.5) return window.t('medium_interest');
  return window.t('low_interest');
}

function createProfileEmptyState(key) {
  const empty = document.createElement('span');
  empty.className = 'profile-empty-state';
  empty.textContent = window.t(key);
  return empty;
}

function renderProfileInterests(interests) {
  const seenKeys = new Set();
  currentInterests = (Array.isArray(interests) ? interests : [])
    .filter(interest => {
      const key = interest && String(interest.key || '').trim();
      if (!key || seenKeys.has(key)) return false;
      seenKeys.add(key);
      return true;
    })
    .map(interest => ({
      key: String(interest.key).trim(),
      weight: normalizeInterestWeight(interest.weight)
    }));
  const container = document.getElementById('profile-interests-list');
  if (!container) return;

  container.replaceChildren();
  if (!currentInterests.length) {
    container.appendChild(createProfileEmptyState('no_selected_interests'));
  }

  currentInterests.forEach((interest, index) => {
    const item = document.createElement('div');
    item.className = 'profile-interest-item';

    const label = interestLabel(interest.key);
    const header = document.createElement('div');
    header.className = 'profile-interest-item__header';
    const name = document.createElement('span');
    name.className = 'profile-interest-item__name';
    name.textContent = label;
    const remove = document.createElement('button');
    remove.type = 'button';
    remove.className = 'profile-interest-remove';
    remove.setAttribute('aria-label', `${window.t('remove_interest')}: ${label}`);
    remove.textContent = '×';
    remove.addEventListener('click', () => window.removeProfileInterest(index));
    header.append(name, remove);

    const controls = document.createElement('div');
    controls.className = 'profile-interest-item__controls';
    const range = document.createElement('input');
    range.type = 'range';
    range.min = '0.3';
    range.max = '1.0';
    range.step = '0.1';
    range.value = String(interest.weight);
    range.setAttribute('aria-label', `${window.t('interest_weight')}: ${label}`);
    const value = document.createElement('span');
    value.className = 'profile-interest-item__value';
    const updateValue = () => {
      const nextWeight = normalizeInterestWeight(range.value, interest.weight);
      currentInterests[index].weight = nextWeight;
      value.textContent = `${interestWeightLabel(nextWeight)} · ${nextWeight.toFixed(1)}`;
    };
    updateValue();
    range.addEventListener('input', () => {
      updateValue();
      updateRelatedFields();
    });
    controls.append(range, value);
    item.append(header, controls);
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
  if (!Number.isInteger(index) || index < 0 || index >= currentInterests.length) return;
  currentInterests.splice(index, 1);
  renderProfileInterests(currentInterests);
};

window.updateProfileInterestWeight = function(index, val) {
  if (!Number.isInteger(index) || index < 0 || index >= currentInterests.length) return;
  currentInterests[index].weight = normalizeInterestWeight(val, currentInterests[index].weight);
  renderProfileInterests(currentInterests);
};

function updateRelatedFields() {
  const relatedContainer = document.getElementById('profile-related-fields');
  if (!relatedContainer) return;

  relatedContainer.replaceChildren();
  if (currentInterests.length === 0) {
    relatedContainer.appendChild(createProfileEmptyState('no_related_fields'));
    return;
  }
  
  const expanded = window.buildExpandedInterestProfile(currentInterests, window.INTEREST_GRAPH || {});
  
  // Filter out the ones directly selected by user to only show 'related'
  const selectedKeys = new Set(currentInterests.map(i => i.key));
  const related = Array.from(expanded.entries())
    .filter(([k, v]) => !selectedKeys.has(k) && v > 0.1)
    .sort((a, b) => b[1] - a[1]);
    
  if (related.length === 0) {
    relatedContainer.appendChild(createProfileEmptyState('no_related_fields'));
    return;
  }

  related.forEach(([k, v]) => {
    const pct = Math.min(100, Math.max(0, Math.round(Number(v) * 100)));
    const entry = document.createElement('div');
    entry.className = 'profile-related-entry';
    const row = document.createElement('div');
    row.className = 'profile-related-row';
    const name = document.createElement('span');
    name.textContent = interestLabel(k);
    const percentage = document.createElement('strong');
    percentage.textContent = `${pct}%`;
    row.append(name, percentage);
    const track = document.createElement('div');
    track.className = 'profile-related-track';
    const fill = document.createElement('div');
    fill.className = 'profile-related-fill';
    fill.style.width = `${pct}%`;
    track.appendChild(fill);
    entry.append(row, track);
    relatedContainer.appendChild(entry);
  });
}

window.handleProfileSubmit = async function(e) {
  e.preventDefault();
  
  const profileData = {
    target_degree: document.getElementById('profile-target-degree')?.value,
    max_tuition_eur_per_year: parseNonNegativeNumber(document.getElementById('profile-max-tuition')?.value),
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

document.addEventListener('languageChanged', () => {
  window.populateProfileInterestOptions();
  renderProfileInterests(currentInterests);
});


window.populateProfileInterestOptions = function() {
    const select = document.getElementById('profile-interest-select');
    if (!select || !window.INTEREST_GRAPH) return;
    
    // Save current selected value if any
    const currentVal = select.value;
    
    select.replaceChildren();
    const placeholder = document.createElement('option');
    placeholder.value = '';
    placeholder.disabled = true;
    placeholder.selected = true;
    placeholder.textContent = window.t ? window.t('select_field_of_interest') : 'Select a field of interest...';
    select.appendChild(placeholder);
    
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
