---
name: milk_rebaseline_run005_task180a
description: Legacy engine re-baseline program (TASK-178 audit + TASK-180) — milk wave done & live on run_005_headpin; snack+bread waves pending; rice carries a do-not-revert override
metadata: 
  node_type: memory
  type: project
  originSessionId: 346019e6-3cc4-4339-8323-105c9db28f4d
---

**The BSIP2 engine drifted unflagged since the May freezes.** TASK-178 audit (CLOSED 2026-06-04) measured it: HEAD reproduces only bread 165/256 (64%, 83 upward grade drifts — the WORST page), milk 13/20, snack 5/53. Root cause: an unconditional/unflagged v2 grade recalibration in `constants.py` (NOVA lift, floors, confidence ceiling) folded in AFTER the freezes; git was init 2026-06-01 (after all freezes) so legacy freezes had no git-pinned engine state. A naive rebuild of any legacy page would silently move published grades.

**TASK-180 = the re-baseline program** (owner-approved 2026-06-04, umbrella owner qa-agent): pin HEAD, then rescore milk→snack→bread, each with owner sign-off + QA freeze. Step 0 done: engine pinned as **git tag `engine-baseline-2026-06-04` (commit f075d9e)** — future drift is now bisectable.

**Milk wave (TASK-180A) — COMPLETE & LIVE:**
- New frozen baseline = **`run_005_headpin`** (supersedes `run_004_recalibrated`, which is retained as history via SUPERSEDED.md). **CLAUDE.md frozen-invariant updated** to point here. Top **85/A trio HELD** (whole 3.4% / natural 4% / goat).
- 3 owner-signed grade moves (all downward, mid/lower shelf): Alpro Choco soy 38.1/D→**34.5/E** (only visible grade flip; first-ever E on the page, label "חלש מאוד" — Content to confirm), Mehadrin 1% 60.2→56.6/C, Müller 49.6→46.5/D. Page reshipped (`bari-web/src/data/milk-comparison.json`), build+lint green.
- **⚠️ RICE OVERRIDE (do not silently revert):** rice drink `8000215204219` shows **52.3/C** live (owner's TASK-169C manual bump, recal raw 55.31 − ~3.0 builder calibration). The frozen run scores it 49.4/D for engine-consistency, but the owner re-confirmed 2026-06-04 the **override WINS**. Any future milk rebuild MUST re-apply rice=52.3/C on top of the run, not overwrite it. Documented in `run_005_headpin/AUTHORITATIVE.md`.

**Pending waves (BLOCKED, awaiting owner go):** TASK-180B snack (5/53 = heavy drift; owner+Nutrition sign off no-A invariant + second-69.5/B ceiling-crowding), TASK-180C bread (worst page; folds in the 4 TASK-169F recal B→A moves; ship gated on owner per-move sign-off). See [[task169_scoring_recal_sprint]], [[decision_authority_matrix]] (frozen-score moves are an owner tripwire).
