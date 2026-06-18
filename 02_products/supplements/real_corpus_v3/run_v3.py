"""TASK-171 revival — v3 re-measurement sprint run harness.

Re-measures real acquisition yield on a brand-stratified 25-SKU sample, using BOTH
acquisition methods the v2 run lacked: (A) brand-site/retailer panels AND (B) name-derived
single-active doses. Per addressable SP SKU: resolve a candidate panel (barcode-first),
assemble a BSIP0-S label, score through the REAL SIE engine, write trace. EDPG: candidate.

This is the same pipeline as run_corpus_v2.py; it reads _sample.json (25 SKUs) and the
v3 cache, and tags each scored SKU with its acquisition_method for the yield breakdown.
"""
import sys, json, pathlib, datetime, collections

ROOT = r"C:\Bari"
ENGINE = pathlib.Path(ROOT) / "03_operations" / "supplement_engine" / "proto_v0"
sys.path.insert(0, ROOT)
sys.path.insert(0, str(ENGINE / "src"))
sys.path.insert(0, str(ENGINE))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from supplement_label import SupplementLabel, LabelActive
from score_engine import score_label
from dossier_loader import load_dossier
from trace_writer import assemble_trace
from integrations.clients.il_supplement_panels import ILPanel, cache_scraper, acquire_panel
from integrations.clients import il_panel_resolver as rez

HERE = pathlib.Path(__file__).resolve().parent
CACHE = HERE / "cache"
SKUDIR = HERE / "skus"
SKUDIR.mkdir(exist_ok=True)

# Hebrew structure/function -> English umbrella key (same map as v2)
_CLAIM_HINT = {
    "לחץ דם": "blood pressure", "לב": "heart health", "לבב": "heart health",
    "עצבים": "nerve health", "עצב": "nerve health",
    "עצמות": "bone health", "עצם": "bone health", "שלד": "bone health",
    "שריר": "muscle health", "שרירים": "muscle health",
    "חיסון": "immune health", "חיסונית": "immune health",
    "עייפות": "fatigue", "תשישות": "fatigue", "אנרגיה": "energy",
    "עור": "skin health", "שיער": "hair health", "ציפורניים": "nail health",
    "מוח": "brain health", "קוגניטיב": "cognitive", "ריכוז": "cognitive",
    "ראיה": "vision", "עיניים": "eye health", "דם אדומים": "blood",
    "שינה": "sleep", "ערנות": "alertness", "הריון": "pregnancy",
}
_STUDIED_HINT = {
    "vitamin_d3": [(("חוסר", "מחסור", "השלמ", "רמת", "status", "deficien", "עצם", "סידן"),
                    "correcting/maintaining vitamin D status (raising serum 25(OH)D)")],
    "iron": [(("חוסר", "מחסור", "אנמי", "ברזל", "הריון"), "iron-deficiency anemia treatment/prevention")],
    "folic_acid": [(("הריון", "עובר", "נטית", "neural"), "neural tube defect risk reduction (periconceptional)")],
    "vitamin_b12": [(("חוסר", "מחסור", "b12", "אנמי", "דם אדומים"), "treating/preventing B12 deficiency")],
    "vitamin_c": [(("חוסר", "צפדינה", "scurvy"), "scurvy / vitamin C deficiency")],
}
UNMAPPED = "__unmapped__"


def panel_from_cache_obj(obj):
    url = obj.get("url")
    one = {url: obj.get("json", obj)}
    return acquire_panel(url, lambda u, s, p: one.get(u, {}), source_id=obj.get("source_id"))


def load_panels():
    panels, methods = [], {}
    for fp in sorted(CACHE.glob("*.json")):
        try:
            obj = json.loads(fp.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            continue
        if not obj.get("url"):
            continue
        p = panel_from_cache_obj(obj)
        panels.append(p)
        methods[p.barcode] = obj.get("acquisition_method", "unknown")
    return panels, methods


def curate_claim(panel, sp_active=None):
    raw = panel.primary_claim or ""
    low = raw.lower()
    for keys, studied in _STUDIED_HINT.get(sp_active or "", []):
        if any(k in low for k in keys):
            return studied, f"studied endpoint from HE: '{raw[:50]}'"
    hits = [en for he, en in _CLAIM_HINT.items() if he in raw]
    if hits:
        return " ".join(sorted(set(hits))), f"S/F umbrella from HE: '{raw[:50]}'"
    if not raw:
        return UNMAPPED, "no on-label claim -> Insufficient"
    return UNMAPPED, f"HE claim did not map -> Insufficient: '{raw[:50]}'"


def build_label(sku_id, sp_item, sp_active, panel):
    lossy = list(panel.missing_fields)
    act = next((a for a in panel.actives if a.active_slug == sp_active), None)
    if act is None:
        act = next((a for a in panel.actives if a.active_slug), None)
    if act is None:
        return None, "no mappable active", lossy + ["no engine-mappable active"]
    claim_text, claim_note = curate_claim(panel, sp_active)
    label = SupplementLabel(
        sku_id=sku_id, product_name=panel.product_name or sp_item.name,
        primary_claim=claim_text, servings_per_day=1.0,
        actives=[LabelActive(active_slug=act.active_slug,
                             display_name=act.ingredient or sp_item.name,
                             quantity=act.amount, unit=act.unit, form=act.form,
                             is_core=True)])
    return label, claim_note, lossy


class SP:
    def __init__(s, r):
        s.barcode = r["barcode"]; s.name = r["name_he"]
        s.manufacturer = r.get("manufacturer"); s.price = r.get("price_ils")


def main():
    sample = json.loads((HERE / "_sample.json").read_text(encoding="utf-8"))
    rows = sample["rows"]
    panels, methods = load_panels()
    print(f"loaded {len(panels)} cached panels; {len(rows)} sample SKUs")

    results = []
    counts = collections.Counter()
    per_method = collections.Counter()
    grades = collections.Counter()

    for r in rows:
        counts["attempted"] += 1
        sp = SP(r); sp_active = r["active"]
        rr = rez.resolve_sku(sp, sp_active, panels)
        rec = {"sku_id": f"SP-{r['barcode']}", "barcode": r["barcode"],
               "name_he": r["name_he"], "brand_bucket": r["brand_bucket"],
               "engine_active": sp_active, "price_ils": r.get("price_ils"),
               "resolution": {"matched": rr.matched, "method": rr.method,
                              "source": rr.source, "confidence": rr.confidence,
                              "reason": rr.reason},
               "verification_status": "candidate"}
        if not rr.matched or rr.panel is None:
            counts["unscoreable_no_panel"] += 1
            rec["outcome"] = "unscoreable_no_panel"
            results.append(rec); continue

        acq = methods.get(rr.panel.barcode, "unknown")
        rec["acquisition_method"] = acq
        label, claim_note, lossy = build_label(rec["sku_id"], sp, sp_active, rr.panel)
        if label is None or label.actives[0].quantity is None or not label.actives[0].unit:
            counts["unscoreable_incomplete"] += 1
            rec["outcome"] = "unscoreable_incomplete"; rec["lossy"] = lossy
            results.append(rec); continue

        try:
            sres = score_label(label, load_dossier(sp_active))
        except Exception as e:
            counts["engine_error"] += 1
            rec["outcome"] = "engine_error"; rec["error"] = str(e)
            results.append(rec); continue

        comb = sres["combination"]
        facts = [{"field": f"claims['{sres['claim_matched']}'].evidence_tier",
                  "value": sres["sub_scores"]["evidence"]["tier"],
                  "supp_ev": sres["supp_ev_refs"][0] if sres["supp_ev_refs"] else None}]
        trace = assemble_trace(sres, facts)
        counts["scored"] += 1
        per_method[acq] += 1
        grades[comb["grade"]] += 1
        rec.update({
            "outcome": "scored", "claim_note": claim_note, "lossy": lossy,
            "panel": rr.panel.as_dict(),
            "bsip0s_label": {"product_name": label.product_name,
                             "primary_claim_fed": label.primary_claim,
                             "actives": [vars(a) for a in label.actives]},
            "engine_output": {
                "claim_matched": sres["claim_matched"], "score": comb["final_score"],
                "grade": comb["grade"], "binding_constraint": comb["binding_constraint"],
                "sub_scores": {d: sres["sub_scores"][d]["value"]
                               for d in ["evidence", "dose", "form", "honesty", "safety"]},
                "signature": trace["signature"],
                "caps_vetoes_fired": comb["caps_vetoes_fired"]},
            "trace": trace})
        results.append(rec)
        (SKUDIR / f"{rec['sku_id']}.json").write_text(
            json.dumps(rec, ensure_ascii=False, indent=2), encoding="utf-8")

    out = {"task": "TASK-171 (revival, v3 sprint)",
           "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
           "verification_status": "candidate",
           "edpg_note": "All records candidate; no published score; nothing ships.",
           "sample_n": counts["attempted"], "counts": dict(counts),
           "scoreable_yield_pct": round(100*counts["scored"]/max(1, counts["attempted"]), 1),
           "per_acquisition_method": dict(per_method),
           "grade_distribution": dict(grades), "results": results}
    (HERE / "_corpus_run_v3.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=" * 80)
    print(f"attempted={counts['attempted']} scored={counts['scored']} "
          f"yield={out['scoreable_yield_pct']}%")
    print("counts:", dict(counts))
    print("per_method:", dict(per_method))
    print("grades:", dict(grades))
    for rec in results:
        if rec["outcome"] == "scored":
            e = rec["engine_output"]
            print(f"  {e['grade']:>2}/{e['score']:<5} {rec['engine_active']:<11} "
                  f"[{rec.get('acquisition_method','?'):<12}] {rec['name_he'][:38]}  "
                  f"<-bind:{e['binding_constraint']}")
        else:
            print(f"   ✗      {rec['engine_active']:<11} [{rec['outcome']}] {rec['name_he'][:38]}")


if __name__ == "__main__":
    main()
