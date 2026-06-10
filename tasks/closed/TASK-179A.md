---
id: TASK-179A
title: Engine-enrichment reference frameworks — scoping dossier
owner: research-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-03
completed_at: 2026-06-03
close_reason: >
  Scoping dossier delivered + verified against artifact (research/glass_box/engine_enrichment_frameworks_scoping_v1.md,
  215 lines, all 5 sections). Additive set empirically derived from real BSIP0 panels (not synthetic) — top hits
  E481/E300/E471/E282/E202, load is overwhelmingly functional/likely-neutral (validates "engineered≠bad" with data);
  only a few contested high-stakes ones (carrageenan E407, CMC E466, aspartame, NNS). DIAAS table, nutrient-framework
  registry (with Israeli MoH red-label anchor), and source/API map (authoritative additive+protein sources are
  bulk-curate, not live APIs) all delivered. No engine/score/frontend change. Feeds W1.5/W2/W3.
depends_on: []
blocks: []
category_id: null
roadmap_impact: false
work_type: execution
cc_comments:
  - flag: verify
    text: "Before any consumer Hebrew text ships from the additive table, re-verify E142/E144 colour-code→colour-name mapping against actual panels (self-flagged in dossier §2)."
  - flag: fyi
    text: "Live frontend JSON ingredient strings are curated/sparse — real ingredient panels live in 02_products\\*\\...bsip0_raw*.json. Relevant for D5 detector + any future enrichment wiring."
summary: >
  Research scoping dossier (suggestion-stage, no engine code, no score movement) proposing the
  authoritative interpretive frameworks to enrich each Glass Box engine dimension. Four artifacts:
  (1) protein-source quality reference table (DIAAS/PDCAAS, ~20-30 shelf sources, disclosure-gated);
  (2) additive prototype set (~20-25 most shelf-frequent additives across live categories, each
  evidence-tiered with authoritative source + draft consumer line); (3) nutrient-interpretation
  framework registry (protein/fiber/sugar/sodium/sat-fat/energy/fat-quality/micros — each with the
  quantity→quality→evidence three-layer treatment, thresholds, and the Israeli MoH red-label anchor);
  (4) source/API leverage map (USDA FDC, EFSA OpenFoodTox, JECFA/Codex, FDA, PubChem, OFF, Tzameret,
  il_gov_data, literature/Cochrane — live-API vs bulk-curate, new wiring needed). Feeds W1.5/W2/W3.
---

# TASK-179A — Engine-enrichment reference frameworks (scoping)

**Part of:** TASK-179 (Glass Box). **Stage:** suggestion / scoping. **No engine changes, no score movement.**
Adoption of anything here is a separate Nutrition+Product gated decision.

## Why
The clinician's PDCAAS point was one instance of a general truth: every nutrient needs a
*quantity → quality/form → evidence* treatment anchored to an authoritative framework, and the
quality layer is frequently undisclosed (so it also feeds D5/D6). This dossier maps the frameworks
and sources so the owner can cost out W1.5 (protein signal) and W2 (additive prototype) and decide
what to initiate.

## Deliverable (single markdown dossier)
Path: `research/glass_box/engine_enrichment_frameworks_scoping_v1.md` (header `**Task:** TASK-179A`).

1. **Protein-source quality table** — ~20-30 protein sources common on the Israeli shelf; DIAAS (FAO 2013),
   PDCAAS where DIAAS absent; quality tier; citation; the disclosure-gating note (no per-product DIAAS without
   proportions → signal must be confidence-gated).
2. **Additive prototype set** — ~20-25 most shelf-frequent additives across Bari's live categories (derive
   frequency from existing ingredient/corpus data where possible, else propose the candidate set). Per additive:
   identity (E-number, name, function class), evidence tier (confirmed-negative / likely-neutral / functional /
   dose-dependent / contested / disclosure-gap), best authoritative source (EFSA/JECFA/FDA/Cochrane), ADI where
   relevant, and a one-line plain-Hebrew-ready consumer explanation draft. Evidence-first: no defensible source → tier = uncertain/disclosure-gap, never a guess.
3. **Nutrient-interpretation framework registry** — protein, fiber (intrinsic vs added/isolated), sugar
   (total/added/free + sweeteners), sodium, saturated fat (flag the contested matrix debate), total fat / fat
   quality (trans = confirmed-negative), energy density (context, not "less=better"), micronutrients/fortification.
   For each: authoritative framework(s) + thresholds, the three-layer treatment, **the Israeli MoH red-label
   anchor called out explicitly**, and a confidence note.
4. **Source/API leverage map** — which dataset/API feeds each dimension (USDA FoodData Central, EFSA OpenFoodTox,
   JECFA/Codex GSFA, FDA Substances-Added-to-Food/GRAS, PubChem, OFF additives taxonomy, Tzameret, il_gov_data,
   literature/Cochrane), distinguishing **live-API vs bulk-import-and-curate**, and what NEW wiring is required.
5. **Recommendations** — cheapest/highest-value first (lean order: D5/D6 → protein table → additive prototype →
   gate D4 scale on engagement); and **maintenance-liability flags** (which tables rot → need a review cadence).

## Constraints
Evidence-first, cite authorities, mark confidence, flag where Israeli/EU/US standards diverge. No engine code,
no score movement, nothing adopted. Use the live integration layer (TASK-170) where it already covers a source.
Keep it tight — a buildable scoping dossier, not an academic review.
