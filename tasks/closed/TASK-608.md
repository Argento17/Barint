---
id: TASK-608
title: Product Dossier (PD) — canonical BSIP0/1/2 spine: STF architecture review
owner: product-agent
status: CLOSED
close_reason: STF verdict memo delivered (01_framework/governance/stf_memos/2026-07-11_product-dossier-architecture.md + 3 appendix files) — 2 debate rounds, CONVERGED, zero surviving cruxes; debate produced net-new architecture (mint bari_pid / registry scope discipline / three L3 namespaces incl. publication_record). OWNER ACCEPTED 2026-07-11 ("Go from my end. good outcome" — DP-1 accept+authorize MVP; "Yes agree. derive-first. We'll revisit this later" — DP-2 not-now migration). Follow-ups registered: TASK-609 (PD-1 registry, dispatched), TASK-610 (PD-2 compiler, depends 609 + parser fix), TASK-611 (PD-3 view, depends 610). Chair wrote only the memo; STF implemented nothing.
priority: HIGH
created_at: 2026-07-11
depends_on: []
blocks: []
category_id: null
lesson_trigger: none
summary: >
  Owner-started major program (2026-07-11): one canonical Product Dossier per product, 4 layers (Identity/Raw-evidence/Derived/Checks) + 2D radar + 2-page internal inspection page, foundation for the barcode scanner. Owner amendment: encapsulates BSIP0+BSIP1+BSIP2 in one spine (huge structural shift). STF (Fable+Sol) convened to stress-test & converge architecture/boundaries/sequencing before any build; verdict memo → owner. Never implements.
---

# TASK-608 — Product Dossier (PD) — canonical BSIP0/1/2 spine: STF architecture review

## Deliverable (DONE)
STF verdict memo: `01_framework/governance/stf_memos/2026-07-11_product-dossier-architecture.md`
(+ appendix position files). Two SST seats (Fable + Sol), 2 debate rounds, CONVERGED — zero
surviving cruxes; the debate produced net-new architecture (mint `bari_pid`; registry scope
discipline; three L3 namespaces incl. `publication_record`).

## Converged verdict (one line)
Build the PD as a **deterministic compiled projection** over the existing stores (601 manifest +
replay + BSIP2 traces + served JSON), one shelf-agnostic compiler, committed baseline + `--check`;
ONE new store = an identity registry (minted `bari_pid` + alias table + barcode-state adjudication);
storage migrates into the PD contract later, field-family-by-family, behind parity gates.

## Awaiting owner (blocker)
- **DP-1:** accept architecture → authorize MVP. On accept, register:
  - PD-1 identity registry + alias table + barcode-state backfill (BUILD-HEAVY) — can start now.
  - PD-2 `build_dossiers.py` compiler v1 (L1+L2 + 3-namespace L3 + 4 checks) + committed baseline +
    `--check` CI gate (BUILD-HEAVY) — committed baseline waits on the parser fix (other session).
  - PD-3 internal Page-1 inspection view (Frontend, internal route).
- **DP-2 (non-blocking):** does the PD eventually REPLACE served JSONs as the publication source
  within ~a quarter? not-now → derive-first is correct (recommended).
