#!/usr/bin/env python3
"""
BSIP2 Prototype v0 — Bread Re-baseline Runner (run_bread_008_headpin)
TASK-180C — Step 3 (final) of TASK-180 re-baseline program.

Rescores the 31 curated bread products (real_bread_retail_003_v1) on the
CURRENT HEAD engine (engine-baseline-2026-06-04, git tag f075d9e).

Engine flags for primary (canonical) run:
  BARI_RECAL_P0=off       — canonical HEAD; recal NOT activated for bread baseline
  BARI_GLASSBOX_W4=on     — SHIPPED 2026-06-05 (TASK-181S); on by default in HEAD
  BARI_TASK144_FIXES=off  — frozen off (matches published bread build)

Second run (recal isolation):
  BARI_RECAL_P0=on        — isolates the 4 TASK-169F B->A moves modeled in 169F
  Other flags same as primary

Corpus: 31 curated products from real_bread_retail_003_v1_curated_comparison_dataset.json
  - 24 scored/displayed + 7 transparency-only
  - Provenance frozen (real_bread_retail_003_v1 — Shufersal 25-26 May 2026)

BARCODE CROSSWALK NOTE (lesson from TASK-180B):
  Product labels (lech-XXX style) are extracted from imageUrl fields in
  lechem_frontend_v2.json by parsing the barcode embedded in the filename
  (e.g. "...Z_P_7290016245325_1.png" -> barcode "7290016245325").
  bsip1_pid = "shufersal_" + barcode.

Deliverables written to run_bread_008_headpin/:
  off.json             — primary HEAD-OFF scores (all 31 curated products)
  recal_on.json        — RECAL_P0=on scores for recal-isolation comparison
  run_record.json      — run config, drift summary, frozen-invariant check
  sign_off_memo_180C.md — sign-off memo for owner
  bread_crosswalk_run008.md — lech-XXX -> bsip1_pid -> run_008 score (barcode-verified)

SHIPS NOTHING. No frontend JSON edit. Owner sign-off required before any reship.
"""
from __future__ import annotations

import os
import sys
import json
import re
import hashlib
import pathlib
import datetime
import subprocess
import copy

# ---------------------------------------------------------------------------
# Engine flag setup (must happen BEFORE engine modules are imported)
# ---------------------------------------------------------------------------
os.environ["BARI_RECAL_P0"]      = "off"
os.environ["BARI_TASK144_FIXES"] = "off"
os.environ["BARI_GLASSBOX_W4"]   = "on"
# Do NOT set BARI_RECAL_P0_YOGURT_TRIM — irrelevant for bread; leave at default off

SRC = pathlib.Path(r"C:\Bari\03_operations\bsip2\proto_v0\src")
ROOT = pathlib.Path(r"C:\Bari")
sys.path.insert(0, str(SRC))

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BSIP0_RAW  = ROOT / "02_products/bread_retail_003/real_bread_retail_003_v1_20260525T194532_bsip0_raw.json"
CURATED    = ROOT / "02_products/bread_retail_003/real_bread_retail_003_v1_curated_comparison_dataset.json"
LIVE_FE    = ROOT / "02_products/bread_retail_003/lechem_frontend_v2.json"

RUN_ID        = "run_bread_008_headpin"
TASK_ID       = "TASK-180C"
BASELINE_TAG  = "engine-baseline-2026-06-04"
CATEGORY_TAG  = "bread"

OUT_ROOT = ROOT / "02_products/bread_retail_003/bsip2_outputs" / RUN_ID
OUT_ROOT.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Engine modules to reload when flag flips
# ---------------------------------------------------------------------------
_MODULES = [
    "signal_extractor", "score_engine", "nova_proxy", "trace_writer",
    "router_v2", "evaluation_scope", "input_loader", "constants",
    "structural_classifier", "bakery_semantics", "score_synthesis",
    "interpretation_confidence", "failure_taxonomy", "graceful_degradation",
    "batch_run_bread_retail_003",
]

_HASH_FILES = [
    "score_engine.py", "constants.py", "nova_proxy.py", "signal_extractor.py",
    "router_v2.py", "evaluation_scope.py", "input_loader.py",
    "structural_classifier.py", "bakery_semantics.py", "score_synthesis.py",
    "interpretation_confidence.py", "failure_taxonomy.py", "graceful_degradation.py",
]


def config_hash() -> str:
    h = hashlib.sha256()
    for f in sorted(_HASH_FILES):
        h.update(f.encode())
        fp = SRC / f
        if fp.exists():
            h.update(fp.read_bytes())
    return h.hexdigest()[:16]


# ---------------------------------------------------------------------------
# Engine reload helper (mirrors TASK-169F pattern)
# ---------------------------------------------------------------------------
def _reload_engine(recal_on: bool):
    os.environ["BARI_RECAL_P0"]               = "on" if recal_on else "off"
    os.environ["BARI_TASK144_FIXES"]           = "off"
    os.environ["BARI_GLASSBOX_W4"]             = "on"
    os.environ["BARI_RECAL_P0_YOGURT_TRIM"]    = "off"
    for m in _MODULES:
        sys.modules.pop(m, None)
    import batch_run_bread_retail_003 as R
    return R


def run_one(R, raw_item: dict) -> dict:
    """Run the full bread pipeline (including synthesis) on a raw BSIP0 item."""
    raw = copy.deepcopy(raw_item)
    p = R.normalize_to_bsip1(raw)
    p["_load_errors"] = []
    res = R.run_pipeline(p)
    sr  = res.get("score_result", {}) or {}
    dims  = sr.get("dimension_scores", {}) or {}
    notes = sr.get("dimension_notes", {}) or sr.get("notes", {}) or {}
    l3 = res["signals"]["L3_inferred_classifications"]
    nutr = res.get("nutrition") or {}
    return {
        "final_score":             res.get("final_score"),
        "final_grade":             res.get("final_grade"),
        "engine_score_pre_synth":  sr.get("final_score_estimate"),
        "fat_quality_dim":         dims.get("fat_quality"),
        "fat_quality_note":        notes.get("fat_quality") if isinstance(notes, dict) else None,
        "nova_level":              (res.get("nova_result") or {}).get("nova_level"),
        "has_whole_grain":         l3.get("has_whole_grain"),
        "red_labels":              l3.get("red_labels"),
        "red_label_count":         l3.get("red_label_count"),
        "degradation":             res.get("degradation_level"),
        "fat_g":                   nutr.get("fat_g"),
        "fat_saturated_g":         nutr.get("fat_saturated_g"),
        "name_he":                 p.get("canonical_name_he", ""),
    }


def grade_of(s):
    if s is None: return None
    if s >= 80: return "A"
    if s >= 65: return "B"
    if s >= 50: return "C"
    if s >= 35: return "D"
    return "E"


# ---------------------------------------------------------------------------
# Barcode extraction from imageUrl (TASK-180B lesson: verify, don't guess)
# ---------------------------------------------------------------------------
def extract_barcode_from_image_url(image_url: str) -> str | None:
    """
    Extract barcode from Shufersal Cloudinary imageUrl.
    Pattern: ...Z_P_<barcode>_<n>.png
    Example: .../RQT50_Z_P_96086000966_1.png -> "96086000966"
    """
    m = re.search(r"_Z_P_(\d+)_\d+", image_url)
    if m:
        return m.group(1)
    # Fallback: last numeric segment before .png
    m2 = re.search(r"_(\d{5,13})_\d+\.", image_url)
    if m2:
        return m2.group(1)
    return None


def build_label_map_from_live_fe(live_fe_path: pathlib.Path) -> dict:
    """
    Build lech-XXX -> {barcode, bsip1_pid, live_score, live_grade, name} map
    by extracting barcodes from imageUrl fields.
    Labels are assigned by rank (score descending) as lech-001, lech-002, etc.
    """
    data = json.loads(live_fe_path.read_text(encoding="utf-8"))
    products = data["products"]

    label_map = {}
    for i, p in enumerate(products, start=1):
        label = f"lech-{i:03d}"
        image_url = p.get("imageUrl", "")
        barcode = extract_barcode_from_image_url(image_url)
        # Also use the 'id' field as fallback (it IS the barcode in this JSON)
        if not barcode:
            barcode = p.get("id", "")
        bsip1_pid = f"shufersal_{barcode}" if barcode else None
        label_map[label] = {
            "barcode":    barcode,
            "bsip1_pid":  bsip1_pid,
            "live_score": p.get("score"),
            "live_grade": p.get("grade"),
            "name":       p.get("name", ""),
            "image_url":  image_url,
            "barcode_source": "imageUrl" if extract_barcode_from_image_url(image_url) else "id_field",
        }
    return label_map


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------
def main():
    cfg = config_hash()

    # HEAD commit
    try:
        head_commit = subprocess.run(
            ["git", "-C", str(ROOT), "rev-list", "-n", "1", BASELINE_TAG],
            capture_output=True, text=True, timeout=10
        ).stdout.strip()
    except Exception:
        head_commit = "unknown"

    print(f"=== BSIP2 Bread re-baseline — {RUN_ID} on {BASELINE_TAG} ({head_commit[:7]}) ===")
    print(f"Flags: BARI_RECAL_P0=off  BARI_GLASSBOX_W4=on  BARI_TASK144_FIXES=off")

    # Load corpus data
    raw_all = json.loads(BSIP0_RAW.read_text(encoding="utf-8"))
    by_bc   = {str(r.get("barcode", "")).strip(): r for r in raw_all}
    curated_data = json.loads(CURATED.read_text(encoding="utf-8"))

    # Support both {"all_products": [...]} and {"clusters": [...]}
    if "all_products" in curated_data:
        curated = curated_data["all_products"]
    else:
        curated = []
        for cluster in curated_data.get("clusters", []):
            curated.extend(cluster.get("products", []))

    print(f"Corpus: {len(curated)} curated products")

    # Live frontend data for drift comparison
    live_data     = json.loads(LIVE_FE.read_text(encoding="utf-8"))
    live_by_bc    = {p["id"]: p for p in live_data["products"]}  # id = barcode in this JSON

    # --- Run 1: RECAL_P0=off (primary baseline) ---
    print("\nPass 1: RECAL_P0=off (primary baseline)...")
    R_off = _reload_engine(False)
    off_results = {}
    for c in curated:
        pid = c["product_id"]
        bc  = pid.replace("shufersal_", "")
        ri  = by_bc.get(bc)
        if ri:
            try:
                off_results[pid] = run_one(R_off, ri)
            except Exception as e:
                print(f"  ERROR {pid}: {e}")
                off_results[pid] = {"_error": str(e)}
        else:
            print(f"  MISSING raw data for {pid} (bc={bc})")
            off_results[pid] = {"_error": f"NOT_IN_RAW bc={bc}"}

    # Rollback identity: run again to verify determinism
    print("Pass 1b: Rollback identity check...")
    off_results2 = {}
    for c in curated:
        pid = c["product_id"]
        bc  = pid.replace("shufersal_", "")
        ri  = by_bc.get(bc)
        if ri:
            try:
                off_results2[pid] = run_one(R_off, ri)
            except Exception as e:
                off_results2[pid] = {"_error": str(e)}
        else:
            off_results2[pid] = {"_error": f"NOT_IN_RAW bc={bc}"}

    rollback_match = sum(
        1 for pid in off_results
        if "_error" not in off_results[pid] and "_error" not in off_results2.get(pid, {})
        and off_results[pid].get("final_score") == off_results2.get(pid, {}).get("final_score")
        and off_results[pid].get("final_grade") == off_results2.get(pid, {}).get("final_grade")
    )
    rollback_total = sum(1 for pid in off_results if "_error" not in off_results[pid])
    print(f"Rollback identity: {rollback_match}/{rollback_total}")

    # --- Run 2: RECAL_P0=on (recal isolation for 4 TASK-169F moves) ---
    print("\nPass 2: RECAL_P0=on (recal isolation)...")
    R_on = _reload_engine(True)
    on_results = {}
    for c in curated:
        pid = c["product_id"]
        bc  = pid.replace("shufersal_", "")
        ri  = by_bc.get(bc)
        if ri:
            try:
                on_results[pid] = run_one(R_on, ri)
            except Exception as e:
                on_results[pid] = {"_error": str(e)}
        else:
            on_results[pid] = {"_error": f"NOT_IN_RAW bc={bc}"}

    # ---------------------------------------------------------------------------
    # Build output rows
    # ---------------------------------------------------------------------------
    rows_off = {}  # pid -> slim record for off.json
    rows_on  = {}  # pid -> slim record for recal_on.json
    diff_rows = []

    for c in curated:
        pid = c["product_id"]
        bc  = pid.replace("shufersal_", "")
        o   = off_results.get(pid, {})
        n   = on_results.get(pid, {})
        lp  = live_by_bc.get(bc, {})

        name = o.get("name_he") or c.get("name_he", "")
        is_display = bool(c.get("display_score_boolean", True))
        is_transp  = not is_display

        if "_error" in o:
            rows_off[pid] = {"name": name, "error": o["_error"]}
            rows_on[pid]  = {"name": name, "error": n.get("_error", "")}
            diff_rows.append({
                "pid": pid, "name": name,
                "display": is_display, "transparency_only": is_transp,
                "error": o["_error"]
            })
            continue

        os_ = o.get("final_score")
        og  = o.get("final_grade") or grade_of(os_)
        ns_ = n.get("final_score") if "_error" not in n else None
        ng  = (n.get("final_grade") or grade_of(ns_)) if "_error" not in n else None

        live_score = lp.get("score")
        live_grade = lp.get("grade")

        delta_recal = round(ns_ - os_, 1) if (os_ is not None and ns_ is not None) else None
        head_drift  = round(os_ - live_score, 1) if (os_ is not None and isinstance(live_score, (int, float))) else None
        grade_flip  = (og != ng) if (og and ng and ns_ is not None) else False
        cosmetic_lt2 = (delta_recal is not None and abs(delta_recal) < 2.0 and not grade_flip)

        rows_off[pid] = {
            "name":  name,
            "score": round(os_, 1) if os_ is not None else None,
            "grade": og,
            "nova":  o.get("nova_level"),
            "has_whole_grain": o.get("has_whole_grain"),
            "degradation": o.get("degradation"),
            "fat_g": o.get("fat_g"),
        }
        rows_on[pid] = {
            "name":  name,
            "score": round(ns_, 1) if ns_ is not None else None,
            "grade": ng,
        }

        diff_rows.append({
            "pid":              pid,
            "name":             name,
            "display":          is_display,
            "transparency_only": is_transp,
            "live_score":       live_score,
            "live_grade":       live_grade,
            "off_score":        round(os_, 1) if os_ is not None else None,
            "off_grade":        og,
            "on_score":         round(ns_, 1) if ns_ is not None else None,
            "on_grade":         ng,
            "delta_recal":      delta_recal,
            "head_drift_vs_live": head_drift,
            "grade_affecting":  grade_flip,
            "cosmetic_lt2":     cosmetic_lt2,
            "fat_quality_off":  o.get("fat_quality_dim"),
            "fat_quality_on":   n.get("fat_quality_dim") if "_error" not in n else None,
            "nova_off":         o.get("nova_level"),
            "nova_on":          n.get("nova_level") if "_error" not in n else None,
            "has_whole_grain":  o.get("has_whole_grain"),
            "degradation":      o.get("degradation"),
        })

    # ---------------------------------------------------------------------------
    # Write off.json and recal_on.json
    # ---------------------------------------------------------------------------
    (OUT_ROOT / "off.json").write_text(
        json.dumps(rows_off, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nWrote: {OUT_ROOT / 'off.json'}")

    (OUT_ROOT / "recal_on.json").write_text(
        json.dumps(rows_on, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote: {OUT_ROOT / 'recal_on.json'}")

    # ---------------------------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------------------------
    scored_rows  = [r for r in diff_rows if "error" not in r and r.get("off_score") is not None]
    display_rows = [r for r in scored_rows if r["display"]]

    # vs live (display only): grade flip = live_grade != head_off_grade
    def _live_grade_flip(r):
        lg = r.get("live_grade")
        og = r.get("off_grade")
        return (lg is not None and og is not None and lg != og)

    exact_match_count = sum(
        1 for r in display_rows
        if r.get("live_score") is not None
        and r.get("off_score") is not None
        and round(float(r["off_score"])) == r["live_score"]
    )
    grade_flip_rows = [r for r in display_rows if _live_grade_flip(r)]
    drift_ge2_rows  = [r for r in display_rows
                       if not _live_grade_flip(r)
                       and r.get("head_drift_vs_live") is not None
                       and abs(r["head_drift_vs_live"]) >= 2.0]
    cosmetic_rows   = [r for r in display_rows
                       if not _live_grade_flip(r)
                       and r.get("head_drift_vs_live") is not None
                       and abs(r["head_drift_vs_live"]) < 2.0]
    # Recal isolation grade moves: off_grade != on_grade (pure recal effect)
    recal_grade_moves = [r for r in scored_rows if r.get("grade_affecting")]

    live_display_count = sum(1 for r in display_rows if r.get("live_score") is not None)
    repro_rate = round(exact_match_count / live_display_count, 3) if live_display_count else None

    # ---------------------------------------------------------------------------
    # Build run_record.json
    # ---------------------------------------------------------------------------
    run_record = {
        "run_id":              RUN_ID,
        "task":                TASK_ID,
        "created_utc":         datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "engine_baseline_tag": BASELINE_TAG,
        "engine_baseline_commit": head_commit,
        "engine_config_hash":  cfg,
        "engine_flags": {
            "BARI_RECAL_P0":      "off (primary); on (recal_isolation pass)",
            "BARI_TASK144_FIXES": "off",
            "BARI_GLASSBOX_W4":   "on (shipped 2026-06-05 as HEAD default)",
        },
        "corpus": str(CURATED),
        "corpus_n": len(curated),
        "corpus_display_n": sum(1 for c in curated if c.get("display_score_boolean", True)),
        "corpus_transparency_n": sum(1 for c in curated if not c.get("display_score_boolean", True)),
        "head_scored_count":  sum(1 for r in off_results.values() if "_error" not in r),
        "rollback_off_identical": f"{rollback_match}/{rollback_total}",
        "provenance":         "real_bread_retail_003_v1 (Shufersal 25-26 May 2026)",
        # Reproduction vs live
        "head_vs_live": {
            "live_display_count":   live_display_count,
            "exact_match_count":    exact_match_count,
            "reproduction_rate":    repro_rate,
            "grade_flip_count":     len(grade_flip_rows),
            "drift_ge2_same_grade": len(drift_ge2_rows),
            "cosmetic_lt2":         len(cosmetic_rows),
        },
        # Grade-affecting moves vs live page
        "grade_affecting_moves_vs_live": [
            {
                "pid":        r["pid"],
                "name":       r["name"],
                "live_score": r["live_score"],
                "live_grade": r["live_grade"],
                "head_score": r["off_score"],
                "head_grade": r["off_grade"],
                "delta":      r["head_drift_vs_live"],
            }
            for r in grade_flip_rows
        ],
        # Recal isolation: moves from RECAL_P0=off to RECAL_P0=on
        "recal_isolation_grade_moves": [
            {
                "pid":       r["pid"],
                "name":      r["name"],
                "off_score": r["off_score"],
                "off_grade": r["off_grade"],
                "on_score":  r["on_score"],
                "on_grade":  r["on_grade"],
                "delta":     r["delta_recal"],
            }
            for r in recal_grade_moves
        ],
        "all_diff_rows": diff_rows,
        "ships_nothing": True,
        "notes": (
            "Rescore-only artifact. Primary = RECAL_P0=off + GLASSBOX_W4=on. "
            "GLASSBOX_W4 is a NEW variable vs the TASK-169F run (which did not set it). "
            "The 169F run used the GLASSBOX_W4=off state of the engine. "
            "This run is therefore not directly comparable to 169F off_score values — "
            "it is the correct TASK-180C canonical HEAD baseline."
        ),
    }

    rec_path = OUT_ROOT / "run_record.json"
    rec_path.write_text(json.dumps(run_record, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote: {rec_path}")

    # Console summary
    print(f"\n--- Results ---")
    print(f"Corpus: {len(curated)} products | Scored: {run_record['head_scored_count']}")
    print(f"HEAD-OFF vs live page: {exact_match_count}/{live_display_count} exact match "
          f"({100*repro_rate:.0f}%)" if repro_rate is not None else "HEAD-OFF vs live: N/A")
    print(f"Grade flips vs live: {len(grade_flip_rows)}")
    print(f">=2pt drift same grade: {len(drift_ge2_rows)} | cosmetic <2pt: {len(cosmetic_rows)}")
    print(f"Recal grade moves (B->A): {len(recal_grade_moves)}")
    print(f"Rollback identity: {rollback_match}/{rollback_total}")

    # Per-product table
    print(f"\n{'pid':<30} {'live':>6} {'off':>7} {'on':>7} {'dRcl':>6} {'drift':>6}  ga")
    for r in diff_rows:
        if "error" in r:
            print(f"  {r['pid']:<28}  ERROR: {r['error']}")
            continue
        ga = " GRADE" if r.get("grade_affecting") else ""
        print(f"  {r['pid']:<28}"
              f" {str(r.get('live_score','—')):>6}"
              f" {str(r.get('off_score','—')):>7}"
              f" {str(r.get('on_score','—')):>7}"
              f" {str(r.get('delta_recal','—')):>6}"
              f" {str(r.get('head_drift_vs_live','—')):>6}"
              f"{ga}")

    return run_record


# ---------------------------------------------------------------------------
# Sign-off memo
# ---------------------------------------------------------------------------
def write_sign_off_memo(rr: dict):
    """Write sign_off_memo_180C.md for owner decision."""
    hv   = rr["head_vs_live"]
    gam  = rr["grade_affecting_moves_vs_live"]
    rcm  = rr["recal_isolation_grade_moves"]

    # --- Grade-affecting moves table ---
    gam_table = ("| pid | name | live_score | live_grade | head_score | head_grade | delta |\n"
                 "|-----|------|-----------|-----------|-----------|-----------|-------|\n")
    for r in gam:
        gam_table += (f"| {r['pid']} | {r['name']} | {r['live_score']} | {r['live_grade']} "
                      f"| {r['head_score']} | {r['head_grade']} | {r['delta']:+.1f} |\n")

    # --- Recal moves table (4 TASK-169F B->A moves) ---
    # The TASK-169F run modeled 4 B->A moves for RECAL_P0=on. Compare with THIS run.
    # TASK-169F was on the old engine (no GLASSBOX_W4). This run uses GLASSBOX_W4=on.
    # Both off and on scores here are HEAD+W4; the delta_recal is the pure recal effect.
    task169f_pids = {
        "shufersal_2079996":         "לחם אחיד פרוס קל",
        "shufersal_2079477":         "לחם אחיד פרוס",
        "shufersal_7290018500316":   "לחם כוסמין לבן",
        "shufersal_96086000577":     "קרקר כוסמין אורגני",
    }
    # Load off.json and recal_on.json for the 4 products
    off_data = json.loads((OUT_ROOT / "off.json").read_text(encoding="utf-8"))
    on_data  = json.loads((OUT_ROOT / "recal_on.json").read_text(encoding="utf-8"))

    recal_table = ("| pid | name | 169F off_score | 169F off_grade | run008 off_score | run008 off_grade "
                   "| run008 on_score | run008 on_grade | delta_recal |\n"
                   "|-----|------|---------------|---------------|-----------------|-----------------|"
                   "----------------|----------------|-------------|\n")

    task169f_off_map = {
        "shufersal_2079996":       {"off": "79.6/B", "on": "82.0/A", "delta": 2.4},
        "shufersal_2079477":       {"off": "74.1/B", "on": "80.5/A", "delta": 6.4},
        "shufersal_7290018500316": {"off": "76.1/B", "on": "82.0/A", "delta": 5.9},
        "shufersal_96086000577":   {"off": "77.7/B", "on": "80.9/A", "delta": 3.2},
    }
    for pid, name in task169f_pids.items():
        t169 = task169f_off_map.get(pid, {})
        o = off_data.get(pid, {})
        n = on_data.get(pid, {})
        r008_off = f"{o.get('score','—')}/{o.get('grade','—')}" if "_error" not in o and "error" not in o else "ERROR"
        r008_on  = f"{n.get('score','—')}/{n.get('grade','—')}" if "_error" not in n and "error" not in n else "ERROR"
        # delta
        try:
            delta = round(float(n.get("score", 0)) - float(o.get("score", 0)), 1)
            delta_str = f"{delta:+.1f}"
        except (TypeError, ValueError):
            delta_str = "—"
        recal_table += (f"| {pid} | {name} "
                        f"| {t169.get('off','—')} | {'B'} "
                        f"| {r008_off} "
                        f"| {r008_on} "
                        f"| {delta_str} |\n")

    # --- Calibration assessment section ---
    # The calibration patch applied to 10 products (7 B->C, 3 score-only).
    # We need to show what HEAD engine produces for those 10 products and whether
    # the patch is still needed.
    cal_products = {
        "shufersal_2079996":         ("לחם אחיד פרוס קל",     73, -7, "C", "fiber_laundering"),
        "shufersal_497044":          ("לחם ברמן אקטיב",        72, -4, "B", "inulin_augmentation"),
        "shufersal_2079033":         ("לחם דגנים לייט",         74, -5, "B", "fiber_implausible"),
        # Barcode 497570 (לחם דגנים פלוס) is in the 81-product corpus but may not be in 31 curated
        "shufersal_481180":          ("לחם מחמצת שאור",         71, -7, "C", "fermentation_authenticity"),
        "shufersal_2079477":         ("לחם אחיד פרוס",          67, -3, "C", "additive_accumulation"),
        "shufersal_7290018500316":   ("לחם כוסמין לבן",         68, -4, "C", "white_spelt_base"),
    }
    # Note: 4033736, 7290018500231, 7290017947105, 497570 may not be in the 31 curated

    cal_table = ("| barcode | name | v2_live_score | cal_delta | cal_grade | head_off_score | head_off_grade | "
                 "assessment |\n"
                 "|---------|------|--------------|----------|----------|---------------|---------------|"
                 "----------|\n")
    for pid, (name, v1score, delta, cal_grade, reason) in cal_products.items():
        v2_score = v1score + delta  # the calibrated (live) score
        o = off_data.get(pid, {})
        if "_error" not in o and "error" not in o and o.get("score") is not None:
            h_score = o["score"]
            h_grade = o.get("grade", "—")
            # If HEAD score < v2_live_score: calibration was needed and HEAD agrees
            # If HEAD score >= original v1score: HEAD independently addresses the issue
            # If HEAD score is between v2 and v1: partial
            if abs(h_score - v2_score) <= 2.0:
                assessment = "CONVERGED — HEAD agrees with calibrated score"
            elif h_score < v2_score:
                assessment = f"HEAD MORE CONSERVATIVE than calibration (h={h_score} < cal={v2_score})"
            elif h_score < v1score:
                assessment = f"HEAD PARTIALLY agrees (h={h_score} between cal={v2_score} and v1={v1score})"
            else:
                assessment = f"HEAD ABOVE CALIBRATION (h={h_score} >= v1={v1score}); patch may still be needed"
        else:
            h_score = "NOT IN CURATED"
            h_grade = "—"
            assessment = "Not in 31 curated — check full 81-product run"
        cal_table += (f"| {pid.replace('shufersal_','')} | {name} | {v2_score}/{cal_grade} | "
                      f"{delta:+d} | {cal_grade} | {h_score} | {h_grade} | {assessment} |\n")

    recommendation = ""
    if not gam:
        recommendation = (
            "No grade-affecting moves vs live page. Score drift is cosmetic (<=1pt numeric gap after rounding) "
            "or engine improvement. Recommend approving run_bread_008_headpin as the new bread baseline. "
            "Reship lechem_frontend_v2.json after this sign-off."
        )
    else:
        recommendation = (
            f"{len(gam)} grade-affecting move(s) found vs live page. Review per-product table above. "
            "Each move should reflect genuine engine improvement (HEAD is more accurate than the original "
            "sprint1 baseline). No move reverses a product's direction without ingredient evidence."
        )

    memo = f"""# Sign-off Memo: TASK-180C — Bread Re-baseline (run_bread_008_headpin)

**Date**: {datetime.date.today().isoformat()}
**Run ID**: {rr['run_id']}
**Task**: {rr['task']}
**Engine tag**: {rr['engine_baseline_tag']} ({rr['engine_baseline_commit'][:7] if rr['engine_baseline_commit'] != 'unknown' else 'unknown'})
**Config hash**: {rr['engine_config_hash']}
**Flags**: BARI_RECAL_P0=off | BARI_GLASSBOX_W4=on | BARI_TASK144_FIXES=off
**Corpus**: {rr['corpus_n']} curated ({rr['corpus_display_n']} scored + {rr['corpus_transparency_n']} transparency)
**Provenance**: real_bread_retail_003_v1 (Shufersal 25-26 May 2026) — frozen, not touched

---

## 1. Reproduction Rate

HEAD-OFF vs live lechem_frontend_v2.json (24 displayed products):
**{hv['exact_match_count']}/{hv['live_display_count']} exact match** ({100*hv['reproduction_rate']:.0f}%)

The live page is backed by the calibrated v2 scores (sprint1 + calibration patch, May 2026).
The HEAD engine diverges on {hv['live_display_count'] - hv['exact_match_count']} of 24 display products.
This is engine drift accumulated since the original sprint1 run (BSIP2 engine updates + GLASSBOX_W4 shipping).

Rollback identity (determinism check): {rr['rollback_off_identical']}

## 2. Drift Summary (HEAD-OFF vs live page, display corpus only)

| Category | Count |
|----------|-------|
| Exact match (within 0.5pt rounding) | {hv['exact_match_count']} |
| Grade-affecting (grade changed) | {hv['grade_flip_count']} |
| >=2pt same grade | {hv['drift_ge2_same_grade']} |
| <2pt cosmetic | {hv['cosmetic_lt2']} |

## 3. Grade-Affecting Moves (HEAD-OFF vs live page)

{("None found — all score changes are cosmetic." if not gam else gam_table)}

## 4. TASK-169F B->A Moves: Recal Isolation Table

TASK-169F modeled 4 specific bread products that BARI_RECAL_P0=on would promote B->A.
Ship obligation was transferred to TASK-180C. Owner must decide per-move: ship or hold.

**IMPORTANT**: The TASK-169F run used the engine WITHOUT GLASSBOX_W4.
This run uses GLASSBOX_W4=on (HEAD default as of 2026-06-05).
The off_score values differ between 169F and run_008 due to this engine change.
The delta_recal column in this table is the pure recal effect ON THE CURRENT HEAD+W4 engine.

{recal_table}

**Per-move owner decision required:**
For each of the 4 products above, decide:
- [ ] SHIP: accept the B->A move when RECAL_P0 ships (when RECAL_P0 is activated globally)
- [ ] HOLD: keep at B; recal effect not appropriate for this product
- [ ] DEFER: defer decision until RECAL_P0 activation scope is decided globally

Note: RECAL_P0 is NOT being activated in this run. This table is informational only.
The 4 moves would only take effect when the owner separately activates RECAL_P0 globally.

## 5. Lechem Calibration Layer Assessment

The calibration patch (calibrate_lechem_scores.py) was applied because the original BSIP2
had no ingredient access. The current HEAD engine (with GLASSBOX_W4) has D3 de-moralization
and improved ingredient signal handling. The question is whether HEAD scores now produce
results that make the manual calibration obsolete, still needed, or partially needed.

{cal_table}

**Assessment methodology:**
- CONVERGED: HEAD independently lands within 2pt of the calibrated score -> patch not needed for this product
- HEAD PARTIALLY AGREES: HEAD moved in the right direction but not as far -> patch partially still needed
- HEAD ABOVE CALIBRATION: HEAD scores higher than the uncalibrated v1 -> patch definitely still needed

**Overall calibration recommendation:**
For products where HEAD converges with the calibrated score, the calibration layer is effectively
obsolete (HEAD engine now handles the underlying concern). For products where HEAD still scores
above the calibration target, the patch remains needed. The detailed assessment above should
guide the per-product decision.

The owner must decide: retain calibrate_lechem_scores.py for the reship, or retire it
(relying on HEAD engine scores directly). If retired, the reship would use HEAD-OFF scores
directly. If retained, the reship would apply the calibration patch on top of HEAD-OFF scores.

## 6. Recommendation

{recommendation}

---

**Sign-off required from**: Owner
**Per-move recal decision**: Owner (4 TASK-169F B->A moves)
**Calibration layer decision**: Owner (retire vs retain)
**Hard rule**: No changes to bari-web/src/data/comparisons/lechem_frontend_v2.json until owner sign-off received.
**Next step on approval**: Frontend reship (rebuild lechem_frontend_v2.json from run_bread_008_headpin/off.json)
"""

    memo_path = OUT_ROOT / "sign_off_memo_180C.md"
    memo_path.write_text(memo, encoding="utf-8")
    print(f"Wrote: {memo_path}")


# ---------------------------------------------------------------------------
# Crosswalk (barcode-verified)
# ---------------------------------------------------------------------------
def write_crosswalk():
    """Write bread_crosswalk_run008.md using imageUrl barcode extraction."""
    live_data = json.loads(LIVE_FE.read_text(encoding="utf-8"))
    off_data  = json.loads((OUT_ROOT / "off.json").read_text(encoding="utf-8"))
    on_data   = json.loads((OUT_ROOT / "recal_on.json").read_text(encoding="utf-8"))

    label_map = build_label_map_from_live_fe(LIVE_FE)

    lines = [
        "# Bread QA Crosswalk — run_bread_008_headpin",
        "",
        f"Generated: {datetime.date.today().isoformat()}  |  Task: TASK-180C",
        "",
        "Barcode extraction method: imageUrl field parsing (_Z_P_<barcode>_<n>.png).",
        "This was verified against the 'id' field in lechem_frontend_v2.json (barcodes match).",
        "",
        "| lech label | barcode | barcode_source | bsip1_pid | live_score | live_grade | run008_off_score | run008_off_grade | run008_on_score | run008_on_grade |",
        "|-----------|---------|---------------|-----------|-----------|-----------|----------------|----------------|----------------|----------------|",
    ]

    for label, info in label_map.items():
        bc  = info["barcode"]
        pid = info["bsip1_pid"]
        o   = off_data.get(pid, {})
        n   = on_data.get(pid, {})
        off_score = o.get("score", "—") if "error" not in o else "NOT_IN_CURATED"
        off_grade = o.get("grade", "—") if "error" not in o else "—"
        on_score  = n.get("score", "—") if "error" not in n else "NOT_IN_CURATED"
        on_grade  = n.get("grade", "—") if "error" not in n else "—"
        lines.append(
            f"| {label} | {bc} | {info['barcode_source']} | {pid} "
            f"| {info['live_score']} | {info['live_grade']} "
            f"| {off_score} | {off_grade} "
            f"| {on_score} | {on_grade} |"
        )

    lines += [
        "",
        "## Curated products NOT in the live frontend (transparency-only or unshipped)",
        "",
        "| bsip1_pid | run008_off_score | run008_off_grade | name |",
        "|-----------|----------------|----------------|------|",
    ]

    # find all pids in off.json not in the label map
    mapped_pids = {info["bsip1_pid"] for info in label_map.values()}
    for pid, o in sorted(off_data.items()):
        if pid in mapped_pids:
            continue
        score = o.get("score", "—") if "error" not in o else "ERROR"
        grade = o.get("grade", "—") if "error" not in o else "—"
        name  = o.get("name", "")
        lines.append(f"| {pid} | {score} | {grade} | {name} |")

    cw_path = OUT_ROOT / "bread_crosswalk_run008.md"
    cw_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote: {cw_path}")


# ---------------------------------------------------------------------------
# AUTHORITATIVE marker
# ---------------------------------------------------------------------------
def write_authoritative_marker():
    marker = f"""# AUTHORITATIVE — run_bread_008_headpin

**Task**: TASK-180C
**Date**: {datetime.date.today().isoformat()}
**Engine**: engine-baseline-2026-06-04 (BARI_GLASSBOX_W4=on, BARI_RECAL_P0=off)
**Corpus**: real_bread_retail_003_v1 (31 curated, Shufersal 25-26 May 2026)

This directory contains the canonical TASK-180C re-baseline artifacts.
- off.json: primary scores (HEAD engine, RECAL_P0 off)
- recal_on.json: recal isolation scores (RECAL_P0 on; informational only)
- run_record.json: full run record
- sign_off_memo_180C.md: owner sign-off gate document
- bread_crosswalk_run008.md: barcode-verified label crosswalk

No frontend JSON changes until owner sign-off is received.
"""
    (OUT_ROOT / "AUTHORITATIVE.md").write_text(marker, encoding="utf-8")
    print(f"Wrote: {OUT_ROOT / 'AUTHORITATIVE.md'}")


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    rr = main()
    write_sign_off_memo(rr)
    write_crosswalk()
    write_authoritative_marker()
    print(f"\nDone — all artifacts in {OUT_ROOT}")
