# P459 / TASK-449 brined inversion fix (Option A) + router "מלא" collision fix (route: C1-GROK)

## 1. Repo / paths / baseline
- Repo: `C:\Bari` (monorepo; engine at `03_operations\bsip2\proto_v0\src\`, website at `bari-web\`).
- **Work in an ISOLATED WORKTREE — never touch the main working tree** (it is on `feature/homepage-mascots` and shared):
  ```
  git -C C:\Bari fetch origin
  git -C C:\Bari worktree add C:\bari_wt_t449 -b fix/task449-brined-inversion origin/master
  ```
  Record the origin/master SHA you branched from in your return. All edits, runs, and commits happen inside `C:\bari_wt_t449`.
- Read FIRST: `C:\Bari\tasks\TASK-449.md` (full D6/D7 verified diagnosis) and `C:\Bari\tasks\reports\TASK-449_brined_inversion_diagnosis_2026-07-02.md`.

## 2. Objective (owner GO recorded 2026-07-02 — tripwire #1 cleared for implementation; deploy stays owner-gated)
Two scoped engine fixes, **two separate commits**, each with its own cross-corpus proof:

**Commit 1 — TASK-449 Option A (D6+D7 co-signed):**
- Restrict the Path B `cultured_cheese_name` fermentation bonus (`score_engine.py:3850-3863`, `FERMENTATION_DIRECT_BONUS=8` at `constants.py:122`, markers `CULTURED_CHEESE_NAME_MARKERS_HE` at `constants.py:831`) so it does NOT fire when `context_flag == "brined_food"` (`context_flag` is a first-class engine concept: `score_engine.py:2405`, `:2660`). Implement behind a sub-flag `BARI_FERMENT_MARKER_BRINED_FIX_V1` (default OFF in constants; candidate artifacts built with it ON).
- Product's co-sign conditions are part of the DoD: (a) the engine must now EMIT `fermentation_bonus_applied` (bool) + `fermentation_bonus_note` into every bsip2 trace JSON; (b) full cross-corpus baseline diff (contract Rule 8): flag-OFF must be byte-identical to origin/master baseline across ALL live categories; flag-ON must move ONLY brined_food-context products, downward-only; (c) deliver a brined grade-distribution artifact (min/max/median/stdev/histogram, per Rule 5) before/after.
- Census: how many brined products carry a name marker and lose the +8? Trace-derived count with the deriving command (Rule 6).
- Build the brined candidate page artifact using the ESTABLISHED method (see DISPATCH_BOARD "FIXED via the correct construction method"): start from the exact LIVE `brined_cheeses` frontend JSON on origin/master, swap ONLY score/grade from the new traces, recompute `rank` from the new order, keep live names/copy/schema. Emit the Rule-7 flat verification table (`barcode, score, grade, binding_caps, nova, fat, sodium, context_flag`). Run `python 03_operations\page_generator\gates\run_gates.py` on the candidate; report every gate result. List every product whose rowVerdict/insightLine cites a number or rank that your rescore changed (DO NOT edit copy — Content lane owns copy; just list them).

**Commit 2 — router fix:**
- `router_v2.py` (~line 595): the bread-name term "מלא" outweighs the dairy anchor "חלב", classifying whole milk (7290000051352) as `category: bread` conf 0.68. Fix the term-weight collision so fluid-milk names route dairy. Then prove with a full cross-corpus rescore diff that the fix moves **ZERO scores and ZERO grades** across all live categories (expected: the NOVA-1 floor masks milk; nothing else should shift). If ANY score/grade moves, STOP, do not proceed — report the movement table and propose BLOCKED (that would need a fresh Nutrition D6 ruling).

## 3. Boundaries / guards
- **OFF ban absolute (TASK-238):** no Open Food Facts anywhere — no import, no lookup, no fallback, no "temporary" fill. Unknown stays NULL.
- Do NOT invent nutrition/ingredient data. Do NOT edit any consumer-facing copy string. Do NOT touch scoring weights, caps, or any mechanism beyond the two named fixes. Do NOT flip any other flag.
- Commit locally on the worktree branch; **do NOT push, do NOT open a PR, do NOT deploy** — Content + Adversarial QA gates and the owner sit between you and the site.
- Do not modify the main tree, the registry, or the dispatch board.
- If a step is impossible as specced, stop and return honestly with `proposed_status: BLOCKED` — never approximate around it.

## 4. Return format
Write your return to `C:\Bari\tasks\returns\P459_return.md`: per-commit summary (SHA, files, diff stats), the cross-corpus diff results (both commits), the census + grade-distribution artifacts (paths), gate results, the copy-impact list, and the flat verification table path. **Do not close the task — propose RETURNED** (or BLOCKED per above).

## 5. Machine-readable contract (mandatory, last block of the return)
```json
{
  "task": "P459",
  "proposed_status": "RETURNED | BLOCKED",
  "artifacts": [{"path": "...", "action": "created|modified|deleted", "sha256": "..."}],
  "counts": {"claim": "N/M (denominator source)"},
  "commands_run": [{"cmd": "...", "exit_code": 0}],
  "not_done": [],
  "self_check": "flag-OFF byte-identical to origin/master across all live categories (commit 1) AND zero score/grade movement (commit 2): observed result here"
}
```
Rules 5–8 of `01_framework\operations\return_contract_v1.md` apply: full distributions with stdev, trace-derived counts with the deriving command, the Rule-7 flat table, and the full cross-corpus baseline diff.
