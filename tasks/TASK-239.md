---
id: TASK-239
title: "BSIP0 Structural Parser + Exit Gate — kill the manual-JSON-patch loop (frozen-veg dual-table bug)"
owner: data-agent
reviewers: [qa-agent, nutrition-agent]
status: CLOSED
close_reason: >
  Structural parser fix + exit gate + 8 regression tests delivered, verified by orchestrator
  at file:line, and landed on salty-snacks-v4 (pending owner commit). 20/20 tests pass on the
  working branch. Per-100g selection live-proven on real Dorot ginger fixture (basis=per_100g,
  competing=2; 77 kcal/12 mg = the hand-patched values, with no patch); "never silent first-pick"
  guarantee confirmed in code (bsip0_nutrition.py:223-259). 01/02/03 now route through the shared
  parser (3 inline extractions removed). [:50] dev cap replaced with BSIP0_SCRAPE_LIMIT env. OFF
  gate (05_bsip0_gate.py) hard-fails all 9 variants; frozen-veg corpus clean. The "no new BSIP0
  run until resolved" rule is now lifted. Frozen-veg DATA re-run owner-deferred ("Not yet",
  2026-06-10) → tracked in TASK-240 with the MEDIUM follow-ups. Verdict: PASS WITH FIXES.
closed_at: 2026-06-10
priority: HIGH
created_at: 2026-06-10
depends_on: [TASK-238]
relates_to: [TASK-235, TASK-238]
roadmap_impact: true
work_type: pipeline-structural-fix
mode: BLOCKER / HARSH VERIFICATION
opened_note: >
  Requested as "TASK-237" by reviewer (nutrition-agent), but TASK-237 was already
  taken (salty-snacks OFF re-source, IN_PROGRESS) and TASK-238 is the project-wide
  OFF ban. Renumbered to TASK-239 per Registry-First rule to avoid clobbering.
  The OFF-contamination gate (deliverable #6) is the BSIP0-level implementation of
  TASK-238's ban; this task is broader (structural nutrition parser + exit gate).
---

# TASK-239 — BSIP0 Structural Parser + Exit Gate

## Why
Repeated BSIP0→BSIP1→BSIP2→web failure loop. Frozen vegetables exposed a structural
parser bug fixed by **manual JSON patching** — the scraper/parser path can reproduce the
same bug on the next run. Manual JSON patching is not a fix. A page that builds is not
proof the source data is valid. Goal: convert the reported defects into **structural gates
and regression tests** so the bug cannot recur on the next category run.

## Pre-dispatch verification (orchestrator, 2026-06-10) — CONFIRMED before fixing
- **#2 bypass shared parser — CONFIRMED.** `01/02/03` in `shufersal_frozen_vegetables/` do
  NOT import `_shared/bsip0_nutrition.py`; three separate inline extractions.
- **#1 first-table selection — CONFIRMED.** `01:208` and `02:227` use
  `soup.find("div", class_="nutritionList")` (first match only, var `first_nutrition_list`),
  no per-100g preference.
- **#7 50-product dev limit — CONFIRMED.** `01:180` `list(scope_in.items())[:50]  # limit to 50 for now`.
- **OFF in frozen-veg dir — clean** on first pass (to be re-verified by full gate scan).

## Definition of Done (deliverables)
- [ ] `reports/task_239_bsip0_parser_gate_audit.md` — evidence table (finding_id, claim,
      confirmed/refuted/partial, file, line/function, severity, can-affect-future-runs, fix)
- [ ] `_shared/bsip0_nutrition.py`: multi-table handling under `div.nutritionList`; explicitly
      prefer the `ל-100 גרם` / per-100g table; record `selected_basis`, `selected_table_index`,
      `selected_table_header`, `competing_table_count`; **never silently pick first** — return
      insufficient/gate-fail when per-100g unidentifiable (unless explicitly waived)
- [ ] `01/02/03` frozen-veg scripts refactored to call the shared parser; offline re-extraction
      uses the **same** parser as live scraping
- [ ] Regression fixtures + tests: Dorot dual-table (ginger) fixture proves per-cube NOT selected
      when per-100g exists, `selected_basis = per_100g`, values match per-100g table; + one normal
      single-table fixture still parses
- [ ] BSIP0 exit gate (`05_bsip0_gate.py` or wired into `04_scope_cleanup_v3.py`) running before
      BSIP1/BSIP2: duplicate-barcode, conflicting-identity, selected_basis, multi-table detection,
      numeric sanity, ingredient coverage, ingredients_raw_source presence/reason, image
      reachability, source provenance, run-summary contract, **OFF contamination hard-fail**
- [ ] OFF gate proof: hard-fail on all listed variants across source/fallback/enrichment/image/
      barcode/name/nutrition/ingredients/validation/cache/trace. Unknown OK; OFF not OK.
- [ ] Scope: document the 4 drifted scope layers + whether they changed frozen-veg in/out +
      recommend (do NOT build full scope-standardization unless cheap/safe)
- [ ] `ingredients_raw_source` preserved for offline re-parse, or registered as follow-up
- [ ] BSIP0 gate sample output + before/after proof on Dorot ginger fixture
- [ ] Final verdict: PASS / PASS WITH FIXES / FAIL

## Hard rules
- No scoring-methodology change. No manual JSON patch as the fix. No new BSIP0 category run
  until structural parser/gate resolved. No OFF for anything. No broad ScraperBase rewrite
  unless separately approved. Not "fixed" unless tests prove the bug cannot recur. "Build
  passed" is not evidence of data correctness.

## Lifecycle
data-agent executes + proposes verdict; qa-agent verifies recurrence-proof + gate; nutrition-agent
reviews parser/basis correctness. Orchestrator closes only after verifying claims at file:line.

## Orchestrator verification (2026-06-10) — data-agent verdict PASS WITH FIXES
Work delivered in worktree `agent-aed81e287380bd262` (branch `worktree-agent-aed81e287380bd262`).
Claims independently verified at file:line:
- 20/20 tests pass (`_shared/test_bsip0_nutrition.py`).
- Per-100g selection live-proven on real fixture `dorot_ginger_dual_table.html`:
  `selected_basis=per_100g, index=0, competing_table_count=2`. "Never silent first-pick"
  confirmed in code: `bsip0_nutrition.py:223-259` → multi-table w/ no per-100g = `insufficient`.
- `01/02/03` all route through `bn.extract_nutrition_raw` (inline extractions removed).
- `[:50]` cap → `BSIP0_SCRAPE_LIMIT` env (default 0 = unlimited), `01:185-190`.
- OFF gate real: `05_bsip0_gate.py` has `gate_off_contamination`/`OFF_TOKENS`/`_OFF_BARE_RE`;
  frozen-veg corpus G1 PASS (clean). #8 refuted (dir was already clean); gate now enforces.
- Before/after: structural parser yields 77 kcal / 12 mg per-100g = exactly the hand-patched
  values; pipeline previously produced 6 kcal / 1 mg per-cube. Manual patch was correct AND
  the structural fix reproduces it without a patch.

**Verification confidence: structural fix is sound and recurrence-proof.** Two items remain
before CLOSED:
1. Worktree branch must be merged to the working branch (git op — owner go-ahead, changes branch).
2. Published frozen-veg v3 data is still the MANUAL PATCH; gated re-run (now unblocked) needed to
   regenerate it from the fixed scraper. Re-run moves published frozen-veg data (relates_to
   TASK-235, Phase 1 locked) → consumer-facing, needs green light.

Registered follow-ups (not blockers): #6 `ingredients_raw_source` (MEDIUM), #3 scope
consolidation (MEDIUM), other-retailer scraper migration to shared parser (MEDIUM).

## Worktree quarantine (owner directive, 2026-06-10)
Original data-agent worktree retained for forensic reference only; not mergeable due unrelated
commits. Branch `worktree-agent-aed81e287380bd262` (worktree
`C:\Bari\.claude\worktrees\agent-aed81e287380bd262`) is REFERENCE-ONLY / CONTAMINATED:
- do NOT merge the branch
- do NOT push it
- do NOT cherry-pick wholesale
- do NOT use it as launch evidence
- inspect only for forensic context

**Authoritative TASK-239 implementation = the clean transferred diff on `salty-snacks-v4`:**
shared parser per-100g selection · frozen-veg scraper refactor · `05_bsip0_gate.py` · OFF
hard-fail · regression fixtures/tests · audit report. (Worktree's TASK-239 edits were
uncommitted and the branch carries 6 unrelated commits — that is why it is not mergeable.)
