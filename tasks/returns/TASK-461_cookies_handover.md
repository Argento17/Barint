# TASK-461 HANDOVER #3 → git-owning sibling lane (cookies/coffee copy overhaul, Phase-2 #2)

**From:** description-overhaul session (no-commit ruling). **Status: TWO-GATE SIGNED OFF — ready to
commit.** Same protocol as brined (PR #44, live) and cheese (handover #2).

## The artifact
- **`C:\Bari\tasks\returns\TASK-461_cookies_coffee_copy_overhaul.json`**
  sha256 `af492d788f0c03494e5d2e76018accc62163bb99481e96bfaa608152a8dceddc`
- Replaces: `bari-web/src/data/comparisons/cookies_coffee_frontend_v2.json`
- Baseline: **origin/master blob `675eac00…`** (117 products — largest live shelf).

## Verification already done
1. **Field isolation ×4** (author, orchestrator, QA original pass, QA re-check — all independent):
   234/234 changed leaves = exactly the two copy fields ×117; `_meta`/`page_copy`/scores/grades/ranks
   byte-identical. Zero score movement by construction. (Known: `page_copy` carries a pre-existing
   stale-count issue from the TASK-460 era — intentionally untouched, out of scope.)
2. **Adversarial QA (Opus): original pass GO_WITH_FIXES (0C/0H/3M) → M1 template-drift fix applied
   (17 products, 13 stamped red-label clauses varied + 4 repetition chains broken) → targeted re-check
   GO (0C/0H/0 new M).** Final report `TASK-461_cookies_QA_report.md` (this dir, sha f58c03b6…) incl.
   the M1 re-check section. Corpus-wide: no 5-gram repeats >2×.
3. **The legal-grade claim CLEARED by QA:** the "ללא תוספת סוכר" Quaker (ck-7290119041350) — its
   scanned list literally contains סוכר + אבקת סוכר and the 23.2g panel corroborates; copy phrases it
   as a hedged scan finding. Defensible as written; underlying data ambiguity routed to Data (below).
4. Hygiene: em dashes 242→0, engine vocab 0, openings 117/117 unique both fields, panel numbers
   6/117 (all verified extremes), OFF 0. Orchestrator stratified read + full read of all 17 reworked.

## ⚠️ THREE live truth-defect fixes riding in (PR-body material)
Production copy today: (1) a D product whose copy claims grade E; (2) a hydrogenated-fat, E-code
product whose copy calls the list "clean, no additives"; (3) an unverifiable "six food colors" count.
All corrected (QA-confirmed).

## Git steps
1. Verify sha256 → swap file in worktree off origin/master → `run_gates.py` G1–G8 (`--baseline` =
   origin/master copy; expect pre-existing G1 schema debt only) → tsc/build → branch
   `content/task461-cookies-copy-overhaul` → push origin → owner PR.
2. QA asks that its report be copied to `02_products/cookies_coffee/reports/red_team_cookies_<date>.md`
   in the commit to satisfy the mechanical challenge-gate check.
3. Tick board (TASK-461 Phase-2 #2).

## Routed follow-ups (NOT blockers — registry notes)
- **→ data-agent (integrity):** (a) 4 products whose panels are per-serving values stored as per-100g
  (ids in QA report §per-serving; their copy deliberately makes no panel-magnitude claims);
  (b) Quaker ck-7290119041350 name-vs-scanned-list sugar ambiguity (copy survives either resolution);
  (c) r4/r70 `verified` confidence chip despite missing fields.
- **→ TASK-453 gate backlog:** hebrew_readability flagged 1 false positive (ingredient % misread);
  plus the תנובה/'נובה' brand false-positive from the cheese pass.
