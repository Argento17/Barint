# Lane Routing Rules v1 — Orchestrator Law

> **SUPERSEDED 2026-06-14 by [`bari_router_v4_2.md`](bari_router_v4_2.md)** (the canonical routing law).
> v4.2 routes **capability-first** (engine-to-strength) where v1 routed **cost-first**, adds the 4-axis
> model (band × lane × control × validation), honest lane wiring states, and the cloud boundary. **This
> file is retained as the wire-level implementation appendix** — the escalation ladder, selftest/quota
> mechanics, lane-capability constraints (Gemini/Grok), and token rules below still hold and v4.2 points
> here for them. Where the two disagree on *default routing*, **v4.2 wins**.

*Owner-directed 2026-06-12. Originally the canonical routing law for all dispatched work.*

## The principle

**Route every unit of work to the cheapest lane that delivers full quality — never
trade quality for tokens.** Claude tokens (orchestrator + native subagents) are the
metered, scarce resource. Cursor and ChatGPT are flat-rate subscriptions; DeepSeek is
free. Token optimization means *protecting the Claude budget for what only Claude in
this repo can do* — judgment grounded in Bari's personas, skills, memory, and
governance — and pushing everything else outward.

## The lanes

| Lane | Engine | Cost | Transport | Holds a TASK? |
|---|---|---|---|---|
| **Orchestrator** | this chat (Opus/Fable) | metered, highest | — | closes, never executes |
| **C1** | native Claude subagents (Sonnet) | metered | Agent tool | yes |
| **C1-GROK** | xAI Grok Build CLI (`grok -p --always-approve`, SuperGrok sub) | flat | router `(route: C1-GROK)` | yes |
| **C1-GEMINI** | Google Gemini CLI (full executor, `--approval-mode=yolo`) | flat/free tier | router `(route: C1-GEMINI)` | yes |

| **C1-CURSOR** | Cursor headless agent CLI (cursor-agent, `--force --trust`) | flat-rate sub | router `(route: C1-CURSOR)` → `_dispatch_cursor` | yes |

*C1-CURSOR was retired 2026-06-14 (→ C1-GROK) and **REACTIVATED 2026-06-18** when the owner renewed the
Cursor Pro subscription; `(route: C1-CURSOR)` dispatches to its own lane again (`--selftest-cursor` PASS).*
| **C2** | DeepSeek via opencode | free | router `(route: C2)` | yes |
| **C3** | ChatGPT Plus (web) | flat + owner time | owner pastes | **never** — advice only |

## Routing matrix (decide in this order)

1. **Zero-judgment / mechanical?** (probes, counts, grep, format-from-spec, running
   existing scripts, bulk renames) → **C2**. Grunt work never spends subscription or
   Claude tokens.
2. **Spec-complete implementation?** The prompt file fully defines done — code changes
   with a crisp DoD, pipeline scripts, tests, refactors, build fixes, frontend
   components built from an approved spec → **C1-GROK** (or C1-GEMINI on the free tier).
   Quality here depends on the spec plus code correctness, not on Bari judgment, so a
   flat-rate executor lane carries it.
3. **Bari-judgment work?** Quality depends on personas/skills/memory/governance —
   scoring interpretation, editorial copy to the milk bar, category methodology,
   design judgment, QA verdicts, anything governed (frozen invariants, claim gates,
   consumer-facing standards) → **C1** (native subagent, owning agent's frontmatter
   model).
4. **Orchestrator-level decision needing outside perspective?** Strategy calls,
   methodology challenges, pre-launch stress tests, market/evidence research →
   **consult C3** (see below), then decide.
5. **When unsure between C1 and a flat-rate executor (C1-GROK/C1-GEMINI) → C1.** When
   unsure between C2 and anything → the higher lane. Misrouting *down* costs a failed
   loop; misrouting *up* costs only tokens.

### C1 vs C1-GROK — the division test

Ask: **"If the executor had never seen Bari before, would the prompt file alone
produce the right result?"**

- **Yes** → C1-GROK (the flat-rate executor; reads the repo + root/`bari-web` `AGENTS.md`
  automatically). C1-GEMINI is the equivalent free-tier executor for the same class of work.
- **No — it needs Bari's editorial bar, scoring philosophy, agent skills, or memory**
  → C1.

Run the lanes **in parallel on independent workstreams** (different files/dirs);
never two writers on the same files. Per-owner WIP limit (2) applies across both.

### Visual deliverables — split the build from the look (added 2026-06-13)

For any **rendered visual** (charts, a comparison page, layout, anything whose
quality is *seen*): the BUILD is spec-complete code → **C1-GROK / Frontend**.
But the **pixel review CANNOT be delegated** — the orchestrator must render it and
**look at the screenshot itself**. A sub-agent's "0 CRITICAL" on visual work is
untrustworthy until the orchestrator has Read the rendered image. ("Data correct +
builds clean" and "looks good" are *different* verification jobs; the first does not
imply the second.) Harness: dev server + `playwright` → a `scripts/shot-*.mjs` that
writes a PNG the orchestrator Reads. The orchestrator hand-building visual code in-chat
is the wrong default (it's the "fully-specified transform → Cursor" case) — delegate the
build, keep the look. Two corollaries that compound routing cost if missed:
- **Capture the REAL build exit code** (`npm run build > log 2>&1; echo $?`). A `| tail`
  pipe reports tail's exit (0) and masks a failed build — a delegated "build passed" is
  worthless if piped.
- **Don't trust an external tool's chart output** (NotebookLM, Flow, etc.): verify its
  data against the authoritative JSON *and* check it didn't silently swap the chart
  choice off-thesis. (Flow/NotebookLM have no usable API here anyway; Flow is video/image
  generation, not charts — design reference only, implement natively.)

## Escalation ladder (one retry, then up)

A failed return gets **one** in-lane revision (CHANGES_REQUESTED with the specific
gap). A second failure escalates **one lane up** — C2 → C1-GROK → C1 → orchestrator
wall — with the failure history pasted into the new prompt. Never burn a third
attempt in the failing lane; repeated cheap failures cost more (verification tokens +
calendar time) than one correct expensive run.

**SuperGrok quota exhaustion is not a failure — it's a lane outage.** The SuperGrok
subscription has usage limits and may run out mid-cycle. The router detects it
(exit code 75, `⛔ C1-GROK LANE DOWN` banner in the return) — when that fires:
re-route the same prompt to native **C1 immediately** (no revision loop, the work
never started), mark the lane **DOWN on the board** with the date, and route new
spec-complete work to C1 (or C1-GEMINI) until the quota resets. Quota state is
why C1-GROK is an *optimization* of C1, never a dependency: nothing may be planned
that only works if Grok is up. (Exit 75 also fires **NOT ACTIVATED** when Grok isn't
signed in — owner one-time `grok login`; the router fast-fails in <1s rather than
hanging on the interactive welcome screen.)

## C3 — the orchestrator's advisor

C3 exists **for the orchestrator to consult before deciding**, not to execute.
Triggers: a tripwire-adjacent strategy call, a methodology/scoring challenge worth an
outside-family read, pre-launch red-team, Deep Research evidence gathering, fresh-eyes
Hebrew consumer reads. The orchestrator drafts a self-contained consult prompt
(`tasks/prompts/`, `C3:` tag, explicit output format), the owner pastes it, and the
answer returns as **advice the orchestrator weighs — never a return, never a close,
never product/nutrition data** (fabrication + OFF risk).

## Routing self-audit — anti-laziness enforcement (owner-directed 2026-06-13)

*Added after a session where the orchestrator routed **13/13** dispatches to C1 and
consulted C3 **zero** times — collapsing all work onto the two most expensive nodes
(C1 + orchestrator), with C2 and C1-CURSOR dark. The law above already required
otherwise. **Defaulting to C1 because it's familiar is laziness, not caution, and is a
named process violation.** This section makes the failure checkable.*

Before every dispatch the orchestrator states the lane + a one-line reason, and applies:

1. **Spec-complete code → C1-GROK, not C1.** If the prompt fully defines "done"
   (engine edits with a crisp DoD, EV registration, tests, pipeline scripts, refactors,
   build fixes), it routes to **C1-GROK by default** (or C1-GEMINI). Keeping it on metered
   C1 needs a *stated* reason. **"No-regression discipline" is NOT such a reason** — the
   flat-rate lane codes, C1/orchestrator verifies. Implementation and its verification are
   separable; split them (the hybrid). Two EV implementations were kept on metered C1
   (~205k tokens) for exactly this bad reason.
2. **C3 consult is MANDATORY (not optional) before these forks:**
   - an honest-vs-artifact / "is this clustering/collapse real?" scoring call,
   - a precedent / loophole / special-pleading question on a governance change,
   - any tripwire-adjacent ruling where the orchestrator is leaning on a *single* owning
     agent's word.
   The owning C1 agent's ruling **plus the orchestrator's own read is not a substitute**
   for an outside-family second opinion. C3 is flat-rate and near-zero cost to the Claude
   budget — **skipping it is never justified by cost.** Draft the consult, surface it for
   the owner to paste, weigh the answer, then decide.
3. **Don't absorb C2-grade work into the orchestrator.** Mechanical sub-steps (counts,
   tallies, greps, re-derivations) the orchestrator finds itself doing *by hand* are C2
   candidates — small size is not a reason to hoard them in the most expensive node.
4. **Log the distribution at every report/wall.** Name the lane split (C1 vs C1-GROK vs
   C1-GEMINI vs C2, and whether C3 was consulted). A ledger that is ~100% C1 with the
   other lanes dark is itself a routing-failure signal to surface, not bury.
5. **Lane capability constraints (route to what a lane can actually do):**
   - **C1-GEMINI is a full executor (flat-rate, free tier).** Corrected 2026-06-14: the lane was
     mis-described as "read/plan-only" because the router invoked it without an approval-mode flag, so
     Gemini fell to `default` (prompt-for-approval) and **auto-denied every tool call in headless `-p`
     mode → "Unauthorized tool call."** That was a missing flag, not a capability limit. The router now
     passes `--approval-mode=yolo` (mirrors Cursor's `--force`); a write+shell probe confirmed it edits
     files and runs commands. Gemini's CLI supports four modes — `default` / `auto_edit` / `yolo` /
     `plan` (read-only) — so the lane can be pinned read-only *on purpose* via `executor=False`, but its
     default is now execution. **Route to C1-GEMINI like C1-GROK: spec-complete implementation on the
     flat-rate tier** (it reads the repo; same division test). Use `plan` mode only when you deliberately
     want a read-only analyst pass.
   - **C1-GROK (xAI Grok Build CLI) is the primary flat-rate executor** (replaced Cursor 2026-06-14).
     `grok -p --always-approve --output-format plain` = headless single-turn, auto-approves all tool
     calls (mirrors the old Cursor `--force`). Auth = SuperGrok subscription via one-time `grok login`
     (browser OAuth, creds in `~/.grok/auth.json`); the router pre-checks that file and fast-fails
     (exit 75) if absent rather than hanging on the welcome screen. **Beta access is gated to SuperGrok
     Heavy / X Premium Plus** — if `--selftest-grok` rejects, the tier may not cover the CLI.
     **⚠️ Grok is a CLOUD agent — repo-upload guard (enforced by the script):** on session start it
     bulk-uploads a whole-repo "reference snapshot" to xAI GCS. In C:\Bari that is ~800MB of the
     `02_products` tree — it hangs the lane AND exfiltrates the proprietary Agent OS brain. Grok defaults
     to `codebase_indexing=true`, and an update/re-login can reset the config back to it. The router now
     **self-heals before every dispatch** (`_ensure_grok_hardening`): it asserts `~/.grok/config.toml`
     has `[features] codebase_indexing=false` + `[tools] respect_gitignore=true`, repairs it if drifted,
     forces `GROK_RESPECT_GITIGNORE=1` in env, and **fails closed (exit 75, no dispatch) if it can't
     confirm the guard** — the repo is never sent to the cloud on an unverified config. Residual: files a
     task *touches* still reach xAI's server-side model
     (same risk class as the old Cursor lane / Claude itself) — scope dispatch cwd to the smallest
     needed subtree, and never route a task that must not leave the building to any cloud lane.
   - **C2 (DeepSeek)** for mechanical JSON/data passes (count recompute, string sanitization,
     field-strip, tallies). The run_005 cycle ran ~90% C1 with C2/Cursor/Gemini dark — the exact
     failure this rule names. If you find yourself scripting a mechanical pass inline, that was a C2.

## Token-optimization rules (always on, quality never compromised)

1. **Orchestrator orchestrates.** No execution in main context; only dispatch
   summaries + verification evidence land here. Start fresh chats per phase; durable
   state = registry + board + memory.
2. **Crisp DoD = cheap verification.** Every prompt's return format demands
   file:line-checkable claims, so orchestrator verification (the unavoidable Claude
   spend) is a lookup, not an investigation.
3. **No model overrides on dispatch.** Agent frontmatter picks the model (C1);
   Cursor defaults to its auto model — pin `--model` per dispatch type only if quality
   drifts on calibration runs.
4. **Bootstraps reference files, never inline them.** The Cursor/C2 dispatch points at
   the prompt file; prompts point at repo docs instead of copying them (also keeps
   Cursor's rules-budget under their recommended 500-line ceiling).
5. **Subscriptions are flat but rate-limited** — don't dump C2-grade grunt work on
   Cursor; that wastes its quota without saving anything.
6. **Verification is never skipped to save tokens.** All lanes return
   RETURNED-UNVERIFIED; the orchestrator closes on evidence. This is the quality
   floor under every optimization above.

## Hard rules carried by every lane

OFF ban (absolute, TASK-238) · frozen invariants untouchable · registry first ·
return contract on every dispatched prompt · domain agents propose RETURNED, never
CLOSED.
