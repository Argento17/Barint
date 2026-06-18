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
- **NEVER use Open Food Facts (OFF) as a data source — anywhere, any field, any category, forever.**
  Banned for nutrition, ingredients, names, barcodes, images, serving sizes, category, fallback,
  enrichment, validation, "temporary" fills, comparison JSON, frontend display, generated copy,
  scoring traces, and confidence. The **only** source for ingredients + nutrition is the **direct
  product scrape**: if it's parsed, use it; if not, the field is NULL and the page shows "data could
  not be retrieved." Never substitute OFF or any other source. "Unknown is acceptable; OFF is not."
  This is PROJECT-WIDE (owner reconfirmed 2026-06-10, overriding the earlier salty-snacks-only
  localization). Any OFF dependency is a launch blocker. The OFF integration client stays disabled.
  Removing only with a future explicit written owner policy. (Memory: `off_ban_hard_rule`; TASK-238.)

## Re-flow policy (owner ruling, 2026-06-18 — supersedes the 2026-05-30 CNO freeze)
- **Nothing is frozen.** Every live category re-scores on every scoring switch (`spine_flip`), with **no category-level freeze gate and no exit-2 hard block** (the old `class: frozen` + `frozen_touched` gate is removed/inert; never re-arm it). "Freeze shenanigans" are retired — the job is to *version the numbers and verify movement*, never to prevent it. Verify with `03_operations/page_generator/conformance.py --all` (12/12 categories re-flow as of 2026-06-18; see [[spine_conformance_gate]]).
- **Historical baselines (re-verify on rescore, do NOT freeze):** milk top was 85/A at `run_005_headpin` (whole 3.4% / natural 4% / goat); snack-bar ceiling was snk-001 70/B (a validated *finding*, not an enforced cap); bread provenance lineage = `real_bread_retail_003_v1` (corpus identity — which products — NOT a score freeze; 256 scanned → 81 scored → 31 curated). These are starting points to compare against, not values to hold fixed.
- Framing principle retained: "best ≠ excellent." That was always about *framing*, not pinning numbers — and "version the numbers, re-verify on every rescore" is now the whole of it.

## Decision authority (autonomy default, 2026-06-04)
- **Default to autonomous action.** Owning agents, the orchestrator, and Product decide and act within their lanes. The owner makes **extremely strategic decisions only.** Escalate to the owner **only if a decision trips one of 5 tripwires:** (1) **an agent would change published scores / scoring philosophy** (note: an owner-initiated `spine_flip` re-flowing every category is expected and NOT a tripwire — nothing is frozen); (2) ships something **irreversible AND consumer-facing** (category go-live, public claim, brand/positioning); (3) **starts or kills a major program**; (4) creates **external commitment, spend, or legal exposure**; (5) **redefines strategy, target user, or what Bari is.**
- **If no wire fires → decide, act, keep it reversible (flag / PR / draft), and log it in the registry.** If unsure whether a wire fires, it doesn't — act and surface it for after-the-fact review. A decision beyond your lane that trips no wire routes to Product / Orchestrator, **not** the owner. Expert calls inside a lane are the owning agent's — recommend the single best option and implement it; no A/B menus for expert calls.
- Full law (5 tripwires, triage matrix, ownership tiers, safety guarantees): `01_framework/governance/decision_authority_matrix_v1.md`.

## Tasks & registry (Agent OS — all agents)
- **Classify first.** Conversation Work (quick advice, clarifications, prompt edits, minor copy, one-offs, lightweight reviews) → handle inline: **no TASK, no registry.** Registry Work (multi-step, reviewed deliverable, a dependency, changes shipped/governed artifacts, or an explicitly assigned `TASK-XXX`) → tracked. When unsure, default to Conversation Work.
- **Authoritative registry = `C:\Bari\tasks\`** (one `TASK-NNN.md` per task; state in YAML `status:`). The registry is the single source of truth. The markdown `task_registry_v1.md` in the website repo is a frozen, non-authoritative snapshot.
- **Registry First.** Any `TASK-XXX` op (status/close/accept/reject/block/resume/reopen) **consults `C:\Bari\tasks\` first** — the registry is authoritative, conversation is not. If they disagree, the registry wins and you surface it. Unknown id → "not registered."
- **Lifecycle (no other states):** `IN_PROGRESS · BLOCKED · RETURNED · CHANGES_REQUESTED · CLOSED`. Domain agents propose `RETURNED`/`BLOCKED` in their return block; they never write `CLOSED`. **Closing authority is the orchestrator** — which records `CLOSED` only after verifying return-block claims against artifacts (read DoD, check each claim at file:line, add `close_reason`). Judgement calls resolve **autonomously by default** (accept/reject tradeoffs, prioritization, governance → owning agent / Orchestrator / Product per the matrix); only the 5 strategic tripwires reach the owner — see **Decision authority** below.
- Details: `01_framework/operations/work_classification_v1.md`, `registry_first_rule_v1.md`, `registry_protocol_v1.md`.
- **Orchestration (direct dispatch).** The main chat is the orchestrator and holds **undivided closing authority** (there is no separate CC agent — eliminated 2026-06-13). It dispatches owning agents **directly** via the Agent tool / the router with the 5-part delegation spec (parallel/background as fit) — it does **not** hand the user prompts to paste. Execution lives in subagents (own context window; only summaries return) to keep the main context lean. **After any tracked deliverable returns, verify claims before closing** — check each artifact claim, set `status: CLOSED` with a `close_reason` citing evidence. Run the loop with `/orchestrate`; get the read-only decision map with `/roadmap`. Full model: `01_framework/operations/orchestration_model_v1.md`.
- **State lives in the registry — there is no derived dashboard** (command center retired 2026-06-13). `C:\Bari\tasks\` is the single source of truth; `tasks\DISPATCH_BOARD.md` is its live view; `tasks\closed\` is the archive. Open a new tracked task with `python C:\Bari\tasks\new_task.py …`. Durable state = registry + memory; start a fresh chat per phase and rebuild with `/roadmap`.
- **Return Contract.** Every agent return block ends with the machine-readable JSON contract (`01_framework/operations/return_contract_v1.md`); returns without it are auto-`CHANGES_REQUESTED`.

## Where to look
- Architecture: `ARCHITECTURE.md`, `REPO_MAP.md`
- Scoring: `.claude/scoring.md` — read before any BSIP/scoring task
- Project context: `.claude/project.md`
- Skills (canonical): root `.claude/skills/` — the single source of truth for the Agent OS. The website's own scoped config lives at `bari-web/.claude/`; do not mirror Agent OS skills into it (TASK-131 → TASK-134).
