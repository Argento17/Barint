# Hummus Boundary Review — Where Do Canned / Raw Chickpeas Belong?

**Task:** TASK-073
**Owner:** Product Agent
**Date:** 2026-05-31
**Status:** DRAFT — pre-launch decision, requires Nutrition Agent + QA Agent co-sign
**Inputs:** `hummus_frontend_v1.json` (TASK-061), `hummus_frontend_build_report.md` §3.5, `hummus_insights_v1.md` Batches 1–2, `hummus_content_review.md` R-2
**Companion:** `bari_explanation_framework_v1.md`

---

## 1. The Question

The hummus category (`חומוס וממרחים`) is built and frozen as a **comparison of prepared savory spreads** — ready-to-eat hummus, matbucha, eggplant, pepper, masabacha. Inside the corpus sit a distinct set of products that are **not prepared spreads at all**: whole, raw, frozen, or canned chickpeas — the legume itself, a cooking ingredient.

TASK-073 asks where these belong:
- (a) Hummus
- (b) Pantry staples
- (c) Separate category
- (d) Non-ranked informational section

---

## 2. The Affected Products

### Group 1 — Single-ingredient whole / raw / frozen chickpeas (displayable, grade A)
All `ingredient_count` = 1, `additive_count` = 0, NOVA-1 single-ingredient floor (SRC-01).

| PID | Name | Score | Grade |
|---|---|---|---|
| bsip1_7296073733324 | חומוס | 85.5 | A |
| bsip1_7296073733331 | חומוס ענק | 85.5 | A |
| bsip1_7296073005889 | חומוס לבן ענק שופרסל | 85.4 | A |
| bsip1_7296073006015 | חומוס גדול שופרסל | 85.4 | A |
| bsip1_3643820 | חומוס ענק | 85.0 | A |
| bsip1_7296073705505 | חומוס מוקפא (frozen) | 85.0 | A |

### Group 2 — Canned whole chickpeas, branded (displayable, A–B)
Ingredient text scraped as **marketing copy**, not an ingredient list (TASK-064 R-2 — "ללא חומר משמר" unverified).

| PID | Name | Score | Grade |
|---|---|---|---|
| bsip1_7290018359686 | הקיסר חומוס ענק | 80.4 | A |
| bsip1_208428 | חומוס שלם יכין | 79.9 | B |

### Group 3 — Whole chickpeas, no nutrition panel (already unavailable)
| PID | Name | State |
|---|---|---|
| bsip1_7296073733317 | חומוס | `unavailable` |
| bsip1_7296073733348 | חומוס ענק | `unavailable` |

**Total: 10 products** (8 displayable, 2 already suppressed).

### NOT affected — masabacha stays in
`masabacha` (2 products, e.g. חומוס מסבחה) is a **prepared dip** (whole chickpeas served in tahini/sauce), not a raw ingredient. It is a legitimate savory spread and remains in the ranked comparison.

---

## 3. Why This Is a Problem (three distinct failures)

### 3.1 Comparability failure
The category page promises a comparison of *spreads you put on bread*. Raw and canned chickpeas are a *cooking ingredient*. Scoring a bag of dried chickpeas on the same axis as a finished hummus and then ranking them against each other is apples-to-oranges; the resulting order does not help the shopper who came to compare hummus.

### 3.2 Data-conditional inflation at the very top of the ranking
The build report (§3.5) is explicit: ranks 1–6 score 85–85.5 via the single-ingredient floor, and **"grades are data-conditional, not earned organically"** — they have *no ingredient list*, so the floor protects them from the data gap. Of the **8 grade-A products in the entire corpus, 7 are whole or canned chickpeas; only one (סלט חומוס, 80.2) is a genuine prepared spread.**

> The first six things a consumer sees in a hummus comparison are bags of chickpeas that out-rank every actual hummus — and they rank first *because Bari had the least information about them*, not the most.

### 3.3 Unverified claims surface as top results
Group 2's "ללא חומר משמר" lines (TASK-064 R-2) are unverified marketing copy. Putting these at A/near-top means Bari's least-substantiated records get its highest visibility.

---

## 4. Options Evaluated

| Option | Verdict | Reasoning |
|---|---|---|
| **(a) Keep in Hummus, ranked** | ✗ Reject | Causes all three failures in §3. Status quo. |
| **(b) Move to Pantry staples** | ◐ Correct long-term, not available now | Dried/canned chickpeas genuinely belong with pantry legumes. But there is **no Pantry category** — Hummus is the launch category. Cannot block launch on a category that does not exist. |
| **(c) Separate ranked category** ("גרגירי חומוס") | ◐ Partial | Removes the comparability break, but ranking 6–8 near-identical single-ingredient products against each other produces a meaningless 85.0-vs-85.5 leaderboard driven by the fat-data noise. Ranking adds no value here. |
| **(d) Non-ranked informational section** | ◐ Right shape, needs a home | Correctly drops the ranking; on its own it leaves the products' category membership ambiguous. |

No single listed option is sufficient alone. The recommendation combines (c)+(d) now and (b) later.

---

## 5. Recommendation

### 5.1 For the Hummus launch (now)
**Remove all Group 1 and Group 2 products from the ranked prepared-spread comparison, and present them in a separate, clearly-labelled, NON-RANKED informational section on the hummus page.**

- Section heading (draft): **"גרגירי חומוס — חומר גלם, לא ממרח מוכן"**
- Section note (draft): "מוצרים אלה הם גרגירי חומוס לבישול, ולא ממרחים מוכנים. הם מוצגים לעיון בלבד ואינם מדורגים מול הממרחים."
- **No grade letter, no rank position, no score-vs-score ordering** inside this section. If a number is shown at all, it is shown without a competing grade badge.
- Per-product explanation uses the `bari_explanation_framework_v1.md` §4.5 treatment (states "חומר גלם, לא ממרח מוכן" and the unverified-list caveat for Group 2).
- Group 3 (already `unavailable`) stays suppressed — no change.

This is option **(d) executed as a labelled sub-section (c) of the hummus page**, deferring the true home **(b)** until Pantry exists.

### 5.2 Effect on the ranked comparison
Removing the 8 displayable chickpea products from the ranking:
- The ranked set becomes ~59 genuine prepared spreads.
- **The #1 prepared spread becomes סלט חומוס (80.2, A)** — an actual hummus, which is the honest, useful top result.
- Grade-A among ranked spreads drops from 8 to ~1–2, which correctly reflects that very few *prepared* hummus products reach A. This is a more truthful distribution, not a worse one.
- Category counts, methodology copy, and `grade_distribution` in `hummus_content_v2.json` must be re-derived for the ranked set (coordinate with Data + Content Agents).

### 5.3 Long-term (post-launch)
When a **Pantry / קטניות** category is built, migrate these products there as their true home (option b), and replace the hummus-page informational section with a cross-link.

---

## 6. What This Touches (handoff)

| Area | Change | Owner |
|---|---|---|
| `hummus_frontend_v1.json` | Tag Group 1+2 with a `ranked: false` / informational flag; recompute ranked-set distributions | Data Agent |
| Hummus page | Render the non-ranked informational section; exclude flagged products from sort/filter | Frontend Agent |
| `hummus_content_v2.json` | Re-derive `grade_distribution`, counts, score stats for the ranked set; add the section heading/note strings | Content Agent (Nutrition + Product co-sign) |
| Per-product copy | §4.5 boundary treatment for the 8 products | Content Agent |
| Methodology | Note that raw chickpeas are shown separately and unranked | Content Agent |
| Verdict | Verify ranked set excludes all 10, top result is a prepared spread, no orphaned counts | QA Agent |

---

## 7. Open Decisions for Co-Sign

1. **Nutrition Agent:** confirm the single-ingredient floor products carry no scoring objection to being shown unranked (the floor was a data-gap protection, not an earned-quality signal — consistent with build report §3.5).
2. **Product + Frontend:** confirm the informational section is in launch scope, or defer the section and simply *exclude* the 10 products from launch (showing only ranked prepared spreads) — a lighter option if section build is too costly for v1.
3. **Data Agent:** confirm recomputed ranked-set statistics before Content re-writes the methodology counts.

---

*Hummus Boundary Review — TASK-073 — Product Agent — 2026-05-31*
*Recommendation: non-ranked informational section now (c+d); migrate to Pantry later (b). Top ranked spread becomes סלט חומוס (80.2).*
