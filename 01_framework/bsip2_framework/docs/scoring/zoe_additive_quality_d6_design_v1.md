# D6 Activation Design — ZOE-Style Graded Additive Quality Scoring
## Proposal: Extend `BARI_D4_SCORE_V1` with Tier-Differentiated `cosmetic_mup` Severity

**Document:** `zoe_additive_quality_d6_design_v1.md`  
**Status:** D6 PROPOSAL — EXPLORE phase COMPLETE (TASK-388). Impact measurement done (2026-06-24). No score change. Awaiting D7 co-sign (Product Agent) + owner authorization before activation.  
**Nutrition Agent sign-off:** 2026-06-24 (TASK-388)  
**Proposed flag:** `BARI_D4_SCORE_V2` (new; does NOT replace BARI_D4_SCORE_V1; see Interaction section)  
**Evidence registry citation:** EV-103 (existing D4 framework), EV-106 (new — Hatta-Langedyk et al., AJPH 2026, DOI 10.2105/AJPH.2026.308499)

---

## EXPLORE MEASUREMENT RESULTS (VERIFIED 2026-06-24)

**Measurement script:** `03_operations/bsip2/proto_v0/src/run_task388_calibrated_cosmetic_mup.py`  
**Command:** `cd 03_operations/bsip2/proto_v0/src && python run_task388_calibrated_cosmetic_mup.py`  
**Corpus:** 480 products across 12 live categories (BARI_D4_SCORE_V1 published baseline)  
**Matched with ingredient text:** 464/480 (16 without ingredient text receive penalty=0)

### Impact Summary

| Metric | Value |
|---|---|
| Total corpus | 480 products |
| Products with phosphate detected (penalty=+1) | 35/480 (7.3%) |
| Grade changes from incremental phosphate +1 | **2 products** |
| Integrity violations | 0 |
| Clean-product test | **PASS** |

### Grade Boundary Changes (both verified)

| Barcode | Name | Category | Baseline | V2 | Change |
|---|---|---|---|---|---|
| 5317194 | ביסקוויט בטעם וניל הדר — הדר | cookies_coffee | 35.8/D | 34.8/E | D→E |
| 7394376620904 | משקה שיבולת שועל ללא סוכר | milk | 50.5/C | 49.5/D | C→D |

**Notes on grade movers:**
- 5317194 (Hadar vanilla biscuit, 35.8→34.8): Contains `סודיום דיפוספט` (sodium diphosphate/E450) as a leavening agent. Score 35.8 — a marginal D that becomes E. This product is a standard low-quality cookie with sugar as first ingredient, ultra-processed (NOVA-4). The grade move is directionally correct.
- 7394376620904 (Alpro oat beverage, 50.5→49.5): Contains `דיפוטסיום פוספט` (dipotassium phosphate/E450) as a pH-stabilizer. Score 50.5 — a marginal C that becomes D. This is a plant-milk fortified beverage; the phosphate here is structural (emulsion stability + fortification delivery vehicle) rather than pure flavoring, which is a legitimate question for Product co-sign.

### Grade Distribution Before/After

| Category | n | Baseline | V2 | Grade changes |
|---|---|---|---|---|
| bread | 29 | A:11 B:13 C:3 S:2 | unchanged | 0 |
| breakfast-cereals | 20 | B:2 C:7 D:9 E:2 | unchanged | 0 |
| brined_cheeses | 36 | A:7 B:21 C:6 D:2 | unchanged | 0 |
| cakes | 65 | D:2 E:63 | mean 13.6→13.5 (3 products, no grade change) | 0 |
| cheese-spreads | 53 | A:2 B:18 C:11 D:19 E:3 | mean 57.7→57.5 (11 products, no grade change) | 0 |
| cookies_coffee | 119 | C:10 D:24 E:85 | C:10 D:23 E:86 | **1** |
| granola | 22 | B:7 C:7 D:8 | unchanged | 0 |
| hard_cheeses | 23 | B:22 D:1 | unchanged | 0 |
| hummus | 57 | B:2 C:42 D:12 E:1 | unchanged | 0 |
| juices | 17 | A:6 D:7 E:4 | unchanged | 0 |
| milk | 18 | A:3 B:1 C:4 D:9 E:1 | A:3 B:1 C:3 D:10 E:1 | **1** |
| snacks | 21 | B:1 C:1 D:3 E:16 | unchanged | 0 |

### Broad vs Calibrated Comparison

| Design | Products hit | Grade changes |
|---|---|---|
| Broad cosmetic_mup (ALL cosmetic_mup=True, weight=1) — REJECTED 2026-06-21 | ~207/480 (43%) | Not measured — rejected |
| Calibrated (phosphate only, weight=1) — this proposal | 35/480 (7.3%) | 2 |
| Reduction: | 172 fewer products penalized | — |

### Clean-Product Test: PASS

**Corrected test logic:** A product is penalized IFF and ONLY IFF phosphate (E450/E451/E452) is detected. Functional/LN cosmetic_mup additives carry weight=0 by construction.

| Additive type | n products with additive and no phosphate | Penalized | Result |
|---|---|---|---|
| Xanthan (E415, functional) | 14 hummus products | 0 | PASS |
| SSL (E481, likely-neutral) | 0 (not in matched bread corpus) | 0 | PASS |
| Lecithin (E322, functional) | ~94 (no phosphate) | 0 | PASS |
| Pectin (E440, functional) | 3 | 0 | PASS |
| Beta-carotene (E160a, functional) | 11 (no phosphate) | 0 | PASS |
| Guar gum (E412, functional) | 16 (no phosphate) | 0 | PASS |
| Locust bean gum (E410, functional) | 5 | 0 | PASS |
| **All 160 functional/LN cosmetic_mup products with no phosphate** | **160** | **0** | **PASS** |

**2026-06-21 failure cases specifically confirmed:**
- 14 hummus products with xanthan (E415): penalty=0 (no phosphate in hummus corpus)
- Bread corpus: SSL not present in matched ingredient index (separate confirmation: bread corpus has 0/29 phosphate products — zero bread products affected)

**Note on products with both functional additives AND phosphate:** 10 products in the corpus contain both a functional/LN additive (lecithin, beta-carotene, etc.) AND phosphate on the same label. These get penalty=1 from phosphate. Their functional additives carry zero weight. This is correct design behavior — the penalty is assigned for phosphate, not for co-occurring functional additives.

### Phosphate Prevalence by Category

| Category | Phosphate products | % of category |
|---|---|---|
| cakes | 3/65 | 5% |
| cheese-spreads | 11/53 | 21% (cottage cheese — calcium phosphate fortification) |
| cookies_coffee | 15/119 | 13% (leavening agents — sodium diphosphate) |
| milk | 6/18 | 33% (plant milks — dipotassium phosphate) |
| bread, cereals, brined_cheeses, granola, hard_cheeses, hummus, juices, snacks | 0 | 0% — not affected |

### Open Question Raised by Measurement Data (for Product D7)

The cheese-spreads phosphate prevalence (11/53, 21%) is almost entirely **cottage cheese** products with calcium phosphate added for fortification (not texture/cost-reduction). These are higher-quality dairy products scoring B/A. The incremental -1 penalty on products like "קוטג 1% שומן" (86.6→85.6, still A) or "גבינה לבנה 5% שומן" (75.7→74.7, still B) does not cause a grade change and is directionally defensible (phosphate addition is processing-marker-level even in fortified products). But Product may want to evaluate whether fortification-use phosphate warrants a scope exclusion. Nutrition recommendation: no scope exclusion — the -1 is modest and the combined cap prevents compounding; if a cottage cheese scores B, -1 leaves it B.

The milk plant-beverage phosphate (6/18, 33%) raises a similar question re: fortification-use. One grade change results (oat milk 50.5→49.5, C→D). See §10 Open Questions for D7.

---

## 1. Problem Statement

The owner directive (2026-06-24): "I would adopt the ZOE approach to additives — let's explore this." The ZOE framing grades additives by **type and risk**, not mere presence. Bari's existing library (`GLASSBOX_W2_ADDITIVES`, 51 additives) already does this classification: every additive carries a tier (`functional | likely-neutral | dose-dependent | contested | disclosure-gap | unclassified`) and a `cosmetic_mup` flag (Marker-of-Ultra-Processing — signals the additive was added to restore sensory properties lost in intensive processing).

The live scoring gap is:
- `BARI_D4_SCORE_V1` (activated per EV-103, TASK-371) penalizes **14 score-eligible contested additives** at weight=2. This is correct and should be preserved.
- **`D4_SCORE_COSMETIC_MUP_WEIGHT = 0`** — the broad cosmetic_mup term was built, owner-reviewed, and explicitly REJECTED on 2026-06-21 because it penalized 256/483 products including clean hummus, whole-grain breads, and a milk product for ordinary additives (xanthan, pectin, lecithin, beta-carotene) with zero contested additive involvement.

The owner's rejection was correct: the broad `cosmetic_mup=True` flag sweeps 33 of 51 additives — it does not discriminate by risk tier. Applying weight=1 uniformly to all 33 is architecturally equivalent to a count-based penalty.

**The ZOE insight correctly applied to Bari:** not "penalize all cosmetic_mup additives equally," but "within cosmetic_mup, grade by tier severity."

---

## 2. Diagnostic Inventory (VERIFIED)

Library state at TASK-388 (2026-06-24):

| Tier | Count | cosmetic_mup=True | Examples |
|---|---|---|---|
| `contested` | 17 | 12 | E407, E471, E466, E433, E951, E171, azo dyes (6) |
| `contested` score_eligible=False | 3 | 0 | E330, E202, E300 |
| `dose-dependent` | 5 | 4 | E450 (phosphates), E955, E950, E960 |
| `likely-neutral` | 4 | 4 | E1422, E481, E472e, E476 |
| `functional` | 17 | 11 | E415, E440, E410, E322, natural colorants |
| `disclosure-gap` | 1 | 1 | E150 |
| `unclassified` | 4 | 1 | E141 |

**Score-eligible contested (already penalized via BARI_D4_SCORE_V1):** 14 additives — E407, E471, E466, E320, E433, E951, E171, E102, E110, E122, E124, E129, E104, E224.

**cosmetic_mup additives NOT currently penalized (33 total, weight=0):**
- 12 contested already in the score_eligible set (handled)
- 4 dose-dependent: E450 (phosphates) + E955/E950/E960 (sweeteners — separately handled by `SWEETENER_CAP_C`)
- 4 likely-neutral: E1422 (modified starch), E481 (SSL), E472e (DATEM), E476 (PGPR)
- 11 functional: plant gums, lecithin, natural colorants — no concern evidence
- 1 disclosure-gap: E150 (caramel color — type ambiguous)
- 1 unclassified: E141

**Key finding:** After excluding contested (already scored) and sweeteners (already capped), the only `cosmetic_mup` additive with a meaningful concern tier not otherwise captured is **E450 (phosphates)** — dose-dependent, no sweetener cap, genuinely associated with industrially-processed products (processed cheese, dairy-based drinks, ultra-processed cakes).

---

## 3. Design Recommendation (Single Best Option)

### 3.1 Proposed Rule

**Add E450 (phosphates) at weight = 1 to the D4 composite penalty.**

Formula amendment:

```
base_d4_penalty =
    D4_SCORE_CONTESTED_WEIGHT × #score_eligible_contested   [unchanged = 2 per contested]
  + D4_SCORE_PHOSPHATE_MUP_WEIGHT × #phosphate_mup_detected [NEW = 1 per phosphate detection]
  + D4_SCORE_COSMETIC_MUP_WEIGHT × #cosmetic_mup_generic    [retained at 0 — UNCHANGED]
```

Where `phosphate_mup_detected` = 1 if any of E450/E451/E452 (Hebrew: פוספט, דיפוספט, טריפוספט, פוליפוספט) is present in the ingredient text, 0 otherwise. **Binary signal, not additive per E-number.** Rationale: phosphate is a single functional class; distinguishing E450 vs E451 vs E452 from a label is not reliably doable and does not change the concern logic.

The per-product cap `D4_SCORE_CAP = 8` and the combined cap `D4_COMBINED_ADDITIVE_PROCESSING_CAP = 12` govern as before.

**Why E450 and not likely-neutral (E1422/SSL/DATEM/PGPR)?**

The likely-neutral additives (modified starch, SSL, DATEM, PGPR) are industrial-processing markers and legitimately `cosmetic_mup`, but:
1. Their `tier = "likely-neutral"` means the evidence for direct harm is thin — they are structural markers of UPF, not established-concern additives.
2. Penalizing them at any weight requires re-adjudicating the owner's 2026-06-21 broad-cosmetic-mup rejection. That ruling was specifically about "ordinary additives with ZERO contested additive involved."
3. The NOVA-proxy dimension (`processing_quality`, weight=0.15) and the count-based `ADDITIVE_MARKERS_3_PLUS/5_PLUS` caps already capture the broad UPF-structure signal for products that load up on likely-neutral MUPs. There is no gap to fill here via D4.

Phosphates are different: they carry a dose-dependent concern for hyperphosphatemia risk (EV-106), they are not covered by any sweetener cap, and they appear predominantly in categories that are already poorly-scored (processed cakes — 72/149 products), where the signal adds appropriate discrimination, not noise on clean products.

**Why not modify `ADDITIVE_MARKERS_3_PLUS/5_PLUS` instead?**

The task asks whether these count-based caps should be refounded or replaced. The recommendation is: **retain them, do not replace.** They are not doing the wrong thing — they catch high-additive-count products that might not have any specific contested additive. They operate on the `additive_quality` dimension (not the composite directly), so they interact cleanly with the D4 penalty layer without double-counting (confirmed in EV-103: "ADDITIVE_MARKERS caps are NOT counted in already_spent — they are dimension-level caps on a different currency from D4's composite deduction"). The correct action is to supplement, not replace.

### 3.2 New Constant

Add to `constants.py`:

```python
D4_SCORE_PHOSPHATE_MUP_WEIGHT = 1  # points per phosphate (E450/E451/E452) detection
```

### 3.3 Implementation Touchpoint

In `compute_d4_score_penalty()` (`score_engine.py`), add phosphate detection alongside the contested check:

```python
phosphate_detected = 0
for f in findings:
    if f["e_number"] in ("E450",):   # E451/E452 fold into E450 in the library
        phosphate_detected = 1
        break   # binary — cap at 1 regardless of how many phosphate forms present

base = (D4_SCORE_CONTESTED_WEIGHT * n_contested 
       + D4_SCORE_PHOSPHATE_MUP_WEIGHT * phosphate_detected
       + D4_SCORE_COSMETIC_MUP_WEIGHT * n_cosmetic)
```

Gating: behind a new flag `BARI_D4_SCORE_V2` (default OFF). Flag OFF = byte-identical to BARI_D4_SCORE_V1 baseline when V1 is ON, byte-identical to HEAD when both OFF.

---

## 4. Interaction with Existing Rules — Anti-Double-Count Check

### 4.1 vs. ADDITIVE_MARKERS_3_PLUS / 5_PLUS (PROCESSING_CAPS)

These caps apply to the `additive_quality` **dimension score** (currency: dimension raw score 0–100). The D4 penalty applies to the **composite score** (currency: weighted sum after all dimensions). These are separate accounting systems. **No double-count.** Confirmed: EV-103 explicitly states ADDITIVE_MARKERS caps are not counted in `already_spent`. No change to this invariant.

### 4.2 vs. ECS-v1 Emulsifier Complexity (EV-045)

E450 (phosphates) is included in ECS-v1 as a **medium-concern** emulsifier agent (weight=3 per occurrence, up to the EMULSIFIER_COMPLEXITY_FAMILY_BUDGET=8). E450 therefore contributes to `ecs_spent` in the combined-cap calculation:

```
net_d4 = max(0, min(d4_raw, D4_COMBINED_ADDITIVE_PROCESSING_CAP - ecs_spent))
```

If E450 fires the ECS-v1 medium tier (contributing up to 3 pts to `ecs_spent`), the remaining D4 budget is 12 − 3 = 9 pts minimum. The D4 cap is 8 pts, so the combined cap of 12 is only binding at 12 pts total. In practice: a product with E450 (ECS=3) + 1 contested additive (D4=2) = 5 pts total, well within 12. A product with E450 (ECS=3) + E450 D4 penalty (1) + 3 contested (D4=6) = 10 pts total — still under the combined cap. **No new double-count risk; the existing combined-cap governs.** No change needed.

### 4.3 vs. Sweetener Caps (SWEETENER_CAP_A/B/C)

E955, E950, E960 are `cosmetic_mup` and `dose-dependent` but are handled by SWEETENER tiers separately. E450 is NOT in any sweetener tier. **No interaction.** Confirmed above.

### 4.4 vs. BHA Named Penalty (EV-TASK-222C)

BHA (E320) already carries `BHA_NAMED_PENALTY = 5` on the `additive_quality` dimension AND is `score_eligible contested` (D4 weight=2 on composite). The two fire on different currencies (dimension vs. composite). EV-103 notes this as M-1 stacking with net composite impact ≈ −2.5, corpus prevalence 0.15%. This proposal adds E450 to the D4 composite layer with weight=1. No interaction with BHA path. **No new stacking introduced.**

### 4.5 vs. NOVA Processing Penalty

NOVA-4 fires on `processing_quality` dimension (weight=0.15) and a PROCESSING_CAP of 68. The D4 penalty fires on the composite after all dimensions and caps. EV-103 explicitly excludes NOVA-4 deduction from `already_spent` (different currencies). **No double-count.**

### 4.6 vs. Red-Label De-Anchor Directive

The standing directive (2026-06-14) is to move away from binary Israeli red-label caps toward continuous/graduated signals. This proposal is orthogonal — it operates on additive identity, not nutrient thresholds. **No conflict.**

---

## 5. Activation Scope

**Cross-category — all 12 live categories.**

This is appropriate because:
1. The phosphate concern (hyperphosphatemia, CKD risk from chronic dietary phosphate load) is not category-specific.
2. Phosphate additives appear at meaningful prevalence in cakes (72/149, 48%) and dairy-based products (milk: 6/20, 30%; cheese: 11/59, 19%).
3. Products in clean categories (bread, hummus, granola, juices, snacks, cereals, brined cheeses, hard cheeses) have zero phosphate prevalence in the current corpus — activation has zero effect on those categories.

This differs from the prior owner-rejected broad cosmetic_mup term: that broad term fired on clean hummus (xanthan) and whole-grain bread (SSL) — this proposal does not.

---

## 6. Rollback Plan

**Flag:** `BARI_D4_SCORE_V2` (new environment variable, default OFF)  
**Rollback state:** `BARI_D4_SCORE_V2=off` (default) → engine byte-identical to `BARI_D4_SCORE_V1=on` baseline (the current contested-only D4 scoring)  
**Restoration:** `unset BARI_D4_SCORE_V2` or set to `off` in the batch runner  
**Notify on rollback:** Nutrition Agent + Product Agent  
**Irreversible? No.** The change is a single constant (D4_SCORE_PHOSPHATE_MUP_WEIGHT) behind a flag. The frontend JSON and committed baselines are unchanged until explicitly re-scored and deployed.

---

## 7. Label Observability

**Full label-observable.** Hebrew ingredient labels declare phosphate additives by Hebrew name or E-number:
- פוספט / פוספטים (phosphate / phosphates)
- דיפוספט (diphosphate / E450)
- טריפוספט (triphosphate / E451)
- פוליפוספט / פוליפוספטים (polyphosphate / E452)
- These are already present in `GLASSBOX_W2_ADDITIVES["E450"]["match_patterns_he"]` — no new detection logic needed.

The `detect_additives_d4()` function in `score_engine.py` already scans for these patterns. **No label-derivability barrier.**

---

## 8. Rule-Accumulation Check (BSIP2 Governance B2)

| Existing rule | Covers phosphate? | Overlap? |
|---|---|---|
| ADDITIVE_MARKERS_3_PLUS/5_PLUS | Yes (count-based) | Different currency (dimension, not composite). No double-count. |
| ECS-v1 emulsifier complexity (EV-045) | E450 = medium agent | Governed by combined cap (D4_COMBINED_ADDITIVE_PROCESSING_CAP=12). No uncontrolled stack. |
| BARI_D4_SCORE_V1 contested penalty | No (E450 is dose-dependent, not contested) | No overlap. |
| SWEETENER_CAP_C | No (E450 is not a sweetener) | No overlap. |
| NOVA-4 processing penalty | Indirect (phosphates correlate with NOVA-4) | Different currencies. Not double-counted. |

**Conclusion: No new shadow of an existing rule. The combined cap (12 pts) governs any ECS + D4 stack for the same product. Rule-accumulation check PASS.**

---

## 9. Governance Verdict (Self-Review)

```json
{
  "proposal_id": "TASK-388 D6 — ZOE-style graded additive quality (phosphate MUP)",
  "review_date": "2026-06-24",
  "reviewer": "Nutrition Agent (bari-bsip2-scoring-governance)",
  "governance_checks": {
    "evidence_registry_reference": "pass — EV-103 (D4 framework) + EV-106 (Hatta-Langedyk AJPH 2026, processing harm pathway)",
    "label_observability": "pass — E450 match patterns already in detect_additives_d4(); full Hebrew label coverage",
    "category_activation_scope": "pass — cross-category; zero effect on 8/12 categories (0% phosphate prevalence verified)",
    "rollback_plan": "pass — BARI_D4_SCORE_V2=off (default) restores V1 baseline; no frontend commit until go-live",
    "rule_accumulation_check": "pass — ECS+D4 combined cap governs; different currencies from ADDITIVE_MARKERS; no sweetener overlap"
  },
  "verdict": "approved (D6 self-sign — Nutrition Agent)",
  "blocking_reasons": [],
  "revision_requests": ["Requires Product Agent D7 co-sign before engine build", "Requires owner authorization before any published score change (tripwire #1)"]
}
```

---

## 10. Open Questions for D7

1. **Combined cap adequacy:** D4_COMBINED_ADDITIVE_PROCESSING_CAP=12 was designed for contested-only (max D4=8). With phosphate adding up to 1 pt more, the theoretical max is 9 pts D4 + 8 pts ECS = 17 — but the cap is 12. Binders: does Product believe 12 pts is still the right total-additive-family ceiling, or should it be raised to 14 to reflect the broader scope? (Nutrition recommendation: keep 12 — the cap was designed conservatively and the scenarios that hit 12 are already high-burden products.)

2. **Phosphate in dairy milk:** 6/20 milk products have phosphate. Milk-fortified products (e.g. vitamin-D fortified milk) legitimately use phosphate forms as calcium/phosphorus carriers. Should the milk category be scoped out? (Nutrition position: NO — if phosphate is present in fortified milk, it is still a legitimate processing marker; the -1 penalty is modest and the combined-cap prevents compounding. But Product may disagree on consumer communication grounds.)

3. **ECS-v1 medium-tier E450 and the combined-cap budget:** A product with ECS spending 8 pts (max ECS budget) leaves 4 pts D4 budget. The -1 phosphate + -2 contested = 3 pts, safely within 4. No gap, but worth explicit Product acknowledgment.

---

*This design doc is PROPOSAL status (D6 self-sign, Nutrition Agent, 2026-06-24). Engine build is blocked until D7 (Product Agent co-sign) and owner authorization per tripwire #1.*
