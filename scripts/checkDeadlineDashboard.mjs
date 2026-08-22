import { readFile } from 'node:fs/promises';
import vm from 'node:vm';

const code = await readFile(new URL('../public/deadlineDashboard.js', import.meta.url), 'utf8');
const sandbox = {
  URL,
  Date,
  Intl,
  Set,
  Map,
  console,
  window: null,
  document: {
    readyState: 'loading',
    addEventListener: () => {},
  },
  localStorage: {
    getItem: () => '[]',
  },
};
sandbox.window = sandbox;
sandbox.currentLanguage = 'tr';
sandbox.getCountryName = value => value;
sandbox.uniDataAdapter = {
  normalizeUniversityRecord(record) {
    return {
      id: record.id,
      universityName: record.university,
      programName: record.program_name,
      country: record.country,
      city: record.city,
      degree: record.degree_level,
    };
  },
};

vm.runInNewContext(code, sandbox, { filename: 'deadlineDashboard.js' });
const dashboard = sandbox.uniDeadlineDashboard;
const failures = [];

const exact = dashboard.datePartsFromIso('Deadline: 2027-01-15T14:00:00+02:00');
if (exact.length !== 1 || exact[0].key !== '2027-01-15') failures.push('Exact ISO deadline was not parsed.');
if (dashboard.datePartsFromIso('December 1 (annual)').length !== 0) failures.push('A yearless date was incorrectly inferred.');
const naturalDate = dashboard.formatDate(dashboard.datePartsFromIso('2026-08-24')[0]);
if (naturalDate !== '24 Ağustos 2026 Pazartesi') failures.push(`Deadline date is not in natural Turkish format: ${naturalDate}`);
if (dashboard.eventDisplayLabel({ label: 'programme_application_deadline' }) !== 'Program başvurusunun son günü') {
  failures.push('Technical application event label was not rewritten for the Turkish UI.');
}
if (dashboard.eventOfficialNote({ raw: '2026-08-24' })) failures.push('A bare ISO date was repeated as official wording.');

const record = {
  id: 'test-program',
  university: 'Test University',
  program_name: 'MSc Aerospace',
  country: 'Türkiye',
  city: 'Ankara',
  degree_level: 'Master',
  eligibility_profile: {
    required_documents: ['official_transcript', { en: 'Statement of purpose', tr: 'Amaç beyanı' }],
  },
  application_timeline_profile: {
    non_eu_deadline: '2027-01-15',
    application_rounds: [{ intake: 'Fall 2027', deadline: '2027-01-15' }],
    visa_sensitive_deadline: 'Universitaly deadline not yet published',
    deadline_events: [
      { event: 'application_deadline', date: '2027-01-15', status: 'published', applicant_scope: 'international' },
      { event: 'home_application_deadline', date: '2027-02-01', status: 'published', applicant_scope: 'home' },
      { event: 'classes_begin', date: '2027-09-01', status: 'published', applicant_scope: 'all' },
    ],
  },
  data_quality: { verified_fields: ['admission', 'deadline'] },
  source_profile: {
    field_confidence: { admission: 'high', deadlines: 'high' },
    last_verified: '2026-08-22',
    source_log: [{
      url: 'https://example.edu/admission',
      title: 'Official admission page',
      source_type: 'official_admission_page',
      access_status: 'ok',
      relevant_fields: ['admission', 'deadline', 'required_documents'],
      confidence: 'high',
    }],
  },
};

const events = dashboard.collectDeadlineEvents(record);
const exactApplications = events.filter(event => event.exact && event.kind === 'application' && event.datePart.key === '2027-01-15');
if (exactApplications.length !== 1) failures.push('Duplicate representations of one application date were not coalesced.');
if (!events.some(event => !event.exact && event.kind === 'visa')) failures.push('Undated visa milestone was not kept for verification.');
if (events.some(event => event.datePart?.key === '2027-02-01' || /classes begin/i.test(event.label))) failures.push('Home-only or non-actionable dates reached the non-EU countdown.');

const documents = dashboard.documentItems(record);
if (documents.join('|') !== 'Official transcript|Amaç beyanı') failures.push('Verified document labels were not localized/humanized.');

const unverifiedDocuments = dashboard.documentItems({
  eligibility_profile: { required_documents: ['Unverified claim'] },
  source_profile: { field_confidence: { admission: 'unknown' } },
  data_quality: { verified_fields: [] },
});
if (unverifiedDocuments.length !== 0) failures.push('Unverified required documents reached the UI model.');

const model = dashboard.programModel(record, 0);
if (!model.deadlineSource?.url || model.confidence !== 'high' || model.documents.length !== 2) failures.push('Program calendar model lost verified source metadata.');

let refreshCalls = 0;
sandbox.document.hidden = false;
sandbox.refreshUniRankData = async () => {
  refreshCalls += 1;
  return true;
};
if (!await dashboard.refreshNow() || refreshCalls !== 1) failures.push('Automatic API refresh hook did not run.');

if (failures.length) {
  console.error(`Deadline dashboard checks failed (${failures.length})`);
  failures.forEach(failure => console.error(`- ${failure}`));
  process.exitCode = 1;
} else {
  console.log(`Deadline dashboard checks passed: ${events.length} normalized events, ${documents.length} verified documents.`);
}
