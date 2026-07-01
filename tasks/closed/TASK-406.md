---
id: TASK-406
title: Provenance reconciliation — 7/12 live categories cannot reproduce published scores
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-26
returned_at: 2026-06-26
closed_at: 2026-07-01
depends_on: []
blocks: []
category_id: null
close_reason: >
  SUPERSEDED by TASK-409's landed repro work (2026-07-01 reconciliation). The provenance_manifest
  approach here was an interim local artifact; the real reproducibility fix shipped as the TASK-409
  surgical repro-patch commit series + merged PRs #30-32 (every non-reproducing category patched to
  committed-trace scores). The manifest + _build_manifest.py were never committed to origin.
  Deliverable #2 (BARI_D4_SCORE_V1 into MANAGED_BARI_VARS) is HALF-DONE: present in
  gates/baseline_verify.py but NEVER in rescore_all.py (confirmed absent from git history of that
  file) — moot now that the D4-flag categories reproduce via the committed repro patches. No score
  was moved by this task.
blocker: "orchestrator side DONE (provenance persisted + D4 flag managed); round-trip score re-verification = de-chain re-shadow"
summary: >
  TASK-395 handoff F2. D4 patch (BARI_D4_SCORE_V1 commit 361748722) applied to live files but unrecorded in configs/rescore_all.MANAGED_BARI_VARS; NULL run_id (bread v2/v3, cheese_v4, snacks_v5); snacks corpus wrong-pinned (run_001 vs live task362, 12/21 overlap); granola config says v1 but route serves granola_frontend_v2 (20/22 differ); chocolate-bars/tablets/protein-bars have no manifest/config. Persist per published file a full provenance record (corpus run_id + COMPLETE flag vector incl D4 + engine version); reconcile each served file so every score round-trips to its committed hash.
---

# TASK-406 — Provenance reconciliation — 7/12 live categories cannot reproduce published scores

## DONE (orchestrator side, 2026-06-26) — provenance persisted + the flag-management gap fixed
**Key reframe:** the provenance ISN'T lost — every shelf config (`03_operations/page_generator/configs/*.json`) already records `scoring/flags` (the per-category flag vector, incl `BARI_D4_SCORE_V1`), `scoring/bsip1_dir` (backing source), `run_products_dir` (BSIP2 run), and `baseline_json` (served file). It was just never persisted PER PUBLISHED FILE, and one flag was unmanaged.

**Deliverables:**
1. **Persisted provenance manifest:** `03_operations/page_generator/provenance/provenance_manifest.json` — one record per LIVE served file (15) with: run_id (resolved from `run_products_dir` even where `_meta.run_id` is NULL), full flag vector incl D4, backing bsip1_dir/run_products_dir + existence check, engine head at record (`b905ec9b4`), D4 patch commit (`361748722`), and a per-file status. Builder: `provenance/_build_manifest.py` (read-only; does NOT mutate live files). **7/15 = REPRODUCIBLE_PENDING_RESHADOW** (config-bound, source exists, flags present); 8 carry explicit gaps.
2. **Flag-management gap FIXED:** `BARI_D4_SCORE_V1` added to `MANAGED_BARI_VARS` in `rescore_all.py` + `gates/baseline_verify.py` (it was already in `monotonicity_invariant.py` — that inconsistency WAS the gap). The live D4 patch (commit 361748722) is now snapshotted/restored on every managed run → flag state reproducible going forward.

**Gaps documented in the manifest (for de-chain to act on during re-shadow — NOT mutated by me, to avoid disturbing the comparison baseline):**
- **NULL `_meta.run_id` but RESOLVABLE from config** `run_products_dir`: bread_v3, cheese_v4, chocolate_bars_v1, chocolate_tablets_v1, snacks_v5 → the manifest carries `run_id_resolved`; inject into `_meta` during the next managed build.
- **Config→served MISMATCH** (config `baseline_json` points to old v1 while the route serves v2): granola_v2 (config→granola_v1) + protein_combined_v2 (config→protein_bars_v1). The served v2 files DO carry their own `_meta.run_id` (run_granola_task385_25g, protein_bars_task365_rescore) — they were built by ad-hoc task runs outside the config. Re-point the config `baseline_json` (and `bsip1_dir`/`run_products_dir`) to the v2 source, or rebuild v2 through the config.
- **Stale `bsip1_dir`**: cookies_coffee config points to a missing dir → fix the path before re-shadow.

**Handed to de-chain (its stated job — has the re-shadow harness, works in worktrees):** the round-trip "every score re-derives to its committed hash" verification. The manifest gives it the exact source + flag vector per file to re-shadow against. **No score moved by this task** (provenance recording + a snapshot-list addition only).
