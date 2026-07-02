---
id: TASK-384
title: Magnesium full data rebuild + corrected model
owner: data-agent
status: IN_PROGRESS
priority: HIGH
created_at: 2026-06-23
depends_on: []
blocks: []
category_id: magnesium
summary: >
  Rebuild magnesium corpus on verified per-product elemental-mg foundation (reconcile Nutrition vs Data label-audit conflict), apply corrected administered-elemental + bioavailability-class + safety model, re-gate. Page OFFLINE (master 3da07e681). Re-publish needs owner+Product co-sign (tripwire 1).
---

# TASK-384 — Magnesium full data rebuild + corrected model

<!-- opened with new_task.py; fill in context / scope / the deliverable -->

## Progress log

### 2026-06-25 (orchestrate, unattended) — post-publish queue item #1 DONE: owner-requested post-mortem
- Owner asked (2026-06-23) for "what went wrong + how to get smarter for next supplement work." Dispatched native Sonnet; report written to **`02_products/supplements/magnesium_v3_postmortem_v1.md`** (24KB, UNCOMMITTED — supersedes the cycle-1-only `magnesium_postmortem_v1.md`, which was left intact).
- Orchestrator-verified: file exists, full structure (timeline cycles 0/1/2 · grouped root causes · gates-caught-vs-missed · concrete recommendations), exec-summary facts match the board record (absorbed-vs-administered v1 bug; elemental flip-flop resolved by Altman NRV 186% + MagUP dual-line 750/450; LOW=0.35 outcome-engineered; deterministic gates as the real safety net; 3× mobile-geometry + 2× verdict-drift).
- Top-2 recommendations: a mandatory physical-label-panel gate (NRV%/two-line compound+elemental) before scoring any supplement where compound-vs-elemental matters; a clinical-model-validity gate separate from the structural gates.
- TASK-384 itself stays IN_PROGRESS — page is re-published LIVE and fully gate-cleared; pending owner live-review. Other post-publish-queue items remain (H-1 discoverability/Product, H-2 theme image/Design, M-1 grade-chip contrast/Design, Tink label attempt, skus_full JSON sync).
