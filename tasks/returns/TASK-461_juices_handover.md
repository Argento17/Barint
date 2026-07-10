# TASK-461 HANDOVER #8 → git-owning sibling lane (juices copy overhaul, Phase-2 #6)

**From:** description-overhaul session (no-commit ruling). **Status: TWO-GATE SIGNED OFF — ready to
commit.** Same protocol as the previous seven, with ONE documented scope exception (below).

## The artifact
- **`C:\Bari\tasks\returns\TASK-461_juices_copy_overhaul.json`**
  sha256 `9ba0dbcab35dc36774c6116f90befee85eb23c5002a64c4af5a66fba0ccc3ad9`
- Replaces: `bari-web/src/data/comparisons/juices_frontend_v3.json`
- Baseline: **origin/master blob `95c42010…`** (17 products, post-de-anchor).

## ⚠️ SCOPE EXCEPTION (orchestrator-authorized, QA-re-verified — the diff is NOT two-fields-only here)
Changed surface = **36 leaves**: 34 = insightLine+rowVerdict ×17 (standard) **+ 2 =
`expansion.comparisonContext` on jc-021 and jc-024**. Reason: those two expansion texts leaked raw
score literals ("35.3"/"35.4") and asserted a stale pre-de-anchor ordering — after the verdict fix,
each card would have CONTRADICTED ITSELF on screen. Fix was minimal-edit (openings replaced, tails
byte-preserved — QA verified new_opening + old_tail == new_text), score literals regex-swept to 0,
tie framing aligned with the rowVerdicts. QA ruled the residual pre-existing tail text shippable.
Everything else (scores/grades/ranks/nutrition/_meta) byte-identical — zero score movement.

## Verification already done
1. Field isolation: 36/36 changed leaves within the authorized surface, verified ×3 (author,
   orchestrator leaf-walk, QA full-tree diff); QA additionally diffed post-fix vs its own gated
   pre-fix copy: exactly 4 leaves changed by the fix pass.
2. **Adversarial QA (Opus): initial GO_WITH_FIXES (0C/2H/3M) → all 3 mandated fixes applied →
   targeted re-check GO (0 open CRITICAL/HIGH).** Final report `TASK-461_juices_QA_report.md`
   (this dir, sha 05b19ba5…). Six-way A-tie honest; sugar/kcal/additive extremes verified; no
   health-halo on any 100%-juice product; diet product explicitly anti-haloed.
3. **THREE live truth defects fixed (PR-body material):** two verdicts described the pre-de-anchor
   trio ordering (stale since sweep PR #35); one leaked literal engine scores into consumer copy;
   one self-contradicted on its own ingredient count.
4. Hygiene: em dashes 38→0 in the copy fields, engine vocab 0, openings 34/34 unique, panel numbers
   4/17 justified extremes (+1 kcal anchor on a missing-sugar label).

## Git steps
1. Verify sha256 → swap file in worktree off origin/master → run_gates G1–G8 (`--baseline`
   origin/master) → tsc/build → branch `content/task461-juices-copy-overhaul` → push origin →
   owner PR (PR body should mention the scope exception + the score-literal leak fix). Copy the QA
   report to `02_products/juices/reports/red_team_juices_<date>.md` in the commit.
2. Tick board (TASK-461 Phase-2 #6).

## Routed follow-ups (NOT blockers)
- **→ data-agent:** corrupted parse tails jc-019 ("אססולאם קי") / jc-025 / jc-023 (no copy leans on
  them, QA-verified).
- **→ pending expansion pass (accumulating list):** choctab "רק C" (ct-001/002), bread r16/r20
  stale comparisonContext, juices residual old-style tails on jc-021/jc-024 (now coherent but
  old-register). One dedicated expansion-copy pass across categories would clear all of these.
- **→ TASK-453 backlog:** hebrew_readability decimal false-positives (recurring class).
