/**
 * Strict schema for homepage carousel cards.
 * Single source of truth — import types from here, never from the data file.
 */

export const CAROUSEL_PRODUCT_FALLBACK = "/home/carousel-product-fallback.svg";

// ── Card type & visual mode ──────────────────────────────────────────────────

export type CardType =
  | "comparison"
  | "category_report"
  | "ingredient_investigation"
  | "supplement_report"
  | "methodology"
  | "product_spotlight";

export type VisualMode =
  | "product_duel"
  | "product_single"
  | "score_spread"
  | "ingredient_tokens"
  | "supplement_molecule";

// ── Product reference (used in comparison + spotlight) ───────────────────────

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

// ── Score spread (category_report only) ─────────────────────────────────────

export type ScoreSpread = {
  low: number;
  high: number;
  count: number;
  label: string;
};

// ── Unified card shape ───────────────────────────────────────────────────────

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
  // comparison + spotlight
  leftProduct?: ProductRef;
  rightProduct?: ProductRef;
  spotlightProduct?: ProductRef;
  // category_report
  scoreSpread?: ScoreSpread;
  // ingredient_investigation
  ingredientTokens?: string[];
  // supplement_report
  supplementStat?: { value: string; label: string };
};
