import type { Metadata } from "next";

import rawCorpus from "@/data/comparisons/salty_snacks_frontend_v4.json";

import {
  formatComparisonMetadataLine,
  loadComparisonCorpus,
  type ComparisonCorpusMeta,
  type ComparisonCorpusRaw,
} from "@/lib/comparisons/corpus";
import type { ComparisonCategoryPageData } from "@/lib/comparisons/registry/types";
import {
  filterSaltySnacksProducts,
  SALTY_SNACKS_SHELF_LENS_OPTIONS,
  type SaltySnacksShelfFilterId,
} from "@/lib/comparisons/salty-snacks-shelf-filters";
import type { BariProductVM } from "@/lib/view-models";

export type SaltySnacksCorpusMeta = ComparisonCorpusMeta;

function isSaltySnacksShelfFilterId(
  filter: string
): filter is SaltySnacksShelfFilterId {
  return SALTY_SNACKS_SHELF_LENS_OPTIONS.some((option) => option.id === filter);
}

const { meta: saltySnacksCorpusMeta, products: _saltySnacksProductsRaw } =
  loadComparisonCorpus(rawCorpus as ComparisonCorpusRaw);

// Populate fiber_g metric from nutrition panel — fiber is the headline differentiator
// for salty snacks (baked legume snacks vs processed extruded puffs vs plain rice cakes).
// The subPool field is preserved from the raw corpus so shelf filters can read it.
const saltySnacksProducts: BariProductVM[] = _saltySnacksProductsRaw.map(
  (p) => ({
    ...p,
    metrics: {
      protein_g: p.expansion?.nutrition?.protein ?? null,
      fiber_g: p.expansion?.nutrition?.fiber ?? null,
      sodium_mg: p.expansion?.nutrition?.sodium ?? null,
    },
    rowVerdict: p.insightLine,
  })
);

export { saltySnacksCorpusMeta, saltySnacksProducts };

export const saltySnacksMetadataLine = formatComparisonMetadataLine(
  saltySnacksProducts.length,
  saltySnacksCorpusMeta.generated
);

export const saltySnacksHero = {
  eyebrow: "חטיפים מלוחים",
  title: "הבמבה מקבל C — והכי גבוה במדף עוצר ב-B.",
} as const;

// TASK-226 COPY-LOCK: single shelf-investigator line. Removed the stat-dump prologue
// (counts / grams / grade names) and any leaked scoring-axis names.
export const saltySnacksPrologueSentences = [
  "עברנו על מדף החטיפים המלוחים בסופר, מקצה לקצה, ומיינו אותו בשבילכם.",
] as const;

// Category caveat — visible without scroll on mobile (spec requirement).
// Grounded in the real scoring logic: per-100g basis vs actual serving size gap.
export const saltySnacksCategoryNote =
  "הדירוג מבוסס על 100 גרם. חטיפים נמכרים בשקיות של 50–200 גרם — כדאי לבדוק כמה סידרת לאכול, לא רק מה הציון.";

export const saltySnacksMethodologyLines = [
  "בדקנו 41 חטיפים מלוחים ממדף יוחננוף — רכיבים, ערכי תזונה ורמת עיבוד.",
  "הציונים יחסיים לקטגוריית חטיפים מלוחים בלבד; מוצר עם A בקטגוריה זו אינו בהכרח שקול ל-A בקטגוריה אחרת.",
  "מוצרים עם נתוני רכיבים חלקיים מסומנים בהתאם — הציון מבוסס על מה שזמין על האריזה.",
  "מסד הנתונים עודכן ביוני 2026 — ייתכן שינויים בנוסחאות שאינם משתקפים עדיין בציון.",
] as const;

export const saltySnacksComparisonMetadata: Metadata = {
  title: "השוואת חטיפים מלוחים | Bari",
  description:
    "השוואת 41 חטיפים מלוחים מהמדף הישראלי — ציון Bari, רכיבים, ערכי תזונה ורמת עיבוד. מידע, לא המלצה.",
};

const saltySnacksShelfFilters = {
  lensOptions: SALTY_SNACKS_SHELF_LENS_OPTIONS,
  filterProducts: (products: BariProductVM[], activeFilters: string[]) =>
    filterSaltySnacksProducts(
      products,
      activeFilters.filter(isSaltySnacksShelfFilterId)
    ),
};

export function getSaltySnacksPageData(): ComparisonCategoryPageData {
  return {
    products: saltySnacksProducts,
    metadataLine: saltySnacksMetadataLine,
    hero: saltySnacksHero,
    prologueSentences: saltySnacksPrologueSentences,
    methodologyLines: saltySnacksMethodologyLines,
    corpusMeta: saltySnacksCorpusMeta,
    shelfFilters: saltySnacksShelfFilters,
  };
}

export function getSaltySnacksCorpusPayload(): {
  _meta: SaltySnacksCorpusMeta;
  products: BariProductVM[];
} {
  return {
    _meta: saltySnacksCorpusMeta,
    products: saltySnacksProducts,
  };
}
