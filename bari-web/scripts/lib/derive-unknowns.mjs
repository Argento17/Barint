// derive-unknowns — single root-cause fix for the §2.5 unknowns[] gap (TASK-130D).
//
// The contract (category_module_contract_v1.md §2.5) requires: when any nutrition field
// is null on a SCORED product, expansion.unknowns[] must be non-empty — the suppressed
// metric must be disclosed, not silently dropped. The four launch builders (bread .mjs,
// snacks .ts, maadanim .py, yogurts .mjs) never emitted it. This module is the single
// shared derivation all corpora are normalized through (scripts/normalize-corpus-unknowns.mjs).
//
// Deterministic. No score changes. No editorial authoring — it instantiates the exact
// disclosure template already shipped in hummus_frontend_v3.json
// ("ערכי השומן לא היו זמינים במקור הנתונים — מדד זה לא נכלל בניתוח.").

export const NUTRITION_FIELDS = ["energyKcal", "protein", "sugar", "fat", "fiber", "sodium"];

// Definite form (single-metric line) — matches the live hummus string verbatim for fat.
const DEFINITE = {
  energyKcal: "האנרגיה",
  protein: "החלבון",
  sugar: "הסוכר",
  fat: "השומן",
  fiber: "הסיבים התזונתיים",
  sodium: "הנתרן",
};
// Bare noun (multi-metric list).
const BARE = {
  energyKcal: "אנרגיה",
  protein: "חלבון",
  sugar: "סוכר",
  fat: "שומן",
  fiber: "סיבים תזונתיים",
  sodium: "נתרן",
};

export function missingNutritionFields(nutrition) {
  if (!nutrition || typeof nutrition !== "object") return [];
  return NUTRITION_FIELDS.filter((f) => nutrition[f] === null);
}

// One deterministic disclosure line covering all suppressed metrics.
export function deriveUnknownsLine(missing) {
  if (!missing || missing.length === 0) return null;
  if (missing.length === 1) {
    return `ערכי ${DEFINITE[missing[0]]} לא היו זמינים במקור הנתונים — מדד זה לא נכלל בניתוח.`;
  }
  const nouns = missing.map((f) => BARE[f]);
  const last = nouns.pop();
  const list = `${nouns.join(", ")} ו${last}`;
  return `ערכי ${list} לא היו זמינים במקור הנתונים — מדדים אלה לא נכללו בניתוח.`;
}

// Idempotent, scored-only, never overwrites existing unknowns (no content rewrite).
// Mutates product in place. Returns true iff it added an unknowns line.
export function backfillProductUnknowns(product) {
  if (product.score === null || product.score === undefined) return false; // scored only (§2.5)
  const e = product.expansion;
  if (!e || typeof e !== "object") return false;
  if (Array.isArray(e.unknowns) && e.unknowns.length > 0) return false; // never rewrite existing
  const missing = missingNutritionFields(e.nutrition);
  if (missing.length === 0) return false;
  e.unknowns = [deriveUnknownsLine(missing)];
  return true;
}
