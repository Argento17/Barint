"""
Standalone confidence-annotation pass over the LIVE frontend JSONs.

Reads the BSIP2 traces (authoritative), derives the four confidence fields per
product, and writes them back into each live category JSON under
  C:\\bari\\bari-web\\src\\data\\comparisons\\
and into the matching 02_products source copy where one exists.

INVARIANT (hard): the count of currently-displayed products that flip to
`insufficient` MUST be 0. If it is not, the pass aborts without writing.

Run:  python run_confidence_annotation_pass.py            (writes)
      python run_confidence_annotation_pass.py --dry-run  (report only)
"""
import sys, io, json, glob, pathlib, shutil, datetime
from collections import Counter

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import confidence_annotation as CA

WEB_DIR = pathlib.Path(r"C:\bari\bari-web\src\data\comparisons")
PROD_BASE = pathlib.Path(r"C:\Bari\02_products")
DRY = "--dry-run" in sys.argv

# The 14 live category files (current versions). salty_snacks v2 is superseded by v3.
LIVE_FILES = [
    "bread_frontend_v2.json", "butter_frontend_v2.json", "cereals_frontend_v2.json",
    "cheese_frontend_v3.json", "crackers_staged_v1.json", "granola_frontend_v1.json",
    "hard_cheeses_frontend_v2.json", "hummus_frontend_v5.json", "juices_frontend_v3.json",
    "maadanim_frontend_v3.json", "olive_oil_frontend_v1.json", "salty_snacks_frontend_v3.json",
    "snacks_frontend_v2.json", "yogurts_frontend_v3.json",
]

# The deployment boundary is the web copy under src/data/comparisons/ (CLAUDE.md hard rule:
# "the JSON copy to src\\data\\comparisons\\ is the only permitted website write"). The
# 02_products *_frontend_*.json files are build-artifact snapshots owned by their own build
# scripts, with divergent version names (maadanim_v2 vs web_v3, hummus_v3 vs web_v5); mirroring
# into them risks writing stale/mismatched copies. This pass therefore writes the authoritative
# web copies only. Build scripts pick up the shared annotation via confidence_annotation.py.
SOURCE_COPY = {}


def build_trace_index():
    """
    Index ALL traces per key as a list (a product id/barcode can appear across
    multiple runs of a category). Collision is resolved at JOIN time, score-aware,
    so we always read the trace that actually backs the DISPLAYED grade — never an
    older, superseded run (e.g. an early butter run that flagged insufficient before
    the panel was completed). This is the fix for the trace-join ambiguity that the
    threshold report §3 anticipated ("insufficient butter traces filtered out of the
    displayed corpus").
    """
    idx_id, idx_bc = {}, {}
    files = glob.glob(str(PROD_BASE / "**" / "bsip2_trace.json"), recursive=True)
    for tp in files:
        try:
            t = json.loads(pathlib.Path(tp).read_text("utf-8"))
        except Exception:
            continue
        ref = t.get("input_reference") or {}
        pid = ref.get("canonical_product_id") or t.get("canonical_product_id")
        bc = ref.get("barcode")
        if pid:
            idx_id.setdefault(pid, []).append(t)
        if bc:
            idx_bc.setdefault(str(bc), []).append(t)
    return idx_id, idx_bc, len(files)


def _gen_at(t):
    return t.get("trace_generated_at") or ""


def select_trace(candidates, displayed_score):
    """
    From all traces for a product, pick the one that backs the displayed score:
      1) prefer a trace whose round(final_score_estimate) == displayed_score
         (most-recent such trace if several);
      2) else the most-recently generated trace.
    """
    if not candidates:
        return None
    if displayed_score is not None:
        score_matches = [
            t for t in candidates
            if t.get("final_score_estimate") is not None
            and round(t["final_score_estimate"]) == round(displayed_score)
        ]
        if score_matches:
            return max(score_matches, key=_gen_at)
    return max(candidates, key=_gen_at)


def join_trace(idx_id, idx_bc, pid, bc, displayed_score):
    cands = list(idx_id.get(pid, []))
    if bc:
        cands += idx_bc.get(bc, [])
    # de-dup identical trace objects by (id, generated_at)
    seen = set(); uniq = []
    for t in cands:
        key = (id(t),)
        if key in seen:
            continue
        seen.add(key); uniq.append(t)
    return select_trace(uniq, displayed_score)


def main():
    idx_id, idx_bc, ntrace = build_trace_index()
    print(f"Trace index: {ntrace} trace files | by id {len(idx_id)} | by barcode {len(idx_bc)}\n")

    global_conf = Counter()
    global_state = Counter()
    flips_to_insufficient = []   # the invariant guard
    matched_total = unmatched_total = 0
    per_file_payload = {}        # path -> mutated data (write after invariant passes)

    for fn in LIVE_FILES:
        web_path = WEB_DIR / fn
        data = json.loads(web_path.read_text("utf-8"))
        prods = data["products"]
        fconf = Counter()
        f_matched = f_unmatched = 0
        for p in prods:
            pid = p.get("id")
            bc = str(p.get("barcode")) if p.get("barcode") else None
            old_conf = p.get("confidence")
            trace = join_trace(idx_id, idx_bc, pid, bc, p.get("score"))
            if trace is not None:
                f_matched += 1
                fields = CA.annotate_from_trace(trace)
            else:
                f_unmatched += 1
                fields = CA.annotate_fallback(old_conf)

            # INVARIANT: a currently-displayed product must not flip to insufficient.
            if old_conf in ("verified", "partial") and fields["confidence"] == "insufficient":
                flips_to_insufficient.append((fn, pid, old_conf))

            p.update(fields)
            fconf[fields["confidence"]] += 1
            global_conf[fields["confidence"]] += 1
            # state label for reporting
            st = state_label(fields["confidence"], fields["confidence_sub_reason"])
            global_state[st] += 1

        matched_total += f_matched
        unmatched_total += f_unmatched
        per_file_payload[web_path] = data
        if SOURCE_COPY.get(fn):
            per_file_payload[SOURCE_COPY[fn]] = data
        print(f"{fn:32s} n={len(prods):3d}  match={f_matched:3d} fallback={f_unmatched:2d}  {dict(fconf)}")

    print()
    print(f"JOIN: matched={matched_total} fallback(unmatched)={unmatched_total}")
    print(f"LIVE confidence distribution: {dict(global_conf)} (total {sum(global_conf.values())})")
    print(f"STATE distribution: {dict(global_state)}")
    print(f"\nINVARIANT — products flipping to insufficient: {len(flips_to_insufficient)}")
    if flips_to_insufficient:
        print("  *** INVARIANT VIOLATED — aborting, no files written ***")
        for x in flips_to_insufficient:
            print("   ", x)
        sys.exit(1)
    print("  PASS — zero currently-displayed products move to insufficient.")

    if DRY:
        print("\n[--dry-run] no files written.")
        return

    for path, data in per_file_payload.items():
        path = pathlib.Path(path)
        if not path.parent.exists():
            print(f"  skip (parent missing): {path}")
            continue
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"  wrote {path}")


def state_label(confidence, sub):
    if confidence == "verified":
        return "1_verified"
    if confidence == "insufficient":
        return "7_insufficient"
    return {
        "partial_field": "2_partial_field",
        "missing_ingredients": "3_missing_ingredients",
        "missing_nutrition": "4_missing_nutrition",
        "inferred_category": "5_inferred_category",
        "low_extraction": "6_low_extraction",
    }.get(sub, "2_partial_field")


if __name__ == "__main__":
    main()
