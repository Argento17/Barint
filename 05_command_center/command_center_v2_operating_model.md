# Command Center v2 — Operating Model

**Task:** TASK-186
**Owner:** cc-agent
**Date:** 2026-06-05
**Status:** PROPOSAL — owner sign-off required before any build (touches the owner's primary instrument; go-live is owner-gated)
**Supersedes (framing only, not mechanics):** the left-rail "monitoring spine" in `command_center.html`; the executive framing in `command_center_data_model.md`
**Keeps (mechanics, in full):** `generate_dashboard.py` derivation engine, `command_center_v3_design.md` drift model, `source_of_truth_design.md` "registry is authoritative, JSON is derived" rule, `command_center_v2_architecture.md` "derive, don't maintain" constraint

> This is a **reframing of what the screen shows and why**, not a rewrite of how state is derived. The v2/v3 derivation engine (`generate_dashboard.py`) is correct and stays. What changes is the **render contract**: today the generator computes the right signals (`next_action`, `critical_path`, `category_state`, `drift`, `banked_assets`) and the HTML then **buries them behind decoration**. v2 is the rule that the screen must lead with those signals and stay silent otherwise.

---

## REVISION 1 (2026-06-05) — CC is TOM'S Chief of Staff, not Bari's

> **Owner decision of record (Tom, 2026-06-05).** This revision redefines *what CC is* — a strategic, owner-authorized call. The prior version (sections A–D, Widgets, Keep/Kill/Build, Migration below) was written as if the Command Center were *Bari's* operating board. **It is not. It is Tom's.** Everything below the original A. heading is preserved as authored — its mechanics (derivation engine, drift model, next-action ladder, earned silence, activity-vs-progress) are all still correct and still load-bearing — but it is now **scoped down to one portfolio item** inside a larger surface. Read this revision block first; it is the new organizing spine. The original sections remain as the detailed design of the **Bari portfolio panel** and as the reasoning history of how the exception-based render contract was derived.

### What changed, in one move

CC is **Tom's personal Chief of Staff**, and his Command Center is **Tom's day**, not Bari's board. The classic Chief-of-Staff frame (Cohen) has three pillars — **Process · People · Portfolio** — and **Bari is one Portfolio item.** The top surface is the decisions only Tom can make, his calendar, his inbox, and what the org escalates upward. The entire prior document (the autonomous multi-agent company, the next-move ladder, the progress line) is now the contents of **one tile**: the Bari portfolio. It does not get the whole screen; it gets a lane that stays quiet unless Bari needs Tom.

```
TOM'S CHIEF OF STAFF  (the whole surface)
├── PROCESS   — Tom's operating rhythm: today/this-week, the cadences CC owns,
│              protected focus, what's on-pace vs slipping
├── PEOPLE    — the people in Tom's orbit: inbox that needs HIM, who he owes a
│              reply, agents-as-direct-reports (each with a commitment, not a pulse)
└── PORTFOLIO — Tom's ventures/programs. BARI IS ONE OF THESE.
               (the entire original A–D design renders inside this one lane)
```

The success sentence is rewritten accordingly (the original is preserved in §A):

> **When Tom opens his Command Center, within 10 seconds he knows the one decision only he can make today (across everything — inbox, calendar, and every portfolio), what got handled so it never reached him, and whether his week is on-pace — or the screen is honestly quiet because nothing needs him. Bari is one line in that brief, not the brief.**

### The acid test (Decision 2, upgrade 1 — *Measure CC by what did NOT reach Tom*)

From Monkhouse: **a great Chief of Staff makes the principal's job *smaller*.** CC's own headline KPI is therefore not throughput but **absorption**: the **decisions-absorbed ÷ decisions-escalated ratio, trended over time.** The board reports, in one line, *"handled N so you didn't have to · escalated M to you"* and the trend arrow on that ratio. A board that brags about activity ("216 closed!") is the **failure mode**, not the success state — it proves CC is performing work instead of shrinking Tom's load. The "SINCE YOU LEFT" element (originally §A L1 #3) is reframed from an *activity ledger* into a **"what I handled so you didn't have to"** statement plus the short escalation list — same data, inverted emphasis: the point is the *shrinking*, not the *doing*.

### The six Chief-of-Staff-practice upgrades (Decision 2)

Each is wired to the principle it comes from (Cohen: Process/People/Portfolio; Monkhouse: 7 traits + failure modes). These **revise** the original §A–§D, they don't sit beside it.

1. **Measure CC by what did NOT reach Tom** *(Monkhouse — the CoS shrinks the boss's job).* See the acid test above. Headline KPI = absorption ratio, trending. Kill any vanity counter.
2. **Own the strategic rhythm/cadence, not just tasks** *(Cohen — Process pillar).* CC owns Tom's **operating rhythm**, not just his task list. Add a **pace layer**. For the Bari portfolio that's **launch cadence**: categories live · next one · gates out · days-since-last-launch → an **on-pace / slipping** verdict (this generalizes the original PROGRESS LINE). Generalized across the surface: CC tracks each of Tom's recurring rhythms (weekly review, launch beat, decision cadence) and flags the one that's slipping.
3. **Never surface a naked blocker — surface a framed decision** *(decision architecture; Cohen — the CoS removes friction from the principal's choices).* Every escalation is a **decision object**: *question + 2–3 options + CC's recommendation + the one fact that decides it*, answerable in **10 seconds**. "TASK-182 is blocked" is forbidden; "Sign the clinician NDA, or drop the clinician co-sign and ship D7-only? I'd sign — it's the only gate left and reversible" is the contract.
4. **"Verified, not self-reported" as a visible trust primitive** *(single source of truth — a function doesn't mark its own homework).* Closed/completed work carries a visible provenance badge: **"✓ verified by CC against artifacts"** vs **"agent claims done."** The trust primitive is *on the surface*, not buried in a close_reason. This is the close-readiness gate made visible.
5. **Agent status = accountability, not activity** *(Cohen — People pillar; agents are direct reports).* Each agent is shown as a **direct report with a commitment**: *owns X · owes Y · by when · on-pace/slipping · last verified delivery* — **never "busy/online."** This replaces the original §A Q5 "agents are invisible unless bottlenecked": agents still don't get vanity avatars, but when shown they show *accountability*, not presence.
6. **Force-the-agenda element** *(Monkhouse — agenda-setting is the CoS's dominant influence lever).* Detect **important-but-untouched**, not just blocked: anything **parked > N days** surfaces as **"decide or kill."** The board sets Tom's agenda proactively rather than only reacting to faults.

**Failure-mode guardrails (baked in, from Monkhouse's failure modes):**
- **Kill vanity counters** — activity ≠ value. No headline count of closed/opened/commits anywhere above L3.
- **Silent when healthy** — a great CoS is **invisible when things go well.** This is *why* exception-based rendering (original §A "earned silence") is correct, not merely an aesthetic: the boss's attention is the scarce resource, and a quiet board is CC succeeding.
- **Always distinguish autonomous/reversible from escalated** — the **authority-ambiguity trap.** Every object is badged HANDLED (reversible — veto) or YOURS (decide). Authority must never be ambiguous.

---

## REVISION 2 (2026-06-05) — the PERSONAL layer (Gmail + Calendar), read-only

> **Owner decision of record (Tom, 2026-06-05).** Tom is adding a **read-only Google connector (Gmail + Calendar)** so CC sees his inbox and calendar. This makes CC a *personal* Chief of Staff, not only an org one — it is the **People + Process** half of the frame that Bari alone could never fill. Tom is building the client in parallel; this document models **what the board does with it**, not the client itself.

**Decided posture (non-negotiable, owner-set):**
- **Read-only.** CC may **look and draft**, never send, accept, decline, delete, or change anything. Every personal-layer output is a *draft for Tom to approve and act on himself.*
- **Credential stays local.** OAuth refresh-token lives only on Tom's laptop in a **gitignored local token store** — never in the registry, never committed, never synced.
- **Full visibility, near-zero surface.** CC reads the *whole* inbox and calendar but **surfaces almost nothing** — same exception-gated discipline as the rest of the board. ~95% of mail stays invisible.

**The three personal elements (all Level 1, exception-gated):**

1. **Inbox** *(People pillar).* Only mail that **needs Tom**: awaiting his reply, time-sensitive, or from people who matter. Each surfaced item carries a **CC-drafted reply Tom approves** (never auto-sent). 95% of the inbox never appears. — *Changes: whether Tom replies now, and approves CC's draft.*
2. **Calendar / Day** *(Process pillar — Tom's operating rhythm).* Today and this-week: **conflicts, missing prep, and protected focus gaps**, with each meeting tied to the **decision or portfolio item it concerns.** — *Changes: how Tom spends the next block; whether a meeting needs prep CC should draft.*
3. **The join** *(the cross-pillar move).* Personal-world items **link to portfolio items**: *"this email is about TASK-182's blocker"* / *"your 2pm is the clinician whose NDA gates the Glass Box launch."* The inbox and calendar stop being a separate app and become **the same brief** as the org escalations — one surface, one decision queue.

**New input (model only — Tom builds it):** a read-only `integrations/clients/google_workspace.py` client — Gmail + Calendar REST, OAuth **refresh-token** auth, **local-only**, mirroring the EDPG read-only client pattern already used across `integrations/clients/`. The board treats it exactly like any other read-only source: it reads, it never writes, and an unavailable/unauth state is an honest *"can't see your inbox right now"*, never a silent empty.

**Risks flagged in making CC personal (surfaced for owner review):**
- **Privacy / blast radius.** CC now reads Tom's *personal* mail and calendar, not just org state. Mitigation: read-only, local-only credential, gitignored token store, and the same surface-almost-nothing discipline — but the *read* surface is wide, so the local-only credential boundary is the load-bearing control.
- **Scope creep.** "Look & draft" can quietly drift toward "send & schedule." The read-only posture must be a **hard primitive**, not a setting — no write path should exist in the client at all.
- **The Bari-vs-Tom boundary.** CC must never let *Bari's* interests frame *Tom's* personal decisions (e.g. nudging him to prioritize a Bari meeting over a personal one). The Portfolio pillar serves Tom; Tom does not serve the portfolio. When a personal item and a Bari item compete, CC surfaces the conflict neutrally and lets Tom decide — it does not advocate for Bari.

---

## A. Command Center Philosophy
> **[REVISION NOTE]** Section A as originally written treats the *Bari org* as the whole world. Post-revision, **read every "the Command Center" below as "the Bari portfolio panel"** and every "Tom's executive interface to the org" as "the Bari lane inside Tom's Chief-of-Staff surface." The reasoning is unchanged and still correct *for that panel*; the scope is now one-of-many. The success sentence here is superseded by the revised one in Revision 1.

### What it is

The Command Center is **Tom's executive interface to an autonomous multi-agent company.** It is not a task tracker. The tasks are the *org's* working memory; the Command Center is the *owner's* control surface onto an org that is supposed to run itself. Ten agents and the orchestrator decide and act by default (CLAUDE.md autonomy-default, 5 tripwires). The Command Center exists for the narrow, high-value slice of reality that the autonomy mandate **cannot** absorb: the calls that are genuinely Tom's, and the signals that tell him whether the autonomous machine is actually moving the company forward or just moving.

It is an **AI Chief of Staff**: a thing that has already read every return block, verified every claim against artifacts, closed what was closeable, and now walks in with a one-line brief — *"Here is the one decision only you can make, here is what I did while you were gone, here is the one thing quietly going wrong, and everything else is handled."* A Chief of Staff who reads you the whole org chart every morning is fired. One who hands you the three things that matter is indispensable.

### The AI-Chief-of-Staff framing (what this changes)

| Task dashboard (today) | Chief of Staff (v2) |
|---|---|
| Shows all open work, equally | Shows only what needs **you**; handles the rest and tells you it did |
| "CC posture": HEALTH/WIP/BLOCKED/DRIFT gauges | Named objects: *which* task, *what* move, *whose* decision |
| Loudest when the page loads (aurora, scan line, breathing badges) | Loudest exactly when something is wrong; silent when clean |
| Measures motion (216 closed, status churn) | Measures advance (which category is live; what's the next one) |
| Reports that work happened | Reports whether the **company** moved |
| You read it to find out the state | It tells you the state and what to do about it |

### The single sentence that defines success

> **When Tom opens Bari, within 10 seconds he knows the one decision only he can make, what the org did autonomously since he last looked, and whether the company actually moved toward another live category — or the screen is honestly quiet because nothing needs him.**

A green board that is silent is the **success state**, not an empty one. The current board cannot express "all handled" — it always performs activity. v2's hardest and most important capability is **earned silence.**

---

## B. Information Hierarchy
> **[REVISED by Revision 1+2]** The L1 list below is rewritten to be **Tom's whole day**, not Bari's board. The original Bari-only L1 (5 objects) is retained verbatim immediately after, as the **Bari portfolio panel's** internal hierarchy (it renders *inside* the Portfolio lane, one level down). The placement rule is unchanged.

Three levels, by the decision each item changes. The rule for placement: **Level 1 = changes a decision in the next 10 seconds. Level 2 = context you reach for when L1 made you ask "why." Level 3 = forensic, you go looking for it.** If an item changes no decision at any level, it is killed (Section "What to REMOVE").

### Level 1 — REVISED — Tom's day (the 10-second brief, across everything)

Capped at **~5 objects, exception-gated**, drawn from **all three pillars** (Process · People · Portfolio) — most absent on a clean day. Each is a *named object with a verb*, badged **HANDLED (veto)** or **YOURS (decide)** (authority-ambiguity guardrail). Bari is at most **one** of these objects.

1. **YOUR DECISION** *(People/Portfolio — only when something is escalated to Tom).* The single highest-stakes call across **everything**: an org tripwire, a person who needs an answer, a calendar conflict only he can resolve. Surfaced as a **framed decision** (upgrade 3): *question + options + CC's recommendation + the one fact*, answerable in 10s. Absent when nothing is escalated. — *Changes: the one thing only Tom can do today.*
2. **INBOX — needs you** *(People; personal layer).* Mail awaiting Tom's reply / time-sensitive / from people who matter, each with a **CC-drafted reply to approve.** Joined to its portfolio item when relevant. Absent when the inbox holds nothing for Tom. — *Changes: whether Tom replies now and approves the draft.*
3. **TODAY / THIS WEEK** *(Process; personal layer).* Calendar: conflicts, missing prep, protected focus gaps, each meeting tied to the decision/portfolio it concerns. The **rhythm/pace verdict** lives here (upgrade 2): is the week on-pace or slipping? — *Changes: how Tom spends the next block.*
4. **HANDLED SO YOU DIDN'T HAVE TO** *(the acid-test ledger — upgrade 1, reframes "Since You Left").* One line: *"absorbed N · escalated M"* + the absorption-ratio trend + any reversible call to **veto.** The emphasis is the *shrinking of Tom's load*, not the activity. — *Changes: whether Tom vetoes an autonomous call.*
5. **GOING WRONG / DECIDE-OR-KILL** *(exceptions + agenda-setting — upgrade 6).* Named faults across the surface (alerts, drift, a person owed a reply too long, a slipping cadence) **and** important-but-untouched items **parked > N days → "decide or kill."** Absent when clean. — *Changes: whether Tom intervenes or kills a stalled thread.*

**The Bari portfolio is a single tile** within this surface — it renders the original 5-object Bari L1 (below) collapsed to **one headline line** when quiet: *"Bari: on-pace — cereals 1 gate from live, nothing needs you."* It expands to the full panel on click. On a clean day, Tom's whole Level 1 can collapse to **#3 + the absorption line**: *"Week's on-pace. I handled 6 things, escalated 0. Bari quiet. Nothing needs you."* That is the target resting state.

#### Level 1 (Bari portfolio panel — the original org L1, now scoped to one lane)
> Retained verbatim from the pre-revision design. This is what the **Bari tile** shows when expanded. "The org" = Bari only. #3 here is superseded in emphasis by the surface-level acid-test ledger (upgrade 1).

1. **YOUR DECISION** *(only if a tripwire-class call is waiting on Tom).* The single highest-stakes escalation: which task/decision, the choice, the recommendation, what it unblocks. Absent when nothing is escalated. — *Changes: the one thing Tom is uniquely required to do.*
2. **NEXT MOVE** *(the org's, named).* `next_action`: task id, owner, one-line reason, what it unblocks. This already exists in the JSON; today it's a fading 9.5px whisper. It becomes a headline. — *Changes: whether Tom redirects the org or lets it run.*
3. **SINCE YOU LEFT** *(autonomous-action ledger; surface emphasis now "handled so you didn't have to").* What CC/agents decided and did since last open — closed N, opened M, 1 reversible call logged. Reversible + autonomous, so Tom can **veto**, not approve. — *Changes: whether Tom reverses an autonomous call.*
4. **GOING WRONG** *(exceptions only).* Open CRITICAL/HIGH alerts, drift, stale decisions, WIP breach — **named** (which task, which blocker), not a "DRIFT/CLEAN" lamp. Absent when clean. — *Changes: whether Tom intervenes on a fault.*
5. **PROGRESS LINE → launch-cadence verdict** *(the anti-vanity signal; upgrade 2 promotes it to a pace verdict).* Live categories N, next category + its single remaining gate, days since last go-live → **on-pace / slipping.** NOT "216 closed." — *Changes: whether Tom believes Bari is advancing.*

On a clean Bari day the panel collapses to **#2 + #5**: *"Next: TASK-184 finishes the cereals re-run → cereals launch. 8 live, cereals 1 gate away, last go-live 4 days ago, on-pace. Nothing needs you."*

### Level 2 — Expandable (the "why")

Reached by clicking an L1 object. Context, not noise. *(Now spans all three pillars, not just Bari.)*

- **The Bari portfolio panel (full)** — the original org L1/L2 board, expanded from its one-line tile. Contains everything below that's Bari-scoped.
- **Direct-reports roster** (People; **upgrade 5**) — each agent as a direct report: *owns X · owes Y · by when · on-pace/slipping · last verified delivery.* Never "busy/online." *Why L2: accountability detail, reached when an L1 object raised "who owns this?"*
- **Decision queue (framed)** (`decisions.json` PENDING; **upgrade 3**) — full pending-decision list, each as question + options + recommendation + the one fact. *Why L2: L1 surfaces only the one escalated to Tom; the rest are being handled.*
- **Calendar — full week** (Process; personal layer) — the whole week with prep/conflict annotations, beyond today's L1 slice. *Why L2: L1 shows only what changes the next block.*
- **Inbox — full triage view** (People; personal layer) — the categorized inbox (needs-reply / FYI / handled), with CC drafts. *Why L2: 95% stays out of L1; this is where the rest lives if Tom wants it.*
- **Open work, grouped by objective** (today's Glass Box / Pending board) — the full Bari in-flight list. *Why L2: Tom needs the next move, not the whole list.*
- **Category factory rollup** (`category_state`) — per-category pipeline→launch state, each non-live linked to its blocking task. *Why L2: the launch-cadence verdict (L1) is the summary; this is the breakdown.*
- **Critical path / dependency chain** (`critical_path`) — longest blocking chain + top unblockers. *Why L2: explains *why* the Bari NEXT MOVE is the next move.*
- **CC review notes** (`cc_comments`) — verify/fyi/blocker stickers per task. *Why L2: per-object detail.*

### Level 3 — Drill-down only (forensic)

- **Closed log** (216 tasks) — collapsed, searchable. *Why L3: history. Zero decision value at a glance; pure audit. Today it's correctly already a collapsed `<details>` — keep that.*
- **Banked assets** — proven-but-not-launched programs (SIE/TASK-171). *Why L3 (demoted from always-open): a banked asset by definition needs **no action now** — its revival is gated on an external trigger. It must never *vanish* (that's why it exists as a section), but it earns a collapsed row, not an open panel. Promote to L1 PROGRESS context only when its `revival_gate` condition is met.*
- **Full alert ledger incl. RESOLVED** — *Why L3: resolved alerts are history.*
- **Per-task frontmatter / raw registry** — *Why L3: the source, for when CC or Tom audits a claim.*
- **Registry-health time-series** (`registry_health_log.jsonl`) — trend, not snapshot. *Why L3: surfaced to L1 GOING WRONG **only** when it shows degradation; otherwise forensic.*

---

### Inline answers to the seven required questions

**(1) What deserves permanent visibility.** Only two things are *unconditionally* on screen: the **NEXT MOVE** (there is always a next move while work is open) and the **PROGRESS LINE** (live-category count is always meaningful). Everything else in L1 is **conditional** — present only when its triggering object exists. A blank L1 (no work at all) shows one honest line: *"No open work. 8 categories live."* Permanent-by-condition, not permanent-by-decoration.

**(2) What to REMOVE (kill-list, justified).**
- **The CC monitoring spine** (`renderSpine`, `spineStats`, `spineVoiceLines`, `startSpineVoice`, all `.cc-spine*` CSS, the scan animation). It reports *CC's posture* via four hollow gauges + a rotating mantra ("registry is truth"). It names no object, changes no decision, and buries the one real signal (`next_action`) in a fading strip. **This is the single biggest thing being killed.** Its *one* real signal (next move) is promoted to L1.
- **The four HUD gauges as gauges** (HEALTH lamp, WIP `n/cap`, BLOCKED count, DRIFT/CLEAN lamp). A gauge that reads CLEAN/GREEN is decoration. Replace with **exception objects**: show the blocked task *named* only when blocked; show drift *named* only when drifting; show nothing when clean. The aggregate health lamp survives only as the L1 GOING WRONG section's on/off trigger.
- **Ambient decoration**: `aurora`, `cc-breathe`, `ip-ping`, `spine-scan`, `hudpulse`, row-flash-on-every-refresh, the breathing CC badge, the 60s auto-refresh repaint. Motion should mean *something changed that matters*, not "the page is alive." Flash is reserved for a real status transition.
- **The agent-chips bar in the header** as a permanent ornament — demote (see Q5).
- **"216 closed" as a headline number anywhere.** It is the vanity metric. It lives only inside the L3 closed log.

**(3) The 3–5 signals Tom must see immediately.** Exactly the L1 set: **YOUR DECISION · NEXT MOVE · SINCE YOU LEFT · GOING WRONG · PROGRESS LINE** — and on a clean day only the last two render. (Real example from today's board: NEXT = TASK-184 → cereals launch; GOING WRONG = TASK-182 blocked on clinician NDA; PROGRESS = 8 live, cereals 1 gate away.)

**(4) How risks/blockers/decisions/opportunities/strategic-drift are represented.** As **named objects in GOING WRONG (L1)**, each carrying *object + verb + what-it-unblocks*, never a count or lamp:
- *Risk/blocker:* the blocked task by id + its blocker text + root unblocker (the engine already computes `_blocking_root`). "TASK-182 blocked — clinician NDA unsigned (external)."
- *Decision:* escalated decisions in YOUR DECISION (L1); all others in the L2 queue. Distinguished by the **tripwire test** (next paragraph).
- *Opportunity:* a first-class new object — a **banked-asset revival trigger firing** or a **category crossing into PRE_LAUNCH**. Derived, not invented: when `category_state` flips to PRE_LAUNCH or a `revival_gate` condition is met, it surfaces as "opportunity: X is ready to launch / revive." This is the proactive Chief-of-Staff move.
- *Strategic drift:* surfaced from the **registry-health time-series** (degradation diff) and from **category staleness** — not "a file changed" (that's SNAPSHOT_DRIFT, mechanical) but "blocked/returned rising, CLOSED dropped, no go-live in N days." Operationalized in the PROGRESS LINE's "days since last go-live" and a health-log degradation flag.

**Autonomy framing (decided-vs-escalated).** Every actionable object is tagged **AUTONOMOUS (reversible — veto)** or **ESCALATED (yours — decide)** by the 5-tripwire test (frozen scores · public-irreversible · start/kill program · spend/legal · redefine-thesis). ESCALATED → YOUR DECISION (L1). AUTONOMOUS → SINCE YOU LEFT ledger (L1, vetoable) or just handled. This is the governance-aware split the current board completely lacks. *(New convention required — see Migration.)*

**(5) How agent status is represented.** **Not as nine always-present avatars.** An idle agent changes no decision. Agent status is represented **only through the work**: each L1/L2 task object carries its owner chip, and the *only* agent-level signal that earns L1 is a **bottleneck** — an owner over the per-owner WIP limit (`owners_over_wip`, already computed) appears in GOING WRONG as "data-agent overloaded (3 tasks)." Otherwise agents are invisible, which is correct: in an autonomous org you watch the *flow*, not the *workers*. The header agent-bar is demoted to L2 (a roster you can open), not a permanent strip.

**(6) How "next action" is determined — the selection algorithm.** **Keep the existing `compute_next_action` ladder verbatim** — it is already concrete and 100% registry-derivable. v2 adds **two things on top** and changes nothing underneath:

```
EXISTING (keep): compute_next_action() priority ladder —
  1. BLOCKED task → recommend its ROOT UNBLOCKER (_blocking_root walks depends_on
     to the deepest unsatisfied actionable ancestor), unless `deferred:`
  2. CHANGES_REQUESTED → rework
  3. IN_PROGRESS tagged to a not-LIVE category → "last gate before <cat> launch"
  4. highest-priority IN_PROGRESS, tie-broken by downstream unblock count
  5. RETURNED → awaiting review
  Fully derived from: status, priority, depends_on/blocks, category_id,
  category launch state, work_type, deferred. No invented data.

v2 ADDS (new, on top):
  0. ESCALATION GATE (runs FIRST): scan open tasks + PENDING decisions for any
     object tripping a tripwire (priority:HIGH + roadmap_impact + no cc_reviewed;
     work_type:go_live; owner == "owner"; decision urgency NOW required_from owner).
     If found → that is YOUR DECISION (L1 #1). The org's next_action ladder still
     runs for NEXT MOVE (#2) — the two are independent: "what only Tom can do"
     vs "what the org does next."
  6. PROGRESS SELECTOR (for the PROGRESS LINE): the single nearest-to-live
     category = min over non-LIVE categories of (remaining gates), where a gate is
     a still-open `blocking_task` or an unmet launch precondition in compute_launch.
     "Next category" = that category; "its one gate" = its blocking_task.
```

Every input is an existing registry/derived field. The escalation gate is the only new logic and it is a pure filter over fields that already exist plus the `owner == "owner"` owner-slug already used today (TASK-182).

**(7) How the board separates activity from real progress.** This is operationalized, not asserted:

- **Activity** (what the current board over-reports): tasks closed, status churn, commits, runs. Defined as: *change in task/registry state.* It is **demoted to L3** (closed log) and **never headlined**. "216 closed" answers "were the agents busy?" — a question Tom should never have to ask of an autonomous org.
- **Real progress** (what v2 headlines): *change in the company's launched surface.* Defined concretely as a **monotonic ladder of irreversible advances**: a category crossing NOT_STARTED → PIPELINE_ONLY → PRE_LAUNCH → **LIVE** (`category_state.launch`), and a **banked asset revived → shipped.** The PROGRESS LINE shows: `live_count`, `next_category + remaining_gate`, `days_since_last_go_live`.
- **The discriminator test:** *"Did the count of live categories, or the distance of the nearest category to live, change since I last looked?"* If yes → progress (headline it). If a task closed but no category moved closer to live → activity (log it, don't celebrate it). Today's board would show "9 closed today!" as if that were progress; v2 shows "cereals moved PRE_LAUNCH→1 gate from LIVE" or, honestly, "no category advanced today" — which is the signal Tom actually needs to know the machine is producing *outcomes*, not just *motion*.

---

## C. Proposed Widgets
> **[REVISED by Revision 1+2]** W1–W9 below are the **Bari portfolio panel** widgets (unchanged). W10–W13 are the **new surface-level widgets** the Chief-of-Staff reframe and the personal layer require. The Bari widgets render *inside* W7's lane; the new ones sit *above* them at the day level.

Each passes the "changes a decision" test. All inputs are existing derived fields unless flagged **(new)**.

### W10 — Inbox Triage `[P0]` *(new — personal layer, People pillar)*
- **Purpose:** Surface only the mail that needs Tom, with a CC-drafted reply to approve; keep ~95% invisible.
- **Inputs:** `integrations/clients/google_workspace.py` (Gmail, read-only) **(new client)**; sender-importance list **(new, local config)**; join keys to `tasks` for the email↔portfolio link.
- **Outputs:** Per surfaced thread: sender · one-line why-it-needs-you · **CC draft reply (approve to send — Tom sends, CC never does)** · linked TASK if relevant. Renders nothing when the inbox holds nothing for Tom.
- **Priority:** P0 — the personal layer's headline value.

### W11 — Calendar / Day `[P0]` *(new — personal layer, Process pillar)*
- **Purpose:** Today/this-week as decisions, not a grid: conflicts, missing prep, protected focus gaps, each meeting tied to its decision/portfolio.
- **Inputs:** `google_workspace.py` (Calendar, read-only) **(new client)**; `tasks`/`category_state` for the meeting↔portfolio join.
- **Outputs:** Next-block view + conflicts + "prep missing for X (draft?)" + protected focus gaps; the **rhythm/pace verdict** (upgrade 2) sits here.
- **Priority:** P0 — the Process pillar's anchor.

### W12 — Decision Queue (framed) `[P0]` *(new — decision architecture, upgrade 3)*
- **Purpose:** Every escalation as a 10-second framed decision, never a naked blocker.
- **Inputs:** `decisions.json` (PENDING), the W1 escalation gate, inbox/calendar escalations, `_blocking_root`.
- **Outputs:** Per decision: **question + 2–3 options + CC's recommendation + the one fact that decides it** + HANDLED/YOURS badge.
- **Priority:** P0 — turns blockers into decisions; the dominant friction-removal move.

### W13 — Direct-Reports Roster `[P1]` *(new — accountability, upgrade 5)*
- **Purpose:** Show agents as direct reports with commitments, never as presence/activity.
- **Inputs:** `tasks` by owner, `owners_over_wip`, `cc_reviewed`/`close_reason` (last **verified** delivery), due/`deferred` fields.
- **Outputs:** Per agent: *owns X · owes Y · by when · on-pace/slipping · last verified delivery.* No "busy/online." Surfaces to L1 only when an owner is a bottleneck or slipping.
- **Priority:** P1 — replaces the demoted agent-chips strip with accountability.

### W1 — Decision Brief `[P0]`
- **Purpose:** Surface the one tripwire-class call only Tom can make.
- **Inputs:** open tasks (`priority`, `roadmap_impact`, `cc_reviewed`, `work_type`, `owner=="owner"`), `decisions` (PENDING, `urgency`, `required_from`), the escalation gate (Section B Q6 step 0).
- **Outputs:** Object + the choice + CC's recommendation + what it unblocks. **Renders nothing when no tripwire is live** (the common case).
- **Priority:** P0 — this is the reason the instrument exists.

### W2 — Next Move `[P0]`
- **Purpose:** The org's single next action, named, as a headline (replaces the buried voice strip).
- **Inputs:** `next_action` (already computed), `critical_path.longest_chain`.
- **Outputs:** task id · owner · one-line reason · "→ unblocks X". One line of critical chain underneath.
- **Priority:** P0 — already computed, currently mis-rendered.

### W3 — Since You Left (autonomous ledger) `[P0]`
- **Purpose:** Show what the org did autonomously while Tom was away, so he can **veto**, not micromanage.
- **Inputs:** `registry_health_log.jsonl` diff since last view **(new: needs a per-view "last seen" marker)**, tasks closed/opened since last snapshot, CC `close_reason` entries tagged autonomous, `cc_reviewed` events.
- **Outputs:** "Since [date]: closed N (cite), opened M, 1 reversible call: [what + why] — [veto]." 
- **Priority:** P0 — operationalizes the autonomy-default safety valve; nothing on the board does this today.

### W4 — Going Wrong (named exceptions) `[P0]`
- **Purpose:** Replace the four CLEAN/GREEN gauges with named faults; loud only when real.
- **Inputs:** `alerts` (OPEN CRITICAL/HIGH), `drift` (counts + named tasks), `owners_over_wip`, stale decisions, health-log degradation flag.
- **Outputs:** Per fault: object + what's wrong + the one fix (alerts already carry `resolution_path`). **Renders nothing when clean** — earned silence.
- **Priority:** P0 — this is the exception-based core principle made concrete.

### W5 — Progress Line (anti-vanity) `[P0]`
- **Purpose:** The honest "is the company moving" signal.
- **Inputs:** `category_state` (launch per category), `compute_launch` gates, `completed_at` of the last LIVE transition **(new: needs a `went_live_at` per category — see Migration)**.
- **Outputs:** "8 live · next: cereals (1 gate: TASK-184) · 4 days since last go-live." Turns amber if days-since-go-live exceeds a threshold (strategic-drift signal).
- **Priority:** P0 — directly answers activity-vs-progress.

### W6 — Opportunity Radar `[P1]`
- **Purpose:** Proactive Chief-of-Staff move: flag when something becomes *ready* (launch or revival), before Tom asks.
- **Inputs:** `category_state` flips to PRE_LAUNCH, `banked_assets[].revival_gate` condition checks.
- **Outputs:** "Opportunity: cereals is ready to launch" / "SIE revival gate met (manufacturer feed live)."
- **Priority:** P1 — high value, but depends on revival-gate conditions being machine-checkable (some are prose today).

### W7 — Open Work Board (grouped) `[P1]`
- **Purpose:** The full in-flight list (today's Glass Box/Pending board), as **L2 context**, not the front page. Hosts the W1–W6/W8/W9 Bari widgets inside the Portfolio lane.
- **Inputs:** open `tasks` grouped by objective, `cc_comments` stickers, `cc_reviewed`/`close_reason` for the trust badge.
- **Outputs:** Existing objective/sub-task rows with action buttons. Largely **the current `render()` board, demoted one level.** Every CLOSED/done row carries the **verified-trust badge (upgrade 4):** "✓ verified by CC against artifacts" when `cc_reviewed` is set, vs "agent claims done" when not — provenance on the surface, not buried in `close_reason`.
- **Priority:** P1 — keep what works; just stop it being the headline.

### W8 — Category Factory Rollup `[P1]`
- **Purpose:** The breakdown behind the PROGRESS LINE.
- **Inputs:** `category_state`, `categories` (bsip0/1/2/qa/dataset/website).
- **Outputs:** Per-category pipeline→launch lane, each non-live linked to its blocking task.
- **Priority:** P1.

### W9 — Closed / Banked / Forensic `[P2]`
- **Purpose:** History and proven-but-parked assets, available, never loud.
- **Inputs:** CLOSED tasks (archive), `banked_assets`.
- **Outputs:** Collapsed, searchable. Banked assets demoted from open to collapsed (revival-gated, no action now).
- **Priority:** P2 — keep the current collapsed `<details>` behavior; demote banked from `open`.

---

## D. Jarvis-style Executive Cockpit recommendation

"Jarvis" is the right north star **if** we read it correctly. Jarvis is not a glowing UI — it's an agent that has **already done the work**, has an **opinion**, **acts within its authority**, and **briefs in one sentence.** The cockpit feeling comes from *agency and brevity*, not from animation. The current board mistakes *ambient motion* for *aliveness*; that is the trap to avoid.

**Make it feel like a company OS, concretely:**

1. **Lead with a spoken-style brief, not a board.** The top of the screen is one CC-authored paragraph in plain English (the morning-digest voice already exists in `emit_digest`): *"Morning. The org closed the Glass Box methodology page and shipped it overnight — nothing needed you. One thing: the clinician hasn't signed the NDA, so TASK-182 is parked; that's external, I'm holding it. Next, the cereals re-run finishes today and cereals goes live — your call only if you want to gate it. Otherwise we're clear."* This is **data we already have** (`next_action`, `alerts`, `category_state`, `banked_assets`, autonomy tags) composed into prose. **This is the single highest-leverage build** — it makes the instrument feel like a Chief of Staff with one rendering change.

2. **Authority-aware framing everywhere.** Every object wears one of two badges: **HANDLED (veto)** or **YOURS (decide)**. The cockpit feeling is *"the machine is running itself and showing me only the seams."* This is the governance matrix made visible — uniquely possible here because Bari actually has a codified 5-tripwire authority model.

3. **The ledger is the trust engine.** An autonomous org is only delegable if Tom can see and reverse what it did. W3 (Since You Left) is what lets him *stop reading the board daily* — the deepest cockpit property: **you trust it enough to look less.**

4. **Silence as a feature, with a heartbeat — not a light show.** When clean, the screen says so in words and goes quiet. One subtle, *meaningful* pulse is allowed: a single dot that beats only when CC last verified the board is truthful (ties to `drift.checked_at`). That's the one piece of "alive" worth keeping — it signals *the watcher is awake*, not *the page has animations*.

**What needs new instrumentation (flagged honestly):**
- **Per-view "last seen" marker** (for W3) — the dashboard has no memory of when Tom last looked. Needs a tiny client-stored or file-stored timestamp. *Low effort, no engine change.*
- **`went_live_at` per category** (for W5 "days since last go-live") — `category_state` has launch *status* but not the *date it became LIVE*. Needs a derived or recorded timestamp. *Medium — can be derived from the go-live task's `completed_at`.*
- **Machine-checkable `revival_gate`** (for W6) — today some gates are prose ("when a manufacturer feed exists"). Opportunity Radar only fires for gates expressible as a check. *Accept partial coverage at MVP.*
- **Autonomy tag on close events** (for W3 ledger) — whether a close was autonomous or owner-gated. *Low — derivable from `cc_reviewed`/`work_type`, or one new frontmatter field.*

Everything else — the brief, the named exceptions, the progress line, the authority badges — is **composable from fields the generator already produces today.** The cockpit is mostly a **render contract**, not new data.

---

## Keep / Kill / Build

| Current element | Verdict | Why |
|---|---|---|
| `generate_dashboard.py` derivation engine | **KEEP** | The whole reason the board can be trusted; v2 is a render change, not a data change |
| Registry-authoritative, JSON-derived rule | **KEEP** | Foundational; never hand-edit JSON (Hard Rule 1) |
| `next_action` ladder + `_blocking_root` | **KEEP** | Concrete, registry-derivable; promote from whisper to headline |
| `critical_path`, `category_state`, `drift`, `banked_assets` blocks | **KEEP** | Already computed; v2 surfaces them correctly |
| Drift model (PHANTOM/CLOSURE/SNAPSHOT/UNPARSEABLE) | **KEEP** | Sound; feeds GOING WRONG as named faults |
| `cc_comments` stickers | **KEEP** (demote to L2) | Per-object detail, not front-page |
| Open-work objective board (`render()`) | **KEEP** (demote to L2) | Good list; just not the headline |
| Closed log (collapsed `<details>`) | **KEEP** (L3) | History; already correctly collapsed |
| **CC monitoring spine** (spine + voice strip + scan) | **KILL** | Reports posture not objects; buries the real signal — *biggest kill* |
| Four HUD gauges *as gauges* | **KILL** (→ exceptions) | CLEAN/GREEN lamps are decoration; replace with named faults |
| Ambient animation (aurora, breathe, ping, flash-on-refresh) | **KILL** | Motion must mean change, not "alive" |
| Header agent-chips strip (permanent) | **DEMOTE** (→ L2 roster) | Idle agents change no decision |
| "216 closed" as any headline | **KILL** | The vanity metric; lives only in L3 |
| Banked assets `<details open>` | **DEMOTE** (→ collapsed) | Revival-gated; no action now (but must stay visible) |
| **BUILD: CC morning brief (prose lead)** | **BUILD** `[P0]` | Highest-leverage cockpit feel; composes existing fields |
| **BUILD: Decision Brief + authority badges** | **BUILD** `[P0]` | Makes the governance split visible (unique to Bari) |
| **BUILD: Since-You-Left ledger** | **BUILD** `[P0]` | The trust engine for autonomy-default |
| **BUILD: Progress Line** | **BUILD** `[P0]` | Operationalizes activity-vs-progress |
| **BUILD: Opportunity Radar** | **BUILD** `[P1]` | Proactive; partial coverage OK at MVP |
| Whole surface = **Tom's Chief of Staff** (Bari = 1 portfolio tile) | **REFRAME** | Rev 1; owner decision of record — top surface is Tom's day, not Bari's board |
| **BUILD: W10 Inbox Triage** (read-only Gmail) | **BUILD** `[P0]` | Rev 2; personal-layer headline value — needs only that mail reach Tom |
| **BUILD: W11 Calendar / Day** (read-only Calendar) | **BUILD** `[P0]` | Rev 2; Process pillar anchor; ties meetings to portfolio |
| **BUILD: W12 Decision Queue (framed)** | **BUILD** `[P0]` | Upgrade 3; never a naked blocker — question+options+rec+fact |
| **BUILD: W13 Direct-Reports Roster** | **BUILD** `[P1]` | Upgrade 5; agents as accountability, not presence |
| **BUILD: Absorption-ratio KPI** (handled÷escalated, trended) | **BUILD** `[P0]` | Upgrade 1; CC's own acid-test metric — the anti-vanity headline |
| **BUILD: Decide-or-kill (parked > N days)** | **BUILD** `[P1]` | Upgrade 6; agenda-setting — important-but-untouched, not just blocked |
| **BUILD: Verified-vs-claimed trust badge** | **BUILD** `[P1]` | Upgrade 4; provenance on the surface (✓ verified vs claims done) |
| **BUILD: Launch-cadence pace verdict** (on-pace/slipping) | **BUILD** `[P1]` | Upgrade 2; CC owns the rhythm, not just the task list |
| Activity / vanity counters as any headline | **KILL** (reaffirmed) | Failure-mode guardrail — a board that brags about activity is failing |

---

## Migration note — can v2 be derived from today's registry?

**~80% yes, from fields that already exist.** L1 #2 (Next Move), #4 (Going Wrong), #5 (Progress Line minus the date), all of L2/L3, and the prose brief compose directly from `next_action`, `alerts`, `drift`, `category_state`, `critical_path`, `banked_assets`, `owners_over_wip`, and `cc_comments`. **No engine rewrite — it is a render-contract change to `command_center.html` plus a thin composition layer.**

**New conventions v2 requires (small, bounded, all default-safe):**

1. **`authority:` frontmatter** — `autonomous` | `escalated` (default `autonomous`, per autonomy-default law). Drives the HANDLED/YOURS badge and the W1 escalation gate. *Today inferred imperfectly from `owner=="owner"` + `roadmap_impact`; an explicit field is cleaner and matches the 5-tripwire matrix.*
2. **`went_live_at:`** (or generator-derived from the go-live task's `completed_at`) per category — enables "days since last go-live" and the strategic-drift amber. *Prefer deriving it over a new field.*
3. **A per-view "last seen" timestamp** — client- or file-stored, outside the registry — to power the Since-You-Left ledger. *Not a registry change; a dashboard-state file.*
4. **Machine-checkable `revival_gate`** on banked assets — optional structured form alongside the prose, so Opportunity Radar can fire. *Partial adoption acceptable.*

None of these break the existing generator (all optional, default-safe — the same discipline `work_type`/`drift_ack`/`roadmap_impact` were added under). **No category data, scores, or pipeline logic are touched.** This is a proposal: **owner sign-off required before any build**, since it reshapes Tom's primary instrument and go-live of that instrument is owner-gated.

### New instrumentation the revisions require (Rev 1 + Rev 2)

Beyond the four Bari conventions above, the Chief-of-Staff reframe and the personal layer add:

5. **`integrations/clients/google_workspace.py`** — read-only Gmail + Calendar REST client, OAuth refresh-token, **local-only**, on the existing EDPG read-only client pattern. *Tom is building it in parallel; the board only consumes it.* No write path should exist in the client.
6. **A local, gitignored token store** — the OAuth refresh-token (and any cached creds) live only on Tom's laptop, never committed, never synced. Add the path to `.gitignore` before any token is written. This is the load-bearing privacy control.
7. **A local sender-importance / people-that-matter config** — drives which inbox items reach L1. Local config, not registry; no PII in the repo.
8. **Absorption-ratio metric** (upgrade 1) — `decisions_absorbed ÷ decisions_escalated`, trended. Derivable from `registry_health_log.jsonl` (close/escalate events) + a small escalation tally; add to the health log rather than a new store.
9. **A `parked_at` / staleness derivation** (upgrade 6) — "important-but-untouched > N days" needs a last-touched timestamp per open object; derive from existing registry mtimes / status-change history, plus a tunable `N`.
10. **A pace/cadence baseline** (upgrade 2) — expected launch interval to judge on-pace vs slipping; a single tunable constant, no new data source.

All of 5–10 are **additive, local-or-derived, and default-safe**; none touch scores, category data, or the derivation engine's correctness. The personal layer is **read-only by construction**.

---
*cc-agent — TASK-186 — 2026-06-05 — PROPOSAL, pending owner sign-off*
*Revised 2026-06-05 (Rev 1: CC = Tom's Chief of Staff, Bari = 1 portfolio; Rev 2: read-only Gmail+Calendar personal layer; +6 CoS-practice upgrades) — owner decisions of record, build still pending owner sign-off*
