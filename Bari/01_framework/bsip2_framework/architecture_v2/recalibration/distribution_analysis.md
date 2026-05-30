# Score Distribution Analysis — Current State

**Status:** Recalibration evidence  
**Version:** 2.0-draft  
**Date:** 2026-05-18  
**Sources:** run_003 milk corpus (n=20), snack_bars latest_review corpus (n=49 scored, 5 insufficient)  
**Companion:** grade_philosophy_v2.md, penalty_pressure_analysis.md

---

## Summary Verdict

The current system produces a **downward-compressed distribution** with:
- **Zero products above 75** across 69 scored products
- **Zero A grades** (threshold: 85+)
- **~80% D or E grades** across both corpora
- **Massive clustering** in the 40–55 range
- **Empty upper range**: the 65–100 band contains fewer than 10% of products

This pattern is not evidence of a categorically bad food landscape. It is evidence of a scoring system whose calibration understates the structural quality of genuinely good products and creates a false floor for the center of the distribution.

---

## Corpus Overview

| Corpus | Products scored | Min | Max | Mean | Median |
|--------|----------------|-----|-----|------|--------|
| Milk & alternatives (run_003) | 20 | 36.2 | 75 | 54.5 | 48.7 |
| Snack bars (latest_review) | 49 | 12.4 | 65 | 35.6 | 38.7 |
| Combined | 69 | 12.4 | 75 | 43.0 | 43.4 |

The combined median is 43.4 — squarely in D territory under current thresholds. The combined maximum is 75, which is itself a floor value (not a naturally computed score — see section below).

---

## The 75 Ceiling Illusion

The three highest milk scores (whole milk 3.4%, 4% milk, goat milk) all report **75**. This is not their computed score. Their actual weighted dimension scores are:
- Whole milk 3.4%: weighted score = **69.54**
- 4% milk: weighted score = **70.44**
- Goat milk: similar range

These products score 70 organically. They reach 75 only because the **NOVA1_SINGLE_FLOOR = 75** is applied after scoring.

Without this floor, the highest-scoring product in the combined corpus would be **73.2** (lactose-free enhanced milk, NOVA 2).

**The true maximum natural score across 69 products is ~70.44.**

This is the core compression problem. The system's ceiling is effectively ~70 for all products that don't receive a structural floor protection. A grade of A (currently 85+) is not merely hard to reach — it is **structurally unreachable** given current formulas and caps.

---

## Milk Corpus Distribution

### Score bands

| Score range | Products | % | Notes |
|-------------|----------|---|-------|
| 75–79 | 4 | 20% | All floor-rescued NOVA 1 single-ingredient products |
| 70–74 | 1 | 5% | Lactose-free enhanced (NOVA 2) |
| 65–69 | 1 | 5% | Plain soy drink (NOVA 2) |
| 55–64 | 2 | 10% | Fortified 1% milk (NOVA 3), NOVA 3 soy |
| 50–54 | 2 | 10% | Generic almond, plain oat |
| 45–49 | 8 | 40% | Oat variants, plant-based cluster |
| 40–44 | 1 | 5% | Alpro almond |
| 35–39 | 2 | 10% | Go Milk protein, Alpro soy chocolate |

### Key clustering observation

**40% of the corpus (8 products) sits in a 4-point band: 45.0–49.1.**

These 8 products include: Alpro oat plain, both Barista oat variants, oat barista for foaming, organic rice drink, Alpro soy barista, plain oat generic, and Go Milk protein drink. These are structurally distinct products — some NOVA 3, some NOVA 4 — but they cluster within 4 points of each other. This is compression, not precision.

### Grade distribution (current thresholds: B=70+, C=55+, D=40+, E<40)

| Grade | Count | % |
|-------|-------|---|
| A | 0 | 0% |
| B | 4 | 20% |
| C | 3 | 15% |
| D | 11 | 55% |
| E | 2 | 10% |

The D grade carries 55% of all milk products — more than half the category in a single grade bucket. This is not a meaningful distribution.

---

## Snack Bar Corpus Distribution

### Score bands

| Score range | Products | % | Notes |
|-------------|----------|---|-------|
| 60–69 | 1 | 2% | Date-almond butter bar (NOVA 2) |
| 55–59 | 5 | 10% | NOVA 2–3 bars with no heavy caps |
| 50–54 | 7 | 14% | NOVA 3 bars, various categories |
| 45–49 | 7 | 14% | NOVA 3–4 transition zone |
| 40–44 | 7 | 14% | NOVA 4 with moderate cap stacking |
| 35–39 | 2 | 4% | NOVA 4 with heavy sugar + processing |
| 25–34 | 8 | 16% | NOVA 4 with combined sugar + processing caps |
| 15–24 | 10 | 20% | NOVA 4 with full cap stacking |
| below 15 | 2 | 4% | Maximally compromised (2+ red labels + NOVA 4 + 5+ additives) |

### Key clustering observations

**The 40–55 range contains 21 of 49 products (43%)** — nearly half the corpus compressed into a 15-point band.

The **15–35 range contains 20 products (41%)** — these are products where multiple caps have stacked. The spread from 12.4 to 35 represents structurally different products (some with 3 caps, some with 8) compressed into the same E grade.

The **top score is 65** — no product in the entire snack bar corpus reaches B grade (currently 70+). The highest-scoring snack bar is a date-stuffed whole-food product, and even it can't reach B.

### Grade distribution (current thresholds)

| Grade | Count | % |
|-------|-------|---|
| A | 0 | 0% |
| B | 0 | 0% |
| C | 6 | 12% |
| D | 21 | 43% |
| E | 22 | 45% |

**B grade: 0%.** The system cannot produce a B grade for any snack bar in this corpus. This is not because there are no good snack bars — the date-almond butter bar is a genuine NOVA 2 whole-food product with no additives and coherent composition. The system simply can't reward it above 65.

---

## Combined Grade Utilization

| Grade | Milk % | Snack bar % | Combined % |
|-------|--------|-------------|------------|
| A | 0% | 0% | 0% |
| B | 20% | 0% | 7% |
| C | 15% | 12% | 13% |
| D | 55% | 43% | 48% |
| E | 10% | 45% | 30% |

**The A grade achieves 0% utilization across all 69 products.**  
The combined D + E population is **78%** of all scored products.

This is the grade utilization problem. It is not solved by "making things score higher" — it is solved by recalibrating the grade boundaries and removing the ceiling compression that prevents excellent products from reaching their appropriate range.

---

## Cliff Transitions

### The NOVA 3 → NOVA 4 cliff (milk corpus)

Looking at the milk corpus ordered by NOVA level and score:

| NOVA level | Sample products | Score range |
|-----------|----------------|-------------|
| NOVA 1 | Whole milk, goat milk | 75 (floor) |
| NOVA 2 | Lactose-free enhanced, plain soy | 66–73 |
| NOVA 3 | Fortified 1% milk, NOVA3 soy, oat drinks | 46–58 |
| NOVA 4 | Muller protein, Alpro almond, Go Milk, Alpro soy chocolate | 36–48 |

NOVA 2 → NOVA 3 drop: ~8–15 points average  
NOVA 3 → NOVA 4 drop: ~8–10 points in this corpus  

The cliff is less dramatic in the milk corpus than in snack bars because most milk products don't hit their processing caps — their dimension scores are already below the caps. But the structural ceiling compression still prevents NOVA 3 products from exceeding 65 without extremely favorable nutritional profiles.

### The NOVA 3 → NOVA 4 cliff (snack bar corpus)

In snack bars, where NOVA 4 products frequently hit the NOVA_PROXY_4 cap at 60, the cliff is visible as a categorical separation:

Products at NOVA 3 peak at ~57. Products at NOVA 4 start at ~48 (with low additive count) and descend to 12 (with full cap stacking).

The gap between best NOVA 3 (~57) and best NOVA 4 (~48) is ~9 points. But for higher-quality NOVA 3 products that would naturally score 65+ (e.g., the date-chocolate bar at 55.8 which scored 55.8 before caps), the NOVA 3 → 4 boundary represents a 15–20 point effective cliff because of combined cap changes. See `penalty_pressure_analysis.md` for detailed quantification.

---

## Underutilized Score Ranges

| Range | Products | % | Assessment |
|-------|----------|---|------------|
| 85–100 | 0 | 0% | Completely empty — S and upper A |
| 75–84 | 0 | 0% | Lower A entirely empty (floor at 75 hits the top of B) |
| 65–74 | 2 | 3% | Upper B — only 2 products reach naturally |
| 55–64 | 8 | 12% | Lower B/upper C — modest utilization |
| 40–54 | 30 | 43% | C-D boundary — massively overloaded |
| 25–39 | 17 | 25% | Lower D / E boundary |
| below 25 | 12 | 17% | Deep E — legitimately problematic products |

The 65–100 range (which should contain A and B grades) holds only 2 products (3% of corpus).  
The 40–54 range (which spans D into C) holds 30 products (43% of corpus).

**The system has inverted the natural distribution.** In a well-calibrated system, the middle grades (B and C) should be the most populated. Currently, D is the most populated grade.

---

## Root Cause Summary

Three structural mechanisms cause the observed compression:

**1. Floor as ceiling.** The NOVA1_SINGLE_FLOOR at 75 is also the effective upper ceiling of the system for most products. Because natural dimension scores for even excellent products (dairy) compute to ~69–71, the floor becomes the grade for every high-quality product — and simultaneously marks the upper boundary. Nothing can be better than 75 except by reaching 85+ (currently impossible).

**2. NOVA as dominant gravity.** NOVA 3 and 4 products carry a structural weight disadvantage that, combined with caps at 75 and 60, compresses the entire middle of the distribution into the 40–60 range. A NOVA 3 product would need an implausibly high nutritional profile to naturally exceed 70 before caps.

**3. Cap stacking without proportional relief.** In the snack bar corpus, multiple caps stack to binding minimums as low as 45 (ISRAELI_LABELS_2_PLUS cap). From this starting point, penalties reduce further. Products with partially different structural profiles land in the same 20–35 range because all of them hit the 45 binding cap.

The proposed recalibration in `recalibration_proposals.md` addresses all three mechanisms while preserving rank ordering and structural conviction.

---

*Next: See `penalty_pressure_analysis.md` for quantitative breakdown of each pressure source.*
