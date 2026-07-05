# -*- coding: utf-8 -*-
"""Compute sha256 for every artifact produced by this Stage-1 run and write a
manifest — used only for the return-contract artifact list, not consumed by
any downstream pipeline stage."""
import hashlib
import json
import pathlib

OUTPUT_DIR = pathlib.Path(r"C:\Bari\02_products\yogurt_system\bsip1_task515")


def sha256_of(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def main():
    product_files = sorted(OUTPUT_DIR.glob("bsip1_yogurt_*.json"))
    manifest = {
        "run_report": {
            "path": str(OUTPUT_DIR / "bsip1_run_report_task515.json"),
            "sha256": sha256_of(OUTPUT_DIR / "bsip1_run_report_task515.json"),
        },
        "excluded_products": {
            "path": str(OUTPUT_DIR / "excluded_products_task515.json"),
            "sha256": sha256_of(OUTPUT_DIR / "excluded_products_task515.json"),
        },
        "build_script": {
            "path": str(OUTPUT_DIR / "build_bsip1_yogurt_task515.py"),
            "sha256": sha256_of(OUTPUT_DIR / "build_bsip1_yogurt_task515.py"),
        },
        "product_count": len(product_files),
        "product_files_sha256": {
            f.name: sha256_of(f) for f in product_files
        },
    }
    out_path = OUTPUT_DIR / "_artifact_manifest_sha256_task515.json"
    out_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print("product_count:", len(product_files))
    print("run_report sha256:", manifest["run_report"]["sha256"])
    print("excluded_products sha256:", manifest["excluded_products"]["sha256"])
    print("build_script sha256:", manifest["build_script"]["sha256"])
    print("manifest written:", out_path)


if __name__ == "__main__":
    main()
