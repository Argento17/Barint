# TASK-461 Exec-A Return Report
**Date:** 2026-07-03  
**Agent:** git-execution lane (Claude Fable 5 / Sonnet 4.6)  
**Worktree:** C:\bari_wt_t461x_a (base commit 06f85de4)  
**Scope:** Batch A — cheese, choctab, snacks, juices

---

## Overall Result: 4/4 PASS

---

## Category 1: Cheese

**Branch:** `content/task461-cheese-copy-overhaul`  
**Commit:** `747ce951c74375e5e6e198dea0cf71a3402da3c1`  
**Target:** `bari-web/src/data/comparisons/cheese_frontend_v5.json`

### Artifact SHA256 Verification
- Stated: `0a490cc55d8ba78e4859da67600eca1293e165251d9a8fac7ef231938cabf4ab`
- Computed (Get-FileHash): `0A490CC55D8BA78E4859DA67600ECA1293E165251D9A8FAC7EF231938CABF4AB`
- Committed blob (git cat-file | sha256): `0a490cc55d8ba78e4859da67600eca1293e165251d9a8fac7ef231938cabf4ab`
- **MATCH: YES**

### Baseline Blob Verification
- Stated: `deec2e91…`
- Computed (git hash-object): `deec2e911cb369444f7bec796ff468220b75c37a`
- **MATCH: YES**

### Isolation Proof (independent Python script: isolation_proof.py)
- Baseline product count: 47 / New file product count: 47
- Top-level fields (non-products) unchanged: OK
- Products with changes: **47/47**
- Total changed leaves: **94** (insightLine + rowVerdict per product, 2×47)
- Violations (leaves outside allowed set): **0**
- PASS

### Gate Results
- Baseline run: **Overall PASS** (G2/G3/G5 WARN only — no corpus/run, expected for copy-only)
- Candidate run with --baseline: **Overall PASS**
- G1 SCHEMA: PASS (cheese file has no TASK-453 schema debt)
- G4 OFF: PASS
- G6 COPY-SAFETY: PASS
- G7 PARITY: PASS — 47/47 products, 0 grade changes, image coverage 100% unchanged
- G8 DATA-SANITY: PASS

### Build Oracle
- `npx tsc --noEmit`: exit 0
- `npm run build`: exit 0

---

## Category 2: Chocolate Tablets (choctab)

**Branch:** `content/task461-choctab-copy-overhaul`  
**Commit:** `9a9a33b15843defeff2dabf76a61fd3c89293f13`  
**Target:** `bari-web/src/data/comparisons/chocolate_tablets_frontend_v1.json`

### Artifact SHA256 Verification
- Stated: `c03cc84fccd91b8ac8d5e7aecfb55eb6dad2c2d3e57568cf7ac91144172d1236`
- Computed: `C03CC84FCCD91B8AC8D5E7AECFB55EB6DAD2C2D3E57568CF7AC91144172D1236`
- Committed blob: `c03cc84fccd91b8ac8d5e7aecfb55eb6dad2c2d3e57568cf7ac91144172d1236`
- **MATCH: YES**

### Baseline Blob Verification
- Stated: `45c962fe…`
- Computed: `45c962fe990ca21be87320b3f65cbc4982803869`
- **MATCH: YES**

### Isolation Proof
- Products: 35/35
- Changed leaves: **70** (2×35)
- Violations: **0**
- PASS

### Gate Results
- G1 SCHEMA: **FAIL (baseline)** / **FAIL (candidate)** — pre-existing TASK-453 debt
  - Baseline fail count: 21 FAIL lines
  - Candidate fail count: 21 FAIL lines
  - Diff: **EMPTY** — fail sets IDENTICAL (proven by sorted Compare-Object)
  - PASS criterion met per procedure: "any failing set identical between baseline-run and candidate-run"
- G4 OFF: PASS
- G6 COPY-SAFETY: PASS
- G7 PARITY: PASS — 35/35 products, 0 grade changes, image coverage 100%
- G8 DATA-SANITY: PASS

### Build Oracle
- `npx tsc --noEmit`: exit 0
- `npm run build`: exit 0

### Additional Artifact
- QA report copied to: `02_products/chocolate/reports/red_team_tablets_2026-07-03.md`
- sha256: `94164244de7db70abf1e415b84ceb183e2d9f4dd3d8c520fcee1810800fa4545`
- (New directory created: `02_products/chocolate/reports/`)

---

## Category 3: Snacks

**Branch:** `content/task461-snacks-copy-overhaul`  
**Commit:** `6b8f2286ffa2dd91e6cbc114d142cf2db0e66bb1`  
**Target:** `bari-web/src/data/comparisons/snacks_frontend_v5.json`

### Artifact SHA256 Verification
- Stated: `406d8363e40aa2d7473881b152b98ddd2fff16268c9622ee4d770530b5e968a8`
- Computed: `406D8363E40AA2D7473881B152B98DDD2FFF16268C9622EE4D770530B5E968A8`
- Committed blob: `406d8363e40aa2d7473881b152b98ddd2fff16268c9622ee4d770530b5e968a8`
- **MATCH: YES**

### Baseline Blob Verification
- Stated: `4febff7b…`
- Computed: `4febff7befeed04274ae00113ea3de6ba771506c`
- **MATCH: YES**

### Isolation Proof
- Products: 21/21
- Changed leaves: **42** (2×21)
- Violations: **0**
- PASS

### Gate Results
- G1 SCHEMA: **FAIL (baseline)** / **FAIL (candidate)** — pre-existing TASK-453 debt
  - Baseline fail count: 21 FAIL lines
  - Candidate fail count: 21 FAIL lines
  - Diff: **EMPTY** — fail sets IDENTICAL
  - PASS criterion met
- G4 OFF: PASS
- G6 COPY-SAFETY: PASS
- G7 PARITY: PASS — 21/21 products, 0 grade changes, image coverage 100%
- G8 DATA-SANITY: PASS

### Build Oracle
- `npx tsc --noEmit`: exit 0
- `npm run build`: exit 0

### Additional Artifact
- QA report copied to: `02_products/snack_bars/reports/red_team_snacks_2026-07-03.md`
- sha256: `1daa459aac21b9af77bac673963f3f9e19412dd0a90426fc69cd2377da973424`
- Note: no `02_products/snacks/` directory exists; placed in `02_products/snack_bars/reports/` (the owning category directory for snacks_frontend_v5.json)

---

## Category 4: Juices

**Branch:** `content/task461-juices-copy-overhaul`  
**Commit:** `f071524292f99a9421e46a7919ae0e9232296e86`  
**Target:** `bari-web/src/data/comparisons/juices_frontend_v3.json`

### Artifact SHA256 Verification
- Stated: `9ba0dbcab35dc36774c6116f90befee85eb23c5002a64c4af5a66fba0ccc3ad9`
- Computed: `9BA0DBCAB35DC36774C6116F90BEFEE85EB23C5002A64C4AF5A66FBA0CCC3AD9`
- Committed blob: `9ba0dbcab35dc36774c6116f90befee85eb23c5002a64c4af5a66fba0ccc3ad9`
- **MATCH: YES**

### Baseline Blob Verification
- Stated: `95c42010…`
- Computed: `95c42010dd40a3bada829e0e6efcd88c6d802f09`
- **MATCH: YES**

### Isolation Proof (scope exception applied)
- Products: 17/17
- Changed leaves: **36 total**
  - 34 = insightLine + rowVerdict on all 17 products (standard)
  - 2 = expansion.comparisonContext on jc-021 and jc-024 only (orchestrator-authorized)
- comparisonContext change products verified: `['jc-021', 'jc-024']` — exactly the authorized set
- Violations (outside authorized surface): **0**
- PASS

### Gate Results
- G1 SCHEMA: **FAIL (baseline)** / **FAIL (candidate)** — pre-existing TASK-453 debt
  - Baseline fail count: 21 FAIL lines
  - Candidate fail count: 21 FAIL lines
  - Diff: **EMPTY** — fail sets IDENTICAL
  - PASS criterion met
- G4 OFF: PASS
- G6 COPY-SAFETY: PASS
- G7 PARITY: PASS — 17/17 products, 0 grade changes, image coverage 100%
- G8 DATA-SANITY: PASS

### Build Oracle
- `npx tsc --noEmit`: exit 0
- `npm run build`: exit 0

### Additional Artifact
- QA report copied to: `02_products/juices/reports/red_team_juices_2026-07-03.md`
- sha256: `05b19ba5162b9d7952c8d2973ee1aaf2add5c6505a619b959b5be835dbfd950c`

---

## Cross-Category Notes

### G1 Schema Debt (TASK-453)
Three categories (choctab, snacks, juices) have pre-existing G1 SCHEMA fails in their baseline. These are NOT introduced by this changeset. Proof: sorted diff of FAIL lines between baseline and candidate runs = empty for all three. The debt is from extra fields (`limitingFactors` as objects, `cosmetic_mup`, `name_he`, `image_url`, `nutrition_per_100g`, `_scoring_trace`, `volumeMl`, `satFat`, `_d4_copy_flag`) present in the baseline files, routed to TASK-453.

### Cheese G1 PASS
Cheese baseline passes G1 cleanly — no TASK-453 debt in that file.

### Build oracle run order
node_modules copied once from C:\Bari\bari-web\node_modules via robocopy (650 entries match). tsc + build run once per category branch in sequence. All exits 0.

### Isolation proof tool
`C:\bari_wt_t461x_a\isolation_proof.py` — written fresh, independent of handover docs. Derives counts from `git show 06f85de4:...` (live baseline git object) vs the artifact file. sha256: `d29dda5e09722f93e66caf3dc12c136ecda9604f16516ede21c904310d3cf840`.

---

```json
{
  "task": "TASK-461",
  "proposed_status": "RETURNED",
  "artifacts": [
    {"path": "bari-web/src/data/comparisons/cheese_frontend_v5.json", "action": "modified", "sha256": "0a490cc55d8ba78e4859da67600eca1293e165251d9a8fac7ef231938cabf4ab"},
    {"path": "bari-web/src/data/comparisons/chocolate_tablets_frontend_v1.json", "action": "modified", "sha256": "c03cc84fccd91b8ac8d5e7aecfb55eb6dad2c2d3e57568cf7ac91144172d1236"},
    {"path": "02_products/chocolate/reports/red_team_tablets_2026-07-03.md", "action": "created", "sha256": "94164244de7db70abf1e415b84ceb183e2d9f4dd3d8c520fcee1810800fa4545"},
    {"path": "bari-web/src/data/comparisons/snacks_frontend_v5.json", "action": "modified", "sha256": "406d8363e40aa2d7473881b152b98ddd2fff16268c9622ee4d770530b5e968a8"},
    {"path": "02_products/snack_bars/reports/red_team_snacks_2026-07-03.md", "action": "created", "sha256": "1daa459aac21b9af77bac673963f3f9e19412dd0a90426fc69cd2377da973424"},
    {"path": "bari-web/src/data/comparisons/juices_frontend_v3.json", "action": "modified", "sha256": "9ba0dbcab35dc36774c6116f90befee85eb23c5002a64c4af5a66fba0ccc3ad9"},
    {"path": "02_products/juices/reports/red_team_juices_2026-07-03.md", "action": "created", "sha256": "05b19ba5162b9d7952c8d2973ee1aaf2add5c6505a619b959b5be835dbfd950c"}
  ],
  "counts": {
    "cheese_products_changed": "47/47 (isolation_proof.py vs git show 06f85de4:cheese_frontend_v5.json)",
    "cheese_changed_leaves": "94/94 expected (2 per product × 47, isolation_proof.py trace)",
    "cheese_violations": "0/47 (isolation_proof.py: zero forbidden-field changes)",
    "cheese_grade_changes": "0/47 (G7 PARITY, run_gates.py --baseline)",
    "choctab_products_changed": "35/35 (isolation_proof.py vs git show 06f85de4:chocolate_tablets_frontend_v1.json)",
    "choctab_changed_leaves": "70/70 expected (2 per product × 35, isolation_proof.py trace)",
    "choctab_violations": "0/35 (isolation_proof.py: zero forbidden-field changes)",
    "choctab_grade_changes": "0/35 (G7 PARITY, run_gates.py --baseline)",
    "choctab_g1_fail_diff": "0 lines diff between baseline and candidate fail-sets (sorted Compare-Object)",
    "snacks_products_changed": "21/21 (isolation_proof.py vs git show 06f85de4:snacks_frontend_v5.json)",
    "snacks_changed_leaves": "42/42 expected (2 per product × 21, isolation_proof.py trace)",
    "snacks_violations": "0/21 (isolation_proof.py: zero forbidden-field changes)",
    "snacks_grade_changes": "0/21 (G7 PARITY, run_gates.py --baseline)",
    "snacks_g1_fail_diff": "0 lines diff between baseline and candidate fail-sets (sorted Compare-Object)",
    "juices_products_changed": "17/17 (isolation_proof.py vs git show 06f85de4:juices_frontend_v3.json)",
    "juices_changed_leaves": "36/36 authorized (34 insightLine+rowVerdict + 2 expansion.comparisonContext on jc-021,jc-024, isolation_proof.py trace + comparisonContext dedicated check)",
    "juices_comparisonContext_ids": "2/2 authorized (jc-021, jc-024 only — dedicated check script)",
    "juices_violations": "0/17 (isolation_proof.py: zero forbidden-field changes)",
    "juices_grade_changes": "0/17 (G7 PARITY, run_gates.py --baseline)",
    "juices_g1_fail_diff": "0 lines diff between baseline and candidate fail-sets (sorted Compare-Object)",
    "tsc_exit_codes": "0/0/0/0 (cheese/choctab/snacks/juices, each branch)",
    "build_exit_codes": "0/0/0/0 (cheese/choctab/snacks/juices, each branch)"
  },
  "commands_run": [
    {"cmd": "Get-FileHash C:\\Bari\\tasks\\returns\\TASK-461_cheese_v5_copy_overhaul.json -Algorithm SHA256", "exit_code": 0},
    {"cmd": "Get-FileHash C:\\Bari\\tasks\\returns\\TASK-461_choctab_copy_overhaul.json -Algorithm SHA256", "exit_code": 0},
    {"cmd": "Get-FileHash C:\\Bari\\tasks\\returns\\TASK-461_snacks_copy_overhaul.json -Algorithm SHA256", "exit_code": 0},
    {"cmd": "Get-FileHash C:\\Bari\\tasks\\returns\\TASK-461_juices_copy_overhaul.json -Algorithm SHA256", "exit_code": 0},
    {"cmd": "cd C:\\bari_wt_t461x_a; git checkout -b content/task461-cheese-copy-overhaul 06f85de4", "exit_code": 0},
    {"cmd": "python isolation_proof.py cheese bari-web/src/data/comparisons/cheese_frontend_v5.json C:\\Bari\\tasks\\returns\\TASK-461_cheese_v5_copy_overhaul.json insightLine,rowVerdict", "exit_code": 0},
    {"cmd": "python 03_operations/page_generator/gates/run_gates.py C:\\Temp\\cheese_baseline.json", "exit_code": 0},
    {"cmd": "python 03_operations/page_generator/gates/run_gates.py C:\\Temp\\cheese_candidate.json --baseline C:\\Temp\\cheese_baseline.json", "exit_code": 0},
    {"cmd": "npx tsc --noEmit (cheese branch)", "exit_code": 0},
    {"cmd": "npm run build (cheese branch)", "exit_code": 0},
    {"cmd": "git commit -F C:\\Temp\\commit_msg.txt (cheese)", "exit_code": 0},
    {"cmd": "cd C:\\bari_wt_t461x_a; git checkout -b content/task461-choctab-copy-overhaul 06f85de4", "exit_code": 0},
    {"cmd": "python isolation_proof.py choctab bari-web/src/data/comparisons/chocolate_tablets_frontend_v1.json C:\\Bari\\tasks\\returns\\TASK-461_choctab_copy_overhaul.json insightLine,rowVerdict", "exit_code": 0},
    {"cmd": "Compare-Object sorted FAIL lines choctab baseline vs candidate (21 vs 21, diff empty)", "exit_code": 0},
    {"cmd": "npx tsc --noEmit (choctab branch)", "exit_code": 0},
    {"cmd": "npm run build (choctab branch)", "exit_code": 0},
    {"cmd": "git commit -F C:\\Temp\\commit_msg.txt (choctab)", "exit_code": 0},
    {"cmd": "cd C:\\bari_wt_t461x_a; git checkout -b content/task461-snacks-copy-overhaul 06f85de4", "exit_code": 0},
    {"cmd": "python isolation_proof.py snacks bari-web/src/data/comparisons/snacks_frontend_v5.json C:\\Bari\\tasks\\returns\\TASK-461_snacks_copy_overhaul.json insightLine,rowVerdict", "exit_code": 0},
    {"cmd": "Compare-Object sorted FAIL lines snacks baseline vs candidate (21 vs 21, diff empty)", "exit_code": 0},
    {"cmd": "npx tsc --noEmit (snacks branch)", "exit_code": 0},
    {"cmd": "npm run build (snacks branch)", "exit_code": 0},
    {"cmd": "git commit -F C:\\Temp\\commit_msg.txt (snacks)", "exit_code": 0},
    {"cmd": "cd C:\\bari_wt_t461x_a; git checkout -b content/task461-juices-copy-overhaul 06f85de4", "exit_code": 0},
    {"cmd": "python isolation_proof.py juices bari-web/src/data/comparisons/juices_frontend_v3.json C:\\Bari\\tasks\\returns\\TASK-461_juices_copy_overhaul.json insightLine,rowVerdict jc-021,jc-024", "exit_code": 0},
    {"cmd": "python -c comparisonContext dedicated check (jc-021, jc-024 only confirmed)", "exit_code": 0},
    {"cmd": "Compare-Object sorted FAIL lines juices baseline vs candidate (21 vs 21, diff empty)", "exit_code": 0},
    {"cmd": "npx tsc --noEmit (juices branch)", "exit_code": 0},
    {"cmd": "npm run build (juices branch)", "exit_code": 0},
    {"cmd": "git commit -F C:\\Temp\\commit_msg.txt (juices)", "exit_code": 0}
  ],
  "not_done": [
    "No push to origin (per hard rules: no push in this task)",
    "No PRs created (per hard rules: no PR in this task)",
    "TASK-461 not closed (closing authority is orchestrator only)",
    "Snacks QA report placed in 02_products/snack_bars/reports/ (not 02_products/snacks/reports/ which does not exist)"
  ],
  "self_check": "Committed blob sha256 for all four target JSONs verified via git cat-file | sha256 Python pipeline matches artifact sha256 from Get-FileHash: cheese 0a490cc5... choctab c03cc84f... snacks 406d8363... juices 9ba0dbca... — all exact matches."
}
```
