# Brined Cheese Cap-45 Ruling v1

**Task:** brined-cheese-cap45-ruling
**Date:** 2026-06-13
**Author:** Nutrition Agent
**Status:** RETURNED — proposed fix requires D7 + Product Agent co-sign before implementation
**Verdict:** OVER_PENALTY
**Depends on:** run_brined_001 traces, score_engine.py, evaluation_scope.py, EV-052

---

## 1. The Governing Question

Does the `ISRAELI_RED_LABELS_2_PLUS` cap at 45 produce an honest score for full-fat
brined cheeses that carry both a saturated-fat red label and a sodium red label? Or does
it double-count, treating brine-preservation sodium as a compounding harm signal on par
with a reformulated junk-food stack?

---

## 2. What the Trace Shows

Product: **קוביות בולגרית מעודנת 13%** (barcode 7290108509106)

- Ingredients: חלב מפוסטר, מלח, תרבית לקטית מקריש (3 items)
- NOVA: 1 (high confidence, 0.85)
- structural_class: A "Intact Whole Food" (confidence 0.67)
- weighted_dimension_score: **87.7**
- `brined_food` flag: fired (context_flag = "brined_food")
- `HIGH_SODIUM_700MG_PLUS` cap: correctly raised to 72 (sodium_weight=0.7 working)
- `ISRAELI_RED_LABELS_2_PLUS` cap: fired at **45**, binding, overrides the 72 cap
- `HP_FAT_SODIUM_COMBO` penalty: 6 points also fired
- **Final score: 39/D**

A product with milk, salt, and a starter culture — structurally classified as "Intact
Whole Food" with 87.7 raw score — is assigned the same grade band as a NOVA-4
ultra-processed product, because two red labels co-occur.

The 10 NOVA-1 products stuck at D in this run all have this same trace structure. The
distribution (28/48 at D, median 39) is not a spread of nutritional quality — it is a
floor produced by a single cap firing on structural grounds that are not compositionally
honest for this food class.

---

## 3. The Case for HONEST

The strongest argument for leaving the cap unchanged:

A 13%-fat brined Bulgarian cheese does carry a genuine saturated-fat load. 8.5g/100g
sat-fat is above the 5g/100g red-label threshold, not trivially. The sodium at 720mg
is also real. These are not trace amounts that triggered thresholds by rounding.

The `ISRAELI_RED_LABELS_2_PLUS` cap was designed for exactly the scenario where a
product fails on two separate nutritional axes — a product that is simultaneously
calorie-dense, high-sugar AND high-sat-fat, or high-fat AND high-sodium from
reformulation choices. In that scenario, the compounding is honest: the product is
genuinely worse than a single-axis failure.

If this were a 13%-fat spreadable processed cheese triangle (גבינה מעובדת) with
emulsifiers, added salt, and cream — the same sat-fat + sodium combination from
processed inputs — a D at 39 would be correct.

**But the problem is that it is not.** The sodium in this product is not a reformulation
choice. It is brine. We already acknowledged this in the methodology brief and in EV-052
— that is why the `brined_food` flag was designed and wired. The 0.7 weight correctly
softens the `HIGH_SODIUM_700MG_PLUS` cap from 60 to 72. The architecture already
recognizes brine sodium as structurally distinct.

---

## 4. The Case for OVER_PENALTY (the true finding)

The 0.7 weight is logically inconsistent if the sodium red label continues to count
toward the 2-label cap unchanged. Here is why.

**The engine holds two contradictory positions simultaneously:**
- Position 1 (sodium weight): "This sodium is brine-structural; it should be penalized
  at 70% of normal weight." → HIGH_SODIUM_700MG_PLUS rises from 60 to 72.
- Position 2 (red-label count): "The sodium red label counts equally toward ISRAELI_RED_
  LABELS_2_PLUS." → The cap fires at 45, binding over the 72.

These positions are irreconcilable. If the engine genuinely believes the sodium is
structural (Position 1), then counting that same sodium red label at full weight in the
2-label cap (Position 2) is double-accounting. The context-limited acknowledgment
("Sodium reflects preservation brine. Not all sodium in the per-100g figure is consumed;
brine is typically not eaten.") is rendered meaningless if the compounding cap fires at
full strength regardless.

**The mirror of the "never manufacture collapse" rule:**

The butter memory rule (owner ruling, standing) says: genuine score clustering is a
valid finding; never add signals to manufacture differentiation that doesn't exist. The
exact inverse applies here. When a structural fact about the food class removes the
justification for full-weight compounding, the engine must not maintain collapse that
does not reflect honest nutritional architecture. The 39/D for milk+salt+cultures is
not an honest finding — it is a mechanical artifact of the 2-label cap treating brine
sodium identically to reformulation sodium, after the engine has already explicitly
decided that brine sodium is different.

**NOVA collapse in the full-fat tier is the consequence:**

The methodology brief (§4, PRIMARY differentiator) stated NOVA would be the primary
quality axis for this category. In the full-fat tier, it is completely suppressed. A
clean NOVA-1 13%-fat Bulgarian (score 39/D) is identical to a NOVA-3 stabilizer-laden
13%-fat product carrying the same red labels. The engine cannot distinguish them
because both are capped at 45. NOVA only expresses in the low-fat tier (≤5%) where
the sat-fat red label does not fire. This is a category-wide methodology failure in
the segment that contains most of the shelf.

**The DISTORTION-010 disclosure does not fix this:**

DISTORTION-010 (sodium endemic) is a disclosure mechanism — it adds a consumer note
explaining the sodium context. It does not change the score. Using the disclosure to
justify leaving the score at 39/D would mean that every clean NOVA-1 brined cheese on
the Israeli shelf would display "D" with a footnote saying "but actually the sodium is
structural." That is not what the disclosure is for. The disclosure is for honest
borderline scores where the category-wide limitation is worth naming. It is not a
mechanism to explain away scores that are architecturally wrong.

---

## 5. Ruling

**OVER_PENALTY.**

The `ISRAELI_RED_LABELS_2_PLUS` cap at 45 is an over-penalty for products that carry
a `brined_food` context flag. The sodium red label in brined-cheese products does not
count as a compounding harm signal on equal terms with a reformulation-sodium label.
The engine has already formally recognized this distinction via the 0.7 sodium weight;
failing to carry that recognition through to the 2-label cap creates a logical
contradiction inside the same scoring pass.

The correct treatment is the minimum-scope fix described in Section 6.

---

## 6. The Fix Specification (PROPOSED — requires D7 + Product Agent co-sign)

### 6.1 What to change

**Scope:** brined_food context flag ONLY. No other category or context is affected.

**Rule:** When `context_flag == "brined_food"`, the sodium red label does NOT count
toward `ISRAELI_RED_LABELS_2_PLUS`. The sat-fat red label continues to count.

**Engine location:** `score_engine.py`, the block that computes `red_label_count` for
the `ISRAELI_RED_LABELS_2_PLUS` cap check (line 1813 area). The modification:

```python
# EV-053 / TASK-266: brined_food context — sodium red label is brine-structural,
# not reformulation excess. Exclude it from the 2-label cap count when the
# brined_food flag is active. The sat-fat label continues to count unchanged.
_rl_count_for_2plus = red_label_count
if context_flag == "brined_food":
    _sodium_in_labels = "sodium" in (l3.get("red_labels") or [])
    if _sodium_in_labels:
        _rl_count_for_2plus = max(0, red_label_count - 1)

check_cap("ISRAELI_RED_LABELS_2_PLUS", _rl_count_for_2plus >= 2, 45, sugar_caps_fired)
```

This is the MINIMAL change. It does not touch the `HIGH_SODIUM_700MG_PLUS` cap (already
softened via 0.7 weight). It does not change the sat-fat cap behavior. It only prevents
the sodium label from activating the 2-label compound cap in the brined-food context.

### 6.2 Why not zero out sodium entirely

Zeroing sodium from the cap would be over-relief. The sodium in brined cheese is real —
a 720mg product genuinely has more sodium than a 400mg product, and that difference
matters. The 0.7 weight already attenuates the standalone sodium cap. The fix here is
specifically about the compounding mechanism: removing the sodium label from the
multi-label count, while leaving the standalone sodium cap active.

### 6.3 HP_FAT_SODIUM_COMBO (separate from this ruling, same context)

The trace also shows `HP_FAT_SODIUM_COMBO` firing (6 points), dropping the product
from 45 to 39. This is a separate over-penalty: structural dairy fat + brine sodium is
not a hyper-palatability stack. The methodology brief (§4.6) already identified this
and deferred it as requiring D7. This ruling does not address HP_FAT_SODIUM_COMBO — it
is a separate EV entry and a separate D7 scope. It is flagged here for completeness and
should be handled in the same D7 batch.

### 6.4 Predicted new distribution

Assumptions for the projection (not a re-run — analytical):

Products currently at D/cap-45 due to `ISRAELI_RED_LABELS_2_PLUS`:
- 28 products. Of those, most carry both sat-fat and sodium red labels.
- After fix: products where sat-fat red label fires but sodium label no longer counts:
  `_rl_count_for_2plus` drops from 2 to 1. `ISRAELI_RED_LABELS_2_PLUS` no longer fires.
  Binding cap reverts to `HIGH_SODIUM_700MG_PLUS` (72) or `ISRAELI_RED_LABEL_1_SAT_FAT`
  (55, RECAL_P0 path → graded penalty). For a 13%-fat product: sat-fat is at 8.5g;
  the R5 graded penalty applies but does not cap — it reduces the fat_quality dimension
  score. Net score for a clean NOVA-1 13%-fat product: approximately 55–68/C (below the
  B-band, but not D). For a 16%+ fat product with higher sat-fat: approximately 50–58/C.
- Products in the D-cluster that also have NOVA-3 or additives: they lose the 2-label
  cap but retain NOVA processing caps and additive penalties. They remain lower than
  clean products.
- Products in the low-fat tier (5%) without a sat-fat red label: unaffected (they were
  already not hitting the 2-label cap; they stay in B/C as before).

Approximate post-fix distribution (analytical estimate):
- A: 2 (unchanged — clean low-fat NOVA-1, scores above 80)
- B: 15–18 (NOVA-1 moderate-fat products now allowed to reach 60–75 range)
- C: 20–25 (high-fat clean products at 50–60; processed mid-fat products in the same range)
- D: 3–6 (products with genuine triple-failures: NOVA-3 + additives + high-sodium; or
  products from non-dairy-protein category routing that have additional penalties)

NOVA now expresses across the shelf: a clean NOVA-1 16%-fat Bulgarian at ~62/C sits
clearly above a NOVA-3 stabilizer-laden 16%-fat product at ~48/C or ~54/C. The primary
differentiator in the methodology brief (§4) becomes operative.

---

## 7. Evidence Registry Requirement

**This ruling proposes EV-053.** It must be created before D7 can be completed.

**EV-053 draft:**

| Field | Value |
|---|---|
| **finding_id** | EV-053 (to be assigned) |
| **concept** | In brined-food context, the MoH sodium red label does not constitute a reformulation-based compounding harm signal. Brine-preservation sodium is structurally fixed by production method, not a formulation choice. Counting it toward `ISRAELI_RED_LABELS_2_PLUS` contradicts the existing `brined_food` 0.7 weight and produces logical contradiction within a single scoring pass. |
| **task** | TASK-266 + brined-cheese-cap45-ruling |
| **recorded** | 2026-06-13 |
| **scientific_rationale_short** | The `ISRAELI_RED_LABELS_2_PLUS` cap was designed for compounding reformulation choices: a product simultaneously engineered for multiple macronutrient excesses. Brine sodium is not a reformulation choice. The existing EV-052 / 0.7 weight recognizes this at the standalone sodium cap level. Failing to carry the recognition through to the 2-label cap produces internal inconsistency: the engine simultaneously says "this sodium is 70% as penalizable" and "this sodium label is 100% as harmful in compound." The fix removes the inconsistency by scoping the 2-label cap count to exclude brine sodium in the brined_food context. |
| **evidence_strength** | Moderate-Strong — same basis as EV-052 (food-science mechanism; brine production is well-established; no RCT specifically on compound-label scoring in brined foods) |
| **confidence_level** | High (logical consistency argument; food-science mechanism) |
| **BSIP2_relevance** | Direct — without this fix, the brined-cheese category cannot be launched. The run_brined_001 distribution (58% D, NOVA fully collapsed in full-fat tier) is the observable consequence. |
| **implementation_complexity** | Low — 5-line change in score_engine.py |
| **recommended_action** | implement_after_D7_cosign |
| **activation_scope** | brined_food context flag ONLY. Zero effect on any other context or category. |
| **published_scores_moved** | 0 — brined-cheese category not yet live. |
| **rollback** | Revert the 5-line conditional at the `ISRAELI_RED_LABELS_2_PLUS` check point. The change is flagged with `# EV-053` for easy location. |
| **no_regression_proof** | Requires: (a) engine_invariants.py 342-case suite passes unchanged; (b) dedicated brined_food regression test confirming non-brined dairy products (cottage, yogurt, white cheese) are byte-identical before/after; (c) published categories (milk, yogurt, bread, cereals, granola, snack bars, cheese spreads) produce zero score change — must be verified by running their golden corpora against the patched engine. |
| **governance_classification** | New scoring rule (conditional exclusion of a red-label signal from a multi-label cap). Requires D7 co-sign: Nutrition Agent + Product Agent. |

---

## 8. HP_FAT_SODIUM_COMBO — Separate Flag

The `HP_FAT_SODIUM_COMBO` penalty fires on top of the cap in the trace above (6 points),
producing the final 39 rather than 45. Even after the cap-45 fix, this penalty will
continue to fire for full-fat brined cheeses and will drag their scores down from the
~55–68 range into the ~49–62 range.

The methodology brief (§4.6) already proposed suppressing this penalty when
`context_flag == "brined_food"`. That suppression is NOT part of this ruling. It requires
its own EV entry (EV-054 or adjacent numbering) and its own D7 co-sign. It should be
handled in the same D7 session as EV-053, to avoid a second re-run after a partial fix.

**Flag for orchestrator:** Route both EV-053 (cap-45 fix) and the HP_FAT_SODIUM_COMBO
suppression (methodology brief §4.6) to D7 as a batch. They are independent rules but
affect the same products; running them together prevents a re-run cycle.

---

## 9. Secondary Flag — Vocabulary Gap (barcode 3075805)

Barcode 3075805 shows `category: cracker`, `nova: 1`, `context_flag: null`. The product
is described in the task brief as "גבינת ... מלוחה" which didn't match "גבינה מלוחה"
because the noun-adjective order differs ("גבינת" construct form vs "גבינה" absolute form)
or there is an intervening word.

This is a vocabulary gap in `evaluation_scope.py`. The current keyword list uses the
absolute form "גבינה מלוחה" but Hebrew product names often use the construct form
"גבינת ____" (as in "גבינת עזים מלוחה"). A future EV entry should add construct-form
variants:

```
"גבינת מלוחה", "גבינת עזים", "גבינת כבשים", "גבינת צאן"
```

This is a vocabulary item, NOT a scoring rule change, and does not require D7. It
requires a simple EV vocabulary addendum and a regression test. Not addressed in this
ruling — flagged for a future sprint.

---

## 10. Governance Verdict

```json
{
  "proposal_id": "brined-cheese-cap45-ruling",
  "review_date": "2026-06-13",
  "reviewer": "Nutrition Agent (bari-bsip2-scoring-governance)",
  "verdict": "OVER_PENALTY — fix required before category launch",
  "governance_checks": {
    "evidence_registry_reference": "missing — EV-053 draft in this document; must be formally registered before D7",
    "label_observability": "pass — red_labels field is L3-computed from label-observable nutrition values; brined_food context_flag is name+nutrition-observable",
    "category_activation_scope": "pass — fix explicitly scoped to brined_food context flag; zero cross-category effect",
    "rollback_plan": "pass — 5-line conditional; revert at tagged EV-053 comment; no published scores affected",
    "rule_accumulation_check": "pass — this modifies an existing rule (ISRAELI_RED_LABELS_2_PLUS) behavior via a context-conditional; it does not add a new cap; no shadow rule created"
  },
  "blocking_reasons": [
    "EV-053 must be registered before D7 co-sign",
    "D7 requires Product Agent co-sign",
    "HP_FAT_SODIUM_COMBO suppression is a separate required fix — route to D7 in same batch"
  ],
  "required_before_implementation": [
    "EV-053 formally registered in evidence_registry_v1.md",
    "D7 co-sign: Nutrition Agent (this document) + Product Agent",
    "engine_invariants.py 342-case suite: zero regression",
    "Published-category golden-corpus check: milk, yogurt, bread, cereals, granola, snack bars, cheese spreads — all byte-identical",
    "HP_FAT_SODIUM_COMBO suppression EV drafted and batched into same D7"
  ]
}
```

---

```json
{
  "return_contract": "v1",
  "task_id": "brined-cheese-cap45-ruling",
  "proposed_status": "RETURNED",
  "verdict": "OVER_PENALTY",
  "artifacts": [
    {
      "path": "C:\\Bari\\02_products\\brined_cheeses\\methodology\\brined_cheeses_cap45_ruling_v1.md",
      "action": "written",
      "sha256": "pending"
    }
  ],
  "counts": {
    "products_in_run": 48,
    "products_with_binding_cap_45": 28,
    "nova1_products_at_D": 10,
    "nova1_products_at_D_denominator": "products in D-cluster with nova=1 (verified from run_summary product list)",
    "brined_flag_correctly_fired_verified_trace": 1,
    "run_summary_brined_flag_fired_reported": 0,
    "discrepancy_note": "run_summary reports brined_flag_fired=0 but individual trace for 7290108509106 shows context_flag=brined_food — counting logic in batch_run_brined_cheeses_001.py reads context_flag from evaluation_scope key but trace stores it at top level; Data Agent must reconcile before re-run"
  },
  "commands_run": [],
  "not_done": [
    "EV-053 not yet registered in evidence_registry_v1.md — requires orchestrator routing",
    "D7 co-sign from Product Agent not obtained — requires orchestrator routing",
    "HP_FAT_SODIUM_COMBO suppression EV not drafted — separate task, same D7 batch",
    "score_engine.py not modified — ruling only; implementation blocked until D7",
    "No re-run produced — re-run after D7 approval and implementation",
    "Vocabulary gap (construct-form names, barcode 3075805) not fixed — deferred item",
    "brined_flag_fired counter bug in batch_run script not fixed — Data Agent scope"
  ],
  "self_check": {
    "spec_conflict": "none — this ruling surfaces a contradiction inside the existing engine that was not visible until the first real-shelf run; it does not conflict with any standing owner ruling",
    "frozen_invariant_touched": false,
    "published_scores_moved": 0,
    "tripwire_analysis": "No owner tripwires fire: (1) no published scores changed; (2) brined-cheese category not yet live — fix is pre-launch; (3) no major program started or killed; (4) no external commitment; (5) no strategy change. Product Agent co-sign required for D7 (scoring rule change) but this does not require owner escalation.",
    "acceptance_test": "BLOCKED — the acceptance test is: run_brined_002 after fix shows NOVA-1 clean products scoring above NOVA-3 same-fat-tier products in the full-fat tier. Cannot pass until EV-053 registered + D7 co-sign + implementation."
  }
}
```
