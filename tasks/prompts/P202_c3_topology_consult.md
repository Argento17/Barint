# P202 / C3 independent red-team — master⟵task-275 spine reconciliation (route: C3)

➡️ Programmatic C3 consult (advice-only, never edits/closes). Orchestrator dispatches.

---

You are an independent, outside-the-family reviewer (red-team) for the Bari project. Challenge the plan below; do NOT validate it. Be concrete and adversarial. Advice only — you do not edit files or make decisions.

## Context
Bari is a monorepo. `master` is the canonical/deploy branch (Vercel → bari.digital, deploy root `bari-web`). `task-275` is a feature branch that has unintentionally become the de-facto integration branch for the entire scoring brain.

## Finding (measured via git)
- `task-275` is **44 commits ahead** of master: the current scoring engine (**~16,071 lines in `03_operations/bsip2/proto_v0/src`**, 51 files), plus `03_operations/page_generator/` (the "spine": generate_page, rescore_all, spine_flip, copy_stage) and all category configs.
- `master` is **39 commits ahead** of task-275: the frontend "conform" work (yogurt/milk/cheese/bread comparison pages under `bari-web`).
- They have **diverged both ways** across `03_operations`, `bari-web`, and `02_products`. Neither branch is a superset.
- The **live pages were scored by task-275's engine**; master's engine is ~16K lines stale and **cannot reproduce the published scores**. `rescore_all` loads the engine from `bsip2/proto_v0/src`, so the spine cannot run from master until master's engine catches up.
- Production is live and serving from master.

## Proposed plan (challenge it)
1. Integration branch off `master`; merge `task-275` into it.
2. Conflict policy by path: `03_operations` ← take task-275 (engine/spine); `bari-web` ← take master (keep the live conforms); `02_products` ← case-by-case.
3. Verify: (a) `bari-web` build green / conforms intact; (b) spine runs / `generate_page` gates pass; (c) a live category (cheese) **reproduces** its published score under the merged engine.
4. PR → master; after review/merge, retire task-275 and prune worktrees.

## Questions (answer each, adversarially)
1. Merge `task-275 → master`, or reset/fast-forward `master` to `task-275` then re-apply the 39 frontend-conform commits? Which is safer given bidirectional divergence, and why?
2. Biggest risk: master adopting the newer engine **silently changes published scores** on live pages. How do we gate against that — what concrete check proves "live numbers unchanged (or changed only as intended)"?
3. Is the per-path conflict policy in step 2 safe? Where does "bari-web ← master, 03_operations ← task-275" bite (e.g., a frontend file that legitimately depends on engine output shape; data in 02_products produced by the new engine)?
4. Minimum verification set that proves BOTH "spine works from master" AND "live frontend unchanged"?
5. Failure modes of an ~80-commit bidirectional reconciliation on a production-serving repo that we're likely not seeing. Order-of-operations traps. Rollback plan.

Return a tight, prioritized critique: the single biggest risk first, then the rest, then a recommended safer sequence if ours is flawed.
