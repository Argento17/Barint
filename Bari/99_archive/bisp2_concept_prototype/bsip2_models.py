"""
Data models for BSIP2 v0.3.1
"""
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Callable
import hashlib
import json
import datetime


# ---------------------------------------------------------------------------
# Input wrapper
# ---------------------------------------------------------------------------
@dataclass
class FoodProduct:
    raw: Dict[str, Any]

    def get(self, key: str, default=None):
        value = self.raw.get(key, default)
        if value == "" or value is None or str(value).lower() in ["nan", "none", "null"]:
            return default
        return value

    def num(self, key: str, default: Optional[float] = None) -> Optional[float]:
        try:
            value = self.get(key, None)
            if value is None:
                return default
            if isinstance(value, str):
                value = value.replace("<", "").replace(",", ".").strip()
            return float(value)
        except Exception:
            return default

    def text(self, key: str) -> str:
        return str(self.get(key, "") or "")

    def boolish(self, key: str) -> Optional[bool]:
        value = self.get(key, None)
        if value is None:
            return None
        if isinstance(value, bool):
            return value
        v = str(value).strip().lower()
        if v in ["true", "yes", "1", "y", "כן", "אמת"]:
            return True
        if v in ["false", "no", "0", "n", "לא", "שקר"]:
            return False
        return None

    def input_hash(self) -> str:
        payload = json.dumps(self.raw, sort_keys=True, ensure_ascii=False, default=str)
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:12]


# ---------------------------------------------------------------------------
# Dimension scores
# ---------------------------------------------------------------------------
@dataclass
class DimensionScores:
    nutrient_density: float = 50
    processing_quality: float = 50
    protein_quality: float = 50
    glycemic_quality: float = 50
    fat_quality: float = 50
    additive_quality: float = 50
    satiety_support: float = 50
    regulatory_quality: float = 50
    whole_food_integrity: float = 50
    calorie_density_quality: float = 50
    confidence: float = 70


# ---------------------------------------------------------------------------
# Rule engine objects
# ---------------------------------------------------------------------------
@dataclass
class TriggeredRule:
    rule_id: str
    rule_type: str  # "veto" | "cap" | "penalty" | "floor"
    value: float
    rationale: str
    framework_ref: Optional[str] = None
    family: str = "general"


@dataclass
class GuardrailResult:
    veto: Optional[TriggeredRule] = None
    caps: List[TriggeredRule] = field(default_factory=list)
    penalties: List[TriggeredRule] = field(default_factory=list)
    floors: List[TriggeredRule] = field(default_factory=list)

    @property
    def lowest_cap(self) -> Optional[TriggeredRule]:
        return min(self.caps, key=lambda r: r.value) if self.caps else None

    @property
    def total_penalty(self) -> float:
        return sum(r.value for r in self.penalties)

    @property
    def highest_floor(self) -> Optional[TriggeredRule]:
        return max(self.floors, key=lambda r: r.value) if self.floors else None


# ---------------------------------------------------------------------------
# Rule (used in static rule catalog)
# ---------------------------------------------------------------------------
@dataclass
class Rule:
    rule_id: str
    rule_type: str
    condition: Callable[[Dict[str, Any]], bool]
    value: float
    rationale: str
    framework_ref: Optional[str] = None
    family: str = "general"
    tags: List[str] = field(default_factory=list)

    def evaluate(self, features: Dict[str, Any]) -> Optional[TriggeredRule]:
        try:
            if self.condition(features):
                return TriggeredRule(
                    rule_id=self.rule_id,
                    rule_type=self.rule_type,
                    value=self.value,
                    rationale=self.rationale,
                    framework_ref=self.framework_ref,
                    family=self.family,
                )
        except (KeyError, TypeError):
            return None
        return None


# ---------------------------------------------------------------------------
# Scoring trace
# ---------------------------------------------------------------------------
@dataclass
class TraceStep:
    step: str
    rule_id: Optional[str]
    before: float
    after: float
    delta: float
    rationale: str


@dataclass
class ScoringTrace:
    base_score: float
    steps: List[TraceStep] = field(default_factory=list)
    final_score: float = 0.0

    def add(self, step: str, rule_id: Optional[str], before: float, after: float, rationale: str):
        self.steps.append(TraceStep(
            step=step, rule_id=rule_id,
            before=round(before, 2), after=round(after, 2),
            delta=round(after - before, 2), rationale=rationale,
        ))


# ---------------------------------------------------------------------------
# Final assessment
# ---------------------------------------------------------------------------
@dataclass
class FoodAssessment:
    barcode: str
    product_name: str
    inferred_category: str
    base_score: float
    final_score: float
    grade: str
    confidence: float
    confidence_band: str
    dimensions: Dict[str, float]
    guardrails: Dict[str, Any]
    reasons_positive: List[str]
    reasons_negative: List[str]
    reason_codes: List[str]
    triggered_rule_ids: List[str]
    calorie_reason_codes: List[str]
    calorie_caps_triggered: List[str]
    calorie_penalties_triggered: List[str]
    hyper_palatability_score: float
    hyper_palatability_combos: List[str]
    hyper_palatability_near_miss: List[str]
    family_penalties_applied: Dict[str, float]
    family_caps_applied: Dict[str, float]
    concern_audit: Dict[str, Any]
    trace: List[Dict[str, Any]]
    algorithm_version: str
    input_hash: str
    computed_at: str


def utc_now_iso() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")