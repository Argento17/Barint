---
id: TASK-560
title: conformance.py CI job is red: page_generator configs hardcode C:\Bari absolute paths (HARD-1 fails on ubuntu)
owner: qa-agent
status: CLOSED
priority: CRITICAL
created_at: 2026-07-10
closed_at: 2026-07-10
close_reason: >
  Orchestrator-verified 2026-07-10, commit 8ea45ea4 on branch task560-conformance-ci (pushed; PR awaits
  owner). Root cause confirmed by direct evidence, not inference: PurePosixPath of the config literal has
  len(parts)==1 and is_absolute()==False, so every is_dir()/is_file() check on the 16 live configs'
  absolute paths returns False on ubuntu -> HARD-1 failed for all 16. Fix = conformance.resolve_repo_path(),
  re-anchoring any config path onto the running checkout (corpus + run trees ARE git-tracked, 48 files each,
  so no data migration); unknown-shape paths returned unchanged so bad paths still fail loudly. Applied to
  corpus_dirs, run_products_dir AND baseline_json (HARD-3 had the same defect -- that is why cheese
  "failed" for a cheese_frontend_v5.json that exists: the literal pointed at the OTHER checkout, C:\Bari on
  branch task506). Result 14/16 -> 15/16 conform.
  SECOND, INDEPENDENT cause: unmodified master already exited 1 ON WINDOWS (bread + cheese), so the job was
  red for reasons unrelated to platform. Cheese was the path bug. Bread is REAL and DOCUMENTED -- bread.json
  baseline_json targets v3 while live_manifest + bari-web serve v4; the config's own comment (TASK-433)
  records this as deliberate, out of the Data lane, and says a re-score through the config drifts a survivor
  -0.8pts (explicitly rejected). I was one edit from silently re-pointing it; that comment stopped it.
  Routed to TASK-561 (product-agent), NOT fixed here.
  CI now runs conformance_gate.py -- protective, not permissive: fails on any undocumented non-conformer, on
  drift in an excepted shelf's hard_failures, and on a stale exception (anti-zombie: an excepted shelf that
  starts conforming forces deletion of its entry). Mirrors the shadow/gold "block on regression, never on a
  documented standing state" design. Verified: gate battery 6/6 (pass/regression/drift/stale/unknown-stem/
  malformed -> 0,1,1,1,1,2); 9/9 new pytest unit tests incl. a monkeypatched POSIX-root simulation, wired
  into the workflow so they run ON the ubuntu runner (no WSL/docker locally; did not install system
  components to test); 5/5 workflows YAML-parse. The battery also caught a real BOM bug in the gate's JSON
  read (utf-8 -> utf-8-sig), same trap as board_check.py.
  NOT DONE (surfaced, not buried): resolve_repo_path is applied only in conformance.py. Other config
  consumers (run_gates.py, generate_page.py, spine_flip.py, affected_set.py) still read raw absolute paths
  and would break identically off this machine -- which is why the originally-queued "run_gates.py in CI"
  item remains BLOCKED. Needs its own task.
depends_on: []
blocks: []
category_id: null
summary: >
  Self-inflicted by TASK-554: bari_page_gates.yml runs conformance.py --all on ubuntu-latest, but all 19 page_generator configs declare corpus_dirs/run_products_dir as absolute C:\Bari\... paths. On POSIX those parse as a single relative filename (is_absolute=False), so Path().is_dir() is False, HARD-1-corpus_dirs fails for every category, conforms=False for all, exit 1. The gate cannot pass in CI. Corpus + run dirs ARE git-tracked (48 files each), so a repo-root-relative resolver fixes it with no data migration. Fix in code (portable path re-anchoring), not by rewriting configs, so other consumers keep working.
---

# TASK-560 — conformance.py CI job is red: page_generator configs hardcode C:\Bari absolute paths (HARD-1 fails on ubuntu)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
