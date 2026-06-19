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
  title: "קונים מיץ בסופרמרקט? הנה מה שאתם צריכים לדעת על מה שבבקבוק.",
} as const;

export const juicesPrologueSentences = [
  "מדף המיצים בסופרמרקט: שורות של בקבוקים צבעוניים, תמונות פרי על כל אריזה, ושלושה מילים שמסכמות את המדף — \"מיץ\", \"נקטר\", \"משקה פירות\".",
  "אז זהו — שלא תמיד הסיפור שעל האריזה מתאים לסיפור שברשימת הרכיבים.",
  'כולם נראים דומה: בקבוק, צבע, שם פרי. אבל ה\"100% מיץ\" הוא רכיב אחד — הפרי. ה\"נקטר\" הוא בין 25% ל-99% פרי, מים, ולרוב גם סוכר לבן מוסף. ה\"משקה פירות\" יכול להכיל פחות מ-10% פרי: השאר הוא מים, סוכר ורכז.',
  "בארי לא שאלה אם \"מותר\" לשתות מיץ. בארי שאלה: כמה פרי יש בבקבוק, ומה עוד יש שם?",
] as const;

// Category caveat — visible without scroll on mobile (spec requirement).
export const juicesCategoryNote =
  'הערת קטגוריה — גם מיץ 100% הוא סוכר נוזלי\n\nגם מיץ פרי סחוט 100% מספק סוכר — כ-8–13 גרם ל-100 מ"ל — ללא הסיבים שיש בפרי שלם. זה לא פגם ביצרן, זה אופי הנוזל: הסיבים נשארים בתפוז, לא עוברים לכוס. ציון Bari מבוסס על המרחק מהפרי עצמו — כמה פרי בפועל, האם נוסף סוכר, מה רמת העיבוד.\n\nהתווית "נקטר" פירושה 25%–99% פרי — השאר מים ולרוב סוכר לבן מוסף. "משקה פירות" יכול להכיל פחות מ-25% פרי בכלל. בחלק מהמוצרים שבסקירה יש פחות מ-10% פרי: מה שנראה ושומר על טעם הפרי הוא חומרי טעם וריח ורכז, לא הפרי עצמו. שלושת המינוחים יכולים לשבת על אותו מדף, באריזות בגודל זהה.';

export const juicesMethodologyLines = [
  "בדקנו מיצים ומשקאות פירות מיוחננוף — ריכוז פרי בפועל, ערכי תזונה ורמת עיבוד, לא רק סוכר.",
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
