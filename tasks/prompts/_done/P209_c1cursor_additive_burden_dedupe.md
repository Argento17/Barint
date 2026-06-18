# P209 — TASK-329 additive_burden double-count reconcile (route: C1-CURSOR)
# Data Agent build — representation-only module, no scoring path

**Repo:** `C:\Bari`
**Task to read:** `C:\Bari\tasks\TASK-329.md`
**ONLY file you may edit:** `03_operations/bsip2/proto_v0/src/method_additive_burden.py`

## Problem
`evaluate_additive_burden()` double-counts: an additive that is BOTH an EV-002 named-concern
(`tax_named_concern_additives`, weight 3.0) AND an EV-003 high-risk emulsifier
(`sprint1_high_risk_emulsifier_found`, weight 2.0) is scored under both — CMC/E466 and carrageenan/E407 (and
polysorbate/E433) inflate the index by an extra ×2 each. Verified live: cakes barcode 2472148 shows index
13.0 = 3×3 + 2×2.

## Exact change
Dedupe the EV-003 high-risk component against the EV-002 at-risk set: any high-risk emulsifier that already
appears (by canonical additive / E-number) in the EV-002 `at_risk_list` is **excluded from the EV-003 high-risk
count** before weighting. Recompute `additive_burden_index` and `burden_band`. Keep the EV-002 ×3 as the
authoritative weight for those shared additives (do not drop them entirely — just stop counting them twice).
Add a one-line trace note in the component payload recording how many were de-duplicated.

## Hard guards
- **Representation-only module — touches NO scoring path.** Index is a display rollup; do not import/alter
  score_engine, constants, configs, or any page JSON.
- OFF-ban: trace data only; OFF-sourced traces stay `index: null` (existing behaviour — preserve it).

## Acceptance test (run it, put result in self_check)
1. `python 03_operations/bsip2/proto_v0/src/method_additive_burden.py --single <trace path for cakes 2472148>`
   before vs after — show the index drops by exactly the overlap (e.g. 13.0 → 11.0 if one shared additive).
2. `python 03_operations/bsip2/proto_v0/src/method_additive_burden.py --calibrate` — report the FULL new
   `burden_band_distribution` and the count of products whose index changed, with the deriving command.
3. Confirm `git diff --stat` touches ONLY `method_additive_burden.py`.

## Return
RETURNED proposal + return-contract JSON (`01_framework/operations/return_contract_v1.md`).
**Do not close. Do not commit or push.**
