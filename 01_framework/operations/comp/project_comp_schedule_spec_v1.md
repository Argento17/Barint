# Project Comp — Schedule Spec v1

**Status:** D1 — **CREATED & LIVE** (owner-triggered 2026-06-10). **Built:** 2026-06-10.

**Live routine (cloud):**
- Routine ID: `trig_0171rxWLPZrTBfUjquGVA2vJ`
- Manage: https://claude.ai/code/routines/trig_0171rxWLPZrTBfUjquGVA2vJ
- Cron: `30 17 * * *` **UTC** = 20:30 Asia/Jerusalem (IDT/UTC+3). First run: 2026-06-10 20:30 IL.
- Repo: `Argento17/Barint` @ master · model `claude-sonnet-4-6` · tools incl. WebSearch/WebFetch.
- MCP connectors: **none** (stripped 2026-06-10 — not needed for this task).
- **DST caveat:** cron is fixed UTC. When Israel switches to UTC+2 (~late Oct), update cron to `30 18 * * *` to hold 20:30 local.

**First-run baseline:** run 1 is a **comprehensive ~5-month look-back** (since ~2026-01-01) — a
landscape snapshot of standing competitor/regulator positions and recurring discourse, prioritizing
durable signals over one-off spikes. **From run 2 onward it is a daily ~24–36h delta.** (See run prompt → RUN WINDOW.)

---

## 1. The daily automated run

| Field | Value |
|---|---|
| Name | `project-comp-daily` |
| Cadence | Daily, evening |
| Time | **20:30 Asia/Jerusalem** (after the IL news day; before late night) |
| Cron | `30 20 * * *` (TZ = Asia/Jerusalem) |
| Start | Today (2026-06-10) |
| Prompt | runs `project_comp_daily_run_prompt_v1.md` |
| Output template | `project_comp_output_template_v1.md` |
| Output path | `01_framework/operations/comp/daily_reports/<YYYY-MM-DD>.md` |
| Rolling action queue | `01_framework/operations/comp/comp_action_queue.md` (append-only; never auto-actioned) |
| Tools needed | WebSearch + WebFetch (public web only), Read, Write |
| Expected runtime | ~15–25 min |
| Scope | **Automated = `platform: web` sources only** (Tier A/B/C per the run prompt). Social = excluded, stamped `not_checked`. |
| Owner | **research-agent + marketing-agent** (joint) |
| Reviewer | **qa-agent reviews the first 3 outputs** before any downstream task is opened |

**Calibration mode (first 3 runs):** runs 1–3 are **calibration**. Do NOT overreact to single-day
virality — a one-day spike from one creator is a `monitor` row at most, never a P0/P1 action. Stamp
each of the first three reports `RUN MODE: calibration (run k/3)` in the Context block. **No
downstream task (`TASK-XXX`) may be opened off a calibration report until qa-agent has reviewed all
three** and confirmed the run is behaving (coverage honest, C/D separation holding, gates respected,
no over-firing). After run 3 + QA sign-off, the run graduates to normal mode.

**Failure handling:**
- If WebSearch/WebFetch is unavailable → write a stub report stating the outage and `not_checked`
  for all sources; do not fabricate. Surface in the next run.
- If a run is missed → next run covers a wider look-back window (note it in the source log); do not
  attempt to backfill multiple dated reports.
- A run is **invalid** (QA may void it) if any Hard Rule in the run prompt was violated — e.g. a
  social source was auto-fetched, a score change was proposed, or a source log has silent gaps.

---

## 2. Manual-periodic social sweep (NOT automated — human-in-loop)

Per the D1 social-access decision: **manual-periodic sweep, no automated Instagram/TikTok scraping.**
A person (or a human-supervised assisted session) opens the public profiles, reads recent posts, and
logs findings. The system may fire **reminders** for these; it must not auto-scrape.

| Sweep | Sources | Cadence | Suggested day(s) | Log path |
|---|---|---|---|---|
| IL social sweep | IL `instagram`/`tiktok` creators (e.g. il-024 Omer Miller, il-032 Yaniv Salman, + promoted IL creators) | **2× / week** | Sun + Wed | `01_framework/operations/comp/social_sweep/sweep_il_<YYYY-MM-DD>.md` |
| Global social sweep | Global `instagram`/`tiktok` creators (gl-021/022/027–034 …) | **Weekly** | Thu | `01_framework/operations/comp/social_sweep/sweep_global_<YYYY-MM-DD>.md` |
| Candidate review | `source_candidates_v1.yaml` live candidates | **Weekly** | Sun | promote/reject decisions logged in `source_discovery_report_v1.md` change log |

Optional reminder crons (reminders only — they prompt a human, they do NOT scrape):
- IL sweep reminder: `0 18 * * 0,3` (Sun & Wed 18:00 Asia/Jerusalem)
- Global sweep reminder: `0 18 * * 4` (Thu 18:00)
- Candidate review reminder: `0 17 * * 0` (Sun 17:00)

Each sweep log feeds the daily run's `not_checked (last swept YYYY-MM-DD)` stamps and appends to the
same rolling action queue. Credibility vs. discourse separation applies identically in sweeps.

**Candidate review rules (weekly):** promote a candidate to active only when its public URL/handle is
confirmed live AND relevance holds (the D0b/D0c promotion standard); reject/park otherwise. No
guessed handles. Tombstone promoted/rejected entries; never silently delete.

---

## 3. What the schedule does NOT do

- Does **not** change scores, copy, methodology, or `tasks/` registry state.
- Does **not** publish anything consumer-facing.
- Does **not** fetch private/paywalled/logged-in/social content.
- Does **not** auto-promote candidates or auto-action the queue — those are weekly human/agent calls.

---

## 4. Pre-flight checklist before the owner creates the run

- [ ] Confirm time/timezone (default 20:30 Asia/Jerusalem) and that evening suits the IL news cycle.
- [ ] Confirm output dirs exist or will be created on first run:
      `03_operations/reports/comp/daily/`, `.../social_sweep/`.
- [ ] Assign the **human owner** of the manual social sweeps (the automated run cannot do them).
- [ ] Confirm the run agent has WebSearch + WebFetch (public web) enabled.
- [ ] Decide whether the optional sweep **reminders** are wanted, or sweeps are tracked manually.

When these are green, the run is safe to create via the scheduling tool. **Project Comp does not
create it itself** (program-start = owner trigger).
