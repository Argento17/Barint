# Hebrew Health Scan — Output Template v1

Emit this structure to the **run history** (cloud routine writes no files — see schedule spec). Keep it short. Empty lanes say so.

---

```markdown
# Hebrew Health Scan — <YYYY-MM-DD>

**Run:** #<k>  ·  **Articles read:** <n> (1–2)  ·  **Mode:** <calibration run k/3 | normal>

## Coverage
- <source id> — <URL> — <opened | inaccessible (reason)> — *why chosen:* <one line>
- <source id> — <URL> — <opened | inaccessible (reason)> — *why chosen:* <one line>

---

## LANE A — Voice (register calibration)
> Technique described, never phrasing copied. Emulate/avoid shape (file 9 §2).

**EMULATE**
- <move/technique> — <which article> — <why it fits Tom's register>

**AVOID**
- <scare / prescriptive / moralizing / translationese-tell> — <which article> — <cross-ref file 10 Tx, or "new tell candidate: …">

**Proposed append to `9_israeli_food_blog_research.md`:** <yes — block below | no — nothing new>
<!-- if yes, the exact append block, in file-9 style, for the Content Agent to apply through the normal flow -->

---

## LANE B — Evidence (Horizon-Scan routing)
> Pointers, not evidence. No data inherited.

| claim (paraphrased, no number copied) | article | bucket | action |
|---|---|---|---|
| <…> | <src> | already-live / label-derivable+new / KB-candidate / declined | <one line> |

**KB / EV candidates for Nutrition Agent:** <none | list — Nutrition Agent decides, this run does not write>

---

## Firewall self-attestation
- Lane A: 0 phrasings copied · Lane B: 0 numbers/ingredients inherited · 0 consumer copy authored · 0 scores moved · COI sources signal-only.

## Notes / limitations
- <paywalls hit, thin day, anything the reader needs to trust the coverage>
```

---

**Reminder:** if both lanes are empty, the digest is still emitted to run history (honest empty day),
and owner-facing surfacing stays silent unless a Lane A keeper or a Lane B KB/EV candidate appeared.
