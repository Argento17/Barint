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

export function countIngredients(product: MilkComparisonProduct): number {
  const raw = product.ingredients_display?.trim();
  if (!raw) return 1;
  return raw.split(/[,،·]/).map((s) => s.trim()).filter(Boolean).length;
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
    title: "סויה בסיסית מול סויה מועשרת",
    subtitle: "אותה קטגוריה על המדף — מטרות פורמולציה שונות.",
    leftBarcode: "7290110324926",
    rightBarcode: "7290116936116",
    story:
      "שני המשקאות נמכרים כסויה, אבל אחד נשאר קרוב יותר למבנה מינימלי והשני בנוי סביב חלבון ויציבות.",
    divergence:
      "פער הציון נובע בעיקר מאריכות רשימת הרכיבים, מערכת ייצוב והעשרה — לא רק מגרם חלבון אחד על האריזה.",
    formulationNote: "המוצר המועשר פותר בעיה תזונתית ברורה; המוצר הפשוט יותר פותר בעיית מינימליזם מבני.",
    whatChanged: "נוספו שכבות של העשרה, מייצבים ורכיבי מרקם כדי להגיע לפרופיל חלבון גבוה יותר.",
  },
  {
    id: "oat-barista-vs-lighter",
    title: "שיבולת שועל לקפה מול שיבולת שועל קלה יותר",
    subtitle: "שני מוצרים שנראים כמו אותו מדף — אבל נבנו לשימושים שונים.",
    leftBarcode: "5411188112709",
    rightBarcode: "5411188300328",
    story:
      "גרסת הקפה מכוונת להקצפה ולמרקם; הגרסה השנייה מכוונת לפרופיל קל יותר — וההבדל עובר דרך הרכב, לא רק דרך הסוכר.",
    divergence:
      "הפער נובע משילוב של סוכר, רכיבי מרקם ועומק עיבוד — לא ממילה אחת על האריזה.",
    formulationNote: "מרקם נעים לקפה לרוב דורש יותר תמיכה טכנולוגית ברשימת הרכיבים.",
    whatChanged: "יותר רכיבים תומכי מרקם וייצוב בגרסת הקפה; פחות שכבות בגרסה הקלה.",
  },
  {
    id: "dairy-vs-protein-system",
    title: "חלב פרה בסיסי מול מערכת חלבון מהונדסת",
    subtitle: "מוצר מינימלי לעומת מוצר פונקציונלי — שני סיפורים שונים על אותו מדף.",
    leftBarcode: "7290000051352",
    rightBarcode: "8000215204219",
    story:
      "החלב נשען על מבנה פשוט; משקה החלבון נשען על הרכבה שמכוונת ליעד תזונתי ברור.",
    divergence:
      "ההבדל אינו רק בציון — אלא בכמה שכבות נדרשו כדי שהמוצר ייראה, ירגיש ויתנהג כפי שמתוכנן.",
    formulationNote: "מוצר החלבון פותר שובע וחלבון; החלב פותר פשטות ושימוש יומיומי ישיר.",
    whatChanged: "במערכת החלבון: יותר רכיבים, יותר עיבוד, יותר תפקוד — פחות מינימליזם.",
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
