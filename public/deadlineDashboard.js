(function () {
  'use strict';

  const DAY_MS = 24 * 60 * 60 * 1000;
  const AUTO_REFRESH_MS = 15 * 60 * 1000;
  const REFRESH_CHECK_MS = 60 * 1000;
  const TARGET_INTAKE_YEAR = 2027;
  const VALID_SOURCE_STATUSES = new Set(['ok', 'redirects', 'pdf', 'requires_js']);
  const CLOSED_WORDS = /closed|passed|expired|historical|cancelled|canceled|deadline_passed|kapand|geçti/i;
  const GENERIC_EVENT_LABELS = /^(application|non-eu|international|final|regular|document|scholarship|funding|visa|enrolment|enrollment|housing).*(deadline|close)$/i;

  const copy = {
    en: {
      urgent: 'Urgent', soon: 'Approaching', later: 'Later', verify: 'Verify date', closed: 'Closed cycle', all: 'All', upcoming: 'All upcoming',
      urgentHint: '30 days or less', soonHint: '31–90 days', laterHint: 'More than 90 days', verifyHint: 'No exact future date',
      remainingToday: 'Due today', remainingTomorrow: '1 day left', remainingDays: '{count} days left', overdueToday: 'Closed today', overdueDays: 'Closed {count} days ago',
      exactDateMissing: 'Exact cycle date is not published', noFuture: 'No exact future application date has been verified',
      deadlineUnknown: 'Deadline needs verification', documents: 'Required documents', documentsUnknown: 'Official required-document list is not yet verified.',
      documentsCount: '{count} documents', timeline: 'Dates and milestones', expand: 'Show all dates and documents', collapse: 'Hide details',
      applicationSource: 'Official application source', documentSource: 'Document source', programDetails: 'Open program details',
      verified: 'Last verified', confidence: 'Deadline confidence', showing: 'Showing {shown} of {total} programs', noMatches: 'No programs match these calendar filters.',
      noFavorites: 'You have no matching favorite programs.', urgentLauncher: '{count} urgent · {upcoming} upcoming', noUrgentLauncher: '{count} upcoming deadline(s)',
      sourceUnavailable: 'Official link not recorded', current: 'Upcoming', past: 'Past / closed', undated: 'Date to verify', sourceHigh: 'High', sourceMedium: 'Medium', sourceLow: 'Low', sourceUnknown: 'Unknown',
      markedClosed: 'Marked closed in the source',
      applicationDeadline: 'Application deadline', nonEuDeadline: 'Non-EU deadline', finalDeadline: 'Final application deadline', documentDeadline: 'Document completion',
      englishDeadline: 'English-score deadline', recommendationDeadline: 'Recommendation deadline', feeWaiverDeadline: 'Fee-waiver deadline', scholarshipDeadline: 'Scholarship deadline',
      fundingDeadline: 'Funding priority', visaDeadline: 'Visa / pre-enrolment milestone', enrolmentDeadline: 'Enrolment deadline', housingDeadline: 'Housing deadline', applicationRound: 'Application round', otherDeadline: 'Application milestone',
      currentFilters: '2027 intake watch · exact dates are never inferred', openNewTab: 'opens in a new tab',
      autoUpdated: 'Auto-updated at {time} · every 15 min', syncing: 'Checking for updates…', syncFailed: 'Update check failed · cached data shown',
      officialWording: 'Official wording', targetCycle: '2027 intake', cyclePublished: '2027 cycle published', cycleAnnual: 'Standing annual rule', cycleAwaiting: '2027 cycle awaiting publication', cycleUnknown: '2027 date not verified',
      previousCycle: 'Previous cycle · reference only', lastPublishedDate: 'Last published application date', referenceWarning: '{cycle} reference · not a 2027 deadline', openOfficialStep: 'Open official step', applicationLinkHint: 'Deadline and application instructions', documentLinkHint: 'Official checklist and eligibility evidence',
      runwayEmpty: 'No exact target-cycle date has been verified yet', runwayEmptyHint: 'Programs awaiting publication remain visible below with their previous-cycle reference.', runwayEvents: '{count} milestone(s)', admittedOnly: 'Application window closed · remaining dates apply to admitted students'
    },
    tr: {
      urgent: 'Acil', soon: 'Yaklaşıyor', later: 'Daha sonra', verify: 'Tarihi doğrula', closed: 'Kapanan dönem', all: 'Tümü', upcoming: 'Tüm yaklaşanlar',
      urgentHint: '30 gün veya daha az', soonHint: '31–90 gün', laterHint: '90 günden fazla', verifyHint: 'Kesin gelecek tarih yok',
      remainingToday: 'Son gün bugün', remainingTomorrow: '1 gün kaldı', remainingDays: '{count} gün kaldı', overdueToday: 'Bugün kapandı', overdueDays: '{count} gün önce kapandı',
      exactDateMissing: 'İlgili dönem için kesin tarih yayımlanmamış', noFuture: 'Doğrulanmış kesin bir gelecek başvuru tarihi yok',
      deadlineUnknown: 'Son tarih doğrulanmalı', documents: 'İstenen belgeler', documentsUnknown: 'Resmî istenen belge listesi henüz doğrulanmamış.',
      documentsCount: '{count} belge', timeline: 'Tarihler ve aşamalar', expand: 'Tüm tarihleri ve belgeleri göster', collapse: 'Detayları gizle',
      applicationSource: 'Resmî başvuru kaynağı', documentSource: 'Belge kaynağı', programDetails: 'Program detayını aç',
      verified: 'Son doğrulama', confidence: 'Deadline güveni', showing: '{total} programdan {shown} tanesi gösteriliyor', noMatches: 'Bu takvim filtreleriyle eşleşen program yok.',
      noFavorites: 'Eşleşen favori programın yok.', urgentLauncher: '{count} acil · {upcoming} yaklaşan', noUrgentLauncher: '{count} yaklaşan tarih',
      sourceUnavailable: 'Resmî bağlantı kaydedilmemiş', current: 'Yaklaşan', past: 'Geçmiş / kapalı', undated: 'Tarih doğrulanmalı', sourceHigh: 'Yüksek', sourceMedium: 'Orta', sourceLow: 'Düşük', sourceUnknown: 'Bilinmiyor',
      markedClosed: 'Kaynakta kapalı olarak işaretli',
      applicationDeadline: 'Başvuru son tarihi', nonEuDeadline: 'AB dışı son tarih', finalDeadline: 'Nihai başvuru tarihi', documentDeadline: 'Belge tamamlama',
      englishDeadline: 'İngilizce puanı tarihi', recommendationDeadline: 'Referans mektubu tarihi', feeWaiverDeadline: 'Ücret muafiyeti tarihi', scholarshipDeadline: 'Burs son tarihi',
      fundingDeadline: 'Fonlama öncelik tarihi', visaDeadline: 'Vize / ön kayıt aşaması', enrolmentDeadline: 'Kayıt son tarihi', housingDeadline: 'Konut son tarihi', applicationRound: 'Başvuru turu', otherDeadline: 'Başvuru aşaması',
      currentFilters: '2027 dönemi takibi · kesin tarihler tahmin edilmez', openNewTab: 'yeni sekmede açılır',
      autoUpdated: 'Otomatik güncellendi: {time} · 15 dakikada bir', syncing: 'Güncellemeler kontrol ediliyor…', syncFailed: 'Güncelleme kontrolü başarısız · kayıtlı veri gösteriliyor',
      officialWording: 'Resmî ifade', targetCycle: '2027 dönemi', cyclePublished: '2027 dönemi yayımlandı', cycleAnnual: 'Her yıl geçerli resmî kural', cycleAwaiting: '2027 dönemi henüz yayımlanmadı', cycleUnknown: '2027 tarihi doğrulanmadı',
      previousCycle: 'Önceki dönem · yalnızca referans', lastPublishedDate: 'Son yayımlanan başvuru tarihi', referenceWarning: '{cycle} referansı · 2027 son tarihi değildir', openOfficialStep: 'Resmî adıma git', applicationLinkHint: 'Son tarih ve başvuru yönergeleri', documentLinkHint: 'Resmî belge listesi ve uygunluk kanıtları',
      runwayEmpty: 'Hedef dönem için kesin bir tarih henüz doğrulanmadı', runwayEmptyHint: 'Yayın bekleyen programlar, önceki dönem referanslarıyla aşağıda görünmeye devam eder.', runwayEvents: '{count} aşama', admittedOnly: 'Başvuru dönemi kapandı · kalan tarihler kabul edilmiş öğrenciler için'
    }
  };

  const state = {
    records: [],
    models: [],
    filter: 'all',
    query: '',
    favoritesOnly: false,
    lastFocus: null,
    lastSyncedAt: null,
    syncing: false,
    syncFailed: false
  };

  const elements = {};

  function lang() {
    return window.currentLanguage === 'tr' ? 'tr' : 'en';
  }

  function tr(key, replacements = {}) {
    let value = copy[lang()][key] || copy.en[key] || key;
    Object.entries(replacements).forEach(([name, replacement]) => {
      value = value.replace(`{${name}}`, String(replacement));
    });
    return value;
  }

  function escapeHtml(value) {
    return String(value ?? '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  function localized(value) {
    if (value === null || value === undefined) return '';
    if (typeof value === 'string' || typeof value === 'number') return String(value).trim();
    if (Array.isArray(value)) return value.map(localized).filter(Boolean).join(', ');
    if (typeof value === 'object') {
      const preferred = value[lang()] ?? value.en ?? value.tr ?? value.name ?? value.label ?? value.title ?? value.document ?? value.requirement;
      return localized(preferred);
    }
    return '';
  }

  function safeUrl(value) {
    try {
      const url = new URL(String(value || ''));
      return ['http:', 'https:'].includes(url.protocol) ? url.href : '';
    } catch {
      return '';
    }
  }

  function humanize(value) {
    const text = localized(value).replace(/[_-]+/g, ' ').replace(/\s+/g, ' ').trim();
    return text ? text.charAt(0).toUpperCase() + text.slice(1) : tr('otherDeadline');
  }

  function readableToken(value) {
    const text = localized(value);
    return /^[a-z0-9]+(?:[_-][a-z0-9]+)+$/i.test(text) ? humanize(text) : text;
  }

  function datePartsFromIso(value) {
    const text = localized(value);
    const matches = [...text.matchAll(/\b(20\d{2})-(\d{2})-(\d{2})(?:T\d{2}:\d{2}(?::\d{2})?(?:Z|[+-]\d{2}:?\d{2})?)?/g)];
    const seen = new Set();
    return matches.map(match => {
      const year = Number(match[1]);
      const month = Number(match[2]);
      const day = Number(match[3]);
      const date = new Date(year, month - 1, day, 12, 0, 0);
      if (date.getFullYear() !== year || date.getMonth() !== month - 1 || date.getDate() !== day) return null;
      const key = `${match[1]}-${match[2]}-${match[3]}`;
      if (seen.has(key)) return null;
      seen.add(key);
      return { key, year, month, day, date, rawMatch: match[0] };
    }).filter(Boolean);
  }

  function todayUtcDay() {
    const now = new Date();
    return Date.UTC(now.getFullYear(), now.getMonth(), now.getDate());
  }

  function daysFromToday(datePart) {
    return Math.round((Date.UTC(datePart.year, datePart.month - 1, datePart.day) - todayUtcDay()) / DAY_MS);
  }

  function cycleInfo(record, events) {
    const timeline = record.application_timeline_profile || {};
    const academicYear = localized(timeline.target_academic_year || timeline.academic_year);
    const intake = localized(timeline.intake_terms || timeline.intake || timeline.start_term);
    const searchable = `${academicYear} ${intake} ${JSON.stringify(timeline)}`.toLowerCase();
    const explicitAwaiting = /not[_ -]published|awaiting[_ -]publication|next[_ -]cycle[_ -]not[_ -]published/.test(String(timeline.next_cycle_status || '').toLowerCase());
    const explicitTarget = /2027\s*\/\s*2028|2027\s*\/\s*28|2027 entry|fall 2027|autumn 2027|september 2027|spring 2027|summer 2027|february 2027/.test(searchable);
    const exactTargetApplication = events.some(event => event.exact && event.datePart.year >= TARGET_INTAKE_YEAR && ['application', 'documents', 'scholarship'].includes(event.kind));
    const annual = /recurring|standing annual|annual application|annual deadline|current application rules|every year|yearly/.test(searchable);

    if (!explicitAwaiting && (explicitTarget || exactTargetApplication)) {
      return { key: 'published', label: tr('cyclePublished'), academicYear: academicYear || tr('targetCycle'), targetReady: true };
    }
    if (!explicitAwaiting && annual) {
      return { key: 'annual', label: tr('cycleAnnual'), academicYear: academicYear || tr('targetCycle'), targetReady: true };
    }
    if (explicitAwaiting || academicYear || events.length) {
      return { key: 'awaiting', label: tr('cycleAwaiting'), academicYear: academicYear || tr('previousCycle'), targetReady: false };
    }
    return { key: 'unknown', label: tr('cycleUnknown'), academicYear: tr('targetCycle'), targetReady: false };
  }

  function inferKind(text) {
    const value = String(text || '').toLowerCase();
    if (/scholar|fund|fellow|burs/.test(value)) return 'scholarship';
    if (/housing|accommodation|konut|barın/.test(value)) return 'housing';
    if (/visa|universitaly|pre.?enrol|pre.?enroll|vize|ön kayıt/.test(value)) return 'visa';
    if (/enrol|enroll|registration|matriculat|kayıt/.test(value)) return 'enrolment';
    if (/document|transcript|english|language|recommend|reference|score|belge|referans/.test(value)) return 'documents';
    return 'application';
  }

  function appliesToTargetApplicant(scope) {
    const value = localized(scope).toLowerCase().replace(/[\s-]+/g, '_');
    if (!value) return true;
    if (/non_?eu|international|overseas|foreign|third_?country|visa|all|eligible/.test(value)) return true;
    if (/(^|_)(home|uk|domestic)($|_)/.test(value) || /(^|_)eu(_|$)/.test(value)) return false;
    return true;
  }

  function isActionableDeadlineEvent(event) {
    const label = localized(event?.label || event?.title || event?.event || event?.name).toLowerCase().replace(/[_-]+/g, ' ');
    if (!label) return false;
    const isOpeningOrOutcome = /\b(open|opened|opening|start|starts|begin|begins|result|results|decision|publication|classes|orientation|arrival|check in)\b/.test(label);
    const hasDeadlineSignal = /deadline|close|closing|due|selection|registration|enrol|enroll|application|visa|document|fee|deposit|scholar|fund|housing|accommodation|offer reply/.test(label);
    return hasDeadlineSignal && (!isOpeningOrOutcome || /deadline|close|closing|due|selection|registration/.test(label));
  }

  // An event can be a real milestone worth listing and still be the wrong thing
  // to headline.  A deposit due date, a CAS issue date, an enrolment window or
  // the first day of teaching only binds somebody who already holds an offer -
  // showing one as the countdown made closed programmes look open.
  const ADMITTED_ONLY_EVENT = /offer holder|existing offer|admitted|enrolled|matriculated/i;
  // Deliberately narrow: only steps that cannot exist before an offer.  A
  // scholarship or funding deadline stays eligible, because an applicant does
  // act on it - the defect was never that funding dates showed, it was that
  // deposits, enrolment windows and the first day of term did.
  const NOT_AN_APPLICATION_STEP = /deposit|conditions deadline|\bcas\b|atas|visa(?! required)|pre ?enrol|enrol|enroll|matricul|immatricul|commence|begin|start|teaching|induction|orientation|arrival|housing|accommodation|residence|deferral|verification|verify|offer reply|offer acceptance|opened|opens/i;
  const APPLICATION_STEP = /applica|apply|admission|call for|intake|round|selection|competition|scholarship|funding|bursary|fellowship|fee waiver/i;

  function isNewApplicantEvent(event) {
    const text = `${event?.label || ''} ${event?.statusText || ''} ${event?.applicantScope || ''}`
      .replace(/[_-]+/g, ' ');
    if (!text.trim()) return false;
    if (ADMITTED_ONLY_EVENT.test(text)) return false;
    if (!APPLICATION_STEP.test(text)) return false;
    return !NOT_AN_APPLICATION_STEP.test(text);
  }

  function addEvent(target, config) {
    const raw = localized(config.value);
    if (!raw) return;
    const dates = datePartsFromIso(config.value);
    const label = localized(config.label) || tr('otherDeadline');
    const base = {
      label,
      raw,
      kind: config.kind || inferKind(`${label} ${raw}`),
      statusText: localized(config.status),
      priority: Number(config.priority) || 0,
      sourceIds: Array.isArray(config.sourceIds) ? config.sourceIds : [],
      applicantScope: localized(config.applicantScope),
      sourceUrl: safeUrl(config.sourceUrl)
    };
    if (dates.length === 0) {
      target.push({ ...base, exact: false, datePart: null, days: null, closed: CLOSED_WORDS.test(`${base.statusText} ${raw}`) });
      return;
    }
    dates.forEach(datePart => {
      const days = daysFromToday(datePart);
      target.push({
        ...base,
        exact: true,
        datePart,
        days,
        closed: days < 0 || CLOSED_WORDS.test(`${base.statusText} ${raw}`)
      });
    });
  }

  function collectDeadlineEvents(record) {
    const timeline = record.application_timeline_profile || {};
    const events = [];
    const scalarFields = [
      ['non_eu_deadline', 'nonEuDeadline', 'application'],
      ['deadline_non_eu', 'nonEuDeadline', 'application'],
      ['application_deadline', 'applicationDeadline', 'application'],
      ['final_application_deadline', 'finalDeadline', 'application'],
      ['document_completion_deadline', 'documentDeadline', 'documents'],
      ['english_score_deadline_if_required', 'englishDeadline', 'documents'],
      ['recommendation_deadline', 'recommendationDeadline', 'documents'],
      ['fee_waiver_deadline', 'feeWaiverDeadline', 'documents'],
      ['scholarship_deadline', 'scholarshipDeadline', 'scholarship'],
      ['funding_priority_deadline', 'fundingDeadline', 'scholarship'],
      ['visa_sensitive_deadline', 'visaDeadline', 'visa'],
      ['universitaly_deadline', 'visaDeadline', 'visa'],
      ['pre_enrolment_deadline', 'visaDeadline', 'visa'],
      ['pre_enrollment_deadline', 'visaDeadline', 'visa'],
      ['enrollment_deadline', 'enrolmentDeadline', 'enrolment'],
      ['enrolment_deadline', 'enrolmentDeadline', 'enrolment'],
      ['offer_reply_deadline', 'enrolmentDeadline', 'enrolment'],
      ['housing_deadline', 'housingDeadline', 'housing']
    ];

    scalarFields.forEach(([field, labelKey, kind]) => {
      addEvent(events, { value: timeline[field], label: tr(labelKey), kind, priority: 1 });
    });

    addEvent(events, {
      value: record.eligibility_profile?.application_fee_waiver_request_deadline,
      label: tr('feeWaiverDeadline'), kind: 'documents', priority: 1
    });

    (Array.isArray(timeline.deadline_events) ? timeline.deadline_events : []).forEach(event => {
      if (!event || typeof event !== 'object') return;
      if (!appliesToTargetApplicant(event.applicant_scope) || !isActionableDeadlineEvent(event)) return;
      const label = readableToken(event.label || event.title || event.event || event.name);
      addEvent(events, {
        value: event.date || event.deadline,
        label: label || tr('otherDeadline'),
        kind: inferKind(label),
        status: event.status_as_of_last_checked || event.status || event.date_status,
        sourceIds: event.source_ids,
        sourceUrl: event.source_url,
        applicantScope: event.applicant_scope,
        priority: 4
      });
    });

    (Array.isArray(timeline.application_rounds) ? timeline.application_rounds : []).forEach((round, index) => {
      if (typeof round === 'string') {
        addEvent(events, { value: round, label: `${tr('applicationRound')} ${index + 1}`, kind: 'application', priority: 2 });
        return;
      }
      if (!round || typeof round !== 'object') return;
      if (!appliesToTargetApplicant(round.applicant_scope)) return;
      const roundName = localized(round.round || round.intake || round.name || round.label);
      addEvent(events, {
        value: round.international_deadline || round.non_eu_deadline || round.deadline,
        label: roundName ? `${tr('applicationRound')} · ${roundName}` : `${tr('applicationRound')} ${index + 1}`,
        kind: 'application', status: round.status, sourceUrl: round.source_url, priority: 3
      });
    });

    const scholarship = record.scholarship_profile || {};
    ['scholarship_deadline', 'funding_deadline', 'application_deadline', 'funding_priority_deadline'].forEach(field => {
      addEvent(events, { value: scholarship[field], label: field.includes('priority') ? tr('fundingDeadline') : tr('scholarshipDeadline'), kind: 'scholarship', priority: 2 });
    });
    (Array.isArray(scholarship.opportunities) ? scholarship.opportunities : []).forEach(opportunity => {
      if (!opportunity || typeof opportunity !== 'object') return;
      const name = localized(opportunity.name);
      addEvent(events, { value: opportunity.deadline || opportunity.application_deadline, label: name || tr('scholarshipDeadline'), kind: 'scholarship', status: opportunity.status, priority: 3 });
    });

    const living = record.living_profile || {};
    [living.housing_deadline, living.application_deadline, living.housing_guarantee?.application_deadline, living.housing_guarantee?.offer_acceptance_deadline, living.housing_guarantee?.latest_published_housing_deadline]
      .forEach(value => addEvent(events, { value, label: tr('housingDeadline'), kind: 'housing', priority: 2 }));

    const bySignature = new Map();
    events.forEach(event => {
      const signature = event.exact
        ? `${event.datePart.key}|${event.kind}`
        : `undated|${event.kind}|${event.raw.toLowerCase()}`;
      const existing = bySignature.get(signature);
      if (!existing || event.priority > existing.priority || (GENERIC_EVENT_LABELS.test(existing.label) && !GENERIC_EVENT_LABELS.test(event.label))) {
        bySignature.set(signature, event);
      }
    });
    return [...bySignature.values()].sort((left, right) => {
      if (left.exact !== right.exact) return left.exact ? -1 : 1;
      if (left.exact && right.exact) return left.days - right.days;
      return left.label.localeCompare(right.label);
    });
  }

  function documentItems(record) {
    const eligibility = record.eligibility_profile || {};
    const confidence = record.source_profile?.field_confidence || {};
    const verifiedFields = new Set((record.data_quality?.verified_fields || []).map(value => String(value).toLowerCase()));
    const confidenceValue = String(confidence.required_documents || confidence.documents || confidence.admission || '').toLowerCase();
    const documentsVerified = ['high', 'medium'].includes(confidenceValue)
      || ['required_documents', 'documents', 'admission'].some(field => verifiedFields.has(field));
    if (!documentsVerified) return [];
    const candidates = [eligibility.required_documents, eligibility.application_documents, eligibility.documents_required];
    const output = [];
    candidates.forEach(items => {
      (Array.isArray(items) ? items : []).forEach(item => {
        const text = readableToken(item);
        if (text && !output.some(existing => existing.toLowerCase() === text.toLowerCase())) output.push(text);
      });
    });
    return output;
  }

  function relevantSource(record, type) {
    const sourceProfile = record.source_profile || {};
    const logs = Array.isArray(sourceProfile.source_log) ? sourceProfile.source_log : [];
    const wanted = type === 'documents' ? /admission|document|required|eligib/i : /deadline|timeline|application|admission/i;
    const scored = logs.map(source => {
      if (!source || typeof source !== 'object') return null;
      const url = safeUrl(source.url);
      if (!url) return null;
      const status = String(source.access_status || '').toLowerCase();
      if (status && !VALID_SOURCE_STATUSES.has(status)) return null;
      const fields = Array.isArray(source.relevant_fields) ? source.relevant_fields.join(' ') : localized(source.relevant_fields);
      let score = wanted.test(fields) ? 5 : 0;
      if (/official/.test(String(source.source_type || '').toLowerCase())) score += 2;
      if (String(source.confidence || '').toLowerCase() === 'high') score += 1;
      return { url, title: localized(source.title) || url, score };
    }).filter(Boolean).sort((a, b) => b.score - a.score);
    return scored[0]?.score > 0 ? scored[0] : null;
  }

  function fieldConfidence(record) {
    const confidence = record.source_profile?.field_confidence || {};
    const raw = String(confidence.deadlines || confidence.deadline || confidence.application_timeline || confidence.admission || 'unknown').toLowerCase();
    return ['high', 'medium', 'low'].includes(raw) ? raw : 'unknown';
  }

  function programModel(record, index) {
    const normalized = window.uniDataAdapter?.normalizeUniversityRecord(record) || {};
    const collectedEvents = collectDeadlineEvents(record);
    const cycle = cycleInfo(record, collectedEvents);
    const events = collectedEvents.map(event => ({ ...event, referenceOnly: !cycle.targetReady }));
    const upcomingEvents = cycle.targetReady
      ? events.filter(event => event.exact && !event.closed && event.days >= 0)
      : [];
    // The headline date has to be one a new applicant can still act on; the
    // remaining milestones stay in upcomingEvents for the timeline and count.
    const applicantEvents = upcomingEvents.filter(isNewApplicantEvent);
    const next = applicantEvents[0] || null;
    const admittedOnlyAhead = !next && upcomingEvents.length > 0;
    const referenceDeadline = !cycle.targetReady
      ? events
        .filter(event => event.exact && event.kind === 'application')
        .sort((left, right) => right.datePart.date - left.datePart.date)[0] || null
      : null;
    let status = 'missing';
    if (next) status = next.days <= 30 ? 'urgent' : next.days <= 90 ? 'soon' : 'later';
    else if (!cycle.targetReady || events.some(event => !event.exact && !event.closed)) status = 'undated';
    else if (events.length) status = 'closed';

    const cleanCountry = String(normalized.country || record.country || '').replace(/^[^a-zA-ZçğıöşüÇĞİÖŞÜ]+/, '').trim();
    const visual = typeof window.uniCountryVisual === 'function'
      ? window.uniCountryVisual(cleanCountry)
      : { key: 'global', code: '', accent: '#6f85a2', rgb: '111, 133, 162' };
    return {
      index,
      record,
      id: normalized.id || record.id || `record-${index}`,
      university: localized(normalized.universityName) || localized(record.university) || tr('deadlineUnknown'),
      program: localized(normalized.programName) || localized(record.program_name) || '—',
      country: window.getCountryName ? window.getCountryName(cleanCountry) : cleanCountry,
      countryRaw: cleanCountry,
      countryVisual: visual,
      city: localized(normalized.city),
      degree: localized(normalized.degree),
      events,
      upcomingEvents,
      applicantEvents,
      admittedOnlyAhead,
      next,
      status,
      cycle,
      referenceDeadline,
      referenceAcademicYear: localized(record.application_timeline_profile?.academic_year) || tr('previousCycle'),
      documents: documentItems(record),
      deadlineSource: relevantSource(record, 'deadline'),
      documentSource: relevantSource(record, 'documents'),
      confidence: fieldConfidence(record),
      lastVerified: localized(record.source_profile?.last_verified || record.updated_at || normalized.lastVerified)
    };
  }

  function rebuildModels() {
    state.models = state.records.map(programModel).sort((left, right) => {
      const order = { urgent: 0, soon: 1, later: 2, undated: 3, missing: 4, closed: 5 };
      const statusDifference = order[left.status] - order[right.status];
      if (statusDifference) return statusDifference;
      if (left.next && right.next && left.next.days !== right.next.days) return left.next.days - right.next.days;
      return left.university.localeCompare(right.university);
    });
  }

  function formatDate(datePart) {
    if (!datePart) return '—';
    return new Intl.DateTimeFormat(lang() === 'tr' ? 'tr-TR' : 'en-GB', {
      weekday: 'long', day: 'numeric', month: 'long', year: 'numeric'
    }).format(datePart.date);
  }

  function formatStoredDate(value) {
    const [datePart] = datePartsFromIso(value);
    return datePart ? formatDate(datePart) : localized(value) || '—';
  }

  function eventDisplayLabel(event) {
    const source = humanize(event?.label || tr('otherDeadline'));
    const normalized = source.toLocaleLowerCase('en-US').replace(/[–—]/g, '-').replace(/\s+/g, ' ').trim();
    if (lang() !== 'tr') {
      return source
        .replace(/\bProgramme application deadline\b/i, 'Programme application deadline')
        .replace(/\bProgram application deadline\b/i, 'Program application deadline');
    }

    const exactLabels = [
      [/^(programme|program) application deadline$/, 'Program başvurusunun son günü'],
      [/^regular application deadline$/, 'Normal başvuru döneminin son günü'],
      [/^final application deadline$/, 'Nihai başvuru günü'],
      [/^application deadline$/, 'Başvurunun son günü'],
      [/^non eu deadline$/, 'AB dışı adaylar için son başvuru günü'],
      [/^international application deadline$/, 'Uluslararası adaylar için son başvuru günü'],
      [/^document (submission|completion) deadline$/, 'Belgeleri tamamlama günü'],
      [/^english score deadline$/, 'İngilizce puanını iletme günü'],
      [/^recommendation deadline$/, 'Referans mektubunu iletme günü'],
      [/^fee waiver deadline$/, 'Başvuru ücreti muafiyetinin son günü'],
      [/^scholarship deadline$/, 'Burs başvurusunun son günü'],
      [/^funding priority$/, 'Fonlama önceliği için son gün'],
      [/^visa \/ pre enrolment milestone$/, 'Vize / ön kayıt aşaması'],
      [/^enrolment deadline$/, 'Kesin kayıt günü'],
      [/^housing deadline$/, 'Konut başvurusunun son günü']
    ];
    const exact = exactLabels.find(([pattern]) => pattern.test(normalized));
    if (exact) return exact[1];

    return source
      .replace(/\bprogramme application deadline\b/gi, 'program başvurusunun son günü')
      .replace(/\bprogram application deadline\b/gi, 'program başvurusunun son günü')
      .replace(/\bapplication deadline\b/gi, 'başvurunun son günü')
      .replace(/\bsecond level selection\b/gi, 'ikinci aşama seçimi')
      .replace(/\bfirst level selection\b/gi, 'birinci aşama seçimi')
      .replace(/\bselection deadline\b/gi, 'seçim sürecinin son günü')
      .replace(/\bfee waiver deadline\b/gi, 'ücret muafiyetinin son günü')
      .replace(/\bscholarship deadline\b/gi, 'burs başvurusunun son günü')
      .replace(/\bhousing deadline\b/gi, 'konut başvurusunun son günü')
      .replace(/\benrolment deadline\b/gi, 'kayıt günü')
      .replace(/\benrollment deadline\b/gi, 'kayıt günü');
  }

  function eventOfficialNote(event) {
    const raw = localized(event?.raw);
    if (!raw) return '';
    const withoutDates = raw
      .replace(/\b20\d{2}-\d{2}-\d{2}(?:T\d{2}:\d{2}(?::\d{2})?(?:Z|[+-]\d{2}:?\d{2})?)?/g, '')
      .replace(/^[\s·:;,.()\[\]-]+|[\s·:;,.()\[\]-]+$/g, '')
      .trim();
    if (!withoutDates || !/[\p{L}]/u.test(withoutDates)) return '';
    return `${tr('officialWording')}: ${raw}`;
  }

  function remainingLabel(days, closed = false) {
    if (closed && days > 0) return tr('markedClosed');
    if (closed && days === 0) return tr('overdueToday');
    if (closed && days < 0) return tr('overdueDays', { count: Math.abs(days) });
    if (days === 0) return tr('remainingToday');
    if (days === 1) return tr('remainingTomorrow');
    if (days > 1) return tr('remainingDays', { count: days });
    return tr('overdueDays', { count: Math.abs(days) });
  }

  function statusLabel(status) {
    return { urgent: tr('urgent'), soon: tr('soon'), later: tr('later'), undated: tr('verify'), missing: tr('verify'), closed: tr('closed') }[status];
  }

  function confidenceLabel(value) {
    return tr(`source${value.charAt(0).toUpperCase()}${value.slice(1)}`);
  }

  function renderSummary() {
    const counts = state.models.reduce((result, model) => {
      result[model.status] += 1;
      return result;
    }, { urgent: 0, soon: 0, later: 0, undated: 0, missing: 0, closed: 0 });
    const cards = [
      ['urgent', '!', tr('urgent'), counts.urgent, tr('urgentHint')],
      ['soon', '◷', tr('soon'), counts.soon, tr('soonHint')],
      ['later', '↗', tr('later'), counts.later, tr('laterHint')],
      ['undated', '?', tr('verify'), counts.undated + counts.missing, tr('verifyHint')]
    ];
    elements.summary.innerHTML = cards.map(([filter, icon, label, count, hint]) => `
      <button class="deadline-summary-card deadline-summary-card--${filter}${state.filter === filter ? ' is-active' : ''}" type="button" data-deadline-filter="${filter}">
        <i aria-hidden="true">${escapeHtml(icon)}</i><span>${escapeHtml(label)}</span><strong>${count}</strong><small>${escapeHtml(hint)}</small>
      </button>`).join('');

    const upcoming = counts.urgent + counts.soon + counts.later;
    elements.badge.textContent = String(counts.urgent);
    elements.badge.classList.toggle('is-empty', counts.urgent === 0);
    elements.badge.setAttribute('aria-label', `${counts.urgent} ${tr('urgent').toLowerCase()}`);
    elements.launcherSummary.textContent = counts.urgent
      ? tr('urgentLauncher', { count: counts.urgent, upcoming })
      : tr('noUrgentLauncher', { count: upcoming });
  }

  function renderFilters() {
    const filters = [
      ['all', tr('all')], ['upcoming', tr('upcoming')], ['urgent', tr('urgent')], ['soon', tr('soon')],
      ['later', tr('later')], ['undated', tr('verify')], ['closed', tr('closed')]
    ];
    elements.filters.innerHTML = filters.map(([value, label]) => `
      <button type="button" class="deadline-filter-chip${state.filter === value ? ' is-active' : ''}" data-deadline-filter="${value}" aria-pressed="${state.filter === value}">${escapeHtml(label)}</button>`).join('');
  }

  function renderRunway() {
    if (!elements.runway) return;
    const milestones = state.models
      .flatMap(model => model.upcomingEvents.map(event => ({ model, event })))
      .filter(item => item.event.exact && item.event.datePart.year >= TARGET_INTAKE_YEAR)
      .sort((left, right) => left.event.datePart.date - right.event.datePart.date);
    if (!milestones.length) {
      elements.runway.innerHTML = `<div class="deadline-runway__empty"><span aria-hidden="true">◎</span><div><strong>${escapeHtml(tr('runwayEmpty'))}</strong><small>${escapeHtml(tr('runwayEmptyHint'))}</small></div></div>`;
      return;
    }
    const grouped = new Map();
    milestones.forEach(item => {
      const key = `${item.event.datePart.year}-${String(item.event.datePart.month).padStart(2, '0')}`;
      if (!grouped.has(key)) grouped.set(key, []);
      grouped.get(key).push(item);
    });
    elements.runway.innerHTML = [...grouped.values()].map(items => {
      const month = new Intl.DateTimeFormat(lang() === 'tr' ? 'tr-TR' : 'en-GB', { month: 'long', year: 'numeric' }).format(items[0].event.datePart.date);
      const rows = items.slice(0, 4).map(({ model, event }) => `<li><span class="deadline-runway-date"><strong>${String(event.datePart.day).padStart(2, '0')}</strong><small>${escapeHtml(remainingLabel(event.days))}</small></span><span><b>${escapeHtml(model.university)}</b><small>${escapeHtml(eventDisplayLabel(event))}</small></span></li>`).join('');
      return `<article class="deadline-runway-month"><header><span>${escapeHtml(month)}</span><b>${escapeHtml(tr('runwayEvents', { count: items.length }))}</b></header><ol>${rows}</ol></article>`;
    }).join('');
  }

  function favoritesSet() {
    try {
      return new Set(window.uniStorage.readArray('unirank_favorites'));
    } catch {
      return new Set();
    }
  }

  function filteredModels() {
    const query = state.query.trim().toLocaleLowerCase(lang() === 'tr' ? 'tr-TR' : 'en-US');
    const favorites = favoritesSet();
    return state.models.filter(model => {
      if (state.favoritesOnly && !favorites.has(model.id)) return false;
      if (state.filter === 'upcoming' && !model.next) return false;
      if (state.filter === 'undated' && !['undated', 'missing'].includes(model.status)) return false;
      if (!['all', 'upcoming', 'undated'].includes(state.filter) && model.status !== state.filter) return false;
      if (!query) return true;
      const haystack = [model.university, model.program, model.country, model.city, model.cycle.label, model.cycle.academicYear, ...model.documents, ...model.events.map(event => `${event.label} ${event.raw}`)]
        .join(' ').toLocaleLowerCase(lang() === 'tr' ? 'tr-TR' : 'en-US');
      return haystack.includes(query);
    });
  }

  function eventState(event) {
    if (event.referenceOnly) return { key: 'reference', label: tr('previousCycle') };
    if (!event.exact) return { key: 'undated', label: tr('undated') };
    if (event.closed) return { key: 'past', label: tr('past') };
    return { key: 'current', label: tr('current') };
  }

  function sourceLink(source, label, hint = '') {
    if (!source?.url) return `<span class="deadline-source-unavailable">${escapeHtml(tr('sourceUnavailable'))}</span>`;
    return `<a class="deadline-source-link" href="${escapeHtml(source.url)}" target="_blank" rel="noopener noreferrer"><span class="deadline-source-link__icon" aria-hidden="true">↗</span><span><strong>${escapeHtml(label)}</strong>${hint ? `<small>${escapeHtml(hint)}</small>` : ''}</span><span class="sr-only"> (${escapeHtml(tr('openNewTab'))})</span></a>`;
  }

  function renderEvent(event) {
    const stateInfo = eventState(event);
    const dateText = event.exact ? formatDate(event.datePart) : tr('exactDateMissing');
    const countdown = event.referenceOnly ? tr('previousCycle') : (event.exact ? remainingLabel(event.days, event.closed) : tr('undated'));
    const officialNote = eventOfficialNote(event);
    const stepLink = event.sourceUrl
      ? `<a class="deadline-event__source" href="${escapeHtml(event.sourceUrl)}" target="_blank" rel="noopener noreferrer" aria-label="${escapeHtml(`${tr('openOfficialStep')} · ${eventDisplayLabel(event)}`)}">↗</a>`
      : '';
    return `<li class="deadline-event deadline-event--${stateInfo.key} deadline-event--kind-${escapeHtml(event.kind)}">
      <span class="deadline-event__dot" aria-hidden="true"></span>
      <div><strong>${escapeHtml(eventDisplayLabel(event))}</strong>${officialNote ? `<small>${escapeHtml(officialNote)}</small>` : ''}</div>
      <div class="deadline-event__date"><strong>${escapeHtml(dateText)}</strong><span>${escapeHtml(countdown)}</span></div>
      <span class="deadline-event__state">${escapeHtml(stateInfo.label)}</span>${stepLink}
    </li>`;
  }

  function renderProgramCard(model) {
    const next = model.next;
    const reference = !next ? model.referenceDeadline : null;
    const displayedEvent = next || reference;
    const nextDate = displayedEvent ? formatDate(displayedEvent.datePart) : (model.cycle.key === 'awaiting' ? String(TARGET_INTAKE_YEAR) : '—');
    const nextLabel = next
      ? eventDisplayLabel(next)
      : reference
        ? `${tr('lastPublishedDate')} · ${eventDisplayLabel(reference)}`
        : (model.cycle.key === 'awaiting' ? model.cycle.label : (model.status === 'closed' ? tr('noFuture') : tr('deadlineUnknown')));
    const remaining = next
      ? remainingLabel(next.days)
      : reference
        ? tr('referenceWarning', { cycle: model.referenceAcademicYear })
        : (model.cycle.key === 'awaiting' ? tr('exactDateMissing') : (model.status === 'closed' ? tr('closed') : tr('verify')));
    const location = [model.city, model.country].filter(Boolean).join(' · ') || '—';
    const previewDocuments = model.documents.slice(0, 3);
    const extraDocuments = Math.max(0, model.documents.length - previewDocuments.length);
    const futureEvents = model.events.filter(event => !event.closed);
    const pastEvents = model.events.filter(event => event.closed);
    const timelineEvents = [...futureEvents, ...pastEvents];
    const verifiedText = formatStoredDate(model.lastVerified);
    const flagCode = String(model.countryVisual?.code || '').toLowerCase();
    const flag = flagCode
      ? `<span class="deadline-country-flag"><img src="https://flagcdn.com/w80/${escapeHtml(flagCode)}.png" alt="" width="40" height="28" loading="lazy"></span>`
      : '<span class="deadline-country-flag" aria-hidden="true">🌐</span>';
    const accent = /^#[0-9a-f]{6}$/i.test(String(model.countryVisual?.accent || '')) ? model.countryVisual.accent : '#6f85a2';
    const rgb = /^\d{1,3},\s*\d{1,3},\s*\d{1,3}$/.test(String(model.countryVisual?.rgb || '')) ? model.countryVisual.rgb : '111, 133, 162';

    return `<article class="deadline-program-card deadline-program-card--${model.status} deadline-cycle--${escapeHtml(model.cycle.key)}" data-deadline-model="${model.index}" data-country-theme="${escapeHtml(model.countryVisual?.key || 'global')}" style="--deadline-country-accent:${escapeHtml(accent)};--deadline-country-rgb:${escapeHtml(rgb)}">
      <div class="deadline-program-card__accent" aria-hidden="true"></div>
      <div class="deadline-program-card__main">
        <div class="deadline-program-card__identity">
          <div class="deadline-program-card__identity-head">${flag}<div><div class="deadline-program-card__eyebrow"><span>${escapeHtml(location)}</span><span class="deadline-status-pill deadline-status-pill--${model.status}">${escapeHtml(statusLabel(model.status))}</span></div>
          <h3><button type="button" class="deadline-program-title" data-open-deadline-program="${model.index}" title="${escapeHtml(tr('programDetails'))}">${escapeHtml(model.university)}<span class="deadline-program-title__cue" aria-hidden="true">→</span></button></h3>
          <p>${escapeHtml(model.program)}</p></div></div>
          <div class="deadline-program-card__facts">
            ${model.degree ? `<span>${escapeHtml(model.degree)}</span>` : ''}
            <span class="deadline-cycle-pill deadline-cycle-pill--${escapeHtml(model.cycle.key)}">${escapeHtml(model.cycle.label)}</span>
            <span>${escapeHtml(tr('documentsCount', { count: model.documents.length }))}</span>
            <span>${escapeHtml(tr('confidence'))}: ${escapeHtml(confidenceLabel(model.confidence))}</span>
          </div>
        </div>
        <div class="deadline-program-card__next${reference ? ' deadline-program-card__next--reference' : ''}">
          <span>${escapeHtml(next ? tr('current') : (reference ? tr('previousCycle') : statusLabel(model.status)))}</span>
          <strong>${escapeHtml(nextLabel)}</strong>
          <time${displayedEvent ? ` datetime="${escapeHtml(displayedEvent.datePart.key)}"` : ''}>${escapeHtml(nextDate)}</time>
          <b>${escapeHtml(remaining)}</b>
          ${model.admittedOnlyAhead ? `<small class="deadline-admitted-only">${escapeHtml(tr('admittedOnly'))}</small>` : ''}
          ${model.upcomingEvents.length > 1 ? `<small>+${model.upcomingEvents.length - 1} ${escapeHtml(lang() === 'tr' ? 'yaklaşan aşama' : 'upcoming milestone(s)')}</small>` : ''}
        </div>
        <div class="deadline-program-card__documents">
          <span class="deadline-section-label">${escapeHtml(tr('documents'))}</span>
          ${previewDocuments.length ? `<ul>${previewDocuments.map((document, index) => `<li><span class="deadline-document-index" aria-hidden="true">${String(index + 1).padStart(2, '0')}</span><span>${escapeHtml(document)}</span></li>`).join('')}</ul>` : `<p>${escapeHtml(tr('documentsUnknown'))}</p>`}
          ${extraDocuments ? `<small>+${extraDocuments} ${escapeHtml(lang() === 'tr' ? 'belge daha' : 'more document(s)')}</small>` : ''}
        </div>
      </div>
      <details class="deadline-program-details">
        <summary><span>${escapeHtml(tr('expand'))}</span><span aria-hidden="true">⌄</span></summary>
        <div class="deadline-program-details__body">
          <section>
            <h4>${escapeHtml(tr('timeline'))} <span class="deadline-detail-cycle">${escapeHtml(model.cycle.label)}</span></h4>
            ${timelineEvents.length ? `<ol class="deadline-event-list">${timelineEvents.map(renderEvent).join('')}</ol>` : `<p class="deadline-empty-copy">${escapeHtml(tr('deadlineUnknown'))}</p>`}
          </section>
          <section>
            <h4>${escapeHtml(tr('documents'))}</h4>
            ${model.documents.length ? `<ul class="deadline-document-list">${model.documents.map((document, index) => `<li><span class="deadline-document-index" aria-hidden="true">${String(index + 1).padStart(2, '0')}</span><span>${escapeHtml(document)}</span></li>`).join('')}</ul>` : `<p class="deadline-empty-copy">${escapeHtml(tr('documentsUnknown'))}</p>`}
          </section>
          <footer class="deadline-program-details__footer">
            <div class="deadline-verification-meta"><span>${escapeHtml(tr('verified'))}: <strong>${escapeHtml(verifiedText)}</strong></span><span>${escapeHtml(tr('confidence'))}: <strong>${escapeHtml(confidenceLabel(model.confidence))}</strong></span></div>
            <div class="deadline-program-actions">
              ${sourceLink(model.deadlineSource, tr('applicationSource'), tr('applicationLinkHint'))}
              ${model.documentSource?.url && model.documentSource.url !== model.deadlineSource?.url ? sourceLink(model.documentSource, tr('documentSource'), tr('documentLinkHint')) : ''}
              <button type="button" class="deadline-program-open" data-open-deadline-program="${model.index}">${escapeHtml(tr('programDetails'))} <span aria-hidden="true">→</span></button>
            </div>
          </footer>
        </div>
      </details>
    </article>`;
  }

  function syncStatusHtml() {
    let label = tr('syncing');
    let modifier = ' is-syncing';
    if (!state.syncing && state.syncFailed) {
      label = tr('syncFailed');
      modifier = ' is-failed';
    } else if (!state.syncing && state.lastSyncedAt) {
      const time = new Intl.DateTimeFormat(lang() === 'tr' ? 'tr-TR' : 'en-GB', { hour: '2-digit', minute: '2-digit' }).format(state.lastSyncedAt);
      label = tr('autoUpdated', { time });
      modifier = '';
    }
    return `<span class="deadline-auto-sync${modifier}" role="status"><i aria-hidden="true"></i>${escapeHtml(label)}</span>`;
  }

  function renderList() {
    const models = filteredModels();
    elements.meta.innerHTML = `<span>${escapeHtml(tr('showing', { shown: models.length, total: state.models.length }))}</span><span>${escapeHtml(tr('currentFilters'))}</span>${syncStatusHtml()}`;
    if (!models.length) {
      const message = state.favoritesOnly ? tr('noFavorites') : tr('noMatches');
      elements.list.innerHTML = `<div class="deadline-empty-state"><span aria-hidden="true">🗓</span><h3>${escapeHtml(message)}</h3><p>${escapeHtml(tr('verifyHint'))}</p></div>`;
      return;
    }
    elements.list.innerHTML = models.map(renderProgramCard).join('');
  }

  function render() {
    renderSummary();
    renderRunway();
    renderFilters();
    renderList();
  }

  function setFilter(filter) {
    state.filter = filter;
    render();
  }

  function modalIsOpen() {
    return Boolean(elements.modal && !elements.modal.hidden);
  }

  function refreshCountdowns() {
    if (!state.records.length && Array.isArray(window.uniRankRecords)) state.records = window.uniRankRecords;
    rebuildModels();
    renderSummary();
    if (modalIsOpen()) {
      renderRunway();
      renderList();
    }
  }

  async function requestDataRefresh() {
    if (state.syncing || document.hidden || typeof window.refreshUniRankData !== 'function') return false;
    state.syncing = true;
    state.syncFailed = false;
    if (modalIsOpen()) renderList();
    try {
      const refreshed = await window.refreshUniRankData();
      state.syncFailed = !refreshed;
      return Boolean(refreshed);
    } catch (error) {
      console.warn('Deadline calendar auto-refresh failed:', error);
      state.syncFailed = true;
      return false;
    } finally {
      state.syncing = false;
      if (modalIsOpen()) renderList();
    }
  }

  function dataIsStale() {
    return !state.lastSyncedAt || Date.now() - state.lastSyncedAt.getTime() >= AUTO_REFRESH_MS;
  }

  function scheduleMidnightRefresh() {
    const now = new Date();
    const nextMidnight = new Date(now.getFullYear(), now.getMonth(), now.getDate() + 1, 0, 0, 1);
    window.setTimeout(() => {
      refreshCountdowns();
      scheduleMidnightRefresh();
    }, Math.max(1000, nextMidnight.getTime() - now.getTime()));
  }

  function open() {
    state.lastFocus = document.activeElement;
    state.records = Array.isArray(window.uniRankRecords) ? window.uniRankRecords : state.records;
    rebuildModels();
    render();
    elements.modal.hidden = false;
    elements.modal.setAttribute('aria-hidden', 'false');
    document.body.classList.add('deadline-modal-open');
    requestAnimationFrame(() => elements.close.focus());
    if (dataIsStale()) requestDataRefresh();
  }

  function close() {
    elements.modal.hidden = true;
    elements.modal.setAttribute('aria-hidden', 'true');
    document.body.classList.remove('deadline-modal-open');
    if (state.lastFocus instanceof HTMLElement) state.lastFocus.focus();
  }

  function handleModalClick(event) {
    const filterButton = event.target.closest('[data-deadline-filter]');
    if (filterButton) {
      setFilter(filterButton.dataset.deadlineFilter);
      return;
    }
    const openButton = event.target.closest('[data-open-deadline-program]');
    if (openButton) {
      const model = state.models.find(item => item.index === Number(openButton.dataset.openDeadlineProgram));
      close();
      if (model && typeof window.openDrawer === 'function') setTimeout(() => window.openDrawer(model.record), 60);
    }
  }

  function trapFocus(event) {
    if (event.key !== 'Tab' || elements.modal.hidden) return;
    const focusable = [...elements.modal.querySelectorAll('button:not([disabled]), a[href], input:not([disabled]), summary')].filter(element => element.offsetParent !== null);
    if (!focusable.length) return;
    const first = focusable[0];
    const last = focusable[focusable.length - 1];
    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  }

  function setup() {
    elements.modal = document.getElementById('deadline-modal');
    elements.launcher = document.getElementById('deadline-launcher');
    elements.launcherSummary = document.getElementById('deadline-launcher-summary');
    elements.badge = document.getElementById('deadline-launcher-badge');
    elements.close = document.getElementById('deadline-modal-close');
    elements.summary = document.getElementById('deadline-summary-grid');
    elements.runway = document.getElementById('deadline-runway-track');
    elements.filters = document.getElementById('deadline-filter-chips');
    elements.search = document.getElementById('deadline-search-input');
    elements.favorites = document.getElementById('deadline-favorites-only');
    elements.meta = document.getElementById('deadline-results-meta');
    elements.list = document.getElementById('deadline-program-list');
    if (!elements.modal || !elements.launcher) return;

    elements.launcher.addEventListener('click', open);
    elements.close.addEventListener('click', close);
    elements.modal.addEventListener('click', event => {
      if (event.target === elements.modal) close();
      else handleModalClick(event);
    });
    elements.search.addEventListener('input', event => {
      state.query = event.target.value;
      renderList();
    });
    elements.favorites.addEventListener('change', event => {
      state.favoritesOnly = event.target.checked;
      renderList();
    });
    document.addEventListener('keydown', event => {
      if (event.key === 'Escape' && !elements.modal.hidden) {
        event.preventDefault();
        close();
      } else {
        trapFocus(event);
      }
    });
    window.addEventListener('unirank:recordsLoaded', event => {
      state.records = Array.isArray(event.detail?.records) ? event.detail.records : [];
      state.lastSyncedAt = new Date(event.detail?.refreshedAt || Date.now());
      state.syncFailed = false;
      rebuildModels();
      renderSummary();
      if (modalIsOpen()) {
        renderRunway();
        renderList();
      }
    });
    document.addEventListener('languageChanged', () => {
      if (!state.records.length && Array.isArray(window.uniRankRecords)) state.records = window.uniRankRecords;
      rebuildModels();
      render();
    });
    document.addEventListener('visibilitychange', () => {
      if (document.hidden) return;
      refreshCountdowns();
      if (dataIsStale()) requestDataRefresh();
    });
    window.addEventListener('online', () => {
      if (dataIsStale()) requestDataRefresh();
    });
    window.setInterval(() => {
      if (!document.hidden && dataIsStale()) requestDataRefresh();
    }, REFRESH_CHECK_MS);
    scheduleMidnightRefresh();

    if (Array.isArray(window.uniRankRecords)) {
      state.records = window.uniRankRecords;
      rebuildModels();
      renderSummary();
    }

    if (new URLSearchParams(window.location.search).get('calendar') === 'open') {
      window.requestAnimationFrame(open);
    }
  }

  window.uniDeadlineDashboard = {
    collectDeadlineEvents,
    documentItems,
    programModel,
    daysFromToday,
    datePartsFromIso,
    cycleInfo,
    formatDate,
    eventDisplayLabel,
    eventOfficialNote,
    refreshNow: requestDataRefresh,
    refreshCountdowns
  };
  window.openDeadlineDashboard = open;
  window.closeDeadlineDashboard = close;

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', setup, { once: true });
  else setup();
})();
