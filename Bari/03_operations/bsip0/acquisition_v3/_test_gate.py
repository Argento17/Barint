import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from composition_gate import classify_archetype, check_composition, print_gate_result

test_products = [
    {"name_he": "לחם לבן"},
    {"name_he": "לחם אחיד"},
    {"name_he": "פיתה"},
    {"name_he": "קרקר כוסמין"},
    {"name_he": "לחם מחמצת שיפון"},
    {"name_he": "טוסט"},
    {"name_he": "חלה"},
    {"name_he": "בגט"},
    {"name_he": "לחם"},
    {"name_he": "קרקר פריך בסגנון שוודי"},
]
for p in test_products:
    arch = classify_archetype(p["name_he"])
    print(f'{p["name_he"]:30s} -> {arch}')

print("\n--- Gate check on small corpus (expected FAIL, too few products) ---")
gate = check_composition(test_products)
print_gate_result(gate)
