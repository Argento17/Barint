---
id: TASK-584
title: Rename integrations/clients/http.py to stop stdlib http shadow
owner: data-agent
status: BLOCKED
priority: LOW
created_at: 2026-07-10
depends_on: []
blocks: []
summary: >
  integrations/clients/http.py shadows the stdlib `http` package when that dir is on
  sys.path[0]. Any script doing `sys.path.insert(0,'integrations/clients'); import X`
  where X (or its deps, e.g. transformers) does `import http.client` fails with a
  misleading error. On 2026-07-10 this made the DictaBERT grammar gate falsely report
  "requires transformers/torch"; the Content lane recorded grammar as unrunnable.
  Root cause diagnosed (TASK-576); correct-import workaround in use.
---

# TASK-584 — Rename integrations/clients/http.py (stdlib shadow)

## The defect
`integrations/clients/http.py` is a legitimate shared HTTP helper, imported correctly
as `from integrations.clients.http import HttpError` (verify_citations.py:74). But when a
script runs with `integrations/clients/` as sys.path[0], the local `http.py` shadows the
stdlib `http` package. transformers/torch (and anything doing `import http.client`) then
fail. Manifests as a FALSE "transformers not installed" error.

## Fix (deferred — LOW, not blocking)
Rename `integrations/clients/http.py` -> `bari_http.py` (or `http_client.py`) and update
every importer. Confirmed importers in the LIVE tree (not worktrees):
  - 03_operations/validators/verify_citations.py:74  `from integrations.clients.http import HttpError`
Re-grep the full live tree before renaming; there may be more. Worktrees carry their own
copies and are out of scope.

## Meanwhile — the workaround (verified working 2026-07-10)
Import repo modules as PACKAGES from the repo root, never `sys.path.insert` the clients dir:
  from integrations.clients import hebrew_grammar_gate as g   # loads transformers fine
Run with `.venv/Scripts/python.exe`, `PYTHONUTF8=1`. This fully unblocks grammar verification.

## Status
BLOCKED on nothing technical — deferred as LOW so it is not done inline while other lanes
run in the shared tree. Pick up when the tree is quiet. Memory: hebrew_shell_corruption_and_verify_gotchas item 5.
