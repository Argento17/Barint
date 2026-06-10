"""
Wire D4 additive enrichment for salty_snacks_frontend_v4.json (TASK-228 real rebuild).

Ingredient source: BSIP1 real corpus (02_products/salty_snacks/bsip1_outputs),
  ingredients_text_he keyed by barcode (v4 products carry `barcode` directly).
Explanation source: 01_framework/glass_box/w2_additive_copy_v1.md.

Coverage gate: if < 15% of products have ingredient text in BSIP1, halt.
Invariant (hard): score, grade, glassBox byte-identical after writing.
Products with no ingredient text: key absent (no empty array).
"""
import json, pathlib, sys, os
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT   = pathlib.Path(r"C:\Bari")
SRC    = ROOT / "03_operations" / "bsip2" / "proto_v0" / "src"
COMP   = ROOT / "bari-web" / "src" / "data" / "comparisons"
BSIP1  = ROOT / "02_products" / "salty_snacks" / "bsip1_outputs"
COPY   = ROOT / "01_framework" / "glass_box" / "w2_additive_copy_v1.md"
FE     = COMP / "salty_snacks_frontend_v4.json"
FE_LOCAL = ROOT / "02_products" / "salty_snacks" / "salty_snacks_frontend_v4.json"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
os.environ.setdefault("BARI_GLASSBOX_W2", "on")
os.environ.setdefault("BARI_RECAL_P0", "on")
from score_engine import detect_additives_d4  # noqa: E402

import re

def load_explanations(p):
    text = p.read_text(encoding="utf-8")
    lk = {}
    for block in re.split(r"(?=^### E)", text, flags=re.MULTILINE):
        hm = re.match(r"^### (E[\d]+[a-z]?(?:/E[\d]+[a-z]?)*)", block)
        if not hm: continue
        primary = hm.group(1).split("/")[0]
        em = re.search(r"\*\*Explanation \(final\):\*\*\s*(.+)", block)
        if em: lk[primary] = em.group(1).strip()
    return lk

def load_ingredients():
    m = {}
    for fp in BSIP1.glob("bsip1_snack_*.json"):
        d = json.loads(fp.read_text(encoding="utf-8"))
        bc = d.get("barcode")
        if bc:
            m[bc] = d.get("ingredients_text_he", "") or ""
    return m

def enrich(e, lk):
    out = {k: v for k, v in e.items() if k != "match_source"}
    out["explanation_he"] = lk.get(e["e_number"], "")
    return out

def main():
    lk = load_explanations(COPY)
    ing = load_ingredients()
    print(f"Explanations: {len(lk)} | BSIP1 ingredient map: {len(ing)}")

    fe = json.loads(FE.read_text(encoding="utf-8"))
    prods = fe["products"]
    have_ing = sum(1 for p in prods if ing.get(p.get("barcode", "")))
    cov = have_ing / max(1, len(prods))
    print(f"Ingredient coverage: {have_ing}/{len(prods)} = {cov:.1%}")
    if cov < 0.15:
        raise SystemExit(f"HALT: ingredient coverage {cov:.1%} < 15% D4 gate")

    pre = {p["id"]: (p.get("score"), p.get("grade"), json.dumps(p.get("glassBox"), ensure_ascii=False)) for p in prods}

    enriched_n = no_ing = zero = 0
    for p in prods:
        bc = p.get("barcode", "")
        text = ing.get(bc, "")
        if not text:
            p.pop("d4_additives", None); no_ing += 1; continue
        d4 = detect_additives_d4(text)
        rows = [enrich(e, lk) for e in d4]
        if rows:
            p["d4_additives"] = rows; enriched_n += 1
            print(f"  {p['id']} [{bc}]: {[r['e_number'] for r in rows]}")
        else:
            p.pop("d4_additives", None); zero += 1

    out = json.dumps(fe, ensure_ascii=False, indent=2)
    FE.write_text(out, encoding="utf-8")
    FE_LOCAL.write_text(out, encoding="utf-8")

    fe2 = json.loads(FE.read_text(encoding="utf-8"))
    viol = []
    for p in fe2["products"]:
        s, g, gb = pre[p["id"]]
        if p.get("score") != s: viol.append(f"{p['id']} score")
        if p.get("grade") != g: viol.append(f"{p['id']} grade")
        if json.dumps(p.get("glassBox"), ensure_ascii=False) != gb: viol.append(f"{p['id']} glassBox")
    if viol:
        raise AssertionError(f"INVARIANT VIOLATION: {viol}")

    print(f"\nWith d4_additives: {enriched_n} | no ingredients: {no_ing} | 0 additives: {zero}")
    print("INVARIANT (score/grade/glassBox): PASS")

if __name__ == "__main__":
    main()
