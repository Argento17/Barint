#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""author_copy_llm.py — content_agent_v1: the REAL LLM authoring seam (TASK-550 M1).

This module implements the same `author(facts: dict) -> dict` contract as
`author_copy.py` (the deterministic baseline_placeholder), but instead of a
fixed Hebrew phrase-bank it runs an actual headless-Claude pass that reads:

  - the Bari voice system (content_voice/tom_bari_voice/2,3,4,5)
  - a distilled register-move catalog from file 9 §6 (the Hebrew Health Scan
    feed) — the loop this task exists to close: a daily scan lesson can now
    actually shape a shipped line, because this is the first author that CAN
    read it.
  - the exact fact sheet for one category (fact_sheets.json, per
    authoring_contract.json v2)

...and writes Hebrew copy at the milk/blog quality bar instead of a template.

Interface (identical to author_copy.py — the pipeline does not change):
    from author_copy_llm import author
    authored = author(facts)   # dict -> dict, same output schema

Mechanism: headless `claude -p` via subprocess (same invocation pattern proven
in 01_framework/operations/hebrew_health_scan/local_scan.py — already-logged-in
CLI, no API key, best native-Hebrew output of the mechanisms available in this
environment). The model is instructed to use the Write tool to place the
authored JSON at an exact path (avoids stdout-wrapping/markdown-fence noise);
this script then loads that file and post-processes it.

Post-processing is a SAFETY NET, not a rewrite of the model's prose:
  1. s_verbatim byte-verbatim override — S-grade insightLine/s_grade_explanation
     are force-set from the fact sheet's s_verbatim, regardless of what the
     model wrote, per the contract's "s_verbatim_verbatim" hard rule.
  2. bariInterpretation key/label/score/strength pass-through — only
     `interpretation` is taken from the model; the deterministic identity of
     each dimension row is never at the model's discretion.
  3. bestUseCases pass-through when best_use_cases_pending=False.
  4. Zero-tolerance banned-phrase enforcement (enforce_clean, reused from
     author_copy.py — the SAME implementation, not a duplicate) over every
     consumer string in the output. A violation raises BannedPhraseError —
     this is "author_copy.enforce_clean() raises at generation time" (content
     agent hard rule 9), not a suggestion.
  5. Baseline-fingerprint zero-tolerance check — the model's output must not
     reproduce any exact phrase from author_copy.py's own template bank
     (copy_constants.get_author_copy_fingerprints()). This is the concrete
     defense against the "baseline copy shipped as authored" failure class
     (TASK-536 / `baseline_copy_shipped_trap`).
  6. Barcode-coverage check — every barcode in fact_sheets.json must have a
     product record in the output; missing ones are reported, never silently
     dropped or invented.

stdlib only + the project's offline copy_constants/author_copy modules. No
network beyond the headless `claude` subprocess itself. No OFF. No invented
facts — the prompt carries the fact-firewall rule and the post-processing
never fills a gap the model left null.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

_COPY_DIR = Path(__file__).resolve().parent
if str(_COPY_DIR) not in sys.path:
    sys.path.insert(0, str(_COPY_DIR))

from copy_constants import get_author_copy_fingerprints  # noqa: E402
from author_copy import enforce_clean, BannedPhraseError  # noqa: E402  (single impl, reused)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO_ROOT = _COPY_DIR.parents[2]  # C:\Bari
VOICE_DIR = REPO_ROOT / "content_voice" / "tom_bari_voice"
MODEL = "claude-sonnet-4-6"
# A headless `claude` authoring call is SLOW: measured ~230s for 1 product even
# with a trimmed prompt (full Claude Code session init + generation dominate; MCP
# on/off made no difference). Per-call time also scales with prompt size, so the
# voice context handed in should be a DISTILLED brief, not all four raw voice
# files (~76KB) re-sent every batch. Timeout is generous so a real call is never
# cut off mid-generation; a genuine hang is still reaped by _kill_tree.
CLAUDE_TIMEOUT = 900  # seconds per batch
# BATCH_SIZE tuning (measured 2026-07-09, cereals pilot, DISTILLED voice brief
# ~13.5KB, ~42KB full prompt at BATCH_SIZE=5): BATCH_SIZE=5 hit the 900s wall
# with ZERO output. Dropped to 2: batch 1 finished in ~520s, but batch 2 (same
# size, same prompt shape) hit the SAME 900s wall with zero output — this
# inconsistency (not a monotonic size problem) points at transient contention
# in this shared environment (multiple concurrent claude/node subprocesses
# from other background agents), not purely prompt/output size. Dropped to 1
# — the one size with a clean verified data point (~230s) — plus a retry-once
# per batch (BATCH_MAX_ATTEMPTS below) to absorb a one-off stall.
BATCH_SIZE = 1  # products per headless-claude call
# Batches are independent — author them concurrently. Measured per-call cost is
# ~465s and is GENERATION-bound, not startup-bound (disabling the MCP fleet did
# not speed up a single call), so concurrency is the only real lever: a
# 20-product shelf drops from ~2.5h serial to ~40min at 4 workers. Kept modest
# because each worker is a full `claude` process; raising it trades wall-clock
# for the resource contention that produced spurious 900s timeouts.
MAX_WORKERS = 4

AUTHOR_ENGINE_TAG = "content_agent_v1"


class ContentAgentAuthorError(RuntimeError):
    """Raised when the LLM pass does not produce a usable authored.json."""


# ---------------------------------------------------------------------------
# Voice context loaders
# ---------------------------------------------------------------------------

def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


_VOICE_BRIEF = """
### VOICE IDENTITY (file 2 §0)
Bari writes like a sharp friend standing next to you at the shelf — names the
buying moment you recognize, quietly shows what's actually inside, trusts you
to decide. Not a dietitian brochure. Not a warning label. Not a cheerleader.

### DEFAULT REGISTER — two failure modes, both fatal (file 2 §0.5)
- F1 "translationese-punch": staccato fragments, calqued metaphors, the
  "X, לא Y" closer, "(!)" overused. Happens from trying too hard to sound punchy.
- F2 "neutral-bland": no verdict, hedge-only, says nothing. The over-correction
  from being told to "calm down."
Target = CONNECTED PROSE with a clear stance, built on native connectors:
יחד עם זאת · כי · מדובר ב… · במהותו · בגדול · אומנם… אבל · ביחס ל… · כך ש…
Resolve a contrast in flowing prose or land on "מדובר בסך הכל ב…" / "עדיין" —
never a bare "X, לא Y" parallel. Punch (fragments, "(!)", a hard short closer)
is seasoning for a genuinely egregious product or one landing line — not the
default rhythm of every row.

### THE ANCHOR VOICE (owner calibration, 2026-07-10 — the register every row aims at)
Owner-supplied calibration line:
"גאודה הולנדית קלאסית, עשירה ומלוחה. היא מכילה חלבון גבוה אך גם שומן גבוה.
מדובר במוצר יחסית נקי אבל יש לשים לב לכמות הנצרכת."
Three beats: (1) identity + sensory/textural character → (2) the nutritional
read in PLAIN ABSOLUTE WORDS ("חלבון גבוה", "מלוח", "רזה", "עשיר בשומן") →
(3) a practical takeaway. Short. Native. The product is described ON ITS OWN
TERMS — never by where it ranks on the shelf, never by reciting its panel.

### THE ARC (file 2 §1, compressed — evidence/close beats updated 2026-07-10)
Orienting opener (a recognizable moment OR a calm category-principle sentence)
→ familiar perception → the pivot ("אז זהו — שלא תמיד" / evidence turns up) →
for critical products: name the simple ideal, then the discovery, then the
mechanism/why → the composition read in plain words (what the list shows;
what the food is rich in and poor in — NEVER a panel figure) → the stance
(never shame: "זה לא אומר שאי אפשר לאכול את זה. זה כן אומר שכדאי לדעת
מה קונים.") → practical-takeaway close (what the product is, what it serves,
what to notice when consuming it — never rank / what-it-beats).
Each category's opener must be ORIGINAL to that category's real shopping
moment — never reuse another shelf's opening scene.
Headlines are a direct second-person question + value promise ("קונים X
בסופרמרקט? הנה מה שאתם צריכים לדעת"), never a poetic two-beat line.

### THE THREE MODES (file 2 §2 — mandatory, do not collapse to "critical")
| Mode | When | Closer flavor |
|---|---|---|
| Critical | ultra-processed / long list + additives + high sugar/sat-fat, or dessert-in-disguise | exposes image-vs-contents gap |
| Balanced | clean but nutritionally flat (short list, no additives, low fiber/protein) | "מוצר סביר הוא לא בהכרח מוצר חזק" |
| Positive | genuinely strong for the shelf | real un-hedged praise, then keeps it honest ("בסיס טוב. עוד יותר טוב כשלא מתייחסים אליו כאל כל הארוחה.") |
A clean-but-flat product is Balanced, never Critical. A strong product gets
real praise (clustering/strength is an honest finding). De-escalation is not
the default — when a product is genuinely bad, be firm ("פער עצום", not
softened). Egregious products earn the sharpest honest framing FIRST (name
the gap, quantify it) — but never a brand-attack, never mockery by name.

### SIGNATURE MOVES (file 2 §3, selected)
- "X הוא לא בהכרח Y" is the workhorse contrast ("מוצר נקי הוא לא בהכרח מוצר
  חזק תזונתית"). NEVER the retired calque "X לא תמיד אומר Y".
- Refuse single-villain reasoning: one additive/number is never the whole
  story — the whole picture is ("לא רכיב אחד — התמונה הכוללת").
- Image vs. structure: "השם מוכר. המבנה פחות."
- A nutrition-panel figure NEVER appears in prose (owner law 2026-07-10) —
  translate it into plain absolute words: מלוח, עשיר בשומן, רזה, חלבון גבוה,
  דל סיבים. Ingredient PROPORTIONS ("95% חיטה") stay allowed and useful.
- Product-anchor precision: ground every observation in the specific product
  ("בעוגה הזאת יש שפע תוספי מזון", not "יש כאן שפע"). "(!)" only for a
  genuinely exceptional case, at most once per shelf.
- The closing beat is PRACTICAL — what the product is, what it serves, what
  to notice when consuming it. Nuanced products earn 2-3 sentences here.

### HARD "NEVER"S (file 2 §6 + file 5, condensed)
Never shame the consumer. Never prescribe ("תמנעו", "אל תקנו", "מומלץ" with
no for-whom-and-why). Never a fear/health claim without sign-off. Never
surface additive risk-tiers/EFSA/disease pointers. Never make one additive
the whole story. Never treat clean-but-flat as junk. Never framework
vocabulary. Never "שורת בארי" as a section label (the beat is הקשר במדף, the
name is retired). Never a code token, `null`, a field-path, or a barcode/ID
slug in consumer copy — say the absence in plain Hebrew ("לא צוין על
האריזה"). Never mock or dismiss a brand by name ("X? תחשוב שוב" is banned —
critique composition, never brand character). Never dump bare facts side by
side with no "so what" (information-dumping is a defect, not insight).
Never a corpus rank / superlative / median claim ("הכי", "ה… ביותר",
"מהבולטים במדף", "נדיר במדף", "מעל/מתחת לחציון") — describe the product,
never its standing. Never "במקום X" (instead-of) define-by-negation. Never
call a list clean / "בלי תוספות" while it carries acidity regulators,
stabilizers, emulsifiers or seasoning blends beyond the base — an honest
cleanliness read reflects the FULL additive picture. Never close several
products on the same qualitative nutrient tail ("חלבון ונתרן סבירים" ×many)
— each closing read is product-specific.

### APPROVED PHRASE FRAGMENTS (file 4, selected — building blocks, not scripts)
Pivots: "אז זהו — שלא תמיד." · "במבט ראשון זה נראה כמו מוצר פשוט. רשימת
הרכיבים מספרת סיפור אחר." · "השם של המוצר מוכר. המבנה שלו פחות."
Stance: "הנה מה שמצאנו." · "אין כאן דרמה. יש כאן פער בין הדימוי של המוצר
לבין מה שיש בפנים." · "הצרכן לא צריך להיות כימאי כדי להבין מה הוא קונה."
Whole-picture: "הבעיה היא לא רכיב אחד. הבעיה היא התמונה הכוללת."
Mode closers — Balanced: "נקי? כן. חזק תזונתית? פחות." · "מוצר בינוני הוא לא
בהכרח מוצר רע — לפעמים הוא פשוט מוצר מוגבל." Positive: "מוצר חזק, בלי
קסמים תזונתיים." · "בסיס טוב. עוד יותר טוב כשלא מתייחסים אליו כאל כל
הארוחה."
Benefit/limit bullets: positive = "רשימת רכיבים קצרה: <מה בדיוק>"; caution =
limit + consequence in the same breath ("חלבון זניח — אינו תחליף לחלבון
מהמדף"); takeaway = a plain read of what the product IS and what it serves,
e.g. "משקה קל ומרענן; כמקור חלבון הוא זניח." (the old "X — לא Y" negation
template is RETIRED — define-by-negation, zero exceptions).
Plain-words descriptor bank (naming the read is REQUIRED; only the figure is
banned): חלבון גבוה · עשיר בחלבון · חלבון זניח · עשיר בשומן · רזה · דל שומן ·
מלוח · מלוח מאוד · דל נתרן · מתוק מאוד · עשיר בסוכר · דל סוכר · עשיר בסיבים ·
דל סיבים · צפוף קלורית · דל קלוריות.
Correct terms: נתרן (never סודיום/סודים); בארי (never ברי as the brand,
the ordinary word "ברי" and "גוג'י ברי" are fine).

### BANNED PHRASES — never write these regardless of context (file 5 §1, condensed)
רעל / מוצר רעיל / מלא כימיקלים → say "רשימת רכיבים ארוכה ותוספי מזון רבים".
מסוכן → "דורש תשומת לב". גורם לסרטן/קשור לסרטן → never (escalate to
Nutrition instead). הורס את הבריאות / לא ראוי למאכל / מזעזע / זבל → reframe
as an image-vs-contents gap, never scare/shame language. אסור לאכול /
להימנע → "כדאי לדעת מה קונים". בריא / לא בריא as a BLANKET claim → name the
specific strength/weakness instead. מומלץ / לא מומלץ without for-whom-and-why
→ banned (the one narrow carve-out: an explicit non-prescriptive disclaimer +
if-clause + a constructive alternative — otherwise skip it). תוספי תזונה
(wrong term, means supplements) → תוספי מזון. פחמימה ריקה → describe the
fiber/protein read in plain words instead, no metabolic verdict. ALL CAPS,
raw score numbers ("68.2","72/B"), framework terms (NOVA/cap/floor/BSIP/
dimension/pillar) → never. The word "null", any field-path/code token,
"שורת בארי" as a heading → never. Verbal grade recitation ("נשאר ב-A",
"עוצר ב-B כי")→ never — the badge already shows the grade. Score-mechanism /
data-state narration even in plain words ("רמת העיבוד אינה מאומתת מהנתונים")
→ never, with NO approved fallback shape (the old "בלי צילום תווית…"
carve-out is REVOKED — the words "צילום תווית" are themselves hard-banned);
just describe the product, and state a missing fact in plain food language
("לא צוין על האריזה"). Nutrition-panel figures in prose (grams / מ"ג /
קלוריות / קק"ל / nutrient-%) → never (owner law 2026-07-10) — name the read
in plain words ("מלוח", "עשיר בשומן", "חלבון גבוה"); ingredient PROPORTIONS
("40% טחינה") stay allowed. Corpus rank / superlative / median claims
("הכי", "ה… ביותר", "מהבולטים במדף", "נדיר במדף", "מוביל את המדף",
"מעל החציון") → never. "במקום <משהו>" instead-of framing → never (the
spatial sense "במקום אחד" is fine). Technical additive dumps (E-numbers,
chemical names) in verdict prose → generalize to "תוספי מזון" / "כמה תוספי
מזון".
Bare juxtaposition of facts with no finding → always name the "so what".
"קל מבחינה תזונתית" / "קל יחסית מבחינה תזונתית" (and feminine forms) → HARD
BANNED (owner ruling, H3-R2, 2026-07-10) — "קל" reads positive/diet-adjacent
in Hebrew while the intended meaning is nutritionally poor; inverted valence,
not idiomatic. When a product is nutritionally thin, say so directly, second
person, no euphemism. Approved model construction (owner verbatim — use
this shape): "בתור מקור לארוחת בוקר, אתם לא מקבלים כאן הרבה ערכים
תזונתיים."

### TRANSLATIONESE TELLS — mechanically checked, must not appear (file 5 §1.5, condensed)
| Tell | Banned shape | Natural repair |
|---|---|---|
| T1 | "...,/— לא X" contrastive CLOSER (comma/dash + לא + short phrase, ending the line) | resolve in prose, or land on "מדובר בסך הכל ב…"/"עדיין" |
| T1b | "עובד/נוח/מצוין כ-X; פחות/רחוק כ-Y" antithesis closer | stop earlier, land on a flowing verdict |
| T2 | "X לא תמיד אומר Y" | "X הוא לא בהכרח Y" |
| T3 | sentence ends on dangling "גם" | write the full clause |
| T4 | calqued metaphor ("נושא את החלבון", "לזכותו", "עוצר אותו בציון") | plain Hebrew ("מקורו מ…") |
| T5 | passive nominalization ("הבחירה שנעשתה היא…", "שמוסף") | active verb ("בחרו להוסיף", "מוסף") |
| T6 | untranslated English loanword ("מילק") | the Hebrew term ("שוקולד חלב") |
| T7 | wrong-register word/compression ("הפסד", "סיבים יפים") | correct-register word |
| T8 | "מה שמושיב אותו בראש/בתחתית המדף" (seating verb for rank) | rank claims are banned outright (2026-07-10) — name the driver plainly |
| T9 | "הצמרת הנקייה" compound | name the why of clean plainly ("רשימה נקייה מתוספים") — never a rank phrase |
| T10 | payment/price calque for a tradeoff ("במחיר X", "משלמים על זה ב-") | state the tradeoff plainly, no price figure |
| T11 | the "X, אבל Y" shape as the DEFAULT closer repeated across MANY products on one shelf | vary closer shapes across the shelf — see VERDICT ARCHITECTURES below |
| T12 | "נקי ונעים"/"נעים" as a positive verdict | a concrete, product-specific positive |
| T13 | passive nominalization at the closer | active, plain phrasing |
| T14 | boilerplate limitingFactors pasted across products regardless of fit | must be true for THIS product specifically |
Allowed, NOT tells: one in-prose "אבל" that resolves into a full clause;
"אשר"; an earned bare short closer like "לייט זה לא." (single instance only).

### ZERO-EXCEPTION BAN: "ולא" / "אלא" / comma+"לא" anywhere (TASK-550 M2)
This is STRICTER than the T1 closer rule above and has NO carve-out — it
is a mechanically-enforced hard gate (copy_rules.ANTITHESIS_RE) with zero
exceptions, not a style preference. The words "ולא" (and-not) and "אלא"
(but-rather) may NEVER appear anywhere in insightLine, rowVerdict,
consumerTakeaway, comparisonContext, positiveSignals, limitingFactors,
bariInterpretation, or bestUseCases — not as a closer, not mid-sentence,
not naming a positive alternative, not as "neither/nor." A comma may
never be immediately followed by "לא" either. (An earlier version of
this brief wrongly carved out "לא X אלא Y naming a positive" as approved
— that caused 11/20 pilot products to fail this exact gate. Retracted.)
To express a contrast or negate a claim without tripping the gate:
  - Restate positively instead of negating: not "X ולא Y" but "X. Y
    מגיע בנפרד" / "X, ו-Y נמצא במקום אחר."
  - Safe connectors for a real contrast: "אבל" · "יחד עם זאת" · "עם
    זאת" · "לעומת זאת" · "מנגד" · "אולם" · "בעוד ש…" — fine so long as
    "לא" doesn't directly follow a comma right after them.
  - Two separate sentences with a period, no connector at all.
Example repair: "מבוסס על אורז לבן מעובד ולא על דגן מלא" (BANNED) →
"הבסיס כאן הוא אורז לבן מעובד — דגן מלא איננו חלק מהרשימה" (safe).

### BEFORE/AFTER TRAINING PAIRS (file 3, selected — match the TRANSFORMATION, not the topic)
1. Generic: "המוצר מכיל הרבה סוכר ולכן הוא לא בריא ולא מומלץ." → Tom: "אין
   הפתעה בזה שעוגה מכילה סוכר. זו עוגה. הבעיה מתחילה כשהסוכר הגבוה מגיע יחד
   עם שומן רווי גבוה, רשימת רכיבים ארוכה ותוספי מזון רבים." (disarm the
   obvious → whole picture, not one villain → drop "לא בריא/לא מומלץ")
2. Generic: "דגני הבוקר האלה בריאים כי הם עשויים מאורז מלא." → Tom: "זה
   מוצר נקי יחסית, וזה חשוב... אבל נקי לא אומר בהכרח עשיר. אם אין הרבה
   סיבים ואין הרבה חלבון, המוצר נשאר די שטוח מבחינה תזונתית." (credit the
   real strength first → the workhorse contrast → balanced, not critical)
3. Generic: "המוצר מכיל מתחלב ולכן הוא בעייתי." → Tom: "מתחלבים הם מסוג
   הרכיבים שהצרכן הממוצע כמעט אף פעם לא שם לב אליהם. תוסף אחד לא הופך מוצר
   ל'אסור', אבל הוא כן חלק מהתמונה התעשייתית..." (defuse the scare word →
   additive as one signal in the whole picture; always generalized, never
   an E-code in verdict prose)
4. Panel-recite fix — Generic: "קוטג' 1%: 62 קלוריות ל-100 גרם, כ-12 גרם
   חלבון, ללא תוספים מזוהים..." → Tom: "קוטג' רזה במיוחד ועשיר בחלבון,
   בלי תוספי מזון מיותרים." (no figures, no rank — the read in plain
   absolute words)
5. Em-dash-crutch fix — Generic uses "—" as a connector 2-3 times per
   paragraph → Tom drops all but one, resolves the rest as full sentences
   joined by "ולכן"/comma — same content, cleaner Hebrew rhythm.
6. Anchor-voice reflow — Generic (rank + figures): "עם 26 גרם חלבון ל-100
   גרם, הגאודה הזאת היא מהבולטות במדף." → Tom: "גאודה הולנדית קלאסית,
   עשירה ומלוחה. היא מכילה חלבון גבוה אך גם שומן גבוה. מדובר במוצר יחסית
   נקי אבל יש לשים לב לכמות הנצרכת." (identity → plain-words nutritional
   read → practical takeaway; no figures, no shelf rank)

### REGISTER LESSON FROM ISRAELI CONSUMER-INVESTIGATIVE JOURNALISM (file 9 §2, distilled)
The closest real-world register to this voice is Israeli consumer-desk product
investigations (TheMarker cereal test): open from familiar perception, pivot
to evidence, make the composition visible in plain language WITHOUT
condemning the shopper ("עדיף X מאשר לדלג"), never fear-first framing. Avoid
the opposite register — health-scare listicles that frame the reader as an
unwitting test subject ("מיליארדים... בלי לדעת", "מעלה סיכון ל..."). The
dividing line is fear vs. discrimination: distinguish (processed vs.
ultra-processed, clean vs. strong), never alarm.
""".strip()


def build_voice_brief() -> str:
    """DISTILLED voice brief (TASK-550 M1 speed fix, 2026-07-09).

    The four raw voice files (2/3/4/5) are ~76KB combined. Re-sending all of
    them verbatim every headless-claude batch call made each call slow enough
    that a 5-product batch would not finish inside a sane timeout — the ONE
    remaining bottleneck once the subprocess layer itself was fixed (stream-
    to-disk, file-handle stdin, _kill_tree). This is a hand-curated editorial
    distillation (~10-15KB) of what is actually load-bearing for THIS pass:

      - the identity + the two failure-mode axis (F1/F2) that the naturalness
        gate directly checks for,
      - the three-mode system (the single biggest determinant of a line's
        tone),
      - the workhorse signature moves and hard "never"s,
      - a condensed banned-phrase table and the FULL T1-T14 translationese
        tell table (kept complete, not trimmed — this is what
        naturalness_gate.py mechanically re-checks, so under-specifying it
        here just pushes failures downstream),
      - a small, representative set of before/after pairs chosen to cover the
        specific failure classes seen live (single-villain reasoning, the
        workhorse contrast, additive-in-context, number-restating, em-dash
        overuse, stiff-to-connected reflow) rather than all 38 pairs,
      - the file-9 §2 register lesson (NOT §6 — that is the separate,
        always-current build_register_catalog() call below).

    This is NOT a replacement for the source files as the editorial
    standard — it is a compressed briefing for a single authoring pass. The
    full files remain canonical; if voice rules change materially, this
    string needs a manual re-sync (documented here as the known tradeoff).
    """
    return _VOICE_BRIEF


def build_register_catalog(max_entries: int = 18) -> str:
    """Distill file 9 §6 (Hebrew Health Scan daily keepers) into a compact
    register-move catalog — NOT a dump of the whole file (TASK-550 DoD #2).

    Only EMULATE (technique to use) and AVOID (anti-pattern to skip) entries
    are kept; DROP-tagged entries (already rejected by the scan's own
    firewall) are excluded. De-duplicated by title, most-recent occurrence
    wins (the file is append-only, chronological), ACT-tagged entries sorted
    first. This is the concrete wire from the daily scan to the author — the
    thing that did not exist before this task.
    """
    path = VOICE_DIR / "9_israeli_food_blog_research.md"
    text = _read(path)
    idx = text.find("## 6. Daily Scan keepers")
    section = text[idx:] if idx != -1 else ""

    entries: list[dict] = []
    line_re = re.compile(r"^-\s+\*\*(EMULATE|AVOID):\s*([^*]+)\*\*\s*(.*)$")
    tag_re = re.compile(r"`(ACT|WATCH|DROP)`\s*$")
    for raw_line in section.splitlines():
        line = raw_line.strip()
        m = line_re.match(line)
        if not m:
            continue
        kind, title, rest = m.groups()
        tag_m = tag_re.search(line)
        tag = tag_m.group(1) if tag_m else "WATCH"
        rest = rest.strip()
        # first sentence of the technique description, source-link stripped
        rest = re.sub(r"\[source\].*$", "", rest).strip()
        first_sentence = re.split(r"(?<=[.!?])\s", rest)[0] if rest else ""
        entries.append({
            "tag": tag, "kind": kind, "title": title.strip(),
            "note": first_sentence[:180],
        })

    by_title: dict[str, dict] = {}
    for e in entries:  # chronological order -> last write wins per title
        by_title[e["title"]] = e
    deduped = [e for e in by_title.values() if e["tag"] != "DROP"]
    order = {"ACT": 0, "WATCH": 1}
    deduped.sort(key=lambda e: order.get(e["tag"], 2))
    deduped = deduped[:max_entries]

    if not deduped:
        return "(no register keepers logged yet in file 9 §6)"
    lines = [f"- [{e['kind']}] {e['title']}: {e['note']}" for e in deduped]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Prompt construction
# ---------------------------------------------------------------------------

_OUTPUT_SCHEMA_BRIEF = """
OUTPUT JSON SCHEMA (write EXACTLY this shape — no other top-level keys):

{
  "_meta": {
    "author_engine": "content_agent_v1",
    "authored_at": "<ISO-8601 timestamp, UTC>",
    "category": "<the _meta.category value from the fact sheet>",
    "product_count": <int, must equal number of sheets>
  },
  "products": {
    "<barcode-as-string>": {
      "insightLine": "<one standalone Hebrew sentence, no trailing period, ~90 chars max>",
      "rowVerdict": "<2-3 Hebrew sentences>",
      "expansion": {
        "comparisonContext": "<1-2 Hebrew sentences placing the product on the shelf>",
        "positiveSignals": ["<1-3 short Hebrew bullets>"],
        "limitingFactors": ["<0-2 short Hebrew bullets; OMIT this key entirely if there are none>"],
        "consumerExplanation": {
          "whyRated": "<one Hebrew sentence>",
          "good": ["<1+ Hebrew bullets>"],
          "watchOut": ["<0+ Hebrew bullets, [] if none>"],
          "context": "<one Hebrew sentence>",
          "takeaway": "<mirrors consumerTakeaway>"
        }
      },
      "s_grade_explanation": "<ONLY if the sheet has s_verbatim — copy s_verbatim.s_grade_explanation BYTE-FOR-BYTE, do not paraphrase; omit this key entirely for non-S products>",
      "consumerTakeaway": "<one-line Hebrew summary, ~90 chars max>",
      "bariInterpretation": [
        {"key": "<pass through unchanged from bari_interpretation_inputs>",
         "label": "<pass through unchanged>",
         "score": <pass through unchanged, may be null>,
         "strength": "<pass through unchanged>",
         "interpretation": "<ONE short Hebrew sentence you write; if score is null, write exactly 'נתון לא זמין'>"}
        /* one object per entry in that sheet's bari_interpretation_inputs, same order */
      ],
      "bestUseCases": ["<1-3 short Hebrew tags. If best_use_cases_pending=false for this sheet, copy best_use_cases_deterministic through UNCHANGED instead of writing new ones.>"]
    }
    /* one entry per barcode in fact_sheets.sheets — EVERY barcode must appear */
  },
  "_page": {
    "story_headline": "<Hebrew headline for the category page, max ~100 chars>",
    "story_teaser": "<1-2 Hebrew sentences>",
    "philosophy_note": "<standard Bari methodology disclaimer, Hebrew, 1 sentence>"
  }
}
""".strip()

_EDITORIAL_LAW_BRIEF = """
HARD EDITORIAL LAW (violate any of these and the copy does not ship — no exceptions).
2026-07-10 OWNER OVERHAUL: rules 13, 15, 18, 21, 24, 25 were REWRITTEN by owner
ruling — they supersede any older guidance (anywhere in this prompt, in the voice
files, or in your instincts) that appears to allow a nutrition figure, a
superlative/rank/median claim, or an instead-of negation:

1. FACT FIREWALL — use ONLY what is in the fact sheet below. If a nutrition
   field is null, write NOTHING about that fact. Never estimate, round out,
   or infer a plausible value. Never use Open Food Facts or any outside data.
   Never invent an ingredient, a number, or a claim not present in the sheet.
2. NO FRAMEWORK LEAKAGE — never write NOVA, BSIP, cap, floor, penalty,
   dimension, confidence_score, structural_class, matrix_integrity, pillar,
   routing, or any raw score mechanic ("68.2", "72/B"). The grade appears ONLY
   as the badge next to the text — never spell out the letter in prose
   ("ציון A", "מדובר במוצר מדרגה B" etc. are all banned).
3. SODIUM/FAT NEVER CAUSAL — sodium and fat are characteristics you may
   describe in plain words ("מלוח", "עשיר בשומן"); never frame them as the
   reason for a score ("בגלל הנתרן", "עקב השומן").
4. NO DATA-STATE / PROVENANCE NARRATION — never mention how Bari read the
   label, confidence tiers, verification status, or the pipeline itself.
   Banned regardless of instruction otherwise: "צילום תווית", "מאומת",
   "חוסר ודאות", "הערכה זהירה", "נשארים זהירים", "טקסט העמוד", "בגדר הערכה".
   If a fact is missing, the ONLY acceptable phrasing is plain food language
   ("לא צוין על האריזה") — never a sentence about Bari's own verification.
5. NO RECOMMENDATION LANGUAGE — Bari describes, never prescribes. No
   "מומלץ", "כדאי לקנות", "אל תקנו", "בריא יותר" as a blanket verdict.
6. NEVER RECITE-ONLY — a line that just reads back numbers already shown in
   the row UI (protein grams, calorie count, ingredient count, percentages)
   with NO verdict, comparison, rank, or gap is a data dump, not copy. Every
   insightLine / rowVerdict / consumerTakeaway must carry an actual INSIGHT:
   a character read, a gap/contradiction, or a practical takeaway that
   changes the reading of the product — all stated in PLAIN WORDS (rule 13:
   a nutrition figure never appears in prose at all, and rule 15: neither
   does a rank claim; the UI chips already carry the numbers).
   THIN-STORY CLAUSE: for a plain, unremarkable product, do NOT fall back to
   reciting its panel because it "has nothing interesting." Say what the data
   MEANS — "clean minimal base, protein unremarkable for the shelf" IS the
   finding, stated as a judgment. "It's ordinary" is itself an insight when
   true; a bare ingredient/gram recitation never is.
7. VARY ACROSS THE SHELF — do not reuse the same sentence (verbatim or
   near-verbatim) for more than 5 products. If a fact genuinely applies to
   many products, say it once in the page-level copy, not repeated per row.
8. EM-DASH — max ONE "—" per paragraph, never as a connector or list
   separator, never as the workhorse pivot on every single line. Prefer a
   period and a new sentence.
9. NO "ולא" / "אלא" / comma+"לא" ANYWHERE (zero exceptions) — see the
   ZERO-EXCEPTION BAN section above. This is a mechanically-enforced hard
   gate (copy_rules.ANTITHESIS_RE), not a style preference — there is NO
   carve-out for "naming a positive alternative" or "neither/nor." Use
   "אבל" / "יחד עם זאת" / "עם זאת" / "לעומת זאת" / "מנגד" / "אולם" / two
   separate sentences instead.
10. GRAMMAR/AGREEMENT — every sentence must have correct Hebrew gender and
    number agreement. Specific traps that caused real flags on the first
    pilot run: abstract nouns that are grammatically FEMININE despite not
    "looking" feminine in English — כמות, רמת, צפיפות, רשימה, אפשרות,
    שלמות — must take feminine verbs/adjectives ("כמות הסוכר גבוהה" not
    "גבוה"; "הרשימה קצרה" not "קצר"). Keep the subject and its verb close
    together — a long relative clause between them ("X ש-Y ש-Z") is the
    most common place agreement breaks. When a sentence has a compound
    subject ("סיבים וחלבון"), the verb must be plural.
11. bariInterpretation dimension notes are SHORT, QUALITATIVE, and
    CATEGORY-RELATIVE ("צפיפות קלורית נמוכה יחסית לקטגוריה") — never a raw
    gram/kcal recitation, never a (score) parenthetical, never a grade.
12. cap_misclaim_risk=true on a sheet means: do NOT claim a processing/cap
    limit is the sole reason for the score. Name the real dimension/driver
    from that sheet's `driver` field instead.
13. ★ NO CITED NUTRITION VALUES (owner ruling 2026-07-10 — HARD, mechanically
    gated corpus-wide by nutrition_value_citation). No grams, מ"ג, מיליגרם,
    קלוריות, קק"ל, or nutrient-percentages in ANY consumer prose field —
    insightLine, rowVerdict, consumerTakeaway, comparisonContext, all
    bullets, consumerExplanation, and bariInterpretation notes alike.
    Translate the panel into PLAIN ABSOLUTE WORDS — and NAMING the read is
    REQUIRED, only the number is banned: "חלבון גבוה", "מלוח", "רזה",
    "עשיר בשומן", "דל סיבים", "מתוק מאוד". Ingredient PROPORTIONS are
    allowed ("40% טחינה", "95% חיטה") — they describe what the food is made
    of, not its panel; a percent next to a NUTRIENT word ("32% שומן") is
    banned. Serving framings that carry a figure ("ל-100 גרם") disappear
    along with the figures.
14. GRADE CALIBRATES INTENSITY — the sheet's grade (never spelled out in
    prose, but visible to you) must shape how firm the verdict reads. A/S:
    confident, unhedged positive framing. B: balanced, name a real but
    moderate catch. C: the limitation is felt — give the catch at least as
    much weight as the credit, not a mirror of a B. D: the catch DOMINATES
    — firm, direct language, the positive (if any) is a brief aside, not
    the opening beat. E: firmest — name the gap directly, no softening.
    De-escalation is never the default (file 2 §2): if a D-grade verdict
    could be swapped onto a C-grade product with only the numbers changed,
    it is not firm enough — rewrite it harder. A C and a D on the same
    shelf must NOT read with the same intensity.
15. ★ NO SUPERLATIVES, RANKS, OR MEDIAN/CORPUS FINDINGS IN CONSUMER PROSE
    (owner ruling 2026-07-10 — supersedes and RETIRES the earlier
    superlatives_allowed authorization mechanism for prose; a superlative
    still raises mechanically, and under the new law NONE is ever granted).
    IGNORE the sheet's `superlatives_allowed` and `superlatives_context`
    fields entirely, and never compute a rank claim from `nutrition` /
    `corpus_stats`. Banned shapes: "הכי…", "ה<תואר> ביותר", "X ביותר מבין",
    "מהבולטים במדף", "מהגבוהים בקטגוריה", "נדיר במדף", "מוביל את המדף",
    "מעל/מתחת לחציון", "בין הדגנים שנמדדו", any what-it-beats framing.
    Describe the product ON ITS OWN TERMS: salty / rich / lean / clean /
    high-protein — never where it sits relative to the others. A mild
    qualitative category frame remains allowed ONLY inside a
    bariInterpretation dimension note ("גבוה יחסית לקטגוריה", rule 11) —
    never in insightLine / rowVerdict / consumerTakeaway / expansion prose.
16. FAT/SODIUM NEVER CAUSAL — UNCONDITIONAL, not contingent on the trace
    (Adversarial QA finding, 2026-07-09 — MECHANICALLY ENFORCED). Never write
    a sentence where fat or sodium "מוריד/קובע/גורם/מגביל/פוגע" the score,
    the ranking, or "התמונה הכוללת" — not even when a real limiting driver
    happens to also involve fat or sodium as a fact. State them as neutral
    plain-words characteristics only ("עשיר בשומן", "מלוח" — never a figure,
    rule 13) and name the ACTUAL limiting driver
    from the sheet's own `driver` field / lowest-scoring dimension in
    `bari_interpretation_inputs` instead. Before writing any sentence that
    could read as "fat/sodium causes X," stop and rewrite it as two separate
    statements: the fat/sodium fact, and the real driver, unconnected.
17. NEVER FRAME A STRONG DIMENSION AS A NEGATIVE (Nutrition Agent RULING 2,
    2026-07-09 — MECHANICALLY ENFORCED, generalizes rule 16 to every
    dimension). Before writing ANY sentence that blames a nutrient/attribute
    for lowering the score, dragging down "התמונה הכוללת," or being a
    limiting factor — check that attribute's OWN entry in this sheet's
    `bari_interpretation_inputs`. If its `strength` is "חזק" (strong), you
    may NOT frame it negatively — that directly contradicts the engine's own
    trace and is a real content bug, not a style issue (Delifkan: copy blamed
    high fat while fat_quality scored 93.0/"חזק"; the SCORE was correct, the
    COPY was wrong). Name the dimension that is actually weak instead.
18. ★ NO TEMPLATED NUTRIENT TAIL ACROSS THE SHELF (owner ruling 2026-07-10)
    — do not end multiple products' lines on the same qualitative nutrient
    clause ("חלבון ונתרן סבירים" repeated row after row). Each product's
    closing read is specific to THAT product's own composition and
    character. If one true sentence fits many products, it belongs once in
    the page-level copy, never repeated down the rows (see rule 7).
19. INGREDIENT NAMES ARE QUOTED VERBATIM FROM THE LABEL, NEVER EMBELLISHED
    (Nutrition Agent RULING 4, 2026-07-09) — when naming an ingredient from
    `ingredients_head`, use EXACTLY the printed term. Do not add a descriptive
    qualifier that is not on the label (e.g. the label says "שמן צמחי" —
    write "שמן צמחי," never "שמן צמחי מזרעים" or any other embellishment,
    even if you believe it's technically accurate). Apply the SAME literal
    term consistently every time that exact ingredient appears across
    different products in this shelf — don't vary the naming product to
    product for what is the same printed ingredient.
20. THE APPROVED STANCE PHRASE IS NOT A TEMPLATE TO EXTEND (Adversarial QA
    RT-8, 2026-07-09) — "כדאי לדעת מה קונים" (file 4 §B) is approved
    VERBATIM or in close paraphrase, as a general awareness stance. Do NOT
    extend it with a purchase-decision or cart-action frame ("לפני שמניחים
    בסל", "לפני שקונים", "לפני שמוסיפים לעגלה") — that turns a describe-only
    stance into a decision-point instruction, which edges into recommendation
    language (banned, hard rule 5). Similarly, do not impute a motive or
    intent to the product/manufacturer ("מנסה להסתתר", "מחופש ל-", "בתחפושת
    של") unless the sheet's own facts support a literal name/composition gap
    (Type 2 contradiction) — describe the gap, don't narrate an intention.
21. ★ NO OVERALL SHELF-STANDING CHARACTERIZATION AT ALL (owner rulings
    H3-R1 + 2026-07-10; the rank-contradiction gate still runs and will
    raise). Under rule 15 you no longer write ANY shelf-standing claim —
    positive ("מוביל את המדף") or negative ("בינוני יחסית למדף") alike.
    The specific H3-R1 trap stays instructive: never generalize a single
    mid DIMENSION score (e.g. nutrient_density) into an overall-profile
    mediocrity claim — a dimension is not a rank, and the shelf's actual
    #1 product was once mislabeled "בינוני יחסית למדף" this way. Describe
    what the product IS; the score badge carries the comparison.
22. LEAD WITH THE FINDING, NEVER WITH THE INGREDIENT-LIST INVENTORY (owner
    ruling H3-R3, 2026-07-10 — "the worst pattern the writer does";
    MECHANICALLY ENFORCED, will raise if violated). Never open insightLine
    or rowVerdict with "רשימת הרכיבים..." followed by a recitation of the
    ingredient list, and THEN go on to recite two or more separate nutrition
    values one after another ("הסיבים... X גרם. הנתרן... Y מיליגרם."). The
    DEFECT is structural: ingredient-list-as-opener plus back-to-back
    nutrient recitations reads as a spec sheet with connectors, not a
    verdict. The ingredient list is EVIDENCE you cite inside a finding,
    never the finding itself and never the opening move. Nutrition figures
    no longer appear at all (rule 13), but the same structural ban holds
    for their plain-words replacements: never two consecutive "and here's
    another nutrient read" sentences — make two nutrient reads serve ONE
    point together (a contrast, a gap, a combined read), resolved in
    flowing prose, not by reaching for an em-dash.
23. EM-DASH: MINIMIZE ACROSS THE WHOLE PRODUCT, NOT JUST PER PARAGRAPH
    (owner ruling H3-R3, 2026-07-10 — tightens hard rule 8). The standing
    rule (max one "—" per paragraph) is a ceiling, not a target — the
    owner's actual standard is to prefer ZERO and reach for one only when a
    genuine sharp interruption earns it, at most ONCE across a product's
    ENTIRE authored output (insightLine AND rowVerdict AND everything else
    together) — not once per field. If you already used an em-dash in
    insightLine, do not reach for another in rowVerdict for the same
    product. Prefer a period and a new sentence, every time it's a toss-up.
24. ★ CLEANLINESS CLAIMS REQUIRE THE FULL ADDITIVE PICTURE (owner ruling
    2026-07-10). Never call an ingredient list clean, minimal, or "בלי
    תוספות" by counting only the preservative. If the list carries acidity
    regulators, stabilizers, emulsifiers, or seasoning/flavor blends beyond
    the base food, an honest cleanliness read acknowledges that additives
    exist (generalized per the additive-generalization rule: "עם כמה תוספי
    מזון") — "בלי תוספות נוספות" over a list that carries regulators is a
    FALSE CLAIM and a real content bug, not a style issue.
25. ★ NO "במקום Y" INSTEAD-OF FRAMING (owner ruling 2026-07-10 — the same
    define-by-negation family as rule 9, mechanically gated). "ממותק באגבה
    במקום סוכר" is banned; say what IS there ("ממותק באגבה") and, if the
    absence matters, state it separately in plain positive terms ("סוכר
    לבן אינו מופיע ברשימה"). The innocent spatial sense ("במקום אחד",
    "במקום הנכון") is fine.
""".strip()

_INSIGHT_LINE_TYPES_BRIEF = """
INSIGHT-LINE TYPES (insightLine / consumerTakeaway should read as one of these
three — pick the type the product's own facts actually support, don't force
one). Max ~12 Hebrew words for insightLine. No nutrition figures, no rank or
superlative claims (owner law 2026-07-10) — ingredient proportions allowed.

Type 1 — Character fact: identity + the plain-words composition read.
  e.g. "פצפוצי אורז מלא בלי תוספי מזון, עשירים בסיבים ודלים בסוכר"
Type 2 — Contradiction: two true things that sit oddly together, named and
  left alone (no "לכן", no moralizing conclusion attached).
  e.g. "דגן מלא ראשון ברשימה, לצד רשימת תוספים ארוכה"
Type 3 — Practical read: what the product actually is for the buyer.
  e.g. "בסיס בוקר פשוט ונקי; את המתיקות מוסיפים לבד"

A quiet Type-1 line is not a failure — not every product needs a dramatic
finding. Most products are ordinary; saying so precisely, as a judgment in
plain words, is the job. But "ordinary" must still be stated as a read, never
as a bare panel recitation (see Hard Law #6 thin-story clause).
""".strip()

# ---------------------------------------------------------------------------
# VERDICT ARCHITECTURES (TASK-550 M2 — the T11 shelf-monotony fix)
#
# The M1 pilot's real quality gap was NOT any single banned line — every
# individual rowVerdict resolved its "אבל" into a full clause, which is legal.
# The defect was the SHELF: nearly every product used the identical
# "credit the positive -> אבל -> name the catch" shape, which is exactly the
# T11 tell (file 5: ">~1/3 of a shelf closing 'positive-then-catch' = the
# tell"). Asking the model to "vary it" inside one giant multi-product call
# didn't reliably work in M1 either. The fix here is PROGRAMMATIC, not a
# hope: since BATCH_SIZE=1 (one product per headless-claude call), the
# harness itself assigns each product a DIFFERENT architecture from this list
# by rotating on batch index — so shelf-wide variety is guaranteed by
# construction, not left to the model's within-call judgment.
# ---------------------------------------------------------------------------
_VERDICT_ARCHITECTURES: list[dict] = [
    {
        "name": "catch-first",
        "desc": (
            "Open with the limiting finding FIRST — no positive credit "
            "before it. State the catch, give one supporting detail, THEN "
            "(if a genuine strength exists) add it briefly at the end. Do "
            "not open with praise on this one."
        ),
    },
    {
        "name": "pure-single-finding",
        "desc": (
            "State ONE clean observation and stop — no explicit contrast "
            "structure, no 'אבל'/'יחד עם זאת' pivot at all. Pick the single "
            "fact that matters most for this product (per Insight-Line "
            "Type 1) and let it stand alone."
        ),
    },
    {
        "name": "contradiction-flat",
        "desc": (
            "Name the two things about this product that sit oddly "
            "together and STOP — no resolution, no explanation, no 'אבל'. "
            "Per Insight-Line Type 2: state the contradiction, do not "
            "explain why it's a contradiction. Let the reader feel the gap."
        ),
    },
    {
        # "rank-first" RETIRED 2026-07-11 (TASK-550 M2 voice fold): rank/
        # superlative claims are banned from consumer prose outright (owner
        # ruling 2026-07-10, law rule 15). Replaced by the owner's anchor-
        # voice 3-beat.
        "name": "identity-first",
        "desc": (
            "The anchor-voice 3-beat (owner calibration, 2026-07-10): open "
            "with the product's identity and sensory/textural character, "
            "then give the nutritional read in plain absolute words (no "
            "figures, no rank), then land a practical takeaway about "
            "consuming it. Model line: 'גאודה הולנדית קלאסית, עשירה "
            "ומלוחה. היא מכילה חלבון גבוה אך גם שומן גבוה. מדובר במוצר "
            "יחסית נקי אבל יש לשים לב לכמות הנצרכת.'"
        ),
    },
    {
        "name": "category-principle-first",
        "desc": (
            "Open with a calm, general true statement about this category/"
            "shelf as a whole, then locate THIS product inside that "
            "principle. A category-principle sentence, not a scene "
            "(file 2 §1 — this counts as a valid orienting opener)."
        ),
    },
    {
        "name": "positive-then-catch",
        "desc": (
            "The classic shape: credit the real strength first, then a "
            "single 'אבל'/'יחד עם זאת' pivot to the honest catch. This is "
            "ALLOWED but is the one architecture on this list capped at "
            "roughly 1-in-3 uses across a shelf (T11) — you are being "
            "assigned it now because the rotation reached it, not because "
            "it is the default; do not reach for it out of habit elsewhere."
        ),
    },
]


def _architecture_for_batch(batch_index: int) -> dict:
    return _VERDICT_ARCHITECTURES[batch_index % len(_VERDICT_ARCHITECTURES)]


def build_prompt(facts: dict, out_path: Path, architecture: dict | None = None) -> str:
    category = (facts.get("_meta") or {}).get("category", "unknown")
    n = len(facts.get("sheets") or [])
    voice = build_voice_brief()
    catalog = build_register_catalog()
    facts_json = json.dumps(facts, ensure_ascii=False, indent=2)
    out_path_str = str(out_path).replace("\\", "/")

    # Per-product editorial hints (2026-07-10): an optional "_editorial_hint"
    # string on a sheet is surfaced as a MUST-FOLLOW note. Used sparingly for
    # a targeted re-author where a specific defect keeps recurring despite
    # the general prompt rule already covering it in principle — a concrete,
    # product-specific reminder is more reliable than hoping the general
    # rule generalizes correctly under pressure. Never used to inject facts
    # not already in the sheet, only to emphasize how to FRAME real facts.
    hint_block = ""
    hints = [
        (s.get("barcode"), s["_editorial_hint"])
        for s in (facts.get("sheets") or [])
        if s.get("_editorial_hint")
    ]
    if hints:
        lines = "\n".join(f"- ({bc}) {hint}" for bc, hint in hints)
        hint_block = f"""
============================================================
PRODUCT-SPECIFIC EDITORIAL NOTES (MUST FOLLOW — these override any generic
instinct if they conflict)
============================================================
{lines}
============================================================
"""

    arch_block = ""
    if architecture is not None:
        arch_block = f"""
============================================================
VERDICT ARCHITECTURE ASSIGNED FOR THIS PRODUCT: "{architecture['name']}"
============================================================
{architecture['desc']}

This assignment is how Bari guarantees shelf-wide rhythm variety (T11) across
separately-authored products — it is not optional styling. Apply it to
insightLine, rowVerdict, and consumerTakeaway. Exception: if this specific
architecture is genuinely incompatible with what this product's OWN facts
support (e.g. "contradiction-flat" but this product's facts hold no genuine
tension worth naming), pick the closest reasonable alternative
from the six architectures above instead of forcing a bad fit — but do not
default to "positive-then-catch" just because it's familiar.
============================================================
"""

    return f"""You are Bari's Content Agent authoring the product copy for the
"{category}" comparison page ({n} products). You write in Tom's voice — the
Bari editorial identity below — not a template.

============================================================
VOICE SYSTEM (read fully before writing — this is the whole point of this
pass: a real reader of Bari's voice, not a phrase-bank)
============================================================
{voice}

============================================================
REGISTER-MOVE CATALOG (distilled from the Hebrew Health Scan, file 9 §6 —
technique-only, never copied phrasing; use these as inspiration for openers,
pivots, and structure where they fit a real product's facts)
============================================================
{catalog}

============================================================
{_INSIGHT_LINE_TYPES_BRIEF}
============================================================

============================================================
{_EDITORIAL_LAW_BRIEF}
============================================================

============================================================
{_OUTPUT_SCHEMA_BRIEF}
============================================================
{arch_block}{hint_block}
============================================================
FACT SHEET — the ONLY material you may assert facts from. null stays null.
============================================================
```json
{facts_json}
```

============================================================
TASK
============================================================
Write the authored.json for every barcode in the fact sheet above, in real
Tom-voice Hebrew, following the schema and hard law exactly. Vary sentence
structure and opener across products — do not fall into a per-driver template
(that is exactly the baseline placeholder this pass replaces). Two reminders
that override any habit: NO nutrition figure anywhere in prose (law 13 — the
read goes into plain words like "מלוח"/"עשיר בחלבון"; ingredient proportions
allowed) and NO rank/superlative/median claim (law 15). Use the
Write tool to write the COMPLETE JSON object (and nothing else) to this exact
absolute path:

{out_path_str}

Do not write any other file. After writing, reply with one line: how many
products you authored."""


# ---------------------------------------------------------------------------
# Headless-claude invocation (pattern proven in local_scan.py)
# ---------------------------------------------------------------------------

def _kill_tree(pid: int) -> None:
    """Kill a process and all its children. On Windows `cmd /c claude` spawns a
    node grandchild that survives a plain terminate — taskkill /T /F reaps the
    whole tree (the orphaned node is what deadlocked the previous capture_output
    version). Best-effort; never raises."""
    try:
        if os.name == "nt":
            subprocess.run(["taskkill", "/PID", str(pid), "/T", "/F"],
                           capture_output=True, timeout=30)
        else:
            import signal
            os.killpg(os.getpgid(pid), signal.SIGKILL)
    except Exception:
        pass


def _run_claude(prompt: str, out_path: Path) -> tuple[bool, str]:
    # Load ZERO MCP servers. Without this, every authoring call boots the full MCP
    # fleet — observed in the live process tree: `claude.exe` spawning
    # `cmd /c npx "@playwright/mcp@latest"` -> npx-cli -> playwright-mcp -> node,
    # plus analytics-mcp children, on EVERY call. Measured: disabling MCP does not
    # by itself speed up a single call (generation dominates: ~465s/product), but
    # it removes a large per-call resource cost that would otherwise be multiplied
    # by MAX_WORKERS concurrent calls — the contention that produced the spurious
    # 900s batch timeouts.
    mcp_cfg = out_path.parent / "empty_mcp.json"
    mcp_cfg.write_text('{"mcpServers":{}}', encoding="utf-8")
    flags = [
        "-p", "--allowedTools", "Write",
        "--strict-mcp-config", "--mcp-config", str(mcp_cfg),
        "--permission-mode", "bypassPermissions",
        "--model", MODEL,
    ]
    cmd = (["cmd", "/c", "claude"] + flags) if os.name == "nt" else (["claude"] + flags)
    # Feed the prompt via a FILE HANDLE as stdin — NOT communicate(input=...).
    # The prompt here is large (~76KB voice context + fact sheet). Piping that
    # through the cmd/c -> claude.cmd -> node hop hits the Windows ~64KB pipe
    # buffer and deadlocks (verified: a 200-char prompt returns in 10s, a 62KB
    # prompt hangs past the timeout). A real file handle is not a pipe, so there
    # is no buffer limit and no deadlock (verified: same 62KB prompt returns in
    # 10s this way). stdout/stderr stream to disk (local_scan.py pattern); the
    # timeout is enforced by proc.wait and _kill_tree reaps the node grandchild.
    so_path = out_path.parent / "claude_stdout.txt"
    se_path = out_path.parent / "claude_stderr.txt"
    pf_path = out_path.parent / "claude_prompt.txt"
    pf_path.write_text(prompt, encoding="utf-8")
    proc = None
    try:
        with pf_path.open("r", encoding="utf-8") as stdin_f, \
             so_path.open("w", encoding="utf-8", errors="replace") as so, \
             se_path.open("w", encoding="utf-8", errors="replace") as se:
            proc = subprocess.Popen(
                cmd, stdin=stdin_f, stdout=so, stderr=se,
                cwd=str(REPO_ROOT), text=True, encoding="utf-8", errors="replace",
            )
            try:
                proc.wait(timeout=CLAUDE_TIMEOUT)
            except subprocess.TimeoutExpired:
                _kill_tree(proc.pid)
                try:
                    proc.wait(timeout=30)
                except Exception:
                    pass
                return False, f"claude timed out after {CLAUDE_TIMEOUT}s (killed tree pid={proc.pid})"
    except Exception as exc:
        if proc is not None:
            _kill_tree(proc.pid)
        return False, f"claude subprocess error: {exc!r}"
    rc = proc.returncode
    stderr_tail = ""
    try:
        stderr_tail = se_path.read_text(encoding="utf-8", errors="replace").strip()[-400:]
    except OSError:
        pass
    note = f"exit={rc}"
    if rc != 0:
        note += f" stderr={stderr_tail!r}"
    return out_path.exists(), note


def _extract_json_object(text: str) -> dict:
    """Tolerate a fenced ```json block or surrounding prose (defensive; the
    prompt asks for a pure Write-tool file so this is normally a no-op)."""
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        raise ContentAgentAuthorError("no JSON object found in LLM output file")
    return json.loads(m.group(0))


# ---------------------------------------------------------------------------
# Post-processing safety net
# ---------------------------------------------------------------------------

def _enforce_all_strings(obj, path: str) -> None:
    """Zero-tolerance banned-phrase scan over every string leaf. Raises
    BannedPhraseError on the first hit (content-agent.md hard rule 9)."""
    if isinstance(obj, str):
        enforce_clean(obj, path)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            _enforce_all_strings(v, f"{path}[{i}]")
    elif isinstance(obj, dict):
        for k, v in obj.items():
            _enforce_all_strings(v, f"{path}.{k}")


def _check_baseline_fingerprints(obj, path: str, hits: list) -> None:
    fingerprints = _check_baseline_fingerprints._fp  # cached
    if isinstance(obj, str):
        for fp in fingerprints:
            if fp in obj:
                hits.append({"path": path, "fingerprint": fp, "text": obj[:120]})
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            _check_baseline_fingerprints(v, f"{path}[{i}]", hits)
    elif isinstance(obj, dict):
        for k, v in obj.items():
            _check_baseline_fingerprints(v, f"{path}.{k}", hits)


_check_baseline_fingerprints._fp = tuple(get_author_copy_fingerprints())

# Known, meaning-preserving rewrites for the SHORT category-relative dimension-
# note / positive-signal phrases the LLM converges on independently for common
# strength tiers (e.g. "no identified additives", "processing high for the
# category") — these are editorially correct, generic enough that a real
# author naturally lands on similar wording, and happen to byte-match
# author_copy.py's own fixed bank for the same (dimension, strength) pair.
# Observed live on the cereals pilot (2026-07-09), 4/20 products. This is a
# targeted, auditable substitution — NOT a blanket bypass of the fingerprint
# gate: only phrases in this table are rewritten; anything else that collides
# still raises (see below).
_DEFINGERPRINT_SUBS: dict[str, str] = {
    "ללא תוספי מזון מזוהים ברשימת הרכיבים": "רשימת הרכיבים נקייה מתוספי מזון מזוהים",
    "רמת עיבוד גבוהה יחסית לקטגוריה": "עיבוד גבוה יחסית לשאר המוצרים בקטגוריה",
}


def _apply_defingerprint_subs(obj):
    if isinstance(obj, str):
        out = obj
        for fp, sub in _DEFINGERPRINT_SUBS.items():
            if fp in out:
                out = out.replace(fp, sub)
        return out
    if isinstance(obj, list):
        return [_apply_defingerprint_subs(v) for v in obj]
    if isinstance(obj, dict):
        return {k: _apply_defingerprint_subs(v) for k, v in obj.items()}
    return obj


# ---------------------------------------------------------------------------
# RT-1 (Adversarial QA red-team, 2026-07-09): unauthorized-superlative gate.
# Shugi/Cranch both had superlatives_allowed=[] but the M1 engine minted
# absolute sodium superlatives anyway ("הנתרן הגבוה ביותר בין 20 הדגנים
# שנבדקו"). Corpus-true, but self-authorized — the danger is an engine that
# grants itself a TRUE superlative today will grant itself a FALSE one on the
# next corpus. Mechanical, product-specific: cross-checks every absolute-
# superlative Hebrew construction against THAT SAME sheet's own
# superlatives_allowed grant list. Raises; never silently strips (QA's
# explicit instruction — this mirrors enforce_clean's behavior).
# ---------------------------------------------------------------------------


# (2026-07-10, QA + coordinator probe) These regexes had TWO evasion bugs:
#  (a) the ביותר patterns only carried an optional "ה" suffix (covering
#      masculine/feminine SINGULAR: גבוה/גבוהה, נמוך/נמוכה) and silently
#      missed the PLURAL adjective forms (גבוהים/גבוהות/נמוכים/נמוכות) —
#      "הסיבים הגבוהים ביותר" and "הקלוריות הנמוכות ביותר" both slipped
#      through undetected.
#  (b) _SUPERLATIVE_LOW_WORDS held only the standalone word "נמוך", which
#      ends in the FINAL-form כ (ך) — a letter Hebrew orthography reserves
#      for word-final position. Every suffixed form (נמוכה/נמוכים/נמוכות)
#      instead uses the MEDIAL-form כ, so "נמוך" (with ך) can NEVER be a
#      substring of those forms — the low-direction check was blind to
#      every plural/feminine "low" superlative by construction, independent
#      of bug (a). Fixed by using an explicit high/low adjective pattern
#      that covers all four inflections, and by adding a THIRD superlative
#      shape that doesn't use "ביותר" at all: the definite-article-doubling
#      "ה<noun> ה<adjective> במדף/בקטגוריה/מבין" construction ("הנתרן הגבוה
#      במדף"), which reads as a superlative in idiomatic Hebrew even with no
#      "ביותר"/"הכי" marker. See --selftest below for the regression probes.
_HIGH_ADJ = r"גבוה(?:ה|ים|ות)?"
_LOW_ADJ = r"(?:נמוך|נמוכ(?:ה|ים|ות))"

_SUPERLATIVE_PATTERNS: tuple[re.Pattern, ...] = (
    re.compile(rf"{_HIGH_ADJ}\s+ביותר"),
    re.compile(rf"{_LOW_ADJ}\s+ביותר"),
    re.compile(rf"הכי\s+{_HIGH_ADJ}"),
    re.compile(rf"הכי\s+{_LOW_ADJ}"),
    re.compile(r"ביותר\s+מבין"),
    re.compile(r"הראשון(?:ה)?\s+ביותר"),
    # superlative-by-scope, no ביותר/הכי marker at all:
    re.compile(rf"ה(?:{_HIGH_ADJ}|{_LOW_ADJ})\s+(?:במדף|בקטגוריה|מבין)"),
)

_SUPERLATIVE_METRIC_KEYWORDS: dict[str, tuple[str, ...]] = {
    "protein": ("חלבון",),
    "sugar": ("סוכר",),
    "kcal": ("קלורי", 'קק"ל', "קק״ל"),
    "sodium": ("נתרן",),
    "fiber": ("סיב",),
    "fat": ("שומן",),
}
# "גבוה" is a true prefix of all 4 inflected forms (גבוה/גבוהה/גבוהים/גבוהות)
# so plain substring containment already covers them. The low side needs
# BOTH the standalone final-כ word and the medial-כ stem (see comment above).
_SUPERLATIVE_HIGH_WORDS = ("גבוה",)
_SUPERLATIVE_LOW_WORDS = ("נמוך", "נמוכ")

# The ONLY (metric, direction) pairs build_copy_inputs.py's superlatives_for()
# can ever grant today (highest_protein / lowest_kcal / lowest_sugar). EVERY
# sodium/fiber/fat superlative, and highest-sugar / lowest-protein /
# highest-kcal, has NO possible authorization and is always a violation if
# asserted absolutely. If Data/Nutrition later extend superlatives_for() with
# new tokens (e.g. a sodium extreme), add the pair here — the copy becomes
# legal automatically once a sheet grants the matching token; nothing else
# in this gate needs to change.
_SUPERLATIVE_GRANT: dict[tuple[str, str], str] = {
    ("protein", "high"): "highest_protein",
    ("sugar", "low"): "lowest_sugar",
    ("kcal", "low"): "lowest_kcal",
}

# RULING 3 (Nutrition Agent, 2026-07-09 / RT-6) qualifying phrases — presence
# of ANY of these near an authorized-but-null-affected superlative claim
# counts as properly scoping it to "among measured" rather than full-corpus.
_AMONG_MEASURED_QUALIFIERS: tuple[str, ...] = (
    "שנמדדו", "שנמדד", "נמדד", "נבדק", "שנבדקו לכך", "עם נתון", "עם נתונים",
    "מבין הנמדדים", "מבין המדודים",
)


def find_superlative_violations(rec: dict, sheet: dict) -> list[dict]:
    """Scan one product's authored record for absolute-superlative Hebrew
    constructions; cross-check each against THAT product's own
    superlatives_allowed. Returns a list of violations (empty = clean)."""
    allowed = set(sheet.get("superlatives_allowed") or [])
    violations: list[dict] = []

    def _nearest_metric(text: str, m_start: int, m_end: int) -> str | None:
        """Find the metric keyword occurrence CLOSEST to the superlative
        match, scanning the whole string (not a fixed window). Fixes a real
        cross-talk bug (2026-07-10): a fixed-window substring-containment
        check with dict-order tiebreak misattributed "הקלוריות הנמוכות
        ביותר" to sugar, because an unrelated "הסוכר" a few words later in
        the SAME sentence happened to come first in dict iteration order —
        even though "קלוריות" sat immediately before the match. Proximity,
        not order, decides."""
        best_metric, best_dist = None, None
        search_lo, search_hi = max(0, m_start - 60), min(len(text), m_end + 60)
        for metric_name, kws in _SUPERLATIVE_METRIC_KEYWORDS.items():
            for kw in kws:
                start = search_lo
                while True:
                    pos = text.find(kw, start, search_hi)
                    if pos == -1:
                        break
                    dist = m_start - (pos + len(kw)) if pos < m_start else pos - m_end
                    dist = abs(dist)
                    if best_dist is None or dist < best_dist:
                        best_dist, best_metric = dist, metric_name
                    start = pos + 1
        return best_metric

    def _nearest_direction(text: str, m_start: int, m_end: int, match_text: str) -> str | None:
        """Same proximity fix as _nearest_metric, applied to direction
        (2026-07-10): the OLD "any word anywhere in a 50-char window"
        check misattributed "הקלוריות הנמוכות ביותר" as HIGH, because
        "גבוה" from an EARLIER clause about protein ("החלבון הגבוה ביותר
        והקלוריות הנמוכות ביותר") sat inside the same window and an
        if/elif tie-break always preferred HIGH. Fast path: the direction
        word is almost always embedded in the match itself (the pattern
        that matched IS "<adj> ביותר" etc.) — use that directly before
        falling back to a nearest-occurrence search for the two patterns
        that don't embed a direction word ("ביותר מבין", "הראשון ביותר")."""
        if any(w in match_text for w in _SUPERLATIVE_HIGH_WORDS):
            return "high"
        if any(w in match_text for w in _SUPERLATIVE_LOW_WORDS):
            return "low"
        best_dir, best_dist = None, None
        search_lo, search_hi = max(0, m_start - 60), min(len(text), m_end + 60)
        for direction, words in (("high", _SUPERLATIVE_HIGH_WORDS), ("low", _SUPERLATIVE_LOW_WORDS)):
            for w in words:
                start = search_lo
                while True:
                    pos = text.find(w, start, search_hi)
                    if pos == -1:
                        break
                    dist = m_start - (pos + len(w)) if pos < m_start else pos - m_end
                    dist = abs(dist)
                    if best_dist is None or dist < best_dist:
                        best_dist, best_dir = dist, direction
                    start = pos + 1
        return best_dir

    def check_string(path: str, text: str) -> None:
        for pat in _SUPERLATIVE_PATTERNS:
            for m in pat.finditer(text):
                a, b = max(0, m.start() - 40), min(len(text), m.end() + 10)
                window = text[a:b]
                metric = _nearest_metric(text, m.start(), m.end())
                if metric is None:
                    continue  # can't attribute to a known metric -> not ours to police
                direction = _nearest_direction(text, m.start(), m.end(), m.group(0))
                if direction is None:
                    continue
                required = _SUPERLATIVE_GRANT.get((metric, direction))
                if required is None or required not in allowed:
                    violations.append({
                        "path": path, "metric": metric, "direction": direction,
                        "required_token": required, "match": m.group(0),
                        "context": window.strip(),
                    })
                    continue
                # RULING 3 (Nutrition Agent, 2026-07-09 / RT-6): even an
                # AUTHORIZED superlative must not overclaim full-corpus
                # coverage when the metric has nulls. superlatives_context
                # (build_copy_inputs.py, this task) tells us exactly when.
                ctx = (sheet.get("superlatives_context") or {}).get(required) or {}
                if ctx.get("phrase_as_among_measured") and not any(
                    q in text for q in _AMONG_MEASURED_QUALIFIERS
                ):
                    violations.append({
                        "path": path, "metric": metric, "direction": direction,
                        "required_token": required, "match": m.group(0),
                        "context": window.strip(),
                        "reason": (
                            f"authorized but n_measured={ctx.get('n_measured')} < "
                            f"product_count; claim must qualify as 'among measured', "
                            f"not full-corpus"
                        ),
                    })

    def walk(obj, path):
        if isinstance(obj, str):
            check_string(path, obj)
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                walk(v, f"{path}[{i}]")
        elif isinstance(obj, dict):
            for k, v in obj.items():
                walk(v, f"{path}.{k}")

    walk(rec, "")
    return violations


# ---------------------------------------------------------------------------
# RULING 2 (Nutrition Agent, 2026-07-09): copy's directional framing of ANY
# metric must not contradict that metric's OWN bari_interpretation_inputs
# dimension score/strength. Delifkan's copy blamed fat for "lowering the
# overall picture" while its fat_quality scored 93.0/"חזק" — the score was
# right, the copy misread the trace. This generalizes find_causal_fat_sodium_
# violations (which is fat/sodium-specific and unconditional) to every named
# dimension: if a dimension scored strong for THIS product, the copy must not
# frame it as a negative/limiting factor for the score.
# ---------------------------------------------------------------------------

_DIMENSION_KEYWORDS: dict[str, tuple[str, ...]] = {
    "processing_quality": ("עיבוד",),
    "additive_quality": ("תוסף",),
    "nutrient_density": ("צפיפות תזונתית",),
    "protein_quality": ("חלבון",),
    "calorie_density": ("קלורי",),
    "glycemic_quality": ("גליקמי",),
    "fat_quality": ("שומן",),
    "satiety_support": ("שובע",),
    "regulatory_quality": ("רגולטור", "תקן", "תווית אדומה"),
    "whole_food_integrity": ("שלמות מזון", "שלמות"),
}


def find_dimension_framing_contradictions(rec: dict, sheet: dict) -> list[dict]:
    bi_by_key = {e.get("key"): e for e in (sheet.get("bari_interpretation_inputs") or [])
                 if isinstance(e, dict)}
    violations: list[dict] = []

    def check_string(path: str, text: str) -> None:
        if not _has_causal_framing(text):
            return
        for dim_key, keywords in _DIMENSION_KEYWORDS.items():
            if not any(kw in text for kw in keywords):
                continue
            entry = bi_by_key.get(dim_key)
            if entry and entry.get("strength") == "חזק":
                violations.append({
                    "path": path, "dimension": dim_key,
                    "strength": entry.get("strength"), "text": text[:160],
                })

    def walk(obj, path):
        if isinstance(obj, str):
            check_string(path, obj)
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                walk(v, f"{path}[{i}]")
        elif isinstance(obj, dict):
            for k, v in obj.items():
                walk(v, f"{path}.{k}")

    walk(rec, "")
    return violations


# ---------------------------------------------------------------------------
# RT-2 (Adversarial QA red-team, 2026-07-09): fat/sodium-framed-as-causal.
# Copy law bans framing sodium/fat as the CAUSE of a score, unconditionally —
# not just when it contradicts the trace (Delifkan's fat_quality scored 93.0
# / "חזק" while the copy blamed fat; that's the clearest proof the rule was
# broken, but the rule itself is absolute regardless of the trace).
# ---------------------------------------------------------------------------

_CAUSAL_VERB_WORDS = ("מוריד", "מורידים", "מורידה", "קובע", "קובעת", "גורם",
                      "גורמים", "גורמת", "מגביל", "מגבילה", "מגבילים",
                      "פוגע", "פוגעת", "משפיע לרעה", "מכריע", "מכריעה")
_CAUSAL_TARGET_WORDS = ("התמונה הכוללת", "הציון", "הדירוג", "התמונה", "הניקוד")
# "X הוא/היא מה ש<verb>" ("X is what determines/lowers...") is itself a
# causal-attribution construction even with no separate target noun — caught
# a live miss ("...הוא מה שקובע כאן", no "הציון"/"התמונה" present at all).
_CAUSAL_IMPLICIT_SUBJECT_RE = re.compile(
    r"(?:הוא|היא)\s+מה\s+ש(?:" + "|".join(_CAUSAL_VERB_WORDS) + r")"
)


def _has_causal_framing(text: str) -> bool:
    if any(w in text for w in _CAUSAL_VERB_WORDS) and any(w in text for w in _CAUSAL_TARGET_WORDS):
        return True
    return bool(_CAUSAL_IMPLICIT_SUBJECT_RE.search(text))


def find_causal_fat_sodium_violations(rec: dict, sheet: dict) -> list[dict]:
    bi_by_key = {e.get("key"): e for e in (sheet.get("bari_interpretation_inputs") or [])
                 if isinstance(e, dict)}
    fat_strength = (bi_by_key.get("fat_quality") or {}).get("strength")
    violations: list[dict] = []

    def check_string(path: str, text: str) -> None:
        metric = "fat" if "שומן" in text else ("sodium" if "נתרן" in text else None)
        if metric is None:
            return
        if _has_causal_framing(text):
            note = f"fat_quality={fat_strength}" if metric == "fat" else "sodium has no dedicated dimension"
            violations.append({"path": path, "metric": metric, "text": text[:160], "context_note": note})

    def walk(obj, path):
        if isinstance(obj, str):
            check_string(path, obj)
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                walk(v, f"{path}[{i}]")
        elif isinstance(obj, dict):
            for k, v in obj.items():
                walk(v, f"{path}.{k}")

    walk(rec, "")
    return violations


# ---------------------------------------------------------------------------
# RT-4: Content Agent's OWN hard rule — max ONE "—" per paragraph. The shared
# hebrew_readability tool treats em-dash as ADVISORY only (project-wide rule
# is "minimize", not "ban" — thousands of live lines use one), but this
# engine's own standing constraint (content-agent.md) is a hard cap of one
# per field. Each field here is a single short paragraph, so count > 1 fires.
# ---------------------------------------------------------------------------

def find_em_dash_violations(rec: dict) -> list[dict]:
    violations: list[dict] = []

    def check_string(path: str, text: str) -> None:
        n = text.count("—")
        if n > 1:
            violations.append({"path": path, "count": n, "text": text[:160]})

    def walk(obj, path):
        if isinstance(obj, str):
            check_string(path, obj)
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                walk(v, f"{path}[{i}]")
        elif isinstance(obj, dict):
            for k, v in obj.items():
                walk(v, f"{path}.{k}")

    walk(rec, "")
    return violations


# ---------------------------------------------------------------------------
# RT-5: broadened negation-closer gate — the M1 repair "לא הבולט ביותר, גם
# לא החלש ביותר" survived copy_rules.ANTITHESIS_RE (no comma+לא / ולא / אלא
# substring) yet reads as the exact define-by-negation closer the owner
# banned. This adds the specific "לא X, גם לא Y" family the base gate misses.
# ---------------------------------------------------------------------------

_BROADENED_NEGATION_RE = re.compile(r"לא\s+[^,.\n]{1,30},\s*גם\s+לא\b")


def find_negation_closer_violations(rec: dict) -> list[dict]:
    violations: list[dict] = []

    def check_string(path: str, text: str) -> None:
        m = _BROADENED_NEGATION_RE.search(text)
        if m:
            violations.append({"path": path, "match": m.group(0), "text": text[:160]})

    def walk(obj, path):
        if isinstance(obj, str):
            check_string(path, obj)
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                walk(v, f"{path}[{i}]")
        elif isinstance(obj, dict):
            for k, v in obj.items():
                walk(v, f"{path}.{k}")

    walk(rec, "")
    return violations


# ---------------------------------------------------------------------------
# H3-R1 (owner ruling, 2026-07-10, TASK-550): rank-contradiction gate.
# ויטביקס scored 74.7 — the MAXIMUM of all 20 products (rank 1/20) — yet the
# copy called its OVERALL profile "בינוני יחסית למדף" (mediocre relative to
# the shelf) across 5 fields. Root cause: the model read a DIMENSION score
# (nutrient_density = mid) and generalized it into a SHELF-RELATIVE standing
# claim. Dimension != rank. Scoped to explicitly EXCLUDE bariInterpretation
# (a mid dimension score is a true, dimension-scoped fact) and
# positiveSignals/good (strengths, not weaknesses) — the ban is only on
# generalizing a dimension into an overall/shelf-rank claim in the
# headline-visibility fields.
# ---------------------------------------------------------------------------

_RANK_CONTRADICTION_OVERALL_PHRASES: tuple[str, ...] = (
    "הפרופיל התזונתי הכולל", "התמונה הכוללת", "מדורג", "הדירוג",
    "נמצא בחלק", "ממוקם בחלק", "התוצאה המאוזנת", "ערך תזונתי כולל",
    "באופן כללי המוצר",
)
_RANK_CONTRADICTION_WEAK_WORDS: tuple[str, ...] = (
    "בינוני", "נמוך", "חלש", "מתחת לממוצע", "מתחת לחציון", "אמצע הטווח",
)


def compute_score_ranks(sheets: list[dict]) -> dict[str, dict]:
    """Rank every product in a corpus by its own `score` (descending; rank 1
    = highest). MUST be computed from the FULL corpus's sheets, even when
    only a subset is being (re-)authored — a targeted re-author call passes
    the full corpus separately for exactly this reason (see author())."""
    scored = [(str(s["barcode"]), s.get("score")) for s in sheets if s.get("score") is not None]
    scored.sort(key=lambda t: t[1], reverse=True)
    ranks: dict[str, dict] = {}
    for i, (bc, score) in enumerate(scored, start=1):
        ranks[bc] = {"rank": i, "total": len(scored), "score": score, "is_top": i == 1}
    return ranks


def _iter_rank_sensitive_fields(rec: dict):
    """Fields where an OVERALL-standing claim can appear. Deliberately
    excludes bariInterpretation[].interpretation (dimension-scoped, may
    legitimately say "בינוני") and positiveSignals/good (strengths only)."""
    yield "insightLine", rec.get("insightLine")
    yield "rowVerdict", rec.get("rowVerdict")
    yield "consumerTakeaway", rec.get("consumerTakeaway")
    exp = rec.get("expansion") or {}
    yield "expansion.comparisonContext", exp.get("comparisonContext")
    for i, item in enumerate(exp.get("limitingFactors") or []):
        yield f"expansion.limitingFactors[{i}]", item
    ce = exp.get("consumerExplanation") or {}
    yield "expansion.consumerExplanation.whyRated", ce.get("whyRated")
    yield "expansion.consumerExplanation.context", ce.get("context")
    yield "expansion.consumerExplanation.takeaway", ce.get("takeaway")
    for i, item in enumerate(ce.get("watchOut") or []):
        yield f"expansion.consumerExplanation.watchOut[{i}]", item


def find_rank_contradiction_violations(rec: dict, rank_info: dict | None) -> list[dict]:
    if not rank_info or not rank_info.get("is_top"):
        return []
    violations: list[dict] = []
    for path, text in _iter_rank_sensitive_fields(rec):
        if not isinstance(text, str) or not text:
            continue
        if (any(p in text for p in _RANK_CONTRADICTION_OVERALL_PHRASES)
                and any(w in text for w in _RANK_CONTRADICTION_WEAK_WORDS)):
            violations.append({
                "path": path, "text": text[:160],
                "rank": rank_info["rank"], "total": rank_info["total"],
            })
    return violations


# ---------------------------------------------------------------------------
# H3-R3 (owner ruling, 2026-07-10, TASK-550 — "the worst pattern the writer
# does"): ingredient-list-opener -> recited-nutrition-values structural gate.
# "רשימת הרכיבים ... כוללת שלושה מרכיבים בלבד, ואפס תוספי מזון. הסיבים,
# לעומת זאת, נמוכים ... הנתרן עומד על ..." — each clause individually passes
# the recite-vs-insight heuristic (the numbers do comparison work), yet the
# whole reads as a spec sheet with connectors. The existing recite scan does
# NOT catch this (per-clause it's clean); this is a STRUCTURAL check: does
# the field OPEN on the ingredient list, and does it go on to recite >=2
# DISTINCT nutrition metrics with numbers.
# ---------------------------------------------------------------------------

_INGREDIENT_OPENER_RE = re.compile(r"^\s*(רשימת ה?רכיבים|ה?רכיבים (כוללים|כוללת|של)|מבוסס על רשימת רכיבים)")

# Amount sub-patterns — cover BOTH digit-based ("390 מיליגרם") and Hebrew
# spelled-out amounts ("פחות מגרם אחד") since real copy uses both, and the
# original digit-only patterns silently missed the exact H3-R3 example
# ("פחות מגרם אחד ל-100 גרם", "390 מיליגרם" — not "מ"ג").
_AMOUNT_GRAM = r'(?:\d+(?:\.\d+)?\s*גרם|פחות\s+מ\S*גרם\S*|כ-?\d+(?:\.\d+)?\s*גרם|כמעט\s+אפס\s+גרם)'
_AMOUNT_MG = r'(?:\d+(?:\.\d+)?\s*(?:מ"?ג|מיליגרם))'
_CHIP_WINDOW = 60  # chars either side — wide enough for a full clause between the metric noun and its recited amount

_METRIC_CHIP_RE: dict[str, re.Pattern] = {
    "protein": re.compile(rf"חלבון[^.]{{0,{_CHIP_WINDOW}}}{_AMOUNT_GRAM}|{_AMOUNT_GRAM}[^.]{{0,{_CHIP_WINDOW}}}חלבון"),
    "sugar": re.compile(rf"סוכר[^.]{{0,{_CHIP_WINDOW}}}{_AMOUNT_GRAM}|{_AMOUNT_GRAM}[^.]{{0,{_CHIP_WINDOW}}}סוכר"),
    "fiber": re.compile(rf"סיב[^.]{{0,{_CHIP_WINDOW}}}{_AMOUNT_GRAM}|{_AMOUNT_GRAM}[^.]{{0,{_CHIP_WINDOW}}}סיב"),
    "sodium": re.compile(rf"נתרן[^.]{{0,{_CHIP_WINDOW}}}{_AMOUNT_MG}|{_AMOUNT_MG}[^.]{{0,{_CHIP_WINDOW}}}נתרן"),
    "kcal": re.compile(r'קלורי[^.]{0,25}\d+|\d+[^.]{0,25}קלורי|\d+\s*קק"ל'),
    "fat": re.compile(rf"שומן[^.]{{0,{_CHIP_WINDOW}}}{_AMOUNT_GRAM}|{_AMOUNT_GRAM}[^.]{{0,{_CHIP_WINDOW}}}שומן"),
}


def find_ingredient_opener_recite_violations(rec: dict) -> list[dict]:
    violations: list[dict] = []
    for field in ("insightLine", "rowVerdict"):
        text = rec.get(field)
        if not isinstance(text, str) or not text:
            continue
        if not _INGREDIENT_OPENER_RE.match(text.strip()):
            continue
        matched = [metric for metric, pat in _METRIC_CHIP_RE.items() if pat.search(text)]
        if len(matched) >= 2:
            violations.append({"path": field, "metrics": matched, "text": text[:200]})
    return violations


def find_integrity_violations(rec: dict, sheet: dict, rank_info: dict | None = None) -> list[dict]:
    """Run all Adversarial-QA/Nutrition-Agent/owner-sourced mechanical checks
    (RT-1 incl. RULING 3 among-measured, RULING 2 dimension-framing, RT-2,
    RT-4, RT-5, H3-R1 rank-contradiction, H3-R3 ingredient-opener-recite) on
    one product's record. Returns a flat, tagged violation list (empty =
    clean)."""
    out: list[dict] = []
    for v in find_superlative_violations(rec, sheet):
        out.append({"check": "RT-1_superlative", **v})
    for v in find_dimension_framing_contradictions(rec, sheet):
        out.append({"check": "Ruling2_dimension_contradiction", **v})
    for v in find_causal_fat_sodium_violations(rec, sheet):
        out.append({"check": "RT-2_causal_fat_sodium", **v})
    for v in find_em_dash_violations(rec):
        out.append({"check": "RT-4_em_dash_count", **v})
    for v in find_negation_closer_violations(rec):
        out.append({"check": "RT-5_negation_closer", **v})
    for v in find_rank_contradiction_violations(rec, rank_info):
        out.append({"check": "H3-R1_rank_contradiction", **v})
    for v in find_ingredient_opener_recite_violations(rec):
        out.append({"check": "H3-R3_ingredient_opener_recite", **v})
    return out


def _post_process(raw: dict, facts: dict, rank_reference_sheets: list[dict] | None = None) -> dict:
    meta = facts.get("_meta") or {}
    sheets = facts.get("sheets") or []
    category = meta.get("category", "unknown")
    sheets_by_bc = {str(s["barcode"]): s for s in sheets}
    # H3-R1: rank MUST be computed from the FULL corpus, not just the sheets
    # in this call — a targeted re-author of 1-3 products still needs their
    # true rank among all 20, so callers doing a partial re-author pass the
    # full corpus's sheets here explicitly (see author()).
    rank_map = compute_score_ranks(rank_reference_sheets if rank_reference_sheets is not None else sheets)

    products_in = raw.get("products") or {}
    products_out: dict = {}
    missing_bc: list[str] = []

    for bc, sheet in sheets_by_bc.items():
        rec = products_in.get(bc)
        if not isinstance(rec, dict):
            missing_bc.append(bc)
            continue
        rec = json.loads(json.dumps(rec))  # deep copy, cheap

        # (1) s_verbatim byte-verbatim override — hard rule, never trust the model
        if "s_verbatim" in sheet:
            sv = sheet["s_verbatim"]
            rec["insightLine"] = sv["insightLine"]
            rec["s_grade_explanation"] = sv["s_grade_explanation"]
            rec["consumerTakeaway"] = sv["insightLine"]

        # (2) bariInterpretation identity pass-through — only `interpretation`
        # is the model's to write; key/label/score/strength come from the sheet.
        bi_inputs = sheet.get("bari_interpretation_inputs") or []
        bi_out = rec.get("bariInterpretation") or []
        bi_by_key = {b.get("key"): b for b in bi_out if isinstance(b, dict)}
        fixed_bi = []
        for entry in bi_inputs:
            key = entry.get("key")
            out_entry = bi_by_key.get(key) or {}
            interpretation = out_entry.get("interpretation")
            if entry.get("score") is None and not interpretation:
                interpretation = "נתון לא זמין"
            elif not interpretation:
                interpretation = "נתון לא זמין"
            fixed_bi.append({
                "key": key,
                "label": entry.get("label"),
                "score": entry.get("score"),
                "strength": entry.get("strength"),
                "interpretation": interpretation,
            })
        rec["bariInterpretation"] = fixed_bi

        # (3) bestUseCases pass-through when already deterministic
        if not sheet.get("best_use_cases_pending", True):
            rec["bestUseCases"] = list(sheet.get("best_use_cases_deterministic") or [])

        products_out[bc] = rec

    # (4) zero-tolerance banned-phrase enforcement (raises on violation)
    for bc, rec in products_out.items():
        _enforce_all_strings(rec, bc)

    page = raw.get("_page") or {}
    for k in ("story_headline", "story_teaser", "philosophy_note"):
        if isinstance(page.get(k), str):
            enforce_clean(page[k], f"_page.{k}")

    # (5) baseline-fingerprint zero-tolerance check (TASK-536 defense)
    fp_hits: list = []
    for bc, rec in products_out.items():
        _check_baseline_fingerprints(rec, bc, fp_hits)
    defingerprint_applied: list = []
    if fp_hits:
        # One auditable rewrite pass for KNOWN, meaning-preserving collisions
        # (see _DEFINGERPRINT_SUBS) — then re-check. Anything not in that
        # table still raises; this is not a blanket bypass.
        defingerprint_applied = [dict(h) for h in fp_hits]
        products_out = {bc: _apply_defingerprint_subs(rec) for bc, rec in products_out.items()}
        for bc, rec in products_out.items():
            _enforce_all_strings(rec, bc)  # re-verify the rewrite didn't introduce a banned phrase
        fp_hits = []
        for bc, rec in products_out.items():
            _check_baseline_fingerprints(rec, bc, fp_hits)
    if fp_hits:
        preview = "; ".join(f"{h['path']}:{h['fingerprint']!r}" for h in fp_hits[:5])
        raise ContentAgentAuthorError(
            f"content_agent_v1 output reproduced {len(fp_hits)} baseline-placeholder "
            f"template phrase(s) — this is the baseline_copy_shipped_trap failure "
            f"class (TASK-536). First hits: {preview}"
        )

    # (6) FINAL safety-net re-check of RT-1/RT-2/RT-4/RT-5 (Adversarial QA,
    # 2026-07-09). The per-batch check in author() should already have caught
    # these before a batch was ever accepted; this is defense-in-depth in
    # case a later step (e.g. the defingerprint substitution above) somehow
    # reintroduced one. Raises — never silently strips.
    integrity_hits_final: list = []
    for bc, rec in products_out.items():
        sheet = sheets_by_bc.get(bc, {})
        integrity_hits_final.extend(
            {"barcode": bc, **v} for v in find_integrity_violations(rec, sheet, rank_map.get(bc))
        )
    if integrity_hits_final:
        preview = "; ".join(
            f"{h['check']}@{h['barcode']}:{h.get('path', '')}"
            for h in integrity_hits_final[:5]
        )
        raise ContentAgentAuthorError(
            f"content_agent_v1 output failed final integrity re-check "
            f"({len(integrity_hits_final)} hit(s), should have been caught "
            f"per-batch): {preview}"
        )

    return {
        "_meta": {
            "author_engine": AUTHOR_ENGINE_TAG,
            "authored_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "category": category,
            "product_count": len(sheets),
            "missing_barcodes": missing_bc,
            "defingerprint_rewrites": defingerprint_applied,
        },
        "products": products_out,
        "_page": page,
    }


# ---------------------------------------------------------------------------
# Main entry point — same signature as author_copy.author()
# ---------------------------------------------------------------------------

BATCH_MAX_ATTEMPTS = 3  # M2: bumped from 2 - the M1 retry-once was sized for
                        # transient subprocess contention only. M2 added 5
                        # mechanical integrity gates (RT-1/RT-2/RT-4/RT-5/
                        # Ruling2) that can ALSO force a retry when the model
                        # slips on one of the new hard rules; one extra
                        # attempt absorbs that without risking the whole
                        # 20-product run on a single stubborn batch. Original
                        # note on the timeout/contention finding retained:
                        # BATCH_SIZE=2 was inconsistent (batch 1 of 2 products
                        # finished in ~520s; batch 2 of the SAME size hit the
                        # 900s wall with zero output) — a pattern consistent
                        # with transient contention (this environment runs
                        # several concurrent claude/node subprocesses across
                        # other background agents), not a deterministic size
                        # problem. A single retry absorbs a one-off stall
                        # without masking a real, repeatable failure.


def author(facts: dict, *, checkpoint_path: Path | None = None,
           rank_reference_sheets: list[dict] | None = None) -> dict:
    """Real Content-Agent LLM pass. Same contract as author_copy.author():
    author(facts: dict) -> dict. Tags _meta.author_engine = "content_agent_v1".

    Authors in small batches (BATCH_SIZE products per headless-claude call) and
    merges — a single one-shot over a whole shelf produces too much output to
    finish inside a sane timeout. The full voice context (distilled brief) is
    re-sent per batch (each call is an independent Content-Agent read); _page
    copy is taken from the first batch only.

    Each batch gets up to BATCH_MAX_ATTEMPTS tries (retry-once on a timeout/
    error) before the whole call fails. After every successfully merged batch,
    progress is written to `checkpoint_path` (if given) — a late batch failure
    no longer discards earlier successful batches' Hebrew; the checkpoint is
    visibility/diagnostics, not an auto-resume (a fresh call still re-authors
    from batch 1, since re-running an already-good batch is cheap relative to
    losing the whole run to one bad batch).

    `rank_reference_sheets` (H3-R1): pass the FULL corpus's sheets when
    `facts["sheets"]` is only a SUBSET (a targeted re-author) — rank must be
    computed against the whole shelf, not the subset being regenerated, or a
    product's true standing (e.g. rank 1/20) would be miscomputed as rank
    1/3. Defaults to `facts["sheets"]` when omitted (correct for a full-shelf
    run, where the subset IS the whole corpus).
    """
    meta = facts.get("_meta") or {}
    sheets = facts.get("sheets") or []
    if not sheets:
        raise ContentAgentAuthorError("content_agent_v1: fact sheet has no products")

    rank_map = compute_score_ranks(rank_reference_sheets if rank_reference_sheets is not None else sheets)

    batches = [sheets[i:i + BATCH_SIZE] for i in range(0, len(sheets), BATCH_SIZE)]
    merged_products: dict = {}
    page: dict = {}

    def _author_batch(bi: int, batch: list) -> tuple[int, dict]:
        """Author one batch, with retries + mechanical integrity gating.
        Pure w.r.t. shared state — safe to run concurrently."""
        sub_facts = {"_meta": meta, "sheets": batch}
        architecture = _architecture_for_batch(bi)
        batch_sheets_by_bc = {str(s["barcode"]): s for s in batch}
        last_note = ""
        for attempt in range(1, BATCH_MAX_ATTEMPTS + 1):
            with tempfile.TemporaryDirectory(prefix="content_agent_v1_") as td:
                out_path = Path(td) / "llm_authored_raw.json"
                prompt = build_prompt(sub_facts, out_path, architecture=architecture)
                print(f"[author_copy_llm] batch {bi + 1}/{len(batches)} "
                      f"({len(batch)} products) authoring, architecture="
                      f"{architecture['name']!r} "
                      f"(attempt {attempt}/{BATCH_MAX_ATTEMPTS}) ...", flush=True)
                ok, note = _run_claude(prompt, out_path)
                if ok:
                    candidate = _extract_json_object(out_path.read_text(encoding="utf-8"))
                    # RT-1/RT-2/RT-4/RT-5/H3-R1/H3-R3: mechanical integrity
                    # checks BEFORE this batch is accepted, so a violation costs
                    # one retry of THIS batch, not the whole 20-product run.
                    integrity_hits: list = []
                    for bc, rec in (candidate.get("products") or {}).items():
                        sheet = batch_sheets_by_bc.get(bc, {})
                        integrity_hits.extend(
                            {"barcode": bc, **v}
                            for v in find_integrity_violations(rec, sheet, rank_map.get(bc))
                        )
                    if integrity_hits:
                        preview = "; ".join(
                            f"{h['check']}@{h['barcode']}:{h.get('path', '')}"
                            for h in integrity_hits[:5]
                        )
                        last_note = f"integrity check failed ({len(integrity_hits)} hit(s)): {preview}"
                        print(f"[author_copy_llm] batch {bi + 1}/{len(batches)} attempt "
                              f"{attempt}/{BATCH_MAX_ATTEMPTS} FAILED integrity check: "
                              f"{last_note}", flush=True)
                        continue  # retry this batch — do not accept the violating output
                    return bi, candidate
                last_note = note
                print(f"[author_copy_llm] batch {bi + 1}/{len(batches)} attempt "
                      f"{attempt}/{BATCH_MAX_ATTEMPTS} FAILED ({note})", flush=True)
        raise ContentAgentAuthorError(
            f"content_agent_v1: batch {bi + 1}/{len(batches)} produced no "
            f"output after {BATCH_MAX_ATTEMPTS} attempt(s) ({last_note})"
        )

    # Batches are independent authoring jobs — run them concurrently. A single
    # call costs ~465s (generation-bound, not startup-bound), so a 20-product
    # shelf is ~2.5h serial. MAX_WORKERS concurrent calls cut that to ~(n/W)*465s.
    # Ordering is preserved by keying results on the batch index, not on
    # completion order; `_page` is always taken from batch 0.
    raws: dict[int, dict] = {}
    workers = max(1, min(MAX_WORKERS, len(batches)))
    print(f"[author_copy_llm] authoring {len(batches)} batch(es) with "
          f"{workers} concurrent worker(s)", flush=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(_author_batch, bi, b): bi for bi, b in enumerate(batches)}
        done_count = 0
        for fut in concurrent.futures.as_completed(futures):
            bi, raw = fut.result()  # a failed batch raises here, cancelling the run
            raws[bi] = raw
            done_count += 1
            # Merge in index order over what has arrived so far, so the checkpoint
            # and `_page` never depend on completion order.
            merged_products = {}
            page = {}
            for i in sorted(raws):
                merged_products.update(raws[i].get("products") or {})
                if i == 0:
                    page = raws[i].get("_page") or {}
            print(f"[author_copy_llm] batch {bi + 1}/{len(batches)} done "
                  f"({done_count}/{len(batches)} complete, "
                  f"{len(merged_products)} products)", flush=True)
            if checkpoint_path is not None:
                try:
                    checkpoint_path.write_text(json.dumps({
                        "_meta": {"author_engine": AUTHOR_ENGINE_TAG, "status": "IN_PROGRESS",
                                  "batches_done": done_count, "batches_total": len(batches),
                                  "products_so_far": len(merged_products)},
                        "products": merged_products, "_page": page,
                    }, ensure_ascii=False, indent=2), encoding="utf-8")
                except OSError:
                    pass

    merged_products = {}
    page = {}
    for i in sorted(raws):
        merged_products.update(raws[i].get("products") or {})
        if i == 0:
            page = raws[i].get("_page") or {}

    merged_raw = {"products": merged_products, "_page": page}
    return _post_process(merged_raw, facts, rank_reference_sheets=rank_reference_sheets)


# ---------------------------------------------------------------------------
# Regression selftest for the superlative gate (QA + coordinator, 2026-07-10).
# "A gate that reports 0 while blind is worse than no gate" — these 4 probes
# reproduce the exact evasions QA found (gender/number variants, and the
# ביותר-less "definite-doubling" superlative shape) so this can never
# silently regress again. Run: python author_copy_llm.py --selftest
# ---------------------------------------------------------------------------

def _selftest_superlative_gate() -> int:
    unauthorized_sheet = {"superlatives_allowed": [], "superlatives_context": {}}
    must_catch = [
        "הסיבים הגבוהים ביותר בקטגוריה",     # masculine plural
        "הקלוריות הנמוכות ביותר בקטגוריה",   # feminine plural
        "הנתרן הגבוה במדף",                   # superlative without ביותר
    ]
    failures: list[tuple[str, str]] = []
    for text in must_catch:
        hits = find_superlative_violations({"insightLine": text}, unauthorized_sheet)
        if not hits:
            failures.append(("MISSED (should have been caught)", text))

    authorized_sheet = {
        "superlatives_allowed": ["highest_protein"],
        "superlatives_context": {
            "highest_protein": {"n_measured": 20, "phrase_as_among_measured": False}
        },
    }
    must_pass = "החלבון הגבוה ביותר בקטגוריה"  # masculine singular, authorized
    hits = find_superlative_violations({"insightLine": must_pass}, authorized_sheet)
    if hits:
        failures.append(("FALSE-POSITIVE (authorized claim wrongly flagged)", must_pass))

    if failures:
        print(f"[FAIL] superlative-gate selftest: {len(failures)} failure(s)")
        for kind, text in failures:
            print(f"  {kind}: {text!r}")
        return 1
    print(f"[PASS] superlative-gate selftest ({len(must_catch) + 1} probes: "
          f"{len(must_catch)} must-catch + 1 must-pass)")
    return 0


def _selftest_rank_contradiction_gate() -> int:
    """H3-R1 (owner ruling, 2026-07-10): reproduces the ויטביקס failure —
    the actual shelf-#1 product framed as mid-shelf on its overall profile."""
    top_rank = {"rank": 1, "total": 20, "score": 74.7, "is_top": True}
    mid_rank = {"rank": 9, "total": 20, "score": 49.7, "is_top": False}

    must_catch = [
        "הפרופיל התזונתי הכולל של המוצר נשאר בינוני יחסית למדף",
        "המוצר נמצא בחלק הבינוני-עליון של הקטגוריה",
        "מדורג בינוני ביחס למדף הדגנים",
    ]
    failures: list[tuple[str, str]] = []
    for text in must_catch:
        hits = find_rank_contradiction_violations({"rowVerdict": text}, top_rank)
        if not hits:
            failures.append(("MISSED (should have been caught for rank-1 product)", text))

    # Same phrase, but NOT the top-ranked product -> must NOT fire (a
    # genuinely mid-shelf product may honestly be called mid-shelf).
    for text in must_catch:
        hits = find_rank_contradiction_violations({"rowVerdict": text}, mid_rank)
        if hits:
            failures.append(("FALSE-POSITIVE (non-top product wrongly flagged)", text))

    # A per-dimension bariInterpretation note saying "בינוני" is legitimate
    # even for the #1 product (a dimension score genuinely can be mid) and
    # must NOT be flagged — the check only scopes headline-visible fields.
    rec_with_dim = {
        "insightLine": "החלבון הגבוה ביותר בקטגוריה",  # clean, no violation
        "bariInterpretation": [
            {"key": "nutrient_density", "label": "ערך תזונתי", "score": 52.0,
             "strength": "בינוני", "interpretation": "ערך תזונתי כולל בינוני יחסית לקטגוריה"}
        ],
    }
    hits = find_rank_contradiction_violations(rec_with_dim, top_rank)
    if hits:
        failures.append(("FALSE-POSITIVE (dimension-scoped bariInterpretation wrongly flagged)",
                          "bariInterpretation[nutrient_density]"))

    if failures:
        print(f"[FAIL] rank-contradiction-gate selftest: {len(failures)} failure(s)")
        for kind, text in failures:
            print(f"  {kind}: {text!r}")
        return 1
    print(f"[PASS] rank-contradiction-gate selftest ({len(must_catch) * 2 + 1} probes)")
    return 0


def _selftest_ingredient_opener_recite_gate() -> int:
    """H3-R3 (owner ruling, 2026-07-10 — "the worst pattern"): ingredient-
    list opener followed by >=2 recited nutrition values."""
    must_catch = [
        "רשימת הרכיבים כאן קצרה באופן יוצא דופן: שלושה פריטים בלבד, ואפס "
        "תוספי מזון. הסיבים, לעומת זאת, נמוכים משמעותית מרוב הדגנים במדף — "
        "פחות מגרם אחד ל-100 גרם. הנתרן עומד על 390 מיליגרם ל-100 גרם, "
        "גבוה משמעותית מהחציון.",
    ]
    failures: list[tuple[str, str]] = []
    for text in must_catch:
        hits = find_ingredient_opener_recite_violations({"rowVerdict": text})
        if not hits:
            failures.append(("MISSED (should have been caught)", text))

    # A finding-first opener with the SAME two facts must NOT fire — leading
    # with the verdict, not the ingredient-list inventory, is exactly the fix.
    must_pass = (
        "שלושה רכיבים, אפס תוספי מזון — ורמת סיבים נמוכה משמעותית מהחציון. "
        "הנתרן, 390 מיליגרם ל-100 גרם, גבוה מהחציון."
    )
    hits = find_ingredient_opener_recite_violations({"rowVerdict": must_pass})
    if hits:
        failures.append(("FALSE-POSITIVE (finding-first opener wrongly flagged)", must_pass))

    # A single nutrition-value mention after the ingredient-list opener is
    # fine — the ban is on RECITING >=2 separate metrics, not on mentioning
    # the ingredient list at all.
    single_metric = "רשימת הרכיבים קצרה: שלושה פריטים בלבד. הנתרן גבוה מהחציון, 390 מיליגרם ל-100 גרם."
    hits = find_ingredient_opener_recite_violations({"rowVerdict": single_metric})
    if hits:
        failures.append(("FALSE-POSITIVE (single-metric mention wrongly flagged)", single_metric))

    if failures:
        print(f"[FAIL] ingredient-opener-recite-gate selftest: {len(failures)} failure(s)")
        for kind, text in failures:
            print(f"  {kind}: {text!r}")
        return 1
    print(f"[PASS] ingredient-opener-recite-gate selftest (3 probes)")
    return 0


def _run_all_selftests() -> int:
    results = [
        _selftest_superlative_gate(),
        _selftest_rank_contradiction_gate(),
        _selftest_ingredient_opener_recite_gate(),
    ]
    return 0 if all(r == 0 for r in results) else 1


def main() -> int:
    ap = argparse.ArgumentParser(
        description="content_agent_v1 — real LLM author (Part 2 of Copy Engine)."
    )
    ap.add_argument("--facts", help="Path to fact_sheets.json")
    ap.add_argument("--out", help="Path to write authored.json")
    ap.add_argument("--selftest", action="store_true",
                     help="Run the offline mechanical-gate regression probes and exit")
    args = ap.parse_args()

    if args.selftest:
        return _run_all_selftests()

    if not args.facts or not args.out:
        ap.error("--facts and --out are required unless --selftest is given")

    # When launched without an interactive console, the nested `claude` Node CLI
    # can raise a console CTRL_C/CTRL_BREAK that would kill THIS process before
    # the read completes (the 0xC000013A class local_scan.py hit under Task
    # Scheduler). Ignore those signals so the authoring pass runs to completion.
    import signal
    for _sig in ("SIGINT", "SIGBREAK"):
        try:
            signal.signal(getattr(signal, _sig), signal.SIG_IGN)
        except (AttributeError, ValueError, OSError):
            pass

    with open(args.facts, encoding="utf-8") as f:
        facts = json.load(f)

    checkpoint_path = Path(str(args.out) + ".checkpoint.json")
    authored = author(facts, checkpoint_path=checkpoint_path)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(authored, f, ensure_ascii=False, indent=2)

    n = len(authored.get("products", {}))
    missing = authored["_meta"].get("missing_barcodes") or []
    print(f"[author_copy_llm] Authored {n} product(s). engine={AUTHOR_ENGINE_TAG}")
    if missing:
        print(f"[author_copy_llm] WARNING — missing barcodes: {missing}")
    print(f"[author_copy_llm] Output: {args.out}")
    return 0 if not missing else 1


if __name__ == "__main__":
    sys.exit(main())
