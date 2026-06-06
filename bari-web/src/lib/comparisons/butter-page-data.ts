import type { Metadata } from "next";

import rawCorpus from "@/data/comparisons/butter_frontend_v2.json";

import {
  formatComparisonMetadataLine,
  loadComparisonCorpus,
  type ComparisonCorpusMeta,
  type ComparisonCorpusRaw,
} from "@/lib/comparisons/corpus";
import type { ComparisonCategoryPageData } from "@/lib/comparisons/registry/types";
import {
  filterButterProducts,
  BUTTER_SHELF_LENS_OPTIONS,
  type ButterShelfFilterId,
} from "@/lib/comparisons/butter-shelf-filters";
import type { BariProductVM } from "@/lib/view-models";

export type ButterCorpusMeta = ComparisonCorpusMeta;

function isButterShelfFilterId(filter: string): filter is ButterShelfFilterId {
  return BUTTER_SHELF_LENS_OPTIONS.some((option) => option.id === filter);
}

const { meta: butterCorpusMeta, products: butterProducts } =
  loadComparisonCorpus(rawCorpus as ComparisonCorpusRaw);

export { butterCorpusMeta, butterProducts };

export const butterMetadataLine = formatComparisonMetadataLine(
  butterProducts.length,
  butterCorpusMeta.generated
);

export const butterHero = {
  eyebrow: "חמאה",
  title: "חמאה: מה שמשנה הוא המלח — לא הדגל על האריזה",
} as const;

export const butterPrologueSentences = [
  "בדקנו את מדף החמאות הישראלי: חמאות ייבוא ומקומיות, מלוחות ולא מלוחות, חמאות טהורות, ממרחים ומתובלות.",
  "הממצא המרכזי: כל החמאות הטהורות — קרי גולד, לורפק, פרזידן, טרה, יוטבתה ועשרים ואחת חברות נוספות — מגיעות לאותו ציון בדיוק. המנוע רואה שמנת ושומן חלב, ואין בתווית מידע שמבדיל ביניהן.",
  "ההבחנה שבאמת נמצאת בנתונים: מלח. חמאה מלוחה מקבלת תווית אדומה על נתרן לפי תקן בריאות ישראלי, ויורדת 20 נקודות.",
  "מעבר לזה, יש שני סוגים שיוצאים מהמדף הרגיל לגמרי: ממרח שנמכר בשם חמאה אבל בנוי ממים, 13% שומן חלב ורשימת תוספים ארוכה — וחמאה מתובלת עם שמן צמחי מוסף בבסיס.",
] as const;

export const butterCategoryNote =
  "הניתוח מבוסס על הרכב הרכיבים והערכים התזונתיים כפי שמופיעים על האריזה. חמאה גולמית טהורה — שמנת בלבד, ללא תוספות — מגיעה לאותו ציון בדיוק בין אם מקורה מאירלנד, מצרפת או מישראל: המנוע רואה רכיבים זהים, ומשקלל אותם באופן זהה. ההבחנות שבאמת משנות על המדף הזה הן שלוש: מלח (שמוסיף תווית אדומה ומוריד 20 נקודות), תוספות מזוניות שמשנות את אופי המוצר מחמאה לממרח, ותיבול שמשנה גם את ההרכב הבסיסי. מידע על מרעה, עונתיות או מקור גיאוגרפי לא מופיע בצורה אחידה על תוויות המוצרים הנמכרים בישראל, ולכן הוא אינו חלק מהניקוד כיום.";

export const butterMethodologyLines = [
  "המנוע מנתח שומן חלב, נתרן, סוג תוספות ואורך רשימת הרכיבים כפי שמופיעים על האריזה.",
  "B הוא תקרת הקטגוריה — חמאה טהורה היא מזון שומן שלם ואינה מגיעה ל-A; מלח, תוספות ועיבוד מנמיקים את הציון מ-B כלפי מטה.",
] as const;

export const butterComparisonMetadata: Metadata = {
  title: "השוואת חמאה | Bari",
  description:
    "השוואת 39 מוצרי חמאה מהמדף הישראלי — ציון Bari, רכיבים, ערכי תזונה ורמת עיבוד. מידע, לא המלצה.",
};

const butterShelfFilters = {
  lensOptions: BUTTER_SHELF_LENS_OPTIONS,
  filterProducts: (products: BariProductVM[], activeFilters: string[]) =>
    filterButterProducts(
      products,
      activeFilters.filter(isButterShelfFilterId)
    ),
};

export function getButterPageData(): ComparisonCategoryPageData {
  return {
    products: butterProducts,
    metadataLine: butterMetadataLine,
    hero: butterHero,
    prologueSentences: butterPrologueSentences,
    methodologyLines: butterMethodologyLines,
    corpusMeta: butterCorpusMeta,
    shelfFilters: butterShelfFilters,
  };
}

export function getButterCorpusPayload(): {
  _meta: ButterCorpusMeta;
  products: BariProductVM[];
} {
  return {
    _meta: butterCorpusMeta,
    products: butterProducts,
  };
}
