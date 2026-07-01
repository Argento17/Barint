# 11 — The Naturalness Gate (Tom / Bari Hebrew) · v1.0

**Project Tom's Voice (TASK-374), Phase 1.** The gate that finally blocks mediocre
Hebrew — the defect no existing gate catches (`10_translationese_taxonomy.md`).
It is **two-axis** (owner ruling 2026-06-22, file 10 §D):

- **F1 — Naturalness:** is this native connected Hebrew, free of translationese
  (the T1–T7 tells)?
- **F2 — Stance/substance:** does it actually say something — a clear verdict, not
  neutral-bland hedging? ("calm" is a trap; the AI over-corrects into mush.)

**A line is excellent only when it is F1-clean AND F2-clean.** Calm-but-empty fails
exactly as hard as punchy-but-calqued. Target register = *opinionated substance in
natural connected Hebrew.*

---

## Architecture — two layers

```
Layer 1 (cheap, deterministic, offline):  integrations/clients/naturalness_gate.py
   → flags the mechanical T1–T7 tells. HIGH = block; MEDIUM = route to judge.
   → run by the CONTENT AGENT in its pre-return self-check (new gate 5.6).

Layer 2 (the LLM judge — F1 nuance + F2 stance):  this rubric + prompt
   → run on an INDEPENDENT lane (the Adversarial QA Agent, Track C — it did NOT
     author the copy, which satisfies the independence requirement for free;
     a C3 fresh-eyes pass is the fallback when QA is the author's lane).
   → scores F1 and F2 1–5, names failing lines, proposes in-voice rewrites.
```

**Why independence matters:** the agent that wrote the copy cannot judge its own
naturalness — that is the self-assessment hole that let mediocre Hebrew ship. The
judge must be a different context/lane. This reuses the existing two-gate
([[content_signoff_hard_rule]]); it is not new infrastructure.

---

## The judge prompt (paste to the independent lane)

> אתה עורך עברית ישראלי, חד ובלתי מתפשר, שאכפת לו רק משני דברים: (1) שהטקסט נשמע
> עברית טבעית וזורמת — לא תרגומית, לא מכנית; (2) שהטקסט אומר משהו — יש בו עמדה
> וקביעה ברורה, לא ניטרליות מימימית שלא אומרת כלום. אתה לא מתקן דקדוק ולא מחפש
> הדלפות — רק טבעיות ועמדה.
>
> לכל פסקה תן שני ציונים 1–5:
> - **F1 טבעיות:** 5 = עברית ילידית זורמת; 1 = תרגומית/מכנית. הורד ציון על:
>   מבנה "X, לא Y" כסוגר, "X לא תמיד אומר Y", "גם" תלוי בסוף משפט, מטאפורות
>   מתורגמות ("המחיר שלו ברור", "נושא את החלבון"), האנגלזה (נומינליזציה פסיבית
>   "הבחירה שנעשתה היא…"), מילים לועזיות לא מתורגמות ("מילק"), שימוש יתר ב-"(!)".
> - **F2 עמדה:** 5 = יש קביעה/שיפוט ברור ומבוסס; 1 = ניטרלי, מגמגם, "לא אומר כלום".
>   הורד ציון על: רק הסתייגויות בלי קביעה, היעדר ורדיקט, טקסט שיכול להתאים לכל מוצר.
>
> לכל ציון מתחת ל-4: צטט את השורה הבעייתית, אמור איזה כשל (T1–T7 או "ניטרלי
> מדי"), והצע ניסוח חלופי בקול בארי — חיבורים טבעיים (יחד עם זאת / כי / מדובר ב…),
> עמדה חדה אך לא מבוצעת בכוח, ועצירה נקייה כשנגמר. אל תכתוב "רגוע" — כתוב "חד אבל
> טבעי". החזר JSON: {f1, f2, failing_lines:[{line, tell, rewrite}], verdict}.

---

## Pass / fail

| Result | Condition |
|---|---|
| **PASS** | F1 ≥ 4 AND F2 ≥ 4 AND Layer-1 HIGH-clean |
| **REJECT → refiner** | F1 ≤ 3 OR F2 ≤ 3 OR any Layer-1 HIGH flag |
| **REFINER** | rewrite the failing lines using the judge's in-voice suggestions, then re-run BOTH layers. Max 2 refine cycles before escalating to human edit. |

The refiner is the *same* draft lane fixing its lines from the judge's notes — the
judge stays independent. This is the Critic→Refiner loop, gated.

---

## Calibration & acceptance test (TASK-374)

The gate is calibrated against the owner's real examples:
- **Must REJECT** every owner-flagged line (`10_translationese_taxonomy.md` T1–T7;
  the 12 live examples). Layer 1 already does this for the mechanical tells
  (`python -m integrations.clients.naturalness_gate` → PASS, 7/7 flagged lines HIGH).
- **Must PASS** every owner gold line (`phase0_owner_gold_examples.md`, 8 rewrites)
  — including the guards: `לייט זה לא.` (earned fragment), mid-sentence `גם`, and
  the repaired `מוצר נקי הוא לא בהכרח מוצר חזק`.
- **F2 negative test (to add):** a calm-but-empty paragraph (no verdict, hedge-only)
  must REJECT on F2 even when F1 is clean — the "calm trap" guard.

Whenever the owner supplies new flagged/gold lines, add them here and re-run; the
gate is not calibrated until it flags every flagged line and passes every gold line.

---

## Integration into the gate chain

Updated order (extends `5_banned_phrases_and_claims.md` §3 and `7_voice_match_gate.md`):
```
1 Claim scan · 2 Leakage (hebrew_readability) · 3 Tone (HebEMO) · 4 Form (Nakdan) ·
5 Grammar (hebrew_grammar_gate) · 5.6 Naturalness Layer 1 (naturalness_gate.py) ·
6 Voice-match gate (file 7) · 7 Naturalness Layer 2 (LLM judge, independent lane) ·
8 Tom-edit / harvest loop (file 8)
```
A draft must pass all of them. Layer 1 (5.6) runs in the Content Agent self-check;
Layer 2 (7) runs in the Adversarial QA Track-C review before go-live.
