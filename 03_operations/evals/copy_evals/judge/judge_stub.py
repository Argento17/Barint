"""LLM-judge interface for Hebrew naturalness (Project Tom's Voice, TASK-374 / TASK-505).

This is a STUB on purpose. The naturalness judge may only become a gate after it is
CALIBRATED against owner-labeled examples with tracked TPR/TNR — see calibration.md
in this directory. Shipping an uncalibrated judge as a gate would be exactly the
failure mode this suite exists to prevent (an authority no one has measured).

Contract (when implemented):

    score_naturalness(text) -> {
        "score": float,        # 0.0 (translationese) .. 1.0 (native, natural Hebrew)
        "rationale": str,      # short Hebrew/English explanation naming the signals
    }

Determinism note: the implementation must pin model + prompt version, and every
prompt/model change re-runs calibration (TPR/TNR re-measured) before the judge
regains gate authority.

TASK-506 status (2026-07-04): a real, blind LLM judge IS implemented in
`judge/naturalness_judge.py` (pinned `claude-opus-4-8`, prompt_hash 3aa7928ff4167c4a)
and was calibrated against the owner labels — see `judge/calibration_record_v1.md`.
The acceptance bar (TPR>=0.80 AND TNR>=0.90) was **not** cleared (best v1.1:
TPR=0.452 @ TNR=0.900), so the judge stays ADVISORY and this stub stays
`NotImplementedError` — it is NOT wired into `run_evals.py`. Do not import
`naturalness_judge` as a gate until the owner resolves the provisional
partially_approved labels and signs off on a cleared calibration record.
"""
from __future__ import annotations


JUDGE_VERSION = "0.0-uncalibrated-stub"


def score_naturalness(text: str) -> dict:
    """Score Hebrew naturalness of consumer copy. NOT IMPLEMENTED — uncalibrated.

    Raises:
        NotImplementedError: always, until calibration per judge/calibration.md is
        complete (owner labels collected in labels_template.jsonl, TPR/TNR measured
        and above threshold, and the calibration record committed).
    """
    raise NotImplementedError(
        "The naturalness judge is not calibrated yet. Do NOT wire it as a gate. "
        "See 03_operations/evals/copy_evals/judge/calibration.md for the protocol: "
        "owner labels (labels_template.jsonl) -> blind judge run -> TPR/TNR vs "
        "thresholds -> committed calibration record. Until then, naturalness "
        "verdicts belong to the owner / C3 review, not to this function."
    )
