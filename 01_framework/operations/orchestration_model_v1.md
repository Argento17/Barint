# Orchestration Model v2 — registry-direct, undivided orchestrator

**Status:** active (2026-06-13; supersedes v1 of 2026-06-02). **Scope:** how the main chat runs
work as the orchestrator, so the user stops pasting prompts and the main context stays lean.

**What changed in v2.** The separate **CC agent** and the **derived command-center dashboard** are
**both eliminated** (2026-06-13). CC's two jobs were (a) keeping the derived dashboard honest vs the
registry — which disappears once there is no dashboard — and (b) verification + closing authority,
which the orchestrator already exercises. Both now live in the orchestrator, undivided. The registry
is read **directly**; nothing is generated or reconciled.

## The roles (concrete)

- **Main chat session = the Orchestrator.** The only place that can spawn agents (subagents cannot
  spawn subagents). It classifies → dispatches → **verifies** → closes/opens, and holds **undivided
  closing authority**. Run the executing loop with `/orchestrate`; the read-only decision map with
  `/roadmap`.
- **Domain agents** (`data-agent`, `frontend-agent`, `qa-agent`, …) = workers. Each runs in **its own
  context window**; only its result summary returns to the main chat. They *propose* RETURNED/BLOCKED
  in their return block — they never write CLOSED.
- **Registry** (`C:\Bari\tasks\`) + **DISPATCH_BOARD** (`tasks\DISPATCH_BOARD.md`) + **memory** =
  durable state. The registry is the single source of truth; the board is its live view; `tasks\closed\`
  is the archive. There is **no derived dashboard** — nothing to regenerate, nothing to drift.

## The loop (what happens when you say "go" / run `/orchestrate`)

1. **Read state (lean):** `tasks\DISPATCH_BOARD.md` + only the specific `TASK-NNN.md` files the move
   needs. Don't sweep the whole registry to build a picture — the board holds it.
2. **Pick the next READY move** (deps satisfied, not blocked on a decision or external capacity). THE
   ROAD on the board takes priority over the ladder.
3. **Dispatch directly:** spawn the owning agent(s) via the Agent tool / the router with the **5-part
   delegation spec**. Independent work → parallel; long work → background. *No prompts handed to the
   user to paste.*
4. **Collect:** each agent returns a summary; its heavy work stayed in its own context.
5. **Verify before close (undivided orchestrator gate):** a return is a *claim, not proof*. Check every
   claim against the artifact (file:line / real number / build / deployed-state), hunt for unstated
   side-effects, risk-classify. A return missing the return contract = CHANGES_REQUESTED.
6. **Close or escalate:** verified + pass/fail → record `CLOSED` with a `close_reason` citing evidence,
   tick the board, move the file to `tasks\closed\`. Verified-but-tradeoff (accept/reject of
   cost/scope/strategy) → route to Product / surface to the owner. go-live → `red_team_cleared` first
   (the `guard-golive-close.ps1` hook enforces it).
7. **Open the next:** any `blocks`/`depends_on` gap the close unlocks → open + dispatch.
8. **Report:** decision map + what closed + what's next.

## The one enforced gate (hooks can't spawn agents)

Hooks cannot spawn an agent or nudge the parent on `SubagentStop` (verified 2026-06-02). So
verify-before-close is an **orchestrator discipline, not a hook**: *after any tracked deliverable
returns, verify claims against artifacts before recording CLOSED.* The single deterministic backstop
that remains is `guard-golive-close.ps1` — it hard-blocks closing a `work_type: go_live` task without
`red_team_cleared`, and advises when a CLOSED task lacks a `close_reason`. (The old cc_reviewed /
roadmap_impact close gates went away with the CC agent — the orchestrator IS the reviewer now.)

## Context hygiene (the "one huge chat" problem)

- Push execution into **subagents** → their tokens stay in their context, not the main chat.
- Use **background** agents for long runs.
- Keep the main chat for **decisions**, not file dumps.
- Read the **7 KB board + specific task files**, never a big derived JSON (there isn't one anymore).
- **Start a fresh chat per phase/epoch.** The registry + board + memory let `/roadmap` rebuild full
  state in seconds. Don't nurse one eternal session.

## What the user types

- `/orchestrate [focus]` — run the executing dispatch loop (dispatch → verify → close → next).
- `/roadmap` — read-only decision map (Done · In-flight · Left + next action) off the registry.
- "go" / "do X" — the orchestrator dispatches the right agents directly and verifies; the user never
  writes or pastes agent prompts.
