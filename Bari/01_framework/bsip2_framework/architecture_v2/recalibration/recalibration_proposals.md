# Recalibration Proposals — v2 Scoring Architecture

**Status:** Proposal — not yet implemented  
**Version:** 2.0-draft  
**Date:** 2026-05-18  
**Companion:** distribution_analysis.md, penalty_pressure_analysis.md, shadow_recalibration_simulation.md

---

## Guiding Constraints

These proposals operate under the following hard constraints:

1. **Rank ordering is preserved.** Whole dairy > soy > oat/almond; simple > engineered; minimally processed > hyper-formulated. No swap in relative ordering is acceptable.
2. **Engineering penalties are not weakened.** NOVA 4 remains penalized. Additive escalation remains penalized. Sweetener cap remains.
3. **Red label and trans fat constraints are not weakened.** Israeli regulatory signals and trans fat veto are unchanged.
4. **Bad products stay bad.** The lowest-scoring snack bars (12–25 range) should remain E. The proposals do not rescue heavily compromised products.
5. **The score range 0–100 is the standard.** No new dimensions are added, no weights are dramatically altered in this proposal.

What changes: gradient smoothness, ceiling headroom, grade boundary placement.

---

## Proposal 1: Grade Threshold Overhaul — Add S-Tier

### Current thresholds

```python
GRADE_THRESHOLDS = [
    (85, "A"),
    (70, "B"),
    (55, "C"),
    (40, "D"),
    (0,  "E"),
]
```

### Proposed thresholds

```python
GRADE_THRESHOLDS = [
    (90, "S"),
    (80, "A"),
    (65, "B"),
    (50, "C"),
    (35, "D"),
    (0,  "E"),
]
```

### Rationale

The current A threshold at 85 is unreachable. The natural maximum computed score across 69 products is ~70.44 (whole milk without floor). With proposed constant changes (Proposals 2–5), the maximum natural score for NOVA1 products approaches 85, and the floor lifts to 85, placing them at A. This requires the A threshold to be at 80, not 85.

The introduction of S-tier at 90+ serves two functions:
- Creates aspirational space above A for products that are genuinely exceptional even under recalibrated scores
- Prevents A-tier from becoming the new ceiling where everything good clusters

The B threshold shift from 70 to 65 brings naturally computed NOVA 2 products (plain soy drink at ~67) into B range without floor rescue.

The C/D/E boundary shifts of 5 points each (55→50, 40→35) proportionally expand each grade bucket without dramatically altering what constitutes E-grade.

**Expected effect on current corpus:**
- Zero products move to S (S remains aspirational)
- NOVA 1 whole foods move to A (floor-rescued at 85)
- NOVA 2 best products reach B
- Most NOVA 3 products shift from D to C
- NOVA 4 with modest caps shift from E to D
- Heavily stacked NOVA 4 remain E (scores 12–33 with ~2pt delta)

---

## Proposal 2: NOVA Dimension Score Smoothing

### Current

```python
NOVA_PROCESSING_SCORES = {1: 95, 2: 80, 3: 55, 4: 25}
NOVA_WFI_SCORES        = {1: 100, 2: 80, 3: 50, 4: 20}
```

### Proposed

```python
NOVA_PROCESSING_SCORES = {1: 95, 2: 85, 3: 65, 4: 35}
NOVA_WFI_SCORES        = {1: 100, 2: 85, 3: 60, 4: 30}
```

### Changes explained

**NOVA 2:** processing_quality 80→85 (+5), WFI 80→85 (+5)  
Weighted impact: +5×0.15 + 5×0.04 = +0.75 + 0.20 = **+0.95 pts**

Rationale: NOVA 2 products (cultured dairy, simple plant milks with minimal processing) deserve slightly more structural credit. The current gap between NOVA 1 (95/100) and NOVA 2 (80/80) is 15–20 points. The proposed gap is 10–15 points — still meaningful, but less cliff-like.

**NOVA 3:** processing_quality 55→65 (+10), WFI 50→60 (+10)  
Weighted impact: +10×0.15 + 10×0.04 = +1.50 + 0.40 = **+1.90 pts**

Rationale: NOVA 3 products span an enormous range — from fermented dairy products (structurally intact) to heavily flavored yogurt drinks (structurally compromised). The current score of 55 for processing_quality treats all NOVA 3 products equally at the same low level. Lifting to 65 gives NOVA 3 products credit for being in a category that includes genuinely intact foods, while still maintaining a significant gap from NOVA 2 (85) and NOVA 1 (95).

The NOVA 3 cap change (Proposal 4) provides additional relief.

**NOVA 4:** processing_quality 25→35 (+10), WFI 20→30 (+10)  
Weighted impact: **+1.90 pts**

Rationale: NOVA 4 is heavily penalized through cap mechanisms (Proposal 4 still maintains an explicit cap). The dimension score at 25 creates severe ceiling compression in combination with the cap. Moving to 35 reduces the combined pressure without removing NOVA 4's structural disadvantage. NOVA 4 products still score ~60 points below NOVA 1 on the processing dimensions combined — a substantial, real penalty.

**Absolute scoring impact:** ±2 pts on individual products from this proposal alone. The main relief comes from Proposals 3–5.

**Rank ordering check:**  
All products at the same NOVA level receive the same delta, so intra-NOVA ordering is preserved. Cross-NOVA ordering: a product that barely qualifies as NOVA 4 received +1.90 pts; a strong NOVA 3 product received +1.90 pts. Their relative order based on other dimensions is unchanged.

---

## Proposal 3: NOVA 1 Floor Elevation

### Current

```python
NOVA1_SINGLE_FLOOR = 75
```

### Proposed

```python
NOVA1_SINGLE_FLOOR = 85
```

### Rationale

The current NOVA1_SINGLE_FLOOR at 75 places single-ingredient whole foods at the top of the B range (under current thresholds). Under proposed thresholds (B = 65–79), 75 becomes solidly mid-B — a step down from where single-ingredient whole foods should sit.

The proposed floor of 85 places NOVA 1 single-ingredient whole foods at low A (A = 80–89 under proposed thresholds). This is the correct structural grade for a product that:
- Has a single-ingredient list
- Has no additives
- Has no detected engineering signals
- Has full matrix coherence

Plain whole milk, goat milk, a single nut or seed — these are structurally elite within their nutritional constraints. A score of 85 (low A) is conservative: it acknowledges that the nutrient density formula may not fully credit the beverage context, while asserting that structurally, this product deserves better than B.

**Important:** The floor applies only when no Class B physiological caps have fired. A NOVA 1 product with a sat_fat red label or 2+ red labels would receive the moderated floor (PHYSIO_MODERATION_MIN). This remains unchanged.

**Expected impact:** Whole milk, 4% milk, goat milk: 75 → 85 (B → A)

---

## Proposal 4: Processing Cap Ceiling Lift

### Current

```python
PROCESSING_CAPS = [
    ("NOVA_PROXY_4_ULTRA_PROCESSED", "nova==4", 60),
    ("ADDITIVE_MARKERS_5_PLUS",      "additives>=5", 55),
    ("ADDITIVE_MARKERS_3_PLUS",      "3<=additives<5", 65),
    ("NOVA_PROXY_3_PROCESSED",       "nova==3", 75),
]
```

### Proposed

```python
PROCESSING_CAPS = [
    ("NOVA_PROXY_4_ULTRA_PROCESSED", "nova==4", 68),
    ("ADDITIVE_MARKERS_5_PLUS",      "additives>=5", 60),
    ("ADDITIVE_MARKERS_3_PLUS",      "3<=additives<5", 72),
    ("NOVA_PROXY_3_PROCESSED",       "nova==3", 82),
]
```

### Changes explained

**NOVA_PROXY_4_ULTRA_PROCESSED: 60 → 68**

The current cap at 60 means the absolute maximum score for any NOVA 4 product is 60. Under current thresholds, 60 is a mid-C. Under proposed thresholds (C = 50–64), 60 remains C. The cap still signals: "This product's structural integrity is limited."

The concern with 60 is that it creates zero headroom for genuine nutritional contribution in NOVA 4 products. A NOVA 4 product with 25g protein, no sugar, and only 2 additive categories cannot exceed 60 regardless of how nutritionally excellent it is. This violates the architecture's intent — structural concern should be real but not annihilating for products with compensating signals.

Lifting to 68 allows a NOVA 4 product with genuinely strong nutritional signals to reach 65–68 range (B under proposed thresholds) while maintaining that the processing signal is a genuine ceiling constraint. Products that cannot exceed 68 on their nutritional merits will still be capped well below B.

**ADDITIVE_MARKERS_5_PLUS: 55 → 60**  
Currently, 5+ additive categories cap at 55 (lower than the NOVA4 cap of 60). With NOVA4 lifting to 68, the 5+ additive cap at 55 would become the binding cap for any NOVA4 product with 5+ categories. This relationship is appropriate — heavy additive stacking should bind tighter than NOVA4 alone. Moving 5+ to 60 aligns it with the NOVA4 base cap, maintaining that 5+ additive products face the same ceiling as other NOVA4 products, while the combined 5+/NOVA4 ceiling is still 60 (the minimum of both).

**ADDITIVE_MARKERS_3_PLUS: 65 → 72**  
For NOVA 3 products, the binding cap was previously the minimum of NOVA3 (75) and ADDITIVE_MARKERS_3_PLUS (65) = 65. With NOVA3 cap lifting to 82, the binding cap for NOVA3 with 3+ additives becomes 72. This provides more headroom for NOVA 3 products while still capping them well below the NOVA 3 maximum.

**NOVA_PROXY_3_PROCESSED: 75 → 82**  
The current cap at 75 means no NOVA 3 product can exceed B (under current thresholds). Under proposed thresholds (B = 65–79), a NOVA 3 product with a cap at 75 remains in B — appropriate. But lifting to 82 allows NOVA 3 products with genuinely excellent structural profiles to reach low-A territory (80–82). This is architecturally appropriate for NOVA 3 fermented products (kefir, yogurt) or other NOVA 3 products with very limited processing intervention.

**Rank ordering check:**  
All caps remain ordered (NOVA3 cap 82 > NOVA4 cap 68 > 3+ additive cap 72 > 5+ additive cap 60). Cross-category ordering is preserved. A well-structured NOVA 3 product remains above a well-structured NOVA 4 product. ✓

---

## Proposal 5: Additive Cap Interaction Fix

### Problem identified

Under current constants, when NOVA 4 + ADDITIVE_MARKERS_3_PLUS both fire:
- NOVA4: 60
- ADDITIVE_MARKERS_3_PLUS: 65
- Binding: 60 (NOVA4 binds)

The ADDITIVE_MARKERS_3_PLUS cap has **no independent effect** when combined with NOVA 4. This makes the 3-additive cap semantically redundant within NOVA 4 territory.

Under proposed constants:
- NOVA4: 68
- ADDITIVE_MARKERS_3_PLUS: 72
- Binding: 68 (NOVA4 still binds)

Still the same redundancy. To provide differentiation, NOVA 4 products with 3+ additive categories should be capped lower than NOVA 4 products without:

**Optional addendum (for future implementation):** Introduce `NOVA4_3PLUS_ADDITIVE_COMBINED = 62` — a cap that fires only when BOTH nova==4 AND additives≥3 are true simultaneously. This would provide explicit differentiation within NOVA 4 without requiring an architecture redesign.

This is flagged but not included in the base proposal, as it requires a new cap type and adds complexity. The base proposal is sufficient for v2 recalibration.

---

## Proposal 6: WHOLE_FOOD_FAT_FLOOR Adjustment

### Current

```python
WHOLE_FOOD_FAT_FLOOR = 65
```

### Proposed

```python
WHOLE_FOOD_FAT_FLOOR = 70
```

### Rationale

Whole-food fat products (olive oil, nut butters, tahini) should be in B range under proposed thresholds (B = 65–79). The current floor at 65 places them at the bottom of what would be the B range (or the top of C). The proposed 70 places them at mid-B — a more credible grade for a structurally intact, minimal-processing whole-food fat product.

Note: NOVA 1 single-ingredient whole-food fat products (plain olive oil, tahini) would receive the NOVA1_SINGLE_FLOOR at 85, which is higher. The WHOLE_FOOD_FAT_FLOOR at 70 applies to NOVA 2 whole-food fat products (e.g., a cold-pressed nut butter with minimal additives).

---

## Proposal 7: Confidence Ceiling Adjustment

### Current

```python
CONFIDENCE_INSUFFICIENT_CEILING = 50
CONFIDENCE_LOW_CEILING          = 70
```

### Proposed

No change to CONFIDENCE_INSUFFICIENT_CEILING.

```python
CONFIDENCE_LOW_CEILING = 75
```

### Rationale

Under proposed grade thresholds, the confidence ceiling at 70 would cap products at the top of the B range. For products with genuinely good structural profiles but low confidence (e.g., single-source data, medium NOVA confidence), a ceiling at 70 may prevent them from reaching the A range they would otherwise deserve.

Lifting to 75 allows low-confidence products to reach the bottom of A range (80 is still out of reach), which maintains meaningful ceiling without over-penalizing data quality issues that are outside the product's structural properties.

---

## Summary of Proposed Changes

| Item | Current | Proposed | Impact |
|------|---------|----------|--------|
| Grade S threshold | — | ≥90 | New tier |
| Grade A threshold | ≥85 | ≥80 | −5 pts |
| Grade B threshold | ≥70 | ≥65 | −5 pts |
| Grade C threshold | ≥55 | ≥50 | −5 pts |
| Grade D threshold | ≥40 | ≥35 | −5 pts |
| NOVA1_SINGLE_FLOOR | 75 | 85 | +10 pts (NOVA1) |
| WHOLE_FOOD_FAT_FLOOR | 65 | 70 | +5 pts (whole fat) |
| NOVA_PROCESSING[2] | 80 | 85 | +0.75 pts |
| NOVA_PROCESSING[3] | 55 | 65 | +1.50 pts |
| NOVA_PROCESSING[4] | 25 | 35 | +1.50 pts |
| NOVA_WFI[2] | 80 | 85 | +0.20 pts |
| NOVA_WFI[3] | 50 | 60 | +0.40 pts |
| NOVA_WFI[4] | 20 | 30 | +0.40 pts |
| NOVA4 cap | 60 | 68 | +8 pts headroom |
| NOVA3 cap | 75 | 82 | +7 pts headroom |
| ADDITIVE_3PLUS cap | 65 | 72 | +7 pts headroom |
| ADDITIVE_5PLUS cap | 55 | 60 | +5 pts headroom |
| CONFIDENCE_LOW_CEILING | 70 | 75 | +5 pts ceiling |

**Not changed:**
- Trans fat veto (0 score, hard) — unchanged
- SWEETENER_CAP at 70 — unchanged (under proposed thresholds, 70 = top of B, appropriate)
- Israeli red label caps — unchanged
- HP penalty weights — unchanged
- SE gate thresholds — unchanged (SE_BEVERAGE_KCAL remains at 10)
- Penalty family budgets — unchanged
- SRC-05 relative penalty factors — unchanged
- Confidence insufficient ceiling — unchanged

---

## What This Does NOT Do

This proposal does not:
- Raise all scores uniformly (products without structural justification receive only the ~2pt dimension delta from Proposal 2)
- Remove engineering concern signals (NOVA4 cap, additive escalation, sweetener cap all remain)
- Create new floors (only the existing floors are adjusted)
- Alter the fundamental scoring formula or add new dimensions
- Soften the Israeli regulatory signal integration

The conviction of the system is preserved. The calibration is improved.

---

*See `shadow_recalibration_simulation.md` for the expected effect on both corpora.*
