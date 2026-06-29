import breadArticleData from "@/data/blog/bread-article.json";

export const BREAD_BLOG_HREF = "/blog/lechem";
export const BREAD_HASHVAOT_HREF = "/hashvaot/bread";

/**
 * Article content object for the bread deep-dive.
 *
 * Corpus: real_bread_retail_003_v1 — Shufersal shelf scan, 25–26 May 2026.
 * 256 scanned → 81 scored → 24 displayed products (frontend v2).
 * Scores from run_bread_008_headpin (engine-baseline-2026-06-04).
 * Scope: Shufersal only — no multi-retailer claims.
 *
 * Template: blog_template_v1.md (TASK-199). Second article after olive oil.
 * Component extraction: InsightBlock, FindingCard, BuyingGuideCard,
 * RecentArticleCard, ScienceSection extracted to src/components/blog/shared/.
 */
export const breadArticle = breadArticleData;
