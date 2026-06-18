"""TASK-276 — Full addressable shelf run.

Scores all 118 addressable Super-Pharm supplement SKUs through the existing engine
(unchanged). Reads _addressable_shelf.json + cache/*.json; outputs _corpus_run_full.json
and per-SKU skus_full/<sku_id>.json traces.

EDPG: all records candidate. Nothing ships; no published score moves.
Engine at 03_operations/supplement_engine/proto_v0 — DO NOT MODIFY.
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
SKUDIR = HERE / "skus_full"
SKUDIR.mkdir(exist_ok=True)

# Hebrew structure/function -> English umbrella key (same map as v3)
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
    # TASK-277: studied-endpoint strings must be RESOLVABLE claim keys in the dossier umbrella.
    # These paths produce a specific English claim-key that the engine matches against dossier
    # claim entries (NOT the umbrella). Keep as-is: Bug A fix means the over-promise scan on
    # these strings no longer false-fires on 'treatment/prevention' (word-boundary fix).
    "vitamin_d3": [(("חוסר", "מחסור", "השלמ", "רמת", "status", "deficien", "עצם", "סידן"),
                    "correcting/maintaining vitamin D status (raising serum 25(OH)D)")],
    "iron": [(("חוסר", "מחסור", "אנמי", "ברזל", "הריון"), "iron-deficiency anemia treatment/prevention")],
    # TASK-277: expanded folic_acid triggers to catch 'בהיריון' (prefixed), 'היריון' (alt spelling),
    # 'צינור' (neural tube anatomical reference) — all map to the same NTD studied endpoint.
    "folic_acid": [(("הריון", "היריון", "בהיריון", "עובר", "נטית", "neural", "צינור"),
                    "neural tube defect risk reduction (periconceptional)")],
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
        # Skip unscoreable markers — they have no usable panel
        if obj.get("acquisition_method") == "unscoreable":
            continue
        p = panel_from_cache_obj(obj)
        panels.append(p)
        methods[p.barcode] = obj.get("acquisition_method", "unknown")
    return panels, methods


def curate_claim(panel, sp_active=None):
    """Resolve panel primary_claim → engine claim string.

    TASK-277 fix (Item 1 — claim-mapping):
    The old approach translated Hebrew → synthetic English keyword strings
    (e.g. "heart health", "bone health") that partially failed umbrella matching:
    some English umbrella keys worked ("muscle health" → "muscle" survives after
    "health" stripped); others failed when the key was purely generic ("heart health"
    → "heart" is NOT generic but "health" IS stripped — so "heart" survives and
    DOES map for English umbrella keys like "heart").

    Root cause for remaining misses: the dossier umbrella uses BOTH English keys
    (existing) AND Hebrew keys (added TASK-171K). Hebrew keys like "לב", "בהיריון"
    only match if the raw Hebrew claim text is also present. But raw Hebrew alone
    causes REGRESSIONS because Hebrew grammatical prefixes (ה, ו, ל, ב, כ, מ, ש)
    attach directly to words, making tokens like "השרירים" that don't match "שרירים".

    Fix: CONCATENATE raw Hebrew + English translation so that:
    - Hebrew umbrella keys (לב, עצמות, בהיריון, etc.) match from the raw Hebrew portion
    - English umbrella keys (muscle health, nerve health, etc.) match from the translation
    - Grammatical-prefix forms (השרירים) are covered by English translation fallback
    - New Hebrew-only keys (בהיריון, היריון, צינור) are covered by raw Hebrew
    Only truly empty/non-claim labels → UNMAPPED → Insufficient.
    """
    raw = panel.primary_claim or ""
    low = raw.lower()
    # Studied-endpoint path: produce a specific dossier-claim-entry key (English)
    for keys, studied in _STUDIED_HINT.get(sp_active or "", []):
        if any(k in low for k in keys):
            return studied, f"studied endpoint from HE: '{raw[:50]}'"
    # TASK-277: build combined claim = raw Hebrew + English translation.
    # Raw Hebrew hits Hebrew key_tokens directly (לב, בהיריון, etc.)
    # English translation hits English key_tokens and handles grammatical-prefix forms.
    he_hits = [en for he, en in _CLAIM_HINT.items() if he in raw]
    if he_hits:
        en_translation = " ".join(sorted(set(he_hits)))
        # Concatenate: engine tokenizer processes BOTH; union of tokens = union of matches
        combined = raw + " " + en_translation
        return combined, f"HE+EN combined -> umbrella: '{raw[:50]}'"
    if raw:
        # Raw Hebrew only — some dossiers have Hebrew-only umbrella keys (e.g. omega3 הריון)
        return raw, f"raw HE claim -> umbrella will resolve: '{raw[:50]}'"
    return UNMAPPED, "no on-label claim -> Insufficient"


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
    shelf = json.loads((HERE / "_addressable_shelf.json").read_text(encoding="utf-8"))
    rows = shelf["rows"]
    panels, methods = load_panels()
    print(f"loaded {len(panels)} scoreable panels; {len(rows)} addressable shelf SKUs")

    results = []
    counts = collections.Counter()
    per_method = collections.Counter()
    per_brand = collections.Counter()
    per_active = collections.Counter()
    grades = collections.Counter()

    # Track unscoreable barcodes for residue report
    # TASK-277: distinguish premarket (label data disqualified) vs incomplete (data missing/undisclosed)
    # Cache files with 'unscoreable_reason' containing 'name_derived' or 'undisclosed' = incomplete
    unscoreable_barcodes = {}  # barcode -> outcome sub-type
    for fp in sorted(CACHE.glob("*.json")):
        try:
            obj = json.loads(fp.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            continue
        if obj.get("acquisition_method") == "unscoreable":
            bc = obj.get("json", {}).get("barcode") or fp.stem
            reason = obj.get("unscoreable_reason", "")
            # Incomplete = data was name-derived with undisclosed active breakdown
            if "name_derived" in reason or "undisclosed" in reason or "EPA/DHA" in reason:
                unscoreable_barcodes[str(bc)] = "unscoreable_incomplete"
            else:
                unscoreable_barcodes[str(bc)] = "unscoreable_premarket"

    for r in rows:
        counts["attempted"] += 1
        sp = SP(r); sp_active = r["active"]
        brand_bucket = r.get("brand_bucket", "other")

        # Check if barcode is pre-marked unscoreable
        if str(r["barcode"]) in unscoreable_barcodes:
            outcome = unscoreable_barcodes[str(r["barcode"])]
            counts[outcome] += 1
            results.append({
                "sku_id": f"SP-{r['barcode']}", "barcode": r["barcode"],
                "name_he": r["name_he"], "brand_bucket": brand_bucket,
                "engine_active": sp_active, "price_ils": r.get("price_ils"),
                "outcome": outcome,
                "verification_status": "candidate"
            })
            continue

        rr = rez.resolve_sku(sp, sp_active, panels)
        rec = {"sku_id": f"SP-{r['barcode']}", "barcode": r["barcode"],
               "name_he": r["name_he"], "brand_bucket": brand_bucket,
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
        per_brand[brand_bucket] += 1
        per_active[sp_active] += 1
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

    out = {"task": "TASK-277 (SIE calibration re-score — v3, CHANGES_REQUESTED retry)",
           "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
           "verification_status": "candidate",
           "edpg_note": "All records candidate; no published score; nothing ships. TASK-277 v3 adds: primary-claim tier discipline fix in _match_studied_claim (max-specificity overlap + single-letter filter + lowest-tier tiebreaker). Items 2/3/4 preserved from v2.",
           "shelf_n": counts["attempted"], "counts": dict(counts),
           "scoreable_yield_pct": round(100*counts["scored"]/max(1, counts["attempted"]), 1),
           "per_acquisition_method": dict(per_method),
           "per_brand_bucket": dict(per_brand),
           "per_active_slug": dict(per_active),
           "grade_distribution": dict(grades), "results": results}
    (HERE / "_corpus_run_full_v3.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=" * 80)
    print(f"attempted={counts['attempted']} scored={counts['scored']} "
          f"yield={out['scoreable_yield_pct']}%")
    print("counts:", dict(counts))
    print("per_method:", dict(per_method))
    print("per_brand:", dict(per_brand))
    print("per_active:", dict(per_active))
    print("grades:", dict(grades))
    print()
    print("SCORED RESULTS:")
    for rec in sorted(results, key=lambda r: (r.get("engine_output", {}).get("score", 0) or 0), reverse=True):
        if rec["outcome"] == "scored":
            e = rec["engine_output"]
            print(f"  {e['grade']:>2}/{e['score']:<5} {rec['engine_active']:<14} "
                  f"[{rec.get('acquisition_method','?'):<12}] {rec['name_he'][:35]}  "
                  f"<-bind:{e['binding_constraint']}")
    print()
    print("UNSCOREABLE RESIDUE:")
    for rec in results:
        if rec["outcome"] != "scored":
            print(f"   x  {rec['engine_active']:<14} [{rec['outcome']}] {rec['name_he'][:40]}")


if __name__ == "__main__":
    main()
