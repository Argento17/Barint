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

/**
 * TASK-161B is display-only: it must NOT change any score/grade/confidence that is
 * already live. We load the existing shipped file and, for any id present there,
 * preserve its score/grade/confidence verbatim (only limitingFactors is added).
 * If the builder's curated-derived grade disagrees with the live grade, we keep the
 * live value and record the divergence in _meta.grade_divergences for escalation —
 * we never silently ship a grade change under a signals task.
 */
let liveById = new Map();
let gradeDivergences = [];
try {
  const live = JSON.parse(
    readFileSync(join(root, "src/data/comparisons/bread_frontend_v2.json"), "utf-8")
  );
  for (const p of live.products ?? []) {
    liveById.set(p.id, { score: p.score, grade: p.grade, confidence: p.confidence });
  }
} catch {
  // no existing live file (first build) — builder-derived values stand.
}

function splitStructuralSummary(summary) {
  if (!summary?.trim()) return [];
  return summary
    .split("|")
    .map((part) => part.trim())
    .filter(Boolean);
}

/**
 * TASK-161B — deterministic limitingFactors[] for the bread "rich row" amber (-).
 *
 * Derived ONLY from the CE-approved curated status fields (the same real signals
 * the engine's signal_* functions read): fermentation_status_he, fiber_source_status_he,
 * seed_halo_status_he, refined-flour base (from structural_summary_he), and the
 * measured sodium_mg. No invented copy, no score/grade change. Honors engine-v2
 * governance: every factor names a specific, real characteristic with its value
 * where one exists; none of the 9 banned phrases is used. Salience-ordered, top 2.
 *
 * A product with a genuinely clean profile (whole-grain base + real fermentation +
 * grain-sourced fiber + no seed halo + moderate sodium) legitimately yields [].
 */
const BANNED_PHRASES = [
  "עיבוד מרבי", "בסיס מהונדס", "ריבוי ממתיקים", "מיצוב פיטנס", "מוצר מעובד מאוד",
  "בעיית סוכר", "חלבון נמוך", "מרכיבים רבים", "ציון בסיסי",
];

function computeLimitingFactors(raw) {
  const ranked = []; // [salience, phrase]
  const summary = raw.structural_summary_he || "";

  // L1 — refined-flour base (structural; the defining limiter for non-wholegrain bread).
  if (summary.includes("בסיס קמח מזוקק")) {
    ranked.push([1, "בסיס קמח מזוקק — לא דגן מלא"]);
  } else if (summary.includes("בסיס דגן — לא ברור")) {
    ranked.push([1, "בסיס הדגן לא ברור מהרשימה — לא ניתן לאשר דגן מלא"]);
  }

  // L2 — fiber not from the grain (laundering: added inulin/chicory, or unclear source).
  const fiberStatus = raw.fiber_source_status_he || "";
  if (fiberStatus.includes("מתוספים")) {
    ranked.push([2, "חלק מהסיבים מתוספים (אינולין / ציקוריה) — לא מבסיס דגן מלא"]);
  } else if (fiberStatus.includes("לא ברור")) {
    ranked.push([2, "מקור הסיבים לא ברור — לא ניתן לייחס אותם לדגן מלא"]);
  }

  // L3 — fermentation claimed by name but not real (sourdough halo).
  const fermStatus = raw.fermentation_status_he || "";
  if (fermStatus.includes("מחמצת בשם")) {
    ranked.push([3, "מחמצת בשם — ברשימת הרכיבים מופיעים שמרים, לא תסיסה אמיתית"]);
  }

  // L4 — seed halo over a refined base (seeds suggest health the base does not deliver).
  const seedStatus = raw.seed_halo_status_he || "";
  if (seedStatus.includes("בסיס מזוקק")) {
    ranked.push([4, "זרעים על בסיס מזוקק — מראה בריא על בסיס קמח לבן"]);
  }

  // L5 — high sodium (real measured value; >=500mg/100g is high for bread).
  const sodium = raw.sodium_mg;
  if (typeof sodium === "number" && sodium >= 500) {
    ranked.push([5, `נתרן גבוה — ${Number.isInteger(sodium) ? sodium : Math.round(sodium)} מ"ג ל-100 גרם`]);
  }

  ranked.sort((a, b) => a[0] - b[0]);
  const factors = ranked.slice(0, 2).map(([, phrase]) => phrase);
  for (const f of factors) {
    for (const b of BANNED_PHRASES) {
      if (f.includes(b)) throw new Error(`banned phrase '${b}' in bread limitingFactor: ${f}`);
    }
  }
  return factors;
}

function mapProduct(raw) {
  const id = raw.product_id;
  const extra = shufersalById.get(id);
  const positiveSignals = splitStructuralSummary(raw.structural_summary_he);
  const limitingFactors = computeLimitingFactors(raw);

  // Display-only guard: preserve any live score/grade/confidence (TASK-161B).
  const derivedScore = raw.score == null ? null : Math.round(raw.score);
  const derivedGrade = raw.grade;
  const derivedConfidence = mapConfidence(raw.confidence_label_he);
  const live = liveById.get(id);
  const score = live ? live.score : derivedScore;
  const grade = live ? live.grade : derivedGrade;
  const confidence = live ? live.confidence : derivedConfidence;
  if (live && live.grade !== derivedGrade) {
    gradeDivergences.push({ id, name: raw.name_he, live_grade: live.grade, curated_grade: derivedGrade, score });
  }

  return {
    id,
    name: raw.name_he,
    imageUrl: raw.image_url || null,
    score,
    grade,
    insightLine: raw.suggested_card_blurb_he?.trim() ?? "",
    confidence,
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
      limitingFactors: limitingFactors.length > 0 ? limitingFactors : undefined,
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
    signals_task: "TASK-161B",
    signals_note:
      "limitingFactors[] added deterministically from curated status fields (fermentation/fiber-source/seed-halo/sodium); display-only, live scores/grades preserved.",
    ...(gradeDivergences.length > 0
      ? {
          grade_divergences: gradeDivergences,
          grade_divergences_note:
            "Live grade preserved (display-only task). Curated source disagrees — escalate for separate grade reconciliation; NOT resolved by TASK-161B.",
        }
      : {}),
  },
  products: shelfProducts,
};

const outPath = join(root, "src/data/comparisons/bread_frontend_v2.json");
writeFileSync(outPath, `${JSON.stringify(corpus, null, 2)}\n`, "utf-8");
const withLimiting = shelfProducts.filter((p) => p.expansion.limitingFactors).length;
console.log(`Wrote ${shelfProducts.length} products to ${outPath}`);
console.log(`  with limitingFactors: ${withLimiting} | without: ${shelfProducts.length - withLimiting}`);
if (gradeDivergences.length > 0) {
  console.log(`  GRADE DIVERGENCES (live preserved, escalate): ${JSON.stringify(gradeDivergences)}`);
}
