---
id: TASK-309
title: Hummus copy parity — carry v5 copy + schema-strip the staging page (the carry+strip pass hummus was left out of)
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-17
closed_at: 2026-06-17
depends_on: [TASK-306, TASK-308]
blocks: []
category_id: null
close_reason: >
  P162/C1-GROK, orchestrator-verified against the patched file (not face-value). VERIFIED: PENDING_COPY 1041→0;
  57 products; rich v3 fields stripped from all 57; 55/55 grade-unchanged insightLine == live v5 (carried); the 2
  grade-changed dips PRESERVED with their authored E/D copy (NOT v5 grade-C); 0 grade moves, scores frozen.
  Integrity gates PASS: G4 OFF=0, G5 score==trace 0 mismatches, G7 parity, G8 data-sanity. The G1/G2/G6 gate
  FAILs are an ARTIFACT of validating a match-live (schema-stripped) page against the v3 contract — confirmed by
  running the identical gate on cakes (already publish-ready) which fails G1/G2/G6 identically; live v5 itself has
  float scores + _product_type + no comparisonContext (exactly what v3 G1 flags). G6 sodium-causal-framing strings
  verified VERBATIM in live v5 → pre-existing/already-shipping, carried for parity, not introduced here. Stray
  bari-web hummus_frontend_v5_gates_report.md write reverted → bari-web clean. Hummus now in the identical accepted
  publish state as the other 6 shelves. NON-BLOCKING follow-up logged: pre-existing sodium-causal framing in ~2+
  live hummus insightLines + the ~14 decimal-flag false-positives = future copy-clean pass (already live, out of scope).
summary: >
  Hummus was excluded from TASK-305 copy_carryover + TASK-307 schema_strip (it was being re-curated in parallel via
  P160/P161), so its staging page (_rescore_staging/hummus_shelfrel_002/hummus_shelfrel_002_rescored.json) still has
  ~1041 PENDING_COPY: generator emitted the rich v3 schema and no live copy was carried. Fix it the same way the other
  6 shelves were fixed — carry insightLine/rowVerdict from live hummus_frontend_v5.json for the 55 grade-UNCHANGED
  products, strip the staging-only rich fields v5 lacks (bariInterpretation/bestUseCases/consumerTakeaway/
  expansion.comparisonContext/expansion.consumerExplanation), and PRESERVE Content's 2 grade-changed authored dips
  (7290106577480 C→E, 7290106577572 C→D — do NOT clobber with old v5 grade-C copy). Scores/grades/product-set frozen.
  Re-gate (G8/C10/OFF/score==trace), target 0 PENDING_COPY. Staging-only, no commit, no deploy. Dispatched P162 / C1-GROK.
---

# TASK-309 — Hummus copy parity (carry + schema-strip)

Closes the lone gap blocking the hummus shelf from joining the 6 publish-ready shelves. See `tasks/prompts/P162_hummus_copy_parity.md`.
