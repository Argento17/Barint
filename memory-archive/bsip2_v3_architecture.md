---
name: bsip2-v3-architecture
description: "BSIP2 v3 architecture design — universal core + archetype interpretation system. Location, philosophy, migration phases, and routing decisions."
metadata: 
  node_type: memory
  type: project
  originSessionId: e98ff19c-3c0d-4e26-8e96-38583f14e9c8
---

BSIP2 v3 architecture documents were created at:
`C:\Bari\01_framework\bsip2_framework\v3_architecture\`

Seven documents: architecture_overview.md, proposed_folder_structure.md, archetype_philosophy.md, router_design.md, shared_vs_local_dimensions.md, migration_strategy.md, future_archetype_candidates.md.

**Core philosophy:** BSIP0 and BSIP1 are universal. BSIP2 diverges at the archetype level. One shared scoring engine; different interpretation contexts (calorie density tables, guardrail modules, floors) injected per archetype.

**Why:** cereals run exposed routing as the primary failure mode. 6/8 granola products misrouted because whole_food_fat nut/seed signals (0.95 weight) dominated granola signals (0.9). Solution: hard anchors ("גרנולה" → snack_bar_granola unconditionally) + context-gated signals (nut/seed signals only fire when name also has whole-food-fat context).

**Migration phases (5 phases, zero breakage):**
- Phase 0 (NOW): Apply 5 targeted bug fixes to proto_v0 (granola anchor, fiber laundering cap, whole-grain NOVA discount, matrix disruption floor gate, threshold smoothing)
- Phase 1: Extract ontology (marker dictionaries) to ontology/ — import shims only
- Phase 2: Upgrade router (category_classifier.py → router/bsip2_router/) with 3-stage resolution
- Phase 3: Extract core (score_engine.py → core/scoring_engine/) — relocation only
- Phase 4: Create archetype shells (archetypes/*/) and inject context into guardrails
- Phase 5: Unify 6 batch_run_*.py scripts into one generic runner

**Next category after architecture stabilizes:** yogurt_system — BSIP0 ready, routing anchor clear ("יוגורט"), fermentation_quality is the one new dimension needed.

**Do NOT add:** supplement_system — requires an entirely different framework. frozen_meal_system — composite ingredient parsing is a v4+ problem.

**Why:** To prevent "bsip2_cereal.py / bsip2_nuts.py" fragmentation as categories multiply.
