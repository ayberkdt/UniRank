let rawData = [];
let filteredData = [];
let selectedCountries = new Set();
let selectedCategoryKeys = new Set();
let favorites = new Set(window.uniStorage.readArray('unirank_favorites'));
let countryPickerEntries = [];
let countryPickerOpen = false;
let activeDrawerData = null;
let initialResearchDeepLinkHandled = false;


function validateRecordShape(record) {
  const issues = [];
  if (!window.uniDataAdapter) return issues;
  const n = window.uniDataAdapter.normalizeUniversityRecord(record);

  if (!n.universityName) issues.push("Missing university name");
  if (!n.programName) issues.push("Missing program name");
  if (!n.country) issues.push("Missing country");
  if (!n.degree) issues.push("Missing degree");
  if (!n.tuitionPerYear && !n.totalAcademicCost && !n.foreignTuition) issues.push("Missing tuition/cost");

  return issues;
}

// Utility Functions
function formatMoney(amount) {
    return formatMoneySafe(amount);
    const val = parseFloat(amount);
    if (isNaN(val)) return '—';
    if (val === 0) return window.t ? window.t('free') : 'Free';
    return '€' + val.toLocaleString('en-US');
}

function formatMoneySafe(amount) {
    const value = parseFloat(amount);
    if (!Number.isFinite(value)) return "\u2014";
    if (value === 0) return window.t ? window.t('free') : 'Free';
    return `\u20AC${value.toLocaleString('en-US')}`;
}

// Alternate spellings and translations used across country files for the
// same institution or programme. Without these, "University of Padua" and
// "University of Padova" rank as two different universities.
const UNIVERSITY_NAME_ALIASES = {
    'padua': 'padova',
    'turin': 'torino',
    'milan': 'milano',
    'rome': 'roma'
};
const PROGRAMME_NAME_ALIASES = {
    'ingegneria aerospaziale': 'aerospace engineering',
    'ingegneria aeronautica': 'aeronautical engineering',
    'ingegneria spaziale': 'space engineering'
};

function canonicalUniversityKey(value) {
    let text = String(value || '')
        .toLocaleLowerCase('en-US')
        .normalize('NFD')
        .replace(/[̀-ͯ]/g, '')
        .replace(/[^a-z0-9]+/g, ' ')
        .trim()
        .replace(/\b(university|universita|universite|universitat|universiteit|degli|studi|di|of|the|la|del|della)\b/g, ' ')
        .replace(/\s+/g, ' ')
        .trim();
    for (const [from, to] of Object.entries(UNIVERSITY_NAME_ALIASES)) {
        text = text.replace(new RegExp(`\\b${from}\\b`, 'g'), to);
    }
    return text;
}

function canonicalProgrammeKey(value) {
    let text = String(value || '')
        .toLocaleLowerCase('en-US')
        .normalize('NFD')
        .replace(/[̀-ͯ]/g, '')
        .replace(/[^a-z0-9]+/g, ' ')
        .trim()
        // Degree qualifiers are already captured by the degree part of the key.
        .replace(/\b(master of science in|laurea magistrale in|master s degree in|m sc|msc|b sc|bsc|master|lm \d+|lm)\b/g, ' ')
        .replace(/\s+/g, ' ')
        .trim()
        .replace(/^in\s+/, '');
    for (const [from, to] of Object.entries(PROGRAMME_NAME_ALIASES)) {
        text = text.replace(from, to);
    }
    return text;
}

function canonicalDegreeKey(value) {
    const text = String(value || '').toLocaleLowerCase('en-US');
    if (/(doctor|phd)/.test(text)) return 'phd';
    if (/(master|msc|m sc|magistrale)/.test(text)) return 'msc';
    if (/(bachelor|bsc|b sc|lisans|first cycle)/.test(text)) return 'bsc';
    return text.replace(/[^a-z0-9]+/g, ' ').trim();
}

function duplicateProgrammeKey(record) {
    const normalized = window.uniDataAdapter?.normalizeUniversityRecord(record);
    const key = [
        String(normalized?.country || '').toLocaleLowerCase('en-US').replace(/[^a-z0-9]+/g, ' ').trim(),
        canonicalUniversityKey(window.uniDataAdapter?.localizedField(normalized?.universityName) || normalized?.universityName),
        canonicalProgrammeKey(window.uniDataAdapter?.localizedField(normalized?.programName) || normalized?.programName),
        canonicalDegreeKey(normalized?.degreeLevel || normalized?.degree)
    ];
    return key.every(Boolean) ? key.join('|') : `id:${record?.id || normalized?.id || Math.random()}`;
}

function recordPreference(record) {
    const quality = record?.data_quality || {};
    const statusRank = { verified: 3, partial: 2, needs_verification: 1 }[quality.status] || 0;
    return [
        statusRank,
        Array.isArray(quality.verified_fields) ? quality.verified_fields.length : 0,
        Array.isArray(record?.source_profile?.source_log) ? record.source_profile.source_log.length : 0,
        String(record?.source_profile?.last_verified || record?.updated_at || '')
    ];
}

function compareRecordPreference(left, right) {
    const a = recordPreference(left);
    const b = recordPreference(right);
    for (let index = 0; index < a.length; index += 1) {
        if (a[index] === b[index]) continue;
        return a[index] > b[index] ? 1 : -1;
    }
    return 0;
}

function deduplicateProgrammeRecords(records) {
    const selected = new Map();
    for (const record of Array.isArray(records) ? records : []) {
        const key = duplicateProgrammeKey(record);
        const existing = selected.get(key);
        if (!existing || compareRecordPreference(record, existing) > 0) selected.set(key, record);
    }
    // Second pass: within the same university and degree, a programme name
    // that extends another one ("… Engineering" vs "… Engineering, Space
    // Systems track") is the same record written with a longer title.
    const keys = [...selected.keys()];
    for (const key of keys) {
        if (!selected.has(key)) continue;
        const parts = key.split('|');
        if (parts.length !== 4) continue;
        for (const otherKey of keys) {
            if (otherKey === key || !selected.has(otherKey) || !selected.has(key)) continue;
            const otherParts = otherKey.split('|');
            if (otherParts.length !== 4) continue;
            if (parts[0] !== otherParts[0] || parts[1] !== otherParts[1] || parts[3] !== otherParts[3]) continue;
            const shorter = parts[2].length <= otherParts[2].length ? parts[2] : otherParts[2];
            const longer = parts[2].length <= otherParts[2].length ? otherParts[2] : parts[2];
            if (shorter.length < 8 || !longer.startsWith(`${shorter} `)) continue;
            const keep = compareRecordPreference(selected.get(key), selected.get(otherKey)) >= 0 ? key : otherKey;
            const drop = keep === key ? otherKey : key;
            selected.delete(drop);
        }
    }
    return [...selected.values()];
}

function isUndergraduateProgramme(record) {
    const normalized = window.uniDataAdapter?.normalizeUniversityRecord(record);
    const degreeText = [
        record?.degree_level,
        record?.program_degree,
        record?.target_program_degree,
        record?.Program_Degree,
        record?.degree,
        normalized?.degreeLevel,
        normalized?.degree,
    ].map(value => String(value || '')).join(' ').toLowerCase();
    return /\b(bachelor|b\.\s*sc\.?|bsc|undergraduate|first[- ]cycle|lisans)\b/.test(degreeText)
        || (degreeText.includes('diplom') && degreeText.includes('direct'));
}

function formatPublishedMoney(money) {
    return formatPublishedMoneySafe(money);
    if (!money || money.amount === null || money.amount === undefined || !money.currency) return 'â€”';
    const amount = Number(money.amount);
    if (!Number.isFinite(amount)) return 'â€”';
    const currency = String(money.currency).toUpperCase();
    try {
        return new Intl.NumberFormat('en-US', { style: 'currency', currency, maximumFractionDigits: 2 }).format(amount);
    } catch {
        return `${amount.toLocaleString('en-US')} ${currency}`;
    }
}

function formatPublishedMoneySafe(money) {
    if (!money || money.amount === null || money.amount === undefined || !money.currency) return "\u2014";
    const amount = Number(money.amount);
    if (!Number.isFinite(amount)) return "\u2014";
    const currency = String(money.currency).toUpperCase();
    try {
        return new Intl.NumberFormat('en-US', { style: 'currency', currency, maximumFractionDigits: 2 }).format(amount);
    } catch {
        return `${amount.toLocaleString('en-US')} ${currency}`;
    }
}

function formatPublishedRange(range) {
    return formatPublishedRangeSafe(range);
    if (!range || !range.currency || range.min === null || range.min === undefined) return 'â€”';
    const start = formatPublishedMoney({ amount: range.min, currency: range.currency });
    const end = range.max !== null && range.max !== undefined && Number(range.max) !== Number(range.min)
        ? formatPublishedMoney({ amount: range.max, currency: range.currency })
        : '';
    return end ? `${start}–${end}` : start;
}

function formatPublishedTuition(value) {
    if (!value) return '\u2014';
    const amount = value.amount !== null && value.amount !== undefined
        ? formatPublishedMoney(value)
        : formatPublishedRange(value);
    if (!value.isHistorical) return amount;
    const year = value.academicYear ? `${value.academicYear} ` : '';
    const context = window.currentLanguage === 'tr'
        ? `${year}tarihsel ölçüt; güncel değil`
        : `${year}historical benchmark; not current`;
    return `${amount} · ${context}`;
}

function publishedTuitionPeriodSuffix(value, isTurkish) {
    if (!value) return '';
    if (value.period === 'quarter') return isTurkish ? ' / dönem' : ' / quarter';
    if (value.period === 'academic_year') return isTurkish ? ' / akademik yıl' : ' / academic year';
    return isTurkish ? ' / yıl' : ' / year';
}

function formatPublishedRangeSafe(range) {
    if (!range || !range.currency || range.min === null || range.min === undefined) return "\u2014";
    const start = formatPublishedMoneySafe({ amount: range.min, currency: range.currency });
    const end = range.max !== null && range.max !== undefined && Number(range.max) !== Number(range.min)
        ? formatPublishedMoneySafe({ amount: range.max, currency: range.currency })
        : '';
    return end ? `${start}\u2013${end}` : start;
}

function escapeHtml(value) {
    return String(value ?? '')
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}

function safeUrl(value) {
    if (!value) return '';
    try {
        const parsed = new URL(String(value));
        return ['http:', 'https:'].includes(parsed.protocol) ? parsed.href : '';
    } catch {
        return '';
    }
}

function getAnnualCost(record) {
    const normalized = window.uniDataAdapter ? window.uniDataAdapter.normalizeUniversityRecord(record) : null;
    const value = normalized?.totalAcademicCost ?? normalized?.tuitionPerYear;
    const number = value === null || value === undefined || value === '' ? null : Number(value);
    return Number.isFinite(number) ? number : null;
}

function displayValue(val) {
    if (val === null || val === undefined || val === '') return "\u2014";
    let output;
    if (window.localizedField) {
        const loc = window.localizedField(val);
        output = loc ? loc : '—';
    } else {
        output = String(val);
    }

    if (typeof output !== 'string' || output.includes('://')) return output;
    const token = output.trim();
    if (!/^[a-z0-9]+(?:_[a-z0-9]+)+$/i.test(token)) return token;

    const normalized = token.toLowerCase();
    const labels = window.currentLanguage === 'tr'
        ? {
            not_listed_as_required_or_scored_in_checked_2026_27_programme_sources: 'Kontrol edilen 2026/27 program kaynaklarında zorunlu veya puanlanan bir ölçüt olarak listelenmiyor',
            not_listed_as_required_or_recommended_for_this_programme: 'Bu program için zorunlu veya önerilen bir ölçüt olarak listelenmiyor',
            limited_place_merit_ranking: 'Kontenjanı sınırlı başarı sıralaması',
            conditional_if_documents_are_insufficient: 'Yalnızca belgeler değerlendirme için yetersizse koşullu mülakat',
            document_based_competitive_selection: 'Belge temelli rekabetçi seçim',
            possible_but_not_guaranteed: 'Mümkün, ancak garanti değil',
            individual_email_deadline: 'Tarih kabul sonrası kişisel e-postayla bildirilir',
            individual_relative_deadline: 'Kabul sonrası bildirilen göreli süre'
        }
        : {
            not_listed_as_required_or_scored_in_checked_2026_27_programme_sources: 'Not listed as required or scored in the checked 2026/27 programme sources',
            not_listed_as_required_or_recommended_for_this_programme: 'Not listed as required or recommended for this programme',
            limited_place_merit_ranking: 'Limited-place merit ranking',
            conditional_if_documents_are_insufficient: 'Conditional interview only when documents are insufficient for assessment',
            document_based_competitive_selection: 'Document-based competitive selection',
            possible_but_not_guaranteed: 'Possible, but not guaranteed',
            individual_email_deadline: 'Date is communicated individually after admission',
            individual_relative_deadline: 'Relative deadline communicated after admission'
        };
    if (labels[normalized]) return labels[normalized];

    return token
        .replace(/_+/g, ' ')
        .replace(/\bnon eu\b/gi, window.currentLanguage === 'tr' ? 'AB dışı' : 'non-EU')
        .replace(/\bprogramme\b/gi, window.currentLanguage === 'tr' ? 'program' : 'programme')
        .replace(/^./, character => character.toUpperCase());
}

function formatCalendarValue(value) {
    const text = displayValue(value);
    return text.replace(/\b(20\d{2})-(\d{2})-(\d{2})(?:T\d{2}:\d{2}(?::\d{2})?(?:Z|[+-]\d{2}:?\d{2})?)?/g, (raw, yearText, monthText, dayText) => {
        const year = Number(yearText);
        const month = Number(monthText);
        const day = Number(dayText);
        const date = new Date(year, month - 1, day, 12, 0, 0);
        if (date.getFullYear() !== year || date.getMonth() !== month - 1 || date.getDate() !== day) return raw;
        return new Intl.DateTimeFormat(window.currentLanguage === 'tr' ? 'tr-TR' : 'en-GB', {
            weekday: 'long', day: 'numeric', month: 'long', year: 'numeric'
        }).format(date);
    });
}

// Database enum values ("high", "Moderate", "Bilinmiyor / Resmi Veri Yok",
// "nightmare"…) must never reach the screen raw: they are mapped to a
// severity key and shown as a translated, colour-coded badge.
function levelInfo(value) {
    const raw = String(value ?? '').trim().toLowerCase();
    let key = 'unknown';
    if (/(nightmare|very[\s_]?high|very[\s_]?hard)/.test(raw)) key = 'very_high';
    else if (/(high|hard|difficult)/.test(raw)) key = 'high';
    else if (/(medium|moderate)/.test(raw)) key = 'medium';
    else if (/(low|safe|easy)/.test(raw)) key = 'low';
    const label = window.t ? window.t(`level_${key}`) : key;
    return { key, label };
}

function formatRiskBadge(risk) {
    const level = levelInfo(risk);
    const cssKey = level.key === 'very_high' ? 'high' : level.key;
    return `<span class="risk-badge risk-${cssKey}">${escapeHtml(level.label)}</span>`;
}

function scoreBand(score) {
    const value = Number(score) || 0;
    if (value >= 6.5) return { key: 'excellent', label: window.currentLanguage === 'tr' ? 'Güçlü genel sonuç' : 'Strong overall result' };
    if (value >= 5.5) return { key: 'strong', label: window.currentLanguage === 'tr' ? 'İyi genel sonuç' : 'Good overall result' };
    if (value >= 4.5) return { key: 'moderate', label: window.currentLanguage === 'tr' ? 'Orta genel sonuç' : 'Moderate overall result' };
    return { key: 'weak', label: window.currentLanguage === 'tr' ? 'Sınırlı genel sonuç' : 'Limited overall result' };
}

function compactList(value) {
    if (Array.isArray(value)) return value.map(displayValue).filter(Boolean).join(', ');
    return displayValue(value);
}

function formatTeachingLanguages(value) {
    const values = Array.isArray(value) ? value : [value];
    const turkishLabels = {
        English: 'İngilizce', Spanish: 'İspanyolca', German: 'Almanca', French: 'Fransızca',
        Italian: 'İtalyanca', Portuguese: 'Portekizce', Dutch: 'Felemenkçe', Swedish: 'İsveççe',
        Danish: 'Danca', Norwegian: 'Norveççe', Finnish: 'Fince', Romanian: 'Romence',
        Greek: 'Yunanca', Polish: 'Lehçe', Czech: 'Çekçe', Russian: 'Rusça', Turkish: 'Türkçe',
        Estonian: 'Estonca', Lithuanian: 'Litvanca', Unknown: 'Bilinmiyor',
        needs_verification: 'Doğrulama gerekli', not_verified: 'Doğrulanmadı'
    };
    return values
        .map(displayValue)
        .filter(Boolean)
        .map(language => window.currentLanguage === 'tr' ? (turkishLabels[language] || language) : language)
        .join(', ');
}

function confidenceLabel(value) {
    const normalized = ['high', 'medium', 'low'].includes(String(value).toLowerCase())
        ? String(value).toLowerCase()
        : 'unknown';
    const key = `confidence_${normalized}`;
    return {
        key: normalized,
        label: window.t ? window.t(key) : normalized
    };
}

// CSS-only flag textures keep every country card visually distinct without
// adding external image requests to the ranked-results view.
const COUNTRY_VISUALS = {
    austria: { accent: '#ed2939', rgb: '237, 41, 57', flag: 'linear-gradient(to bottom, #ed2939 0 33%, #ffffff 33% 66%, #ed2939 66% 100%)' },
    belgium: { accent: '#f2bd28', rgb: '242, 189, 40', flag: 'linear-gradient(90deg, #191919 0 33%, #f2bd28 33% 66%, #d4303d 66% 100%)' },
    china: { accent: '#e53a3e', rgb: '229, 58, 62', flag: 'url("https://flagcdn.com/w320/cn.png") center right / cover no-repeat' },
    czechia: { accent: '#d73445', rgb: '215, 52, 69', flag: 'url("https://flagcdn.com/w320/cz.png") center right / cover no-repeat' },
    denmark: { accent: '#c8102e', rgb: '200, 16, 46', flag: 'linear-gradient(90deg, transparent 0 29%, #ffffff 29% 40%, transparent 40% 100%), linear-gradient(transparent 0 41%, #ffffff 41% 58%, transparent 58% 100%), #c8102e' },
    estonia: { accent: '#4891d9', rgb: '72, 145, 217', flag: 'linear-gradient(to bottom, #4891d9 0 33%, #17191e 33% 66%, #f7f7f3 66% 100%)' },
    finland: { accent: '#2f70b7', rgb: '47, 112, 183', flag: 'linear-gradient(90deg, transparent 0 30%, #2f70b7 30% 43%, transparent 43% 100%), linear-gradient(transparent 0 40%, #2f70b7 40% 57%, transparent 57% 100%), #f7f7f3' },
    france: { accent: '#2d57a1', rgb: '45, 87, 161', flag: 'linear-gradient(90deg, #21468b 0 33%, #f7f8fa 33% 66%, #ef4135 66% 100%)' },
    germany: { accent: '#d9a620', rgb: '217, 166, 32', flag: 'linear-gradient(to bottom, #1a1a1a 0 33%, #d83232 33% 66%, #e2b42a 66% 100%)' },
    greece: { accent: '#3474bb', rgb: '52, 116, 187', flag: 'url("https://flagcdn.com/w320/gr.png") center right / cover no-repeat' },
    ireland: { accent: '#169b62', rgb: '22, 155, 98', flag: 'linear-gradient(90deg, #169b62 0 33%, #f7f7f3 33% 66%, #ff883e 66% 100%)' },
    italy: { accent: '#159447', rgb: '21, 148, 71', flag: 'linear-gradient(90deg, #009246 0 33%, #f7f8f6 33% 66%, #ce2b37 66% 100%)' },
    japan: { accent: '#dc3044', rgb: '220, 48, 68', flag: 'radial-gradient(circle at 50% 50%, #cf2738 0 22%, transparent 22.5%), #f8f8f4' },
    lithuania: { accent: '#f3b61f', rgb: '243, 182, 31', flag: 'linear-gradient(to bottom, #fdb913 0 33%, #006a44 33% 66%, #c1272d 66% 100%)' },
    netherlands: { accent: '#2d62ad', rgb: '45, 98, 173', flag: 'linear-gradient(to bottom, #ae1c28 0 33%, #f7f8f6 33% 66%, #21468b 66% 100%)' },
    norway: { accent: '#ba0c2f', rgb: '186, 12, 47', flag: 'url("https://flagcdn.com/w320/no.png") center right / cover no-repeat' },
    poland: { accent: '#d92b48', rgb: '217, 43, 72', flag: 'linear-gradient(to bottom, #fafafa 0 50%, #d22645 50% 100%)' },
    portugal: { accent: '#d84536', rgb: '216, 69, 54', flag: 'url("https://flagcdn.com/w320/pt.png") center right / cover no-repeat' },
    romania: { accent: '#f7c600', rgb: '247, 198, 0', flag: 'linear-gradient(90deg, #002b7f 0 33%, #fcd116 33% 66%, #ce1126 66% 100%)' },
    russia: { accent: '#4366ae', rgb: '67, 102, 174', flag: 'linear-gradient(to bottom, #f7f7f5 0 33%, #3156a6 33% 66%, #ce303c 66% 100%)' },
    south_korea: { accent: '#d43848', rgb: '212, 56, 72', flag: 'url("https://flagcdn.com/w320/kr.png") center right / cover no-repeat' },
    spain: { accent: '#efb933', rgb: '239, 185, 51', flag: 'linear-gradient(to bottom, #aa151b 0 25%, #f1bf36 25% 75%, #aa151b 75% 100%)' },
    sweden: { accent: '#e4b424', rgb: '228, 180, 36', flag: 'linear-gradient(90deg, transparent 0 29%, #f6cc38 29% 40%, transparent 40% 100%), linear-gradient(transparent 0 40%, #f6cc38 40% 57%, transparent 57% 100%), #2166a5' },
    switzerland: { accent: '#e13c43', rgb: '225, 60, 67', flag: 'linear-gradient(90deg, transparent 0 39%, #fff 39% 61%, transparent 61% 100%), linear-gradient(transparent 0 32%, #fff 32% 68%, transparent 68% 100%), #d52b1e' },
    turkey: { accent: '#e12d3c', rgb: '225, 45, 60', flag: 'url("https://flagcdn.com/w320/tr.png") center right / cover no-repeat' },
    united_kingdom: { accent: '#c8394d', rgb: '200, 57, 77', flag: 'url("https://flagcdn.com/w320/gb.png") center right / cover no-repeat' },
    usa: { accent: '#b9334a', rgb: '185, 51, 74', flag: 'url("https://flagcdn.com/w320/us.png") center right / cover no-repeat' }
};

function countryVisualKey(country) {
    const normalized = String(country || '')
        .trim()
        .toLocaleLowerCase('en-US')
        .normalize('NFD')
        .replace(/[\u0300-\u036f]/g, '')
        .replace(/[^a-z0-9]+/g, '_')
        .replace(/^_|_$/g, '');

    return {
        uk: 'united_kingdom',
        great_britain: 'united_kingdom',
        united_states: 'usa',
        united_states_of_america: 'usa',
        america: 'usa',
        republic_of_korea: 'south_korea',
        turkiye: 'turkey'
    }[normalized] || normalized;
}

function applyCountryVisual(element, country) {
    if (!element) return;
    const key = countryVisualKey(country);
    const visual = COUNTRY_VISUALS[key] || { accent: '#6f85a2', rgb: '111, 133, 162', flag: 'linear-gradient(135deg, #274261, #162a42)' };
    element.classList.add('country-themed');
    element.dataset.countryTheme = key || 'global';
    element.style.setProperty('--country-accent', visual.accent);
    element.style.setProperty('--country-rgb', visual.rgb);
    element.style.setProperty('--country-flag', visual.flag);
}

const COUNTRY_FLAG_CODES = {
    austria: 'AT',
    belgium: 'BE',
    china: 'CN',
    czech_republic: 'CZ',
    czechia: 'CZ',
    denmark: 'DK',
    estonia: 'EE',
    finland: 'FI',
    france: 'FR',
    germany: 'DE',
    greece: 'GR',
    ireland: 'IE',
    italy: 'IT',
    japan: 'JP',
    lithuania: 'LT',
    netherlands: 'NL',
    norway: 'NO',
    poland: 'PL',
    portugal: 'PT',
    romania: 'RO',
    russia: 'RU',
    south_korea: 'KR',
    spain: 'ES',
    sweden: 'SE',
    switzerland: 'CH',
    turkey: 'TR',
    united_kingdom: 'GB',
    usa: 'US'
};

function countryFlagCode(country) {
    return COUNTRY_FLAG_CODES[countryVisualKey(country)] || '';
}

function countryVisualMeta(country) {
    const key = countryVisualKey(country);
    const visual = COUNTRY_VISUALS[key] || { accent: '#6f85a2', rgb: '111, 133, 162', flag: 'linear-gradient(135deg, #274261, #162a42)' };
    return { key, code: COUNTRY_FLAG_CODES[key] || '', ...visual };
}

window.uniCountryVisual = countryVisualMeta;

function renderCountryFlag(container, country) {
    if (!container) return;
    const code = countryFlagCode(country);
    container.innerHTML = '';
    if (!code) {
        container.textContent = '🌐';
        return;
    }

    const image = document.createElement('img');
    image.src = `https://flagcdn.com/w40/${code.toLowerCase()}.png`;
    image.alt = '';
    image.width = 28;
    image.height = 20;
    image.loading = 'lazy';
    image.decoding = 'async';
    image.addEventListener('error', () => {
        container.innerHTML = '';
        container.textContent = code;
    }, { once: true });
    container.appendChild(image);
}

// Global Boundaries for Normalization
let globalMaxTuition = 10000;
let globalMinTuition = 0;
let globalMaxRank = 1000;
let globalMinRank = 1;

// DOM Elements
const els = {
    countryFilter: document.getElementById('country-filter'),
    countryTags: document.getElementById('country-tags'),
    countryPicker: {
        trigger: document.getElementById('country-picker-trigger'),
        triggerFlag: document.getElementById('country-picker-trigger-flag'),
        value: document.getElementById('country-picker-value'),
        count: document.getElementById('country-picker-count'),
        popover: document.getElementById('country-picker-popover'),
        search: document.getElementById('country-picker-search'),
        options: document.getElementById('country-picker-options'),
        empty: document.getElementById('country-picker-empty'),
        clear: document.getElementById('country-picker-clear')
    },
    categorySearchInput: document.getElementById('categorySearchInput'),
    categorySuggestions: document.getElementById('categorySuggestions'),
    selectedCategoryChips: document.getElementById('selectedCategoryChips'),
    popularCategoryChips: document.getElementById('popularCategoryChips'),
    favFilter: document.getElementById('fav-filter'),
    searchInput: document.getElementById('search-input'),
    sortSelect: document.getElementById('sort-select'),
    hardFilters: {
        degree: document.getElementById('degree-filter'),
        englishOnly: document.getElementById('english-only-filter'),
        maxTuition: document.getElementById('max-tuition-filter')
    },
    preset: document.getElementById('preset-profile-select'),
    weights: {
        academic: document.getElementById('w-academic'),
        eligibility: document.getElementById('w-eligibility'),
        cost: document.getElementById('w-cost'),
        career: document.getElementById('w-career'),
        living: document.getElementById('w-living'),
        confidence: document.getElementById('w-confidence')
    },
    vals: {
        academic: document.getElementById('val-academic'),
        eligibility: document.getElementById('val-eligibility'),
        cost: document.getElementById('val-cost'),
        career: document.getElementById('val-career'),
        living: document.getElementById('val-living'),
        confidence: document.getElementById('val-confidence')
    },
    kpi: {
        total: document.getElementById('kpi-total'),
        sourceCoverage: document.getElementById('kpi-source-coverage'),
        mapCoverage: document.getElementById('kpi-map-coverage'),
        score: document.getElementById('kpi-score')
    },
    tableBody: document.getElementById('table-body'),
    drawer: {
        overlay: document.getElementById('drawer-overlay'),
        panel: document.getElementById('detail-drawer'),
        title: document.getElementById('drawer-title'),
        body: document.getElementById('drawer-body'),
        closeBtn: document.getElementById('drawer-close'),
        favBtn: document.getElementById('drawer-fav-btn')
    }
};

function toggleFavorite(id) {
    if (favorites.has(id)) {
        favorites.delete(id);
        if (window.removeFavorite) window.removeFavorite(id);
    } else {
        favorites.add(id);
        if (window.addFavorite) window.addFavorite(id);
    }
window.uniStorage.writeJSON('unirank_favorites', Array.from(favorites));
    processAndRender();
}

// Initialize
async function init() {
    if (window.initAuth) await window.initAuth();

    if (window.currentUser) {
        const authFavs = window.uniStorage.readArray('unirank_demo_favs');
        authFavs.forEach(id => favorites.add(id));
    }

    if (window.updateAuthUI) window.updateAuthUI();

    setupEventListeners();
    initSpotlightCards();
    await fetchData();
    window.applyTranslations();
}

function initSpotlightCards() {
    document.addEventListener("mousemove", (e) => {
        document.querySelectorAll(".kpi-card").forEach(card => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            card.style.setProperty("--mouse-x", `${x}px`);
            card.style.setProperty("--mouse-y", `${y}px`);
        });
    });
}

// Fetch Data
let dataRefreshInFlight = false;

async function fetchData({ silent = false } = {}) {
    if (dataRefreshInFlight) return false;
    dataRefreshInFlight = true;
    const loader = document.getElementById('loader');
    if (loader && !silent) loader.classList.add('active');
    try {
        const res = await fetch('/api/universities');
        if (!res.ok) throw new Error(`API request failed (${res.status})`);
        const json = await res.json();
        
        if (json.status === 'success') {
            
            // The API already removes exact programme clones. This client-side
            // guard also protects people viewing an older cached deployment.
            rawData = deduplicateProgrammeRecords(json.data.filter(record => !isUndergraduateProgramme(record)));
            window.uniRankRecords = rawData;
            window.dispatchEvent(new CustomEvent('unirank:recordsLoaded', {
                detail: { records: rawData, refreshedAt: new Date().toISOString(), silent }
            }));
            rawData.slice(0, 20).forEach((r) => {
              const issues = validateRecordShape(r);
              if (issues.length) console.warn("Record shape issues:", r.id || r.name, issues);
            });

            
            // Calculate Global Boundaries for Min-Max Normalization
            if (rawData.length > 0) {
                globalMaxTuition = Math.max(...rawData.map(r => parseFloat(r.tuition_eur_per_year) || 0));
                globalMinTuition = Math.min(...rawData.map(r => parseFloat(r.tuition_eur_per_year) || 0));
                if (globalMaxTuition === globalMinTuition) globalMaxTuition = globalMinTuition + 1; // Prevent division by zero
                
                const validRanks = rawData.map(r => r.qs_ranking).filter(r => r && r <= 1000);
                globalMaxRank = validRanks.length > 0 ? Math.max(...validRanks) : 1000;
                globalMinRank = validRanks.length > 0 ? Math.min(...validRanks) : 1;
                if (globalMaxRank === globalMinRank) globalMaxRank = globalMinRank + 1;
            }

            populateCountryFilter();
            if (window.renderCategoryUI) window.renderCategoryUI();
            
            // Pre-calculate category profiles synchronously for the UI
            for (let r of rawData) {
                if (!r.Category_Profile && typeof window.buildCategoryProfile === 'function') {
                    r.Category_Profile = await window.buildCategoryProfile(r);
                }
            }
            
            await applyInitialResearchDeepLink();
            processAndRender();
            return true;
        } else {
            console.error("API Error:", json.message);
            if (!silent) els.tableBody.innerHTML = `<div class="empty-results-card" role="alert"><h3>${escapeHtml(json.message || 'API request failed.')}</h3></div>`;
            return false;
        }
    } catch (err) {
        if (silent) console.warn("Background data refresh failed:", err);
        else {
            console.error("Fetch Error:", err);
            els.tableBody.innerHTML = `<div class="empty-results-card" role="alert"><h3>${escapeHtml(err.message || 'Network request failed.')}</h3></div>`;
        }
        return false;
    } finally {
        dataRefreshInFlight = false;
        if (loader && !silent) loader.classList.remove('active');
    }
}

async function applyInitialResearchDeepLink() {
    if (initialResearchDeepLinkHandled) return;
    initialResearchDeepLinkHandled = true;
    const params = new URLSearchParams(window.location.search);
    const requestedProgram = params.get('program');
    const requestedField = params.get('field');

    if (requestedField) {
        const taxonomy = await window.loadTaxonomy?.();
        if (taxonomy?.[requestedField]) selectedCategoryKeys.add(requestedField);
    }

    if (!requestedProgram) return;
    const record = rawData.find((item) => {
        const normalized = window.uniDataAdapter?.normalizeUniversityRecord(item);
        return normalized?.id === requestedProgram || item.id === requestedProgram || item.programme_id === requestedProgram;
    });
    if (record) window.requestAnimationFrame(() => openDrawer(record));
}

window.refreshUniRankData = function() {
    return fetchData({ silent: true });
};

const UI_WEIGHT_KEYS = ['academic', 'eligibility', 'cost', 'career', 'living', 'confidence'];
const DEFAULT_UI_WEIGHTS = { academic: 30, eligibility: 20, cost: 20, career: 15, living: 10, confidence: 5 };

function sanitizeUiWeight(value) {
    const numeric = Number(value);
    return Number.isFinite(numeric) ? Math.min(100, Math.max(0, Math.round(numeric))) : 0;
}

function distributeIntegerWeight(total, keys, basis) {
    if (!keys.length) return {};
    const basisTotal = keys.reduce((sum, key) => sum + sanitizeUiWeight(basis[key]), 0);
    const allocations = keys.map((key, index) => {
        const ratio = basisTotal > 0 ? sanitizeUiWeight(basis[key]) / basisTotal : 1 / keys.length;
        const raw = ratio * total;
        return { key, index, value: Math.floor(raw), fraction: raw - Math.floor(raw) };
    });
    let remainder = total - allocations.reduce((sum, item) => sum + item.value, 0);
    allocations.sort((left, right) => right.fraction - left.fraction || left.index - right.index);
    for (let index = 0; index < allocations.length && remainder > 0; index += 1, remainder -= 1) {
        allocations[index].value += 1;
    }
    return Object.fromEntries(allocations.map(item => [item.key, item.value]));
}

function readUiWeights() {
    return Object.fromEntries(UI_WEIGHT_KEYS.map(key => [key, sanitizeUiWeight(els.weights[key]?.value)]));
}

function applyUiWeights(weights) {
    UI_WEIGHT_KEYS.forEach(key => {
        const value = sanitizeUiWeight(weights[key]);
        if (els.weights[key]) els.weights[key].value = String(value);
        if (els.vals[key]) els.vals[key].textContent = `${value}%`;
    });
    const total = UI_WEIGHT_KEYS.reduce((sum, key) => sum + sanitizeUiWeight(weights[key]), 0);
    const totalElement = document.getElementById('weight-total');
    if (totalElement) totalElement.textContent = `${total}%`;
}

function rebalanceUiWeights(changedKey, requestedValue) {
    const changedValue = sanitizeUiWeight(requestedValue);
    const current = readUiWeights();
    const otherKeys = UI_WEIGHT_KEYS.filter(key => key !== changedKey);
    const redistributed = distributeIntegerWeight(100 - changedValue, otherKeys, current);
    const next = { ...redistributed, [changedKey]: changedValue };
    applyUiWeights(next);
    return next;
}

window.uniWeighting = { read: readUiWeights, rebalance: rebalanceUiWeights };

function setupEventListeners() {
    initCountryPicker();

    // Presets
    if (els.preset) {
        els.preset.addEventListener('change', (e) => {
            const p = e.target.value;
            let w = {};
            if (p === 'balanced') w = { academic: 30, eligibility: 20, cost: 20, career: 15, living: 10, confidence: 5 };
            else if (p === 'low_cost') w = { academic: 20, eligibility: 20, cost: 35, career: 10, living: 10, confidence: 5 };
            else if (p === 'best_fit') w = { academic: 45, eligibility: 15, cost: 10, career: 20, living: 5, confidence: 5 };
            else if (p === 'safe_choice') w = { academic: 25, eligibility: 35, cost: 15, career: 10, living: 10, confidence: 5 };
            else if (p === 'career') w = { academic: 25, eligibility: 15, cost: 10, career: 35, living: 10, confidence: 5 };
            
            if (p !== 'custom' && Object.keys(w).length > 0) {
                applyUiWeights(w);
                clearTimeout(window.renderTimeout);
                window.renderTimeout = setTimeout(processAndRender, 100);
            }
        });
    }

    // Weights
    Object.keys(els.weights).forEach(k => {
        if (els.weights[k]) {
            els.weights[k].addEventListener('input', (e) => {
                rebalanceUiWeights(k, e.target.value);
                if (els.preset) els.preset.value = 'custom';
                // Debounce re-render slightly
                clearTimeout(window.renderTimeout);
                window.renderTimeout = setTimeout(processAndRender, 100);
            });
        }
    });

    applyUiWeights(DEFAULT_UI_WEIGHTS);

    // Hard Filters
    Object.keys(els.hardFilters).forEach(k => {
        if (els.hardFilters[k]) {
            els.hardFilters[k].addEventListener('change', processAndRender);
            if (els.hardFilters[k].type === 'number' || els.hardFilters[k].type === 'range') {
                els.hardFilters[k].addEventListener('input', (e) => {
                    if (k === 'maxTuition') {
                        const valDisplay = document.getElementById('tuition-val-display');
                        if (valDisplay) {
                            if (e.target.value >= 25000) {
                                valDisplay.textContent = 'Any';
                            } else {
                                valDisplay.textContent = `≤ €${Number(e.target.value).toLocaleString('en-US')}`;
                            }
                        }
                    }
                    clearTimeout(window.renderTimeout);
                    window.renderTimeout = setTimeout(processAndRender, 200);
                });
            }
        }
    });

    // Keep the hidden native control as a compatibility hook for existing
    // integrations while the visible, accessible picker owns interaction.
    els.countryFilter.addEventListener('change', (event) => {
        const country = event.target.value;
        if (country) toggleCountrySelection(country, true);
        event.target.value = '';
    });

    // Category listener is attached inside populateCategoryTree
    
    // city filter listener removed
    els.favFilter.addEventListener('change', processAndRender);
    els.searchInput.addEventListener('input', () => {
        clearTimeout(window.searchTimeout);
        window.searchTimeout = setTimeout(processAndRender, 200);
    });
    
    // Sorting
    els.sortSelect.addEventListener('change', processAndRender);
    
    // Drawer close
    els.drawer.closeBtn.addEventListener('click', closeDrawer);
    els.drawer.overlay.addEventListener('click', closeDrawer);

    const filterToggle = document.getElementById('filter-toggle');
    const sidebarClose = document.getElementById('sidebar-close');
    const sidebarScrim = document.getElementById('sidebar-scrim');
    if (filterToggle) filterToggle.addEventListener('click', () => setFilterSidebar(true));
    if (sidebarClose) sidebarClose.addEventListener('click', () => setFilterSidebar(false));
    if (sidebarScrim) sidebarScrim.addEventListener('click', () => setFilterSidebar(false));

    ['clear-filters-sidebar', 'clear-active-filters'].forEach(id => {
        const button = document.getElementById(id);
        if (button) button.addEventListener('click', clearAllFilters);
    });

    document.addEventListener('keydown', event => {
        if (event.key !== 'Escape') return;
        if (countryPickerOpen) closeCountryPicker(true);
        else if (els.drawer.panel.classList.contains('active')) closeDrawer();
        else setFilterSidebar(false);
    });

    const sidebarBreakpoint = window.matchMedia('(max-width: 1100px)');
    const handleSidebarBreakpoint = () => setFilterSidebar(false);
    if (sidebarBreakpoint.addEventListener) sidebarBreakpoint.addEventListener('change', handleSidebarBreakpoint);
    else sidebarBreakpoint.addListener(handleSidebarBreakpoint);
    setFilterSidebar(false);
}

function setFilterSidebar(open) {
    const isOpen = Boolean(open);
    const wasOpen = document.body.classList.contains('filters-open');
    if (!isOpen && countryPickerOpen) closeCountryPicker();
    if (isOpen && !wasOpen) window.lastFilterTrigger = document.activeElement;
    document.body.classList.toggle('filters-open', isOpen);
    const toggle = document.getElementById('filter-toggle');
    if (toggle) toggle.setAttribute('aria-expanded', String(isOpen));
    const sidebar = document.getElementById('filter-sidebar');
    if (sidebar) sidebar.setAttribute('aria-hidden', String(!isOpen && window.matchMedia('(max-width: 1100px)').matches));
    if (isOpen) document.getElementById('sidebar-close')?.focus();
    else if (wasOpen && window.lastFilterTrigger instanceof HTMLElement) window.lastFilterTrigger.focus();
}

function clearAllFilters() {
    selectedCountries.clear();
    selectedCategoryKeys.clear();
    if (els.searchInput) els.searchInput.value = '';
    if (els.categorySearchInput) els.categorySearchInput.value = '';
    if (els.categorySuggestions) els.categorySuggestions.innerHTML = '';
    if (els.hardFilters.degree) els.hardFilters.degree.value = 'All';
    if (els.hardFilters.englishOnly) els.hardFilters.englishOnly.checked = false;
    if (els.hardFilters.maxTuition) els.hardFilters.maxTuition.value = '25000';
    if (els.favFilter) els.favFilter.checked = false;
    const tuitionOutput = document.getElementById('tuition-val-display');
    if (tuitionOutput) tuitionOutput.textContent = 'Any';
    populateCountryFilter();
    renderCountryTags();
    renderSelectedCategories();
    renderPopularCategories();
    processAndRender();
}

function populateCountryFilter() {
    const countryCounts = new Map();
    rawData.forEach(record => {
        const normalized = window.uniDataAdapter ? window.uniDataAdapter.normalizeUniversityRecord(record) : null;
        const country = normalized?.country || record.country || record.Country;
        if (country) countryCounts.set(country, (countryCounts.get(country) || 0) + 1);
    });

    const locale = window.currentLanguage === 'tr' ? 'tr-TR' : 'en-US';
    countryPickerEntries = Array.from(countryCounts, ([country, count]) => ({
        country,
        count,
        label: window.getCountryName ? window.getCountryName(country) : country
    })).sort((a, b) => a.label.localeCompare(b.label, locale, { sensitivity: 'base' }));

    els.countryFilter.innerHTML = '';
    const defaultOption = document.createElement('option');
    defaultOption.value = '';
    defaultOption.textContent = window.t ? window.t('search_country') : 'Search country...';
    els.countryFilter.appendChild(defaultOption);

    countryPickerEntries.forEach(({ country, label }) => {
        const option = document.createElement('option');
        option.value = country;
        option.textContent = label;
        els.countryFilter.appendChild(option);
    });

    els.countryFilter.value = '';
    renderCountryPickerOptions(els.countryPicker.search?.value || '');
    updateCountryPickerTrigger();
    renderCountryTags();
}

window.renderCountryFilter = populateCountryFilter;

function updateCountryPickerTrigger() {
    if (!els.countryPicker.trigger) return;

    const selected = countryPickerEntries.filter(entry => selectedCountries.has(entry.country));
    const selectedCount = selectedCountries.size;
    let value = window.t ? window.t('country_picker_all') : 'All countries';
    let flag = '🌍';

    if (selectedCount === 1 && selected[0]) {
        value = selected[0].label;
        flag = '';
    } else if (selectedCount > 1) {
        value = `${selectedCount} ${window.t ? window.t('country_picker_selected') : 'countries selected'}`;
    }

    els.countryPicker.value.textContent = value;
    if (selectedCount === 1 && selected[0]) renderCountryFlag(els.countryPicker.triggerFlag, selected[0].country);
    else els.countryPicker.triggerFlag.textContent = flag;
    els.countryPicker.count.textContent = String(selectedCount);
    els.countryPicker.count.hidden = selectedCount === 0;
    els.countryPicker.clear.disabled = selectedCount === 0;
    els.countryPicker.trigger.setAttribute('aria-label', value);
}

function renderCountryPickerOptions(query = '') {
    if (!els.countryPicker.options) return;
    const normalize = window.normalizeSearchText || (value => String(value || '').toLowerCase().trim());
    const normalizedQuery = normalize(query);
    const visibleEntries = countryPickerEntries.filter(entry => (
        !normalizedQuery || normalize(`${entry.label} ${entry.country}`).includes(normalizedQuery)
    ));

    els.countryPicker.options.innerHTML = '';
    visibleEntries.forEach(entry => {
        const selected = selectedCountries.has(entry.country);
        const button = document.createElement('button');
        button.type = 'button';
        button.className = `country-picker-option${selected ? ' is-selected' : ''}`;
        button.dataset.country = entry.country;
        button.setAttribute('role', 'option');
        button.setAttribute('aria-selected', String(selected));

        const flag = document.createElement('span');
        flag.className = 'country-picker-option__flag';
        flag.setAttribute('aria-hidden', 'true');
        renderCountryFlag(flag, entry.country);

        const copy = document.createElement('span');
        copy.className = 'country-picker-option__copy';
        const label = document.createElement('strong');
        label.textContent = entry.label;
        const count = document.createElement('small');
        const programmeKey = entry.count === 1 ? 'country_picker_programme' : 'country_picker_programmes';
        count.textContent = `${entry.count} ${window.t ? window.t(programmeKey) : (entry.count === 1 ? 'programme' : 'programmes')}`;
        copy.append(label, count);

        const check = document.createElement('span');
        check.className = 'country-picker-option__check';
        check.setAttribute('aria-hidden', 'true');
        check.textContent = '✓';

        button.append(flag, copy, check);
        button.addEventListener('click', () => toggleCountrySelection(entry.country));
        button.addEventListener('keydown', handleCountryOptionKeydown);
        els.countryPicker.options.appendChild(button);
    });

    els.countryPicker.empty.hidden = visibleEntries.length > 0;
    if (countryPickerOpen) positionCountryPickerPopover();
}

function toggleCountrySelection(country, forceSelected = false) {
    if (!country) return;
    if (forceSelected || !selectedCountries.has(country)) selectedCountries.add(country);
    else selectedCountries.delete(country);

    els.countryFilter.value = '';
    renderCountryPickerOptions(els.countryPicker.search?.value || '');
    updateCountryPickerTrigger();
    renderCountryTags();
    processAndRender();
}

function renderCountryTags() {
    els.countryTags.innerHTML = '';
    selectedCountries.forEach(country => {
        const button = document.createElement('button');
        const label = window.getCountryName ? window.getCountryName(country) : country;
        button.type = 'button';
        button.className = 'tag-removable';

        const flag = document.createElement('span');
        flag.className = 'tag-removable__flag';
        flag.setAttribute('aria-hidden', 'true');
        renderCountryFlag(flag, country);
        const text = document.createElement('span');
        text.textContent = label;
        const remove = document.createElement('span');
        remove.className = 'tag-removable__remove';
        remove.setAttribute('aria-hidden', 'true');
        remove.textContent = '×';
        button.append(flag, text, remove);

        button.setAttribute('aria-label', `${label} ${window.currentLanguage === 'tr' ? 'filtresini kaldır' : 'remove filter'}`);
        button.addEventListener('click', () => {
            selectedCountries.delete(country);
            renderCountryPickerOptions(els.countryPicker.search?.value || '');
            updateCountryPickerTrigger();
            renderCountryTags();
            processAndRender();
        });
        els.countryTags.appendChild(button);
    });
}

function initCountryPicker() {
    const { trigger, popover, search, clear } = els.countryPicker;
    if (!trigger || !popover || !search || !clear) return;

    trigger.addEventListener('click', () => {
        if (countryPickerOpen) closeCountryPicker();
        else openCountryPicker();
    });
    trigger.addEventListener('keydown', event => {
        if (event.key !== 'ArrowDown') return;
        event.preventDefault();
        openCountryPicker();
    });
    search.addEventListener('input', event => renderCountryPickerOptions(event.target.value));
    search.addEventListener('keydown', event => {
        if (event.key === 'ArrowDown') {
            event.preventDefault();
            els.countryPicker.options.querySelector('.country-picker-option')?.focus();
        }
    });
    clear.addEventListener('click', () => {
        if (!selectedCountries.size) return;
        selectedCountries.clear();
        renderCountryPickerOptions(search.value);
        updateCountryPickerTrigger();
        renderCountryTags();
        processAndRender();
    });
    document.addEventListener('pointerdown', event => {
        if (!countryPickerOpen) return;
        if (popover.contains(event.target) || trigger.contains(event.target)) return;
        closeCountryPicker();
    });
    window.addEventListener('resize', () => {
        if (countryPickerOpen) positionCountryPickerPopover();
    });
    document.addEventListener('scroll', () => {
        if (countryPickerOpen) positionCountryPickerPopover();
    }, true);
}

function openCountryPicker() {
    if (!els.countryPicker.popover || !els.countryPicker.trigger) return;
    countryPickerOpen = true;
    els.countryPicker.popover.hidden = false;
    els.countryPicker.popover.classList.add('is-open');
    els.countryPicker.trigger.classList.add('is-open');
    els.countryPicker.trigger.setAttribute('aria-expanded', 'true');
    renderCountryPickerOptions(els.countryPicker.search.value);
    positionCountryPickerPopover();
    requestAnimationFrame(() => els.countryPicker.search.focus());
}

function closeCountryPicker(returnFocus = false) {
    if (!els.countryPicker.popover || !els.countryPicker.trigger) return;
    countryPickerOpen = false;
    els.countryPicker.popover.hidden = true;
    els.countryPicker.popover.classList.remove('is-open');
    els.countryPicker.trigger.classList.remove('is-open');
    els.countryPicker.trigger.setAttribute('aria-expanded', 'false');
    if (returnFocus) els.countryPicker.trigger.focus();
}

function positionCountryPickerPopover() {
    const { trigger, popover } = els.countryPicker;
    if (!countryPickerOpen || !trigger || !popover) return;

    const margin = 12;
    const gap = 8;
    const rect = trigger.getBoundingClientRect();
    // Match the control rail instead of forcing a 320px panel that protrudes
    // beyond the sidebar. Keep only a small usability floor on narrow screens.
    const width = Math.min(Math.max(rect.width, Math.min(260, window.innerWidth - (margin * 2))), window.innerWidth - (margin * 2));
    const left = Math.min(Math.max(rect.left, margin), window.innerWidth - width - margin);
    popover.style.width = `${width}px`;
    popover.style.left = `${left}px`;

    const popoverHeight = popover.offsetHeight;
    const roomBelow = window.innerHeight - rect.bottom - gap - margin;
    const roomAbove = rect.top - gap - margin;
    const top = roomBelow < Math.min(popoverHeight, 320) && roomAbove > roomBelow
        ? Math.max(margin, rect.top - popoverHeight - gap)
        : Math.min(rect.bottom + gap, window.innerHeight - popoverHeight - margin);
    popover.style.top = `${Math.max(margin, top)}px`;
}

function handleCountryOptionKeydown(event) {
    const options = Array.from(els.countryPicker.options.querySelectorAll('.country-picker-option'));
    const index = options.indexOf(event.currentTarget);
    if (event.key === 'ArrowDown') {
        event.preventDefault();
        options[(index + 1) % options.length]?.focus();
    } else if (event.key === 'ArrowUp') {
        event.preventDefault();
        options[(index - 1 + options.length) % options.length]?.focus();
    } else if (event.key === 'Home') {
        event.preventDefault();
        options[0]?.focus();
    } else if (event.key === 'End') {
        event.preventDefault();
        options.at(-1)?.focus();
    }
}

// Normalize function for search
window.normalizeSearchText = function(value) {
  return String(value || "")
    .toLowerCase()
    .trim()
    .replaceAll("ı", "i")
    .replaceAll("ğ", "g")
    .replaceAll("ü", "u")
    .replaceAll("ş", "s")
    .replaceAll("ö", "o")
    .replaceAll("ç", "c");
};

// Popular categories
const POPULAR_CATEGORIES = [
    "space_systems", "gnc", "cfd", "jet_propulsion", "aerospace_structures",
    "scientific_ai", "surrogate_modeling", "digital_twin", "satellite_systems", "astrodynamics"
];
let categorySearchBound = false;

window.renderCategoryUI = async function() {
    if (!els.categorySearchInput) return;
    if (!categorySearchBound) {
      els.categorySearchInput.addEventListener('input', async (e) => {
        const val = e.target.value;
        if (!val) {
            els.categorySuggestions.innerHTML = '';
            return;
        }
        const taxonomy = await window.loadTaxonomy();
        const normVal = window.normalizeSearchText(val);
        const results = [];
        for (const [key, info] of Object.entries(taxonomy)) {
            let match = false;
            
            // Safe label check
            const lblEn = typeof info.label === 'object' ? info.label.en : info.label;
            const lblTr = typeof info.label === 'object' ? info.label.tr : info.label;
            
            if (window.normalizeSearchText(lblEn).includes(normVal) || window.normalizeSearchText(lblTr).includes(normVal)) match = true;
            for (const alias of info.aliases || []) {
                if (window.normalizeSearchText(alias).includes(normVal)) { match = true; break; }
            }
            if (match) {
                results.push({ key, ...info });
            }
        }

        els.categorySuggestions.innerHTML = '';
        if (results.length === 0) {
            els.categorySuggestions.innerHTML = `<div class="category-suggestion" style="cursor:default; opacity:0.6"><span class="category-suggestion-title">${window.t('no_category_results')}</span></div>`;
            return;
        }
        results.slice(0, 8).forEach(res => {
            const button = document.createElement('button');
            button.type = 'button';
            button.className = 'category-suggestion';
            button.innerHTML = `<span class="category-suggestion-title">${escapeHtml(window.localizedValue(res.label))}</span>
                                <span class="category-suggestion-parent">${escapeHtml(window.localizedValue(res.parent))}</span>`;
            button.onclick = () => {
                selectedCategoryKeys.add(res.key);
                els.categorySearchInput.value = '';
                els.categorySuggestions.innerHTML = '';
                renderSelectedCategories();
                renderPopularCategories();
                processAndRender();
            };
            els.categorySuggestions.appendChild(button);
        });
      });
      categorySearchBound = true;
    }
    renderSelectedCategories();
    renderPopularCategories();
};

async function renderSelectedCategories() {
    if (!els.selectedCategoryChips) return;
    els.selectedCategoryChips.innerHTML = '';
    const taxonomy = await window.loadTaxonomy();
    selectedCategoryKeys.forEach(key => {
        const info = taxonomy[key];
        if (!info) return;
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'selected-category-chip';
        btn.innerHTML = `<span>${escapeHtml(window.localizedValue(info.label))}</span><span aria-hidden="true">×</span>`;
        btn.onclick = () => {
            selectedCategoryKeys.delete(key);
            renderSelectedCategories();
            renderPopularCategories();
            processAndRender();
        };
        els.selectedCategoryChips.appendChild(btn);
    });
}

async function renderPopularCategories() {
    if (!els.popularCategoryChips) return;
    els.popularCategoryChips.innerHTML = '';
    const taxonomy = await window.loadTaxonomy();
    POPULAR_CATEGORIES.forEach(key => {
        const info = taxonomy[key];
        if (!info) return;
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'popular-category-chip';
        btn.innerHTML = `<span>${escapeHtml(window.localizedValue(info.label))}</span>`;
        btn.disabled = selectedCategoryKeys.has(key);
        btn.onclick = () => {
            selectedCategoryKeys.add(key);
            renderSelectedCategories();
            renderPopularCategories();
            processAndRender();
        };
        els.popularCategoryChips.appendChild(btn);
    });
}
// Data Processing & Scoring
const COST_MAP = {
    'very_low': 1, 'low': 2, 'medium': 3, 'high': 4, 'very_high': 5
};

function processAndRender() {
    const search = window.normalizeSearchText(els.searchInput.value);
    
    const showFavs = els.favFilter.checked;

    const weights = {
        academic_fit: parseFloat(els.weights.academic ? els.weights.academic.value : 30),
        eligibility_language: parseFloat(els.weights.eligibility ? els.weights.eligibility.value : 20),
        cost_funding: parseFloat(els.weights.cost ? els.weights.cost.value : 20),
        career_research: parseFloat(els.weights.career ? els.weights.career.value : 15),
        living_risk: parseFloat(els.weights.living ? els.weights.living.value : 10),
        confidence_deadline: parseFloat(els.weights.confidence ? els.weights.confidence.value : 5)
    };

    const preferences = {
        selectedCategoryKeys: Array.from(selectedCategoryKeys),
        degreeFilter: els.hardFilters.degree ? els.hardFilters.degree.value : 'All',
        onlyEnglish: els.hardFilters.englishOnly ? els.hardFilters.englishOnly.checked : false,
        maxTuition: (els.hardFilters.maxTuition && parseFloat(els.hardFilters.maxTuition.value) < 25000) ? parseFloat(els.hardFilters.maxTuition.value) : 0,
        minFieldFit: 0 // Could add UI for this later
    };

    let filtered = rawData.filter(r => {
        const n = window.uniDataAdapter ? window.uniDataAdapter.normalizeUniversityRecord(r) : null;
        const rid = n?.id || r.Uni_ID || r.id || r.name || r.university;
        if (showFavs && !favorites.has(rid)) return false;
        if (selectedCountries.size > 0 && !selectedCountries.has(n?.country || r.country)) return false;
        
        if (search) {
            const text = [
                n?.universityName,
                n?.universityAliases?.join(' '),
                n?.programName,
                n?.city,
                n?.country,
                n?.degree,
                n?.researchSummary,
                n?.industrySummary,
                n?.strongAreas?.join(' '),
                r.tags_raw,
                r.focus
            ].filter(Boolean).join(' ');
            if (!window.normalizeSearchText(text).includes(search)) return false;
        }

        // Apply new scoring model and hard filters
        const scoringResult = window.unirankScoring.calculateScore(r, preferences, weights);
        if (!scoringResult.passed_hard_filters) {
            return false; // Skip if hard filters fail
        }

        // Inject scoring result into the record
        r._score = scoringResult.total_score / 10.0; // scale 0-10 for UI compatibility
        r._scoringDetails = scoringResult;
        
        r._costNum = getAnnualCost(r);
        
        return true;
    });

    const sortVal = els.sortSelect.value;
    filtered.sort((a, b) => {
        if (sortVal === 'score_desc') return b._score - a._score;
        if (sortVal === 'tuition_asc' || sortVal === 'cost_asc') {
            if (a._costNum === null) return b._costNum === null ? 0 : 1;
            if (b._costNum === null) return -1;
            return a._costNum - b._costNum;
        }
        if (sortVal === 'name_asc') {
            const nameA = window.uniDataAdapter?.normalizeUniversityRecord(a)?.universityName || a.display_name || a.name || '';
            const nameB = window.uniDataAdapter?.normalizeUniversityRecord(b)?.universityName || b.display_name || b.name || '';
            return String(nameA).localeCompare(String(nameB));
        }
        return 0;
    });

    filteredData = filtered;
    // Keep the filtered collection public for map popups and other view layers.
    // The map used to read window.filteredData while this variable stayed local,
    // so clicking a map result could never open its detail drawer.
    window.filteredData = filteredData;
    renderKPIs();
    renderTable();
    renderActiveFilters();
    window.dispatchEvent(new CustomEvent('unirank:dataUpdated', { detail: { filteredData } }));
}

function renderActiveFilters() {
    const bar = document.getElementById('active-filter-bar');
    const container = document.getElementById('active-filter-chips');
    const mobileCount = document.getElementById('mobile-filter-count');
    if (!bar || !container) return;

    const filters = [];
    selectedCountries.forEach(country => {
        filters.push({
            label: window.getCountryName ? window.getCountryName(country) : country,
            remove: () => {
                selectedCountries.delete(country);
                populateCountryFilter();
                renderCountryTags();
            }
        });
    });
    selectedCategoryKeys.forEach(key => {
        filters.push({
            label: window.getCategoryLabel ? window.getCategoryLabel(key) : key,
            remove: () => {
                selectedCategoryKeys.delete(key);
                renderSelectedCategories();
                renderPopularCategories();
            }
        });
    });

    const degree = els.hardFilters.degree?.value;
    if (degree && degree !== 'All') filters.push({ label: degree, remove: () => { els.hardFilters.degree.value = 'All'; } });
    if (els.hardFilters.englishOnly?.checked) {
        filters.push({ label: window.t ? window.t('only_english') : 'English study option', remove: () => { els.hardFilters.englishOnly.checked = false; } });
    }
    const maxTuition = Number(els.hardFilters.maxTuition?.value || 25000);
    if (maxTuition < 25000) {
        filters.push({
            label: `≤ €${maxTuition.toLocaleString('en-US')}`,
            remove: () => {
                els.hardFilters.maxTuition.value = '25000';
                const output = document.getElementById('tuition-val-display');
                if (output) output.textContent = 'Any';
            }
        });
    }
    if (els.favFilter?.checked) filters.push({ label: window.t ? window.t('show_favorites') : 'Favorites', remove: () => { els.favFilter.checked = false; } });
    if (els.searchInput?.value.trim()) filters.push({ label: `“${els.searchInput.value.trim()}”`, remove: () => { els.searchInput.value = ''; } });

    container.innerHTML = '';
    filters.forEach(filter => {
        const button = document.createElement('button');
        button.type = 'button';
        button.className = 'active-filter-chip';
        button.innerHTML = `<span>${escapeHtml(filter.label)}</span><span aria-hidden="true">×</span>`;
        button.addEventListener('click', () => {
            filter.remove();
            processAndRender();
        });
        container.appendChild(button);
    });

    bar.hidden = filters.length === 0;
    if (mobileCount) mobileCount.textContent = String(filters.length);
}

window.switchView = function(view) {
    const listBtn = document.getElementById('btn-view-list');
    const mapBtn = document.getElementById('btn-view-map');
    const listContainer = document.getElementById('list-view-container');
    const mapContainer = document.getElementById('map-view-container');
    const showMap = view === 'map';
    window.currentView = showMap ? 'map' : 'list';

    listBtn.classList.toggle('active', !showMap);
    mapBtn.classList.toggle('active', showMap);
    listBtn.setAttribute('aria-pressed', String(!showMap));
    mapBtn.setAttribute('aria-pressed', String(showMap));
    listContainer.hidden = showMap;
    mapContainer.hidden = !showMap;
    document.body.dataset.view = showMap ? 'map' : 'list';

    if (showMap) {
        setTimeout(() => {
            if (window.unirankMap) window.unirankMap.invalidateSize();
            window.dispatchEvent(new CustomEvent('unirank:viewChanged', { detail: { view: 'map' } }));
        }, 80);
    } else {
        window.dispatchEvent(new CustomEvent('unirank:viewChanged', { detail: { view: 'list' } }));
    }
}

function renderKPIs() {
    els.kpi.total.textContent = filteredData.length;
    const countriesSet = new Set();
    let officialSourceCount = 0;
    let mappedCount = 0;
    let totalScore = 0;

    filteredData.forEach(record => {
        const normalized = window.uniDataAdapter ? window.uniDataAdapter.normalizeUniversityRecord(record) : null;
        const country = normalized?.country || record.country;
        if (country) countriesSet.add(country);
        const hasOfficialSource = (normalized?.sources || []).some(source => (
            String(source?.source_type || '').toLowerCase().startsWith('official_') &&
            ['ok', 'redirects', 'pdf', 'requires_js'].includes(String(source?.access_status || '').toLowerCase())
        ));
        if (hasOfficialSource) officialSourceCount += 1;
        if (Number.isFinite(normalized?.location?.latitude) && Number.isFinite(normalized?.location?.longitude)) mappedCount += 1;
        totalScore += Number(record._score) || 0;
    });

    if (els.kpi.sourceCoverage) {
        els.kpi.sourceCoverage.textContent = filteredData.length
            ? `${Math.round((officialSourceCount / filteredData.length) * 100)}%`
            : '0%';
    }
    if (els.kpi.mapCoverage) {
        els.kpi.mapCoverage.textContent = filteredData.length
            ? `${Math.round((mappedCount / filteredData.length) * 100)}%`
            : '0%';
    }
    els.kpi.score.textContent = filteredData.length
        ? (totalScore / filteredData.length).toFixed(2)
        : '0.0';

    const kpiCountries = document.getElementById('kpi-countries');
    if (kpiCountries) kpiCountries.textContent = countriesSet.size;
}


function renderTable() {
    els.tableBody.innerHTML = '';
    if (filteredData.length === 0) {
        const title = window.t ? window.t('no_results_title') : 'No matching programs';
        const description = window.t ? window.t('no_results_desc') : 'Try removing one or two filters.';
        const resetLabel = window.t ? window.t('reset_filters') : 'Reset filters';
        els.tableBody.innerHTML = `
            <div class="empty-results-card" role="listitem">
                <span class="empty-results-card__icon" aria-hidden="true">⌁</span>
                <h3>${escapeHtml(title)}</h3>
                <p>${escapeHtml(description)}</p>
                <button class="btn btn-primary" type="button" data-reset-results>${escapeHtml(resetLabel)}</button>
            </div>`;
        els.tableBody.querySelector('[data-reset-results]')?.addEventListener('click', clearAllFilters);
        return;
    }

    filteredData.forEach((row, i) => {
        const n = window.uniDataAdapter ? window.uniDataAdapter.normalizeUniversityRecord(row) : null;
        if (!n) return;
        const rid = n ? n.id : (row.Uni_ID || row.id || row.name || row.university);
        const isFav = favorites.has(rid);
        const cleanCountry = n.country ? n.country.replace(/^[^a-zA-ZçğıöşüÇĞİÖŞÜ]+/, '').trim() : '—';
        const displayCountry = window.getCountryName ? window.getCountryName(cleanCountry) : cleanCountry;
        const band = scoreBand(row._score);
        const confidence = confidenceLabel(n.confidenceSummary);
        const language = formatTeachingLanguages(n.teachingLanguage) || (window.t ? window.t('unknown_value') : 'Unknown');
        const annualCost = n.totalAcademicCost !== null || n.tuitionPerYear !== null
            ? formatMoney(n.totalAcademicCost ?? n.tuitionPerYear)
            : formatPublishedTuition(n.foreignTuition);
        const city = displayValue(n.city);
        const degree = displayValue(n.degree);
        const admissionHTML = n.eligibleForNonEu === true
            ? escapeHtml(window.currentLanguage === 'tr' ? 'AB dışı uygun' : 'Non-EU eligible')
            : n.eligibleForNonEu === false
                ? escapeHtml(window.currentLanguage === 'tr' ? 'AB dışı uygun değil' : 'Not Non-EU eligible')
                : formatRiskBadge(n.admissionRisk);
        const housingHTML = formatRiskBadge(n.housingDifficulty);
        const deadline = n.deadline ? formatCalendarValue(n.deadline) : '';
        const profileMatch = row._scoringDetails?.personalized_match?.personal_field_fit;
        const university = window.localizedField(n.universityName) || (window.currentLanguage === 'tr' ? 'Üniversite adı doğrulanmalı' : 'University name needs verification');
        const program = window.localizedField(n.programName) || (window.currentLanguage === 'tr' ? 'Program adı doğrulanmalı' : 'Program name needs verification');

        const article = document.createElement('article');
        article.className = 'program-card country-card staggered-item';
        article.setAttribute('role', 'listitem');
        article.dataset.programId = rid;
        article.style.animationDelay = `${Math.min(i * 0.05, 1.0)}s`;
        article.innerHTML = `
            <div class="country-card__flag" aria-hidden="true"></div>
            <div class="program-card__rank" aria-label="Rank ${i + 1}"><span>${String(i + 1).padStart(2, '0')}</span></div>
            <div class="program-card__content">
                <div class="program-card__eyebrow">
                    <span>${escapeHtml([city, displayCountry].filter(value => value && value !== '—').join(' · ') || '—')}</span>
                    <span class="confidence-badge confidence-badge--${confidence.key}">${escapeHtml(confidence.label)}</span>
                </div>
                <h3>${escapeHtml(university)}</h3>
                <p class="program-card__program">${escapeHtml(program)}</p>
                <div class="program-card__meta">
                    <span>${escapeHtml(degree)}</span>
                    ${n.ects ? `<span>${escapeHtml(n.ects)} ECTS</span>` : ''}
                    ${n.duration ? `<span>${escapeHtml(n.duration)}</span>` : ''}
                    ${deadline ? `<span class="program-card__meta-date">${escapeHtml(window.currentLanguage === 'tr' ? 'Son başvuru' : 'Deadline')} · ${escapeHtml(deadline)}</span>` : ''}
                </div>
                <dl class="decision-grid">
                    <div class="decision-item decision-item--score"><dt>${escapeHtml(window.t ? window.t('technical_match') : 'Technical match')}</dt><dd><span class="fit-score fit-score--${band.key}">${Number(row._score).toFixed(1)}</span><small>${escapeHtml(band.label)}</small>${window.personalizationEnabled && Number.isFinite(profileMatch) ? `<em>${Math.round(profileMatch)}% ${escapeHtml(window.t('profile_match'))}</em>` : ''}</dd></div>
                    <div class="decision-item"><dt>${escapeHtml(window.t ? window.t('teaching_language') : 'Teaching language')}</dt><dd>${escapeHtml(language)}</dd></div>
                    <div class="decision-item"><dt>${escapeHtml(window.t ? window.t('annual_cost') : 'Annual cost')}</dt><dd>${escapeHtml(annualCost)}</dd></div>
                    <div class="decision-item"><dt>${escapeHtml(window.t ? window.t('admission_reality') : 'Admission reality')}</dt><dd>${admissionHTML}</dd></div>
                    <div class="decision-item"><dt>${escapeHtml(window.t ? window.t('housing_risk') : 'Housing risk')}</dt><dd>${housingHTML}</dd></div>
                </dl>
            </div>
            <div class="program-card__actions">
                <button class="favorite-button${isFav ? ' is-active' : ''}" type="button" aria-pressed="${String(isFav)}" aria-label="${escapeHtml(window.t ? window.t(isFav ? 'remove_favorite' : 'add_favorite') : 'Favorite')}">${isFav ? '★' : '☆'}</button>
                <button class="detail-btn" type="button">${escapeHtml(window.t ? window.t('view_program') : 'View program')} <span aria-hidden="true">→</span></button>
            </div>`;

        applyCountryVisual(article, cleanCountry);

        article.querySelector('.favorite-button').addEventListener('click', () => {
            toggleFavorite(rid);
        });
        article.querySelector('.detail-btn').addEventListener('click', () => openDrawer(row));
        els.tableBody.appendChild(article);
    });
}



function openDrawer(data) {
    try {
        activeDrawerData = data;
        window.lastDrawerTrigger = document.activeElement;
        const n = window.uniDataAdapter ? window.uniDataAdapter.normalizeUniversityRecord(data) : null;
        if (!n) return;
        applyCountryVisual(els.drawer.panel, n.country);
        n.programUrl = safeUrl(n.programUrl);
        n.admissionUrl = safeUrl(n.admissionUrl);
        n.tuitionUrl = safeUrl(n.tuitionUrl);
        n.scholarshipUrl = safeUrl(n.scholarshipUrl);

        const t = window.t || (k => k);
        els.drawer.title.textContent = window.localizedField(n.universityName) || 'Details';
        
        const rid = n.id;
        const isFav = favorites.has(rid);
        els.drawer.favBtn.innerHTML = isFav ? '★' : '☆';
        els.drawer.favBtn.setAttribute('aria-pressed', String(isFav));
        els.drawer.favBtn.setAttribute('aria-label', window.t ? window.t(isFav ? 'remove_favorite' : 'add_favorite') : 'Favorite');
        els.drawer.favBtn.onclick = () => {
            toggleFavorite(rid);
            const nowFavorite = favorites.has(rid);
            els.drawer.favBtn.innerHTML = nowFavorite ? '★' : '☆';
            els.drawer.favBtn.setAttribute('aria-pressed', String(nowFavorite));
            els.drawer.favBtn.setAttribute('aria-label', window.t ? window.t(nowFavorite ? 'remove_favorite' : 'add_favorite') : 'Favorite');
        };

        const scoreVal = data._score ? data._score.toFixed(2) : '0.00';
        const isTurkish = window.currentLanguage === 'tr';
        const band = scoreBand(data._score);
        const confidence = confidenceLabel(n.confidenceSummary);
        const languageText = formatTeachingLanguages(n.teachingLanguage) || (window.t ? window.t('unknown_value') : 'Unknown');
        const publishedProgrammeFee = n.costDetails?.tuition_non_eu_full_program;
        const headlineCost = n.totalAcademicCost != null || n.tuitionPerYear != null
            ? formatMoney(n.totalAcademicCost ?? n.tuitionPerYear)
            : n.foreignTuition
                ? `${formatPublishedTuition(n.foreignTuition)}${publishedTuitionPeriodSuffix(n.foreignTuition, isTurkish)}`
            : publishedProgrammeFee?.amount != null && publishedProgrammeFee?.currency
                ? `${Number(publishedProgrammeFee.amount).toLocaleString('en-US')} ${publishedProgrammeFee.currency} (${isTurkish ? 'program toplamı' : 'full programme'})`
                : '—';
        const decisionHeroHTML = `
            <section class="drawer-decision-hero">
                <div class="drawer-decision-hero__topline">
                    <span>${escapeHtml([displayValue(n.city), window.getCountryName ? window.getCountryName(n.country) : n.country].filter(Boolean).join(' · '))}</span>
                    <span class="confidence-badge confidence-badge--${confidence.key}">${escapeHtml(confidence.label)}</span>
                </div>
                <h3>${escapeHtml(displayValue(n.programName))}</h3>
                <div class="drawer-score-line"><strong class="fit-score fit-score--${band.key}">${escapeHtml(scoreVal)}</strong><span><b>${escapeHtml(band.label)}</b><small>${escapeHtml(window.t ? window.t('technical_match') : 'Technical match')}</small></span></div>
                <dl class="drawer-decision-grid">
                    <div><dt>${escapeHtml(window.t ? window.t('teaching_language') : 'Teaching language')}</dt><dd>${escapeHtml(languageText)}</dd></div>
                    <div><dt>${escapeHtml(window.t ? window.t('annual_cost') : 'Annual cost')}</dt><dd>${escapeHtml(headlineCost)}${n.tuitionScope === 'non_eu_target' ? ` <small>(${isTurkish ? 'AB dışı hedef ücret' : 'non-EU target fee'})</small>` : ''}</dd></div>
                    <div><dt>ECTS / ${escapeHtml(window.t ? window.t('degree') : 'Degree')}</dt><dd>${escapeHtml([n.ects ? `${n.ects} ECTS` : '', displayValue(n.degree)].filter(Boolean).join(' · ') || '—')}</dd></div>
                    <div><dt>${escapeHtml(isTurkish ? 'Başvuru son tarihi' : 'Application deadline')}</dt><dd>${escapeHtml(n.deadline ? displayValue(n.deadline) : '—')}</dd></div>
                </dl>
                ${n.lastVerified ? `<p class="drawer-verified">${escapeHtml(window.t ? window.t('last_verified') : 'Last verified')}: ${escapeHtml(formatCalendarValue(n.lastVerified))}</p>` : ''}
            </section>`;
        const verificationBanner = n.needsVerification
            ? `<div class="verification-banner warning"><strong>${isTurkish ? 'Doğrulama gerekli' : 'Verification required'}</strong><span>${isTurkish ? 'Kritik kayıt alanları resmi kaynaklarla yeniden kontrol edilmelidir.' : 'Critical record fields should be rechecked against official sources.'}</span></div>`
            : `<div class="verification-banner"><strong>${isTurkish ? 'Kaynak durumu' : 'Source status'}</strong><span>${n.sources.length ? (isTurkish ? `${n.sources.length} kaynak kaydı mevcut.` : `${n.sources.length} source record(s) available.`) : (isTurkish ? 'Kaynak kaydı sınırlı.' : 'Source evidence is limited.')}</span></div>`;

        const quality = n.dataQuality || {};
        const verifiedFields = quality.verifiedFields || [];
        const unverifiedFields = quality.unverifiedCriticalFields || [];
        const qualityStatusLabel = {
            verified: isTurkish ? 'Kritik alanlar doğrulandı' : 'Critical fields verified',
            partial: isTurkish ? 'Kısmi doğrulama' : 'Partially verified',
            needs_verification: isTurkish ? 'Doğrulama bekliyor' : 'Verification pending'
        }[quality.status] || (isTurkish ? 'Doğrulama bekliyor' : 'Verification pending');
        const humanField = (field) => ({
            program: isTurkish ? 'program' : 'programme', language: isTurkish ? 'öğretim dili' : 'teaching language',
            admission: isTurkish ? 'kabul' : 'admission', non_eu_eligibility: isTurkish ? 'AB dışı uygunluk' : 'non-EU eligibility',
            tuition: isTurkish ? 'öğrenim ücreti' : 'tuition', scholarship: isTurkish ? 'burs' : 'scholarship',
            deadline: isTurkish ? 'son tarih' : 'deadline', curriculum: isTurkish ? 'müfredat' : 'curriculum',
            research: isTurkish ? 'araştırma' : 'research', industry: isTurkish ? 'endüstri ilişkisi' : 'industry links',
            housing: isTurkish ? 'konaklama' : 'housing'
        }[field] || field);
        const qualityHTML = `
            <section class="evidence-strip evidence-strip--${escapeHtml(quality.status || 'needs_verification')}">
                <div><span class="evidence-strip__eyebrow">${isTurkish ? 'VERİ KAPSAMI' : 'DATA COVERAGE'}</span><strong>${escapeHtml(qualityStatusLabel)}</strong></div>
                <div class="evidence-strip__counts"><b>${Number(quality.checkedOfficialSourceCount || 0)}</b><span>${isTurkish ? 'kontrol edilmiş resmi kaynak' : 'checked official sources'}</span></div>
                <p>${verifiedFields.length ? (isTurkish ? `Doğrulanan: ${verifiedFields.map(humanField).join(', ')}.` : `Verified: ${verifiedFields.map(humanField).join(', ')}.`) : (isTurkish ? 'Henüz karar verdiren alan doğrulanmadı.' : 'No decision-critical field is verified yet.')}</p>
                ${unverifiedFields.length ? `<small>${isTurkish ? 'Kontrol bekleyen: ' : 'Still to verify: '}${escapeHtml(unverifiedFields.map(humanField).join(', '))}</small>` : ''}
            </section>`;

        const weighted = data._scoringDetails?.weighted_components || {};
        const impactLabels = {
            academic_fit: isTurkish ? 'Akademik güç' : 'Academic strength',
            eligibility_language: isTurkish ? 'Uygunluk ve dil' : 'Eligibility & language',
            cost_funding: isTurkish ? 'Maliyet ve burs' : 'Cost & funding',
            career_research: isTurkish ? 'Kariyer / araştırma' : 'Career / research',
            living_risk: isTurkish ? 'Yaşam riski' : 'Living risk',
            confidence_deadline: isTurkish ? 'Veri güveni' : 'Data confidence'
        };
        const impactRows = Object.entries(weighted)
            .sort(([, left], [, right]) => Number(right) - Number(left))
            .map(([key, value]) => `<li><span>${escapeHtml(impactLabels[key] || key)}</span><b>${Number(value).toFixed(1)}</b></li>`)
            .join('');
        const scoreImpactHTML = impactRows ? `
            <section class="score-impact-card">
                <div><span class="evidence-strip__eyebrow">${isTurkish ? 'AĞIRLIK ETKİSİ' : 'WEIGHT IMPACT'}</span><strong>${isTurkish ? 'Bu puanı hangi ağırlıklar taşıyor?' : 'Which weights drive this score?'}</strong></div>
                <ol>${impactRows}</ol>
                <small>${isTurkish ? 'Katkılar, seçtiğiniz ağırlıklarla 100 üzerinden puana yapılan katkıdır; akademik katkı kaynaklı müfredat ve araştırma kanıtından hesaplanır.' : 'Contributions are points toward the 100-point result at your selected weights; academic contribution uses source-backed curriculum and research evidence.'}</small>
            </section>` : '';

        // 2. Basic info card. Every label follows the active language: mixed
        // Turkish labels inside the English UI read like leaked internals.
        const rawQsRank = String(n.qsRankDisplay || '').trim();
        const isTiedQsRank = rawQsRank.startsWith('=');
        const cleanQsRank = rawQsRank.replace(/^[#=\s]+/, '');
        const rawEngineeringRank = n.engineeringRanking ? displayValue(n.engineeringRanking) : '';
        const rankingItems = [
            cleanQsRank ? `<div><dt>QS World University Rankings${n.qsRankYear ? ` · ${escapeHtml(n.qsRankYear)}` : ''}</dt><dd>#${escapeHtml(cleanQsRank)}${isTiedQsRank ? `<small>${isTurkish ? 'eşit sıra' : 'tied'}</small>` : ''}</dd></div>` : '',
            rawEngineeringRank ? `<div><dt>${isTurkish ? 'Mühendislik sıralaması' : 'Engineering ranking'}</dt><dd>#${escapeHtml(String(rawEngineeringRank).replace(/^[#=\s]+/, ''))}</dd></div>` : ''
        ].filter(Boolean).join('');

        let basicInfoHTML = `
            <div class="drawer-section premium-card">
                <div class="premium-header">
                    <span class="premium-icon" aria-hidden="true"></span>
                    <h4 class="premium-title">${isTurkish ? 'Temel Bilgiler' : 'Overview'}</h4>
                </div>
                <div class="premium-grid">
                    <div class="premium-item full-span">
                        <label>${isTurkish ? 'Ülke / Şehir' : 'Country / City'}</label>
                        <span class="country-gradient" data-country="${escapeHtml(n.country)}">${escapeHtml(window.getCountryName ? window.getCountryName(n.country) : n.country)} - ${escapeHtml(displayValue(n.city))}</span>
                    </div>
                    <div class="premium-item full-span">
                        <label>${isTurkish ? 'Üniversite & Program' : 'University & Programme'}</label>
                        <span class="highlight-text">${escapeHtml(displayValue(n.universityName))} - ${escapeHtml(displayValue(n.programName))}</span>
                    </div>
                    <div class="premium-item">
                        <label>${isTurkish ? 'Derece' : 'Degree'}</label>
                        <span>${escapeHtml(displayValue(n.degree))}</span>
                    </div>
                    <div class="premium-item">
                        <label>${isTurkish ? 'Öğretim Dili' : 'Teaching Language'}</label>
                        <span>${escapeHtml(formatTeachingLanguages(n.teachingLanguage))}</span>
                    </div>
                    ${rankingItems ? `
                    <div class="premium-item full-span ranking-container">
                        <label>${isTurkish ? 'Sıralamalar' : 'Rankings'}</label>
                        <dl class="ranking-list">${rankingItems}</dl>
                    </div>` : ''}
                </div>
            </div>
        `;

        // 3. Bölüm / Araştırma Bilgileri (Department Info)
        // Practical admissions are shown before prestige/research information.
        const admission = n.eligibilityDetails || {};
        const languageDetails = n.languageDetails || {};
        const yesNoUnknown = (value) => value === true
            ? (isTurkish ? 'Evet' : 'Yes')
            : value === false ? (isTurkish ? 'Hayır' : 'No') : (isTurkish ? 'Bilinmiyor' : 'Unknown');
        const admissionList = (values) => (Array.isArray(values) ? values : [])
            .map((value) => `<li>${escapeHtml(displayValue(value))}</li>`).join('');
        const backgroundsHTML = admissionList(admission.accepted_backgrounds);
        const documentsHTML = admissionList(admission.required_documents);
        const grePolicyLabel = {
            required: isTurkish ? 'Zorunlu' : 'Required',
            required_with_waivers: isTurkish ? 'Zorunlu; sınırlı muafiyetler var' : 'Required; limited waivers available',
            optional: isTurkish ? 'İsteğe bağlı' : 'Optional',
            optional_not_required: isTurkish ? 'İsteğe bağlı · zorunlu değil' : 'Optional · not required',
            optional_waived: isTurkish ? 'Şart kaldırıldı; gönderilirse değerlendirilir' : 'Waived; evaluated if submitted',
            not_required: isTurkish ? 'Gerekli değil' : 'Not required',
            not_required_and_not_considered: isTurkish ? 'Gerekli değil · değerlendirmeye alınmıyor' : 'Not required · not considered',
            not_accepted: isTurkish ? 'Kabul edilmiyor · değerlendirmeye alınmıyor' : 'Not accepted · not considered',
            not_required_but_encouraged: isTurkish ? 'Zorunlu değil; rekabetçi başvuru için teşvik ediliyor' : 'Not required; encouraged for a more competitive application',
            not_listed_as_required: isTurkish ? 'Resmî şartlarda listelenmiyor' : 'Not listed in the official requirements',
            unknown: isTurkish ? 'Bilinmiyor' : 'Unknown'
        }[String(admission.gre?.policy || 'unknown')] || displayValue(admission.gre?.policy);
        const interviewText = admission.interview_policy === 'optional_at_academic_committee_discretion'
            ? (isTurkish ? 'Komisyonun takdirinde isteğe bağlı' : 'Optional at the committee’s discretion')
            : admission.interview_policy === 'may_be_invited_not_required_for_all'
                ? (isTurkish ? 'Bazı adaylar davet edilebilir; herkes için zorunlu değil' : 'Some applicants may be invited; not required for everyone')
                : yesNoUnknown(admission.interview_required);
        const testText = admission.test_policy ? displayValue(admission.test_policy) : yesNoUnknown(admission.test_required);
        const englishTests = Array.isArray(languageDetails.accepted_english_tests) ? languageDetails.accepted_english_tests : [];
        const englishTestText = englishTests.map((test) => {
            const testName = test.test || test.name || '';
            const minimum = test.minimum_score ?? test.minimum_overall;
            const oldScale = test.minimum_score_old_scale;
            const newScale = test.minimum_score_new_scale ?? test.minimum_score_2026_scale;
            const newSpeaking = test.minimum_speaking_new_scale;
            const newWriting = test.minimum_writing_new_scale;
            const datedSpeaking = test.minimum_speaking_from_2026_01_21;
            const datedWriting = test.minimum_writing_from_2026_01_21;
            const score = oldScale != null || newScale != null
                ? [
                    oldScale != null ? `${oldScale} (${isTurkish ? 'eski ölçek' : 'old scale'})` : '',
                    newScale != null
                        ? `${newScale} ${isTurkish ? 'toplam' : 'total'}${newSpeaking != null || newWriting != null ? `; S/W ${newSpeaking ?? '—'}/${newWriting ?? '—'}` : ''} (${isTurkish ? '21 Ocak 2026 sonrası' : 'from 21 Jan 2026'})`
                        : ''
                ].filter(Boolean).join(' / ')
                : minimum != null
                    ? `${minimum}${datedSpeaking != null || datedWriting != null ? `; S/W ${datedSpeaking ?? '—'}/${datedWriting ?? '—'} (${isTurkish ? '21 Ocak 2026 sonrası' : 'from 21 Jan 2026'})` : ''}`
                    : '';
            return [testName, score].filter(Boolean).join(' ');
        }).filter(Boolean).join(' · ');
        const applicationFeeUsd = admission.application_fee_usd ?? admission.application_fee_usd_international;
        const applicationFeeText = Number.isFinite(Number(applicationFeeUsd))
            ? formatPublishedMoney({ amount: Number(applicationFeeUsd), currency: 'USD' })
            : '';
        const languageRequirement = languageDetails.spanish_required
            ? `${isTurkish ? 'İspanyolca' : 'Spanish'} ${escapeHtml(languageDetails.spanish_level_required || '')}`.trim()
            : languageDetails.italian_required
                ? `${isTurkish ? 'İtalyanca' : 'Italian'} ${escapeHtml(languageDetails.italian_level_required || '')}`.trim()
                : languageDetails.german_required
                    ? `${isTurkish ? 'Almanca' : 'German'} ${escapeHtml(languageDetails.german_level_required || '')}`.trim()
                    : languageDetails.english_required
                        ? `${isTurkish ? 'İngilizce yeterlilik gerekli' : 'English proficiency required'}${languageDetails.english_level_required ? ` · ${escapeHtml(displayValue(languageDetails.english_level_required))}` : ''}`
                        : languageDetails.english_proficiency_required_conditionally
                            ? (isTurkish ? 'Muafiyet yoksa İngilizce yeterlilik kanıtı gerekli' : 'English-proficiency evidence required unless exempt')
                        : (isTurkish ? 'Ek program dili şartı yayımlanmamış' : 'No additional programme-language requirement published');
        const admissionsHTML = `
            <div class="drawer-section premium-card admission-card">
                <div class="premium-header"><span class="premium-icon" aria-hidden="true"></span><h4 class="premium-title">${isTurkish ? 'Kabul & Dil Gereklilikleri' : 'Admission & Language Requirements'}</h4></div>
                <div class="premium-grid">
                    <div class="premium-item"><label>${isTurkish ? 'AB dışı başvuru' : 'Non-EU application'}</label><span>${yesNoUnknown(n.eligibleForNonEu)}</span></div>
                    <div class="premium-item"><label>${isTurkish ? 'Program dili şartı' : 'Programme language requirement'}</label><span>${languageRequirement}</span></div>
                    <div class="premium-item"><label>GRE</label><span>${escapeHtml(grePolicyLabel)}</span></div>
                    <div class="premium-item"><label>${isTurkish ? 'Mülakat' : 'Interview'}</label><span>${escapeHtml(interviewText)}</span></div>
                    <div class="premium-item full-span"><label>${isTurkish ? 'Program sınavı' : 'Programme test'}</label><span>${escapeHtml(testText)}</span></div>
                    ${applicationFeeText ? `<div class="premium-item"><label>${isTurkish ? 'Başvuru ücreti' : 'Application fee'}</label><span>${escapeHtml(applicationFeeText)}</span></div>` : ''}
                    ${englishTestText ? `<div class="premium-item full-span source-note"><label>${isTurkish ? 'Kabul edilen İngilizce sınavları ve asgariler' : 'Accepted English tests and minimums'}</label><span>${escapeHtml(englishTestText)}</span></div>` : ''}
                    ${admission.cohort_size_max ? `<div class="premium-item"><label>${isTurkish ? 'Azami kontenjan' : 'Maximum cohort'}</label><span>${escapeHtml(admission.cohort_size_max)}</span></div>` : ''}
                    ${admission.video_requirement ? `<div class="premium-item"><label>Video</label><span>${admission.video_requirement === 'only_if_requested_in_the_call' ? (isTurkish ? 'Yalnızca çağrıda istenirse' : 'Only if requested in the call') : escapeHtml(displayValue(admission.video_requirement))}</span></div>` : ''}
                    ${admission.ranking_or_selection ? `<div class="premium-item full-span source-note"><label>${isTurkish ? 'Seçim ölçütleri' : 'Selection criteria'}</label><span>${escapeHtml(displayValue(admission.ranking_or_selection))}</span></div>` : ''}
                    ${admission.notes_for_turkish_students ? `<div class="premium-item full-span source-note"><label>${isTurkish ? 'Türkiye’den başvuran için' : 'For an applicant from Turkey'}</label><span>${escapeHtml(displayValue(admission.notes_for_turkish_students))}</span></div>` : ''}
                </div>
                ${backgroundsHTML ? `<details class="detail-disclosure"><summary>${isTurkish ? 'Kabul edilen akademik geçmişler' : 'Accepted academic backgrounds'}</summary><ul>${backgroundsHTML}</ul></details>` : ''}
                ${documentsHTML ? `<details class="detail-disclosure"><summary>${isTurkish ? `Gerekli belgeler (${admission.required_documents.length})` : `Required documents (${admission.required_documents.length})`}</summary><ul>${documentsHTML}</ul></details>` : ''}
            </div>`;

        const curriculum = n.curriculumDetails || {};
        const mandatoryCourses = Array.isArray(curriculum.mandatory_courses)
            ? curriculum.mandatory_courses
            : (Array.isArray(curriculum.core_courses) ? curriculum.core_courses : []);
        const requirementComponents = Array.isArray(curriculum.requirement_components) ? curriculum.requirement_components : [];
        const curriculumTracks = Array.isArray(curriculum.tracks)
            ? curriculum.tracks
            : (Array.isArray(curriculum.specializations) ? curriculum.specializations : []);
        const publishedComponents = mandatoryCourses.length ? mandatoryCourses : requirementComponents;
        const courseRows = publishedComponents.map((item) => {
            const name = displayValue(typeof item === 'object' ? item.name : item);
            const ectsLabel = item && typeof item === 'object' && item.ects != null ? `${item.ects} ECTS` : '';
            const creditHoursLabel = item && typeof item === 'object' && item.credit_hours != null
                ? `${displayValue(item.credit_hours)} ${isTurkish ? 'kredi saati' : 'credit hours'}` : '';
            const semesterLabel = item && typeof item === 'object' && item.semester != null
                ? `${isTurkish ? 'Yarıyıl' : 'Semester'} ${item.semester}` : '';
            return `<li><span>${escapeHtml(name)}</span><small>${escapeHtml([ectsLabel, creditHoursLabel, semesterLabel].filter(Boolean).join(' · '))}</small></li>`;
        }).join('');
        const trackRows = curriculumTracks.map((track) =>
            `<li><span>${escapeHtml(displayValue(track))}</span></li>`
        ).join('');
        const totalComponentCount = curriculum.course_count_summary
            ? displayValue(curriculum.course_count_summary)
            : curriculum.course_count_total_including_thesis
                ?? ((curriculum.total_credit_hours ?? curriculum.credit_hours_total) != null
                    ? `${displayValue(curriculum.total_credit_hours ?? curriculum.credit_hours_total)} ${isTurkish ? 'kredi' : 'credits'}`
                    : (mandatoryCourses.length || null));
        const taughtComponentCount = curriculum.course_count_fixed === false
            ? (isTurkish ? 'Programa göre değişir' : 'Pathway-dependent')
            : curriculum.taught_project_and_seminar_component_count
                ?? (curriculum.typical_course_equivalent != null
                    ? `${isTurkish ? 'Yaklaşık' : 'About'} ${displayValue(curriculum.typical_course_equivalent)} ${isTurkish ? 'ders; yola göre değişir' : 'classes; pathway-dependent'}`
                    : curriculum.typical_three_unit_course_equivalent != null
                        ? `${displayValue(curriculum.typical_three_unit_course_equivalent)} ${isTurkish ? 'adet üç kredilik ders' : 'three-unit courses'}`
                    : (mandatoryCourses.length || '—'));
        const hasThesisAndNonThesisRoutes = curriculum.thesis_required === false
            && Array.isArray(curriculum.tracks)
            && curriculum.tracks.includes('thesis')
            && curriculum.tracks.includes('non_thesis');
        const thesisLabel = curriculum.thesis_requirement_summary
            ? displayValue(curriculum.thesis_requirement_summary)
            : (curriculum.thesis_route_available === true || curriculum.thesis_option_available_by_request === true || hasThesisAndNonThesisRoutes) && curriculum.thesis_required === false
                ? (curriculum.thesis_option_guaranteed === false
                    ? (isTurkish ? 'İsteğe bağlı talep edilebilir · garanti değil' : 'Optional by request · not guaranteed')
                    : (isTurkish ? 'İsteğe bağlı · tezli ve tezsiz yollar var' : 'Optional · thesis and non-thesis routes available'))
            : curriculum.thesis_required === true
                ? `${isTurkish ? 'Zorunlu' : 'Required'}${curriculum.thesis_ects ? ` · ${curriculum.thesis_ects} ECTS` : ''}`
                : yesNoUnknown(curriculum.thesis_required);
        const internshipRequired = curriculum.internship_required ?? curriculum.mandatory_internship;
        const internshipLabel = internshipRequired === true
            ? (isTurkish ? 'Zorunlu' : 'Required')
            : internshipRequired === false ? (isTurkish ? 'Zorunlu değil' : 'Not compulsory') : (isTurkish ? 'Bilinmiyor' : 'Unknown');
        const curriculumHTML = `
            <div class="drawer-section premium-card curriculum-card">
                <div class="premium-header"><span class="premium-icon" aria-hidden="true"></span><h4 class="premium-title">${isTurkish ? 'Müfredat & Ders Yükü' : 'Curriculum & Course Load'}</h4></div>
                <div class="premium-grid">
                    <div class="premium-item"><label>${curriculum.course_count_fixed === false ? (isTurkish ? 'Ders sayısı yapısı' : 'Course-count structure') : (isTurkish ? 'Toplam değerlendirilen bileşen' : 'Total assessed components')}</label><span>${escapeHtml(totalComponentCount ?? '—')}</span></div>
                    <div class="premium-item"><label>${isTurkish ? 'Ders / proje / seminer' : 'Courses / projects / seminar'}</label><span>${escapeHtml(taughtComponentCount)}</span></div>
                    <div class="premium-item"><label>${isTurkish ? 'Tez' : 'Thesis'}</label><span>${escapeHtml(thesisLabel)}</span></div>
                    <div class="premium-item"><label>${isTurkish ? 'Zorunlu staj' : 'Compulsory internship'}</label><span>${internshipLabel}</span></div>
                    ${curriculum.internship_notes ? `<div class="premium-item full-span source-note"><label>${isTurkish ? 'Staj / şirket çalışması notu' : 'Internship / company-work note'}</label><span>${escapeHtml(displayValue(curriculum.internship_notes))}</span></div>` : ''}
                    ${curriculum.track_selection_policy ? `<div class="premium-item full-span source-note"><label>${isTurkish ? 'Alan / alt plan seçimi' : 'Track / subplan selection'}</label><span>${escapeHtml(displayValue(curriculum.track_selection_policy))}</span></div>` : ''}
                    ${curriculum.verification_notes ? `<div class="premium-item full-span source-note"><label>${isTurkish ? 'Müfredat doğrulama notu' : 'Curriculum verification note'}</label><span>${escapeHtml(displayValue(curriculum.verification_notes))}</span></div>` : ''}
                </div>
                ${courseRows ? `<details class="detail-disclosure"><summary>${mandatoryCourses.length ? (isTurkish ? `Zorunlu ders/proje listesi (${mandatoryCourses.length})` : `Mandatory course/project list (${mandatoryCourses.length})`) : (isTurkish ? `Yayımlanmış şart yapısı (${requirementComponents.length})` : `Published requirement structure (${requirementComponents.length})`)}</summary><ul class="course-detail-list">${courseRows}</ul></details>` : ''}
                ${trackRows ? `<details class="detail-disclosure"><summary>${isTurkish ? `Yayımlanmış alanlar / alt planlar (${curriculumTracks.length})` : `Published tracks / subplans (${curriculumTracks.length})`}</summary><ul class="course-detail-list">${trackRows}</ul></details>` : ''}
            </div>`;

        const timeline = n.timelineDetails || {};
        const applicationRounds = Array.isArray(timeline.application_rounds) ? timeline.application_rounds : [];
        const nextCycleStatus = String(timeline.next_cycle_status || '').toLowerCase();
        const nextCyclePending = /not[_ -]published|awaiting[_ -]publication|needs[_ -]verification/.test(nextCycleStatus);
        const targetAcademicYear = displayValue(timeline.target_academic_year || timeline.academic_year);
        const targetCycleStatusText = nextCyclePending
            ? (isTurkish ? 'Kesin 2027/28 tarihi henüz resmî olarak yayımlanmadı' : 'The exact 2027/28 date has not yet been officially published')
            : (isTurkish ? 'Yayımlanmış dönem bilgisi' : 'Published cycle information');
        const roundRows = applicationRounds.map((round, index) => {
            if (typeof round === 'string') {
                return `<li><strong>${escapeHtml(nextCyclePending ? (isTurkish ? `Önceki dönem turu ${index + 1}` : `Previous-cycle round ${index + 1}`) : (isTurkish ? `Başvuru turu ${index + 1}` : `Application round ${index + 1}`))}</strong><span>${escapeHtml(formatCalendarValue(round))}</span></li>`;
            }
            const roundKey = round.round ?? round.intake;
            const roundName = roundKey === 'extraordinary_if_places_remain'
                ? (isTurkish ? 'Ek çağrı (yalnızca boş kontenjan varsa)' : 'Extraordinary call (only if places remain)')
                : displayValue(roundKey);
            const dates = [round.opens, round.deadline].filter(Boolean).map(formatCalendarValue).join(' → ');
            const result = round.decision ? `${isTurkish ? 'Sonuç' : 'Decision'}: ${formatCalendarValue(round.decision)}` : '';
            return `<li><strong>${escapeHtml(roundName)}</strong><span>${escapeHtml(dates)}</span><small>${escapeHtml(result)}</small></li>`;
        }).join('');
        const timelineHTML = `
            <div class="drawer-section premium-card timeline-card">
                <div class="premium-header"><span class="premium-icon" aria-hidden="true"></span><h4 class="premium-title">${isTurkish ? 'Başvuru Takvimi' : 'Application Timeline'}</h4></div>
                <div class="premium-grid">
                    ${timeline.target_academic_year ? `<div class="premium-item"><label>${isTurkish ? 'Hedef dönem' : 'Target cycle'}</label><span>${escapeHtml(targetAcademicYear)}</span></div>` : ''}
                    ${timeline.next_cycle_status ? `<div class="premium-item ${nextCyclePending ? 'timeline-cycle-pending' : ''}"><label>${isTurkish ? '2027 yayın durumu' : '2027 publication status'}</label><span>${escapeHtml(targetCycleStatusText)}</span></div>` : ''}
                    ${timeline.intake ? `<div class="premium-item"><label>${isTurkish ? 'Başlangıç dönemi' : 'Intake'}</label><span>${escapeHtml(displayValue(timeline.intake))}</span></div>` : ''}
                    ${!nextCyclePending && timeline.application_opens ? `<div class="premium-item"><label>${isTurkish ? 'Başvuru açılışı' : 'Application opens'}</label><span>${escapeHtml(formatCalendarValue(timeline.application_opens))}</span></div>` : ''}
                    ${!nextCyclePending && (timeline.non_eu_deadline || timeline.deadline_non_eu) ? `<div class="premium-item"><label>${isTurkish ? 'AB dışı olağan son tarih' : 'Regular non-EU deadline'}</label><span>${escapeHtml(formatCalendarValue(timeline.non_eu_deadline ?? timeline.deadline_non_eu))}</span></div>` : ''}
                    ${!nextCyclePending && timeline.scholarship_deadline ? `<div class="premium-item"><label>${isTurkish ? 'Burs son tarihi' : 'Scholarship deadline'}</label><span>${escapeHtml(formatCalendarValue(timeline.scholarship_deadline))}</span></div>` : ''}
                    ${!nextCyclePending && timeline.english_score_deadline_if_required ? `<div class="premium-item"><label>${isTurkish ? 'İngilizce puanı son tarihi' : 'English-score deadline'}</label><span>${escapeHtml(formatCalendarValue(timeline.english_score_deadline_if_required))}</span></div>` : ''}
                    ${!nextCyclePending && timeline.recommendation_deadline ? `<div class="premium-item"><label>${isTurkish ? 'Referans mektubu son tarihi' : 'Recommendation deadline'}</label><span>${escapeHtml(formatCalendarValue(timeline.recommendation_deadline))}</span></div>` : ''}
                    ${!nextCyclePending && timeline.enrollment_deadline ? `<div class="premium-item"><label>${isTurkish ? 'Kayıt dönemi' : 'Enrollment window'}</label><span>${escapeHtml(formatCalendarValue(timeline.enrollment_deadline))}</span></div>` : ''}
                    ${!nextCyclePending && timeline.document_completion_deadline ? `<div class="premium-item"><label>${isTurkish ? 'Belge tamamlama' : 'Document completion'}</label><span>${escapeHtml(formatCalendarValue(timeline.document_completion_deadline))}</span></div>` : ''}
                    ${timeline.decision_timing ? `<div class="premium-item"><label>${isTurkish ? 'Karar zamanı' : 'Decision timing'}</label><span>${escapeHtml(displayValue(timeline.decision_timing))}</span></div>` : ''}
                    ${timeline.offer_reply_deadline ? `<div class="premium-item"><label>${isTurkish ? 'Teklif yanıt tarihi' : 'Offer reply deadline'}</label><span>${escapeHtml(formatCalendarValue(timeline.offer_reply_deadline))}</span></div>` : ''}
                    ${timeline.visa_document_path ? `<div class="premium-item full-span source-note"><label>${isTurkish ? 'Göçmenlik belgesi adımları' : 'Immigration-document steps'}</label><span>${escapeHtml(displayValue(timeline.visa_document_path))}</span></div>` : ''}
                    ${timeline.visa_document_request_system ? `<div class="premium-item"><label>${isTurkish ? 'Göçmenlik belgesi yolu' : 'Immigration-document route'}</label><span>${escapeHtml(displayValue(timeline.visa_document_request_system))}</span></div>` : ''}
                    ${timeline.visa_document_processing_time_business_days_max != null ? `<div class="premium-item"><label>${isTurkish ? 'I-20 / DS-2019 işlem süresi' : 'I-20 / DS-2019 processing'}</label><span>${escapeHtml(`${timeline.visa_document_processing_time_business_days_min ?? '—'}–${timeline.visa_document_processing_time_business_days_max} ${isTurkish ? 'iş günü' : 'business days'}`)}</span></div>` : ''}
                    ${timeline.financial_proof_required_before_i20_or_ds2019 === true ? `<div class="premium-item full-span source-note"><label>${isTurkish ? 'Mali kanıt' : 'Financial proof'}</label><span>${escapeHtml(isTurkish ? `I-20 / DS-2019 öncesi zorunlu; tutar ${timeline.financial_proof_amount_location ? displayValue(timeline.financial_proof_amount_location) : 'başvuru sisteminde gösterilir'}.` : `Required before I-20 / DS-2019; amount ${timeline.financial_proof_amount_location ? displayValue(timeline.financial_proof_amount_location) : 'is shown in the application system'}.`)}</span></div>` : ''}
                    ${timeline.visa_sensitive_deadline ? `<div class="premium-item full-span source-note"><label>${isTurkish ? 'Vize açısından' : 'Visa-sensitive advice'}</label><span>${escapeHtml(displayValue(timeline.visa_sensitive_deadline))}</span></div>` : ''}
                    ${timeline.deadline_notes ? `<div class="premium-item full-span source-note"><label>${isTurkish ? 'Takvim riski' : 'Timeline risk'}</label><span>${escapeHtml(displayValue(timeline.deadline_notes))}</span></div>` : ''}
                </div>
                ${roundRows ? (nextCyclePending
                    ? `<details class="detail-disclosure timeline-history"><summary>${isTurkish ? 'Önceki dönemin tarihlerini yalnızca referans için göster' : 'Show previous-cycle dates for reference only'}</summary><ol class="timeline-round-list">${roundRows}</ol></details>`
                    : `<ol class="timeline-round-list">${roundRows}</ol>`) : ''}
            </div>`;

        let strongAreasHTML = '';
        if (n.strongAreas && n.strongAreas.length > 0) {
            strongAreasHTML = n.strongAreas.map(a => `<li>${escapeHtml(window.getCategoryLabel ? window.getCategoryLabel(a) : a)}</li>`).join('');
        }
        let labsHTML = '';
        if (n.labs && n.labs.length > 0) {
            labsHTML = n.labs.map(l => `<span class="lab-chip">${escapeHtml(displayValue(typeof l === 'object' ? (l.name || l.label) : l))}</span>`).join('');
        }
        let profsHTML = '';
        if (n.professors && n.professors.length > 0) {
            profsHTML = n.professors.map(p => {
                const professor = typeof p === 'object' ? p : { name: p };
                const fitTags = Array.isArray(professor.fit_tags)
                    ? professor.fit_tags.map(tag => `<span class="prof-fit-tag">${escapeHtml(window.getCategoryLabel ? window.getCategoryLabel(tag) : tag)}</span>`).join('')
                    : '';
                const timingLabel = professor.contact_timing
                    ? (String(professor.contact_timing).includes('after_admission')
                        ? (isTurkish ? 'RA iletişimi: kabul sonrası' : 'RA outreach: after admission')
                        : (isTurkish ? 'Yalnızca belirli araştırma sorusuyla yaz' : 'Contact only with a specific research question'))
                    : '';
                return `
                    <article class="prof-card">
                        <div class="prof-card__top">
                            <div><strong class="prof-name">${escapeHtml(displayValue(professor.name))}</strong>${professor.role ? `<span class="prof-role">${escapeHtml(displayValue(professor.role))}</span>` : ''}</div>
                            ${professor.profile_url ? `<a class="prof-profile-link" href="${escapeHtml(professor.profile_url)}" target="_blank" rel="noopener noreferrer">${isTurkish ? 'Resmî profil' : 'Official profile'} ↗</a>` : ''}
                        </div>
                        ${professor.focus ? `<p class="prof-focus">${escapeHtml(displayValue(professor.focus))}</p>` : ''}
                        ${fitTags ? `<div class="prof-fit-tags">${fitTags}</div>` : ''}
                        <div class="prof-card__contact">
                            ${professor.email ? `<a href="mailto:${escapeHtml(professor.email)}">${escapeHtml(professor.email)}</a>` : ''}
                            ${timingLabel ? `<span>${escapeHtml(timingLabel)}</span>` : ''}
                        </div>
                    </article>`;
            }).join('');
        }
        const facultyContactNote = n.raw?.research_profile?.faculty_contact_note;
        const researchSummaryHTML = n.researchSummary
            ? `<div class="dept-block"><label>${isTurkish ? 'Araştırma erişimi notu' : 'Research access note'}</label><p>${escapeHtml(displayValue(n.researchSummary))}</p></div>`
            : '';
        const industrySummaryHTML = n.industrySummary
            ? `<div class="dept-block"><label>${isTurkish ? 'Endüstri ekosistemi notu' : 'Industry ecosystem note'}</label><p>${escapeHtml(displayValue(n.industrySummary))}</p></div>`
            : '';
        const partnersHTML = Array.isArray(n.confirmedPartners) && n.confirmedPartners.length
            ? n.confirmedPartners.map((partner) => `<span class="lab-chip">${escapeHtml(displayValue(typeof partner === 'object' ? (partner.partner || partner.name || partner.label) : partner))}</span>`).join('')
            : '';

        let deptHTML = `
            <div class="drawer-section premium-card">
                <div class="premium-header">
                    <span class="premium-icon" aria-hidden="true"></span>
                    <h4 class="premium-title">${isTurkish ? 'Bölüm & Araştırma Bilgileri' : 'Department & Research'}</h4>
                </div>
                <div class="dept-content">
                    ${researchSummaryHTML}
                    ${strongAreasHTML ? `
                    <div class="dept-block">
                        <label>${isTurkish ? 'Güçlü Alanlar' : 'Strong Areas'}</label>
                        <ul class="aesthetic-list">${strongAreasHTML}</ul>
                    </div>` : ''}
                    ${labsHTML ? `
                    <div class="dept-block">
                        <label>${isTurkish ? 'İlgili Laboratuvarlar' : 'Related Laboratories'}</label>
                        <div class="chip-container">${labsHTML}</div>
                    </div>` : ''}
                    ${profsHTML ? `
                    <div class="dept-block">
                        <label>${isTurkish ? 'Araştırma uyumu olan hocalar' : 'Faculty matched to this research area'}</label>
                        ${facultyContactNote ? `<p class="faculty-contact-note"><strong>${isTurkish ? 'Ne zaman yazmalı?' : 'When should you contact them?'}</strong>${escapeHtml(displayValue(facultyContactNote))}</p>` : ''}
                        <div class="prof-grid">${profsHTML}</div>
                    </div>` : ''}
                    ${partnersHTML ? `
                    <div class="dept-block">
                        <label>${isTurkish ? 'Doğrulanmış ortaklar' : 'Verified partners'}</label>
                        <div class="chip-container">${partnersHTML}</div>
                    </div>` : ''}
                    ${industrySummaryHTML}
                </div>
            </div>
        `;

        // 4. Money reality.  Tuition, compulsory fees, room rent and total
        // monthly living budget are deliberately separate: a cheap tuition
        // never implies an affordable city.
        const tuitionVerified = verifiedFields.includes('tuition');
        const scholarshipVerified = verifiedFields.includes('scholarship');
        const housingVerified = verifiedFields.includes('housing');
        const unknownMoney = isTurkish ? 'Resmi kaynakla doğrulanmadı' : 'Not verified by an official source';
        const fullProgrammeFee = n.costDetails?.tuition_non_eu_full_program;
        const foreignProgrammeFee = fullProgrammeFee?.amount && fullProgrammeFee?.currency
            ? `${Number(fullProgrammeFee.amount).toLocaleString('en-US')} ${escapeHtml(fullProgrammeFee.currency)}${isTurkish ? ' (tam program)' : ' (full programme)'}`
            : '';
        const noRegularTuition = ["no_regular_tuition_within_standard_period", "no_general_tuition_regular_programme"].includes(n.costDetails?.tuition_basis);
        const tuitionText = tuitionVerified
            ? (n.tuitionPerYear !== null
                ? (noRegularTuition
                    ? (isTurkish ? 'Normal süre içinde genel öğrenim ücreti yok' : 'No general tuition within standard period')
                    : `${formatMoney(n.tuitionPerYear)}${isTurkish ? ' / yıl' : ' / year'}`)
                : n.foreignTuition
                    ? `${formatPublishedTuition(n.foreignTuition)}${publishedTuitionPeriodSuffix(n.foreignTuition, isTurkish)}`
                    : (foreignProgrammeFee || (isTurkish ? 'Tutar yayımlanmış para biriminde belirtilmemiş' : 'Amount is not stated in a published currency')))
            : unknownMoney;
        const feeText = tuitionVerified && n.semesterFee !== null
            ? `${n.semesterFeeApproximate ? '≈ ' : ''}${formatMoney(n.semesterFee)}${n.feeScope === 'enrollment' ? (isTurkish ? ' · kayıt sırasında' : ' · at enrolment') : (isTurkish ? ' / dönem' : ' / term')}`
            : tuitionVerified && n.foreignCompulsoryFee
                ? `${formatPublishedTuition(n.foreignCompulsoryFee)}${publishedTuitionPeriodSuffix(n.foreignCompulsoryFee, isTurkish)}`
            : (tuitionVerified ? '—' : unknownMoney);
        const scholarshipModeLabel = {
            automatic: isTurkish ? 'Otomatik değerlendirme' : 'Automatic consideration',
            separate: isTurkish ? 'Ayrı başvuru gerekir' : 'Separate application required',
            mixed: isTurkish ? 'Fırsata göre otomatik veya ayrı' : 'Automatic or separate, depending on the opportunity',
            nomination: isTurkish ? 'Aday gösterme' : 'Nomination',
            invitation_only: isTurkish ? 'Yalnızca davet' : 'Invitation only',
            not_available: isTurkish ? 'Mevcut değil' : 'Not available',
            unknown: isTurkish ? 'Bilinmiyor' : 'Unknown'
        }[String(n.scholarshipDetails?.application_mode || 'unknown')] || displayValue(n.scholarshipDetails?.application_mode);
        const fundingOpportunities = Array.isArray(n.scholarshipDetails?.opportunities) ? n.scholarshipDetails.opportunities : [];
        const fundingRows = fundingOpportunities.map((opportunity) => {
            const amountUsdMin = Number(opportunity.amount_usd_min);
            const amountUsdMax = Number(opportunity.amount_usd_max);
            const amount = Number.isFinite(amountUsdMin)
                ? formatPublishedRange({ min: amountUsdMin, max: Number.isFinite(amountUsdMax) ? amountUsdMax : amountUsdMin, currency: 'USD' })
                : opportunity.amount_eur != null
                ? formatMoney(opportunity.amount_eur)
                : opportunity.amount != null && opportunity.currency
                    ? formatPublishedMoney({ amount: opportunity.amount, currency: opportunity.currency })
                    : '—';
            const deadline = opportunity.deadline ? `${isTurkish ? 'Son tarih' : 'Deadline'}: ${displayValue(opportunity.deadline)}` : '';
            const eligibility = opportunity.eligibility_summary ? displayValue(opportunity.eligibility_summary) : '';
            return `<li><strong>${escapeHtml(opportunity.name || (isTurkish ? 'Burs fırsatı' : 'Funding opportunity'))}</strong><span>${escapeHtml(amount)}</span><small>${escapeHtml([deadline, eligibility].filter(Boolean).join(' · '))}</small></li>`;
        }).join('');
        const totalAttendanceCostRaw = n.costDetails?.total_cost_of_attendance_usd_per_year
            ?? n.costDetails?.total_cost_of_attendance_usd_per_academic_year;
        const totalAttendanceCost = Number(totalAttendanceCostRaw);
        const totalAttendanceCostMin = Number(n.costDetails?.total_cost_of_attendance_usd_per_year_min);
        const totalAttendanceCostMax = Number(n.costDetails?.total_cost_of_attendance_usd_per_year_max);
        const attendanceCostText = totalAttendanceCostRaw !== null
            && totalAttendanceCostRaw !== undefined
            && Number.isFinite(totalAttendanceCost)
            && totalAttendanceCost >= 0
            ? `${formatPublishedMoney({ amount: totalAttendanceCost, currency: 'USD' })}${isTurkish ? ' / akademik yıl' : ' / academic year'}`
            : Number.isFinite(totalAttendanceCostMin) && totalAttendanceCostMin >= 0
                ? `${formatPublishedRange({ min: totalAttendanceCostMin, max: Number.isFinite(totalAttendanceCostMax) ? totalAttendanceCostMax : totalAttendanceCostMin, currency: 'USD' })}${isTurkish ? ' / akademik yıl' : ' / academic year'}`
                : '';
        const twoTermBillingBaselineRaw = n.costDetails?.academic_billed_baseline_usd_per_two_terms;
        const firstYearBillingBaselineRaw = n.costDetails?.first_year_direct_university_cost_with_ship_usd
            ?? n.costDetails?.first_year_tuition_and_mandatory_fees_usd_example
            ?? n.costDetails?.total_tuition_and_required_fees_usd_nonresident;
        const academicBillingBaseline = Number(twoTermBillingBaselineRaw ?? firstYearBillingBaselineRaw);
        const academicBillingPeriodLabel = twoTermBillingBaselineRaw !== null
            && twoTermBillingBaselineRaw !== undefined
            ? (isTurkish ? ' / iki tam zamanlı dönem' : ' / two full-time terms')
            : (isTurkish ? ' / ilk yıl' : ' / first year');
        const academicBillingIsHistorical = n.costDetails?.current_for_fall_2027 === false;
        const academicBillingContext = academicBillingIsHistorical
            ? ` · ${n.costDetails?.academic_year ? `${n.costDetails.academic_year} ` : ''}${isTurkish ? 'tarihsel ölçüt; güncel değil' : 'historical benchmark; not current'}`
            : '';
        const academicBillingBaselineText = Number.isFinite(academicBillingBaseline) && academicBillingBaseline >= 0
            ? `${formatPublishedMoney({ amount: academicBillingBaseline, currency: 'USD' })}${academicBillingPeriodLabel}${academicBillingContext}`
            : '';
        const insurancePremiumRaw = n.costDetails?.health_insurance_premium_usd
            ?? n.costDetails?.health_insurance_usd_per_year
            ?? n.costDetails?.anthem_gold_ship_usd_per_year_fall_and_spring
            ?? n.costDetails?.ship_health_insurance_usd;
        const insurancePremium = Number(insurancePremiumRaw);
        const insurancePremiumVerified = insurancePremiumRaw !== null
            && insurancePremiumRaw !== undefined
            && Number.isFinite(insurancePremium)
            && insurancePremium >= 0;
        const insuranceRequired = n.costDetails?.health_insurance_required_for_international_students === true
            || n.costDetails?.health_insurance_required_for_f_or_j_students === true
            || n.costDetails?.health_insurance_required === true;
        const insuranceText = insuranceRequired
            ? insurancePremiumVerified
                ? `${formatPublishedMoney({ amount: insurancePremium, currency: 'USD' })}${isTurkish ? ' · zorunlu' : ' · required'}${academicBillingContext}`
                : (isTurkish ? 'Zorunlu; 2026/27 primi doğrulanamadı' : 'Required; 2026/27 premium not verified')
            : '';
        const financeHTML = `
            <div class="drawer-section premium-card financial-card">
                <div class="premium-header"><span class="premium-icon" aria-hidden="true"></span><h4 class="premium-title">${isTurkish ? 'Maliyet & Burs Gerçeği' : 'Cost & Funding Reality'}</h4></div>
                <p class="card-disclaimer">${isTurkish ? 'Tutarlar yalnızca kontrol edilmiş resmi kaynak bulunduğunda gösterilir. Konaklama ve yaşam bütçesi okul ücretinden ayrıdır.' : 'Amounts are displayed only with a checked official source. Housing and living budget are separate from tuition.'}</p>
                <div class="premium-grid">
                    <div class="premium-item"><label>${isTurkish ? 'Öğrenim ücreti' : 'Tuition'}${n.tuitionScope === 'non_eu_target' ? ` · ${isTurkish ? 'AB dışı hedef' : 'non-EU target'}` : ''}</label><span class="finance-val tuition">${tuitionText}</span></div>
                    <div class="premium-item"><label>${isTurkish ? 'Zorunlu ek ücret' : 'Compulsory fee'}</label><span class="finance-val fee">${feeText}</span></div>
                    ${attendanceCostText ? `<div class="premium-item"><label>${isTurkish ? 'Resmî toplam katılım bütçesi' : 'Official total cost of attendance'}</label><span class="finance-val">${attendanceCostText}</span></div>` : ''}
                    ${academicBillingBaselineText ? `<div class="premium-item"><label>${academicBillingIsHistorical ? (isTurkish ? 'Tarihsel akademik faturalama tabanı' : 'Historical academic billing baseline') : (isTurkish ? 'Güncel akademik faturalama tabanı' : 'Current academic billing baseline')}</label><span class="finance-val">${academicBillingBaselineText}</span></div>` : ''}
                    ${insuranceText ? `<div class="premium-item"><label>${isTurkish ? 'Sağlık sigortası' : 'Health insurance'}</label><span class="finance-val">${escapeHtml(insuranceText)}</span></div>` : ''}
                    <div class="premium-item full-span scholarship-box"><label>${isTurkish ? 'Burs / ücret muafiyeti' : 'Scholarship / fee waiver'}</label><span class="scholarship-text">${scholarshipVerified ? escapeHtml(compactList(n.scholarshipSummary) || '—') : unknownMoney}</span></div>
                    ${scholarshipVerified ? `<div class="premium-item"><label>${isTurkish ? 'Burs değerlendirme biçimi' : 'Funding consideration'}</label><span>${escapeHtml(scholarshipModeLabel)}</span></div>` : ''}
                    ${scholarshipVerified && (n.scholarshipDetails?.scholarship_deadline || n.scholarshipDetails?.funding_deadline || n.scholarshipDetails?.deadline) ? `<div class="premium-item"><label>${isTurkish ? 'Güncel burs son tarihi' : 'Current funding deadline'}</label><span>${escapeHtml(displayValue(n.scholarshipDetails.scholarship_deadline || n.scholarshipDetails.funding_deadline || n.scholarshipDetails.deadline))}</span></div>` : ''}
                    ${n.costDetails?.cost_notes ? `<div class="premium-item full-span source-note"><label>${isTurkish ? 'Maliyet notu' : 'Cost note'}</label><span>${escapeHtml(displayValue(n.costDetails.cost_notes))}</span></div>` : ''}
                    ${n.costDetails?.verification_notes ? `<div class="premium-item full-span source-note"><label>${isTurkish ? 'Maliyet doğrulama notu' : 'Cost verification note'}</label><span>${escapeHtml(displayValue(n.costDetails.verification_notes))}</span></div>` : ''}
                </div>
                ${fundingRows ? `<details class="detail-disclosure"><summary>${isTurkish ? `Doğrulanan güncel fırsatlar (${fundingOpportunities.length})` : `Verified current opportunities (${fundingOpportunities.length})`}</summary><ul class="funding-detail-list">${fundingRows}</ul></details>` : ''}
            </div>`;

        const roomRentText = housingVerified && n.euroRoomRent
            ? `${formatPublishedRange(n.euroRoomRent)}${isTurkish ? ' / ay (oda)' : ' / month (room)'}`
            : housingVerified && n.averageRoomRent !== null
            ? `${formatMoney(n.averageRoomRent)}${isTurkish ? ' / ay (oda)' : ' / month (room)'}`
            : housingVerified && n.foreignRoomRent
                ? `${formatPublishedRange(n.foreignRoomRent)}${n.foreignRoomRent.kind === 'housing_estimate' ? (isTurkish ? ' / ay' : ' / month') : (isTurkish ? ' / ay (oda)' : ' / month (room)')}${n.foreignRoomRent.kind === 'official_graduate_housing_rate' ? ` · ${n.foreignRoomRent.academicYear ? `${n.foreignRoomRent.academicYear} ` : ''}${isTurkish ? 'resmî lisansüstü konutu' : 'official graduate housing'}` : ''}`
            : unknownMoney;
        const housingAmountLabel = n.foreignRoomRent?.kind === 'housing_estimate'
            ? (isTurkish ? 'Üniversite dairesi kirası' : 'University apartment rent')
            : (isTurkish ? 'Oda kirası' : 'Room rent');
        // A checked national average is useful for planning, but must never
        // look like a city-specific rent quote.  The database may therefore
        // attach an explicit scope label next to the amount.
        const roomRentScope = n.livingDetails?.average_room_rent_scope_label
            ? displayValue(n.livingDetails.average_room_rent_scope_label)
            : '';
        const roomRentLabel = roomRentScope
            ? `${housingAmountLabel} · ${roomRentScope}`
            : housingAmountLabel;
        const monthlyLivingText = housingVerified && (n.monthlyLivingCostMin !== null || n.monthlyLivingCost !== null)
            ? (n.monthlyLivingCostMin !== null && n.monthlyLivingCostMax !== null
                ? `${formatMoney(n.monthlyLivingCostMin)}–${formatMoney(n.monthlyLivingCostMax)}${isTurkish ? ' / ay' : ' / month'}`
                : `${formatMoney(n.monthlyLivingCost ?? n.monthlyLivingCostMin)}${isTurkish ? ' / ay' : ' / month'}`)
            : housingVerified && n.foreignMonthlyLivingBudget
                ? `${formatPublishedRange(n.foreignMonthlyLivingBudget)}${isTurkish ? ' / ay' : ' / month'}`
            : unknownMoney;
        const monthlyLivingScope = n.livingDetails?.monthly_living_cost_scope_label
            ? displayValue(n.livingDetails.monthly_living_cost_scope_label)
            : '';
        const monthlyLivingLabel = monthlyLivingScope
            ? `${isTurkish ? 'Aylık toplam yaşam bütçesi' : 'Monthly living budget'} · ${monthlyLivingScope}`
            : (isTurkish ? 'Aylık toplam yaşam bütçesi' : 'Monthly living budget');
        const housingAccessLabel = n.livingDetails?.housing_guarantee_type === 'conditional_first_year_guarantee'
            ? (isTurkish ? 'İlk yıl koşullu garanti' : 'Conditional first-year guarantee')
            : ({
            guaranteed: isTurkish ? 'Garantili' : 'Guaranteed',
            priority: isTurkish ? 'Öncelik veriliyor; garanti değil' : 'Priority, not guaranteed',
            lottery: isTurkish ? 'Kura' : 'Lottery',
            waitlist: isTurkish ? 'Bekleme listesi' : 'Waitlist',
            first_come_first_served: isTurkish ? 'İlk gelen alır' : 'First come, first served',
            not_guaranteed: isTurkish ? 'Sunuluyor; garanti değil' : 'Offered, not guaranteed',
            available_not_guaranteed: isTurkish ? 'Mevcut; garanti değil' : 'Available, not guaranteed',
            not_offered: isTurkish ? 'Üniversite yurdu sunulmuyor' : 'University housing not offered',
            unknown: isTurkish ? 'Bilinmiyor' : 'Unknown'
        }[String(n.livingDetails?.housing_access || 'unknown')] || displayValue(n.livingDetails?.housing_access));
        const officialRentItems = Array.isArray(n.livingDetails?.official_rent_items) ? n.livingDetails.official_rent_items : [];
        const officialRentRows = officialRentItems.map((item) => {
            const label = displayValue(item.item || item.name);
            const min = Number(item.amount_usd_min);
            const max = Number(item.amount_usd_max);
            const range = Number.isFinite(min)
                ? formatPublishedRange({ min, max: Number.isFinite(max) ? max : min, currency: 'USD' })
                : '—';
            const periodLabels = {
                academic_year: isTurkish ? 'akademik yıl' : 'academic year',
                '12_month_contract': isTurkish ? '12 aylık sözleşme' : '12-month contract',
                month: isTurkish ? 'ay' : 'month'
            };
            return `<li><strong>${escapeHtml(label)}</strong><span>${escapeHtml(range)}</span><small>${escapeHtml(periodLabels[item.period] || item.period || '')}</small></li>`;
        }).join('');
        const livingHTML = `
            <div class="drawer-section premium-card">
                <div class="premium-header"><span class="premium-icon" aria-hidden="true"></span><h4 class="premium-title">${isTurkish ? 'Konaklama & Yaşam' : 'Housing & Living'}</h4></div>
                <div class="premium-grid">
                    <div class="premium-item"><label>${roomRentLabel}</label><span class="finance-val">${roomRentText}</span></div>
                    <div class="premium-item"><label>${monthlyLivingLabel}</label><span class="finance-val">${monthlyLivingText}</span></div>
                    <div class="premium-item"><label>${isTurkish ? 'Üniversite konutu' : 'University housing'}</label><span>${escapeHtml(housingAccessLabel)}</span></div>
                    <div class="premium-item"><label>${isTurkish ? 'Konaklama başvurusu' : 'Housing application'}</label><span>${n.livingDetails?.housing_access === 'not_offered'
                        ? (isTurkish ? 'Harici sağlayıcıya ayrı başvuru gerekir' : 'Separate application to an external provider')
                        : yesNoUnknown(n.livingDetails?.housing_application_separate)}</span></div>
                    <div class="premium-item"><label>${isTurkish ? 'Konut bulma riski' : 'Housing availability risk'}</label>${housingVerified ? formatRiskBadge(n.housingDifficulty) : `<span class="risk-badge risk-unknown">${unknownMoney}</span>`}</div>
                    ${housingVerified && n.foreignAnnualLivingBudget ? `<div class="premium-item"><label>${isTurkish ? 'Resmî yıllık yaşam bütçesi' : 'Official annual living budget'}</label><span class="finance-val">${formatPublishedRange(n.foreignAnnualLivingBudget)}</span></div>` : ''}
                    ${housingVerified && n.foreignAnnualHousingBudget ? `<div class="premium-item"><label>${isTurkish ? 'Resmî yıllık konut bütçesi' : 'Official annual housing budget'}</label><span class="finance-val">${formatPublishedRange(n.foreignAnnualHousingBudget)}</span></div>` : ''}
                    ${housingVerified && n.foreignMonthlyBudgetExamples ? `<div class="premium-item full-span source-note"><label>${isTurkish ? 'Resmî öğrenci bütçesi örnekleri' : 'Official student budget examples'}</label><span>${n.foreignMonthlyBudgetExamples.values.map((value) => `${Number(value).toLocaleString('en-US')} ${n.foreignMonthlyBudgetExamples.currency}${isTurkish ? ' / ay' : ' / month'}`).join(' · ')}</span></div>` : ''}
                    ${n.monthlyLivingCostBasis ? `<div class="premium-item full-span source-note"><label>${isTurkish ? 'Bütçe kapsamı' : 'Budget basis'}</label><span>${escapeHtml(displayValue(n.monthlyLivingCostBasis))}</span></div>` : ''}
                    ${n.livingDetails?.housing_notes ? `<div class="premium-item full-span source-note"><label>${isTurkish ? 'Konut notu' : 'Housing note'}</label><span>${escapeHtml(displayValue(n.livingDetails.housing_notes))}</span></div>` : ''}
                </div>
                ${officialRentRows ? `<details class="detail-disclosure"><summary>${isTurkish ? `Resmî konut ve yemek fiyatları (${officialRentItems.length})` : `Official housing and meal rates (${officialRentItems.length})`}</summary><ul class="funding-detail-list">${officialRentRows}</ul></details>` : ''}
            </div>`;

        // 6. Avantaj ve Dezavantajlar (Pros & Cons)
        let prosHTML = '';
        let consHTML = '';
        if (n.mainStrengths && n.mainStrengths.length) {
            prosHTML = n.mainStrengths.map(p => `<li><span class="icon">✅</span> <span class="text">${window.localizedField(p)}</span></li>`).join('');
        }
        if (n.mainRisks && n.mainRisks.length) {
            consHTML = n.mainRisks.map(c => `<li><span class="icon">⚠️</span> <span class="text">${window.localizedField(c)}</span></li>`).join('');
        }

        let prosConsHTML = '';
        if (prosHTML || consHTML) {
            prosConsHTML = `
            <div class="drawer-section premium-card pros-cons-card">
                <div class="premium-header">
                    <span class="premium-icon" aria-hidden="true"></span>
                    <h4 class="premium-title">${isTurkish ? 'Avantaj & Dezavantaj Analizi' : 'Strengths & Risks'}</h4>
                </div>
                <div class="pros-cons-grid">
                    ${prosHTML ? `<div class="pros-col"><h5>${isTurkish ? 'Artılar' : 'Pros'}</h5><ul class="clean-list">${prosHTML}</ul></div>` : ''}
                    ${consHTML ? `<div class="cons-col"><h5>${isTurkish ? 'Eksiler' : 'Cons'}</h5><ul class="clean-list">${consHTML}</ul></div>` : ''}
                </div>
            </div>`;
        }

        // 6.5 Student experience is deliberately displayed as perception,
        // never as a substitute for the official programme facts above.
        const sentiment = n.studentSentiment || {};
        const sentimentSources = Array.isArray(n.studentReviews) ? n.studentReviews : [];
        // Search result pages and platform homepages are not student comments.
        // Only render direct, accessible discussion/review URLs as evidence.
        const directSentimentSources = sentimentSources.map((review) => {
            if (typeof review === 'string') return { title: isTurkish ? 'Öğrenci deneyimi kaynağı' : 'Student-experience source', url: review };
            return review && typeof review === 'object' ? review : {};
        }).filter((review) => {
            const url = safeUrl(review.url);
            return Boolean(url) && !/\/(?:search|r\/[^/]+)\/?(?:[?#].*)?$/i.test(url) && !/eksisozluk\.com\/?$/i.test(url);
        });
        const rawSentimentScore = sentiment.student_satisfaction_score;
        const sentimentScore = rawSentimentScore !== null && rawSentimentScore !== undefined && rawSentimentScore !== '' && Number.isFinite(Number(rawSentimentScore))
            ? Number(rawSentimentScore)
            : null;
        const sentimentSummary = displayValue(sentiment.sentiment_summary || sentiment.student_sentiment_summary || sentiment.verification_notes);
        const sourceLinks = directSentimentSources.map((review) => {
            const url = safeUrl(review?.url);
            const title = review?.title || review?.source || review?.platform || (isTurkish ? 'Öğrenci deneyimi kaynağı' : 'Student-experience source');
            const quote = review?.quote ? `<p class="review-quote">“${escapeHtml(review.quote)}”</p>` : '';
            return `<li>${quote}<span>${escapeHtml(title)}</span>${url ? `<a href="${url}" target="_blank" rel="noreferrer">${isTurkish ? 'Kaynağı aç ↗' : 'Open source ↗'}</a>` : ''}</li>`;
        }).join('');
        const studentReviewsHTML = `
            <div class="drawer-section premium-card student-reviews-card">
                <div class="premium-header"><span class="premium-icon" aria-hidden="true"></span><h4 class="premium-title">${isTurkish ? 'Öğrenci Deneyimi Sinyali' : 'Student Experience Signal'}</h4></div>
                <p class="card-disclaimer">${isTurkish ? 'Bu bölüm resmi bilgi değildir; sınırlı öğrenci deneyimlerinin ihtiyatlı bir özetidir.' : 'This section is not official fact; it is a cautious summary of student-experience evidence.'}</p>
                <div class="sentiment-facts">
                    <span><b>${sentimentScore === null ? '—' : `${sentimentScore}/100`}</b><small>${isTurkish ? 'memnuniyet sinyali' : 'satisfaction signal'}</small></span>
                    <span><b>${directSentimentSources.length || '—'}</b><small>${isTurkish ? 'doğrudan kaynak' : 'direct sources'}</small></span>
                    <span><b>${escapeHtml(confidenceLabel(sentiment.sentiment_confidence).label)}</b><small>${isTurkish ? 'güven' : 'confidence'}</small></span>
                </div>
                ${sentiment.date_range ? `<p class="sentiment-date">${isTurkish ? 'Tarih aralığı: ' : 'Date range: '}${escapeHtml(sentiment.date_range)}</p>` : ''}
                <p class="sentiment-summary">${escapeHtml(sentimentSummary || (isTurkish ? 'Kaynaklı öğrenci deneyimi özeti henüz yeterli değil; bu nedenle puan gösterilmiyor.' : 'There is not yet enough sourced student-experience evidence, so no score is shown.'))}</p>
                ${sourceLinks ? `<ul class="student-source-list">${sourceLinks}</ul>` : `<p class="empty-source-note">${isTurkish ? 'Doğrudan ve erişilebilir öğrenci yorumu kaynağı henüz doğrulanmadı.' : 'No direct, accessible student-review source has been verified yet.'}</p>`}
            </div>`;

        // Raw pipeline enums ("requires_js", "official_program_page",
        // "Bilinmiyor / Resmi Veri Yok") are translated before display.
        const accessStatusLabel = (value) => {
            const raw = String(value || 'unknown').trim().toLowerCase();
            const key = /bilinmiyor/.test(raw) ? 'unknown' : raw.replace(/\s+/g, '_');
            const labels = {
                ok: { en: 'Accessible', tr: 'Erişilebilir' },
                redirects: { en: 'Redirects', tr: 'Yönlendirme' },
                pdf: { en: 'PDF', tr: 'PDF' },
                requires_js: { en: 'Requires JS', tr: 'JS gerektirir' },
                blocked: { en: 'Blocked', tr: 'Engellendi' },
                broken: { en: 'Broken', tr: 'Kırık bağlantı' },
                not_found: { en: 'Not found', tr: 'Bulunamadı' },
                unknown: { en: 'Unverified', tr: 'Doğrulanmadı' }
            };
            const label = labels[key] || labels.unknown;
            return { key: labels[key] ? key : 'unknown', label: isTurkish ? label.tr : label.en };
        };
        const sourceTypeLabel = (value) => {
            const key = String(value || 'other').trim().toLowerCase();
            const labels = {
                official_program_page: { en: 'Official programme page', tr: 'Resmî program sayfası' },
                official_admission_page: { en: 'Official admission page', tr: 'Resmî kabul sayfası' },
                official_curriculum_page: { en: 'Official curriculum page', tr: 'Resmî müfredat sayfası' },
                official_tuition_page: { en: 'Official tuition page', tr: 'Resmî ücret sayfası' },
                official_scholarship_page: { en: 'Official scholarship page', tr: 'Resmî burs sayfası' },
                official_department_page: { en: 'Official department page', tr: 'Resmî bölüm sayfası' },
                official_lab_page: { en: 'Official lab page', tr: 'Resmî laboratuvar sayfası' },
                official_housing_page: { en: 'Official housing page', tr: 'Resmî konaklama sayfası' },
                official_visa_or_government_page: { en: 'Official government page', tr: 'Resmî devlet sayfası' },
                official_industry_partner_page: { en: 'Official partner page', tr: 'Resmî ortak sayfası' },
                student_forum: { en: 'Student forum', tr: 'Öğrenci forumu' },
                third_party_database: { en: 'Third-party database', tr: 'Üçüncü taraf veritabanı' }
            };
            const label = labels[key];
            if (label) return isTurkish ? label.tr : label.en;
            return String(value || 'other').replaceAll('_', ' ');
        };
        const sourceRows = (n.sources || []).map((item) => {
            const url = safeUrl(item?.url);
            const title = item?.title || sourceTypeLabel(item?.source_type) || (isTurkish ? 'Kaynak' : 'Source');
            const access = accessStatusLabel(item?.access_status);
            const type = sourceTypeLabel(item?.source_type);
            const fields = Array.isArray(item?.relevant_fields) && item.relevant_fields.length
                ? item.relevant_fields.map(humanField).join(', ')
                : (isTurkish ? 'Alan belirtilmemiş' : 'Fields not specified');
            return `<li><div><strong>${escapeHtml(title)}</strong><small>${escapeHtml(type)} · ${escapeHtml(fields)}</small></div><span class="source-access source-access--${escapeHtml(access.key.replace(/_/g, '-'))}">${escapeHtml(access.label)}</span>${url ? `<a href="${url}" target="_blank" rel="noreferrer">↗</a>` : ''}</li>`;
        }).join('');
        const sourcesHTML = `
            <div class="drawer-section premium-card sources-card">
                <div class="premium-header"><span class="premium-icon" aria-hidden="true"></span><h4 class="premium-title">${isTurkish ? 'Kaynak Günlüğü' : 'Source Log'}</h4></div>
                <p class="card-disclaimer">${isTurkish ? 'Her sayı veya iddia için kaynak türünü ve erişim durumunu görün. “unknown”, “broken” veya “requires js” durumları karar kanıtı değildir.' : 'Inspect the source type and access status behind each claim. “unknown”, “broken” and “requires js” are not decision evidence.'}</p>
                ${sourceRows ? `<ul class="source-log-list">${sourceRows}</ul>` : `<p class="empty-source-note">${isTurkish ? 'Kaynak günlüğü henüz yok.' : 'No source log yet.'}</p>`}
            </div>`;

        // 7. Linkler (Links)
        let linksHTML = `
            <div class="drawer-section links-card">
                <div class="action-buttons">
                    ${n.programUrl && n.programUrl !== '—' ? `<a href="${n.programUrl}" target="_blank" class="premium-btn main-action">${isTurkish ? 'Programa Git' : 'Programme Page'} ↗</a>` : ''}
                    ${n.admissionUrl && n.admissionUrl !== '—' ? `<a href="${n.admissionUrl}" target="_blank" class="premium-btn secondary-action">${isTurkish ? 'Kabul Sayfası' : 'Admissions'} ↗</a>` : ''}
                    ${n.tuitionUrl && n.tuitionUrl !== '—' ? `<a href="${n.tuitionUrl}" target="_blank" class="premium-btn secondary-action">${isTurkish ? 'Okul Ücreti' : 'Tuition & Fees'} ↗</a>` : ''}
                    ${n.scholarshipUrl && n.scholarshipUrl !== '—' ? `<a href="${n.scholarshipUrl}" target="_blank" class="premium-btn secondary-action">${isTurkish ? 'Burs Sayfası' : 'Scholarships'} ↗</a>` : ''}
                </div>
            </div>
        `;

        document.getElementById('drawer-info').innerHTML =
            decisionHeroHTML +
            verificationBanner +
            qualityHTML +
            scoreImpactHTML +
            basicInfoHTML +
            admissionsHTML +
            timelineHTML +
            curriculumHTML +
            financeHTML +
            livingHTML +
            deptHTML +
            studentReviewsHTML +
            prosConsHTML +
            sourcesHTML +
            linksHTML;

        // 1. Radar Chart Setup
        const ctx = document.getElementById('radarChart');
        if (ctx) {
            if (window.uniChart) {
                window.uniChart.destroy();
            }
            
            const sd = data._scoringDetails ? data._scoringDetails.components : {};
            const fitMetric = (sd.academic_fit || 0) / 10;
            const eligMetric = (sd.eligibility_language || 0) / 10;
            const costMetric = (sd.cost_funding || 0) / 10;
            const careerMetric = (sd.career_research || 0) / 10;
            const livingMetric = (sd.living_risk || 0) / 10;
            const confMetric = (sd.confidence_deadline || 0) / 10;

            window.uniChart = new Chart(ctx.getContext('2d'), {
                type: 'radar',
                data: {
                    labels: [isTurkish ? 'Akademik Güç' : 'Academic Strength', isTurkish ? 'Uygunluk' : 'Eligibility', isTurkish ? 'Maliyet & Fon' : 'Cost & Fund.', isTurkish ? 'Kariyer' : 'Career', isTurkish ? 'Yaşam Riski' : 'Living Risk', isTurkish ? 'Veri Güveni' : 'Data Conf.'],
                    datasets: [{
                        data: [fitMetric, eligMetric, costMetric, careerMetric, livingMetric, confMetric],
                        backgroundColor: 'rgba(232, 128, 74, 0.18)',
                        borderColor: '#e8804a',
                        pointBackgroundColor: '#d7c765',
                        pointBorderColor: '#141519',
                        pointHoverBackgroundColor: '#f4efe5',
                        pointHoverBorderColor: '#e8804a'
                    }]
                },
                options: {
                    scales: {
                        r: {
                            angleLines: { color: 'rgba(255, 255, 255, 0.1)' },
                            grid: { color: 'rgba(255, 255, 255, 0.1)' },
                            pointLabels: { color: '#aaa9a8', font: { family: 'Source Sans 3', size: 11 } },
                            ticks: { display: false, min: 0, max: 10 }
                        }
                    },
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    return context.raw.toFixed(2) + ' / 1.0';
                                }
                            }
                        }
                    },
                    maintainAspectRatio: false
                }
            });
        }

        els.drawer.panel.classList.add('active');
        els.drawer.overlay.classList.add('active');
        els.drawer.panel.setAttribute('aria-hidden', 'false');
        document.body.classList.add('drawer-open');
        els.drawer.body.scrollTop = 0;
        setTimeout(() => els.drawer.closeBtn.focus(), 40);
    } catch (err) {
        console.error('Drawer Error:', err);
    }
}
function closeDrawer() {
    els.drawer.panel.classList.remove('active');
    els.drawer.overlay.classList.remove('active');
    els.drawer.panel.setAttribute('aria-hidden', 'true');
    document.body.classList.remove('drawer-open');
    activeDrawerData = null;
    if (window.lastDrawerTrigger instanceof HTMLElement) window.lastDrawerTrigger.focus();
}

document.addEventListener('languageChanged', async () => {
    // Re-render components that depend on language
    if (rawData.length > 0) {
        els.countryFilter.innerHTML = '<option value="" data-i18n="search_country">Search country...</option>';
        
        populateCountryFilter();
        renderCountryTags();
        
        if (window.renderCategoryUI) window.renderCategoryUI();
        
        // Re-apply static translations inside dynamically updated selects
        if (window.applyTranslations) {
            // But applyTranslations triggers this event, so we just manually fix the default options.
            const allCountriesOpt = els.countryFilter.querySelector('option[value=""]');
            if (allCountriesOpt) allCountriesOpt.textContent = window.t('all_countries');
            

        }

        const drawerDataToRender = activeDrawerData;
        const drawerWasOpen = els.drawer.panel.classList.contains('active');
        const drawerScrollTop = els.drawer.body.scrollTop;
        processAndRender();
        
        // Re-render the open record so bilingual programme data changes immediately too.
        if (drawerWasOpen && drawerDataToRender) {
            openDrawer(drawerDataToRender);
            els.drawer.body.scrollTop = drawerScrollTop;
        }
    }
});

window.processAndRender = processAndRender;
window.openDrawer = openDrawer;

function startApplication() {
    init().catch((error) => {
        console.error('Application initialization failed:', error);
        const message = window.currentLanguage === 'tr'
            ? 'Uygulama başlatılamadı. Lütfen sayfayı yenileyin.'
            : 'The application could not start. Please refresh the page.';
        els.tableBody.innerHTML = `<div class="empty-results-card" role="alert"><h3>${escapeHtml(message)}</h3></div>`;
    });
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', startApplication, { once: true });
} else {
    startApplication();
}



window.updateAuthUI = function() {
    const authLinks = document.getElementById('auth-links');
    const authProfile = document.getElementById('auth-profile');
    if (window.currentUser) {
        if (authLinks) authLinks.style.display = 'none';
        if (authProfile) {
            authProfile.style.display = 'flex';
            document.getElementById('auth-user-name').textContent = window.currentUser.display_name;
        }
    } else {
        if (authLinks) authLinks.style.display = 'flex';
        if (authProfile) authProfile.style.display = 'none';
    }
    
    // Update Use My Profile button state
    const useProfileBtn = document.getElementById('btn-use-profile');
    if (useProfileBtn) {
        const isApplied = Boolean(window.personalizationEnabled);
        useProfileBtn.classList.toggle('active', isApplied);
        useProfileBtn.setAttribute('aria-pressed', String(isApplied));

        // Keep the authored component structure intact. Replacing the entire
        // button with a text node made its spacing and hierarchy collapse after
        // every auth refresh.
        const icon = useProfileBtn.querySelector('.profile-cta__icon');
        const title = useProfileBtn.querySelector('.profile-cta__copy strong');
        const description = useProfileBtn.querySelector('.profile-cta__copy small');
        if (icon) icon.textContent = isApplied ? '✓' : '◎';
        if (title) title.textContent = window.t(isApplied ? 'profile_applied' : 'use_my_profile');
        if (description) description.textContent = window.t('profile_cta_desc');
    }
};

window.togglePersonalization = function() {
    if (!window.currentUser) {
        window.openLoginModal();
        return;
    }
    if (!window.userProfile) {
        window.openProfileModal();
        return;
    }
    window.setPersonalization(!window.personalizationEnabled);
    window.updateAuthUI();
};
