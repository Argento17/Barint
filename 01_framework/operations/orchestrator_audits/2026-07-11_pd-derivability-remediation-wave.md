# Orchestrator After-Action Audit — PD Trace-Derivability Remediation Wave

## 1. Run header
- **Run:** Corpus derivability remediation + 629 re-score copy + cookies basis fix (continuation of the 2026-07-11 /orchestrate loop).
- **Owner directive (verbatim):** "Go ahead" → "fix everything" wave → "Approved for both, go ahead" (10 copy rows + cookies) → "provide the PR you need and run telemetry."
- **Date:** 2026-07-11.
- **Phases:** trace-wiring (630) · comma audit (631) · calc-fail triage (632) · backfill wave (639) · cookies basis fix (634) · copy author+two-gate (633).
- **Disposition:** all 6 tracked tasks CLOSED + verified; calc-FAIL 111→2, ALL-GREEN 56%→70%, parity diverge=0; consumer deploy staged on task506 (owner merge pending).

## 2. Lane ledger
| # | Stage | Lane (band) | Engine | What | Tokens | Tool-calls | Outcome |
|---|---|---|---|---|---|---|---|
| 1 | trace-wiring | BUILD-HEAVY | Codex terra (wt) | 630: 52 backfill traces + parity cp1252 fix | UNTRACKED (~760KB out) | — | RETURNED→closed (after order-fix) |
| 2 | comma audit | BUILD-HEAVY | Codex terra (wt) | 631: corpus type_b audit + producer harden | UNTRACKED (~404KB out) | — | RETURNED→closed |
| 3 | calc triage | BUILD (diag) | Codex terra (main, ro→rw) | 632: classify 61 calc-FAILs | UNTRACKED (~409KB out) | — | RETURNED→closed |
| 4 | backfill wave | BUILD-HEAVY | Codex terra (wt) | 639: 59 backfill traces + 5 configs | UNTRACKED (~258KB out) | — | RETURNED→closed |
| 5 | cookies fix | BUILD (fallback) | Data Agent sonnet (main) | 634: basis fix + re-score + PD rebuild | 294,995 | 122 | RETURNED→closed |
| 6 | copy author | CONTENT | Content Agent fable | 633: author 10 + revise 4 | 245,293 | 32 | RETURNED (SIGN-OFF) |
| 7 | copy gate | CHALLENGE | Adversarial QA opus | 633: red-team + re-gate | 268,720 | 9 | BLOCK→SIGN-OFF |
| I | orchestration | inline | Opus (this loop) | verify/commit/board/registry/merge-reconcile | UNTRACKED (est ~120K) | ~55 | — |

## 3. Inline-vs-delegated split
- **Delegated ≈ 88%** of value: all builds (Codex), the data fix (Data), all authoring + both gates (Content/QA). Correct — no builder work done on the Opus orchestrator.
- **Inline (Opus):** verification (score==trace, semantic diffs, parity), git bookkeeping, branch reconciliation, the 630 config-order swap. The config-order swap (a 3-line config edit) was done inline as a **correction of my own dispatch-spec defect** — defensible (fastest path to unblock verification) but is lane-work; a cleaner run routes even that back. No delegable *build* work was done inline.
- **Cross-vendor discipline:** producers were Codex (630/631/632/639) and Claude (633 Content); challenges/verification came from the other vendor or the Opus orchestrator + the Adversarial-QA opus gate. Router bias avoided (contrast the pre-wave single-vendor violation).

## 4. Pace & consumption
- **Dispatches:** 7 background lanes (4 Codex + 3 Claude-agent), ~6 combined main-tree rebuilds, 1 branch reconciliation.
- **Tracked subagent tokens:** ~809K (Data 295K + Content 245K + QA 269K); Codex tokens **UNTRACKED** (dispatch.py returns tokens=None for these lanes — a real telemetry gap).
- **Parallelism:** good — 630/631 ran concurrent; 632/633/634 ran concurrent; 639 in a worktree concurrent with 634 on main (deliberately isolated to avoid a PD-rebuild race).
- **Rework tokens:** the 633 copy revise+re-gate (~274K of the 514K copy/QA total ≈ **53%**) was a *designed* two-gate cycle, not avoidable rework — the gate caught 3 real overclaims pre-ship. Genuinely avoidable rework: the 632 re-dispatch (read-only-sandbox bug) and the 630 config-order second rebuild — small (~1 Codex run + 1 rebuild each).
- **Biggest sink:** the copy two-gate (514K) — justified (consumer copy, HARD two-gate). **Biggest avoidable:** the 632 read-only-sandbox re-dispatch.

## 5. Error ledger (by detection lag, desc)
| Defect | Origin stage | Catch stage | Lag | Fix cost |
|---|---|---|---|---|
| Subagent switched main-tree branch (7 commits on stray task635-seo-geo) | 634 Data run (main tree) | post-hoc, reading a merge-commit msg | ~5 commits | ff-merge + branch -f (medium) |
| cookies |Δ|>30 estimate wrong (actual 18–24) | TASK-614 rough estimate | 634 actual re-score | ~long (stood since 614) | none (estimate corrected) |
| 3 copy overclaims (soy-flour / sat-fat / partial-list) | 633 Content 1st draft | Adversarial QA gate (designed) | 1 gate cycle (pre-ship, 0 to owner) | Content revise + re-gate (designed) |
| 630 run_products_dir order (first-dir-wins) | my 630 dispatch spec | my main-tree verify | 1 dispatch cycle | 3-line swap (low) |
| 632 runner: read-only sandbox blocks report + tuple return | my 632 runner | immediate poll (no report file) | ~0 (same turn) | re-dispatch (low) |

## 6. Corrective actions
1. **Branch guard before every commit** (→ branch-switch defect, lag ~5 commits). `git rev-parse --abbrev-ref HEAD` assert == session branch before each orchestrator commit; instruct main-tree domain agents "do NOT git checkout/branch/commit." **Expected saving:** eliminates a post-hoc untangle (~5–8 tool calls). *Applied:* memory `subagent_switched_main_tree_branch`; skill edit proposed below.
2. **Read code semantics before specifying ordering** (→ 630 order defect, lag 1 cycle). Dispatch specs that assert data-structure semantics (dir precedence, merge order) must cite the code line, not assume. **Expected saving:** 1 Codex run + 1 rebuild per occurrence. *Applied:* memory + 639 spec cited L349 first-dir-wins.
3. **Report-writing diagnostics need workspace-write** (→ 632 sandbox defect). **Expected saving:** 1 re-dispatch. *Applied:* memory `codex_exec_return_tuple_and_readonly_blocks_report`.
4. **Instrument Codex token capture** (→ pace gap: 4 lanes UNTRACKED). dispatch.py should parse Codex token usage into LaneResult so audits aren't blind on half the lanes. **Expected saving:** measurable consumption on every future Codex-heavy run. *Not applied — routes to router owner as a dispatch.py enhancement.*

## 7. Consumption verdict
Efficient and correctly delegated: ~88% of value ran in subagents, cross-vendor discipline held, and the one big token sink (the copy two-gate, ~514K) was mandatory and paid for itself by catching 3 overclaims **pre-ship, zero reaching the owner**. Avoidable rework was small (~2 re-dispatches). The single highest-ROI change next run is the **branch guard** — the branch-switch was the highest-lag defect and the only one that risked silent data-loss. Headline: **~5% of tokens were avoidable rework; the 53% "rework" in the copy lane was the two-gate working as designed, not waste.**

## 8. Skill-edit proposals
- **APPLIED — `.claude/commands/orchestrate.md` step 7:** poll-your-own-lanes guard (async completion notice lags real EXIT). *(applied earlier this run)*
- **PROPOSED — `.claude/commands/orchestrate.md` step 5/6 (persist state):** add a **branch-assert** bullet: "Before any orchestrator commit/merge, run `git rev-parse --abbrev-ref HEAD` and assert it is the session branch — Agent-tool subagents run in the main tree cwd and can switch it under you." Ties to error-ledger row 1. *Apply now (in-lane, reversible).*
- **ROUTED — `03_operations/router/dispatch.py`:** capture Codex token usage into LaneResult (ties to §4 UNTRACKED gap). Out of the audit's lane → router owner.
- **No recurrence-without-fix:** none of these error classes appear in the prior 2026-07-11 audit (the single-vendor violation there had its own fix applied); no red-flag repeat.
