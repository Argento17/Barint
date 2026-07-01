---
id: TASK-418
title: Repro repair: granola + hard_cheeses baselines don't reproduce (blocks de-chain activation)
owner: nutrition-agent
status: IN_PROGRESS
priority: HIGH
created_at: 2026-07-01
depends_on: []
blocks: []
category_id: null
summary: >
  De-chain activation eval (2026-07-01) found granola (2 products off +16/+20 vs committed) and hard_cheeses (matched=0 + conformance path bug 'C:\Bariari-web' + granola manifest still points v1 not v2) do NOT cleanly reproduce their published scores. Score-NEUTRAL repair (patch to committed-trace like TASK-409; fix conformance path concat; repoint granola live_manifest v1->v2). No new score move. Precondition for any future de-chain activation.
---

# TASK-418 — Repro repair: baselines don't reproduce (blocks de-chain Stage 2)

## Update 2026-07-01 (orchestrator) — scope broadened, NOT resolved
P259 fixed granola (manifest v1->v2, config) and the hard_cheeses conformance path bug; granola now
reproduces within grade (drift 2 / 0 grade moves). BUT a fresh `_reproduce_diag.py` run shows the
gap is wider than the original two categories and still open:

- **hard_cheeses** (v4, run_hc_task412_rt4_fix): 12 drift, max 12.0, **3 grade moves** — bidirectional
  (`7290110324872` A->B down; `7290110323301` C->B up 12; `7290110320850` C->B).
- **cheese** (v4): 22 drift, max 5.3, **2 grade moves** (`3523230065467` C->B; `7290019635581` E->D).
- **cereals** (v2): 2 drift, **1 grade move** (`7290017894911` D->C).

All 16 live configs carry `flags: None`, yet most categories reproduce — so it is not a blanket
missing-flags issue. Root cause per grade-mover is unknown (flag-set mismatch / corpus drift /
engine-version drift / non-engine adjustment) and must be classified as **score-neutral-fixable** vs
**requires-a-published-score-change (owner tripwire #1)**. Conformance passing had MASKED this because
conformance tests re-flow, not reproduction-to-baseline.

**This is the Phase-0 reproducible-baseline prerequisite for the whole de-chain program (D7 co-sign,
non-negotiable). TASK-419 (Stage 2) stays BLOCKED until hard_cheeses + cheese + cereals reproduce or
the owner rules on any tripwire product.** Diagnosis dispatched: P267 (read-only, C1-CURSOR).
