"""Deeper investigation of 6 mismatching barcodes."""
import io
import json
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

rami_path = sys.argv[1]
shuf_path = sys.argv[2]

with open(rami_path, encoding="utf-8") as f:
    rami_table = json.load(f)

# Load full Shufersal raw for richer data
with open(shuf_path, encoding="utf-8") as f:
    shuf_raw = json.load(f)

rami_by_bc = {str(p["barcode"]).strip(): p for p in rami_table if p.get("barcode")}
shuf_by_bc = {str(p.get("barcode","")).strip(): p for p in shuf_raw if p.get("barcode")}

MISMATCH_BCS = [
    "7290016867046",
    "7290016867114",
    "7290016867282",
    "7290016967074",
    "7290017947105",
    "7290112968807",
]

print("=== Mismatch root-cause analysis ===\n")
for bc in MISMATCH_BCS:
    r = rami_by_bc.get(bc)
    s = shuf_by_bc.get(bc)
    if not r or not s:
        print(f"BC={bc}: missing in one source")
        continue
    s_nutr = s.get("nutrition", {})
    print(f"BC={bc}")
    print(f"  RL: {r.get('name_he','')}")
    print(f"  SH: {s.get('name_he', s.get('name',''))}")
    print(f"  RL source_url: {r.get('source_url','')[:80]}")
    # Check if numbers are consistent with a "light" (per-serving not per-100g) scenario
    rl_e = r.get("energy_kcal_raw", "")
    sh_e = s_nutr.get("energy_kcal_raw", "")
    print(f"  energy: RL={rl_e}  SH={sh_e}")
    rl_so = r.get("sodium_raw", "")
    sh_so = s_nutr.get("sodium_raw", "")
    print(f"  sodium: RL={rl_so}  SH={sh_so}")
    rl_fat = r.get("fat_raw", "")
    sh_fat = s_nutr.get("fat_raw", "")
    print(f"  fat:    RL={rl_fat}  SH={sh_fat}")
    print()

# Summary: ratio analysis for the big-diff cases
print("=== Ratio analysis for 300%+ mismatches ===")
print("(if RL/SH ~ 4.2, likely SH stored per-serving ~24g; RL is per-100g)")
for bc in ["7290016867114", "7290112968807"]:
    r = rami_by_bc.get(bc, {})
    s = shuf_by_bc.get(bc, {})
    s_nutr = s.get("nutrition", {}) if s else {}
    try:
        rl_e = float(r.get("energy_kcal_raw", 0))
        sh_e = float(s_nutr.get("energy_kcal_raw", 0))
        ratio = rl_e / sh_e if sh_e else 0
        print(f"  BC={bc}: RL_energy={rl_e}  SH_energy={sh_e}  ratio={ratio:.2f}")
    except Exception as e:
        print(f"  BC={bc}: error {e}")
