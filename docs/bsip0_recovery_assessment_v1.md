# BSIP0 Recovery Assessment v1

**Date:** 2026-05-29  
**Asset root:** `C:\Bari\02_products\snack_bars\observations_bsip0\yohananof\`  
**Scope:** Recoverability of nutrition and ingredients for the 18 `/hashvaot/snacks` products

---

## Corpus inventory (full Yohananof scrape)

| Asset | Count / 48 products |
|-------|---------------------:|
| Product directories | 48 |
| `nutrition.html` | **48** (100%) |
| `ingredients.html` | **48** (100%) |
| `product.json` (parsed) | **48** (100%) |
| Audit `usable_raw` | 39 (81%) |
| Audit `partial_raw` | 9 (19%) |

Source: `observations_bsip0/yohananof/audit_report.json`

---

## Shelf cohort coverage (18 displayed products)

### Summary

| Metric | Count |
|--------|------:|
| BSIP0 yohananof folder + parsed `product.json` | 16/18 |
| BSIP0 `nutrition.html` present | 16/18 |
| BSIP0 `ingredients.html` present | 16/18 |
| BSIP1 canonical (any retailer) | **18/18** |
| BSIP1 yohananof-only | 17/18 |

### Per-product matrix

| ID | Product | Barcode | nutrition.html | ingredients.html | product.json parsed | Audit status | Notes |
|----|---------|---------|:--------------:|:----------------:|:-------------------:|--------------|-------|
| snk-001 | חטיף תמרים חמאת שקדים | 7290011498870 | ✓ | ✓ | ✓ | usable_raw | 92 kcal/100g suspicious — see quality |
| snk-002 | תמרים ציפוי קקאו | 7290011498948 | ✓ | ✓ | ✓ | usable_raw | |
| snk-003 | קראנצ'י שיבולת דבש | 16000548404 | ✓ | ✓ | ✓ | usable_raw | |
| snk-004 | סלים דליס שוקולד מריר | 8423207206495 | ✓ | ✓ | ✓ | usable_raw | |
| snk-005 | פיטנס קלאסי | 5900020039590 | ✓ | ✓ | ✓ | usable_raw | Long ingredient list (501 chars) |
| snk-006 | פיטנס בר גרנולה | 7290118427858 | ✗ | ✗ | ✗ | not in scrape | Carrefour-only; BSIP1 has full data |
| snk-007 | פיטנס שוקולד מריר | 5900020015174 | ✓ | ✓ | ✓ | usable_raw | |
| snk-009 | NV פרוטאין בוטנים שוקולד | 8410076610379 | ✓ | ✓ | ✓ | usable_raw | |
| snk-010 | NV פרוטאין קרמל מלוח | 8410076610386 | ✓ | ✓ | ✓ | usable_raw | |
| snk-011 | פרי מארז תמרים לוז | 7290111936784 | ✓ | ✓ | ✓ | usable_raw | |
| snk-012 | פרי מארז תמרים קקאו | 7290111937262 | ✓ | ✓ | ✓ | usable_raw | |
| snk-013 | קורני שחור לבן | 4011800633516 | ✓ | ✓ | ✓ | usable_raw | |
| snk-015 | תמרים חמאת בוטנים | 7290011498894 | ✓ | ✓ | ✓ | usable_raw | |
| snk-016 | סלים טופינג לוז | 8423207210928 | ✓ | ✓ | ✓ | usable_raw | |
| snk-017 | NV צ'ואי שוקולד מריר | 8410076610508 | ✓ | ✓ | ✓ | usable_raw | |
| snk-018 | קראנצ'י שוקולד | 8410076602251 | ✓ | ✓ | ✓ | usable_raw | |
| snk-019 | פיטנס שיבולת דבש | 7290118427896 | ✓* | ✓* | ✓* | usable_raw | *Folder `7290118247896` (image URL barcode typo) |
| snk-020 | סלים קריספי אוכמניות | 7290014525306 | ✓ | ✓ | ✓ | partial_raw | Ingredients truncated in parse |

---

## Parsing quality assessment

### High confidence (14 products)

`usable_raw`, full nutrition basis `per_100g`, clean ingredient text, zero parser warnings. Examples: snk-003, snk-004, snk-009, snk-015.

### Medium confidence (3 products)

| Product | Issue | Recoverability |
|---------|-------|----------------|
| snk-020 | `ingredients_raw_he` truncated mid-string (`ס????`); nutrition complete | Re-parse from `ingredients.html` or use BSIP1 string (already normalized) |
| snk-005, snk-007, snk-017 | Very long ingredient lists (400–680 chars) | Usable; verify delimiter parsing only |
| snk-019 | Folder/barcode mismatch | Data valid in `7290118247896/product.json`; remap folder alias |

### Low confidence / review required (1 product)

| Product | Issue | Impact |
|---------|-------|--------|
| snk-001 | 92 kcal, 0g fat, 15.5g sugar per 100g for 76% dates | Retailer label likely **per-unit** mislabeled as per 100g. BSIP2 used this value → inflated `calorie_density` dimension. Recovery should flag for CE review, not blind copy. |

### Not recoverable from BSIP0 yohananof (1 product)

| Product | Fallback |
|---------|----------|
| snk-006 | BSIP1 Carrefour scrape: 479 kcal, 22.1g sugar, 520-char ingredients — **already in canonical layer** |

---

## HTML asset quality

`nutrition.html` and `ingredients.html` are full Yohananof modal DOM captures (MUI tab panels). Example nutrition extract (snk-001):

- אנרגיה: 92
- חלבונים: 1.6
- פחמימות: 17.6
- סוכרים: 15.5
- שומנים: 0

Parser successfully extracted these into `product.json` → BSIP1. **Re-parsing HTML is possible but redundant** given BSIP1 already normalized the same source.

---

## Recoverability verdict

| Question | Answer |
|----------|--------|
| Can nutrition be recovered for shelf products? | **Yes — 18/18** (16 from BSIP0 yohananof + 2 via BSIP1-only sources) |
| Can ingredients be recovered? | **Yes — 18/18** (snk-020 may need BSIP1 fallback for complete string) |
| Is re-scraping required? | **No** for displayed cohort |
| Best recovery source | **BSIP1** (already normalized, used by BSIP2) |
| BSIP0 role | Provenance + re-parse if BSIP1 disputed |

---

## Partial_raw products (full scrape — not all on shelf)

Nine products flagged `partial_raw` in the 48-product scrape. Only **snk-020** is on the displayed shelf. Others (e.g. `7290118427872`, `7290018333952`) are out of CE v2 display scope.

Common partial causes:
- `nutrition_missing_or_unparsed`
- `ingredients_missing_or_unparsed`
- Truncated modal capture

---

## Recommended recovery source priority

1. **BSIP1** `normalized_nutrition_per_100g` + `ingredients_text_he` — canonical, scoring-aligned
2. **BSIP0** `product.json` — same values, audit trail
3. **BSIP0** raw HTML — only if re-validation needed (snk-001 kcal, snk-020 truncation)

---

## Conclusion

BSIP0 capture is **substantially complete** for the snacks category (48/48 HTML pairs). The 18-product shelf is **recoverable without new scraping**. Two edge cases (snk-006 Carrefour-only, snk-019 folder alias) are already resolved in BSIP1. One data-quality flag (snk-001 kcal basis) should be reviewed before user-facing display, not silently ignored.
