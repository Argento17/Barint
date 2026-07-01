---
id: TASK-409
title: Corpus traceability / provenance reconciliation — clean re-derive so every live category reproduces its published scores
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-26
closed_at: 2026-07-01
depends_on: []
blocks: [TASK-395]
category_id: null
close_reason: >
  Registered retroactively during the 2026-07-01 post-port registry reconciliation (the task was
  referenced as TASK-395's depends_on and in memory [[corpus_traceability_program]] but had no
  registry file — a broken-dependency gap the reconciliation fixed).
  VERIFIED via committed artifact evidence (local master == origin/master, 0/0): the corpus
  re-derive / provenance repair landed on origin as a reviewed, merged commit series, patching
  every non-reproducing live category to its committed-trace scores:
    - 24dda6ccf repro: chocolate-bars + chocolate-tablets provenance (Phase 1)
    - 931db01af repro: snacks provenance + config fix (Phase 1)
    - 5900cbb77 repro: protein-bars provenance + config fix (Phase 1)
    - 69f046a6d repro: granola BARI_GRAN_SUGAR_25G_V1 flag + severe-cap (Phase 1b)
    - d7c574f7f repro(bread): patch score to committed-trace value + surgical_repro_patch tool
    - e51db8d11 repro(wave1): patch 6 categories to committed-trace scores
    - 7850a054a repro(cheese): patch to committed-trace scores + sync 2 grade citations
    - c554c5e63 TASK-409 cookies_coffee repro: keep 80083764, patch 33 scores, fix grade counts
    - 33b866244 clean(seo+corpus): align SEO/admin to live; delete orphaned frontend JSONs
    - 6b90a8cc8 clean(hc config): fix stale baseline v2->v4 + document true v4 provenance
    - merged PRs #30 (repro-provenance), #31 (repro-phase2), #32.
  These commits ARE what TASK-395E (provenance repair) and the interim TASK-406 (provenance
  manifest) were driving toward; both are subsumed/superseded by this landed work.
  HONESTY NOTE: closure rests on the committed/merged-PR evidence above, NOT on a fresh
  end-to-end round-trip gate run this session. A confirming full reproducibility/conformance
  pass is recommended before de-chain activation (TASK-395) proceeds — that pass is TASK-395's
  own resume trigger and remains owner-gated.
---

# TASK-409 — Corpus traceability / provenance reconciliation

Retroactive registry entry (see close_reason). The published scores for the previously
non-reproducing live categories were patched to their committed-trace values and the provenance /
config bindings repaired, all committed to origin/master via the repro commit series + merged
PRs #30–#32. This satisfies the depends_on for TASK-395 (de-chain), whose forward move is now the
owner-gated activation go/no-go against this clean baseline.

**Related open threads (NOT part of this closure):**
- TASK-395F — the forward C0 data-integrity firewall (sanitation + provenance contract gate at a
  single page-generator point) was NOT built/committed; still IN_PROGRESS.
- TASK-405 — the ingredient-field de-pollution was done locally but deliberately not ported
  (score-neutral; origin retains raw source + runtime sanitization).
