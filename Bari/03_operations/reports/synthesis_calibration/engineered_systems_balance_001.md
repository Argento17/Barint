# Engineered Systems Balance — synthesis_calibration_001

**Generated:** 2026-05-24 17:03 UTC

## Philosophy

Not all engineering is equal. The synthesis distinguishes:
- **Functional engineering**: dietary necessity (gluten-free, keto) → protected (+2 to +3)
- **Therapeutic engineering**: nutritional intent with clean label (protein isolate + no sweetener) → modest relief
- **Deceptive engineering**: fiber laundering, sweetener stacking, palatability-first → full structural penalties
- **Hyper-palatable reconstruction** (class F): sweetener + additives + no protein → −3 amplification

The goal: meaningful gradients between these types, not collapse into one 'processed = bad' bucket.

## Gluten-Free Products

| Grp | Product                          | Base | Synth | Total Δ | Eng Adj | SC | GSS |
|-----|----------------------------------|------|-------|---------|---------|----|-----|
| E   | לחם "ללא גלוטן" עמילן תפוחי אדמה | 52.3 | 45.3  | -7.0    | +7.0    | D  | 16  |

## Keto / Low-Carb Products

| Grp | Product              | Base | Synth | Total Δ | Eng Adj | SC | GSS |
|-----|----------------------|------|-------|---------|---------|----|-----|
| E   | לחם "קטו" דל פחמימות | 49.0 | 43.0  | -6.0    | +8.0    | E  | 41  |

## All Engineering Nuance Activations

| Grp | Product                          | Base | Synth | Eng Adj | SC | Reason                                                                 |
|-----|----------------------------------|------|-------|---------|----|------------------------------------------------------------------------|
| E   | לחם "קטו" דל פחמימות             | 49.0 | 43.0  | +8.0    | E  | engineering_nuance: keto + isolated_fiber = dietary structural necessi |
| E   | לחם "ללא גלוטן" עמילן תפוחי אדמה | 52.3 | 45.3  | +7.0    | D  | engineering_nuance: gluten-free + isolated_fiber = structural necessit |

## Key Findings

- **Gluten-free** products had their GSS penalties partially offset (+3 nuance credit),
  correctly distinguishing structural necessity from deceptive reconstruction.
- **Keto bread** received +2 credit, moving from Grade D to Grade C —
  acknowledging therapeutic purpose while maintaining the score below conventional whole-grain products.
- **Isolated-fiber engineering** (inulin/psyllium/cellulose on refined base) received NO protection.
  This is correct: fiber-laundering products have no dietary necessity for isolated additives.

## Overcorrection Risk

- **Gluten-free +3 relief** may protect products that use gluten-free as a marketing angle
  on an otherwise incoherent matrix. Watch for: score ≥ 55 for NOVA4 GF products.
- **Keto +2 relief** is small enough to be low-risk. The NOVA4 guardrail still applies.
- Future: protein bakery products with isolate + sweetener should NOT get engineering_nuance relief.
  Currently this is correctly gated (is_protein_functional requires NO sweetener).