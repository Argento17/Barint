"""TASK-171 thin-live-proof — score the global-brand real Israeli supplement corpus.

Completes TASK-171D's "thin live proof": the global-brand addressable Super-Pharm SKUs,
scored end-to-end through the real 15-active SIE engine, using the TASK-171G plumbing
(il_prices -> firecrawl iHerb panel -> supplement_bridge -> supplement_label -> engine).

This runner consumes the LIVE results captured THIS SESSION (2026-06-03):
  * step0 derived the global-brand single-active SKUs from the LIVE Super-Pharm catalog
    (derive_global_brand_skus.py -> global_brand_skus.json),
  * each SKU's CURRENT iHerb URL was resolved via firecrawl_search (NOT a hardcoded id),
  * the panel was extracted live via firecrawl_scrape(json) with the BSIP0-S schema,
  * the barcode was verified against the Super-Pharm SKU BEFORE the page was trusted.

The live firecrawl panels are embedded below as LIVE_PANELS (exactly what firecrawl
returned this session). The pipeline then bridges (barcode-first), assembles the BSIP0-S
label INCLUDING the on-label primary claim, and scores through the engine.

EDPG: every record verification_status=candidate / should_affect_score_now=false.
Nothing ships. No engine/dossier edit. Missing fields are recorded, never fabricated.
"""
import sys, json, pathlib, datetime

ROOT = r"C:\Bari"
ENGINE = pathlib.Path(ROOT) / "03_operations" / "supplement_engine" / "proto_v0"
sys.path.insert(0, ROOT)
sys.path.insert(0, str(ENGINE / "src"))
sys.path.insert(0, str(ENGINE))

from integrations.clients.iherb_panel import _coerce, IherbPanel          # noqa: E402
from integrations.clients import supplement_bridge as br                  # noqa: E402
from supplement_label import SupplementLabel, LabelActive                 # noqa: E402
from score_engine import score_label                                      # noqa: E402
from dossier_loader import load_dossier                                   # noqa: E402
from trace_writer import assemble_trace                                   # noqa: E402

OUT = pathlib.Path(__file__).resolve().parent
FETCHED_AT = "2026-06-03T00:00:00Z"
CLIENT = "firecrawl_scrape(json)/live-2026-06-03 + iHerb PDP"

# ---------------------------------------------------------------------------
# The LIVE firecrawl results captured this session, per derived global-brand SKU.
# `sp` = the Super-Pharm Israeli-shelf identity (from global_brand_skus.json).
# `iherb_url` = the CURRENT URL resolved via firecrawl_search this session.
# `panel` = EXACTLY what firecrawl_scrape(json) returned for that URL this session.
# `iherb_barcode` is carried in the panel; the bridge verifies it against sp.barcode.
# A SKU with no exact-pack iHerb match is recorded matched=False (honest 'not found').
# ---------------------------------------------------------------------------
SKUS = [
    # 1) Solgar Biotin 1000mcg / 50ct  — SP barcode 0033984003101.
    #    iHerb carries Solgar Biotin 1000mcg only in 100ct (...003118) & 250ct (...003125),
    #    and 50ct only at 5000mcg (...003132). NO exact 1000mcg/50ct on iHerb -> NO barcode
    #    bridge. Recorded honest 'not found'; not force-scored on a wrong-pack/wrong-dose panel.
    dict(
        sp=dict(barcode="0033984003101", name="סולגר ביוטין 1000 מק\"ג 50 כמוסות",
                manufacturer="אמברוזיה/סולגר", price=None, active_slug="biotin"),
        iherb_url=None,
        resolve_status="no_exact_pack_on_iherb",
        resolve_note=("iHerb Solgar Biotin 1000mcg = 100ct(...003118)/250ct(...003125); "
                      "50ct only at 5000mcg(...003132). The IL 1000mcg/50ct(...003101) pack "
                      "is not on iHerb US. Verified by scraping all 3 candidate barcodes; "
                      "none == ...003101. Honest miss, not forced."),
        panel=None,
    ),
    # 2) Solgar Zinc lozenge 22mg / 50  — SP barcode 0033984010642.
    #    iHerb Solgar 22mg zinc = Picolinate tablet(...037250) & Chelated tablet(...008007),
    #    both 100ct tablets, neither a 50ct lozenge, neither barcode == ...010642. NO bridge.
    dict(
        sp=dict(barcode="0033984010642", name="סולגר אבץ מציצה22מ\"ג50טבליות",
                manufacturer="אמברוזיה/סולגר", price=None, active_slug="zinc"),
        iherb_url=None,
        resolve_status="no_exact_pack_on_iherb",
        resolve_note=("IL SKU is a 22mg zinc LOZENGE x50 (...010642). iHerb Solgar 22mg zinc "
                      "is Picolinate(...037250) & Chelated(...008007) TABLETS x100 — different "
                      "form/pack, neither barcode matches. Honest miss, not forced."),
        panel=None,
    ),
    # 3) Solgar Omega-3 950mg / 100 softgels — SP barcode 0033984020580.
    #    LIVE firecrawl: iHerb /pr/.../26738 barcode 033984020580 == SP (GTIN12/13). CLEAN bridge.
    dict(
        sp=dict(barcode="0033984020580", name="סולגאר אומגה 950 100 כמוסות",
                manufacturer="אמברוזיה/סולגר", price=None, active_slug="omega3"),
        iherb_url="https://www.iherb.com/pr/solgar-omega-3-epa-dha-triple-strength-950-mg-100-softgels/26738",
        resolve_status="barcode_match",
        resolve_note="iHerb panel barcode 033984020580 == SP 0033984020580 (exact GTIN12/13).",
        panel=dict(
            brand="Solgar", product_name="Omega 3, EPA & DHA, Triple Strength",
            barcode_upc="033984020580", serving_size="1 softgel",
            servings_per_container="100", proprietary_blend=False,
            primary_on_label_claim="Heart Healthy",
            actives=[
                {"ingredient": "EPA (eicosapentaenoic acid)", "amount": 504, "unit": "mg", "form": "ethyl ester"},
                {"ingredient": "DHA (docosahexaenoic acid)", "amount": 378, "unit": "mg", "form": "ethyl ester"},
            ],
        ),
        # the dossier scored active is COMBINED EPA+DHA; sum the two rows (504+378=882 mg).
        scored_active=dict(ingredient="EPA+DHA (combined)", amount=882, unit="mg", form="ethyl ester"),
        # on-label claim "Heart Healthy" -> the dossier's CV endpoint (truthful; broad CV).
        primary_claim_fed="cardiovascular disease / CV events prevention",
        servings_per_day=2.0,  # label: 1 softgel twice daily
    ),
    # 4) Solgar Zinc Picolinate 22mg / 100 tablets — SP barcode 0033984037250.
    #    LIVE firecrawl: iHerb /pr/.../10035 barcode 033984037250 == SP. CLEAN bridge.
    dict(
        sp=dict(barcode="0033984037250", name="סולגר אבץ פיקולינט100 טבליות",
                manufacturer="אמברוזיה/סולגר", price=None, active_slug="zinc"),
        iherb_url="https://www.iherb.com/pr/solgar-zinc-picolinate-22-mg-100-tablets/10035",
        resolve_status="barcode_match",
        resolve_note="iHerb panel barcode 033984037250 == SP 0033984037250 (exact GTIN12/13).",
        panel=dict(
            brand="Solgar", product_name="Zinc Picolinate",
            barcode_upc="033984037250", serving_size="1 Tablet",
            servings_per_container="100", proprietary_blend=False,
            primary_on_label_claim="Immune support; antioxidant support",
            actives=[
                {"ingredient": "Zinc (as zinc picolinate)", "amount": 22, "unit": "mg", "form": "Zinc Picolinate"},
            ],
        ),
        scored_active=dict(ingredient="Zinc (as zinc picolinate)", amount=22, unit="mg", form="zinc picolinate"),
        primary_claim_fed="immune support",
        servings_per_day=1.0,
    ),
]


def prov(url, status, note):
    return {
        "source": "iherb.com" if url else "super_pharm (no iHerb match)",
        "source_url": url,
        "fetched_at": FETCHED_AT,
        "client_version": CLIENT,
        "verification_status": "candidate",
        "should_affect_score_now": False,
        "resolve_status": status,
        "resolve_note": note,
        "admission_note": ("candidate only; live thin-proof of acquisition->engine reach; "
                           "no BSIP0/QA pass; does NOT move any published score."),
    }


def make_panel(rec) -> IherbPanel | None:
    """Re-coerce the LIVE firecrawl dict through the REAL iherb_panel._coerce so lossiness
    is recorded by the production code path (not hand-curated)."""
    if not rec.get("panel"):
        return None
    return _coerce({"json": rec["panel"]}, rec["iherb_url"], source_id=rec["iherb_url"])


def run():
    records, summary = [], []
    n_attempt = len(SKUS)
    n_url_resolved = n_panel_ok = n_bridged = n_scored = 0

    for rec in SKUS:
        sp = rec["sp"]
        sku_id = f"REAL-IL-{sp['active_slug'].upper()}-SOLGAR-{br.normalize_barcode(sp['barcode'])}"
        panel = make_panel(rec)
        url_ok = bool(rec.get("iherb_url"))
        panel_ok = bool(panel and panel.actives)
        n_url_resolved += int(url_ok)
        n_panel_ok += int(panel_ok)

        # --- bridge (barcode-first) against the resolved panel -----------------
        sp_obj = type("SP", (), dict(barcode=sp["barcode"], name=sp["name"],
                                     manufacturer=sp["manufacturer"], price=sp["price"],
                                     provenance=None))()
        if panel_ok:
            match = br.bridge_one(sp_obj, [panel])
        else:
            match = br.MatchResult(sp["barcode"], sp["name"], False, "none", 0.0,
                                   notes=rec["resolve_note"])
        bridged = bool(match.matched and match.method == "barcode")
        n_bridged += int(bridged)

        engine_output = trace = None
        bsip0s = None
        if bridged:
            # --- assemble BSIP0-S label (incl. the on-label primary claim) -----
            sa = rec["scored_active"]
            label = SupplementLabel(
                sku_id=sku_id,
                product_name=panel.product_name or sp["name"],
                primary_claim=rec["primary_claim_fed"],      # on-label claim, curated to dossier endpoint
                servings_per_day=rec.get("servings_per_day", 1.0),
                labeled_regimen="daily",
                actives=[LabelActive(active_slug=sp["active_slug"],
                                     display_name=sa["ingredient"], quantity=sa["amount"],
                                     unit=sa["unit"], form=sa["form"], is_core=True)],
            )
            dossier = load_dossier(sp["active_slug"])
            result = score_label(label, dossier)
            comb = result["combination"]
            cm = result["claim_matched"]
            facts = [{"field": f"claims['{cm}'].evidence_tier",
                      "value": result["sub_scores"]["evidence"]["tier"],
                      "supp_ev": result["supp_ev_refs"][0] if result["supp_ev_refs"] else None}]
            trace = assemble_trace(result, facts)
            engine_output = {
                "claim_matched": cm,
                "primary_on_label_claim_raw": panel.primary_claim,
                "score": comb["final_score"], "grade": comb["grade"], "blend": comb["blend"],
                "binding_constraint": comb["binding_constraint"],
                "sub_scores": {d: result["sub_scores"][d]["value"] for d in
                               ["evidence", "dose", "form", "honesty", "safety"]},
                "signature": trace["signature"],
                "caps_vetoes_fired": comb["caps_vetoes_fired"],
            }
            bsip0s = {
                "product_name": label.product_name,
                "primary_claim_raw_on_label": panel.primary_claim,
                "primary_claim_fed_to_engine": label.primary_claim,
                "actives": [vars(a) for a in label.actives],
                "servings_per_day": label.servings_per_day,
            }
            n_scored += 1
            summary.append((sku_id, dossier["canonical_name"], comb["final_score"],
                            comb["grade"], comb["binding_constraint"]["mechanism"], cm))
        else:
            summary.append((sku_id, sp["active_slug"], None, None,
                            rec["resolve_status"], None))

        out = {
            "sku_id": sku_id,
            "verification_status": "candidate",
            "should_affect_score_now": False,
            "israeli_shelf": {  # Super-Pharm = local-shelf integrity control
                "barcode": sp["barcode"], "name_he": sp["name"],
                "brand": "Solgar (global)", "importer": sp["manufacturer"],
                "price_ils": sp["price"], "chain": "super_pharm", "active_slug": sp["active_slug"],
            },
            "iherb_resolution": {
                "url": rec.get("iherb_url"),
                "resolve_status": rec["resolve_status"],
                "note": rec["resolve_note"],
                "url_resolved": url_ok, "panel_extracted": panel_ok,
            },
            "panel": (panel.as_dict() if panel else None),
            "bridge": {"matched": match.matched, "method": match.method,
                       "confidence": match.confidence, "ambiguous": match.ambiguous,
                       "notes": match.notes},
            "bsip0s_label": bsip0s,
            "engine_output": engine_output,
            "missing_or_lossy_fields": (panel.missing_fields if panel else ["no panel matched"]),
            "trace": trace,
            "provenance": prov(rec.get("iherb_url"), rec["resolve_status"], rec["resolve_note"]),
        }
        records.append(out)
        (OUT / f"{sku_id}.json").write_text(
            json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

    rates = {
        "global_brand_skus_attempted": n_attempt,
        "iherb_url_resolved": f"{n_url_resolved}/{n_attempt}",
        "panel_extracted": f"{n_panel_ok}/{n_attempt}",
        "barcode_bridge_matched": f"{n_bridged}/{n_attempt}",
        "scored_end_to_end": f"{n_scored}/{n_attempt}",
    }
    idx = {
        "task": "TASK-171 thin-live-proof (global-brand real IL supplement corpus)",
        "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
        "verification_status": "candidate",
        "should_affect_score_now": False,
        "edpg_note": ("All SKUs candidate; engine outputs are a LIVE proof of the "
                      "acquisition->engine pipeline, NOT authoritative, NOT admitted to any "
                      "published score. No engine/dossier edits."),
        "engine": "03_operations/supplement_engine/proto_v0 (unchanged)",
        "source": "Super-Pharm PriceFull (live) + iHerb PDPs via firecrawl (live 2026-06-03)",
        "measured_rates": rates,
        "skus": [r["sku_id"] for r in records],
    }
    (OUT / "_index.json").write_text(json.dumps(idx, ensure_ascii=False, indent=2),
                                     encoding="utf-8")

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print("=" * 104)
    print("TASK-171 THIN LIVE PROOF — global-brand real IL supplement corpus (ALL candidate)")
    print("=" * 104)
    print(f"{'sku':<46}{'active':<22}{'score':>6}{'grd':>4}  binding/status")
    print("-" * 104)
    for sid, act, sc, gr, bind, cm in summary:
        scs = f"{sc:>6}" if sc is not None else f"{'—':>6}"
        grs = f"{gr:>4}" if gr else f"{'—':>4}"
        print(f"{sid:<46}{act:<22}{scs}{grs}  {bind}")
    print("-" * 104)
    for k, v in rates.items():
        print(f"  {k:<32}{v}")
    print("=" * 104)
    return idx, rates, summary


if __name__ == "__main__":
    run()
