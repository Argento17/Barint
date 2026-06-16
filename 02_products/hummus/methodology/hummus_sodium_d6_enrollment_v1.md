# Hummus × Sodium — D6 Enrollment Proposal
**EV-094 | TASK-278 Phase-12**
**Date:** 2026-06-14
**Author:** Nutrition Agent
**Status:** PROPOSAL — pending D7 co-sign (Nutrition + Product)
**Engine modified:** NO
**Score movement:** ZERO

---

## 1. Corpus

| Field | Value |
|---|---|
| Category | Hummus and savory dips (Israeli retail) |
| BSIP2 run | `02_products/hummus/intelligence_bsip2/run_hummus_002/` |
| BSIP1 files | `02_products/hummus/canonical_bsip1/bsip1_*.json` |
| Total BSIP1 files | 69 |
| Products with sodium data | 69 (100% coverage) |
| Source | Direct Shufersal product scrape via BSIP0 HTML parse |
| OFF used | NO (banned project-wide) |

The 69-product corpus contains three sub-pools: `hummus_spread` (30), `hummus_and_savory_dips` (30), `eggplant_spread` (4), and `matbucha_pepper_spread` (5). Only the first two sub-pools constitute the hummus shelf. See Section 3 for scope guard recommendation.

---

## 2. Sodium Shelf Statistics

Nutrient: `normalized_nutrition_per_100g.sodium_mg` (BSIP1 source field)

All 69 products have sodium data — 100% coverage. Statistics below are computed on the full 69-product corpus (see Section 3 for the scope guard recommendation and its stat implications).

| Statistic | Value | Notes |
|---|---|---|
| n | 69 | All products with sodium data |
| min | 6.0 mg | |
| max | 864.0 mg | |
| Q1 | 360.0 mg | |
| median | 392.0 mg | |
| Q3 | 395.0 mg | Used as floor_threshold (de-anchored from binary 600mg cap) |
| IQR | 35.0 mg | |
| MAD | 12.0 mg | |
| mean | 354.2 mg | Reference only |
| stdev | 185.2 mg | Reference only |

**Robust scale computation (IQR-primary, per D7 spec):**

```
IQR/1.349  = 35.0 / 1.349 = 25.9451
1.4826*MAD = 1.4826 * 12.0 = 17.7912
floor       = 1.40
robust_scale = max(25.9451, 17.7912, 1.40) = 25.945
```

Robust scale >> 3.0 (standard guard): 25.945 / 3.0 = 8.6x margin. Standard guard passes.

**Critical distribution observation:** The corpus has a bimodal structure. A dense core of 40 products clusters within the Q1–Q3 band (360–395mg), with 36/69 products falling within ±6mg of the median. Outside this core: 17 products below 360mg and 12 products above 395mg. The IQR of 35mg reflects the tightness of the core, not the spread of the full shelf.

This is the primary D7 open question (see Section 7).

---

## 3. Scope Guard

**Recommendation:** `bsip0_source.product_category in ("hummus_spread", "hummus_and_savory_dips")`

**Rationale:**

The `bsip0_source.product_category` field is present in all 69 BSIP1 files and takes four values in this corpus:

| product_category | Count | In scope? |
|---|---|---|
| `hummus_spread` | 30 | YES |
| `hummus_and_savory_dips` | 30 | YES |
| `eggplant_spread` | 4 | NO |
| `matbucha_pepper_spread` | 5 | NO |

Total in-scope products: 60. The eggplant and matbucha sub-pools have structurally different sodium profiles and should not be ranked against the hummus shelf.

**Scope guard expression (at scoring time):**

```python
bsip_product_category = product.get("bsip0_source", {}).get("product_category")
if bsip_product_category in ("hummus_spread", "hummus_and_savory_dips"):
    # apply EV-094 SR
```

This field is populated directly from the BSIP0 scrape (Shufersal source category routing) and is present in all 69 canonical BSIP1 files. No new infrastructure is needed — it reads a field already available on the product object.

**Alternative considered and rejected:** Using the BSIP2 router category `sauce_spread` would be too broad — all hummus, eggplant, and matbucha products route there, and the hummus-only sodium range (~360–395mg) differs from the eggplant/matbucha range. No dedicated subtype constant currently exists for hummus in `constants.py` (unlike `CULTURED_YOGURT_SUBTYPES` or `HARD_CHEESE_YELLOW_SUBPOOLS`). A new constant will be required.

---

## 4. SR Parameters

| Parameter | Value | Basis |
|---|---|---|
| direction | asymmetric | High-sodium penalty + low-sodium relief (one-sided is insufficient given 17 products significantly below median) |
| P_max | 6 | Standard |
| B_max | 3 | Standard |
| z_threshold | 0.3 | Products with \|z\| < 0.3 receive delta=0 (standard guard) |
| floor_threshold | 395.0 mg (Q3) | De-anchored from binary 600mg Israeli cap. Q3-based. |
| floor | 62 | Anti-immunity: 62 + B_max(3) = 65 < 70 PASS |
| robust_scale | 25.945 | IQR-primary (see Section 2) |

**Anti-immunity verification:**
floor (62) + B_max (3) = 65 < 70 (grade B threshold). PASS.

**Z-score reference for key sodium values:**

| Sodium (mg) | z-score | Band | SR direction |
|---|---|---|---|
| 6 | -14.88 | Band 3 | Relief +B_max |
| 23 | -14.22 | Band 3 | Relief +B_max |
| 150 | -9.33 | Band 3 | Relief +B_max |
| 231 | -6.21 | Band 3 | Relief +B_max |
| 328 | -2.47 | Band 3 | Relief +B_max |
| 360 | -1.23 | Band 2 | Relief (scaled) |
| 380 | -0.46 | Band 1 | Relief (minor) |
| 392 (median) | 0.00 | Band 0 | No delta |
| 395 | +0.12 | Band 0 | No delta |
| 400 | +0.31 | Band 1 | Penalty (minor) |
| 452 | +2.31 | Band 2 | Penalty (scaled) |
| 480 | +3.39 | Band 3 | Penalty -P |
| 623 | +8.90 | Band 3 | Penalty -P_max |
| 852 | +17.73 | Band 3 | Penalty -P_max |

**Scale >> 3.0 guard:** 25.945 > 3.0. Standard guard passes. This is expected given the tight IQR.

---

## 5. Named Inversions

### INV-A: הקיסר חומוס ענק (150mg) vs סלט חומוס (480mg)

| Product | Barcode/ID | Sodium | Current Score/Grade |
|---|---|---|---|
| הקיסר חומוס ענק | bsip1_7290018359686 | 150 mg/100g | 80.4 / A |
| סלט חומוס | bsip1_6666307 | 480 mg/100g | 80.2 / A |

**Inversion type:** Near-identical grades despite a 3.2x sodium difference. The current engine does not differentiate sodium within the hummus shelf — both products receive grade A. The 480mg product has exceptionally high protein (18.2g/100g) that offsets all other signals, making it immune to its sodium burden at current settings.

**Expected SR correction:**
- הקיסר חומוס ענק (z = -9.33, Band 3): +B_max = +3 → new score ~83.4/A
- סלט חומוס (z = +3.39, Band 3): -P = up to -6 (capped by budget) → estimated -4 → new score ~76.2/A

Net effect: gap opens from 0.2 pts to approximately 7.2 pts. Both remain grade A but sodium is no longer invisible. This is a gap-opening correction, not a rank swap — the correct behavior when both products have legitimate strengths.

**Verification paths (from BSIP2 traces, run_hummus_002):**
- bsip1_7290018359686: sodium_mg=150.0, score=80.4, nova_proxy=3, additives=[], penalties=[]
- bsip1_6666307: sodium_mg=480.0, score=80.2, nova_proxy=3, additives=[preservative], caps=[NOVA_PROXY_3_PROCESSED], penalties=[]

### INV-B: חומוס אבו גוש (328mg) vs סלט חומוס (480mg)

| Product | Barcode/ID | Sodium | Current Score/Grade |
|---|---|---|---|
| חומוס אבו גוש | bsip1_7296073725381 | 328 mg/100g | 69.9 / B |
| סלט חומוס | bsip1_6666307 | 480 mg/100g | 80.2 / A |

**Inversion type:** True rank inversion. The product with 46% more sodium (480mg vs 328mg) scores 10.3 points higher and holds a different grade. The gap exists because the 480mg product has high protein (18.2g vs 7.0g) and no seed oil penalty, while the 328mg product is penalized for SEED_OIL_PRESENT. Sodium is invisible in both scores.

**Expected SR correction:**
- חומוס אבו גוש (z = -2.47, Band 3, below median): +B_max = +3 → new score ~72.9/B
- סלט חומוס (z = +3.39, Band 3, above Q3): -P = up to -6 → estimated -4 → new score ~76.2/A

Net effect: gap narrows from 10.3 pts to approximately 3.3 pts. Full rank swap is not achievable at these parameters — this is acceptable per Phase-7 (cheese_spreads) precedent where gap-narrowing was ruled sufficient. The 480mg product retains its grade advantage because of its genuine protein density; SR correctly modulates the sodium dimension without overriding legitimate nutrition quality signals.

**Note on maximum correction capability:** With B_max=3 and P_max=6, the maximum single-pair differential correction is 9 pts. INV-B's baseline gap of 10.3 pts exceeds this ceiling. Partial correction is the correct mechanism behavior, not a failure.

---

## 6. EV Designation

**EV-094** — Hummus × Sodium Shelf-Relative Differentiator

This follows:
- EV-092 (maadanim × sugar)
- EV-093 (salty_snacks × sodium, in parallel)

EV-094 is not yet registered in the evidence registry. Registration occurs after D7 co-sign is obtained.

---

## 7. Open Questions for D7

### Q1 (CRITICAL): Tight IQR — does the hummus corpus justify SR enrollment?

The core hummus shelf (60 products) has IQR = 35mg and 36/69 products within ±6mg of the median (380–398mg band). With robust_scale = 25.945 and z_threshold = 0.3:

- Products with sodium between ~384mg and ~400mg receive z < 0.3 and delta = 0 (the dead zone)
- Estimated dead-zone products: ~30–35 out of 60 in-scope products (50–58%)

This resembles the salty_snacks case described as "mixed signal / 59% pinned" in the Phase-3 spread analysis. D7 must decide: is 42–50% effective differentiation on the hummus shelf sufficient to justify enrollment, or does the dead-zone percentage exceed the absorption tolerance?

**My recommendation:** Enroll. The differentiation that matters is at the extremes — 17 products below 360mg (genuinely low-sodium, many scoring A) and 4 products at 700–864mg (genuinely excessive, currently scoring C/D despite sodium). The dead zone correctly identifies products where sodium is endemic to the category — uniform, not quality-differentiating. SR does not punish uniformity; it surfaces the outliers. The INV-A and INV-B inversions both involve the 480mg outlier, which is the most consequential case.

### Q2: Scope guard implementation — new constant or inline expression?

The `bsip0_source.product_category` field is available but not currently used as a scope guard in any SR call site. Options:

- **Option A (new constant):** Define `HUMMUS_PRODUCT_CATEGORIES = {"hummus_spread", "hummus_and_savory_dips"}` in constants.py, analogous to `CULTURED_YOGURT_SUBTYPES` and `CREAM_CHEESE_SPREAD_SUBTYPES`.
- **Option B (inline):** Read `bsip0_source.product_category` directly in score_engine.py, no new constant.

**My recommendation:** Option A. A named constant makes the scope explicit, testable, and consistent with the pattern established in Phases 6–8. It also enables the Data Agent to grep for scope guards without reading score_engine.py logic.

### Q3: Stats should be re-confirmed on in-scope n=60 only

Current stats are computed on all 69 corpus products. The eggplant and matbucha products have different sodium profiles. D7 should decide: re-compute stats on in-scope n=60 only, or accept n=69 (which includes the 9 out-of-scope products)?

**My recommendation:** Re-compute on n=60 in-scope products. This is the established precedent (Phase-5 cereals: stats corrected from n=45 to n=34 cereal-only). The eggplant/matbucha products may have different sodium distribution characteristics that shift the median and IQR. Stats should reflect the shelf being ranked.

**Implication:** If D7 accepts Option A (re-compute on n=60), the enrollment doc should be revised with updated stats before the Data Agent wires the engine. This proposal presents n=69 stats as the working basis; the D7-corrected n=60 stats are the binding implementation target.

### Q4: HIGH_SODIUM_700MG_PLUS cap interaction

Three products currently have sodium ≥ 852mg and the HIGH_SODIUM_700MG_PLUS hard cap (60) fires on bsip1_7296073451969 (852mg/48.0/D). With SR enrollment:

- These products are already capped at 60 or lower by the binary rule
- SR would add an additional penalty of -P_max = -6

D7 must confirm: is double-application (binary cap + SR penalty) acceptable for high-sodium products, or should the SR branch be suppressed when the binary sodium cap fires? The precedent from brined_cheeses (EV-056) did not encounter this interaction. The concern is that stacking a -6 SR penalty on a product already capped at 60 is redundant — the cap already prevents grade inflation, and the additional penalty produces no consumer-visible outcome beyond driving the score deeper into D/E territory.

**My recommendation:** Suppress SR sodium penalty when HIGH_SODIUM_700MG_PLUS fires (i.e., `if sodium_mg >= 700: skip_SR`). The binary cap adequately signals extreme sodium; SR is redundant here and adds complexity without consumer benefit.

### Q5: Two insufficient_data products

Two products (bsip1_7296073733317 at 23mg and bsip1_7296073733348 at 64mg) received `score=50/insufficient_data` in run_hummus_002. These are in-scope hummus products with valid sodium data. The SR should still apply (low sodium → relief), but the base score of 50 is a data-sufficiency floor, not a genuine composite score. D7 should confirm: apply SR to insufficient_data products or skip?

**My recommendation:** Skip SR for insufficient_data products. Applying SR to a data-floor score produces a misleading result (e.g., 50 + 3 = 53/C) that suggests the product has been evaluated when the engine explicitly could not score it. This aligns with the spirit of the insufficient_data designation.

---

## 8. Methodology Rationale

Hummus is a whole-food product where sodium is the primary quality-differentiation signal available at the category level. The NOVA proxy assigns most hummus products NOVA 3 (processed, preservative or acidity regulator present), which binds a cap of 87 and limits vertical separation. The fat profile (seed oil presence drives -3 for many products) creates a similar horizontal band. Within this constrained landscape, sodium is the one continuous signal that varies meaningfully across the shelf — from 6mg (fresh-ground tahini-forward products) to 864mg (industrial preparations).

The de-anchored floor_threshold at Q3 (395mg) reflects where the genuine hummus shelf ends and excess-sodium formulations begin. The Israeli binary 600mg cap is appropriate as a harm signal but insufficient as a quality differentiator — 9 products score above 395mg and below 600mg, none of which are currently penalized despite adding 50–60% more sodium than the shelf median.

The SR mechanism is not intended to reshuffle grades across the full hummus shelf. It is intended to:
1. Surface the quality signal at the extremes (low-sodium whole-food hummus deserves relief; high-sodium industrial preparations deserve penalty)
2. Make the 480mg "סלט חומוס" product visible as a high-sodium outlier despite its strong protein profile
3. Not punish the 40-product homogeneous core where sodium uniformity reflects category physiology, not formulation choice

This is consistent with the owner directive (2026-06-14): relative scoring expresses within-shelf variation where it exists, does not manufacture differentiation where none exists.

---

## 9. What This Proposal Does Not Do

- Does not modify score_engine.py or constants.py (engine unmodified)
- Does not move any published scores
- Does not register EV-094 (held pending D7)
- Does not change the binary HIGH_SODIUM_700MG_PLUS cap rule
- Does not affect non-hummus categories or frozen-category baselines

---

## Source Verification

All sodium values sourced from:
- `02_products/hummus/canonical_bsip1/bsip1_*.json` → `normalized_nutrition_per_100g.sodium_mg`
- Populated from direct Shufersal HTML scrape (BSIP0), `scraped_at` 2026-05-30
- `bsip0_source.matched_by: shufersal_bsip0_html_scrape` confirmed on all products
- OFF not consulted (banned)

BSIP2 scores from `02_products/hummus/intelligence_bsip2/run_hummus_002/products/bsip1_*/bsip2_trace.json`, marked AUTHORITATIVE in `run_hummus_002/AUTHORITATIVE.md`.
