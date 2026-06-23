---
id: TASK-381
title: Hebrew Health Scan — daily IL health-writing routine (voice register + evidence horizon-scan)
owner: content-agent
status: IN_PROGRESS
priority: MEDIUM
created_at: 2026-06-23
depends_on: [TASK-374]
blocks: []
category_id: null
summary: >
  A daily scheduled routine that reads 1-2 Israeli health/nutrition articles from a curated
  14-source registry and runs two firewalled passes: LANE A (voice) calibrates Bari's natural-Hebrew
  register for Project Tom's Voice (output = emulate/avoid register notes appended to file 9, NEVER
  harvested phrasings); LANE B (evidence) runs each claim through the Nutrition Agent's Evidence
  Horizon-Scan four-bucket routing (output = KB stub / EV proposal / decline, NEVER inherited data).
  Owner-initiated 2026-06-23. Sibling to Project Comp (kept; overlap is fine - different outputs).
---

# TASK-381 — Hebrew Health Scan (daily IL health-writing routine)

**Spec dir:** `01_framework/operations/hebrew_health_scan/`. **Serves:** TASK-374 (Tom's Voice
register) + Evidence Horizon-Scan (Nutrition Agent). **Memory:** [[scheduled_routines_state]],
[[project_toms_voice]].

## Owner direction (2026-06-23)
- Want a routine over Israeli health blogs, 1-2 articles/day, to (1) improve Content Agent Hebrew
  writing and (2) extract any valuable info for Bari.
- Sources: owner-supplied list of 14 (logged in `source_registry_v1.yaml`).
- Output: both lanes feed the Tom's Voice program; digest-only surfacing per the owner interaction contract.
- Project Comp stays; content overlap with it is acceptable (different routine, different output).

## Built (D1 spec-ready, 2026-06-23)
- `source_registry_v1.yaml` — 14 owner sources lane-mapped (voice_lane / evidence_lane), COI-flagged
  (pharmaguri/tnuva = evidence none; dietamir/tali-diet = anti_model tone), cross-referenced to the
  9 already in Project Comp (`comp_ref`). 5 new to the Bari universe (maccabi4u, n12, israelhayom,
  agogo, plus the diet/pharma brands).
- `daily_run_prompt_v1.md` — two-lane run prompt with 6 non-negotiable firewalls (Lane A = register
  technique only, zero copied phrasing, RAG-over-blogs rejected per charter; Lane B = zero data
  inherited, OFF ban, Horizon-Scan four-bucket; COI/anti-model handling; no consumer copy; no score move).
- `output_template_v1.md` — digest shape (coverage / Lane A emulate-avoid / Lane B routing table /
  firewall self-attestation), honest-empty-day rule.
- `schedule_spec_v1.md` — daily 08:30 Asia/Jerusalem (cron `30 5 * * *` UTC; distinct from Comp's
  20:30 slot), calibration mode (first 3 runs, Adversarial QA reviews firewall adherence), outputs map.
- `daily_scans/.gitkeep` — output dir.

## NOT done (remaining to go live)
- **Cloud routine not yet created** (program-start = owner trigger, per the Project Comp convention).
- **Spec files must reach the routine's branch/repo first** — cloud routines run on `Argento17/Barint @
  master`; these files are on `task-374-toms-voice`, unpushed. Push (owner-gated) before creating the cron.
- First 3 runs = calibration; Adversarial QA confirms firewalls hold before any Lane A keeper is applied
  to file 9 or any Lane B candidate reaches the KB.
