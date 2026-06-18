---
id: TASK-307
title: Schema-match strip + final author-list — align 6 staging pages to each shelf's live copy field set (minimal publish)
owner: frontend-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-17
closed_at: 2026-06-17
close_reason: >
  Frontend Agent + orchestrator-verified. Aligned 6 staging pages to each shelf's LIVE copy field set, stripping orphan v3
  placeholder fields (so pages render like live, minimal publish). VERIFIED: final author-list = 25 (cereals 1, cakes 3,
  cookies_coffee 2, granola 12, juices 4, brined 3) + hummus 2 = 27 total; 0 NEW PENDING on grade-unchanged products on all shelves.
  Confirmed cookies_coffee 392 PENDING are INHERITED from live (live cookies_coffee_v2 already ships 392 PENDING — frontend handles
  gracefully; resolves the PENDING-render concern). bari-web/engine untouched, idempotent, sha256 verified. Field sets per shelf:
  cereals/granola/brined=insightLine[+rowVerdict/comparisonContext]; juices=insightLine; cakes/cookies=richer (takeaway/explanation/bariInterp/bestUseCases/bottomLine).
depends_on: [TASK-305]
blocks: []
category_id: null
summary: >
  Owner ruling: minimal publish (match live schema). For the 6 staging pages, determine each shelf's LIVE copy field set; remove v3 copy fields the live page does NOT have (so pages render like today, no PENDING_COPY artifacts); keep numbers + the live-set copy fields. Output: staging pages schema-matched to live, with PENDING_COPY remaining ONLY on changed/new products in their shelf's live field set = the precise final author-list for the Content Agent (per shelf: barcode, fields, grade-change/new). Staging-only; no authoring; no deploy.
---

# TASK-307 — Schema-match strip + final author-list — align 6 staging pages to each shelf's live copy field set (minimal publish)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
