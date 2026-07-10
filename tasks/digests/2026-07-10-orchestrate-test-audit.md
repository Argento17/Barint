# After-action audit — orchestrate-mode test run (2026-07-10 night)

## 1. Run header
- **Directive (verbatim):** "1. Approve, 2. Approve, 3. Ok, 4. Wire. 5. We reduced it to Lumo and
  Oli only. remove the canva pipeline its useless. We now have the OpenAI assets which we can
  leverage?" + mid-turn "use the orchestrate mode in this run. lets test it"
- **Date:** 2026-07-10 evening→night. **Task:** TASK-588 + 5 owner-approved policy executions.
- **Phases:** policy edits → TASK-588 BUILD-HEAVY dispatch (×3 attempts) → verification → delivery.
- **Disposition:** TASK-588 RETURNED+VERIFIED, PR handed to owner (Speed 2). First real run of
  Capability Router v5 BUILD-HEAVY + first two Speed-1 autonomous merges. One router bug found+fixed.

## 2. Lane ledger
| # | stage | lane (capability) | engine | what | tokens | tool-calls | wall | outcome |
|---|-------|-------------------|--------|------|--------|-----------|------|---------|
| 1 | policy | inline (orchestrator) | fable-5 | CLAUDE.md merge ruling, orchestrate.md telemetry wiring, 3 memory files, settings Canva removal, board | UNTRACKED (~15k est) | ~20 | ~15m | done |
| 2 | dispatch | BUILD-HEAVY | gpt-5.6-sol | TASK-588 attempt 1 | 0 | 1 | ~1s | FAIL — driver TypeError (`cwd`→`worktree`); **no telemetry row** |
| 3 | dispatch | BUILD-HEAVY | gpt-5.6-sol | TASK-588 attempt 2 | UNKNOWN (schema gap) | — | short | FAIL — spec truncated to line 1 by .cmd shim; Codex correctly refused; telemetry trigger `empty diff` @18:37Z |
| 4 | infra fix | inline (orchestrator) | fable-5 | dispatch.py stdin fix + 3-line PONG proof + Speed-1 merge b5524728 | UNTRACKED (~8k est) | ~12 | ~20m | done |
| 5 | dispatch | BUILD-HEAVY | gpt-5.6-sol | TASK-588 attempt 3 (full 5-part spec) | UNKNOWN (schema gap) | — | ~35m (log 19:11Z → notify) | **PASS** — 18 files, exit_criterion_met=true |
| 6 | verify | inline (orchestrator) | fable-5 | C0 gate, parity+tsc independent re-runs, Hebrew-literal scan, diff reads, eyebrow value reads | UNTRACKED (~20k est) | ~14 | ~15m | PASS — all claims held |
| 7 | deliver | inline (orchestrator) | fable-5 | commit e1b25d19 on real branch, push, PR URL, registry+board | UNTRACKED (~5k est) | ~8 | ~5m | done |

## 3. Inline-vs-delegated split
- **Delegated:** 100% of the build (455-line diff, 18 files) — correct; zero orchestrator-authored
  product code.
- **Inline:** policy/bookkeeping (rows 1, 7 — the orchestrator's own lane, justified), verification
  (row 6 — undivided orchestrator duty, justified), and **row 4: the dispatch.py stdin fix, which is
  engine code done inline.** Justification: chicken-and-egg — the broken pipe was the only route to
  a builder, and the fix was 3 lines + a proof. Borderline-acceptable this once; a larger router
  defect must be routed to BUILD-LIGHT even if it delays the run.
- No "novel diagnostic build" over-claim occurred.

## 4. Pace & consumption
- Dispatches: 3 (1 productive). Subagent tokens: UNKNOWN — the v5 telemetry record does not capture
  them (finding E4). Wall: ~90m end-to-end; the productive path (attempt 3 + verify + deliver) ≈ 55m.
- Sequential by necessity (same files, one worktree). Nothing parallelizable was serialized.
- **Rework: 2 of 3 dispatches (67% of dispatch count), but near-0 token waste** — attempt 1 died in
  ~1s pre-lane; attempt 2 was a one-line prompt Codex refused cheaply. Biggest avoidable sink: the
  ~20m inline infra-fix loop (row 4), avoidable only if the .cmd-shim behavior had been caught by a
  multi-line selftest at TASK-583/585 time.

## 5. Error ledger (detection lag desc)
| defect | origin stage | catch stage | lag | fix cost |
|---|---|---|---|---|
| E2 `.cmd` shim truncates multi-line argv → one-line specs | TASK-583 (`_run_codex_exec` design) | first real BUILD-HEAVY dispatch (attempt 2) | 2 tasks (583→588); selftests used single-line prompts so it shipped green | 3-line stdin fix + PONG + merge (~20m) |
| E3 sandboxed Codex can't reach worktree's external `.git` → commit/push impossible; fell back to a private git-dir | worktree topology + spec demanded push | return verification | 1 run | orchestrator commit/push (~5m) |
| E4 telemetry record lacks tokens/duration/tool-calls | TASK-583 schema design | **this audit** | 2 tasks | pending (TASK-589) |
| E5 pre-lane driver crashes leave NO telemetry row | TASK-583 (log written only at lane completion) | this audit (attempt 1 invisible in log) | 2 tasks | pending (TASK-589) |
| E1 driver called `build_heavy(cwd=…)`, real kwarg `worktree` | orchestrator dispatch call | immediately (TypeError) | ~0 | re-dispatch |

No owner-caught defects this run (lag ∞ count: 0).

## 6. Corrective actions
| # | tied to | action | expected saving | status |
|---|---|---|---|---|
| C1 | E2 | Selftests must exercise the REAL failure surface: `--selftest-codex` now conceptually covered by the 3-line PONG used to prove the fix; keep multi-line prompts in any future lane selftest | kills the whole "green selftest, broken lane" class | **implemented** (stdin fix merged b5524728; PONG was multi-line) |
| C2 | E3 | Codify: BUILD lanes under `workspace-write` CANNOT git-commit/push from a worktree (external `.git`); spec asks for a clean tree + return contract, orchestrator commits/pushes after verification | 1 failed-expectation per future worktree build; no more fallback git-dirs to clean | **implemented** (orchestrate.md edit below) |
| C3 | E4+E5 | Extend `dispatch.py` telemetry: write a row at dispatch ENTRY and enrich the completion row with duration_s + Codex token usage (parsed from its output) | makes §4 of every future audit real data instead of UNKNOWN | routed → **TASK-589** (BUILD-LIGHT) |
| C4 | E1 | none needed beyond the fix — lane function signatures are keyword-only and self-erroring; cost was ~1s | — | n/a |

## 7. Consumption verdict
Efficient where it matters: the entire 455-line build was delegated to the subscription Codex lane,
verification stayed inline where it belongs, and the two dispatch failures burned seconds, not
tokens. The real cost of the run was the ~20m inline router repair — the price of a lane defect that
TASK-583's single-line selftest could not see. Highest-ROI change: C3 (telemetry tokens/entry rows),
because right now the router's own audit trail cannot answer this audit's §4.
**Headline: ~0% of delegated tokens were rework; 100% of rework cost was inline infra time caused by
one lane defect that shipped green.**

## 8. Skill-edit proposals
- **APPLIED (my lane, reversible):** `.claude/commands/orchestrate.md` step-4 BUILD bullet — added
  the sandbox-git rule (spec must ask for a clean tree, orchestrator commits after verification).
  Exact text in the file; see commit.
- **ROUTED:** C3 → TASK-589 (dispatch.py is router engineering, not an orchestrator hand-edit;
  BUILD-LIGHT, gpt-5.6-terra when dispatched).
- Recurrence check: none of E1–E5 has appeared in a prior audit — no red flags.
