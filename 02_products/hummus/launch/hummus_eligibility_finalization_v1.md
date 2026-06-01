# Hummus Category Eligibility — Finalization

**Task:** TASK-087A
**Owner:** Product Agent
**Date:** 2026-05-31
**Reviewed:** all 63 products currently displayed on `/hashvaot/hummus` (`hummus_frontend_v3.json`, run_hummus_002)
**Test applied:** *Would a shopper searching "חומוס" reasonably expect this product to appear in a **ranked hummus-spread** comparison?*

---

## 1. Finding

Of the 63 displayed products, **4 are not prepared spreads** — they are whole/canned chickpeas (the legume / a cooking ingredient). Two of them currently sit at the **top of the ranking**:

- **Rank 1** = הקיסר חומוס ענק — a **can of whole chickpeas**, ingredient field is cooking instructions ("סננו, הוסיפו מלח ופלפל… יבשו בתנור"), ranked **A above every real hummus**.
- **Rank 3** = חומוס שלם יכין — a **can of whole chickpeas** ("מעולה כתוספת לרוטב, לקוסקוס או למרק").

This is the exact failure the task targets: a shopper comparing hummus spreads sees a can of chickpeas ranked first.

The 6 single-ingredient raw/frozen chickpeas (NOVA-1) flagged in TASK-073/069 are **already excluded** and not displayed — no further action; listed at the bottom for completeness.

---

## 2. Decision Table

| Product | Current rank | Decision | Reason |
|---|---|---|---|
| הקיסר חומוס ענק · `bsip1_7290018359686` · 80/A | **1** | **EXCLUDE** | Canned whole chickpeas (cooking ingredient). Ingredient field is cooking instructions, not a spread recipe. A shopper comparing hummus spreads would not expect a can of chickpeas ranked #1. |
| חומוס שלם יכין · `bsip1_208428` · 80/B | **3** | **EXCLUDE** | Canned whole chickpeas ("חומוס שלם" = whole chickpeas; "תוספת לרוטב/קוסקוס/מרק"). Cooking ingredient, not a ready-to-eat spread. |
| חומוס · `bsip1_7296073733317` · no score | 62 | **EXCLUDE** | Whole chickpeas, no nutrition panel (already `unavailable`). Not a prepared spread; should not be on the spread page at all. |
| חומוס ענק · `bsip1_7296073733348` · no score | 63 | **EXCLUDE** | Whole/giant chickpeas, no nutrition panel (already `unavailable`). Cooking ingredient, not a spread. |
| חומוס גרגרים בתטבילה · `bsip1_7290112968685` · 63/C | 39 | **ELIGIBLE** | Genuine **prepared dip** — cooked chickpeas in a seasoned tahini/oil/hot-pepper sauce ("חומוס מבושל 34%, טחינה גולמית 20%, פלפלים חריפים…"). Ready-to-eat savory spread (masabacha-family). Keep ranked. |
| *6× raw/frozen NOVA-1 chickpeas (e.g. `bsip1_7296073733324`, `bsip1_7296073705505` מוקפא)* | — *(already excluded)* | **EXCLUDE** (confirm) | Already filtered via `EXCLUDED_NOVA1_IDS`. Single-ingredient raw/frozen chickpeas; confirmed not eligible. No change. |

**All other 58 displayed products are prepared spreads (hummus, masabacha, matbucha, eggplant, pepper) → ELIGIBLE, unchanged.**

---

## 3. Final Recommendation

# REMOVE_NON_SPREAD_PRODUCTS_ENTIRELY

Add the 4 non-spread products above to the existing exclusion set (alongside the 6 already-excluded NOVA-1 chickpeas).

**Why remove entirely rather than KEEP_INFORMATIONAL_SECTION:**
1. **No home and no built section.** There is no Pantry/legumes category, and the non-ranked informational section was deferred in TASK-086 (unbuilt UI). EXCLUDE needs no new structure.
2. **Consistency.** The 6 NOVA-1 chickpeas are already removed entirely with no negative effect. Removing these 4 completes one coherent policy: *no whole/canned/raw chickpeas on the spread page.*
3. **Low display value.** The two canned products' ingredient data is unverified marketing/cooking copy (TASK-064 R-2); the two `unavailable` products have no nutrition data. Neither adds informational value even unranked.
4. **Goal met immediately and unambiguously** — the goal ("a shopper should never see a canned/raw chickpea product ranked against prepared hummus spreads") is fully satisfied with zero ranking ambiguity.

*Revisit later (option b, TASK-073 §5.3): if a Pantry / קטניות category is built, migrate these products there as their true home and cross-link.*

---

## 4. Effect on the Ranked Comparison

| Metric | Before | After REMOVE |
|---|---|---|
| Displayed products | 63 | **59** |
| Scored displayed | 61 | **59** |
| **Rank #1** | הקיסר חומוס ענק (can of chickpeas, A) | **סלט חומוס (80/A — a real prepared hummus)** |
| Grade A (displayed) | 2 | **1** | (the surviving A is a genuine spread) |
| Non-spread products in ranking | 4 | **0** |

The grade-A count dropping to 1 is **more truthful, not worse**: very few *prepared* hummus reach A, and the one that does is an actual spread.

---

## 5. Handoff

| Change | Owner |
|---|---|
| Add the 4 IDs to `EXCLUDED_NOVA1_IDS` (or a renamed `EXCLUDED_NON_SPREAD_IDS`) in `hummus-comparison-page-data.ts` | Frontend Agent |
| Re-derive ranked-set counts / `grade_distribution` (59 products, 1×A) in hero/methodology copy | Content + Data Agent |
| Verify ranked set contains 0 whole/canned/raw chickpeas; #1 is a prepared spread | QA Agent |

IDs to exclude: `bsip1_7290018359686`, `bsip1_208428`, `bsip1_7296073733317`, `bsip1_7296073733348`.

---

*TASK-087A — Product Agent — 2026-05-31 — Recommendation: REMOVE_NON_SPREAD_PRODUCTS_ENTIRELY*
