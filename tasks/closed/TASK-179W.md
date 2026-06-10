---
id: TASK-179W
title: "Glass Box W2 — EV-041: D4 evidence registry entry"
owner: nutrition-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-04
completed_at: 2026-06-04
cc_reviewed: 2026-06-04
depends_on: [TASK-179S]
blocks: []
category_id: null
roadmap_impact: true
work_type: governance
close_reason: >
  CC close-readiness gate PASS (2026-06-04). EV-041 verified at
  03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md lines 931–954.
  All 5 return-block claims independently confirmed against artifact: (1) 6-tier model
  present (line 940); (2) W2 presentation-only scope explicit (line 942); (3) W3
  demand-gate constraint explicit — "D4 does NOT enter the score formula until TASK-179X
  passes" (line 943); (4) source additive_prototype_set_v1.md + TASK-179Q D7 co-sign
  referenced (lines 941, 948); (5) BARI_GLASSBOX_W2 default OFF confirmed (lines 942,
  945, 950). Governance compliance gap closed retroactively.
summary: >
  Compliance-gap close: Nutrition writes the evidence registry entry (EV-041) covering
  the D4 tier model (6 tiers, no score movement in W2, demand-gated path to W3 scoring).
  Retroactive but required before W2 is considered fully clean per governance rule that
  evidence precedes engine code.
---

# TASK-179W — Glass Box W2: EV-041 D4 evidence registry entry

Part of TASK-179 (Glass Box), Wave 2 governance close-out.

## Why this exists

TASK-179S shipped the D4 additive-tier detector behind `BARI_GLASSBOX_W2`. The governance
rule (`03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md`) requires an
evidence registry entry to precede engine code. The entry was not filed before W2 shipped —
this task closes the compliance gap retroactively. It blocks nothing until W3 opens, but
W2 cannot be considered fully clean without it.

## Scope

Write **EV-041** in `03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md`.

Entry must cover:

1. **Dimension:** D4 additive evidence
2. **Tier model:** 6 tiers — `functional` / `likely-neutral` / `dose-dependent` / `contested` /
   `disclosure-gap` / `confirmed-negative` / (`unclassified` for no-match fallback)
3. **W2 scope:** Presentation-only. `d4_additives` array is additive to the result dict.
   No score movement, no grade change, no gate field change. OFF = byte-identical (verified
   by `verify_glassbox_w2_off_identical.py`, TASK-179S deliverable).
4. **W3 path:** Score movement is demand-gated. The engagement gate (TASK-179X) must pass
   before any D4 weight enters the headline score. This constraint is to be stated explicitly
   in the registry entry.
5. **Source:** `01_framework/glass_box/additive_prototype_set_v1.md` (20 additives, D7
   co-signed via TASK-179Q).
6. **Activation flag:** `BARI_GLASSBOX_W2` env var (default off).

## Guardrails

- Do NOT modify the tier model itself — the 20-additive prototype sheet is the source of
  truth (TASK-179Q CLOSED). This task is documentation only.
- Do NOT change any score, grade, or existing engine field.

## Deliverable

One new evidence registry entry (EV-041) in `bsip2_evidence_registry_v1.md`, referencing
`additive_prototype_set_v1.md` as the authoritative tier source and stating the W3
demand-gate constraint explicitly.

## Return block

Nutrition returns with: (a) EV-041 entry written, (b) file path + line range,
(c) explicit statement that the 6-tier model, W2 presentation-only scope, and W3
demand-gate constraint are all captured.
CC closes after verifying EV-041 is present and complete.

## Return block — Nutrition Agent (2026-06-04)

**EV-041 filed.** File: `03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md`
Lines: 931–954

Confirms:
- 6-tier model documented (`functional` / `likely-neutral` / `dose-dependent` / `contested` / `disclosure-gap` / `confirmed-negative` + `unclassified` fallback) ✓
- W2 presentation-only scope stated explicitly (`d4_additives` array additive only; no score/grade/gate field change; OFF = byte-identical per `verify_glassbox_w2_off_identical.py`) ✓
- W3 demand-gate constraint stated explicitly (score movement gated on TASK-179X engagement gate passing; D4 does not enter headline score formula until TASK-179X passes) ✓
- Source: `additive_prototype_set_v1.md` (TASK-179Q, D7 co-signed Nutrition + Product 2026-06-04) ✓
- Activation flag: `BARI_GLASSBOX_W2` (default OFF) ✓

**Status proposal: RETURNED** — ready for CC close-readiness gate.
