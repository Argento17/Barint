# Bread-Light — Most Deceptive Products

**Run:** run_bread_light_001  **Date:** 2026-05-20

## Definition

A product is *deceptive* when its marketing signals (name, claims, packaging) imply
a structural quality that the ingredient list and matrix signals do not support.
These are the products most likely to fool a consumer — and an algorithm.

## Deception Taxonomy

| Type | Signal | Reality |
|------|--------|---------|
| Wholegrain halo | '100% חיטה מלאה', '7 דגנים' | Refined flour dominant, WG minor |
| Fiber laundering | '14g fiber', 'עשיר בסיבים' | Inulin/psyllium, not grain fiber |
| Seed halo | Seeds on surface, superfood naming | <5% seeds, refined flour base |
| Sourdough theater | 'מחמצת' in name | Dehydrated sourdough powder, industrial yeast |
| Protein assembly | '30g protein', 'sport nutrition' | Isolates, not whole-food protein |

## Product Analysis

### לחמי קריספ "14 גרם סיבים" תאית [Group B]

**Score:** 76.5  **Grade:** B  **Category:** whole_food_fat  **Struct.Class:** D
**Claims:** 14 גרם סיבים, ללא סוכר, מחיטה מלאה, גבוה בסיבים
**Design note:** FIBER LAUNDERING — 14g fiber headline. 8% is wood-pulp cellulose (סיבי תאית). Whole wheat is 60% but refined wheat also present. Cellulose adds bulk without nutritional structure or fermentability. Pure fiber inflation. This is a critical test case.
**Ingredients (preview):** `קמח חיטה מלאה (60%), קמח חיטה (20%), סיבי תאית (8%), מלח, שמרים, שמן צמחי...`
**Fiber:** 14g  **Protein:** 10g  **Matrix markers:** סיבי תאית

_Deception assessment:_ Fiber laundering likely: 14g fiber but matrix markers (סיבי תאית) indicate isolated fibers, not grain-structural fiber. Whole-grain signal fires but does not confirm WG as dominant flour.

### לחם "100% חיטה מלאה" מעורב [Group B]

**Score:** 68.9  **Grade:** B  **Category:** default  **Struct.Class:** D
**Claims:** 100% חיטה מלאה, ללא חומרי שימור
**Design note:** DECEPTIVE LABEL — front-of-pack says '100% whole wheat' but ingredient list is 50% whole wheat + 45% refined flour. First ingredient whole wheat gives legal cover. Refined flour is almost equal. This is a structurally critical stress case: fiber=5 is modest despite the claim.
**Ingredients (preview):** `קמח חיטה מלאה (50%), קמח חיטה (45%), מים, שמרים, מלח, שמן זית (2%), E-471...`
**Fiber:** 5g  **Protein:** 9g  **Matrix markers:** —

_Deception assessment:_ Wholegrain halo: whole_grain signal detected but refined flour is dominant ingredient. Algorithm cannot distinguish structural vs. decorative whole grain.

### קרקרים "מולטיגריין" עשיר בסיבים [Group B]

**Score:** 68.1  **Grade:** B  **Category:** cereal  **Struct.Class:** D
**Claims:** 12 גרם סיבים, מולטיגריין, עשיר בסיבים, תומך בעיכול
**Design note:** FIBER LAUNDERING — 12g fiber from isolated inulin (10%). Refined flour first. 'Multigrain' from oat flour + rye flour (5%). All fiber can be attributed to extracted chicory inulin, not structural grain. High fiber claim is technically accurate but structurally misleading.
**Ingredients (preview):** `קמח חיטה, אינולין (10%), קמח שיבולת שועל, קמח שיפון (5%), מלח, שמן צמחי, E-450, E-500...`
**Fiber:** 12g  **Protein:** 9g  **Matrix markers:** אינולין

_Deception assessment:_ Fiber laundering likely: 12g fiber but matrix markers (אינולין) indicate isolated fibers, not grain-structural fiber. Whole-grain signal fires but does not confirm WG as dominant flour.

### קרקר "בטא-גלוקן" תומך בלב [Group B]

**Score:** 63.5  **Grade:** C  **Category:** cereal  **Struct.Class:** D
**Claims:** בטא-גלוקן, מוריד כולסטרול, סיבים גבוהים, מאושר בריאות הלב
**Design note:** FUNCTIONAL FIBER SYSTEM — real beta-glucan (3%) plus isolated inulin (5%). Oat flour 40% + refined wheat 35%. Fiber=9 is a mix of genuine oat beta-glucan, extracted concentrate, and inulin. Health claim requires distinguishing structural beta-glucan from extracted inulin. Borderline legitimate.
**Ingredients (preview):** `קמח שיבולת שועל (40%), קמח חיטה (35%), בטא-גלוקן שיבולת שועל (3%), אינולין (5%), מלח, שמן קנולה, לצי...`
**Fiber:** 9g  **Protein:** 10g  **Matrix markers:** אינולין, בטא-גלוקן

_Deception assessment:_ Fiber laundering likely: 9g fiber but matrix markers (אינולין, בטא-גלוקן) indicate isolated fibers, not grain-structural fiber. Whole-grain signal fires but does not confirm WG as dominant flour.

### קרקרים "5 דגנים" ושיפון [Group B]

**Score:** 58.9  **Grade:** C  **Category:** snack_bar_granola  **Struct.Class:** D
**Claims:** 5 דגנים, עשיר בסיבים, מולטיגריין
**Design note:** WHOLEGRAIN HALO — refined wheat flour listed first. '5 grain' grains are minor: rye 3%, oats unlisted%, flax 2%. Fiber=6 is plausible but grain tokens, not whole-grain structure. Classic marketing halo without structural commitment.
**Ingredients (preview):** `קמח חיטה, קמח שיפון, גרגרי שיפון (3%), שיבולת שועל, פלקס (2%), מלח, שמן סויה, לציטין (E-322), E-500...`
**Fiber:** 6g  **Protein:** 10g  **Matrix markers:** —

_Deception assessment:_ Multi-grain naming with no confirmed whole-grain detection — possible weak halo.

### לחם "7 דגנים" תעשייתי [Group B]

**Score:** 53.0  **Grade:** C  **Category:** default  **Struct.Class:** E
**Claims:** 7 דגנים, מחיטה מלאה, טבעי
**Design note:** '7 GRAIN' HALO — refined wheat first, whole wheat only 25%, grain blend 4%. Added vital gluten. Two preservatives (E-282 + E-300). 'מחיטה מלאה' claim on label legally valid but structurally misleading. Maximum marketing halo with minimum structural commitment.
**Ingredients (preview):** `קמח חיטה, קמח חיטה מלאה (25%), מים, גרגרי שבעה דגנים (4%), סוכר, שמן צמחי, שמרים, מלח, E-471, E-481,...`
**Fiber:** 4g  **Protein:** 9g  **Matrix markers:** —

_Deception assessment:_ Wholegrain halo: whole_grain signal detected but refined flour is dominant ingredient. Algorithm cannot distinguish structural vs. decorative whole grain.

### לחמי קריספ שיפון וגרעינים נורדי [Group C]

**Score:** 81.6  **Grade:** A  **Category:** whole_food_fat  **Struct.Class:** D
**Claims:** גרעינים מלאים, עשיר בסיבים, ללא תוספת סוכר
**Design note:** GENUINE NORDIC CRISPBREAD — seeds 25% structurally significant. Whole rye base (65%). No additives. High fiber (11g) from real grain + seeds. High protein (13g). This is a good product. Can the system reward it correctly vs the seed-halo products?
**Ingredients (preview):** `קמח שיפון מלא (65%), זרעי חמנייה (12%), זרעי פשתן (8%), זרעי שומשום (5%), מלח, שמרים...`
**Fiber:** 11g  **Protein:** 13g  **Matrix markers:** —

_Deception assessment:_ Seed halo: seeds visible in name/claims but ingredient order places seeds at position 4-7 (minor ingredient). Seed token triggers WFF routing but structural identity is a refined-flour cracker.

### לחם גרעינים אמיתי [Group C]

**Score:** 76.5  **Grade:** B  **Category:** default  **Struct.Class:** D
**Claims:** עשיר בגרעינים, ללא מוסיפים, טבעי
**Design note:** GENUINE SEED BREAD — seeds ~20% structurally meaningful. Whole wheat base (55%). No additives. Good product that LOOKS like seed-halo but ISN'T. Key stress test: can the system distinguish 20% seeds from 3% seeds? High protein (12g) from seed combination.
**Ingredients (preview):** `קמח חיטה מלאה (55%), מים, שומשום (8%), זרעי חמנייה (7%), פשתן (5%), מלח, שמרים...`
**Fiber:** 7g  **Protein:** 12g  **Matrix markers:** —

_Deception assessment:_ Seed halo: seeds visible in name/claims but ingredient order places seeds at position 4-7 (minor ingredient). Seed token triggers WFF routing but structural identity is a refined-flour cracker.

### קרקרים "שבעת המינים" גרעינים [Group C]

**Score:** 59.1  **Grade:** C  **Category:** whole_food_fat  **Struct.Class:** D
**Claims:** שבעת המינים, עשיר בגרעינים, טבעי, ארץ ישראל
**Design note:** SEED HALO — seeds total <15%, all in visually evocative packaging. Refined wheat flour base. The '7 species' branding is cultural/religious marketing. Seeds are cosmetic garnish, not structural components. Classic Israeli market deception.
**Ingredients (preview):** `קמח חיטה, שמן סויה, מלח, גרגרי שיבולת שועל (4%), שומשום (3%), כוסמין (2%), זרעי פשתן (2%), זרעי חמני...`
**Fiber:** 4g  **Protein:** 9g  **Matrix markers:** —

_Deception assessment:_ Seed halo: seeds visible in name/claims but ingredient order places seeds at position 4-7 (minor ingredient). Seed token triggers WFF routing but structural identity is a refined-flour cracker.

### קרקר "גרעינים זהובים" פרמיום [Group C]

**Score:** 57.9  **Grade:** C  **Category:** whole_food_fat  **Struct.Class:** D
**Claims:** גרעינים זהובים, טבעי, ללא GMO, פרמיום
**Design note:** PREMIUM SEED HALO — golden sesame visually dominant on packaging, only 5% by weight. Honey at 2% adds naturalness halo. Refined base + canola oil + emulsifiers. Premium price for cosmetic seeds. Classic upmarket deception pattern.
**Ingredients (preview):** `קמח חיטה, שמן קנולה, זרעי שומשום מזהב (5%), מלח, דבש (2%), לציטין (E-322), E-471, E-481...`
**Fiber:** 3g  **Protein:** 8g  **Matrix markers:** —

_Deception assessment:_ Seed halo: seeds visible in name/claims but ingredient order places seeds at position 4-7 (minor ingredient). Seed token triggers WFF routing but structural identity is a refined-flour cracker.

### קרקר "פשתן וצ'יה" סופר-פוד [Group C]

**Score:** 52.6  **Grade:** C  **Category:** snack_bar_granola  **Struct.Class:** D
**Claims:** אומגה 3, פשתן וצ'יה, סופר-פוד, ברא-טבע
**Design note:** SUPERFOOD SEED HALO — 'omega-3 from flax' marketing. Flax only 4%, chia only 3%. Omega-3 contribution from 4% flax is ~160mg per 30g serving — marginal. Refined flour 70% base with emulsifiers and artificial flavoring. Premium pricing for negligible nutritional benefit from the headline seeds.
**Ingredients (preview):** `קמח חיטה (70%), שמן צמחי, זרעי פשתן (4%), זרעי צ'יה (3%), מלח, לציטין (E-322), E-471, E-500, טעם טבע...`
**Fiber:** 5g  **Protein:** 8g  **Matrix markers:** —

_Deception assessment:_ Seed halo: seeds visible in name/claims but ingredient order places seeds at position 4-7 (minor ingredient). Seed token triggers WFF routing but structural identity is a refined-flour cracker.

### לחם מחמצת אמיתי ממחיטה מלאה [Group D]

**Score:** 79.0  **Grade:** B  **Category:** default  **Struct.Class:** B
**Claims:** מחמצת אמיתית, תסיסה ל-24 שעות, ללא שמרים מסחריים, עבודת יד
**Design note:** GENUINE SOURDOUGH — only leavening is live sourdough culture. No commercial yeast. Whole wheat 60%. Long fermentation implied by process claim. This is the gold standard sourdough. Can the system recognize it vs industrial sourdough-style products?
**Ingredients (preview):** `קמח חיטה מלאה (60%), קמח חיטה (35%), מים, מחמצת חיה (15%), מלח...`
**Fiber:** 5g  **Protein:** 9g  **Matrix markers:** —

_Deception assessment:_ Sourdough theater: fermentation detected (מחמצת token) but this product uses dehydrated sourdough powder as flavor agent. Commercial yeast does the actual leavening. Algorithm cannot distinguish genuine sourdough from sourdough-flavored industrial bread.

### לחמי קריספ מחמצת שיפון מסורתי [Group D]

**Score:** 78.6  **Grade:** B  **Category:** default  **Struct.Class:** B
**Claims:** מחמצת שיפון מסורתית, ללא שמרים
**Design note:** GENUINE SOURDOUGH CRISPBREAD — 90% whole rye + rye sourdough. Only 3 ingredients. Highest fiber (12g) from structural grain. Authentic fermentation. Fermentation protects the product — expect NOVA 2/3 routing. Strong structural class A/B.
**Ingredients (preview):** `קמח שיפון מלא (90%), מחמצת שיפון (8%), מלח...`
**Fiber:** 12g  **Protein:** 8g  **Matrix markers:** —

_Deception assessment:_ Sourdough theater: fermentation detected (מחמצת token) but this product uses dehydrated sourdough powder as flavor agent. Commercial yeast does the actual leavening. Algorithm cannot distinguish genuine sourdough from sourdough-flavored industrial bread.

### לחם כפרי "מחמצת ושמרים" [Group D]

**Score:** 68.0  **Grade:** B  **Category:** default  **Struct.Class:** D
**Claims:** מחמצת כפרית, ביתי, אמיתי, כפרי
**Design note:** MIXED LEAVENING SYSTEM — both sourdough (8%) and commercial yeast (1.5%). 'כפרי' (rustic/farmhouse) marketing. Refined wheat dominates (50% vs 40% whole). Genuinely intermediate: sourdough is substantial but not sole leavening. Fermentation semantics should distinguish this from pure sourdough.
**Ingredients (preview):** `קמח חיטה מלאה (40%), קמח חיטה (50%), מים, שמרים (1.5%), מחמצת (8%), מלח, שמן זית (2%), E-471...`
**Fiber:** 4g  **Protein:** 9g  **Matrix markers:** —

_Deception assessment:_ Sourdough theater: fermentation detected (מחמצת token) but this product uses dehydrated sourdough powder as flavor agent. Commercial yeast does the actual leavening. Algorithm cannot distinguish genuine sourdough from sourdough-flavored industrial bread.

### קרקר "מחמצת" בייצור מהיר [Group D]

**Score:** 65.8  **Grade:** B  **Category:** whole_food_fat  **Struct.Class:** D
**Claims:** מחמצת, תסיסה טבעית, שיפון
**Design note:** MIXED FERMENTATION SIGNAL — 5% sourdough is real but chemical leaveners (E-450, E-500) do the actual leavening work. Lactic acid added separately. The sourdough is a flavor contributor, not a structural fermentation system. Routing should see: mחמצת present but leavening_agent additives also present — ambiguous signal.
**Ingredients (preview):** `קמח חיטה (65%), קמח שיפון (20%), מחמצת (5%), מלח, שמן קנולה, E-450, E-500, חומצה לקטית...`
**Fiber:** 5g  **Protein:** 9g  **Matrix markers:** —

_Deception assessment:_ Sourdough theater: fermentation detected (מחמצת token) but this product uses dehydrated sourdough powder as flavor agent. Commercial yeast does the actual leavening. Algorithm cannot distinguish genuine sourdough from sourdough-flavored industrial bread.

### לחם "בסגנון מחמצת" תעשייתי [Group D]

**Score:** 62.5  **Grade:** C  **Category:** default  **Struct.Class:** D
**Claims:** בטעם מחמצת, בסגנון מסורתי, מחמצת
**Design note:** DECEPTIVE SOURDOUGH — 'מחמצת מגובשת' (dehydrated sourdough powder) at 2% is a flavor ingredient, not a leavening system. Commercial yeast does the fermentation. Lactic acid added chemically for sour taste. Two additives (E-471, E-481), preservative. The sourdough claim is technically present but structurally meaningless.
**Ingredients (preview):** `קמח חיטה, מים, שמרים, מחמצת מגובשת (2%), מלח, גלוטן חיטה, E-471, E-481, חומר שימור E-282, חומצה לקטי...`
**Fiber:** 2g  **Protein:** 9g  **Matrix markers:** —

_Deception assessment:_ Sourdough theater: fermentation detected (מחמצת token) but this product uses dehydrated sourdough powder as flavor agent. Commercial yeast does the actual leavening. Algorithm cannot distinguish genuine sourdough from sourdough-flavored industrial bread.

### לחמי קריספ חלבון ופשתן "17 גרם" [Group E]

**Score:** 71.1  **Grade:** B  **Category:** dairy_protein  **Struct.Class:** D
**Claims:** 17 גרם חלבון, עשיר בפשתן, ללא תוספת סוכר, חיטה מלאה
**Design note:** ENGINEERED ON GENUINE BASE — good grain foundation (whole rye 45% + whole wheat 20%) but whey protein concentrate (15%) added to boost protein. Hybrid between natural and engineered. Flax (8%) is structurally significant. Tests whether the system can credit the good base while flagging the protein engineering.
**Ingredients (preview):** `קמח שיפון מלא (45%), חלבון מי גבינה מרוכז (15%), קמח חיטה מלאה (20%), פשתן (8%), מלח, שמרים, לציטין ...`
**Fiber:** 8g  **Protein:** 17g  **Matrix markers:** —

_Deception assessment:_ Engineered wellness: 17g protein, high fiber — scores better than structural analysis warrants.

### לחם חלבון ואגוזים "נוטרישן" [Group E]

**Score:** 70.9  **Grade:** B  **Category:** default  **Struct.Class:** D
**Claims:** 20 גרם חלבון, אגוזים ושקדים, ללא פחמימות ריקות, מאוזן
**Design note:** MULTI-ENGINEERED BAKERY — vital gluten (20%) + pea protein (10%) + almond flour (25%) creates a protein-dense product (20g) with engineered fat profile. Real walnuts (10%). Carbs=22g is genuinely low. This is a premium engineered system — tests whether the system can recognize engineering even when some ingredients are real.
**Ingredients (preview):** `קמח שקדים (25%), גלוטן חיטה (20%), קמח חיטה מלאה (15%), אגוזי מלך (10%), חלבון אפונה (10%), שמן זית,...`
**Fiber:** 6g  **Protein:** 20g  **Matrix markers:** —

_Deception assessment:_ Engineered wellness: 20g protein, high fiber — scores better than structural analysis warrants.

### קרקר "סיבים+" אינולין וסיליום [Group E]

**Score:** 69.0  **Grade:** B  **Category:** whole_food_fat  **Struct.Class:** D
**Claims:** 15 גרם סיבים, תומך בעיכול, סיבים טבעיים, צ'יקורי
**Design note:** FIBER SYSTEM — 15g fiber but: chicory inulin 12% + psyllium husk 5% = 17% extracted fiber systems. Refined flour first. Rye only 15%. 'Naturally sourced' fiber is true but non-structural. Tests fiber laundering detection at extreme fiber claims. Most aggressive fiber engineering in corpus.
**Ingredients (preview):** `קמח חיטה (50%), אינולין מצ'יקורי (12%), קמח שיפון (15%), psyllium husk (5%), מלח, שמן קנולה, לציטין ...`
**Fiber:** 15g  **Protein:** 9g  **Matrix markers:** אינולין, psyllium, psyllium husk

_Deception assessment:_ Engineered wellness: 9g protein, high fiber — scores better than structural analysis warrants.

### קרקר חלבון 30 "פרוטין קריספ" [Group E]

**Score:** 66.6  **Grade:** B  **Category:** dairy_protein  **Struct.Class:** D
**Claims:** 30 גרם חלבון, פחות פחמימות, מושלם לאחר אימון, צמחי
**Design note:** ENGINEERED PROTEIN — pea protein isolate (20%) + vital wheat gluten (10%) creates artificial protein density. The cracker matrix is a protein delivery vehicle with grain as filler. Structural class E. The 30g protein is real but mechanistically assembled. Tests whether the system penalizes protein engineering in bakery.
**Ingredients (preview):** `קמח שיפון (35%), חלבון אפונה מבודד (20%), קמח חיטה (20%), גלוטן חיטה (10%), שמן קנולה, מלח, לציטין (...`
**Fiber:** 5g  **Protein:** 30g  **Matrix markers:** —

_Deception assessment:_ Engineered wellness: 30g protein, high fiber — scores better than structural analysis warrants.

### לחם "ללא גלוטן" עמילן תפוחי אדמה [Group E]

**Score:** 50.0  **Grade:** C  **Category:** default  **Struct.Class:** D
**Claims:** ללא גלוטן, מוסמך, בריא
**Design note:** GLUTEN-FREE STRUCTURAL VOID — starch base (potato + corn + rice) with gum systems (guar + xanthan) to simulate bread texture. Protein=4g, fiber=2g, preservative added. 'ללא גלוטן' claim on packaging implies health benefit it doesn't have. Classic gluten-free trap: structurally poorer than standard refined bread.
**Ingredients (preview):** `עמילן תפוחי אדמה (35%), קמח אורז (25%), עמילן תירס (20%), שמן צמחי, מלח, שמרים, E-412 (גואר), E-415 ...`
**Fiber:** 2g  **Protein:** 4g  **Matrix markers:** גואר, קסנטן

_Deception assessment:_ Engineered wellness: 4g protein, high fiber — scores better than structural analysis warrants.

### לחם "קטו" דל פחמימות [Group E]

**Score:** 49.0  **Grade:** D  **Category:** default  **Struct.Class:** F
**Claims:** 3 גרם פחמימות נטו, ידידותי לקטו, ללא גלוטן, ללא דגנים
**Design note:** KETO BREAD SYSTEM — no cereal grains. Nut flour base (almond) + psyllium husk fiber + inulin + erythritol + sucralose. Structurally mimics bread without grain matrix. Fiber is 100% extracted. Sweetener present. Tests structural class interpretation when the product lacks cereal backbone entirely.
**Ingredients (preview):** `קמח שקדים (40%), psyllium husk (15%), ביצים, שמן קוקוס, אינולין (8%), אבקת אפייה, מלח, אריתריטול (5%...`
**Fiber:** 9g  **Protein:** 11g  **Matrix markers:** אינולין, psyllium, psyllium husk

_Deception assessment:_ Engineered wellness: 11g protein, high fiber — scores better than structural analysis warrants.
