---
id: TASK-606
title: Milk shelf fat/carbs published as null despite being live-scrapable (BSIP1 enrichment gap)
owner: data-agent
status: BLOCKED
blocker: owner-gated - re-enrichment changes published data/scores; movement table first (after TASK-602 fan-out)
priority: MEDIUM
created_at: 2026-07-11
depends_on: []
blocks: []
category_id: null
summary: >
  Found by TASK-602 milk pilot: fat and carbs are published null on 15/15 evidence-backed milk products, yet both are present on the live Shufersal labels (e.g. 8000215204554: live fat 2.4g/carbs 10g, published null). This is a BSIP1 enrichment gap (data not carried from capture to served JSON), not a source problem - now that captures exist (TASK-602), the values are recoverable. Re-enrichment CHANGES PUBLISHED DATA and may touch scores -> owner-gated, movement table first, do NOT silently fill. Likely extends to other liquid shelves. Diagnose scope after the re-scrape fan-out completes.
---

# TASK-606 — Milk shelf fat/carbs published as null despite being live-scrapable (BSIP1 enrichment gap)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
