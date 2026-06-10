#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_copy_golden_diff.py — Deliverable 3 (TASK-BARI-PROMPT-REGISTRY-CI-EVAL-V1)

Thin golden-diff harness for VERIFIED-DETERMINISTIC copy generators ONLY.

HARD RULE (from D2 corrected audit v1.1): golden_diff may ONLY be attached to
copy that is COMPUTED from the trace by a pure builder function. Authored /
carried-verbatim / patched / unverified copy is NEVER snapshotted here.

Wired surfaces (function-import, no production side effects):
  CMP-01  salty_snacks  build_salty_snacks_frontend_v2.py :: build_insight_line(trace, b1)
  CMP-10  snacks        (same builder/function as salty_snacks)
  CMP-11  butter        build_frontend_v2.py             :: build_insight_line(trace, subtype)

DEFERRED (NOT wired — inline in main(), cannot snapshot without running the
builder which writes production JSON, or refactoring the builder which is a
production change). Documented in the D3 report; not failed here:
  EXP-06  snacks limitingFactors   (inline, build_salty_snacks_frontend_v2.py main)
  (cereals multiretailer rowVerdict — inline f-string, build_cereals_multiretailer_frontend.py)

Usage:
  python run_copy_golden_diff.py            # compare against committed snapshots (CI mode)
  python run_copy_golden_diff.py --update   # (re)capture snapshots; requires a registry change_reason

Exit code 0 = all wired cases match; non-zero = drift or missing snapshot.
"""
import sys, io, json, argparse, importlib.util
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]  # 01_framework/operations/evals -> repo root
FIX = HERE / "fixtures" / "copy_inputs"
SNAP = HERE / "golden_snapshots" / "copy"
SNAP.mkdir(parents=True, exist_ok=True)

# (case_id, builder_path_relative_to_repo, fn_name, fixture_file, arg_names)
CASES = [
    ("CMP-01", "03_operations/bsip2/proto_v0/src/build_salty_snacks_frontend_v2.py",
     "build_insight_line", "salty_snacks__CMP-01.json", ["trace", "b1"]),
    ("CMP-10", "03_operations/bsip2/proto_v0/src/build_salty_snacks_frontend_v2.py",
     "build_insight_line", "snacks__CMP-10.json", ["trace", "b1"]),
    ("CMP-11", "02_products/butter/build_frontend_v2.py",
     "build_insight_line", "butter__CMP-11.json", ["trace", "subtype"]),
]

_MODCACHE = {}


def load_fn(builder_rel, fn_name):
    key = (builder_rel, fn_name)
    if key in _MODCACHE:
        return _MODCACHE[key]
    path = REPO / builder_rel
    spec = importlib.util.spec_from_file_location(f"_bld_{abs(hash(builder_rel))}", path)
    mod = importlib.util.module_from_spec(spec)
    saved_stdout = sys.stdout            # some builders rewrap stdout at import
    try:
        spec.loader.exec_module(mod)
    finally:
        new_stdout = sys.stdout
        if new_stdout is not saved_stdout:
            # The builder wrapped saved_stdout.buffer in a new TextIOWrapper. Its
            # __del__ would close the shared buffer; detach() severs it harmlessly.
            try:
                new_stdout.detach()
            except Exception:
                pass
            sys.stdout = saved_stdout    # restore harness stdout
    fn = getattr(mod, fn_name)
    _MODCACHE[key] = fn
    return fn


def run_case(case):
    case_id, builder_rel, fn_name, fixture_file, arg_names = case
    data = json.loads((FIX / fixture_file).read_text(encoding="utf-8"))
    fn = load_fn(builder_rel, fn_name)
    args = [data[a] for a in arg_names]
    return str(fn(*args))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--update", action="store_true", help="(re)capture snapshots")
    args = ap.parse_args()

    failures, updated, passed = [], [], []
    for case in CASES:
        case_id = case[0]
        try:
            out = run_case(case)
        except Exception as e:
            failures.append((case_id, f"ERROR running case: {e!r}"))
            continue
        snap_file = SNAP / f"{case_id}.txt"
        if args.update:
            snap_file.write_text(out, encoding="utf-8")
            updated.append(case_id)
            print(f"[update] {case_id} -> {snap_file.name}: {out}")
            continue
        if not snap_file.exists():
            failures.append((case_id, "MISSING snapshot (run --update first)"))
            continue
        expected = snap_file.read_text(encoding="utf-8")
        if out == expected:
            passed.append(case_id)
            print(f"[pass]   {case_id}: {out}")
        else:
            failures.append((case_id, f"DRIFT\n   expected: {expected!r}\n   actual:   {out!r}"))

    print("-" * 60)
    if args.update:
        print(f"Snapshots updated: {len(updated)} -> {updated}")
        return 0
    print(f"PASS {len(passed)} / FAIL {len(failures)} (wired deterministic copy cases)")
    for cid, msg in failures:
        print(f"  FAIL {cid}: {msg}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
