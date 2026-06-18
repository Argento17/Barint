---
id: TASK-308
title: Content authoring — fresh Hebrew copy for the 27 changed/new products across 7 shelves (minimal publish, milk-quality bar)
owner: content-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-17
closed_at: 2026-06-17
depends_on: [TASK-307]
blocks: []
category_id: null
close_reason: >
  Orchestrator-verified against artifacts (not face-value). 27/27 PENDING_COPY authored across 7 staging files
  (cereals 1, cakes 3, cookies_coffee 2, granola 12, juices 4, brined 3, hummus 2); confirmed 0 remaining PENDING on
  the 6 clean shelves' author-targets. Quality spot-check on all grade-changed products (dump _rescore_staging/_qa_authored_dump.txt)
  = milk-grade: every rowVerdict opens with calorie density; sodium fact-only; grades as letters; no framework leakage;
  grade-changed copy honestly reflects the NEW grade (cakes E margarine-base+additives, brined B/B/C brine-sodium,
  hummus 577480 C→E eggplant-spread = RT-3 Anti-Immunity fix, 577572 C→D matbucha). The 6 clean shelves are publish-ready.
  NOTE (not a TASK-308 defect): hummus had 55 grade-unchanged products still at PENDING because hummus was excluded from
  TASK-305 copy_carryover + TASK-307 schema_strip (it was being re-curated in parallel). That carry+strip parity gap is
  tracked separately as TASK-309 (P162, C1-GROK) — TASK-308 authored exactly its 2 hummus grade-changed targets correctly.
summary: >
  Author PENDING_COPY for the 27 grade-changed/new products (cereals 1, cakes 3, cookies_coffee 2, granola 12, juices 4, brined 3, hummus 2) in each shelf's LIVE copy field set ONLY. Ground every line in the product's staging trace (real drivers/score/grade/nutrition/ingredients); milk-quality editorial bar; assertive/finding-first; sodium fact-only; no banned phrases; no fabrication; Hebrew. Also sanity-check the 10 grade-same-but-score-moved carried products for stale number references. Staging-only; no deploy.
---

# TASK-308 — Content authoring — fresh Hebrew copy for the 27 changed/new products across 7 shelves (minimal publish, milk-quality bar)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
