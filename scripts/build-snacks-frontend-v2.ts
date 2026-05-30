/**
 * DEPRECATED for production shelf — CE Handoff v2 corpus is canonical at
 * src/data/comparisons/snacks_frontend_v2.json (18 products, score order, full expansion).
 *
 * Do NOT run this script after CE v2 — it maps snack-page-data.ts without limitingFactors
 * and uses fixture order, not CE score-descending order.
 *
 * Legacy: mapped snack-page-data.ts displayable rows only.
 */
import { writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

import {
  SNACK_REPORT_STATS,
  snackProducts,
} from "../src/lib/comparisons/snack-page-data";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const outPath = join(root, "src/data/comparisons/snacks_frontend_v2.json");

const NOVA_TAG = /^NOVA/i;
const CAP_TAG = /\bcap\b/i;

function approvedExplainabilityTags(tags: string[]): string[] {
  return tags
    .map((tag) => tag.trim())
    .filter((tag) => tag.length > 0 && !NOVA_TAG.test(tag) && !CAP_TAG.test(tag));
}

function mapConfidence(
  level: (typeof snackProducts)[number]["confidence_level"]
): "verified" | "partial" | "insufficient" {
  if (level === "full") return "verified";
  if (level === "partial") return "partial";
  return "insufficient";
}

function mapProduct(raw: (typeof snackProducts)[number]) {
  const observation = raw.key_observation_he?.trim() ?? "";
  const positiveSignals = approvedExplainabilityTags(raw.explainability_tags);

  return {
    id: raw.id,
    name: raw.name_he,
    imageUrl: raw.image_url ?? null,
    score: raw.score == null ? null : Math.round(raw.score),
    grade: raw.grade,
    insightLine: observation,
    confidence: mapConfidence(raw.confidence_level),
    expansion: {
      nutrition: {
        energyKcal: null,
        protein: null,
        sugar: null,
        fat: null,
        fiber: null,
        sodium: null,
      },
      ingredients: null,
      confidenceLabel: raw.confidence_label_he,
      servingNote: "ל-100 גרם",
      positiveSignals: positiveSignals.length > 0 ? positiveSignals : undefined,
      bottomLine: observation || undefined,
      comparisonContext: raw.segment?.trim() || undefined,
    },
    _internal_cluster: raw.cluster_id,
  };
}

const shelfProducts = snackProducts.filter((product) => product.displayable).map(mapProduct);

const scoredCount = shelfProducts.filter((product) => product.score != null).length;

const corpus = {
  _meta: {
    generated: "2026-05-01T12:00:00Z",
    category: "snacks",
    product_count: shelfProducts.length,
    scored_count: scoredCount,
    schema: "BariProductVM[]",
    version: "v2-production",
    expansion: "interpretive_expansion_system_v2",
    source_run_id: "yochananof_snack_retail_v1",
    scope_note: `ניתוח מדף ${SNACK_REPORT_STATS.retailer} בלבד — לא סקר שוק ישראלי`,
    production_pass:
      "Built from CE-approved snack-page-data.ts displayable products; array order preserved; NOVA/cap tags excluded from shelf-facing signals.",
  },
  products: shelfProducts,
};

writeFileSync(outPath, `${JSON.stringify(corpus, null, 2)}\n`, "utf-8");
console.log(`Wrote ${shelfProducts.length} products to ${outPath}`);
