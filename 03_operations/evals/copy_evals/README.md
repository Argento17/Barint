# Copy Evals — calibrated regression suite for Bari's Hebrew consumer copy (TASK-505)

A promptfoo-style, versioned eval harness: a fixed dataset of known-good and known-bad
Hebrew copy, scored by the deterministic gates on every run, with a committed baseline
so **any behavior change in the gates is caught as a diff, not discovered on a live page.**

Serves Project Tom's Voice (TASK-374): the deterministic layer is frozen here, and the
classes it provably cannot catch (fabrication, stale rank, relational framing,
translationese) stay visible as FN/SKIP rows — the calibration target for the future
LLM naturalness judge (`judge/`).

## Layout

```
copy_evals/
  dataset/cases.jsonl        # the eval set (one JSON case per line, UTF-8)
  dataset/baseline.json      # committed snapshot of gate verdicts (default mode)
  run_evals.py               # the runner / regression gate
  judge/calibration.md       # LLM-judge calibration protocol (judge is NOT live)
  judge/labels_template.jsonl# owner labeling session template
  judge/judge_stub.py        # interface stub — raises NotImplementedError
```

## Run

```
cd C:\Bari
python 03_operations\evals\copy_evals\run_evals.py                  # readability gate only
python 03_operations\evals\copy_evals\run_evals.py --with-grammar   # + DictaBERT grammar gate
python 03_operations\evals\copy_evals\run_evals.py --update-baseline
```

- Exit **0** = every gate verdict matches `dataset/baseline.json`. Exit **1** = regression
  (or missing baseline / bad dataset).
- `--with-grammar` is opt-in because `hebrew_grammar_gate.py` downloads a ~440MB
  DictaBERT model on first use. Grammar-mode verdicts are informational and are **not**
  compared to the baseline (the baseline freezes default-mode verdicts only).
- `--update-baseline` re-freezes the snapshot. Use it **only after an intentional
  change** (gate improved, case added), review the `baseline.json` diff, and commit
  both files together. An unexplained baseline diff in review = a silent gate change.

## Reading the output

Positive class = "copy is defective". `TP` = known-bad copy the gates caught;
`FN` = known-bad copy the gates missed; `FP` = known-good copy wrongly flagged;
`SKIP` = `expected: null` owner-label slots (translationese) awaiting calibration.

**FNs are expected and deliberate** for `fabricated_provenance`, `stale_rank`,
`relational_framing`, and (default mode) `grammar_agreement` — deterministic string
gates cannot see those. They are frozen in the baseline so the day a gate (or the
calibrated judge) starts catching them, the run flips to exit 1 and the improvement
gets re-frozen consciously.

Known documented quirks frozen in the baseline:

- `fl-001` (FN): `hebrew_readability.py`'s Hebrew leak-term list misses
  `מדד עיבוד`/`תקרת עיבוד` — the same Hebrew-coverage gap TASK-445 recorded for G6.
- `cc-004` (FP): the score-mechanic regex `\b\d{2,3}\.\d+\b` flags the legitimate
  nutrition decimal `10.1` (grams of protein) as an exposed score.

Fixing either is welcome — the run will exit 1, you re-freeze with `--update-baseline`,
and the diff documents the improvement.

## Adding a case

1. Append one JSON line to `dataset/cases.jsonl` (UTF-8; edit the file directly —
   never route Hebrew through `python -c` on Windows, it corrupts):
   `{"id", "text", "expected": "pass"|"fail"|null, "failure_class", "source", "owner_labeled", "note"}`
2. Sourcing rule (**hard**): if the text is a real artifact, `source` is its repo
   path (and the incident doc in `note`). If you could not find the real string,
   write a minimal synthetic example with `"source": "synthetic"` — **never present
   synthetic text as a real incident**, including "reconstructions" (label them as
   such in `note`, as `fp-002`/`sr-002` do).
3. Naturalness/translationese candidates get `expected: null, needs_label: true` —
   only the owner labels naturalness until the judge is calibrated.
4. Run the suite → it exits 1 ("NEW CASE") → review, `--update-baseline`, commit
   `cases.jsonl` + `baseline.json` together.

## Judge calibration (short version — full protocol in `judge/calibration.md`)

Owner labels ≥40 mixed examples (`judge/labels_template.jsonl`) → blind judge run on a
pinned model+prompt → TPR ≥ 0.80 and TNR ≥ 0.90 → committed calibration record with
owner sign-off → only then does the judge become a gate (and its verdicts enter this
baseline). Every prompt/model change re-runs calibration. `judge_stub.py` raises
`NotImplementedError` until that happens — do not fake it.

## The rule

**Every change to any of the following MUST run this suite (default mode) and commit
the resulting baseline diff, if any, in the same change:**

- `integrations/clients/hebrew_readability.py`
- `integrations/clients/hebrew_grammar_gate.py`
- any copy-generating skill or prompt (Content lane templates, verdict authoring
  prompts, tone briefs that alter generation)
- editorial law that defines what copy may say (leak-term lists, recommendation-language
  policy, score-presentation rules, phrasing bans)

A gate change without a green (or consciously re-frozen) eval run is unverified —
the exact class of silent drift that shipped the granola fabrication (TASK-385) and
the brined framework leakage (TASK-445).
