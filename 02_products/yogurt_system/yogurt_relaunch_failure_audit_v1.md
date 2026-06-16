# Yogurt Relaunch Failure Audit v1
**Date:** 2026-06-12 · **Auditor:** Orchestrator (self-audit, owner-ordered)
**Incident:** The P19→P14→P24 chain replaced a working yogurts page (owner: 8/10)
with a regression (owner: 2/10) — 17 products instead of the scored shelf, 6 dropped
images, weak relational copy. Caught at owner preview; never published.
**State:** Reverted in commit `4e2ec1a3` (page restored to checkpoint `ae88df9e`).
All S-tier scoring/audit work intact (`run_yogurt_006_shipcfg2`, 87 products).

---

## The one-sentence version
Every agent did exactly what its prompt said; **the prompts encoded the wrong product,
and every verification step checked spec-compliance instead of "is this better than
the page we have."**

---

## Root causes (evidence-backed)

### RC1 — Scope: 17 products was written into the spec and never challenged
- `P19_yogurts_frontend_rebuild.md:11` — "Page scope: the 18 products of the current
  v3 page minus 7290000408316."
- **The same prompt, one line above (line 10), states the run scored 87** ("D=23, E=1
  over 87"). The contradiction was visible in a single screenful.
- `TASK-256.md:40` carried the same "18 products Shufersal-only" ruling; the handover
  repeated it; the orchestrator (me) copied it forward and never asked the only
  question that mattered: *why does a relaunch show 18 of 87 scored products?*
- The owner's standing Leap-4 amendment (`TASK-255.md`, same day: "do not only
  re-verify known products — EXPAND approved shelves") pointed the **opposite**
  direction. Nobody connected the two.
- **Class:** decision-inheritance failure. A scoping ruling made in an earlier
  context (when 18 was the page's reality) was treated as law in a new context
  (a relaunch with 87 scored) where it no longer made sense.

### RC2 — Images: the builder dropped data present in its own sources
- v4 shipped 11/17 images. **5 of the 6 lost images existed in BOTH v3 and BSIP1**
  (all 88 BSIP1 yogurt records carry real `res.cloudinary.com/shufersal` URLs;
  the 6th existed in BSIP1).
- P19's builder simply failed to carry/look up `imageUrl`; the return block did not
  report image coverage; my verification checked grades/scores/dedup/strings —
  **never image coverage**, because the P19 RETURN BLOCK spec (my authorship) never
  asked for it.
- **Class:** silent field loss + verification blind spot. One of the lost images was
  the flagship S product (7290110565527, 90.6/S).

### RC3 — Copy: the gate proves truth, nothing proved value
- v4 copy is *longer* than v3 (avg 267 vs 159 consumer-text chars) — the weakness is
  quality, not quantity. The shipped lines are relational diff-notes ("אותו מותג כמו
  ה-S, תוספת וניל — הפרש של 20 ציונים") that don't stand alone for a reader.
- The relational framing was **instructed by the orchestrator's own P14 brief**
  (driver spine: "Story: same brand as the S plain… the vanilla version's additives
  are the whole gap"). Content executed the brief faithfully.
- The claim gate (rubric v2) checks entailment — copy can't *lie*. No gate checks
  whether copy is *good*. The editorial standards (insight-first, consumer attention
  test) exist in memory but were never run against the rendered page.
- **Class:** quality gate missing; truth gate mistaken for quality gate.

### RC4 — Verification anchored to the wrong baseline
- Every closing verification this session (P19, P14, P24) verified **agent-claims
  against the delegation spec**: grades match shipcfg2 ✓, S verbatim ✓, imports
  flipped ✓, build clean ✓. All true. All irrelevant to the regression.
- The correct baseline was **the live page**: products 18→17 (−87 potential), image
  coverage 94%→65%, copy standalone-quality down. A 5-minute side-by-side would have
  failed the swap instantly. It was never run because no step owned "compare the new
  page to the old page."
- **Class:** self-referential verification. The orchestrator wrote the spec, then
  verified compliance with its own spec — a closed loop that can't catch a wrong spec.

### RC5 — Confidence cascade
- Board after each step: "RETURNED + verified ✅". Eleven green checks in a row built
  false certainty; by P24 the swap felt like a formality. No agent (Design, Product,
  QA) ever reviewed the **assembled page as a product** — each saw only its slice.

---

## What was NOT the problem
- The engine and run are sound (87 scored, S=2 honest, audit valid).
- The cheap-lane agents executed their prompts correctly — this was not an execution
  failure, it was a **specification + verification-design failure**, i.e. mine.
- Nothing reached production. The preview gate (owner read before publish) worked —
  it is the only gate that did.

---

## Permanent fixes (adopt before any future page swap)

1. **Page Parity Gate (hard, blocking).** No import flip without a side-by-side
   table vs the current page: product count, image coverage %, avg copy weight,
   3 random card screenshots old/new. Any regression on any axis → STOP, owner call.
   This gate is owned by QA and the result is shown to the owner **before** the swap.
2. **Scope assertions in every rebuild spec.** Any prompt that sets a page scope
   must state: scored-corpus size, proposed display size, and one line justifying
   the delta. A delta >20% requires explicit owner sign-off in the spec.
3. **Return blocks must report field coverage** (images, names, every display field)
   as N/M vs source, not just the fields the spec emphasized.
4. **Editorial quality review ≠ claim gate.** Rendered-page read by Content/Design
   against the standalone-value test ("does each line inform a reader who sees only
   this card?") before any copy ships.
5. **Inherited rulings expire.** A scope/curation ruling carried across sessions must
   be re-validated against current data before reuse ("ruling X assumed Y; Y changed").

---

## Rebuild plan (separate, owner-gated)
Target: full clean shelf (~80 after dedup/OFF-exclusion) from `run_yogurt_006_shipcfg2`,
100% image carry-through from BSIP1, standalone copy at editorial bar, S-tier framing.
Built **offline**, presented to owner **side-by-side with the restored v3 page**, and
swapped only on explicit owner approval. No timeline pressure — correctness first.
