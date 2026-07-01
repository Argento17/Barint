---
id: TASK-284
title: Margarine/shortening fat-technology: adjudicate 2 evidence deltas (seed-oil penalty; FH/IE vs PHO ceiling)
owner: nutrition-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-06-15
depends_on: []
blocks: []
category_id: null
summary: >
  Research (research/Margarine and Shortening Effects in Bari Scoring.pdf) validates the existing fat-tech-first engine (EV-012/Fix-C/EV-031/EV-048). Two open deltas to adjudicate as D6, gated by D7+Shadow backtest+owner: (1) seed_pen=10 conflicts with LA/inflammation meta-analyses + Bari's own misinformation_watch stance; (2) generic hardened-fat markers give FH/IE the full PHO 40-ceiling. Register research as evidence-registry entries; do NOT move published scores without gate.
---

# TASK-284 — Margarine/shortening fat-technology: adjudicate 2 evidence deltas (seed-oil penalty; FH/IE vs PHO ceiling)

## Origin
Owner supplied `research/Margarine and Shortening Effects in Bari Scoring.pdf` (ChatGPT-authored,
58 WHO/EFSA/FDA/BMJ citations, 2026-06-15) and asked that the engine "know this issue very well."
Orchestrator assessment: **the engine already implements ~the whole document** — fat-technology-first
scoring, not category-label. See memory `fat-technology-scoring-state`. The research is external
validation; only two deltas are genuinely new. This task adjudicates them.

## Inputs
- `research/Margarine and Shortening Effects in Bari Scoring.pdf` — primary research + citations.
- `research/israel_margarine_label_research_v1.md` — Israel-specific parser research (Gemini,
  2026-06-15). **Unverified leads** (flash model, some fabricated URLs) — verify before use.
- Engine: `03_operations/bsip2/proto_v0/src/score_engine.py` (`_score_fat_quality_sprint1`,
  `_fat_ratio_to_score`, `_red_satfat_penalty`) + `signal_extractor.py` (`_PHVO_MARKERS`,
  `has_seed_oil`, `trans_fat_status`). Already shipped: EV-012, Fix-C (PHVO ceiling 40), Fix-B
  (Hebrew markers), EV-031/R5 (graded sat-fat), EV-048 (whole-food-fat cap gate), EV-086 (מחמאה
  de-listed).

## Deliverable (D6 — gated by D7 Nutrition+Product, Shadow backtest, owner ratify if scores move)
1. Register the research as BSIP2 evidence-registry entries (`03_operations/bsip2/evidence_registry/`)
   with primary `source_doi`s from the PDF's citation list. Include a Section-B guardrail candidate:
   "do not penalize seed oils as inherently inflammatory."
2. **Delta 1 — seed-oil penalty.** `seed_pen=10` (fat_quality) vs the LA/inflammation meta-analyses
   and Bari's own `misinformation_watch` stance on seed-oil panic. Run a Shadow backtest: how many
   live products does it bind, and would removing/reducing it move any PUBLISHED grades? Recommend
   keep / reduce / remove with evidence tier. **Touches published scores → tripwire → no change
   without D7 + owner.**
3. **Delta 2 — FH/IE vs PHO ceiling.** Generic `שומן מוקשה / שומנים מוקשים` currently get the full
   PHO 40-ceiling. Israel research suggests generic מוקשה now ≈ fully hydrogenated / trans-free, and
   the true industrial-trans signal is `מוקשה חלקית`. Verify the Hebrew-term claims against real
   BSIP0 Israeli label scrapes, then recommend whether to reserve the full ceiling for
   `מוקשה חלקית / partially hydrogenated` and give generic hardened-fat a lighter FH/IE penalty.

## Out of scope / guardrails
- Do NOT move published scores in this task; produce the gated proposal only.
- Side-flag found during research (DO NOT act here): engine `_RED_LABEL_THRESHOLDS["sat_fat"]=5.0`
  vs regulatory 4.0 g/100 g — separate check, note only.
- US marketplace composition bands in the PDF = directional evidence, never values of record
  (engine reads in-house BSIP0 labels; EDPG firewall).

## Return (Nutrition Agent, 2026-06-15) — status RETURNED
- **EV-095** registered (research anchor + Section-B seed-oil guardrail); **EV-096** (seed-oil) and
  **EV-097** (FH/IE vs PHO) registered as gated D6 proposals in `bsip2_evidence_registry_v1.md`.
- **Delta 1 → REDUCE seed_pen 10→5** (not remove): LA/inflammation evidence kills the inflammation
  framing, but "שמן צמחי" remains a processing/ingredient-quality marker → 5-pt residual. Blast radius:
  has_seed_oil=True on 1008/4255 traces; seed_pen confirmed firing on 719; full removal crosses 27/719
  grade boundaries, 10→5 crosses ~10–14 (all single-grade upticks). **Touches milk (3) = frozen
  invariant → tripwire.**
- **Delta 2 → two-tier proposal** (`מוקשה חלקית`→ceiling 40; generic `מוקשה`→ceiling 55), **BLOCKED on a
  Data Agent ingredient-text verification pass** (trace ingredient text empty; needs BSIP1 source).
  Corpus check found 13 products with muksha markers — 2 confirmed `מוקשה חלקית`, 11 generic.
  Israel/Gemini claims correctly treated as UNVERIFIED; no parser change recommended on them alone.

## Orchestrator verification (2026-06-15)
- VERIFIED: EV-095/096/097 present in `bsip2_evidence_registry_v1.md`. VERIFIED: מוקשה/מוקשה חלקית
  terms present in real BSIP0 scrapes (cheese_spreads, cookies, cakes, cereals). Proposal accepted as
  a verified D6 deliverable; **not CLOSED** — gates pending (below).
- Minor gaps for downstream: (a) the recommended 10→5 blast radius is estimated, not exactly computed
  (only full-removal 27/719 is exact) — firm up in the Shadow re-score; (b) "milk has_seed_oil=3" is
  suspicious (milk shouldn't carry seed oil) — confirm in the Data pass; if an extraction artifact it's
  a separate data-quality finding.
- Temp scripts left in `tasks/`: `_temp_backtest_284.py`, `_temp_gradeshift2_284.py`,
  `_temp_phvo_verify_284.py`, `_temp_pdf_284.py` (retain for the Shadow re-score).

## Gates remaining (activation = owner decision; both deltas touch published scores incl. frozen milk)
1. ✅ **DONE — TASK-284A (Data Agent, CLOSED 2026-06-15).** PHVO split = **0 partial / 49 generic**
   (margarine-dominated; EV-097 unblocked). Milk seed-oil = 8 real plant-based drinks, 0 artifacts, 0
   frozen — anomaly resolved, no correction. EV-096 exact blast radius = **5 grade crossers** (not
   ~10–14), all upward, 0 frozen.
2. Product Agent: D7 co-sign on EV-096 + EV-097. ← NEXT
3. ✅ **DONE — TASK-284B (Data Agent, CLOSED 2026-06-15).** Built behind default-OFF `BARI_FAT_TECH_V1`
   (flag-OFF byte-identical, invariant PASS); shadow diff vs baseline. **EV-097 = 4/49 move, 0 grade
   changes** (45 inert under sat-fat). **EV-096 = 62 move, 2 registered grade crossers (both up).**
   **29 frozen-corpus products move score, 0 frozen grade changes** → exit 2 (milk + snack_bars are
   `class:frozen`). Two reconciliation items in TASK-284B (milk-freeze membership of the 4 plant-drink
   movers; 284A↔284B crosser mismatch).
4. **Owner ratification (frozen-invariant tripwire) — THE GATE.** Because activation moves 29 frozen
   scores (milk + snack_bars), even at 0 grade changes, the flag CANNOT flip globally without owner
   sign-off + a design choice: (a) accept the small frozen score nudges & re-freeze baseline, (b) scope
   the flag to EXCLUDE frozen corpora (don't re-score milk/snack_bars), or (c) hold. Substantive call:
   EV-097 *softens* margarine fat-quality scoring (low blast); EV-096 *softens* seed-oil penalty (broad
   but tiny). Both directionally aligned with research + de-anchor directive.
5. Separate task: `_RED_LABEL_THRESHOLDS["sat_fat"]` 5.0 → 4.0 g/100g.

## CLOSED — owner-accepted, activated + committed (2026-06-15)
EV-096 (seed_pen 10→5) + EV-097 (two-tier PHVO ceiling) fully adjudicated and ACTIVATED behind
`BARI_FAT_TECH_V1` (default ON). Gate chain: D6 (Nutrition) + D7 (Product, both CO-SIGNED) + owner
ratification + fully measured blast radius (**4 grade changes, all upward; 0 frozen grade changes; 0
invariant breaches; 6/6 invariants PASS**). Committed by the parallel /orchestrate (TASK-278) bundle:
`97a9213b` + `4cf58ac0` (SR + fat-tech go-live, comp JSONs updated, milk re-frozen). **Owner accepted the
bundled commit 2026-06-15.** close_reason: deliverable (the 2 fat-tech scoring deltas) complete, gated,
activated, committed, owner-accepted; orchestrator-verified the 4-grade signature + frozen invariants hold.

### Residuals carried OUT of this task (track separately — do not lose in the thread collision)
1. **QA + red-team for the fat-tech activation**: the parallel-thread go-live bundle may not have run the
   factory red-team gate specifically for the fat-tech change — confirm before/at deploy. (Per the
   render+red-team terminal-layer rule.)
2. **Legacy milk page** comp data: milk re-frozen in engine; its legacy MVP frontend refresh still pending
   (4 plant-drink sub-grade nudges, 0 grade change) — fold into milk's next rebuild.
3. **Separate task:** `_RED_LABEL_THRESHOLDS["sat_fat"]` 5.0 → 4.0 g/100g (regulatory; out of TASK-284 scope).
4. Temp scripts/artifacts under `tasks/` (`_temp_*_284*.py`, `TASK-284D-artifacts/`) — housekeeping cleanup.

## OWNER RATIFICATION (2026-06-15) — "On everywhere + re-freeze"
Owner ratified activating `BARI_FAT_TECH_V1` (EV-096 + EV-097) **on all published categories**, and
**accepting + re-freezing** the sub-grade frozen score nudges on milk + snack_bars at the new values.
Frozen-invariant tripwire (tripwire-1) CLEARED by owner. Confirmed (orchestrator check): the 4 moved
plant-drink products ARE in the published milk set (`bari-web/src/data/milk-comparison.json` +
`run_milk_002`), so this is a real frozen-score change — now owner-authorized.

### Deployment runway (gated, consumer-facing — still sequence properly)
0. ⚠️ **PRE-DEPLOY MEASUREMENT GAP (orchestrator-caught 2026-06-15).** The Shadow run (TASK-284B)
   covered only the 12 REGISTERED corpora (704 products). `cakes_hard_cookies` + `cookies_coffee` are
   NOT in `shadow_registry_v1.json`, yet they hold the BULK of the 49 PHVO/margarine products (cakes 42 /
   cookies 14, per TASK-284A) — so **EV-097's main blast radius is UNMEASURED** ("4/49, 0 grade" is the
   registered subset only). Same for EV-096's 3 non-registered crossers (cakes/cookies/salty_snacks per
   TASK-284A). **Before global activation:** register or directly re-score cakes_hard_cookies +
   cookies_coffee + salty_snacks under `BARI_FAT_TECH_V1=on`, diff vs baseline, get the real grade impact.
1. ✅ **Product D7 co-sign** on EV-096 + EV-097 (TASK-284C, CLOSED 2026-06-15) — both CO-SIGNED.
2. Implement activation: wire `BARI_FAT_TECH_V1=on` into the category ship configs +
   `shadow_registry_v1.json engine_default_flags`; re-score affected published categories; regenerate
   frontend JSON.
3. **Re-freeze:** capture new milk + snack_bars frozen baselines at the new values; update the freeze
   records + the CLAUDE.md frozen-invariants note (milk reference moves off the bare `run_005_headpin`
   to a `+BARI_FAT_TECH_V1` headpin) + promote a new APPROVED Shadow baseline.
4. QA Agent verification (score propagation, no unintended regressions) + red-team gate (consumer-facing pages).
5. Owner final go-live (publish) — the consumer-facing deploy step.
