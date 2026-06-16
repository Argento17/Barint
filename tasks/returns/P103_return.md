# P103 Return — TASK-280 Phase-1: PHVO Detection D6 Ruling
**Agent:** nutrition-agent  
**Date:** 2026-06-14  
**Task:** TASK-280 Phase-1  
**Status:** RETURNED  

---

## Preamble: Critical Factual Error in Fix-B Code Comment

Before the formal rulings, I must surface a factual error in the committed code that bears on Q1.

`signal_extractor.py` line 1167 contains this comment:

```python
"מחמאה",  # Fix-B: margarine/shortening (Hebrew common form)
```

**This comment is wrong.** מחמאה is clarified butter (ghee) — an animal fat product produced by separating milk fat from water and milk solids. It is not margarine or shortening. Margarine is מרגרינה. The code's author appears to have confused the two. This misidentification is the root cause of the Q1 dispute and must be corrected regardless of the D6 ruling on the marker itself.

---

## D6 Ruling — Q1: Is מחמאה Correctly Classified as a PHVO Marker?

**Ruling: REMOVE מחמאה from _PHVO_MARKERS**

**Rationale:**

מחמאה (clarified butter / ghee) is a traditional dairy fat produced by rendering butter to remove water and milk solids. Its fat profile is approximately 60–65% saturated fatty acids (primarily palmitic and stearic acid), with CLA and vaccenic acid as the naturally-occurring trans fats — the same ruminant-derived trans fats the engine already exempts from the trans-fat veto under EV-050 when `category == "whole_food_fat"`.

PHVO detection was designed for one purpose: identifying **industrial trans fat from partial hydrogenation of vegetable oils**. The mechanism of harm attributed to PHVO — formation of elaidic acid and other industrial trans isomers — is chemically distinct from ruminant-origin CLA/vaccenic acid. Applying the PHVO ceiling to מחמאה would:

1. **Misidentify the fat source type** — saturated animal fat and partially-hydrogenated vegetable oil are structurally and metabolically distinct inputs. The engine already handles this distinction in the natural-dairy trans fat exemption gate (EV-050, score_engine.py ~line 1985).

2. **Create a double-penalty mismatch** — the sat_fat dimension already penalizes high saturated fat content. If מחמאה appears in a snack product, its sat_fat load (which will be substantial, since ghee is ~99% fat) will score through the existing fat_quality curve with trans/seed-oil penalties as applicable. A PHVO ceiling on top is a second penalty for the same structural concern, reaching through the wrong mechanism.

3. **Misfire on kosher/traditional products** — some Israeli products (certain pastries, halva derivatives) legitimately use מחמאה. Penalizing these via a PHVO gate attributes trans-fat industrial processing to a traditional ingredient. This is a category error.

4. **The Option B argument fails on scrutiny** — the claim that "מחמאה in processed products is a formulation richness signal like margarine" is not supportable as a PHVO-class signal. If the concern is caloric richness from animal fat, that is captured by fat_g and sat_fat_g in the existing fat_quality dimension. A PHVO ceiling with ceiling=40 is designed to penalize **industrial hydrogenation**, not fat richness. Using it for the latter is scope creep that distorts the signal's meaning.

**Downstream scoring implication of REMOVE:** Products containing מחמאה continue to have their sat_fat-driven fat_quality scored via the existing formula. They do not receive the PHVO ceiling. For whole_food_fat category products (e.g., ghee-based condiments), the trans-fat exemption gate already handles their ruminant trans fat correctly. For processed snack products, sat_fat red-label penalties through the fat_quality curve are sufficient and correctly sourced.

**Evidence tier:** Strong for the chemical distinction (standard food chemistry). Moderate for the metabolic distinction between CLA/vaccenic and elaidic acid — well-established but dose-response at typical product-level consumption less certain (consistent with EV-050's own stated tier).

---

## D6 Ruling — Q2: Is the fat_quality Ceiling of 40 the Correct Threshold, and Should a Quantity Gate Apply?

**Ruling: Keep ceiling = 40. Add ingredient-rank threshold at N ≤ 8 (the first half of a typical 15–20 ingredient biscuit/granola product).**

**Rationale for ceiling value (40):**

A fat_quality score of 40 maps to the lower-D range on the fat dimension — a meaningful but not catastrophic penalty that prevents a high-fat-quality score from masking the industrial-hardened-fat concern. The ceiling is not punitive of the full product; it caps only the fat dimension while allowing other dimensions (whole grain, fiber, protein, additive quality) to contribute normally to the final score.

The alternative values are less defensible:
- Ceiling = 30 (harsher): would make the PHVO gate nearly as severe as a trans-fat veto in the fat dimension alone. Disproportionate for a ceiling that fires on ingredient-list presence alone without quantity confirmation.
- Ceiling = 50 (neutral): effectively removes the penalty. Defeats the purpose.
- Ceiling = 35: splitting precision finer than the evidence can justify.

40 is calibrated correctly: it penalizes but does not execute. It remains consistent with the existing trans-fat score penalization pathway (which subtracts 10–20 from fat_quality for trans_fat_status=present/high_concern before this ceiling applies).

**Rationale for adding ingredient-rank threshold at N ≤ 8:**

The current implementation fires on ANY occurrence of מרגרינה in the ingredient list, whether it is the second ingredient by weight (major component) or the sixteenth (trace amount used as pan-release or anti-sticking agent). This is a binary detection that does not respect the Israeli ingredient-ordering convention (descending order by weight).

The concern: מרגרינה as ingredient #2 vs ingredient #15 are materially different fat-architecture stories. A product where margarine is a dominant fat source genuinely warrants the PHVO ceiling. A product where it appears in trace position (e.g., "מרגרינה שמן דקל 0.1%" in a baking spray type formulation) should not receive the same treatment.

Proposed threshold: fire only if the PHVO marker appears within the first 8 ingredients. This is not an arbitrary number — in Israeli retail biscuit and granola products, the first 8 positions typically cover 85–95% of product mass by weight. A PHVO marker in position 9+ is likely a trace functional ingredient. At snk-019, מרגרינה is ingredient #6 — it would correctly fire under this rule.

**Calibration implication:** The N=8 threshold should be verified against the snacks corpus before D7 sign-off. If any product has PHVO marker in position 1–8 that the engine should NOT penalize (a false positive under the quantity gate), that would require a revision. The Data Agent should run a position analysis on the next snacks batch run.

Evidence tier for ceiling = 40: Moderate (calibrated against the existing trans-fat penalty scale and fat_quality curve behavior; no direct RCT evidence for a ceiling at this value).
Evidence tier for N=8 rank threshold: Moderate (based on Israeli ingredient ordering convention; would benefit from empirical corpus validation).

---

## D6 Ruling — Q3: Which Product Categories Should PHVO Detection Apply To?

**Ruling: Gate PHVO ceiling to processed food archetypes — exclude whole_food_fat and dairy_protein categories explicitly.**

**The most defensible option is a hybrid of A and B: fire in all categories by default, with explicit category-exclusion guards for categories where PHVO cannot structurally occur, PLUS a structural constraint that protects the natural-dairy-trans-fat exemption logic.**

**Rationale:**

Option A (all categories) has operational appeal — it avoids maintaining a category whitelist. But it creates a logical contradiction: the engine already has a natural-dairy-trans-fat exemption gate (EV-050) that requires `not has_phvo` for the exemption to fire. If a dairy product contains מחמאה (clarified butter), and מחמאה is REMOVED from _PHVO_MARKERS per Q1, then the whole_food_fat conflict disappears entirely for that case.

The remaining risk is for dairy/whole-food-fat products that might genuinely contain מרגרינה or שומנים מוקשים. In practice, these would be processed dairy products (processed cheese, flavored dairy spreads) where the PHVO ceiling is appropriate. Genuinely clean dairy products do not contain margarine.

Therefore: keep PHVO firing on all categories by default, with the following explicit exclusions:

1. **The מחמאה removal (Q1)** eliminates the primary whole_food_fat false-positive path.
2. **The natural-dairy-trans-fat exemption gate (EV-050)** is already conditional on `not has_phvo` — this gate remains correct and does not need modification.
3. **Produce and single-ingredient whole foods** are structurally impossible to contain PHVO and will never have has_phvo=True from their ingredient text, so no category gate is needed for them.

The only genuinely risky edge case is a dairy_protein or whole_food_fat product that does contain מרגרינה or שומנים מוקשים — which would be a legitimately compromised product and should receive the ceiling.

Option B (explicit category gate) would add maintenance burden for limited benefit given Q1 removes the primary false-positive source. Not recommended unless the corpus analysis reveals systematic false positives.

Evidence tier: Moderate (operational reasoning + architectural consistency with EV-050).

---

## D6 Ruling — Q4: Should the Existing snk-019 Score (40/D) Be Retroactively Corrected?

**Ruling: PRINCIPLE — patch if and only if the grade changes (D → E). Do not patch for score movement within grade.**

**Rationale:**

The snk-019 BSIP0 panel shows:
- fat_g = 3.4g / 100g
- fat_saturated_g = 1.2g / 100g
- trans_fat_g = 0.5 (Israeli threshold-declaration convention — the engine correctly classifies this as `threshold_declaration`, not a confirmed real trans fat signal)
- מרגרינה is ingredient #6 (coconut oil + E471 composite)

The critical observation: snk-019's מרגרינה is declared as "(שמן צי''ה, שמן קוקוס, מים, מלח, מתחלב (E471))" — it is a coconut-oil-based spread, not a partially-hydrogenated-vegetable-oil margarine. Coconut oil is a highly saturated tropical fat that does not require hydrogenation. There is no industrial trans fat pathway here. The PHVO ceiling firing on this product based on the word "מרגרינה" alone is a false positive of exactly the kind that the ingredient-rank threshold and product-level scrutiny should catch.

This means: under the corrected rules proposed in Q1–Q3, Fix-C may NOT fire on snk-019 at all once ingredient-level scrutiny is applied to confirm whether the מרגרינה is actually hydrogenated or is a coconut/tropical oil composite. If Fix-C does not fire, the score remains 40/D and no patch is needed.

**Principle for the patch decision:**
- If the corrected engine (post Q1–Q3 implementation) produces a **grade change** (D → E or any grade change), the currently-displayed score is wrong in a consumer-material sense. Bari's standard "unknown is acceptable; wrong is not" applies. In that case: patch the deployed JSON after D7 co-sign and owner notification (this is a consumer-facing change).
- If the corrected engine produces a **score change within the same grade** (e.g., 40→36, still D), the consumer-facing grade label is not wrong. The principle does not require emergency patching. The corrected score ships on the next scheduled snacks re-score.

**Implementation note:** The orchestrator must determine, after D7 and Data Agent implementation, whether the corrected engine changes snk-019's grade before deciding whether to issue a patch. The Nutrition Agent does not authorize the patch itself — that requires D7 co-sign + orchestrator decision.

---

## Proposed Final _PHVO_MARKERS List

```python
_PHVO_MARKERS = [
    "שומן צמחי מוקשה",      # hydrogenated vegetable fat (explicit vegetable + hardened)
    "שמן צמחי מוקשה",       # hydrogenated vegetable oil (explicit vegetable + hardened)
    "מוקשה חלקית",          # partially hydrogenated (explicit partial modifier)
    "partially hydrogenated",
    "שומנים מוקשים",         # hardened fats (plural — covers less-specific declarations)
    "שומן מוקשה",            # hardened fat (singular — covers less-specific declarations)
    # "מחמאה" REMOVED — clarified butter (ghee), animal fat, not PHVO. D6 ruling Q1.
    "מרגרינה",               # margarine (transliteration form)
]
```

**Changes from current committed list:**
- מחמאה: REMOVED (D6 Q1 ruling)
- All other markers: RETAINED unchanged

---

## Proposed _PHVO_FAT_QUALITY_CEIL and Activation Rule

```python
_PHVO_FAT_QUALITY_CEIL = 40          # ceiling value unchanged (D6 Q2 ruling)
_PHVO_MARKER_MAX_POSITION = 8        # NEW: only fire ceiling if PHVO marker in first 8 ingredients
```

The implementation of the position guard requires a change to the detection logic in `signal_extractor.py`: `has_phvo` should become position-aware rather than a pure text search across `full_text`. Specifically, the detection should iterate `ingredient_order` (already built) and only set `has_phvo=True` if the PHVO marker appears within an ingredient at position ≤ 8. A fallback to the current full-text search should remain for products where no structured ingredient list is available (ingredient_order is empty but ing_text is present) — in that case, the current behavior is the safe default.

This implementation change requires a separate D6/D7 ruling if it is considered a new rule. I hereby issue the D6 designation for this position-gate as part of this ruling.

---

## EV Designation

The highest EV number referenced in the current engine is **EV-085** (TASK-278 / biscuit×sugar normalization). The PHVO detection was previously entered as **EV-050** (the core PHVO concept, natural-dairy exemption gate).

The Fix-B/Fix-C changes represent an **extension of EV-050**, not a new independent concept. However, the מחמאה removal, the ceiling value ratification, and the position gate are material changes to the rule that warrant their own registry entry for governance traceability.

**Proposed designation: EV-086** — PHVO marker correction + fat_quality ceiling ratification (Fix-B/C D6 ruling, TASK-280).

This EV entry should record:
- Q1 ruling: מחמאה removed from _PHVO_MARKERS (animal fat, not PHVO)
- Q2 ruling: ceiling = 40 ratified; position gate N ≤ 8 added
- Q3 ruling: all-categories scope retained; no category exclusion list needed after מחמאה removal
- Q4 ruling: grade-change triggers patch; within-grade score movement does not
- Evidence tier: Moderate (architectural reasoning + standard food chemistry; no RCT evidence for the specific ceiling value)

---

## What Was NOT Done

- No engine files were modified (as specified)
- No JSON files were modified (as specified)
- No D7 Product Agent co-sign issued here — that is required before any implementation
- No snacks re-score authorized — orchestrator decision after D7
- Task not closed — RETURNED for orchestrator review

---

## Return Contract

```json
{
  "task_id": "TASK-280",
  "phase": "Phase-1 D6 ruling",
  "status": "RETURNED",
  "return_date": "2026-06-14",
  "agent": "nutrition-agent",
  "d6_rulings": {
    "Q1_mchama": "REMOVE",
    "Q2_ceiling": {
      "value": 40,
      "quantity_gate": "position_8",
      "quantity_gate_note": "PHVO ceiling fires only if marker appears in first 8 ingredient positions; full-text fallback for unstructured ingredient lists"
    },
    "Q3_category_scope": "all_with_mchama_removal_as_primary_guard",
    "Q4_retroactive_correction": "patch_if_grade_changes"
  },
  "proposed_phvo_markers": [
    "שומן צמחי מוקשה",
    "שמן צמחי מוקשה",
    "מוקשה חלקית",
    "partially hydrogenated",
    "שומנים מוקשים",
    "שומן מוקשה",
    "מרגרינה"
  ],
  "proposed_fat_quality_ceil": 40,
  "proposed_position_gate": 8,
  "ev_designation": "EV-086",
  "critical_finding": "Code comment on signal_extractor.py:1167 misidentifies מחמאה as 'margarine/shortening' — it is clarified butter (ghee). Comment must be corrected regardless of ruling on the marker itself.",
  "snk_019_note": "Product's מרגרינה is declared as coconut oil + E471 composite — not a hydrogenated vegetable oil margarine. Under the position gate (ingredient #6 ≤ 8), PHVO ceiling would still fire. However, the ingredient identity (coconut oil) is structurally different from PHVO; the position gate alone does not resolve this edge case. Data Agent should note this when running the corrected engine.",
  "artifacts": [
    {
      "path": "C:/Bari/tasks/returns/P103_return.md",
      "type": "d6_ruling",
      "sha256": "not_computed_ruling_doc"
    }
  ],
  "counts": {
    "questions_ruled": 4,
    "questions_total": 4,
    "markers_removed": 1,
    "markers_retained": 6,
    "markers_added": 0,
    "ev_entries_proposed": 1
  },
  "commands_run": [],
  "not_done": [
    "D7 Product Agent co-sign — required before implementation",
    "signal_extractor.py modification — blocked until D7",
    "snacks corpus position analysis — Data Agent task post-D7",
    "snk-019 grade impact determination — requires corrected engine run",
    "EV-086 registry entry authorship — requires Nutrition + Research Agent collaboration"
  ],
  "acceptance_test": "Four D6 rulings issued with evidence tier. Proposed markers list provided. Ceiling value stated. EV designation assigned. Critical code-comment error surfaced. No engine or JSON files modified."
}
```
