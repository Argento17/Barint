/**
 * Homepage carousel cards with real product data from published frontend JSONs.
 * Self-contained types — no circular imports with micro-comparison-snapshots.ts.
 */

export type CardVisual = {
  accent: string;
  photo?: string;
  productImages?: string[];
};

type ComparisonProductData = {
  name: string;
  brand: string;
  score: number;
  imageUrl?: string;
  strengths: [string, string];
};

type ComparisonCardWithVisual = {
  archetype: "comparison";
  id: string;
  category: string;
  title: string;
  href: string;
  tradeoff: string;
  leftProduct: ComparisonProductData;
  rightProduct: ComparisonProductData;
  visual: CardVisual;
};

type EditorialArchetype =
  | "investigation"
  | "category-report"
  | "ingredient"
  | "methodology"
  | "what-surprised-us"
  | "product-spotlight";

type EditorialCardWithVisual = {
  archetype: EditorialArchetype;
  id: string;
  category: string;
  title: string;
  href: string;
  eyebrow: string;
  finding: string;
  context?: string;
  stat?: { value: string; label: string };
  visual: CardVisual;
};

export type HomepageCardWithVisual =
  | ComparisonCardWithVisual
  | EditorialCardWithVisual;

const CL = "https://res.cloudinary.com/shufersal/image/upload/f_auto,q_auto/v1551800922/prod/product_images/products_zoom/";
const YO = "https://api.yochananof.co.il/media/catalog/product/cache/7d40ab1d2c85da43a7701c1338d70a16/";

export const HOMEPAGE_CAROUSEL_CARDS: HomepageCardWithVisual[] = [
  {
    archetype: "comparison",
    id: "bread-sourdough-vs-cracker",
    category: "לחם ומאפים",
    title: "מחמצת קמח מלא מול קרקר שומשום",
    href: "/hashvaot/bread",
    tradeoff: "המחמצת — 89 נקודות, 90% קמח מלא; הקרקר — 58, קמח מזוקק ותוספות.",
    leftProduct: {
      name: "לחם מחמצת קמח מלא",
      brand: "ארנה",
      score: 89,
      imageUrl: CL + "IUU18_Z_P_481203_1.png",
      strengths: ["קמח מלא ראשון ברשימה", "מחמצת שיפון אמיתית"],
    },
    rightProduct: {
      name: "קרקר שומשום אסם",
      brand: "אסם",
      score: 58,
      imageUrl: CL + "EUV20_Z_P_74252_1.png",
      strengths: ["נוח לנשיאה", "קל לכמת"],
    },
    visual: {
      accent: "#6B7B5E",
      photo: "/hashvaot/themes/bread.jpg",
      productImages: [
        CL + "IUU18_Z_P_481203_1.png",
        CL + "EUV20_Z_P_74252_1.png",
      ],
    },
  },

  {
    archetype: "comparison",
    id: "dairy-vs-plant",
    category: "חלב ותחליפים",
    title: "חלב מלא מול סויה ללא סוכר",
    href: "/hashvaot/milk-comparison",
    tradeoff: "חלב — רכיב יחיד, ציון A; סויה — 3 רכיבים בלבד אך צפיפות תזונתית נמוכה מורידה לציון C.",
    leftProduct: {
      name: "חלב מלא בטעם של פעם",
      brand: "תנובה",
      score: 85,
      imageUrl: YO + "7/2/7290000051352_s1_1502-12-2026_14-38-30.jpg",
      strengths: ["רכיב יחיד: חלב", "ציון A במדף"],
    },
    rightProduct: {
      name: "משקה סויה ללא סוכרים",
      brand: "תנובה אלטרנטיב",
      score: 64,
      imageUrl: YO + "7/2/7290116936116_s1_1512-04-2025_13-57-05.jpg",
      strengths: ["3 רכיבים בלבד", "ללא סוכר מוסף"],
    },
    visual: {
      accent: "#4A7B8C",
      photo: "/hashvaot/themes/milk.jpg",
      productImages: [
        YO + "7/2/7290000051352_s1_1502-12-2026_14-38-30.jpg",
        YO + "7/2/7290116936116_s1_1512-04-2025_13-57-05.jpg",
      ],
    },
  },

  {
    archetype: "comparison",
    id: "granola-premium-vs-bottom",
    category: "גרנולה",
    title: "גרנולה דני וגלית מול שוק קולינרי",
    href: "/hashvaot/granola",
    tradeoff: "38 נקודות מפרידות: שיבולת שועל ראשונה אצל דני וגלית; סוכר לפני שיבולת שועל אצל שוק קולינרי.",
    leftProduct: {
      name: "גרנולה חמוציות ושקדים",
      brand: "דני וגלית",
      score: 70,
      imageUrl: CL + "ARO54_Z_P_7290017962047_1.png",
      strengths: ["שיבולת שועל ראשונה", "ללא סירופ תירס"],
    },
    rightProduct: {
      name: "גרנולה עם פירות",
      brand: "שוק קולינרי",
      score: 31,
      imageUrl: CL + "KXI28_Z_P_1343845_1.png",
      strengths: ["מחיר נגיש", "פרי גלוי"],
    },
    visual: {
      accent: "#8B7355",
      photo: "/hashvaot/themes/granola.jpg",
      productImages: [
        CL + "ARO54_Z_P_7290017962047_1.png",
        CL + "KXI28_Z_P_1343845_1.png",
      ],
    },
  },

  {
    archetype: "product-spotlight",
    id: "bread-tahini-spotlight",
    category: "לחם ומאפים",
    title: "לחם טחינה פרוס — ציון 95",
    href: "/hashvaot/bread",
    eyebrow: "מוצר מוביל",
    finding: "הציון הגבוה ביותר מבין 29 לחמים: קמח מלא ראשון, טחינה טבעית, ללא סוכר מוסף ורשימה נקייה.",
    context: "מתוך 29 מוצרים שנסרקו",
    stat: { value: "95", label: "ציון Bari" },
    visual: {
      accent: "#6B7B5E",
      productImages: [CL + "JDU46_Z_P_7290016245325_1.png"],
    },
  },

  {
    archetype: "category-report",
    id: "cereals-report",
    category: "דגני בוקר",
    title: "20 דגנים — ואף אחד לא A",
    href: "/hashvaot/breakfast-cereals",
    eyebrow: "דוח קטגוריה",
    finding: "פרש ציונים 74.7–30.2 — הטוב ביותר B+, אין ציון A בכל המדף. הסוכר שולט ברשימה.",
    context: "20 מוצרים · פרש 44.5 נקודות",
    stat: { value: "20", label: "מוצרים" },
    visual: {
      accent: "#7A8C5E",
      photo: "/hashvaot/themes/breakfast-cereals.jpg",
      productImages: [
        CL + "KAG24_Z_P_5010029000061_1.png",
        CL + "ERH84_Z_P_7297488098688_1.png",
      ],
    },
  },

  {
    archetype: "category-report",
    id: "snacks-report",
    category: "חטיפים",
    title: "21 חטיפים: פרש 52 נקודות",
    href: "/hashvaot/snacks",
    eyebrow: "דוח קטגוריה",
    finding: "67 עד 15 — אותה קטגוריה, עולמות שונים. המוביל: תמרים וקינמון בלבד.",
    context: "21 מוצרים · ציון 67–15",
    stat: { value: "21", label: "מוצרים" },
    visual: {
      accent: "#BC6A33",
      photo: "/hashvaot/themes/snacks.jpg",
      productImages: [CL + "DPB48_Z_P_7290100659090_1.png"],
    },
  },

  {
    archetype: "category-report",
    id: "granola-category-report",
    category: "גרנולה",
    title: "22 גרנולות: פרש 38 נקודות",
    href: "/hashvaot/granola",
    eyebrow: "דוח קטגוריה",
    finding: "אם הסוכר מקדים את שיבולת השועל ברשימת הרכיבים — זה ממתק בשם גרנולה, לא גרנולה.",
    context: "22 מוצרים · ציון 70–31",
    stat: { value: "22", label: "מוצרים" },
    visual: {
      accent: "#8B7355",
      photo: "/hashvaot/themes/granola.jpg",
      productImages: [
        CL + "ARO54_Z_P_7290017962047_1.png",
        CL + "KXI28_Z_P_1343845_1.png",
      ],
    },
  },

  {
    archetype: "ingredient",
    id: "cereal-sugar-aliases",
    category: "חקירת מרכיב",
    title: "מלטוז, ממתיק גלוקוז-פרוקטוז, דבש — סוכר תחת שלוש מסכות",
    href: "/hashvaot/breakfast-cereals",
    eyebrow: "תובנת מרכיב",
    finding: "בדגנים עם תווית «דגנים מלאים»: מלטוז, ממתיק גלוקוז-פרוקטוז ודבש מופיעים כרכיבים שלישי-רביעי — שלושה שמות, מקור סוכר אחד.",
    context: "מתוך בדיקת 20 מוצרי דגני בוקר",
    visual: {
      accent: "#7A8C5E",
      photo: "/hashvaot/themes/breakfast-cereals.jpg",
    },
  },

  {
    archetype: "investigation",
    id: "magnesium-investigation",
    category: "תוספי תזונה",
    title: "18 מגנזיומים — הצורה הכימית מכריעה",
    href: "/hashvaot/magnesium",
    eyebrow: "חקירת קטגוריה",
    finding: "מגנזיום גליצינאט, ציטראט, תחמוצת — אותו מינרל, ספיגה שונה לחלוטין. הצורה הכימית קובעת יותר מהמינון.",
    context: "18 מוצרים מוכרים בישראל",
    stat: { value: "18", label: "מוצרים" },
    visual: {
      accent: "#4A7B8C",
      photo: "/hashvaot/themes/magnesium.jpg",
    },
  },
];
