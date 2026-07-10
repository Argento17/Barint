# P507 / C3 challenge — do 4 recommendation tiers re-create the rejected grade system? (route: C3)

**Repo:** C:\Bari. **Task:** TASK-504 (Supplement Guides / מדריכים — magnesium guide).
**Role:** C3 = independent challenge/consult. You do NOT build/edit/close. Challenge hard, then give support / support-with-changes / oppose.

## Context
The owner originally killed ORDINAL ranking of supplements and the whole מדריכים redirection replaced it with transparent per-bar states (PASS/FLAG/FAIL/CANNOT-VERIFY) grouped into unordered buckets. After seeing the built page, the owner has now directed a REVERSAL: group products into 4 NAMED, ORDERED recommendation tiers — **מומלץ מאוד · מומלץ · טוב · לא מומלץ** — and remove the old bucket header. Product has proposed the mapping.

## Read
- Product's proposal (what you challenge): `C:\Bari\03_operations\reports\product\magnesium_guide_recommendation_tiers_v1.md`
- The anti-drift invariant it must not break: `C:\Bari\01_framework\nutrition\supplement_guides_bar_rubric_v1.yaml` HARD RULE 1 (no composite/weighted number, "no 'N/6 bars passed' percentage, no point value per bar-state").
- The founding finding: the whole redirection exists because ranking-by-composite-number was the owner's identified failure mode.

## Challenge these specifically
1. **The count-threshold split rule.** Product splits `passes_with_flag` into מומלץ (exactly 1 non-PASS bar among the 4 displayed) vs טוב (2+). Counting non-PASS bars and thresholding is arguably EXACTLY the "N bars passed" aggregation HARD RULE 1 forbids. Is this a smuggled composite? If you think it crosses the line, propose a QUALITATIVE alternative split (e.g. by WHICH bar/what kind of caveat, not a count) that achieves 4 tiers without any counting.
2. **Ordered tiers vs the rejected ranking.** The 4 tiers are displayed as an ordered ladder (מומלץ מאוד → לא מומלץ). Is this materially different from the ordinal ranking the owner rejected, or is it the same thing relabeled? Is Product's defensibility argument (every placement is a falsifiable lookup over visible bars, no number) sufficient, or does an ordered recommendation ladder re-create the opaque-grade UX regardless of how it's computed?
3. **Honesty of the tier labels.** 12 of 18 land in לא מומלץ and the top tier is empty. Is a guide where two-thirds of products are "not recommended" and zero are "highly recommended" honest and useful, or does it read as broken/harsh? Is TRIOMAG's separate "לא ניתן להעריך" callout the right honest home, or a dodge?
4. **Precedent risk.** If magnesium gets 4 recommendation tiers, does that bind every future guide (creatine) to the same, and does it quietly re-open the door to the composite scoring the redirection closed?

## Return
Write to `C:\Bari\tasks\returns\P507_return.md`: verdict (support / support-with-changes / oppose) up top, the four points each with a concrete recommendation, and — if you find the count-rule crosses anti-drift — a specific qualitative replacement split rule. End with the machine-readable return contract JSON. Edit nothing but your return.
