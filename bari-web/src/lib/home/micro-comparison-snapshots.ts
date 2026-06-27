import type { CardVisual, HomepageCardWithVisual } from "./homepage-carousel-data";
import { HOMEPAGE_CAROUSEL_CARDS } from "./homepage-carousel-data";

export type { CardVisual };

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
  visual?: CardVisual;
};

export type EditorialArchetype =
  | "investigation"
  | "category-report"
  | "ingredient"
  | "methodology"
  | "what-surprised-us"
  | "product-spotlight";

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
  visual?: CardVisual;
};

export type HomepageCard = ComparisonCard | EditorialCard;

export function getHomepageCards(): HomepageCardWithVisual[] {
  return HOMEPAGE_CAROUSEL_CARDS;
}

export function getMicroComparisonSnapshots(): HomepageCardWithVisual[] {
  return getHomepageCards();
}
