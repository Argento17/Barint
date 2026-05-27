import { milkProducts } from "@/lib/comparisons/milk-page-data";
import type { MilkComparisonProduct } from "@/lib/comparisons/milk-types";

/** Flagship SKUs from handoff — narrative focus */
const FLAGSHIP_BARCODES = [
  "7290000051352",
  "7290116936116",
  "5411188112709",
  "7394376619939",
  "7290110324926",
  "8000215204219",
] as const;

export const milkEditorialHero = {
  eyebrow: "BARI · ניתוח מדף",
  title: "מה באמת קורה במדף החלב?",
  subtitle: "חלב, תחליפי צמח ומשקאות חלבון — מעבר לאריזה, מעבר לשפה השיווקית.",
  meta: `${milkProducts.length} מוצרים · מדף ישראלי · מידע, לא המלצה`,
} as const;

/** Exact editorial intro copy — do not paraphrase */
export const milkEditorialIntroParagraphs = [
  "בשנים האחרונות מדפי הסופר התמלאו בתחליפי חלב, משקאות שיבולת שועל, שקדים, סויה ואורז — רובם ממותגים כמוצרים «טבעיים», «קלים», «מאוזנים» או «מתקדמים יותר». במקביל, חלב רגיל הפך כמעט למוצר «ישן», כזה שנתפס אצל חלק מהצרכנים כפחות עדכני או פחות איכותי. אבל כשמסתכלים מעבר לאריזה, מעבר לשפה השיווקית ומעבר לטבלאות החלבון והקלוריות — מתקבלת תמונה הרבה יותר מורכבת.",
  "בבדיקה הראשונה של בריא בתחום החלב ותחליפי החלב, ניתחנו שישה מוצרים פופולריים בישראל: חלב מלא, משקאות סויה, שקדים, אורז ושיבולת שועל, לצד משקה חלבון מועשר. המטרה לא הייתה לבדוק «מה בריא יותר», אלא להבין משהו עמוק יותר: עד כמה המוצר נשאר קרוב למזון המקורי שלו — וכמה שכבות של פירוק, עיבוד, ייצוב והנדסה נוספו בדרך.",
  "התוצאה המעניינת ביותר הייתה דווקא זו שלא מעט צרכנים אולי לא היו מצפים לה: חלב מלא רגיל קיבל את הציון הגבוה ביותר בהשוואה. לא בגלל שהוא «מושלם», ולא בגלל שבריא מעדיף מוצרים מן החי — אלא משום שמבחינה מבנית והרכבית הוא נשאר פשוט יחסית. רשימת רכיבים קצרה, כמעט ללא תוספים, ללא מערכות ייצוב מורכבות, וללא צורך «לבנות מחדש» את המוצר באמצעים תעשייתיים.",
  "לעומתו, חלק ממשקאות הצומח הציגו פרופיל הרבה יותר מהונדס. במקרים מסוימים, המוצר התחיל מחומר גלם פשוט יחסית — כמו שיבולת שועל או שקדים — אך בדרך הפך למערכת מורכבת של מייצבים, שמנים, סיבים מבודדים, חומרי טעם, תוספי ויטמינים וחומרי איזון מרקם. חלק מהמוצרים אף נזקקו להשלמות תזונתיות כדי «להחזיר» רכיבים שאבדו במהלך העיבוד.",
  "זה לא אומר שמשקה צמחי הוא «רע», וגם לא אומר שחלב הוא «טוב». בריא לא עובד בשחור ולבן. האלגוריתם לא מתגמל אידיאולוגיה, טרנד או קטגוריה — אלא בוחן את המבנה בפועל של המזון. שני מוצרים יכולים להציג כמעט אותו מספר חלבון על האריזה, אבל להגיע אליו בדרכים שונות לחלוטין: אחד דרך מזון יחסית שלם, והשני דרך הרכבה מחדש של רכיבים מבודדים.",
  "אחד הדברים הבולטים ביותר בניתוח היה מושג שבריא מכנה «שלמות מבנית» — עד כמה המזון נשאר קרוב למטריצה המקורית שלו. זהו מימד שכמעט לא קיים כיום בשיח התזונתי הרגיל. רוב הצרכנים רגילים להסתכל על סוכר, חלבון או קלוריות, אבל כמעט אף אחד לא מדבר על עומק הפירוק התעשייתי שהמזון עבר לפני שהגיע למדף.",
  "וכאן בדיוק מתחיל הפער בין תדמית לבין הרכב אמיתי. חלק מהמוצרים בהשוואה נראו «נקיים» מאוד מקדימה, אבל מאחור הסתתרו מערכות ייצוב מורכבות. אחרים דווקא נראו פשוטים או אפילו «מיושנים», אבל הציגו מבנה תזונתי יציב וקוהרנטי יחסית.",
  "גם בתוך עולם תחליפי החלב עצמו נראו הבדלים משמעותיים. לא כל משקה צמחי זהה לאחר. חלק מהמשקאות הצליחו לשמור על רשימת רכיבים יחסית מאוזנת ופשוטה, בעוד אחרים נשענו הרבה יותר על הנדסת מרקם, ממתיקים, מייצבים ותוספי פונקציונליות. במילים אחרות: עצם העובדה שמוצר מבוסס צומח לא אומרת הרבה בפני עצמה.",
  "בריא מנסה לחשוף בדיוק את האזור הזה — האזור שבין טבלת הערכים לבין המציאות התעשייתית של המזון. לא כדי להגיד לצרכנים מה לקנות, אלא כדי להפוך את המזון עצמו לקריא יותר.",
  "כי בסופו של דבר, השאלה היא כבר לא רק כמה חלבון יש במוצר. השאלה היא מה היה צריך לקרות בדרך כדי שהוא ייראה, ירגיש ויתנהג כמו שהוא נראה היום.",
] as const;

export const processingTimelineSteps = [
  { id: "source", label: "מזון מקורי" },
  { id: "separation", label: "הפרדה" },
  { id: "isolation", label: "בידוד רכיבים" },
  { id: "rebuild", label: "בנייה מחדש" },
  { id: "stabilize", label: "ייצוב" },
  { id: "flavor", label: "תיקון טעם" },
  { id: "fortify", label: "העשרה" },
] as const;

export const ingredientStructureExamples = {
  dairy: {
    label: "חלב פרה — מבנה פשוט",
    layers: ["חלב"],
  },
  plant: {
    label: "משקה צמחי — הרכבה שכבתית",
    layers: [
      "מים",
      "שמנים",
      "מייצבים",
      "סיבים",
      "חומרי טעם",
      "ויטמינים מוספים",
    ],
  },
} as const;

export const editorialDimensionKeys = [
  { key: "processing_quality", label: "איכות עיבוד" },
  { key: "whole_food_integrity", label: "שלמות מזון" },
  { key: "additive_quality", label: "עומס תוספים" },
  { key: "protein_quality", label: "איכות חלבון" },
  { key: "fat_quality", label: "איכות שומן" },
] as const;

export function getFlagshipProducts(): MilkComparisonProduct[] {
  const byBarcode = new Map(milkProducts.map((p) => [p.barcode, p]));
  const flagship = FLAGSHIP_BARCODES.map((b) => byBarcode.get(b)).filter(
    (p): p is MilkComparisonProduct => p != null
  );
  if (flagship.length >= 4) return flagship;
  return [...milkProducts].sort((a, b) => b.score - a.score).slice(0, 6);
}

export function getHeroFloatingProducts(): MilkComparisonProduct[] {
  return milkProducts.filter((p) => p.image_url).slice(0, 6);
}

/** Map engineering intensity to timeline step index 0–6 */
export function productTimelineIndex(product: MilkComparisonProduct): number {
  const depth = product.matrix_integrity.reconstruction_depth;
  const eng = product.matrix_integrity.engineering_intensity;
  if (eng >= 12 || depth >= 4) return 6;
  if (eng >= 6 || depth >= 3) return 5;
  if (eng >= 3 || depth >= 2) return 4;
  if (eng >= 1.5) return 3;
  if (eng >= 0.5) return 2;
  if (depth >= 1) return 1;
  return 0;
}

export function maxEngineeringIntensity(products: MilkComparisonProduct[]): number {
  return Math.max(1, ...products.map((p) => p.matrix_integrity.engineering_intensity));
}
