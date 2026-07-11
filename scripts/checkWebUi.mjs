import { readFile } from 'node:fs/promises';
import vm from 'node:vm';

const root = new URL('../', import.meta.url);
const files = {
  html: new URL('public/index.html', root),
  css: new URL('public/style.css', root),
  i18n: new URL('public/i18n.js', root),
  map: new URL('public/map.js', root),
  script: new URL('public/script.js', root),
};

const [html, css, i18nCode, mapCode, scriptCode] = await Promise.all([
  readFile(files.html, 'utf8'),
  readFile(files.css, 'utf8'),
  readFile(files.i18n, 'utf8'),
  readFile(files.map, 'utf8'),
  readFile(files.script, 'utf8'),
]);

const failures = [];
const ids = [...html.matchAll(/\bid="([^"]+)"/g)].map((match) => match[1]);
const duplicateIds = ids.filter((id, index) => ids.indexOf(id) !== index);
if (duplicateIds.length) failures.push(`Duplicate HTML ids: ${[...new Set(duplicateIds)].join(', ')}`);

const requiredIds = [
  'filter-sidebar',
  'filter-toggle',
  'search-input',
  'country-filter',
  'categorySearchInput',
  'degree-filter',
  'english-only-filter',
  'max-tuition-filter',
  'sort-select',
  'btn-view-list',
  'btn-view-map',
  'list-view-container',
  'map-view-container',
  'table-body',
  'map',
  'map-results-list',
  'map-results-status',
  'map-kpi-count',
  'map-kpi-universities',
  'map-kpi-missing',
  'detail-drawer',
  'drawer-overlay',
];
const missingIds = requiredIds.filter((id) => !ids.includes(id));
if (missingIds.length) failures.push(`Missing UI contract ids: ${missingIds.join(', ')}`);

const sandbox = {
  window: null,
  localStorage: { getItem: () => null, setItem: () => {} },
  document: {
    documentElement: {},
    querySelectorAll: () => [],
    addEventListener: () => {},
    dispatchEvent: () => {},
  },
  CustomEvent: class CustomEvent {},
};
sandbox.window = sandbox;
vm.runInNewContext(i18nCode, sandbox, { filename: 'i18n.js' });

const translationKeys = new Set();
for (const pattern of [
  /\bdata-i18n="([^"]+)"/g,
  /\bdata-i18n-placeholder="([^"]+)"/g,
  /\bdata-i18n-aria-label="([^"]+)"/g,
]) {
  for (const match of html.matchAll(pattern)) translationKeys.add(match[1]);
}
for (const key of translationKeys) {
  if (!sandbox.I18N?.en?.[key]) failures.push(`Missing English translation: ${key}`);
  if (!sandbox.I18N?.tr?.[key]) failures.push(`Missing Turkish translation: ${key}`);
}

const cssWithoutComments = css.replace(/\/\*[\s\S]*?\*\//g, '');
const openingBraces = (cssWithoutComments.match(/{/g) || []).length;
const closingBraces = (cssWithoutComments.match(/}/g) || []).length;
if (openingBraces !== closingBraces) failures.push(`CSS brace mismatch: ${openingBraces} opening / ${closingBraces} closing`);

for (const contract of [
  ['responsive filter drawer', css.includes('.filters-open .sidebar')],
  ['reduced motion support', css.includes('@media (prefers-reduced-motion: reduce)')],
  ['map result cards', css.includes('.map-result-card') && mapCode.includes('map-result-card')],
  ['shared map score thresholds', mapCode.includes('score >= 6.0') && scriptCode.includes('value >= 6')],
  ['list/map aria state', scriptCode.includes("setAttribute('aria-pressed'")],
  ['drawer aria state', scriptCode.includes("setAttribute('aria-hidden'")],
]) {
  if (!contract[1]) failures.push(`Missing contract: ${contract[0]}`);
}

if (failures.length) {
  console.error(`Web UI checks failed (${failures.length})`);
  failures.forEach((failure) => console.error(`- ${failure}`));
  process.exitCode = 1;
} else {
  console.log(`Web UI checks passed: ${ids.length} unique ids, ${translationKeys.size} bilingual keys, ${requiredIds.length} required contracts.`);
}
