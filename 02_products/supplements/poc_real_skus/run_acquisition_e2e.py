"""TASK-171G — End-to-end acquisition-layer test.

Proves the catalog -> panel -> assembled-BSIP0-S-label plumbing on a small live sample:
  1. read the LIVE Super-Pharm supplement catalog (il_prices.fetch_super_pharm_supplements),
  2. extract the 5 real PoC iHerb panels (iherb_panel.extract_panel + poc_fixture_scraper —
     the same panels the Phase-3 probe pulled live 2026-06-03),
  3. bridge each Super-Pharm SKU <-> panel (supplement_bridge), barcode-first then name,
  4. report the real match rate, lossy fields, and the assembled candidate labels.

EDPG: every record verification_status=candidate; nothing admitted to a published score.
"""
import json
import pathlib
import sys

sys.path.insert(0, r"C:\Bari")

from integrations.clients.il_prices import fetch_super_pharm_supplements
from integrations.clients.iherb_panel import extract_panel, poc_fixture_scraper
from integrations.clients import supplement_bridge as br

OUT = pathlib.Path(__file__).resolve().parent

# The 5 PoC iHerb PDP URLs + source ids (the actives the engine can score today).
POC_URLS = [
    ("https://www.iherb.com/pr/california-gold-nutrition-sport-pure-creatine-monohydrate-unflavored-0-18-oz-5-g/149273", "iherb:149273"),
    ("https://www.iherb.com/pr/california-gold-nutrition-magnesium-bisglycinate-chelate-albion-traacs-60-veggie-capsules-100-mg-per-capsule/103273", "iherb:103273"),
    ("https://www.iherb.com/pr/country-life-vitamin-d3-125-mcg-5-000-lu-365-softgels/141067", "iherb:141067"),
    ("https://www.iherb.com/pr/allmax-essentials-caffeine-200-mg-100-tablets/67652", "iherb:67652"),
    ("https://www.iherb.com/pr/now-foods-omega-3-fish-oil-1-000-mg-180-epa-120-dha-100-softgels/102333", "iherb:102333"),
]


def run():
    print("=" * 92)
    print("TASK-171G acquisition-layer E2E  (ALL candidate / EDPG — nothing admitted)")
    print("=" * 92)

    # --- step 1: live Super-Pharm supplement catalog -----------------------------------
    catalog = fetch_super_pharm_supplements()
    print(f"[1] Super-Pharm LIVE supplement catalog: {len(catalog)} oral-supplement SKUs "
          f"(barcode+name+brand+price, identity-only)")

    # --- step 2: extract the 5 PoC iHerb panels ----------------------------------------
    scraper = poc_fixture_scraper()
    panels = []
    panel_ok = 0
    for url, sid in POC_URLS:
        p = extract_panel(url, scraper, source_id=sid)
        got = bool(p.actives) and bool(p.product_name)
        panel_ok += int(got)
        panels.append(p)
        print(f"[2] panel {sid:<16} extracted={'Y' if got else 'N'} "
              f"actives={len(p.actives)} lossy={len(p.missing_fields)} "
              f"barcode={p.barcode}")
    print(f"    panel-extract success: {panel_ok}/{len(POC_URLS)}")

    # --- step 3: bridge each panel against the live catalog ----------------------------
    # For the panel-centric test we ask: for each iHerb panel, does a Super-Pharm SKU on
    # the live Israeli shelf carry it? (barcode-first; then brand+dose name match)
    assembled = []
    matched = 0
    for p in panels:
        # build a pseudo SP-side search by scanning the live catalog for a barcode or
        # brand+dose match to THIS panel (the bridge is symmetric — reuse bridge_one by
        # treating each catalog item as the SP side and this single panel as the pool).
        best = None
        for sp in catalog:
            m = br.bridge_one(sp, [p])
            if m.matched and (best is None or m.confidence > best[1].confidence):
                best = (sp, m)
        if best:
            sp, m = best
            matched += 1
            lbl = br.assemble_label(sp, m, sku_id=f"SP-{br.normalize_barcode(sp.barcode)}")
            assembled.append(lbl)
            print(f"[3] panel {p.provenance.source_id:<16} -> MATCH via {m.method} "
                  f"conf={m.confidence}  SP='{sp.name[:40]}'  price={sp.price}")
        else:
            # no Israeli-shelf SKU carries this exact panel — honest 'not found'
            lbl = br.assemble_label(
                type("X", (), {"barcode": p.barcode, "name": p.product_name,
                               "manufacturer": p.brand, "price": None, "provenance": None})(),
                br.MatchResult(p.barcode, p.product_name or "", False, "none", 0.0,
                               panel=p, notes="no Super-Pharm shelf SKU carries this panel"),
                sku_id=p.provenance.source_id)
            assembled.append(lbl)
            print(f"[3] panel {p.provenance.source_id:<16} -> NO Israeli-shelf SKU "
                  f"(iHerb ships-to-IL != on Super-Pharm shelf)")

    # --- step 4: report -----------------------------------------------------------------
    rate = matched / len(panels) if panels else 0.0
    print("-" * 92)
    print(f"[4] barcode-bridge match rate (PoC panels found on Super-Pharm shelf): "
          f"{matched}/{len(panels)} = {rate:.0%}")

    out = {
        "task": "TASK-171G",
        "verification_status": "candidate",
        "edpg_note": "All records candidate; nothing admitted to a published score.",
        "live_super_pharm_supplement_skus": len(catalog),
        "poc_panels": len(panels),
        "panel_extract_success": f"{panel_ok}/{len(POC_URLS)}",
        "barcode_bridge_matched": matched,
        "barcode_bridge_match_rate": round(rate, 3),
        "assembled_labels": assembled,
    }
    (OUT / "acquisition_e2e_result.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"    wrote {OUT / 'acquisition_e2e_result.json'}")
    return out


if __name__ == "__main__":
    run()
