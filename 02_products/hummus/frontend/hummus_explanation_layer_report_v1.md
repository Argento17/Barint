# Hummus Explanation Layer — Implementation Report

**Task:** TASK-086 (implements TASK-085 BSIP2 → Web Translation Contract)
**Owner:** Product Agent (impl) · **Date:** 2026-05-31
**Status:** BUILT — typecheck + Next build + lint all green
**Scope:** Explanation-layer only. No score / grade / ranking / scoring changes. No new categories.

---

## What changed

| Layer | File | Change |
|---|---|---|
| Schema | `bari/src/lib/view-models/index.ts` | `BariExpansionVM` gains `unknowns?: string[]` and `caveats?: string[]` (`positiveSignals`/`limitingFactors`/`confidence` already existed) |
| Translation | `02_products/hummus/frontend/build_hummus_explanation_v1.py` | NEW deterministic generator: BSIP2-trace + BSIP1 signals → the 4 arrays |
| Dataset | `hummus_frontend_v3.json` (workspace + `bari/src/data/comparisons/`) | v2 + the 4 arrays per product; everything else byte-identical to v2 |
| Page data | `bari/src/lib/comparisons/hummus-comparison-page-data.ts` | Removed `GRADE_INSIGHT_FALLBACK` + `GRADE_BOTTOM_LINE`; imports v3 |
| Filters | `bari/src/lib/comparisons/hummus-shelf-filters.ts` | Imports v3 |
| UI | `bari/src/components/shared/expansion-section.tsx` (mobile) and `bari/src/components/comparisons/bari-product-shelf-row.tsx` (desktop) | Render `מה שלא ניתן לאמת` (unknowns) + `הערות` (caveats); both hide when empty |

**Section mapping** (task headers → rendered sections):
`מה בלט` = `positiveSignals` (existing "מה עובד לטובת המוצר?" section), `מה הגביל` = `limitingFactors` (existing "מה מגביל את הציון?"), `מה לא ניתן לאמת` = `unknowns` (NEW "מה שלא ניתן לאמת"), `הערות` = `caveats` (NEW).
The positive/limiting section labels were left unchanged because the same shared components render bread, maadanim, snacks, and yogurts; the two genuinely-new sections are added gated on array presence, so those four live categories are unaffected.

## Determinism

The 4 arrays are a pure function of structured signals — `caps_applied`, `penalties_applied`, `extracted_additives`, `extracted_sweeteners`, `protein_g`, `sodium_mg`, `dietary_fiber_g`, `nova_confidence_band`, `data_sufficiency`, `unresolved_flags` — through a fixed phrase table. No LLM copy; re-running reproduces byte-identical output. Framework vocabulary (NOVA/cap/floor/dimension/BSIP) never appears in output strings; the processed-structure cap is translated to "מבנה רכיבים מעובד".

## Coverage (67 scored displayed products)

`positiveSignals` 67/67 · `limitingFactors` 61/67 (6 genuinely clean) · `unknowns` 67/67 (fat line always) · `caveats` 6 (partial-data / low-confidence products). No scored product relies on generic grade text (verified: 0 occurrences in v3).

---

## Before / After — 5 products

"Before" = the page injected a per-grade `bottomLine` (e.g. `ציון 64 (C) — הרכב מציג היבטים לעיון ביחס לממרחים האחרים בקטגוריה.`) and, when an insightLine was missing, the per-grade `GRADE_INSIGHT_FALLBACK`. Both are generic-to-the-grade. The expansion had **no** what-helped / what-limited / what-unknown breakdown.

### 1. סלט חומוס — `bsip1_6666307` — 80 / A (hummus_spread)
**Before** — expansion: `בשורה התחתונה: ציון 80 (A) — מבנה הרכב חזק ביחס לממרחים האחרים בקטגוריה.` *(same sentence as every other A)*
**After**
- **מה שבלט:** חלבון גבוה לקטגוריה — 18.2 גרם ל-100 גרם · רשימת תוספים קצרה — תוסף מזון יחיד מעבר לבסיס
- **מה שהגביל:** חומר משמר אחד מופיע ברשימה — תוספת בודדת על בסיס פשוט
- **מה שלא ניתן לאמת:** ערכי השומן לא היו זמינים במקור הנתונים — מדד זה לא נכלל בניתוח.

### 2. חומוס עם טחינה אחלה — `bsip1_7290104061417` — 64 / C (hummus_spread)
**Before** — `בשורה התחתונה: ציון 64 (C) — הרכב מציג היבטים לעיון ביחס לממרחים האחרים בקטגוריה.`
**After**
- **מה שבלט:** תכולת חלבון משמעותית לקטגוריה — 7.9 גרם ל-100 גרם
- **מה שהגביל:** רשימת תוספים ארוכה — מספר תוספי מזון מעבר לבסיס
- **מה שלא ניתן לאמת:** ערכי השומן לא היו זמינים במקור הנתונים — מדד זה לא נכלל בניתוח.

### 3. סלט מטבוחה — `bsip1_7290010931330` — 62 / C (matbucha)
**Before** — `בשורה התחתונה: ציון 62 (C) — הרכב מציג היבטים לעיון ביחס לממרחים האחרים בקטגוריה.`
**After**
- **מה שבלט:** בסיס ירקות מבושל — עגבניות ופלפל *(מבושל, never קלוי — TASK-064 B-6)*
- **מה שהגביל:** מספר תוספי מזון ברשימה — חומר משמר ותוסף נוסף מעבר לבסיס · סוכר מצוין ברשימת הרכיבים — תוספת סוכר על בסיס ירקות
- **מה שלא ניתן לאמת:** ערכי השומן לא היו זמינים במקור הנתונים — מדד זה לא נכלל בניתוח.

### 4. מטבוחה אמיתית — `bsip1_7290106577572` — 49 / D (matbucha, caveated)
**Before** — `בשורה התחתונה: ציון 49 (D) — חששות מבניים ביחס לממרחים האחרים בקטגוריה.`
**After**
- **מה שבלט:** בסיס ירקות מבושל — עגבניות ופלפל
- **מה שהגביל:** מספר תוספי מזון ברשימה — חומר משמר ותוסף נוסף מעבר לבסיס · סוכר מצוין ברשימת הרכיבים — תוספת סוכר על בסיס ירקות
- **מה שלא ניתן לאמת:** ערכי השומן לא היו זמינים במקור הנתונים — מדד זה לא נכלל בניתוח.
- **הערות:** ציון מבוסס על נתונים חלקיים

### 5. הקיסר חומוס ענק — `bsip1_7290018359686` — 80 / A (canned, unverified list)
**Before** — `בשורה התחתונה: ציון 80 (A) — מבנה הרכב חזק ביחס לממרחים האחרים בקטגוריה.`
**After**
- **מה שבלט:** תכולת חלבון משמעותית לקטגוריה — 7 גרם ל-100 גרם · סיבים תזונתיים — 6 גרם ל-100 גרם
- **מה שהגביל:** מבנה רכיבים מעובד — מעבר לממרח בסיסי
- **מה שלא ניתן לאמת:** ערכי השומן לא היו זמינים במקור הנתונים — מדד זה לא נכלל בניתוח. · פירוט הרכיבים המלא לא אומת — לא ניתן לאשר נוכחות או היעדר חומר משמר.

*(Note on #5: because the ingredient text is marketing copy, not a verified list (TASK-064 R-2), no additive/sugar claim is derived from it — the limiter comes only from the scoring cap, and the unverified-list note is surfaced under "מה שלא ניתן לאמת". The same guard prevents a false "clean list" claim on the no-text Batch-3 products.)*

---

## Build verification

| Check | Result |
|---|---|
| `tsc --noEmit` | ✅ exit 0 |
| `next build` | ✅ exit 0 — `/hashvaot/hummus` statically generated |
| `eslint` (changed files) | ✅ exit 0 |
| Ranking order v2 vs v3 | ✅ identical |
| score / grade / confidence / insightLine / name / nutrition v2 vs v3 | ✅ 0 diffs |
| Generic fallback occurrences in v3 | ✅ 0 |
| `≥1` of positiveSignals/limitingFactors on every scored product | ✅ asserted in build |

## Out of scope (deferred, noted for the record)
- The non-ranked "raw chickpeas" informational section from TASK-085 §1 is a separate frontend build; existing boundary handling (`EXCLUDED_NOVA1_IDS`) is unchanged here. The two canned chickpeas remain in the ranked set as before, now with honest unverified-list unknowns.

---

*TASK-086 — Product Agent — 2026-05-31 — implements bsip2_to_web_translation_contract_v1.md*
