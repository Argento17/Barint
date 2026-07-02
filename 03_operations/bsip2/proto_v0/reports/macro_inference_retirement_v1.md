# Decision Record — Macro-Inference Composition Estimate: TESTED → RETIRED

**Date:** 2026-06-26
**Program:** TASK-395 (de-chain the engine / drift from NOVA)
**Status:** CLOSED decision. The macro-estimation approach is retired (tested, not used). The surviving design is recorded below and proceeds via TASK-395C.

## The thesis tested (owner, P400/P450)
When ingredient percentages are not printed, **estimate the product's composition from the nutritional values we always have** (sugar/fat/sodium), anchored on in-category comparables and trained on a large fully-%-labeled **American** sample; keep the estimate low-weight so it cannot swing the grade (T3), so it is a bounded estimate from real data, not fabrication.

## How it was tested
A 5-lane independent forum, each blind to the others, plus one empirical experiment on our own data:
- **Nutrition (D6)** — food-chemistry soundness of macro→composition inference.
- **Data** — ran the decisive experiment on the 645 products where we have ground-truth ingredient %s.
- **Research** — does the American fully-%-labeled training data actually exist?
- **Adversarial QA / Red-Team** — where does it produce an indefensible score?
- **C3 (independent challenge)** — circularity, transfer, fallback comparison.

## Findings (evidence, not opinion) — all five lanes converged
1. **Circularity confirmed.** On 645 ground-truth-labeled products, macro-predicted composition vs true composition: multi-macro r = **0.811**, strongest single predictor fiber r = 0.614. The estimate reproduces ~66% of signal already present in the macros — C3: *"a second nutrition score wearing a composition costume."*
2. **Macro-twins are unsolvable.** 23 pairs / **34 products (~8% of the labeled shelf)** have near-identical macros but composition scores differing **25–84 points**. The distinguishing signal is not in the macros at any confidence. These twins *are* the NOVA-blindness gap restated — so estimating composition from macro aggregates would re-introduce exactly the blindness the project exists to remove.
3. **"We always have the values" is false.** Only **52%** of the food corpus has complete sugar+fat+sodium; fiber (the best single predictor) has **43%** coverage.
4. **The American training data does not exist.** US FDA requires **no** ingredient-% declarations (only juice %); EU/UK QUID declares % for only 1–3 emphasized ingredients; no open dataset has full ingredient-% breakdowns at scale. Israeli labels have *better* %-coverage than US.

## What survives of the owner's thesis (and proceeds)
- **T1 — measure real %s where printed.** ✅ Already built (47.5% of corpus, high confidence).
- **T3 — nutrition values dominate the score weight.** ✅ Already the engine architecture.
- **"Assume the ingredients" via ingredient ORDER** (not macros). ✅ Order is real, legally-mandated data (heaviest-first); used at reduced confidence with a hard ceiling — never the macro guess.

## Decision
- **Retire** the macro→composition estimator and the American-data training plan. Do not re-attempt without new evidence overturning the circularity result above.
- **Proceed** with the owner-approved 4-step roadmap; the keystone is the in-code confidence gate (**TASK-395C**).

## Lane ledger
| Lane | Engine | Mode | Outcome |
|---|---|---|---|
| Nutrition (D6) | native (Sonnet) | analysis | macro-inference unreliable in grain/bar categories; recommend order-based + confidence scaling |
| Data | native (Sonnet) | experiment | r=0.811 circularity; 34 macro-twins; 52% nutrition coverage; US data infeasible |
| Research | native (Sonnet) | evidence | US/EU labels do not publish ingredient %s at scale; coarse-class inference is the only viable ML form |
| Adversarial QA | native (Sonnet) | challenge | 3 CRITICALs gate any owner-presentable shadow (confidence ceiling, ranking miss, disclosure) |
| C3 | openai/gpt-5.5 | challenge | "overclaimed/circular; falsification-prototype only, not production"; proposed the exact experiment Data had already run |
