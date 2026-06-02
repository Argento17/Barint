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

/**
 * Shorten a pre-authored signal line to a row-sized reason (§3.3). Deterministic:
 * take the clause before the first em-dash / colon, trimmed. The full string stays
 * in the expansion; this is display-only and never alters corpus content.
 */
function shortenReason(line: string | undefined): string | null {
  if (!line) return null;
  const head = line.split(/\s+[—–-]\s+|:\s+/)[0]?.trim();
  return head && head.length > 0 ? head : line.trim();
}

/**
 * Row surface enrichment (comparison_ui_reference_v2 §2.2). Surfaces the already-present
 * protein value as a first-class metric and derives the row reason from
 * positiveSignals[0] / limitingFactors[0]. Display-only; not a score input.
 */
function enrichMaadanimRowSurface(products: BariProductVM[]): BariProductVM[] {
  return products.map((product) => ({
    ...product,
    metrics: { protein_g: product.expansion.nutrition?.protein ?? null },
    rowReason: {
      positive: shortenReason(product.expansion.positiveSignals?.[0]),
      limiting: shortenReason(product.expansion.limitingFactors?.[0]),
    },
  }));
}

// TASK-137F category-boundary sweep (Product directive 2026-06-01): the maadanim shelf
// is ready-to-eat DAIRY desserts/puddings. These are not — removed from the displayed set:
//  • non-dairy fruit preserves (jam-like): משמש, תפוז
//  • savory vegetable spread: חצילים
//  • non-dairy jellies (water + sugar, 0 g protein): ג'לי פטל, לימבו פטל
//  • instant-pudding POWDERS (not finished products; ingredient text is marketing copy)
// Scores untouched (TASK-136 owns scores); these only leave the comparison view.
const EXCLUDED_MAADANIM_IDS = new Set([
  "bsip1_maadanim_7296073725640", // מעדן חצילים — eggplant/vegetable, not a dessert
  "bsip1_maadanim_5014271300429", // מעדן משמש — apricot fruit preserve, no dairy
  "bsip1_maadanim_5014271360423", // מעדן תפוז — orange fruit preserve, no dairy
  "bsip1_maadanim_4136857",       // מעדן ג'לי פטל — jelly, water+sugar, 0g protein
  "bsip1_maadanim_7290110565435", // לימבו פטל קו חלבי — jelly, water+sugar, no dairy
  "bsip1_maadanim_7290112966827", // פודינג אינסטנט שוקולד — powder
  // 3 pudding-powder records below were scrubbed from maadanim_frontend_v2.json
  // (QA hygiene, 2026-06-02): removed from the corpus entirely, so no exclusion
  // entry is needed: bsip1_maadanim_7290112966803, bsip1_maadanim_68138,
  // bsip1_maadanim_7290018249550 (the last also had score=null).
  "bsip1_maadanim_7290104501661", // פודינג וניל צרפתי — powder
  "bsip1_maadanim_7290018249123", // אינסטנט פודינג בטעם וניל — powder
]);

const { meta: maadanimCorpusMeta, products: loadedMaadanimProducts } =
  loadComparisonCorpus(rawCorpus as ComparisonCorpusRaw);

const maadanimProducts = enrichMaadanimRowSurface(
  loadedMaadanimProducts.filter((p) => !EXCLUDED_MAADANIM_IDS.has(p.id))
);

export { maadanimCorpusMeta, maadanimProducts };

export function formatMaadanimMetadataLine(
  productCount: number,
  generatedIso: string
): string {
  return formatComparisonMetadataLine(productCount, generatedIso);
}

export const maadanimMetadataLine = formatMaadanimMetadataLine(
  maadanimProducts.length,
  maadanimCorpusMeta.generated
);

export const maadanimHero = {
  eyebrow: "מעדנים",
  // TASK-137F: sharper, assumption-challenging title (was the generic "מה שווה לקחת מהמדף").
  title: "מעדנים: פינוק או חלבון?",
} as const;

// TASK-137F: prologue rewritten to the hummus reference — what we measured, how, and
// why protein is the headline metric (rationale: 02_products/maadanim/maadanim_metric_137F.md).
export const maadanimPrologueSentences = [
  "בדקנו עשרות מעדנים וקינוחי חלב מהמדף הישראלי לפי מה שבאמת בגביע — רשימת הרכיבים, רמת העיבוד, נטל המייצבים והתוספים והרכב הערכים התזונתיים.",
  "כל מוצר מקבל ציון על סולם 0–100 ביחס לקטגוריית המעדנים בלבד: מעדן נמדד מול מעדן, לא מול מזון אחר.",
  "בחזית כל מוצר בחרנו להציג את החלבון, כי הוא מפריד בין שני דברים שנמכרים תחת אותו שם — קינוח לפינוק לעומת חטיף חלבון פונקציונלי. במדף הזה החלבון נע מ-0 גרם (פודינג וג'לי שאינם מבוססי חלב) ועד כ-10 גרם (מעדנים מועשרי חלבון).",
  "אבל חלבון גבוה לא הופך מעדן ל'בריא': הציון משקלל גם את נטל המייצבים, התוספים ורמת העיבוד. מעדן מסורתי דל-חלבון אינו 'פחות טוב' — הוא פשוט נועד לשימוש אחר.",
  "ערכי הסוכר אינם זמינים באופן עקבי בקטגוריה זו בשל מגבלות במקור הנתונים; החלבון הוא לכן המספר האמין ביותר שאפשר להעמיד להשוואה.",
] as const;

// Category caveat (cheese gold-standard format), rendered once in the header. Two nuances:
// (1) "diet"/"מעודנת"/"ללא סוכר" framing — grounded in the live data (e.g. דנונה במתיקות
//     מעודנת surfaces a sweetener in its row line); a lighter label is not automatically a
//     higher score, and the engine reads the sweetener from the ingredient list.
// (2) CORRECTED (Nutrition co-sign, 2026-06-02): the cheese sodium/sat-fat limitation does
//     NOT carry over to maadanim. The cheese disclosure reflects a cheese-package reality
//     (factory_run disclosures); the maadanim run (run_maadanim_001, engine 0.4.1) actively
//     scores both — verified in the 167 scored traces: fat_quality dim varies 17→100, 30
//     products take the ISRAELI_RED_LABEL_1_SAT_FAT cap (55), 24 take HIGH_SODIUM_700MG_PLUS
//     (60), 12 take the fat-sodium hyper-palatability penalty. Asserting "not scored" would be
//     false. Replaced with a truthful composition statement (sugar/sat-fat/sodium DO lower the
//     score). EV-027 in scoring.md is the fiber-not-applicable fix, unrelated to sodium/sat-fat.
export const maadanimCategoryNote = [
  "הערת קטגוריה — 'דיאט', 'מעודנת' ו'ללא סוכר' לא תמיד מה שנדמה\n\nמעדן שמסומן 'דיאט' או 'מתיקות מעודנת' מחליף לעיתים סוכר בממתיקים מלאכותיים, ולעיתים מוסיף מייצבים כדי לשמר מרקם. הציון קורא את הרכיבים מהרשימה — לא את הכותרת — כך שמוצר 'קליל' עשוי שלא לקבל ציון גבוה יותר מהגרסה הרגילה.",
  "הערת קטגוריה — סוכר, שומן רווי ונתרן\n\nבקטגוריה זו עומס סוכר, שומן רווי גבוה ונתרן גבוה מורידים את הציון. מעדן שעשיר בהם ידורג נמוך יותר — אך כשהערך אינו מופיע על האריזה, הוא אינו נכנס לחישוב. בדקו את התווית להשלמת התמונה.\n\nהציון מודד את מה שהתווית והנתונים מאפשרים בכל קטגוריה בנפרד; בקטגוריה זו ערכים אלה כן נכנסים לחישוב.\n\nסיבים תזונתיים, לעומת זאת, כמעט אינם מצוינים על תווית של מוצרי חלב, ולכן ערך זה אינו נכנס לניתוח בקטגוריה זו.",
]
  .join("\n\n");

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
