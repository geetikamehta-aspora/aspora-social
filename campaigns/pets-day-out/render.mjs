// Renders an HTML post -> 1x and 2x PNGs using the Playwright that ships with the environment.
// usage: node render.mjs [html-file] [out-prefix] [out-dir]
//   node render.mjs post.html pets-day-out-coming-soon
//   node render.mjs post-classy.html pets-day-out-classy
import { createRequire } from "node:module";
import path from "node:path";
import { fileURLToPath } from "node:url";

const require = createRequire("/opt/node-tools/node_modules/");
const { chromium } = require("playwright");

const here = path.dirname(fileURLToPath(import.meta.url));
const htmlFile = process.argv[2] ?? "post.html";
const prefix = process.argv[3] ?? "pets-day-out-coming-soon";
const outDir = path.resolve(process.argv[4] ?? here);

const browser = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium-1194/chrome-linux/chrome" });
for (const [scale, size] of [[1, "1080x1350"], [2, "2160x2700"]]) {
  const ctx = await browser.newContext({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: scale });
  const page = await ctx.newPage();
  await page.goto("file://" + path.join(here, htmlFile));
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(400);
  await page.locator("#post").screenshot({ path: path.join(outDir, `${prefix}-${size}.png`) });
  await ctx.close();
}
await browser.close();
console.log("rendered", htmlFile, "to", outDir);
