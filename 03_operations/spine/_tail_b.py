
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
