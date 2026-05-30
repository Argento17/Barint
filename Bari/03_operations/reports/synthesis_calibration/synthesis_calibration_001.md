# BSIP2 Score Synthesis Calibration v1 — Overview

**Generated:** 2026-05-24 17:03 UTC
**Corpus:** bread_light (32 synthetic products across 6 stress groups)
**Synthesis version:** score_synthesis_v1

## Overview

The Score Synthesis Layer v1 integrates four structural coherence signals
that the base score_engine cannot see:
- Fiber source quality (structural grain vs isolated extracted fiber)
- Fermentation quality (traditional → theater)
- Grain Structure Score (GSS) coherence gradient
- Engineering type nuance (gluten-free / keto / hyper-palatable protection/amplification)

## Score Shift Statistics

| Metric | Value |
|--------|-------|
| Products scored | 32 |
| Average adjustment | -2.08 pts |
| Maximum upward | +10.0 pts |
| Maximum downward | -18.0 pts |
| Products shifted up | 12 |
| Products unchanged | 5 |
| Products shifted down | 15 |
| Adjustments clamped (±cap) | 5 |
| Grade changes | 12 |

## Grade Distribution: Base vs Synthesized

| Grade             | Base Count | Synth Count | Change |
|-------------------|------------|-------------|--------|
| A                 | 1          | 6           | +5     |
| B                 | 15         | 8           | -7     |
| C                 | 11         | 9           | -2     |
| D                 | 4          | 7           | +3     |
| E                 | 1          | 2           | +1     |
| insufficient_data | 0          | 0           | 0      |

## Group-Level Score Shifts

| Group | N | Avg Base | Avg Synth | Avg Δ |
|-------|---|----------|-----------|-------|
| A     | 5 | 67.8     | 68.4      | +0.6  |
| B     | 6 | 65.8     | 59.5      | -6.3  |
| C     | 5 | 64.0     | 63.2      | -0.8  |
| D     | 5 | 71.4     | 73.8      | +2.4  |
| E     | 6 | 64.0     | 58.7      | -5.3  |
| F     | 5 | 42.7     | 41.1      | -1.6  |

## Synthesis Confidence Distribution

| Confidence | Count |
|------------|-------|
| high       | 7     |
| medium     | 25    |

## Key Observations

### What improved
- Traditional sourdough + whole-grain products: +10 pts (GSS + fermentation coherence)
- Genuine Nordic crispbread: +4–6 pts (high GSS on coherent B-class products)

### What was corrected downward
- Isolated-fiber (inulin/psyllium/cellulose) on refined base: −18 pts (fiber+GSS)
- Fermentation theater bread: −5 to −7 pts (ferm penalty + GSS discount)
- Seed-halo crackers on refined flour: −4 pts (GSS coherence penalty)

### What was protected
- Gluten-free bread (isolated fiber): engineering nuance +7 offsets most of fiber and GSS penalties
- Keto bread (isolated psyllium fiber): engineering nuance +8 reduces net impact from −14 to −6
- Both: isolated fiber in GF/keto baking is dietary necessity, not gaming — protected accordingly

### What was not changed
- Rice cakes (NOVA1, class=A): modest +2 only — already correctly scored
- Corn puffs (non-bakery): no synthesis signals available — unchanged
- Products in the neutral GSS zone (40–55) with no fermentation or fiber issues

## Remaining Calibration Gaps

1. **Non-bakery categories**: synthesis is pass-through — GSS/fermentation not yet available for cereals, snack bars.
2. **FQC position proxy**: no declared flour %, position is the only discriminator — multigrain % ambiguity persists.
3. **Sourdough % threshold**: products with >10% sourdough + yeast still classify as mixed_industrial not flavor_only.
4. **Matrix integrity integration**: matrix_integrity.py signals (engineering_intensity, transformation_type) not yet in synthesis.