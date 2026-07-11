# Lesson-Resolution Contract v1 — embedded `lesson_*` frontmatter on `TASK-NNN` (TASK-604)

**Status:** active (2026-07-11). **Source:** STF verdict memo
`01_framework/governance/stf_memos/2026-07-11_lesson-resolution-mechanism.md` (Fable↔Sol,
blind-converged, owner-accepted). **Enforced by:** `03_operations/validators/check_lesson_resolution.py`
(the ONE validator — invoked by both the close hook and the required CI job; single interpretation,
never divergent copies).

## Why this exists

Bari lessons currently die as passive prose (out-of-repo memory, `close_reason` text, step-6b
discipline) — they do not reliably change the system. The STF rejected a separate `LESSON-NNN`
ledger (a parallel task-management system — the exact failure class Bari's hard rules forbid) and
replaced it with a **lesson-resolution contract embedded in the originating `TASK-NNN`**. This is
additive and reversible: flat frontmatter keys, one validator, one hook extension, one CI check.
Revert = delete. **No new record type. No `lessons/` directory. No `lessons.py` engine. No change
to the 5-state task lifecycle** (`IN_PROGRESS · BLOCKED · RETURNED · CHANGES_REQUESTED · CLOSED`).

## The contract — flat frontmatter keys (NOT nested)

`board_check.py` (`tasks/board_check.py`) is a hand-rolled line-based frontmatter parser with no
YAML library — a nested map would be mis-parsed. `check_lesson_resolution.py` parses frontmatter
the same flat, line-based way (see "Parser compatibility" below). Flat keys are also
grep-scannable across hundreds of closed task files with no parser at all.

```yaml
lesson_trigger:    failure | correction | recurrence | user_complaint | none
lesson_outcome:    immediate_fix | rule_change | implementation_task | regression_test | human_decision | not_applicable
lesson_evidence:   <pointer/citation to the failure evidence — file:line, run output, task id>
lesson_artifact:   <repo-relative tracked file path>          # used by immediate_fix / rule_change / regression_test
lesson_generated_task_id: TASK-NNN                             # used by implementation_task
lesson_validator:  <exact command/test that proves the prevention, e.g. "python 03_operations/validators/foo.py --selftest">
lesson_signature:  <stable key clustering machine-identical incidents: validator-id / error-code / test-id / subsystem+normalized-failure-class>
lesson_related:    [TASK-x, TASK-y]                             # flat inline list, same syntax as depends_on/blocks
lesson_approval_required: true|false
lesson_approval:   <owner-decision record ref, when required — e.g. a memory-file slug or decision log line>
```

Provenance on a GENERATED follow-up task (written by `tasks/new_task.py --origin-task TASK-NNN
--lesson-trigger <trigger>`):

```yaml
origin_task:   TASK-NNN     # the task this follow-up was generated FROM (reciprocal provenance)
lesson_trigger: <trigger>   # optional, on the NEW task itself
```

All keys are **optional on non-CLOSED tasks** and **only enforced at the CLOSE transition**
(`status: CLOSED`). A task with no lesson fields at all can move through IN_PROGRESS / BLOCKED /
RETURNED / CHANGES_REQUESTED freely — the gate only fires when a task is about to become CLOSED.

## What CLOSE requires

A task moving to `status: CLOSED` must carry a `lesson_trigger`. For any trigger that is **not**
`none`, exactly **one** `lesson_outcome` is required, and its referent must be **machine-verified**:

| `lesson_outcome` | Machine verification |
|---|---|
| `immediate_fix` | `lesson_artifact` is a tracked file that **exists** on disk **and** `lesson_validator` (a command) **exits 0** |
| `rule_change` | `lesson_artifact` (the changed rule/validator file) **exists**; its verification command (`lesson_validator`, or `python <artifact> --selftest` by default for `.py` files) **exits 0** |
| `implementation_task` | `lesson_generated_task_id` **exists** in `tasks/` or `tasks/closed/`, is **not self-referencing**, carries **reciprocal provenance** back to this task (the generated task's own text/frontmatter names this task's id — normally via `origin_task:`), and if that generated task is itself CLOSED it is **not closed-without-verification** (carries a non-empty `close_reason`) |
| `regression_test` | `lesson_artifact` (a tracked fixture/test) **exists**; `lesson_validator` (the exact test/regression command) **exits 0** |
| `human_decision` | `lesson_approval` names a recorded owner-decision ref, **or** `lesson_generated_task_id` points to an **open** approval task (`IN_PROGRESS`/`BLOCKED`/`RETURNED`/`CHANGES_REQUESTED`) |
| `not_applicable` | requires an owner waiver (`lesson_approval`) **or** a clean (non-failure-shaped) history — see anti-gaming below |

**Rejected, always (HARD block):**
- `lesson_trigger` missing on a CLOSED task.
- Multiple `lesson_outcome` values on one task (comma/space-separated) — exactly one.
- `lesson_evidence` missing when `lesson_trigger != none`.
- Self-reference — `lesson_generated_task_id` or any entry of `lesson_related` equal to the task's
  own `id`.
- Dangling ids — any `lesson_generated_task_id` / `lesson_related` entry that does not resolve to a
  real file under `tasks/` or `tasks/closed/`.
- A closed `implementation_task` follow-up with no `close_reason` (closed without verification).
- An unverified artifact — the named file is missing, or the named validator command exits non-zero.

## Anti-gaming — the honest residual (owner ruling)

Deterministically detecting `correction` / `user_complaint` from a transcript is not sha256-hard —
the realistic gaming move is `lesson_trigger: none`. Per the STF's adjudicated mitigation:
`none`/`not_applicable` is **allowed** (never hard-blocked on its own), but the validator emits a
**WARN (non-blocking)** when `lesson_trigger: none` sits on a task whose history is **failure-shaped**
— detected heuristically by scanning the task file's raw text for: a prior `RETURNED` /
`CHANGES_REQUESTED` status mention, `RED` / `gate-fail` language in the body, or a `retry` /
`attempt > 1` mention — **and** no `lesson_approval` (owner waiver) is present. This is an audit
signal, not a truth oracle: honesty beyond artifact-existence is a `/telemetry` §8 /
orchestrator-verify-before-close problem, not a regex problem, and the design says so rather than
implying the hook enforces truth.

## Recurrence — recomputed from the corpus, never stored

`check_lesson_resolution.py` scans closed tasks under `tasks/` and `tasks/closed/` by
`lesson_signature` **every time it runs** (at close, and in CI) — there is **no mutable counter**
anywhere (a stored counter drifts from reality; recompute cannot). `lesson_signature` is an
index/suggester, never the authority; confirmed recurrence is via `lesson_related`. When a
signature recurs across two or more CLOSED tasks and **none** of the matched tasks used a
structural outcome (`immediate_fix` / `rule_change` / `regression_test`) — i.e. every occurrence
was resolved as `human_decision` or `not_applicable` — the validator flags it **RED** (blocking,
rendered distinctly from an ordinary HARD fail): a recurring failure whose standing prevention is
documentation-only must be escalated to a validator/test, not re-waived silently.

## Enforcement — fail-open local, fail-closed CI

- **Close hook** (`.claude/hooks/guard-lesson-on-close.ps1`, wired in `.claude/settings.json`
  `PreToolUse` for `Write|Edit`) intercepts a Write/Edit to `tasks/TASK-*.md` that sets
  `status: CLOSED`, reconstructs the resulting content, and delegates to
  `check_lesson_resolution.py` against the real registry. **`exit 2` blocks the tool call.** The
  hook **fails open on any infra error** (house convention — a broken hook must never brick
  unrelated local work): missing validator, missing repo root, any PowerShell exception.
- **Required CI job** (`.github/workflows/lesson_resolution_gate.yml`) re-runs the SAME validator
  (`check_lesson_resolution.py --selftest` plus the contract check) on every `tasks/TASK-*.md`
  changed in a PR that ends up `status: CLOSED`. **This job fails closed** — it is the binding
  guarantee; without a mandatory CI check the guarantee is nominal (both STF seats: *"if CI is not
  mandatory, the guarantee does not exist"*).
- **Single interpretation.** The hook and the CI job both call
  `03_operations/validators/check_lesson_resolution.py` directly — neither re-implements the logic.
  Divergence between hook and CI is the one failure mode this design exists to make structurally
  impossible.

## Parser compatibility

`check_lesson_resolution.py` parses frontmatter with the same technique as `tasks/board_check.py`:
a line-based scan between the leading `---` markers, `key: value` split on the first `:`, and
skip-forward handling for YAML block scalars (`summary: >`) so their indented body lines are not
mis-read as keys. No YAML library. Flat inline lists (`lesson_related: [TASK-x, TASK-y]`) are
parsed the same way `new_task.py` already writes `depends_on` / `blocks`.

## Exit codes (`check_lesson_resolution.py`, house convention)

```
0  PASS  — no CLOSE-blocking violation (WARN/RED-info allowed to print, but RED is blocking — see above)
1  FAIL  — >=1 HARD or RED (recurrence) check failed; the CLOSE transition is blocked
2  USAGE — bad input / target file not found / no target given
```

## Scope note (hard constraints)

This contract does not add a new record type, lifecycle state, or engine. `lesson_outcome:
implementation_task` reuses the **ordinary** `TASK-NNN` registry — a lesson with no originating
task simply opens an action-shaped ordinary task carrying the `lesson_*` block, never a
`work_type: lesson` record (STF Appendix C). Nothing here changes published scores, scoring
philosophy, or any consumer-facing surface.
