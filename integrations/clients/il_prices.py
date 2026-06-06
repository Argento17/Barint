"""Israeli price-transparency feeds — structured retail catalog by law.

For: Data Agent. Israel's food-competition law (חוק קידום התחרות בענף המזון, 2014)
requires major chains to publish full SKU files publicly. This replaces fragile
storefront scraping with a structured feed of barcode + item name + brand + quantity +
unit + price, across many chains.

IMPORTANT — what this gives you and what it does NOT:
  * YES: product identity (barcode/EAN), Hebrew item name, manufacturer, pack size,
    unit, price, per-store availability. Great for corpus building + de-duplication.
  * NO: nutrition panels or ingredient lists. Those are NOT in the feeds. Pair each
    barcode with `open_food_facts` / `tzameret` to get a panel.

Three live portal families (all LIVE-VERIFIED 2026-06-03):
  1. Self-hosted Shufersal (`prices.shufersal.co.il`) — lists Azure-blob .gz files;
     parse links, gunzip, read standard XML.  → list_shufersal_files()
  2. laibcatalog.co.il — multi-chain publisher portal serving Victory + others as open
     .gz files (NO login). Same XML schema → parse_price_xml is reused; only the listing
     (relative, backslash paths, ASP.NET) differs.  → list_laibcatalog_files()
  3. Super-Pharm (`prices.super-pharm.co.il`, chain 7290172900007) — a PriceTransparency.WS
     ASP.NET MVC-grid portal (open, NO login). The file list is an HTML grid paginated with
     `?page=N` and filterable by file type with `?Category-equals=<Type>` (empty grid-name
     => empty param prefix). Same standard transparency XML (`<Line>` rows in
     OrderXml/Envelope/Header/Details) → parse_price_xml is reused unchanged.
     → list_super_pharm_files() / fetch_super_pharm_supplements() (TASK-171G).
     Identity+price ONLY — never a nutrition panel. Pair the barcode with an iHerb panel
     (see integrations/clients/iherb_panel.py) for the BSIP0-S label.

HISTORICAL NOTE: the old central host `url.publishedprices.co.il` (Cerberus) is DEAD as
of 2026-06-03 — DNS no longer resolves from any network tested. laibcatalog replaced it.
Other live publisher hosts exist (e.g. prices.mega.co.il, matrixcatalog.co.il) and can be
added with the same `_descriptors` + `parse_price_xml` plumbing as coverage needs grow.

Standard file types: PriceFull (full catalog), Price (delta), PromoFull/Promo,
Stores. File name: <Type><ChainId>-<StoreId>-<Seq>-<YYYYMMDD>-<HHMMSS>.gz
"""
from __future__ import annotations

import gzip
import html
import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from datetime import date
from urllib.parse import urljoin

from .http import get
from .provenance import Provenance, stamp

CLIENT_VERSION = "1.2"  # 1.2 = Super-Pharm PriceTransparency.WS grid reader (TASK-171G)

SHUFERSAL_PORTAL = "https://prices.shufersal.co.il/"
LAIBCATALOG_PORTAL = "https://laibcatalog.co.il/"  # multi-chain, no login (verified 2026-06-03)
SUPERPHARM_PORTAL = "https://prices.super-pharm.co.il/"  # PriceTransparency.WS grid, no login (verified 2026-06-03)
SUPERPHARM_CHAIN_ID = "7290172900007"

# Chain registry. status reflects live verification on the date noted.
#
# NOTE (2026-06-03): the old central Cerberus host `url.publishedprices.co.il` is DEAD
# (DNS no longer resolves, from both this sandbox and the owner's network). The live
# replacement is `laibcatalog.co.il`, which serves standard .gz price files openly (no
# login). Victory (7290696200003) is confirmed present; the other chain_ids below were
# discovered live but not yet name-confirmed — use discover_laibcatalog_chains() to see
# the current set and confirm names via each chain's Stores file.
CHAINS: dict[str, dict] = {
    "shufersal": {
        "chain_id": "7290027600007",
        "kind": "self_hosted",
        "portal": SHUFERSAL_PORTAL,
        "status": "LIVE-VERIFIED",
    },
    "victory": {
        "chain_id": "7290696200003",
        "kind": "laibcatalog",
        "portal": LAIBCATALOG_PORTAL,
        "status": "LIVE-VERIFIED",
    },
    # Present on laibcatalog 2026-06-03, names to confirm via Stores file:
    "laib_7290058179503": {"chain_id": "7290058179503", "kind": "laibcatalog", "portal": LAIBCATALOG_PORTAL, "status": "NAME-UNCONFIRMED"},
    "laib_7290455000004": {"chain_id": "7290455000004", "kind": "laibcatalog", "portal": LAIBCATALOG_PORTAL, "status": "NAME-UNCONFIRMED"},
    "laib_7290661400001": {"chain_id": "7290661400001", "kind": "laibcatalog", "portal": LAIBCATALOG_PORTAL, "status": "NAME-UNCONFIRMED"},
    "laib_7290875100001": {"chain_id": "7290875100001", "kind": "laibcatalog", "portal": LAIBCATALOG_PORTAL, "status": "NAME-UNCONFIRMED"},
    "super_pharm": {
        "chain_id": SUPERPHARM_CHAIN_ID,
        "kind": "superpharm_grid",
        "portal": SUPERPHARM_PORTAL,
        "status": "LIVE-VERIFIED",  # 2026-06-03, TASK-171G
    },
}


@dataclass
class PriceFile:
    type: str           # Price | PriceFull | Promo | PromoFull | Stores
    chain_id: str
    store_id: str
    file_date: str      # YYYYMMDD
    url: str


@dataclass
class PriceItem:
    barcode: str
    name: str
    manufacturer: str | None = None
    price: float | None = None
    quantity: str | None = None
    unit: str | None = None
    provenance: Provenance | None = None  # identity+price only — never a nutrition panel
    raw: dict = field(default_factory=dict)


_FTYPE = re.compile(r"^(PriceFull|Price|PromoFull|Promo|StoresFull|Stores)", re.I)


def _parse_fname(fname: str) -> tuple[str, str, str, str] | None:
    """Tolerant parser for both portal naming orders. Returns (type, chain, store, date).

    Shufersal: Price<chain13>-<store>-<seq>-<YYYYMMDD>-<HHMMSS>.gz
    Laib:      Price<chain13>-<store>-<YYYYMMDDHHMM>-<seq>.xml.gz
    """
    t = _FTYPE.match(fname)
    if not t:
        return None
    chain_m = re.search(r"\d{13}", fname)
    if not chain_m:
        return None
    chain = chain_m.group(0)
    rest = fname[chain_m.end():].lstrip("-")
    store = (re.match(r"(\d+)", rest) or re.match(r"", rest)).group(0) or ""
    # First timestamp run (>=8 digits) anywhere after the chain → take YYYYMMDD.
    ts = re.search(r"\d{8,14}", fname[chain_m.end():])
    date = ts.group(0)[:8] if ts else ""
    return t.group(1), chain, store, date


def _descriptors(page: str, base: str) -> list[PriceFile]:
    out: list[PriceFile] = []
    for link in re.findall(r"href=[\"']([^\"']+\.gz[^\"']*)[\"']", page):
        link = html.unescape(link).replace("\\", "/")          # laib uses backslashes
        link = urljoin(base, link)                              # resolve relative paths
        fname = link.split("/")[-1].split("?")[0]
        parsed = _parse_fname(fname)
        if not parsed:
            continue
        ftype, chain, store, date = parsed
        out.append(PriceFile(type=ftype, chain_id=chain, store_id=store,
                             file_date=date, url=link))
    return out


def list_shufersal_files(category: int | None = None) -> list[PriceFile]:
    """Parse the Shufersal portal page into download descriptors. LIVE-VERIFIED."""
    url = SHUFERSAL_PORTAL if category is None else f"{SHUFERSAL_PORTAL}?catID={category}"
    page = get(url).decode("utf-8", errors="replace")
    return _descriptors(page, SHUFERSAL_PORTAL)


def list_laibcatalog_files(chain_id: str | None = None) -> list[PriceFile]:
    """Parse the laibcatalog portal (Victory + others). No login. LIVE-VERIFIED 2026-06-03.
    Pass chain_id to filter to one chain."""
    page = get(LAIBCATALOG_PORTAL).decode("utf-8", errors="replace")
    files = _descriptors(page, LAIBCATALOG_PORTAL)
    return [f for f in files if chain_id is None or f.chain_id == chain_id]


def discover_laibcatalog_chains() -> dict[str, int]:
    """Return {chain_id: file_count} currently served by laibcatalog — keeps the registry
    honest as chains come and go, instead of trusting a hardcoded list."""
    counts: dict[str, int] = {}
    for f in list_laibcatalog_files():
        counts[f.chain_id] = counts.get(f.chain_id, 0) + 1
    return counts


# --------------------------------------------------------------------------- #
# Super-Pharm — PriceTransparency.WS MVC-grid reader (TASK-171G)               #
# --------------------------------------------------------------------------- #
# The portal renders the file list as an ASP.NET MVC grid. Listing differs from
# the other two portals (paginated HTML grid, server-side filter) but the .gz
# payload is the SAME standard transparency XML → parse_price_xml is reused.
# Download links look like /Download/<fname>.gz?bucketName=sp_transparency_output_prod
_SP_DL = re.compile(r'href=[\"\'](/Download/[^\"\']+\.gz[^\"\']*)[\"\']')


def list_super_pharm_files(file_type: str = "PriceFull", max_pages: int = 1) -> list[PriceFile]:
    """List Super-Pharm transparency files of one type (default PriceFull).

    The grid is filtered server-side by the file-type column (`Category-equals=<Type>`)
    and paginated with `?page=N` (empty grid-name => empty param prefix). 20 rows/page.
    `max_pages` bounds how many grid pages to walk (each PriceFull row is one store, so
    one page = up to 20 store catalogs; one store is enough to read the whole shelf).
    LIVE-VERIFIED 2026-06-03.
    """
    out: list[PriceFile] = []
    seen: set[str] = set()
    for page in range(1, max_pages + 1):
        sep = "&" if "?" in SUPERPHARM_PORTAL else "?"
        url = f"{SUPERPHARM_PORTAL}{sep}Category-equals={file_type}&page={page}"
        page_html = get(url).decode("utf-8", errors="replace")
        rels = _SP_DL.findall(page_html)
        if not rels:
            break
        for rel in rels:
            link = urljoin(SUPERPHARM_PORTAL, html.unescape(rel))
            fname = link.split("/")[-1].split("?")[0]
            if not fname.startswith(file_type):  # the grid filter is authoritative; double-check
                continue
            if fname in seen:
                continue
            seen.add(fname)
            parsed = _parse_fname(fname)
            if not parsed:
                continue
            ftype, chain, store, fdate = parsed
            out.append(PriceFile(type=ftype, chain_id=chain, store_id=store,
                                 file_date=fdate, url=link))
    return out


# Oral-supplement classifier over the Hebrew item name. The Super-Pharm shelf mixes
# food, cosmetics, cleaning and supplements in one catalog, with NO category code on the
# line — so the shelf is identified by name. Two-sided test: an oral dose-form/active
# signal must be present AND no cosmetic/topical/household signal. Tunable; deliberately
# conservative (favours precision — a missed SKU is "not found", never invented).
_SUPP_FORM_KW = (
    "כמוסות", "קפסולות", "טבליות", "טבליה", "כמוסה", "קפליות", "סופטג'ל", "סופטגל",
    "טיפות", "אבקה", "סירופ", "מסטיק", "סוכריות גומי", "גאמיז", "תוסף", "תוספי",
)
_SUPP_ACTIVE_KW = (
    "ויטמין", "מגנזיום", "אומגה", "קריאטין", "קפאין", "אבץ", "ברזל", "סידן", "סלניום",
    "ביוטין", "פרוביוטיק", "קולגן", "חומצה פולית", "B12", "B-12", "D3", "D-3", "מולטי",
    "מינרל", "אומגה 3", "זרעי", "כורכום", "קואנזים", "מלטונין", "גלוקוזאמין",
)
# Hard excludes — cosmetic / topical / household that the active/form keywords falsely hit.
_SUPP_EXCLUDE_KW = (
    "סרום", "מסכה", "מסיכה", "קרם", "שמפו", "דאודורנט", "סבון", "ג'ל רחצה", "תרסיס שיער",
    "מרכך", "בושם", "איפור", "שפתון", "לק", "מסקרה", "טבליות מדיח", "טבליות כביסה",
    "ניחוח", "מרענן", "פילר", "טישו", "דיאודורנט", "אל-סבון", "קונדישנר", "תחבושת",
)


def is_oral_supplement(name: str) -> bool:
    """Heuristic: does this Hebrew item name look like an ORAL supplement (not a
    cosmetic/topical/household SKU)? Conservative precision-first classifier."""
    if not name:
        return False
    if any(x in name for x in _SUPP_EXCLUDE_KW):
        return False
    has_form = any(k in name for k in _SUPP_FORM_KW)
    has_active = any(k in name for k in _SUPP_ACTIVE_KW)
    # Require an active signal; a dose-form alone (e.g. cleaning "טבליות") is not enough.
    return has_active and (has_form or "תוסף" in name or "מולטי" in name)


def fetch_super_pharm_supplements(
    limit_items: int | None = None,
    supplement_only: bool = True,
) -> list[PriceItem]:
    """Read ONE Super-Pharm PriceFull store catalog and return its oral-supplement SKUs
    (barcode + Hebrew name + brand + price, provenance-stamped `candidate`).

    Identity+price ONLY — NEVER a nutrition panel (guardrail). Pair each barcode with an
    iHerb panel via the barcode bridge to assemble a BSIP0-S label. LIVE-VERIFIED.
    """
    files = list_super_pharm_files("PriceFull", max_pages=1)
    if not files:
        return []
    items = fetch_items(files[0], limit=None)  # fetch_items stamps provenance per item
    if supplement_only:
        items = [it for it in items if is_oral_supplement(it.name)]
    if limit_items:
        items = items[:limit_items]
    return items


def parse_price_xml(xml_bytes: bytes) -> list[PriceItem]:
    """Parse the standard transparency price XML (schema shared across all chains)."""
    root = ET.fromstring(xml_bytes)
    items: list[PriceItem] = []
    # Item containers vary in tag/case across chains: <Item>, <Product>, <Line>.
    for it in root.iter():
        if it.tag.lower() not in ("item", "product", "line"):
            continue
        g = {child.tag.lower(): (child.text or "").strip() for child in it}
        barcode = g.get("itemcode") or g.get("barcode")
        if not barcode:
            continue
        price = None
        for k in ("itemprice", "price", "unitofmeasureprice"):
            if g.get(k):
                try:
                    price = float(g[k]); break
                except ValueError:
                    pass
        items.append(PriceItem(
            barcode=barcode,
            name=g.get("itemname") or g.get("itemnm") or "",
            manufacturer=g.get("manufacturername") or g.get("manufacturer") or None,
            price=price,
            quantity=g.get("quantity") or None,
            unit=g.get("unitqty") or g.get("unitofmeasure") or None,
            raw=g,
        ))
    return items


def fetch_items(price_file: PriceFile, limit: int | None = None) -> list[PriceItem]:
    """Download a .gz price file, gunzip, parse. LIVE-VERIFIED for Shufersal."""
    blob = get(price_file.url)
    xml_bytes = gzip.decompress(blob)
    items = parse_price_xml(xml_bytes)
    items = items[:limit] if limit else items
    for it in items:
        it.provenance = stamp(
            source=f"il_prices:{price_file.chain_id}",
            source_id=it.barcode,
            source_url=price_file.url,
            client_version=CLIENT_VERSION,
        )
    return items


if __name__ == "__main__":
    import sys
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # Hebrew-safe on Windows
    files = list_shufersal_files()
    print(f"portal listed {len(files)} files; sample:")
    pricefiles = [f for f in files if f.type in ("Price", "PriceFull")]
    for f in pricefiles[:3]:
        print(f"  {f.type} chain={f.chain_id} store={f.store_id} date={f.file_date}")
    if pricefiles:
        items = fetch_items(pricefiles[0], limit=3)
        print(f"parsed {len(items)} sample items from {pricefiles[0].type}:")
        for i in items:
            print(f"  barcode={i.barcode} price={i.price} qty={i.quantity} {i.unit} "
                  f"name_len={len(i.name)}")

    print(f"\nlaibcatalog chains live now: {discover_laibcatalog_chains()}")
    laib = [f for f in list_laibcatalog_files() if f.type in ("Price", "PriceFull")]
    if laib:
        litems = fetch_items(laib[0], limit=3)
        print(f"laibcatalog chain {laib[0].chain_id}: parsed {len(litems)} items; "
              f"first barcode={litems[0].barcode} price={litems[0].price}")
