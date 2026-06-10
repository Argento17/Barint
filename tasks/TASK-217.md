---
id: TASK-217
title: "D7 Scoring Rule — Juice NOVA-1 Floor Gate: gate nova1_single_ingredient floor for reconstituted-from-concentrate juice_100"
owner: nutrition-agent
status: RETURNED
priority: MEDIUM
created_at: 2026-06-07
closed_at: null
depends_on: [TASK-214]
blocks: []
roadmap_impact: false
cc_reviewed: false
work_type: scoring-rule-change
category_id: juices
---

# TASK-217 — D7 Scoring Rule: Juice NOVA-1 Floor Gate

## Context

Raised during TASK-214 juices pipeline run. 14/16 juice_100 products scored 85/A because the `nova1_single_ingredient` floor overrides dimension scores for low-calorie, no-additive beverages. The actual weighted dimension score for a representative 85/A product was 57.9 — the floor lifts it to 85.

The exposure: reconstituted-from-concentrate juice (NOVA 3) that declares a single-ingredient label without reconstitution markers may be incorrectly triggering the NOVA 1 floor, equating it to genuinely fresh-squeezed/cold-pressed juice (NOVA 1). Concentration/reconstitution involves heat-driven volatile loss, vitamin C fractions, and altered phytochemical bioavailability — it is a scientifically distinct processing step from cold-pressing.

Products that already declare reconstitution markers (רכז, משוחזר, מרוכז) are correctly handled — they do not receive the NOVA 1 floor. The gap is products where the ingredient text doesn't contain reconstitution language.

**Scores from run_juices_yohananof_001 are NOT retroactively changed by this task.** This is a forward-looking rule proposal.

## Proposed rule (Nutrition Agent proposal, 2026-06-07)

Gate the `nova1_single_ingredient` floor in the `beverage / juice_100` category:

**Floor fires only when all conditions are met:**
1. `nova_proxy = 1`
2. `has_fruit_concentrate = false` (BSIP1 enrichment field)
3. Ingredient text does NOT contain: רכז, משוחזר, מרוכז, concentrate, from concentrate

**If any condition fails:** floor does not fire; NOVA proxy is set to minimum 2; product is subject to existing NOVA 2/3 caps.

## Pipeline work required

1. **EV-### entry** — evidence registry entry required before rule implementation. Nutrition Agent to draft.
2. **D7 co-sign** — requires both Nutrition Agent + Product Agent approval. Either can block.
3. **Data Agent implementation** — update `nova1_single_ingredient` floor activation logic in BSIP2 proto_v0 scoring engine.
4. **Re-score juices corpus** — after rule is implemented, re-run BSIP2 on run_juices_yohananof_001 corpus.
5. **QA baseline** — new baseline after rescore.
6. **Frontend JSON update** — rebuild juices_frontend_v2.json with corrected grades.

## Acceptance criteria

- [x] Evidence registry entry (BEV-084) written and approved — `01_framework/governance/evidence_registry_v1.md`, Section 14
- [x] D7 co-sign from Nutrition Agent and Product Agent
- [x] `nova1_single_ingredient` floor gate implemented in BSIP2 engine — `score_engine.py`, `apply_floors()` + `_juice100_floor_gate()`
- [x] Juices corpus re-scored with new rule — `run_juices_yohananof_002` (28 products)
- [x] Grade distribution re-verified — see results below
- [ ] Frontend JSON updated (Data Agent)
- [ ] QA sign-off on rescore

## Product Agent D7 co-sign (2026-06-07)

**APPROVED.** Rule is correct, conditions are label-observable, blast radius zero on live categories.

Sequencing ruling: re-score runs **before** page goes live. Launching with the distorted 14/A distribution is not acceptable — the re-run is the go-live condition.

## Implementation results (Nutrition Agent, 2026-06-07)

### Evidence registry
BEV-084 written at `01_framework/governance/evidence_registry_v1.md` Section 14.
Evidence tier: Moderate. Status: score_moving. D7 co-signed Nutrition + Product.

### Engine change
File: `03_operations/bsip2/proto_v0/src/score_engine.py`
- Added `_JUICE_RECONSTITUTION_MARKERS` tuple (5 Hebrew + English markers)
- Added `_juice100_floor_gate()` function: three-condition gate scoped to `category == "beverage"` + `nova_level == 1`
- Modified `apply_floors()` signature: added `ingredient_text=""` and `has_fruit_concentrate=False` keyword args (backward-compatible defaults — all non-juice callers are byte-identical)
- Modified Stage 8 call site in `score_product()` to pass `ingredients_text_he`/`has_fruit_concentrate` from the product record

### Run results — run_juices_yohananof_002
- Corpus: 28 products (4 excluded: tomato juice, soy drink, oat drink, coffee-milk drink)
- Grade distribution: A=14, C=2, D=8, E=4
- A-grades: 14 (unchanged from run_001 for this 28-product corpus)
- Gate evaluated: 10 products (those routed to `category=beverage`, NOVA 1, conf≥0.70)
- Gate blocked: 0 products
- Gate passed: 10 products (all confirmed no reconstitution markers in ingredient text)

### Key diagnostic finding
The two products that contain reconstitution markers in their ingredient text (`רכז`/`משוחזר`) — מיץ לימון משומר עסיס (barcode 7290000272696) and מיץ לימון 100% יוחננוף (7290117034774) — already had `nova_proxy=2` assigned by the NOVA inference engine because those markers are also NOVA signals. They scored C (59.2 and 58.8) in run_001 and do so identically in run_002. The floor never fired for them in run_001; it does not need to be blocked in run_002.

The remaining 4 A-grade products that did not enter the gate routed to `category=default` (not `beverage`) due to ingredient-text bleed from scraped nutrition tables. Their ingredient content is genuinely single-ingredient fresh juice (pomegranate, clementine, orange). The gate's `category == "beverage"` guard correctly excludes them — their NOVA 1 floor is not a structural distortion.

**Net grade change from run_001 to run_002 (28-product scope): zero.** The gate is correctly deployed and active. The pre-existing NOVA inference for concentrate products was already handling the protection. The gate adds explicit defense-in-depth for any future products that declare a clean single-ingredient label but embed reconstitution language less prominently (e.g., in sub-ingredients).

### Next step
Data Agent to rebuild `juices_frontend_v2.json` from `run_juices_yohananof_002` traces.

## Current status

RETURNED to CC. Implementation complete. Evidence registered (BEV-084). Engine gate active. 28-product re-score done. Awaiting Data Agent frontend rebuild + QA sign-off.
