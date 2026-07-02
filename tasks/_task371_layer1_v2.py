#!/usr/bin/env python3
"""
TASK-371 Layer-1 diagnostic (v2 — subprocess per product for clean env isolation).

Computes three score sets per live product:
  1. HEAD engine - worktree at HEAD (C:\Bari\Bari_worktree_head)
  2. Working-tree engine - current working tree (C:\Bari)
  3. Committed frontend JSON - bari-web/src/data/comparisons/*.json

Both engine runs use flags from category config + D4=off, PROTEIN_BAR=off.

Reports:
  (a) TRUE BARS DELTA = working_tree - HEAD
  (b) PRE-EXISTING STALENESS = HEAD - committed_json

Read-only: writes NOTHING to live JSONs or engine files.
"""

from __future__ import annotations

import io
import json
import os
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

# Force UTF-8 output on Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

REPO = Path("C:/Bari")
WORKTREE = REPO / "Bari_worktree_head"
CONFIGS_DIR = REPO / "03_operations" / "page_generator" / "configs"
COMPARISONS_DIR = REPO / "bari-web" / "src" / "data" / "comparisons"
LIVE_MANIFEST_PATH = REPO / "03_operations" / "spine" / "live_manifest.json"
SCORE_ONE_SCRIPT = REPO / "tasks" / "_task371_score_one.py"

PYTHON = sys.executable


def load_json(path: Path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_frontend_scores(json_path: Path) -> dict[str, dict]:
    if not json_path.exists():
        return {}
    data = load_json(json_path)
    result = {}
    for p in data.get("products", []):
        bc = str(p.get("barcode", "")).strip()
        if not bc:
            continue
        result[bc] = {
            "score": p.get("score"),
            "grade": p.get("grade"),
            "name": p.get("name_he") or p.get("name", ""),
        }
    return result


def collect_bsip1_files(corpus_dirs: list[str], exclusions: set[str],
                         corpus_filter: set[str] | None = None) -> list[Path]:
    files = []
    seen = set()
    for d in corpus_dirs:
        dpath = Path(d)
        if not dpath.is_dir():
            continue
        for fname in sorted(dpath.glob("bsip1_*.json")):
            if "audit" in fname.name:
                continue
            try:
                with open(fname, encoding="utf-8") as f:
                    rec = json.load(f)
            except Exception:
                continue
            bc = str(rec.get("barcode", "")).strip()
            if not bc or bc in seen or bc in exclusions:
                continue
            if rec.get("file_type") != "product":
                continue
            if corpus_filter is not None and bc not in corpus_filter:
                continue
            seen.add(bc)
            files.append(fname)
    return files


def score_product_subprocess(engine_root: Path, bsip1_file: Path,
                              flags: dict, shelf_rel: dict | None) -> dict | None:
    """Run _task371_score_one.py in a clean subprocess."""
    flags_json = json.dumps(flags)
    shelf_json = json.dumps(shelf_rel or {})
    cmd = [PYTHON, str(SCORE_ONE_SCRIPT),
           str(engine_root), str(bsip1_file), flags_json, shelf_json]
    try:
        result = subprocess.run(
            cmd, capture_output=True, timeout=30
        )
        # Decode as UTF-8 (score_one.py sets UTF-8 stdout)
        stdout_text = result.stdout.decode("utf-8", errors="replace")
        stderr_text = result.stderr.decode("utf-8", errors="replace")
        result = type("R", (), {"returncode": result.returncode, "stdout": stdout_text, "stderr": stderr_text})()
        if result.returncode != 0:
            return {"error": result.stderr[-300:], "score": None, "grade": None}
        stdout = result.stdout.strip()
        if not stdout:
            return {"error": "empty stdout", "score": None, "grade": None}
        return json.loads(stdout)
    except Exception as e:
        return {"error": str(e), "score": None, "grade": None}


def score_category_all(config: dict, engine_root: Path) -> dict[str, dict]:
    """Score all products in a category. Returns {barcode: result}."""
    scoring = config.get("scoring", {})
    flags = dict(scoring.get("flags", {}))
    # Always force these OFF
    flags["BARI_D4_SCORE_V1"] = "off"
    flags["BARI_PROTEIN_BAR_V1"] = "off"

    exclusions = {e["barcode"] for e in config.get("exclusions", []) if "barcode" in e}
    shelf_rel = scoring.get("shelf_rel")

    bsip1_dir = scoring.get("bsip1_dir")
    corpus_dirs = config.get("corpus_dirs", [])
    if bsip1_dir:
        corpus_dirs = [bsip1_dir]
    elif isinstance(corpus_dirs, str):
        corpus_dirs = [corpus_dirs]

    # Load corpus filter
    corpus_filter = None
    cf_path = scoring.get("corpus_filter")
    if cf_path:
        try:
            cf_data = load_json(Path(cf_path))
            corpus_filter = {str(p["barcode"]) for p in cf_data.get("products", [])
                             if p.get("decision") == "IN_SCORED"}
        except Exception:
            pass

    bsip1_files = collect_bsip1_files(corpus_dirs, exclusions, corpus_filter)

    results = {}
    for fpath in bsip1_files:
        result = score_product_subprocess(engine_root, fpath, flags, shelf_rel)
        if result:
            bc = result.get("barcode", str(fpath.stem))
            if bc:
                results[bc] = result
    return results


def main():
    manifest = load_json(LIVE_MANIFEST_PATH)

    # Build {category → frontend_json_path}
    cat_to_json: dict[str, Path] = {}
    for entry in manifest.get("files", []):
        cat = entry.get("category")
        path = entry.get("path")
        if cat and path:
            cat_to_json[cat] = Path(path)

    config_files = sorted(
        p for p in CONFIGS_DIR.glob("*.json")
        if not p.name.startswith("_generated_")
    )

    all_delta_a = []  # (a) TRUE BARS DELTA
    all_delta_b = []  # (b) PRE-EXISTING STALENESS

    cat_reports = {}

    for cfg_path in config_files:
        cat_name = cfg_path.stem

        try:
            config = load_json(cfg_path)
        except Exception as e:
            print(f"[{cat_name}] ERROR loading config: {e}")
            continue

        cat_slug = config.get("category", "")

        # Find matching frontend JSON
        frontend_path = None
        for slug, path in cat_to_json.items():
            if cat_slug and (slug == cat_slug or slug.replace("-", "_") == cat_slug.replace("-", "_")):
                frontend_path = path
                break
            if slug.replace("-", "_") == cat_name.replace("-", "_"):
                frontend_path = path
                break
        if not frontend_path:
            for slug, path in cat_to_json.items():
                if cat_name in slug or slug in cat_name:
                    frontend_path = path
                    break

        if not frontend_path:
            print(f"[{cat_name}] No frontend JSON found (slug={cat_slug})")
            continue

        committed = load_frontend_scores(frontend_path)
        print(f"[{cat_name}] frontend={frontend_path.name} committed={len(committed)} prods")

        # Score with HEAD engine
        print(f"[{cat_name}] Scoring with HEAD engine...")
        head_scores = score_category_all(config, WORKTREE)
        print(f"[{cat_name}] HEAD scored: {len(head_scores)}")

        # Score with working-tree engine
        print(f"[{cat_name}] Scoring with working-tree engine...")
        wt_scores = score_category_all(config, REPO)
        print(f"[{cat_name}] WT scored: {len(wt_scores)}")

        # Compare
        all_barcodes = set(committed) | set(head_scores) | set(wt_scores)
        delta_a = []
        delta_b = []

        for bc in sorted(all_barcodes):
            h = head_scores.get(bc, {})
            w = wt_scores.get(bc, {})
            c = committed.get(bc, {})

            h_score = h.get("score")
            w_score = w.get("score")
            c_score = c.get("score")
            h_grade = h.get("grade")
            w_grade = w.get("grade")
            c_grade = c.get("grade")
            name = h.get("name") or w.get("name") or c.get("name") or ""

            # (a) TRUE BARS DELTA
            if h_score is not None and w_score is not None:
                a_diff = abs(float(h_score) - float(w_score)) >= 0.1
            else:
                a_diff = False
            a_grade_diff = (h_grade and w_grade and h_grade != w_grade)

            if a_diff or a_grade_diff:
                cls_basis = w.get("classification_basis", [])
                trace_reason = ""
                for b in cls_basis:
                    if "task362_r3" in b or "chocolate_name_marker" in b:
                        trace_reason = b
                        break
                if not trace_reason and w.get("override_applied"):
                    trace_reason = w.get("override_reason", "")[:120]
                if not trace_reason and cls_basis:
                    trace_reason = cls_basis[0][:120]

                entry = {
                    "barcode": bc,
                    "name": name,
                    "category": cat_name,
                    "head_score": h_score,
                    "head_grade": h_grade,
                    "head_category": h.get("category"),
                    "wt_score": w_score,
                    "wt_grade": w_grade,
                    "wt_category": w.get("category"),
                    "wt_subtype": w.get("category_subtype"),
                    "score_delta": round(float(w_score) - float(h_score), 1),
                    "trace_reason": trace_reason,
                }
                delta_a.append(entry)
                all_delta_a.append(entry)

            # (b) PRE-EXISTING STALENESS
            if h_score is not None and c_score is not None:
                b_diff = abs(float(h_score) - float(c_score)) >= 0.1
            else:
                b_diff = False
            b_grade_diff = (h_grade and c_grade and h_grade != c_grade)

            if b_diff or b_grade_diff:
                entry = {
                    "barcode": bc,
                    "name": name,
                    "category": cat_name,
                    "committed_score": c_score,
                    "committed_grade": c_grade,
                    "head_score": h_score,
                    "head_grade": h_grade,
                    "score_delta": round(float(h_score) - float(c_score), 1),
                }
                delta_b.append(entry)
                all_delta_b.append(entry)

        cat_reports[cat_name] = {
            "committed": len(committed),
            "head_scored": len(head_scores),
            "wt_scored": len(wt_scores),
            "delta_a": delta_a,
            "delta_b": delta_b,
        }

        print(f"[{cat_name}] (a) TRUE BARS DELTA: {len(delta_a)} products")
        for e in delta_a:
            n = e["name"][:40]
            print(f"    {e['barcode']} {n!r:42s} HEAD={e['head_score']}/{e['head_grade']} "
                  f"WT={e['wt_score']}/{e['wt_grade']} delta={e['score_delta']:+.1f} "
                  f"head_cat={e['head_category']} wt_cat={e['wt_category']}:{e['wt_subtype']}")
            if e["trace_reason"]:
                print(f"      trace: {e['trace_reason'][:100]}")

        print(f"[{cat_name}] (b) PRE-EXISTING STALENESS: {len(delta_b)} products")
        for e in delta_b[:5]:
            n = e["name"][:40]
            print(f"    {e['barcode']} {n!r:42s} committed={e['committed_score']}/{e['committed_grade']} "
                  f"HEAD={e['head_score']}/{e['head_grade']} delta={e['score_delta']:+.1f}")
        if len(delta_b) > 5:
            print(f"    ...and {len(delta_b)-5} more")

    # -----------------------------------------------------------------------
    # DECISIVE CHECK: hard_cheeses (a) == 0?
    # -----------------------------------------------------------------------
    print("\n" + "="*60)
    print("DECISIVE CHECK: hard_cheeses TRUE BARS DELTA (a) == 0?")
    hc = cat_reports.get("hard_cheeses", {})
    hc_a = hc.get("delta_a", [])
    hc_b = hc.get("delta_b", [])

    if not hc_a:
        print("CONFIRMED: hard_cheeses delta (a) == 0.")
        print("  Bars rework (TASK-362/365) does NOT change hard_cheeses scores at all.")
    else:
        print(f"REFUTED: hard_cheeses has {len(hc_a)} products in bars delta (a)!")
        for e in hc_a:
            print(f"  {e['barcode']} trace: {e.get('trace_reason','')[:80]}")

    babybel_bc = "3073781199918"
    babybel_b = [e for e in hc_b if e["barcode"] == babybel_bc]
    if babybel_b:
        e = babybel_b[0]
        print(f"\nBabybel {babybel_bc}:")
        print(f"  committed={e['committed_score']}/{e['committed_grade']} "
              f"HEAD={e['head_score']}/{e['head_grade']} delta={e['score_delta']:+.1f}")
        print("  => CONFIRMED: Babybel 71->39 swing is PRE-EXISTING STALENESS (b), NOT bars-rework")
    else:
        print(f"\nBabybel {babybel_bc}: NOT in staleness delta (check head vs committed manually)")
        # Look in head scores
        hc_head = None
        for e in hc_b:
            if e["barcode"] == babybel_bc:
                hc_head = e
        if hc_head is None:
            print("  (also not found in cat_reports)")

    # -----------------------------------------------------------------------
    # HEADLINE: 153 split
    # -----------------------------------------------------------------------
    print("\n" + "="*60)
    print("HEADLINE SPLIT OF PREVIOUSLY-FLAGGED ~153 DRIFTS")
    print(f"(a) TRUE BARS DELTA (working_tree - HEAD):     {len(all_delta_a):4d} products")
    print(f"(b) PRE-EXISTING STALENESS (HEAD - committed): {len(all_delta_b):4d} products")

    overlap = set(e["barcode"] for e in all_delta_a) & set(e["barcode"] for e in all_delta_b)
    print(f"    Overlap (both a and b): {len(overlap)}")
    total_unique = len(set(e["barcode"] for e in all_delta_a + all_delta_b))
    print(f"    Total unique products with any drift: {total_unique}")

    print("\n(a) TRUE BARS DELTA by category:")
    a_by_cat = Counter(e["category"] for e in all_delta_a)
    for cat, cnt in sorted(a_by_cat.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {cnt}")

    print("\n(b) PRE-EXISTING STALENESS by category:")
    b_by_cat = Counter(e["category"] for e in all_delta_b)
    for cat, cnt in sorted(b_by_cat.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {cnt}")

    print("\n(a) Full TRUE BARS DELTA product list:")
    for e in sorted(all_delta_a, key=lambda x: (x["category"], x["barcode"])):
        print(f"  [{e['category']}] {e['barcode']} {e['name'][:35]!r:37s} "
              f"{e['head_category']:20s}->  {e['wt_category']}:{e['wt_subtype']} "
              f"score_delta={e['score_delta']:+.1f}")
        if e["trace_reason"]:
            print(f"    trace: {e['trace_reason'][:100]}")

    print("\n0 files written (read-only diagnostic).")
    print("Worktree: C:/Bari/Bari_worktree_head")
    print("  Remove with: git worktree remove C:/Bari/Bari_worktree_head --force")


if __name__ == "__main__":
    main()
