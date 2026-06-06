"""Israeli local-brand supplement panel adapters  (TASK-171J, parent TASK-171).

The local-brand panel-acquisition stack the MVP decision pack (TASK-171I) GO'd. The
Super-Pharm price feed (`il_prices`) gives Israeli-shelf identity + price but NO panel;
~80% of the addressable shelf is local-brand (Altman/SupHerb/Life/Tink/...) with no iHerb
panel. This module acquires a *candidate* per-active panel for those SKUs from the Israeli
vitamin e-tailers + brand sites Data's feasibility probe found richest + redundant.

Two adapters, one shape:
  * E-TAILER generic adapter — vitamins4all / biogaya / klilhateva / vitamania. Mostly
    WooCommerce-style `רכיבים` + per-active dose blocks; one firecrawl JSON-extract schema
    covers them all. This is the high-leverage unlock (~55-65% of addressable).
  * ALTMAN brand-site adapter — altman.co.il publishes a clean full panel (the #1 local
    brand, ~24 addressable SKUs). Same extract schema, brand-site selector.

FIRECRAWL BOUNDARY (same contract as iherb_panel.py): this module does NOT import an MCP
SDK. `acquire_panel(... , scraper=...)` takes a `scraper(url, schema, prompt) -> dict`
callable the agent wires to the firecrawl_scrape tool. A `search` callable is likewise
injected for URL discovery. Missing field = recorded `missing`, NEVER fabricated.

EDPG: every panel is born `verification_status="candidate"`. Nothing is admitted to a
published score; the assembled label must still clear BSIP0/QA to be promoted. The engine
reads in-house labels only — this is a quarantined candidate.
"""
from __future__ import annotations

import json
import pathlib
import re
from dataclasses import dataclass, field
from typing import Callable, Optional

from .provenance import Provenance, stamp

CLIENT_VERSION = "il_supplement_panels/0.1 (firecrawl json + IL e-tailer/brand-site)"

# Sites the probe found richest + redundant. host -> (label, is_brand_site).
ETAILER_HOSTS = {
    "vitamins4all.co.il": ("vitamins4all", False),
    "biogaya.co.il": ("biogaya", False),
    "klilhateva.co.il": ("klilhateva", False),
    "vitamania.co.il": ("vitamania", False),
}
BRAND_HOSTS = {
    "altman.co.il": ("altman", True),
}
ALL_PANEL_HOSTS = {**ETAILER_HOSTS, **BRAND_HOSTS}

# ---- the firecrawl JSON-extract schema (one shape for every IL panel source) ----
PANEL_SCHEMA = {
    "type": "object",
    "properties": {
        "brand": {"type": "string"},
        "product_name": {"type": "string"},
        "barcode": {"type": "string"},
        "serving_size": {"type": "string"},
        "servings_per_container": {"type": "string"},
        "ingredient_list_raw": {"type": "string"},
        "primary_claim": {"type": "string"},
        "proprietary_blend": {"type": "boolean"},
        "actives": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "ingredient": {"type": "string"},
                    "amount": {"type": "number"},
                    "unit": {"type": "string"},
                    "form": {"type": "string"},
                },
            },
        },
    },
}
PANEL_PROMPT = (
    "Extract the supplement product panel from this Israeli supplement product page. "
    "For each active ingredient give the ingredient name, the per-serving (per capsule / "
    "tablet / softgel) amount, the unit (מ\"ג=mg, מק\"ג=mcg, יחב\"ל/IU), and the chemical "
    "form if shown (e.g. אוקסיד=oxide, ציטראט=citrate, ביסגליצינאט=bisglycinate, "
    "כלצterm=carbonate). Also extract: brand, product name, barcode/EAN/מק\"ט, serving "
    "size, servings per container, the raw ingredient list (רכיבים) text, whether a "
    "proprietary blend is declared, and the primary on-label health claim/benefit. "
    "Return any field you cannot find as null. NEVER guess or fabricate a value."
)

# --------------------------------------------------------------------------- #
# Hebrew/Latin -> engine normalization (active slug, unit, form). FROZEN maps,  #
# precision-first; a miss is recorded, never invented.                          #
# --------------------------------------------------------------------------- #
# active display -> engine dossier slug (dossier_loader.ACTIVE_DOSSIER_FILES keys)
_ACTIVE_SLUG = [
    ("vitamin_b12", ("b12", "b-12", "קובלמין", "cobalamin", "ויטמין b12")),
    ("folic_acid", ("חומצה פולית", "פולית", "folic", "folate", "פולאט")),
    ("vitamin_d3", ("d3", "d-3", "ויטמין d", "ויטמין די", "כולקלציפרול", "cholecalciferol")),
    ("omega3", ("אומגה", "omega", "epa", "dha", "שמן דגים", "fish oil")),
    ("magnesium", ("מגנזיום", "magnesium", "מגנז")),
    ("vitamin_c", ("ויטמין c", "vitamin c", "ויטמין סי", "אסקורב", "ascorb")),
    ("zinc", ("אבץ", "zinc")),
    ("iron", ("ברזל", "iron", "פומרט", "ביסגלי", "fumarate")),
    ("calcium", ("סידן", "calcium")),
    ("biotin", ("ביוטין", "biotin")),
    ("caffeine", ("קפאין", "caffeine")),
    ("vitamin_e", ("ויטמין e", "vitamin e", "ויטמין אי", "טוקופרול", "tocopherol")),
]

_UNIT_MAP = {
    'מ"ג': "mg", "מ״ג": "mg", "מג": "mg", "mg": "mg", "מיליגרם": "mg",
    'מק"ג': "mcg", "מקג": "mcg", "mcg": "mcg", "µg": "mcg", "מיקרוגרם": "mcg",
    'יחב"ל': "IU", "יחבל": "IU", "iu": "IU", "יב״ל": "IU",
    "g": "g", "גרם": "g", 'גר': "g",
}

# Hebrew chemical-form -> Latin form token (so it hits the dossier form_ladder which is
# normalized lowercase Latin). FROZEN; only forms the dossiers actually ladder.
_FORM_MAP = {
    "אוקסיד": "oxide", "ציטראט": "citrate", "citrate": "citrate", "oxide": "oxide",
    "ביסגליצינאט": "bisglycinate", "גליצינאט": "glycinate", "bisglycinate": "bisglycinate",
    "מאלאט": "malate", "malate": "malate", "טאורט": "taurate", "taurate": "taurate",
    "כלוריד": "chloride", "לקטט": "lactate", "קרבונט": "carbonate", "carbonate": "carbonate",
    "קרבונאט": "carbonate", "פומרט": "fumarate", "fumarate": "fumarate",
    "ביסגליצינאט": "bisglycinate", "סולפט": "sulfate", "סולפאט": "sulfate",
    "כולקלציפרול": "cholecalciferol", "cholecalciferol": "cholecalciferol", "d3": "cholecalciferol",
    "מתילקובלמין": "methylcobalamin", "methylcobalamin": "methylcobalamin",
    "ציאנוקובלמין": "cyanocobalamin", "אסקורבית": "ascorbic acid", "אסקורבי": "ascorbic acid",
    "פיקולינאט": "picolinate", "picolinate": "picolinate", "גלוקונט": "gluconate",
    "טוקופרול": "alpha-tocopherol",
}


def normalize_unit(u: Optional[str]) -> Optional[str]:
    if not u:
        return None
    u2 = u.strip().lower().replace(" ", "")
    for k, v in _UNIT_MAP.items():
        if k.lower().replace(" ", "") in u2 or u2 in k.lower():
            return v
    return u.strip() or None


def detect_active_slug(*texts: str) -> Optional[str]:
    blob = " ".join(t for t in texts if t).lower()
    for slug, kws in _ACTIVE_SLUG:
        if any(k in blob for k in kws):
            return slug
    return None


# Excipient/antioxidant tokens that are NOT the active's chemical form even though they
# carry a "form-like" word (e.g. di-alpha-tocopherol is an omega-3 antioxidant, not the
# omega form). Guards the ingredient-list sniff against false form attribution.
_FORM_SNIFF_EXCLUDE = ("טוקופרול", "tocopherol", "גליצרול", "glycerol", "גליצרין",
                       "ג'לטין", "gelatin", "חמניות", "סויה")


def normalize_form(form: Optional[str], ingredient: Optional[str] = None,
                   ingredient_list: Optional[str] = None) -> Optional[str]:
    """Map a Hebrew/Latin form string to a dossier-ladder Latin token.

    Priority: (1) the explicit form column, (2) the ingredient NAME (e.g. 'מגנזיום אוקסיד'),
    (3) the רכיבים ingredient list — but ONLY the leading token of the list, and never an
    excipient (tocopherol/glycerol/etc). Sniffing the WHOLE list mis-attributes an
    excipient's form-word to the active; precision-first."""
    # (1) explicit form column
    if form:
        low = form.lower()
        for k, v in _FORM_MAP.items():
            if k.lower() in low:
                return v
    # (2) the ingredient name itself
    if ingredient:
        low = ingredient.lower()
        for k, v in _FORM_MAP.items():
            if k.lower() in low:
                return v
    # (3) leading token of the רכיבים list (the active's compound), excipient-guarded
    if ingredient_list:
        head = ingredient_list.split(",")[0].lower()
        if not any(x in head for x in _FORM_SNIFF_EXCLUDE):
            for k, v in _FORM_MAP.items():
                if k.lower() in head:
                    return v
    return form.strip() if form else None


@dataclass
class PanelActiveIL:
    ingredient: Optional[str] = None
    amount: Optional[float] = None
    unit: Optional[str] = None          # normalized: mg|mcg|IU|g
    form: Optional[str] = None          # normalized Latin form token
    form_raw: Optional[str] = None      # the raw (Hebrew) form as extracted
    active_slug: Optional[str] = None   # engine dossier slug, or None if unmapped


@dataclass
class ILPanel:
    """A candidate per-active panel from an Israeli e-tailer / brand site."""
    url: str
    source: str                          # host label (vitamins4all / altman / ...)
    brand: Optional[str] = None
    product_name: Optional[str] = None
    barcode: Optional[str] = None
    serving_size: Optional[str] = None
    servings_per_container: Optional[str] = None
    ingredient_list_raw: Optional[str] = None
    primary_claim: Optional[str] = None
    proprietary_blend: Optional[bool] = None
    actives: list[PanelActiveIL] = field(default_factory=list)
    missing_fields: list[str] = field(default_factory=list)
    provenance: Optional[Provenance] = None
    raw: dict = field(default_factory=dict)

    def has_scoreable_active(self) -> bool:
        """At least one active with a slug + amount + unit (form may be sniffed/None)."""
        return any(a.active_slug and a.amount is not None and a.unit for a in self.actives)

    def as_dict(self) -> dict:
        return {
            "url": self.url, "source": self.source, "brand": self.brand,
            "product_name": self.product_name, "barcode": self.barcode,
            "serving_size": self.serving_size,
            "servings_per_container": self.servings_per_container,
            "ingredient_list_raw": self.ingredient_list_raw,
            "primary_claim": self.primary_claim,
            "proprietary_blend": self.proprietary_blend,
            "actives": [vars(a) for a in self.actives],
            "missing_fields": self.missing_fields,
            "provenance": self.provenance.as_dict() if self.provenance else None,
        }


def _host_of(url: str) -> str:
    m = re.search(r"https?://([^/]+)/", url + "/")
    host = (m.group(1) if m else "").lower().lstrip("www.")
    for h in ALL_PANEL_HOSTS:
        if h in host:
            return h
    return host


def _norm_num(v) -> Optional[float]:
    if v is None or v == "":
        return None
    try:
        return float(str(v).replace(",", "").strip())
    except (ValueError, TypeError):
        return None


def _coerce(raw: dict, url: str, source_id: str | None) -> ILPanel:
    data = raw
    for key in ("json", "data", "extract", "llm_extraction"):
        if isinstance(data, dict) and key in data and isinstance(data[key], dict):
            data = data[key]
    host = _host_of(url)
    label, _is_brand = ALL_PANEL_HOSTS.get(host, (host, False))
    p = ILPanel(url=url, source=label, raw=raw)
    p.brand = data.get("brand") or None
    p.product_name = data.get("product_name") or None
    p.barcode = (re.sub(r"\D", "", str(data.get("barcode"))) or None) if data.get("barcode") else None
    p.serving_size = data.get("serving_size") or None
    p.servings_per_container = (str(data.get("servings_per_container")).strip() or None
                                if data.get("servings_per_container") is not None else None)
    p.ingredient_list_raw = data.get("ingredient_list_raw") or None
    p.primary_claim = data.get("primary_claim") or None
    p.proprietary_blend = data.get("proprietary_blend")

    for a in (data.get("actives") or []):
        if not isinstance(a, dict):
            continue
        ing = a.get("ingredient") or None
        raw_form = a.get("form") or None
        act = PanelActiveIL(
            ingredient=ing,
            amount=_norm_num(a.get("amount")),
            unit=normalize_unit(a.get("unit")),
            form=normalize_form(raw_form, ing, p.ingredient_list_raw),
            form_raw=raw_form,
            active_slug=detect_active_slug(ing or "", p.product_name or "", url),
        )
        p.actives.append(act)

    # lossiness pass — record, NEVER fill.
    for f in ("brand", "product_name", "barcode", "serving_size", "primary_claim"):
        if getattr(p, f) in (None, ""):
            p.missing_fields.append(f)
    if not p.actives:
        p.missing_fields.append("actives (none extracted)")
    for i, a in enumerate(p.actives):
        if a.amount is None:
            p.missing_fields.append(f"actives[{i}].amount")
        if not a.unit:
            p.missing_fields.append(f"actives[{i}].unit")
        if not a.form:
            p.missing_fields.append(f"actives[{i}].form (not on panel)")
        if not a.active_slug:
            p.missing_fields.append(f"actives[{i}].active_slug (unmapped to engine dossier)")

    p.provenance = stamp(
        source=f"il_supplement_panels:{label}",
        source_id=source_id or p.barcode or url,
        source_url=url,
        client_version=CLIENT_VERSION,
    )
    return p


def acquire_panel(url: str, scraper: Callable[[str, dict, str], dict],
                  source_id: str | None = None) -> ILPanel:
    """Acquire a candidate ILPanel from one e-tailer/brand-site product URL.

    `scraper(url, schema, prompt) -> dict` is the firecrawl_scrape(json) adapter (injected
    so the module stays SDK-free + testable). Missing fields recorded, never fabricated.
    """
    raw = scraper(url, PANEL_SCHEMA, PANEL_PROMPT)
    return _coerce(raw or {}, url, source_id)


# --------------------------------------------------------------------------- #
# Cache scraper (offline replay — respectful: never re-hit a cached URL).      #
# --------------------------------------------------------------------------- #
def cache_scraper(cache_dir: str | pathlib.Path) -> Callable[[str, dict, str], dict]:
    """Replay cached firecrawl extractions keyed by URL. Cache = dir of <slug>.json each
    holding {'url':..., 'json':{...extraction...}}. Returns {} on a miss (honest 'not
    found', never a fabricated panel)."""
    cache_dir = pathlib.Path(cache_dir)
    index: dict[str, dict] = {}
    if cache_dir.exists():
        for fp in cache_dir.glob("*.json"):
            try:
                obj = json.loads(fp.read_text(encoding="utf-8"))
            except (ValueError, OSError):
                continue
            u = obj.get("url")
            if u:
                index[u] = obj.get("json", obj.get("extraction", obj))

    def _scrape(url: str, schema: dict, prompt: str) -> dict:
        return index.get(url, {})
    return _scrape
