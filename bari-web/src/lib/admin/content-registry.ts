/**
 * Admin site-content registry (hub, homepage, page chrome slugs).
 */
import comparisonPages from "@/data/site-content/comparison-pages.json";

export const PAGE_CHROME_FILE = "comparison-pages.json";

export interface SiteContentEntry {
  id: string;
  file: string;
  labelHe: string;
}

export const SITE_CONTENT_ENTRIES: SiteContentEntry[] = [
  { id: "hashvaot-hub", file: "hashvaot-hub.json", labelHe: "\u05de\u05e8\u05db\u05d6 \u05d4\u05d4\u05e9\u05d5\u05d5\u05d0\u05d5\u05ea (Hub)" },
  { id: "hashvaot-categories", file: "hashvaot-categories.json", labelHe: "\u05e7\u05d8\u05d2\u05d5\u05e8\u05d9\u05d5\u05ea \u05d4\u05d4\u05e9\u05d5\u05d5\u05d0\u05d5\u05ea" },
  { id: "homepage-marketing", file: "homepage-marketing.json", labelHe: "\u05d3\u05e3 \u05d4\u05d1\u05d9\u05ea \u2014 \u05e9\u05d9\u05d5\u05d5\u05d5\u05d9\u05d9\u05d5\u05df" },
];

export function listComparisonEntries(): { slug: string; nameHe: string }[] {
  const pages = comparisonPages as Record<string, { hero?: { title?: string }; metadata?: { title?: string } }>;
  return Object.keys(pages)
    .sort()
    .map((slug) => ({
      slug,
      nameHe: pages[slug]?.hero?.title ?? pages[slug]?.metadata?.title ?? slug,
    }));
}

export function getSiteContentEntry(id: string): SiteContentEntry | undefined {
  return SITE_CONTENT_ENTRIES.find((e) => e.id === id);
}
