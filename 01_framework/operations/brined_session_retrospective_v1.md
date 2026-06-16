# Brined-Cheeses Factory Run — Session Retrospective v1

**Date:** 2026-06-13 · **Author:** Orchestrator (Opus) · **Scope:** the brined/salty-cheeses
factory run + the C3-lane build + the Stage-9 remediation chain (post-compaction half of the session).

---

## 1. What went right / wrong / what to codify

### Went RIGHT (the prior codifications paid off)
1. **C3 became a real programmatic lane and immediately earned its keep.** Built it into
   `dispatch.py` (route `C3` → `openai/gpt-5.5` via opencode), proved it (P51 PONG), and on its
   FIRST real use (P52) it caught a **fabricated methodology line** ("salt stays in brine / isn't
   eaten") that all internal agents had passed. This validates the owner's instinct: an
   outside-the-family read catches what the family rationalizes.
2. **Healthy lane distribution** — C3×1, C1×4, C1-CURSOR×2, orchestrator = verify-only. The
   anti-laziness codification (`feedback_lane_routing_antilaziness`) held: no 100%-C1 collapse.
3. **Returns were trustworthy this time** — the return-contract hardening
   (`feedback_return_self_verifying`, rules 5-8) worked. Every return carried full distributions +
   trace-derived counts; my independent re-derivation matched the agents' self-reports (vs the prior
   session where they were wrong twice). Verification was confirmation, not correction.
4. **Stage-9 red-team caught real defects I missed** — bc-031 `B/73` vs score 72, and it correctly
   forced the `מלח (27%)` question to a raw-scrape investigation. The "auto-red-team, never hand the
   owner an un-torn-apart page" rule produced exactly the catch it exists for.
5. **Honesty held under pressure** — the fiber-confidence fix shipped with a verified honesty guard
   (the 15 genuinely-incomplete products stayed partial; only the 30 false-partials moved).

### Went WRONG / friction
1. **Slow — the dominant problem.** ~34 min of delegated wall-clock, run mostly SEQUENTIALLY
   (Content → re-render → red-team → [Nutrition∥Data] → confidence-fix → verify). Only ONE parallel
   pair in the whole chain.
2. **TWO render cycles where ONE would do.** Sequence was: copy-fix → re-render(P53) → red-team →
   more fixes → confidence-recompute(P54). Had the red-team run on the copy-fixed page FIRST and
   surfaced ALL findings at once, a single consolidated remediation + single re-render would have
   replaced two render passes and an extra verify loop.
3. **The brined page is hand-built, not generator output** — discovered LATE (via the Nutrition
   agent noticing `sub_reason:"partial_field"` ≠ what `generate_page.py` emits). Because Stage 8
   (`render_local_page`, TASK-268) isn't generalized yet, every brined render was semi-manual
   (Cursor mapping copy→VM by hand). This is the ROOT CAUSE of the multi-cycle slowness — there's no
   one-command re-render, so each change is a bespoke dispatch.
4. **Incomplete first-pass scoping.** Content removed `מלח (27%)` from the insightLine but it lived
   in the ingredients data field — so it survived to the red-team. A fix that doesn't trace the
   string to ALL its homes is a half-fix that costs a later cycle.
5. **bc-id drift, again.** Agents referenced `bc-NN` labels that don't map cleanly to barcodes;
   keyed-by-barcode data saved correctness, but the prose confusion recurs every session.
6. **Heavy C1 agents carried mechanical sub-work.** Content spent a chunk of its 68 tool calls on
   superlative trace-verification (mechanical lookups) — judgment-agent time spent on grunt work.

### To CODIFY
- **C-1 · "Render once → red-team once → consolidated remediation → re-render once."** Never
  fix-then-render-then-red-team-then-fix-then-render. Render the page, red-team the WHOLE thing,
  bundle every finding, fix in parallel by domain, re-render once, re-verify once. (Targets WRONG #2.)
- **C-2 · Parallel-by-default for independent workstreams.** If two dispatches don't share files or a
  dependency, they fire in the SAME turn. Sequential is the exception, justified by a real dependency.
  (Targets WRONG #1.)
- **C-3 · A fix must trace its target string to EVERY artifact it lives in** (copy source + rendered
  JSON + data field) before it's "done." Grep the whole tree, not just the obvious field. (WRONG #4.)
- **C-4 · Strip mechanical sub-tasks out of C1 judgment agents.** Pre-compute the trace facts
  (superlative checks, counts) as a script/C2 and hand the agent the table, so C1 spends tokens only
  on judgment. (WRONG #6 + speed.)
- **C-5 · Generalize Stage 8 (`render_local_page`, TASK-268) is now a SPEED blocker, not just a
  tidiness goal** — promote its priority. A one-command re-render kills the per-change bespoke
  dispatch. (WRONG #3.)

---

## 2. Routing, lane distribution, tokens, modifications

### Lane ledger (this session, post-compaction)
| Lane | Dispatches | Claude tokens | Agent wall-clock | Notes |
|---|---|---|---|---|
| Orchestrator (Opus) | — | unmetered* | — | verification only; ~45 tool calls, 1 compaction |
| C1 native (Sonnet subagents) | 4 | **404,988** | ~26.5 min | Content, Red-Team, Nutrition, Data |
| C1-CURSOR (flat-rate) | 2 | 0 | ~4.7 min | re-render, confidence fix |
| C3 (OpenAI via opencode) | 2 | 0 | ~2.5 min | copy review + selftest |

\*Orchestrator tokens aren't directly metered; load was dominated by large agent returns landing in
context (the 149K-token Content return, the red-team return, etc.) + one compaction. Honest estimate:
the orchestrator's own generation was a minority of total spend; the **C1 native lane (~405K tokens)
was the cost center.**

### Per-C1-agent detail
| Agent | Tokens | Tool calls | Wall-clock | Tokens/min |
|---|---|---|---|---|
| Content remediation | 149,524 | 68 | 12.5 min | ~12.0K |
| Red-Team | 110,373 | 27 | 7.3 min | ~15.1K |
| Data | 91,363 | 35 | 4.0 min | ~22.8K |
| Nutrition | 53,728 | 13 | 2.6 min | ~20.7K |

### What the numbers say
- **C1-CURSOR is 3-11× faster AND ~free vs C1 native** for comparable file-edit work (P54 confidence
  recompute = 67s flat-rate vs any C1 agent at 150-750s + tokens). Every spec-complete edit kept on
  C1 native is paying twice — money and time.
- **Content (149K tok, 68 tools, 12.5 min) is the single heaviest node** and was ~30% mechanical
  (superlative verification). That 30% belongs on a script.
- **C3 cost ≈ zero to the Claude budget** and delivered the highest-leverage single catch of the
  session. Under-using it is leaving free quality on the table.

### Modifications needed
- **M-1 · Move the mechanical half of judgment dispatches to C2/script.** Pre-compute trace tables
  (superlatives, distributions, null-field maps) and pass them in; C1 returns judgment only.
- **M-2 · Default spec-complete edits to C1-CURSOR, harder.** The bar for keeping an edit on C1
  native should be "this genuinely needs Bari persona/memory/judgment mid-edit," not "it touches
  governed data." (P54 proved a fully-specified data transform runs clean + fast on Cursor.)
- **M-3 · Cap C1-agent tool-call budgets in the prompt.** Content at 68 tool calls signals scope
  bleed; give agents a pre-built evidence packet so they don't re-derive the corpus.
- **M-4 · Keep C3 in the standard loop, not as a special event.** It's free and programmatic now —
  a fresh-eyes pass before any page is declared owner-ready should be routine.

---

## 3. Speed — why it was slow and how to make it fast

### Root causes (in order of impact)
1. **Sequential dependency chain with one parallel pair.** ~34 min of delegated wall-clock ran
   nose-to-tail. The critical path was: Content(12.5) → re-render(3.6) → red-team(7.3) →
   Nutrition∥Data(4.0) → confidence-fix(1.1) → verify ≈ 28+ min just in agent time, plus my verify
   loops between each.
2. **No one-command re-render (Stage 8 not generalized).** Each render was a bespoke C1-CURSOR
   dispatch with a hand-written spec. Two of them. With a generator, re-render is seconds and needs
   no prompt authoring.
3. **Two render cycles** from fix-render-redteam-fix-render ordering (see C-1).
4. **Cold-start re-derivation.** Each subagent boots fresh and re-reads the corpus/trace. The Content
   agent re-derived superlatives the run record already knew.

### Optimization plan (concrete, ranked by payoff)
- **S-1 · Adopt the "render→red-team→consolidate→render" macro (C-1).** Collapses 2 render cycles +
  2 verify loops into 1 each. Biggest single win on this exact workflow. **Est. −8-10 min.**
- **S-2 · Parallelize by default (C-2).** Content's copy fix and a FIRST deterministic red-team pass
  on the un-fixed page could overlap; Nutrition∥Data proved the pattern works. Fire every independent
  dispatch in one turn. **Est. −5-7 min.**
- **S-3 · Generalize Stage 8 render (TASK-268) and prioritize it.** Turns every re-render from a
  3-4 min bespoke dispatch into a seconds-long script call, and removes prompt-authoring latency.
  **Est. −3-4 min per render cycle, compounding every future shelf.**
- **S-4 · Hand C1 agents a pre-built evidence packet** (trace table, distributions, null-map) so they
  spend tool calls on judgment, not corpus re-derivation. Shrinks the heaviest nodes. **Est. −2-4 min
  on Content-class agents + fewer tokens.**
- **S-5 · Batch my own verification** into fewer, denser scripts (one Stage-9 deterministic script vs
  several Bash calls). Minor wall-clock, but reduces round-trips. **Est. −1-2 min.**
- **S-6 · Route the mechanical to the fast lanes.** Cursor (fast, flat) and C2 (free) for anything
  spec-complete or mechanical; reserve slow metered C1 for true judgment. Both cheaper AND faster.

### The headline
The slowness was **structural, not effort** — a sequential chain over a not-yet-automated render
stage. The two highest-payoff fixes are **(a) the render→red-team→consolidate→render macro** and
**(b) parallel-by-default**, together roughly halving the wall-clock without losing a single
verification gate. The durable fix underneath both is **finishing Stage 8 (TASK-268)** so re-render
stops being a hand-built dispatch.

---

## Action items
- [ ] Codify C-1…C-5 into `lane_routing_rules_v1.md` + a new "remediation macro" section.
- [ ] Promote **TASK-268** (Stage 8 render generalization) — reclassify as a speed blocker.
- [ ] Apply M-1…M-4 to the next shelf run as a live test of the optimizations.
- [ ] Memory updates: extend `feedback_lane_routing_antilaziness` with the parallel-by-default +
      mechanical-off-C1 rules; note C3-is-programmatic everywhere it's referenced.
