# Orchestration Model v1 — direct dispatch

**Status:** active (updated 2026-06-10 — CC layer removed). **Scope:** how the main chat session
runs work as the orchestrator, so the user stops pasting prompts and the main context stays lean.

## The roles (concrete)

- **Main chat session = the Orchestrator.** It is the only place that can spawn agents
  (subagents cannot spawn other subagents — no nested agents). It classifies, dispatches,
  verifies, and closes work.
- **Domain agents** (`data-agent`, `frontend-agent`, `qa-agent`, …) = workers. Each runs
  in **its own context window**; only its result summary returns to the main chat.
- **Registry** (`C:\Bari\tasks\`) + **memory** = durable state. They survive across chats,
  so a fresh chat reconstructs everything.

## The loop (what happens when you say "go")

1. **Classify**: Conversation Work → handle inline. Registry Work → open/locate the TASK.
2. **Dispatch directly**: spawn the owning agent(s) via the Agent tool with the
   **5-part delegation spec** (objective / boundaries / inputs / deliverable+return-format / guards).
   Independent work → spawn in **parallel**; long work → **background**. *No prompts handed to the user to paste.*
3. **Collect**: each agent returns a summary to the main chat (its heavy work stayed in its own
   context — the main chat does not absorb it).
4. **Verify before closing**: read each return-block claim against the actual artifact (file:line /
   real number, not prose). Hunt for unstated side-effects. Risk-classify high-stakes work.
5. **Close or escalate**: verified + pass/fail → set `status: CLOSED` with `close_reason` citing
   evidence; genuine judgement call → escalate to the user/Product.
6. **Open the next**: any `blocks`/`depends_on` gap the close unlocks → open + dispatch.
7. **Report**: decision map + what closed + what's next.

## Context hygiene (the "one huge chat" problem)

- Push execution into **subagents** → their tokens stay in their context, not the main chat.
- Use **background** agents for long runs.
- Keep the main chat for **decisions**, not file dumps.
- **Start a fresh chat per phase/epoch.** The registry + memory let the orchestrator rebuild full
  state in seconds (`/roadmap`). Don't nurse one eternal session.

## What the user types

- `/roadmap` — full decision map on demand (reads registry directly).
- `/cc <question or op>` — ad-hoc registry query / status / close / open.
- "go" / "do X" — the orchestrator dispatches the right agents directly; the user does not write
  or paste agent prompts.
