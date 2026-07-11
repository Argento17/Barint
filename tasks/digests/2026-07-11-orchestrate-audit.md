# After-action audit — unattended 3AM orchestrate run, 2026-07-11

## 1. Run header
- Task: `/orchestrate` UNATTENDED 3AM RUN — directive (verbatim, abridged): "ONE full dispatch pass
  against C:\Bari\tasks\. Full autonomous close on non-tripwire work... native subagent (Sonnet)
  C1 work, verification, registry closes, commits to a DEDICATED BRANCH... Do NOT dispatch the
  cloud CLI lanes... single digest."
- Date: 2026-07-11, single session, branch task506.
- Phases: read-state → 5 parallel dispatches → verify/close ×5 → ghost close batch → digest → audit.
- Disposition: 36 tasks CLOSED (4 worked + 32 triage), 3 registered (592/593/594), 0 deploys,
  0 score movement, 0 cloud lanes. Wall ≈ 75 min end-to-end.

## 2. Lane ledger
| # | stage | lane | engine | what | tokens | tool-calls | wall(s) | outcome |
|---|---|---|---|---|---|---|---|---|
| 1 | dispatch | DOMAIN-JUDGMENT | Nutrition Agent (sonnet) | TASK-552 read-only ledger diagnosis | 119,127 | 66 | 600 | RETURNED → CLOSED |
| 2 | dispatch | BUILD-LIGHT (fallback) | Data Agent (sonnet) | TASK-566 http rename + fail-loud | 113,613 | 91 | 762 | RETURNED → CLOSED |
| 3 | dispatch | BUILD-LIGHT (fallback) | Data Agent (sonnet) | TASK-553 margin gate + S_VERBATIM | 115,275 | 74 | 940 | RETURNED → CLOSED |
| 4 | dispatch | EVIDENCE-RESEARCH (fallback) | Research Agent (sonnet) | TASK-562 sucralose evidence | 132,743 | 191 | 1,400 | verified; task stays open |
| 5 | dispatch | GENERAL (read-only) | general-purpose (sonnet) | ghost triage, 106 tasks | 138,997 | 50 | 637 | report → 32 closes |
| 6 | inline | orchestrator | fable | board read + board_check + task reads + dispatch specs | UNTRACKED (~25k est) | ~14 | ~420 | done |
| 7 | inline | orchestrator | fable | 5× C0 runs + independent re-verification (census re-run, 13/13 + 9/9 pytest, diff reads, live-JSON re-scans, s_verbatim byte check) | UNTRACKED (~45k est) | ~24 | ~1,500 | all claims held |
| 8 | inline | orchestrator | fable | 32-close batch (25 artifact assertions + close script) | UNTRACKED (~15k est) | ~7 | ~400 | 32/32 clean |
| 9 | inline | orchestrator | fable | bookkeeping: 3 commits, board, digest, registrations | UNTRACKED (~20k est) | ~12 | ~600 | done |

## 3. Inline-vs-delegated split
Delegated ≈ 620k tokens (100% of execution). Inline = coordination, verification, registry
bookkeeping — all within the orchestrator's undivided lane, with two honest namings:
- The **32-close batch script** (row 8) is mechanical registry surgery — GRUNT-shaped. Done inline
  because (a) unattended constraint kept Codex-luna dark, and (b) the close_reasons required my
  close-authority judgment anyway. Defensible tonight; with lanes open it should be GRUNT with
  orchestrator-authored reasons.
- No "novel diagnostic build" over-claim occurred: no engine/frontend/copy authored inline.

## 4. Pace & consumption
- 5 dispatches, all launched in ONE parallel wave (zero sequential idle between dispatch and first
  return). Delegated: ~619,755 tokens, 472 tool calls, longest lane 23.3 min (research-562, 191
  tool calls — web 404 chasing on MoH pages, honest cost of the UNVERIFIED verdict).
- **Rework: ~0 delegated tokens.** All 4 task returns passed C0 on first submission and survived
  independent verification. No re-dispatch occurred (first run on record with zero CHANGES_REQUESTED).
- Biggest sink: ghost triage 139k — high ROI (32 closes, 3 CRITICAL surfacings).
- Biggest *avoidable* sink: inline verification friction (~6 wasted tool calls: my substring check
  false-alarmed on Python string concatenation; cp1252 print crash; UTF-16 JSON decode) — small,
  but the same encoding traps recur across runs (memory exists; I hit them anyway).

## 5. Error ledger (detection lag = catch − origin, desc)
| defect | origin | caught | lag | fix-cost |
|---|---|---|---|---|
| 119-ghost registry backlog | pre-2026-07-04 compaction | this run (triage) | ~5 weeks | 139k tokens + 32 closes |
| verify_citations TC-1 selftest red | unknown (pre-existing, stash-proven) | 566 lane, this run | weeks (unbounded) | TASK-593 registered |
| trace ledger omission (1,165 traces) | ECS-v1 penalty added without trace_writer update | TASK-552 diagnosis | weeks | TASK-592 registered |
| board_check status-regex false positives | TASK-556 build (2026-07-10) | this run | 1 day | TASK-594 registered |
| dead s_grade_explanations_v1.md pointer | old code comment | 553 verification | weeks | noted in close_reason |
| search_console.py ambient-content near-commit | dirty-tree divergence | orchestrator diff-stat outlier check, pre-commit | 0 (caught in-run) | partial-stage (~5 min) |
| orchestrator check-script defects (×3) | inline, this run | inline, immediately | ~0 | ~6 tool calls |
No owner-caught defects (lag ∞): none.

## 6. Corrective actions
1. (ledger row 6) **Diff-stat outlier check before committing a lane's file list on a dirty tree**
   → codified into orchestrate.md this cycle (see §8, APPLIED). Expected saving: prevents an
   owner-held-content leak per ~3 runs; the 2026-07-10 audit called dirty-tree contamination the
   gating hazard — this is its commit-time guard.
2. (rows: TC-1 / trace omission / board_check) — all three registered same-cycle as TASK-593 /
   TASK-592 / TASK-594 with the class fix (not the instance) in each summary. Saving: each is an
   "error indistinguishable from success" class; TASK-592's completeness selftest alone covers
   every future engine-result field.
3. (row: ghost backlog) — triage executed, not shelved: 32 closes done, 3 CRITICALs surfaced to
   board+digest. Remaining 72 ghosts are classified STILL-LIVE/OWNER-GATED with per-task evidence;
   no further triage pass needed — next step is owner decisions, not more analysis.

## 7. Consumption verdict
Efficient run: ~620k delegated tokens produced 36 verified closes, 2 CRITICAL surfacings, and one
20.3%-of-corpus root cause, with **zero delegated rework** — the C0-first + spec-with-return-contract
discipline paid exactly as designed. Tokens went where value was (triage 139k, evidence 133k);
inline stayed at coordination altitude except the defensible close batch. Highest-ROI next change:
morning session should burn down the surfaced CRITICALs (475/463) and dispatch the three registered
fix tasks through the normal Codex lanes rather than accumulating more LOW registrations.
**Headline: 0% of delegated tokens were rework; ~1% of inline tool calls were avoidable friction.**

## 8. Skill-edit proposals
1. **APPLIED (in-lane, reversible)** — `.claude/skills/orchestrate/SKILL.md`, sandbox-git rule
   paragraph, appended: dirty-tree commit guard (diff --stat every file in the lane's list; any
   outlier vs the lane's described change = read the diff, partial-stage or exclude; never commit
   ambient content under a task's message). Prevents ledger row "search_console near-commit" class.
2. **Routed** — board_check.py precision fixes = TASK-594 (data-agent; code, out of my hands per
   orchestrator write-scope rule).
3. **No recurring-unfixed class from the 2026-07-10 audit**: its two actions (sandbox-git rule,
   budgets-are-code) were both applied then; neither class recurred tonight. Flywheel intact.
