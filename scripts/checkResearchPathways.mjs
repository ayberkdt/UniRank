import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import vm from 'node:vm';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const catalog = JSON.parse(fs.readFileSync(path.join(root, 'research_fields', 'catalog.json'), 'utf8'));
const taxonomy = JSON.parse(fs.readFileSync(path.join(root, 'data_base', 'taxonomy.json'), 'utf8'));
const america = JSON.parse(fs.readFileSync(path.join(root, 'data_base', 'amerika.json'), 'utf8'));
const netherlands = JSON.parse(fs.readFileSync(path.join(root, 'data_base', 'hollanda.json'), 'utf8'));
const page = fs.readFileSync(path.join(root, 'public', 'research.html'), 'utf8');
const client = fs.readFileSync(path.join(root, 'public', 'research.js'), 'utf8');
const api = fs.readFileSync(path.join(root, 'api', 'index.py'), 'utf8');
const devServer = fs.readFileSync(path.join(root, 'scripts', 'devServer.mjs'), 'utf8');
const adapterCode = fs.readFileSync(path.join(root, 'public', 'dataAdapter.js'), 'utf8');
const errors = [];
const validAccess = new Set(['ok', 'redirects', 'pdf', 'requires_js', 'blocked']);

function assert(condition, message) {
  if (!condition) errors.push(message);
}

function bilingual(value, field) {
  assert(value && typeof value.en === 'string' && value.en.trim(), `${field} is missing English text`);
  assert(value && typeof value.tr === 'string' && value.tr.trim(), `${field} is missing Turkish text`);
}

function flattenRecords(payload) {
  if (Array.isArray(payload)) return payload;
  if (Array.isArray(payload.universities)) return payload.universities;
  if (Array.isArray(payload.programs)) return payload.programs;
  if (Array.isArray(payload.data)) return payload.data;
  return [];
}

assert(catalog.schema_version === '1.0.0', 'Unexpected research catalog schema version');
assert(/^\d{4}-\d{2}-\d{2}$/.test(catalog.last_verified), 'Research catalog last_verified must be an ISO date');
bilingual(catalog.scope, 'scope');
assert(catalog.canonical_fields.length === 6, 'Canonical research field count must remain six');
assert(catalog.strong_programmes.length >= 6, 'At least six evidence-backed programmes are required');
assert(catalog.advisor_guides.length >= 2, 'MIT and TU Delft advisor guides are required');

const fieldIds = new Set();
for (const field of catalog.canonical_fields) {
  assert(field.id && !fieldIds.has(field.id), `Missing or duplicate field id: ${field.id}`);
  fieldIds.add(field.id);
  bilingual(field.label, `${field.id}.label`);
  bilingual(field.short_label, `${field.id}.short_label`);
  bilingual(field.definition, `${field.id}.definition`);
  assert(Array.isArray(field.includes) && field.includes.length >= 3, `${field.id} needs concrete included topics`);
  assert(Array.isArray(field.not_the_same_as) && field.not_the_same_as.length >= 2, `${field.id} needs semantic exclusions`);
}

for (const required of ['astrodynamics', 'mission_analysis', 'orbit_determination', 'gnc', 'attitude_dynamics_control', 'space_domain_awareness']) {
  assert(fieldIds.has(required), `Canonical field is missing: ${required}`);
  assert(taxonomy[required], `Taxonomy does not define canonical field: ${required}`);
  bilingual(taxonomy[required]?.label, `taxonomy.${required}.label`);
  bilingual(taxonomy[required]?.definition, `taxonomy.${required}.definition`);
}

const genericAliases = new Set(['guidance', 'navigation', 'control']);
for (const [key, entry] of Object.entries(taxonomy)) {
  const aliases = Array.isArray(entry?.aliases) ? entry.aliases.map((alias) => String(alias).trim().toLowerCase()) : [];
  for (const alias of aliases) assert(!genericAliases.has(alias), `Over-broad alias “${alias}” remains under ${key}`);
}

const databaseRecords = [...flattenRecords(america), ...flattenRecords(netherlands)];
const programmeIds = new Set();
for (const programme of catalog.strong_programmes) {
  assert(programme.programme_id && !programmeIds.has(programme.programme_id), `Missing or duplicate programme id: ${programme.programme_id}`);
  programmeIds.add(programme.programme_id);
  assert(programme.country?.flag, `${programme.programme_id} has no country flag`);
  assert(['very_strong', 'strong'].includes(programme.evidence_tier), `${programme.programme_id} has an unsupported evidence tier`);
  assert(Array.isArray(programme.fit_fields) && programme.fit_fields.length, `${programme.programme_id} has no fit fields`);
  programme.fit_fields.forEach((field) => assert(fieldIds.has(field), `${programme.programme_id} references unknown field ${field}`));
  bilingual(programme.why, `${programme.programme_id}.why`);
  bilingual(programme.practical_note, `${programme.programme_id}.practical_note`);
  assert(/^https:\/\//.test(programme.official_research_url || ''), `${programme.programme_id} has no HTTPS official research URL`);
  assert(Array.isArray(programme.source_ids) && programme.source_ids.length, `${programme.programme_id} has no source links`);

  // The fee shown here is a build-time copy of the programme database's
  // application_fee_standard, because this page never loads the full
  // database. A copy that drifts from its source is worse than no copy, so
  // the two are compared field by field on every run.
  const record = databaseRecords.find((row) => row.id === programme.programme_id);
  const canonical = record?.cost_profile?.application_fee_standard;
  const embedded = programme.application_fee;
  assert(embedded && canonical, `${programme.programme_id} has no embedded/canonical application fee`);
  if (embedded && canonical) {
    assert(embedded.status === canonical.status, `${programme.programme_id} embedded fee status drifted from the database`);
    assert(embedded.amount === canonical.amount, `${programme.programme_id} embedded fee amount drifted from the database`);
    assert(embedded.currency === canonical.currency, `${programme.programme_id} embedded fee currency drifted from the database`);
    assert(embedded.charged_per === (canonical.charged_per || 'application'), `${programme.programme_id} embedded charged_per drifted from the database`);
    assert(embedded.waiver_open_to_international === (canonical.waiver?.open_to_international ?? null), `${programme.programme_id} embedded waiver flag drifted from the database`);
    const canonicalEur = canonical.amount_eur_equivalent ? Math.round(canonical.amount_eur_equivalent.amount) : null;
    assert(embedded.eur_equivalent === canonicalEur, `${programme.programme_id} embedded euro equivalent drifted from the database`);
  }
}
assert(programmeIds.has('mit-aeroastro'), 'MIT programme is missing from the research shortlist');
assert(programmeIds.has('netherlands_delft_msc_aerospace'), 'TU Delft programme is missing from the research shortlist');

const sourceIds = new Set();
for (const source of catalog.sources) {
  assert(source.id && !sourceIds.has(source.id), `Missing or duplicate source id: ${source.id}`);
  sourceIds.add(source.id);
  assert(/^https:\/\//.test(source.url || ''), `${source.id} source URL is not HTTPS`);
  assert(source.source_type?.startsWith('official_'), `${source.id} is not classified as official`);
  assert(validAccess.has(source.access_status), `${source.id} has invalid access_status`);
  assert(source.last_checked === catalog.last_verified, `${source.id} was not checked on the catalog verification date`);
  assert(Array.isArray(source.relevant_fields) && source.relevant_fields.length, `${source.id} has no relevant_fields`);
  assert(['high', 'medium', 'low', 'unknown'].includes(source.confidence), `${source.id} has invalid confidence`);
  assert(typeof source.notes === 'string' && source.notes.trim(), `${source.id} has no source note`);
}
assert(catalog.sources.length >= 15, 'At least 15 official sources are required');
catalog.strong_programmes.flatMap((programme) => programme.source_ids).forEach((id) => assert(sourceIds.has(id), `Programme references unknown source ${id}`));

let facultyCount = 0;
for (const guide of catalog.advisor_guides) {
  assert(programmeIds.has(guide.programme_id), `Advisor guide references unknown programme ${guide.programme_id}`);
  assert(['contact_after_admission_for_ra', 'supervisor_match_during_msc'].includes(guide.policy), `${guide.programme_id} has unsupported contact policy`);
  bilingual(guide.before_application, `${guide.programme_id}.before_application`);
  bilingual(guide.after_admission, `${guide.programme_id}.after_admission`);
  assert(guide.programme_contact?.url?.startsWith('https://'), `${guide.programme_id} has no official programme contact URL`);
  for (const person of guide.faculty) {
    facultyCount += 1;
    assert(person.name, `${guide.programme_id} has an unnamed faculty record`);
    bilingual(person.role, `${person.name}.role`);
    bilingual(person.focus, `${person.name}.focus`);
    assert(/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(person.email || ''), `${person.name} has an invalid email`);
    assert(person.profile_url?.startsWith('https://'), `${person.name} has no official HTTPS profile`);
    assert(sourceIds.has(person.source_id), `${person.name} references unknown source ${person.source_id}`);
    person.fit_fields.forEach((field) => assert(fieldIds.has(field), `${person.name} references unknown field ${field}`));
  }
}
assert(facultyCount >= 7, 'At least seven named MIT/TU Delft faculty matches are required');

bilingual(catalog.outreach_template.subject, 'outreach_template.subject');
bilingual(catalog.outreach_template.avoid, 'outreach_template.avoid');
assert(catalog.outreach_template.steps.length === 4, 'The outreach checklist must contain four steps');
catalog.outreach_template.steps.forEach((step, index) => bilingual(step, `outreach_template.steps[${index}]`));

const allRecords = [...flattenRecords(america), ...flattenRecords(netherlands)];
for (const id of ['mit-aeroastro', 'netherlands_delft_msc_aerospace']) {
  const record = allRecords.find((item) => item.id === id || item.programme_id === id || item.Uni_ID === id);
  assert(record, `${id} detailed programme record is missing`);
  assert(record?.research_profile?.notable_professors?.length >= (id === 'mit-aeroastro' ? 3 : 4), `${id} does not expose the expected faculty details`);
}

for (const id of ['research-stats', 'field-tabs', 'field-definition', 'programme-grid', 'advisor-grid', 'faculty-grid', 'outreach-steps']) {
  assert(page.includes(`id="${id}"`), `Research page contract #${id} is missing`);
  assert(client.includes(`'${id}'`), `Research client does not bind #${id}`);
}
assert(client.includes('/api/research-pathways'), 'Research client does not use the catalog API');
assert(api.includes('/api/research-pathways'), 'Production API does not expose the research catalog');
assert(devServer.includes('/api/research-pathways'), 'Development server does not expose the research catalog');
assert(client.includes('index.html?program='), 'Research programme deep-link contract is missing');

const adapterSandbox = { window: { localizedValue: (value) => value?.en || value?.tr || value || '' } };
vm.runInNewContext(adapterCode, adapterSandbox, { filename: 'dataAdapter.js' });
const normalizedTestTags = adapterSandbox.window.uniDataAdapter.getCategoryProfile({
  category_profile: { normalized_tags: ['orbital_mechanics', 'guidance_navigation_control', 'control', 'flight_control', 'cfd'] }
}).normalized_tags;
assert(normalizedTestTags.includes('astrodynamics'), 'Orbital mechanics is not normalized to astrodynamics');
assert(normalizedTestTags.includes('gnc'), 'Guidance-navigation-control is not normalized to GNC');
assert(normalizedTestTags.includes('flight_control'), 'A valid specific legacy tag was dropped during normalization');
assert(normalizedTestTags.includes('cfd'), 'An unrelated valid canonical tag was dropped during normalization');
assert(!normalizedTestTags.includes('control'), 'Ambiguous generic control tag survived normalization');

if (errors.length) {
  console.error(`Research pathway checks failed (${errors.length}):`);
  errors.forEach((error) => console.error(`- ${error}`));
  process.exit(1);
}

console.log(`Research pathway checks passed: ${catalog.canonical_fields.length} fields, ${catalog.strong_programmes.length} programmes, ${facultyCount} faculty matches, ${catalog.sources.length} official sources.`);
