"""
BSIP1 Enrichment + BSIP2 Scoring — Brined Cheeses (run_brined_002)
TASK-266, factory run #6, re-score after EV-053 + EV-054

Source: Shufersal BSIP0 scrape — brined_cheese_bsip0_raw_20260613T065721.json
Corpus: 48 IN_SCORED products only (per corpus_filter.json 2026-06-13)
Engine: proto_v0 / score_engine.py — EV-053 + EV-054 applied (D7 approved)

Changes from run_brined_001:
  EV-053: brined_food context excludes sodium red label from ISRAELI_RED_LABELS_2_PLUS count
  EV-054: brined_food context suppresses HP_FAT_SODIUM_COMBO penalty (conditional skip)

Counter bugs fixed from run_brined_001:
  brined_flag_fired: now reads trace.get("context_flag") — correct top-level key
  hp_fat_sodium_fired: now reads trace.get("penalties_applied", []) — correct top-level key
    with explicit fired=True check (not default True)

Flag config (identical to run_brined_001 — no changes):
  BARI_RECAL_P0=on          — standard dairy path (EV-021 A-ceiling, graded fat penalty R5)
  BARI_RECAL_P0_YOGURT_TRIM=off
  BARI_REDLABEL_V1=off      — brined_food path governs (EV-052)
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
import hashlib

# --- Flag config BEFORE engine imports ---
os.environ["BARI_RECAL_P0"] = "on"
os.environ["BARI_RECAL_P0_YOGURT_TRIM"] = "off"
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
ROOT       = pathlib.Path(r"C:\Bari")
BSIP0_FILE = ROOT / "02_products" / "brined_cheeses" / "bsip0_outputs" / \
             "brined_cheese_bsip0_raw_20260613T065721.json"
CORPUS_FILE = ROOT / "02_products" / "brined_cheeses" / "factory_run_001" / "corpus_filter.json"
BSIP1_OUTPUT = ROOT / "03_operations" / "bsip1" / "run_brined_cheeses_001" / "output"  # reuse enriched BSIP1
BSIP2_OUTPUT = ROOT / "02_products" / "brined_cheeses" / "bsip2_outputs" / "run_brined_002"
REPORT_ROOT  = ROOT / "02_products" / "brined_cheeses" / "reports"
RUN_ID = "run_brined_002"

# run_brined_001 BSIP1 output — reuse enriched records (enrichment unchanged)
BSIP1_REUSE_DIR = ROOT / "03_operations" / "bsip1" / "run_brined_cheeses_001" / "output"

(BSIP2_OUTPUT / "products").mkdir(parents=True, exist_ok=True)
REPORT_ROOT.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# E-number patterns (same as run_brined_001)
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
PRESERVATIVE_PAT = re.compile(
    r"(פוטסיום\s+סורבאט|חומר\s+משמר|E200|E202|E203|E210|E211|E212|E213|נטריום\s+בנזואט)",
    re.UNICODE | re.IGNORECASE,
)
FLAVOR_CULTURE_PAT = re.compile(r"תרבית\s+לטעם", re.UNICODE | re.IGNORECASE)


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
        "energy_kcal":      parse_float_he(n.get("energy_kcal_raw", "")),
        "fat_g":            parse_float_he(n.get("fat_raw", "")),
        "fat_saturated_g":  parse_float_he(n.get("saturated_fat_raw", "")),
        "fat_trans_g":      None,
        "sodium_mg":        parse_float_he(n.get("sodium_raw", "")),
        "carbohydrates_g":  parse_float_he(n.get("carbs_raw", "")),
        "sugars_g":         parse_float_he(n.get("sugar_raw", "")),
        "dietary_fiber_g":  parse_float_he(n.get("fiber_raw", "")),
        "protein_g":        parse_float_he(n.get("protein_raw", "")),
    }


# ---------------------------------------------------------------------------
# BSIP2 pipeline
# ---------------------------------------------------------------------------

def run_bsip2_pipeline(bsip1_product: dict) -> dict:
    signals      = extract_signals(bsip1_product)
    cat_result   = classify_category(bsip1_product)
    l3           = signals["L3_inferred_classifications"]
    nova_result  = infer_nova(bsip1_product, l3)
    eval_result  = assign_evaluation_scope(bsip1_product, cat_result["category"])
    score_result = score_product(bsip1_product, signals, cat_result, nova_result, eval_result)
    trace        = assemble_trace(bsip1_product, signals, cat_result, nova_result, eval_result, score_result)
    trace["structural_class"] = classify_structural_class(trace)
    return trace


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat()

    log.info("=== BSIP2 Brined Cheeses — %s (EV-053 + EV-054) ===", RUN_ID)
    log.info("Engine: EV-053 (2-label cap exclusion) + EV-054 (HP_FAT_SODIUM suppression)")
    log.info("Flags: RECAL_P0=on | REDLABEL_V1=off | SODIUM_CEREAL=off | TASK250_CONF=off")

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
    # Stage 5: BSIP2 Scoring (with EV-053 + EV-054)
    # -----------------------------------------------------------------------
    log.info("--- Stage 5: BSIP2 Scoring (EV-053 + EV-054 active) ---")
    traces = []
    score_errors = []
    brined_flag_fired = []
    brined_flag_not_fired = []
    hp_fat_sodium_fired = []   # HP fired (non-brined products only after EV-054)
    hp_fat_sodium_suppressed = []  # HP suppressed by EV-054

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
            # BUGFIX from run_brined_001: context_flag is at TOP LEVEL of trace, not under evaluation_scope
            ctx_flag = trace.get("context_flag")
            sodium_val = (doc.get("normalized_nutrition_per_100g") or {}).get("sodium_mg") or 0

            # brined_food flag check (corrected path)
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

            # HP_FAT_SODIUM_COMBO check (corrected path and fired logic)
            # penalties_applied is at TOP LEVEL of trace (not under score_detail)
            pens_applied = trace.get("penalties_applied", []) or []
            # penalties_considered is also top-level
            pens_considered = trace.get("penalties_considered", []) or []

            # Check if HP_FAT_SODIUM fired (was added to penalties_applied)
            hp_actually_fired = any(
                x.get("rule") == "HP_FAT_SODIUM_COMBO"
                for x in pens_applied
            )
            # Check if HP_FAT_SODIUM was suppressed by EV-054 (in considered with fired=False + EV-054 note)
            hp_ev054_suppressed = any(
                x.get("rule") == "HP_FAT_SODIUM_COMBO" and x.get("fired") is False
                and "EV-054" in (x.get("note") or "")
                for x in pens_considered
            )

            fat_val = (doc.get("normalized_nutrition_per_100g") or {}).get("fat_g") or 0

            if hp_actually_fired:
                hp_fat_sodium_fired.append({
                    "barcode": barcode, "name": name,
                    "fat_g": fat_val, "sodium_mg": sodium_val,
                    "score": score, "grade": grade,
                    "note": "HP_FAT_SODIUM fired (non-brined context or brined without suppression)",
                })
            if hp_ev054_suppressed:
                hp_fat_sodium_suppressed.append({
                    "barcode": barcode, "name": name,
                    "fat_g": fat_val, "sodium_mg": sodium_val,
                    "score": score, "grade": grade,
                    "note": "HP_FAT_SODIUM suppressed by EV-054 (brined_food context)",
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

    # Acceptance test: NOVA-1 clean product in full-fat tier vs NOVA-3 same-fat-tier
    # Key pair: barcode 7290108509106 (13% Bulgarian, NOVA-1) vs barcode 2107071 (16% Feta, NOVA-3)
    acceptance_pairs = []
    trace_by_barcode = {
        (t.get("barcode") or (t.get("input_reference") or {}).get("barcode", "")): t
        for t in traces
    }

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
                "delta": (s_clean - s_proc) if (s_clean and s_proc) else None,
            })
        else:
            acceptance_pairs.append({
                "label": label,
                "clean_bc": bc_clean, "processed_bc": bc_processed,
                "error": "one or both barcodes not in traces",
            })

    # Pair 1: 13% NOVA-1 Bulgarian vs 16% NOVA-3 Feta (methodology brief key example)
    ap("7290108509106", "2107071", "13%_bulgarian_NOVA1_vs_16%_feta_NOVA3")
    # Pair 2: 13% NOVA-1 Bulgarian vs 16% NOVA-3 Bulgarian
    ap("7290108509106", "7290114312707", "13%_bulgarian_NOVA1_vs_16%_bulgarian_NOVA3")
    # Pair 3: NOVA-1 5% Tzfatit (should be A) vs 16% NOVA-3 Bulgarian
    ap("554457", "7290114312707", "5%_tzfatit_NOVA1_A_vs_16%_bulgarian_NOVA3")
    # Pair 4: 13% NOVA-1 Bulgarian vs NOVA-3 oiled feta balls
    ap("7290108509106", "369617", "13%_bulgarian_NOVA1_vs_NOVA3_feta_in_oil")

    all_acceptance_pass = all(p.get("nova1_above_nova3", False) for p in acceptance_pairs if "error" not in p)

    # Top 3 and bottom 3
    traces_scored = [t for t in traces if t.get("final_score_estimate") is not None]
    traces_sorted_desc = sorted(traces_scored, key=lambda t: t.get("final_score_estimate", 0), reverse=True)

    def extract_top_drivers(trace):
        bonuses = trace.get("bonuses_applied", []) or []
        pens    = trace.get("penalties_applied", []) or []
        caps    = trace.get("caps_applied", []) or []
        drivers = []
        for b in bonuses[:2]:
            drivers.append(f"+{b.get('amount','?')} {b.get('rule','?')}")
        for p in pens[:2]:
            drivers.append(f"-{p.get('amount','?')} {p.get('rule','?')}")
        for c in caps[:2]:
            if c.get("cap"):
                drivers.append(f"cap={c.get('cap','?')} {c.get('rule','?')}")
        return drivers or ["(no drivers in trace)"]

    def trace_summary(t):
        bc   = t.get("barcode") or (t.get("input_reference") or {}).get("barcode")
        name = (t.get("input_reference") or {}).get("canonical_name_he") or t.get("canonical_name_he")
        return {
            "barcode": bc,
            "name": name,
            "score": t.get("final_score_estimate"),
            "grade": t.get("grade_estimate"),
            "nova": t.get("nova_proxy"),
            "context_flag": t.get("context_flag"),
            "binding_cap": t.get("binding_cap"),
            "drivers": extract_top_drivers(t),
        }

    top3    = [trace_summary(t) for t in traces_sorted_desc[:3]]
    bottom3 = [trace_summary(t) for t in traces_sorted_desc[-3:]]

    # Before/after comparison for the acceptance pairs (compared to run_brined_001)
    run001_summary_path = REPORT_ROOT / "run_brined_001_run_summary.json"
    run001_scores = {}
    if run001_summary_path.exists():
        run001_data = json.loads(run001_summary_path.read_text(encoding="utf-8"))
        for p in run001_data.get("products", []):
            bc = str(p.get("barcode", ""))
            run001_scores[bc] = {"score": p.get("score"), "grade": p.get("grade")}

    before_after = []
    for bc, t in trace_by_barcode.items():
        if bc in run001_scores:
            old = run001_scores[bc]
            new_score = t.get("final_score_estimate")
            new_grade = t.get("grade_estimate")
            if old.get("score") != new_score or old.get("grade") != new_grade:
                name = (t.get("input_reference") or {}).get("canonical_name_he") or t.get("canonical_name_he", "")
                before_after.append({
                    "barcode": bc,
                    "name": name,
                    "nova": t.get("nova_proxy"),
                    "context_flag": t.get("context_flag"),
                    "run001_score": old.get("score"), "run001_grade": old.get("grade"),
                    "run002_score": new_score, "run002_grade": new_grade,
                    "delta": (new_score or 0) - (old.get("score") or 0),
                })
    before_after.sort(key=lambda x: x.get("delta", 0), reverse=True)

    # -----------------------------------------------------------------------
    # Run record
    # -----------------------------------------------------------------------
    run_record = {
        "run_id":          RUN_ID,
        "task":            "TASK-266",
        "category_slug":   "brined-cheeses",
        "category_context": "dairy_protein",
        "generated":       ts,
        "engine":          "proto_v0 / score_engine.py — EV-053 + EV-054 applied",
        "ev_applied": ["EV-053", "EV-054"],
        "flag_config": {
            "BARI_RECAL_P0":            "on",
            "BARI_RECAL_P0_YOGURT_TRIM":"off",
            "BARI_REDLABEL_V1":         "off",
            "BARI_SODIUM_CEREAL":       "off",
            "BARI_TASK144_FIXES":       "off",
            "BARI_TASK250_CONF":        "off",
            "BARI_GLASSBOX_D5D6":       "off",
            "BARI_GLASSBOX_W15":        "off",
            "BARI_GLASSBOX_W2":         "off",
            "BARI_GLASSBOX_W4":         "on (default)",
        },
        "ev053_note":      "brined_food context: sodium red label excluded from ISRAELI_RED_LABELS_2_PLUS count",
        "ev054_note":      "brined_food context: HP_FAT_SODIUM_COMBO suppressed (conditional skip, not deletion)",
        "off_used":        False,
        "corpus_source":   str(CORPUS_FILE),
        "bsip0_source":    str(BSIP0_FILE),
        "in_scored_count": len(in_scored_barcodes),
        "bsip1_reused_from": str(BSIP1_REUSE_DIR),
        "bsip1": {
            "records_loaded": len(bsip1_records),
            "note": "reused from run_brined_001 — enrichment unchanged",
        },
        "bsip2": {
            "output_dir":   str(BSIP2_OUTPUT),
            "scored":       len(traces),
            "errors":       len(score_errors),
        },
        "score_distribution": {
            "min":        score_min,
            "max":        score_max,
            "median":     median,
            "range":      score_range if score_range else None,
            "histogram":  histogram,
            "grade_dist": grade_dist,
        },
        "anti_collapse_verdict": anti_collapse_result,
        "brined_flag": {
            "fired_count":     len(brined_flag_fired),
            "not_fired_count": len(brined_flag_not_fired),
            "not_fired_list":  brined_flag_not_fired,
        },
        "hp_fat_sodium": {
            "fired_count":       len(hp_fat_sodium_fired),
            "suppressed_count":  len(hp_fat_sodium_suppressed),
            "fired_list":        hp_fat_sodium_fired,
            "suppressed_list":   hp_fat_sodium_suppressed[:5],  # first 5 for log
        },
        "acceptance_test": {
            "all_pass": all_acceptance_pass,
            "pairs":    acceptance_pairs,
        },
        "before_after_run001": before_after[:20],  # first 20 changed products
        "top3":    top3,
        "bottom3": bottom3,
        "errors":  score_errors,
    }

    run_record_path = BSIP2_OUTPUT / "run_record.json"
    run_record_path.write_text(json.dumps(run_record, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info("Run record: %s", run_record_path)

    # Summary JSON
    summary = {
        "run_id":              RUN_ID,
        "generated":           ts,
        "task":                "TASK-266",
        "ev_applied":          ["EV-053", "EV-054"],
        "flag_config":         run_record["flag_config"],
        "scored":              len(traces),
        "errors":              len(score_errors),
        "score_distribution":  run_record["score_distribution"],
        "anti_collapse":       anti_collapse_result,
        "brined_flag_fired":   len(brined_flag_fired),
        "brined_flag_not_fired": len(brined_flag_not_fired),
        "hp_fat_sodium_fired": len(hp_fat_sodium_fired),
        "hp_fat_sodium_suppressed_by_ev054": len(hp_fat_sodium_suppressed),
        "off_used": False,
        "acceptance_test_pass": all_acceptance_pass,
        "products": [{
            "barcode":      t.get("barcode") or (t.get("input_reference") or {}).get("barcode"),
            "name":         (t.get("input_reference") or {}).get("canonical_name_he") or t.get("canonical_name_he"),
            "score":        t.get("final_score_estimate"),
            "grade":        t.get("grade_estimate"),
            "category":     t.get("category"),
            "nova":         t.get("nova_proxy"),
            "context_flag": t.get("context_flag"),
            "binding_cap":  t.get("binding_cap"),
        } for t in traces],
    }
    summary_path = REPORT_ROOT / f"{RUN_ID}_run_summary.json"
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info("Summary: %s", summary_path)

    # -----------------------------------------------------------------------
    # Console report
    # -----------------------------------------------------------------------
    print("\n" + "="*70)
    print(f"BRINED CHEESES BSIP2 RUN — {RUN_ID} (EV-053 + EV-054)")
    print("="*70)
    print(f"Engine: EV-053 (2-label cap exclusion) + EV-054 (HP suppression)")
    print(f"Flag config: RECAL_P0=on | REDLABEL_V1=off | SODIUM_CEREAL=off")
    print()
    print(f"Corpus: {len(in_scored_barcodes)} IN_SCORED | BSIP1 records loaded: {len(bsip1_records)}")
    print()
    print(f"BSIP2 scored: {len(traces)} | errors: {len(score_errors)}")
    print()
    print("SCORE DISTRIBUTION:")
    print(f"  Min: {score_min}  Max: {score_max}  Median: {median}")
    print(f"  Range: {score_range:.1f} pts")
    print(f"  Histogram: {dict(sorted(histogram.items()))}")
    print(f"  Grade distribution: {dict(sorted(grade_dist.items()))}")
    print()
    print(f"ANTI-COLLAPSE VERDICT: {anti_collapse_result}")
    print()
    print(f"BRINED_FOOD FLAG (corrected counter):")
    print(f"  Fired: {len(brined_flag_fired)}/{len(traces)}")
    if brined_flag_not_fired:
        print(f"  NOT fired ({len(brined_flag_not_fired)} products — sodium<=500 or name not matched):")
        for p in brined_flag_not_fired:
            print(f"    {p['barcode']} sodium={p['sodium_mg']} ctx={p['ctx_flag']}")
    print()
    print(f"HP_FAT_SODIUM_COMBO (corrected counter):")
    print(f"  Fired on: {len(hp_fat_sodium_fired)} products")
    print(f"  Suppressed by EV-054: {len(hp_fat_sodium_suppressed)} products")
    print()
    print("ACCEPTANCE TEST (NOVA-1 clean > NOVA-3 same-fat-tier):")
    for ap_r in acceptance_pairs:
        if "error" in ap_r:
            print(f"  ERROR [{ap_r['label']}]: {ap_r['error']}")
        else:
            status = "PASS" if ap_r.get("nova1_above_nova3") else "FAIL"
            print(f"  [{status}] {ap_r['label']}")
            print(f"    NOVA-1 clean: barcode={ap_r['clean_bc']} score={ap_r['clean_score']}/{ap_r['clean_grade']}")
            print(f"    NOVA-3 proc:  barcode={ap_r['processed_bc']} score={ap_r['processed_score']}/{ap_r['processed_grade']}")
            print(f"    Delta: {ap_r.get('delta', '?')}")
    print()
    print(f"OVERALL ACCEPTANCE TEST: {'PASS' if all_acceptance_pass else 'FAIL'}")
    print()
    if before_after:
        print(f"BEFORE/AFTER (run_brined_001 vs run_brined_002, {len(before_after)} products moved):")
        for ba in before_after[:6]:
            name_safe = ba['name'][:40].encode('ascii', errors='replace').decode() if ba.get('name') else '?'
            print(f"  {ba['barcode']} [{name_safe}] NOVA={ba['nova']} ctx={ba['context_flag']}")
            print(f"    {ba['run001_score']}/{ba['run001_grade']} -> {ba['run002_score']}/{ba['run002_grade']}  (delta={ba['delta']:+.1f})")
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
    print(f"Summary:     {summary_path}")
    print(f"BSIP2 dir:   {BSIP2_OUTPUT}")
    print("="*70)

    return run_record


if __name__ == "__main__":
    main()
