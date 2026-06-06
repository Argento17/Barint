# AUTHORITATIVE — Snack Bars Baseline: run_snackbars_007_headpin

**Frozen: 2026-06-05**
**Task: TASK-180B**
**Engine tag: engine-baseline-2026-06-04 (f075d9e)**
**Config hash: d6f0b99fc5c49e0e**
**Flags: BARI_RECAL_P0=off | BARI_GLASSBOX_W4=on | BARI_TASK144_FIXES=off**

---

## Status
This run is the **canonical snack bars baseline** as of 2026-06-05.
Supersedes: `sprint1/outputs/production_snack_bars.json` (old sprint1 baseline).

Live frontend JSON: `bari-web/src/data/comparisons/snacks_frontend_v2.json`
(reshippped 2026-06-05 with TASK-180B re-baseline pass)

---

## Corpus
- Source: `C:\Bari\03_operations\bsip1\run_001\output` (53 snack bar products)
- Scored: 53 (0 errors)
- Rollback identity: 53/53 byte-identical (engine deterministic)

## Reproduction Rate
- HEAD-OFF vs sprint1 production baseline: 46/53 (87%)
- HEAD-OFF vs proto_v0 sealed traces (May-17): 4/53 (historical drift, expected)

## Frozen Invariants
| Invariant | Status |
|-----------|--------|
| snk-001 = 70/B (ceiling) | **HELD** |
| No snack bar ≥ 80 (A) | **HELD** |

## Drift Classification (HEAD-OFF vs sprint1 baseline)
| Class | Count |
|-------|-------|
| Exact match | 46 |
| Grade-affecting | **0** |
| ≥2pt cosmetic, same grade | 2 |
| <2pt cosmetic, same grade | 5 |

## Frontend Reship Summary (18 displayed products)
- Products updated: 11/18
- Grade changes: 0
- All changes: ≤2pt cosmetic (same grade)
- Crosswalk: `snk_crosswalk_run007_corrected.md` (imageUrl-barcode verified)

## Editorial Note
comparisonContext and insightLine fields quote specific score numbers that may be ±2pt
stale after this re-baseline. A Content Agent editorial pass should update quoted scores
in expansion text where they cross-reference other products' scores.

## Voided Decision
The 69.5/B ceiling-crowding editorial call (Owner + Nutrition approved a quiet note) was
based on a fabricated crosswalk entry. The 69.5/B product (bsip1_8423207210287,
"מרבה סלים דליס שוקולד לבן בטעם יוגורט") is confirmed NOT in the 18 displayed products
by imageUrl-barcode analysis. No note was added to the frontend. Decision void.

The second-highest **displayed** product is snk-015 at 63/C — a 7-point gap from the
70/B ceiling, well outside the ≤2pt noise band. No ceiling-crowding presentation issue exists.

## Sign-off Chain
- Data Agent: RETURNED 2026-06-05
- Owner + Nutrition D7: approved re-baseline + freeze 2026-06-05
- CC close-readiness gate: PASSED 2026-06-05
  - Independent verification: barcode-based crosswalk, zero grade moves confirmed
  - Ghost product identified and note approval voided
  - Reship executed and verified
