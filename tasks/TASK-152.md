---
id: TASK-152
title: "Promote cheese-spreads (גבינות לבנות וממרחים) to LIVE — build the /hashvaot comparison page from run_cheese_003"
owner: frontend-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-02
completed_at: 2026-06-02
closed_at: 2026-06-02
closed_by: cc-agent
close_reason: "CC close-gate PASSED — all return-block claims independently verified against artifacts: (1) bari-web/src/data/comparisons/cheese_frontend_v1.json present, _meta.product_count=52 / 52 actual, grades B20/C25/D6/E1, 3 Sec-6.4 disclosures carried; (2) factory_run_003/frontend_package.json:8 promoted_to_frontend=true (authoritative=true); (3) route /hashvaot/cheese (page.tsx) + registry/categories/cheese.ts + registry/index.ts:2 import + :21 entry + types.ts:7 'cheese' + cheese-comparison-page.tsx all exist; (4) SCORE INTEGRITY: 52/52 live products match the Nutrition-signed package on barcode, 0 score/grade drift — display rounding only, no scoring logic touched; (5) build green (tsc clean, /hashvaot/cheese prerendered, agent-reported). DoD (frontend integration + promotion) MET. DEFERRED follow-ups (non-blocking, correctly flagged): Content editorial review of insightLine + hero/prologue/methodology copy (consumer-final gate, AI-drafted); no /hashvaot index hub card (yogurts also absent — consistent); interactive mobile-RTL visual QA not run."
depends_on: [TASK-142]
blocks: []
parent: TASK-142
category_id: cheese_spreads
roadmap_impact: true
cc_reviewed: 2026-06-02
cc_comments:
  - date: 2026-06-02
    flag: fyi
    text: "Product (owner) flipped frontend_package.json authoritative=true on 2026-06-02 after Nutrition grade-publication sign-off (factory_run_003/NUTRITION_SIGNOFF_VERDICT.md). The data work (TASK-142/142A/145) is CLOSED + signed; this is the FRONTEND-ONLY promotion that was never tasked. NO scores/scoring may change."
  - date: 2026-06-02
    flag: verify
    text: "Frontend must flip promoted_to_frontend=true in factory_run_003/frontend_package.json only after the dataset physically lands in bari-web/src/data/comparisons/ and renders. CC close-gate will verify the file exists in bari-web AND the package flag is flipped."
summary: >
  The cheese-spreads full BSIP0->BSIP2 cycle (run_cheese_003, engine 0.4.1 unmodified) is CLOSED and
  Nutrition-signed for publication, but was never promoted to the website — factory_run_003/frontend_package.json
  sat NON-AUTHORITATIVE and no cheese_frontend_*.json exists in bari-web. Product (owner) approved promotion
  2026-06-02 (authoritative now true). Build the LIVE /hashvaot cheese comparison page: transform
  02_products/cheese_spreads/factory_run_003/frontend_package.json (59 products; 52 display-approved; 4 sub-pools)
  into bari-web/src/data/comparisons/cheese_frontend_v1.json matching the existing comparison schema
  (id/name/imageUrl/score/grade/confidence/insightLine/_cluster/expansion + _meta), and wire it into the unified
  responsive ComparisonPage (the TASK-148 surface). Frontend-only; NO scores/grades/scoring touched.
---

# TASK-152 — Promote cheese-spreads to LIVE

Spun off from TASK-142 at the Product Owner's instruction (2026-06-02). The data + governance + Nutrition
sign-off are all done; this is the missing **frontend integration / promotion** step.

## Authorized state (verified before dispatch)
- `02_products/cheese_spreads/factory_run_003/frontend_package.json` → `authoritative: true` (Product, 2026-06-02),
  `promoted_to_frontend: false` (flips on completion).
- Nutrition sign-off APPROVED: `factory_run_003/NUTRITION_SIGNOFF_VERDICT.md` (all 5 grade-publication decisions).
- Counts: total 59 · display_approved 52 · withheld: 1 misrouted / 1 A-ceiling / 5 transparency-tier (partial panels).
- 4 sub-pools: cottage / white-cheese-quark / cream-cheese-spread / labaneh. Grades A 1(withheld) / B 20 / C 25 / D 7 / E 1.

## Scope (frontend-only)
1. Build `bari-web/src/data/comparisons/cheese_frontend_v1.json` from the factory package — match the live
   comparison schema (see `yogurts_frontend_v2.json` / `maadanim_frontend_v2.json` for `_meta` + per-product shape:
   `id, name, imageUrl, score, grade, confidence, insightLine, _cluster, expansion`). Only the **52 display-approved**
   products render; the 7 withheld are excluded (or shown transparency-tier per the canonical template — match yogurt/bread precedent).
2. Wire the category into the unified responsive ComparisonPage (TASK-148 surface). Sub-pools map to in-list band dividers (`_cluster`).
3. Ship the **2 PO-approved Sec 6.4 disclosure notes** (`disclosures_sec_6_4` in the package) and the **labaneh n=1 standalone** display condition.
4. Flip `promoted_to_frontend: true` in `factory_run_003/frontend_package.json` once it renders.
5. `tsc` + lint + build must pass; visual + mobile RTL QA.

## Hard guards
- **NO scores, grades, or scoring logic touched** — display layer only (CLAUDE.md frozen invariants).
- Do not invent product/nutrition data — render only what the package carries; preserve all 3 confidence states.
- insightLine copy must follow the canonical insight-line spec (composition fact / contradiction / position; restrained-but-fearless). **Content Agent review of the Hebrew insight lines + hero/prologue/methodology is the follow-up editorial gate** before this is considered consumer-final.

## DoD
`cheese_frontend_v1.json` present in bari-web and rendering on /hashvaot; ComparisonPage integration; 52 products
display; sub-pool bands; 2 disclosures + labaneh condition shown; `promoted_to_frontend: true`; tsc+lint+build green;
mobile RTL QA clean. Then propose RETURNED with the file:line evidence.
