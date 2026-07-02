(route: C3)

# P400 — Stress-test the owner's "estimate composition, anchor on measured values" thesis

You are C3, the independent challenge lane. Evidence-based red-team only; NO code, NO data production. Default to skepticism — Bari acts on your honest pushback.

## Context
Bari scores packaged foods. The owner ordered "drift away from NOVA." NOVA was BLIND: it saw a long ingredient list and punished the product for *having many ingredients*, without knowing what's actually inside. A genuinely decent product full of benign ingredients got punished. Closing THAT gap is the whole project.

We hit a wall: ~36% of Israeli labels print real ingredient percentages; ~45% print only ingredient ORDER (heaviest-first by law) with no sub-percentages; ~3% are unreadable. I told the owner we can't put a number on the unstated ingredients without fabricating, and fabrication is a hard no-go.

## The owner's counter-thesis (what you must challenge)
He argues my "fabrication" framing is wrong, and proposes:
- **T1.** If full ingredient %s exist → measure composition directly.
- **T2.** If they don't → *estimate* composition two ways: (a) against comparable products in-category, and (b) inferred from the NUTRITIONAL VALUES we always have (sugar, fat, sodium → "grosso modo" what the composition must be). Train this estimator on a large sample of fully-labeled AMERICAN products where the % granularity IS published.
- **T3.** Weight the score so the *measured nutritional values dominate* and composition is a MINORITY input — so even if the composition estimate is wrong, it can't swing the grade much. This (he argues) makes T2 not-fabrication: a bounded, low-weight estimate from real data, not an invented fact presented as truth.

## Challenge these, hard
1. **Circularity (the killer):** If composition is estimated FROM macros, and macros already dominate the score (T3), does the composition signal add ANY independent discriminating power — or does it just echo the macros, losing the exact whole-vs-refined signal NOVA-replacement was meant to capture? A whole-grain and a refined-flour product can have near-identical macros. Can a macro-derived estimate EVER separate them? If not, what is T2 actually buying?
2. **Is "low-weight estimate from real data" genuinely not fabrication**, or is it fabrication with a smaller coefficient? Where is the honest line between "modeling from a real prior" and "presenting a guess as fact"? Does T3's low weight actually make it defensible to a skeptical consumer?
3. **American→Israeli transfer:** does a macro→composition mapping trained on US products transfer to Israeli reformulations, or is that an unstated leap?
4. **"We ALWAYS have nutritional values" — is that assumption safe?** What breaks if it's only ~90% true?
5. **The better fallback, if you'd reject T2:** is the honest answer instead "score on measured values + a COARSE confidence-tiered composition read (real-% / order-only / none), never an inferred number"? Compare that against the owner's estimate-and-downweight approach. Which is more defensible AND more useful?
6. **Bottom line:** Is the owner's two-part thesis sound enough to prototype, or does the circularity make it a dead end? What is the SINGLE decisive experiment that would settle it (we can run it on the ~36% of products where we already have ground-truth %s)?

Return a blunt verdict per question + the single biggest risk + whether you'd authorize prototyping the thesis. No fabricated specifics.
