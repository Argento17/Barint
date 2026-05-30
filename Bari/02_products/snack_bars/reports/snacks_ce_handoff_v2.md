# Snacks CE Handoff v2 — Product-Live Readiness
**Built:** 2026-05-29  
**Status:** Implementation complete. Cursor: verify + deploy.

---

## What Changed (CE decisions, not Cursor decisions)

### Corpus: 14 → 18 displayable products

**Removed (2):**
- snk-008 (פיטנס שוקולד בננה) — near-duplicate of snk-007 (≤7pt gap, same archetype, no editorial gain)
- snk-014 (חטיף אנרג'י אגוזים ושוקולד) — unverifiable; not found in BSIP2 run data; violates data integrity rule

**Replaced (2) — old snk-015/016 were placeholder "insufficient" products:**
- snk-015: חטיף תמרים במילוי חמאת בוטנים (55/C, NOVA2) — sibling to snk-001, editorial: 15pt gap from peanut vs almond butter
- snk-016: מרבה סלים טופינג אגוזי לוז (51/C, NOVA3) — extends Slim brand coverage

**Added (4):**
- snk-017: נייצ'ר וואלי צ'ואי שוקולד מריר (39/D) — NV Chewy vs NV Protein intra-brand comparison
- snk-018: קראנצ'י שיבולת שועל עם חתיכות שוקולד (46/D) — same brand as snk-003, chocolate variant shows 7pt cost
- snk-019: חטיפי פיטנס שיבולת שועל דבש (41/D) — "oat+honey" naming vs processed reality
- snk-020: מרבה סלים דליס קריספי אוכמניות (32/E) — Slim brand reaching E, editorial paradox

**Children's exclusion:** מרבה סלים דליס לילדים (52/C) — EXCLUDED per Section 2.8 (name contains "לילדים")

---

## Files Changed

| File | Change |
|---|---|
| `src/data/comparisons/snacks_frontend_v2.json` | Complete rewrite: 18 products, all expansion fields, limitingFactors added, NOVA removed |
| `src/lib/comparisons/snack-types.ts` | SnackFilterId type: removed NOVA/processing filters, added oat-cereal/wellness/grade-e |
| `src/lib/comparisons/snack-page-data.ts` | Products updated, SNACK_FILTERS updated, snackMatchesFilter rewritten, NOVA text cleaned |
| `src/lib/comparisons/snacks-shelf-filters.ts` | Exclude type simplified (NOVA filter IDs removed) |
| `src/lib/blog/snack-analysis-content.ts` | Methodology line 2: now mentions 18 displayed |
| `src/lib/comparisons/snacks-comparison-page-data.ts` | Prologue updated: "53 מוצרים" → accurate 18-of-53 framing |
| `src/components/snack/snack-shelf-stat-bar.tsx` | Removed NOVA4% stat, added "18 מוצגים" stat |

---

## Final Product Order (score descending)

| # | ID | Product | Score | Grade |
|---|---|---|---|---|
| 1 | snk-001 | חטיף תמרים במילוי חמאת שקדים | 70 | B |
| 2 | snk-004 | מרבה סלים דליס שוקולד מריר | 58 | C |
| 3 | snk-002 | חטיף תמרים בציפוי שוקולד 100% קקאו | 56 | C |
| 4 | snk-015 | חטיף תמרים במילוי חמאת בוטנים | 55 | C |
| 5 | snk-003 | קראנצ'י שיבולת שועל עם דבש | 53 | C |
| 6 | snk-016 | מרבה סלים טופינג אגוזי לוז | 51 | C |
| 7 | snk-009 | נייצ'ר וואלי פרוטאין בוטנים ושוקולד | 47 | D |
| 8 | snk-005 | חטיפי דגנים פיטנס קלאסי | 46 | D |
| 9 | snk-018 | קראנצ'י שיבולת שועל עם חתיכות שוקולד | 46 | D |
| 10 | snk-010 | נייצ'ר וואלי פרוטאין בוטנים קרמל מלוח | 45 | D |
| 11 | snk-011 | פרי מארז תמרים ואגוזי לוז | 43 | D |
| 12 | snk-012 | פרי מארז תמרים ושברי קקאו | 42 | D |
| 13 | snk-019 | חטיפי פיטנס שיבולת שועל דבש | 41 | D |
| 14 | snk-017 | נייצ'ר וואלי צ'ואי שוקולד מריר | 39 | D |
| 15 | snk-020 | מרבה סלים דליס קריספי אוכמניות | 32 | E |
| 16 | snk-007 | חטיפי דגנים פיטנס שוקולד מריר | 29 | E |
| 17 | snk-006 | פיטנס בר גרנולה שוקולד מריר | 17 | E |
| 18 | snk-013 | שחור ולבן קורני שוקולד | 13 | E |

---

## Shelf Filters (4 CE-approved lens options)

| Filter ID | Label | Matching Logic | Count |
|---|---|---|---|
| date-based | תמרים/טבעי | positioning === "טבעי/תמרים" | 5 |
| oat-cereal | שיבולת שועל ודגנים | cluster_id in [granola-oat, fitness] | 7 |
| wellness | מיצוב בריאות | positioning in [פרוטאין, פיטנס] | 10 |
| grade-e | ציון E | grade === "E" | 4 |

Note: "הכל" (all) is always shown first by the shelf component. These 4 are the content lenses.

---

## Expansion Schema (all 18 products)

All products in snacks_frontend_v2.json now have:
- `positiveSignals` — actual compositional positives only (no limiting factors misclassified here)
- `limitingFactors` — new field, was missing from all products
- `bottomLine` — distinct from insightLine (synthesis, not hook)
- `comparisonContext` — cluster placement in Hebrew
- `insightLine` — no NOVA terminology

---

## NOVA Terminology Cleanup

Removed from all shelf-facing fields:
- `insightLine` strings: NOVA references replaced with "עיבוד מרבי" / "עיבוד בינוני"
- `key_observation_he` in snack-page-data.ts: same replacements
- `explainability_tags`: "NOVA4" → "עיבוד מרבי", "NOVA3" → "עיבוד בינוני"
- `snackExplainabilityLegend`: replaced NOVA4/הנדסת טעם with עיבוד מרבי/עיבוד בינוני/סוכר גבוה
- `snackGlossary`: NOVA4 entry → "עיבוד מרבי" entry
- `SNACK_FILTERS`: removed nova2/nova3/nova4 filter IDs entirely
- `SNACK_REPORT_STATS`: removed nova4Pct, added displayed: 18
- `SnackShelfStatBar`: removed "X% NOVA4" stat, added "18 מוצגים"

NOVA terminology RETAINED (engine/blog routes only, not shelf):
- `filter-panel.tsx` engine toggle
- `snack-product-detail.ts` engine detail
- `map-section.tsx` engine map

---

## Cursor Verification Checklist

1. `tsc --noEmit` — must pass with zero errors
2. Navigate to `/hashvaot/snacks` — confirm 18 products visible
3. Stat bar shows: "53 נסרקו | 48 קיבלו ציון | 18 מוצגים" (no "NOVA4")
4. Filter bar shows exactly 4 lenses: תמרים/טבעי | שיבולת שועל ודגנים | מיצוב בריאות | ציון E
5. snk-001 first at top, snk-013 last
6. snk-015 (חמאת בוטנים) visible at position 4
7. Expansion panel on any product shows positiveSignals AND limitingFactors
8. No "NOVA4", "NOVA3", "NOVA2" text visible anywhere on /hashvaot/snacks

---

## What Cursor Should NOT Do

- Do not reorder products (order is score-descending, pre-computed)
- Do not invent product details or fill in null nutrition values
- Do not add snk-008 or snk-014 back
- Do not add new filter IDs beyond the 4 CE-approved ones
- Do not display limitingFactors with negative framing in the UI (no red/warning colors — these are observations, not penalties)
