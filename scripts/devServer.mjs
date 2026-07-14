import { createServer } from 'node:http';
import { readFile, readdir } from 'node:fs/promises';
import { extname, normalize } from 'node:path';

const root = new URL('../', import.meta.url);
const publicDir = new URL('../public/', import.meta.url);
const dataDir = new URL('../data_base/', import.meta.url);
const port = Number(process.env.PORT || 8765);

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
    if (['year', 'annual', 'annually', 'yr'].includes(period)) return { amount, entry };
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
    record?.university,
    record?.University_Display_Name,
    record?.University_Name,
    record?.display_name,
    record?.name
  );
}

function programName(record) {
  return firstDisplayValue(
    record?.program_name,
    record?.Program_Name,
    record?.target_program_name,
    record?.Target_Program_Name
  );
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

async function loadPrograms() {
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

        records.push(applySourceGuard(isLegacyRecord(record) ? normalizeLegacyRecord(record, fileName) : record));
      });
    } catch (error) {
      skipped.push({ file: fileName, message: error.message });
    }
  }

  return {
    records,
    report: {
      files_seen: fileNames.length,
      files_loaded: filesLoaded,
      records_seen: recordsSeen,
      records_loaded: records.length,
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
