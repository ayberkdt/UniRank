(() => {
  'use strict';

  const copy = {
    en: {
      skip: 'Skip to research matches', brand: 'Research fit', programmes: 'Programmes', calendar: 'Application calendar', scholarships: 'Scholarships', researchFit: 'Research fit',
      heroKicker: 'FROM VAGUE LABELS TO RESEARCH EVIDENCE', heroTitle: 'Choose the lab, not just the university name.', heroText: 'Separate orbital mechanics, trajectory design, estimation and GNC; then compare programmes and faculty using current official evidence.', browse: 'Explore matches', contactGuide: 'When should I contact faculty?', heroAside: 'A strong programme here means the official department publishes a relevant group, lab or research area. It is not a prestige ranking or an admission guarantee.', officialEvidence: 'Official evidence only',
      fieldKicker: 'Canonical field system', fieldTitle: 'Start by naming the problem correctly.', fieldText: 'These filters are deliberately narrower than “space” or “control”. Select one to update programmes and faculty together.', allFields: 'All fields', includes: 'Includes', distinctFrom: 'Keep distinct from',
      programmeKicker: 'Evidence-led shortlist', programmeTitle: 'Strong programmes for the selected field', advisorKicker: 'Practical application note', advisorTitle: 'Do I need to find a professor first?', advisorText: 'The answer changes by programme and stage. The cards below distinguish an application requirement from useful research networking.',
      facultyKicker: 'Named research matches', facultyTitle: 'Faculty worth investigating', outreachKicker: 'A focused first contact', outreachTitle: 'Write one useful email, not ten generic ones.', outreachText: 'Use this only when the programme timing and your technical overlap make contact appropriate.', subject: 'Subject', footerPolicy: 'No invented faculty match. Every named person and programme claim links to an official source.',
      canonicalFields: 'canonical fields', strongProgrammes: 'evidence-backed programmes', facultyMatches: 'named faculty matches', officialSources: 'official sources checked', verified: 'Verified', showingProgrammes: '{count} programme matches', showingFaculty: '{count} faculty matches', veryStrong: 'Very strong evidence', strong: 'Strong evidence', whyFit: 'Why it fits', practical: 'Practical note', officialResearch: 'Official research evidence', programmeDetails: 'Open programme details', beforeApplication: 'Before application', afterAdmission: 'After admission', programmeContact: 'Programme contact', officialProfile: 'Official profile', email: 'Email', noMatch: 'No match for this filter yet.', avoid: 'Avoid',
      policy_after: 'RA outreach after admission', policy_during: 'Supervisor match during the MSc',
      applyFee: 'Cost to apply', perApplication: 'per application', perProgrammeChoice: 'per programme choice',
      nonRefundable: 'non-refundable', waiverClosedIntl: 'fee waiver closed to applicants from abroad'
    },
    tr: {
      skip: 'Araştırma eşleşmelerine geç', brand: 'Araştırma uyumu', programmes: 'Programlar', calendar: 'Başvuru takvimi', scholarships: 'Burslar', researchFit: 'Araştırma uyumu',
      heroKicker: 'BELİRSİZ ETİKETTEN ARAŞTIRMA KANITINA', heroTitle: 'Sadece üniversite adını değil, laboratuvarı seç.', heroText: 'Yörünge mekaniği, yörünge tasarımı, kestirim ve GNC’yi birbirinden ayır; programları ve hocaları güncel resmî kanıtlarla karşılaştır.', browse: 'Eşleşmeleri incele', contactGuide: 'Hocaya ne zaman yazmalıyım?', heroAside: 'Burada güçlü program, ilgili grup, laboratuvar veya araştırma alanının resmî bölüm sayfasında yayımlandığı anlamına gelir. Prestij sıralaması veya kabul garantisi değildir.', officialEvidence: 'Yalnızca resmî kanıt',
      fieldKicker: 'Standart alan sistemi', fieldTitle: 'Önce problemi doğru adlandır.', fieldText: 'Bu filtreler bilerek “uzay” veya “kontrol” etiketlerinden daha dardır. Birini seçtiğinde program ve hoca listesi birlikte güncellenir.', allFields: 'Tüm alanlar', includes: 'Kapsar', distinctFrom: 'Şunlardan ayrı tut',
      programmeKicker: 'Kanıta dayalı kısa liste', programmeTitle: 'Seçilen alan için güçlü programlar', advisorKicker: 'Pratik başvuru notu', advisorTitle: 'Önce hoca bulmam gerekiyor mu?', advisorText: 'Cevap programa ve aşamaya göre değişir. Aşağıdaki kartlar başvuru şartıyla yararlı araştırma iletişimini birbirinden ayırır.',
      facultyKicker: 'İsimlendirilmiş araştırma eşleşmeleri', facultyTitle: 'İncelemeye değer hocalar', outreachKicker: 'Hedefli ilk iletişim', outreachTitle: 'On genel e-posta değil, bir faydalı e-posta yaz.', outreachText: 'Bunu yalnızca programın zamanlaması ve teknik kesişimin iletişimi anlamlı kılıyorsa kullan.', subject: 'Konu', footerPolicy: 'Uydurma hoca eşleşmesi yok. Her kişi ve program iddiası resmî bir kaynağa bağlıdır.',
      canonicalFields: 'standart alan', strongProgrammes: 'kanıtlı güçlü program', facultyMatches: 'isimlendirilmiş hoca eşleşmesi', officialSources: 'kontrol edilen resmî kaynak', verified: 'Doğrulandı', showingProgrammes: '{count} program eşleşmesi', showingFaculty: '{count} hoca eşleşmesi', veryStrong: 'Çok güçlü kanıt', strong: 'Güçlü kanıt', whyFit: 'Neden uyumlu?', practical: 'Pratik not', officialResearch: 'Resmî araştırma kanıtı', programmeDetails: 'Program detayını aç', beforeApplication: 'Başvurudan önce', afterAdmission: 'Kabulden sonra / program içinde', programmeContact: 'Program iletişimi', officialProfile: 'Resmî profil', email: 'E-posta', noMatch: 'Bu filtre için henüz eşleşme yok.', avoid: 'Kaçın',
      policy_after: 'RA iletişimi kabulden sonra', policy_during: 'Danışman eşleşmesi MSc içinde',
      applyFee: 'Başvurmanın maliyeti', perApplication: 'başvuru başına', perProgrammeChoice: 'program tercihi başına',
      nonRefundable: 'iade edilmez', waiverClosedIntl: 'ücret muafiyeti yurt dışından başvuranlara kapalı'
    }
  };

  let catalog = null;
  let selectedField = 'all';
  const byId = (id) => document.getElementById(id);
  const lang = () => window.currentLanguage === 'tr' ? 'tr' : 'en';
  const t = (key, vars = {}) => Object.entries(vars).reduce((value, [name, replacement]) => value.replace(`{${name}}`, replacement), copy[lang()][key] || copy.en[key] || key);
  const local = (value) => value == null ? '' : typeof value === 'string' ? value : value[lang()] || value.en || value.tr || '';
  const escapeHtml = (value) => String(value ?? '').replace(/[&<>'"]/g, (character) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[character]));
  const fieldMap = () => new Map(catalog.canonical_fields.map((field) => [field.id, field]));
  const fieldLabel = (id) => local(fieldMap().get(id)?.short_label) || id;
  const schoolFor = (programmeId) => catalog.strong_programmes.find((item) => item.programme_id === programmeId)?.university || programmeId;

  function applyCopy() {
    document.querySelectorAll('[data-copy]').forEach((element) => { element.textContent = t(element.dataset.copy); });
    document.title = lang() === 'tr' ? 'UniRank | Araştırma Uyumu' : 'UniRank | Research Fit';
  }

  function renderStats() {
    const facultyCount = catalog.advisor_guides.reduce((sum, guide) => sum + guide.faculty.length, 0);
    const stats = [
      [catalog.canonical_fields.length, t('canonicalFields'), '⌁'],
      [catalog.strong_programmes.length, t('strongProgrammes'), '◈'],
      [facultyCount, t('facultyMatches'), '◎'],
      [catalog.sources.length, t('officialSources'), '✓']
    ];
    byId('research-stats').innerHTML = stats.map(([number, label, icon]) => `<article class="stat-card"><i>${icon}</i><strong>${number}</strong><span>${escapeHtml(label)}</span></article>`).join('');
  }

  function renderFields() {
    const fields = [{ id: 'all', short_label: { en: 'All fields', tr: 'Tüm alanlar' } }, ...catalog.canonical_fields];
    byId('field-tabs').innerHTML = fields.map((field) => `<button class="field-tab${field.id === selectedField ? ' is-active' : ''}" type="button" data-field="${escapeHtml(field.id)}" aria-pressed="${field.id === selectedField}">${escapeHtml(local(field.short_label))}</button>`).join('');
    byId('field-tabs').querySelectorAll('[data-field]').forEach((button) => button.addEventListener('click', () => {
      selectedField = button.dataset.field;
      renderAll();
      byId('research-programmes').scrollIntoView({ behavior: 'smooth', block: 'start' });
    }));

    const definition = selectedField === 'all' ? null : fieldMap().get(selectedField);
    byId('field-definition').innerHTML = definition
      ? `<div><h3>${escapeHtml(local(definition.label))}</h3><p>${escapeHtml(local(definition.definition))}</p></div><aside><strong>${escapeHtml(t('includes'))}</strong>${escapeHtml(definition.includes.join(' · '))}<strong style="margin-top:12px">${escapeHtml(t('distinctFrom'))}</strong>${escapeHtml(definition.not_the_same_as.map(fieldLabel).join(' · '))}</aside>`
      : `<div><h3>${escapeHtml(t('allFields'))}</h3><p>${escapeHtml(local(catalog.scope))}</p></div><aside><strong>${escapeHtml(t('includes'))}</strong>${escapeHtml(catalog.canonical_fields.map((field) => local(field.short_label)).join(' · '))}</aside>`;
  }

  function filteredProgrammes() {
    return catalog.strong_programmes.filter((programme) => selectedField === 'all' || programme.fit_fields.includes(selectedField));
  }

  // The fee is a build-time copy of the programme database's figure and the
  // check script breaks the build if the two ever disagree, so this page can
  // price the application without loading the full database.
  function feeLine(programme) {
    const fee = programme.application_fee;
    if (!fee || fee.status !== 'published') return '';
    let money;
    try {
      money = new Intl.NumberFormat(lang() === 'tr' ? 'tr-TR' : 'en-GB', {
        style: 'currency', currency: fee.currency, maximumFractionDigits: 0
      }).format(fee.amount);
    } catch { money = `${fee.currency} ${fee.amount}`; }
    const parts = [];
    if (fee.eur_equivalent) parts.push(`≈ €${fee.eur_equivalent}`);
    parts.push(t(fee.charged_per === 'programme_choice' ? 'perProgrammeChoice' : 'perApplication'));
    if (fee.refundable === false) parts.push(t('nonRefundable'));
    // Only the closed waiver is asserted: an "open" flag derived from prose
    // is too weak a claim to print on a card.
    if (fee.waiver_open_to_international === false) parts.push(t('waiverClosedIntl'));
    return `<div class="programme-fee"><span class="research-kicker">${escapeHtml(t('applyFee'))}</span><p><strong>${escapeHtml(money)}</strong> · ${escapeHtml(parts.join(' · '))}</p></div>`;
  }

  function renderProgrammes() {
    const programmes = filteredProgrammes();
    byId('programme-meta').textContent = t('showingProgrammes', { count: programmes.length });
    byId('programme-grid').innerHTML = programmes.length ? programmes.map((programme) => {
      const tierLabel = programme.evidence_tier === 'very_strong' ? t('veryStrong') : t('strong');
      const detailsUrl = `index.html?program=${encodeURIComponent(programme.programme_id)}${selectedField !== 'all' ? `&field=${encodeURIComponent(selectedField)}` : ''}`;
      return `<article class="programme-card">
        <div class="programme-card__top"><div><span class="programme-card__country">${programme.country.flag} ${escapeHtml(local(programme.country))}</span><h3>${escapeHtml(programme.university)}</h3></div><span class="tier-badge${programme.evidence_tier === 'strong' ? ' tier-badge--strong' : ''}">${escapeHtml(tierLabel)}</span></div>
        <div class="field-chips">${programme.fit_fields.map((field) => `<span class="field-chip">${escapeHtml(fieldLabel(field))}</span>`).join('')}</div>
        <div><span class="research-kicker">${escapeHtml(t('whyFit'))}</span><p class="programme-card__why">${escapeHtml(local(programme.why))}</p></div>
        <div class="programme-note"><strong>${escapeHtml(t('practical'))}:</strong> ${escapeHtml(local(programme.practical_note))}</div>
        ${feeLine(programme)}
        <div class="programme-card__actions"><a class="text-link text-link--primary" href="${escapeHtml(programme.official_research_url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(t('officialResearch'))} ↗</a><a class="text-link" href="${detailsUrl}">${escapeHtml(t('programmeDetails'))} →</a></div>
      </article>`;
    }).join('') : `<div class="empty-state">${escapeHtml(t('noMatch'))}</div>`;
  }

  function renderAdvisorGuides() {
    byId('advisor-grid').innerHTML = catalog.advisor_guides.map((guide) => {
      const programme = catalog.strong_programmes.find((item) => item.programme_id === guide.programme_id);
      const afterPolicy = guide.policy === 'contact_after_admission_for_ra';
      const contact = guide.programme_contact;
      return `<article class="advisor-card${afterPolicy ? '' : ' is-during'}">
        <span class="advisor-card__policy">${escapeHtml(t(afterPolicy ? 'policy_after' : 'policy_during'))}</span>
        <h3>${escapeHtml(programme?.university || guide.programme_id)}</h3>
        <div class="advisor-stage"><strong>${escapeHtml(t('beforeApplication'))}</strong><p>${escapeHtml(local(guide.before_application))}</p></div>
        <div class="advisor-stage"><strong>${escapeHtml(t('afterAdmission'))}</strong><p>${escapeHtml(local(guide.after_admission))}</p></div>
        <div class="advisor-contact"><strong>${escapeHtml(t('programmeContact'))}:</strong><a href="${escapeHtml(contact.url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(contact.label)} ↗</a>${contact.email ? `<a href="mailto:${escapeHtml(contact.email)}">${escapeHtml(contact.email)}</a>` : ''}</div>
      </article>`;
    }).join('');
  }

  function renderFaculty() {
    const faculty = catalog.advisor_guides.flatMap((guide) => guide.faculty.map((person) => ({ ...person, programme_id: guide.programme_id })));
    const matches = faculty.filter((person) => selectedField === 'all' || person.fit_fields.includes(selectedField));
    byId('faculty-meta').textContent = t('showingFaculty', { count: matches.length });
    byId('faculty-grid').innerHTML = matches.length ? matches.map((person) => `<article class="faculty-card">
      <div><span class="faculty-card__school">${escapeHtml(schoolFor(person.programme_id))}</span><h3>${escapeHtml(person.name)}</h3><p class="faculty-card__role">${escapeHtml(local(person.role))}</p></div>
      <div class="field-chips">${person.fit_fields.map((field) => `<span class="field-chip">${escapeHtml(fieldLabel(field))}</span>`).join('')}</div>
      <p class="faculty-card__focus">${escapeHtml(local(person.focus))}</p>
      <div class="faculty-card__actions"><a class="text-link text-link--primary" href="${escapeHtml(person.profile_url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(t('officialProfile'))} ↗</a><a class="text-link" href="mailto:${escapeHtml(person.email)}">${escapeHtml(t('email'))}</a></div>
    </article>`).join('') : `<div class="empty-state">${escapeHtml(t('noMatch'))}</div>`;
  }

  function renderOutreach() {
    byId('outreach-subject').textContent = local(catalog.outreach_template.subject);
    byId('outreach-steps').innerHTML = catalog.outreach_template.steps.map((step) => `<li>${escapeHtml(local(step))}</li>`).join('');
    byId('outreach-avoid').innerHTML = `<strong>${escapeHtml(t('avoid'))}:</strong> ${escapeHtml(local(catalog.outreach_template.avoid))}`;
  }

  function renderAll() {
    if (!catalog) return;
    applyCopy();
    renderStats();
    renderFields();
    renderProgrammes();
    renderAdvisorGuides();
    renderFaculty();
    renderOutreach();
    const verifiedText = `${t('verified')}: ${catalog.last_verified}`;
    byId('last-verified').textContent = verifiedText;
    byId('footer-verified').textContent = verifiedText;
    window.updateLanguageToggleUI?.();
  }

  async function init() {
    const response = await fetch('/api/research-pathways', { headers: { Accept: 'application/json' } });
    if (!response.ok) throw new Error(`Research catalog request failed: ${response.status}`);
    const payload = await response.json();
    catalog = payload.data || payload;
    const requestedField = new URLSearchParams(location.search).get('field');
    if (requestedField && catalog.canonical_fields.some((field) => field.id === requestedField)) selectedField = requestedField;
    renderAll();
  }

  document.addEventListener('languageChanged', renderAll);
  init().catch((error) => {
    console.error(error);
    byId('programme-grid').innerHTML = `<div class="empty-state">${escapeHtml(lang() === 'tr' ? 'Araştırma rehberi yüklenemedi.' : 'The research guide could not be loaded.')}</div>`;
  });
})();
