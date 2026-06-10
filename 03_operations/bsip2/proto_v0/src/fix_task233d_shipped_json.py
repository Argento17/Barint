"""
TASK-233D — targeted data fixes applied directly to the SHIPPED frontend JSONs.

These are discrete defects from the TASK-233 confirmation sweep, not root-cause work.
Each fix is a data-only edit (dedup / round / wrong-barcode removal). NO scoring
methodology change; the only score change is the butter float -> int rounding (QA-007),
which is a display normalization, not a re-score.

Run: python fix_task233d_shipped_json.py
"""
import io, json, pathlib, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

WEB = pathlib.Path(r"C:\bari\bari-web\src\data\comparisons")


def load(fn):
    return json.loads((WEB / fn).read_text("utf-8"))


def save(fn, data):
    (WEB / fn).write_text(json.dumps(data, ensure_ascii=False, indent=2), "utf-8")


def fix_yogurt_dup():
    """QA-005: barcode 7290107936309 appears twice — yog-007 (Shufersal, real Hebrew
    name, 78/B) and bsip1_yogurt_7290107936309 (Yohananof, untranslated 'Greek yogurt',
    75/B). Same product scored twice. Keep the Shufersal record (named, frozen baseline);
    drop the untranslated Yohananof duplicate."""
    fn = "yogurts_frontend_v3.json"
    d = load(fn)
    before = len(d["products"])
    keep, dropped = [], []
    for p in d["products"]:
        if p.get("id") == "bsip1_yogurt_7290107936309":
            dropped.append(p)
            continue
        keep.append(p)
    d["products"] = keep
    if "_meta" in d:
        d["_meta"]["product_count"] = len(keep)
        d["_meta"]["scored_count"] = sum(1 for p in keep if p.get("score") is not None)
        rb = d["_meta"].get("retailer_breakdown")
        if isinstance(rb, dict) and "yohananof" in rb and dropped:
            rb["yohananof"] = max(0, rb["yohananof"] - len(dropped))
    save(fn, d)
    print(f"[QA-005] yogurts dedup 7290107936309: {before} -> {len(keep)} "
          f"(dropped {[p['id'] for p in dropped]}; kept Shufersal yog-007)")


def fix_snacks_barcode():
    """QA-006: barcode 7290011498894 is on TWO distinct products — snk-015
    ('חטיף תמרים במילוי חמאת בוטנים', the genuine owner per BSIP1 name match) and snk-003
    ('קראנצ׳י שיבולת שועל עם דבש', a different oat+honey product). snk-003 carries the
    WRONG barcode. Its true barcode is not recoverable without inventing identity (the
    only name-matching candidate, 16000548404, is already used by another snack), so null
    snk-003's barcode rather than ship a known-wrong identity. snk-015 keeps the barcode."""
    fn = "snacks_frontend_v2.json"
    d = load(fn)
    fixed = None
    for p in d["products"]:
        if p.get("id") == "snk-003" and str(p.get("barcode")) == "7290011498894":
            p["barcode"] = None
            fixed = p["id"]
    save(fn, d)
    print(f"[QA-006] snacks barcode 7290011498894: nulled wrong barcode on {fixed} "
          f"(snk-015 retains it — exact BSIP1 name match)")


def fix_butter_float():
    """QA-007: bsip1_butter_369709 ships score 45.2 (float). The VM requires a rounded
    int. round(45.2)=45 -> grade D unchanged (35..49). Display normalization only."""
    fn = "butter_frontend_v2.json"
    d = load(fn)
    fixed = []
    for p in d["products"]:
        s = p.get("score")
        if isinstance(s, float):
            p["score"] = int(round(s))
            fixed.append((p["id"], s, p["score"]))
    save(fn, d)
    print(f"[QA-007] butter float scores rounded: {fixed}")


if __name__ == "__main__":
    fix_yogurt_dup()
    fix_snacks_barcode()
    fix_butter_float()
    print("TASK-233D shipped-JSON fixes applied.")
