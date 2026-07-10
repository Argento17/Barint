# TASK-461 HANDOVER → git-owning sibling lane (brined-cheeses copy overhaul, pilot)

**From:** description-overhaul session (owner ruling 2026-07-02: that session commits NOTHING; all git
writes belong to this lane). **Status: TWO-GATE SIGNED OFF — ready to commit.**

## What this is
Full re-authoring of `insightLine` + `rowVerdict` (Hebrew) for all 36 products of the brined-cheeses
comparison page, per owner directive (TASK-461): replace robotic data-recitation with the engine's
opinion, cereals-golden voice. Program spec + verified dispatch log: `C:\Bari\tasks\TASK-461.md`.

## The artifact
- **`C:\Bari\tasks\returns\TASK-461_brined_v2_copy_overhaul.json`**
  sha256 `9ba7fc112fd43230aff032fe2aed986ecc117a755eaab6197c89a43f5886fe62`
- Target file it replaces: `bari-web/src/data/comparisons/brined_cheeses_frontend_v2.json`
- **Baseline it was built on: origin/master** (post TASK-449 #38 + sweep #35). NOT the local
  working-tree copy (993 lines stale). QA independently fetched origin/master (blob content sha256
  `583db150…`) and confirmed the candidate differs from it ONLY in the two copy fields.

## Verification already done (both gates + orchestrator, all independent)
1. **Field isolation (verified 3×: author, orchestrator, QA — each with own scripts):** 36/36 products
   changed on exactly {insightLine, rowVerdict}; `_meta`, `_hash_no_rank`, scores, grades, ranks,
   nutrition, ingredients, additives byte-identical to origin/master. Zero score movement by construction.
2. **Content gate (author lane, Sonnet):** report `TASK-461_author_report.md` (this dir) — 60-row
   superlative rank-check, number-kept justifications, before/after samples.
3. **Adversarial QA gate (Opus, independent): VERDICT GO — 0 CRITICAL / 0 HIGH / 3 MEDIUM
   (observational, none blocking).** Report `TASK-461_QA_report.md` (this dir). Claim-by-claim truth
   audit vs independently built rank tables (30/30 hotspot claims TRUE); hebrew_readability leakage
   gate 72/72 clean; em dashes 0; banned engine vocab 0; OFF refs 0; partial-panel disclosure 3/3.
4. Copy metrics old→new: em dashes 74→0; engine-mechanic vocab 44→0; products reciting panel numbers
   36→4 (each a verified shelf extreme); opening-template repetition eliminated (36/36 unique).

## ⚠️ Bonus truth fix (worth a line in the PR body)
Production copy on **bc-035 (בולגרית מעודנת 24%) falsely claims "14 גרם שומן על התווית" — its panel
says 24.0g** (the 14g belongs to bc-017). The artifact corrects this consumer-facing factual error.

## What this lane asks you to do (the git steps)
1. Verify the artifact sha256 matches the value above.
2. In your worktree off origin/master: overwrite
   `bari-web/src/data/comparisons/brined_cheeses_frontend_v2.json` with the artifact.
3. Run `run_gates.py` G1–G8 with `--baseline` = the origin/master copy (never `C:\Bari`'s), plus your
   usual build oracle (tsc + build). Known posture: G1 SCHEMA debt + hebrew_readability decimal
   false-positives are PRE-EXISTING category-wide (TASK-453 backlog), byte-identical on live — not
   introduced here.
4. Commit on branch `content/task461-brined-copy-overhaul`, push to **origin (Argento17/Barint)** only,
   owner PR (tripwire #2 — owner clicks merge; Vercel auto-deploys).
5. Tick `DISPATCH_BOARD.md` with the TASK-461 line (that session deferred all board writes to you to
   avoid working-tree collisions).
6. On merge, update `C:\Bari\tasks\TASK-461.md`: mark the pilot shipped (task stays IN_PROGRESS —
   Phase-2 fan-out across the other 15 categories is scoped in `TASK-461_fanout_audit.md`, this dir,
   pending owner acceptance of the pilot pattern).

## Also delivered (no action needed now)
- `TASK-461_fanout_audit.md` — copy-badness ranking of all 16 live categories off origin/master
  (fan-out order: cheese_v5 → cookies_coffee → chocolate_tablets → hummus → …; milk/cereals excluded).
  Includes one live defect OUTSIDE this artifact: **hard_cheeses rowVerdict leaks a literal score
  ("67 נקודות")** — fold into that category's pass or an earlier hotfix.
