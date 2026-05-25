export type ComparisonProductData = {
  name: string;
  brand: string;
  score: number;
  imageUrl?: string;
  strengths: [string, string];
};

export type ComparisonCard = {
  archetype: "comparison";
  id: string;
  category: string;
  title: string;
  href: string;
  tradeoff: string;
  leftProduct: ComparisonProductData;
  rightProduct: ComparisonProductData;
};

export type EditorialArchetype =
  | "investigation"
  | "category-report"
  | "ingredient"
  | "methodology"
  | "what-surprised-us"
  | "product-spotlight";

export type EditorialCard = {
  archetype: EditorialArchetype;
  id: string;
  category: string;
  title: string;
  href: string;
  eyebrow: string;
  finding: string;
  context?: string;
  stat?: { value: string; label: string };
};

export type HomepageCard = ComparisonCard | EditorialCard;

/** Homepage carousel — max 1–2 milk touches; diverse categories */
const CARDS: HomepageCard[] = [
  {
    archetype: "investigation",
    id: "bread-investigation",
    category: "לחם וקמח",
    title: "מה מסתיר לחם 'דגן מלא'",
    href: "/hashvaot",
    eyebrow: "חקירת קטגוריה",
    finding: "לעיתים פחות ממחצית הקמח הוא מלא — והתווית עדיין חוקית",
    context: "32 מוצרי לחם מהמדף הישראלי",
    stat: { value: "32", label: "מוצרים" },
  },
  {
    archetype: "category-report",
    id: "cereals-report",
    category: "דגנים וחטיפי בוקר",
    title: "דגני בוקר: מה באמת שולט בקופסה",
    href: "/hashvaot",
    eyebrow: "דוח קטגוריה",
    finding: "סוכר, דגנים מעובדים ושומנים — לעיתים יותר מאשר «דגנים מלאים» על האריזה",
    context: "24 מוצרים מובילים · 4 ארכיטיפים",
    stat: { value: "24", label: "מוצרים" },
  },
  {
    archetype: "category-report",
    id: "snack-bars-report",
    category: "חטיפי גרנולה",
    title: "גרנולה: המחיר השקט של «בריא»",
    href: "/hashvaot",
    eyebrow: "דוח קטגוריה",
    finding: "לעיתים שליש עד מחצית מהמשקל — סוכרים ושומנים, לא רק «גרנולה»",
    context: "14 חטיפים · 6 ארכיטיפים",
    stat: { value: "14", label: "מוצרים" },
  },
  {
    archetype: "ingredient",
    id: "sugar-names",
    category: "חקירת מרכיב",
    title: "12 שמות לסוכר, שם אחד שמחפשים פחות",
    href: "/hashvaot",
    eyebrow: "תובנת מרכיב",
    finding: "מייפל, דבש, טאפיוקה, מאלטוזה — אותו סוכר, שמות שונים על התווית",
  },
  {
    archetype: "methodology",
    id: "bari-methodology",
    category: "מתודולוגיה",
    title: "מה ציון Bari בודק שתזונאים לא מציגים",
    href: "/#methodology",
    eyebrow: "מתודולוגיה",
    finding: "8 אותות, השוואה לקטגוריה — מבנה ורכיבים, לא סיסמאות שיווק",
    stat: { value: "8", label: "אותות" },
  },
  {
    archetype: "investigation",
    id: "protein-products",
    category: "מוצרי חלבון",
    title: "14 גרם על האריזה — מה עוד ברשימה?",
    href: "/hashvaot",
    eyebrow: "חקירת קטגוריה",
    finding: "חלבון גבוה לא תמיד אומר רשימה קצרה; לעיתים יותר העשרה וייצוב",
    context: "יוגורטים, משקאות וחטיפים · בקרוב במלואם",
    stat: { value: "26", label: "מוצרים" },
  },
  {
    archetype: "comparison",
    id: "dairy-vs-plant",
    category: "חלב ותחליפים",
    title: "חלב מלא מול סויה ללא סוכר",
    href: "/hashvaot/milk-comparison",
    tradeoff: "חלב — פשטות רכיבים; סויה — חלבון צמחי ולעיתים יותר שכבות בפורמולה.",
    leftProduct: {
      name: "חלב מלא",
      brand: "חלב פרה",
      score: 85,
      imageUrl:
        "https://api.yochananof.co.il/media/catalog/product/cache/7d40ab1d2c85da43a7701c1338d70a16/7/2/7290000051352_s1_1502-12-2026_14-38-30.jpg",
      strengths: ["רשימה קצרה", "ציון גבוה בקטגוריה"],
    },
    rightProduct: {
      name: "סויה ללא סוכרים",
      brand: "תחליף צמחי · סויה",
      score: 67,
      imageUrl:
        "https://api.yochananof.co.il/media/catalog/product/cache/7d40ab1d2c85da43a7701c1338d70a16/7/2/7290116936116_s1_1512-04-2025_13-57-05.jpg",
      strengths: ["חלבון סויה בולט", "ללא סוכר מוסף"],
    },
  },
];

export function getHomepageCards(): HomepageCard[] {
  return CARDS;
}

export function getMicroComparisonSnapshots(): HomepageCard[] {
  return getHomepageCards();
}
