"""Project Spine1 (TASK-252 / TASK-290, Phase 3) — manifest-driven production smoke test.

Read-only checks against the live site, expectations from spine ``live_state``:
  1. Every deployed comparison route answers HTTP 200.
  2. No page body contains an Open Food Facts reference (hard rule, TASK-238).
  3. Page body is non-trivial (catches blank/error shells that still return 200).
  4. Freshness: served product_count / version vs manifest (drift = FINDING, not crash).

Exit code 0 = all pass; 1 = any HTTP non-200 or OFF>0. Routes that 404 are ABSENT
(informational, not failure — a category may be intentionally unlaunched).

Usage:
  python smoke_test.py                          # prod default, ingest + HTTP
  python smoke_test.py --base-url http://localhost:3000
  python smoke_test.py --dry-run                # manifest parse only (no HTTP)
  python smoke_test.py --skip-ingest            # use existing spine.db
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path

from spine_db import connect

SPINE_DIR = Path(__file__).resolve().parent
REPO = SPINE_DIR.parents[1]
DEFAULT_BASE = "https://bari.digital"

OFF_MARKERS = (
    "openfoodfacts",
    "open_food_facts",
    "off_api",
    "off_candidate_panel",
    "openfoodfacts.org",
)
MIN_BODY_BYTES = 5_000

# Wired frontend imports (page-data.ts) → deployed route(s). One manifest row each.
DEPLOYED_ROUTES: dict[str, list[str]] = {
    "bread_frontend_v2.json": ["/hashvaot/bread"],
    "cereals_frontend_v2.json": ["/hashvaot/breakfast-cereals"],
    "brined_cheeses_frontend_v2.json": ["/hashvaot/brined-cheeses"],
    "butter_frontend_v2.json": ["/hashvaot/butter"],
    "cakes_hard_cookies_frontend_v1.json": ["/hashvaot/cakes"],
    "cheese_frontend_v3.json": ["/hashvaot/cheese"],
    "cookies_coffee_frontend_v2.json": ["/hashvaot/cookies-coffee"],
    "granola_frontend_v1.json": ["/hashvaot/granola"],
    "hard_cheeses_frontend_v2.json": ["/hashvaot/hard-cheeses"],
    "hummus_frontend_v5.json": ["/hashvaot/hummus", "/hashvaot/vegetable-spreads"],
    "juices_frontend_v3.json": ["/hashvaot/juices"],
    "salty_snacks_frontend_v4.json": ["/hashvaot/salty-snacks"],
    "snacks_frontend_v2.json": ["/hashvaot/snacks"],
    "yogurts_frontend_v3.json": ["/hashvaot/yogurts"],
}

# Legacy route — no comparisons/*.json in live_state; HTTP + OFF only.
LEGACY_ROUTES = ["/hashvaot/milk-comparison"]

PRODUCT_COUNT_PATTERNS = (
    re.compile(r"(\d+)\s*מוצרים\s*נבדקו"),
    re.compile(r"(\d+)\s*מוצרים\s*בדף"),
    re.compile(r"(\d+)\s*מוצרים\s*•"),
    re.compile(r"(\d+)\s*מוצרים\s*בדירוג"),
    re.compile(r"(\d+)\s*מוצרים\s*·"),
)


@dataclass
class ManifestEntry:
    data_file: str
    basename: str
    category: str
    version: str | None
    run_id: str | None
    product_count: int | None
    routes: list[str] = field(default_factory=list)


@dataclass
class RouteResult:
    route: str
    status: str  # PASS | FAIL | ABSENT | DRY-RUN
    http_status: int | None
    off_count: int
    expected_version: str | None
    expected_count: int | None
    served_version: str | None
    served_count: int | None
    findings: list[str] = field(default_factory=list)
    detail: str = ""


def run_ingest(db_path: Path | None) -> None:
    cmd = [sys.executable, str(SPINE_DIR / "ingest.py")]
    if db_path:
        cmd.extend(["--db", str(db_path)])
    print("ingest:", " ".join(cmd))
    subprocess.run(cmd, check=True, cwd=SPINE_DIR)


def load_manifest(db_path: Path | str | None) -> list[ManifestEntry]:
    conn = connect(db_path)
    try:
        rows = conn.execute(
            "SELECT data_file, category, version, run_id, product_count "
            "FROM live_state ORDER BY data_file"
        ).fetchall()
    finally:
        conn.close()

    entries: list[ManifestEntry] = []
    for row in rows:
        basename = Path(row["data_file"]).name
        routes = DEPLOYED_ROUTES.get(basename)
        if not routes:
            continue
        entries.append(
            ManifestEntry(
                data_file=row["data_file"],
                basename=basename,
                category=row["category"],
                version=row["version"],
                run_id=row["run_id"],
                product_count=row["product_count"],
                routes=routes,
            )
        )
    return entries


def verify_json_manifest(entry: ManifestEntry) -> list[str]:
    """Dry-run: committed JSON must match live_state row."""
    findings: list[str] = []
    path = Path(entry.data_file)
    if not path.is_file():
        findings.append(f"missing data file {path}")
        return findings
    doc = json.loads(path.read_text(encoding="utf-8"))
    meta = doc.get("_meta", {}) if isinstance(doc, dict) else {}
    if isinstance(doc, list):
        json_count = len(doc)
    elif isinstance(doc.get("products"), list):
        json_count = len(doc["products"])
    else:
        json_count = meta.get("product_count") or doc.get("totalProducts")
    json_version = meta.get("version")
    if entry.product_count is not None and json_count != entry.product_count:
        findings.append(f"live_state product_count={entry.product_count} ≠ json={json_count}")
    if entry.version and json_version and entry.version != json_version:
        findings.append(f"live_state version={entry.version} ≠ json={json_version}")
    return findings


def fetch(url: str) -> tuple[int, bytes]:
    req = urllib.request.Request(url, headers={"User-Agent": "bari-spine-smoke/2.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read() if e.fp else b""
    except urllib.error.URLError as e:
        raise ConnectionError(f"unreachable: {e.reason}") from e


def count_off_markers(body: bytes) -> int:
    lower = body.lower()
    return sum(lower.count(m.encode()) for m in OFF_MARKERS)


def extract_product_count(text: str, expected: int | None) -> int | None:
    hits: list[int] = []
    for pat in PRODUCT_COUNT_PATTERNS:
        hits.extend(int(m) for m in pat.findall(text))
    if not hits:
        return None
    if expected is not None and expected in hits:
        return expected
    # Prefer hero metadata: first pattern match in document order.
    for pat in PRODUCT_COUNT_PATTERNS:
        m = pat.search(text)
        if m:
            return int(m.group(1))
    return hits[0]


def extract_version(text: str, expected: str | None) -> str | None:
    if not expected:
        return None
    if expected.lower() in text.lower():
        return expected
    return None


def check_route_http(
    base: str,
    route: str,
    expected_version: str | None,
    expected_count: int | None,
) -> RouteResult:
    result = RouteResult(
        route=route,
        status="FAIL",
        http_status=None,
        off_count=0,
        expected_version=expected_version,
        expected_count=expected_count,
        served_version=None,
        served_count=None,
    )
    try:
        status, body = fetch(base.rstrip("/") + route)
    except ConnectionError as e:
        result.detail = str(e)
        return result

    result.http_status = status
    if status == 404:
        result.status = "ABSENT"
        result.detail = "404 (not launched)"
        return result
    if status != 200:
        result.detail = f"HTTP {status}"
        return result

    result.off_count = count_off_markers(body)
    if result.off_count:
        result.detail = f"OFF markers={result.off_count}"
        return result
    if len(body) < MIN_BODY_BYTES:
        result.detail = f"suspiciously small body ({len(body)} bytes)"
        return result

    text = body.decode("utf-8", errors="ignore")
    result.served_count = extract_product_count(text, expected_count)
    result.served_version = extract_version(text, expected_version)

    if expected_count is not None and result.served_count != expected_count:
        result.findings.append(
            f"product_count drift: manifest={expected_count} served={result.served_count}"
        )
    if expected_version:
        if result.served_version != expected_version:
            result.findings.append(
                f"version drift: manifest={expected_version} served={result.served_version or 'not exposed'}"
            )

    result.status = "PASS"
    result.detail = f"200, {len(body):,} bytes"
    return result


def check_route_dry(
    route: str,
    entry: ManifestEntry,
    json_findings: list[str],
) -> RouteResult:
    return RouteResult(
        route=route,
        status="DRY-RUN",
        http_status=None,
        off_count=0,
        expected_version=entry.version,
        expected_count=entry.product_count,
        served_version=entry.version,
        served_count=entry.product_count,
        findings=json_findings,
        detail=f"manifest ok ({entry.basename})" if not json_findings else "manifest drift",
    )


def format_expected(version: str | None, count: int | None) -> str:
    v = version or "-"
    c = str(count) if count is not None else "-"
    return f"{v}/{c}"


def format_served(version: str | None, count: int | None) -> str:
    v = version if version else "-"
    c = str(count) if count is not None else "-"
    return f"{v}/{c}"


def print_report(results: list[RouteResult], findings_total: int) -> tuple[int, int]:
    header = (
        f"{'ROUTE':<34} {'STATUS':<8} {'OFF':>3}  "
        f"{'EXPECTED':<22} {'SERVED':<22} NOTES"
    )
    print(header)
    print("-" * len(header))
    failures = 0
    for r in results:
        notes = r.detail
        if r.findings:
            notes = "; ".join(r.findings)
        if r.status == "FAIL":
            failures += 1
        print(
            f"{r.route:<34} {r.status:<8} {r.off_count:>3}  "
            f"{format_expected(r.expected_version, r.expected_count):<22} "
            f"{format_served(r.served_version, r.served_count):<22} {notes}"
        )
    print()
    print(
        f"result: {'FAIL' if failures else 'PASS'} "
        f"({failures} hard failures, {findings_total} freshness findings)"
    )
    return failures, findings_total


def main() -> None:
    parser = argparse.ArgumentParser(description="Bari manifest-driven production smoke test")
    parser.add_argument("--base-url", "--base", dest="base_url", default=DEFAULT_BASE)
    parser.add_argument("--db", default=None, help="spine database path (default: spine.db)")
    parser.add_argument("--ingest", action="store_true", help="rebuild spine.db before check")
    parser.add_argument("--skip-ingest", action="store_true", help="use existing spine.db as-is")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="parse committed JSON manifest only; no HTTP (proves manifest logic)",
    )
    args = parser.parse_args()

    db_path = Path(args.db) if args.db else None
    if args.ingest or not args.skip_ingest:
        run_ingest(db_path)

    manifest = load_manifest(db_path)
    if not manifest:
        print("ERROR: no deployed manifest entries in live_state", file=sys.stderr)
        sys.exit(1)

    mode = "dry-run (manifest)" if args.dry_run else f"HTTP against {args.base_url}"
    print(f"smoke test — {mode} — {len(manifest)} manifest entries, "
          f"{sum(len(e.routes) for e in manifest)} routes")
    print()

    results: list[RouteResult] = []
    findings_total = 0

    for entry in manifest:
        json_findings = verify_json_manifest(entry) if args.dry_run else []
        for route in entry.routes:
            if args.dry_run:
                r = check_route_dry(route, entry, json_findings)
            else:
                r = check_route_http(
                    args.base_url, route, entry.version, entry.product_count
                )
            findings_total += len(r.findings)
            results.append(r)

    if not args.dry_run:
        for route in LEGACY_ROUTES:
            r = check_route_http(args.base_url, route, None, None)
            # Milk has no manifest version; still try product count from page.
            if r.status == "PASS" and r.served_count is None:
                try:
                    _, body = fetch(args.base_url.rstrip("/") + route)
                    text = body.decode("utf-8", errors="ignore")
                    r.served_count = extract_product_count(text, None)
                except ConnectionError:
                    pass
            results.append(r)

    failures, _ = print_report(results, findings_total)
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()