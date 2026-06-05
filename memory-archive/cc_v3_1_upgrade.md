---
name: cc-v3-1-upgrade
description: "Command Center generator upgrade — lean live read path, --digest, drift_ack/work_type, blocked-aware next-action, critical path"
metadata: 
  node_type: memory
  type: project
  originSessionId: ab7390dd-3012-49c9-8263-5bac99a32d5f
---

Command Center (`05_command_center/generate_dashboard.py`) upgraded 2026-06-02 for token efficiency + accuracy. Key workflow changes:

- **Read `command_center_live.json` (~19KB, open tasks only)** as the default — NOT the full `command_center.json` (72KB) or `command_center_archive.json` (closed-task detail). Full board trims CLOSED summaries (moved to archive); the HTML renderer is unaffected (never reads closed `summary`).
- **`python generate_dashboard.py --digest`** prints the morning report (health/WIP, critical chain, open board, closed-today, drift triage) — no files written. Use it instead of hand-building the morning picture.
- **`next_action` is now blocked-aware**: it walks `depends_on` to the actionable ROOT unblocker instead of recommending a BLOCKED task. (Fixed the bug where it pointed at BLOCKED TASK-142 instead of TASK-142A.)
- **`critical_path`** section: `longest_chain` + `top_unblockers` (unblocks-N), derived from the depends_on/blocks graph.
- **Real WIP (`task_summary.wip`)**: capacity + health now measure execution-only IN_PROGRESS. Tag umbrellas `work_type: coordination`, decisions `work_type: decision` so they don't inflate the capacity alert.
- **`drift_ack: "<reason>"`** frontmatter suppresses a known-good CLOSURE_DRIFT; a `reopened_at:` value auto-suppresses (deliverable expected-invalid). Acknowledged drift shows in `drift.acknowledged` and does NOT count against `clean`.

`check_drift.py` inherits the ack logic and now also refreshes `command_center_live.json`. See [[bsip2_task133_and_maadanim_drift]] for the registry-first discipline this supports.
