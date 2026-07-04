# Naturalness Judge — Calibration Record v1 (TASK-506)

> **STATUS: BAR NOT CLEARED. Judge stays UN-WIRED (advisory only).**
> This record documents a real, measured calibration attempt per
> `judge/calibration.md`. The acceptance bar (TPR ≥ 0.80 AND TNR ≥ 0.90) was
> **not** met by any judge version. Per calibration.md the judge may gain gate
> authority ONLY after a committed record that clears the bar **and** owner
> sign-off — neither holds. `judge_stub.py` remains `NotImplementedError`;
> nothing is wired into `run_evals.py`.

Date: **2026-07-04**
OWNER DECISION (2026-07-04): **SHELVE the LLM judge (option b).** Owner reviewed the
bar-not-cleared result and the structural analysis and chose to keep the deterministic
system (the D3 sign-off gate: em-dash advisory / antithesis+sodium+brand hard, plus the
existing heuristic `naturalness_gate.py`) + the manual rewrite pass. The LLM judge is
**not adopted** — it stays `NotImplementedError` / un-wired, and this record is filed as
the honest calibration outcome. A future re-attempt would first resolve the provisional
`partially_approved` mapping per the Recommendation below.

---

## Judge identity (best version)

| Field | Value |
|---|---|
| Judge module | `judge/naturalness_judge.py` |
| Best `JUDGE_VERSION` | **1.1** |
| Pinned model | **`claude-opus-4-8`** (exact id) |
| Pinned-prompt hash (v1.1) | **`3aa7928ff4167c4a`** (sha256[:16] of `PROMPT_TEMPLATE`) |
| LLM-call mechanism | local `claude` CLI headless print mode (`claude -p --model claude-opus-4-8 --output-format json --max-turns 1`), prompt fed over **stdin as UTF-8** (Windows Hebrew-argv safe). Reuses the environment's existing Claude credential — no `ANTHROPIC_API_KEY` in env, no `anthropic` SDK installed. |
| Blindness | Judge sees ONLY the rubric + the single line to score. Owner labels are never in the prompt. |
| Decision rule | `score < threshold` ⇒ predict **UNNATURAL** (flag); `score ≥ threshold` ⇒ **NATURAL** (pass). |

## Labeled set

Source: `judge/labels_template.jsonl`, rows with `in_judge_scope: true` (rowVerdict
+ tr_slot; insightLines excluded per owner). Ground truth = `owner_label`
(owner-locked "flag": approved ⇒ natural; partially_approved OR not_approved ⇒
unnatural).

| Set | N | natural | unnatural |
|---|---|---|---|
| In-scope originals | 41 | 10 | 31 |
| Rewrite seeds (non-empty `owner_rewrite` of in-scope rows; owner-authored, natural by construction) | 19 | 19 | 0 |
| **With seeds (union)** | 60 | 29 | 31 |

Per-example blind scores (all three versions): `judge/calibration_scores_v1.0.json`,
`…_v1.1.json`, `…_v1.2.json`.

---

## Iterations (each a real blind run of all 60 items; ASCII metrics)

Metrics on **originals only** (the owner in-scope labels). "best@TNR≥.90" =
highest-TPR operating point that still holds TNR ≥ 0.90; "balanced" = max
min(TPR,TNR).

| Ver | Prompt change | class sep (natural−unnatural mean) | best@TNR≥.90 TPR | balanced TPR/TNR | Bar |
|---|---|---|---|---|---|
| 1.0 | Holistic "how natural does this read" | 0.837 − 0.787 = **0.05** | 0.161 | 0.581 / 0.600 | ✗ |
| **1.1** | Reframed as a **strict publish-as-is editorial gate** (exacting senior editor; reserve ≥0.85 for publish-perfect; treat number-restatement / em-dash-crutch / X-not-Y / סודיום / ברי / fragment-tags / stiffness as real defects, holistically) | 0.738 − 0.453 = **0.285** | **0.452** | **0.710 / 0.700** | ✗ |
| 1.2 | v1.1 + **hard** cap-at-0.30 rules for literal `סודיום`/`סודים`, standalone `ברי`, `X, לא Y` | 0.657 − 0.538 = **0.12** | 0.161 | 0.516 / 0.600 | ✗ |

**v1.2 regressed** and was reverted: the hard `X, לא Y` rule over-fired on
legitimate negations inside the *natural* lines (e.g. "אין פה תוספת", "לא תוספת"),
pulling naturals down to 0.28 and collapsing separation. **v1.1 is the best
version** and is what the module is pinned to.

---

## Best version (v1.1) — confusion matrix at the chosen operating point

calibration.md sets specificity as the stricter target ("an ignored gate is worse
than no gate"), so the chosen point is the specificity-first one: **threshold = 0.28**
(highest-TPR point still holding TNR ≥ 0.90).

**Originals only (N=41), threshold 0.28:**

|  | pred UNNATURAL (flag) | pred NATURAL (pass) |
|---|---|---|
| **owner UNNATURAL** (31) | TP = 14 | FN = 17 |
| **owner NATURAL** (10) | FP = 1 | TN = 9 |

- **TPR = 14/31 = 0.452** (share of unnatural flagged) — **FAILS** the 0.80 floor.
- **TNR = 9/10 = 0.900** (share of natural passed) — meets the 0.90 floor.
- **Bar (TPR ≥ 0.80 AND TNR ≥ 0.90): NOT CLEARED.**

**With rewrite seeds (N=60):** worse. The owner's own rewrites score LOW
(median 0.28) — the judge rates the owner's terse rewrites as needing work — so at
TNR ≥ 0.90 the threshold collapses to ~0.05 and **TPR = 2/31 = 0.065**. Seeds do
not help; they show the "natural" target is not a fluency axis (see analysis).

**Held-out sanity check (v1.1, stratified ~50/50, seed 506):** tune threshold on
train (thr=0.72, train TPR 0.88 / TNR 1.00) → **test TPR 0.533 / TNR 0.400**. The
operating point does not generalize — expected given N and the class overlap.

---

## Why the bar was not cleared (honest failure analysis)

1. **The "unnatural" class is dominated by *partially_approved* lines** (24 of the
   31 in-scope unnaturals). Their owner objection is a **sub-threshold editorial
   preference** — "only take out the em-dashes" (lb2-020), "change only the ending"
   (ls-023), one odd simile (lb2-014 "לא חד כמו פגיון") — on lines that are otherwise
   publish-quality native Hebrew. A strong holistic judge rates them **0.72–0.90**,
   the same band as the *approved* lines. 11 of the 31 unnaturals score ≥ 0.70.

2. **The flagging surface features also appear in APPROVED lines.** ls-029 (approved)
   restates 31% / 34% / 10.1 g **and** uses an em-dash; lb2-021/023 (approved) use
   em-dashes. Keying on em-dashes/number-restatement therefore destroys TNR — v1.2
   demonstrated this directly (naturals ls-029→0.32, lb2-022→0.20). The two classes
   are **not separable on the axis the judge can perceive**.

3. **Ground-truth is internally inconsistent for a naturalness axis.** The owner
   *approved* lines carrying the very "defect" flagged elsewhere (owner's own note on
   the approved ls-034: "would drop the nutritional-value repetition"). And the
   owner's **rewrites** (ground-truth natural) trade fluency for terseness, so they
   score *lower* than the flagged originals (seed mean 0.685 at v1.0). "Natural" per
   owner is not "reads more natural" per model — on the terse rewrites it is inverted.

4. **The binary mapping is explicitly provisional.** Every partially_approved ⇒
   unnatural row is `label_provisional: true`; the labeling session
   (`labeling_session_2026-07-04.md` → "Open") left the partially_approved mapping
   **unresolved** and recommended a one-line flip if the owner prefers "ship". The
   bar is being measured against labels the labeling session itself flagged as not
   final.

**Conclusion:** with the current provisional labels the bar is likely
**structurally unreachable** by a single-line LLM judge — not a prompt-tuning gap.
The strict-editorial reframe (v1.0→v1.1) already tripled TPR-at-fixed-TNR
(0.16→0.45) and is near the ceiling the label overlap allows.

## Recommendation (before any re-attempt)

- **Resolve the provisional partially_approved mapping** (the open item in the
  labeling session). If partially_approved is re-mapped to "ship" (natural), or the
  set is re-labeled on a single clean **"publish exactly as-is: yes/no"** axis, the
  target becomes learnable. As labeled today it mixes "needs a rewrite" with "would
  tweak one word."
- **Drop or re-derive the rewrite seeds** from the natural class — terse owner
  rewrites depress the natural band and are not representative of shippable copy.
- Until then, the deterministic `integrations/clients/naturalness_gate.py` remains
  the only naturalness check (mechanical translationese tells, HIGH/MEDIUM). This
  LLM judge stays **advisory / un-wired**; do not add it to `run_evals.py`.

---

## Provenance / reproducibility

- Judge: `judge/naturalness_judge.py` (`JUDGE_VERSION=1.1`, `PINNED_MODEL=claude-opus-4-8`,
  `prompt_hash()=3aa7928ff4167c4a`). The module as committed reproduces the v1.1 hash.
- Blind scores: `judge/calibration_scores_v1.0.json` / `_v1.1.json` / `_v1.2.json`
  (each records model, prompt_hash, and per-example {id, gold, score, rationale}).
- `dataset/cases.jsonl`, `baseline.json`, and `run_evals.py` were **not** modified.
- No consumer copy was touched. No git commit. Judge NOT wired as a gate.
