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

// ─── Glass Box D5/D6 (presentation-only, flag-gated) ────────────────────────────
// TASK-179I Wave 1. Carries the engine's D5/D6 gate output to the UI as PLAIN-LANGUAGE
// findings only — never raw numbers, never engine terms (DEC-006 Q4). This object is
// purely additive and is read ONLY when the NEXT_PUBLIC_GLASSBOX_D5D6 frontend flag is ON;
// absent or flag-OFF → the UI is byte-identical to today. It never participates in scoring,
// sorting, or rounding — it annotates an already-decided VM.
//
//  - "demote"  → product keeps its grade chip + carries a calm `ניתוח חלקי` flag + a plain
//                one-line note of what was not disclosed (partialNote).
//  - "withhold"→ product shows `לא נוקד` where the grade chip would be, with a plain reason
//                (withholdReason) — never a number, never an error look.
//  - "unconstrained" → no glass-box surface (a normal graded row).
export type BariGlassBoxGate = "unconstrained" | "demote" | "withhold";

export interface BariGlassBoxVM {
  gateState: BariGlassBoxGate;
  /** TASK-179N — CODED disclosure-gap vocabulary the engine emits (the live JSON path).
   *  Vocabulary: proportions | compound | generic_additive | protein_source | missing_field.
   *  These codes are mapped to calm Hebrew lines at render time via the Content-owned map in
   *  view-models/glass-box-copy.ts — the JSON carries NO prose. Empty/absent for a clean
   *  withhold (panel simply absent) or unconstrained product. */
  disclosureCodes?: string[];
  /** TASK-179N — true on a withheld product (panel absent / unscored). Mirrors gateState
   *  === "withhold"; carried explicitly because that is what Data emits. */
  withheld?: boolean;
  /** TASK-179N — the score/grade the engine would have assigned before the D5 demote.
   *  PRESENTATION-IRRELEVANT: never rendered (the published grade chip still shows). Carried
   *  for provenance/parity only; the UI never reads these as a number (DEC-006 Q4). */
  gatedScore?: number;
  gatedGrade?: BariGrade;
  /** Legacy prose render targets — authored directly only by the self-contained /dev preview
   *  dataset (glass-box-preview-data.ts). The LIVE pages carry codes, not prose; these stay
   *  optional so the preview keeps working. Source of truth for live prose is the code→Hebrew
   *  map (view-models/glass-box-copy.ts), NOT these fields.
   *  Calm, factual register — never intent attribution ("היצרן מסתיר" is forbidden). */
  partialNote?: string | null;
  /** Plain-Hebrew reason a product is unscored (withhold). Legacy prose target — see above. */
  withholdReason?: string | null;
  /** Optional plain-language disclosure findings (demote). Legacy prose target — see above. */
  disclosureNotes?: string[];
}

// Content-owned code→Hebrew copy map + resolvers, re-exported so canonical shared
// components read every glass-box string via `@/lib/view-models` only (legacy isolation).
export {
  GLASS_BOX_DISCLOSURE_LINES,
  GLASS_BOX_PARTIAL_LABEL,
  GLASS_BOX_PARTIAL_TOOLTIP,
  GLASS_BOX_DISCLOSURE_HEADING,
  GLASS_BOX_WITHHOLD_LABEL,
  GLASS_BOX_WITHHOLD_REASON,
  resolveDisclosureLines,
  resolveWithholdReason,
} from "./glass-box-copy";

// ─── D4 Additive Tier (Glass Box W2, TASK-179T) ─────────────────────────────────
// Presentation-only. No score field. Disclosure/transparency surface only.
// Tier taxonomy: 6 active tiers. "confirmed-negative" additives are scoring-level
// vetoes and never appear in the D4 panel (they do not reach product.d4_additives).
// Hebrew explanations come from the Content-owned TASK-179U sign-off.
// DEC-006 Q3 posture: no alarm framing for any tier including contested/dose-dependent.
export type AdditiveTier =
  | "functional"
  | "likely-neutral"
  | "dose-dependent"
  | "contested"
  | "disclosure-gap"
  | "unclassified";

export interface AdditiveEntry {
  /** E-number string, e.g. "E407". Displayed as a secondary parenthetical only —
   *  never as the primary visible label (DEC-006). */
  e_number: string;
  /** Hebrew common name. Always the primary label. Example: "קרגינן". */
  name_he: string;
  tier: AdditiveTier;
  /** Technological function in Hebrew. Shown in the "עוד" expanded sub-row. */
  function_he: string;
  /** Plain-language Hebrew one-liner. Max ~12 words (spec §5.1). Content sign-off required
   *  (TASK-179U) before final ship. Draft copy from additive_prototype_set_v1.md acceptable
   *  during build. */
  explanation_he: string;
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
  /** TASK-179I: Glass Box D5/D6 presentation state. Optional + flag-gated (read only when
   *  NEXT_PUBLIC_GLASSBOX_D5D6 is ON). Absent → no glass-box surface. Presentation only. */
  glassBox?: BariGlassBoxVM;
  /** TASK-179T: Glass Box W2 D4 additive tier data. Optional + flag-gated (same gate as
   *  glassBox: NEXT_PUBLIC_GLASSBOX_D5D6). Absent / empty → AdditivePanel renders empty
   *  state (לא זוהו תוספי מזון — still rendered, not hidden). Presentation only — no score
   *  movement. Populated by TASK-179S (Data pipeline D4 detector). */
  d4_additives?: AdditiveEntry[];
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
