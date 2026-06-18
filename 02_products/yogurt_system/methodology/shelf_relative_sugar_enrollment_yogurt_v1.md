# Shelf-Relative Sugar Enrollment — Yogurt Category
## D6 Design Proposal — Awaiting D7 Co-Sign (Nutrition Agent + Product Agent)

**EV Number:** EV-088 (draft)
**Status:** D6 PROPOSAL — no engine edits, no score movement, no pilot wiring
**Author:** Nutrition Agent
**Date:** 2026-06-14
**Task:** TASK-278 Phase-6
**Authoritative corpus:** `run_yogurt_006` (88 products, 2026-06-11)
**Prior diagnostic:** `run_yogurt_shelfrel_pilot` (TASK-278 Phase-3, 2026-06-14)

---

## 1. Background

The P103 yogurt diagnostic (TASK-278 Phase-3) confirmed that the shelf-relative sugar mechanism lands cleanly on the yogurt shelf. The pilot used the same 88-product corpus as `run_yogurt_006` (authoritative yogurt run) with a runtime namespace patch that set `SUGAR_SHELF_REL_SCOPE = frozenset({'dairy_protein'})` as a diagnostic proxy.

**Key pilot results (run_yogurt_shelfrel_pilot):**
- 88 products scored; 74 with non-null sugars_g
- 61 movers (69% of corpus)
- 8 grade changes: 2 upgrades to S (plain yogurts), 5 C→B upgrades, 1 D→E downgrade
- 0% absorption (all 61 movers' SR terms fully landed)
- The shelf shows a bimodal structure: plain yogurts at 0–5g vs flavored/mix-in products at 9–14g

The biscuit pilot (P102) was degenerate — a floor-saturated shelf where SR had no headroom. Yogurt is the opposite: spread-y, spread across grades B→D, with no HP floor saturation. The mechanism is validated.

**Why the pilot scope was insufficient for production:** The pilot enrolled the entire `dairy_protein` category as a diagnostic shortcut. `dairy_protein` includes milk, hard cheeses, cheese spreads, brined cheeses, cream cheese, kefir, and cottage — all structurally different from yogurt and with different sugar distributions. A production enrollment must scope to yogurt products only within `dairy_protein`. This document designs that scope guard.

---

## 2. Authoritative Corpus

| Field | Value |
|---|---|
| Run ID | `run_yogurt_006` |
| Date generated | 2026-06-11 |
| Total products | 88 |
| Products with non-null sugars_g | 74 |
| Products with null sugars_g | 14 |
| Router category (all 88) | `dairy_protein` |
| Non-yogurt routing | 1 product routes to `cereal` (7290116932620, excluded from pilot) |
| Status | Authoritative; non-authoritative runs: run_yogurt_001 through run_yogurt_005 |

All 87 products (excluding one cereal-routed outlier) route to `dairy_protein`. All carry `bsip_yogurt_subtype` fields or `category_subtype` values in the yogurt family (see Section 3). Source of sugars_g: exclusively `L1_observed_signals.sugars_g` in committed trace files — direct product scrape, no external source.

---

## 3. Scope Guard Design

### The Core Problem

`dairy_protein` is a composite router category. It contains genuine yogurt products, but also:
- Fluid milk (חלב)
- Hard cheeses (גאודה, אמנטל, גרנה פדנו)
- Brined cheeses (פטה, בולגרית, חלומי) — already governed by EV-056 (sodium SR)
- Cream cheese / cheese spreads (גבינת שמנת, ממרח גבינה, פילדלפיה)
- Kefir (קפיר)
- Cottage (קוטג')
- Ricotta, mascarpone

Enrolling `dairy_protein` wholesale would apply yogurt sugar calibration (median 5.45g) to hard cheeses (typically 0–1g sugar) and processed cheese spreads (typically 1–3g sugar), producing nonsensical relief awards. The scope guard must restrict SR sugar to yogurt products only.

### Discriminator Options

**(A) Router `category_subtype` field — RECOMMENDED**

The router already emits a `category_subtype` field for every `dairy_protein` product via `HARD_ANCHORS`. Yogurt products receive subtypes: `"yogurt"`, `"greek_yogurt"`, `"protein_yogurt"`, `"bio_yogurt"`, `"froop_yogurt"`, `"yogurt_mixin"`. Constants.py already defines:

```python
CULTURED_YOGURT_SUBTYPES = (
    "yogurt", "greek_yogurt", "protein_yogurt", "bio_yogurt", "froop_yogurt",
    "yogurt_mixin", "bio",
)
```

The SR enrollment gate would check:
```python
category == "dairy_protein" AND category_subtype in CULTURED_YOGURT_SUBTYPES
```

**No router edit required.** The subtype field is populated by existing HARD_ANCHORS and has been stable since TASK-139C. This is the cleanest option and requires only a constants.py scope definition and a score_engine.py gate — identical to how EV-056 sodium SR gates on `dairy_protein` already (with a brined-cheese subpool check).

**Also supported by `bsip_yogurt_subtype` field:** Products scraped from the yogurt shelf carry `bsip_yogurt_subtype` (non-null), which the category prior system (CATEGORY_PRIOR_SUBTYPE_FIELDS) already maps to `dairy_protein`. This provides a secondary confirmation signal, though `category_subtype` is the primary discriminator.

**(B) Dedicated `yogurt` router category**

Adding `yogurt` as a first-class CATEGORIES entry would require router_v2.py edits (CATEGORIES list, routing resolution) and updating all callers. More invasive than needed. No benefit over Option A given the subtype field already exists.

**(C) Explicit barcode enrollment frozenset**

Would require manually maintaining a set of ~87 barcodes. Brittle for new product additions and fragile under barcode changes. Not recommended.

**(D) Hebrew name signal discriminant**

Pattern-matching on יוגורט in product name is already what produces the `category_subtype="yogurt"` anchor — Option A captures this more robustly. Not recommended as a standalone approach.

### Recommendation: Option A

**Scope constant (proposed):**
```python
SUGAR_SHELF_REL_YOGURT_SUBTYPES = CULTURED_YOGURT_SUBTYPES  # reuse existing constant
```

**Engine gate (proposed, score_engine.py):**
```python
# Gate for yogurt×sugar shelf-relative enrollment (EV-088)
is_yogurt_for_sr = (
    category == "dairy_protein"
    and category_subtype in CULTURED_YOGURT_SUBTYPES
    and flag_sugar_shelf_relative
)
```

**Router change needed:** None. `category_subtype` is already populated by router_v2.py `_build_anchor_result()` for all anchor-routed products. The kefir, cottage, cream_cheese, hard_cheese, feta_brined, bulgarian_brined, and halloumi_brined subtypes are distinct from `CULTURED_YOGURT_SUBTYPES` and will correctly be excluded.

---

## 4. Sugar Statistics (Yogurt-Only, from Authoritative Corpus)

Source: `run_yogurt_shelfrel_pilot/run_record.json` (yogurt_sugar_stats block), derived from run_yogurt_006 traces.

| Statistic | Value | Source |
|---|---|---|
| n_total products | 88 | run_yogurt_006 |
| n_with_sugars_g | 74 | L1_observed_signals, direct product scrape |
| n_excluded (null sugars_g) | 14 | not used in distribution |
| min | 2.5g | 7290114311069 (מולר אקטיב לבן0% 25חלבון) |
| Q1 | 3.9g | |
| median | 5.45g | |
| Q3 | 9.7g | |
| max | 14.0g | 7290102393060 (יוגורט מולר מיקס גליליות) |
| IQR | 5.80g | Q3 − Q1 |
| MAD (raw) | 2.55g | median(|xi − median|) |
| IQR/1.349 | 4.299g | |
| 1.4826 × MAD | 3.781g | |
| robust_scale | **4.299g** | max(4.299, 3.781, 1.4) — IQR-primary |
| scale_formula | max(IQR/1.349, 1.4826×MAD, 1.4) | per D7 co-sign (P98) |
| scale_primary | IQR-primary | IQR/1.349 = 4.299 > 1.4826×MAD = 3.781 |

### Comparison to P103 Pilot Calibration

The P103 diagnostic used these same stats (they were computed from run_yogurt_006). Values match exactly:
- Pilot recorded: median=5.45, IQR=5.80, scale=4.299
- This proposal: median=5.45g, IQR=5.80g, scale=4.299g
- Divergence: 0.0g (within calibration tolerance, no flag needed)

### Distribution Summary

The yogurt shelf is bimodal:
- **Plain yogurt cluster:** 2.5–5.0g (plain, bio, Greek, goat variants). These are genuinely low-sugar — lactose from milk is not added sugar.
- **Flavored/mix-in cluster:** 8.0–14.0g (GO flavors, מולר מיקס variants, flavored soft yogurts). Sugar added via fruit preparation, sugar, dextrose.

This bimodal structure is exactly the condition where shelf-relative scoring produces clean discrimination without needing a cliff.

---

## 5. Band Design

### Asymmetric P>B (per D7 co-sign)

The D7 co-sign (P98, shelf_relative_d7_cosign_v1.md) established asymmetric P>B as the mandatory design: penalty for above-median is steeper than relief for below-median. This reflects that sugar enrichment is a formulation choice with health implications, while naturally low sugar is a structural characteristic of plain dairy.

### Proposed Surcharge (Penalty) Bands

| z-score range | r-units above median | Surcharge (pts) |
|---|---|---|
| 0.0 – 0.5 | 0.0 – 2.15g | 0 |
| 0.5 – 1.0 | 2.15g – 4.30g | 1 |
| 1.0 – 1.5 | 4.30g – 6.45g | 2 |
| 1.5 – 2.5 | 6.45g – 10.75g | 4 |
| 2.5+ | 10.75g+ | 6 |

**P_max = 6 pts** (same as biscuits and cereals enrollment). Justification: on a shelf scoring 35–90, a 6-point maximum adjustment is 6–17% of a grade band (10 pts). Proportionate for within-shelf discrimination; does not override the backbone.

Note: The pilot used a max surcharge of 8 pts (band [2.5, null]→8). This proposal reduces P_max to 6 to match the biscuit/cereal standardization. The D7 co-sign will decide the final P_max value.

### Proposed Relief Bands

| z-score range | r-units below median | Relief (pts) |
|---|---|---|
| 0.0 – 0.5 | 0.0 – 2.15g | 0 |
| 0.5 – 1.5 | 2.15g – 6.45g | 2 |
| 1.5 – 3.0 | 6.45g – 12.90g | 3 |
| 3.0+ | 12.90g+ | 3 |

**B_max = 3 pts.** Relief is capped at 3 to preserve the absolute backbone's authority and prevent curve-grading immunity for plain yogurts on a bad shelf.

### Scale Guard

IQR ≥ 1.4 (guard met: IQR = 5.80). No low-variance shelf collapse.

---

## 6. Floor Design and Anti-Immunity Proof

### Why a Floor Is Required

The D7 co-sign (P98) requires a formulation_absolute_floor for any SR enrollment. Without a floor, high-sugar yogurts benefiting from high backbone scores (from protein quality, fermentation bonuses, or favorable processing) could reach A or B grades despite 12–14g added sugar. This violates the Anti-Immunity Rule.

### Yogurt-Specific Floor Design

Yogurt backbone scores differ from biscuits. Plain yogurts score 70–90 (B–A range). High-sugar flavored yogurts currently score 35–65 from backbone penalties (NOVA 4, additive loads, long ingredient lists). However, the engine has no consistent floor on high-sugar yogurts — some score 55+ in the C range despite 10–14g sugar, and the mix-in segment (מולר מיקס) can reach 55–65 despite high sugar.

**Floor threshold:** sugars_g ≥ 12g (dessert territory; this is 2.5+ z-scores above the median, which maps to the maximum surcharge band already)

**Floor value:** 62 (grade C ceiling)

**Rationale:**
- A yogurt with ≥12g sugar/100g is in the dessert-adjacent segment. Score ≥ 70 (grade B) would be misleading to consumers comparing it to plain yogurt.
- 62 is grade C (60–70 range). A score of 62 communicates "acceptable but not recommended" — appropriate for a sweetened yogurt variant.
- In the pilot, the highest-scoring high-sugar yogurt (7290102397600, 13.6g, score_off=62.4) is already near this floor. The floor anchors behavior going forward.

**Comparison to biscuits:** Biscuit floor = 55, reflecting that biscuit backbone scores are lower overall. Yogurt backbone is structurally higher, so the yogurt floor of 62 is calibrated to the yogurt grade distribution. The Anti-Immunity proof below holds regardless.

### Anti-Immunity Proof

Anti-Immunity formula: `floor + B_max < 70` (grade B threshold)

```
floor(62) + B_max(3) = 65 < 70 ✓ PASS
```

A high-sugar yogurt (≥12g) cannot reach grade B even with maximum SR relief, because:
- It is capped at floor = 62
- Relief (B_max = 3) is not available to products above the median — high-sugar products receive surcharges, not relief
- Even if a novel product somehow qualified for relief AND had a floor, 62 + 3 = 65 < 70

Anti-Immunity is proven. No dessert yogurt reaches grade B under this design.

---

## 7. Named Inversions

Both inversions are derived from committed `run_yogurt_006` trace files. Scores are `final_score_estimate` from `L1_observed_signals.sugars_g` — no external data source.

### Inversion 1: Within the C Band (both above median)

| Field | Product A (lower sugar, lower score) | Product B (higher sugar, higher score) |
|---|---|---|
| Barcode | 7290110321697 | 7290102397600 |
| Name | יופלה GO אפרסק | מולר מיקס שקדים ובוטנים |
| sugars_g | 9.8g | 13.6g |
| Current score (backbone) | 61.2 / C | 62.4 / C |
| Sugar delta | — | +3.8g more |
| Score delta today | — | +1.2 pts HIGHER |

**Why the inversion exists:** 7290102397600 (מולר מיקס שקדים ובוטנים) has a cleaner additive profile — 1 added sugar source vs 2, no MULTIPLE_ADDED_SUGAR_MARKERS penalty, 12 ingredients vs a longer list. The backbone rewarded its lower additive complexity. The sugar content difference (3.8g) is not currently differentiated by any backbone signal.

**How SR corrects it:**
- A (9.8g): z = (9.8 − 5.45) / 4.299 = 1.01 → band 1 → +1 pt surcharge → score ~60.2
- B (13.6g): z = (13.6 − 5.45) / 4.299 = 1.90 → band 3 → +4 pt surcharge → score ~58.4
- After SR: A (60.2) > B (58.4) — inversion corrected ✓
- Both confirmed as movers in pilot: A gets rel_pen=+2 (pilot surcharge band), B gets rel_pen=+4

### Inversion 2: Between Plain and Flavored Segments (straddling median)

| Field | Product A (lower sugar, lower score) | Product B (higher sugar, higher score) |
|---|---|---|
| Barcode | 7290102396740 | 7290102393060 |
| Name | יוגורט אפרסק+תות 0% | יוגורט מולר מיקס גליליות |
| sugars_g | 4.5g | 14.0g |
| Current score (backbone) | 36.4 / D | 43.5 / D |
| Sugar delta | — | +9.5g more |
| Score delta today | — | +7.1 pts HIGHER |

**Why the inversion exists:** 7290102393060 (מולר מיקס גליליות) has NOVA 4 confidence=0.55 (medium) and a different processing cap path than 7290102396740. Product A has NOVA 4 high-confidence (0.82), 17 ingredients, 6 additive categories, and a severe NOVA_PROXY_4_ULTRA_PROCESSED binding cap. Product B, despite 14.0g sugar vs 4.5g, benefits from fewer current engine signals against it in the score_after_penalty chain. The backbone does not discriminate by relative sugar position within the shelf.

**How SR corrects it:**
- A (4.5g): z = (4.5 − 5.45) / 4.299 = −0.22 → |z| < 0.5 → band 0 → 0 pts (no change at ≤0.5 z)
- B (14.0g): z = (14.0 − 5.45) / 4.299 = 1.99 → band 3 → +4 pt surcharge → score ~39.5
- After SR: A (36.4) is now closer to B (39.5); gap reduced from 7.1 to 3.1 pts
- Direction: partially corrected. The 7.1 pt gap is not fully eliminated because A is near-median (nearly no relief) while B gets penalized. Full inversion elimination is not the goal — SR moves the relative signal in the correct direction.
- Note: A could receive 1–2 pts of relief if scale is applied to the below-median band for z values of 0.22, which is below the 0.5 threshold. D7 can consider lowering the 0.5 threshold to 0.3 in the yogurt enrollment to pick up near-median relief.

---

## 8. EV-088 Draft

**For inclusion in `03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md` after D7 co-sign:**

```
### EV-088 — Yogurt × Sugar: Shelf-Relative Enrollment Proposal (D6)

| Field | Value |
|---|---|
| finding_id | EV-088 |
| concept | D6 enrollment proposal: yogurt × sugars_g into BARI_SHELF_RELATIVE_V1 mechanism (EV-084). Applies asymmetric P>B shelf-relative surcharge/relief within dairy_protein category, scoped to yogurt subtypes only via category_subtype in CULTURED_YOGURT_SUBTYPES. Resolves within-shelf rank inversions between plain yogurts (2.5–5g sugar) and flavored/mix-in yogurts (9–14g). |
| task | TASK-278 Phase-6 |
| recorded | 2026-06-14 |
| extends | EV-084 (shelf-relative differentiator design), EV-087 (cereals × sugar) |
| layer | Shelf-relative differentiator enrollment — scopes to category == "dairy_protein" AND category_subtype in CULTURED_YOGURT_SUBTYPES |
| scope_guard | Option A: category_subtype in CULTURED_YOGURT_SUBTYPES. No router edit required. category_subtype already populated by router_v2.py HARD_ANCHORS for all yogurt products. |
| corpus | run_yogurt_006 (2026-06-11), n=88, n_with_sugars_g=74 |
| corpus_stats | n=74, median=5.45g, Q1=3.9g, Q3=9.7g, IQR=5.80g, MAD=2.55g, robust_scale=4.299g (IQR-primary: max(4.299, 3.781, 1.4)) |
| surcharge_bands | [0,0.5)→0, [0.5,1.0)→1, [1.0,1.5)→2, [1.5,2.5)→4, [2.5,∞)→6 (in r-units) |
| relief_bands | [0,0.5)→0, [0.5,1.5)→2, [1.5,3.0)→3, [3.0,∞)→3 (in r-units) |
| P_max | 6 pts |
| B_max | 3 pts |
| floor | 62 (grade C ceiling) for sugars_g ≥ 12g (dessert territory, z ≥ 2.5+) |
| anti_immunity_proof | floor(62) + B_max(3) = 65 < 70 (grade B threshold) PASS |
| named_inversions | (1) 7290110321697 (9.8g / 61.2C) vs 7290102397600 (13.6g / 62.4C): B scores 1.2pts higher despite +3.8g sugar; SR corrects (A→60.2, B→58.4). (2) 7290102396740 (4.5g / 36.4D) vs 7290102393060 (14.0g / 43.5D): B scores 7.1pts higher despite +9.5g sugar; SR partially corrects. |
| status | D6 PROPOSAL — awaiting D7 co-sign (Nutrition Agent + Product Agent) |
| off_used | false — all stats from L1_observed_signals.sugars_g in committed trace files |
| file | 02_products/yogurt_system/methodology/shelf_relative_sugar_enrollment_yogurt_v1.md |
```

---

## 9. What D7 Must Decide

The following parameters remain open for D7 co-sign:

1. **Scope guard option (A vs B vs C):** This proposal recommends Option A (`category_subtype in CULTURED_YOGURT_SUBTYPES`). D7 must confirm this is sufficient and does not miss any yogurt products that lack a `category_subtype` (e.g., products routing via the category prior rather than a hard anchor).

2. **P_max parameter:** This proposal uses P_max=6 for standardization with cereals and biscuits. The pilot used P_max=8 (max surcharge=8 per the pilot bands). D7 must decide whether yogurt warrants a lower P_max (6, standardized) or the pilot's P_max (8, more aggressive penalization of the 13–14g sugar segment).

3. **Floor value:** Floor=62 is proposed. D7 should verify that the highest-scoring high-sugar yogurt in the corpus (7290102397600, score=62.4) falls at or below this floor, and whether the floor is tight enough to prevent grade B misclassification across the full yogurt product range.

4. **Near-median relief threshold:** The 0.5 z-unit minimum for any relief means products at 4.5g sugar (z=−0.22) receive no benefit. D7 can lower this to 0.3 to pick up the near-median plain segment, or leave it at 0.5 for standardization.

5. **Router change decision:** If D7 concludes that `category_subtype` is insufficient (e.g., some yogurt products in production lack the subtype field), Option B (dedicated yogurt category in router) may be needed. This would require a router_v2.py edit and a separate D7 scope approval.

6. **Null-sugars handling:** 14 products (16%) have null sugars_g. The pilot treated these as median-equivalent (median imputation) and all received rel_pen=−2 (minimum relief). D7 must affirm this is the correct behavior or specify an alternative (e.g., null → no SR adjustment, 0 pts).

---

## Appendix: Products with null sugars_g (14 of 88)

These products received median imputation in the pilot (→ z=0 → below 0.5 threshold → minimum relief band). Barcodes: 43944, 45771, 5416262, 5416415, 5839078, 6664990, 7290012645297, 7290110321031, 7290110321680, 7290110328221, 7290110328764, 7290110328788, 7290110329952, 7290116932484.

All are plain yogurt variants (כד yogurts, lactose-free, GO variants) that received +2 relief in the pilot — consistent with the expectation that products without sugars_g data are likely plain or minimally sweetened.

---

*This document is a D6 proposal. No engine files are modified. No scores change until D7 co-sign + pilot rescore + owner go-live (tripwire-1).*
