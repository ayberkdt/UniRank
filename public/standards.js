/**
 * Loader for the categorical standards in config/standards.json.
 *
 * Every ordinal label the interface shows — housing difficulty, cost basis,
 * academic-match tier, faculty contact timing, scholarship step timing — is
 * defined once on the server.  The UI reads the definition instead of
 * hard-coding a second, drifting copy of it, so a student can always open a
 * label and see the criteria that produced it.
 */

let standardsData = null;
let standardsPromise = null;

async function loadStandards() {
  if (standardsData) return standardsData;
  if (standardsPromise) return standardsPromise;

  standardsPromise = fetch('/api/standards')
    .then((response) => response.json())
    .then((payload) => {
      standardsData = payload && payload.data ? payload.data : payload || {};
      return standardsData;
    })
    .catch(() => {
      standardsData = {};
      return standardsData;
    });

  return standardsPromise;
}

function standards() {
  return standardsData || {};
}

/** Return the housing level definition, or a safe unknown placeholder. */
function housingLevel(code) {
  const levels = standards().housing_difficulty?.levels || [];
  return levels.find((level) => level.code === code)
    || levels.find((level) => level.code === 'unknown')
    || { code: 'unknown', label: { en: 'Unknown', tr: 'Bilinmiyor' }, criteria: null };
}

function housingDimension(key) {
  return (standards().housing_difficulty?.scoring_dimensions || []).find((entry) => entry.key === key) || null;
}

function costBasis(code) {
  return (standards().cost_model?.cost_basis_values || []).find((entry) => entry.code === code) || null;
}

function costComponent(key) {
  return (standards().cost_model?.components || []).find((entry) => entry.key === key) || null;
}

function matchTier(code) {
  return (standards().academic_match?.tiers || []).find((entry) => entry.code === code) || null;
}

function matchDimension(key) {
  return (standards().academic_match?.evidence_dimensions || []).find((entry) => entry.key === key) || null;
}

function contactTiming(code) {
  return (standards().faculty_contact?.contact_timing_values || []).find((entry) => entry.code === code) || null;
}

function stepTiming(code) {
  return (standards().scholarship_playbook?.step_timing_values || []).find((entry) => entry.code === code) || null;
}

window.uniStandards = {
  load: loadStandards,
  all: standards,
  housingLevel,
  housingDimension,
  costBasis,
  costComponent,
  matchTier,
  matchDimension,
  contactTiming,
  stepTiming,
};
