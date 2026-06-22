import type { Metadata } from "next";

import rawCorpus from "@/data/comparisons/snacks_frontend_v5.json";

import {
  snacksShelfMethodologyLines,
  snackComparisonMeta,
} from "@/lib/blog/snack-analysis-content";
import {
  loadComparisonCorpus,
  type ComparisonCorpusMeta,
  type ComparisonCorpusRaw,
} from "@/lib/comparisons/corpus";
import type { ComparisonCategoryPageData } from "@/lib/comparisons/registry/types";
import { enrichRowReasonOnly } from "@/lib/comparisons/row-surface";
import {
  filterSnacksProducts,
  SNACKS_SHELF_LENS_OPTIONS,
  type SnacksShelfFilterId,
} from "@/lib/comparisons/snacks-shelf-filters";
import type { BariProductVM } from "@/lib/view-models";

export type SnacksCorpusMeta = ComparisonCorpusMeta;

type SnacksCorpusProduct = BariProductVM & {
  _internal_cluster?: string;
};

function stripSnacksInternalFields(products: SnacksCorpusProduct[]): BariProductVM[] {
  return products.map((product) => {
    const { _internal_cluster, ...rest } = product;
    void _internal_cluster;
    return rest;
  });
}

const loaded = loadComparisonCorpus(rawCorpus as ComparisonCorpusRaw);
const snacksCorpusMeta = loaded.meta;
// rowReason only — NO metric bar. All snack nutrition is null (the category invariant),
// so a protein bar would be fabricated; the page keeps metricSpecs={[]} (TASK-161A).
const snacksProducts = enrichRowReasonOnly(
  stripSnacksInternalFields(loaded.products as SnacksCorpusProduct[])
);

export { snacksCorpusMeta, snacksProducts };

const snacksMetadataUpdated = (() => {
  const date = new Date(snacksCorpusMeta.generated);
  return Number.isNaN(date.getTime())
    ? ""
    : date.toLocaleDateString("he-IL", { month: "long", year: "numeric" });
})();

/** Count auto-derives from the corpus so it can never go stale. */
export const snacksMetadataLine = snacksMetadataUpdated
  ? `${snacksProducts.length} חטיפי דגנים בדף · נסרקו ממדף החטיפים בשופרסל · עודכן ב${snacksMetadataUpdated}`
  : `${snacksProducts.length} חטיפי דגנים בדף · נסרקו ממדף החטיפים בשופרסל`;

/** Shelf hero — focused on grain/oat/date bars (protein bars are a separate page). */
export const snacksHero = {
  eyebrow: "חטיפי דגנים",
  title: "חטיף דגנים נשמע כמו הבחירה הבריאה במדף — הרשימה לא תמיד מסכימה",
} as const;

export const snacksPrologueSentences = [
  "חטיף דגנים, שיבולת שועל או תמרים. האריזות מבטיחות 'טבעי', 'דגן מלא', 'מקור לסיבים' — וקל להניח שכל החטיפים על המדף דומים זה לזה.",
  "הם לא. מצד אחד משפחה של חטיפי תמרים עם שניים עד שלושה רכיבים שכולם מזון ואפס סוכר מוסף; מצד שני 'חטיף דגנים' ששוקולד חלב הוא הרכיב הראשון שלו וסירופ גלוקוז השני. אותו מדף, אותה הבטחה — וציונים שנעים מ-67 עד 15.",
  "גם החטיף החזק כאן מגיע רק ל-B, כי במדף הזה 'טוב' אומר פחות מהונדס — לא בריא במובן הרחב. חטיפי חלבון מהונדסים סביב 25–34 גרם חלבון נמדדים בקטגוריה ובעמוד נפרדים.",
] as const;

// Category caveat (cheese gold-standard format), rendered once in the header. Grounded in
// the validated category ceiling (snk-001 at 66.8/B; no snack bar reaches A) and the
// engineered-snack scoring nuance (.claude/scoring.md Stage 4 — fat-sugar / fat-sodium
// hyper-palatability patterns). "Best" here is relative. Note: TASK-373 moved snk-004/008/009/010
// from E to D (clean whole-food date bars); category B ceiling is unchanged (snk-001).
export const snacksCategoryNote = [
  "הערת קטגוריה — 'הכי טוב' כאן הוא B, לא A\n\nבמדף חטיפי הדגנים אף מוצר אינו מגיע ל-A. הציון הגבוה בקטגוריה הוא 67/B. זו אינה החמרה אלא תיאור הקטגוריה: חטיפי דגנים מתוכננים סביב שילוב של דגן מעובד, סוכר ולעיתים שוקולד שמעלה את החיך — והציון משקף זאת.",
  "הערת קטגוריה — חטיפי חלבון נמצאים בעמוד נפרד\n\nהעמוד הזה מציג חטיפי דגנים בלבד. חטיפי חלבון (פרוטאין) — מוצרים מהונדסים סביב 25–34 גרם חלבון, ממתיקים ותחליפי סוכר — נמדדים בקטגוריה משלהם ומוצגים בעמוד נפרד.",
  "הערת קטגוריה — ההשוואה היא בתוך הקטגוריה בלבד\n\nחטיף נמדד מול חטיפים אחרים, לא מול מזון אחר. ציון B כאן אומר 'הטוב יחסית במדף חטיפי הדגנים' — לא שהמוצר שקול לארוחה או לבסיס מזון מלא.",
]
  .join("\n\n");

export const snacksMethodologyLines = snacksShelfMethodologyLines;

export const snacksComparisonMetadata: Metadata = {
  title: snackComparisonMeta.title,
  description: snackComparisonMeta.description,
};

function isSnacksShelfFilterId(filter: string): filter is SnacksShelfFilterId {
  return SNACKS_SHELF_LENS_OPTIONS.some((option) => option.id === filter);
}

const snacksShelfFilters = {
  lensOptions: SNACKS_SHELF_LENS_OPTIONS,
  filterProducts: (products: BariProductVM[], activeFilters: string[]) =>
    filterSnacksProducts(products, activeFilters.filter(isSnacksShelfFilterId)),
};

export function getSnacksPageData(): ComparisonCategoryPageData {
  return {
    products: snacksProducts,
    metadataLine: snacksMetadataLine,
    hero: snacksHero,
    prologueSentences: snacksPrologueSentences,
    methodologyLines: snacksMethodologyLines,
    corpusMeta: snacksCorpusMeta,
    shelfFilters: snacksShelfFilters,
  };
}

export function getSnacksCorpusPayload(): {
  _meta: SnacksCorpusMeta;
  products: BariProductVM[];
} {
  return {
    _meta: snacksCorpusMeta,
    products: snacksProducts,
  };
}
