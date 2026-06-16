
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
        for row in nutrition_disagreements:
            print(
                f"  {row['barcode']} {row['field']}: "
                f"A={row['extractor_a']} vs B={row['extractor_b']}"
            )

    print()
    print("=== PER-PRODUCT FIELD TABLE ===")
    for prod in report["products"]:
        print(f"\n{prod['name']} ({prod['barcode']})")
        print(f"  {'Field':<22} {'A':>10}  {'B':>10}  Verdict")
        print(f"  {'-'*22} {'-'*10}  {'-'*10}  -------")
        for fr in prod["fields"]:
            a_s = str(fr["extractor_a"]) if fr["extractor_a"] is not None else "null"
            b_s = str(fr["extractor_b"]) if fr["extractor_b"] not in (None, "UNAVAILABLE") else str(fr["extractor_b"])
            marker = " <-- REVIEW" if fr["verdict"] in ("DISAGREE", "FLAG") else ""
            print(f"  {fr['field']:<22} {a_s:>10}  {b_s:>10}  {fr['verdict']}{marker}")

    if s["fields_disagree"] > 0 or s["fields_flag"] > 0:
        print()
        print(f"NOTE: {s['fields_disagree']} DISAGREE + {s['fields_flag']} FLAG field(s) found.")
        print("These would block auto-publish in the factory. See report for details.")
