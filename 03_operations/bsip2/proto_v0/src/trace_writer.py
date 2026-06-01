"""
BSIP2 Prototype v0 — Trace Writer
Assembles and writes the complete bsip2_trace.json for each product.
"""
import json
import pathlib
import datetime


def assemble_trace(product: dict, signals: dict, cat_result: dict,
                   nova_result: dict, eval_result: dict, score_result: dict) -> dict:
    """Assemble the complete trace record."""
    return {
        "bsip2_version": "proto_v0",
        "algorithm_version": "0.4.0",   # TASK-133: protein matrix-awareness + named-additive identity
        "trace_generated_at": datetime.datetime.utcnow().isoformat() + "Z",
        "specification_version": "bsip2_concept_v1 + score_resolution_contract_SRC-v1",

        # Input reference (read-only pointer to BSIP1 record)
        "input_reference": {
            "canonical_product_id": product.get("canonical_product_id"),
            "barcode":              product.get("barcode"),
            "product_name_he":      product.get("canonical_name_he"),
            "brand":                product.get("brand"),
            "source_retailers":     product.get("source_retailers"),
            "bsip1_source_path":    product.get("_source_path"),
            "audit_ref":            product.get("audit_ref"),
            "bsip1_schema_version": product.get("schema_version"),
            "load_errors":          product.get("_load_errors") or [],
        },

        # Evaluation status (Stage 0 — must come first)
        "evaluation_status":    eval_result.get("evaluation_status"),
        "context_flag":         eval_result.get("context_flag"),
        "context_note":         eval_result.get("context_note"),
        "scope_basis":          eval_result.get("scope_basis"),

        # Category and NOVA
        "category":                   cat_result.get("category"),
        "category_confidence":         cat_result.get("category_confidence"),
        "secondary_category":          cat_result.get("secondary_category"),
        "secondary_confidence":        cat_result.get("secondary_confidence"),
        "category_instability_flag":   cat_result.get("category_instability_flag"),
        "category_confidence_band":    cat_result.get("confidence_band"),
        "classification_basis":        cat_result.get("classification_basis"),

        "nova_proxy":              nova_result.get("nova_level"),
        "nova_confidence":         nova_result.get("nova_confidence"),
        "nova_confidence_band":    nova_result.get("nova_confidence_band"),
        "nova_evidence_for":       nova_result.get("nova_evidence_for"),
        "nova_evidence_against":   nova_result.get("nova_evidence_against"),
        "nova_uncertainty_notes":  nova_result.get("nova_uncertainty_notes"),

        # Signal layers L1-L6
        "L1_observed_signals":         signals.get("L1_observed_signals"),
        "L2_derived_signals":          signals.get("L2_derived_signals"),
        "L3_inferred_classifications": signals.get("L3_inferred_classifications"),
        "L4_interpreted_concerns":     signals.get("L4_interpreted_concerns"),
        "L5_behavioral_hypotheses":    signals.get("L5_behavioral_hypotheses"),
        "L6_policy_decisions":         signals.get("L6_policy_decisions"),

        # Scoring trace
        "structural_emptiness_result": score_result.get("structural_emptiness_result"),
        "confidence_score":            score_result.get("confidence_result", {}).get("confidence_score"),
        "confidence_band":             score_result.get("confidence_result", {}).get("confidence_band"),
        "confidence_reductions":       score_result.get("confidence_result", {}).get("confidence_reductions"),

        "dimension_scores":           score_result.get("dimension_scores"),
        "dimension_notes":            score_result.get("dimension_notes"),
        "dimension_weights":          score_result.get("dimension_weights"),
        "weighted_dimension_score":   score_result.get("weighted_dimension_score"),

        "caps_considered":     score_result.get("caps_considered"),
        "caps_applied":        score_result.get("caps_applied"),
        "binding_cap":         score_result.get("binding_cap"),
        "score_after_cap":     score_result.get("score_after_cap"),

        "penalties_considered":           score_result.get("penalties_considered"),
        "penalties_applied":              score_result.get("penalties_applied"),
        "total_penalty_before_scaling":   score_result.get("total_penalty_before_scaling"),
        "total_penalty_after_scaling":    score_result.get("total_penalty_after_scaling"),
        "penalty_scaling_note":           score_result.get("penalty_scaling_note"),
        "score_after_penalty":            score_result.get("score_after_penalty"),

        "concern_family_coordination":    score_result.get("concern_family_coordination"),

        "floors_considered":         score_result.get("floors_considered"),
        "floors_applied":            score_result.get("floors_applied"),
        "score_after_floors":        score_result.get("score_after_floors"),

        "confidence_ceiling_applied": score_result.get("confidence_ceiling_applied"),

        "sugar_context_class": score_result.get("sugar_context_class"),
        "hp_nova_weight":      score_result.get("hp_nova_weight"),

        "final_score_estimate": score_result.get("final_score_estimate"),
        "grade_estimate":       score_result.get("grade_estimate"),
        "data_sufficiency":     score_result.get("data_sufficiency"),

        "explanation_drivers":  score_result.get("explanation_drivers"),
        "unresolved_flags":     score_result.get("unresolved_flags"),
    }


def write_trace(trace: dict, output_root: pathlib.Path) -> pathlib.Path:
    """Write trace JSON to outputs/products/{product_id}/bsip2_trace.json."""
    pid = trace["input_reference"]["canonical_product_id"]
    product_dir = output_root / "products" / pid
    product_dir.mkdir(parents=True, exist_ok=True)
    out_path = product_dir / "bsip2_trace.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(trace, f, ensure_ascii=False, indent=2)
    return out_path
