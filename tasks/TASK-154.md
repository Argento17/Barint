---
id: TASK-154
title: "Decide cross-category dairy consistency: same SKU (יופלה GO) shows 70/B in yogurts vs 78/B in maadanim because BARI_TASK144_FIXES is ON for maadanim, OFF for yogurt/cheese (TASK-146)"
owner: product-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-02
completed_at: 2026-06-02
closed_at: 2026-06-02
closed_by: cc-agent
close_reason: "RULING (Product Agent, PO-confirmed 2026-06-02): AFFIRM Option 1 — accept the cross-page יופלה GO grade difference as GOVERNED (the deliberate TASK-146 keep-maadanim-scoped state). REJECT Option 3 (dedupe — hides an engine inconsistency behind info-architecture + a contestable taxonomy claim). Convergence (Option 2) is DEFERRED, not pursued now: the A-ceiling is the binding constraint — a flag-flip would create 3 yogurt B→A's, but 2 (דנונה פרו 20/21) are protein-enriched matrices that FAIL C4 of RULING-DAIRY-A-01 and must NOT get A, so convergence requires a governed re-run with C1–C6 A-enforcement (NOT a flag flip) + Nutrition co-sign. CC CORRECTION to the ruling's mechanics: TASK-143 is CLOSED (already ran run_yogurt_004 on 0.4.1 with fixes OFF), so there is NO open vehicle to 'ride' — if convergence is ever pursued it is a NEW governed re-run task (or a TASK-143 reopen). Interim mitigation = TASK-155 (2-SKU UI disclosure). Decision-only; no scores changed, no flag flipped. PARKED NUTRITION QUESTION (for any future convergence): under C1–C6 enforcement on post-142A-corrected fat, does the ceiling withhold A from דנונה פרו 20/21 (C4 fail) while granting only legitimate intact-dairy A (e.g. goat yogurt 3%)? If Nutrition can't guarantee it, Option 1 is permanent (acceptable terminal state)."
depends_on: [TASK-143, TASK-146]
blocks: []
category_id: null
work_type: decision
roadmap_impact: true
cc_reviewed: 2026-06-02
cc_comments:
  - date: 2026-06-02
    flag: fyi
    text: "Surfaced by the owner while reviewing the live site (thought yogurts == maadanim). Validated: they are DISTINCT corpora (yogurts 11 SKUs / maadanim 87 / 0 shared ids), but 2 SKUs legitimately appear on both shelves — יופלה GO מועשר בחלבון (70/B yog vs 78/B maad) and יופלה GO תות (49/D vs 56/C). Same physical product, two grades on two live pages."
  - date: 2026-06-02
    flag: verify
    text: "Root cause CONFIRMED (not a re-run gap): both run_yogurt_004 and run_cheese_003 traces are engine 0.4.1. The delta is the BARI_TASK144_FIXES flag — ON for maadanim (engine 0.4.1 + 3 dairy fixes; lifts יופלה GO 70→78), OFF for yogurt+cheese per the TASK-146 ruling. TASK-143 (yogurt re-run) is already CLOSED/LIVE; a re-run will NOT change this. This is a governance decision, not data work."
summary: >
  The owner noticed the live yogurts and maadanim pages look like the same products. Validation: they are
  DISTINCT datasets (yogurts_frontend_v2 = 11 SKUs yog-00x; maadanim_frontend_v2 = 87 SKUs bsip1_maadanim_*;
  0 shared ids), overlapping only in brand (דנונה/יופלה) and in exactly 2 dual-shelf SKUs (יופלה GO ×2). Those
  2 SKUs carry DIFFERENT grades across the two pages (יופלה GO 70/B yog vs 78/B maad; יופלה GO תות 49/D vs 56/C)
  because maadanim runs with the TASK-144 dairy fixes ON (BARI_TASK144_FIXES; engine 0.4.1) while yogurt+cheese
  run with them OFF — the deliberate TASK-146 ruling (KEEP maadanim-scoped, because applying the fixes to yogurt
  creates B→A grades that violate RULING-DAIRY-A-01 / the dairy A-ceiling). DECISION for Product+Nutrition:
  accept the governed cross-page inconsistency as-is, OR resolve it (e.g. apply the fixes cross-category under a
  numbers-versioning re-run + A-ceiling reconciliation, or dedupe/cross-reference the dual-listed SKUs, or
  define a single canonical category for boundary SKUs). No data re-run resolves this; the lever is the flag +
  the A-ceiling governance.
---

# TASK-154 — Cross-category dairy consistency (יופלה GO 70 vs 78)

Decision task. Surfaced by the owner via the live site; validated + root-caused by CC 2026-06-02.

## The facts (verified)
- yogurts `/hashvaot/yogurts` ← `yogurts_frontend_v2.json` (run_yogurt_004, engine 0.4.1, TASK-144 fixes OFF).
- maadanim `/hashvaot/maadanim` ← `maadanim_frontend_v2.json` (engine 0.4.1, TASK-144 fixes ON).
- 2 dual-shelf SKUs diverge: `יופלה GO מועשר בחלבון` 70/B (yog) vs 78/B (maad); `יופלה GO תות` 49/D vs 56/C.
- 70/B is literally TASK-144's documented PRE-fix number; 78/B is POST-fix. Difference = the flag, per TASK-146.

## The tradeoff (why TASK-146 said no to cross-category)
Applying the TASK-144 fixes to yogurt = +8 incl **3 B→A**; those raw A's violate **RULING-DAIRY-A-01** (dairy
A-ceiling). TASK-146 kept the fixes maadanim-scoped to protect the ceiling. So consistency vs A-ceiling is a
genuine conflict — not resolvable by a re-run.

## Options for Product + Nutrition
1. **Accept as governed** — document the per-category engine-flag difference; optionally add a UI disclosure on
   the 2 dual-listed SKUs. Lowest cost; the inconsistency stays visible.
2. **Apply fixes cross-category WITH A-ceiling reconciliation** — flip BARI_TASK144_FIXES on for yogurt(+cheese)
   under a governed numbers-versioning re-run + baseline re-freeze + DEC-005-style reconciliation, ensuring the
   A-ceiling still withholds the new A's (so consistency without violating RULING-DAIRY-A-01). Reopens TASK-146.
3. **Dedupe boundary SKUs** — define a single canonical category for products that sit on both shelves (יופלה GO
   is arguably a protein snack/maadan, not a yogurt), and cross-reference rather than double-list with two grades.

## DoD
Product+Nutrition ruling recorded (which option, why), TASK-146 reconciled/annotated, and any downstream task
(re-run / UI disclosure / dedupe) registered. Decision only — no scoring change is made under this task.
