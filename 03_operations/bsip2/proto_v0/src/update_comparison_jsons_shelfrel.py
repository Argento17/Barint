"""
TASK-278 go-live: update live comparison JSONs with new SR+fat-tech scores.

Reads new traces from run_*_shelfrel_001 directories.
For each product in the comparison JSON (matched by barcode), updates:
  - score (final_score_estimate)
  - grade (grade_estimate)
Leaves all copy fields (insightLine, rowVerdict, etc.) INTACT.

OFF ban: zero. No data sourcing here — score update only.
"""
import json, pathlib, sys, logging
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

ROOT = pathlib.Path(r"C:\Bari")
COMP_DIR = ROOT / "bari-web" / "src" / "data" / "comparisons"

# Map: comparison JSON filename → new trace dir
CATEGORY_MAP = {
    "cereals_frontend_v2.json": ROOT / "02_products" / "breakfast_cereals" / "bsip2_outputs" / "run_cereals_shelfrel_001" / "products",
    "hard_cheeses_frontend_v2.json": ROOT / "02_products" / "hard_cheeses" / "bsip2_outputs" / "run_hard_cheeses_002_shelfrel" / "products",
    "juices_frontend_v3.json": ROOT / "02_products" / "juices" / "bsip2_outputs" / "run_juices_shelfrel_001" / "products",
    "salty_snacks_frontend_v4.json": ROOT / "02_products" / "salty_snacks" / "bsip2_outputs" / "run_salty_snacks_shelfrel_001" / "products",
    "hummus_frontend_v5.json": ROOT / "02_products" / "hummus" / "intelligence_bsip2" / "run_hummus_shelfrel_001" / "products",
    "cakes_hard_cookies_frontend_v1.json": ROOT / "02_products" / "cakes_hard_cookies" / "bsip2_outputs" / "run_cakes_shelfrel_001" / "products",
}


def load_traces(trace_dir):
    """Build barcode → {score, grade} map from trace directory."""
    scores = {}
    if not trace_dir.exists():
        log.warning("Trace dir not found: %s", trace_dir)
        return scores
    for p in trace_dir.glob("*.json"):
        try:
            tr = json.loads(p.read_text(encoding="utf-8"))
        except Exception as e:
            log.error("Failed to read trace %s: %s", p, e)
            continue
        bc = str(tr.get("barcode", ""))
        s = tr.get("final_score_estimate")
        g = tr.get("grade_estimate")
        if bc and s is not None and g:
            scores[bc] = {"score": round(s, 1), "grade": g}
    return scores


def load_traces_nested(trace_dir):
    """Build barcode → {score, grade} map from nested trace directories (bsip1_BC/bsip2_trace.json)."""
    scores = {}
    if not trace_dir.exists():
        log.warning("Trace dir not found: %s", trace_dir)
        return scores
    for prod_dir in trace_dir.iterdir():
        if not prod_dir.is_dir():
            continue
        trace_path = prod_dir / "bsip2_trace.json"
        if not trace_path.exists():
            # Try direct json
            trace_path = prod_dir / f"{prod_dir.name}.json"
        if not trace_path.exists():
            continue
        try:
            tr = json.loads(trace_path.read_text(encoding="utf-8"))
        except Exception:
            continue
        bc = str(tr.get("barcode", ""))
        s = tr.get("final_score_estimate")
        g = tr.get("grade_estimate")
        if bc and s is not None and g:
            scores[bc] = {"score": round(s, 1), "grade": g}
    return scores


def update_comparison_json(json_filename, trace_dir):
    """Update a single comparison JSON with new scores. Returns change count."""
    json_path = COMP_DIR / json_filename
    if not json_path.exists():
        log.error("Comparison JSON not found: %s", json_path)
        return 0

    # Load traces — try flat then nested
    traces = load_traces(trace_dir)
    if not traces:
        traces = load_traces_nested(trace_dir)

    if not traces:
        log.error("No traces found in %s", trace_dir)
        return 0

    log.info("%s: loaded %d new traces", json_filename, len(traces))

    data = json.loads(json_path.read_text(encoding="utf-8"))
    products = data.get("products", data.get("items", []))
    if not products and isinstance(data, list):
        products = data

    changed = 0
    not_found = []
    for prod in products:
        bc = str(prod.get("barcode", ""))
        if not bc:
            continue
        if bc in traces:
            old_score = prod.get("score")
            old_grade = prod.get("grade")
            prod["score"] = traces[bc]["score"]
            prod["grade"] = traces[bc]["grade"]
            if old_score != traces[bc]["score"] or old_grade != traces[bc]["grade"]:
                changed += 1
                log.info("  bc=%s: %s/%s → %s/%s", bc,
                          old_score, old_grade, traces[bc]["score"], traces[bc]["grade"])
        else:
            not_found.append(bc)

    if not_found:
        log.warning("%s: %d products not found in traces: %s...",
                     json_filename, len(not_found), not_found[:3])

    # Write back
    json_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info("%s: %d score changes written", json_filename, changed)
    return changed


def main():
    total_changes = 0
    for json_filename, trace_dir in CATEGORY_MAP.items():
        log.info("=" * 50)
        log.info("Updating: %s", json_filename)
        n = update_comparison_json(json_filename, trace_dir)
        total_changes += n

    print(f"\nTotal score updates across all comparison JSONs: {total_changes}")
    print("Done. Copy fields untouched. Run 'npx tsc --noEmit' to verify TypeScript.")


if __name__ == "__main__":
    main()
