"""Diagnostic: re-score 3 big snack movers through the current engine (TASK-371 step 1)."""
import sys, json, pathlib, os

ROOT = pathlib.Path(r"C:\Bari")
SRC = ROOT / "03_operations" / "bsip2" / "proto_v0" / "src"
sys.path.insert(0, str(SRC))
sys.path.insert(0, str(ROOT / "02_products" / "snack_bars"))
sys.path.insert(0, str(ROOT / "03_operations" / "bsip0" / "scrape" / "_shared"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import run_task360_phase3 as P3

BARCODES = ["7290011498986", "7290011498917", "7290011498900"]
BSIP1_DIR = ROOT / "03_operations" / "bsip1" / "score_bars_task362_20260620_150421" / "output"
OUT_DIR = ROOT / "03_operations" / "bsip2" / "proto_v0" / "diag_task371_step1" / "products"
OUT_DIR.mkdir(parents=True, exist_ok=True)

for bc in BARCODES:
    p = BSIP1_DIR / f"bsip1_{bc}.json"
    if not p.exists():
        print(f"MISSING: {bc}")
        continue
    res = P3.run_bsip2(p, OUT_DIR)
    if res["status"] != "ok":
        print(f"ERROR {bc}: {res.get('error')}")
        continue
    tr = res["trace"]
    score = tr.get("final_score_estimate", tr.get("score"))
    grade = tr.get("grade_estimate", tr.get("grade"))
    cat   = tr.get("category")
    nova  = tr.get("nova_group", tr.get("nova"))
    caps  = tr.get("caps_applied", tr.get("active_caps", []))
    dims  = tr.get("dimension_scores", {})
    print(f"\n=== BC={bc} ===")
    print(f"  score={score} grade={grade} cat={cat} nova={nova}")
    print(f"  caps={caps}")
    print(f"  dims={dims}")
