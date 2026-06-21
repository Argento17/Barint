import yogurtArticleData from "@/data/blog/yogurt.json";

export const YOGURT_BLOG_HREF = "/blog/yogurt";
export const YOGURT_HASHVAOT_HREF = "/hashvaot/yogurt";
export const HASHVAOT_HREF = "/hashvaot";

/**
 * Article content object for the yogurt deep-dive.
 *
 * Corpus (historical, at time of writing): 89 scored products
 *   Shufersal: 89 products (run_yogurt_005, 2026-06-11 scrape, real Hebrew ingredients)
 *   NOTE: yogurts_frontend_v4.json was retired in the TASK-321 conformance sweep —
 *   yogurts now ships from yogurts_frontend_v1.json on the uniform spine path.
 * Grade distribution: A×9, B×30, C×27, D×23
 * Score range: ~40/D → 90/A (high-protein Greek, 89.9 cap applied per TASK-169D)
 *
 * Corpus scope: Shufersal only (Yohananof products de-listed — OFF contamination).
 * All quantitative claims are scoped to this 89-product corpus.
 *
 * A-ceiling note: the highest score in this corpus is 96/A (partial-confidence product).
 * No yogurt in the corpus reaches the highest confidence tier at A — the top
 * verified-confidence A is דנונה פרו 21 חלבון 0% at 87/A.
 *
 * TASK-201 — Content Agent
 */
export const yogurtArticle = yogurtArticleData;
