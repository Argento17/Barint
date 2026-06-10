import type { ComparisonMomentProps } from "@/components/snack/comparison-moment";
import { snackProducts } from "@/lib/comparisons/snack-page-data";

function product(id: string) {
  const item = snackProducts.find((entry) => entry.id === id);
  if (!item) {
    throw new Error(`Missing snack product: ${id}`);
  }
  return item;
}

export const snackWellnessHero = {
  headlineLines: ["בר פרוטאין: 47/D.", "חטיף תמרים עם 4 רכיבים: 70/B."],
  subline: "23 נקודות הפרש. אותה קטגוריה.",
  driverSubline: "מה שהפריד ביניהם — לא השם על האריזה.",
  productIds: ["snk-009", "snk-001"] as const,
} as const;

export const snackShelfIntro = `יוחננוף, מדף הקטגוריה. חטיפי פיטנס בצהוב-כחול. Nature Valley קלאסי. קורני ושוגי. חטיפי תמרים בחום. בשורה הבאה — חטיפי פרוטאין, ובצד: "אנרג'י", "סלים", "Free". אנחנו סרקנו 53 מוצרים מהמדף הזה. הציון הגבוה ביותר — 70/B — לא הלך לאף אחד מהשמות שהזכרנו.`;

export const snackWellnessFindings = [
  {
    tag: "ממצא",
    title: "חטיפי הפרוטאין קיבלו D. חטיף תמרים עם 4 רכיבים קיבל B.",
    body: "הפרש: 23 נקודות. הגורם: עומק העיבוד, לא כמות הפרוטאין.",
  },
  {
    tag: "דפוס",
    title: '"תמרים" על האריזה לא אמר את אותו הדבר בשני מוצרים שונים.',
    body: "חטיף תמרים במילוי חמאת שקדים: 70/B. פרי מארז תמרים ואגוזי לוז: 43/D.",
  },
  {
    tag: "פער",
    title: 'עיבוד עמוק הוא תקרת ציון — לא מדד "רע".',
    body: "כשמוצר עובר עיבוד עמוק, הציון המקסימלי שיכול לקבל הוא D. המיצוב על האריזה לא שינה את זה.",
  },
] as const;

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
      "4 רכיבים, עיבוד מינימלי: 70/B. 15+ רכיבים, עיבוד עמוק: 47/D. הפרש הציון לא בא מהפרוטאין.",
    products: [product("snk-001"), product("snk-009")],
    detailLines: [
      "חטיף תמרים: תמרים ראשון, ללא סוכר מוסף, 0–2 תוספות.",
      "נייצ'ר וואלי פרוטאין: בסיס מורכב, 3+ מקורות ממתיקים, 5+ תוספות.",
    ],
  },
  {
    title: "שלושה חטיפי שוקולד מריר — שלושה ציונים",
    spanLabel: "טווח של 41 נקודות בין שלושת המוצרים",
    driverSentence:
      "שלושה חטיפים בציפוי שוקולד מריר. בסיס שונה — עומק עיבוד שונה — 41 נקודות הפרש.",
    products: [product("snk-002"), product("snk-004"), product("snk-006")],
    detailLines: [
      "תמרים-קקאו: בסיס שלם, עיבוד מינימלי.",
      "סלים דליס: בסיס מעובד, עיבוד בינוני.",
      "פיטנס גרנולה: בסיס מורכב, עיבוד עמוק.",
    ],
  },
  {
    title: "תמרים — אבל לא אותו דבר",
    driverSentence:
      "שניהם 'תמרים'. אחד: תמרים ראשון ברשימה, עיבוד מינימלי. אחד: עיבוד עמוק, סוכרים מוספים.",
    products: [product("snk-001"), product("snk-011")],
    detailLines: [
      "חטיף תמרים במילוי חמאת שקדים: 4 רכיבים.",
      "פרי מארז תמרים ואגוזי לוז: מקורות מתיקות מרובים ועומק עיבוד גבוה.",
    ],
  },
];

export const snackWellnessSynthesis = `מה שהפריד את המוצרים בקטגוריה הזו היה מבנה הרכיבים ועומק העיבוד — לא השם. חטיפי פרוטאין, חטיפי פיטנס, ומוצרים עם "תמרים" בשם שעברו עיבוד עמוק — כולם הגיעו לאותה תקרה. הציון הגבוה ביותר — 70/B — לא נשא שום תווית. 4 רכיבים, עיבוד מינימלי.`;

export const snackBlogCta = {
  line: "→ לכל 53 המוצרים, סוננים לפי ציון",
  button: "לטבלת ההשוואה המלאה",
} as const;

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
