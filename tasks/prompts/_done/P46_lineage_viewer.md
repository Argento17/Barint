# P46 / Cursor calibration — spine.db lineage viewer (route: C1-CURSOR)

**➡️ OWNER: this is the C1-CURSOR calibration task (non-critical, additive). After dispatch, board auto-ticks.**

---

TASK: Create a new read-only utility `03_operations/spine/show_lineage.py` that prints the
artifact lineage of the latest end-to-end pipeline run from the Spine datastore.

CONTEXT (repo C:\Bari, all paths relative to repo root):
- The Spine datastore is `03_operations/spine/spine.db` (SQLite). Its schema is
  `03_operations/spine/schema.sql` — read it. Relevant tables: `stage_runs`
  (stage_name, signature, status, started_at, finished_at, outputs_json, error),
  `lineage` (child_path, parent_path, relation), `artifacts` (path, sha256, …).
- Connection helpers live in `03_operations/spine/spine_db.py` (e.g. `connect()`). Reuse them
  if convenient, or open the db read-only with stdlib `sqlite3`.
- The e2e pipeline (`03_operations/spine/pipeline_e2e.py`) produced stages:
  extract_bsip0 → build_bsip1 → score_products → generate_page → gate_page →
  build_copy_inputs → author_copy → merge_copy_and_gate.

REQUIREMENTS:
1. `python 03_operations/spine/show_lineage.py` prints, for the most recent run:
   (a) each stage_run (name, status, finished_at) in chronological order;
   (b) the lineage edges (child ← parent) grouped so a reader can follow raw → bsip0 →
       bsip1 → bsip2_trace → page → gate. Indent or arrow-format it so the chain is readable.
2. Read-only: the script must NOT write, alter, or delete anything in spine.db or on disk.
   Open the db read-only (e.g. `sqlite3.connect("file:...?mode=ro", uri=True)`), or just never
   execute a write. No `--execute`, no mutation.
3. Stdlib only (`sqlite3`, `pathlib`, `argparse` ok). No new dependencies. No network. No OFF
   (Open Food Facts) anything — not relevant here, but never introduce it.
4. Resolve the db path relative to the script location so it runs from any cwd.
5. If the db or a table is empty, print a clear "no runs found" message — don't crash.

ACCEPTANCE: `python 03_operations/spine/show_lineage.py` exits 0 and prints the stage list +
a readable lineage chain for the e2e run. No writes occur. Stdlib only.

RETURN: the file path; the exact command you ran and its output (first ~30 lines); confirmation
it is read-only (how you opened the db); stdlib-only confirmation. End with the machine-readable
JSON return contract (`01_framework/operations/return_contract_v1.md`); counts must include
`file_created: 1`, `writes_to_db: 0`, `new_deps: 0`, `exit_code`. Propose RETURNED — do not
write CLOSED; the orchestrator verifies and closes.
