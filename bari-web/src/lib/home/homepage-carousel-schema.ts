/**
 * Strict schema for homepage carousel cards.
 * Single source of truth — import types from here, never from the data file.
 */

export const CAROUSEL_PRODUCT_FALLBACK = "/home/carousel-product-fallback.svg";

export type CardType =
  | "comparison"
  | "category_report"
  | "ingredient_investigation"
  | "supplement_report"
  | "methodology"
  | "product_spotlight";

export type GradeLetter = "A" | "B" | "C" | "D" | "E";

export type GradeDistribution = {
  count: number;
  label: string;
  low: number;
  high: number;
  spread: number;
  grades: Record<GradeLetter, number>;
  gradeOrder: GradeLetter[];
};

export type CategoryChartVariant = "grade_histogram" | "grade_skew" | "grade_stacked";

export type VisualMode =
  | "product_duel"
  | "product_single"
  | "grade_histogram"
  | "grade_skew"
  | "grade_stacked"
  | "ingredient_mask"
  | "supplement_molecule";

export type ProductRef = {
  productId: string;
  barcode?: string;
  name: string;
  brand: string;
  score: number;
  imageUrl?: string;
  imageAlt: string;
  imageStatus: "verified" | "unverified" | "missing";
};

/** @deprecated use gradeDistribution */
export type ScoreSpread = {
  low: number;
  high: number;
  count: number;
  label: string;
};

export type CarouselCard = {
  id: string;
  type: CardType;
  visualMode: VisualMode;
  title: string;
  eyebrow: string;
  category: string;
  evidence: string;
  metric?: string;
  href: string;
  accent: string;
  fallbackVisual?: string;
  leftProduct?: ProductRef;
  rightProduct?: ProductRef;
  spotlightProduct?: ProductRef;
  gradeDistribution?: GradeDistribution;
  chartVariant?: CategoryChartVariant;
  scoreSpread?: ScoreSpread;
  ingredientTokens?: string[];
  ingredientSpotlightProductId?: string;
  ingredientMaskCount?: number;
  supplementStat?: { value: string; label: string };
};