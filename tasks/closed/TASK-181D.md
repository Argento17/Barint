---
id: TASK-181D
title: "Glass Box W3 — Data: wire expanded library into D4 detector + regenerate pilot JSONs (annotate-only, OFF byte-identical)"
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-04
completed_at: 2026-06-04
depends_on: [TASK-181B]
blocks: []
category_id: null
roadmap_impact: true
work_type: execution
cc_reviewed: 2026-06-04
close_reason: >
  CC close-readiness gate PASS (2026-06-04), owner-authorized close. Annotate-only
  invariant INDEPENDENTLY verified: OFF byte-identity 0-diff across all 4 corpora
  (verify_glassbox_w2_off_identical.py) + per-product score/grade/gate/glassBox diff vs
  git HEAD = 0 deltas across all 3 pilot JSONs (only d4_additives changed). Detector
  extended 20->35 keys covering 36 additives (E1412/14 folded into E1422). Engine matcher
  digit-boundary guard reviewed + ACCEPTED — forced by the lookup extension to prevent a
  fabricated E141 (no-invent hard rule); ON-path only, OFF 0-diff confirms; remaining E141
  a true positive. Bread 17/24 panels via the 179Y BSIP0-raw source — display-wire only,
  0 score/grade deltas, provenance intact. Content gap (14 additives lack explanation_he)
  handed to TASK-181E (owner directive: author all 14). No score moved, no engine logic
  change beyond the necessary matcher guard, frozen invariants untouched.
cc_comments:
  - flag: fyi
    note: >
      CC close-readiness gate PASS (2026-06-04). Annotate-only invariant INDEPENDENTLY
      verified: (1) OFF byte-identity 0-diff across all 4 corpora via
      verify_glassbox_w2_off_identical.py; (2) per-product score/grade/gate/glassBox diff
      vs git HEAD = 0 deltas across all 3 pilot JSONs (only d4_additives changed). Detector
      extended 20->35 keys covering 36 additives (E1412/14 folded into E1422 per the tiered
      library). Engine matcher change reviewed + ACCEPTED: a digit-boundary guard
      (score_engine.py ~268-286) that rejects a match when the next char is a digit —
      forced by the lookup extension to stop "e141" matching inside "e1412" (would FABRICATE
      an E141, a no-invent violation); ON-path only, OFF untouched (0-diff confirms).
      Remaining E141 (מילקי טופ) is a true positive (label prints "E-141"). Bread: 17/24
      panels via the 179Y BSIP0-raw-panel source (not 181A's displayed-JSON 9) — display-wire
      only, bread_frontend_v2 score/grade deltas=0, no rescore, provenance intact.
  - flag: verify
    note: >
      CONTENT GAP -> recommend opening TASK-181E. 14 displayed-shelf additives (94 instances)
      have no explanation_he (all 16 new additives lack W2 copy; 14 surface on shelf).
      Priority copy targets: E960 steviol (dose-dependent) + E141 (unclassified) — their tier
      chips carry weight; the other 12 are tier=functional (calmest). Panel degrades
      gracefully (AdditivePanel.tsx:146 explanation_he ?? ""), so this is a completeness gap,
      not a broken-UI blocker. Data did NOT fabricate copy (no-invent governance).
summary: >
  Replace the 24-entry GLASSBOX_W2_ADDITIVES table with the full tiered library from 181B; regenerate d4_additives + explanation_he across the pilot JSONs (hummus / maadanim / bread / veg-spreads). Guardrails: behind BARI_GLASSBOX_W2 flag; OFF = byte-identical (rerun verify_glassbox_w2_off_identical.py); published score / grade / gate / glassBox fields UNMODIFIED (annotate-only — D4 does not enter the grade in W3). QA confirms 0-diff on score fields + Hebrew copy coverage before close.
---

# TASK-181D — Glass Box W3: Data — wire expanded library into D4 detector + regenerate pilot JSONs

Part of **TASK-181** (Glass Box program-of-record), Wave 3. Last build step.

## Return block — Data Agent (2026-06-04)
- Detector lookup extended **20 → 35 keys covering all 36 tiered additives** (E1412/E1414 folded into the E1422 modified-starch key per the tiered library). Each carries its EV-043 tier.
- Pilot JSON regen (only `d4_additives` changed): hummus_frontend_v4 (incl. veg-spreads) 56/64 with additives · maadanim_frontend_v2 74/84 · bread_frontend_v2 17/24 (was 0 in HEAD).
- **OFF byte-identity: PASS, 0-diff** (4 corpora). **score/grade/gate/glassBox violations: 0.**
- Engine matcher precision fix (digit-boundary guard) — forced by the lookup extension to stop `e141` matching inside `e1412` (would fabricate an E141). ON-path only; OFF untouched.
- Content gap: 14 displayed-shelf additives (94 instances) lack `explanation_he` → recommend TASK-181E. Data did not fabricate copy.
- Artifacts: `_181d_run_record.json`; engine `constants.py` + `score_engine.py`; 3 pilot JSONs.

## CC close-readiness gate — PASS (2026-06-04)
OFF 0-diff (verifier) + 0 score/grade/gate/glassBox deltas vs HEAD (independent per-product diff) + matcher guard reviewed sound (ON-path only, forced by no-invent) + remaining E141 a true positive. Annotate-only invariant holds. **CLOSEABLE — held for owner go (bundle close + commit). Content gap → TASK-181E decision pending.**
