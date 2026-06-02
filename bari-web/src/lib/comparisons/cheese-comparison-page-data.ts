import type { Metadata } from "next";

import rawCorpus from "@/data/comparisons/cheese_frontend_v1.json";

import {
  loadComparisonCorpus,
  type ComparisonCorpusMeta,
  type ComparisonCorpusRaw,
} from "@/lib/comparisons/corpus";
import type { ComparisonCategoryPageData } from "@/lib/comparisons/registry/types";
import { enrichRowSurface } from "@/lib/comparisons/row-surface";
import {
  filterCheeseProducts,
  CHEESE_SHELF_LENS_OPTIONS,
  type CheeseShelfFilterId,
} from "@/lib/comparisons/cheese-shelf-filters";
import type { BariProductVM } from "@/lib/view-models";

export type CheeseCorpusMeta = ComparisonCorpusMeta;

type CheeseCorpusProduct = BariProductVM & { _cluster?: string };

// Strip the internal `_cluster` (used only by the shelf-lens filter) before the
// VM reaches the UI — the UI never sees sub-pool routing fields.
function stripCheeseInternalFields(
  products: CheeseCorpusProduct[]
): BariProductVM[] {
  return products.map((product) => {
    const { _cluster, ...rest } = product;
    void _cluster;
    return rest;
  });
}

const loaded = loadComparisonCorpus(rawCorpus as ComparisonCorpusRaw);
const cheeseCorpusMeta = loaded.meta;
const cheeseProducts = enrichRowSurface(
  stripCheeseInternalFields(loaded.products as CheeseCorpusProduct[])
);

export { cheeseCorpusMeta, cheeseProducts };

export const cheeseMetadataLine = `${cheeseCorpusMeta.product_count} מוצרים נבדקו · מדגם מדף ישראלי · ממוין לפי ציון Bari`;

export const cheeseHero = {
  eyebrow: "מנוע השוואה · גבינות לבנות וממרחים",
  title: "גבינה לבנה: מה מפריד גבינה מממרח?",
} as const;

// Reviewed & refined by Content Agent against the insight-line spec (TASK-152).
// Numbers cite the rounded chip values (ScoreChip renders Math.round): top 77/B; no A on
// the shelf (the lone macro-A was withheld at source). Cream-cheese pool falls on real
// fat (16–30%, EV-029).
export const cheesePrologueSentences = [
  "בדקנו את מדף הגבינות הלבנות והממרחים בשופרסל לפי מה שבאמת באריזה — חלבון, שומן וערכים תזונתיים כפי שמופיעים על המוצר עצמו. המדף מתפצל לארבע קבוצות: קוטג', גבינה לבנה / קוורק, ממרחי גבינת שמנת, ולבנה.",
  "הקוטג' והגבינות הלבנות מובילות את המדף — בסיס חלבי, חלבון של עד 11.5 גרם ל-100 גרם מול מעט שומן. הציון הגבוה הוא 77/B.",
  "ממרחי גבינת השמנת הם סיפור אחר: ברגע שסופרים את השומן האמיתי שבהם — 16 עד 30 אחוז — החלבון מתגמד והם נופלים ל-C ו-D, גם כשהשם 'גבינה' זהה.",
  "במדף הזה 'הכי טוב' הוא B — ולא יותר. אף מוצר לא מגיע ל-A.",
] as const;

// The 2 PO-approved Sec 6.4 disclosures (run_cheese_003, carried verbatim from the
// package via cheese_frontend_v1.json _meta.disclosures) + the labaneh n=1 standalone
// condition, rendered ONCE in the single header categoryNote slot (IMP-6).
const D = cheeseCorpusMeta as ComparisonCorpusMeta & {
  disclosures?: Record<string, string>;
};
const cheeseDisclosures = D.disclosures ?? {};

export const cheeseCategoryNote = [
  cheeseDisclosures.category_wide_sodium_satfat,
  cheeseDisclosures.pool_specific_light_reformulation,
  cheeseDisclosures.labaneh_n1_condition,
  "הערת קטגוריה — סיבים תזונתיים\n\nמוצרי חלב כמעט אינם מציינים סיבים תזונתיים על התווית, ולכן ערך זה אינו נכנס לניתוח בקטגוריה זו.",
]
  .filter((line): line is string => typeof line === "string" && line.length > 0)
  .join("\n\n");

export const cheeseMethodologyLines = [
  "הסקירה מבוססת על גבינות לבנות וממרחים שנאספו ממדף שופרסל בישראל.",
  "לכל מוצר נבחנו הרכב הרכיבים, רמת החלבון, תוספי המייצבים, רמת העיבוד והתסיסה כפי שמופיעים על האריזה.",
  "ההשוואה היא קטגורית בלבד — כל מוצר מוערך ביחס לגבינות לבנות וממרחים, לא מול קטגוריות אחרות.",
  "חלק מהמוצרים שנסרקו לא הוצגו: נתוני תווית חלקיים, מוצר ששויך לקטגוריה אחרת, ומוצר יחיד שציון ה-A שלו נמנע במקור.",
  "הדירוג נועד לעזור בהשוואה בין מוצרים ואינו מהווה המלצה תזונתית אישית.",
] as const;

export const cheeseComparisonMetadata: Metadata = {
  title: "השוואת גבינות לבנות וממרחים | Bari",
  description:
    "השוואה בין גבינות לבנות, קוטג', ממרחי גבינת שמנת ולבנה — לפי רכיבים, חלבון, שומן ורמת עיבוד.",
};

function isCheeseShelfFilterId(filter: string): filter is CheeseShelfFilterId {
  return CHEESE_SHELF_LENS_OPTIONS.some((option) => option.id === filter);
}

const cheeseShelfFilters = {
  lensOptions: CHEESE_SHELF_LENS_OPTIONS,
  filterProducts: (products: BariProductVM[], activeFilters: string[]) =>
    filterCheeseProducts(products, activeFilters.filter(isCheeseShelfFilterId)),
};

export function getCheesePageData(): ComparisonCategoryPageData {
  return {
    products: cheeseProducts,
    metadataLine: cheeseMetadataLine,
    hero: cheeseHero,
    prologueSentences: cheesePrologueSentences,
    methodologyLines: cheeseMethodologyLines,
    corpusMeta: cheeseCorpusMeta,
    shelfFilters: cheeseShelfFilters,
  };
}

export function getCheeseCorpusPayload(): {
  _meta: CheeseCorpusMeta;
  products: BariProductVM[];
} {
  return {
    _meta: cheeseCorpusMeta,
    products: cheeseProducts,
  };
}
