"""
rescore_cookies_task393.py — TASK-393 Stage 1: Cookies-coffee freshness re-score
=================================================================================
Re-scores all 119 displayed products against the CURRENT engine with CURRENT
production default flags. Matches each product from the live frontend JSON to its
BSIP1 source, re-scores, and compares grades/scores against the live baseline.

CRITICAL: env flags set BEFORE any engine import (juices contamination bug pattern).

Production flag state replicated (from cookies_coffee.json + batch runner):
  BARI_RECAL_P0                  = off
  BARI_GRAD_SODIUM_V1            = off
  BARI_SODIUM_SHELF_RELATIVE_V1  = off
  BARI_DAIRY_PROTEIN_REWEIGHT_V1 = off
  BARI_REDLABEL_V1               = off
  BARI_SODIUM_CEREAL             = off
  BARI_TASK144_FIXES             = off
  BARI_FAT_TECH_V1               = on   (engine default ON since 2026-06-15)
  BARI_D4_SCORE_V1               = off  (engine default; NOT in config → OFF)
  BARI_HC_DAIRY_SATFAT_V1        = off  (engine default; dairy-only flag)
  BARI_SHELF_RELATIVE_V1         = off
  BARI_RECAL_P0_YOGURT_TRIM      = off

Outputs:
  run_cookies_task393_fresh/
    products/bsip2_trace_<barcode>.json  — per-product fresh trace
    verification_table.csv               — barcode,score,grade,binding_cap,... (stable artifact)
    grade_mover_table.json               — grade movers with per-product driver
    score_drift_table.json               — score-only drifts
    cross_category_scan.json             — foreign cap token scan result
    run_record.json                      — run metadata + distribution

Does NOT touch frontend JSON.
"""
import os, sys

# === CRITICAL: Set all flags BEFORE any engine import ===
os.environ["BARI_RECAL_P0"]                 = "off"
os.environ["BARI_GRAD_SODIUM_V1"]           = "off"
os.environ["BARI_SODIUM_SHELF_RELATIVE_V1"] = "off"
os.environ["BARI_DAIRY_PROTEIN_REWEIGHT_V1"]= "off"
os.environ["BARI_REDLABEL_V1"]              = "off"
os.environ["BARI_SODIUM_CEREAL"]            = "off"
os.environ["BARI_TASK144_FIXES"]            = "off"
os.environ["BARI_FAT_TECH_V1"]              = "on"   # engine default ON; explicit for reproducibility
os.environ["BARI_D4_SCORE_V1"]              = "off"  # NOT in config; engine default OFF
os.environ["BARI_HC_DAIRY_SATFAT_V1"]       = "off"  # dairy-only; ensure off for cookies
os.environ["BARI_SHELF_RELATIVE_V1"]        = "off"
os.environ["BARI_RECAL_P0_YOGURT_TRIM"]     = "off"
os.environ["BARI_GLASSBOX_W2"]              = "off"
os.environ["BARI_GLASSBOX_D5D6"]            = "off"
os.environ["BARI_GLASSBOX_W15"]             = "off"

import json, pathlib, logging, datetime, hashlib, csv
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

_SRC = pathlib.Path(__file__).parent
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from signal_extractor import extract_signals
from router_v2 import classify_category
from nova_proxy import infer_nova
from evaluation_scope import assign_evaluation_scope
from score_engine import score_product
from trace_writer import assemble_trace, write_trace
from structural_classifier import classify_structural_class
from constants import score_to_grade

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

ROOT = pathlib.Path(r"C:\Bari")

# ---- Paths ----
FRONTEND_JSON = ROOT / "bari-web" / "src" / "data" / "comparisons" / "cookies_coffee_frontend_v2.json"
CORPUS_DIRS = [
    ROOT / "03_operations" / "bsip1" / "run_cookies_001" / "output",
    ROOT / "03_operations" / "bsip1" / "run_cakes_001"   / "output",
]
RUN_OUT = ROOT / "02_products" / "cookies_coffee" / "bsip2_outputs" / "run_cookies_task393_fresh"
RUN_ID  = "run_cookies_task393_fresh"

# Exclusions from config (all barcodes that should be excluded)
EXCLUDED_BARCODES = {
    "7290013453631",  # discard_wrong_ingredients
    "7290017962108",  # discard_wrong_scrape
    "7290119040513",  # t1_removed_misclassified_cake
    "7290119040568",  # t1_removed_misclassified_cake
    "7290119040612",  # t1_removed_misclassified_cake
    "7290119040667",  # t1_removed_misclassified_cake
}

GRADE_SCALE = [("S", 90), ("A", 80), ("B", 65), ("C", 50), ("D", 35), ("E", 0)]

def score_to_grade_local(score):
    if score is None:
        return None
    for grade, floor in GRADE_SCALE:
        if score >= floor:
            return grade
    return "E"

# Foreign-category cap tokens: tokens that should NOT appear in cookies category traces
FOREIGN_CAP_TOKENS = [
    "granola", "cereal", "magnesium", "cheese", "dairy", "brined",
    "SODIUM_CEREAL", "HC_DAIRY", "dairy_protein", "hard_cheese",
    "yogurt", "milk", "BARI_DAIRY", "BARI_RECAL",
    "snack_bar_granola",  # routing leak
]

def sha256_file(path):
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()

def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def stdev(scores):
    if not scores: return 0.0
    n = len(scores)
    mean = sum(scores) / n
    return (sum((x - mean)**2 for x in scores) / n) ** 0.5

def extract_driver(trace: dict) -> str:
    """Extract primary scoring driver from trace (cap token + top penalties)."""
    parts = []
    bc = trace.get("binding_cap")
    if bc:
        parts.append(f"binding_cap={bc}")
    caps = trace.get("caps_applied") or []
    for c in caps[:2]:
        rule = c.get("rule") or c.get("cap")
        if rule:
            parts.append(f"cap:{rule}")
    pens = trace.get("penalties_applied") or []
    for p in pens[:2]:
        amt = p.get("amount")
        rule = p.get("rule") or p.get("name")
        if rule:
            parts.append(f"pen-{amt}:{rule}")
    # Check D4 (will be 0/None since D4 off, but include for completeness)
    d4_pen = trace.get("d4_score_penalty")
    if d4_pen:
        parts.append(f"D4_pen={d4_pen}")
    ctx = trace.get("context_flag")
    if ctx:
        parts.append(f"ctx={ctx}")
    return " | ".join(parts) if parts else "(no driver)"

def scan_foreign_tokens(trace: dict, barcode: str) -> list:
    """Scan trace JSON for foreign-category cap tokens in scoring-relevant fields."""
    found = []
    category   = str(trace.get("category") or "")
    caps_str   = json.dumps(trace.get("caps_applied") or [], ensure_ascii=False)
    pens_str   = json.dumps(trace.get("penalties_applied") or [], ensure_ascii=False)
    notes_str  = json.dumps(trace.get("dimension_notes") or {}, ensure_ascii=False)
    # binding_cap may be an int (score value) or a string label; str-cast for safety
    binding_cap_str = str(trace.get("binding_cap") or "")

    scoring_ctx = caps_str + " " + pens_str + " " + notes_str + " " + binding_cap_str

    for token in FOREIGN_CAP_TOKENS:
        if token in scoring_ctx:
            found.append({"token": token, "context": "scoring_fields (caps/pens/notes/binding_cap)"})
        # Check router category for known foreign routes
        if token in ("snack_bar_granola", "dairy_protein") and category == token:
            found.append({"token": token, "context": f"router_category={category}"})
    return found

def main():
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
    log.info("=== TASK-393 Stage 1: Cookies-coffee freshness re-score (%s) ===", RUN_ID)
    log.info("Flags: FAT_TECH=on | D4_SCORE=off | all others off")

    # ---- Load live frontend JSON to get the 119 displayed barcodes ----
    frontend = json.loads(FRONTEND_JSON.read_text(encoding="utf-8"))
    live_products = frontend.get("products") or []
    log.info("Live frontend: %d products", len(live_products))

    # Build baseline lookup: barcode -> {score, grade, name}
    baseline = {}
    for p in live_products:
        bc = str(p.get("barcode") or "")
        baseline[bc] = {
            "score": p.get("score"),
            "grade": p.get("grade"),
            "name":  p.get("name") or p.get("nameHe") or "",
        }
    log.info("Baseline barcodes: %d", len(baseline))

    # ---- Build BSIP1 corpus lookup: barcode -> bsip1 record (first-listed wins) ----
    corpus_lookup = {}
    for cdir in CORPUS_DIRS:
        if not cdir.exists():
            log.warning("Corpus dir missing: %s", cdir)
            continue
        for fp in sorted(cdir.glob("bsip1_*.json")):
            try:
                doc = json.loads(fp.read_text(encoding="utf-8"))
                bc = str(doc.get("barcode") or "")
                if bc and bc not in corpus_lookup:
                    corpus_lookup[bc] = doc
            except Exception as e:
                log.error("Corpus load error %s: %s", fp.name, e)
    log.info("BSIP1 corpus loaded: %d unique barcodes", len(corpus_lookup))

    # ---- Setup output dir ----
    (RUN_OUT / "products").mkdir(parents=True, exist_ok=True)
    log.info("Output dir: %s", RUN_OUT)

    # ---- Re-score each displayed product ----
    results = []
    no_corpus_match = []
    score_errors = []
    foreign_hits = []

    for bc, base in sorted(baseline.items()):
        if bc in EXCLUDED_BARCODES:
            log.info("EXCLUDED: %s", bc)
            continue

        bsip1_doc = corpus_lookup.get(bc)
        if not bsip1_doc:
            log.warning("NO BSIP1 MATCH: %s (%s) — applying missing-data discard rule", bc, base["name"])
            no_corpus_match.append({"barcode": bc, "name": base["name"], "action": "discarded_no_corpus"})
            continue

        try:
            signals     = extract_signals(bsip1_doc)
            cat_result  = classify_category(bsip1_doc)
            l3          = signals["L3_inferred_classifications"]
            nova_result = infer_nova(bsip1_doc, l3)
            eval_result = assign_evaluation_scope(bsip1_doc, cat_result["category"])
            score_result= score_product(bsip1_doc, signals, cat_result, nova_result, eval_result)
            trace       = assemble_trace(bsip1_doc, signals, cat_result, nova_result, eval_result, score_result)
            trace["structural_class"] = classify_structural_class(trace)

            new_score = trace.get("final_score_estimate")
            new_grade = score_to_grade_local(new_score)

            # Write fresh trace
            trace_path = RUN_OUT / "products" / f"bsip2_trace_{bc}.json"
            trace_path.write_text(json.dumps(trace, ensure_ascii=False, indent=2), encoding="utf-8")

            # Scan for foreign-category tokens
            foreign = scan_foreign_tokens(trace, bc)
            if foreign:
                foreign_hits.append({"barcode": bc, "name": base["name"], "hits": foreign})
                log.warning("FOREIGN TOKEN: %s — %s", bc, foreign)

            old_score = base["score"]
            old_grade = base["grade"]

            result = {
                "barcode": bc,
                "name": base["name"],
                "old_score": old_score,
                "old_grade": old_grade,
                "new_score": new_score,
                "new_grade": new_grade,
                "score_delta": round(new_score - old_score, 1) if (new_score is not None and old_score is not None) else None,
                "grade_changed": (old_grade != new_grade),
                "driver": extract_driver(trace),
                "category": trace.get("category"),
                "binding_cap": trace.get("binding_cap"),
                "nova": trace.get("nova_proxy"),
                "context_flag": trace.get("context_flag"),
                "d4_score_penalty": trace.get("d4_score_penalty", 0),
            }
            results.append(result)

            log.info("  %s  %s->%s  %s->%s  delta=%s",
                     bc[:20], old_grade, new_grade, old_score, new_score, result["score_delta"])

        except Exception as e:
            log.error("SCORE ERROR %s (%s): %s", bc, base["name"], e)
            import traceback; traceback.print_exc()
            score_errors.append({"barcode": bc, "name": base["name"], "error": str(e)})

    # ---- Derive distribution from trace files (trace-derived per return contract) ----
    log.info("Reading back traces from disk for verified distribution...")
    verified_scores = []
    verified_grades = []
    trace_barcodes_on_disk = set()
    for trace_fp in sorted((RUN_OUT / "products").glob("bsip2_trace_*.json")):
        try:
            t = json.loads(trace_fp.read_text(encoding="utf-8"))
            s = t.get("final_score_estimate")
            g = score_to_grade_local(s)
            if s is not None:
                verified_scores.append(s)
                verified_grades.append(g)
            bc_from_file = trace_fp.stem.replace("bsip2_trace_", "")
            trace_barcodes_on_disk.add(bc_from_file)
        except Exception as e:
            log.error("Re-read error %s: %s", trace_fp.name, e)
    log.info("Traces on disk: %d | Scores: %d", len(trace_barcodes_on_disk), len(verified_scores))

    grade_dist = Counter(verified_grades)
    score_min  = min(verified_scores) if verified_scores else None
    score_max  = max(verified_scores) if verified_scores else None
    score_stdev = round(stdev(verified_scores), 2) if verified_scores else None
    n = len(verified_scores)
    ss = sorted(verified_scores)
    score_median = ss[n//2] if (n % 2) else ((ss[n//2 - 1] + ss[n//2]) / 2) if n else None
    most_common  = Counter(verified_scores).most_common(1)[0] if verified_scores else (None, 0)
    histogram = {}
    for s in verified_scores:
        band = f"{int(s//10)*10}-{int(s//10)*10+9}"
        histogram[band] = histogram.get(band, 0) + 1

    # ---- Grade mover table ----
    grade_movers = [r for r in results if r["grade_changed"]]
    score_only_drifts = [r for r in results if not r["grade_changed"] and r["score_delta"] is not None and abs(r["score_delta"]) > 0]

    mover_table_path = RUN_OUT / "grade_mover_table.json"
    mover_table_path.write_text(json.dumps(grade_movers, ensure_ascii=False, indent=2), encoding="utf-8")

    drift_table_path = RUN_OUT / "score_drift_table.json"
    drift_table_path.write_text(json.dumps({
        "count": len(score_only_drifts),
        "drifts": sorted(score_only_drifts, key=lambda x: abs(x["score_delta"] or 0), reverse=True)
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    # ---- Cross-category isolation scan ----
    cross_cat_path = RUN_OUT / "cross_category_scan.json"
    cross_cat_path.write_text(json.dumps({
        "total_products_scanned": len(results),
        "foreign_hits": len(foreign_hits),
        "pass": len(foreign_hits) == 0,
        "hits": foreign_hits,
        "tokens_checked": FOREIGN_CAP_TOKENS,
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    # ---- Verification table (stable CSV per return contract §7) ----
    verify_path = RUN_OUT / "verification_table.csv"
    with verify_path.open("w", encoding="utf-8", newline="") as vf:
        writer = csv.writer(vf)
        writer.writerow(["barcode", "name", "old_score", "old_grade", "new_score", "new_grade",
                         "score_delta", "grade_changed", "binding_cap", "nova", "context_flag",
                         "category", "d4_score_penalty", "driver"])
        for r in sorted(results, key=lambda x: x["barcode"]):
            writer.writerow([
                r["barcode"], r["name"], r["old_score"], r["old_grade"],
                r["new_score"], r["new_grade"], r["score_delta"], r["grade_changed"],
                r["binding_cap"], r["nova"], r["context_flag"], r["category"],
                r.get("d4_score_penalty", 0), r["driver"],
            ])

    # ---- Run record ----
    engine_sha = sha256_file(_SRC / "score_engine.py")
    signal_sha = sha256_file(_SRC / "signal_extractor.py")
    eval_sha   = sha256_file(_SRC / "evaluation_scope.py")

    run_record = {
        "run_id": RUN_ID,
        "task": "TASK-393",
        "category": "cookies_coffee",
        "generated": ts,
        "flag_state_replicated": {
            "BARI_RECAL_P0":                  "off",
            "BARI_GRAD_SODIUM_V1":            "off",
            "BARI_SODIUM_SHELF_RELATIVE_V1":  "off",
            "BARI_DAIRY_PROTEIN_REWEIGHT_V1": "off",
            "BARI_REDLABEL_V1":               "off",
            "BARI_SODIUM_CEREAL":             "off",
            "BARI_TASK144_FIXES":             "off",
            "BARI_FAT_TECH_V1":               "on",   # engine default ON
            "BARI_D4_SCORE_V1":               "off",  # NOT in config; engine default OFF
            "BARI_HC_DAIRY_SATFAT_V1":        "off",
            "BARI_SHELF_RELATIVE_V1":         "off",
        },
        "flag_state_rationale": (
            "BARI_FAT_TECH_V1=on is the engine default since 2026-06-15; "
            "original batch_run_cookies_005.py did not set it explicitly, "
            "so it inherited the engine default. "
            "BARI_D4_SCORE_V1=off: not present in cookies_coffee.json config; "
            "engine default is off. D4 was shadow-tested in affected_set_spine.json "
            "but NOT activated for production cookies scoring."
        ),
        "baseline": {
            "run_id": "run_cookies_005+run_cakes_001_cookies",
            "grade_distribution": {"C": 10, "D": 24, "E": 85},
            "product_count": 119,
        },
        "fresh_run": {
            "products_in_baseline": len(baseline),
            "products_excluded": len(EXCLUDED_BARCODES),
            "no_corpus_match": len(no_corpus_match),
            "score_errors": len(score_errors),
            "rescored": len(results),
            "grade_distribution": dict(sorted(grade_dist.items())),
            "score_stats": {
                "min": score_min, "max": score_max, "median": score_median,
                "stdev": score_stdev, "n": n,
                "most_common_score": most_common[0],
                "most_common_count": most_common[1],
                "histogram": dict(sorted(histogram.items())),
            },
        },
        "grade_movers": {
            "count": len(grade_movers),
            "movers": grade_movers,
        },
        "score_only_drifts": {
            "count": len(score_only_drifts),
            "nonzero_drift_count": len([d for d in score_only_drifts if d["score_delta"] != 0]),
        },
        "cross_category_isolation": {
            "pass": len(foreign_hits) == 0,
            "foreign_hits": len(foreign_hits),
        },
        "no_corpus_match": no_corpus_match,
        "score_errors": score_errors,
        "engine_sha256": engine_sha,
        "signal_extractor_sha256": signal_sha,
        "evaluation_scope_sha256": eval_sha,
        "off_used": False,
        "artifacts": {
            "verification_table": str(verify_path),
            "grade_mover_table": str(mover_table_path),
            "score_drift_table": str(drift_table_path),
            "cross_category_scan": str(cross_cat_path),
        },
    }

    rr_path = RUN_OUT / "run_record.json"
    rr_path.write_text(json.dumps(run_record, ensure_ascii=False, indent=2), encoding="utf-8")

    # ---- Print summary ----
    print("\n" + "=" * 72)
    print(f"TASK-393 STAGE 1: COOKIES-COFFEE FRESHNESS RE-SCORE — {RUN_ID}")
    print("=" * 72)
    print(f"Baseline: C10/D24/E85 (119 products, run_cookies_005+run_cakes_001_cookies)")
    print(f"Rescored: {len(results)} products | Errors: {len(score_errors)} | No-corpus: {len(no_corpus_match)}")
    print(f"Flag state: FAT_TECH=on | D4_SCORE=off | all others off")
    print(f"\nNEW GRADE DISTRIBUTION (trace-derived from {len(trace_barcodes_on_disk)} traces on disk):")
    for g in ["S", "A", "B", "C", "D", "E"]:
        count = grade_dist.get(g, 0)
        print(f"  {g}: {count}")
    print(f"\nSCORE STATS:")
    print(f"  Min={score_min} Max={score_max} Median={score_median} StDev={score_stdev} N={n}")
    print(f"  Most common: {most_common[0]} ({most_common[1]} products)")
    print(f"  Histogram: {dict(sorted(histogram.items()))}")
    print(f"\nGRADE MOVERS: {len(grade_movers)}")
    for m in sorted(grade_movers, key=lambda x: x["barcode"]):
        print(f"  {m['barcode'][:20]}  {m['old_grade']}->{m['new_grade']}  {m['old_score']}->{m['new_score']}  driver: {m['driver'][:60]}")
    print(f"\nSCORE-ONLY DRIFTS (no grade change): {len(score_only_drifts)}")
    if score_only_drifts:
        deltas = [abs(d["score_delta"]) for d in score_only_drifts if d["score_delta"] is not None]
        if deltas:
            print(f"  Delta range: {min(deltas):.1f} – {max(deltas):.1f} pts")
            print(f"  Largest drifts:")
            for d in sorted(score_only_drifts, key=lambda x: abs(x["score_delta"] or 0), reverse=True)[:5]:
                print(f"    {d['barcode'][:20]} {d['old_grade']}  {d['old_score']}->{d['new_score']} (delta={d['score_delta']})")
    print(f"\nCROSS-CATEGORY ISOLATION: {'PASS' if len(foreign_hits)==0 else 'FAIL — ' + str(len(foreign_hits)) + ' hits'}")
    if foreign_hits:
        for h in foreign_hits:
            print(f"  FOREIGN: {h['barcode']} — {h['hits']}")
    print(f"\nARTIFACTS:")
    print(f"  Run dir:            {RUN_OUT}")
    print(f"  Run record:         {rr_path}")
    print(f"  Verification table: {verify_path}")
    print(f"  Grade mover table:  {mover_table_path}")
    print(f"  Score drift table:  {drift_table_path}")
    print(f"  Cross-cat scan:     {cross_cat_path}")
    print(f"  Traces:             {RUN_OUT}/products/ ({len(trace_barcodes_on_disk)} files)")
    print("=" * 72)

    return run_record


if __name__ == "__main__":
    main()
