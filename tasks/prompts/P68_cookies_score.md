# P68 — Cookies-near-coffee: BSIP1 build + BSIP2 score (Stage 3) (route: C1-CURSOR)

**Task:** TASK-275 (factory run #7, `cookies-coffee`). **Lane:** C1-CURSOR — spec-complete: build BSIP1 +
run the committed scoring engine on the corpus, mirroring proven brined templates. No engine edits.

## Objective
Score the **61 IN_SCORED** coffee biscuits with the committed engine, producing a real run
(`run_cookies_001`) + traces + run_record + a verification table. This is the keystone scoring stage.

## Inputs
1. Corpus: `02_products/cookies_coffee/factory_run_001/corpus_filter.json` — score the **IN_SCORED** bucket only (61).
2. Raw BSIP0: `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json`.
3. Methodology (the prediction to verify against): `02_products/cookies_coffee/methodology/cookies_coffee_scoring_interpretation_v1.md`.
4. TEMPLATES to mirror exactly (only paths/category differ):
   - BSIP1 build: `03_operations/bsip1/run_brined_cheeses_002/build_bsip1_002.py`
   - BSIP2 batch: `03_operations/bsip2/proto_v0/src/batch_run_brined_cheeses_005.py`

## Steps
1. **BSIP1 build** → `03_operations/bsip1/run_cookies_001/` : convert the 61 IN_SCORED BSIP0 records to
   BSIP1 (normalized nutrition + ingredients_list + the standard fields), mirroring `build_bsip1_002.py`.
   Use the canonical `bsip0_nutrition.parse_nutrition_numeric` path. OFF ban: a field not in the scrape
   stays NULL — never fill from any external source.
2. **BSIP2 score** → `02_products/cookies_coffee/bsip2_outputs/run_cookies_001/` : run the engine on the
   61 BSIP1 records, write `bsip2_trace.json` per product + `run_record.json` + `verification_table.csv`.

## Flag config (CRITICAL — cookies is NON-dairy / NON-brined; brined flags must NOT fire)
Set the env exactly:
```
BARI_RECAL_P0 = off            # per methodology §2.3 (sat-fat cliff cap 55 operative for this category)
BARI_GRAD_SODIUM_V1 = off      # brined-only; cookies are not brined
BARI_SODIUM_SHELF_RELATIVE_V1 = off
BARI_DAIRY_PROTEIN_REWEIGHT_V1 = off   # cookies are not a dairy-protein food
BARI_REDLABEL_V1 = off
BARI_SODIUM_CEREAL = off
BARI_GLASSBOX_W4 = (engine committed default — do NOT override; report what it is)
```
All other experimental flags: leave at the engine's committed default (do not set). **Report the full
resolved env config used AND the engine's default value for BARI_RECAL_P0 and BARI_GLASSBOX_W4.**

## Guards (hard)
- **No engine edits.** Do not modify `score_engine.py` / `nova_proxy.py` / `evaluation_scope.py` / `constants.py`.
  This is a run, not a recalibration.
- **OFF ban absolute** — `off_used=0` in run_record and every trace.
- `brined_food` context flag must NOT fire on any cookie (verify: 0/61). If it fires, STOP and report.
- Frozen invariants: this is a new category with no published scores; do not touch any other category's data.

## Definition of done (report all)
1. 61 traces written; run_record + verification_table present (paths + sha256 of run_record).
2. **Full grade distribution** (A/B/C/D/E counts) + **score min/max/median/stdev + most-common score & its count**.
3. **Per-product table**: barcode · score · grade · top cap(s) fired · nova_level — for all 61 (in the csv;
   paste the first 15 rows + the full distribution in the return).
4. `engine_invariants.py` re-run → **342 cases, expect 6/6 PASS** (paste the verdict). Confirms no leakage.
5. off_used=0 (run_record + grep all traces); brined_food fired = 0/61.
6. **Compare to methodology prediction** (§2.3/§5): is the spread C-modal with a B-ceiling and no A? Report
   match/mismatch plainly — do NOT adjust anything to force a match; report what the engine actually did.

## Return format
End with the return contract (`01_framework/operations/return_contract_v1.md`): task=P68,
proposed_status=RETURNED, artifacts (run_record + verification_table + sha256), counts (full distribution +
stdev + most-common-count + off_used + brined_food_fired + invariants), commands_run (with exit codes),
not_done, self_check. Do NOT close — propose RETURNED. The orchestrator verifies vs the traces + P65.
