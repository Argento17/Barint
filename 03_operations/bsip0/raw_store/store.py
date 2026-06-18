"""
store.py — Raw evidence store for BSIP0.5.

Persistence layer: saves raw HTTP responses as HTML files and maintains a
manifest.jsonl per category. content_sha256 = hash of raw bytes — the Leap 4
change-detection substrate.

Layout:
  raw_store/<retailer>/<category>/<barcode-or-pageid>/<fetch_ts>.html
  raw_store/<retailer>/<category>/manifest.jsonl
"""
from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STORE_ROOT = Path(__file__).resolve().parent


def _ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def _page_dir(retailer: str, category: str, page_id: str) -> Path:
    return _ensure_dir(STORE_ROOT / retailer / category / page_id)


def _manifest_path(retailer: str, category: str) -> Path:
    return STORE_ROOT / retailer / category / "manifest.jsonl"


def store_page(
    content: bytes,
    retailer: str,
    category: str,
    page_id: str,
    url: str,
    barcode_hint: str = "",
    http_status: int = 200,
    fetch_engine: str = "requests",
) -> dict[str, Any]:
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%f")
    sha256 = hashlib.sha256(content).hexdigest()
    pdir = _page_dir(retailer, category, page_id)
    fname = f"{ts}.html"
    (pdir / fname).write_bytes(content)

    entry = {
        "url": url,
        "retailer": retailer,
        "category": category,
        "barcode_hint": barcode_hint,
        "page_id": page_id,
        "fetch_ts": ts,
        "content_sha256": sha256,
        "http_status": http_status,
        "bytes": len(content),
        "fetch_engine": fetch_engine,
        "filename": f"{retailer}/{category}/{page_id}/{fname}",
    }
    mpath = _manifest_path(retailer, category)
    with open(mpath, "a", encoding="utf-8") as mf:
        mf.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry


def _read_manifest(retailer: str, category: str) -> list[dict[str, Any]]:
    mpath = _manifest_path(retailer, category)
    if not mpath.exists():
        return []
    entries: list[dict[str, Any]] = []
    with open(mpath, "r", encoding="utf-8") as mf:
        for line in mf:
            line = line.strip()
            if line:
                entries.append(json.loads(line))
    return entries


def latest(retailer: str, category: str, barcode_or_pageid: str) -> dict[str, Any] | None:
    """Return the most recent manifest entry for a given page."""
    entries = [
        e for e in _read_manifest(retailer, category)
        if e.get("page_id") == barcode_or_pageid or e.get("barcode_hint") == barcode_or_pageid
    ]
    if not entries:
        return None
    entries.sort(key=lambda e: e["fetch_ts"], reverse=True)
    return entries[0]


def latest_content(
    retailer: str, category: str, barcode_or_pageid: str
) -> bytes | None:
    """Return the raw bytes of the most recent fetch for a page."""
    entry = latest(retailer, category, barcode_or_pageid)
    if entry is None:
        return None
    fpath = STORE_ROOT / entry["filename"]
    if not fpath.exists():
        return None
    return fpath.read_bytes()


def changed_since_last_fetch(
    retailer: str, category: str, barcode_or_pageid: str, new_sha256: str
) -> bool | None:
    """Return True if content changed since last fetch, False if same, None if no prior fetch."""
    entry = latest(retailer, category, barcode_or_pageid)
    if entry is None:
        return None
    return entry["content_sha256"] != new_sha256


def manifest_entries(retailer: str, category: str) -> list[dict[str, Any]]:
    return _read_manifest(retailer, category)


def all_barcodes(retailer: str, category: str) -> set[str]:
    """Return all unique barcode_hint values in the manifest."""
    barcodes: set[str] = set()
    for e in _read_manifest(retailer, category):
        bh = e.get("barcode_hint", "").strip()
        if bh:
            barcodes.add(bh)
    return barcodes


def page_count(retailer: str, category: str) -> int:
    mpath = _manifest_path(retailer, category)
    if not mpath.exists():
        return 0
    count = 0
    with open(mpath, "r", encoding="utf-8") as mf:
        for line in mf:
            if line.strip():
                count += 1
    return count
