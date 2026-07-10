#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""voice_judge_validate.py — calibration harness for voice_judge.py (TASK-576).

Runs the BLIND voice judge over the owner's labeled calibration set and prints a
confusion matrix + precision/recall on catching the owner's REJECTIONS. The
judge is NOT trusted until it reproduces the owner's labels; this harness states
the accuracy honestly, including the HARD case (v3 negatives, which — like the
v5 positives — carry NO numbers, so only voice/altitude separates them).

Labeled set (all in the scratchpad; labels are the owner's actual verdicts):
  POSITIVES (owner-APPROVED voice)  = datastate_rewrite_drafts_v5.json  (`after`)
  NEGATIVES (owner-REJECTED, v2)    = datastate_rewrite_drafts.json     (`after`)  -> cited numbers
  NEGATIVES (owner-REJECTED, v3)    = datastate_rewrite_drafts_v3.json  (`after`)  -> corpus-ranked analyst-speak

Held-out: any line whose exact text is embedded as a few-shot example in the
judge prompt is EXCLUDED from scoring (no train/test leakage).

"Catch the rejection" framing (positive class = a REJECTED line the judge should FAIL):
  TP = negative labeled, judged FAIL   (correctly caught junk)
  FN = negative labeled, judged PASS   (MISSED junk — the dangerous error)
  FP = positive labeled, judged FAIL   (false alarm on good copy)
  TN = positive labeled, judged PASS
"""
from __future__ import annotations

import argparse
import concurrent.futures
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from voice_judge import score_line, PINNED_MODEL, JUDGE_VERSION, prompt_hash  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SCRATCH = Path(r"C:\Users\HP\AppData\Local\Temp\claude\c--Bari"
               r"\789e78e2-be96-44bd-9fb3-efbe15b24485\scratchpad")

# Exact texts embedded in the judge prompt as few-shot examples -> held out.
_EMBEDDED = {
    "גאודה הולנדית קלאסית, עשירה ומלוחה. היא מכילה חלבון גבוה אך גם שומן גבוה. מדובר במוצר יחסית נקי אבל יש לשים לב לכמות הנצרכת.",
    "גבינת גאודה גוסטו 30%, גבינה עשירה וטעימה. חלבון גבוה לצד שומן גבוה, כמצופה מגבינה בדרגת שומן זו.",
    "גרנה פדנו מגורדת, גבינה איטלקית קשה וחריפה בטעמה. החלבון בה גבוה מאוד והשומן מתון יחסית לגבינה מסוג זה.",
    "גאודה מאסדם אמנטל הולנדי: 26 גרם חלבון, נתרן 660 מיליגרם, רשימת רכיבים שלא הגיעה מהסריקה.",
    "גאודה הולנדית עם חלבון מהגבוהים בין הגאודות המלאות בסקירה, לצד נתרן שגם הוא מהגבוהים במדף.",
    "גבינת גאודה גוסטו 30%, עם חלבון גבוה יחסית לגאודות אחרות באותה דרגת שומן, לצד נתרן שגם הוא מהגבוהים במדף.",
}


def _load(path: Path, label: str, source: str) -> list[dict]:
    rows = json.loads(path.read_text(encoding="utf-8"))
    out = []
    for r in rows:
        text = (r.get("after") or "").strip()
        if not text:
            continue
        out.append({
            "text": text,
            "label": label,               # "PASS" (approved) / "FAIL" (rejected)
            "source": source,             # v5 / v2 / v3
            "barcode": str(r.get("barcode", "")),
            "field": r.get("field", ""),
        })
    return out


def build_dataset() -> list[dict]:
    pos = _load(SCRATCH / "datastate_rewrite_drafts_v5.json", "PASS", "v5")
    neg2 = _load(SCRATCH / "datastate_rewrite_drafts.json", "FAIL", "v2")
    neg3 = _load(SCRATCH / "datastate_rewrite_drafts_v3.json", "FAIL", "v3")
    data = pos + neg2 + neg3
    # de-dupe exact-duplicate texts within the same label, and drop embedded few-shot
    seen = set()
    kept = []
    for d in data:
        key = (d["label"], d["text"])
        if d["text"] in _EMBEDDED or key in seen:
            d["held_out_reason"] = "embedded_few_shot" if d["text"] in _EMBEDDED else "dup"
            continue
        seen.add(key)
        kept.append(d)
    return kept


def run(model: str, workers: int, timeout: int, limit: int | None) -> None:
    data = build_dataset()
    if limit:
        # keep a balanced-ish slice for a quick check
        data = data[:limit]
    print(f"# voice_judge validation  (judge={JUDGE_VERSION}  model={model}  "
          f"prompt_hash={prompt_hash()})")
    print(f"# scoring {len(data)} held-out lines "
          f"(POS/approved={sum(d['label']=='PASS' for d in data)}  "
          f"NEG/rejected={sum(d['label']=='FAIL' for d in data)})  workers={workers}")
    sys.stdout.flush()

    def _score(d):
        try:
            res = score_line(d["text"], model=model, timeout=timeout)
            return d, res, None
        except Exception as e:
            return d, None, repr(e)

    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as ex:
        for d, res, err in ex.map(_score, data):
            results.append((d, res, err))
            tag = "ERR" if err else f"{res['verdict']:4s} {res['score']:3d}"
            mark = ""
            if res:
                ok = (res["verdict"] == d["label"])
                mark = "ok " if ok else "XX "
            line_preview = d["text"][:46]
            print(f"  {mark}[{d['source']}/{d['label']:4s}] {tag}  {line_preview}")
            sys.stdout.flush()

    scored = [(d, r) for d, r, e in results if r is not None]
    errors = [(d, e) for d, r, e in results if e is not None]

    # Confusion matrix (positive class = a REJECTED line correctly FAILed)
    TP = FN = FP = TN = 0
    hard_correct = hard_total = 0     # v3 negatives (the no-numbers hard case)
    v2_correct = v2_total = 0         # v2 negatives (easy: has numbers)
    pos_correct = pos_total = 0       # v5 positives
    for d, r in scored:
        j = r["verdict"]
        if d["label"] == "FAIL":       # owner rejected
            if j == "FAIL":
                TP += 1
            else:
                FN += 1
            if d["source"] == "v3":
                hard_total += 1
                hard_correct += (j == "FAIL")
            elif d["source"] == "v2":
                v2_total += 1
                v2_correct += (j == "FAIL")
        else:                          # owner approved
            pos_total += 1
            pos_correct += (j == "PASS")
            if j == "PASS":
                TN += 1
            else:
                FP += 1

    total = TP + FN + FP + TN
    acc = (TP + TN) / total if total else 0.0
    prec = TP / (TP + FP) if (TP + FP) else 0.0
    rec = TP / (TP + FN) if (TP + FN) else 0.0
    f1 = 2 * prec * rec / (prec + rec) if (prec + rec) else 0.0

    print("\n" + "=" * 60)
    print("CONFUSION MATRIX  (positive class = owner-REJECTED line the judge should FAIL)")
    print("=" * 60)
    print(f"                        judged FAIL   judged PASS")
    print(f"  owner REJECTED (neg)      {TP:3d} (TP)     {FN:3d} (FN)")
    print(f"  owner APPROVED (pos)      {FP:3d} (FP)     {TN:3d} (TN)")
    print("-" * 60)
    print(f"  accuracy                 {acc:.3f}   ({TP+TN}/{total})")
    print(f"  precision (catch)        {prec:.3f}   TP/(TP+FP)")
    print(f"  recall    (catch)        {rec:.3f}   TP/(TP+FN)")
    print(f"  F1                       {f1:.3f}")
    print("-" * 60)
    print("SUBSET breakdown:")
    print(f"  v5 positives  correct-PASS : {pos_correct}/{pos_total}"
          f"   ({pos_correct/pos_total:.2f})" if pos_total else "  v5 positives: none")
    print(f"  v2 negatives  correct-FAIL : {v2_correct}/{v2_total}"
          f"   ({v2_correct/v2_total:.2f})   [EASY: has numbers]" if v2_total else "")
    print(f"  v3 negatives  correct-FAIL : {hard_correct}/{hard_total}"
          f"   ({hard_correct/hard_total:.2f})   [HARD: no numbers, analyst-speak]"
          if hard_total else "")
    if errors:
        print("-" * 60)
        print(f"  transport/parse ERRORS: {len(errors)}")
        for d, e in errors[:8]:
            print(f"    [{d['source']}/{d['label']}] {e[:120]}")
    print("=" * 60)

    report = {
        "judge_version": JUDGE_VERSION, "model": model, "prompt_hash": prompt_hash(),
        "n_scored": total, "accuracy": acc, "precision_catch": prec,
        "recall_catch": rec, "f1": f1,
        "confusion": {"TP": TP, "FN": FN, "FP": FP, "TN": TN},
        "subsets": {
            "v5_pos_correct": [pos_correct, pos_total],
            "v2_neg_correct": [v2_correct, v2_total],
            "v3_neg_correct": [hard_correct, hard_total],
        },
        "errors": len(errors),
        "detail": [
            {"source": d["source"], "label": d["label"], "barcode": d["barcode"],
             "field": d["field"], "verdict": r["verdict"], "score": r["score"],
             "reason": r["reason"], "text": d["text"]}
            for d, r in scored
        ],
    }
    out = SCRATCH / f"voice_judge_validation_{model.replace('/', '_')}.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"# full report -> {out}")


def _main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default=PINNED_MODEL)
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--timeout", type=int, default=180)
    ap.add_argument("--limit", type=int, default=None, help="score only first N (quick check)")
    args = ap.parse_args()
    run(args.model, args.workers, args.timeout, args.limit)
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
