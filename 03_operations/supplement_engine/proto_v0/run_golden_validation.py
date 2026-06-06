"""
SIE Prototype v0 — Golden-Corpus Validation Runner
==================================================
Scores every golden fixture; emits a table (fixture -> score, grade,
binding_constraint, signature); asserts each lands in its expected grade band AND
carries the expected binding constraint. The decisive test (§13.2): the two E
archetypes (no-evidence vs dangerous) must carry DIFFERENT binding constraints and
never be confused.

Run:  .venv/Scripts/python.exe run_golden_validation.py
"""
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))

import constants as C
from score_engine import score_label
from trace_writer import assemble_trace, write_trace
from dossier_loader import load_dossier
from golden_corpus.fixtures import (FIXTURES, ARCHETYPES, RESOLUTION_FIXTURES,
                                     ALL_FIXTURES)

TRACE_DIR = ROOT / "golden_corpus" / "traces"


def _dossier_facts(result):
    cm = result["claim_matched"]
    facts = [{
        "field": f"claims['{cm}'].evidence_tier",
        "value": result["sub_scores"]["evidence"]["tier"],
        "supp_ev": result["supp_ev_refs"][0] if result["supp_ev_refs"] else None,
    }]
    return facts


def run_one(fx):
    dossier = load_dossier(fx["dossier_slug"])
    result = score_label(fx["label"], dossier, **fx["flags"])
    trace = assemble_trace(result, _dossier_facts(result))
    write_trace(trace, str(TRACE_DIR))
    return result, trace


def check(fx, trace):
    exp = fx["expect"]
    grade = trace["final"]["grade"]
    binding = trace["binding_constraint"]["mechanism"]
    sig = trace["signature"]
    problems = []

    if "grade_in" in exp and grade not in exp["grade_in"]:
        problems.append(f"grade {grade} not in {exp['grade_in']}")
    if "grade_not" in exp and grade in exp["grade_not"]:
        problems.append(f"grade {grade} should not be {exp['grade_not']}")
    if "binding" in exp and binding != exp["binding"]:
        problems.append(f"binding {binding} != {exp['binding']}")
    if "binding_not" in exp and binding == exp["binding_not"]:
        problems.append(f"binding {binding} should not be {exp['binding_not']}")
    if "sig" in exp:
        for dim, want in exp["sig"].items():
            if sig.get(dim) != want:
                problems.append(f"sig.{dim}={sig.get(dim)} != {want}")
    return problems


def fmt_subs(trace):
    s = trace["sub_scores"]
    def v(d):
        val = s[d]["value"]
        return str(val)
    return (f"Ev={v('evidence')}({s['evidence'].get('tier','')[:4]}) "
            f"Do={v('dose')} Fo={v('form')} Ho={v('honesty')} Sa={v('safety')}")


def main():
    print("=" * 110)
    print("SIE GOLDEN-CORPUS VALIDATION  —  proto_v0  (ALL NUMBERS CALIBRATION-PENDING)")
    print("=" * 110)
    rows = []
    all_pass = True

    def section(title, fxs):
        nonlocal all_pass
        print(f"\n## {title}")
        print(f"{'fixture':<34}{'score':>6} {'grade':>6}  {'binding_constraint':<32}{'result'}")
        print("-" * 110)
        for fx in fxs:
            result, trace = run_one(fx)
            problems = check(fx, trace)
            status = "PASS" if not problems else "FAIL: " + "; ".join(problems)
            if problems:
                all_pass = False
            print(f"{fx['sku_id']:<34}{trace['final']['score']:>6} "
                  f"{trace['final']['grade']:>6}  "
                  f"{trace['binding_constraint']['mechanism']:<32}{status}")
            print(f"{'':>4}{fmt_subs(trace)}   sig={trace['signature']}")
            rows.append((fx, trace, problems))

    section("A. Per-dimension PASS/FAIL anchors (§6)", FIXTURES)
    section("B. Attribution archetypes (§13)", ARCHETYPES)
    section("C. Claim-resolution fixtures (§13.4, v1.3)", RESOLUTION_FIXTURES)

    # --- decisive test: inverted-E pair (§13.2) ----------------------------
    print("\n" + "=" * 110)
    print("DECISIVE TEST — inverted-E pair (§13.2): two E products, opposite reasons, never confused")
    print("=" * 110)
    by_id = {t["sku_id"]: t for (_, t, _) in rows}
    e_noev = by_id["ARCH-noevidence-creatine-fatloss"]
    e_danger = by_id["ARCH-dangerous-d3-50k"]
    inv_problems = []
    if e_noev["final"]["grade"] != "E":
        inv_problems.append("no-evidence archetype is not E")
    if e_danger["final"]["grade"] != "E":
        inv_problems.append("dangerous archetype is not E")
    b1 = e_noev["binding_constraint"]["mechanism"]
    b2 = e_danger["binding_constraint"]["mechanism"]
    if b1 == b2:
        inv_problems.append(f"both E archetypes share binding constraint {b1} (CONFUSED)")
    if b1 != C.MECH_CAP_1:
        inv_problems.append(f"no-evidence binding {b1} != {C.MECH_CAP_1}")
    if b2 != C.MECH_VETO_SAFETY:
        inv_problems.append(f"dangerous binding {b2} != {C.MECH_VETO_SAFETY}")

    print(f"  no-evidence E  : grade={e_noev['final']['grade']} "
          f"binding={b1} reason={e_noev['binding_constraint']['machine_reason']} "
          f"sig={e_noev['signature']}")
    print(f"  dangerous E    : grade={e_danger['final']['grade']} "
          f"binding={b2} reason={e_danger['binding_constraint']['machine_reason']} "
          f"sig={e_danger['signature']}")
    if inv_problems:
        all_pass = False
        print("  >>> INVERTED-E TEST FAILED: " + "; ".join(inv_problems))
    else:
        print("  >>> INVERTED-E TEST PASSED: both E, DIFFERENT binding constraints, "
              "inverted signatures, never confused.")

    # --- §13.4 cross-fixture invariants (v1.3 claim resolution) -------------
    print("\n" + "=" * 110)
    print("CROSS-FIXTURE INVARIANTS — §13.4 claim resolution (v1.3): resolution helps, never a loophole")
    print("=" * 110)
    r1 = by_id["R1-vague-evidenced-mg"]
    r2 = by_id["R2-vague-snakeoil"]
    r3 = by_id["R3-overspecific-false-mg"]
    xinv = []

    # (i) R1 is reachable ONLY via resolution, NOT by R2. R1 binding must be the
    #     blend (cap-1 did NOT fire); R2 binding must be cap-1 (nothing mapped).
    r1_binding = r1["binding_constraint"]["mechanism"]
    r2_binding = r2["binding_constraint"]["mechanism"]
    if r1_binding != C.MECH_BLEND_DOMINANT:
        xinv.append(f"R1 binding {r1_binding} != blend_dominant_limit "
                    f"(cap-1 must NOT fire for a resolved claim)")
    if r1_binding == C.MECH_CAP_1:
        xinv.append("R1 fired cap_1 — resolution FAILED to fire (rule broken)")
    if r2_binding != C.MECH_CAP_1:
        xinv.append(f"R2 binding {r2_binding} != cap_1 (snake-oil must floor at cap-1)")
    if r1["final"]["grade"] not in ("B", "A"):
        xinv.append(f"R1 grade {r1['final']['grade']} not in B/A (resolution must lift off E)")
    if r2["final"]["grade"] != "E":
        xinv.append(f"R2 grade {r2['final']['grade']} != E (snake-oil must stay E)")

    # (ii) R3 grades STRICTLY BELOW R1 on the SAME active (a lie cannot out-earn
    #      honest vagueness). Compare by band index AND raw score.
    band_rank = {g: i for i, (g, _) in enumerate(C.GRADE_BANDS)}  # S=0 best ... E=5
    r1_g, r3_g = r1["final"]["grade"], r3["final"]["grade"]
    if not (band_rank[r3_g] > band_rank[r1_g]):
        xinv.append(f"R3 grade {r3_g} is NOT strictly below R1 grade {r1_g} "
                    f"(a confident lie out-earned honest vagueness — loophole)")
    if r3["final"]["score"] >= r1["final"]["score"]:
        xinv.append(f"R3 score {r3['final']['score']} >= R1 score {r1['final']['score']} "
                    f"(over-promise catch failed)")
    if r3["binding_constraint"]["mechanism"] not in (C.MECH_CAP_3_CORE,):
        # spec allows cap-3 OR the Weak-tier path; we assert the over-promise catch bound it.
        xinv.append(f"R3 binding {r3['binding_constraint']['mechanism']} "
                    f"!= cap_3_honesty_core (over-promise catch did not bind)")

    print(f"  R1 (vague/evidenced) : grade={r1_g} score={r1['final']['score']} "
          f"binding={r1_binding}  resolved={r1.get('claim_resolution',{}).get('resolved_endpoint')} "
          f"tier={r1.get('claim_resolution',{}).get('resolved_tier')}")
    print(f"  R2 (vague/snake-oil) : grade={r2['final']['grade']} score={r2['final']['score']} "
          f"binding={r2_binding}  (nothing maps)")
    print(f"  R3 (over-specific)   : grade={r3_g} score={r3['final']['score']} "
          f"binding={r3['binding_constraint']['mechanism']}  resolved="
          f"{r3.get('claim_resolution',{}).get('resolved_endpoint')} "
          f"tier={r3.get('claim_resolution',{}).get('resolved_tier')} "
          f"over_promise={r3.get('claim_resolution',{}).get('over_promise')}")
    if xinv:
        all_pass = False
        print("  >>> CROSS-FIXTURE INVARIANTS FAILED: " + "; ".join(xinv))
    else:
        print("  >>> CROSS-FIXTURE INVARIANTS PASSED: R1 reachable ONLY via resolution "
              "(R2 stays E); R3 strictly below R1 on the same active.")

    print("\n" + "=" * 110)
    print(f"OVERALL: {'ALL FIXTURES PASS' if all_pass else 'FAILURES PRESENT'}  "
          f"({sum(1 for _,_,p in rows if not p)}/{len(rows)} fixtures pass)")
    print("=" * 110)
    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
