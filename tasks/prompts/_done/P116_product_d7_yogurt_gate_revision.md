# P116 — TASK-278 Phase-6: D7 Gate Revision — Yogurt×Sugar Pilot Gate (route: C1 Product Agent)
# Two hard gate failures from P115 pilot: C1 (tied clusters) + C3 (inversion gap). Revise both.

**Repo:** `C:\Bari`
**Task:** `C:\Bari\tasks\TASK-278.md` (Phase-6 gate revision)
**P115 return:** `tasks/returns/P115_return.md`
**Prior gate spec:** `02_products/yogurt_system/methodology/yogurt_sugar_d7_cosign_v1.md`

---

## Context

P115 wired yogurt×sugar SR and ran the dual-run pilot (`run_yogurt_shelfrel_v2/`). The mechanism LANDS:
- **46 movers** (of 72 with known sugars_g), **5 grade changes**, **0% absorption** — confirmed
- **C10 milk CRITICAL: PASS** — all 20 milk run_005_headpin products delta=0.0 ✓ (frozen invariant safe)
- **C9 no scope bleed: PASS** — 0 non-yogurt dairy_protein products with non-zero delta ✓

**Two hard failures (C1 + C3):**

### C1 FAIL — tied-score clusters: 4=4 (unchanged)
The C1 criterion required FEWER tied-score clusters at flag-on vs flag-off. The pilot shows 4 products tied at flag-on and 4 products tied at flag-off — unchanged. The SR mechanism fires on 46 of 72 products, so why are 4 products still tied? Likely the 14 null-sugars products (no SR adjustment) + some integer rounding artifacts create these ties. The C1 criterion as written doesn't account for the null-sugars exclusion.

### C3 FAIL — inversion gap: 0.6 pts < 2.0 threshold
The named inversion pair (7290110321697 9.8g vs 7290102397600 13.6g) fails because **BOTH products are above the median (5.45g)**, so BOTH received penalties (not a below-median relief vs above-median penalty inversion):
- Product A (9.8g): z=(9.8-5.45)/4.299=+1.01 → 2pt PENALTY (flag_on=59.0, from 61.0)
- Product B (13.6g): z=(13.6-5.45)/4.299=+1.90 → 4pt PENALTY (flag_on=58.4, from 62.4)
- Gap = 59.0-58.4 = 0.6 pts (direction CORRECTED — A now > B, but gap < 2.0)

**D6 sign error caught:** D6 claimed "A z=1.01→+1pt (relief)" — wrong; z=+1.01 is above median → penalty (-2pt). D7 accepted without catching this. The named pair was never a genuine below-median vs above-median inversion — it was a within-surcharge-zone differential penalty test. That's still useful evidence, but not a gap-inversion.

**The yogurt shelf has no true below-median/above-median inversion pair that creates ≥2.0 gap** because:
- Products below median (≤5.45g) have low baseline scores from NOVA/additives (e.g., 4.5g at 36.4/D — backbone drives them low for other reasons)
- Products above median (≥9.8g) have higher baseline scores despite more sugar (e.g., 9.8g at 61.0/C — fewer additives)
- The backbone score gap (7+ pts) exceeds the maximum SR delta range (±6 pts at P_max/B_max caps)

---

## Your task: propose revised gate criteria for C1 and C3

### Section A: Diagnose root causes from pilot data

**A1 — C1 diagnosis:**
The pilot returns `run_record.json` in `02_products/yogurt_system/bsip2_outputs/run_yogurt_shelfrel_v2/`.
Read it to find:
- Which 4 products are tied at flag-on? Which 4 at flag-off? Are they the same products?
- Are the tied products null-sugars products (delta=0) or SR-firing products that landed on the same score?
- Does the SR mechanism reduce within-SR-firing-group ties (i.e., among the 46 movers, are there fewer ties)?

**A2 — C3 diagnosis:**
Confirm from the pilot that no below-median/above-median inversion pair produces a ≥2.0 gap. List the 3 best available corrected pairs (A below median, B above median, A post-SR > B post-SR) and their actual gaps. Report the best achievable gap from the current pilot data.

---

### Section B: Propose revised criteria (you decide — all 3 proposals must be falsifiable)

**B1 — C1 revised (pick ONE):**

Option A: **SR-firing group resolution** — among the 46 SR-firing yogurt products (those with non-zero delta), the number of tied pairs decreases or stays 0 at flag-on vs flag-off. The 14 null-sugars products are excluded from this count (they can't change). Rationale: C1's purpose is to check that SR adds resolution within the SR-eligible population.

Option B: **Delta distribution monotonicity** — the mean delta for above-median products (sugars_g > 5.45g) is negative AND the mean delta for below-median products (sugars_g < 5.45g, non-null) is positive or zero. This directly tests that the mechanism fires in the correct direction across both clusters. More informative than counting clusters.

Option C: **Keep C1 as is (tied 4=4 = genuine failure)** — if the tied products are SR-firing products (not null-sugars), this is a real signal of insufficient resolution.

Recommend Option A, B, or C. Justify.

**B2 — C3 revised (pick ONE):**

Option A: **Best-achievable inversion gap ≥ 0.5 pts** — replace the named pair (9.8g vs 13.6g) with the best genuine below-median/above-median inversion identified in the pilot (if any exist). Lower the gap threshold from 2.0 to 0.5 pts. Rationale: 0.5 pt gap is directionally significant given scale=4.299 (it's ~0.12 sigma). Minimum evidence of mechanism.

Option B: **Distribution separation evidence** — drop the named-pair inversion entirely. Replace with: (i) at least 3 above-median products have negative delta (penalized), AND (ii) at least 1 below-median product has positive or zero delta (neutral/relieved), AND (iii) the mean delta for products with sugars_g ≥ 9.0g is < 0. This is distribution-level evidence that the mechanism fires in the correct direction.

Option C: **Signed-rank separation** — the median delta for products with sugars_g > median (5.45g) must be negative. The median delta for products with sugars_g ≤ median must be ≥ 0. If both hold, C3 passes.

Recommend one option. Justify. If you choose to lower the gap threshold (Option A), you must identify the specific new named pair from the pilot data.

**B3 — C2-revised(D) reassessment:**
The pilot returned C2-D = 0.4118 (mean delta for sugars≤5g = 0.4118 ≥ 0, PASS). Confirm this is genuinely positive (not a rounding artifact) and explain why below-median products are getting positive deltas if the z-threshold is 0.3 and most are at z=-0.1 to -0.4. (If most products below median are within the z-threshold and getting delta=0, the mean ≥ 0 is trivially satisfied and not informative. Consider whether C2-D should be revised to "mean delta for sugars≤4g > 0" which tests actual relief, not near-neutral behavior.)

---

### Section C: Lock revised gate summary

After deciding B1/B2/B3, write the revised gate table (all 11 criteria, marking revised ones). Include what evidence from the **existing P115 pilot data** would be needed to score the revised C1/C3 — if the existing data is sufficient, no re-pilot is needed.

---

## Definition of Done

- [ ] A1 diagnosis: which 4 products tied at flag-on/off; null-sugars or SR-firing?
- [ ] A2 diagnosis: 3 best below-median/above-median corrected pairs with actual gaps
- [ ] B1: C1 revision decided (Option A, B, or C) with justification
- [ ] B2: C3 revision decided (Option A, B, or C) with justification
- [ ] B3: C2-D assessment (confirm valid or propose revision)
- [ ] Revised gate table (11 criteria): updated C1/C3 (and C2-D if revised), others unchanged
- [ ] Statement on whether existing P115 pilot data is sufficient to score revised C1/C3, or whether a re-pilot is needed
- [ ] engine_invariants 342 PASS (no engine edits expected — governance only)
- [ ] OFF=0, no engine files modified

---

## Constraints

- **No engine edits** — governance only
- **No score movement** — 0 published scores
- **Do not re-run the pilot** — use existing `run_yogurt_shelfrel_v2/` pilot data for analysis
- **OFF ban absolute**
- **Must preserve C10 milk safety gate (CRITICAL)** — non-negotiable; milk frozen invariant
- **Must preserve C7/C8 anti-immunity / floor compliance gates** — non-negotiable

---

## Return format

Write to `C:\Bari\tasks\returns\P116_return.md`:

```json
{
  "task_id": "TASK-278",
  "phase": "Phase-6 yogurt×sugar gate revision (D7)",
  "status": "RETURNED",
  "return_date": "2026-06-14",
  "agent": "product-agent",
  "c1_root_cause": "...",
  "c1_tied_products": [{"barcode": "...", "score": <f>, "null_sugars": true/false}],
  "c3_root_cause": "...",
  "c3_best_available_pairs": [
    {"barcode_a": "...", "sugars_a": <f>, "score_off_a": <f>, "score_on_a": <f>, "barcode_b": "...", "sugars_b": <f>, "score_off_b": <f>, "score_on_b": <f>, "gap_on": <f>}
  ],
  "c1_revised_option": "A/B/C",
  "c1_revised_pass_condition": "...",
  "c3_revised_option": "A/B/C",
  "c3_revised_pass_condition": "...",
  "c3_revised_pair_or_distribution": "...",
  "c2d_assessment": "valid/revised",
  "c2d_revised_if_needed": "...",
  "revised_gate_c1_pass": true/false,
  "revised_gate_c3_pass": true/false,
  "repilot_needed": true/false,
  "repilot_reason": "...",
  "revised_gate_table": [
    {"criterion": "C1", "name": "...", "pass_condition": "...", "changed": true, "evidence_available": true/false},
    {"criterion": "C2", "name": "...", "pass_condition": "...", "changed": false, "evidence_available": true},
    {"criterion": "C3", "name": "...", "pass_condition": "...", "changed": true, "evidence_available": true/false},
    ...
  ],
  "engine_invariants": "342 PASS",
  "off_used": false,
  "not_done": []
}
```

**Do not close. Propose RETURNED — orchestrator verifies and either closes Phase-6 (if revised criteria pass on existing data) or dispatches a re-pilot.**

Machine-readable return contract:

```json
{
  "artifacts_claimed": [],
  "claims_verified_by_agent": false,
  "propose": "RETURNED"
}
```
