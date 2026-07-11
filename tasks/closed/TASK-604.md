---
id: TASK-604
title: Lesson-resolution mechanism: embedded TASK-NNN contract + validator + fail-closed CI gate
owner: qa-agent
status: CLOSED
priority: HIGH
created_at: 2026-07-11
depends_on: []
blocks: []
category_id: null
lesson_trigger: failure
lesson_outcome: immediate_fix
lesson_evidence: STF memo 2026-07-11 accepted; 10/10 acceptance scenarios pass; stale-worktree hazard salvaged (see agent_worktree_stale_base_hazard memory + orchestrate.md worktree-stale-base rule)
lesson_artifact: 03_operations/validators/check_lesson_resolution.py
lesson_validator: python 03_operations/validators/check_lesson_resolution.py --selftest
lesson_signature: agent-worktree-stale-base
closed_at: 2026-07-11
close_reason: >
  Built the embedded lesson-resolution mechanism per the owner-accepted STF verdict. Delivered:
  the flat lesson_* contract (lesson_resolution_contract_v1.md), check_lesson_resolution.py --selftest
  (10/10 fixture matrix), guard-lesson-on-close.ps1 (fail-open local, C7-reviewed) wired in settings.json,
  the required fail-closed lesson_resolution_gate.yml CI job, and additive new_task.py --origin-task/
  --lesson-trigger flags. Verified against the LIVE tree (not the stale worktree): --selftest exit 0,
  --demo block->pass, and all 10 owner acceptance scenarios PASS. This close is itself gated by the
  mechanism (immediate_fix outcome: validator selftest passes).
  Embedded lesson_* frontmatter contract on TASK-NNN + check_lesson_resolution.py --selftest, close-hook (fail-open local) + required CI (fail-closed). Per STF memo 2026-07-11_lesson-resolution-mechanism.
---

# TASK-604 — Lesson-resolution mechanism: embedded TASK-NNN contract + validator + fail-closed CI gate

**Source:** STF verdict memo `01_framework/governance/stf_memos/2026-07-11_lesson-resolution-mechanism.md` (owner-accepted 2026-07-11). This is the failure→prevention mechanism: "a lesson must never end as passive documentation."

## Context
Bari lessons currently die as passive prose (out-of-repo memory, `close_reason` text, step-6b discipline). The STF (Fable↔Sol, blind-converged) rejected a separate `LESSON-NNN` ledger as a parallel task system and replaced it with a **lesson-resolution contract embedded in the originating `TASK-NNN`**, enforced by ONE validator invoked by both the close hook (fail-open local) and a REQUIRED CI job (fail-closed).

## Scope (build these)
1. **Lesson-resolution contract** — flat frontmatter keys on `TASK-NNN` (flat, NOT nested: `board_check.py` is a hand-rolled line parser — verified). Document the contract in `01_framework/operations/lesson_resolution_contract_v1.md`:
   - `lesson_trigger`: `failure | correction | recurrence | user_complaint | none`
   - `lesson_outcome`: `immediate_fix | rule_change | implementation_task | regression_test | human_decision | not_applicable`
   - `lesson_evidence`, `lesson_artifact` | `lesson_generated_task_id`, `lesson_validator`, `lesson_signature`, `lesson_related` (list), `lesson_approval_required`, `lesson_approval`.
2. **`03_operations/validators/check_lesson_resolution.py`** with `--selftest` (house convention: exit 0 pass / 1 hard-fail / 2 usage). Given a TASK md (or `--staged`), it BLOCKS a `status: CLOSED` transition unless:
   - a `lesson_trigger` is present; and for any non-`none` trigger, exactly ONE `lesson_outcome` whose referent is machine-verified:
     - `immediate_fix` → `lesson_artifact` is a tracked file that exists + `lesson_validator` command/test passes;
     - `rule_change` → changed rule/validator exists + its `--selftest` passes;
     - `implementation_task` → `lesson_generated_task_id` exists in `tasks/` or `tasks/closed/`, is NOT closed-without-verification, and carries reciprocal provenance back to this task;
     - `regression_test` → `lesson_artifact` fixture/test exists + `lesson_validator` command passes;
     - `human_decision` → tripwire category + a recorded owner-decision ref OR an open approval task.
   - Rejects: multiple outcomes, missing evidence, self-reference, dangling IDs, closed follow-up lacking verification.
   - **Anti-gaming (owner ruling):** `lesson_trigger: none`/`not_applicable` allowed only with `lesson_approval` (owner waiver) OR a clean history; emit a **WARN** (non-blocking) when `trigger: none` sits on a failure-shaped task (frontmatter shows prior `RETURNED`/`CHANGES_REQUESTED`, body mentions RED/gate-fail, or retry/attempt > 1).
   - **Recurrence: recomputed from the corpus, never stored.** Scan closed tasks by `lesson_signature`; report a recurrence; flag **RED** when a recurrence's standing prevention was documentation-only. No mutable counters.
3. **Close hook** — extend `.claude/hooks/guard-golive-close.ps1` (or a sibling `guard-lesson-on-close.ps1` wired the same way) to invoke the validator on a Write/Edit that sets a TASK to `status: CLOSED`. `exit 2` blocks; **fails open on infra error** (house convention). Wire in `.claude/settings.json`.
4. **Required CI job** — `.github/workflows/lesson_resolution_gate.yml` runs `check_lesson_resolution.py --selftest` + the contract check on tasks changed in the PR; **fails closed** (this is the binding guarantee — owner-approved).
5. **`tasks/new_task.py`** — add optional provenance flags (`--origin-task`, `--lesson-trigger`) so generated follow-up tasks carry reciprocal provenance. Do NOT change existing behavior/defaults.
6. **Doc-contract stubs** — propose (do not self-apply) the one-paragraph edits folding the close-contract into `orchestrate.md` step 6b + `orchestration_model_v1.md` step 6; leave them as a diff in the return for orchestrator review (governance text).

## Hard constraints
- Additive & reversible only. No change to the 5-state task lifecycle, no new record type, no `lessons/` directory, no `lessons.py` engine.
- **Leave a clean working tree + the return contract; the ORCHESTRATOR commits after C0 verify** (sandbox-git rule). Anything you write under `.claude/` will be C7-reviewed line-by-line before accept.
- Flat frontmatter keys only (parser compatibility). Cross-platform: the validator is Python; the hook is PowerShell but must delegate logic to the Python validator (single interpretation, no hook/CI divergence).

## Definition of Done (machine-checkable)
1. `python 03_operations/validators/check_lesson_resolution.py --selftest` → exit 0, with fixtures proving BOTH a well-formed resolution PASSES and each malformed case (missing trigger, dangling id, multiple outcomes, unverified artifact, gamed `none` on failure-shaped task) is REJECTED.
2. A demo: a scratch TASK md set to `CLOSED` with no valid resolution → validator exit 1 (blocked); the same task with a valid `immediate_fix`+existing artifact+passing validator → exit 0.
3. `lesson_resolution_gate.yml` present, invokes the validator, fails closed on violation (show the YAML).
4. `new_task.py` still passes its existing behavior (create a throwaway task, confirm frontmatter unchanged for the no-new-flags path); new provenance flags work.
5. Return contract JSON with sha256 of every artifact; clean working tree.

Return `RETURNED` (propose) — do not self-close.
