---
id: TASK-222C
title: "BSIP2 Phase 1 — BHA/E320 flag confirmation + synonym gap fix"
owner: orchestrator
status: CLOSED
priority: HIGH
created_at: 2026-06-09
closed_at: 2026-06-09
depends_on: [TASK-222]
blocks: []
roadmap_impact: false
cc_reviewed: true
work_type: execution
close_reason: >
  BHA/E320 prevalence scan completed across 1,357 BSIP1 products: 2 products (0.15%)
  contain BHA (both bread light with E-320 in ingredient text). Below threshold for
  a scoring sprint — treated as library/evidence update only. Fixed a taxonomy
  synonym gap: ingredient_taxonomy.py had E320/E 320 but not E-320 (hyphen form),
  so the bread light products were undetected by the existing BHA_NAMED_PENALTY=5.
  Added E-320 to BHA synonyms and E-321 to BHT synonyms (data consistency). BHA
  penalty was always structurally live at -5 on additive_quality; this task confirms
  the magnitude and fixes detection. Router regression 16/16 PASS; golden regression
  11 PASS / 1 pre-existing WARN. Evidence registry BEV-087 added.
---

# TASK-222C — BHA/E320 flag confirmation + synonym gap fix

**Part of:** TASK-222 (BSIP2 research-to-implementation). **Scope:** prevalence scan,
evidence update, and data-quality fix.

## What was done

- **Prevalence scan:** Grepped 1,357 BSIP1 product JSONs across 25 runs for BHA/E320.
  Result: 2 products (0.15%), both bread light with `E-320` in ingredients.
- **Synonym gap fix:** Added `"E-320"` to BHA synonyms and `"E-321"` to BHT synonyms
  in `ingredient_taxonomy.py` — the hyphen variant was missing.
- **DEC-004 confirmation:** The magnitude (BHA_NAMED_PENALTY=5) was always structurally
  active (unlike the zero-gated F1 identity deltas). TASK-222C confirms the value.
- **Evidence registry:** BEV-087 added (regulatory transparency flag, near-zero prevalence).
- **No scoring sprint:** Per TASK-222 decision matrix — near-zero prevalence → library update only.

## Verification

| Check | Result |
|-------|--------|
| Router regression (16 tests) | PASS |
| Golden corpus regression (12 entries) | 11 PASS, 1 WARN (pre-existing) |
| BHA detection on bread light products | Verified — `tax_bha_present=True` after synonym fix |
| E-320 detection | `resolve_additive("E-320")` → bha, is_named_concern=True |
| E-321 detection | `resolve_additive("E-321")` → bht, is_named_concern=False |

## Key files changed

- `03_operations/bsip2/proto_v0/src/ingredient_taxonomy.py` — added `"E-320"` to BHA, `"E-321"` to BHT synonyms
- `03_operations/bsip2/proto_v0/src/constants.py` — updated F4 comment block to TASK-222C activation
- `03_operations/bsip2/proto_v0/review/task_222c_corpus_diff_gate.md` — diff gate report
- `01_framework/governance/evidence_registry_v1.md` — BEV-087 added
