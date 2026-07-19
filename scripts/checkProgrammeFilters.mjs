import { readdir, readFile } from 'node:fs/promises';
import vm from 'node:vm';

const root = new URL('../', import.meta.url);
const dataRoot = new URL('data_base/', root);
const loadJson = async (file) => JSON.parse(await readFile(new URL(file, dataRoot), 'utf8'));
const rows = (payload) => Array.isArray(payload) ? payload : (payload?.programs || payload?.universities || []);
const programme = (payload, id) => {
  const record = rows(payload).find((row) => row.id === id);
  if (!record) throw new Error(`Record not found: ${id}`);
  return record;
};

const html = await readFile(new URL('public/index.html', root), 'utf8');
if (/value="BSc"|Bachelor \(BSc\)/i.test(html)) {
  throw new Error('The postgraduate UI still exposes a Bachelor option.');
}

const undergraduate = [];
for (const file of await readdir(dataRoot)) {
  if (!file.endsWith('.json') || file === 'taxonomy.json') continue;
  for (const record of rows(await loadJson(file))) {
    const degreeText = [
      record?.degree_level,
      record?.program_degree,
      record?.target_program_degree,
      record?.Program_Degree,
      record?.degree,
    ].map((value) => String(value || '')).join(' ').toLowerCase();
    if (/\b(bachelor|b\.?\s*sc\.?|bsc|undergraduate|first[- ]cycle|lisans)\b/.test(degreeText)) {
      undergraduate.push(`${file}:${record.id || record.program_name || 'unknown'}`);
    }
  }
}
if (undergraduate.length) {
  throw new Error(`Undergraduate records remain in the active database: ${undergraduate.join(', ')}`);
}

const sandbox = { window: null, console };
sandbox.window = sandbox;
vm.createContext(sandbox);
vm.runInContext(await readFile(new URL('public/dataAdapter.js', root), 'utf8'), sandbox, { filename: 'dataAdapter.js' });
vm.runInContext(await readFile(new URL('public/scoring.js', root), 'utf8'), sandbox, { filename: 'scoring.js' });

const germany = await loadJson('almanya.json');
const tuhh = programme(germany, 'de_tuhh_aeronautics_msc');
const tum = programme(germany, 'germany-tum-msc-aerospace');
const stuttgart = programme(germany, 'germany-stuttgart-msc-aerospace');
const preferences = { degreeFilter: 'All', onlyEnglish: true, maxTuition: 0 };
const weights = { academic_fit: 30, eligibility_language: 20, cost_funding: 20, career_research: 15, living_risk: 10, confidence_deadline: 5 };

for (const record of [tuhh, tum]) {
  if (!sandbox.unirankScoring.calculateScore(record, preferences, weights).passed_hard_filters) {
    throw new Error(`${record.id} was rejected despite its verified English study option.`);
  }
}
if (sandbox.unirankScoring.calculateScore(stuttgart, preferences, weights).passed_hard_filters) {
  throw new Error('German-only Stuttgart passed the English-study-option filter.');
}

console.log('Postgraduate-only and English-study-option filter checks passed.');
