import type { MetadataRoute } from "next";

import { absoluteUrl } from "@/lib/site-url";

/**
 * SEO baseline sitemap (DEC-003 market-facing readiness: comparison pages
 * publicly available + indexable). Lists stable, indexable public routes only.
 * Platform-only — no scoring, corpus, or product-order impact.
 *
 * Routes are listed explicitly (matching the live `app/hashvaot/*` and
 * `app/blog/*` route folders) rather than derived, so a route appears here only
 * once its page is actually reachable. Verified against the on-disk page.tsx set.
 *
 * Excluded by design: /nagisut, /privacy, /terms — these legal shells still hold
 * un-approved placeholder copy and are noindexed, so they must NOT be in the sitemap.
 *
 * Priorities: home 1.0 · hub 0.9 · comparison pages 0.8 · blog 0.7.
 */

const HOME_PATHS = ["/"] as const;
const HUB_PATHS = ["/hashvaot", "/blog"] as const;

// Comparison routes — one per live `app/hashvaot/<slug>/page.tsx` folder.
const COMPARISON_PATHS = [
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
  "/hashvaot/supplements",
] as const;

// Blog routes — one per live `app/blog/<slug>/page.tsx` folder.
const BLOG_PATHS = [
  "/blog/bread-analysis",
  "/blog/bread-everyday",
  "/blog/bread-standouts",
  "/blog/bread-wellness-gap",
  "/blog/hummus",
  "/blog/lechem",
  "/blog/milk-analysis",
  "/blog/shemen-zayit",
  "/blog/sugar-alcohols",
  "/blog/yogurt",
] as const;

export default function sitemap(): MetadataRoute.Sitemap {
  const lastModified = new Date();

  const entry = (path: string, priority: number): MetadataRoute.Sitemap[number] => ({
    url: absoluteUrl(path),
    lastModified,
    changeFrequency: "weekly",
    priority,
  });

  return [
    ...HOME_PATHS.map((p) => entry(p, 1)),
    ...HUB_PATHS.map((p) => entry(p, 0.9)),
    ...COMPARISON_PATHS.map((p) => entry(p, 0.8)),
    ...BLOG_PATHS.map((p) => entry(p, 0.7)),
  ];
}
