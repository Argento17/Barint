"""
grade_governance.py — _shared re-export

The canonical implementation lives at:
  C:\\Bari\\03_operations\\bsip2\\proto_v0\\src\\grade_governance.py

This module re-exports everything from that location so that builders which
add the _shared path to sys.path can import apply_a_grade_floor without
knowing the bsip2 proto path.

TASK-188 — A-grade ingredient observability floor (Product + Nutrition co-sign,
2026-06-05).
"""
import importlib
import importlib.util
import pathlib
import sys

_CANONICAL_SRC = str(
    pathlib.Path(__file__).parent.parent.parent.parent
    / "bsip2" / "proto_v0" / "src"
)

# Load the canonical module under a distinct name to avoid the circular-import
# that would arise if Python tried to re-import *this* file when executing
# `from grade_governance import ...`.
_spec = importlib.util.spec_from_file_location(
    "_grade_governance_canonical",
    str(pathlib.Path(_CANONICAL_SRC) / "grade_governance.py"),
)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

# Re-export the public API.
apply_a_grade_floor = _mod.apply_a_grade_floor  # noqa: F401
floor_reasons = _mod.floor_reasons              # noqa: F401
