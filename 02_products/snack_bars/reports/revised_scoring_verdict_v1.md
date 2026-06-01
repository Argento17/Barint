# Revised Scoring Verdict v1
**Date:** 2026-05-29  
**Status:** CE Advisory Board — Verdict Revision After Data Lineage Confirmation  
**Supersedes:** `bari_scoring_verdict_v1.md` Section "Four Specific Failures" and Verdict

---

## Revision Summary

The previous verdict (MODERATE REVISION) was based partly on the incorrect assumption that snacks were scored without nutritional data. Data lineage audit confirmed:
- BSIP1: 18/18 nutrition available, 18/18 ingredients available
- BSIP2: 18/18 nutrition consumed, 18/18 ingredients consumed

This changes two of the four identified failures and downgrades the overall verdict.

---

## Revised Verdict

**MINOR REVISION**

---

## What Changed and What Remains

### Previous Failure 1 (Zero nutritional data): RETRACTED

The scoring engine DID consume nutritional and ingredient data for all 18 displayed snacks. The null values in the production JSON are display-layer stripping decisions, not evidence of missing scoring inputs.

The confidence labeling issue partially remains: products labeled "verified" vs "partial" may need review based on BSIP1 confidence scores, but this is a display-layer decision, not a scoring failure.

**Status: CLOSED**

### Previous Failure 2 (Mean convergence): REANALYZED — ROOT CAUSE CORRECTED

The 43.50 vs 43.78 convergence is explained by editorial selection, not scoring compression.

Full corpus comparison:
- Full snacks (53 products): mean = 37.20
- Maadanim (90 products): mean = 43.78
- Gap: 6.58 points — the engine correctly scores snacks lower than maadanim

The displayed snacks (18/53) were selected from the better half of the corpus. This editorial uplift of +6.30 points creates the appearance of convergence with maadanim. The scoring engine is doing its job. The editorial selection is creating a misleading display.

**Status: SCORING FRAMEWORK CLEARED. Editorial disclosure required.**

### Previous Failure 3 (False precision in D-band): CONFIRMED, REDUCED IN SEVERITY

The 1–2 point gaps between near-identical products (snk-011/012 at 43/42; snk-009/010 at 47/45) remain. These are not scoring artifacts — they reflect genuinely small compositional differences between similar products. But the practical question is whether a 1-point gap is meaningful enough to display as a ranking difference.

**Status: MINOR — no scoring change required. Consider display rounding to nearest 5 for near-identical products.**

### Previous Failure 4 (Date Sugar Halo): CONFIRMED, UNCHANGED

The date bars at 70/B receive their scores based on structural simplicity (4 ingredients, NOVA2, no additives). This reflects the framework's design philosophy. The concern is that high intrinsic sugar density is not penalized when the source is whole-food. This is a documented philosophical choice, not a scoring error, and requires disclosure rather than correction.

**Status: DISCLOSE — add sugar density note to date-bar explanations. No score change.**

---

## New Finding: The Universal Caps Are Not the Problem

The previous analysis theorized that universal caps at 68/55/60 were forcing mean convergence. This is disproven:

- NOVA4 cap at 60: NOT BINDING. Maximum NOVA4 snack score is 47.4.
- NOVA3 cap at 75: NOT BINDING. Maximum NOVA3 snack score is 62.2.
- The caps are functioning correctly as safety nets, not as mean anchors.

Introducing category-specific caps would have zero effect on current snacks rankings.

**The cap architecture does not need modification for the snacks category.**

---

## New Finding: Category Discrimination Is Working

The scoring engine produces three genuinely different means for three categories:
- Bread: 72.0
- Maadanim: 43.8
- Full snacks: 37.2

Within snacks, the engine produces three genuinely different means by NOVA tier:
- NOVA2 snacks: 54.5
- NOVA3 snacks: 47.4
- NOVA4 snacks: 28.4

This is correct, meaningful discrimination. The framework is not collapsing categories.

---

## What Requires Revision (Revised List)

### Revision 1: Editorial display transparency (URGENT)
The shelf displays 18 of 53 scored products. The displayed mean (43.5) is 6.3 points above the full corpus mean (37.2). The methodology section should communicate this explicitly.

Current methodology text mentions "18 מוצרים נבחרו לתצוגה." This needs a direct statement that the selection overrepresents the better products and the displayed average is not the category average.

**Change required:** Update `snacksPrologueSentences` and `snacksShelfMethodologyLines` to add: "ממוצע ציוני כלל הקטגוריה (53 מוצרים): 37."

### Revision 2: Explanation engine (UNCHANGED — MODERATE URGENCY)
The explanation quality audit from `snacks_explanation_engine_review_v1.md` remains valid. Only 22% of explanations are classified as Strong. The rebuild design in that document is the right scope.

This is independent of the scoring verdict. The scores may be correct; the explanations of those scores are not strong enough.

**Change required:** Full explanation rebuild per snacks_explanation_engine_review_v1.md.

### Revision 3: Date sugar halo disclosure (LOW URGENCY)
Date bars scoring 55–70/B-C receive no sugar-density awareness. A date bar is 60–70% simple sugars, which is nutritionally relevant for some consumer segments (diabetics, low-sugar diets). This does not require a score change — it requires an explanation addition.

**Change required:** Add "תמרים = ~60 גרם סוכר ל-100 גרם — מרוכז, גם אם טבעי" to date bar explanations.

### Revision 4: Category-specific grade thresholds (OPTIONAL)
Current C threshold: 55 (universal). For snacks, where most decent products score 47–58, a C threshold of 48 would better reflect category-relative quality. Under the current threshold, a product at 51/C is "above average for snacks" — but the C grade doesn't communicate this.

This is an editorial choice, not a scoring correction. It would change grade display without changing scores.

**Change required:** Optional. Evaluate after explanation rebuild is complete.

---

## What Does NOT Require Revision

1. **The BSIP2 four-layer scoring architecture** — functioning correctly
2. **NOVA classification as primary driver** — scientifically defensible and well-calibrated
3. **Universal cap values (60/75/55)** — not binding for snacks; no change needed
4. **Dimension weights** — producing correct category discrimination
5. **Category-specific calorie density tiers** — already implemented and working
6. **Concern coordination system** — prevents double-counting correctly
7. **The relative ranking order within snacks** — broadly correct; date bars at top, confectionery at bottom
8. **The full corpus score range (13–70)** — appropriate for the actual quality spread

---

## Verdict Comparison

| Dimension | Previous Verdict | Revised Verdict |
|---|---|---|
| Core scoring framework | KEEP | KEEP |
| Four-layer architecture | KEEP | KEEP |
| Universal caps | MODIFY | KEEP (not binding) |
| Confidence labels | FIX NOW | Review only |
| Explanation engine | REBUILD | REBUILD (unchanged) |
| Nutritional data pipeline | COMPLETE (urgent) | CLOSED (data was present) |
| Date sugar disclosure | DISCLOSE | DISCLOSE (unchanged) |
| Editorial transparency | — | ADD (new finding) |
| Overall verdict | MODERATE REVISION | **MINOR REVISION** |

---

## Sequencing (Revised)

**Immediate (this week):**
1. Update snacks methodology: add full-corpus mean (37) and editorial selection disclosure
2. Add date sugar awareness note to date-bar product explanations

**Short-term (2–4 weeks):**
3. Rebuild snacks explanation engine per snacks_explanation_engine_review_v1.md
4. Review confidence labels for displayed products (verify "verified" vs "partial" calls)

**Optional:**
5. Evaluate category-specific grade thresholds for snacks (C at 48 vs current 55)

**Not required:**
6. Cap architecture changes — not needed, no impact
7. Scoring formula changes — framework is producing correct results
8. Data pipeline work — data was already consumed
