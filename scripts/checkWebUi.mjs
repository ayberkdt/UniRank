import { readFile } from 'node:fs/promises';
import vm from 'node:vm';

const root = new URL('../', import.meta.url);
const files = {
  html: new URL('public/index.html', root),
  css: new URL('public/style.css', root),
  redesign: new URL('public/redesign.css', root),
  i18n: new URL('public/i18n.js', root),
  map: new URL('public/map.js', root),
  script: new URL('public/script.js', root),
  deadline: new URL('public/deadlineDashboard.js', root),
};

const [html, css, redesignCss, i18nCode, mapCode, scriptCode, deadlineCode] = await Promise.all([
  readFile(files.html, 'utf8'),
  readFile(files.css, 'utf8'),
  readFile(files.redesign, 'utf8'),
  readFile(files.i18n, 'utf8'),
  readFile(files.map, 'utf8'),
  readFile(files.script, 'utf8'),
  readFile(files.deadline, 'utf8'),
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
  'country-picker-trigger',
  'country-picker-popover',
  'country-picker-search',
  'country-picker-options',
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
  'deadline-launcher',
  'deadline-modal',
  'deadline-summary-grid',
  'deadline-program-list',
  'kpi-source-coverage',
  'kpi-map-coverage',
  'weight-total',
];
const missingIds = requiredIds.filter((id) => !ids.includes(id));
if (missingIds.length) failures.push(`Missing UI contract ids: ${missingIds.join(', ')}`);
if (/value="BSc"|Bachelor \(BSc\)/i.test(html)) {
  failures.push('Undergraduate degree option is exposed in the postgraduate UI.');
}
if (!html.includes('value="english_available"')) {
  failures.push('Profile language preference does not expose the English-study-option semantic.');
}

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

const cssWithoutComments = `${css}\n${redesignCss}`.replace(/\/\*[\s\S]*?\*\//g, '');
const openingBraces = (cssWithoutComments.match(/{/g) || []).length;
const closingBraces = (cssWithoutComments.match(/}/g) || []).length;
if (openingBraces !== closingBraces) failures.push(`CSS brace mismatch: ${openingBraces} opening / ${closingBraces} closing`);

for (const contract of [
  ['responsive filter drawer', css.includes('.filters-open .sidebar')],
  ['custom country picker', html.includes('class="country-picker-native" hidden') && scriptCode.includes('renderCountryFlag') && css.includes('.country-picker-popover')],
  ['country picker accessibility', html.includes('aria-multiselectable="true"') && scriptCode.includes("setAttribute('aria-selected'")],
  ['fixed filter rail controls', html.includes('class="sidebar__scroll"') && css.includes('.sidebar__scroll')],
  ['reduced motion support', css.includes('@media (prefers-reduced-motion: reduce)')],
  ['map result cards', css.includes('.map-result-card') && mapCode.includes('map-result-card')],
  ['shared map score thresholds', [6.5, 5.5, 4.5].every((value) => mapCode.includes(`score >= ${value}`) && scriptCode.includes(`value >= ${value}`))],
  ['list/map aria state', scriptCode.includes("setAttribute('aria-pressed'")],
  ['drawer aria state', scriptCode.includes("setAttribute('aria-hidden'")],
  ['deadline dashboard', html.includes('deadlineDashboard.js') && deadlineCode.includes('collectDeadlineEvents') && css.includes('.deadline-modal-shell')],
  ['deadline source integrity', deadlineCode.includes('VALID_SOURCE_STATUSES') && deadlineCode.includes('documentsVerified')],
  ['deadline automatic refresh', deadlineCode.includes('AUTO_REFRESH_MS') && deadlineCode.includes('visibilitychange') && deadlineCode.includes('scheduleMidnightRefresh') && scriptCode.includes('refreshUniRankData') && css.includes('.deadline-auto-sync')],
  ['Sunumatik editorial redesign', html.includes('redesign.css') && redesignCss.includes('--ui-ember') && redesignCss.includes('Space Grotesk') && redesignCss.includes('.deadline-program-card__next time')],
  ['natural deadline dates', deadlineCode.includes("weekday: 'long'") && deadlineCode.includes('eventDisplayLabel')],
  ['normalized weighting UI', scriptCode.includes('rebalanceUiWeights') && scriptCode.includes('distributeIntegerWeight') && html.includes('weight-normalization-note')],
  ['non-tuition overview KPIs', !html.includes('id="kpi-tuition"') && html.includes('id="kpi-source-coverage"') && html.includes('id="kpi-map-coverage"')],
  ['reliable map sizing', mapCode.includes("unirank:viewChanged") && mapCode.includes('ResizeObserver') && redesignCss.includes('grid-template-rows: minmax(0, 1fr)')],
  ['no decorative GeoJSON dependency', !mapCode.includes('raw.githubusercontent.com/johan/world.geo.json')],
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
