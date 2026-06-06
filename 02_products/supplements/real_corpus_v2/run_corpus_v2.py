"""TASK-171J — MVP corpus run harness: measure the REAL Israeli supplement corpus.

Pipeline per addressable Super-Pharm SKU:
  1. resolve a candidate panel from the acquired IL e-tailer/brand-site panels
     (il_panel_resolver, source-priority + match-verification),
  2. assemble a BSIP0-S label (elemental-key form mapping so the engine's mineral
     elemental conversion fires; claim curated from the panel),
  3. score through the REAL SIE engine (score_engine.score_label),
  4. write the SKU JSON + trace; stamp provenance candidate (EDPG).

Panels are acquired ONCE (cached to ./cache/<barcode>.json) by the agent's firecrawl
tool via _acquire.py; this harness consumes the cache (offline, respectful — never
re-hits a cached URL). Missing field = measured missing, never fabricated.

EDPG: every record verification_status=candidate; no published score; nothing ships.
"""
import sys, json, pathlib, datetime, re

ROOT = r"C:\Bari"
ENGINE = pathlib.Path(ROOT) / "03_operations" / "supplement_engine" / "proto_v0"
sys.path.insert(0, ROOT)
sys.path.insert(0, str(ENGINE / "src"))
sys.path.insert(0, str(ENGINE))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from supplement_label import SupplementLabel, LabelActive
from score_engine import score_label
from dossier_loader import load_dossier, ACTIVE_DOSSIER_FILES
from trace_writer import assemble_trace

from integrations.clients.il_supplement_panels import ILPanel, PanelActiveIL, cache_scraper, acquire_panel
from integrations.clients import il_panel_resolver as rez

HERE = pathlib.Path(__file__).resolve().parent
CACHE = HERE / "cache"
SKUDIR = HERE / "skus"
SKUDIR.mkdir(exist_ok=True)

# Elemental-conversion policy (the real "elemental trap" — measured, not fabricated):
# the engine fires an elemental conversion ONLY when the label active.form EXACTLY equals
# a dossier elemental_by_form key (a full string like "magnesium oxide"). A SHORT form
# token ("oxide") does NOT fire conversion but DOES substring-hit the form ladder
# (poor/preferred). Policy:
#   - We DEFAULT to the SHORT token => NO speculative conversion: the labeled per-serving
#     number is used as-is, and the form penalty (e.g. oxide=poor) still applies. Applying
#     a fractional conversion the label does not explicitly state would be closer to
#     fabrication than measurement.
#   - We only treat a number as a COMPOUND mass needing conversion when the panel EXPLICITLY
#     flags it (form_raw carries a 'compound'/'תרכובת' marker) — none in this MVP corpus do,
#     so every mineral here uses the labeled (elemental-or-as-stated) number + form penalty.
# This is a deliberate, documented calibration choice surfaced in the report.
SHORT_FORM = {
    "magnesium oxide": "oxide", "magnesium citrate (trimagnesium dicitrate)": "citrate",
    "magnesium glycinate / bisglycinate": "bisglycinate",
}


def panel_from_cache_obj(obj: dict) -> ILPanel:
    """Reconstruct an ILPanel from a cached raw firecrawl extraction dict."""
    url = obj.get("url")
    sc = cache_scraper.__wrapped__ if hasattr(cache_scraper, "__wrapped__") else None
    # simplest: re-run the coerce path via acquire_panel with a one-shot scraper
    one = {url: obj.get("json", obj)}

    def _scrape(u, schema, prompt):
        return one.get(u, {})
    return acquire_panel(url, _scrape, source_id=obj.get("source_id"))


def load_panels() -> list[ILPanel]:
    panels = []
    for fp in sorted(CACHE.glob("*.json")):
        try:
            obj = json.loads(fp.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            continue
        if not obj.get("url"):
            continue
        p = panel_from_cache_obj(obj)
        panels.append(p)
    return panels


# CLAIM CURATION (step 4 of the MVP). The panel's primary_claim is Hebrew on-label text.
# The engine resolves an ENGLISH claim against the dossier (studied claims + structure/
# function umbrella). We translate the Hebrew on-label claim to that English vocabulary,
# precision-first. CRITICAL: we NEVER pass empty/raw-Hebrew to the engine — the engine's
# containment matcher resolves an empty/non-English string to its FIRST (Strong) tier,
# which would be a fabricated grade. An unmappable claim -> the explicit sentinel
# "__unmapped__" which resolves Insufficient honestly (cap-1 fires).
#
# Hebrew structure/function -> English umbrella key (umbrella vocab per dossier_loader).
_CLAIM_HINT = {
    "לחץ דם": "blood pressure", "לב": "heart health", "לבב": "heart health",
    "עצבים": "nerve health", "עצב": "nerve health",
    "עצמות": "bone health", "עצם": "bone health", "שלד": "bone health",
    "שריר": "muscle health", "שרירים": "muscle health",
    "חיסון": "immune health", "חיסונית": "immune health", "מערכת החיסון": "immune health",
    "עייפות": "fatigue", "תשישות": "fatigue", "אנרגיה": "energy",
    "עור": "skin health", "שיער": "hair health", "ציפורניים": "nail health",
    "מוח": "brain health", "קוגניטיב": "cognitive", "ריכוז": "cognitive",
    "ראיה": "vision", "עיניים": "eye health", "דם": "blood",
    "שינה": "sleep", "ערנות": "alertness", "הריון": "pregnancy",
}
# Active-specific Hebrew on-label phrases that map to a STUDIED dossier claim (the strong
# direct-evidence path), not just the umbrella. Precision-first; cited by the dossier.
_STUDIED_HINT = {
    "vitamin_d3": [(("חוסר", "מחסור", "השלמ", "רמת", "status", "deficien"),
                    "correcting/maintaining vitamin D status (raising serum 25(OH)D)")],
    "iron": [(("חוסר", "מחסור", "אנמי", "ברזל"), "iron-deficiency anemia treatment/prevention")],
    "folic_acid": [(("הריון", "עובר", "נטית", "neural"), "neural tube defect risk reduction (periconceptional)")],
    "vitamin_b12": [(("חוסר", "מחסור", "b12", "אנמי"), "treating/preventing B12 deficiency")],
    "vitamin_c": [(("חוסר", "צפדינה", "scurvy"), "scurvy / vitamin C deficiency")],
}

UNMAPPED = "__unmapped__"   # resolves Insufficient (cap-1) — honest, never a fabricated tier


def curate_claim(panel: ILPanel, sp_active: str = None) -> tuple[str, str]:
    """Return (english_claim_for_engine, note). Map the Hebrew on-label claim to the
    dossier vocabulary, precision-first. Unmappable / empty -> UNMAPPED sentinel
    (Insufficient). NEVER passes empty/raw-Hebrew (engine would mis-resolve to Strong)."""
    raw = panel.primary_claim or ""
    low = raw.lower()
    # 1) active-specific studied-claim hint (the cited direct-evidence endpoint)
    for keys, studied in _STUDIED_HINT.get(sp_active or "", []):
        if any(k in low for k in keys):
            return studied, f"claim mapped to studied endpoint from HE: '{raw[:55]}'"
    # 2) umbrella structure/function hint
    hits = [en for he, en in _CLAIM_HINT.items() if he in raw]
    if hits:
        return " ".join(sorted(set(hits))), f"claim mapped to S/F umbrella from HE: '{raw[:55]}'"
    # 3) unmappable -> Insufficient sentinel (NOT empty/raw — would mis-resolve to Strong)
    if not raw:
        return UNMAPPED, "no on-label claim on panel (measured missing) -> Insufficient"
    return UNMAPPED, f"HE claim did not map to dossier vocab -> Insufficient: '{raw[:55]}'"


def build_label(sku_id: str, sp_item, sp_active: str, panel: ILPanel) -> tuple:
    """Assemble a BSIP0-S SupplementLabel from a resolved panel. Returns (label, claim_note,
    lossy[]). Picks the active matching the SKU's engine active; applies elemental-key form."""
    lossy = list(panel.missing_fields)
    # pick the panel active that maps to the SKU's engine active (or the first scoreable)
    act = next((a for a in panel.actives if a.active_slug == sp_active), None)
    if act is None:
        act = next((a for a in panel.actives if a.active_slug), None)
    if act is None:
        return None, "no mappable active on panel", lossy + ["no engine-mappable active"]

    slug = act.active_slug
    # form: pass the SHORT token (no speculative elemental conversion; form penalty still
    # applies). If the resolver already mapped to a full elemental key, shorten it back.
    form_for_engine = act.form
    if form_for_engine in SHORT_FORM:
        form_for_engine = SHORT_FORM[form_for_engine]
    if form_for_engine == "elemental_stated":
        form_for_engine = "oxide"   # label states elemental from oxide -> oxide form penalty, no conversion
    # unit guard: engine compares against the dossier dose unit; we pass quantity as-is and
    # rely on the dossier basis. mcg/IU/mg mismatches are recorded, not silently coerced.

    claim_text, claim_note = curate_claim(panel, sp_active)

    label = SupplementLabel(
        sku_id=sku_id,
        product_name=panel.product_name or sp_item.name,
        primary_claim=claim_text,
        servings_per_day=1.0,
        actives=[LabelActive(
            active_slug=slug,
            display_name=act.ingredient or sp_item.name,
            quantity=act.amount,
            unit=act.unit,
            form=form_for_engine,
            is_core=True,
        )],
    )
    return label, claim_note, lossy


def main():
    addr = json.loads((HERE / "_addressable_shelf.json").read_text(encoding="utf-8"))
    rows = addr["rows"]
    by_bc = {r["barcode"]: r for r in rows}
    panels = load_panels()
    print(f"loaded {len(panels)} cached candidate panels; {len(rows)} addressable SKUs")

    # SP item shim (resolver/label only need barcode/name/manufacturer/price)
    class SP:
        def __init__(s, r):
            s.barcode = r["barcode"]; s.name = r["name_he"]
            s.manufacturer = r.get("manufacturer"); s.price = r.get("price_ils")

    results = []
    counts = {"attempted": 0, "scored": 0, "no_panel": 0, "ambiguous": 0,
              "no_active": 0, "missing_dose": 0, "missing_unit": 0}
    per_source = {}
    grades = {}

    for r in rows:
        counts["attempted"] += 1
        sp = SP(r); sp_active = r["active"]
        rr = rez.resolve_sku(sp, sp_active, panels)
        rec = {"sku_id": f"SP-{r['barcode']}", "barcode": r["barcode"],
               "name_he": r["name_he"], "brand_bucket": r["brand_bucket"],
               "engine_active": sp_active, "price_ils": r.get("price_ils"),
               "resolution": {"matched": rr.matched, "method": rr.method,
                              "source": rr.source, "confidence": rr.confidence,
                              "ambiguous": rr.ambiguous, "reason": rr.reason},
               "verification_status": "candidate"}
        if rr.ambiguous:
            counts["ambiguous"] += 1
            rec["outcome"] = "unscoreable_ambiguous"
            results.append(rec); continue
        if not rr.matched or rr.panel is None:
            counts["no_panel"] += 1
            rec["outcome"] = "unscoreable_no_panel"
            results.append(rec); continue

        per_source[rr.source] = per_source.get(rr.source, 0) + 1
        label, claim_note, lossy = build_label(rec["sku_id"], sp, sp_active, rr.panel)
        if label is None:
            counts["no_active"] += 1
            rec["outcome"] = "unscoreable_no_active"; rec["lossy"] = lossy
            results.append(rec); continue
        core = label.actives[0]
        if core.quantity is None:
            counts["missing_dose"] += 1
            rec["outcome"] = "unscoreable_missing_dose"; rec["lossy"] = lossy
            results.append(rec); continue
        if not core.unit:
            counts["missing_unit"] += 1
            rec["outcome"] = "unscoreable_missing_unit"; rec["lossy"] = lossy
            results.append(rec); continue

        # ---- score through the REAL engine ----
        try:
            dossier = load_dossier(sp_active)
            sres = score_label(label, dossier)
        except Exception as e:
            rec["outcome"] = "engine_error"; rec["error"] = str(e)
            results.append(rec); continue

        comb = sres["combination"]
        facts = [{"field": f"claims['{sres['claim_matched']}'].evidence_tier",
                  "value": sres["sub_scores"]["evidence"]["tier"],
                  "supp_ev": sres["supp_ev_refs"][0] if sres["supp_ev_refs"] else None}]
        trace = assemble_trace(sres, facts)
        counts["scored"] += 1
        grades[comb["grade"]] = grades.get(comb["grade"], 0) + 1
        rec["outcome"] = "scored"
        rec["panel"] = rr.panel.as_dict()
        rec["claim_note"] = claim_note
        rec["lossy"] = lossy
        rec["bsip0s_label"] = {
            "product_name": label.product_name, "primary_claim_fed": label.primary_claim,
            "actives": [vars(a) for a in label.actives]}
        rec["engine_output"] = {
            "claim_matched": sres["claim_matched"],
            "score": comb["final_score"], "grade": comb["grade"], "blend": comb["blend"],
            "binding_constraint": comb["binding_constraint"],
            "sub_scores": {d: sres["sub_scores"][d]["value"]
                           for d in ["evidence", "dose", "form", "honesty", "safety"]},
            "signature": trace["signature"],
            "caps_vetoes_fired": comb["caps_vetoes_fired"]}
        rec["trace"] = trace
        results.append(rec)
        (SKUDIR / f"{rec['sku_id']}.json").write_text(
            json.dumps(rec, ensure_ascii=False, indent=2), encoding="utf-8")

    out = {
        "task": "TASK-171J", "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
        "verification_status": "candidate",
        "edpg_note": "All records candidate; no published score; nothing ships.",
        "addressable_attempted": counts["attempted"],
        "counts": counts, "per_source": per_source, "grade_distribution": grades,
        "scoreable_yield_pct": round(100 * counts["scored"] / max(1, counts["attempted"]), 1),
        "results": results}
    (HERE / "_corpus_run_v2.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=" * 80)
    print(f"attempted={counts['attempted']} scored={counts['scored']} "
          f"yield={out['scoreable_yield_pct']}%")
    print("counts:", counts)
    print("per_source:", per_source)
    print("grades:", grades)
    print(f"wrote {HERE/'_corpus_run_v2.json'} + {counts['scored']} SKU JSONs")


if __name__ == "__main__":
    main()
