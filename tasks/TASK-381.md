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

## LIVE (created 2026-06-23)
- **Cloud routine created:** `trig_01CkS9V6cacHDY3WCToqrK9i` (daily `30 5 * * *` UTC = 08:30 IL; first
  run 2026-06-23 08:31 IL). Manage: https://claude.ai/code/routines/trig_01CkS9V6cacHDY3WCToqrK9i
- Prompt embedded **inline** (self-contained); read-only tools (WebSearch/WebFetch/Read) → no commit
  attempts, output to run history. Repo files are the versioned source-of-truth, not a runtime dependency.

## D2 — loop closed (2026-06-24, owner directive "make it work")
Owner clarified the purpose: this is a TRAINING LOOP that reads real Hebrew writing and *implements*
register lessons into the Content Agent's skill — not a radar that proposes to Notion and waits. Two
defects found and fixed:
1. **It wasn't reading articles.** Both 06-24 keepers carried "full article not read — snippet only"
   (Ynet article 403'd). Fixed: cloud prompt now has a **HARD READ-GATE** (body-confirmed or no keeper) +
   **reliably-fetchable sources first** (gov.il/Clalit/Maccabi return full body; verified 2026-06-24).
   Cloud inline prompt updated via `RemoteTrigger` (working body shape: `job_config.ccr` with
   `environment_id`+`session_context`+`events:[{data:{message:{role,content}}}]`; extra event fields 400).
2. **It never implemented.** Keepers sat in Notion as `WATCH/New`. Built **`apply_scan_keepers.py`** —
   reads Lane A Notion rows, runs a deterministic no-harvest firewall (bucket=Content-Hebrew skills;
   EMULATE/AVOID framing; no Hebrew verbatim run > 7 words; ≤ 14 Hebrew words total), and appends
   survivors to **§6 of file 9**. APPLY / HOLD / REJECT. `--selftest` PASS.
- **Proven end-to-end on the 2 real 06-24 keepers:** both APPLY → written to file 9 §6 → Notion rows
  flipped to `Actioned`. Re-run = DUPLICATE (idempotent via `daily_scans/applied_index.json`).
- **Governance change:** owner directed automatic application, superseding the calibration-hold. The
  deterministic firewall + HOLD escape-hatch replace the blanket Adversarial-QA hold for Lane A. File 9
  is internal voice-training reference, NOT consumer copy — two-gate sign-off still governs consumer strings.

## NOT done (follow-ups)
- **Headless apply scheduler.** The cloud routine extracts to Notion daily, but the apply runs locally
  (cloud can't commit). Currently run during the daily `/orchestrate` pass. A fully-headless option
  (Windows Scheduled Task + Notion integration token) is available on owner request.
- **Optional:** push the spec files to `Argento17/Barint @ master` (owner-gated) so the versioned
  source-of-truth is shared; not required for the routine to run.
- Keep the inline cron prompt in sync with `daily_run_prompt_v1.md` on any edit.
