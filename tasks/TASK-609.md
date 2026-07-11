---
id: TASK-609
title: PD-1: Product identity registry + alias table + barcode-state backfill
owner: data-agent
status: IN_PROGRESS
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
