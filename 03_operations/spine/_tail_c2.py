
def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Dual-extractor consensus (rule-based BSIP0 vs Gemini on banked HTML)."
    )
    parser.add_argument("--raw-store", help="raw_store category dir with per-code subfolders and manifest.jsonl")
    parser.add_argument("--bsip0", help="BSIP0 raw JSON (array of products) for extractor A")
    parser.add_argument("--corpus", help="Optional corpus_filter.json; restrict to IN_SCORED barcodes")
    parser.add_argument("--out", help="Output directory for consensus report (default: _e2e_out or alongside run)")
    parser.add_argument("--limit", type=int, default=None, help="Optional cap on products processed (rate-limit safety)")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None):
    args = parse_args(argv)
    use_raw_store = bool(args.raw_store)

    if use_raw_store:
        if not args.bsip0:
            print("ERROR: --raw-store requires --bsip0", file=sys.stderr)
            sys.exit(2)
        raw_store_dir = _resolve_repo_path(args.raw_store)
        bsip0_path = _resolve_repo_path(args.bsip0)
        corpus_path = _resolve_repo_path(args.corpus) if args.corpus else None
        out_dir = _resolve_repo_path(args.out) if args.out else raw_store_dir.parent / "dual_extract"
        print("=== dual_extract.py — raw_store mode (P69) ===")
        print(f"Raw store: {raw_store_dir}")
        print(f"BSIP0    : {bsip0_path}")
        print(f"Corpus   : {corpus_path or '(all banked HTML with BSIP0 match)'}")
        print(f"Output   : {out_dir}")
        print(f"Gemini   : {GEMINI_BIN}")
        if args.limit:
            print(f"Limit    : {args.limit}")
        print()

        products_input, run_meta = discover_raw_store_products(
            raw_store_dir, bsip0_path, corpus_path, args.limit
        )
        if not products_input:
            print("ERROR: no products to process after discovery/filter.", file=sys.stderr)
            sys.exit(1)
        print(f"Found {len(products_input)} product(s) to process.\n")
    else:
        out_dir = _resolve_repo_path(args.out) if args.out else OUT_DIR
        run_meta = {"mode": "e2e_fixtures"}
        print("=== dual_extract.py — e2e fixture mode (TASK-265 / P48) ===")
        print(f"Fixtures : {FIXTURES_DIR}")
        print(f"BSIP0 dir: {BSIP0_DIR}")
        print(f"Output   : {out_dir}")
        print(f"Gemini   : {GEMINI_BIN}")
        print()
        try:
            products_input = discover_e2e_products()
        except FileNotFoundError as e:
            print(f"ERROR: {e}", file=sys.stderr)
            sys.exit(1)
        if args.limit is not None:
            products_input = products_input[: args.limit]
        print(f"Found {len(products_input)} fixture(s) to process.\n")

    products_data, stopped_early = process_products(products_input)
    if stopped_early:
        run_meta["stopped_early_unavailable_threshold"] = True

    report = run_consensus(products_data, meta=run_meta)
    emit_report(report, out_dir)
    print_summary(report)

    print()
    print("dual_extract.py complete. Exit 0.")
    sys.exit(0)


if __name__ == "__main__":
    main()
