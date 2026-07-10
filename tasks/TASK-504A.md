---
id: TASK-504A
title: GLP-1 / suppressed-appetite dairy guide (מדריך pilot)
owner: frontend-agent
status: CHANGES_REQUESTED
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

## Blocked → owner decision (RESOLVED 2026-07-05)
Milk-shelf GLP-1 guide could not ship honestly. Owner chose option (b): commissioned the high-protein-dairy
corpus, which became **TASK-515/515A (yogurt category)** — cottage was already in-corpus but skyr/Greek/
protein-yogurt were not. Owner: "build a real yogurt category." TASK-515/515A shipped 2026-07-08 (two
owner-ready comparison pages, spoonable 78 + drinkable 20, both zero-open-finding after 3 red-team rounds).

Spin-off: **TASK-513** (literature.py wrong-DOI citation-integrity bug) — surfaced by the original milk-shelf
assessment's Research lane. CLOSED 2026-07-05.

## Re-pivot on the yogurt corpus (2026-07-08, same session as TASK-515/515A close)
Original blocker resolved — re-scoped and rebuilt on real data, not the milk-shelf compromise.
1. **Product re-scope ✅ GO** (orchestrator-verified against live JSON): RT-1 (protein bar was a low-cal-filter
   artifact) and RT-2 (medication frame lacked real high-protein-dairy backing) both resolved — 23/78 spoonable
   products clear ≥8g protein/100g in a real bimodal tier (top group 10-13g, dead zone 6.5-10g, not a smooth
   gradient a fat-trim could climb). Scope: spoonable primary/backbone, drinkable folded in as a secondary
   "on-the-go" callout only (3/20 clear the threshold — too thin for a standalone section).
2. **Nutrition bar-finalization ✅ LOCKED** (independently re-derived, all numbers orchestrator-verified exact):
   protein bar = absolute grams, ≥8g/100g threshold; sodium bands = real corpus stats (≤35/36-65/&gt;65mg);
   sugar bar REDESIGNED (planned field didn't exist in the real data) → 3-way word-boundary keyword +
   d4_additives classifier, caught 2 real substring-collision traps (סוכר⊂סוכרלוז, פרוקטוז⊂אוליגופרוקטוז).
   `satiety_support` re-confirmed DROPPED (still calorie/ratio-driven one layer down, worse than first reported).
3. **Content GATE-1 ✅ + Adversarial QA GATE-2 ✅ PASS** (after one real round: RT-1 wrong-additive-identity on
   barcode 7290119377411 fixed + verified; RT-2 no on-disk evidence record for the hero's lean-mass/protein
   science claims → Research produced `GLP1_GUIDE_SCIENCE_COSIGN_v1.md`, 11 real CrossRef-verified PMIDs,
   primary source PMID:41877354 [2026 meta-analysis, 20 RCTs, 15,782 participants] reports "25%-39%" verbatim;
   both hero claims ruled defensible as written, no reword needed). Two-gate complete.
4. **Frontend build ✅ RETURNED**: `/madrichim/yogurt-glp1`, noindex until owner robots-flip, reuses frozen
   ScoreChip + CategoryNoteBox components, copy rendered byte-frozen, 23/23 copy fields verified verbatim in
   DOM, all grade badges pulled live from the shipped comparison JSON (no new scores). **Frontend correctly
   caught + disclosed a spec-conflict** (2 S-grade products' badges fold to "A" per the frozen chip's no-S-slot
   rule, matching the live comparison page) which surfaced a real gap: the signed-off copy's prose for those 2
   products literally said "דירוג S," contradicting the A-badge — the SAME defect class (RT-R2-1) already
   caught once this session on the spoonable comparison page. Orchestrator confirmed + dispatched the fix
   (genericize, same pattern as the earlier fix) before terminal red-team.
5. **Terminal red-team ✅ RETURNED + orchestrator-VERIFIED: OWNER-READY.** 0 open CRITICAL, 0 open HIGH.
   All 3 fixes this session (RT-1 additive identity, RT-2 evidence record, S-vs-A copy/chip mismatch)
   confirmed live and correct. Shortlist independently re-derived as the complete, correct intersection
   (4/4, no product wrongly omitted) across the full 78-product corpus. 0 drug names, 0 per-product
   medical claims, 0 "GLP-1 friendly" badge, 0 nausea/fiber/hydration in visible output anywhere. Full
   report: `02_products/yogurt_system/guides/red_team_yogurt_glp1_guide_task504a_v1.md`. 1 MEDIUM
   (TASK-531, VM over-serialization, consumer-invisible/noindex, non-blocking) + 1 LOW (TASK-532)
   routed, not blocking.
6. ~~**FINAL GATE:** owner index/robots flip~~ — superseded by owner review below.

## OWNER REJECTION (2026-07-08, localhost review) → CHANGES_REQUESTED
Owner: "extremely bad work as well. The theme of this article is abit GLP-1. We need a rich background
to explain the issues + visuals + youtube links + rich context and then explain the protein thing and
provide recommendations. Why just Yogurts also? complete logic failure here."
Verdict: the shipped guide is a thin shortlist page, not the rich educational article the topic demands,
and yogurt-only coverage is a scoping error. Full re-scope tracked as **TASK-535** (Product architecture
+ Research evidence/video pack → Content → Frontend rich-article build). This task stays
CHANGES_REQUESTED until the re-scoped guide replaces the current page. Page remains noindex throughout.
