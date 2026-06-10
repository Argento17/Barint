import type { Metadata } from "next";

import rawCorpus from "@/data/comparisons/cheese_frontend_v3.json";

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

// `_cluster` (read off the raw JSON by cheese-shelf-filters) is now stripped centrally
// by loadComparisonCorpus' BariProductVM allowlist (TASK-233A) — no local strip needed.
const loaded = loadComparisonCorpus(rawCorpus as ComparisonCorpusRaw);
const cheeseCorpusMeta = loaded.meta;

// The Shufersal scrape carried the same physical product under several barcodes: e.g.
// "גבינה לבנה 5% שומן" appears 3× at 82/A and 3× at 79/B with byte-identical nutrition and
// the same verdict, so the shelf showed runs of indistinguishable rows. With no brand field
// to tell them apart, disambiguation isn't possible — collapse rows that are identical in
// every displayed dimension (name + score + per-100g nutrition), keeping the first. This
// only touches true duplicates: the קוטג' 5% trio (87/84/75) differs on protein, so all
// three correctly survive.
function dedupeIdenticalProducts(products: BariProductVM[]): BariProductVM[] {
  const seen = new Set<string>();
  return products.filter((product) => {
    const n = product.expansion?.nutrition;
    // FIX-6: use Math.round(score) so two products with raw scores differing by
    // <1pt (e.g. 82.1 vs 82.4) collapse correctly when they display the same chip value.
    const sig = JSON.stringify([
      product.name,
      product.score != null ? Math.round(product.score) : null,
      n?.protein ?? null,
      n?.fat ?? null,
      n?.satFat ?? null,
      n?.sodium ?? null,
      n?.energyKcal ?? null,
    ]);
    if (seen.has(sig)) return false;
    seen.add(sig);
    return true;
  });
}

const cheeseProducts = dedupeIdenticalProducts(
  enrichRowSurface(loaded.products)
);

export { cheeseCorpusMeta, cheeseProducts };

export const cheeseMetadataLine = `${cheeseProducts.length} מוצרים נבדקו · מדגם מדף ישראלי · ממוין לפי ציון Bari`;

export const cheeseHero = {
  eyebrow: "מנוע השוואה · גבינות לבנות וממרחים",
  title: "גבינה לבנה: מה מפריד גבינה מממרח?",
} as const;

// Reviewed & refined by Content Agent against the insight-line spec (TASK-152;
// recalibrated TASK-169B). Numbers cite the rounded chip values (ScoreChip renders
// Math.round): leader קוטג' 1% = 90/A; 9 products reach A after the identical-row dedupe
// below (was 11 — two of the A's were byte-identical duplicates of גבינה לבנה 5% שומן).
// The two 9% cottages are held at 81/B by the A-gate (high on the data, but saturated
// fat over the line). Cream-cheese
// pool falls on real fat (16–30%, EV-029) into C/D/E.
export const cheesePrologueSentences = [
  "בדקנו את מדף הגבינות הלבנות והממרחים בשופרסל לפי מה שבאמת באריזה — חלבון, שומן וערכים תזונתיים כפי שמופיעים על המוצר עצמו. המדף מתפצל לארבע קבוצות: קוטג', גבינה לבנה / קוורק, ממרחי גבינת שמנת, ולבנה.",
  "הקוטג' והגבינות הלבנות הרזות מובילות את המדף — בסיס חלבי, הרבה חלבון מול מעט שומן. בראש עומד קוטג' 1% עם 90/A, ותשע גבינות טריות מגיעות ל-A.",
  "ממרחי גבינת השמנת הם סיפור אחר: ברגע שסופרים את השומן האמיתי שבהם — 16 עד 30 אחוז — החלבון מתגמד והם נופלים ל-C, D ואף E, גם כשהשם 'גבינה' זהה.",
  "ו'הכי טוב' עדיין לא אומר 'מושלם': אפילו גבינה עתירת חלבון יכולה להיעצר ב-B אם השומן הרווי שלה גבוה — כמו הקוטג' 9%, שנשאר ב-81/B דווקא מהסיבה הזו.",
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
  "ציון A שמור לגבינות שהן גם נקיות במלח ובשומן רווי — שני הדברים שהציון עצמו אינו משקלל. כך ש-A כאן אומר טוב על פי הנתונים, וגם נקי במה שהנתונים לא רואים; גבינה עתירת חלבון אך עשירה בשומן רווי נעצרת ב-B.",
  "חלק מהמוצרים שנסרקו לא הוצגו: נתוני תווית חלקיים, או מוצר ששויך לקטגוריה אחרת.",
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
