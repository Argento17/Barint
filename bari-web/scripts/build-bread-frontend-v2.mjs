/**
 * Builds src/data/comparisons/bread_frontend_v2.json from CE-approved repo sources:
 * - src/data/bread-retail-curated.json (product shelf order, scores, Hebrew copy)
 * - src/data/bread-retail-shufersal.json (ingredient_architecture_summary, short_summary_he)
 *
 * No invented copy — only field mapping and structural splits of existing strings.
 */
import { readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const curated = JSON.parse(
  readFileSync(join(root, "src/data/bread-retail-curated.json"), "utf-8")
);
const shufersal = JSON.parse(
  readFileSync(join(root, "src/data/bread-retail-shufersal.json"), "utf-8")
);

/** @type {Map<string, { ingredient_architecture_summary?: string; short_summary_he?: string }>} */
const shufersalById = new Map();

function indexShufersalProduct(product) {
  if (!product?.id) return;
  const existing = shufersalById.get(product.id) ?? {};
  shufersalById.set(product.id, {
    ingredient_architecture_summary:
      product.ingredient_architecture_summary ?? existing.ingredient_architecture_summary,
    short_summary_he: product.short_summary_he ?? existing.short_summary_he,
  });
}

for (const product of shufersal.featured_products ?? []) {
  indexShufersalProduct(product);
}
for (const product of shufersal.products ?? []) {
  indexShufersalProduct(product);
}
function walkClusters(node) {
  if (!node || typeof node !== "object") return;
  if (Array.isArray(node)) {
    for (const item of node) walkClusters(item);
    return;
  }
  if (node.id && node.name_he) indexShufersalProduct(node);
  for (const value of Object.values(node)) {
    if (value && typeof value === "object") walkClusters(value);
  }
}
walkClusters(shufersal.clusters);

function mapConfidence(label) {
  if (label === "נתונים מלאים יחסית") return "verified";
  if (label === "נתונים חלקיים") return "partial";
  return "insufficient";
}

function splitStructuralSummary(summary) {
  if (!summary?.trim()) return [];
  return summary
    .split("|")
    .map((part) => part.trim())
    .filter(Boolean);
}

function mapProduct(raw) {
  const id = raw.product_id;
  const extra = shufersalById.get(id);
  const positiveSignals = splitStructuralSummary(raw.structural_summary_he);

  return {
    id,
    name: raw.name_he,
    imageUrl: raw.image_url || null,
    score: raw.score == null ? null : Math.round(raw.score),
    grade: raw.grade,
    insightLine: raw.suggested_card_blurb_he?.trim() ?? "",
    confidence: mapConfidence(raw.confidence_label_he),
    expansion: {
      nutrition: {
        energyKcal: null,
        protein: raw.protein_g ?? null,
        sugar: null,
        fat: null,
        fiber: raw.fiber_g ?? null,
        sodium: raw.sodium_mg ?? null,
      },
      ingredients: extra?.ingredient_architecture_summary ?? null,
      confidenceLabel: raw.confidence_label_he,
      servingNote: "ל-100 גרם",
      positiveSignals: positiveSignals.length > 0 ? positiveSignals : undefined,
      bottomLine: raw.suggested_card_blurb_he?.trim() || undefined,
      comparisonContext: raw.why_featured_he?.trim() || undefined,
    },
    _website_cluster: raw.website_cluster,
  };
}

const shelfProducts = curated.all_products
  .filter((product) => product.display_score_boolean)
  .map(mapProduct);

const scoredCount = shelfProducts.filter((product) => product.score != null).length;

const corpus = {
  _meta: {
    generated: `${curated.meta.generated}T12:00:00Z`,
    category: "bread",
    product_count: shelfProducts.length,
    scored_count: scoredCount,
    schema: "BariProductVM[]",
    version: "v2-production",
    expansion: "interpretive_expansion_system_v2",
    source_run_id: curated.meta.run_id,
    scope_note: curated.meta.scope_note,
    production_pass:
      "Built from CE-approved bread-retail-curated.json + bread-retail-shufersal.json; shelf order preserved from curated all_products.",
  },
  products: shelfProducts,
};

const outPath = join(root, "src/data/comparisons/bread_frontend_v2.json");
writeFileSync(outPath, `${JSON.stringify(corpus, null, 2)}\n`, "utf-8");
console.log(`Wrote ${shelfProducts.length} products to ${outPath}`);
