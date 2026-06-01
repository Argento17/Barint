---
id: TASK-136
title: "Governed maadanim rescore — re-sync the live page to engine 0.4.0 (resolve pre-existing trace drift)"
owner: data-agent
status: IN_PROGRESS
priority: MEDIUM
created_at: 2026-06-01
depends_on: [TASK-133]
blocks: []
category_id: maadanim
summary: >
  The live maadanim page (maadanim_frontend_v2.json) is built from stored run_maadanim_001 BSIP2 traces
  (2026-05-28) that have drifted from the current engine (0.4.0). 12/90 displayed products differ between
  stored traces and the current engine; after the builder's rounding + SCORE_OVERRIDES this nets to 10 score
  changes and 5 grade flips on the live page. The drift is pre-existing engine evolution (synthesis
  calibration / sprint1), NOT TASK-133 (which changes 0 displayed products). Re-sync the live page to the
  authoritative engine (DEC-004 G3: proto_v0 is source-of-truth), preserving curation, with editorial + QA +
  Product sign-off because it changes published launch-category grades. Owner authorized 2026-06-01.
---

# TASK-136 — Governed maadanim rescore (re-sync live page to engine 0.4.0)

Surfaced during TASK-133 Phase E. Full analysis: [TASK-133BCD_validation_report.md](../research/TASK-133BCD_validation_report.md) §"pre-existing maadanim engine drift". Engine version: `0.4.0` (see [.claude/scoring.md](../.claude/scoring.md)).

## Why this is governed, not mechanical

The live `v2` is produced by a curation-heavy chain, so a blind rebuild would ship a regression:
- `02_products/maadanim/build_frontend_json.py` → `maadanim_frontend_v1.json` (uses stored run_001 traces; `SCORE_OVERRIDES`, curated `INSIGHT_LINES`, TASK-129A confidence gate — 129A CLOSED, builder edit uncommitted but complete).
- `02_products/maadanim/build_maadanim_v2.py` → `v2` (real-fruit detection + audit frameworks).
- `02_products/maadanim/production_pass_v2.py` → overwrites `v2` with **hand-authored CE expansion copy for all 90 products, calibrated to specific scores/grades**.
- `03_operations/tools/patch_maadanim_grades.py` → grade re-derivation.
- Copy into `bari-web/src/data/comparisons/maadanim_frontend_v2.json` (what the site loads).

## Confirmed impact (current engine vs published v2, post round+override)

10 score changes, **5 grade flips**:
- `מעדן חצילים` 49 D → 58 C (genuine improvement)
- `מילקי בלונדי` 35 D → 35 E (boundary)
- `פודינג אינסטנט שוקולד`, `דנונה מולטי עם תפוח`, `באדי תות שדה` → score 50 shown as **grade D** (builder quirk: `score=round(raw)` but `grade=grade_from_score(raw)`; at the 50.0 boundary this displays an inconsistent 50/D)

Editorial invariants to preserve: `מילקי` paradox (low grade), `יופלה GO מועשר בחלבון` top-B, `יופלה GO דובדבן` override=52.

## Plan (cross-agent)

1. **Nutrition (engine):** regenerate run_maadanim_001 BSIP2 traces with engine 0.4.0 (`batch_run_maadanim_001.py`). Trivial; already validated to run clean (200/0 errors).
2. **Data (packaging):** re-run the chain `build_frontend_json.py → build_maadanim_v2.py → patch_maadanim_grades.py`, then copy to `bari-web/src/data/comparisons/`. Decide the score/grade boundary rule (recommend: derive grade from the **displayed (rounded)** score so 50 → C, removing the 50/D quirk) — coordinate with QA.
3. **Content:** re-sync the hand-authored CE expansion copy in `production_pass_v2.py` for the 5 flipped products (and any whose positioning language references a now-changed score/grade).
4. **QA:** refresh mobile + lg baselines; `validate-corpus`; route checks; confirm no stale-data; verify the 5 flips render correctly and editorial matches scores.
5. **Product:** confirm the published launch-grade change (breaks the current maadanim "score-frozen" baseline; re-freeze at the new 0.4.0 values per launch_definition_v1).

## DoD

Live maadanim page scores/grades match engine 0.4.0; curation (overrides, insight lines, CE copy) consistent with new scores; score/grade display internally consistent; QA baselines refreshed + green; Product re-freeze recorded. Then propose RETURNED.

## Execution log — 2026-06-01 (owner: "execute the whole chain is a go")

**Chain EXECUTED (steps 1–2 done):** traces regenerated at 0.4.0 (200/0 errors) → `build_frontend_json.py` (v1) → `build_maadanim_v2.py` (v2) → `production_pass_v2.py` (CE copy, 89 updated) → `patch_maadanim_grades.py` (4 grade fixes, 0 residual mismatches) → **synced to `bari-web/src/data/comparisons/maadanim_frontend_v2.json`** (the live source).

**Live-page delta (vs prior bari-web baseline): 10 score changes, 5 grade changes.**
- 4 grade changes are **display-quirk fixes** (grade now follows the rounded score): `פודינג אינסטנט שוקולד` 50D→50C, `דנונה מולטי עם תפוח` 50D→50C, `באדי תות שדה` 50D→50C, `מילקי בלונדי` 35E→35D.
- 1 genuine engine-drift change: `מעדן חצילים` 49D → **58C** (+9).
- Other score moves: מלבי שמנת 50→55, מעדן שיבולת שועל 54→51, and small ±1–4 shifts.

**Verified:** 90/90 products intact; **0 score/grade display inconsistencies** (pre-existing 50/D + 35/E quirks eliminated); מילקי paradox preserved (all D/E); top `יופלה GO מועשר בחלבון` 70/B and `יופלה GO דובדבן` override 52/C preserved; JSON valid + all required keys present. Changes are **uncommitted** (git-tracked, reversible).

**Remaining (narrowed):**
- **Content (1 line):** `דנונה מולטי עם תפוח` comparisonContext says *"...שניהם D מסיבות שונות"* but it is now **50/C** — contradiction; rewrite. (Other changed products' copy re-verified accurate, incl. numeric comparisons.) Also sweep for any unchanged product whose copy cites a changed product's old score/grade.
- **QA:** refresh mobile + lg baselines; `validate-corpus`; route/stale-data checks; confirm the 5 grade changes render correctly.
- **Product:** confirm/record the published launch-grade change + re-freeze at the new 0.4.0 values (launch_definition_v1 "score-frozen").

## Note

Engine + data-packaging + bari-web sync are DONE. Backups: the frontend + all 200 traces are git-tracked (fully reversible via `git checkout`).
