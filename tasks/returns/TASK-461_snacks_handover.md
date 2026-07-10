# TASK-461 HANDOVER #5 → git-owning sibling lane (snacks copy overhaul, Phase-2 #5)

**From:** description-overhaul session (no-commit ruling). **Status: TWO-GATE SIGNED OFF — ready to
commit.** Same protocol as brined (live), cheese (#2), cookies (#3), choc-tablets (#4).

## The artifact
- **`C:\Bari\tasks\returns\TASK-461_snacks_copy_overhaul.json`**
  sha256 `406d8363e40aa2d7473881b152b98ddd2fff16268c9622ee4d770530b5e968a8`
- Replaces: `bari-web/src/data/comparisons/snacks_frontend_v5.json`
- Baseline: **origin/master blob `4febff7b…`** (21 products).

## Verification already done
1. **Field isolation ×3:** 21/21 only {insightLine, rowVerdict}; everything else byte-identical.
2. **Adversarial QA (Opus): GO_WITH_FIXES — 0 CRITICAL / 0 HIGH / 3 MEDIUM, ALL advisory (no rework
   needed; two soft superlatives ruled defensible as written).** Report `TASK-461_snacks_QA_report.md`
   (this dir, sha 1daa459a…). Truth audit 21/21 TRUE incl. every name-vs-content exposure (honey 3%,
   maple 2%, dried fruit 1%+1%, chocolate-share claims), Shaked-Tavor trio satFat ordering, dual
   records, sodium/satFat/fiber extremes. No copy leans on the flagged data defects.
3. **QA already ran run_gates G1–G8 on the candidate:** G4/G6/G7/G8 PASS (G7 parity: 0 grade changes);
   **G1 fail-set byte-identical to live baseline (diff empty) = pre-existing TASK-453 schema debt,
   nothing introduced**; G2/G3/G5 WARN only for missing --run/--corpus (copy-only change). Re-run in
   the worktree if your protocol requires, expect identical results.
4. Hygiene: em dashes 55→0, engine vocab 0, hebrew_readability 42/42 clean, openings 42/42 unique,
   panel numbers 4/21 (fiber-max 23g, protein-max 14g + kcal-max 540, sodium-max 416mg, satFat-max 18g).

## Git steps
1. Verify sha256 → swap file in worktree off origin/master → gates/build → branch
   `content/task461-snacks-copy-overhaul` → push origin → owner PR. Copy the QA report to
   `02_products/snacks/reports/red_team_snacks_<date>.md` (or category report dir) in the commit.
2. Tick board (TASK-461 Phase-2 #5).

## Routed follow-ups (NOT blockers)
- **→ data-agent:** snk-018 sodium 0.2mg = suspect unit error + fiber NULL; snk-014/016 ingredient
  tails corrupted to "????" (copy claims sit on the intact head, QA-verified); stray parse chars
  snk-010/013.
- **→ TASK-453 backlog:** G1 schema debt (same pre-existing set as pilot/other categories).
