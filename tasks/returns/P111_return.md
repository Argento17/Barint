# P111 Return — TASK-278 Phase-5: D6 Cereals Stats Re-run

**Task:** TASK-278  
**Phase:** Phase-5 D6 cereals stat re-run  
**Agent:** nutrition-agent  
**Return date:** 2026-06-14  
**Status:** RETURNED

---

## Summary

Recomputed cereal-only sugar shelf-relative stats from the 34 cereal-routed products in
`run_cereals_001_shelfrel_pilot` pilot traces. The prior n=45 stats (median=14.0, IQR=11.0,
scale=8.896) included 11 `snack_bar_granola` products out of scope for `SUGAR_SHELF_REL_SCOPE`.

New stats (n=34 cereal-only): median=13.0g, IQR=13.5g, MAD=8.0g, robust_scale=11.861
(MAD-primary). Three new constants added to `constants.py`. Engine invariants: 342 PASS.
Anti-Immunity re-verified: floor(62) + B_max(3) = 65 < 70. Floor, threshold, scope unchanged.

---

## Step 1: Corpus extraction

**Pilot traces directory:** `02_products/breakfast_cereals/bsip2_outputs/run_cereals_001_shelfrel_pilot/products/`
**Total traces:** 45
**Cereal-routed (n=34):** category == "cereal"
**Granola-routed (n=11):** category == "snack_bar_granola"

Note on n=33 vs n=34: The original enrollment doc (D6, P106) used `run_cereals_synthesis_001`
which routed the spelt-flakes product as `bread` (n=33 cereal). The pilot run routes that same
product as `cereal`, yielding n=34. This addendum uses n=34 as authoritative for constants.py.

### Cereal barcodes + sugars_g (n=34, sorted by sugars_g)

| Barcode | sugars_g |
|---|---|
| 5900100000005 | 0.5 |
| 7290100000002 | 1.0 |
| 5900100000003 | 1.1 |
| 7290100000001 | 1.1 |
| 7290100000004 | 1.5 |
| 4013228100001 | 2.0 |
| 8437014100001 | 4.0 |
| 5011145100001 | 4.5 |
| 7290100000008 | 5.0 |
| 7290100000042 | 5.0 |
| 7290100000011 | 7.5 |
| 5054568100001 | 8.0 |
| 7290100000041 | 8.0 |
| 7613031100001 | 8.5 |
| 5054568100002 | 9.0 |
| 7290100000045 | 10.0 |
| 7613031100050 | 12.0 |
| 5054568100050 | 14.0 |
| 5054568100022 | 16.0 |
| 5054568100040 | 16.0 |
| 7613031100020 | 16.0 |
| 5900100000007 | 16.0 |
| 5054568100020 | 17.0 |
| 5054568100021 | 18.5 |
| 5900100000006 | 18.5 |
| 7613031100021 | 18.5 |
| 5000159100001 | 24.0 |
| 7613031100011 | 26.0 |
| 7613031100012 | 28.0 |
| 7290100000020 | 30.0 |
| 5054568100010 | 35.0 |
| 7613031100010 | 36.0 |
| 5054568100011 | 38.0 |
| 5054568100012 | 39.0 |

### Granola barcodes + sugars_g (n=11)

| Barcode | sugars_g |
|---|---|
| 7290100000034 | 8.0 |
| 4016249100002 | 10.0 |
| 7290100000031 | 10.0 |
| 4016249100001 | 12.0 |
| 7290100000030 | 12.0 |
| 7290100000038 | 15.0 |
| 7290100000028 | 18.0 |
| 7290100000033 | 19.0 |
| 5054568100030 | 20.0 |
| 7290100000032 | 22.0 |
| 7290100000029 | 24.0 |

---

## Step 2: Cereal-only stats (n=34)

| Statistic | n=45 (superseded) | n=34 cereal-only (new) | Shift |
|---|---|---|---|
| n | 45 | 34 | -11 |
| Q1 | — | 5.0g | — |
| **median** | **14.0g** | **13.0g** | **-1.0g** |
| Q3 | — | 18.5g | — |
| **IQR** | **11.0g** | **13.5g** | **+2.5g** |
| **MAD** | — | **8.0g** | — |
| scale_iqr (IQR/1.349) | — | 10.007 | — |
| scale_mad (1.4826×MAD) | — | 11.861 | — |
| **robust_scale** | **8.896** | **11.861** (MAD-primary) | **+2.965** |

**Low-variance guard:** 11.861 >= 1.4 PASS  
**n guard:** 34 >= 20 PASS  
**Scale divergence confirmed:** 11.861 ≠ 8.896 (the n=45 contaminated value)

---

## Step 3: constants.py update

**File:** `03_operations/bsip2/proto_v0/src/constants.py`  
**Location:** Added after line 567 (SUGAR_SHELF_REL_CEREAL_FLOOR_THRESHOLD_G)

Three new constants added:
- `SUGAR_SHELF_REL_CEREAL_MEDIAN = 13.0`
- `SUGAR_SHELF_REL_CEREAL_IQR = 13.5`
- `SUGAR_SHELF_REL_CEREAL_SCALE = 11.8608`

With comment: `# n=34 cereal-only (updated P111, 2026-06-14; prior n=45 was contaminated by 11 snack_bar_granola products)`

**DO NOT changed (confirmed unchanged):**
- `SUGAR_SHELF_REL_CEREAL_FLOOR = 62`
- `SUGAR_SHELF_REL_CEREAL_FLOOR_THRESHOLD_G = 25.0`
- `SUGAR_SHELF_REL_SCOPE = frozenset({"biscuit", "cereal"})`
- All biscuit constants

---

## Step 4: Verification

**Load check:**
```
CEREAL_MEDIAN: 13.0
CEREAL_IQR: 13.5
CEREAL_SCALE: 11.8608
CEREAL_FLOOR: 62
CEREAL_FLOOR_THRESHOLD_G: 25.0
SCOPE: frozenset({'cereal', 'biscuit'})
```

**engine_invariants:** ALL PASS — 342/342 (6 invariants: I1_BOUNDS, I2_DETERMINISM, I3_NULL_SAFETY, I4_OFF_FREE, I5_GRADE_CONSISTENCY, I6_MONOTONICITY; 300 synthetic + 42 real records)

---

## Anti-Immunity re-check

With revised stats, the maximum SR relief is still bounded by `B_max = 3`. Re-verified:
- EV-087 floor: 62 (unchanged)
- Maximum score above floor: floor(62) + B_max(3) = 65
- 65 < 70 (grade B threshold) PASS

The Anti-Immunity rule holds regardless of median shift (floor and B_max are unchanged).

---

## Spec-conflict note

The dispatch prompt states the enrollment document path as:
`02_products/breakfast_cereals/intelligence_bsip2/cereals_sugar_enrollment_v1.md`

The actual path is:
`02_products/breakfast_cereals/methodology/shelf_relative_sugar_enrollment_cereals_v1.md`

The addendum was written to the correct actual path. The dispatch prompt contains a stale/wrong path reference. Flagging for orchestrator awareness.

---

```json
{
  "task_id": "TASK-278",
  "phase": "Phase-5 D6 cereals stat re-run",
  "status": "RETURNED",
  "return_date": "2026-06-14",
  "agent": "nutrition-agent",
  "cereal_n": 34,
  "granola_n": 11,
  "n45_stats": {"median": 14.0, "IQR": 11.0, "scale": 8.896},
  "n34_stats": {
    "median": 13.0,
    "IQR": 13.5,
    "MAD": 8.0,
    "scale": 11.8608
  },
  "median_shift_g": -1.0,
  "scale_shift": 2.9648,
  "constants_updated": ["SUGAR_SHELF_REL_CEREAL_MEDIAN", "SUGAR_SHELF_REL_CEREAL_IQR", "SUGAR_SHELF_REL_CEREAL_SCALE"],
  "floor_unchanged": 62,
  "threshold_unchanged": 25.0,
  "anti_immunity_recheck": "floor(62) + B_max(3) = 65 < 70 PASS",
  "engine_invariants": "342 PASS",
  "off_used": false,
  "spec_conflict_flagged": "Dispatch prompt path 'intelligence_bsip2/cereals_sugar_enrollment_v1.md' is wrong; actual path is 'methodology/shelf_relative_sugar_enrollment_cereals_v1.md'; addendum written to correct path",
  "cereal_barcodes_with_sugar": [
    {"barcode": "4013228100001", "sugars_g": 2.0},
    {"barcode": "5000159100001", "sugars_g": 24.0},
    {"barcode": "5011145100001", "sugars_g": 4.5},
    {"barcode": "5054568100001", "sugars_g": 8.0},
    {"barcode": "5054568100002", "sugars_g": 9.0},
    {"barcode": "5054568100010", "sugars_g": 35.0},
    {"barcode": "5054568100011", "sugars_g": 38.0},
    {"barcode": "5054568100012", "sugars_g": 39.0},
    {"barcode": "5054568100020", "sugars_g": 17.0},
    {"barcode": "5054568100021", "sugars_g": 18.5},
    {"barcode": "5054568100022", "sugars_g": 16.0},
    {"barcode": "5054568100040", "sugars_g": 16.0},
    {"barcode": "5054568100050", "sugars_g": 14.0},
    {"barcode": "5900100000003", "sugars_g": 1.1},
    {"barcode": "5900100000005", "sugars_g": 0.5},
    {"barcode": "5900100000006", "sugars_g": 18.5},
    {"barcode": "5900100000007", "sugars_g": 16.0},
    {"barcode": "7290100000001", "sugars_g": 1.1},
    {"barcode": "7290100000002", "sugars_g": 1.0},
    {"barcode": "7290100000004", "sugars_g": 1.5},
    {"barcode": "7290100000008", "sugars_g": 5.0},
    {"barcode": "7290100000011", "sugars_g": 7.5},
    {"barcode": "7290100000020", "sugars_g": 30.0},
    {"barcode": "7290100000041", "sugars_g": 8.0},
    {"barcode": "7290100000042", "sugars_g": 5.0},
    {"barcode": "7290100000045", "sugars_g": 10.0},
    {"barcode": "7613031100001", "sugars_g": 8.5},
    {"barcode": "7613031100010", "sugars_g": 36.0},
    {"barcode": "7613031100011", "sugars_g": 26.0},
    {"barcode": "7613031100012", "sugars_g": 28.0},
    {"barcode": "7613031100020", "sugars_g": 16.0},
    {"barcode": "7613031100021", "sugars_g": 18.5},
    {"barcode": "7613031100050", "sugars_g": 12.0},
    {"barcode": "8437014100001", "sugars_g": 4.0}
  ],
  "granola_barcodes_with_sugar": [
    {"barcode": "4016249100001", "sugars_g": 12.0},
    {"barcode": "4016249100002", "sugars_g": 10.0},
    {"barcode": "5054568100030", "sugars_g": 20.0},
    {"barcode": "7290100000028", "sugars_g": 18.0},
    {"barcode": "7290100000029", "sugars_g": 24.0},
    {"barcode": "7290100000030", "sugars_g": 12.0},
    {"barcode": "7290100000031", "sugars_g": 10.0},
    {"barcode": "7290100000032", "sugars_g": 22.0},
    {"barcode": "7290100000033", "sugars_g": 19.0},
    {"barcode": "7290100000034", "sugars_g": 8.0},
    {"barcode": "7290100000038", "sugars_g": 15.0}
  ],
  "artifacts": [
    {
      "path": "03_operations/bsip2/proto_v0/src/constants.py",
      "sha256": "3aea86614f97cb03518450681b7a86eb2290d4ce08c71d83af9fc173bcedd52c",
      "change": "Added SUGAR_SHELF_REL_CEREAL_MEDIAN=13.0, SUGAR_SHELF_REL_CEREAL_IQR=13.5, SUGAR_SHELF_REL_CEREAL_SCALE=11.8608"
    },
    {
      "path": "02_products/breakfast_cereals/methodology/shelf_relative_sugar_enrollment_cereals_v1.md",
      "sha256": "d60e2f9d638c7e5c808d5b85cdca7faf392f9cb91f983411af7ca45dabc28f49",
      "change": "Appended corpus correction addendum (P111, 2026-06-14)"
    }
  ],
  "counts": {
    "cereal_products": 34,
    "granola_products": 11,
    "total_pilot_traces": 45,
    "products_missing_sugar": 0,
    "constants_added": 3,
    "constants_unchanged_floor": 1,
    "constants_unchanged_threshold": 1,
    "engine_invariants_total": 342,
    "engine_invariants_pass": 342,
    "engine_invariants_fail": 0
  },
  "commands_run": [
    {
      "cmd": "python extract category+sugars_g from 45 pilot traces",
      "exit_code": 0,
      "output_summary": "cereal_n=34, granola_n=11, total=45, 0 unexpected categories, 0 missing sugars_g"
    },
    {
      "cmd": "python numpy stats on n=34 cereal sugars",
      "exit_code": 0,
      "output_summary": "median=13.0, IQR=13.5, MAD=8.0, scale_iqr=10.007, scale_mad=11.861, robust_scale=11.8608 (MAD-primary), low_var_guard=PASS"
    },
    {
      "cmd": "python -c 'from constants import SUGAR_SHELF_REL_CEREAL_MEDIAN...'",
      "exit_code": 0,
      "output_summary": "CEREAL_MEDIAN=13.0, CEREAL_IQR=13.5, CEREAL_SCALE=11.8608, FLOOR=62 (unchanged), THRESHOLD=25.0 (unchanged)"
    },
    {
      "cmd": "python ../../../shadow/engine_invariants.py (from proto_v0/src/)",
      "exit_code": 0,
      "output_summary": "ALL PASS: 342/342 (6 invariants, 300 synthetic + 42 real records)"
    }
  ],
  "not_done": [
    "Pilot rescore P112 (run_cereals_001 batch with corrected n=34 stats) — awaits orchestrator dispatch",
    "PROPOSAL_MEDIAN and PROPOSAL_SCALE in batch_run_cereals_001_shelfrel_pilot.py are still 14.0/8.896 — these are pilot-run-level validation constants; whether to update them is P112's concern, not P111's scope",
    "EV-087 registry formal registration — still pending Product Agent D7 co-sign (separate gate)"
  ]
}
```
