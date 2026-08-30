/**
 * Permit, funds and clearance panel.
 *
 * This was the only decision field in the database with zero coverage. Nothing
 * told the reader which permit a country issues, how much money has to be
 * proven, or which clearance gates the visa — so each of those questions meant
 * leaving for a search engine, at the point where a wrong answer costs a whole
 * application cycle.
 *
 * The rules are nationality-specific and the file says so: they are written for
 * a Turkish citizen applying from Türkiye. A country that has not been read
 * from an official source renders as unverified rather than as empty, because
 * an empty field here would read as "nothing required".
 */

// Wrapped in an IIFE. Written as a plain script, this file's local helpers -
// t(), lang(), text(), esc() - become globals, and t() in particular overwrote
// window.t from i18n.js, which silently turned every translated string on the
// page into its raw key.
(function () {
  'use strict';
  let visaData = null;
  let visaPromise = null;

  async function loadVisaRequirements() {
    if (visaData) return visaData;
    if (visaPromise) return visaPromise;

    visaPromise = fetch('/api/visa-requirements')
      .then((response) => response.json())
      .then((payload) => {
        visaData = (payload && payload.data) || {};
        return visaData;
      })
      .catch(() => {
        visaData = {};
        return visaData;
      });

    return visaPromise;
  }

  function lang() {
    return window.currentLanguage === 'tr' ? 'tr' : 'en';
  }

  function text(value) {
    if (!value) return '';
    if (typeof value === 'string') return value;
    return value[lang()] || value.en || value.tr || '';
  }

  function esc(value) {
    return String(value == null ? '' : value).replace(/[&<>"']/g, (character) => (
      { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[character]
    ));
  }

  const copy = {
    en: {
      title: 'Permit, funds and clearances',
      subtitle: 'For a Turkish citizen applying from Türkiye',
      permit: 'Permit',
      applyFrom: 'Earliest application',
      money: 'Money you must prove',
      holding: 'How long the money must sit there',
      plusFees: 'On top of that',
      clearance: 'Clearance that gates the visa',
      processing: 'Processing time',
      sequencing: 'Where it sits in your order of work',
      needFirst: 'You need this before you can start it',
      documents: 'Documents',
      sources: 'Official sources',
      unverified: 'Not verified yet',
      unverifiedBody: 'This country is in the database but its immigration rules have not been read from an official source yet. Nothing here is estimated — treat it as unknown, not as "nothing required", and check the mission in Türkiye before you budget.',
      notApplicable: 'No permit needed',
      perMonth: '/month',
      upToMonths: 'for up to {n} months',
      turkishNote: 'What this means for a Turkish passport',
    },
    tr: {
      title: 'İzin, fon ve ön onaylar',
      subtitle: 'Türkiye’den başvuran bir Türk vatandaşı için',
      permit: 'İzin',
      applyFrom: 'En erken başvuru',
      money: 'Kanıtlaman gereken para',
      holding: 'Paranın ne kadar süre durması gerektiği',
      plusFees: 'Buna ek olarak',
      clearance: 'Vizeyi kilitleyen ön onay',
      processing: 'İşlem süresi',
      sequencing: 'İş sıranda nereye oturuyor',
      needFirst: 'Başlamadan önce buna ihtiyacın var',
      documents: 'Belgeler',
      sources: 'Resmî kaynaklar',
      unverified: 'Henüz doğrulanmadı',
      unverifiedBody: 'Bu ülke veritabanında var ancak göçmenlik kuralları henüz resmî bir kaynaktan okunmadı. Buradaki hiçbir şey tahmin değildir — "hiçbir şey gerekmiyor" değil, "bilinmiyor" olarak gör ve bütçelemeden önce Türkiye’deki temsilcilikten kontrol et.',
      notApplicable: 'İzin gerekmiyor',
      perMonth: '/ay',
      upToMonths: 'en fazla {n} ay için',
      turkishNote: 'Türk pasaportu için bunun anlamı',
    },
  };

  function t(key, replacements) {
    let value = copy[lang()][key] || copy.en[key] || key;
    Object.entries(replacements || {}).forEach(([name, replacement]) => {
      value = value.replace(`{${name}}`, String(replacement));
    });
    return value;
  }

  function row(label, body, modifier) {
    if (!body) return '';
    return `<div class="visa-row${modifier ? ` visa-row--${modifier}` : ''}">
      <span class="visa-row__label">${esc(label)}</span>
      <div class="visa-row__body">${body}</div>
    </div>`;
  }

  function amountsHTML(financial) {
    const amounts = Array.isArray(financial.amounts) ? financial.amounts : [];
    if (!amounts.length) return '';
    const items = amounts.map((entry) => {
      const value = entry.amount_gbp_per_month != null
        ? `£${entry.amount_gbp_per_month.toLocaleString(lang() === 'tr' ? 'tr-TR' : 'en-GB')}`
        : entry.amount || '';
      const months = entry.months ? ` <small>${esc(t('upToMonths', { n: entry.months }))}</small>` : '';
      return `<li><strong>${esc(value)}</strong><span>${esc(t('perMonth'))}</span>
        <em>${esc(entry.scope || '')}</em>${months}</li>`;
    }).join('');
    return `<ul class="visa-amounts">${items}</ul>`;
  }

  function sourcesHTML(sources) {
    if (!Array.isArray(sources) || !sources.length) return '';
    const items = sources.map((source) => `<li>
        <a href="${esc(source.url)}" target="_blank" rel="noopener noreferrer">${esc(source.title || source.url)}</a>
        ${source.notes ? `<small>${esc(text(source.notes))}</small>` : ''}
      </li>`).join('');
    return `<div class="visa-sources"><span class="visa-row__label">${esc(t('sources'))}</span><ul>${items}</ul></div>`;
  }

  function visaPanel(record) {
    if (!record || !visaData || !visaData.countries) return '';
    const country = String(record.country || '').trim();
    const entry = visaData.countries[country];
    if (!entry) return '';

    const head = `<div class="visa-panel__head">
        <span class="premium-icon" data-glyph="🛂" aria-hidden="true"></span>
        <div>
          <h4>${esc(t('title'))}</h4>
          <small>${esc(t('subtitle'))} · ${esc(country)}</small>
        </div>
      </div>`;

    if (entry.status === 'not_applicable') {
      return `<section class="decision-panel visa-panel">${head}
        <p class="visa-note">${esc(text(entry.note))}</p></section>`;
    }

    if (entry.status !== 'verified') {
      const extra = entry.known_shape ? `<p class="visa-note">${esc(text(entry.known_shape))}</p>` : '';
      const why = entry.blocked_source_note ? `<p class="visa-note visa-note--muted">${esc(text(entry.blocked_source_note))}</p>` : '';
      return `<section class="decision-panel visa-panel visa-panel--unverified">${head}
        <p class="visa-unverified"><strong>${esc(t('unverified'))}</strong> ${esc(t('unverifiedBody'))}</p>
        ${extra}${why}</section>`;
    }

    const financial = entry.financial_requirement || {};
    const clearance = entry.special_clearance || {};

    const documents = Array.isArray(entry.documents) && entry.documents.length
      ? `<ul class="visa-documents">${entry.documents.map((item) => `<li>${esc(text(item))}</li>`).join('')}</ul>`
      : '';

    const clearanceBody = clearance.name ? [
      `<strong class="visa-clearance__name">${esc(clearance.name)}</strong>`,
      clearance.why_it_matters_here ? `<p>${esc(text(clearance.why_it_matters_here))}</p>` : '',
      clearance.processing_time ? `<p class="visa-callout"><span>${esc(t('processing'))}</span>${esc(text(clearance.processing_time))}</p>` : '',
      clearance.sequencing ? `<p><span class="visa-inline-label">${esc(t('sequencing'))}</span>${esc(text(clearance.sequencing))}</p>` : '',
      clearance.what_you_need_first ? `<p><span class="visa-inline-label">${esc(t('needFirst'))}</span>${esc(text(clearance.what_you_need_first))}</p>` : '',
      clearance.contact ? `<p class="visa-contact"><a href="mailto:${esc(clearance.contact)}">${esc(clearance.contact)}</a></p>` : '',
    ].join('') : '';

    return `<section class="decision-panel visa-panel">
      ${head}
      ${row(t('permit'), entry.permit_name ? `<p>${esc(text(entry.permit_name))}</p>` : '')}
      ${row(t('applyFrom'), entry.apply_from ? `<p>${esc(text(entry.apply_from.note) || entry.apply_from.earliest || '')}</p>` : '')}
      ${row(t('money'), [
        amountsHTML(financial),
        financial.plus_course_fees ? `<p><span class="visa-inline-label">${esc(t('plusFees'))}</span>${esc(text(financial.plus_course_fees))}</p>` : '',
        financial.holding_period ? `<p><span class="visa-inline-label">${esc(t('holding'))}</span>${esc(text(financial.holding_period))}</p>` : '',
        financial.turkish_citizen_note ? `<p class="visa-callout visa-callout--flag"><span>${esc(t('turkishNote'))}</span>${esc(text(financial.turkish_citizen_note))}</p>` : '',
      ].join(''))}
      ${row(t('clearance'), clearanceBody, 'clearance')}
      ${row(t('documents'), documents)}
      ${sourcesHTML(entry.sources)}
    </section>`;
  }

  window.uniVisaPanel = {
    load: loadVisaRequirements,
    panel: visaPanel,
    isLoaded: () => Boolean(visaData),
  };
})();
