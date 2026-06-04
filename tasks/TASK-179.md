---
id: TASK-179
title: Glass Box — Evidence-Aware Engine Evolution (program)
owner: nutrition-agent
status: IN_PROGRESS
priority: HIGH
created_at: 2026-06-03
depends_on: []
blocks: []
category_id: null
roadmap_impact: true
work_type: objective
drift_ack: "Closure-drift on TASK-179 is the return-header regex (TASK-\\d+) collapsing the sub-task header **Task:** TASK-179A → TASK-179. The dossier is authored by 179A (CLOSED, deliverable expected); the umbrella is legitimately IN_PROGRESS (objective program-of-record). Not real drift — same pattern affects any lettered sub-task whose parent is still open."
summary: >
  Program-of-record to evolve BSIP2 from a single collapsed grade into six explicit,
  separable dimensions (D1 nutrition · D2 ingredient evidence · D3 processing signal ·
  D4 additive evidence · D5 transparency/disclosure · D6 confidence) while PRESERVING
  one decisive consumer grade. Born from the clinician stress-test (2026-06-03): label
  visibility is partial, engineering is not inherently bad, additives need evidence not
  vibes, and the engine must not pretend certainty. Lean sequencing: ship the cheap
  honesty axes (D5/D6) first; treat the additive library as a DEMAND-GATED bet. All work
  is flagged, OFF = byte-identical, owner-gated before any published score moves; frozen
  invariants (milk/snack-ceiling/bread) re-verified, never assumed. Sub-tasks created per
  wave as each is initiated (SIE/TASK-171 pattern). First in flight: TASK-179A (Research
  scoping of enrichment frameworks).
---

# TASK-179 — Glass Box: Evidence-Aware Engine Evolution

**Status:** **W0 (foundation) COMPLETE 2026-06-04** — TASK-179A (enrichment scoping) · TASK-179B
(six-dimension contract) · TASK-179C (Product co-sign + owner ratification) all CLOSED; the four
governance postures + D-SCO-1 rollup resolved (**DEC-006**). **W1 (D5 transparency + D6 confidence —
the cheap honesty axes) is cleared to build.** Later wave sub-tasks created as the owner initiates
each (mirrors TASK-171/SIE: umbrella + phases on execution).

## Origin
Clinician stress-test (2026-06-03). Four challenges, all valid, none fatal:
1. **Partial label visibility** — labels disclose first-level ingredients only ("protein blend",
   compound ingredients, no proportions/source). Missing data is a structural market limit, not a parser bug.
2. **Engineering ≠ bad** — long ingredient lists / additives / isolates are not automatically worse.
3. **Additives need an evidence model** — confirmed-negative / likely-neutral / functional /
   dose-dependent / contested / disclosure-gap — not "unfamiliar name = harm".
4. **No false certainty** — say what we know, infer, and cannot know, with confidence + evidence.

The critique does not destroy Bari; it destroys the crude "ingredient list + processing penalty = health
score" version and strengthens the better one: *observable label data + scientific evidence + uncertainty-aware
interpretation + local trust = food-intelligence platform.* Codename **Glass Box** (decisive outside, fully
inspectable underneath — the opposite of Yuka's black box; also the published-methodology / NDA materials asset).

## Target-state engine: six dimensions → one decisive grade
| Dim | Answers | State |
|---|---|---|
| D1 Nutritional quality | macro/micro merit, category-relative | exists (TASK-169 rubric) |
| D2 Ingredient evidence | what named ingredients are + evidence | partial (Evidence Registry) |
| D3 Processing/formulation | how engineered — **de-moralized**, population-level probabilistic signal + uncertainty | exists, must be reframed |
| D4 Additive evidence | each additive tiered by evidence + consumer explanation | **NEW (the moat)** |
| D5 Transparency/disclosure | what the label reveals vs hides — **scored** | **NEW** |
| D6 Confidence | how sure; can demote/withhold the grade | partial (`INSUFFICIENT→null`) |

Headline grade = function of D1–D5, **gated by D6**. Internally reframed as *a within-shelf ranking over
observable data — not a health verdict*. Externally: one grade + one confidence flag + drill-down (consumer
surface) vs full six-dimension graph (professional surface). Same engine, two faces.

## Guardrails (non-negotiable)
- No published score moves without owner sign-off; every change flagged; **OFF reproduces current output byte-for-byte**.
- Every new penalty/credit cites an evidence-registry entry (enforced by `bari-bsip2-scoring-governance`).
- Decisiveness preserved — never ship six numbers to a shopper.
- MVP the corpus, not the principle (classify shelf-present additives, not all E-number space).
- Frozen invariants re-verified each rescore (milk = run_004; snk ceiling 70/B; bread provenance).

## Lean wave sequence (revised after token/time-efficiency review)
Cheap, unfalsifiable honesty ships first; the expensive maintenance-heavy library is gated on proven demand.

| Wave | Scope | Owners | Score movement |
|---|---|---|---|
| **W0** Foundation | Six-dimension contract + scoring-philosophy reframe (doc) | Nutrition (lead) + Product | none |
| **W1** Cheap honesty | **D5** transparency axis + **D6** confidence load-bearing | Nutrition (rules) · Data (detector) · Frontend (presentation) | gated |
| **W1.5** Protein-quality signal | DIAAS source table → engine signal, disclosure-gated | Research (table) · Nutrition · Data | gated |
| **W2** Additive PROTOTYPE | ~20 shelf-frequent additives, 1 pilot category, consumer panel, **instrument engagement** | Research (evidence) · Nutrition (tiers) · Content (He) · Frontend+Design (panel) · Data | none (candidate) |
| **— GATE —** | **Do consumers engage the additive panel?** (directional: 5–8 moderated sessions + 15-sec test + instrumentation) | Product + Design | — |
| **W3** Scale additives *(only if W2 validates)* | Full D4 library + EFSA/JECFA/FDA wiring + maintenance protocol | Research · Nutrition · Product (cadence gate) | gated |
| **W4** Reframe & separate | De-moralize **D3** + internal six-dimension emit + consumer/professional surfaces (view-model) | Nutrition · Data · Frontend · Design | gated |
| **W5** Publish & polish | Public methodology page + NDA materials packet + consumer additive UI polish | Content · Nutrition · Product · Marketing | none |
| **Cross-cutting** | Regression, flag-OFF byte-identity, invariant re-verification, registry health + close gates | QA · CC | — |

## Progress
- **W0 COMPLETE 2026-06-04** — 179A scoping · 179B contract · 179C Product co-sign + owner ratification (DEC-006). Six-dimension contract + philosophy reframe ratified.
- **W1 BUILD PHASE COMPLETE 2026-06-04** — 179D D5/D6 rule spec · 179E Product number co-sign · 179F EV-035…039 (BSIP2 registry, adopted-behind-flag) · 179G engine build behind `BARI_GLASSBOX_D5D6` (OFF byte-identical / ON zero-promotion) · 179H independent QA PASS · 179I consumer preview (calm `ניתוח חלקי` / `לא נוקד` states, behind FE flag, no live JSON touched). **D5/D6 are built, independently proven, and visually previewable — nothing live.**
- **W1+W1.5 LIVE 2026-06-04** (owner go-live directive) — feature-flags.ts flipped to default ON; rollback = set `NEXT_PUBLIC_GLASSBOX_D5D6=off` in hosting env. Code was already on origin/master (commit `b6f2015`). Go-live prep all closed: 179J numbers LOCKED + WARN-2 accepted · 179K Hebrew copy · 179L P3 spec reconcile + final number co-sign · 179M Data wired glassBox into hummus_frontend_v4 + maadanim_frontend_v2 · 179N Frontend integration · 179O final QA PASS. W1.5 DIAAS engine detector (BARI_GLASSBOX_W15) is live in engine code; score credits apply on next category rescore; 0 Rule B disclosure-gap fires in current pilot JSONs (no JSON regeneration needed). Visible effect: vegetable-spreads pepper-spread → ניתוח חלקי; auto-flags any future under-disclosing displayed product; no-op on curated hummus/maadanim (gated items filtered out — the finding that D5/D6's value lands on broad shelves).
- **W1.5 + W2 research COMPLETE 2026-06-04** — TASK-179P (CLOSED: DIAAS table + EV-040 + detect_diaas_signal() in engine, BARI_GLASSBOX_W15 OFF, QA 342-product PASS, Product D7 co-sign on +3) · TASK-179Q (CLOSED: 20 additive dossiers, 6/6/4/3/1/0 tier distribution, Nutrition + Product D7 co-signed, MVP = hummus+maadanim) · TASK-179R (CLOSED: engagement gate locked — 5/8 sessions + 8/12 comp + 20% live rate, all-three-must-pass). **W1+W1.5 go live together on owner flag flip (NEXT_PUBLIC_GLASSBOX_D5D6=on + BARI_GLASSBOX_W15=on).** W2 prototype build (additive panel component + engine D4 wire) is next wave — gates cleared.
- **W2 BUILD PHASE OPENED 2026-06-04** — TASK-179S (Data: D4 engine wire behind BARI_GLASSBOX_W2 flag, additive lookup table in constants.py, detect_additives_d4(), OFF byte-identity verify script) · TASK-179T (Frontend+Design: AdditivePanel component, 6 instrumentation events, mobile QA, gated on GLASSBOX_D5D6_ON) · TASK-179U (Content: Hebrew additive copy sign-off, w2_additive_copy_v1.md, 20 finalized lines) — all three IN_PROGRESS, parallel. TASK-179V (QA: 4-check gate — OFF byte-identity + engine ON sample + frontend visual + instrumentation) — IN_PROGRESS, depends on S+T+U. W2 ships when TASK-179V PASS returns.

Pilot categories (proposed): **hummus + maadanim** (cleanest — re-scored, EV-029-fixed). Owner to confirm.

## Data substrate
Already wired (TASK-170): OFF, PubChem, DSLD, literature (PubMed/EuropePMC/OpenAlex/ClinicalTrials),
il_gov_data, Tzameret. New wiring needed: **USDA FoodData Central** (amino acids / protein quality),
**EFSA OpenFoodTox + JECFA + FDA** additive evaluations (bulk-import-and-curate, not live-per-product),
**Cochrane** (systematic-review tier). Israeli MoH red-label thresholds = local authoritative anchor.

## Owners at a glance
Nutrition (engine methodology, six-dim contract, D1/D3/D4-tiers/D5-rules/D6-logic) · Research (additive
dossiers, DIAAS table, EFSA/JECFA, nutrient frameworks, maintenance) · Data (detectors, extraction, dark
re-derivation, frontend JSON) · Frontend (view-model, two surfaces, additive UI, confidence presentation) ·
Design (additive visual, confidence hierarchy, consumer/professional split) · Content (Hebrew additive
explanations, methodology copy) · Product (gates, MVP scope, maintenance-cadence gate, sign-off) · QA
(regression, flag-OFF byte-identity, invariant re-verification) · CC (registry, close gates, drift) ·
Marketing (methodology positioning, W5+).

## Sub-tasks
- **TASK-179A** (Research, IN_PROGRESS) — engine-enrichment reference frameworks scoping dossier
  (DIAAS protein-source table + additive prototype set + nutrient-interpretation framework registry +
  source/API leverage map). Feeds W1.5/W2/W3. Suggestion-stage; informs initiation. *No score movement.*
- Wave execution sub-tasks (TASK-179B…) created when the owner initiates each wave.

## Governance
Nutrition + Product co-sign on any rule that affects a grade; evidence registry entry per rule; flag-OFF
byte-identity proven by QA; `roadmap_impact: true` → CC close-gate applies. Nothing ships without owner go.
