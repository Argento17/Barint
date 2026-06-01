# BSIP2 Router v2 — Anchor Audit & Routing Explainability Report

**Generated:** 2026-05-20 10:52 UTC
**Router:** router_v2
**Products analyzed:** 163
**Anchor activations:** 82 (50%)
**Signal-anchor agreement:** 71/82 anchored products (87%) — signal scoring would have returned same category
**Anchor overrides (signal disagreed):** 11 products
**V1→V2 routing changes:** 23

> **Audit goal:** Confirm anchors are conservative and explainable. Flag any anchor that fires too broadly, suppresses useful hybrid context, or produces false certainty. Prefer transparent uncertainty over strong but wrong routing.

---

## 1. Anchor Term Activation Table

How many products each anchor term claimed, and what it routed them to.

| Anchor Term | Count | Routes to         | Mean Conf | Signal Agrees | Over-reach Risk |
|-------------|-------|-------------------|-----------|---------------|-----------------|
| יוגורט      | 35    | dairy_protein     | 0.92      | 28/35         | LOW             |
| דגני בוקר   | 20    | cereal            | 0.92      | 20/20         | LOW             |
| גרנולה      | 9     | snack_bar_granola | 0.90      | 7/9           | LOW             |
| שיבולת שועל | 8     | cereal            | 0.88      | 8/8           | LOW             |
| קורנפלקס    | 5     | cereal            | 0.93      | 5/5           | LOW             |
| מוסלי       | 3     | snack_bar_granola | 0.88      | 2/3           | MEDIUM          |
| קפיר        | 2     | dairy_protein     | 0.93      | 1/2           | MEDIUM          |

---

## 2. Anchor Overrides — Signal Disagreement Cases

11 products where the anchor routed to a different category than signal-only scoring would have. Each case is reviewed for legitimacy.

### גרנולה זרעים עם שמן זית ודבש 350 גרם
- **Anchor:** 'גרנולה' → `snack_bar_granola`
- **Signal-only would route to:** `whole_food_fat` (score=3.10)
- **Signal mass (top-3):** whole_food_fat=3.10  snack_bar_granola=2.10  cereal=0.55
- **Assessment:** LEGITIMATE — granola anchor correctly overrides ingredient-nut contamination; 'גרנולה' in name is definitive product identity

### גרנולה עם אגוזים ודבש טבעי 400 גרם
- **Anchor:** 'גרנולה' → `snack_bar_granola`
- **Signal-only would route to:** `whole_food_fat` (score=2.20)
- **Signal mass (top-3):** whole_food_fat=2.20  snack_bar_granola=2.10  cereal=0.55
- **Assessment:** LEGITIMATE — granola anchor correctly overrides ingredient-nut contamination; 'גרנולה' in name is definitive product identity

### יוגורט חלבון ממרח שוקולד
- **Anchor:** 'יוגורט' → `dairy_protein`
- **Signal-only would route to:** `sauce_spread` (score=3.20)
- **Signal mass (top-3):** sauce_spread=3.20  dairy_protein=1.95  snack_bar_granola=1.10
- **Assessment:** LEGITIMATE — 'יוגורט' anchor overrides sauce_spread misroute; product is a dairy product, not a condiment

### יוגורט ילדים שוקולד
- **Anchor:** 'יוגורט' → `dairy_protein`
- **Signal-only would route to:** `snack_bar_granola` (score=1.10)
- **Signal mass (top-3):** snack_bar_granola=1.10  dairy_protein=0.95  sauce_spread=0.80
- **Assessment:** LEGITIMATE — small margin; anchor 'יוגורט' provides name-based certainty over ambiguous signal mass (snack_bar_granola=1.10)

### יוגורט מולר קורנר דבש אגוזים
- **Anchor:** 'יוגורט' → `dairy_protein`
- **Signal-only would route to:** `whole_food_fat` (score=1.95)
- **Signal mass (top-3):** whole_food_fat=1.95  dairy_protein=0.95
- **Assessment:** LEGITIMATE — 'יוגורט' anchor correctly overrides WFF contamination from nut toppings; nut toppings don't change product identity

### יוגורט שיבולת שועל
- **Anchor:** 'יוגורט' → `dairy_protein`
- **Signal-only would route to:** `cereal` (score=1.40)
- **Signal mass (top-3):** cereal=1.40  dairy_protein=0.95  beverage=0.75
- **Assessment:** LIKELY LEGITIMATE — signal mildly preferred cereal; anchor 'יוגורט' provides product-name certainty over text-signal noise

### יוגורט שקדים ואניל
- **Anchor:** 'יוגורט' → `dairy_protein`
- **Signal-only would route to:** `whole_food_fat` (score=0.98)
- **Signal mass (top-3):** whole_food_fat=0.97  dairy_protein=0.95  beverage=0.75
- **Assessment:** LEGITIMATE — 'יוגורט' anchor correctly overrides WFF contamination from nut toppings; nut toppings don't change product identity

### יוגורט שתייה תות
- **Anchor:** 'יוגורט' → `dairy_protein`
- **Signal-only would route to:** `beverage` (score=1.65)
- **Signal mass (top-3):** beverage=1.65  dairy_protein=0.95
- **Assessment:** LEGITIMATE (dairy drink) — 'שתייה' triggers primary_liquid_kw beverage boost, but יוגורט product is a fermented dairy item consumed in liquid form. dairy_protein is the correct scoring context. Beverage score (1.65) reflects liquid format descriptor, not product identity. Consider is_hybrid=True if liquid-dairy nuance is needed in future.

### מוס שוקולד יוגורט
- **Anchor:** 'יוגורט' → `dairy_protein`
- **Signal-only would route to:** `dessert` (score=2.20)
- **Signal mass (top-3):** dessert=2.20  snack_bar_granola=1.23  dairy_protein=0.95
- **Assessment:** LIKELY LEGITIMATE — yogurt-based יוגורט: dessert signal reflects texture/flavor ('מוס שוקולד'), not category identity. dairy_protein is the appropriate scoring context. The dessert score (2.20) is driven by 'מוס'+'שוקולד' signals but these are secondary to the dairy_protein product identity.

### מוסלי פירות ואגוזים 500 גרם
- **Anchor:** 'מוסלי' → `snack_bar_granola`
- **Signal-only would route to:** `whole_food_fat` (score=1.95)
- **Signal mass (top-3):** whole_food_fat=1.95  snack_bar_granola=1.90  dessert=1.70
- **Assessment:** LEGITIMATE — small margin; anchor 'מוסלי' provides name-based certainty over ambiguous signal mass (whole_food_fat=1.95)

### קפיר שתייה 3%
- **Anchor:** 'קפיר' → `dairy_protein`
- **Signal-only would route to:** `beverage` (score=1.65)
- **Signal mass (top-3):** beverage=1.65  dairy_protein=0.95
- **Assessment:** LEGITIMATE (dairy drink) — 'שתייה' triggers primary_liquid_kw beverage boost, but קפיר product is a fermented dairy item consumed in liquid form. dairy_protein is the correct scoring context. Beverage score (1.65) reflects liquid format descriptor, not product identity. Consider is_hybrid=True if liquid-dairy nuance is needed in future.

---

## 3. Suppressed Signal Review

For each suppression event: was it legitimate, or did it discard useful hybrid context?

**A. WFF ingredient contamination suppressed (15 products)**

These products contain nuts, seeds, or oils in ingredient text, but their NAME does not establish WFF context (no 'ממרח', 'חמאת', 'שמן' etc.). Suppression is correct in all cases below: the nut/oil is a secondary ingredient, not the product's identity.

  - **קורני חטיפי דגנים בוטנים מתוק מלוח** → `snack_bar_granola`
    Suppressed: whole_food_fat:שמן קוקוס(suppressed:wff_excluded)
    Verdict: **LEGITIMATE** — name contains a WFF-exclusion term (granola/cereal/snack context); oil ingredient is part of cereal/bar formulation, not product identity

  - **חטיפי דגנים פיטנס קרם ועוגיות שישייה** → `snack_bar_granola`
    Suppressed: whole_food_fat:גרעינים(suppressed:no_wff_context)
    Verdict: **LEGITIMATE** — name has no WFF identity marker; nut/oil is a secondary ingredient (coating, filling, or minor component)

  - **חטיף דגנים שוקו וניל נסטלה שישייה** → `snack_bar_granola`
    Suppressed: whole_food_fat:גרעינים(suppressed:no_wff_context)
    Verdict: **LEGITIMATE** — name has no WFF identity marker; nut/oil is a secondary ingredient (coating, filling, or minor component)

  - **סיני מיניס חטיף בטעם קינמון על שכבת קרם חלב 6 יח'** → `snack_bar_granola`
    Suppressed: whole_food_fat:גרעינים(suppressed:no_wff_context)
    Verdict: **LEGITIMATE** — name has no WFF identity marker; nut/oil is a secondary ingredient (coating, filling, or minor component)

  - **חטיף דגנים עם פירות יער** → `snack_bar_granola`
    Suppressed: whole_food_fat:גרעינים(suppressed:no_wff_context)
    Verdict: **LEGITIMATE** — name has no WFF identity marker; nut/oil is a secondary ingredient (coating, filling, or minor component)

  - **חטיפי דגנים פיטנס שוקולד בננה שישייה** → `snack_bar_granola`
    Suppressed: whole_food_fat:גרעינים(suppressed:no_wff_context)
    Verdict: **LEGITIMATE** — name has no WFF identity marker; nut/oil is a secondary ingredient (coating, filling, or minor component)

  - **חטיפי דגנים פיטנס שקדים ודבש שישייה** → `whole_food_fat` *(also hybrid-flagged)*
    Suppressed: whole_food_fat:גרעינים(suppressed:no_wff_context)
    Verdict: **LEGITIMATE** — name has no WFF identity marker; nut/oil is a secondary ingredient (coating, filling, or minor component)

  - **חטיף דגנים מצופה שוקולד עם עוגיות בטעם קרמל וקרם נוגט ט** → `snack_bar_granola`
    Suppressed: whole_food_fat:אגוז(suppressed:no_wff_context), whole_food_fat:אגוזים(suppressed:no_wff_context)
    Verdict: **LEGITIMATE** — name has no WFF identity marker; nut/oil is a secondary ingredient (coating, filling, or minor component)

  - **חטיף דגנים מצופה שוקולד חלב עם שברי אגוזים שישייה** → `snack_bar_granola`
    Suppressed: whole_food_fat:שקד(suppressed:wff_excluded)
    Verdict: **LEGITIMATE** — name contains a WFF-exclusion term (granola/cereal/snack context); oil ingredient is part of cereal/bar formulation, not product identity

  - **חטיף דגנים עם שברי אגוזים ושוקולד חלב בטר שישייה** → `snack_bar_granola`
    Suppressed: whole_food_fat:שקד(suppressed:wff_excluded)
    Verdict: **LEGITIMATE** — name contains a WFF-exclusion term (granola/cereal/snack context); oil ingredient is part of cereal/bar formulation, not product identity

  - **פרי מארז חטיפי תמרים ושברי קקאו 5+1** → `whole_food_fat` *(also hybrid-flagged)*
    Suppressed: whole_food_fat:אגוז(suppressed:no_wff_context), whole_food_fat:אגוזים(suppressed:no_wff_context)
    Verdict: **LEGITIMATE** — name has no WFF identity marker; nut/oil is a secondary ingredient (coating, filling, or minor component)

  - **חטיפי פיטנס שיבולת שועל דבש 5*38 גרם** → `cereal`
    Suppressed: whole_food_fat:שמן קוקוס(suppressed:no_wff_context)
    Verdict: **LEGITIMATE** — name has no WFF identity marker; nut/oil is a secondary ingredient (coating, filling, or minor component)

  - **סלים דליס חטיף רב דגנים מצופה שוקולד לבן בטעם יוגורט** → `snack_bar_granola`
    Suppressed: whole_food_fat:כוסמת(suppressed:no_wff_context)
    Verdict: **LEGITIMATE** — name has no WFF identity marker; nut/oil is a secondary ingredient (coating, filling, or minor component)

  - **מרבה סלים דליס שוקולד חלב ללא גלוטן חדש** → `snack_bar_granola`
    Suppressed: whole_food_fat:כוסמת(suppressed:no_wff_context)
    Verdict: **LEGITIMATE** — name has no WFF identity marker; nut/oil is a secondary ingredient (coating, filling, or minor component)

  - **מרבה סלים דליס שוקולד לבן בטעם יוגורט** → `snack_bar_granola`
    Suppressed: whole_food_fat:כוסמת(suppressed:no_wff_context)
    Verdict: **LEGITIMATE** — name has no WFF identity marker; nut/oil is a secondary ingredient (coating, filling, or minor component)

**B. Beverage signal zeroed — no liquid context (5 products)**

These products triggered a beverage name-only signal (e.g. 'שיבולת שועל' → some liquid context) but the product name provides no liquid identity marker. Zeroing is correct: they are solid food products.

  - **קראנצ'י חטיף שיבולת שועל מיקס חמישייה** → `cereal`
    beverage:zeroed(no_liquid_context,had=0.40)
    Verdict: **LEGITIMATE** — solid product, no liquid identity in name

  - **חטיף אגוזים וחמוציות רפאלס 5*30 גרם** → `whole_food_fat`
    beverage:zeroed(no_liquid_context,had=0.40)
    Verdict: **LEGITIMATE** — solid product, no liquid identity in name

  - **חטיף פאי פקאן רפאלס 5*30 גרם** → `snack_bar_granola`
    beverage:zeroed(no_liquid_context,had=0.40)
    Verdict: **LEGITIMATE** — solid product, no liquid identity in name

  - **חטיפי פיטנס שיבולת שועל חמוציות 5*38 גרם** → `cereal`
    beverage:zeroed(no_liquid_context,had=0.40)
    Verdict: **LEGITIMATE** — solid product, no liquid identity in name

  - **חטיף דגנים מצופה שוקולד מריר סלים דליס** → `snack_bar_granola`
    beverage:zeroed(no_liquid_context,had=0.40)
    Verdict: **LEGITIMATE** — solid product, no liquid identity in name

**C. Dairy flavor-descriptor suppression (2 products)**

'יוגורט' appears after 'בטעם' (flavor descriptor) in name. These are yogurt-FLAVORED products (typically coatings or fillings), not yogurt products. Suppression is correct.

  - **סלים דליס חטיף רב דגנים מצופה שוקולד לבן בטעם יוגורט** → `snack_bar_granola`
    Suppressed: dairy_protein:יוגורט(flavor_suppressor)
    Verdict: **LEGITIMATE** — 'בטעם יוגורט' is a flavor coating, not a dairy product

  - **מרבה סלים דליס שוקולד לבן בטעם יוגורט** → `snack_bar_granola`
    Suppressed: dairy_protein:יוגורט(flavor_suppressor)
    Verdict: **LEGITIMATE** — 'בטעם יוגורט' is a flavor coating, not a dairy product

---

## 4. V1 → V2 Routing Change Classification

23 products changed routing between v1 and v2.

| Icon | Verdict |
|------|---------|
| ✓✓ | clear improvement — v1 was definitively wrong |
| ✓  | likely improvement — v1 was probably wrong, v2 defensible |
| ?  | uncertain — both routes have merit; verdict depends on scoring goals |
| ✗  | possible regression — v2 may be less accurate than v1 |

| Product                                          | V1 Category       | V2 Category       | Basis  | Verdict |
|--------------------------------------------------|-------------------|-------------------|--------|---------|
| דגני בוקר צ'יריוס דבש ואגוזים 375 גרם            | whole_food_fat    | cereal            | anchor | ✓✓      |
| קורנפלקס דגנים מלאים קלוגס 375 גרם               | snack_bar_granola | cereal            | anchor | ✓✓      |
| גרנולה עם אגוזים ודבש טבעי 400 גרם               | whole_food_fat    | snack_bar_granola | anchor | ✓✓      |
| גרנולה חלבון עם חלבון מי גבינה 350 גרם           | dairy_protein     | snack_bar_granola | anchor | ✓✓      |
| גרנולה דייטס ללא תוספת סוכר 400 גרם              | whole_food_fat    | snack_bar_granola | anchor | ✓✓      |
| גרנולה עם חמוציות 400 גרם                        | whole_food_fat    | snack_bar_granola | anchor | ✓✓      |
| גרנולה פצפוצים פריכים עם דבש ואגוזים 400 גרם     | whole_food_fat    | snack_bar_granola | anchor | ✓✓      |
| גרנולה זרעים עם שמן זית ודבש 350 גרם             | whole_food_fat    | snack_bar_granola | anchor | ✓✓      |
| מוסלי פירות ואגוזים 500 גרם                      | whole_food_fat    | snack_bar_granola | anchor | ✓✓      |
| דגני בוקר פיטנס נסטלה 375 גרם                    | snack_bar_granola | cereal            | anchor | ✓✓      |
| דגני בוקר פיטנס שוקולד נסטלה 375 גרם             | snack_bar_granola | cereal            | anchor | ✓✓      |
| קראנצ'י חטיף שיבולת שועל ושוקולד מריר חמישיה     | cereal            | snack_bar_granola | signal | ✓       |
| חטיפי דגנים פיטנס שקדים ודבש שישייה              | snack_bar_granola | whole_food_fat    | signal | ?       |
| חטיפי פיטנס שיבולת שועל דבש 5*38 גרם             | whole_food_fat    | cereal            | signal | ?       |
| קראנצ'י חטיף שיבולת שועל עם חתיכות בטעם שוקולד ח | cereal            | snack_bar_granola | signal | ✓       |
| נייצר וואלי פרוטאין בוטנים בציפוי קרמל מלוח רביע | whole_food_fat    | snack_bar_granola | signal | ✓       |
| נייצ'ר וואלי צ'ואי בוטנים קלויים חמישייה         | whole_food_fat    | snack_bar_granola | signal | ✓       |
| נייצ'ר וואלי צ'ואי שוקולד מריר בוטנים ושקדים חמי | whole_food_fat    | snack_bar_granola | signal | ✓       |
| מרבה סלים דליס שוקולד חלב ללא גלוטן חדש          | whole_food_fat    | snack_bar_granola | signal | ✓       |
| מרבה סלים דליס שוקולד לבן בטעם יוגורט            | whole_food_fat    | snack_bar_granola | signal | ✓       |
| יוגורט ילדים שוקולד                              | sauce_spread      | dairy_protein     | anchor | ✓✓      |
| יוגורט מולר קורנר דבש אגוזים                     | whole_food_fat    | dairy_protein     | anchor | ✓✓      |
| מוס שוקולד יוגורט                                | sauce_spread      | dairy_protein     | anchor | ✓✓      |


**Verdict summary:** ✓✓ clear=14  ✓ likely=7  ? uncertain=2  ✗ regression=0

### Uncertain/Regression Cases — Detail

**חטיפי דגנים פיטנס שקדים ודבש שישייה** (`snack_bar_granola` → `whole_food_fat`)
> genuine hybrid: high almond load pulls WFF; snack-bar format pulls snack_bar_granola; v1 snack_bar_granola also defensible; product flagged as hybrid (snack_bar_granola + WFF) — WFF primary driven by almond-honey signal mass

**חטיפי פיטנס שיבולת שועל דבש 5*38 גרם** (`whole_food_fat` → `cereal`)
> cereal beats WFF (clear improvement over v1); however snack_bar_granola would be more precise for multi-pack bars; 'שיבולת שועל' anchor excluded by 'חטיפי' → signal routing; cereal is next-best given current signal weights

---

## 5. Special-Area Anchor Review

The six areas flagged in the audit brief, with specific product examples.

### A. Plant-Milk Brand Bypass

Products where the brand/name-first-word is in `_KNOWN_PLANT_MILK_BRANDS`. These skip the anchor stage. The bypass includes a guard: if the name also contains a dairy-format anchor term ('יוגורט', 'קפיר', etc.), the bypass does NOT fire — the yogurt anchor is allowed to settle routing instead.

**Bypass triggered (anchor skipped):**
  - אלפרו שקדים ללא סוכר → `beverage` (conf=0.82)
  - אלפרו שיבולת שועל ללא סוכר → `beverage` (conf=0.64)
  - אלפרו שוקו משקה סויה → `beverage` (conf=0.92)

**Guard held (anchor allowed despite known brand):**
  *(Products where brand is Alpro/Oatly etc. but name has 'יוגורט' — anchor fires, dairy_protein wins)*
  *(None in current corpus — no Alpro yogurt products present)*

### B. Yogurt vs Beverage

The 'יוגורט' anchor (conf=0.92) routes to dairy_protein whenever 'יוגורט' appears in name before 'בטעם'. Plant-based yogurts with 'יוגורט' in name correctly remain dairy_protein. Oat/almond milks without 'יוגורט' correctly route to beverage via the plant-milk brand bypass or liquid gate.

  - Products anchored to dairy_protein via 'יוגורט': 35
  - Products routed to beverage: 19
  - Yogurt-anchored products where signal agreed: 28/35

  Sample yogurt-anchored products:
    - יוגורט טבעי 1.5% שומן (sig would: dairy_protein, agrees=True)
    - יוגורט טבעי 3% שומן (sig would: dairy_protein, agrees=True)
    - יוגורט טבעי 5% שומן יוטבתה (sig would: dairy_protein, agrees=True)
    - יוגורט עיזים 9% שומן (sig would: dairy_protein, agrees=True)
    - יוגורט יווני 0% שומן (sig would: dairy_protein, agrees=True)

### C. Oat Drink vs Cereal

'שיבולת שועל' anchors to cereal (conf=0.88) with position check (≤20 chars). ANCHOR_EXCLUSIONS include 'משקה', 'שתייה', 'חטיף', 'חטיפי', 'ברים', etc. The plant-milk brand bypass handles products where 'שיבולת שועל' appears after a known liquid brand (e.g. 'אלפרו שיבולת שועל').

  - Products anchored to cereal via 'שיבולת שועל': 8
  - Oat-named products routed to beverage (brand bypass): 5
    - אלפרו שיבולת שועל ללא סוכר → `beverage` (conf=0.64)
    - משקה שיבולת שועל → `beverage` (conf=0.65)
    - משקה בריסטה שיבולת שועל → `beverage` (conf=0.74)
    - משקה שיבולת שועל ללא סוכר → `beverage` (conf=0.74)

  Anchored (cereal): שיבולת שועל מהירה קוואקר 500 גרם (sig=cereal, agrees=True)
  Anchored (cereal): שיבולת שועל גרוסה ספרוגרן 500 גרם (sig=cereal, agrees=True)
  Anchored (cereal): דייסת שיבולת שועל מיידית בטעם דבש קוואקר 340 גרם (sig=cereal, agrees=True)
  Anchored (cereal): דייסת שיבולת שועל מיידית בטעם וניל קוואקר 340 גרם (sig=cereal, agrees=True)
  Anchored (cereal): שיבולת שועל גלגולה קוואקר 500 גרם (sig=cereal, agrees=True)

### D. Nut Butter vs Filling

Nut-butter anchors ('חמאת בוטנים', 'חמאת שקדים', etc.) are excluded when 'מילוי', 'חטיף', 'עוגיות', 'שכבת' appear in the name. This prevents 'חטיף תמרים במילוי חמאת בוטנים' (date bar with PB filling) from anchoring to whole_food_fat.

  - Products anchored via nut-butter terms: 0
  - Products where nut-butter term was EXCLUDED (anchor suppressed): 2
    - חטיף תמרים במילוי חמאת שקדים → `whole_food_fat` (anchor skipped)
    - חטיף תמרים במילוי חמאת בוטנים → `snack_bar_granola` (anchor skipped)

### E. Snack Bar vs Oatmeal

'שיבולת שועל' anchor is excluded when 'חטיפי' or 'חטיף' appear in name (added in this sprint). This prevents fitness oat bars from anchoring to cereal when the product format is clearly a bar.

  - Oat-named products NOT anchored (exclusion fired), routed to snack_bar_granola: 2
    - קראנצ'י חטיף שיבולת שועל ושוקולד מריר חמישיה → `snack_bar_granola` (exclusion: חטיף)
    - קראנצ'י חטיף שיבולת שועל עם חתיכות בטעם שוקולד חמישייה. → `snack_bar_granola` (exclusion: חטיף)
  - Oat-named products NOT anchored, routed to cereal (signal): 5
    - קראנצ'י חטיף שיבולת שועל עם דבש חמישייה → `cereal`
    - קראנצ'י חטיף שיבולת שועל עם מייפל קנדי חמישייה → `cereal`
    - קראנצ'י חטיף שיבולת שועל מיקס חמישייה → `cereal`
    - חטיפי פיטנס שיבולת שועל חמוציות 5*38 גרם → `cereal`

### F. Granola vs Whole-Food-Fat

The 'גרנולה' anchor (conf=0.90) routes to snack_bar_granola. In v1, granola products with nuts/oils in ingredients were contaminated to whole_food_fat via full-text signal matching. The anchor + WFF context gate eliminates this failure mode.

  - Granola products now anchored to snack_bar_granola: 9
  - Granola products that previously misrouted to whole_food_fat (now fixed): 5
    - גרנולה קלאסטרס קלוגס 400 גרם (sig=snack_bar_granola, agrees=True)
    - גרנולה עם אגוזים ודבש טבעי 400 גרם (sig=whole_food_fat, agrees=False)
    - גרנולה עם שבבי שוקולד 400 גרם (sig=snack_bar_granola, agrees=True)
    - גרנולה חלבון עם חלבון מי גבינה 350 גרם (sig=snack_bar_granola, agrees=True)
    - גרנולה דייטס ללא תוספת סוכר 400 גרם (sig=snack_bar_granola, agrees=True)
    - גרנולה עם חמוציות 400 גרם (sig=snack_bar_granola, agrees=True)

---

## 6. Anchor Conservatism Assessment

Anchors are ordered here by their potential for over-reach. 'Over-reach risk' is HIGH when >50% of anchor activations disagreed with signal-only scoring.

| Anchor Term | Count | Override Cases | Position Check  | Exclusions                               | Risk                                                     |
|-------------|-------|----------------|-----------------|------------------------------------------|----------------------------------------------------------|
| יוגורט      | 35    | 7              | no              | none                                     | LOW                                                      |
| דגני בוקר   | 20    | 0              | no              | none                                     | LOW                                                      |
| גרנולה      | 9     | 2              | no              | none                                     | LOW                                                      |
| שיבולת שועל | 8     | 0              | yes (≤20 chars) | לחם, עוגיות, מאפה, ביסקוויט, פריכיות, מש | LOW                                                      |
| קורנפלקס    | 5     | 0              | no              | none                                     | LOW                                                      |
| מוסלי       | 3     | 1              | no              | none                                     | MEDIUM — consider tightening exclusions or reducing conf |
| קפיר        | 2     | 1              | no              | none                                     | MEDIUM — consider tightening exclusions or reducing conf |


### Recommended Actions

- **'יוגורט' (LOW RISK):** 7/35 overrides — anchor is conservative and consistent with signal scoring.
- **'דגני בוקר' (LOW RISK):** 0/20 overrides — anchor is conservative and consistent with signal scoring.
- **'גרנולה' (LOW RISK):** 2/9 overrides — anchor is conservative and consistent with signal scoring.
- **'שיבולת שועל' (LOW RISK):** 0/8 overrides — anchor is conservative and consistent with signal scoring.
- **'קורנפלקס' (LOW RISK):** 0/5 overrides — anchor is conservative and consistent with signal scoring.
- **'מוסלי' (MEDIUM RISK):** 1/3 overrides. Monitor with next corpus expansion.
- **'קפיר' (MEDIUM RISK):** 1/2 overrides. Monitor with next corpus expansion.
