# Hebrew Health Scan — Schedule Spec v1

**Status:** D1 — **CREATED & LIVE** (owner-triggered 2026-06-23). **Built:** 2026-06-23 ·
**Registry:** TASK-381 · **Serves:** TASK-374 + Evidence Horizon-Scan.

**Live routine (cloud):**
- Routine ID: `trig_01CkS9V6cacHDY3WCToqrK9i` · Manage: https://claude.ai/code/routines/trig_01CkS9V6cacHDY3WCToqrK9i
- Cron `30 5 * * *` UTC = 08:30 Asia/Jerusalem (IDT/UTC+3). First run: 2026-06-23 08:31 IL.
- Model `claude-sonnet-4-6` · repo `Argento17/Barint` · tools: **WebSearch, WebFetch, Read only** (no write/bash → cannot attempt the commit that 403s; output = run history).
- **The run prompt is embedded INLINE in the cron** (self-contained — does not depend on these repo files being on master). These spec files are the versioned source-of-truth + the place to evolve the prompt; sync inline ↔ files when either changes.
- **DST:** when IL → UTC+2 (~late Oct), change cron to `30 6 * * *` to hold 08:30 local.
- Auto-attached MCP connectors (Calendar/Gmail/Drive/Notion/Spotify) are inert (empty permitted_tools) — ignore.

---

## 1. The daily automated run

| Field | Value |
|---|---|
| Name | `hebrew-health-scan-daily` |
| Cadence | Daily |
| Articles/run | **1–2** (owner spec) |
| Time | **08:30 Asia/Jerusalem** (morning read; pairs with the day's content work — distinct from Project Comp's 20:30 evening slot so the two routines don't collide) |
| Cron (UTC) | `30 5 * * *` = 08:30 IDT (UTC+3). **DST:** when IL → UTC+2 (~late Oct), change to `30 6 * * *`. |
| Prompt | `01_framework/operations/hebrew_health_scan/daily_run_prompt_v1.md` |
| Sources | `01_framework/operations/hebrew_health_scan/source_registry_v1.yaml` |
| Output template | `01_framework/operations/hebrew_health_scan/output_template_v1.md` |
| Output | **Two sinks (loop closed 2026-06-24):** (1) the run-history digest at claude.ai/code/routines, and (2) structured keeper rows in the shared Notion "Bari Routine Log" (data_source `77bd20b8-fd7f-4486-b477-475a387f6b5e`). The cloud routine still writes NO repo files / commits NOTHING (git dropped — `git push` 403s; see [[scheduled_routines_state]]). The **apply** step that folds Lane A keepers into the voice corpus runs LOCALLY via `apply_scan_keepers.py` (the cloud routine cannot commit). `daily_scans/` holds the per-day keeper/result JSON + the applied-index dedup sidecar. |
| Tools needed | WebSearch + WebFetch (public web only), Read |
| Expected runtime | ~8–15 min (only 1–2 articles) |
| Owner | **content-agent (Lane A)** + **nutrition-agent (Lane B)** |
| Reviewer | **Adversarial QA** reviews the first 3 digests (firewall adherence) before any keeper is applied |

**Calibration mode (first 3 runs):** stamp `mode: calibration (run k/3)`. During calibration, Lane A
keepers and Lane B KB/EV candidates are *collected* but **not applied** until Adversarial QA confirms
the firewalls are holding (no copied phrasing, no inherited data, COI/anti-model handling correct).

---

## 2. The closed loop (read → extract → firewall → apply) — owner directive 2026-06-24 "make it work"

The routine is now a TRAINING LOOP for the Content Agent's Hebrew, not a suggestion box. Two halves:

**(A) Extractor = the cloud routine** (read-only; inline prompt updated 2026-06-24):
- **HARD READ-GATE:** a keeper may only come from an article whose BODY was actually read. A
  section/index page (cards + headlines) is not an article; headline/snippet-only inference is a
  FAILED run, not a keeper. (This fixes the 06-24 defect: both keepers carried "full article not read".)
- **Reliably-fetchable sources tried first:** efsharibari.health.gov.il, clalit.co.il, maccabi4u.co.il
  return full Hebrew body; ynet/mako/n12/walla/israelhayom article pages sometimes 403 → move on, never
  degrade to the snippet. (Verified 2026-06-24: gov.il/Clalit/Ynet-article ✅; mako *section* = cards only.)
- Logs Lane A keepers (Finding must start `EMULATE:`/`AVOID:`) to the Notion "Bari Routine Log".

**(B) Applier = `apply_scan_keepers.py`** (LOCAL; the cloud routine cannot commit):
- Reads the new Lane A Notion rows, runs a **deterministic no-harvest firewall**, and appends survivors
  to **§6 of `content_voice/tom_bari_voice/9_israeli_food_blog_research.md`** with provenance + firewall
  verdict. Three outcomes: **APPLY** (clean → Notion row → Actioned), **HOLD** (borderline → left New for
  a human/Adversarial QA), **REJECT** (violation → Dropped).
- Firewall rules: bucket = `Content-Hebrew skills`; Finding framed `EMULATE:`/`AVOID:`; no verbatim
  Hebrew run > 7 words (a harvested sentence); ≤ 14 Hebrew words total. `--selftest` PASS.
- **Governance:** owner directed automatic application 2026-06-24, superseding the calibration-hold
  ("collect, don't apply, until Adversarial QA"). The deterministic firewall + the HOLD escape-hatch
  replace the blanket human hold. This is **internal voice-training reference, not consumer copy** — the
  two-gate content sign-off still governs every consumer-facing string. Material shifts to
  `2_voice_fingerprint.md` still go through the Tom's Voice program, not this routine.

**Operating the apply step (HEADLESS — wired 2026-06-24):** a Windows Scheduled Task
**"Bari - Hebrew Health Scan apply"** runs `drain_and_apply.py` daily at **09:15 local** (after the
~08:30 cloud run). It queries the Notion "Bari Routine Log" (DB `fb50a533316440c4a571f9bb32206e48`)
for `Routine=Hebrew Health Scan · Status=New · Bucket=Content-Hebrew skills`, runs each through
`apply_scan_keepers` (firewall → file 9 §6), then writes back: APPLY → `Actioned`, REJECT → `Dropped`,
HOLD/SKIP → left `New`. Commits the file-9 change locally (cloud can't commit). Logs to
`daily_scans/drain_log.txt`. Offline `--selftest` PASS; `--dry-run` available; live HTTP exercised once
the token exists.
- **AUTH (one-time owner step):** a Notion internal-integration secret in `NOTION_TOKEN` env var OR
  `%USERPROFILE%\.bari\notion_token` (setup readme at `~/.bari/README_notion_token.txt`). Until present,
  the task runs harmlessly and logs "token not configured". The cloud routine's own Notion writes use its
  OAuth connector and are unaffected.
- The `/orchestrate` MCP-based drain remains a valid manual fallback if the task is disabled.

- **Lane B keepers** → listed for the **Nutrition Agent**, who runs the formal Horizon-Scan decision
  (KB stub / `EV-###` proposal / decline). The routine writes neither the KB nor the evidence registry.

---

## 3. What this routine does NOT do

- Does **not** author consumer copy or move any score (copy = Content Agent + two-gate; scores = governed BSIP path).
- Does **not** inherit any blog number/ingredient/value (OFF ban + file 9 firewall).
- Does **not** copy phrasing into a phrase library (charter rejects RAG over external blog text).
- Does **not** fetch paywalled/logged-in/private content.
- Does **not** duplicate Project Comp's job — Comp = discourse/competitor/misinformation radar (evening);
  this = voice-register + evidence-extraction reader (morning). Overlapping sources, different outputs.

---

## 4. Post-creation notes (created 2026-06-23)

- Created with the prompt **inline** (self-contained) so it runs regardless of repo/branch state — the
  spec files reaching master is therefore NOT a runtime blocker. Pushing them to master is still worth
  doing so the versioned source-of-truth is shared, but the routine does not depend on it.
- First 3 runs = calibration; Adversarial QA reviews firewall adherence (no copied phrasing, no inherited
  data, COI/anti-model handling) before any Lane A keeper is applied to file 9 or Lane B candidate reaches the KB.
- To change the prompt: edit `daily_run_prompt_v1.md` here AND update the inline event via
  `RemoteTrigger` update (keep them in sync).

When green, safe to create. **This routine does not create itself** (program-start = owner trigger).
