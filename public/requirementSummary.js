/**
 * Requirement summary: the admission facts a reader scans first, as tokens.
 *
 * "IELTS 6.5", "GRE not required", "3 recommendation letters", "GPA ≥ 3.0/4"
 * used to be spread across the admission card, the language card and the
 * document list, so answering "can I apply here?" meant reading the whole
 * rail.  This panel lifts those facts to the top of the drawer.
 *
 * Nothing here is inferred.  A token exists only when the record publishes
 * the value; a fact the catalogue has not verified renders as a muted
 * "not verified" token rather than a guess, and never as an absence that
 * could be read as "not needed".
 */
(function () {
  'use strict';

  const esc = (value) => String(value ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');

  const tr = () => window.currentLanguage === 'tr';
  const t = (en, tur) => (tr() ? tur : en);
  const text = (value) => {
    if (value === null || value === undefined) return '';
    if (typeof value === 'string' || typeof value === 'number') return String(value).trim();
    if (typeof value === 'object') return text(value[tr() ? 'tr' : 'en'] ?? value.en ?? value.tr ?? value.name ?? value.label);
    return '';
  };
  const english = (value) => {
    if (value === null || value === undefined) return '';
    if (typeof value === 'string' || typeof value === 'number') return String(value).trim();
    if (typeof value === 'object') return english(value.en ?? value.name ?? value.label ?? value.tr);
    return '';
  };
  const number = (value) => {
    if (value === null || value === undefined || value === '') return null;
    const parsed = typeof value === 'number' ? value : Number(String(value).trim().replace(',', '.'));
    return Number.isFinite(parsed) ? parsed : null;
  };
  const fmt = (value) => String(value).replace('.', tr() ? ',' : '.');

  // ------------------------------------------------------------ English tests

  const TEST_NAMES = [
    [/ielts/i, 'IELTS'],
    [/toefl/i, 'TOEFL iBT'],
    [/duolingo/i, 'Duolingo'],
    [/pte/i, 'PTE Academic'],
    [/c2|proficiency|cpe/i, 'Cambridge C2'],
    [/c1|advanced|cae/i, 'Cambridge C1'],
    [/b2|first|fce/i, 'Cambridge B2'],
    [/cambridge/i, 'Cambridge'],
    [/oxford/i, 'Oxford Test'],
    [/trinity/i, 'Trinity ISE'],
  ];

  function shortTestName(raw) {
    const name = english(raw);
    if (!name) return '';
    // The 2026 TOEFL rescaling is published as two rows for one test; the
    // reader wants the score on the scale a test taken now reports.
    const found = TEST_NAMES.find(([pattern]) => pattern.test(name));
    return found ? found[1] : '';
  }

  // The 2026 TOEFL rescaling is published as two rows for one test.  The
  // row for tests taken before the change is skipped, so the token shows the
  // bar a test taken now has to clear.
  function isOldToeflScale(raw) {
    const name = english(raw).toLowerCase();
    return /toefl/.test(name) && /before|old|former|prior|önce|eski/.test(name);
  }

  function englishTokens(language) {
    const tests = new Map();
    const push = (rawName, minimum, grade, note) => {
      const name = shortTestName(rawName);
      if (!name) return;
      const min = number(minimum);
      if (min === null && !grade) return;
      if (isOldToeflScale(rawName)) return;
      const existing = tests.get(name);
      // Keep the lowest published overall minimum for the test: a university
      // that lists 90 (old scale) and 4.5 (new scale) is asking for one bar.
      if (!existing || (min !== null && existing.min !== null && min < existing.min)) tests.set(name, { min, grade, note });
      else if (!existing.min && !existing.grade) tests.set(name, { min, grade, note });
    };

    // Some records publish the minimum as a policy keyed by test date
    // ({ test_before_2026_01_21: { overall: 90 }, test_on_or_after_2026_01_21:
    // { overall: 4.5 } }); the row for a test taken now is the one that counts.
    const policyMinimum = (policy) => {
      if (!policy || typeof policy !== 'object') return null;
      const entries = Object.entries(policy);
      const current = entries.find(([key]) => /after|new|current|2026/i.test(key) && !/before/i.test(key)) || entries.find(([key]) => !/before|old|former/i.test(key));
      const value = current ? current[1] : null;
      return value && typeof value === 'object' ? value.overall ?? value.total ?? null : value;
    };

    const lists = [language.accepted_english_tests, language.accepted_tests, language.english_tests];
    lists.forEach((list) => {
      (Array.isArray(list) ? list : []).forEach((test) => {
        if (!test) return;
        if (typeof test === 'string') { push(test, null, null); return; }
        // Prefer the score on the scale a test taken today reports.
        const newScale = test.minimum_score_new_scale ?? test.minimum_score_2026_scale ?? policyMinimum(test.minimum_score_policy);
        push(test.test || test.name, newScale ?? test.minimum_score ?? test.minimum_overall ?? test.minimum_score_old_scale, test.minimum_grade || null, english(test.score_purpose || test.subscore_rule));
      });
    });

    const scores = language.minimum_scores;
    if (scores && typeof scores === 'object' && !Array.isArray(scores)) {
      Object.entries(scores).forEach(([key, value]) => {
        const readable = key.replace(/_/g, ' ');
        const min = value && typeof value === 'object' ? value.overall : value;
        if (number(min) === null) return;
        push(readable, min, null);
      });
    }

    const tokens = [];
    tests.forEach((value, name) => {
      let shown = value.min !== null ? fmt(value.min) : (value.grade ? String(value.grade) : '');
      // A TOEFL bar of six or less is on the 1–6 scale introduced in 2026.
      if (shown && name === 'TOEFL iBT' && value.min !== null && value.min <= 6) shown = `${shown} (${t('2026 scale', '2026 ölçeği')})`;
      if (shown) tokens.push({ kind: name, value: shown, tone: 'blue', title: value.note || t('Published minimum overall score', 'Yayımlanmış asgari toplam puan') });
    });
    // IELTS first, TOEFL second: the two a Turkish applicant actually sits.
    const order = ['IELTS', 'TOEFL iBT'];
    tokens.sort((a, b) => (order.indexOf(a.kind) === -1 ? 9 : order.indexOf(a.kind)) - (order.indexOf(b.kind) === -1 ? 9 : order.indexOf(b.kind)));
    if (tokens.length) return tokens.slice(0, 3).concat(tokens.length > 3 ? [{ kind: t('English', 'İngilizce'), value: `+${tokens.length - 3}`, tone: 'blue', title: tokens.slice(3).map((item) => `${item.kind} ${item.value}`).join(' · ') }] : []);

    // No structured test rows: read the published sentence for the two
    // common tests only, and otherwise say that proof is required.
    const level = english(language.english_level_required);
    const ielts = level.match(/ielts(?:\s*academic)?\s*(?:minimum|min\.?|at least|of|overall)?\s*(\d(?:[.,]\d)?)/i);
    const toefl = level.match(/toefl(?:\s*ibt)?\s*(?:minimum|min\.?|at least|of|overall)?\s*(\d{2,3})/i);
    const cefr = level.match(/\b([BC][12])\b/);
    const parsed = [];
    if (ielts) parsed.push({ kind: 'IELTS', value: fmt(ielts[1].replace(',', '.')), tone: 'blue', title: level });
    if (toefl) parsed.push({ kind: 'TOEFL iBT', value: toefl[1], tone: 'blue', title: level });
    if (!parsed.length && cefr) parsed.push({ kind: 'CEFR', value: cefr[1], tone: 'blue', title: level });
    if (parsed.length) return parsed;
    if (language.english_required === true) return [{ kind: t('English', 'İngilizce'), value: t('proof required', 'kanıt gerekli'), tone: 'blue', title: level || t('The programme requires English proficiency; no test minimum is published in the record.', 'Program İngilizce yeterlilik istiyor; kayıtta sınav asgarisi yayımlanmamış.') }];
    return [];
  }

  // ------------------------------------------------------------------- GRE

  const GRE_POLICY = {
    required: { en: 'required', tr: 'zorunlu', tone: 'violet' },
    required_with_waivers: { en: 'required · waivers', tr: 'zorunlu · muafiyet var', tone: 'violet' },
    optional: { en: 'optional', tr: 'isteğe bağlı', tone: 'neutral' },
    optional_not_required: { en: 'optional', tr: 'isteğe bağlı', tone: 'neutral' },
    optional_waived: { en: 'waived', tr: 'şart kaldırıldı', tone: 'neutral' },
    not_required: { en: 'not required', tr: 'gerekli değil', tone: 'teal' },
    not_required_and_not_considered: { en: 'not considered', tr: 'değerlendirilmiyor', tone: 'teal' },
    not_accepted: { en: 'not accepted', tr: 'kabul edilmiyor', tone: 'teal' },
    not_required_but_encouraged: { en: 'encouraged', tr: 'teşvik ediliyor', tone: 'neutral' },
    not_listed_as_required: { en: 'not listed', tr: 'listelenmiyor', tone: 'neutral' },
  };

  function greToken(eligibility) {
    const gre = eligibility.gre;
    const policy = String(gre?.policy || (gre?.required === true ? 'required' : gre?.required === false ? 'not_required' : 'unknown')).toLowerCase();
    const known = GRE_POLICY[policy];
    if (!known) return { kind: 'GRE', value: t('not verified', 'doğrulanmadı'), tone: 'muted', title: t('The record does not verify a GRE policy.', 'Kayıt bir GRE politikası doğrulamıyor.') };
    return { kind: 'GRE', value: known[tr() ? 'tr' : 'en'], tone: known.tone, title: english(gre?.policy_conflict) || '' };
  }

  // --------------------------------------------------- recommendation letters

  const WORD_NUMBERS = { one: 1, two: 2, three: 3, four: 4, bir: 1, iki: 2, üç: 3, dört: 4 };

  function documentList(eligibility) {
    return [eligibility.required_documents, eligibility.application_documents, eligibility.documents_required]
      .flatMap((list) => (Array.isArray(list) ? list : []))
      .map((item) => ({ shown: text(item), en: english(item) }))
      .filter((item) => item.en || item.shown);
  }

  function recommendationToken(eligibility, documents) {
    const count = number(eligibility.recommendation_letter_count ?? eligibility.recommendation_letter_count_minimum ?? eligibility.academic_recommendation_minimum);
    const label = (n) => (n === 1 ? t('recommendation letter', 'referans mektubu') : t('recommendation letters', 'referans mektubu'));
    if (count !== null) return { kind: t('Letters', 'Referans'), value: `${count} ${label(count)}`, tone: 'teal', title: '' };
    const match = documents.map((item) => item.en.toLowerCase()).find((line) => /recommend|reference|referee|referans|tavsiye/.test(line));
    if (match) {
      const numeric = match.match(/\b(\d)\b/);
      const word = Object.keys(WORD_NUMBERS).find((key) => new RegExp(`\\b${key}\\b`, 'i').test(match));
      const n = numeric ? Number(numeric[1]) : (word ? WORD_NUMBERS[word] : null);
      if (n) return { kind: t('Letters', 'Referans'), value: `${n} ${label(n)}`, tone: 'teal', title: match };
      return { kind: t('Letters', 'Referans'), value: t('required', 'gerekli'), tone: 'teal', title: match };
    }
    if (eligibility.recommendation_required === true || eligibility.references_required === true) return { kind: t('Letters', 'Referans'), value: t('required', 'gerekli'), tone: 'teal', title: '' };
    if (eligibility.recommendation_required === false || eligibility.references_required === false) return { kind: t('Letters', 'Referans'), value: t('none required', 'istenmiyor'), tone: 'neutral', title: '' };
    return null;
  }

  // ------------------------------------------------------------------- GPA

  function gpaToken(eligibility) {
    const raw = eligibility.minimum_gpa ?? eligibility.gpa_requirement;
    if (raw === null || raw === undefined || raw === '') return null;
    const scale = number(eligibility.gpa_scale ?? eligibility.minimum_gpa_scale);
    const value = number(raw);
    if (value !== null) {
      if (scale !== null) return { kind: t('Min GPA', 'Min. not'), value: `≥ ${fmt(value)}/${fmt(scale)}`, tone: 'gold', title: english(eligibility.minimum_gpa_context || eligibility.minimum_gpa_policy) };
      if (value > 10) return { kind: t('Min GPA', 'Min. not'), value: `≥ ${fmt(value)}%`, tone: 'gold', title: t('Published as a percentage of the home scale', 'Kendi ölçeğinin yüzdesi olarak yayımlanmış') };
      return { kind: t('Min GPA', 'Min. not'), value: `≥ ${fmt(value)}`, tone: 'gold', title: t('Scale not published in the record', 'Ölçek kayıtta yayımlanmamış') };
    }
    if (typeof raw === 'object' && raw.percentage !== undefined) return { kind: t('Min GPA', 'Min. not'), value: `≥ ${fmt(raw.percentage)}%`, tone: 'gold', title: english(raw.rule) };
    if (typeof raw === 'object' && raw.italian_equivalent_weighted_average) return { kind: t('Min GPA', 'Min. not'), value: String(raw.italian_equivalent_weighted_average), tone: 'gold', title: english(raw.foreign_conversion) };
    const sentence = english(raw);
    if (!sentence) return null;
    if (/no numeric|not (strictly )?specified|not published|none published|yayımlanmam|belirtilmem/i.test(sentence)) {
      return { kind: t('Min GPA', 'Min. not'), value: t('no fixed floor', 'sabit eşik yok'), tone: 'neutral', title: text(raw) };
    }
    const percent = sentence.match(/(\d{2})\s*%/);
    if (percent) return { kind: t('Min GPA', 'Min. not'), value: `≥ ${percent[1]}%`, tone: 'gold', title: text(raw) };
    return { kind: t('Min GPA', 'Min. not'), value: t('rule published', 'kural yayımlı'), tone: 'gold', title: text(raw) };
  }

  // ------------------------------------------------- documents and the rest

  function documentTokens(eligibility, documents) {
    const lines = documents.map((item) => item.en.toLowerCase());
    const has = (pattern) => lines.some((line) => pattern.test(line));
    const tokens = [];
    if (eligibility.motivation_letter_required === true || eligibility.personal_statement_required === true || has(/motivation|statement of purpose|personal statement|amaç|motivasyon/)) {
      tokens.push({ kind: t('Statement', 'Beyan'), value: t('motivation / SOP', 'motivasyon / SOP'), tone: 'neutral', title: '' });
    }
    if (eligibility.cv_required === true || has(/\bcv\b|curriculum vitae|r[ée]sum[ée]|özgeçmiş/)) {
      tokens.push({ kind: 'CV', value: t('required', 'gerekli'), tone: 'neutral', title: '' });
    }
    if (eligibility.portfolio_required === true || has(/portfolio/)) tokens.push({ kind: t('Portfolio', 'Portfolyo'), value: t('required', 'gerekli'), tone: 'neutral', title: '' });
    if (eligibility.writing_sample_required === true) tokens.push({ kind: t('Writing sample', 'Yazı örneği'), value: t('required', 'gerekli'), tone: 'neutral', title: '' });
    return tokens;
  }

  function interviewToken(eligibility) {
    const policy = String(eligibility.interview_policy || '').toLowerCase();
    if (eligibility.interview_required === true) return { kind: t('Interview', 'Mülakat'), value: t('required', 'zorunlu'), tone: 'violet', title: '' };
    if (eligibility.interview_required === 'conditional' || /conditional/.test(String(eligibility.interview_required)) || /optional|may_be|discretion/.test(policy) || eligibility.interview_possible === true) {
      return { kind: t('Interview', 'Mülakat'), value: t('possible', 'olabilir'), tone: 'neutral', title: english(eligibility.interview_policy) };
    }
    if (eligibility.interview_required === false) return { kind: t('Interview', 'Mülakat'), value: t('none', 'yok'), tone: 'neutral', title: '' };
    return null;
  }

  function testToken(eligibility) {
    if (eligibility.test_required === true || eligibility.entrance_exam) return { kind: t('Entrance test', 'Giriş sınavı'), value: t('required', 'zorunlu'), tone: 'violet', title: english(eligibility.test_policy || eligibility.entrance_exam) };
    if (typeof eligibility.test_required === 'string') return { kind: t('Entrance test', 'Giriş sınavı'), value: t('conditional', 'koşullu'), tone: 'neutral', title: english(eligibility.test_required) };
    return null;
  }

  function feeToken(record) {
    const helper = window.uniApplicationFee;
    if (!helper) return null;
    const fee = helper.read(record);
    if (!fee) return null;
    if (fee.status === 'published') return { kind: t('Fee', 'Ücret'), value: helper.headline(fee).split(' · ')[0], tone: 'gold', title: helper.qualifiers(fee).join(' · ') };
    if (fee.status === 'no_fee' || fee.status === 'not_published') return { kind: t('Fee', 'Ücret'), value: t('none', 'yok'), tone: 'teal', title: helper.headline(fee) };
    return null;
  }

  function eligibilityToken(eligibility) {
    if (eligibility.eligible_for_non_eu === false) return { kind: t('Non-EU', 'AB dışı'), value: t('not open', 'kapalı'), tone: 'rose', title: t('The record marks the programme as not open to non-EU applicants.', 'Kayıt programı AB dışı adaylara kapalı olarak işaretliyor.') };
    return null;
  }

  // ---------------------------------------------------------------- render

  function tokenHtml(token) {
    return `<li class="req-token req-token--${esc(token.tone)}"${token.title ? ` title="${esc(token.title)}"` : ''}><span class="req-token__kind">${esc(token.kind)}</span><strong>${esc(token.value)}</strong></li>`;
  }

  function panel(record) {
    if (!record || typeof record !== 'object') return '';
    const eligibility = record.eligibility_profile || {};
    const language = record.language_profile || {};
    const documents = documentList(eligibility);

    const tokens = [
      ...englishTokens(language),
      greToken(eligibility),
      recommendationToken(eligibility, documents),
      gpaToken(eligibility),
      ...documentTokens(eligibility, documents),
      interviewToken(eligibility),
      testToken(eligibility),
      feeToken(record),
      eligibilityToken(eligibility),
    ].filter(Boolean);

    if (documents.length) tokens.push({ kind: t('Documents', 'Belge'), value: String(documents.length), tone: 'neutral', title: documents.map((item) => item.shown).join(' · ') });
    if (!tokens.length) return '';

    return `
      <section class="drawer-section requirement-summary" aria-label="${esc(t('Requirements at a glance', 'Bir bakışta gereklilikler'))}">
        <div class="requirement-summary__head">
          <span class="requirement-summary__eyebrow">${esc(t('At a glance', 'Bir bakışta'))}</span>
          <strong>${esc(t('What this application asks for', 'Bu başvuru ne istiyor'))}</strong>
        </div>
        <ul class="req-tokens">${tokens.map(tokenHtml).join('')}</ul>
        <small class="requirement-summary__note">${esc(t('Only values published on the official pages appear here; a fact the catalogue has not verified is marked, never assumed.', 'Burada yalnızca resmî sayfalarda yayımlanan değerler görünür; doğrulanmamış bir bilgi varsayılmaz, işaretlenir.'))}</small>
      </section>`;
  }

  window.uniRequirementSummary = { panel, englishTokens, greToken, recommendationToken, gpaToken };
})();
