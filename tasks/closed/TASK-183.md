---
id: TASK-183
title: BSIP0 product origination — evaluate & improve acquisition quality for next runs
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-05
closed_at: 2026-06-05
depends_on: []
blocks: [TASK-184]
category_id: null
cc_close_note: >
  Close-readiness gate PASS (orchestrator-verified against artifacts 2026-06-05). Deliverable
  exists: 03_operations/factory/bsip0_origination_improvement_v1.md (17.8KB). Memo ranks origination
  upgrades (top: BSIP0 contaminant+energy pre-scan; category-code anchoring on A2502/A2803/A2808;
  leaderboard-integrity assert) and handed an apply-ready pre-scan spec to TASK-184 (shared
  bsip0_prescan.py; 3 signal layers; EV-029 שמרים word-boundary carried in). Evaluation only — no
  scores/engine/scraper touched. TASK-184 confirmed the structural finding (category codes absent on
  the price-feed path → pre-scan is the only door-gate there). No owner tripwire.
summary: >
  Evaluate how to improve BSIP0 origination so corpora arrive clean (the TASK-140 cereals batch shipped ~28% non-cereals). Recommend concrete upgrades: category-code anchoring over name-substring queries, ingredient-aware acquisition, an OOS/contaminant pre-scan at the BSIP0 gate, energy-plausibility checks, dedup, and multi-retailer sourcing. Output a ranked improvement plan adopted by the category factory.
---

# TASK-183 — BSIP0 product origination — evaluate & improve acquisition quality for next runs

## Why
The TASK-140 cereals batch (run_004, live) shipped **~26 of 92 displayable products (≈28%) as
non-cereals or bad data** — ptitim pasta (one at #1/A), bread, flour, chocolate confections, an oat
drink, and per-serving parse errors. Root cause traced to **origination**: BSIP0 acquired by Hebrew
name-substring queries (`פתיתי`, `פצפוצי`, `שיבולת שועל`) with no food-class/ingredient gate, so
adjacent products (pasta, candy, drinks, baking flour) were pulled in and only partially caught
downstream. EV-045/045b hardened the BSIP1 *curation* filter — this task addresses the *acquisition*
stage so the wrong products don't enter in the first place.

## Scope (evaluation + ranked plan — not a code rewrite)
Evaluate and rank concrete origination upgrades, each with effort/impact and a proposed owner:
1. **Category-code anchoring** — acquire from the retailer's cereal *shelf/category code* (e.g.
   Shufersal A2211) as the primary spine, with name queries only as supplements; reject products whose
   category code is off-shelf (the organic ptitim carried an F03 code).
2. **Ingredient-aware acquisition / early food-class tag** — pull the ingredient panel at acquisition
   and run the EV-045b classifier (name-head + first-ingredient dominance + energy floor) at the BSIP0
   gate, not only at BSIP1 curation.
3. **OOS / contaminant pre-scan at the BSIP0 gate** (the Stage-5 automation candidate already noted in
   `category_factory_v1.md`) — surface suspected non-category products with reasons before scoring.
4. **Energy-plausibility & unit-sanity check** — flag per-serving/per-100g parse ambiguity (the
   110–139 kcal "dry cereals") at acquisition.
5. **De-dup & brand-line awareness** — collapse the same product across retailers; flag known
   pasta/bakery brand lines (Osem/Intaria ptitim, etc.).
6. **Multi-retailer sourcing** feasibility (feeds TASK-184).

## Definition of Done
- A ranked improvement memo (impact × effort) under `03_operations/factory/` or `02_products/` with a
  recommended adoption set, wired into `category_factory_v1.md` Stage 3–5 and the BSIP0 gate.
- At least the contaminant/energy pre-scan specified concretely enough for TASK-184 to apply.
- Proposes RETURNED with the memo attached. Central Controller / CC records CLOSED.

**Assigned:** data-agent. **Related:** TASK-140 (origin), `corpus_purity_gates_v1.md`. **Blocks:** TASK-184.
