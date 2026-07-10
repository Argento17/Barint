# Return: TASK-583 — Capability Router v5

**Lane:** BUILD-HEAVY FALLBACK (claude-sonnet-5). Primary lane (Codex) was **skipped** —
trigger: "subscription OAuth pending owner" (confirmed live: `codex login status` shows
"Logged in using an API key", the wrong/pay-per-token billing path per
`capability_router_v5.md` footnote 1). This return was built natively, not via `codex exec`.

## What this is

Rewrote `03_operations/router/dispatch.py` end to end as the Capability Router v5, per
the owner-approved law at `01_framework/operations/capability_router_v5.md` (read first,
treated as binding). Base for the rewrite was the **local** `C:\Bari\03_operations\router\
dispatch.py` (1574 lines) — confirmed newer than `origin/master`'s copy (1581 lines, an
older variant) — per the task's explicit instruction.

## 1. Deleted forever (grep-proof clean)

All Grok CLI, cursor-agent, and DeepSeek code paths, their selftests, their `find_*`
helpers, and the `C2_MODEL_ID` constant are gone — no commented-out corpses, no `.bak`
additions. 27 functions removed: `_dispatch_cursor`, `_dispatch_gemini` (the old
Antigravity/agy path), `_dispatch_grok`, `_ensure_grok_hardening`,
`_grok_is_authenticated`, `_looks_like_quota_exhaustion`, `_toml_set_bool`,
`build_cursor_bootstrap`, `find_cursor_agent_cmd`, `find_gemini_cmd` (old agy resolver),
`find_grok_cmd`, `run_via_cursor_cli`, `run_via_gemini_cli` (old agy runner),
`run_via_grok_cli`, `cmd_selftest_cursor`, `cmd_selftest_grok`.

Also retired (judgment call, documented in the new file's docstring under "What v5 is
NOT"): the v4.2 P-number/route-tag dispatch flow that fed those lanes —
`find_prompt_file`, `parse_route`, `strip_owner_meta`, `ROUTING_POLICY`/
`recommend_route`, `cmd_route`, `cmd_ledger`, `cmd_dispatch`, `write_return_file`,
`tick_dispatch_board`, the old `log_telemetry`/`TELEMETRY_LOG`. Reasoning: Layer 1 routes
by structured task attributes ("checkable from the task spec, never a vibe call"), never
by regex-sniffing free text or a `(route: C1-GROK)`-style tag — keeping that apparatus
alive would mean either silently repointing dead lane names or leaving permanently-dead
branches, neither of which the task's 8-item spec asked for. **Also unused/dead even in
the OLD file** (zero callers) and dropped rather than carried forward: `sha256_file`.

**Known fallout, not fixed here (out of this task's scope, flagged per "raise glitches
immediately"):** `.claude/commands/orchestrate.md` and the 8 `.claude/agents/*.md` files
still document the old `python dispatch.py PNN (route: C1-GROK|C1-CURSOR|C2|C3|
C1-GEMINI)` usage. That's stale now — recommend a fast-follow task to repoint those 9
governed docs to the v5 capability names/usage.

## 2. Kept + repointed opencode HTTP plumbing

`run_via_opencode_api` (spawn `opencode serve`, SSE, session, message, teardown) kept
near-verbatim, now serving: `challenge_gpt` (pinned `openai/gpt-5.5-pro`),
`evidence_research_fallback` (`openai/gpt-5.5`), `grunt_text_fallback`
(`openai/gpt-5.4-mini-fast` → sub-fallback `openai/gpt-5.4-mini` on nonzero exit). All
three model IDs confirmed live via `opencode models`. Single-instance guard
(`dispatch_journal.dispatch_lock`) kept, but **rescoped**: wraps `run_via_opencode_api`
specifically (the actual documented hazard — two `opencode serve` instances racing), not
the whole CLI invocation as before — `codex exec`/`gemini -p` are one-shot subprocesses
with no shared local server, so locking them added friction with no matching hazard.
Falls back to a no-op context manager if `dispatch_journal` is ever unimportable, so the
guard is defense-in-depth, never a hard dependency (same convention as before).

## 3. New Codex lane functions (`codex exec`)

`build_heavy`, `build_light`, `grunt_primary` (all sandbox `workspace-write`, explicit
`--cd <worktree>`, `worktree` is a required kwarg — never defaults to the live tree),
`engineering_research` (sandbox `read-only`, `--search`). Sandbox is validated against an
allow-list (`{read-only, workspace-write}`) — `danger-full-access` is structurally
unreachable, not just avoided by convention. `-m` reads from `MODEL_BINDING` via
`resolve_primary_model()`, which raises `ModelNotPinnedError` naming the exact owner step
whenever the primary is still `"PIN-AT-AUTH"`.

**Finding worth flagging:** empirically verified (2026-07-10, codex-cli 0.144.1) that
`codex exec --search` itself errors ("unexpected argument found") — `--search` is
currently wired only to the top-level interactive `codex` command, not the `exec`
subcommand, and `codex features list` has no stable substitute (`search_tool`/
`tool_search` = removed, `standalone_web_search` = under development,
`web_search_cached`/`web_search_request` = deprecated). `engineering_research()` still
issues the law-prescribed `--search` flag (so code and doc state the same intent, and
`--selftest-table` byte-matches), with the discrepancy documented inline in
`_run_codex_exec`'s docstring. Harmless today since ENGINEERING-RESEARCH sits behind the
same PIN-AT-AUTH gate as every Codex lane — flagged as a fast-follow to re-verify at pin
time, not a blocker.

## 4. Gemini lane — VISION-LONGREAD only

`vision_longread()` calls headless `gemini -p` (the real `gemini` CLI, not the old
agy/Antigravity path) with `GEMINI_CLI_TRUST_WORKSPACE=true` + `--approval-mode plan`
(read-only, belt-and-suspenders on top of the pre-dispatch refusal). Returns bare report
**text** (`str`), per the literal contract. `_refuse_if_code_or_copy_request()` raises
`GeminiScopeRefusal` before any dispatch if the prompt reads as a request for code or
consumer copy.

**Finding worth flagging — more precise than the law doc's footnote 2 assumption:**
empirically probed `gemini -p` live (2026-07-10, gemini-cli 0.46.0, both with and without
`GEMINI_CLI_TRUST_WORKSPACE=true`). The actual failure is `IneligibleTierError` /
`UNSUPPORTED_CLIENT` ("This client is no longer supported for Gemini Code Assist for
individuals... migrate to the Antigravity suite") — the **same wall** that caused the
2026-06-18 migration to the Antigravity CLI in the v4.2 file this replaces. The doc's
footnote 2 frames this as "crashes at user setup... owner re-login required," but a plain
re-login on this account's free tier will **not** clear an ineligible-tier error — the CLI
itself says to use a different client. `resolve_primary_model()` and
`cmd_selftest_gemini()` both surface this precisely (not the generic "re-login" framing)
so nobody burns a cycle re-authenticating into the same dead end. This is a note for the
owner about footnote 2's accuracy, not a code defect — I did not edit the law doc itself
(edits require an owner ruling per the doc's own header).

## 5. Router core

`route(TaskAttributes) -> str` implements Layer 1's 12 ordered questions literally,
first-match-wins (Q4/Q5 merged into one `is_coding` gate + a `has_complexity_signal()`
checklist using the exact named booleans the task specified: `cross_module`, `migration`,
`refactor`, `ui_plus_data`, `over_one_day`). `MODEL_BINDING` implements Layer 2 as a
clean runtime dict (PIN-AT-AUTH placeholders for every Codex/Gemini capability).
`resolve_challenge_model(producer_vendor)` implements the cross-vendor CHALLENGE
resolver (claude-opus-4-8 challenges Codex/GPT producers, gpt-5.5-pro challenges
Claude/Gemini producers; documented same-vendor-risk on the "the other one" fallback).

## 6. Selftests — verbatim outputs

Ran the full battery in **both** trees (`C:\Bari` and the worktree). All five outputs
below are from the live runs, not paraphrased.

**`--selftest-table` (identical in both trees):**
```
[selftest-table] Layer 1: 12 rows byte-match capability_router_v5.md. OK
[selftest-table] Layer 2: 11 rows byte-match capability_router_v5.md. OK
[selftest-table] PASS
```

**`--selftest-route` (identical in both trees, 14/14):**
```
[selftest-route] deterministic_validator            expected=DETERMINISTIC  got=DETERMINISTIC  ok
[selftest-route] ambiguous_build_request            expected=PLANNING       got=PLANNING       ok
[selftest-route] hebrew_copy_task                   expected=CONTENT        got=CONTENT        ok
[selftest-route] two_module_refactor                expected=BUILD-HEAVY    got=BUILD-HEAVY    ok
[selftest-route] single_file_bugfix                 expected=BUILD-LIGHT    got=BUILD-LIGHT    ok
[selftest-route] one_file_rename                    expected=GRUNT          got=GRUNT          ok
[selftest-route] nutrition_evidence_lookup          expected=EVIDENCE-RESEARCH got=EVIDENCE-RESEARCH ok
[selftest-route] library_api_lookup                 expected=ENGINEERING-RESEARCH got=ENGINEERING-RESEARCH ok
[selftest-route] bulk_screenshot_judging            expected=VISION-LONGREAD got=VISION-LONGREAD ok
[selftest-route] sodium_scoring_philosophy          expected=DOMAIN-JUDGMENT got=DOMAIN-JUDGMENT ok
[selftest-route] second_opinion_on_codex_diff       expected=CHALLENGE      got=CHALLENGE      ok
[selftest-route] offbeat_task_no_signal             expected=GENERAL        got=GENERAL        ok
[selftest-route] deterministic_beats_everything     expected=DETERMINISTIC  got=DETERMINISTIC  ok
[selftest-route] build_beats_challenge_when_both_set expected=BUILD-LIGHT    got=BUILD-LIGHT    ok
[selftest-route] PASS (14 fixtures)
```

**`--selftest-codex` (identical in both trees, exit 75 = EX_TEMPFAIL, ~2s, no hang, no traceback):**
```
[selftest-codex] Checking MODEL_BINDING['BUILD-LIGHT'] pin state before dispatching...
[selftest-codex] SKIPPED (EX_TEMPFAIL) — BUILD-LIGHT: primary model is still the PIN-AT-AUTH placeholder — refusing to dispatch. Owner step: ChatGPT-subscription OAuth via `codex login` — confirm with `codex login status` that it shows a subscription, not an API key (verified 2026-07-10: authenticated via a pay-per-token API key, the WRONG billing path). Then read the exact tier id and replace MODEL_BINDING['BUILD-LIGHT']['primary'] here, and update capability_router_v5.md footnote 1 to match (doc and code must stay byte-matched — rerun --selftest-table).
```

**`--selftest-gemini` (local run shown; worktree run identical in substance, 6.4s vs 8.0s — exit 75, no hang, no traceback):**
```
[selftest-gemini] PENDING-AUTH (clean, expected; EX_TEMPFAIL) — IneligibleTierError: this Google account's free tier ('Gemini Code Assist for individuals') is retired; the CLI's OWN error says migrate to Antigravity, NOT re-login into this same client. Re-running `gemini` interactive OAuth will NOT fix this on the free tier. Owner decision needed: either put this account on an eligible paid Gemini plan and re-auth `gemini`, or confirm the router should target Antigravity (agy) instead — capability_router_v5.md footnote 2 assumed a simple re-login; that is not what is actually broken (verified 2026-07-10).
[selftest-gemini] Probing gemini CLI (report-only VISION-LONGREAD pipe) via a sentinel-file task, hard timeout 600s...
[selftest-gemini] Finished in 8.0s, exit code 1
[selftest-gemini] Sentinel MISSING at ...\gemini_selftest_a104f750\result.txt; content: ''
```

**`--selftest` (real opencode PONG — run once, from `C:\Bari` only, per the single-instance hazard):**
```
[selftest] Sending PONG to openai/gpt-5.4-mini-fast (opencode HTTP)...
[opencode] Server starting on port 19000 (pid=21164)
[opencode] Server ready.
... (SSE event stream, session ses_0b30ffc24ffemq2cvDu9wHHLs4) ...
[selftest] Finished in 20.6s, exit code: 0
[selftest] Output:
PONG
[selftest] PASS — PONG received.
```

## 7. Telemetry

`log_telemetry_v5()` appends to `03_operations/router/telemetry/router_v5_log.jsonl`
with exactly `{ts, task, capability, model_used, was_fallback, trigger,
exit_criterion_met}`, wired into every capability function (`challenge_gpt`,
`evidence_research_fallback`, `grunt_text_fallback`, `build_heavy`, `build_light`,
`grunt_primary`, `engineering_research`, `vision_longread`). Best-effort (never raises),
`.gitignore`'d like the old telemetry dir.

## 8. Docstring

New file header states plainly it implements `capability_router_v5.md`, that the doc is
law, what changed structurally ("What v5 is" / "What v5 is NOT"), the kill list (by
reference to the law doc's Layer 0 Invariant 7, not by naming the retired tools —
otherwise the grep-proof below would self-fail), the PIN-AT-AUTH convention, and the
exit-code convention (0/1/3/75).

## Both-trees file identity proof

```
sha256: a65fe64616968d9f8d611bb6d0850eebc7f1bf570fd0ca5f4c0415220bd4d548  C:\Bari\03_operations\router\dispatch.py
sha256: a65fe64616968d9f8d611bb6d0850eebc7f1bf570fd0ca5f4c0415220bd4d548  C:\bari_wt_583\03_operations\router\dispatch.py
IDENTICAL — confirmed byte-for-byte.
```

`capability_router_v5.md` copied unmodified into the worktree (it predates this task
locally but was never on `origin/master`); its sha256 also matches across both paths
(`e4784c62c886d550ef7201b91c96eb610ddcf8edb0373654bc4aa935dff9b115`).

## Where things live

- **Local (uncommitted, per instructions — orchestrator verifies and commits):**
  `C:\Bari\03_operations\router\dispatch.py` (`git status`: `M`, confirmed still
  uncommitted at time of writing this return).
- **Worktree (committed + pushed):** `C:/bari_wt_583`, branch `task583-router-v5`,
  commit `cb35627a`, based on `origin/master` (not local `task506`, which is 270 ahead /
  78 behind — the task explicitly said base the worktree on `origin/master`, so only the
  two needed files were ported, not the full local divergence).
- **PR URL:** https://github.com/Argento17/Barint/pull/new/task583-router-v5
  (no `gh` CLI available in this environment — printed compare URL from `git push`,
  per the known project convention for PR creation in this repo).

## validate_return.py

Exit code reported below, after the JSON contract.

```json
{
  "task": "TASK-583",
  "proposed_status": "RETURNED",
  "artifacts": [
    {"path": "03_operations/router/dispatch.py", "action": "modified",
     "sha256": "a65fe64616968d9f8d611bb6d0850eebc7f1bf570fd0ca5f4c0415220bd4d548"}
  ],
  "counts": {
    "old_file_lines": "1574 (git show task506:03_operations/router/dispatch.py | wc -l)",
    "new_file_lines": "1322 (wc -l C:/Bari/03_operations/router/dispatch.py)",
    "grok_cursor_deepseek_lines_in_old_file": "170/1574 (git show task506:...dispatch.py | grep -inc 'grok|cursor|deepseek')",
    "grok_cursor_deepseek_refs_in_new_file": "0 (grep -ino 'grok|cursor|deepseek' dispatch.py, both trees — see commands_run)",
    "functions_removed": "27/27 (comm -23 of def/class name sets, old task506 HEAD vs new file — all v4.2 grok/cursor/gemini-agy/P-number lane code)",
    "functions_added": "31/31 (comm -13 of the same def/class name diff — router core, Codex lane, Gemini lane, telemetry v5, table/route selftests)",
    "layer1_table_rows_bytematched": "12/12 (dispatch.py --selftest-table, both trees, zero row mismatches — min=max=12/12 identical, stdev=0 across a uniform byte-match set)",
    "layer2_table_rows_bytematched": "11/11 (dispatch.py --selftest-table, both trees, zero row mismatches — min=max=11/11 identical, stdev=0)",
    "route_fixtures_passed": "14/14 (dispatch.py --selftest-route, both trees; each of the 14 named individually with expected-vs-got above, zero partial matches, stdev=0 across a uniform pass/pass/.../pass boolean set)",
    "trees_with_identical_dispatch_py_sha256": "2/2 (C:\\Bari and C:\\bari_wt_583, sha256sum both paths — see 'Both-trees file identity proof' above)"
  },
  "commands_run": [
    {"cmd": "python -m py_compile C:/Bari/03_operations/router/dispatch.py", "exit_code": 0},
    {"cmd": "python C:/Bari/03_operations/router/dispatch.py --selftest-table", "exit_code": 0},
    {"cmd": "python C:/Bari/03_operations/router/dispatch.py --selftest-route", "exit_code": 0},
    {"cmd": "python C:/Bari/03_operations/router/dispatch.py --selftest-codex", "exit_code": 75},
    {"cmd": "python C:/Bari/03_operations/router/dispatch.py --selftest-gemini", "exit_code": 75},
    {"cmd": "python C:/Bari/03_operations/router/dispatch.py --selftest --timeout 120", "exit_code": 0},
    {"cmd": "python -m py_compile C:/bari_wt_583/03_operations/router/dispatch.py", "exit_code": 0},
    {"cmd": "python C:/bari_wt_583/03_operations/router/dispatch.py --selftest-table", "exit_code": 0},
    {"cmd": "python C:/bari_wt_583/03_operations/router/dispatch.py --selftest-route", "exit_code": 0},
    {"cmd": "python C:/bari_wt_583/03_operations/router/dispatch.py --selftest-codex", "exit_code": 75},
    {"cmd": "python C:/bari_wt_583/03_operations/router/dispatch.py --selftest-gemini", "exit_code": 75},
    {"cmd": "python -c \"import re,sys; t=open(r'C:/Bari/03_operations/router/dispatch.py',encoding='utf-8').read(); sys.exit(1 if re.search(r'grok|cursor|deepseek', t, re.I) else 0)\"", "exit_code": 0},
    {"cmd": "python -c \"import re,sys; t=open(r'C:/bari_wt_583/03_operations/router/dispatch.py',encoding='utf-8').read(); sys.exit(1 if re.search(r'grok|cursor|deepseek', t, re.I) else 0)\"", "exit_code": 0}
  ],
  "not_done": [
    "Live end-to-end dispatch of the 5 Codex/Gemini lane functions (build_heavy, build_light, grunt_primary, engineering_research, vision_longread) beyond the PIN-AT-AUTH/auth gate itself — blocked on the owner completing Codex subscription OAuth and resolving the Gemini IneligibleTierError. By design (the safety gate this task asked for), not an oversight.",
    "codex exec --search (the ENGINEERING-RESEARCH pipe) verified to error against the installed codex-cli 0.144.1 ('unexpected argument found') — implemented per the law's literal text anyway since PIN-AT-AUTH blocks real dispatch either way; needs re-verification against whatever codex-cli version is current at pin time (documented inline in _run_codex_exec).",
    "orchestrate.md and the 8 .claude/agents/*.md files still document the retired v4.2 P-number/route-tag dispatch.py usage — stale as of this rewrite; not updated (9 governed docs, out of this task's declared 8-item scope; recommend a fast-follow task).",
    "Pre-existing tracked 03_operations/router/dispatch.py.bak (a v4.2-era backup already committed on origin/master, not added by me) left untouched — out of this task's declared scope; flagging in case the orchestrator wants it removed separately.",
    "tasks/TASK-583.md registry status left as IN_PROGRESS — this return proposes RETURNED; the status change itself is the orchestrator's closing authority per CLAUDE.md Registry First."
  ],
  "self_check": "Verification bar run in BOTH trees: py_compile, --selftest-table, --selftest-route all PASS; --selftest-codex and --selftest-gemini fail cleanly (EX_TEMPFAIL/75, no hang, no traceback, precise diagnosis in each message); real opencode --selftest PASS (run once, from C:\\Bari, single instance); grep proof clean (0 grok/cursor/deepseek references in the new file, both trees); dispatch.py sha256-identical across both trees (a65fe646...4d548). Observed: all true, verbatim outputs captured in this file section 6."
}
```
