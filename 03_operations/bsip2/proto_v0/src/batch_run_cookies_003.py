# BSIP2 batch -- Cookies-near-coffee (run_cookies_003) / TASK-275/P75b
# Mirrors batch_run_brined_cheeses_005.py structure. OFF ban: absolute.
# Flag config BEFORE engine imports (CRITICAL: cookies is NON-dairy / NON-brined)
import os, sys, json, pathlib, logging, datetime, hashlib
from collections import Counter

# --- Flag config BEFORE engine imports ---
os.environ["BARI_RECAL_P0"] = "off"           # sat-fat cliff cap 55 operative
os.environ["BARI_GRAD_SODIUM_V1"] = "off"      # brined-only; cookies are not brined
os.environ["BARI_SODIUM_SHELF_RELATIVE_V1"] = "off"
os.environ["BARI_DAIRY_PROTEIN_REWEIGHT_V1"] = "off"
os.environ["BARI_REDLABEL_V1"] = "off"
os.environ["BARI_SODIUM_CEREAL"] = "off"
# BARI_GLASSBOX_W4: leave at engine committed default (do NOT override; report what it is)

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
BSIP2_OUTPUT= ROOT/"02_products"/"cookies_coffee"/"bsip2_outputs"/"run_cookies_003"
RUN_ID = "run_cookies_003"

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
    for p in pens[:2]: drivers.append(f"-{p.get(chr(97)+chr(109)+chr(111)+chr(117)+chr(110)+chr(116),chr(63))} {p.get(chr(114)+chr(117)+chr(108)+chr(101),chr(63))}")
    for c in caps[:2]:
        if c.get("cap"): drivers.append(f"cap={c.get(chr(99)+chr(97)+chr(112),chr(63))} {c.get(chr(114)+chr(117)+chr(108)+chr(101),chr(63))}")
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
            "drivers":extract_drivers(t)}

def main():
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
    glassbox_w4 = os.environ.get("BARI_GLASSBOX_W4","engine_default(on)")
    log.info("=== BSIP2 Cookies-near-coffee -- %s ===", RUN_ID)
    log.info("Flags: RECAL_P0=off | GRAD_SODIUM=off | SHELF_RELATIVE=off | DAIRY_REWEIGHT=off | REDLABEL=off | SODIUM_CEREAL=off")
    log.info("BARI_GLASSBOX_W4: %s", glassbox_w4)

    corpus = json.loads(CORPUS_FILE.read_text(encoding="utf-8"))
    in_scored = {str(p["barcode"]) for p in corpus["products"] if p["decision"]=="IN_SCORED"}
    log.info("IN_SCORED barcodes: %d", len(in_scored))

    bsip1_records = []
    for p in sorted(BSIP1_DIR.glob("bsip1_cookies_*.json")):
        try:
            doc = json.loads(p.read_text(encoding="utf-8"))
            if str(doc.get("barcode","")) in in_scored:
                bsip1_records.append(doc)
        except Exception as e:
            log.error("Load error %s: %s", p.name, e)
    log.info("BSIP1 records loaded: %d", len(bsip1_records))
    if len(bsip1_records) != 61:
        log.warning("Expected 61 BSIP1 records, got %d", len(bsip1_records))

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
            log.info("  BSIP2 %-40s score=%-5s grade=%-2s cat=%-20s nova=%s ctx=%s",
                     name[:38], score, grade, cat, nova, ctx_flag or "standard")
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
    score_fld = "final_score_estimate"
    grade_fld = "grade_estimate"
    cap_fld   = "binding_cap"
    nova_fld  = "nova_proxy"
    ctx_fld   = "context_flag"
    with verify_path.open("w", encoding="utf-8", newline="") as vf:
        vf.write("barcode,score,grade,binding_cap,nova,fat_g,sat_fat_g,sugar_g,sodium_mg,context_flag" + chr(10))
        for t in sorted(traces, key=lambda x: str(x.get("barcode") or "")):
            bc = t.get("barcode") or (t.get("input_reference") or {}).get("barcode") or ""
            nn = {}
            for doc in bsip1_records:
                if str(doc.get("barcode")) == str(bc):
                    nn = doc.get("normalized_nutrition_per_100g") or {}
                    break
            row = ",".join(str(x) for x in [bc, t.get(score_fld), t.get(grade_fld),
                  t.get(cap_fld), t.get(nova_fld), nn.get("fat_g"), nn.get("fat_saturated_g"),
                  nn.get("sugars_g"), nn.get("sodium_mg"), t.get(ctx_fld)])
            vf.write(row + chr(10))

    eval_scope_sha = sha256_file(pathlib.Path(__file__).parent/"evaluation_scope.py")
    run_record = {
        "run_id":RUN_ID,"task":"TASK-275_P75b","category_slug":"cookies-coffee",
        "generated":ts,"engine":"proto_v0 / score_engine.py (unmodified)",
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
        "router_ev":"EV-058",
        "evaluation_scope_sha256":eval_scope_sha,
        "verification_table":str(verify_path),
        "top3":top3,"bottom3":bottom3,"errors":score_errors,
        "self_check":{"off_used":False,"brined_food_fired":len(brined_flag_fired),
                        "brined_food_guard_pass":len(brined_flag_fired)==0,
                        "scored_count":len(traces),"expected_count":61,"count_match":len(traces)==61},
    }
    rr_path = BSIP2_OUTPUT/"run_record.json"
    rr_path.write_text(json.dumps(run_record,ensure_ascii=False,indent=2),encoding="utf-8")
    log.info("Run record: %s", rr_path)
    log.info("Verification table: %s", verify_path)

    print(chr(10) + "="*70)
    print(f"COOKIES-NEAR-COFFEE BSIP2 RUN -- {RUN_ID}")
    print("="*70)
    print(f"Flags: RECAL_P0=off | GRAD_SODIUM=off | SHELF_RELATIVE=off | DAIRY_REWEIGHT=off")
    print(f"BARI_GLASSBOX_W4: {glassbox_w4}")
    print(f"Corpus: {len(in_scored)} IN_SCORED | BSIP1: {len(bsip1_records)}")
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
    print(f"BRINED_FOOD GUARD: fired={len(brined_flag_fired)}/61 -- {brined_status}")
    if brined_flag_fired:
        for p in brined_flag_fired: print(f"  CRITICAL: {p[chr(98)+chr(97)+chr(114)+chr(99)+chr(111)+chr(100)+chr(101)]} {p[chr(110)+chr(97)+chr(109)+chr(101)]}")
    print("TOP 3:")
    for i, p in enumerate(top3,1):
        print(f"  {i}. [{p[chr(115)+chr(99)+chr(111)+chr(114)+chr(101)]}/{p[chr(103)+chr(114)+chr(97)+chr(100)+chr(101)]}] {str(p.get(chr(110)+chr(97)+chr(109)+chr(101),chr(63)))[:50]} nova={p[chr(110)+chr(111)+chr(118)+chr(97)]}")
    print("BOTTOM 3:")
    for i, p in enumerate(bottom3,1):
        print(f"  {i}. [{p[chr(115)+chr(99)+chr(111)+chr(114)+chr(101)]}/{p[chr(103)+chr(114)+chr(97)+chr(100)+chr(101)]}] {str(p.get(chr(110)+chr(97)+chr(109)+chr(101),chr(63)))[:50]} nova={p[chr(110)+chr(111)+chr(118)+chr(97)]}")
    print(f"evaluation_scope.py SHA256: {eval_scope_sha[:16]}...")
    print(f"Run record: {rr_path}")
    print(f"BSIP2 dir:  {BSIP2_OUTPUT}")
    print("="*70)
    return run_record

if __name__ == "__main__":
    main()
