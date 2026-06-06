---
id: TASK-187
title: "Command Center v2 W1+W2 — Chief-of-Staff prose morning brief at top of board (NEXT MOVE / SINCE YOU LEFT / WHAT'S WRONG, exception-gated)"
owner: cc-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-06-05
completed_at: 2026-06-05
close_reason: "Dashboard is approved for now"
depends_on: [TASK-186]
blocks: []
category_id: null
roadmap_impact: true
cc_reviewed: "2026-06-05"
cc_comments:
  - flag: fyi
    date: "2026-06-05"
    text: >
      Roadmap-impact review (CC, 2026-06-05): deliverable verified against
      command_center.html (working tree, uncommitted). renderBrief() at lines
      1114-1224 implements all three exception-gated sections (NEXT MOVE,
      SINCE YOU LEFT, WHAT'S WRONG) composing from next_action / tasks /
      alerts / drift — no invented fields. Injected at line 1408 above all
      other content. TASK-186A additions untouched. Roadmap impact is
      render-contract only; generator and registry unchanged. Owner preview
      required before CLOSED (DoD criterion).
summary: >
  First build of TASK-186: a short CC-voiced prose brief at the very top of command_center.html leading with NEXT MOVE (named), then SINCE YOU LEFT (autonomous closes/opens) and WHAT'S WRONG (named faults), exception-gated so a clean day stays calm. Reuses the emit_digest voice. Additive, reversible, render-only — all clauses derived from existing command_center.json fields; no generator change. Does NOT remove the monitoring spine, progress line, or new registry conventions (later steps).
---

# TASK-187 — Command Center v2 W1+W2: Chief-of-Staff prose morning brief

## Parent
First build of **TASK-186** (`05_command_center/command_center_v2_operating_model.md`),
the owner-approved Command Center v2 reframe. Owner picked the **prose morning brief**
(Section D.1, the highest-leverage move) as the first slice to ship.

## Scope (this build only)
- Add a short CC-voiced **prose brief** at the very top of `command_center.html`,
  above the existing board, leading with **NEXT MOVE** (named), then **SINCE YOU LEFT**
  (what the org did autonomously) and **WHAT'S WRONG** (named faults).
- **Exception-gated**: a clean day stays short and calm; faults appear only when real.
- Reuse the `emit_digest` voice/composition tone — do not invent a new register.
- Everything composed from existing `command_center.json` fields
  (`next_action`, `executive`, `critical_path`, `tasks` closed/opened-today,
  `category_state`, `alerts`, `drift`). **No `generate_dashboard.py` change.**
- Additive and reversible: the brief renders *above* the current spine/board; nothing
  removed. If a clause's source field is missing, the clause is **omitted**, never faked.

## Out of scope (later steps of TASK-186)
- Removing the CC monitoring spine / HUD gauges.
- The PROGRESS LINE (W5) — needs `went_live_at` (a later convention).
- YOUR DECISION (W1 escalation) beyond what's already derivable, and the four new
  registry conventions (`authority`, `went_live_at`, last-seen marker, machine `revival_gate`).
  Clauses that depend on those degrade gracefully (omitted) until the conventions land.

## roadmap_impact
`true` — this reshapes Tom's primary instrument (the render contract of the board).
CC does not self-close until the owner has seen it rendered (owner-gated go-live).

## Definition of Done
- Brief renders at the top of the board against live registry-derived data, in CC's voice.
- NEXT MOVE names the real next task; SINCE YOU LEFT cites real closed/opened counts;
  WHAT'S WRONG names the real blocker (or stays silent when clean).
- No invented content; missing fields degrade gracefully.
- Owner previews it; CC records CLOSED only after owner sign-off.

**Assigned:** cc-agent. **Related:** TASK-186 (parent design).

---

## Return block (2026-06-05)

### What changed
- **`05_command_center/command_center.html`** — the implementation spans:
  - CSS: lines 349–375 (`.cc-brief` block and all sub-selectors: `.cc-brief-head`, `.cc-brief-by`, `.cc-brief-date`, `.cc-brief p`, `.lead.next/.since/.wrong/.yours`, `b.tid`, `.cc-brief .calm`)
  - JS: `renderBrief(d)` function at lines 1114–1224
  - Injection point: line 1408 (`<div id="cos-brief">${renderBrief(d)}</div>`) — first element inside `.main`, above `renderDecision`, `renderTodos`, `cos-personal`, `renderGoingWrong`, and the portfolio tile
  - `rerenderRegistry()` at line 585 refreshes the brief when the personal store mutates (fault dismissals update the WHAT'S WRONG count)

### What the brief renders today (live data, 2026-06-05)

All three sections are active on today's board (RED health, 3 live faults, 12 closed today, 8 opened today):

**NEXT MOVE**
> [DA chip] **TASK-190** — Granola/cereal data-capture fix. Root unblocker for TASK-189 (Sodium scoring + capture fix for granola/cereal ...) — do this to clear the chain. → unblocks TASK-189

**SINCE YOU LEFT**
> Closed 12 (TASK-180B, TASK-180C, TASK-181, TASK-181O, +8 more), 6 on the CC close-readiness gate with no sign-off needed. Opened 8. All reversible — flag any you want rolled back.

**WHAT'S WRONG**
> **TASK-182** Waiting for clinician to sign the NDA (sent 2026-06-05). Pe · +2 more — see "going wrong" below.

On a clean board (zero alerts, no BLOCKED tasks, no drift) the brief stays entirely silent — no header, no box, no placeholder. The "Nothing else needs you" calm line appears only when NEXT MOVE or SINCE YOU LEFT rendered but no faults exist.

### Confirmation TASK-186A additions are untouched
All TASK-186A elements verified present in working tree:
- `renderDecision()`, `renderTodos()`, `personalPlaceholder()` / `hydratePersonal()` at their original positions (lines 1409–1411)
- `renderGoingWrong()` at line 1412
- `details.portfolio` tile (BARI PORTFOLIO collapsible) in `render()` output
- `cos-decision`, `cos-todo`, `cos-personal`, `cos-going-wrong` section IDs all intact
- `command_center_v1_backup.html` untouched

### DoD status
- Brief renders at top of board against live data: PASS
- NEXT MOVE names TASK-190 (real next task per `next_action`): PASS
- SINCE YOU LEFT cites 12 closed / 8 opened / 6 auto-gated: PASS
- WHAT'S WRONG names TASK-182 fault + "+2 more": PASS
- No invented content; missing fields degrade gracefully: PASS
- **Owner preview required before CLOSED** — not yet previewed. CC does not self-close this task.
