"""
TASK-413 — Diff staged output vs live snacks_frontend_v5.json
"""
import json, io, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

def load(path):
    with io.open(path, encoding="utf-8") as f:
        return json.load(f)

staged = load(r"C:\bari_snacks\03_operations\page_generator\outputs\snacks_task413_staged.json")
live = load(r"C:\Bari\bari-web\src\data\comparisons\snacks_frontend_v5.json")

staged_map = {p["barcode"]: p for p in staged["products"]}
live_map = {p["barcode"]: p for p in live["products"]}

print(f"Staged products: {len(staged_map)}")
print(f"Live products:   {len(live_map)}")
print()

live_bcs = set(live_map.keys())
staged_bcs = set(staged_map.keys())
overlap = live_bcs & staged_bcs
missing_from_staged = live_bcs - staged_bcs

print(f"Overlap (live barcodes in staged): {len(overlap)}/{len(live_bcs)}")
if missing_from_staged:
    print(f"Missing from staged: {sorted(missing_from_staged)}")
print()

REPRODUCE_THRESHOLD = 0.1

reproduced = []
grade_moves = []
score_movers = []

print("Barcode            Live  LG  Staged  SG   Delta  Status")
print("-" * 65)
for bc in sorted(overlap, key=lambda b: -(live_map[b].get("score") or 0)):
    lp = live_map[bc]
    sp = staged_map[bc]
    ls = lp.get("score")
    ss = sp.get("score")
    lg = lp.get("grade", "?")
    sg = sp.get("grade", "?")

    delta = round(ss - ls, 1) if ss is not None and ls is not None else None
    reproduces = delta is not None and abs(delta) <= REPRODUCE_THRESHOLD
    grade_moved = lg != sg

    # check task405 clean in bsip1
    task405 = ""
    for bsip_f in [f"bsip1_{bc}"]:
        import pathlib
        bsip1_path = pathlib.Path(r"C:\Bari\03_operations\bsip1\score_bars_task362_20260620_143230\output") / f"bsip1_{bc}.json"
        if bsip1_path.exists():
            d = json.loads(bsip1_path.read_text(encoding="utf-8"))
            if d.get("_task405_clean"):
                task405 = "CLEAN"

    status = "REPRODUCE" if reproduces else "DRIFT"
    print(f"{bc:18} {ls!r:6} {lg:2}  {ss!r:7} {sg:2} {str(delta):6} {status} {task405}")

    if reproduces:
        reproduced.append(bc)
    else:
        score_movers.append({
            "barcode": bc,
            "live_score": ls,
            "staged_score": ss,
            "delta": delta,
            "live_grade": lg,
            "staged_grade": sg,
            "task405_clean": task405 == "CLEAN",
        })
    if grade_moved:
        grade_moves.append({"barcode": bc, "from_grade": lg, "to_grade": sg, "delta": delta})

print()
print(f"REPRODUCE: {len(reproduced)}/{len(overlap)} (threshold ±0.1)")
print(f"GRADE MOVES: {len(grade_moves)}")
print(f"SCORE MOVERS: {len(score_movers)}")

if score_movers:
    print("\nScore-movers detail:")
    for m in score_movers:
        print(f"  {m['barcode']}: live={m['live_score']} -> staged={m['staged_score']} "
              f"(delta={m['delta']}) grade: {m['live_grade']} -> {m['staged_grade']} "
              f"{'CLEAN' if m['task405_clean'] else ''}")

if grade_moves:
    print("\n*** GRADE MOVES DETECTED — HALT CONDITION ***")
    for g in grade_moves:
        print(f"  {g}")

print()
print("--- Full score/grade distribution (staged, all 51) ---")
from collections import Counter
grades = [p.get("grade", "?") for p in staged["products"]]
scores = [p.get("score") for p in staged["products"] if p.get("score") is not None]
grade_dist = dict(sorted(Counter(grades).items()))
print(f"Grade distribution: {grade_dist}")
print(f"Score range: {min(scores):.1f} - {max(scores):.1f}")
import statistics
print(f"Score mean: {statistics.mean(scores):.1f}, stdev: {statistics.stdev(scores):.1f}")

print()
print("--- Stable barcode/score/grade table (live 21 overlap) ---")
print(f"{'Barcode':<18} {'Score':>6} {'Grade':>5}")
for bc in sorted(live_bcs):
    if bc in staged_map:
        p = staged_map[bc]
        print(f"{bc:<18} {p.get('score', 'N/A'):>6} {p.get('grade', '?'):>5}")
