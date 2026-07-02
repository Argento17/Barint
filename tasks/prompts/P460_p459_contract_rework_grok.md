# P460 / P459 contract rework — fix Return Contract violations, no new code (route: C1-GROK)

## 1. Context
- You are in worktree `C:\bari_wt_t449` (branch `fix/task449-brined-inversion`). Your P459 work (commits `1a25819b`, `6616f78a`, return committed at `5ea997bb`) was orchestrator-reviewed: **code verified correct and scoped — do NOT change any code.** The return FAILED the C0 contract validator. This dispatch fixes the contract + adds two missing verifications. This is the single allowed rework; a second failure escalates.

## 2. Exact C0 failures to fix
Run `git show 5ea997bb:tasks/returns/P459_return.md` to see your prior return. Produce a corrected full return at a NEW path: **`tasks\returns\P459_contract.md`** (the router overwrites `P459_return.md`, so the durable contract lives at the new path). Fixes:
1. **Real sha256 for every artifact.** The 6 code files carried `"sha256": "to-be-verified"` — compute actual sha256 of each file's current state (`certutil -hashfile <f> SHA256` or python hashlib). Update the staging-artifact hashes too if they changed.
2. **Remove the return-file self-entry** from `artifacts` (`"sha256": "self"` is invalid; the return is not an artifact).
3. **Rule-5 distribution markers inside the flagged counts values** — `brined_score_moves_ON`, `brined_grade_moves_ON`, `grade_flips_listed_in_G7`, `router_induced_score_moves` must each carry `stdev` and `most_common` markers in the value string, e.g. `"24/36 (rescore_all vs live; OFF dist median 72.25 stdev 9.24 most_common 72.25(x3) → ON median 65.05 stdev 8.34 most_common ...)"`. Pull the real numbers from your rescore outputs.
4. **Exit-code semantics inline** in each `commands_run` entry that returned 1, e.g. `"exit 1 = diffs detected by design (rescore_all exits nonzero when movement found)"` / `"exit 1 = gate FAILs present (pre-existing G1/G3)"`. If that is NOT actually the tool's semantics — i.e., the run genuinely errored — say so honestly and propose BLOCKED.

## 3. Two additional verifications (evidence, not code)
5. **Pinned-corpus identity:** prove the candidate `_rescore_staging/brined_cheeses/brined_cheeses_candidate_brinedfix.json` has the EXACT barcode set of the live `bari-web/src/data/comparisons/brined_cheeses_frontend_v2.json` (36/36, 0 added, 0 dropped). Add as a count with the deriving command.
6. **OFF-trace byte-identity spot-proof:** with flag OFF, regenerate the trace for ONE brined product and ONE non-brined product and byte-diff each against its pre-change counterpart (git stash-free: use the committed baseline trace or re-run at `origin/master` code via `git worktree`-less `git show` reconstruction if needed — simplest: rerun rescore for those two products at HEAD with flag OFF and diff against their live committed traces). Add as counts (`off_trace_byte_identical: 2/2 (...cmd...)`).

## 4. Self-gate before returning
Run: `python 03_operations\validators\validate_return.py --md tasks\returns\P459_contract.md --root C:\bari_wt_t449` — it MUST exit 0. Iterate until it does. Then commit the contract file (`git add tasks/returns/P459_contract.md && git commit -m "P459 contract rework (P460): real shas, Rule-5 dists, exit-code semantics, pin+byte-identity proofs"`).

## 5. Boundaries
No code changes. No push/PR/deploy. No edits outside `tasks/returns/P459_contract.md`. OFF ban absolute. Main tree `C:\Bari` untouched. End your stdout summary with the same JSON contract you wrote to the file. Propose RETURNED.
