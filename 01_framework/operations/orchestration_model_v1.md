# Orchestration Model v1 — direct dispatch + CC gate

**Status:** active (2026-06-02). **Scope:** how the main chat session runs work as the
orchestrator, so the user stops pasting prompts and the main context stays lean.

## The roles (concrete)

- **Main chat session = the Orchestrator.** It is the only place that can spawn agents
  (subagents cannot spawn other subagents — no nested agents). It adopts CC Agent's
  controller logic: classify → dispatch → verify → close/open.
- **Domain agents** (`data-agent`, `frontend-agent`, `qa-agent`, …) = workers. Each runs
  in **its own context window**; only its result summary returns to the main chat.
- **Registry** (`C:\Bari\tasks\`) + **dashboard** (`command_center.json`) + **memory** =
  durable state. They survive across chats, so a fresh chat reconstructs everything.

## The loop (what happens when you say "go")

1. **Classify** (CC): Conversation Work → handle inline. Registry Work → open/locate the TASK.
2. **Dispatch directly** (Orchestrator): spawn the owning agent(s) via the Agent tool with the
   **5-part delegation spec** (objective / boundaries / inputs / deliverable+return-format / guards).
   Independent work → spawn in **parallel**; long work → **background**. *No prompts handed to the
   user to paste.*
3. **Collect**: each agent returns a summary to the main chat (its heavy work stayed in its own
   context — the main chat does not absorb it).
4. **CC close-readiness gate** (run after every tracked deliverable): verify each return-block claim
   against the artifact (file:line / real number, not prose), hunt for unstated side-effects,
   risk-classify.
5. **Close or escalate**: verified + pass/fail → CC records `CLOSED` with evidence; genuine
   judgement call → escalate to the user/Product. `roadmap_impact` → set `cc_reviewed` first
   (the guard enforces it).
6. **Open the next**: any `blocks`/`depends_on` gap the close unlocks → open + dispatch.
7. **Report**: decision map + what closed + what's next. Dashboard auto-refreshes (PostToolUse hook).

## Standing rule (the "CC after each agent" mechanism)

Hooks **cannot** spawn an agent or nudge the parent on `SubagentStop` (verified 2026-06-02). So this
is an **orchestrator instruction, not a hook**: *after any tracked deliverable returns, run the CC
close-readiness gate before moving on.* The dashboard `ROADMAP_REVIEW` alert + the close-guard are the
backstops that make a skipped gate visible/blocking.

## Context hygiene (the "one huge chat" problem)

- Push execution into **subagents** → their tokens stay in their context, not the main chat.
- Use **background** agents for long runs.
- Keep the main chat for **decisions**, not file dumps.
- **Start a fresh chat per phase/epoch.** The registry + dashboard + memory let CC rebuild full state
  in seconds (`/roadmap`). Don't nurse one eternal session.

## What the user types

- `/roadmap` — full decision map on demand.
- `/cc <question or op>` — ad-hoc CC query / status / close / open.
- "go" / "do X" — the orchestrator dispatches the right agents directly and runs the gate; the user
  does not write or paste agent prompts.
