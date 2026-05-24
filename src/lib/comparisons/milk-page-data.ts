import rawPage from "@/data/milk-comparison.json";

import type {
  ComparisonFilterId,
  MilkComparisonPageData,
  MilkComparisonProduct,
} from "@/lib/comparisons/milk-types";

export const milkComparisonPage = rawPage as MilkComparisonPageData;

export const milkProducts: MilkComparisonProduct[] = milkComparisonPage.products;

export const GRADE_COLORS: Record<
  string,
  { bg: string; text: string; border: string }
> = {
  A: { bg: "#2E7D32", text: "#FFFFFF", border: "#2E7D3215" },
  B: { bg: "#558B2F", text: "#FFFFFF", border: "#558B2F15" },
  C: { bg: "#F9A825", text: "#111318", border: "#F9A82520" },
  D: { bg: "#EF6C00", text: "#FFFFFF", border: "#EF6C0020" },
  E: { bg: "#C62828", text: "#FFFFFF", border: "#C6282820" },
};

export const DEGRADATION_LABELS: Record<string, string> = {
  minimal: "פירוק מבני מינימלי",
  low: "פירוק מבני נמוך",
  moderate: "פירוק מבני בינוני",
  high: "פירוק מבני גבוה",
  severe: "פירוק מבני חמור",
  extreme: "פירוק מבני קיצוני",
};

export const PRIMARY_DIMENSION_KEYS = [
  "processing_quality",
  "nutrient_density",
  "protein_quality",
  "additive_quality",
  "fat_quality",
  "glycemic_quality",
  "whole_food_integrity",
] as const;

export const comparisonFilters: {
  id: ComparisonFilterId;
  label: string;
  group: "type" | "trait";
}[] = [
  { id: "type:dairy", label: "חלב פרה", group: "type" },
  { id: "type:oat", label: "שיבולת שועל", group: "type" },
  { id: "type:soy", label: "סויה", group: "type" },
  { id: "type:almond", label: "שקדים", group: "type" },
  { id: "type:rice", label: "אורז", group: "type" },
  { id: "no_additives", label: "ללא תוספים", group: "trait" },
  { id: "high_protein", label: "חלבון גבוה", group: "trait" },
  { id: "low_sugar", label: "פחות סוכר", group: "trait" },
  { id: "coffee", label: "הכי מתאים לקפה", group: "trait" },
  { id: "high_score", label: "ציון Bari הגבוה", group: "trait" },
];

export const howToReadComparison = [
  "הציון משקף מבנה, רכיבים, תרומה תזונתית והקשר קטגוריאלי — בהשוואה למוצרים דומים.",
  "חלבון גבוה משרת מטרה אחת; פשטות רכיבים משרתת אחרת. בחרו לפי השימוש שלכם.",
  "למה קיבל את הציון? מפרק תרומה, טריידאופים והשוואה לעמיתים באותה משפחה.",
  "פירוט לפי היבטים זמין למי שרוצה עומק — אפשר להבין את העיקר גם בלי להיכנס לשם.",
] as const;

export function formatNutrient(value: number | null, unit = " ג׳"): string {
  if (value == null) return "לא מוצהר";
  const rounded = Math.round(value * 10) / 10;
  return `${Number.isInteger(rounded) ? rounded : rounded.toFixed(1)}${unit}`;
}

export function productMatchesFilters(
  product: MilkComparisonProduct,
  active: Set<ComparisonFilterId>
): boolean {
  if (active.size === 0) return true;

  const typeFilters = [...active].filter((f) => f.startsWith("type:"));
  const traitFilters = [...active].filter((f) => !f.startsWith("type:"));

  if (typeFilters.length > 0) {
    const typeMatch = typeFilters.some((f) => product.filterTags.includes(f));
    if (!typeMatch) return false;
  }

  for (const trait of traitFilters) {
    if (!product.filterTags.includes(trait)) return false;
  }

  return true;
}

export function getRowEmphasis(
  product: MilkComparisonProduct,
  active: Set<ComparisonFilterId>
): "emphasized" | "muted" | "neutral" {
  if (active.size === 0) return "neutral";
  return productMatchesFilters(product, active) ? "emphasized" : "muted";
}

export function countVisible(active: Set<ComparisonFilterId>): number {
  return milkProducts.filter((p) => productMatchesFilters(p, active)).length;
}
