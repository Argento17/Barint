# Hummus Explanation-Layer Preview Report

**Task:** TASK-082 — Deploy Hummus v2 explanation-layer preview
**Owner:** Frontend Agent
**Date:** 2026-05-31
**Route:** `/hashvaot/hummus`
**Purpose:** Let the Product Agent evaluate whether the *existing* single-line insight layer is
sufficient before committing to a larger Explanation Framework build.

---

## 1. What was deployed

| | Fallback experience (baseline) | Insight-line experience (preview) |
|---|---|---|
| Data source | `hummus_frontend_v1.json` | `hummus_frontend_v2.json` (`v2-content-integrated`) |
| `insightLine` per product | empty → filled by `GRADE_INSIGHT_FALLBACK` | product-specific, from `hummus_insights_v1.md` (TASK-062 / TASK-081) |
| Content origin | generic, one string per grade | derived from each product's ingredient list / composition |
| Build | `next build` ✓ compiled | `next build` ✓ compiled (final live state) |

The preview is wired through the existing import in
`src/lib/comparisons/hummus-comparison-page-data.ts`:

```ts
import rawCorpus from "@/data/comparisons/hummus_frontend_v2.json";
```

`stripHummusInternalFields()` keeps the grade fallback as a safety net
(`rest.insightLine || GRADE_INSIGHT_FALLBACK[grade]`), but because **all 69 products in v2 carry a
populated `insightLine`, the fallback no longer fires** for any row. No component or layout changes
were required — this is a pure content swap on the existing UI.

The rebuild completed cleanly and `/hashvaot/hummus` prerenders as static content in both states.

---

## 2. How big is the difference? (measured)

Across the **63 ranked products** (6 NOVA-1 whole-chickpea items excluded; 2 score-unavailable items
retained):

| Metric | Fallback (v1) | Insight (v2) |
|---|---|---|
| Distinct `בקצרה` strings shown | **4** (one per grade A/B/C/D) | **59** (near one-per-product) |
| Products with no `בקצרה` line | 2 (null-grade) | 0 — even the 2 score-unavailable items get a line (*"מידע תזונתי לא מספיק לניתוח"*) |
| Information in the line | restates the grade | states the product's actual composition |

In the fallback build, **61 scored products collapse into 4 sentences.** Every A-grade product reads
*"מבנה הרכב חזק ביחס לקטגוריה"*; every B reads *"פרופיל הרכב טוב ביחס לקטגוריה"*, and so on. The line
is therefore redundant with the grade badge already shown next to it.

In the insight build, the same rows carry distinct, composition-derived statements such as:

| Rank | Product | Grade | Insight line (v2) |
|---|---|---|---|
| 1 | הקיסר חומוס ענק | A | גרגרי חומוס ענק בשימור — מידע רכיבים מלא לא אומת |
| 4 | חומוס מסעדות | B | 34% חומוס, 31% טחינה גולמית — חומר משמר ותוספים נוספים |
| 9 | חומוס אבו גוש | B | 53% חומוס, 11% טחינה ושמן זית — מכיל עמילן ומשמר |
| 42 | סלט מטבוחה | C | 63% עגבניות מרוסקות ו-13% פלפל — מכיל סוכר לבן |
| — | מטבוחה אמיתית | D | מטבוחה עם תוספות שונות — ציון מבוסס על נתונים חלקיים |

---

## 3. Side-by-side screenshots

All images in [`screenshots/explanation_preview/`](screenshots/explanation_preview/). Both sets were
captured from production (`next start`) builds of the identical UI — only the data source differs.

| View | Fallback (v1) | Insight (v2) |
|---|---|---|
| Top 10 (desktop) | [fallback_top10_desktop.png](screenshots/explanation_preview/fallback_top10_desktop.png) | [insight_top10_desktop.png](screenshots/explanation_preview/insight_top10_desktop.png) |
| Product list (desktop) | [fallback_product_list_desktop.png](screenshots/explanation_preview/fallback_product_list_desktop.png) | [insight_product_list_desktop.png](screenshots/explanation_preview/insight_product_list_desktop.png) |
| Expanded A-grade | [fallback_a_grade_expanded.png](screenshots/explanation_preview/fallback_a_grade_expanded.png) | [insight_a_grade_expanded.png](screenshots/explanation_preview/insight_a_grade_expanded.png) |
| Expanded B-grade | [fallback_b_grade_expanded.png](screenshots/explanation_preview/fallback_b_grade_expanded.png) | [insight_b_grade_expanded.png](screenshots/explanation_preview/insight_b_grade_expanded.png) |
| Expanded C-grade | [fallback_c_grade_expanded.png](screenshots/explanation_preview/fallback_c_grade_expanded.png) | [insight_c_grade_expanded.png](screenshots/explanation_preview/insight_c_grade_expanded.png) |
| Matbucha example | [fallback_matbucha_expanded.png](screenshots/explanation_preview/fallback_matbucha_expanded.png) | [insight_matbucha_expanded.png](screenshots/explanation_preview/insight_matbucha_expanded.png) |
| Mobile view | [fallback_mobile.png](screenshots/explanation_preview/fallback_mobile.png) | [insight_mobile.png](screenshots/explanation_preview/insight_mobile.png) |

**What to look for:**

- **Top 10 / product list** — In the fallback shots, ranks 1–2 (both A) carry word-for-word
  identical text, and ranks 4–5 (both B) likewise. In the insight shots each row is distinct and
  describes the product in front of you. This is the clearest demonstration of the change.
- **Mobile** — same content swap reaches the mobile shelf with no layout regression; lines wrap to
  one or two tidy rows under each product.

---

## 4. The gap this preview reveals

The insight line is the *only* thing that changed. **The expansion panel
("למה קיבל את הציון?") is byte-for-byte identical between the two builds** — compare the expanded
screenshots: the "בשורה התחתונה" reads the same generic, grade-derived sentence in both
(*"ציון 76 (B) — פרופיל הרכב טוב ביחס לממרחים האחרים בקטגוריה."*).

That is because v2 populates `insightLine` **only**. The richer expansion fields the UI already
supports —

- `positiveSignals` — "מה עובד לטובת המוצר?"
- `limitingFactors` — "מה מגביל את הציון?"
- `comparisonContext` — "הקשר במדף"

— are **absent from v2** (0 occurrences in the JSON), so those sections never render. The expansion
still falls back to a per-grade `bottomLine` template, identical for every product of the same grade.

So the preview answers two different questions very differently:

| Question the user asks | Fallback | Insight (v2) | Still missing |
|---|---|---|---|
| "What *is* this product?" (list scan) | ✗ grade restated | ✓ composition stated | — |
| "*Why* this score vs. the one above it?" (expansion) | ✗ generic | ✗ generic (unchanged) | needs `positiveSignals` / `limitingFactors` / `comparisonContext` |

---

## 5. Recommendation for the Product Agent

The single-line insight layer in v2 is a **real, low-cost win at the list/scan level** — it removes
the redundancy of restating the grade and gives every one of 63 rows a distinct, ingredient-grounded
sentence, with zero UI work and a clean rebuild. For the *browsing/triage* job it is plausibly
"sufficient" on its own.

It is **not** sufficient for the *explanation* job. Anyone who opens "למה קיבל את הציון?" sees the
same generic grade sentence they saw before — the insight line does not reach the expansion, and the
two builds are indistinguishable there.

**Suggested decision framing:**

- If the priority is shelf scannability → **ship v2 as-is**; the insight layer is enough and is
  already live behind this preview.
- If the priority is defensible per-product *reasoning* (the "why") → the larger Explanation Framework
  is warranted, and its first increment should be the three already-supported expansion fields
  (`positiveSignals`, `limitingFactors`, `comparisonContext`), since the rendering is built and only
  the content/data is missing.

### Caveats carried into this preview (unchanged from v1)
- Fat / saturated-fat suppressed (HUM-001); sugar 0% coverage (HUM-002) — insight lines correctly
  avoid claiming either.
- 2 products remain score-unavailable (HUM-004); v2 gives them an honest insight line rather than a
  blank row.
- Go-live gate **DEC-002** (Product approval, gated on TASK-073) is still open — this preview is
  evaluation input to that decision, not a launch.

---

## Reproduction

```bash
# Insight (v2) — current live state
npx next build && npx next start -p 3000
BASE_URL=http://localhost:3000 VARIANT=insight \
  node scripts/capture-hummus-explanation-preview.mjs

# Fallback (v1) — baseline
#   temporarily set the import in src/lib/comparisons/hummus-comparison-page-data.ts
#   to hummus_frontend_v1.json, then:
npx next build && npx next start -p 3001
BASE_URL=http://localhost:3001 VARIANT=fallback \
  node scripts/capture-hummus-explanation-preview.mjs
#   then restore the import to hummus_frontend_v2.json
```

Capture script: [`scripts/capture-hummus-explanation-preview.mjs`](scripts/capture-hummus-explanation-preview.mjs)
