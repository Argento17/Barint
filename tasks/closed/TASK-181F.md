---
id: TASK-181F
title: Glass Box W4 Nutrition EV-042 finalize and file plus Product D7 co-sign
owner: nutrition-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-04
completed_at: 2026-06-04
depends_on: []
blocks: []
category_id: null
roadmap_impact: true
work_type: governance
cc_reviewed: 2026-06-04
close_reason: >
  CC close-readiness gate PASS (2026-06-04), owner-authorized close. EV-042 filed
  (bsip2_evidence_registry_v1.md L982–1003) binding the three D3 value-sets (confidence
  criteria, confidence_scale 1.0/0.70/0.40, population_correlation 0.05/0.15/0.40/0.75) —
  verified against the file, with a methodology_judgment row (Nutrition reviewed not
  transcribed) and a sound frozen-invariant check. BOTH D7 co-signs now complete: Nutrition
  (TASK-181F) + Product (verified in the file — co_sign flipped PENDING→CO-SIGNED, status
  updated, 2-line additive edit, EV-041/043 untouched). Governance only — no engine code,
  no score moved, no JSON. The rule is adopted on paper, behind BARI_GLASSBOX_W4 (default
  OFF). Live grade movement remains a SEPARATE owner go-live decision (tripwire #1, still
  owes the TASK-179X demand check). Closing unblocks TASK-181G (Data build).
cc_comments:
  - flag: fyi
    note: >
      CC close-readiness gate PASS (2026-06-04). EV-042 filed at
      bsip2_evidence_registry_v1.md lines 982–1003, verified against the file: all 3
      value-sets bound (confidence criteria keyed to evidence-quality-not-class;
      confidence_scale 1.0/0.70/0.40 + the 50+(base−50)×scale pull-to-neutral formula;
      population_correlation 0.05/0.15/0.40/0.75). methodology_judgment row present
      (Nutrition reviewed, not transcribed: justified low=0.40>0.0; NOVA-3=0.40 logged as
      heterogeneous central estimate). Frozen-invariant check sound (milk high-conf → no
      move; snack 70/B held by independent guardrails; D3 pull-to-neutral can't promote).
      EDPG firewall preserved. Purely additive (26 ins/0 del); EV-041/043 untouched; no
      engine/score/JSON touched. CLOSE GATED ON PRODUCT D7 CO-SIGN (Nutrition signed;
      Product PENDING) — mirrors W3 181B. TASK-181G stays BLOCKED until Product co-signs.
summary: >
  Bind the conceptual values in d3_demoralization_spec_v1.md into evidence-registry entry EV-042 and file it: confidence criteria high/medium/low (spec 2.3), confidence_scale 1.0/0.70/0.40 (2.5), population_correlation reference values 0.05/0.15/0.40/0.75 (2.4). Section 3 consumer framing is ALREADY Product-co-signed (spec lines 427-482); EV-042's numeric bindings still need Product D7 co-sign (spec line 659). Governance only - no engine code, no score move. THE UNBLOCKING GATE for 181G (Data build).
---

# TASK-181F — Glass Box W4: Nutrition — finalize + file EV-042 + Product D7 co-sign

Part of **TASK-181** (Glass Box program-of-record), Wave 4. The unblocking governance gate for 181G.

## Return block — Nutrition Agent (2026-06-04)
- **EV-042 filed:** `bsip2_evidence_registry_v1.md` lines 982–1003 (after EV-043; EV-042 was the reserved slot, no collision). Purely additive (26 ins / 0 del); EV-041/043 untouched.
- **3 value-sets bound (all KEPT from the spec draft, none changed):** (1) confidence criteria high/medium/low keyed to ingredient-evidence quality + D5-band dependency + two-signal fallback; (2) confidence_scale 1.0/0.70/0.40, formula `modifier_score = 50 + (base_score−50)×scale`; (3) population_correlation 0.05/0.15/0.40/0.75.
- **methodology_judgment:** low=0.40 (not 0.0) preserves a weak NOVA-4 prior while routing uncertainty to D6; NOVA-3=0.40 logged as a heterogeneous central estimate; confidence-keyed-to-evidence is the de-circularizing move.
- **Frozen-invariant check:** no breach risk when ON (milk high-conf → scale 1.0 → identical; snack 70/B held by independent guardrails; bread low-conf → pull-to-neutral, no new run). Live flag-flip remains a separate owner gate.
- **Co-sign:** Nutrition D7 co-signed; **Product D7 PENDING**. Governance only — no engine/score/JSON touched.

## CC close-readiness gate — PASS (2026-06-04)
EV-042 verified against the file (3 value-sets bound, methodology_judgment present, frozen-invariant check sound, EDPG firewall preserved, additive-only diff). **CLOSE GATED ON PRODUCT D7 CO-SIGN** (Nutrition signed; Product pending) — mirrors W3 181B. TASK-181G (Data build) stays BLOCKED until Product co-signs EV-042.
