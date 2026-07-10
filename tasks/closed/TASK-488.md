---
id: TASK-488
title: Cookies + granola description-parity — remove crackers-class deep-dive layer (match golden), mirror TASK-486
owner: frontend-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-07-03
closed_at: 2026-07-03
close_reason: "SHIPPED LIVE PR #70 (merged; origin/master 32198372 ancestor-verified; cookies deep-dive 0/117 live). Cookies+granola deep-dive layer removed → golden parity (mirror #67). Barcode-keyed 0 protected-field change (117→117, 22→22); Adversarial QA render gate GO. Orchestrator finalized push after lane stalled on node_modules copy."
depends_on: []
blocks: []
category_id: null
summary: >
  Orchestrator cross-page audit (2026-07-03, part of the owner "all batches" + crackers flag) found cookies
  and granola are ALSO out of golden parity on the deep-dive description layer — worse, PARTIALLY, so the
  block appears on some rows and not others within the same page. cookies_coffee_frontend_v2: consumerTakeaway
  61/117, bestUseCases 61/117, bariInterpretation 117/117. granola_frontend_v2: expansion.consumerExplanation
  7/22. Golden brined-cheeses = 0 on all four. Same fix as crackers TASK-486 (PR #67): remove the four
  DeepDiveSection-feeding fields so both pages match the golden 4-section structure.
---

# TASK-488 — cookies + granola deep-dive parity (mirror TASK-486 crackers)

## Verified facts (orchestrator, origin/master)
- The DeepDiveSection block is gated by hasDeepDiveContent() (deep-dive-section.tsx:251-262) on four fields:
  `consumerTakeaway`, `bestUseCases`, `bariInterpretation` (top-level), `expansion.consumerExplanation`.
- Golden brined-cheeses + 12 live pages have 0/N on all four → no block (correct golden structure).
- `cookies_coffee_frontend_v2.json` (117 products): consumerTakeaway 61, bestUseCases 61, bariInterpretation 117.
- `granola_frontend_v2.json` (22 products): expansion.consumerExplanation 7.
- TASK-486 already proved wholesale removal = golden parity (Adversarial QA GO, PR #67).

## Deliverable (Frontend owns; mirror TASK-486; do NOT close — propose RETURNED)
1. Remove all four fields wherever present from ALL products in both JSONs (crackers-identical subtraction).
   Preserve byte-for-byte: score/grade/rank/categoryTotal/rowVerdict/insightLine/brand + expansion
   comparisonContext/positiveSignals/limitingFactors/nutrition/ingredients/confidence. Zero score/grade/rank
   change. Add a `_meta` note per file (same convention as TASK-486).
2. Base OFF origin/master (git worktree add -b <branch> C:\bari_wt_t488 origin/master) — do NOT cut off local
   HEAD (F1 divergence). Do NOT git stash/checkout the shared tree.
3. tsc + lint + build must pass; confirm /hashvaot routes for cookies + granola still generate.
4. Consumer-facing removal → owner merges (tripwire-2); build+push+return, never merge. Adversarial QA render
   gate before owner PR (same as TASK-486) — confirm nothing stranded on real DOM.

## Guards
- No new copy authored (pure subtraction). No score change (tripwire-1). OFF irrelevant (removal only).

## Return: 5-part + machine-readable Return Contract. Propose RETURNED. Do not write CLOSED.

## RETURNED (branch fix/task488-cookies-granola-parity) + orchestrator-VERIFIED
- Agent did the edits off origin/master but stalled in a wait-loop copying node_modules for tsc/build, never committed/pushed. Substance was complete + correct.
- **Orchestrator barcode-keyed verify vs origin/master:** cookies 117→117, granola 22→22; **0 protected-field mismatches** (score/grade/rank/rowVerdict/insightLine/brand/comparisonContext/positiveSignals/limitingFactors); 0 residual removed fields. Same clean subtraction as crackers #67.
- Orchestrator committed + pushed the verified worktree diff (2 files) as branch fix/task488-cookies-granola-parity (lane stalled; git mechanics only, no content authored). tsc/build deferred to QA gate (pure optional-field removal — crackers proved identical op builds clean).
- **Adversarial QA render gate = GO** (ab940cc4): independently re-diffed vs origin/master (0 protected mismatch, 0 residual banned fields); deep-dive block absent on real DOM cookies+granola mobile+desktop (rows across full range incl. formerly-populated + never-populated → partial-application bug resolved); structure matches golden; retained content intact; 0 console errors/0 h-scroll; tsc/lint/build 0 (262 pages). Pre-existing note (NOT introduced, byte-identical on live): hebrew_readability "NN.N" false-positive on ingredient-% callouts (10.6% oat etc.) on 6 rows → known TASK-453 class, no action.
- **🚀 PR #70 OPENED** https://github.com/Argento17/Barint/pull/70 (consumer-facing removal = owner merge, tripwire-2). CLOSE on merge; prune t488 + t488qa.
