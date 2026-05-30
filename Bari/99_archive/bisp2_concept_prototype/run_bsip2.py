import sys, json
import pandas as pd
from dataclasses import asdict
from bsip2_score import score_product


def flatten_result(result_dict):
    flat = {
        "barcode": result_dict["barcode"],
        "product_name": result_dict["product_name"],
        "base_score": result_dict["base_score"],
        "final_score": result_dict["final_score"],
        "grade": result_dict["grade"],
        "confidence": result_dict["confidence"],
        "algorithm_version": result_dict["algorithm_version"],
        "input_hash": result_dict["input_hash"],
        "computed_at": result_dict["computed_at"],
        "reasons_positive": " | ".join(result_dict["reasons_positive"]),
        "reasons_negative": " | ".join(result_dict["reasons_negative"]),
        "guardrails_json": json.dumps(result_dict["guardrails"], ensure_ascii=False),
    }
    for k, v in result_dict["dimensions"].items():
        flat[f"dim_{k}"] = v
    return flat


def main():
    if len(sys.argv) < 3:
        print("Usage: python run_bsip2.py input.xlsx output.xlsx")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    if input_path.lower().endswith(".csv"):
        df = pd.read_csv(input_path)
    else:
        df = pd.read_excel(input_path)

    results = []
    for _, row in df.iterrows():
        assessment = score_product(row.to_dict())
        results.append(flatten_result(asdict(assessment)))

    pd.DataFrame(results).to_excel(output_path, index=False)
    print(f"Saved BSIP2 results to {output_path}")


if __name__ == "__main__":
    main()
