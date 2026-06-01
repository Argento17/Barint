# Tahini — Inclusion / Exclusion Rules

**Task:** TASK-054  
**Owner:** Data Agent  
**Date:** 2026-05-31  
**Category:** Tahini  
**Version:** v1.0  
**Status:** Pre-lock draft — requires Head of Product sign-off  
**Lock statement:** This document must be explicitly locked (with date and sign-off appended below) before BSIP0 candidate review begins. All inclusion/exclusion decisions during review are made against this document.

---

## IN Scope — Approve These Products

| Product type | Hebrew name examples | Tag | Notes |
|---|---|---|---|
| Raw/natural tahini (hulled sesame) | טחינה גולמית, טחינה טבעית, טחינה משומשום קלוף | `tahini_raw` | Core. Single ingredient: ground sesame. Most common form in Israel |
| Raw tahini (whole sesame) | טחינה כל שומשום, טחינה משומשום מלא, טחינה מלאה | `tahini_raw` | Higher fiber/mineral content. Include |
| Roasted tahini | טחינה קלויה, טחינה קלויה בהירה, טחינה קלויה כהה | `tahini_raw` | Roasting is a processing step, not a reformulation |
| Organic tahini | טחינה אורגנית, טחינה ביולוגית, טחינה ביו | `tahini_raw` | Certification claim only; same product structure |
| Ready-to-eat tahini dip | טחינה מוכנה, ממרח טחינה, טחינה ביתית, סלט טחינה | `tahini_dip_prepared` | Deferred from Hummus corpus (TASK-026). Refrigerated shelf |
| Ready-to-eat tahini with garlic | טחינה עם שום, ממרח טחינה עם שום | `tahini_dip_prepared` | Garlic is a legitimate seasoning addition |
| Ready-to-eat tahini with parsley | טחינה עם פטרוזיליה | `tahini_dip_prepared` | Include |
| Ready-to-eat tahini with lemon | טחינה עם לימון | `tahini_dip_prepared` | Lemon is standard in tahini dip |
| Tahini with date | טחינה עם תמרים, טחינה עם ממרח תמרים, טחינה ותמר | `tahini_sweetened` | IN — tahini-primary, natural sweetener secondary. See EC-1 |
| Tahini with honey | טחינה עם דבש | `tahini_sweetened` | IN — tahini-primary, honey secondary. See EC-1 |
| Tahini with carob | טחינה עם חרוב, דיבס וטחינה | `tahini_sweetened` | IN — carob syrup (dibs) is a traditional natural sweetener |
| Tahini with lemon flavoring | טחינה בטעם לימון | `tahini_raw` | Minor flavoring addition only; still a raw tahini product |
| Ethiopian sesame tahini | טחינה אתיופית, טחינה מהומרה | `tahini_raw` | Premium variety; include; sourcing claim only |
| Light-roasted tahini | טחינה קלויה בהיר | `tahini_raw` | Include |
| Tahini in tube format | טחינה בטיוב | `tahini_raw` | Include; format variant, same product |
| Shufersal / Yohananof own-brand tahini | שופרסל טחינה, יוחננוף טחינה | `tahini_raw` | Store-brand products are first-class corpus members |

---

## OUT of Scope — Reject These Products

| Product type | Hebrew name examples | Reason | Hard exclude? |
|---|---|---|---|
| **Halva** | חלבה, חלווה | Confection; tahini + sugar in confection ratio | YES |
| **Halva spread** | ממרח חלבה, ממרח חלווה | Same: dessert spread with sugar co-dominant | YES |
| **Chocolate tahini spread** | טחינה שוקולד, ממרח טחינה ושוקולד, ממרח טחינה עם קקאו | Sugar + cocoa co-dominant; dessert product | YES ("שוקולד" in name) |
| **Nut butters** | חמאת בוטנים, חמאת שקדים, חמאת קשיו, חמאת אגוזים | Different primary ingredient (nut, not sesame). Wave 3 | YES ("חמאת" not "טחינה") |
| **Hazelnut-chocolate spread** | נוטלה, ממרח שוקולד ואגוזי לוז | Dessert spread; no sesame | YES ("נוטלה") |
| **Sesame oil** | שמן שומשום | Liquid oil, different format and purpose | YES ("שמן שומשום") |
| **Whole sesame seeds** | גרעיני שומשום, שומשום | Not a paste; raw ingredient | YES ("גרעיני") |
| **Sesame candy / brittle** | ממתק שומשום, קרוקנט שומשום, עוגיות שומשום | Confection; not a paste | YES ("ממתק", "קרוקנט") |
| **Sesame crackers / snacks** | קרקרים שומשום, ביסלי שומשום | Snack format, not paste | YES ("קרקר", "ביסלי", "חטיף") |
| **Sesame flour / sesame powder** | אבקת שומשום, קמח שומשום | Dry ingredient, not a spread | YES ("אבקת", "קמח") |
| **Multi-packs / party packs** | מארז טחינה ×4, מארז 3 יחידות | Pack format, not product | YES ("מארז") |
| **Catering sizes (≥ 1 kg)** | טחינה 1 ק"ג מוסדי, 5 ק"ג | Consumer retail only | YES (weight >1 kg) |
| **Single-serving sachets** | פורשן טחינה, מנת טחינה 30 גרם | No reliable per-100g panel | YES (package < 100g sachet) |
| **Ready-to-eat flatbread with tahini** | פיתה עם טחינה, לאפה בטחינה | Composite product; tahini is a component | YES ("פיתה", "לאפה") |
| **Hummus products** | חומוס עם טחינה | Already in Hummus corpus. No duplication | Cross-check barcode |
| **Pesto / olive spread** | פסטו, ממרח זיתים | Different category | YES |
| **Date paste / date spread (standalone)** | ממרח תמרים, דיבס | Sweetener product; tahini absent or minor | Only if no tahini |
| **Tahini-cooking sauce (heavily diluted)** | רוטב טחינה (10% tahini), ציר טחינה | Apply dilution test; if tahini < 20% → OUT | Apply test |

---

## Blend Rules

### BR-1 — Tahini vs. Halva

**Problem:** Both are made from sesame. Halva adds sugar in a 1:1 or higher ratio and forms a solid confection.

**Test (apply in order):**
1. Is "חלבה" or "חלווה" anywhere in the product name? → OUT, no further evaluation
2. Are declared `sugars_g > 20g/100g`? → REVIEW with BR-1b
3. BR-1b: Does the product name contain any of "מוצק", "טבלה", or similar solid-form descriptors? → OUT
4. BR-1b: Is "חלבה" present anywhere in the ingredient list? → OUT
5. If all tests pass: → IN scope (product is sweetened tahini, not halva)

**Rationale for 20g threshold:** Pure raw tahini has essentially 0g sugar. Ready-to-eat tahini dip has 0–3g from natural sesame sugars. Tahini with date/honey has 10–20g. Halva has 25–40g. A 20g threshold captures date-sweetened tahini (below threshold) while excluding halva-style products (above).

---

### BR-2 — Tahini vs. Chocolate Spread

**Problem:** "טחינה שוקולד" products appear on the same shelf as tahini. Some are chocolate dessert spreads that happen to include some tahini.

**Test:**
1. Is "שוקולד" OR "קקאו" in the product name? → Apply BR-2b
2. BR-2b: Is tahini/sesame the **first ingredient by weight** AND `sugars_g ≤ 15g`? → BORDERLINE (escalate)
3. BR-2b: Is chocolate/cocoa the first or second ingredient, or `sugars_g > 15g`? → OUT (chocolate-primary product)
4. Products meeting condition 2 (tahini-first, low sugar, chocolate as minor ingredient): include with note; these are "chocolate-flavored tahini" — a legitimate sub-type with BSIP2 glycemic penalty applied correctly

---

### BR-3 — Tahini vs. Cooking Sauces (dilution test)

**Problem:** Some products called "רוטב טחינה" are heavily diluted (10–20% tahini in water) and are essentially a condiment, not a tahini product.

**Test:**
1. Is the product name "רוטב X" or "ציר X"? → Apply dilution test
2. Dilution test: Is tahini/sesame listed as the **first ingredient**? → IN scope
3. Dilution test: Is tahini percentage declared and ≥ 20%? → IN scope
4. All others (water first, tahini far down the ingredient list): → OUT (condiment, not a tahini product)
5. If ingredient list unavailable: → REVIEW (hold; do not approve)

---

### BR-4 — Ready-to-Eat Tahini Dip vs. Hummus Corpus

**Problem:** Ready-to-eat tahini dip was shelved alongside hummus and may have been scraped during the Hummus BSIP0. These products must not be duplicated.

**Test:**
1. Check the Hummus exclusion_log (`C:\Bari\02_products\hummus\observations_bsip0\shufersal\_excluded_bsip0\exclusion_log.json`) for any entry with "טחינה מוכנה" or similar
2. For any ready-to-eat tahini dip found during Tahini acquisition: check barcode against existing Hummus canonical_bsip1/ files
3. If barcode match found: SKIP (already captured) OR re-use the Hummus observation with a category update
4. If barcode not found: proceed normally

**Note:** The hummus corpus_filter (TASK-026) explicitly excluded ready-to-eat tahini dip. They should appear in the exclusion_log. If they do not, it means they were never discovered during Hummus BSIP0 — proceed normally.

---

## BSIP0 Gate Thresholds

| Criterion | Minimum | Notes |
|---|---|---|
| Total approved products | ≥ 30 (target 45–65) | Must pass before BSIP1 |
| Nutrition coverage (kcal + protein + carbs + fat) | ≥ 85% | Higher threshold than hummus; tahini labels are standardized |
| **Fat_g plausibility check** | **≥ 90% of tahini products with fat_g > 40g** | **Critical — mandatory pre-gate audit. Tahini has ~55g fat; if fat_g < 15g for raw tahini, the Shufersal fat-row defect has fired** |
| Ingredient list coverage | ≥ 80% | Higher than hummus; single-ingredient products should have complete labels |
| Image URL availability | ≥ 90% | Standard |
| Retailer traceability | 100% | Every product has a source URL |
| Sub-type coverage | ≥ 3 sub-types represented | Raw tahini, ready-to-eat dip, at least one specialty variant |

**The fat_g plausibility check is a new mandatory gate item specific to this category.** It does not exist in the hummus gate specification but was identified as required based on TASK-039 findings. The protocol:

1. Select a random sample of 5 raw tahini products from the approved corpus
2. Compute implied fat: `(kcal − protein×4 − carbs×4) / 9`
3. For raw tahini at ~600 kcal, ~20g protein, ~20g carbs: implied fat ≈ (600 − 80 − 80) / 9 = **48.9g**
4. Accept if `fat_g > 40g` (within rounding tolerance of actual 55g)
5. Block gate if `fat_g < 20g` for any raw tahini product — this indicates fat-row capture error
6. Document results in `bsip0_gate_result.md` with per-product fat plausibility table

---

## Acquisition Risks

### Risk 1 — Shufersal fat-row scraping defect

**Severity: Critical**  
The Shufersal fat scraper captures the saturated fat sub-row ("שומן רווי") instead of total fat ("שומן") for some products (confirmed in TASK-039 for hummus). For tahini, this produces:
- Expected: `fat_g ≈ 55g` (actual total fat of raw sesame paste)
- Corrupted: `fat_g ≈ 8g` (saturated fat only)

Unlike hummus where the corrupted value (0.5g) was visibly implausible, tahini's corrupted value (8g) could pass casual inspection. The mandatory caloric gap analysis at gate is the only reliable check.

**Mitigation:** Mandatory fat plausibility check before gate passes. Do not run BSIP1 or BSIP2 if fat_g < 20g for more than 10% of raw tahini products.

---

### Risk 2 — Shelf code contamination from halva

**Severity: Medium**  
Halva products may appear on the same shelf code as tahini. Halva products often have "טחינה" in their ingredient list (since halva is made from tahini), which could cause a false-positive suggestion in the candidate review.

**Mitigation:** Hard-exclude any product with "חלבה" in the product name at the discovery stage. Apply the sugars_g > 20g secondary test during candidate review.

---

### Risk 3 — Ready-to-eat tahini dip has variable tahini concentration

**Severity: Medium**  
The tahini concentration in ready-to-eat dips ranges from 15% to 60%. Very diluted dips (< 20% tahini) are structurally equivalent to a condiment. If the scraper captures many extremely diluted products, BSIP2 scores will be compressed at the low end and the comparison will be less useful.

**Mitigation:** Apply the dilution test (BR-3) during candidate review. Reject any product where tahini percentage < 20% OR where water is declared as the first ingredient AND no tahini percentage is stated.

---

### Risk 4 — Organic tahini brands are distributed across multiple shelf locations

**Severity: Low**  
Premium organic tahini brands (Har Bracha, Adina, local producers) may be stocked in the organic/health food section rather than the primary tahini shelf. If only the primary shelf is traversed, these products will be missed.

**Mitigation:** Run targeted search queries for "טחינה אורגנית" and "טחינה ביולוגית" in addition to full shelf traversal.

---

### Risk 5 — Duplication with hummus corpus for ready-to-eat tahini dip

**Severity: Low**  
If any ready-to-eat tahini dip product was scraped during Hummus BSIP0 (despite being excluded from the hummus corpus), it would appear as a duplicate. The exclusion_log will contain the product but the barcode may match a Tahini BSIP0 discovery.

**Mitigation:** Cross-check all discovered ready-to-eat tahini dips against the hummus canonical_bsip1/ barcode index. Reuse existing BSIP0 observation files where possible (saves re-scraping); update category to "tahini" in BSIP1 conversion.

---

## BSIP Interpretation Risks

### BSIP2-IR-1 — fat_quality scores will be very high for raw tahini

Raw tahini has approximately 55g fat/100g, of which:
- ~8g saturated (15% of total fat — within whole-food acceptable range)
- ~22g monounsaturated (MUFA)
- ~25g polyunsaturated (PUFA)

Under the current `fat_quality` formula:
```
base = max(0, 100 - sat_f × 3.0 - sat_frac × 25)
     = max(0, 100 - 8×3.0 - 0.15×25)
     = max(0, 100 - 24 - 3.75) = 72.25
```

No seed oil penalty (raw sesame is a whole food, no refined oil added). Tahini should score ~72–78 on `fat_quality`.

**Why this is a risk:** The formula applies a saturated fat penalty of 3.0 per gram regardless of fat source. Sesame's saturated fat is in a whole-food matrix — it behaves differently from palm oil saturated fat. The evidence registry (EV-003, whole-food fat protection) flags this concern. The current formula does not yet implement whole-food fat protection for sesame.

**Expected impact:** BSIP2 slightly under-scores raw tahini on `fat_quality` relative to what a properly calibrated engine would produce. This is a known calibration gap, not a blocking issue. Document in the run report.

### BSIP2-IR-2 — NOVA 1 floor dominates pure raw tahini scores

Single-ingredient raw tahini (one ingredient: sesame) will be classified NOVA 1 by the engine (no additive signals, no reconstruction markers). The SRC-01 floor applies: score cannot go below 85 for NOVA 1 products with high confidence.

This means most raw tahini variants (hulled, whole, roasted, organic) will cluster at 85 regardless of minor differences. The `fat_quality`, `additive_quality`, and `nutrient_density` dimensions will not create visible differentiation within the raw tahini sub-type.

**Expected impact:** The A-grade cluster for raw tahini may be large (15–25 products at 85). This is not wrong — pure sesame paste genuinely merits grade A — but the comparison page may need sub-type filtering to show meaningful within-category comparisons.

**Mitigation:** Use the `bsip_tahini_subtype` tag to separate raw tahini from ready-to-eat tahini dip on the frontend. The ready-to-eat dip sub-type will not trigger the NOVA 1 floor (it has 3–7 ingredients, NOVA 2–3) and will produce the score differentiation users need.

### BSIP2-IR-3 — Ready-to-eat tahini dip routing conflict

Ready-to-eat tahini dip products have "טחינה" in their name, which routes them to `whole_food_fat` via the "טחינה" hard anchor. But they should route to `sauce_spread` (like the hummus category) because they are diluted preparations, not concentrated fat sources.

The TASK-044 routing fix added anchors for "מוכנה", "ממרח", "סלט" → `sauce_spread`. This should handle most ready-to-eat dip names. However, products named "טחינה ביתית" (home-style tahini) may not hit the sauce_spread anchors and may route to `whole_food_fat` incorrectly.

**Mitigation:** Pre-run router validation for ready-to-eat dip product names before BSIP2 executes. Add "ממרח טחינה" → sauce_spread anchor if not already present. Verify "טחינה מוכנה" routing.

---

## Expected Score Distribution

For planning purposes only. Not a scoring constraint.

| Product type | Expected grade | Expected score range | Key driver |
|---|---|---|---|
| Pure raw tahini (1 ingredient) | **A** | 85–90 | NOVA 1 floor |
| Organic raw tahini | **A** | 85–90 | NOVA 1 floor |
| Roasted tahini (1–2 ingredients) | **A / B** | 80–90 | NOVA 1–2; roasting = minor processing |
| Tahini with date/honey | **B** | 65–80 | Glycemic_quality penalty from sugar; no floor |
| Ready-to-eat tahini dip (simple, 3–5 ingredients) | **B** | 65–80 | NOVA 2–3; good fat quality; lower calorie density |
| Ready-to-eat tahini dip (with preservatives/emulsifiers) | **C** | 50–65 | Additive penalty; NOVA 3 |
| Heavily diluted tahini sauce (< 30% tahini) | **C / D** | 40–60 | Low fat contribution; water-diluted; lower structural integrity |

---

*Inclusion / Exclusion Rules — Tahini — TASK-054 — 2026-05-31*  
*Version v1.0 — DRAFT — NOT LOCKED*  
*Lock requires: Head of Product signature below*

**To lock this document, append:**
`*Locked by [Name] on [Date]. Version [N]. No changes permitted without a new version.*`
