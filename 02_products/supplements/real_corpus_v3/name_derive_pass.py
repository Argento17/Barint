"""Free (zero-web) name-derive pass over the full addressable shelf.

Conservatively extracts active+dose+unit from the Super-Pharm item name ALONE, for
single-active SKUs where the name explicitly encodes the dose. Honesty-first: emits a
candidate ONLY on an unambiguous pattern; anything else -> needs_fetch (never inferred).
This produces (a) a zero-cost coverage floor and (b) the exact remaining fetch worklist
by brand, so the heavy acquisition can be scoped/dispatched.

EDPG: all candidate; name_derived doses are flagged for QA unit-verification.
"""
import sys, json, pathlib, re, collections
ROOT = r"C:\Bari"
sys.path.insert(0, ROOT)
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = pathlib.Path(__file__).resolve().parent

addr = json.loads((HERE / "_addressable_shelf.json").read_text(encoding="utf-8"))
rows = addr["rows"]

# pack-count / non-dose tokens to strip before dose extraction (so '60 כמוסות',
# '100 טבליות', '9 חודשים', '40 מל' don't masquerade as a dose).
PACK = re.compile(r"\d+\s*(?:כמוסות|כמוסה|טבליות|טבליה|קפסולות|קפליות|קפליה|יח['\"]?|"
                  r"יחידות|חודשים|מל|מ\"ל|ml|גרם|ג['\"]?|טיפות|softgel|capsules?)", re.I)
# explicit unit tokens
UNIT = r"(?:מ\"?ג|מ['׳]ג|מג|mg|מק\"?ג|מקג|mcg|µg|יחב\"?ל|יחבל|iu)"
DOSE = re.compile(r"(\d{2,4})\s*(" + UNIT + r")", re.I)
# active-specific in-name dose conventions (number adjacent to the active token)
CONV = {
    "vitamin_d3": (re.compile(r"\bd[\s\-]?(\d{2,5})\b", re.I), "IU"),   # D-400 / D 1000
    "vitamin_c":  (re.compile(r"\bc[\s\-]?(\d{2,4})\b", re.I), "mg"),    # C500 / C 1000
}

def norm_unit(u):
    u = u.lower().replace('"', "").replace("׳", "").replace("'", "").replace(" ", "")
    if u in ("מג", "מ״ג", "mg", "מגג"): return "mg"
    if u.startswith("מק") or u in ("mcg", "µg"): return "mcg"
    if u.startswith("יחב") or u == "iu": return "IU"
    if "מג" in u: return "mg"
    return None

# omega3 NEVER name-derives: a single name number is total fish-oil, not the EPA/DHA the
# engine scores. caffeine/biotin/b12/iron/zinc/calcium/folic: only on an explicit unit.
NAME_DERIVABLE = {"magnesium", "vitamin_c", "vitamin_d3", "biotin", "vitamin_b12",
                  "caffeine", "zinc", "iron", "calcium", "vitamin_e"}

derived, needs_fetch = [], []
for r in rows:
    name, active = r["name_he"], r["active"]
    if active not in NAME_DERIVABLE:
        needs_fetch.append(r); continue
    stripped = PACK.sub(" ", name)
    dose = unit = None
    # 1) explicit "<num><unit>"
    m = DOSE.search(stripped)
    if m:
        dose, unit = int(m.group(1)), norm_unit(m.group(2))
    # 2) active-specific convention (D-/C-)
    if dose is None and active in CONV:
        cm = CONV[active][0].search(stripped)
        if cm:
            dose, unit = int(cm.group(1)), CONV[active][1]
    if dose is not None and unit:
        rec = dict(r); rec["derived_dose"] = dose; rec["derived_unit"] = unit
        rec["unit_inferred"] = bool(m is None)  # convention path infers the unit
        derived.append(rec)
    else:
        needs_fetch.append(r)

print(f"addressable={len(rows)}  name_derived={len(derived)}  needs_fetch={len(needs_fetch)}")
print(f"zero-cost coverage floor = {100*len(derived)/len(rows):.1f}% of addressable\n")
print("name-derived by active:",
      dict(collections.Counter(r["active"] for r in derived).most_common()))
print("\nNEEDS-FETCH worklist by brand:")
for b, n in collections.Counter(r["brand_bucket"] for r in needs_fetch).most_common():
    print(f"  {b:<10} {n}")
print("\nNEEDS-FETCH by active:",
      dict(collections.Counter(r["active"] for r in needs_fetch).most_common()))

(HERE / "_name_derived.json").write_text(
    json.dumps({"derived": derived, "needs_fetch": needs_fetch},
               ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\nwrote {HERE/'_name_derived.json'}  (derived + needs_fetch worklist)")
