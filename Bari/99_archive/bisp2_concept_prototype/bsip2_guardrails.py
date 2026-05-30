"""
Rule-engine guardrails with penalty families + HP integration.
"""
from typing import Dict, Any, List
from bsip2_models import Rule, GuardrailResult, TriggeredRule
from bsip2_config import VETO_SCORE_FAIL
from bsip2_calorie_engine import evaluate_calorie_interactions
from bsip2_hyper_palatability import evaluate_hyper_palatability, hyper_palatability_guardrails


STATIC_RULES: List[Rule] = [
    # ---- VETOS ----
    Rule(
        rule_id="TRANS_FAT_VETO", rule_type="veto",
        condition=lambda f: f.get("trans_fat_g_100g", 0) and f["trans_fat_g_100g"] > 0.2,
        value=VETO_SCORE_FAIL,
        rationale="Trans fat present above 0.2g/100g",
        framework_ref="WHO REPLACE / Israeli MoH",
        family="general",
    ),

    # ---- HARD CAPS — PROCESSING family ----
    Rule("NOVA_PROXY_4_ULTRA_PROCESSED", "cap",
         lambda f: f["nova_proxy"] == 4, 60,
         "Likely ultra-processed (NOVA 4 proxy)",
         "NOVA Classification", family="processing"),
    Rule("NOVA_PROXY_3_PROCESSED", "cap",
         lambda f: f["nova_proxy"] == 3, 75,
         "Likely processed (NOVA 3 proxy)",
         "NOVA Classification", family="processing"),

    # ---- HARD CAPS — REGULATORY family ----
    Rule("ISRAELI_RED_LABELS_2_PLUS", "cap",
         lambda f: f["red_label_count"] >= 2, 45,
         "Two or more Israeli MoH red warning labels",
         "Israeli MoH 2017", family="regulatory"),
    Rule("ISRAELI_RED_LABEL_1", "cap",
         lambda f: f["red_label_count"] == 1, 55,
         "One Israeli MoH red warning label",
         "Israeli MoH 2017", family="regulatory"),

    # ---- HARD CAPS — ADDITIVES family ----
    Rule("SWEETENER_PRESENT", "cap",
         lambda f: f["has_sweetener"], 70,
         "Artificial / non-nutritive sweetener present",
         family="additives"),
    Rule("ADDITIVE_MARKERS_5_PLUS", "cap",
         lambda f: f["additive_marker_count"] >= 5, 55,
         "Five or more concerning additive markers",
         family="additives"),
    Rule("ADDITIVE_MARKERS_3_PLUS", "cap",
         lambda f: 3 <= f["additive_marker_count"] < 5, 65,
         "Three or more concerning additive markers",
         family="additives"),

    # ---- HARD CAPS — SUGAR / SODIUM ----
    Rule("HIGH_SUGAR_25G_PLUS", "cap",
         lambda f: f["sugars_g_100g"] >= 25, 60,
         "High sugar (≥25g/100g)", family="sugar"),
    Rule("HIGH_SODIUM_700MG_PLUS", "cap",
         lambda f: f["sodium_mg_100g"] >= 700, 60,
         "High sodium (≥700mg/100g)", family="sodium"),

    # ---- SOFT PENALTIES ----
    Rule("SEED_OIL_PRESENT", "penalty",
         lambda f: f["has_seed_oil"], 3,
         "Industrial seed oil present", family="fat_quality"),
    Rule("LONG_INGREDIENT_LIST", "penalty",
         lambda f: f["ingredient_count"] > 12, 4,
         "Long ingredient list (>12)", family="ingredient_complexity"),
    Rule("MULTIPLE_ADDED_SUGAR_MARKERS", "penalty",
         lambda f: f["added_sugar_marker_count"] >= 2, 5,
         "Multiple distinct added-sugar sources", family="sugar"),

    # ---- FLOORS ----
    Rule("SINGLE_INGREDIENT_WHOLE_FOOD", "floor",
         lambda f: f["ingredient_count"] == 1 and f["nova_proxy"] == 1, 75,
         "Single-ingredient whole food", family="general"),
    Rule("WHOLE_FOOD_FAT_FLOOR", "floor",
         lambda f: f["inferred_category"] == "whole_food_fat" and f["nova_proxy"] in (1, 2), 65,
         "Whole-food fat with minimal processing", family="general"),
]


def _tag_family(rule_list: List[TriggeredRule], default_family: str) -> List[TriggeredRule]:
    for r in rule_list:
        if not getattr(r, "family", None) or r.family == "general":
            r.family = default_family
    return rule_list


def apply_guardrails(features: Dict[str, Any]) -> GuardrailResult:
    result = GuardrailResult()

    # 1. Static rules
    for rule in STATIC_RULES:
        triggered = rule.evaluate(features)
        if not triggered:
            continue
        if triggered.rule_type == "veto" and result.veto is None:
            result.veto = triggered
        elif triggered.rule_type == "cap":
            result.caps.append(triggered)
        elif triggered.rule_type == "penalty":
            result.penalties.append(triggered)
        elif triggered.rule_type == "floor":
            result.floors.append(triggered)

    # 2. Calorie interactions
    cal_caps, cal_penalties, cal_reason_codes = evaluate_calorie_interactions(features)
    result.caps.extend(_tag_family(cal_caps, "calorie_density"))
    result.penalties.extend(_tag_family(cal_penalties, "calorie_density"))
    features["_calorie_reason_codes"] = cal_reason_codes
    features["_calorie_caps_triggered"] = [r.rule_id for r in cal_caps]
    features["_calorie_penalties_triggered"] = [r.rule_id for r in cal_penalties]

    # 3. Hyper-palatability  ← THIS IS THE KEY FIX
    hp = evaluate_hyper_palatability(features)
    features["_hp_result"] = hp     # ← writes _hp_result so score_product can read it
    hp_rules = hyper_palatability_guardrails(features, hp)
    for r in hp_rules:
        r.family = "hyper_palatability"
        if r.rule_type == "cap":
            result.caps.append(r)
        elif r.rule_type == "penalty":
            result.penalties.append(r)

    return result