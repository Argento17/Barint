---
id: TASK-029
title: Bari Category Launch Queue v1
owner: product-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-05-30
completed_at: 2026-05-30
depends_on: []
blocks: []
category_id: null
summary: >
  Bari Category Launch Queue v1. Frontmatter added by TASK-125 (the file existed with a full body
  but no YAML block, so it surfaced as REGISTRY_UNPARSEABLE). Body unchanged.
---

# TASK-029 — Bari Category Launch Queue v1

**Status:** Complete  
**Owner:** Head of Product  
**Date:** 2026-05-30  
**Inputs:** TASK-014 (Category Expansion Plan), TASK-015 (Category Factory), TASK-018 (Hummus Launch), TASK-024 (Hummus Execution Plan), TASK-026 (Scope Decision)

---

## Executive Summary

Hummus is the active factory run. This document defines the five categories that enter the factory after Hummus ships, in priority order. Three categories (Bread, Snack Bars) are data-complete and require frontend production only. Three categories (Yogurt, Milk, Cereals) require a full factory pass. Yellow Cheese is governance-cleared but deferred due to execution complexity and absent data. Oil, Frozen Meals, and Supplements are structurally deferred — not execution choices but framework constraints.

---

## Launch Queue

| Slot | Category | Hebrew | Rationale |
|------|----------|--------|-----------|
| 1 | Bread | לחם | BSIP2 complete + calibrated (3 runs). Blog content ready. Shovel-ready: frontend work only remaining. Highest consumer value among data-complete categories — sourdough gap and "multigrain" halo are the most frequently encountered label-trust failures in the Israeli bread aisle. |
| 2 | Snack Bars | חטיפי בריאות | BSIP2 complete. Corpus v2 (18 products). Explanation engine v2 with trace-verified text. Blog handoffs built. Shovel-ready: frontend work only. Closes the date-bar vs. protein-bar confusion problem that has no existing consumer resource. |
| 3 | Yogurt | יוגורט | Highest-priority new BSIP pipeline category. BSIP0 dairy section already scraped (Yohananof). BSIP1 pipeline extends from milk. Product directory exists (`02_products/yogurt_system`). One new BSIP2 dimension required (`fermentation_quality`). Routing anchor "יוגורט" is unambiguous. Fermentation interpretation is the single highest-value signal Bari can add in the dairy aisle — probiotic claims are pervasive and largely unverifiable from label data. |
| 4 | Milk | חלב | Governance production simulation complete (verdict B — Launch Ready with Conditions). Product directory exists (`02_products/milk_and_alternatives`). Shares BSIP0 dairy scope with Yogurt (Slot 3); enter factory immediately after yogurt run closes. Five-pool structure defined. Three D6 claim thresholds documented, pending ratification. Plant-based pool (Pool D) activates DISTORTION-004 endemic note. |
| 5 | Cereals | דגני בוקר | Governance stress test passed (verdict B). Product directory exists (`02_products/breakfast_cereals`). `cereal_system` archetype is active; `run_cereals_001` complete. `run_cereals_002` is the launch gate — must complete before frontend. Children's segment (Sec 2.8) and fortification endemic note (DISTORTION-004, Sec 6.4) required before publishing. Highest endemic distortion count of any category in the queue. |

---

## Ranking Rationale by Criterion

### Consumer Value

| Slot | Category | Consumer value signal |
|------|----------|-----------------------|
| 1 | Bread | Daily staple; sourdough + multigrain wellness fraud is the most visible trust gap in Israeli retail |
| 2 | Snack Bars | Growing snacking category; "date bar is natural" vs. "protein bar is healthy" is a live consumer confusion |
| 3 | Yogurt | Most-purchased refrigerated dairy; probiotic + light + protein claims are high-frequency and poorly validated |
| 4 | Milk | Essential household staple; plant-based alternatives drive confusion; lactose-free premium poorly justified |
| 5 | Cereals | Large children's segment with highest marketing distortion density; parents are the most motivated Bari audience |

### Execution Complexity

| Slot | Category | Complexity | Primary constraint |
|------|----------|------------|--------------------|
| 1 | Bread | LOW (data done) | Frontend production only |
| 2 | Snack Bars | LOW (data done) | Frontend production only |
| 3 | Yogurt | MEDIUM | `fermentation_quality` BSIP2 module required |
| 4 | Milk | MODERATE | 3 D6 thresholds; 5 pools; 2 endemic distortion notes |
| 5 | Cereals | MODERATE-HIGH | `run_cereals_002`; children's D3 threshold; DISTORTION-004 endemic note; most active distortions |

### BSIP Readiness

| Slot | Category | BSIP status |
|------|----------|-------------|
| 1 | Bread | COMPLETE — `bread_retail_003` + calibration patch v1 applied; v2 JSON is canonical |
| 2 | Snack Bars | COMPLETE — corpus v2 (18 products); explanation engine v2; trace-verified |
| 3 | Yogurt | READY TO START — BSIP0 dairy scraped; BSIP1 pipeline active; v3 router archetype slot defined |
| 4 | Milk | READY TO START — governance simulation confirms pool structure; BSIP0 scope defined |
| 5 | Cereals | IN PROGRESS — `run_cereals_001` done; `run_cereals_002` is the next step |

### Data Availability

| Slot | Category | Data signal |
|------|----------|-------------|
| 1 | Bread | 258 scraped / 81 coherent (retail run); ingredient access confirmed in calibration patch |
| 2 | Snack Bars | 18 curated canonical products; 4 NOVA-free shelf filters active |
| 3 | Yogurt | Yohananof dairy section scraped; plant-based yogurt will require supplemental scrape |
| 4 | Milk | Standard dairy well-scraped; plant-based (Pool D) may need dedicated scrape pass |
| 5 | Cereals | Yohananof cereal section scraped; children's segment requires targeted inclusion to avoid healthy-skew bias |

---

## Dependencies

### Slot 1 — Bread
- **None blocking.** All BSIP work complete.
- Canonical data: `02_products/bread_retail_003/`, v2 JSON from `calibrate_lechem_scores.py`
- Blog: 2 articles, Cursor handoffs ready (`bari_bread_blog_v3.md`)
- Gate before launch: Governance Stress Test (E6 advisory) recommended before first consumer-facing publish
- D6 open: Sourdough claim threshold — not resolvable from label data; document limitation; Finding type excluded from bread until process data available

### Slot 2 — Snack Bars
- **None blocking.** All BSIP work complete.
- Canonical data: `02_products/snack_bars/`, corpus v2, `bsip2_explanation_engine_v2`
- Blog: 2 articles, Cursor handoffs ready (`bari_snack_bar_blog_v1.md`)
- Governance ruling: Date-bar sub-pool (Section 2.9 inverted-NOVA case) — one paragraph, document before frontend
- Endemic: DISTORTION-002 (protein source quality) activates for protein bar pool; category note required

### Slot 3 — Yogurt
- **Blocking: `fermentation_quality` BSIP2 module** — covers live culture signals, heat treatment markers, probiotic claim detection in Hebrew
- Depends on: Slot 4 (Milk) shares BSIP0 dairy scope; yogurt and milk can be scraped in a single BSIP0 run
- D6 blocks to resolve before Marketing Divergence Findings: probiotic claim threshold; plant-based protein comparison threshold
- Children's exposure: LOW (no significant children's yogurt segment); Section 2.8 available if needed
- Pool structure: plain / flavored / protein-fortified / kefir / plant-based / dessert-adjacent (skyr/mousse) — six pools; plant-based may activate DISTORTION-004

### Slot 4 — Milk
- **Blocking: 3 claim thresholds require ratification** — protein ≥5.5g/100ml; light ≥25% fat reduction; calcium ≥120mg/100ml. D6 gates Marketing Divergence Findings until documented.
- Depends on: Slot 3 (Yogurt) dairy BSIP0 run covers milk scope simultaneously
- Growing-up formulas (Pool E): Section 2.8 confirmed — excluded from adult pools; D2+D3 indicators documented
- Endemic: DISTORTION-007 (Pool A — lactose as natural sugar); DISTORTION-004 (Pool D — plant-based fortification). Two separate category notes; do not consolidate.

### Slot 5 — Cereals
- **Blocking: `run_cereals_002`** — must complete before frontend. Run_001 identified routing gaps; run_002 corrects them.
- D3 calibration: Children's cereal serving size threshold (≤25g for cereals) — document before launch
- Endemic: DISTORTION-004 (fortification) — category note required under Sec 6.4
- Granola: Sub-pool established via Section 2.9 (standing precedent); cross-pool comparison requires purpose divergence disclosure
- Sourdough threshold is NOT a cereals concern — but whole-grain threshold (≥30% / ≥51%) is already in Sec 5.2.1

---

## Deferred Categories

### DEFERRED — Yellow Cheese (גבינה צהובה)
**Reason:** Governance cleared (no constitutional amendment required), but execution complexity is the highest of any category in the backlog. No BSIP data exists. Full BSIP0 scrape required. Three open D6 blocks ("light" threshold, D3 children's cheese threshold, DISTORTION-010 endemic potential). Sub-pool multiplicity (hard cheese / processed cheese / cream cheese / labaneh) requires the most analyst judgment of any category yet attempted.

**When to reconsider:** After Yogurt + Milk dairy pipeline is proven (Slots 3–4). Yellow Cheese enters the factory as Slot 6, using the established dairy BSIP0 scope.

**Pre-work to complete before entry:** "Light" claim threshold (≥25% fat reduction from reference); DISTORTION-010 endemic assessment for hard cheese; labaneh/cream cheese pool boundary ruling.

---

### DEFERRED — Tahini (טחינה)
**Reason:** Naturally extends the Hummus launch. Shares sauce_spread / whole_food_fat archetype. No new BSIP2 dimensions required. Consumer value is real but standalone urgency is low — tahini is typically purchased alongside hummus; a combined spread/dip shelf page may deliver more value than a standalone tahini category. The Hummus factory run (TASK-018/024) resolves the routing tension between `whole_food_fat` and `sauce_spread`; Tahini inherits the resolution.

**When to reconsider:** Post-Hummus launch debrief. If Hummus shelf page shows strong engagement and tahini is a high-traffic companion query, fast-track Tahini as a Slot 6 add-on. If not, defer to post-Slot 5.

---

### STRUCTURALLY DEFERRED — Olive Oil (שמן זית)
**Reason:** Fundamental data gap. Fatty acid profiles (oleic acid, omega-3/6, polyphenol content) are not included on Israeli nutrition labels and cannot be inferred from available retail scrape data. Without these, oil scoring is driven almost entirely by NOVA level — technically correct but commercially useless (cannot distinguish extra-virgin from refined). Scores would mislead consumers with high confidence.

**Resolution path:** Requires a dedicated data enrichment strategy (e.g., manufacturer API access, third-party fatty acid database). Do not add to queue until data strategy is defined.

---

### STRUCTURALLY DEFERRED — Frozen Meals (ארוחות קפואות)
**Reason:** Composite ingredient parsing problem — nested ingredient lists (e.g., "tomato sauce (tomatoes, salt, olive oil)") are not supported by BSIP2's flat ingredient list model. This is a v4+ architecture task. Adding frozen meals now produces architecturally unsound scores.

**Resolution path:** BSIP2 v4 composite ingredient parser. Not on current roadmap.

---

### DO NOT ADD — Supplements / Protein Powder
**Reason:** BSIP2 is a structural food interpretation engine. Supplements are not food in the BSIP2 sense — their quality criteria (amino acid profile, digestibility, heavy metal contamination) are not available from Israeli retail label data. NOVA proxy correctly classifies every protein powder as NOVA 4, which is accurate but uninformative. A separate `BSIP_SUPPLEMENT` track with its own framework is required.

**Resolution path:** Separate product track. Not a BSIP2 extension.

---

### NOT IN QUEUE — Legumes / Whole Beans (קטניות)
**Reason:** Simple category scientifically (NOVA 1–2; protein + fiber are clear quality anchors; minimal marketing distortion). Consumer decision value is lower than other queue candidates — nutritionally coherent products with few deceptive claims. Hummus covers the highest-stakes use case (legume spread). Standalone legume shelf page is low urgency.

**When to reconsider:** After Slot 5 (Cereals), if product expansion continues into pantry staples. Legumes is a fast, low-risk factory run when bandwidth is available.

---

## Target Factory Order

| Factory Slot | Category | Type | BSIP Gate | Frontend Gate |
|---|---|---|---|---|
| Active | Hummus | New pipeline run | run in progress | post-BSIP2 |
| 1 | Bread | Frontend only | COMPLETE | blog handoffs ready |
| 2 | Snack Bars | Frontend only | COMPLETE | blog handoffs ready |
| 3 | Yogurt | Full factory run | BSIP0→BSIP2 (fermentation_quality) | post-BSIP2 |
| 4 | Milk | Full factory run | BSIP0→BSIP2 (shares dairy scope with Slot 3) | post-BSIP2 |
| 5 | Cereals | BSIP2 run + frontend | run_cereals_002 | post-run_002 |

**Note on Slots 3 and 4:** Yogurt and Milk share a single BSIP0 scrape pass (both are in the dairy section). Run them as a combined BSIP0 operation. Diverge at BSIP2 into separate archetype interpretations. This reduces two BSIP0 scrape sessions to one.

---

## Recommended Next Step

**Ship Slot 1 (Bread).** No pipeline work remains. Bread has the highest data completeness, the most calibration investment (3 runs + patch), and a clear consumer value proposition. The sourdough disclosure limitation (D6 — no Marketing Divergence Finding for sourdough claims) must be documented before publish but does not block the category page. Bread ships as a working frontend page with 81 coherent products, calibrated scores, and two editorial articles. This advances the Consumer Interaction Validation phase while Slot 3 (Yogurt) BSIP pipeline begins in parallel.

**Concurrent action:** Begin Yogurt BSIP0 scrape pass. Dairy section is already scraped for milk; a targeted yogurt + milk combined pass can be run in the same session. `fermentation_quality` module is the only new BSIP2 engineering required.

---

*TASK-029 — Bari Category Launch Queue v1*  
*Head of Product — 2026-05-30*  
*Next review: After Slot 2 (Snack Bars) ships or Slot 3 (Yogurt) BSIP run completes, whichever comes first*
