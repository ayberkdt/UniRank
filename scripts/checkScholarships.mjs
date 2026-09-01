import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const catalogPath = path.join(root, 'scholarships', 'catalog.json');
const pagePath = path.join(root, 'public', 'scholarships.html');
const clientPath = path.join(root, 'public', 'scholarships.js');
const errors = [];

const catalog = JSON.parse(fs.readFileSync(catalogPath, 'utf8'));
const page = fs.readFileSync(pagePath, 'utf8');
const client = fs.readFileSync(clientPath, 'utf8');
const ids = new Set();
const validAccess = new Set(['ok', 'redirects', 'pdf', 'requires_js', 'blocked']);

function assert(condition, message) {
  if (!condition) errors.push(message);
}

function bilingual(value, field) {
  assert(value && typeof value.en === 'string' && value.en.trim(), `${field} is missing English text`);
  assert(value && typeof value.tr === 'string' && value.tr.trim(), `${field} is missing Turkish text`);
}

assert(catalog.schema_version === '1.0.0', 'Unexpected scholarship schema version');
assert(/^\d{4}-\d{2}-\d{2}$/.test(catalog.last_verified), 'Catalog last_verified must be ISO date');
assert(Array.isArray(catalog.scholarships) && catalog.scholarships.length >= 8, 'At least eight researched scholarship routes are required');
bilingual(catalog.research_policy, 'research_policy');

for (const item of catalog.scholarships) {
  assert(item.id && !ids.has(item.id), `Missing or duplicate scholarship id: ${item.id}`);
  ids.add(item.id);
  bilingual(item.name, `${item.id}.name`);
  bilingual(item.provider, `${item.id}.provider`);
  bilingual(item.destination, `${item.id}.destination`);
  assert(item.destination?.flag, `${item.id} has no destination flag`);
  assert(Array.isArray(item.levels) && item.levels.length, `${item.id} has no study level`);
  assert(item.cycle?.academic_year === '2027/2028', `${item.id} is not explicitly modelled for 2027/2028`);
  assert(item.source_profile?.last_verified === catalog.last_verified, `${item.id} last_verified differs from catalog`);
  assert(['high', 'medium', 'low', 'unknown'].includes(item.source_profile?.confidence), `${item.id} has invalid confidence`);
  assert(Array.isArray(item.source_profile?.sources) && item.source_profile.sources.length, `${item.id} has no official source`);
  assert(Array.isArray(item.coverage) && item.coverage.length, `${item.id} has no coverage data`);

  // What applying costs is a decision field: each route must state it, in both
  // languages, and back a definite answer with a source that covers it.
  const cost = item.application_cost;
  assert(cost && cost.scholarship_application, `${item.id} has no application_cost block`);
  if (cost?.scholarship_application) {
    assert(['free', 'not_published', 'unknown'].includes(cost.scholarship_application.status),
      `${item.id} application_cost has an invalid status`);
    bilingual(cost.scholarship_application.note, `${item.id}.application_cost.scholarship_application.note`);
    if (cost.scholarship_application.status !== 'unknown') {
      const covered = item.source_profile.sources.some((source) => (source.relevant_fields || []).includes('application_cost'));
      assert(covered, `${item.id} states an application cost without a source covering application_cost`);
    }
  }
  if (cost?.university_step) bilingual(cost.university_step.note, `${item.id}.application_cost.university_step.note`);
  assert(Array.isArray(item.requirements) && item.requirements.length, `${item.id} has no requirements data`);

  for (const [index, source] of item.source_profile.sources.entries()) {
    assert(/^https:\/\//.test(source.url || ''), `${item.id} source ${index + 1} is not HTTPS`);
    assert(validAccess.has(source.access_status), `${item.id} source ${index + 1} has invalid access_status`);
    // Sources keep the date they were actually read on; a research pass that
    // adds one route must not claim it re-checked every older page the same
    // day. A source may only never postdate the catalogue stamp.
    assert(/^\d{4}-\d{2}-\d{2}$/.test(source.last_checked || '') && source.last_checked <= catalog.last_verified,
      `${item.id} source ${index + 1} has an invalid or future last_checked date`);
    assert(source.source_type?.startsWith('official_'), `${item.id} source ${index + 1} is not classified as official`);
    assert(Array.isArray(source.relevant_fields) && source.relevant_fields.length, `${item.id} source ${index + 1} has no relevant_fields`);
  }

  if (['awaiting_publication', 'programme_calls_pending'].includes(item.cycle.status)) {
    assert(item.cycle.deadline == null, `${item.id} must not present an unverified current deadline`);
  }
  if (item.cycle.reference_deadline) {
    assert(item.cycle.reference_academic_year, `${item.id} reference deadline needs a reference academic year`);
    assert(item.cycle.deadline == null, `${item.id} cannot expose reference and current deadlines together`);
  }
}

const chevening = catalog.scholarships.find((item) => item.id === 'chevening-turkiye-2027');
assert(chevening?.cycle.deadline === '2026-10-06' && chevening?.cycle.status === 'open', 'Chevening 2027/28 confirmed deadline contract changed');
const fulbright = catalog.scholarships.find((item) => item.id === 'fulbright-turkiye-masters-2027');
assert(fulbright?.cycle.deadline === '2026-04-10' && fulbright?.cycle.status === 'closed_current_cycle', 'Fulbright 2027/28 closed-cycle contract changed');
assert(catalog.common_mismatches?.some((item) => item.id === 'turkiye-scholarships-citizenship-exclusion'), 'Türkiye Scholarships citizenship mismatch is missing');

for (const id of ['funding-next', 'funding-calendar-track', 'scholarship-search', 'scholarship-grid', 'mismatch-grid']) {
  assert(page.includes(`id="${id}"`), `Scholarship page contract #${id} is missing`);
  assert(client.includes(`#${id}`), `Scholarship client does not bind #${id}`);
}
assert(client.includes('/api/scholarships'), 'Scholarship client does not use the catalog API');
assert(client.includes('previousCycleWarning'), 'Previous-cycle warning contract is missing');

if (errors.length) {
  console.error(`Scholarship checks failed (${errors.length}):`);
  errors.forEach((error) => console.error(`- ${error}`));
  process.exit(1);
}

const sourceCount = catalog.scholarships.reduce((sum, item) => sum + item.source_profile.sources.length, 0);
console.log(`Scholarship checks passed: ${catalog.scholarships.length} routes, ${sourceCount} official sources, ${catalog.common_mismatches.length} mismatch warnings.`);
