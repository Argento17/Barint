# Dual Extractor Consensus Report

Generated: 2026-06-13T17:17:42.762067+00:00

## Summary
- Products cross-checked: **3**
- Gemini calls succeeded: **3**
- Fields with both extractors: **27**
- Fields AGREE: **27** (includes BOTH_NULL)
- Fields DISAGREE: **0**
- Gemini calls unavailable: **0**
- Fields FLAG (one-missing): **0**
- Agreement rate: **100.0%**

### Per-field verdict tallies

| Field | AGREE | DISAGREE | FLAG | B_UNAVAILABLE |
|---|---:|---:|---:|---:|
| energy_kcal | 3 | 0 | 0 | 0 |
| protein_g | 3 | 0 | 0 | 0 |
| fat_g | 3 | 0 | 0 | 0 |
| fat_saturated_g | 3 | 0 | 0 | 0 |
| carbohydrates_g | 3 | 0 | 0 | 0 |
| sugars_g | 3 | 0 | 0 | 0 |
| dietary_fiber_g | 3 | 0 | 0 | 0 |
| sodium_mg | 3 | 0 | 0 | 0 |
| ingredients | 3 | 0 | 0 | 0 |

Tolerance: abs=0.1, rel=1.0%

## Fabrication Guard

Gemini prompt explicitly forbids: (1) inferring/estimating values, (2) using outside world knowledge, (3) using Open Food Facts or any external source (TASK-238). Disagreements with the rule-based parser are the consensus check — if Gemini invents a value it disagrees with Extractor A and is FLAGGED, never silently accepted.

## Factory Wiring

dual_extract.py runs at the extraction stage (post-scrape, pre-BSIP1). Fields with DISAGREE or FLAG verdict block auto-publish and route to human review. Only AGREE fields are promoted to the scored pipeline. B-side 'unavailable' (Gemini timeout/error) triggers manual review of the affected product — it does not crash the pipeline.

## Product: קרקר בדיקה סינטטי (barcode 9990000000001)

| Field | Extractor A (rule-based) | Extractor B (Gemini) | Verdict |
|---|---|---|---|
| energy_kcal | 450.0 | 450.0 | AGREE |
| protein_g | 8.0 | 8.0 | AGREE |
| fat_g | 18.0 | 18.0 | AGREE |
| fat_saturated_g | 3.0 | 3.0 | AGREE |
| carbohydrates_g | 62.0 | 62.0 | AGREE |
| sugars_g | 4.0 | 4.0 | AGREE |
| dietary_fiber_g | 3.5 | 3.5 | AGREE |
| sodium_mg | 420.0 | 420.0 | AGREE |
| ingredients | קמח חיטה, שמן דקלים, מלח, שמשום | קמח חיטה, שמן דקלים, מלח, שמשום | AGREE |

## Product: עוגיית שוקולד בדיקה סינטטי (barcode 9990000000002)

| Field | Extractor A (rule-based) | Extractor B (Gemini) | Verdict |
|---|---|---|---|
| energy_kcal | 520.0 | 520.0 | AGREE |
| protein_g | 6.0 | 6.0 | AGREE |
| fat_g | 28.0 | 28.0 | AGREE |
| fat_saturated_g | 16.0 | 16.0 | AGREE |
| carbohydrates_g | 60.0 | 60.0 | AGREE |
| sugars_g | 38.0 | 38.0 | AGREE |
| dietary_fiber_g | 2.0 | 2.0 | AGREE |
| sodium_mg | 80.0 | 80.0 | AGREE |
| ingredients | קמח, סוכר, שוקולד, חמאה, שמן דקלים, מצק פרה, גליצרין, חומצת לימון | קמח, סוכר, שוקולד, חמאה, שמן דקלים, מצק פרה, גליצרין, חומצת לימון | AGREE |

## Product: חטיף בדיקה סינטטי שיבולת שועל (barcode 9990000000003)

| Field | Extractor A (rule-based) | Extractor B (Gemini) | Verdict |
|---|---|---|---|
| energy_kcal | 370.0 | 370.0 | AGREE |
| protein_g | 14.0 | 14.0 | AGREE |
| fat_g | 7.0 | 7.0 | AGREE |
| fat_saturated_g | 1.2 | 1.2 | AGREE |
| carbohydrates_g | 66.0 | 66.0 | AGREE |
| sugars_g | 12.0 | 12.0 | AGREE |
| dietary_fiber_g | 8.0 | 8.0 | AGREE |
| sodium_mg | 150.0 | 150.0 | AGREE |
| ingredients | שיבולת שועל מלאה, דבש, צימוקי פירות, קינמון | שיבולת שועל מלאה, דבש, צימוקי פירות, קינמון | AGREE |
