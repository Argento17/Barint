# BSIP2 batch -- Cookies-near-coffee (run_cookies_005) / TASK-275
# Engine fixes: Fix-A (ingredient truncation), Fix-B (PHVO markers), Fix-C (fat_quality ceiling).
# Inherits run_cookies_004 corpus (58 products). No flag changes from run_004.
# Flag config BEFORE engine imports (CRITICAL: cookies is NON-dairy / NON-brined)
import os, sys, json, pathlib, logging, datetime, hashlib
from collections import Counter

# --- Flag config BEFORE engine imports (identical to run_cookies_004) ---
os.environ["BARI_RECAL_P0"] = "off"
os.environ["BARI_GRAD_SODIUM_V1"] = "off"
os.environ["BARI_SODIUM_SHELF_RELATIVE_V1"] = "off"
os.environ["BARI_DAIRY_PROTEIN_REWEIGHT_V1"] = "off"
os.environ["BARI_REDLABEL_V1"] = "off"
os.environ["BARI_SODIUM_CEREAL"] = "off"

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, str(pathlib.Path(__file__).parent))

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

ROOT        = pathlib.Path(r"C:\Bari")
BSIP0_FILE  = ROOT/"02_products"/"cookies_coffee"/"bsip0_outputs"/"cookies_coffee_bsip0_raw_20260613T163431.json"
CORPUS_FILE = ROOT/"02_products"/"cookies_coffee"/"factory_run_001"/"corpus_filter.json"
BSIP1_DIR   = ROOT/"03_operations"/"bsip1"/"run_cookies_001"/"output"
BSIP2_OUTPUT= ROOT/"02_products"/"cookies_coffee"/"bsip2_outputs"/"run_cookies_005"
RUN_ID = "run_cookies_005"
EXPECTED_COUNT = 58

(BSIP2_OUTPUT/"products").mkdir(parents=True, exist_ok=True)

def run_bsip2_pipeline(bsip1_product):
    signals      = extract_signals(bsip1_product)
    cat_result   = classify_category(bsip1_product)
    l3           = signals["L3_inferred_classifications"]
    nova_result  = infer_nova(bsip1_product, l3)
    eval_result  = assign_evaluation_scope(bsip1_product, cat_result["category"])
    score_result = score_product(bsip1_product, signals, cat_result, nova_result, eval_result)
    trace        = assemble_trace(bsip1_product, signals, cat_result, nova_result, eval_result, score_result)
    trace["structural_class"] = classify_structural_class(trace)
    return trace

def sha256_file(path):
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()

def stdev(scores):
    if not scores: return 0.0
    n = len(scores); mean = sum(scores)/n
    return (sum((x-mean)**2 for x in scores)/n)**0.5

def extract_drivers(t):
    pens = t.get("penalties_applied",[]) or []
    caps = t.get("caps_applied",[]) or []
    drivers = []
    for p in pens[:2]: drivers.append(f"-{p.get('amount','?')} {p.get('rule','?')}")
    for c in caps[:2]:
        if c.get("cap"): drivers.append(f"cap={c.get('cap','?')} {c.get('rule','?')}")
    return drivers or ["(no drivers)"]

def trace_summary(t, bsip1_records):
    bc = t.get("barcode") or (t.get("input_reference") or {}).get("barcode")
    name = (t.get("input_reference") or {}).get("product_name_he") or t.get("canonical_name_he")
    nn = {}
    for doc in bsip1_records:
        if str(doc.get("barcode")) == str(bc):
            nn = doc.get("normalized_nutrition_per_100g") or {}
            break
    return {"barcode":bc,"name":name,"score":t.get("final_score_estimate"),
            "grade":t.get("grade_estimate"),"nova":t.get("nova_proxy"),
            "context_flag":t.get("context_flag"),"binding_cap":t.get("binding_cap"),
            "category":t.get("category"),
            "drivers":extract_drivers(t)}

def main():
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
    glassbox_w4 = os.environ.get("BARI_GLASSBOX_W4","engine_default(on)")
    log.info("=== BSIP2 Cookies-near-coffee -- %s (TASK-275 engine fixes) ===", RUN_ID)
    log.info("Fixes: Fix-A ingredient-truncation | Fix-B PHVO markers | Fix-C fat_quality ceil@40")
    log.info("Flags: RECAL_P0=off | GRAD_SODIUM=off | SHELF_RELATIVE=off | DAIRY_REWEIGHT=off | REDLABEL=off | SODIUM_CEREAL=off")

    corpus = json.loads(CORPUS_FILE.read_text(encoding="utf-8"))
    in_scored = {str(p["barcode"]) for p in corpus["products"] if p["decision"]=="IN_SCORED"}
    log.info("IN_SCORED barcodes: %d (expected %d)", len(in_scored), EXPECTED_COUNT)

    bsip1_records = []
    for p in sorted(BSIP1_DIR.glob("bsip1_cookies_*.json")):
        try:
            doc = json.loads(p.read_text(encoding="utf-8"))
            if str(doc.get("barcode","")) in in_scored:
                bsip1_records.append(doc)
        except Exception as e:
            log.error("Load error %s: %s", p.name, e)
    log.info("BSIP1 records loaded: %d", len(bsip1_records))

    traces, score_errors, brined_flag_fired, routing_cats = [], [], [], {}

    for doc in bsip1_records:
        barcode = str(doc.get("barcode",""))
        name    = doc.get("canonical_name_he","")
        try:
            trace = run_bsip2_pipeline(doc)
            write_trace(trace, BSIP2_OUTPUT)
            traces.append(trace)
            score = trace.get("final_score_estimate"); grade = trace.get("grade_estimate")
            cat = trace.get("category"); nova = trace.get("nova_proxy")
            ctx_flag = trace.get("context_flag")
            routing_cats[cat] = routing_cats.get(cat,0) + 1
            if ctx_flag == "brined_food":
                brined_flag_fired.append({"barcode":barcode,"name":name,"score":score,"grade":grade,"CRITICAL":"brined_food fired on a cookie"})
                log.error("  CRITICAL: brined_food fired on %s (%s)!", barcode, name)
            # Log has_phvo for PHVO-relevant products
            l3 = trace.get("L3_inferred_classifications") or {}
            has_phvo = l3.get("has_phvo", False)
            fq_note = (trace.get("dimension_notes") or {}).get("fat_quality","")
            if has_phvo:
                log.info("  PHVO %-40s score=%-5s grade=%-2s fq_note=%s", name[:38], score, grade, fq_note[:60])
            else:
                log.info("  BSIP2 %-40s score=%-5s grade=%-2s cat=%-20s nova=%s", name[:38], score, grade, cat, nova)
        except Exception as e:
            log.error("  BSIP2 ERROR %s (%s): %s", barcode, name, e)
            import traceback; traceback.print_exc()
            score_errors.append({"barcode":barcode,"name":name,"error":str(e)})

    all_scores = [t.get("final_score_estimate") for t in traces if t.get("final_score_estimate") is not None]
    grade_dist = {}
    for t in traces:
        g = t.get("grade_estimate","?")
        grade_dist[g] = grade_dist.get(g,0)+1
    if all_scores:
        ss = sorted(all_scores); n = len(ss)
        median = ss[n//2] if n%2 else (ss[n//2-1]+ss[n//2])/2
        score_min = min(all_scores); score_max = max(all_scores)
        score_stdev = round(stdev(all_scores),2)
        score_range = score_max - score_min
        mc = Counter(all_scores).most_common(1)[0]
        most_common_score, most_common_count = mc[0], mc[1]
    else:
        median=score_min=score_max=score_stdev=score_range=most_common_score=most_common_count=None
    histogram = {}
    for s in (all_scores or []):
        band = f"{int(s//10)*10}-{int(s//10)*10+9}"
        histogram[band] = histogram.get(band,0)+1
    score_range_v = round(score_range,2) if score_range else None
    grade_bands = len([g for g in grade_dist if g not in ("?",None)])
    if score_range and score_range>=20 and grade_bands>=2:
        anti_collapse = f"SPREAD_HONEST: range={score_range:.1f} pts ({score_min}-{score_max}), {grade_bands} grade bands"
    elif score_range and score_range<10:
        anti_collapse = f"CLUSTERED: range={score_range:.1f} pts, {grade_bands} grade bands"
    else:
        anti_collapse = f"MODERATE_SPREAD: range={score_range} pts, {grade_bands} grade bands"

    tsd = sorted([t for t in traces if t.get("final_score_estimate") is not None],
                 key=lambda t: t.get("final_score_estimate",0), reverse=True)
    top3    = [trace_summary(t, bsip1_records) for t in tsd[:3]]
    bottom3 = [trace_summary(t, bsip1_records) for t in tsd[-3:]]

    verify_path = BSIP2_OUTPUT/"verification_table.csv"
    with verify_path.open("w", encoding="utf-8", newline="") as vf:
        vf.write("barcode,score,grade,binding_cap,nova,fat_g,sat_fat_g,sugar_g,sodium_mg,context_flag,category,has_phvo\n")
        for t in sorted(traces, key=lambda x: str(x.get("barcode") or "")):
            bc = t.get("barcode") or (t.get("input_reference") or {}).get("barcode") or ""
            nn = {}
            for doc in bsip1_records:
                if str(doc.get("barcode")) == str(bc):
                    nn = doc.get("normalized_nutrition_per_100g") or {}
                    break
            l3 = t.get("L3_inferred_classifications") or {}
            row = ",".join(str(x) for x in [bc, t.get("final_score_estimate"), t.get("grade_estimate"),
                  t.get("binding_cap"), t.get("nova_proxy"), nn.get("fat_g"), nn.get("fat_saturated_g"),
                  nn.get("sugars_g"), nn.get("sodium_mg"), t.get("context_flag"), t.get("category"),
                  l3.get("has_phvo", False)])
            vf.write(row + "\n")

    eval_scope_sha = sha256_file(pathlib.Path(__file__).parent/"evaluation_scope.py")
    signal_extractor_sha = sha256_file(pathlib.Path(__file__).parent/"signal_extractor.py")
    score_engine_sha = sha256_file(pathlib.Path(__file__).parent/"score_engine.py")

    run_record = {
        "run_id":RUN_ID,"task":"TASK-275","category_slug":"cookies-coffee",
        "generated":ts,"engine":"proto_v0 / score_engine.py (Fix-B+Fix-C applied)",
        "engine_fixes":{
            "fix_a":"build_bsip1_cookies_001.py: _rfind_outside_parens replaces rfind for allergen-strip",
            "fix_b":"signal_extractor.py: added PHVO markers: שומנים מוקשים, שומן מוקשה, מחמאה, מרגרינה",
            "fix_c":"score_engine.py: fat_quality dimension ceiling=40 when has_phvo==True",
        },
        "flag_config":{"BARI_RECAL_P0":"off","BARI_GRAD_SODIUM_V1":"off",
                        "BARI_SODIUM_SHELF_RELATIVE_V1":"off","BARI_DAIRY_PROTEIN_REWEIGHT_V1":"off",
                        "BARI_REDLABEL_V1":"off","BARI_SODIUM_CEREAL":"off",
                        "BARI_GLASSBOX_W4":glassbox_w4},
        "off_used":False,"corpus_source":str(CORPUS_FILE),"bsip0_source":str(BSIP0_FILE),
        "in_scored_count":len(in_scored),"bsip1_source":str(BSIP1_DIR),
        "bsip1":{"records_loaded":len(bsip1_records)},
        "bsip2":{"output_dir":str(BSIP2_OUTPUT),"scored":len(traces),"errors":len(score_errors)},
        "score_distribution":{"min":score_min,"max":score_max,"median":median,
                                "stdev":score_stdev,"range":score_range_v,
                                "most_common_score":most_common_score,"most_common_count":most_common_count,
                                "histogram":histogram,"grade_dist":grade_dist},
        "anti_collapse_verdict":anti_collapse,
        "routing_distribution":routing_cats,
        "brined_flag":{"fired_count":len(brined_flag_fired),"guard_pass":len(brined_flag_fired)==0,
                         "fired_products":brined_flag_fired},
        "evaluation_scope_sha256":eval_scope_sha,
        "signal_extractor_sha256":signal_extractor_sha,
        "score_engine_sha256":score_engine_sha,
        "verification_table":str(verify_path),
        "top3":top3,"bottom3":bottom3,"errors":score_errors,
        "self_check":{"off_used":False,"brined_food_fired":len(brined_flag_fired),
                        "brined_food_guard_pass":len(brined_flag_fired)==0,
                        "scored_count":len(traces),"expected_count":EXPECTED_COUNT,
                        "count_match":len(traces)==EXPECTED_COUNT},
    }
    rr_path = BSIP2_OUTPUT/"run_record.json"
    rr_path.write_text(json.dumps(run_record,ensure_ascii=False,indent=2),encoding="utf-8")
    log.info("Run record: %s", rr_path)

    print("\n" + "="*70)
    print(f"COOKIES-NEAR-COFFEE BSIP2 RUN -- {RUN_ID} (TASK-275 ENGINE FIXES)")
    print("="*70)
    print(f"Fix-A: ingredient truncation | Fix-B: PHVO markers | Fix-C: fat_quality ceil@40")
    print(f"Flags: RECAL_P0=off | GRAD_SODIUM=off | SHELF_RELATIVE=off | DAIRY_REWEIGHT=off")
    print(f"Corpus: {len(in_scored)} IN_SCORED (expected {EXPECTED_COUNT}) | BSIP1: {len(bsip1_records)}")
    print(f"BSIP2 scored: {len(traces)} | errors: {len(score_errors)}")
    print("ROUTING DISTRIBUTION:")
    for cat, cnt in sorted(routing_cats.items()): print(f"  {cat}: {cnt}")
    print("SCORE DISTRIBUTION:")
    print(f"  Min: {score_min}  Max: {score_max}  Median: {median}  StDev: {score_stdev}")
    print(f"  Range: {score_range_v}")
    print(f"  Histogram: {dict(sorted(histogram.items()))}")
    print(f"  Grade distribution: {dict(sorted(grade_dist.items()))}")
    print(f"  Most common score: {most_common_score} ({most_common_count} products)")
    brined_status = "PASS" if len(brined_flag_fired)==0 else "FAIL (CRITICAL)"
    print(f"BRINED_FOOD GUARD: fired={len(brined_flag_fired)}/{EXPECTED_COUNT} -- {brined_status}")
    print("TOP 3:")
    for i, p in enumerate(top3,1):
        print(f"  {i}. [{p['score']}/{p['grade']}] {str(p.get('name','?'))[:50]} nova={p['nova']}")
    print("BOTTOM 3:")
    for i, p in enumerate(bottom3,1):
        print(f"  {i}. [{p['score']}/{p['grade']}] {str(p.get('name','?'))[:50]} nova={p['nova']}")
    print(f"signal_extractor.py SHA256: {signal_extractor_sha[:16]}...")
    print(f"score_engine.py SHA256:     {score_engine_sha[:16]}...")
    print(f"Run record: {rr_path}")
    print("="*70)
    return run_record

if __name__ == "__main__":
    main()
