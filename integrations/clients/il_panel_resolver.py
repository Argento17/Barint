"""Per-SKU source-priority panel resolver  (TASK-171J, parent TASK-171).

Given a Super-Pharm SKU (barcode + Hebrew name + brand from il_prices) and a pool of
candidate ILPanels acquired from the Israeli e-tailers/brand sites, pick the BEST panel
in source-priority order and assemble a candidate BSIP0-S label. Verifies the match
before trusting a source; flags ambiguous rather than guessing.

Source priority (per the MVP decision pack):
  1. BARCODE match  — the e-tailers print the EAN; an exact barcode hit is near-certain.
  2. BRAND-SITE (Altman) brand+active+dose match — authoritative for that brand.
  3. E-TAILER brand+active+dose match — the breadth source.
  4. residue — no trustworthy panel; recorded as unscoreable with the reason.

A match is TRUSTED only if (barcode hit) OR (same engine active AND same brand-token AND a
corroborating dose/lead-number). Two near-tie panels for one SKU => ambiguous (not guessed).
Everything candidate (EDPG); claim->tier is left to the engine + Nutrition curation.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Optional

from .il_supplement_panels import ILPanel, detect_active_slug

# brand-token map: a coarse brand bucket from the SP manufacturer/name, matched against
# the panel brand. FROZEN, precision-first.
_BRAND_TOKENS = {
    "altman": ("altman", "אלטמן"),
    "supherb": ("supherb", "סופהרב", "סאפ הרב", "אמברוזיה", "ambrosia"),
    "life": ("life", "לייף"),
    "solgar": ("solgar", "סולגאר", "סולגר"),
    "tink": ("tink", "tinc", "טינק"),
    "now": ("now", "נאו"),
    "floris": ("floris", "florish", "פלוריש"),
    "magnesia": ("magnesia", "מגנזיה"),
    "amorphical": ("amorphical", "אמורפיקל"),
    "marshall": ("marshall", "מרשל"),
    "sequoia": ("sequoia", "סקויה"),
}


def _brand_token(*texts: str) -> Optional[str]:
    blob = " ".join(t for t in texts if t).lower()
    for b, kws in _BRAND_TOKENS.items():
        if any(k in blob for k in kws):
            return b
    return None


def _norm_bc(bc: Optional[str]) -> Optional[str]:
    if not bc:
        return None
    d = re.sub(r"\D", "", str(bc))
    return d or None


def _barcodes_match(a: Optional[str], b: Optional[str]) -> bool:
    a, b = _norm_bc(a), _norm_bc(b)
    if not a or not b:
        return False
    if a == b:
        return True
    return a.lstrip("0") == b.lstrip("0") and abs(len(a) - len(b)) <= 1


_NUM = re.compile(r"(\d{2,4})")


def _lead_numbers(text: str) -> set[str]:
    """The dose-ish numbers in a name/label (e.g. '520', '5000'). Unit-agnostic; used only
    to CORROBORATE a brand+active match, never as the sole signal."""
    return set(_NUM.findall(text or ""))


# source-priority rank (lower = tried first)
_SOURCE_RANK = {"altman": 1, "vitamins4all": 2, "biogaya": 2, "klilhateva": 2, "vitamania": 2}


@dataclass
class ResolveResult:
    sp_barcode: Optional[str]
    sp_name: str
    sp_active: Optional[str]
    matched: bool
    method: str                # "barcode" | "brand_active_dose" | "none"
    source: Optional[str]      # panel host label
    confidence: float          # 0..1
    ambiguous: bool = False
    panel: Optional[ILPanel] = None
    candidates: list = field(default_factory=list)
    reason: str = ""


def _score_panel(sp_barcode, sp_name, sp_brand, sp_active, panel: ILPanel) -> tuple:
    """Return (trusted, confidence, method) for one (SP SKU, panel) pair."""
    # 1) barcode
    if _barcodes_match(sp_barcode, panel.barcode):
        return True, 1.0, "barcode"
    # 2) brand + active + corroborating dose
    sp_brand_tok = _brand_token(sp_brand or "", sp_name)
    panel_brand_tok = _brand_token(panel.brand or "", panel.product_name or "")
    brand_ok = bool(sp_brand_tok and panel_brand_tok and sp_brand_tok == panel_brand_tok)

    panel_active = next((a.active_slug for a in panel.actives if a.active_slug), None)
    if not panel_active:
        panel_active = detect_active_slug(panel.product_name or "", panel.url)
    active_ok = bool(sp_active and panel_active and sp_active == panel_active)

    sp_nums = _lead_numbers(sp_name)
    panel_nums = _lead_numbers(panel.product_name or "")
    panel_dose_nums = set()
    for a in panel.actives:
        if a.amount is not None:
            panel_dose_nums.add(str(int(a.amount)) if float(a.amount).is_integer() else str(a.amount))
    panel_nums |= panel_dose_nums
    # STRONG dose corroboration: a dose/product number from the panel actually appears in
    # the SP item name (e.g. SP 'מגנזיום 520' <-> panel 520). Precision-first: brand+active
    # alone is NOT enough — two different Tink magnesiums (malate 136 vs oxide 520) must NOT
    # collapse onto one panel. Requiring a shared salient number prevents that.
    dose_ok = bool(sp_nums & panel_nums)

    # FORM corroboration / CONTRADICTION: if the SP name names a chemical form (טאורט/אוקסיד/
    # מאלאט/ציטראט/ביסגליצינאט) AND the panel has a different form, that's a CONTRADICTION ->
    # not the same SKU, reject the brand+active match.
    sp_form = _form_in_name(sp_name)
    panel_form = next((a.form for a in panel.actives if a.form), None)
    form_contradiction = bool(sp_form and panel_form and sp_form != panel_form)

    if brand_ok and active_ok and dose_ok and not form_contradiction:
        return True, round(0.85, 3), "brand_active_dose"
    if brand_ok and active_ok and sp_form and panel_form and sp_form == panel_form:
        # form match substitutes for a dose-number match (e.g. both 'ביסגליצינאט')
        return True, round(0.8, 3), "brand_active_form"
    # otherwise NOT trusted (precision-first)
    weak = 0.3 * active_ok + 0.2 * brand_ok + 0.1 * dose_ok
    return False, round(weak, 3), "weak"


# chemical-form tokens that may appear in an SP item NAME (Hebrew), used for form
# corroboration/contradiction against the panel form.
_NAME_FORM = {
    "אוקסיד": "oxide", "ציטראט": "citrate", "ציטרט": "citrate",
    "ביסגליצינאט": "bisglycinate", "ביסגליצינט": "bisglycinate", "גליצינאט": "glycinate",
    "מאלאט": "malate", "מלאט": "malate", "מאלט": "malate",
    "טאורט": "taurate", "טאוראט": "taurate", "פיקולינאט": "picolinate",
    "קרבונט": "carbonate", "קרבונאט": "carbonate", "ציטרט": "citrate",
}


def _form_in_name(name: str) -> Optional[str]:
    low = (name or "").lower()
    for he, lat in _NAME_FORM.items():
        if he in low:
            return lat
    return None


def resolve_sku(sp_item, sp_active: Optional[str], panels: list[ILPanel],
                ambiguity_margin: float = 0.08) -> ResolveResult:
    """Resolve the best candidate panel for one Super-Pharm SKU. Source-priority +
    match-verification; flags ambiguous near-ties instead of guessing."""
    sp_barcode = getattr(sp_item, "barcode", None)
    sp_name = getattr(sp_item, "name", "") or ""
    sp_brand = getattr(sp_item, "manufacturer", None)

    scored = []
    for p in panels:
        trusted, conf, method = _score_panel(sp_barcode, sp_name, sp_brand, sp_active, p)
        if trusted:
            # tie-break by source priority then confidence
            rank = _SOURCE_RANK.get(p.source, 9)
            scored.append((conf, -rank, method, p))
    if not scored:
        return ResolveResult(sp_barcode, sp_name, sp_active, False, "none", None, 0.0,
                             reason="no trustworthy panel (no barcode hit; no brand+active+dose match)")

    scored.sort(key=lambda x: (x[0], x[1]), reverse=True)
    top = scored[0]
    # ambiguity: two DIFFERENT panels (different barcode/product) within the margin AND
    # neither is a barcode-certain hit.
    if len(scored) > 1:
        runner = scored[1]
        same_product = (_norm_bc(top[3].barcode) == _norm_bc(runner[3].barcode)
                        and top[3].barcode is not None)
        if (top[2] != "barcode" and not same_product
                and abs(top[0] - runner[0]) < ambiguity_margin):
            return ResolveResult(sp_barcode, sp_name, sp_active, False, top[2],
                                 top[3].source, top[0], ambiguous=True,
                                 candidates=[s[3] for s in scored[:3]],
                                 reason=f"ambiguous: top {top[0]} vs runner {runner[0]}")
    return ResolveResult(sp_barcode, sp_name, sp_active, True, top[2], top[3].source,
                         top[0], panel=top[3],
                         reason=f"{top[2]} match via {top[3].source}")
