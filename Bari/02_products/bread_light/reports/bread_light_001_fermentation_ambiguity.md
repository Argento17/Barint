# Bread-Light — Fermentation Ambiguity Examples

**Run:** run_bread_light_001  **Date:** 2026-05-20

## Definition

Fermentation in bread exists on a spectrum:
1. **Genuine live-culture sourdough** — מחמצת חיה with extended fermentation
   (12-24h). Live bacteria present at consumption. Structural and metabolic benefits.
2. **Traditional sourdough** — מחמצת from established culture, may not be live
   at consumption but underwent genuine fermentation during production.
3. **Industrial sourdough-style** — commercial yeast leavening with 2-5%
   dehydrated sourdough powder or rye sourdough concentrate for flavor.
   The 'מחמצת' token appears in ingredients but provides no fermentation benefit.
4. **Sourdough theater** — 'בסגנון מחמצת' (sourdough style) naming with no
   sourdough ingredient whatsoever. Pure marketing.

The current enrichment engine detects `מחמצת` as a fermentation marker but
cannot distinguish types 1-4. All get `has_fermentation=True`.

## Group D Products — Fermentation Spectrum

### לחם "בסגנון מחמצת" תעשייתי

**Score:** 62.5  **NOVA:** 3  **Struct.Class:** D
**Claims:** בטעם מחמצת, בסגנון מסורתי, מחמצת
**Fermentation markers detected:** מחמצת, שמרים, חומצה לקטית  **has_fermentation:** YES
**Design note (stress intent):** DECEPTIVE SOURDOUGH — 'מחמצת מגובשת' (dehydrated sourdough powder) at 2% is a flavor ingredient, not a leavening system. Commercial yeast does the fermentation. Lactic acid added chemically for sour taste. Two additives (E-471, E-481), preservative. The sourdough claim is technically present but structurally meaningless.
**Ingredients:** `קמח חיטה, מים, שמרים, מחמצת מגובשת (2%), מלח, גלוטן חיטה, E-471, E-481, חומר שימור E-282, חומצה לקטית...`

_Fermentation assessment:_ Sourdough theater: name uses 'בסגנון מחמצת' (sourdough style) with no sourdough ingredient. Fermentation marker should NOT fire. Check if detection leaked.

### לחם כפרי "מחמצת ושמרים"

**Score:** 68.0  **NOVA:** 3  **Struct.Class:** D
**Claims:** מחמצת כפרית, ביתי, אמיתי, כפרי
**Fermentation markers detected:** מחמצת, שמרים  **has_fermentation:** YES
**Design note (stress intent):** MIXED LEAVENING SYSTEM — both sourdough (8%) and commercial yeast (1.5%). 'כפרי' (rustic/farmhouse) marketing. Refined wheat dominates (50% vs 40% whole). Genuinely intermediate: sourdough is substantial but not sole leavening. Fermentation semantics should distinguish this from pure sourdough.
**Ingredients:** `קמח חיטה מלאה (40%), קמח חיטה (50%), מים, שמרים (1.5%), מחמצת (8%), מלח, שמן זית (2%), E-471...`

_Fermentation assessment:_ Genuine sourdough. Fermentation marker correctly detected. Live culture signal is real. NOVA 2 assignment appropriate.

### לחם מחמצת אמיתי ממחיטה מלאה

**Score:** 79.0  **NOVA:** 2  **Struct.Class:** B
**Claims:** מחמצת אמיתית, תסיסה ל-24 שעות, ללא שמרים מסחריים, עבודת יד
**Fermentation markers detected:** מחמצת  **has_fermentation:** YES
**Design note (stress intent):** GENUINE SOURDOUGH — only leavening is live sourdough culture. No commercial yeast. Whole wheat 60%. Long fermentation implied by process claim. This is the gold standard sourdough. Can the system recognize it vs industrial sourdough-style products?
**Ingredients:** `קמח חיטה מלאה (60%), קמח חיטה (35%), מים, מחמצת חיה (15%), מלח...`

_Fermentation assessment:_ Genuine sourdough. Fermentation marker correctly detected. Live culture signal is real. NOVA 2 assignment appropriate.

### לחמי קריספ מחמצת שיפון מסורתי

**Score:** 78.6  **NOVA:** 2  **Struct.Class:** B
**Claims:** מחמצת שיפון מסורתית, ללא שמרים
**Fermentation markers detected:** מחמצת  **has_fermentation:** YES
**Design note (stress intent):** GENUINE SOURDOUGH CRISPBREAD — 90% whole rye + rye sourdough. Only 3 ingredients. Highest fiber (12g) from structural grain. Authentic fermentation. Fermentation protects the product — expect NOVA 2/3 routing. Strong structural class A/B.
**Ingredients:** `קמח שיפון מלא (90%), מחמצת שיפון (8%), מלח...`

_Fermentation assessment:_ Genuine sourdough. Fermentation marker correctly detected. Live culture signal is real. NOVA 2 assignment appropriate.

### קרקר "מחמצת" בייצור מהיר

**Score:** 65.8  **NOVA:** 3  **Struct.Class:** D
**Claims:** מחמצת, תסיסה טבעית, שיפון
**Fermentation markers detected:** מחמצת, חומצה לקטית  **has_fermentation:** YES
**Design note (stress intent):** MIXED FERMENTATION SIGNAL — 5% sourdough is real but chemical leaveners (E-450, E-500) do the actual leavening work. Lactic acid added separately. The sourdough is a flavor contributor, not a structural fermentation system. Routing should see: mחמצת present but leavening_agent additives also present — ambiguous signal.
**Ingredients:** `קמח חיטה (65%), קמח שיפון (20%), מחמצת (5%), מלח, שמן קנולה, E-450, E-500, חומצה לקטית...`

_Fermentation assessment:_ Fermentation marker 'מחמצת' detected. Unable to determine genuine vs industrial without percentage/position context. Ambiguous case.

## Cross-Product NOVA Comparison

| Product | Ferm Detected | Ferm Type | NOVA | Score |
|---------|--------------|-----------|------|-------|
| לחם "בסגנון מחמצת" תעשייתי | YES | Theater (no sourdough) | 3 | 62.5 |
| לחם כפרי "מחמצת ושמרים" | YES | Genuine/Traditional | 3 | 68.0 |
| לחם מחמצת אמיתי ממחיטה מלאה | YES | Genuine/Traditional | 2 | 79.0 |
| לחמי קריספ מחמצת שיפון מסורתי | YES | Genuine/Traditional | 2 | 78.6 |
| קרקר "מחמצת" בייצור מהיר | YES | Ambiguous (token detected) | 3 | 65.8 |

## Ontology Gap

The engine cannot differentiate sourdough types because BSIP1 enrichment
only detects the presence of fermentation keywords, not their:
- Ingredient position (early = structural vs late = flavor)
- Percentage declaration (2% sourdough powder vs 80% sourdough base)
- Accompanying leavening agents (מחמצת + שמרים = industrial; מחמצת alone = traditional)

**Recommended enrichment addition:** If `מחמצת` appears AND `שמרים` (yeast) also
appears in ingredients, flag as `fermentation_quality=mixed` (industrial sourdough).
If `מחמצת` appears WITHOUT `שמרים`, flag as `fermentation_quality=traditional`.
If percentage of sourdough ingredient <10%, flag as `fermentation_role=flavor`.