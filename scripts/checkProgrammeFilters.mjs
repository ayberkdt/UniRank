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
const romania = await loadJson('romania.json');
const airTransport = programme(romania, 'ro-politehnica-bucharest-air-transport-engineering-msc');
const holisticSpace = programme(romania, 'ro-politehnica-bucharest-holistic-space-systems-msc');
const avionicsNavigation = programme(romania, 'ro-politehnica-bucharest-avionics-aerospace-navigation-msc');
const propulsionEnvironment = programme(romania, 'ro-politehnica-bucharest-aerospace-propulsion-environment-msc');
const aeronauticalSpaceStructures = programme(romania, 'ro-politehnica-bucharest-aeronautical-space-structures-msc');
const engineeringAerospaceManagement = programme(romania, 'ro-politehnica-bucharest-aerospace-engineering-management-msc');
const aeronauticalManagement = programme(romania, 'ro-politehnica-bucharest-aeronautical-management-msc');
const aviationInformationTechnology = programme(romania, 'ro-politehnica-bucharest-information-technologies-aviation-msc');
const craiovaComplexSystems = programme(romania, 'ro-university-craiova-complex-systems-aerospace-engineering-msc');
const mtaAeronauticalSystems = programme(romania, 'ro-military-technical-academy-aerospace-systems-engineering-msc');
const preferences = { degreeFilter: 'All', onlyEnglish: true, maxTuition: 0 };
const weights = { academic_fit: 30, eligibility_language: 20, cost_funding: 20, career_research: 15, living_risk: 10, confidence_deadline: 5 };

for (const record of [tuhh, tum]) {
  if (!sandbox.unirankScoring.calculateScore(record, preferences, weights).passed_hard_filters) {
    throw new Error(`${record.id} was rejected despite its verified English study option.`);
  }
}
if (!sandbox.unirankScoring.calculateScore(airTransport, preferences, weights).passed_hard_filters) {
  throw new Error('English-taught POLITEHNICA Air Transport Engineering failed the English-study-option filter.');
}
const aviationInformationTechnologyScore = sandbox.unirankScoring.calculateScore(aviationInformationTechnology, preferences, weights);
if (!aviationInformationTechnologyScore.passed_hard_filters) {
  throw new Error('English-taught POLITEHNICA Information Technologies Applied in Aviation failed the English-study-option filter.');
}
if (aviationInformationTechnologyScore.components.academic_fit > 78) {
  throw new Error('Medium-relevance POLITEHNICA Information Technologies Applied in Aviation exceeded its academic-fit cap.');
}
if (sandbox.unirankScoring.calculateScore(holisticSpace, preferences, weights).passed_hard_filters) {
  throw new Error('Romanian-taught POLITEHNICA Holistic Space Systems passed the English-study-option filter.');
}
if (sandbox.unirankScoring.calculateScore(avionicsNavigation, preferences, weights).passed_hard_filters) {
  throw new Error('Romanian-taught POLITEHNICA Avionics and Aerospace Navigation passed the English-study-option filter.');
}
if (sandbox.unirankScoring.calculateScore(propulsionEnvironment, preferences, weights).passed_hard_filters) {
  throw new Error('Romanian-taught POLITEHNICA Aerospace Propulsion and Environmental Protection passed the English-study-option filter.');
}
if (sandbox.unirankScoring.calculateScore(aeronauticalSpaceStructures, preferences, weights).passed_hard_filters) {
  throw new Error('Romanian-taught POLITEHNICA Aeronautical and Space Structures passed the English-study-option filter.');
}
if (sandbox.unirankScoring.calculateScore(engineeringAerospaceManagement, preferences, weights).passed_hard_filters) {
  throw new Error('Romanian-taught POLITEHNICA Engineering and Aerospace Management passed the English-study-option filter.');
}
if (sandbox.unirankScoring.calculateScore(aeronauticalManagement, preferences, weights).passed_hard_filters) {
  throw new Error('Romanian-taught POLITEHNICA Aeronautical Management passed the English-study-option filter.');
}
if (sandbox.unirankScoring.calculateScore(craiovaComplexSystems, preferences, weights).passed_hard_filters) {
  throw new Error('Romanian-taught University of Craiova Complex Systems for Aerospace Engineering passed the English-study-option filter.');
}
if (sandbox.unirankScoring.calculateScore(mtaAeronauticalSystems, preferences, weights).passed_hard_filters) {
  throw new Error('Romanian-taught MTA Ferdinand I Aeronautical Systems Engineering passed the English-study-option filter.');
}

const directSpaceScore = sandbox.unirankScoring.calculateScore(holisticSpace, { ...preferences, onlyEnglish: false }, weights);
for (const record of [engineeringAerospaceManagement, aeronauticalManagement]) {
  const result = sandbox.unirankScoring.calculateScore(record, { ...preferences, onlyEnglish: false }, weights);
  if (result.components.academic_fit > 45) {
    throw new Error(`${record.id} exceeded the weak-relevance academic-fit cap.`);
  }
  if (result.components.academic_fit >= directSpaceScore.components.academic_fit) {
    throw new Error(`${record.id} ranked at or above the direct Holistic Space Systems programme on academic fit.`);
  }
}
if (sandbox.unirankScoring.calculateScore(stuttgart, preferences, weights).passed_hard_filters) {
  throw new Error('German-only Stuttgart passed the English-study-option filter.');
}

console.log('Postgraduate-only and English-study-option filter checks passed.');
