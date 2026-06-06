# ADR-001 — Autonomy Default: agents act, owner escalated to 5 tripwires only

**Status:** Accepted  
**Date:** 2026-06-04  
**Deciders:** owner (ruling), CC Agent (implementation)  
**Supersedes:** none (inverts the prior "genuine judgement calls escalate" default)

---

## Context

The prior operating model required agents to escalate "genuine judgement calls" to the owner — a wide, fuzzy category that in practice meant nearly every non-trivial decision paused for human approval. This created a bottleneck: the owner reviewed far more decisions than they needed to, most of which were expert calls inside a well-defined domain (UX metric choices, scoring calibration, copy framing) that any capable agent could make correctly. The result was slow iteration and owner attention spread too thin to give meaningful guidance on the decisions that actually mattered.

---

## Decision

Agents, orchestrators, CC, and Product decide and act by default. The owner is escalated to only if one of five enumerated strategic tripwires fires. If none fires, the agent acts, keeps the action reversible (flag/PR/draft), and logs it in the registry for after-the-fact review. Uncertainty about whether a tripwire fires resolves in favor of autonomy.

---

## Reasoning chain

1. **Constraint:** Owner attention is finite and most valuable on genuinely irreversible or thesis-level decisions.
2. **Option A — status quo escalation:** Every judgement call surfaces to the owner. Cost: bottleneck; expert calls are delayed and the owner provides less value on decisions they shouldn't need to make. Risk: agents lose judgment muscle.
3. **Option B — autonomy default with enumerated gates:** Agents own expert calls in their lanes. Escalate only the 5 truly strategic cases. Cost: risk of agent error on high-stakes decisions that slip through the gate. Mitigated by: CC close-readiness gate (verify before closing), flag-gate pattern (nothing public moves without a wire sign-off), registry audit trail.
4. **Tiebreaker:** The 5 tripwires are objectively enumerable (frozen invariants, irreversible+consumer-facing, major program start/kill, external commitment, thesis redefinition). Everything else has a reversible path. The risk of agent error is dominated by the cost of systematic bottleneck.
5. **Ruling:** Autonomy default (Option B). The five tripwires are the only escalation path to the owner.

---

## Consequences

**Positive:**
- Expert calls (UX metric, scoring calibration, copy framing, sequencing) resolve in the owning agent's context window — faster, less context-switching for owner.
- Owner attention concentrates on genuinely strategic decisions.
- Agents develop stronger judgment through consistent exercise of domain authority.

**Negative / trade-offs:**
- A borderline decision that should have been escalated may not be. Mitigated by: "if unsure whether a wire fires, it doesn't — act and surface for after-the-fact review."
- Requires CC close-readiness gate to remain mandatory — a skipped gate is the primary failure mode.
- Requires registry discipline — every autonomous action must be logged so the owner can audit direction without gating every step.

**Follow-up required:**
- [x] Wire Autonomy Mandate into all 10 agent files (done 2026-06-04)
- [x] Wire into CLAUDE.md (done 2026-06-04)
- [x] Publish decision_authority_matrix_v1.md (done 2026-06-04)
- [ ] Add periodic "autonomy audit" to CC scorecard to catch systematic under-escalation

---

## Tripwire evaluation

| Tripwire | Fired? | Note |
|---|---|---|
| 1. Frozen invariant / published scores | No | This is a process change, not a score change |
| 2. Irreversible AND consumer-facing | No | Internal operating model change |
| 3. Starts or kills a major program | No | Governance, not a new program |
| 4. External commitment / spend / legal | No | Internal only |
| 5. Redefines strategy / target user | No | Does not change what Bari is, only how decisions are made |

_Owner ruling was solicited as a strategic directive, not because a tripwire fired — the owner proactively reshaped the governance model._

---

## Reversibility

- **Door type:** two-way (process change, reversible by re-wiring CLAUDE.md and agent files)
- **Rollback path:** Revert CLAUDE.md "Decision authority" section to the prior escalation default; update all 10 Autonomy Mandate sections; re-issue to agents.

---

## Related

- `01_framework/governance/decision_authority_matrix_v1.md` (full law)
- All 10 `.claude/agents/*.md` Autonomy Mandate sections
- CLAUDE.md §Decision authority
