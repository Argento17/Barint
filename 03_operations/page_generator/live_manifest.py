#!/usr/bin/env python3
"""
live_manifest.py — Route-derived live manifest (TASK-466 / P474 rework).

Source of truth is the Next.js app directory: every bari-web/src/app/hashvaot/*/page.tsx
route (plus the /hashvaot index). For each route, statically resolves:
  page.tsx -> page-data TS -> src/data/comparisons/*.json

comparisonCategoryRegistry is an annotation (in_comparison_registry), not the filter.
Consumed by conformance.py --all and CI drift gate.

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
HASHVAOT_APP = REPO / "bari-web" / "src" / "app" / "hashvaot"
COMPARISONS_LIB = REPO / "bari-web" / "src" / "lib" / "comparisons"
REGISTRY_INDEX = COMPARISONS_LIB / "registry" / "index.ts"
CATALOG_ROUTE = HASHVAOT_APP / "catalog" / "page.tsx"

OTHER_VERTICAL_SLUGS = frozenset({
    "magnesium",
    "supplements",
    "personal-care",
    "raw-foods",
})
HUB_SLUGS = frozenset({"supermarket"})

ROUTE_CONFIG_ALIASES: dict[str, str] = {
    "milk-comparison": "milk",
    "breakfast-cereals": "cereals",
}

PAGE_DATA_IMPORT_RE = re.compile(
    r'from\s+"@/lib/comparisons/([^"]+)"'
)
IMPORT_JSON_RE = re.compile(
    r'import\s+\w+\s+from\s+"@/data/(?:comparisons/)?([^"]+\.json)"'
)


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


def parse_registry_ids(src: str) -> set[str]:
    block = re.search(
        r"comparisonCategoryRegistry\s*=\s*\{(.*?)\}\s*as const",
        src,
        re.DOTALL,
    )
    if not block:
        return set()
    ids: set[str] = set()
    for m in re.finditer(
        r'["\']?([\w-]+)["\']?\s*:\s*\w+CategoryDefinition', block.group(1)
    ):
        ids.add(m.group(1))
    return ids


def enumerate_route_slugs() -> list[str]:
    slugs: list[str] = []
    if not HASHVAOT_APP.is_dir():
        return slugs
    for child in sorted(HASHVAOT_APP.iterdir()):
        if not child.is_dir():
            continue
        if (child / "page.tsx").is_file():
            slugs.append(child.name)
    return slugs


def parse_page_data_import(page_tsx: Path) -> str | None:
    src = load_text(page_tsx)
    m = PAGE_DATA_IMPORT_RE.search(src)
    if not m:
        return None
    rel = m.group(1)
    if not rel.endswith(".ts"):
        rel = f"{rel}.ts"
    return rel


def resolve_page_data_ts(module_rel: str) -> tuple[str | None, list[str]]:
    gaps: list[str] = []
    page_data = COMPARISONS_LIB / module_rel
    if not page_data.is_file():
        gaps.append(f"page-data file missing: {repo_rel(page_data)}")
        return None, gaps
    return repo_rel(page_data), gaps


def _json_import_to_repo_rel(match: re.Match[str]) -> str:
    full = match.group(0)
    rel_name = match.group(1)
    if rel_name.startswith("comparisons/"):
        return f"bari-web/src/data/{rel_name}"
    if "/comparisons/" in full:
        return f"bari-web/src/data/comparisons/{rel_name}"
    return f"bari-web/src/data/{rel_name}"


def resolve_frontend_json(page_data_ts: Path) -> tuple[str | None, list[str], list[str]]:
    gaps: list[str] = []
    src = load_text(page_data_ts)
    matches = list(IMPORT_JSON_RE.finditer(src))
    if not matches:
        gaps.append(f"no @/data/comparisons/*.json import in {repo_rel(page_data_ts)}")
        return None, gaps, []

    all_imports: list[str] = []
    for m in matches:
        rel = _json_import_to_repo_rel(m)
        all_imports.append(rel)
        if not (REPO / rel).is_file():
            gaps.append(f"frontend JSON missing on disk: {rel}")

    comparisons_hits = [
        m for m in matches if m.group(1).startswith("comparisons/")
        or "/comparisons/" in m.group(0)
    ]
    chosen = comparisons_hits[0] if comparisons_hits else matches[0]
    primary = _json_import_to_repo_rel(chosen)
    return primary, gaps, sorted(set(all_imports))


def resolve_config_json(route_slug: str) -> tuple[str | None, list[str]]:
    gaps: list[str] = []
    alias = ROUTE_CONFIG_ALIASES.get(route_slug, route_slug)

    direct = CONFIGS_DIR / f"{alias}.json"
    if direct.is_file():
        return repo_rel(direct), gaps

    underscored = CONFIGS_DIR / f"{alias.replace('-', '_')}.json"
    if underscored.is_file():
        return repo_rel(underscored), gaps

    target = norm(alias)
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
            f"ambiguous config match for route={route_slug}: "
            f"{', '.join(p.name for p in matches)}"
        )
        return repo_rel(matches[0]), gaps

    return None, gaps


def route_type_for_slug(route_slug: str, *, is_index: bool = False) -> str:
    if is_index or route_slug in HUB_SLUGS:
        return "hub"
    if route_slug in OTHER_VERTICAL_SLUGS:
        return "other-vertical"
    return "comparison"


def derive_route(
    route_slug: str,
    *,
    registry_ids: set[str],
    is_index: bool = False,
) -> dict[str, Any]:
    gaps: list[str] = []
    route = "/hashvaot" if is_index else f"/hashvaot/{route_slug}"
    route_type = route_type_for_slug(route_slug, is_index=is_index)

    if is_index:
        return {
            "route_slug": "(index)",
            "route": route,
            "type": "hub",
            "page_tsx": repo_rel(HASHVAOT_APP / "page.tsx"),
            "in_comparison_registry": False,
        }

    page_tsx = HASHVAOT_APP / route_slug / "page.tsx"
    entry: dict[str, Any] = {
        "route_slug": route_slug,
        "route": route,
        "type": route_type,
        "page_tsx": repo_rel(page_tsx),
        "in_comparison_registry": route_slug in registry_ids,
    }

    if route_type != "comparison":
        return entry

    module_rel = parse_page_data_import(page_tsx)
    page_data_rel = None
    if module_rel:
        page_data_rel, pd_gaps = resolve_page_data_ts(module_rel)
        gaps.extend(pd_gaps)
    else:
        gaps.append(f"no @/lib/comparisons/* import in {repo_rel(page_tsx)}")

    frontend_json = None
    imported_jsons: list[str] = []
    if page_data_rel:
        frontend_json, fj_gaps, imported_jsons = resolve_frontend_json(REPO / page_data_rel)
        gaps.extend(fj_gaps)

    if page_data_rel:
        entry["page_data_ts"] = page_data_rel
    if frontend_json:
        entry["frontend_json"] = frontend_json
    if len(imported_jsons) > 1:
        entry["imported_jsons"] = imported_jsons

    config_json, cfg_gaps = resolve_config_json(route_slug)
    gaps.extend(cfg_gaps)
    if config_json:
        entry["config_json"] = config_json
        entry["config_stem"] = Path(config_json).stem
    elif not cfg_gaps:
        gaps.append(f"no page_generator config for live comparison route={route_slug}")

    if not frontend_json:
        gaps.append(f"comparison route {route_slug} has no resolvable frontend JSON")

    if gaps:
        entry["gaps"] = sorted(set(gaps))
    return entry


def build_manifest() -> dict[str, Any]:
    registry_ids: set[str] = set()
    if REGISTRY_INDEX.is_file():
        registry_ids = parse_registry_ids(load_text(REGISTRY_INDEX))

    routes: list[dict[str, Any]] = []

    index_page = HASHVAOT_APP / "page.tsx"
    if index_page.is_file():
        routes.append(
            derive_route("(index)", registry_ids=registry_ids, is_index=True)
        )

    for slug in enumerate_route_slugs():
        routes.append(derive_route(slug, registry_ids=registry_ids))

    catalog_note = None
    if CATALOG_ROUTE.is_file():
        routes.append({
            "route_slug": "catalog",
            "route": "/hashvaot/catalog",
            "type": "hub",
            "page_tsx": repo_rel(CATALOG_ROUTE),
            "in_comparison_registry": False,
        })
    else:
        catalog_note = "/hashvaot/catalog page.tsx not present (skipped)"

    comparison_count = sum(1 for r in routes if r.get("type") == "comparison")
    meta: dict[str, Any] = {
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": "bari-web/src/app/hashvaot/*/page.tsx (derived, static parse)",
        "route_count": len(routes),
        "comparison_route_count": comparison_count,
    }
    if catalog_note:
        meta["catalog_note"] = catalog_note

    return {"_meta": meta, "routes": routes}


def manifest_routes(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    return manifest.get("routes") or manifest.get("categories") or []


def write_manifest(path: Path = MANIFEST_PATH) -> dict[str, Any]:
    manifest = build_manifest()
    text = json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    path.write_text(text, encoding="utf-8")
    return manifest


def load_committed_manifest(path: Path = MANIFEST_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_for_drift(manifest: dict[str, Any]) -> str:
    copy = json.loads(json.dumps(manifest, ensure_ascii=False, sort_keys=True))
    meta = copy.get("_meta", {})
    meta.pop("generated", None)
    copy["_meta"] = meta
    return json.dumps(copy, ensure_ascii=False, indent=2, sort_keys=True)


def manifest_frontend_files(manifest: dict[str, Any]) -> set[str]:
    out: set[str] = set()
    for route in manifest_routes(manifest):
        for key in ("imported_jsons", "frontend_json"):
            val = route.get(key)
            if isinstance(val, list):
                out.update(v.replace("\\", "/") for v in val)
            elif val:
                out.add(val.replace("\\", "/"))
    return out


def comparison_routes_with_config(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        r for r in manifest_routes(manifest)
        if r.get("type") == "comparison" and r.get("config_json")
    ]


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
        routes = list(manifest_routes(fresh))
        for i, route in enumerate(routes):
            if route.get("type") == "comparison" and route.get("frontend_json"):
                routes[i] = dict(route)
                routes[i]["frontend_json"] = routes[i]["frontend_json"] + ".DRIFT_SIM"
                break
        fresh = dict(fresh)
        fresh["routes"] = routes

    if canonical_for_drift(committed) != canonical_for_drift(fresh):
        if simulate:
            errors.append(
                "DRIFT (simulate): committed manifest differs from fresh derivation"
            )
        else:
            errors.append("committed live_manifest.json is stale (re-run generator)")

    manifest_files = manifest_frontend_files(committed)

    for route in manifest_routes(committed):
        fj = route.get("frontend_json")
        if fj and not (REPO / fj).is_file():
            errors.append(f"manifest frontend_json missing on disk: {fj}")

    for route in manifest_routes(committed):
        if route.get("type") != "comparison":
            continue
        page_data = route.get("page_data_ts")
        if not page_data:
            continue
        page_path = REPO / page_data
        if not page_path.is_file():
            continue
        src = load_text(page_path)
        for m in IMPORT_JSON_RE.finditer(src):
            rel = _json_import_to_repo_rel(m)
            if rel not in manifest_files:
                errors.append(
                    f"live route imports {rel} but it is not in manifest "
                    f"(route={route.get('route_slug')})"
                )

    live_config_stems = {
        Path(r["config_json"]).stem
        for r in comparison_routes_with_config(committed)
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
    parser = argparse.ArgumentParser(description="Route-derived live manifest.")
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
            f"live_manifest.json written: {manifest['_meta']['route_count']} routes "
            f"({manifest['_meta']['comparison_route_count']} comparison)"
        )
        for route in manifest["routes"]:
            gap_note = f"  gaps={route['gaps']}" if route.get("gaps") else ""
            print(
                f"  {route.get('route_slug', '?'):22s} "
                f"[{route.get('type', '?'):14s}] "
                f"{route.get('frontend_json') or '(no json)'}{gap_note}"
            )
    return 0


if __name__ == "__main__":
    sys.exit(main())