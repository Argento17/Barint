"""Source entry validation — detect WAF blocks, fake maintenance, and portal failures
before a scrape run wastes time or silently returns 0 products.

Two validation layers:
  1. il_prices portal check (HTTP, no browser) — confirms price-feed portals are up.
  2. Storefront content check (called after a page scrape returns) — matches the response
     against known failure fingerprints to detect WAF blocks masquerading as real pages.

Usage in a Playwright-based scraper:
    from integrations.source_validator import require_il_prices_accessible, detect_storefront_failure
    from integrations.source_registry import get_source

    require_il_prices_accessible("victory")   # raises SourceAccessError if il_prices portal is down

    # After Playwright page.content():
    html = page.content()
    detect_storefront_failure("victory", html, http_status=200)   # raises if WAF fingerprint matched

Usage with check_dom_markers:
    if not check_dom_markers("yohananof", html):
        raise SourceAccessError("yohananof", "NO_DOM_MARKERS",
            "Page loaded but expected Hebrew markers absent — login wall or partial render")

Note: Firecrawl is NOT the production scraping path. Local Playwright is the default.
Firecrawl may be used for one-off diagnostics or access probes only.
"""
from __future__ import annotations

import datetime
from dataclasses import dataclass

from .source_registry import RETAILER_SOURCES, FailureFingerprint, RetailerSource, get_source


# ---------------------------------------------------------------------------
# Exception
# ---------------------------------------------------------------------------

class SourceAccessError(RuntimeError):
    """Raised when a retailer source is confirmed blocked or a portal is unreachable.

    Attributes:
        retailer_id: the source id from RETAILER_SOURCES
        access_status: the blocking classification (e.g. BLOCKED_CLOUDFLARE_403)
        fingerprint: the matched FailureFingerprint if detected from response content
        detail: human-readable explanation
    """
    def __init__(
        self,
        retailer_id: str,
        access_status: str,
        detail: str,
        fingerprint: FailureFingerprint | None = None,
    ) -> None:
        self.retailer_id = retailer_id
        self.access_status = access_status
        self.fingerprint = fingerprint
        self.detail = detail
        super().__init__(
            f"[{retailer_id}] {access_status}: {detail}"
        )


# ---------------------------------------------------------------------------
# Registry-based pre-flight check
# ---------------------------------------------------------------------------

def require_storefront_clear(retailer_id: str) -> RetailerSource:
    """Check the registry and raise immediately if the source is known-blocked.

    Call this at the top of any scrape function that uses Firecrawl on a retailer's
    storefront, before making any API calls. Prevents wasting credits on a known block.

    Returns the RetailerSource so callers can use it without a second lookup.
    """
    source = get_source(retailer_id)
    if source.access_status.startswith("BLOCKED_"):
        fp = source.failure_fingerprints[0] if source.failure_fingerprints else None
        raise SourceAccessError(
            retailer_id=retailer_id,
            access_status=source.access_status,
            fingerprint=fp,
            detail=(
                f"Source is registry-classified as {source.access_status} "
                f"(verified {source.access_status_verified_at}). "
                f"{source.notes}"
            ),
        )
    return source


# ---------------------------------------------------------------------------
# Storefront content fingerprint detection (post-Firecrawl)
# ---------------------------------------------------------------------------

@dataclass
class ContentCheckResult:
    blocked: bool
    fingerprint: FailureFingerprint | None
    matched_pattern: str | None
    retailer_id: str
    checked_at: str


def detect_storefront_failure(
    retailer_id: str,
    content: str,
    http_status: int = 200,
    raise_on_block: bool = True,
) -> ContentCheckResult:
    """Check Firecrawl response content against known failure fingerprints.

    Call this immediately after every Firecrawl scrape call before attempting to
    parse the content as a product page. Prevents silently treating a WAF block page
    as a valid (empty) product page.

    Args:
        retailer_id: source id from RETAILER_SOURCES
        content: the markdown/text body returned by Firecrawl
        http_status: the HTTP status code returned (default 200)
        raise_on_block: if True (default), raises SourceAccessError on a match.
                        Set False to check without raising (returns result).

    Returns:
        ContentCheckResult — always returned when raise_on_block=False.
    """
    source = get_source(retailer_id)
    now = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

    for fp in source.failure_fingerprints:
        # Status match: skip if fingerprint specifies a status and it doesn't match.
        if fp.http_status is not None and fp.http_status != http_status:
            continue
        for pattern in fp.content_patterns:
            if pattern.lower() in content.lower():
                result = ContentCheckResult(
                    blocked=True,
                    fingerprint=fp,
                    matched_pattern=pattern,
                    retailer_id=retailer_id,
                    checked_at=now,
                )
                if raise_on_block:
                    raise SourceAccessError(
                        retailer_id=retailer_id,
                        access_status=fp.name,
                        fingerprint=fp,
                        detail=(
                            f"Failure fingerprint '{fp.name}' matched on pattern "
                            f"'{pattern}' (HTTP {http_status}). {fp.description}"
                        ),
                    )
                return result

    return ContentCheckResult(
        blocked=False,
        fingerprint=None,
        matched_pattern=None,
        retailer_id=retailer_id,
        checked_at=now,
    )


def check_dom_markers(retailer_id: str, content: str) -> bool:
    """Verify that at least one expected Hebrew DOM marker is present in the content.

    A page that passes fingerprint detection but contains none of the expected
    Hebrew markers (e.g. 'הוסף לסל', 'ערכים תזונתיים') is likely a redirect,
    login wall, or partial render — not a real product page.

    Returns True if at least one marker is found, False if none are.
    """
    source = get_source(retailer_id)
    if not source.dom_markers:
        return True  # no markers defined → cannot validate
    return any(marker in content for marker in source.dom_markers)


# ---------------------------------------------------------------------------
# il_prices portal reachability check
# ---------------------------------------------------------------------------

def require_il_prices_accessible(retailer_id: str, timeout: int = 10) -> None:
    """Confirm the il_prices portal for this retailer is reachable before fetching feeds.

    Makes a lightweight HEAD request (or GET if HEAD is not supported) to the portal
    entry URL. Raises SourceAccessError if the portal is unreachable or returns a
    non-2xx status.

    This is a network-level check only — it does not validate feed contents.
    """
    import urllib.request
    import urllib.error

    source = get_source(retailer_id)

    if source.il_prices_kind is None:
        raise SourceAccessError(
            retailer_id=retailer_id,
            access_status="NO_IL_PRICES",
            detail=f"No il_prices chain registered for '{retailer_id}'.",
        )

    from .clients.il_prices import SHUFERSAL_PORTAL, LAIBCATALOG_PORTAL
    portal_url = SHUFERSAL_PORTAL if source.il_prices_kind == "self_hosted" else LAIBCATALOG_PORTAL

    try:
        req = urllib.request.Request(portal_url, method="HEAD")
        req.add_header("User-Agent", "Bari-SourceValidator/1.0")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            if resp.status >= 400:
                raise SourceAccessError(
                    retailer_id=retailer_id,
                    access_status=f"PORTAL_HTTP_{resp.status}",
                    detail=f"il_prices portal {portal_url} returned HTTP {resp.status}.",
                )
    except urllib.error.URLError as exc:
        raise SourceAccessError(
            retailer_id=retailer_id,
            access_status="PORTAL_UNREACHABLE",
            detail=f"il_prices portal {portal_url} unreachable: {exc.reason}",
        ) from exc


# ---------------------------------------------------------------------------
# Diagnostic report
# ---------------------------------------------------------------------------

def print_access_report() -> None:
    """Print a human-readable access status table for all registered sources."""
    rows = []
    for src in RETAILER_SOURCES.values():
        il = src.il_prices_chain_id or "—"
        status = src.access_status
        verified = src.access_status_verified_at or "never"
        rows.append((src.display_name, il, status, verified))

    col_w = [max(len(r[i]) for r in rows + [("Retailer", "Chain ID", "Storefront Status", "Verified")]) + 2
             for i in range(4)]

    header = (
        "Retailer".ljust(col_w[0]) +
        "Chain ID".ljust(col_w[1]) +
        "Storefront Status".ljust(col_w[2]) +
        "Verified"
    )
    print(header)
    print("-" * len(header))
    for name, chain, status, verified in rows:
        print(name.ljust(col_w[0]) + chain.ljust(col_w[1]) + status.ljust(col_w[2]) + verified)


if __name__ == "__main__":
    print_access_report()
