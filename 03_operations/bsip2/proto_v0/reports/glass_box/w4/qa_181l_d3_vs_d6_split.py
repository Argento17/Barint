"""TASK-181L QA — decompose the residual ON moves: is the move from D3 score, or
from the D6 −5 confidence dent hitting the ceiling / insufficient gate?

For every product, compare OFF vs ON on:
  - processing_quality dim (D3 score) : should be IDENTICAL for non_material
  - confidence_score                  : the −5 dent
  - confidence_ceiling_applied        : did a ceiling clamp the final score?
  - grade flip to insufficient_data   : did confidence cross 40?
"""
import os, sys, json, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "src"))

CORPORA = {
    "hummus":      r"C:\Bari\02_products\hummus\canonical_bsip1",
    "maadanim":    r"C:\Bari\03_operations\bsip1\run_maadanim_001\output",
    "snack_bars":  r"C:\Bari\03_operations\bsip1\run_001\output",
    "golden_milk": r"C:\Bari\03_operations\bsip1\run_milk_002\output",
}
_MODULES = ["signal_extractor", "score_engine", "nova_proxy", "trace_writer",
            "router_v2", "evaluation_scope", "input_loader", "constants",
            "structural_classifier"]

def _score(source, w4_on):
    os.environ["BARI_GLASSBOX_W4"] = "on" if w4_on else "off"
    for f in ["D5D6", "W2", "W15"]:
        os.environ[f"BARI_GLASSBOX_{f}"] = "off"
    os.environ["BARI_RECAL_P0"] = "off"; os.environ["BARI_TASK144_FIXES"] = "off"
    for m in _MODULES:
        sys.modules.pop(m, None)
    import io, contextlib
    from input_loader import load_batch
    from signal_extractor import extract_signals
    from router_v2 import classify_category
    from nova_proxy import infer_nova
    from evaluation_scope import assign_evaluation_scope
    from score_engine import score_product
    out = {}
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
        prods = list(load_batch(pathlib.Path(source)))
    for p in prods:
        pid = p.get("canonical_product_id")
        try:
            sig = extract_signals(p); cat = classify_category(p)
            nova = infer_nova(p, sig["L3_inferred_classifications"])
            ev = assign_evaluation_scope(p, cat["category"])
            out[pid] = score_product(p, sig, cat, nova, ev)
        except Exception as e:
            out[pid] = {"_error": repr(e)}
    return out

d3_moved_nonmaterial = 0
d3_moved_material = 0
d3_moved_low = 0
score_move_no_d3_move = 0       # final score moved but D3 dim did NOT — => D6 side-effect
ceiling_clamp_moves = 0
insufficient_flips = 0
examples = []

for name, src in CORPORA.items():
    if not pathlib.Path(src).exists():
        continue
    off = _score(src, False); on = _score(src, True)
    for pid, r in on.items():
        o = off.get(pid, {})
        d3_off = o.get("dimension_scores", {}).get("processing_quality")
        d3_on  = r.get("dimension_scores", {}).get("processing_quality")
        s_off, s_on = o.get("final_score_estimate"), r.get("final_score_estimate")
        g_off, g_on = o.get("grade_estimate"), r.get("grade_estimate")
        sig = r.get("d3_processing_signal") or {}
        mat = sig.get("uncertainty_materiality"); band = sig.get("confidence")
        d3_moved = (d3_off != d3_on)
        if d3_moved:
            if band == "low": d3_moved_low += 1
            elif mat == "material": d3_moved_material += 1
            elif mat == "non_material": d3_moved_nonmaterial += 1
        # final-score move with NO D3-dim move => attributable to D6 confidence dent
        if (s_off is not None and s_on is not None and s_off != s_on and not d3_moved):
            score_move_no_d3_move += 1
            if r.get("confidence_ceiling_applied") and not o.get("confidence_ceiling_applied"):
                ceiling_clamp_moves += 1
        if g_off != "insufficient_data" and g_on == "insufficient_data":
            insufficient_flips += 1
        if g_off != g_on and len(examples) < 20:
            examples.append({
                "pid": pid, "corpus": name, "g": f"{g_off}->{g_on}",
                "score": f"{s_off}->{s_on}", "d3_dim": f"{d3_off}->{d3_on}",
                "d3_moved": d3_moved, "mat": mat,
                "conf_off": o.get("confidence_result", {}).get("confidence_score"),
                "conf_on": r.get("confidence_result", {}).get("confidence_score"),
                "ceiling_off": o.get("confidence_ceiling_applied"),
                "ceiling_on": r.get("confidence_ceiling_applied"),
            })

print("D3 dim moved | non_material:", d3_moved_nonmaterial,
      " material:", d3_moved_material, " low:", d3_moved_low)
print("final-score moves with NO D3-dim move (=> D6 confidence side-effect):", score_move_no_d3_move)
print("  of which a NEW confidence ceiling clamp appeared:", ceiling_clamp_moves)
print("grade flips to insufficient_data (confidence crossed 40):", insufficient_flips)
print("\nGRADE-CHANGE EXAMPLES:")
for e in examples:
    print(" ", json.dumps(e, ensure_ascii=False))
