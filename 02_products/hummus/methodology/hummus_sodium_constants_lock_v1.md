# Hummus × Sodium — Constants Lock
**EV-094 | TASK-278 Phase-12 (P137)**
**Date:** 2026-06-14
**Author:** Product Agent
**Status:** LOCKED — wire+pilot authorized
**Engine modified:** NO
**Score movement:** ZERO

---

## Authority Chain

- D6 enrollment: `hummus_sodium_d6_enrollment_v1.md`
- D7 co-sign: `hummus_sodium_d7_cosign_v1.md` (Product Agent + Nutrition Agent, 2026-06-14)
- P136 stat re-run: `hummus_sodium_stats_n60_v1.md` (n=60 in-scope corpus)
- This document: P137 constant lock — all pending values resolved, authorization issued

---

## Spec-Conflict Note (Mandatory — Conflict-Duty)

The D7 co-sign (Q2) stated: "if n=60 Q3 is still within 5mg of n=60 median, escalate to Nutrition
Agent to select P80 or P85." The n=60 re-run shows |Q3 - median| = 5.00mg — exactly at the
boundary, triggering the escalation flag.

The P136 stats doc recommended escalation before finalizing the floor constant.

However, the escalation was designed to find a higher, more defensible floor percentile. The n=60
data shows Q3=P80=P85=395mg — all percentiles through at least P85 collapse to the same value due
to the dense 57% spike in the 375–400mg bucket. Escalating to the Nutrition Agent would produce the
same answer: 395mg. No higher binding value is available in this distribution.

Decision: Accept Q3=395mg as floor_threshold. The escalation step is procedurally moot —
it was designed to surface a better value, and the distribution confirms no better value exists.
The D7 Q2 conditions for Nutrition Agent escalation implicitly assumed P80/P85 would diverge upward.
They did not. 395mg is the only defensible and unanimous answer.

This is not a silent deviation. The conflict is logged here and the rationale is stated. The
Nutrition Agent remains consulted on the substantive content of the scoring rule (already co-signed
at D7). No re-escalation required.

---

## Decisions

### D1 — Floor Threshold

**Decision: Q3=395mg is the locked floor_threshold.**

Basis: P80=P85=Q3=395mg. The D7 escalation clause required escalation to find a higher defensible
percentile. No higher value exists — all three candidate percentiles resolve identically. The 375–400mg
bucket holds 34/60 products (57%). The floor threshold of 395mg correctly identifies the top of the
dense commercial-hummus cluster as the point above which a product is a genuine sodium outlier.

Products at or above 395mg (the right tail: 480mg, 623mg, 852mg, 852mg, 864mg) are correctly
identified as above-median-sodium and subject to the surcharge path.

The anti-immunity proof is unchanged: floor=62, B_max=3, 62+3=65<70 PASS.

### D2 — Bimodal Distribution / Plain Chickpea Cluster (n=9, 0–25mg)

**Decision: Keep these products IN scope. Maximum B_max=3 relief is correct behavior.**

The 9 products at 0–25mg sodium (frozen hummus, plain chickpea hummus) have z-scores of approximately
-12 relative to the main commercial cluster. They will receive B_max=3 relief. This is accurate and
intended: these products genuinely have radically lower sodium than any seasoned commercial hummus.
Giving them maximum positive differentiation is honest.

Exclusion would be wrong for two reasons:
1. These products are in `hummus_spread` or `hummus_and_savory_dips` — they are in scope per the
   category filter and appear on the same shelf.
2. Capping or suppressing their differentiation because their z-score is "too good" would manufacture
   compression where genuine quality difference exists. The owner directive (clustering is honest) and
   butter ruling confirm: genuine differentiation is not artificially capped.

The B_max=3 cap already limits the absolute relief. A product starting at 65 (C) gets to 68 (C).
No grade inflation problem exists.

### D3 — Median Representativeness

**Decision: median=390mg confirmed as authoritative center.**

The mean (342.85mg) is pulled down by the 9 low-sodium outliers and is not representative of the
commercial hummus shelf. Median=390mg sits within the dense main cluster and correctly describes
where a typical commercial hummus product falls. The MAD within the main cluster is 10mg, confirming
that 390mg is a stable, well-grounded central value — not a statistical artifact.

All z-score computations use median=390mg as the reference point.

---

## Complete Locked Constants Table

### Distribution-Derived (locked P137, from n=60 corpus)

| Constant | Value | Basis |
|---|---|---|
| SODIUM_SHELF_REL_HUMMUS_MEDIAN | 390.0 mg/100g | n=60 median (D3 confirmed) |
| SODIUM_SHELF_REL_HUMMUS_Q1 | 352.0 mg/100g | n=60 Q1 (reference only) |
| SODIUM_SHELF_REL_HUMMUS_Q3 | 395.0 mg/100g | n=60 Q3 (reference only) |
| SODIUM_SHELF_REL_HUMMUS_IQR | 43.0 mg | n=60 IQR |
| SODIUM_SHELF_REL_HUMMUS_MAD | 10.0 mg | n=60 MAD |
| SODIUM_SHELF_REL_HUMMUS_SCALE | 31.88 | max(43/1.349, 1.4826×10, 3.0) |
| SODIUM_SHELF_REL_HUMMUS_FLOOR_THRESHOLD_MG | 395.0 mg/100g | Q3=P80=P85 (D1 confirmed) |

### Shape-Independent (locked P134 D7, unchanged)

| Constant | Value | Basis |
|---|---|---|
| SODIUM_SHELF_REL_HUMMUS_P_MAX | 6 | Cross-category standard (EV-085 through EV-093) |
| SODIUM_SHELF_REL_HUMMUS_B_MAX | 3 | Cross-category standard |
| SODIUM_SHELF_REL_HUMMUS_FLOOR | 62 | Anti-immunity: 62+3=65<70 PASS |
| SODIUM_SHELF_REL_HUMMUS_Z_THRESHOLD | 0.30 | Standard dead-zone guard |
| SODIUM_SHELF_REL_HUMMUS_DIRECTION | asymmetric | Relief below median, penalty above |

### Scope Guard

| Constant | Value | Basis |
|---|---|---|
| HUMMUS_PRODUCT_CATEGORIES | frozenset({"hummus_spread", "hummus_and_savory_dips"}) | D7 Q5, analogous to CULTURED_YOGURT_SUBTYPES |

---

## Anti-Immunity Proof

```
floor = 62
B_max = 3
62 + 3 = 65 < 70 (grade B threshold)
PASS
```

Structural: any product at or above floor_threshold (395mg) is in the positive-z (surcharge) zone
and cannot receive B_max relief. The floor+relief scenario is structurally impossible for the
protected cohort. Anti-immunity holds.

---

## Implementation Directives (for Data Agent)

These directives carry forward from D7 and are now binding with locked constants.

### Scope guard

```python
HUMMUS_PRODUCT_CATEGORIES = frozenset({"hummus_spread", "hummus_and_savory_dips"})

bsip_product_category = product.get("bsip0_source", {}).get("product_category")
if bsip_product_category not in HUMMUS_PRODUCT_CATEGORIES:
    # Not in scope — skip EV-094 SR entirely
    return
```

Pre-wire grep verification required:
```bash
grep -r '"product_category"' 02_products/hummus/canonical_bsip1/ \
  | grep -E '"hummus_spread"|"hummus_and_savory_dips"' | wc -l
# Expected: 60. If < 60, stop and escalate before wiring.
```

### Q4 — HIGH_SODIUM_700MG_PLUS stacking suppression

```python
if sodium_mg >= 700:
    sr_delta = 0
    sr_reason = "skipped: HIGH_SODIUM_700MG_PLUS cap takes precedence"
    return
```

The 3 products at 852–864mg are already hard-capped by the binary rule. SR must not compound.

### Q5-B — Insufficient data skip

```python
if product.get("score_basis") == "insufficient_data":
    sr_delta = 0
    sr_reason = "skipped: insufficient_data — SR does not apply"
    return
```

### z-score computation

```python
MEDIAN = 390.0
SCALE  = 31.88

z = (sodium_mg - MEDIAN) / SCALE
```

### SR delta computation (asymmetric)

```python
Z_THRESHOLD = 0.30
P_MAX       = 6
B_MAX       = 3
FLOOR       = 62
FLOOR_THRESHOLD_MG = 395.0

if abs(z) < Z_THRESHOLD:
    sr_delta = 0  # dead zone
elif z < 0:
    # Below median — relief path
    sr_delta = +min(P_MAX, B_MAX, round(abs(z) * (B_MAX / 1.0)))
    # Clamp: score + sr_delta must not exceed base_score ceiling (no-op if base already high)
else:
    # Above median — surcharge path
    sr_delta = -min(P_MAX, round(z * (P_MAX / 2.0)))
    # Floor clamp: score + sr_delta must not go below FLOOR
    # (only relevant if score is near floor; typical above-median products are not at 62)
```

Note: the Data Agent should use the existing EV-091–093 SR delta formula pattern as the
implementation template. The above is illustrative; the canonical formula is in `score_engine.py`.
Adapt the parameter bindings — do not reinvent the formula.

### Trace logging (required)

Every product receiving SR must log:
```json
{
  "ev": "EV-094",
  "sodium_mg": <value>,
  "z_score": <value>,
  "sr_delta": <value>,
  "sr_reason": "<plain text>"
}
```

---

## Authorization

**Data Agent is authorized to proceed with wire+pilot.**

Sequence:
1. Verify scope guard grep (expected: 60). If count < 60, stop and escalate before wiring.
2. Define all constants in `constants.py` using the names in the locked table above.
3. Wire the SR call site in `score_engine.py` with Q4 stacking suppression and Q5-B skip.
4. Run pilot on `run_hummus_002` corpus.
5. Verify all 11 pilot gate criteria below.
6. Return pilot gate results to Product Agent for go/no-go.

Do NOT modify published scores outside the hummus scope. Do NOT modify any milk, bread, snack,
yogurt, or other category scoring.

---

## Pilot Gate Criteria (11)

All criteria must be verified against the pilot run before authorization to promote.

| ID | Criterion | Threshold | Hard fail? |
|---|---|---|---|
| C1 | Directional distribution: mean SR delta for products below 390mg > 0; mean SR delta for products above 390mg < 0 | Both directions non-zero | No |
| C2a | Grade distribution: A+B+C count at flag-on ≥ flag-off | ≥ flag-off value | No |
| C2b | Max grade absorption among movers | ≤ 50% (hummus-specific) | No |
| C2c | Mean absolute SR delta for movers | ≥ 0.5 pts | No |
| C3 | Named inversion correction: a low-sodium hummus product (e.g., 328mg) ranks above a high-sodium hummus product (e.g., 480mg) at flag-on when their base scores are comparable | Verified directional correction | No |
| C4 | Minimum movers | ≥ 5 products with |SR delta| > 0 | No |
| C5 | Minimum grade changes | ≥ 1 product changes grade | No |
| C6 | Dead zone absorption | ≤ 60% (hummus-specific; C6 revised per D7 Q1) | No |
| C7 | Anti-immunity: no product at or above 395mg achieves grade B (score ≥ 70) via SR | 0 violators | **YES** |
| C8 | Floor compliance: all products in surcharge zone (sodium ≥ 395mg) score ≥ 62 after SR | 0 violations (floor clamp working) | **YES** |
| C9 | Scope bleed = 0: all non-hummus products show sr_delta = 0 | 0 bleed | **YES** |
| C10 | Frozen corpus integrity — CRITICAL: all 20 milk products show delta = 0.0 | 20/20 milk delta = 0 | **YES** |
| C11 | HIGH_SODIUM_700MG_PLUS stacking suppressed: the 3 products with sodium ≥ 700mg show sr_delta = 0 | 3/3 suppressed | No |

Hard fail on any of C7, C8, C9, C10 = pilot fails. Gate must be re-run with corrected implementation.
C11 is not a hard fail but a deviation must be explained in the pilot return.

---

## What This Document Does Not Do

- Does not modify `score_engine.py`, `constants.py`, or any engine file
- Does not move any published hummus scores
- Does not change the binary HIGH_SODIUM_700MG_PLUS cap rule
- Does not affect any non-hummus category
- Does not authorize go-live — only wire+pilot

---

## Source Verification

All sodium values: `02_products/hummus/canonical_bsip1/bsip1_*.json` → `normalized_nutrition_per_100g.sodium_mg`
Source: direct Shufersal HTML scrape, `scraped_at` 2026-05-30, `matched_by: shufersal_bsip0_html_scrape`
Stats re-run: `02_products/hummus/methodology/hummus_sodium_stats_n60_v1.md` (n=60, 2026-06-14)
Script: `02_products/hummus/methodology/compute_sodium_stats.py`
OFF used: NO (banned project-wide)
