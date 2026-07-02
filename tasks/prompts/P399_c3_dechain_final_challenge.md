(route: C3)

# P399 — Final challenge: is the NOVA-replacement signal's pass REAL, or false confidence?

You are C3, the independent challenge lane. Evidence-based red-team only; no code, no data production. You challenged this work earlier (P398) and were rightly skeptical. The team has since rebuilt it. Judge whether your earlier concerns are now genuinely met or whether we're fooling ourselves.

## What changed since your P398 challenge
The earlier failure was traced to a READING-layer problem, not the scoring formula. The team:
1. Built a single shared Hebrew ingredient reader (replacing ad-hoc per-consumer regex). Stated-percentage extraction went from 25.5% (which turned out to be a parsing-bug artifact) to ~80% of labels — i.e. the data was always on the label, we were discarding it.
2. Fixed two reading bugs that independent QA caught the builder mis-attributing as "formula gaps" (pct-after-closing-paren; parent-composite marker override).
3. Refined the scoring formula (tighter mixed-band sensitivity; nuts/seeds at half-weight vs grain, now with a trace-grain guard so a 1% grain can't trigger it; sourdough starter removed as a non-food process agent).

## The current result (v5.1) on an EXPANDED, INDEPENDENTLY-FROZEN, NEUTRAL test set
- Test set expanded from 12 to **20 hard ranking pairs** by the independent QA lane; the formula author was BLIND to the 8 new pairs; frozen BEFORE v5 scoring.
- Gates: **B1 (calibration) 96.8%, B2 (ranking) 100% (with one co-signed test-pair correction; 95% without it), B3 (coverage) 100%.** All three pass.
- Independence: a lane separate from the builder graded it, and caught the builder over-claiming "zero reading bugs" TWICE before confirming on v5.1.
- One test pair (RP-04) had its expected answer corrected — independently ruled by Product as pure arithmetic (28g vs 39g of oats per 100g, readable off the label), and flagged as a broken answer BEFORE this fix existed.

## Challenge — be blunt, default to skepticism
1. **Your P398 "position-inference fragility" concern:** with stated-% now read on ~80% of labels (not 25.5%), is that concern resolved, or does the ~20% still relying on position inference remain a real risk?
2. **Your "frozen-before-scoring / metric-shopping" concern:** does expanding to 20 pairs, frozen before scoring, with the author blind to 8, adequately prove generalization — or is 20 still too few / the 8 new pairs possibly too easy?
3. **The RP-04 test-answer correction:** legitimate (test catching up to the reading fix), or still metric-shopping dressed up? Would you accept it?
4. **Independence:** is "a separate lane grades + caught the builder over-claiming twice" sufficient, or is there a residual conflict (e.g. the test-owner lane is the same as the grader lane)?
5. **The honest residue:** B2 still has 1 knife-edge pair (~0.5pt margin); one product (481180) exposed a separate pre-existing dedup bug; one calibration product (a nested-label cookie) is still unsolved (within the passing rate). Do these undermine the "it passes" claim, or are they acceptable tracked follow-ups?
6. **Bottom line:** is this now a REAL, generalizable component-level result that justifies moving the ingredient-reading signal from "experimental secondary" toward becoming the NOVA-replacement driver (subordinating NOVA) — pending the still-required whole-corpus shadow run + owner deploy gate? Or do you still counsel keeping NOVA as a meaningful (not ±5-10) input, and what's the remaining evidence gap?

Return a blunt verdict per question + the single biggest remaining risk + whether you'd authorize proceeding to the whole-corpus shadow stage. No fabricated specifics.
