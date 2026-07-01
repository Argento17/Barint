#!/usr/bin/env python3
r"""
verify_variance.py — independent-lane variance verification of a claim (TASK-422 / W3-B)
========================================================================================

Second half of W3. `rank_check.py` handles claims a script can settle deterministically
(superlatives vs the corpus). This handles the claims a script CANNOT settle — "is this
verdict defensible?", "is this framing honest?", "does this explanation match the trace?" —
by asking several INDEPENDENT lanes and measuring their agreement.

The 2026 evidence is specific and slightly counterintuitive:
  - Cross-model verification cuts hallucination ~25% (MDPI 15/7/3676).
  - Orchestrated multi-agent DEBATE often UNDERPERFORMS simple self-consistency across
    independent samples (OpenReview Vusd1Hw2D9); and panels converge on false consensus
    when they can see each other (Microsoft: cap at <=3). So we do NOT run a debate — we
    sample INDEPENDENT lanes blind and treat DISAGREEMENT (high variance) as the signal:
    "if variance exceeds a threshold, flag for review."

Decision rule (deliberately strict — this is a gate, and a false CONFIRM is the costly error):
  CONFIRMED  — decisive votes agree at/above --confirm-agreement (default 1.0 = unanimous),
               no refusals. The claim survives independent scrutiny.
  REFUTED    — a MAJORITY of lanes refute it (no >= ceil(N/2) and no > yes). Kill it.
  FLAGGED    — anything else: a split, an UNSURE, a lone dissenter. High variance → a human
               looks. (Better to flag a true claim than confirm a false one.)

Lanes are pluggable and INDEPENDENT by construction — each is a shell command that receives
the claim (as JSON) on stdin and prints one verdict. Wire the real Bari lanes as adapters:
  - C3 (ChatGPT, independent):  a wrapper around `03_operations/router/dispatch.py` route C3
  - Opus critic (independent):  the Adversarial-QA critic lane (opus, per critic_lane_opus_and_c3)
A lane's output is parsed as JSON {"vote":"YES|NO|UNSURE","confidence":0..1,"rationale":"..."},
or a bare leading token YES/NO/UNSURE. Any lane error → that lane abstains (does not crash the gate).

Exit codes: 0 CONFIRMED · 1 REFUTED or FLAGGED (needs attention) · 2 usage/no-lanes.

Usage:
  python verify_variance.py --claim "Tvorog has the highest protein on this shelf" \
      --context-file cheese.json \
      --lane "python 03_operations/router/dispatch.py --verify-stdin C3" \
      --lane "python tools/opus_critic.py"
  python verify_variance.py --claim "..." --lane "..." --json
  python verify_variance.py --selftest
"""
from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]
    except (AttributeError, ValueError):
        pass

VOTES = ("YES", "NO", "UNSURE")


def parse_verdict(raw: str, lane: str) -> dict:
    """Normalise a lane's stdout into {lane, vote, confidence, rationale}."""
    raw = (raw or "").strip()
    if not raw:
        return {"lane": lane, "vote": "UNSURE", "confidence": 0.0, "rationale": "(empty output)"}
    # try JSON first
    try:
        obj = json.loads(raw)
        if isinstance(obj, dict) and "vote" in obj:
            vote = str(obj["vote"]).strip().upper()
            if vote not in VOTES:
                vote = "UNSURE"
            conf = obj.get("confidence")
            conf = float(conf) if isinstance(conf, (int, float)) else 0.5
            return {"lane": lane, "vote": vote, "confidence": max(0.0, min(1.0, conf)),
                    "rationale": str(obj.get("rationale", ""))[:400]}
    except (json.JSONDecodeError, ValueError):
        pass
    # fall back to a leading token
    head = raw.upper()[:16]
    for v in VOTES:
        if head.startswith(v):
            return {"lane": lane, "vote": v, "confidence": 0.5, "rationale": raw[:400]}
    return {"lane": lane, "vote": "UNSURE", "confidence": 0.0,
            "rationale": f"(unparseable: {raw[:120]})"}


def run_lane(cmd: str, payload: str, timeout: int = 180) -> dict:
    """Run one lane command, feeding the claim payload on stdin. Errors → abstain (UNSURE)."""
    try:
        # UTF-8 explicitly — the claim payload carries Hebrew; default cp1252 stdin encode crashes.
        proc = subprocess.run(cmd, shell=True, input=payload, encoding="utf-8",
                              errors="replace", capture_output=True, timeout=timeout)
        if proc.returncode != 0:
            return {"lane": cmd, "vote": "UNSURE", "confidence": 0.0,
                    "rationale": f"(lane exit {proc.returncode}: {proc.stderr[:120]})"}
        return parse_verdict(proc.stdout, cmd)
    except subprocess.TimeoutExpired:
        return {"lane": cmd, "vote": "UNSURE", "confidence": 0.0, "rationale": "(timeout)"}
    except Exception as e:  # noqa: BLE001 — a lane failure must not crash the gate
        return {"lane": cmd, "vote": "UNSURE", "confidence": 0.0, "rationale": f"(error: {e})"}


def aggregate(verdicts: list[dict], confirm_agreement: float = 1.0) -> dict:
    """Combine independent verdicts into a decision + variance signal."""
    total = len(verdicts)
    yes = sum(1 for v in verdicts if v["vote"] == "YES")
    no = sum(1 for v in verdicts if v["vote"] == "NO")
    unsure = sum(1 for v in verdicts if v["vote"] == "UNSURE")
    decisive = yes + no
    agreement = (max(yes, no) / decisive) if decisive else 0.0
    # normalized entropy over {yes,no,unsure} as a variance/uncertainty scalar (0=consensus)
    dist = [c / total for c in (yes, no, unsure) if c]
    entropy = -sum(p * math.log(p, 2) for p in dist) if dist else 0.0
    max_ent = math.log(min(3, total), 2) if total > 1 else 1.0
    variance = round(abs(entropy / max_ent), 3) if max_ent else 0.0

    majority = math.ceil(total / 2)
    if no >= majority and no > yes:
        decision = "REFUTED"
    elif unsure == 0 and no == 0 and yes >= 1 and agreement >= confirm_agreement:
        decision = "CONFIRMED"
    else:
        decision = "FLAGGED"

    return {"decision": decision, "tally": {"YES": yes, "NO": no, "UNSURE": unsure, "total": total},
            "agreement": round(agreement, 3), "variance": variance,
            "verdicts": verdicts}


def render(claim: str, agg: dict) -> str:
    icon = {"CONFIRMED": "PASS", "REFUTED": "FAIL", "FLAGGED": "WARN"}[agg["decision"]]
    out = [f"verify_variance :: {agg['decision']}",
           f'  claim: "{claim[:90]}"',
           f"  tally: {agg['tally']}  agreement={agg['agreement']}  variance={agg['variance']}",
           "-" * 60]
    for v in agg["verdicts"]:
        out.append(f"  [{v['vote']:<6}] c={v['confidence']:.2f}  {v['lane'][:44]}")
        if v["rationale"]:
            out.append(f"           {v['rationale'][:100]}")
    out.append("-" * 60)
    out.append(f"  [{icon}] {agg['decision']}")
    return "\n".join(out)


def verify(claim: str, context: str, lanes: list[str], confirm_agreement: float) -> dict:
    payload = json.dumps({"claim": claim, "context": context}, ensure_ascii=False)
    verdicts = [run_lane(cmd, payload) for cmd in lanes]
    return aggregate(verdicts, confirm_agreement)


def run_selftest() -> int:
    """Aggregation logic must be correct regardless of live lanes — mock the verdicts."""
    def mock(votes):
        return [{"lane": f"mock{i}", "vote": v, "confidence": 0.7, "rationale": ""}
                for i, v in enumerate(votes)]

    cases = [
        (["YES", "YES", "YES"], "CONFIRMED"),   # unanimous
        (["NO", "NO", "YES"], "REFUTED"),        # majority refute
        (["YES", "NO", "YES"], "FLAGGED"),       # lone dissenter → not confirmed
        (["YES", "YES", "UNSURE"], "FLAGGED"),   # an abstention breaks unanimity
        (["NO", "NO", "NO"], "REFUTED"),         # unanimous refute
    ]
    ok = True
    for votes, expected in cases:
        got = aggregate(mock(votes))["decision"]
        mark = "ok" if got == expected else "WRONG"
        if got != expected:
            ok = False
        print(f"  {votes} -> {got} (expect {expected}) {mark}")
    # a relaxed confirm-agreement should let 2/3 confirm
    relaxed = aggregate(mock(["YES", "YES", "NO"]), confirm_agreement=0.66)["decision"]
    # still FLAGGED because a NO is present (no==0 required for CONFIRMED) — verify strictness
    strict_ok = relaxed == "FLAGGED"
    print(f"  2Y/1N @agree0.66 -> {relaxed} (expect FLAGGED: a refusal blocks CONFIRM) "
          f"{'ok' if strict_ok else 'WRONG'}")
    ok = ok and strict_ok
    print(f"SELFTEST: {'OK' if ok else 'BROKEN'}")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Independent-lane variance verification of a claim.")
    ap.add_argument("--claim", help="the claim to verify")
    ap.add_argument("--context", default="", help="inline context string")
    ap.add_argument("--context-file", help="path whose contents become the context")
    ap.add_argument("--lane", action="append", default=[], metavar="CMD",
                    help="a lane command (repeatable); receives the claim JSON on stdin, prints a verdict")
    ap.add_argument("--confirm-agreement", type=float, default=1.0,
                    help="min agreement among decisive votes to CONFIRM (default 1.0 = unanimous)")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return run_selftest()
    if not args.claim:
        print("verify_variance: --claim required", file=sys.stderr)
        return 2
    if not args.lane:
        print("verify_variance: at least one --lane required (independent verifiers)", file=sys.stderr)
        return 2

    context = args.context
    if args.context_file:
        try:
            context = Path(args.context_file).read_text(encoding="utf-8")[:6000]
        except OSError as e:
            print(f"verify_variance: cannot read context-file: {e}", file=sys.stderr)
            return 2

    agg = verify(args.claim, context, args.lane, args.confirm_agreement)
    if args.json:
        print(json.dumps({"claim": args.claim, **agg}, ensure_ascii=False, indent=2))
    else:
        print(render(args.claim, agg))
    return 0 if agg["decision"] == "CONFIRMED" else 1


if __name__ == "__main__":
    sys.exit(main())
