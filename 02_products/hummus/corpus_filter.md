# Corpus Filter — Hummus and Savory Dips

**Version:** v1  
**Locked at:** Stage 1 gate (TASK-026)  
**Effective for:** BSIP0 candidate review  
**Date:** 2026-05-30

---

## Primary shelf

Shufersal: מזון מקורר, קפואים ונקניקים → חומוס וסלטים (A1624)

| Subcategory | Code | Scrape | Notes |
|---|---|---|---|
| סלטי חומוס וטחינה | A162406 | Full traversal | Core category |
| סלטי חצילים | A162403 | Selective | Eggplant spreads IN; pesto/tapenade OUT |
| סחוג + מטבוחה | A162408 | Selective | Matbucha IN; schug/arissa OUT |
| ממרחים מצוננים | A162405 | Optional | Pepper pastes IN; horseradish/pesto OUT |
| סלטים אחרים | A162407 | **Do not traverse** | 80% contamination — use search queries only |
| סלטי כרוב | A162404 | **Exclude** | Coleslaw, out of scope |

---

## IN scope — approve these products

| Type | Hebrew | Notes |
|---|---|---|
| Plain hummus | חומוס רגיל / ביתי | Core |
| Hummus with oil | חומוס עם שמן זית | Core |
| Hummus with pine nuts | חומוס עם צנוברים | Core |
| Whole chickpea hummus | חומוס עם שלמים | Core |
| Flavoured hummus (garlic, spicy, za'atar) | חומוס שום / חריף / זעתר | Core |
| Organic / bio hummus | חומוס אורגני / ביולוגי / ביו | Core |
| Light / low-fat hummus | חומוס קל / דל שומן / 0% | Core |
| Protein-enriched hummus | חומוס עשיר בחלבון | Include; purpose divergence note applies |
| Roasted eggplant spread | ממרח חצילים / חציליות | Secondary |
| Eggplant with tahini | חצילים בטחינה | Include |
| Roasted / fire-roasted eggplant | חצילים צלויים | Include |
| Matbucha (cooked tomato-pepper) | מטבוחה | Secondary |
| Moroccan matbucha | מטבוחה מרוקאית | Include |
| Spicy matbucha | מטבוחה חריפה | Include |
| Turkish salad (cooked tomato-pepper) | סלט טורקי | Include |
| Cooked red pepper spread | ממרח פלפל אדום | Include |
| Filfel chuma (Libyan spiced pepper) | פלפל צ'ומה | Include |
| Garlic dip (sold as a bread dip, not condiment) | ממרח שום | Approve if packaging shows it is a dip/spread; reject if it is a grilling condiment |
| Mixed vegetable spread | ממרח ירקות | Include if primary ingredients are chickpea/eggplant/pepper |

---

## OUT scope — reject these products

| Type | Hebrew | Reason |
|---|---|---|
| **Ready-to-eat tahini dip** | **סלט טחינה, טחינה מוכנה, ממרח טחינה, טחינה ביתית** | **BSIP2 routes to `whole_food_fat`, not `sauce_spread`. Defer to Tahini category. (TASK-026)** |
| Raw tahini jar | טחינה, טחינה גולמית | Separate category (whole_food_fat) |
| Tahini-hummus blend | see note below | See blend rule |
| Labane-based dips | גבינה לבנה, לאבנה | Separate category (dairy_protein, D-001 prerequisite) |
| Cream cheese / cottage | גבינת שמנת, קוטג' | Separate category |
| Schug / zhug | סחוג, זחוג | Hot condiment, not a dip |
| Harissa / arissa | חריסה, אריסה, ארוסה | Hot condiment, not a dip |
| Pesto | פסטו | Different consumer purpose |
| Olive tapenade | טפנד, ממרח זיתים | Different consumer purpose |
| Artichoke spread | ממרח ארטישוק | Different consumer purpose |
| Horseradish | חזרת | Condiment, not a dip |
| Lemon baladi | לימון בלאדי | Condiment |
| Vegetable salads | קולסלאו, גזר, סלק, כרוב, תפוח אדמה | Not a dip/spread |
| Bulgarian / Ukrainian / Korean salads | סלט בולגרי, אוקראיני | Not in scope |
| Chocolate / sweet spreads | ממרח שוקולד, נוטלה, ריבה, דבש | Wrong category entirely |
| Fish / meat spreads | ממרח דגים, פטה | Out of scope |
| Pasta sauces / ketchup | רוטב פסטה, קטשופ, חרדל, מיונז | Wrong category |
| Pickles | חמוצים, כבוש | Wrong category |
| Hummus chips / snacks | צ'יפס חומוס, חומוסיות | Wrong format (snack, not spread) |
| Multi-pack formats | מארז 3×, 4× | Exclude packaging bundles; include single units only |
| Restaurant / deli counter (sold by weight) | חומוס מסעדות (sold open-weight) | No packaged label, cannot get nutritional data |
| Catering sizes (≥1 kg) | 1 ק"ג, 1.5 ק"ג | Consumer retail scope only |

---

## Tahini-hummus blend rule (TASK-026)

When a product contains both chickpeas and tahini:

- If chickpeas appear as the **first or second ingredient** AND the product is marketed as hummus → **APPROVE**
- If tahini/sesame appears as the **first ingredient** AND the product is marketed as a tahini preparation → **REJECT** (defer to Tahini category)
- If uncertain: check the product name; "חומוס" in the name → APPROVE; "טחינה" only in the name → REJECT

---

## BSIP0 gate thresholds

| Criterion | Minimum |
|---|---|
| Total approved products | ≥ 30 (target 50–60) |
| Nutritional label coverage | ≥ 80% (calories + protein + carbs + fat) |
| Ingredient list availability | ≥ 70% |
| Product image availability | ≥ 90% |
| Retailer traceability | 100% (every product has a Shufersal or Yohananof source URL) |
| Corpus filter filed | This file |

---

## Expected score distribution (for Stage 3e validation)

| Product type | Expected grade |
|---|---|
| Plain 3-ingredient hummus (chickpea, tahini, lemon) | A |
| Premium organic hummus (≤5 ingredients, olive oil) | A–B |
| Standard commercial hummus (6–8 ingredients) | B–C |
| Industrial hummus (8–12 ingredients, gums, preservatives) | C–D |
| Traditional matbucha (3–5 ingredients, cooked tomato) | B–C |
| Eggplant spread (simple, 4–6 ingredients) | B–C |
| Light hummus with stabilisers | C |

---

*This document is locked. Changes require a Head of Product decision with a dated note appended here.*
