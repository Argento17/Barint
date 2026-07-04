/**
 * Explore-Next category directory (TASK-507).
 *
 * Drives the "עוד השוואות" (More comparisons) module rendered at the bottom of every
 * leaf comparison page. This is a read-only cross-link directory, separate from the
 * typed `comparisonCategoryRegistry` (src/lib/comparisons/registry) — that registry
 * only covers 7 of the 17 live leaf categories (it exists to drive page-data/gates,
 * not navigation) and could not be reused as-is without extending it to carry
 * getPageData/getCorpusPayload wiring for the other 10, which was out of scope for a
 * navigation-only task. See TASK-507 return notes for the full finding.
 *
 * Every `label` below is an ALREADY-SHIPPED, already-approved Hebrew string copied
 * verbatim from a live source (cited per entry) — no new category copy was authored.
 * The `id` is the literal route segment under /hashvaot/<id>.
 */

export interface ExploreNextCategory {
  id: string;
  /** Already-approved short Hebrew label. Source cited inline. */
  label: string;
  /** Self-hosted stock category image (public/hashvaot/themes/*.jpg) — same asset
   *  already used by the existing Featured*IntelligenceCard components. */
  image: string;
  /** Existing per-category accent color, copied from the matching Featured*Card. */
  accent: string;
}

export const EXPLORE_NEXT_CATEGORIES: ExploreNextCategory[] = [
  // label source: src/lib/comparisons/registry/categories/bread.ts (nameHe)
  { id: "bread", label: "לחם ומאפים", image: "/hashvaot/themes/bread.jpg", accent: "#B0823C" },
  // label source: src/lib/comparisons/registry/categories/breakfast-cereals.ts (nameHe)
  { id: "breakfast-cereals", label: "דגני בוקר", image: "/hashvaot/themes/breakfast-cereals.jpg", accent: "#7A8C5E" },
  // label source: src/lib/comparisons/brined-cheeses-page-data.ts (hero.eyebrow)
  { id: "brined-cheeses", label: "גבינות מלוחות", image: "/hashvaot/themes/brined-cheeses.jpg", accent: "#7FA8B8" },
  // label source: src/app/hashvaot/cakes/page.tsx metadata.title ("השוואת עוגות | Bari"),
  // universal " | Bari" suffix + "השוואת " prefix stripped (site-wide template, not content)
  { id: "cakes", label: "עוגות", image: "/hashvaot/themes/cakes-hard-cookies.jpg", accent: "#C4975A" },
  // label source: src/lib/comparisons/registry/categories/cheese.ts (nameHe)
  { id: "cheese", label: "גבינות", image: "/hashvaot/themes/cheese.jpg", accent: "#D8CBB0" },
  // label source: src/lib/comparisons/chocolate-bars-comparison-page-data.ts (hero.eyebrow)
  { id: "chocolate-bars", label: "חטיפי שוקולד", image: "/hashvaot/themes/chocolate-bars.jpg", accent: "#3D2314" },
  // label source: src/lib/comparisons/chocolate-tablets-comparison-page-data.ts (hero.eyebrow)
  { id: "chocolate-tablets", label: "טבלאות שוקולד", image: "/hashvaot/themes/chocolate-tablets.jpg", accent: "#5C3D2E" },
  // label source: src/lib/comparisons/cookies-coffee-page-data.ts (hero.eyebrow)
  { id: "cookies-coffee", label: "עוגיות לקפה", image: "/hashvaot/themes/cookies-coffee.jpg", accent: "#C4975A" },
  // label source: src/lib/comparisons/registry/categories/crackers.ts (nameHe)
  { id: "crackers", label: "קרקרים", image: "/hashvaot/themes/crackers.jpg", accent: "#BF8F4A" },
  // label source: src/lib/comparisons/registry/categories/granola.ts (nameHe)
  { id: "granola", label: "גרנולה ומוזלי", image: "/hashvaot/themes/granola.jpg", accent: "#7A8C5E" },
  // label source: src/lib/comparisons/hard-cheeses-page-data.ts (hero.eyebrow)
  { id: "hard-cheeses", label: "גבינות קשות וצהובות", image: "/hashvaot/themes/hard-cheeses.jpg", accent: "#C9A96E" },
  // label source: src/lib/comparisons/registry/categories/hummus.ts (nameHe)
  { id: "hummus", label: "חומוס וממרחים", image: "/hashvaot/themes/hummus.jpg", accent: "#BF9540" },
  // label source: src/lib/comparisons/juices-page-data.ts (hero.eyebrow)
  { id: "juices", label: "מיצים ומשקאות פירות", image: "/hashvaot/themes/juices.jpg", accent: "#E8A020" },
  // label source: src/lib/comparisons/magnesium-page-data.ts (hero.eyebrow)
  { id: "magnesium", label: "תוספי מגנזיום", image: "/hashvaot/themes/magnesium.jpg", accent: "#4A7B8C" },
  // label source: src/data/site-content/comparison-pages.json ("milk".hero.eyebrow)
  { id: "milk-comparison", label: "חלב ותחליפים", image: "/hashvaot/themes/milk.jpg", accent: "#5C7FB0" },
  // label source: src/lib/comparisons/protein-bars-comparison-page-data.ts (hero.eyebrow)
  { id: "protein-bars", label: "חטיפי חלבון ועוגיות חלבון", image: "/hashvaot/themes/protein-bars.jpg", accent: "#3A6B50" },
  // label source: src/lib/comparisons/snacks-comparison-page-data.ts (hero.eyebrow).
  // NOTE: the typed registry's snacks.ts nameHe ("חטיפים מלוחים" / salty snacks) is STALE —
  // the live /hashvaot/snacks page and its own FeaturedSnacksIntelligenceCard both use
  // "חטיפי דגנים" (cereal/grain bars, post TASK-228 rebuild). Using the correct, currently
  // live label here; flagging the registry drift separately (not fixed in this task).
  { id: "snacks", label: "חטיפי דגנים", image: "/hashvaot/themes/snacks.jpg", accent: "#BC6A33" },
];

/**
 * Returns up to `count` categories other than `currentCategoryId`, in a stable
 * deterministic order (no randomness — same page always shows the same set, easy to
 * screenshot-diff and QA). Order starts right after the current category's position in
 * the manifest and wraps around, so different leaf pages surface different neighbors
 * instead of all pointing at the same fixed leading N.
 *
 * Data-driven: adding a category to EXPLORE_NEXT_CATEGORIES makes it eligible to appear
 * (and to receive incoming links) on every other page automatically.
 */
export function getExploreNextCategories(
  currentCategoryId: string | null | undefined,
  count = 4
): ExploreNextCategory[] {
  const others = EXPLORE_NEXT_CATEGORIES.filter((c) => c.id !== currentCategoryId);
  const startIndex = EXPLORE_NEXT_CATEGORIES.findIndex((c) => c.id === currentCategoryId);
  if (startIndex === -1) {
    return others.slice(0, count);
  }
  // Rotate `others` so the selection starts from the category right after `current`
  // in the full (unfiltered) list — keeps a stable per-category "neighborhood".
  const rotated = [
    ...EXPLORE_NEXT_CATEGORIES.slice(startIndex + 1),
    ...EXPLORE_NEXT_CATEGORIES.slice(0, startIndex),
  ].filter((c) => c.id !== currentCategoryId);
  return rotated.slice(0, count);
}
