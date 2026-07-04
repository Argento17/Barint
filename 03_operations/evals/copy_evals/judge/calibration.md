# Naturalness Judge — Calibration Protocol (uncalibrated; NOT a gate)

Status: **STUB.** `judge_stub.py` raises `NotImplementedError` by design. No LLM judge
in this repo has gate authority over Hebrew naturalness.

## Why calibration is mandatory

Project Tom's Voice (TASK-374) identified the core defect: **no deterministic gate
catches translationese.** `hebrew_readability.py` catches framework leakage,
recommendation language, and score mechanics — it cannot tell "השמן שמציעים" from
natural Hebrew. The planned centerpiece is an LLM-judge naturalness gate.

But an LLM judge is an opinion until it is measured. The project's own history shows
why unmeasured checkers are dangerous: self-gates that "passed" fabricated copy
(granola canola incident, TASK-385), self-counts that reported "0 issues" while 6
false superlatives shipped (TASK-409 protein bars). A judge that blocks or approves
consumer copy without a measured error rate is the same failure with better branding.

**Rule: the naturalness judge may become a gate ONLY after calibration against
owner-labeled examples, with tracked TPR/TNR, committed as a calibration record.**
Until then its output is advisory at most, and it must not set `is_clean`-style
verdicts anywhere in the pipeline.

## Protocol

1. **Collect owner labels.** Fill `labels_template.jsonl` in an owner labeling
   session. Each row: the owner reads the Hebrew text and sets
   `owner_label: "natural" | "unnatural"` plus an optional one-line `owner_note`
   (what grated, if anything). Target: **≥ 40 labeled examples**, mixed —
   the dataset's `translationese` slot cases (tr-001…tr-005), live shipped verdicts,
   and fresh candidates. Do not let one author's style dominate the natural set.
2. **Freeze a judge version.** Implement `score_naturalness` behind a pinned model id
   + pinned prompt (record both in `JUDGE_VERSION`). The judge never sees the owner
   labels during scoring (blind run).
3. **Measure.** Run the judge over every labeled example. Pick the decision threshold
   on `score`, then report:
   - **TPR** (sensitivity): share of owner-labeled *unnatural* examples the judge flags.
   - **TNR** (specificity): share of owner-labeled *natural* examples the judge passes.
4. **Acceptance bar (initial):** TPR ≥ 0.80 AND TNR ≥ 0.90. Specificity is
   deliberately stricter — a judge that nags on natural Hebrew will be ignored, and an
   ignored gate is worse than no gate. If the bar fails: fix the prompt/model, bump
   `JUDGE_VERSION`, re-run step 3. Never tune the threshold on the same labels you
   report on if more labels are available (hold out when N allows).
5. **Commit the calibration record** next to this file
   (`calibration_record_vN.md`): judge version, model id, prompt hash, label count,
   confusion matrix, TPR/TNR, threshold, date, owner sign-off. Only then may the
   judge be wired as a gate — and it enters `run_evals.py` as a scored gate whose
   verdicts get frozen into the baseline like any other.
6. **Re-calibrate on every change.** Any change to the judge prompt, model, or
   threshold invalidates the record: re-run steps 3–5 before the judge regains gate
   authority. Track drift by re-running the labeled set on a schedule.

## Labeling session mechanics

- Labels live in `labels_template.jsonl` (UTF-8; never paste Hebrew through
  `python -c` on Windows — edit the file directly).
- `owner_label` values: `"natural"`, `"unnatural"`. Anything else (including leaving
  `null`) means unlabeled; the runner keeps such cases in SKIP.
- After a session, copy labels back into `dataset/cases.jsonl`: set
  `expected: "pass"` (natural) or `"fail"` (unnatural), `owner_labeled: true`,
  drop `needs_label` — then `--update-baseline` and commit.
