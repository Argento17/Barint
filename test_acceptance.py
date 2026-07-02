import os
import sys
import json

sys.path.insert(0, r"C:\Bari\03_operations\bsip2\proto_v0\src")
import signal_extractor

def test_product(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        doc = json.load(f)
    
    # Test OFF
    os.environ["BARI_PALM_HYDRO_V1"] = "off"
    signal_extractor.PALM_HYDRO_V1_ON = False
    signals_off = signal_extractor.extract_signals(doc)
    val_off = signals_off["L3_inferred_classifications"]["has_phvo_generic"]

    # Test ON
    os.environ["BARI_PALM_HYDRO_V1"] = "on"
    signal_extractor.PALM_HYDRO_V1_ON = True
    signals_on = signal_extractor.extract_signals(doc)
    val_on = signals_on["L3_inferred_classifications"]["has_phvo_generic"]
    
    print(f"Product: {os.path.basename(filepath)}")
    print(f"  OFF: {val_off}")
    print(f"  ON:  {val_on}")

print("--- Acceptance Test ---")
test_product(r"C:\Bari\03_operations\bsip1\run_cakes_001\output\bsip1_cakes_2472841.json")
test_product(r"C:\Bari\03_operations\bsip1\run_cakes_001\output\bsip1_cakes_1361177.json")
# Also testing the Maadan that ONLY has hardened palm oil
test_product(r"C:\Bari\03_operations\bsip1\run_maadanim_001\output\bsip1_7290019167112.json")
