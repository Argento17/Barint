---
id: TASK-605
title: Living-rules pilot: adapter version-parity selftest + fix router v4.2->v5 drift
owner: qa-agent
status: CLOSED
priority: HIGH
created_at: 2026-07-11
depends_on: []
blocks: []
category_id: null
lesson_trigger: correction
lesson_outcome: rule_change
lesson_evidence: AGENTS.md line 32 + 8 agent .md cited retired router v4.2; retargeted to capability_router_v5.md (v5.2); parity selftest wired to CI so drift fails closed
lesson_artifact: 03_operations/router/adapters_parity_selftest.py
lesson_validator: python 03_operations/router/adapters_parity_selftest.py --selftest
lesson_signature: router-adapter-version-drift
closed_at: 2026-07-11
close_reason: >
  Living-rules pilot per STF verdict. Delivered adapters_parity_selftest.py (mirrors dispatch.py
  --selftest-table), fixed the live v4.2 drift (AGENTS.md + 8 agent .md retargeted to
  capability_router_v5.md, zero v4.2 remaining), synced orchestrator_audit_standard §8, and wired the
  parity selftest into bari_page_gates.yml so drift fails closed. Verified on the LIVE tree: parity
  selftest exit 0 (11 adapters), drift-fixture catches reinjected v4.2, dispatch.py --selftest-table
  still passes. No shared_rules/ directory created (STF: extend the proven parity pattern, do not add a
  second SoT). This close is gated by the mechanism (rule_change outcome: adapters_parity_selftest passes).
  adapters_parity selftest (extend --selftest-table pattern) failing CI on retired version strings; fix AGENTS.md + 8 agent .md v4.2->v5 drift; sync telemetry standard section-8 + orchestration_model step-6b. Per STF memo 2026-07-11.
---

# TASK-605 — Living-rules pilot: adapter version-parity selftest + fix router v4.2->v5 drift

**Source:** STF verdict memo `01_framework/governance/stf_memos/2026-07-11_lesson-resolution-mechanism.md` (owner-accepted 2026-07-11). Living-rules pilot — the mechanism's proof-of-life on a live recurring failure (adapter drift), and the anti-duplication answer to Constraint 10 WITHOUT a new `shared_rules/` directory.

## Context
Per-vendor rule adapters have drifted: `AGENTS.md` (Codex adapter) still cites the retired **router v4.2** as canonical; all 8 `.claude/agents/*.md` cite v4.2; the telemetry standard doc `orchestrator_audit_standard_v1.md` is stale at §7 while §8 lives only in the SKILL. The STF verdict: do NOT create a `shared_rules/` directory (it adds a SoT mid-migration). Instead **extend the proven `dispatch.py --selftest-table` byte-parity pattern** so CI fails on retired version strings and adapters are pointers, not duplicated law.

## Scope (build + fix)
1. **`03_operations/router/adapters_parity_selftest.py`** with `--selftest` (exit 0/1/2 house convention): designate `01_framework/operations/capability_router_v5.md` as the canonical SoT; assert every adapter (`CLAUDE.md`, `AGENTS.md`, each `.claude/agents/*.md`) references the CURRENT router version and contains a machine-checkable pointer, NOT duplicated rule prose. **FAIL on any retired version string (`v4.2`, `bari_router_v4_2`)** anywhere in an adapter.
2. **Fix the live drift (mechanical, verify each edit):** update `AGENTS.md` and all 8 `.claude/agents/*.md` to cite Capability Router **v5.2** (the current law) and point at `capability_router_v5.md` / `dispatch.py` — replacing the `bari_router_v4_2.md` references. Do not rewrite the adapters' substance; retarget the pointer + version only.
3. **Doc-sync (mechanical):** bring `orchestrator_audit_standard_v1.md` to include §8 (self-improvement / skill-edit-proposals) so it matches the telemetry SKILL; note the sync in the return (do not invent new policy — mirror the SKILL's existing §8 text).
4. **CI wiring:** add `adapters_parity_selftest.py --selftest` to a CI workflow (extend `bari_page_gates.yml` or a small new job) so drift **fails closed** in future.

## Hard constraints
- Retarget pointers/versions ONLY — do not alter router policy or any adapter's operational substance. This is drift-repair + a parity guard, not a rewrite.
- **Leave a clean working tree + return contract; the ORCHESTRATOR commits after verify.** `.claude/agents/*.md` writes are C7 config — expect line-by-line review before accept.
- Disjoint from TASK-604's files (validator/hook/settings/lesson CI) — safe to run in parallel; stay in your worktree.

## Definition of Done (machine-checkable)
1. `python 03_operations/router/adapters_parity_selftest.py --selftest` → exit 0 AFTER the drift fix; and a fixture/demo showing it returns exit 1 when a `v4.2` string is reintroduced into any adapter.
2. `grep -rn "v4.2\|bari_router_v4_2" AGENTS.md .claude/agents/` → zero hits (show the command output).
3. `python 03_operations/router/dispatch.py --selftest-table` still passes (you did not disturb the router doc↔code parity).
4. The parity selftest is wired into a CI workflow (show the YAML diff).
5. Return contract JSON with sha256 of every changed file; clean working tree.

Return `RETURNED` (propose) — do not self-close.
