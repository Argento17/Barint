(route: C1-CURSOR)

# P232 — Spine red-team fixes PASS 2 (C3-blessed scoring-detection). Worktree-isolated.

You are a C1 builder in an ISOLATED git worktree (cwd = worktree root, NOT C:\Bari). Pass 1
(commit b5fb25153) already landed RT-1/2/4/8/9/10/11. This pass implements the 4 decisions a C3
consult ruled on. Make ONLY these changes. After EACH, run the stated verification and paste
evidence. Do NOT touch published scores or any config's shelf_rel median/scale VALUES. Do NOT push.

Key files: 03_operations/bsip2/proto_v0/src/shadow_backtest.py, 03_operations/page_generator/
{rescore_all.py, onboard_category.py, conformance.py}, 03_operations/shadow/shadow_registry_v1.json,
03_operations/page_generator/configs/*.json.

## FIX RT-5 (C3 Decision 1) — inject pinned shelf stats into the shadow diff
PROBLEM (verified): `shadow_backtest.score_corpus(source, flags)` (~line 168) only calls
`_set_flags` — it does NOT inject shelf-relative stats, while the real `rescore_all.setup_shelf_stats`
(~line 331-352) does. So for shelf-relative shelves (cakes=sugars_g, brined=sodium_mg [api
sodium_ev056], cheese=fat_saturated_g) the shadow diff scores in ABSOLUTE mode and can report a
shelf as CLEAN when the real rescore would move it → spine_flip silently skips it (proven: a palm
flip omitted cakes from affected_set).
C3 ruling: option (a) — make the shadow path use the SAME pinned shelf stats as `rescore_all`.
IMPLEMENT:
  1. Add a helper that maps a registry corpus (name + source) to its page_generator config's
     `scoring.shelf_rel` block. Match by: config whose `corpus_dirs`/`scoring.bsip1_dir` contains
     the corpus source (normalized path), else config whose normalized `category` == corpus name.
     Return the shelf_rel dict or None.
  2. Change `score_corpus` to accept an optional `shelf_rel` arg; after `_set_flags`, if shelf_rel
     is given, inject it EXACTLY like rescore_all.setup_shelf_stats: if shelf_rel.get("api")==
     "sodium_ev056" call `set_shelf_sodium_stats(median, scale)`, else call
     `set_shelf_stats(nutrient, median, scale, scale_type or "iqr")`. Import the engine module the
     same way score_corpus already does. Do NOT recompute stats — use the pinned config values verbatim.
  3. In BOTH callers — `cmd_baseline` (~line 235) and `cmd_diff` (~line 414) — look up the shelf_rel
     for each corpus and pass it to score_corpus.
VERIFY: run `python 03_operations/bsip2/proto_v0/src/shadow_backtest.py baseline --corpus cakes`
(and brined_cheeses, cheese). Confirm it runs without error and the per-product scores now reflect
shelf-relative scoring (compare a couple to the live frontend JSON grades — they should be MUCH
closer than absolute-mode). Paste the baseline output.

## FIX RT-6 (C3 Decision 4) + the 2 real SOFT-9 drifts — registry source must equal the live corpus
PROBLEM (verified by SOFT-9): registry `source` != config corpus for several categories:
  - hard_cheeses: registry `run_hard_cheeses_001/output` vs config `02_products/hard_cheeses/bsip1_outputs`
  - juices: registry `run_juices_001/output` vs config `02_products/juices/bsip1_outputs`
  - cookies_coffee: registry single source vs config TWO corpus_dirs
  - granola: registry `run_cereals_005` vs live traces `run_cereals_008`
C3 ruling (D4): extend the registry + shadow loader to support MULTIPLE sources per corpus, and make
the registry describe the ACTUAL live corpus.
IMPLEMENT (carefully, verify each):
  1. Allow `source` in shadow_registry_v1.json to be EITHER a string OR a list of strings.
     Update `resolve_source` / `score_corpus` / `cmd_baseline` / `cmd_diff` and
     `affected_set._registry_sources()` to handle a list (load_batch over each dir, concatenate).
  2. For each drifted corpus, set its registry `source` to the config's corpus_dirs (the REAL live
     corpus): hard_cheeses + juices -> the single config corpus dir; cookies_coffee -> BOTH config
     corpus_dirs; granola -> reconcile to the run that produced live traces (run_cereals_008 if its
     bsip1 output dir exists and load_batch loads it; otherwise leave run_cereals_005 and note why).
  BEFORE changing any source: confirm the target dir(s) exist and `load_batch` loads >0 products.
  If a target dir does not load, DO NOT change it — report it instead.
VERIFY: `python 03_operations/page_generator/conformance.py --all` — SOFT-9 warnings for
hard_cheeses + juices must be GONE, SUMMARY still "12 conform / 0 non-conforming". Paste it.

## FIX RT-3 (C3 Decision 3) — onboard reproduce-check
ADD to `onboard_category.py`: after the existing conformance gate passes, run a shadow reproduce
check for the category — invoke `shadow_backtest.py diff --corpus <name>` (or import cmd_diff) with
NO flag overrides (baseline flags only) and assert ZERO score moves for that corpus. If moves > 0,
the registered flags do NOT reproduce live → print a HARD "NOT LIVE-READY: registered flags do not
reproduce live scores (N moves)" and exit non-zero. If the corpus is not yet in a baseline, print a
clear INFO that the reproduce-check needs a baseline first (do not hard-fail on missing baseline).
VERIFY: run `onboard_category.py --slug juices` (already conforming) and paste the result.

## FIX RT-7 (C3 Decision 2) — expansion drift guardrail (warn only)
C3 ruling: keep pinned stats; warn at >25% corpus-size drift from calibration.
IMPLEMENT as a new conformance.py SOFT check (SOFT-12-calibration_drift): if a config has a
`scoring.shelf_rel` with a recorded calibration corpus size (add/read an optional
`shelf_rel.calibration_n` field; if absent, SKIP the check — do not guess), compare to the current
corpus product count; warn if `abs(current - calibration_n)/calibration_n > 0.25`. Detail must name
both numbers. Do NOT recompute or move any score. Also append a one-paragraph note to
`03_operations/page_generator/configs/README` or a new `SHELF_REL_RECALIBRATION_POLICY.md` stating
the hybrid policy: new products score against the pinned baseline; recalibration only via explicit
review with a before/after movement report; publish only after approval. (If no README exists,
create SHELF_REL_RECALIBRATION_POLICY.md in the configs dir.)
VERIFY: conformance --all still 12/12; note whether SOFT-12 fired anywhere (likely nowhere, since
calibration_n is new/absent — that is correct).

## FINAL VERIFICATION (paste all)
```
python -c "import ast;[ast.parse(open(f,encoding='utf-8').read()) for f in ['03_operations/bsip2/proto_v0/src/shadow_backtest.py','03_operations/page_generator/onboard_category.py','03_operations/page_generator/conformance.py']];print('valid')"
$env:PYTHONIOENCODING='utf-8'; python 03_operations/page_generator/conformance.py --all
```
Report: per-fix evidence, the conformance SUMMARY (must stay 12/0), unified diffs of all changed
files, and the registry source changes you made (and any you DECLINED because the target didn't load).
End with the return-contract JSON. If ANYTHING is ambiguous or a target corpus doesn't load, STOP and
report rather than guess — do not move scores.
