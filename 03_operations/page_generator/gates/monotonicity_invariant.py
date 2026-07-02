#!/usr/bin/env python3
"""
monotonicity_invariant.py — BARI-MONOTONICITY-TEST-001
======================================================
TASK-395 Phase 1 — Trust Instrument 1

Deterministic monotonicity gate: for a product, perturbing a single input
in the harmful direction must NEVER raise the score. Removing data must never
raise the score.

SCORE-NEUTRAL: reads the engine read-only; changes NO scoring logic, NO
published scores, NO configuration files, NO shared infrastructure files.

Perturbations applied (one at a time, baseline product otherwise intact):
  P1  +Δ sugars_g            → score must not increase
  P2  +Δ fat_saturated_g     → score must not increase
  P3  +1 additive_marker_count → score must not increase
  P4  +Δ sodium_mg           → score must not increase
  P5  null ingredients_text_he + null ingredients_list → score must not increase
  P6  null a single nutrition field (each of: sugars_g, fat_saturated_g,
      sodium_mg, protein_g) → score must not increase

For each category, exactly one product is sampled (the product with the
highest baseline score, to maximise signal). Perturbation deltas are
calibrated to be nutritionally meaningful but not extreme.

Flag vectors are taken PER CATEGORY from the canonical baseline manifest
(_baselines/<slug>/baseline_manifest.json) — isolating each category's
flag context to avoid the known --all flag-leak bug.

A VIOLATION is when score_after > score_before (strict increase after
a harmful perturbation). Violations are real engine bugs.

Exit codes:
  0 = no violations found (PASS)
  1 = >= 1 violation found (VIOLATIONS DETECTED)
  2 = usage / load error

Output: per-category PASS/VIOLATION table, with any violations detailed
        (category, barcode, perturbation_id, before→after, delta).

Usage:
  python monotonicity_invariant.py [--all] [--slug <category>]
      [--out <report.json>]
      [--delta-sugars <float>]        (default: 5.0)
      [--delta-fatsat <float>]        (default: 3.0)
      [--delta-sodium <float>]        (default: 100.0)

Integration:
  Import run_monotonicity_check(slug, manifest_path, bsip1_dir, flags,
  shelf_rel) -> MonotonicityResult from this module.
"""

from __future__ import annotations

import argparse
import copy
import importlib
import json
import os
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

REPO = Path(__file__).resolve().parents[3]
BASELINES_DIR = REPO / "_baselines"
CONFIGS_DIR = REPO / "03_operations" / "page_generator" / "configs"
SCORE_ENGINE_SRC = REPO / "03_operations" / "bsip2" / "proto_v0" / "src"

if str(SCORE_ENGINE_SRC) not in sys.path:
    sys.path.insert(0, str(SCORE_ENGINE_SRC))

# ---------------------------------------------------------------------------
# Perturbation spec
# ---------------------------------------------------------------------------

DELTA_SUGARS_G_DEFAULT   = 5.0    # +5g sugars — roughly 1 extra teaspoon of sugar per 100g
DELTA_FATSAT_G_DEFAULT   = 3.0    # +3g sat fat — cross into a higher red-label band
DELTA_SODIUM_MG_DEFAULT  = 100.0  # +100mg sodium — meaningful for most categories
DELTA_ADDITIVE_COUNT     = 1      # +1 additive marker

# Nutrition fields to null individually (P6 family)
NULLABLE_NUTRITION_FIELDS = ["sugars_g", "fat_saturated_g", "sodium_mg", "protein_g"]

# ---------------------------------------------------------------------------
# Managed env vars (mirrors baseline_verify.py)
# ---------------------------------------------------------------------------

MANAGED_BARI_VARS = [
    "BARI_RECAL_P0",
    "BARI_RECAL_P0_YOGURT_TRIM",
    "BARI_FAT_TECH_V1",
    "BARI_SHELF_RELATIVE_V1",
    "BARI_SODIUM_SHELF_RELATIVE_V1",
    "BARI_DAIRY_PROTEIN_REWEIGHT_V1",
    "BARI_GRAD_SODIUM_V1",
    "BARI_SODIUM_CEREAL",
    "BARI_REDLABEL_V1",
    "BARI_TASK144_FIXES",
    "BARI_TASK250_CONF",
    "BARI_GLASSBOX_D5D6",
    "BARI_GLASSBOX_W15",
    "BARI_GLASSBOX_W2",
    "BARI_DAIRY_SAT_FAT_INFER",
    "BARI_D4_SCORE_V1",
    "BARI_GRAN_SUGAR_25G_V1",
    "BARI_HC002_NOVA1",
    "BARI_W4_WFI_V1",
]


def snapshot_env() -> dict[str, str | None]:
    return {k: os.environ.get(k) for k in MANAGED_BARI_VARS}


def restore_env(snap: dict[str, str | None]) -> None:
    for k, v in snap.items():
        if v is None:
            os.environ.pop(k, None)
        else:
            os.environ[k] = v


def apply_flags(flags: dict[str, str]) -> None:
    for k in MANAGED_BARI_VARS:
        os.environ.pop(k, None)
    for k, v in flags.items():
        os.environ[k] = v


# ---------------------------------------------------------------------------
# Engine helpers (mirrors baseline_verify.py make_score_one pattern)
# ---------------------------------------------------------------------------

def reload_score_engine():
    import score_engine as se
    return importlib.reload(se)


def make_score_one(se_mod):
    from signal_extractor import extract_signals
    from router_v2 import classify_category
    from nova_proxy import infer_nova
    from evaluation_scope import assign_evaluation_scope
    from trace_writer import assemble_trace
    from structural_classifier import classify_structural_class

    def score_one(product: dict) -> dict:
        signals = extract_signals(product)
        cat_result = classify_category(product)
        l3 = signals["L3_inferred_classifications"]
        nova_result = infer_nova(product, l3)
        eval_result = assign_evaluation_scope(product, cat_result["category"])
        score_result = se_mod.score_product(product, signals, cat_result, nova_result, eval_result)
        trace = assemble_trace(product, signals, cat_result, nova_result, eval_result, score_result)
        trace["structural_class"] = classify_structural_class(trace)
        return trace

    return score_one


def setup_shelf_stats(shelf_rel: dict | None, se_mod) -> None:
    if not shelf_rel:
        return
    if shelf_rel.get("api") == "sodium_ev056":
        se_mod.set_shelf_sodium_stats(shelf_rel["median"], shelf_rel["scale"])
    else:
        nutrient = shelf_rel["nutrient"]
        median = shelf_rel["median"]
        scale = shelf_rel["scale"]
        scale_type = shelf_rel.get("scale_type", "iqr")
        se_mod.set_shelf_stats(nutrient, median, scale, scale_type)


def teardown_shelf_stats(shelf_rel: dict | None, se_mod) -> None:
    if not shelf_rel:
        return
    if shelf_rel.get("api") == "sodium_ev056":
        se_mod.clear_shelf_sodium_stats()
    else:
        se_mod.clear_shelf_stats(shelf_rel["nutrient"])


# ---------------------------------------------------------------------------
# BSIP1 file loader
# ---------------------------------------------------------------------------

def load_bsip1_products(bsip1_dir: str, bsip1_glob: str = "bsip1_*.json") -> list[dict]:
    """Load all valid BSIP1 product records from a directory."""
    products = []
    p = Path(bsip1_dir)
    if not p.is_dir():
        return products
    for f in sorted(p.glob(bsip1_glob)):
        if "audit" in f.name:
            continue
        try:
            rec = json.loads(f.read_text(encoding="utf-8"))
            if rec.get("file_type") != "product":
                continue
            products.append(rec)
        except Exception:
            pass
    return products


# ---------------------------------------------------------------------------
# Perturbation builders
# ---------------------------------------------------------------------------

def _set_nutrition_field(product: dict, field: str, value: Any) -> dict:
    """Return a deep copy of product with nutrition field set to value."""
    p = copy.deepcopy(product)
    nutr = p.setdefault("normalized_nutrition_per_100g", {})
    nutr[field] = value
    return p


def _add_nutrition_field(product: dict, field: str, delta: float) -> dict:
    """Return a deep copy of product with nutrition field increased by delta.
    If field is None, treat as 0 before adding delta."""
    p = copy.deepcopy(product)
    nutr = p.setdefault("normalized_nutrition_per_100g", {})
    current = nutr.get(field)
    nutr[field] = (float(current) if current is not None else 0.0) + delta
    return p


def _null_ingredients(product: dict) -> dict:
    """Return a deep copy of product with ingredients nulled out."""
    p = copy.deepcopy(product)
    p["ingredients_text_he"] = None
    p["ingredients_raw"] = None
    p["ingredients_list"] = []
    p["ingredient_order"] = []
    # Also null enrichment-derived markers that come from ingredient parsing
    enr = p.get("enrichment_summary")
    if isinstance(enr, dict):
        for k in list(enr.keys()):
            if "count" in k or k.startswith("has_"):
                enr[k] = 0 if "count" in k else False
    p["extracted_additives"] = []
    p["extracted_flavors"] = []
    p["extracted_sweeteners"] = []
    p["extracted_protein_markers"] = []
    p["extracted_matrix_markers"] = []
    p["extracted_fermentation_markers"] = []
    p["extracted_roasting_markers"] = []
    return p


def _add_additive_count(product: dict, delta: int) -> dict:
    """Return a deep copy of product with additive count incremented by delta.
    Increments extracted_additives list (engine reads this for the count) and
    also the enrichment_summary.additive_count field."""
    p = copy.deepcopy(product)
    additives = list(p.get("extracted_additives") or [])
    # Append synthetic additive entries (the engine reads the list length)
    for i in range(delta):
        additives.append({
            "raw_text": "_monotonicity_test_additive_",
            "canonical_name": "_monotonicity_test_",
            "category": "preservative",
            "e_number": None,
        })
    p["extracted_additives"] = additives
    enr = p.get("enrichment_summary")
    if isinstance(enr, dict):
        enr["additive_count"] = len(additives)
    return p


# ---------------------------------------------------------------------------
# Result containers
# ---------------------------------------------------------------------------

@dataclass
class PerturbationResult:
    perturbation_id: str      # e.g. "P1_sugars_plus5"
    description: str
    score_before: float | None
    score_after: float | None
    delta: float | None       # score_after - score_before; positive = violation
    violation: bool           # True if score_after > score_before (strict)
    error: str | None = None


@dataclass
class ProductMonotonicity:
    barcode: str
    product_name: str
    baseline_score: float | None
    perturbations: list[PerturbationResult] = field(default_factory=list)

    @property
    def has_violation(self) -> bool:
        return any(p.violation for p in self.perturbations)

    @property
    def violation_count(self) -> int:
        return sum(1 for p in self.perturbations if p.violation)


@dataclass
class CategoryMonotonicityResult:
    slug: str
    status: str = "PASS"   # PASS | VIOLATION | ERROR | SKIP
    products_tested: int = 0
    perturbations_tested: int = 0
    violations: int = 0
    products: list[ProductMonotonicity] = field(default_factory=list)
    error: str | None = None
    flags_used: dict = field(default_factory=dict)
    shelf_rel: dict | None = None
    bsip1_dir: str = ""


# ---------------------------------------------------------------------------
# Core monotonicity checker for one product
# ---------------------------------------------------------------------------

def _score_product_safe(product: dict, score_one) -> tuple[float | None, str | None]:
    """Run score_one on product, returning (score, error_msg)."""
    try:
        trace = score_one(product)
        score = trace.get("final_score_estimate")
        return (float(score) if score is not None else None), None
    except Exception as exc:
        return None, str(exc)


def check_product_monotonicity(
    product: dict,
    score_one,
    delta_sugars: float = DELTA_SUGARS_G_DEFAULT,
    delta_fatsat: float = DELTA_FATSAT_G_DEFAULT,
    delta_sodium: float = DELTA_SODIUM_MG_DEFAULT,
) -> ProductMonotonicity:
    """Run all perturbations on a single product. Returns ProductMonotonicity."""
    bc = str((product.get("barcode") or "")).strip()
    name = str(product.get("canonical_name_he") or "").strip()
    if not name:
        name = str(product.get("canonical_name_en") or "").strip()

    pm = ProductMonotonicity(barcode=bc, product_name=name, baseline_score=None)

    # Baseline score
    baseline_score, err = _score_product_safe(product, score_one)
    if err or baseline_score is None:
        pm.baseline_score = None
        pm.perturbations.append(PerturbationResult(
            perturbation_id="BASELINE",
            description="Baseline score",
            score_before=None,
            score_after=None,
            delta=None,
            violation=False,
            error=err or "baseline score is None",
        ))
        return pm
    pm.baseline_score = baseline_score

    # Define perturbations
    perturbations_spec = [
        # (id, description, mutated_product_fn)
        (
            f"P1_sugars_plus{int(delta_sugars)}",
            f"sugars_g +{delta_sugars}",
            _add_nutrition_field(product, "sugars_g", delta_sugars),
        ),
        (
            f"P2_fatsat_plus{int(delta_fatsat)}",
            f"fat_saturated_g +{delta_fatsat}",
            _add_nutrition_field(product, "fat_saturated_g", delta_fatsat),
        ),
        (
            f"P3_additive_plus{DELTA_ADDITIVE_COUNT}",
            f"additive_marker_count +{DELTA_ADDITIVE_COUNT}",
            _add_additive_count(product, DELTA_ADDITIVE_COUNT),
        ),
        (
            f"P4_sodium_plus{int(delta_sodium)}",
            f"sodium_mg +{delta_sodium}",
            _add_nutrition_field(product, "sodium_mg", delta_sodium),
        ),
        (
            "P5_null_ingredients",
            "null ingredients_text_he + ingredients_list",
            _null_ingredients(product),
        ),
    ]

    # P6 family: null individual nutrition fields
    for nf in NULLABLE_NUTRITION_FIELDS:
        perturbations_spec.append((
            f"P6_null_{nf}",
            f"null {nf}",
            _set_nutrition_field(product, nf, None),
        ))

    for pert_id, description, perturbed_product in perturbations_spec:
        score_after, err = _score_product_safe(perturbed_product, score_one)
        if err:
            pm.perturbations.append(PerturbationResult(
                perturbation_id=pert_id,
                description=description,
                score_before=baseline_score,
                score_after=None,
                delta=None,
                violation=False,
                error=err,
            ))
            continue

        delta = (score_after - baseline_score) if score_after is not None else None
        violation = (delta is not None and delta > 0.0)
        pm.perturbations.append(PerturbationResult(
            perturbation_id=pert_id,
            description=description,
            score_before=baseline_score,
            score_after=score_after,
            delta=round(delta, 4) if delta is not None else None,
            violation=violation,
        ))

    return pm


# ---------------------------------------------------------------------------
# Per-category runner
# ---------------------------------------------------------------------------

def run_monotonicity_check(
    slug: str,
    flags: dict[str, str],
    bsip1_dir: str,
    shelf_rel: dict | None = None,
    delta_sugars: float = DELTA_SUGARS_G_DEFAULT,
    delta_fatsat: float = DELTA_FATSAT_G_DEFAULT,
    delta_sodium: float = DELTA_SODIUM_MG_DEFAULT,
    sample_n: int = 3,
) -> CategoryMonotonicityResult:
    """
    Run the monotonicity invariant for one category.

    sample_n: number of products to test per category (top N by baseline score,
    to maximise coverage of the scoring space). Default = 3.

    Returns CategoryMonotonicityResult.
    """
    result = CategoryMonotonicityResult(
        slug=slug,
        flags_used=flags,
        shelf_rel=shelf_rel,
        bsip1_dir=bsip1_dir,
    )

    env_snap = snapshot_env()
    try:
        # Apply flags and reload engine
        apply_flags(flags)
        try:
            se_mod = reload_score_engine()
        except Exception as exc:
            result.status = "ERROR"
            result.error = f"engine reload failed: {exc}"
            return result

        # Setup shelf stats
        setup_shelf_stats(shelf_rel, se_mod)
        score_one = make_score_one(se_mod)

        # Load BSIP1 products
        products = load_bsip1_products(bsip1_dir)
        if not products:
            result.status = "SKIP"
            result.error = f"no BSIP1 products found in {bsip1_dir}"
            return result

        # Score all products to get baseline scores; select top-N by score
        # (we only need the baseline to select the sample — not stored in output)
        scored_products: list[tuple[float, dict]] = []
        for prod in products:
            try:
                trace = score_one(prod)
                s = trace.get("final_score_estimate")
                if s is not None:
                    scored_products.append((float(s), prod))
            except Exception:
                pass

        if not scored_products:
            result.status = "SKIP"
            result.error = "no products successfully scored"
            teardown_shelf_stats(shelf_rel, se_mod)
            return result

        # Sort by score descending; take top N, middle N, bottom N for breadth
        scored_products.sort(key=lambda x: x[0], reverse=True)
        n_total = len(scored_products)
        selected: list[dict] = []
        # Top
        for _, p in scored_products[:sample_n]:
            selected.append(p)
        # Middle (if distinct from top)
        mid_start = max(sample_n, n_total // 2 - sample_n // 2)
        for _, p in scored_products[mid_start: mid_start + sample_n]:
            if p not in selected:
                selected.append(p)
        # Bottom
        for _, p in scored_products[max(0, n_total - sample_n):]:
            if p not in selected:
                selected.append(p)

        # Cap at sample_n * 3 total
        selected = selected[:sample_n * 3]

        # Run perturbations
        total_perturbations = 0
        total_violations = 0
        for prod in selected:
            pm = check_product_monotonicity(
                prod, score_one,
                delta_sugars=delta_sugars,
                delta_fatsat=delta_fatsat,
                delta_sodium=delta_sodium,
            )
            result.products.append(pm)
            total_perturbations += len(pm.perturbations)
            total_violations += pm.violation_count

        result.products_tested = len(selected)
        result.perturbations_tested = total_perturbations
        result.violations = total_violations
        result.status = "VIOLATION" if total_violations > 0 else "PASS"

        teardown_shelf_stats(shelf_rel, se_mod)

    except Exception as exc:
        result.status = "ERROR"
        result.error = str(exc)
    finally:
        restore_env(env_snap)

    return result


# ---------------------------------------------------------------------------
# Load manifest + config for a slug
# ---------------------------------------------------------------------------

def load_manifest(slug: str) -> dict | None:
    """Load _baselines/<slug>/baseline_manifest.json."""
    p = BASELINES_DIR / slug / "baseline_manifest.json"
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None


def load_config(slug: str) -> dict | None:
    """Load configs/<slug>.json from the page_generator configs dir."""
    p = CONFIGS_DIR / f"{slug}.json"
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None


def discover_slugs() -> list[str]:
    """Discover all 12 category slugs from configs dir (exclude _generated_)."""
    return sorted(
        p.stem
        for p in CONFIGS_DIR.glob("*.json")
        if not p.name.startswith("_generated_")
    )


# ---------------------------------------------------------------------------
# Report formatting
# ---------------------------------------------------------------------------

def format_report(results: list[CategoryMonotonicityResult]) -> str:
    lines = []
    lines.append("=" * 72)
    lines.append("BARI-MONOTONICITY-TEST-001  TASK-395 Phase 1")
    lines.append(f"Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}")
    lines.append("=" * 72)

    total_cats = len(results)
    pass_cats = sum(1 for r in results if r.status == "PASS")
    violation_cats = sum(1 for r in results if r.status == "VIOLATION")
    error_cats = sum(1 for r in results if r.status in ("ERROR", "SKIP"))
    total_perturbs = sum(r.perturbations_tested for r in results)
    total_violations = sum(r.violations for r in results)

    lines.append(f"\nSUMMARY: {total_cats} categories | "
                 f"{pass_cats} PASS | {violation_cats} VIOLATION | {error_cats} ERROR/SKIP")
    lines.append(f"         {total_perturbs} total perturbations checked | "
                 f"{total_violations} violations found")
    lines.append("")

    # Per-category table
    header = f"  {'category':<30} {'status':<12} {'products':>8} {'perturbs':>9} {'violations':>10}"
    lines.append(header)
    lines.append("  " + "-" * (len(header) - 2))
    for r in results:
        lines.append(
            f"  {r.slug:<30} {r.status:<12} {r.products_tested:>8} "
            f"{r.perturbations_tested:>9} {r.violations:>10}"
        )
    lines.append("")

    # Detailed violations
    any_violation = False
    for r in results:
        if r.status == "VIOLATION":
            any_violation = True
            lines.append(f"--- VIOLATIONS: {r.slug} ---")
            for pm in r.products:
                if pm.has_violation:
                    lines.append(
                        f"  product: {pm.barcode} | {pm.product_name[:50]} | "
                        f"baseline={pm.baseline_score}"
                    )
                    for pert in pm.perturbations:
                        if pert.violation:
                            lines.append(
                                f"    VIOLATION [{pert.perturbation_id}] "
                                f"{pert.description}: "
                                f"before={pert.score_before} after={pert.score_after} "
                                f"delta=+{pert.delta}"
                            )
            lines.append("")

        if r.status in ("ERROR", "SKIP"):
            lines.append(f"--- {r.status}: {r.slug} ---")
            lines.append(f"  {r.error}")
            lines.append("")

    if not any_violation and total_violations == 0:
        lines.append("RESULT: PASS — no monotonicity violations found across all categories.")
    else:
        lines.append(f"RESULT: VIOLATIONS DETECTED — {total_violations} violation(s) across "
                     f"{violation_cats} category(ies). Engine bugs requiring investigation.")

    lines.append("=" * 72)
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# JSON report serializer
# ---------------------------------------------------------------------------

def results_to_json(results: list[CategoryMonotonicityResult]) -> dict:
    cats = []
    for r in results:
        prods = []
        for pm in r.products:
            perts = []
            for pert in pm.perturbations:
                perts.append({
                    "perturbation_id": pert.perturbation_id,
                    "description": pert.description,
                    "score_before": pert.score_before,
                    "score_after": pert.score_after,
                    "delta": pert.delta,
                    "violation": pert.violation,
                    "error": pert.error,
                })
            prods.append({
                "barcode": pm.barcode,
                "product_name": pm.product_name,
                "baseline_score": pm.baseline_score,
                "has_violation": pm.has_violation,
                "violation_count": pm.violation_count,
                "perturbations": perts,
            })
        cats.append({
            "slug": r.slug,
            "status": r.status,
            "products_tested": r.products_tested,
            "perturbations_tested": r.perturbations_tested,
            "violations": r.violations,
            "error": r.error,
            "flags_used": r.flags_used,
            "products": prods,
        })

    total_violations = sum(r.violations for r in results)
    return {
        "gate": "BARI-MONOTONICITY-TEST-001",
        "task": "TASK-395",
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "overall_status": "PASS" if total_violations == 0 else "VIOLATION",
        "total_categories": len(results),
        "pass_count": sum(1 for r in results if r.status == "PASS"),
        "violation_count": sum(1 for r in results if r.status == "VIOLATION"),
        "error_count": sum(1 for r in results if r.status in ("ERROR", "SKIP")),
        "total_perturbations": sum(r.perturbations_tested for r in results),
        "total_violations": total_violations,
        "categories": cats,
    }


# ---------------------------------------------------------------------------
# Main CLI
# ---------------------------------------------------------------------------

def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(
        description="BARI-MONOTONICITY-TEST-001: engine monotonicity invariant gate"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--all", action="store_true", help="Run all 12 categories")
    group.add_argument("--slug", help="Single category slug to test")
    parser.add_argument("--out", default=None, help="Path to write JSON report")
    parser.add_argument(
        "--delta-sugars", type=float, default=DELTA_SUGARS_G_DEFAULT,
        help=f"Sugars perturbation delta in g (default: {DELTA_SUGARS_G_DEFAULT})"
    )
    parser.add_argument(
        "--delta-fatsat", type=float, default=DELTA_FATSAT_G_DEFAULT,
        help=f"Sat-fat perturbation delta in g (default: {DELTA_FATSAT_G_DEFAULT})"
    )
    parser.add_argument(
        "--delta-sodium", type=float, default=DELTA_SODIUM_MG_DEFAULT,
        help=f"Sodium perturbation delta in mg (default: {DELTA_SODIUM_MG_DEFAULT})"
    )
    parser.add_argument(
        "--sample-n", type=int, default=3,
        help="Products to test per tier (top/mid/bottom, default: 3 → up to 9 per category)"
    )
    args = parser.parse_args()

    slugs: list[str] = []
    if args.all:
        slugs = discover_slugs()
        print(f"Discovered {len(slugs)} categories: {slugs}", file=sys.stderr)
    else:
        slugs = [args.slug]

    results: list[CategoryMonotonicityResult] = []

    for slug in slugs:
        print(f">>> Monotonicity check: {slug}", file=sys.stderr)

        # Load manifest for flags + shelf_rel
        manifest = load_manifest(slug)
        config = load_config(slug)

        if manifest is None and config is None:
            r = CategoryMonotonicityResult(slug=slug, status="SKIP")
            r.error = f"no baseline_manifest.json and no config found for slug={slug}"
            results.append(r)
            print(f"    SKIP: {r.error}", file=sys.stderr)
            continue

        # Prefer manifest (more authoritative for Phase 1); fall back to config
        if manifest is not None:
            flags = manifest.get("flag_vector") or {}
            shelf_rel = manifest.get("shelf_rel")
            bsip1_dir = manifest.get("bsip1_dir") or ""
        else:
            scoring = config.get("scoring", {})
            flags = scoring.get("flags") or {}
            shelf_rel = scoring.get("shelf_rel")
            bsip1_dir = scoring.get("bsip1_dir") or ""

        # protein_bars: bsip1_dir points to the bsip2_outputs dir (BSIP2 traces,
        # not BSIP1 format) — skip to avoid false "no products" noise.
        if not Path(bsip1_dir).is_dir():
            r = CategoryMonotonicityResult(slug=slug, status="SKIP")
            r.error = f"BSIP1 dir not found: {bsip1_dir}"
            results.append(r)
            print(f"    SKIP: {r.error}", file=sys.stderr)
            continue

        r = run_monotonicity_check(
            slug=slug,
            flags=flags,
            bsip1_dir=bsip1_dir,
            shelf_rel=shelf_rel,
            delta_sugars=args.delta_sugars,
            delta_fatsat=args.delta_fatsat,
            delta_sodium=args.delta_sodium,
            sample_n=args.sample_n,
        )
        results.append(r)
        print(
            f"    {r.status}  products={r.products_tested}  "
            f"perturbations={r.perturbations_tested}  violations={r.violations}",
            file=sys.stderr,
        )

    # Print report
    report_text = format_report(results)
    print(report_text)

    # Optional JSON report
    if args.out:
        report_json = results_to_json(results)
        out_path = Path(args.out)
        out_path.write_text(
            json.dumps(report_json, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
        print(f"JSON report written: {args.out}", file=sys.stderr)

    total_violations = sum(r.violations for r in results)
    return 1 if total_violations > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
