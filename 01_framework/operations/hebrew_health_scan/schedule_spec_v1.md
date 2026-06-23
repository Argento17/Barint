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
| Output | **Run history (no files written / no commit)** — cloud routines here have git dropped (`git push` 403s every run; see [[scheduled_routines_state]] + Project Comp's redesign). Read the digest at claude.ai/code/routines. `daily_scans/` is for optional manual/local runs only. |
| Tools needed | WebSearch + WebFetch (public web only), Read |
| Expected runtime | ~8–15 min (only 1–2 articles) |
| Owner | **content-agent (Lane A)** + **nutrition-agent (Lane B)** |
| Reviewer | **Adversarial QA** reviews the first 3 digests (firewall adherence) before any keeper is applied |

**Calibration mode (first 3 runs):** stamp `mode: calibration (run k/3)`. During calibration, Lane A
keepers and Lane B KB/EV candidates are *collected* but **not applied** until Adversarial QA confirms
the firewalls are holding (no copied phrasing, no inherited data, COI/anti-model handling correct).

---

## 2. Outputs and where they go (both feed TASK-374's program, per owner)

- **Daily digest** → emitted to the **run history** (no file written; honest empty days included). The
  digest text carries everything below; a human/agent applies anything worth keeping.
- **Lane A keepers** → emitted as a ready-to-paste **append block** for
  `content_voice/tom_bari_voice/9_israeli_food_blog_research.md`. Applied by the Content Agent through
  the normal flow — the routine never edits the voice corpus unilaterally. Material register shifts that
  would change `2_voice_fingerprint.md` go through the Tom's Voice program, not this routine.
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
