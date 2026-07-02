"""Quick laibcatalog access check."""
import sys, requests
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

LAIBCATALOG_PORTAL = "https://laibcatalog.co.il/"
try:
    r = requests.get(LAIBCATALOG_PORTAL, timeout=15)
    print(f"Status: {r.status_code}", flush=True)
    print(f"Content length: {len(r.text)}", flush=True)
    # Look for any gz links
    import re
    gz_links = re.findall(r'href=["\']([^"\']+\.gz[^"\']*)["\']', r.text)
    print(f"GZ links found: {len(gz_links)}", flush=True)
    for lnk in gz_links[:10]:
        print(f"  {lnk}", flush=True)
    # Check for chain IDs
    chain_ids = re.findall(r'\d{13}', r.text)
    from collections import Counter
    print(f"\nChain IDs in page: {dict(Counter(chain_ids).most_common(10))}", flush=True)
except Exception as e:
    print(f"Error: {e}", flush=True)
    import traceback
    traceback.print_exc()
