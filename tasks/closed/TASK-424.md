---
id: TASK-424
title: W5: Memory retrieval — SQLite hybrid index over memory/*.md (memweave pattern)
owner: data-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-07-01
closed_at: 2026-07-01
depends_on: []
blocks: []
category_id: null
close_reason: >
  Built + verified 03_operations/agentos/memory_index.py (sha256 533930504e0f…0acb2f).
  `--selftest` exit 0 (4 assertions: OFF-query top1, copy-query top1, wikilink-expansion,
  freshness). Built real index over the live store: 134 memories indexed (MEMORY.md
  excluded), by type project=61/feedback=45/none=27/reference=1. Live recalls correct:
  natural-language "can I use open food facts for nutrition data" -> off_ban_hard_rule #1;
  "two parallel cloud lanes wiped the git tree" -> lane_dispatch_wipes_shared_tree #1. Zero
  new dependencies (FTS5 present; embeddings optional). Read-only over the store; fails safe
  to load-all. No published-score/consumer-facing change (no tripwire).
summary: >
  memory_index.py: index the memory store into local SQLite (FTS5/BM25 + recency + MMR + wikilink hop); recall(task) pulls top-k relevant memories instead of loading all ~135. Markdown stays source of truth, git-diffable, no vector DB. Read-only; fails safe to full-load.
---

# TASK-424 — W5: Memory retrieval (memweave pattern)

## Problem
All ~135 memory files load wholesale into context every session. Context engineering is the
2026 discipline: a poorly-contexted agent is ~10x cost, and loading everything drowns the few
memories that matter for the task. Needed: intent-aware retrieval WITHOUT a vector DB and
WITHOUT changing the store (markdown stays the git-diffable source of truth).

## Deliverable
- `03_operations/agentos/memory_index.py` — the "memweave" pattern: markdown source + SQLite
  sidecar index (`<memory_dir>/.memory_index/memory_index.db`). Retrieval blend:
  - **FTS5 / BM25** lexical ranking, column-weighted (name 10 >> description 5 >> body 1).
  - **Recency decay** — mild boost by file mtime (halflife ~45d, cap +25%).
  - **MMR** diversification (lambda 0.72) so top-k covers different aspects, not near-dupes.
  - **Wikilink hop** — `--expand` pulls 1-hop `[[linked]]` neighbours at half weight.
  - Embeddings are an OPTIONAL enhancement (auto-activates if sentence-transformers present);
    no hard dependency — BM25+MMR is fully functional alone.
- CLI: `--build`, `--recall "QUERY" -k N [--expand] [--auto-build]`, `--stats`, `--selftest`, `--json`.
- **Fails safe:** any recall error returns `{fallback: "load_all"}` — can never blind the agent.
- Read-only over the store; only writes its own SQLite index; idempotent rebuild; staleness-aware.

## Verification
- `python 03_operations/agentos/memory_index.py --selftest` → exit 0 (4 assertions).
- Real store: 134 indexed; two natural-language recalls return the correct memory ranked #1.
- Env: FTS5 available, numpy present, sentence-transformers absent (embeddings layer dormant, as designed).

## Integration (follow-up, not blocking)
- Callable now by the orchestrator: `memory_index.py --recall "<current task>"` to pull focused
  memories instead of scanning the full index. FULL auto-wiring into the harness session
  memory-load is a harness-level change (the harness injects MEMORY.md, not this script) —
  left as a noted follow-up; the engine is done and usable today.
- A build hook (rebuild on memory write) can be added later; today `--auto-build` refreshes on stale.
