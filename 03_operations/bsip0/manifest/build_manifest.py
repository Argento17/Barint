"""Build the authoritative BSIP0 nutrition-capture corpus manifest.

Membership policy: every JSON object beneath ``02_products`` or
``03_operations/bsip0`` which has a dictionary ``nutrition_raw_source`` containing
a list ``rows`` is one capture, irrespective of whether it is currently served.
Deduplication is by ``(retailer, gtin)`` only when both values are known.  The
canonical capture is selected newest scrape timestamp, then content stability
(the most frequently occurring canonical raw-source hash), then lexicographic
``capture_file``/``object_path``.  No capture is dropped: non-canonical members
remain in the manifest with ``superseded_by`` pointing to the canonical record.

This program writes only its declared manifest artifact; input corpus files are
read-only by construction.
"""
from __future__ import annotations

import hashlib
import json
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUTPUT = ROOT / "03_operations/bsip0/manifest/capture_manifest.json"
SCAN_ROOTS = (ROOT / "02_products", ROOT / "03_operations/bsip0")
RETAILERS = ("shufersal", "victory", "yohananof", "carrefour", "rami_levy", "tiv_taam")
GTIN_KEYS = ("gtin", "barcode", "ean", "upc", "product_code", "product_id")
TIME_KEYS = ("scrape_timestamp", "scraped_at", "captured_at", "timestamp", "fetched_at")


def assert_write_path(path: Path) -> None:
    if path.resolve() != OUTPUT.resolve():
        raise AssertionError(f"write outside TASK-601 boundary: {path}")


def pointer(parts: list[str]) -> str:
    return "/" + "/".join(p.replace("~", "~0").replace("/", "~1") for p in parts)


def walk(value, path: list[str]):
    if isinstance(value, dict):
        yield value, path
        for key, child in value.items():
            yield from walk(child, path + [str(key)])
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from walk(child, path + [str(index)])


def scalar(obj: dict, keys: tuple[str, ...]):
    for key in keys:
        value = obj.get(key)
        if value is not None and str(value).strip():
            return str(value).strip()
    return None


def infer_retailer(obj: dict, rel: str) -> str:
    for key in ("retailer", "store", "source_retailer", "source"):
        value = obj.get(key)
        if isinstance(value, str):
            low = value.lower().replace("-", "_").replace(" ", "_")
            if low in RETAILERS:
                return low
    low_path = rel.lower().replace("-", "_").replace(" ", "_")
    hits = [name for name in RETAILERS if name in low_path]
    return hits[0] if len(hits) == 1 else "unknown"


def filename_timestamp(name: str):
    match = re.search(r"(20\d{2})[-_]?([01]\d)[-_]?([0-3]\d)(?:[T_ -]?([0-2]\d)[-_:]?([0-5]\d)?(?:[_:]?([0-5]\d)?)?)?", name)
    if not match:
        return None
    y, mo, d, h, mi, sec = match.groups()
    try:
        return datetime(int(y), int(mo), int(d), int(h or 0), int(mi or 0), int(sec or 0)).isoformat() + "Z"
    except ValueError:
        return None


def timestamp(obj: dict, file_name: str):
    value = scalar(obj, TIME_KEYS) or filename_timestamp(file_name)
    return value if value else None


def timestamp_key(value):
    if not value:
        return (0, "")
    return (1, str(value))


def main() -> int:
    records = []
    for scan_root in SCAN_ROOTS:
        for path in sorted(scan_root.rglob("*.json")):
            if path.resolve() == OUTPUT.resolve():
                continue
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, UnicodeDecodeError):
                continue
            rel = path.relative_to(ROOT).as_posix()
            for obj, obj_path in walk(data, []):
                raw = obj.get("nutrition_raw_source")
                if not isinstance(raw, dict) or not isinstance(raw.get("rows"), list):
                    continue
                canonical_raw = json.dumps(raw, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
                records.append({
                    "retailer": infer_retailer(obj, rel),
                    "gtin": scalar(obj, GTIN_KEYS),
                    "capture_file": rel,
                    "object_path": pointer(obj_path),
                    "scrape_timestamp": timestamp(obj, path.name),
                    "content_hash": hashlib.sha256(canonical_raw.encode("utf-8")).hexdigest(),
                    "parser_notes": obj.get("parser_notes") if isinstance(obj.get("parser_notes"), str) else None,
                    "canonical": True,
                    "superseded_by": None,
                })
    groups = defaultdict(list)
    for i, record in enumerate(records):
        # ``unknown`` is an explicit, non-guessed retailer value.  It remains a
        # valid dedup dimension: two unknown-retailer captures of the same GTIN
        # are still competing capture observations, never silently duplicated.
        if record["gtin"]:
            groups[(record["retailer"], record["gtin"])].append(i)
    for members in groups.values():
        stability = Counter(records[i]["content_hash"] for i in members)
        winner = sorted(members, key=lambda i: (timestamp_key(records[i]["scrape_timestamp"]), stability[records[i]["content_hash"]], records[i]["capture_file"], records[i]["object_path"]), reverse=True)[0]
        ref = f"{records[winner]['capture_file']}#{records[winner]['object_path']}"
        for i in members:
            if i != winner:
                records[i]["canonical"] = False
                records[i]["superseded_by"] = ref
    records.sort(key=lambda r: (r["capture_file"], r["object_path"]))
    payload = {"schema": "bsip0_capture_manifest_v1", "records": records}
    assert_write_path(OUTPUT)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    canonical = [r for r in records if r["canonical"]]
    print(json.dumps({"total_captures": len(records), "canonical": len(canonical), "duplicates_superseded": len(records) - len(canonical), "distinct_gtins": len({r['gtin'] for r in canonical if r['gtin']}), "retailers": dict(sorted(Counter(r['retailer'] for r in records).items()))}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
