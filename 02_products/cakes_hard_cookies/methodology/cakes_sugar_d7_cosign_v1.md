# Cakes × Hard Cookies × Sugar — D7 Co-Sign
## Product Agent Decision | EV-098 | TASK-278 Phase-13

**Status:** D7 CO-SIGNED — EV-098 registered, pilot gate locked
**Product Agent:** Claude Sonnet 4.6
**Date:** 2026-06-15
**D6 source:** `02_products/cakes_hard_cookies/methodology/cakes_sugar_d6_enrollment_v1.md`
**Extends:** EV-087 (cereals×sugar), EV-088 (yogurt×sugar), EV-092 (maadanim×sugar), EV-093 (salty_snacks×sodium), EV-094 (hummus×sodium)
**EV assigned:** EV-098 (EV-095 already registered for margarine research TASK-284; EV-096/097 also registered same date)
**OFF data used:** NONE — all corpus stats derived from BSIP2 traces sourced from direct Shufersal + Yohananof scrape via BSIP0 HTML parse. OFF not consulted. OFF ban satisfied.

---

## Q1 — floor_threshold: median (29.0g) vs Q3 (33.0g)

**Decision: USE Q3 = 33.0g as floor_threshold.**

Decisive reason: Consistency with EV-087 through EV-094 across eight prior enrollments is the binding constraint. Every prior SR enrollment used Q3 as the floor_threshold; the surcharge zone covers the top 25% of the distribution by design. The D6 argument for median rests on the claim that the 40–70g tail is "already floor-compressed, so effective surcharge has near-zero absolute effect there." This is true — but it is equally true for every prior indulgent category enrolled. The argument is not cakes-specific; it is a general property of the SR mechanism in indulgent categories. Accepting it here would retroactively destabilize the rationale for all prior Q3 choices. Furthermore, the modal range of this corpus is 30–35g (35/143 products, 24.5%), meaning a median threshold of 29.0g would pull the surcharge zone boundary into the center of the densest product cluster. Products at 30–33g — the typical, representative cakes product — should not be penalized relative to the shelf: they are the shelf. Using Q3=33g correctly targets only the top quartile, where sugar genuinely exceeds the norm for this already-indulgent category.

Reversal condition: If a future evidence review shows that products in the 29–33g band are creating material scoring inversions that Q3 threshold cannot resolve — specifically, if the Nutrition Agent identifies inversion pairs where both products fall below 33g and SR is structurally unable to resolve the inversion at Q3. That scenario does not exist in the current corpus.

---

## Q2 — Floor + SR Bonus for Already-Floored Products

**Decision: ACCEPT. Floor is a minimum guarantee; SR bonus is additive.**

D6's framing is correct and consistent with all prior SR enrollments. The floor (52) guarantees that no cakes product falls below 52 due to cap accumulation. When a product at score-after-all-caps < 52 also has low sugar (z < −0.30), it receives up to +B_max = +3 bonus from SR, which may lift it above the floor. This is intended and correct behavior for three reasons:

1. The floor protects against over-penalization from non-sugar signals (PHVO, NOVA-4, additive load). A product that earns a floor guarantee but also has genuinely low sugar deserves the SR relief on top of that floor protection.
2. The anti-immunity check (floor + B_max = 52 + 3 = 55 < 70) holds regardless of the path — whether a product arrives at floor from below or receives bonus from above floor, the ceiling is structurally enforced.
3. The 9 products in the 0–5g sugar band carry severe PHVO and additive penalties that suppress their scores to 18–26 range. SR bonus of up to +3 does not eliminate those penalties; it provides honest directional relief for the sugar dimension only.

This framing is accepted without qualification. No modification to the D6 proposal.

Reversal condition: If a product receives SR bonus that lifts it past 55 (floor + B_max) — which would require a bug in the floor guard. The implementation test in C7/C8 catches this. If pilot shows any bonus recipient exceeding 55, that is a D8 implementation error, not a D7 framing error.

---

## Q3 and Q4 — Data Agent Operational Flags

These are D8 implementation requirements. They do not block D7 sign-off.

**Q3 (Scope guard field verification):** Data Agent must grep-verify that all 149 IN_SCORED BSIP1 files carry the expected field before wiring. Primary guard: `product.get("category") == "cakes_hard_cookies"`. Fallback: `product.get("bsip1_canonical_id", "").startswith("bsip1_cakes_")`. Data Agent chooses the canonical implementation after field verification.

**Q4 (OOS trace contamination):** 17 OOS products in run_cakes_001/products/ must not participate in SR computation. The scope guard handles this if BSIP1 category field is absent or differs for OOS products. Data Agent must confirm that OOS products either (a) lack the BSIP1 category field, or (b) carry a different value. If OOS products carry the same category field, the scope guard must cross-reference corpus_filter.json decisions explicitly.

Both flags are written into the D8 requirement section of this co-sign and are recorded in EV-098. They are not blocking.

---

## Anti-Immunity Proof

floor(52) + B_max(3) = **55 < 70 PASS**

Structural verification:
- B-grade threshold = 70
- Maximum score achievable via SR relief: 52 (floor) + 3 (B_max) = 55
- Products above Q3 (33.0g, n ≈ 36 products = top 25% of 143) sit in the surcharge zone (z > 0) — they receive negative delta; they cannot receive B_max relief
- The floor-plus-relief scenario (55) applies only to products with sugar well below Q3; those products carry PHVO, NOVA-4, and additive penalties that further constrain their actual ceiling
- No cakes_hard_cookies product can reach B-grade (70) through SR mechanics alone
- The actual category ceiling from run_cakes_001 is 54.5/C — confirming that even without SR, B is unreachable on this shelf

---

## Named Inversions — D7 Verification

### INV-A: מיני שטרודל חלבה שוקולד vs פרה קראנץ' שוקולד לבן

| Product | Barcode | Sugar/100g | Current Score | Sugar z-score |
|---|---|---|---|---|
| מיני שטרודל חלבה שוקולד | 4504687 | 2.0g | 18.2/E | −2.985 |
| פרה קראנץ' שוקולד לבן | 7290105364784 | 47.0g | 18.4/E | +1.987 |

Current gap: 0.2pt in the wrong direction (45g sugar difference, score difference near-zero).
Both |z| >> 0.30: strudel z=−2.985 PASS, krantz z=+1.987 PASS.
SR expected direction: strudel → +B_max bonus, krantz → −P_max penalty.
Estimated post-SR gap: ~9 pts (correct direction: strudel scores higher).
Pilot gate C3 test: |gap_on| > |gap_off| AND strudel scores above krantz at flag-on.
**INV-A ACCEPTED as qualifying C3 pair.**

### INV-B: עוגת פס דובדבנים vs עוגיות אוראו בציפוי שוקולד לבן

| Product | Barcode | Sugar/100g | Current Score | Sugar z-score |
|---|---|---|---|---|
| עוגת פס דובדבנים | 1361177 | 11.0g | 13.6/E | −1.989 |
| עוגיות אוראו בציפוי שוקולד לבן | 7622300489427 | 49.0g | 16.5/E | +2.209 |

Current gap: 2.9pt in the wrong direction (38g sugar difference).
Both |z| >> 0.30: cherry cake z=−1.989 PASS, Oreo coated z=+2.209 PASS.
SR expected direction: cherry cake → +B_max bonus, Oreo → −P_max penalty.
Estimated post-SR gap: ~6 pts (correct direction: cherry cake scores higher).
Both remain E-grade — goal is score rank correction within E tier, not grade movement.
Pilot gate C3 test: |gap_on| > |gap_off| AND cherry cake scores above Oreo at flag-on.
**INV-B ACCEPTED as qualifying C3 pair.**

---

## Pilot Gate — 11 Criteria (Locked)

| # | Name | Pass condition | Fail type |
|---|---|---|---|
| C1 | directional_distribution | Mean delta above-Q3 products (sugars_g > 33.0g) ≤ 0; mean delta below-Q3 products (sugars_g < 33.0g and outside dead zone) ≥ 0 | Soft |
| C2a | grade_dist | Net C+D+E count not degraded at flag-on vs baseline (run_cakes_001) | Soft |
| C2b | grade_absorption | No single grade absorbs >40% of movers | Soft |
| C2c | magnitude | Mean |delta| for movers in [0.5, P_max=6] | Soft |
| C3 | gap_narrows_inversion | INV-A: gap widens, strudel (bc=4504687) above krantz (bc=7290105364784) at flag-on. INV-B: gap widens, cherry cake (bc=1361177) above Oreo (bc=7622300489427) at flag-on. Both pairs must pass. | Soft |
| C4 | min_movers | ≥5 cakes_hard_cookies products with |delta| ≥ 1pt (sugars_g signal must activate) | Soft |
| C5 | min_grade_changes | ≥1 grade change at flag-on (E→D expected for lowest-sugar outliers near current score ceiling) | Soft |
| C6 | max_absorption | Dead zone products (sugars_g in 21.3–31.7g, |z|≤0.30) ≤ 40% of corpus at flag-on | Soft |
| C7 | anti_immunity | 0 cakes_hard_cookies products with sugars_g ≥ 33.0g reach grade B (≥70) at flag-on | **Hard fail** |
| C8 | floor_compliance | All cakes_hard_cookies products: flag-on score ≥ 52 (floor enforced); and no product receiving B_max bonus exceeds 55 (floor + B_max ceiling enforced) | **Hard fail** |
| C9 | no_scope_bleed | 0 non-cakes_hard_cookies products with SUGAR_CAKES_SHELF_REL_V1 fired in trace | **Hard fail** |
| C10 | frozen_milk_headpin | CRITICAL: 20/20 milk run_005_headpin products delta=0.0 at flag-on. Milk scores are frozen invariant — any movement = implementation blocker. | **Hard fail** |
| C11 | flag_off_drift | Flag-off scores match run_cakes_001 baseline ±5pts (documentation only — not a pass/fail gate for flag-on validation) | Docs only |

**Hard fails: C7, C8, C9, C10** — any single failure blocks D8 implementation.
**Soft fails: C1, C2a, C2b, C2c, C3, C4, C5, C6** — failures require Product + Nutrition joint review before block decision.

Note on C5: Given the score distribution (median 17.4, max 54.5), E→D grade changes require SR bonus to lift a product from the high-50s E zone to 55+. The 5 products currently at C (scores ~54.5 range) are low-sugar structural outliers — SR bonus may lift the lowest-sugar ones marginally but they are already at C. Grade movement will be limited; C5 confirms the signal is active at all.

---

## D7 Decisions Summary Table

| Q | Decision | Decisive Reason | Reversal Condition |
|---|---|---|---|
| Q1 floor_threshold | Q3 = 33.0g (not median 29.0g) | Cross-category consistency EV-087–094; median threshold would penalize the modal product band (30–35g), which is the shelf norm, not an outlier | INV pairs emerge where both products are below 33g and SR cannot resolve them at Q3 threshold |
| Q2 floor+SR bonus | ACCEPT — floor is minimum guarantee, SR is additive | Consistent with all prior SR enrollments; anti-immunity holds at floor(52)+B_max(3)=55<70 regardless of path | Pilot shows bonus recipients exceeding 55 (implementation bug, not D7 framing error) |
| Q3 scope guard verification | D8 requirement — does not block D7 | Operational flag; field verification is Data Agent's task before wiring | N/A — D8 blocker if field absent |
| Q4 OOS contamination check | D8 requirement — does not block D7 | Operational flag; scope guard handles if field differs for OOS products | N/A — D8 blocker if OOS products share category field with IN_SCORED products |

---

## Parameters Locked for D8

```python
SUGAR_CAKES_HARD_COOKIES_SHELF_REL_V1 = {
    "scope_guard": "product.get('category') == 'cakes_hard_cookies' and nn.get('sugars_g') is not None",
    "scope_guard_fallback": "product.get('bsip1_canonical_id', '').startswith('bsip1_cakes_') and nn.get('sugars_g') is not None",
    "nutrient": "sugars_g",
    "direction": "asymmetric",
    "n_scope": 143,
    "median_g": 29.0,
    "q1_g": 21.0,
    "q3_g": 33.0,
    "iqr": 12.0,
    "mad": 6.1,
    "robust_scale": 9.044,  # max(IQR/1.349=8.895, 1.4826×MAD=9.044, 1.40)
    "p_max": 6,
    "b_max": 3,
    "floor": 52,
    "z_dead": 0.30,
    "floor_threshold_g": 33.0,  # Q3 — D7 decision; surcharge zone = top 25% of corpus
    "wiring": "standalone_post_dimension_pre_floor",
    "flag": "SUGAR_CAKES_HARD_COOKIES_SHELF_REL_V1",
    "family": "sugar_family",
}
```

**Scope guard field note (D8 requirement):** Data Agent must grep-verify that `product.get("category") == "cakes_hard_cookies"` returns the expected value in all 149 IN_SCORED BSIP1 files before wiring. If the primary guard is absent, use the fallback (`bsip1_canonical_id.startswith("bsip1_cakes_")`). Data Agent chooses the canonical implementation. D8 is blocked until field verification completes.

**OOS contamination note (D8 requirement):** 17 OOS products in run_cakes_001/products/ must be excluded. Data Agent must confirm that OOS products either lack the BSIP1 category field or carry a different value. If they share the same category field, implement explicit cross-reference to corpus_filter.json.

No changes to `constants.py`, `score_engine.py`, or any engine file during D7 or before pilot gate clears. `BARI_SHELF_RELATIVE_V1` stays default=False.

---

## Files

| File | Purpose |
|---|---|
| `02_products/cakes_hard_cookies/methodology/cakes_sugar_d6_enrollment_v1.md` | D6 proposal (Nutrition Agent) |
| `02_products/cakes_hard_cookies/methodology/cakes_sugar_d7_cosign_v1.md` | This file — D7 co-sign (Product Agent) |
| `03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md` | EV-098 registered (appended after EV-097) |

---

*Product Agent | TASK-278 Phase-13 | 2026-06-15*
*D7 co-sign only — no engine edits, 0 score movement, OFF data used: NONE*
