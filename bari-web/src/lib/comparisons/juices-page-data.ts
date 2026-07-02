import type { Metadata } from "next";

import { withComparisonOpenGraph } from "@/lib/seo/open-graph";

import rawCorpus from "@/data/comparisons/juices_frontend_v3.json";

import type { ComparisonCorpusMeta } from "@/lib/comparisons/corpus";
import { normalizeProductBrandDisplay } from "@/lib/comparisons/product-brand-display";
import type { ComparisonCategoryPageData } from "@/lib/comparisons/registry/types";
import {
  filterJuicesProducts,
  JUICES_SHELF_LENS_OPTIONS,
  type JuicesShelfFilterId,
} from "@/lib/comparisons/juices-shelf-filters";
import type { BariProductVM } from "@/lib/view-models";

// The juices JSON uses a flat top-level schema (no _meta wrapper).
// We normalise it here before it touches the UI layer.
// Cast via unknown because the raw JSON products omit optional VM fields (expansion,
// metrics) that are populated below in the map call.
const juicesRaw = rawCorpus as unknown as {
  generatedAt: string;
  totalProducts: number;
  products: Array<
    Record<string, unknown> & {
      id: string;
      name: string;
      brand: string | null;
      score: number;
      grade: string;
      retailers?: string[];
      imageUrl?: string | null;
      insightLine?: string | null;
      limitingFactors?: string[];
      subPool?: string;
      confidence?: string;
      sugarPer100ml?: number | null;
      kcalPer100ml?: number | null;
      fruitContentPct?: number | null;
      volumeMl?: number | null;
      novaGroup?: number | null;
    }
  >;
};

export const juicesCorpusMeta: ComparisonCorpusMeta = {
  generated: juicesRaw.generatedAt,
  category: "juices",
  product_count: juicesRaw.totalProducts,
};

// Map sugar_g metric from sugarPer100ml for the metric column display.
// The metric is explicitly per-100ml (the juice corpus measures by volume).
// The raw JSON products don't carry an expansion block — we provide a minimal one so the
// expansion section component doesn't crash on undefined.confidenceLabel.
export const juicesProducts: BariProductVM[] = juicesRaw.products.map((p) => {
  const base = p as unknown as BariProductVM;
  return normalizeProductBrandDisplay({
    ...base,
    expansion: base.expansion ?? {
      nutrition: null,
      ingredients: null,
      confidenceLabel:
        p.confidence === "high"
          ? "ביטחון גבוה"
          : p.confidence === "low"
            ? "ביטחון נמוך"
            : "ביטחון בינוני",
      servingNote: 'ל-100 מ"ל',
    },
    metrics: {
      protein_g: null,
      sugar_g: p.sugarPer100ml ?? null,
    },
  });
});

function formatJuicesMetadataLine(): string {
  const date = new Date(juicesRaw.generatedAt);
  const monthYear = Number.isNaN(date.getTime())
    ? ""
    : date.toLocaleDateString("he-IL", { month: "long", year: "numeric" });
  const updated = monthYear ? `עודכן ב${monthYear}` : "עודכן לאחרונה";
  return `${juicesProducts.length} מוצרים • ${updated}`;
}

export const juicesMetadataLine = formatJuicesMetadataLine();

export const juicesHero = {
  eyebrow: "מיצים ומשקאות פירות",
  title: "קונים מיץ בסופרמרקט? הנה מה שאתם צריכים לדעת על מה שבבקבוק.",
} as const;

export const juicesPrologueSentences = [
  "המדף נראה אחיד: פרי על האריזה, צבעים טבעיים, שמות מרגיעים. בפועל, \"מיץ\", \"נקטר\" ו\"משקה פירות\" הם שלוש רמות שונות לגמרי של פרי, מים ותוספות.",
  "\"100% מיץ\" פירושו פרי בלבד — לא מים, לא סוכר, לא רכז. \"נקטר\" פירושו בין 25% ל-99% פרי, עם מים ולרוב גם סוכר לבן מוסף. \"משקה פירות\" יכול להכיל פחות מ-10% פרי — השאר מים, סוכר, רכז וחומרי טעם.",
  "גם מיץ 100% סחוט הוא לא ניטרלי: הוא מספק את כל הסוכר שהיה בפרי, בלי הסיבים שהיו מאיטים את ספיגתו. זה לא פגם — זו פשוט הגדרת הנוזל. הציון מבוסס על כמה פרי יש בפועל, האם נוסף סוכר, ורמת העיבוד.",
  "בארי שאלה: כמה פרי יש בבקבוק, ומה עוד יש שם?",
] as const;

// Category caveat — visible without scroll on mobile (spec requirement).
export const juicesCategoryNote =
  'הערת קטגוריה — גם מיץ 100% הוא סוכר נוזלי\n\nמיץ פרי סחוט 100% מכיל את כל הסוכר שהיה בפרי — ללא הסיבים שמאיטים את ספיגתו בפרי שלם. הסיבים נשארים בתפוז, לא עוברים לכוס. זה אופי הנוזל, לא פגם ביצרן. ציון Bari מבוסס על שלושה דברים: כמה פרי אמיתי בפועל, האם נוסף סוכר, ורמת העיבוד.\n\nטווח הפרי על המדף הזה: מ-100% פרי שלם ועד פחות מ-10% פרי עם חומרי טעם ורכז. שלושת המינוחים — "מיץ", "נקטר", "משקה פירות" — יכולים לשבת על אותו מדף, באריזות בגודל זהה.';

export const juicesMethodologyLines = [
  "בדקנו מיצים ומשקאות פירות מיוחננוף — ריכוז פרי בפועל, ערכי תזונה ורמת עיבוד, לא רק סוכר.",
  "הציונים יחסיים לקטגוריית מיצים ומשקאות פירות בלבד; ערכי תזונה מחושבים ל-100 מ\"ל — הקטגוריה היחידה בבארי שנמדדת בנפח.",
  "מוצרים עם נתוני רכיבים חלקיים מסומנים בהתאם — הציון מבוסס על מה שזמין על האריזה.",
  "מסד הנתונים עודכן ביוני 2026 — ייתכן שינויים בנוסחאות שאינם משתקפים עדיין בציון.",
] as const;

export const juicesComparisonMetadata: Metadata = withComparisonOpenGraph({
  title: "השוואת מיצים ומשקאות פירות | Bari",
  description:
    "השוואת 17 מיצים ומשקאות פירות מהמדף הישראלי — ציון Bari, סוכר ל-100 מ\"ל, ריכוז פרי ורמת עיבוד. מידע, לא המלצה.",
});

function isJuicesShelfFilterId(filter: string): filter is JuicesShelfFilterId {
  return JUICES_SHELF_LENS_OPTIONS.some((option) => option.id === filter);
}

const juicesShelfFilters = {
  lensOptions: JUICES_SHELF_LENS_OPTIONS,
  filterProducts: (products: BariProductVM[], activeFilters: string[]) =>
    filterJuicesProducts(products, activeFilters.filter(isJuicesShelfFilterId)),
};

export function getJuicesPageData(): ComparisonCategoryPageData {
  return {
    products: juicesProducts,
    metadataLine: juicesMetadataLine,
    hero: juicesHero,
    prologueSentences: juicesPrologueSentences,
    methodologyLines: juicesMethodologyLines,
    corpusMeta: juicesCorpusMeta,
    shelfFilters: juicesShelfFilters,
  };
}

export function getJuicesCorpusPayload(): {
  _meta: ComparisonCorpusMeta;
  products: BariProductVM[];
} {
  return {
    _meta: juicesCorpusMeta,
    products: juicesProducts,
  };
}
