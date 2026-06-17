# P158 / TASK-298 (retry 1) — Fix rescore_all.py: per-shelf shelf-relative setup + idempotency (route: C1-GROK)

Repo: C:\Bari. Branch: task-275-engine-fixes-abc. Full repo access. Read `tasks/TASK-298.md` + your prior
`tasks/returns/P157_return.md`.

## Why this is a retry (the defect)
Your `rescore_all.py` runs and passes gates, but it **re-scores WRONG**: it scores every product with default flags and
**never sets shelf-relative stats**. The orchestrator verified: re-scored brined differs from the committed
`run_brined_005` traces (which reproduce the live GOLDEN page) on **46/48 products, deltas to −17.9** — the shelf-relative
sodium credit (EV-056) is missing. `score==trace` is NOT sufficient — it only proves the page matches its own (wrong) traces.

## The canonical CORRECT pattern (study these — they are the source of truth)
- `03_operations/bsip2/proto_v0/src/batch_run_shelfrel_golive_001.py` — the multi-category go-live re-score. Note per
  category: `set_shelf_stats(nutrient, median, scale, "iqr")` with FROZEN params from `constants.py`, the specific
  env flags (L30-37: `BARI_RECAL_P0=on`, `BARI_SODIUM_SHELF_RELATIVE_V1=off` because it's brined-only, etc.), the
  `score_one()` chain (L79-88), `clear_shelf_stats` after each, the **C10 milk invariant** guard (L91-125), and
  `corpus_filter` (cakes, L312). Nutrient per shelf: cereals=sugars_g, hard_cheeses=fat_saturated_g, juices=sugars_g,
  hummus=sodium_mg, cakes=sugars_g.
- `batch_run_brined_cheeses_005.py` — brined uses its OWN path: `BARI_SODIUM_SHELF_RELATIVE_V1=on` + EV-056 sodium stats.
  Read it for brined's exact flags + median/scale.
- `batch_run_cookies_005_shelfrel_pilot.py` — cookies_coffee sugar shelf-rel params.
- `constants.py` — all the frozen `*_SHELF_REL_*_MEDIAN`/`*_SCALE` values.
- For **granola** and **snacks** (snack bars): determine whether they are shelf-relative enrolled at all (check for a
  batch runner / constants entry). If a shelf is NOT enrolled, scoring it with no shelf stats is correct FOR IT — the
  idempotency test (below) will confirm.

## The fix (two parts)
1. **Declare per-shelf scoring metadata** (so the trigger stays ONE generic path, no per-shelf Python branches). Add a
   `"scoring"` block to each `03_operations/page_generator/configs/<shelf>.json`, e.g.:
   ```
   "scoring": {
     "flags": {"BARI_SHELF_RELATIVE_V1":"on","BARI_FAT_TECH_V1":"on","BARI_RECAL_P0":"on", ...},
     "shelf_rel": {"nutrient":"sugars_g","median":<frozen>,"scale":<frozen>,"scale_type":"iqr"},  // null if not enrolled
     "bsip1_dir": "<the BSIP1 corpus dir the real runner used>",
     "corpus_filter": "<path to corpus_filter.json or null>"
   }
   ```
   Pull the EXACT frozen values from the canonical runners + constants.py. brined's block uses its own sodium flag/path.
2. **Rewrite `rescore_all.py`** to be ONE generic loop that, per shelf: applies `scoring.flags` (os.environ),
   `set_shelf_stats(...)` from `scoring.shelf_rel` (skip if null), applies `corpus_filter` if present, scores via the
   `score_one()` chain, `clear_shelf_stats` after, runs the **C10 milk-invariant guard** (milk delta must be 0 — CRITICAL
   STOP if not), then `generate_page` → staging. No per-shelf `if` branches in code — all difference lives in config.

## ACCEPTANCE TEST (this is the gate, not score==trace)
Run under TODAY's engine: each shelf's re-scored page MUST **reproduce the current live page** (`config.baseline_json`):
**0 grade moves** and score moves only from float-vs-rounded display. Print per shelf: products, score-moves(rounded),
grade-moves, reproduces-live? (YES/NO). A shelf that does NOT reproduce live is either (a) a remaining trigger bug — fix it,
or (b) a genuine finding (the live page wasn't produced by the current engine) — report it, don't force. Target: all
shelves reproduce live. (This proves the trigger faithfully replicates real scoring; only then is it a trustworthy flip-switch.)

## Boundaries
- Output to `_rescore_staging/` only. NEVER overwrite live (`bari-web/`) or the live `bsip2_outputs` run dirs. No engine edits.
- OFF ban (TASK-238): 0 OFF; any OFF marker fails that shelf.
- Deterministic (fixed `--timestamp 2026-06-16T00:00:00Z`). No commit, no deploy.
- Clean up the stray `agent-tools/` dir if your tooling created it.

## Return
- The per-shelf ACCEPTANCE table (products · score-moves · grade-moves · reproduces-live?) from an actual run + wall-clock.
- The `scoring` block you wrote per shelf (nutrient/median/scale/flags) + the canonical source you took each from.
- C10 milk result per shelf.
- Any shelf not reproducing live → finding with root cause.
- Do NOT close — propose RETURNED. End with the return contract JSON (`01_framework/operations/return_contract_v1.md`):
  `task`, `proposed_status`, `artifacts[]` (path+action+sha256), `counts{}` (trace-derived + command), `commands_run[]`, `not_done[]`, `self_check`.
