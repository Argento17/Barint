/**
 * Canonical public origin for the Bari website.
 *
 * Used for `metadataBase` (absolute OG/canonical URLs), `robots.ts`, and
 * `sitemap.ts`. Override per-environment with `NEXT_PUBLIC_SITE_URL`
 * (e.g. a preview deployment); defaults to the established production host.
 *
 * Establishes the SEO baseline launch criterion (DEC-003 market-facing
 * readiness: comparison pages publicly available + indexable). Presentation /
 * platform only — no scoring, corpus, or product-order impact.
 */
export const SITE_URL = (
  process.env.NEXT_PUBLIC_SITE_URL ?? "https://bari.digital"
).replace(/\/+$/, "");

/** Build an absolute URL from a site-relative path (`/hashvaot/hummus`). */
export function absoluteUrl(path: string): string {
  return `${SITE_URL}${path.startsWith("/") ? path : `/${path}`}`;
}
