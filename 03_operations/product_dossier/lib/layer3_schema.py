"""
layer3_schema.py — Layer 3 (derived) three-namespace model for the Product
Dossier compiler (PD-2 / TASK-610).

Per STF memo `2026-07-11_product-dossier-architecture.md` §3 R-C / §4:
  "Layer 3 splits into three disjoint namespaces, never blended, no
  cross-namespace composite number:
    - assessment -- what the PRODUCT is: score, grade, nutrition/ingredient/
      processing/additive dims, category performance. Source: BSIP2 traces
      ONLY.
    - data_quality (record_health) -- how good the RECORD is: completeness,
      evidence/identity/barcode confidence, image confidence. Source: PD
      compiler over Layers 1-2.
    - publication_record -- what Bari CURRENTLY publishes, verbatim: the
      served score/grade/copy, stamped with its run_id + trace hash, pending
      a Layer-4 calculation check that may say FAIL.
  Quality vs data-quality is enforced by TYPE, not convention: every metric
  declares axis: assessment | data_quality | publication_record; a metric
  reading inputs across namespaces fails the build; no overall_score field
  is permitted."

This module is the structural enforcement mechanism: `Metric` carries its
own axis + declared input-axis provenance; `Layer3.__post_init__` validates
every metric (namespace-membership match, cross-namespace input scan,
`overall_score` ban) and raises `NamespaceViolation` (a `DossierBuildError`
subclass) the instant any of those invariants is violated. There is no way
to construct a *valid* Layer3 object that violates R-C -- validation runs at
construction, not as an optional post-hoc lint.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .layer2_evidence import DossierBuildError

AXES = ("assessment", "data_quality", "publication_record")

# Axis-neutral input provenance tags a metric is always allowed to cite,
# regardless of its own axis -- these are Layers 1/2 (identity/evidence),
# never a Layer-3 namespace, so citing them can never be a cross-namespace
# read.
NEUTRAL_INPUT_TAGS = {"layer1_identity", "layer2_evidence", "served_json_verbatim", "bsip2_trace"}


class NamespaceViolation(DossierBuildError):
    """A Layer-3 structural invariant (axis declaration, cross-namespace
    input, or banned overall_score) was violated. Always fatal.
    """


@dataclass
class Metric:
    key: str
    axis: str                       # one of AXES -- required, no default
    value: Any
    derivation: str                 # honest label, e.g. "bsip2_trace", "published_json_as_record",
                                     # "layer2_coverage", "stub_pending_registry_join"
    inputs: List[str] = field(default_factory=list)   # provenance tags this metric actually reads
    note: Optional[str] = None

    def validate(self) -> None:
        if self.key == "overall_score" or self.key == "overall_quality":
            raise NamespaceViolation(
                f"metric key '{self.key}' is a banned composite field (memo §3 R-C / §4: "
                f"'no overall_score field is permitted')."
            )
        if self.axis not in AXES:
            raise NamespaceViolation(f"metric '{self.key}' declares axis={self.axis!r}, not one of {AXES}")
        other_axes = set(AXES) - {self.axis} - NEUTRAL_INPUT_TAGS
        crossed = [inp for inp in self.inputs if inp in other_axes]
        if crossed:
            raise NamespaceViolation(
                f"metric '{self.key}' (axis={self.axis}) reads cross-namespace input(s) {crossed} "
                f"-- a metric may only read its own axis plus neutral Layer-1/2 evidence "
                f"({sorted(NEUTRAL_INPUT_TAGS)}); this is the exact averaging risk R-C forbids."
            )


@dataclass
class Layer3:
    assessment: Dict[str, Metric] = field(default_factory=dict)
    data_quality: Dict[str, Metric] = field(default_factory=dict)
    publication_record: Dict[str, Metric] = field(default_factory=dict)

    def __post_init__(self) -> None:
        namespaces = {
            "assessment": self.assessment,
            "data_quality": self.data_quality,
            "publication_record": self.publication_record,
        }
        for ns_name, ns_dict in namespaces.items():
            if "overall_score" in ns_dict or "overall_quality" in ns_dict:
                raise NamespaceViolation(
                    f"namespace '{ns_name}' contains a banned composite key -- "
                    f"no overall_score field is permitted anywhere in Layer 3."
                )
            for key, metric in ns_dict.items():
                if metric.key != key:
                    raise NamespaceViolation(
                        f"metric stored under dict key '{key}' but Metric.key={metric.key!r} -- must match."
                    )
                if metric.axis != ns_name:
                    raise NamespaceViolation(
                        f"metric '{key}' stored under namespace '{ns_name}' but declares "
                        f"axis={metric.axis!r} -- namespace storage and axis declaration must agree."
                    )
                metric.validate()

    def to_dict(self) -> dict:
        def _ns(ns_dict: Dict[str, Metric]) -> dict:
            return {
                k: {
                    "value": m.value,
                    "axis": m.axis,
                    "derivation": m.derivation,
                    "inputs": m.inputs,
                    "note": m.note,
                }
                for k, m in ns_dict.items()
            }

        return {
            "assessment": _ns(self.assessment),
            "data_quality": _ns(self.data_quality),
            "publication_record": _ns(self.publication_record),
        }
