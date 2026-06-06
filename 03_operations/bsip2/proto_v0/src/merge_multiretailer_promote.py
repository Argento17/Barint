"""
Merge the TASK-184 multi-retailer promote set into the two LIVE corpora.
Owner-approved (2026-06-05): promote 33 new products (held the 81.2/A artifact + 6 savory
Fitness crackers at curation; HOLD 'Nestle Fitness Chocolate & Rice' 7613032045753 for an
implausible sodium=1272 OFF artifact). ADD-ONLY: existing 66 rows + scores are untouched.
"""
import json, pathlib, datetime, re

STAGING = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_cereals_multiretailer_001\promote_staging.json")
CEREALS = pathlib.Path(r"C:\Bari\bari-web\src\data\comparisons\cereals_frontend_v1.json")
GRANOLA = pathlib.Path(r"C:\Bari\bari-web\src\data\comparisons\granola_frontend_v1.json")

HOLD_IDS = {"7613032045753"}  # implausible sodium=1272 — route for re-verify, do not ship
VM_KEYS = {"id","name","imageUrl","score","grade","insightLine","confidence",
           "expansion","rowVerdict","_subpool","_isChildrens","_wholeGrainClaim"}
CONTAM = re.compile(r"^\s*פתיתים\b|פתיתים\s+אפויים|^\s*קמח\b|^\s*שוקולד|פסטה|נודלס|וויט|חלה")

staging = json.loads(STAGING.read_text("utf-8"))
staging = staging["products"] if isinstance(staging, dict) and "products" in staging else staging

new_by_cat = {"breakfast-cereals": [], "granola": []}
held = []
for p in staging:
    if any(h in p["id"] for h in HOLD_IDS):
        held.append(p["name"]); continue
    assert p.get("insightLine") and p.get("rowVerdict"), f"missing authored copy: {p['id']}"
    cat = p["category"]
    rec = {k: p[k] for k in VM_KEYS if k in p}     # drop the non-VM 'category' field
    new_by_cat[cat].append(rec)

print(f"held (not promoted): {held}")
print(f"new to promote: cereals={len(new_by_cat['breakfast-cereals'])} granola={len(new_by_cat['granola'])}")

def merge(live_path, new_recs, cat_label):
    doc = json.loads(live_path.read_text("utf-8"))
    live = doc["products"]
    old_scores = {p["id"]: p["score"] for p in live}
    old_ids = set(old_scores)
    new_ids = {p["id"] for p in new_recs}
    dup = old_ids & new_ids
    assert not dup, f"{cat_label}: id collision with live: {dup}"
    merged = live + new_recs
    # regression: every pre-existing row unchanged
    for p in merged:
        if p["id"] in old_scores:
            assert p["score"] == old_scores[p["id"]], f"score drift on existing {p['id']}"
    assert all(p.get("insightLine") and p.get("rowVerdict") for p in merged), "empty copy after merge"
    assert len({p["id"] for p in merged}) == len(merged), "dup ids after merge"
    merged.sort(key=lambda x: (x.get("score") or 0), reverse=True)
    assert not CONTAM.search(merged[0]["name"]), f"{cat_label}: #1 looks like a contaminant: {merged[0]['name']}"
    doc["products"] = merged
    doc["_meta"]["product_count"] = len(merged)
    doc["_meta"]["scored_count"] = len(merged)
    doc["_meta"]["generated"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    doc["_meta"]["provenance"] = (doc["_meta"].get("provenance","") +
        f" | +{len(new_recs)} multi-retailer (Carrefour/Yochananof, run_cereals_multiretailer_001, "
        f"EV-045/045b/045c; held A artifact + sodium artifact). 2026-06-05.")
    live_path.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
    g = {}
    for p in merged: g[p["grade"]] = g.get(p["grade"],0)+1
    print(f"\n{cat_label}: {len(live)} -> {len(merged)}  grades={g}")
    print(f"  top5: {[(p['name'][:28], p['score'], p['grade']) for p in merged[:5]]}")
    return len(merged)

c = merge(CEREALS, new_by_cat["breakfast-cereals"], "breakfast-cereals")
g = merge(GRANOLA, new_by_cat["granola"], "granola")
print(f"\nFINAL LIVE: cereals={c}  granola={g}")
