---
id: TASK-233D
title: "Targeted data fixes from the TASK-233 sweep (non-root-cause)"
owner: data-agent
status: IN_PROGRESS
priority: MEDIUM
created_at: 2026-06-10
depends_on: [TASK-233]
blocks: []
roadmap_impact: false
work_type: data-fix
---

# TASK-233D — Targeted data fixes

Discrete defects from `reports/task_233_confirmation_sweep.md` that are not root-cause work.

## Items
- [ ] **frozen_vegetables confidence** — add to `run_confidence_annotation_pass.py` LIVE_FILES and
      re-derive (interim fix if 233B not yet landed) so "full data" stops contradicting `unknowns` (DA-006).
- [ ] **yogurts dup barcode** `7290107936309` — yog-007 + bsip1_yogurt_… scored twice, second is
      untranslated "Greek yogurt"; de-dupe to one product/score (QA-005).
- [ ] **snacks dup barcode** `7290011498894` — snk-015 + snk-003 share one barcode (QA-006).
- [ ] **butter float score** bsip1_butter_369709 `45.2` → round to int (QA-007).
- [ ] **yogurts null image** bsip1_yogurt_7290102394081 — supply image or confirm placeholder (QA-008).
- [ ] **hard_cheeses orphan filename** — `build_hard_cheeses_frontend_redlabel_v1.py` `OUT_WEB`
      points at `hard_cheeses.json`, not the imported `hard_cheeses_frontend_v2.json` (DA-010).
- [ ] **frozen_vegetables broken image URLs (404)** — generator synthesizes
      `MNH68_Z_P_{barcode}_1.png`; the `MNH68_` prefix is a guess and 404s (Frontend Agent
      HTTP-verified). Use the product's real scraped Shufersal asset prefix (cf. cheese `TZE58_`,
      hummus `UFL56_`) or carry the scraped `image_url` through instead of synthesizing it.

## DoD
- [ ] Each item fixed + verified against the 233A gate; no score *methodology* change (rounding/de-dup only)
