---
id: TASK-172
title: "Bread corpus: clear the false 'refined base' limitingFactor where non-propagation made it untrue (per-product source check; no score change)"
owner: data-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-06-03
closed_at: 2026-06-03
closed_by: cc-agent
roadmap_impact: true
cc_reviewed: 2026-06-03
depends_on: []
blocks: []
category_id: bread
close_reason: "Both halves DONE + CC-gate verified; owner ruled text-only/keep-grades (TASK-173 model proved scores were never corrupted). (a) limitingFactors half: 5 FALSE-cleared (grounded in real_bread_retail_003_v1 ingredient lists), 3 TRUE-kept (genuinely refined: אחיד/קרקר שוודי/קרם קרקר), 1 kept-as-defensible (חצי מלא, 50/50 whole/white — 'not whole grain' is fair for a half-white loaf). (b) verdict half: 5 insightLines rewritten (497044/7290016967074/2079927/3268252/7290018500460) — false 'refined base / fiber-source unclear' removed, replaced with the TRUE why-B the TASK-173 model exposed (added inulin fiber; long additive/3-emulsifier load; 17% white-flour minority; added gluten+soy engineering; honest half-and-half + low fiber for the name). Independent gate: 0 residual false-claim tokens in the 5 verdicts; git diff = ONLY insightLine (10) + limitingFactors (10) lines, zero score/grade/bottomLine/nutrition drift; grades held (all B); sourdough claimed only where the real list asserts מחמצת; no energy/sugar/fat figures; no framework vocab. Frozen bread grades untouched. shufersal_3268429 (the original trigger) was cleared earlier same day."
cc_comments:
  - date: 2026-06-03
    flag: verify
    text: "limitingFactors half DONE + CC-verified (git diff = limitingFactors-only, 0 score/grade/insightLine/bottomLine drift): 5 FALSE-cleared (shufersal_497044 base-line only, 7290016967074, 2079927, 3268252, 7296073134442), 3 TRUE-kept (2079477, 7296073134459, 8434165658523), 1 AMBIGUOUS (7290018500460 חצי מלא, 50/50 whole/white — Nutrition to rule). RESIDUAL (task NOT done): the SAME false 'refined base' claim is also the stated B-reason in 4 consumer VERDICTS (insightLine) — 497044/7290016967074/2079927/3268252 — now contradicting the cleared limitingFactors + verified-whole-grain raw, on named brands (ברמן/אנג'ל). Needs Content rewrite (drop false claim, keep frozen B, base-agnostic per shufersal_3268429 precedent) + Nutrition grounding. Deeper: per TASK-164 the same bug may have depressed the SCORE itself (B may be an artifact) — frozen-grade, owner ruled de-minimis for 3268429. Held IN_PROGRESS pending owner nod on verdict rewrites."
summary: >
  Full-corpus follow-up to TASK-164: the BSIP0->signal ingredient non-propagation bug stamped 'בסיס קמח מזוקק — לא דגן מלא' onto ~9 bread products in bread_frontend_v2.json as a default. Some are genuinely refined (line TRUE, keep); some are genuinely whole-grain (line FALSE, drop) like shufersal_3268429 (already cleared 2026-06-03). Data: check each carrier against its BSIP0 raw scrape (real_bread_retail_003_v1) ingredient list; Nutrition: confirm true/false per product. Clear limitingFactors (and any 'fiber source unclear' twin) ONLY where demonstrably false; keep where accurate. Display/text only — NO score, grade, or other field change (bread frozen). QA: build + diff isolation.
---

# TASK-172 — Bread corpus: clear the false 'refined base' limitingFactor where non-propagation made it untrue (per-product source check; no score change)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
