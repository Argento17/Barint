import type { Metadata } from "next";

import rawCorpus from "@/data/comparisons/hard_cheeses_frontend_v3.json";

import {
  formatComparisonMetadataLine,
  loadComparisonCorpus,
  type ComparisonCorpusMeta,
  type ComparisonCorpusRaw,
} from "@/lib/comparisons/corpus";
import type { ComparisonCategoryPageData } from "@/lib/comparisons/registry/types";
import {
  filterHardCheesesProducts,
  HARD_CHEESES_SHELF_LENS_OPTIONS,
  type HardCheesesShelfFilterId,
} from "@/lib/comparisons/hard-cheeses-shelf-filters";
import type { BariProductVM } from "@/lib/view-models";

export type HardCheesesCorpusMeta = ComparisonCorpusMeta;

function isHardCheesesShelfFilterId(
  filter: string
): filter is HardCheesesShelfFilterId {
  return HARD_CHEESES_SHELF_LENS_OPTIONS.some((option) => option.id === filter);
}

const { meta: hardCheesesCorpusMeta, products: _hardCheesesProductsRaw } =
  loadComparisonCorpus(rawCorpus as unknown as ComparisonCorpusRaw);

// Protein per 100g is the headline differentiator — hard cheeses carry 20–28g/100g.
const hardCheesesProducts: BariProductVM[] = _hardCheesesProductsRaw.map(
  (p) => ({
    ...p,
    metrics: {
      protein_g: p.expansion?.nutrition?.protein ?? null,
    },
  })
);

export { hardCheesesCorpusMeta, hardCheesesProducts };

export const hardCheesesMetadataLine = formatComparisonMetadataLine(
  hardCheesesProducts.length,
  hardCheesesCorpusMeta.generated
);

export const hardCheesesHero = {
  eyebrow: "גבינות קשות וצהובות",
  title: "קונים גבינה צהובה בסופרמרקט? הנה מה שאתם צריכים לדעת.",
} as const;

export const hardCheesesPrologueSentences = [
  "עומדים מול מקרר הגבינות — שורה של פרוסות צהובות, גוש עמק, שקית מגורדת — וצריך לבחור מהר כי יש תור מאחור.",
  "גבינה צהובה קשה היא, בגדול, מזון עם בסיס אמיתי: חלבון, רשימה קצרה, מעט עיבוד. הערכים במדף הזה לרוב טובים.",
  "יחד עם זאת, אותה גבינה נושאת שומן רווי ונתרן אמיתיים, ולכן רוב הגבינות כאן נוחתות סביב C — ציון של מזון אמיתי שכדאי לאכול בכמות מדודה, ולא של מוצר חלש.",
  "בין המותגים יש בכל זאת פערים: חלבון של 33 גרם מול 23, נתרן שמכפיל את עצמו בין גבינה לגבינה, וגרסה אחת שבה רוב החלב הוחלף בעמילן.",
  "בדקנו 24 גבינות קשות מהמדף כדי שתדעו מה באמת נכנס לכריך מאחורי הפרוסות.",
] as const;

export const hardCheesesCategoryNote =
  "הערת קטגוריה — למה רוב הגבינות נוחתות על C?\n\nרוב הגבינות הקשות במדף הזה מקבלות ציון C, וזה ציון הוגן ולא עונש. גבינה צהובה מלאה היא מזון אמיתי עם רשימת רכיבים קצרה, אבל היא נושאת שומן רווי ונתרן ממשיים — ושניהם נספרים. ה-C כאן מתאר בדיוק את זה: מזון אמיתי וטוב כבסיס, שכדאי לאכול בכמות מדודה. הגבינות שמטפסות גבוה יותר הן הרזות (5% או 9% שומן), והגבינות שצונחות ל-D הן המעובדות באמת — מוצר מותך או גבינה עם שני סימוני אזהרה במקביל.\n\nהערת קטגוריה — שומן רווי בגבינה הוא לא כמו בחמאה\n\nהשומן הרווי בגבינה הוא אמיתי, מעלה את הכולסטרול הרע (LDL) ונספר בציון. יש עדויות ראשוניות, ברמת ודאות בינונית, שכשמשווים כמות זהה של שומן רווי מגבינה לעומת חמאה, הגבינה מעלה את ה-LDL פחות מהחמאה — ככל הנראה בזכות מבנה הגבינה (סידן וחלבון). שימו לב: פחות מחמאה, לא במקום חמאה — הגבינה עדיין מעלה את ה-LDL, פשוט בעוצמה מתונה יותר, ולכן עדיין כדאי לאכול אותה בכמות מדודה. לכן הציון לא קונס גבינה נקייה באותה חומרה שבה הוא קונס שומן מהונדס, אבל השומן בגבינה משמעותי ונספר — הוא פשוט יושב במקום אחר על הסקאלה.\n\nהערת קטגוריה — 'לייט' הוא לא בהכרח נקי יותר\n\nגבינה 9% שומן היא לא בהכרח נקייה יותר מגבינה 28%. בסקירה זו חלק מהגרסאות הרזות מגיעות דווקא עם יותר נתרן, וזה מקזז חלק מהיתרון של השומן הנמוך. הציון משקלל את כלל הרכיבים, ולא רק את אחוז השומן שעל האריזה.\n\nהערת קטגוריה — סוכר וסיבים\n\nערכי הסוכר והסיבים לא צוינו בלוחות התזונה של רוב הגבינות בסקירה זו. אין פירוש הדבר שהם אפס, אלא שהיצרן לא נדרש לציין אותם כשהם נמוכים מאוד, ובחר שלא. הציון מבוסס על הנתונים שכן היו זמינים.";

export const hardCheesesMethodologyLines = [
  "בדקנו 24 גבינות קשות וצהובות מהמדף — רכיבים, ערכי תזונה ורמת עיבוד, מעבר לאחוז השומן בלבד.",
  "הציונים יחסיים לקטגוריית גבינות קשות בלבד; אחוז השומן על האריזה הוא שומן בחומר רטוב, והחישוב משתמש בשומן בפועל (גרם ל-100 גרם).",
  "שומן רווי משוקלל כגורם אמיתי, אך גבינה נקייה אינה מקבלת את אותו קנס כמו שומן מהונדס — בהתאם לעדות שמבנה הגבינה ממתן את ההשפעה על הכולסטרול.",
  "מוצרים עם נתוני תזונה חלקיים מסומנים בהתאם, והציון מבוסס על הנתונים שהיו זמינים.",
  "מסד הנתונים עודכן ביוני 2026 — ייתכנו שינויים בנוסחאות שטרם משתקפים בציון.",
] as const;

export const hardCheesesComparisonMetadata: Metadata = {
  title: "השוואת גבינות קשות וצהובות | Bari",
  description:
    "השוואת 24 גבינות קשות מהמדף הישראלי — ציון Bari, חלבון, שומן ונתרן ל-100 גרם. מידע, לא המלצה.",
};

const hardCheesesShelfFilters = {
  lensOptions: HARD_CHEESES_SHELF_LENS_OPTIONS,
  filterProducts: (products: BariProductVM[], activeFilters: string[]) =>
    filterHardCheesesProducts(
      products,
      activeFilters.filter(isHardCheesesShelfFilterId)
    ),
};

export function getHardCheesesPageData(): ComparisonCategoryPageData {
  return {
    products: hardCheesesProducts,
    metadataLine: hardCheesesMetadataLine,
    hero: hardCheesesHero,
    prologueSentences: hardCheesesPrologueSentences,
    methodologyLines: hardCheesesMethodologyLines,
    corpusMeta: hardCheesesCorpusMeta,
    shelfFilters: hardCheesesShelfFilters,
  };
}

export function getHardCheesesCorpusPayload(): {
  _meta: HardCheesesCorpusMeta;
  products: BariProductVM[];
} {
  return {
    _meta: hardCheesesCorpusMeta,
    products: hardCheesesProducts,
  };
}
