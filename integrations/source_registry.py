"""Bari retailer source registry — verified entry points, URL patterns, and failure fingerprints.

Each entry documents what we know about a retailer's accessibility for BSIP0 scraping:
  - il_prices identity layer (price-feed portals, always open)
  - storefront scraping layer (product pages, subject to WAF/bot-detection)

access_status values:
  CLEAR                          — confirmed accessible via local Playwright, no bot protection
  BLOCKED_TLS_FINGERPRINT_FAKE_200 — server fingerprints headless Chromium; returns HTTP 200
                                     with fake maintenance image instead of real content
  BLOCKED_CLOUDFLARE_403         — Cloudflare Bot Management hard block (HTTP 403)
  BLOCKED_F5_BIGIP_403           — F5 BIG-IP Advanced WAF hard block (HTTP 403)
  UNKNOWN                        — not yet tested or status stale (>30 days)

All statuses verified 2026-06-07 by local Playwright + Firecrawl diagnostic probe.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class FailureFingerprint:
    """Pattern that identifies a WAF/bot-block response vs. real product content."""
    name: str
    description: str
    http_status: int | None           # None = applies at any HTTP status
    content_patterns: list[str]       # any match → fingerprint detected


@dataclass
class RetailerSource:
    id: str
    display_name: str

    # --- il_prices identity layer ---
    il_prices_chain_id: str | None    # 13-digit chain ID from the price feed
    il_prices_kind: str | None        # "self_hosted" | "laibcatalog" | None

    # --- storefront scraping layer ---
    storefront_entry_url: str | None
    product_url_pattern: str | None   # {barcode} placeholder; None if unverified
    product_url_pattern_verified: bool

    # Hebrew DOM markers that confirm a real product page loaded (not a block page)
    dom_markers: list[str] = field(default_factory=list)

    # Known WAF/bot-block fingerprints for this retailer
    failure_fingerprints: list[FailureFingerprint] = field(default_factory=list)

    # Current access status and when it was last confirmed
    access_status: str = "UNKNOWN"
    access_status_verified_at: str | None = None

    notes: str = ""


# ---------------------------------------------------------------------------
# Fingerprint library (shared across retailers where applicable)
# ---------------------------------------------------------------------------

FP_SHUFERSAL_FAKE_200 = FailureFingerprint(
    name="BLOCKED_TLS_FINGERPRINT_FAKE_200",
    description=(
        "Server fingerprints headless Chromium at the TLS layer (JA3/JA4 hash). "
        "Returns HTTP 200 with a static <img src='Maintenance1.jpg'> — no HTML body, "
        "no cookies, no JS. Looks like maintenance but fires for all non-browser agents. "
        "Stealth and enhanced Firecrawl proxy tiers do not bypass this."
    ),
    http_status=200,
    content_patterns=["Maintenance1.jpg", "s3-eu-west-1.amazonaws.com/www.shufersal.co.il"],
)

FP_CLOUDFLARE_403 = FailureFingerprint(
    name="BLOCKED_CLOUDFLARE_403",
    description=(
        "Cloudflare Bot Management (paid tier) hard block. Returns HTTP 403 with "
        "'Attention Required! | Cloudflare' page. No interactive challenge — the block "
        "is final based on IP reputation + TLS fingerprint. Firecrawl stealth/enhanced "
        "proxies do not bypass this tier of Cloudflare."
    ),
    http_status=403,
    content_patterns=["Attention Required! | Cloudflare", "You have been blocked", "cloudflare"],
)

FP_F5_BIGIP_403 = FailureFingerprint(
    name="BLOCKED_F5_BIGIP_403",
    description=(
        "F5 BIG-IP Advanced WAF hard block. Returns HTTP 403 before any HTML renders. "
        "Block fires at the network/IP-reputation layer. Error page contains F5 support ID. "
        "No cookie or JS bypass possible — the connection is rejected pre-render."
    ),
    http_status=403,
    content_patterns=["The requested URL was rejected", "F5 site:", "Your support ID"],
)


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

RETAILER_SOURCES: dict[str, RetailerSource] = {

    "yohananof": RetailerSource(
        id="yohananof",
        display_name="יוחננוף",
        il_prices_chain_id="7290455000004",
        il_prices_kind="laibcatalog",
        storefront_entry_url="https://www.yochananof.co.il/",
        product_url_pattern="https://www.yochananof.co.il/category?search={query}",
        product_url_pattern_verified=True,
        dom_markers=["הוסף לסל", "ערכים תזונתיים", "רכיבים", "מחיר"],
        failure_fingerprints=[],
        access_status="CLEAR",
        access_status_verified_at="2026-06-07",
        notes=(
            "PRIMARY source. MUI React SPA — requires local Playwright (headless=False "
            "preferred). Cookie popup: [data-aria-desc='dialog_cookies_accept']. "
            "Product modal: [role='dialog'] with tabs 'ערכים תזונתיים' / 'רכיבים' / 'מידע אלרגני'. "
            "Barcodes in CDN image paths (d226b0iufwcjmj.cloudfront.net, retailer ID 1470). "
            "il_prices via laibcatalog confirmed live 2026-06-07."
        ),
    ),

    "shufersal": RetailerSource(
        id="shufersal",
        display_name="שופרסל",
        il_prices_chain_id="7290027600007",
        il_prices_kind="self_hosted",
        storefront_entry_url="https://www.shufersal.co.il/online/he/",
        product_url_pattern="https://www.shufersal.co.il/online/he/A{barcode}",
        product_url_pattern_verified=True,
        dom_markers=["הוסף לסל", "ערכים תזונתיים", "מרכיבים", "מחיר"],
        failure_fingerprints=[FP_SHUFERSAL_FAKE_200],
        access_status="CLEAR",
        access_status_verified_at="2026-06-07",
        notes=(
            "UNLOCKED 2026-06-07 via crawlee 1.7 + DefaultFingerprintGenerator (browserforge). "
            "Raw Playwright / Firecrawl still blocked: server fingerprints headless Chromium "
            "at the TLS layer (JA3/JA4) and returns fake HTTP 200 + Maintenance1.jpg. "
            "crawlee's DefaultFingerprintGenerator injects realistic Chrome TLS/navigator "
            "fingerprints that bypass the check. Homepage loaded: 2.5MB real content, "
            "confirmed 'שופרסל'/'הוסף לסל' signals present. "
            "Usage: from crawlee.crawlers import PlaywrightCrawler; "
            "from crawlee.fingerprint_suite import DefaultFingerprintGenerator, HeaderGeneratorOptions; "
            "fp = DefaultFingerprintGenerator(header_options=HeaderGeneratorOptions(browsers=['chrome'])); "
            "crawler = PlaywrightCrawler(fingerprint_generator=fp, navigation_timeout=timedelta(seconds=30)). "
            "il_prices identity feed (prices.shufersal.co.il) is LIVE and unaffected — "
            "separate Azure blob portal with no bot protection. "
            "Scraper: 03_operations/bsip0/scrape/shufersal/ (to be built)."
        ),
    ),

    "victory": RetailerSource(
        id="victory",
        display_name="ויקטורי",
        il_prices_chain_id="7290696200003",
        il_prices_kind="laibcatalog",
        storefront_entry_url="https://www.victoryonline.co.il/",
        product_url_pattern="https://www.victoryonline.co.il/?catalogProduct={id}",
        product_url_pattern_verified=True,
        dom_markers=["הוסף לסל", "ערכים תזונתיים", "מרכיבים", "מחיר"],
        failure_fingerprints=[],
        access_status="CLEAR",
        access_status_verified_at="2026-06-07",
        notes=(
            "SECONDARY source. Same SaaS as Yohananof (CDN: d226b0iufwcjmj.cloudfront.net, "
            "retailer ID 1470 — confirmed 2026-06-07). Playwright adapter: "
            "03_operations/bsip0/scrape/victory/01_acquire_victory.py. "
            "Search URL: victoryonline.co.il/category?search={query}. "
            "Modal/tab pattern identical to Yohananof — 'ערכים תזונתיים' / 'רכיבים' tabs "
            "present in SPA modal, NOT in static page scrape. "
            "Product URL pattern CONFIRMED 2026-06-07 via Firecrawl: "
            "/?catalogProduct=<numeric_internal_ID> (not barcode). "
            "Discovery pattern: category page links are ?catalogProduct=<ID>. "
            "Nutrition availability: present in Playwright modal scrape only; "
            "static Firecrawl scrape of ?catalogProduct URL returns SPA shell with "
            "product list embedded — nutrition tab does not render without JS execution. "
            "Recommended approach: Playwright headless=True (same as Yohananof) — "
            "search yochananof.co.il/category?search={query} then click modal. "
            "il_prices chain 7290696200003 confirmed live on laibcatalog 2026-06-07."
        ),
    ),

    "carrefour": RetailerSource(
        id="carrefour",
        display_name="קרפור",
        il_prices_chain_id="7290661400001",   # NAME-UNCONFIRMED on laibcatalog
        il_prices_kind="laibcatalog",
        storefront_entry_url="https://www.carrefour.co.il/",
        product_url_pattern="https://www.carrefour.co.il/product/{barcode}",
        product_url_pattern_verified=False,
        dom_markers=["הוסף לסל", "ערכים תזונתיים", "מרכיבים"],
        failure_fingerprints=[FP_F5_BIGIP_403],
        access_status="BLOCKED_F5_BIGIP_403",
        access_status_verified_at="2026-06-07",
        notes=(
            "il_prices chain_id 7290661400001 is present on laibcatalog but NAME-UNCONFIRMED "
            "— has not been verified as Carrefour via a Stores file. Storefront blocked by "
            "F5 BIG-IP WAF at network layer (pre-render, HTTP 403). "
            "Alternative: check il_gov_data / prices.food.gov.il — Carrefour participates "
            "in mandatory price reporting and structured data may be available there."
        ),
    ),

    "rami_levi": RetailerSource(
        id="rami_levi",
        display_name="רמי לוי",
        il_prices_chain_id=None,          # not in current CHAINS registry; unknown chain_id
        il_prices_kind=None,
        storefront_entry_url="https://www.rami-levy.co.il/",
        product_url_pattern="https://www.rami-levy.co.il/he/online/market/product/{barcode}",
        product_url_pattern_verified=False,
        dom_markers=["הוסף לסל", "ערכים תזונתיים", "מרכיבים", "מחיר"],
        failure_fingerprints=[FP_CLOUDFLARE_403],
        access_status="BLOCKED_CLOUDFLARE_403",
        access_status_verified_at="2026-06-07",
        notes=(
            "No il_prices chain_id confirmed — Rami Levi may publish via matrixcatalog.co.il "
            "or prices.mega.co.il (not yet tested). Storefront blocked by Cloudflare Bot "
            "Management (paid tier, hard 403 — not the free JS challenge). "
            "Fix: residential proxy + real browser fingerprint, OR find structured data feed."
        ),
    ),

    "tiv_taam": RetailerSource(
        id="tiv_taam",
        display_name="טיב טעם",
        il_prices_chain_id=None,          # not yet confirmed on laibcatalog; check needed
        il_prices_kind=None,
        storefront_entry_url="https://www.tivtaam.co.il/",
        product_url_pattern=None,
        product_url_pattern_verified=False,
        dom_markers=[],
        failure_fingerprints=[FP_F5_BIGIP_403],
        access_status="BLOCKED_F5_BIGIP_403",
        access_status_verified_at="2026-06-07",
        notes=(
            "Storefront blocked by F5 BIG-IP Advanced WAF (HTTP 403, transaction ID in body). "
            "WAF fires at network/IP-reputation layer — not a geo-block. "
            "il_prices chain_id not yet confirmed: check laibcatalog for 'tiv taam' or '729000' "
            "prefix chain IDs. Available on Wolt as 'tiv-taam-ibn-gabirol'. "
            "Unlock path: Playwright with playwright-stealth + Israeli residential proxy. "
            "Status: INVESTIGATE — not yet attempted with full stealth browser profile."
        ),
    ),

    "machsaney_hashuk": RetailerSource(
        id="machsaney_hashuk",
        display_name="מחסני השוק",
        il_prices_chain_id=None,          # not yet confirmed; check laibcatalog
        il_prices_kind=None,
        storefront_entry_url="https://www.mck.co.il/",
        product_url_pattern=None,
        product_url_pattern_verified=False,
        dom_markers=[],
        failure_fingerprints=[FP_F5_BIGIP_403],
        access_status="BLOCKED_F5_BIGIP_403",
        access_status_verified_at="2026-06-07",
        notes=(
            "Domain: mck.co.il (confirmed from Google index 2026-06-07). "
            "Full e-commerce catalog confirmed accessible in Google index (/categories). "
            "Storefront blocked by F5 BIG-IP Advanced WAF — same pattern as Tiv Taam. "
            "il_prices chain_id not yet confirmed. "
            "Unlock path: Playwright with playwright-stealth + Israeli residential proxy. "
            "Status: INVESTIGATE — not yet attempted with full stealth browser profile."
        ),
    ),

    "hazi_hinam": RetailerSource(
        id="hazi_hinam",
        display_name="חצי חינם",
        il_prices_chain_id=None,          # NOT on laibcatalog (verified 2026-06-07); check matrixcatalog or self-hosted portal
        il_prices_kind=None,
        storefront_entry_url="https://shop.hazi-hinam.co.il/",
        product_url_pattern="https://shop.hazi-hinam.co.il/catalog/{id}/{slug}",
        product_url_pattern_verified=True,
        dom_markers=["הוסף לסל", "ערכים תזונתיים", "סינון לפי יצרן"],
        failure_fingerprints=[],
        access_status="CLEAR",
        access_status_verified_at="2026-06-07",
        notes=(
            "CLEAR — no WAF block detected. Angular SPA (NOT Yohananof/Victory MUI React SaaS). "
            "Own CDN: cdn.hazi-hinam.co.il (app version V_1.3027). "
            "Catalog URL: /catalog/{numeric_id}/{hebrew-slug} (e.g. /catalog/10/מיצים-ומשקאות). "
            "Products are loaded client-side via API — catalog pages render shell + filters only "
            "in static scrape; actual product list requires JS execution (Playwright). "
            "Search route (/search?q=, /search?term=) redirects to /NotFound in static scrape "
            "— Angular router handles search client-side only. "
            "il_prices: NOT on laibcatalog (only Yohananof on laibcatalog as of 2026-06-07). "
            "Chain ID unknown — check matrixcatalog.co.il or self-hosted portal for mandatory price feed. "
            "Playwright adapter: adapt 03_operations/bsip0/scrape/yohananof/ for Angular patterns "
            "(no MUI dialog — check for Angular CDK overlay or custom modal). "
            "~12 stores, northern Israel focus. Specialty: deli cheeses, fresh meat, fish."
        ),
    ),
}


def get_source(retailer_id: str) -> RetailerSource:
    """Return source entry; raises KeyError for unknown retailer IDs."""
    if retailer_id not in RETAILER_SOURCES:
        raise KeyError(
            f"Unknown retailer '{retailer_id}'. "
            f"Known: {list(RETAILER_SOURCES)}"
        )
    return RETAILER_SOURCES[retailer_id]


def clear_sources() -> list[RetailerSource]:
    """Return only retailers currently confirmed as CLEAR for storefront scraping."""
    return [s for s in RETAILER_SOURCES.values() if s.access_status == "CLEAR"]


def blocked_sources() -> list[RetailerSource]:
    """Return retailers with a known access block."""
    return [
        s for s in RETAILER_SOURCES.values()
        if s.access_status.startswith("BLOCKED_")
    ]
