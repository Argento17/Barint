# P67 — Cookies-near-coffee: corpus filter (narrow the broad scrape) (route: C1 / Data)

**Task:** TASK-275 (factory run #7, `cookies-coffee`). **Lane:** C1 native Data Agent — Bari-judgment
(scope classification of a real Hebrew shelf + the missing-data discard rule).

## Objective
Narrow the broad 129-product BSIP0 scrape into the honest **coffee-biscuit corpus**, by applying the
Nutrition methodology's scope rules + the owner discard rule. This is Stage 2 ("diminish after BSIP0").

## Inputs (read first)
1. Methodology (authoritative scope law): `02_products/cookies_coffee/methodology/cookies_coffee_scoring_interpretation_v1.md`
   — apply §1.3 in/out rule, §1.4 ambiguous rulings, §1.2 in-scope table exactly.
2. Raw scrape: `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json` (129 products).
3. Structural TEMPLATE to mirror (buckets + per-product reason): `02_products/brined_cheeses/factory_run_001/corpus_filter.json`.

## Deliverable
`02_products/cookies_coffee/factory_run_001/corpus_filter.json` — three buckets, **a reason string per
product**, mirroring the brined template's shape:
- **IN_SCORED** — dry/crisp sweet biscuit, no integrated filling, not choc/compound-coated as primary
  architecture, coffee-occasion plausible, AND has BOTH core nutrition (energy+protein/macros) AND an
  ingredient list. These get scored.
- **TRANSPARENCY_NULL** — in-scope biscuit but missing nutrition OR ingredients (the 24 missing-nutrition
  + any missing-ingredients). Per `missing_data_discard_rule`: one-shot only, else DISCARD — do NOT
  re-scrape, do NOT score-punish.
- **OUT_OF_SCOPE** — fails the structural/occasion test: spreads (ממרח עוגיות/Lotus spread), cream-filled
  & sandwich cookies (סנדוויץ), maamoul/date-filled (מעמול), wafers, chocolate-COATED biscuits, soft/
  cake-like, children's character cookies, protein/functional, rice cakes, energy bars.

## Hard rulings to apply (from §1.3/§1.4 + the C3/orchestrator watch-item)
- **Chocolate-chip / minor flavoring:** IN if the primary architecture is a crisp biscuit body AND
  choc/cream content is not the dominant structure (>30% by volume or full outer coating → OUT). Where a
  choc-chip product is positioned as a standalone "treat cookie" rather than a coffee biscuit, lean OUT.
  State your call + reason per such product.
- **Maamoul / filled (מעמול, ממולא):** OUT (integrated filling).
- **Sandwich / cream (סנדוויץ, קרם as filling):** OUT.
- **Gluten-free:** IN by default if occasion matches; OUT only if clinical/medical positioning. **Vegan/
  organic:** IN (fat source is a scoring signal, not a scope filter).
- **Implausible nutrition:** 2 products show sodium ~6000mg/100g (parse error). Verify against the raw
  HTML/label; if genuinely a parse artifact → TRANSPARENCY_NULL (don't score on bad data), note it.
- **Digestive / whole-grain:** IN (quality differentiator, not exclusion).

## Guards
- **OFF ban absolute** — corpus uses only the direct scrape; `off_used` must be 0 in your summary.
- Do not invent products, rename, or alter nutrition/ingredients. Classification only.
- Scorability rule (brined lesson): an IN_SCORED product MUST have fat AND protein AND energy present
  (the engine requires them) — if a core macro is null, it is TRANSPARENCY_NULL, not IN_SCORED.
- Sum of the three buckets MUST equal 129.

## Return format
Report: bucket counts (sum=129), the IN_SCORED count (must be ≥25 to proceed; report the number even if
lower), a short list of every borderline/ambiguous call with your reason, the 2 implausible-sodium
dispositions, and off_used=0. Domain agent: propose RETURNED, never CLOSED. End with the machine-readable
return contract (`01_framework/operations/return_contract_v1.md`): task=P67, artifact (corpus_filter.json
+ sha256), counts, commands_run, not_done, self_check.
