/* Read the application fee the standard publishes, once, for every surface.
 *
 * The fee was already researched for a third of the catalogue and none of it
 * reached a reader, because it was stored under seven key names across two
 * profiles and five currencies.  scripts/standardize_categories.py moves
 * whichever key a record used into cost_profile.application_fee_standard;
 * this file is the only place that reads it, so the cost card and the
 * application calendar can never disagree about what a programme costs to
 * apply to.
 */
(function () {
  'use strict';

  const FX = {
    EUR: 1, USD: 1.1643, GBP: 0.8572, CHF: 0.9364, SEK: 11.0885, DKK: 7.4748,
    NOK: 10.8595, PLN: 4.3365, CZK: 24.148, JPY: 185.92, KRW: 1600.39,
    CNY: 7.8251, RON: 5.2584, TRY: 56.1718, HUF: 364.79
  };

  const COPY = {
    en: {
      free: 'No application fee',
      notPublished: 'No fee on the official route',
      unknown: 'Not verified',
      unknownShort: 'Fee not verified',
      perApplication: 'per application',
      perProgramme: 'per programme choice',
      portalAccount: 'one payment for the whole cycle',
      coversProgrammes: 'one payment covers {count} programmes',
      chargedByService: 'charged by {name}, not the university',
      nonRefundable: 'non-refundable',
      refundable: 'refundable',
      waiverOpen: 'Fee waiver available',
      waiverClosed: 'Fee waiver closed to applicants from abroad',
      waiverNone: 'No fee waiver',
      waiverBy: 'waiver request by {date}',
      waiverLead: 'allow {count} business days',
      earlyBird: '{early} until {date}, then {full}',
      earlyBirdPast: 'Last cycle charged {early} until {date} and {full} after it — expect the same window to reopen',
      earlySaving: 'Applying by {date} saves {amount}',
      approx: '≈ {amount}',
      routesPriced: 'The published fees are for routes a non-EU applicant cannot use',
      pagesChecked: 'Pages read: {count}',
      totalTitle: 'Cost of applying',
      totalNone: 'No verified fee among these programmes',
      totalLine: '{total} to apply to {count} programmes',
      totalUnverified: '{count} of them publish no verified fee',
      totalSaving: '{amount} of that disappears if you apply inside the early windows'
    },
    tr: {
      free: 'Başvuru ücreti yok',
      notPublished: 'Resmî yolda ücret yok',
      unknown: 'Doğrulanmadı',
      unknownShort: 'Ücret doğrulanmadı',
      perApplication: 'başvuru başına',
      perProgramme: 'program tercihi başına',
      portalAccount: 'tüm dönem için tek ödeme',
      coversProgrammes: 'tek ödeme {count} programı kapsıyor',
      chargedByService: 'üniversite değil {name} tahsil ediyor',
      nonRefundable: 'iade edilmez',
      refundable: 'iade edilebilir',
      waiverOpen: 'Ücret muafiyeti var',
      waiverClosed: 'Ücret muafiyeti yurt dışından başvuranlara kapalı',
      waiverNone: 'Ücret muafiyeti yok',
      waiverBy: 'muafiyet talebi için son gün {date}',
      waiverLead: '{count} iş günü payı bırak',
      earlyBird: '{date} tarihine kadar {early}, sonrasında {full}',
      earlyBirdPast: 'Geçen dönem {date} tarihine kadar {early}, sonrasında {full} alındı — aynı pencerenin yeniden açılmasını bekle',
      earlySaving: '{date} tarihine kadar başvurmak {amount} kazandırıyor',
      approx: '≈ {amount}',
      routesPriced: 'Yayımlanan ücretler, AB dışı bir adayın kullanamayacağı yollara ait',
      pagesChecked: 'Okunan sayfa: {count}',
      totalTitle: 'Başvurmanın maliyeti',
      totalNone: 'Bu programlar arasında doğrulanmış ücret yok',
      totalLine: '{count} programa başvurmak {total}',
      totalUnverified: 'Bunlardan {count} tanesi doğrulanmış bir ücret yayımlamıyor',
      totalSaving: 'Erken pencerelerin içinde başvurursan bunun {amount} kadarı ortadan kalkıyor'
    }
  };

  function lang() {
    return window.currentLanguage === 'tr' ? 'tr' : 'en';
  }

  function tr(key, replacements) {
    let value = (COPY[lang()] || COPY.en)[key] || COPY.en[key] || key;
    Object.entries(replacements || {}).forEach(([name, replacement]) => {
      value = value.replace(`{${name}}`, String(replacement));
    });
    return value;
  }

  function money(amount, currency) {
    if (!Number.isFinite(Number(amount)) || !currency) return '';
    try {
      return new Intl.NumberFormat(lang() === 'tr' ? 'tr-TR' : 'en-GB', {
        style: 'currency', currency, maximumFractionDigits: Number(amount) % 1 === 0 ? 0 : 2
      }).format(Number(amount));
    } catch {
      return `${currency} ${Number(amount).toLocaleString()}`;
    }
  }

  function toEur(amount, currency) {
    const rate = FX[String(currency || '').toUpperCase()];
    if (!rate || !Number.isFinite(Number(amount))) return null;
    return Number(amount) / rate;
  }

  function localized(value) {
    if (!value) return '';
    if (typeof value === 'string') return value;
    if (typeof value === 'object') return value[lang()] || value.en || value.tr || '';
    return String(value);
  }

  function formatDate(iso) {
    if (!/^\d{4}-\d{2}-\d{2}$/.test(String(iso || ''))) return '';
    const [year, month, day] = String(iso).split('-').map(Number);
    return new Intl.DateTimeFormat(lang() === 'tr' ? 'tr-TR' : 'en-GB', {
      day: 'numeric', month: 'long', year: 'numeric'
    }).format(new Date(year, month - 1, day, 12));
  }

  /** The published fee block for one record, or null when the record has none. */
  function read(record) {
    const fee = record && record.cost_profile && record.cost_profile.application_fee_standard;
    return fee && typeof fee === 'object' ? fee : null;
  }

  /** The headline a card shows: the amount, or an honest word instead of one. */
  function headline(fee) {
    if (!fee) return tr('unknown');
    if (fee.status === 'no_fee') return tr('free');
    if (fee.status === 'not_published') return tr('notPublished');
    if (fee.status !== 'published') return tr('unknown');
    const primary = money(fee.amount, fee.currency);
    if (!primary) return tr('unknown');
    if (String(fee.currency).toUpperCase() === 'EUR') return primary;
    const euros = toEur(fee.amount, fee.currency);
    return euros === null ? primary : `${primary} · ${tr('approx', { amount: money(Math.round(euros), 'EUR') })}`;
  }

  /** Everything worth saying about the fee in one line of short phrases. */
  function qualifiers(fee) {
    if (!fee || fee.status !== 'published') return [];
    const parts = [];
    if (fee.charged_by === 'central_application_service') {
      parts.push(tr('chargedByService', { name: serviceName(fee) }));
    }
    if (fee.covers_programmes) parts.push(tr('coversProgrammes', { count: fee.covers_programmes }));
    else if (fee.charged_per === 'programme_choice') parts.push(tr('perProgramme'));
    else if (fee.charged_per === 'admission_portal_account') parts.push(tr('portalAccount'));
    else parts.push(tr('perApplication'));
    if (fee.refundable === false) parts.push(tr('nonRefundable'));
    else if (fee.refundable === true) parts.push(tr('refundable'));
    return parts;
  }

  // Naming the body that takes the money is part of the answer: it says who to
  // pay, who to chase when it goes wrong, and - for uni-assist - why a second
  // German application costs a third of the first.
  const SERVICES = [
    [/uni[-_ ]?assist/i, 'uni-assist'],
    [/universityadmissions|antagning/i, 'universityadmissions.se'],
    [/studyinfo|finnish national agency/i, 'Studyinfo.fi'],
    [/campus ?france|etudes en france|études en france/i, 'Campus France']
  ];

  function serviceName(fee) {
    if (fee.charged_by_name) return fee.charged_by_name;
    const haystack = `${JSON.stringify(fee.derived_from || {})} ${JSON.stringify(fee.components || [])}`;
    const match = SERVICES.find(([pattern]) => pattern.test(haystack));
    if (match) return match[1];
    return lang() === 'tr' ? 'merkezi başvuru servisi' : 'the central application service';
  }

  /** The waiver sentence, when the record says anything usable about one. */
  function waiverLine(fee) {
    const waiver = fee && fee.waiver;
    if (!waiver) return '';
    const parts = [];
    // "No waiver at all" is the stronger statement and has to win: saying a
    // waiver is closed to applicants from abroad implies one exists for
    // somebody else, and at Politecnico di Milano nobody gets one.
    if (waiver.available === false) parts.push(tr('waiverNone'));
    else if (waiver.open_to_international === false) parts.push(tr('waiverClosed'));
    else if (waiver.available === true) parts.push(tr('waiverOpen'));
    else if (waiver.note) parts.push(localized(waiver.note));
    else return '';
    if (waiver.request_deadline) parts.push(tr('waiverBy', { date: formatDate(waiver.request_deadline) }));
    if (waiver.processing_days) parts.push(tr('waiverLead', { count: waiver.processing_days }));
    return parts.filter(Boolean).join(' · ');
  }

  /** An early window is a deadline with a price on it, so it gets its own line. */
  function earlyWindow(fee) {
    if (!fee || fee.status !== 'published') return null;
    const early = Number(fee.early_amount);
    const full = Number(fee.amount);
    if (!Number.isFinite(early) || !Number.isFinite(full) || early >= full || !fee.early_deadline) return null;
    const days = daysUntil(fee.early_deadline);
    const open = days !== null && days >= 0;
    return {
      saving: full - early,
      currency: fee.currency,
      deadline: fee.early_deadline,
      days,
      open,
      // A window that closed belongs to the cycle the university has already
      // published.  Repeating its date as though it were live would be the
      // same mistake as counting last year's deadline as this year's.
      label: tr(open ? 'earlyBird' : 'earlyBirdPast', {
        early: money(early, fee.currency),
        full: money(full, fee.currency),
        date: formatDate(fee.early_deadline)
      }),
      savingLabel: tr('earlySaving', {
        date: formatDate(fee.early_deadline),
        amount: money(full - early, fee.currency)
      })
    };
  }

  function daysUntil(iso) {
    if (!/^\d{4}-\d{2}-\d{2}$/.test(String(iso || ''))) return null;
    const [year, month, day] = String(iso).split('-').map(Number);
    const now = new Date();
    return Math.round(
      (Date.UTC(year, month - 1, day) - Date.UTC(now.getFullYear(), now.getMonth(), now.getDate()))
      / 86400000
    );
  }

  /** The euro amount a shortlist costs to apply to, and what is missing from it.
   *
   * A fee whose payment covers several programmes is counted once per
   * university rather than once per record, because that is how the money
   * actually leaves the account: Sweden charges SEK 900 for the semester
   * however many Swedish programmes are on the list.
   */
  function total(records) {
    const perPayer = new Map();
    let unverified = 0;
    let free = 0;
    let saving = 0;
    let priced = 0;

    (records || []).forEach(record => {
      const fee = read(record);
      if (!fee || fee.status === 'unknown') { unverified += 1; return; }
      if (fee.status !== 'published') { free += 1; return; }
      const euros = toEur(fee.amount, fee.currency);
      if (euros === null) { unverified += 1; return; }
      priced += 1;

      const early = earlyWindow(fee);
      // One payment covering several programmes is charged once, keyed on who
      // takes the money rather than on the record it was found in.
      const shared = fee.covers_programmes || fee.charged_by === 'central_application_service';
      const key = shared
        ? `${fee.charged_by}|${fee.currency}|${fee.amount}|${record.country || ''}`
        : `record|${record.id || Math.random()}`;
      if (!perPayer.has(key)) {
        perPayer.set(key, euros);
        if (early && early.open) saving += toEur(early.saving, fee.currency) || 0;
      }
    });

    const amount = [...perPayer.values()].reduce((sum, value) => sum + value, 0);
    return {
      euros: amount,
      // `priced` is how many of the listed programmes carry a fee; `payments`
      // is how many separate payments those become once a fee that covers
      // several programmes is counted once.  They are different numbers and
      // reporting either as the other would misstate the bill.
      priced,
      payments: perPayer.size,
      unverified,
      free,
      saving,
      label: money(Math.round(amount), 'EUR')
    };
  }

  window.uniApplicationFee = {
    read, headline, qualifiers, waiverLine, earlyWindow, total,
    money, toEur, formatDate, daysUntil, localized, tr
  };
})();
