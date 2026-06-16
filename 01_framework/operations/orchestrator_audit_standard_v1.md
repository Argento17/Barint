# Orchestrator After-Action Audit — Standard v1
**Owner ruling 2026-06-14.** Supersedes the old "what landed" report format (rejected: it described the
deliverable, not the system). An orchestrator audit exists to answer **how efficient was the system, where
was it not, where did errors originate vs. get caught, and what we change** — backed by router/lane telemetry
(tokens, tool calls, wall time, outcome). If a section can't be filled with data, that gap is itself a finding.

The deliverable summary (what shipped, grades, gate results) belongs in the **task registry close_reason**, NOT
in the audit. The audit is about the machine, not the product.

---

## Mandatory sections (in order)

### 1. Run header
Task, directive (verbatim), date, phases, final disposition. ≤5 lines.

### 2. Lane Ledger — one row per dispatch + inline work
The core of the audit. Table columns:
`# · stage · lane (band) · engine/agent · what · tokens · tool-calls · wall(s) · outcome`
- **Every** subagent dispatch is a row (tokens/tools/wall come from the Agent return — capture them at return time).
- **Inline orchestrator work is a row too** — if tokens aren't measurable, write `UNTRACKED` and treat that as a red flag, not a blank. Untracked inline work is the #1 thing this audit exists to surface.
- `outcome` ∈ {accepted, superseded(rework), FAIL→fixed, aborted, owner-caught}.

### 3. Inline-vs-delegated split
% of work value done inline vs delegated, by phase. **Explicitly name any inline work that was delegable**
and why it wasn't delegated. The orchestrator-not-executor rule (`orchestrator_not_executor`) is the bar:
inline is justified ONLY for irreducible coordination + first-pass pattern discovery + the pixel review.
Repeats of a known pattern, spec-complete adapters, and parallelizable builds MUST be delegated. Over-claiming
the "novel diagnostic build" carve-out is the canonical violation — call it out by name when it happened.

### 4. Pace & consumption metrics
- Total dispatches; total subagent tokens; total tool-calls; total subagent wall-time.
- Sequential vs. parallelizable (how much of the wall-time was forced-serial by real dependencies vs. could
  have run in parallel).
- **Rework tokens** (sum of superseded/aborted dispatches) and **rework %** of total.
- Single biggest token sink, and single biggest *avoidable* token sink.

### 5. Error ledger — origin stage vs. catch stage
One row per defect: `defect · origin-stage · catch-stage · detection-lag (stages) · fix-cost (tokens/passes)`.
**Detection lag = catch-stage − origin-stage** is the headline efficiency metric: a defect born at stage 2 and
caught at stage 9 cost everything built in between. Sort by lag descending. A defect caught by the OWNER is
lag = ∞ (worst possible) and must be flagged red.

### 6. Corrective actions
One per finding, each tied to a ledger row, each with an **expected saving** (tokens / passes / stages of lag
removed). No generic "do better" — concrete pipeline/process changes only. Mark which are now implemented.

### 7. Consumption verdict
Two-to-four sentences: was this run efficient? Where did the tokens actually go? What is the one change with
the highest ROI for next run? End with the run's headline efficiency ratio (e.g. "30% of delegated tokens were
avoidable rework").

---

## Capture discipline (so the data exists next time)
- **At every Agent return**, record `subagent_tokens / tool_uses / duration_ms / outcome` into the ledger
  immediately — do not reconstruct later.
- **Time-box inline diagnostic loops** (≈20 min). When the pattern is proven, STOP and delegate the repeats.
- **Capability preflight before dispatch**: confirm the target lane actually has the tool (don't send image-gen
  to a text-only agent — that's an aborted-dispatch token waste).
- **Estimate inline tokens** even when exact counts are unavailable (phase length × rate) so inline cost is never
  invisible. Invisible cost is unmanaged cost.

## Anti-patterns this standard kills
- A report that lists grades/gates/what-shipped and calls itself an audit. (That's a close_reason.)
- "~95% orchestrator-inline" stated as a fact with no token data and a hand-wave justification.
- No per-lane telemetry. No rework accounting. No origin-vs-catch error analysis. No quantified actions.
