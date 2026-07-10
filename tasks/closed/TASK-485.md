---
id: TASK-485
title: Small launch-hardening fixes: chocolate-bars nuts-filter name-only under-select + generator NUTRITION_FIELD_MAP carbs/satFat backfill (cheese/bread/cereals display)
owner: frontend-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-07-03
closed_at: 2026-07-03
close_reason: "SHIPPED LIVE PR #64 (merged 5f29dfa1). chocolate-bars nuts/peanuts filter now matches scraped expansion.ingredients + name (was name-only), + Hebrew plural-stem bugfix; 1→15/23, Snickers caught; verified 15 matches/0 false pos-neg, tsc/build 0, 1 file. Generator carbs/satFat backfill SPLIT to backlog follow-up."
depends_on: []
blocks: []
category_id: null
summary: >
  Small launch-hardening fixes: chocolate-bars nuts-filter name-only under-select + generator NUTRITION_FIELD_MAP carbs/satFat backfill (cheese/bread/cereals display)
---

# TASK-485 — chocolate-bars nuts-filter under-select (from TASK-474 F-C1)

**RESCOPED to nuts-filter ONLY.** Generator NUTRITION_FIELD_MAP carbs/satFat backfill (cheese/bread/cereals, milk-class) SPLIT to a follow-up (bigger, touches confidence copy).

## RETURNED (Frontend, commit a2b7f550) + orchestrator-VERIFIED → PR #64
`chocolate-bars-shelf-filters.ts` nuts filter matched NAME only → 1/23 (missed Snickers). Fix = match scraped `expansion.ingredients` + name; fixed latent Hebrew bug (singular `בוטן` never substrings plural `בוטנים` → stem `בוטנ`). Match 1→15/23.
- Orchestrator-verified: predicate reads expansion.ingredients (scraped, no OFF); independent recount 15 matches, cb-001 Snickers has בוטנים ✓; 1 file 24/7, tsc/build 0.
- **PR #64** https://github.com/Argento17/Barint/pull/64 — consumer-facing = owner merge. CLOSE on merge; prune worktree C:\Bari\bari_wt_t485.
