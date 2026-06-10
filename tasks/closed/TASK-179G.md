---
id: TASK-179G
title: Glass Box W1 — build D5/D6 in the engine behind BARI_GLASSBOX_D5D6 (Data)
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-04
completed_at: 2026-06-04
cc_reviewed: 2026-06-04
depends_on: [TASK-179D, TASK-179F]
blocks: []
category_id: null
roadmap_impact: true
work_type: execution
close_reason: >
  D5/D6 built in the BSIP2 engine behind BARI_GLASSBOX_D5D6 (default OFF). CC gate verified against
  artifacts. Proof A (OFF=byte-identical) PASS — 0-diff on all 342 products (golden_milk 20 + snack_bars 53
  + hummus 69 + maadanim 200); frozen ceilings preserved (milk 85/A, snk-001 70/B). Proof B (ON pilot diff,
  hummus+maadanim) PASS — ZERO promotions; hummus 0 demote/4 null, maadanim 5 demote/32 null/163 unchanged;
  EV-036 endemic-flavoring exclusion confirmed (130/200 detected → shelf not over-demoted); withholds are
  floor failures only (mostly relabeling already-ungraded insufficient_data → לא נוקד). Numbers (−10/−20/30/60)
  remain PROPOSALS pending the post-pilot Product D7 review. Independent verification → QA (TASK-179H). No
  published score moved; no frontend touched.
cc_comments:
  - flag: verify
    text: "Spec deviation needing Nutrition blessing at the post-pilot co-sign: Data made P3 (panel-absent) TOKEN-AWARE instead of the literal '<15 chars = absent', because short clean single-ingredient Hebrew panels (e.g. אגוזי מלך = 8 chars) were wrongly read as absent → would withhold a clean whole food, contradicting the spec's own single-ingredient-protection intent. Reduced hummus withholds 7→4. OFF still byte-identical (change is inside the flag-guarded detector)."
  - flag: fyi
    text: "Byte-identity was anchored on a pre-change SELF-baseline (current engine, flag OFF) — the correct reading of 'OFF = byte-identical to today' — because published frozen traces were generated under different flags (run_004 = RECAL_P0 on; snack predates sprint1/TASK-133). QA (179H) to independently confirm, incl. milk under RECAL+GlassboxOFF = published, and the snk/bread invariants."
summary: >
  Wave 1 build: Data implements the D5 disclosure-gap detector + the D6 confidence gate
  (unconstrained · demote · withhold→null) per the rule spec (d5_d6_rule_spec_v1.md) and EV-035…039,
  wired into the BSIP2 score engine behind env flag BARI_GLASSBOX_D5D6 (default OFF). Two proofs required:
  (1) FLAG OFF = byte-identical — 0-diff on the golden corpus + the three frozen runs (milk run_004,
  snk-001=70/B, bread retail_003); this is the hard gate. (2) FLAG ON pilot diff on hummus + maadanim —
  a report proving every ON-vs-OFF delta is demote-or-null ONLY, never a promotion (Product's condition).
  Honors the spec's build cautions: live constants (CONFIDENCE_LOW_CEILING=75 / INSUFFICIENT=50), G5
  no-double-count, raw BSIP0 panels, endemic-flavoring exclusion (EV-036), single-ingredient protection,
  nutrition-bleed truncation + Hebrew normalization. No published score moves (everything behind OFF).
---

# TASK-179G — Build D5/D6 behind the flag (Data)

**Part of:** TASK-179 (Glass Box), Wave 1. **Chain:** 179D spec → 179E/179F co-sign+EV → **179G (this, build)**
→ QA (independent byte-identity + invariant re-verify + ON demote/null-only proof) → Frontend (surface flag
+ confidence state on pilot pages). Domain agent proposes RETURNED; the OFF-byte-identical + ON-pilot proofs
feed the separate D10 go-live gate (Product), they do not self-activate anything.

Spec: `01_framework/glass_box/d5_d6_rule_spec_v1.md`. Controlling evidence: EV-035…039 (BSIP2 registry,
adopted-behind-flag). Flag pattern: mirror `BARI_RECAL_P0` / `BARI_TASK144_FIXES`. OFF = byte-identical is
the hard gate; ON moves scores DOWN only (demote/null), never up — frozen invariants structurally safe.
