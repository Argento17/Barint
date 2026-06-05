---
name: bsip2_task133_and_maadanim_drift
description: BSIP2 engine is at 0.4.0 (TASK-133 protein matrix-awareness + named-additive identity); live maadanim page has pre-existing engine drift unrelated to TASK-133
metadata: 
  node_type: memory
  type: project
  originSessionId: fd379588-f436-4fda-afcc-a5ac11ef20d7
---

**BSIP2 proto_v0 engine is now `0.4.0`** (TASK-133, 2026-06-01): Protein Quality is matrix-aware
(reconstructed-protein ×0.80 / collagen ×0.55 quality-only discount, bar-format + primary-position
gated); Additive Quality has named-additive identity (emulsifier tiering via `ingredient_taxonomy.py`;
BHA −5 named penalty, BHT differentiated). Dimension weights re-synced (DEC-004 G3): 15/15/15/12/10/10/8/6/5/4.
F1 emulsifier deltas are deliberately **neutral/0** — the EV-003 `sprint1` correction already realizes
the directions; don't add a second emulsifier dial without retiring sprint1 (double-count).

**⚠️ Pre-existing maadanim drift (NOT TASK-133):** the live `maadanim_frontend_v2.json` was built by an
older engine state — **85/90 displayed products no longer match the current engine**, including a latent
grade flip (`bsip1_maadanim_7290110323585` 52 C → 47.9 D). Any future maadanim rebuild/rescore must treat
this as its own governed decision; do **not** silently fold it into an unrelated rescore. Recommended a
QA/Product triage task. See [[bari_phase_status]] and `research/TASK-133BCD_validation_report.md`.
