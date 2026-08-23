import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const publicDir = path.join(root, 'public');
const pages = ['index.html', 'scholarships.html', 'research.html'];
const failures = [];
let checkedAssetCount = 0;

function isLocalAsset(reference) {
  const pathOnly = String(reference || '').split(/[?#]/, 1)[0];
  return reference
    && !reference.startsWith('#')
    && !reference.startsWith('data:')
    && !reference.startsWith('mailto:')
    && !reference.startsWith('tel:')
    && !/^https?:\/\//i.test(reference)
    && !reference.startsWith('/api/')
    && /\.(?:css|js|mjs|png|jpe?g|svg|webp|gif|ico|json|woff2?|ttf)$/i.test(pathOnly);
}

for (const pageName of pages) {
  const pagePath = path.join(publicDir, pageName);
  const html = fs.readFileSync(pagePath, 'utf8');
  const storagePosition = html.indexOf('storage.js');
  const i18nPosition = html.indexOf('i18n.js');
  if (i18nPosition >= 0 && (storagePosition < 0 || storagePosition > i18nPosition)) {
    failures.push(`${pageName} must load storage.js before i18n.js`);
  }
  const references = [
    ...html.matchAll(/\b(?:src|href)="([^"]+)"/g),
    ...html.matchAll(/\b(?:src|href)='([^']+)'/g),
  ].map((match) => match[1]).filter(isLocalAsset);

  const seen = new Set();
  for (const reference of references) {
    const cleanReference = reference.split(/[?#]/, 1)[0];
    if (!cleanReference) continue;
    const normalized = cleanReference.replace(/^\//, '');
    const assetPath = path.resolve(publicDir, normalized);
    checkedAssetCount += 1;

    if (!assetPath.startsWith(`${publicDir}${path.sep}`) && assetPath !== publicDir) {
      failures.push(`${pageName} references an asset outside public/: ${reference}`);
      continue;
    }
    if (!fs.existsSync(assetPath)) failures.push(`${pageName} references missing asset: ${reference}`);
    if (seen.has(reference)) failures.push(`${pageName} loads the same local asset twice: ${reference}`);
    seen.add(reference);
  }
}

if (failures.length) {
  console.error(`Static asset checks failed (${failures.length})`);
  failures.forEach((failure) => console.error(`- ${failure}`));
  process.exit(1);
}

console.log(`Static asset checks passed: ${pages.length} pages, ${checkedAssetCount} local references.`);
