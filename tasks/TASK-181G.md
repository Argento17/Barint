---
id: TASK-181G
title: Glass Box W4 Data implement D3 de-moralization behind BARI_GLASSBOX_W4 OFF byte-identical
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-04
completed_at: 2026-06-04
depends_on: [TASK-181F]
blocks: []
category_id: null
roadmap_impact: true
work_type: execution
cc_reviewed: 2026-06-04
close_reason: >
  CC close-readiness gate PASS (2026-06-04), owner-authorized close. D3 reframe built behind
  BARI_GLASSBOX_W4 (default OFF). OFF byte-identity INDEPENDENTLY verified (0-diff, 342
  products, all 4 corpora) — engine behaves exactly as before with the flag off. Scope clean:
  only score_engine.py (+245) + a new verifier; constants.py frozen tables untouched; no
  published JSON touched; NOVA classifier untouched. Built to EV-042 locked values (worked
  examples match). Did NOT flip the flag, rescore, or move a published grade; ON smoke keeps
  frozen milk top at 85/A. 4 build decisions (Data-derived cap-scaling formula, NOVA-2
  note=null, D6 deduction=10pts, ON preview's 1 milk E→D boundary move) routed to 181H (QA)
  + Nutrition for sign-off. Closing unblocks 181H + 181I.
cc_comments:
  - flag: fyi
    note: >
      CC close-readiness gate PASS (2026-06-04). D3 reframe built behind BARI_GLASSBOX_W4
      (default OFF). OFF byte-identity INDEPENDENTLY verified: verify_glassbox_w4_off_identical.py
      = 0-diff across 4 corpora / 342 products. Scope clean: only score_engine.py (+245)
      changed + a new verifier; constants.py frozen tables (NOVA_PROCESSING_SCORES /
      NOVA_WFI_SCORES / NOVA_HP_WEIGHTS / DIMENSION_WEIGHTS) untouched; no published
      comparison JSON touched; NOVA classifier untouched. Built to EV-042 locked values;
      worked examples match (NOVA4 35/39.5/44, NOVA1 95/81.5/68). ON smoke confirms frozen
      milk top stays 85/A. Did NOT flip the flag, rescore, or move a published grade.
  - flag: verify
    note: >
      4 build decisions flagged FOR 181H (QA) + Nutrition sign-off — not adjudicated by CC:
      (1) cap-scaling formula Data derived (the spec left it to Data): scaled_cap =
      50+(base_cap−50)×scale → lower confidence loosens the NOVA-3/4 ceiling (68→57.2 / 87→64.8
      at low); needs direction+magnitude confirm. (2) NOVA-2 non-low emits note_he=null (no
      co-signed NOVA-2 string exists) — confirm none wanted. (3) low_confidence_nova → D6
      deduction = 10 pts (magnitude Data picked; EV-042 said "may", unspecified) — needs
      Nutrition sign-off. (4) ON preview: 1 milk grade move at the E→D boundary (34.5→35.2,
      the intended less-punitive direction); high-confidence products unchanged. Full ON
      score-impact analysis is 181H's deliverable.
summary: >
  Implement the D3 reframe per spec section 2 + EV-042: d3_processing_signal struct (2.2); confidence-scaled modifier_score = 50 + (base_score-50)*confidence_scale (2.5); confidence-scaled PROCESSING_LOAD caps (4.1); REMOVE NOVA_HP_WEIGHTS NOVA-class amplification (HP reverts to direct-observation magnitude); wire the 3 final note_he strings A/B/C + C-mobile (spec 463-480). All behind BARI_GLASSBOX_W4 (default OFF). OFF = byte-identical to the W2 baseline (0-diff golden/frozen runs). Does NOT flip the flag live - go-live is a separate owner gate.
---

# TASK-181G — Glass Box W4: Data — implement D3 de-moralization behind BARI_GLASSBOX_W4

Part of **TASK-181** (Glass Box program-of-record), Wave 4.

## Return block — Data Agent (2026-06-04)
- **Changed:** `score_engine.py` (+245) only; new verifier `verify_glassbox_w4_off_identical.py`. `constants.py` frozen tables untouched; no published JSON touched.
- **Flag:** `BARI_GLASSBOX_W4` (default OFF), same pattern as the other Glass Box flags.
- **OFF byte-identity:** 0-diff across 4 corpora / 342 products (also byte-identical to the pre-edit W2 baseline).
- **Built to EV-042:** confidence calc (evidence-quality keyed, D5 path + two-signal fallback); confidence-scaled D3 score (worked examples match 35/39.5/44, 95/81.5/68); confidence-scaled NOVA caps; NOVA_HP_WEIGHTS de-amplification; `d3_processing_signal` struct + 4 co-signed `note_he` strings verbatim; insufficient-data → confidence=low + route to D6.
- Did NOT flip the flag, rescore, or move a published grade. ON smoke: frozen milk top stays 85/A.
- **4 decisions flagged for 181H/Nutrition:** cap-scaling formula (Data-derived), NOVA-2 note=null, D6 deduction=10pts, ON preview shows 1 milk E→D boundary move (less-punitive direction).

## CC close-readiness gate — PASS (2026-06-04)
OFF byte-identity independently verified (0-diff, 342 products); scope clean (engine-only, behind flag, frozen tables + published data untouched); built to EV-042 locked values. **CLOSEABLE — held for owner go.** The 4 flagged decisions route to 181H (QA) + Nutrition. Closing unblocks 181H (QA) + 181I (Frontend).
