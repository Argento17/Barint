import rawData from "@/data/bread-comparison.json";
import type { BreadArchetype, BreadComparisonPage, BreadFilterId, BreadGrade, BreadProduct } from "./bread-types";

export const breadComparisonPage = rawData as BreadComparisonPage;
export const breadProducts: BreadProduct[] = breadComparisonPage.products;

export const BREAD_GRADE_COLORS: Record<BreadGrade, { bg: string; text: string; border: string }> = {
  A: { bg: "#2E7D32", text: "#FFFFFF", border: "#2E7D3215" },
  B: { bg: "#558B2F", text: "#FFFFFF", border: "#558B2F15" },
  C: { bg: "#F9A825", text: "#111318", border: "#F9A82520" },
  D: { bg: "#EF6C00", text: "#FFFFFF", border: "#EF6C0020" },
  E: { bg: "#C62828", text: "#FFFFFF", border: "#C6282820" },
};

export const ARCHETYPE_META: Record<
  BreadArchetype,
  { label: string; labelShort: string; color: string; bgClass: string; textClass: string; borderClass: string }
> = {
  sourdough_traditional: {
    label: "מחמצת מסורתית",
    labelShort: "מחמצת",
    color: "#92400E",
    bgClass: "bg-amber-50",
    textClass: "text-amber-800",
    borderClass: "border-amber-200",
  },
  nordic_whole_grain: {
    label: "קריספ נורדי / דגן שלם",
    labelShort: "דגן שלם",
    color: "#1F8F6A",
    bgClass: "bg-emerald-50",
    textClass: "text-emerald-800",
    borderClass: "border-emerald-200",
  },
  seeds_multigrain: {
    label: "גרעינים ורב-דגן",
    labelShort: "גרעינים",
    color: "#854D0E",
    bgClass: "bg-yellow-50",
    textClass: "text-yellow-800",
    borderClass: "border-yellow-200",
  },
  sourdough_theater: {
    label: "מחמצת כטעם",
    labelShort: "מחמצת-תיאטרלי",
    color: "#9A3412",
    bgClass: "bg-orange-50",
    textClass: "text-orange-800",
    borderClass: "border-orange-200",
  },
  fiber_inflation: {
    label: "ניפוח סיבים",
    labelShort: "ניפוח סיבים",
    color: "#9F1239",
    bgClass: "bg-rose-50",
    textClass: "text-rose-800",
    borderClass: "border-rose-200",
  },
  engineered_functional: {
    label: "הנדסה פונקציונלית",
    labelShort: "פונקציונלי",
    color: "#3730A3",
    bgClass: "bg-indigo-50",
    textClass: "text-indigo-800",
    borderClass: "border-indigo-200",
  },
  simple_white: {
    label: "בסיס לבן / תעשייתי",
    labelShort: "לבן / תעשייתי",
    color: "#374151",
    bgClass: "bg-slate-50",
    textClass: "text-slate-700",
    borderClass: "border-slate-200",
  },
  treat_salty: {
    label: "פינוק / מלוח",
    labelShort: "פינוק",
    color: "#6B3B2E",
    bgClass: "bg-stone-50",
    textClass: "text-stone-700",
    borderClass: "border-stone-200",
  },
};

export const BREAD_FILTERS: { id: BreadFilterId; label: string }[] = [
  { id: "all", label: "הכל" },
  { id: "sourdough_traditional", label: "מחמצת מסורתית" },
  { id: "nordic_whole_grain", label: "דגן שלם" },
  { id: "seeds_multigrain", label: "גרעינים" },
  { id: "sourdough_theater", label: "מחמצת-תיאטרלי" },
  { id: "fiber_inflation", label: "ניפוח סיבים" },
  { id: "engineered_functional", label: "פונקציונלי" },
  { id: "simple_white", label: "לבן / תעשייתי" },
  { id: "grade_a", label: "ציון A" },
  { id: "has_fermentation", label: "תסיסה" },
  { id: "isolated_fiber", label: "סיב מופרד" },
];

export const breadComparisonFilters: {
  id: BreadFilterId;
  label: string;
  group: "archetype" | "trait";
}[] = [
  { id: "sourdough_traditional", label: "מחמצת מסורתית", group: "archetype" },
  { id: "nordic_whole_grain", label: "דגן שלם", group: "archetype" },
  { id: "seeds_multigrain", label: "גרעינים", group: "archetype" },
  { id: "sourdough_theater", label: "מחמצת כתוסף", group: "archetype" },
  { id: "engineered_functional", label: "פונקציונלי", group: "archetype" },
  { id: "grade_a", label: "ציון A", group: "trait" },
  { id: "has_fermentation", label: "תסיסה", group: "trait" },
  { id: "isolated_fiber", label: "סיב מופרד", group: "trait" },
];

const BREAD_ARCHETYPE_FILTERS = new Set<BreadFilterId>([
  "sourdough_traditional",
  "nordic_whole_grain",
  "seeds_multigrain",
  "sourdough_theater",
  "fiber_inflation",
  "engineered_functional",
  "simple_white",
  "treat_salty",
]);

export function filterBreadProducts(products: BreadProduct[], filterId: BreadFilterId): BreadProduct[] {
  switch (filterId) {
    case "all":
      return products;
    case "grade_a":
      return products.filter((p) => p.grade === "A");
    case "grade_b_plus":
      return products.filter((p) => p.grade === "A" || p.grade === "B");
    case "has_fermentation":
      return products.filter((p) => p.ferm_q === "traditional" || p.ferm_q === "mixed");
    case "isolated_fiber":
      return products.filter((p) => p.fiber_q === "isolated");
    default:
      return products.filter((p) => p.archetype === filterId);
  }
}

export function sortBreadProducts(
  products: BreadProduct[],
  by: "score" | "fiber" | "protein" | "delta"
): BreadProduct[] {
  return [...products].sort((a, b) => {
    switch (by) {
      case "score":
        return b.score - a.score;
      case "fiber":
        return b.nutrition.fiber_g - a.nutrition.fiber_g;
      case "protein":
        return b.nutrition.protein_g - a.nutrition.protein_g;
      case "delta":
        return b.delta - a.delta;
    }
  });
}

export function getProductById(id: string): BreadProduct | undefined {
  return breadProducts.find((p) => p.id === id);
}

export function breadMatchesFilters(product: BreadProduct, active: Set<BreadFilterId>): boolean {
  if (active.size === 0) return true;

  const archetypeFilters = [...active].filter((filterId) => BREAD_ARCHETYPE_FILTERS.has(filterId));
  const traitFilters = [...active].filter((filterId) => !BREAD_ARCHETYPE_FILTERS.has(filterId));

  if (archetypeFilters.length > 0) {
    const archetypeMatch = archetypeFilters.some((filterId) => product.archetype === filterId);
    if (!archetypeMatch) return false;
  }

  for (const trait of traitFilters) {
    if (filterBreadProducts([product], trait).length === 0) return false;
  }

  return true;
}

export function getBreadRowEmphasis(
  product: BreadProduct,
  active: Set<BreadFilterId>
): "emphasized" | "muted" | "neutral" {
  if (active.size === 0) return "neutral";
  return breadMatchesFilters(product, active) ? "emphasized" : "muted";
}

export function breadCountVisible(active: Set<BreadFilterId>): number {
  return breadProducts.filter((product) => breadMatchesFilters(product, active)).length;
}

export function getBreadFlagshipProducts(): BreadProduct[] {
  return [
    "9990001000018",
    "9990001000017",
    "9990001000013",
    "9990001000003",
    "9990001000010",
    "9990001000016",
  ]
    .map((id) => getProductById(id))
    .filter((product): product is BreadProduct => Boolean(product));
}
