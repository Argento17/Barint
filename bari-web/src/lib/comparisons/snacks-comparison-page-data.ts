import type { Metadata } from "next";

import rawCorpus from "@/data/comparisons/snacks_frontend_v2.json";

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
import { snackHeroLine } from "@/lib/comparisons/snack-page-data";
import type { BariProductVM } from "@/lib/view-models";

export type SnacksCorpusMeta = ComparisonCorpusMeta;

// `_internal_cluster` (the snacks lens reads its sub-pool off the snack data module,
// not the loaded VM) is now stripped centrally by loadComparisonCorpus' BariProductVM
// allowlist (TASK-233A) — no local strip needed.
const loaded = loadComparisonCorpus(rawCorpus as ComparisonCorpusRaw);
const snacksCorpusMeta = loaded.meta;
// rowReason only — NO metric bar. All snack nutrition is null (the category invariant),
// so a protein bar would be fabricated; the page keeps metricSpecs={[]} (TASK-161A).
const snacksProducts = enrichRowReasonOnly(loaded.products);

export { snacksCorpusMeta, snacksProducts };

const snacksMetadataUpdated = (() => {
  const date = new Date(snacksCorpusMeta.generated);
  return Number.isNaN(date.getTime())
    ? ""
    : date.toLocaleDateString("he-IL", { month: "long", year: "numeric" });
})();

/** CE framing: 18 displayed · 53 scanned · 48 scored (hero metadata line). */
export const snacksMetadataLine = snacksMetadataUpdated
  ? `18 מוצרים בדף · 53 נסרקו · 48 קיבלו ציון · עודכן ב${snacksMetadataUpdated}`
  : "18 מוצרים בדף · 53 נסרקו · 48 קיבלו ציון";

/** Shelf copy from CE-stabilized snack comparison hero line. */
export const snacksHero = {
  eyebrow: "חטיפים",
  title: "השוואת חטיפים",
} as const;

/** Verbatim sentences from snack-editorial-content.ts (snackShelfIntro closing lines) + snackHeroLine. */
export const snacksPrologueSentences = [
  snackHeroLine,
  "מתוך 53 מוצרים שנסרקו, 48 קיבלו ציון, ו-18 נבחרו לתצוגה על בסיס מגוון קטגוריות ופערי ציון משמעותיים.",
  "הציון הגבוה ביותר — 70/B — לא הלך לאף אחד מהשמות שהזכרנו.",
] as const;

// Category caveat (cheese gold-standard format), rendered once in the header. Grounded in
// the frozen category invariant (CLAUDE.md: "No snack bar reaches A. snk-001 = 70/B is the
// validated category ceiling") and the engineered-snack scoring nuance (.claude/scoring.md
// Stage 4 — fat-sugar / fat-sodium hyper-palatability patterns). "Best" here is relative.
export const snacksCategoryNote = [
  "הערת קטגוריה — 'הכי טוב' כאן הוא B, לא A\n\nבמדף החטיפים אף מוצר אינו מגיע ל-A. הציון הגבוה בקטגוריה הוא 70/B. זו אינה החמרה אלא תיאור הקטגוריה: חטיפים מתוכננים סביב שילוב של שומן, סוכר או מלח שמעלה את החיך — והציון משקף זאת.",
  "הערת קטגוריה — ההשוואה היא בתוך הקטגוריה בלבד\n\nחטיף נמדד מול חטיפים אחרים, לא מול מזון אחר. ציון B כאן אומר 'הטוב יחסית במדף החטיפים' — לא שהמוצר שקול לארוחה או לחטיף בריאות.",
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
