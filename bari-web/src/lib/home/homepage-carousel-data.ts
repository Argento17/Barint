/**
 * Homepage carousel — 9 cards using the strict CarouselCard schema.
 * Rules enforced here:
 *  - comparison → visualMode:product_duel, products keyed by productId, pack images only
 *  - category_report → visualMode:score_spread, NO product images
 *  - ingredient_investigation → visualMode:ingredient_tokens, NO photos
 *  - supplement_report → visualMode:supplement_molecule, NO external bottle URLs
 *  - product_spotlight → visualMode:product_single, one pack by productId
 */

import type { CarouselCard } from "./homepage-carousel-schema";
import { CAROUSEL_PRODUCT_FALLBACK } from "./homepage-carousel-schema";

const CL =
  "https://res.cloudinary.com/shufersal/image/upload/f_auto,q_auto/v1551800922/prod/product_images/products_zoom/";
const YO =
  "https://api.yochananof.co.il/media/catalog/product/cache/7d40ab1d2c85da43a7701c1338d70a16/";

export { CAROUSEL_PRODUCT_FALLBACK };

export const HOMEPAGE_CAROUSEL_CARDS: CarouselCard[] = [
  // ── Comparison 1: Bread ────────────────────────────────────────────────────
  {
    id: "comparison-bread-sourdough-vs-cracker",
    type: "comparison",
    visualMode: "product_duel",
    eyebrow: "השוואה",
    category: "לחם ומאפים",
    title: "מחמצת קמח מלא מול קרקר שומשום",
    evidence: "פרש 31 נקודות: קמח מלא ראשון אצל המחמצת, קמח מזוקק אצל הקרקר.",
    metric: "89 מול 58",
    href: "/hashvaot/bread",
    accent: "#6B7B5E",
    fallbackVisual: CAROUSEL_PRODUCT_FALLBACK,
    leftProduct: {
      productId: "bsip1_bread_481203",
      barcode: "481203",
      name: "לחם מחמצת קמח מלא",
      brand: "ארנה",
      score: 89,
      imageUrl: CL + "IUU18_Z_P_481203_1.png",
      imageAlt: "לחם מחמצת קמח מלא ארנה",
      imageStatus: "verified",
    },
    rightProduct: {
      productId: "bsip1_bread_74252",
      barcode: "74252",
      name: "קרקר שומשום",
      brand: "אסם",
      score: 58,
      imageUrl: CL + "EUV20_Z_P_74252_1.png",
      imageAlt: "קרקר שומשום אסם",
      imageStatus: "verified",
    },
  },

  // ── Comparison 2: Milk ─────────────────────────────────────────────────────
  {
    id: "comparison-milk-whole-vs-soy",
    type: "comparison",
    visualMode: "product_duel",
    eyebrow: "השוואה",
    category: "חלב ותחליפים",
    title: "חלב מלא מול משקה סויה",
    evidence: "חלב — רכיב יחיד; סויה — 3 רכיבים, צפיפות תזונתית נמוכה יותר.",
    metric: "85 מול 64",
    href: "/hashvaot/milk-comparison",
    accent: "#4A7B8C",
    fallbackVisual: CAROUSEL_PRODUCT_FALLBACK,
    leftProduct: {
      productId: "milk_7290000051352",
      barcode: "7290000051352",
      name: "חלב מלא",
      brand: "תנובה",
      score: 85,
      imageUrl: YO + "7/2/7290000051352_s1_1502-12-2026_14-38-30.jpg",
      imageAlt: "חלב מלא תנובה",
      imageStatus: "verified",
    },
    rightProduct: {
      productId: "milk_7290116936116",
      barcode: "7290116936116",
      name: "משקה סויה ללא סוכרים",
      brand: "תנובה אלטרנטיב",
      score: 64,
      imageUrl: YO + "7/2/7290116936116_s1_1512-04-2025_13-57-05.jpg",
      imageAlt: "משקה סויה ללא סוכרים תנובה אלטרנטיב",
      imageStatus: "verified",
    },
  },

  // ── Comparison 3: Granola ──────────────────────────────────────────────────
  {
    id: "comparison-granola-premium-vs-bottom",
    type: "comparison",
    visualMode: "product_duel",
    eyebrow: "השוואה",
    category: "גרנולה",
    title: "גרנולה דני וגלית מול שוק קולינרי",
    evidence: "38 נקודות פרש: שיבולת שועל ראשונה אצל דני וגלית, סוכר ראשון אצל שוק קולינרי.",
    metric: "70 מול 31",
    href: "/hashvaot/granola",
    accent: "#8B7355",
    fallbackVisual: CAROUSEL_PRODUCT_FALLBACK,
    leftProduct: {
      productId: "bsip1_cereal_7290017962047",
      barcode: "7290017962047",
      name: "גרנולה חמוציות ושקדים",
      brand: "דני וגלית",
      score: 70,
      imageUrl: CL + "ARO54_Z_P_7290017962047_1.png",
      imageAlt: "גרנולה חמוציות ושקדים דני וגלית",
      imageStatus: "verified",
    },
    rightProduct: {
      productId: "bsip1_cereal_1343845",
      barcode: "1343845",
      name: "גרנולה עם פירות",
      brand: "שוק קולינרי",
      score: 31,
      imageUrl: CL + "KXI28_Z_P_1343845_1.png",
      imageAlt: "גרנולה עם פירות שוק קולינרי",
      imageStatus: "verified",
    },
  },

  // ── Product spotlight: Tahini bread ───────────────────────────────────────
  {
    id: "spotlight-bread-tahini",
    type: "product_spotlight",
    visualMode: "product_single",
    eyebrow: "מוצר מוביל",
    category: "לחם ומאפים",
    title: "לחם טחינה — ציון 95",
    evidence: "הציון הגבוה ביותר מבין 29 לחמים: קמח מלא ראשון, טחינה טבעית, ללא סוכר.",
    metric: "95 / A",
    href: "/hashvaot/bread",
    accent: "#6B7B5E",
    fallbackVisual: CAROUSEL_PRODUCT_FALLBACK,
    spotlightProduct: {
      productId: "bsip1_bread_7290016245325",
      barcode: "7290016245325",
      name: "לחם טחינה פרוס",
      brand: "לחם ארץ",
      score: 95,
      imageUrl: CL + "JDU46_Z_P_7290016245325_1.png",
      imageAlt: "לחם טחינה פרוס לחם ארץ",
      imageStatus: "verified",
    },
  },

  // ── Category report: Cereals ───────────────────────────────────────────────
  {
    id: "category-report-cereals",
    type: "category_report",
    visualMode: "score_spread",
    eyebrow: "דוח קטגוריה",
    category: "דגני בוקר",
    title: "20 דגנים — אפילו הטוב ביותר לא A",
    evidence: "הסוכר שולט: גם המוביל מסתיים ב-B+. אין ציון A בכל המדף.",
    metric: "פרש 44.5 נקודות",
    href: "/hashvaot/breakfast-cereals",
    accent: "#7A8C5E",
    scoreSpread: { low: 30, high: 75, count: 20, label: "דגני בוקר" },
  },

  // ── Category report: Snacks ────────────────────────────────────────────────
  {
    id: "category-report-snacks",
    type: "category_report",
    visualMode: "score_spread",
    eyebrow: "דוח קטגוריה",
    category: "חטיפים",
    title: "21 חטיפים: פרש 52 נקודות",
    evidence: "67 עד 15 — אותה קטגוריה, עולמות שונים. המוביל: תמרים וקינמון בלבד.",
    metric: "ציון 15–67",
    href: "/hashvaot/snacks",
    accent: "#BC6A33",
    scoreSpread: { low: 15, high: 67, count: 21, label: "חטיפים" },
  },

  // ── Category report: Granola ───────────────────────────────────────────────
  {
    id: "category-report-granola",
    type: "category_report",
    visualMode: "score_spread",
    eyebrow: "דוח קטגוריה",
    category: "גרנולה",
    title: "22 גרנולות: מי באמת בריא?",
    evidence: "אם הסוכר מקדים שיבולת שועל — זה ממתק, לא גרנולה.",
    metric: "ציון 31–70",
    href: "/hashvaot/granola",
    accent: "#8B7355",
    scoreSpread: { low: 31, high: 70, count: 22, label: "גרנולות" },
  },

  // ── Ingredient investigation ───────────────────────────────────────────────
  {
    id: "ingredient-cereal-sugar-aliases",
    type: "ingredient_investigation",
    visualMode: "ingredient_tokens",
    eyebrow: "חקירת מרכיב",
    category: "דגני בוקר",
    title: "סוכר תחת שלוש מסכות",
    evidence: "מלטוז, ממתיק גלוקוז-פרוקטוז ודבש — שלושה שמות, מקור סוכר אחד ב-20 דגנים.",
    metric: "20 מוצרים נבדקו",
    href: "/hashvaot/breakfast-cereals",
    accent: "#7A8C5E",
    ingredientTokens: ["מלטוז", "ממתיק גלוקוז-פרוקטוז", "דבש"],
  },

  // ── Supplement report: Magnesium ───────────────────────────────────────────
  {
    id: "supplement-magnesium-form",
    type: "supplement_report",
    visualMode: "supplement_molecule",
    eyebrow: "חקירת קטגוריה",
    category: "תוספי תזונה",
    title: "18 מגנזיומים — הצורה קובעת",
    evidence: "גליצינאט, ציטראט, תחמוצת — אותו מינרל, ספיגה שונה לחלוטין.",
    metric: "18 מוצרים",
    href: "/hashvaot/magnesium",
    accent: "#4A7B8C",
    supplementStat: { value: "18", label: "מוצרים" },
  },
];
