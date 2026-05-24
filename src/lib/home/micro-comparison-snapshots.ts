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
  | "what-surprised-us";

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

const CARDS: HomepageCard[] = [
  {
    archetype: "comparison",
    id: "dairy-vs-soy",
    category: "חלב ותחליפים",
    title: "חלב מלא מול משקה סויה",
    href: "/hashvaot/milk-comparison",
    tradeoff:
      "חלב הפרה המלא מוביל במבנה פשוט ואפס תוספים; הסויה — ביתרון חלבוני ממוקד ומתאים לנמנעים מחלב.",
    leftProduct: {
      name: "חלב מלא תנובה",
      brand: "חלב פרה",
      score: 85,
      imageUrl:
        "https://api.yochananof.co.il/media/catalog/product/cache/7d40ab1d2c85da43a7701c1338d70a16/7/2/7290000051352_s1_1502-12-2026_14-38-30.jpg",
      strengths: ["מבנה פשוט, ללא תוספים", "ציון A — מהטובים בקטגוריה"],
    },
    rightProduct: {
      name: "משקה סויה ללא סוכרים",
      brand: "תנובה אלטרנטיב · סויה",
      score: 67,
      imageUrl:
        "https://api.yochananof.co.il/media/catalog/product/cache/7d40ab1d2c85da43a7701c1338d70a16/7/2/7290116936116_s1_1512-04-2025_13-57-05.jpg",
      strengths: ["3.3 ג׳ חלבון / 100 מ״ל", "מתאים לנמנעים מחלב"],
    },
  },
  {
    archetype: "investigation",
    id: "bread-investigation",
    category: "לחם וקמח",
    title: "מה מסתיר לחם 'דגן מלא'",
    href: "/hashvaot",
    eyebrow: "חקירת קטגוריה",
    finding:
      "רוב לחמי הדגנים המלאים מכילים פחות מ-50% קמח מלא — והתווית חוקית לחלוטין",
    context: "מתוך ניתוח 32 מוצרי לחם מהמדף הישראלי",
    stat: { value: "32", label: "מוצרים נבדקו" },
  },
  {
    archetype: "category-report",
    id: "snack-bars-report",
    category: "חטיפי גרנולה",
    title: "גרנולה: המיתוס הבריאותי הכי יקר במדף",
    href: "/hashvaot",
    eyebrow: "דוח קטגוריה",
    finding:
      "גרנולה בר ממוצע — 35–45% מהמשקל סוכרים ושמנים. השיווק מוביל; הנתונים, פחות",
    context: "14 חטיפים מובילים · 6 ארכיטיפים",
    stat: { value: "14", label: "מוצרים" },
  },
  {
    archetype: "ingredient",
    id: "sugar-names",
    category: "מרכיב · סוכר",
    title: "12 שמות לסוכר, שם אחד שמחפשים פחות",
    href: "/hashvaot",
    eyebrow: "תובנת מרכיב",
    finding:
      "סירופ מייפל, דבש, טאפיוקה, מאלטוזה — כולם סוכר בצורות שונות. ממצא מתוך 200+ מוצרים",
  },
  {
    archetype: "methodology",
    id: "bari-methodology",
    category: "מתודולוגיה",
    title: "מה ציון Bari בודק שתזונאים לא מציגים",
    href: "/hashvaot",
    eyebrow: "מתודולוגיה",
    finding:
      "7 ממדים, 40+ אותות — מדד שמשקף מבנה תזונתי, לא הבטחות שיווקיות",
    stat: { value: "7", label: "ממדי ניתוח" },
  },
  {
    archetype: "what-surprised-us",
    id: "almond-surprise",
    category: "מה הפתיע אותנו",
    title: "חלב שקדים עם 1–2% שקדים",
    href: "/hashvaot/milk-comparison",
    eyebrow: "ממצא מפתיע",
    finding:
      "בדקנו: רוב משקאות השקדים בישראל מכילים 1–2% שקדים בלבד. המרכיב העיקרי — מים",
  },
];

export function getHomepageCards(): HomepageCard[] {
  return CARDS;
}
