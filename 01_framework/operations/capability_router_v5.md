# Capability Router v5 — HARD-STONED (owner-approved 2026-07-10, TASK-583)

**This document is law for all model routing in the Bari Agent OS.** It supersedes Router
v4.2 (BAND=FUNCTION) and every lane memory that conflicts with it. Changing this document
requires an explicit owner ruling. Sessions route every task through Layer 1; models are
bound ONLY in Layer 2, so model swaps edit one table row and never restructure the router.

Owner design requirements captured here verbatim in spirit:
complexity-based (never file-count) build routing · planning resolves ambiguity BEFORE any
implementation · evidence research and engineering research are separate lanes · cross-vendor
second opinions · an exit criterion for every lane · route by CAPABILITY, bind models
separately.

---

## Layer 0 — Invariants (apply to every task, always)

1. **Deterministic first.** If written rules + a validator fully determine the output, no
   model runs. Scripts decide (C0: validators, run_gates, conformance, verify_signoffs).
2. **Two-gate copy law unchanged.** Every consumer-facing string needs Content sign-off AND
   the Adversarial gate, sha256-pinned (TASK-567). The orchestrator never authors copy.
3. **Cross-vendor challenge invariant.** Whoever challenges/verifies a deliverable is from a
   different company than whoever produced it. No exceptions inside one vendor family.
4. **Exit criteria are gates.** A lane's work is not "done" until its exit criterion (Layer 1
   table) is met and the orchestrator has verified the claims against artifacts before close.
5. **Explicit model pins.** Every Claude subagent dispatch states its model. An unpinned
   dispatch silently downgrades to Sonnet (the known drift trap) and is a routing error.
6. **Fallback logging.** Every fallback activation is logged in the task registry with the
   trigger that fired.
7. **Kill list (retired forever, never re-add without owner ruling):** Grok CLI, Cursor
   (cursor-agent), DeepSeek, and all anonymous opencode free-proxy models
   (big-pickle / hy3-free / mimo-v2.5-free / nemotron-3-ultra-free / north-mini-code-free /
   deepseek-v4-flash-free). Qwen: evaluated and declined by owner 2026-07-10.
8. **Prohibitions.** Gemini writes zero consumer copy and zero code (reports only). Grunt
   receives zero judgment calls. Builders never author Hebrew copy. Nothing skips
   orchestrator verification, including Codex ("fully trusted with tasks" means trusted to
   execute, never exempt from verification).

---

## Layer 1 — Capability Router (ordered questions; FIRST MATCH WINS)

| # | Question about the task | Capability | Exit criterion |
|---|---|---|---|
| 1 | Output fully determined by written rules, validator exists? | DETERMINISTIC | Validator exit 0 |
| 2 | Needs decomposition, architecture, or ambiguous scope? | PLANNING | Written spec with acceptance criteria + the re-routing decision for the implementation |
| 3 | Produces consumer-facing Hebrew copy? | CONTENT | Copy validators pass AND both gates signed, sha256-pinned |
| 4 | Coding with ANY complexity signal (checklist below)? | BUILD-HEAVY | Builds clean, tests pass, reviewed diff, return contract validates |
| 5 | Coding with NO complexity signal? | BUILD-LIGHT | Same as BUILD-HEAVY |
| 6 | Mechanical non-code work (renames, fills, conversions)? | GRUNT | Re-verified by validator/orchestrator; zero unexplained diffs |
| 7 | Evidence research (papers, regulation, government sources, nutrition science, competitors)? | EVIDENCE-RESEARCH | Every claim carries a source; citations pass verify_citations.py |
| 8 | Engineering research (GitHub, libraries, frameworks, APIs, implementation patterns)? | ENGINEERING-RESEARCH | Recommendation names exact versions + licenses + a working proof snippet |
| 9 | Bulk one-pass reading, or judging images / rendered pages? | VISION-LONGREAD | Structured report produced (only artifact type accepted) |
| 10 | Scoring or nutrition philosophy? | DOMAIN-JUDGMENT | Reasoned recommendation citing the governing framework docs |
| 11 | Needs an independent second opinion (or follows any delivery above)? | CHALLENGE | Verdict with evidence, produced cross-vendor per Invariant 3 |
| 12 | Anything else | GENERAL | Return contract validates |

**Complexity checklist (question 4).** ANY single signal routes BUILD-HEAVY. All are
checkable from the task spec — never a vibe call:
- Touches ≥ 2 modules/packages
- Any migration (schema, data, framework)
- A refactor intended to preserve behavior
- A feature spanning UI + data layers
- PLANNING estimated it above ~1 day

**Ordering rule.** PLANNING (Q2) sits above all implementation. An ambiguous build request
never reaches a builder directly: Claude resolves it into a spec, and the spec re-enters the
router.

---

## Layer 2 — Model Binding (the ONLY table edited when models change)

| Capability | Primary (exact) | Fallback (exact) | Pipe | Fallback trigger |
|---|---|---|---|---|
| PLANNING | claude-fable-5 | claude-opus-4-8 | Main chat / Plan agent | Model unavailable |
| CONTENT | claude-fable-5 | claude-sonnet-5 | Content Agent, pinned | Spawn failure or 2 consecutive rejected drafts |
| BUILD-HEAVY | Codex — top coding tier (PIN-AT-AUTH¹) | claude-sonnet-5 (Frontend/Data agent) | `codex exec` in a worktree, sandbox `workspace-write` | Nonzero exit, empty diff, sandbox refusal, or auth pending |
| BUILD-LIGHT | Codex — cheap/fast tier (PIN-AT-AUTH¹) | claude-sonnet-5 agent | same | same |
| GRUNT | Codex — cheapest tier (PIN-AT-AUTH¹) | claude-haiku-4-5 (Agent tool) | `codex exec`, sandbox `workspace-write`; deliberately cross-vendor fallback | API/CLI error, or any output failing its validator once |
| EVIDENCE-RESEARCH | gpt-5.5 + web search | Claude Research Agent (sonnet pin) | Codex CLI `--search` / opencode API | API error or timeout 120s |
| ENGINEERING-RESEARCH | Codex + web search (PIN-AT-AUTH¹) | Claude Research Agent (sonnet pin) | `codex exec --search`, read-only sandbox | same |
| VISION-LONGREAD | Gemini subscription model (PIN-AT-AUTH²) | claude-sonnet-5 subagent reading screenshots | `gemini -p` headless, `GEMINI_CLI_TRUST_WORKSPACE=true`, report-only | CLI hang > 10 min, crash, or empty output |
| DOMAIN-JUDGMENT | claude-fable-5 | claude-opus-4-8 | Nutrition/Product agents, pinned | Spawn failure |
| CHALLENGE | claude-opus-4-8 **when producer was Codex/GPT** · gpt-5.5-pro **when producer was Claude or Gemini** | the other one | Agent tool (opus pin) / opencode API | Producer-vendor outage |
| GENERAL | claude-sonnet-5 (explicit pin) | claude-haiku-4-5 for trivial | Agent tool | Spawn failure |

¹ **PIN-AT-AUTH (Codex):** exact tier IDs are read from `codex` after the owner completes
ChatGPT-subscription OAuth (`codex login`), then written here in place of the placeholder.
Status 2026-07-10: CLI v0.144.1 installed; currently authed with a **pay-per-token API key**
(wrong billing path — subscription OAuth pending owner). Config default: `gpt-5.5`, reasoning
`medium`. Sandbox tiers available: `read-only` / `workspace-write` / `danger-full-access`
(never use the third). **Build-time caveat (2026-07-10):** on 0.144.1, `--search` is a
top-level flag only — `codex exec --search` errors. The ENGINEERING-RESEARCH invocation gets
re-verified and corrected at pin time (TASK-584).

² **PIN-AT-AUTH (Gemini) — CORRECTED 2026-07-10 after live probing:** the working binary for
this subscription is **Antigravity (`%LOCALAPPDATA%\agy\bin\agy.exe`, v1.1.0 present)**, auth
in Windows Credential Manager (Target=gemini:antigravity). The npm `gemini` CLI v0.46.0
crashes with IneligibleTier/UNSUPPORTED_CLIENT on this account — that client is simply not
supported on this tier; **no plan upgrade needed, no owner re-login proven necessary yet.**
Live agy sentinel-file round-trip FAILED 2026-07-10 (lane flaky since 07-08). Until revived,
VISION-LONGREAD stays pin-gated (fails loudly, falls back to claude-sonnet-5 per binding).
Revival = TASK-584: repoint the lane to agy, fix headless flags, sentinel selftest green,
pin the exact model ID, and update this doc's Layer-2 pipe cell + code together (the
--selftest-table byte-match keeps them honest).

---

## Operational appendix

- **Router implementation:** `03_operations/router/dispatch.py` implements Layer 1 + Layer 2
  literally. The routing table in code must byte-match this document's tables (a selftest
  asserts it). Old v4.2 lanes (grok/cursor/deepseek) are deleted, not commented out.
- **opencode API path** (GRUNT-fallback text calls, CHALLENGE-GPT, EVIDENCE fallback):
  `opencode serve` HTTP as today; authenticated models: `openai/gpt-5.5-pro`,
  `openai/gpt-5.5`, `openai/gpt-5.4-mini(-fast)` via OpenAI OAuth.
- **Hazards carried over:** never two dispatch.py processes in parallel; cloud/CLI lanes run
  in worktrees (lane dispatch can wipe a shared tree); executor prompts include "do NOT
  spawn subagents".
- **Telemetry:** every routed task logs {capability, primary/fallback used, trigger, exit
  criterion result} to `03_operations/router/telemetry/`.
