"""
BSIP1 Enrichment + BSIP2 Scoring — Brined Cheeses (run_brined_003)
TASK-267, graduated-sodium implementation: EV-055 + routing fix (TASK-267)

Source: Shufersal BSIP0 scrape — brined_cheese_bsip0_raw_20260613T065721.json
Corpus: 48 IN_SCORED products only (per corpus_filter.json 2026-06-13)
Engine: proto_v0 / score_engine.py — EV-053 + EV-054 + EV-055 applied (D7 approved)

Changes from run_brined_002:
  EV-055: BARI_GRAD_SODIUM_V1=on — graduated sodium replaces hard 700mg cliff for
          brined_food context within dairy_protein category. The 72-pin is BROKEN:
          products formerly capped at 72 now differentiate by NOVA+fat tiers.
  Routing fix: 19/48 previously misrouted products (default/cracker) now route to
               dairy_protein via hard anchors (פטה, בולגרית, חלומי) + bsip_cheese_subpool
               category prior in router_v2.py (TASK-267 Decision 4).

Flag config:
  BARI_RECAL_P0=on          — standard dairy path
  BARI_RECAL_P0_YOGURT_TRIM=off
  BARI_GRAD_SODIUM_V1=on    — EV-055 graduated sodium (brined_food scope only)
  BARI_REDLABEL_V1=off      — NOT activated (bundled flag; separate D7 required)
  BARI_SODIUM_CEREAL=off
  BARI_TASK144_FIXES=off
  BARI_TASK250_CONF=off
  BARI_GLASSBOX_W4=on

OFF ban: absolute. off_used=0. No field filled from any source other than direct BSIP0 scrape.
"""
import os
import sys
import json
import re
import pathlib
import logging
import datetime

# --- Flag config BEFORE engine imports ---
os.environ["BARI_RECAL_P0"] = "on"
os.environ["BARI_RECAL_P0_YOGURT_TRIM"] = "off"
os.environ["BARI_GRAD_SODIUM_V1"] = "on"   # EV-055
os.environ["BARI_REDLABEL_V1"] = "off"
os.environ["BARI_SODIUM_CEREAL"] = "off"
os.environ["BARI_TASK144_FIXES"] = "off"
os.environ["BARI_TASK250_CONF"] = "off"
os.environ["BARI_GLASSBOX_D5D6"] = "off"
os.environ["BARI_GLASSBOX_W15"] = "off"
os.environ["BARI_GLASSBOX_W2"] = "off"
# BARI_GLASSBOX_W4 defaults to on (module-level default)

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

# --- Paths ---
ROOT        = pathlib.Path(r"C:\Bari")
BSIP0_FILE  = ROOT / "02_products" / "brined_cheeses" / "bsip0_outputs" / \
              "brined_cheese_bsip0_raw_20260613T065721.json"
CORPUS_FILE = ROOT / "02_products" / "brined_cheeses" / "factory_run_001" / "corpus_filter.json"
BSIP1_REUSE_DIR = ROOT / "03_operations" / "bsip1" / "run_brined_cheeses_001" / "output"
BSIP2_OUTPUT    = ROOT / "02_products" / "brined_cheeses" / "bsip2_outputs" / "run_brined_003"
REPORT_ROOT     = ROOT / "02_products" / "brined_cheeses" / "reports"
RUN_ID = "run_brined_003"

(BSIP2_OUTPUT / "products").mkdir(parents=True, exist_ok=True)
REPORT_ROOT.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# E-number patterns (same as run_brined_002)
# ---------------------------------------------------------------------------
NOVA4_PAT = re.compile(
    r"(E339|E340|E341|E-339|E-340|E-341|פוספט|שמן דקלים|שמן צמחי מוקשה)",
    re.UNICODE,
)
NOVA3_PAT = re.compile(
    r"(עמילן מתוקן|E\d{3,4}[a-z]?|חומר\s+(מייצב|ייצוב|מונע|עיכוב)|קרגינן|"
    r"חומצה ציטרית|גומי זרעי חרובים|אגר|קסנטן|גואר|לוקוסט|כרגינן)",
    re.UNICODE | re.IGNORECASE,
)
E_PAT = re.compile(r"E[-\s]?\d{3,4}[a-z]?", re.IGNORECASE)
CULTURE_PAT = re.compile(
    r"(תרביות\s+חיידקים|תרבית\s+חיידקים|תרביות\s+פעילות|cultures|"
    r"חיידקי\s+מחמצת|חיידקי\s+גבינה|מחמצת|rennet|קואגולנט|קורנית)",
    re.UNICODE | re.IGNORECASE,
)


def parse_float_he(raw: str):
    if not raw:
        return None
    m = re.search(r"פחות\s+מ\s+([\d.]+)", raw)
    if m:
        return float(m.group(1)) / 2
    cleaned = raw.replace(",", "").strip()
    m = re.search(r"([\d.]+)", cleaned)
    if m:
        return float(m.group(1))
    return None


def normalize_nutrition(n: dict) -> dict:
    return {
        "energy_kcal":     parse_float_he(n.get("energy_kcal_raw", "")),
        "fat_g":           parse_float_he(n.get("fat_raw", "")),
        "fat_saturated_g": parse_float_he(n.get("saturated_fat_raw", "")),
        "fat_trans_g":     None,
        "sodium_mg":       parse_float_he(n.get("sodium_raw", "")),
        "carbohydrates_g": parse_float_he(n.get("carbs_raw", "")),
        "sugars_g":        parse_float_he(n.get("sugar_raw", "")),
        "dietary_fiber_g": parse_float_he(n.get("fiber_raw", "")),
        "protein_g":       parse_float_he(n.get("protein_raw", "")),
    }


def run_bsip2_pipeline(bsip1_product: dict) -> dict:
    signals     = extract_signals(bsip1_product)
    cat_result  = classify_category(bsip1_product)
    l3          = signals["L3_inferred_classifications"]
    nova_result = infer_nova(bsip1_product, l3)
    eval_result = assign_evaluation_scope(bsip1_product, cat_result["category"])
    score_result = score_product(bsip1_product, signals, cat_result, nova_result, eval_result)
    trace       = assemble_trace(bsip1_product, signals, cat_result, nova_result, eval_result, score_result)
    trace["structural_class"] = classify_structural_class(trace)
    return trace


def main():
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat()

    log.info("=== BSIP2 Brined Cheeses — %s (EV-055 + routing fix) ===", RUN_ID)
    log.info("Flags: RECAL_P0=on | GRAD_SODIUM_V1=on | REDLABEL_V1=off | SODIUM_CEREAL=off")

    # Load corpus filter — build IN_SCORED barcode set
    corpus = json.loads(CORPUS_FILE.read_text(encoding="utf-8"))
    in_scored_barcodes = {
        str(p["barcode"]) for p in corpus["products"]
        if p["decision"] == "IN_SCORED"
    }
    log.info("IN_SCORED barcodes: %d", len(in_scored_barcodes))

    # Load BSIP1 records from run_brined_001 (enrichment unchanged)
    bsip1_records = []
    for p in sorted(BSIP1_REUSE_DIR.glob("bsip1_brinedcheese_*.json")):
        try:
            doc = json.loads(p.read_text(encoding="utf-8"))
            barcode = str(doc.get("barcode", ""))
            if barcode in in_scored_barcodes:
                bsip1_records.append(doc)
        except Exception as e:
            log.error("Load error %s: %s", p.name, e)

    log.info("BSIP1 records loaded: %d (reused from run_brined_001)", len(bsip1_records))

    if len(bsip1_records) != 48:
        log.warning("Expected 48 BSIP1 records, got %d", len(bsip1_records))

    # -----------------------------------------------------------------------
    # Stage 5: BSIP2 Scoring (with EV-053 + EV-054 + EV-055)
    # -----------------------------------------------------------------------
    log.info("--- Stage 5: BSIP2 Scoring (EV-053 + EV-054 + EV-055 active) ---")
    traces = []
    score_errors = []
    brined_flag_fired = []
    brined_flag_not_fired = []
    sodium_grad_fired = []   # products where graduated sodium fired
    routing_cats = {}        # category distribution

    for doc in bsip1_records:
        barcode = doc.get("barcode", "")
        name    = doc.get("canonical_name_he", "")
        try:
            trace = run_bsip2_pipeline(doc)
            write_trace(trace, BSIP2_OUTPUT)
            traces.append(trace)

            score    = trace.get("final_score_estimate")
            grade    = trace.get("grade_estimate")
            cat      = trace.get("category")
            nova     = trace.get("nova_proxy")
            ctx_flag = trace.get("context_flag")
            sodium_val = (doc.get("normalized_nutrition_per_100g") or {}).get("sodium_mg") or 0

            # Track routing category
            routing_cats[cat] = routing_cats.get(cat, 0) + 1

            # brined_food flag check
            if ctx_flag == "brined_food":
                brined_flag_fired.append({
                    "barcode": barcode, "name": name,
                    "sodium_mg": sodium_val, "score": score, "grade": grade,
                })
            else:
                brined_flag_not_fired.append({
                    "barcode": barcode, "name": name,
                    "sodium_mg": sodium_val,
                    "ctx_flag": ctx_flag,
                    "score": score, "grade": grade,
                    "note": "sodium<=500 or name not matched",
                })

            # graduated sodium fired check
            pens_applied = trace.get("penalties_applied", []) or []
            grad_fired = any(x.get("rule") == "SODIUM_LOAD_GENERAL_GRAD" for x in pens_applied)
            if grad_fired:
                pen_entry = next((x for x in pens_applied if x.get("rule") == "SODIUM_LOAD_GENERAL_GRAD"), {})
                sodium_grad_fired.append({
                    "barcode": barcode, "name": name,
                    "sodium_mg": sodium_val, "score": score, "grade": grade,
                    "penalty": pen_entry.get("amount"),
                    "note": pen_entry.get("note", ""),
                })

            log.info("  BSIP2 %-40s score=%-5s grade=%-2s cat=%-14s nova=%s ctx=%s",
                     name[:38], score, grade, cat, nova, ctx_flag or "standard")
        except Exception as e:
            log.error("  BSIP2 ERROR %s (%s): %s", barcode, name, e)
            import traceback; traceback.print_exc()
            score_errors.append({"barcode": barcode, "name": name, "error": str(e)})

    # -----------------------------------------------------------------------
    # Score distribution analysis
    # -----------------------------------------------------------------------
    all_scores = [t.get("final_score_estimate") for t in traces if t.get("final_score_estimate") is not None]
    grade_dist = {}
    for t in traces:
        g = t.get("grade_estimate", "?")
        grade_dist[g] = grade_dist.get(g, 0) + 1

    if all_scores:
        scores_sorted = sorted(all_scores)
        n = len(scores_sorted)
        median = scores_sorted[n // 2] if n % 2 else (scores_sorted[n//2 - 1] + scores_sorted[n//2]) / 2
        score_min = min(all_scores)
        score_max = max(all_scores)
    else:
        median = score_min = score_max = None

    histogram = {}
    for s in all_scores:
        band = f"{int(s // 10) * 10}-{int(s // 10) * 10 + 9}"
        histogram[band] = histogram.get(band, 0) + 1

    score_range = (score_max - score_min) if (score_max is not None and score_min is not None) else 0
    num_grade_bands = len([g for g in grade_dist if g not in ("?", None)])
    if score_range >= 20 and num_grade_bands >= 2:
        anti_collapse_result = "SPREAD_HONEST: range={:.1f} pts ({:.1f}–{:.1f}), {} grade bands".format(
            score_range, score_min, score_max, num_grade_bands)
    elif score_range < 10:
        anti_collapse_result = "CLUSTERED: range={:.1f} pts ({:.1f}–{:.1f}), {} grade bands".format(
            score_range, score_min or 0, score_max or 0, num_grade_bands)
    else:
        anti_collapse_result = "MODERATE_SPREAD: range={:.1f} pts ({:.1f}–{:.1f}), {} grade bands".format(
            score_range, score_min or 0, score_max or 0, num_grade_bands)

    # Check for 72-pin (the acceptance test)
    pin_72_count = sum(1 for s in all_scores if s == 72.0)
    pin_broken = pin_72_count < 10  # Previously 42/48 were pinned at 72; if <10 remain, pin is broken

    # Before/after vs run_brined_002 (the 72-pin baseline)
    run002_dir = ROOT / "02_products" / "brined_cheeses" / "bsip2_outputs" / "run_brined_002"
    trace_by_barcode = {
        (t.get("barcode") or (t.get("input_reference") or {}).get("barcode", "")): t
        for t in traces
    }
    before_after = []
    for bc, trace in trace_by_barcode.items():
        run002_trace_path = run002_dir / "products" / f"bsip1_brinedcheese_{bc}" / "bsip2_trace.json"
        if run002_trace_path.exists():
            old = json.loads(run002_trace_path.read_text(encoding="utf-8"))
            old_score = old.get("final_score_estimate")
            old_grade = old.get("grade_estimate")
            new_score = trace.get("final_score_estimate")
            new_grade = trace.get("grade_estimate")
            if old_score != new_score or old_grade != new_grade:
                nova_val = trace.get("nova_proxy")
                fat_val = (doc.get("normalized_nutrition_per_100g") or {}).get("fat_g") if False else None
                # Get from bsip1
                bsip1_f = BSIP1_REUSE_DIR / f"bsip1_brinedcheese_{bc}.json"
                fat_val = None
                sodium_val = None
                if bsip1_f.exists():
                    b1 = json.loads(bsip1_f.read_text(encoding="utf-8"))
                    fat_val = (b1.get("normalized_nutrition_per_100g") or {}).get("fat_g")
                    sodium_val = (b1.get("normalized_nutrition_per_100g") or {}).get("sodium_mg")
                name_val = (trace.get("input_reference") or {}).get("product_name_he") or trace.get("canonical_name_he", "")
                before_after.append({
                    "barcode": bc,
                    "name": name_val,
                    "nova": nova_val,
                    "fat_g": fat_val,
                    "sodium_mg": sodium_val,
                    "context_flag": trace.get("context_flag"),
                    "run002_score": old_score, "run002_grade": old_grade,
                    "run003_score": new_score, "run003_grade": new_grade,
                    "delta": (new_score or 0) - (old_score or 0),
                })
    before_after.sort(key=lambda x: x.get("delta", 0), reverse=True)

    # Acceptance test: NOVA-1 low-fat products score higher than NOVA-3 high-fat products
    # Key pairs for pin-break verification
    acceptance_pairs = []

    def ap(bc_clean, bc_processed, label):
        t_clean = trace_by_barcode.get(bc_clean)
        t_proc  = trace_by_barcode.get(bc_processed)
        if t_clean and t_proc:
            s_clean = t_clean.get("final_score_estimate")
            s_proc  = t_proc.get("final_score_estimate")
            g_clean = t_clean.get("grade_estimate")
            g_proc  = t_proc.get("grade_estimate")
            nova_clean = t_clean.get("nova_proxy")
            nova_proc  = t_proc.get("nova_proxy")
            passes = (s_clean is not None and s_proc is not None and s_clean > s_proc)
            acceptance_pairs.append({
                "label": label,
                "clean_bc": bc_clean, "clean_score": s_clean, "clean_grade": g_clean, "clean_nova": nova_clean,
                "processed_bc": bc_processed, "processed_score": s_proc, "processed_grade": g_proc, "processed_nova": nova_proc,
                "nova1_above_nova3": passes,
                "delta": round((s_clean - s_proc), 2) if (s_clean and s_proc) else None,
            })
        else:
            acceptance_pairs.append({"label": label, "error": "barcode not found"})

    # Pair 1: NOVA-1 5% Bulgarian vs NOVA-2 16% Bulgarian (was both pinned at 72 in run_002)
    ap("2107798", "7290114312707", "NOVA1_5pct_bulgarian_vs_NOVA3_16pct_bulgarian_pin_break")
    # Pair 2: NOVA-1 low-fat vs NOVA-3 (feta in oil)
    ap("7290108509106", "369617", "NOVA1_13pct_bulgarian_vs_NOVA3_feta_oil")
    # Pair 3: 5% vs 24% fat same NOVA tier (sodium effect)
    ap("2107798", "2385455", "NOVA3_5pct_bulgarian_vs_NOVA3_24pct_bulgarian_sodium_effect")
    # Pair 4: Low sodium NOVA-1 vs high sodium NOVA-1 (graduated sodium test)
    ap("7290108509106", "7290017065236", "NOVA1_13pct_low_sodium_vs_NOVA1_24pct_high_sodium")

    all_acceptance_pass = all(p.get("nova1_above_nova3", False) for p in acceptance_pairs if "error" not in p)

    # Top 3 and bottom 3
    traces_scored = [t for t in traces if t.get("final_score_estimate") is not None]
    traces_sorted_desc = sorted(traces_scored, key=lambda t: t.get("final_score_estimate", 0), reverse=True)

    def extract_drivers(t):
        pens = t.get("penalties_applied", []) or []
        caps = t.get("caps_applied", []) or []
        drivers = []
        for p in pens[:2]:
            drivers.append(f"-{p.get('amount','?')} {p.get('rule','?')}")
        for c in caps[:2]:
            if c.get("cap"):
                drivers.append(f"cap={c.get('cap','?')} {c.get('rule','?')}")
        return drivers or ["(no drivers)"]

    def trace_summary(t):
        bc = t.get("barcode") or (t.get("input_reference") or {}).get("barcode")
        name = (t.get("input_reference") or {}).get("product_name_he") or t.get("canonical_name_he")
        return {
            "barcode": bc, "name": name,
            "score": t.get("final_score_estimate"),
            "grade": t.get("grade_estimate"),
            "nova": t.get("nova_proxy"),
            "context_flag": t.get("context_flag"),
            "binding_cap": t.get("binding_cap"),
            "drivers": extract_drivers(t),
        }

    top3    = [trace_summary(t) for t in traces_sorted_desc[:3]]
    bottom3 = [trace_summary(t) for t in traces_sorted_desc[-3:]]

    # -----------------------------------------------------------------------
    # Run record
    # -----------------------------------------------------------------------
    run_record = {
        "run_id":           RUN_ID,
        "task":             "TASK-267",
        "category_slug":    "brined-cheeses",
        "category_context": "dairy_protein",
        "generated":        ts,
        "engine":           "proto_v0 / score_engine.py — EV-053 + EV-054 + EV-055 applied",
        "ev_applied":       ["EV-053", "EV-054", "EV-055"],
        "flag_config": {
            "BARI_RECAL_P0":             "on",
            "BARI_RECAL_P0_YOGURT_TRIM": "off",
            "BARI_GRAD_SODIUM_V1":       "on",
            "BARI_REDLABEL_V1":          "off",
            "BARI_SODIUM_CEREAL":        "off",
            "BARI_TASK144_FIXES":        "off",
            "BARI_TASK250_CONF":         "off",
            "BARI_GLASSBOX_D5D6":        "off",
            "BARI_GLASSBOX_W15":         "off",
            "BARI_GLASSBOX_W2":          "off",
            "BARI_GLASSBOX_W4":          "on (default)",
        },
        "ev055_note":       "BARI_GRAD_SODIUM_V1=on: graduated SODIUM_GENERAL_BANDS replaces HIGH_SODIUM_700MG_PLUS cliff for brined_food context within dairy_protein",
        "routing_fix_note": "19 previously misrouted products (default/cracker) now route to dairy_protein via hard anchors (פטה, בולגרית, חלומי) + bsip_cheese_subpool category prior",
        "off_used":         False,
        "corpus_source":    str(CORPUS_FILE),
        "bsip0_source":     str(BSIP0_FILE),
        "in_scored_count":  len(in_scored_barcodes),
        "bsip1_reused_from": str(BSIP1_REUSE_DIR),
        "bsip1": {
            "records_loaded": len(bsip1_records),
            "note": "reused from run_brined_001 — enrichment unchanged",
        },
        "bsip2": {
            "output_dir": str(BSIP2_OUTPUT),
            "scored":     len(traces),
            "errors":     len(score_errors),
        },
        "score_distribution": {
            "min":       score_min,
            "max":       score_max,
            "median":    median,
            "range":     score_range if score_range else None,
            "histogram": histogram,
            "grade_dist": grade_dist,
        },
        "routing_distribution":  routing_cats,
        "anti_collapse_verdict": anti_collapse_result,
        "pin_72_count":          pin_72_count,
        "pin_broken":            pin_broken,
        "brined_flag": {
            "fired_count":     len(brined_flag_fired),
            "not_fired_count": len(brined_flag_not_fired),
            "not_fired_list":  brined_flag_not_fired,
        },
        "sodium_grad_fired": {
            "count":   len(sodium_grad_fired),
            "list":    sodium_grad_fired[:10],
        },
        "acceptance_test": {
            "all_pass": all_acceptance_pass,
            "pairs":    acceptance_pairs,
        },
        "before_after_run002": before_after[:20],
        "top3":    top3,
        "bottom3": bottom3,
        "errors":  score_errors,
    }

    run_record_path = BSIP2_OUTPUT / "run_record.json"
    run_record_path.write_text(json.dumps(run_record, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info("Run record: %s", run_record_path)

    # -----------------------------------------------------------------------
    # Console report
    # -----------------------------------------------------------------------
    print("\n" + "="*70)
    print(f"BRINED CHEESES BSIP2 RUN — {RUN_ID} (EV-055 + routing fix)")
    print("="*70)
    print(f"Flag config: RECAL_P0=on | GRAD_SODIUM_V1=on | REDLABEL_V1=off")
    print()
    print(f"Corpus: {len(in_scored_barcodes)} IN_SCORED | BSIP1 records: {len(bsip1_records)}")
    print(f"BSIP2 scored: {len(traces)} | errors: {len(score_errors)}")
    print()
    print("ROUTING DISTRIBUTION:")
    for cat, cnt in sorted(routing_cats.items()):
        print(f"  {cat}: {cnt}")
    print()
    print("SCORE DISTRIBUTION:")
    print(f"  Min: {score_min}  Max: {score_max}  Median: {median}")
    print(f"  Range: {score_range:.1f} pts")
    print(f"  Histogram: {dict(sorted(histogram.items()))}")
    print(f"  Grade distribution: {dict(sorted(grade_dist.items()))}")
    print()
    print(f"ANTI-COLLAPSE VERDICT: {anti_collapse_result}")
    print()
    print(f"72-PIN STATUS: pin_72_count={pin_72_count} (was 42/48 in run_002)")
    print(f"PIN BROKEN: {pin_broken}")
    print()
    print(f"GRADUATED SODIUM FIRED: {len(sodium_grad_fired)} products")
    for s in sodium_grad_fired[:5]:
        print(f"  {s['barcode']} sodium={s['sodium_mg']}mg  {s['score']}/{s['grade']}  pen={s['penalty']}")
    print()
    print("ACCEPTANCE TEST (pin-break + NOVA differentiation):")
    for ap_r in acceptance_pairs:
        if "error" in ap_r:
            print(f"  ERROR [{ap_r['label']}]: {ap_r['error']}")
        else:
            status = "PASS" if ap_r.get("nova1_above_nova3") else "FAIL"
            print(f"  [{status}] {ap_r['label']}")
            print(f"    clean: bc={ap_r['clean_bc']} score={ap_r['clean_score']}/{ap_r['clean_grade']} NOVA={ap_r['clean_nova']}")
            print(f"    proc:  bc={ap_r['processed_bc']} score={ap_r['processed_score']}/{ap_r['processed_grade']} NOVA={ap_r['processed_nova']}")
            print(f"    Delta: {ap_r.get('delta', '?')}")
    print()
    print(f"OVERALL ACCEPTANCE TEST: {'PASS' if all_acceptance_pass else 'FAIL'}")
    print()
    if before_after:
        print(f"BEFORE/AFTER (run_002 vs run_003, {len(before_after)} products moved):")
        for ba in before_after[:8]:
            name_safe = (ba.get('name') or '?')[:40].encode('ascii', errors='replace').decode()
            print(f"  {ba['barcode']} [{name_safe}] NOVA={ba['nova']} fat={ba.get('fat_g')}% sodium={ba.get('sodium_mg')}mg")
            print(f"    {ba['run002_score']}/{ba['run002_grade']} -> {ba['run003_score']}/{ba['run003_grade']}  (delta={ba.get('delta', '?'):+.1f})" if isinstance(ba.get('delta'), (int, float)) else f"    {ba['run002_score']}/{ba['run002_grade']} -> {ba['run003_score']}/{ba['run003_grade']}")
    print()
    print("TOP 3:")
    for i, p in enumerate(top3, 1):
        name_safe = (p['name'] or '?')[:50].encode('ascii', errors='replace').decode()
        print(f"  {i}. [{p['score']}/{p['grade']}] {name_safe}")
        print(f"     NOVA={p['nova']} ctx={p['context_flag']} cap={p['binding_cap']}")
        print(f"     Drivers: {'; '.join(p['drivers'][:3])}")
    print()
    print("BOTTOM 3:")
    for i, p in enumerate(bottom3, 1):
        name_safe = (p['name'] or '?')[:50].encode('ascii', errors='replace').decode()
        print(f"  {i}. [{p['score']}/{p['grade']}] {name_safe}")
        print(f"     NOVA={p['nova']} ctx={p['context_flag']} cap={p['binding_cap']}")
        print(f"     Drivers: {'; '.join(p['drivers'][:3])}")
    print()
    print(f"Run record:  {run_record_path}")
    print(f"BSIP2 dir:   {BSIP2_OUTPUT}")
    print("="*70)

    return run_record


if __name__ == "__main__":
    main()
