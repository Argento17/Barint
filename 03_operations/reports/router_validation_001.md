# BSIP2 Router v2 Validation Report

**Generated:** 2026-05-20 10:38 UTC
**Router:** router_v2
**Products analyzed:** 163
**Anchor activations:** 82 (50%)
**V1→V2 routing changes:** 23
**Suppression events:** 20 products with ≥1 suppressed signal
**Instability flags:** 6
**Hybrid products:** 3

---

## 1. V2 Routing Distribution

| Category          | Count | Anchor-driven | Hybrid | Mean Conf |
|-------------------|-------|---------------|--------|-----------|
| beverage          | 19    | 0             | 0      | 0.83      |
| cereal            | 39    | 33            | 0      | 0.90      |
| dairy_protein     | 46    | 37            | 0      | 0.90      |
| snack_bar_granola | 53    | 12            | 1      | 0.81      |
| whole_food_fat    | 6     | 0             | 2      | 0.72      |
| dessert           | 0     | 0             | 0      | —         |
| sauce_spread      | 0     | 0             | 0      | —         |
| default           | 0     | 0             | 0      | —         |

---

## 2. Anchor Activation Rate

82/163 products (50%) routed via hard anchor. Anchors reflect stable, high-confidence routing decisions.

| Product                                           | Category          | Subtype    | Conf |
|---------------------------------------------------|-------------------|------------|------|
| מוסלי שוויצרי קלאסי 500 גרם                       | snack_bar_granola | muesli     | 0.88 |
| מוסלי בירכר בסיס 500 גרם                          | snack_bar_granola | muesli     | 0.88 |
| דגני בוקר צ'יריוס דבש ואגוזים 375 גרם             | cereal            | —          | 0.92 |
| וויטביקס דגני בוקר חיטה מלאה 430 גרם              | cereal            | —          | 0.92 |
| קורנפלקס קלוגס 375 גרם                            | cereal            | cornflakes | 0.93 |
| קורנפלקס דגנים מלאים קלוגס 375 גרם                | cereal            | cornflakes | 0.93 |
| דגני בוקר קוקו פופס קלוגס 375 גרם                 | cereal            | —          | 0.92 |
| דגני בוקר סמאקס דבש קלוגס 330 גרם                 | cereal            | —          | 0.92 |
| דגני בוקר פרוט לופס קלוגס 375 גרם                 | cereal            | —          | 0.92 |
| דגני בוקר ספשל K קלוגס 375 גרם                    | cereal            | —          | 0.92 |
| דגני בוקר ספשל K פירות אדומים קלוגס 375 גרם       | cereal            | —          | 0.92 |
| דגני בוקר אול-בראן פתיתי סובין קלוגס 375 גרם      | cereal            | —          | 0.92 |
| גרנולה קלאסטרס קלוגס 400 גרם                      | snack_bar_granola | granola    | 0.90 |
| דגני בוקר פתיתי סובין קלוגס 375 גרם               | cereal            | —          | 0.92 |
| דגני בוקר ספשל K חלבון קלוגס 320 גרם              | cereal            | —          | 0.92 |
| שיבולת שועל מהירה קוואקר 500 גרם                  | cereal            | oatmeal    | 0.88 |
| שיבולת שועל גרוסה ספרוגרן 500 גרם                 | cereal            | oatmeal    | 0.88 |
| דייסת שיבולת שועל מיידית בטעם דבש קוואקר 340 גרם  | cereal            | oatmeal    | 0.88 |
| דייסת שיבולת שועל מיידית בטעם וניל קוואקר 340 גרם | cereal            | oatmeal    | 0.88 |
| שיבולת שועל גלגולה קוואקר 500 גרם                 | cereal            | oatmeal    | 0.88 |
*... and 62 more anchor-routed products.*

---

## 3. Suppressed Contamination Signals

Products where context gating prevented ingredient-text signals from contaminating the routing decision.

**A. WFF ingredient contamination suppressed:** 15 products
  - קורני חטיפי דגנים בוטנים מתוק מלוח → routed to **snack_bar_granola**; suppressed: whole_food_fat:שמן קוקוס(suppressed:wff_excluded)
  - חטיפי דגנים פיטנס קרם ועוגיות שישייה → routed to **snack_bar_granola**; suppressed: whole_food_fat:גרעינים(suppressed:no_wff_context)
  - חטיף דגנים שוקו וניל נסטלה שישייה → routed to **snack_bar_granola**; suppressed: whole_food_fat:גרעינים(suppressed:no_wff_context)
  - סיני מיניס חטיף בטעם קינמון על שכבת קרם חלב 6 יח' → routed to **snack_bar_granola**; suppressed: whole_food_fat:גרעינים(suppressed:no_wff_context)
  - חטיף דגנים עם פירות יער → routed to **snack_bar_granola**; suppressed: whole_food_fat:גרעינים(suppressed:no_wff_context)
  - חטיפי דגנים פיטנס שוקולד בננה שישייה → routed to **snack_bar_granola**; suppressed: whole_food_fat:גרעינים(suppressed:no_wff_context)
  - חטיפי דגנים פיטנס שקדים ודבש שישייה → routed to **whole_food_fat**; suppressed: whole_food_fat:גרעינים(suppressed:no_wff_context)
  - חטיף דגנים מצופה שוקולד עם עוגיות בטעם קרמל וקרם נוגט ט → routed to **snack_bar_granola**; suppressed: whole_food_fat:אגוז(suppressed:no_wff_context), whole_food_fat:אגוזים(suppressed:no_wff_context)

**B. Beverage signal zeroed (no liquid context):** 5 products
  - קראנצ'י חטיף שיבולת שועל מיקס חמישייה → routed to **cereal**
  - חטיף אגוזים וחמוציות רפאלס 5*30 גרם → routed to **whole_food_fat**
  - חטיף פאי פקאן רפאלס 5*30 גרם → routed to **snack_bar_granola**
  - חטיפי פיטנס שיבולת שועל חמוציות 5*38 גרם → routed to **cereal**
  - חטיף דגנים מצופה שוקולד מריר סלים דליס → routed to **snack_bar_granola**

**C. Dairy flavor-descriptor suppression:** 2 products
  - סלים דליס חטיף רב דגנים מצופה שוקולד לבן בטעם יוגורט → routed to **snack_bar_granola**; suppressed: dairy_protein:יוגורט(flavor_suppressor)
  - מרבה סלים דליס שוקולד לבן בטעם יוגורט → routed to **snack_bar_granola**; suppressed: dairy_protein:יוגורט(flavor_suppressor)

---

## 4. Routing Instability and Hybrid Products

**Unstable routes (6 products):** top-2 category delta < 0.3
  - פרי מארז חטיפי תמרים ושברי קקאו 5+1 → **whole_food_fat** (0.40) vs snack_bar_granola;  top-2 delta=0.10: whole_food_fat(0.25) vs snack_bar_granola(0.15)
  - חטיפי דגנים פיטנס קרם ועוגיות שישייה → **snack_bar_granola** (0.56) vs dessert;  top-2 delta=0.25: snack_bar_granola(1.27) vs dessert(1.02)
  - נייצ'ר וואלי צ'ואי בוטנים קלויים חמישייה → **snack_bar_granola** (0.56) vs whole_food_fat;  top-2 delta=0.22: snack_bar_granola(0.82) vs whole_food_fat(0.60)
  - חטיפי דגנים פיטנס שקדים ודבש שישייה → **whole_food_fat** (0.60) vs snack_bar_granola;  top-2 delta=0.13: whole_food_fat(0.98) vs snack_bar_granola(0.85)
  - אלפרו שיבולת שועל ללא סוכר → **beverage** (0.64) vs cereal;  top-2 delta=0.20: beverage(1.60) vs cereal(1.40)
  - משקה שיבולת שועל → **beverage** (0.65) vs cereal;  top-2 delta=0.25: beverage(1.65) vs cereal(1.40)

**Hybrid products (3):** genuinely straddle two routing contexts
  - חטיפי דגנים פיטנס שקדים ודבש שישייה → **whole_food_fat** + snack_bar_granola
  - פרי מארז חטיפי תמרים ושברי קקאו 5+1 → **whole_food_fat** + snack_bar_granola
  - נייצ'ר וואלי צ'ואי בוטנים קלויים חמישייה → **snack_bar_granola** + whole_food_fat

---

## 5. V1 → V2 Routing Changes

23 products changed category between v1 and v2. Changes are expected where v1 misrouted due to the failure modes this router fixes.

| Product                                            | V1 Category       | V2 Category       | Routing Basis | Dataset           |
|----------------------------------------------------|-------------------|-------------------|---------------|-------------------|
| דגני בוקר צ'יריוס דבש ואגוזים 375 גרם              | whole_food_fat    | cereal            | anchor        | breakfast_cereals |
| קורנפלקס דגנים מלאים קלוגס 375 גרם                 | snack_bar_granola | cereal            | anchor        | breakfast_cereals |
| גרנולה עם אגוזים ודבש טבעי 400 גרם                 | whole_food_fat    | snack_bar_granola | anchor        | breakfast_cereals |
| גרנולה חלבון עם חלבון מי גבינה 350 גרם             | dairy_protein     | snack_bar_granola | anchor        | breakfast_cereals |
| גרנולה דייטס ללא תוספת סוכר 400 גרם                | whole_food_fat    | snack_bar_granola | anchor        | breakfast_cereals |
| גרנולה עם חמוציות 400 גרם                          | whole_food_fat    | snack_bar_granola | anchor        | breakfast_cereals |
| גרנולה פצפוצים פריכים עם דבש ואגוזים 400 גרם       | whole_food_fat    | snack_bar_granola | anchor        | breakfast_cereals |
| גרנולה זרעים עם שמן זית ודבש 350 גרם               | whole_food_fat    | snack_bar_granola | anchor        | breakfast_cereals |
| מוסלי פירות ואגוזים 500 גרם                        | whole_food_fat    | snack_bar_granola | anchor        | breakfast_cereals |
| דגני בוקר פיטנס נסטלה 375 גרם                      | snack_bar_granola | cereal            | anchor        | breakfast_cereals |
| דגני בוקר פיטנס שוקולד נסטלה 375 גרם               | snack_bar_granola | cereal            | anchor        | breakfast_cereals |
| קראנצ'י חטיף שיבולת שועל ושוקולד מריר חמישיה       | cereal            | snack_bar_granola | signal        | snack_bars        |
| חטיפי דגנים פיטנס שקדים ודבש שישייה                | snack_bar_granola | whole_food_fat    | signal        | snack_bars        |
| חטיפי פיטנס שיבולת שועל דבש 5*38 גרם               | whole_food_fat    | cereal            | signal        | snack_bars        |
| קראנצ'י חטיף שיבולת שועל עם חתיכות בטעם שוקולד חמי | cereal            | snack_bar_granola | signal        | snack_bars        |
| נייצר וואלי פרוטאין בוטנים בציפוי קרמל מלוח רביעיי | whole_food_fat    | snack_bar_granola | signal        | snack_bars        |
| נייצ'ר וואלי צ'ואי בוטנים קלויים חמישייה           | whole_food_fat    | snack_bar_granola | signal        | snack_bars        |
| נייצ'ר וואלי צ'ואי שוקולד מריר בוטנים ושקדים חמישי | whole_food_fat    | snack_bar_granola | signal        | snack_bars        |
| מרבה סלים דליס שוקולד חלב ללא גלוטן חדש            | whole_food_fat    | snack_bar_granola | signal        | snack_bars        |
| מרבה סלים דליס שוקולד לבן בטעם יוגורט              | whole_food_fat    | snack_bar_granola | signal        | snack_bars        |
| יוגורט ילדים שוקולד                                | sauce_spread      | dairy_protein     | anchor        | yogurt_system     |
| יוגורט מולר קורנר דבש אגוזים                       | whole_food_fat    | dairy_protein     | anchor        | yogurt_system     |
| מוס שוקולד יוגורט                                  | sauce_spread      | dairy_protein     | anchor        | yogurt_system     |

---

## 6. V2 Routing Distribution by Source Category

**breakfast_cereals** (45 products): cereal=34  snack_bar_granola=11
**milk_and_alternatives** (20 products): beverage=15  dairy_protein=5
**snack_bars** (53 products): snack_bar_granola=42  whole_food_fat=6  cereal=5
**yogurt_system** (45 products): dairy_protein=41  beverage=4

---

## 7. Remaining Weak Zones

Products with low confidence or instability that may need further attention.

| Product                                            | Category          | Conf | Band   | Dataset    |
|----------------------------------------------------|-------------------|------|--------|------------|
| פרי מארז חטיפי תמרים ושברי קקאו 5+1                | whole_food_fat    | 0.40 | low    | snack_bars |
| נייצ'ר וואלי צ'ואי שוקולד מריר בוטנים ושקדים חמישי | snack_bar_granola | 0.52 | medium | snack_bars |

---

## 8. Bread/Crackers Readiness Assessment

Products that would be affected by bread/crackers category launch:
*No bread-adjacent products detected in current corpus.*
