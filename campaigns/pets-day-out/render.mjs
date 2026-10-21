// Renders post.html -> PNG using the Playwright that ships with the environment.
// usage: node render.mjs [out-dir]
import { createRequire } from "node:module";
import path from "node:path";
import { fileURLToPath } from "node:url";

const require = createRequire("/opt/node-tools/node_modules/");
const { chromium } = require("playwright");

const here = path.dirname(fileURLToPath(import.meta.url));
const outDir = path.resolve(process.argv[2] ?? here);

const browser = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium-1194/chrome-linux/chrome" });
for (const [scale, name] of [[1, "pets-day-out-coming-soon-1080x1350.png"], [2, "pets-day-out-coming-soon-2160x2700.png"]]) {
  const ctx = await browser.newContext({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: scale });
  const page = await ctx.newPage();
  await page.goto("file://" + path.join(here, "post.html"));
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(400);
  await page.locator("#post").screenshot({ path: path.join(outDir, name) });
  await ctx.close();
}
await browser.close();
console.log("rendered to", outDir);
