# Bread-Light — Fermentation Spectrum Validation (run_002)

**Date:** 2026-05-20

## Context

Run_001 identified fermentation ambiguity as a key ontology gap: the engine detected
'מחמצת' tokens but could not distinguish genuine sourdough from industrial theater.

Run_002 introduces `classify_fermentation_quality` in the Bakery Semantics Layer v1,
which distinguishes: traditional / mixed_industrial / flavor_only / theater / none.

## Group D — Fermentation Gradient (Primary Validation Target)

### לחמי קריספ מחמצת שיפון מסורתי

**Score:** 79.4  **Grade:** B  **NOVA:** 2  **SC:** B  **GSS:** 100.0
**Fermentation quality:** `traditional`
**Fermentation basis:** ['מחמצת']
**Fermentation notes:** Traditional sourdough fermentation at 8.0%. No commercial yeast detected.
**Flour quality class:** 1  **WG dominance:** high
**Design intent:** GENUINE SOURDOUGH CRISPBREAD — 90% whole rye + rye sourdough. Only 3 ingredients. Highest fiber (12g) from structural grain. Authentic fermentation. Fermentation protects the product — expect NOVA 2/3 routing. Strong structural class A/B.
**Ingredients:** `קמח שיפון מלא (90%), מחמצת שיפון (8%), מלח...`

### לחם מחמצת אמיתי ממחיטה מלאה

**Score:** 79.0  **Grade:** B  **NOVA:** 2  **SC:** B  **GSS:** 87.5
**Fermentation quality:** `traditional`
**Fermentation basis:** ['מחמצת', 'מחמצת חיה']
**Fermentation notes:** Traditional sourdough fermentation at 15.0%. No commercial yeast detected.
**Flour quality class:** 2  **WG dominance:** high
**Design intent:** GENUINE SOURDOUGH — only leavening is live sourdough culture. No commercial yeast. Whole wheat 60%. Long fermentation implied by process claim. This is the gold standard sourdough. Can the system recognize it vs industrial sourdough-style products?
**Ingredients:** `קמח חיטה מלאה (60%), קמח חיטה (35%), מים, מחמצת חיה (15%), מלח...`

### לחם כפרי "מחמצת ושמרים"

**Score:** 70.3  **Grade:** B  **NOVA:** 3  **SC:** D  **GSS:** 51.0
**Fermentation quality:** `flavor_only`
**Fermentation basis:** ['מחמצת', 'pct=8.0%', 'שמרים']
**Fermentation notes:** Sourdough (8.0%) is a minor flavor contributor; commercial yeast is the structural leavening agent.
**Flour quality class:** 3  **WG dominance:** partial
**Design intent:** MIXED LEAVENING SYSTEM — both sourdough (8%) and commercial yeast (1.5%). 'כפרי' (rustic/farmhouse) marketing. Refined wheat dominates (50% vs 40% whole). Genuinely intermediate: sourdough is substantial but not sole leavening. Fermentation semantics should distinguish this from pure sourdough.
**Ingredients:** `קמח חיטה מלאה (40%), קמח חיטה (50%), מים, שמרים (1.5%), מחמצת (8%), מלח, שמן זית (2%), E-471...`

### לחם "בסגנון מחמצת" תעשייתי

**Score:** 64.8  **Grade:** C  **NOVA:** 3  **SC:** D  **GSS:** 26.0
**Fermentation quality:** `flavor_only`
**Fermentation basis:** ['מחמצת מגובשת', 'commercial_leavener_confirmed']
**Fermentation notes:** Dehydrated/powdered sourdough is a flavor agent, not a leavening system. Commercial yeast/chemical leaveners do the actual leavening.
**Flour quality class:** 5  **WG dominance:** none
**Design intent:** DECEPTIVE SOURDOUGH — 'מחמצת מגובשת' (dehydrated sourdough powder) at 2% is a flavor ingredient, not a leavening system. Commercial yeast does the fermentation. Lactic acid added chemically for sour taste. Two additives (E-471, E-481), preservative. The sourdough claim is technically present but structurally meaningless.
**Ingredients:** `קמח חיטה, מים, שמרים, מחמצת מגובשת (2%), מלח, גלוטן חיטה, E-471, E-481, חומר שימור E-282, חומצה לקטית...`

### קרקר "מחמצת" בייצור מהיר

**Score:** 63.5  **Grade:** C  **NOVA:** 3  **SC:** C  **GSS:** 50.0
**Fermentation quality:** `traditional`
**Fermentation basis:** ['מחמצת']
**Fermentation notes:** Traditional sourdough fermentation at 5.0%. No commercial yeast detected.
**Flour quality class:** 5  **WG dominance:** none
**Design intent:** MIXED FERMENTATION SIGNAL — 5% sourdough is real but chemical leaveners (E-450, E-500) do the actual leavening work. Lactic acid added separately. The sourdough is a flavor contributor, not a structural fermentation system. Routing should see: mחמצת present but leavening_agent additives also present — ambiguous signal.
**Ingredients:** `קמח חיטה (65%), קמח שיפון (20%), מחמצת (5%), מלח, שמן קנולה, E-450, E-500, חומצה לקטית...`

## Fermentation Gradient Score Table

Expected: Traditional (highest GSS) → None (lowest GSS)

| Product                       | Ferm Quality | GSS   | Score | Grade |
|-------------------------------|--------------|-------|-------|-------|
| לחמי קריספ מחמצת שיפון מסורתי | traditional  | 100.0 | 79.4  | B     |
| לחם מחמצת אמיתי ממחיטה מלאה   | traditional  | 87.5  | 79.0  | B     |
| לחם כפרי "מחמצת ושמרים"       | flavor_only  | 51.0  | 70.3  | B     |
| לחם "בסגנון מחמצת" תעשייתי    | flavor_only  | 26.0  | 64.8  | C     |
| קרקר "מחמצת" בייצור מהיר      | traditional  | 50.0  | 63.5  | C     |

## Cross-Group Fermentation Summary

All products with any fermentation marker, regardless of group:

| Grp | Product                       | Ferm Quality | GSS   | Score |
|-----|-------------------------------|--------------|-------|-------|
| D   | לחמי קריספ מחמצת שיפון מסורתי | traditional  | 100.0 | 79.4  |
| D   | לחם מחמצת אמיתי ממחיטה מלאה   | traditional  | 87.5  | 79.0  |
| D   | לחם כפרי "מחמצת ושמרים"       | flavor_only  | 51.0  | 70.3  |
| D   | לחם "בסגנון מחמצת" תעשייתי    | flavor_only  | 26.0  | 64.8  |
| D   | קרקר "מחמצת" בייצור מהיר      | traditional  | 50.0  | 63.5  |

## Validation Assessment

### Correct Identifications

| Signal | Expected | Classified | Status |
|--------|----------|------------|--------|
| Genuine sourdough (מחמצת חיה / no שמרים) | traditional | traditional | ✓ |
| Mixed system (מחמצת + שמרים) | mixed_industrial | flavor_only/mixed | ⚠ |
| Dehydrated powder (מחמצת מגובשת) | flavor_only | flavor_only | ✓ |
| Sourdough style name, no ingredient | theater | theater | ✓ |
| No fermentation markers | none | none | ✓ |

### Known Limitation

The `classify_fermentation_quality` function classifies `מחמצת + שמרים` as
`mixed_industrial` (partial fermentation benefit). However, some products use
low-percentage sourdough (2-5%) as a flavor additive while commercial yeast does
all the leavening. These should be `flavor_only`, not `mixed_industrial`.

The percentage-based gate (`sourdough_pct < 10 AND has_yeast → flavor_only`) handles
this for products where percentage is declared. When percentage is undeclared,
the function defaults to `mixed_industrial` — which may overstate the fermentation benefit.