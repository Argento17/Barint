"""
EvidenceStudy — structured per-study record for the Bari Evidence Registry.

Purpose
-------
Every study that backs a scoring signal in either the food Evidence Registry
(BEV-### / EV-###) or the Supplement Evidence Registry (SUPP-EV-###) can
optionally carry a ``study_objects:`` block containing one or more
``EvidenceStudy`` instances.  The dataclass captures the seven quality
dimensions that matter for Bari's scoring use-case: what is claimed, whether
the experimental conditions match real-world use, how trustworthy the study is,
and where it lives.

Where it is used
----------------
- ``01_framework/governance/evidence_registry_v1.md`` — food findings (BEV-###)
- ``03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md`` — BSIP2 EV-###
- ``03_operations/supplement_engine/proto_v0/evidence_registry/supp_evidence_registry_v1.md``

How to fill it in
-----------------
See ``evidence_grading_sop_v1.md`` for plain-language grading instructions.

Governance
----------
- Research Agent authors study objects; Nutrition Agent co-signs tier assignments
  for any entry that is marked ``should_affect_score_now: true``.
- No ``EvidenceStudy`` block, by itself, creates a scoring rule.  Scoring rules
  are governed separately under BSIP2 / SIE methodology (D7 authority).
- This schema is tooling only.  Adding a study object to a registry entry does
  not change any published score.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


@dataclass
class EvidenceStudy:
    """One study that backs a registry claim.

    All fields are required when the object is authored.  Use the grading SOP
    (``evidence_grading_sop_v1.md``) to determine the correct value for each field.
    """

    claim: str
    """Plain-language statement of what the study claims.

    Use standardized vocabulary from the SOP claim-vocabulary table where
    possible (e.g. "triglyceride lowering", "blood pressure reduction",
    "fermentation produces SCFA", "emulsifier disrupts gut barrier").
    One sentence.  Do not embed effect sizes here — put them in ``notes``.
    """

    dose_realistic: bool
    """True if the study dose is at or below twice the typical label dose.

    "Typical label dose" means the serving size or daily dose printed on a
    real product in the relevant category.  If a study used 10× the label
    dose, mark False — the finding may not apply to what a consumer actually
    consumes.  For food studies where "dose" is not meaningful (e.g. a whole
    population dietary pattern study), mark True and note the reason.
    """

    population_direct: bool
    """True if the study population matches Israeli general-consumer baseline.

    The Israeli general-consumer baseline is healthy adults aged 18–65 without
    a diagnosed condition that the supplement or food is intended to treat.
    Mark False if the study was in: children, elderly (65+), diagnosed patients,
    athletes at elite training loads, or animal/cell models.  Always explain in
    ``notes`` when False.
    """

    rob_grade: Literal["low", "moderate", "high", "very_high"]
    """Risk of bias grade — how much the study design could distort the result.

    ``low``      — Randomized, pre-registered, blinded, adequate allocation
                   concealment, low dropout, plausible control arm.
    ``moderate`` — Mostly well-designed but one meaningful weakness (e.g.
                   open-label, short follow-up, modest sample).
    ``high``     — Observational or uncontrolled with meaningful confounders,
                   OR an RCT with major protocol deviations.
    ``very_high`` — Case series, self-report only, or industry-funded with no
                   independent replication.

    Use the evidence tier (below) as the outcome signal; use this field to
    explain WHY the tier is what it is.
    """

    evidence_tier: Literal["A", "B", "C", "D"]
    """Overall quality tier for THIS study.

    ``A`` — Strong: high-quality RCT or systematic review with consistent
             findings; mechanism well established.
    ``B`` — Moderate: reasonable RCT evidence or consistent observational
             findings; mechanism plausible; some conflicting results.
    ``C`` — Weak: small samples, short duration, animal/in-vitro only, or
             significant methodological issues.
    ``D`` — Insufficient: single low-quality study, purely theoretical,
             anecdotal, or no reliable human evidence.

    This field rates the study itself.  The registry entry's overall
    ``evidence_tier`` or ``evidence_strength`` field synthesises across all
    study objects in its ``study_objects:`` block.
    """

    source_doi: str
    """DOI for the study, or ``"internal:[doc-name]"`` for Bari research docs.

    Examples:
      ``"10.1093/ajcn/nqy048"``
      ``"internal:bsip2_evidence_registry_v1.md"``
      ``"PMID:30102092"``   (when a DOI is unavailable but PMID is known)

    Always run ``crossref.get_doi()`` on the DOI before using it — check
    ``is_retracted`` and ``update_types`` for integrity signals.
    """

    notes: str
    """Free text: caveats, conflicts of interest, applicability limits, or
    any context that makes this study different from the face value of its tier.

    Required content when applicable:
    - Industry funding or conflict of interest
    - Why ``dose_realistic`` or ``population_direct`` is False
    - Effect size or confidence interval if load-bearing
    - Retraction or correction status
    """
