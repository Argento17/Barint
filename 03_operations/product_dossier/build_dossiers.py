#!/usr/bin/env python3
"""
build_dossiers.py — Product Dossier compiler v1 (PD-2 / TASK-610).

Per STF memo `01_framework/governance/stf_memos/2026-07-11_product-dossier-
architecture.md`: one shelf-agnostic compiler that regenerates, per product,
a deterministic dossier {generation, layer_1, layer_2, layer_3, layer_4} by
DERIVING wholesale from existing stores (page_generator shelf configs ->
served frontend JSON + BSIP2 trace dirs; TASK-601 capture manifest + replay
harness for raw evidence). It never recomputes or mutates a published
score (tripwire-1) and writes ONLY under 03_operations/product_dossier/.

Scope of THIS build (per TASK-610 delegation spec): registry-INDEPENDENT.
The bari_pid / alias join (TASK-609, PD-1) is a documented stub --
see lib/registry_interface.py. Layer-1 identity FACTS (name/brand/etc, R-B
projections), Layer-2 raw evidence (the ~90%-built core, reusing
replay_harness.py), Layer-3's three disjoint namespaces (assessment /
data_quality / publication_record, R-C), and Layer-4's source_traceability +
calculation checks are REAL. Layer-4's barcode check is a documented stub.

Usage:
  python build_dossiers.py                      # build sample dossiers for all discovered shelves
  python build_dossiers.py --shelves cereals,milk --limit 5
  python build_dossiers.py --check              # compare in-memory build vs committed baseline (if any)
  python build_dossiers.py --selftest           # run the 4 required structural proofs

Exit codes: 0 = success / selftest passed / no baseline drift. 1 = selftest
failure or --check drift found. 2 = a DossierBuildError aborted the compile
(banned-source cell, cross-namespace metric, or banned overall_score field).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib import layer1_identity, layer2_evidence, layer3_schema, layer4_checks  # noqa: E402
from lib.layer2_evidence import DossierBuildError  # noqa: E402
from lib.layer3_schema import Layer3, Metric, NamespaceViolation  # noqa: E402

COMPILER_VERSION = "pd2_build_dossiers_v1_task610"

PRODUCT_DOSSIER_ROOT = REPO_ROOT / "03_operations" / "product_dossier"
CONFIGS_DIR = REPO_ROOT / "03_operations" / "page_generator" / "configs"
DEFAULT_OUT_DIR = PRODUCT_DOSSIER_ROOT / "dossiers_sample"
MANIFEST_SUMMARY_PATH = PRODUCT_DOSSIER_ROOT / "generation_manifest.json"
# NOTE: dossier_baseline.jsonl is the future COMMITTED baseline (memo §4). It is
# intentionally NOT written by this task -- R-D: "Only the fixed parser may
# produce a COMMITTED baseline; any pre-fix projection is uncommitted... never
# a comparison base." --check reads it if present; --write-baseline exists as
# a dormant adapter for whoever runs it after the parser fix + replay
# re-baseline lands.
BASELINE_PATH = PRODUCT_DOSSIER_ROOT / "dossier_baseline.jsonl"

RUN_GATES_PATH = REPO_ROOT / "03_operations" / "page_generator" / "gates" / "run_gates.py"


def assert_write_boundary(path: Path) -> None:
    """Tripwire-guard: this compiler must never write outside its own tree."""
    resolved = path.resolve()
    if PRODUCT_DOSSIER_ROOT.resolve() not in resolved.parents and resolved != PRODUCT_DOSSIER_ROOT.resolve():
        raise DossierBuildError(f"write outside product_dossier boundary: {resolved}")


def rebase_path(path_str: str, root: Path = REPO_ROOT) -> Path:
    """Shelf configs under 03_operations/page_generator/configs/*.json carry
    ABSOLUTE paths baked in at authoring time (e.g. "C:\\Bari\\02_products\\..."
    or "C:\\Bari\\bari-web\\..."). This compiler runs inside an isolated git
    worktree (a separate physical checkout on disk) -- using those absolute
    paths verbatim would silently read from a DIFFERENT repo checkout than
    the one this code lives in. Rebase onto THIS repo's own root instead by
    finding the last path segment literally named "Bari" (every checkout of
    this repo is named that, worktree or not) and rejoining the remainder.
    """
    parts = Path(path_str).parts
    idx = None
    for i, part in enumerate(parts):
        if part.lower() == "bari":
            idx = i
    if idx is None:
        return Path(path_str)
    return root.joinpath(*parts[idx + 1:])


def normalize_dirs(value) -> List[str]:
    """A shelf config's run_products_dir/corpus_dirs may be EITHER a single
    path string OR a list of path strings (cookies_coffee, crackers, and
    granola configs use a list -- multiple BSIP2 run dirs merged, first
    dir wins on barcode collision, same semantics validate_comparison_page.py
    already documents for its own --traces nargs="+"). Always normalize to
    a list here so downstream code never branches on type.
    """
    if not value:
        return []
    if isinstance(value, str):
        return [value]
    return list(value)


def category_folder_from_config(cfg: dict) -> Optional[str]:
    candidates = normalize_dirs(cfg.get("run_products_dir")) + normalize_dirs(cfg.get("corpus_dirs"))
    for c in candidates:
        m = re.search(r"02_products[\\/]+([^\\/]+)[\\/]", c or "")
        if m:
            return m.group(1)
    return None


def discover_shelf_configs(only: Optional[List[str]] = None) -> List[Tuple[str, dict, Path]]:
    """Returns [(shelf_id, config_dict, config_path), ...], deduped by
    rebased baseline_json path (some configs, e.g. snacks_task413_staging.json,
    intentionally point at the same served page as another config; the
    first one found -- alphabetical -- wins, the rest are skipped).
    """
    seen_baseline = set()
    out = []
    for path in sorted(CONFIGS_DIR.glob("*.json")):
        if path.name.startswith("_generated_"):
            continue
        shelf_id = path.stem
        if only and shelf_id not in only:
            continue
        try:
            cfg = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if "baseline_json" not in cfg or "run_products_dir" not in cfg:
            continue
        # Defensive guard (unrelated to the registry join -- discovered while
        # running a full-corpus build to verify TASK-610's join): two shelf
        # configs (yogurt_drinkable.json, yogurt_spoonable.json) carry
        # baseline_json: null. rebase_path()/Path() cannot accept None; skip
        # rather than crash discovery for every OTHER shelf. Not a silent
        # data fix -- these two shelves are simply not eligible for a
        # dossier build until their config is corrected (outside PD-2 scope).
        if cfg.get("baseline_json") is None:
            continue
        baseline_key = str(rebase_path(cfg["baseline_json"]))
        if baseline_key in seen_baseline:
            continue
        seen_baseline.add(baseline_key)
        out.append((shelf_id, cfg, path))
    return out


def load_run_gates():
    import importlib.util
    spec = importlib.util.spec_from_file_location("pd2_run_gates_main_ref", RUN_GATES_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _sha256_of_obj(obj) -> str:
    canon = json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(canon.encode("utf-8")).hexdigest()


# identity_confidence: derived purely from Layer 1's registry-adjudicated
# barcode_state (never from an assessment/publication_record value -- axis
# rules forbid it, and it wouldn't make sense anyway: this is a RECORD
# confidence, not a product-quality judgment). "verified" is the only clean
# high; the two real-but-unresolved-review states sit lower; the two
# adjudicated-bad states sit lowest; an unresolved pid (registry miss, or
# this worktree has no registry at all) is honestly None -- there is no
# registry signal to score at all, this is not a case to guess a number for.
_BARCODE_STATUS_TO_IDENTITY_CONFIDENCE = {
    "verified": 1.0,
    "pending_manual_review": 0.5,
    "malformed": 0.3,
    "found_but_conflicting": 0.2,
    "not_found": 0.1,
}


def _identity_confidence(layer1: dict) -> Tuple[Optional[float], str, Optional[str]]:
    status = layer1.get("barcode_state", {}).get("status")
    if layer1.get("pid_status") != "resolved" or status not in _BARCODE_STATUS_TO_IDENTITY_CONFIDENCE:
        return (
            None,
            "unresolved_pid_no_registry_signal",
            f"pid_status={layer1.get('pid_status')!r}, registry barcode_status={status!r}: "
            f"no adjudicated registry signal to score",
        )
    value = _BARCODE_STATUS_TO_IDENTITY_CONFIDENCE[status]
    return value, "registry_barcode_status_mapped", f"mapped from registry barcode_status={status!r}"


def build_layer3(product: dict, trace: Optional[dict], layer2_cells: Dict[str, dict], meta: dict, layer1: dict) -> Layer3:
    cov = layer2_evidence.coverage_stats(layer2_cells)

    # --- assessment: BSIP2 trace ONLY when present; published fallback is
    # honestly labeled "published_json_as_record" (TASK-563 class shelves),
    # never silently presented as a fresh assessment.
    assessment: Dict[str, Metric] = {}
    if trace is not None:
        for key, trace_key in [
            ("final_score_estimate", "final_score_estimate"),
            ("grade_estimate", "grade_estimate"),
            ("category", "category"),
            ("nova_proxy", "nova_proxy"),
            ("confidence_score", "confidence_score"),
            ("dimension_scores", "dimension_scores"),
        ]:
            assessment[key] = Metric(
                key=key, axis="assessment", value=trace.get(trace_key),
                derivation="bsip2_trace", inputs=["bsip2_trace"],
            )
    else:
        for key, prod_key in [("final_score_estimate", "score"), ("grade_estimate", "grade")]:
            assessment[key] = Metric(
                key=key, axis="assessment", value=product.get(prod_key),
                derivation="published_json_as_record", inputs=["served_json_verbatim"],
                note="no recoverable BSIP2 trace for this product (TASK-563 class gap)",
            )
        for key in ("category", "nova_proxy", "confidence_score", "dimension_scores"):
            assessment[key] = Metric(
                key=key, axis="assessment", value=None,
                derivation="published_json_as_record", inputs=["served_json_verbatim"],
                note="not recoverable without a trace",
            )

    # --- data_quality: computed from Layer-2 coverage (+ Layer-1 registry
    # signal for identity_confidence) only. Never reads an assessment or
    # publication_record value.
    identity_confidence_value, identity_confidence_derivation, identity_confidence_note = _identity_confidence(layer1)
    data_quality: Dict[str, Metric] = {
        "evidence_completeness": Metric(
            key="evidence_completeness", axis="data_quality",
            value=round(cov["fields_retrieved"] / cov["fields_total"], 4) if cov["fields_total"] else None,
            derivation="layer2_coverage", inputs=["layer2_evidence"],
        ),
        "evidence_flag_rate": Metric(
            key="evidence_flag_rate", axis="data_quality",
            value=round(cov["fields_flagged"] / cov["fields_total"], 4) if cov["fields_total"] else None,
            derivation="layer2_coverage", inputs=["layer2_evidence"],
        ),
        "identity_confidence": Metric(
            key="identity_confidence", axis="data_quality",
            value=identity_confidence_value,
            derivation=identity_confidence_derivation, inputs=["layer1_identity"],
            note=identity_confidence_note,
        ),
        "image_confidence": Metric(
            key="image_confidence", axis="data_quality", value=None,
            derivation="deferred_mvp_scope", inputs=["layer1_identity"],
            note="explicitly deferred per memo section 5 (MVP boundary)",
        ),
    }

    # --- publication_record: served JSON verbatim, stamped run_id + trace hash.
    trace_hash = _sha256_of_obj(trace) if trace is not None else None
    publication_record: Dict[str, Metric] = {
        "score": Metric(key="score", axis="publication_record", value=product.get("score"),
                         derivation="served_json_verbatim", inputs=["served_json_verbatim"]),
        "grade": Metric(key="grade", axis="publication_record", value=product.get("grade"),
                         derivation="served_json_verbatim", inputs=["served_json_verbatim"]),
        "run_id": Metric(key="run_id", axis="publication_record", value=meta.get("run_id"),
                          derivation="served_meta_verbatim", inputs=["served_json_verbatim"]),
        "trace_hash": Metric(key="trace_hash", axis="publication_record", value=trace_hash,
                              derivation="computed_over_trace_file" if trace is not None else "no_trace_available",
                              inputs=["bsip2_trace"]),
    }

    return Layer3(assessment=assessment, data_quality=data_quality, publication_record=publication_record)


def build_dossier_for_product(
    product: dict,
    shelf_id: str,
    category_folder: Optional[str],
    by_pair: Dict[Tuple[str, str], dict],
    by_gtin: Dict[str, List[dict]],
    traces: Dict[str, dict],
    meta: dict,
    config_path: Path,
) -> dict:
    rg = load_run_gates()
    barcode = rg.get_barcode_from_product(product)
    retailer = product.get("retailer") or "unknown"

    layer2_cells, match_note = layer2_evidence.assemble_layer2_for_product(
        retailer, barcode, category_folder, by_pair, by_gtin
    )
    layer1 = layer1_identity.assemble_layer1(product, layer2_cells)
    trace = traces.get(barcode)
    layer3 = build_layer3(product, trace, layer2_cells, meta, layer1)
    checks = layer4_checks.run_all_checks(product, layer2_cells, match_note, trace, layer1)

    return {
        "generation": {
            "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),  # wall-clock OK: metadata only
            "compiler_version": COMPILER_VERSION,
            "parser_version": layer2_evidence.parser_version(),
            "shelf_id": shelf_id,
            "shelf_config_path": str(config_path.relative_to(REPO_ROOT)),
            "capture_match_note": match_note,
        },
        "layer_1": layer1,
        "layer_2": layer2_cells,
        "layer_3": layer3.to_dict(),
        "layer_4": {k: v.to_dict() for k, v in checks.items()},
    }


def canonical_for_check(dossier: dict) -> dict:
    """Strip the one wall-clock field before comparing/hashing -- generated_at
    is metadata-only per spec ("a generation generated_at metadata field is
    fine") and must never cause spurious --check drift.
    """
    d = json.loads(json.dumps(dossier))
    d.get("generation", {}).pop("generated_at", None)
    return d


def process_shelf(shelf_id: str, cfg: dict, config_path: Path, by_pair, by_gtin, limit: Optional[int]):
    rg = load_run_gates()
    baseline_path = rebase_path(cfg["baseline_json"])
    run_dirs = [rebase_path(p) for p in normalize_dirs(cfg.get("run_products_dir"))]
    if not baseline_path.is_file():
        return shelf_id, [], {"error": f"baseline_json not found at rebased path {baseline_path}"}

    frontend = json.loads(baseline_path.read_text(encoding="utf-8"))
    products = frontend.get("products", [])
    if limit:
        products = products[:limit]
    meta = frontend.get("_meta", {})
    # First dir wins on barcode collision -- same semantics
    # validate_comparison_page.py documents for its own --traces nargs="+".
    traces: Dict[str, dict] = {}
    any_dir_found = False
    for run_dir in run_dirs:
        if not run_dir.is_dir():
            continue
        any_dir_found = True
        for bc, t in rg.load_bsip2_traces(str(run_dir)).items():
            traces.setdefault(bc, t)
    category_folder = category_folder_from_config(cfg)

    dossiers = []
    pid_resolved = 0
    for product in products:
        dossier = build_dossier_for_product(
            product, shelf_id, category_folder, by_pair, by_gtin, traces, meta, config_path
        )
        # Key by the real bari_pid when the registry resolved this product;
        # provisional_key (the served id) is the fallback ONLY for the
        # genuinely unresolvable case (registry miss / registry absent) --
        # never a re-adjudication, per lib/registry_interface.py.
        layer1 = dossier["layer_1"]
        if layer1["pid_status"] == "resolved" and layer1["pid"]:
            pid_resolved += 1
            key = layer1["pid"]
        else:
            key = layer1["provisional_key"]
        dossiers.append((key, dossier))

    stats = {
        "product_count": len(products),
        "trace_dir_found": any_dir_found,
        "trace_count_available": len(traces),
        "pid_resolved_count": pid_resolved,
        "pid_unresolved_count": len(dossiers) - pid_resolved,
    }
    return shelf_id, dossiers, stats


def cmd_build(args) -> int:
    manifest = layer2_evidence.load_manifest()
    by_pair, by_gtin = layer2_evidence.build_capture_index(manifest)

    only = args.shelves.split(",") if args.shelves else None
    shelves = discover_shelf_configs(only=only)
    if not shelves:
        print("No shelf configs discovered (check --shelves filter).", file=sys.stderr)
        return 1

    out_dir = Path(args.out_dir) if args.out_dir else DEFAULT_OUT_DIR
    assert_write_boundary(out_dir)

    summary = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "compiler_version": COMPILER_VERSION,
        "parser_version": layer2_evidence.parser_version(),
        "note": "UNCOMMITTED pre-fix sample projection -- see TASK-610 return contract. "
                "Never a comparison baseline (R-D).",
        "shelves": {},
    }

    total_products = 0
    total_dossiers = 0
    total_pid_resolved = 0
    check_tally: Dict[str, Dict[str, int]] = {}
    registry_barcode_status_tally: Dict[str, int] = {}

    for shelf_id, cfg, config_path in shelves:
        shelf_id_out, dossiers, stats = process_shelf(shelf_id, cfg, config_path, by_pair, by_gtin, args.limit)
        if "error" in stats:
            summary["shelves"][shelf_id_out] = stats
            continue

        shelf_out_dir = out_dir / shelf_id_out
        shelf_out_dir.mkdir(parents=True, exist_ok=True)
        assert_write_boundary(shelf_out_dir)

        for key, dossier in dossiers:
            safe_key = re.sub(r"[^A-Za-z0-9_.-]", "_", key)
            out_path = shelf_out_dir / f"{safe_key}.json"
            assert_write_boundary(out_path)
            out_path.write_text(json.dumps(dossier, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")

            for check_name, check_result in dossier["layer_4"].items():
                check_tally.setdefault(check_name, {"pass": 0, "fail": 0, "warn": 0, "unknown": 0})
                check_tally[check_name][check_result["status"]] = check_tally[check_name].get(check_result["status"], 0) + 1

            registry_status = dossier["layer_1"]["barcode_state"]["status"]
            registry_barcode_status_tally[registry_status] = registry_barcode_status_tally.get(registry_status, 0) + 1

        total_products += stats["product_count"]
        total_dossiers += len(dossiers)
        total_pid_resolved += stats.get("pid_resolved_count", 0)
        summary["shelves"][shelf_id_out] = stats

    summary["total_products"] = total_products
    summary["total_dossiers_written"] = total_dossiers
    summary["total_pid_resolved"] = total_pid_resolved
    summary["total_pid_unresolved"] = total_dossiers - total_pid_resolved
    summary["registry_barcode_status_tally"] = registry_barcode_status_tally
    summary["layer4_check_tally"] = check_tally

    assert_write_boundary(MANIFEST_SUMMARY_PATH)
    MANIFEST_SUMMARY_PATH.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")

    print(f"Built {total_dossiers} dossiers across {len(shelves)} shelves ({total_products} products scanned).")
    print(f"Sample written to: {out_dir}")
    print(f"Manifest summary: {MANIFEST_SUMMARY_PATH}")
    print(f"pid resolved: {total_pid_resolved}/{total_dossiers}; registry barcode_status tally: "
          f"{json.dumps(registry_barcode_status_tally, sort_keys=True)}")
    print(f"Layer-4 check tally: {json.dumps(check_tally, sort_keys=True)}")
    return 0


def cmd_check(args) -> int:
    manifest = layer2_evidence.load_manifest()
    by_pair, by_gtin = layer2_evidence.build_capture_index(manifest)
    only = args.shelves.split(",") if args.shelves else None
    shelves = discover_shelf_configs(only=only)

    actual_lines = []
    for shelf_id, cfg, config_path in shelves:
        _, dossiers, stats = process_shelf(shelf_id, cfg, config_path, by_pair, by_gtin, args.limit)
        if "error" in stats:
            continue
        for key, dossier in dossiers:
            actual_lines.append(json.dumps(
                {"shelf": shelf_id, "key": key, "dossier": canonical_for_check(dossier)},
                sort_keys=True, ensure_ascii=False, separators=(",", ":"),
            ) + "\n")

    if not BASELINE_PATH.exists():
        print(
            "No committed dossier_baseline.jsonl yet -- expected per R-D (the committed baseline "
            "waits on the BSIP0 parser fix + replay re-baseline; this compiler must not produce one "
            "prematurely). This is NOT a failure of --check; it means the CI gate has nothing to "
            "compare against yet."
        )
        print(f"Current build would emit {len(actual_lines)} dossier lines across {len(shelves)} shelves.")
        return 0

    expected_lines = BASELINE_PATH.read_text(encoding="utf-8").splitlines(keepends=True)
    if actual_lines != expected_lines:
        print("dossier baseline drift detected.")
        return 2
    print(f"dossier baseline check passed: {len(actual_lines)} rows")
    return 0


def cmd_write_baseline(args) -> int:
    """Dormant adapter. Writes the COMMITTED baseline. Per R-D this must
    only ever be invoked AFTER the BSIP0 parser fix lands and replay is
    re-baselined -- this task does not call it.
    """
    print(
        "REFUSING to write dossier_baseline.jsonl automatically: R-D requires the parser fix + "
        "replay re-baseline to land FIRST (TASK-610 scope explicitly forbids committing a baseline "
        "now). Pass --force-write-baseline-i-have-verified-the-parser-fix-landed to override.",
        file=sys.stderr,
    )
    if not args.force_write_baseline:
        return 1
    manifest = layer2_evidence.load_manifest()
    by_pair, by_gtin = layer2_evidence.build_capture_index(manifest)
    shelves = discover_shelf_configs()
    lines = []
    for shelf_id, cfg, config_path in shelves:
        _, dossiers, stats = process_shelf(shelf_id, cfg, config_path, by_pair, by_gtin, None)
        if "error" in stats:
            continue
        for key, dossier in dossiers:
            lines.append(json.dumps(
                {"shelf": shelf_id, "key": key, "dossier": canonical_for_check(dossier)},
                sort_keys=True, ensure_ascii=False, separators=(",", ":"),
            ) + "\n")
    assert_write_boundary(BASELINE_PATH)
    BASELINE_PATH.write_text("".join(lines), encoding="utf-8")
    print(f"dossier_baseline.jsonl written: {len(lines)} rows")
    return 0


def cmd_selftest(args) -> int:
    failures = []

    # (1) cross-namespace metric fails the build
    try:
        Layer3(data_quality={
            "evidence_completeness": Metric(
                key="evidence_completeness", axis="data_quality", value=0.5,
                derivation="layer2_coverage", inputs=["assessment"],
            )
        })
        failures.append("cross-namespace metric did NOT raise NamespaceViolation")
    except NamespaceViolation:
        print("[PASS] cross-namespace metric input raises NamespaceViolation")
    except Exception as e:
        failures.append(f"cross-namespace metric raised wrong exception type: {type(e).__name__}: {e}")

    # (1b) banned overall_score field fails the build
    try:
        Layer3(assessment={
            "overall_score": Metric(key="overall_score", axis="assessment", value=72.0, derivation="bsip2_trace")
        })
        failures.append("overall_score metric did NOT raise NamespaceViolation")
    except NamespaceViolation:
        print("[PASS] overall_score field raises NamespaceViolation (banned per memo)")
    except Exception as e:
        failures.append(f"overall_score raised wrong exception type: {type(e).__name__}: {e}")

    # (2) banned-source cell fails the build -- both unit-level and via the
    # real assembly path with a synthetic manifest index. banned marker
    # (TASK-238) used only to prove rejection -- never a real source.
    try:
        layer2_evidence.assert_source_not_banned("open_food_facts", context="selftest")  # banned marker, synthetic
        failures.append("assert_source_not_banned did NOT raise for a banned marker")
    except DossierBuildError:
        print("[PASS] banned-source marker raises DossierBuildError (unit level)")

    banned_marker_value = "open_food_facts"  # banned marker (TASK-238) -- synthetic fixture, used only to prove rejection
    synthetic_by_pair = {
        (banned_marker_value, "9999999999999"): {
            "retailer": banned_marker_value, "gtin": "9999999999999",  # banned marker synthetic fixture, never real
            "capture_file": "02_products/fake/bsip0_outputs/fake.json", "object_path": "/0",
            "scrape_timestamp": "2026-01-01T00:00:00Z", "content_hash": "deadbeef", "canonical": True,
        }
    }
    try:
        layer2_evidence.assemble_layer2_for_product(
            banned_marker_value, "9999999999999", None, synthetic_by_pair, {}  # banned marker synthetic fixture
        )
        failures.append("assemble_layer2_for_product did NOT raise for a banned-source manifest record")
    except DossierBuildError:
        print("[PASS] banned-source manifest record raises DossierBuildError (assembly level)")

    # (3) missing -> null, no imputation
    manifest = layer2_evidence.load_manifest()
    by_pair, by_gtin = layer2_evidence.build_capture_index(manifest)
    cells, note = layer2_evidence.assemble_layer2_for_product(
        "shufersal", "0000000000000_does_not_exist", None, by_pair, by_gtin
    )
    null = layer2_evidence.null_cell()
    if note == "no_canonical_capture" and all(c == null for c in cells.values()):
        print("[PASS] missing capture -> every field cell is the exact null_cell() shape (no imputation)")
    else:
        failures.append(f"missing-capture path did not produce pure null cells: note={note} cells={cells}")

    # (4) Layer-2 dereference matches replay_harness on a sample (dynamic --
    # compare against a live replay() run, not hardcoded constants)
    rh = layer2_evidence.replay_harness()
    replay_rows = rh.replay()
    replay_index = {(r["retailer"], r["gtin"], r["field"]): r for r in replay_rows}

    sample_checks = [("unknown", "3075805", "sodium", "brined_cheeses"), ("unknown", "5010029000061", "fat", "breakfast_cereals")]
    for retailer, gtin, field, category_folder in sample_checks:
        expected = replay_index.get((retailer, gtin, field))
        if expected is None:
            failures.append(f"selftest sample ({retailer},{gtin},{field}) not found in this worktree's replay() output "
                             f"-- corpus drift, update the selftest sample pair")
            continue
        cells, match_note = layer2_evidence.assemble_layer2_for_product(
            retailer, gtin, category_folder, by_pair, by_gtin
        )
        actual = cells[field]
        if (actual["raw_source_text"] == expected["raw_value"]
                and actual["value"] == expected["parsed_value"]
                and actual["flags"] == expected["flags"]):
            print(f"[PASS] Layer-2 cell for ({retailer},{gtin},{field}) exact-matches replay_harness.replay(): "
                  f"raw={actual['raw_source_text']!r} flags={actual['flags']}")
        else:
            failures.append(
                f"Layer-2/replay mismatch for ({retailer},{gtin},{field}): "
                f"compiler={actual['raw_source_text']!r}/{actual['value']}/{actual['flags']} vs "
                f"replay={expected['raw_value']!r}/{expected['parsed_value']}/{expected['flags']}"
            )

    if failures:
        print("\nSELFTEST FAILURES:")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("\nALL SELFTEST CHECKS PASSED (4/4 required proofs + 1 bonus overall_score proof).")
    return 0


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--shelves", help="comma-separated shelf ids (config filename stems) to restrict to")
    ap.add_argument("--out-dir", help=f"output dir for sample dossiers (default: {DEFAULT_OUT_DIR})")
    ap.add_argument("--limit", type=int, help="max products per shelf (dev convenience)")
    ap.add_argument("--check", action="store_true", help="compare in-memory build vs committed baseline")
    ap.add_argument("--selftest", action="store_true", help="run the 4 required structural proofs")
    ap.add_argument("--write-baseline", action="store_true", help="dormant adapter, see R-D -- refuses without --force")
    ap.add_argument("--force-write-baseline-i-have-verified-the-parser-fix-landed", dest="force_write_baseline", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return cmd_selftest(args)
    if args.check:
        return cmd_check(args)
    if args.write_baseline:
        return cmd_write_baseline(args)
    return cmd_build(args)


if __name__ == "__main__":
    raise SystemExit(main())
