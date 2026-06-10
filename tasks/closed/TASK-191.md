---
id: TASK-191
title: "Butters — full pipeline (BSIP0 → site comparison page)"
status: CLOSED
owner: data-agent
created: 2026-06-05
completed_at: 2026-06-05
roadmap_impact: false
close_reason: >-
  CC close-readiness gate PASS (2026-06-05). Full pipeline delivered: BSIP0 (39 products,
  Shufersal+Yohananof+Carrefour) → BSIP1 enriched (39/39 sufficient via USDA FDC/OFF) →
  BSIP2 butter_run_003 (EV-047+EV-048+EV-050 all active) → frontend JSON → site page.
  Three engine fixes landed: EV-047 (kcal ceiling 700→800), EV-048 (sat-fat cap endemic
  gate for whole_food_fat), EV-050 (dairy trans fat veto endemic gate, PHVO-based). Score
  distribution: B=26 plain unsalted 70/B cluster (owner-confirmed correct finding), C=12
  salted 50/C + additive spread 53.8/C, D=1 flavored 45.2/D, E=0. Route /hashvaot/butter
  live in Next.js build (PASS), butter added to /hashvaot index + sitemap. Hebrew copy: 43/43
  texts clean (category note + 3 insight lines + 39 verdicts). Owner M2 gate cleared
  2026-06-05 ("all road to close"). butter_frontend_v2.json deployed to bari-web/src/data/comparisons/.
category: butter
route: /hashvaot/butter
milestones:
  - id: M1
    name: "Scrape validated — owner approves product list"
    gate: owner_approval
  - id: M2
    name: "Pre-publish demo — owner reviews 4-5 product cards (content + image)"
    gate: owner_approval
pipeline_stages:
  - bsip0_scrape
  - bsip1_enrich
  - bsip2_score
  - frontend_json
  - site_comparison_page
---

## Objective

Run the complete Bari pipeline for the butter category (חמאה) — from Shufersal shelf scrape
through scored BSIP2 output, frontend JSON, and live comparison page at `/hashvaot/butter`.

## Scope

**Include:**
- Pure dairy butter (חמאה) — plain, salted, unsalted, cultured
- Imported European butters (Kerrygold, Anchor, President, Lurpak, etc.)
- Israeli dairy butters (Tnuva, Tara, Noga, Adom Adom, Beit HaEmek)
- Reduced-fat butter variants (if labeled "חמאה", not "מרגרינה")

**Exclude:**
- Margarine (מרגרינה) — different category entirely
- Butter-flavored spreads without predominant dairy butter (blends labeled מרגרינה+חמאה)
- Baking fats (שומן אפייה) 
- Cooking sprays

## BSIP2 routing

Router already handles `חמאה` → `whole_food_fat` archetype (Stage 2, 0.65 name_only signal).
`WHOLE_FOOD_FAT_FLOOR = 70`, but saturated fat Class-B cap will modulate to physiological
moderation range (~50-65) for high-sat-fat products.

## Milestone gates

- **M1 (BSIP0):** Owner reviews scraped product list before proceeding to enrichment/scoring.
  Present: product name, brand, barcode, scrape confidence, image URL.
- **M2 (pre-publish):** Owner sees 4-5 full product cards (score + grade + verdict text + image)
  rendered in the comparison page format before the page goes live.

## Work log

- 2026-06-05: Task opened. BSIP0 (Shufersal, Yohananof, Carrefour) + BSIP1 enrichment + BSIP2 run_001 + frontend JSON all complete. M1 approved.
- 2026-06-05: BLOCKED at M2 — owner froze for review. Scoring concern: category ceiling is C (45–60/C), compressed differentiation. No frontend page written. Content caveat left to Content Agent when unblocked.
- 2026-06-05: Owner initiated pre-ship scoring evaluation. Orchestrator dispatched Nutrition Agent (Q1: sat-fat cap appropriateness; Q2: floor-cap interaction differentiation; Q3: per-portion frame) and Red-Team Agent (adversarial challenge: consumer deception risk, cap defensibility, floor misuse, 59% insufficient ratio, missing differentiation signals) in parallel. Mechanical root cause confirmed from traces: ISRAELI_RED_LABEL_1_SAT_FAT cap fires universally (butter = 48–70g sat-fat/100g vs. 5g threshold) → cap=55, WFF floor downgraded to 60 (SRC-01 Class-B interaction), floor overrides cap → all plain butters = 60/C. FLOOR_CAP_INTERACTION flag fires on every product. Awaiting both reports before any scoring decision.
- 2026-06-05: Both evaluations returned. UNANIMOUS FAIL — two independent blocker classes. Class 1 (scoring): sat-fat cap categorically inapplicable to butter; fix = add category_endemic_sat_fat gate to ISRAELI_RED_LABEL_1_SAT_FAT in constants.py (fat_saturated_g/fat_g >= 0.50 exclusion for whole_food_fat), also fix kcal plausibility upper bound (~800) for high-fat archetype; requires new EV entry + D7 co-sign (Nutrition+Product) + butter_run_002. Class 2 (data): 23/39 (59%) INSUFFICIENT including Kerrygold (all 3 SKUs), Lurpak, President, Anchor, Tnuva plain, Adom Adom, Yotvata, Beit HaEmek — scored shelf is not representative of Israeli butter market. BLOCKED pending owner decision on path forward (see open questions).
- 2026-06-05: OWNER DIRECTIVE — Do not launch. Sat-fat cap fix endorsed. Current output not defensible. Owner philosophical position (binding): do NOT engineer artificial differentiation among plain butters. If honest scoring causes plain butters to cluster at similar scores, that is the correct finding and should be embraced and reported as such, not worked around by adding signals. Post-fix expected output: plain butter clustering at ~70/B (full WFF floor), additive-heavy spreads separating downward (~45-55/D) — this is a valid consumer-intelligence finding. Data enrichment for landmark brands (Class 2) still required for representativeness before any launch; scoring fix + re-run proceeds first.
- 2026-06-05: Owner set priority order — Phase A (parallel): (1) fix insufficient-data coverage [Data Agent], (2+4) fix kcal plausibility bug + sat-fat cap gate [Nutrition Agent, combined to avoid constants.py conflict], (3) verify additive-heavy spread scoring [QA Agent]. Phase B: re-run butter_run_002 [Data Agent] after all Phase A complete. Phase C: owner decides ranking vs transparency category. IN_PROGRESS.
- 2026-06-05: Phase A Step 3 DONE (QA Agent) — additive spread (7290108507997) correctly differentiated from plain butter (53.8/C vs 60/C; WFF floor correctly not applied; all 4 additives detected). Pre-launch blocker: expansion.explanation field contains raw rule names — frontend fix at M2. Non-blocking: E471/E476 not in sprint1_high_risk_emulsifier taxonomy (Nutrition Agent to document).
- 2026-06-05: Phase A Steps 2+4 DONE (Nutrition Agent) — EV-047 (kcal plausibility 700→800) + EV-048 (sat-fat cap endemic gate: whole_food_fat + sat_f/fat >= 0.50) implemented across constants.py, signal_extractor.py, score_engine.py, failure_taxonomy.py. Regression: 11 PASS + 1 pre-existing WARN, 0 FAIL; router 16/16 PASS. Zero score drift on all live categories. Awaiting Data Agent (Step 1) before Phase B.
- 2026-06-05: Phase A Step 1 DONE (Data Agent) — 39/39 sufficient (was 16/39). USDA FDC SR Legacy for 21 products; OFF for 2. All 23 enriched products carry verification_status: candidate (EDPG compliant). Data quality flag: President unsalted + Lurpak branded FDC entries show sodium_mg: 0.0 — needs label photo sanity check before QA promotion. 11 plain unsalted products share fdc_id=173430 (expected — composition is structurally similar). Phase A fully complete.
- 2026-06-05: Phase B dispatched — butter_run_002 running (Data Agent) with EV-047 + EV-048 active + enriched corpus. Awaiting score distribution before owner makes ranking-vs-transparency call.
- 2026-06-05: Phase B DONE — butter_run_002 complete (see above). UF-001 identified (dairy CLA trans fat veto misfire).
- 2026-06-05: EV-050 DONE (Nutrition Agent) — natural dairy trans fat (CLA/vaccenic acid) exempt from trans fat veto when: whole_food_fat AND no PHVO markers in ingredients. Gate is compositional+categorical (numeric thresholds overlap for industrial vs. natural). Residual signal preserved: fat_quality dimension retains trans_pen=20. Evidence tier: Moderate. Regression clean (11/12 PASS + pre-existing WARN, router 16/16). Product Agent D7 co-sign required before scores go live. butter_run_003 dispatched in parallel with co-sign.
- 2026-06-05: EV-050 D7 CO-SIGNED (Product Agent) — approved. Gate scope verified correct; industrial trans fat exposure confirmed non-gameable; residual fat_quality penalty confirmed preserved (butter cannot reach A). Content brief flag: consumer copy must not frame EV-050 as a health endorsement of dairy trans fat — it is a classification fix, not a nutritional claim. All three EVs (047/048/050) now have required co-signs. butter_run_003 in flight.
- 2026-06-05: Phase B — butter_run_003 DONE (Data Agent). 39/39 products scored, 0 pipeline errors. Grade distribution: B=26, C=12, D=1, E=0. EV-050 resolved UF-001: all 6 previously-0/E salted candidates now score 50/C (all_now_fixed=True). sat_fat_caps_fired=0 (EV-048 gated 39), trans_fat_vetoes_fired=0 (EV-050 suppressed all), FLOOR_CAP_INTERACTION=11 (all salted butters — LEGITIMATE). Confirmed sub-distribution (16 products): 9×70/B plain + 5×50/C salted + 1×53.8/C additive spread + 1×45.2/D flavored. Score range: 45.2–70, mean=63.3. Plain unsalted range: 70–70 (cluster). Salted range: 50–50 (cluster). Additive spread: 53.8/C. frontend_v2 JSON built and staged at C:\Bari\02_products\butter\butter_frontend_v2.json — NOT deployed (Phase C M2 gate required). Blockers: none. Ready for owner Phase C decision.
- 2026-06-05: Phase C DECISION — Owner resolved ranking-vs-transparency. Binding position: differentiation is valid only when (1) scientifically defensible, (2) reliably capturable at scale, and (3) explainable to consumers — all three simultaneously. Current engine correctly concludes that ~95% of pure butter is nutritionally equivalent on the signals it can read. That is the correct answer today. Grass-fed / dairy provenance (e.g. Kerrygold vs Tnuva separation) is a legitimate future dimension but requires a dedicated, validated framework — it is not an intuitive adjustment because consumers expect premium butter to win. DECISION: publish butter_run_003 distribution as-is. The unsalted B / salted C / additive-C–D / seasoned-D tier structure is the finding. The editorial framing should surface this structure rather than ranking within the B tier. Proceed to M2 gate. Dispatching: Content Agent (verdict copy + category caveat + content brief per EV-050 flag), QA Agent (candidate promotion + sodium=0.0 sanity check), Frontend Agent (comparison page build + raw explanation field fix for 7290108507997).

## CC Close Record (2026-06-05)

**Close-readiness gate: PASSED**

Independent verification:
1. **Engine fixes** — EV-047, EV-048, EV-050 all confirmed in constants.py + score_engine.py + evidence registry.
2. **butter_run_003** — 39 products, B=26/C=12/D=1/E=0. TRANS_FAT_VETO fires 0 times. EV-050 resolved all 6 previously-wrong 0/E products.
3. **Data coverage** — 39/39 sufficient confirmed via Python script (butter_bsip1_merged.json).
4. **Content** — 43/43 texts clean; category note + 3 insight lines + 39 verdicts; 3 subtype mismatches fixed.
5. **Route** — /hashvaot/butter in Next.js build output; build PASS; navigation + sitemap updated.
6. **butter_frontend_v2.json** — deployed to bari-web/src/data/comparisons/ (49,740 bytes, content-enriched). DRAFT flag removed.
7. **Owner M2 gate** — cleared 2026-06-05 ("all road to close is open").

**Status: CLOSED** (by CC Agent, delegated closing authority 2026-06-02)

---

## Artifacts produced (frozen at this state)

- BSIP0 merged corpus (39 products): `C:\Bari\02_products\butter\bsip0_outputs\butter_merged_corpus.json`
- BSIP1 enriched: `C:\Bari\02_products\butter\bsip1_outputs\butter_bsip1_merged.json`
- BSIP2 run_001 traces: `C:\Bari\02_products\butter\bsip2_outputs\butter_run_001\`
- BSIP2 summary: `C:\Bari\02_products\butter\bsip2_outputs\butter_run_001_summary.json`
- BSIP2 run_002 traces: `C:\Bari\02_products\butter\bsip2_outputs\butter_run_002\`
- BSIP2 run_002 summary: `C:\Bari\02_products\butter\bsip2_outputs\butter_run_002_summary.json`
- BSIP2 run_003 traces: `C:\Bari\02_products\butter\bsip2_outputs\butter_run_003\` (CANONICAL — EV-047/048/050 all active)
- BSIP2 run_003 summary: `C:\Bari\02_products\butter\bsip2_outputs\butter_run_003_summary.json`
- Frontend JSON v1 (built from run_001, superseded): `C:\Bari\02_products\butter\butter_frontend_v1.json`
- Frontend JSON v2 (built from run_003, STAGED — M2 gate required): `C:\Bari\02_products\butter\butter_frontend_v2.json`
- Frontend JSON copy (in bari-web, stale run_001): `C:\bari\bari-web\src\data\comparisons\butter_frontend_v1.json`
- Router patch: `router_v2.py` — hard anchor `("חמאה", "whole_food_fat", "dairy_butter", 0.92)` added
- Frontend builder v2: `C:\Bari\02_products\butter\build_frontend_v2.py`

## Open questions for owner review

1. Category ceiling at C: saturated fat red label fires universally at standard butter fat content. Is a C-ceiling comparison page valuable, or does this need a different framing (e.g. "best within a high-sat-fat category") or a different scoring lens?
2. 16 scored / 23 INSUFFICIENT ratio: is this shelf coverage sufficient, or should a second nutrition data pass happen before publish?
3. Score range 45–60/C: meaningful differentiation for consumers (salted vs unsalted = 10 points; flavored+additive = 15 points below) or too compressed to publish?

## Product Decision (2026-06-05)

**Decision: Fix and proceed (Option A) — phased.**

Both blocker classes are real and must be resolved before any page ships. However, the blockers are fixable, the pipeline artifacts are solid, and the owner has confirmed a clear philosophical position on what correct butter scoring looks like post-fix. Parking the category permanently would discard the pipeline work and leave Israeli consumers with no honest butter comparison tool. The right call is to fix the engine, enrich the data, and re-run.

The two blockers are not symmetrical. Class 1 (scoring) is a genuine engine bug — `ISRAELI_RED_LABEL_1_SAT_FAT` was designed for processed foods adding unnecessary saturated fat; firing it on whole dairy fat (48–70g/100g) is categorically inapplicable and produces scores the engine itself cannot defend. Class 2 (data coverage) is a shelf-representativeness problem — 59% INSUFFICIENT including all landmark import brands means the scored shelf does not reflect the Israeli butter market a consumer would actually shop. Publishing with either blocker present would be misleading. Publishing with both present would be indefensible.

**Phased execution plan (owner-directed):**

- Phase A (parallel): (1) Data Agent resolves insufficient-data coverage for landmark brands; (2+4) Nutrition Agent fixes kcal plausibility upper bound and adds `category_endemic_sat_fat` gate to `ISRAELI_RED_LABEL_1_SAT_FAT` in `constants.py` (combined to avoid constants.py conflict), with a new EV entry; (3) QA Agent verifies additive-heavy spread scoring under the proposed fix.
- Phase B: Data Agent runs `butter_run_002` after all Phase A deliverables are complete and Nutrition+Product D7 co-sign the new EV entry.
- Phase C: Owner decides ranking vs transparency framing based on the post-fix score distribution. Owner philosophical position (binding): do not engineer artificial differentiation. If plain butters cluster at ~70/B after the fix, that clustering is the correct finding and is presented as-is.

**Open question resolution:**

- Q1 (C-ceiling): Moot after the fix. Expected post-fix output is plain butters at ~70/B, additive-heavy spreads separating to ~45–55/D. That is a valid and publishable differentiation.
- Q2 (59% INSUFFICIENT): Must be resolved in Phase A before publish. Kerrygold, Lurpak, President, Anchor, Tnuva plain, and Adom Adom are not optional — they are the brands consumers compare by name.
- Q3 (compressed range): Post-fix range expected to widen. Reopen if Phase B output still shows insufficient spread.

**Banked asset status:** Not applicable. This is an active fix-and-proceed. The pipeline artifacts are valid and are the foundation for butter_run_002; they are not banked.

**Status after this decision:** IN_PROGRESS. No status change — owner already set this track. Phase A work is the current blocking action.
