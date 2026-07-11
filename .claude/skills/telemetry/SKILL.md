---
name: telemetry
description: Produce a Bari orchestrator after-action audit — lane ledger, inline-vs-delegated split, pace/consumption, error origin-vs-catch, and quantified corrective actions. Use after any tracked run to measure the SYSTEM, not the deliverable.
---

# /telemetry — Orchestrator after-action audit

**Owner ruling (2026-06-14).** An audit answers *how efficient was the system, where was it
not, where did errors originate vs. get caught, and what we change* — backed by router/lane
telemetry (tokens, tool-calls, wall, outcome). It is about the **machine, not the product**.
Standard: `01_framework/operations/orchestrator_audit_standard_v1.md`.

> The "what shipped / grades / gate results" summary belongs in the **task registry
> `close_reason`**, NOT here. If you're listing deliverables, you're writing the wrong doc.

## Use this when
- "Audit that run", "telemetry", "after-action report", end of any tracked `/orchestrate` loop
  or factory run. Auto-emit alongside any delivered page.

## Mandatory sections (in order — a gap you can't fill IS a finding)
1. **Run header** — task, directive verbatim, date, phases, disposition (≤5 lines).
2. **Lane ledger** — one row per dispatch **and per inline orchestrator step**:
   `# · stage · lane(band) · engine/agent · what · tokens · tool-calls · wall(s) · outcome`.
   Inline work with no token count = `UNTRACKED` (a red flag, never a blank — untracked inline
   work is the #1 thing this audit exists to surface).
3. **Inline-vs-delegated split** — % value inline vs delegated, by phase. **Name any delegable
   work done inline** and why. Inline is justified ONLY for irreducible coordination, first-pass
   pattern discovery, and the pixel review; repeats / spec-complete adapters / parallel builds
   MUST be delegated. Flag the "novel diagnostic build" over-claim by name if it happened.
4. **Pace & consumption** — total dispatches / subagent tokens / tool-calls / wall; sequential
   vs parallelizable; **rework tokens + rework %**; biggest token sink + biggest *avoidable* one.
5. **Error ledger** — one row per defect: `defect · origin-stage · catch-stage · detection-lag ·
   fix-cost`. Sort by lag desc. **Detection lag = catch − origin** is the headline metric; an
   owner-caught defect is lag = ∞ and flagged red.
6. **Corrective actions** — one per finding, tied to a ledger row, each with an **expected
   saving** (tokens / passes / stages of lag removed). Concrete pipeline changes only — no
   "do better". Mark which are implemented.
7. **Consumption verdict** — 2–4 sentences: was it efficient, where did tokens go, the single
   highest-ROI change next run. End with the headline ratio (e.g. "30% of delegated tokens were
   avoidable rework").
8. **Skill-edit proposals (the self-improvement step — added 2026-07-04, TASK-505).** The audit
   is incomplete until its findings flow BACK into the system files. For each corrective action
   in §6, answer: *which SKILL.md / agent .md / hook / C0 gate would have prevented this class of
   error?* Emit a concrete proposed diff (file + section + exact replacement text) — not "do
   better" prose. Rules: (a) reversible skill/agent text edits within your lane → APPLY them now
   and list them as applied; (b) edits touching governance, scoring philosophy, or another
   agent's lane law → file the proposed diff in the report and route to the owning agent;
   (c) an error class that recurs across two audits without its proposed edit applied = a
   process failure, flag it red. This closes the loop the 2026 pattern calls "self-improving
   skills": telemetry measures, then the measured lesson gets codified where the next run will
   actually read it.

## Capture discipline (so the data exists)
- Record `subagent_tokens / tool_uses / duration_ms / outcome` **at each Agent return** — never
  reconstruct later.
- Estimate inline tokens (phase length × rate) when exact counts are unavailable — invisible
  cost is unmanaged cost.
- Lane preflight before dispatch; flag lane-laziness if C2 / C1-CURSOR were dark.

## Output
`02_products/<category>/reports/factory_runN_orchestrator_report_v1.md` (or the run's report
dir). Also valid as a standalone audit of an `/orchestrate` session.

> For a machine-wide view of your *own* Claude Code usage over time (not a single run), see the
> History Analyzer at `03_operations/cc_history_analyzer/` (`python analyze.py`).

## Related
`/orchestrate`, `/roadmap`, `rescore`, `build-page`.
