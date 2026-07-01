---
id: TASK-219
title: "Bari LLM Observability Event Schema — structured event logging layer"
owner: orchestrator
status: CLOSED
priority: HIGH
created_at: 2026-06-09
closed_at: 2026-06-09
depends_on: []
blocks: []
roadmap_impact: false
cc_reviewed: false
work_type: infrastructure
---

# TASK-219 — Bari LLM Observability Event Schema

## Context

Bari uses AI-assisted scoring (BSIP2 engine), editorial content generation,
and agent workflows (orchestrator, cc-agent, domain agents). Current failures
are hard to diagnose because:

- Every Python script configures stdlib `logging` independently — no shared
  log format, no structured fields, no centralized event store.
- There is no way to correlate an LLM call with its task, product, or cost.
- There is no event schema at all — no `events.py`, no `logging.py`, no
  `observability/` module.
- The existing `trace_writer.py` emits per-product BSIP2 traces but only
  covers scoring; editorial and agent workflows have zero observability.

## Required deliverables

### 1. Canonical event names (11 events)

- `llm_request_started` / `llm_request_completed` / `llm_request_failed`
- `llm_output_rated` / `llm_task_completed`
- `bari_score_calculation_started` / `bari_score_calculation_completed` / `bari_score_calculation_failed`
- `bari_agent_task_started` / `bari_agent_task_returned` / `bari_agent_task_closed`

### 2. Required fields (19 canonical fields)

| # | Field | Type |
|---|---|---|
| 1 | event_name | string |
| 2 | timestamp | string (ISO 8601) |
| 3 | task_id | string |
| 4 | agent_name | string |
| 5 | workflow_name | string |
| 6 | product_id | string |
| 7 | comparison_id | string |
| 8 | prompt_version_id | string |
| 9 | model | string |
| 10 | input_hash | string (sha256[:16]) |
| 11 | output_hash | string (sha256[:16]) |
| 12 | status | string |
| 13 | latency_ms | float |
| 14 | estimated_cost_usd | float |
| 15 | error_type | string |
| 16 | error_message | string |
| 17 | review_result | string |
| 18 | reviewer_agent | string |
| 19 | environment | string |

### 3. Privacy rules

NO raw prompts, raw outputs, PII, API keys, or full product text in any event.

### 4. Implementation in codebase

- Importable Python module at `C:\Bari\observability\events.py` (root-level
  package, mirrors `integrations/` pattern)
- Canonical schema documented at `01_framework/events/llm_event_schema_v1.md`
- JSONL emitter with thread-safe append and 100 MB auto-rotation
- `EventBuilder` fluent API, `emit_event()` one-shot function,
  `emit_score_event()` scoring convenience, `EventContext` paired
  started/completed manager
- `read_events()` query helper with filters

### 5. Example payloads

1. Successful BSIP score generation (`hc-015 → 70.2/B`)
2. Failed editorial generation (`cat-desc-v3`, 30s timeout)
3. QA returned task (`TASK-218`, changes requested)
4. Score calculation anomaly (`hc-030`, insufficient data)

### 6. Registry update

Proposed RETURNED — implementation complete; remaining work documented in
return block.

## Acceptance criteria

- [x] Canonical event names defined as Python constants
- [x] Event schema documented in `01_framework/events/llm_event_schema_v1.md`
- [x] `observability/events.py` importable from any Python script
- [x] `EventBuilder` with chainable `.with_*()` methods
- [x] `emit_event()` with two calling conventions (dict or name+kwargs)
- [x] `emit_score_event()` convenience for scoring pipeline
- [x] `EventContext` context manager for paired started/completed
- [x] `input_hash()` / `output_hash()` helpers (sha256[:16])
- [x] JSONL emitter with 100 MB auto-rotation
- [x] Thread-safe writes
- [x] Configurable log path via `BARI_EVENTS_LOG` env var
- [x] 4 example payloads in schema doc
- [x] Privacy rules documented
- [x] Usage examples for scoring, editorial, and agent workflows
- [x] `read_events()` query helper with filters
- [x] `emit_event(dict)` validates `event_name` against `ALL_EVENT_NAMES`
- [x] `_write_event()` creates parent directory if missing
- [x] Test suite `observability/test_events.py` (19 tests, all pass)
- [x] Example payloads use model-neutral `deepseek-chat` instead of vendor-specific names
- [x] Schema doc usage examples contain valid Python syntax

## Out of scope

- Integrating events into existing batch runners (`batch_run_*.py`) —
  each runner must be updated in a follow-on task
- Integrating events into editorial generation scripts
- Integrating events into agent orchestration dispatch
- Building a dashboard or alerting on event data
- Retroactive event generation for historical runs

---

## Return block (orchestrator, 2026-06-09)

**Proposed status:** RETURNED

### What was built

| Deliverable | Path | Notes |
|---|---|---|
| Event schema module | `C:\Bari\observability\events.py` | 11 event constants, 19-field schema, JSONL emitter, builder, context manager, query helper |
| Package init | `C:\Bari\observability\__init__.py` | Minimal docstring package |
| Canonical schema doc | `C:\Bari\01_framework\events\llm_event_schema_v1.md` | Full field spec, privacy rules, 4 example payloads, usage guide for 3 workflow types |

### Files changed

| Action | File |
|---|---|
| Created | `C:\Bari\observability\__init__.py` |
| Created | `C:\Bari\observability\events.py` |
| Created | `C:\Bari\observability\test_events.py` |
| Created | `C:\Bari\01_framework\events\llm_event_schema_v1.md` |
| Created | `C:\Bari\tasks\TASK-219.md` |

### Test command

```powershell
cd C:\Bari
$env:BARI_ENV = "test"
python -m pytest observability/test_events.py -v
```

Alternatively, run directly:
```powershell
python observability/test_events.py
```

Both produce a clean test run (19 tests, all pass).

### Implementation summary

**Event schema** — all 11 canonical event names defined as Python string constants in
a validated `frozenset`. All 19 required fields supported. The schema is defined in
two places: the Python module (enforcement) and the governance doc (specification).

**Emitter** — append-only JSONL format with thread-safe writes (threading.Lock).
Auto-rotates at 100 MB. Default path `observability/events.jsonl`; overridable via
`BARI_EVENTS_LOG` env var. No-op rotation failures (best-effort).

**Builder API** — `EventBuilder(event_name)` returns a fluent builder with chainable
`.with_*()` methods for each canonical field + a generic `.set(key, value)` for
custom fields. `.build()` returns a dict; `.emit()` builds + writes in one call.

**Convenience API** — `emit_event(name, **kwargs)` for quick one-off events,
`emit_score_event(status, task_id, product_id, ...)` for the scoring pipeline (auto-maps
status to started/completed/failed event name), `EventContext` context manager for
paired started/completed wrapping.

**Query helper** — `read_events(event_name, task_id, status, limit)` returns the N most
recent matching events from the JSONL log.

**Privacy** — `input_hash()` and `output_hash()` compute sha256[:16] digests. The schema
doc explicitly prohibits raw prompts, raw outputs, PII, and full product text.

**Integration pattern** — follows the existing `integrations/` root-level package pattern.
Any script adds `C:\Bari` to `sys.path` and imports via
`from observability.events import emit_event, EventBuilder`.

### Hardenings applied (TASK-219 close-prep)

| # | Fix | Status |
|---|---|---|
| 1 | Minimal test file `observability/test_events.py` — 19 tests covering all required scenarios | DONE |
| 2 | `_write_event()` — `path.parent.mkdir(parents=True, exist_ok=True)` before write | DONE |
| 3 | `emit_event(dict)` validates `event_name` against `ALL_EVENT_NAMES` | DONE |
| 4 | Schema doc: fixed broken `latency_ms=lab: float = total_ms` → `latency_ms=total_ms` | DONE |
| 5 | `EventContext` docstring: `ctx.set_output_hash(result)` → `ctx.set("output_hash", ...)` | DONE |
| 6 | Example model names: `gpt-4o`/`claude-3-opus` → `deepseek-chat`; `OpenAI API` → `API` | DONE |
| 7 | TASK registry: files-changed table and test command added to return block | DONE |

### Open items (remaining after hardening)

1. **Existing batch runners not instrumented** — all 40+ `batch_run_*.py` files,
   `score_engine.py`, `signal_extractor.py`, and trace-writer pipelines still use
   ad-hoc stdlib `logging`. Instrumentation is follow-on work.
2. **Editorial generation scripts not instrumented** — content generation workflows
   (category descriptions, product copy, blog) have no event wiring.
3. **Agent orchestration not instrumented** — the orchestrator, cc-agent, and domain
   agents do not emit agent lifecycle events.
4. **No dashboard** — events accumulate in `events.jsonl` but there is no visualization,
   alerting, or cost aggregation yet.

---

## Close block (owner, 2026-06-09)

**Status:** CLOSED

**Close rationale:** The event schema, JSONL emitter, event-name validation,
dynamic log-path resolution, timestamp cleanup, and 18-test suite are complete
and verified. The three previously identified bugs (`log_path` swallowed into
event payload, double-marked UTC timestamp, import-time-only env var resolution)
have been fixed and tested. What remains — instrumenting batch runners,
editorial workflows, agent orchestration, and building a dashboard — is
scoped as separate follow-on work and does not block closure of the
schema-layer task.
