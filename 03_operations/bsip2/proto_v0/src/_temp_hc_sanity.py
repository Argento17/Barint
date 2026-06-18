"""
EV-099 HC-002 revert sanity check.
Runs the two affected HC products through the amended engine.
Expected: nova=2 (or 3 from main classifier), score ~39/D, sat_fat_inferred=True.
"""
import os, json, pathlib, sys
os.environ.setdefault("BARI_RECAL_P0", "on")
os.environ.setdefault("BARI_SHELF_RELATIVE_V1", "on")
os.environ.setdefault("BARI_FAT_TECH_V1", "on")
sys.path.insert(0, str(pathlib.Path(__file__).parent))

from signal_extractor import extract_signals
from router_v2 import classify_category
from nova_proxy import infer_nova
from evaluation_scope import assign_evaluation_scope
from score_engine import score_product, set_shelf_stats, clear_shelf_stats
from constants import FATSAT_SHELF_REL_HARDCHEESE_MEDIAN, FATSAT_SHELF_REL_HARDCHEESE_SCALE

HC_BSIP1_DIR = pathlib.Path(r"C:\Bari\02_products\hard_cheeses\bsip1_outputs")
TARGET_FILES = [
    HC_BSIP1_DIR / "bsip1_hardcheese_7290108502725.json",
    HC_BSIP1_DIR / "bsip1_hardcheese_7290019635192.json",
]

set_shelf_stats("fat_saturated_g", FATSAT_SHELF_REL_HARDCHEESE_MEDIAN, FATSAT_SHELF_REL_HARDCHEESE_SCALE, "mad", 22)

results = []
for fpath in TARGET_FILES:
    if not fpath.exists():
        print(f"FILE NOT FOUND: {fpath}")
        continue
    d = json.loads(fpath.read_text(encoding="utf-8"))
    bc = str(d.get("barcode", fpath.stem))
    signals = extract_signals(d)
    cat = classify_category(d)
    l3 = signals["L3_inferred_classifications"]
    nova = infer_nova(d, l3)
    ev = assign_evaluation_scope(d, cat["category"])
    sr = score_product(d, signals, cat, nova, ev)
    nn = d.get("normalized_nutrition_per_100g", {})
    sat_fat_inf = l3.get("sat_fat_inferred")
    sat_fat_val = l3.get("sat_fat_inferred_value")
    score = sr.get("final_score_estimate")
    grade = sr.get("grade_estimate")
    nova_lvl = nova["nova_level"]
    caps = [c["rule"] for c in sr.get("caps_applied", [])]
    binding = sr.get("binding_cap")

    print(f"bc:{bc}")
    print(f"  fat_g={nn.get('fat_g')}  sat_fat_label={nn.get('fat_saturated_g')}  sodium={nn.get('sodium_mg')}")
    print(f"  nova={nova_lvl}  score={score}  grade={grade}")
    print(f"  sat_fat_inferred={sat_fat_inf}  sat_fat_inferred_value={sat_fat_val}")
    print(f"  binding_cap={binding}  caps={caps}")
    print()
    results.append((bc, nova_lvl, score, grade, sat_fat_inf))

clear_shelf_stats("fat_saturated_g")

print("=== SANITY CHECK ===")
for bc, nova_lvl, score, grade, sat_fat_inf in results:
    nova_ok = nova_lvl != 1  # Must NOT be NOVA-1 after revert
    score_ok = score is not None and score <= 45  # Should be ~39/D with 2-redlabel cap
    satfat_ok = sat_fat_inf is True
    status = "PASS" if (nova_ok and score_ok and satfat_ok) else "FAIL"
    print(f"  {status}  bc:{bc}  nova={nova_lvl} (not 1? {nova_ok})  score={score} (<=45? {score_ok})  sat_fat_inf={sat_fat_inf} ({satfat_ok})")
