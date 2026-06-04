---
document: w2_engagement_gate_spec_v1
task: TASK-179R
status: DRAFT_PENDING_PRODUCT_LOCK
created_at: 2026-06-04
go_nogo_locked: true  # Locked 2026-06-04 — autonomous product decision, no tripwire fired; CC verified
---

# Glass Box W2 — Engagement Gate Specification v1

**Author:** Product Agent  
**Date:** 2026-06-04  
**Wave:** TASK-179, Wave 2  
**Reads-first (binding):**
- `01_framework/glass_box/six_dimension_contract_v1.md` — D4 scope, asymmetric-by-design taxonomy
- `01_framework/glass_box/d5_d6_rule_spec_v1.md` — DEC-006 Q3 posture; no alarm framing for contested/dose-dependent
- `01_framework/glass_box/w0_product_cosign_v1.md` — Q3 ceiling: contested aggregate ≤ ~one grade band; "explain plainly, do not alarm"
- `01_framework/frontend/architecture_generations_registry_v1.md` — Gen 0 patterns are forbidden

**Gate purpose:** D4 (additive evidence library) is a demand-gated bet. Engineering cost is only justified if consumers
engage the additive panel in practice. This spec defines in advance what "engage" means and at what quantitative
threshold W3 (full library at scale) opens. These thresholds are locked before the prototype exists and cannot be
revised after data arrives.

**If the gate fires:** W3 opens (full additive library, EFSA/JECFA/FDA wiring, maintenance protocol).  
**If the gate does not fire:** D4 is parked. Glass Box ships as D1+D2+D3+D5+D6 without D4. This is an explicitly
pre-approved, acceptable outcome — it is not failure. It means we built the right cheap things and skipped the
expensive wrong one.

---

## 1. Session Protocol

### 1.1 Format

- **Volume:** 5–8 moderated sessions. 5 is the minimum to draw conclusions; 8 is the ceiling (returns
  diminish quickly for a comprehension/engagement test, and over-recruiting signals are cheap).
- **Mode:** Remote preferred (screen-share + verbal think-aloud via Zoom or equivalent). In-person acceptable
  if remote recruitment proves difficult. Remote is preferred because it matches the real smartphone-in-hand
  context and makes session recording straightforward.
- **Duration per session:** 30–40 minutes. The actual test tasks are short; the extra time is for settling,
  intro, and the exit question. Do not run longer — fatigue changes engagement behavior.
- **Pilot session:** Run one unpaid pilot with a non-target-user (e.g. a team member who has not seen the
  prototype) before any paid recruits see it. Validate that the task list is clear, timing is realistic, and
  the recording setup works. Pilot session data is excluded from the gate calculation.

### 1.2 Stimulus

A live or Figma-prototyped page for the **hummus category** (preferred over maadanim for W2: fewer products,
cleaner BSIP0 panels, lower additive density — a harder test for panel engagement; if the panel gets attention
here, it will get attention in a more additive-dense category). The page must be at prototype fidelity — not a
wireframe. Specifically:

- The top section shows the shelf: product rows with score chips and insight lines, exactly as on the live
  maadanim page (canonical Gen 1 pattern).
- Below the score section and above the nutrition table, the additive panel is **visible but collapsed** on
  load. The collapsed state shows a single entry point: "X תוספים — הצג פירוט" (see §5 for the precise
  visual spec).
- Two or three hummus products in the prototype should have non-trivial additive panels (e.g. a product with
  a carrageenan-class contested additive and one with only functional/neutral additives) to create genuine
  differences between products. The contrast is load-bearing: users need something to compare.
- Products with no detected additives should show the empty state (§5.6).

The moderator does not describe the additive panel before Task 3. It is visible, but the user is not directed to it.

### 1.3 Task List (three tasks per session)

**Task 1 — Find a product.**  
"You are in a supermarket looking for hummus. You have ~15 seconds at the shelf. Using this page, find the
product you would consider buying and tell me when you have chosen."  
*Measure:* time-to-selection; does the user look at the score chip before other elements? (screen recording + think-aloud)

**Task 2 — Understand the grade.**  
"You chose [product X]. What does its grade tell you? What does it mean to you?"  
*Measure:* comprehension accuracy: does the user understand the grade as a within-shelf relative ranking
(acceptable answer) or interpret it as an absolute health verdict (failure indicator)? Score binary.

**Task 3 — Explore the additive panel.**  
"Take another look at this product page. Is there anything else here that would affect your decision?"  
*Measure:* Unprompted interaction: did the user open or tap on the additive panel entry point **without being
told to?** Record binary (yes/no) and note the time elapsed before they noticed it (or confirm they did not).  
If the user opens the panel (unprompted), let them explore freely before asking Task 3 follow-up.  
If the user does not open the panel after a reasonable pause (~45 seconds of free exploration), the moderator
may say: "I notice there is one section of the page you haven't looked at yet — is there anything you haven't
tried?" This is a single soft prompt, not a direct instruction.

**Task 3 follow-up (comprehension — 30 seconds post-exploration).**  
After the user has had any contact with the additive panel (prompted or unprompted), wait 30 seconds and ask:  
"Can you tell me in your own words what that panel was telling you about this product?"  
*Measure:* comprehension score (see §2.3 for operationalization).

### 1.4 Session Measures

| Measure | Collection method | Type |
|---|---|---|
| Time-on-panel | Screen recording; moderator notes timestamp of panel open + close | Quantitative (seconds) |
| Unprompted interaction | Moderator binary rating during session | Binary (yes/no) |
| Grade comprehension (Task 2) | Moderator binary rating from think-aloud: relative ranking vs absolute verdict | Binary (pass/fail) |
| Additive panel comprehension (Task 3 follow-up) | Moderator rating against §2.3 rubric | Binary (pass/fail) |
| Exit question response | Verbatim transcript | Qualitative (yes/no/conditional) |

**Exit question (asked at the end of every session, verbatim):**  
"Based on what you just saw — the additive panel, the tier labels, the explanations — would you use this to
decide between two similar products at the supermarket?"  
Record the answer verbatim. Binary classification: yes / conditional-yes (e.g. "yes, if it covered more
products") / no. Do not prompt or elaborate. Conditional-yes counts as yes for gate purposes (it means the
feature is valuable but the corpus is the barrier, not the concept).

### 1.5 Screening Criteria for Recruits

**In:** Israeli residents; primary smartphone user (uses phone for at least 50% of digital activity including
shopping); reads Hebrew fluently; does regular grocery shopping at least once per week; any age 22–55;
any education level.  
**Out:** Registered dietitians, nutritionists, food scientists, medical professionals (their professional
knowledge contaminates comprehension results); Bari employees or people who have previously tested a Bari
prototype; people who currently use Yuka or a similar additive-scanning app (their prior mental model of
additive tiers makes the comprehension test trivially easy and inflates the result).  
**Balance:** Target at least 2 sessions with users who have expressed concern about food additives in a
screening question ("how much do you think about food additives when shopping?") and at least 2 with users
who have not. This controls for the risk that only already-concerned users engage the panel.

---

## 2. 15-Second Comprehension Test

### 2.1 Stimulus

A single additive tier card rendered at prototype fidelity. The card must represent the **dose-dependent** tier
(not confirmed-negative, not likely-neutral — those are too easy; dose-dependent is the hardest and most
consequential to communicate because it requires conveying nuance without alarm framing, per DEC-006 Q3).

The card shows:
- The tier chip (visual encoding per §5.5 — warm amber chip, label "תלוי במינון")
- The additive's Hebrew common name: e.g. "ניטריטים (E250)" — human name first, E-number in parentheses
- One-line Hebrew explanation: "כמות נמוכה — לא צפוי להשפיע. בכמות גבוהה יש דיון מדעי על בטיחות לטווח ארוך."
- The "עוד" expand link is visible but collapsed; the expanded state is not shown during the 15-second window.

The card must be shown on a phone-sized screen (375px width), not a desktop. The test is for smartphone interaction.

### 2.2 Procedure

1. The tester sees the card on a phone screen for exactly 15 seconds. They may tap or interact normally.
2. After 15 seconds the card disappears (or the tester is asked to stop looking).
3. The tester answers verbally or in writing: "What does this mean for this product?"

### 2.3 Success Criterion — What "Correctly Identifies" Means

A response is scored **pass** if it demonstrates all three of the following:

1. **Tier awareness:** The tester indicates that the additive has some conditional or context-dependent quality
   — not uniformly bad, not uniformly fine. Acceptable phrasings include anything conveying "depends on amount,"
   "at low levels OK," "high levels could be a concern," "not clearly safe or unsafe." A response of simply
   "this is dangerous" or "this is fine" fails this criterion.

2. **No alarm:** The tester does not characterize the additive as "toxic," "poisonous," "harmful," "causes
   cancer," or equivalent alarm-register language. A calm acknowledgment of uncertainty ("there's some
   discussion about it") passes; a fear verdict fails. This criterion directly tests whether the DEC-006 posture
   (no alarm framing for contested/dose-dependent) holds at the consumer level.

3. **Product relevance:** The tester connects the finding to the *product* ("this product has something that..."
   or "the hummus contains..."), not just to the abstract molecule. A purely theoretical answer ("E250 in general
   is...") that does not connect to the product at hand fails this criterion.

A response must pass all three criteria to count as a pass. If the tester cannot answer at all (blank response),
it is a fail.

**Scoring:** The rater applies the three criteria independently and records pass/fail for each, then derives
the overall pass/fail. Two raters should score independently for sessions where the response is ambiguous; in
case of disagreement, the more conservative rating (fail) stands.

### 2.4 Minimum N and Threshold

- **Minimum testers:** 12 people complete the 15-second test (separate from the moderated sessions — this is
  a standalone timed card test, recruitable from the same pool but run in a separate brief session of ~5 minutes).
  12 is the floor; 15 is preferred for a tighter confidence interval.
- **Go threshold:** **≥ 8 out of 12 pass** (≥ 67%) — or, if N=15, **≥ 10 out of 15 pass** (≥ 67%).
  The 67% threshold is the decision: the additive tier system is communicating clearly enough that a
  supermajority of non-expert shoppers can correctly identify the tier meaning after a 15-second glance.
  Below this threshold the card design fails comprehension and must be revised before W3 opens (the design
  problem, not the demand problem, is the barrier).

---

## 3. Instrumentation Plan

### 3.1 Events to Instrument

All event names are in English (analytics layer convention). All fire as anonymous aggregate events — no user
ID, no session ID, no device fingerprint.

| Event name | When it fires | Parameters |
|---|---|---|
| `additive_panel_open` | User taps/clicks the additive panel entry point and the panel expands | `category: string`, `product_id: string` (anonymous shelf position, not linked to user) |
| `additive_panel_close` | User collapses the additive panel | `category`, `product_id`, `time_open_ms: int` |
| `tier_card_expand` | User taps the "עוד" link on any individual tier card | `category`, `product_id`, `tier: string` (one of 6 tier values) |
| `tier_card_collapse` | User collapses the tier card detail | `category`, `product_id`, `tier` |
| `scroll_past_additive_panel` | User scrolls below the additive panel section without opening it | `category`, `product_id` |
| `additive_panel_impression` | The additive panel entry point is in viewport for ≥ 2 seconds | `category`, `product_id` — fires once per page session |

**Derived metric (computed from raw events, not a raw event itself):**  
`panel_open_rate` = sessions with `additive_panel_open` / sessions with `additive_panel_impression`.  
This is the primary instrumentation gate metric (§4.3).

### 3.2 Minimum Sample Size

**500 unique page sessions** with a recorded `additive_panel_impression` event (i.e. the user reached the
additive panel section and it was visible to them for ≥ 2 seconds) before the instrumentation gate is evaluated.
Sessions where the user never reached the panel are excluded from the denominator — they are a scroll-depth
problem, not an engagement problem.

500 is chosen because it provides a stable rate estimate: a 20% open rate (the go threshold, §4.3) at N=500
gives a 95% confidence interval of ±3.5 percentage points — narrow enough to be actionable. At N=200 the
interval is ±5.5 pp, which is too wide to distinguish 15% (fail) from 25% (clear pass).

### 3.3 Time Window

**4 weeks of live instrumentation** after the W2 prototype is deployed to production (behind the feature flag,
on the hummus or maadanim category page). The window starts on the day the flag is turned on for live traffic
and ends 28 calendar days later. Evaluation happens on day 29, not before.

If 500 impressions are not reached within 4 weeks, extend the window by up to 2 additional weeks (6 weeks
maximum). If 500 impressions are not reached in 6 weeks, the gate evaluation proceeds on whatever N was
reached, with an explicit caveat that the result is directional only (not a clean pass/fail). The Product
Agent documents this caveat in the gate-evaluation memo.

### 3.4 Privacy Boundary (explicit)

**What IS collected:** aggregate event counts per category and per (anonymous) shelf position. Counts only.
No rate per user, no session sequence, no scroll depth per user, no time-on-site per user.

**What IS NOT collected:**
- No user ID, login state, or authenticated identity.
- No device fingerprint, browser fingerprint, or IP address.
- No geographic location (not even city-level).
- No session replay or heatmap recording.
- No individual event sequences (i.e. we do not track "user X did A then B then C").
- No cross-session linkage of any kind.
- No A/B cohort assignment or exposure tracking.

All events are batched and aggregated server-side before storage. The raw event stream is not persisted. The
only persisted artifact is the daily aggregate count per event type per category.

This boundary is non-negotiable and is documented here before any instrumentation code is written. If a
future analytics need requires crossing this boundary, it requires a new product decision, not a tooling
change.

---

## 4. Go / No-Go Thresholds (LOCKED)

These thresholds are set on 2026-06-04, before the W2 prototype is built. They cannot be adjusted after
instrumentation data arrives. The Product Agent's signature on this document (and CC recording it in the
registry) constitutes the lock.

### 4.1 Moderated Sessions — Go Criterion

**Go:** At least **5 out of 8** moderated sessions (≥ 62.5%) show **unprompted additive panel interaction**
(user opened or tapped the panel before the moderator's soft prompt) AND at least **5 out of 8 sessions**
(≥ 62.5%) pass the **Task 3 additive panel comprehension test** (per §2.3 rubric).

**Rationale for 5/8:** In a population of non-expert Israeli smartphone users, 5/8 unprompted interaction
means the panel is discoverable and sufficiently compelling that the majority of shoppers engage it on their
own. A lower threshold (e.g. 3/8) would mean the feature attracts only a minority of already-interested
users — a niche, not a mainstream engagement signal. 5/8 is not a vanity metric: it means the panel is pulling
attention in a context where the user has no prior reason to look for additives.

If only 5 sessions are run (minimum), the thresholds scale: **≥ 4 out of 5** (80%) for both unprompted
interaction AND comprehension. The smaller the N, the higher the per-session bar, to compensate.

### 4.2 15-Second Comprehension Test — Go Criterion

**Go:** **≥ 8 out of 12** testers (≥ 67%) pass the three-criterion comprehension test (§2.3).

This threshold is independent of the moderated session threshold. Both must pass.

### 4.3 Live Instrumentation — Go Criterion

**Go:** **≥ 20%** `panel_open_rate` (additive panel opens / panel impressions) across the minimum 500 sessions
within the evaluation window.

**Rationale for 20%:** On a product page where the main job is shelf comparison and the additive panel is a
secondary feature below the score section, 20% open rate means 1 in 5 users who see the panel choose to open
it. That is a strong secondary feature engagement signal. For comparison: typical secondary feature CTRs in
e-commerce contexts are 5–12%; a 20% threshold is set deliberately above that range because the additive
panel is a permanent, high-maintenance commitment (EFSA/JECFA wiring, quarterly re-eval, QA harness). We need
genuine engagement, not marginal. A 10–15% open rate would be interesting but not sufficient to justify W3
scope. 20%+ is meaningful.

### 4.4 Combined Gate Rule

**All three criteria must pass** for W3 to open:
1. Moderated sessions threshold (§4.1) — pass
2. 15-second comprehension test (§4.2) — pass
3. Live instrumentation rate (§4.3) — pass

If **any single criterion fails,** the gate does not fire. There is no partial-pass outcome. The reason for
requiring all three: the moderated sessions test discoverability and comprehension in a controlled context;
the comprehension test validates the visual design in isolation; the instrumentation validates real-world
interest at scale. Each tests a different failure mode. A feature can pass two and fail one in ways that matter:

- Pass sessions + pass comp + fail instrumentation: the panel is understandable but nobody opens it in the
  wild — D4 is not worth building at scale.
- Pass sessions + fail comp + pass instrumentation: people open it but do not understand it — the design
  must be fixed before W3, but this is a design problem, not a demand problem. Fix the design, re-run
  comprehension test, then re-evaluate.
- Fail sessions + pass comp + pass instrumentation: should not happen given test correlation, but if it does,
  treat as a measurement artifact and escalate to Product for a judgment call.

### 4.5 No-Go Outcome (pre-approved)

If the gate fails on any criterion: **D4 is parked. Glass Box ships as D1+D2+D3+D5+D6 without D4.**

This is an explicitly acceptable and pre-approved product outcome. The parked state means:
- No EFSA/JECFA/FDA bulk curation is initiated.
- No additive maintenance protocol is built.
- No QA harness for the additive library is scoped.
- The W2 prototype additive panel is removed from production (or hidden behind a stricter flag) after evaluation.
- The D4 dimension remains in the six-dimension contract as a future option; it is not permanently removed from
  the architecture.
- Glass Box's consumer value proposition (D5 transparency + D6 confidence + the de-moralized D3 reframe) is
  intact and ships on its own merits.

Do not frame the no-go as failure in any internal or external communication. The gate is doing its job correctly
if it prevents building an expensive unmaintainable feature that shoppers do not use. That is a good outcome.

---

## 5. Design Brief — Additive Panel Component (W2 Prototype)

**Scope:** This brief covers the W2 prototype only. W3 UI evolves separately after the gate passes; do not
design for W3 requirements here.

**Owners:** Design Agent (visual spec, tier encoding, mobile layout), Frontend Agent (component build,
Gen 1 compliance, no Gen 0 patterns).

**Reference:** `01_framework/frontend/architecture_generations_registry_v1.md` — Gen 1 patterns only.
`01_framework/glass_box/six_dimension_contract_v1.md` §D4 — the six-tier taxonomy and DEC-006 postures.
`01_framework/glass_box/w0_product_cosign_v1.md` §Q3 — "explain plainly, do not alarm."

---

### 5.1 Information Hierarchy

The panel renders one additive finding per row. Within each row, the hierarchy is strictly:

1. **Tier chip** (top-left) — the single most important signal; must be legible in < 1 second.
2. **Hebrew common name** — the human name of the additive (e.g. "קרגינן", "ניטריט נתרן", "פקטין").
   E-number in parentheses, secondary weight: "קרגינן (E407)". Never lead with the E-number.
3. **One-line Hebrew explanation** — plain language, max ~12 words. Describes what the tier means for this
   specific additive. Examples:
   - Likely neutral: "מרכיב טכנולוגי מוכר — לא צפויה השפעה על הבריאות."
   - Dose-dependent: "בכמויות המקובלות — לא בעייתי. ריכוז גבוה — קיים דיון מדעי."
   - Contested: "קיים דיון מדעי על השפעה על מערכת העיכול. רגולטורים מתירים אותו."
   - Functional: "ממלא תפקיד טכנולוגי — מרקם, שימור. לא נמצאה השפעה שלילית."
   - Confirmed negative: (if it appears) — prohibited in the prototype; any confirmed-negative additive
     is a scoring veto, not a panel display item; it will not appear in W2 pilot categories.
   - Disclosure gap: "השם המדויק לא פורט — לא ניתן להעריך."
4. **"עוד" expand link** — right-aligned, small text. Opens the full evidence summary (one paragraph,
   citing tier source in plain language: "לפי EFSA" / "על פי מחקרים ב-2022" — never raw citation format).
5. **Expanded state** — full evidence summary (2–4 sentences max), followed by a "סגור" / up-arrow collapse.

**Max panel height (collapsed):** the full panel entry point ("X תוספים — הצג פירוט") must fit within 44px
height (one tap target row). Individual additive rows within the open panel: 64–80px each. If a product has
many additives (>4), show the top 3 by tier severity (contested first, then dose-dependent, then others)
with a "הצג עוד X תוספים" link for the remainder.

### 5.2 Visual Affordance (Entry Point)

The collapsed entry point is a single-line row rendered **below the score section, above the nutrition table.**
It uses the Gen 1 row geometry (72px product row spec does not apply here — this is a section divider row,
not a product row).

Collapsed state content: "[chip indicating highest severity tier present] X תוספים זוהו — הצג פירוט"
where X is the count of detected additives. A right-pointing chevron (›) at the far right signals it is
expandable (consistent with the existing expansion pattern).

If the product has no detected additives, the row shows the empty state (§5.6) — still rendered, not hidden.
Hiding the panel entirely when there are no additives removes the signal that the product is clean, which is
part of the value.

The row is visually differentiated from the product rows above it by a subtle top border (1px, `border-subtle`
token) and a `bg-surface-secondary` background tint — same treatment as the nutrition table section divider.
No new design tokens introduced.

### 5.3 Mobile-First Constraints

The panel must be usable in a 15-second scanning interaction on a phone (375px width, iOS Safari primary target).

- The entry point must be reachable without scrolling on a standard product row load (i.e. the top of the panel
  is visible within 2 full swipes from page top on a 375px device — roughly 1600px from the top of the page).
  If the current page layout puts the panel further down, this is a layout problem to fix before the prototype
  launches.
- No horizontal scroll, no carousel, no swipeable tier cards.
- Each additive row's tap target is ≥ 44px height (iOS minimum tap target).
- The "עוד" expand link has a minimum touch area of 44x44px even if the visible text is smaller — pad it.
- The expanded evidence summary must fit on-screen without horizontal scroll on 375px. If it overflows, truncate
  at 120 words with a "קרא עוד" link.
- Text sizes: tier chip label at min 12px; additive name at min 14px; one-line explanation at min 13px.
  Do not go smaller to fit more content — cut content instead.

**Two-swipe rule:** the complete collapsed additive panel (entry point row) must be reachable within two swipes
from the page top. The detailed per-additive rows inside the expanded panel may require additional scrolling —
that is acceptable. The initial discovery affordance must not require deep scrolling.

### 5.4 Forbidden Patterns

The following patterns are explicitly forbidden in the W2 prototype:

- **No alarm iconography** for contested or dose-dependent tiers: no red skulls, warning triangles (⚠), exclamation
  marks (!) in chip or card design. Alarm framing is reserved for confirmed-negative, and confirmed-negative
  additives do not appear in the W2 pilot categories (they are scoring-level vetoes, not display-level items).
- **No raw E-numbers as the primary label.** Human common name always leads; E-number is a secondary parenthetical.
  "E407" as a primary label is a forbidden pattern.
- **No attribution of manufacturer intent.** One-line explanations and expanded summaries must not include
  "היצרן הוסיף," "הסתיר," "ניסה," or any language implying a reason behind the product's formulation. The
  panel describes what is present and what science says about it — not why it is there.
- **No Gen 0 patterns** from the architecture generations registry: no dimension bars, no color-coded score
  components, no NOVA labels, no score attribution ("מה מעלה / מוריד את הציון"), no pillar strength labels
  (חזק / בינוני / חלש), no `MatrixIntegrityBadge`, no card grid layout for products.
- **No six raw numbers.** The additive panel does not show D4 sub-scores. It shows tier chips + plain language
  findings. Numeric sub-scores stay on the professional surface only.
- **No "safe" / "unsafe" binary labels.** The tier system has six states; reducing it to a binary is both
  misleading and a DEC-006 violation. The chip label and one-line explanation must convey the actual tier, not
  a simplified verdict.

### 5.5 Tier Visual Encoding

Six tiers, six visual states. The encoding respects DEC-006: no alarm colors for contested or dose-dependent.
The color system borrows from the existing Gen 1 score chip palette (A=green, B=olive, C=gold, D=orange, E=red)
but uses a distinct muted variant so additive chips are not confused with grade chips.

| Tier | Hebrew label (chip) | Chip visual | Semantic intent |
|---|---|---|---|
| confirmed-negative | "שלילי מוכח" | Deep orange-red fill, white text — close to grade D/E hue but in a subdued, matte variant. Use `bg-score-d` at 80% opacity or equivalent. | The only tier that warrants a warning-adjacent visual — but it does not appear in W2 pilot categories (scoring veto), so this is specified for completeness only. |
| scientifically-contested | "קיים ויכוח מדעי" | Warm amber / mustard fill, dark text — distinct from both alarm red and neutral grey. Closest to grade C chip hue (gold). Use `bg-score-c` at 70% or a purpose-defined `bg-tier-contested` token. | Indicates unsettled science without alarm. Must not look like a warning sign. |
| dose-dependent | "תלוי במינון" | Soft amber-orange, dark text — warmer than contested but cooler than alarm. Use a token `bg-tier-dose-dependent` between `bg-score-c` and `bg-score-d` hue. | Conveys "context matters" without alarm. |
| functional | "תפקיד טכנולוגי" | Neutral grey fill, dark text — `bg-surface-tertiary` or equivalent. | Maximally calm; this is the majority case on any real shelf. |
| likely-neutral | "ניטרלי ככל הנראה" | Light grey-green, dark text — slightly warmer than functional to signal positive-neutral. Could use a very desaturated `bg-score-b` tint. | Calm positive signal without overclaiming. |
| disclosure-gap | "לא פורט" | Light grey fill with a subtle dashed border (1px, `border-dashed`, `border-subtle-strong`). No fill color signal at all. | The absence of information should look visually "empty" — it is a data gap, not a quality verdict. The dashed border communicates "incomplete" without judgment. |

**Chip size:** 24px height, 8px horizontal padding, 11px font, border-radius 4px (pill-adjacent but rectangular
— distinct from score grade chips which are circular). Do not reuse the circular score chip component for
additive tiers.

**Chip placement:** left-aligned within the additive row, first element in the visual hierarchy.

### 5.6 Empty State

When no additives are detected for a product, the panel entry point still renders (do not hide it). The empty
state content:

"לא זוהו תוספי מזון שכיחים — המוצר מבוסס על רכיבים מזוהים בלבד."

No chip in the entry point row for the empty state. The row uses a `bg-surface-secondary` tint consistent
with the non-empty collapsed state. No checkmark, no "clean" badge, no star — the Gen 1 pattern does not
award visual decoration for the absence of a finding. State the fact plainly.

The empty state row is collapsed by default and does not expand. It is a one-line statement, not a panel.

---

## Product sign-off

[x] Thresholds locked 2026-06-04 — Product Agent (autonomous, no tripwire) + CC verified

**Rationale for key threshold choices (for the sign-off reviewer):**

- **5/8 unprompted sessions (62.5%):** below this threshold, the panel attracts only a self-selected minority —
  not a mainstream engagement signal. A feature with 3/8 unprompted opens is a niche. The threshold is set
  before we know the result so there is no temptation to call 3/8 a success.
- **67% comprehension (8/12):** the tier system is meaningless if users misread it. The three-criterion rubric
  specifically tests for alarm misreading (criterion 2) — if users see "קיים ויכוח מדעי" and think "toxic,"
  the design has failed DEC-006 at the consumer level. 67% is the minimum supermajority: we need the concept
  to land for most users, not just the attentive ones.
- **20% panel-open rate (live):** set above typical secondary feature CTRs (5–12%) because the maintenance
  commitment (EFSA quarterly re-evals, QA harness, content ops) is significant. Marginal engagement does not
  justify that cost. 20% means 1-in-5 real shoppers who saw the panel chose to open it — that is genuine
  curiosity, not accidental taps.
- **All-three-must-pass:** each test covers a different failure mode. Two out of three passes still means one
  mode failed. The gate is only meaningful if it is not negotiable on individual criteria.
