---
document: additive_library_maintenance_protocol_v1
task: TASK-181C
program: TASK-181 (Glass Box program-of-record) — Wave 3, D4 additive library
owner: product-agent
status: RETURNED (proposed; CC close-readiness gate to verify)
created_at: 2026-06-04
related: TASK-181A (expanded library) · TASK-181B (tiered library) · TASK-181D (Data wiring)
registry: EV-043 (tier assignments) · EV-041 (tier model + detector)
---

# Additive Library Maintenance Protocol v1 — Glass Box W3 (D4)

**Purpose.** The D4 additive library is the program's **named dominant risk**: an
evidence-curated dataset only stays correct if someone keeps re-checking it against the
authorities it cites (EFSA / JECFA / FDA / IARC). A stale "evidence-aware" additive panel is
worse than no panel — it spends Bari's credibility on a number that is quietly wrong. This
protocol defines the refresh cadence, ownership, staleness alerting, and — the load-bearing
part — **the Product go/no-go gate that decides whether the library is worth its ongoing
maintenance cost at all.**

**Scope boundary (inherited, hard).** This protocol governs the maintenance of an
**annotate-only** library. Nothing here authorizes D4 to move a headline grade. Score
integration is a separate, future, owner-gated decision (frozen-invariant tripwire #1) and is
explicitly out of scope. Maintaining the library does not pre-commit to ever scoring with it.

---

## 1. Refresh cadence

The library is **import-and-curate**, not live-per-product, so the maintenance unit is a
periodic review pass, not a per-page lookup. Two cadences run in parallel:

### 1.1 Scheduled cadence

| Pass | Frequency | What it re-checks | Owner |
|---|---|---|---|
| **Annual full re-verify** | every 12 months | Every additive's cited ADI / tier re-confirmed against the current EFSA/JECFA/FDA position; any authority opinion superseded since last pass is pulled and re-read. | Nutrition (executes) → Product (signs the delta) |
| **Quarterly light scan** | every 3 months | Cheap watch-list scan only: EFSA "Latest" re-evaluation feed + JECFA meeting reports + IARC monograph announcements, filtered to the 36 shelf-present additives. No re-tiering unless a hit. | Data/Research (scan) → Nutrition (triage hits) |

The **36 shelf-present additives** are the maintenance surface — not the full E-number space.
This is the standing guardrail: a new additive enters the library only when it is **observed
on a displayed shelf** (a 181A-style corpus pass surfaces it), never speculatively.

### 1.2 Trigger events (force an off-cycle review)

Any of these fires an immediate single-additive review, independent of the calendar:

1. **A new EFSA re-evaluation opinion** is published for a library additive (EFSA is on a
   rolling re-evaluation programme for all pre-2009 additives — these land unpredictably).
2. **A JECFA ADI change** (new "not specified" → numeric, or a numeric tightening) at a JECFA
   meeting.
3. **An IARC reclassification** of a library additive (e.g. a 2B → 2A move, or a new listing).
4. **An FDA action** — a GRAS withdrawal, a ban, or a CFR change — affecting a library
   additive (this is the channel that would, e.g., flip a `functional` to `contested`).
5. **A high-quality new primary study** (pre-registered human RCT, or a mechanistic finding
   that materially changes a `contested`/`likely-neutral` call) — Nutrition's judgment whether
   it crosses the bar; the E407 carrageenan and E466 CMC entries are the live examples of
   tiers that a single strong RCT could move.
6. **A new additive appears on a displayed shelf** that is not in the 36 — adds a row, runs
   the 181A→181B mini-pipeline (Research evidence → Nutrition tier → Product co-sign).

A trigger-event review re-tiers only the affected additive(s) and is recorded as a delta in
EV-043 (or its successor), with Product co-signing any tier change.

---

## 2. Ownership + staleness alerting

### 2.1 Ownership (RACI, lean)

| Concern | Owner |
|---|---|
| **Library correctness** (tiers match current evidence) | **Nutrition Agent** — accountable. Holds the tier verdicts; executes the re-verify and triages trigger hits. |
| **Evidence sourcing** (the EFSA/JECFA/FDA cites + the watch-list scan) | **Research Agent** (evidence) + **Data Agent** (the scan tooling / staleness instrumentation). |
| **The go/no-go gate + scope** (is it worth maintaining; demand revisit) | **Product Agent** — this document. |
| **The wired artifact** (`GLASSBOX_W2_ADDITIVES` / W3 successor in `constants.py`) | **Data Agent** — applies a signed tier delta; never re-tiers. |

No new role is created. The library rides the existing agent stack; the cost is review-time,
not headcount.

### 2.2 Staleness detection / surfacing

Staleness must be **visible without anyone remembering to look.** Mechanism:

1. **Per-entry `last_verified` date.** Every additive row in the tiered library and EV-043
   carries the date its tier was last confirmed against live authority text.
2. **Staleness threshold = 15 months.** Any additive whose `last_verified` is older than 15
   months (the 12-month cadence + a 3-month grace) is **stale**. The annual pass resets all 36.
3. **Surfacing — two channels (no new infra):**
   - **Command Center.** A derived staleness count surfaces on the dashboard the same way
     banked-asset / drift state already does — `generate_dashboard.py` reads the `last_verified`
     dates and emits a "D4 library: N additives stale / next re-verify due <date>" line. This
     is the always-on radar; it is registry-derived, never hand-edited.
   - **Watch-list scan output.** The quarterly scan writes its hit list (authority changes
     touching the 36) into the same channel, so a trigger-event surfaces as a dashboard item,
     not an email someone misses.
4. **A stale-but-live library is itself a go/no-go input** (see §3): if the dashboard shows the
   library has been stale past threshold and no re-verify is scheduled, that is evidence the
   maintenance commitment is not being honored — which is a freeze signal, not a "try harder"
   signal.

---

## 3. The Product go/no-go gate (the named dominant risk)

**The question this gate answers:** *is the additive library worth its ongoing maintenance
cost?* It is asked at every annual re-verify, and on demand whenever a freeze signal fires.

### 3.1 The decision rule

The library is **KEEP / SCALE** only if **all three** hold:

1. **Correctness is sustainable.** The last annual re-verify completed on cadence, and the
   stale count on the dashboard is 0 (or has a scheduled, owned re-verify clearing it). If the
   library is chronically stale, it fails here regardless of demand — an un-maintained
   evidence library is the risk this whole protocol exists to prevent.
2. **The shelf surface is bounded.** The maintenance surface is still "shelf-present additives,"
   not creeping toward the full E-number space. If the row count is ballooning because the
   guardrail eroded, scope is cut back before scaling continues.
3. **Demand is not disproven.** See §3.2 — the bypassed-gate clause. The default is KEEP
   (owner already chose to scale on product judgment); demand evidence can only move this to
   FREEZE, it is not re-litigated from zero each pass.

If any one fails → **FREEZE** (stop adding additives, stop re-verifying beyond what keeps the
live set honest, leave the panel as-is or hide it pending an owner call). **FREEZE is a
legitimate, expected outcome — not a failure of the program.** A go/no-go gate that can only
say "go" is theatre.

### 3.2 Demand-revisit checkpoint (the bypassed W2 gate)

**Provenance, recorded.** W3 was designed as the expensive, maintenance-heavy bet **gated on
proven consumer demand** (the W2 engagement gate, TASK-179X: 5/8 unprompted panel opens · 8/12
comprehension · 20% live panel-open rate). That gate was **closed by owner override on
2026-06-04 without engagement data** — none of the three thresholds was measured. W3 therefore
proceeds on **owner product judgment, not measured engagement.** This protocol exists partly to
carry that unpaid debt forward so it does not silently disappear.

**The checkpoint.** When **live panel-open instrumentation arrives** (Plausible
`breakdown('event:page')` / a panel-open custom event — the `analytics` client named in the
Product External Data section, currently NEEDS-ENV-VERIFY), Product runs a one-time
demand-revisit before authorizing any further scaling (W3.x library growth, or any move toward
score integration). Usage informs **priority/order, never a product's quality/score** — the
same hard fence as Trends.

**What evidence triggers a "no-go / freeze the library" call:**

- **Engagement is near-zero.** If, once instrumented, the AdditivePanel is opened on **< ~5%**
  of comparison-page sessions that reach a page carrying it (directionally at/below the floor
  the W2 gate's 20% target implied a healthy panel should clear), the demand premise that
  justified the maintenance cost is **disproven by data**, not just unmeasured → **FREEZE**:
  stop scaling, keep the live 36 honest only if cheap, and route a keep-or-retire decision to
  the owner.
- **Comprehension fails in the wild.** If instrumentation or a light moderated check shows users
  open the panel but it does not change their read of the product (bounce-without-engagement,
  or it tests as confusing), the panel is cost without user value → **FREEZE** pending a content
  rework, not a library expansion.
- **Maintenance is not being honored.** If two consecutive annual re-verifies slip (dashboard
  stale count stays > 0 with no owned re-verify), the org has revealed it will not pay the
  maintenance cost → **FREEZE and consider retiring**, because a stale evidence library is the
  dominant risk realized.

If instrumentation shows **healthy engagement** (panel opens comfortably above the floor, and
comprehension holds), the demand premise is retroactively **confirmed** and the bypassed-gate
debt is cleared — KEEP/SCALE proceeds on data rather than judgment. That is the good outcome,
and the checkpoint is how we earn it rather than assume it.

**Authority note.** The freeze/keep call within the annotate-only library is Product's
(reversible, no grade moves, no consumer claim retracted — the panel is additive display copy).
**Score integration** remains owner-gated regardless of demand (tripwire #1). So the worst this
gate can do autonomously is hide/freeze a display feature — safely reversible.

---

## 4. The EFSA OpenFoodTox bulk-import decision (routed from 181A)

**The gap.** 181A (§4) found: the live `food_additives` client (OFF taxonomy) gives identity +
class + an EFSA-eval *pointer*, but **not numeric ADI values** and **not** the Israel-vs-EFSA
divergence. EFSA numeric ADI and JECFA ADI have **no free per-substance REST API** — 181A had
to web-scrape opinion PDFs per substance. `openfda.py` covers recalls/adverse-events, **not**
GRAS/CFR substance status. 181A recommends a one-time **EFSA OpenFoodTox bulk import**
(a downloadable substance-level hazard/reference-point dataset) to close the numeric-ADI gap
inside the import-and-curate model.

**Decision: DEFER to a later wave (do not wire now). Conditionally — wire it the moment EITHER
(a) the demand-revisit checkpoint confirms engagement, OR (b) score integration is opened by
the owner.** Until then, keep the per-substance web-scrape + carried-forward prototype numbers.

**Rationale (Product):**

- **The gap is real but not currently load-bearing.** The 36 additives are already tiered, with
  every numeric ADI sourced (carried-forward or web-located) and cited per entry. The library
  is **complete and co-signable today without OpenFoodTox.** The import buys *efficiency on the
  next re-verify*, not correctness now — it removes a manual scrape step, it does not unblock W3.
- **Annotate-only doesn't need numeric precision yet.** Numeric ADI matters most when a number
  drives a *score* (you need a defensible exposure-vs-ADI margin). In annotate-only display, the
  tier + a one-line justification is what the user sees; the precise mg/kg figure is governance
  provenance, which a cited web source already satisfies. **Spending the integration cost before
  the demand gate clears would repeat the W3 mistake** — paying for the expensive infrastructure
  ahead of proven need — at the integration layer this time.
- **It is cheap to defer and cheap to do later.** OpenFoodTox is a static-ish bulk dataset; the
  import is a bounded one-time job whenever we want it. Deferring loses nothing but a scrape step
  on the annual re-verify; it does not decay. So the option value of waiting is free.
- **What would flip it to "wire now."** If the annual re-verify becomes painful at 36 additives
  (the web-scrape step is the bottleneck), or the moment score integration opens (where numeric
  margins become load-bearing) — wire it then. That is the natural trigger, and §1.2 trigger
  events will surface the need.

**Maintenance-cost implication.** Deferring **keeps maintenance cost flat-to-lower now** (no new
data pipeline to own, version, and re-validate). When wired later, OpenFoodTox **reduces** the
recurring re-verify cost (replaces the per-substance scrape with a cached dataset refresh) at the
one-time cost of building + owning the importer — a cost worth paying once volume or score-need
justifies it, not before. **The Israel-MoH divergence gap has no free source and stays a
documented limitation** (a D5 disclosure-note candidate, never a D4 tier driver), not a blocked
task. JECFA monograph index: same DEFER call, same triggers.

---

## 5. Summary — what this protocol commits Bari to

1. **Annual full re-verify** (Nutrition executes, Product signs the delta) + **quarterly light
   scan** of the 36 shelf-present additives, plus **6 trigger events** that force off-cycle review.
2. **Ownership on the existing stack** (Nutrition correctness · Research/Data evidence+scan ·
   Product gate · Data wires signed deltas) — no new role.
3. **Staleness surfaced on the Command Center** via per-entry `last_verified` + a 15-month
   threshold; staleness is itself a go/no-go input.
4. **A Product go/no-go gate** with a real FREEZE outcome, run every annual pass, gated on
   correctness-sustainability + bounded-shelf-surface + demand-not-disproven.
5. **A demand-revisit checkpoint** that pays the bypassed-W2-gate debt: on live instrumentation,
   < ~5% panel-open / comprehension-fail / unhonored-maintenance each trigger a FREEZE; healthy
   engagement clears the debt and confirms KEEP.
6. **EFSA OpenFoodTox: DEFER**, wire on demand-confirm OR score-integration-open; keep the
   web-scrape until then; Israel-MoH divergence stays a documented D5 limitation.

**Annotate-only throughout.** No grade movement is authorized by this protocol. No score moved,
no JSON edited, no engine code touched. Frozen invariants (milk run_005_headpin / snack 70/B /
bread provenance) untouched.

**Proposed task status:** RETURNED for CC close-readiness verification. CC records CLOSED.
