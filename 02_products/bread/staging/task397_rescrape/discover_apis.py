"""
Discover the actual API endpoints used by Victory and Rami Levy by examining
their homepage HTML/JS bundles for fetch() calls and API URL patterns.
"""
from __future__ import annotations
import re
import sys
import urllib.request
import urllib.error

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"


def http_get(url: str, headers: dict = None, timeout: int = 25) -> bytes | None:
    hdrs = {
        "User-Agent": UA,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "he-IL,he;q=0.9,en;q=0.7",
    }
    if headers:
        hdrs.update(headers)
    req = urllib.request.Request(url, headers=hdrs)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            import gzip as gz
            raw = r.read()
            if r.headers.get("Content-Encoding") == "gzip":
                return gz.decompress(raw)
            return raw
    except Exception as e:
        print(f"  ERROR fetching {url}: {e}")
        return None


def find_api_patterns(text: str) -> list[str]:
    """Extract API URL patterns from JavaScript/HTML."""
    patterns = []
    # Look for /api/ paths
    for m in re.finditer(r'["\'/]([a-zA-Z0-9/_.-]*api[a-zA-Z0-9/_.-]*)["\'/]', text, re.I):
        p = m.group(1)
        if len(p) > 4 and len(p) < 120:
            patterns.append(p)
    # Look for fetch() or axios calls
    for m in re.finditer(r'(?:fetch|axios\.get|axios\.post)\s*\(\s*["\']([^"\']+)["\']', text, re.I):
        patterns.append(m.group(1))
    # Look for baseURL patterns
    for m in re.finditer(r'baseURL\s*[:=]\s*["\']([^"\']+)["\']', text, re.I):
        patterns.append(m.group(1))
    return list(dict.fromkeys(patterns))  # deduplicate preserving order


def extract_js_links(html: str, base_url: str) -> list[str]:
    """Extract JS bundle URLs from HTML."""
    links = []
    for m in re.finditer(r'src=["\']([^"\']*\.js[^"\']*)["\']', html):
        src = m.group(1)
        if src.startswith("http"):
            links.append(src)
        elif src.startswith("/"):
            # Derive base domain
            from urllib.parse import urlparse
            p = urlparse(base_url)
            links.append(f"{p.scheme}://{p.netloc}{src}")
    return links


print("=== Discovering Rami Levy API endpoints ===\n")
rl_home = http_get("https://www.rami-levy.co.il/he/search?q=74252", headers={"Accept": "text/html"})
if rl_home:
    html = rl_home.decode("utf-8", errors="replace")
    print(f"Homepage size: {len(html)} chars")
    # Find script tags
    js_links = extract_js_links(html, "https://www.rami-levy.co.il")
    print(f"JS bundles found: {len(js_links)}")
    for l in js_links[:5]:
        print(f"  {l}")

    # Find API patterns in the HTML itself (often has inline config)
    pats = find_api_patterns(html)
    api_pats = [p for p in pats if "/api" in p.lower() or "catalog" in p.lower() or "product" in p.lower() or "search" in p.lower()]
    print(f"\nAPI-like patterns in HTML ({len(api_pats)}):")
    for p in api_pats[:30]:
        print(f"  {p}")

    # Print a wider chunk of the HTML looking for data-src or config
    config_idx = html.lower().find("config")
    api_idx = html.lower().find("/api/")
    if api_idx >= 0:
        print(f"\n/api/ found at idx {api_idx}:")
        print(html[max(0,api_idx-50):api_idx+200])

    # Check for JSON in the page (Next.js / Nuxt data)
    json_idx = html.find("__NEXT_DATA__")
    if json_idx >= 0:
        print(f"\nNext.js data found at {json_idx}")
        chunk = html[json_idx:json_idx+2000]
        print(chunk[:500])

    nuxt_idx = html.find("window.__nuxt__")
    if nuxt_idx >= 0:
        print(f"\nNuxt data at {nuxt_idx}")

    # Try fetching a JS bundle
    if js_links:
        for js_url in js_links[:3]:
            print(f"\nFetching JS bundle: {js_url}")
            js = http_get(js_url, headers={"Accept": "*/*", "Referer": "https://www.rami-levy.co.il/"})
            if js:
                js_text = js.decode("utf-8", errors="replace")
                pats = find_api_patterns(js_text)
                api_pats = [p for p in pats if any(kw in p.lower() for kw in ["/api", "catalog", "product", "search", "barcode"])]
                print(f"  API patterns in bundle ({len(api_pats)}):")
                for p in api_pats[:20]:
                    print(f"    {p}")
            break

print("\n\n=== Discovering Victory API endpoints ===\n")
v_home = http_get("https://www.victory.co.il/search?q=74252", headers={"Accept": "text/html"})
if v_home is None:
    v_home = http_get("https://www.victory.co.il/", headers={"Accept": "text/html"})
if v_home:
    html = v_home.decode("utf-8", errors="replace")
    print(f"Homepage size: {len(html)} chars")

    js_links = extract_js_links(html, "https://www.victory.co.il")
    print(f"JS bundles: {len(js_links)}")
    for l in js_links[:5]:
        print(f"  {l}")

    pats = find_api_patterns(html)
    api_pats = [p for p in pats if any(kw in p.lower() for kw in ["/api", "catalog", "product", "search", "barcode", "umbraco"])]
    print(f"\nAPI-like patterns in HTML ({len(api_pats)}):")
    for p in api_pats[:30]:
        print(f"  {p}")

    api_idx = html.lower().find("/api/")
    if api_idx >= 0:
        print(f"\n/api/ found at {api_idx}:")
        print(html[max(0,api_idx-50):api_idx+200])

    next_idx = html.find("__NEXT_DATA__")
    if next_idx >= 0:
        print(f"\nNext.js data at {next_idx}")
        print(html[next_idx:next_idx+1000])

print("\n=== Done ===")
