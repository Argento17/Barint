---
id: TASK-233C
title: "Editorial copy routing + grade-literal policy ruling (root cause #3)"
owner: content-agent
status: IN_PROGRESS
priority: HIGH
created_at: 2026-06-10
depends_on: [TASK-233]
blocks: []
roadmap_impact: true
work_type: editorial-governance
---

# TASK-233C — Editorial copy routing + policy

From the TASK-233 sweep, root cause #3: per-product consumer copy is emitted by `build_*()`
template functions in the generators, never filtered by the editorial system.

## Two parts
1. **Policy ruling (Content + Design, do first).** Grade literals (`90/A`, `70/B:`) appear in
   consumer copy on 4 categories (frozen_vegetables, snacks, cereals, bread); the offline
   `is_clean` gate flags them as score-mechanic leaks. But this is a **pre-existing style on the
   oldest categories**, and it collides with the verdict-row model (verdict ends on grade).
   **Rule:** is the literal score in prose banned, or acceptable when the chip already shows it?
   Document the ruling; it sets whether QA-001/002/004 are blockers.
2. **Unambiguous fix regardless of the ruling:** remove the **internal rescore-history narration**
   in cereals (bsip1_cereal_5010029000061 / 5900020012814 rowVerdict — "78/B in the previous
   version due to a data error; corrected to 55/C"). That exposes pipeline internals.
3. **Forward fix:** route per-product copy through the editorial banned-term filter at write time
   (couples to TASK-233B's shared core).

## Ruling delivered (Content Agent, 2026-06-10) → `01_framework/editorial/grade_literal_in_copy_ruling_v1.md`
1. **Grade literals (`NN/X`) in prose: BANNED everywhere** — the chip is the sole home for the
   numeral (score_presentation_v1 Rule 1 + insight_line_spec anti-redundancy). The grade *letter*
   in a causal clause ("עוצר ב-B כי…") stays allowed; only the `NN/X` mechanic moves to the chip.
   QA-001 blocks frozen_vegetables **at merge** (pre-merge); QA-002/004 are HIGH defects on the
   normal track, **not** emergency-paused.
2. **Cereals rescore narration: REMOVE unconditionally** — no rescore/version/pipeline references
   in consumer copy (framework invisibility).
3. **Verified tooltip canonical = "הציון מבוסס על רשימת הרכיבים ולוח התזונה המלאים"; RETIRE
   "ממקור המזון הרשמי"** as an inaccurate provenance overclaim (data is a Shufersal scrape).

## DoD
- [x] Written grade-literal policy ruling (Content), disposition of QA-001/002/004
- [x] Cereals rescore-narration removed (or re-authored) — no internal pipeline references
      (3 rowVerdicts + 2 insightLines re-authored on current truth; grade letter matched to chip,
      catching a stale "55/C" claim on a product that is live at 75/B)
- [x] `NN/X` literals stripped from consumer copy per ruling (frozen_veg via regen of
      build_insight_line; snacks/cereals/bread via surgical string patch). 0 residual slash
      literals across all 4 categories.
- [ ] Banned-term filter applied to per-product copy generation path (couples to 233B) — deferred:
      forward-fix belongs with 233B's shared-core write path; this task delivered the data remediation.
- [x] No score values changed (string-only edits verified via diff; frozen-veg regen preserved
      Data's Phase-1 confidence=partial + real image URLs — produced by the untouched shared core)
