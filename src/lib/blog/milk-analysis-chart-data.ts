import { milkProducts } from "@/lib/comparisons/milk-page-data";
import type { MilkComparisonProduct, ProductType } from "@/lib/comparisons/milk-types";

/** Representative SKUs for editorial map — not full database */
export const FEATURED_MAP_BARCODES = [
  "7290000051352",
  "7290110324926",
  "7290116936116",
  "7394376620904",
  "7394376619939",
  "7290114313865",
] as const;

export type ScatterPoint = {
  product: MilkComparisonProduct;
  /** 0 = פשוט, 100 = מורכב */
  ingredientComplexity: number;
  /** 0 = יותר עיבוד, 100 = פחות עיבוד */
  lessProcessing: number;
  ingredientCount: number;
  label: string;
  shortLabel: string;
  placementInsight: string;
};

export const SCATTER_EDITORIAL_NOTES = [
  "חלב פרה בסיסי נוטה לפשטות רכיבים",
  "שיבולת שועל נוטה למבנה מורכב יותר",
  "סויה מובילה בחלבון אך לעיתים כוללת יותר רכיבים",
] as const;

export type HeroShelfCluster = {
  id: string;
  label: string;
  barcodes: string[];
};

export const PRODUCT_TYPE_COLORS: Record<ProductType, string> = {
  dairy: "#111318",
  soy: "#1F8F6A",
  oat: "#B8860B",
  almond: "#6B7B8C",
  rice: "#8B7355",
  coconut: "#5A9E7E",
  protein_drink: "#2D6A4F",
  other_plant: "#7A817C",
};

export const PRODUCT_TYPE_LABELS: Record<ProductType, string> = {
  dairy: "חלב פרה",
  soy: "סויה",
  oat: "שיבולת שועל",
  almond: "שקדים",
  rice: "אורז",
  coconut: "קוקוס",
  protein_drink: "משקה חלבון",
  other_plant: "צמחי אחר",
};

function dimScore(product: MilkComparisonProduct, key: string): number {
  return product.dimensions[key]?.score ?? 0;
}

function normalizeNutrientDensity(products: MilkComparisonProduct[]): Map<string, number> {
  const values = products.map((p) => dimScore(p, "nutrient_density"));
  const min = Math.min(...values);
  const max = Math.max(...values);
  const span = max - min || 1;
  return new Map(
    products.map((p) => [
      p.barcode,
      ((dimScore(p, "nutrient_density") - min) / span) * 100,
    ])
  );
}

const INGREDIENT_SEP = /[,،·]/;

function mergeUnclosedIngredientTokens(tokens: string[]): string[] {
  const out: string[] = [];
  let buffer = "";

  for (const token of tokens) {
    const piece = buffer ? `${buffer}, ${token}` : token;
    const open = (piece.match(/[\(\[\{]/g) ?? []).length;
    const close = (piece.match(/[\)\]\}]/g) ?? []).length;
    if (open > close) {
      buffer = piece;
      continue;
    }
    out.push(piece);
    buffer = "";
  }

  if (buffer) {
    out.push(buffer);
  }

  return out;
}

/** Parsed ingredient list — same logic as bar count and chip display */
export function parseIngredientsDisplay(raw: string | null | undefined): string[] {
  const text = raw?.trim();
  if (!text) return [];
  const tokens = text.split(INGREDIENT_SEP).map((s) => s.trim()).filter(Boolean);
  return mergeUnclosedIngredientTokens(tokens);
}

export function countIngredients(product: MilkComparisonProduct): number {
  const count = parseIngredientsDisplay(product.ingredients_display).length;
  return count || 1;
}

/** פשטות הרכב — higher = simpler */
export function compositionSimplicity(product: MilkComparisonProduct): number {
  const additive = dimScore(product, "additive_quality");
  const integrity = dimScore(product, "whole_food_integrity");
  return (additive + integrity) / 2;
}

/** תרומה תזונתית — higher = stronger nutritional profile in category */
export function nutritionalContribution(
  product: MilkComparisonProduct,
  densityNorm: Map<string, number>
): number {
  const protein = dimScore(product, "protein_quality");
  const density = densityNorm.get(product.barcode) ?? 0;
  const satiety = dimScore(product, "satiety_support");
  return protein * 0.45 + density * 0.35 + satiety * 0.2;
}

export function getPlacementInsight(product: MilkComparisonProduct): string {
  const count = countIngredients(product);
  const protein = product.proteinPer100ml ?? 0;
  const sugar = product.sugarPer100ml ?? 0;
  const simple = compositionSimplicity(product) >= 88;
  const complex = compositionSimplicity(product) < 65;
  const hasAdditives = !product.additivesLabel.includes("ללא");

  if (count <= 2 && simple) {
    return "רשימת רכיבים קצרה יחסית, ללא שכבות ייצוב משמעותיות.";
  }
  if (highProteinInsight(protein) && complex) {
    return "כמות חלבון גבוהה, אך עם מערכת רכיבים מורכבת יותר.";
  }
  if (product.productType === "oat" && sugar >= 4 && hasAdditives) {
    return "נבנה לטעם ולהקצפה — מרקם נעים שמגיע עם יותר סוכר ורכיבי מרקם.";
  }
  if (product.productType === "almond" && protein < 1) {
    return "קל יחסית בקלוריות, עם תרומת חלבון מוגבלת — מבנה פשוט יותר.";
  }
  if (complex && hasAdditives) {
    return "הרכבה שכבתית: מייצבים, רכיבי מרקם או העשרה שמסבירים את מיקום המוצר.";
  }
  if (simple && protein >= 2) {
    return "תרומה תזונתית סבירה עם מבנה יחסית ישיר — פחות שכבות ביניים.";
  }

  const takeaway = product.consumerTakeaway?.trim();
  if (takeaway && takeaway.length > 20) {
    return takeaway.length > 110 ? `${takeaway.slice(0, 107)}…` : takeaway;
  }
  return "מיקום המוצר משקף את האיזון בין פשטות הרכב לתרומה התזונתית בקטגוריה.";
}

function highProteinInsight(protein: number): boolean {
  return protein >= 2.8;
}

/** Higher = more ingredient complexity */
export function ingredientComplexityScore(product: MilkComparisonProduct): number {
  const simplicity = compositionSimplicity(product);
  const count = countIngredients(product);
  const countNorm = Math.min(100, (count / 12) * 100);
  return 100 - simplicity * 0.65 - countNorm * 0.35;
}

/** Higher = less processing (פחות עיבוד at top) */
export function lessProcessingScore(product: MilkComparisonProduct): number {
  return dimScore(product, "processing_quality");
}

function shortLabel(product: MilkComparisonProduct): string {
  const title = product.displayTitle ?? product.shortName;
  if (title.length <= 22) return title;
  const brand = product.brandLine ?? product.productTypeLabel;
  return brand.length <= 20 ? brand : product.productTypeLabel;
}

function toScatterPoint(product: MilkComparisonProduct): ScatterPoint {
  return {
    product,
    ingredientComplexity: ingredientComplexityScore(product),
    lessProcessing: lessProcessingScore(product),
    ingredientCount: countIngredients(product),
    label: product.displayTitle ?? product.shortName,
    shortLabel: shortLabel(product),
    placementInsight: getPlacementInsight(product),
  };
}

/** Shelf-map products (excludes protein drinks — separate functional category) */
export function buildScatterPoints(): ScatterPoint[] {
  return milkProducts
    .filter((p) => p.productType !== "protein_drink")
    .map(toScatterPoint);
}

export function buildFeaturedScatterPoints(): ScatterPoint[] {
  const byBarcode = new Map(milkProducts.map((p) => [p.barcode, p]));
  return FEATURED_MAP_BARCODES.map((barcode) => {
    const product = byBarcode.get(barcode);
    return product ? toScatterPoint(product) : null;
  }).filter((p): p is ScatterPoint => p != null);
}

export const heroShelfClusters: HeroShelfCluster[] = [
  {
    id: "dairy",
    label: "חלב פרה",
    barcodes: ["7290000051352", "7290019790259"],
  },
  {
    id: "soy",
    label: "סויה",
    barcodes: ["7290116936116", "7290110324926"],
  },
  {
    id: "oat",
    label: "שיבולת שועל",
    barcodes: ["5411188112709", "5411188300328"],
  },
  {
    id: "protein",
    label: "עתיר חלבון",
    barcodes: ["8000215204219", "8000215204554"],
  },
];

export function getHeroShelfProducts(): { cluster: HeroShelfCluster; products: MilkComparisonProduct[] }[] {
  const byBarcode = new Map(milkProducts.map((p) => [p.barcode, p]));
  return heroShelfClusters.map((cluster) => ({
    cluster,
    products: cluster.barcodes
      .map((b) => byBarcode.get(b))
      .filter((p): p is MilkComparisonProduct => p != null && !!p.image_url),
  }));
}

export type MilkComparisonNarrative = {
  id: string;
  title: string;
  subtitle: string;
  leftBarcode: string;
  rightBarcode: string;
  story: string;
  divergence: string;
  formulationNote: string;
  whatChanged: string;
};

export const milkComparisonNarratives: MilkComparisonNarrative[] = [
  {
    id: "soy-simple-vs-enriched",
    title: "סויה בסיסית מול סויה עם אסטרטגיית העשרה",
    subtitle: "אותה קטגוריה — שתי תפיסות פורמולציה שונות לחלוטין.",
    leftBarcode: "7290110324926",
    rightBarcode: "7290116936116",
    story:
      "שני המשקאות מתחילים מפולי סויה, אבל אחד שומר על מטריצה קרובה למקורית — והשני בנוי אסטרטגיית העשרה: ויטמינים, מינרלים ומייצבי מרקם שנוספו אחרי שהמבנה המקורי עבר פירוק חלקי. הציון אינו שיפוט; הוא מדד עומק ההרכבה.",
    divergence:
      "הפער אינו בגרם חלבון בודד על האריזה — אלא בנתיב: מבנה ראשוני מול הרכבה מחדש עם שכבות ייצוב והעשרה. שתיהן עונות על שאלה שונה.",
    formulationNote: "מוצר עם אסטרטגיית העשרה נוטה להכיל שכבות נוספות גם כשהכוונה מאחוריהן תזונתית לחלוטין. Bari מודד את עומק ההרכבה — לא את הכוונה.",
    whatChanged: "מייצבי מרקם, ויטמינים ומינרלים נוספו כדי לייצב פרופיל עקבי — על חשבון קיצור רשימת הרכיבים. הטריידאוף הוא בין ביצוע תזונתי לפשטות מבנית.",
  },
  {
    id: "oat-barista-vs-lighter",
    title: "שיבולת שועל לקפה מול שיבולת שועל מינימלית",
    subtitle: "הנדסת מרקם מכוונת מול פשטות בחירה — שתי תשובות לשתי שאלות שונות.",
    leftBarcode: "5411188112709",
    rightBarcode: "5411188300328",
    story:
      "גרסת הקפה עוצבה סביב דרישה טכנית: יצירת קצף עקבי מתחת לאספרסו. שמן חמניות, מייצבים וסיבים מבודדים אינם שגיאה בפורמולה — הם תנאי הכרחי לביצוע קולינרי. הגרסה הקלה ויתרה על הביצוע הזה כדי להרוויח פשטות.",
    divergence:
      "גרסת הקפה אופטימלית לביצוע בכוס קפה; הגרסה הקלה אופטימלית לרשימת רכיבים מינימלית. Bari לא שופט איזו שאלה חשובה יותר — הוא מודד כמה שכבות כל תשובה דרשה.",
    formulationNote: "הנדסת מרקם אינה ניטרלית מבחינת ציון — מייצבים ורכיבי תמיכה מוסיפים שכבות. ההקשר חשוב: שאלת השימוש קודמת לשאלת הפשטות.",
    whatChanged: "שמן, מייצבים וסיבים מבודדים נוספו בגרסת הקפה — לא כמילוי, אלא כמנגנון ביצועי. הגרסה הקלה מוותרת על הביצוע ומקבלת פרופיל רכיבים קצר יותר.",
  },
  {
    id: "dairy-vs-protein-system",
    title: "חלב פרה בסיסי מול מערכת חלבון מתוכננת",
    subtitle: "מבנה שהתפתח מול מבנה שתוכנן — שני לוגיקות של הגעה למדף.",
    leftBarcode: "7290000051352",
    rightBarcode: "8000215204219",
    story:
      "חלב מלא לא תוכנן — הוא קיים. מבנה הפרוטאין, השומן והלקטוז שלו נוצר אבולוציונית. משקה החלבון, לעומתו, תוכנן: פרוטאין יעד, שובע ממוקד ויציבות במדף. כל אחד מהרכיבים בא לענות על דרישה ספציפית של המוצר הסופי.",
    divergence:
      "ההבדל אינו בין «טבעי» ל«מעובד» — אלא בין מבנה שהתפתח לבין מבנה שתוכנן. Bari מודד את עומק ההרכבה; לא את הנכונות או ה«טבעיות» של המוצר.",
    formulationNote: "משקה שיוצר פרופיל חלבון כפול מחלב רגיל מחייב הרכבה שונה בתכלית. הביצועים גבוהים יותר; מורכבות הרכיבים גבוהה יותר. זהו טריידאוף, לא כישלון.",
    whatChanged: "בחלב: רשימת רכיבים בת פריט אחד. במשקה החלבון: מבודדי חלבון, מייצבים, העשרת ויטמינים ורכיבי מרקם — כל אחד מהם חלק מפתרון תזונתי שתוכנן מראש.",
  },
];

export type ShelfAnchor = {
  id: string;
  title: string;
  subtitle: string;
  insight: string;
  barcode: string;
};

export const shelfAnchors: ShelfAnchor[] = [
  {
    id: "dairy",
    title: "חלב בסיסי",
    subtitle: "רשימת רכיבים קצרה, מבנה ישיר",
    insight: "המוצר שנשאר הכי קרוב למה שרואים על האריזה.",
    barcode: "7290000051352",
  },
  {
    id: "soy",
    title: "סויה מועשרת",
    subtitle: "חלבון גבוה, לעיתים עם שכבות העשרה",
    insight: "מספק חלבון — לפעמים עם רכיבים נוספים בדרך.",
    barcode: "7290116936116",
  },
  {
    id: "oat",
    title: "שיבולת שועל לקפה",
    subtitle: "מרקם נעים, לעיתים יותר סוכר",
    insight: "נבנה לטעם ולהקצפה, לא רק לטבלה תזונתית.",
    barcode: "5411188112709",
  },
  {
    id: "protein",
    title: "משקה חלבון",
    subtitle: "ערך פונקציונלי ברור",
    insight: "מכוון ליעד — שובע וחלבון — עם הרכב מורכב יותר.",
    barcode: "8000215204219",
  },
  {
    id: "almond",
    title: "שקדים קל",
    subtitle: "קלוריות נמוכות, חלבון מוגבל",
    insight: "מתאים למי שמחפש משקה קל, פחות למי שמחפש חלבון.",
    barcode: "7394376619939",
  },
];

export function getProductByBarcode(barcode: string): MilkComparisonProduct | undefined {
  return milkProducts.find((p) => p.barcode === barcode);
}
