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
 * Priorities: home 1.0 · hub 0.9 · comparison pages 0.8 · blog 0.7 ·
 * methodology 0.6 · legal pages 0.3.
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

// Blog routes — only the curated, launch-ready articles are indexed. The
// bread/hummus/yogurt/lechem articles + the bread-analysis redirect are
// de-listed (and marked noindex on the page) per owner ruling 2026-06-26.
const BLOG_PATHS = [
  "/blog/milk-analysis",
  "/blog/shemen-zayit",
  "/blog/sugar-alcohols",
] as const;

// Methodology + legal pages (now public/approved).
const LEGAL_PATHS = [
  "/methodology",
  "/nagisut",
  "/privacy",
  "/terms",
  "/cookies",
  "/disclaimer",
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
    ...LEGAL_PATHS.map((p) => entry(p, p === "/methodology" ? 0.6 : 0.3)),
  ];
}
