---
id: TASK-304
title: Hummus curation — exclude raw/dried chickpea products from the prepared-hummus comparison, re-run, re-gate
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-17
closed_at: 2026-06-17
close_reason: >
  C1-GROK (P160) + orchestrator-verified. Excluded 6 single-ingredient raw/dried/frozen chickpea products (3643820,
  7296073005889, 7296073006015, 7296073705505, 7296073733324, 7296073733331) from configs/hummus_shelfrel_002.json,
  re-ran --shelf, re-gated. VERIFIED: 63 products, all 6 excluded absent, grade-A count 0 (was 5 raw-chickpea bags),
  G8 PASS, C10 milk Δ0, OFF=0, score==trace OK. EGREGIOUS problem fixed. RESIDUAL flagged to owner (softer scope call,
  NOT done here): new top-2 = canned WHOLE chickpeas (B, TASK-069 boundary); ranks 3-5 = products with EMPTY ingredient
  data (7296073733317/733348/1990261, conf=partial) scoring B/75 — first prepared tahini dip is rank 7. Open scope question:
  is the hummus shelf prepared-dips-only or all chickpea products? + data-completeness (empty-ingredient products at B). Owner/Product decision before hummus deploys.
depends_on: [TASK-303]
blocks: []
category_id: null
summary: >
  The hummus shelf's top 5 (all A) are raw/dried chickpeas (single-ingredient חומוס/גרגרי חומוס/100% חומוס), not prepared hummus dip. Add them to configs/hummus_shelfrel_002.json exclusions (reason: out_of_scope raw/dried chickpeas, not prepared spread), identify ALL such single-chickpea-ingredient products on the shelf (not just the 5), re-run via rescore_all --shelf, re-gate (G8+C10+OFF). Staging-only, no deploy. Brings hummus into the clean set.
---

# TASK-304 — Hummus curation — exclude raw/dried chickpea products from the prepared-hummus comparison, re-run, re-gate

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
