"""
TASK-284D: Measure EV-096/097 blast radius on non-registered categories.
Categories: cakes_hard_cookies, cookies_coffee, salty_snacks.
Method: Two-pass scoring using subprocess isolation (flag-OFF then flag-ON).
Flag-OFF = current published behavior (byte-identical to committed engine).
Flag-ON  = BARI_FAT_TECH_V1=on (EV-096 seed_pen=5; EV-097 two-tier PHVO ceiling).
MEASUREMENT ONLY — no score promotion, no frontend writes, no flag flip.
"""
import os, sys, json, pathlib, hashlib, subprocess, datetime, statistics
from collections import Counter

ROOT = pathlib.Path(r"C:\Bari")
ENGINE_DIR = ROOT / "03_operations" / "bsip2" / "proto_v0" / "src"
OUT_DIR = ROOT / "tasks" / "TASK-284D-artifacts"
OUT_DIR.mkdir(parents=True, exist_ok=True)

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# ── Category configs (live ship flags matching authoritative batch runners) ──────
CATEGORIES = {
    "cakes_hard_cookies": {
        "bsip1_dir": ROOT / "03_operations" / "bsip1" / "run_cakes_001" / "output",
        "bsip1_glob": "bsip1_cakes_*.json",
        "corpus_file": ROOT / "02_products" / "cakes_hard_cookies" / "factory_run_001" / "corpus_filter.json",
        "use_corpus_filter": True,
        "flags": {  # identical to batch_run_cakes_001.py — all OFF
            "BARI_RECAL_P0": "off",
            "BARI_GRAD_SODIUM_V1": "off",
            "BARI_SODIUM_SHELF_RELATIVE_V1": "off",
            "BARI_DAIRY_PROTEIN_REWEIGHT_V1": "off",
            "BARI_REDLABEL_V1": "off",
            "BARI_SODIUM_CEREAL": "off",
        },
        "published_invariant": None,  # no frozen invariant; published non-frozen
        "expected_total": 149,        # from run_cakes_001 run_summary
    },
    "cookies_coffee": {
        "bsip1_dir": ROOT / "03_operations" / "bsip1" / "run_cookies_001" / "output",
        "bsip1_glob": "bsip1_cookies_*.json",
        "corpus_file": ROOT / "02_products" / "cookies_coffee" / "factory_run_001" / "corpus_filter.json",
        "use_corpus_filter": True,
        "flags": {  # identical to batch_run_cookies_005.py — all OFF
            "BARI_RECAL_P0": "off",
            "BARI_GRAD_SODIUM_V1": "off",
            "BARI_SODIUM_SHELF_RELATIVE_V1": "off",
            "BARI_DAIRY_PROTEIN_REWEIGHT_V1": "off",
            "BARI_REDLABEL_V1": "off",
            "BARI_SODIUM_CEREAL": "off",
        },
        "published_invariant": None,
        "expected_total": 58,
    },
    "salty_snacks": {
        "bsip1_dir": ROOT / "02_products" / "salty_snacks" / "bsip1_outputs",
        "bsip1_glob": "bsip1_snack_*.json",
        "corpus_file": None,
        "use_corpus_filter": False,
        "flags": {  # batch_run_salty_snacks_002.py: BARI_RECAL_P0=on (all others default)
            "BARI_RECAL_P0": "on",
        },
        "published_invariant": "no_A_grade_on_snack_bar",  # note: snack_bars frozen; salty_snacks not registered/frozen
        "expected_total": 54,
    },
}


def sha256_file(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_score_subprocess(cat_name: str, cat_cfg: dict, flag_value: str) -> dict:
    """
    Run the scoring pipeline for a category in a fresh subprocess with BARI_FAT_TECH_V1={flag_value}.
    Returns dict: barcode -> {score, grade, has_phvo, has_phvo_partial, has_phvo_generic,
                              has_seed_oil, category}
    """
    bsip1_dir = str(cat_cfg["bsip1_dir"])
    bsip1_glob = cat_cfg["bsip1_glob"]
    use_filter = cat_cfg["use_corpus_filter"]
    corpus_file = str(cat_cfg["corpus_file"]) if cat_cfg["corpus_file"] else ""
    flags = cat_cfg["flags"]

    flags_setup = "\n".join(
        f'os.environ[{k!r}] = {v!r}' for k, v in flags.items()
    )

    script = f"""
import os, sys, json, pathlib
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# Category live-ship flags
{flags_setup}
# FAT TECH flag (this is what we're measuring)
os.environ['BARI_FAT_TECH_V1'] = {flag_value!r}

sys.path.insert(0, {str(ENGINE_DIR)!r})
from signal_extractor import extract_signals
from router_v2 import classify_category
from nova_proxy import infer_nova
from evaluation_scope import assign_evaluation_scope
from score_engine import score_product
from trace_writer import assemble_trace
from structural_classifier import classify_structural_class

BSIP1_DIR = pathlib.Path({bsip1_dir!r})
USE_FILTER = {use_filter!r}
CORPUS_FILE = pathlib.Path({corpus_file!r}) if {corpus_file!r} else None

in_scored = None
if USE_FILTER and CORPUS_FILE and CORPUS_FILE.exists():
    corpus = json.loads(CORPUS_FILE.read_text(encoding='utf-8'))
    in_scored = {{str(p['barcode']) for p in corpus['products'] if p['decision'] == 'IN_SCORED'}}

results = {{}}
errors = []
for p in sorted(BSIP1_DIR.glob({bsip1_glob!r})):
    try:
        doc = json.loads(p.read_text(encoding='utf-8'))
        bc = str(doc.get('barcode', ''))
        if in_scored is not None and bc not in in_scored:
            continue
        signals = extract_signals(doc)
        cat = classify_category(doc)
        l3 = signals['L3_inferred_classifications']
        nova = infer_nova(doc, l3)
        ev = assign_evaluation_scope(doc, cat['category'])
        sr = score_product(doc, signals, cat, nova, ev)
        tr = assemble_trace(doc, signals, cat, nova, ev, sr)
        tr['structural_class'] = classify_structural_class(tr)
        score = tr.get('final_score_estimate')
        grade = tr.get('grade_estimate')
        has_phvo = l3.get('has_phvo', False)
        has_phvo_partial = l3.get('has_phvo_partial', False)
        has_phvo_generic = l3.get('has_phvo_generic', False)
        has_seed_oil = l3.get('has_seed_oil', False)
        if score is None: continue
        results[bc] = {{
            'score': score,
            'grade': grade,
            'has_phvo': has_phvo,
            'has_phvo_partial': has_phvo_partial,
            'has_phvo_generic': has_phvo_generic,
            'has_seed_oil': has_seed_oil,
            'category': tr.get('category'),
            'name': doc.get('canonical_name_he', ''),
        }}
    except Exception as e:
        errors.append({{'file': p.name, 'error': str(e)}})

output = {{'results': results, 'errors': errors}}
print(json.dumps(output, ensure_ascii=False))
"""

    proc = subprocess.run(
        [sys.executable, "-c", script],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        timeout=300,
    )
    if proc.returncode != 0:
        print(f"  SUBPROCESS ERROR for {cat_name} flag={flag_value}:", file=sys.stderr)
        print(proc.stderr[:2000], file=sys.stderr)

    try:
        raw = json.loads(proc.stdout.strip())
        return raw["results"], raw.get("errors", []), proc.returncode
    except Exception as e:
        print(f"  Parse error: {e}  stdout={proc.stdout[:300]}", file=sys.stderr)
        return {}, [{"parse_error": str(e)}], proc.returncode


def grade_from_score(s):
    if s is None: return "?"
    if s >= 85: return "S"
    if s >= 70: return "A"
    if s >= 55: return "B"
    if s >= 40: return "C"
    if s >= 25: return "D"
    return "E"


def compute_stdev(values):
    if len(values) < 2: return 0.0
    return round(statistics.stdev(values), 2)


def diff_category(cat_name: str, cat_cfg: dict) -> dict:
    print(f"\n{'='*60}")
    print(f"Category: {cat_name}")

    # --- FLAG-OFF (baseline = current published behavior) ---
    print(f"  Pass 1: BARI_FAT_TECH_V1=off (baseline)...")
    off_results, off_errors, off_rc = build_score_subprocess(cat_name, cat_cfg, "off")
    print(f"    Scored: {len(off_results)}  Errors: {len(off_errors)}  RC: {off_rc}")

    # --- FLAG-ON (proposed) ---
    print(f"  Pass 2: BARI_FAT_TECH_V1=on (proposed)...")
    on_results, on_errors, on_rc = build_score_subprocess(cat_name, cat_cfg, "on")
    print(f"    Scored: {len(on_results)}  Errors: {len(on_errors)}  RC: {on_rc}")

    # --- Diff ---
    all_barcodes = set(off_results.keys()) | set(on_results.keys())
    movers = []
    grade_changers = []
    ev097_movers = []   # has_phvo_generic products that changed score
    ev097_inert = []    # has_phvo_generic products that didn't change score
    ev096_movers = []   # has_seed_oil products that changed grade
    stable_table = []

    off_grades = Counter(off_results[bc]["grade"] for bc in off_results if off_results[bc].get("grade"))
    on_grades  = Counter(on_results[bc]["grade"]  for bc in on_results  if on_results[bc].get("grade"))

    for bc in sorted(all_barcodes):
        off = off_results.get(bc)
        on  = on_results.get(bc)
        if not off or not on: continue

        off_score = off["score"]
        on_score  = on["score"]
        off_grade = off["grade"]
        on_grade  = on["grade"]
        delta = round(on_score - off_score, 2)
        has_phvo = off.get("has_phvo", False)
        has_phvo_partial = off.get("has_phvo_partial", False)
        has_phvo_generic = off.get("has_phvo_generic", False)
        has_seed_oil = off.get("has_seed_oil", False)
        name = off.get("name", "")

        row = {
            "barcode": bc,
            "name": name,
            "score_off": off_score,
            "grade_off": off_grade,
            "score_on": on_score,
            "grade_on": on_grade,
            "delta": delta,
            "grade_change": off_grade != on_grade,
            "has_phvo": has_phvo,
            "has_phvo_partial": has_phvo_partial,
            "has_phvo_generic": has_phvo_generic,
            "has_seed_oil": has_seed_oil,
            "category": off.get("category", ""),
        }

        if abs(delta) > 0.001:
            movers.append(row)
        if off_grade != on_grade:
            grade_changers.append(row)

        # EV-097: any PHVO generic product (ceiling changes 40→55)
        if has_phvo_generic:
            if abs(delta) > 0.001:
                ev097_movers.append(row)
            else:
                ev097_inert.append(row)

        # EV-096: seed_oil products that cross a grade boundary
        if has_seed_oil and off_grade != on_grade:
            ev096_movers.append(row)

        stable_table.append(row)

    # Grade-movement distribution
    grade_transitions = Counter(
        f"{r['grade_off']}->{r['grade_on']}" for r in grade_changers
    )

    # Score stats
    off_scores = [off_results[bc]["score"] for bc in off_results]
    on_scores  = [on_results[bc]["score"]  for bc in on_results]
    delta_scores = [r["delta"] for r in stable_table]

    # Most common score
    off_mc = Counter(round(s, 1) for s in off_scores).most_common(1)
    on_mc  = Counter(round(s, 1) for s in on_scores).most_common(1)

    # Invariant check
    invariant_breaches = []
    invariant = cat_cfg.get("published_invariant")
    if invariant == "no_A_grade_on_snack_bar":
        # salty_snacks note: the frozen "no snack bar reaches A" invariant applies to snack_bars
        # (a different frozen corpus). salty_snacks is published-but-not-frozen, no ceiling invariant.
        # Check anyway: flag any products gaining A or above when flag-ON
        for r in stable_table:
            if r["grade_off"] not in ("A", "S") and r["grade_on"] in ("A", "S"):
                invariant_breaches.append({
                    "barcode": r["barcode"],
                    "name": r["name"],
                    "grade_off": r["grade_off"],
                    "grade_on": r["grade_on"],
                    "note": "product moves INTO A/S grade — note for invariant review",
                })

    result = {
        "category": cat_name,
        "expected_total": cat_cfg["expected_total"],
        "scored_off": len(off_results),
        "scored_on": len(on_results),
        "errors_off": off_errors[:5],
        "errors_on": on_errors[:5],
        "subprocess_rc_off": off_rc,
        "subprocess_rc_on": on_rc,
        "grade_dist_off": dict(sorted(off_grades.items())),
        "grade_dist_on":  dict(sorted(on_grades.items())),
        "score_off_min": round(min(off_scores), 1) if off_scores else None,
        "score_off_max": round(max(off_scores), 1) if off_scores else None,
        "score_off_stdev": compute_stdev(off_scores),
        "score_off_most_common": off_mc[0][0] if off_mc else None,
        "score_on_min": round(min(on_scores), 1) if on_scores else None,
        "score_on_max": round(max(on_scores), 1) if on_scores else None,
        "score_on_stdev": compute_stdev(on_scores),
        "score_on_most_common": on_mc[0][0] if on_mc else None,
        "n_movers": len(movers),
        "n_grade_changers": len(grade_changers),
        "grade_transitions": dict(sorted(grade_transitions.items())),
        "ev097_phvo_generic_total": len(ev097_movers) + len(ev097_inert),
        "ev097_movers": len(ev097_movers),
        "ev097_inert": len(ev097_inert),
        "ev097_mover_details": [
            {"barcode": r["barcode"], "name": r["name"],
             "score_off": r["score_off"], "grade_off": r["grade_off"],
             "score_on": r["score_on"], "grade_on": r["grade_on"], "delta": r["delta"]}
            for r in ev097_movers
        ],
        "ev096_grade_crossers": len(ev096_movers),
        "ev096_crosser_details": [
            {"barcode": r["barcode"], "name": r["name"],
             "score_off": r["score_off"], "grade_off": r["grade_off"],
             "score_on": r["score_on"], "grade_on": r["grade_on"], "delta": r["delta"]}
            for r in ev096_movers
        ],
        "grade_changers_table": [
            {"barcode": r["barcode"], "name": r["name"],
             "score_off": r["score_off"], "grade_off": r["grade_off"],
             "score_on": r["score_on"], "grade_on": r["grade_on"], "delta": r["delta"],
             "has_phvo": r["has_phvo"], "has_phvo_partial": r["has_phvo_partial"],
             "has_phvo_generic": r["has_phvo_generic"], "has_seed_oil": r["has_seed_oil"]}
            for r in sorted(grade_changers, key=lambda r: r["score_on"], reverse=True)
        ],
        "invariant_breaches": invariant_breaches,
        "stable_table": sorted(stable_table, key=lambda r: r["score_off"], reverse=True),
    }

    # Print summary
    print(f"\n  Results for {cat_name}:")
    print(f"    Scored off={len(off_results)} on={len(on_results)} (expected={cat_cfg['expected_total']})")
    print(f"    Grade dist OFF: {dict(sorted(off_grades.items()))}")
    print(f"    Grade dist ON:  {dict(sorted(on_grades.items()))}")
    print(f"    Movers: {len(movers)}/{len(stable_table)}  Grade changers: {len(grade_changers)}")
    print(f"    Grade transitions: {dict(sorted(grade_transitions.items()))}")
    print(f"    EV-097 (PHVO generic): {len(ev097_movers)} move / {len(ev097_inert)} inert  (total={len(ev097_movers)+len(ev097_inert)})")
    print(f"    EV-096 (seed_oil grade crossers): {len(ev096_movers)}")
    print(f"    Invariant breaches: {len(invariant_breaches)}")

    if grade_changers:
        print(f"\n  Grade changer table:")
        print(f"    {'Barcode':<16} {'Off':>5} {'On':>5} {'Δ':>6} {'PHVO':>5} {'Seed':>5}  Name")
        for r in sorted(grade_changers, key=lambda r: r["score_on"], reverse=True):
            phvo = "Y" if r["has_phvo"] else "n"
            seed = "Y" if r["has_seed_oil"] else "n"
            print(f"    {r['barcode']:<16} {r['grade_off']}->{r['grade_on']}  {r['delta']:>+6.1f}  {phvo:>5}  {seed:>5}  {r['name'][:45]}")

    if ev097_movers:
        print(f"\n  EV-097 movers (PHVO generic, score changed):")
        for r in ev097_movers:
            print(f"    {r['barcode']:<16} {r['grade_off']}->{r['grade_on']}  {r['delta']:>+6.1f}  {r['name'][:50]}")

    return result


def main():
    print("=== TASK-284D: EV-096/097 Blast Radius Measurement (non-registered categories) ===")
    print(f"Date: {datetime.date.today().isoformat()}")
    print(f"Engine dir: {ENGINE_DIR}")

    # Verify engine SHA256 (must match committed baseline)
    engine_sha = sha256_file(ENGINE_DIR / "score_engine.py")
    signal_sha = sha256_file(ENGINE_DIR / "signal_extractor.py")
    print(f"\nscore_engine.py    SHA256: {engine_sha}")
    print(f"signal_extractor.py SHA256: {signal_sha}")

    all_results = {}
    for cat_name, cat_cfg in CATEGORIES.items():
        all_results[cat_name] = diff_category(cat_name, cat_cfg)

    # ── Aggregate summary ──────────────────────────────────────────────────────
    print(f"\n\n{'='*70}")
    print("AGGREGATE SUMMARY — EV-096/097 BLAST RADIUS (NON-REGISTERED CATEGORIES)")
    print(f"{'='*70}")

    total_scored = sum(r["scored_off"] for r in all_results.values())
    total_movers = sum(r["n_movers"] for r in all_results.values())
    total_grade_changers = sum(r["n_grade_changers"] for r in all_results.values())
    total_ev097_phvo_generic = sum(r["ev097_phvo_generic_total"] for r in all_results.values())
    total_ev097_movers = sum(r["ev097_movers"] for r in all_results.values())
    total_ev097_inert = sum(r["ev097_inert"] for r in all_results.values())
    total_ev096_crossers = sum(r["ev096_grade_crossers"] for r in all_results.values())
    total_invariant_breaches = sum(len(r["invariant_breaches"]) for r in all_results.values())

    print(f"\nTotal scored (OFF pass): {total_scored} products across 3 categories")
    print(f"Total movers (|Δ|>0):   {total_movers}/{total_scored}")
    print(f"Total grade changers:   {total_grade_changers}/{total_scored}")

    print(f"\nEV-097 (PHVO generic ceiling 40→55):")
    print(f"  PHVO-generic products in these 3 categories: {total_ev097_phvo_generic}")
    print(f"  Of those that MOVE score: {total_ev097_movers}")
    print(f"  Of those INERT (sat-fat holds ≤40):          {total_ev097_inert}")

    print(f"\nEV-096 (seed_pen 10→5 grade crossers): {total_ev096_crossers}")
    print(f"Invariant breaches (potential): {total_invariant_breaches}")

    print(f"\nPer-category grade-change details:")
    for cat_name, r in all_results.items():
        print(f"  {cat_name}:")
        print(f"    Scored: {r['scored_off']}  Movers: {r['n_movers']}  Grade changes: {r['n_grade_changers']}")
        print(f"    Grade dist OFF: {r['grade_dist_off']}")
        print(f"    Grade dist ON:  {r['grade_dist_on']}")
        print(f"    Score stdev OFF: {r['score_off_stdev']}  ON: {r['score_on_stdev']}")
        print(f"    Transitions: {r['grade_transitions']}")
        if r["grade_changers_table"]:
            for row in r["grade_changers_table"]:
                print(f"      {row['barcode']:<16}  {row['score_off']:>5}/{row['grade_off']} → {row['score_on']:>5}/{row['grade_on']}  Δ={row['delta']:>+.1f}  phvo={row['has_phvo']}  seed={row['has_seed_oil']}  {row['name'][:45]}")

    # ── Write artifact ─────────────────────────────────────────────────────────
    artifact = {
        "task": "TASK-284D",
        "date": datetime.date.today().isoformat(),
        "measurement_only": True,
        "flag_off_meaning": "BARI_FAT_TECH_V1=off = current published/committed behavior",
        "flag_on_meaning": "BARI_FAT_TECH_V1=on = EV-096 (seed_pen=5) + EV-097 (two-tier PHVO ceiling)",
        "engine_sha256": engine_sha,
        "signal_extractor_sha256": signal_sha,
        "aggregate": {
            "total_scored_off": total_scored,
            "total_movers": total_movers,
            "total_grade_changers": total_grade_changers,
            "ev097_phvo_generic_total": total_ev097_phvo_generic,
            "ev097_movers": total_ev097_movers,
            "ev097_inert": total_ev097_inert,
            "ev096_grade_crossers": total_ev096_crossers,
            "invariant_breaches_potential": total_invariant_breaches,
        },
        "categories": all_results,
    }

    # Remove stable_table from the saved artifact (too large; grade_changers_table keeps key info)
    for cat_data in artifact["categories"].values():
        cat_data.pop("stable_table", None)

    out_path = OUT_DIR / "blast_radius_284d.json"
    out_path.write_text(json.dumps(artifact, ensure_ascii=False, indent=2), encoding="utf-8")
    sha = sha256_file(out_path)
    print(f"\nArtifact: {out_path}")
    print(f"SHA256:   {sha}")

    return artifact, out_path, sha


if __name__ == "__main__":
    main()
