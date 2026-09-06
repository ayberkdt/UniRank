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
      ,labKicker: 'Facilities and access', labTitle: 'What each laboratory actually offers', labText: 'Named equipment and student-access routes are shown only when an official university source states them. Laboratory existence is not a guaranteed place.',
      showingLabs: '{units} research units across {programmes} programmes', featuredProfile: 'Priority profile', facilities: 'Named facilities', studentAccess: 'Student access', labLead: 'Lead', officialLab: 'Official lab page', contactTiming: 'Contact timing', acceptingStudents: 'Accepting-student signal', emailNotPublished: 'Email not published on the checked official profile',
      before_application_encouraged: 'Contact before applying is encouraged', before_application_optional: 'Optional before application', only_with_specific_research_question: 'Only with a specific research question', after_admission_for_ra: 'After admission for RA opportunities', do_not_contact_centralised_admission: 'Centralised admission — do not cold-email', unknown: 'Not stated', stated_open: 'Officially stated open', stated_closed: 'Officially stated closed', not_stated: 'Not stated',
      msc_thesis_open: 'MSc thesis route published', project_course_open: 'Project/course access published', ra_position_only: 'RA/project position only', phd_only: 'PhD only'
      ,showAllProfiles: 'Show all evidence profiles', showPriorityProfiles: 'Show priority universities only'
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
      ,labKicker: 'Tesisler ve erişim', labTitle: 'Her laboratuvar gerçekte ne sunuyor?', labText: 'Adlandırılmış ekipman ve öğrenci erişim rotaları yalnızca resmî üniversite kaynağında yazıyorsa gösterilir. Laboratuvarın varlığı yer garantisi değildir.',
      showingLabs: '{programmes} programda {units} araştırma birimi', featuredProfile: 'Öncelikli profil', facilities: 'Adlandırılmış tesisler', studentAccess: 'Öğrenci erişimi', labLead: 'Yürütücü', officialLab: 'Resmî laboratuvar sayfası', contactTiming: 'İletişim zamanı', acceptingStudents: 'Öğrenci kabul sinyali', emailNotPublished: 'Kontrol edilen resmî profilde e-posta yayımlanmamış',
      before_application_encouraged: 'Başvuru öncesi iletişim teşvik ediliyor', before_application_optional: 'Başvuru öncesi isteğe bağlı', only_with_specific_research_question: 'Yalnızca spesifik araştırma sorusuyla', after_admission_for_ra: 'RA fırsatları için kabulden sonra', do_not_contact_centralised_admission: 'Merkezî kabul — soğuk e-posta gönderme', unknown: 'Belirtilmemiş', stated_open: 'Resmen açık olduğu belirtilmiş', stated_closed: 'Resmen kapalı olduğu belirtilmiş', not_stated: 'Belirtilmemiş',
      msc_thesis_open: 'MSc tez rotası yayımlanmış', project_course_open: 'Proje/ders erişimi yayımlanmış', ra_position_only: 'Yalnızca RA/proje pozisyonu', phd_only: 'Yalnızca doktora'
      ,showAllProfiles: 'Tüm kanıtlı profilleri göster', showPriorityProfiles: 'Yalnızca öncelikli üniversiteleri göster'
    }
  };

  let catalog = null;
  let selectedField = 'all';
  let showAllProfiles = false;
  const byId = (id) => document.getElementById(id);
  const lang = () => window.currentLanguage === 'tr' ? 'tr' : 'en';
  const t = (key, vars = {}) => Object.entries(vars).reduce((value, [name, replacement]) => value.replace(`{${name}}`, replacement), copy[lang()][key] || copy.en[key] || key);
  const local = (value) => value == null ? '' : typeof value === 'string' ? value : value[lang()] || value.en || value.tr || '';
  const escapeHtml = (value) => String(value ?? '').replace(/[&<>'"]/g, (character) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[character]));
  const fieldMap = () => new Map(catalog.canonical_fields.map((field) => [field.id, field]));
  const fieldLabel = (id) => local(fieldMap().get(id)?.short_label) || id;
  const schoolFor = (programmeId) => catalog.strong_programmes.find((item) => item.programme_id === programmeId)?.university || programmeId;
  const researchDetails = () => catalog.programme_research_details || [];

  function applyCopy() {
    document.querySelectorAll('[data-copy]').forEach((element) => { element.textContent = t(element.dataset.copy); });
    document.title = lang() === 'tr' ? 'UniRank | Araştırma Uyumu' : 'UniRank | Research Fit';
  }

  function renderStats() {
    const detailedFacultyCount = researchDetails().reduce((sum, profile) => sum + profile.notable_professors.length, 0);
    const facultyCount = detailedFacultyCount || catalog.advisor_guides.reduce((sum, guide) => sum + guide.faculty.length, 0);
    const stats = [
      [catalog.canonical_fields.length, t('canonicalFields'), '⌁'],
      [catalog.strong_programmes.length, t('strongProgrammes'), '◈'],
      [facultyCount, t('facultyMatches'), '◎'],
      [catalog.official_source_count || catalog.sources.length, t('officialSources'), '✓']
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
    const detailedFaculty = researchDetails().filter((profile) => showAllProfiles || profile.featured).flatMap((profile) => profile.notable_professors.map((person) => ({
      ...person,
      programme_id: profile.programme_id,
      university: profile.university,
      fit_fields: person.fit_tags || [],
      verified_email: Boolean(person.email && person.email_source)
    })));
    const faculty = detailedFaculty.length ? detailedFaculty : catalog.advisor_guides.flatMap((guide) => guide.faculty.map((person) => ({ ...person, programme_id: guide.programme_id, university: schoolFor(guide.programme_id), verified_email: Boolean(person.email) })));
    const matches = faculty.filter((person) => selectedField === 'all' || person.fit_fields.includes(selectedField));
    byId('faculty-meta').textContent = t('showingFaculty', { count: matches.length });
    byId('faculty-grid').innerHTML = matches.length ? matches.map((person) => `<article class="faculty-card">
      <div><span class="faculty-card__school">${escapeHtml(person.university || schoolFor(person.programme_id))}</span><h3>${escapeHtml(person.name)}</h3><p class="faculty-card__role">${escapeHtml(local(person.role))}</p></div>
      <div class="field-chips">${person.fit_fields.map((field) => `<span class="field-chip">${escapeHtml(fieldLabel(field))}</span>`).join('')}</div>
      <p class="faculty-card__focus">${escapeHtml(local(person.focus))}</p>
      ${person.lab ? `<p class="faculty-card__lab">${escapeHtml(person.lab)}</p>` : ''}
      <dl class="faculty-signals"><div><dt>${escapeHtml(t('contactTiming'))}</dt><dd>${escapeHtml(t(person.contact_timing || 'unknown'))}</dd></div><div><dt>${escapeHtml(t('acceptingStudents'))}</dt><dd>${escapeHtml(t(person.accepting_students_signal || 'not_stated'))}</dd></div></dl>
      <div class="faculty-card__actions"><a class="text-link text-link--primary" href="${escapeHtml(person.profile_url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(t('officialProfile'))} ↗</a>${person.verified_email ? `<a class="text-link" href="mailto:${escapeHtml(person.email)}">${escapeHtml(person.email)}</a>` : `<span class="faculty-email-missing">${escapeHtml(t('emailNotPublished'))}</span>`}</div>
    </article>`).join('') : `<div class="empty-state">${escapeHtml(t('noMatch'))}</div>`;
  }

  function renderLabs() {
    const profiles = researchDetails().filter((profile) => showAllProfiles || profile.featured).map((profile) => ({
      ...profile,
      matching_units: profile.research_units.filter((unit) => selectedField === 'all' || (unit.topics || []).includes(selectedField))
    })).filter((profile) => profile.matching_units.length);
    const unitCount = profiles.reduce((sum, profile) => sum + profile.matching_units.length, 0);
    byId('lab-meta').textContent = t('showingLabs', { units: unitCount, programmes: profiles.length });
    byId('lab-grid').innerHTML = profiles.length ? profiles.map((profile) => `<article class="lab-programme${profile.featured ? ' is-featured' : ''}">
      <header><div><span>${escapeHtml(profile.country || '')}</span><h3>${escapeHtml(profile.university)}</h3><p>${escapeHtml(profile.programme)}</p></div>${profile.featured ? `<b>${escapeHtml(t('featuredProfile'))}</b>` : ''}</header>
      ${profile.faculty_contact_note ? `<p class="lab-contact-note">${escapeHtml(local(profile.faculty_contact_note))}</p>` : ''}
      <div class="lab-units">${profile.matching_units.map((unit) => `<details class="lab-unit"><summary><span><strong>${escapeHtml(unit.name)}</strong><small>${escapeHtml(String(unit.unit_type || '').replaceAll('_', ' '))}</small></span><span aria-hidden="true">⌄</span></summary><div class="lab-unit__body">
        <div class="field-chips">${(unit.topics || []).map((topic) => `<span class="field-chip">${escapeHtml(fieldLabel(topic))}</span>`).join('')}</div>
        ${unit.why_it_fits ? `<p>${escapeHtml(local(unit.why_it_fits))}</p>` : ''}
        <dl>${unit.lead ? `<div><dt>${escapeHtml(t('labLead'))}</dt><dd>${escapeHtml(unit.lead)}</dd></div>` : ''}<div><dt>${escapeHtml(t('studentAccess'))}</dt><dd>${escapeHtml(t(unit.student_access || 'not_stated'))}</dd></div></dl>
        ${unit.facilities?.length ? `<section><h4>${escapeHtml(t('facilities'))}</h4><ul>${unit.facilities.map((facility) => `<li>${escapeHtml(typeof facility === 'string' ? facility : local(facility))}</li>`).join('')}</ul></section>` : ''}
        <a class="text-link text-link--primary" href="${escapeHtml(unit.url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(t('officialLab'))} ↗</a>
      </div></details>`).join('')}</div>
      ${profile.faculty_email_availability?.note ? `<p class="lab-email-note">${escapeHtml(local(profile.faculty_email_availability.note))}</p>` : ''}
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
    renderLabs();
    const scopeToggle = byId('research-scope-toggle');
    scopeToggle.textContent = t(showAllProfiles ? 'showPriorityProfiles' : 'showAllProfiles');
    scopeToggle.setAttribute('aria-pressed', String(showAllProfiles));
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
    byId('research-scope-toggle').addEventListener('click', () => { showAllProfiles = !showAllProfiles; renderAll(); });
    renderAll();
  }

  document.addEventListener('languageChanged', renderAll);
  init().catch((error) => {
    console.error(error);
    byId('programme-grid').innerHTML = `<div class="empty-state">${escapeHtml(lang() === 'tr' ? 'Araştırma rehberi yüklenemedi.' : 'The research guide could not be loaded.')}</div>`;
  });
})();
