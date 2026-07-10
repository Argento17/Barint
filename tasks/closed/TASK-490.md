---
id: TASK-490
title: Milk product-row antithesis + em-dash sweep (milk skipped the PR#51/#53 overhaul as old "gold standard")
owner: content-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-07-03
closed_at: 2026-07-03
close_reason: "SHIPPED LIVE PR #72 (merged; origin/master 32198372 ancestor-verified). Milk product-row antithesis 13 rewrites (all לא forms) → positive declaratives + em-dash 80→72, meaning preserved. Two-gate: Content lane (Sonnet, separate author) + Adversarial QA GO (13/13 meaning-preserved vs live nutrition, 0 residual in-scope, 0 invented). Barcode-keyed 0 score/grade/rank change. Legacy milk-comparison.json correctly untouched (unrendered). Micro-follow-ups: page_copy.methodology disclaimer ולא (TASK-484 tail), hebrew_readability word-boundary."
depends_on: []
blocks: []
category_id: milk
summary: >
  Milk was excluded from the PR#51/#53 copy overhaul as the old "gold standard" (retired 2026-07-03 — milk
  is like any other category). Its product-row copy (rowVerdict / positiveSignals / limitingFactors) still
  carries ~10 "X, לא Y" antithesis lines (e.g. "נגיעת שקדים, לא בסיס שקדים"; 1 "אלא") + em-dashes that every
  other category's overhaul removed. Bring milk product-row copy to the same standard: owner phrasing rules
  (no define-by-negation antithesis in any לא/ולא/אלא form; minimize em-dashes; no grade-letter-as-crutch),
  preserving meaning + any legitimate owner-voice signature. Two-gate (Content author + Adversarial QA).
---

# TASK-490 — milk product-row antithesis + em-dash sweep

## Scope (origin/master live milk files)
- `bari-web/src/data/comparisons/milk_frontend_v1.json` — product rowVerdict / expansion.positiveSignals /
  expansion.limitingFactors. (Confirm whether milk-comparison.json legacy rows also render antithesis via
  milk-page-data.ts's milkProducts export — if a rendered legacy row carries antithesis, include it.)
- This is the milk PRODUCT-ROW copy — NOT page_copy (page narrative was swept in TASK-484).

## Deliverable (Content lane authors; do NOT close — propose RETURNED)
1. Find every antithesis/define-by-negation in milk product-row copy across ALL Hebrew forms — scan
   `,\s*ו?לא\s`, `\bאלא\b`, and the "X, not Y" English pattern (the recurring miss is the non-comma `ולא`
   form — TASK-477 RT-M1, 3rd recurrence). Rewrite to positive declaratives that carry the same fact.
2. Minimize em-dashes (owner rule). Do not name the grade letter as a crutch.
3. PRESERVE: the real fact/number in each line; any legitimate owner-voice rhetorical signature (keep-vs-
   reword ledger like TASK-484); do NOT touch score/grade/rank or any non-copy field.
4. Base OFF origin/master (worktree off origin/master, not local HEAD — F1 divergence). Isolated worktree.
5. Two-gate: Content author → Adversarial QA (residual-antithesis scan all forms + meaning-preservation +
   render). Consumer copy → owner PR (tripwire-2).

## Guards
- No score/grade/rank change (tripwire-1). No new claims/numbers invented. OFF irrelevant (copy only).
- Orchestrator does NOT author — Content lane authors, QA gates.

## Return: 5-part + keep-vs-reword ledger + machine-readable Return Contract. Propose RETURNED.

## RETURNED (Content lane general-purpose+Sonnet, branch content/task490-milk-antithesis) + orchestrator-VERIFIED
- (Data-Agent mis-route self-refused as out-of-charter — correct lane discipline; re-routed to a Sonnet content lane, a separate author from orchestrator per content_signoff_hard_rule.)
- **13 antithesis rewrites across 10 products** (rowVerdict / expansion.limitingFactors / expansion.comparisonContext) → positive declaratives; 0 KEEP (no legitimate rhetorical לא found — all were pre-overhaul define-by-negation). Legacy milk-comparison.json correctly UNTOUCHED (agent grep-confirmed its antithesis fields are unrendered — only image/name/score/grade consumed by the 4 blog/home consumers).
- **Orchestrator barcode-keyed verify vs origin/master:** 0 protected-field change (score/grade/rank/brand/confidence); only copy fields changed; independent all-forms residual-antithesis scan = 0. tsc 0. Em-dash 72 = house style (peers 68–583); reworded only in the 13 antithesis-adjacent lines, no blanket sweep (correct — no scope creep).
- **Adversarial QA = GO** (a400f8da): 0 CRIT/0 HIGH. 13/13 rewrites meaning-preserved (independently re-derived vs live nutrition/ingredients, not from ledger); 0 residual antithesis in-scope; 0 invented claims; render clean (200/RTL/0 console/phrases live in DOM/0 encoding corruption); tsc+eslint 0; exactly 13 diff lines, 0 score/grade/nutrition change. 3 MEDIUM non-blocking: (1) almond-pair 2 products softened explicit "not-a-base" → implicit via "נגיעה/touch" (defensible, numbers preserved) — content-agent awareness; (2) 1 PRE-EXISTING residual `ולא` in page_copy.methodology (TASK-484 page-narrative scope, likely approved disclaimer form — not TASK-490); (3) hebrew_readability false-positive נובה-in-תנובה — gate word-boundary bug.
- **🚀 PR #72 OPENED** https://github.com/Argento17/Barint/pull/72 (consumer copy = owner merge, tripwire-2). Two-gate satisfied (Content author + Adversarial QA GO). CLOSE on merge; prune t490 (⚠️ NESTED C:\Bari\bari_wt_t490) + t490_qa.
- **Micro-follow-ups logged:** page_copy.methodology `ולא` disclaimer double-check (TASK-484 tail); hebrew_readability word-boundary fix (TASK-453 class).
