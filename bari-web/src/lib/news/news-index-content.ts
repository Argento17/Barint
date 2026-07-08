import newsIndexData from "@/data/news/news-index.json";

/**
 * Content module for the חדשות (News) index page.
 *
 * Mirrors the canonical blog content pattern (src/lib/blog/blog-index-content.ts,
 * TASK-134/TASK-199 lineage): a single JSON data file consumed by a layout-stable
 * component. Content authors edit the JSON only; the component never sorts,
 * rounds, or interprets — it renders what's here.
 *
 * News differs from the blog only in kind of content (timely/event-driven
 * commentary vs. evergreen scoring analysis) — not in architecture. Built via
 * TASK-521.
 */
export type NewsArticleCard = {
  slug: string;
  href: string;
  title: string;
  description: string;
  readTime: string;
  published?: string;
  metaLine?: string;
  comingSoon?: boolean;
};

export const newsIndex = newsIndexData.newsIndex;

export const newsArticles: NewsArticleCard[] = newsIndexData.articles as NewsArticleCard[];
