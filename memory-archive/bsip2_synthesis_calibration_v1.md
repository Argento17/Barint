---
name: bsip2-synthesis-calibration-v1
description: "BSIP2 Score Synthesis Layer v1 — post-score calibration integrating fiber, fermentation, GSS, engineering nuance. Sprint outcomes, constants, file locations."
metadata:
  type: project
  originSessionId: synthesis-calibration-2026-05-24
---

Score Synthesis Calibration v1 completed 2026-05-24. Closes the gap between rich bakery
ontology signals (GSS, fiber source, fermentation) and the final synthesis score.

**New files:**
- `C:\Bari\03_operations\bsip2\proto_v0\src\score_synthesis.py` — synthesis engine (v1)
- `C:\Bari\03_operations\bsip2\proto_v0\src\batch_run_synthesis_calibration_001.py` — calibration runner
- `C:\Bari\03_operations\bsip2\proto_v0\src\generate_synthesis_calibration_reports.py` — 6-report generator

**Reports:**
`C:\Bari\03_operations\reports\synthesis_calibration\` — 6 files (calibration_001, score_shift, fiber_impact, fermentation, structural_coherence, engineered_systems)

**MODULE_VERSION:** `score_synthesis_v1`

---

## Architecture

`run_synthesis(trace)` takes a fully assembled BSIP2 trace (after bakery_semantics + structural_class attached)
and returns `synthesis_result` dict. Applied in the batch runner AFTER `assemble_trace()`.

**Four components:**

### 1. Fiber Source Quality Discount (bakery only)
- `isolated` + fiber ≥ 6g: −14
- `isolated` + fiber ≥ 4g: −10
- `isolated` + fiber ≥ 2g: −7
- `isolated` + fiber < 2g: −4
- `hybrid` (grain + isolated additives): −4
- `structural` + fiber ≥ 6g: +1.5
- `structural` < 6g or `minimal` or `unknown`: 0

### 2. Fermentation Credit (bakery only)
- `traditional` + fqc ≤ 2: +6
- `traditional` + fqc = 3: +4
- `traditional` + fqc ≥ 4: +2
- `mixed_industrial`: +1.5
- `flavor_only`: −3
- `theater`: −5
- `none`: 0

### 3. GSS Coherence Adjustment (bakery only)
**Class A/B/C receive upward adjustments; class D/E/F receive only downward or neutral.**
- GSS ≥ 85, class A/B: +6
- GSS ≥ 85, class C: +3
- GSS 70–84, class A/B: +4
- GSS 70–84, class C: +2.5
- GSS 55–69, class A/B: +2
- GSS 55–69, class C: +0.5
- GSS 40–54: 0 (neutral zone for all classes)
- GSS 25–39, class D/E/F: −4
- GSS 12–24, class D/E/F: −7
- GSS < 12, class D/E/F: −10

### 4. Engineering Type Nuance (all categories, class D/E/F only)
- Gluten-free + isolated fiber: +7 (dietary necessity, offsets fiber discount)
- Gluten-free + non-isolated fiber: +3
- Keto + isolated fiber: +8 (psyllium/coconut fiber = format requirement)
- Keto + non-isolated: +2
- Protein-functional (isolate + no sweetener + ≤3 additives): +1.5
- Hyper-palatable F-class (sweetener + ≥3 additives + non-isolate): −3

**Caps:** max upward = +10, max downward = −18

---

## Calibration Results (32 bread_light products)

| Group | Avg Base | Avg Synth | Avg Δ |
|-------|----------|-----------|-------|
| A (baselines) | 67.8 | 68.4 | +0.6 |
| B (wholegrain halo) | 65.8 | 59.5 | −6.3 |
| C (seed halo) | 64.0 | 63.2 | −0.8 |
| D (sourdough spectrum) | 71.4 | 73.8 | +2.4 |
| E (engineered wellness) | 64.0 | 58.7 | −5.3 |
| F (hyper-palatable) | 42.7 | 41.1 | −1.6 |

**Grade changes:** 12 products changed grade
- Grade A: 1→6 (+5)
- Grade B: 15→8 (−7)
- Grade D: 4→7 (+3)

**Key corrections:**
- Traditional sourdough rye (GSS=100, fqc=1): 79.4 → 89.4 (B→A) ✓
- Real sourdough whole wheat (GSS=87.5, fqc=2): 79.0 → 89.0 (B→A) ✓
- Isolated-fiber crackers (GSS=16, refined): 65.8/67.0/68.1 → 47.8/49.0/50.1 (B→D) ✓
- Fermentation theater (GSS=26, flavor_only): 64.8 → 57.8 (C lower) ✓
- GF bread (isolated necessity): 52.3 → 45.3 (C→D, mild) ✓
- Keto bread (isolated necessity): 49.0 → 43.0 (D, protected) ✓

---

## Integration Pattern

```python
# In batch runners:
bakery_result = run_bakery_semantics(product, category, l3)
trace["bakery_semantics"] = bakery_result
trace["structural_class"] = classify_structural_class(trace, bakery_result)
trace["synthesis_result"] = run_synthesis(trace)  # NEW
```

`synthesized_score` and `synthesized_grade` are the preferred outputs in synthesis-aware runners.
`base_score` (from score_engine) preserved in synthesis_result for comparison.

---

## Known Limitations / Next Steps

1. **Non-bakery categories**: synthesis is pass-through — GSS/fermentation not available for cereals, snack bars.
2. **FQC position proxy**: flour % is undeclared — multigrain % ambiguity persists (run_002 gap #4).
3. **Matrix integrity integration**: matrix_integrity.py signals (engineering_intensity, transformation_type) not yet in synthesis — planned for v2.
4. **Beta-glucan from real oats**: currently classified as "isolated" if extracted beta-glucan markers appear, even when the product contains real oats. May slightly over-penalize.

**Why:** The score_engine computes NOVA/nutrients/guardrails correctly but cannot see bakery structural coherence. The synthesis layer is the bridge — it reads what bakery_semantics computed and translates it into score adjustments.
