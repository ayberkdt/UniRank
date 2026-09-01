/**
 * Decision panels for the programme drawer.
 *
 * These panels answer the questions a student actually asks and the old
 * drawer could not: how long is left to apply, which laboratory would take
 * me and why it fits my tagged interests, which professor to write to and
 * when, what I must physically do to win the funding, and — for every
 * ordinal label on the page — which criteria produced that label.
 *
 * Nothing here invents a value.  A panel is omitted when the record has no
 * evidence for it, and a label always renders next to the reason it exists.
 */

(function () {
  const esc = (value) => String(value ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');

  const url = (value) => {
    if (!value) return '';
    try {
      const parsed = new URL(String(value));
      return ['http:', 'https:'].includes(parsed.protocol) ? parsed.href : '';
    } catch {
      return '';
    }
  };

  const text = (value) => (window.localizedValue ? window.localizedValue(value) : (typeof value === 'string' ? value : ''));

  const tr = () => window.currentLanguage === 'tr';

  const pick = (bilingual) => (bilingual ? text(bilingual) : '');

  const std = () => window.uniStandards || null;

  const number = (value) => {
    const parsed = typeof value === 'number' ? value : Number(String(value ?? '').replace(/,/g, ''));
    return Number.isFinite(parsed) ? parsed : null;
  };

  const money = (amount, currency) => {
    const value = number(amount);
    if (value === null) return '—';
    try {
      return new Intl.NumberFormat(tr() ? 'tr-TR' : 'en-GB', {
        style: 'currency',
        currency: currency || 'EUR',
        maximumFractionDigits: 0,
      }).format(value);
    } catch {
      return `${Math.round(value).toLocaleString()} ${currency || ''}`.trim();
    }
  };

  const humanTag = (tag) => (window.getCategoryLabel ? window.getCategoryLabel(tag) : String(tag).replace(/_/g, ' '));

  const section = (modifier, icon, title, body, note) => `
    <div class="drawer-section premium-card decision-panel decision-panel--${modifier}">
      <div class="premium-header">
        <span class="premium-icon decision-panel__icon" aria-hidden="true" data-glyph="${icon}"></span>
        <h4 class="premium-title">${esc(title)}</h4>
      </div>
      ${note ? `<p class="card-disclaimer">${esc(note)}</p>` : ''}
      ${body}
    </div>`;

  const disclosure = (summary, body) => `
    <details class="decision-disclosure">
      <summary>${esc(summary)}</summary>
      <div class="decision-disclosure__body">${body}</div>
    </details>`;

  const sourceLink = (href, label) => {
    const safe = url(href);
    if (!safe) return '';
    return `<a class="decision-source-link" href="${esc(safe)}" target="_blank" rel="noopener noreferrer">${esc(label || (tr() ? 'Kaynak' : 'Source'))} ↗</a>`;
  };

  // ---------------------------------------------------------------- countdown

  const COUNTDOWN_STATUS = {
    open: { tr: 'Başvurular açık', en: 'Applications open' },
    closing_soon: { tr: 'Son günler', en: 'Closing soon' },
    closed: { tr: 'Bu dönem kapandı', en: 'Closed for this cycle' },
    rolling: { tr: 'Sürekli başvuru', en: 'Rolling admission' },
    not_published: { tr: 'Tarih yayımlanmamış', en: 'No published date' },
  };

  const AUDIENCE = {
    all_applicants: { tr: 'Tüm adaylar', en: 'All applicants' },
    non_eu: { tr: 'AB dışı adaylar', en: 'Non-EU applicants' },
    eu_eea: { tr: 'AB/AEA adayları', en: 'EU/EEA applicants' },
    international: { tr: 'Uluslararası adaylar', en: 'International applicants' },
    scholarship_track: { tr: 'Burs rotası', en: 'Scholarship track' },
  };

  function daysBetween(iso) {
    const target = new Date(`${iso}T23:59:59`);
    if (Number.isNaN(target.getTime())) return null;
    const now = new Date();
    return Math.ceil((target - now) / 86400000);
  }

  function countdownPanel(record) {
    const timeline = record.application_timeline_profile || {};
    const primary = timeline.primary_deadline;
    if (!primary) return '';

    const turkish = tr();
    const status = primary.status || 'not_published';
    const statusLabel = (COUNTDOWN_STATUS[status] || COUNTDOWN_STATUS.not_published)[turkish ? 'tr' : 'en'];

    if (!primary.date) {
      const body = `
        <div class="countdown">
          <div class="countdown__figure countdown__figure--muted"><span class="countdown__value">—</span></div>
          <div class="countdown__detail">
            <span class="deadline-chip deadline-chip--not_published">${esc(statusLabel)}</span>
            <p>${esc(turkish
              ? 'Bu kayıt için resmî bir başvuru tarihi doğrulanmadı. Tarih uydurmak yerine boş bırakıldı — programın kendi sayfasından teyit et.'
              : 'No official application date has been verified for this record. It is left blank rather than invented — confirm it on the programme page.')}</p>
          </div>
        </div>`;
      return section('countdown', '⏳', turkish ? 'Başvuruya kalan süre' : 'Time left to apply', body);
    }

    const live = daysBetween(primary.date);
    const isPast = live !== null && live < 0;
    const shownDays = live === null ? null : Math.abs(live);
    const figureModifier = isPast ? 'past' : live !== null && live <= 30 ? 'urgent' : 'open';

    const meta = [
      primary.time ? `${esc(primary.time)}${primary.timezone ? ` ${esc(primary.timezone)}` : ''}` : '',
      primary.applies_to ? esc((AUDIENCE[primary.applies_to] || { tr: primary.applies_to, en: primary.applies_to })[turkish ? 'tr' : 'en']) : '',
      primary.cycle_label ? esc(text(primary.cycle_label)) : '',
    ].filter(Boolean);

    const nextLine = isPast && primary.next_expected_date
      ? `<p class="countdown__next">${esc(turkish ? 'Aynı takvim tekrar ediyor; beklenen sonraki tarih: ' : 'The same calendar repeats; next expected date: ')}<strong>${esc(primary.next_expected_date)}</strong></p>`
      : '';

    const notes = timeline.deadline_notes ? `<p class="countdown__note">${esc(pick(timeline.deadline_notes))}</p>` : '';

    const body = `
      <div class="countdown">
        <div class="countdown__figure countdown__figure--${figureModifier}">
          <span class="countdown__value">${shownDays === null ? '—' : esc(String(shownDays))}</span>
          <span class="countdown__unit">${esc(turkish ? (isPast ? 'gün önce kapandı' : 'gün kaldı') : (isPast ? 'days ago' : 'days left'))}</span>
        </div>
        <div class="countdown__detail">
          <span class="deadline-chip deadline-chip--${esc(status)}">${esc(statusLabel)}</span>
          <p class="countdown__date"><strong>${esc(primary.date)}</strong>${meta.length ? ` · ${meta.join(' · ')}` : ''}</p>
          ${nextLine}
          ${notes}
          <p class="countdown__provenance">
            ${esc(turkish ? 'Güven: ' : 'Confidence: ')}${esc(primary.confidence || 'unknown')}
            ${sourceLink(primary.source_url, turkish ? 'Resmî sayfa' : 'Official page')}
          </p>
        </div>
      </div>`;

    return section('countdown', '⏳', turkish ? 'Başvuruya kalan süre' : 'Time left to apply', body);
  }

  // ----------------------------------------------------------- academic match

  const MATCH_LEVEL_LABEL = {
    strong: { tr: 'Güçlü', en: 'Strong' },
    moderate: { tr: 'Orta', en: 'Moderate' },
    weak: { tr: 'Zayıf', en: 'Weak' },
    none: { tr: 'Yok', en: 'None' },
    unknown: { tr: 'Doğrulanmadı', en: 'Not verified' },
  };

  function academicMatchPanel(record) {
    const profile = record.academic_match_profile;
    if (!profile) return '';
    const turkish = tr();
    const tier = std()?.matchTier(profile.tier);
    const tierLabel = tier ? pick(tier.label) : (turkish ? 'Bilinmiyor' : 'Unknown');

    const rows = Object.entries(profile.dimensions || {}).map(([key, entry]) => {
      const spec = std()?.matchDimension(key);
      const question = spec ? pick(spec.question) : key.replace(/_/g, ' ');
      const level = entry.level || 'unknown';
      const label = (MATCH_LEVEL_LABEL[level] || MATCH_LEVEL_LABEL.unknown)[turkish ? 'tr' : 'en'];
      const basis = entry.basis ? String(entry.basis).replace(/_/g, ' ') : '';
      return `
        <li class="match-dimension match-dimension--${esc(level)}">
          <div class="match-dimension__head">
            <span class="match-dimension__question">${esc(question)}</span>
            <span class="match-level match-level--${esc(level)}">${esc(label)}</span>
          </div>
          <div class="match-dimension__meta">
            <span class="match-dimension__weight">${esc(turkish ? 'ağırlık' : 'weight')} ${esc(String(entry.weight ?? ''))}</span>
            ${basis ? `<span class="match-dimension__basis">${esc(basis)}</span>` : ''}
            ${sourceLink(entry.source_url, turkish ? 'kanıt' : 'evidence')}
          </div>
        </li>`;
    }).join('');

    const tags = (profile.matched_tags || []).slice(0, 12)
      .map((tag) => `<span class="lab-chip">${esc(humanTag(tag))}</span>`).join('');

    const scoreBlock = profile.score === null || profile.score === undefined
      ? `<div class="match-score match-score--unknown"><span>—</span><small>${esc(turkish ? 'yayımlanmadı' : 'not published')}</small></div>`
      : `<div class="match-score"><span>${esc(String(profile.score))}</span><small>/100</small></div>`;

    const explanation = std()?.all().academic_match?.why_stronger_categories_were_needed;
    const rule = std()?.all().academic_match?.publication_rule;

    const body = `
      <div class="match-header">
        ${scoreBlock}
        <div class="match-header__text">
          <span class="match-tier match-tier--${esc(profile.tier || 'unknown')}">${esc(tierLabel)}</span>
          <p>${esc(turkish
            ? `${profile.evidenced_dimensions}/5 boyut resmî kaynakla doğrulandı. Puan, doğrulanan boyutların ağırlıkları üzerinden normalize edilir; doğrulanmayan boyut puanı ne yükseltir ne düşürür.`
            : `${profile.evidenced_dimensions} of 5 dimensions are backed by an official source. The score is normalised over the weights of the evidenced dimensions, so an unverified dimension neither raises nor lowers it.`)}</p>
        </div>
      </div>
      <ul class="match-dimension-list">${rows}</ul>
      ${tags ? `<div class="dept-block"><label>${esc(turkish ? 'Eşleşen teknik etiketler' : 'Matched technical tags')}</label><div class="chip-container">${tags}</div></div>` : ''}
      ${explanation ? disclosure(
        turkish ? 'Bu kategoriler neye göre belirlendi?' : 'What produced these categories?',
        `<p>${esc(pick(explanation))}</p>${rule ? `<p>${esc(pick(rule))}</p>` : ''}`
      ) : ''}`;

    return section('match', '◎', turkish ? 'Akademik uyum analizi' : 'Academic match analysis', body);
  }

  // ------------------------------------------------------------ research units

  const UNIT_TYPE = {
    laboratory: { tr: 'Laboratuvar', en: 'Laboratory' },
    research_group: { tr: 'Araştırma grubu', en: 'Research group' },
    chair: { tr: 'Kürsü', en: 'Chair' },
    institute: { tr: 'Enstitü', en: 'Institute' },
    centre: { tr: 'Merkez', en: 'Centre' },
    facility: { tr: 'Tesis', en: 'Facility' },
    consortium: { tr: 'Konsorsiyum', en: 'Consortium' },
  };

  const UNIT_ACCESS = {
    msc_thesis_open: { tr: 'Yüksek lisans tezine açık', en: 'Open to MSc theses' },
    project_course_open: { tr: 'Proje dersine açık', en: 'Open via project courses' },
    ra_position_only: { tr: 'Yalnızca RA pozisyonuyla', en: 'Through an RA position only' },
    phd_only: { tr: 'Yalnızca doktora', en: 'PhD only' },
    not_stated: { tr: 'Erişim koşulu belirtilmemiş', en: 'Access not stated' },
  };

  function researchUnitsPanel(record) {
    const units = (record.research_profile || {}).research_units;
    if (!Array.isArray(units) || !units.length) return '';
    const turkish = tr();

    const cards = units.map((unit) => {
      const topics = (unit.topics || []).map((topic) => `<span class="lab-chip">${esc(humanTag(topic))}</span>`).join('');
      const facilities = (unit.facilities || []).map((facility) => `<li>${esc(text(facility) || facility)}</li>`).join('');
      const projects = (unit.named_projects || []).map((project) => `<span class="unit-project">${esc(text(project) || project)}</span>`).join('');
      const areas = (unit.stated_research_areas || []).map((area) => `<li>${esc(text(area) || area)}</li>`).join('');
      const typeLabel = (UNIT_TYPE[unit.unit_type] || { tr: unit.unit_type, en: unit.unit_type })[turkish ? 'tr' : 'en'];
      const accessLabel = (UNIT_ACCESS[unit.student_access] || UNIT_ACCESS.not_stated)[turkish ? 'tr' : 'en'];
      const fit = pick(unit.why_it_fits);

      return `
        <article class="unit-card">
          <div class="unit-card__top">
            <div>
              <strong class="unit-card__name">${esc(unit.name)}</strong>
              <span class="unit-card__type">${esc(typeLabel || '')}</span>
            </div>
            ${sourceLink(unit.url, turkish ? 'Resmî sayfa' : 'Official page')}
          </div>
          ${unit.lead ? `<p class="unit-card__lead">${esc(turkish ? 'Yürütücü: ' : 'Lead: ')}${esc(unit.lead)}</p>` : ''}
          ${topics ? `<div class="chip-container">${topics}</div>` : ''}
          ${fit ? `<div class="unit-card__fit"><span class="unit-card__fit-label">${esc(turkish ? 'Sana neden uygun?' : 'Why this fits you')}</span><p>${esc(fit)}</p></div>` : ''}
          ${areas ? `<div class="unit-card__list"><label>${esc(turkish ? 'İlan edilmiş araştırma alanları' : 'Stated research areas')}</label><ul>${areas}</ul></div>` : ''}
          ${facilities ? `<div class="unit-card__list"><label>${esc(turkish ? 'Tesisler' : 'Facilities')}</label><ul>${facilities}</ul></div>` : ''}
          ${projects ? `<div class="unit-card__projects">${projects}</div>` : ''}
          <div class="unit-card__foot"><span class="unit-access">${esc(accessLabel)}</span>${unit.last_verified ? `<span class="unit-verified">${esc(turkish ? 'doğrulandı ' : 'verified ')}${esc(unit.last_verified)}</span>` : ''}</div>
        </article>`;
    }).join('');

    const note = turkish
      ? 'Her birim resmî bölüm veya laboratuvar sayfasından alınmıştır. "Sana neden uygun?" açıklaması, birimin somut faaliyetini senin teknik etiketlerinle eşleştirir; tanıtım metni değildir.'
      : 'Every unit comes from an official department or laboratory page. The "why this fits you" note matches a concrete activity of the unit to your technical tags; it is not marketing copy.';

    return section('units', '⌬', turkish ? 'Laboratuvarlar ve araştırma grupları' : 'Laboratories and research groups', `<div class="unit-grid">${cards}</div>`, note);
  }

  // ------------------------------------------------------------------ faculty

  function facultyPanel(record) {
    const research = record.research_profile || {};
    const people = research.notable_professors;
    if (!Array.isArray(people) || !people.length) return '';
    const turkish = tr();

    const cards = people.map((person) => {
      const timing = std()?.contactTiming(person.contact_timing);
      const timingLabel = timing ? pick(timing.label) : '';
      const timingGuidance = timing ? pick(timing.guidance) : '';
      const tags = (person.fit_tags || []).map((tag) => `<span class="prof-fit-tag">${esc(humanTag(tag))}</span>`).join('');
      const mail = person.email ? esc(person.email) : '';

      const contactRow = mail
        ? `<a class="prof-mail" href="mailto:${mail}">${mail}</a>
           <button type="button" class="prof-copy" data-copy-email="${mail}">${esc(turkish ? 'kopyala' : 'copy')}</button>
           ${sourceLink(person.email_source, turkish ? 'adresin kaynağı' : 'address source')}`
        : `<span class="prof-mail prof-mail--missing">${esc(turkish ? 'Resmî sayfada e-posta yayımlanmamış' : 'No email published on an official page')}</span>`;

      return `
        <article class="prof-card prof-card--rich">
          <div class="prof-card__top">
            <div>
              <strong class="prof-name">${esc(person.name)}</strong>
              ${person.role ? `<span class="prof-role">${esc(pick(person.role))}</span>` : ''}
            </div>
            ${sourceLink(person.profile_url, turkish ? 'Profil' : 'Profile')}
          </div>
          ${person.focus ? `<p class="prof-focus">${esc(pick(person.focus))}</p>` : ''}
          ${tags ? `<div class="prof-fit-tags">${tags}</div>` : ''}
          ${person.lab ? `<p class="prof-lab">${esc(turkish ? 'Birim: ' : 'Unit: ')}${esc(person.lab)}</p>` : ''}
          <div class="prof-card__contact">${contactRow}${person.phone ? `<span class="prof-phone">${esc(person.phone)}</span>` : ''}</div>
          ${person.email_note ? `<p class="prof-email-note">${esc(pick(person.email_note))}</p>` : ''}
          ${timingLabel ? `<div class="prof-timing"><span class="prof-timing__chip">${esc(timingLabel)}</span>${timingGuidance ? `<p>${esc(timingGuidance)}</p>` : ''}</div>` : ''}
        </article>`;
    }).join('');

    const policyNote = research.faculty_contact_note ? `<p class="faculty-contact-note"><strong>${esc(turkish ? 'Ne zaman yazmalı?' : 'When should you write?')}</strong>${esc(pick(research.faculty_contact_note))}</p>` : '';
    const availability = research.faculty_email_availability?.note
      ? `<p class="card-footnote">${esc(pick(research.faculty_email_availability.note))}</p>`
      : '';

    const emailRule = std()?.all().faculty_contact?.email_rule;
    const body = `
      ${policyNote}
      <div class="prof-grid">${cards}</div>
      ${availability}
      ${emailRule ? disclosure(turkish ? 'E-posta adresleri nereden geliyor?' : 'Where do these email addresses come from?', `<p>${esc(pick(emailRule))}</p>`) : ''}`;

    return section('faculty', '✉', turkish ? 'Hoca bağlantıları' : 'Faculty contacts', body);
  }

  // ------------------------------------------------------- scholarship playbook

  const COMPETITIVENESS = {
    open_to_all_eligible: { tr: 'Uygun olan herkese açık', en: 'Open to all eligible' },
    selective: { tr: 'Seçici', en: 'Selective' },
    highly_selective: { tr: 'Çok seçici', en: 'Highly selective' },
    unknown: { tr: 'Bilinmiyor', en: 'Unknown' },
  };

  const OWNER = {
    applicant: { tr: 'Sen', en: 'You' },
    university: { tr: 'Üniversite', en: 'University' },
    external_body: { tr: 'Dış kurum', en: 'External body' },
  };

  function scholarshipPlaybookPanel(record) {
    const playbook = (record.scholarship_profile || {}).playbook;
    if (!Array.isArray(playbook) || !playbook.length) return '';
    const turkish = tr();

    const blocks = playbook.map((entry) => {
      const gates = (entry.eligibility_gates || []).map((gate) => `<li>${esc(pick(gate))}</li>`).join('');
      const criteria = (entry.selection_criteria || []).map((item) => `<li>${esc(pick(item))}</li>`).join('');
      const steps = (entry.steps || []).slice().sort((a, b) => (a.order || 0) - (b.order || 0)).map((step) => {
        const timing = std()?.stepTiming(step.timing);
        const timingLabel = timing ? pick(timing.label) : String(step.timing || '').replace(/_/g, ' ');
        const owner = (OWNER[step.owner] || { tr: step.owner, en: step.owner })[turkish ? 'tr' : 'en'];
        const docs = (step.required_documents || []).map((doc) => `<li>${esc(pick(doc))}</li>`).join('');
        return `
          <li class="playbook-step${step.hard_requirement ? ' playbook-step--required' : ''}">
            <span class="playbook-step__order">${esc(String(step.order ?? ''))}</span>
            <div class="playbook-step__body">
              <p class="playbook-step__action">${esc(pick(step.action))}</p>
              <div class="playbook-step__meta">
                <span class="playbook-chip playbook-chip--timing">${esc(timingLabel)}</span>
                ${owner ? `<span class="playbook-chip">${esc(owner)}</span>` : ''}
                ${step.hard_requirement ? `<span class="playbook-chip playbook-chip--required">${esc(turkish ? 'atlanırsa elenirsin' : 'skipping disqualifies')}</span>` : ''}
              </div>
              ${docs ? `<div class="playbook-docs"><label>${esc(turkish ? 'Gereken belgeler' : 'Required documents')}</label><ul>${docs}</ul></div>` : ''}
            </div>
          </li>`;
      }).join('');

      const award = entry.typical_award || {};
      const coverage = (award.coverage || []).map((item) => `<span class="lab-chip">${esc(String(item).replace(/_/g, ' '))}</span>`).join('');
      const competitiveness = (COMPETITIVENESS[entry.competitiveness] || COMPETITIVENESS.unknown)[turkish ? 'tr' : 'en'];

      return `
        <article class="playbook-card">
          <div class="playbook-card__top">
            <strong>${esc(entry.opportunity)}</strong>
            <span class="playbook-competitiveness playbook-competitiveness--${esc(entry.competitiveness || 'unknown')}">${esc(competitiveness)}</span>
          </div>
          ${coverage ? `<div class="chip-container">${coverage}</div>` : ''}
          ${award.amount_note ? `<p class="playbook-amount">${esc(pick(award.amount_note))}</p>` : ''}
          ${entry.award_count_note ? `<p class="playbook-amount">${esc(pick(entry.award_count_note))}</p>` : ''}
          ${gates ? `<div class="playbook-block"><label>${esc(turkish ? 'Karşılanmazsa elenirsin' : 'Fail one of these and you are out')}</label><ul class="clean-list">${gates}</ul></div>` : ''}
          ${criteria ? `<div class="playbook-block"><label>${esc(turkish ? 'Komite neyi puanlıyor?' : 'What the committee scores')}</label><ul class="clean-list">${criteria}</ul></div>` : ''}
          ${steps ? `<ol class="playbook-steps">${steps}</ol>` : ''}
          ${entry.renewal_conditions ? `<p class="playbook-renewal">${esc(turkish ? 'Yenileme: ' : 'Renewal: ')}${esc(text(entry.renewal_conditions) || entry.renewal_conditions)}</p>` : ''}
          ${sourceLink(entry.evidence_url, turkish ? 'Resmî burs sayfası' : 'Official scholarship page')}
        </article>`;
    }).join('');

    const notes = (record.scholarship_profile || {}).funding_notes;
    const honesty = std()?.all().scholarship_playbook?.honesty_rule;

    const body = `
      ${notes ? `<p class="playbook-intro">${esc(pick(notes))}</p>` : ''}
      <div class="playbook-grid">${blocks}</div>
      ${honesty ? disclosure(turkish ? 'Bu adımlar nereden geliyor?' : 'Where do these steps come from?', `<p>${esc(pick(honesty))}</p>`) : ''}`;

    return section('playbook', '◈', turkish ? 'Bursu almak için ne yapmalısın?' : 'What to do to win the funding', body);
  }

  // ---------------------------------------------------------- housing rubric

  function housingRubricPanel(record) {
    const profile = (record.living_profile || {}).housing_difficulty_profile;
    if (!profile) return '';
    const turkish = tr();
    const level = std()?.housingLevel(profile.level);
    const levelLabel = level ? pick(level.label) : profile.level;
    const criteria = level ? pick(level.criteria) : '';

    const rows = Object.entries(profile.dimensions || {}).map(([key, entry]) => {
      const spec = std()?.housingDimension(key);
      const question = spec ? pick(spec.question) : key.replace(/_/g, ' ');
      const known = entry.value !== null && entry.value !== undefined;
      const defined = known && spec && spec.values ? spec.values[entry.value] : null;
      const valueLabel = known
        ? (defined && defined.label ? pick(defined.label) : String(entry.value).replace(/_/g, ' '))
        : (turkish ? 'yayımlanmamış' : 'not published');
      const maxPoints = spec ? spec.weight_max : null;
      return `
        <li class="housing-dimension${known ? '' : ' housing-dimension--unknown'}">
          <div class="housing-dimension__head">
            <span>${esc(question)}</span>
            <span class="housing-dimension__points">${known ? `${esc(String(entry.points))}${maxPoints !== null ? `/${esc(String(maxPoints))}` : ''}` : '—'}</span>
          </div>
          <p class="housing-dimension__value">${esc(valueLabel)}</p>
          ${entry.evidence_quote ? `<blockquote class="housing-quote"><span class="housing-quote__label">${esc(turkish ? 'Resmî sayfadan alıntı' : 'Quoted from the official page')}</span>${esc(entry.evidence_quote)}</blockquote>` : ''}
          ${sourceLink(entry.derived_from, turkish ? 'kanıt' : 'evidence')}
        </li>`;
    }).join('');

    const scale = std()?.all().housing_difficulty;
    const scorePct = profile.scaled_score === null || profile.scaled_score === undefined
      ? 0
      : Math.round((profile.scaled_score / (profile.score_max || 15)) * 100);

    const body = `
      <div class="housing-header">
        <span class="housing-level housing-level--${esc(profile.level)}">${esc(levelLabel)}</span>
        <div class="housing-meter" role="img" aria-label="${esc(String(profile.scaled_score ?? '—'))} / ${esc(String(profile.score_max))}">
          <div class="housing-meter__fill housing-meter__fill--${esc(profile.level)}" style="width:${scorePct}%"></div>
        </div>
        <span class="housing-score">${esc(profile.scaled_score === null || profile.scaled_score === undefined ? '—' : String(profile.scaled_score))}<small>/${esc(String(profile.score_max))}</small></span>
      </div>
      ${criteria ? `<p class="housing-criteria">${esc(criteria)}</p>` : ''}
      ${profile.capped_from_very_high ? `<p class="housing-cap">${esc(turkish
        ? `Puan (${profile.scaled_score}/${profile.score_max}) "çok yüksek" bandına düşüyor, ancak o bandın yazılı ölçütü — uluslararası öğrencilerin çoğunun barındırılamadığına dair resmî ifade ya da sözleşmesiz gelmeme uyarısı — bu kayıtta belgelenmemiş. Bu yüzden seviye "yüksek" ile sınırlandırıldı: aritmetik tek başına en üst bandı üretemez.`
        : `The score (${profile.scaled_score}/${profile.score_max}) falls in the "very high" band, but that band's written criterion — an official statement that most internationals cannot be housed, or advice not to travel without a contract — is not documented on this record. The level is therefore capped at "high": arithmetic alone cannot reach the top band.`)}</p>` : ''}
      <p class="housing-coverage">${esc(turkish
        ? `${profile.evidenced_dimensions}/5 ölçüt resmî kaynakla dolduruldu (yayım için en az ${profile.dimensions_required_for_publication} gerekir). Güven: ${profile.confidence}.`
        : `${profile.evidenced_dimensions} of 5 criteria are backed by an official source (at least ${profile.dimensions_required_for_publication} are required to publish a level). Confidence: ${profile.confidence}.`)}</p>
      <ul class="housing-dimension-list">${rows}</ul>
      ${scale ? disclosure(
        turkish ? 'Bu kategoriler neye göre seçildi?' : 'How was this category chosen?',
        `<p>${esc(pick(scale.why_previous_options_were_incomplete))}</p>
         <p>${esc(pick(scale.scoring_rule))}</p>
         <p>${esc(pick(scale.forbidden_inference))}</p>`
      ) : ''}`;

    return section('housing', '⌂', turkish ? 'Konaklama zorluğu — nasıl hesaplandı' : 'Housing difficulty — how it was scored', body);
  }

  // ------------------------------------------------------------ cost breakdown

  function costBreakdownPanel(record) {
    const living = record.living_profile || {};
    const cost = record.cost_profile || {};
    const col = living.cost_of_living_profile;
    const normalized = cost.normalized_cost;
    if (!col && !normalized) return '';
    const turkish = tr();

    let basisBlock = '';
    if (col) {
      const basis = std()?.costBasis(col.cost_basis);
      const basisLabel = basis ? pick(basis.label) : String(col.cost_basis || '').replace(/_/g, ' ');
      const basisNote = basis && basis.note ? pick(basis.note) : '';
      basisBlock = `
        <div class="cost-basis">
          <span class="cost-basis__chip cost-basis__chip--${esc(basis ? basis.reliability : 'unknown')}">${esc(basisLabel)}</span>
          ${basisNote ? `<p>${esc(basisNote)}</p>` : ''}
          ${col.note ? `<p class="cost-basis__note">${esc(pick(col.note))}</p>` : ''}
          ${sourceLink(col.source_url, turkish ? 'Resmî kaynak' : 'Official source')}
        </div>`;
    }

    const componentRows = col && col.components
      ? Object.entries(col.components).map(([key, entry]) => {
        const spec = std()?.costComponent(key);
        const label = spec ? pick(spec.label) : key.replace(/_/g, ' ');
        return `<li><span>${esc(label)}</span><strong>${esc(money(entry.monthly_amount, entry.currency || col.currency))}</strong></li>`;
      }).join('')
      : '';

    const missing = col && (col.mandatory_components_missing || []).length
      ? `<p class="cost-missing">${esc(turkish ? 'Resmî kaynakta bulunmayan zorunlu kalemler: ' : 'Mandatory components the official source does not publish: ')}${esc((col.mandatory_components_missing || []).map((key) => {
        const spec = std()?.costComponent(key);
        return spec ? pick(spec.label) : key.replace(/_/g, ' ');
      }).join(', '))}</p>`
      : '';

    const monthlyBlock = col && col.monthly_total !== null && col.monthly_total !== undefined
      ? `<div class="cost-headline">
           <span class="cost-headline__value">${esc(money(col.monthly_total, col.currency))}</span>
           <span class="cost-headline__unit">${esc(turkish ? '/ ay' : '/ month')}</span>
           <span class="cost-headline__scope">${esc(turkish ? `${col.months_covered} aylık dönem üzerinden` : `over a ${col.months_covered}-month period`)}</span>
         </div>`
      : '';

    const totalBlock = normalized && normalized.annual_total
      ? `<div class="cost-total">
           <div>
             <span class="cost-total__label">${esc(turkish ? 'Yıllık toplam' : 'Annual total')}</span>
             <strong>${esc(money(normalized.annual_total, normalized.currency))}</strong>
             ${normalized.annual_total_eur_equivalent ? `<em>≈ ${esc(money(normalized.annual_total_eur_equivalent.amount, 'EUR'))} · ${esc(turkish ? 'çevrim' : 'converted')} ${esc(normalized.annual_total_eur_equivalent.fx_rate_date)}</em>` : ''}
           </div>
           <ul class="cost-total__includes">${(normalized.includes || []).map((item) => `<li>${esc(String(item).replace(/_/g, ' '))}</li>`).join('')}</ul>
         </div>`
      : normalized
        ? `<p class="cost-missing">${esc(turkish
          ? `Yıllık toplam yayımlanmadı çünkü şu zorunlu bileşen doğrulanmadı: ${(normalized.missing_mandatory_components || []).join(', ')}. Uydurma toplam yerine parçalar ayrı gösteriliyor.`
          : `No annual total is published because these mandatory components are unverified: ${(normalized.missing_mandatory_components || []).join(', ')}. The parts are shown separately instead of an invented sum.`)}</p>`
        : '';

    const excludes = col && (col.excludes || []).length
      ? `<p class="cost-excludes">${esc(turkish ? 'Bu rakama dâhil değil: ' : 'Not included in this figure: ')}${esc((col.excludes || []).map((item) => String(item).replace(/_/g, ' ')).join(', '))}</p>`
      : '';

    const method = std()?.all().cost_model;

    const body = `
      ${monthlyBlock}
      ${basisBlock}
      ${componentRows ? `<ul class="cost-component-list">${componentRows}</ul>` : ''}
      ${missing}
      ${excludes}
      ${totalBlock}
      ${method ? disclosure(
        turkish ? 'Ortalama giderler nasıl hesaplandı?' : 'How were the average expenses calculated?',
        `<p>${esc(pick(method.why_previous_values_were_unreliable))}</p>
         <p>${esc(pick(method.period_rule))}</p>
         <p>${esc(pick(method.total_rule))}</p>
         <p>${esc(pick(method.fx_rule))}</p>`
      ) : ''}`;

    return section('cost', '₪', turkish ? 'Ortalama giderler — dayanağıyla' : 'Average expenses — with their basis', body);
  }

  // -------------------------------------------------------- application fee

  const FEE_STATUS_TONE = {
    published: 'charged',
    no_fee: 'free',
    not_published: 'free',
    unknown: 'unverified',
  };

  function applicationFeePanel(record) {
    const helper = window.uniApplicationFee;
    const fee = helper ? helper.read(record) : null;
    if (!fee) return '';
    const turkish = tr();
    const spec = std()?.all().application_fee;
    const statusSpec = (spec?.status_values || []).find((entry) => entry.code === fee.status);

    const qualifiers = helper.qualifiers(fee);
    const waiver = helper.waiverLine(fee);
    const early = helper.earlyWindow(fee);
    const verification = record.cost_profile?.application_fee_verification;
    const pages = Array.isArray(fee.pages_checked) ? fee.pages_checked : [];
    const refused = Array.isArray(fee.refused_items) ? fee.refused_items : [];

    const headline = `
      <div class="fee-headline fee-headline--${esc(FEE_STATUS_TONE[fee.status] || 'unverified')}">
        <span class="fee-headline__value">${esc(helper.headline(fee))}</span>
        ${statusSpec ? `<span class="fee-headline__status">${esc(pick(statusSpec.label))}</span>` : ''}
        ${qualifiers.length ? `<span class="fee-headline__qualifiers">${esc(qualifiers.join(' · '))}</span>` : ''}
      </div>`;

    // An early window is a deadline with a price on it, so it gets the same
    // visual weight as a countdown rather than a footnote.
    const earlyBlock = early
      ? `<div class="fee-early${early.open ? ' fee-early--open' : ''}">
           <span class="fee-early__label">${esc(early.open
             ? (turkish ? 'Erken başvuru penceresi açık' : 'Early window still open')
             : (turkish ? 'Yayımlanan dönemin erken penceresi' : 'The published cycle’s early window'))}</span>
           <strong>${esc(early.label)}</strong>
           ${early.open ? `<em>${esc(early.savingLabel)}</em>` : ''}
         </div>`
      : '';

    const waiverBlock = waiver
      ? `<div class="fee-waiver">
           <span class="fee-waiver__label">${esc(turkish ? 'Ücret muafiyeti' : 'Fee waiver')}</span>
           <p>${esc(waiver)}</p>
           ${fee.waiver && fee.waiver.note ? `<p class="fee-waiver__note">${esc(helper.localized(fee.waiver.note))}</p>` : ''}
           ${fee.waiver && Array.isArray(fee.waiver.categories) && fee.waiver.categories.length
             ? `<ul class="fee-waiver__categories">${fee.waiver.categories.map((item) => `<li>${esc(text(item) || String(item))}</li>`).join('')}</ul>`
             : ''}
         </div>`
      : '';

    const componentRows = Array.isArray(fee.components) && fee.components.length
      ? `<ul class="fee-component-list">${fee.components.map((item) => `<li><span>${esc(text(item.label) || String(item.label || '').replace(/_/g, ' '))}</span><strong>${esc(money(item.amount, item.currency))}</strong></li>`).join('')}</ul>`
      : '';

    const noteBlock = fee.note && fee.status === 'not_published'
      ? `<p class="fee-note">${esc(helper.localized(fee.note))}</p>`
      : '';

    const verificationBlock = verification && verification.note
      ? `<p class="fee-note fee-note--verification">${esc(helper.localized(verification.note))}${verification.confidence && verification.confidence !== 'high'
        ? ` <span class="fee-confidence fee-confidence--${esc(verification.confidence)}">${esc(turkish ? 'orta güven' : 'medium confidence')}</span>`
        : ''}</p>`
      : '';

    const pagesBlock = pages.length
      ? `<p class="fee-pages">${esc(turkish ? 'Okunan sayfalar' : 'Pages read')}${fee.checked_on ? ` · ${esc(fee.checked_on)}` : ''}: ${pages.map((page, index) => sourceLink(page, `${turkish ? 'sayfa' : 'page'} ${index + 1}`)).join(' ')}</p>`
      : '';

    // Where every published fee names a route this reader cannot use, saying
    // which routes were priced is more useful than an empty field.
    const refusedBlock = refused.length
      ? `<div class="fee-refused">
           <p>${esc(turkish
             ? 'Yayımlanan ücretler AB dışı bir adayın kullanamayacağı yollara ait:'
             : 'The published fees are for routes a non-EU applicant cannot use:')}</p>
           <ul>${refused.map((item) => `<li><strong>${esc(money(item.amount, item.currency))}</strong> — ${esc(text(item.basis) || String(item.applicant_scope || '').replace(/_/g, ' '))}</li>`).join('')}</ul>
         </div>`
      : '';

    const method = spec
      ? disclosure(
        turkish ? 'Bu rakam nasıl belirlendi?' : 'How was this figure decided?',
        `<p>${esc(pick(spec.total_rule))}</p>
         <p>${esc(pick(spec.forbidden_promotions))}</p>
         ${spec.who_charges_it ? `<p>${esc(pick(spec.who_charges_it))}</p>` : ''}
         ${statusSpec && statusSpec.note ? `<p>${esc(pick(statusSpec.note))}</p>` : ''}`
      )
      : '';

    const body = `
      ${headline}
      ${componentRows}
      ${earlyBlock}
      ${waiverBlock}
      ${refusedBlock}
      ${noteBlock}
      ${verificationBlock}
      ${pagesBlock}
      ${method}`;

    return section(
      'fee',
      '€',
      turkish ? 'Başvurmanın maliyeti' : 'What it costs to apply',
      body,
      turkish
        ? 'Başvuru sırasında bir kez ödenir ve yıllık toplama girmez.'
        : 'Paid once when you apply, and never counted inside the annual total.'
    );
  }

  // ------------------------------------------------------------------- export

  function bindPanelEvents(root) {
    if (!root) return;
    root.querySelectorAll('[data-copy-email]').forEach((button) => {
      button.addEventListener('click', async () => {
        const address = button.getAttribute('data-copy-email');
        try {
          await navigator.clipboard.writeText(address);
          const original = button.textContent;
          button.textContent = tr() ? 'kopyalandı' : 'copied';
          button.classList.add('is-copied');
          setTimeout(() => {
            button.textContent = original;
            button.classList.remove('is-copied');
          }, 1600);
        } catch {
          button.textContent = tr() ? 'kopyalanamadı' : 'copy failed';
        }
      });
    });
  }

  window.uniDecisionPanels = {
    countdownPanel,
    applicationFeePanel,
    academicMatchPanel,
    researchUnitsPanel,
    facultyPanel,
    scholarshipPlaybookPanel,
    housingRubricPanel,
    costBreakdownPanel,
    bindPanelEvents,
  };
}());
