---
id: TASK-305
title: Copy carry-over + author-list sizing for the 6 clean shelves (reuse live copy for grade-unchanged; isolate the ~25 needing fresh authoring)
owner: frontend-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-17
closed_at: 2026-06-17
close_reason: >
  Frontend Agent + orchestrator-verified. Carried live copy into the 6 staging pages for 264 grade-unchanged products;
  isolated 25 needing fresh authoring (12 new + 13 grade-changed); flagged 10 grade-same-but-score-moved for copy sanity.
  Idempotent (3 runs identical sha), no bari-web/engine/live touched, OFF=0. SURFACED a publish-scope fork: the staging pages
  are v3 schema but 4 live shelves (cereals/granola/juices/brined) are legacy (insightLine[+rowVerdict] only) — so v3-enrichment
  fields are PENDING on ~244 products that the LIVE pages never had. CORE fields (what live shows) PENDING only on the ~25.
  → Owner decision: Option A minimal publish (author ~25 in each shelf's live field set + strip unused v3 placeholders to match
  live render) vs Option B v3 content upgrade (~244 products). Author list is in the return. Content authoring HELD pending A/B choice.
depends_on: [TASK-303]
blocks: []
category_id: null
summary: >
  For the 6 clean staging pages (cereals/cakes/cookies_coffee/granola/juices/brined): for each grade-UNCHANGED barcode, carry over the existing live page's copy fields (insightLine/rowVerdict/consumerTakeaway/expansion.consumerExplanation/bariInterpretation.interpretation/bestUseCases/comparisonContext) into the staging page; leave PENDING_COPY on grade-CHANGED + NEW products. Flag any grade-unchanged-but-score-moved product whose carried copy might quote a now-stale figure. Output: staging pages copy-filled for the 264 + the precise list of remaining PENDING_COPY products (~25) for the Content Agent. Staging-only; no authoring; no deploy.
---

# TASK-305 — Copy carry-over + author-list sizing for the 6 clean shelves (reuse live copy for grade-unchanged; isolate the ~25 needing fresh authoring)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
