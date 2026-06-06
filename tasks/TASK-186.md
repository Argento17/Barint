---
id: TASK-186
title: Command Center v2 operating model (Chief-of-Staff reframe of the board)
owner: cc-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-06-05
completed_at: 2026-06-05
close_reason: "Dashboard is approved"
depends_on: []
blocks: [TASK-187]
category_id: null
roadmap_impact: true
cc_reviewed: "2026-06-05"
cc_comments:
  - flag: fyi
    date: "2026-06-05"
    text: >
      Roadmap-impact review (CC, 2026-06-05): primary artifact verified —
      05_command_center/command_center_v2_operating_model.md exists (394
      lines, two owner-ratified revisions). Design document only; no scoring,
      no published data, no frozen invariants touched. W1+W2 child TASK-187
      is RETURNED with cc_reviewed set and return block present. Remaining
      waves (spine-kill, PROGRESS LINE, authority-badge, Opportunity-Radar)
      explicitly out of scope for this umbrella close. Owner preview of the
      rendered brief is the remaining gate before either task closes.
drift_ack: "Closure-drift false-positive: the operating-model deliverable (command_center_v2_operating_model.md) is the design proposal authored under this umbrella, but TASK-186 is legitimately IN_PROGRESS — only the W1+W2 prose-brief slice (TASK-187) is being built; the spine-kill / PROGRESS LINE / authority-badge / Since-You-Left / Opportunity-Radar waves and the four new registry conventions are not yet shipped. Same umbrella pattern as TASK-179/180."
summary: >
  Umbrella design proposal: command_center_v2_operating_model.md. Reframes the Command Center as Tom's executive interface to an autonomous org (AI Chief of Staff): lead with NEXT MOVE / SINCE YOU LEFT / WHAT'S WRONG / PROGRESS, exception-gated, earned silence. Render-contract change over the existing generator. Owner approved the W1+W2 prose-brief slice first (TASK-187). W1+W2 prose brief delivered via TASK-187 (RETURNED 2026-06-05). Remaining waves (spine-kill, PROGRESS LINE, authority-badge, Since-You-Left deeper, Opportunity-Radar) not in scope for this task.
---

# TASK-186 — Command Center v2 operating model (Chief-of-Staff reframe)

## What
Umbrella design: `05_command_center/command_center_v2_operating_model.md`. Reframes the
Command Center from a task dashboard into **Tom's executive interface to an autonomous
multi-agent org** — an AI Chief of Staff that leads with the few things that need him and
stays silent ("earned silence") otherwise. Level-1 brief: **YOUR DECISION · NEXT MOVE ·
SINCE YOU LEFT · GOING WRONG · PROGRESS LINE**, exception-gated. It is a **render-contract
change** over the existing `generate_dashboard.py` derivation engine — the engine stays.

## Status
Proposal accepted in principle by the owner (2026-06-05). Owner selected the **prose
morning brief** (Section D.1) as the first build slice → **TASK-187** (W1+W2 brief).
Remaining waves (kill the spine, PROGRESS LINE, authority badges, Since-You-Left ledger,
Opportunity Radar, the four new registry conventions) sequence after the brief lands.

## roadmap_impact
`true` — reshapes Tom's primary instrument; go-live owner-gated.

**Blocks:** TASK-187. **Assigned:** cc-agent.
