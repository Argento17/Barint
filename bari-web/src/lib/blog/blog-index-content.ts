import { SUGAR_ALCOHOLS_HREF } from "@/lib/blog/sugar-alcohols-article-content";

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
  stat?: { value: string; unit: string };
};

export const blogCategories: { id: BlogCategoryId; label: string }[] = [
  { id: "all", label: "הכל" },
  { id: "israeli-shelf", label: "מדף ישראלי" },
  { id: "ingredients", label: "רכיבים" },
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
  stat: { value: "18", unit: "מוצרים נותחו" },
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
    metaLine: "יוני 2026 · 7 דקות קריאה · 12 מותגים · 4 רשתות",
    published: "יוני 2026",
    stat: { value: "12", unit: "מותגים" },
  },
  {
    slug: "sugar-alcohols",
    href: SUGAR_ALCOHOLS_HREF,
    title: "קונים חטיף חלבון בגלל המספר הנמוך של הסוכר? כדאי לדעת מאיפה הוא בא",
    description:
      "מלטיטול וכוהלי סוכר אחרים מורידים את מספר הסוכר על האריזה דרך החלפה, לא הפחתה. הסברנו איך זה עובד.",
    cta: "לקריאת הניתוח",
    category: "ingredients",
    categoryLabel: "רכיבים",
    readTime: "6 דקות",
    published: "יוני 2026",
    metaLine: "יוני 2026 · 6 דקות קריאה · 32 חטיפים",
    stat: { value: "75%", unit: "מכילים מלטיטול" },
  },
];

export function articleMatchesCategory(
  article: BlogArticleCard,
  category: BlogCategoryId
): boolean {
  if (category === "all") return true;
  return article.category === category;
}
