import { createServer } from 'node:http';
import { readFile, readdir } from 'node:fs/promises';
import { extname, normalize } from 'node:path';

const root = new URL('../', import.meta.url);
const publicDir = new URL('../public/', import.meta.url);
const dataDir = new URL('../data_base/', import.meta.url);
const scholarshipCatalogUrl = new URL('../scholarships/catalog.json', import.meta.url);
const researchFieldCatalogUrl = new URL('../research_fields/catalog.json', import.meta.url);
const catalogScopeUrl = new URL('../config/catalog_scope.json', import.meta.url);
const standardsUrl = new URL('../config/standards.json', import.meta.url);
const visaUrl = new URL('../config/visa_requirements.json', import.meta.url);
const port = Number(process.env.PORT || 8765);
const featuredResearchProgramIds = [
  'mit-aeroastro',
  'stanford-aa',
  'caltech-galcit',
  'university-of-cambridge',
  'imperial-college-london',
  'netherlands_delft_msc_aerospace',
  'se-kth-aero-msc',
  'germany-tum-msc-aerospace',
  'germany-stuttgart-msc-aerospace',
  'purdue-aae',
  'uiuc-ae',
  'georgia-tech-ae',
  'umich-aero',
];

const mimeTypes = {
  '.css': 'text/css; charset=utf-8',
  '.html': 'text/html; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.png': 'image/png',
  '.svg': 'image/svg+xml',
  '.webp': 'image/webp',
};

function sendJson(response, payload, statusCode = 200) {
  response.writeHead(statusCode, {
    'Cache-Control': 'no-store',
    'Content-Type': mimeTypes['.json'],
  });
  response.end(JSON.stringify(payload));
}

function finiteNumber(value) {
  if (value === null || value === undefined || value === '') return null;
  const number = typeof value === 'number' ? value : Number(String(value).trim());
  return Number.isFinite(number) ? number : null;
}

function displayText(value) {
  if (value === null || value === undefined) return '';
  if (typeof value === 'string') return value.trim();
  if (typeof value === 'object') return displayText(value.en || value.tr || value.name || value.label);
  return String(value).trim();
}

function programmeIdentity(record) {
  return {
    programme_id: record.id || record.Uni_ID,
    university: displayText(record.university || record.University),
    programme: displayText(record.program_name || record.Program || record.programme_name),
    country: displayText(record.country || record.Country),
    degree_level: displayText(record.degree_level || record.Degree),
  };
}

function latestVerified(current, profiles) {
  const dates = [current, ...profiles.map(profile => profile.last_verified)].filter(value => typeof value === 'string');
  return dates.length ? dates.sort().at(-1) : null;
}

function institutionalFunding(records) {
  const order = new Map(featuredResearchProgramIds.map((id, index) => [id, index]));
  return records.flatMap(record => {
    const profile = record.scholarship_profile || {};
    const playbook = Array.isArray(profile.playbook) ? profile.playbook : [];
    const identity = programmeIdentity(record);
    if (!identity.programme_id || !playbook.length) return [];
    return [{
      ...identity,
      featured: order.has(identity.programme_id),
      application_mode: profile.application_mode,
      scholarship_deadline: profile.scholarship_deadline,
      deadline_notes: profile.notes || profile.verification_notes,
      funding_status: profile.funding_status,
      playbook,
      last_verified: record.source_profile?.last_verified || record.last_verified,
    }];
  }).sort((left, right) => {
    const featuredDelta = Number(!left.featured) - Number(!right.featured);
    if (featuredDelta) return featuredDelta;
    const orderDelta = (order.get(left.programme_id) ?? 999) - (order.get(right.programme_id) ?? 999);
    return orderDelta || left.university.localeCompare(right.university);
  });
}

function programmeResearchDetails(records) {
  const order = new Map(featuredResearchProgramIds.map((id, index) => [id, index]));
  return records.flatMap(record => {
    const profile = record.research_profile || {};
    const notableProfessors = Array.isArray(profile.notable_professors) ? profile.notable_professors : [];
    const researchUnits = Array.isArray(profile.research_units) ? profile.research_units : [];
    const identity = programmeIdentity(record);
    if (!identity.programme_id || (!notableProfessors.length && !researchUnits.length)) return [];
    return [{
      ...identity,
      featured: order.has(identity.programme_id),
      faculty_contact_policy: profile.faculty_contact_policy,
      faculty_contact_note: profile.faculty_contact_note,
      faculty_email_availability: profile.faculty_email_availability,
      notable_professors: notableProfessors,
      research_units: researchUnits,
      verification_notes: profile.verification_notes,
      last_verified: record.source_profile?.last_verified || record.last_verified,
    }];
  }).sort((left, right) => {
    const featuredDelta = Number(!left.featured) - Number(!right.featured);
    if (featuredDelta) return featuredDelta;
    const orderDelta = (order.get(left.programme_id) ?? 999) - (order.get(right.programme_id) ?? 999);
    const evidenceDelta = (right.notable_professors.length + right.research_units.length)
      - (left.notable_professors.length + left.research_units.length);
    return orderDelta || evidenceDelta || left.university.localeCompare(right.university);
  });
}

function officialSourceCount(catalogSources, records, relevantTerms) {
  const urls = new Set((catalogSources || []).map(source => source?.url).filter(Boolean));
  const acceptedStatuses = new Set(['ok', 'redirects', 'pdf', 'requires_js']);
  records.forEach(record => (record.source_profile?.source_log || []).forEach(source => {
    if (!String(source?.source_type || '').startsWith('official_') || !acceptedStatuses.has(source?.access_status) || !source?.url) return;
    const fields = (source.relevant_fields || []).join(' ').toLowerCase();
    if (relevantTerms.some(term => fields.includes(term))) urls.add(source.url);
  }));
  return urls.size;
}

function firstDisplayValue(...values) {
  for (const value of values) {
    if (displayText(value)) return value;
  }
  return null;
}

function annualTuition(entries) {
  if (!Array.isArray(entries)) return { amount: null, entry: null };

  for (const entry of entries) {
    if (!entry || typeof entry !== 'object') continue;
    const amount = finiteNumber(entry.amount);
    if (amount === null) continue;

    const period = String(entry.period || '').trim().toLowerCase();
    if (['year', 'annual', 'annually', 'yr', 'academic_year'].includes(period)) return { amount, entry };
    if (['semester', 'term'].includes(period)) return { amount: amount * 2, entry };
  }
  return { amount: null, entry: null };
}

function semesterFee(entries) {
  if (!Array.isArray(entries)) return null;
  for (const entry of entries) {
    if (!entry || typeof entry !== 'object') continue;
    const amount = finiteNumber(entry.amount);
    if (amount !== null) return amount;
  }
  return null;
}

function isStructuredRecord(record) {
  return Boolean(record?.eligibility_profile && record?.cost_profile);
}

function isV2Record(record) {
  return String(record?.schema_version || '').startsWith('2.')
    && Boolean(record?.institution_profile && record?.program_profile);
}

function isLegacyRecord(record) {
  return !isStructuredRecord(record) && Boolean(
    record?.Uni_ID || record?.University_Name || record?.Program_Name || record?.Cost_Tuition
  );
}

function isNonEuScope(scope) {
  if (scope === null || scope === undefined || String(scope).trim() === '') return true;
  const normalizedScope = String(scope).trim().toLowerCase().replace(/[\s-]+/g, '_');
  return normalizedScope === 'non_eu' || normalizedScope === 'noneu';
}

function verifiedFields(record) {
  const fields = record?.data_quality?.verified_fields;
  return Array.isArray(fields) ? new Set(fields) : new Set();
}

// The development server mirrors the production API's source-safety boundary.
// It never turns an unchecked legacy value into a locally visible decision
// fact, so screenshots and local QA cannot accidentally validate the wrong UI.
function applySourceGuard(record) {
  const guarded = structuredClone(record);
  const verified = verifiedFields(guarded);
  guarded.needs_verification = guarded.data_quality?.status !== 'verified';
  guarded.source_profile = { ...(guarded.source_profile || {}), needs_verification: guarded.needs_verification };

  if (!verified.has('language')) {
    guarded.teaching_language = ['Unknown'];
    guarded.language_req = '';
    if (guarded.language_profile) guarded.language_profile = { ...guarded.language_profile, teaching_language: ['Unknown'], language_risk: 'unknown' };
  }
  if (!verified.has('tuition')) {
    guarded.tuition_eur_per_year = null;
    guarded.annual_fee_eur = null;
    guarded.semester_fee_eur = null;
    if (guarded.cost_profile) {
      guarded.cost_profile = {
        ...guarded.cost_profile,
        tuition_eur_per_year_estimated: null,
        tuition_eur_per_year_min: null,
        tuition_eur_per_year_max: null,
        total_academic_cost_eur_per_year_estimated: null,
        regional_tax_eur: null,
        student_contribution_eur: null,
        enrollment_fee_eur: null,
      };
    }
  }
  if (!verified.has('deadline')) {
    guarded.deadline_winter_closes = '';
    guarded.deadline_summer_closes = '';
    guarded.deadlines_note = '';
    if (guarded.application_timeline_profile) guarded.application_timeline_profile = {};
  }
  if (!verified.has('housing') && guarded.living_profile) {
    guarded.living_profile = {
      ...guarded.living_profile,
      average_room_rent_eur: null,
      monthly_living_cost_eur_estimated: null,
      living_cost_eur_per_month: null,
      housing_difficulty: null,
    };
  }
  if (!verified.has('scholarship') && guarded.scholarship_profile) {
    guarded.scholarship_profile = {
      ...guarded.scholarship_profile,
      regional_scholarship_available: null,
      regional_scholarship_name: null,
      non_eu_eligible: null,
      scholarship_deadline: null,
      funding_notes: null,
    };
  }
  return guarded;
}

function recordId(record) {
  return displayText(firstDisplayValue(record?.Uni_ID, record?.id, record?.name, record?.university));
}

function universityName(record) {
  return firstDisplayValue(
    record?.institution_profile?.name,
    record?.university,
    record?.University_Display_Name,
    record?.University_Name,
    record?.display_name,
    record?.name
  );
}

function programName(record) {
  return firstDisplayValue(
    record?.program_profile?.name,
    record?.program_name,
    record?.Program_Name,
    record?.target_program_name,
    record?.Target_Program_Name
  );
}

function isUndergraduateProgramme(record) {
  const degreeText = [
    record?.degree_level,
    record?.program_degree,
    record?.target_program_degree,
    record?.Program_Degree,
    record?.degree,
    record?.level,
    record?.program_profile?.degree_level,
    record?.program_profile?.degree_award,
  ].map(displayText).join(' ').toLowerCase();
  return /\b(bachelor|b\.\s*sc\.?|bsc|undergraduate|first[- ]cycle|lisans)\b/.test(degreeText)
    || (degreeText.includes('diplom') && degreeText.includes('direct'));
}

function duplicateProgrammeKey(record) {
  const compact = (value) => displayText(value).toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim();
  const key = [
    compact(record?.country),
    compact(universityName(record)),
    compact(programName(record)),
    compact(firstDisplayValue(record?.degree_level, record?.program_degree, record?.target_program_degree)),
  ];
  return key.every(Boolean) ? key.join('|') : '';
}

function programmePreference(record) {
  const quality = record?.data_quality || {};
  const statusRank = { verified: 3, partial: 2, needs_verification: 1 }[String(quality.status || '').toLowerCase()] || 0;
  return [
    statusRank,
    Array.isArray(quality.verified_fields) ? quality.verified_fields.length : 0,
    Array.isArray(record?.source_profile?.source_log) ? record.source_profile.source_log.length : 0,
    String(record?.updated_at || ''),
  ];
}

function keepPreferredProgramme(records) {
  const selected = new Map();
  const duplicates = [];
  for (const record of records) {
    const key = duplicateProgrammeKey(record);
    if (!key) {
      selected.set(`id:${recordId(record)}:${selected.size}`, record);
      continue;
    }
    const current = selected.get(key);
    if (!current) {
      selected.set(key, record);
      continue;
    }
    const currentRank = programmePreference(current).join('|');
    const candidateRank = programmePreference(record).join('|');
    if (candidateRank > currentRank) {
      duplicates.push({ retained: recordId(record), suppressed: recordId(current) });
      selected.set(key, record);
    } else {
      duplicates.push({ retained: recordId(current), suppressed: recordId(record) });
    }
  }
  return { records: [...selected.values()], duplicates };
}

function normalizeLegacyRecord(record, sourceFile) {
  const tuition = annualTuition(record.Cost_Tuition);
  const fee = semesterFee(record.Cost_Semester_Fees);
  const annualFee = tuition.amount === null ? null : tuition.amount + ((fee || 0) * 2);
  const tags = Array.isArray(record.Analysis_Tags) ? record.Analysis_Tags : [];
  const scholarships = Array.isArray(record.Scholarships_Info) ? record.Scholarships_Info : [];

  return {
    ...record,
    id: record.Uni_ID || '',
    name: record.University_Name || '',
    display_name: record.University_Display_Name || record.University_Name || '',
    short: record.University_Short_Name || '',
    university: record.University_Display_Name || record.University_Name || '',
    city: record.City || '',
    state: record.State_Region || '',
    country: record.Country || '',
    location: record.location || null,
    scope: record.Program_Scope || 'non_eu',
    needs_verification: record.Meta_Needs_Verification === true,
    cost_city: record.Cost_City_Living || '',
    cost_city_raw: record.Cost_City_Living || '',
    city_cost_rank: finiteNumber(record.Cost_City_Rank),
    semester_fee_eur: fee,
    tuition_eur_per_year: tuition.amount,
    annual_fee_eur: annualFee,
    tuition_raw: tuition.entry?.raw || '',
    tuition_program: tuition.entry?.program || '',
    tuition_period: tuition.entry?.period || '',
    tuition_scope: tuition.entry?.scope || '',
    aerospace_ecosystem: record.Industry_Ecosystem || '',
    strong_areas_summary: record.Analysis_Strong_Areas || '',
    strength: record.Analysis_Strong_Areas || '',
    focus: tags.join(', '),
    pros: Array.isArray(record.Analysis_Pros) ? record.Analysis_Pros : [],
    cons: Array.isArray(record.Analysis_Cons) ? record.Analysis_Cons : [],
    tags,
    tags_raw: tags.join(', '),
    target_program_name: record.Program_Name || '',
    target_program_degree: record.Program_Degree || '',
    target_program_ects: finiteNumber(record.Program_ECTS),
    target_program_url: record.Program_URL || '',
    admission_mode: record.Admission_Mode || '',
    language_req: record.Admission_Language_Req || '',
    internship_mandatory: record.Internship_Mandatory === true,
    internship_notes: record.Internship_Notes || '',
    deadline_winter_opens: record.Deadline_Winter_Open || '',
    deadline_winter_closes: record.Deadline_Winter_Close || '',
    deadline_summer_opens: record.Deadline_Summer_Open || '',
    deadline_summer_closes: record.Deadline_Summer_Close || '',
    deadlines_note: record.Deadline_General_Note || '',
    housing_difficulty: record.Living_Housing_Difficulty || '',
    housing_difficulty_score: finiteNumber(record.Living_Housing_Score),
    key_partners: Array.isArray(record.Industry_Partners) ? record.Industry_Partners : [],
    scholarship_names: scholarships.map(item => displayText(item?.name)).filter(Boolean).join(', '),
    qs_ranking: finiteNumber(record.qs_ranking),
    global_recognition: record.global_recognition || '',
    field_recognition: record.field_recognition || '',
    source_file: sourceFile,
    updated_at: record.Meta_Updated_At || '',
  };
}

function normalizeV2Record(record, sourceFile) {
  const institution = record.institution_profile || {};
  const programme = record.program_profile || {};
  const language = record.language_profile || {};
  const cost = record.cost_profile || {};
  const curriculum = record.curriculum_profile || {};
  const timeline = record.application_timeline_profile || {};
  const scholarship = record.scholarship_profile || {};
  const living = record.living_profile || {};
  const categories = [
    ...(record.category_profile?.primary_categories || []),
    ...(record.category_profile?.secondary_categories || []),
  ];
  const tuition = annualTuition(cost.tuition_items);
  const tuitionEur = String(tuition.entry?.currency || '').toUpperCase() === 'EUR' ? tuition.amount : null;
  const currentDeadline = (timeline.deadline_events || []).find(event =>
    event?.date_status === 'current'
    && ['non_eu', 'international', 'all', undefined, null].includes(event?.applicant_scope)
  );
  const languageRequirement = (language.accepted_tests || [])
    .map(test => {
      const score = test?.minimum_overall ?? test?.minimum_score;
      return [displayText(test?.test), score].filter(value => value !== '' && value !== null && value !== undefined).join(' ');
    })
    .filter(Boolean)
    .join(' / ');

  return {
    ...record,
    name: institution.name || '',
    display_name: institution.native_name || institution.name || '',
    short: institution.short_name || '',
    university: institution.name || '',
    city: record.location?.city || '',
    state: record.location?.region || '',
    scope: 'non_eu',
    needs_verification: record.source_profile?.needs_verification === true,
    tuition_eur_per_year: tuitionEur,
    annual_fee_eur: tuitionEur,
    tuition_raw: tuition.entry?.basis || '',
    tuition_program: programme.name || '',
    tuition_period: tuition.entry?.period || '',
    tuition_scope: tuition.entry?.applicant_scope || '',
    strong_areas_summary: record.research_profile?.summary || '',
    strength: record.research_profile?.summary || '',
    focus: categories.join(', '),
    pros: record.decision_summary?.main_strengths || [],
    cons: record.decision_summary?.main_risks || [],
    tags: categories,
    tags_raw: categories.join(', '),
    target_program_name: programme.name || '',
    target_program_degree: programme.degree_award || '',
    target_program_ects: finiteNumber(programme.credits?.value),
    target_program_url: programme.official_url || '',
    admission_mode: record.eligibility_profile?.selection_method || '',
    language_req: languageRequirement,
    internship_mandatory: curriculum.internship?.required === true,
    internship_notes: curriculum.internship?.notes || '',
    deadline_winter_closes: currentDeadline?.date || '',
    deadlines_note: timeline.planning_advice || '',
    housing_difficulty: living.housing_risk || '',
    scholarship_names: (scholarship.opportunities || []).map(item => displayText(item?.name)).filter(Boolean).join(', '),
    source_file: sourceFile,
    updated_at: record.source_profile?.last_verified || '',
    program_name: programme.name || '',
    program_degree: programme.degree_award || '',
    degree_level: programme.degree_level || '',
    duration_years: programme.duration?.unit === 'years' ? finiteNumber(programme.duration?.value) : null,
    ects: finiteNumber(programme.credits?.value),
    teaching_language: language.teaching_languages || [],
    program_url: programme.official_url || '',
    program_status: programme.program_status || '',
  };
}

async function loadPrograms() {
  const catalogScope = JSON.parse(await readFile(catalogScopeUrl, 'utf8'));
  const countryAliases = catalogScope.country_aliases || {};
  const excludedCountries = new Set(
    (catalogScope.excluded_countries || []).map(country => countryAliases[country] || country)
  );
  const fileNames = (await readdir(dataDir, { withFileTypes: true }))
    .filter((entry) => entry.isFile() && entry.name.endsWith('.json') && entry.name !== 'taxonomy.json')
    .map((entry) => entry.name)
    .sort((left, right) => left.localeCompare(right));

  const records = [];
  const skipped = [];
  let filesLoaded = 0;
  let recordsSeen = 0;

  for (const fileName of fileNames) {
    try {
      const parsed = JSON.parse(await readFile(new URL(fileName, dataDir), 'utf8'));
      const rows = Array.isArray(parsed)
        ? parsed
        : Array.isArray(parsed.programs)
          ? parsed.programs
          : Array.isArray(parsed.universities)
            ? parsed.universities
            : (parsed && typeof parsed === 'object' ? [parsed] : []);

      filesLoaded += 1;
      rows.forEach((record, index) => {
        recordsSeen += 1;
        const id = recordId(record);
        const rawCountry = displayText(firstDisplayValue(record?.country, record?.Country));
        const catalogCountry = countryAliases[rawCountry] || rawCountry;

        if (excludedCountries.has(catalogCountry)) {
          skipped.push({ file: fileName, record_index: index, id, message: `Outside active catalogue scope: ${catalogCountry}` });
          return;
        }

        if (isStructuredRecord(record) && record.eligibility_profile.eligible_for_non_eu === false) {
          skipped.push({ file: fileName, record_index: index, id, message: 'Explicitly ineligible for non-EU applicants.' });
          return;
        }
        if (isLegacyRecord(record) && !isNonEuScope(record.Program_Scope)) {
          skipped.push({ file: fileName, record_index: index, id, message: `Unsupported Program_Scope: ${record.Program_Scope}` });
          return;
        }
        if (!displayText(universityName(record))) {
          skipped.push({ file: fileName, record_index: index, id, message: 'University name is missing.' });
          return;
        }
        if (!displayText(programName(record))) {
          skipped.push({ file: fileName, record_index: index, id, message: 'Program name is missing.' });
          return;
        }
        if (isUndergraduateProgramme(record)) {
          skipped.push({ file: fileName, record_index: index, id, message: 'Undergraduate programme excluded from the postgraduate-only dataset.' });
          return;
        }

        const normalized = isLegacyRecord(record)
          ? normalizeLegacyRecord(record, fileName)
          : isV2Record(record)
            ? normalizeV2Record(record, fileName)
            : record;
        records.push(applySourceGuard(normalized));
      });
    } catch (error) {
      skipped.push({ file: fileName, message: error.message });
    }
  }

  const deduplicated = keepPreferredProgramme(records);
  return {
    records: deduplicated.records,
    report: {
      files_seen: fileNames.length,
      files_loaded: filesLoaded,
      records_seen: recordsSeen,
      records_loaded: deduplicated.records.length,
      duplicate_programmes_suppressed: deduplicated.duplicates,
      skipped,
    },
  };
}

const server = createServer(async (request, response) => {
  try {
    const url = new URL(request.url || '/', `http://${request.headers.host || 'localhost'}`);

    if (url.pathname === '/api/universities') {
      const { records, report } = await loadPrograms();
      sendJson(response, {
        status: 'success',
        data: records,
        report,
      });
      return;
    }

    if (url.pathname === '/api/taxonomy') {
      const taxonomy = JSON.parse(await readFile(new URL('taxonomy.json', dataDir), 'utf8'));
      sendJson(response, taxonomy);
      return;
    }

    if (url.pathname === '/api/scholarships') {
      const catalog = JSON.parse(await readFile(scholarshipCatalogUrl, 'utf8'));
      const { records } = await loadPrograms();
      const opportunities = institutionalFunding(records);
      catalog.institutional_opportunities = opportunities;
      catalog.last_verified = latestVerified(catalog.last_verified, opportunities);
      sendJson(response, { status: 'success', data: catalog });
      return;
    }

    if (url.pathname === '/api/research-pathways') {
      const catalog = JSON.parse(await readFile(researchFieldCatalogUrl, 'utf8'));
      const { records } = await loadPrograms();
      const details = programmeResearchDetails(records);
      catalog.programme_research_details = details;
      catalog.last_verified = latestVerified(catalog.last_verified, details);
      catalog.official_source_count = officialSourceCount(
        catalog.sources, records, ['research', 'faculty', 'professor', 'lab', 'facilit']
      );
      sendJson(response, { status: 'success', data: catalog });
      return;
    }

    if (url.pathname === '/api/visa-requirements') {
      const visa = JSON.parse(await readFile(visaUrl, 'utf8'));
      sendJson(response, { status: 'success', data: visa });
      return;
    }

    if (url.pathname === '/api/standards') {
      const standards = JSON.parse(await readFile(standardsUrl, 'utf8'));
      sendJson(response, { status: 'success', data: standards });
      return;
    }

    const requestedPath = decodeURIComponent(url.pathname === '/' ? '/index.html' : url.pathname);
    const safePath = normalize(requestedPath).replace(/^([.][.][/\\])+/, '').replace(/^[/\\]+/, '');
    const fileUrl = new URL(safePath, publicDir);

    if (!fileUrl.href.startsWith(publicDir.href)) {
      sendJson(response, { status: 'error', message: 'Invalid path.' }, 400);
      return;
    }

    const body = await readFile(fileUrl);
    response.writeHead(200, {
      'Cache-Control': 'no-store',
      'Content-Type': mimeTypes[extname(safePath)] || 'application/octet-stream',
    });
    response.end(body);
  } catch (error) {
    if (error?.code === 'ENOENT') {
      sendJson(response, { status: 'error', message: 'Not found.' }, 404);
      return;
    }
    sendJson(response, { status: 'error', message: error.message }, 500);
  }
});

server.listen(port, '127.0.0.1', () => {
  console.log(`UniRank dev server: http://127.0.0.1:${port}`);
  console.log(`Serving ${new URL('.', root).pathname}`);
});
