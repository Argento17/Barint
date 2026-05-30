/**
 * Capture expanded reasoning screenshots for maadanim v2 QA.
 * Usage: node scripts/capture-maadanim-expansions.mjs
 * Requires: playwright (npm install -D playwright && npx playwright install chromium)
 */
import { mkdirSync, readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { chromium } from "playwright";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const JSON_PATH = "src/data/comparisons/maadanim_frontend_v2.json";
const OUT_DIR = path.join(ROOT, "public", "qa", "maadanim-v2");
const BASE_URL = process.env.PREVIEW_URL ?? "http://localhost:3000/dev/preview";

/** Ten products spanning CE themes: comparative, low-fat, fruit, partial data, collagen, flagship, format, oats, inversion, high performer. */
const REPRESENTATIVE_NAMES = [
  "יופלה GO מועשר בחלבון",
  "יופלה GO דובדבן 0.7%",
  "יופלה GO אפרסק 0.7%",
  "מעדן משמש",
  "מעדן סויה ביו טבעי",
  "דנונה מולטי קולגן",
  "מילקי בטעם שוקולד",
  "פודינג אינסטנט שוקולד",
  "מעדן שיבולת שועל",
  "מעדן הגולן שוקולד מריר",
];

/** v2 SPECIFIC fixes + CE-flagged shelf edge cases (deduped at runtime). */
const PROBLEMATIC_NAMES = [
  "יופלה GO מועשר בחלבון",
  "יופלה GO דובדבן 0.7%",
  "מעדן משמש",
  "מעדן סויה ביו טבעי",
  "מעדן שיבולת שועל",
  "מעדן הגולן שוקולד מריר",
  "דנונה מולטי קולגן",
  "מלבי שמנת",
  "מעדן הגולן וניל",
  "מעדן חצילים",
  "מילקי בטעם שוקולד",
  "באדי תות שדה 3% שומן",
  "לימבו פטל קו חלבי",
  "מעדן מוו בטעם שוקולד",
  "מעדן  מוו בטעם וניל מארז",
  "דני שוקולד 1.5%",
  "מילקי בטעם תות",
  "מילקי עם 26% פחות סוכר",
  "מילקי בטעם פסק זמן",
  "מילקי שכבות שוקולד+קצפת",
  "מילקי שכבות שוקולד קוקוס",
  "דניאלה תות בננה",
  "דניאלה תות מוקצף5% שומן",
  "דניאלה בננה",
  "דניאלה בטעם ענבים",
  "מעדן גבינה מוקצף וניל",
  "יופלה טיוב בטעם וניל",
  "פודינג אינסטנט שוקולד",
];

function slugify(name) {
  return name
    .replace(/[^\w\u0590-\u05FF]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 80);
}

function loadProducts() {
  const raw = readFileSync(JSON_PATH, "utf-8");
  const data = JSON.parse(raw);
  const byName = new Map(data.products.map((p) => [p.name, p]));
  return { byName };
}

function resolveIds(names, byName) {
  const ids = [];
  const missing = [];
  for (const name of names) {
    const product = byName.get(name);
    if (product) ids.push({ id: product.id, name: product.name });
    else missing.push(name);
  }
  return { ids, missing };
}

async function captureProduct(page, { id, name }, folder) {
  const url = `${BASE_URL}?expand=${encodeURIComponent(id)}`;
  await page.goto(url, { waitUntil: "networkidle" });
  await page.waitForSelector(`[aria-label="${name}"][aria-expanded="true"]`, {
    timeout: 30000,
  });
  const row = page.locator("article").filter({
    has: page.locator(`[aria-label="${name}"]`),
  });
  await row.scrollIntoViewIfNeeded();
  await page.waitForTimeout(500);
  const file = path.join(folder, `${slugify(name)}.png`);
  await row.screenshot({ path: file });
  return file;
}

async function main() {
  const { byName } = loadProducts();

  const rep = resolveIds(REPRESENTATIVE_NAMES, byName);
  const prob = resolveIds([...new Set(PROBLEMATIC_NAMES)], byName);

  if (rep.missing.length) console.warn("Missing representative:", rep.missing);
  if (prob.missing.length) console.warn("Missing problematic:", prob.missing);

  mkdirSync(path.join(OUT_DIR, "representative"), { recursive: true });
  mkdirSync(path.join(OUT_DIR, "problematic"), { recursive: true });

  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({
    viewport: { width: 390, height: 844 },
  });

  console.log("Representative captures:");
  for (const item of rep.ids) {
    const file = await captureProduct(page, item, path.join(OUT_DIR, "representative"));
    console.log(" ", file);
  }

  console.log("Problematic captures:");
  for (const item of prob.ids) {
    const file = await captureProduct(page, item, path.join(OUT_DIR, "problematic"));
    console.log(" ", file);
  }

  await browser.close();
  console.log(`Done. ${rep.ids.length} representative, ${prob.ids.length} problematic.`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
