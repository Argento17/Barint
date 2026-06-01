# Hummus Launch Blocker Fix Report

**Task:** TASK-069  
**Agent:** Frontend Agent  
**Date:** 2026-05-31  
**Status:** All four blockers resolved. Build passes. Screenshots captured.

---

## Blocker 1 — Corpus/Display Eligibility: Raw/Canned Chickpeas Excluded

**Issue:** Six single-ingredient NOVA-1 products (raw/whole/frozen chickpeas) appeared at the top of the ranked list with scores 85–86 (grade A). These are not prepared hummus spreads and are not comparable to the rest of the corpus.

**Fix:** Added `EXCLUDED_NOVA1_IDS` set in `hummus-comparison-page-data.ts`. Products are filtered out in `stripHummusInternalFields()` before being exported to the page.

**Files changed:**
- [hummus-comparison-page-data.ts](src/lib/comparisons/hummus-comparison-page-data.ts)

**Impact:**
- Displayed products: 69 → 63
- Scored displayed: 67 → 61
- Grade A displayed: 8 → 2
- First ranked product is now "הקיסר חומוס ענק" (score 80, prepared canned hummus with 8 ingredients)

**Documentation:** See [excluded_products_hummus_v1.md](excluded_products_hummus_v1.md)

---

## Blocker 2 — Expansion/Reasoning: Empty Expansion Content Fixed

**Issue:** All 69 products had empty `insightLine` ("") and no `positiveSignals`, `bottomLine`, or `comparisonContext` in their expansion objects. Product rows showed no description text. Expanded rows showed only the confidence label.

**Root cause:** Product-specific editorial content from `hummus_insights_v1.md` has not yet been integrated into the frontend JSON. Yogurts and other Gen 1 categories have this content populated per-product.

**Fix:** In `stripHummusInternalFields()`:

1. **`insightLine` fallback:** Each product now receives a grade-level fallback text if `insightLine` is empty. Content is factual and matches the approved grade descriptions from the methodology.
   - Grade A: "מבנה הרכב חזק ביחס לקטגוריה"
   - Grade B: "פרופיל הרכב טוב ביחס לקטגוריה"
   - Grade C: "היבטים לעיון ביחס לקטגוריה"
   - Grade D: "חששות מבניים ביחס לקטגוריה"

2. **Expansion `bottomLine` fallback:** For all scored, non-insufficient products, a grade-based bottomLine is generated: `"ציון [N] ([grade]) — [grade description] ביחס לממרחים האחרים בקטגוריה."`

Both fallbacks are marked in code comments as pending content integration from `hummus_insights_v1.md`. They use no health claims, no framework vocabulary, and no invented data.

3. **`HUMMUS_INSIGHT_LINES` (desktop hero):** Updated to use category-level fallback lines rather than `productInsightLines(products)`, since grade-based insightLines are not suitable for the rotating category headline section. The `productInsightLines` call was removed.

**Files changed:**
- [hummus-comparison-page-data.ts](src/lib/comparisons/hummus-comparison-page-data.ts)
- [hummus-comparison-page.tsx](src/components/comparisons/hummus-comparison-page.tsx)

**Pending:** Full content integration from `hummus_insights_v1.md` (Content Agent, TASK-067 output).

---

## Blocker 3 — Hero/Prologue Copy: Replaced

**Issue:** Hero title "חומוס: 69 מוצרים — לא כולם מה שהם נראים" was weak, off-brand, and clickbait-adjacent. Prologue contained grammar error ("בארי הערכה" — noun used as verb) and referenced ministry warning labels as a primary scoring factor (TASK-064 B-2, B-3 blocking corrections).

**Fix:** Applied all TASK-069 directed copy and TASK-064 blocking corrections.

**Hero title:**
| v1 | v2 |
|----|----|
| "חומוס: 69 מוצרים — לא כולם מה שהם נראים" | "חומוס וממרחים: מה באמת יש במדף?" |

**Prologue sentences (4 sentences, replacing 3):**
1. "בדקנו 69 מוצרי חומוס וממרחים הנמכרים בשופרסל — לפי הרכב המוצר, רשימת הרכיבים, סימוני האריזה ומבנה המוצר." *(TASK-069 suggested subtitle)*
2. "הקטגוריה כוללת ממרחי חומוס, מטבוחה, ממרח חצילים, ממרח פלפלים ומסבחה."
3. "61 מוצרים מקבלים ציון; שני מוצרים אינם מוצגים עם ציון בשל היעדר נתוני תזונה." *(updated count after exclusion)*
4. "ערכי השומן אינם מוצגים בקטגוריה זו בשל מגבלות באיכות מקור הנתונים." *(TASK-069 suggested caveat; also TASK-064 mandatory disclosure)*

**Methodology line 1** (B-3 fix — remove ministry warning label as primary factor):
| v1 | v2 |
|----|----|
| "...ועמידה בסמני האזהרה של משרד הבריאות הישראלי." | "...ומדדים נוספים הנוגעים למבנה המוצר." |

**Metadata line:**
| v1 | v2 |
|----|----|
| "69 מוצרים נבדקו · ..." | "63 מוצרים בדירוג · ..." |

**Files changed:**
- [hummus-comparison-page-data.ts](src/lib/comparisons/hummus-comparison-page-data.ts)
- [hummus-comparison-page.tsx](src/components/comparisons/hummus-comparison-page.tsx) (HUMMUS_INSIGHT_LINES updated)

---

## Addendum — Hummus Not Listed on /hashvaot Hub

**Issue (discovered during TASK-069):** `/hashvaot/hummus` was reachable by direct URL but had no entry on the `/hashvaot` comparison hub. The page was invisible to organic navigation.

**Fix:**
1. Created [featured-hummus-intelligence-card.tsx](src/components/hashvaot/featured-hummus-intelligence-card.tsx) — follows the same pattern as `FeaturedYogurtsIntelligenceCard`. Uses `hummusCorpusMeta`, `hummusProducts`, and `hummusPrologueSentences` for live stats. Hardcodes `HUMMUS_CARD_INSIGHT_LINES` (category-level, not product-level).
2. Added `FeaturedHummusIntelligenceCard` to `/hashvaot/page.tsx` in the "ניתוח עדכני" section with route `/hashvaot/hummus`.

**Files changed:**
- [featured-hummus-intelligence-card.tsx](src/components/hashvaot/featured-hummus-intelligence-card.tsx) *(new)*
- [src/app/hashvaot/page.tsx](src/app/hashvaot/page.tsx)

---

## Blocker 4 — Build and Verification

**Build:** `npm run build` — ✓ Passed. All 30 static pages generated. TypeScript clean. No warnings.

**Route verified:** `/hashvaot/hummus` renders. `/hashvaot` links to it.

**No duplicate or legacy routes created.** The existing `/hashvaot/hummus` route was unchanged. Only the hub listing was added.

---

## Screenshots

All screenshots saved to `bari/screenshots/`:

| File | Content |
|------|---------|
| `hummus_hero_desktop.png` | Desktop view — new hero title, prologue, stats |
| `hummus_product_list_desktop.png` | Desktop — stats area showing 69 / 67 / 63 counts; prologue sentences |
| `hummus_expanded_row_desktop.png` | Desktop — first product expanded (desktop view) |
| `hummus_mobile.png` | Mobile — product list, first product expanded, bottomLine visible: "ציון 80 (A) — מבנה הרכב חזק ביחס לממרחים האחרים בקטגוריה." |
| `hashvaot_hub_hummus.png` | /hashvaot hub — hummus card visible at bottom of "ניתוח עדכני" section |

---

## Remaining Content Gap (Not a Launch Blocker)

Product-specific insight lines from `hummus_insights_v1.md` have not been integrated into the frontend JSON. Expansion content currently shows grade-level fallback bottomLines. When the Content Agent integrates the per-product insight lines, the `insightLine` and expansion `bottomLine` fallback code in `hummus-comparison-page-data.ts` can be replaced. The component flag in `hummus-comparison-page.tsx` should also be reverted to use `productInsightLines(products)` at that point.

---

*Frontend Agent — TASK-069 — 2026-05-31*
