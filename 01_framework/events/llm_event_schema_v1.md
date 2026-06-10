# Bari LLM Observability Event Schema v1

Canonical specification for structured event logging across all Bari AI-assisted
workflows: scoring engine, editorial generation, and agent orchestration.

**Schema version:** 1.0  
**Implementation:** `C:\Bari\observability\events.py`  
**Event log:** `observability/events.jsonl` (overridable via `BARI_EVENTS_LOG` env var)  
**Author:** TASK-219

---

## 1. Canonical Event Names

| Event name | When emitted | Typical emitter |
|---|---|---|
| `llm_request_started` | An LLM API call is dispatched (prompt sent) | editor, agent, scoring wrapper |
| `llm_request_completed` | LLM API call returns successfully | editor, agent, scoring wrapper |
| `llm_request_failed` | LLM API call fails (timeout, 4xx, 5xx, parse error) | editor, agent, scoring wrapper |
| `llm_output_rated` | Human or automated review scores the LLM output | reviewer, QA agent |
| `llm_task_completed` | A multi-step LLM workflow finishes (all sub-calls done) | orchestrator, workflow runner |
| `bari_score_calculation_started` | BSIP scoring pipeline starts for a single product | `score_engine.py` wrapper |
| `bari_score_calculation_completed` | BSIP scoring pipeline produces a result | `score_engine.py` wrapper |
| `bari_score_calculation_failed` | BSIP scoring pipeline errors out for a product | `score_engine.py` wrapper |
| `bari_agent_task_started` | An agent begins work on a TASK-XXX | orchestrator, CLI dispatch |
| `bari_agent_task_returned` | An agent completes and submits a return block | agent (RETURNED status) |
| `bari_agent_task_closed` | CC agent verifies and closes a task | cc-agent (CLOSED status) |

---

## 2. Field Specifications

All fields are **optional** at the JSONL level (sparse event, send what applies).
Only `event_name` and `timestamp` are truly required.

| Field | Type | Description | Privacy |
|---|---|---|---|
| `event_name` | string | One of the 11 canonical event names above | — |
| `timestamp` | string | ISO 8601 UTC (`2026-06-09T12:00:00Z`) | — |
| `task_id` | string | TASK-XXX identifier | — |
| `agent_name` | string | Emitting agent role (`bsip2-engine`, `content-editor`, `cc-agent`, etc.) | — |
| `workflow_name` | string | Workflow identifier (`batch_run_hard_cheeses_001`, `generate_category_description`, etc.) | — |
| `product_id` | string | Canonical product ID (`hc-001`, `snk-002`, etc.) | — |
| `comparison_id` | string | Category comparison ID (`hard_cheeses`, `milk`, etc.) | — |
| `prompt_version_id` | string | Version/prompt template identifier | — |
| `model` | string | LLM model name (`deepseek-chat`, `claude-sonnet-4`, etc.) | — |
| `input_hash` | string | `sha256(prompt)[:16]` — first 16 hex chars | **Safe** — hash only |
| `output_hash` | string | `sha256(output)[:16]` — first 16 hex chars | **Safe** — hash only |
| `status` | string | `started`, `success`, `failed`, `returned`, `closed`, `rated` | — |
| `latency_ms` | float | Wall-clock duration in milliseconds | — |
| `estimated_cost_usd` | float | Estimated LLM API cost in USD | — |
| `error_type` | string | Error class (`TimeoutError`, `APIError`, `ValueError`, etc.) | — |
| `error_message` | string | Short error summary (no prompt context) | **Safe** — no PII |
| `review_result` | string | Review verdict (`pass`, `warn`, `fail`, `changes_requested`) | — |
| `reviewer_agent` | string | Agent or human reviewer name | — |
| `environment` | string | `development`, `staging`, `production` (from `BARI_ENV`) | — |

### Custom fields

Events MAY include additional fields beyond the canonical 19. Examples:

- `final_score` (float) — for `bari_score_calculation_completed`
- `grade` (string) — grade letter A/B/C/D/E/S
- `confidence` (float) — score confidence 0–100
- `category` (string) — BSIP router category
- `nova_level` (integer) — NOVA proxy level
- `product_count` (integer) — for batch-summary events

Custom fields MUST NOT contain raw prompt text, raw model output, PII,
or full product ingredient/nutrition text.

---

## 3. Privacy Rules (Hard)

1. **NEVER** log raw prompts or raw LLM outputs.
2. **NEVER** log user PII, API keys, or environment secrets.
3. **NEVER** log full product ingredient text or full nutrition panels.
4. Use `input_hash` / `output_hash` for traceability instead of content.
5. `error_message` must be a short summary — no prompt context leakage.
6. Any field that would violate rules 1–5 must be excluded; if the event
   is meaningless without it, skip emitting the event.
7. Approved exceptions require a documented governance override
   (e.g., spot-check dataset with explicit Product Agent approval).

---

## 4. Example Payloads

### 4.1 Successful BSIP score generation

```json
{
  "event_name": "bari_score_calculation_completed",
  "timestamp": "2026-06-09T12:34:56Z",
  "task_id": "TASK-219",
  "agent_name": "bsip2-engine",
  "workflow_name": "batch_run_hard_cheeses_001",
  "product_id": "hc-015",
  "comparison_id": "hard_cheeses",
   "model": "deepseek-chat",
  "input_hash": "a1b2c3d4e5f6a7b8",
  "output_hash": "9a8b7c6d5e4f3a2b",
  "status": "success",
  "latency_ms": 4230.5,
  "estimated_cost_usd": 0.00215,
  "environment": "production",
  "final_score": 70.2,
  "grade": "B",
  "confidence": 84.0,
  "category": "hard_cheeses",
  "nova_level": 2
}
```

### 4.2 Failed editorial generation

```json
{
  "event_name": "llm_request_failed",
  "timestamp": "2026-06-09T14:20:00Z",
  "task_id": "TASK-220",
  "agent_name": "content-editor",
  "workflow_name": "generate_category_description",
  "product_id": "hc-022",
  "comparison_id": "hard_cheeses",
  "prompt_version_id": "cat-desc-v3",
  "model": "deepseek-chat",
  "input_hash": "b2c3d4e5f6a7b8c9",
  "status": "failed",
  "latency_ms": 30500.0,
  "estimated_cost_usd": 0.00850,
  "error_type": "TimeoutError",
  "error_message": "API timeout after 30s — model overloaded",
  "environment": "production"
}
```

### 4.3 QA returned task

```json
{
  "event_name": "bari_agent_task_returned",
  "timestamp": "2026-06-09T16:45:00Z",
  "task_id": "TASK-218",
  "agent_name": "qa-agent",
  "workflow_name": "qa-audit",
  "status": "returned",
  "latency_ms": 250000.0,
  "estimated_cost_usd": 0.000,
  "review_result": "changes_requested",
  "reviewer_agent": "cc-agent",
  "environment": "production",
  "product_count": 37
}
```

### 4.4 Score calculation anomaly

```json
{
  "event_name": "bari_score_calculation_failed",
  "timestamp": "2026-06-08T09:15:30Z",
  "task_id": "TASK-215",
  "agent_name": "bsip2-engine",
  "workflow_name": "batch_run_hard_cheeses_001",
  "product_id": "hc-030",
  "comparison_id": "hard_cheeses",
  "model": "deepseek-chat",
  "input_hash": "d4e5f6a7b8c9d0e1",
  "status": "failed",
  "latency_ms": 1580.0,
  "estimated_cost_usd": 0.00120,
  "error_type": "ValueError",
  "error_message": "Nutrition panel missing fat_g and protein_g — cannot compute base score",
  "environment": "production",
  "category": "hard_cheeses",
  "data_sufficiency": "insufficient"
}
```

---

## 5. Usage Guide

### 5.1 From BSIP2 scoring batch runners

Add to any `batch_run_*.py`:

```python
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(r"C:\Bari")))
from observability.events import emit_event, EventBuilder, emit_score_event

# Wrap per-product scoring
for product in products:
    pid = product.get("canonical_product_id", "unknown")
    try:
        emit_score_event("started", task_id="TASK-XXX", product_id=pid)
        t0 = time.monotonic()
        trace = run_pipeline(product)
        latency = (time.monotonic() - t0) * 1000
        emit_score_event("success", task_id="TASK-XXX", product_id=pid,
                         score=trace.get("final_score_estimate"),
                         grade=trace.get("grade_estimate"),
                         latency_ms=latency)
    except Exception as e:
        emit_score_event("failed", task_id="TASK-XXX", product_id=pid,
                         error=("PipelineError", str(e)))
```

### 5.2 From editorial/LLM generation workflows

```python
from observability.events import emit_event, EventBuilder

builder = EventBuilder("llm_request_started")
builder.with_task_id("TASK-220")
builder.with_agent("content-editor")
builder.with_workflow("generate_category_description")
builder.with_product_id("hc-022")
builder.with_prompt_version("cat-desc-v3")
builder.with_model("deepseek-chat")
builder.with_input_hash(input_hash(prompt_text))
start_event = builder.emit()
```

### 5.3 From agent orchestration (orchestrator / cc-agent)

```python
from observability.events import emit_event

emit_event("bari_agent_task_started",
           task_id="TASK-221",
           agent_name="cc-agent",
           workflow_name="cc-close-gate",
           status="started")

# ... do work ...

emit_event("bari_agent_task_closed",
           task_id="TASK-221",
           agent_name="cc-agent",
           workflow_name="cc-close-gate",
           status="closed",
           review_result="pass",
           reviewer_agent="cc-agent",
           latency_ms=total_ms)
```

### 5.4 Using EventContext (paired started/completed)

```python
from observability.events import EventContext

with EventContext("bari_score_calculation",
                  task_id="TASK-219",
                  product_id="hc-001",
                  agent_name="bsip2-engine") as ctx:
    trace = run_pipeline(product)
    ctx.set("final_score", trace.get("final_score_estimate"))
    ctx.set("grade", trace.get("grade_estimate"))
```

---

## 6. Reading Events

```python
from observability.events import read_events

# Last 10 failed score calculations
fails = read_events(
    event_name="bari_score_calculation_failed",
    status="failed",
    limit=10,
)

# All events for a specific task
task_events = read_events(task_id="TASK-219")
```
