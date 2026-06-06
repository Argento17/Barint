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
  "/hashvaot/butter",
  "/hashvaot/hummus",
  "/hashvaot/maadanim",
  "/hashvaot/snacks",
  "/hashvaot/yogurts",
  "/hashvaot/bread",
  "/hashvaot/vegetable-spreads",
  "/hashvaot/milk-comparison",
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
