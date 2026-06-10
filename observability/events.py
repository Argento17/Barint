"""
Bari LLM Observability Events — structured event logging for AI-assisted workflows.

Canonical schema: 01_framework/events/llm_event_schema_v1.md
Event log:        BARI_EVENTS_LOG env var or observability/events.jsonl

Usage:
    from observability.events import emit_event, EventBuilder

    # One-shot emit
    emit_event("llm_request_started", task_id="TASK-219", model="deepseek-chat")

    # Builder for rich events
    event = (EventBuilder("bari_score_calculation_completed")
        .with_task_id("TASK-219")
        .with_agent("bsip2-engine")
        .with_product_id("hc-001")
        .with_status("success")
        .with_latency_ms(3420)
        .build())
    emit_event(event)

Design principles:
- NEVER logs raw prompts, raw outputs, private data, or full product text
- Uses hashes for prompt/output traceability
- Append-only JSONL — no mutation, no deletion
- Configurable log path via BARI_EVENTS_LOG env var
"""
from __future__ import annotations

import datetime
import hashlib
import json
import os
import pathlib
import time
import threading
from typing import Any, Optional

# ---------------------------------------------------------------------------
# Canonical event names
# ---------------------------------------------------------------------------
EVENT_LLM_REQUEST_STARTED      = "llm_request_started"
EVENT_LLM_REQUEST_COMPLETED    = "llm_request_completed"
EVENT_LLM_REQUEST_FAILED       = "llm_request_failed"
EVENT_LLM_OUTPUT_RATED         = "llm_output_rated"
EVENT_LLM_TASK_COMPLETED       = "llm_task_completed"

EVENT_SCORE_CALCULATION_STARTED  = "bari_score_calculation_started"
EVENT_SCORE_CALCULATION_COMPLETED = "bari_score_calculation_completed"
EVENT_SCORE_CALCULATION_FAILED    = "bari_score_calculation_failed"

EVENT_AGENT_TASK_STARTED   = "bari_agent_task_started"
EVENT_AGENT_TASK_RETURNED  = "bari_agent_task_returned"
EVENT_AGENT_TASK_CLOSED    = "bari_agent_task_closed"

ALL_EVENT_NAMES: frozenset = frozenset({
    EVENT_LLM_REQUEST_STARTED,
    EVENT_LLM_REQUEST_COMPLETED,
    EVENT_LLM_REQUEST_FAILED,
    EVENT_LLM_OUTPUT_RATED,
    EVENT_LLM_TASK_COMPLETED,
    EVENT_SCORE_CALCULATION_STARTED,
    EVENT_SCORE_CALCULATION_COMPLETED,
    EVENT_SCORE_CALCULATION_FAILED,
    EVENT_AGENT_TASK_STARTED,
    EVENT_AGENT_TASK_RETURNED,
    EVENT_AGENT_TASK_CLOSED,
})

# ---------------------------------------------------------------------------
# Required field names (the canonical schema)
# ---------------------------------------------------------------------------
REQUIRED_FIELDS: tuple = (
    "event_name", "timestamp", "task_id", "agent_name", "workflow_name",
    "product_id", "comparison_id", "prompt_version_id", "model",
    "input_hash", "output_hash", "status", "latency_ms",
    "estimated_cost_usd", "error_type", "error_message",
    "review_result", "reviewer_agent", "environment",
)

# ---------------------------------------------------------------------------
# Default event log path
# ---------------------------------------------------------------------------
_DEFAULT_LOG_PATH = pathlib.Path(__file__).resolve().parent / "events.jsonl"
_LOG_PATH = pathlib.Path(os.environ.get("BARI_EVENTS_LOG", str(_DEFAULT_LOG_PATH)))
_LOG_LOCK = threading.Lock()
_MAX_LOG_BYTES = 100 * 1024 * 1024  # 100 MB rotate threshold

# ---------------------------------------------------------------------------
# Hashing helpers (privacy-safe — never raw content)
# ---------------------------------------------------------------------------

def input_hash(text: str, length: int = 16) -> Optional[str]:
    if not text:
        return None
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:length]


def output_hash(text: str, length: int = 16) -> Optional[str]:
    if not text:
        return None
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:length]


def _now_iso() -> str:
    return datetime.datetime.now(datetime.UTC).isoformat().replace("+00:00", "Z")


def _detect_environment() -> str:
    return os.environ.get("BARI_ENV", "development")


# ---------------------------------------------------------------------------
# Event builder
# ---------------------------------------------------------------------------

class EventBuilder:
    """Fluent builder for constructing event dicts.

    Only ``event_name`` is required. Every event auto-gets ``timestamp``
    and ``environment`` if not explicitly set.

    Usage:
        event = (EventBuilder("llm_request_started")
            .with_task_id("TASK-219")
            .with_model("gpt-4o")
            .build())
    """

    def __init__(self, event_name: str) -> None:
        if event_name not in ALL_EVENT_NAMES:
            raise ValueError(
                f"Unknown event name {event_name!r}. "
                f"Known: {sorted(ALL_EVENT_NAMES)}"
            )
        self._data: dict[str, Any] = {
            "event_name": event_name,
            "timestamp": _now_iso(),
            "environment": _detect_environment(),
        }

    def with_task_id(self, value: str) -> EventBuilder:
        self._data["task_id"] = value; return self

    def with_agent(self, value: str) -> EventBuilder:
        self._data["agent_name"] = value; return self

    def with_workflow(self, value: str) -> EventBuilder:
        self._data["workflow_name"] = value; return self

    def with_product_id(self, value: str) -> EventBuilder:
        self._data["product_id"] = value; return self

    def with_comparison_id(self, value: str) -> EventBuilder:
        self._data["comparison_id"] = value; return self

    def with_prompt_version(self, value: str) -> EventBuilder:
        self._data["prompt_version_id"] = value; return self

    def with_model(self, value: str) -> EventBuilder:
        self._data["model"] = value; return self

    def with_input_hash(self, value: str) -> EventBuilder:
        self._data["input_hash"] = value; return self

    def with_output_hash(self, value: str) -> EventBuilder:
        self._data["output_hash"] = value; return self

    def with_status(self, value: str) -> EventBuilder:
        self._data["status"] = value; return self

    def with_latency_ms(self, value: float) -> EventBuilder:
        self._data["latency_ms"] = round(value, 1); return self

    def with_estimated_cost_usd(self, value: float) -> EventBuilder:
        self._data["estimated_cost_usd"] = round(value, 6); return self

    def with_error(self, error_type: str, error_message: str) -> EventBuilder:
        self._data["error_type"] = error_type
        self._data["error_message"] = error_message
        return self

    def with_review(self, result: str, reviewer: str) -> EventBuilder:
        self._data["review_result"] = result
        self._data["reviewer_agent"] = reviewer
        return self

    def with_timestamp(self, value: str) -> EventBuilder:
        self._data["timestamp"] = value; return self

    def with_environment(self, value: str) -> EventBuilder:
        self._data["environment"] = value; return self

    def set(self, key: str, value: Any) -> EventBuilder:
        self._data[key] = value; return self

    def build(self) -> dict[str, Any]:
        return dict(self._data)

    def emit(self, log_path: Optional[str | pathlib.Path] = None) -> dict[str, Any]:
        event = self.build()
        _write_event(event, log_path=log_path)
        return event


# ---------------------------------------------------------------------------
# Emitter
# ---------------------------------------------------------------------------

def emit_event(
    event_or_name: str | dict[str, Any],
    log_path: Optional[str | pathlib.Path] = None,
    **kwargs: Any,
) -> dict[str, Any]:
    """Emit a single event to the JSONL log.

    Two calling conventions:

    1. ``emit_event(event_dict)`` — pass a pre-built dict.
    2. ``emit_event(event_name, task_id=..., model=...)`` — name + kwargs.
    """
    if isinstance(event_or_name, dict):
        event = event_or_name
        name = event.get("event_name")
        if name not in ALL_EVENT_NAMES:
            raise ValueError(
                f"Unknown event name {name!r}. "
                f"Known: {sorted(ALL_EVENT_NAMES)}"
            )
    else:
        builder = EventBuilder(event_or_name)
        for key, value in kwargs.items():
            builder.set(key, value)
        event = builder.build()

    _write_event(event, log_path=log_path)
    return event


def _resolve_log_path(log_path: Optional[str | pathlib.Path] = None) -> pathlib.Path:
    """Resolve log path: explicit arg > BARI_EVENTS_LOG > _LOG_PATH > default."""
    if log_path is not None:
        return pathlib.Path(log_path)
    env = os.environ.get("BARI_EVENTS_LOG")
    if env:
        return pathlib.Path(env)
    return _LOG_PATH


def _write_event(event: dict[str, Any], log_path: Optional[str | pathlib.Path] = None) -> None:
    """Append one JSON line to the event log. Thread-safe."""
    path = _resolve_log_path(log_path)
    line = json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n"

    with _LOG_LOCK:
        _maybe_rotate(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "a", encoding="utf-8") as f:
            f.write(line)


def _maybe_rotate(path: pathlib.Path) -> None:
    """Rotate log when it exceeds _MAX_LOG_BYTES."""
    try:
        if path.exists() and path.stat().st_size >= _MAX_LOG_BYTES:
            rotated = path.with_suffix(f".{_now_iso().replace(':', '-')}.jsonl")
            path.rename(rotated)
    except OSError:
        pass  # best-effort rotation; don't crash on emit


def set_log_path(path: str | pathlib.Path) -> None:
    global _LOG_PATH
    _LOG_PATH = pathlib.Path(path)


# ---------------------------------------------------------------------------
# Batch / context helpers
# ---------------------------------------------------------------------------

class EventContext:
    """Context manager that emits ``_started`` / ``_completed`` paired events.

    Usage:
        with EventContext("bari_score_calculation", task_id="TASK-219",
                          product_id="hc-001") as ctx:
            result = run_scoring(...)
            ctx.set("output_hash", output_hash(result))
    """

    def __init__(self, event_base_name: str, **kwargs: Any):
        self._start_event = event_base_name + "_started"
        self._end_event = event_base_name + "_completed"
        self._fail_event = event_base_name + "_failed"
        self._kwargs = kwargs
        self._start_time: Optional[float] = None

    def __enter__(self) -> EventContext:
        self._start_time = time.monotonic()
        emit_event(self._start_event, **self._kwargs)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        latency = (time.monotonic() - self._start_time) * 1000 if self._start_time else 0
        if exc_type is not None:
            emit_event(
                self._fail_event,
                status="failed",
                latency_ms=latency,
                error_type=exc_type.__name__,
                error_message=str(exc_val),
                **self._kwargs,
            )
        else:
            emit_event(
                self._end_event,
                status="success",
                latency_ms=latency,
                **self._kwargs,
            )

    def set(self, key: str, value: Any) -> None:
        self._kwargs[key] = value


def emit_score_event(
    status: str,
    task_id: str,
    product_id: str,
    score: Optional[float] = None,
    grade: Optional[str] = None,
    latency_ms: Optional[float] = None,
    error: Optional[tuple[str, str]] = None,
    log_path: Optional[str | pathlib.Path] = None,
    **extra: Any,
) -> dict[str, Any]:
    """Convenience for score-calculation events.

    - status "started" → ``bari_score_calculation_started``
    - status "success" → ``bari_score_calculation_completed``
    - otherwise        → ``bari_score_calculation_failed``

    ``log_path`` is never written into the event payload.
    """
    event_name = {
        "started": EVENT_SCORE_CALCULATION_STARTED,
        "success": EVENT_SCORE_CALCULATION_COMPLETED,
    }.get(status, EVENT_SCORE_CALCULATION_FAILED)

    builder = EventBuilder(event_name)
    builder.with_task_id(task_id).with_product_id(product_id)
    builder.with_status(status)
    if score is not None:
        builder.set("final_score", score)
    if grade is not None:
        builder.set("grade", grade)
    if latency_ms is not None:
        builder.with_latency_ms(latency_ms)
    if error is not None:
        builder.with_error(*error)

    for k, v in extra.items():
        builder.set(k, v)

    return builder.emit(log_path=log_path)


def read_events(
    event_name: Optional[str] = None,
    task_id: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 100,
    log_path: Optional[str | pathlib.Path] = None,
) -> list[dict[str, Any]]:
    """Read recent events from the JSONL log with optional filters."""
    path = _resolve_log_path(log_path)
    if not path.exists():
        return []

    events: list[dict[str, Any]] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                ev = json.loads(line)
            except json.JSONDecodeError:
                continue
            if event_name and ev.get("event_name") != event_name:
                continue
            if task_id and ev.get("task_id") != task_id:
                continue
            if status and ev.get("status") != status:
                continue
            events.append(ev)

    return events[-limit:]
