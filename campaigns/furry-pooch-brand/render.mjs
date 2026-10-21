// Renders post-a/b/c.html -> 1080x1350 PNG + JPG. usage: node render.mjs [out-dir]
import { createRequire } from "node:module";
import path from "node:path";
import { fileURLToPath } from "node:url";
const require = createRequire("/opt/node-tools/node_modules/");
const { chromium } = require("playwright");
const here = path.dirname(fileURLToPath(import.meta.url));
const outDir = path.resolve(process.argv[2] ?? here);
const names = { "post-a": "furry-pooch-A-festive-edit", "post-b": "furry-pooch-B-cats-love-fashion", "post-c": "furry-pooch-C-wedding-season" };
const browser = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium-1194/chrome-linux/chrome" });
const ctx = await browser.newContext({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 1 });
for (const [f, n] of Object.entries(names)) {
  const page = await ctx.newPage();
  await page.goto("file://" + path.join(here, f + ".html"));
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(400);
  const el = page.locator("#post");
  await el.screenshot({ path: path.join(outDir, n + ".png") });
  await el.screenshot({ path: path.join(outDir, n + ".jpg"), type: "jpeg", quality: 95 });
  await page.close();
}
await browser.close();
console.log("rendered to", outDir);
