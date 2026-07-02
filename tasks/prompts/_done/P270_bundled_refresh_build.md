# P270 / TASK-418 bundled refresh build — HC+cheese+cereals score patch + audit pack (route: C1)

## 0. Environment / isolation
- Isolated worktree **C:\bari_p270** ONLY (off master 7733065a). No git ops (no stash/checkout/commit). Single
  synchronous worker. Nothing here deploys.
- Scoring engine: `03_operations/bsip2/proto_v0/src`. Proven HC harness + doc:
  `03_operations/page_generator/provenance/hard_cheeses_reproduce_harness.py` +
  `hard_cheeses_canonical_invocation_v1.md`. Verified HC movement table (from P268) is at
  `C:\bari_p268\tasks\returns\P268_movement_table.json` — READ it (do not recompute HC from scratch; re-verify
  a couple rows with the harness).

## 1. Scope (owner ruling 2026-07-01: GO, bundle HC with the TASK-405 set — juices CARVED OUT to TASK-430)
Refresh three live categories to their current-correct scores. **JUICES IS EXCLUDED** (baseline
non-reproducible + downward drift, unexplained → TASK-430). Categories + baselines:
- `hard_cheeses` → `bari-web/src/data/comparisons/hard_cheeses_frontend_v4.json` — 8 pollution-clean moves
  (verified P268): UP 4137311 70.8→76.8, 7290014760448 65.9→71.9, 7290014760912 65.0→67.0; grade-UP
  4122270 62.6→67.0 (C→B), 7290110320850 62.6→67.0 (C→B); DOWN 5384356 74.6→67.0, 9150162 72.2→67.0,
  7290116931524 70.2→67.0. Mechanism verified (EV-104 ceiling restored after pollution removed).
- `cheese` → `cheese_frontend_v4.json` — TASK-405 upward de-pollution drift (P268 drift_rows, 20 products
  incl. 2 grade-UP: 3523230065467 63.8→68.0 C→B, 7290019635581 32.8→37.0 E→D). Many are ≤2pt noise.
- `cereals` → `cereals_frontend_v2.json` — 2 upward (7290017894911 46→50 D→C grade-UP, 7290017894928 43→47).

## 2. Build method (surgical, deterministic — NOT a full generate_page regen)
generate_page does NOT reproduce HC (loader drops bsip1_enriched) and HC's bespoke builder is gone. So:
1. For each category, RE-DERIVE the current-correct score/grade for every published barcode via the canonical
   invocation (HC: cleaned corpus + TASK-429 canonical; cheese/cereals: their config invocation on the current
   corpus). PROVE the un-moved barcodes still reproduce published exactly (drift 0) — only the identified
   movers may change. If anything else moves, STOP and report (do not patch a surprise).
2. **Surgically patch** only `score` + `grade` (and any derived numeric rank/position that must re-sort) of the
   moved barcodes in a WORKTREE COPY of each frontend JSON. Preserve every other field byte-for-byte. Re-sort
   the product array by score if the category renders sorted, and reindex rank 1..N. Do NOT touch copy text in
   this task.
3. **OFF-ban absolute** (TASK-238). Invent nothing.

## 3. Deliverables (write into the worktree; do NOT deploy)
- Patched worktree copies of the 3 frontend JSONs (scores/grades/rank only).
- **Audit pack** `tasks/returns/P270_audit_pack.json` — the C3-demanded artifact, per moved barcode:
  category, barcode, name, raw scraped ingredient text (HC), cleaned ingredient list, removed spans (HC),
  pub_score/grade → new_score/grade, delta, grade_move, cap_before/cap_after (HC), mechanism tag
  {pollution_ceiling_restored | pollution_penalty_removed | task405_depollution}.
- **Copy-impact list** `tasks/returns/P270_copy_impact.json` — every product whose GRADE changed OR whose
  score-dependent verdict/insightLine/rowVerdict text references the old number or grade standing (so the copy
  two-gate knows exactly what to re-derive). Expect the 5 grade movers + any verdict that cites a moved score.
- A verification script path so the orchestrator can re-run.

## 4. Boundaries
- Read-only on the MAIN tree's published files; all writes are worktree copies. No deploy, no git, no copy edits.
- Do not close. Propose RETURNED. End with the machine-readable return contract
  (`01_framework/operations/return_contract_v1.md`): artifacts w/ sha256, counts w/ named denominators,
  distribution marker on the full-set claim, and list any barcode that FAILED to reproduce as expected.
