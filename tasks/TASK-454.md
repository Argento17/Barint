---
id: TASK-454
title: Triage + correct 4 real citation defects surfaced by the restored verify_citations gate
owner: research-agent
status: IN_PROGRESS
priority: HIGH
created_at: 2026-07-02
depends_on: []
blocks: []
category_id: null
summary: >
  verify_citations (TASK-452) --all sweep surfaced 4 REAL citation-integrity defects in live evidence files: (1) PMID 37357639 misattributed to Nosworthy (real: Bailey/Fanelli/Stein) diaas_source_table_v1.md:52; (2) PMID 9771853 wrong paper/year 'Willett 1997' (real: Judd 1998) bsip2_evidence_registry_v1.md:2428/2447; (3) PMID 31122155 attributed to Monteiro/NOVA 2019 but resolves to an unrelated nursing case study — UNDERPINS live D6 proposal BARI_HC_NOVA1_V1 (evidence_registry:2548/2553/2556); (4) 2 tier-A/rob_low DOIs (10.1016/j.cell.2021.12.019, 10.3390/nu11081781) resolve to unrelated papers. Research verifies correct attributions/replacements; Nutrition assesses whether #3 invalidates the BARI_HC_NOVA1_V1 evidence basis. Correct or flag each; NO score change without Nutrition/Product co-sign.
---

# TASK-454 — Triage + correct 4 real citation defects surfaced by the restored verify_citations gate

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
