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
    slug: "sourdough-label",
    href: "#",
    title: "מה באמת מסתתר מאחורי מחמצת?",
    description:
      "כשהאריזה מבטיחה מסורת — מה רשימת הרכיבים והעיבוד מספרים בפועל.",
    cta: "בקרוב",
    category: "israeli-shelf",
    categoryLabel: "מדף ישראלי",
    readTime: "5 דקות",
    comingSoon: true,
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
