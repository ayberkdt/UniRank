import { readFile } from 'node:fs/promises';

const script = await readFile(new URL('../public/script.js', import.meta.url), 'utf8');
const activeCountries = {
  austria: 'AT', belgium: 'BE', czechia: 'CZ', denmark: 'DK', estonia: 'EE',
  finland: 'FI', france: 'FR', germany: 'DE', greece: 'GR', ireland: 'IE',
  italy: 'IT', lithuania: 'LT', netherlands: 'NL', norway: 'NO', poland: 'PL',
  portugal: 'PT', romania: 'RO', spain: 'ES', sweden: 'SE', switzerland: 'CH',
  turkey: 'TR', united_kingdom: 'GB', usa: 'US'
};

const failures = [];
for (const [key, code] of Object.entries(activeCountries)) {
  const visualPattern = new RegExp(`\\b${key}:\\s*\\{\\s*accent:`);
  const codePattern = new RegExp(`\\b${key}:\\s*['\"]${code}['\"]`);
  if (!visualPattern.test(script)) failures.push(`${key}: card flag visual missing`);
  if (!codePattern.test(script)) failures.push(`${key}: picker flag code ${code} missing`);
}

if (failures.length) {
  console.error(`Country flag checks failed (${failures.length})`);
  failures.forEach(failure => console.error(`- ${failure}`));
  process.exitCode = 1;
} else {
  console.log(`Country flag checks passed: ${Object.keys(activeCountries).length} active countries covered.`);
}
