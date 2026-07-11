# Adversarial QA / Red-Team Report — Seed Oils Blog Draft (TASK-492A)

**Reviewer:** Adversarial QA Agent (Bari). Independent of Content/Nutrition authorship — read the
draft, the Nutrition co-sign, and the Research verification report directly; did not accept a
builder summary.
**Date:** 2026-07-03
**Draft:** `C:\Bari\03_operations\reports\content\seed_oils_blog_draft_v1.md`
**Evidence:** `C:\Bari\01_framework\nutrition\seed_oils_blog_cosign_v1.md`,
`C:\Bari\03_operations\reports\research\seed_oils_evidence_verification_v1.md`
**Live data checked:** `C:\Bari\bari-web\src\data\comparisons\cookies_coffee_frontend_v2.json`
(117 products, read directly via Python, not via the cosign's summary)
**Engine code checked:** `C:\Bari\03_operations\bsip2\proto_v0\src\score_engine.py`,
`bsip2_evidence_registry_v1.md` (EV-095/096/097/104)

---

## Findings by Severity

### HIGH

**RT-1 — JHU/Marklund attribution stated with MSK-level confidence the evidence doesn't support.**
Line 28: *"Johns Hopkins Bloomberg School of Public Health הגיע לאותו מקום דרך נתיב עצמאי לגמרי.
ד"ר מתי מרקלונד... ניסח את זה חד: אין ראיה אמינה לכך ששמני זרעים או חומצה לינולאית מעודדים דלקת
בבני אדם."* This is written in the exact same flat, unhedged register as the MSK paragraph
immediately above it (line 26), which the verification report confirms was checked by **direct
fetch, 200 OK, primary source read** (`seed_oils_evidence_verification_v1.md` §3, MSK section).
The JHU/Marklund attribution is materially weaker: the primary JHU page **403'd on every attempt**;
the quote is "verified via convergent independent secondary sourcing" (three health-press outlets
citing the same event), and the verification report's own confidence rating is **"Moderate-high...
but it is not the same as reading the primary source directly"** (§3, JHU section, and explicitly
flagged again in §5 Gap 1... actually Gap discussion). The draft collapses that distinction — a
reader (or a journalist checking the JHU page) has no way to know from the copy that this quote
was never read at its source. Naming Marklund by name and rendering the quote as a direct,
unqualified statement ("ניסח את זה חד") overstates the verification tier. This is the single
weakest attackable sentence in the piece: a critic who tries to pull the primary JHU URL and hits
the same 403 will reasonably ask why Bari presented a secondhand quote as primary-sourced.
**Fix belongs to Content**, not this gate — routing only.

**RT-2 — The "halved" self-correction claim conflates two different, non-identical scoring
mechanisms.** Line 58 says Bari *"הקטין את ההתאמה שהוא נותן לנוכחות של שמן זרעים בערך בחצי"*
("reduced the adjustment it gives to seed-oil presence by roughly half"), directly following the
cookies demonstration (lines 50–54) built entirely on the trace-verified flat **`SEED_OIL_PRESENT`
penalty (`score_engine.py:3014`, hardcoded `check_penalty(..., 3, ...)`)** — confirmed live against
the actual JSON trace on all three cited products (rank 1, 116, 117 all show
`{'rule': 'SEED_OIL_PRESENT', 'amount': 3}`). That `-3` constant has **never been changed by EV-096
or any other evidence review** — it is a separate code path from the mechanism EV-096 actually
touched (`_seed_pen_base` in `_score_fat_quality_sprint1`, `score_engine.py:1713`, gated behind
`BARI_FAT_TECH_V1`, serving the `whole_food_fat`/dairy-fat/margarine/milk-alternative pathway per
the cosign's own §2 admission: *"a different signal path serving whole_food_fat/dairy_protein
categories, not the biscuit pathway below"*). The draft's paragraph structure — cookies demo, then
immediately "Bari already corrected itself" — reads as one continuous narrative about the same
signal, but it is two different penalties in two different pathways, only one of which moved. A
technically literate reader (or a competitor engineer) who reads the trace JSON, as this gate just
did, can show the −3 constant on the exact cookie examples cited was never reduced. This is
defensible only if a reader never checks; it is not defensible against the standard this draft
itself invites ("kachu, mano data חיים") by showing raw trace-adjacent claims. **Routes to
Nutrition Agent** to confirm whether the "halved" claim should be scoped explicitly to the
fat-quality/dairy pathway rather than stated as a general engine-wide seed-oil correction, since as
written it implies the very penalty just demonstrated in the cookies example was the one reduced.

### MEDIUM

**RT-3 — "נתיב עצמאי לגמרí" (a fully independent path) is stated more strongly than the underlying
verification tiers justify when read together.** Line 30 says the two institutions arrived at the
same place independently, "בלי אינטרס מסחרי משותף" (with no shared commercial interest) — that part
is fine and matches the verification report's landscape-consensus framing (§4). But by placing this
sentence directly after an unhedged JHU quote (RT-1) and before disclosing that JHU itself was only
secondary-sourced, the paragraph implies both institutions carry equal evidentiary weight as
"independent, directly-checked" sources. Once RT-1 is corrected with an appropriate hedge, this
line's "two fully independent, equally-weighted institutions" framing should be re-examined for
consistency — currently it slightly overstates parity between a directly-fetched primary source
(MSK) and a secondary-corroborated one (JHU).

**RT-4 — Example B's penalty count characterization inherited from the cosign is close but not
exact; draft doesn't repeat the specific number so it isn't itself wrong, but flag for awareness.**
The cosign (§2, Example B) says "Five to six independent structural penalties/caps stack" for
rank 116–117. Direct trace read shows rank 116 has 3 caps + 4 penalties (7 items total, including
the −3 seed-oil one) and rank 117 has 3 caps + 3 penalties (6 items, including seed-oil). The
draft itself (line 54) does not cite a specific count — it says generically "כמה תוספים נערמים בו"
(several additives stack) — so **this is not a draft error**, only a note that the upstream cosign's
count was loosely stated. No action needed on the draft; noting for the record since Hard Rule 14
(evidence-weight check) requires checking the upstream citation too, not just the draft's own text.

**RT-5 — "האשם הסביר" (the likely culprit) rendering of the JHU confound quote is a paraphrase, not
a quote, presented adjacent to a directly-quoted sentence — verify this is clearly Bari's editorial
gloss and not attributed to JHU verbatim.** Line 38: *"Johns Hopkins מנסח את זה בדיוק כך: שמני זרעים
מואשמים בנזקים של המזון האולטרה-מעובד שבו הם מופיעים. האשם הסביר הוא התבנית המעובדת עצמה."* The
first sentence ("שמני זרעים מואשמים...") is presented as a direct JHU formulation ("מנסח את זה
בדיוק כך" = "phrases it exactly like this") and reasonably tracks the verification report's
paraphrase of JHU's confound position (§3: *"seed oils 'are often blamed for the negative effects
of ultraprocessed foods'"*). But the second sentence ("האשם הסביר הוא התבנית המעובדת עצמה" — "the
likely culprit is the processed pattern itself") is a stronger, more definitive causal claim than
anything in the verification report, which frames this as confounding/correlation, not an
established causal culprit-identification. Presented back-to-back with "מנסח את זה בדיוק כך" (phrases
it exactly like this), a careful reader could believe both sentences are JHU's formulation, when the
second is Bari's own inferential leap dressed in the same "this is what JHU said" framing. This is a
MEDIUM attribution-boundary issue, not a fabrication (the underlying substance — UPF is the likely
confound — is supported directionally by the verification report's §4.2), but the sentence boundary
between "what JHU said" and "what Bari concludes from what JHU said" is blurred.

---

## Items Checked and Cleared (no finding)

1. **AICR correctly excluded.** Draft cites only MSK, Johns Hopkins, and Nagra et al. throughout
   (body + frontmatter `sources_inline` + closing citation block). AICR, which the verification
   report explicitly says is "snippet-only... do not treat as fully confirmed," never appears.
   Correctly compliant with cosign §1a and verification report §3/§5 Gap 2.
2. **COI disclosure (Track C item 2).** Line 32 discloses the Nagra et al. COI in-line (senior
   author tied to a soy-oil-promoting institute), correctly notes it is a scoping/narrative review
   not a meta-analysis, and explicitly demotes it to corroboration ("לא הראיה שעליה נשענת הטענה
   שלנו, אלא קול נוסף"). Matches cosign §1a exactly. No finding.
3. **Demonstration numbers (Track C item 3) — VERIFIED against live JSON, not the cosign's report.**
   Independently re-derived from `cookies_coffee_frontend_v2.json` (117 products total, confirmed
   by direct count):
   - Rank 1: score **59.8**, grade **C**, ingredients contain שמן קנולה (canola oil), confirmed
     `SEED_OIL_PRESENT` fires (`amount: 3`), binding cap `NOVA_PROXY_3_PROCESSED` at 94.8 — matches
     draft line 50 exactly.
   - Rank 116: score **10.7**, grade **E**, contains קנולה/חמניות/סויה.
   - Rank 117: score **10.0** (draft rounds to "10"), grade **E**, contains קנולה/חמניות/סויה.
   - Spread: 59.8 − 10.0 = **49.8**, matches draft's "פער של כמעט 50 נקודות" (a gap of almost 50
     points) precisely.
   All four numeric claims in the draft's demonstration section (lines 50–54) are correct as
   independently re-verified against the live, committed frontend JSON. No discrepancy. This is the
   load-bearing proof of the piece and it holds.
4. **"Halved" date claim.** EV-096 registry entry confirms `seed_pen` 10→5, recorded 2026-06-15,
   status "ACTIVATED 2026-06-15 (BARI_FAT_TECH_V1 default ON, TASK-284E)." Draft says "ביוני 2026"
   — correct month, and 10→5 is exactly half. (See RT-2 above for the separate concern about *which*
   penalty this claim is scoped to — the date/magnitude arithmetic itself is correct.)
5. **No banned overclaim language found.** Draft does not use "מוכיח" (proves) about safety; line 64
   explicitly states the narrower, correct claim ("ברי לא מוכיח ששמני זרעים 'בריאים' או 'בטוחים'
   באופן גורף"). Matches cosign §3.3 required boundary language almost verbatim.
6. **No conflation of frying/oxidation with the inflammation claim.** Lines 40–44 keep the two
   questions explicitly separate ("זו שאלה אחרת לגמרי... שמרנו את שתי השאלות נפרדות בכוונה, כי
   לערבב ביניהן זו טעות עובדתית"). Matches cosign §3.1 requirement.
7. **MSK 16%/17% mortality/cancer-mortality statistics — absent.** Confirmed via grep: no numeric
   mortality stats, no "Nutrients" or "JAMA" study citations appear anywhere in the draft. Correctly
   compliant with cosign §3.4 (unverified-numbers ban) and verification report §5 Gap 4.
8. **No framework-vocabulary leakage.** Grepped draft body for NOVA/BSIP/cap/floor/structural_class/
   pillar/routing/matrix_integrity — zero matches in body copy (the single "pillar:" match is
   frontmatter taxonomy metadata, not consumer-facing text). Compliant with cosign §3.5 and standing
   leakage hard rule.
9. **No fabrication detected.** DOI, PMID, author names, MSK byline/date, and product names all
   trace to the verification report or the live JSON; nothing invented was found in the draft.

---

## Summary Assessment

**Plausible-but-unverifiable:** the JHU/Marklund attribution (RT-1) — publicly defensible only if a
reader never attempts to verify the primary source, which is an unsafe assumption for a piece that
explicitly stakes its credibility on "we checked because a journalist would."

**Justified:** the MSK attribution, the demonstration numbers, the COI disclosure, the frying/
inflammation separation, the overclaim boundary language.

**Overriding structural problem:** none — no CRITICAL. The two HIGH findings are attribution-
precision and narrative-conflation problems, not fabrications, not safety-overclaims, and not
propagation errors. Both are fixable by Content without touching the underlying (accurate) evidence
or the (verified) demonstration numbers.

---

## Findings Table

| ID | Severity | Line(s) | Issue | Routes to |
|---|---|---|---|---|
| RT-1 | HIGH | 28 | JHU/Marklund quote stated with MSK-equivalent confidence despite secondary-only (403'd primary) verification | content-agent |
| RT-2 | HIGH | 50–58 | "Halved" self-correction narrative conflates the flat `-3 SEED_OIL_PRESENT` penalty (shown in the cookies demo, never changed) with the separate EV-096 `10→5` reduction (different pathway, different products) | nutrition-agent |
| RT-3 | MEDIUM | 30 | "Fully independent path" framing implies false parity between directly-verified (MSK) and secondary-verified (JHU) sources | content-agent |
| RT-4 | MEDIUM | (cosign §2, not draft) | Upstream cosign's "five to six penalties" count is loosely stated vs. actual trace (6–7 items); draft itself doesn't repeat the number, no draft-level action | nutrition-agent (for the record only) |
| RT-5 | MEDIUM | 38 | Second sentence of the JHU confound paragraph reads as a JHU quote but is Bari's own causal inference, boundary blurred by "מנסח את זה בדיוק כך" | content-agent |

---

## Verdict

**GO_WITH_FINDINGS**

No CRITICAL findings. The load-bearing proof (the cookies demonstration numbers) is independently
verified against live committed data and holds exactly. No fabrication, no banned overclaim, no
leakage, AICR correctly excluded, COI correctly disclosed and demoted. Two HIGH findings on
attribution precision (RT-1) and mechanism-conflation (RT-2) should be resolved before this reaches
the owner — both are narrow, contained edits (add a hedge phrase to the JHU attribution; either
scope the "halved" claim explicitly to the fat-quality/dairy pathway or drop the direct juxtaposition
with the cookies demo) rather than structural rewrites. Per the standing content sign-off hard rule,
this draft still requires Content Agent's own sign-off in addition to this gate; this report does
not substitute for that or for owner review.

```json
{"verdict":"GO_WITH_FINDINGS","critical":0,"high":2,"medium":3}
```
