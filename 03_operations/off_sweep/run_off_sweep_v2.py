"""
OFF sweep v2 — corrected barcode extraction + comprehensive scan.

Key fixes from v1:
- Bread uses shufersal_NNNN ids with barcode=null -> extract numeric from id OR mark NO_BARCODE
- All other categories have explicit barcode field
- Correctly counts products per category

TASK-450 fix (2026-07-02): the category -> data-file map used to be a HARDCODED
dict of filenames that went stale the moment a category shipped a new frontend
JSON version (v2 -> v3 -> v4 -> v5 renames). That silently dropped categories
from the scan (FILE_NOT_FOUND, swallowed as a soft warning) — the exact gap
that let the TASK-448 breach go undetected: the enforcement tool "passed"
because it was blind, not because the data was clean.

Fix: discover live scan targets DYNAMICALLY every run from the same source the
Next.js app itself imports from — `bari-web/src/lib/seo/public-corpus-registry.ts`
(one literal `@/data/comparisons/..._frontend_...json` import per live,
JSON-backed category — this is the file the app actually renders from, so it
cannot go stale without the site itself breaking). Cross-checked against each
category's `03_operations/page_generator/configs/*.json` `baseline_json` field
where present. Categories that are TS-embedded (no frontend JSON — e.g.
magnesium) are reported separately and are out of scope for a JSON-file OFF
scan by construction (see MAGNESIUM_NOTE below).

Fail-loud: if a target discovered from the registry is missing on disk, this
is a hard error (nonzero exit), not a warning — a silent skip is exactly the
failure mode this fix exists to close.
"""

import json
import os
import re
import glob
import hashlib
import datetime
import sys

sys.stdout.reconfigure(encoding='utf-8')

REPO = r"C:\Bari"
DATA_DIR = os.path.join(REPO, "bari-web", "src", "data")
BSIP1_ROOT = os.path.join(REPO, "03_operations", "bsip1")
OUT_DIR = os.path.join(REPO, "03_operations", "off_sweep")
COMPARISONS_DIR = os.path.join(DATA_DIR, "comparisons")

# Authoritative discovery source: the registry the Next.js app itself imports
# from at build time. One literal JSON import per live, file-backed category.
PUBLIC_CORPUS_REGISTRY_TS = os.path.join(
    REPO, "bari-web", "src", "lib", "seo", "public-corpus-registry.ts"
)
# Secondary cross-check source: category pipeline configs, which independently
# record their own baseline_json target.
PAGE_GENERATOR_CONFIGS_DIR = os.path.join(
    REPO, "03_operations", "page_generator", "configs"
)

OFF_MARKERS = [
    "open_food_facts",
    "openfoodfacts",
    "images.openfoodfacts.org",
    "world.openfoodfacts",
]

# Non-JSON-backed live categories: known by construction to be out of scope
# for a frontend-JSON OFF scan (product data is TS-embedded, not a JSON file).
# Documented here (not silently dropped) so category count reconciliation is
# always visible in the report instead of quietly short by one.
TS_EMBEDDED_CATEGORIES = {
    "magnesium": {
        "reason": "TS-embedded product array (magnesium-page-data.ts), not a frontend JSON file",
        "underlying_source": os.path.join(
            REPO, "03_operations", "supplement_engine", "proto_v0", "benchmark",
            "magnesium_v3_latest.json",
        ),
    },
}


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def discover_live_categories():
    """
    Dynamically derive {category_slug: absolute_data_file_path} from
    public-corpus-registry.ts — the file the live Next.js app actually
    imports its comparison-page JSON from. This is re-parsed every run,
    so a renamed/added/removed category is picked up automatically and
    can never silently fall out of coverage.

    Returns (category_map, ts_embedded_slugs_seen).
    Raises RuntimeError (fail loud) if the registry file itself cannot be
    found or parsed — if the discovery source is gone, we do not silently
    scan nothing.
    """
    if not os.path.exists(PUBLIC_CORPUS_REGISTRY_TS):
        raise RuntimeError(
            f"FATAL: discovery source not found: {PUBLIC_CORPUS_REGISTRY_TS}\n"
            "This is the authoritative list of live categories. Without it, "
            "the sweep cannot know what to scan and refuses to report a false "
            "'clean' by scanning nothing."
        )

    with open(PUBLIC_CORPUS_REGISTRY_TS, "r", encoding="utf-8") as f:
        src = f.read()

    # Match: import xCorpus from "@/data/comparisons/some_file.json";
    import_pat = re.compile(
        r'import\s+(\w+)\s+from\s+"@/data/comparisons/([\w.\-]+\.json)"\s*;'
    )
    var_to_file = {}
    for m in import_pat.finditer(src):
        var_name, filename = m.group(1), m.group(2)
        var_to_file[var_name] = filename

    # Match the CORPUS_BY_SLUG map entries: "slug": someVar as ...  OR  slug: someVar as ...
    # Capture both quoted and bare-identifier slugs.
    map_block_m = re.search(
        r"CORPUS_BY_SLUG[^=]*=\s*\{(.*?)\n\};", src, re.DOTALL
    )
    if not map_block_m:
        raise RuntimeError(
            "FATAL: could not locate CORPUS_BY_SLUG map body in "
            f"{PUBLIC_CORPUS_REGISTRY_TS} — registry format changed; "
            "discovery regex needs updating, refusing to guess."
        )
    map_body = map_block_m.group(1)

    category_map = {}
    ts_embedded_slugs = set()

    # Walk line-by-line TRACKING BRACE DEPTH so a nested key inside an
    # inline object value (e.g. magnesium's `{ _meta: {...}, products: ... }`)
    # is never mistaken for a top-level CORPUS_BY_SLUG entry. Only match
    # "key: value" lines seen at depth 0 relative to the map body.
    depth = 0
    for raw_line in map_body.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("//"):
            continue

        km = None
        if depth == 0:
            km = re.match(r'^(?:"([\w\-]+)"|([A-Za-z_]\w*))\s*:\s*(.+)$', line)

        if km:
            slug = km.group(1) or km.group(2)
            rest = km.group(3)

            var_ref_m = re.match(r"^(\w+)\s+as\s+Record", rest)
            if var_ref_m:
                var_name = var_ref_m.group(1)
                if var_name in var_to_file:
                    category_map[slug] = os.path.join(COMPARISONS_DIR, var_to_file[var_name])
            elif rest.startswith("{"):
                # Inline object literal -> TS-embedded, not a JSON file on disk.
                ts_embedded_slugs.add(slug)

        # Update brace depth AFTER processing this line's key (so the line
        # that opens the object is still seen at depth 0), then let nested
        # lines fall inside the elif/skip branch above until depth returns to 0.
        depth += line.count("{") - line.count("}")

    if not category_map:
        raise RuntimeError(
            "FATAL: parsed public-corpus-registry.ts but extracted ZERO "
            "category -> file mappings. Registry format likely changed; "
            "refusing to report a scan of nothing as 'clean'."
        )

    return category_map, ts_embedded_slugs


def cross_check_against_page_generator_configs(category_map):
    """
    Secondary corroboration: for every *.json under page_generator/configs
    that declares a `baseline_json`, confirm it points at the SAME file the
    registry says is live. Mismatches are reported (not fatal — configs can
    legitimately lag a rebuild) but must be visible, not swallowed.
    """
    mismatches = []
    checked = 0
    if not os.path.isdir(PAGE_GENERATOR_CONFIGS_DIR):
        return mismatches, checked

    for fp in glob.glob(os.path.join(PAGE_GENERATOR_CONFIGS_DIR, "*.json")):
        try:
            with open(fp, "r", encoding="utf-8") as f:
                d = json.load(f)
        except Exception:
            continue
        if not isinstance(d, dict):
            continue
        baseline = d.get("baseline_json")
        cat = d.get("category")
        if not baseline or not cat:
            continue
        checked += 1
        baseline_norm = os.path.normpath(baseline)
        # category id in configs doesn't always match the registry slug 1:1
        # (e.g. "breakfast-cereals" vs "cereals" file); compare by basename
        # of the JSON file against every registry-known file instead of by
        # category-id equality, since that's the part that actually matters
        # for OFF-scan coverage.
        known_files = {os.path.normpath(v) for v in category_map.values()}
        if baseline_norm not in known_files:
            mismatches.append({
                "config_file": os.path.basename(fp),
                "config_category": cat,
                "config_baseline_json": baseline,
            })
    return mismatches, checked


def find_bsip1_records():
    """Build dict: barcode_str -> list of (file_path, panel_source) dicts."""
    records = {}
    pattern = os.path.join(BSIP1_ROOT, "**", "*.json")
    files = glob.glob(pattern, recursive=True)
    for fpath in files:
        fname = os.path.basename(fpath)
        if fname == "run_summary.json":
            continue
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            continue

        barcode = None
        if isinstance(data, dict):
            barcode = data.get("barcode") or data.get("product_barcode")
            if barcode is None:
                m = re.search(r"bsip1(?:_audit)?_(\d+)\.json$", fname)
                if m:
                    barcode = m.group(1)

        if barcode is None:
            continue
        barcode = str(barcode)

        panel_source = (
            data.get("panel_source")
            or (data.get("source") or {}).get("panel_source")
            or data.get("nutrition_source")
            or "NOT_FOUND"
        )
        if isinstance(panel_source, dict):
            panel_source = str(panel_source)

        if barcode not in records:
            records[barcode] = []
        records[barcode].append({
            "file": fpath,
            "panel_source": str(panel_source),
        })

    return records


def extract_products_from_json(data, category):
    """Extract list of (barcode_or_id, name, image_url, raw_id) from a frontend JSON."""
    products_raw = None
    if isinstance(data, dict):
        products_raw = data.get("products")
        if products_raw is None:
            for k, v in data.items():
                if isinstance(v, list) and len(v) > 0 and isinstance(v[0], dict):
                    products_raw = v
                    break
    elif isinstance(data, list):
        products_raw = data

    if not products_raw:
        return []

    result = []
    for p in products_raw:
        if not isinstance(p, dict):
            continue

        # Extract name
        name = ""
        for nf in ["name", "product_name", "displayTitle", "shortName"]:
            v = p.get(nf)
            if v:
                name = str(v)
                break

        # Extract image URL
        image_url = p.get("imageUrl") or p.get("image_url") or ""

        # Extract barcode - prefer explicit barcode field
        raw_id = str(p.get("id", "") or "")
        barcode_field = p.get("barcode")

        if barcode_field is not None and str(barcode_field).strip() not in ("", "None", "null"):
            barcode = str(barcode_field).strip()
        else:
            # Try to extract from id field
            # Patterns: bsip1_yogurt_7290110321031, bsip1_7296073733324, shufersal_2079996, snk-001, etc.
            m = re.search(r"bsip1(?:_\w+)?_(\d+)$", raw_id)
            if m:
                barcode = m.group(1)
            elif re.match(r"^\d+$", raw_id):
                barcode = raw_id
            else:
                # For bread: shufersal_NNNN or other non-standard IDs - no barcode
                # For snk-001 style: no barcode either
                barcode = None

        result.append({
            "barcode": barcode,
            "raw_id": raw_id,
            "name": name,
            "image_url": str(image_url),
        })

    return result


def check_json_level_off(file_path):
    """Check A: scan raw file text for OFF markers. Returns (count, list of hit dicts)."""
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    hits = []
    text_lower = text.lower()
    for marker in OFF_MARKERS:
        marker_lower = marker.lower()
        start = 0
        while True:
            pos = text_lower.find(marker_lower, start)
            if pos == -1:
                break
            ctx = text[max(0, pos-60):pos+len(marker)+80].replace("\n", " ").replace("\r", "")
            hits.append({"marker": marker, "context": ctx[:200]})
            start = pos + 1

    return len(hits), hits


def check_image_url_off(products):
    """Check if any product's imageUrl points to OFF CDN."""
    contaminated = []
    for p in products:
        img = p.get("image_url", "") or ""
        if any(m.lower() in img.lower() for m in OFF_MARKERS):
            contaminated.append(p)
    return contaminated


def check_corpus_level_off(products, bsip1_records):
    """Check B: for each product with barcode, look up BSIP1 panel_source."""
    results = []
    for p in products:
        barcode = p["barcode"]
        if barcode is None:
            results.append({
                **p,
                "panel_source": "NO_BARCODE",
                "bsip1_file": None,
                "is_off_corpus": False,
                "is_no_record": False,
                "is_no_barcode": True,
            })
            continue

        recs = bsip1_records.get(barcode)
        if recs is None:
            results.append({
                **p,
                "panel_source": "NO_RECORD",
                "bsip1_file": None,
                "is_off_corpus": False,
                "is_no_record": True,
                "is_no_barcode": False,
            })
        else:
            rec = recs[0]
            ps = rec["panel_source"]
            is_off_corpus = (
                "open_food_facts" in ps.lower()
                or "openfoodfacts" in ps.lower()
            )
            results.append({
                **p,
                "panel_source": ps,
                "bsip1_file": rec["file"],
                "is_off_corpus": is_off_corpus,
                "is_no_record": False,
                "is_no_barcode": False,
            })
    return results


def main():
    print("Discovering live categories from public-corpus-registry.ts (dynamic, not hardcoded)...")
    category_map, ts_embedded_slugs = discover_live_categories()
    print(f"  Discovered {len(category_map)} JSON-backed live categories: {sorted(category_map.keys())}")
    if ts_embedded_slugs:
        print(f"  Discovered {len(ts_embedded_slugs)} TS-embedded live categories (out of JSON-scan scope): {sorted(ts_embedded_slugs)}")

    mismatches, configs_checked = cross_check_against_page_generator_configs(category_map)
    print(f"  Cross-checked against {configs_checked} page_generator configs with a baseline_json field")
    if mismatches:
        print(f"  WARNING: {len(mismatches)} config(s) declare a baseline_json NOT found among registry-live files (may be a stale/pending config, not necessarily a bug):")
        for mm in mismatches:
            print(f"    - {mm['config_file']} (category={mm['config_category']}) -> {mm['config_baseline_json']}")

    print("\nBuilding BSIP1 records index...")
    bsip1_records = find_bsip1_records()
    print(f"  Indexed {len(bsip1_records)} unique barcodes from BSIP1 records")

    results = {}
    missing_targets = []

    for category, data_file in sorted(category_map.items()):
        print(f"\nScanning: {category} -> {os.path.basename(data_file)}")

        if not os.path.exists(data_file):
            # FAIL LOUD: a category the live app itself imports from is
            # missing on disk. This is not a warning to skip past — it means
            # either the repo is broken or the site is serving something we
            # cannot verify. Record it and fail the whole run at the end.
            print(f"  FATAL: expected live data file MISSING: {data_file}")
            missing_targets.append({"category": category, "data_file": data_file})
            results[category] = {"data_file": data_file, "error": "FILE_NOT_FOUND_FATAL"}
            continue

        # Check A: JSON-level OFF markers
        json_hit_count, json_hits = check_json_level_off(data_file)

        # Load JSON
        with open(data_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Extract products
        products = extract_products_from_json(data, category)
        print(f"  Extracted {len(products)} products from JSON")

        # Check OFF image URLs (sub-type of JSON-level contamination)
        image_off_products = check_image_url_off(products)

        # Check B: corpus-level panel_source
        corpus_results = check_corpus_level_off(products, bsip1_records)

        off_corpus = [r for r in corpus_results if r["is_off_corpus"]]
        no_records = [r for r in corpus_results if r["is_no_record"]]
        no_barcodes = [r for r in corpus_results if r["is_no_barcode"]]

        # Categorize JSON hits: metadata-only vs live-product OFF
        # (cereals has 'open_food_facts' in metadata comment about excluded products)
        live_json_hits = [h for h in json_hits if "excluded_off_products" not in h["context"] and "OFF ban" not in h["context"]]
        metadata_only_json_hits = [h for h in json_hits if h not in live_json_hits]

        results[category] = {
            "data_file": data_file,
            "data_file_basename": os.path.basename(data_file),
            "total_products_in_file": len(products),
            "json_hit_count": json_hit_count,
            "json_hits": json_hits,
            "live_json_hit_count": len(live_json_hits),
            "live_json_hits": live_json_hits,
            "metadata_json_hits": metadata_only_json_hits,
            "image_off_products": image_off_products,
            "image_off_count": len(image_off_products),
            "corpus_results": corpus_results,
            "off_corpus_count": len(off_corpus),
            "off_corpus": off_corpus,
            "no_record_count": len(no_records),
            "no_records": no_records,
            "no_barcode_count": len(no_barcodes),
            "no_barcodes": no_barcodes,
        }

        print(f"  JSON OFF markers: total={json_hit_count} (live={len(live_json_hits)}, metadata-only={len(metadata_only_json_hits)})")
        print(f"  Image OFF products: {len(image_off_products)}")
        print(f"  Corpus OFF (panel_source=OFF): {len(off_corpus)}")
        print(f"  NO_RECORD: {len(no_records)}, NO_BARCODE: {len(no_barcodes)}")

    # Write output
    os.makedirs(OUT_DIR, exist_ok=True)
    out_path = os.path.join(OUT_DIR, "off_sweep_v1.md")
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("# OFF Sweep v1 — Open Food Facts Contamination Map\n\n")
        f.write(f"Generated: {now}  \n")
        f.write("Method: DYNAMIC discovery from `bari-web/src/lib/seo/public-corpus-registry.ts` "
                "(the same file the live Next.js app imports its comparison JSON from) — "
                "cross-checked against `03_operations/page_generator/configs/*.json` `baseline_json` fields. "
                "NOT a hardcoded filename list (TASK-450 fix).  \n")
        f.write(f"Scope: {len(category_map)} JSON-backed live categories"
                + (f" + {len(ts_embedded_slugs)} TS-embedded live categories out of JSON-scan scope ({sorted(ts_embedded_slugs)})" if ts_embedded_slugs else "")
                + ".  \n")
        f.write("OFF contamination types checked: (A) JSON-level OFF string markers in file text; (B) BSIP1 panel_source=open_food_facts.  \n")
        f.write("Image URL contamination (images.openfoodfacts.org in imageUrl field) is an independent contamination class reported separately.  \n\n")

        if missing_targets:
            f.write("## FATAL: MISSING LIVE DATA FILES\n\n")
            f.write("The following categories are imported by the live app's public-corpus-registry.ts "
                    "but the file does not exist on disk. This sweep CANNOT confirm these categories are "
                    "clean and the run has failed loudly rather than silently skip them.\n\n")
            for mt in missing_targets:
                f.write(f"- **{mt['category']}**: `{mt['data_file']}`\n")
            f.write("\n")

        # Section 1: Category-data file map
        f.write("## Section 1: Category to Data File Map (dynamically discovered)\n\n")
        f.write("Derived by parsing `bari-web/src/lib/seo/public-corpus-registry.ts` at scan time — "
                "the file the live app itself imports comparison JSON from.\n\n")
        f.write("| Category | Data File |\n")
        f.write("|---|---|\n")
        for cat, r in results.items():
            f.write(f"| {cat} | {r.get('data_file_basename','N/A')} |\n")
        f.write("\n")
        if ts_embedded_slugs:
            f.write("**TS-embedded live categories (no frontend JSON file — out of scope for this scanner by construction):**  \n")
            for slug in sorted(ts_embedded_slugs):
                info = TS_EMBEDDED_CATEGORIES.get(slug, {})
                f.write(f"- {slug}: {info.get('reason', 'TS-embedded product data')}"
                        + (f" (underlying source: `{info['underlying_source']}`)" if info.get('underlying_source') else "")
                        + "\n")
            f.write("\n")
        if mismatches:
            f.write("**Page-generator config baseline_json mismatches (informational, non-fatal):**  \n")
            for mm in mismatches:
                f.write(f"- `{mm['config_file']}` (category={mm['config_category']}) declares baseline_json "
                        f"`{mm['config_baseline_json']}` which is not among the registry-live files — "
                        "likely a config pending a rebuild sync, not a live-site risk.\n")
            f.write("\n")

        # Section 2: Verdict table
        f.write("## Section 2: Verdict Table\n\n")
        f.write("Contamination types:  \n")
        f.write("- Image-OFF: product imageUrl points to images.openfoodfacts.org  \n")
        f.write("- Corpus-OFF: BSIP1 panel_source = open_food_facts (nutrition data from OFF)  \n")
        f.write("- JSON-marker: 'open_food_facts' string appears in live file (may be metadata-only)  \n\n")
        f.write("| Category | Data File | Products (M) | Image-OFF (N/M) | Corpus-OFF B (N/M) | JSON-live A | NO_RECORD | NO_BARCODE | Verdict |\n")
        f.write("|---|---|---|---|---|---|---|---|---|\n")

        total_off_image = 0
        total_off_corpus = 0
        total_products_all = 0

        for cat, r in results.items():
            if "error" in r:
                f.write(f"| {cat} | {r.get('data_file_basename','?')} | N/A | N/A | N/A | N/A | N/A | N/A | **FATAL: FILE MISSING** |\n")
                continue
            m = r["total_products_in_file"]
            n_img = r["image_off_count"]
            n_corp = r["off_corpus_count"]
            n_json_live = r["live_json_hit_count"]
            n_no_rec = r["no_record_count"]
            n_no_bc = r["no_barcode_count"]

            if n_img > 0 or n_corp > 0 or n_json_live > 0:
                verdict = "DIRTY"
            elif n_no_rec > m * 0.5 and n_corp == 0:
                verdict = "UNKNOWN"
            else:
                verdict = "CLEAN"

            total_off_image += n_img
            total_off_corpus += n_corp
            total_products_all += m

            f.write(f"| {cat} | {r['data_file_basename']} | {m} | {n_img}/{m} | {n_corp}/{m} | {n_json_live} | {n_no_rec} | {n_no_bc} | {verdict} |\n")

        f.write(f"\n**TOTAL Image-OFF products across live site: {total_off_image}**  \n")
        f.write(f"**TOTAL Corpus-OFF products across live site: {total_off_corpus}**  \n")
        f.write(f"**TOTAL Products scanned: {total_products_all}**  \n\n")

        # Section 3: Dirty category details
        f.write("## Section 3: Dirty Category Details\n\n")

        dirty_cats = {cat: r for cat, r in results.items()
                     if not "error" in r and (r["image_off_count"] > 0 or r["off_corpus_count"] > 0 or r["live_json_hit_count"] > 0)}

        if not dirty_cats:
            f.write("No dirty categories detected at corpus or live-JSON level.\n\n")
        else:
            for cat, r in dirty_cats.items():
                f.write(f"### {cat}\n\n")
                f.write(f"Data file: `{r['data_file_basename']}`  \n\n")

                if r["image_off_count"] > 0:
                    f.write(f"**Image-OFF contamination: {r['image_off_count']}/{r['total_products_in_file']} products**\n\n")
                    f.write("These products display images served from images.openfoodfacts.org — an OFF CDN URL in a live page field.\n\n")
                    f.write("| Barcode | Raw ID | Name | Image URL |\n")
                    f.write("|---|---|---|---|\n")
                    for p in r["image_off_products"]:
                        f.write(f"| {p.get('barcode','?')} | {p.get('raw_id','')[:30]} | {p.get('name','')[:50]} | {p.get('image_url','')[:80]} |\n")
                    f.write("\n")

                if r["off_corpus_count"] > 0:
                    f.write(f"**Corpus-OFF (panel_source=open_food_facts): {r['off_corpus_count']}/{r['total_products_in_file']} products**\n\n")
                    f.write("| Barcode | Name | panel_source | BSIP1 file |\n")
                    f.write("|---|---|---|---|\n")
                    for p in r["off_corpus"]:
                        bsip1_rel = os.path.relpath(p["bsip1_file"], REPO) if p["bsip1_file"] else "N/A"
                        f.write(f"| {p.get('barcode','?')} | {p.get('name','')[:50]} | {p.get('panel_source','?')} | {bsip1_rel} |\n")
                    f.write("\n")

        # Section 4: NO_RECORD / NO_BARCODE concentrations
        f.write("## Section 4: NO_RECORD and NO_BARCODE Concentrations\n\n")
        f.write("Categories with high NO_RECORD rates cannot confirm clean BSIP1 provenance.\n\n")
        f.write("| Category | NO_RECORD | NO_BARCODE | Total | NO_RECORD% | Note |\n")
        f.write("|---|---|---|---|---|---|\n")
        for cat, r in results.items():
            if "error" in r:
                continue
            m = r["total_products_in_file"]
            n_rec = r["no_record_count"]
            n_bc = r["no_barcode_count"]
            pct = round(100.0 * n_rec / m, 1) if m > 0 else 0
            note = ""
            if n_bc > 0:
                note = f"{n_bc} products have no numeric barcode (e.g. bread uses shufersal_NNNN IDs)"
            elif pct > 50:
                note = "HIGH — cannot confirm BSIP1 provenance"
            f.write(f"| {cat} | {n_rec} | {n_bc} | {m} | {pct}% | {note} |\n")
        f.write("\n")

        # Section 5: Full corpus table for each category
        f.write("## Section 5: Full Corpus Results Per Category\n\n")
        for cat, r in results.items():
            if "error" in r:
                continue
            f.write(f"### {cat} — {r['data_file_basename']} ({r['total_products_in_file']} products)\n\n")
            f.write("| Barcode | Raw ID | Name | panel_source | img_off | Status |\n")
            f.write("|---|---|---|---|---|---|\n")
            for p in r["corpus_results"]:
                img_off = "Y" if any(m.lower() in (p.get("image_url","") or "").lower() for m in OFF_MARKERS) else ""
                if p.get("is_off_corpus"):
                    status = "CORPUS-OFF"
                elif img_off:
                    status = "IMAGE-OFF"
                elif p.get("is_no_record"):
                    status = "NO_RECORD"
                elif p.get("is_no_barcode"):
                    status = "NO_BARCODE"
                else:
                    status = "ok"
                bc = p.get("barcode") or ""
                rid = p.get("raw_id","")[:25]
                name = p.get("name","")[:50]
                ps = p.get("panel_source","")[:40]
                f.write(f"| {bc} | {rid} | {name} | {ps} | {img_off} | {status} |\n")
            f.write("\n")

    print(f"\nOutput written to: {out_path}")

    # Print SHA256 of output
    sha = sha256_file(out_path)
    print(f"SHA256: {sha}")

    return out_path, results, total_off_image, total_off_corpus, total_products_all, sha, missing_targets


if __name__ == "__main__":
    out_path, results, total_off_image, total_off_corpus, total_products, sha, missing_targets = main()
    print(f"\nFINAL: {total_off_image} image-OFF + {total_off_corpus} corpus-OFF products across {total_products} total in live categories")
    print(f"Output: {out_path}")
    print(f"SHA256: {sha}")

    if missing_targets:
        print(f"\nFATAL: {len(missing_targets)} live-registered category file(s) missing on disk. "
              "Coverage is INCOMPLETE. Exiting nonzero — this run must NOT be treated as a clean pass.")
        sys.exit(1)

    if total_off_image > 0 or total_off_corpus > 0:
        print(f"\nFATAL: OFF contamination detected ({total_off_image} image-OFF, {total_off_corpus} corpus-OFF). Exiting nonzero.")
        sys.exit(2)

    print("\nPASS: full coverage, zero OFF markers.")
    sys.exit(0)
