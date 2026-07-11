## Result

For Bari’s current workflows, use Vercel’s native GitHub-check selection—**not** the `repository_dispatch` status action. Both workflows already run on `push` to `master`, so GitHub produces job checks on the deployed SHA. Vercel can require those directly. [Vercel Deployment Checks docs](https://vercel.com/docs/deployment-checks)

One repository discrepancy: `barint_ci.yml` currently defines `frontend`, `python-tests`, and `off-sweep`; it does **not** contain `e2e-smoke`. The requested six-job setup cannot be completed until that job exists or its actual job name is supplied.

### 1. Authentication and minimal snippet

`vercel/repository-dispatch/actions/status@v1` does **not** use `VERCEL_TOKEN`, Vercel org ID, or Vercel project ID. Its manifest exposes `github_token`, defaulting to GitHub Actions’ `${{ github.token }}`. It writes a GitHub status for the deployment SHA received in a `repository_dispatch` event; Vercel then reads that GitHub status. It is not authenticated by the installed Vercel GitHub App. [Action manifest](https://raw.githubusercontent.com/vercel/repository-dispatch/main/actions/status/action.yaml)

Minimal action step, exactly as Vercel documents:

```yaml
- name: Notify Vercel
  uses: vercel/repository-dispatch/actions/status@v1
  with:
    name: "Vercel - bari: e2e-smoke"
```

For an explicit least-privilege workflow declaration, add:

```yaml
permissions:
  statuses: write
```

No `VERCEL_TOKEN` secret is involved. The Vercel documentation’s supplied snippet likewise has only `name`. [Vercel docs](https://vercel.com/docs/deployment-checks)

This action is necessary when a workflow is triggered by `repository_dispatch` (notably `vercel.deployment.ready`), because GitHub otherwise associates that run with the current default-branch SHA rather than the deployment’s SHA. [Vercel GitHub integration docs](https://vercel.com/docs/git/vercel-for-github), [GitHub event reference](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows)

### 2. Empty “Select checks to add”

The documented mechanism is: choose **GitHub** in Deployment Checks, then search/select GitHub Actions checks. Vercel documents neither:

- the data source or retention window for that picker,
- whether it requires a prior observed check on a deployed commit, nor
- that adding the status-action snippet and pushing once will populate it.

So the proposed “add snippet, make one `master` push, then the list populates” is plausible but **not documented and cannot be stated as fact**.

What is documented precisely:

- GitHub Actions job results can be selected directly as Deployment Checks.
- The status action is required for `repository_dispatch`-triggered workflows.
- If a workflow is not using `repository_dispatch`, the status action is optional and Vercel can depend on the GitHub check directly. [Vercel Deployment Checks docs](https://vercel.com/docs/deployment-checks)

Therefore the snippet is **not** the only path, and it should not be added merely to work around an empty picker for these normal `push` workflows.

### 3. Correct Bari wiring and fail-closed behavior

Use one directly selected Vercel Deployment Check for each required GitHub Actions **job**:

- `frontend`
- `python-tests`
- `off-sweep`
- `e2e-smoke` — after it actually exists
- `conformance`
- `off-ban-census`

Do not aggregate unless the product requirement intentionally changes from “every underlying job is independently required” to “one aggregate result is required.” An aggregate can hide a skipped or omitted upstream job unless its own logic explicitly rejects every non-success result.

No status-action steps are needed in either present workflow. Their existing `push: branches: [master]` triggers are important: Vercel evaluates the deployed commit, so these jobs must run on that exact `master` SHA.

A check becomes a promotion gate only after it is added/selected in Vercel. Vercel says it holds production deployments until all required checks pass; a selected failure therefore prevents automatic alias promotion, although a user can **Force Promote** from deployment details. [Vercel Deployment Checks docs](https://vercel.com/docs/deployment-checks)

Vercel’s GitHub-check documentation does **not** specify the Deployment Checks result for a GitHub job reported as `skipped`. It only says GitHub-backed behavior follows GitHub’s status-reporting behavior. Do not rely on “skipped blocks” as a safety property. Make each required job run on every `master` push; if conditional execution is unavoidable, use a separate always-running gate job that explicitly fails unless every required upstream job result is `success`.

### 4. Paid-tier gate

No paid-tier requirement is documented. Vercel’s launch announcement says GitHub-based deployment checks are available for **all projects**, and the current Deployment Checks documentation lists GitHub connection and automatic production aliasing as prerequisites, not a plan. [Vercel announcement](https://vercel.com/changelog/block-vercel-deployment-promotions-with-github-actions), [Vercel Deployment Checks docs](https://vercel.com/docs/deployment-checks)

## Owner and workflow-editor handoff

1. Confirm the project is linked to the correct GitHub repository in **Project → Settings → Git**.
2. In **Project → Settings → Environments → Production**, leave **Automatic Aliasing** enabled.
3. Ensure every required job runs on every `master` push. In the current repository, add/restore `e2e-smoke` before treating it as required.
4. Push a normal `master` commit and allow the Vercel production deployment and both CI workflows to complete.
5. Open **Project → Settings → Deployment Checks → Add Checks → GitHub**.
6. Search/select the exact six job-check names above. This is the required action that turns observed GitHub checks into Vercel promotion gates.
7. Make a harmless follow-up `master` push. Verify the production deployment remains unaliased until every selected check succeeds, then aliases to `bari.digital`.
8. If the selector remains empty after a completed production deployment and completed `master` workflow runs, do not add the snippet as a speculative workaround. Capture the deployment URL/SHA and contact Vercel support; the public docs do not explain that picker’s discovery failure.

No files changed. Verify the existing master-push triggers in [.github/workflows/barint_ci.yml](C:\Bari\.github\workflows\barint_ci.yml:14) and [.github/workflows/bari_page_gates.yml](C:\Bari\.github\workflows\bari_page_gates.yml:18), plus the absence of `e2e-smoke` in the former.

```json
{
  "task": "TASK-603",
  "proposed_status": "RETURNED",
  "artifacts": [],
  "counts": {
    "workflow_jobs_inspected": "5/2 workflow files (.github/workflows/barint_ci.yml and .github/workflows/bari_page_gates.yml)"
  },
  "commands_run": [
    {
      "cmd": "Get-Content -Raw 01_framework/operations/return_contract_v1.md",
      "exit_code": 0
    },
    {
      "cmd": "Get-Content -Raw .github/workflows/barint_ci.yml; Get-Content -Raw .github/workflows/bari_page_gates.yml",
      "exit_code": 0
    }
  ],
  "not_done": [],
  "self_check": "Read-only research completed: current Vercel Deployment Checks documentation and the official action manifest were inspected; no repository files were modified."
}
```


--- STDERR ---
OpenAI Codex v0.144.1
--------
workdir: C:\Bari
model: gpt-5.6-terra
provider: openai
approval: never
sandbox: read-only
reasoning effort: low
reasoning summaries: none
session id: 019f4fbb-60b8-71c3-96e5-af6564a152fa
--------
user
TASK-603 ENGINEERING-RESEARCH (read-only, web search). Determine the EXACT current (2026) Vercel mechanism to gate production-alias promotion on GitHub Actions job results. Observed: Vercel project Deployment Checks shows a Connect GitHub Actions dialog with (a) a snippet step  uses: vercel/repository-dispatch/actions/status@v1  with  name: Vercel - <proj>: <check>  and (b) an EMPTY Select checks to add list (our 6 GitHub Actions jobs do not appear).

Answer precisely with Vercel doc URLs:
1. Does vercel/repository-dispatch/actions/status@v1 need a VERCEL_TOKEN secret (+ ORG/PROJECT IDs) or does it auth via the installed Vercel GitHub app with no secret? Give the minimal correct step YAML.
2. Why is Select checks to add empty - does it only list checks Vercel already observed on a deployed commit, and does adding the snippet + one master push populate it, or is the snippet the ONLY path for GitHub Actions jobs (no ticking)?
3. For 6 jobs across 2 workflow files (barint_ci.yml: frontend, python-tests, off-sweep, e2e-smoke; bari_page_gates.yml: conformance, off-ban-census) that must ALL pass before bari.digital promotes: correct minimal wiring - one status step per job or one aggregating job? Does a failed/skipped reported check block promotion fail-closed, or must it be explicitly required?
4. Any paid-tier gate on Deployment Checks / this snippet?
Deliverable: step-by-step for the repo owner + a workflow editor, exact YAML + exact remaining Vercel dashboard clicks, sources cited. Where docs are ambiguous, say so - do not guess.
codex
I’ll verify this against current Vercel documentation and the action’s authoritative source, keeping the answer strictly read-only and flagging any ambiguity.
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command 'Get-Content -Raw 01_framework/operations/return_contract_v1.md' in C:\Bari
 succeeded in 1413ms:
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
   and source. A number with no artifact behind it is not a claim â€” omit it.
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
   Exit != 0 â†’ automatic CHANGES_REQUESTED. Self-test: `validate_return.py --selftest`.

## Verification-hardening requirements (owner-directed 2026-06-13)

*Added after return-block COUNTS proved untrustworthy: a scoring run reported
`HP_FAT_SODIUM 0/48` when it was **48/48**, and a "4/4 acceptance pairs pass" masked a
**31-product score collapse**. Self-reported numbers are not evidence. These make returns
self-verifying instead of forcing the orchestrator to re-derive everything by hand.*

5. **Full distributions, never example counts.** Any return reporting on a SET (scores,
   grades, products) MUST give the full distribution â€” histogram, min/max/median,
   **stdev**, and the **most-common-value count** â€” not a hand-picked sample of N passing
   examples. "4/4 pairs pass" is rejected; `grade_dist + stdev + most_common_score(count)`
   is required. A collapse is invisible in a sampled acceptance test and obvious in a
   distribution (the 72-pin would have shown in the agent's *own* return).
6. **Counts must be trace-derived, with the derivation shown.** Every number in `counts`
   is computed from the committed artifacts (traces/JSON), and the deriving command goes
   in `commands_run`. A counter read from an in-memory variable or a summary field is NOT
   trustworthy â€” summary counters have been wrong twice. If the orchestrator cannot re-run
   the command and reproduce the number, the count is unverified.
7. **Scoring runs emit a stable verification artifact.** Every scoring/re-scoring run
   writes one flat machine-readable table â€”
   `barcode, score, grade, binding_caps, nova, fat, sodium, context_flag` â€” at a
   predictable path. Verification becomes one query against a known schema, not a bespoke
   parser per run (trace keys have drifted: `grade` vs `grade_estimate` vs
   `final_score_estimate`).
8. **Scope/keyword/routing/flag changes require a full cross-corpus baseline diff â€” from
   the FIRST one.** Re-score EVERY corpus (all published categories + the target) and diff
   against a committed baseline. The invariant/property suite is NOT sufficient â€” it checks
   properties, not byte-identity; a keyword add can silently rescore products in OTHER
   corpora (EV-052 moved 18 products in maadanim/hard_cheeses, caught two stages late).
   The cross-corpus byte-diff is mandatory on the first such change, not after a surprise.
9. **Any artifact under `.claude/` is a CRITICAL finding, not a routine one (Guard C7).**
   Project-local config (hooks/agents/skills/settings) executes with the orchestrator's own
   authority the next time the project loads â€” a pre-trust attack surface (containment
   doctrine: Anthropic, "How we contain Claude across products", 2026-05). `validate_return.py`
   flags it distinctly from an ordinary schema/count failure; the orchestrator reads that
   file's diff directly before accept/reject â€” it is never auto-bounced as CHANGES_REQUESTED
   without a human look.


web search: 
web search: site:vercel.com/docs deployment checks GitHub Actions repository-dispatch actions status v1 ...
web search: 
web search: 
web search: 
web search: https://raw.githubusercontent.com/vercel/repository-dispatch/main/actions/status/action.yml
web search: 
web search: 
web search: 
web search: "vercel/repository-dispatch/actions/status@v1" "token" ...
web search: 
web search: repo:vercel/repository-dispatch github_token status action.yml ...
web search: 
web search: https://github.com/vercel/repository-dispatch/tree/v1/actions/status
web search: 
web search: Vercel "Select checks to add" ...
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command 'Get-Content -Raw .github/workflows/barint_ci.yml; Get-Content -Raw .github/workflows/bari_page_gates.yml' in C:\Bari
 succeeded in 787ms:
name: CI â€” Barint

on:
  pull_request:
    paths:
      - "bari-web/src/**"
      - "bari-web/scripts/**"
      - "bari-web/package.json"
      - "bari-web/next.config.ts"
      - "bari-web/tsconfig.json"
      - "bari-web/eslint.config.mjs"
      - "03_operations/**"
      - ".github/workflows/barint_ci.yml"
      - ".github/workflows/argento_bari_ci.yml"
  push:
    branches: [master]
  workflow_dispatch: {}

jobs:
  frontend:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: bari-web
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: "20"
          cache: npm
          cache-dependency-path: bari-web/package-lock.json

      - name: Install deps
        run: npm ci

      - name: TypeScript + Next build
        run: npm run build

      - name: ESLint
        run: npm run lint

      - name: Validate corpus (all datasets, error mode)
        run: node scripts/validate-corpus.mjs --all --handoff

  python-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install deps
        run: pip install pytest beautifulsoup4 lxml

      - name: BSIP0 nutrition tests (20)
        run: python -m pytest 03_operations/bsip0/scrape/_shared/test_bsip0_nutrition.py -v --tb=short

      - name: BSIP1 enricher tests (64)
        run: python 03_operations/bsip1/core/test_enricher.py

      - name: Router regression
        run: python 03_operations/bsip2/proto_v0/src/run_router_regression.py

      - name: Scoring regression (golden corpus)
        run: python 03_operations/bsip2/proto_v0/src/run_regression_check.py

      - name: BSIP0 QA validator tests
        run: python -m pytest 03_operations/bsip0/validators/test_bsip0_qa_validator.py -v --tb=short

      - name: BSIP0 exit gate tests (30)
        run: python -m pytest 03_operations/bsip0/scrape/_shared/test_bsip0_gate.py -v --tb=short

      - name: BSIP0 exit gate â€” live corpus check
        run: python 03_operations/bsip0/scrape/_shared/bsip0_gate.py 02_products/breakfast_cereals/bsip0_outputs/cereals_bsip0_raw_20260601T152207.json || true

      - name: Spine smoke manifest dry-run (TASK-290)
        run: python 03_operations/spine/smoke_test.py --dry-run

  off-sweep:
    # TASK-238 â€” OFF is BANNED project-wide. Fail if any Open-Food-Facts marker
    # appears in the frontend data directory (bari-web/src/data/).
    # Mechanises the manual Phase-J check from the QA checklist.
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: OFF-string sweep (bari-web/src/data/)
        run: |
          if grep -riE \
            "openfoodfacts|open_food_facts|off_api|off_candidate_panel|openfoodfacts\.org" \
            bari-web/src/data/; then
            echo "::error::Banned Open-Food-Facts marker found in bari-web/src/data/ (TASK-238). Remove before merge."
            exit 1
          fi
          echo "OFF sweep CLEAN â€” no banned markers found."

# Bari page-gate battery (TASK-505) â€” CI-resident deterministic gates.
# Runs the spine conformance sweep + an OFF-ban census on every PR that touches
# comparison data or the page generator. These gates already exist locally; this
# workflow makes them fire even when nobody remembers to run them (audit finding:
# "everything fires interactively only").
name: Bari Page Gates

on:
  pull_request:
    paths:
      - "bari-web/src/data/comparisons/**"
      - "bari-web/src/data/seo/**"
      - "03_operations/page_generator/**"
      - "03_operations/spine/**"
      - "02_products/**"
      - ".github/workflows/bari_page_gates.yml"
  push:
    branches: [master]
  workflow_dispatch: {}

jobs:
  conformance:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Spine conformance sweep (every category must re-flow)
        run: python 03_operations/page_generator/conformance.py --all

  off-ban-census:
    # OFF is banned project-wide (CLAUDE.md hard rule, TASK-238). Any OFF reference
    # reaching consumer-facing data or site source is a launch blocker.
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Census â€” no OFF references in site source or comparison data
        run: |
          set -e
          MATCHES=$(grep -rniE "openfoodfacts" bari-web/src/ 2>/dev/null | grep -viE "banned|forbidden|do not use|never use" || true)
          if [ -n "$MATCHES" ]; then
            echo "OFF-ban violation(s) found (launch blocker, TASK-238):"
            echo "$MATCHES"
            exit 1
          fi
          echo "OFF census clean: no Open Food Facts references in bari-web/src/."


web search: 
web search: https://raw.githubusercontent.com/vercel/repository-dispatch/main/actions/status/action.yaml
web search: 
web search: https://raw.githubusercontent.com/vercel/repository-dispatch/main/actions/status/src/main.ts
codex
## Result

For Bari’s current workflows, use Vercel’s native GitHub-check selection—**not** the `repository_dispatch` status action. Both workflows already run on `push` to `master`, so GitHub produces job checks on the deployed SHA. Vercel can require those directly. [Vercel Deployment Checks docs](https://vercel.com/docs/deployment-checks)

One repository discrepancy: `barint_ci.yml` currently defines `frontend`, `python-tests`, and `off-sweep`; it does **not** contain `e2e-smoke`. The requested six-job setup cannot be completed until that job exists or its actual job name is supplied.

### 1. Authentication and minimal snippet

`vercel/repository-dispatch/actions/status@v1` does **not** use `VERCEL_TOKEN`, Vercel org ID, or Vercel project ID. Its manifest exposes `github_token`, defaulting to GitHub Actions’ `${{ github.token }}`. It writes a GitHub status for the deployment SHA received in a `repository_dispatch` event; Vercel then reads that GitHub status. It is not authenticated by the installed Vercel GitHub App. [Action manifest](https://raw.githubusercontent.com/vercel/repository-dispatch/main/actions/status/action.yaml)

Minimal action step, exactly as Vercel documents:

```yaml
- name: Notify Vercel
  uses: vercel/repository-dispatch/actions/status@v1
  with:
    name: "Vercel - bari: e2e-smoke"
```

For an explicit least-privilege workflow declaration, add:

```yaml
permissions:
  statuses: write
```

No `VERCEL_TOKEN` secret is involved. The Vercel documentation’s supplied snippet likewise has only `name`. [Vercel docs](https://vercel.com/docs/deployment-checks)

This action is necessary when a workflow is triggered by `repository_dispatch` (notably `vercel.deployment.ready`), because GitHub otherwise associates that run with the current default-branch SHA rather than the deployment’s SHA. [Vercel GitHub integration docs](https://vercel.com/docs/git/vercel-for-github), [GitHub event reference](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows)

### 2. Empty “Select checks to add”

The documented mechanism is: choose **GitHub** in Deployment Checks, then search/select GitHub Actions checks. Vercel documents neither:

- the data source or retention window for that picker,
- whether it requires a prior observed check on a deployed commit, nor
- that adding the status-action snippet and pushing once will populate it.

So the proposed “add snippet, make one `master` push, then the list populates” is plausible but **not documented and cannot be stated as fact**.

What is documented precisely:

- GitHub Actions job results can be selected directly as Deployment Checks.
- The status action is required for `repository_dispatch`-triggered workflows.
- If a workflow is not using `repository_dispatch`, the status action is optional and Vercel can depend on the GitHub check directly. [Vercel Deployment Checks docs](https://vercel.com/docs/deployment-checks)

Therefore the snippet is **not** the only path, and it should not be added merely to work around an empty picker for these normal `push` workflows.

### 3. Correct Bari wiring and fail-closed behavior

Use one directly selected Vercel Deployment Check for each required GitHub Actions **job**:

- `frontend`
- `python-tests`
- `off-sweep`
- `e2e-smoke` — after it actually exists
- `conformance`
- `off-ban-census`

Do not aggregate unless the product requirement intentionally changes from “every underlying job is independently required” to “one aggregate result is required.” An aggregate can hide a skipped or omitted upstream job unless its own logic explicitly rejects every non-success result.

No status-action steps are needed in either present workflow. Their existing `push: branches: [master]` triggers are important: Vercel evaluates the deployed commit, so these jobs must run on that exact `master` SHA.

A check becomes a promotion gate only after it is added/selected in Vercel. Vercel says it holds production deployments until all required checks pass; a selected failure therefore prevents automatic alias promotion, although a user can **Force Promote** from deployment details. [Vercel Deployment Checks docs](https://vercel.com/docs/deployment-checks)

Vercel’s GitHub-check documentation does **not** specify the Deployment Checks result for a GitHub job reported as `skipped`. It only says GitHub-backed behavior follows GitHub’s status-reporting behavior. Do not rely on “skipped blocks” as a safety property. Make each required job run on every `master` push; if conditional execution is unavoidable, use a separate always-running gate job that explicitly fails unless every required upstream job result is `success`.

### 4. Paid-tier gate

No paid-tier requirement is documented. Vercel’s launch announcement says GitHub-based deployment checks are available for **all projects**, and the current Deployment Checks documentation lists GitHub connection and automatic production aliasing as prerequisites, not a plan. [Vercel announcement](https://vercel.com/changelog/block-vercel-deployment-promotions-with-github-actions), [Vercel Deployment Checks docs](https://vercel.com/docs/deployment-checks)

## Owner and workflow-editor handoff

1. Confirm the project is linked to the correct GitHub repository in **Project → Settings → Git**.
2. In **Project → Settings → Environments → Production**, leave **Automatic Aliasing** enabled.
3. Ensure every required job runs on every `master` push. In the current repository, add/restore `e2e-smoke` before treating it as required.
4. Push a normal `master` commit and allow the Vercel production deployment and both CI workflows to complete.
5. Open **Project → Settings → Deployment Checks → Add Checks → GitHub**.
6. Search/select the exact six job-check names above. This is the required action that turns observed GitHub checks into Vercel promotion gates.
7. Make a harmless follow-up `master` push. Verify the production deployment remains unaliased until every selected check succeeds, then aliases to `bari.digital`.
8. If the selector remains empty after a completed production deployment and completed `master` workflow runs, do not add the snippet as a speculative workaround. Capture the deployment URL/SHA and contact Vercel support; the public docs do not explain that picker’s discovery failure.

No files changed. Verify the existing master-push triggers in [.github/workflows/barint_ci.yml](C:\Bari\.github\workflows\barint_ci.yml:14) and [.github/workflows/bari_page_gates.yml](C:\Bari\.github\workflows\bari_page_gates.yml:18), plus the absence of `e2e-smoke` in the former.

```json
{
  "task": "TASK-603",
  "proposed_status": "RETURNED",
  "artifacts": [],
  "counts": {
    "workflow_jobs_inspected": "5/2 workflow files (.github/workflows/barint_ci.yml and .github/workflows/bari_page_gates.yml)"
  },
  "commands_run": [
    {
      "cmd": "Get-Content -Raw 01_framework/operations/return_contract_v1.md",
      "exit_code": 0
    },
    {
      "cmd": "Get-Content -Raw .github/workflows/barint_ci.yml; Get-Content -Raw .github/workflows/bari_page_gates.yml",
      "exit_code": 0
    }
  ],
  "not_done": [],
  "self_check": "Read-only research completed: current Vercel Deployment Checks documentation and the official action manifest were inspected; no repository files were modified."
}
```
tokens used
130,499
