import { breadEditorial } from "@/lib/comparisons/bread-editorial-content";
import { breadProducts, getBreadFlagshipProducts } from "@/lib/comparisons/bread-page-data";
import type { BreadProduct } from "@/lib/comparisons/bread-types";

export const BREAD_BLOG_HREF = "/blog/bread-analysis";
export const BREAD_COMPARISON_HREF = "/hashvaot/bread-comparison";

function ingredientCount(product: BreadProduct) {
  return product.ingredients_display
    .split(",")
    .map((part) => part.trim())
    .filter(Boolean).length;
}

export const breadAnalysisArticle = {
  slug: "bread-analysis",
  hero: {
    eyebrow: "ניתוח · מדף ישראלי",
    title: "מה באמת קורה במדף הלחמים?",
    subtitle:
      "בדקנו 32 מוצרי לחם, קרקר וקריספ פופולריים בישראל כדי להבין איפה המדף באמת מתפצל: רשימות רכיבים, מחמצת, מקור סיבים, רמת עיבוד והפער בין שם המוצר לבין המבנה שלו בפועל.",
    meta: "מאי 2026 · 7 דקות קריאה · 32 מוצרים נותחו",
  },
  disclaimer:
    "הניתוח מבוסס על השוואה קטגוריאלית בין מוצרים דומים במדף הישראלי. לא מדובר בהמלצה רפואית או תזונתית אישית.",
  lead: [
    breadEditorial.lead[0],
    breadEditorial.lead[1],
    breadEditorial.lead[2],
  ],
  editorialInsights: [
    "מחמצת על האריזה לא תמיד מספרת שהיה כאן תהליך מחמצת אמיתי.",
    "גם כשמספר הסיבים מרשים, חשוב לבדוק אם הם מגיעים מהדגן או מתוסף שנוסף אחר כך.",
    "אותו מדף מציג יחד מוצרים שנראים קרובים מאוד, אבל בנויים כמעט משפות מזון שונות.",
  ],
  findings: {
    title: "תובנות שחזרו שוב ושוב",
    subtitle:
      "לא מקרים חריגים, אלא דפוסים שחזרו שוב ושוב לאורך המדף והסבירו למה מוצרים דומים מקבלים קריאה אחרת.",
    items: [
      {
        title: "מחמצת לא תמיד אומרת פחות רכיבים",
        finding:
          "במוצרים שבהם המחמצת היתה חלק מתהליך אמיתי, ראינו בדרך כלל מבנה פשוט יותר ותוצאה גבוהה יותר. במוצרים אחרים, היא נשארה בעיקר שכבת טעם.",
        whyItMatters:
          "שתי אריזות יכולות להשתמש באותה מילה בדיוק, אבל לספר על שני תהליכי ייצור שונים לגמרי. זה פער שקשה לראות בלי לקרוא לעומק.",
      },
      {
        title: "פער קטן בשם — פער גדול במבנה",
        finding:
          "מוצרים כמעט זהים בשם ובשפה הוויזואלית הגיעו שוב ושוב לבסיסים שונים מאוד: דגן שלם מצד אחד, קמח לבן עם תוספות מצד שני.",
        whyItMatters:
          "הצרכן קורא כותרת קצרה, אבל ההבדל האמיתי מתחיל ברשימת הרכיבים ובאופן שבו המוצר נבנה בפועל.",
      },
      {
        title: "גם לחמים 'בריאים' יכולים להיות מעובדים מאוד",
        finding:
          "מוצרים עשירים בסיבים, חלבון או הבטחות תפקודיות אחרות דרשו לא פעם יותר שכבות הרכבה, יותר תוספות ויותר פער מהמבנה הדגני הפשוט.",
        whyItMatters:
          "הבטחה תזונתית יכולה להיות רלוונטית מאוד, אבל היא לא אומרת שהמוצר נשאר קרוב ללחם בסיסי. אלו שני דברים שונים.",
      },
    ],
  },
  archetypes: {
    title: "דפוסים שחזרו במדף",
    subtitle: "שישה מבנים שחזרו שוב ושוב לאורך הקטגוריה, ולא רק על מוצר אחד בודד.",
  },
  lookalikes: {
    title: "נראים אותו דבר — אבל לא אותו דבר",
    subtitle:
      "אריזות דומות וטענות דומות, עם פערים שנפתחים דווקא במבנה, בתסיסה ובמקור הסיבים.",
  },
  productPreview: {
    title: "שישה מוצרים, שישה מבנים",
    subtitle: "כמה דוגמאות מתוך הדוח, כדי לראות איך אותה קטגוריה מתפצלת למבנים שונים.",
  },
  howToRead: {
    title: "איך לקרוא את ההשוואה",
    lead:
      "המטרה היא לא לבחור 'לחם מושלם', אלא להבין מה עומד מאחורי מוצרים שנראים דומים על המדף.",
    rows: [
      {
        label: "ציון Bari",
        text: "סיכום קטגוריאלי של מבנה רכיבים, תסיסה, מקור סיבים ורמת עיבוד בתוך משפחת המוצר.",
      },
      {
        label: "רשימת רכיבים",
        text: "כאן רואים אם הבסיס נשאר פשוט יחסית, או שנבנתה שכבת הרכבה שלמה מעליו.",
      },
      {
        label: "מקור הסיבים",
        text: "לא רק כמה סיבים יש, אלא אם הם מגיעים מתוך הדגן או מתוספים מבודדים שנוספו אחר כך.",
      },
      {
        label: "מחמצת ועיבוד",
        text: "מילה כמו 'מחמצת' אינה מספיקה. חשוב להבין אם מדובר בתהליך אמיתי או בעיקר בשפה שיווקית.",
      },
    ],
  },
  methodology: {
    title: "איך בדקנו",
    steps: [
      {
        title: "אספנו מוצרים אמיתיים",
        text: "32 מוצרי לחם, קרקר וקריספ שנמכרים בישראל.",
      },
      {
        title: "פירקנו את המבנה",
        text: "רשימות רכיבים, תסיסה, מקור סיבים, חלבון, סוכר ורמת עיבוד.",
      },
      {
        title: "השווינו בתוך משפחות דומות",
        text: "כל מוצר נקרא מול מוצרים מאותה משפחה, לא מול כל המזון במדף.",
      },
    ],
    footnote:
      "הציון והפירוט מוצגים בהשוואה למוצרים דומים בקטגוריה — לא כהכרעה אוניברסלית על כל סוגי הלחם.",
  },
  ctaPrimary: {
    title: "רוצים לראות את ההשוואה המלאה?",
    description:
      "בדוח ההשוואה אפשר לראות את כל 32 המוצרים, לסנן לפי סוגי לחם, ולפתוח פירוט מוצר-מוצר לפי מבנה, רכיבים והקשר קטגוריאלי.",
    button: "פתיחת דוח ההשוואה",
  },
  conclusion: {
    title: "אין לחם אחד שמתאים לכולם — וזה חלק מהסיפור",
    paragraphs: [
      "מדף הלחמים לא מחולק לטובים ורעים. הוא מחולק למבנים שונים, צרכים שונים ורמות שונות של פשטות או הנדסה.",
      "לחם מחמצת מסורתי, קריספ שיפון פשוט או מוצר פונקציונלי עתיר חלבון לא מנסים לעשות אותו דבר. לכן גם אי אפשר לקרוא אותם באותה דרך.",
      "הערך של Bari כאן הוא לא לבחור בשבילכם, אלא להראות מה עומד מאחורי המילים על האריזה: מאיפה מגיעים הסיבים, מה באמת עושה המחמצת, וכמה שכבות נדרשו כדי לבנות את המוצר.",
    ],
    cta: "לדוח ההשוואה המלא",
  },
} as const;

export function getBreadPreviewProducts(): BreadProduct[] {
  return getBreadFlagshipProducts();
}

export function getBreadPreviewTags(product: BreadProduct): string[] {
  const tags: string[] = [];

  const ingredients = ingredientCount(product);
  if (ingredients <= 4) tags.push("רכיבים פשוטים");
  else if (ingredients >= 8) tags.push("הרכבה מורכבת");

  if (product.fiber_q === "structural") tags.push("סיבים מתוך הדגן");
  else if (product.fiber_q === "isolated") tags.push("סיבים מתוספים");

  if (product.ferm_q === "traditional") tags.push("מחמצת אמיתית");
  else if (product.ferm_q === "flavor_only") tags.push("מחמצת לטעם");

  if (product.gss >= 75) tags.push("מבנה דגני מובהק");
  else if (product.gss <= 35) tags.push("בסיס רחוק מדגן מלא");

  return [...new Set(tags)].slice(0, 3);
}

export function getBreadBlogMetaLine() {
  return `${breadProducts.length} מוצרים · ${breadEditorial.archetypes.length} דפוסים · מדף ישראלי`;
}
