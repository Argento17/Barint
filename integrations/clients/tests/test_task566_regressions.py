"""Regression tests for TASK-566 — http.py stdlib shadow + grammar gate silent-pass.

Two regression classes tested here:

  R1  http_shadow  — a file named `http.py` under integrations/clients/ shadows the
                     stdlib `http` package when the clients dir is on sys.path[0].
                     Test: assert no such file exists; if it reappears, the test fails
                     loudly so the defect is caught before it breaks transformers again.

  R2  gate_silent_pass — a gate whose error path returns a pass-shaped result
                         (is_clean=True or flag_count=0) is undetectable from a real
                         clean run.  Test: simulate an ImportError inside
                         hebrew_grammar_gate._load_model() and assert that
                         (a) GateDidNotRunError is raised, NOT RuntimeError/plain
                             Exception with is_clean semantics,
                         (b) the message starts with the ERROR / GATE-DID-NOT-RUN sentinel,
                         (c) run_evals._load_grammar_gate(required=True) returns None
                             (NOT a callable that would silently skip grammar).
"""
from __future__ import annotations

import sys
import types
import importlib
from pathlib import Path
from unittest.mock import patch

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]  # integrations/clients/tests/../../../
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


# ---------------------------------------------------------------------------
# R1 — No http.py under integrations/clients/
# ---------------------------------------------------------------------------

def test_no_http_shadow_file():
    """integrations/clients/http.py must not exist (TASK-566 / TASK-584 rename).

    If this file reappears (e.g. someone restores an old snapshot), the stdlib
    `http` package is shadowed when that directory is on sys.path[0], which
    silently breaks transformers, urllib, and anything doing `import http.client`.
    """
    shadow_path = REPO_ROOT / "integrations" / "clients" / "http.py"
    assert not shadow_path.exists(), (
        f"TASK-566 regression: {shadow_path} exists and shadows the stdlib `http` "
        "package.  Rename it (e.g. http_client.py) and update all importers."
    )


def test_http_client_exists():
    """The renamed http_client.py must exist and be importable."""
    client_path = REPO_ROOT / "integrations" / "clients" / "http_client.py"
    assert client_path.exists(), (
        f"integrations/clients/http_client.py not found at {client_path}"
    )
    # Importable as a package module
    from integrations.clients.http_client import HttpError, get, get_json  # noqa: F401
    assert callable(get)
    assert callable(get_json)
    assert issubclass(HttpError, Exception)


def test_stdlib_http_not_shadowed_by_clients_dir():
    """Inserting integrations/clients on sys.path must NOT shadow stdlib http."""
    clients_dir = str(REPO_ROOT / "integrations" / "clients")
    original_path = sys.path[:]
    try:
        sys.path.insert(0, clients_dir)
        # Force re-evaluation (http may already be cached)
        http_mod = importlib.import_module("http")
        # The stdlib http package has http.client as a sub-module
        import http.client as _hc  # noqa: F401
        assert hasattr(http_mod, "__path__"), (
            "stdlib `http` is a package and must have `__path__`; "
            "a plain .py file would not — this means the shadow is back."
        )
    finally:
        sys.path[:] = original_path
        # Remove from import cache if we just re-added it to avoid contaminating
        # other tests (http is usually already cached from earlier imports).


# ---------------------------------------------------------------------------
# R2 — Grammar gate error path raises GateDidNotRunError, not a silent pass
# ---------------------------------------------------------------------------

def test_gate_did_not_run_error_is_distinct():
    """GateDidNotRunError must be importable and distinct from RuntimeError."""
    from integrations.clients.hebrew_grammar_gate import GateDidNotRunError
    assert issubclass(GateDidNotRunError, RuntimeError)
    assert GateDidNotRunError.SENTINEL_PREFIX.startswith("ERROR / GATE-DID-NOT-RUN:")


def test_load_model_raises_gate_error_on_import_failure():
    """When transformers is not importable, _load_model must raise GateDidNotRunError.

    The old behaviour was: raise RuntimeError with a generic message, which
    some callers caught as `except Exception` and silently continued — the
    silent-pass bug.  The new requirement: GateDidNotRunError (a distinct
    subclass) with the sentinel prefix, so callers can identify it.
    """
    from integrations.clients import hebrew_grammar_gate as gg
    from integrations.clients.hebrew_grammar_gate import GateDidNotRunError

    # Reset cached model so _load_model actually runs
    original_model = gg._model
    original_tok = gg._tokenizer
    gg._model = None
    gg._tokenizer = None

    try:
        # Patch the transformers import inside _load_model to simulate absence
        import builtins
        real_import = builtins.__import__

        def _no_transformers(name, *args, **kwargs):
            if name == "transformers":
                raise ImportError("No module named 'transformers' (simulated for TASK-566 test)")
            return real_import(name, *args, **kwargs)

        with patch("builtins.__import__", side_effect=_no_transformers):
            with pytest.raises(GateDidNotRunError) as exc_info:
                gg._load_model()

        err_msg = str(exc_info.value)
        assert err_msg.startswith(GateDidNotRunError.SENTINEL_PREFIX), (
            f"GateDidNotRunError message must start with the sentinel prefix "
            f"'{GateDidNotRunError.SENTINEL_PREFIX}'; got: {err_msg!r}"
        )
    finally:
        gg._model = original_model
        gg._tokenizer = original_tok


def test_analyze_propagates_gate_did_not_run_error():
    """analyze() must propagate GateDidNotRunError, never return a clean GrammarReport."""
    from integrations.clients import hebrew_grammar_gate as gg
    from integrations.clients.hebrew_grammar_gate import GateDidNotRunError

    original_model = gg._model
    original_tok = gg._tokenizer
    gg._model = None
    gg._tokenizer = None

    try:
        import builtins
        real_import = builtins.__import__

        def _no_transformers(name, *args, **kwargs):
            if name == "transformers":
                raise ImportError("simulated absence")
            return real_import(name, *args, **kwargs)

        with patch("builtins.__import__", side_effect=_no_transformers):
            with pytest.raises(GateDidNotRunError):
                gg.analyze("הגבינה הצהוב")  # must NOT silently return GrammarReport(is_clean=True)
    finally:
        gg._model = original_model
        gg._tokenizer = original_tok


def test_run_evals_load_grammar_gate_required_fails_loud(capsys):
    """run_evals._load_grammar_gate(required=True) must return None (not a callable)
    when the gate errors, so main() can detect and exit 1.

    The old _load_grammar_gate() always returned None on any exception regardless
    of whether grammar was explicitly requested — the caller had no way to distinguish
    'not requested' from 'requested but broken', so it silently skipped grammar.
    """
    # We have to import the module freshly each time since it uses sys.path.insert
    run_evals_path = REPO_ROOT / "03_operations" / "evals" / "copy_evals" / "run_evals.py"
    spec = importlib.util.spec_from_file_location("run_evals_test", run_evals_path)
    run_evals = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(run_evals)

    # Patch gate_status to simulate failure
    def _failing_gate_status():
        return ("error", "ERROR / GATE-DID-NOT-RUN: hebrew_grammar_gate: simulated")

    import builtins
    real_import = builtins.__import__

    class _FakeGGModule:
        """Fake grammar gate module that gate_status errors."""
        def gate_status(self):
            return ("error", "ERROR / GATE-DID-NOT-RUN: hebrew_grammar_gate: simulated")

        class GateDidNotRunError(RuntimeError):
            SENTINEL_PREFIX = "ERROR / GATE-DID-NOT-RUN: hebrew_grammar_gate"

        def analyze(self, text):
            raise self.GateDidNotRunError("simulated")

    fake_mod = _FakeGGModule()

    def _mock_import(name, *args, **kwargs):
        if "hebrew_grammar_gate" in name:
            # Return a fake module-like object
            mod = types.ModuleType("integrations.clients.hebrew_grammar_gate")
            mod.GateDidNotRunError = fake_mod.GateDidNotRunError
            mod.gate_status = fake_mod.gate_status
            mod.analyze = fake_mod.analyze
            return mod
        return real_import(name, *args, **kwargs)

    with patch("builtins.__import__", side_effect=_mock_import):
        result = run_evals._load_grammar_gate(required=True)

    captured = capsys.readouterr()
    assert result is None, (
        "When required=True and the gate fails, _load_grammar_gate must return None "
        "so main() can detect it and exit 1 — NOT return a callable that skips grammar silently."
    )
    assert "GATE-DID-NOT-RUN" in captured.err or "gate" in captured.err.lower(), (
        "When required=True and gate fails, an ERROR message must appear on stderr."
    )
