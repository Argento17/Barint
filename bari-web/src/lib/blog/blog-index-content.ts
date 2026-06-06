import {
  BREAD_EVERYDAY_HREF,
  BREAD_STANDOUTS_HREF,
  BREAD_WELLNESS_HREF,
} from "@/lib/blog/bread-analysis-content";

export type BlogCategoryId =
  | "all"
  | "comparisons"
  | "ingredients"
  | "processing"
  | "israeli-shelf"
  | "bari-labs";

export type BlogArticleCard = {
  slug: string;
  href: string;
  title: string;
  description: string;
  cta: string;
  category: BlogCategoryId;
  categoryLabel: string;
  readTime: string;
  published?: string;
  metaLine?: string;
  featured?: boolean;
  comingSoon?: boolean;
};

export const blogCategories: { id: BlogCategoryId; label: string }[] = [
  { id: "all", label: "הכל" },
  { id: "comparisons", label: "השוואות" },
  { id: "ingredients", label: "רכיבים" },
  { id: "processing", label: "עיבוד" },
  { id: "israeli-shelf", label: "מדף ישראלי" },
  { id: "bari-labs", label: "Bari Labs" },
];

export const blogIndex = {
  eyebrow: "BARI FOOD INTELLIGENCE",
  title: "בלוג Bari",
  subtitle: "ניתוחי מוצרים, רכיבים והשוואות מזון מבוססי נתונים.",
  supporting:
    "מוצרים אמיתיים מהמדף הישראלי — מפורקים לרכיבים, עיבוד, תוספים והקשר צרכני.",
  featuredSectionLabel: "ניתוח מוביל",
  articlesSectionLabel: "מהמדף ומהמעבדה",
  labs: {
    title: "Bari Labs",
    text: "המקום שבו Bari מפרקת קטגוריות מזון, משווה מוצרים אמיתיים ומתרגמת נתונים לתובנות ברורות.",
    tags: ["רכיבים", "עיבוד", "תוספים", "מדף ישראלי"] as const,
  },
  comparisonsNote:
    "לסינון, ציונים ופירוט מוצר-מוצר — מנוע ההשוואה האינטראקטיבי ב",
  comparisonsHref: "/hashvaot",
} as const;

export const featuredArticle: BlogArticleCard = {
  slug: "milk-analysis",
  href: "/blog/milk-analysis",
  title: "מה באמת קורה במדף החלב?",
  description:
    "בדקנו 18 מוצרי חלב ומשקאות חלב פופולריים בישראל כדי להבין איך רכיבים, חלבון, סוכר, תוספים ורמת עיבוד משתנים בין מוצרים שנראים כמעט זהים.",
  cta: "לקריאת הניתוח",
  category: "israeli-shelf",
  categoryLabel: "מדף ישראלי",
  readTime: "6 דקות",
  published: "מאי 2026",
  metaLine: "מאי 2026 · 6 דקות קריאה · 18 מוצרים נותחו",
  featured: true,
};

export const secondaryArticles: BlogArticleCard[] = [
  {
    slug: "shemen-zayit",
    href: "/blog/shemen-zayit",
    title: "20 שמני זית. 10 מותגים. אפס גילויים על תאריך הקציר.",
    description:
      "שופרסל מוכרת BORGES ו-MATTEO. יוחננוף מוכרת יד מרדכי, סבא חביב, ג'השאן, זיתא. שוק אחד, שני מדפים שונים לגמרי — ואף אחד לא מצהיר על תאריך קציר.",
    cta: "לקריאת הניתוח",
    category: "israeli-shelf",
    categoryLabel: "מדף ישראלי",
    readTime: "7 דקות",
    metaLine: "יוני 2026 · 7 דקות קריאה · 10 מותגים",
    published: "יוני 2026",
  },
  {
    slug: "bread-everyday",
    href: BREAD_EVERYDAY_HREF,
    title: "לחם יומיומי: למה מוצרים שנשמעים דומים מתפצלים בציון",
    description:
      "שיפון מלא (76) מול מחמצת בשם (61) — מה ברשימת הרכיבים מסביר את הפער על אותו מדף.",
    cta: "לקריאת הניתוח",
    category: "israeli-shelf",
    categoryLabel: "מדף ישראלי",
    readTime: "5 דקות",
    metaLine: "מאי 2026 · 5 דקות קריאה · לחם יומיומי",
  },
  {
    slug: "bread-standouts",
    href: BREAD_STANDOUTS_HREF,
    title: "לחם שבלט — ולחם שנשמע פרימיום אבל לא מחזיק",
    description:
      "פער של 20 נקודות בין לחם ירוק מקמח מלא ללחם מחמצת אגוזים צימוקים — שניהם על אותו מדף.",
    cta: "לקריאת הניתוח",
    category: "israeli-shelf",
    categoryLabel: "מדף ישראלי",
    readTime: "6 דקות",
    metaLine: "מאי 2026 · 6 דקות קריאה · מוצרים בולטים",
  },
  {
    slug: "bread-wellness-gap",
    href: BREAD_WELLNESS_HREF,
    title: "לחמי בריאות: אותו מדף, פערים של 22 נקודות",
    description:
      "לחם טחינה (82) מול מחמצת אגוזים צימוקים (60) — למה מוצרים שנשמעים דומים נפרדו בניתוח.",
    cta: "לקריאת הניתוח",
    category: "israeli-shelf",
    categoryLabel: "מדף ישראלי",
    readTime: "6 דקות",
    metaLine: "מאי 2026 · 6 דקות קריאה · פרמיום מול מבנה",
  },
  {
    slug: "fiber-crackers-vs-bread",
    href: "#",
    title: "למה קרקרים עתירי סיבים לא תמיד דומים ללחם מלא?",
    description: "אותה הבטחה על האריזה — מבנה שונה לגמרי מתחת.",
    cta: "בקרוב",
    category: "comparisons",
    categoryLabel: "השוואות",
    readTime: "6 דקות",
    comingSoon: true,
  },
  {
    slug: "protein-engineered",
    href: "#",
    title: "איך מוצר עם 14 גרם חלבון עדיין נשאר מאוד מהונדס?",
    description: "כשהמספר על האריזה חזק — אבל רשימת הרכיבים ארוכה.",
    cta: "בקרוב",
    category: "processing",
    categoryLabel: "עיבוד",
    readTime: "5 דקות",
    comingSoon: true,
  },
  {
    slug: "short-ingredient-list",
    href: "#",
    title: "למה רשימת רכיבים קצרה לא תמיד מספרת את כל הסיפור?",
    description: "מינימליזם על הנייר מול מה שקורה בתהליך הייצור.",
    cta: "בקרוב",
    category: "ingredients",
    categoryLabel: "רכיבים",
    readTime: "4 דקות",
    comingSoon: true,
  },
  {
    slug: "oat-drinks-deep",
    href: "#",
    title: "מה באמת קורה במשקאות שיבולת שועל?",
    description: "מרקם, סוכר, ייצוב — ומה מפריד בין גרסת קפה לגרסה קלה.",
    cta: "בקרוב",
    category: "israeli-shelf",
    categoryLabel: "מדף ישראלי",
    readTime: "6 דקות",
    comingSoon: true,
  },
  {
    slug: "ingredient-list-reading",
    href: "#",
    title: "איך לקרוא רשימת רכיבים בלי ללכת לאיבוד",
    description:
      "סדר הופעה, קיצורים ורכיבים תפקודיים — מדריך קצר לקריאה מדויקת של תווית.",
    cta: "בקרוב",
    category: "ingredients",
    categoryLabel: "רכיבים",
    readTime: "7 דקות",
    comingSoon: true,
  },
  {
    slug: "labs-category-teaser",
    href: "#",
    title: "מעבדת מדף: יוגורטים ומוצרי חלבון",
    description: "סדרת ניתוחים קטגורית — מוצרים אמיתיים מהמדף הישראלי.",
    cta: "בקרוב",
    category: "bari-labs",
    categoryLabel: "Bari Labs",
    readTime: "8 דקות",
    comingSoon: true,
  },
];

export function articleMatchesCategory(
  article: BlogArticleCard,
  category: BlogCategoryId
): boolean {
  if (category === "all") return true;
  return article.category === category;
}
