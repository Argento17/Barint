import hummusArticleData from "@/data/blog/hummus.json";

export const HUMMUS_BLOG_HREF = "/blog/hummus";
export const HUMMUS_HASHVAOT_HREF = "/hashvaot/hummus";
export const HASHVAOT_HREF = "/hashvaot";

/**
 * Article content object for the hummus deep-dive.
 *
 * The prose now lives in src/data/blog/hummus.json so it can be edited through
 * the /admin blog editor (TASK-350). The page renders identically — this module
 * just re-exports the data. Provenance (unchanged):
 *
 * Corpus anchor: run_hummus_003 (v5-glassbox_w4) — 64 products, Shufersal only,
 * scrape date 2026-05-30.
 *
 * Products referenced with exact corpus scores (not rounded, not invented):
 *   - חומוס (bsip1_7296073733324): 88/A
 *   - חומוס מסעדות (bsip1_7296073725404): 80/A
 *   - סלט חומוס (bsip1_6666307): 77/B
 *   - חומוס גלילי (bsip1_7290110579319): 67/B
 *   - חומוס אבו גוש (bsip1_7296073725381): 67/B
 *   - חומוס גרגרים בתטבילה (bsip1_7290112968685): 61/C
 *
 * Grade distribution from corpus: A=6, B=24, C=28, D=6
 * Sodium range (hummus_spread): 12 mg – 623 mg per 100g
 * Score range: 42–88
 *
 * CORPUS SCOPE: single-retailer (Shufersal). Do not claim multi-retailer.
 */
export const hummusArticle = hummusArticleData;
