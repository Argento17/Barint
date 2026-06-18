# Hummus × Sodium — D7 Co-Sign (Product Agent)
**EV-094 | TASK-278 Phase-12**
**Date:** 2026-06-14
**Author:** Product Agent
**Status:** CO-SIGNED — BLOCKED pending n=60 stat re-run before constants finalize
**Engine modified:** NO
**Score movement:** ZERO

---

## Decision Summary

ENROLL hummus × sodium as a shelf-relative differentiator. Five open questions resolved below.
One hard blocker: n=60 stat re-run required before the Data Agent wires constants into the engine.
EV-094 registered in evidence registry with PENDING constants.

---

## Q1 — Dead Zone Absorption (~50–58%)

**Decision: ENROLL. C6 threshold revised to ≤60% hummus-specific.**

The tight IQR (35mg on n=69) reflects genuine category physiology: commercial hummus is formulated around a narrow sodium target (~360–400mg). The ~40-product homogeneous core receiving delta=0 is correct — their sodium uniformity is a distributional fact, not a scoring failure. The SR mechanism should not manufacture differentiation where none exists; the owner directive confirms this.

The differentiation that matters is at the extremes:
- 17 products below 360mg (genuinely low-sodium, many scoring A) earn relief
- Products above Q3 (high-sodium outliers) earn penalty
- INV-A and INV-B are both resolvable and constitute the primary consumer harm

Precedent: maadanim C6 revised to 55% (P132, Phase-10) on a similarly bottom-heavy distribution. Hummus dead zone is estimated 50–58% on n=69 stats, which may shift on n=60. C6 threshold of ≤60% is conservative and hummus-specific — it does not propagate to other categories.

**Reversal condition:** If n=60 re-run shows dead_zone >60%, re-examine whether the in-scope corpus has sufficient non-dead-zone products to justify enrollment. At that point escalate to Nutrition Agent.

---

## Q2 — Floor Threshold (Q3 = 395mg)

**Decision: PENDING n=60 re-run. n=69 Q3=395mg is NOT binding.**

On the n=69 corpus, Q3=395mg sits only 3mg above median=392mg. A floor threshold that is 3mg above the median would cap 25% of the shelf based on a margin smaller than typical measurement precision in a sodium scrape. This is not a defensible implementation constant.

Two scenarios after the n=60 re-run:

| Scenario | Outcome |
|---|---|
| n=60 Q3 is meaningfully higher than n=69 Q3 (e.g., ≥410mg) | Use n=60 Q3 as floor_threshold |
| n=60 Q3 is still within 5mg of n=60 median | Escalate to Nutrition Agent to select a higher percentile (80th or 85th) for floor_threshold |

The anti-immunity proof is structurally independent of the exact floor_threshold value: floor=62, B_max=3 → 65 < 70 PASS regardless of whether floor_threshold lands at 395mg or 430mg.

---

## Q3 — Stat Re-Run on n=60

**Decision: REQUIRED. Hard blocker on constants finalization.**

The D6 doc computes all statistics on n=69 (60 in-scope + 9 out-of-scope). The 9 out-of-scope products (eggplant spread: 4, matbucha: 5) have different sodium physiology from hummus — eggplant spread typically runs 250–450mg, matbucha 400–700mg. Including them compresses the IQR and distorts Q1/Q3 by mixing products that will not be scored by this rule.

Phase-5 cereals precedent applies: when corpus scope narrowed from n=45 to n=34 cereal-only, stats were recomputed before implementation constants were locked.

**Data Agent dispatch (from this return):** Compute sodium distribution stats on the 60 in-scope BSIP1 files only (`bsip0_source.product_category in ("hummus_spread", "hummus_and_savory_dips")`). Deliver: n, min, max, Q1, median, Q3, IQR, MAD, robust_scale. Return to Product Agent for constant lock before engine wiring begins.

Until n=60 stats are confirmed, the following constants are PENDING:

| Constant | n=69 proxy | Binding value |
|---|---|---|
| median_mg | 392.0 | PENDING |
| q1_mg | 360.0 | PENDING |
| q3_mg | 395.0 | PENDING |
| iqr | 35.0 | PENDING |
| mad | 12.0 | PENDING |
| robust_scale | 25.945 | PENDING |
| floor_threshold_mg | 395.0 | PENDING (see Q2) |

The following constants are locked now (distribution-shape independent):

| Constant | Value | Basis |
|---|---|---|
| P_max | 6 | Cross-category standard (EV-085 through EV-093) |
| B_max | 3 | Cross-category standard |
| floor | 62 | Anti-immunity: 62+3=65<70 PASS |
| z_threshold | 0.30 | Standard dead-zone guard |
| direction | asymmetric | Low-sodium relief + high-sodium penalty |

---

## Q4 — HIGH_SODIUM_700MG_PLUS Stacking

**Decision: SUPPRESS SR penalty when HIGH_SODIUM_700MG_PLUS binary cap fires.**

Three products (bsip1_7296073451969 at 852mg and two others at 852–864mg) already trigger the `HIGH_SODIUM_700MG_PLUS` binary cap, which sets a hard ceiling of 60 or lower. Applying an additional SR penalty of -P_max=-6 on top of a score that is already capped:
- Produces no consumer-visible grade change (these products are already D)
- Creates redundant signal noise in the trace
- Contradicts the design principle that SR expresses within-shelf variation, not harm magnitude

The binary cap is the correct instrument for extreme sodium. SR is the correct instrument for relative quality positioning within the shelf. These are complementary, not compounding.

**Implementation directive for Data Agent:**
```python
# Before applying EV-094 SR:
if sodium_mg >= 700:
    # HIGH_SODIUM_700MG_PLUS already fired — skip SR
    sr_delta = 0
    sr_reason = "skipped: HIGH_SODIUM_700MG_PLUS cap takes precedence"
else:
    # Apply EV-094 shelf-relative SR normally
    ...
```

---

## Q5 — Scope Guard Field Accessor

**Decision: ACCEPT nested accessor. Require Data Agent grep-verify before wiring.**

The D6-proposed accessor is:
```python
bsip_product_category = product.get("bsip0_source", {}).get("product_category")
if bsip_product_category in ("hummus_spread", "hummus_and_savory_dips"):
    # apply EV-094 SR
```

This is confirmed present in all 69 BSIP1 files per D6's own survey. However, it is a nested dict accessor — different from the flat BSIP1 fields used in EV-091/092/093 (`category`, `bsip_maadanim_subtype`, `juice_sub_pool`). Before wiring, the Data Agent must verify:

```bash
# Verify nested key is populated in all in-scope BSIP1 files:
grep -r '"product_category"' 02_products/hummus/canonical_bsip1/ | grep -E '"hummus_spread"|"hummus_and_savory_dips"' | wc -l
# Expected: 60
```

If count < 60, the scope guard is not reliable and a different field must be identified.

**Constant naming:** Define `HUMMUS_PRODUCT_CATEGORIES = frozenset({"hummus_spread", "hummus_and_savory_dips"})` in `constants.py`. Analogous to `CULTURED_YOGURT_SUBTYPES` and `CREAM_CHEESE_SPREAD_SUBTYPES`. A named constant makes scope explicit, testable, and greppable.

---

## Q5-B (from D6 Section 7.5) — Insufficient Data Products

The D6 doc raises the question of two products (bsip1_7296073733317 at 23mg, bsip1_7296073733348 at 64mg) that received `score=50/insufficient_data`. Nutrition Agent recommends skipping SR for these.

**Decision: SKIP SR for insufficient_data products.**

Applying SR to a data-floor score (50) produces a misleading result (e.g., 50+3=53/C) that implies nutritional evaluation when the engine explicitly flagged insufficient data. The insufficient_data designation must remain unmodified by any SR layer.

**Implementation directive:** Check `product.get("score_basis") != "insufficient_data"` before applying SR. If insufficient_data, skip and log `sr_delta=0, sr_reason="skipped: insufficient_data"`.

---

## Anti-Immunity Proof

floor = 62, B_max = 3
62 + 3 = 65 < 70 (grade B threshold)
**PASS**

Structural: any product at or above floor_threshold (pending n=60 value) is in the surcharge zone (positive z-score) and cannot receive B_max relief. The floor+relief scenario is structurally impossible for the protected cohort — anti-immunity holds regardless of the exact floor_threshold.

---

## Pilot Gate Criteria (11)

| ID | Criterion | Threshold | Hard fail? |
|---|---|---|---|
| C1 | Directional distribution: mean SR delta for below-median products > 0; mean SR delta for above-median products < 0 | Both directions non-zero | No |
| C2a | Grade distribution: A+B+C count at flag-on ≥ flag-off | ≥ flag-off value | No |
| C2b | Max grade absorption among movers | ≤ 50% (relaxed; hummus-specific) | No |
| C2c | Mean absolute SR delta for movers | ≥ 1.5 pts | No |
| C3 | Gap narrows / directional correction: INV-A gap_after > gap_before (correct direction); INV-B score(328mg product) closer to score(480mg product) at flag-on | Both INV verified | No |
| C4 | Minimum movers | ≥ 5 products with |SR delta| > 0 | No |
| C5 | Minimum grade changes | ≥ 1 product changes grade | No |
| C6 | Dead zone absorption | ≤ 60% hummus-specific (revised from standard 40%) | No |
| C7 | Anti-immunity: no product at/above floor_threshold achieves grade B | 0 violators | **YES** |
| C8 | Floor compliance: no product scores > floor when flagged for surcharge | 0 violations | **YES** |
| C9 | No scope bleed: non-hummus products show 0 SR delta | 0 bleed | **YES** |
| C10 | Frozen: milk CRITICAL — all 10 milk products show delta=0 | 20/20 milk delta=0 | **YES** |
| C11 | HIGH_SODIUM_700MG_PLUS stacking suppressed: products ≥700mg show sr_delta=0 | 3/3 suppressed | No |

Hard fail on any of C7, C8, C9, C10 = pilot fails. Gate must be re-run after n=60 stat re-run confirms final constants.

---

## What This D7 Does Not Do

- Does not modify `score_engine.py`, `constants.py`, or any engine file
- Does not move any published scores
- Does not finalize implementation constants (blocked on n=60 re-run)
- Does not change the binary HIGH_SODIUM_700MG_PLUS cap rule
- Does not affect non-hummus categories

---

## Next Steps (sequenced)

1. **Data Agent:** Re-run sodium stats on n=60 in-scope hummus products. Deliver stats to Product Agent.
2. **Product Agent:** Receive n=60 stats, lock final constants (median, Q3 as floor_threshold or custom percentile per Q2 decision), update EV-094 with binding values.
3. **Data Agent:** Verify scope guard grep (Q5), define `HUMMUS_PRODUCT_CATEGORIES` constant, implement SR call site with Q4 stacking suppression and Q5-B insufficient_data skip.
4. **Data Agent:** Run pilot on `run_hummus_002` corpus against 11-criteria gate.
5. **Product Agent:** Review pilot gate result, approve or revise.

---

## Source Verification

All sodium values: `02_products/hummus/canonical_bsip1/bsip1_*.json` → `normalized_nutrition_per_100g.sodium_mg`
Source: direct Shufersal HTML scrape, `scraped_at` 2026-05-30, `matched_by: shufersal_bsip0_html_scrape`
BSIP2 scores: `02_products/hummus/intelligence_bsip2/run_hummus_002/products/bsip1_*/bsip2_trace.json`, marked AUTHORITATIVE
OFF not consulted (banned project-wide)
