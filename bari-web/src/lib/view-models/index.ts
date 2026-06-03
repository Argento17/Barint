// Bari Comparison View Model — canonical frontend contract.
// All BSIP outputs must be transformed into these types before reaching the UI.
// The UI layer never imports from lib/comparisons/, lib/bsip/, or any scoring module.

export type BariGrade = "A" | "B" | "C" | "D" | "E";

// "verified" maps from backend "full" — language boundary lives here
export type BariConfidence = "verified" | "partial" | "insufficient";

// ─── Nutrition ────────────────────────────────────────────────────────────────
// All values are per 100g or 100ml. Backend normalizes and rounds. UI never rounds.
// null = data not available → hide cell. 0 is valid → display it.
export interface BariNutritionVM {
  energyKcal: number | null;
  protein: number | null;
  sugar: number | null;
  fat: number | null;
  /** Saturated fat g per 100g/ml (TASK-168J). Optional/absent on categories whose source
   *  JSON predates the field; null = data not available → row hidden. Additive, non-breaking. */
  satFat?: number | null;
  fiber: number | null;
  sodium: number | null;
}

// ─── Expansion ────────────────────────────────────────────────────────────────
// Always present on BariProductVM. Content fields may be null.
// confidenceLabel is pre-rendered by backend — UI renders verbatim.
// servingNote is always present (e.g. "ל-100 גרם").
//
// Interpretive Expansion v2 (optional): pre-authored shelf reasoning only.
// UI renders verbatim — no BSIP, NOVA, caps, dimensions, or score mechanics.
export interface BariExpansionVM {
  nutrition: BariNutritionVM | null;
  ingredients: string | null;
  confidenceLabel: string;
  servingNote: string;
  /** מה שבלט — 1–3 observable strengths (Hebrew strings). */
  positiveSignals?: string[];
  /** מה שהגביל — 0–2 compositional limits (no cap/score language). */
  limitingFactors?: string[];
  /** מה שלא ניתן לאמת — data gaps Bari could not verify (e.g. suppressed fat). */
  unknowns?: string[];
  /** הערות — product-level caveats (partial-data, confidence, routing). */
  caveats?: string[];
  /** Editorial synthesis — בשורה התחתונה. */
  bottomLine?: string;
  /** Shelf-relative context without algorithm vocabulary. */
  comparisonContext?: string | null;
}

// ─── Metrics (v2 — comparison_ui_reference_v2 §2.1, §4) ─────────────────────────
// Display-only, column-aligned metric block. Derived deterministically from existing
// label data — NEVER a score input. null = data not available → render "—", never 0.
// The metric SET rendered is category-scoped (README §7, MILK_RECOMMENDATION): the
// MetricColumn reads a per-category spec, so milk can show sugar where hummus shows
// % grain without forking the component. All fields optional/nullable: a category
// only populates the metrics it has real source data for — we never fabricate a value.
export interface BariProductMetricsVM {
  /** g per 100g/ml. Display scale 0–20 (hummus); good ≥10, poor <5 (§4.1). */
  protein_g: number | null;
  /** Fiber g per 100g — bread's headline metric (TASK-162). Real per-label value, never fabricated. */
  fiber_g?: number | null;
  /** Count of recognised additives, 0–5 pips. NOT yet exposed by BSIP → Data Agent dependency. */
  additive_count?: number | null;
  /** Main-ingredient %, bar 0–100. NOT in current label data → Data Agent dependency. */
  base_pct?: number | null;
  /** Sugar g per 100g/ml — a real dairy signal (MILK_RECOMMENDATION §1). */
  sugar_g?: number | null;
}

// ─── Row reason (v2 — comparison_ui_reference_v2 §3.3) ───────────────────────────
// Short strongest +/− shown beneath the name on the collapsed row. Derived from
// positiveSignals[0] / limitingFactors[0]; both null → slot collapses. Optional.
export interface BariRowReasonVM {
  positive: string | null;
  limiting: string | null;
}

// ─── Product ──────────────────────────────────────────────────────────────────
// The single unit of shelf rendering.
// insightLine: pre-authored Hebrew string. "" = no insight slot rendered.
// score: null = unscored (chip renders "—"). Present = 0–100 integer, already rounded.
// expansion: always present; content nullability is per-field.
// metrics / rowReason: optional v2 surface (§2.2). Absent on non-v2 categories.
export interface BariProductVM {
  id: string;
  name: string;
  imageUrl: string | null;
  score: number | null;
  grade: BariGrade | null;
  insightLine: string;
  confidence: BariConfidence;
  expansion: BariExpansionVM;
  metrics?: BariProductMetricsVM;
  rowReason?: BariRowReasonVM;
  /** TASK-137: 2–3 sentence editorial verdict shown on the collapsed row in place of
   *  the +/− reason lines (which move into the "למה קיבל את הציון?" expansion). Authored
   *  by Content; display-only, never a score input. Absent → row falls back to rowReason. */
  rowVerdict?: string;
}

// ─── Filter ───────────────────────────────────────────────────────────────────
// id is opaque to the UI — never branch on its value.
// label is pre-rendered Hebrew. count is pre-computed.
// First filter in the array is always the "all" filter.
export interface BariFilterVM {
  id: string;
  label: string;
  count: number;
  isActive: boolean;
}

// ─── Hero ─────────────────────────────────────────────────────────────────────
// averageScore: null if fewer than 3 scored products exist.
// topProduct: null if no product has score >= 60.
// UI never computes these — it receives them.
export interface BariHeroVM {
  categoryNameHe: string;
  tagline: string;
  productCount: number;
  scoredCount: number;
  averageScore: number | null;
  topProduct: {
    name: string;
    score: number;
    grade: BariGrade;
  } | null;
}

// ─── Prologue ─────────────────────────────────────────────────────────────────
// 2–3 pre-authored sentences. UI renders them sequentially.
export interface BariPrologueVM {
  sentences: string[];
}

// ─── Methodology ──────────────────────────────────────────────────────────────
// Entirely pre-authored. UI renders verbatim. No computation.
export interface BariMethodologyVM {
  text: string;
  sourceNote: string | null;
  lastUpdated: string | null;
}

// ─── Category Page ────────────────────────────────────────────────────────────
// The complete payload for one category comparison page.
// products: pre-ordered (scored desc, insufficient appended last). UI never sorts.
// filters: pre-ordered, first entry is always "all".
export interface BariCategoryPageVM {
  hero: BariHeroVM;
  prologue: BariPrologueVM;
  products: BariProductVM[];
  filters: BariFilterVM[];
  methodology: BariMethodologyVM;
}
