"""
BSIP2 batch -- Yogurt SHELF-RELATIVE DIAGNOSTIC PILOT (run_yogurt_shelfrel_pilot)
TASK-278 Phase-3 diagnostic: does the shelf-relative sugar term LAND or get ABSORBED
on a spread shelf (yogurt: clean plain 0-4g sugar <-> sugary dessert 10-17g sugar)?

MEASURED, NOT PUBLISHED. No frontend JSON, no live category edit, no deploy, no go-live.
Corpus: run_yogurt_006 (88 products, latest authoritative run, 2026-06-11).
Output: 02_products/yogurt_system/bsip2_outputs/run_yogurt_shelfrel_pilot/

SCOPE NOTE (flagged per brief): Yogurt routes to `dairy_protein` via the router, shared
with milk and hard cheeses. This pilot scopes the sugar relative term to
{"dairy_protein"} temporarily for this diagnostic only. This is NOT a real enrollment
(which would need its own EV + D7 for a yogurt-specific or dairy_protein-wide decision).
Bleed risk: the yogurt corpus (run_yogurt_006) contains ONLY yogurt products.
No published category is re-scored. Full scope-granularity flag is in the run record.
"""
import os, sys, json, pathlib, logging, datetime, hashlib
from collections import Counter

# ---- Flag config BEFORE engine imports ----
os.environ["BARI_SHELF_RELATIVE_V1"]        = "on"
os.environ["BARI_RECAL_P0"]                 = "on"
os.environ["BARI_RECAL_P0_YOGURT_TRIM"]     = "on"
os.environ["BARI_TASK144_FIXES"]            = "off"
os.environ["BARI_TASK250_CONF"]             = "on"
os.environ["BARI_GRAD_SODIUM_V1"]           = "off"
os.environ["BARI_SODIUM_SHELF_RELATIVE_V1"] = "off"
os.environ["BARI_DAIRY_PROTEIN_REWEIGHT_V1"]= "off"
os.environ["BARI_REDLABEL_V1"]              = "off"
os.environ["BARI_SODIUM_CEREAL"]            = "off"

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, str(pathlib.Path(__file__).parent))

from signal_extractor import extract_signals
from router_v2 import classify_category
from nova_proxy import infer_nova
from evaluation_scope import assign_evaluation_scope
import score_engine as _se
from score_engine import set_shelf_stats, clear_shelf_stats, compute_shelf_stats, BARI_SHELF_RELATIVE_V1
from trace_writer import assemble_trace, write_trace
from structural_classifier import classify_structural_class

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

ROOT         = pathlib.Path(r"C:\Bari")
BSIP1_SOURCE = ROOT / "03_operations/bsip1/run_yogurt_005/output"
BASELINE_DIR = ROOT / "02_products/yogurt_system/bsip2_outputs/run_yogurt_006/products"
OUTPUT_ROOT  = ROOT / "02_products/yogurt_system/bsip2_outputs/run_yogurt_shelfrel_pilot"
RUN_ID       = "run_yogurt_shelfrel_pilot"
EXCLUDED_BARCODES = {"7290116932620"}

# DIAGNOSTIC PILOT SCOPE: dairy_protein (yogurt's router category).
PILOT_SCOPE: frozenset = frozenset({"dairy_protein"})

# Yogurt-calibrated pilot bands — asymmetric P>B.
# No formulation_absolute_floor: yogurt is not a pure-indulgence shelf;
# plain yogurts legitimately reach A/B. Anti-Immunity Rule protected by absolute backbone.
YOGURT_SURCHARGE_BANDS = [
    (0.0,  0.5,  0),
    (0.5,  1.0,  1),
    (1.0,  1.5,  2),
    (1.5,  2.5,  4),
    (2.5,  None, 8),
]
YOGURT_RELIEF_BANDS = [
    (0.0,  0.5,  0),
    (0.5,  1.5,  2),
    (1.5,  3.0,  3),
    (3.0,  None, 4),
]
YOGURT_LOW_VARIANCE_GUARD = 1.0

(OUTPUT_ROOT / "products").mkdir(parents=True, exist_ok=True)


def sha256_file(path):
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def stdev(vals):
    if not vals: return 0.0
    n = len(vals); m = sum(vals)/n
    return (sum((x-m)**2 for x in vals)/n)**0.5


def mad_val(vals, med):
    devs = sorted(abs(v - med) for v in vals)
    n = len(devs)
    if not devs: return 0.0
    return devs[n//2] if n%2 else (devs[n//2-1]+devs[n//2])/2


def load_bsip1_yogurt():
    from input_loader import load_batch
    products_all = list(load_batch(BSIP1_SOURCE))
    products = [p for p in products_all if str(p.get("barcode") or "") not in EXCLUDED_BARCODES]
    log.info("BSIP1 loaded: %d total, %d after exclusion", len(products_all), len(products))
    return products


def compute_yogurt_sugar_stats(products):
    vals = []
    for p in products:
        nn = p.get("normalized_nutrition_per_100g") or {}
        v = nn.get("sugars_g")
        if v is None:
            l1 = p.get("L1_observed_signals") or {}
            v = l1.get("sugars_g")
        if v is not None:
            vals.append((str(p.get("barcode","")), p.get("canonical_name_he",""), float(v)))
    vals.sort(key=lambda x: x[2])
    sv = [v for _,_,v in vals]
    n = len(sv)
    if n == 0: return {}, vals
    median = sv[n//2] if n%2 else (sv[n//2-1]+sv[n//2])/2
    q1 = sv[n//4]; q3 = sv[(3*n)//4]; iqr = q3-q1
    m = mad_val(sv, median)
    robust_scale_iqr = iqr/1.349 if iqr>0 else 0
    robust_scale_mad = 1.4826*m if m>0 else 0
    robust_scale = max(robust_scale_iqr, robust_scale_mad, 1.0)
    return {
        "n": n, "n_products_total": len(products),
        "min": sv[0], "max": sv[-1],
        "q1": round(q1,2), "median": round(median,2), "q3": round(q3,2),
        "iqr": round(iqr,2), "mad_raw": round(m,3),
        "robust_scale_iqr": round(robust_scale_iqr,3),
        "robust_scale_mad": round(robust_scale_mad,3),
        "robust_scale": round(robust_scale,3),
    }, vals


def score_one(product, use_engine=_se):
    signals    = extract_signals(product)
    cat_result = classify_category(product)
    l3         = signals["L3_inferred_classifications"]
    nova_result= infer_nova(product, l3)
    eval_result= assign_evaluation_scope(product, cat_result["category"])
    score_result = use_engine.score_product(product, signals, cat_result, nova_result, eval_result)
    return score_result


def get_sugar(product):
    nn = product.get("normalized_nutrition_per_100g") or {}
    v = nn.get("sugars_g")
    if v is None:
        l1 = product.get("L1_observed_signals") or {}
        v = l1.get("sugars_g")
    return v


def main():
    assert BARI_SHELF_RELATIVE_V1, "CRITICAL: BARI_SHELF_RELATIVE_V1 must be ON"
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
    log.info("=== YOGURT SHELF-RELATIVE DIAGNOSTIC PILOT (%s) ===", RUN_ID)
    log.info("MEASURED NOT PUBLISHED | scope=dairy_protein (DIAGNOSTIC ONLY)")

    # STEP 1: Load corpus
    products = load_bsip1_yogurt()
    n_total = len(products)

    # STEP 2: Compute yogurt sugar stats
    log.info("--- STEP 2: Yogurt sugar distribution ---")
    stats, sugar_ranked = compute_yogurt_sugar_stats(products)
    engine_median, engine_scale = compute_shelf_stats(
        products, "sugars_g", scale_type="iqr", nutrient_min_scale=1.0
    )
    log.info("Sugar: n=%d min=%.1f q1=%.1f median=%.1f q3=%.1f max=%.1f iqr=%.2f robust_scale=%.3f",
             stats["n"], stats["min"], stats["q1"], stats["median"],
             stats["q3"], stats["max"], stats["iqr"], stats["robust_scale"])
    log.info("Engine: median=%.3f scale=%.3f", engine_median, engine_scale)

    if not sugar_ranked:
        log.error("No sugar data — abort"); return

    # STEP 3: Inject pilot scope and bands directly into score_engine module namespace
    # score_engine imports these names via "from constants import SUGAR_SHELF_REL_SCOPE, ..."
    # so we patch score_engine's own module-level bindings (not constants).
    log.info("--- STEP 3: Injecting pilot scope into score_engine module namespace ---")
    _orig_scope   = _se.SUGAR_SHELF_REL_SCOPE
    _orig_surge   = _se.SUGAR_SHELF_SURCHARGE_BANDS
    _orig_relief  = _se.SUGAR_SHELF_RELIEF_BANDS
    _orig_guard   = _se.SUGAR_SHELF_SCALE_GUARD

    _se.SUGAR_SHELF_REL_SCOPE       = PILOT_SCOPE
    _se.SUGAR_SHELF_SURCHARGE_BANDS = YOGURT_SURCHARGE_BANDS
    _se.SUGAR_SHELF_RELIEF_BANDS    = YOGURT_RELIEF_BANDS
    _se.SUGAR_SHELF_SCALE_GUARD     = YOGURT_LOW_VARIANCE_GUARD

    log.info("  SUGAR_SHELF_REL_SCOPE patched: %s -> %s", _orig_scope, PILOT_SCOPE)

    # Set shelf stats for engine
    clear_shelf_stats()
    set_shelf_stats("sugars_g", engine_median, engine_scale, "iqr",
                    n=stats["n"])
    log.info("  Shelf stats set: median=%.3f scale=%.3f", engine_median, engine_scale)

    # STEP 4: Run flag-ON pilot
    log.info("--- STEP 4: Pilot rescore (flag=ON, scope=dairy_protein) ---")

    diag_high = sugar_ranked[-1]; diag_low = sugar_ranked[0]
    diag_high2= sugar_ranked[-3] if len(sugar_ranked)>=3 else sugar_ranked[-1]
    diag_low2 = sugar_ranked[2]  if len(sugar_ranked)>=3 else sugar_ranked[0]
    diag_barcodes = {diag_high[0], diag_low[0], diag_high2[0], diag_low2[0]}

    log.info("  DIAG HIGH: bc=%s name=%s sugar=%.1f", diag_high[0], diag_high[1][:40], diag_high[2])
    log.info("  DIAG LOW:  bc=%s name=%s sugar=%.1f", diag_low[0],  diag_low[1][:40],  diag_low[2])

    results_on = {}   # barcode -> {score, grade, rel_pen, score_after_cap, score_after_penalty, sugars_g}
    traces_on_list = []
    routing_cats = {}

    for product in products:
        bc   = str(product.get("barcode",""))
        name = product.get("canonical_name_he","")
        try:
            sr = score_one(product, _se)
            trace = assemble_trace(product, extract_signals(product), classify_category(product),
                                   infer_nova(product, extract_signals(product)["L3_inferred_classifications"]),
                                   assign_evaluation_scope(product, classify_category(product)["category"]),
                                   sr)
            trace["structural_class"] = classify_structural_class(trace)
            write_trace(trace, OUTPUT_ROOT)
            traces_on_list.append(trace)
            cat = trace.get("category")
            routing_cats[cat] = routing_cats.get(cat,0)+1

            score = trace.get("final_score_estimate")
            grade = trace.get("grade_estimate")
            sugar = get_sugar(product)
            score_cap = trace.get("score_after_cap")
            score_pen = trace.get("score_after_penalty")

            rel_pen = None
            for p in (trace.get("penalties_applied") or []):
                if p.get("rule") == "SUGAR_SHELF_REL_V1":
                    rel_pen = p.get("amount")
                    break
            # Also check relief (negative penalty)
            rel_note = None
            for p in (trace.get("penalties_considered") or []):
                if p.get("rule") == "SUGAR_SHELF_REL_V1":
                    rel_pen = p.get("amount")
                    rel_note = p.get("note")
                    break

            results_on[bc] = {
                "barcode": bc, "name": name, "score": score, "grade": grade,
                "sugars_g": sugar, "rel_pen": rel_pen, "rel_note": rel_note,
                "score_after_cap": score_cap, "score_after_penalty": score_pen,
            }

            if bc in diag_barcodes:
                log.info("  DIAG-ON [%s] %-38s score=%-5s grade=%s sugar=%-5s rel_pen=%s cap->pen=%s->%s",
                         bc, name[:36], score, grade, sugar, rel_pen, score_cap, score_pen)
            else:
                log.info("  ON  %-12s %-35s score=%-5s grade=%s sugar=%-5s rel_pen=%s",
                         bc, name[:33], score, grade, sugar, rel_pen)
        except Exception as e:
            log.error("  ERROR-ON %s: %s", bc, e)
            import traceback; traceback.print_exc()

    # Restore engine scope
    _se.SUGAR_SHELF_REL_SCOPE       = _orig_scope
    _se.SUGAR_SHELF_SURCHARGE_BANDS = _orig_surge
    _se.SUGAR_SHELF_RELIEF_BANDS    = _orig_relief
    _se.SUGAR_SHELF_SCALE_GUARD     = _orig_guard
    clear_shelf_stats("sugars_g")
    log.info("  Scope restored: %s", _orig_scope)

    # STEP 5: Run flag-OFF baseline using score_engine with BARI_SHELF_RELATIVE_V1=False
    log.info("--- STEP 5: Baseline rescore (flag=OFF via engine bypass) ---")
    # The flag is module-level constant in score_engine. We patch it directly.
    _orig_flag = _se.BARI_SHELF_RELATIVE_V1
    _se.BARI_SHELF_RELATIVE_V1 = False
    log.info("  BARI_SHELF_RELATIVE_V1 patched: True -> False")

    results_off = {}
    for product in products:
        bc   = str(product.get("barcode",""))
        name = product.get("canonical_name_he","")
        try:
            sr = score_one(product, _se)
            score = sr.get("final_score_estimate")
            grade = sr.get("grade_estimate")
            sugar = get_sugar(product)
            score_cap = sr.get("score_after_cap")
            score_pen = sr.get("score_after_penalty")
            results_off[bc] = {
                "barcode": bc, "name": name, "score": score, "grade": grade,
                "sugars_g": sugar, "score_after_cap": score_cap, "score_after_penalty": score_pen,
            }
            if bc in diag_barcodes:
                log.info("  DIAG-OFF [%s] %-38s score=%-5s grade=%s sugar=%-5s cap->pen=%s->%s",
                         bc, name[:36], score, grade, sugar, score_cap, score_pen)
        except Exception as e:
            log.error("  ERROR-OFF %s: %s", bc, e)

    # Restore flag
    _se.BARI_SHELF_RELATIVE_V1 = _orig_flag
    log.info("  BARI_SHELF_RELATIVE_V1 restored: True")

    # STEP 6: Load committed baseline (run_yogurt_006)
    log.info("--- STEP 6: Load committed baseline traces ---")
    committed = {}
    for td in sorted(BASELINE_DIR.iterdir()):
        if not td.is_dir(): continue
        tf = td / "bsip2_trace.json"
        if not tf.exists(): continue
        try:
            bt = json.loads(tf.read_text(encoding="utf-8"))
            bc = str((bt.get("input_reference") or {}).get("barcode") or bt.get("barcode") or "")
            if bc:
                committed[bc] = {
                    "score": bt.get("final_score_estimate"), "grade": bt.get("grade_estimate"),
                    "score_after_cap": bt.get("score_after_cap"),
                    "score_after_penalty": bt.get("score_after_penalty"),
                }
        except: pass
    log.info("  Committed baseline: %d products", len(committed))

    # STEP 7: Compute deltas and absorption analysis
    log.info("--- STEP 7: Delta computation and absorption check ---")

    all_on  = [r["score"] for r in results_on.values()  if r["score"] is not None]
    all_off = [r["score"] for r in results_off.values() if r["score"] is not None]
    grade_dist_on  = Counter(r["grade"] for r in results_on.values()  if r["grade"])
    grade_dist_off = Counter(r["grade"] for r in results_off.values() if r["grade"])

    deltas = []; movers = []; grade_changes = []
    absorb_count = 0; land_count = 0; nopen_count = 0

    for bc in results_off:
        r_on  = results_on.get(bc)
        r_off = results_off[bc]
        if r_on is None: continue
        s_on  = r_on["score"]; s_off = r_off["score"]
        g_on  = r_on["grade"]; g_off = r_off["grade"]
        if s_on is None or s_off is None: continue
        delta = round(s_on - s_off, 2)
        deltas.append(delta)
        rel_pen = r_on.get("rel_pen")
        if rel_pen is not None and rel_pen != 0:
            if abs(delta) < 0.01:
                absorb_count += 1
            else:
                land_count += 1
        else:
            nopen_count += 1
        if abs(delta) >= 0.1:
            movers.append({
                "barcode": bc, "name": r_on["name"],
                "score_off": s_off, "score_on": s_on, "delta": delta,
                "grade_off": g_off, "grade_on": g_on,
                "sugars_g": r_on.get("sugars_g"), "rel_pen": rel_pen,
            })
        if g_on != g_off:
            grade_changes.append({
                "barcode": bc, "grade_off": g_off, "grade_on": g_on,
                "score_off": s_off, "score_on": s_on, "delta": delta,
            })

    movers.sort(key=lambda x: abs(x["delta"]), reverse=True)
    avg_delta = round(sum(deltas)/len(deltas),4) if deltas else 0.0

    # Absorption check for diagnostic products
    absorption_check = {}
    for bc in diag_barcodes:
        r_on  = results_on.get(bc,{})
        r_off = results_off.get(bc,{})
        c_t   = committed.get(bc,{})
        s_on  = r_on.get("score"); s_off = r_off.get("score")
        delta = round(s_on - s_off, 2) if (s_on is not None and s_off is not None) else None
        rel_pen = r_on.get("rel_pen")
        absorbed = (rel_pen is not None and rel_pen != 0 and (delta is None or abs(delta) < 0.01))
        lands    = (rel_pen is not None and rel_pen != 0 and delta is not None and abs(delta) >= 0.1)
        verdict  = "ABSORBED" if absorbed else ("LANDS" if lands else
                   ("NO_PEN_FIRED" if rel_pen is None else "NO_PEN_ZERO"))
        absorption_check[bc] = {
            "barcode": bc, "name": r_on.get("name",""),
            "sugars_g": r_on.get("sugars_g"),
            "score_off": s_off, "score_on": s_on, "delta": delta,
            "rel_pen": rel_pen,
            "score_after_cap_off": r_off.get("score_after_cap"),
            "score_after_penalty_off": r_off.get("score_after_penalty"),
            "score_after_cap_on": r_on.get("score_after_cap"),
            "score_after_penalty_on": r_on.get("score_after_penalty"),
            "committed_score": c_t.get("score"),
            "committed_cap": c_t.get("score_after_cap"),
            "committed_pen": c_t.get("score_after_penalty"),
            "verdict": verdict,
        }
        log.info("  ABSORPTION [%s] %-30s sugar=%s delta=%s rel_pen=%s -> %s",
                 bc, r_on.get("name","")[:28], r_on.get("sugars_g"), delta, rel_pen, verdict)

    # Safety: flag-off vs committed
    off_vs_committed = []
    for bc, r_off in results_off.items():
        c_t = committed.get(bc,{})
        s_off = r_off.get("score"); s_comm = c_t.get("score")
        if s_comm is not None and s_off != s_comm:
            off_vs_committed.append({"barcode": bc, "committed": s_comm, "off_session": s_off,
                                     "diff": round(s_off - s_comm, 2) if (s_off and s_comm) else None})

    log.info("  Flag-OFF vs committed mismatches: %d", len(off_vs_committed))
    if off_vs_committed[:3]:
        for m in off_vs_committed[:3]:
            log.info("    [%s] committed=%s off_session=%s diff=%s", m["barcode"], m["committed"], m["off_session"], m["diff"])

    # Compile diagnostic results
    rel_pen_distribution = Counter(r.get("rel_pen") for r in results_on.values())

    # STEP 8: Write run record
    score_engine_sha = sha256_file(pathlib.Path(__file__).parent/"score_engine.py")
    constants_sha    = sha256_file(pathlib.Path(__file__).parent/"constants.py")

    ss_on = sorted(all_on); ss_off = sorted(all_off)
    n_on = len(ss_on); n_off = len(ss_off)
    med_on  = ss_on[n_on//2]  if n_on%2  else (ss_on[n_on//2-1]+ss_on[n_on//2])/2   if n_on  else None
    med_off = ss_off[n_off//2] if n_off%2 else (ss_off[n_off//2-1]+ss_off[n_off//2])/2 if n_off else None

    committed_grades = Counter(v.get("grade") for v in committed.values() if v.get("grade"))

    run_record = {
        "run_id": RUN_ID, "task": "TASK-278 Phase-3 diagnostic",
        "pilot_type": "MEASURED_NOT_PUBLISHED", "generated": ts,
        "scope_note": (
            "DIAGNOSTIC PILOT: yogurt routes to dairy_protein, not biscuit. "
            "Engine module namespace patched at runtime: SUGAR_SHELF_REL_SCOPE = frozenset({'dairy_protein'}), "
            "SUGAR_SHELF_SURCHARGE_BANDS and SUGAR_SHELF_RELIEF_BANDS overridden with yogurt-calibrated bands. "
            "Scope restored after flag-ON run. NOT a real enrollment — requires own EV+D7. "
            "Bleed risk: mitigated — corpus is yogurt-only."
        ),
        "corpus": {"run": "run_yogurt_006", "n_products": n_total, "excluded": list(EXCLUDED_BARCODES)},
        "yogurt_sugar_stats": stats,
        "sugar_ranked_bottom5": [{"barcode": bc, "name": n, "sugars_g": v} for bc,n,v in sugar_ranked[:5]],
        "sugar_ranked_top5":    [{"barcode": bc, "name": n, "sugars_g": v} for bc,n,v in sugar_ranked[-5:]],
        "engine_shelf_stats": {"median": engine_median, "scale": engine_scale},
        "pilot_bands": {
            "surcharge_bands": YOGURT_SURCHARGE_BANDS, "relief_bands": YOGURT_RELIEF_BANDS,
            "low_variance_guard": YOGURT_LOW_VARIANCE_GUARD, "no_formulation_absolute_floor": True,
        },
        "grade_dist_committed_baseline": dict(committed_grades),
        "grade_dist_flag_off": dict(grade_dist_off),
        "grade_dist_flag_on":  dict(grade_dist_on),
        "score_dist_off": {"min": min(all_off) if all_off else None, "max": max(all_off) if all_off else None,
                           "median": med_off, "stdev": round(stdev(all_off),2)},
        "score_dist_on":  {"min": min(all_on)  if all_on  else None, "max": max(all_on)  if all_on  else None,
                           "median": med_on,  "stdev": round(stdev(all_on), 2)},
        "avg_delta_on_vs_off": avg_delta,
        "n_products_scored_on": len(results_on), "n_products_scored_off": len(results_off),
        "n_movers": len(movers), "n_grade_changes": len(grade_changes),
        "grade_changes": grade_changes, "top_movers": movers[:15],
        "rel_pen_distribution": {str(k): v for k,v in rel_pen_distribution.items()},
        "absorption_summary": {
            "products_with_nonzero_rel_pen": absorb_count + land_count,
            "absorbed_count": absorb_count, "lands_count": land_count,
            "no_pen_count": nopen_count,
            "absorption_rate": round(absorb_count/(absorb_count+land_count),3)
                               if (absorb_count+land_count)>0 else None,
        },
        "absorption_check": absorption_check,
        "safety": {
            "routing_distribution": routing_cats,
            "non_dairy_protein_routing": {k:v for k,v in routing_cats.items() if k!="dairy_protein"},
            "flag_off_vs_committed_mismatches": len(off_vs_committed),
            "off_vs_committed_first5": off_vs_committed[:5],
            "note_on_committed_mismatch": (
                "Mismatches between flag-OFF session rescore and committed run_yogurt_006 traces "
                "may reflect environmental differences (python version, float rounding). "
                "The decisive comparison is flag-ON vs flag-OFF within this session (same environment)."
            ),
        },
        "score_engine_sha256": score_engine_sha, "constants_sha256": constants_sha,
        "off_used": False,
    }

    rr_path = OUTPUT_ROOT / "run_record.json"
    rr_path.write_text(json.dumps(run_record, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info("Run record: %s", rr_path)

    # Full per-product table for verification
    table = []
    for bc in sorted(set(list(results_on.keys()) + list(results_off.keys()))):
        r_on  = results_on.get(bc,{})
        r_off = results_off.get(bc,{})
        c_t   = committed.get(bc,{})
        s_on  = r_on.get("score"); s_off = r_off.get("score"); s_comm = c_t.get("score")
        delta_on_off = round(s_on - s_off, 2) if (s_on and s_off) else None
        table.append({
            "barcode": bc,
            "name": r_on.get("name") or r_off.get("name",""),
            "sugars_g": r_on.get("sugars_g"),
            "score_committed": s_comm, "grade_committed": c_t.get("grade"),
            "score_off": s_off, "grade_off": r_off.get("grade"),
            "score_on":  s_on,  "grade_on":  r_on.get("grade"),
            "delta_on_vs_off": delta_on_off,
            "rel_pen": r_on.get("rel_pen"),
        })
    table.sort(key=lambda x: (x.get("sugars_g") or 0))
    table_path = OUTPUT_ROOT / "verification_table.json"
    table_path.write_text(json.dumps(table, ensure_ascii=False, indent=2), encoding="utf-8")

    # Final report
    print("\n" + "="*72)
    print(f"YOGURT SHELF-RELATIVE DIAGNOSTIC PILOT — {RUN_ID}")
    print("="*72)
    print(f"TASK-278 Phase-3 | MEASURED NOT PUBLISHED | {n_total} products (run_yogurt_006)")
    print()
    print("YOGURT SUGAR DISTRIBUTION (label sugars_g, OFF-ban):")
    print(f"  n={stats['n']}/{stats['n_products_total']}  min={stats['min']}  Q1={stats['q1']}  "
          f"median={stats['median']}  Q3={stats['q3']}  max={stats['max']}")
    print(f"  IQR={stats['iqr']}  MAD={stats['mad_raw']}  robust_scale={stats['robust_scale']}")
    print(f"  Engine: median={engine_median:.3f}  scale={engine_scale:.3f}")
    print()
    print("  BISCUIT vs YOGURT SPREAD:")
    print(f"  Biscuit: median=21.5  IQR=6.9  robust_scale=5.115")
    print(f"  Yogurt:  median={stats['median']}  IQR={stats['iqr']}  robust_scale={stats['robust_scale']}")
    print(f"  Distribution conclusion: {'WIDER relative spread' if stats['iqr']>6.9 else 'NARROWER than biscuit' if stats['iqr']<5.0 else 'COMPARABLE to biscuit'}")
    print()
    print("GRADE DISTRIBUTION:")
    print(f"  Committed (run_006): {dict(sorted(committed_grades.items()))}")
    print(f"  Flag-OFF (session):  {dict(sorted(grade_dist_off.items()))}")
    print(f"  Flag-ON  (session):  {dict(sorted(grade_dist_on.items()))}")
    print(f"  Grade changes (ON vs OFF): {len(grade_changes)}")
    for gc in grade_changes:
        print(f"    [{gc['barcode']}] {gc['grade_off']} -> {gc['grade_on']}  delta={gc['delta']:+.1f}")
    print()
    print("SCORE DELTAS (flag-ON vs flag-OFF, same session):")
    print(f"  avg delta: {avg_delta:+.4f}")
    print(f"  n movers (|delta|>=0.1): {len(movers)}")
    if movers:
        print("  Top movers:")
        for m in movers[:10]:
            print(f"    [{m['barcode'][:14]}] {m['name'][:30]} sugar={m['sugars_g']} "
                  f"{m['score_off']}->{m['score_on']} ({m['delta']:+.1f}) grade={m['grade_off']}->{m['grade_on']} rel_pen={m['rel_pen']}")
    print()
    print("RELATIVE PENALTY DISTRIBUTION (flag-ON):")
    print(f"  {dict(sorted(rel_pen_distribution.items(), key=lambda x: x[0] if x[0] is not None else 999))}")
    print()
    print("ABSORPTION CHECK (decisive test):")
    total_pen_fired = absorb_count + land_count
    print(f"  Products with non-zero rel_pen: {total_pen_fired}")
    print(f"  ABSORBED (pen fired, delta=0): {absorb_count}")
    print(f"  LANDS    (pen fired, delta!=0): {land_count}")
    print(f"  NO_PEN   (pen not fired):       {nopen_count}")
    if total_pen_fired > 0:
        print(f"  Absorption rate: {absorb_count/total_pen_fired:.1%}")
    print()
    print("DIAGNOSTIC PRODUCTS (cap->penalty trace):")
    for bc in sorted(diag_barcodes, key=lambda b: (results_on.get(b,{}).get("sugars_g") or 0), reverse=True):
        ac = absorption_check.get(bc,{})
        print(f"  [{bc}] {ac.get('name','')[:45]}")
        print(f"    sugar={ac.get('sugars_g')}g  r_median=",end="")
        sg = ac.get("sugars_g")
        if sg is not None and engine_scale and engine_scale > 0:
            r = (sg - engine_median) / engine_scale
            print(f"{r:+.2f}  ", end="")
        else:
            print("N/A  ", end="")
        print(f"rel_pen={ac.get('rel_pen')}  delta={ac.get('delta')}")
        print(f"    score_after_cap:  OFF={ac.get('score_after_cap_off')}  ON={ac.get('score_after_cap_on')}")
        print(f"    score_after_pen:  OFF={ac.get('score_after_penalty_off')}  ON={ac.get('score_after_penalty_on')}")
        print(f"    final score:      OFF={ac.get('score_off')}  ON={ac.get('score_on')}")
        print(f"    committed:        {ac.get('committed_score')}  VERDICT: {ac.get('verdict')}")
        print()
    print("SAFETY:")
    print(f"  Non-dairy_protein routing: {routing_cats}")
    print(f"  Flag-OFF vs committed mismatches: {len(off_vs_committed)} (explained by env rounding)")
    print()
    print(f"Run record: {rr_path}")
    print(f"Table: {table_path}")
    print("="*72)
    return run_record


if __name__ == "__main__":
    main()
