# §2.8 Editorial Review — Heuristic-Vocab Resolution (Content Agent)

**Task:** TASK-130 follow-up (resolve §2.8 editorial review items)
**Owner:** content-agent
**Date:** 2026-06-01
**Reads:** `launch_readiness_validation_002.md` (data-agent), `category_module_contract_v1.md` (§2.8, R2, R4)
**Constraints honored:** follow-up only · **TASK-130 stays CLOSED** · **no score changes** · **no validator changes**. Only consumer-facing rendered copy was edited (Content domain).

---

## 0. Summary

Validation-002 left **21** §2.8 errors, all the heuristic health/recommendation-word class (`נקי`/`כדאי`/`בריא`); zero framework vocab. After this review:

| Disposition | Count | Effect |
|---|---|---|
| **Rephrased** (genuine claim) | 2 | edited → tokens gone, `--handoff` 21→19 |
| **Accepted exemption** (legitimate use) | 15 | keep copy; register so validator stops flagging |
| **False positive** (heuristic misfire) | 4 | keep copy; register / fix heuristic |

The 19 remaining errors are **not editorial defects** — they are the validator's R4 backstop firing on correct copy. They clear only when the R4 exemption mechanism (R2 registry) is wired by Data; that is a validator change and is **out of scope here** (recommendation in §4).

**Editorial principle applied:** §2.8 targets two things — health **verdicts** ("this product is healthy/clean-as-virtue") and purchase **recommendations** ("buy / prefer this"). It does **not** target (a) **compositional facts** (`נקי` = a short, additive-free ingredient list — the core Bari concept rewarded across every category), (b) **reader-information guidance** (`כדאי לבדוק את האריזה` = "worth checking the label" — Bari's transparency doctrine), or (c) **meta-references / negations** (text *about* a health label, quoted, or denied). Token presence ≠ prohibited sense.

---

## 1. Items rephrased (2) — genuine claims, now edited

| # | Product | Field | Before | After | Why |
|---|---|---|---|---|---|
| 1 | `snk-012` (snacks) | positiveSignals | "…שומן **בריא** ממקורות שונים" | "…שומן ממקור אגוזים שלמים, לא משמן מוסף" | "healthy fat" is a true health **verdict** — and it sits beside a limitingFactor flagging *high saturated fat from the cashew*, so the claim was also internally inconsistent. Rephrased to the structural fact (fat originates in whole nuts, not added refined oil). No score/nutrition change. |
| 2 | `yog-001` (yogurts) | bottomLine | "…המוצר שממנו **כדאי לצאת** כשמשווים" | "…נקודת הייחוס של הקטגוריה בהשוואה" | "worth starting from" is the one `כדאי` that reads as a soft purchase **recommendation** rather than information. Rephrased to its methodological role (the category's reference point). Meaning preserved; no score change. |

Re-run after edits: `--handoff` **21 → 19** errors (snacks 4→3, yogurts 3→2). JSON valid.

---

## 2. Items accepted as exemptions (15) — legitimate copy, keep as-is

### 2A. Compositional `נקי` / `נקייה` — "clean = short, additive-free ingredient list" (11)
This is core Bari vocabulary; the methodology *rewards* clean labels, so describing one is a finding, not a health verdict. It cannot be rephrased away without losing the central compositional concept, and it recurs in every category.

| Category | Product | Field | String (excerpt) |
|---|---|---|---|
| hummus | bsip1_7296073733324 | positiveSignals | "רשימת רכיבים נקייה — ללא תוספי מזון מזוהים" |
| hummus | bsip1_7296073733331 | positiveSignals | (same compositional phrase) |
| hummus | bsip1_3643820 | positiveSignals | (same compositional phrase) |
| maadanim | bsip1_maadanim_5014271300429 | bottomLine | "הרשימה הנקייה ביותר בקטגוריה — אבל 214 קק\"ל…" |
| maadanim | bsip1_maadanim_5014271360423 | limitingFactors | "…צפיפות קלורית גבוהה אפילו עם רשימה נקייה" |
| maadanim | bsip1_maadanim_5014271360423 | bottomLine | "תפוז טבעי ונקי — הציון הנמוך מגיע מצפיפות קלורית…" |
| maadanim | bsip1_maadanim_7290110325312 | comparisonContext | "…הסויה הנקייה ניצחת." |
| snacks | snk-001 | bottomLine | "70/B: …הבסיס הנקי ביותר…" |
| snacks | snk-011 | positiveSignals | "6 מרכיבים — אחד הבסיסים הנקיים בקטגוריה" |
| snacks | snk-011 | limitingFactors | "…מסמן עיבוד תעשייתי למרות הרשימה הנקייה אחרת" |
| yogurts | yog-003 | bottomLine | "82/A: יוגורט רזה בלי לשלם בממתיקים — בסיס נקי" |

### 2B. Informational `כדאי` — reader guidance, not a product recommendation (4)
The prohibited sense is "buy/prefer this." These advise the **reader to act on information** (know this / check the label) — consistent with Bari's transparency doctrine, not a purchase steer.

| Category | Product | Field | String (excerpt) | Sense |
|---|---|---|---|---|
| bread | shufersal_7290016245325 | insightLine | "…אבל כדאי לדעת: הסיבים כאן מגיעים מהטחינה…" | discourse marker ("worth knowing") introducing a composition fact |
| bread | shufersal_7290016245325 | bottomLine | (same string) | same |
| maadanim | bsip1_maadanim_7290107958035 | bottomLine | "…נתוני הנתרן נראים חריגים; כדאי לבדוק את האריזה." | directs reader to verify the label |
| maadanim | bsip1_maadanim_7290110561604 | comparisonContext | "…ציון שונה; כדאי לבדוק אם ההרכב שונה." | directs reader to verify composition |

---

## 3. Items that are false positives (4) — heuristic misfire, keep copy

The token appears but the prohibited sense is **absent** (negated, quoted, or the sentence is explicitly *about* a health label — often the opposite of a health claim).

| Category | Product | Field | String (excerpt) | Why it's a misfire |
|---|---|---|---|---|
| maadanim | bsip1_maadanim_5014271360423 | insightLine | "מעדן פרי בלי **תווית בריאות**" | states the product carries *no* health label — anti-claim |
| maadanim | bsip1_maadanim_7290110558703 | bottomLine | "…הפכו את ה**'בריא'** לעמוס יותר בתוספים…" | quoted-ironic, critical of the "healthy" framing |
| maadanim | bsip1_maadanim_7290107950206 | limitingFactors | "\"דיאט\" — …לא **'מוצר בריא'**" | explicitly negated ("not a 'healthy product'") |
| yogurts | yog-007 | bottomLine | "62/C: …ממוצע, לא **בסיס נקי**" | negated ("not a clean base") |

---

## 4. Final recommendation — validator R4 handling

R4 (heuristic vocab) + R2 (no machine-readable exemptions) are the same gap: the backstop has no way to know a reviewed string is legitimate, so it blocks correct copy. Recommended handling (for Data/Controller — **all validator-side, not done here**):

1. **Adopt a reviewed exemption registry (resolves R2).** A machine-readable whitelist the §2.8 scan consults; suppress a finding only when `(category, productId, field, token)` matches an **active, reasoned** entry. Per-instance and reviewed — never a blanket token whitelist, so new unreviewed uses still get caught. I have drafted the 15 exemptions + 4 false-positives as a candidate file: **`bari-web/scripts/vocab-exemptions.candidate.json`** (not wired; `.candidate` suffix is deliberate).
2. **Keep `נקי`/`בריא`/`כדאי` in the token list.** Do not weaken the backstop by deleting tokens — the value is catching *unreviewed* future copy. Exempt instances, not words.
3. **Cheap heuristic refinement (optional, future validator task).** Auto-suppress when the token is immediately preceded by a negation (`לא`/`בלי`/`אין`) or wrapped in quotes — this clears all 4 false positives and most negated/meta cases without per-instance entries, shrinking the registry to genuine compositional/informational exemptions.
4. **Disposition encoded:** of 21 → **2 rephrased** (real claims, fixed), **15 exempted** (compositional `נקי` + informational `כדאי`), **4 false positives** (negated/meta). After the registry is wired, expected `--handoff` §2.8 result = **0 blocking** with no further copy edits.

> Net: there is **no remaining editorial work** on the launch corpus. The two genuine claims are fixed; the other 19 are correct Bari copy that the heuristic over-flags. Launch is gated only on Data wiring the exemption registry (a `validate-corpus` change), per the launch-readiness report's close condition.

---

*§2.8 Editorial Review 001 — TASK-130 follow-up — content-agent — 2026-06-01. 2 copy rephrases (no score/nutrition/validator changes); 15 exemptions + 4 false-positives documented; candidate registry at `bari-web/scripts/vocab-exemptions.candidate.json`.*
