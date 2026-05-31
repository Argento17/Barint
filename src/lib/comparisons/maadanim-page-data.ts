import type { Metadata } from "next";

import rawCorpus from "@/data/comparisons/maadanim_frontend_v2.json";

import {
  formatComparisonMetadataLine,
  loadComparisonCorpus,
  type ComparisonCorpusMeta,
  type ComparisonCorpusRaw,
} from "@/lib/comparisons/corpus";
import type { ComparisonCategoryPageData } from "@/lib/comparisons/registry/types";
import {
  filterMaadanimProducts,
  MAADANIM_SHELF_LENS_OPTIONS,
  type MaadanimShelfFilterId,
} from "@/lib/comparisons/maadanim-shelf-filters";

function isMaadanimShelfFilterId(filter: string): filter is MaadanimShelfFilterId {
  return MAADANIM_SHELF_LENS_OPTIONS.some((option) => option.id === filter);
}
import type { BariProductVM } from "@/lib/view-models";

export type MaadanimCorpusMeta = ComparisonCorpusMeta;

const { meta: maadanimCorpusMeta, products: maadanimProducts } =
  loadComparisonCorpus(rawCorpus as ComparisonCorpusRaw);

export { maadanimCorpusMeta, maadanimProducts };

export function formatMaadanimMetadataLine(
  productCount: number,
  generatedIso: string
): string {
  return formatComparisonMetadataLine(productCount, generatedIso);
}

export const maadanimMetadataLine = formatMaadanimMetadataLine(
  maadanimCorpusMeta.product_count,
  maadanimCorpusMeta.generated
);

export const maadanimHero = {
  eyebrow: "מעדנים",
  title: "מה שווה לקחת מהמדף",
} as const;

export const maadanimPrologueSentences = [
  "ניתחנו עשרות מעדנים מהמדף הישראלי כדי להבין איפה ההבדלים האמיתיים מתחילים.",
  "בחלק מהמוצרים רואים מבנה רכיבים קצר ופשוט יחסית, ובאחרים עומס תוספים שמכוון בעיקר למרקם ומתיקות.",
  "הפערים לא תמיד נראים מהחזית, אבל הם מופיעים בבירור כשמסתכלים על התמונה המלאה של הקטגוריה.",
] as const;

export const maadanimMethodologyLines = [
  "הסקירה מבוססת על מוצרים שנאספו ממדפים בישראל.",
  "הערכת המוצרים נשענת על רכיבים, ערכים תזונתיים והקשר עיבודי כפי שמופיעים על האריזה.",
  "הקריאה היא יחסית לקטגוריית המעדנים עצמה ולא מול קטגוריות אחרות.",
  "הקטגוריה כוללת מעדנים מסורתיים לצד מוצרים מועשרי חלבון — שניהם משרתים שימושים שונים. ציון גבוה לא מחייב שהמוצר מתאים לכל מטרה.",
] as const;

export const maadanimComparisonMetadata: Metadata = {
  title: "השוואת מעדנים | Bari",
  description:
    "השוואת מעדנים וקינוחי חלב מהמדף הישראלי — ציון Bari, רכיבים, חלבון והקשר במדף. מידע, לא המלצה.",
};

const maadanimShelfFilters = {
  lensOptions: MAADANIM_SHELF_LENS_OPTIONS,
  filterProducts: (products: BariProductVM[], activeFilters: string[]) =>
    filterMaadanimProducts(
      products,
      activeFilters.filter(isMaadanimShelfFilterId)
    ),
};

export function getMaadanimPageData(): ComparisonCategoryPageData {
  return {
    products: maadanimProducts,
    metadataLine: maadanimMetadataLine,
    hero: maadanimHero,
    prologueSentences: maadanimPrologueSentences,
    methodologyLines: maadanimMethodologyLines,
    corpusMeta: maadanimCorpusMeta,
    shelfFilters: maadanimShelfFilters,
  };
}

export function getMaadanimCorpusPayload(): {
  _meta: MaadanimCorpusMeta;
  products: BariProductVM[];
} {
  return {
    _meta: maadanimCorpusMeta,
    products: maadanimProducts,
  };
}
