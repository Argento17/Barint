# P114 — TASK-278 Phase-6: Product D7 Co-sign — Yogurt × Sugar Enrollment (route: C1 Product Agent)
# Ratify D6 proposal; decide 5 open questions; register EV-088; lock pilot gate criteria

**Repo:** `C:\Bari`
**Task:** `C:\Bari\tasks\TASK-278.md` (Phase-6, yogurt×sugar D7 co-sign)
**D6 proposal:** `02_products/yogurt_system/methodology/shelf_relative_sugar_enrollment_yogurt_v1.md`
**D6 return:** `tasks/returns/P113_return.md`
**Evidence registry:** `03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md`

---

## Context

TASK-278 Phase-6: yogurt×sugar shelf-relative enrollment. Nutrition Agent (D6/P113) completed the
enrollment proposal. Summary of proposal:

- **Scope guard**: Option A — `category == "dairy_protein" AND category_subtype in CULTURED_YOGURT_SUBTYPES`. No router edit needed. `CULTURED_YOGURT_SUBTYPES` already defined in constants.py and already used by the fermentation bonus gate in score_engine.py.
- **Corpus**: `run_yogurt_006` — 88 total, 87 yogurt-only (1 cereal outlier), 74 with known sugars_g.
- **Stats (n=74, IQR-primary)**: median=5.45g, IQR=5.80g, MAD=2.55g, robust_scale=4.299
- **Bands**: P_max=6, B_max=3, asymmetric P>B
- **Floor**: 62 for sugars_g ≥ 12.0g
- **Anti-Immunity proof**: 62+3=65<70 ✓
- **Named inversions**: 2 confirmed from run_yogurt_006 traces (see D6 doc)
- **EV-088** designated (not yet registered)

**Prior context for yogurt SR:**
- P103 yogurt diagnostic validated mechanism on yogurt shelf: 61 movers, 8 grade changes, 0% absorption (vs biscuits = 0 grade changes / full absorption). Yogurt is a LAND category.
- D7 co-sign from P98/P101 established the program-level conditions that apply here.

---

## Your task: ratify + decide 5 open questions + register EV-088 + lock pilot gate

### A. Ratify D6 proposal

Read `02_products/yogurt_system/methodology/shelf_relative_sugar_enrollment_yogurt_v1.md` in full.
Confirm or flag each element:
1. Scope guard Option A (no router edit)
2. Corpus n=74 (with sugars_g) out of 87 yogurt-only products
3. Stats: median=5.45/IQR=5.80/scale=4.299 (IQR-primary)
4. Asymmetric P>B (P_max=6, B_max=3)
5. Floor=62/threshold=12.0g / Anti-Immunity 65<70
6. Named inversions quality (are the 2 pairs real and directionally correct?)

### B. Decide 5 open questions

**D7-YS-01: P_max — 6 or 8?**
D6 proposes P_max=6 (standardized, same as cereals/biscuits). P103 pilot used P_max=8. Yogurt has a
tighter IQR (4.299 vs cereals 11.861) so the SAME P_max=6 produces smaller absolute adjustments on
yogurt. Higher P_max=8 would produce larger adjustments for above-median yogurts.
- **Anti-Immunity check**: raising to 8 does NOT affect immunity (floor controlled by B_max, not P_max)
- Recommend 6 or 8, with justification.

**D7-YS-02: Floor value — 62 or different?**
D6 proposes floor=62 for sugars_g ≥ 12.0g. Context:
- Biscuits floor=55 (very high sugar, energy-dense, more restrictive)
- Cereals floor=62 (same as this proposal — same class of concern)
- Yogurts in the 12–25g range: from run_yogurt_006 traces, what do these products score at flag-off? If any score below 62 already at baseline (flag-off), the floor is non-binding (OK). If they score above 62, the floor needs to be ≤ their maximum expected flag-on score to be effective.
- Confirm floor=62 adequacy or recommend an adjustment. Note: D7 must not set a floor above the current backbone scores of high-sugar yogurts (that would cap them lower than the backbone already does — which would be wrong; the floor's purpose is to prevent SR-relief from pushing high-sugar products above it, not to additionally penalize backbone scores).

**D7-YS-03: Threshold — 12.0g or different?**
D6 proposes floor threshold at 12.0g (dessert territory). Context: yogurt median=5.45g, Q3=9.7g. 
At 12.0g a product is well above Q3 (roughly top 25%). Review the trace distribution to confirm 12.0g
is the right threshold for "clearly high sugar" in the yogurt context. Alternative: 10.0g (above Q3).

**D7-YS-04: Near-median relief threshold — 0.5 z-units or 0.3?**
D6 proposes minimum z-magnitude of 0.5 before SR fires (to suppress noise near the median). With scale=4.299,
z=0.5 corresponds to |sugars_g - 5.45| ≥ 0.5 × 4.299 = 2.15g from median. Products within 2.15g of the
median (sugars in ~3.3–7.6g) would receive zero adjustment.
- 0.5 threshold: tighter, reduces noise but misses some below-median products
- 0.3 threshold: looser, picks up products at 3.9g–7.0g range (Q1-range products get relief)
- For cereals, the analog resolution at scale=11.861 with any threshold: a 7.5g cereal gets z=(7.5-13)/11.861=-0.464 and received +1pt in P112. This suggests the cereals implementation fires at z=-0.464 (< 0.5 magnitude). Check whether cereals has any explicit z-threshold guard in score_engine.py or whether it's purely the B_max cap.
- Decide: 0.5 or 0.3, or no explicit threshold (let B_max=3 naturally cap near-median relief to near-zero via the band lookup).

**D7-YS-05: Null-sugars treatment**
14 yogurt products (87-73=14) have null sugars_g in run_yogurt_006. When SR fires for yogurt, what happens to a product with null sugars_g?
Options:
- (A) **No adjustment** (delta=0, excluded from SR computation) — safest; missing data = no opinion
- (B) **Median imputation** (sugars_g=median → z=0 → SR fires but delta≈0) — equivalent to A for the score
- Option A is consistent with the missing-data discard rule (owner 2026-06-13: "if a product's data isn't found one-shot, DISCARD it"). Recommend Option A.
- Confirm or override.

### C. Register EV-088

After deciding the questions, register EV-088 in `03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md`.

EV-088 covers: yogurt×sugar shelf-relative enrollment. Format consistent with existing entries. Include:
- Category: yogurt (dairy_protein subtype: CULTURED_YOGURT_SUBTYPES)
- Nutrient: sugars_g
- Scope guard: Option A (category_subtype in CULTURED_YOGURT_SUBTYPES, no router edit)
- Stats: median=5.45g, IQR=5.80, scale=4.299 (IQR-primary), n=74
- Bands: P_max=<D7-decided>, B_max=3, floor=<D7-decided>, threshold=<D7-decided>g
- Anti-Immunity: floor+3<70 ✓
- Named inversions: 2 (7290110321697 vs 7290102397600; 7290102396740 vs 7290102393060)
- Date: 2026-06-14

**Verify EV-088 is the next free id** (check that no EV-088 already exists in the registry).

### D. Lock pilot gate criteria

Lock the pilot gate criteria for the yogurt×sugar pilot (to be run in Phase-6 wire+pilot step).
Pattern same as P110 cereals gate (11 criteria), adjusted for yogurt context.

Key gate criteria to define:
1. **resolution_restored**: fewer tied-score clusters flag-on vs flag-off (cereal gate precedent)
2. **grade_dist_and_magnitude** (C2-revised equivalent): (A) 0 yogurts with sugar≥12g at grade B (score≥70) at flag-on; ≥2 yogurts with sugar≤5g at grade A/S (score≥80); (C) mean|delta|≥0.5 among SR-firing yogurts; mean delta≥0 for sugar≤5g products
3. **inversion_gap** (C3 equivalent): gap (lower-sugar barcode flag_on minus higher-sugar barcode flag_on) for at least 1 named inversion pair — propose minimum gap in pts
4. **min_movers**: ≥ N yogurt products with clean_delta ≠ 0 (adjust for n=74 basis)
5. **min_grade_changes**: ≥ 1 yogurt grade change
6. **max_absorption**: ≤ 40% among SR-firing yogurts (delta=0 despite SR expected to fire)
7. **anti_immunity**: 0 yogurts with sugar ≥ 12g at grade B (score ≥ 70) at flag-on
8. **floor_compliance**: all sugars ≥ 12g yogurt products: flag-on score ≤ floor value
9. **no_scope_bleed**: 0 non-yogurt dairy_protein products (milk, hard cheese, brined cheese, kefir) with non-zero clean_delta
10. **frozen_byte_id**: milk run_005_headpin byte-identical when BARI_SHELF_RELATIVE_V1=True (yogurt-SR flag-on must not touch milk; milk is frozen invariant)
11. **flag_off_drift**: documentation-only mismatch count vs committed baseline

**Critical on C10 (no_scope_bleed):** yogurt and milk share `dairy_protein`. If scope guard fails (a milk product has `category_subtype in CULTURED_YOGURT_SUBTYPES` due to miscoding), SR would fire on milk scores — which are a FROZEN INVARIANT. This is the most important safety check for yogurt×sugar.

**Critical on frozen milk:** The pilot script must verify milk run_005_headpin is byte-identical. Any milk score movement = immediate pilot FAIL.

---

## Definition of Done

- [ ] D6 enrollment doc read in full; all 6 elements ratified or flagged
- [ ] All 5 D7 open questions resolved with justification
- [ ] EV-088 registered (verify free id first; 0 deletions to existing entries)
- [ ] Pilot gate criteria locked (11 criteria, with yogurt-specific C2/C3/C4/C9/C10 thresholds)
- [ ] `cereals_d7_cosign_v1.md` equivalent written at: `02_products/yogurt_system/methodology/yogurt_sugar_d7_cosign_v1.md`
- [ ] engine_invariants 342 PASS
- [ ] OFF=0
- [ ] No engine edits (score_engine.py, constants.py, router_v2.py MUST NOT be modified)

---

## Constraints

- **NO engine edits** — governance only; score_engine.py/constants.py/router_v2.py untouched
- **NO rescore / no pilot** — that's the next step (wire + pilot, separate phase)
- **OFF ban absolute**
- **Frozen invariant:** milk run_005_headpin is FROZEN. Do not reference or modify milk scores. The pilot gate must enforce milk byte-identity.
- **0 score movement** — D7 co-sign does not move any scores

---

## Return format

Write to `C:\Bari\tasks\returns\P114_return.md`:

```json
{
  "task_id": "TASK-278",
  "phase": "Phase-6 yogurt×sugar D7 co-sign",
  "status": "RETURNED",
  "return_date": "2026-06-14",
  "agent": "product-agent",
  "d6_ratified": true,
  "d7_decisions": {
    "D7-YS-01_P_max": <6 or 8>,
    "D7-YS-01_justification": "...",
    "D7-YS-02_floor_value": <f>,
    "D7-YS-02_justification": "...",
    "D7-YS-03_floor_threshold_g": <f>,
    "D7-YS-03_justification": "...",
    "D7-YS-04_near_median_threshold_z": <f or null>,
    "D7-YS-04_justification": "...",
    "D7-YS-05_null_sugars_treatment": "no_adjustment or median_imputation",
    "D7-YS-05_justification": "..."
  },
  "ev_088_registered": true,
  "ev_088_registry_line": <n>,
  "anti_immunity_proof": "floor(<f>) + B_max(3) = <sum> < 70 PASS",
  "pilot_gate_criteria_count": 11,
  "pilot_gate_criteria": [
    {"criterion": "C1", "name": "...", "pass_condition": "..."},
    ...
  ],
  "cosign_doc": "02_products/yogurt_system/methodology/yogurt_sugar_d7_cosign_v1.md",
  "engine_invariants": "342 PASS",
  "off_used": false,
  "not_done": []
}
```

**Do not close. Propose RETURNED — orchestrator verifies + dispatches Phase-6 wire + pilot next.**

Machine-readable return contract:

```json
{
  "artifacts_claimed": [
    {"path": "02_products/yogurt_system/methodology/yogurt_sugar_d7_cosign_v1.md", "sha256": "<sha>"},
    {"path": "03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md", "sha256": "<sha>"}
  ],
  "claims_verified_by_agent": false,
  "propose": "RETURNED"
}
```
