"""Try to discover laibcatalog file listing via AJAX endpoint."""
import sys, re, requests
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

LAIB_BASE = "https://laibcatalog.co.il/"
VICTORY_CHAIN = "7290696200003"

# Common ASP.NET MVC / WebAPI patterns
CANDIDATE_ENDPOINTS = [
    f"{LAIB_BASE}api/files/{VICTORY_CHAIN}",
    f"{LAIB_BASE}api/pricefile/list/{VICTORY_CHAIN}",
    f"{LAIB_BASE}PriceFile/GetFileList?chainId={VICTORY_CHAIN}",
    f"{LAIB_BASE}PriceFile/List?chainId={VICTORY_CHAIN}",
    f"{LAIB_BASE}Home/GetFiles?chainId={VICTORY_CHAIN}",
    f"{LAIB_BASE}Home/FileList/{VICTORY_CHAIN}",
    # Direct file listing
    f"https://laibcatalog.co.il/CompetitionRegulationsFiles/latest/{VICTORY_CHAIN}/",
    # Try with just chain partial
    f"{LAIB_BASE}72906962/",
]

# Also try accessing the main page with a chain filter parameter
CHAIN_PARAMS = [
    f"{LAIB_BASE}?chainId={VICTORY_CHAIN}",
    f"{LAIB_BASE}?chain={VICTORY_CHAIN}",
    f"{LAIB_BASE}home/index?chainId={VICTORY_CHAIN}",
]

print("=== Trying direct AJAX/API endpoints ===", flush=True)
for url in CANDIDATE_ENDPOINTS:
    try:
        r = requests.get(url, timeout=10)
        has_gz = '.gz' in r.text.lower() if r.text else False
        has_pricefull = 'pricefull' in r.text.lower() if r.text else False
        print(f"  {r.status_code} len={len(r.text)} gz={has_gz} pf={has_pricefull} | {url}", flush=True)
        if has_gz or (r.status_code == 200 and len(r.text) > 500):
            gz_links = re.findall(r'([^\s"\'<>]*\.gz)', r.text[:5000], re.I)
            for gl in gz_links[:5]:
                print(f"    -> {gl}", flush=True)
    except Exception as e:
        print(f"  ERROR: {e} | {url}", flush=True)

print("\n=== Trying chain filter on main page ===", flush=True)
for url in CHAIN_PARAMS:
    try:
        r = requests.get(url, timeout=10)
        has_gz = '.gz' in r.text.lower() if r.text else False
        print(f"  {r.status_code} len={len(r.text)} gz={has_gz} | {url}", flush=True)
    except Exception as e:
        print(f"  ERROR: {e} | {url}", flush=True)

# Try to see if the 98KB page has the Victory files in a hidden section
print("\n=== Searching 98KB page for Victory file patterns ===", flush=True)
r = requests.get(LAIB_BASE, timeout=15)
page = r.text

# Look for the chain ID pattern near any file-like string
for m in re.finditer(re.escape(VICTORY_CHAIN), page):
    start = max(0, m.start() - 200)
    end = min(len(page), m.end() + 300)
    snippet = page[start:end]
    if re.search(r'(Price|\.gz|download|file)', snippet, re.I):
        print(f"\n  Context: {snippet[:400]}", flush=True)
        break

# Check if there's a data-table or grid with file entries
victory_region_start = page.find(VICTORY_CHAIN)
if victory_region_start != -1:
    region = page[victory_region_start:victory_region_start+500]
    print(f"\n  Victory region sample: {region}", flush=True)
