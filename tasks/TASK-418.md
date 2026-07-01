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

## Update 2026-07-01 (later) — root cause is CORPUS POLLUTION, not simple flag drift
Diagnosis (Data Agent, verified by orchestrator) + a follow-on catch reframed this:

- **cheese (2) + cereals (1):** published scores were computed on ingredient lists polluted with
  retailer disclaimers ("אין להסתמך על הפירוט המופיע באתר" etc.) and nutrition-panel bleed ("ערכים
  תזונתיים…") COUNTED AS INGREDIENTS, which inflated the ingredient count / fired false sugar markers
  and depressed the score. TASK-405 (cheese) + TASK-412 I2 (sugar bleed, not flag-gated) already
  cleaned these engine/data-side, so the clean engine now scores them HIGHER. **Owner approved
  2026-07-01: REFRESH all 3** (cheese `3523230065467` C63.8→B68, `7290019635581` E32.8→D37; cereals
  `7290017894911` D46→C50). All upward, all from since-fixed pollution.

- **hard_cheeses:** the first fix attempt (Data Agent) "reproduced" the published 62.6/62.0 for
  `7290110320850` / `7290110323301` by RE-INSTALLING the polluted task412 corpus — literally counting
  three retailer-disclaimer lines + a bled nutrition panel as ingredients so the endemic-relief gate
  (≤6 ingredients) fails and the penalty applies. Orchestrator REJECTED and REVERTED this (git checkout
  + clean): pinning a score on re-injected known-bad data is the opposite of the clean-corpus policy.
  Correct reading: those two hard_cheeses published scores are ALSO stale/defective — clean corpus
  scores them 66.0 / 74.0 (up). `7290110324872` (A81.6→B75.6) is a genuine flag-only miss (config
  lacks `BARI_HC_DAIRY_SATFAT_V1` + `BARI_DAIRY_SAT_FAT_INFER`, both ON in v4 `_meta`) — score-neutral.

- **Scope:** 322 / 2527 bsip1 records corpus-wide carry the pollution signature. The live-published
  subset that would actually MOVE on cleaning is smaller but > 3. This is a systemic corpus-hygiene
  issue, not a handful of products. **Awaiting owner scope decision** on how wide to run clean+refresh.
