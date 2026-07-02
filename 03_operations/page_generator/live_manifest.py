#!/usr/bin/env python3
"""
live_manifest.py — Derived live-category manifest (TASK-466 / P473).

Parses the frontend comparisons registry (bari-web/src/lib/comparisons/registry/)
and each category's page-data import chain to produce a single machine-readable
manifest of live comparison categories. Consumed by conformance.py --all and CI.

Usage:
  python 03_operations/page_generator/live_manifest.py           # write manifest
  python 03_operations/page_generator/live_manifest.py --check # drift gate
  python 03_operations/page_generator/live_manifest.py --check --simulate-drift
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

THIS_DIR = Path(__file__).resolve().parent
REPO = THIS_DIR.parents[1]
MANIFEST_PATH = THIS_DIR / "live_manifest.json"
CONFIGS_DIR = THIS_DIR / "configs"
REGISTRY_DIR = REPO / "bari-web" / "src" / "lib" / "comparisons" / "registry"
REGISTRY_INDEX = REGISTRY_DIR / "index.ts"
REGISTRY_CATEGORIES_DIR = REGISTRY_DIR / "categories"
COMPARISONS_LIB = REPO / "bari-web" / "src" / "lib" / "comparisons"
WEB_DATA_DIR = REPO / "bari-web" / "src" / "data" / "comparisons"
PUBLIC_CORPUS_REGISTRY = REPO / "bari-web" / "src" / "lib" / "seo" / "public-corpus-registry.ts"

IMPORT_JSON_RE = re.compile(
    r'import\s+\w+\s+from\s+"@/data/comparisons/([\w.\-]+\.json)"\s*;'
)
PAGE_DATA_IMPORT_RE = re.compile(
    r'from\s+"\.\./\.\./([^"]+)"\s*;'
)
ROUTE_PATH_RE = re.compile(r'routePath:\s*"(/hashvaot/[^"]+)"')
CATEGORY_ID_RE = re.compile(r'\bid:\s*"([^"]+)"')
CATALOG_SLUG_RE = re.compile(r'^\s*["\']?([\w-]+)["\']?\s*:', re.MULTILINE)


def norm(s: str | None) -> str:
    return (s or "").strip().lower().replace("-", "_")


def repo_rel(path: Path | str) -> str:
    p = Path(path)
    if p.is_absolute():
        try:
            p = p.resolve().relative_to(REPO.resolve())
        except ValueError:
            return str(p).replace("\\", "/")
    return str(p).replace("\\", "/")


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_catalog_slugs(src: str) -> set[str]:
    block = re.search(r"CORPUS_BY_SLUG[^=]*=\s*\{(.*?)\n\};", src, re.DOTALL)
    if not block:
        return set()
    slugs: set[str] = set()
    for line in block.group(1).splitlines():
        m = CATALOG_SLUG_RE.match(line)
        if m:
            slugs.add(m.group(1))
    return slugs


def parse_registry_index_ids(src: str) -> list[str]:
    """Return category ids registered in comparisonCategoryRegistry (sorted)."""
    block = re.search(
        r"comparisonCategoryRegistry\s*=\s*\{(.*?)\}\s*as const",
        src,
        re.DOTALL,
    )
    if not block:
        return []
    ids: list[str] = []
    for m in re.finditer(r'["\']?([\w-]+)["\']?\s*:\s*\w+CategoryDefinition', block.group(1)):
        ids.append(m.group(1))
    return sorted(ids, key=norm)


def resolve_page_data_ts(category_ts: Path) -> tuple[str | None, list[str]]:
    """Follow category -> page-data import; return (repo-rel ts path, gaps)."""
    gaps: list[str] = []
    src = load_text(category_ts)
    m = PAGE_DATA_IMPORT_RE.search(src)
    if not m:
        gaps.append(f"no page-data import in {repo_rel(category_ts)}")
        return None, gaps
    rel = m.group(1)
    if not rel.endswith(".ts"):
        rel = f"{rel}.ts"
    page_data = COMPARISONS_LIB / rel
    if not page_data.is_file():
        gaps.append(f"page-data file missing: {repo_rel(page_data)}")
        return None, gaps
    return repo_rel(page_data), gaps


def resolve_frontend_json(page_data_ts: Path) -> tuple[str | None, list[str]]:
    gaps: list[str] = []
    src = load_text(page_data_ts)
    m = IMPORT_JSON_RE.search(src)
    if not m:
        gaps.append(f"no @/data/comparisons/*.json import in {repo_rel(page_data_ts)}")
        return None, gaps
    rel = f"bari-web/src/data/comparisons/{m.group(1)}"
    if not (REPO / rel).is_file():
        gaps.append(f"frontend JSON missing on disk: {rel}")
    return rel, gaps


def resolve_config_json(category_id: str) -> tuple[str | None, list[str]]:
    gaps: list[str] = []
    direct = CONFIGS_DIR / f"{category_id}.json"
    if direct.is_file():
        return repo_rel(direct), gaps

    alt = CONFIGS_DIR / f"{category_id.replace('-', '_')}.json"
    if alt.is_file():
        return repo_rel(alt), gaps

    target = norm(category_id)
    matches: list[Path] = []
    for cfg_path in sorted(CONFIGS_DIR.glob("*.json")):
        if cfg_path.name.startswith("_generated_"):
            continue
        try:
            data = json.loads(cfg_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if norm(data.get("category")) == target:
            matches.append(cfg_path)

    if len(matches) == 1:
        return repo_rel(matches[0]), gaps
    if len(matches) > 1:
        gaps.append(
            f"ambiguous config match for {category_id}: "
            f"{', '.join(p.name for p in matches)}"
        )
        return repo_rel(matches[0]), gaps

    gaps.append(f"no config for category_id={category_id}")
    return None, gaps


def derive_category(category_id: str, catalog_slugs: set[str]) -> dict[str, Any]:
    gaps: list[str] = []
    cat_file = REGISTRY_CATEGORIES_DIR / f"{category_id}.ts"
    if not cat_file.is_file():
        gaps.append(f"registry category file missing: categories/{category_id}.ts")
        return {
            "category_id": category_id,
            "gaps": sorted(gaps),
        }

    cat_src = load_text(cat_file)
    route_m = ROUTE_PATH_RE.search(cat_src)
    route = route_m.group(1) if route_m else None
    if not route:
        gaps.append(f"routePath not resolved in {repo_rel(cat_file)}")

    page_data_rel, pd_gaps = resolve_page_data_ts(cat_file)
    gaps.extend(pd_gaps)

    frontend_json = None
    if page_data_rel:
        frontend_json, fj_gaps = resolve_frontend_json(REPO / page_data_rel)
        gaps.extend(fj_gaps)

    config_json, cfg_gaps = resolve_config_json(category_id)
    gaps.extend(cfg_gaps)

    entry: dict[str, Any] = {
        "category_id": category_id,
        "route": route,
        "frontend_json": frontend_json,
        "page_data_ts": page_data_rel,
        "config_json": config_json,
        "registered_in_catalog": category_id in catalog_slugs,
    }
    if gaps:
        entry["gaps"] = sorted(set(gaps))
    return entry


def build_manifest() -> dict[str, Any]:
    if not REGISTRY_INDEX.is_file():
        raise RuntimeError(f"registry index missing: {repo_rel(REGISTRY_INDEX)}")

    index_src = load_text(REGISTRY_INDEX)
    category_ids = parse_registry_index_ids(index_src)
    if not category_ids:
        raise RuntimeError("no categories found in comparisonCategoryRegistry")

    catalog_slugs: set[str] = set()
    if PUBLIC_CORPUS_REGISTRY.is_file():
        catalog_slugs = parse_catalog_slugs(load_text(PUBLIC_CORPUS_REGISTRY))

    categories = [derive_category(cid, catalog_slugs) for cid in category_ids]
    return {
        "_meta": {
            "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "source": "bari-web/src/lib/comparisons/registry (derived, static parse)",
            "category_count": len(categories),
        },
        "categories": categories,
    }


def write_manifest(path: Path = MANIFEST_PATH) -> dict[str, Any]:
    manifest = build_manifest()
    text = json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    path.write_text(text, encoding="utf-8")
    return manifest


def load_committed_manifest(path: Path = MANIFEST_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_for_drift(manifest: dict[str, Any]) -> str:
    """Stable JSON for drift comparison (exclude volatile _meta.generated timestamp)."""
    copy = json.loads(json.dumps(manifest, ensure_ascii=False, sort_keys=True))
    meta = copy.get("_meta", {})
    meta.pop("generated", None)
    copy["_meta"] = meta
    return json.dumps(copy, ensure_ascii=False, indent=2, sort_keys=True)


def manifest_frontend_files(manifest: dict[str, Any]) -> set[str]:
    out: set[str] = set()
    for cat in manifest.get("categories", []):
        fj = cat.get("frontend_json")
        if fj:
            out.add(fj.replace("\\", "/"))
    return out


def check_drift(*, simulate: bool = False) -> int:
    errors: list[str] = []
    warnings: list[str] = []

    if not MANIFEST_PATH.is_file():
        errors.append(f"committed manifest missing: {repo_rel(MANIFEST_PATH)}")
        _emit_check(errors, warnings)
        return 1

    committed = load_committed_manifest()
    fresh = build_manifest()

    if simulate:
        cats = fresh.get("categories", [])
        if cats and cats[0].get("frontend_json"):
            cats[0] = dict(cats[0])
            cats[0]["frontend_json"] = cats[0]["frontend_json"] + ".DRIFT_SIM"
            fresh = dict(fresh)
            fresh["categories"] = cats

    # (d) stale committed manifest (ignore volatile generated timestamp)
    committed_canon = canonical_for_drift(committed)
    fresh_canon = canonical_for_drift(fresh)
    if committed_canon != fresh_canon:
        if simulate:
            errors.append(
                "DRIFT (simulate): committed manifest differs from fresh derivation"
            )
        else:
            errors.append("committed live_manifest.json is stale (re-run generator)")

    manifest_files = manifest_frontend_files(committed)

    # (b) manifest names file that does not exist
    for cat in committed.get("categories", []):
        fj = cat.get("frontend_json")
        if fj and not (REPO / fj).is_file():
            errors.append(f"manifest frontend_json missing on disk: {fj}")

    # (a) live page imports JSON not in manifest
    for cat in committed.get("categories", []):
        page_data = cat.get("page_data_ts")
        if not page_data:
            continue
        page_path = REPO / page_data
        if not page_path.is_file():
            continue
        src = load_text(page_path)
        for m in IMPORT_JSON_RE.finditer(src):
            rel = f"bari-web/src/data/comparisons/{m.group(1)}"
            if rel not in manifest_files:
                errors.append(
                    f"live page imports {rel} but it is not in manifest "
                    f"(category={cat.get('category_id')})"
                )

    # (c) orphan configs — WARN not FAIL
    live_config_stems = {
        Path(c["config_json"]).stem
        for c in committed.get("categories", [])
        if c.get("config_json")
    }
    for cfg_path in sorted(CONFIGS_DIR.glob("*.json")):
        if cfg_path.name.startswith("_generated_"):
            continue
        if cfg_path.stem in live_config_stems:
            continue
        try:
            data = json.loads(cfg_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        cat_field = data.get("category")
        warnings.append(
            f"orphan config (no live page): {repo_rel(cfg_path)} "
            f"(category={cat_field})"
        )

    _emit_check(errors, warnings)
    return 1 if errors else 0


def _emit_check(errors: list[str], warnings: list[str]) -> None:
    if errors:
        print("LIVE_MANIFEST CHECK: FAIL", file=sys.stderr)
        for e in errors:
            print(f"  ERROR: {e}", file=sys.stderr)
    else:
        print("LIVE_MANIFEST CHECK: PASS")
    for w in warnings:
        print(f"  WARN: {w}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Derived live-category manifest.")
    parser.add_argument(
        "--check",
        action="store_true",
        help="exit nonzero on manifest drift / coverage gaps",
    )
    parser.add_argument(
        "--simulate-drift",
        action="store_true",
        help="with --check, inject synthetic drift to demonstrate failure",
    )
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="print manifest JSON to stdout instead of writing file",
    )
    args = parser.parse_args()

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]

    if args.check:
        return check_drift(simulate=args.simulate_drift)

    manifest = build_manifest()
    if args.stdout:
        print(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        write_manifest()
        print(
            f"live_manifest.json written: {manifest['_meta']['category_count']} categories"
        )
        for cat in manifest["categories"]:
            gap_note = f"  gaps={cat['gaps']}" if cat.get("gaps") else ""
            print(
                f"  {cat['category_id']:20s}  "
                f"{cat.get('frontend_json') or '(no json)'}{gap_note}"
            )
    return 0


if __name__ == "__main__":
    sys.exit(main())