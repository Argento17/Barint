import snackEditorialData from "@/data/blog/snack-editorial.json";
import type { ComparisonMomentProps } from "@/components/snack/comparison-moment";
import { snackProducts } from "@/lib/comparisons/snack-page-data";

function product(id: string) {
  const item = snackProducts.find((entry) => entry.id === id);
  if (!item) {
    throw new Error(`Missing snack product: ${id}`);
  }
  return item;
}

export const snackWellnessHero = snackEditorialData.snackWellnessHero;

export const snackShelfIntro = snackEditorialData.snackShelfIntro;

export const snackWellnessFindings = snackEditorialData.snackWellnessFindings;

export const snackBlogMap = {
  title: "פשטות הרכיבים מול מיצוב — 53 חטיפים",
  caption: "ציר אופקי: עומק עיבוד · ציר אנכי: ארכיטקטורת סוכר · שלוש נקודות מסומנות לעוגן החקירה.",
  annotatedIds: ["snk-001", "snk-013", "snk-009"] as const,
  annotations: {
    "snk-001": "70/B — 4 רכיבים",
    "snk-013": "13/E",
    "snk-009": "חטיפי פרוטאין — 45–47/D",
  },
} as const;

export const snackWellnessComparisons: ComparisonMomentProps[] = [
  {
    title: "בר פרוטאין מול חטיף תמרים — 23 נקודות",
    driverSentence:
      "4 רכיבים, NOVA2: 70/B. 15+ רכיבים, NOVA4: 47/D. הפרש הציון לא בא מהפרוטאין.",
    products: [product("snk-001"), product("snk-009")],
    detailLines: [
      "חטיף תמרים: תמרים ראשון, ללא סוכר מוסף, 0–2 תוספות.",
      "נייצ'ר וואלי פרוטאין: בסיס מהונדס, 3+ מקורות ממתיקים, 5+ תוספות.",
    ],
  },
  {
    title: "שלושה חטיפי שוקולד מריר — שלושה ציונים",
    spanLabel: "טווח של 41 נקודות בין שלושת המוצרים",
    driverSentence:
      "שלושה חטיפים בציפוי שוקולד מריר. בסיס שונה — NOVA שונה — 41 נקודות הפרש.",
    products: [product("snk-002"), product("snk-004"), product("snk-006")],
    detailLines: [
      "תמרים-קקאו: בסיס שלם, NOVA2.",
      "סלים דליס: בסיס מעובד, NOVA3.",
      "פיטנס גרנולה: בסיס מהונדס, NOVA4.",
    ],
  },
  {
    title: "תמרים — אבל לא אותו דבר",
    driverSentence:
      "שניהם 'תמרים'. אחד: תמרים ראשון ברשימה, NOVA2. אחד: NOVA4, סוכרים מוספים.",
    products: [product("snk-001"), product("snk-011")],
    detailLines: [
      "חטיף תמרים במילוי חמאת שקדים: 4 רכיבים.",
      "פרי מארז תמרים ואגוזי לוז: ריבוי ממתיקים ועומק עיבוד גבוה.",
    ],
  },
];

export const snackWellnessSynthesis = snackEditorialData.snackWellnessSynthesis;

export const snackBlogCta = snackEditorialData.snackBlogCta;

export const snackEnginePresets: Array<{
  label: string;
  moment: ComparisonMomentProps;
}> = [
  {
    label: "שיבולת שועל משני קצות המדף",
    moment: {
      title: "אותה שיבולת שועל — 36 נקודות הפרש",
      driverSentence:
        "שניהם שיבולת שועל. אחד בסיס שיבולת שועל שלמה — אחד בסיס קמח וסירופ גלוקוז עם 14 רכיבים.",
      products: [product("snk-003"), product("snk-006")],
      spanLabel: "36 נקודות הפרש",
    },
  },
  {
    label: "בר פרוטאין מול חטיף תמרים",
    moment: snackWellnessComparisons[0],
  },
  {
    label: "שלושה חטיפי שוקולד מריר",
    moment: snackWellnessComparisons[1],
  },
];
