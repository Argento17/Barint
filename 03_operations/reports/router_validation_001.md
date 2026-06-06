# BSIP2 Router v2 Validation Report

**Generated:** 2026-06-03 13:53 UTC
**Router:** router_v2
**Products analyzed:** 163
**Anchor activations:** 84 (52%)
**V1→V2 routing changes:** 19
**Suppression events:** 20 products with ≥1 suppressed signal
**Instability flags:** 9
**Hybrid products:** 3

---

## 1. V2 Routing Distribution

| Category          | Count | Anchor-driven | Hybrid | Mean Conf |
|-------------------|-------|---------------|--------|-----------|
| beverage          | 15    | 0             | 0      | 0.81      |
| cereal            | 39    | 33            | 0      | 0.89      |
| dairy_protein     | 47    | 37            | 0      | 0.91      |
| snack_bar_granola | 52    | 12            | 1      | 0.77      |
| whole_food_fat    | 6     | 0             | 2      | 0.71      |
| dessert           | 2     | 2             | 0      | 0.92      |
| sauce_spread      | 0     | 0             | 0      | —         |
| default           | 0     | 0             | 0      | —         |

---

## 2. Anchor Activation Rate

84/163 products (52%) routed via hard anchor. Anchors reflect stable, high-confidence routing decisions.

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
*... and 64 more anchor-routed products.*

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

**Unstable routes (9 products):** top-2 category delta < 0.3
  - פרי מארז חטיפי תמרים ושברי קקאו 5+1 → **whole_food_fat** (0.40) vs snack_bar_granola;  top-2 delta=0.10: whole_food_fat(0.25) vs snack_bar_granola(0.15)
  - חטיפי דגנים פיטנס קרם ועוגיות שישייה → **snack_bar_granola** (0.47) vs dessert;  top-2 delta=0.25: snack_bar_granola(1.27) vs dessert(1.02)
  - נייצ'ר וואלי צ'ואי בוטנים קלויים חמישייה → **snack_bar_granola** (0.53) vs whole_food_fat;  top-2 delta=0.22: snack_bar_granola(0.82) vs whole_food_fat(0.60)
  - מרבה סלים דליס קריספי תות 125 גר → **snack_bar_granola** (0.54) vs crispbread;  top-2 delta=0.07: snack_bar_granola(1.47) vs crispbread(1.40)
  - חטיפי דגנים פיטנס שקדים ודבש שישייה → **whole_food_fat** (0.56) vs snack_bar_granola;  top-2 delta=0.13: whole_food_fat(0.98) vs snack_bar_granola(0.85)
  - אלפרו שיבולת שועל ללא סוכר → **beverage** (0.59) vs cereal;  top-2 delta=0.20: beverage(1.60) vs cereal(1.40)
  - משקה שיבולת שועל → **beverage** (0.65) vs cereal;  top-2 delta=0.25: beverage(1.65) vs cereal(1.40)
  - חלב מלא בטעם של פעם 1ליטר לפחות 3.4%שומן → **bread** (0.68) vs dairy_protein;  top-2 delta=0.10: bread(0.80) vs dairy_protein(0.70)
  - מרבה סלים דליס קריספי אוכמניות 125 גר → **crispbread** (0.68) vs snack_bar_granola;  top-2 delta=0.18: crispbread(1.40) vs snack_bar_granola(1.22)

**Hybrid products (3):** genuinely straddle two routing contexts
  - חטיפי דגנים פיטנס שקדים ודבש שישייה → **whole_food_fat** + snack_bar_granola
  - פרי מארז חטיפי תמרים ושברי קקאו 5+1 → **whole_food_fat** + snack_bar_granola
  - נייצ'ר וואלי צ'ואי בוטנים קלויים חמישייה → **snack_bar_granola** + whole_food_fat

---

## 5. V1 → V2 Routing Changes

19 products changed category between v1 and v2. Changes are expected where v1 misrouted due to the failure modes this router fixes.

| Product                                      | V1 Category       | V2 Category       | Routing Basis | Dataset               |
|----------------------------------------------|-------------------|-------------------|---------------|-----------------------|
| חלב מלא בטעם של פעם 1ליטר לפחות 3.4%שומן     | dairy_protein     | bread             | signal        | milk_and_alternatives |
| דגני בוקר צ'יריוס דבש ואגוזים 375 גרם        | whole_food_fat    | cereal            | anchor        | breakfast_cereals     |
| קורנפלקס דגנים מלאים קלוגס 375 גרם           | snack_bar_granola | cereal            | anchor        | breakfast_cereals     |
| גרנולה עם אגוזים ודבש טבעי 400 גרם           | whole_food_fat    | snack_bar_granola | anchor        | breakfast_cereals     |
| גרנולה חלבון עם חלבון מי גבינה 350 גרם       | dairy_protein     | snack_bar_granola | anchor        | breakfast_cereals     |
| גרנולה דייטס ללא תוספת סוכר 400 גרם          | whole_food_fat    | snack_bar_granola | anchor        | breakfast_cereals     |
| גרנולה עם חמוציות 400 גרם                    | whole_food_fat    | snack_bar_granola | anchor        | breakfast_cereals     |
| גרנולה פצפוצים פריכים עם דבש ואגוזים 400 גרם | whole_food_fat    | snack_bar_granola | anchor        | breakfast_cereals     |
| גרנולה זרעים עם שמן זית ודבש 350 גרם         | whole_food_fat    | snack_bar_granola | anchor        | breakfast_cereals     |
| מוסלי פירות ואגוזים 500 גרם                  | whole_food_fat    | snack_bar_granola | anchor        | breakfast_cereals     |
| דגני בוקר פיטנס נסטלה 375 גרם                | snack_bar_granola | cereal            | anchor        | breakfast_cereals     |
| דגני בוקר פיטנס שוקולד נסטלה 375 גרם         | snack_bar_granola | cereal            | anchor        | breakfast_cereals     |
| אקטימל משקה חלב פרוביוטי                     | beverage          | dessert           | anchor        | yogurt_system         |
| לבן שתייה 3% שומן                            | beverage          | dairy_protein     | signal        | yogurt_system         |
| יוגורט ילדים שוקולד                          | sauce_spread      | dairy_protein     | anchor        | yogurt_system         |
| שתייה חלב לילדים פרוביוטיקה                  | beverage          | dessert           | anchor        | yogurt_system         |
| יוגורט מולר קורנר דבש אגוזים                 | whole_food_fat    | dairy_protein     | anchor        | yogurt_system         |
| מוס שוקולד יוגורט                            | sauce_spread      | dairy_protein     | anchor        | yogurt_system         |
| לבן שתייה 3% טנובה                           | beverage          | dairy_protein     | signal        | yogurt_system         |

---

## 6. V2 Routing Distribution by Source Category

**breakfast_cereals** (45 products): cereal=34  snack_bar_granola=11
**milk_and_alternatives** (20 products): beverage=15  dairy_protein=4  bread=1
**snack_bars** (53 products): snack_bar_granola=41  whole_food_fat=6  cereal=5  crispbread=1
**yogurt_system** (45 products): dairy_protein=43  dessert=2

---

## 7. Remaining Weak Zones

Products with low confidence or instability that may need further attention.

| Product                                            | Category          | Conf | Band   | Dataset    |
|----------------------------------------------------|-------------------|------|--------|------------|
| פרי מארז חטיפי תמרים ושברי קקאו 5+1                | whole_food_fat    | 0.40 | low    | snack_bars |
| חטיפי דגנים פיטנס קרם ועוגיות שישייה               | snack_bar_granola | 0.47 | low    | snack_bars |
| נייצ'ר וואלי צ'ואי שוקולד מריר בוטנים ושקדים חמישי | snack_bar_granola | 0.51 | medium | snack_bars |
| נייצ'ר וואלי צ'ואי בוטנים קלויים חמישייה           | snack_bar_granola | 0.53 | medium | snack_bars |
| מרבה סלים דליס קריספי תות 125 גר                   | snack_bar_granola | 0.54 | medium | snack_bars |

---

## 8. Bread/Crackers Readiness Assessment

Products that would be affected by bread/crackers category launch:
*No bread-adjacent products detected in current corpus.*
