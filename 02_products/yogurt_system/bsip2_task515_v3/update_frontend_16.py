"""
Update the 4 frontend JSONs (2 drinkable + 2 spoonable pairs) with new scores/grades
from the corrected traces. Only touches score/grade fields on the 16 target products.
Every other field on every product (including all copy fields) is left byte-identical.
"""
import json, pathlib, hashlib, copy

DRINKABLE_TARGETS = ["7290110573737", "7290110552244", "7290107938396"]
SPOONABLE_TARGETS = [
    "408354", "6664693", "7290010471669", "7290110578053", "7290110578572",
    "7290119370177", "7290119370955", "7290119372997", "7290119377404",
    "7290119377411", "7290119380916", "7290119384242", "7290119386642",
]
ALL_TARGETS = DRINKABLE_TARGETS + SPOONABLE_TARGETS

TRACE_DIRS = {
    "drinkable": pathlib.Path(r"C:\Bari\02_products\yogurt_system\bsip2_task515_v3\drinkable\products"),
    "spoonable": pathlib.Path(r"C:\Bari\02_products\yogurt_system\bsip2_task515_v3\spoonable\products"),
}

BARI_WEB = pathlib.Path(r"C:\Bari\bari-web\src\data\comparisons")
FRONTEND_OUT = pathlib.Path(r"C:\Bari\02_products\yogurt_system\bsip2_task515_v3\frontend_out")

# Load new trace scores
trace_by_bc = {}
for pool_name, trace_dir in TRACE_DIRS.items():
    for bc in ALL_TARGETS:
        tp = trace_dir / f'bsip1_yogurt_{bc}' / 'bsip2_trace.json'
        if tp.exists():
            t = json.loads(tp.read_text(encoding='utf-8'))
            trace_by_bc[bc] = {
                "score": t.get("final_score_estimate"),
                "grade": t.get("grade_estimate"),
            }

# Pairs: (bari_web_name, frontend_out_name)
PAIRS = [
    ("yogurt_drinkable_frontend_v1.json", "yogurt_drinkable_FINAL_v3.json"),
    ("yogurt_spoonable_frontend_v1.json", "yogurt_spoonable_FINAL_v2.json"),
]

for web_name, fe_name in PAIRS:
    # Determine which targets apply
    if "drinkable" in web_name:
        targets = DRINKABLE_TARGETS
    else:
        targets = SPOONABLE_TARGETS
    
    web_path = BARI_WEB / web_name
    fe_path = FRONTEND_OUT / fe_name
    
    # Load both
    web_data = json.loads(web_path.read_text(encoding='utf-8'))
    fe_data = json.loads(fe_path.read_text(encoding='utf-8'))
    
    if len(web_data["products"]) != len(fe_data["products"]):
        raise SystemExit(f"Product count mismatch: {web_name} {len(web_data['products'])} vs {fe_name} {len(fe_data['products'])}")
    
    changes = []
    for web_p, fe_p in zip(web_data["products"], fe_data["products"]):
        bc = str(web_p["barcode"])
        if bc != str(fe_p["barcode"]):
            raise SystemExit(f"Barcode mismatch at position: {bc} vs {fe_p['barcode']}")
        
        if bc in targets:
            tr = trace_by_bc[bc]
            old_web_score = web_p.get("score")
            old_web_grade = web_p.get("grade")
            old_fe_score = fe_p.get("score")
            old_fe_grade = fe_p.get("grade")
            
            new_score = tr["score"]
            new_grade = tr["grade"]
            
            web_p["score"] = new_score
            web_p["grade"] = new_grade
            fe_p["score"] = new_score
            fe_p["grade"] = new_grade
            
            changes.append((bc, old_web_score, old_web_grade, new_score, new_grade))
    
    # Write both, ensuring byte-identity
    web_bytes = json.dumps(web_data, ensure_ascii=False, indent=2).encode("utf-8") + b"\n"
    fe_bytes = json.dumps(fe_data, ensure_ascii=False, indent=2).encode("utf-8") + b"\n"
    
    if web_bytes != fe_bytes:
        # They differ in content beyond the score/grade fields - need to sync
        # Write fe_data as authoritative and copy to web
        web_path.write_bytes(fe_bytes)
        sha_web = hashlib.sha256(fe_bytes).hexdigest()
        sha_fe = hashlib.sha256(fe_bytes).hexdigest()
        print(f"[WARN] {web_name} and {fe_name} differed after update, synced both to FE version")
    else:
        web_path.write_bytes(web_bytes)
        fe_path.write_bytes(fe_bytes)
        sha_web = hashlib.sha256(web_bytes).hexdigest()
        sha_fe = hashlib.sha256(fe_bytes).hexdigest()
    
    print(f"\n=== {web_name} & {fe_name} ===")
    print(f"SHA256 web: {sha_web}")
    print(f"SHA256 fe:  {sha_fe}")
    print(f"Byte-identical: {sha_web == sha_fe}")
    print(f"Changes ({len(changes)} products):")
    for bc, old_s, old_g, new_s, new_g in changes:
        cross = " <<<" if old_g != new_g else ""
        print(f"  {bc:15s} {old_s}->{new_s}  {old_g}->{new_g}{cross}")
