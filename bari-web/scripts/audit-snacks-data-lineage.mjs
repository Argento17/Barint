/**
 * Forensic audit: shelf products vs BSIP0/BSIP1 (read-only).
 * Run: node scripts/audit-snacks-data-lineage.mjs
 */
import { existsSync, readFileSync, readdirSync, statSync } from "node:fs";
import { join } from "node:path";

const SHELF = {
  "snk-001": "7290011498870",
  "snk-002": "7290011498948",
  "snk-003": "16000548404",
  "snk-004": "8423207206495",
  "snk-005": "5900020039590",
  "snk-006": "7290118427858",
  "snk-007": "5900020015174",
  "snk-009": "8410076610379",
  "snk-010": "8410076610386",
  "snk-011": "7290111936784",
  "snk-012": "7290111937262",
  "snk-013": "4011800633516",
  "snk-015": "7290011498894",
  "snk-016": "8423207210928",
  "snk-017": "8410076610508",
  "snk-018": "8410076602251",
  "snk-019": "7290118427896",
  "snk-020": "7290014525306",
};

const bsip0Root = "c:/Bari/02_products/snack_bars/observations_bsip0/yohananof";
const bsip1Root = "c:/Bari/02_products/snack_bars/canonical_bsip1/run_001";
const bsip2Root =
  "c:/Bari/02_products/snack_bars/bsip2_outputs/run_snack_bars_synthesis_001/products";
const corpusPath = "c:/bari/bari-web/src/data/comparisons/snacks_frontend_v2.json";

const corpus = JSON.parse(readFileSync(corpusPath, "utf8"));
const audit = JSON.parse(readFileSync(join(bsip0Root, "audit_report.json"), "utf8"));
const auditByBarcode = Object.fromEntries(audit.products.map((p) => [p.barcode, p]));

const rows = [];
for (const p of corpus.products) {
  const bc = SHELF[p.id];
  const b0dir = join(bsip0Root, bc);
  const b0json = join(b0dir, "product.json");
  const nutHtml = join(b0dir, "nutrition.html");
  const ingHtml = join(b0dir, "ingredients.html");
  const b1 = join(bsip1Root, `bsip1_${bc}.json`);
  const b2 = join(bsip2Root, `bsip1_${bc}`, "bsip2_trace.json");

  let b0 = null;
  let b1d = null;
  let b2d = null;
  if (existsSync(b0json)) b0 = JSON.parse(readFileSync(b0json, "utf8"));
  if (existsSync(b1)) b1d = JSON.parse(readFileSync(b1, "utf8"));
  if (existsSync(b2)) b2d = JSON.parse(readFileSync(b2, "utf8"));

  const feNut = p.expansion?.nutrition ?? {};
  const feHasNut = Object.values(feNut).some((v) => v != null);

  rows.push({
    id: p.id,
    name: p.name,
    barcode: bc,
    score: p.score,
    confidence: p.confidence,
    fe_nut_populated: feHasNut,
    fe_ingredients: p.expansion?.ingredients ?? null,
    b0_dir: existsSync(b0dir),
    b0_nut_html: existsSync(nutHtml),
    b0_ing_html: existsSync(ingHtml),
    b0_nut_parsed: b0?.parser_status?.nutrition_present ?? false,
    b0_ing_parsed: b0?.parser_status?.ingredients_present ?? false,
    b0_kcal: b0?.nutrition_per_100g?.energy_kcal_100g ?? null,
    b0_sugar: b0?.nutrition_per_100g?.sugars_g_100g ?? null,
    b0_ing_len: b0?.raw_observations?.ingredients_raw_he?.length ?? 0,
    b1_exists: existsSync(b1),
    b1_kcal: b1d?.normalized_nutrition_per_100g?.energy_kcal ?? null,
    b1_ing_len: b1d?.ingredients_text_he?.length ?? 0,
    b2_exists: existsSync(b2),
    b2_score: b2d?.final_score ?? b2d?.score ?? null,
    b2_nut_layer: b2d?.layers?.nutritional?.status ?? b2d?.nutritional_layer_status ?? null,
    audit_status: auditByBarcode[bc]?.recommended_status ?? "missing_from_audit",
    audit_has_nutrition: auditByBarcode[bc]?.has_nutrition ?? null,
    audit_has_ingredients: auditByBarcode[bc]?.has_ingredients ?? null,
  });
}

const allB0 = readdirSync(bsip0Root).filter((f) =>
  statSync(join(bsip0Root, f)).isDirectory()
);
let nutHtmlCount = 0;
let ingHtmlCount = 0;
let productJsonCount = 0;
for (const d of allB0) {
  if (existsSync(join(bsip0Root, d, "nutrition.html"))) nutHtmlCount++;
  if (existsSync(join(bsip0Root, d, "ingredients.html"))) ingHtmlCount++;
  if (existsSync(join(bsip0Root, d, "product.json"))) productJsonCount++;
}

const summary = {
  bsip0_yohananof_dirs: allB0.length,
  bsip0_nutrition_html: nutHtmlCount,
  bsip0_ingredients_html: ingHtmlCount,
  bsip0_product_json: productJsonCount,
  audit_total_products: audit.total_products,
  audit_usable_raw: audit.usable_raw_count,
  audit_partial_raw: audit.partial_raw_count,
  shelf_count: rows.length,
  shelf_fe_null_nutrition: rows.filter((r) => !r.fe_nut_populated).length,
  shelf_fe_null_ingredients: rows.filter((r) => !r.fe_ingredients).length,
  shelf_b0_nut_html: rows.filter((r) => r.b0_nut_html).length,
  shelf_b0_ing_html: rows.filter((r) => r.b0_ing_html).length,
  shelf_b0_nut_parsed: rows.filter((r) => r.b0_nut_parsed).length,
  shelf_b0_ing_parsed: rows.filter((r) => r.b0_ing_parsed).length,
  shelf_b1_nut: rows.filter((r) => r.b1_kcal != null).length,
  shelf_b1_ing: rows.filter((r) => r.b1_ing_len > 0).length,
  shelf_verified_confidence: rows.filter((r) => r.confidence === "verified").length,
  shelf_partial_confidence: rows.filter((r) => r.confidence === "partial").length,
};

console.log(JSON.stringify({ summary, rows }, null, 2));
