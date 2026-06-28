import comparisonPages from "@/data/site-content/comparison-pages.json";

export interface ComparisonPageChrome {
  hero: { eyebrow: string; title: string };
  prologue: readonly string[];
  methodology: readonly string[];
  categoryNote: string;
  metadata: { title: string; description: string };
}

const pages = comparisonPages as Record<string, ComparisonPageChrome>;

export function getComparisonPageChrome(slug: string): ComparisonPageChrome {
  const chrome = pages[slug];
  if (!chrome) {
    throw new Error(`Unknown comparison page chrome slug: ${slug}`);
  }
  return chrome;
}

export function listComparisonChromeSlugs(): string[] {
  return Object.keys(pages).sort();
}
