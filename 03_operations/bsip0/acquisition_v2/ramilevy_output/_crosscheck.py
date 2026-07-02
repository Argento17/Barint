"""Cross-check Rami Levy vs Shufersal nutrition for overlapping bread barcodes."""
import io
import json
import sys

# Force UTF-8 output to avoid cp1252 crash on Hebrew
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

rami_path = sys.argv[1]
shuf_path = sys.argv[2]

with open(rami_path, encoding="utf-8") as f:
    rami = json.load(f)
with open(shuf_path, encoding="utf-8") as f:
    shuf = json.load(f)

# Build barcode lookup dicts
shuf_by_bc = {}
for p in shuf:
    bc = str(p.get("barcode", "")).strip()
    if bc:
        shuf_by_bc[bc] = p

rami_by_bc = {}
for p in rami:
    bc = str(p.get("barcode", "")).strip()
    if bc:
        rami_by_bc[bc] = p

overlap_bcs = set(rami_by_bc.keys()) & set(shuf_by_bc.keys())
print(f"Rami Levy unique barcodes : {len(rami_by_bc)}")
print(f"Shufersal unique barcodes : {len(shuf_by_bc)}")
print(f"Overlapping barcodes      : {len(overlap_bcs)}")
print()

def safe_float(v):
    try:
        return float(str(v).replace(",", ".").strip())
    except Exception:
        return None

MAX_DIFF_PCT = 10.0
matches = []
mismatches = []

for bc in sorted(overlap_bcs):
    r = rami_by_bc[bc]
    s = shuf_by_bc[bc]
    s_nutr = s.get("nutrition", {})

    fields = [
        ("energy_kcal", r["energy_kcal_raw"], s_nutr.get("energy_kcal_raw", "")),
        ("sodium",      r["sodium_raw"],       s_nutr.get("sodium_raw", "")),
        ("protein",     r["protein_raw"],      s_nutr.get("protein_raw", "")),
        ("carbs",       r["carbs_raw"],        s_nutr.get("carbs_raw", "")),
        ("fat",         r["fat_raw"],          s_nutr.get("fat_raw", "")),
    ]

    mismatch_fields = []
    for fname, rv, sv in fields:
        rf = safe_float(rv)
        sf = safe_float(sv)
        if rf is None or sf is None:
            continue
        if sf == 0:
            continue
        diff_pct = abs(rf - sf) / sf * 100
        if diff_pct > MAX_DIFF_PCT:
            mismatch_fields.append((fname, rv, sv, f"{diff_pct:.1f}%"))

    r_name = r.get("name_he", "")[:40]
    s_name = s.get("name_he", s.get("name", ""))[:40]

    if mismatch_fields:
        mismatches.append((bc, r_name, s_name, mismatch_fields))
    else:
        matches.append(bc)

print(f"Cross-check (>{MAX_DIFF_PCT}% diff threshold):")
print(f"  Consistent  : {len(matches)}/{len(overlap_bcs)}")
print(f"  Mismatches  : {len(mismatches)}/{len(overlap_bcs)}")
print()

if mismatches:
    print("Mismatch details:")
    for bc, rn, sn, mf in mismatches[:15]:
        print(f"  BC={bc}")
        print(f"    Rami Levy : {rn}")
        print(f"    Shufersal : {sn}")
        for fn, rv, sv, dp in mf:
            print(f"    {fn}: RL={rv}  SH={sv}  diff={dp}")
        print()
else:
    print("No mismatches. All overlapping products consistent within 10%.")

print()
print("Sample overlapping products (first 5):")
for bc in sorted(overlap_bcs)[:5]:
    r = rami_by_bc[bc]
    s = shuf_by_bc[bc]
    s_nutr = s.get("nutrition", {})
    print(f"  BC={bc}")
    print(f"    RL name   : {r.get('name_he','')[:50]}")
    print(f"    SH name   : {s.get('name_he', s.get('name',''))[:50]}")
    print(f"    RL energy={r['energy_kcal_raw']}  fat={r['fat_raw']}  sodium={r['sodium_raw']}")
    print(f"    SH energy={s_nutr.get('energy_kcal_raw','')}  fat={s_nutr.get('fat_raw','')}  sodium={s_nutr.get('sodium_raw','')}")
    print()
