"""Project Spine1 (TASK-252, Phase 3) — production smoke test (ADD-1).

Read-only checks against the live site:
  1. Every known comparison route answers HTTP 200.
  2. No page body contains an Open Food Facts reference (hard rule, TASK-238).
  3. Page body is non-trivial (catches blank/error shells that still return 200).

Exit code 0 = all pass; 1 = any FAIL. Routes that 404 are reported as ABSENT
(informational, not failure — a category may be intentionally unlaunched).

Usage:
  python smoke_test.py                 # against https://bari.digital
  python smoke_test.py --base URL      # against a preview deployment
"""
from __future__ import annotations

import argparse
import sys
import urllib.error
import urllib.request

BASE = "https://bari.digital"

# Candidate comparison routes; ABSENT is acceptable, FAIL is not.
ROUTES = [
    "/hashvaot/bread",
    "/hashvaot/butter",
    "/hashvaot/breakfast-cereals",
    "/hashvaot/granola",
    "/hashvaot/snacks",
    "/hashvaot/salty-snacks",
    "/hashvaot/yogurts",
    "/hashvaot/cheese",
    "/hashvaot/hard-cheeses",
    "/hashvaot/hummus",
    "/hashvaot/maadanim",
    "/hashvaot/juices",
]

OFF_MARKERS = ("openfoodfacts", "off_api", "openfoodfacts.org")
MIN_BODY_BYTES = 5_000


def fetch(url: str) -> tuple[int, bytes]:
    req = urllib.request.Request(url, headers={"User-Agent": "bari-spine-smoke/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as e:
        return e.code, b""
    except urllib.error.URLError as e:
        raise ConnectionError(f"unreachable: {e.reason}") from e


def check_route(base: str, route: str) -> tuple[str, str]:
    """Returns (verdict, detail): PASS | ABSENT | FAIL"""
    status, body = fetch(base + route)
    if status == 404:
        return "ABSENT", "404 (not launched)"
    if status != 200:
        return "FAIL", f"HTTP {status}"
    lower = body.lower()
    hits = [m for m in OFF_MARKERS if m.encode() in lower]
    if hits:
        return "FAIL", f"OFF reference in page body: {hits}"
    if len(body) < MIN_BODY_BYTES:
        return "FAIL", f"suspiciously small body ({len(body)} bytes)"
    return "PASS", f"200, {len(body):,} bytes, 0 OFF refs"


def main() -> None:
    parser = argparse.ArgumentParser(description="Bari production smoke test")
    parser.add_argument("--base", default=BASE)
    args = parser.parse_args()

    print(f"smoke test against {args.base}")
    failures = 0
    for route in ROUTES:
        try:
            verdict, detail = check_route(args.base, route)
        except ConnectionError as e:
            verdict, detail = "FAIL", str(e)
        if verdict == "FAIL":
            failures += 1
        print(f"  {verdict:6s} {route:32s} {detail}")
    print(f"\nresult: {'FAIL' if failures else 'PASS'} ({failures} failing routes)")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
