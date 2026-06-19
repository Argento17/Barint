import oliveOilArticleData from "@/data/blog/olive-oil.json";

export const OLIVE_OIL_BLOG_HREF = "/blog/shemen-zayit";
export const HASHVAOT_HREF = "/hashvaot";

/**
 * Article content object for the olive oil deep-dive.
 *
 * TEMPLATE NOTE (TASK-199):
 * This file is the canonical content pattern for all Bari blog articles.
 * Future articles (bread, yogurt, hummus, etc.) should follow the same
 * top-level structure:
 *   slug · hero · disclaimer · lead[] · editorialInsights[]
 *   science{} (narrative + citations[]) · findings{items[]} · originData{}
 *   transparencyMatrix{} · externalResearch{} · buyingGuide{} · conclusion{}
 *   methodology{} · recentAnalyses{}
 *
 * Each section maps 1:1 to a named sub-component under src/components/blog/.
 * Content authors edit this file only. Components are layout-stable.
 */
export const oliveOilArticle = oliveOilArticleData;
