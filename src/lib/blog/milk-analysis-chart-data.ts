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
  /** 0 = פחות עיבוד, 100 = יותר עיבוד */
  processingIntensity: number;
  /** grams protein per 100ml */
  proteinLevel: number;
  ingredientCount: number;
  label: string;
  shortLabel: string;
  placementInsight: string;
};

export type ScatterEditorialNote = {
  id: string;
  title: string;
  text: string;
  productTypes: ProductType[];
  representativeBarcodes: string[];
};

export const SCATTER_EDITORIAL_NOTES: ScatterEditorialNote[] = [
  {
    id: "dairy",
    title: "חלב פרה — בסיס ישיר",
    text: "נשאר באזור פחות מעובד, עם חלבון יציב יחסית לקטגוריה. פשוט מבנית — לא בהכרח הכי עשיר בכל מדד.",
    productTypes: ["dairy"],
    representativeBarcodes: ["7290000051352", "7290019790259"],
  },
  {
    id: "oat",
    title: "שיבולת שועל — מרקם כמוצר",
    text: "גרסאות הבריסטה נודדות ימינה: יותר עיבוד כדי לייצר הקצפה ומרקם, לאו דווקא כדי לספק יותר חלבון.",
    productTypes: ["oat"],
    representativeBarcodes: ["7394376621451", "7394376620904", "7394376619939"],
  },
  {
    id: "soy",
    title: "סויה — פיצול בתוך קטגוריה",
    text: "נוטה לטפס גבוה יותר בציר החלבון, אך הפער בין גרסה בסיסית למועשרת נשאר מורגש גם בעיבוד.",
    productTypes: ["soy"],
    representativeBarcodes: ["7290116936116", "7290110324926"],
  },
];

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
    return "קל בקלוריות, חלבון זניח — משקה, לא מקור חלבון.";
  }
  if (complex && hasAdditives) {
    return "יותר מייצבים והעשרה ברשימה — מיקום המוצר משקף עומק פורמולציה.";
  }
  if (simple && protein >= 2) {
    return "מבנה ישיר יחסית, עם חלבון סביר לקטגוריה.";
  }

  return "מיקום לפי איזון בין אורך רשימת רכיבים, עיבוד ופרופיל תזונתי בקטגוריה.";
}

function highProteinInsight(protein: number): boolean {
  return protein >= 2.8;
}

/** Higher = less processing (פחות עיבוד at top) */
export function lessProcessingScore(product: MilkComparisonProduct): number {
  return dimScore(product, "processing_quality");
}

/** Higher = more processing (יותר עיבוד at right) */
export function processingIntensityScore(product: MilkComparisonProduct): number {
  return 100 - lessProcessingScore(product);
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
    processingIntensity: processingIntensityScore(product),
    proteinLevel: product.proteinPer100ml ?? 0,
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
    barcodes: ["7394376621451", "7394376620904"],
  },
  {
    id: "protein",
    label: "חלבון מועשר",
    barcodes: ["7290114313865", "7290000051352"],
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
    subtitle: "אותה משפחה — שני מסלולי פורמולציה.",
    leftBarcode: "7290116936116",
    rightBarcode: "7290110324926",
    story:
      "משמאל: סויה ללא סוכר, בלי תוספים מזוהים — רשימה קצרה יחסית. מימין: אותו בסיס סויה, עם סידן, ויטמינים ומווסתי חומציות. הציון מודד עומק הרכבה, לא כוונה.",
    divergence:
      "הפער הוא במספר השכבות — לא בגרם חלבון בודד. מי שמחפש מינימום רכיבים בוחר אחרת ממי שמחפש העשרה מלאה.",
    formulationNote:
      "בגרסה המועשרת: יותר מינרלים וויטמינים, יותר רכיבי ייצוב. בבסיסית: פחות תוספים, פחות «בנייה מחדש».",
    whatChanged:
      "מעבר מימין לשמאל: מורידים העשרה ומווסתים — ומקבלים רשימה קצרה יותר.",
  },
  {
    id: "oat-barista-vs-lighter",
    title: "שיבולת בריסטה מול שיבולת ללא סוכר",
    subtitle: "שתי גרסאות שיבולת — שאלות שימוש שונות.",
    leftBarcode: "7394376621451",
    rightBarcode: "7394376620904",
    story:
      "משמאל: אוטלי בריסטה להקצפה — שמן קנולה, מווסתים, מינרלים. מימין: שיבולת ללא סוכר — פחות ממוקדת בקצף, פחות שכבות ביצוע. שתיהן שיבולת; לא אותה מטרה.",
    divergence:
      "בריסטה נבנתה לכוס קפה; הגרסה ללא סוכר נוטה לשימוש יומיומי פשוט יותר. Bari לא בוחר «מנצח» — מודד כמה שכבות כל גרסה דרשה.",
    formulationNote:
      "בבריסטה: שמן ומווסתים תומכים במרקם והקצפה. בללא סוכר: פחות דגש על ביצוע, יותר פרופיל «נייטרלי».",
    whatChanged:
      "כשעוברים מבריסטה לגרסה קלה — מורידים חלק משכבות המרקם, לא רק סוכר.",
  },
  {
    id: "dairy-vs-protein-system",
    title: "חלב מלא מול חלב מועשר בחלבון",
    subtitle: "שני מוצרי חלב פרה — מטרות שונות.",
    leftBarcode: "7290000051352",
    rightBarcode: "7290114313865",
    story:
      "משמאל: חלב מלא — חלב בלבד, ציון גבוה, מבנה ישיר. מימין: חלב נטול לקטוז עם כ־6.5 גרם חלבון ל־100 מ״ל — תהליך עשיר יותר, רשימה ארוכה יותר.",
    divergence:
      "החלבון הגבוה במוצר מימין מגיע מסינון והעשרה — לא מאותה פשטות כמו חלב בסיסי. השאלה: חלב יומיומי או מקור חלבון מרוכז.",
    formulationNote:
      "במועשר: יותר חלבון, יותר עומק ייצור. במלא: פחות שכבות, פחות פונקציונליות ממוקדת.",
    whatChanged:
      "מעבר לחלב מועשר: יותר חלבון בכוס, פחות «פריט אחד ברשימה».",
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
    barcode: "7394376621451",
  },
  {
    id: "protein",
    title: "חלב מועשר בחלבון",
    subtitle: "חלבון גבוה בתוך משפחת החלב",
    insight: "יותר חלבון בכוס — עם תהליך ייצור עמוק יותר מחלב בסיסי.",
    barcode: "7290114313865",
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
