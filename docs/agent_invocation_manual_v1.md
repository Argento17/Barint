# Bari Agent Invocation Manual

**Version:** 1.0
**Last updated:** 2026-06-01
**Applies to:** the 9 Claude Code subagents defined in `C:\Bari\.claude\agents\`

This manual explains (1) what to do **before** you prompt so the agents exist and have their environment, and (2) **how to phrase a prompt** so an agent starts with full context instead of a blank slate.

---

## 1. The one thing to understand first

Your agents are **project-scoped Claude Code subagents**. They are just the `*.md` files in
`C:\Bari\.claude\agents\`. They only exist when Claude Code is launched **with `C:\Bari` as the
working directory**. Launch from anywhere else (your home folder, `bari-web` alone, a random
path) and the roster is empty — the agents simply won't be found.

The 9 agents:

| Agent name (use this in prompts) | Use it for |
|---|---|
| **Product Agent** | strategy, prioritization, MVP/scope, go-live calls, approvals |
| **Nutrition Agent** | scoring philosophy, BSIP logic, food-science reasoning |
| **Research Agent** | evidence gathering, sources, competitor/market research |
| **Data Agent** | running the pipeline, corpus, BSIP runs, scoring, frontend JSON |
| **Frontend Agent** | Next.js/React/Tailwind implementation in `bari-web` |
| **Design Agent** | UX, visual hierarchy, layout, design critique, drift |
| **QA Agent** | verification, regression, data integrity, route/build checks |
| **Content Agent** | Hebrew consumer copy, insight lines, methodology text |
| **Marketing Agent** | SEO, content marketing, growth, launch strategy |

---

## 2. Before you prompt — terminal / startup

### Option A — Terminal (Claude Code CLI)

```powershell
cd C:\Bari
claude
```

That's the whole setup. Launching from `C:\Bari` makes Claude Code auto-load:

- `.claude\agents\*.md` → the 9 agents become invocable
- `CLAUDE.md` → repo rules, frozen invariants, registry protocol (loaded into context)
- `.mcp.json` → the Firecrawl MCP server (already allow-listed in `settings.json`)
- `.claude\settings.json` → permissions + the Write/Edit hooks

You do **not** need a separate window for the website. `bari-web` is a subtree of `C:\Bari`,
so the Frontend Agent reaches `C:\bari\bari-web` from this same session.

### Option B — VS Code extension

Open the folder `C:\Bari` (File → Open Folder), then open the Claude panel. Same effect: the
workspace root is `C:\Bari`, so the agents and config load. Don't open just `bari-web` if you
want the full roster.

### First-run checks (once per machine)

- **Firecrawl MCP** — `settings.json` already lists it under `enabledMcpjsonServers`, so it
  starts automatically. If prompted to trust the server, approve it. Its key lives in `.mcp.json`.
- **Python venv** — operational scripts use `C:\Bari\.venv`. The Data Agent runs `python`/`pytest`
  (already in the permission allow-list). No manual activation is needed for the agent, but if you
  run scripts yourself: `.\.venv\Scripts\Activate.ps1`.
- **Verify the roster loaded** — type `/agents` in Claude Code; you should see the 9 Bari agents.

---

## 3. How agents get context (why prompt wording matters)

A subagent runs in its **own fresh context window**. It does **not** automatically inherit your
main conversation. On launch it sees:

1. Its own definition file (mission, workspace path, decision rights, hard rules, skills) — automatic.
2. The repo `CLAUDE.md` rules — available in the project.
3. **Only what you put in the prompt** — everything else from your current chat is invisible to it.

So "immediate context" = **you hand it the pointers in the prompt**: the task ID, the exact
files/folders, and the goal. The agent files are written to self-load their workspace docs once
they know what they're working on — your job is to tell them *what* and *where*.

---

## 4. How to invoke — two ways

### 4a. Explicit (recommended — predictable)

Name the agent at the start of the prompt:

> **Use the Data Agent to** regenerate the snack-bar frontend JSON from the latest BSIP2 outputs
> and copy it to `bari-web\src\data\comparisons\`. This is **TASK-XXX**.

Claude matches the words "Data Agent" to the `name:` field in the agent file and delegates.

### 4b. Automatic delegation

Just describe the work; Claude reads each agent's `description:` and picks one:

> Audit the comparison page UX on mobile and flag any Gen 1 drift.

(That routes to the Design Agent.) Reliable, but explicit naming wins when it matters.

---

## 5. The context-loaded prompt template

Use this shape so the agent starts fully oriented:

```
Use the <Agent Name>.

Task: <TASK-XXX if registry work, or "conversation work — no task"> — <one-line goal>.

Context:
- Workspace: <C:\Bari  or  C:\bari\bari-web>
- Read first: <specific files, e.g. .claude\scoring.md, the category folder,
  the relevant TASK-XXX.md in C:\Bari\tasks\>
- Constraint: <any frozen invariant that applies, e.g. "milk scores frozen at run_004">

Deliverable: <what you want back — a return block, a JSON, a critique, a PR-ready diff>.
```

### Worked examples

**Data Agent (registry work):**
> Use the Data Agent. Task: TASK-142 — re-run BSIP1 enrichment for snack_bars with the
> Nutrition-Agent-approved config. Workspace `C:\Bari`. Read `02_products\snack_bars\` and the
> task file `tasks\TASK-142.md` first. Do not self-approve scoring rules. Deliver a run record
> (run ID + config hash + artifact paths) and the return block.

**Nutrition Agent (conversation work):**
> Use the Nutrition Agent. Conversation work — no task. Read `.claude\scoring.md`. Is the
> snack-bar B ceiling (snk-001 = 70/B) still defensible if we add a protein-density signal?
> Reason it through; don't change any published score.

**Frontend Agent:**
> Use the Frontend Agent. Task: TASK-150 — fix the mobile hero spacing on the comparison page.
> Workspace `C:\bari\bari-web`. Match the Design Agent's spec; run `npm run lint` and
> `npm run build` before returning. Hand back a diff summary.

**QA Agent:**
> Use the QA Agent. Verify TASK-142 actually reached the site: compare BSIP2 trace scores to the
> JSON in `bari-web\src\data\comparisons\`, check for stale data, validate routes. Read
> `C:\Bari\tasks\TASK-142.md`. Report pass/fail only — do not fix.

---

## 6. Rules that affect invocation (from CLAUDE.md)

- **Classify first.** Quick advice / clarification / minor copy = **Conversation Work** → no TASK,
  no registry, no dashboard. Multi-step reviewed deliverables or an assigned `TASK-XXX` =
  **Registry Work** → tracked. When unsure, default to Conversation Work. Say which one in the prompt.
- **Registry is authoritative.** Any `TASK-XXX` operation consults `C:\Bari\tasks\` first. Give the
  agent the task ID so it reads the right file.
- **Only the Central Controller records `CLOSED`.** Agents *propose* `RETURNED`/`BLOCKED` in their
  return block; they don't close their own tasks.
- **Workspace boundary.** Pipeline/scoring/research/content work → `C:\Bari`. Website code →
  `C:\bari\bari-web`. The frontend JSON is the only thing that crosses (generated at root, copied to
  `bari-web\src\data\comparisons\`). Don't ask an agent to cross that line.
- **Frozen invariants** (do not let an agent override without explicit instruction): milk =
  `run_004_recalibrated` (top 85/A); snack-bar ceiling snk-001 = 70/B; bread provenance =
  `real_bread_retail_003_v1`.

---

## 7. Multi-agent flows

For a full category launch the order is fixed (see `01_framework/operations` and
`.claude/skills/agent_os_v2.md`):

```
Product Agent → Research Agent → Nutrition Agent → Product Agent (approve brief)
→ Data Agent (shelf map → corpus → BSIP0 → BSIP1) → QA Agent (gate)
→ Nutrition + Product (BSIP2 readiness) → Data Agent (frontend JSON)
→ Frontend Agent (integrate) → QA Agent (go-live verification)
```

You can either drive this step-by-step (invoke each agent in turn, feeding the previous return
block forward) or ask the Product Agent to coordinate and tell you which agent to invoke next.
Because each subagent has a clean context, **pass the prior agent's output forward in your next
prompt** — that is how the chain stays informed.

---

## 8. Quick checklist

- [ ] `cd C:\Bari` then `claude` (or open the `C:\Bari` folder in VS Code)
- [ ] `/agents` shows the 9 Bari agents
- [ ] Decide: Conversation Work or Registry Work (TASK-XXX)?
- [ ] Name the agent explicitly
- [ ] In the prompt: goal + workspace path + files to read first + constraints + deliverable
- [ ] For chained work, paste the previous agent's return block into the next prompt
