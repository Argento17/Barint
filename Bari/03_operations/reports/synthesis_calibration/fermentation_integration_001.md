# Fermentation Quality Integration — synthesis_calibration_001

**Generated:** 2026-05-24 17:03 UTC

## Fermentation Quality Tiers and Score Impact

| Tier | Synthesis Credit | Condition |
|------|-----------------|-----------|
| traditional + fqc ≤ 2 | +6 | Genuine sourdough on whole-grain dominant flour |
| traditional + fqc = 3 | +4 | Genuine sourdough on mixed flour |
| traditional + fqc ≥ 4 | +2 | Genuine sourdough on refined flour (reduced coherence) |
| mixed_industrial | +1.5 | Sourdough starter + commercial yeast |
| none | 0 | No fermentation markers |
| flavor_only | −3 | Dehydrated/minor sourdough — commercial yeast does leavening |
| theater | −5 | Sourdough name but no sourdough ingredient |

### fermentation_quality = traditional (3 products)
**Avg base:** 74.0  |  **Avg synthesized:** 81.3  |  **Avg Δ:** +7.3

| Grp | Product                       | Base | Synth | Total Δ | Ferm Adj | SC | GSS |
|-----|-------------------------------|------|-------|---------|----------|----|-----|
| D   | לחמי קריספ מחמצת שיפון מסורתי | 79.4 | 89.4  | +10.0   | +6.0     | B  | 100 |
| D   | לחם מחמצת אמיתי ממחיטה מלאה   | 79.0 | 89.0  | +10.0   | +6.0     | B  | 88  |
| D   | קרקר "מחמצת" בייצור מהיר      | 63.5 | 65.5  | +2.0    | +2.0     | C  | 50  |

### fermentation_quality = none (26 products)
**Avg base:** 62.2  |  **Avg synthesized:** 59.1  |  **Avg Δ:** -3.1

| Grp | Product                           | Base | Synth | Total Δ | Ferm Adj | SC | GSS |
|-----|-----------------------------------|------|-------|---------|----------|----|-----|
| A   | עוגיות אורז ללא מלח               | 85   | 87.0  | +2.0    | —        | A  | 57  |
| A   | לחמי קריספ שיפון פשוט             | 79.3 | 84.8  | +5.5    | —        | B  | 82  |
| A   | קרקר חיטה מלאה פשוט               | 79.7 | 83.2  | +3.5    | —        | B  | 70  |
| C   | לחמי קריספ שיפון וגרעינים נורדי   | 79.4 | 81.4  | +2.0    | —        | C  | 70  |
| C   | לחם גרעינים אמיתי                 | 77.2 | 79.2  | +2.0    | —        | C  | 70  |
| E   | לחמי קריספ חלבון ופשתן "17 גרם"   | 74.9 | 76.9  | +2.0    | —        | C  | 70  |
| E   | לחם חלבון ואגוזים "נוטרישן"       | 71.7 | 73.2  | +1.5    | —        | D  | 57  |
| B   | לחם "100% חיטה מלאה" מעורב        | 71.1 | 71.6  | +0.5    | —        | C  | 57  |
| B   | לחמי קריספ "14 גרם סיבים" תאית    | 73.5 | 69.5  | -4.0    | —        | D  | 62  |
| E   | קרקר חלבון 30 "פרוטין קריספ"      | 69.0 | 65.0  | -4.0    | —        | D  | 32  |
| B   | קרקרים "5 דגנים" ושיפון           | 63.4 | 64.9  | +1.5    | —        | D  | 57  |
| F   | עוגיות אורז "חמאה" שמן דקל        | 58.1 | 58.1  | +0.0    | —        | D  | 57  |
| A   | לחם לבן פרוס פשוט                 | 59.2 | 55.2  | -4.0    | —        | D  | 32  |
| C   | קרקרים "שבעת המינים" גרעינים      | 55.2 | 55.2  | +0.0    | —        | D  | 44  |
| B   | לחם "7 דגנים" תעשייתי             | 53.0 | 53.0  | +0.0    | —        | E  | 57  |
| F   | עוגיות אורז שוקולד "בלה שוקו"     | 51.0 | 51.0  | +0.0    | —        | F  | 57  |
| C   | קרקר "פשתן וצ'יה" סופר-פוד        | 54.8 | 50.8  | -4.0    | —        | D  | 32  |
| B   | קרקרים "מולטיגריין" עשיר בסיבים   | 68.1 | 50.1  | -18.0   | —        | D  | 16  |
| C   | קרקר "גרעינים זהובים" פרמיום      | 53.4 | 49.4  | -4.0    | —        | D  | 32  |
| E   | קרקר "סיבים+" אינולין וסיליום     | 67.0 | 49.0  | -18.0   | —        | D  | 16  |
| B   | קרקר "בטא-גלוקן" תומך בלב         | 65.8 | 47.8  | -18.0   | —        | D  | 16  |
| E   | לחם "ללא גלוטן" עמילן תפוחי אדמה  | 52.3 | 45.3  | -7.0    | —        | D  | 16  |
| E   | לחם "קטו" דל פחמימות              | 49.0 | 43.0  | -6.0    | —        | E  | 41  |
| F   | לחמי קריספ "שום ועשבים" תעשייתי   | 40.6 | 36.6  | -4.0    | —        | E  | 32  |
| A   | קרקר מלוח פריך                    | 36.0 | 32.0  | -4.0    | —        | D  | 32  |
| F   | קרקרים מתוקים לילדים "גולדה קידס" | 28.4 | 24.4  | -4.0    | —        | E  | 32  |

### fermentation_quality = flavor_only (2 products)
**Avg base:** 67.5  |  **Avg synthesized:** 62.5  |  **Avg Δ:** -5.0

| Grp | Product                    | Base | Synth | Total Δ | Ferm Adj | SC | GSS |
|-----|----------------------------|------|-------|---------|----------|----|-----|
| D   | לחם כפרי "מחמצת ושמרים"    | 70.3 | 67.3  | -3.0    | -3.0     | D  | 51  |
| D   | לחם "בסגנון מחמצת" תעשייתי | 64.8 | 57.8  | -7.0    | -3.0     | D  | 26  |

## Key Findings

- **Traditional sourdough + whole-grain** (fqc ≤ 2) earned maximum fermentation credit (+6).
  Combined with high GSS, these products gained +10 (capped), reaching Grade A.
- **Traditional sourdough + refined flour** (fqc ≥ 4) earned only +2 — genuine fermentation
  on a refined base is less coherent and does not fully earn the structural credit.
- **Flavor-only sourdough** (dehydrated starter + commercial yeast) received −3 penalty,
  reflecting that the fermentation claim is deceptive at the system level.
- **Fermentation theater** (sourdough name, no sourdough ingredient) received −5.

## Ambiguous Cases

- **Mixed_industrial** systems (sourdough + yeast) earned +1.5 credit. This is conservative.
  If the sourdough fraction is ≥30%, this may understate the fermentation benefit.
  The system cannot distinguish 5% sourdough (flavor) from 40% sourdough (meaningful)
  within the mixed_industrial tier when no % is declared.

## Overcorrection Risk

- Do NOT over-expand the fermentation credit in v2. The current +6 maximum
  is already significant. Risk: rewarding fermentation theater that passes as traditional
  when ingredient inspection is insufficient.