---
id: TASK-181A
title: "Glass Box W3 — Research: expand additive library to full shelf-frequent set + wire EFSA/JECFA/FDA evidence sources"
owner: research-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-04
completed_at: 2026-06-04
cc_reviewed: 2026-06-04
depends_on: []
blocks: []
category_id: null
roadmap_impact: true
work_type: research
close_reason: >
  CC close-readiness gate PASS (2026-06-04). Artifact verified at
  01_framework/glass_box/additive_library_expanded_v1.md (35 KB). Claims independently
  confirmed against the file, not the return prose: (1) NO evidence tiers assigned —
  header "What this is NOT" + §6 "Handoff to Nutrition — explicit non-decisions" frame
  every tiering judgment as an open question for 181B (incl. line 473 "confirm these are
  functional", which is a question to Nutrition, not an assignment); (2) integrity —
  score_engine.py / constants.py absent from git changes, only the .md was created, no
  comparison JSON newly modified by the agent; (3) 36 additives (20 prototype carried +
  16 new), per-corpus frequency table present; (4) 9 EVIDENCE-GAP additives recorded,
  each with a JECFA/FDA fallback anchor, none fabricated (CLAUDE.md hard rule honored).
  Two findings propagated downstream (not blockers): (a) SCOPE — agent scanned the
  *displayed* JSONs per spec; displayed bread JSON carries ingredient text for only 9/24
  products → 0 additives on the displayed bread shelf; prototype bread additives carry
  forward at displayed-frequency 0 (consistent with TASK-179Y bread glassBox=false). (b)
  WIRING GAP — EFSA numeric ADI + JECFA ADI have no free REST API (web-scraped);
  openfda.py covers recalls/AEs not GRAS/CFR; agent recommends a one-time EFSA
  OpenFoodTox bulk import — routed to 181C (Product maintenance/wiring decision).
summary: >
  Expand the D4 additive library from the 24-row prototype (additive_prototype_set_v1.md) to the full set of additives observed on Israeli shelves across the displayed corpora (hummus/maadanim/bread/veg-spreads + any next category). Guardrail: classify SHELF-PRESENT additives, not the full E-number space. Bulk-import + curate evidence from EFSA OpenFoodTox, JECFA, and FDA additive evaluations (import-and-curate, NOT live-per-product). Deliver: an expanded additive evidence sheet (per-additive: identity, function, EFSA/JECFA/FDA evaluation refs, ADI where set) ready for Nutrition tiering in 181B. No scoring, no tiering decisions (Nutrition owns tiers).
---

# TASK-181A — Glass Box W3: Research — expand additive library + wire EFSA/JECFA/FDA evidence

Part of **TASK-181** (Glass Box program-of-record), Wave 3.

## Deliverable
`01_framework/glass_box/additive_library_expanded_v1.md` — full shelf-present additive library
with curated EFSA/JECFA/FDA evidence, ready for Nutrition tiering (181B). No tiers assigned, no
score moved, annotate-only.

## Return block — Research Agent (2026-06-04)

- **Output:** `01_framework/glass_box/additive_library_expanded_v1.md` (35 KB).
- **Counts:** 36 additives total — 20 prototype carried forward + 16 newly added (colours E160a/E163/E162/E100/E141,
  acid-salts E331/E333/E327/E296/E270, hydrocolloid E401, E516, E500, E575 GDL, E960 steviol, modified-starch E1412/E1414).
  Top displayed-shelf frequencies: sorbates 60 · modified starch 50 · citric/citrates 47 · sodium carbonate 37 · carrageenan 34 · xanthan 26.
- **Scope correction (flagged):** scanned the *displayed* comparison JSONs (hummus 62 + maadanim 84 + bread 9-with-text = 155),
  per spec. Displayed `bread_frontend_v2.json` carries ingredient text for only 9/24 products (all clean) → **0 additives on the
  displayed bread shelf**; prototype bread additives (E282/E481/E472e/E300) carry forward at displayed-frequency 0.
- **EFSA/JECFA/FDA wiring gap:** identity + function + EFSA evaluation pointer + over-exposure flag are LIVE via
  `integrations/clients/food_additives.py` (OFF taxonomy); **EFSA numeric ADI + JECFA ADI** have no free REST API (web-scraped);
  `openfda.py` covers recalls/AEs, not GRAS/CFR. Recommends a one-time **EFSA OpenFoodTox bulk import** → routed to 181C.
- **EVIDENCE GAPs (9):** E331, E333, E327, E296, E270, E516, E575, E141, E1412/E1414 — no discrete EFSA numeric opinion;
  each anchored on JECFA "not limited" and/or FDA CFR. Never fabricated.
- **Integrity:** no tiers assigned (Nutrition's call in 181B), no score moved, no JSON edited, no engine code touched.

**CC close-readiness gate: PASS (2026-06-04)** — claims verified against the artifact. CLOSED.
