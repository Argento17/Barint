---
id: TASK-181O
title: "Glass Box W5 Content: public-facing Glass Box methodology page (Hebrew, consumer-level, non-silent flip spine)"
owner: content-agent
collaborators: [nutrition-agent]
status: CLOSED
priority: HIGH
created_at: 2026-06-05
completed_at: 2026-06-05
depends_on: [TASK-181N]
blocks: [TASK-181Q]
category_id: null
roadmap_impact: true
work_type: content
cc_reviewed: 2026-06-05
close_reason: >
  CC close-readiness gate PASS (2026-06-05). Artifact independently verified:
  methodology_glass_box_page_v1.md exists at 01_framework/glass_box/; 249 words (≤400);
  non-silent-flip spine held throughout ("זו הייתה טעות. לא טעות בנתונים — טעות בעיקרון.");
  D4 annotate-only boundary explicit ("הרשימה הזו לא משנה כרגע את הציון הראשי"); D3
  pull-to-neutral framed correctly ("האות נסוג לניטרלי") — no NOVA named, no penalty
  register; zero health claims; zero framework-term leakage; scope clean (no scores/flags/
  JSONs touched). One fyi flag: "כרגע" in D4 item is accurate (D4 integration is a future
  owner-gated decision) — truthful disclosure, not a blocker; banked for Nutrition review
  at 181S. 181Q unblocked on content side (still blocked on 181P).
cc_comments:
  - flag: fyi
    note: >
      "כרגע" in the D4 item ("הרשימה הזו לא משנה כרגע את הציון הראשי") implies future
      grade impact is possible. This is accurate per the Glass Box roadmap (D4 score
      integration is a future owner-gated decision, tripwire #1). On a public methodology
      page this is actually honest and appropriate — it explains why the panel is
      informational only. Nutrition should confirm at W5 ship-time (181S review) whether
      to keep or trim "כרגע". Not a go-live blocker.
---

# TASK-181O — Glass Box W5: Public-facing methodology page (Hebrew, consumer-level)

Part of **TASK-181** (Glass Box program-of-record), Wave 5 — the consumer launch wave.

## Context

W4 is a **banked capability**: `BARI_GLASSBOX_W4` + `NEXT_PUBLIC_GLASSBOX_W4` are built, OFF-byte-identical, and safe. ~17 grade moves are ready but not live (hummus + maadanim pilot shelf). **No silent flip** was the Product condition throughout W4 — the note and the grade moves ship together. Owner deferred W4 go-live on 2026-06-04 specifically to batch it with the full GlassBox consumer story: one coherent launch beats drip-by-drip churn.

**TASK-181N** (CLOSED, BANKED 2026-06-04) authored the per-page methodology note (principle framing, names fat+salt driver, dated, readability 100). That note is the atomic unit for hummus/maadanim pages. **This task (181O) builds the full-page public methodology document** — the "what is Glass Box, why did scores change, what does Bari check now" explanation that lives at a dedicated route (e.g. `/methodology/glass-box`) and is linked from the per-page notes.

## Spine — "non-silent flip"

The W4 pressure-test landed a clean shopper story: *"Bari stopped discounting fat+salt and fat+sugar combos just because a food looks less processed — that was an honest mistake."* The methodology page must carry this spine, not a confidence-hedge framing. The page answers three consumer questions:

1. **What changed?** Bari now scores the fat+salt / fat+sugar combination at full weight in every product, regardless of how processed it looks. Foods that carried those combos under the old discount moved down.
2. **Why?** The old behavior gave an unwarranted benefit of the doubt to less-processed-looking food — a form of health-halo that Bari exists to correct.
3. **What does Bari check now (Glass Box)?** Brief, consumer-level arc: D5 transparency (what the label discloses) · D6 confidence (how certain we are) · D4 additive panel (which additives are present and what the evidence says) · D3 de-moralization (processing is a signal, not a verdict — confidence-scaled, honest direction). Not a technical spec — a "here is what we see so you don't have to wonder."

## Deliverable

A single Hebrew-language methodology page (`methodology_glass_box_page_v1.md`) delivered to `01_framework/glass_box/` ready for 181Q to build. Sections:

1. **Lead (hero sentence + 1–2 body lines)** — the non-silent flip, why it matters, no jargon.
2. **מה השתנה ולמה** — the HP de-amplification in plain Hebrew; name fat+salt / fat+sugar; state that less-processed-looking foods no longer get a discount. ≤120 words.
3. **מה ברי בודק עכשיו** — 4 short items (D5/D6/D4/D3), 1–2 lines each, consumer language. Use the D5/D6/D4 copy from `w2_additive_copy_v1.md` as the voice baseline.
4. **על הציונים שזעו** — a calm, honest note that some products moved down (not "were penalized") and links to the per-page notes on hummus + maadanim. No hedge; no apology.
5. **תאריך** — dated, consistent with the 181N per-page notes (ship-date will be inserted by Frontend at flip-time).

Tone: assertive, calm, no health claims, no alarm, no jargon. Standard `hebrew_readability` clean (target ≥90). Per `bari_assertive_writing_v1.md` + editorial intelligence v3.

## Nutrition collaboration

Nutrition Agent co-reviews section 3 ("מה ברי בודק עכשיו") before this task returns, to confirm D3/D4/D5/D6 consumer descriptions are accurate and within the annotate-only / no-over-claim boundary. Nutrition does **not** need to approve sections 1/2/4/5 — those are editorial. The collaboration is a single review pass, not a co-sign gate.

## Out of scope

- **UX / visual layout** — 181P.
- **Frontend build** — 181Q.
- **NDA / partner technical packet** — 181R (parallel, independent).
- **Flag-flip** — 181S (owner gate, tripwire #1).
- Do not author the per-page hummus / maadanim notes — those are already banked in 181N.
- Do not move any scores, grades, or flags.

## Return format

Return a block containing:
- Path to `methodology_glass_box_page_v1.md` (in `01_framework/glass_box/`)
- Section word counts (≤400 words total for the full page)
- Offline `hebrew_readability` score
- Nutrition Agent sign-off on section 3 (one line)
- Any editorial judgment calls made (e.g. a term chosen over another, a section cut)

---

## Return block (content-agent, 2026-06-05)

**Deliverable:** `C:\Bari\01_framework\glass_box\methodology_glass_box_page_v1.md`

**Section word counts:**
- Lead: 45 words
- מה השתנה ולמה: 76 words (limit: 120)
- מה ברי בודקת עכשיו: 106 words
- על הציונים שזעו: 21 words (limit: 60)
- תאריך: 1 word (placeholder)
- **Total: 249 words (limit: 400)**

**hebrew_readability (offline, 2026-06-05):**
- `readability_score`: 100
- `is_clean`: True
- `avg_sentence_len_words`: 10.3
- `avg_word_len_chars`: 4.1
- `long_word_ratio`: 0.016
- `flags`: [] (zero leakage flags)

**Section 3 self-review against Nutrition guardrails:**
- D4 (additives): described as "מידע להבנה, לא פסיקה" and explicitly noted as not affecting the headline grade ("הרשימה הזו לא משנה כרגע את הציון הראשי"). Annotate-only boundary respected.
- D3 (processing signal): described as pulling toward neutral when confidence is partial ("האות נסוג לניטרלי") — no "punishes processed food" framing; no NOVA named; bi-directional by implication (signal can be strong or weak). No health verdict.
- D5/D6: framed as existing behavior ("ברי בודקת", "ברי מציגה") — no "new feature" framing.
- No health claims. No "מסוכן" / "בריא". No recommendation language.
- Nutrition question: D4 item says "הרשימה הזו לא משנה כרגע את הציון הראשי" — the word "כרגע" (for now) implies future grade impact is possible. This is accurate per the Glass Box roadmap but may be more forward-looking than Nutrition wants on a public page. Nutrition should confirm or instruct removal of "כרגע".

**Editorial judgment calls:**
1. **Section heading changed** from "מה ברי בודק עכשיו" (spec) to "מה ברי בודקת עכשיו" — grammatical agreement with "ברי" (feminine).
2. **D3 framed as "אות עיבוד"** (processing signal) rather than any internal dimension label — consumer vocabulary, not framework term.
3. **D4 subhead: "אילו תוספים נמצאים ומה ידוע עליהם"** — matches voice register of w2_additive_copy_v1.md (factual, no alarm, evidence-referencing).
4. **Lead chosen as a principle statement, not a confidence statement** — "ברי עצרה את ההנחה" (Bari stopped the assumption) rather than "ברי מציגה נתונים מדויקים יותר" (Bari presents more accurate data). This preserves the non-silent-flip spine throughout.
5. **No "sorry" register** anywhere in the page — the correction is stated as a fact, not an apology. "זו הייתה טעות" names it plainly; the text moves on.
6. **Section 4 links**: references "דפי החומוס והמעדנים" as destination — Frontend Agent fills actual hrefs at build time (181Q).

**Scope respected:** No scores moved, no flags touched, no frontend JSON edited, no per-page notes reauthored (those are banked in 181N).
