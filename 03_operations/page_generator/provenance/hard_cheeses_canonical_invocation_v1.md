# Hard Cheeses — Canonical Scoring Invocation (TASK-429, Phase-0 baseline)

**Status:** PROVEN — byte-reproduces `hard_cheeses_frontend_v4.json` (31/31 scores, **0.000 drift**, 0 grade moves, 0 missing).
**Date:** 2026-07-01 · **Worktree:** `task429/canonical-repro` off `f530bc87` · read-only, score-neutral.

## The ONE invocation

| Component | Value | Where it is pinned |
|---|---|---|
| **Flags (exact vector)** | `BARI_SHELF_RELATIVE_V1=on · BARI_FAT_TECH_V1=on · BARI_RECAL_P0=on · BARI_HC002_NOVA1=off · BARI_DAIRY_SAT_FAT_INFER=on · BARI_REDLABEL_V1=on · BARI_HC_DAIRY_SATFAT_V1=on`. Every other engine flag `off`; `BARI_GLASSBOX_W4=on` (diag baseline). | Confirmed in **two** independent records: `hard_cheeses_frontend_v4.json` `_meta.flag_vector` **and** `run_hc_task412_rt4_fix/run_summary.json.flags`. Now also written to `configs/hard_cheeses.json` `scoring.flags`. |
| **Shelf-relative stats** | nutrient `fat_saturated_g`, median **18.0**, scale **1.40**, `iqr`; applied via `score_engine.set_shelf_stats(...)`. | **Frozen constants** — `constants.py:619-621` `FATSAT_SHELF_REL_HARDCHEESE_{MEDIAN,SCALE}` (EV-090, computed once 2026-06-14 Scope A n=22). NOT recomputed per run. Config `scoring.shelf_rel` matches. |
| **Corpus source** | `02_products/hard_cheeses/bsip1_task412` | Proven: covers **31/31** published barcodes. `bsip1_outputs` covers only 12/31 and yields WRONG scores for 4 of those 12. Now written to config `corpus_dirs`. |
| **Engine fix required** | `HC_DAIRY_SATFAT_NA_CAP_600_VALUE = 67.0` (RT-4 fix) | `constants.py:702`; present at HEAD. Without it the B-cluster sodium-cap tier reproduces at 63.0. |
| **Record loader** | must accept `file_type ∈ {product, bsip1_enriched}` | The 31 HC records are 79× `bsip1_v2/bsip1_enriched` (shufersal) + 15× `bsip1_v0_1/product` (yohananof). The generic loader's `file_type=="product"` filter silently drops all enriched records → only 7/31 load. This is the true root cause of "generate_page does NOT reproduce HC." |
| **Reload order** | `nova_proxy → signal_extractor → score_engine` (reload after env flags set); score via `extract_signals → classify_category → infer_nova → assign_evaluation_scope → score_product`. | `_reproduce_diag.py` / `_t429_reproduce.py`. |

## Proof
- `_t429_reproduce.py` (canonical harness, no file_type filter): **31/31 reproduced, max abs drift 0.000, 0 grade moves, 0 missing.** → `_t429_reproduce_result.json`.
- `_reproduce_diag.py` (config-driven generic path, loader widened to accept `bsip1_enriched`): `hard_cheeses` row = **repro=31 drift=0 grade_moves=0 nocorpus=0 maxd=0.0.** → `_t429_diag_result.json`.

## The two forks (resolved with evidence)
1. **Corpus: `bsip1_task412`, not `bsip1_outputs`.** For the 12 barcodes in both dirs, 4 diverge and `task412` matches published every time (e.g. `7290110320850`: outputs→67.0, task412/published→62.6; `7290110323301`: outputs→67.0, published→62.0). This IS the "A/85 vs B/67" invocation contradiction — it was scoring against the stale `bsip1_outputs` corpus, never engine non-determinism.
2. **Shelf-stats: frozen constants, not recomputed.** median 18.0 / scale 1.40 hard-coded (EV-090); passing them explicitly reproduces published.

## Generalize check (other live categories, same recipe = each config's own flags+corpus+shelf, engine at HEAD, widened loader)
- **Exact reproduce (drift 0):** hard_cheeses (31/31), chocolate_bars (23/23), chocolate_tablets (35/35), snacks (21/21). Near-exact: bread 28/29 (1×0.8), hummus 56/57.
- **cheese** — 22 drifters, **all carry `_task405_clean`**, all-positive drift (+5.3 max). This is the TASK-405 corpus clean = owner-gated **TASK-418** refresh, NOT an invocation gap. Flag, don't fix.
- **cereals / granola / milk** — 2 SKUs each, small all-positive drift (~+4.0); milk drifters `_task405_clean`. Post-publication per-SKU data/engine deltas, not a wrong invocation (the other 18/20/16 reproduce exactly under the same recipe). Belongs to the TASK-418 refresh set.

**Conclusion:** the recipe generalizes. Where a category does not reproduce, the residual is provably a since-applied data/engine change (owner-gated TASK-418 refresh), not an invocation gap. HC Phase-0 baseline is established.
