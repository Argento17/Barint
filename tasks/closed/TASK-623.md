---
id: TASK-623
title: PD<->catalog<->comparison alignment: audit current agreement + build parity gate (always-aligned spine)
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-07-11
depends_on: []
blocks: []
category_id: null
origin_task: TASK-608
lesson_trigger: none
close_reason: "VERIFIED + merged 82e16591. Codex gpt-5.6-terra built it, Opus cross-vendor verified. Audit: 710 comparison rows / 687 PD, matched=710 agree=710 diverge=0 gaps=0 — PD publication_record (served_json_verbatim) == comparison score/grade == catalog (inventory loader reads comparison registry). parity_gate.py: --selftest PASS (catches an injected PD-score mismatch → real gate, not a no-op), real check exit 0 on current tree; CI-wired into bari_page_gates.yml (path trigger + --selftest + gate run). Owner's 'always aligned' rule now enforced in CI."
summary: >
  Owner rule: PD must ALWAYS align with product catalog + comparison pages. Audit current agreement (PD publication_record score/grade/identity vs *_frontend_v*.json vs catalog) across all 687; build a parity gate (extend TASK-588 registry-parity pattern) that FAILS if the 3 surfaces diverge on score/grade/identity; wire to CI. Foundation for the re-score program.
---

# TASK-623 — PD<->catalog<->comparison alignment: audit current agreement + build parity gate (always-aligned spine)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
