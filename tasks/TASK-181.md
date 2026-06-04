---
id: TASK-181
title: "Glass Box — Evidence-Aware Engine Evolution (program-of-record; continues TASK-179)"
owner: nutrition-agent
status: IN_PROGRESS
priority: HIGH
created_at: 2026-06-04
depends_on: []
supersedes: TASK-179
blocks: []
category_id: null
roadmap_impact: true
work_type: objective
summary: >
  Glass Box program-of-record, promoted 2026-06-04 to succeed TASK-179 (CLOSED — W0–W2 delivered:
  six-dimension contract, D5/D6 transparency+confidence LIVE, W1.5 DIAAS signal, W2 additive prototype
  + panel LIVE on hummus/maadanim). This umbrella carries the program forward: W3 (current — scale the
  D4 additive library) · W4 (D3 de-moralization, spec ready) · W5 (publish methodology + NDA packet).
  Current wave W3 expands the D4 library from the 24-row prototype to the full shelf-frequent set,
  bulk-imports + curates EFSA/JECFA/FDA evaluations, tiers each additive, and stands up a
  maintenance-cadence protocol (the named dominant risk). ANNOTATE-ONLY: D4 does NOT enter the headline
  grade; OFF = byte-identical; score-integration is a separate future owner-gated decision
  (frozen-invariant tripwire). W3 children: 181A Research · 181B Nutrition tiers · 181C Product
  maintenance gate · 181D Data wire. W2 demand gate was bypassed by owner override (see Provenance).
---

# TASK-181 — Glass Box: Evidence-Aware Engine Evolution (program-of-record)

**Promoted to program-of-record 2026-06-04**, continuing **TASK-179** (CLOSED — W0–W2 delivered).
TASK-179's A–Z sub-letters were exhausted; this umbrella succeeds it and carries the remaining waves.
Origin, six-dimension contract, and W0–W2 delivery history live in TASK-179 + `01_framework/glass_box/`.

## Wave status
- **W0–W2 — DELIVERED** (under TASK-179, CLOSED): six-dimension contract (`six_dimension_contract_v1.md`,
  DEC-006) · D5 transparency + D6 confidence LIVE (`BARI_GLASSBOX_D5D6`) · W1.5 DIAAS signal
  (`BARI_GLASSBOX_W15`) · W2 additive prototype (20 dossiers) + AdditivePanel LIVE on hummus + maadanim.
- **W3 — CURRENT (this umbrella):** scale the D4 additive library — 181A/B/C/D below.
- **W4 — READY:** D3 de-moralization. Spec complete + Product D7 co-signed (`d3_demoralization_spec_v1.md`,
  authored under TASK-179Z); draft EV-042 pending filing at W4 open. Opens on owner go.
- **W5 — BACKLOG:** publish public methodology page + NDA materials packet + consumer additive UI polish.

## Provenance — the W2 demand gate was bypassed
W3 was designed (per TASK-179 umbrella + `glass_box_engine_program_task179` memory) as the
**expensive, maintenance-heavy bet, gated on proven consumer demand**. The W2 engagement gate
(`TASK-179X`) was **closed by owner override on 2026-06-04 without engagement data** — no moderated
sessions were run, none of the three thresholds (5/8 unprompted opens · 8/12 comprehension · 20%
live panel-open rate) were measured. W3 therefore proceeds on **owner product judgment, not measured
engagement**. This is recorded so the decision to scale carries its full context.

## Scope (annotate-only)
1. **Expand the D4 library** from the 24-row prototype (`additive_prototype_set_v1.md`) to the full
   set of additives observed on the displayed Israeli shelves. **Classify shelf-present additives,
   not the full E-number space** (standing guardrail).
2. **Wire evidence sources** — bulk-import + curate EFSA OpenFoodTox, JECFA, FDA additive evaluations
   (import-and-curate, not live-per-product).
3. **Tier** each additive on the 6-tier evidence model; file evidence-registry entries.
4. **Maintenance-cadence protocol** + Product go/no-go gate — the program's **named dominant risk**.

## Hard boundary — no score movement in W3
D4 **does not enter the headline grade** in W3. This stays **annotate-only / candidate**: OFF =
byte-identical; published `score`/`grade`/`gate`/`glassBox` fields are untouched. Letting additives
move the grade is a **separate, future, owner-gated decision** (frozen-invariant tripwire #1 — it
re-scores every pilot category and needs explicit owner sign-off). Do not fold score-integration
into this wave.

## Sub-tasks
- **TASK-181A** (Research, **CLOSED 2026-06-04**) — `additive_library_expanded_v1.md`: 36 additives (20 carried + 16 new), EFSA/JECFA/FDA evidence, 9 EVIDENCE-GAPs, no tiers. Flagged: displayed bread shelf has 0 additives; EFSA/JECFA numeric-ADI wiring gap → 181C.
- **TASK-181B** (Nutrition, **CLOSED 2026-06-04**) — `additive_tiered_library_v1.md` + EV-043: 36 additives tiered 19/7/5/3/1/0/1. Product D7 CO-SIGNED. Annotate-only.
- **TASK-181C** (Product, **CLOSED 2026-06-04**) — `additive_library_maintenance_protocol_v1.md`: cadence + go/no-go FREEZE gate + demand-revisit checkpoint; EFSA-import DEFERred; carried the 181B co-sign.
- **TASK-181D** (Data, **CLOSED 2026-06-04**) — detector 20→35 keys (36 additives); pilot JSONs regenerated (hummus 56/64 · maadanim 74/84 · bread 17/24); OFF 0-diff + 0 score/grade deltas; matcher digit-boundary guard added (no-invent).
- **TASK-181E** (Content, **IN_PROGRESS** — owner directive: all 14) — author Hebrew `explanation_he` for the 14 displayed-shelf additives 181D wired without copy (priority E960 steviol + E141); then a small Data re-wire injects them (annotate-only, OFF byte-identical).

## W3 status
Build complete: 181A (Research) · 181B (Nutrition tiers) · 181C (Product maintenance) · 181D (Data wire) all CLOSED. **One completeness task open — 181E (Hebrew copy for 14 additives + re-wire).** W3 closes when 181E lands; then assess TASK-181 program for next wave (W4 D3 de-moralization — spec ready).

## W3 end condition
W3 closes when 181A–181D are all CLOSED and the maintenance protocol (181C) is signed. Score-integration,
if pursued, opens as a separate owner-gated task — not part of W3.

## Guardrails
Every tier cites an evidence-registry entry (`bari-bsip2-scoring-governance`). Nutrition + Product
co-sign tiers. OFF byte-identity proven by QA. `roadmap_impact: true` → CC close-gate applies.
Frozen invariants (milk run_005_headpin / snack 70/B / bread provenance) untouched. Nothing ships without owner go.
