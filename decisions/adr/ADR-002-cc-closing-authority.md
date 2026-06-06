# ADR-002 — CC Agent holds closing authority, not Product Agent

**Status:** Accepted  
**Date:** 2026-06-02  
**Deciders:** owner (delegation grant), CC Agent (implementation)  
**Supersedes:** none

---

## Context

In the early operating model, closing a task (recording `CLOSED`) was an informal act — any agent or the orchestrator could update the status field. This meant closures happened on the return agent's own prose summary ("I completed X"), without independent verification that the deliverable actually existed, matched the DoD, or had no silent side effects. The result: phantom closes, closed tasks with stale or missing artifacts, and gradual erosion of registry integrity.

A separate problem: the Anthropic SDK limitation — `SubagentStop` cannot spawn new agents — means no hook can automatically invoke CC after an agent returns. The close-readiness gate must be an orchestrator discipline, not a hook.

---

## Decision

Closing authority is delegated exclusively to CC Agent, which records `CLOSED` only after its close-readiness gate passes: each return-block claim independently verified against the actual artifact (file:line / real number, not prose), silent side effects hunted, risk classified. The returning agent proposes `RETURNED`; CC closes or escalates.

---

## Reasoning chain

1. **Constraint:** Return-block prose is a claim, not proof. An agent that completed 90% of a task will write a return block indistinguishable from one that completed 100%. Trust without verification is the primary registry corruption vector.
2. **Option A — returning agent self-closes:** Fast, but no independent check. Proven failure mode (phantom closes in prior sessions).
3. **Option B — Product Agent closes:** Product holds strategy authority but not verification capability — it would need to re-read every artifact. Adds overhead without adding verification quality.
4. **Option C — CC Agent closes (this ruling):** CC's mandate is registry accuracy. Its close-readiness gate (verify, don't trust) is purpose-built for exactly this check. CC reads the artifact, not the summary. For high-stakes tasks, it also routes to a second adversarial reviewer.
5. **Ruling:** Option C. CC holds closing authority. `CLOSED` is a CC act.

---

## Consequences

**Positive:**
- Registry integrity is enforced structurally, not by convention.
- Silent side effects (a rescore that invalidates copy, a frontend change that breaks a route) are caught before the task is recorded as done.
- The `cc_reviewed` + `guard-roadmap-close.ps1` PreToolUse hook makes the gate machine-enforced for high-impact tasks.

**Negative / trade-offs:**
- Adds a verification step to every task close — small latency cost.
- CC must have enough context to verify each domain's artifacts — mitigated by the 5-part delegation spec and the GitHub artifact verification client.
- The gate is advisory (not hard-enforced by hook) for non-`roadmap_impact` tasks — primary failure mode. Mitigated by extended guard (ADR-003).

**Follow-up required:**
- [x] Wire `guard-roadmap-close.ps1` PreToolUse hook (done 2026-06-02)
- [x] Document close-readiness gate in cc-agent.md (done 2026-06-02)
- [x] Extend guard to warn on HIGH priority non-roadmap-impact closes (ADR-003, 2026-06-04)

---

## Tripwire evaluation

| Tripwire | Fired? | Note |
|---|---|---|
| 1. Frozen invariant / published scores | No | Governance process only |
| 2. Irreversible AND consumer-facing | No | Internal operating model |
| 3. Starts or kills a major program | No | |
| 4. External commitment / spend / legal | No | |
| 5. Redefines strategy / target user | No | |

---

## Reversibility

- **Door type:** two-way
- **Rollback path:** Remove `guard-roadmap-close.ps1` hook, update cc-agent.md to remove closing authority section, update CLAUDE.md lifecycle paragraph.

---

## Related

- `.claude/agents/cc-agent.md` — Close-readiness gate section
- `.claude/hooks/guard-roadmap-close.ps1` — Machine enforcement
- ADR-003 — Extended guard for HIGH priority tasks
- `01_framework/operations/orchestration_model_v1.md`
