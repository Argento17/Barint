# Real Israeli Supplement Corpus — MVP run v2 (measured)

**Task:** TASK-171J · **Date:** 2026-06-03 · **Status:** candidate / EDPG — nothing ships, no published score.
*(Report assembled by orchestrator from `_corpus_run_v2.json`; the build agent hit a session limit before writing it. The corpus run itself completed over all 118 attempted SKUs.)*

## The measured headline — the MVP under-delivered vs projection

| Metric | Projected (TASK-171I) | **Measured (this run)** |
|---|---|---|
| Scoreable yield of addressable shelf | ~31–37% net (MVP subset) | **6.8% (8 of 118 addressable SKUs)** |
| Unscoreable | — | **110 (no trustworthy panel)** |
| Panel sources that delivered | 3rd-party e-tailers + Altman | altman 4 · biogaya 2 · vitamins4all 2 |
| Grade distribution | — | **S: 3 · E: 5** |

**The projected ~75–85% addressable coverage did NOT materialize at scale.** The feasibility probe's number was measured on a handful of hand-picked products that happened to be on the e-tailers; run against the *real* addressable shelf, the resolver found a barcode-matchable, dose-complete, trustworthy panel for only **8 of 118**. 110 SKUs returned "no barcode hit on any source; no brand+active+dose match." The local-brand panel sources (Altman site + biogaya/vitamins4all e-tailers) simply do not carry most local-brand SKUs in a resolvable form.

**Caveat (honest):** this is the *first* measured MVP run, built fast and cut short by a session limit before any tuning. 6.8% is likely a **floor** — more e-tailer sources, looser (still-verified) matching, and the Hebrew claim-vocab fix below would lift it. But it is far below the ~31–37% projection, and that gap is the decision-relevant fact.

## The real Israeli shelf through Bari's engine (the 8 scored — all candidate)

- **Altman Vitamin D-1000 (×2) → S / 91.2** — the clean win: Strong evidence (status correction), in-range dose, D3 (cholecalciferol), honest label. This is what a *good* supplement looks like through the engine, on a real Israeli product.
- **Altman Magnesium "Balance" (450 mg oxide) → E / 20** — "heart health" resolved to BP=Moderate, good honesty, **but the 450 mg dose triggers the Safety veto (>350 mg toxicity UL)** → E. The standing safety meta-rule firing on a real over-dosed product.
- **Altman Biotin 1000 mcg → E / 34** — "hair & nails" resolved to the cosmetic-in-replete-adults endpoint = Insufficient → cap-1 ceiling → E. The biotin-cosmetic case, on a real SKU.
- **TINC Magnesium Malate → E / 34** — claim "עייפות/fatigue" **did not map** to the magnesium umbrella → Insufficient. ⚠️ *calibration gap, see below.*
- **SupHerb Magnesium Bisglycinate → E / 34** — claim "ספיגה משופרת / improved absorption" did not map → Insufficient. *(Arguably correct — "better absorption" is not a health-benefit claim — but worth a Nutrition ruling.)*

## Two decision-grade findings the measurement surfaced

1. **Acquisition yield is the binding constraint, and it's worse than projected (~7% measured).** Reaching a launch-credible corpus needs either (a) materially more panel sources + a more thorough resolver, or (b) acceptance that the local-brand shelf is largely unreachable by scraping — which points back to a manufacturer-feed (BD) path. **The "build the acquisition" case is materially weakened by this measurement.**

2. **The claim-resolution umbrella vocab is incomplete for real Hebrew labels (calibration gap, fixable).** Real products scored E because their actual on-label Hebrew claims ("עייפות/fatigue", "ספיגה/absorption") aren't in the dossier umbrella maps — even though **magnesium-for-fatigue is an EFSA-authorized claim** with real evidence. The umbrella maps were built against English/expected claims, not the actual Hebrew structure/function phrases on the Israeli shelf. This depresses grades unfairly and is a **Nutrition D6 calibration task** (expand each dossier's `structure_function_umbrella` to the real Hebrew claim vocab).

## Bottom line
The MVP did its job as a **measurement instrument**: the engine scores real Israeli products correctly (clean D3→S, oxide-overdose→veto, biotin-cosmetic→E), but **the acquisition yields ~7% as-measured, not the projected ~31–37%**, and the claim vocab needs Hebrew-real-label expansion. This is a re-decision point, not a launch — the acquisition path needs another iteration (more sources + claim-vocab fix) before a real ~half-shelf corpus is credible, or the category's reachability has to be reassessed.

## Artifacts
- `_corpus_run_v2.json` — full per-SKU results (118 attempted, 8 scored, traces)
- `skus/*.json` — scored SKU records · `cache/*.json` — fetched panels
- Adapters: `integrations/clients/il_supplement_panels.py` (3rd-party e-tailer + brand-site) · `il_panel_resolver.py` (source-priority resolver)
