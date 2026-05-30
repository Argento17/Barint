# BSIP2 Score Synthesis — Real Corpora Combined Report

**Generated:** 2026-05-24 17:11 UTC
**Synthesis version:** score_synthesis_v1
**Total products:** 98 across 2 corpora

## Corpus Summary

| Corpus     | N  | ↑Up | =Same | ↓Down | Grade Changes | Eng Nuance Fired |
|------------|----|-----|-------|-------|---------------|------------------|
| cereals    | 45 | 0   | 45    | 0     | 0             | 0                |
| snack_bars | 53 | 1   | 45    | 7     | 0             | 8                |

## Structural Class Distribution (combined)

| SC | Count |
|----|-------|
| A  | 7     |
| B  | 9     |
| D  | 41    |
| E  | 21    |
| F  | 20    |

## Synthesis v1 Scope for Non-Bakery Corpora

### What fires
- **Engineering nuance** (class D/E/F only): gluten-free (+7 w/ isolated fiber, +3 without),
  keto (+8 w/ isolated fiber, +2 without), protein-functional (+1.5),
  hyper-palatable class-F confirmation (−3).

### What does NOT fire (requires bakery_semantics)
- **Fiber source quality discount** — no GSS, no fiber_source_quality computed
- **Fermentation credit** — no fermentation_quality computed
- **GSS coherence adjustment** — grain_structure_score not available

### Implication
The synthesis pass-through rate for non-bakery is high (~80–90%) by design.
Products that shift are those where structural class + L3 signals clearly indicate
engineering intent (hyper-palatable F-class) or functional necessity (GF/keto E-class).

## Engineering Nuance Activations (all products)

| Corpus     | Product                            | Base | Synth | Δ    | Adj  | SC | Reason                                                  |
|------------|------------------------------------|------|-------|------|------|----|---------------------------------------------------------|
| snack_bars | חטיפי דגנים פיטנס קרם ועוגיות שישי | 25.7 | 22.7  | -3.0 | -3.0 | F  | engineering_nuance: hyper-palatable reconstruction conf |
| snack_bars | חטיף דגנים שוקו וניל נסטלה שישייה  | 28.5 | 25.5  | -3.0 | -3.0 | F  | engineering_nuance: hyper-palatable reconstruction conf |
| snack_bars | סיני מיניס חטיף בטעם קינמון על שכב | 27.0 | 24.0  | -3.0 | -3.0 | F  | engineering_nuance: hyper-palatable reconstruction conf |
| snack_bars | חטיפי דגנים פיטנס שוקולד בננה שישי | 25.0 | 22.0  | -3.0 | -3.0 | F  | engineering_nuance: hyper-palatable reconstruction conf |
| snack_bars | חטיף דגנים מצופה שוקולד עם עוגיות  | 16.9 | 13.9  | -3.0 | -3.0 | F  | engineering_nuance: hyper-palatable reconstruction conf |
| snack_bars | חטיף דגנים מצופה שוקולד חלב עם שבר | 18.1 | 15.1  | -3.0 | -3.0 | F  | engineering_nuance: hyper-palatable reconstruction conf |
| snack_bars | חטיף דגנים עם שברי אגוזים ושוקולד  | 31.1 | 28.1  | -3.0 | -3.0 | F  | engineering_nuance: hyper-palatable reconstruction conf |
| snack_bars | מרבה סלים דליס שוקולד חלב ללא גלוט | 59.2 | 62.2  | +3.0 | +3.0 | D  | engineering_nuance: gluten-free = structural limitation |

## Products Remaining Unchanged (synthesis pass-through)

These products are candidates for v2 synthesis extensions:
- Isolated fiber inflation (chicory/inulin in granola/cereal bars) → needs fiber_source detection
- Fortification compensation (NOVA4 cereals with vitamins) → needs matrix_integrity signals
- Protein realism (protein cereals with moderate isolate) → protein_quality already in score_engine

## Recommended v2 Extensions for Non-Bakery

1. **Fiber source classification** (from signal_extractor L3): isolated fiber markers already
   detected in L3.extracted_matrix_markers — can be wired to synthesis without bakery_semantics.
2. **Matrix integrity integration**: run matrix_integrity.py in the batch pipeline and pass
   engineering_intensity + transformation_type to synthesis.
3. **NOVA4 + fortification discount**: wellness_engineering fortification (currently untested)
   maps to synthesis penalty once protein shake / sports bar categories are added.