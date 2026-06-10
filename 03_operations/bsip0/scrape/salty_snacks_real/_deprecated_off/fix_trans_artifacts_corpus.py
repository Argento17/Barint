"""
TASK-234 — Systematize the 0.5g trans-declaration guard CORPUS-WIDE + correct
implausible per-100g basis errors (kcal / fiber). Re-score affected products on the
UNCHANGED engine (engine-baseline-2026-06-04 + TASK-216, BARI_RECAL_P0=on).

NO scoring-engine change. This corrects bad INPUT DATA only, exactly as TASK-231 (beet
cracker) and TASK-229 (Apropo caramel) did for the two products that tripped the veto.

──────────────────────────────────────────────────────────────────────────────
RT-2 — the 0.5g serving-declaration trans artifact is corpus-wide
──────────────────────────────────────────────────────────────────────────────
OFF reports `trans-fat_serving = 0.5 g` as the Israeli "<1 g" mandatory THRESHOLD
DECLARATION (not a measured value). Wherever a product's serving size != 100 g, OFF
divides 0.5 by the serving fraction, yielding a bogus per-100g trans (0.625 / 0.6 / 0.4 /
1.25 / 2.33 ...). Products at exactly 0.5/100g are already neutralized by the engine's
`threshold_declaration` guard (signal_extractor L1104), but the scaled values land at
0.4 / 0.6 / 0.625 / 1.25 and are penalized (present -10 / high_concern -20) or vetoed as
if measured.

TASK-238 NOTE: This script's trans-fat corrections were sourced from an Open Food Facts
re-probe (off_reprobe_task234.json). OFF is now BANNED — these corrections are OFF-derived
and must be treated as contamination, not as a valid input. Script DISABLED below.

Robust detector (authoritative OFF re-probe in off_reprobe_task234.json):
  serving-level trans is a sub-1g "<1g" declaration token (trans_serving <= 0.5) OR the
  per-100g value back-computes to such a declaration via the serving fraction (every other
  macro scales identically), AND no PHVO / hydrogenated-oil marker is present in the
  ingredient list (or ingredients absent). PHVO is the sole industrial trans source; its
  absence is the necessary condition. Confirmed: NONE of the corrected products carry a
  PHVO marker (the one product that does — Click nougat 7290116537375 — has trans=None and
  is NOT in this set).

Action: neutralize fat_trans_g -> 0.0 at BSIP1 with a data_corrections entry, re-score.

──────────────────────────────────────────────────────────────────────────────
MEDIUM — implausible per-100g basis errors
──────────────────────────────────────────────────────────────────────────────
* Click cornflakes (7290112494313): fiber 38 g/100g is mathematically impossible —
  fiber(38) + sugars(29.6) = 67.6 > total carbohydrates(66.15); fiber is a subset of carbs.
  Single-field error; rest of panel (483 kcal) is plausible. -> omit fiber (set None), keep.
* Three "chips" (7290018198254 / 7290018198148 / 7290004943738) at 128/139/145 kcal/100g:
  Atwater(macros) reproduces the stated kcal, so the WHOLE panel is internally consistent
  but on a wrong (per-serving) basis — a real fried/baked potato crisp is ~450-540 kcal/100g.
  OFF carries no serving_size to recover the scale factor -> per-100g basis UNRECOVERABLE.
  Honest action: drop from the scored shelf (handled in 03_build_frontend_v4.py
  BASIS_ERROR_EXCLUDE; NOT a single-field omission because every macro is on the wrong basis).
  This script only records the diagnosis in BSIP1 data_corrections for traceability.
"""
import json, sys, os, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# TASK-238: Open Food Facts is BANNED. This script's trans-fat corrections were sourced
# from an OFF re-probe (off_reprobe_task234.json) — OFF-derived input. DISABLED.
raise RuntimeError(
    "OFF is banned (TASK-238): fix_trans_artifacts_corpus.py applied trans-fat values from "
    "an Open Food Facts re-probe and is disabled. OFF-derived nutrition must be NULLed, not "
    "corrected from OFF. Never use OFF."
)

os.environ["BARI_RECAL_P0"] = "on"
sys.path.insert(0, r"C:\Bari\03_operations\bsip2\proto_v0\src")

from input_loader import load_batch  # noqa: E402
from signal_extractor import extract_signals  # noqa: E402
from router_v2 import classify_category  # noqa: E402
from nova_proxy import infer_nova  # noqa: E402
from evaluation_scope import assign_evaluation_scope  # noqa: E402
from score_engine import score_product  # noqa: E402
from trace_writer import assemble_trace, write_trace  # noqa: E402
from structural_classifier import classify_structural_class  # noqa: E402

BSIP1_DIR = pathlib.Path(r"C:\Bari\02_products\salty_snacks\bsip1_outputs")
OUTPUT_ROOT = pathlib.Path(r"C:\Bari\02_products\salty_snacks\bsip2_outputs\run_salty_snacks_002")

# ── Trans artifacts to neutralize (authoritative OFF re-probe, TASK-234) ─────────
# barcode -> (per100g_before, serving_decl, serving_fraction, note)
TRANS_ARTIFACTS = {
    "7290000066318": (0.625, 0.5, 0.80, "Bamba classic: 0.5g/0.80 serving (kcal 428/535). high_concern -20 on artifact."),
    "7290104500572": (0.6,   0.3, 0.50, "Apropo Italiano: 0.3g '<1g' decl / 0.50 serving (every macro scales 0.50). high_concern -20 on artifact."),
    "7290000420325": (0.4,   0.4, 1.00, "Pop Star popcorn: 0.4g '<1g' decl at per-100g (frac 1.0). present -10 on artifact."),
    "7290004943738": (0.5,   0.5, 1.00, "Milotal chips: 0.5g '<1g' decl at per-100g. (engine already no-penalty; data made honest)."),
    "5701932026971": (0.5,   0.5, 1.00, "Hot Pop popcorn: 0.5g '<1g' decl at per-100g. (engine already no-penalty; data made honest)."),
    "7290117035009": (0.5,   None, None, "Yochananof popcorn: 0.5g '<1g' decl at per-100g (no serving block). (engine already no-penalty)."),
    "7290018198254": (0.5,   None, None, "Tapugan crisps: 0.5g '<1g' decl at per-100g. (engine already no-penalty; product also basis-error excluded)."),
    "7290110551926": (0.5,   None, None, "Tapuchips sweet-potato gourmet: 0.5g '<1g' decl at per-100g. (engine already no-penalty)."),
    "4011800528416": (0.5,   None, None, "Corny: 0.5g '<1g' decl at per-100g. (engine already no-penalty)."),
}

# ── Single-field per-100g basis omission (fiber) ─────────────────────────────────
FIBER_OMIT = {
    "7290112494313": (38.0, "Click cornflakes: fiber 38g impossible — fiber(38)+sugars(29.6)=67.6 > carbohydrates(66.15). Omit fiber (set None); rest of panel plausible."),
}

# ── Whole-panel basis-error diagnosis (drop handled in build; logged here) ────────
BASIS_ERROR_CHIPS = {
    "7290018198254": (128.0, "Whole-panel per-serving basis mislabeled per-100g (Atwater(macros)~123 == stated 128; real crisp ~450-540). No serving_size in OFF to recover -> unrecoverable; dropped from shelf."),
    "7290018198148": (139.0, "Whole-panel per-serving basis mislabeled per-100g (Atwater~135 == stated 139). Unrecoverable -> dropped from shelf."),
    "7290004943738": (145.0, "Whole-panel per-serving basis mislabeled per-100g (Atwater~142 == stated 145). Unrecoverable -> dropped from shelf."),
}

TASK = "TASK-234"


def add_correction(rec, field, old, new, reason):
    rec.setdefault("data_corrections", []).append({
        "field": field, "old_value": old, "new_value": new,
        "reason": reason, "task": TASK,
        "corrected_at_source": "open_food_facts (authoritative serving-level re-probe, off_reprobe_task234.json)",
    })


def main():
    corrected_files = set()

    # 1. Trans artifacts -> 0.0
    for bc, (before, decl, frac, note) in TRANS_ARTIFACTS.items():
        f = BSIP1_DIR / f"bsip1_snack_{bc}.json"
        rec = json.loads(f.read_text("utf-8"))
        nn = rec["normalized_nutrition_per_100g"]
        old = nn.get("fat_trans_g")
        if old in (0.0, None):
            print(f"  [trans] {bc} already 0.0/None (skipped) — {note}")
            continue
        nn["fat_trans_g"] = 0.0
        add_correction(rec, "normalized_nutrition_per_100g.fat_trans_g", old, 0.0,
                       f"OFF trans-fat per-100g ({old}) is the Israeli '<1g' serving "
                       f"THRESHOLD DECLARATION (serving={decl}g, serving_fraction={frac}), "
                       f"not a measured value. No PHVO/hydrogenated-oil marker present. {note}")
        f.write_text(json.dumps(rec, ensure_ascii=False, indent=2), encoding="utf-8")
        corrected_files.add(bc)
        print(f"  [trans] {bc}: fat_trans_g {old} -> 0.0")

    # 2. Fiber single-field omission
    for bc, (badval, note) in FIBER_OMIT.items():
        f = BSIP1_DIR / f"bsip1_snack_{bc}.json"
        rec = json.loads(f.read_text("utf-8"))
        nn = rec["normalized_nutrition_per_100g"]
        old = nn.get("dietary_fiber_g")
        if old is None:
            print(f"  [fiber] {bc} already None (skipped)")
        else:
            nn["dietary_fiber_g"] = None
            add_correction(rec, "normalized_nutrition_per_100g.dietary_fiber_g", old, None, note)
            f.write_text(json.dumps(rec, ensure_ascii=False, indent=2), encoding="utf-8")
            corrected_files.add(bc)
            print(f"  [fiber] {bc}: dietary_fiber_g {old} -> None")

    # 3. Basis-error diagnosis log (drop is in the build; no nutrition mutation here)
    for bc, (kcal, note) in BASIS_ERROR_CHIPS.items():
        f = BSIP1_DIR / f"bsip1_snack_{bc}.json"
        rec = json.loads(f.read_text("utf-8"))
        # avoid duplicate diagnosis entries on re-run
        already = any(c.get("field") == "BASIS_ERROR_DIAGNOSIS" for c in rec.get("data_corrections", []))
        if not already:
            add_correction(rec, "BASIS_ERROR_DIAGNOSIS", kcal, "excluded_from_shelf", note)
            f.write_text(json.dumps(rec, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"  [basis] {bc}: kcal {kcal}/100g flagged unrecoverable -> excluded in build")

    # 4. Re-score every product whose nutrition changed (trans + fiber), unchanged engine
    rescore = sorted(corrected_files)
    print(f"\nRe-scoring {len(rescore)} products on the UNCHANGED engine: {rescore}")
    batch = {p.get("barcode"): p for p in load_batch(BSIP1_DIR)}
    deltas = []
    for bc in rescore:
        product = batch.get(bc)
        if product is None:
            print(f"  ERROR: {bc} not found in batch"); continue
        # read prior published score from existing trace
        prev_tp = OUTPUT_ROOT / "products" / f"bsip1_snack_{bc}" / "bsip2_trace.json"
        prev_score = None
        if prev_tp.exists():
            prev_score = json.loads(prev_tp.read_text("utf-8")).get("final_score_estimate")

        signals = extract_signals(product)
        cat = classify_category(product)
        l3 = signals["L3_inferred_classifications"]
        nova = infer_nova(product, l3)
        scope = assign_evaluation_scope(product, cat["category"])
        score = score_product(product, signals, cat, nova, scope)
        trace = assemble_trace(product, signals, cat, nova, scope, score)
        trace["structural_class"] = classify_structural_class(trace)
        write_trace(trace, OUTPUT_ROOT)
        new_score = trace.get("final_score_estimate")
        deltas.append((bc, prev_score, new_score, trace.get("grade_estimate"),
                       score.get("trans_fat_veto")))
        print(f"  RESCORED {bc}: {prev_score} -> {new_score} ({trace.get('grade_estimate')}) "
              f"veto={score.get('trans_fat_veto')}")

    print("\n=== SCORE DELTAS ===")
    for bc, prev, new, grade, veto in deltas:
        d = (new - prev) if (prev is not None and new is not None) else None
        print(f"  {bc}: {prev} -> {new} ({grade})  delta={d}")


if __name__ == "__main__":
    main()
