---
name: tone
description: Set the tone & theme of a Bari consumer-facing page from owner direction — capture it into a firewalled Page Tone Brief, then drive Content + Frontend to build to it through the normal two-gate. Tone modulates feel; it never overrides truth, governance, or conformance. Use for shelf / 1v1 comparison pages, blogs, landing — new or already-live.
---

# /tone — Owner-directed page tone & theme

The owner gives free-form direction on how a consumer-facing page should **feel** (tone, theme, angle). This skill turns that into a durable **Page Tone Brief**, runs a firewall pass so the direction can't breach a hard rule, then drives the **Content Agent** (authoring) and **Frontend Agent** (within conformance) to build to it — through the **existing two-gate sign-off**, never around it.

**Backbone principle (non-negotiable).** Tone **modulates how it feels**; it **never overrides what's true or what's allowed.** Any owner phrasing that would breach a lock is kept in spirit but **translated** to stay legal, and the translation is surfaced for owner confirmation before authoring. A tone brief is a *constraint on authoring*, not a bypass of governance. The orchestrator never authors copy inline.

## Use this when
- "Set the tone for the <page>", "I want <page> to feel like X", `/tone <page>`, "re-tone <existing page>".
- Pages in scope: shelf comparison, 1v1 comparison, blog, category landing — anything consumer-facing. New build OR already-live (retro-fit / re-tone).

## LOCKED — tone can NEVER override these
- **Content:** DEC-006 alarm-framing ban · no fabricated facts or provenance · citations discipline (every claim traceable) · Bari Score Presentation (numeric/grade only; no color/strength labels) · comparison governance (≤2 pts = noise; Anti-Immunity Rule) · **the two-gate sign-off itself** (Content Agent + Adversarial-QA / Red-Team).
- **Frontend:** comparison pages are in the **conformance phase** — frozen golden template, frozen pixel values, design-token governance. Tone moves copy / emphasis / framing / order / within-token accent ONLY — never new layout, components, or tokens.
- **Scores:** tone NEVER moves a score, grade, cap, or dimension. Scoring is a separate governed path (tripwire 1) — even on a page whose copy is fully in scope.

## TONE MAY turn — the latitude, by page type
| Knob | shelf / 1v1 comparison (frozen) | blog / landing (looser) |
|---|---|---|
| Copy voice & register | ✅ | ✅ |
| Hero / prologue / category-note framing | ✅ | ✅ |
| Section emphasis & narrative order | ✅ (within the golden section set) | ✅ |
| Within-design-token accent (allowed tokens only) | ✅ | ✅ |
| New layout / components / tokens | ❌ frozen | ⚠️ only via design-token governance + Design Agent |

Composes with — does not replace — the editorial OS: **Tom-Bari voice** (`content_voice/tom_bari_voice/`, the global fingerprint; this brief is the page's modulation *within* it), Editorial Intelligence v3, Assertive Writing v1, Insight Line Spec v1, Score Presentation v1.

## Flow (orchestrator drives; agents own their stages)

### 1. Capture
Take the owner's free-form input + the target page (type + slug/topic). Prompt for any missing brief field — never invent the owner's intent.

### 2. Structure → the Page Tone Brief
Copy `content_voice/tone_briefs/_TEMPLATE.md` → `content_voice/tone_briefs/<slug>_tone_v<N>.md` and fill it. Preserve the owner's words verbatim in **Your input**.

### 3. Firewall pass (the load-bearing step)
Map each tone descriptor onto the LATITUDE table for that page type. For anything that touches a LOCK, keep the intent and **translate** it:
- "alarming / scary" → "direct, unflinching — *within* DEC-006 (no מסוכן/רעיל)".
- "make it pop / flashy" → "stronger hero copy + allowed within-token accent — NOT a redesign" (frozen pages).
- "play up how bad X is" → "name the real finding plainly + carry the number — no moralizing, no score move".
Record every translation in **Firewall notes** and **surface them to the owner for confirmation before any authoring starts.**

### 4. Save
Save the versioned brief (bump `v<N>` on every re-tone). This is the single reference the agents build against and the red-team checks against.

### 5. Drive the build (active — this skill does not just file a doc)
- **New page:** the brief is an input to `build-page` Stage 4 (copy) and the frontend stage.
- **Existing / live page:** dispatch a tone-revision pass — Content Agent re-authors the consumer strings to the brief; Frontend Agent applies the within-latitude changes only.
- **Lane:** authoring engine is lane-agnostic (Sonnet / Cursor / Grok); Frontend Agent owns the page. Orchestrator dispatches; never authors inline.

### 6. Two-gate + tone-conformance (HARD)
Every string stays a *draft* until **both** gates pass. Add a **tone-conformance check** to the Adversarial-QA / Red-Team gate: *does the shipped copy/page honor the declared tone AND stay inside every LOCK?* A page that reads on-tone but breaches a lock **FAILS**. The orchestrator records the second sign-off only after the gate passes — never self-stamp. Deploy stays a separate owner-gated step.

## The Page Tone Brief — required fields
See `content_voice/tone_briefs/_TEMPLATE.md`. Sections: header (slug · type · version · date · status) · Audience/mood · **Your input (verbatim)** · Tone (3–5 adjectives) · Theme/angle · Register (incl. Hebrew register, אתם plural) · Emphasize · Mute/avoid · Touchstones · **Latitude (auto by page type)** · **Locked** · **Firewall notes (translations for owner confirm)** · Hand-off (lanes + red-team tone check).

## Never
- Never let tone override a LOCK (content, frontend conformance, or score). Never author copy inline. Never ship on one gate. Never re-tone a live page without a new brief version + both gates. Never introduce a new layout / component / token under "theme" for a frozen comparison page. Never auto-deploy (owner-gated).

## Related
`build-page` (Stage 4 = where copy tone lands), `bari-frontend-ui`, `bari-qa-audit` / Adversarial-QA gate, the Tom-Bari voice system, Editorial Intelligence v3.
