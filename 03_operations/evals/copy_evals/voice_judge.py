#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""voice_judge.py — the calibrated VOICE / ALTITUDE judge for Bari consumer copy
(TASK-576).

WHAT THIS IS
------------
The hard gates in `copy_rules.py` catch MECHANICAL defects (cited nutrition
values, grade-in-prose, define-by-negation, em-dash). They are blind to the
SEMANTIC defect that took the owner four rounds to correct: copy that *recites
the nutrition profile* — with numbers OR as corpus-ranked analyst-speak —
instead of *describing the food*. Only the owner or an LLM judge can see that.

This module is that LLM judge. It scores ONE Hebrew consumer line 0-100 against
the owner's approved 3-beat voice (his §H5 anchor, 2026-07-10) and returns
PASS / FAIL + a reason. It COMPLEMENTS the hard gates; it does not replace them
and it never looks at numbers/grammar/leakage (those are the deterministic
gates' job). It only judges VOICE ALTITUDE: describe-the-food vs recite-the-panel.

THE RUBRIC (owner's approved voice — 3 beats, §H5)
--------------------------------------------------
A GOOD line:
  (1) leads with IDENTITY + sensory character (what the food is, how it eats);
  (2) gives the nutritional read in PLAIN ABSOLUTE words (high protein, high
      fat, salty, lean) — NOT numbers, NOT corpus-rank ("among the highest in
      the review");
  (3) lands a practical TAKEAWAY (who it's for / when / the catch).
  It DESCRIBES the food.
A BAD line recites the nutrition panel (numbers OR ranked analyst-speak) with
no real description of the product.

Owner gold anchor (גאודה מאסדם, §H5):
  גאודה הולנדית קלאסית, עשירה ומלוחה. היא מכילה חלבון גבוה אך גם שומן גבוה.
  מדובר במוצר יחסית נקי אבל יש לשים לב לכמות הנצרכת.

MECHANISM (Windows-safe headless `claude`, pattern proven in
author_copy_llm.py / local_scan.py)
------------------------------------------------------------------------------
The judge shells out to the already-logged-in `claude` CLI in headless print
mode (`-p`) against a pinned strong Claude model. No ANTHROPIC_API_KEY, no
`anthropic` SDK, no paid service — the user's existing subscription.

The proven Windows subprocess discipline is copied verbatim from
author_copy_llm._run_claude:
  * the prompt (which contains Hebrew) is fed via a FILE HANDLE as stdin — NOT
    communicate(input=...) — because the cmd/c -> claude.cmd -> node hop hits
    the Windows ~64KB pipe buffer and deadlocks;
  * stdout/stderr stream to disk;
  * on timeout the whole process TREE is reaped with `taskkill /PID <pid> /T /F`
    (the node grandchild survives a plain terminate);
  * MCP is disabled with `--strict-mcp-config --mcp-config <empty>` so no MCP
    fleet boots per call.
The judge is BLIND — the prompt carries the rubric + a fixed set of gold
examples, never the owner's labels for the line under test.

Contract:
    score_line(text) -> {
        "verdict": "PASS" | "FAIL",
        "score": int 0..100,          # >= PASS_THRESHOLD  => PASS
        "describes_food": bool,       # beat (1) present?
        "recites_panel": bool,        # numbers OR analyst-speak rank?
        "reason": str                 # one short sentence
    }
    PASS  = describes the food in the owner's 3-beat voice.
    FAIL  = recites the nutrition profile without describing the product.

TRUST STATUS (be honest — a judge that passes everything is worse than none)
----------------------------------------------------------------------------
Measured on the owner's full labeled calibration set (N=51 held-out; embedded
few-shot excluded) via voice_judge_validate.py, 2026-07-10:
  * RECALL on catching the owner's REJECTIONS = 1.000 (35/35). It caught EVERY
    rejected line — all 19 v2 lines that cite numbers AND all 16 v3 lines that
    recite the profile as corpus-ranked analyst-speak with NO numbers. This is
    the hard case (v3 negatives vs v5 positives are number-free and, on some
    products, differ only by a sensory adjective) and the judge still separated
    them. This is the semantic defect the deterministic gates cannot see.
  * PRECISION = 0.87-0.91 (stochastic run-to-run). accuracy ~0.90.
  * KNOWN FAILURE MODE — over-strict on POSITIVES: the 3-5 false positives are
    all v5-approved lines that establish IDENTITY via ingredient composition
    ("שקדים (18%) וחמוציות אמיתיות...", "קוקיס שוקולד לבן (כ-20%)...") rather
    than a sensory adjective. The judge under-credits the "identity+sensory
    character" beat for ingredient-led descriptions (concentrated on the
    cookies shelf) — ~69-81% of positives pass.
  * VERDICT: trustworthy as an ADVISORY flag-for-human-review, NOT an auto-block.
    It errs on the SAFE side for a complement to the hard gates (never lets a
    recite-the-panel line through; occasionally over-flags a good ingredient-led
    line). Tightening precision needs more owner-approved ingredient-led
    positives in the calibration set. Do NOT wire it as a hard blocking gate on
    this evidence.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# --- PINNED judge identity (bump on ANY change to model or prompt) -----------
JUDGE_VERSION = "voice-1.0"
# MEASURED model (voice_judge_validate.py, full labeled set, N=51, 2026-07-10):
#   recall(catch rejections) = 1.000  (35/35: all 19 v2-number + all 16 v3
#   analyst-speak rejections caught), accuracy = 0.90, precision = 0.87-0.91
#   (stochastic across runs). recall is the rock-solid property; precision is
#   the soft spot (false positives on ingredient-led positives, see docstring).
#   opus-4-8 is available via --model but is NOT independently validated here.
PINNED_MODEL = "claude-sonnet-4-6"
PASS_THRESHOLD = 60                # score >= this => PASS
CLAUDE_TIMEOUT = 180               # seconds per single-line call

# The owner's §H5 gold anchor and a small, FIXED set of approved/rejected
# contrasts. These are the same products across positive/negative so the model
# is forced to separate VOICE, not topic. Kept deliberately small (well under
# 64KB) — this is a few-shot rubric, not the whole calibration set.
_PROMPT_TEMPLATE = """אתה עורך בכיר וקפדן במותג בארי — אתר השוואת מזון בעברית. תפקידך כאן צר וממוקד: לשפוט את ה"גובה" / הקול של שורת תיאור מוצר אחת. אתה לא בודק דקדוק, לא מספרים, לא נכונות עובדתית — רק האם השורה מְתָארֶת את המזון בקול המאושר, או מְדַקְלֶמֶת את פרופיל הערכים התזונתיים.

## הכלל (הקול שהבעלים אישר — 3 פעימות)
שורה טובה:
  (1) פותחת בזהות + אופי חושי — מה המוצר, איך הוא נאכל (למשל: "גאודה הולנדית קלאסית, עשירה ומלוחה", "גבינה איטלקית קשה וחריפה").
  (2) נותנת את הקריאה התזונתית במילים פשוטות ומוחלטות — "חלבון גבוה", "שומן גבוה", "מלוח", "רזה" — לא מספרים, ולא דירוג-קורפוס בסגנון אנליסט ("מהגבוהים בין הגאודות המלאות בסקירה", "מהעשירות שנבדקו במדף").
  (3) נוחתת על תובנה מעשית / הסתייגות — למי זה מתאים, מתי, מה הקאץ'.
  היא מְתָארֶת את המזון.
שורה גרועה מְדַקְלֶמֶת את פרופיל הערכים — עם מספרים (גרם/מ"ג/קלוריות/אחוזים) או כדירוג-קורפוס בסגנון אנליסט ("מהגבוהים בסקירה", "בין הגבוהות במדף") — בלי לתאר את המוצר עצמו. שורה שהיא רק קריאה תזונתית, בלי זהות ואופי של המזון, נכשלת גם אם אין בה מספרים.

## הזהב (הבעלים כתב את השורה הזו בעצמו — זה בדיוק הקול הנדרש)
"גאודה הולנדית קלאסית, עשירה ומלוחה. היא מכילה חלבון גבוה אך גם שומן גבוה. מדובר במוצר יחסית נקי אבל יש לשים לב לכמות הנצרכת."
→ PASS. זהות+אופי ("קלאסית, עשירה ומלוחה"), קריאה תזונתית פשוטה ("חלבון גבוה... שומן גבוה"), תובנה מעשית ("יש לשים לב לכמות הנצרכת").

## דוגמאות מאושרות (PASS)
- "גבינת גאודה גוסטו 30%, גבינה עשירה וטעימה. חלבון גבוה לצד שומן גבוה, כמצופה מגבינה בדרגת שומן זו." → PASS (זהות+אופי, קריאה פשוטה מוחלטת).
- "גרנה פדנו מגורדת, גבינה איטלקית קשה וחריפה בטעמה. החלבון בה גבוה מאוד והשומן מתון יחסית לגבינה מסוג זה." → PASS.

## דוגמאות שנדחו (FAIL) — אותם מוצרים בדיוק, קול שגוי
- "גאודה מאסדם אמנטל הולנדי: 26 גרם חלבון, נתרן 660 מיליגרם, רשימת רכיבים שלא הגיעה מהסריקה." → FAIL (דקלום מספרים מפאנל הערכים; אין תיאור מזון).
- "גאודה הולנדית עם חלבון מהגבוהים בין הגאודות המלאות בסקירה, לצד נתרן שגם הוא מהגבוהים במדף." → FAIL (אין מספרים, אבל זו קריאה תזונתית כדירוג-קורפוס בסגנון אנליסט — "מהגבוהים... בסקירה", "במדף" — בלי זהות ואופי חושי של המזון).
- "גבינת גאודה גוסטו 30%, עם חלבון גבוה יחסית לגאודות אחרות באותה דרגת שומן, לצד נתרן שגם הוא מהגבוהים במדף." → FAIL (הזהות שטחית, הגוף כולו הוא דירוג-קורפוס יחסי; לא מְתָאר את המזון).

## ההבחנה הקשה
ההבדל בין מאושר לנדחה הוא לרוב עדין: שתי השורות עשויות להיות בלי מספרים. השאלה המכרעת — האם השורה מוסיפה זהות ואופי חושי של המזון ונותנת קריאה תזונתית פשוטה-מוחלטת (PASS), או שהיא בעיקר מיקום/דירוג יחסי של המוצר במדף/בסקירה (FAIL). מותר להזכיר סופרלטיב מאומת ("הנתרן הגבוה ביותר מכל הגבינות הקשות בסקירה") — אבל רק אם השורה גם פותחת בזהות+אופי ("עשירה ומלוחה") ובאמת מְתָארֶת. אם הדירוג היחסי הוא כל הגוף, זה FAIL.

## השורה לשיפוט (בין הסימונים)
<<<BARI_LINE
{text}
BARI_LINE

החזר אך ורק אובייקט JSON אחד מוקטן, בלי markdown, בלי code fence, בלי הערות:
{{"score": <מספר שלם 0-100, ביטחון שהבעלים היה מקבל את הקול הזה>, "verdict": "PASS" או "FAIL", "describes_food": <true/false — האם יש פעימת זהות+אופי חושי>, "recites_panel": <true/false — האם הגוף הוא דקלום מספרים או דירוג-קורפוס>, "reason": "<משפט קצר אחד בעברית שמנמק את השיפוט>"}}"""


class VoiceJudgeError(RuntimeError):
    """Raised when the headless-claude call cannot produce a usable verdict."""


def prompt_hash() -> str:
    import hashlib
    return hashlib.sha256(_PROMPT_TEMPLATE.encode("utf-8")).hexdigest()[:16]


def _kill_tree(pid: int) -> None:
    """Kill a process and all its children (author_copy_llm._kill_tree pattern).
    On Windows `cmd /c claude` spawns a node grandchild that survives a plain
    terminate; taskkill /T /F reaps the whole tree. Best-effort, never raises."""
    try:
        if os.name == "nt":
            subprocess.run(["taskkill", "/PID", str(pid), "/T", "/F"],
                           capture_output=True, timeout=30)
        else:
            import signal
            os.killpg(os.getpgid(pid), signal.SIGKILL)
    except Exception:
        pass


def _run_claude(prompt: str, model: str, timeout: int) -> str:
    """Run one headless-claude call and return raw stdout text.

    File-handle stdin + stream-to-disk + taskkill-on-timeout, copied from
    author_copy_llm._run_claude (the only pattern proven not to deadlock on the
    Windows cmd/c -> claude.cmd -> node hop with a Hebrew prompt)."""
    workdir = Path(tempfile.mkdtemp(prefix="voice_judge_"))
    mcp_cfg = workdir / "empty_mcp.json"
    mcp_cfg.write_text('{"mcpServers":{}}', encoding="utf-8")
    pf_path = workdir / "prompt.txt"
    so_path = workdir / "stdout.txt"
    se_path = workdir / "stderr.txt"
    pf_path.write_text(prompt, encoding="utf-8")

    flags = [
        "-p",
        "--output-format", "json",
        "--model", model,
        "--max-turns", "1",
        "--strict-mcp-config", "--mcp-config", str(mcp_cfg),
    ]
    cmd = (["cmd", "/c", "claude"] + flags) if os.name == "nt" else (["claude"] + flags)

    proc = None
    try:
        with pf_path.open("r", encoding="utf-8") as stdin_f, \
             so_path.open("w", encoding="utf-8", errors="replace") as so, \
             se_path.open("w", encoding="utf-8", errors="replace") as se:
            proc = subprocess.Popen(
                cmd, stdin=stdin_f, stdout=so, stderr=se,
                text=True, encoding="utf-8", errors="replace",
            )
            try:
                proc.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                _kill_tree(proc.pid)
                try:
                    proc.wait(timeout=30)
                except Exception:
                    pass
                raise VoiceJudgeError(f"claude timed out after {timeout}s (pid={proc.pid})")
    except VoiceJudgeError:
        raise
    except Exception as exc:
        if proc is not None:
            _kill_tree(proc.pid)
        raise VoiceJudgeError(f"claude subprocess error: {exc!r}") from exc

    out = so_path.read_text(encoding="utf-8", errors="replace")
    if not out.strip():
        tail = se_path.read_text(encoding="utf-8", errors="replace").strip()[-300:]
        raise VoiceJudgeError(f"empty CLI output (rc={proc.returncode}); stderr={tail!r}")
    return out


def _salvage_fields(blob: str) -> dict:
    """Regex-salvage the structured fields when the model emits invalid JSON
    (most commonly an unescaped double-quote inside the Hebrew `reason`, which
    breaks json.loads). The verdict/score are the load-bearing outputs; a
    mangled `reason` must not discard an otherwise-correct judgment."""
    score_m = re.search(r'"score"\s*:\s*(\d{1,3})', blob)
    verdict_m = re.search(r'"verdict"\s*:\s*"?(PASS|FAIL)"?', blob, re.IGNORECASE)
    if not (score_m or verdict_m):
        raise VoiceJudgeError(f"no salvageable score/verdict in reply: {blob[:200]!r}")

    def _bool(field: str) -> bool:
        bm = re.search(rf'"{field}"\s*:\s*(true|false)', blob, re.IGNORECASE)
        return bool(bm) and bm.group(1).lower() == "true"

    return {
        "score": int(score_m.group(1)) if score_m else None,
        "verdict": verdict_m.group(1).upper() if verdict_m else "",
        "describes_food": _bool("describes_food"),
        "recites_panel": _bool("recites_panel"),
        "reason": "(reason unparsed: model emitted invalid JSON)",
        "_salvaged": True,
    }


def _extract_inner_json(result_text: str) -> dict:
    """Pull the judge's JSON verdict out of the model reply, tolerating fences.
    Falls back to a regex salvage of the structured fields if the reply is not
    valid JSON (an unescaped quote in the Hebrew `reason` is the usual culprit)."""
    s = result_text.strip()
    s = re.sub(r"^```(?:json)?", "", s).strip()
    s = re.sub(r"```$", "", s).strip()
    m = re.search(r"\{.*\}", s, re.DOTALL)
    if not m:
        raise VoiceJudgeError(f"no JSON object in judge reply: {result_text[:200]!r}")
    try:
        return json.loads(m.group(0))
    except json.JSONDecodeError:
        return _salvage_fields(m.group(0))


def score_line(text: str, *, model: str = PINNED_MODEL,
               timeout: int = CLAUDE_TIMEOUT) -> dict:
    """Score one Hebrew consumer line for voice/altitude via a blind LLM call.

    Returns {"verdict","score","describes_food","recites_panel","reason"}.
    Raises VoiceJudgeError on transport/parse failure."""
    prompt = _PROMPT_TEMPLATE.format(text=text)
    raw = _run_claude(prompt, model=model, timeout=timeout)

    # `--output-format json` wraps the model text in an envelope with a "result".
    try:
        envelope = json.loads(raw)
    except json.JSONDecodeError:
        # Defensive: if the envelope isn't clean JSON, treat the whole thing as text.
        envelope = {"result": raw, "is_error": False}
    if isinstance(envelope, dict) and envelope.get("is_error"):
        raise VoiceJudgeError(f"CLI reported error: {envelope.get('result')!r}")
    result_text = str(envelope["result"]) if isinstance(envelope, dict) and "result" in envelope else raw

    data = _extract_inner_json(result_text)
    verdict = str(data.get("verdict", "")).upper().strip()
    raw_score = data.get("score", None)
    if raw_score is None:
        if verdict not in ("PASS", "FAIL"):
            raise VoiceJudgeError(f"reply has neither score nor verdict: {data!r}")
        # salvaged verdict-only reply: pin score just past the threshold
        score = (PASS_THRESHOLD + 10) if verdict == "PASS" else (PASS_THRESHOLD - 10)
    else:
        score = int(round(float(raw_score)))
        if not (0 <= score <= 100):
            raise VoiceJudgeError(f"score out of range: {score}")
    if verdict not in ("PASS", "FAIL"):
        # fall back to threshold if the model omitted/garbled the verdict
        verdict = "PASS" if score >= PASS_THRESHOLD else "FAIL"
    return {
        "verdict": verdict,
        "score": score,
        "describes_food": bool(data.get("describes_food", False)),
        "recites_panel": bool(data.get("recites_panel", False)),
        "reason": str(data.get("reason", "")),
    }


def _main() -> int:
    ap = argparse.ArgumentParser(description="Bari voice/altitude judge (TASK-576).")
    ap.add_argument("--text", help="Hebrew line to score (prefer --text-file on Windows).")
    ap.add_argument("--text-file", help="UTF-8 file whose contents are the line to score.")
    ap.add_argument("--model", default=PINNED_MODEL)
    ap.add_argument("--timeout", type=int, default=CLAUDE_TIMEOUT)
    args = ap.parse_args()

    if args.text_file:
        text = Path(args.text_file).read_text(encoding="utf-8").strip()
    elif args.text:
        text = args.text
    else:
        ap.error("supply --text or --text-file")
        return 2

    res = score_line(text, model=args.model, timeout=args.timeout)
    sys.stdout.write(json.dumps(res, ensure_ascii=False) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
