"""LLM naturalness judge for Bari Hebrew consumer copy (Project Tom's Voice, TASK-374 / TASK-506).

CALIBRATION ARTEFACT — NOT WIRED AS A GATE. This module implements the real LLM
judge described in judge/calibration.md. It may only gain gate authority AFTER a
committed calibration record shows measured TPR>=0.80 AND TNR>=0.90 and the owner
signs off (see judge/calibration_record_v1.md). `judge_stub.py` remains the
un-wired entry point that `run_evals.py` sees; this module is invoked only by the
calibration runner until then.

Real model calls: the judge shells out to the local `claude` CLI in headless
print mode against a PINNED strong Claude model. This reuses the environment's
existing Claude credential (no ANTHROPIC_API_KEY in env; no `anthropic` SDK
installed). The judge is BLIND — it never sees the owner labels at scoring time.

Windows Hebrew note: prompts (which contain Hebrew) are passed to the CLI over
STDIN as UTF-8 bytes, never as an argv string, to avoid the documented Windows
argv/console Hebrew corruption. Callers must read/write Hebrew via UTF-8 files,
never through `python -c` or the console.

Contract:
    score_naturalness(text) -> {"score": float 0..1, "rationale": str}
    score 1.0 = flowing native Hebrew, ready to publish as-is
    score 0.0 = stiff / translationese / needs an editorial rewrite
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys


def _resolve_claude() -> str:
    """Resolve the `claude` CLI executable, preferring the Windows .cmd shim."""
    if sys.platform == "win32":
        cand = os.path.join(
            os.environ.get("APPDATA", ""), "npm", "claude.cmd"
        )
        if os.path.exists(cand):
            return cand
        w = shutil.which("claude.cmd") or shutil.which("claude")
        if w:
            return w
    w = shutil.which("claude")
    if w:
        return w
    raise FileNotFoundError("`claude` CLI not found on PATH")


CLAUDE_EXE = _resolve_claude()

# --- PINNED judge identity (bump JUDGE_VERSION on ANY change to model or prompt) ---
JUDGE_VERSION = "1.1"  # best calibrated version (see calibration_record_v1.md); v1.2 regressed
PINNED_MODEL = "claude-opus-4-8"

# The pinned prompt. The judge sees ONLY the rubric + the single line to score —
# never the owner labels. The rubric is the one from the 2026-07-04 labeling
# session (judge/labeling_session_2026-07-04.md), stated as guidance, not hard
# regex rules — the whole point of an LLM judge is a holistic native-speaker call.
PROMPT_TEMPLATE = """You are the FINAL editorial gate for a demanding senior Hebrew editor at the consumer food-comparison brand בארי. You are handed ONE short Hebrew product line. Decide whether it is publish-perfect exactly as written, or whether this exacting editor would send it back for at least one revision pass.

Output a single score = your confidence that the editor would ship this line with ZERO edits:
- 0.85-1.0 : publish-perfect as-is. Confident, flowing, native editorial prose that INTERPRETS the product rather than listing data; clear subject; idiomatic; no house-style violations.
- 0.5-0.84 : basically fine but the editor would tweak something (a little stiff, a touch too plain, a minor flow issue).
- 0.0-0.49 : the editor sends it back — it needs a real revision pass before it can ship.

This editor is exacting and holds a strong house style. Push the score DOWN toward the 0.0-0.49 band whenever the line shows any of these — they each trigger a revision:
- Restates the nutritional numbers in prose: reciting grams / calories / percentages / mg that merely echo the data panel instead of interpreting what they mean. (A single number used in service of a point can be fine; a line that lists several numbers is not.)
- Em-dash (—) used as a structural crutch: several in one short line, or an em-dash standing in for a proper connector or full clause.
- Define-by-negation of the form "X, לא Y" ("X, not Y").
- Sodium written as "סודיום" or "סודים" instead of the correct "נתרן".
- Brand written as "ברי" instead of the correct "בארי".
- Calque / translationese / stiffness — reads translated or mechanical rather than natively written.
- A bare label, tag, or clipped fragment ("high protein, low calories") rather than a written sentence — too little to be a real description.
- Unclear or dangling reference (relational framing like "the previous one" with no clear anchor); non-idiomatic simile/metaphor.

Reserve the 0.85-1.0 band ONLY for lines that are genuinely ready to publish untouched. Most lines are not — do not give the benefit of the doubt. Judge the WHOLE line holistically (a single purposeful number or one em-dash inside otherwise flowing, interpretive prose need not sink it), but treat the triggers above as real defects, not stylistic taste.

Judge ONLY the Hebrew writing quality and publish-readiness — NOT factual correctness, NOT whether the information is complete.

TEXT TO SCORE (between the markers):
<<<BARI_TEXT
{text}
BARI_TEXT

Respond with ONLY a single minified JSON object and nothing else (no markdown, no code fence, no commentary):
{{"score": <number between 0 and 1>, "rationale": "<one short sentence naming the main signal you weighted>"}}"""


def prompt_hash() -> str:
    """Stable short hash of the pinned prompt template (part of the judge identity)."""
    return hashlib.sha256(PROMPT_TEMPLATE.encode("utf-8")).hexdigest()[:16]


def _extract_json(blob: str) -> dict:
    """Pull the JSON object out of the model's reply, tolerating stray fences."""
    s = blob.strip()
    s = re.sub(r"^```(?:json)?", "", s).strip()
    s = re.sub(r"```$", "", s).strip()
    m = re.search(r"\{.*\}", s, re.DOTALL)
    if not m:
        raise ValueError(f"no JSON object in judge reply: {blob[:200]!r}")
    return json.loads(m.group(0))


def score_naturalness(text: str, *, model: str = PINNED_MODEL, timeout: int = 150) -> dict:
    """Score one Hebrew line for naturalness via a real, blind LLM call.

    Returns {"score": float 0..1, "rationale": str}. Raises on transport/parse failure.
    """
    prompt = PROMPT_TEMPLATE.format(text=text)
    proc = subprocess.run(
        [CLAUDE_EXE, "-p", "--model", model, "--output-format", "json", "--max-turns", "1"],
        input=prompt.encode("utf-8"),
        capture_output=True,
        timeout=timeout,
    )
    out = proc.stdout.decode("utf-8", errors="replace")
    if not out.strip():
        raise RuntimeError(
            f"empty CLI output (rc={proc.returncode}); stderr="
            f"{proc.stderr.decode('utf-8', errors='replace')[:300]!r}"
        )
    envelope = json.loads(out)
    if envelope.get("is_error"):
        raise RuntimeError(f"CLI reported error: {envelope.get('result')!r}")
    data = _extract_json(str(envelope["result"]))
    score = float(data["score"])
    if not (0.0 <= score <= 1.0):
        raise ValueError(f"score out of range: {score}")
    return {"score": score, "rationale": str(data.get("rationale", ""))}


if __name__ == "__main__":
    # Manual smoke test (kept off the console for Hebrew safety — writes to a file).
    import sys

    sample = "חלב טבעי 4% ממחלבות רמת הגולן."
    r = score_naturalness(sample)
    sys.stdout.write(json.dumps({"score": r["score"]}) + "\n")
