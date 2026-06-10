"""
Tests for observability/events.py — Bari LLM observability event schema.

Run: python -m pytest observability/test_events.py -v
     (or: python observability/test_events.py)
"""
from __future__ import annotations

import json
import os
import pathlib
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from observability.events import (
    ALL_EVENT_NAMES,
    EventBuilder,
    EventContext,
    emit_event,
    emit_score_event,
    input_hash,
    output_hash,
    read_events,
    set_log_path,
)


class TestEventSchema(unittest.TestCase):

    def test_import_succeeds(self):
        self.assertIsInstance(ALL_EVENT_NAMES, frozenset)
        self.assertEqual(len(ALL_EVENT_NAMES), 11)

    def test_valid_event_emits_to_temp_jsonl(self):
        with tempfile.TemporaryDirectory() as tmp:
            log = pathlib.Path(tmp) / "events.jsonl"
            ev = emit_event("llm_request_started", task_id="T-1", log_path=str(log))
            self.assertEqual(ev["event_name"], "llm_request_started")
            self.assertEqual(ev["task_id"], "T-1")
            self.assertTrue(log.exists())
            lines = log.read_text(encoding="utf-8").strip().splitlines()
            self.assertEqual(len(lines), 1)
            parsed = json.loads(lines[0])
            self.assertEqual(parsed["event_name"], "llm_request_started")

    def test_invalid_event_name_raises_value_error(self):
        with self.assertRaises(ValueError):
            EventBuilder("nonexistent_event")

    def test_emit_event_dict_validates_event_name(self):
        with self.assertRaises(ValueError):
            emit_event({"event_name": "bad_name", "task_id": "T-1"})

    def test_emit_event_dict_valid_name_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            log = pathlib.Path(tmp) / "events.jsonl"
            ev = emit_event({"event_name": "llm_request_completed", "status": "success"}, log_path=str(log))
            self.assertEqual(ev["event_name"], "llm_request_completed")
            self.assertTrue(log.exists())

    def test_read_events_filters_by_event_name(self):
        with tempfile.TemporaryDirectory() as tmp:
            log = pathlib.Path(tmp) / "events.jsonl"
            emit_event("llm_request_started", task_id="T-1", log_path=str(log))
            emit_event("llm_request_completed", task_id="T-1", log_path=str(log))
            emit_event("bari_score_calculation_started", task_id="T-2", log_path=str(log))

            started = read_events(event_name="llm_request_started", log_path=str(log))
            self.assertEqual(len(started), 1)
            self.assertEqual(started[0]["event_name"], "llm_request_started")

    def test_read_events_filters_by_task_id(self):
        with tempfile.TemporaryDirectory() as tmp:
            log = pathlib.Path(tmp) / "events.jsonl"
            emit_event("llm_request_started", task_id="T-1", log_path=str(log))
            emit_event("llm_request_started", task_id="T-2", log_path=str(log))

            t1 = read_events(task_id="T-1", log_path=str(log))
            self.assertEqual(len(t1), 1)
            self.assertEqual(t1[0]["task_id"], "T-1")

    def test_read_events_filters_by_status(self):
        with tempfile.TemporaryDirectory() as tmp:
            log = pathlib.Path(tmp) / "events.jsonl"
            emit_event("llm_request_completed", task_id="T-1", status="success", log_path=str(log))
            emit_event("llm_request_failed", task_id="T-2", status="failed", log_path=str(log))

            fails = read_events(status="failed", log_path=str(log))
            self.assertEqual(len(fails), 1)
            self.assertEqual(fails[0]["status"], "failed")

    def test_event_context_emits_started_and_completed(self):
        with tempfile.TemporaryDirectory() as tmp:
            log = pathlib.Path(tmp) / "events.jsonl"
            set_log_path(str(log))
            with EventContext("bari_score_calculation", task_id="T-1", product_id="p-1"):
                pass
            events = read_events(log_path=str(log))
            names = [e["event_name"] for e in events]
            self.assertIn("bari_score_calculation_started", names)
            self.assertIn("bari_score_calculation_completed", names)
            completed = [e for e in events if e["event_name"] == "bari_score_calculation_completed"]
            self.assertEqual(completed[0]["status"], "success")

    def test_failed_event_context_emits_failed_event(self):
        with tempfile.TemporaryDirectory() as tmp:
            log = pathlib.Path(tmp) / "events.jsonl"
            set_log_path(str(log))
            try:
                with EventContext("bari_score_calculation", task_id="T-1", product_id="p-1"):
                    raise ValueError("test failure")
            except ValueError:
                pass
            events = read_events(log_path=str(log))
            names = [e["event_name"] for e in events]
            self.assertIn("bari_score_calculation_started", names)
            self.assertIn("bari_score_calculation_failed", names)
            failed = [e for e in events if e["event_name"] == "bari_score_calculation_failed"]
            self.assertEqual(failed[0]["status"], "failed")
            self.assertEqual(failed[0]["error_type"], "ValueError")
            self.assertEqual(failed[0]["error_message"], "test failure")

    def test_bari_events_log_env_var(self):
        with tempfile.TemporaryDirectory() as tmp:
            log = pathlib.Path(tmp) / "custom" / "path" / "events.jsonl"
            os.environ["BARI_EVENTS_LOG"] = str(log)
            try:
                emit_event("llm_task_completed", task_id="T-1")
                self.assertTrue(log.exists())
                lines = log.read_text(encoding="utf-8").strip().splitlines()
                self.assertEqual(len(lines), 1)
            finally:
                os.environ.pop("BARI_EVENTS_LOG", None)

    def test_explicit_log_path_writes_to_subdir(self):
        with tempfile.TemporaryDirectory() as tmp:
            log = pathlib.Path(tmp) / "nested" / "dir" / "events.jsonl"
            ev = emit_event("llm_output_rated", task_id="T-1", log_path=str(log))
            self.assertTrue(log.exists())
            self.assertEqual(ev["event_name"], "llm_output_rated")

    def test_input_hash_and_output_hash(self):
        h1 = input_hash("hello")
        h2 = output_hash("hello")
        self.assertEqual(h1, h2)
        self.assertEqual(len(h1), 16)
        self.assertIsNone(input_hash(""))
        self.assertIsNone(output_hash(None))

    def test_emit_score_event_success(self):
        with tempfile.TemporaryDirectory() as tmp:
            log = pathlib.Path(tmp) / "events.jsonl"
            ev = emit_score_event("success", task_id="T-1", product_id="p-1", score=70.2, grade="B",
                                  log_path=str(log))
            self.assertEqual(ev["event_name"], "bari_score_calculation_completed")
            self.assertEqual(ev["final_score"], 70.2)
            self.assertEqual(ev["grade"], "B")
            self.assertTrue(log.exists())
            raw = json.loads(log.read_text(encoding="utf-8"))
            self.assertNotIn("log_path", raw)

    def test_emit_score_event_failed(self):
        with tempfile.TemporaryDirectory() as tmp:
            log = pathlib.Path(tmp) / "events.jsonl"
            ev = emit_score_event("failed", task_id="T-1", product_id="p-1",
                                  error=("ValueError", "bad data"), log_path=str(log))
            self.assertEqual(ev["event_name"], "bari_score_calculation_failed")
            self.assertEqual(ev["error_type"], "ValueError")
            self.assertTrue(log.exists())
            raw = json.loads(log.read_text(encoding="utf-8"))
            self.assertNotIn("log_path", raw)

    def test_builder_emit_method(self):
        with tempfile.TemporaryDirectory() as tmp:
            log = pathlib.Path(tmp) / "events.jsonl"
            ev = (EventBuilder("llm_request_started")
                  .with_task_id("T-1")
                  .with_model("deepseek-chat")
                  .emit(log_path=str(log)))
            self.assertEqual(ev["event_name"], "llm_request_started")
            self.assertTrue(log.exists())

    def test_all_event_names_accepted(self):
        for name in sorted(ALL_EVENT_NAMES):
            ev = EventBuilder(name).build()
            self.assertEqual(ev["event_name"], name)

    def test_environment_auto_detect(self):
        os.environ["BARI_ENV"] = "staging"
        try:
            ev = EventBuilder("llm_request_started").build()
            self.assertEqual(ev["environment"], "staging")
        finally:
            os.environ["BARI_ENV"] = "test"


if __name__ == "__main__":
    unittest.main()
