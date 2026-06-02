import type { Metadata } from "next";

import rawCorpus from "@/data/comparisons/hummus_frontend_v3.json";

import {
  loadComparisonCorpus,
  type ComparisonCorpusMeta,
  type ComparisonCorpusRaw,
} from "@/lib/comparisons/corpus";
import type { ComparisonCategoryPageData } from "@/lib/comparisons/registry/types";
import { enrichRowSurface } from "@/lib/comparisons/row-surface";
import {
  filterVegetableSpreadsProducts,
  VEGETABLE_SPREADS_SHELF_LENS_OPTIONS,
  type VegetableSpreadsShelfFilterId,
} from "@/lib/comparisons/vegetable-spreads-shelf-filters";
import type { BariProductVM } from "@/lib/view-models";

export type VegetableSpreadsCorpusMeta = ComparisonCorpusMeta;

type VegetableSpreadsCorpusProduct = BariProductVM & {
  _product_type?: string;
};

// Vegetable-spread product types to include on this page.
const VEGETABLE_SPREAD_TYPES = new Set([
  "matbucha",
  "eggplant_spread",
  "pepper_spread",
]);

function buildVegetableSpreadsProducts(
  products: VegetableSpreadsCorpusProduct[]
): BariProductVM[] {
  return products
    .filter((product) => VEGETABLE_SPREAD_TYPES.has(product._product_type ?? ""))
    .map((product) => {
      const { _product_type, ...rest } = product;
      void _product_type;
      return rest;
    });
}

const loaded = loadComparisonCorpus(rawCorpus as unknown as ComparisonCorpusRaw);
export const vegetableSpreadsCorpusMeta: VegetableSpreadsCorpusMeta = loaded.meta;
export const vegetableSpreadsProducts = enrichRowSurface(
  buildVegetableSpreadsProducts(loaded.products as VegetableSpreadsCorpusProduct[])
);

export const vegetableSpreadsMetadataLine = `${vegetableSpreadsProducts.length} מוצרים בדירוג · שופרסל, מאי 2026 · ממוין לפי ציון Bari`;

export const vegetableSpreadsHero = {
  eyebrow: "מנוע השוואה · ממרחי ירקות",
  title: "ממרחי ירקות: מה באמת יש במדף?",
} as const;

export const vegetableSpreadsPrologueSentences = [
  "בדקנו ממרחי ירקות הנמכרים בשופרסל — לפי הרכב המוצר, רשימת הרכיבים, סימוני האריזה ומבנה המוצר.",
  "הקטגוריה כוללת מטבוחה, ממרח חצילים וממרח פלפלים.",
  `כל ${vegetableSpreadsProducts.length} המוצרים המוצגים מקבלים ציון.`,
  "ממרחי חומוס ומסבחה מוצגים בדף נפרד.",
] as const;

// Category caveat (cheese gold-standard format), rendered once in the header. This page
// draws from the same source corpus as hummus (hummus_frontend_v3.json), so it inherits the
// documented fat-data limitation (hummusCategoryNote). Second nuance: matbucha / eggplant /
// pepper spreads are cooked-vegetable + oil bases — the score reads the ingredient list and
// processing, but fat is not displayed for this source.
export const vegetableSpreadsCategoryNote = [
  "הערת קטגוריה — ערכי שומן אינם מוצגים\n\nבקטגוריה זו ערכי השומן אינם מוצגים בשל מגבלות באיכות מקור הנתונים. ממרחי ירקות נשענים לרוב על שמן כבסיס — שימו לב לכך בתווית גם כשהציון גבוה יחסית.",
  "הערת קטגוריה — ההשוואה היא בתוך הקטגוריה בלבד\n\nמטבוחה, ממרח חצילים וממרח פלפלים נמדדים זה מול זה בלבד — לא מול חומוס או מזון אחר. הציון משקף את רשימת הרכיבים ורמת העיבוד כפי שהם מופיעים על האריזה.",
]
  .join("\n\n");

export const vegetableSpreadsMethodologyLines = [
  "הציון מחושב לפי מדדים מרובים: רמת עיבוד המוצר, נטל תוספי המזון, הרכב הערכים התזונתיים ומדדים נוספים הנוגעים למבנה המוצר.",
  "הציון הסופי הוא ממוצע משוקלל על סולם של 0 עד 100. ההשוואה היא קטגורית בלבד — כל מוצר מוערך ביחס לממרחי ירקות בלבד.",
  "הדירוג נועד לעזור בהשוואה בין מוצרים ואינו מהווה המלצה תזונתית אישית.",
] as const;

export const vegetableSpreadsComparisonMetadata: Metadata = {
  title: "השוואת ממרחי ירקות | Bari",
  description:
    "בדקנו ממרחי ירקות — מטבוחה, ממרח חצילים וממרח פלפלים — בשופרסל לפי הרכב המוצר, רשימת הרכיבים ומבנה המוצר.",
};

function isVegetableSpreadsShelfFilterId(
  filter: string
): filter is VegetableSpreadsShelfFilterId {
  return VEGETABLE_SPREADS_SHELF_LENS_OPTIONS.some((option) => option.id === filter);
}

const vegetableSpreadsShelfFilters = {
  lensOptions: VEGETABLE_SPREADS_SHELF_LENS_OPTIONS,
  filterProducts: (products: BariProductVM[], activeFilters: string[]) =>
    filterVegetableSpreadsProducts(
      products,
      activeFilters.filter(isVegetableSpreadsShelfFilterId)
    ),
};

export function getVegetableSpreadsPageData(): ComparisonCategoryPageData {
  return {
    products: vegetableSpreadsProducts,
    metadataLine: vegetableSpreadsMetadataLine,
    hero: vegetableSpreadsHero,
    prologueSentences: vegetableSpreadsPrologueSentences,
    methodologyLines: vegetableSpreadsMethodologyLines,
    corpusMeta: vegetableSpreadsCorpusMeta,
    shelfFilters: vegetableSpreadsShelfFilters,
  };
}

export function getVegetableSpreadsCorpusPayload(): {
  _meta: VegetableSpreadsCorpusMeta;
  products: BariProductVM[];
} {
  return {
    _meta: vegetableSpreadsCorpusMeta,
    products: vegetableSpreadsProducts,
  };
}
