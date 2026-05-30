"""
BSIP2 Dashboard — Anomaly Detection Engine
Severity-tiered detection of architectural violations and engineering edge cases.
"""
import pandas as pd

SEVERITY_COLORS = {
    "CRITICAL": "#c0392b",
    "HIGH":     "#e67e22",
    "MEDIUM":   "#b7950b",
    "LOW":      "#1a5276",
}
SEVERITY_TEXT_COLORS = {
    "CRITICAL": "#fff",
    "HIGH":     "#fff",
    "MEDIUM":   "#fff",
    "LOW":      "#aac8e8",
}
SEVERITY_ORDER = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}


# ── Detection functions ───────────────────────────────────────────────────────

def _nova1_floor_masks_beverage(row: dict) -> bool:
    return (row.get("nova") == 1 and
            row.get("category") == "beverage" and
            row.get("grade") == "A" and
            bool(row.get("floors_applied")))


def _beverage_from_dairy_name(row: dict) -> bool:
    name = str(row.get("name_he", ""))
    return (row.get("category") == "beverage" and
            any(kw in name for kw in ["יוגורט", "קפיר", "לבן", "חלב"]))


def _ingredient_contamination_sauce(row: dict) -> bool:
    name = str(row.get("name_he", ""))
    return (row.get("category") == "sauce_spread" and
            any(kw in name for kw in ["יוגורט", "מוס", "חלב", "דגני"]))


def _ingredient_contamination_whole_food(row: dict) -> bool:
    name = str(row.get("name_he", ""))
    return (row.get("category") == "whole_food_fat" and
            any(kw in name for kw in ["יוגורט", "דגני"]))


def _vanilla_nova4(row: dict) -> bool:
    return (row.get("nova") == 4 and
            bool(row.get("has_flavor_enh")) and
            not bool(row.get("has_sweetener")) and
            int(row.get("additive_count") or 0) <= 2)


def _nova1_cap_conflict(row: dict) -> bool:
    return row.get("nova") == 1 and pd.notna(row.get("binding_cap"))


def _routing_unstable(row: dict) -> bool:
    return bool(row.get("cat_unstable"))


def _high_conf_low_score(row: dict) -> bool:
    return (row.get("conf_band") == "high" and
            float(row.get("score") or 100) < 50)


def _cap_floor_tension(row: dict) -> bool:
    return pd.notna(row.get("binding_cap")) and bool(row.get("floors_applied"))


def _double_red_label(row: dict) -> bool:
    return int(row.get("red_labels") or 0) >= 2


def _sweetener_only_nova4(row: dict) -> bool:
    return (bool(row.get("has_sweetener")) and
            row.get("nova") == 4 and
            not bool(row.get("has_flavor_enh")) and
            int(row.get("additive_count") or 0) <= 2)


def _plant_dairy_confusion(row: dict) -> bool:
    ing = str(row.get("ingredients_text", ""))
    name = str(row.get("name_he", ""))
    markers = ["סויה", "שקדים", "קוקוס", "שיבולת שועל"]
    return (row.get("category") == "dairy_protein" and
            any(kw in ing or kw in name for kw in markers))


def _non_fat_whole_food(row: dict) -> bool:
    return (row.get("category") == "whole_food_fat" and
            float(row.get("fat_g") or 99) < 5)


def _whole_food_fat_nova4(row: dict) -> bool:
    return (row.get("category") == "whole_food_fat" and
            row.get("nova") == 4)


# ── Rule registry ─────────────────────────────────────────────────────────────

ANOMALY_RULES: list[dict] = [
    # ── CRITICAL ─────────────────────────────────────────────────────────────
    {
        "code": "NOVA1_FLOOR_MASKS_BEVERAGE",
        "severity": "CRITICAL",
        "description": "NOVA1 floor=85 overrides beverage calorie-density penalty — A grade is architecturally incorrect",
        "remediation": "Gate NOVA1 floor by routing category; beverages should not receive the whole-food floor",
        "test": _nova1_floor_masks_beverage,
    },
    {
        "code": "BEVERAGE_FROM_DAIRY_NAME",
        "severity": "CRITICAL",
        "description": "Dairy-named product (יוגורט/קפיר/לבן/חלב) routed to beverage archetype",
        "remediation": "Add v3 hard anchor: יוגורט/קפיר in name → dairy_protein unless explicit beverage container",
        "test": _beverage_from_dairy_name,
    },
    {
        "code": "INGREDIENT_CONTAMINATION_SAUCE",
        "severity": "CRITICAL",
        "description": "Dairy/cereal product routed to sauce_spread — ingredient-text contamination",
        "remediation": "Gate ingredient-text signals for routing; name-only anchor for known food types",
        "test": _ingredient_contamination_sauce,
    },
    # ── HIGH ──────────────────────────────────────────────────────────────────
    {
        "code": "VANILLA_NOVA4",
        "severity": "HIGH",
        "description": "Natural flavor (ואניל) falsely drives NOVA4 — Evolution #5 bug (natural vs artificial not split)",
        "remediation": "Gate 'ואניל' as natural_flavor with weight=0; only 'ונילין'/'חומרי טעם מלאכותיים' → +3",
        "test": _vanilla_nova4,
    },
    {
        "code": "NOVA1_CAP_CONFLICT",
        "severity": "HIGH",
        "description": "NOVA1 whole-food product capped by regulatory rule — floor/cap architectural tension",
        "remediation": "Consider archetype-specific sat_fat context note for intrinsic (not added) fat sources",
        "test": _nova1_cap_conflict,
    },
    {
        "code": "ROUTING_UNSTABLE",
        "severity": "HIGH",
        "description": "Category classifier instability flag set — competing signals produced uncertain routing",
        "remediation": "Inspect secondary_category and scope_basis; add explicit anchor or exclusion rule",
        "test": _routing_unstable,
    },
    {
        "code": "HIGH_CONF_LOW_SCORE",
        "severity": "HIGH",
        "description": "High-confidence evaluation with score < 50 — engine is certain this product is poor quality",
        "remediation": "Verify red labels and cap logic; may be correct behavior for heavily processed items",
        "test": _high_conf_low_score,
    },
    {
        "code": "INGREDIENT_CONTAMINATION_WHOLE_FOOD",
        "severity": "HIGH",
        "description": "Non-fat product (yogurt/cereal name) routed to whole_food_fat archetype",
        "remediation": "Ingredient-text or name contamination ('אגוזים'); add name-priority override",
        "test": _ingredient_contamination_whole_food,
    },
    # ── MEDIUM ────────────────────────────────────────────────────────────────
    {
        "code": "CAP_FLOOR_TENSION",
        "severity": "MEDIUM",
        "description": "Both a regulatory cap and a quality floor applied — opposing guardrails in tension",
        "remediation": "Review which guardrail is semantically dominant; Class B floor logic handles some cases",
        "test": _cap_floor_tension,
    },
    {
        "code": "DOUBLE_RED_LABEL",
        "severity": "MEDIUM",
        "description": "Two or more Israeli red labels → cap=45 (hard E-grade ceiling)",
        "remediation": "Verify label threshold correctness; check for combined sugar+sat_fat edge cases",
        "test": _double_red_label,
    },
    {
        "code": "SWEETENER_ONLY_NOVA4",
        "severity": "MEDIUM",
        "description": "Sweetener alone drives NOVA4 — product otherwise has minimal processing signal",
        "remediation": "Consider sweetener-specific cap path separate from full NOVA4 cascade",
        "test": _sweetener_only_nova4,
    },
    {
        "code": "NON_FAT_WHOLE_FOOD",
        "severity": "MEDIUM",
        "description": "Low-fat (<5g) product routed to whole_food_fat archetype",
        "remediation": "Fat content threshold check should gate whole_food_fat archetype assignment",
        "test": _non_fat_whole_food,
    },
    {
        "code": "WHOLE_FOOD_FAT_NOVA4",
        "severity": "MEDIUM",
        "description": "whole_food_fat archetype assigned to a NOVA4 ultra-processed product — contradictory routing",
        "remediation": "Category classifier should gate whole_food_fat on nova_proxy ≤ 3; or downgrade confidence when NOVA4 fires",
        "test": _whole_food_fat_nova4,
    },
    # ── LOW ───────────────────────────────────────────────────────────────────
    {
        "code": "PLANT_DAIRY_CONFUSION",
        "severity": "LOW",
        "description": "Plant-based product (soy/almond/coconut/oat) likely mislabeled as dairy_protein archetype",
        "remediation": "Add plant-based gate to yogurt_system/dairy archetype (no is_plant_based flag in BSIP1 yet)",
        "test": _plant_dairy_confusion,
    },
]


# ── Public API ────────────────────────────────────────────────────────────────

def detect_anomalies(row: dict) -> list[dict]:
    """Returns list of triggered anomaly dicts sorted by severity."""
    results = []
    for rule in ANOMALY_RULES:
        try:
            if rule["test"](row):
                results.append({
                    "code":        rule["code"],
                    "severity":    rule["severity"],
                    "description": rule["description"],
                    "remediation": rule.get("remediation", ""),
                })
        except Exception:
            pass
    return sorted(results, key=lambda x: SEVERITY_ORDER.get(x["severity"], 99))


def build_anomaly_frame(df: pd.DataFrame) -> pd.DataFrame:
    """Apply detect_anomalies to every row; return flat anomaly DataFrame."""
    rows = []
    for _, r in df.iterrows():
        row_dict = r.to_dict()
        for a in detect_anomalies(row_dict):
            rows.append({
                "Severity":    a["severity"],
                "Code":        a["code"],
                "Product":     row_dict.get("name_he", ""),
                "Score":       row_dict.get("score"),
                "Grade":       row_dict.get("grade", "?"),
                "NOVA":        row_dict.get("nova"),
                "Archetype":   row_dict.get("category", ""),
                "Description": a["description"],
                "Remediation": a["remediation"],
            })
    if not rows:
        return pd.DataFrame()
    adf = pd.DataFrame(rows)
    adf["_sev_order"] = adf["Severity"].map(SEVERITY_ORDER)
    return adf.sort_values(["_sev_order", "Score"]).drop(columns=["_sev_order"]).reset_index(drop=True)


def severity_counts(df: pd.DataFrame) -> dict[str, int]:
    """Count total anomaly detections by severity across all products."""
    counts: dict[str, int] = {k: 0 for k in SEVERITY_ORDER}
    for _, r in df.iterrows():
        for a in detect_anomalies(r.to_dict()):
            counts[a["severity"]] = counts.get(a["severity"], 0) + 1
    return counts
