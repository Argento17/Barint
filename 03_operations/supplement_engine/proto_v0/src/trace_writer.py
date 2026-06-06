"""
SIE Prototype v0 — Trace Writer (§12.2 structured trace contract)
=================================================================
Emits the machine-readable "why" per scored SKU. This is the Phase-2 deliverable
and the contract to the Phase-4 consumer-prose renderer. The trace alone must
regenerate the "why" deterministically (no second dossier/literature pass).

Discipline (§12.3, inherited from BSIP2): grounded-in-real-trace (every field
traces to a real sub-score / fired mechanism / dossier fact), dominant-driver /
anti-attribution (the binding constraint, not the smallest number), no banned
efficacy/necessity tokens, No-Necessity firewall (SIE Invariant 1). NO consumer
prose here (that is Phase 4).
"""
import json
import datetime
import pathlib

import constants as C

NA = "N/A"


def _signature(subs: dict) -> dict:
    """Compact sub-score SIGNATURE for the §13 attribution archetypes:
    HIGH / LOW / N/A / VETO / NEUTRAL per dimension. Used by validation to assert
    that two same-grade products carry inverted signatures."""
    def band(dim, v):
        if v == NA:
            return "N/A"
        if dim == "safety":
            if v == C.SAFETY_VETO:
                return "VETO"
            if v == C.SAFETY_NEUTRAL:
                return "NEUTRAL"
            if v == C.SAFETY_NOTE:
                return "NOTE"
        try:
            fv = float(v)
        except (TypeError, ValueError):
            return str(v)
        return "HIGH" if fv >= 65 else ("MID" if fv >= 35 else "LOW")

    return {dim: band(dim, subs[dim]["value"]) for dim in
            ["evidence", "dose", "form", "honesty", "safety"]}


def assemble_trace(result: dict, dossier_facts: list) -> dict:
    subs = result["sub_scores"]
    comb = result["combination"]

    sub_block = {}
    for dim in ["evidence", "dose", "form", "honesty", "safety"]:
        s = subs[dim]
        entry = {"value": s["value"]}
        if dim == "evidence":
            entry["tier"] = s.get("tier")
        if "reason" in s:
            entry["reason"] = s["reason"]
        sub_block[dim] = entry

    return {
        "sie_engine_version": C.SIE_ENGINE_VERSION,
        "sie_algorithm_version": C.SIE_ALGORITHM_VERSION,
        "methodology_version": C.METHODOLOGY_VERSION,
        "trace_generated_at": datetime.datetime.utcnow().isoformat() + "Z",
        "verification_status": "candidate",   # EDPG: nothing here is authoritative
        "calibration_pending": True,

        "sku_id": result["sku_id"],
        "active": result["active"],
        "on_label_claim": result["on_label_claim"],
        "claim_matched": result["claim_matched"],

        # §2.1 (v1.3) claim-resolution audit: which umbrella key resolved, to
        # which endpoint + tier (so the "why" is auditable, §12). Firewall: this
        # is the in-house dossier map, never a live API.
        "claim_resolution": result.get("claim_resolution", {}),

        "sub_scores": sub_block,
        "signature": _signature(subs),

        "caps_vetoes_fired": comb["caps_vetoes_fired"],
        "binding_constraint": comb["binding_constraint"],
        "also_fired": comb["also_fired"],

        "blend": comb["blend"],
        "dossier_facts_used": dossier_facts,

        "final": {"score": comb["final_score"], "grade": comb["grade"]},
    }


def write_trace(trace: dict, out_dir: str) -> str:
    out = pathlib.Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"{trace['sku_id']}_trace.json"
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(trace, fh, indent=2, ensure_ascii=False)
    return str(path)
