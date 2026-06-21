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
  title: "כל השוקולד הוא ממתק — אבל חלק מהטבלאות קרובות לקקאו אמיתי, ואחרות הן בעיקר סוכר שלובש את השם",
} as const;

export const chocolateTabletsPrologueSentences = [
  "בואו נסכים על משהו לפני שמתחילים: כל טבלת שוקולד על המדף הזה היא ממתק, ואף אחת מהן אינה 'בריאה' — השאלה היחידה היא איזו מהן קרובה יותר לקקאו ואיזו קרובה יותר לסוכר.",
  "המרחק האמיתי במדף הוא בין שלושה צירים: אחוז הקקאו, כמות הסוכר המוספת, והאם יש מילוי — מריר 90% נושא כשני גרם סוכר ל-100 גרם, בעוד שוקולד לבן וטבלאות ממולאות מגיעים ל-58 עד 65 גרם.",
  "לחובבי המריר הצד הנקי כאן הוא הקצה הגבוה של הקקאו; לחובבי המילק והלבן זה פינוק מתוק לכל דבר — וההשוואה הזו עוזרת לבחור טוב יותר בתוך השוקולד, לא במקומו.",
] as const;

export const chocolateTabletsCategoryNote = [
  "המוצר הטוב ביותר במדף הזה מדורג C, לא A או B — וזה לא טעות. שוקולד הוא ממתק, וגם הטבלה הנקייה ביותר נושאת שומן וקלוריות גבוהים. ה-C מסמן את הצד הנכון של מדף הממתקים, לא מוצר 'בריא'.",
  "ההשוואה כאן היא בתוך עולם השוקולד בלבד. אנחנו לא מציעים אותו כתחליף לאוכל אמיתי — רק עוזרים לבחור בין טבלה לטבלה.",
  "טבלאות הקקאו הגבוה (85%–90%) מדורגות גבוה יותר בעיקר כי יש בהן הרבה פחות סוכר, ולא כי הן 'בריאות'. שוקולד לבן וטבלאות ממולאות יורדים בדירוג כי הסוכר בהן קרוב למחצית המוצר ומעלה.",
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
