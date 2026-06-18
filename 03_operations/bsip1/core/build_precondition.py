"""
BSIP1 Builder Precondition — gate-artifact check.

Every BSIP1 builder (02_build_bsip1_*.py) MUST accept a ``--gate-artifact``
flag pointing to the gate result JSON from the preceding BSIP0 exit gate run.
The builder calls ``require_gate_pass`` before doing any work; if the gate
result is FAIL, the builder exits non-zero with a clear message.

Usage in a builder::

    from build_precondition import require_gate_pass

    if __name__ == "__main__":
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument("--gate-artifact", required=True,
                            help="Path to BSIP0 gate result JSON (must be PASS)")
        args = parser.parse_args()
        require_gate_pass(args.gate_artifact)
        # ... rest of build logic
"""
from __future__ import annotations

import json
import logging
import sys
from pathlib import Path

log = logging.getLogger(__name__)


class GateRefusedError(RuntimeError):
    """Raised when the BSIP0 gate result is FAIL — builder must not proceed."""

    def __init__(self, gate_result: dict):
        self.gate_result = gate_result
        n_fail = gate_result.get("summary", {}).get("FAIL", 0)
        super().__init__(
            f"BSIP0 exit gate returned FAIL ({n_fail} failed check(s)). "
            f"Builder refuses to run. Gate: {gate_result.get('gate', '?')}. "
            f"Overall: {gate_result.get('overall_status', '?')}. "
            f"Fix the BSIP0 data and re-run the gate before building."
        )


def require_gate_pass(gate_artifact_path: str | Path) -> dict:
    """Load a gate result JSON and raise ``GateRefusedError`` if not PASS.

    Returns the gate result dict on PASS so the builder can log it.
    """
    path = Path(gate_artifact_path)
    if not path.exists():
        log.error("Gate artifact not found: %s", path)
        sys.exit(1)

    with open(path, encoding="utf-8") as f:
        result = json.load(f)

    status = result.get("overall_status", "UNKNOWN")
    if status == "FAIL":
        raise GateRefusedError(result)

    log.info("BSIP0 gate precondition: %s (%d products, %d checks)",
             status, result.get("product_count", 0),
             len(result.get("checks", [])))
    return result
