# Prompt Registry — Versioning, Rollback & Approval Protocol — v1

**Task:** TASK-BARI-PROMPT-REGISTRY-CI-EVAL-V1 — Deliverable 4
**Owners:** product-agent + qa-agent
**Date:** 2026-06-10
**Status:** Proposed (pending orchestrator acceptance)
**Governs:** [`prompt_registry_v1.yaml`](prompt_registry_v1.yaml),
[`prompt_eval_dataset_v1.yaml`](prompt_eval_dataset_v1.yaml),
[`authored_vs_deterministic_copy_audit_v1.md`](authored_vs_deterministic_copy_audit_v1.md),
the D3 gates in [`evals/`](evals/).

> Scope guard: this protocol defines process only. It changes no production prompt,
> no consumer copy, no scoring/data/frontend behavior. Versioning applies to the
> *registry record* of each surface, not to retroactively editing shipped artifacts.

---

## 0. What this protocol is for

Bari has no runtime LLM API calls; LLM risk enters via (A) Agent-OS instruction
files and (B) authored copy frozen into artifacts. A "prompt change" is therefore a
change to an **instruction/spec/agent file** or to an **authored copy artifact**.
This protocol makes every such change **versioned, reviewed, and reversible** in the
registry, and ties failures to an automatic **rollback**.

---

## 1. When a surface version MUST bump

A registry surface's `version` MUST bump (and `change_reason` + `expected_effect`
recorded) whenever any of the following changes:

| # | Trigger | Example | Bump kind |
|---|---------|---------|-----------|
| 1 | **Agent instruction change** | edit to `.claude/agents/*.md` body that alters behavior | minor/major |
| 2 | **Skill / persona prompt change** | edit to `.claude/skills/**` or persona md | minor/major |
| 3 | **Authored Hebrew copy instruction change** | edit to editorial specs (insight_line_spec, assertive_writing, row_description, translation_contract) | minor/major |
| 4 | **Eval rubric change** | edit to `hebrew_content_golden_eval_v1.md` dimensions / thresholds | minor/major |
| 5 | **model_boundary change** | a surface moves authored_static_copy → agent_generated_artifact, or any → runtime_api | **major (gated)** |
| 6 | **New runtime_api LLM import** | first programmatic anthropic/openai/litellm call added | **major (gated, tripwire)** |
| 7 | **Rollback from failed eval** | reverting a candidate that failed a gate | rollback entry |

Semantic versioning: **major** = behavior/contract/boundary change or anything
gated; **minor** = wording/scope refinement within the same contract; **patch** =
typo/formatting with zero behavioral effect (still logged, no approval beyond owner).
Deterministic builder *phrase-table* edits that change golden_diff output are a
**minor** bump with a mandatory `change_reason` (the golden_diff gate will fail until
the snapshot is re-captured under that reason).

Not a bump: reading the registry, running evals, re-capturing a snapshot under an
already-approved `change_reason`.

---

## 2. Version states (lifecycle)

```
draft ──► candidate ──► production
              │             │
              │             ├──► deprecated   (retired; superseded or surface removed)
              └──────────────► rollback       (reverted to last production after a failure)
```

| State | Meaning | Eval requirement to advance |
|-------|---------|-----------------------------|
| `draft` | authored, not yet eval-ready | — |
| `candidate` | proposed change, under eval | must pass its `eval_method` gate(s) vs production baseline |
| `production` | live / authoritative record | all gates green at promotion |
| `rollback` | reverted to last production after a gate failure | rollback process (§5) executed |
| `deprecated` | retired (superseded or removed) | none; record retained as history |

Notes:
- `deprecated` is added by this protocol to the four states the registry already
  uses (`draft/candidate/production/rollback`). Existing retired surfaces currently
  carrying `status: rollback` for "removed from service" (e.g. `bari-agent-cc-deprecated`,
  ADR-004) SHOULD be migrated to `deprecated` on their next touch — `rollback` is
  reserved for "reverted after a failure," `deprecated` for "retired."
- Every `production` surface keeps `rollback_version` pointing at the prior
  `production` version so a revert target always exists.

---

## 3. Required approvals by surface type

A change reaches `production` only with the sign-offs below (owner authors; reviewers
must approve; qa-agent verifies the gate ran). Maps to `agent_owner` + `reviewer` in
the registry; expands `reviewer` to a sign-off **set** where the surface is high-risk.

| Surface type | Required approvals |
|--------------|--------------------|
| Consumer-facing Hebrew copy (T1-01..06, T2-02/03/04/05) | **content-agent + qa-agent** |
| Nutrition / scoring explanations (T1-04, T1-07, T2-06/08) | **nutrition-agent + content-agent + qa-agent** |
| Evidence extraction (T3-03 / `bari-agent-research`) | **research-agent + nutrition-agent + qa-agent** |
| Task closure / governance prompts (T3-04/10/12/13) | **product-agent + qa-agent** |
| CI / import / runtime boundary (D3 gates, model_boundary, runtime_api) | **frontend-agent + qa-agent + product-agent** |

Tripwire escalation: any change that sets `model_boundary: runtime_api` (trigger #6)
is also a **frozen-invariant-adjacent / irreversible-consumer-facing risk** — it
routes to the owner per decision-authority tripwire #2 before promotion, in addition
to the sign-off set above.

---

## 4. Rollback triggers

A `production` surface is rolled back (→ `rollback` state, revert to
`rollback_version`) when **any** gate fails attributable to that surface:

1. **Eval failure** — pairwise_judge regression crossing threshold (unsafe/unapproved
   consumer wording > 0, or judge flags a hard-dimension regression).
2. **golden_diff failure** — verified-deterministic copy drifted without an approved
   `change_reason` ([`evals/run_copy_golden_diff.py`](evals/run_copy_golden_diff.py)).
3. **CLS-06 false-close failure** — closure verifier would CLOSE an unmet-DoD task
   ([`evals/run_cls06_check.py`](evals/run_cls06_check.py)).
4. **Unregistered LLM SDK import** — anthropic/openai/litellm outside `.venv/` not
   registered as `runtime_api` ([`evals/check_llm_import_tripwire.py`](evals/check_llm_import_tripwire.py)).
5. **Consumer copy leakage** — framework terms / banned phrases / score-internal
   language reaching consumer copy (schema_validation banned-phrase check + pairwise D4).
6. **Unauthorized model_boundary change** — a `model_boundary` edit landing without
   the §3 CI/boundary approval set.

Threshold reference (from the task spec; enforcement status tracked in the registry):
schema validity < 98% = fail · score-affecting classification delta > 5% = fail ·
unsafe/unapproved consumer wording > 0 = fail · unexplained score delta > approved
tolerance = fail.

---

## 5. Rollback process

When a trigger (§4) fires:

1. **Revert the registry surface to `rollback_version`** — set `status: rollback`,
   restore the prior `production` version's fields; the shipped artifact returns to
   its last-known-good state (deterministic surfaces: re-emit from the prior builder;
   authored surfaces: restore the prior authored artifact).
2. **Restore the linked eval baseline** where applicable — re-pin `linked_eval_set`
   golden snapshots / pairwise baseline to the rolled-back version so the gate is
   green against the restored state.
3. **Document the reason** — append a rollback record: trigger, failing gate, surface
   `prompt_id`, from/to versions, date.
4. **Require owner + reviewer sign-off** — the surface's `agent_owner` and the §3
   approval set must sign off on the rollback before it is marked complete; qa-agent
   verifies the relevant gate is green post-rollback.
5. **Re-entry** — a fixed change re-enters as a new `candidate` (never edits the
   reverted `production` record in place) and must pass all gates to be re-promoted.

Rollback is **reversible-by-design and never reaches the owner** unless trigger #6
(runtime_api) is involved — it is an in-lane safety action.

---

## 6. DoD item 6 closure condition

DoD item 6 ("complete inventory produced and reconciled against the registry; no
in-scope prompt unregistered") is satisfied **only when all four hold**:

| Condition | Status (2026-06-10) |
|-----------|---------------------|
| a. Inventory ↔ registry reconciled (30/30 surfaces + 5/5 excluded; no in-scope prompt unregistered) | ✅ done (D1 + D2) |
| b. D2 provenance audit accepted (authored-vs-deterministic v1.1) | ✅ accepted |
| c. D3 CI gates present (golden_diff, CLS-06, tripwire, regression passthrough) | ✅ present & green |
| d. D4 version/rollback protocol accepted | ⏳ **pending orchestrator acceptance of this doc** |

→ **DoD item 6 becomes checkable the moment condition (d) is accepted.** Until then
it remains unchecked (one dependency outstanding: acceptance of this protocol).

---

## 7. Deferred items recorded as governance notes (NOT solved here)

Per D3, these remain open and are recorded — not fixed — in D4:

1. **snacks `limitingFactors` golden_diff** — logic is inline in
   `build_salty_snacks_frontend_v2.py::main()`. Requires a pure-function extraction
   before it can be snapshotted (cannot run the builder — writes production JSON;
   cannot refactor — production change). Tracked: dataset EXP-06 `wired_in: DEFERRED`.
2. **cereals multiretailer computed `rowVerdict`** — inline f-string in
   `build_cereals_multiretailer_frontend.py::main()`. Same extraction requirement.

Both are genuinely deterministic (so they stay `golden_diff` in intent, not
manual_review); they are simply not wirable without a future, separately-approved
builder refactor. They do **not** block this protocol.

---

## 8. Outstanding for FULL task closure (beyond D4)

DoD item 4 ("all four thresholds implemented AND enforced as the fail gate") is
**partially** met: thresholds 2 & 4 (classification / score delta) are enforced via
the existing router + scoring regression; thresholds 1 & 3 (schema validity < 98%,
unsafe wording > 0) are **defined in the dataset but their runners are not yet
implemented** — the schema_validation validator and the pairwise_judge harness for
the 33 pairwise + 4 schema examples are not built (D3 wired only the deterministic
gates). This is the remaining build before the whole task can close (recommend a
follow-on deliverable D3b / folded into the v2 coverage task). It does not block
D4 or DoD 6.
