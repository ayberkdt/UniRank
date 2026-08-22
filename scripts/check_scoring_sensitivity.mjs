import { readFile } from 'node:fs/promises';
import vm from 'node:vm';

const root = new URL('../', import.meta.url);
const loadJson = async (file) => JSON.parse(await readFile(new URL(`data_base/${file}`, root), 'utf8'));
const programme = (payload, id) => {
  const rows = Array.isArray(payload) ? payload : (payload.programs || payload.universities || []);
  const record = rows.find((row) => row.id === id);
  if (!record) throw new Error(`Record not found: ${id}`);
  return record;
};

const sandbox = { window: null, console };
sandbox.window = sandbox;
vm.createContext(sandbox);
vm.runInContext(await readFile(new URL('public/dataAdapter.js', root), 'utf8'), sandbox, { filename: 'dataAdapter.js' });
vm.runInContext(await readFile(new URL('public/scoring.js', root), 'utf8'), sandbox, { filename: 'scoring.js' });

const preferences = { degreeFilter: 'All', onlyEnglish: false, maxTuition: 0 };
const balanced = { academic_fit: 30, eligibility_language: 20, cost_funding: 20, career_research: 15, living_risk: 10, confidence_deadline: 5 };
// Moving one UI slider to 100% now redistributes the others to zero so the
// visible percentages and the scoring shares always describe the same model.
const academicHeavy = { academic_fit: 100, eligibility_language: 0, cost_funding: 0, career_research: 0, living_risk: 0, confidence_deadline: 0 };

const normalizedBalanced = sandbox.unirankScoring.normalizeWeights(balanced);
const normalizedTotal = Object.values(normalizedBalanced).reduce((sum, value) => sum + value, 0);
if (Math.abs(normalizedTotal - 100) > 1e-9) throw new Error(`Normalized weights total ${normalizedTotal}, not 100.`);

const records = await Promise.all([
  loadJson('isvec.json').then((payload) => programme(payload, 'se-kth-aero-msc')),
  loadJson('almanya.json').then((payload) => programme(payload, 'germany-stuttgart-msc-aerospace')),
  loadJson('italy.json').then((payload) => programme(payload, 'unipd_aerospace')),
  loadJson('hollanda.json').then((payload) => programme(payload, 'netherlands_delft_msc_aerospace')),
  loadJson('amerika.json').then((payload) => programme(payload, 'mit-aeroastro')),
]);

const results = records.map((record) => {
  const normal = sandbox.unirankScoring.calculateScore(record, preferences, balanced);
  const heavy = sandbox.unirankScoring.calculateScore(record, preferences, academicHeavy);
  const scaled = sandbox.unirankScoring.calculateScore(record, preferences, Object.fromEntries(Object.entries(balanced).map(([key, value]) => [key, value * 10])));
  if (Math.abs(normal.total_score - scaled.total_score) > 1e-9) {
    throw new Error(`Weight scaling changed ${record.id}: ${normal.total_score} vs ${scaled.total_score}.`);
  }
  return {
    id: record.id,
    academic_component: normal.components.academic_fit,
    balanced: normal.total_score,
    academic_heavy: heavy.total_score,
    change: heavy.total_score - normal.total_score,
  };
});

const stuttgart = results.find((result) => result.id === 'germany-stuttgart-msc-aerospace');
const delft = results.find((result) => result.id === 'netherlands_delft_msc_aerospace');
const mit = results.find((result) => result.id === 'mit-aeroastro');
if (!stuttgart || !delft || !mit) throw new Error('Sensitivity control records are missing.');
if (stuttgart.academic_component <= delft.academic_component) {
  throw new Error('Academic evidence does not distinguish a documented curriculum from an unverified record.');
}
if (stuttgart.change < 5) {
  throw new Error(`Academic-weight change is too small for Stuttgart (${stuttgart.change.toFixed(2)} points).`);
}
if (stuttgart.academic_heavy <= delft.academic_heavy) {
  throw new Error('Academic-heavy ranking does not favour the stronger documented curriculum.');
}
if (mit.academic_component <= stuttgart.academic_component) {
  throw new Error('MIT does not lead the academic-strength control despite its checked research evidence.');
}
if (mit.change < 5) {
  throw new Error(`Academic slider has too little effect on MIT (${mit.change.toFixed(2)} points).`);
}
const academicRank = [...results].sort((left, right) => right.academic_heavy - left.academic_heavy);
if (academicRank[0]?.id !== 'mit-aeroastro') {
  throw new Error('A full Academic Strength slider does not place MIT first in the control set.');
}

console.log('Scoring sensitivity passed.');
for (const result of results) {
  console.log(`${result.id}: academic=${result.academic_component.toFixed(1)}, balanced=${result.balanced.toFixed(2)}, academic-heavy=${result.academic_heavy.toFixed(2)}, change=${result.change.toFixed(2)}`);
}
