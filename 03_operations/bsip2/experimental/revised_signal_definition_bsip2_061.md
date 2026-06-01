# BSIP2-061 Water Predominance — Revised Signal Definition v2

**Signal:** BSIP2-061  
**Version:** pilot_v2  
**Owner:** Chief Nutrition Officer  
**Status:** EXPERIMENTAL — Revised. Not promoted. No production deployment.  
**Revised by:** TASK-051A  
**Preceded by:** bsip2_061_water_predominance_pilot.md (pilot design, TASK-048)  
**Pilot finding:** bsip2_061_pilot_results.md (TASK-051)

---

## Revision Summary

Three changes from v1:

| Change | From v1 | To v2 |
|--------|---------|-------|
| **Chickpea-percentage gate (new WATER_PREDOMINANT trigger)** | WATER_PREDOMINANT required functional ingredient at position 3+. Compound chickpea entries ("חומוס מבושל X%") at position 1 always prevented this from firing. | WATER_PREDOMINANT also fires when the chickpea compound at position 1 declares X ≤ 45% AND standalone water is at position 2. This is Trigger B. |
| **Tahini-first protection (formalized)** | Implied in v1 but not formally specified. The detection function treated the first-listed ingredient as the primary functional ingredient — which handled tahini-first products correctly in practice. | Explicitly documented and enforced: if ingredient[0] is a tahini/sesame term AND water is at position 2, return WATER_EARLY regardless of where chickpeas appear. No WATER_PREDOMINANT on tahini-dominant products. |
| **Concentration floor for WATER_EARLY (new suppression rule)** | WATER_EARLY fired on all products where functional ingredient was at position 1 and water at position 2, regardless of the primary ingredient's declared proportion. | WATER_EARLY is suppressed (→ NOT_PREDOMINANT) when the primary ingredient's declared percentage is ≥ 70%. A product with 72% eggplant adding a small amount of water is not architecturally diluted. |

---

## Section 1 — Revised Signal Logic

### 1.1 The Core Problem This Signal Solves

Israeli commercial hummus products list cooked chickpeas as a compound entry:
`"חומוס מבושל X% (מים, חומוס, מווסת חומציות...)"`

Water appears inside the brackets as a sub-ingredient of the chickpea preparation. Reconstructed hummus further adds **standalone water** at position 2, on top of the already water-diluted chickpea compound. This two-level dilution is the structural pattern the signal must detect:

- **Level 1:** Low chickpea compound percentage (X ≤ 45%) — the compound itself is diluted
- **Level 2:** Standalone water at position 2 — additional water extends the diluted compound further

The v1 signal only detected literal water-first products (Trigger A), which do not exist in this Shufersal corpus. Trigger B closes this gap.

### 1.2 Full Detection Logic

```
Product enters BSIP2-061 evaluation
        │
        ▼
Is archetype one of: beverage, soup, bread, cereal, snack_bar_granola, fruit_puree?
        │
       YES → NOT_EVALUABLE (hard exclusion)
        │
       NO ▼
Does ingredient list have ≥ 2 items?
        │
       NO → NOT_EVALUABLE (insufficient data)
        │
       YES ▼
Is this a matbucha product?
        │
       YES → Return MATBUCHA_MANUAL_REVIEW
             (water position irrelevant; CNO ruling required before scoring)
        │
       NO ▼
Is ingredient[0] a tahini/sesame term?   ← TAHINI-FIRST PROTECTION
        │
       YES → Is water at position 2?
       │         │
       │        YES → Return WATER_EARLY (tahini at pos 1, water at pos 2;
       │                architecturally expected for tahini-dominant formulations)
       │         │
       │        NO  → Check water at position 1; if absent → NOT_PREDOMINANT
        │
       NO ▼
══════════════════════════════════════════════════════════════════════
 TRIGGER B — CHICKPEA-PERCENTAGE GATE (NEW in v2)
══════════════════════════════════════════════════════════════════════
Is ingredient[0] a chickpea compound ("חומוס מבושל X%")
  AND declared percentage X ≤ 45%
  AND ingredient[1] is standalone water?
        │
       YES → Return WATER_PREDOMINANT — full penalty
             (compound is diluted below structural threshold;
              standalone water adds a second layer of dilution)
        │
       NO ▼
══════════════════════════════════════════════════════════════════════
 TRIGGER A — ORIGINAL (unchanged)
══════════════════════════════════════════════════════════════════════
Is water at position 1 or 2?
        │
       NO → NOT_PREDOMINANT (no effect)
        │
       YES ▼
Detect primary functional ingredient (chickpea, eggplant, nut, dairy…)
        │
Is primary functional at position 3+?
        │
       YES → Is primary a naturally high-water vegetable?
       │         │
       │        YES → Return WATER_EARLY (not WATER_PREDOMINANT — per spec)
       │         │
       │        NO  → Return WATER_PREDOMINANT — full penalty
        │
       NO (functional at pos 1 or 2) ▼
══════════════════════════════════════════════════════════════════════
 CONCENTRATION FLOOR (NEW in v2)
══════════════════════════════════════════════════════════════════════
Does the primary ingredient at position 1 declare percentage ≥ 70%?
        │
       YES → Return NOT_PREDOMINANT
             (primary ingredient is sufficiently dominant; water at pos 2
              is minor and not a reliable dilution signal)
        │
       NO ▼
Return WATER_EARLY — half penalty
```

### 1.3 Signal States (unchanged from v1)

| State | Condition | Scoring effect |
|-------|-----------|----------------|
| `WATER_PREDOMINANT` | Trigger A or Trigger B fires | WFI reduced 40 pts → −1.6 pts final |
| `WATER_EARLY` | Water at pos 1–2, functional at pos 1–2; concentration floor not met; tahini-first protection doesn't apply | WFI reduced 20 pts → −0.8 pts final |
| `NOT_PREDOMINANT` | Water absent from pos 1–2, or concentration floor triggered, or no dilution pattern detected | No effect |
| `NOT_EVALUABLE` | Missing ingredients, category exclusion, matbucha | Signal suppressed |
| `MATBUCHA_MANUAL_REVIEW` | Product is matbucha subtype | Signal suppressed pending CNO ruling |

---

## Section 2 — New Rule Specifications

### 2.1 Trigger B — Chickpea-Percentage Gate

**Trigger condition (all three must be true):**

1. `ingredient[0]` begins with a chickpea compound term: "חומוס מבושל", "גרגירי חומוס מבושלים", "מחית חומוס", "חומוס" followed by a percentage
2. The declared percentage X, extracted from the ingredient string, satisfies **X ≤ 45**
3. `ingredient[1]` is standalone water (a top-level water term, not embedded inside brackets)

**Why 45%:**

The 45% threshold is derived from the structural architecture of authentic hummus. A well-made hummus has:
- Cooked chickpeas: 55–70% of the finished product
- Raw tahini: 10–20% (which itself is ~55% fat + sesame)
- Water, lemon, salt, garlic: minor components

When the chickpea compound drops to ≤ 45%, two possibilities exist:
1. **Diluted compound:** The 45% figure reflects a chickpea paste that has been extended with water to reach a larger volume
2. **Tahini-enriched:** Tahini is proportionally larger than chickpeas (e.g., 40% tahini + 26% chickpeas)

For case 2 (tahini-enriched), the TAHINI-FIRST PROTECTION takes precedence before Trigger B is evaluated. If tahini is listed first, we never reach the chickpea-percentage gate.

For case 1 (diluted compound), 45% or lower chickpea compound with standalone water at position 2 represents a two-level dilution pattern that qualifies as WATER_PREDOMINANT.

**Percentage extraction from ingredient strings:**

The declared percentage appears in various formats in Shufersal BSIP1 data:

| Format | Example | Extracted % |
|--------|---------|-------------|
| `N%` (plain integer) | "חומוס מבושל 34%" | 34.0 |
| `N%` (with decimal) | "חומוס מבושל 42.5%" | 42.5 |
| `(N%)` (in parentheses) | "חומוס מבושל (44%)" | 44.0 |
| `N% (sub...)` (compound) | "חומוס מבושל 61% (מים, ...)" | 61.0 |
| No percentage declared | "חומוס מבושל" | None (treat as NOT_EVALUABLE for Trigger B) |

Extraction rule: use a regex `(\d+\.?\d*)%` applied to the ingredient string; take the **first match** (which is always the top-level percentage, not a sub-ingredient percentage). If no percentage is found, Trigger B cannot fire — fall through to Trigger A.

### 2.2 Tahini-First Protection

**Activation condition:**

`ingredient[0]` begins with any of: `"טחינה"`, `"שומשום"`, `"tahini"`, `"sesame"`

**Effect:**

When this protection is active:
- Trigger B does NOT fire (the chickpea-percentage gate is skipped)
- Trigger A does NOT fire WATER_PREDOMINANT based on chickpea position
- If water is at position 2 → return WATER_EARLY
- If water is not at position 1 or 2 → return NOT_PREDOMINANT

**Rationale:**

A product listing tahini (40% or 37%) as its first ingredient has inverted the expected hummus hierarchy — tahini is the structural dominant, not chickpeas. In this formulation:
- Water between tahini (pos 1) and chickpeas (pos 3) serves to make the thick tahini paste workable
- The "dilution" interpretation does not apply — water is thinning the fat matrix, not replacing the chickpea content

Products confirmed affected by this protection: "חומוס עשיר ב40% טחינה" (tahini at pos 1, 40%), "חומוס מועשר 40% עם חריף" (tahini at pos 1, 37%).

### 2.3 Concentration Floor

**Activation condition:**

Primary functional ingredient at position 1 has declared percentage **≥ 70%**

**Effect:**

Return `NOT_PREDOMINANT`. The product is primary-ingredient-dominant; water at position 2 is a minor component that does not represent a dilution pattern.

**Rationale:**

A product with 72% eggplant adding a small amount of water is structurally different from a product with 44% eggplant adding water. At 72% primary ingredient, the water is secondary and cannot represent meaningful dilution of the functional content.

**Threshold:**

70% was chosen based on corpus observation: "חציל קלוי 72%" (plain grilled eggplant, 72%) with water at position 2 does not represent a diluted product. Below 70%, the dilution interpretation is more defensible.

**Products affected in the hummus corpus:**

| Product | Primary % | Old state | New state |
|---------|-----------|-----------|-----------|
| חציל על האש | 72% eggplant | WATER_EARLY | NOT_PREDOMINANT |

Only 1 product in the current corpus is affected by this floor.

---

## Section 3 — WATER_EARLY Reassessment

### Decision: Keep WATER_EARLY with modifications

The pilot found that WATER_EARLY fired on 18 products (26% of corpus) and caused 4 grade changes. The question was whether −0.8 pts is meaningful given the tight score distribution (std dev 9.64).

**Arguments for keeping WATER_EARLY:**

1. **Directional accuracy:** Every WATER_EARLY activation in the pilot was on a product where standalone water genuinely appeared after the primary ingredient. The signal is detecting a real structural pattern.

2. **Grade changes are defensible:** The 3 B→C migrations occurred on products at exactly the B/C boundary (65.2, 65.4). These products have water added as a standalone ingredient, which is an architectural choice. A modest downgrade relative to pure chickpea/tahini products is appropriate.

3. **Future discriminating power:** When BSIP2-062 (tahini density) is deployed, products with WATER_EARLY AND low tahini will accumulate both penalties, creating more meaningful differentiation. WATER_EARLY alone at −0.8 pts is subtle; combined with BSIP2-062, the total impact becomes legible.

4. **Removal cost:** Removing WATER_EARLY entirely would suppress the signal entirely for products where functional ingredient is at pos 1 with water at pos 2 — the only state that currently fires in this corpus.

**Arguments for recalibrating:**

1. The 3 B→C migrations affect products with 59–60% chickpea content. These are not obviously "reconstructed" — they are commercial hummus products where some water addition is normal. A modest B→C move may feel unfair to users.

2. At −0.8 pts, the signal is below the resolution of most meaningful quality distinctions in the corpus.

**Resolution:**

Keep WATER_EARLY at −0.8 pts but with the new concentration floor (Section 2.3). This removes the questionable high-concentration activation (72% eggplant → NOT_PREDOMINANT). The 3 B→C grade changes in the re-pilot must be reviewed against product ingredient lists to confirm they are directionally correct; if they are, they should be accepted.

**Post-BSIP2-062 re-evaluation:**

After BSIP2-062 deploys, reconsider whether WATER_EARLY's −0.8 pts should be raised to −1.0 to create clearer separation. This is a calibration decision, not a design decision, and should not block the v2 pilot.

---

## Section 4 — Expected Corpus Impact (v2 Predictions)

Predictions for the hummus corpus (run_hummus_002, 69 products):

| State | v1 (pilot) | v2 (predicted) | Change |
|-------|------------|----------------|--------|
| WATER_PREDOMINANT | 0 | **4** | +4 |
| WATER_EARLY | 18 | **13** | −5 (4 → WP, 1 → NOT_PREDOMINANT) |
| NOT_PREDOMINANT | 37 | **38** | +1 |
| MATBUCHA_MANUAL_REVIEW | 0 | 0 | — |
| NOT_EVALUABLE | 14 | 14 | — |

**Predicted WATER_PREDOMINANT activations (Trigger B):**

| Product | Chickpea % | Score before | Score after | Note |
|---------|-----------|-------------|-------------|------|
| חומוס מסעדות | 34% | 75.7 | **74.1** | −1.6 pts (was −0.8) |
| חומוס מסבחה | 44% | 64.2 | **62.6** | −1.6 pts (was −0.8) |
| חומוס גרגרים בתטבילה | 34% | 63.1 | **61.5** | −1.6 pts (was −0.8) |
| חומוס עם חציל פיקנטי | 42% | 57.9 | **56.3** | −1.6 pts (was −0.8) |

**Predicted grade changes in v2:**

Same 4 grade changes as v1 (WATER_EARLY at B/C and C/D boundaries) — no new grade changes from the WATER_PREDOMINANT upgrades, since all 4 upgraded products move by only an additional −0.8 pts without crossing a grade boundary.

**Predicted false positive rate for WATER_PREDOMINANT:**

0 expected. All 4 predicted activations are genuine reconstructed hummus cases:
- Low chickpea compound (34–44%) is architecturally below the self-sustaining threshold
- Standalone water at position 2 adds a second dilution layer
- These products also tend to have seed oil (SEED_OIL_PRESENT penalty already active) — corroborating the reconstruction pattern

---

## Section 5 — Promotion Criteria (Experimental → Production)

BSIP2-061 may leave EXPERIMENTAL status only when ALL of the following are met:

### Gate 1 — Empirical activation validation

| Criterion | Threshold | Measured in |
|-----------|-----------|-------------|
| WATER_PREDOMINANT activations | ≥ 4 in hummus corpus | v2 pilot re-run |
| False positive rate (WATER_PREDOMINANT) | ≤ 15% confirmed FPs by manual review | v2 pilot review |
| Grade changes reviewed | 100% of boundary crossings manually confirmed as directionally correct | v2 pilot review |

### Gate 2 — Signal isolation

| Criterion | Requirement |
|-----------|-------------|
| No WATER_PREDOMINANT on tahini-first products | 0 activations on "חומוס עשיר ב40% טחינה" and similar |
| No WATER_PREDOMINANT on matbucha | 0 activations without CNO manual review override |
| Concentration floor validated | Products with primary ingredient ≥ 70% do not receive WATER_EARLY |

### Gate 3 — Penalty stack compliance

| Criterion | Threshold |
|-----------|-----------|
| Max combined post-cap penalty (WATER_PREDOMINANT + existing) | ≤ −20 pts per product |
| Products at risk of combined overflow | 0 |

### Gate 4 — Sequencing

| Criterion | Requirement |
|-----------|-------------|
| BSIP2-062 (tahini density) deployed first | Required — to measure interaction before production |
| Joint interaction review | Confirm BSIP2-061 and BSIP2-062 do not double-penalize the same structural deficit on the same products |

### Gate 5 — Option C readiness (separate gate)

Option C (post-cap penalty, −10 pts) requires additional criteria beyond the above:

| Criterion | Threshold |
|-----------|-----------|
| WATER_PREDOMINANT activations across 2+ corpora | ≥ 8 total (hummus + tahini + nut butter) |
| Grade boundary analysis | Model confirms no more than 15% of corpus changes grade under Option C |
| Stacking cap re-verification | −20 pt total cap holds under combined WATER_PREDOMINANT + SEED_OIL + LONG_INGREDIENT_LIST |
| CNO sign-off | Required before Option C deployment |

---

## Section 6 — Interaction Register (updated from v1)

### vs. SEED_OIL_PRESENT penalty

**Observation from pilot:** 43/69 hummus products had SEED_OIL_PRESENT. Of the 4 predicted WATER_PREDOMINANT products in v2, all are expected to also have SEED_OIL_PRESENT. Both signals are symptoms of the same reconstructed architecture (low chickpea content → replaced with water + seed oil). They measure different observations: water position (dilution) vs. fat source quality.

**Combined stack for predicted WATER_PREDOMINANT products:**

| Product | SEED_OIL penalty | WP penalty | Combined |
|---------|-----------------|------------|---------|
| חומוס מסבחה | −3 pts | −1.6 pts | −4.6 pts |
| חומוס מסעדות | −3 pts (likely) | −1.6 pts | −4.6 pts |
| חומוס גרגרים בתטבילה | −3 pts (likely) | −1.6 pts | −4.6 pts |
| חומוס עם חציל פיקנטי | −3 pts | −1.6 pts | −4.6 pts |

All well within the −20 pt stacking cap.

### vs. BSIP2-062 (tahini density)

Not yet deployed. When deployed: products with WATER_PREDOMINANT AND low tahini density will accumulate both signals. The combined penalty must be verified to not exceed the stacking cap, and the interaction must be reviewed by the CNO to confirm both signals are measuring genuinely independent observations.

---

## Appendix — Revised Detection Logic Summary

| Product type | v1 behavior | v2 behavior |
|---|---|---|
| Chickpea compound ≤ 45%, water at pos 2 | WATER_EARLY | **WATER_PREDOMINANT** (Trigger B) |
| Chickpea compound > 45%, water at pos 2 | WATER_EARLY | WATER_EARLY (unchanged) |
| Tahini first, water at pos 2 | WATER_EARLY | WATER_EARLY (tahini-first protection explicit) |
| Tahini first, water at pos 2, chickpeas at pos 3 | WATER_PREDOMINANT (FP risk) | **WATER_EARLY** (tahini-first protection prevents FP) |
| Primary ingredient ≥ 70%, water at pos 2 | WATER_EARLY | **NOT_PREDOMINANT** (concentration floor) |
| Water at pos 1, functional at pos 3+ | WATER_PREDOMINANT | WATER_PREDOMINANT (unchanged, Trigger A) |
| No ingredients | NOT_EVALUABLE | NOT_EVALUABLE (unchanged) |
| Matbucha | MATBUCHA_MANUAL_REVIEW | MATBUCHA_MANUAL_REVIEW (unchanged) |

---

*BSIP2-061 Revised Signal Definition v2 — TASK-051A*  
*Status: EXPERIMENTAL. Revised. No production deployment.*  
*Next step: implement v2 code changes, run re-pilot per pilot_rerun_spec_bsip2_061.md*
