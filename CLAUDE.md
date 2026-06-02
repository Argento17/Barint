# Bari — Data / Product Workspace + Website (monorepo)

This repo (`C:\Bari`) is the **Agent OS / product-data workspace** AND, since the
TASK-134 consolidation (2026-06-01), it also contains the **website** as a subtree
at `C:\bari\bari-web\` (the Next.js app, formerly the standalone `C:\bari-web` repo).

## Hard rules
- The repo root (`C:\Bari`) is the Agent OS brain. **No Next.js source at the root** —
  all frontend code lives under `bari-web/`. Keep the two concerns in their own trees.
- Scoring/BSIP/research/CE work happens at the root; frontend work happens in `C:\bari\bari-web`.
- Do NOT change published scores or redesign scoring unless explicitly instructed.
- Do NOT invent product, nutrition, or ingredient data.

## Frozen invariants (CNO ruling, 2026-05-30)
- Milk scores = `run_004_recalibrated`. Top = 85/A (whole/4%/goat dairy). No reversion.
- No snack bar reaches A. snk-001 = 70/B is the validated category ceiling.
- Bread provenance = `real_bread_retail_003_v1` (Shufersal, 25–26 May 2026):
  256 scanned → 81 scored → 31 curated (24 scored + 7 transparency).
- Freeze the framing ("best ≠ excellent"); version the numbers (re-verify on every rescore).

## Tasks & registry (Agent OS — all agents)
- **Classify first.** Conversation Work (quick advice, clarifications, prompt edits, minor copy, one-offs, lightweight reviews) → handle inline: **no TASK, no registry, no dashboard.** Registry Work (multi-step, reviewed deliverable, a dependency, changes shipped/governed artifacts, or an explicitly assigned `TASK-XXX`) → tracked. When unsure, default to Conversation Work.
- **Authoritative registry = `C:\Bari\tasks\`** (one `TASK-NNN.md` per task; state in YAML `status:`). The dashboard is *derived* (`05_command_center/generate_dashboard.py` → `command_center.json`); never hand-edit the JSON. The markdown `task_registry_v1.md` in the website repo is a frozen, non-authoritative snapshot.
- **Registry First.** Any `TASK-XXX` op (status/close/accept/reject/block/resume/reopen) **consults `C:\Bari\tasks\` first** — the registry is authoritative, conversation is not. If they disagree, the registry wins and you surface it. Unknown id → "not registered."
- **Lifecycle (no other states):** `IN_PROGRESS · BLOCKED · RETURNED · CHANGES_REQUESTED · CLOSED`. Domain agents propose `RETURNED`/`BLOCKED` in their return block; they never write `CLOSED`. **Closing authority is held by the Central Controller and, by delegation (2026-06-02), the CC Agent** — which records `CLOSED` only after its close-readiness gate passes (return-block claims independently verified against artifacts; see `.claude/agents/cc-agent.md`). Genuine judgement calls (accept/reject tradeoffs, prioritization, governance) still escalate to the human/Product. A `roadmap_impact: true` task cannot be closed until CC sets `cc_reviewed` (enforced by a PreToolUse guard).
- Details: `01_framework/operations/work_classification_v1.md`, `registry_first_rule_v1.md`, `registry_protocol_v1.md`.
- **Orchestration (direct dispatch).** The main chat is the orchestrator: it dispatches owning agents **directly** via the Agent tool with the 5-part delegation spec (parallel/background as fit) — it does **not** hand the user prompts to paste. Execution lives in subagents (own context window; only summaries return) to keep the main context lean. **After any tracked deliverable returns, run the CC close-readiness gate** (verify claims against artifacts) before closing/opening — this is an orchestrator instruction, not a hook (`SubagentStop` can't nudge or spawn). Durable state = registry + dashboard + memory, so start a fresh chat per phase and rebuild with `/roadmap`. Full model: `01_framework/operations/orchestration_model_v1.md`.

## Where to look
- Architecture: `ARCHITECTURE.md`, `REPO_MAP.md`
- Scoring: `.claude/scoring.md` — read before any BSIP/scoring task
- Project context: `.claude/project.md`
- Skills (canonical): root `.claude/skills/` — the single source of truth for the Agent OS. The website's own scoped config lives at `bari-web/.claude/`; do not mirror Agent OS skills into it (TASK-131 → TASK-134).
