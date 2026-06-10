# Project Comp — Daily Output Template v1

**This is the exact structure every daily report must follow.** The scheduled run copies this
skeleton and fills it. Keep section order and headings. If a section has no signal tonight, write
**"אין סיגנל חדש — no new signal"** — never pad. **Built:** 2026-06-10.

> Filename: `01_framework/operations/comp/daily_reports/<YYYY-MM-DD>.md`
> Every creator/competitor/media line carries **C=credibility / D=discourse** (high/med/low),
> kept distinct. Every external claim shows whether it is *circulating* vs *evidence-backed*.

---

```markdown
# Project Comp — Daily Signal Report — <YYYY-MM-DD>

**Run:** project-comp-daily · evening · **Window:** last ~24–36h (FIRST RUN = ~5-month baseline since ~2026-01-01)
**Principle:** influencers are signal, not evidence — C (credibility) and D (discourse) shown separately.

---

## Context
*(mandatory — first block of every report; lets a reader trust the coverage before reading findings)*
- **Run mode:** normal · OR `calibration (run k/3)` — in calibration, do not overreact to single-day virality; qa-agent reviews runs 1–3 before any downstream task opens.
- **Date of run:** <YYYY-MM-DD> <HH:MM Asia/Jerusalem>
- **Source coverage actually checked:** <N> web sources (Tier A <a> · B <b> · C <c>) — ids: <…>
- **Source coverage NOT checked:** <M> social sources (manual sweep) + <k> inaccessible — ids: <…>
- **Social monitoring mode:** manual sweep — IL last swept <YYYY-MM-DD>, global last swept <YYYY-MM-DD>. (Never automated/scraped.)
- **Known limitations:** <e.g. paywalled deck only on Haaretz; podcast = show-notes only; watch-term pass = web-indexed only>
- **Source registry changes proposed:** <none / candidate adds or promotions proposed → see Assignment Queue>

---

## 1. Executive Signal Summary
3–6 bullets. The single most important thing Bari should know tonight, in plain language.
Lead with substance over volume. If it was a quiet night, say so.

## 2. Consumer Concerns
What consumers / media / mainstream voices are worried or excited about (he + en).
- [Topic] — <one line> · sources: <ids> · register: <mainstream/niche>
- Note the *concern*, not a verdict. No Bari claim here.

## 3. Competitor & Creator Moves
What Yuka / OFF / Fooducate / EWG / ZOE and the creator tier did.
- <source id> <name> — <what happened> · **C:<h/m/l> D:<h/m/l>** · url
- Separate genuinely (a high-D / low-C creator post is a reach event, not a credibility event).

## 4. Misinformation Watch
Claims circulating that are unsupported / oversimplified / fear-based.
- <claim> — circulating via <ids> · **C:low D:<h/m/l>** · why it's shaky: <one line>
- This section is descriptive surveillance. Bari's counter-position (if any) is a §9 proposal, not a fact here.

## 5. Category Opportunities
Shelves/categories where discourse suggests Bari coverage would land (e.g. a category heating up).
- <category> — <signal> — why it's an opening — owning call: Product/Nutrition. (Proposal only.)

## 6. Content Opportunities
Editorial angles the discourse opens for Bari (consistent with editorial standards).
- <angle> — grounded in <signal/ids> — owning call: Content/Marketing. (Proposal only.)

## 7. Scoring / Methodology Watchlist
Questions the discourse raises about Bari's scoring — **as questions for Nutrition/Product, never as changes.**
- <observation> → open question for Nutrition/Product: <question>. **No score/rule change implied.**
- (Tripwire #1: published scores & methodology are frozen unless the owner/Nutrition act explicitly.)

## 8. Source Log
Every active registry source with tonight's status. No silent gaps (Hard Rule 4/5).

| id | source | tier | status |
|---|---|---|---|
| gl-001 | Yuka | A | checked / no_update |
| … | … | … | … |
| il-024 | Omer Miller (@omermiller) | social | not_checked (last swept YYYY-MM-DD) |
| <id> | <blocked source> | <tier> | inaccessible (paywalled) |

Watch-term web pass: <ran / which terms surfaced items from unregistered sources → see §9 candidate adds>.

## 9. Bari Assignment Queue  (MANDATORY — every actionable signal gets exactly one primary owner)
This is the operational closer. Each actionable signal from §§1–7 becomes one row. Project Comp
**assigns and gates; it ships nothing.** Rows also append to the rolling `comp_action_queue.md`.

**Allowed primary owners (one per row, only these):** `product-agent` · `research-agent` ·
`nutrition-agent` · `data-agent` · `content-agent` · `frontend-agent` · `design-agent` ·
`marketing-agent` · `qa-agent` · `red-team-agent`. If no action is justified → **owner: none, action: ignore/monitor.**

**Recommended action ∈** monitor · research · nutrition review · category candidate · content draft ·
scoring watch · competitor response · ignore.
**Priority ∈** P0 (act now) · P1 (this week) · P2 (backlog) · P3 (watch).
**Evidence status ∈** social signal only · media signal · competitor signal · institutional source · evidence-backed.

| Signal | Why Bari cares | Action | Owner | Reviewers (≤2) | Priority | Evidence status | Next artifact | Gate |
|---|---|---|---|---|---|---|---|---|
| <what was observed> | <concrete implication> | <action> | <one agent> | <0–2 agents> | <P0–P3> | <status> | <artifact if actioned> | <what must be true before it affects Bari content/scoring/product> |

**Assignment hard rules (QA voids the run on violation):**
1. **No row may recommend a scoring change directly from social/influencer content.**
2. **Any scoring/methodology item routes first to `research-agent` or `nutrition-agent`** (never straight to a score). Action = `scoring watch`; Gate names the required review.
3. **Any consumer-facing content idea must pass `content-agent` AND `nutrition-agent` before publication** — both appear as owner/reviewer, and the Gate says "not published until both clear."
4. **Any category opportunity routes to `product-agent` before any BSIP0 work starts.** Action = `category candidate`; Gate = "product-agent go before BSIP0."
5. **Any source-quality / misinformation concern is marked `signal`, not evidence** (Evidence status = `social signal only` / `media signal`), and never asserted as fact.
6. **If no action is justified:** owner `none`, action `ignore`/`monitor` — do not invent work.

*One primary owner per row (accountability). Reviewers optional, max two. Evidence status must match
the §§3–4 C/D classification — a high-discourse / low-credibility item can never carry evidence
status above `social signal only` without a research/nutrition upgrade.*

---
*Project Comp is an intelligence layer. No scores changed, no claims published, no private/paywalled/
social content scraped, no source coverage implied that wasn't actually checked.*
```

---

## Notes for the run agent

- **C/D discipline:** credibility = is the source/claim trustworthy on the merits; discourse = how
  much reach/attention it has. A 2M-follower post by an uncredentialed creator is **C:low D:high** —
  log it as a reach event under §3 and, if the claim is shaky, also under §4. Never collapse the two.
- **Hebrew + English:** §2 and §4 should reflect both markets; tag language where useful.
- **Proposals vs facts:** §§5–7 and §9 are proposals. §§2–4 and §8 are observations. Nothing in any
  section is a Bari claim or a score/copy change.
- **Thin nights are fine.** A short honest report is a successful run. Padding is a failure.
