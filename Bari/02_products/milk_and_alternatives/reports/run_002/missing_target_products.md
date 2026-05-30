# Missing Target Products — Run 002

**Context:** The golden_candidates.md (run_001 planning) defined 13 adversarial archetypes (G01–G13). This report documents which were found as real products on Yohananof and which are missing.

---

## Coverage Matrix

| Archetype | Target Description | Found? | Real Barcode | Notes |
|-----------|-------------------|--------|--------------|-------|
| G01 | Whole dairy milk 3.5% | **YES** | 7290000051352 | Tnuva 3.8% full milk |
| G01b | Alternative whole dairy | **YES** | 7290019790259 | Golan Hights 4% natural |
| G02 | High-protein dairy (intact) | **PARTIAL** | 7290114313865 | LF enriched; prot=6.5g. Not exactly G02 (no direct intact-protein-only product) |
| G03 | Ultra-low-calorie almond milk | **YES** | 5411188112709 | Alpro almond no sugar, 15 kcal/100ml ✓ |
| G04 | Barista almond milk | **NOT FOUND** | — | No barista almond variant on Yohananof in this run |
| G05 | Unsweetened soy milk | **YES** | 7290110324926 | ללא תוספת סוכר, 32 kcal ✓ |
| G06 | Sweetener-added soy milk | **NOT FOUND** | — | Expected stevia-sweetened soy; found only "ללא סוכרים" (7290116936116) which is plain, not sweetened with stevia |
| G07 | High-protein dairy (enriched) | **YES** | 7290114313865 | LF + protein enriched, 6.5g/100ml ✓ |
| G08 | Protein-enriched almond (isolate) | **NOT FOUND** | — | No pea-isolate-enriched almond milk found on Yohananof |
| G09 | No-sugar-added oat with stevia | **PARTIAL** | 7394376620904 | Oatly no-sugar oat (0g sugar) but ingredients show no stevia — uses enzymatic processing |
| G10 | Plain unsweetened oat | **YES** | 7290110325619 | Tnuva oat drink, simple formulation ✓ |
| G11 | Barista oat milk | **YES** | 7394376619939 | Oatly barista ✓ |
| G12 | Chocolate dairy milk | **NOT SCRAPED** | — | Discovered in search (13 candidates) but filtered from priority scrape; available in full corpus |
| G13 | Kids dairy drink | **NOT SCRAPED** | — | Not searched specifically in this run; requires dedicated query |

---

## Summary

| Status | Count | Target archetypes |
|--------|-------|-------------------|
| Found ✓ | 7 | G01, G03, G05, G07, G10, G11, G01b |
| Partial | 2 | G02 (no isolated intact-protein product), G09 (enzymatic not stevia) |
| Not found on Yohananof | 3 | G04 (barista almond), G06 (stevia soy), G08 (isolate almond) |
| Not scraped (available) | 2 | G12 (chocolate milk), G13 (kids drink) |

---

## Missing Products Detail

### G04 — Barista Almond Milk
**What was searched for:** A barista/frothing almond milk variant  
**Why not found:** No barista almond product appeared in any of the 17 discovery queries. Yohananof appears to stock plain almond milk only.  
**Implication for BSIP2 testing:** Cannot run the "almond barista vs plain almond" comparison. The barista modifier test was run with soy barista (Alpro, barcode 7290119385560) instead.

### G06 — Stevia-Sweetened Soy Milk
**What was searched for:** A soy milk using non-nutritive sweetener (stevia) to maintain sweetness without sugar  
**Why not found:** The only no-sugar soy drinks found (7290110324926, 7290116936116) use neither sugar nor stevia — they are naturally low-sugar soy extracts. The simulated run_001 used Alpro oat with stevia (barcode 5411188004001) to test this archetype, but no real stevia-sweetened soy was found.  
**Implication:** The sweetener taxonomy gap (RISK 4 from run_001) cannot be tested with soy specifically. The Oatly no-sugar oat (7394376620904) with sugar=0 provides a partial proxy.

### G08 — Pea Isolate-Enriched Almond Milk
**What was searched for:** An almond milk enriched with pea protein isolate (the key "protein quality exploit" test)  
**Why not found:** Not available on Yohananof in the milk/alternative beverage category.  
**Implication:** The protein source factor (whole_food=1.0 vs isolate=0.70) cannot be directly tested with almond milk against plain almond. This test was partially covered by the lactose-free enriched dairy (7290114313865) which uses dairy protein concentrate.

---

## Discovered but Not Scraped (Available in Full Corpus)

### Chocolate Dairy Milk (13 candidates)
Discovered via query "חלב שוקולד". Full list available in `all_approved_candidates_full.json`. Represents the NOVA 4 hyper-palatability archetype. Recommended for next scraping run.

### Kids Dairy Drink
Not specifically queried in this run. A dedicated query ("חלב לילדים", "ממותק ילדים", brand names like "Prigat") would be needed.

---

## Recommendations for Next Run

1. **Add query:** "חלב שוקולד" with ≥3 chocolate milk products (covers G12)
2. **Add query:** "משקה שקדים בריסטה" or specific barista almond brand names (covers G04)
3. **Add query:** "חלב ילדים" / "ממותק" (covers G13)
4. **Check:** Whether any Israeli protein-enriched almond drinks exist (covers G08) — may be a Carrefour-exclusive category
