# Decision Authority Matrix v1 — Autonomy Default

**Status:** Authoritative · **Effective:** 2026-06-04 · **Owner ruling.**
**Supersedes:** the broad escalation clause in `CLAUDE.md` §Tasks ("Genuine judgement
calls … still escalate to the human/Product") and any agent text that escalates
domain-expert calls to the owner.

---

## Purpose

Push decision-making **down** to the agents and the orchestrator so the owner makes
**extremely strategic decisions only**. This document is the single source of truth for
*who decides what*. It is referenced by `CLAUDE.md` and by every agent's **Autonomy
Mandate** section.

---

## The core rule

> **Default to autonomous action.** The owning agent (or orchestrator / CC / Product)
> decides and acts. Escalate to the owner **only** if the decision trips one of the 5
> strategic tripwires below. **If you're unsure whether a wire is tripped — it isn't.**
> Act, keep it reversible, and log it for after-the-fact review.

This inverts the old default. Previously "genuine judgement calls" escalated — a wide,
fuzzy door. Now the door is small and enumerable.

---

## The 5 strategic tripwires (escalate to owner if ANY fire)

| # | Tripwire | Why it's the owner's | Escalates | Does NOT escalate |
|---|----------|----------------------|-----------|-------------------|
| **1** | **Frozen invariant / published scores / scoring philosophy** | Constitutional — rewrites the product's truth | Re-opening milk = 85/A; lifting the snack-bar B ceiling; redesigning BSIP2 weights; changing bread provenance | Re-scoring a category *behind a flag*; a recal that **holds** the invariant; methodology drafts |
| **2** | **Irreversible AND consumer-facing** | One-way public doors define the brand | A category **go-live**; a public product claim with legal weight; brand / positioning copy going live | Any internal artifact, draft, methodology doc, or flagged/unshipped change |
| **3** | **Starts or kills a major program** | Resource & identity bets | Launching SIE; greenlighting Glass Box; sunsetting a category | Sequencing tasks *inside* an already-approved program; opening sub-tasks of an approved initiative |
| **4** | **External commitment, spend, or legal exposure** | Outward-facing, hard to retract | Partnerships; paid tools/services; money; public claims liability | Internal tooling; read-only API use; integrations already admitted |
| **5** | **Redefines strategy, target user, or what Bari *is*** | The thesis itself | "Are we Yuka or an Israeli food-intelligence platform?"; changing the target user | Executing the thesis already set |

If **no** wire fires → decide, act, make it reversible (flag / PR / draft), log it.

---

## The triage matrix — Reversibility × Blast radius

Every decision = how reversible × how wide. This maps to who owns it.

|  | **Single artifact** | **One category** | **Whole product / brand** |
|---|---|---|---|
| **Two-way door** (reversible: flag / PR / draft) | Owning agent — autonomous | Owning agent — autonomous, log | Orchestrator + CC — autonomous, log |
| **One-way door** (public, irreversible) | Orchestrator + CC — verify, then act | Product Agent — recommends → ships unless a wire fires | **★ OWNER ★** — the only always-escalate cell |

Only the **bottom-right cell** is the owner's by default. Everything else resolves below.

---

## Ownership tiers (who absorbs what)

- **Owning agent** — every expert call *inside its lane*. Design picks the metric,
  Nutrition interprets scoring behavior, Content writes the copy, Data runs the pipeline,
  QA rules pass/fail. **Recommend the single best option and implement it — never hand the
  owner an A/B menu for an expert call.**
- **Orchestrator + CC Agent** — prioritization within an approved roadmap; accept/reject of
  returned deliverables (CC's close-readiness gate); cross-agent tradeoffs that don't ship
  or move published scores. CC holds closing authority (delegated 2026-06-02).
- **Product Agent** — the mid-tier judgment that *used to* reach the owner: build/pause/cut
  within scope, rollout sequencing, MVP rationalization, cross-domain conflicts. Product is
  the owner's proxy for "important but not existential."
- **Owner** — the 5 tripwires. Nothing else.

**Routing rule:** a decision that exceeds your lane but trips **no** wire goes to
Product / Orchestrator / CC — **not** the owner.

---

## Why this is safe (autonomy is earned by existing guardrails)

Autonomy is only safe because reversibility is the default. These stay non-negotiable —
they are what makes every autonomous action recoverable:

1. **Flag-gate score/logic changes** (the `BARI_RECAL_*` pattern: OFF = byte-identical).
   Nothing public moves until a wire-1/wire-2 owner sign-off.
2. **CC close-readiness gate** stays mandatory — return-block claims verified against
   artifacts, never trusted.
3. **Everything lands in the registry + audit log** — the owner reviews *after the fact*
   instead of gating *before*.
4. **PR, never direct-to-main** on shipped surfaces — a two-way door by construction.

The owner's role shifts from *approving work* → *spot-auditing direction* + *ruling on the
5 wires*.

---

## Operating notes

- **Log, don't ask.** When you act autonomously on anything beyond Conversation Work,
  record it in the registry (task + status) so it's auditable. The dashboard derives it.
- **Surface, don't gate.** If a no-wire decision is high-judgment, act and flag it clearly
  in your summary for after-the-fact review — do not stop and wait.
- **One genuine wire → full stop.** If a wire fires, escalate with a crisp recommendation
  and the tradeoff; the owner rules.
- **Disagreement on whether a wire fired** resolves toward autonomy (it didn't), with the
  decision surfaced for review.

---

## Change log

- **v1 (2026-06-04):** Created by owner directive ("be more autonomous; owner makes
  extremely strategic decisions only"). Confirmed list = exactly the 5 tripwires.
  Wired into `CLAUDE.md` and all 10 agent files (Autonomy Mandate section).
