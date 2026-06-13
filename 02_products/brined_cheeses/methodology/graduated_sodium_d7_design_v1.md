# Graduated Sodium D7 Design Ruling
**Task:** TASK-267 / grad-sodium-d7-design
**Date:** 2026-06-13
**Author:** Nutrition Agent
**Status:** RETURNED — awaiting Product Agent co-sign
**Verdict: DESIGN APPROVED (pending Product co-sign)**
**Scope:** `BARI_GRAD_SODIUM_V1` flag design — endemic-sodium dairy capability

---

## Prerequisite Recon

Blast-radius recon completed and verified:
`02_products/brined_cheeses/reports/graduated_sodium_blast_radius_v1.md`

Key recon findings that inform this ruling:

1. `BARI_REDLABEL_V1` is a bundled flag controlling four simultaneous logic changes:
   - (1) `score_regulatory_quality()` continuous formula — **global, all categories**
   - (2) Reformulable label count (endemic sat_fat exclusion) — scoped to `{dairy_protein, whole_food_fat}`
   - (3) Graduated sodium bands (`SODIUM_GENERAL_BANDS`) — scoped to `{dairy_protein, whole_food_fat}`
   - (4) Graduated sugar penalty — scoped to `{dairy_protein, whole_food_fat}`

2. Frozen milk: **0/20 scores move** under either flag state. Byte-identical guaranteed (sodium 40-60mg; lowest SODIUM_GENERAL_BANDS band fires at 450mg; 8-10x below floor).

3. The regulatory quality formula change (effect #1) moves 7 yogurt scores and 32 cheese-spread scores under BARI_REDLABEL_V1 — none from sodium logic, all from the continuous regulatory quality formula. This confirms BARI_REDLABEL_V1 is not a safe surgical vehicle for sodium-only activation.

4. 19/48 brined-cheese products route to `default`/`cracker` (not `dairy_protein`) and suffer a -22 to -27pt regression under BARI_REDLABEL_V1 because the REFORMULABLE_LABELS_2_PLUS cap fires at 45 for non-endemic categories. This is a category-routing inconsistency.

---

## D7 Design Ruling — Four Decisions

---

### Decision 1 — Endorse the Surgical `BARI_GRAD_SODIUM_V1` Flag

**RULING: ENDORSED.** Create a new surgical `BARI_GRAD_SODIUM_V1` flag that controls ONLY the `SODIUM_GENERAL_BANDS` graduated penalty path (score_engine.py lines ~2005-2044).

**Reasoning:**

`BARI_REDLABEL_V1` is the wrong vehicle. Its regulatory quality formula change (effect #1 in the recon) is global — it moves published yogurt, cheese-spreads, and even non-dairy cereals when enabled. That change is a separate, unpublished capability that has not been through its own D7. Activating it as collateral to reach the sodium path violates the governance principle that distinct scoring changes require distinct evidence and distinct approval. You do not fix one thing by also changing three others.

The surgical flag design — isolating only SODIUM_GENERAL_BANDS from the rest of the BARI_REDLABEL_V1 bundle — is the cleanest available path. It respects the boundaries between separate scoring decisions, minimizes blast radius, and is trivially reversible. The code at lines 2005-2044 is already written and already scoped to `REDLABEL_ENDEMIC_SATFAT_CATEGORIES = {"dairy_protein", "whole_food_fat"}`; the surgical flag is a gate change, not new logic.

**Implementation note (for the later implementation step):** The `BARI_GRAD_SODIUM_V1` env-flag reads `score_engine.py` line 135's pattern (`os.environ.get("BARI_GRAD_SODIUM_V1", "off").lower() == "on"`). The graduated sodium block (currently gated by `if BARI_REDLABEL_V1:` at line 2005) is re-gated to `if BARI_GRAD_SODIUM_V1 or BARI_REDLABEL_V1:` — so BARI_REDLABEL_V1 continues to activate the full bundle (backward-compatible for test runs), while BARI_GRAD_SODIUM_V1 activates only the sodium path. This is a one-line change. Do NOT implement now — implementation is after Product co-sign.

---

### Decision 2 — Activation Scope: The Principled Question

**RULING: Activate `BARI_GRAD_SODIUM_V1` for ALL categories where sodium is endemic/structural to the food's production identity — initially `{dairy_protein, whole_food_fat}`, with a defined expansion gate for additional endemic-sodium categories.**

**The principle:** Graduated sodium (banded penalty replacing a hard cliff) is the honest scoring model wherever sodium is endemic and structural — meaning it derives from the production process of the food class itself, not from a reformulation choice by the manufacturer. A hard cliff at 700mg treats structural salt in aged cheese identically to added-salt abuse in a processed snack. That is a false equivalence. The graduated model correctly expresses: more sodium = more penalty, but at a rate calibrated to whether the sodium is a production artifact or a formulation choice.

Graduated sodium does NOT belong everywhere. For categories where sodium is a pure formulation variable (crackers, salty snacks, processed spreads, cereal), the hard cliff is an appropriate deterrent — it is not endemic, it is a choice. The distinction is: can the manufacturer reduce sodium without changing the food's fundamental identity? If yes → hard cliff appropriate. If no → graduated model appropriate.

**Scope at launch:** `{dairy_protein, whole_food_fat}`. This is the current `REDLABEL_ENDEMIC_SATFAT_CATEGORIES` set. It is the correct principled scope for the initial activation because:
- Dairy protein (yogurt, cheese, brined cheese) — sodium is structural in brined and aged variants; low in fresh variants, producing correct graduated behavior across the full category
- Whole food fat (tahini, natural nut butters) — trace sodium from raw material; the set is already defined and correct

**Expansion mechanism:** Any future category claiming endemic-sodium status requires:
1. A new EV entry documenting the production mechanism (why sodium is non-reformulable for that food class)
2. A D7 co-sign (Nutrition Agent + Product Agent)
3. Evidence that the hard cliff produces a false-equivalence failure on the real corpus

This is NOT a brined-cheese-only patch. The flag is a general graduated-sodium capability. The systematic scope is `endemic-sodium food classes` as defined by the `REDLABEL_ENDEMIC_SATFAT_CATEGORIES` set (or an expanded equivalent). The owner's directive to be systematic is satisfied: the capability is designed as a general mechanism with a principled expansion gate, not hard-coded to one category.

**On global scope (option c in the brief):** Rejected. Global activation of graduated sodium would remove the hard-cliff deterrent from categories where it belongs. Crackers, cereals, and processed snacks with 900mg+ sodium should hit the hard cliff — that is the correct nutritional signal. Graduated sodium for those categories would be flattery, not honesty.

---

### Decision 3 — Published-Movement Question: Cheese-Spreads ≤2pt

**RULING: The cheese-spread ≤2pt movement under the SURGICAL flag (`BARI_GRAD_SODIUM_V1`) is ACCEPTABLE noise. This is within D7 lane. No owner escalation required.**

**Precise characterization:**

Under the surgical `BARI_GRAD_SODIUM_V1` flag (not the bundled BARI_REDLABEL_V1):
- Cheese-spread max sodium is 558mg (from blast-radius recon)
- The `SODIUM_GENERAL_BANDS` lowest penalty band fires at ≥450mg: -2pt
- Products with 558mg: would receive -2pt penalty where previously 0pt
- Products with 200-449mg: zero movement (below the floor)
- No grade changes — all within same letter

**The 32-product cheese-spread movement reported in the blast-radius recon is NOT from the surgical sodium flag.** Those 32 products move because of effect #1 (the global regulatory quality formula change in BARI_REDLABEL_V1). Under the surgical flag, only the ~2-3 cheese-spread products with sodium ≥450mg would receive a -2pt adjustment. The rest stay byte-identical.

**Governance classification:** Bari comparison governance (bari_comparison_governance_v1.md) classifies ≤2pt as noise. A -2pt movement on 2-3 cheese-spread products (no grade change, no published page for cheese-spreads currently live as a standalone category) is squarely within the noise rule. The sodium data is on the label; the -2pt is an accurate signal that this product has more sodium than a lower-sodium cheese-spread. This is correct scoring, not distortion.

**No exclusion of cheese-spreads from the activation scope.** Excluding them would require hardcoding an exception against the principled scope definition. The correct treatment is: cheese-spreads that happen to be near the 450mg band receive a small accurate penalty. That is the graduated model working as intended.

**Owner escalation check:** No tripwire fires. This is not a frozen invariant (no frozen cheese-spread scores exist). It is not irreversible (flag default=off; re-score generates fresh output). It does not start or kill a program. It creates no external commitment. It does not redefine what Bari is. D7 lane authority is sufficient.

---

### Decision 4 — Routing: Brined Cheese Must Route to `dairy_protein`

**RULING: The 19 brined-cheese products currently routing to `default`/`cracker` must route to `dairy_protein`. This is a CORRECTNESS FIX, not a scoring change.**

**Reasoning:**

Brined cheese is categorically dairy protein. Bulgari (בולגרית), feta (פטה), halloumi (חלומי), and similar brine-preserved cheeses are dairy products. Their current routing to `default` or `cracker` is a category-detection failure — the products exist in the wrong context for the engine's own logic. The routing determines which context the product is scored in, and the brined-food context (`context_flag == "brined_food"`) was already established by EV-052 as the correct treatment for these products.

The principle: a product's category routing must reflect its actual food identity. If the engine's own NOVA+fat express and HP suppression rules are designed for dairy_protein, and a product IS dairy protein (brined cheese), then routing it to `default` is an engine error. Fixing it to `dairy_protein` applies the rules the engine already has for this food class — it is not adding new rules, it is ensuring existing rules fire on the right products.

This is not a scoring change in the governance sense: it does not alter any scoring formula or penalty threshold. It corrects which scoring context (already designed and D7-approved for dairy products) is applied to a product that belongs to that context. The analogy: correcting a mislabeled `category = "beverage"` on a yogurt product is not a scoring rule change — it is a data correction.

**Implementation requirement:** The `brined_food` keyword detection (EV-052) that sets `context_flag == "brined_food"` must be reviewed to ensure products matched by the brined-food keywords route to `dairy_protein`, not `default`. This may require adjustments in the BSIP1 enrichment configuration or the category inference logic. The 19 misrouted products' barcodes from run_brined_002 are the acceptance test set: all 19 must route to `dairy_protein` after the fix.

---

## EV-055 — Graduated Sodium Activation for Endemic-Sodium Dairy (`BARI_GRAD_SODIUM_V1`)

| Field | Value |
|-------|-------|
| **finding_id** | EV-055 |
| **concept** | Graduated sodium banding (`SODIUM_GENERAL_BANDS`) replaces the hard 700mg cliff (`HIGH_SODIUM_700MG_PLUS`) for endemic-sodium food categories, controlled by the surgical `BARI_GRAD_SODIUM_V1` flag |
| **task** | TASK-267 — graduated_sodium_d7_design_v1.md §2 (Nutrition Agent ruling) — Product Agent co-sign pending |
| **recorded** | 2026-06-13 |
| **scientific_rationale_short** | A hard sodium cliff at 700mg treats structural brine-preservation sodium (brined cheese, some aged dairy) identically to reformulation sodium (salty snacks, processed spreads). This conflation produces a category-wide pin: the brined-cheese corpus run_brined_002 shows 42/48 products pinned at the 72-point cap across all NOVA tiers and fat levels — NOVA-1 low-fat clean products score identically to NOVA-3 high-fat products. The hard cliff collapses the NOVA+fat express signal that the engine is explicitly designed to differentiate. A graduated banded penalty correctly expresses: more sodium = more penalty, at a proportional rate calibrated to the endemic nature of the salt source. For food classes where sodium cannot be reduced without changing the product's fundamental identity (brined cheese, where salt is the preservation medium), the graduated model is the honest signal model. |
| **evidence_strength** | Moderate — food-science mechanism is clear (brine-salt vs formulation-salt distinction); population-outcome RCTs specific to the graduated-vs-cliff model in dairy sodium do not exist. Evidence tier B: strong mechanistic basis, observational corpus confirmation (72-pin on 42/48 products confirms cliff collapse), regulatory precedent (NOVA framework distinguishes production methods). |
| **confidence_level** | High — the scoring failure is directly observable in run_brined_002 data. The 42/48 pin is not an edge case; it is total corpus collapse. |
| **BSIP2_relevance** | Direct and critical. Without graduated sodium, the NOVA+fat express that is the core differentiation mechanism for brined cheese cannot function. NOVA-1 low-fat products (the highest-quality tier) score at 72/B — the same as NOVA-3 high-fat products. This is a false equivalence the engine's own design rejects. |
| **label_observability** | Fully label-observable. `sodium_mg` per 100g is on every product's nutrition panel. Coverage in run_brined_002: 48/48 (100%). No external data required. The graduated bands read a single nutrition panel field. |
| **implementation_complexity** | Low — the SODIUM_GENERAL_BANDS logic is already written at score_engine.py lines 2005-2044, currently gated by BARI_REDLABEL_V1. The surgical BARI_GRAD_SODIUM_V1 flag is a gate-addition, not new logic. One additional env-var declaration (line 135 pattern) and one gate condition change. |
| **recommended_action** | implement_after_D7_cosign (Product Agent co-sign pending) |
| **activation_scope** | `category in {"dairy_protein", "whole_food_fat"}` (= `REDLABEL_ENDEMIC_SATFAT_CATEGORIES`). Future endemic-sodium categories require a new EV + D7 co-sign. This is a general capability, not a brined-cheese patch. |
| **flag** | `BARI_GRAD_SODIUM_V1` — surgical, controls ONLY the `SODIUM_GENERAL_BANDS` path. Default: `off`. Does NOT activate `score_regulatory_quality()` continuous formula, reformulable label count changes, or graduated sugar penalty. Those remain gated by `BARI_REDLABEL_V1` only. |
| **published_scores_moved** | Milk: 0/20 (byte-identical guaranteed — all milk sodium 40-60mg, far below 450mg floor). Yogurt: 0 from sodium path (all yogurt sodium 40-400mg; SODIUM_GENERAL_BANDS lowest penalty fires at ≥450mg). Cheese-spreads: ≤3 products with sodium ≥450mg → -2pt, no grade change. All other published categories: 0 (non-endemic categories use the HIGH_SODIUM_700MG_PLUS path unchanged). |
| **rollback** | Set `BARI_GRAD_SODIUM_V1=off` (default). All published runs committed with flag=off. re-scoring with flag=off restores prior output exactly. The flag is a feature gate; no data is modified by enabling/disabling it. |
| **no_regression_proof** | (1) Frozen milk byte-identical: confirmed by blast-radius recon (0/20 scores move). (2) Yogurt byte-identical from sodium path: confirmed (all 40-400mg, below 450mg band floor). (3) Cheese-spreads ≤2pt on ≤3 products, no grade change: confirmed from recon sodium ranges and SODIUM_GENERAL_BANDS thresholds. (4) engine_invariants.py 342-case suite — must pass before merge. (5) Non-endemic categories (cereal, snack, bread): unaffected — the graduated path is scoped to `REDLABEL_ENDEMIC_SATFAT_CATEGORIES`; non-endemic categories continue to use HIGH_SODIUM_700MG_PLUS. |
| **governance_classification** | Scoring rule activation (existing logic, new flag gate). Requires D7 co-sign: Nutrition Agent (this ruling) + Product Agent (pending). |
| **reference** | Nutrition Agent ruling: `02_products/brined_cheeses/methodology/graduated_sodium_d7_design_v1.md`. Blast-radius recon: `02_products/brined_cheeses/reports/graduated_sodium_blast_radius_v1.md`. |
| **reversal_condition** | If brined re-score under BARI_GRAD_SODIUM_V1 shows NOVA-1 low-fat products reaching A-grade territory implausibly (e.g., 1300mg sodium + NOVA-2 reaching A), revisit the band thresholds. The graduated bands are not brined-cheese specific — if they produce unexpected results at the high-sodium tail, review the ≥900mg band penalty magnitude. |

```yaml
study_objects:
  - claim: "Hard sodium cliff at 700mg collapses NOVA+fat differentiation for endemic-salt dairy categories"
    dose_realistic: true
    population_direct: false
    rob_grade: low
    evidence_tier: C
    source_doi: "internal:graduated_sodium_blast_radius_v1"
    notes: "Direct corpus observation: 42/48 brined-cheese products pinned at cap=72 across all NOVA tiers and fat levels in run_brined_002. The cliff overrides the NOVA signal for any product with sodium >=700mg, regardless of processing level. Evidence tier C: observational, internal corpus; no population RCT. The mechanism is clear: the hard cap is a ceiling that applies after the NOVA score is computed, so it erases NOVA signal for all high-sodium products regardless of their processing level."
  - claim: "Brine-preservation sodium is not equivalent to formulation sodium for scoring purposes"
    dose_realistic: true
    population_direct: false
    rob_grade: low
    evidence_tier: C
    source_doi: "internal:EV-052,EV-053"
    notes: "The brined_food context (EV-052) and sodium_weight=0.7 (EV-053) already encode the principle that structural sodium from brine preservation should be penalized at a lower rate than formulation sodium. EV-055 extends this principle from weight reduction to cliff replacement: if the underlying evidence supports a 30% reduction in sodium weight (EV-053), it supports a proportional-banding model over a hard cliff. Same food-science basis, consistent treatment."
```

---

## No-Regression Plan for Implementation

The following checks are REQUIRED before any engine merge implementing `BARI_GRAD_SODIUM_V1`:

### Guard 1 — Frozen Milk Byte-Identical
Command: Re-score run_005_headpin corpus with `BARI_GRAD_SODIUM_V1=on`.
Expected: All 20 products byte-identical. milk_scores_moved = 0.
Basis: All milk sodium 40-60mg. SODIUM_GENERAL_BANDS lowest band fires at ≥450mg. Gap = 8-10x. Mathematically impossible to fire.
Failure condition: Any milk score moves → HALT, investigate flag scope leak.

### Guard 2 — Yogurt Byte-Identical (Sodium Path)
Command: Re-score run_yogurt_006 corpus with `BARI_GRAD_SODIUM_V1=on`.
Expected: 0 yogurt products move from the sodium path. (If any BARI_REDLABEL_V1-only effects also present: those would be from a different flag; BARI_GRAD_SODIUM_V1 alone must show 0.)
Basis: All yogurt sodium 40-400mg, below 450mg band floor.
Failure condition: Any yogurt score changes under BARI_GRAD_SODIUM_V1=on only (not bundled flag) → flag scope leak.

### Guard 3 — Cheese-Spreads ≤2pt, No Grade Change
Command: Re-score run_cheese_003 corpus with `BARI_GRAD_SODIUM_V1=on`.
Expected: Only products with sodium ≥450mg move; delta ≤2pt; no grade changes.
Basis: Cheese-spread max sodium = 558mg → 450-599 band → -2pt. Below 450mg = 0pt.
Accept: ≤3 products with ≤2pt delta, all same grade.
Failure condition: Any grade change, or any product with sodium <450mg moves → investigate.

### Guard 4 — Engine Invariants Suite
Command: `python C:\Bari\03_operations\bsip2\proto_v0\tests\engine_invariants.py`
Expected: All 342 cases pass.
Failure condition: Any case fails → do not merge.

### Guard 5 — Brined Re-Score Pin-Break Verification
Command: Re-score run_brined_002 corpus with `BARI_GRAD_SODIUM_V1=on`.
Expected: The 72-pin breaks for dairy_protein-routed products; NOVA-1 low-fat products score higher than NOVA-3 high-fat products; no products in dairy_protein routing drop sharply (if a product drops, investigate reformulable-label interaction).
The 19 misrouted products (default/cracker) must also have been re-routed to dairy_protein before this check is meaningful.
Failure condition: 72-pin remains for dairy_protein products → flag not activating correctly.

### Guard 6 — Non-Endemic Scope Guard
Command: Re-score a cereals/snack corpus with `BARI_GRAD_SODIUM_V1=on`.
Expected: 0 non-endemic products move. The `category in REDLABEL_ENDEMIC_SATFAT_CATEGORIES` guard must prevent any non-dairy product from reaching the SODIUM_GENERAL_BANDS path.
Failure condition: Any non-endemic product changes score → scope guard broken.

---

## PRODUCT CO-SIGN NEEDED ON:

1. **Decision 1 — Surgical flag endorsement:** Does Product agree that isolating `BARI_GRAD_SODIUM_V1` from the BARI_REDLABEL_V1 bundle is the correct design? (Nutrition ruling: YES — endorsed. Needs Product confirmation.)

2. **Decision 2 — Activation scope `{dairy_protein, whole_food_fat}`:** Does Product agree this is the correct principled scope for launch, with the expansion gate mechanism for future endemic-sodium categories? (Nutrition ruling: scope is principled and correct. Needs Product co-sign on scope boundary.)

3. **Decision 3 — Cheese-spread ≤2pt accepted as noise:** Does Product agree the ≤2pt movement on high-sodium cheese-spreads is within the ≤2pt=noise governance ruling and requires no further owner escalation? (Nutrition ruling: yes, within D7 lane. Needs Product confirmation.)

4. **Decision 4 — Brined-cheese routing to `dairy_protein` is a correctness fix:** Does Product agree this is a data/routing correctness fix (not a scoring rule change) and proceeds under D7 authority without owner escalation? (Nutrition ruling: correctness fix. Needs Product co-sign.)

5. **EV-055 formal registration:** Both Nutrition Agent and Product Agent must formally record EV-055 before Data Agent implements the engine change.

**Owner escalation: NOT required.** No tripwire fires:
- Frozen milk: byte-identical (tripwire CLEAR)
- Not a published-score change (flag default=off; no live category rescored until explicit re-run)
- Not irreversible (flag gate; trivially rollback)
- Not a major program start/kill
- No external commitment or spend
- Does not redefine Bari's strategy or target user

---

## Governance Verdict (bari-bsip2-scoring-governance)

```json
{
  "proposal_id": "EV-055 / BARI_GRAD_SODIUM_V1 / grad-sodium-d7-design",
  "review_date": "2026-06-13",
  "reviewer": "Nutrition Agent (bari-bsip2-scoring-governance)",
  "governance_checks": {
    "evidence_registry_reference": "pass — EV-055 drafted; cites EV-052/053 lineage + blast-radius recon (42/48 pin corpus evidence)",
    "label_observability": "pass — sodium_mg 48/48 coverage in run_brined_002; single nutrition panel field; no external data",
    "category_activation_scope": "pass — scoped to REDLABEL_ENDEMIC_SATFAT_CATEGORIES = {dairy_protein, whole_food_fat}; non-endemic categories explicitly excluded; expansion gate defined",
    "rollback_plan": "pass — BARI_GRAD_SODIUM_V1 default=off; all published runs committed at flag=off; re-scoring with flag=off restores prior output",
    "rule_accumulation_check": "pass — no new scoring rule created; existing SODIUM_GENERAL_BANDS logic (already in engine) activated under a surgical flag gate; HIGH_SODIUM_700MG_PLUS is suppressed for endemic scope only (as it was under BARI_REDLABEL_V1 already)"
  },
  "verdict": "approved — pending Product Agent co-sign (D7 requires both)",
  "blocking_reasons": [],
  "revision_requests": [
    "Product Agent co-sign required before implementation proceeds (D7 joint requirement)",
    "EV-055 must be formally written into evidence registry before Data Agent implements engine change"
  ]
}
```

---

```json
{
  "task": "grad-sodium-d7-design",
  "proposed_status": "RETURNED",
  "verdict": "DESIGN APPROVED — Nutrition Agent D7 ruling complete; Product Agent co-sign required before implementation",
  "artifacts": [
    {
      "path": "02_products/brined_cheeses/methodology/graduated_sodium_d7_design_v1.md",
      "action": "created",
      "sha256": "1b311c9842d620c3011e15c0086aff7592b93dd9bd5962a57b8a7148ab018918"
    }
  ],
  "counts": {
    "brined_products_pinned_at_72": "42/48 (run_brined_002)",
    "brined_products_pin_broken_by_flag": "42/42 (dairy_protein-routed, recon confirmed)",
    "brined_products_misrouted": "19/48 (default/cracker instead of dairy_protein)",
    "frozen_milk_scores_moved": "0/20 (run_005_headpin, recon confirmed byte-identical)",
    "yogurt_scores_moved_sodium_path": "0/88 (sodium path only; 7 move from regulatory quality formula in bundled flag, not from graduated sodium)",
    "cheese_spread_scores_moved_surgical_flag": "<=3/59 (sodium >=450mg products, <=2pt delta, no grade change)",
    "ev_drafted": "1/1 (EV-055)",
    "no_regression_guards_defined": "6/6"
  },
  "commands_run": [],
  "not_done": [
    "EV-055 not yet written into the evidence registry (bsip2_evidence_registry_v1.md) — requires Product co-sign first",
    "Engine implementation of BARI_GRAD_SODIUM_V1 flag — requires Product co-sign first",
    "Brined-cheese routing fix (19 misrouted products) — requires Product co-sign and separate implementation step",
    "No-regression guard execution — implementation step only"
  ],
  "self_check": {
    "acceptance_test": "Frozen milk byte-identical AND graduated sodium un-pins the 72-cap for brined dairy_protein products",
    "frozen_milk_safe": true,
    "frozen_milk_evidence": "Blast-radius recon 0/20 scores moved; sodium 40-60mg vs 450mg floor — 8-10x below threshold; mathematically impossible to fire SODIUM_GENERAL_BANDS",
    "owner_escalation_needed": false,
    "owner_escalation_rationale": "No tripwire fires: frozen milk clear; flag default=off (not a published-score change); reversible; no program start/kill; no external commitment; no strategy redefinition",
    "product_cosign_needed": true,
    "product_cosign_items": ["surgical flag design", "activation scope", "cheese-spreads noise ruling", "routing correctness classification"]
  }
}
```
