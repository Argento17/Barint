# Bari Command Center v2 — Architecture

**Task:** TASK-070  
**Owner:** Product Agent  
**Date:** 2026-05-31  
**Status:** SPEC — do not build until implementation_plan.md is reviewed

---

## The Problem With v1

The v1 dashboard (`command_center.json`) requires manual updates. Every time a pipeline stage completes, a task closes, or a category goes live, someone must edit the JSON file. The failure mode is not dramatic — it is quiet. Agents skip the update because the task is done and the update feels secondary. The JSON drifts. The dashboard becomes unreliable. People stop trusting it. People stop opening it.

**Evidence of drift observed on 2026-05-31:**

`hummus_frontend_v1.json` exists in `C:\bari\bari-web\src\data\comparisons\` — the dataset was deployed. The command center shows `frontend_dataset.status: NOT_BUILT`. The truth changed; the JSON did not.

This is not a process failure. It is a structural failure. Manual maintenance cannot outrun operational pace. The architecture must make drift impossible, not harder to achieve.

---

## Design Constraint

**The dashboard should derive state from Bari operations, not require Bari operations to update the dashboard.**

This sentence defines the entire architecture. Every design decision in v2 is evaluated against it.

---

## Option Evaluation

### Option A — Manual JSON (current v1)

**Mechanism:** Agents manually edit `command_center.json` at task boundaries.

**Problem:** Maintenance is a separate task with no natural trigger. It competes with actual work. It is skipped under time pressure. Over weeks, the JSON reflects a past state of the project, not the current one.

**Verdict:** Eliminated. The problem statement is this option. Do not refine it.

---

### Option B — Generated JSON from task artifacts

**Mechanism:** A generator script reads existing TASK-NNN.md files and produces `command_center.json`.

**Why this is insufficient as stated:**

TASK-029.md and TASK-032.md are prose documents. They have a loose header (`**Status:** Complete`) embedded in free text. A parser that reads these files is fragile — it depends on formatting conventions that are not enforced, produce silent failures when violated, and require a custom parser per field.

More fundamentally, current task files do not contain the data needed for the dashboard. TASK-029.md has no `owner` field in machine-readable form, no `depends_on`, no `category_id`. Parsing prose to extract these is unreliable.

Option B is correct in principle but incomplete in definition. It needs a structured task format and a derivation plan for category state. When those are added, it becomes Option C.

**Verdict:** Directionally correct. Insufficient as specified. Superceded by Option C.

---

### Option C — Task Registry + Generated Dashboard

**Mechanism:**

1. **Task registry** (`C:\Bari\tasks\TASK-NNN.md` with mandatory YAML frontmatter) — structured, machine-parseable task metadata embedded in existing task files.
2. **Decision registry** (`C:\Bari\decisions\decisions.json`) — append-only JSON array of decisions.
3. **Category state** — auto-derived by the generator from pipeline filesystem indicators. No manual maintenance.
4. **Website state** — auto-derived by the generator from the Next.js source files. No manual maintenance.
5. **Generator** (`C:\Bari\05_command_center\generate_dashboard.py`) — reads all of the above and produces `command_center.json`. Runs in seconds. Triggered at session start and task completion.
6. **HTML renderer** — unchanged from v1.1. It reads `command_center.json`. The renderer does not care how the JSON was produced.

**Why this works:**

- Category state cannot drift because it is not stored — it is derived. The moment a BSIP2 `AUTHORITATIVE.md` file is created, the next generator run reflects it. No agent needs to remember to update anything.
- Task state requires one additional discipline: task files must have YAML frontmatter. This is a small, bounded, checkable requirement. When a task is created, the frontmatter is written once. When the status changes, one field is updated.
- Decision state requires appending to a registry when a decision is made. This is already implicit in the decision workflow — decisions are currently recorded in task return messages. The registry formalizes an existing behavior.

**Verdict: Recommended.**

---

## Architecture Diagram

```
AUTHORITATIVE SOURCES (never command_center.json)
│
├── C:\Bari\02_products\{category}\           ← pipeline indicators
│     ├── reports\bsip0_gate_result_*.md       ← BSIP0 status
│     ├── canonical_bsip1\*.json               ← BSIP1 status + count
│     ├── intelligence_bsip2\run_*\            ← BSIP2 status
│     │     ├── AUTHORITATIVE.md               ← authoritative marker
│     │     └── INVALID.md                     ← invalid marker
│     └── qa\reports\qa_report_*.md            ← QA status
│
├── C:\bari\bari-web\src\                      ← website state
│     ├── data\comparisons\{cat}_*.json        ← dataset deployed?
│     ├── lib\comparisons\registry\types.ts    ← category registered?
│     └── app\hashvaot\{category}\page.tsx     ← route exists?
│
├── C:\Bari\tasks\TASK-NNN.md                  ← task registry
│     └── YAML frontmatter (machine-readable)
│
└── C:\Bari\decisions\decisions.json           ← decision registry
      └── append-only array

          ↓ generate_dashboard.py (runs on demand)

      command_center.json  (derived, not maintained)

          ↓ fetch('./command_center.json')

      command_center.html  (unchanged from v1.1)
```

---

## What Changes, What Stays

### What changes

| Component | v1 | v2 |
|---|---|---|
| `command_center.json` | Manually maintained | Generated by script |
| Task data source | Hardcoded in JSON | TASK-NNN.md YAML frontmatter |
| Category state source | Hardcoded in JSON | Filesystem scan |
| Website state source | Hardcoded in JSON | Next.js source scan |
| Decision source | Hardcoded in JSON | `decisions.json` append-only registry |
| Alert computation | Hardcoded in JSON | Auto-computed by generator |
| Update trigger | "remember to update" | Run `python generate_dashboard.py` |

### What does not change

- `command_center.html` — untouched. The renderer does not care about the source of its JSON.
- Dashboard sections and data schema — compatible with v1.1. The generator outputs the same JSON structure.
- The visual design, status pill colors, toggle behavior, category table columns — all preserved.

---

## Update Mechanism

For each event that changes dashboard state:

| Event | What changes | Who acts | Generator needed? |
|---|---|---|---|
| New task created | New TASK-NNN.md with frontmatter | Creating agent | Yes — next session or immediately |
| Task status changes | Update `status:` in frontmatter | Task owner | Yes |
| Task blocked | Update `status: BLOCKED`, add `blocker:` | Task owner | Yes |
| BSIP0 gate passes | `bsip0_gate_result_*.md` created by pipeline | Automatic | Yes |
| BSIP1 enrichment completes | JSON files appear in `canonical_bsip1/` | Automatic | Yes |
| BSIP2 run completes | `AUTHORITATIVE.md` created | Automatic | Yes |
| QA verdict issued | `qa_report_*.md` created | QA Agent | Yes |
| Frontend dataset deployed | JSON file copied to `src/data/comparisons/` | Data Agent | Yes |
| Category registered in website | `types.ts` updated, `page.tsx` created | Frontend Agent | Yes |
| Decision made | Append to `decisions.json` | Deciding agent | Yes |
| Alert resolves | Automatically resolved in next generation | None | Yes |

"Yes — generator needed" means run `python generate_dashboard.py` to refresh the dashboard. This is the single maintenance action in v2.

---

## Ownership

| Component | Owner | Maintenance burden |
|---|---|---|
| Task registry (TASK-NNN.md frontmatter) | Product Agent creates; each agent updates own task status | Low — one field update per status change |
| Decision registry (`decisions.json`) | Product Agent appends when decision is made | Low — one append per decision |
| Category state | Automatic — generator reads pipeline indicators | None |
| Website state | Automatic — generator reads Next.js source | None |
| Alert rules | Embedded in generator — no runtime owner | None (code change only to add new alert type) |
| Generator script (`generate_dashboard.py`) | Data Agent maintains | Very low — update only when adding new alert types or schema changes |
| HTML renderer (`command_center.html`) | Frontend Agent maintains | None — unchanged from v1.1 |
| Running the generator | Product Agent at session start; any agent after task completion | One command |

---

## Reliability Properties

| Property | v1 | v2 |
|---|---|---|
| Category state accuracy | Requires manual update | Guaranteed accurate — derived from filesystem |
| Website state accuracy | Requires manual update | Guaranteed accurate — derived from source files |
| Task state accuracy | Requires manual update | Requires frontmatter discipline — 1 field update |
| Alert accuracy | Requires manual update | Auto-computed from accurate derived state |
| Drift possible? | Yes — any missed update | Only for task frontmatter (bounded, checkable) |
| Recovery from stale state | Manual re-entry | Run generator — immediate |
| Time to generate | N/A | < 5 seconds |

The only remaining source of drift in v2 is task frontmatter. This is bounded: there are a small number of tasks, the frontmatter update is a single field, and the generator will show tasks as COMPLETE only when the frontmatter says so. If an agent forgets to update frontmatter, the task appears as IN_PROGRESS in the dashboard, which is a visible signal to investigate — not silent corruption.

---

## What v2 Does Not Require

- No database
- No persistent process or cron job
- No webhook or file watcher
- No changes to the BSIP pipeline scripts
- No changes to the Next.js website
- No authentication or network access
- No real-time sync

v2 is a Python script that reads files and writes one JSON file. It runs when you run it. That is all.
