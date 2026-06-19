import type { BreadArticleContent } from "@/lib/comparisons/bread-types";
import breadEverydayData from "@/data/blog/bread-everyday.json";
import breadStandoutsData from "@/data/blog/bread-standouts.json";
import breadWellnessGapData from "@/data/blog/bread-wellness-gap.json";

// Article prose now lives in src/data/blog/*.json (editable via /admin blog editor,
// TASK-350). Corpus stats that were interpolated are baked into the JSON snapshot.
export const BREAD_EVERYDAY_ARTICLE: BreadArticleContent = breadEverydayData as BreadArticleContent;
export const BREAD_STANDOUTS_ARTICLE: BreadArticleContent = breadStandoutsData as BreadArticleContent;
export const BREAD_WELLNESS_GAP_ARTICLE: BreadArticleContent = breadWellnessGapData as BreadArticleContent;

export const BREAD_COMPARISON_HREF = "/hashvaot/bread";
export const BREAD_EVERYDAY_HREF = "/blog/bread-everyday";
export const BREAD_STANDOUTS_HREF = "/blog/bread-standouts";
export const BREAD_WELLNESS_HREF = "/blog/bread-wellness-gap";

export const BREAD_BLOG_HREF = BREAD_EVERYDAY_HREF;

export const breadComparisonMeta = {
  title: "מה באמת יש בלחם שלכם? | Bari",
  description:
    "השוואת לחם, פיתות וקרקרים ממדף שופרסל: 256 מוצרים נסרקו, 81 קיבלו מספיק נתונים לניתוח מהימן, ו-31 נבחרו להצגה השוואתית.",
} as const;

export const breadArticles = [
  BREAD_EVERYDAY_ARTICLE,
  BREAD_STANDOUTS_ARTICLE,
  BREAD_WELLNESS_GAP_ARTICLE,
] as const;

export const breadArticlesBySlug = Object.fromEntries(
  breadArticles.map((article) => [article.slug, article]),
) as Record<(typeof breadArticles)[number]["slug"], BreadArticleContent>;

export const BREAD_ANALYSIS_ARTICLES = breadArticles;
