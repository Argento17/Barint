---
id: TASK-284D
title: Measure EV-096/097 blast radius on non-registered published categories: cakes_hard_cookies + cookies_coffee + salty_snacks
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-15
completed_at: 2026-06-15
depends_on: []
blocks: []
category_id: null
summary: >
  Pre-deploy gate: the Shadow run (284B) covered only registered corpora; cakes_hard_cookies + cookies_coffee (where 42+14 of the 49 PHVO/margarine products live) + salty_snacks were NOT measured. Re-score each under its live ship config with BARI_FAT_TECH_V1 OFF (baseline) vs ON (proposed); diff grades. Report per-category grade-movement distribution, EV-097 grade movers among the cakes/cookies PHVO products, EV-096 movers, and frozen/ceiling-invariant check. Measurement ONLY: no published-score writes, flag stays OFF in production.
---

# TASK-284D — Measure EV-096/097 blast radius on non-registered published categories: cakes_hard_cookies + cookies_coffee + salty_snacks

## Results (2026-06-15)

### METHOD
Two-pass subprocess scoring for each category: flag-OFF (BARI_FAT_TECH_V1=off) = baseline /
current published behavior; flag-ON = proposed. Live ship flags held identical to authoritative
batch runners (cakes+cookies: all OFF; salty_snacks: BARI_RECAL_P0=on). Flag-OFF byte-identical
confirmed: 20/20 cakes spot-check vs committed run_cakes_001 traces = zero score delta.
Salty-snacks OFF-pass grade dist matches run_salty_snacks_002 exactly.

### CORPUS COUNTS
- cakes_hard_cookies: 149/149 scored both passes, 0 errors (expected=149)
- cookies_coffee: 58/58 scored both passes, 0 errors (expected=58)
- salty_snacks: 54/54 scored both passes, 0 errors (expected=54)

### GRADE DISTRIBUTIONS

| Category | Grade dist OFF | Grade dist ON | Change |
|---|---|---|---|
| cakes_hard_cookies | E=132 D=12 C=5 | E=131 D=13 C=5 | 1 product E→D |
| cookies_coffee | E=31 D=22 C=5 | E=31 D=22 C=5 | 0 changes |
| salty_snacks | E=4 D=9 C=18 B=16 A=7 | E=4 D=8 C=19 B=16 A=7 | 1 product D→C |

### GRADE CHANGERS (complete table — both are upward, EV-096 attribution)

| Barcode | Category | Score OFF | Grade OFF | Score ON | Grade ON | Δ | Signal |
|---|---|---|---|---|---|---|---|
| 313184 | cakes_hard_cookies | 34.9 | E | 35.3 | D | +0.4 | has_seed_oil=True |
| 8710908800018 | salty_snacks | 49.6 | D | 50.0 | C | +0.4 | has_seed_oil=True (Doritos Cool Ranch) |

**2 grade changes total (both upward, both EV-096 seed-oil, no PHVO/EV-097 involvement).**

### EV-097 ATTRIBUTION (PHVO generic ceiling 40→55)

- cakes_hard_cookies: 41 has_phvo_generic products; 33 score-movers, 8 inert (sat-fat holds ≤40). 0 grade changes.
- cookies_coffee: 14 has_phvo_generic products; 11 score-movers, 3 inert. 0 grade changes.
- salty_snacks: 0 has_phvo_generic products (no margarine/muksha ingredients).
- **Non-registered EV-097 total: 55 PHVO-generic products; 44 move score (within-grade only); 0 grade changes.**
- **PHVO overlap: 7 barcodes appear in BOTH cakes+cookies corpora (48 unique barcodes across both).**

### EV-096 ATTRIBUTION (seed_pen 10→5 grade crossers)
- cakes_hard_cookies: 1 crosser (barcode 313184, E→D)
- cookies_coffee: 0 crossers
- salty_snacks: 1 crosser (barcode 8710908800018, D→C)
- **Non-registered EV-096 total: 2 grade crossers (both upward)**

### COMBINED PICTURE (all categories, registered 284B + non-registered 284D)

| Metric | Registered (284B) | Non-Registered (284D) | Combined |
|---|---|---|---|
| Products scored | 704 | 261 | 965 |
| Score movers | 62 | 141 | 203 |
| Grade changers | 2 | 2 | 4 (all upward) |
| EV-097 PHVO-generic total | 49 | 55 | ~104 (48 shared barcodes) |
| EV-097 score-movers | 4 | 44 | 48 |
| EV-097 grade changes | 0 | 0 | 0 |
| EV-096 grade crossers | 2 | 2 | 4 (all upward) |
| Frozen-corpus grade changes | 0 | N/A | 0 |
| Invariant breaches | 0 | 0 | 0 |

### INVARIANT CHECK
- No product enters A or S grade in any of the 3 categories under flag-ON.
- No frozen-corpus products are in scope (cakes, cookies, salty_snacks are all non-frozen).
- salty_snacks: the "no snack bar reaches A" invariant applies to the `snack_bars` frozen corpus (separate). salty_snacks itself has no frozen invariant — the A-grade band is unchanged (7/7 same products).
- **0 invariant breaches.**

### KEY FINDING: EV-097 main blast radius confirmed benign
The unmeasured "main blast radius" concern is now closed. 55 non-registered PHVO-generic products
(41 cakes + 14 cookies) all produce 0 grade changes under ceiling 40→55. The ceiling lift primarily
benefits products with low sat-fat (giving a few points of relief), but in this corpus the
fat_quality dimension was already driving E/D grades via sat-fat penalties that hold below 40.

### Score stdev stability (invariant: flag should not inflate category stdev)
- cakes: stdev OFF=10.59 → ON=10.67 (+0.08, negligible)
- cookies: stdev OFF=12.68 → ON=12.69 (+0.01, negligible)
- salty: stdev OFF=16.74 → ON=16.79 (+0.05, negligible)

### Engine SHAs (at time of measurement)
- score_engine.py: 8e4c7db688e4d66d5908c57f94a8fab1257f6660cb1da18c8f62f7c2a5c3f8ed
- signal_extractor.py: 5b0f46b823ef6e2edeedaf987233afc7990d88b05d2cd30e522db25816044f5f

## Artifacts
- `tasks/TASK-284D-artifacts/blast_radius_284d.json` — full per-product diff (sha256=49f3c3b53c6a46dbad9126a8fa9a8a7e1e7fc63f0bf97ecd1e70bfbafdbb5971)
- `tasks/TASK-284D-artifacts/verification_table_284d.csv` — grade-changer table (sha256=239813550213905ddf364a0ce599796d3e604a54a7b84241130db4647b7eeede)
- `tasks/_temp_measure_284d.py` — measurement script (reproducible)
