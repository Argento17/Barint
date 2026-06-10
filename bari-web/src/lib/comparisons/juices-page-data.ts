import type { Metadata } from "next";

import rawCorpus from "@/data/comparisons/juices_frontend_v3.json";

import type { ComparisonCorpusMeta } from "@/lib/comparisons/corpus";
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
  return {
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
  };
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
  title: 'בין "100% מיץ", "נקטר", ו"משקה פירות" — המדף נראה דומה, אבל מה שבפנים שונה מאוד.',
} as const;

export const juicesPrologueSentences = [
  'כוס מיץ תפוזים "100%" מכילה כ-8 גרם סוכר ל-100 מ"ל — בלי סיבים, בלי תחושת שובע. נקטר יכול להכיל סוכר מוסף על גבי הסוכר שבפרי. "משקה פירות" יכול להכיל 5%–10% פרי בלבד: השאר מים, סוכר לבן ורכז. שלוש אריזות דומות על אותו מדף, שלוש רמות שונות מאוד של פרי בפועל. ההפרש לא כתוב בגדול על האריזה.',
] as const;

// Category caveat — visible without scroll on mobile (spec requirement).
export const juicesCategoryNote =
  'גם מיץ 100% פרי מספק סוכר נוזלי ללא סיבים. זה לא אשמה — זה אופי הקטגוריה. מה שמדורג כאן הוא המרחק מהפרי עצמו: כמה פרי בפועל, האם נוסף סוכר, ומה עוד בתוך הבקבוק.\n\nהתווית "נקטר" פירושה שבין 25% ל-99% מהתוכן הוא פרי — השאר מים ולרוב גם סוכר לבן מוסף. "משקה פירות" יכול להכיל פחות מ-25% פרי. בחלק מהמוצרים שבמדף יש פחות מ-10% פרי: רוב הבקבוק הוא מים, סוכר ורכז. שלושת המינוחים יושבים לפעמים על אותה מדף, באותו גודל אריזה.';

export const juicesMethodologyLines = [
  "בדקנו 65 מיצים ומשקאות פירות משלוש רשתות (שופרסל, קרפור ויוחננוף) — ריכוז פרי, ערכי תזונה ורמת עיבוד.",
  "הציונים יחסיים לקטגוריית מיצים ומשקאות פירות בלבד; ערכי תזונה מחושבים ל-100 מ\"ל — הקטגוריה היחידה בבארי שנמדדת בנפח.",
  "מוצרים עם נתוני רכיבים חלקיים מסומנים בהתאם — הציון מבוסס על מה שזמין על האריזה.",
  "מסד הנתונים עודכן ביוני 2026 — ייתכן שינויים בנוסחאות שאינם משתקפים עדיין בציון.",
] as const;

export const juicesComparisonMetadata: Metadata = {
  title: "השוואת מיצים ומשקאות פירות | Bari",
  description:
    "השוואת 65 מיצים ומשקאות פירות מהמדף הישראלי — ציון Bari, סוכר ל-100 מ\"ל, ריכוז פרי ורמת עיבוד. מידע, לא המלצה.",
};

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
