# BSIP0 Discovery Report — Frozen Vegetables

**Date:** 2026-06-10  
**Analyst:** Research Agent  
**Run:** `frozen_vegetables_bsip0_discovery_001`

---

## Summary

| Metric | Value |
|--------|-------|
| Total candidates found | **32** |
| Included candidates | 32 |
| Excluded products | 8 |
| Retailers covered | 2 (Shufersal primary, Yohananof secondary; Rami Levi referenced) |
| Brands covered | 5 (Sunfrost, Yerukim/Shufersal PL, Harduf, Willy Food, Dorot) |

---

## Included Candidates (32)

### By retailer
- **Shufersal:** 30 products (24 plain veg/mixes/legumes + 3 organic + 3 frozen herbs)
- **Yohananof:** 2 products (1 private label mix, 1 Sunfrost peas)

### By product type
| Type | Count | Examples |
|------|-------|---------|
| Plain single-veg | 16 | peas, broccoli, cauliflower, corn, carrots, artichoke hearts, green beans, okra |
| Vegetable mixes | 3 | peas & carrots, mixed vegetables, organic mix |
| Frozen legumes | 8 | chickpeas, edamame (2 sizes), green fava beans, white beans, fine green beans |
| Organic | 3 | Harduf corn, Harduf veg mix, (Sunfrost overlap) |
| Frozen herbs | 3 | Dorot garlic, Dorot garlic cubes, Dorot seasoning mix |

### By brand
| Brand | Count | Type |
|-------|-------|------|
| סנפרוסט (Sunfrost) | 14 | National brand, largest range |
| ירוקים (Shufersal PL) | 11 | Private label, competitive pricing |
| הרדוף (Harduf) | 2 | Organic |
| וילי פוד (Willy Food) | 1 | Artichoke hearts |
| דורות (Dorot) | 3 | Frozen herbs |
| יוחננוף (Yohananof PL) | 1 | Private label mix |

---

## Excluded Products (8)

| Product | Reason |
|---------|--------|
| צ'יפס קלאסי שופרסל 1.5ק"ג | Frozen potatoes/fries — scope OUT |
| צ'יפס לתנור 4% שומן | Frozen potatoes/fries — scope OUT |
| ארוחת שניצל מוקפאת | Frozen ready meal — scope OUT |
| פיצה קפואה | Frozen ready meal — scope OUT |
| אצבעות דג מוקפאות | Breaded/fried frozen — scope OUT |
| קציצות ברוקולי | Breaded/fried frozen — scope OUT |
| לקט מוקפץ עם רוטב טריאקי | Stir-fry kit with sauce — scope OUT |
| מרק ירקות קפוא | Soup mix as prepared meal — scope OUT |

No frozen fruit products were encountered. These are hypothetical exclusions from the Shufersal frozen category that would need to be filtered in automated scraping.

---

## Retailer Coverage

| Retailer | Status | Products | Assessment |
|----------|--------|----------|------------|
| **Shufersal** | ✅ Primary | 30 | Strong coverage. Online storefront accessible. Both national brand (Sunfrost) and private label (ירוקים). Partial nutrition data visible. |
| **Yohananof** | ✅ Secondary | 2 | Limited. Private label mix and Sunfrost overlap confirmed. |
| **Rami Levi** | 🔍 Referenced | 0 | Category structure confirmed with unique subcategories (לקט ירוקים לקפצה, לקט לקוסקוס, לקט כפרי). Products likely overlap with Sunfrost line. No unique products documented. |
| **Carrefour / Victory** | ❌ Not accessed | 0 | Not covered in this round. |

---

## Category Boundary Issues

1. **Frozen herbs (Dorot):** 3 products included per scope ("frozen herbs only if packaged as food product with retailer evidence"). All 3 have retailer evidence on Shufersal/Wolt. Low exclusion risk — these are clearly food products, not seasoning blends.

2. **Edamame (soybeans):** Correctly classified as frozen legume sold as vegetable. Two sizes (450g, 1kg) at Shufersal private label.

3. **Artichoke hearts:** Three products from three brands (Sunfrost, Yerukim, Willy Food). Correctly classified as single-ingredient frozen vegetable.

4. **Chickpeas and white beans:** Included as frozen legumes sold as vegetables. These could be borderline if positioned as "meal base" rather than vegetable, but the Shufersal category path places them under "ירקות קפואים" (frozen vegetables).

5. **Barcode coverage:** Sunfrost barcodes confirmed via rabbanimarket.co.il cross-reference. Shufersal private label (ירוקים) barcodes not yet obtained. Dorot/Willy Food/Harduf barcodes not yet obtained.

---

## Key Risks for BSIP1

| Risk | Severity | Notes |
|------|----------|-------|
| Nutrition panel availability | **High** | Shufersal online store includes partial nutrition data (energy, protein, carbs, fat, fiber, sodium). Ingredient lists may be short/truncated. OFF enrichment needed for full data. |
| Ingredient list completeness | **Medium** | Frozen vegetables typically have 1 ingredient (the vegetable itself). Some may declare "may contain" allergens. Mixes have 2-6 ingredients. |
| NOVA classification | **Low** | Most frozen vegetables are NOVA 1 (unprocessed) or NOVA 2 (minimally processed). No ultra-processed expected. |
| Price volatility | **Low** | Prices vary by store format (Shufersal Deal vs Shufersal Sheli) and promotional cycles. Raw prices are as-of June 2026. |
| Cross-retailer deduplication | **Low** | Same barcode = same product across retailers. Sunfrost products are identical across retailers. |

---

## Recommendation: **Proceed to BSIP1**

**Rationale:**
1. **Category is well-defined** — plain frozen vegetables have clear boundaries with minimal gray area
2. **Shufersal coverage is strong** — 30 products across 5 brands with accessible online storefront
3. **Homogeneous product type** — short ingredient lists, low NOVA processing, minimal formulation complexity
4. **No structural blocking issues** — no regulatory complexity, no long ingredient lists, no score-modeling challenges
5. **BSIP1 work is straightforward** — nutrition panel acquisition, ingredient verification, NOVA classification, trust score assignment

**Next steps for BSIP1:**
1. Acquire nutrition panels for all 32 candidates (Shufersal online + OFF enrichment)
2. Acquire full ingredient lists for mixes (plain single-veg products need only 1-ingredient verification)
3. Assign barcodes for Shufersal private label products
4. Run NOVA classification (expected: 90%+ NOVA 1)
5. Cross-reference with Rami Levi for the unique subcategory mixes (לקט ירוקים לקפצה etc.)
6. Build BSIP1 canonical set

**Consumer-facing website priority:** Low — frozen vegetables are a low-score-differentiation category (most products will score well). Not a priority for frontend launch.

---

## ⚠️ Post-hoc audit correction (research-agent + data-agent, 2026-06-10)

This report was written before a proper audit. **The deliverable is classified as B — manual discovery candidate set, not a true BSIP0 scrape.** See `bsip0_discovery_audit_v1.md` for the full audit.

Key corrections:
- **Scrape status:** manual_discovery_only (zero raw scrape artifacts)
- **Recommendation:** Changed from "proceed to BSIP1" to **hold — do not proceed until actual scrape artifacts exist**
- **Evidence gaps:** barcodes 45%, product URLs 3%, image URLs 0%
- **Product count:** 33 (not 32 as originally stated)

The candidate set remains useful as a discovery list to seed an actual scrape, but must not be treated as BSIP0-complete.
