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

/** CE framing: 16 displayed · 53 scanned · 48 scored (hero metadata line). */
export const snacksMetadataLine = snacksMetadataUpdated
  ? `25 חטיפי דגנים בדף · 655 נסרקו · 73 קיבלו ציון · עודכן ב${snacksMetadataUpdated}`
  : "25 חטיפי דגנים בדף · 655 נסרקו · 73 קיבלו ציון";

/** Shelf hero — impulse-rack moment, distinct from cereals/juices/cheese openers. */
export const snacksHero = {
  eyebrow: "חטיפים",
  title: "קונים חטיפים בסופרמרקט? הנה מה שאתם צריכים לדעת.",
} as const;

export const snacksPrologueSentences = [
  "התור לקופה. מולכם מדף חטיפים: ברים צבעוניים, חטיפי דגנים עם הבטחות על האריזה, תמרים מצופים. 'רגע, רק משהו קטן.'",
  "החטיף נראה קטן וזמין. לפעמים הרשימה תומכת בזה — שלושה מרכיבים, דגן מלא, בוטנים. לפעמים השם אומר 'שיבולת שועל' וברשימה יושבים שוקולד, סירופ גלוקוזה ועשרה מרכיבים נוספים.",
  "גם החטיף החזק במדף הזה מגיע רק ל-B — כי כאן 'טוב' אומר פחות מהונדס, לא בריא במובן הרחב.",
] as const;

// Category caveat (cheese gold-standard format), rendered once in the header. Grounded in
// the frozen category invariant (CLAUDE.md: "No snack bar reaches A. 68/B ceiling (snk-008) is the
// validated category ceiling") and the engineered-snack scoring nuance (.claude/scoring.md
// Stage 4 — fat-sugar / fat-sodium hyper-palatability patterns). "Best" here is relative.
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
