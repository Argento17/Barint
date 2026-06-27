/**
 * Public surface for homepage carousel data.
 * Exports the CarouselCard type and the cards array.
 */

export type { CarouselCard } from "./homepage-carousel-schema";
export { CAROUSEL_PRODUCT_FALLBACK } from "./homepage-carousel-schema";
export { HOMEPAGE_CAROUSEL_CARDS } from "./homepage-carousel-data";

import { HOMEPAGE_CAROUSEL_CARDS } from "./homepage-carousel-data";

export function getHomepageCards() {
  return HOMEPAGE_CAROUSEL_CARDS;
}

export function getMicroComparisonSnapshots() {
  return HOMEPAGE_CAROUSEL_CARDS;
}
