import sys, json, pathlib, os

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

os.environ["BARI_SHELF_RELATIVE_V1"] = "on"
os.environ["BARI_FAT_TECH_V1"] = "on"
os.environ["BARI_RECAL_P0"] = "on"

SRC = pathlib.Path(r"C:\Bari\03_operations\bsip2\proto_v0\src")
sys.path.insert(0, str(SRC))

from signal_extractor import extract_signals
from nova_proxy import infer_nova

BSIP1_DIR = pathlib.Path(r"C:\Bari\02_products\juices\bsip1_outputs")
BARCODES = ["7290110114886", "7290013153395", "7290004030100", "7290003009640", "7290000525969"]

for bc in BARCODES:
    f = BSIP1_DIR / f"bsip1_juice_{bc}.json"
    doc = json.loads(f.read_text(encoding="utf-8"))
    sigs = extract_signals(doc)
    L1 = sigs["L1_observed_signals"]
    L3 = sigs["L3_inferred_classifications"]
    nova = infer_nova(doc, L3)
    print(f"=== {bc} ===")
    print(f"  L1 ingredient_count={L1.get('ingredient_count')} ingredient_list={L1.get('ingredient_list')}")
    print(f"  L1 ingredient_text_quality={L1.get('ingredient_text_quality')}")
    print(f"  nova_proxy={nova.get('nova_proxy')} nova_confidence={nova.get('nova_confidence')}")
    print(f"  nova_evidence_for={nova.get('nova_evidence_for')}")
    ing_sanitize = L1.get("ingredient_sanitization", {})
    print(f"  sanitization raw_count={ing_sanitize.get('raw_count')} clean_count={ing_sanitize.get('clean_count')}")
    print()
