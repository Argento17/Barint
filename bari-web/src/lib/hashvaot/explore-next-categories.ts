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

/** Product-Agent-owned shelf taxonomy (D1). A category only surfaces candidates
 *  from its OWN shelf — never crosses supermarket ↔ supplements. */
export type ExploreNextShelf = "supermarket" | "supplements";

export interface ExploreNextCategory {
  id: string;
  /** Already-approved short Hebrew label. Source cited inline. */
  label: string;
  /** Self-hosted stock category image (public/hashvaot/themes/*.jpg) — same asset
   *  already used by the existing Featured*IntelligenceCard components. */
  image: string;
  /** Existing per-category accent color, copied from the matching Featured*Card. */
  accent: string;
  /** Product D1: shelf scope. Candidates are only ever drawn from the current
   *  page's own shelf (see getExploreNextCategories). */
  shelf: ExploreNextShelf;
  /** Product D2: optional family tag for the de-dup cap (max 1 card per family
   *  per render). Untagged categories are never capped against each other. */
  family?: string;
}

export const EXPLORE_NEXT_CATEGORIES: ExploreNextCategory[] = [
  // label source: src/lib/comparisons/registry/categories/bread.ts (nameHe)
  { id: "bread", label: "לחם ומאפים", image: "/hashvaot/themes/bread.jpg", accent: "#B0823C", shelf: "supermarket" },
  // label source: src/lib/comparisons/registry/categories/breakfast-cereals.ts (nameHe)
  { id: "breakfast-cereals", label: "דגני בוקר", image: "/hashvaot/themes/breakfast-cereals.jpg", accent: "#7A8C5E", shelf: "supermarket" },
  // label source: src/lib/comparisons/brined-cheeses-page-data.ts (hero.eyebrow)
  { id: "brined-cheeses", label: "גבינות מלוחות", image: "/hashvaot/themes/brined-cheeses.jpg", accent: "#7FA8B8", shelf: "supermarket", family: "cheese" },
  // label source: src/app/hashvaot/cakes/page.tsx metadata.title ("השוואת עוגות | Bari"),
  // universal " | Bari" suffix + "השוואת " prefix stripped (site-wide template, not content)
  { id: "cakes", label: "עוגות", image: "/hashvaot/themes/cakes-hard-cookies.jpg", accent: "#C4975A", shelf: "supermarket" },
  // label source: src/lib/comparisons/registry/categories/cheese.ts (nameHe)
  { id: "cheese", label: "גבינות", image: "/hashvaot/themes/cheese.jpg", accent: "#D8CBB0", shelf: "supermarket", family: "cheese" },
  // label source: src/lib/comparisons/chocolate-bars-comparison-page-data.ts (hero.eyebrow)
  { id: "chocolate-bars", label: "חטיפי שוקולד", image: "/hashvaot/themes/chocolate-bars.jpg", accent: "#3D2314", shelf: "supermarket" },
  // label source: src/lib/comparisons/chocolate-tablets-comparison-page-data.ts (hero.eyebrow)
  { id: "chocolate-tablets", label: "טבלאות שוקולד", image: "/hashvaot/themes/chocolate-tablets.jpg", accent: "#5C3D2E", shelf: "supermarket" },
  // label source: src/lib/comparisons/cookies-coffee-page-data.ts (hero.eyebrow)
  { id: "cookies-coffee", label: "עוגיות לקפה", image: "/hashvaot/themes/cookies-coffee.jpg", accent: "#C4975A", shelf: "supermarket" },
  // label source: src/lib/comparisons/registry/categories/crackers.ts (nameHe)
  { id: "crackers", label: "קרקרים", image: "/hashvaot/themes/crackers.jpg", accent: "#BF8F4A", shelf: "supermarket" },
  // label source: src/lib/comparisons/registry/categories/granola.ts (nameHe)
  { id: "granola", label: "גרנולה ומוזלי", image: "/hashvaot/themes/granola.jpg", accent: "#7A8C5E", shelf: "supermarket" },
  // label source: src/lib/comparisons/hard-cheeses-page-data.ts (hero.eyebrow)
  { id: "hard-cheeses", label: "גבינות קשות וצהובות", image: "/hashvaot/themes/hard-cheeses.jpg", accent: "#C9A96E", shelf: "supermarket", family: "cheese" },
  // label source: src/lib/comparisons/registry/categories/hummus.ts (nameHe)
  { id: "hummus", label: "חומוס וממרחים", image: "/hashvaot/themes/hummus.jpg", accent: "#BF9540", shelf: "supermarket" },
  // label source: src/lib/comparisons/juices-page-data.ts (hero.eyebrow)
  { id: "juices", label: "מיצים ומשקאות פירות", image: "/hashvaot/themes/juices.jpg", accent: "#E8A020", shelf: "supermarket" },
  // label source: src/lib/comparisons/magnesium-page-data.ts (hero.eyebrow)
  { id: "magnesium", label: "תוספי מגנזיום", image: "/hashvaot/themes/magnesium.jpg", accent: "#4A7B8C", shelf: "supplements" },
  // label source: src/data/site-content/comparison-pages.json ("milk".hero.eyebrow)
  { id: "milk-comparison", label: "חלב ותחליפים", image: "/hashvaot/themes/milk.jpg", accent: "#5C7FB0", shelf: "supermarket" },
  // label source: src/lib/comparisons/protein-bars-comparison-page-data.ts (hero.eyebrow)
  { id: "protein-bars", label: "חטיפי חלבון ועוגיות חלבון", image: "/hashvaot/themes/protein-bars.jpg", accent: "#3A6B50", shelf: "supermarket" },
  // label source: src/lib/comparisons/snacks-comparison-page-data.ts (hero.eyebrow).
  // NOTE: the typed registry's snacks.ts nameHe ("חטיפים מלוחים" / salty snacks) is STALE —
  // the live /hashvaot/snacks page and its own FeaturedSnacksIntelligenceCard both use
  // "חטיפי דגנים" (cereal/grain bars, post TASK-228 rebuild). Using the correct, currently
  // live label here; flagging the registry drift separately (not fixed in this task).
  { id: "snacks", label: "חטיפי דגנים", image: "/hashvaot/themes/snacks.jpg", accent: "#BC6A33", shelf: "supermarket" },
];

/** Default shelf for pages whose category id isn't in the manifest (e.g. creatine,
 *  still gated behind its own content sign-off) or has no category context at all
 *  (e.g. the blog feasibility demo). Matches every entry except magnesium today. */
const DEFAULT_SHELF: ExploreNextShelf = "supermarket";

/**
 * Returns up to `count` categories other than `currentCategoryId`, in a stable
 * deterministic order (no randomness — same page always shows the same set, easy to
 * screenshot-diff and QA). Order starts right after the current category's position in
 * the manifest and wraps around, so different leaf pages surface different neighbors
 * instead of all pointing at the same fixed leading N.
 *
 * Product D1 (shelf scoping): candidates are drawn ONLY from the current category's own
 * shelf. If the current category isn't in the manifest (e.g. creatine, still gated behind
 * its own content sign-off) or there is no category context (e.g. the blog demo),
 * DEFAULT_SHELF ("supermarket") is used. Edge case: if the same-shelf pool is empty once
 * the current category is excluded — magnesium is the only "supplements" entry today —
 * this returns [] and the module renders nothing. It must NEVER fall back to a different
 * shelf's pool.
 *
 * Product D2 (family de-dup): at most one card per `family` tag (e.g. "cheese" covers
 * cheese / brined-cheeses / hard-cheeses) is included per render. A family-duplicate is
 * skipped and backfilled from the next candidate in rotation order — no relevance graph,
 * just a linear skip-and-continue over the same deterministic ordering.
 *
 * Data-driven: adding a category to EXPLORE_NEXT_CATEGORIES makes it eligible to appear
 * (and to receive incoming links) on every other same-shelf page automatically.
 */
export function getExploreNextCategories(
  currentCategoryId: string | null | undefined,
  count = 4
): ExploreNextCategory[] {
  const current = EXPLORE_NEXT_CATEGORIES.find((c) => c.id === currentCategoryId);
  const shelf: ExploreNextShelf = current?.shelf ?? DEFAULT_SHELF;
  const startIndex = EXPLORE_NEXT_CATEGORIES.findIndex((c) => c.id === currentCategoryId);

  // Rotate the FULL manifest so the "neighborhood" ordering is stable and independent of
  // shelf composition, then filter to (a) the current page's own shelf and (b) not itself.
  const rotated =
    startIndex === -1
      ? EXPLORE_NEXT_CATEGORIES
      : [
          ...EXPLORE_NEXT_CATEGORIES.slice(startIndex + 1),
          ...EXPLORE_NEXT_CATEGORIES.slice(0, startIndex),
        ];

  const sameShelfPool = rotated.filter(
    (c) => c.id !== currentCategoryId && c.shelf === shelf
  );

  const result: ExploreNextCategory[] = [];
  const usedFamilies = new Set<string>();
  for (const candidate of sameShelfPool) {
    if (result.length >= count) break;
    if (candidate.family && usedFamilies.has(candidate.family)) {
      continue; // family cap hit — skip and backfill from the next candidate
    }
    result.push(candidate);
    if (candidate.family) usedFamilies.add(candidate.family);
  }
  return result;
}
