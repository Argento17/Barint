import type { Metadata } from "next";

import rawCorpus from "@/data/comparisons/chocolate_tablets_frontend_v1.json";

import {
  loadComparisonCorpus,
  type ComparisonCorpusMeta,
  type ComparisonCorpusRaw,
} from "@/lib/comparisons/corpus";
import type { ComparisonCategoryPageData } from "@/lib/comparisons/registry/types";
import { enrichRowReasonOnly } from "@/lib/comparisons/row-surface";
import {
  filterChocolateTabletsProducts,
  CHOCOLATE_TABLETS_SHELF_LENS_OPTIONS,
  type ChocolateTabletsShelfFilterId,
} from "@/lib/comparisons/chocolate-tablets-shelf-filters";
import type { BariProductVM } from "@/lib/view-models";

export type ChocolateTabletCorpusMeta = ComparisonCorpusMeta;

const loaded = loadComparisonCorpus(rawCorpus as ComparisonCorpusRaw);
const chocolateTabletCorpusMeta = loaded.meta;
// rowReason only — rowVerdict is authored per-product and shown collapsed.
const chocolateTabletsProducts = enrichRowReasonOnly(loaded.products as BariProductVM[]);

export { chocolateTabletCorpusMeta, chocolateTabletsProducts };

const chocolateTabletsMetadataUpdated = (() => {
  const date = new Date(chocolateTabletCorpusMeta.generated);
  return Number.isNaN(date.getTime())
    ? ""
    : date.toLocaleDateString("he-IL", { month: "long", year: "numeric" });
})();

export const chocolateTabletsMetadataLine = chocolateTabletsMetadataUpdated
  ? `${chocolateTabletsProducts.length} טבלאות שוקולד בדף · נסרקו ממדף השוקולד בשופרסל · עודכן ב${chocolateTabletsMetadataUpdated}`
  : `${chocolateTabletsProducts.length} טבלאות שוקולד בדף · נסרקו ממדף השוקולד בשופרסל`;

export const chocolateTabletsHero = {
  eyebrow: "טבלאות שוקולד",
  title: "שוקולד מריר לא הופך לבריא בגלל השם — הציון מפריד בין הקקאו האמיתי לבין הסוכר שלובש את השם",
} as const;

export const chocolateTabletsPrologueSentences = [
  "שוקולד מריר לא הופך לבריא בגלל השם: גם טבלת 70% יכולה להיות כמעט שליש סוכר, והמדף מוכיח שצריך לבדוק קקאו מול סוכר יחד.",
  "המדף הזה מחולק בבירור: קומץ טבלות שמרביתן קקאו עם מינימום סוכר, שורה ארוכה של 'מריר' שמציע אחוז קקאו גבוה על הנייר אבל סוכר שמפתיע, ותחתית של שוקולד חלב ולבן שהוא בעיקרו ממתק בכל קנה מידה.",
  "הסתכלו על שניים ביחד — אחוז הקקאו וכמות הסוכר — ותדעו בדיוק איפה כל טבלה עומדת, בלי להאמין לשם.",
] as const;

export const chocolateTabletsCategoryNote = [
  "המוצר הטוב ביותר במדף הזה מדורג C — וזה ממצא אמיתי. שוקולד הוא ממתק צפוף בשומן וסוכר, וגם הטבלה הנקייה ביותר לא מתחמקת מזה. ה-C הוא הצד הנכון של מדף הממתקים; לא מוצר בריאות.",
  "קטגוריית 'ללא סוכר' דורשת עיון בפני עצמה: חלק מהטבלות מחליפות סוכר בממתיק אחד בסיסי, אחרות בונות שלושה ממתיקים שונים ושני מתחלבים. הציון מביא בחשבון את מורכבות הנוסחה הכוללת — היעדר הסוכר הוא רק חלק אחד ממנה.",
  "'ללא סוכר' לא מדרג לבד: כשהקקאו גבוה והתחליפים לא משתלטים, הטבלה יכולה להגיע ל-C; כשהממתיק ראשון ברשימה, אחוז הקקאו נמוך, או הנוסחה עמוסה בממתיקים ומתחלבים — היא יורדת ל-D ואף E.",
  "שוקולד לבן הוא פרק בפני עצמו: אין בו מוצקי קקאו כלל — רק חמאת קקאו, חלב וסוכר. הציונים בתחתית המדף משקפים בדיוק את זה.",
].join("\n\n");

export const chocolateTabletsMethodologyLines = [
  "ניתחנו את טבלאות השוקולד במדף שופרסל — שמות, רכיבים וערכי תזונה ל-100 גרם ישירות מדף המוצר.",
  "כל ערך תזונה עבר בדיקת סבירות ל-100 גרם; פאנלים לא-סבירים הוצאו מהדירוג.",
  "הציון נשען על אחוז הקקאו, כמות הסוכר, סוג השומן ורמת העיבוד — לא על כמות השוקולד בלבד.",
  "ציוני Bari מתעדים מבנה מוצר ואינם המלצה תזונתית.",
] as const;

export const chocolateTabletsComparisonMetadata: Metadata = {
  title: "השוואת טבלאות שוקולד | Bari",
  description:
    "השוואת טבלאות שוקולד מהמדף הישראלי — ציון Bari, אחוז קקאו, כמות סוכר ורמת עיבוד. מידע, לא המלצה.",
};

const chocolateTabletsShelfFilters = {
  lensOptions: CHOCOLATE_TABLETS_SHELF_LENS_OPTIONS,
  filterProducts: (products: BariProductVM[], activeFilters: string[]) =>
    filterChocolateTabletsProducts(
      products,
      activeFilters.filter((f): f is ChocolateTabletsShelfFilterId =>
        CHOCOLATE_TABLETS_SHELF_LENS_OPTIONS.some((o) => o.id === f)
      )
    ),
};

export function getChocolateTabletsPageData(): ComparisonCategoryPageData {
  return {
    products: chocolateTabletsProducts,
    metadataLine: chocolateTabletsMetadataLine,
    hero: chocolateTabletsHero,
    prologueSentences: chocolateTabletsPrologueSentences,
    methodologyLines: chocolateTabletsMethodologyLines,
    corpusMeta: chocolateTabletCorpusMeta,
    shelfFilters: chocolateTabletsShelfFilters,
  };
}

export function getChocolateTabletsCorpusPayload(): {
  _meta: ChocolateTabletCorpusMeta;
  products: BariProductVM[];
} {
  return { _meta: chocolateTabletCorpusMeta, products: chocolateTabletsProducts };
}
