"""
scaffold_category.py — new comparison category frontend-route scaffolder

CANONICAL CONVENTION (this scaffolder is the source of truth for new categories):
  - Loader file:  src/lib/comparisons/<slug>-page-data.ts   (the dominant pattern, 9 cats)
  - LEGACY EXCEPTIONS (do NOT copy — pre-scaffolder): hummus, snacks, bread use
    `<slug>-comparison-page-data.ts`. New categories MUST use `-page-data.ts`.
  - Metadata: exported `*ComparisonMetadata` const from the page-data file (not inline).
  - JSON shape: standard `_meta` + `products` wrapper via loadComparisonCorpus. The
    juices category uses a bespoke FLAT schema — a new category in that shape needs a
    manual loader override (the scaffolder assumes the standard wrapper).

Usage:
    python 03_operations/page_generator/scaffold_category.py \
        --category <slug> \
        --json <frontend_json_filename>

    <slug>              Hyphenated category slug, e.g. "olive-oil"
                        Must match the hashvaot route: /hashvaot/<slug>
    --json <name>       Filename (no path) of the frontend JSON under
                        bari-web/src/data/comparisons/, e.g. olive_oil_frontend_v1.json
                        If omitted, the script tries to auto-detect by matching <slug>
                        (underscored) as a prefix in that directory.

Examples:
    python 03_operations/page_generator/scaffold_category.py --category olive-oil \\
        --json olive_oil_frontend_v1.json

    python 03_operations/page_generator/scaffold_category.py --category cottage \\
        --json cottage_frontend_v1.json

What it emits (5 files, then 3 patch points):
    bari-web/src/lib/comparisons/<slug>-page-data.ts
    bari-web/src/components/comparisons/<slug>-comparison-page.tsx
    bari-web/src/app/hashvaot/<slug>/page.tsx
    bari-web/src/lib/comparisons/registry/categories/<slug>.ts
    — then patches registry/index.ts, registry/types.ts, app/sitemap.ts

Idempotent: warns and skips if a file already exists; does NOT clobber.
"""

import argparse
import os
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Repo layout constants
# ---------------------------------------------------------------------------
# This script lives at 03_operations/page_generator/scaffold_category.py.
# The repo root is two directories up.
SCRIPT_DIR = Path(__file__).parent.resolve()
REPO_ROOT = SCRIPT_DIR.parent.parent.resolve()
BARI_WEB = REPO_ROOT / "bari-web"

DATA_DIR = BARI_WEB / "src" / "data" / "comparisons"
LIB_COMPARISONS = BARI_WEB / "src" / "lib" / "comparisons"
COMPONENTS_COMPARISONS = BARI_WEB / "src" / "components" / "comparisons"
REGISTRY_DIR = LIB_COMPARISONS / "registry"
REGISTRY_CATEGORIES_DIR = REGISTRY_DIR / "categories"
HASHVAOT_DIR = BARI_WEB / "src" / "app" / "hashvaot"
SITEMAP = BARI_WEB / "src" / "app" / "sitemap.ts"
REGISTRY_INDEX = REGISTRY_DIR / "index.ts"
REGISTRY_TYPES = REGISTRY_DIR / "types.ts"

# ---------------------------------------------------------------------------
# Name derivation helpers
# ---------------------------------------------------------------------------

def slug_to_pascal(slug: str) -> str:
    """olive-oil  →  OliveOil"""
    return "".join(word.capitalize() for word in slug.split("-"))


def slug_to_camel(slug: str) -> str:
    """olive-oil  →  oliveOil"""
    pascal = slug_to_pascal(slug)
    return pascal[0].lower() + pascal[1:]


def slug_to_upper_snake(slug: str) -> str:
    """olive-oil  →  OLIVE_OIL"""
    return slug.replace("-", "_").upper()


def slug_to_snake(slug: str) -> str:
    """olive-oil  →  olive_oil"""
    return slug.replace("-", "_")


# ---------------------------------------------------------------------------
# Template generators
# ---------------------------------------------------------------------------

def make_page_data(slug: str, json_filename: str) -> str:
    camel = slug_to_camel(slug)
    pascal = slug_to_pascal(slug)
    upper = slug_to_upper_snake(slug)
    Camel = camel  # alias for readability

    return f'''\
import type {{ Metadata }} from "next";

import rawCorpus from "@/data/comparisons/{json_filename}";

import {{
  formatComparisonMetadataLine,
  loadComparisonCorpus,
  type ComparisonCorpusMeta,
  type ComparisonCorpusRaw,
}} from "@/lib/comparisons/corpus";
import type {{ ComparisonCategoryPageData }} from "@/lib/comparisons/registry/types";
import type {{ BariProductVM }} from "@/lib/view-models";

// TODO(filters): define {pascal}ShelfFilterId and the filter function in
//   src/lib/comparisons/{slug}-shelf-filters.ts, then replace the stub below.
export type {pascal}ShelfFilterId = string;

export type {pascal}CorpusMeta = ComparisonCorpusMeta;

function is{pascal}ShelfFilterId(filter: string): filter is {pascal}ShelfFilterId {{
  // TODO(filters): replace this stub once {slug}-shelf-filters.ts exists.
  void filter;
  return false;
}}

const {{ meta: {Camel}CorpusMeta, products: {Camel}Products }} =
  loadComparisonCorpus(rawCorpus as ComparisonCorpusRaw);

export {{ {Camel}CorpusMeta, {Camel}Products }};

export const {Camel}MetadataLine = formatComparisonMetadataLine(
  {Camel}Products.length,
  {Camel}CorpusMeta.generated
);

// TODO(content): author Hebrew hero copy for {slug}
export const {Camel}Hero = {{
  eyebrow: "TODO — eyebrow Hebrew label for {slug}",
  title: "TODO — hero title Hebrew for {slug}",
}} as const;

// TODO(content): author Hebrew prologue sentences for {slug} (3–5 sentences)
export const {Camel}PrologueSentences = [
  "TODO — משפט פתיחה 1",
  "TODO — משפט פתיחה 2",
] as const;

// TODO(content): author Hebrew category caveat for {slug}
export const {Camel}CategoryNote =
  "הערת קטגוריה — TODO";

// TODO(content): author Hebrew methodology lines for {slug} (2–4 lines)
export const {Camel}MethodologyLines = [
  "TODO — שורת מתודולוגיה 1",
  "TODO — שורת מתודולוגיה 2",
] as const;

// TODO(content): fill in accurate Hebrew title + description for SEO
export const {Camel}ComparisonMetadata: Metadata = {{
  title: "השוואת {slug} | Bari",
  description: "TODO — description for {slug}",
}};

// TODO(filters): wire the real shelf filter here once the filter file exists.
const {Camel}ShelfFilters = {{
  lensOptions: [] as Array<{{ id: {pascal}ShelfFilterId; label: string }}>,
  filterProducts: (products: BariProductVM[], activeFilters: string[]) => {{
    void activeFilters.filter(is{pascal}ShelfFilterId);
    return products;
  }},
}};

export function get{pascal}PageData(): ComparisonCategoryPageData {{
  return {{
    products: {Camel}Products,
    metadataLine: {Camel}MetadataLine,
    hero: {Camel}Hero,
    prologueSentences: {Camel}PrologueSentences,
    methodologyLines: {Camel}MethodologyLines,
    corpusMeta: {Camel}CorpusMeta,
    shelfFilters: {Camel}ShelfFilters,
  }};
}}

export function get{pascal}CorpusPayload(): {{
  _meta: {pascal}CorpusMeta;
  products: BariProductVM[];
}} {{
  return {{
    _meta: {Camel}CorpusMeta,
    products: {Camel}Products,
  }};
}}
'''


def make_comparison_page_component(slug: str) -> str:
    pascal = slug_to_pascal(slug)
    camel = slug_to_camel(slug)
    page_data_import = f"{slug}-page-data"

    return f'''\
"use client";

import {{ ComparisonPage }} from "@/components/comparisons/comparison-page";
import {{
  type {pascal}ShelfFilterId,
}} from "@/lib/comparisons/{page_data_import}";
import type {{ BariProductVM }} from "@/lib/view-models";

export interface {pascal}ComparisonPageProps {{
  products: BariProductVM[];
  metadataLine: string;
  hero: {{
    eyebrow: string;
    title: string;
  }};
  prologueSentences: readonly string[];
  methodologyLines: readonly string[];
  categoryNote?: string;
  initialExpandedProductId?: string | null;
}}

// TODO(filters): replace the empty shelfFilters stub once {slug}-shelf-filters.ts exists.
// Import filterProducts + LENS_OPTIONS from "@/lib/comparisons/{slug}-shelf-filters"
// and wire them here (see hummus-comparison-page.tsx or cereals-comparison-page.tsx).
const {camel}ShelfFilters = {{
  lensOptions: [] as Array<{{ id: {pascal}ShelfFilterId; label: string }}>,
  filterProducts: (products: BariProductVM[], _activeFilters: {pascal}ShelfFilterId[]) =>
    products,
}} as const;

// TODO(filters): define the metric column spec for {slug}.
// Use [] if no single headline numeric signal exists (see cereals-comparison-page.tsx),
// or compose from PROTEIN_METRIC / SUGAR_METRIC / FIBER_METRIC constants in
// "@/components/shared/comparison-metric-column" (see hummus / juices / granola).
const {slug.upper().replace("-", "_")}_METRIC_SPECS = [] as const;

export function {pascal}ComparisonPage({{
  products,
  metadataLine,
  hero,
  prologueSentences,
  methodologyLines,
  categoryNote,
  initialExpandedProductId = null,
}}: {pascal}ComparisonPageProps) {{
  return (
    <ComparisonPage<{pascal}ShelfFilterId>
      products={{products}}
      metadataLine={{metadataLine}}
      hero={{hero}}
      prologueSentences={{prologueSentences}}
      methodologyLines={{methodologyLines}}
      shelfFilters={{{camel}ShelfFilters}}
      metricSpecs={{{slug.upper().replace("-", "_")}_METRIC_SPECS}}
      categoryNote={{categoryNote}}
      initialExpandedProductId={{initialExpandedProductId}}
      category="{slug}"
    />
  );
}}
'''


def make_route(slug: str) -> str:
    pascal = slug_to_pascal(slug)
    camel = slug_to_camel(slug)
    page_data_import = f"{slug}-page-data"

    return f'''\
import type {{ Metadata }} from "next";

import {{ {pascal}ComparisonPage }} from "@/components/comparisons/{slug}-comparison-page";
import {{
  {camel}CategoryNote,
  {camel}ComparisonMetadata,
  {camel}Hero,
  {camel}MetadataLine,
  {camel}MethodologyLines,
  {camel}PrologueSentences,
  {camel}Products,
}} from "@/lib/comparisons/{page_data_import}";

export const metadata: Metadata = {camel}ComparisonMetadata;

export default function {pascal}ComparisonRoute() {{
  return (
    <{pascal}ComparisonPage
      products={{{camel}Products}}
      metadataLine={{{camel}MetadataLine}}
      hero={{{camel}Hero}}
      prologueSentences={{{camel}PrologueSentences}}
      methodologyLines={{{camel}MethodologyLines}}
      categoryNote={{{camel}CategoryNote}}
    />
  );
}}
'''


def make_registry_category(slug: str) -> str:
    pascal = slug_to_pascal(slug)
    camel = slug_to_camel(slug)
    page_data_import = f"{slug}-page-data"

    return f'''\
import type {{ ComparisonCategoryDefinition }} from "../types";
import {{
  get{pascal}CorpusPayload,
  get{pascal}PageData,
  {camel}ComparisonMetadata,
}} from "../../{page_data_import}";

export const {camel}CategoryDefinition: ComparisonCategoryDefinition = {{
  id: "{slug}",
  routePath: "/hashvaot/{slug}",
  metadata: {camel}ComparisonMetadata,
  getPageData: get{pascal}PageData,
  getCorpusPayload: get{pascal}CorpusPayload,
}};
'''


# ---------------------------------------------------------------------------
# Patch helpers
# ---------------------------------------------------------------------------

def write_file(path: Path, content: str) -> bool:
    """Write content to path. Return True if written, False if skipped (exists)."""
    if path.exists():
        print(f"  SKIP (exists): {path.relative_to(REPO_ROOT)}")
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"  WRITE: {path.relative_to(REPO_ROOT)}")
    return True


def patch_registry_index(slug: str) -> None:
    """Insert import + registry entry into registry/index.ts."""
    camel = slug_to_camel(slug)
    pascal = slug_to_pascal(slug)

    src = REGISTRY_INDEX.read_text(encoding="utf-8")

    import_line = f'import {{ {camel}CategoryDefinition }} from "./categories/{slug}";'
    if import_line in src:
        print(f"  SKIP patch registry/index.ts import (already present)")
    else:
        # Insert before the first `import type` line (which ends the concrete imports block)
        src = _insert_before_first_match(
            src,
            r'^import type \{',
            import_line + "\n",
        )
        print(f"  PATCH registry/index.ts — import added")

    registry_entry = f'  "{slug}": {camel}CategoryDefinition,'
    if registry_entry in src:
        print(f"  SKIP patch registry/index.ts registry entry (already present)")
    else:
        # Insert before the closing `} as const satisfies ...` line
        src = _insert_before_first_match(
            src,
            r'^\} as const satisfies',
            "  " + registry_entry.strip() + "\n",
        )
        print(f"  PATCH registry/index.ts — registry entry added")

    REGISTRY_INDEX.write_text(src, encoding="utf-8")


def patch_registry_types(slug: str) -> None:
    """Add slug to the ComparisonCategoryId union in registry/types.ts."""
    src = REGISTRY_TYPES.read_text(encoding="utf-8")

    if f'"{slug}"' in src:
        print(f"  SKIP patch registry/types.ts (slug already present)")
        return

    # Find the ComparisonCategoryId type line and append to the union
    # Pattern: export type ComparisonCategoryId = "bread" | "snacks" | ...;
    new_src = re.sub(
        r'(export type ComparisonCategoryId\s*=\s*)([^;]+)(;)',
        lambda m: m.group(1) + m.group(2).rstrip() + f' | "{slug}"' + m.group(3),
        src,
        count=1,
    )
    if new_src == src:
        print(f"  WARN: could not patch ComparisonCategoryId in registry/types.ts — add manually: | \"{slug}\"")
        return

    REGISTRY_TYPES.write_text(new_src, encoding="utf-8")
    print(f"  PATCH registry/types.ts — \"{slug}\" added to ComparisonCategoryId")


def patch_sitemap(slug: str) -> None:
    """Add /hashvaot/<slug> to the STATIC_PATHS array in sitemap.ts."""
    src = SITEMAP.read_text(encoding="utf-8")
    route = f'  "/hashvaot/{slug}",'

    if f'"/hashvaot/{slug}"' in src:
        print(f"  SKIP patch sitemap.ts (route already present)")
        return

    # Insert before the "/blog" line (always last hashvaot entry)
    new_src = _insert_before_first_match(src, r'^\s*"/blog"', route + "\n")
    if new_src == src:
        print(f"  WARN: could not auto-patch sitemap.ts — add manually: {route}")
        return

    SITEMAP.write_text(new_src, encoding="utf-8")
    print(f'  PATCH sitemap.ts — "/hashvaot/{slug}" added to STATIC_PATHS')


def _insert_before_first_match(text: str, pattern: str, insertion: str) -> str:
    """Return text with insertion placed before the first line matching pattern."""
    lines = text.splitlines(keepends=True)
    for i, line in enumerate(lines):
        if re.match(pattern, line):
            lines.insert(i, insertion)
            return "".join(lines)
    return text  # unchanged if no match


# ---------------------------------------------------------------------------
# Auto-detect JSON
# ---------------------------------------------------------------------------

def autodetect_json(slug: str) -> str | None:
    prefix = slug.replace("-", "_")
    candidates = sorted(DATA_DIR.glob(f"{prefix}*.json"))
    if candidates:
        return candidates[0].name
    return None


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scaffold a new Bari comparison category frontend route.",
    )
    parser.add_argument(
        "--category",
        required=True,
        help="Hyphenated category slug, e.g. olive-oil",
    )
    parser.add_argument(
        "--json",
        dest="json_filename",
        default=None,
        help="Frontend JSON filename under src/data/comparisons/ (auto-detected if omitted)",
    )
    args = parser.parse_args()

    slug: str = args.category.strip().lower()
    if not re.match(r'^[a-z][a-z0-9-]*$', slug):
        sys.exit(f"ERROR: --category must be a hyphenated lowercase slug, got: {slug!r}")

    json_filename: str | None = args.json_filename
    if json_filename is None:
        json_filename = autodetect_json(slug)
        if json_filename is None:
            sys.exit(
                f"ERROR: no frontend JSON found for slug '{slug}' in {DATA_DIR}.\n"
                f"       Pass --json <filename> explicitly."
            )
        print(f"  Auto-detected JSON: {json_filename}")
    else:
        json_path = DATA_DIR / json_filename
        if not json_path.exists():
            sys.exit(
                f"ERROR: {json_path} does not exist.\n"
                f"       Check the filename or generate the frontend JSON first."
            )

    print(f"\nScaffolding category: {slug}")
    print(f"Frontend JSON:        {json_filename}")
    print(f"Repo root:            {REPO_ROOT}")
    print()

    # 1. Page data loader
    page_data_path = LIB_COMPARISONS / f"{slug}-page-data.ts"
    write_file(page_data_path, make_page_data(slug, json_filename))

    # 2. Comparison page wrapper component
    component_path = COMPONENTS_COMPARISONS / f"{slug}-comparison-page.tsx"
    write_file(component_path, make_comparison_page_component(slug))

    # 3. Route
    route_path = HASHVAOT_DIR / slug / "page.tsx"
    write_file(route_path, make_route(slug))

    # 4. Registry category definition
    reg_cat_path = REGISTRY_CATEGORIES_DIR / f"{slug}.ts"
    write_file(reg_cat_path, make_registry_category(slug))

    # 5. Patches
    print()
    patch_registry_index(slug)
    patch_registry_types(slug)
    patch_sitemap(slug)

    print()
    print("=" * 70)
    print("SKELETON ONLY — this category is NOT publish-ready. A green build proves")
    print("the wiring compiles, NOT that the page is content-complete or correct.")
    print("=" * 70)
    print("Post-scaffold checklist (all required before go-live):")
    print(f"  1. Author Hebrew copy in: src/lib/comparisons/{slug}-page-data.ts")
    print(f"     (search for TODO(content) — placeholders, not real copy)")
    print(f"  2. Define shelf filters/metrics in: src/lib/comparisons/{slug}-shelf-filters.ts")
    print(f"     (search for TODO(filters) in the page-data and component files)")
    print(f"  3. Verify the frontend JSON shape: standard is _meta + products wrapper")
    print(f"     (juices-style FLAT schema needs a manual loader override here)")
    print(f"  4. Inspect the metadata block (title/description) in the route file")
    print(f"  5. Run: cd bari-web && npm run build")
    print(f"  6. Verify route renders: /hashvaot/{slug}")


if __name__ == "__main__":
    main()
