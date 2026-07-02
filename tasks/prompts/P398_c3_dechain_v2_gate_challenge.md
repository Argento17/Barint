(route: C3)

# P398 — Independent challenge: did the NOVA-replacement signal really just hit a "bug," or is the approach weaker than claimed?

You are C3 — the independent challenge lane (ChatGPT/OpenAI). Evidence-based red-team only. Do NOT produce data or write code; challenge the reasoning. Bari acts on your honest skepticism, so default to refuting weak claims.

## Background
Bari scores packaged foods. The owner ordered "drift away from NOVA" — instead of a crude 1–4 ultra-processing class, judge a product by READING its actual Hebrew ingredient list and deciding: is it whole-food-led or refined-led? The make-or-break sub-signal ("whole-food matrix") must classify a product from its ingredient text, weighting ingredients by (a) their stated percentage if printed, else (b) their position (Israeli labels list heaviest-first), with a first-ingredient anchor.

## The gate it must pass (set by Product, governance-co-signed)
A 58-product hand-built Hebrew "gold set" (answer key), graded by a dual gate:
- **B1 anchor calibration:** clearly-whole products score ≥60, clearly-refined ≤45 — ≥90% must pass.
- **B2 ordinal ranking:** for ranked pairs, the more-whole product must score higher — ≥95% (must include ≥10 hard-mixed pairs).
- **B3 coverage:** ≥95% of parseable labels fire ≥1 marker.

## The result just in (v2 implementation)
- **B1 = 70%** — and the split is the interesting part: clearly-REFINED products 13/13 PERFECT, but clearly-WHOLE products only **8/17**.
- **B2 = 27.3%** (3/11 pairs correct).
- **B3 = 92.7%.**
- stated-percentage extraction worked on only **25.5%** of labels — so the formula leans mostly on position inference.

## The builder's diagnosis (the claim to challenge)
The Data lane (which also built the formula AND assembled the answer key AND ran the grading) says: *"This is a one-function implementation bug, not a design flaw. The composite-expansion logic over-fires — it treats a single ingredient with its own stated percentage, e.g. 'פתיתי שיבולת שועל מלאה (54%)' (whole-oat-flakes 54%), as if the parenthetical were a sub-recipe, and zeroes the ingredient's weight. Fix one function (only treat a parenthetical as a sub-list if it contains commas), re-run, and the gates will pass. The §2.5 design is sound."*

## Challenge these, hard
1. **Is "just a bug, design is sound" credible** given the asymmetry — refined detection is flawless (13/13) but whole detection collapses (8/17)? Does a single composite-parsing bug plausibly explain a one-sided failure, or does it hint the whole-food side of the design is inherently harder/weaker? What would you need to see to believe the one-bug story?
2. **Methodology independence:** one lane built the formula, built the answer key, and graded it. What specific failures does that conflict invite, and what independent safeguard is mandatory before any "it passes" is trusted?
3. **Position-inference fragility:** with stated-% extraction at only 25.5%, the signal mostly infers dominance from ingredient ORDER. Is order-weighting alone strong enough to reliably separate whole-led from refined-led Hebrew products, or is this structurally fragile (e.g. a granola whose first ingredient is oats but is 40% sugar+oil by the rest of the list)?
4. **Is the dual-gate metric honest** — does excluding "genuinely mixed" products from the binary check and leaning on ranking truly test the hard cases, or is it a softened bar that lets the signal look better than it is?
5. **Bottom line:** is "drift away from NOVA by reading ingredients" achievable to a *trustworthy* standard on Hebrew retail labels, or is the difficulty (composite parsing, sparse percentages, qualifier words like כוסמין לבן vs כוסמין מלא) being underestimated? If you think it's achievable, what's the minimum bar of evidence; if not, what's the honest fallback (e.g. NOVA stays a stronger input than "±5-10 nudge")?

Return: a blunt verdict per question + the single biggest risk you see, and whether you'd authorize a fix-and-rerun or demand a deeper rethink. Cite your reasoning; no fabricated specifics.
