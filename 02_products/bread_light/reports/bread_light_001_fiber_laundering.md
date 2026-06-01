# Bread-Light — Fiber Laundering Examples

**Run:** run_bread_light_001  **Date:** 2026-05-20

## Definition

Fiber laundering: adding isolated, extracted fiber ingredients (inulin, psyllium,
cellulose, guar gum) to artificially inflate the dietary fiber number without
any structural whole-grain basis. Common in 'high fiber' crackers and bread.

## Detected Cases

### קרקר "סיבים+" אינולין וסיליום [Group E]

**Score:** 69.0  **Grade:** B  **Fiber:** 15g/100g
**Claims:** 15 גרם סיבים, תומך בעיכול, סיבים טבעיים, צ'יקורי
**Laundering markers:** אינולין, psyllium, psyllium husk
**Whole-grain signal:** no
**Ingredients:** `קמח חיטה (50%), אינולין מצ'יקורי (12%), קמח שיפון (15%), psyllium husk (5%), מלח, שמן קנולה, לציטין (E-322), E-450, E-500...`

_Assessment:_ High-confidence laundering: 15g fiber with isolated sources (אינולין, psyllium, psyllium husk). No whole-grain base — fiber is entirely from isolated additives.

### לחמי קריספ "14 גרם סיבים" תאית [Group B]

**Score:** 76.5  **Grade:** B  **Fiber:** 14g/100g
**Claims:** 14 גרם סיבים, ללא סוכר, מחיטה מלאה, גבוה בסיבים
**Laundering markers:** סיבי תאית
**Whole-grain signal:** YES
**Ingredients:** `קמח חיטה מלאה (60%), קמח חיטה (20%), סיבי תאית (8%), מלח, שמרים, שמן צמחי...`

_Assessment:_ High-confidence laundering: 14g fiber with isolated sources (סיבי תאית). Whole-grain signal present (masks laundering further).

### קרקרים "מולטיגריין" עשיר בסיבים [Group B]

**Score:** 68.1  **Grade:** B  **Fiber:** 12g/100g
**Claims:** 12 גרם סיבים, מולטיגריין, עשיר בסיבים, תומך בעיכול
**Laundering markers:** אינולין
**Whole-grain signal:** no
**Ingredients:** `קמח חיטה, אינולין (10%), קמח שיבולת שועל, קמח שיפון (5%), מלח, שמן צמחי, E-450, E-500...`

_Assessment:_ High-confidence laundering: 12g fiber with isolated sources (אינולין). No whole-grain base — fiber is entirely from isolated additives.

### לחמי קריספ מחמצת שיפון מסורתי [Group D]

**Score:** 78.6  **Grade:** B  **Fiber:** 12g/100g
**Claims:** מחמצת שיפון מסורתית, ללא שמרים
**Laundering markers:** —
**Whole-grain signal:** no
**Ingredients:** `קמח שיפון מלא (90%), מחמצת שיפון (8%), מלח...`

_Assessment:_ High fiber (12g) without detected isolated markers — may be genuine grain fiber. Monitor ingredient order.

### לחמי קריספ שיפון וגרעינים נורדי [Group C]

**Score:** 81.6  **Grade:** A  **Fiber:** 11g/100g
**Claims:** גרעינים מלאים, עשיר בסיבים, ללא תוספת סוכר
**Laundering markers:** —
**Whole-grain signal:** no
**Ingredients:** `קמח שיפון מלא (65%), זרעי חמנייה (12%), זרעי פשתן (8%), זרעי שומשום (5%), מלח, שמרים...`

_Assessment:_ High fiber (11g) without detected isolated markers — may be genuine grain fiber. Monitor ingredient order.

### לחמי קריספ שיפון פשוט [Group A]

**Score:** 78.6  **Grade:** B  **Fiber:** 10g/100g
**Claims:** —
**Laundering markers:** —
**Whole-grain signal:** no
**Ingredients:** `קמח שיפון מלא (93%), מלח...`

_Assessment:_ High fiber (10g) without detected isolated markers — may be genuine grain fiber. Monitor ingredient order.

### קרקר "בטא-גלוקן" תומך בלב [Group B]

**Score:** 63.5  **Grade:** C  **Fiber:** 9g/100g
**Claims:** בטא-גלוקן, מוריד כולסטרול, סיבים גבוהים, מאושר בריאות הלב
**Laundering markers:** אינולין
**Whole-grain signal:** no
**Ingredients:** `קמח שיבולת שועל (40%), קמח חיטה (35%), בטא-גלוקן שיבולת שועל (3%), אינולין (5%), מלח, שמן קנולה, לציטין (E-322), E-450...`

_Assessment:_ Partial laundering: isolated fiber markers present (אינולין) with 9g fiber.

### לחם "קטו" דל פחמימות [Group E]

**Score:** 49.0  **Grade:** D  **Fiber:** 9g/100g
**Claims:** 3 גרם פחמימות נטו, ידידותי לקטו, ללא גלוטן, ללא דגנים
**Laundering markers:** אינולין, psyllium, psyllium husk
**Whole-grain signal:** no
**Ingredients:** `קמח שקדים (40%), psyllium husk (15%), ביצים, שמן קוקוס, אינולין (8%), אבקת אפייה, מלח, אריתריטול (5%), ממתיק: E-955...`

_Assessment:_ Partial laundering: isolated fiber markers present (אינולין, psyllium, psyllium husk) with 9g fiber.

### לחם "ללא גלוטן" עמילן תפוחי אדמה [Group E]

**Score:** 50.0  **Grade:** C  **Fiber:** 2g/100g
**Claims:** ללא גלוטן, מוסמך, בריא
**Laundering markers:** גואר
**Whole-grain signal:** no
**Ingredients:** `עמילן תפוחי אדמה (35%), קמח אורז (25%), עמילן תירס (20%), שמן צמחי, מלח, שמרים, E-412 (גואר), E-415 (קסנטן), E-471, E-481, סוכר, חומר שימור E-282...`

_Assessment:_ Partial laundering: isolated fiber markers present (גואר) with 2g fiber.

## Ontology Gap

The current engine detects isolated fiber markers in `extracted_matrix_markers`
but does NOT currently:
1. Penalize fiber quantity when matrix markers indicate isolated sources
2. Flag the combination of 'high fiber claim' + isolated fiber markers
3. Distinguish grain-structural fiber from additive fiber in the glycemic_quality dimension

This means products with 14-15g of inulin+psyllium score similarly to products
with genuine whole-grain fiber in the glycemic and nutrient_density dimensions.

**Recommended engine addition:** If `extracted_matrix_markers` contains isolated
fiber terms AND fiber_g > 8, apply a 'fiber source quality' discount to glycemic_quality
and nutrient_density that reflects the isolated (not structural) origin.