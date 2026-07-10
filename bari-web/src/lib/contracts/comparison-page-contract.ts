// TASK-569 — generation source for the page-output JSON Schema.
//
// WHAT THIS FILE IS
// Encodes the shape of the RAW served comparison JSON under
// `src/data/comparisons/*_frontend_v*.json` — the files page-data.ts modules
// (e.g. bread-comparison-page-data.ts, milk-page-data.ts) import directly, BEFORE any
// page-data transform runs. It is deliberately NOT `BariProductVM`
// (`src/lib/view-models/index.ts`): the VM is the post-transform, UI-facing contract.
// The two diverge on purpose in several places the pipeline already ships live —
// documented inline below wherever a field differs from its VM counterpart.
//
// WHY IT EXISTS
// `03_operations/page_generator/contract/page_output_schema_v1.json` is hand-maintained
// and has repeatedly lagged what the pipeline actually emits (TASK-564). This file is the
// single TS source of truth `scripts/schema/generate-page-schema.mjs` (ts-json-schema-generator)
// reads to produce a JSON Schema that can be diffed against the hand-maintained one and,
// once adopted, regenerated instead of hand-edited.
//
// PROVENANCE
// Every field below was verified against the highest-version live dataset for all 18
// currently-served categories (bread v4, brined_cheeses v2, cakes_hard_cookies v1,
// cereals v2, cheese v5, chocolate_bars v1, chocolate_tablets v1, cookies_coffee v2,
// crackers v1, granola v2, hard_cheeses v4, hummus v5, juices v3, milk v1,
// protein_combined v2, snacks v5, yogurt_drinkable v1, yogurt_spoonable v1 — 681 products
// total) on 2026-07-10 (TASK-569). `required` reflects fields present on 681/681 products;
// fields present on fewer are optional, with the observed category subset noted.
//
// TYPES ONLY. Zero runtime import — this file exists purely as a ts-json-schema-generator
// source and must never be imported by component/runtime code (would violate the View
// Model boundary: components read `@/lib/view-models`, never raw pipeline shapes).

// ─── Grade / confidence (raw values — NOT the same enums as the VM) ────────────────
//
// Raw `grade` includes "S" (4/681 live products carry it; owner ruling: engine grades
// are never capped — see owner_s_grade_honesty_ruling memory). `BariGrade` in
// view-models/index.ts is "A"|"B"|"C"|"D"|"E" ONLY — the page-data / ScoreChip layer
// folds S→A at render time. The raw contract must allow "S"; the VM must not.
export type RawGrade = "S" | "A" | "B" | "C" | "D" | "E";

// Raw `confidence` observed values across all 18 live datasets: "full", "partial",
// "verified" (some already-converted categories, e.g. milk, store "verified" directly).
// "insufficient" is not observed on any CURRENTLY live product but is part of the
// documented confidence state model (VM comment: "verified" maps from backend "full" —
// language boundary lives here) — kept in the enum for that state.
export type RawConfidence = "full" | "partial" | "insufficient" | "verified";

// ─── Nutrition (expansion.nutrition) ────────────────────────────────────────────────
// All values per 100g/100ml. null = data not available. Observed on 681/681 products.
export interface RawNutrition {
  energyKcal: number | null;
  protein: number | null;
  sugar: number | null;
  fat: number | null;
  fiber: number | null;
  sodium: number | null;
  /** Present on 237/681 (bread/brined_cheeses/cakes_hard_cookies/cereals/cheese/hard_cheeses/milk). */
  carbs?: number | null;
  /** Present on 370/681 (bread/brined_cheeses/cakes_hard_cookies/cereals/cheese/cookies_coffee/hard_cheeses/juices/milk). */
  satFat?: number | null;
}

// ─── Limiting factor entry ───────────────────────────────────────────────────────────
// TASK-346 introduced { text, magnitude } as a richer alternative to a plain string.
// LIVE FINDING (TASK-569): `magnitude` is NOT uniformly numeric. chocolate_bars /
// chocolate_tablets / snacks emit magnitude as a small integer (1-3, not a 0-1
// continuum as the VM JSDoc claims). cereals emits magnitude as a Hebrew-adjacent
// enum STRING: "high" | "medium" | "low". Both shapes are live today — the raw
// contract must accept `number | string` even though BariExpansionVM's TS type
// (`limitingFactors?: ... { text: string; magnitude: number }[]`) only declares
// number. This is a genuine VM/raw divergence, not a typo — flagged in the schema
// diff for the adopting agent, not silently "fixed" here.
export interface RawLimitingFactorEntry {
  text: string;
  magnitude: number | string;
}

// ─── Expansion ───────────────────────────────────────────────────────────────────────
// Always present (681/681). Sub-field presence varies by category — see per-field notes.
export interface RawExpansion {
  nutrition: RawNutrition | null;
  ingredients: string | null;
  confidenceLabel: string;
  servingNote: string;
  /** Present 681/681; value is `[]` or `null` on categories that ship no signals yet. */
  positiveSignals?: string[] | null;
  /** Present 678/681 (all but 3 low-data products, TASK-564). Legacy string[] or the
   *  richer {text,magnitude}[] shape — see RawLimitingFactorEntry. */
  limitingFactors?: (string | RawLimitingFactorEntry)[] | null;
  /** Present only on hummus (57/681) in current data; category-level invariant per category. */
  unknowns?: string[];
  /** Present only on hummus (57/681) in current data. */
  caveats?: string[];
  /** Present only on cookies_coffee (117/681) in current data. */
  bottomLine?: string;
  /** Present on 409/681 (14/18 categories). De-cross-referencing (TASK-546) means this
   *  is optional going forward — never re-require without an owner ruling (TASK-564). */
  comparisonContext?: string | null;
  /** Declared on BariExpansionVM (sourceLine, consumerExplanation) but not observed on
   *  ANY live product in the current 18-category corpus. Kept optional/typed so a future
   *  emission does not immediately violate the contract. */
  sourceLine?: string | null;
  consumerExplanation?: {
    whyRated: string;
    good: string[];
    watchOut: string[];
    context: string;
    takeaway: string;
  } | null;
}

// ─── D4 additive tier entry ──────────────────────────────────────────────────────────
// tier values observed live: functional, likely-neutral, contested, dose-dependent,
// disclosure-gap, unclassified — the full AdditiveTier union from view-models is used
// as-is (raw and VM agree here).
export type RawAdditiveTier =
  | "functional"
  | "likely-neutral"
  | "dose-dependent"
  | "contested"
  | "disclosure-gap"
  | "unclassified";

export interface RawAdditiveEntry {
  e_number: string;
  name_he: string;
  tier: RawAdditiveTier;
  function_he: string;
  explanation_he: string;
  /** Present on 94/2039 additive entries (chocolate_bars/chocolate_tablets/snacks). */
  cosmetic_mup?: boolean;
}

// ─── Glass Box D5/D6 (raw) ────────────────────────────────────────────────────────────
// Observed only on hummus (57/681). Only "unconstrained" and "demote" gateState values
// are live; "withhold" is part of the documented state machine (BariGlassBoxGate) but
// not currently emitted by any category.
export type RawGlassBoxGate = "unconstrained" | "demote" | "withhold";

export interface RawGlassBox {
  gateState: RawGlassBoxGate;
  disclosureCodes?: string[];
  withheld?: boolean;
  gatedScore?: number;
  gatedGrade?: RawGrade;
  partialNote?: string | null;
  withholdReason?: string | null;
  disclosureNotes?: string[];
}

// ─── D3 processing signal (raw trace shape — distinct from BariProcessingSignalVM) ───
// Observed only on hummus (57/681). This is the raw pipeline's `d3_processing_signal`
// key, NOT the VM's `d3_processing` (BariProcessingSignalVM) — no live category emits
// the VM-shaped key today, but the raw trace shape below is real and 10-key-identical
// across all 57 observed entries (matches the existing hand-maintained schema's
// `d3_processing_signal` definition — TASK-564).
export interface RawD3ProcessingSignal {
  nova_class: number | null;
  confidence: string | null;
  confidence_note: string | null;
  uncertainty_materiality: string | null;
  materiality_note: string | null;
  population_correlation: number | null;
  modifier: number | null;
  modifier_note: string | null;
  note_he: string | null;
  note_he_mobile: string | null;
}

// ─── Metrics (display-only) ──────────────────────────────────────────────────────────
// LIVE FINDING (TASK-569): the current hand-maintained schema's comment claims metrics
// is "Synthesized by page-data layer, not in source JSON" — that is stale. `metrics` IS
// present in the raw milk_frontend_v1.json (18/18 milk products: { protein_g, sugar_g }).
export interface RawMetrics {
  protein_g?: number | null;
  fiber_g?: number | null;
  additive_count?: number | null;
  base_pct?: number | null;
  sugar_g?: number | null;
  sodium_mg?: number | null;
  fat_saturated_g?: number | null;
}

// ─── Bari interpretation entry (both pipeline-version shapes) ───────────────────────
export type RawBariInterpretationEntry =
  | { key: string; label: string; score: number; strength: string; interpretation: string }
  | { dimension: string; score: number; label_he: string; explanation_he: string };

// ─── Product ──────────────────────────────────────────────────────────────────────────
// One entry in `products[]`. `required` = present on 681/681 live products.
export interface RawComparisonProduct {
  id: string;
  name: string;
  barcode: string;
  /** Nullable per pipeline contract (schema/VM); no live product currently has null. */
  imageUrl: string | null;
  /** Nullable for INSUFFICIENT-confidence products; no live product currently has null. */
  score: number | null;
  grade: RawGrade | null;
  confidence: RawConfidence;
  confidence_label_he: string;
  confidence_tooltip_he: string;
  insightLine: string;
  expansion: RawExpansion;

  /** Present 680/681 — the sole exception is hummus product bsip1_7290010154265,
   *  which omits the key entirely (TASK-569 finding; not this task's job to fix). */
  d4_additives?: RawAdditiveEntry[];

  /** Present 659/681. */
  rowVerdict?: string;
  /** Present 553/681 (13/18 categories; absent on chocolate_bars, chocolate_tablets,
   *  juices, protein_combined, snacks). */
  retailer?: string;
  /** Present 614/681 (absent on yogurt_drinkable, yogurt_spoonable). */
  rank?: number;
  /** Present 591/681. */
  categoryTotal?: number;
  /** Present 606/681; null/absent = unknown, never fabricated. */
  brand?: string | null;
  /** Metadata-only, non-rendering. Present 663/681 (absent on milk). */
  confidence_sub_reason?: string | null;
  /** Present 250/681 (bread/cereals/cheese/crackers/granola/milk/yogurt_drinkable/yogurt_spoonable). */
  confidence_level?: string;
  /** Present 320/681 (bread/cereals/cheese/crackers/hard_cheeses/hummus/yogurt_drinkable/yogurt_spoonable). */
  source_traceability_status?: string;
  /** Present 364/681 (brined_cheeses/cakes_hard_cookies/cheese/cookies_coffee/juices/milk/yogurt_drinkable/yogurt_spoonable). */
  novaGroup?: number | null;

  // ── Internal / provenance-only fields (underscore-prefixed; whitelisted 2026-06-18/07-01) ──
  /** Present 216/681. Membership-correction reproducibility marker. */
  _hash_no_rank?: string | null;
  /** Present 42/681 (bread, crackers). */
  _website_cluster?: string;
  /** Present 122/681 (cakes_hard_cookies, cookies_coffee). */
  _category_routed?: string | null;
  _has_phvo?: boolean | null;
  _source_retailers?: string[] | null;
  /** Present 42/681 (cereals, granola). */
  _subpool?: string | null;
  _isChildrens?: boolean | null;
  _wholeGrainClaim?: boolean | null;
  /** Present 57/681 (hummus). */
  _product_type?: string;

  /** Present 53/681 (crackers only). Content-authored Hebrew display name. */
  nameHe?: string | null;

  /** Present 57/681 (hummus only). */
  glassBox?: RawGlassBox;
  d3_processing_signal?: RawD3ProcessingSignal;

  // ── Category-scoped render fields (TASK-316) — juices ──────────────────────────
  /** Present 17/681 (juices only). */
  retailers?: string[] | null;
  subPool?: string | null;
  sugarPer100ml?: number | null;
  kcalPer100ml?: number | null;
  volumeMl?: number | null;

  // ── Category-scoped render fields — milk ────────────────────────────────────────
  /** Present 18/681 (milk only). */
  filterTags?: string[];
  milkProductType?: string | null;
  milkProductTypeLabel?: string | null;
  metrics?: RawMetrics;

  // ── Deep-dive fields (TASK-332) — yogurt_drinkable/yogurt_spoonable ───────────────
  /** Present 67/681; always `[]` in current data (shape reserved for future authoring). */
  bariInterpretation?: RawBariInterpretationEntry[];
  bestUseCases?: string[];
  consumerTakeaway?: string;

  /** Declared in the hand-maintained schema (S-grade explanation) but NOT observed on
   *  ANY of the 4 live S-grade products across all 18 categories — dead in the current
   *  corpus. Kept optional/typed rather than dropped so a future emission is still valid. */
  s_grade_explanation?: string;
}

// ─── _meta ────────────────────────────────────────────────────────────────────────────
// Highly variable per-run pipeline changelog block. Only `category`, `generated`, and
// `product_count` are present on all 18 live datasets — everything else is a one-off
// provenance/changelog key added by a specific TASK's build step (e.g. task433_*,
// task483_traceability). The index signature intentionally keeps this permissive: _meta
// is pipeline-internal, never consumer-rendered, and new one-off changelog keys are
// expected on every future build — constraining them would recreate the exact
// hand-maintained-schema-lag failure class this task exists to prevent.
export interface RawPageMeta {
  category: string;
  generated: string;
  product_count: number;
  scored_count?: number;
  schema?: string;
  version?: string;
  expansion?: string;
  source_run_id?: string;
  run_id?: string;
  scope_note?: string;
  editorial_note?: string;
  provenance?: string;
  production_pass?: string;
  [key: string]: unknown;
}

// ─── page_copy ────────────────────────────────────────────────────────────────────────
// Page-level authored copy block (hero/prologue/methodology/caveat/filters). Present on
// 7/18 live datasets (cakes_hard_cookies, cheese, cookies_coffee, hard_cheeses, milk,
// yogurt_drinkable, yogurt_spoonable). Consumed by frontend page-data, not a per-product
// scoring field — kept as a loose record; its internal shape is a page-data concern, not
// this contract's.
export type RawPageCopy = Record<string, unknown>;

// ─── Category page (top level) ──────────────────────────────────────────────────────
// The complete on-disk shape of one `*_frontend_v*.json` dataset.
export interface ComparisonPageContract {
  _meta: RawPageMeta;
  products: RawComparisonProduct[];
  /** Present on 7/18 datasets — see RawPageCopy. */
  page_copy?: RawPageCopy;
  /** Root-level (no _meta wrapper) — juices only. Distinct from _meta.generated; read
   *  directly by juices-page-data.ts for the rendered "updated on" date (TASK-574). */
  generatedAt?: string;
  /** Root-level (no _meta wrapper) — juices only (TASK-574). */
  totalProducts?: number;
}
