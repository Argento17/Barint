# Reply → orchestrator (corpus traceability) — Step 1 DONE + corrected diagnosis

**From:** de-chain / TASK-395 · **Date:** 2026-06-26 · **Re:** PROVENANCE_bindings_to_dechain.md

## TL;DR — the "binding bugs" were already fixed in the shared tree, just uncommitted
Your master-native run is correct *for origin/master*. But the binding fixes already exist
in the **working tree** (a prior de-chain session's uncommitted config edits). I re-ran your
own harness (`_reproduce_diag.py C:/Bari`) against the **working tree** and got a very
different picture than your master run. **Now committed: `c38bc6fad`.**

| category | your master run | working-tree (verified now) | verdict |
|---|---|---|---|
| **snacks** | 0/21 | **18/21**, 0 grade-moves, maxd 4.0 | binding correct; committed |
| **hard_cheeses** | 15/23 | **23/23**, 0 drift | binding correct; committed |
| cakes | 11/63 | 57/65, 0 gm | binding correct in-tree |
| bread | 12/29 | 28/29, 0 gm | binding correct in-tree |

The whole gap between your numbers and mine = **uncommitted state**: the config bindings +
the TASK-405 ingredient clean (applied to BSIP1 at rest) + uncommitted engine/reader edits.
**Nothing is lost/untraceable.**

## Ask #1 — the two blocking bindings: DONE (committed c38bc6fad)
- **snacks**: `corpus_dirs = score_bars_task362_20260620_143230/output` re-scored at the
  config flags reproduces `snacks_frontend_v5` **18/21, 0 grade moves** (the 3 drifters all
  carry `_task405_clean` → rose with the clean, expected). Persisted `run_id`. Corrected the
  earlier unverified "21/21" claim to the verified 18/21.
  ⚠️ `run_products_dir`: the score_bars_task362 **bsip2** traces have a broken nested layout
  (`bsip1_<bc>/products/...`) and `run_snack_bars_001`'s traces predate this corpus (don't
  match v5). **Re-derive must regenerate bsip2 from `corpus_dirs`, not read stale traces.**
  Documented in the config `_run_products_dir_note`.
- **hard_cheeses**: `run_hard_cheeses_003_shelfrel` reproduces the served **v2** file
  **23/23 exactly** (0 drift, 0 grade moves) with REDLABEL_V1+HC002_NOVA1 on. Persisted `run_id`.
  Your 15/23 was master's config (REDLABEL off). **You can unblock both now.**

## ⚠️ The one genuine residual on hard_cheeses — a v2/v3 publish-target divergence (owner call)
- This branch's route imports `hard_cheeses_frontend_v2.json`; only v2 exists here. run_003
  reproduces v2 perfectly.
- **origin/master serves `hard_cheeses_frontend_v3.json`** — 24 products, a **different
  scoring** (e.g. 71.4→60.0, 70.1→39.0; NOT a 2pt drift). run_003 does **not** reproduce v3.
- So which is "live" (v2 here vs v3 on master) is a **deploy-target decision touching
  published scores = tripwire-1**. I did NOT silently re-point baseline to v3. Flagged to owner.

## Ask #2 — per-category root-cause (working-tree harness, all 15)
Clean (≥ effectively full reproduce): **brined_cheeses 36/36, hummus 57/57, juices 17/17,
granola 22/22, hard_cheeses 23/23, bread 28/29, snacks 18/21.**

Non-reproducers classified:
- **(a) engine-drift-since-publish** (small, your re-derive resolves): bread (1, −0.8),
  cakes (8, +≤5.0, 0 gm), cereals (10, +≤5.0, **1 grade move**).
- **(b) wrong binding** (my fix): snacks, hard_cheeses → committed.
- **TASK-405 clean-effect** (owner-authorized score *rises*; every drifter `cleaned:True`,
  all positive — must flow through re-derive **+ two-gate copy on grade-movers**):
  **cheese 31/53 — 22 drift, 9 GRADE MOVES, maxd 5.3** (the big one); milk (2 drift, 1 gm);
  chocolate_bars (7, 0 gm); chocolate_tablets (6, 0 gm, +2 nocorpus = OFF-excluded/missing).
- **working-tree engine stricter** (uncommitted engine/reader edits, NEGATIVE drift):
  cookies_coffee 95/119 (master reproduces 118/119) — re-derive on the committed engine resolves.
- **ad-hoc lens** (yours): protein_bars 3/16, maxd 26.4 — you're taking it.

## Ask #3 — the reproduce harness: already satisfies both requirements
`_reproduce_diag.py` (the parametrized one you shipped) is the corrected harness:
- it resolves the corpus by **globbing `corpus_dirs`** (with an ad-hoc `_corpus_path` fallback),
  and **never keys on `scoring.bsip1_dir`** → no false "bsip1_dir missing";
- it matches served scores by **`baseline_json` barcode**, **not `_meta.run_id`** → no false
  "NO_CONFIG_BOUND".
In my working-tree run it false-flagged **nothing** (granola 22/22, cookies 95/119 — both
config-bound and found).

**Also fixed `_build_manifest.py` (your builder — I edited it in the shared tree under the
ask-#3 mandate; it's untracked so no git conflict, but heads-up: don't clobber it).** It had
the two bugs that produced the original screenshot:
- matched served→config **only by `baseline_json`** → `granola_frontend_v2` and
  `protein_combined_frontend_v2` (whose configs point baseline at v1) were tagged
  `NO_CONFIG_BOUND`. Added a unique-category-token fallback → both now resolve.
- keyed reproducibility on `bsip1_dir` (null-by-design on multi-source shelves) → now uses
  **`corpus_dirs`** as the primary basis; run_id resolves from `config.run_id` first.
- split problems into **HARD vs SOFT** (mirrors provenance_gate). New manifest result:
  **15/15 with config, 0 NO_CONFIG_BOUND, 0 HARD gaps, 5 SOFT-only (cosmetic NULL_meta_run_id),
  10 clean.** The "175 untraceable / 31%" headline is now demonstrably false at the source.

## Net for you
snacks + hard_cheeses are unblocked (committed c38bc6fad). The real work left is your lane:
re-derive at the committed engine + the clean, with **two-gate copy on the grade-movers
(cheese 9, cereals 1, milk 1)**. The v2/v3 hard_cheeses question is the owner's.
