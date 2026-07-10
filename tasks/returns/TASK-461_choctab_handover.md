# TASK-461 HANDOVER #4 → git-owning sibling lane (chocolate tablets copy overhaul, Phase-2 #3)

**From:** description-overhaul session (no-commit ruling). **Status: TWO-GATE SIGNED OFF — ready to
commit.** Same protocol as brined (live, PR #44), cheese (#2), cookies (#3).

## The artifact
- **`C:\Bari\tasks\returns\TASK-461_choctab_copy_overhaul.json`**
  sha256 `c03cc84fccd91b8ac8d5e7aecfb55eb6dad2c2d3e57568cf7ac91144172d1236`
- Replaces: `bari-web/src/data/comparisons/chocolate_tablets_frontend_v1.json`
- Baseline: **origin/master blob `45c962fe…`** (the fresh TASK-455 page, 35 products).

## Verification already done
1. **Field isolation ×3 + post-fix re-proof:** 35/35 only {insightLine, rowVerdict}; _meta/
   _hash_no_rank/scores/grades/ranks/**expansion** byte-identical. Zero score movement by construction.
2. **Adversarial QA (Opus): GO_WITH_FIXES (0C/0H/3M) → 2 copy MEDIUMs surgically fixed (ct-024 twin
   over-claim made literally true; ct-030 buy-verb removed) → targeted re-check GO (0/0/0 open).**
   Final report `TASK-461_choctab_QA_report.md` (this dir, sha 94164244…).
3. **TASK-455 guardrails verified:** zero health-halo in 70/70 strings; B-grade darks framed as
   engineered/concentrated indulgence, never healthy; co-leadership (0.7pt tie) kept, no sole-leader
   overclaim; "מריר"-naming callouts grounded (real sub-50% cocoa).
4. Hygiene: em dashes 80→0, engine vocab 0 (**kills the live "פרמטרים" leak in ct-036's copy**),
   openings 70/70 unique, panel numbers 4/35 (verified extremes), OFF 0.

## Git steps
1. Verify sha256 → swap file in worktree off origin/master → run_gates G1–G8 (`--baseline` =
   origin/master copy) → tsc/build → branch `content/task461-choctab-copy-overhaul` → push origin →
   owner PR. Copy the QA report to `02_products/chocolate/reports/red_team_tablets_<date>.md` (or the
   category's report dir) in the commit for the challenge-gate check.
2. Tick board (TASK-461 Phase-2 #3).

## Routed follow-ups (NOT blockers)
- **Pre-existing baseline defect (QA M3): `expansion.comparisonContext` on ct-001/ct-002 still says
  "רק C" while both products are now grade B** (post-TASK-455 upward flips). Expansion fields are
  outside this program's two-field scope — deserves a small dedicated expansion-copy pass (could ride
  any future chocolate commit after its own mini-gate).
- **→ data-agent:** corrupted ingredient parses ct-001/ct-002/ct-016 (no copy claim relies on them,
  QA-verified); ct-019 sodium 0.0 worth an eyeball.
- **Standing fan-out rule (QA ruling, adopted as TASK-461 house rule R4):** descriptive buyer-intent
  framing is OK; "כדאי/שווה" + לקנות/לבחור/לרכוש = recommendation drift, banned.
