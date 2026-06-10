---
id: TASK-155
title: "Interim UI disclosure on the 2 dual-shelf יופלה GO SKUs (yogurts vs maadanim baseline difference) — TASK-154 mitigation"
owner: frontend-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-06-02
completed_at: 2026-06-02
closed_at: 2026-06-02
closed_by: cc-agent
close_reason: "Closed by PO direction (2026-06-02) — NOT executed. Superseded by an upcoming large content overhaul that will handle consumer-facing copy holistically; shipping a standalone 2-SKU interim disclosure separately is not worth it. The underlying issue (TASK-154: same יופלה GO SKU shows different grades on the yogurts vs maadanim pages, by governed design) remains accepted-as-governed; the disclosure requirement is folded into the content overhaul scope. No code shipped; nothing to roll back."
depends_on: [TASK-154]
blocks: []
parent: TASK-154
category_id: null
roadmap_impact: false
cc_comments:
  - date: 2026-06-02
    flag: fyi
    text: "Interim mitigation from the PO-confirmed TASK-154 ruling (accept-as-governed). Low-urgency, not an incident: 2 same-brand SKUs, flagship agrees B/B, only יופלה GO תות crosses a letter (D yog / C maad). Disclosure copy is consumer-facing Hebrew — needs PO + Content sign-off on the exact wording before it goes live on 2 pages."
  - date: 2026-06-02
    flag: verify
    text: "The disclosure must NOT imply one grade is 'wrong' — both are correct under their category's baseline. Frame as a transparent baseline note, not an error. Do not touch any score."
summary: >
  Per the PO-confirmed TASK-154 ruling (affirm Option 1 = accept the cross-page grade difference as governed),
  add a short cross-shelf disclosure on the 2 genuinely dual-listed יופלה GO SKUs — יופלה GO מועשר בחלבון
  (70/B yogurts vs 78/B maadanim) and יופלה GO תות (49/D vs 56/C). The same physical product appears on both
  /hashvaot/yogurts and /hashvaot/maadanim with different grades because the two categories run on different
  engine baselines (maadanim = TASK-144 dairy fixes ON; yogurt = earlier frozen baseline, fixes OFF, per
  TASK-146). Add a transparent note on those 2 rows (or their expansion) explaining the baseline difference —
  not an error, a disclosed baseline. Copy + 2 SKU rows on 2 pages; no component/architecture change; no score
  touched. PO + Content approve the Hebrew copy on return.
---

# TASK-155 — Interim UI disclosure on the 2 dual-shelf יופלה GO SKUs

Interim mitigation from TASK-154. Display/copy only — NO scores, NO scoring logic.

## Scope
- Identify the 2 SKUs in `yogurts_frontend_v2.json` (יופלה GO מועשר בחלבון = yog-008; יופלה GO תות = yog-010)
  and their maadanim twins (`bsip1_maadanim_7290110321031`, `bsip1_maadanim_7290110321680`).
- Add a short Hebrew disclosure (row badge / expansion note) on those rows explaining: same product also on the
  other shelf, scored under a different category baseline (maadanim = current dairy-fix baseline; yogurt = earlier
  frozen baseline pending any future re-run). Frame as transparency, not error.
- Reuse existing components; no new design language; additive only.

## Guards + DoD
- No score/grade/data change; no other rows affected; Hebrew RTL correct; `tsc`/build green.
- Copy is a DRAFT pending PO + Content approval (flag on return). DoD: disclosure renders on the 2 SKUs on both
  pages; build green; copy flagged for PO/Content sign-off. Then propose RETURNED.
