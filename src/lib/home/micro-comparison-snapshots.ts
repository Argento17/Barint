import { getProductByBarcode } from "@/lib/blog/milk-analysis-chart-data";
import type { MilkComparisonProduct } from "@/lib/comparisons/milk-types";

export type MicroComparisonSnapshot = {
  id: string;
  category: string;
  title: string;
  href: string;
  leftBarcode: string;
  rightBarcode: string;
  tradeoff: string;
  leftStrengths: [string, string];
  rightStrengths: [string, string];
};

const SNAPSHOTS: MicroComparisonSnapshot[] = [
  {
    id: "soy-enriched",
    category: "תחליפי חלב",
    title: "סויה בסיסית מול סויה מועשרת",
    href: "/blog/milk-analysis#comparisons",
    leftBarcode: "7290110324926",
    rightBarcode: "7290116936116",
    tradeoff:
      "משקה הסויה המועשר מוסיף חלבון — אבל עם מבנה רכיבים מורכב יותר ויותר שכבות ייצוב.",
    leftStrengths: ["רכיבים פשוטים יותר", "פחות שכבות העשרה"],
    rightStrengths: ["יותר חלבון", "יציבות גבוהה יותר"],
  },
  {
    id: "oat-barista",
    category: "שיבולת שועל",
    title: "שיבולת שועל לקפה מול גרסה קלה יותר",
    href: "/blog/milk-analysis#comparisons",
    leftBarcode: "7394376619939",
    rightBarcode: "7394376620904",
    tradeoff:
      "גרסת הבריסטה נבנית להקצפה ולמרקם — לרוב עם יותר רכיבי מרקם מאשר גרסת ללא סוכר.",
    leftStrengths: ["מרקם לקפה", "הקצפה נעימה"],
    rightStrengths: ["פחות סוכר", "רשימה קצרה יותר"],
  },
  {
    id: "dairy-protein",
    category: "חלב פרה",
    title: "חלב מלא מול חלב מועשר בחלבון",
    href: "/hashvaot/milk-comparison",
    leftBarcode: "7290000051352",
    rightBarcode: "7290114313865",
    tradeoff:
      "חלבון מועשר פותר שובע — אבל דורש יותר עיבוד והרכבה מאשר חלב בסיסי עם רשימה קצרה.",
    leftStrengths: ["רכיבים פשוטים", "מבנה ישיר"],
    rightStrengths: ["חלבון גבוה", "ערך פונקציונלי"],
  },
  {
    id: "milk-flagship",
    category: "ניתוח מדף",
    title: "18 מוצרי חלב על אותו מדף",
    href: "/blog/milk-analysis",
    leftBarcode: "7290000051352",
    rightBarcode: "7290116936116",
    tradeoff:
      "הניתוח המלא מראה איך מוצרים שנראים דומים מתפצלים ברכיבים, בעיבוד ובתזונה — לא רק בציון.",
    leftStrengths: ["מבנה פשוט", "רמת עיבוד נמוכה"],
    rightStrengths: ["יותר חלבון", "יעד תזונתי ברור"],
  },
];

export type ResolvedMicroSnapshot = MicroComparisonSnapshot & {
  left: MilkComparisonProduct;
  right: MilkComparisonProduct;
};

export function getMicroComparisonSnapshots(): ResolvedMicroSnapshot[] {
  return SNAPSHOTS.map((snap) => {
    const left = getProductByBarcode(snap.leftBarcode);
    const right = getProductByBarcode(snap.rightBarcode);
    if (!left || !right) return null;
    return { ...snap, left, right };
  }).filter((s): s is ResolvedMicroSnapshot => s != null);
}
