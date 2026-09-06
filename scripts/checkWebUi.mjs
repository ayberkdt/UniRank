import { readFile } from 'node:fs/promises';
import vm from 'node:vm';

const root = new URL('../', import.meta.url);
const files = {
  html: new URL('public/index.html', root),
  calendarHtml: new URL('public/calendar.html', root),
  calendarCss: new URL('public/calendar.css', root),
  calendar: new URL('public/calendar.js', root),
  css: new URL('public/style.css', root),
  redesign: new URL('public/redesign.css', root),
  site: new URL('public/site.css', root),
  profileCss: new URL('public/profile.css', root),
  i18n: new URL('public/i18n.js', root),
  map: new URL('public/map.js', root),
  script: new URL('public/script.js', root),
  deadline: new URL('public/deadlineDashboard.js', root),
  profile: new URL('public/profile.js', root),
  storage: new URL('public/storage.js', root),
};

const [html, calendarHtml, calendarCss, calendarCode, css, redesignCss, siteCss, profileCss, i18nCode, mapCode, scriptCode, deadlineCode, profileCode, storageCode] = await Promise.all([
  readFile(files.html, 'utf8'),
  readFile(files.calendarHtml, 'utf8'),
  readFile(files.calendarCss, 'utf8'),
  readFile(files.calendar, 'utf8'),
  readFile(files.css, 'utf8'),
  readFile(files.redesign, 'utf8'),
  readFile(files.site, 'utf8'),
  readFile(files.profileCss, 'utf8'),
  readFile(files.i18n, 'utf8'),
  readFile(files.map, 'utf8'),
  readFile(files.script, 'utf8'),
  readFile(files.deadline, 'utf8'),
  readFile(files.profile, 'utf8'),
  readFile(files.storage, 'utf8'),
]);

const failures = [];
const ids = [...html.matchAll(/\bid="([^"]+)"/g)].map((match) => match[1]);
const duplicateIds = ids.filter((id, index) => ids.indexOf(id) !== index);
if (duplicateIds.length) failures.push(`Duplicate HTML ids: ${[...new Set(duplicateIds)].join(', ')}`);
const calendarIds = [...calendarHtml.matchAll(/\bid="([^"]+)"/g)].map((match) => match[1]);
const duplicateCalendarIds = calendarIds.filter((id, index) => calendarIds.indexOf(id) !== index);
if (duplicateCalendarIds.length) failures.push(`Duplicate calendar ids: ${[...new Set(duplicateCalendarIds)].join(', ')}`);

const literalDomRefs = new Set();
for (const code of [scriptCode, mapCode, profileCode]) {
  for (const match of code.matchAll(/getElementById\(\s*['"]([^'"]+)['"]\s*\)/g)) {
    literalDomRefs.add(match[1]);
  }
}
// Some controls are intentionally rendered with the selected record rather
// than kept as empty global markup. Their contracts are checked below.
const dynamicDomIds = new Set(['radarChart']);
const missingLiteralDomRefs = [...literalDomRefs].filter((id) => !ids.includes(id) && !dynamicDomIds.has(id)).sort();
const dashboardDomRefs = new Set();
for (const code of [deadlineCode, calendarCode]) {
  for (const match of code.matchAll(/getElementById\(\s*['"]([^'"]+)['"]\s*\)/g)) {
    dashboardDomRefs.add(match[1]);
  }
}
const missingDashboardRefs = [...dashboardDomRefs].filter((id) => !ids.includes(id) && !calendarIds.includes(id)).sort();
if (missingDashboardRefs.length) {
  failures.push(`Calendar JavaScript references ids on neither page: ${missingDashboardRefs.join(', ')}`);
}
if (missingLiteralDomRefs.length) {
  failures.push(`JavaScript references missing HTML ids: ${missingLiteralDomRefs.join(', ')}`);
}

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
  'kpi-source-coverage',
  'kpi-map-coverage',
  'weight-total',
];
const missingIds = requiredIds.filter((id) => !ids.includes(id));
if (missingIds.length) failures.push(`Missing UI contract ids: ${missingIds.join(', ')}`);
const requiredCalendarIds = [
  'deadline-page',
  'deadline-priority',
  'deadline-summary-grid',
  'deadline-cost-strip',
  'deadline-runway-track',
  'deadline-catalog-title',
  'deadline-filter-chips',
  'deadline-search-input',
  'deadline-favorites-only',
  'deadline-results-meta',
  'deadline-program-list',
];
const missingCalendarIds = requiredCalendarIds.filter((id) => !calendarIds.includes(id));
if (missingCalendarIds.length) failures.push(`Missing calendar contract ids: ${missingCalendarIds.join(', ')}`);
if (html.includes('deadline-modal')) failures.push('The programmes page still carries the calendar dialog.');
if (/value="BSc"|Bachelor \(BSc\)/i.test(html)) {
  failures.push('Undergraduate degree option is exposed in the postgraduate UI.');
}
if (!html.includes('value="english_available"')) {
  failures.push('Profile language preference does not expose the English-study-option semantic.');
}

const sandbox = {
  window: null,
  localStorage: { getItem: () => null, setItem: () => {} },
  uniStorage: { read: (_key, fallback) => fallback, write: () => true },
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

const storageMemory = new Map([['broken', '{not-json']]);
const storageSandbox = {
  window: null,
  localStorage: {
    getItem: (key) => storageMemory.has(key) ? storageMemory.get(key) : null,
    setItem: (key, value) => storageMemory.set(key, String(value)),
    removeItem: (key) => storageMemory.delete(key),
  },
};
storageSandbox.window = storageSandbox;
vm.runInNewContext(storageCode, storageSandbox, { filename: 'storage.js' });
if (storageSandbox.uniStorage.readArray('broken').length || storageMemory.has('broken')) {
  failures.push('Shared storage does not recover from malformed JSON.');
}
if (!storageSandbox.uniStorage.writeJSON('valid', ['ok']) || storageSandbox.uniStorage.readArray('valid')[0] !== 'ok') {
  failures.push('Shared storage JSON round-trip failed.');
}

const translationKeys = new Set();
for (const pattern of [
  /\bdata-i18n="([^"]+)"/g,
  /\bdata-i18n-placeholder="([^"]+)"/g,
  /\bdata-i18n-aria-label="([^"]+)"/g,
]) {
  for (const match of html.matchAll(pattern)) translationKeys.add(match[1]);
  for (const match of calendarHtml.matchAll(pattern)) translationKeys.add(match[1]);
}
for (const key of translationKeys) {
  if (!sandbox.I18N?.en?.[key]) failures.push(`Missing English translation: ${key}`);
  if (!sandbox.I18N?.tr?.[key]) failures.push(`Missing Turkish translation: ${key}`);
}

const cssWithoutComments = `${css}\n${redesignCss}\n${profileCss}\n${calendarCss}`.replace(/\/\*[\s\S]*?\*\//g, '');
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
  // The calendar is a page of its own. The programmes page keeps only the
  // launcher, whose badge the same module still feeds.
  ['deadline dashboard page', calendarHtml.includes('deadlineDashboard.js') && calendarHtml.includes('id="deadline-page"') && html.includes('deadlineDashboard.js') && html.includes('href="calendar.html"') && deadlineCode.includes('collectDeadlineEvents') && deadlineCode.includes('pageMode') && calendarCss.includes('.deadline-page') && !css.includes('.deadline-modal-shell') && !redesignCss.includes('.deadline-modal-')],
  ['deadline action hierarchy', deadlineCode.includes('renderPriority') && calendarHtml.includes('class="deadline-overview"') && calendarHtml.includes('class="deadline-runway"') && redesignCss.includes('.deadline-priority__body') && redesignCss.includes('.deadline-catalog')],
  ['decision profile and requirement summary at the top of the rail', html.includes('requirementSummary.js') && scriptCode.includes('uniRequirementSummary') && /decisionHeroHTML \+\s*decisionProfileHTML \+\s*requirementSummaryHTML \+/.test(scriptCode)],
  ['live decision profile', scriptCode.includes('decisionMetrics(data._scoringDetails?.components || {}, isTurkish)') && scriptCode.includes('data: metrics.map(metric => metric.value)') && scriptCode.includes('max: 100') && redesignCss.includes('.drawer-fit-overview')],
  ['runway lists each university once per month', deadlineCode.includes('byUniversity') && deadlineCode.includes('runwayUniversities')],
  ['calendar page loads its own data', calendarCode.includes("fetch('/api/universities')") && calendarCode.includes('unirank:recordsLoaded') && calendarCode.includes('refreshUniRankData') && calendarHtml.includes('countryVisual.js') && html.includes('countryVisual.js')],
  ['deadline source integrity', deadlineCode.includes('VALID_SOURCE_STATUSES') && deadlineCode.includes('documentsVerified')],
  ['deadline automatic refresh', deadlineCode.includes('AUTO_REFRESH_MS') && deadlineCode.includes('visibilitychange') && deadlineCode.includes('scheduleMidnightRefresh') && scriptCode.includes('refreshUniRankData') && css.includes('.deadline-auto-sync')],
  ['no orange accent left', !/#e8804a|#f18046|#ef7f45|rgba\(232,\s*128,\s*74|rgba\(241,\s*128,\s*70|rgba\(239,\s*127,\s*69/i.test(`${css}${redesignCss}${siteCss}${profileCss}${calendarCss}${scriptCode}`)],
  ['Sunumatik editorial redesign', html.includes('redesign.css') && redesignCss.includes('.deadline-program-card__next time')],
  // Tokens live in the shared foundation now, not per page. One palette, one
  // header, loaded by index, research and scholarships alike.
  // A dark product kept shipping light-theme chips: the confidence badges alone
  // painted a pale-cream pill onto 115 cards, the tuition readout was teal on
  // near-white at 1.6:1, and the map fallback was white text on a white panel.
  // Grep for the specific literals rather than "any light colour", because flag
  // stripe gradients legitimately use them.
  ['no light-theme chips left in the dark UI', ![
    '#fff7df', '#e7f5f0', '#fff0f0', '#f3f6f9', '#e7f4ef', '#f4f7fb',
  ].some((literal) => css.includes(literal))],
  // Raw national colours are picked for flags, not for small text on a dark
  // card; they measured 2.5-4.0:1 until they were mixed toward the ink.
  ['country accents are mixed before use as text', css.includes('color-mix(in oklab, var(--country-accent)') && redesignCss.includes('color-mix(in oklab, var(--deadline-country-accent)')],
  ['shared Graphite Violet foundation', html.includes('site.css') && siteCss.includes('--ge-accent') && siteCss.includes('--ui-accent: var(--ge-accent)') && siteCss.includes('--accent: var(--ge-accent)') && siteCss.includes('Space Grotesk') && siteCss.includes('.site-bar__nav') && !redesignCss.includes('--ui-canvas: #')],
  ['Sunumatik Graphite Violet rails', redesignCss.includes('--ui-signal: var(--ge-signal)') && redesignCss.includes('#detail-drawer.drawer.country-themed') && redesignCss.includes('.country-picker-popover')],
  ['pixel-aligned premium filter rail', redesignCss.includes('--ui-filter-rail-inset: 20px') && redesignCss.includes('.sidebar__scroll > .filter-card') && redesignCss.includes('scrollbar-width: none')],
  ['stable profile CTA structure', html.includes('class="profile-cta__arrow"') && scriptCode.includes("querySelector('.profile-cta__copy strong')") && !scriptCode.includes('useProfileBtn.innerHTML')],
  ['structured workspace header', html.includes('class="header-destinations"') && html.includes('class="header-accountbar"') && html.includes('class="account-profile-button"') && !html.includes('class="user-avatar"')],
  ['hierarchical detail rail', scriptCode.includes('class="ranking-list"') && scriptCode.includes('isTiedQsRank') && scriptCode.includes('class="drawer-priority-group') && redesignCss.includes('.drawer-priority-group')],
  ['true map fullscreen', mapCode.includes('requestFullscreen') && mapCode.includes('fullscreenchange') && redesignCss.includes('.map-stage:fullscreen') && redesignCss.includes('inset: 0 !important')],
  ['modular profile workspace', html.includes('profile.css') && profileCss.includes('.profile-interest-item') && profileCode.includes('normalizeInterestWeight') && profileCode.includes('parseNonNegativeNumber') && profileCode.includes('replaceChildren') && !profileCode.includes('innerHTML')],
  ['resilient shared storage', html.indexOf('storage.js') < html.indexOf('i18n.js') && storageCode.includes('readJSON') && storageCode.includes('readArray') && scriptCode.includes("uniStorage.readArray('unirank_favorites')") && profileCode.includes('uniStorage.readArray') && mapCode.includes("uniStorage.read('unirank_map_detailed'")],
  ['compact university cards', redesignCss.includes('grid-template-columns: 34px minmax(0, 1fr) 116px') && redesignCss.includes('min-height: 60px') && redesignCss.includes('The rank marker is hidden here')],
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
