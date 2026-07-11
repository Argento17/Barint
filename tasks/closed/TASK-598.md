---
id: TASK-598
title: BSIP0 full audit + enhancement program (Sol builds/audits, Claude challenges - owner-ordered debate)
owner: data-agent
status: CLOSED
priority: HIGH
close_reason: >
  Owner-ordered BSIP0 audit + debate complete and orchestrator-verified. Sol Round-1 audit
  (audit-only, zero source edits, C0 PASS): 17-row findings + 9 proposals + self-declared
  weaknesses. Opus Round-2 challenge (CHALLENGE pin, cross-vendor): verified every claim vs code —
  REFUTED Sol's fleet-absence finding (both hazi_hinam/acquire_hazi_hinam.py:173 and
  tiv_taam/acquire_tivtaam.py:133 are real acquirers; memory bsip0_retailer_fleet_state holds),
  CONFIRMED comma/collision/sodium-ceiling, pushed 3 cruxes. Sol Round-3 (STRATEGY-CONSULT lane,
  read-only, first live use): CONCEDED all 4 with fresh file:line evidence (Opus spot-verified
  acquire():173, discover_and_scrape():133, barcode-regex:72 — all accurate). Converged, zero
  surviving cruxes. Verdict memo: 01_framework/governance/stf_memos/2026-07-11_bsip0-audit.md.
  Outputs: parser-fix acceptance spec (NULL+FLAG on ambiguity, preserve raw, no silent correction;
  sodium ceiling → review flag) handed to the owner's other fix session; MUST workstream (provenance
  manifest + replay harness) registered as TASK-601 BLOCKED on owner program-start go/no-go. No
  code/data/score changed. TASK-597 (the malfunction fix) remains owned by the other session.
created_at: 2026-07-11
depends_on: []
blocks: []
category_id: null
summary: >
  Owner directive 2026-07-11: 'Use Sol 5.6 to solve the BSIP0 malfunction + full audit on BSIP0 to make it perfect and suggest enhancement. you two solve it. debate.' Round-based: (R1) Codex gpt-5.6-sol fixes the TASK-597 parser bugs AND audits all of 03_operations/bsip0/** (acquire scripts, _shared parser, capture format, tests, integrity flags) hunting further defect classes + ranked enhancement proposals. (R2) Orchestrator (Claude) adversarially challenges every fix decision and proposal - tries to refute, finds counter-cases. (R3+) Sol answers/revises; iterate to convergence, cap 3 rounds. Converged plan -> owner. Depends: TASK-597 folded in as the malfunction half.
---

# TASK-598 — BSIP0 full audit + enhancement program (Sol builds/audits, Claude challenges - owner-ordered debate)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
