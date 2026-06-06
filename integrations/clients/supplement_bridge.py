"""Catalog<->panel barcode/name bridge  (TASK-171G, parent TASK-171).

The integrity control of the Israeli-supplement acquisition layer. Super-Pharm's
price-transparency feed gives the *Israeli-shelf identity + price* (barcode, Hebrew name,
brand, price) but NO panel. iHerb gives a *panel* (active·dose·form·claim·blend) but is a
ships-to-IL catalog, not the Israeli shelf. "ships-to-IL" != "on the Israeli shelf" — so
a panel is only admissible against a Super-Pharm SKU that actually sits on the local
shelf. This module bridges the two:

  1. BARCODE-FIRST. EAN/UPC match (with the common GTIN-12<->GTIN-13 leading-zero shift).
     A barcode hit is a strong, near-unambiguous match.
  2. NORMALIZED BRAND + NAME fallback. When barcodes differ (IL SKU vs iHerb US SKU),
     fall back to a token-overlap score on transliterated brand + active + dose. Records
     a confidence; flags ambiguous (multiple near-ties) rather than guessing.

It then assembles a BSIP0-S `SupplementLabel` (Super-Pharm = Israeli-shelf identity/price;
iHerb = the scored panel) carrying BOTH provenance stamps. Everything is
`verification_status="candidate"` (EDPG). Nothing is admitted to a published score — the
assembled label must still clear BSIP0/QA to be promoted, and claim selection (§2.1)
remains a Nutrition curation step, not a scrape.
"""
from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from typing import Optional

from .iherb_panel import IherbPanel

# Brand transliteration: Hebrew (Super-Pharm) <-> Latin (iHerb). Small, explicit, and
# only for brands present on both shelves — never a fuzzy guess on a brand we don't know.
BRAND_XLIT = {
    "סולגאר": "solgar", "סולגר": "solgar",
    "אלטמן": "altman",
    "סופהרב": "supherb", "סאפ הרב": "supherb",
    "נאוו": "now", "נאו פודס": "now foods", "now foods": "now",
    "קליפורניה גולד": "california gold nutrition", "קליפורניה גולד נוטרישן": "california gold nutrition",
    "קאנטרי לייף": "country life",
    "אולמקס": "allmax", "אלמקס": "allmax",
    "דוקטור'ס בست": "doctor's best", "דוקטורס בست": "doctor's best",
    "ג'ארו": "jarrow", "נייצ'רס באונטי": "nature's bounty",
}

_DOSE = re.compile(r"(\d+(?:[.,]\d+)?)\s*(mg|mcg|g|iu|מ\"?ג|מק\"?ג|גרם|יחב\"?ל)", re.I)
_STOP = {"the", "of", "and", "for", "with", "a", "an", "תוסף", "תזונה", "כמוסות",
         "טבליות", "קפסולות", "כמוסה", "טבליה", "yc", "יח", "מל", "ml"}


def normalize_barcode(bc: str | None) -> str | None:
    if not bc:
        return None
    d = re.sub(r"\D", "", str(bc))
    return d or None


def barcodes_match(a: str | None, b: str | None) -> bool:
    """EAN/UPC equality tolerant of the GTIN-12<->GTIN-13 leading-zero shift."""
    a, b = normalize_barcode(a), normalize_barcode(b)
    if not a or not b:
        return False
    if a == b:
        return True
    # GTIN-12 (UPC, iHerb) vs GTIN-13 (EAN, IL) often differ by a leading zero.
    return a.lstrip("0") == b.lstrip("0") and abs(len(a) - len(b)) <= 1


def _xlit_brand(name: str) -> str:
    low = name.lower()
    for he, lat in BRAND_XLIT.items():
        if he in name or he.lower() in low:
            return lat
    return low


def _tokens(text: str) -> set[str]:
    text = (text or "").lower()
    text = re.sub(r"[^\w֐-׿.]+", " ", text)
    toks = {t for t in text.split() if t and t not in _STOP and len(t) > 1}
    return toks


def _dose_tokens(text: str) -> set[str]:
    out = set()
    for amt, unit in _DOSE.findall(text or ""):
        out.add(re.sub(r"[.,]", "", amt))  # bare number, unit-agnostic (mg vs מ"ג)
    return out


@dataclass
class MatchResult:
    barcode: str | None
    sp_name: str
    matched: bool
    method: str            # "barcode" | "name" | "none"
    confidence: float      # 0..1
    ambiguous: bool = False
    candidates: list = field(default_factory=list)  # near-ties when ambiguous
    panel: Optional[IherbPanel] = None
    notes: str = ""


def _name_score(sp_name: str, sp_brand: str | None, panel: IherbPanel) -> float:
    """Token-overlap score in [0,1] on transliterated brand + active + dose."""
    sp_brand_lat = _xlit_brand(sp_brand or sp_name)
    panel_brand = (panel.brand or "").lower()
    brand_hit = 0.0
    if sp_brand_lat and panel_brand:
        if sp_brand_lat in panel_brand or panel_brand.split()[0] in sp_brand_lat:
            brand_hit = 1.0
    # active overlap (panel ingredient english vs SP hebrew is weak; lean on dose + brand)
    sp_doses = _dose_tokens(sp_name)
    panel_doses = set()
    for a in panel.actives:
        if a.amount is not None:
            panel_doses.add(str(int(a.amount)) if float(a.amount).is_integer() else str(a.amount))
    dose_hit = 1.0 if (sp_doses & panel_doses) else 0.0
    # english ingredient token appearing in the (often part-latin) SP name
    sp_toks = _tokens(sp_name)
    ing_toks = set()
    for a in panel.actives:
        ing_toks |= _tokens(a.ingredient or "")
    ing_hit = 1.0 if (sp_toks & ing_toks) else 0.0
    # weighted: brand is the strongest local signal, dose corroborates, ingredient bonus
    return round(0.55 * brand_hit + 0.30 * dose_hit + 0.15 * ing_hit, 3)


def bridge_one(sp_item, panels: list[IherbPanel],
               name_threshold: float = 0.55,
               ambiguity_margin: float = 0.10) -> MatchResult:
    """Match one Super-Pharm PriceItem to the best iHerb panel.

    Barcode-first; then normalized brand+dose name score. Flags ambiguous matches
    (two candidates within `ambiguity_margin`) instead of guessing.
    """
    bc = sp_item.barcode
    # 1) barcode-first
    bc_hits = [p for p in panels if barcodes_match(bc, p.barcode)]
    if len(bc_hits) == 1:
        return MatchResult(bc, sp_item.name, True, "barcode", 1.0, panel=bc_hits[0],
                           notes="exact barcode/GTIN match")
    if len(bc_hits) > 1:
        return MatchResult(bc, sp_item.name, False, "barcode", 1.0, ambiguous=True,
                           candidates=bc_hits, notes="multiple panels share this barcode")

    # 2) name fallback
    scored = sorted(((_name_score(sp_item.name, sp_item.manufacturer, p), p)
                     for p in panels), key=lambda x: x[0], reverse=True)
    if not scored or scored[0][0] < name_threshold:
        best = scored[0][0] if scored else 0.0
        return MatchResult(bc, sp_item.name, False, "none", best,
                           notes=f"no panel >= name_threshold ({name_threshold})")
    top_score, top_panel = scored[0]
    runner = scored[1][0] if len(scored) > 1 else 0.0
    if top_score - runner < ambiguity_margin:
        return MatchResult(bc, sp_item.name, False, "name", top_score, ambiguous=True,
                           candidates=[p for s, p in scored[:3]],
                           notes=f"ambiguous: top {top_score} vs runner {runner}")
    return MatchResult(bc, sp_item.name, True, "name", top_score, panel=top_panel,
                       notes="brand+dose name match (barcodes differ: IL SKU vs iHerb US SKU)")


def assemble_label(sp_item, match: MatchResult, sku_id: str | None = None) -> dict:
    """Assemble a candidate BSIP0-S label dict from a Super-Pharm SKU + a matched panel.

    Super-Pharm supplies Israeli-shelf identity + price; iHerb supplies the panel. The
    result mirrors `supplement_label.SupplementLabel` (the engine's in-house BSIP0-S
    surface) but is a *candidate* — it must clear BSIP0/QA before any score, and its
    `primary_claim` is left as the raw on-label text (claim->tier selection is a Nutrition
    curation step, §2.1). Both provenance stamps are carried.
    """
    panel = match.panel
    sku_id = sku_id or f"SP-{normalize_barcode(sp_item.barcode)}"
    actives = []
    for a in (panel.actives if panel else []):
        actives.append({
            "active_slug": None,  # dossier mapping is a downstream curation step
            "display_name": a.ingredient,
            "quantity": a.amount,
            "unit": a.unit,
            "form": a.form,
            "is_core": True,
            "in_proprietary_blend": bool(panel.proprietary_blend) if panel else False,
        })
    sp_prov = sp_item.provenance.as_dict() if getattr(sp_item, "provenance", None) else None
    panel_prov = panel.provenance.as_dict() if (panel and panel.provenance) else None
    return {
        "sku_id": sku_id,
        "verification_status": "candidate",  # EDPG firewall — NOT admitted to scoring
        "israeli_shelf": {  # the local-shelf integrity control (Super-Pharm presence)
            "barcode": sp_item.barcode,
            "name_he": sp_item.name,
            "brand": sp_item.manufacturer,
            "price_ils": sp_item.price,
            "chain": "super_pharm",
            "provenance": sp_prov,
        },
        "panel": (panel.as_dict() if panel else None),
        "bsip0s_label": {
            "product_name": (panel.product_name if panel else sp_item.name),
            "primary_claim_raw": (panel.primary_claim if panel else None),
            "primary_claim_mapped": None,   # Nutrition selects the dossier claim tier (§2.1)
            "actives": actives,
            "proprietary_blend": bool(panel.proprietary_blend) if panel else None,
        },
        "match": {
            "matched": match.matched,
            "method": match.method,
            "confidence": match.confidence,
            "ambiguous": match.ambiguous,
            "notes": match.notes,
        },
        "missing_or_lossy_fields": (panel.missing_fields if panel else ["no panel matched"]),
        "provenance_panel": panel_prov,
        "admission_note": ("candidate only; Super-Pharm presence = Israeli-shelf integrity "
                           "control; panel = iHerb candidate; NOT admitted; must clear "
                           "BSIP0/QA; claim->tier is a Nutrition curation step."),
    }


def bridge_catalog(sp_items: list, panels: list[IherbPanel], **kw) -> list[dict]:
    """Bridge a whole Super-Pharm supplement catalog against a set of iHerb panels.
    Returns one assembled-label dict per SP item (matched or not)."""
    out = []
    for it in sp_items:
        m = bridge_one(it, panels, **kw)
        out.append(assemble_label(it, m))
    return out


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    # tiny self-check: barcode tolerance
    print("GTIN 12/13:", barcodes_match("898220100187", "0898220100187"))
    print("differ:", barcodes_match("898220100187", "733739016508"))
