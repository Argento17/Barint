# ---------------------------------------------------------------------------
# Discovery helpers
# ---------------------------------------------------------------------------

def _resolve_repo_path(path_str: str) -> Path:
    p = Path(path_str)
    if p.is_absolute():
        return p
    return REPO_ROOT / p


def load_in_scored_barcodes(corpus_path: Path) -> set[str]:
    corpus = json.loads(corpus_path.read_text(encoding="utf-8"))
    return {
        str(p["barcode"])
        for p in corpus.get("products", [])
        if p.get("decision") == "IN_SCORED"
    }


def load_bsip0_index(bsip0_path: Path) -> dict[str, dict]:
    raw = json.loads(bsip0_path.read_text(encoding="utf-8"))
    if isinstance(raw, list):
        records = raw
    elif isinstance(raw, dict) and "products" in raw:
        records = raw["products"]
    else:
        records = [raw]
    return {str(r.get("barcode", "")): r for r in records if r.get("barcode")}


def discover_raw_store_pairs(raw_store_dir: Path) -> dict[str, Path]:
    """Map barcode -> latest banked HTML under per-page_id subfolders."""
    pairs: dict[str, Path] = {}
    for page_dir in sorted(raw_store_dir.glob("P_*")):
        if not page_dir.is_dir():
            continue
        barcode = page_dir.name[2:] if page_dir.name.startswith("P_") else page_dir.name
        html_files = sorted(page_dir.glob("*.html"))
        if html_files:
            pairs[barcode] = html_files[-1]
    return pairs


def discover_e2e_products() -> list[dict]:
    html_files = sorted(FIXTURES_DIR.glob("raw_e2e_*.html"))
    if not html_files:
        raise FileNotFoundError("no HTML fixtures found")

    products_input = []
    for html_path in html_files:
        idx = re.search(r"raw_e2e_(\d+)\.html", html_path.name)
        if not idx:
            continue
        fixture_num = idx.group(1)

        bsip0_candidates = sorted(BSIP0_DIR.glob("bsip0_*.json"))
        matched_bsip0 = None
        for bc in bsip0_candidates:
            with open(bc, encoding="utf-8") as f:
                d = json.load(f)
            src = d.get("source_url", "")
            if f"raw_e2e_{fixture_num}" in src:
                matched_bsip0 = (bc, d)
                break

        if matched_bsip0 is None:
            print(f"  [A] WARNING: no BSIP0 match for {html_path.name}", file=sys.stderr)
            continue

        bsip0_path, bsip0_data = matched_bsip0
        barcode = bsip0_data.get("barcode", f"unknown_{fixture_num}")
        name = bsip0_data.get("name_he", f"product_{fixture_num}")

        products_input.append({
            "barcode": barcode,
            "name": name,
            "html_path": html_path,
            "bsip0_source": bsip0_path,
        })
    return products_input
