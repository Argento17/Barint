#!/usr/bin/env python3
"""
TASK-254/F1 — Compare reconstructed traces vs live frontend for all 34 cereals.
Outputs match table and summary.
"""

import json, pathlib

FE_PATH = pathlib.Path(r"C:\Bari\bari-web\src\data\comparisons\cereals_frontend_v2.json")
OUT = pathlib.Path(r"C:\Bari\02_products\breakfast_cereals\bsip2_outputs\run_cereals_008_reconstruction\comparison_table.txt")
R008 = pathlib.Path(r"C:\Bari\02_products\breakfast_cereals\bsip2_outputs\run_cereals_008_reconstruction\products")
RMT = pathlib.Path(r"C:\Bari\02_products\breakfast_cereals\bsip2_outputs\run_cereals_multiretailer_001_reconstruction\products")
ORIG_R008 = pathlib.Path(r"C:\Bari\02_products\breakfast_cereals\bsip2_outputs\run_cereals_008\products")

def load_trace(pid, run_dir):
    d = run_dir / pid
    if d.exists():
        for f in d.iterdir():
            if f.name == "bsip2_trace.json":
                return json.loads(f.read_text("utf-8"))
    return None

def get_score(trace):
    return trace.get("final_score_estimate") if trace else None

def get_grade(trace):
    return trace.get("grade_estimate") if trace else None

fe = json.loads(FE_PATH.read_text("utf-8"))
products = fe["products"]

rows = []
for p in products:
    pid = p["id"]
    live_score = p["score"]
    live_grade = p["grade"]

    # Check reconstruction traces
    t8 = load_trace(pid, R008)
    tmt = load_trace(pid, RMT)
    t_orig = load_trace(pid, ORIG_R008)

    recon_score = None
    recon_grade = None
    source_run = None

    if t8:
        recon_score = round(get_score(t8))
        recon_grade = get_grade(t8)
        source_run = "run_cereals_008"
    elif tmt:
        recon_score = round(get_score(tmt))
        recon_grade = get_grade(tmt)
        source_run = "run_cereals_multiretailer_001"
    else:
        source_run = "NO_TRACE_FOUND"

    match = (live_score == recon_score and live_grade == recon_grade) if recon_score is not None else "N/A"
    if recon_score is not None and not match:
        match = False

    rows.append({
        "pid": pid,
        "barcode": p.get("barcode", ""),
        "name": p["name"][:40],
        "live_score": live_score,
        "live_grade": live_grade,
        "recon_score": recon_score,
        "recon_grade": recon_grade,
        "source_run": source_run,
        "match": match,
    })

# Write to output file
with open(OUT, "w", encoding="utf-8") as f:
    f.write(f"{'Product ID':35s} {'Name':40s} {'Live':8s} {'Recon':8s} {'Match':7s} {'Source Run'}\n")
    f.write("-" * 130 + "\n")
    match_count = 0
    mismatch_count = 0
    no_trace_count = 0
    worst = None
    for r in rows:
        match_str = str(r["match"]) if r["match"] is not None else "N/A"
        live_str = f"{r['live_score']}/{r['live_grade']}"
        recon_str = f"{r['recon_score']}/{r['recon_grade']}" if r['recon_score'] is not None else "MISSING"
        f.write(f"{r['pid']:35s} {r['name']:40s} {live_str:8s} {recon_str:8s} {match_str:7s} {r['source_run']}\n")

        if r["match"] is True:
            match_count += 1
        elif r["match"] is False:
            mismatch_count += 1
            diff = abs(r["live_score"] - r["recon_score"])
            if worst is None or diff > worst["diff"]:
                worst = {**r, "diff": diff}
        else:
            no_trace_count += 1

    f.write("\n")
    f.write("=" * 80 + "\n")
    f.write(f"MATCH:     {match_count}/{len(rows)}\n")
    f.write(f"MISMATCH:  {mismatch_count}/{len(rows)}\n")
    f.write(f"NO TRACE:  {no_trace_count}/{len(rows)}\n")
    if worst:
        f.write(f"WORST:     {worst['pid']} ({worst['name']}) live={worst['live_score']}/{worst['live_grade']} recon={worst['recon_score']}/{worst['recon_grade']} diff={worst['diff']}pts\n")

    # Also check original run_cereals_008 traces
    f.write("\n--- Original run_cereals_008 product count check ---\n")
    orig_count = sum(1 for d in ORIG_R008.iterdir() if d.is_dir())
    f.write(f"Original run_cereals_008 products/: {orig_count} dirs\n")
    recon_count = sum(1 for d in R008.iterdir() if d.is_dir())
    f.write(f"Reconstructed run_cereals_008 products/: {recon_count} dirs\n")

    # Check for engine version
    sample_trace = None
    for r in rows:
        if r["source_run"] == "run_cereals_008" and r["recon_score"] is not None:
            t = load_trace(r["pid"], R008)
            if t:
                sample_trace = t
                break

    if sample_trace:
        f.write(f"\n--- Engine version ---\n")
        f.write(f"bsip2_version: {sample_trace.get('bsip2_version')}\n")
        f.write(f"algorithm_version: {sample_trace.get('algorithm_version')}\n")
        f.write(f"trace_generated_at: {sample_trace.get('trace_generated_at')}\n")

print(f"Comparison written to {OUT}")
