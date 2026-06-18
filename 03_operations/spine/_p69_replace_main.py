from pathlib import Path

path = Path(r"C:/Bari/03_operations/spine/dual_extract.py")
text = path.read_text(encoding="utf-8")
marker = "# ---------------------------------------------------------------------------\n# Main\n# ---------------------------------------------------------------------------\n"
idx = text.find(marker)
if idx == -1:
    raise SystemExit("marker not found")

new_tail = r'''# ---------------------------------------------------------------------------
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


def discover_raw_store_products(
    raw_store_dir: Path,
    bsip0_path: Path,
    corpus_path: Path | None,
    limit: int | None,
) -> tuple[list[dict], dict]:
    html_by_barcode = discover_raw_store_pairs(raw_store_dir)
    bsip0_index = load_bsip0_index(bsip0_path)

    allowed: set[str] | None = None
    if corpus_path is not None:
        allowed = load_in_scored_barcodes(corpus_path)

    products_input = []
    for barcode in sorted(html_by_barcode):
        if allowed is not None and barcode not in allowed:
            continue
        bsip0_record = bsip0_index.get(barcode)
        if bsip0_record is None:
            print(f"  [A] WARNING: no BSIP0 record for barcode {barcode}", file=sys.stderr)
            continue
        products_input.append({
            "barcode": barcode,
            "name": bsip0_record.get("name_he", barcode),
            "html_path": html_by_barcode[barcode],
            "bsip0_source": bsip0_record,
        })
        if limit is not None and len(products_input) >= limit:
            break

    meta = {
        "mode": "raw_store",
        "raw_store_dir": str(raw_store_dir),
        "bsip0_path": str(bsip0_path),
        "corpus_path": str(corpus_path) if corpus_path else None,
        "in_scored_filter": allowed is not None,
        "limit": limit,
        "html_discovered": len(html_by_barcode),
        "products_selected": len(products_input),
    }
    return products_input, meta


def process_products(
    products_input: list[dict],
    *,
    stop_unavailable_pct: float = 0.30,
) -> tuple[list[dict], bool]:
    products_data = []
    stopped_early = False

    for i, p in enumerate(products_input, start=1):
        print(f"Processing [{i}/{len(products_input)}]: {p['name']} ({p['barcode']})")

        print(f"  [A] Reading BSIP0 for {p['barcode']}")
        a_result = extract_a(p["barcode"], p["bsip0_source"])
        print(f"  [A] OK — energy={a_result.get('energy_kcal')}, protein={a_result.get('protein_g')}")

        print(f"  [B] Calling Gemini on {p['html_path'].name} ...")
        b_result = extract_b(p["barcode"], p["html_path"])
        if b_result is None:
            print("  [B] UNAVAILABLE — marking for manual review")
        else:
            print(f"  [B] OK — energy={b_result.get('energy_kcal')}, protein={b_result.get('protein_g')}")

        products_data.append({
            "barcode": p["barcode"],
            "name": p["name"],
            "extractor_a": a_result,
            "extractor_b": b_result,
        })
        print()

        processed = len(products_data)
        unavailable = sum(1 for row in products_data if row["extractor_b"] is None)
        if processed >= 3 and (unavailable / processed) > stop_unavailable_pct:
            print(
                f"STOPPING EARLY: {unavailable}/{processed} products B-unavailable "
                f"({unavailable / processed * 100:.1f}% > {stop_unavailable_pct * 100:.0f}% threshold).",
                file=sys.stderr,
            )
            stopped_early = True
            break

    return products_data, stopped_early


def emit_report(report: dict, out_dir: Path) -> tuple[Path, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / "dual_extract_report.json"
    md_path = out_dir / "dual_extract_report.md"

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"Written: {json_path}")

    md_content = render_md(report)
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"Written: {md_path}")
    return json_path, md_path


def print_summary(report: dict) -> None:
    s = report["summary"]
    print()
    print("=== CONSENSUS SUMMARY ===")
    print(f"  Products cross-checked : {s['products_cross_checked']}")
    print(f"  Gemini calls OK        : {s['gemini_calls_ok']}")
    print(f"  Gemini unavailable     : {s.get('gemini_calls_unavailable', 0)}")
    print(f"  Fields compared        : {s['fields_with_both_extractors']}")
    print(f"  AGREE                  : {s['fields_agree']}")
    print(f"  DISAGREE               : {s['fields_disagree']}")
    print(f"  FLAG                   : {s['fields_flag']}")
    print(f"  Agreement rate         : {s['agreement_rate_pct']}%")

    if s.get("per_field_verdicts"):
        print()
        print("=== PER-FIELD VERDICTS (key nutrition) ===")
        for field in ["energy_kcal", "protein_g", "fat_g", "sodium_mg", "sugars_g"]:
            fv = s["per_field_verdicts"].get(field, {})
            print(
                f"  {field:<18} AGREE={fv.get('AGREE', 0)} "
                f"DISAGREE={fv.get('DISAGREE', 0)} FLAG={fv.get('FLAG', 0)} "
                f"B_UNAVAIL={fv.get('B_UNAVAILABLE', 0)}"
            )

    nutrition_disagreements = s.get("nutrition_disagreements") or []
    if nutrition_disagreements:
        print()
        print("=== NUTRITION DISAGREEMENTS ===")
        for 
