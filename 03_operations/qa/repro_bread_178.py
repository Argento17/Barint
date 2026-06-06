"""
TASK-178 bread repro audit (read-only).
Re-runs HEAD bread pipeline against the SAME raw BSIP0 file used by the published
bread_retail_003 run, compares final_score/final_grade against published
bsip2_shufersal_*.json. Writes nothing to product dirs.
"""
import sys, json, pathlib, io, contextlib, importlib.util

SRC = pathlib.Path(r"C:\Bari\03_operations\bsip2\proto_v0\src")
sys.path.insert(0, str(SRC))

# import the bread runner module by path
spec = importlib.util.spec_from_file_location("bread_runner", SRC / "batch_run_bread_retail_003.py")
br = importlib.util.module_from_spec(spec)
buf = io.StringIO()
with contextlib.redirect_stderr(buf):
    spec.loader.exec_module(br)

RAW = pathlib.Path(r"C:\Bari\02_products\bread_retail_003\real_bread_retail_003_v1_20260525T194532_bsip0_raw.json")
PUB_DIR = pathlib.Path(r"C:\Bari\02_products\bread_retail_003\bsip2")

# Load published scores keyed by product_id
pub = {}
for f in PUB_DIR.glob("bsip2_shufersal_*.json"):
    t = json.load(open(f, encoding="utf-8"))
    pub[t.get("product_id")] = t

# Re-run HEAD
raw_products = json.loads(RAW.read_text(encoding="utf-8"))
head = {}
with contextlib.redirect_stderr(buf):
    for raw in raw_products:
        name_he = (raw.get("name_he") or "").strip()
        excl, reason = br._should_exclude(name_he)
        if excl:
            continue
        p = br.normalize_to_bsip1(raw)
        p["_load_errors"] = br.validate_product(p)
        try:
            r = br.run_pipeline(p)
            head[r["product_id"]] = r
        except Exception as e:
            head[p.get("canonical_product_id")] = {"_error": str(e)}

# Compare
matched = grade_aff = cosmetic = nullmatch = 0
rows = []
for pid, pt in sorted(pub.items()):
    ps = pt.get("final_score"); pg = pt.get("final_grade")
    ht = head.get(pid)
    if ht is None:
        rows.append((pid, ps, pg, "NO_HEAD", "-", "-", "MISSING")); continue
    if "_error" in ht:
        rows.append((pid, ps, pg, "ERR", "-", "-", ht["_error"][:25])); continue
    hs = ht.get("final_score"); hg = ht.get("final_grade")
    if ps is None and hs is None:
        rows.append((pid, ps, pg, hs, hg, "-", "MATCH(null)")); nullmatch += 1; matched += 1; continue
    if ps is None or hs is None:
        rows.append((pid, ps, pg, hs, hg, "n/a", "NULL_FLIP")); grade_aff += 1; continue
    delta = round(hs - ps, 1)
    if abs(delta) < 0.05 and pg == hg:
        v = "MATCH"; matched += 1
    elif pg != hg:
        v = "GRADE_FLIP"; grade_aff += 1
    elif abs(delta) >= 2:
        v = "DRIFT>=2"; grade_aff += 1
    else:
        v = "cosmetic"; cosmetic += 1
    rows.append((pid, ps, pg, hs, hg, delta, v))

sys.stdout.reconfigure(encoding="utf-8")
print(f"\n=== BREAD bread_retail_003: HEAD vs published ===")
print(f"published scored products: {len(pub)}   reproduced exactly: {matched}/{len(pub)} (of which null-match: {nullmatch})")
print(f"grade-affecting deltas: {grade_aff}   cosmetic (<2pt same grade): {cosmetic}")
print(f"\n{'product_id':22} {'pub_s':>6} {'pg':>3} {'head_s':>7} {'hg':>3} {'delta':>7}  verdict")
for r in rows:
    print(f"{str(r[0]):22} {str(r[1]):>6} {str(r[2]):>3} {str(r[3]):>7} {str(r[4]):>3} {str(r[5]):>7}  {r[6]}")
