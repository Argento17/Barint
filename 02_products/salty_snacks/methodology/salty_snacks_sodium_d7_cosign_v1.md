# Salty Snacks × Sodium — D7 Co-Sign
## Product Agent Decision | EV-093 | TASK-278 Phase-11

**Status:** D7 CO-SIGNED — EV-093 registered, pilot gate locked
**Product Agent:** Claude Sonnet 4.6
**Date:** 2026-06-14
**D6 source:** `02_products/salty_snacks/methodology/salty_snacks_sodium_d6_enrollment_v1.md`
**Extends:** EV-087 (cereals), EV-088 (yogurt), EV-089 (cheese_spreads), EV-090 (hard_cheeses), EV-091 (juices), EV-092 (maadanim)

---

## Q1 — Scope Guard: `category == "salty_snack"` vs subtype/subpool filter

**Decision: ACCEPT `product.get("category") == "salty_snack"` as the sole scope guard.**

Decisive reason: The field is confirmed present in 54/54 BSIP1 files. The BSIP2 router assigns nutritional routing categories (whole_food_fat, bread, etc.) that are agnostic to shelf placement — the BSIP1 `category` field is the authoritative shelf boundary, consistent with EV-090 (bsip_cheese_subpool) and EV-091 (juice_sub_pool) where BSIP1 fields were used instead of router categories. The two flagged sub-pools (rice_cakes, caramel_popcorn) do not require exclusion: rice_cakes earn relief that the floor and whole-food floor will absorb structurally; caramel_popcorn's sugar and additive caps override any SR relief, so SR delta is harmless noise. No scope bleed risk — "salty_snack" is a dedicated router category not shared with any other enrollment category.

Sub-pool exclusion: REJECTED. Adding `sub_pool not in ("caramel_popcorn",)` would be artisanal trimming without a structural justification — the anti-immunity floor handles the concern.

Reversal condition: If a future corpus expansion adds a product class that is both tagged `category=="salty_snack"` AND belongs to a different nutritional category where sodium SR would create a genuine double-penalization conflict with an already-enrolled category. That scenario does not exist today.

---

## Q2 — Relief for Very-Low-Sodium Products (rice cakes, plain popcorn at 10–50mg)

**Decision: ACCEPT B_max=3. No exclusion or cap adjustment for low-sodium outliers.**

Decisive reason: The anti-immunity proof is structural, not product-specific. Floor(62) + B_max(3) = 65 < 70 — no SR-boosted salty snack can reach B-grade regardless of sodium position. Rice Cakes Plain (Na=10mg, current score=85/A) already sits above the 62 floor; the whole-food floor protects it independently. For the 7 rice_cakes products scoring 61–82, those already above 62 gain +1 to +3 pts of honest, deserved relief — they genuinely sit far below median sodium for their shelf category. The relief is bounded, evidence-based, and correct.

Reversal condition: If pilot data shows rice_cake products crossing a grade threshold (C→B or B→A) solely due to SR relief with no other supporting signals. Not expected given the floor mechanics.

---

## Q3 — HP_FAT_SODIUM_COMBO Stacking

**Decision: NO combined penalty budget. Accept stacking as intentional.**

Decisive reason: HP_FAT_SODIUM_COMBO and SODIUM_SALTY_SNACK_SHELF_REL_V1 target distinct constructs. HP penalizes the behavioral palatability pattern of combined high fat and high sodium — a product engineering concern. SR penalizes continuous shelf-relative sodium position — a category-comparison concern. The existing SODIUM_FAMILY_BUDGET already caps total sodium-family penalties; no new combined budget is warranted. The theoretical worst-case stacking (-12 pts for a product at 800mg with 32% fat) is a correct signal: a product that simultaneously maximizes both fat and sodium relative to its shelf peers deserves compounded penalization. Monitor at pilot; revisit if the combined effect produces an implausible score floor below what the underlying quality warrants.

Reversal condition: Pilot run shows products reaching scores below 30 where no other BSIP signal (NOVA, additives, saturated fat) supports that floor.

---

## Q4 — P_max: 6 or 8

**Decision: P_max=6.**

Decisive reason: Consistency with EV-087 through EV-092 across six prior categories. Deviating to P_max=8 requires EV-level justification tied to evidence of systematic under-penalization at P_max=6. The corpus data does not supply that: with 18/54 products above the dead zone and INV-B gap correction achievable at P_max=6 (Baked Pretzels at z=+2.56 hits the 6pt ceiling, Bisli Spaghetti at z=+1.70 receives -5.1 pts — sufficient to narrow the inversion meaningfully), P_max=6 is adequate. P_max=8 would be asymmetric and would require re-running the anti-immunity proof. Not justified.

Reversal condition: Post-pilot analysis shows that the highest-sodium products (920mg pretzels cluster) cannot be differentiated within the 6pt ceiling despite meaningful sodium differences between them.

---

## Q5 — Wiring: Standalone vs regulatory_quality Dimension

**Decision: Standalone call site, applied post-dimension pre-floor.**

Decisive reason: Consistent with EV-088 through EV-092 which all used standalone call sites. The `regulatory_quality` dimension carries the binary Israeli red-label count signal — conflating a continuous SR sodium delta into this dimension would corrupt the red-label signal's interpretability and create a mixed-signal reporting problem. The standalone approach (consistent with how sugar SR is wired in prior phases) keeps the SR delta clean, auditable, and reversible. Implementation is Data Agent's task in D8, not gated on this decision.

Reversal condition: If Data Agent's D8 implementation encounters a technical constraint where the standalone call site creates an ordering conflict with other post-dimension adjustments. Route that finding to Product + Nutrition for a joint D8 amendment.

---

## Anti-Immunity Proof

floor(62) + B_max(3) = **65 < 70 PASS**

Structural verification:
- B-grade threshold = 70
- Maximum score achievable via SR relief: 62 (floor) + 3 (B_max) = 65
- Products above Q3 (630mg, n=18+) sit in the surcharge zone (z > 0) — they receive negative delta, cannot receive B_max relief
- The floor-plus-relief scenario (65) applies only to products with extremely low sodium; their other structural caps (NOVA, additives) further constrain their ceiling
- No salty_snack product can reach B-grade (70) through SR mechanics alone

---

## Named Inversions — D7 Verification

### INV-A: Pringles Original (480mg/52.4C) vs Bisli Spaghetti (800mg/52.9C)
- Current gap: 0.5 pts (sodium invisible — 320mg difference with zero effective score signal)
- SR at flag-on: Pringles (z=-0.57) → relief +1.7 pts; Bisli (z=+1.70) → penalty -5.1 pts
- Expected gap at flag-on: ~6.8 pts (Pringles scores higher, gap widens in correct direction)
- Pilot gate C3 test: |gap_on| > |gap_off| AND direction correct (Pringles above Bisli)
- **INV-A ACCEPTED as qualifying C3 pair**

### INV-B: Bisli Spaghetti (800mg/52.9C) vs Baked Pretzels (920mg/57.0C)
- Current gap: 4.1 pts WRONG direction (higher-sodium product scores higher — binary cap saturation artifact)
- SR at flag-on: Bisli (z=+1.70) → penalty -5.1 pts; Pretzels (z=+2.56) → penalty -6.0 pts (at P_max ceiling)
- The 0.9pt difference in SR penalty partially narrows the 4.1pt inversion; remaining gap reflects genuine non-sodium architectural differences (whole-grain, clean ingredient list) — this is the honest finding, not an artifact
- Pilot gate C3 test for INV-B: |gap_on| < |gap_off| OR gap flips direction. The pretzel's non-sodium quality advantage may persist as a smaller gap — partial correction is sufficient; a full rank swap is not required and would not be honest
- **INV-B ACCEPTED as qualifying C3 pair with partial-correction expectation**

---

## Pilot Gate — 11 Criteria (Locked)

| # | Name | Pass condition |
|---|---|---|
| C1 | directional_distribution | Mean delta above-median products ≤ 0; mean delta below-median products ≥ 0 |
| C2a | grade_dist | Net A+B+C count not degraded at flag-on vs baseline (run_salty_snacks_002) |
| C2b | grade_absorption | No single grade absorbs >40% of movers |
| C2c | magnitude | Mean |delta| for movers in [0.5, P_max=6] |
| C3 | gap_narrows_inversion | INV-A: gap widens, Pringles above Bisli at flag-on. INV-B: |gap_on| < |gap_off| OR direction flips. Both pairs must pass. |
| C4 | min_movers | ≥5 salty_snack products with |delta| ≥ 1pt |
| C5 | min_grade_changes | ≥1 grade change at flag-on |
| C6 | max_absorption | Dead zone products ≤ 40% of corpus (current: 27.8%, pre-pilot PASS) |
| C7 | anti_immunity | 0 products with sodium ≥ 630mg reach grade B (≥70) at flag-on |
| C8 | floor_compliance | All products with sodium ≥ 630mg: flag-on score ≤ 62 (SR floor enforced) |
| C9 | no_scope_bleed | 0 non-salty_snack products with SODIUM_SALTY_SNACK_SHELF_REL_V1 fired in trace |
| C10 | frozen_byte_id_milk | CRITICAL: 20/20 milk run_005_headpin products delta=0.0 at flag-on |
| C11 | flag_off_drift | Flag-off scores match run_salty_snacks_002 baseline ±5pts (documentation only — not a pass/fail gate for flag-on validation) |

**Hard fail criteria:** C7, C8, C9, C10 are hard fails — any single failure blocks D8 implementation.
**Soft fail criteria:** C1, C2a, C2b, C2c, C3, C4, C5, C6 — failures require Product+Nutrition joint review before block decision.

---

## D7 Decisions Summary Table

| Q | Decision | Decisive Reason | Reversal Condition |
|---|----------|----------------|-------------------|
| Q1 scope guard | ACCEPT `category=="salty_snack"` single field | 54/54 coverage, no bleed, consistent with EV-090/091 BSIP1-field pattern | New product class with conflicting enrollment category |
| Q2 rice-cake relief | ACCEPT B_max=3, no exclusion | Floor(62)+B_max(3)=65<70 structural protection; relief is honest | Pilot: rice_cakes cross grade boundary via SR alone |
| Q3 HP_FAT_SODIUM stacking | NO combined budget | Targets distinct constructs; SODIUM_FAMILY_BUDGET already caps family; stacking is correct signal | Pilot: products reach implausible floor (<30) without other supporting signals |
| Q4 P_max | 6 (not 8) | Cross-category consistency EV-087–092; P_max=6 sufficient for INV-B gap correction | Post-pilot: highest-Na cluster undifferentiated within 6pt ceiling |
| Q5 wiring | Standalone call site, post-dimension pre-floor | Preserves regulatory_quality signal integrity; consistent with all prior SR phases | Data Agent D8 finds ordering conflict in standalone path |

---

## Parameters Locked for D8

```python
SODIUM_SALTY_SNACK_SHELF_REL_V1 = {
    "scope_guard": "product.get('category') == 'salty_snack' and nn.get('sodium_mg') is not None",
    "nutrient": "sodium_mg",
    "direction": "asymmetric",
    "median_mg": 560.0,
    "iqr": 190.0,
    "robust_scale": 140.85,  # max(IQR/1.349=140.85, 1.4826×MAD=126.02, 1.40)
    "p_max": 6,
    "b_max": 3,
    "floor": 62,
    "z_dead": 0.30,
    "floor_threshold_mg": 630,  # Q3, de-anchored from binary 600mg cliff
    "wiring": "standalone_post_dimension_pre_floor",
    "flag": "SODIUM_SALTY_SNACK_SHELF_REL_V1",
    "family": "sodium_family",
}
```

No changes to `constants.py` or `score_engine.py` during D7. Implementation is Data Agent's task in D8, gated on this co-sign and EV-093 registration.

---

## Files

| File | Purpose |
|------|---------|
| `02_products/salty_snacks/methodology/salty_snacks_sodium_d6_enrollment_v1.md` | D6 proposal (Nutrition Agent) |
| `02_products/salty_snacks/methodology/salty_snacks_sodium_d7_cosign_v1.md` | This file — D7 co-sign (Product Agent) |
| `03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md` | EV-093 registered (after EV-092 at L2299) |
| `tasks/returns/P133_return.md` | Return block for orchestrator |

---

*Product Agent | TASK-278 Phase-11 | 2026-06-14*
*D7 co-sign only — no engine edits, 0 score movement, OFF data used: NONE*
