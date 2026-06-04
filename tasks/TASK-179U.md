---
id: TASK-179U
title: "Glass Box W2 — Hebrew additive copy: Content sign-off on 20 consumer explanations"
owner: content-agent
status: IN_PROGRESS
priority: HIGH
created_at: 2026-06-04
depends_on: [TASK-179Q]
blocks: [TASK-179T, TASK-179V]
category_id: null
roadmap_impact: true
work_type: execution
---

# TASK-179U — Glass Box W2: Hebrew additive copy sign-off

Part of TASK-179 (Glass Box), Wave 2. Runs in parallel with TASK-179S (engine) and
feeds TASK-179T (frontend). Content owns this; TASK-179T cannot ship final Hebrew
strings until this task is complete.

**No code, no score movement.**

## Input
`01_framework/glass_box/additive_prototype_set_v1.md` — every entry already has a
`Draft Hebrew consumer explanation` line authored by Nutrition (Phase 3). Content's
job is to review and sign off each of the 20 lines, making editorial refinements
where needed, and produce a finalized `w2_additive_copy_v1.md`.

## Scope

### Phase 1 — Editorial review (Content-agent)
Read all 20 draft Hebrew lines from `additive_prototype_set_v1.md`.
Apply the Bari editorial standards (read these before starting):
- `01_framework/editorial/insight_line_spec_v1.md`
- `01_framework/editorial/row_description_standard_v1.md`
- `C:\Users\HP\.claude\projects\c--Bari\memory\bari_assertive_writing_v1.md` (memory)
- `C:\Users\HP\.claude\projects\c--Bari\memory\bari_editorial_intelligence_v1.md` (memory)

For each line, verify:
1. **Plain language:** No scientific jargon without immediate plain-language translation.
2. **No alarm framing:** "dangerous," "toxic," "harmful," "risky" are forbidden for
   ALL tiers — including contested and dose-dependent. Use tier chip to carry the
   signal; prose explains without alarming.
3. **No manufacturer intent attribution:** "hidden," "disguised," "deliberately added"
   are forbidden.
4. **Restrained but informative:** The line should tell a shopper *what it is and what
   it does* — not whether they should avoid it. The tier chip signals that.
5. **Concision:** ≤ 120 characters per explanation line (fits a single mobile row).
6. **Hebrew grammar:** Correct Modern Israeli Hebrew. RTL display in mind.

### Phase 2 — Revise if needed
If any draft line fails the criteria above, rewrite it. Keep the information content —
only change the framing or trim excess.

### Phase 3 — Produce `w2_additive_copy_v1.md`
Write `01_framework/glass_box/w2_additive_copy_v1.md` — the canonical source of truth
for Hebrew additive copy in the W2 prototype.

Format per entry:
```markdown
### {e_number} — {name_he} ({name_en})
**Tier:** {tier}
**Explanation (final):** {final Hebrew line}
**Change from draft:** [unchanged | {brief note on what changed and why}]
```

The file is what TASK-179T reads for component strings. It is also the record for future
copy maintenance.

### Phase 4 — Content sign-off
Add a sign-off block at the end of `w2_additive_copy_v1.md`:
```markdown
## Content sign-off
- All 20 lines reviewed against Bari editorial standards (insight_line_spec + row_description_standard).
- DEC-006 alarm-framing prohibition: verified across all 20 entries.
- No manufacturer intent attribution in any line: verified.
- Content-agent: APPROVED 2026-06-04.
```

## Guardrails
- Do NOT change tier assignments — those are Nutrition's (already in additive_prototype_set_v1.md).
- Do NOT add or remove additives from the 20-entry set.
- Character limit: ≤ 120 characters per explanation line.
- DEC-006 posture is binding: no alarm framing, no attribution of intent, for ANY tier.

## Deliverables
1. `01_framework/glass_box/w2_additive_copy_v1.md` — 20 finalized Hebrew explanation lines
   with sign-off block

## Return block
Content returns with `w2_additive_copy_v1.md` complete + sign-off block present.
States: how many lines were unchanged vs revised, and the reason for any revisions.
TASK-179T can merge the final strings and proceed to ship.
