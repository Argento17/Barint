---
id: TASK-609
title: PD-1: Product identity registry + alias table + barcode-state backfill
owner: data-agent
status: CLOSED
close_reason: >
  Delivered + orchestrator-verified + committed cec1be4b (task506). Codex terra built
  registry_ops.py (the ONLY registry writer) + product_registry.json. VERIFIED: write-boundary
  clean (git: only 03_operations/product_dossier/ touched, ZERO served JSON); --selftest PASS (GTIN
  good/bad/truncated + 2 deterministic in-memory builds byte-identical + served-JSON write-boundary
  rejection); --check PASS (rebuild == committed) re-run by orchestrator in the MAIN tree off the
  CURRENT manifest (regenerated to absorb batch-3 bread/chocolate captures — the artifact is derived,
  recompile as coverage grows); 687 entries HONEST (710 served rows, 23 exact-duplicate rows deduped,
  0 missing/0 collisions/0 splits — orchestrator-audited served-rows-vs-registry gap = 0); R-B
  COMPLIANT (entries carry only bari_pid/aliases/barcode_status/recovered_gtin + a name_provenance
  POINTER — no authoritative product facts copied). Distribution: verified 440 / malformed 129 /
  pending_manual_review 118 / not_found 0 / conflicting 0. pid = bari_ + 96-bit SHA-256 over
  ['bari-pid-v1', shelf, served_id, verbatim_name] (opaque, insertion-stable, never barcode-derived).
  Refinement follow-up → TASK-613 (malformed conflates benign Shufersal SKU vs true truncation).
priority: HIGH
created_at: 2026-07-11
depends_on: []
blocks: []
category_id: null
origin_task: TASK-608
lesson_trigger: none
summary: >
  First module of the PD spine (STF-approved 2026-07-11). Mint opaque immutable bari_pid per served product; alias table (legacy bsip1 ids / served ids / (retailer,gtin) manifest keys -> pid) with collision+split detection; 5-state barcode adjudication (verified/found_but_conflicting/malformed/not_found/pending_manual_review) + recovered_gtin candidates. Registry owns ONLY these; all other identity facts stay provenance-pointed projections. Deterministic backfill from served JSONs + 601 manifest + barcode audit. Read-mostly; writes only 03_operations/product_dossier/registry/. Tripwire-1 firewall: never flows into served pages.
---

# TASK-609 — PD-1: Product identity registry + alias table + barcode-state backfill

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
