# Bari — Data / Product Workspace

This repo (`C:\Bari`) is the **product/data workspace**, NOT the website.
The website is a separate repo at `C:\bari-web`.

## Hard rules
- Never assume `C:\Bari` is the website repo. No Next.js source lives here.
- Scoring/BSIP/research/CE work happens here; frontend work happens in `C:\bari-web`.
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
- **Lifecycle (no other states):** `IN_PROGRESS · BLOCKED · RETURNED · CHANGES_REQUESTED · CLOSED`. Agents propose `RETURNED`/`BLOCKED` in their return block; **only the Central Controller records `CLOSED`.**
- Details: `01_framework/operations/work_classification_v1.md`, `registry_first_rule_v1.md`, `registry_protocol_v1.md`.

## Where to look
- Architecture: `ARCHITECTURE.md`, `REPO_MAP.md`
- Scoring: `.claude/scoring.md` — read before any BSIP/scoring task
- Project context: `.claude/project.md`
- Skills (canonical): `.claude/skills/` — mirror to the website repo after edits
