# Bari Consumer Interaction Validation Framework — v1

**Status:** Active  
**Date:** 2026-05-28  
**Phase:** Consumer Interaction Validation (current)  
**Replaces:** Architecture Stabilization (complete)

**Primary success metric:**  
> Can a first-time mobile user understand the shelf within 15–20 seconds of scrolling?

Not: framework sophistication, ontology completeness, analytical depth, scoring complexity.

---

## What "Understand the Shelf" Means

Understanding is operational, not impressionistic. A user understands the shelf if they can do the following after a 15–20 second first scroll — without tapping anything, without reading methodology, without prior context:

1. **Point to the best-scoring product** — not the one they personally prefer, but the one the page scores highest
2. **Name one concrete reason a product scored the way it did** — derived from an insight line, not from a guess
3. **Identify one surprising product** — a product they expected to do well that doesn't, or vice versa

If a user cannot do all three, the page has not communicated the shelf. It may have displayed data, but it has not created understanding.

---

## What "First-Time Mobile User" Means

- Has not seen the Bari product before
- Is not a nutritionist, food scientist, or dietitian
- Uses their phone for grocery decisions at least occasionally
- Has 15–20 seconds of genuine attention — not reading every line

Test with people who match this profile. Do not test with:
- Developers who built the page
- People who have read the governance documents
- People with professional food knowledge

---

## The 15–20 Second Scroll Test

### Setup

1. Open the category page on a physical phone (or Chrome mobile emulation at 375×812)
2. Hand the phone to the test participant (or simulate their perspective)
3. Say: "You have about 15 seconds — scroll through this and tell me what you see."
4. Do not explain anything before the test. Do not say "Bari" or "scores" or "comparison."
5. After 15–20 seconds, stop. Ask the three comprehension questions.

### The three comprehension questions

Ask after scrolling stops. Accept the first answer — do not prompt or hint.

**Q1 — Best product:** "Which product here seems to do the best?"  
Pass: points to the highest-scored product, or to one in the top 3.  
Fail: points to a recognizable brand with a low score, or says "I can't tell."

**Q2 — Reason:** "Why did that product do well — or why did another one do poorly?"  
Pass: names a specific observation (ingredient, number, position claim) traceable to an insight line.  
Fail: says "it's healthier" without specifics, or "I don't know."

**Q3 — Surprise:** "Was anything here surprising to you?"  
Pass: identifies a product whose score contradicts its shelf positioning or brand expectation.  
Fail: says nothing was surprising, or names something that is not actually a contradiction.

### Scoring

| Result | Label | Action |
|---|---|---|
| All 3 pass | PASS | Page communicates shelf — proceed |
| Q1 pass, Q2 fail, Q3 anything | PARTIAL — insight lines weak | Rewrite insight lines for bottom-of-list products |
| Q1 fail | FAIL — score hierarchy not visible | Score chip visibility or hero problem |
| Q1 pass, Q2 pass, Q3 fail | PARTIAL — no surprise surfaced | T2 insight line density too low; hero product choice wrong |
| All 3 fail | FAIL — page does not communicate | Geometry or density problem; run full geometry checklist first |

---

## Comprehension Failure Diagnoses

Each failure type maps to a specific intervention. Diagnose before intervening.

### Failure type 1: Score hierarchy not visible (Q1 fail)

**Symptom:** User cannot identify the highest-scoring product after scrolling.  
**Likely causes (in order of frequency):**
1. Score chip is too small or too visually similar across rows — user did not register that the chip encodes rank
2. Hero product is not the highest-scoring product — the hero sets the wrong anchor
3. Pre-table content is too long — user spent their 15 seconds on prologue, not on rows

**Intervention:** Check hero product selection. Check score chip visibility at 375px. Run geometry checklist to verify pre-table height. Do not rewrite insight lines until score hierarchy is visible.

---

### Failure type 2: Insight lines not registering (Q2 fail)

**Symptom:** User can identify the best product but cannot name why.  
**Likely causes:**
1. Insight line font is too small or too low contrast
2. Insight line is a T3 position fact ("הגביע הכי מוכר בקטגוריה") when the user needed a T1 composition fact ("10 גרם חלבון, 3 רכיבים בלבד") — position facts don't anchor composition understanding
3. Insight line is abstract or uses a comparison the user cannot verify ("ציון גבוה מהממוצע")

**Intervention:** Run `validate_insight_lines.py` on current set. Check T1:T2:T3 ratio. Confirm the best-scoring product's insight line is T1 or T2, not T3. Check rendering: confirm 13px at 375px.

---

### Failure type 3: No surprise identified (Q3 fail)

**Symptom:** User can read scores and reasons, but found nothing surprising.  
**Likely causes:**
1. The page has too many T3 lines (position facts) relative to T2 (contradictions) — contradictions create surprise; position facts don't
2. The hero product is not a contradiction — it is simply the best product, which is not surprising
3. The comparison pair (if present) does not surface the most newsworthy gap in the category

**Intervention:** Review T2 line density — target 20–30% of lines. Review hero product selection — the best candidate for hero is a product that surprises, not just leads. Review comparison pair — it should name the most counterintuitive gap.

---

### Failure type 4: User found the page "confusing" or "overwhelming"

**Symptom:** User expresses general confusion or information overload, regardless of comprehension question results.  
**Likely causes:**
1. Too many products — if the category has >40 products, the first scroll does not resolve
2. Row height inconsistency — variable row heights create visual noise
3. Multiple emphasis signals competing (comparison pair highlight, filter chips, insight line colors all demanding attention simultaneously)

**Intervention:** Check row height consistency. Confirm comparison pair is the only highlighted element. Check if category product count warrants a default filter state (not on initial load, but consider whether the default sort order surfaces the most informative products first).

---

## Quick Validation Protocol (No Test Participant)

When a test participant is not available, use this self-test protocol. It is weaker than live testing but catches major failures.

1. Open page on phone. Set a 15-second timer.
2. Scroll naturally for 15 seconds. Stop.
3. Without scrolling back: write down the product you would point to as best.
4. Write down one reason it scored the way it did.
5. Write down one thing that surprised you.
6. Apply the pass/fail criteria.

Honest self-testing works for geometry and density failures (Q1, Q4). It is unreliable for surprise failures (Q3) because the builder knows the data.

---

## Category-Specific Comprehension Anchors

Each category has a dominant story — the thing a user should walk away knowing. If the test shows the user understood something different, the page is communicating the wrong story.

| Category | Dominant story | Comprehension anchor |
|---|---|---|
| מעדנים | מילקי is the most famous product and has the lowest score in its cluster | Q1 should land on a protein-forward product; Q3 should surface the מילקי paradox |
| לחם | "שאור" on the label does not guarantee fermentation in the ingredient list | Q3 should surface the sourdough label gap |
| חלב | Oat and soy alternatives score comparably to dairy with fewer additives | Q3 should surface a non-dairy product outperforming familiar dairy |

If Q3 does not surface the dominant story, the hero product or the comparison pair needs adjustment — not the insight lines.

---

## When to Run This Validation

| Trigger | When to run |
|---|---|
| Before first category launch | Mandatory — run at least one live test + self-test |
| After insight line set changes | Run self-test; run live test if > 20% of lines changed |
| After hero product changes | Run self-test |
| After geometry changes (pre-table height) | Run geometry checklist first, then self-test |
| After adding a filter dimension | Run to confirm filter does not displace first-scroll comprehension |
| Before each additional category launch | Mandatory live test |

---

## What This Framework Does Not Measure

- Whether users prefer Bari to other food information sources
- Whether users trust the scores
- Whether users would return to the page
- Whether users share the page
- Whether the scores are nutritionally correct

These are separate research questions. This framework measures only first-scroll comprehension — whether the page communicates what the shelf contains within the attention budget of a first visit.

---

*Update the per-category results in the Per-Category Status table of `mobile_geometry_checklist_v1.md` after each validation run.*
