import type { MetadataRoute } from "next";

import { absoluteUrl } from "@/lib/site-url";

/**
 * SEO baseline sitemap (DEC-003 market-facing readiness: comparison pages
 * publicly available + indexable). Lists stable, indexable public routes only.
 * Platform-only — no scoring, corpus, or product-order impact.
 *
 * Comparison routes are listed explicitly (matching the live `app/hashvaot/*`
 * route folders) rather than derived, so a route appears here only once its
 * page is actually reachable.
 */
const STATIC_PATHS = [
  "/",
  "/hashvaot",
  "/hashvaot/bread",
  "/hashvaot/breakfast-cereals",
  "/hashvaot/brined-cheeses",
  "/hashvaot/cakes",
  "/hashvaot/cheese",
  "/hashvaot/chocolate-bars",
  "/hashvaot/chocolate-tablets",
  "/hashvaot/cookies-coffee",
  "/hashvaot/granola",
  "/hashvaot/hard-cheeses",
  "/hashvaot/hummus",
  "/hashvaot/juices",
  "/hashvaot/magnesium",
  "/hashvaot/milk-comparison",
  "/hashvaot/protein-bars",
  "/hashvaot/snacks",
  "/hashvaot/supermarket",
  "/hashvaot/supplements",
  "/blog",
] as const;

export default function sitemap(): MetadataRoute.Sitemap {
  const lastModified = new Date();

  return STATIC_PATHS.map((path) => ({
    url: absoluteUrl(path),
    lastModified,
    changeFrequency: "weekly",
    priority: path === "/" ? 1 : path.startsWith("/hashvaot") ? 0.8 : 0.6,
  }));
}
