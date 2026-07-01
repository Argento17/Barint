# Return Contract v1 (mandatory for all agent return blocks)

Every return block MUST end with a fenced JSON block:

```json
{
  "task": "<TASK-ID or P-number>",
  "proposed_status": "RETURNED | BLOCKED",
  "artifacts": [
    {"path": "<repo-relative path>", "action": "created|modified|deleted",
     "sha256": "<hash of final file>"}
  ],
  "counts": {"<claim_name>": "<N>/<M> with M = denominator source named, e.g. 'products_with_image: 80/80 (BSIP1)'"},
  "commands_run": [{"cmd": "<exact command>", "exit_code": 0}],
  "not_done": ["<anything in the spec you did not do, or empty list>"],
  "self_check": "<the one acceptance test from your spec and its observed result>"
}
```

Rules:
1. Every numeric claim in the prose MUST appear in `counts` with its denominator
   and source. A number with no artifact behind it is not a claim — omit it.
2. `artifacts` lists EVERY file touched. sha256 = `Get-FileHash` / `sha256sum` of
   the final state.
3. `not_done` is mandatory honesty: empty list means "spec fully done" and you
   will be held to that.
4. The orchestrator verifies the JSON against the filesystem before acceptance.
   A return block without this JSON is automatically CHANGES_REQUESTED.

   **Enforced deterministically (TASK-420 / W1):** `03_operations\validators\validate_return.py`
   is the C0 gate for this contract. It runs FIRST on every return
   (`python 03_operations\validators\validate_return.py --md tasks\returns\PNN_return.md`):
   schema + 7 keys, sha256 re-hash of every artifact, counts carry a named denominator/source,
   a distribution marker on full-set claims (Rule 5 below), and fabricated-PMID/DOI detection.
   Exit != 0 → automatic CHANGES_REQUESTED. Self-test: `validate_return.py --selftest`.

## Verification-hardening requirements (owner-directed 2026-06-13)

*Added after return-block COUNTS proved untrustworthy: a scoring run reported
`HP_FAT_SODIUM 0/48` when it was **48/48**, and a "4/4 acceptance pairs pass" masked a
**31-product score collapse**. Self-reported numbers are not evidence. These make returns
self-verifying instead of forcing the orchestrator to re-derive everything by hand.*

5. **Full distributions, never example counts.** Any return reporting on a SET (scores,
   grades, products) MUST give the full distribution — histogram, min/max/median,
   **stdev**, and the **most-common-value count** — not a hand-picked sample of N passing
   examples. "4/4 pairs pass" is rejected; `grade_dist + stdev + most_common_score(count)`
   is required. A collapse is invisible in a sampled acceptance test and obvious in a
   distribution (the 72-pin would have shown in the agent's *own* return).
6. **Counts must be trace-derived, with the derivation shown.** Every number in `counts`
   is computed from the committed artifacts (traces/JSON), and the deriving command goes
   in `commands_run`. A counter read from an in-memory variable or a summary field is NOT
   trustworthy — summary counters have been wrong twice. If the orchestrator cannot re-run
   the command and reproduce the number, the count is unverified.
7. **Scoring runs emit a stable verification artifact.** Every scoring/re-scoring run
   writes one flat machine-readable table —
   `barcode, score, grade, binding_caps, nova, fat, sodium, context_flag` — at a
   predictable path. Verification becomes one query against a known schema, not a bespoke
   parser per run (trace keys have drifted: `grade` vs `grade_estimate` vs
   `final_score_estimate`).
8. **Scope/keyword/routing/flag changes require a full cross-corpus baseline diff — from
   the FIRST one.** Re-score EVERY corpus (all published categories + the target) and diff
   against a committed baseline. The invariant/property suite is NOT sufficient — it checks
   properties, not byte-identity; a keyword add can silently rescore products in OTHER
   corpora (EV-052 moved 18 products in maadanim/hard_cheeses, caught two stages late).
   The cross-corpus byte-diff is mandatory on the first such change, not after a surprise.
