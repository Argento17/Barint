---
id: TASK-167
title: Comparison rows: show description sentence (insightLine) instead of +/- on collapsed row
owner: frontend-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-02
closed_at: 2026-06-02
closed_by: cc-agent
close_reason: "Owner reversal after seeing the +/- live (chose 'sentence only' via preview). Removed the rowReason assignment from the 3 enrichers (row-surface.ts enrichRowSurface -> metrics only; enrichRowReasonOnly -> passthrough for snacks; hummus enrichHummusRowSurface; maadanim enrichMaadanimRowSurface) + deleted the now-unused local shortenReason in hummus/maadanim (kept the exported one in row-surface — milk imports it). Collapsed rows now fall back to the authored insightLine sentence (100% coverage across all 8 categories); metric bars retained; +/- positive/limiting signals remain in the expansion (shown when a row opens). Milk unchanged (already renders its 2-sentence rowVerdict). Display-only, no scores touched. tsc/build(34 routes)/lint clean."
depends_on: []
blocks: []
category_id: null
summary: >
  Owner reversal after seeing it live: collapsed rows should show the full description sentence (insightLine) + metric bar, NOT the terse +/- tags. Remove rowReason from enrichers (cheese/yogurts/veg-spreads/bread/snacks/hummus/maadanim); keep metrics; +/- detail stays in expansion. Milk already shows rowVerdict sentence (unchanged). Display-only.
---

# TASK-167 — Comparison rows: show description sentence (insightLine) instead of +/- on collapsed row

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
