---
type: stf_verdict_memo
date: 2026-07-11
slug: lesson-resolution-mechanism
chair: opus-4-8
seats:
  claude: fable-5
  gpt: gpt-5.6-sol
status: DECISION_PENDING_OWNER
supersedes_proposal: "orchestrator 'Lesson Ledger' (LESSON-NNN new record type)"
---

# STF Verdict Memo — Failure→Prevention Mechanism ("a lesson must never end as passive documentation")

## Frame (as debated)

Bari captures lessons (out-of-repo memory graph, `close_reason` prose, `orchestrate.md` step 6b,
`/telemetry` §8) but they do **not reliably change the system** — they end as passive documentation.
Goal: every meaningful failure / correction / recurrence / user-complaint must resolve to exactly one
of {immediate safe fix · rule-or-validator change · generated implementation task · regression test ·
documented human-approval decision}. Bounded by Bari hard rules: **no second source of truth · no
parallel task-management system · deterministic enforcement over prose · no auto-apply of high-risk
changes (5 tripwires) · reversible · auditable · every generated task traceable to evidence.** The
owner explicitly asked the STF to weigh IBM's **"live infrastructure"** concept (governance-as-code
that continuously asserts its own compliance).

The chair (Opus) brought a proposed **"Lesson Ledger"** — a new `LESSON-NNN` record type with its own
8-state lifecycle, JSON-Schema, `lessons.py` engine, `new_lesson.py`, two guard hooks, a `shared_rules/`
directory, and a 20-record migration (9 workstreams, ~12 files). Both SST seats reviewed it blind.

## Converged recommendation — REJECT-AND-REPLACE the ledger

**Both seats, cross-vendor and blind, independently rejected the separate `LESSON-NNN` ledger as a
parallel task system in substance** (Fable: "fiction"; Sol: "semantic fiction") — a record with an
owner, lifecycle, approvals, blockers, implementation + verification status, and closure *is*
operational work regardless of its filename prefix, and two linked state machines force reconciliation
logic (`lessons.py`) that becomes a second orchestration layer. This directly trips the **no-second-SoT
/ no-parallel-task-system** hard rule.

**Replace it with a lesson-resolution contract embedded in the originating `TASK-NNN`.** The chair
adopts this: my original ledger was over-built and the seats materially improved it.

### The design (v2, converged)

**1. Embedded resolution — flat frontmatter keys on the existing `TASK-NNN`** (flat, not a nested
object: `board_check.py` is a hand-rolled line-based parser with no YAML lib — verified — so a nested
map would be mis-parsed; flat keys are also grep-scannable across 543 closed files without a parser):

```
lesson_trigger:    failure | correction | recurrence | user_complaint | none
lesson_outcome:    immediate_fix | rule_change | implementation_task | regression_test | human_decision | not_applicable
lesson_evidence:   <pointer/citation to the failure evidence>
lesson_artifact:   <tracked file path>         # or…
lesson_generated_task_id: TASK-NNN             # when outcome = implementation_task
lesson_validator:  <named test/validator/command that proves the prevention>
lesson_signature:  <exact stable key: validator-id / error-code / test-id / subsystem+normalized-failure-class>
lesson_related:    [TASK-x, TASK-y]
lesson_approval_required: true|false
lesson_approval:   <owner-decision record ref, when required>
```

**2. One validator — `check_lesson_resolution.py --selftest` — invoked by BOTH the close hook AND CI**
(single interpretation, no hook/CI divergence). It **blocks CLOSE** unless the task carries a
`lesson_trigger` and, for any meaningful trigger, exactly one `lesson_outcome` whose referent is
**machine-verified**:
- `immediate_fix` → changed tracked file exists + named verification passes
- `rule_change` → changed rule/validator + its `--selftest` passes
- `implementation_task` → referenced `TASK-NNN` exists, is not closed-without-verification, reciprocal provenance
- `regression_test` → tracked fixture exists + named command passes (pre-fix-fails/post-fix-passes where feasible; else explicit approved exception)
- `human_decision` → tripwire category + recorded owner decision **or** an open approval task
- `not_applicable` → deterministic classifier sees no trigger **or** an owner waiver is recorded

Rejects: multiple outcomes, missing evidence, self-reference, dangling IDs, closed follow-ups lacking
verification. **This is the teeth** — field-existence ("`none — justification`") was rejected by both
seats as gameable; the check asserts the *referenced artifact/task exists and the named verification
passes*, which is the strongest property a deterministic check can honestly assert.

**3. Fail-open local, fail-closed CI.** The hook may fail open on infra error (a broken hook must never
brick unrelated local work — house convention kept) but a **required, protected CI job runs the same
validator and fails closed before merge**. Both seats: *"if CI is not mandatory, the guarantee does not
exist."*

**4. Auto-apply boundary — structurally-additive only.** Auto-apply is allowed ONLY for operations
whose safety is *structural*: create a draft `TASK-NNN`; add/update provenance fields; generate a
regression fixture from already-captured machine data; update a derived index; formatting/schema
normalization; update an exact version pointer whose canonical value is machine-derived + parity-tested.
**Never** auto-merge instructions, validation meaning, policy, owner-visible text, routing, scoring,
nutrition, claims, architecture, data models, or release behavior — that is Bari's exact historical
failure class (unreviewed automated output; baseline-copy ×98; inline-Opus copy). "Auto-applied" means
a reversible branch/patch, **not** merged to the protected branch. Review line: mechanical → CI +
code-owner; semantic → human/SST; 5 tripwires → owner.

**5. Recurrence — recomputed from the corpus, never stored.** The validator scans closed tasks by
`lesson_signature` at close and in CI; exact stable keys cluster machine-identical incidents. The
signature is an **index/suggester, never the authority**; confirmed recurrence is via `lesson_related`.
A recurrence whose standing prevention was documentation-only is flagged **RED** (forces escalation to a
validator/test). No mutable counters anywhere (a stored counter drifts from reality; recompute cannot).

**6. Living rules — no `shared_rules/` directory.** Extend the proven `dispatch.py --selftest-table`
byte-parity pattern instead: designate the canonical router/rules doc as the SoT it already is, make
adapters carry machine-checkable pointers, and **fail CI on retired version strings (`v4.2`)**. Fix the
**live** `AGENTS.md` + 8 agent-`.md` v4.2→v5 drift **now** as the pilot — it is a verified live bug and
the mechanism's proof-of-life. A Gemini adapter only after its pointer contract is defined. A new
directory is justified later only if it *replaces and deletes* the current canonical sources in one
migration.

**7. IBM "live infrastructure" — self-MONITOR yes, self-HEAL no (both seats).** Adopt continuous CI
assertion of a short invariant set: (a) every closed task has exactly one valid lesson outcome; (b)
every generated follow-up task exists + points back to evidence; (c) every claimed prevention names a
passing validator/test + an existing artifact; (d) every tripwire change has the required approval; (e)
no task references missing/contradictory records; (f) canonical rule versions match every adapter; (g)
the checker's own fixture suite rejects malformed examples. **No daemon, no self-healing ledger, no
autonomous semantic repair** — "healing" = open a traceable repair task or a reversible mechanical
patch; never silently rewrite governance. That is governance-as-code: rules executable, violations
observable, remediation enters the authoritative task system.

### MVP scope (both seats: ~3 files + CI wiring; migration deferred)

| Original workstream | Verdict |
|---|---|
| Separate `LESSON-NNN` record type + `lessons/` dir | **CUT** — embed resolution in `TASK-NNN` |
| `lessons.py` engine + `new_lesson.py` | **CUT** — extend `new_task.py` for provenance only |
| 8-state lesson lifecycle | **CUT** — reuse the 5-state task lifecycle; resolution is a typed *closure contract* |
| Schema | **KEEP, reduced** — the flat `lesson_*` contract, asserted by the validator |
| Closure enforcement (2 hooks) | **KEEP, merged** — one validator, close hook + **mandatory fail-closed CI** |
| Verification/regression proof | **KEEP, pragmatic** — named executable verification; pre-fix repro where feasible |
| Auto-apply table | **KEEP, narrowed** — structurally-additive only (above) |
| Recurrence signature-hash | **DEFER** — exact stable keys + `lesson_related` now; assisted clustering later |
| `shared_rules/` + full adapter migration | **DEFER** — extend parity selftest; **fix v4.2 drift now** (pilot) |
| Migration (20 memories / 542 tasks) | **DEFER** — pilot on new closures + ~5 known costly failures; memory = evidence input, not bulk import |

**Deliverables to register on owner acceptance:** (1) the `lesson_*` frontmatter contract +
`new_task.py` provenance flags; (2) `check_lesson_resolution.py --selftest`; (3) close-hook + required
CI wiring; (4) living-rules pilot = adapter version-parity selftest + the v4.2→v5 drift fix; (5) a small
CI invariant/report job (live-infrastructure monitor). All additive, reversible, internal (no
consumer-facing surface), not a tripwire.

## Honest residual (the one soft spot, named by both seats)

The `lesson_trigger` field is the softest point: deterministically detecting `correction` /
`user_complaint` from a transcript is not sha256-hard, so the realistic gaming move is `trigger: none`.
Both seats named **compliance theater** as the top risk and this is where it lives. Mitigation (chair's
adjudication, from Fable's amendment): allow `not_applicable`/`none` only with an owner-waiver path, and
make CI **WARN** when `trigger: none` sits on a task whose history is failure-shaped (RETURNED history,
RED-gate mentions in the body, retry/attempt count > 1). Honesty beyond that is an audit problem
(`/telemetry` §8, orchestrator verify-before-close), not a regex problem — the design should say so
rather than imply the hook enforces truth.

## Reversibility & authority

Reversibility class: **fully reversible** (additive frontmatter keys, one validator, one hook
extension, one CI check; revert = delete). Not consumer-facing. Trips **no tripwire** — internal
governance tooling. The single genuinely new governance commitment is **a mandatory, fail-closed CI
check on task close**; without it the guarantee is nominal. STF does not implement — follow-up tasks
register only after owner acceptance.

## Owner decision points

1. **Accept reject-and-replace?** The STF (cross-vendor, blind-converged) recommends the embedded
   lesson-resolution contract over the chair's original ledger.
2. **Approve the one binding commitment** — a required, fail-closed CI job that blocks a task close /
   merge when its lesson-resolution contract is unsatisfied.
3. **Approve MVP scope** (3 files + CI wiring + v4.2 drift-fix pilot; migration deferred).
4. **Approve the trigger-softness mitigation** (owner-waiver + CI WARN heuristic) or ask for stronger.

---

## Appendix A — Fable 5 blind position (verbatim)

See `scratchpad/stf_fable_position.md`. Recommendation: ACCEPT-WITH-CHANGES — collapse ledger into
`work_type: lesson` tagged task, ~3-file MVP, auto-apply only additive tests + WARN validators, signature
= suggester, no `shared_rules/` dir, live-infra = monitor-not-heal. In round 2 **conceded** to Sol's
embedded-resolution model with three repo-grounded amendments (flat keys, recompute-not-store recurrence,
no-originating-task hosting rule).

## Appendix B — Sol 5.6 blind position (verbatim)

See `scratchpad/stf_sol_position.md`. Recommendation: REJECT-AND-REPLACE — embed a `lesson_resolution`
contract in the originating `TASK-NNN`, one validator invoked by close hook + fail-closed CI, auto-apply
structurally-additive only, signature as index not authority, no `shared_rules/` (extend parity selftest),
live-infra = short CI invariant set, no self-heal. Migration deferred.

## Appendix C — Round-2 resolution

Single live crux (tagged-task vs embedded-resolution) resolved by **Fable conceding to Sol's
embedded-resolution model**, amended with: flat `lesson_*` keys (parser compatibility); recurrence
recomputed-from-corpus never stored; lessons with no originating task open an *action-shaped* ordinary
`TASK-NNN` carrying the `lesson_*` block (not a `work_type: lesson` record). No further round warranted
(diminishing returns after a concession).
