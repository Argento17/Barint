---
id: TASK-504A
title: GLP-1 / suppressed-appetite dairy guide (מדריך pilot)
owner: frontend-agent
status: BLOCKED
blocker: >
  Owner strategic call required (trips tripwire 2 medication-framing + tripwire 3 new-corpus program).
  Adversarial QA pre-check FAILED the claim base (3 CRITICALs, structural): the protein-per-kcal bar is a
  low-calorie filter not a protein signal (A-grade whole/goat milk lose to a D-grade sweetened soy drink on
  identical protein); the GLP-1/medication frame over-claims authority the milk-drink shelf can't carry — the
  actual high-protein dairy (skyr/cottage/quark/Greek yogurt) is NOT in any Bari corpus. Honest version needs a
  new high-protein-dairy corpus build. Orchestrator recommendation: SHELVE + bank the assessment; do not ship the
  milk-shelf compromise. Awaiting owner: shelve vs. commission the high-protein-dairy corpus.
priority: HIGH
created_at: 2026-07-05
depends_on: []
blocks: []
category_id: null
summary: >
  One /madrichim guide reusing LIVE milk_and_alternatives scores through a protein-density + nutrient-density-per-calorie lens for suppressed-appetite eating. NO 'GLP-1 friendly' badge, NO drug named as product qualifier, NO scoring change. Two-gate + elevated Adversarial QA (medication-adjacency). Owner GO 2026-07-05.
---

# TASK-504A — GLP-1 / suppressed-appetite dairy guide (מדריך pilot)

## Origin
Owner category-opportunity scan 2026-07-05: GLP-1 "friendly" food labels (US Conagra/Nestlé, UK high-protein
dairy) + Israel 2026 basket funding Wegovy for teens 12–18. Research + Product parallel assessment → owner
approved the **guide angle (not a badge)**. Pilot = one /madrichim guide reusing the LIVE `milk_and_alternatives`
scores through a protein-density lens for suppressed-appetite eating.

## What happened (gate trail — all pre-build, nothing shipped)
1. **Nutrition gate 1:** dropped the gameable `satiety_support` proxy; set 3 honest bars from raw fields
   (protein_g÷energy_kcal, added_sugar_sources_count, sodium). Spine tier-gated (protein/lean-mass STRONG;
   fiber/nausea/hydration OMITTED for the teen medication-adjacent audience).
2. **Data:** assembled 18-product live-shelf dataset `02_products/milk_and_alternatives/guides/
   task504a_dairy_satiety_shortlist_v1.json` (sha 8fc488e1…, per-100ml, scores byte-checked). No rescore/scrape/OFF.
3. **Product scope ruling:** caught an orchestrator premise error (5/18 clear ≥6 g/100kcal, not "~nothing");
   ruled build on the 5-tier, rename "dairy" → "milk & plant-milk protein density" (3 of 5 winners are soy).
4. **Nutrition gate 2:** mix dairy+soy OK but MUST carry a protein-quality/leucine caveat (dairy leucine-richer).
5. **Adversarial QA pre-check → FAIL as claim base (structural, 3 CRITICALs):** RT-1 protein-per-kcal bar is a
   low-calorie filter (A-grade whole/goat milk lose to a D-grade sweetened soy on identical protein); RT-2 GLP-1/
   medication frame over-claims authority the milk shelf can't carry (real high-protein dairy not scored) — owner
   tripwire; RT-3 orchestrator label errors (Alpro barista not "unsweetened"; יטבתה not "protein-fortified").

## Blocked → owner decision
Milk-shelf GLP-1 guide cannot ship honestly. Fork: **(a) shelve + bank the assessment** (orchestrator rec —
signal persists; don't ship the compromise), or **(b) commission a high-protein-dairy corpus** (skyr/cottage/
quark/Greek yogurt) and build the guide on the food the trend is actually about. Content never dispatched.

Spin-off: **TASK-513** (literature.py wrong-DOI citation-integrity bug) — surfaced by the assessment's Research lane.
