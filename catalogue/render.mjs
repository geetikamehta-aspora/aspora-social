// Renders catalogue.html to Furry-Pooch-Catalogue.pdf (and optional PNG previews with --png).
import { createRequire } from 'module';
import path from 'path';
import { fileURLToPath, pathToFileURL } from 'url';

const require = createRequire('/opt/node22/lib/node_modules/');
const { chromium } = require('playwright');

const here = path.dirname(fileURLToPath(import.meta.url));
const png = process.argv.includes('--png');
const detailed = process.argv.includes('--detailed');
const src = detailed ? 'catalogue-detailed.html' : 'catalogue.html';
const out = detailed ? 'Furry-Pooch-Catalogue-Detailed.pdf' : 'Furry-Pooch-Catalogue.pdf';

const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const page = await browser.newPage({ viewport: { width: 794, height: 1123 }, deviceScaleFactor: 1.5 });
await page.goto(pathToFileURL(path.join(here, src)).href, { waitUntil: 'networkidle' });
await page.evaluate(() => document.fonts.ready);
await page.pdf({ path: path.join(here, out), width: '210mm', height: '297mm', printBackground: true, preferCSSPageSize: true });
if (png) {
  const pages = await page.$$('.page');
  for (let i = 0; i < pages.length; i++) await pages[i].screenshot({ path: `/tmp/claude-0/-home-user-aspora-social/9b718c4d-f21f-52f0-89ec-981b9997f844/scratchpad/fp-preview-${i + 1}.png` });
  console.log(`${pages.length} previews`);
}
await browser.close();
