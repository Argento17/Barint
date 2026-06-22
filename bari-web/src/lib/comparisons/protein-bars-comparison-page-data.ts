import type { Metadata } from "next";

import rawCorpus from "@/data/comparisons/protein_combined_frontend_v2.json";

import {
  loadComparisonCorpus,
  type ComparisonCorpusMeta,
  type ComparisonCorpusRaw,
} from "@/lib/comparisons/corpus";
import type { ComparisonCategoryPageData } from "@/lib/comparisons/registry/types";
import { enrichRowSurface } from "@/lib/comparisons/row-surface";
import {
  filterProteinBarsProducts,
  PROTEIN_BARS_SHELF_LENS_OPTIONS,
  type ProteinBarsShelfFilterId,
} from "@/lib/comparisons/protein-bars-shelf-filters";
import type { BariProductVM } from "@/lib/view-models";

export type ProteinBarsCorpusMeta = ComparisonCorpusMeta;

const loaded = loadComparisonCorpus(rawCorpus as unknown as ComparisonCorpusRaw);
const proteinBarsCorpusMeta = loaded.meta;
// Protein-bar shelf has real per-100g protein data (23–36g) — wire enrichRowSurface
// so the PROTEIN_BAR_PROTEIN_METRIC + PROTEIN_BAR_SUGAR_METRIC columns populate from
// expansion.nutrition. enrichRowSurface populates metrics.protein_g from nutrition.protein;
// sugar_g is mapped in the comparison-page via the VM's metrics.sugar_g field.
const proteinBarsProductsRaw = enrichRowSurface(loaded.products as BariProductVM[]);
// Also surface sugar_g in the metrics object so the sugar metric column renders.
// Explicitly carry protein_g (already set by enrichRowSurface) alongside sugar_g to
// satisfy the BariProductMetricsVM type (protein_g: number | null, not undefined).
const proteinBarsProducts = proteinBarsProductsRaw.map((p) => ({
  ...p,
  // TASK-365 (owner re-critique): the comparison row renders product.name. The corpus
  // carries the brand-less name_he in `name` and the brand-prefixed title in
  // `displayTitle` (canonical brand, de-duplicated). Surface displayTitle as the row
  // title so the brand is visible (owner: brand-in-title is mandatory). Scoped to this
  // page — does not touch other categories' row binding.
  name: (p as { displayTitle?: string }).displayTitle?.trim() || p.name,
  metrics: {
    protein_g: p.expansion.nutrition?.protein ?? null,
    sugar_g: p.expansion.nutrition?.sugar ?? null,
  },
}));

export { proteinBarsCorpusMeta, proteinBarsProducts };

const proteinBarsMetadataUpdated = (() => {
  const date = new Date(proteinBarsCorpusMeta.generated);
  return Number.isNaN(date.getTime())
    ? ""
    : date.toLocaleDateString("he-IL", { month: "long", year: "numeric" });
})();

export const proteinBarsMetadataLine = proteinBarsMetadataUpdated
  ? `${proteinBarsProducts.length} מוצרי חלבון בדף · חטיפי חלבון ועוגיות חלבון · עודכן ב${proteinBarsMetadataUpdated}`
  : `${proteinBarsProducts.length} מוצרי חלבון בדף · חטיפי חלבון ועוגיות חלבון`;

export const proteinBarsHero = {
  eyebrow: "חטיפי חלבון ועוגיות חלבון",
  title: "חטיפי חלבון: הרבה חלבון — אבל איך הוציאו את הסוכר, ובאיזה מחיר הנדסי?",
} as const;

export const proteinBarsPrologueSentences = [
  "אתם עומדים מול מקרר הקופה אחרי אימון, והאריזה מבטיחה דבר אחד גדול: 25 עד 36 גרם חלבון בחטיף אחד. זה הרבה, וזה כתוב נכון על האריזה.",
  "אבל חטיף חלבון הוא לפני הכל מוצר מהונדס סביב מספר. השאלה המעניינת היא לא 'כמה חלבון' אלא איך הוציאו את הסוכר — וכאן מסתתר ההבדל האמיתי בין מוצר למוצר.",
  "ב-24 מתוך 33 המוצרים בדף הזה הסוכר לא הופחת אלא הוחלף במלטיטול, תחליף-סוכר שמרכך את המספר על האריזה בלי להעלים את ההשפעה. הבודדים שמוציאים את הסוכר עם אגוזים, תמרים ושיבולת שועל — הם שמטפסים לראש.",
] as const;

export const proteinBarsCategoryNote = [
  "הערת קטגוריה — 'הכי טוב' כאן הוא B, לא A\n\nבמדף הזה אף מוצר אינו מגיע ל-A. הציון הגבוה בקטגוריה הוא 70/B. חטיף חלבון הוא מוצר מהונדס סביב ריכוז חלבון גבוה, ו'הטוב במדף' כאן אומר 'המהונדס פחות' — לא 'מוצר חזק תזונתית'.",
  "הערת קטגוריה — חטיפי חלבון ועוגיות חלבון נמדדים יחד\n\nהעמוד הזה משווה 33 מוצרים שבנויים סביב חלבון מרוכז: גם חטיפים וגם עוגיות חלבון. חטיפי דגנים, תמרים ושיבולת שועל — מוצרים שאינם בנויים סביב חלבון מבודד — נמדדים בקטגוריה משלהם ומוצגים בעמוד נפרד.",
  "הערת קטגוריה — ההשוואה היא בתוך הקטגוריה בלבד\n\nכל מוצר נמדד מול שאר מוצרי החלבון בדף. ציון B כאן אומר 'הטוב יחסית במדף חטיפי החלבון' — לא שהמוצר שקול לארוחה או לבסיס מזון מלא.",
  "הערת קטגוריה — למה כתריסר חטיפים יושבים בדיוק באותו מקום\n\nתבחינו שגוש שלם של חטיפים באמצע הדף נוחת על אותו ציון. זו לא טעות וזו לא פשרה — אלה פשוט אותו חטיף שוב ושוב: אותה החלפת סוכר במלטיטול, אותו חלבון מולחם מבידודים, אותה הנדסה. כשהמתכון זהה, גם התוצאה זהה. ההבדל היחיד שנשאר בין אחד לשני הוא השם על העטיפה.",
].join("\n\n");

export const proteinBarsMethodologyLines = [
  "ניתחנו 33 חטיפי חלבון ועוגיות חלבון ממדף שופרסל — שמות, רכיבים וערכי תזונה ל-100 גרם ישירות מדף המוצר.",
  "כל ערך תזונה עבר בדיקת סבירות ל-100 גרם; פאנלים לא־סבירים הוצאו מהדירוג. כל הערכים מוצגים ל-100 גרם כדי שמוצרים בגדלים שונים יהיו ברי-השוואה.",
  "הציון נשען על איך הוצא הסוכר ועל עומק ההנדסה — מקור החלבון (מזון שלם מול חלבון מבודד), תחליפי סוכר, ורשימת הרכיבים — לא על כמות החלבון בלבד.",
  "ציוני Bari מתעדים מבנה מוצר ואינם המלצה תזונתית.",
] as const;

export const proteinBarsComparisonMetadata: Metadata = {
  title: "השוואת חטיפי חלבון ועוגיות חלבון | Bari",
  description:
    "השוואת 33 חטיפי חלבון ועוגיות חלבון מהמדף הישראלי — ציון Bari, מקור החלבון, תחליפי הסוכר ורמת העיבוד. מידע, לא המלצה.",
};

const proteinBarsShelfFilters = {
  lensOptions: PROTEIN_BARS_SHELF_LENS_OPTIONS,
  filterProducts: (products: BariProductVM[], activeFilters: string[]) =>
    filterProteinBarsProducts(
      products,
      activeFilters.filter((f): f is ProteinBarsShelfFilterId =>
        PROTEIN_BARS_SHELF_LENS_OPTIONS.some((o) => o.id === f)
      )
    ),
};

export function getProteinBarsPageData(): ComparisonCategoryPageData {
  return {
    products: proteinBarsProducts,
    metadataLine: proteinBarsMetadataLine,
    hero: proteinBarsHero,
    prologueSentences: proteinBarsPrologueSentences,
    methodologyLines: proteinBarsMethodologyLines,
    corpusMeta: proteinBarsCorpusMeta,
    shelfFilters: proteinBarsShelfFilters,
  };
}

export function getProteinBarsCorpusPayload(): {
  _meta: ProteinBarsCorpusMeta;
  products: BariProductVM[];
} {
  return { _meta: proteinBarsCorpusMeta, products: proteinBarsProducts };
}
