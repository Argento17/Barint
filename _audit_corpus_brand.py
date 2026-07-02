import json
from pathlib import Path

DIRS = {
    "bread": r"c:\Bari\03_operations\bsip1\run_bread_conform_001\output",
    "hummus_canonical": r"c:\Bari\02_products\hummus\canonical_bsip1",
    "hummus_run001": r"c:\Bari\03_operations\bsip1\run_hummus_001\output",
    "hard_cheeses": r"c:\Bari\02_products\hard_cheeses\bsip1_outputs",
    "juices": r"c:\Bari\02_products\juices\bsip1_outputs",
    "cheese": r"c:\Bari\03_operations\bsip1\run_cheese_003\output",
    "cereals": r"c:\Bari\03_operations\bsip1\run_cereals_008\output",
}

for name, d in DIRS.items():
    p = Path(d)
    if not p.exists():
        print(name, "MISSING", d)
        continue
    total = with_b = 0
    samples = []
    for f in p.glob("*.json"):
        try:
            rec = json.loads(f.read_text(encoding="utf-8"))
        except:
            continue
        total += 1
        b = rec.get("brand")
        if b and str(b).strip():
            with_b += 1
            if len(samples) < 3:
                samples.append((rec.get("barcode"), str(b).strip(), (rec.get("canonical_name_he") or "")[:40]))
    print(f"{name}: {with_b}/{total} have brand")
    for s in samples:
        print("  ", s)
