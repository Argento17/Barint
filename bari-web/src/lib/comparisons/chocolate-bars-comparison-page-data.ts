import type { Metadata } from "next";

import { withComparisonOpenGraph } from "@/lib/seo/open-graph";

import rawCorpus from "@/data/comparisons/chocolate_bars_frontend_v1.json";

import {
  loadComparisonCorpus,
  type ComparisonCorpusMeta,
  type ComparisonCorpusRaw,
} from "@/lib/comparisons/corpus";
import type { ComparisonCategoryPageData } from "@/lib/comparisons/registry/types";
import { enrichRowReasonOnly } from "@/lib/comparisons/row-surface";
import {
  filterChocolateBarsProducts,
  CHOCOLATE_BARS_SHELF_LENS_OPTIONS,
  type ChocolateBarsShelfFilterId,
} from "@/lib/comparisons/chocolate-bars-shelf-filters";
import type { BariProductVM } from "@/lib/view-models";

export type ChocolateBarsCorpusMeta = ComparisonCorpusMeta;

const loaded = loadComparisonCorpus(rawCorpus as ComparisonCorpusRaw);
const chocolateBarsCorpusMeta = loaded.meta;
// rowReason only — rowVerdict is authored per-product and shown collapsed.
const chocolateBarsProducts = enrichRowReasonOnly(loaded.products as BariProductVM[]);

export { chocolateBarsCorpusMeta, chocolateBarsProducts };

const chocolateBarsMetadataUpdated = (() => {
  const date = new Date(chocolateBarsCorpusMeta.generated);
  return Number.isNaN(date.getTime())
    ? ""
    : date.toLocaleDateString("he-IL", { month: "long", year: "numeric" });
})();

export const chocolateBarsMetadataLine = chocolateBarsMetadataUpdated
  ? `${chocolateBarsProducts.length} חטיפי שוקולד בדף · נסרקו ממדף החטיפים בשופרסל · עודכן ב${chocolateBarsMetadataUpdated}`
  : `${chocolateBarsProducts.length} חטיפי שוקולד בדף · נסרקו ממדף החטיפים בשופרסל`;

export const chocolateBarsHero = {
  eyebrow: "חטיפי שוקולד",
  title: "חטיפי השוקולד האלה הם חטיפי ממתק, לא חטיפי ביניים — וכולם יודעים את זה",
} as const;

export const chocolateBarsPrologueSentences = [
  "כל מוצר במדף הזה הוא אותו דבר ביסודו: ציפוי שוקולד על מילוי קרמל, נוגט, ביסקוויט או ופל, מחוברים בסירופ גלוקוז ושמן צמחי, עם 27 עד 60 גרם סוכר ל-100 גרם — וברוב המדף מעל 45.",
  "ההבדלים ביניהם שוליים — קצת יותר אגוזים כאן, קצת פחות סוכר שם — אבל אף אחד מהם אינו יוצא מאזור הממתק.",
  "המילה 'חטיף' היא שיווק; ההבדל האמיתי היחיד הוא בין החטיפים שיש בהם פירור אוכל אמיתי, בוטנים או אגוזים, לבין אלה שהם רק סוכר ושמן מתחת לשוקולד.",
] as const;

export const chocolateBarsCategoryNote = [
  "כל מוצר במדף הזה מקבל ציון E. זה לא מחמיר, זה מדויק: זו קטגוריה אחת של ממתקים, וההשוואה היא בתוכה.",
  "כשמוצר מדורג גבוה כאן, זה לא אומר שהוא טוב — זה אומר שהוא הכי פחות מהונדס: יש בו רכיב אחד שהוא אוכל ממש, או פחות סוכר, או רשימה קצרה יותר.",
  "אנחנו לא אומרים ולעולם לא נאמר לכם מה לאכול. אנחנו כן אומרים שכשקונים חטיף שוקולד, כדאי לדעת שקונים ממתק.",
].join("\n\n");

export const chocolateBarsMethodologyLines = [
  "ניתחנו את חטיפי השוקולד במדף שופרסל — שמות, רכיבים וערכי תזונה ל-100 גרם ישירות מדף המוצר.",
  "כל ערך תזונה עבר בדיקת סבירות ל-100 גרם; פאנלים לא-סבירים הוצאו מהדירוג.",
  "הציון נשען על כמות הסוכר, סוג המילוי, רמת העיבוד ואורך רשימת הרכיבים — לא על גודל החטיף.",
  "ציוני Bari מתעדים מבנה מוצר ואינם המלצה תזונתית.",
] as const;

export const chocolateBarsComparisonMetadata: Metadata = withComparisonOpenGraph({
  title: "השוואת חטיפי שוקולד | Bari",
  description:
    "השוואת חטיפי שוקולד מהמדף הישראלי — ציון Bari, כמות סוכר, רכיבים ורמת עיבוד. מידע, לא המלצה.",
});

const chocolateBarsShelfFilters = {
  lensOptions: CHOCOLATE_BARS_SHELF_LENS_OPTIONS,
  filterProducts: (products: BariProductVM[], activeFilters: string[]) =>
    filterChocolateBarsProducts(
      products,
      activeFilters.filter((f): f is ChocolateBarsShelfFilterId =>
        CHOCOLATE_BARS_SHELF_LENS_OPTIONS.some((o) => o.id === f)
      )
    ),
};

export function getChocolateBarsPageData(): ComparisonCategoryPageData {
  return {
    products: chocolateBarsProducts,
    metadataLine: chocolateBarsMetadataLine,
    hero: chocolateBarsHero,
    prologueSentences: chocolateBarsPrologueSentences,
    methodologyLines: chocolateBarsMethodologyLines,
    corpusMeta: chocolateBarsCorpusMeta,
    shelfFilters: chocolateBarsShelfFilters,
  };
}

export function getChocolateBarsCorpusPayload(): {
  _meta: ChocolateBarsCorpusMeta;
  products: BariProductVM[];
} {
  return { _meta: chocolateBarsCorpusMeta, products: chocolateBarsProducts };
}
