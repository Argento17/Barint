#!/usr/bin/env python3
"""
P174 / Counterfactual explanation method — minimal-change-to-next-grade.
Pure read-over-traces explanation layer.
Changes no score, touches no engine path.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Grade Boundaries (from grade_boundary_policy_v1.json)
# ---------------------------------------------------------------------------
GRADE_BOUNDARIES = {"S": 90, "A": 80, "B": 65, "C": 50, "D": 35, "E": 0}
GRADE_ORDER = ["E", "D", "C", "B", "A", "S"]

# ---------------------------------------------------------------------------
# Constants / Thresholds
# ---------------------------------------------------------------------------
RED_LABEL_THRESHOLDS = {
    "sugar": 17.5,
    "sat_fat": 5.0,
    "sodium": 600.0,
}

DIMENSION_WEIGHTS = {
    "processing_quality": 0.15,
    "nutrient_density": 0.15,
    "calorie_density": 0.15,
    "glycemic_quality": 0.12,
    "protein_quality": 0.10,
    "additive_quality": 0.10,
    "satiety_support": 0.06,
    "fat_quality": 0.08,
    "regulatory_quality": 0.05,
    "whole_food_integrity": 0.04,
}

# Cliff/binary levers — minimal change is a discrete flip (engine: constants.py PROCESSING_PENALTIES)
CLIFF_LEVER_TARGETS = {
    "ingredient_count": 12,  # LONG_INGREDIENT_LIST: ingredients>12 → 4pt penalty
    "additive_marker_count": 4,  # ADDITIVE_MARKERS_5_PLUS cap cliff
}
CONTINUOUS_LEVERS = {"sugars_g", "sodium_mg"}
LEVER_FLOORS = {"sugars_g": 0.0, "sodium_mg": 0.0}
LEVER_PRECISION = {"sugars_g": 0.1, "sodium_mg": 1.0}


class CounterfactualEngine:
    def __init__(self, trace: dict[str, Any]):
        self.trace = trace
        self.barcode = trace.get("input_reference", {}).get("barcode")
        self.category = trace.get("category")
        self.current_score = trace.get("final_score_estimate", 0)
        self.current_grade = self._calculate_grade(self.current_score)
        self.next_grade = self._get_next_grade(self.current_grade)
        self.target_score = GRADE_BOUNDARIES.get(self.next_grade, 100)
        
        # Current L1 signals
        self.signals = trace.get("L1_observed_signals", {})
        self.l3 = trace.get("L3_inferred_classifications", {})
        
        # Current weights and scores
        self.dim_scores = trace.get("dimension_scores", {})
        self.weights = trace.get("dimension_weights", DIMENSION_WEIGHTS)
        self.binding_cap = trace.get("binding_cap")
        self.penalties = trace.get("penalties_applied", [])
        
    def _calculate_grade(self, score: float) -> str:
        for g in reversed(GRADE_ORDER):
            if score >= GRADE_BOUNDARIES[g]:
                return g
        return "E"

    def _get_next_grade(self, current: str) -> str | None:
        if current not in GRADE_ORDER:
            return None
        idx = GRADE_ORDER.index(current)
        if idx + 1 < len(GRADE_ORDER):
            return GRADE_ORDER[idx + 1]
        return None

    def evaluate_lever(self, lever: str, new_value: Any) -> float:
        """Estimate the new final score with a changed lever."""
        # This is a simplified simulation of the score engine.
        # It uses sensitivities derived from the trace or known formulas.
        
        # 1. Estimate new weighted dimension score
        new_weighted_score = self.trace.get("weighted_dimension_score", 0)
        
        # Sugar changes
        if lever == "sugars_g":
            old_sugar = self.signals.get("sugars_g", 0)
            # glycemic_quality sensitivity: 2.5 pts per g
            delta_sugar = new_value - old_sugar
            dim_delta = -delta_sugar * 2.5
            new_weighted_score += dim_delta * self.weights.get("glycemic_quality", 0.12)
            
            # regulatory_quality
            old_red = old_sugar >= RED_LABEL_THRESHOLDS["sugar"]
            new_red = new_value >= RED_LABEL_THRESHOLDS["sugar"]
            if old_red and not new_red:
                # 1 label -> 0 labels usually adds 35 pts to regulatory_quality
                new_weighted_score += 35 * self.weights.get("regulatory_quality", 0.05)
        
        # Sodium changes
        elif lever == "sodium_mg":
            # sodium usually doesn't affect dimension scores directly in many archetypes
            # but check for red label
            old_red = self.signals.get("sodium_mg", 0) >= RED_LABEL_THRESHOLDS["sodium"]
            new_red = new_value >= RED_LABEL_THRESHOLDS["sodium"]
            if old_red and not new_red:
                new_weighted_score += 35 * self.weights.get("regulatory_quality", 0.05)
                
        # 2. Estimate new binding cap
        new_cap = self.binding_cap
        if lever == "sugars_g":
            # If sugar was causing a cap, check if it's still there
            # e.g. SNACK_BAR_RED_SUGAR_LABEL (55)
            if new_value < RED_LABEL_THRESHOLDS["sugar"]:
                # Removing this cap. In a real engine we'd check all other caps.
                # Here we'll just check if the trace had this cap.
                fired_caps = [c["rule"] for c in self.trace.get("caps_applied", [])]
                if "SNACK_BAR_RED_SUGAR_LABEL" in fired_caps or "ISRAELI_RED_LABEL_1_SUGAR" in fired_caps:
                    # Potential cap lift. We need to find the NEXT strictest cap.
                    all_caps = [c["cap"] for c in self.trace.get("caps_considered", []) if c["rule"] not in ["SNACK_BAR_RED_SUGAR_LABEL", "ISRAELI_RED_LABEL_1_SUGAR"] and c.get("fired") or (c["rule"] == "NOVA_PROXY_4_ULTRA_PROCESSED" and self.l3.get("nova_proxy") == 4)]
                    new_cap = min(all_caps) if all_caps else None
        
        elif lever == "additive_marker_count":
            if new_value < 5 and self.l3.get("additive_marker_count", 0) >= 5:
                 fired_caps = [c["rule"] for c in self.trace.get("caps_applied", [])]
                 if "ADDITIVE_MARKERS_5_PLUS" in fired_caps:
                     all_caps = [c["cap"] for c in self.trace.get("caps_considered", []) if c["rule"] != "ADDITIVE_MARKERS_5_PLUS" and c.get("fired")]
                     new_cap = min(all_caps) if all_caps else None

        # 3. Estimate new penalties
        new_penalties = sum(p["amount"] for p in self.penalties)
        if lever == "ingredient_count":
             if new_value <= 12 and self.signals.get("ingredient_count", 0) > 12:
                 new_penalties -= 4 # LONG_INGREDIENT_LIST
        elif lever == "has_seed_oil":
             if not new_value and self.l3.get("has_seed_oil"):
                 new_penalties -= 3 # SEED_OIL_PRESENT
        
        # Resulting score
        base_score = new_weighted_score
        if new_cap is not None:
            base_score = min(base_score, new_cap)
        
        return base_score - new_penalties

    def _is_continuous_lever(self, lever: str) -> bool:
        return lever in CONTINUOUS_LEVERS

    def _is_cliff_lever(self, lever: str) -> bool:
        return lever in CLIFF_LEVER_TARGETS

    def _cliff_target(self, lever: str) -> Any:
        if lever == "has_seed_oil":
            return False
        return CLIFF_LEVER_TARGETS[lever]

    def _grade_flip_note(self, lever: str, target_value: Any, score: float) -> str:
        grade = self._calculate_grade(score)
        return (
            f"{lever}={target_value} → simulated score {score:.1f} ({grade}), "
            f"crosses {self.current_grade}→{self.next_grade} boundary at {self.target_score}"
        )

    def _solve_minimal_continuous(
        self,
        lever: str,
        evaluate_fn,
    ) -> float | None:
        """Find the largest (closest-to-current) value that crosses the next grade."""
        current = self._get_current(lever)
        if current is None:
            return None

        floor = LEVER_FLOORS[lever]
        precision = LEVER_PRECISION[lever]

        if evaluate_fn(lever, current) >= self.target_score:
            return None
        if evaluate_fn(lever, floor) < self.target_score:
            return None

        low, high = floor, float(current)
        while high - low > precision:
            mid = (low + high) / 2.0
            if evaluate_fn(lever, mid) >= self.target_score:
                low = mid
            else:
                high = mid

        if lever == "sugars_g":
            return round(low, 1)
        return round(low)

    def _build_continuous_lever_record(
        self,
        lever: str,
        target_value: float,
        evaluate_fn,
    ) -> dict[str, Any]:
        current = self._get_current(lever)
        score = evaluate_fn(lever, target_value)
        dim_map = {
            "sugars_g": "glycemic_quality, regulatory_quality, sugar_load_caps",
            "sodium_mg": "regulatory_quality",
        }
        return {
            "field": lever,
            "current_value": current,
            "target_value": target_value,
            "delta": round(target_value - current, 1),
            "dimension_affected": dim_map.get(lever, ""),
            "achievable": True,
            "note": self._grade_flip_note(lever, target_value, score),
        }

    def find_counterfactuals(self) -> list[dict[str, Any]]:
        if not self.next_grade:
            return []
            
        levers = []

        for lever in CONTINUOUS_LEVERS:
            current = self._get_current(lever)
            if current is None or current <= LEVER_FLOORS[lever]:
                continue
            target = self._solve_minimal_continuous(lever, self.evaluate_lever)
            if target is not None:
                levers.append(self._build_continuous_lever_record(lever, target, self.evaluate_lever))

        # Ingredient count cliff (LONG_INGREDIENT_LIST @ ingredients>12, constants.py)
        current_ing = self.signals.get("ingredient_count")
        if current_ing is not None and current_ing > CLIFF_LEVER_TARGETS["ingredient_count"]:
            cliff = CLIFF_LEVER_TARGETS["ingredient_count"]
            score = self.evaluate_lever("ingredient_count", cliff)
            if score >= self.target_score:
                levers.append({
                    "field": "ingredient_count",
                    "current_value": current_ing,
                    "target_value": cliff,
                    "delta": cliff - current_ing,
                    "dimension_affected": "processing_load_penalties",
                    "achievable": True,
                    "note": self._grade_flip_note("ingredient_count", cliff, score),
                })

        # Seed oil (binary)
        if self.l3.get("has_seed_oil"):
            score = self.evaluate_lever("has_seed_oil", False)
            if score >= self.target_score:
                levers.append({
                    "field": "has_seed_oil",
                    "current_value": True,
                    "target_value": False,
                    "delta": -1,
                    "dimension_affected": "fat_quality_penalties",
                    "achievable": True,
                    "note": self._grade_flip_note("has_seed_oil", False, score),
                })

        # Additive marker cliff
        current_add = self.l3.get("additive_marker_count", 0)
        if current_add >= 5:
            cliff = CLIFF_LEVER_TARGETS["additive_marker_count"]
            score = self.evaluate_lever("additive_marker_count", cliff)
            if score >= self.target_score:
                levers.append({
                    "field": "additive_marker_count",
                    "current_value": current_add,
                    "target_value": cliff,
                    "delta": cliff - current_add,
                    "dimension_affected": "processing_load_caps",
                    "achievable": True,
                    "note": self._grade_flip_note("additive_marker_count", cliff, score),
                })

        return sorted(levers, key=lambda x: abs(x["delta"]))

    def _fixed_lever_value(self, lever: str) -> Any:
        """Cliff/binary levers flip to their minimal target; continuous stays at current."""
        if self._is_cliff_lever(lever) or lever == "has_seed_oil":
            return self._cliff_target(lever)
        return self._get_current(lever)

    def _try_double_combo(self, fixed_lever: str, variable_lever: str) -> dict[str, Any] | None:
        fixed_value = self._fixed_lever_value(fixed_lever)
        fixed_current = self._get_current(fixed_lever)

        if self._is_continuous_lever(variable_lever):
            def evaluate_var(_lever: str, val: Any) -> float:
                return self._evaluate_double_lever(fixed_lever, fixed_value, variable_lever, val)

            target = self._solve_minimal_continuous(variable_lever, evaluate_var)
            if target is None:
                return None
            var_current = self._get_current(variable_lever)
            score = evaluate_var(variable_lever, target)
            return {
                "levers": [
                    {"field": fixed_lever, "current": fixed_current, "target": fixed_value},
                    {"field": variable_lever, "current": var_current, "target": target},
                ],
                "total_delta": abs(fixed_value - fixed_current) + abs(target - var_current),
                "achievable": True,
                "note": self._grade_flip_note(
                    f"{fixed_lever}+{variable_lever}",
                    f"{fixed_value}/{target}",
                    score,
                ),
            }

        var_value = self._fixed_lever_value(variable_lever)
        var_current = self._get_current(variable_lever)
        score = self._evaluate_double_lever(fixed_lever, fixed_value, variable_lever, var_value)
        if score < self.target_score:
            return None
        return {
            "levers": [
                {"field": fixed_lever, "current": fixed_current, "target": fixed_value},
                {"field": variable_lever, "current": var_current, "target": var_value},
            ],
            "total_delta": abs(fixed_value - fixed_current) + abs(var_value - var_current),
            "achievable": True,
            "note": self._grade_flip_note(
                f"{fixed_lever}+{variable_lever}",
                f"{fixed_value}/{var_value}",
                score,
            ),
        }

    def find_two_lever_counterfactuals(self, single_levers: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Find combinations of 2 levers that lift the score."""
        if not self.next_grade:
            return []

        combos = []
        available_levers = []
        if self.signals.get("sugars_g") is not None:
            available_levers.append("sugars_g")
        if self.signals.get("sodium_mg") is not None:
            available_levers.append("sodium_mg")
        if self.signals.get("ingredient_count", 0) > CLIFF_LEVER_TARGETS["ingredient_count"]:
            available_levers.append("ingredient_count")
        if self.l3.get("has_seed_oil"):
            available_levers.append("has_seed_oil")
        if self.l3.get("additive_marker_count", 0) >= 5:
            available_levers.append("additive_marker_count")

        for i in range(len(available_levers)):
            for j in range(i + 1, len(available_levers)):
                l1, l2 = available_levers[i], available_levers[j]
                for fixed, variable in [(l1, l2), (l2, l1)]:
                    combo = self._try_double_combo(fixed, variable)
                    if combo is not None:
                        combos.append(combo)

                # Both continuous: fix one at floor, solve minimal on the other
                if self._is_continuous_lever(l1) and self._is_continuous_lever(l2):
                    for fixed, variable in [(l1, l2), (l2, l1)]:
                        floor = LEVER_FLOORS[fixed]

                        def evaluate_at_floor(_lever: str, val: Any) -> float:
                            return self._evaluate_double_lever(fixed, floor, variable, val)

                        target = self._solve_minimal_continuous(variable, evaluate_at_floor)
                        if target is not None:
                            score = self._evaluate_double_lever(fixed, floor, variable, target)
                            combos.append({
                                "levers": [
                                    {"field": fixed, "current": self._get_current(fixed), "target": floor},
                                    {"field": variable, "current": self._get_current(variable), "target": target},
                                ],
                                "total_delta": abs(floor - self._get_current(fixed)) + abs(target - self._get_current(variable)),
                                "achievable": True,
                                "note": self._grade_flip_note(
                                    f"{fixed}+{variable}",
                                    f"{floor}/{target}",
                                    score,
                                ),
                            })

        # Deduplicate by lever targets
        seen: set[tuple] = set()
        unique: list[dict[str, Any]] = []
        for combo in sorted(combos, key=lambda x: x["total_delta"]):
            key = tuple(sorted((lev["field"], lev["target"]) for lev in combo["levers"]))
            if key not in seen:
                seen.add(key)
                unique.append(combo)
        return unique

    def _get_current(self, lever: str) -> Any:
        if lever == "sugars_g": return self.signals.get("sugars_g", 0)
        if lever == "sodium_mg": return self.signals.get("sodium_mg", 0)
        if lever == "ingredient_count": return self.signals.get("ingredient_count", 0)
        if lever == "has_seed_oil": return self.l3.get("has_seed_oil", False)
        if lever == "additive_marker_count": return self.l3.get("additive_marker_count", 0)
        return None

    def _evaluate_double_lever(self, l1: str, v1: Any, l2: str, v2: Any) -> float:
        # Simplified: apply both changes sequentially
        # This isn't perfectly accurate if they interact, but good enough for counterfactuals
        
        # 1. Start with weighted score
        new_weighted_score = self.trace.get("weighted_dimension_score", 0)
        
        # Apply changes to dimension score
        for l, v in [(l1, v1), (l2, v2)]:
            if l == "sugars_g":
                delta = v - self.signals.get("sugars_g", 0)
                new_weighted_score += -delta * 2.5 * self.weights.get("glycemic_quality", 0.12)
                # Regulatory
                if self.signals.get("sugars_g", 0) >= 17.5 and v < 17.5:
                    new_weighted_score += 35 * self.weights.get("regulatory_quality", 0.05)
            elif l == "sodium_mg":
                if self.signals.get("sodium_mg", 0) >= 600 and v < 600:
                    new_weighted_score += 35 * self.weights.get("regulatory_quality", 0.05)
        
        # 2. Binding Cap
        # Identify if either change lifts the binding cap
        new_cap = self.binding_cap
        fired_caps = [c["rule"] for c in self.trace.get("caps_applied", [])]
        
        can_lift_sugar_cap = (l1 == "sugars_g" and v1 < 17.5) or (l2 == "sugars_g" and v2 < 17.5)
        can_lift_add_cap = (l1 == "additive_marker_count" and v1 < 5) or (l2 == "additive_marker_count" and v2 < 5)
        
        active_caps = []
        for c in self.trace.get("caps_considered", []):
            is_fired = c.get("fired")
            if c["rule"] in ["SNACK_BAR_RED_SUGAR_LABEL", "ISRAELI_RED_LABEL_1_SUGAR"] and can_lift_sugar_cap:
                is_fired = False
            if c["rule"] == "ADDITIVE_MARKERS_5_PLUS" and can_lift_add_cap:
                is_fired = False
            # NOVA4 cap is usually not lifted by these levers
            if is_fired:
                active_caps.append(c["cap"])
        
        if active_caps:
            new_cap = min(active_caps)
        else:
            new_cap = None
            
        # 3. Penalties
        new_penalties = sum(p["amount"] for p in self.penalties)
        for l, v in [(l1, v1), (l2, v2)]:
            if l == "ingredient_count" and v <= 12 and self.signals.get("ingredient_count", 0) > 12:
                new_penalties -= 4
            if l == "has_seed_oil" and not v and self.l3.get("has_seed_oil"):
                new_penalties -= 3
                
        base_score = new_weighted_score
        if new_cap is not None:
            base_score = min(base_score, new_cap)
            
        return base_score - new_penalties

    def get_report_record(self) -> dict[str, Any]:
        single_levers = self.find_counterfactuals()
        two_lever_combos = []
        if not single_levers:
            two_lever_combos = self.find_two_lever_counterfactuals(single_levers)
            
        return {
            "barcode": self.barcode,
            "shelf": self.category,
            "current_score": self.current_score,
            "current_grade": self.current_grade,
            "next_grade": self.next_grade,
            "levers": single_levers if single_levers else two_lever_combos,
            "lever_type": "single" if single_levers else ("double" if two_lever_combos else "none"),
            "achievable": len(single_levers) > 0 or len(two_lever_combos) > 0,
            "note": "No single or double-lever improvement found" if not single_levers and not two_lever_combos else None
        }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--trace-dir", type=str, default="03_operations/bsip2/proto_v0/outputs/products")
    parser.add_argument("--output-json", type=str, default="03_operations/bsip2/proto_v0/reports/methods/counterfactual/sample.json")
    parser.add_argument("--output-md", type=str, default="03_operations/bsip2/proto_v0/reports/methods/counterfactual/sample.md")
    args = parser.parse_args()

    trace_dir = Path(args.trace_dir)
    output_json = Path(args.output_json)
    output_md = Path(args.output_md)
    
    output_json.parent.mkdir(parents=True, exist_ok=True)

    records = []
    processed_count = 0
    achievable_count = 0
    single_lever_count = 0
    two_lever_count = 0 # Not implemented but placeholder
    
    for product_dir in trace_dir.iterdir():
        if not product_dir.is_dir():
            continue
        trace_path = product_dir / "bsip2_trace.json"
        if not trace_path.exists():
            continue
            
        with open(trace_path, "r", encoding="utf-8") as f:
            try:
                trace = json.load(f)
            except Exception:
                continue
                
        engine = CounterfactualEngine(trace)
        record = engine.get_report_record()
        records.append(record)
        
        processed_count += 1
        if record["achievable"]:
            achievable_count += 1
            if record["lever_type"] == "single":
                single_lever_count += 1
            elif record["lever_type"] == "double":
                two_lever_count += 1

    # Write JSON
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)
        
    # Write MD
    with open(output_md, "w", encoding="utf-8") as f:
        f.write("# Counterfactual Analysis Report\n\n")
        f.write(f"Generated at: {datetime.now(timezone.utc).isoformat()}\n\n")
        f.write(f"- **Products Processed**: {processed_count}\n")
        f.write(f"- **Achievable Improvements**: {achievable_count}\n")
        f.write(f"- **Single-Lever Counterfactuals**: {single_lever_count}\n")
        f.write(f"- **Two-Lever Counterfactuals**: {two_lever_count}\n")
        f.write(f"- **Achievable False**: {processed_count - achievable_count}\n\n")
        
        f.write("## Sample Results\n\n")
        f.write("| Barcode | Current Grade | Next Grade | Lever Type | Details |\n")
        f.write("| --- | --- | --- | --- | --- |\n")
        for r in records[:50]:
            if r["achievable"]:
                if r["lever_type"] == "single":
                    l = r["levers"][0]
                    f.write(f"| {r['barcode']} | {r['current_grade']} | {r['next_grade']} | Single | {l['field']} ({l['delta']}) |\n")
                else:
                    l = r["levers"][0]
                    details = ", ".join([f"{lev['field']} (→{lev['target']})" for lev in l["levers"]])
                    f.write(f"| {r['barcode']} | {r['current_grade']} | {r['next_grade']} | Double | {details} |\n")
            else:
                f.write(f"| {r['barcode']} | {r['current_grade']} | {r['next_grade']} | N/A | N/A |\n")

    print(f"Report written to {output_json} and {output_md}")
    print(f"Processed {processed_count} products. {achievable_count} achievable.")

if __name__ == "__main__":
    main()
