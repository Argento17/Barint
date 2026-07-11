"""
layer4_checks.py — Layer 4 (checks) for the Product Dossier compiler
(PD-2 / TASK-610).

Per STF memo `2026-07-11_product-dossier-architecture.md` §4:
  "Layer 4 -- Checks. Pure functions recomputed every compile; IMPORTS
  existing gate logic (run_gates G-checks, validate_comparison_page) -- the
  per-product pivot of the gate suite, not a fork. calculation check =
  published (publication_record) vs trace (G5 per-product). `publishability`
  is diagnostic shadow state in the MVP -- it CANNOT change current
  publication."

Four checks, per the PD-2 delegation spec (barcode join WIRED as a follow-up,
TASK-610 registry-interface increment):
  - barcode              -- REAL: reads Layer 1's registry-adjudicated
                             barcode_state (see lib/registry_interface.py +
                             lib/layer1_identity.py) -- never re-derives its
                             own verdict from the raw served barcode string.
  - source_traceability  -- REAL: Layer-2 manifest coverage + BSIP2 trace presence
  - calculation          -- REAL: imports run_gates.gate_grade_integrity (G5) per product
  - publishability       -- REAL but diagnostic-only aggregate of the above two;
                             never gates or mutates current publication (tripwire-1)

This module loads 03_operations/page_generator/gates/run_gates.py by file
path (same importlib.util technique used throughout this compiler) and
calls its functions directly -- it does not reimplement G5's tolerance
logic or grade-scale.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Dict, Optional

REPO_ROOT = Path(__file__).resolve().parents[3]
RUN_GATES_PATH = REPO_ROOT / "03_operations" / "page_generator" / "gates" / "run_gates.py"

_run_gates = None


def run_gates_module():
    global _run_gates
    if _run_gates is None:
        spec = importlib.util.spec_from_file_location("pd2_run_gates_ref", RUN_GATES_PATH)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        _run_gates = module
    return _run_gates


class CheckResult:
    """Uniform per-check result shape. status one of PASS/FAIL/WARN/UNKNOWN.
    UNKNOWN is reserved for checks that are deliberately stubbed pending an
    upstream dependency (the barcode check, until the registry joins) --
    it is distinct from FAIL: a stub is not a failing assertion, it is an
    honest "cannot evaluate yet".
    """

    def __init__(self, name: str, status: str, evidence: Optional[list] = None, reason: Optional[str] = None):
        self.name = name
        self.status = status
        self.evidence = evidence or []
        self.reason = reason

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "status": self.status,
            "evidence": self.evidence,
            "reason": self.reason,
        }


# ---------------------------------------------------------------------------
# barcode -- REAL, reads Layer 1's registry-adjudicated barcode_state
# ---------------------------------------------------------------------------

# Registry barcode_status -> this check's PASS/FAIL/WARN/UNKNOWN verdict.
# "verified" is the only clean pass; "found_but_conflicting"/"not_found" are
# real adjudicated failures (not stubs); "malformed"/"pending_manual_review"
# are real adjudicated warns (a human/registry-process step is still owed,
# but it is not a fabricated verdict -- registry_ops.py already produced it).
_BARCODE_STATUS_TO_CHECK_STATUS = {
    "verified": "pass",
    "found_but_conflicting": "fail",
    "not_found": "fail",
    "malformed": "warn",
    "pending_manual_review": "warn",
}


def check_barcode(layer1: dict) -> CheckResult:
    """Reads Layer 1's already-registry-adjudicated `barcode_state` (see
    lib/registry_interface.py's resolve_bari_pid()/get_registry_record() and
    lib/layer1_identity.py's assemble_layer1()) -- this function never
    re-derives a verdict from the raw served barcode string itself, because
    that is exactly the un-adjudicated guess the registry (TASK-609/PD-1)
    exists to replace. UNKNOWN is reserved for the genuine remainder: the
    product's pid did not resolve against the registry at all (registry
    miss, or an ambiguous alias PD-1 already routed to
    pending_manual_review and excluded from its alias table), or the
    registry file itself is absent from this worktree.
    """
    status = layer1.get("barcode_state", {}).get("status", "unknown")
    reason = layer1.get("barcode_state", {}).get("reason")
    recovered_gtin = layer1.get("recovered_gtin")
    evidence = [
        f"pid_status: {layer1.get('pid_status')}",
        f"registry barcode_status: {status!r}",
        f"served barcode field (unadjudicated): {layer1.get('barcode_state', {}).get('served_barcode_unadjudicated')!r}",
    ]
    if recovered_gtin:
        evidence.append(f"recovered_gtin: {recovered_gtin!r}")
    check_status = _BARCODE_STATUS_TO_CHECK_STATUS.get(status, "unknown")
    return CheckResult("barcode", check_status, evidence=evidence, reason=reason)


# ---------------------------------------------------------------------------
# source_traceability -- real, Layer-2-derived
# ---------------------------------------------------------------------------

def check_source_traceability(layer2_cells: Dict[str, dict], match_note: str, has_trace: bool) -> CheckResult:
    """PASS: at least one Layer-2 field cell was actually retrieved from a
    canonical manifest capture (i.e. this product is not a total capture
    miss) AND a BSIP2 trace was found for it.
    WARN: partial -- either evidence exists but no trace, or a trace exists
    but capture coverage is zero (e.g. captured only under a different
    shelf/category, TASK-602 fan-out gap).
    FAIL: neither evidence nor trace -- a product on a served page with zero
    upstream lineage.
    """
    retrieved = sum(1 for c in layer2_cells.values() if c.get("status") == "retrieved")
    evidence = [f"layer2 fields retrieved: {retrieved}/{len(layer2_cells)}", f"capture match: {match_note}", f"bsip2 trace found: {has_trace}"]
    if retrieved > 0 and has_trace:
        return CheckResult("source_traceability", "pass", evidence=evidence)
    if retrieved == 0 and not has_trace:
        return CheckResult("source_traceability", "fail", evidence=evidence, reason="no manifest capture and no BSIP2 trace")
    return CheckResult("source_traceability", "warn", evidence=evidence, reason="partial lineage (capture without trace, or trace without capture)")


# ---------------------------------------------------------------------------
# calculation -- real, imports run_gates.gate_grade_integrity (G5) per product
# ---------------------------------------------------------------------------

def check_calculation(served_product: dict, trace: Optional[dict]) -> CheckResult:
    """Published (publication_record: served score/grade) vs trace
    (assessment: bsip2_trace final_score_estimate/grade_estimate), per
    product -- the exact G5 GRADE-INTEGRITY comparison run_gates.py runs at
    page level, invoked here on a single-product frontend wrapper so the
    tolerance (0.05) and grade-inflation logic are never re-derived, only
    imported and reused.
    """
    rg = run_gates_module()
    if trace is None:
        return CheckResult(
            "calculation", "warn",
            evidence=["no BSIP2 trace available for this product"],
            reason="cannot verify published score against a trace (see TASK-563: 8/15 processed "
                   "shelves have no recoverable trace directory at all)",
        )
    single_frontend = {"products": [served_product]}
    barcode = rg.get_barcode_from_product(served_product)
    traces = {barcode: trace}
    try:
        gate_result = rg.gate_grade_integrity(single_frontend, traces, config={})
    except Exception as e:
        # run_gates.gate_grade_integrity is imported, not reimplemented (per
        # this module's docstring) -- it can raise on a served product whose
        # copy-field shape it doesn't expect (observed: some granola products
        # carry a non-dict consumer-copy field, an upstream data shape issue
        # unrelated to this compiler or the registry join). A single
        # product's calculation check failing to even RUN is honestly a
        # WARN ("cannot verify"), never a DossierBuildError -- it must not
        # abort every other product's dossier in the same shelf/build.
        return CheckResult(
            "calculation", "warn",
            evidence=[f"run_gates.gate_grade_integrity raised {type(e).__name__}: {e}"],
            reason="calculation check could not run for this product (upstream run_gates exception, "
                   "not a structural dossier-build failure)",
        )
    status_map = {"PASS": "pass", "FAIL": "fail", "WARN": "warn", "SKIP": "warn"}
    return CheckResult(
        "calculation",
        status_map.get(gate_result.status, "warn"),
        evidence=list(gate_result.lines),
        reason=None if gate_result.status == "PASS" else "published score/grade disagrees with BSIP2 trace (G5)",
    )


# ---------------------------------------------------------------------------
# publishability -- diagnostic shadow state ONLY (never gates current pub)
# ---------------------------------------------------------------------------

def check_publishability(source_traceability: CheckResult, calculation: CheckResult, barcode: CheckResult) -> CheckResult:
    """Diagnostic aggregate for the future scanner publish path. Per memo
    §4: "publishability is diagnostic shadow state in the MVP -- it CANNOT
    change current publication; the future scanner publish path uses a
    separately versioned policy + two-gate sign-off." This check result is
    NEVER read by any live page-generation or serving code path in this
    compiler or elsewhere -- it exists purely for the internal inspection
    view (PD-3) to render.
    barcode is intentionally excluded from the pass/fail computation --
    per the PD-2 delegation spec this aggregate stays scoped to
    source_traceability + calculation only, even now that barcode is a real
    (registry-derived) verdict rather than a stub -- but is still reported
    for visibility.
    """
    sub = {"source_traceability": source_traceability.status, "calculation": calculation.status}
    if sub["source_traceability"] == "pass" and sub["calculation"] == "pass":
        status = "pass"
    elif "fail" in sub.values():
        status = "fail"
    else:
        status = "warn"
    return CheckResult(
        "publishability",
        status,
        evidence=[f"{k}={v}" for k, v in sub.items()] + [f"barcode(advisory, not counted)={barcode.status}"],
        reason="DIAGNOSTIC ONLY -- does not gate or change current publication (tripwire-1)",
    )


def run_all_checks(
    served_product: dict,
    layer2_cells: Dict[str, dict],
    match_note: str,
    trace: Optional[dict],
    layer1: dict,
) -> Dict[str, CheckResult]:
    barcode = check_barcode(layer1)
    source_traceability = check_source_traceability(layer2_cells, match_note, has_trace=trace is not None)
    calculation = check_calculation(served_product, trace)
    publishability = check_publishability(source_traceability, calculation, barcode)
    return {
        "barcode": barcode,
        "source_traceability": source_traceability,
        "calculation": calculation,
        "publishability": publishability,
    }
