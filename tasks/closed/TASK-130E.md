---
id: TASK-130E
title: Fix §2.7 ordering errors in bread and snacks
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-01
completed_at: 2026-06-01
close_reason: "eliminated all \u00a72.7 ordering blockers for Bread and Snacks with verified no score/content changes"
depends_on: [TASK-130C, TASK-130D]
blocks: [TASK-132]
category_id: null
summary: >
  Re-sort only. Fix the §2.7 ordering violations in bread (6) and snacks (1) so products
  are scored-descending with insufficient appended last (contract §2.7). No score changes,
  no content changes — stable sort preserves tie order and existing insufficient order.
---

# TASK-130E — Fix §2.7 ordering errors in bread and snacks

Parent: TASK-130. Depends on TASK-130C (audit) + TASK-130D (unknowns fix).
Constraint: re-sort only, no score changes, insufficient stays last.

## Outcome (2026-06-01) — proposed RETURNED
File: `bari-web/scripts/reorder-corpus.mjs` (re-sort utility; stable sort, byte-faithful
guard + per-product content-identity verification). Datasets re-sorted:
bread_frontend_v2.json (20 products repositioned), snacks_frontend_v2.json (2).
§2.7 (validate-corpus --handoff): bread 6→0, snacks 1→0. Score multiset unchanged on both;
now strictly descending; no insufficient products to append. No score/content changes
(every product object byte-identical, only sequence differs).
bread total handoff errors 8→2, snacks 34→33 — remaining is §2.8 only.
Remaining real launch blocker: snacks §2.8 NOVA leak (29 occ, Content rewrite). Other §2.8
hits (נקי/בריא/כדאי) are accepted heuristic debt (R4) pending QA/Content read.
Awaiting Controller to record CLOSED.
