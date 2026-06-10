---
id: TASK-153
title: "Cheese corpus: remove misclassified seasoning blend (תערובת תיבול פילדלפיה, 7290014217492) + add router seasoning-exclusion to the פילדלפיה anchor"
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-02
completed_at: 2026-06-02
closed_at: 2026-06-02
closed_by: cc-agent
close_reason: "CC close-gate PASSED — verified against artifacts: (1) cheese_frontend_v1.json now 51 products (_meta.product_count=51), seasoning SKU che-7290014217492 absent, grades B20/C24/D6/E1 (removed 60/C dropped C 25→24); (2) router_v2.py:172 ANCHOR_EXCLUSIONS['פילדלפיה']=['תערובת תיבול'] mirrors the נפוליאון exclusion; (3) regression negative case exclusion_philadelphia_seasoning at router_regression_corpus.json:369 (→default, must_not_be dairy_protein), 16/16 PASS, deterministic, frozen categories unmoved; (4) EV-030 registered with label-observability + activation scope (cheese only) + full rollback; (5) build green (tsc EXIT 0, validate-corpus 0 cheese errors, next build EXIT 0, /hashvaot/cheese prerendered with 51). Routing/curation only — engine unmodified, no published/frozen score changed, no other product moved (subtractive). category_config + factory_run_003 counts reconciled (51 display / 8 withheld / 59 total). NOTE: historical run_cheese_003 traces + bsip1 output still contain the SKU (immutable run records) — annotation deferred, non-blocking."
depends_on: [TASK-142, TASK-145]
blocks: []
parent: TASK-142
category_id: cheese
roadmap_impact: true
cc_reviewed: 2026-06-02
cc_comments:
  - date: 2026-06-02
    flag: blocker
    text: "LIVE-PAGE DEFECT: a non-cheese (salt-based spice blend, brand טעם וריח, from Shufersal's תבלינים/seasonings shelf, ingredients = spices/salt/dextrose/onion-powder/E551) is displayed at 60/C in the cheese comparison. Pulled in by the TASK-145 פילדלפיה→cream_cheese router anchor (which excluded נפוליאון cake but not תערובת תיבול). Its real 7,905 mg/100g sodium is plausible for a seasoning but distorts the cheese category. Surfaced by the TASK-152 Content review (the '7,905 מ\"ג' insight line)."
  - date: 2026-06-02
    flag: verify
    text: "Sweep done: this is the ONLY non-cheese in the 52 (sole sodium>1500 outlier; other 4 'תיבול' hits are real herbed cheeses at 349-480 mg). Removal is subtractive: 52→51 displayed, no other product's score changes. Confirm no superlative insight line (best/worst/highest-fat) referenced the removed SKU before shipping."
summary: >
  The TASK-152 Content review surfaced that `cheese_frontend_v1.json` includes `תערובת תיבול פילדלפיה`
  (gtin 7290014217492) — a salt-based SEASONING blend (brand טעם וריח; Shufersal shelf
  מוצרי יסוד ותבלינים/תבלינים; ingredients: תבלינים ושמני תבלין, מלח, דקסטרוזה, אבקת בצל, E551), NOT a cheese.
  It was routed into cheese_spreads because the TASK-145/EV-025 פילדלפיה cream-cheese hard anchor caught it
  (the נפוליאון cake exclusion did not cover seasoning blends). Its 7,905 mg/100g sodium is real for a seasoning
  but it is miscategorised and on the LIVE /hashvaot/cheese page at 60/C. Fix: (1) remove it from the cheese
  corpus / live frontend (52→51 display-approved); (2) add a 'תערובת תיבול' / seasoning exclusion to the
  פילדלפיה anchor in router_v2.py + regression-lock (mirrors the נפוליאון cake exclusion, EV-025). Routing/curation
  only — NO scoring weight/threshold/penalty change; no other product's score changes.
---

# TASK-153 — Remove misclassified seasoning blend from cheese + router exclusion

Spun off TASK-142/TASK-152. Curation + routing-identity fix; governed under bari-bsip2-scoring-governance
(evidence + label-observable + rollback). NO scoring rule change.

## The defect (confirmed)
- `cheese_frontend_v1.json` product `che-7290014217492` = `תערובת תיבול פילדלפיה`, brand **טעם וריח**.
- BSIP0 raw `subcategory_raw: "cheese_spread"`, `source_url` = Shufersal `…/מוצרי יסוד ותבלינים/תבלינים/…`
  (basics & **seasonings**), `ingredients_raw: "תבלינים ושמני תבלין,מלח,דקסטרוזה,...אבקת בצל,...E551..."`.
- Sodium 7,905 mg/100g (real for a salt seasoning; ~16× the next-highest cheese). Displayed 60/C — wrong category.
- Root cause: TASK-145 `פילדלפיה → dairy_protein/cream_cheese` hard anchor with no seasoning exclusion.

## Scope
1. Remove `7290014217492` from the cheese corpus and `bari-web/src/data/comparisons/cheese_frontend_v1.json`
   (52 → 51 display-approved); update `_meta.product_count` and `02_products/cheese_spreads/category_config.json`
   baseline displayable count. Confirm no superlative insight line referenced it.
2. Add a seasoning exclusion to the `פילדלפיה` anchor in `router_v2.py` (e.g. exclude `תערובת תיבול`/`תיבול`
   blends with seasoning-brand / spice-ingredient signals), mirroring the `נפוליאון` cake exclusion; regression-lock
   (router corpus + this entry; frozen categories unmoved; determinism verified).
3. Re-verify: misroute still <5%, displayable count, build green if frontend JSON changes.

## Guards + DoD
- Routing/curation only — engine unmodified; no published/frozen score changed; no other product's score moves.
- DoD: SKU removed from live JSON + corpus (51 displayed); router seasoning-exclusion added + regression-locked;
  determinism verified; `tsc`/build green. Then propose RETURNED with file:line + count evidence.
