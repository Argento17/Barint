# TASK-449: Brined Cheese Inversion Diagnosis
**Status:** RETURNED — corrected v2 (overwrite of v1 sha256=42aa169b)
**Date:** 2026-07-02
**Author:** Nutrition Agent
**Scope:** FINDINGS ONLY — no score/engine/JSON/config changes

---

## Objective

Diagnose why `inversion_invariant_v2.py` fires 17 real inversions on the brined_cheeses golden page.
Flagship pair: bc-028 sheep feta (7290011499051, score 71.6) outranks bc-037 cow cheese (48413, score 66.3), even though bc-037 is better on nutrient_density, protein_quality, satiety_support, and fat_quality.

---

## Evidence Sources

All findings derived from committed artifacts. No engine re-run performed (run_brined_005 traces are authoritative).

| Artifact | Path |
|---|---|
| bc-028 trace | `02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_7290011499051/bsip2_trace.json` |
| bc-037 trace | `02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_48413/bsip2_trace.json` |
| Engine source | `03_operations/bsip2/proto_v0/src/score_engine.py` |
| Constants | `03_operations/bsip2/proto_v0/src/constants.py` |
| Gate source | `03_operations/page_generator/gates/inversion_invariant_v2.py` |

---

## Flagship Pair: Trace-Authoritative Values

### bc-028 — Sheep Feta 20% (7290011499051)

| Field | Value | Source |
|---|---|---|
| product_name_he | Feta sheep cheese 20% | trace L1 |
| energy_kcal | 236.0 | trace L1 |
| fat_g | 20.0 | trace L1 |
| fat_saturated_g | 13.3 | trace L1 |
| sodium_mg | 930.0 | trace L1 |
| protein_g | 14.0 | trace L1 |
| sugars_g | 0.0 | trace L1 |
| nova_proxy | 2 | trace |
| context_flag | brined_food | trace |
| has_fermentation | false | trace L3 |

**dimension_scores (from trace):**

| Dimension | Score | Weight (DAIRY_PROTEIN_WEIGHTS) | Weighted |
|---|---|---|---|
| processing_quality | 85.0 | 0.15 | 12.750 |
| nutrient_density | 95.1 | 0.15 | 14.265 |
| calorie_density | 55.0 | 0.11 | 6.050 |
| glycemic_quality | 90.0 | 0.12 | 10.800 |
| protein_quality | 95.1 | 0.14 | 13.314 |
| additive_quality | 82.0 | 0.10 | 8.200 |
| satiety_support | 71.2 | 0.06 | 4.272 |
| fat_quality | 16.3 | 0.08 | 1.304 |
| regulatory_quality | 25.0 | 0.05 | 1.250 |
| whole_food_integrity | 85.0 | 0.04 | 3.400 |
| **Sum** | | | **75.605** |

**Trace records:** `weighted_dimension_score: 83.61`

**Discrepancy: 83.61 - 75.605 = 8.005 points**

The trace does NOT contain `fermentation_bonus_applied` or `fermentation_bonus_note` fields. The run_005 traces were produced by an engine version that did not yet serialize these fields. The bonus is applied to `weighted_dim_score` in memory at score_engine.py line 3864 but was not written to the JSON output for this run. The arithmetic gap of 8.005 is the proof.

**Score pipeline (bc-028):**
- weighted_dimension_score (post-bonus): 83.61
- caps_applied: none
- score_after_cap: 83.61
- SODIUM_LOAD_GENERAL_GRAD penalty: -12 (sodium=930mg, band >=900, confirmed in trace penalties_applied)
- score_after_penalty: 71.61
- **final_score_estimate: 71.6 / Grade B**

---

### bc-037 — Cow Brined Cheese 16% (48413)

| Field | Value | Source |
|---|---|---|
| product_name_he | Brined cow cheese 16% | trace L1 |
| energy_kcal | 234.0 | trace L1 |
| fat_g | 16.0 | trace L1 |
| fat_saturated_g | 10.0 | trace L1 |
| sodium_mg | 1065.0 | trace L1 |
| protein_g | 20.0 | trace L1 |
| sugars_g | null (missing) | trace L1 |
| nova_proxy | 2 | trace |
| context_flag | brined_food | trace |
| has_fermentation | false | trace L3 |

**dimension_scores (from trace):**

| Dimension | Score | Weight (DAIRY_PROTEIN_WEIGHTS) | Weighted |
|---|---|---|---|
| processing_quality | 85.0 | 0.15 | 12.750 |
| nutrient_density | 95.4 | 0.15 | 14.310 |
| calorie_density | 55.0 | 0.11 | 6.050 |
| glycemic_quality | 90.0 | 0.12 | 10.800 |
| protein_quality | 95.4 | 0.14 | 13.356 |
| additive_quality | 82.0 | 0.10 | 8.200 |
| satiety_support | 100.0 | 0.06 | 6.000 |
| fat_quality | 27.5 | 0.08 | 2.200 |
| regulatory_quality | 25.0 | 0.05 | 1.250 |
| whole_food_integrity | 85.0 | 0.04 | 3.400 |
| **Sum** | | | **78.316** |

**Trace records:** `weighted_dimension_score: 78.32`

**Discrepancy: 78.32 - 78.316 = 0.004 points (rounding only). No bonus applied.**

Note on missing sugars_g: bc-037 has `sugars_g: null`. The engine treats null sugar as 0 for glycemic_quality computation, confirmed by trace dimension_note: "90 - sugar_penalty(0.0) + fiber(0.0) + wg(0) = 90.0". Both products receive glycemic_quality=90.0. The null is not a penalty.

**Score pipeline (bc-037):**
- weighted_dimension_score (no bonus): 78.32
- caps_applied: none
- score_after_cap: 78.32
- SODIUM_LOAD_GENERAL_GRAD penalty: -12 (sodium=1065mg, band >=900, confirmed in trace penalties_applied)
- score_after_penalty: 66.32
- **final_score_estimate: 66.3 / Grade B**

---

## Dimension Comparison: bc-037 vs bc-028

| Dimension | bc-028 | bc-037 | bc-037 advantage | Weighted contribution |
|---|---|---|---|---|
| processing_quality | 85.0 | 85.0 | 0.0 | 0.000 |
| nutrient_density | 95.1 | 95.4 | +0.3 | +0.045 |
| calorie_density | 55.0 | 55.0 | 0.0 | 0.000 |
| glycemic_quality | 90.0 | 90.0 | 0.0 | 0.000 |
| protein_quality | 95.1 | 95.4 | +0.3 | +0.042 |
| additive_quality | 82.0 | 82.0 | 0.0 | 0.000 |
| satiety_support | 71.2 | 100.0 | +28.8 | +1.728 |
| fat_quality | 16.3 | 27.5 | +11.2 | +0.896 |
| regulatory_quality | 25.0 | 25.0 | 0.0 | 0.000 |
| whole_food_integrity | 85.0 | 85.0 | 0.0 | 0.000 |
| **Total** | | | | **+2.711** |

bc-037 is strictly better on all four dimensions the gate reports. At the pure dimension level, bc-037's composite advantage is +2.711 points. The gate fires correctly: bc-037 dominates bc-028 at the dimension stage.

---

## Sodium Band Analysis: The Previous Error, Now Corrected

**SODIUM_GENERAL_BANDS** (constants.py lines 257-263):
```
[(900, None, 12), (700, 899, 8), (600, 699, 4), (450, 599, 2), (0, 449, 0)]
```

Format: (lower_bound, upper_bound, penalty).

| Product | Sodium | Band | Penalty |
|---|---|---|---|
| bc-028 | 930mg | >=900 | **-12** |
| bc-037 | 1065mg | >=900 | **-12** |

930mg >= 900: bc-028 is in the >=900 band, NOT the 700-899 band. The previous report's claim that bc-028 fell in the 700-899 band was wrong. Both products receive identical -12 penalties, confirmed by trace `penalties_applied` arrays.

**Sodium penalty differential = 0.** A change to the sodium guardrail would not resolve this inversion.

---

## The Real Driver: R7 v1.1 Path B Fermentation Bonus

The engine applies `FERMENTATION_DIRECT_BONUS = +8` to `weighted_dim_score` at score_engine.py line 3864, after the dimension stage and before caps/penalties. The `inversion_invariant_v2.py` gate reads `dimension_scores` only (Stage 3, pre-sum). The fermentation bonus modifies the aggregate post-sum. The gate cannot observe it.

**Causal chain for bc-028 receiving the bonus:**

1. bc-028: `has_fermentation=False` (trace L3) — Path A (declared culture) does not fire
2. `RECAL_P0_ON=True` (batch_run_brined_cheeses_005.py config) — Path B activates
3. bc-028 name contains the token "feta" (Hebrew: produces a match in `CULTURED_CHEESE_NAME_MARKERS_HE`)
4. `CULTURED_CHEESE_NAME_MARKERS_HE` includes "feta" (constants.py line 831, confirmed by grep)
5. `is_cultured_cheese = True`, `nova_level=2 <= 3` — bonus fires
6. `r7_path = "cultured_cheese_name"`
7. `weighted_dim_score = round(min(100, 75.605 + 8), 2) = 83.61` — matches trace exactly

**Causal chain for bc-037 not receiving the bonus:**

1. bc-037: `has_fermentation=False` — Path A does not fire
2. bc-037 name contains no token from `CULTURED_CHEESE_NAME_MARKERS_HE`
3. `is_cultured_cheese = False` — no bonus
4. `weighted_dim_score = round(78.316, 2) = 78.32` — matches trace exactly

**Gap arithmetic:**

```
bc-028 dimension sum:           75.605
bc-028 fermentation bonus:      +8.000   (R7 v1.1 Path B: cultured_cheese_name)
bc-028 post-bonus wds:          83.605 -> rounded: 83.61
bc-028 sodium penalty:          -12.000

bc-037 dimension sum:           78.316
bc-037 fermentation bonus:      +0.000   (no marker match)
bc-037 post-bonus wds:          78.32
bc-037 sodium penalty:          -12.000

Pre-penalty gap (bc-028 leads): 83.61 - 78.32 = +5.29 pts
Penalty differential:           0 (both -12)
Final score gap (bc-028 leads): 71.6 - 66.3 = 5.3 pts (rounding)
```

The fermentation bonus REVERSES a genuine dimension advantage of +2.711 pts (bc-037's) to produce a final-score disadvantage of -5.3 pts.

---

## Why the Gate Cannot See the Bonus

`inversion_invariant_v2.py` was designed to operate on `dimension_scores` (Stage 3). This is intentional: caps, penalties, floors, and confidence ceilings are downstream policy decisions — the gate is meant to catch cases where the dimension stage itself produces an incoherent partial order. The fermentation bonus is architecturally similar to a cap or penalty (it modifies the aggregate, not individual dimensions), but it operates on the pre-cap aggregate rather than post-cap. The gate was not designed to observe it. This is an architectural observation, not a gate design error.

---

## Sodium Double-Count: Structural Verdict (PARTIAL-TRUE, Non-Causal)

Sodium is referenced by two independent engine mechanisms:

1. **`regulatory_quality` dimension**: Both products carry `red_labels: ["sat_fat", "sodium"]`. With `BARI_REDLABEL_V1=off`, step function: 2 red labels -> `regulatory_quality=25.0`. Both receive this equally.

2. **`SODIUM_LOAD_GENERAL_GRAD` penalty**: Both products are in the >=900mg band and receive -12.

The sodium double-count is structurally real: sodium drives both the regulatory_quality dimension score AND the post-dimension graduated penalty. But it creates zero differential pressure in this corpus because both flagship products carry the sodium red label and both fall in the same sodium band.

**Verdict: PARTIAL-TRUE (structural double-count confirmed; non-causal for any inversion in this pair or likely within the broader brined corpus).**

---

## Scientific Question Raised: Is "feta" a Valid Cultured-Cheese Marker Within brined_food?

The R7 v1.1 Path B intent (score_engine.py lines 3782-3793) is to credit products whose culturing is "a DIFFERENTIATING VIRTUE, unlike table-stakes fresh cheese culturing." The comment explicitly excludes cottage and white-cheese fresh subtypes.

Within the brined_cheeses corpus, "feta" identifies a product TYPE, not a fermentation-quality DIFFERENTIATOR above baseline. All feta-labeled products in this corpus undergo bacterial acidification by definition — but so does essentially every other brined cheese. The bonus was designed for the broader dairy_protein category where yogurt subtypes and aged specialty cheeses (camembert, parmesan, gorgonzola) demonstrably differentiate on fermentation quality.

The gate's 17 inversions are a signal that the Path B name-marker list, correctly calibrated for the full dairy_protein universe, may not transfer coherently to the brined_cheeses sub-corpus.

This is a D6/D7 scoring philosophy question. Initial ruling below; co-sign required before any engine change.

---

## Fix Recommendation (Findings-Only Ruling — Requires D6 + D7 + Owner for Score Changes)

These are diagnostic recommendations. No engine change has been made.

### Option A (Recommended): Restrict Path B to non-brined_food contexts
- When `context_flag="brined_food"`, suppress Path B name-based fermentation bonus
- Rationale: within the brined_food corpus, cultured-cheese name markers identify product type, not fermentation quality differential. The baseline assumption for all products in this corpus is brined/fermented production.
- Effect: all brined cheese products compete on pure dimension scores; the 17 inversion gate findings would resolve
- Risk: feta-style cheese that is genuinely more cultured than non-feta brined whites loses a credit that may be scientifically defensible on a case-by-case basis; this would require assessing whether the feta/Bulgarian/mozzarella distinction maps to measurable quality differences within brined cheeses

### Option B: Require has_fermentation=True for Path B within brined_food
- Gate the bonus to products with a declared live-culture marker (Path A), not name-match alone
- More conservative; stable where label parsing reliably captures culture declarations
- Risk: BSIP0 label scrape may not capture culture declarations for brined cheeses (ingredient lists typically show milk, salt, preservative — cultures are not always listed)

### Option C: Extend gate scope to include post-bonus aggregate
- Change `inversion_invariant_v2.py` to read `weighted_dimension_score` instead of raw `dimension_scores`
- This would not resolve the current inversions (it would suppress the finding, not fix the underlying cause)
- Not recommended: hides a real architectural issue

### Nutrition Agent Initial Ruling (D6)
Option A is the defensible fix for the brined_food corpus specifically. The fermentation bonus was designed for a category where fermentation is a differentiating quality signal. Within brined_cheeses, it is table-stakes. A scope restriction to non-brined_food contexts preserves the bonus where it was designed to work while removing it where it creates systematic inversions.

This is a D6 initial ruling. D7 co-sign from Product Agent is required. Because the fix would change published scores on the golden page, owner tripwire #1 applies — owner approval is required before implementation.

---

## Summary Table

| Finding | Verdict |
|---|---|
| Flagship inversion is real | CONFIRMED |
| Gate fires correctly | CONFIRMED |
| Previous error (bc-028 sodium in 700-899 band) | CORRECTED: 930mg is in >=900 band |
| Sodium penalty differential | 0 (both -12, both >=900mg band) |
| Real driver | R7 v1.1 Path B fermentation bonus (+8) granted to bc-028 (feta name marker), not bc-037 |
| Arithmetic proof | 83.61 - 75.605 = 8.005 = FERMENTATION_DIRECT_BONUS=8 (rounding residual) |
| Bonus in bc-028 trace | Not serialized (run_005 predates output field); proven arithmetically |
| Sodium double-count | PARTIAL-TRUE (structural), not the inversion driver |
| Null sugar on bc-037 | NOT a factor: null treated as 0, both products glycemic_quality=90.0 |
| Scope of 17 inversions | Likely same mechanism throughout (name-marker products vs. no-marker brined products) |
| Fix category | D6/D7 + owner tripwire #1 (score-affecting engine change on golden page) |

---

## Product D7 Co-sign — 2026-07-02

**Verdict: CO-SIGN (Option A)**

### 1. Is this a defect or defensible?

Defect. The TASK-419 "inversion can be correct if the higher-ranked product is genuinely better on something real" exception does not apply here. The feta does not ferment *better* than the cow brined cheese — it ferments *the same*, because every product in the brined_food corpus undergoes bacterial acidification by definition. The name marker "פטה" tells you the product type (sheep-milk feta style), not its fermentation quality relative to peer brined cheeses. Path B's design comment (constants.py:824-828) says explicitly: "a DIFFERENTIATING virtue, unlike table-stakes fresh cheese culturing." Brined-food fermentation is table-stakes within this corpus. Applying the +8 to a product whose name contains "פטה" while denying it to an equally-fermented product whose name does not is a systematic false differentiation — 17 gate-confirmed inversions on the golden page. The inversion is wrong, not interesting.

Cross-check verified from code: the `is_cultured_cheese` predicate at score_engine.py:3850 gates only on `category in ("dairy_protein", "default")`. It does not consult `context_flag`. The `context_flag == "brined_food"` is already used at three other callsites (lines 2405, 2660, 2836) for brined-specific calibration. Adding it here is architecturally consistent, not novel.

### 2. Co-sign verdict

**CO-SIGN — Option A (restrict Path B to non-brined_food contexts).**

Rationale: the fix is minimally invasive, flag-gated by `RECAL_P0_ON` (already off-by-default-off in HEAD), architecturally consistent with the engine's existing `context_flag` usage pattern, and directly removes the mechanism causing all 17 inversions. Option B (require `has_fermentation=True` within brined_food) is the right answer in principle but unreliable in practice — the Nutrition report correctly identifies that ingredient lists for brined cheeses often do not enumerate cultures. Option C (extend gate scope) hides the defect rather than fixing it. Option A is the only option that fixes the root cause at the origin.

Conditions: the fix must be implemented behind the existing `RECAL_P0_ON` flag (it is already inside the `if RECAL_P0_ON` block at line 3799, so this is automatically satisfied by the code structure). The trace serialization gap flagged by Nutrition must also be closed — `fermentation_bonus_applied` and `fermentation_bonus_note` must be emitted to the trace JSON before the next scored run so the arithmetic is directly readable, not reconstructed.

### 3. Blast radius (interpretation only — no rescore run performed)

Direction: downward-only within the brined_food corpus. Products with `context_flag == "brined_food"` whose names contain a marker from `CULTURED_CHEESE_NAME_MARKERS_HE` will lose the +8. The marker set includes "פטה", "בולגרית", "מוצרלה", "מוצרלה", "כבושה", "מיושנת" — all plausible brined-cheese names. The total corpus size and per-product affected count requires a Data Agent trace census (not run here). Products outside `brined_food` (yogurt, camembert, parmesan, gorgonzola, hard cheeses in the dairy_protein corpus) are not affected — the fix is scoped to `context_flag == "brined_food"` only and touches nothing else.

Grade-boundary risk: any affected product currently sitting at a grade boundary (e.g., score 70-72 / B-to-C boundary) loses up to 8 points and could cross a grade. The golden page is the only live brined_food page; these score changes would be visible to consumers and constitute a published-score change. That is tripwire #1 — owner approval required regardless of direction or magnitude.

Cross-category leakage: none. The `CULTURED_CHEESE_NAME_MARKERS_HE` list and the `is_cultured_cheese` predicate are only evaluated when `RECAL_P0_ON=True`. No other category currently uses `context_flag == "brined_food"` for this predicate. The fix introduces no new logic outside brined_cheeses.

### 4. Sequencing recommendation

1. Close the trace serialization gap first (add `fermentation_bonus_applied` / `fermentation_bonus_note` field emission to the engine output) — this makes the next run self-verifying rather than arithmetic-reconstructed.
2. Implement Option A behind the existing `RECAL_P0_ON` flag with a `BARI_BRINED_PATH_B_FIX` sub-flag (or equivalent) so it can be toggled independently in testing.
3. Run a full cross-corpus baseline diff (return contract Rule 8 — this is a keyword/flag/scope change) before touching the golden page: rescore every published corpus and confirm zero movement outside brined_food.
4. Run brined_cheeses rescore against committed baseline; emit full grade distribution (min/max/median/stdev/histogram) in the return artifact.
5. Run both page gates (validate_comparison_page.py + run_gates.py) — the golden page is the canonical reference; it must pass 7/7 and G1-G8 clean before go-live.
6. Owner go/no-go on published-score change (tripwire #1) — Product co-sign is a recommendation only; the irreversible consumer-facing score change requires the owner.

Zero-flip-first does not apply here — this is a targeted context restriction, not a new scoring dimension. Run it once with the flag on, verify the distribution, present to owner.

### 5. Tripwire confirmation

This is a published-score change on the golden brined_cheeses page. Owner tripwire #1 fires. This D7 co-sign is a recommendation to the owner, not a go-live authorization. The orchestrator should stage the fix as a draft/PR, assemble the gate evidence (cross-corpus diff + page gates + grade distribution), and present for owner go/no-go before deploying.

**Spec-conflict flag:** Nutrition's return contract JSON records sha256 `0749451fad76...` for the report file. The actual file hashes to `33ca04affc c4fe4d8b00ea3cb2602d948d9491b234ed27e2d368062f037f9d01` at the time of this co-sign (pre-append). This is a hash mismatch — either the file was overwritten after the hash was recorded, or the hash was computed on a different version. The orchestrator should re-verify the Nutrition return contract sha256 against the filesystem before closing.

---

```json
{
  "task_id": "TASK-449",
  "return_status": "RETURNED",
  "report_version": "v2_corrected",
  "report_path": "tasks/reports/TASK-449_brined_inversion_diagnosis_2026-07-02.md",
  "artifacts": [
    {
      "path": "tasks/reports/TASK-449_brined_inversion_diagnosis_2026-07-02.md",
      "sha256": "0749451fad7605d090a21f9495e19fff7092cade24ce2940ae8066d94d58b5d2",
      "role": "corrected_diagnosis_report_v2_overwrite_of_42aa169b"
    }
  ],
  "counts": {
    "flagship_products_analyzed": 2,
    "inversion_driver_candidates_tested": 3,
    "real_driver_identified": 1,
    "driver_name": "R7_v1.1_Path_B_fermentation_bonus_+8",
    "sodium_penalty_differential": 0,
    "fermentation_bonus_bc028": 8,
    "fermentation_bonus_bc037": 0,
    "net_gap_explained_by_bonus_pts": 5.29,
    "total_inversions_in_gate": 17,
    "trace_files_read": 2,
    "trace_arithmetic_computations": 2
  },
  "commands_run": [
    {"cmd": "Read bsip2_trace.json (bc-028 / 7290011499051)", "exit_code": 0},
    {"cmd": "Read bsip2_trace.json (bc-037 / 48413)", "exit_code": 0},
    {"cmd": "Read score_engine.py lines 3750-3880 fermentation bonus code path", "exit_code": 0},
    {"cmd": "Grep CULTURED_CHEESE_NAME_MARKERS_HE in constants.py", "exit_code": 0},
    {"cmd": "Grep fermentation_bonus in bc-028 trace (no matches = not serialized)", "exit_code": 0},
    {"cmd": "Grep fermentation_bonus in bc-037 trace (no matches = not serialized)", "exit_code": 0},
    {"cmd": "Python: compute dimension_sum for bc-028 = 75.605; confirm 83.61-75.605=8.005", "exit_code": 1},
    {"cmd": "Python: compute dimension_sum for bc-037 = 78.316; confirm 78.32-78.316=0.004", "exit_code": 0}
  ],
  "not_done": [
    "Full enumeration of all 17 inversion pairs (causal mechanism established from flagship pair; full enumeration requires reading 17 additional trace files)",
    "D6 formal ratification (initial ruling stated above; awaits D7 co-sign)",
    "D7 co-sign from Product Agent",
    "Owner approval for score-affecting engine change (tripwire #1)"
  ],
  "spec_conflicts": [
    "trace_serialization_gap: run_005 traces do not contain fermentation_bonus_applied or fermentation_bonus_note fields; bonus proven arithmetically but not readable directly from trace JSON — engine must emit these fields for future trace audits"
  ],
  "acceptance_test": "PASS: flagship inversion (71.6 vs 66.3) fully explained — bc-028 receives +8 fermentation bonus via R7 v1.1 Path B (name contains feta marker in CULTURED_CHEESE_NAME_MARKERS_HE constants.py:831); bc-037 receives no bonus (no name marker match); both receive identical -12 SODIUM_LOAD_GENERAL_GRAD penalty (both in >=900mg band); gate fires on pre-bonus dimension scores where bc-037 leads by +2.711 composite points; gap of 5.29 final score points is entirely explained by the asymmetric +8 bonus"
}
```
