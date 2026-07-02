"""
rescore_cookies_task393_final.py — TASK-393/394 Stage 3: Final production re-score
===================================================================================
Clean re-score of all 119 cookies_coffee displayed products with:
  - BARI_R3_BISCUIT_NARROW_V1 = on  (production-default ON as of TASK-394 owner sign-off)
  - BARI_FAT_TECH_V1           = on  (engine default)
  - all others = off

This is the bake run that produces the authoritative traces to be written into
cookies_coffee_frontend_v2.json (scores + grades + categories).

CRITICAL: env flags set BEFORE any engine import (juices contamination bug pattern).

Expected result (pre-verified by task394 measurement):
  Grade distribution: C10 / D26 / E83
  Key products:
    313184          → biscuit / 35.3 / D  (co-signed E→D biscuit-path correction)
    7290018893845   → biscuit / 36.4 / D  (co-signed E→D biscuit-path correction)
    2986065         → biscuit / 35.8 / D  (R3-narrowed: flavor-descriptor biscuit, stays D)
    7290017894317   → biscuit / 36.1 / D  (R3-narrowed: flavor-descriptor biscuit, stays D)
"""
import os, sys

# === CRITICAL: Set ALL flags BEFORE any engine import ===
os.environ["BARI_R3_BISCUIT_NARROW_V1"]      = "on"   # TASK-394: production default activated
os.environ["BARI_RECAL_P0"]                  = "off"
os.environ["BARI_GRAD_SODIUM_V1"]            = "off"
os.environ["BARI_SODIUM_SHELF_RELATIVE_V1"]  = "off"
os.environ["BARI_DAIRY_PROTEIN_REWEIGHT_V1"] = "off"
os.environ["BARI_REDLABEL_V1"]               = "off"
os.environ["BARI_SODIUM_CEREAL"]             = "off"
os.environ["BARI_TASK144_FIXES"]             = "off"
os.environ["BARI_FAT_TECH_V1"]               = "on"   # engine default ON; explicit for reproducibility
os.environ["BARI_D4_SCORE_V1"]               = "off"  # NOT in config; engine default OFF
os.environ["BARI_HC_DAIRY_SATFAT_V1"]        = "off"  # dairy-only; ensure off for cookies
os.environ["BARI_SHELF_RELATIVE_V1"]         = "off"
os.environ["BARI_RECAL_P0_YOGURT_TRIM"]      = "off"
os.environ["BARI_GLASSBOX_W2"]               = "off"
os.environ["BARI_GLASSBOX_D5D6"]             = "off"
os.environ["BARI_GLASSBOX_W15"]              = "off"

import json, pathlib, logging, datetime, hashlib, csv
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

_SRC = pathlib.Path(__file__).parent
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from signal_extractor import extract_signals
from router_v2 import classify_category, BARI_R3_BISCUIT_NARROW_V1
from nova_proxy import infer_nova
from evaluation_scope import assign_evaluation_scope
from score_engine import score_product
from trace_writer import assemble_trace, write_trace
from structural_classifier import classify_structural_class
from constants import score_to_grade

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

ROOT = pathlib.Path(r"C:\Bari")

# Verify flag is live
assert BARI_R3_BISCUIT_NARROW_V1 is True, (
    "FATAL: BARI_R3_BISCUIT_NARROW_V1 is False at import — env-before-import discipline violated. "
    "Env var must be set before importing router_v2."
)
log.info("BARI_R3_BISCUIT_NARROW_V1 confirmed ON at import time")

# ---- Paths ----
FRONTEND_JSON = ROOT / "bari-web" / "src" / "data" / "comparisons" / "cookies_coffee_frontend_v2.json"
CORPUS_DIRS = [
    ROOT / "03_operations" / "bsip1" / "run_cookies_001" / "output",
    ROOT / "03_operations" / "bsip1" / "run_cakes_001"   / "output",
]
RUN_OUT = ROOT / "02_products" / "cookies_coffee" / "bsip2_outputs" / "run_cookies_task393_final"
RUN_ID  = "run_cookies_task393_final"

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
    binding_cap_str = str(trace.get("binding_cap") or "")

    scoring_ctx = caps_str + " " + pens_str + " " + notes_str + " " + binding_cap_str

    for token in FOREIGN_CAP_TOKENS:
        if token in scoring_ctx:
            found.append({"token": token, "context": "scoring_fields (caps/pens/notes/binding_cap)"})
        if token in ("snack_bar_granola", "dairy_protein") and category == token:
            found.append({"token": token, "context": f"router_category={category}"})
    return found

def main():
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
    log.info("=== TASK-393/394 Final: Cookies-coffee production re-score (%s) ===", RUN_ID)
    log.info("Flags: R3_BISCUIT_NARROW=on | FAT_TECH=on | D4_SCORE=off | all others off")

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
    # Track for PENDING_COPY marking
    GRADE_CHANGED_BARCODES: set = set()

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
            grade_changed = (old_grade != new_grade)
            if grade_changed:
                GRADE_CHANGED_BARCODES.add(bc)

            result = {
                "barcode": bc,
                "name": base["name"],
                "old_score": old_score,
                "old_grade": old_grade,
                "new_score": new_score,
                "new_grade": new_grade,
                "score_delta": round(new_score - old_score, 1) if (new_score is not None and old_score is not None) else None,
                "grade_changed": grade_changed,
                "driver": extract_driver(trace),
                "category": trace.get("category"),
                "binding_cap": trace.get("binding_cap"),
                "nova": trace.get("nova_proxy"),
                "context_flag": trace.get("context_flag"),
                "d4_score_penalty": trace.get("d4_score_penalty", 0),
            }
            results.append(result)

            log.info("  %s  %s->%s  %s->%s  delta=%s  cat=%s",
                     bc[:20], old_grade, new_grade, old_score, new_score, result["score_delta"],
                     trace.get("category"))

        except Exception as e:
            log.error("SCORE ERROR %s (%s): %s", bc, base["name"], e)
            import traceback; traceback.print_exc()
            score_errors.append({"barcode": bc, "name": base["name"], "error": str(e)})

    # ---- HARD STOP: any score errors = halt ----
    if score_errors:
        log.error("HALT: %d score errors — do NOT bake frontend JSON", len(score_errors))
        for e in score_errors:
            log.error("  ERROR: %s — %s", e["barcode"], e["error"])
        sys.exit(1)

    # ---- Derive distribution from trace files (trace-derived per return contract) ----
    log.info("Reading back traces from disk for verified distribution...")
    verified_scores = []
    verified_grades = []
    trace_barcodes_on_disk = set()
    trace_score_map = {}   # barcode -> new_score (for frontend bake)
    trace_grade_map = {}   # barcode -> new_grade
    trace_cat_map   = {}   # barcode -> category
    trace_full_map  = {}   # barcode -> full trace
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
            trace_score_map[bc_from_file] = s
            trace_grade_map[bc_from_file] = g
            trace_cat_map[bc_from_file]   = t.get("category")
            trace_full_map[bc_from_file]  = t
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

    # ---- ASSERT: expected distribution ----
    assert grade_dist.get("C", 0) == 10, f"ASSERT FAIL: expected C=10, got {grade_dist.get('C', 0)}"
    assert grade_dist.get("D", 0) == 26, f"ASSERT FAIL: expected D=26, got {grade_dist.get('D', 0)}"
    assert grade_dist.get("E", 0) == 83, f"ASSERT FAIL: expected E=83, got {grade_dist.get('E', 0)}"
    log.info("ASSERT PASS: C10/D26/E83 verified from traces")

    # ---- ASSERT: 4 key products ----
    KEY_PRODUCTS = {
        "313184":         {"cat": "biscuit", "grade": "D", "score": 35.3},
        "7290018893845":  {"cat": "biscuit", "grade": "D", "score": 36.4},
        "2986065":        {"cat": "biscuit", "grade": "D", "score": 35.8},
        "7290017894317":  {"cat": "biscuit", "grade": "D", "score": 36.1},
    }
    for bc, expected in KEY_PRODUCTS.items():
        actual_score = trace_score_map.get(bc)
        actual_grade = trace_grade_map.get(bc)
        actual_cat   = trace_cat_map.get(bc)
        assert actual_grade == expected["grade"], (
            f"ASSERT FAIL: {bc} expected grade {expected['grade']} got {actual_grade}"
        )
        assert actual_cat == expected["cat"], (
            f"ASSERT FAIL: {bc} expected cat {expected['cat']} got {actual_cat}"
        )
        # Score may be slightly different from measurement run if engine state differs; tolerance 1.0
        assert actual_score is not None and abs(actual_score - expected["score"]) <= 1.0, (
            f"ASSERT FAIL: {bc} expected score ~{expected['score']} got {actual_score}"
        )
        log.info("KEY ASSERT PASS: %s → cat=%s score=%s grade=%s", bc, actual_cat, actual_score, actual_grade)

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

    # ---- Verification table (stable CSV per return contract) ----
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

    # ---- Score==trace check ----
    score_trace_mismatch = []
    for r in results:
        bc = r["barcode"]
        front_score_new = r["new_score"]
        trace_score_new = trace_score_map.get(bc)
        if front_score_new != trace_score_new:
            score_trace_mismatch.append({
                "barcode": bc, "result_score": front_score_new, "trace_score": trace_score_new
            })
    if score_trace_mismatch:
        log.error("SCORE!=TRACE MISMATCHES: %d", len(score_trace_mismatch))
        for m in score_trace_mismatch:
            log.error("  %s: result=%s trace=%s", m["barcode"], m["result_score"], m["trace_score"])
    else:
        log.info("SCORE==TRACE: PASS (0 mismatches across %d products)", len(results))

    # ---- Run record ----
    engine_sha = sha256_file(_SRC / "score_engine.py")
    signal_sha = sha256_file(_SRC / "signal_extractor.py")
    eval_sha   = sha256_file(_SRC / "evaluation_scope.py")
    router_sha = sha256_file(_SRC / "router_v2.py")

    run_record = {
        "run_id": RUN_ID,
        "task": "TASK-393 Stage 2.5 + TASK-394",
        "category": "cookies_coffee",
        "generated": ts,
        "flag_state": {
            "BARI_R3_BISCUIT_NARROW_V1":       "on",   # TASK-394: production-default activated
            "BARI_RECAL_P0":                   "off",
            "BARI_GRAD_SODIUM_V1":             "off",
            "BARI_SODIUM_SHELF_RELATIVE_V1":   "off",
            "BARI_DAIRY_PROTEIN_REWEIGHT_V1":  "off",
            "BARI_REDLABEL_V1":                "off",
            "BARI_SODIUM_CEREAL":              "off",
            "BARI_TASK144_FIXES":              "off",
            "BARI_FAT_TECH_V1":                "on",
            "BARI_D4_SCORE_V1":                "off",
            "BARI_HC_DAIRY_SATFAT_V1":         "off",
            "BARI_SHELF_RELATIVE_V1":          "off",
        },
        "router_version": "router_v2.5",
        "flag_rationale": (
            "BARI_R3_BISCUIT_NARROW_V1 promoted to production-default ON by owner sign-off (TASK-394). "
            "This yields R3 for biscuit-anchored flavor-descriptor cookies: 2986065 and 7290017894317 "
            "stay biscuit/D instead of routing to snack_bar_granola/E. "
            "313184 and 7290018893845 are co-signed biscuit-path E→D corrections. "
            "BARI_FAT_TECH_V1=on is the engine default since 2026-06-15."
        ),
        "baseline": {
            "run_id": "cookies_coffee_frontend_v2.json (current live)",
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
        "score_trace_check": {
            "pass": len(score_trace_mismatch) == 0,
            "mismatch_count": len(score_trace_mismatch),
            "mismatches": score_trace_mismatch,
        },
        "distribution_assert": {
            "pass": True,
            "expected": {"C": 10, "D": 26, "E": 83},
            "actual": dict(sorted(grade_dist.items())),
        },
        "key_product_asserts": {bc: {"pass": True} for bc in KEY_PRODUCTS},
        "grade_changed_barcodes": sorted(GRADE_CHANGED_BARCODES),
        "no_corpus_match": no_corpus_match,
        "score_errors": score_errors,
        "engine_sha256": engine_sha,
        "signal_extractor_sha256": signal_sha,
        "evaluation_scope_sha256": eval_sha,
        "router_sha256": router_sha,
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
    print(f"TASK-393/394 FINAL: COOKIES-COFFEE PRODUCTION RE-SCORE — {RUN_ID}")
    print("=" * 72)
    print(f"Baseline: C10/D24/E85 (119 products, live frontend)")
    print(f"Rescored: {len(results)} products | Errors: {len(score_errors)} | No-corpus: {len(no_corpus_match)}")
    print(f"Flags: R3_BISCUIT_NARROW=on | FAT_TECH=on | D4_SCORE=off | all others off")
    print(f"\nNEW GRADE DISTRIBUTION (trace-derived from {len(trace_barcodes_on_disk)} traces):")
    for g in ["S", "A", "B", "C", "D", "E"]:
        count = grade_dist.get(g, 0)
        print(f"  {g}: {count}")
    print(f"\nSCORE STATS:")
    print(f"  Min={score_min} Max={score_max} Median={score_median} StDev={score_stdev} N={n}")
    print(f"  Most common: {most_common[0]} ({most_common[1]} products)")
    print(f"\nGRADE MOVERS: {len(grade_movers)}")
    for m in sorted(grade_movers, key=lambda x: x["barcode"]):
        print(f"  {m['barcode'][:20]}  {m['old_grade']}->{m['new_grade']}  {m['old_score']}->{m['new_score']}  cat={m['category']}")
    print(f"\nKEY PRODUCTS:")
    for bc, expected in KEY_PRODUCTS.items():
        actual_score = trace_score_map.get(bc)
        actual_grade = trace_grade_map.get(bc)
        actual_cat   = trace_cat_map.get(bc)
        print(f"  {bc}: cat={actual_cat} score={actual_score} grade={actual_grade}")
    print(f"\nSCORE==TRACE: {'PASS (0 mismatches)' if not score_trace_mismatch else 'FAIL ' + str(len(score_trace_mismatch)) + ' mismatches'}")
    print(f"\nCROSS-CATEGORY ISOLATION: {'PASS' if len(foreign_hits)==0 else 'FAIL — ' + str(len(foreign_hits)) + ' hits'}")
    print(f"\nARTIFACTS:")
    print(f"  Run dir:            {RUN_OUT}")
    print(f"  Run record:         {rr_path}")
    print(f"  Verification table: {verify_path}")
    print(f"  Grade mover table:  {mover_table_path}")
    print(f"  Score drift table:  {drift_table_path}")
    print(f"  Cross-cat scan:     {cross_cat_path}")
    print(f"  Traces:             {RUN_OUT}/products/ ({len(trace_barcodes_on_disk)} files)")
    print("=" * 72)

    return run_record, {
        "trace_score_map": trace_score_map,
        "trace_grade_map": trace_grade_map,
        "trace_cat_map":   trace_cat_map,
        "trace_full_map":  trace_full_map,
        "grade_changed_barcodes": GRADE_CHANGED_BARCODES,
    }


if __name__ == "__main__":
    run_record, score_data = main()
    # Export maps for the bake step (imported by the bake script or caller)
    import builtins
    builtins._task393_final_run_record = run_record
    builtins._task393_final_score_data = score_data
