# Return: P392

> ⚠️ **STATUS: RETURNED-UNVERIFIED.** Raw agent output captured by the router.
> Nothing here is accepted, closed, or true until the ORCHESTRATOR verifies every
> claim against artifacts (Return Contract v1). The router never closes.
> (Law added after P35 was face-value-closed with contradictions inside it.)

| Field | Value |
|---|---|
| Prompt file | `tasks\prompts\P392_juices_decite_c3.md` |
| Model | `openai/gpt-5.5` |
| Started | 2026-06-24T09:40:56.285631+00:00 |
| Finished | 2026-06-24T09:42:35.632805+00:00 |
| Exit code | 0 |

---

## Output

```
**(a) Intro Verdict**
Strong enough and materially better than generic. It gives the reader the category trick in one pass: same-looking shelf, different legal/product meanings, then Bari’s question.

Sharper line 1 option:
> המדף נראה אחיד: פרי על האריזה, צבעים טבעיים, שמות מרגיעים. בפועל, “מיץ”, “נקטר” ו“משקה פירות” הם שלוש רמות שונות לגמרי של פרי, מים ותוספות.

Keep line 3. It is honest and useful: 100% juice is not demonized, but the liquid-sugar limitation is clear.

**(b) New False / Risky Claims**
1. **jc-019: “ממתיקים — פרוקטוז, סוכרלוז”**
Evidence issue: fructose is a sugar/caloric sweetener, not usually read as “ממתיק” in the same category as sucralose. Current phrasing blurs “sweeteners” and “sugar replacement.”
Fix:
> הסוכר הלבן הוחלף במתיקות מסוג אחר: פרוקטוז, סוכרלוז ומסמיך.

2. **jc-021: “הגבוה ביותר בין מוצרי ה-D”**
Confirmed true from table: jc-021 fruit 40%, higher than jc-022 ~38%, jc-017/019/024 25%, jc-020 17%, jc-018 2%. Safe.

3. **jc-020: “17% הוא כמעט פי עשרה מקריסטל מיץ ענבים”**
Numerically defensible but rhetorically a little too cute: 17% vs 2% = 8.5x, so “כמעט פי עשרה” is acceptable but slightly loose.
Safer fix:
> 17% הוא פי כמה מקריסטל מיץ ענבים — אבל שניהם רחוקים מ-100% סחוט.

4. **jc-024: “שלושה רבעי הפחית מים וסוכר”**
Risky precision. If 25% is mango puree, the remaining 75% is not necessarily only water + sugar; could include acids/stabilizers/etc. The table only supports “not fruit.”
Fix:
> 25% מחית מנגו מרכז — כלומר רוב הפחית אינו פרי.

5. **jc-026: “הסוכר בעיקר מהסוכר שנוסף”**
Likely true from ingredient order: 9% fruit, sugar second. Still, “בעיקר” is an inferred proportion unless label math confirms it.
Safer fix:
> הסוכר הלבן הוא מקור מרכזי למתיקות, לא רק הפרי.

6. **jc-018: “הצבע הכהה לא בא מהענבים”**
Directionally fair because 2% grapes + caramel color, but absolute wording is too strong. Some color can come from grapes.
Fix:
> הצבע הכהה לא נשען על הענבים בלבד.

7. **jc-025: “חמישה חומרי עיבוד נוספים”**
Cannot verify from provided table, which only says “NO orange” and fruit percentages. If label supports it, fine; from evidence supplied, this is an unsupported count.
Fix if not verified:
> ועוד חומרי עיבוד נוספים.

**(c) Residual Numbers To Drop**
Confirmed drops:
- jc-011: drop `44 קלוריות`.
- jc-017: drop or correct `60 נקודות`; correct gap from 85 to 49.1 is about 36.
- jc-024: drop `(35.4)` from prose.
- jc-027: drop `28.5` from prose.

Additional numeric recitation to consider:
- jc-006: “הגבוה ביותר בין שישת מוצרי ה-A” is okay because it interprets the visible sugar bar rather than merely restating `12.6`.
- jc-020: “17% ... פי עשרה” is insight, not panel recitation, but soften as above.
- jc-021/jc-022/jc-024/jc-025/jc-026/jc-027 fruit percentages should stay. In this page, fruit percentage is the core hidden fact, unlike sugar which is already visualized.

**(d) A-Framing Check**
A-products are framed correctly overall. The copy says: fruit-only, no added sugar, A is earned, but juice still has the category limitation of liquid sugar without fiber. That is the right balance.

Small tone issue:
- jc-005: “רימון מתוק מטבעו” is fine, but with missing sugar label it should avoid sounding like a hidden estimate. Better:
> הסוכר לא צוין, אבל רכיב הסוכר היחיד האפשרי כאן הוא הפרי עצמו.

- jc-011: “הדרים קלות-יחסית בסוכר טבעי” is awkward and partly inferential. Since sugar is missing, avoid comparative sugar language.
Fix:
> קלמנטינות, ורק קלמנטינות. A נשען על רשימת רכיבים קצרה וברורה: פרי בלבד.

**(e) Hebrew / Naturalness**
Stiff or calqued phrases:
- “חמוציות מרכז” should be “חמוציות מרוכזות” or “רכז חמוציות.”
- “מחית מנגו מרכז” should be “מחית מנגו מרוכזת.”
- “כל הפרי מרכז” should be “כל הפרי מרוכז” or “ממקור רכז.”
- “שלושה רבעי הפחית מים וסוכר” is unnatural and overprecise.
- “עצרנו כאן” is nice but slightly colloquial; acceptable if page voice allows it.
- “חולק A עם חמישה אחרים” is understandable but stiff. Better: “נמצא באותה קבוצת A עם עוד חמישה מוצרים מאותה פילוסופיה.”

**(f) Ship / Fix-First**
Fix-first.

Required before ship:
- Correct/drop jc-017 false 60-point gap.
- Remove jc-011 kcal sentence.
- Remove score citations in jc-024 and jc-027.
- Soften jc-024 “three quarters water and sugar.”
- Fix “מרכז” grammar across the D/E rows.
- Verify or remove jc-025 “חמישה חומרי עיבוד נוספים.”

After those, the copy is shippable.

--- SSE Events ---
  server.connected: {}
  session.created: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "info": {"id": "ses_106fee694ffePN0RGW3bPUzoY8", "slug": "clever-cactus", "projectID": "e7f90f8a5abbaca924c7d1983e3ba702c9bbf643", "directory": "C:\\Bar
  session.next.agent.switched: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9011ee9001t3e2Oh3airw5WG", "timestamp": "2026-06-24T09:41:00.777Z", "agent": "build"}
  message.updated: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "info": {"id": "msg_ef9011ee90018CdRGqVgGLT0rm", "role": "user", "sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "time": {"created": 1782294060777}, "age
  message.part.updated: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "part": {"type": "text", "text": "You are the independent challenger (ChatGPT). Advice/critique ONLY \u2014 never build, never close. The juices compari
  session.updated: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "info": {"id": "ses_106fee694ffePN0RGW3bPUzoY8", "slug": "clever-cactus", "projectID": "e7f90f8a5abbaca924c7d1983e3ba702c9bbf643", "directory": "C:\\Bar
  session.status: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "status": {"type": "busy"}}
  message.updated: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "info": {"id": "msg_ef9012088001tjRMc1ji2CuCQG", "parentID": "msg_ef9011ee90018CdRGqVgGLT0rm", "role": "assistant", "mode": "build", "agent": "build", "
  session.updated: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "info": {"id": "ses_106fee694ffePN0RGW3bPUzoY8", "slug": "clever-cactus", "projectID": "e7f90f8a5abbaca924c7d1983e3ba702c9bbf643", "directory": "C:\\Bar
  session.diff: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "diff": []}
  message.updated: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "info": {"role": "user", "time": {"created": 1782294060777}, "agent": "build", "model": {"providerID": "openai", "modelID": "gpt-5.5"}, "id": "msg_ef901
  session.status: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "status": {"type": "busy"}}
  message.part.updated: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "part": {"id": "prt_ef9013513001cRbMzM9JzXAqHc", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "snapshot
  session.updated: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "info": {"id": "ses_106fee694ffePN0RGW3bPUzoY8", "slug": "clever-cactus", "projectID": "e7f90f8a5abbaca924c7d1983e3ba702c9bbf643", "directory": "C:\\Bar
  message.part.updated: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "part": {"id": "prt_ef9013891001yfCS7ytfDIY2z2", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "type": "
  message.part.updated: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "part": {"id": "prt_ef9013891001yfCS7ytfDIY2z2", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "type": "
  message.part.updated: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "part": {"id": "prt_ef90146550010gYuKcgGLqZmIR", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "type": "
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "("}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "a"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ")"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " Intro"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " Verdict"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "**\n"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "Strong"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " enough"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " materially"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " better"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " than"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " generic"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " It"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " gives"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " reader"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " category"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " trick"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " in"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " one"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " pass"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " same"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "-looking"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " shelf"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " different"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " legal"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "/product"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " meanings"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " then"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " Bari"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u2019s"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " question"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "Sharper"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " line"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " option"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ":\n"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ">"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05d4\u05de\u05d3"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05e3"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05e0\u05e8\u05d0\u05d4"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05d0\u05d7"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d9\u05d3"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05e4\u05e8"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d9"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05e2\u05dc"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05d4\u05d0\u05e8"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d9\u05d6\u05d4"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05e6\u05d1\u05e2"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05d8\u05d1\u05e2"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d9\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05e9\u05de"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05de\u05e8"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d2\u05d9\u05e2"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05d1\u05e4"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d5\u05e2\u05dc"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05de"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d9\u05e5"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u201d,"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05e0\u05e7"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d8\u05e8"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05d5"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u201c"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05de\u05e9"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05e7\u05d4"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05e4"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d9\u05e8\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05d4\u05dd"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05e9\u05dc"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d5\u05e9"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05e8"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05de\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05e9\u05d5\u05e0\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05dc\u05d2"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05de\u05e8"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d9"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05e9\u05dc"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05e4\u05e8"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d9"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05de\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d5\u05e1"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05e4\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "Keep"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " line"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "3"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " It"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " honest"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " useful"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "100"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "%"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " juice"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " demon"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "ized"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " liquid"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "-s"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "ugar"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " limitation"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " clear"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "("}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "b"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ")"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " New"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " False"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " /"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " Risk"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "y"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " Claims"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "**\n"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "jc"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "019"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05de"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05de\u05ea"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d9\u05e7\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u2014"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05e4\u05e8"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d5\u05e7\u05d8"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d5\u05d6"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05e1"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d5\u05db\u05e8"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05dc"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d5\u05d6"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "**\n"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "Evidence"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " issue"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " fruct"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "ose"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " sugar"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "/cal"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "oric"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " sweet"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "ener"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " usually"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " read"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " as"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05de"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05de\u05ea"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d9\u05e7"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " in"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " same"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " category"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " as"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " su"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "cr"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "al"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "ose"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " Current"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " phr"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "asing"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " bl"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "urs"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "sweet"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "eners"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "s"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "ugar"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " replacement"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ".\u201d\n"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "Fix"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ":\n"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ">"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05d4\u05e1"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d5\u05db\u05e8"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05d4\u05dc"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d1\u05df"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05d4"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d5\u05d7"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05dc"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05e3"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05d1\u05de"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05ea"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d9\u05e7\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05de\u05e1\u05d5\u05d2"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05d0\u05d7\u05e8"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05e4\u05e8"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d5\u05e7\u05d8"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d5\u05d6"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05e1"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d5\u05db\u05e8"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05dc"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d5\u05d6"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05d5\u05de"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05e1"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05de"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d9\u05da"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "jc"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "021"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d4"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d2\u05d1"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d5\u05d4"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05d1\u05d9\u05d5\u05ea\u05e8"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05d1\u05d9\u05df"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05de\u05d5\u05e6\u05e8"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d9"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05d4"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "-D"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "**\n"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "Confirmed"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " true"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " from"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " table"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " jc"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "021"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " fruit"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "40"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "%,"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " higher"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " than"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " jc"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "022"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " ~"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "38"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "%,"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " jc"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "017"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "019"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "024"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "25"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "%,"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " jc"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "020"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "17"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "%,"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " jc"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "018"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "%."}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " Safe"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "3"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "jc"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "020"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "17"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "%"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05d4\u05d5\u05d0"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05db\u05de\u05e2\u05d8"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05e4\u05d9"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05e2"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05e9\u05e8\u05d4"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05de\u05e7\u05e8"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d9\u05e1\u05d8"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05dc"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05de"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d9\u05e5"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05e2\u05e0"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d1\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "**\n"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "Numer"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "ically"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " defens"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "ible"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " rhet"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "or"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "ically"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " little"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " too"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " cute"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "17"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "%"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " vs"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "%"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "8"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "5"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "x"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " so"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05db"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05de\u05e2\u05d8"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05e4\u05d9"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05e2"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05e9\u05e8\u05d4"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " acceptable"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " slightly"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " loose"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "Sa"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "fer"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " fix"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ":\n"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ">"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "17"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "%"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05d4\u05d5\u05d0"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05e4\u05d9"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05db\u05de\u05d4"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05de\u05e7\u05e8"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d9\u05e1\u05d8"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05dc"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05de"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d9\u05e5"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05e2\u05e0"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d1\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u2014"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05d0\u05d1\u05dc"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05e9\u05e0"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d9\u05d4\u05dd"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05e8\u05d7"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d5\u05e7\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05de"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "100"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "%"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05e1"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d7"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d5\u05d8"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "4"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "jc"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "024"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05e9\u05dc"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d5\u05e9\u05d4"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05e8"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d1\u05e2"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d9"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05d4\u05e4"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d7"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d9\u05ea"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05de\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05d5\u05e1"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d5\u05db\u05e8"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "**\n"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "Risk"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "y"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " precision"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " If"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "25"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "%"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " mango"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " puree"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " remaining"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "75"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "%"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " necessarily"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " only"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " water"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " +"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " sugar"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ";"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " could"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " include"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " acids"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "/st"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "abil"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "izers"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "/etc"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " The"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " table"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " only"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " supports"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "not"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " fruit"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ".\u201d\n"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "Fix"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ":\n"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ">"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "25"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "%"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05de\u05d7"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d9\u05ea"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05de\u05e0"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d2\u05d5"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05de\u05e8\u05db\u05d6"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u2014"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05db\u05dc\u05d5\u05de\u05e8"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05e8\u05d5\u05d1"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05d4\u05e4"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d7"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d9\u05ea"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05d0\u05d9\u05e0\u05d5"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05e4\u05e8"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d9"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "5"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "jc"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "026"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d4"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05e1"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d5\u05db\u05e8"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05d1\u05e2\u05d9\u05e7\u05e8"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05de\u05d4"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05e1"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d5\u05db\u05e8"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05e9\u05e0"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d5\u05e1\u05e3"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "**\n"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "Lik"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "ely"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " true"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " from"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " ingredient"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " order"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "9"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "%"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " fruit"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " sugar"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " second"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " Still"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d1\u05e2"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d9\u05e7\u05e8"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " an"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " inferred"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " proportion"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " unless"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " label"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " math"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " confirms"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " it"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "Sa"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "fer"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " fix"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ":\n"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ">"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05d4\u05e1"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d5\u05db\u05e8"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05d4\u05dc"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d1\u05df"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05d4\u05d5\u05d0"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05de\u05e7\u05d5\u05e8"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05de\u05e8\u05db\u05d6"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d9"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05dc\u05de"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05ea"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d9\u05e7\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05dc\u05d0"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05e8\u05e7"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05d4\u05e4\u05e8"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d9"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "6"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "jc"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "018"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d4"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05e6"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d1\u05e2"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05d4\u05db"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d4"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d4"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05dc\u05d0"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05d1\u05d0"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05de\u05d4"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05e2\u05e0"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d1\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "**\n"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "Direction"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "ally"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " fair"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " because"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "%"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " grapes"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " +"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " caramel"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " color"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " absolute"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " wording"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " too"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " strong"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " Some"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " color"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " can"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " come"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " from"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " grapes"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "Fix"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ":\n"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ">"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05d4\u05e6"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d1\u05e2"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05d4\u05db"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d4"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d4"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05dc\u05d0"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05e0\u05e9"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05e2\u05df"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05e2\u05dc"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05d4\u05e2\u05e0"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d1\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05d1\u05dc\u05d1\u05d3"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "7"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "jc"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "025"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d7"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05de"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d9\u05e9\u05d4"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05d7\u05d5\u05de\u05e8"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d9"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05e2"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d9\u05d1"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d5\u05d3"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05e0\u05d5\u05e1\u05e4\u05d9\u0
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "**\n"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "Cannot"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " verify"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " from"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " provided"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " table"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " which"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " only"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " says"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "NO"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " orange"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " fruit"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " percentages"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " If"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " label"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " supports"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " it"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " fine"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ";"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " from"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " evidence"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " supplied"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " this"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " an"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " unsupported"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " count"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "Fix"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " if"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " verified"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ":\n"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ">"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05d5\u05e2\u05d5\u05d3"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05d7\u05d5\u05de\u05e8"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d9"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05e2"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d9\u05d1"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d5\u05d3"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05e0\u05d5\u05e1\u05e4\u05d9\u0
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "("}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "c"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ")"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " Resid"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "ual"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " Numbers"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " To"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " Drop"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "**\n"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "Confirmed"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " drops"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ":\n"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " jc"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "011"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " drop"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "44"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05e7\u05dc"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d5\u05e8"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d9\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "`.\n"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " jc"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "017"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " drop"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " or"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " correct"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "60"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05e0\u05e7"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d5\u05d3\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "`;"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " correct"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " gap"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " from"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "85"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "49"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " about"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "36"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " jc"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "024"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " drop"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " `("}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "35"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "4"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ")`"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " from"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " prose"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " jc"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "027"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " drop"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "28"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "5"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "`"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " from"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " prose"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "Additional"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " numeric"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " rec"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "itation"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " consider"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ":\n"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " jc"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "006"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d4"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d2\u05d1"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d5\u05d4"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05d1\u05d9\u05d5\u05ea\u05e8"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05d1\u05d9\u05df"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05e9\u05d9\u05e9"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05ea"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05de\u05d5\u05e6\u05e8"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d9"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05d4"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "-A"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " okay"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " because"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " it"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " interpre"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "ts"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " visible"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " sugar"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " bar"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " rather"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " than"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " merely"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " rest"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "ating"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "12"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "6"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "`.\n"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " jc"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "020"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "17"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "%"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " ..."}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05e4\u05d9"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05e2"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05e9\u05e8\u05d4"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " insight"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " panel"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " rec"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "itation"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " soften"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " as"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " above"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " jc"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "021"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "/j"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "c"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "022"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "/j"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "c"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "024"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "/j"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "c"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "025"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "/j"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "c"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "026"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "/j"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "c"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "027"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " fruit"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " percentages"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " should"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " stay"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " In"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " this"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " page"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " fruit"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " percentage"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " core"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " hidden"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " fact"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " unlike"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " sugar"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " which"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " already"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " visual"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "ized"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "("}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "d"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ")"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " A"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "-Fr"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "aming"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " Check"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "**\n"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "A"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "-products"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " are"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " framed"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " correctly"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " overall"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " The"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " copy"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " says"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " fruit"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "-only"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " no"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " added"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " sugar"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " A"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " earned"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " juice"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " still"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " has"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " category"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " limitation"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " of"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " liquid"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " sugar"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " without"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " fiber"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " That"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " right"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " balance"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "Small"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " tone"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " issue"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ":\n"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " jc"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "005"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05e8"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d9\u05de\u05d5\u05df"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05de\u05ea"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d5\u05e7"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05de\u05d8"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d1\u05e2"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d5"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " fine"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " with"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " missing"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " sugar"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " label"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " it"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " should"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " avoid"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " sounding"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " like"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " hidden"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " estimate"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " Better"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ":\n"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ">"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05d4\u05e1"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d5\u05db\u05e8"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05dc\u05d0"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05e6"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d5\u05d9\u05df"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05d0\u05d1\u05dc"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05e8\u05db"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d9\u05d1"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05d4\u05e1"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d5\u05db\u05e8"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05d4\u05d9\u05d7"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d9\u05d3"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05d4\u05d0\u05e4\u05e9\u05e8"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d9"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05db\u05d0\u05df"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05d4\u05d5\u05d0"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05d4\u05e4\u05e8"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d9"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05e2\u05e6\u05de\u05d5"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " jc"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "011"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d4"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d3\u05e8"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05e7\u05dc"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d9\u05d7"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05e1"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d9\u05ea"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05d1\u05e1"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d5\u05db\u05e8"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05d8\u05d1\u05e2"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d9"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " awkward"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " partly"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " infer"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "ential"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " Since"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " sugar"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " missing"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " avoid"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " comparative"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " sugar"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " language"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "Fix"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ":\n"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ">"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05e7\u05dc"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05de"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05e0\u05d8"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d9\u05e0\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05d5\u05e8"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05e7"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05e7\u05dc"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05de"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05e0\u05d8"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d9\u05e0\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " A"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05e0\u05e9"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05e2\u05df"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05e2\u05dc"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05e8\u05e9"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d9\u05de\u05ea"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05e8\u05db"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d9\u05d1\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05e7\u05e6\u05e8"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d4"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05d5\u05d1\u05e8"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d5\u05e8\u05d4"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05e4\u05e8"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d9"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05d1\u05dc\u05d1\u05d3"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "("}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "e"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ")"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " Hebrew"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " /"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " Natural"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "ness"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "**\n"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "St"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "iff"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " or"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " cal"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "qu"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "ed"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " phrases"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ":\n"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d7"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05de"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d5\u05e6"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d9\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05de\u05e8\u05db\u05d6"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " should"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " be"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d7"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05de"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d5\u05e6"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d9\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05de\u05e8"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d5\u05db"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d6"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " or"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05e8\u05db\u05d6"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05d7\u05de"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d5\u05e6"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d9\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ".\u201d\n"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05de\u05d7"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d9\u05ea"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05de\u05e0"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d2\u05d5"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05de\u05e8\u05db\u05d6"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " should"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " be"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05de\u05d7"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d9\u05ea"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05de\u05e0"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d2\u05d5"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05de\u05e8"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d5\u05db"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d6"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05ea"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ".\u201d\n"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05db\u05dc"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05d4\u05e4\u05e8"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d9"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05de\u05e8\u05db\u05d6"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " should"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " be"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05db\u05dc"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05d4\u05e4\u05e8"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d9"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05de\u05e8"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d5\u05db"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d6"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " or"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05de"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05de\u05e7"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d5\u05e8"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05e8"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05db\u05d6"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ".\u201d\n"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05e9\u05dc"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d5\u05e9\u05d4"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05e8"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d1\u05e2"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d9"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05d4\u05e4"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d7"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d9\u05ea"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05de\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05d5\u05e1"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d5\u05db\u05e8"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " unnatural"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " over"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "prec"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "ise"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05e2"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05e6\u05e8"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05e0\u05d5"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05db\u05d0\u05df"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " nice"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " slightly"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " collo"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "quial"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ";"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " acceptable"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " if"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " page"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " voice"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " allows"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " it"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d7"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d5\u05dc"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05e7"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " A"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05e2\u05dd"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05d7\u05de"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d9\u05e9\u05d4"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05d0\u05d7\u05e8\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " understandable"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " stiff"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " Better"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05e0"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05de\u05e6\u05d0"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05d1\u05d0"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d5\u05ea\u05d4"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05e7\u05d1\u05d5\u05e6"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05ea"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " A"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05e2\u05dd"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05e2\u05d5\u05d3"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05d7\u05de"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d9\u05e9\u05d4"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05de\u05d5\u05e6"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05e8\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05de\u05d0"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d5\u05ea\u05d4"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05e4\u05d9\u05dc"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d5\u05e1"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d5\u05e4"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d9\u05d4"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ".\u201d\n\n"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "("}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "f"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ")"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " Ship"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " /"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " Fix"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "First"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "**\n"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "Fix"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "-first"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "Required"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " before"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " ship"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ":\n"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " Correct"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "/drop"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " jc"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "017"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " false"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "60"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "-point"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " gap"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " Remove"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " jc"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "011"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " kcal"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " sentence"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " Remove"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " score"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " citations"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " in"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " jc"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "024"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " jc"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "027"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " So"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "ften"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " jc"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "024"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "three"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " quarters"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " water"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " sugar"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ".\u201d\n"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " Fix"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05de\u05e8"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05db\u05d6"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " grammar"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " across"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " D"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "/E"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " rows"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " Verify"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " or"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " remove"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " jc"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "025"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d7"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05de"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d9\u05e9\u05d4"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05d7\u05d5\u05de\u05e8"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d9"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05e2"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d9\u05d1"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "\u05d5\u05d3"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " \u05e0\u05d5\u05e1\u05e4\u05d9\u0
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ".\u201d\n\n"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "After"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " those"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " copy"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": " sh"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "ipp"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "able"}
  message.part.delta: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "partID": "prt_ef90146550010gYuKcgGLqZmIR", "field": "text", "delta": "."}
  message.part.updated: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "part": {"id": "prt_ef90146550010gYuKcgGLqZmIR", "messageID": "msg_ef9012088001tjRMc1ji2CuCQG", "sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "type": "
  message.part.updated: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "part": {"id": "prt_ef9027648001HarCM7xzePbobO", "reason": "stop", "snapshot": "7e9ed61c021d1381490d46ea5d8b20d0ef113cc0", "messageID": "msg_ef901208800
  message.updated: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "info": {"id": "msg_ef9012088001tjRMc1ji2CuCQG", "parentID": "msg_ef9011ee90018CdRGqVgGLT0rm", "role": "assistant", "mode": "build", "agent": "build", "
  message.updated: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "info": {"id": "msg_ef9012088001tjRMc1ji2CuCQG", "parentID": "msg_ef9011ee90018CdRGqVgGLT0rm", "role": "assistant", "mode": "build", "agent": "build", "
  session.status: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "status": {"type": "busy"}}
  session.status: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "status": {"type": "idle"}}
  session.idle: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8"}
  session.updated: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "info": {"id": "ses_106fee694ffePN0RGW3bPUzoY8", "slug": "clever-cactus", "projectID": "e7f90f8a5abbaca924c7d1983e3ba702c9bbf643", "directory": "C:\\Bar
  session.diff: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "diff": []}
  message.updated: {"sessionID": "ses_106fee694ffePN0RGW3bPUzoY8", "info": {"role": "user", "time": {"created": 1782294060777}, "agent": "build", "model": {"providerID": "openai", "modelID": "gpt-5.5"}, "summary": {"dif
```

---

## CHANGED-FILES (git status delta)

### Before dispatch

```
M 01_framework/editorial/editorial_intelligence_v3.md
 M 02_products/supplements/real_corpus_v3/_addressable_shelf.json
 M 02_products/supplements/real_corpus_v3/cache/7290015318426.json
 M 02_products/supplements/real_corpus_v3/run_full.py
 M 02_products/supplements/real_corpus_v3/skus_full/SP-0033984003101.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-0033984005181.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-0033984010642.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-0033984020573.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-0033984020580.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-0033984037250.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-712179581913.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290001065594.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290001065662.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290001066973.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290001186237.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290001471845.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290001943212.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290001943700.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290006437273.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290006437563.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290008111041.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290010035984.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290010207640.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290010318230.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290011899127.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290011899967.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290012056741.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290012497643.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290012497650.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290012760204.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290012760266.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290012760761.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290012760853.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290012760891.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290013142146.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290013142894.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290013464248.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290013464897.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290013465535.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290015318426.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290015318433.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290015318532.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290015429177.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290015429245.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290015429290.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290015765572.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290015765985.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290016417197.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290016417227.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017218328.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017218366.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017218526.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017218564.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017218809.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017242170.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017243368.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017243450.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017399638.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017490601.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017847122.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290018365243.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290018365359.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290018439043.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290018439579.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290018439623.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290019444183.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290019444206.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290019444312.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290019444374.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290019444480.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290019918011.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290103449414.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290103449421.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290109317199.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290111594342.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290113826052.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290113828728.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290114965279.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290115971873.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290118814061.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290118816065.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290118818205.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-783495578741.json
 M 03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md
 M 03_operations/bsip2/proto_v0/src/constants.py
 M 03_operations/bsip2/proto_v0/src/router_v2.py
 M 03_operations/bsip2/proto_v0/src/score_engine.py
 M 03_operations/page_generator/conform_baseline.py
 M 03_operations/reports/regression/regression_check_001.md
 M 03_operations/reports/regression/router_regression_001.md
 M 03_operations/supplement_engine/proto_v0/evidence_dossiers/iron.yaml
 M 03_operations/supplement_engine/proto_v0/evidence_dossiers/magnesium.yaml
 M 03_operations/supplement_engine/proto_v0/evidence_dossiers/zinc.yaml
 M 03_operations/supplement_engine/proto_v0/evidence_registry/supp_evidence_registry_v1.md
 M 03_operations/supplement_engine/proto_v0/golden_corpus/fixtures.py
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/ARCH-dangerous-d3-50k_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/ARCH-noevidence-creatine-fatloss_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/ARCH-wasted-creatine-1g_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/DOSE-FAIL-creatine-1g_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/DOSE-PASS-creatine-5g_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/EV-FAIL-omega3-brain_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/EV-PASS-omega3-tg_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/FORM-FAIL-mg-oxide_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/FORM-PASS-mg-glycinate_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/HON-FAIL-caffeine-blend_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/HON-PASS-caffeine-200_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/R1-vague-evidenced-mg_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/R2-vague-snakeoil_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/R3-overspecific-false-mg_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/SAFE-CTRL-d3-50k-weekly_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/SAFE-FAIL-d3-50k_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/SAFE-PASS-d3-2000_trace.json
 M 03_operations/supplement_engine/proto_v0/run_golden_validation.py
 M 03_operations/supplement_engine/proto_v0/src/constants.py
 M 03_operations/supplement_engine/proto_v0/src/dossier_loader.py
 M 03_operations/supplement_engine/proto_v0/src/score_engine.py
 M bari-web/next.config.ts
 M bari-web/src/app/globals.css
 M bari-web/src/app/hashvaot/page.tsx
 M bari-web/src/app/sitemap.ts
 M bari-web/src/components/comparisons/bari-product-thumbnail.tsx
 M bari-web/src/components/comparisons/cereals-comparison-page.tsx
 M bari-web/src/components/comparisons/comparison-page.tsx
 M bari-web/src/components/comparisons/granola-comparison-page.tsx
 M bari-web/src/components/comparisons/protein-bars-comparison-page.tsx
 M bari-web/src/components/shared/category-prologue.tsx
 M bari-web/src/components/shared/comparison-metric-column.tsx
 M bari-web/src/components/shared/comparison-row.tsx
 M bari-web/src/components/shared/comparison-table.tsx
 M bari-web/src/components/shared/expansion-section.tsx
 M bari-web/src/data/comparisons/cereals_frontend_v2.json
 M bari-web/src/data/comparisons/juices_frontend_v3.json
 M bari-web/src/lib/blog/blog-index-content.ts
 M bari-web/src/lib/comparisons/cereals-page-data.ts
 M bari-web/src/lib/comparisons/granola-page-data.ts
 M bari-web/src/lib/comparisons/juices-page-data.ts
 M bari-web/src/lib/comparisons/protein-bars-comparison-page-data.ts
 M bari-web/src/lib/comparisons/row-surface.ts
 M bari-web/src/lib/view-models/index.ts
 M integrations/clients/il_supplement_panels.py
 M tasks/DISPATCH_BOARD.md
?? .claude/skills/build-page/
?? .claude/skills/conformance/
?? .claude/skills/corpus/
?? .claude/skills/telemetry/
?? .claude/skills/tone/
?? 01_framework/bsip2_framework/docs/scoring/zoe_additive_quality_d6_design_v1.md
?? 01_framework/editorial/blog_backlog_v1.md
?? 02_products/_parsing_audit/task378_phase2_analytic.py
?? 02_products/_parsing_audit/task378_phase2_analytic_result.txt
?? 02_products/_parsing_audit/task378_phase2_analytic_results.json
?? 02_products/_parsing_audit/task378_phase2_check.py
?? 02_products/_parsing_audit/task378_phase2_rescore_result.txt
?? 02_products/_parsing_audit/task378_phase2_rescore_results.json
?? 02_products/_parsing_audit/task378_phase2_rescore_sim.py
?? 02_products/_parsing_audit/task378_phase2_result.txt
?? 02_products/_parsing_audit/task378_phase3_rescore_results.json
?? 02_products/_parsing_audit/task378_phase3_shufersal_scrape.json
?? 02_products/bread/staging/
?? 02_products/breakfast_cereals/batch_run_cereals_task387_25g.py
?? 02_products/breakfast_cereals/batch_run_granola_task385_25g.py
?? 02_products/breakfast_cereals/bsip2_outputs/run_cereals_task387_25g/
?? 02_products/breakfast_cereals/bsip2_outputs/run_cereals_task387_off/
?? 02_products/breakfast_cereals/bsip2_outputs/run_granola_task385_25g/
?? 02_products/breakfast_cereals/bsip2_outputs/run_granola_task385_off/
?? 02_products/breakfast_cereals/bsip2_outputs/run_granola_task385_on/
?? 02_products/breakfast_cereals/reports/red_team_granola_run_granola_task385_off.md
?? 02_products/breakfast_cereals/reports/task385_ev105_granola_25g_report.json
?? 02_products/breakfast_cereals/reports/task385_granola_rescore_report.json
?? 02_products/breakfast_cereals/reports/task385_run_record.json
?? 02_products/breakfast_cereals/reports/task387_stage1_cereals_25g_report.json
?? 02_products/breakfast_cereals/task385_granola_rescore.py
?? 02_products/breakfast_cereals/task385_rescore_out.txt
?? 02_products/breakfast_cereals/verify_gran_cross_category_isolation.py
?? 02_products/chocolate/_curate.txt
?? 02_products/chocolate/_score_review.txt
?? 02_products/chocolate/_score_run.log
?? 02_products/chocolate/_scrape_run.log
?? 02_products/chocolate/bsip0_outputs/
?? 02_products/chocolate/bsip2_outputs/
?? 02_products/chocolate/build_rich_chocolate.py
?? 02_products/chocolate/choc_fix_task366.py
?? 02_products/chocolate/choc_laibcatalog_ajax.py
?? 02_products/chocolate/choc_laibcatalog_check.py
?? 02_products/chocolate/choc_laibcatalog_debug.py
?? 02_products/chocolate/choc_tablets_fix_task366_20260622T130415.json
?? 02_products/chocolate/choc_tablets_fix_task366b_20260622T131938.json
?? 02_products/chocolate/choc_tablets_fix_task366b_20260622T135657.json
?? 02_products/chocolate/choc_tablets_fix_task366b_20260622T140340.json
?? 02_products/chocolate/choc_tablets_fix_task366b_20260622T141254.json
?? 02_products/chocolate/choc_task366b_finalize.py
?? 02_products/chocolate/choc_task366b_victory_probe.py
?? 02_products/chocolate/choc_victory_api_probe.py
?? 02_products/chocolate/choc_victory_branch_correct.py
?? 02_products/chocolate/choc_victory_branch_direct.py
?? 02_products/chocolate/choc_victory_catalog_probe.py
?? 02_products/chocolate/choc_victory_catalog_probe2.py
?? 02_products/chocolate/choc_victory_datajs.py
?? 02_products/chocolate/choc_victory_datajs_search.py
?? 02_products/chocolate/choc_victory_direct.py
?? 02_products/chocolate/choc_victory_final.py
?? 02_products/chocolate/choc_victory_final_scrape.py
?? 02_products/chocolate/choc_victory_js_api.py
?? 02_products/chocolate/choc_victory_nutr_api.py
?? 02_products/chocolate/choc_victory_product_direct.py
?? 02_products/chocolate/choc_victory_product_page.py
?? 02_products/chocolate/choc_victory_structure.py
?? 02_products/chocolate/choc_victory_targeted_playwright.py
?? 02_products/chocolate/choc_victory_v2_api.py
?? 02_products/chocolate/choc_victory_v3.py
?? 02_products/chocolate/choc_victory_verify.py
?? 02_products/chocolate/compare_task391.py
?? 02_products/chocolate/fresh_rescore_task391.py
?? 02_products/chocolate/fresh_rescore_task391_20260624_113405_manifest.json
?? 02_products/chocolate/score_choc_task362_20260621_114229_manifest.json
?? 02_products/chocolate/score_choc_task362_20260621_114707_manifest.json
?? 02_products/chocolate/score_choc_task362_20260621_114832_manifest.json
?? 02_products/chocolate/score_chocolate_task362.py
?? 02_products/chocolate/selfverify_task391.py
?? 02_products/chocolate/victory_branch_captured.json
?? 02_products/chocolate/victory_branch_found.json
?? 02_products/chocolate/victory_v2_raw.json
?? 02_products/juices/bsip2_outputs/run_task389_rescore_001/
?? 02_products/juices/bsip2_outputs/run_task389_rescore_002/
?? 02_products/juices/debug2.py
?? 02_products/juices/debug3.py
?? 02_products/juices/debug_nova_signals.py
?? 02_products/juices/run_task389_rescore.py
?? 02_products/juices/write_corrected_rr.py
?? 02_products/milk_and_alternatives/patch_task378_almond_milk_sugar.py
?? 02_products/milk_and_alternatives/task378_almond_milk_rescore.json
?? 02_products/milk_and_alternatives/task378_artifact_sha256.py
?? 02_products/milk_and_alternatives/task378_copy_scan.py
?? 02_products/milk_and_alternatives/task378_sha256.py
?? 02_products/snack_bars/_build_return_contract.py
?? 02_products/snack_bars/_check_borderlines.py
?? 02_products/snack_bars/_check_pb008.py
?? 02_products/snack_bars/_check_pb008_deep.py
?? 02_products/snack_bars/_check_v5.py
?? 02_products/snack_bars/_gate_run_379.py
?? 02_products/snack_bars/_gate_run_379_efsa.py
?? 02_products/snack_bars/_gate_run_379_efsa_out.json
?? 02_products/snack_bars/_gate_run_379_out.json
?? 02_products/snack_bars/_gate_run_379_v2_out.json
?? 02_products/snack_bars/_verify_task365_fix.py
?? 02_products/snack_bars/_verify_v5.py
?? 02_products/snack_bars/bsip2_outputs/protein_bars_task365/
?? 02_products/snack_bars/bsip2_outputs/rescore_prot014_20260621_092813/
?? 02_products/snack_bars/bsip2_outputs/run_snacks_task360_phase3_20260620_083413/
?? 02_products/snack_bars/bsip2_outputs/score_bars_task362_20260620_143230/
?? 02_products/snack_bars/bsip2_outputs/score_bars_task362_20260620_143317/
?? 02_products/snack_bars/bsip2_outputs/score_bars_task362_20260620_143502/
?? 02_products/snack_bars/bsip2_outputs/score_bars_task362_20260620_150421/
?? 02_products/snack_bars/fix_task365_discard_truncated.py
?? 02_products/snack_bars/protein_combined_corpus_task365_20260621_115610.json
?? 02_products/snack_bars/protein_combined_corpus_task365_20260621_120233.json
?? 02_products/snack_bars/protein_combined_corpus_task365_20260621_120733.json
?? 02_products/snack_bars/protein_combined_corpus_task365_20260621_121241.json
?? 02_products/snack_bars/protein_combined_corpus_task365_33_20260621_fix.json
?? 02_products/snack_bars/protein_combined_manifest_task365_20260621_115610.json
?? 02_products/snack_bars/protein_combined_manifest_task365_20260621_120233.json
?? 02_products/snack_bars/protein_combined_manifest_task365_20260621_120733.json
?? 02_products/snack_bars/protein_combined_manifest_task365_20260621_121241.json
?? 02_products/snack_bars/rescore_prot014_20260621_092813_run_record.json
?? 02_products/snack_bars/rescore_prot014_task362.py
?? 02_products/snack_bars/rescore_task365_inplace.py
?? 02_products/snack_bars/run_task365_protein_combined.py
?? 02_products/snack_bars/score_bars_task362_20260620_143317_manifest.json
?? 02_products/snack_bars/score_bars_task362_20260620_143502_manifest.json
?? 02_products/snack_bars/sugar_alcohols_blog_copy_v1.md
?? 02_products/snack_bars/sugar_alcohols_blog_embed_candidates_v1.md
?? 02_products/snack_bars/sugar_alcohols_blog_evidence_v1.md
?? 02_products/snack_bars/sugar_alcohols_blog_nutrition_spec_v1.md
?? 02_products/snack_bars/sugar_alcohols_blog_nutrition_spec_v2.md
?? 02_products/snack_bars/sugar_alcohols_polyol_pct_check_v1.md
?? 02_products/supplements/magnesium_citation_correction_v1.md
?? 02_products/supplements/magnesium_clinical_content_spec_v1.md
?? 02_products/supplements/magnesium_clinical_content_spec_v2.md
?? 02_products/supplements/magnesium_label_interpretation_v1.json
?? 02_products/supplements/magnesium_postmortem_v1.md
?? 02_products/supplements/real_corpus_v3/_corpus_run_full_v10.json
?? 02_products/supplements/real_corpus_v3/_corpus_run_full_v4.json
?? 02_products/supplements/real_corpus_v3/_corpus_run_full_v5.json
?? 02_products/supplements/real_corpus_v3/_corpus_run_full_v6.json
?? 02_products/supplements/real_corpus_v3/_corpus_run_full_v7.json
?? 02_products/supplements/real_corpus_v3/_corpus_run_full_v8.json
?? 02_products/supplements/real_corpus_v3/_corpus_run_full_v9.json
?? 02_products/supplements/real_corpus_v3/_qa_report.md
?? 02_products/supplements/real_corpus_v3/magnesium_assumptions_nutrition_v1.md
?? 02_products/supplements/real_corpus_v3/magnesium_assumptions_redteam_v1.md
?? 02_products/supplements/real_corpus_v3/magnesium_corpus_corrections_applied_v1.md
?? 02_products/supplements/real_corpus_v3/magnesium_corrections_v1.md
?? 02_products/supplements/real_corpus_v3/magnesium_elemental_reconciliation_v1.md
?? 02_products/supplements/real_corpus_v3/magnesium_label_audit_v1.md
?? 02_products/supplements/real_corpus_v3/magnesium_ul_ruling_v1.md
?? 02_products/supplements/real_corpus_v3/qa_audit.py
?? 02_products/supplements/real_corpus_v3/red_team_magnesium_page_v1.md
?? 02_products/supplements/real_corpus_v3/red_team_magnesium_page_v2.md
?? 02_products/supplements/real_corpus_v3/red_team_magnesium_page_v3.md
?? 02_products/supplements/real_corpus_v3/red_team_magnesium_page_v3_regate.md
?? 02_products/supplements/real_corpus_v3/red_team_magnesium_page_v4.md
?? 02_products/supplements/real_corpus_v3/red_team_magnesium_value_framing_v1.md
?? 02_products/supplements/real_corpus_v3/red_team_sie_v3.md
?? 02_products/supplements/real_corpus_v3/red_team_sie_v6.md
?? 02_products/supplements/real_corpus_v3/red_team_sie_v7.md
?? 02_products/supplements/real_corpus_v3/red_team_sie_v8.md
?? 03_operations/bsip1/choc_task366_pass2_20260622_135915/
?? 03_operations/bsip1/choc_task366_pass2_20260622_140019/
?? 03_operations/bsip1/choc_task366_pass2_20260622_140047/
?? 03_operations/bsip1/choc_task366_pass2_20260622_140126/
?? 03_operations/bsip1/choc_task366_pass2_20260622_140336/
?? 03_operations/bsip1/choc_tmp/
?? 03_operations/bsip1/fresh_rescore_task391_20260624_113405/
?? 03_operations/bsip1/score_bars_task362_20260620_143230/
?? 03_operations/bsip1/score_bars_task362_20260620_143317/
?? 03_operations/bsip1/score_bars_task362_20260620_143502/
?? 03_operations/bsip1/score_bars_task362_20260620_150421/
?? 03_operations/bsip1/score_choc_task362_20260621_114229/
?? 03_operations/bsip1/score_choc_task362_20260621_114707/
?? 03_operations/bsip1/score_choc_task362_20260621_114832/
?? 03_operations/bsip1/task366_20260622T130415/
?? 03_operations/bsip2/protein_bar_lens_spec_task365.md
?? 03_operations/bsip2/proto_v0/diag_task371_step1/
?? 03_operations/bsip2/proto_v0/reports/glass_box/w2/_verify_d4_bars.py
?? 03_operations/bsip2/proto_v0/src/batch_run_protein_bars_task365.py
?? 03_operations/bsip2/proto_v0/src/run_task371_d4_score.py
?? 03_operations/bsip2/proto_v0/src/run_task388_calibrated_cosmetic_mup.py
?? 03_operations/bsip2/proto_v0/src/run_task388_clean_test.py
?? 03_operations/bsip2/proto_v0/src/run_task388_full_table.py
?? 03_operations/bsip2/proto_v0/src/run_task388_groundtruth.py
?? 03_operations/cc_history_analyzer/
?? 03_operations/shadow/goldset/
?? 03_operations/supplement_engine/proto_v0/benchmark/
?? 03_operations/supplement_engine/proto_v0/golden_corpus/traces/RT7-H1-elemental-form-none-overdose_trace.json
?? 03_operations/supplement_engine/proto_v0/magnesium_benchmark_recalibration_proposal.md
?? 03_operations/supplement_engine/proto_v0/prototype_absorbed_scoring.py
?? 03_operations/tools/task366_r2_verify.py
?? 03_operations/tools/task366_verify.py
?? 03_operations/tools/task366_verify_out.txt
?? 03_operations/tools/task366_wave6_audit.py
?? 03_operations/tools/task366_wave6_out.txt
?? "C\357\200\272Temppb_head.json"
?? _content_r2_verify.txt
?? _devserver.log
?? _fat_check.txt
?? _granola_audit.txt
?? _granola_content_verify.txt
?? _granola_rec.txt
?? _granola_render.html
?? _granola_score.txt
?? _granola_score2.txt
?? _granola_trace.txt
?? _granola_verify.txt
?? _meeting/
?? _milk_deploy_check.txt
?? _milk_final.txt
?? _milk_ranks.txt
?? _milk_verify.txt
?? _naturalness_result.json
?? _nut_xcheck.txt
?? _p282_dispatch.log
?? _prov_check.txt
?? _r3_final.txt
?? _r3_remaining.txt
?? _r3_verify.txt
?? _r_snacks.html
?? _render_result.txt
?? _snk_patch.py
?? _snk_verdicts_for_c3.txt
?? _task388_groundtruth.json
?? _tmp_hc_fields.py
?? _tmp_hc_orig.py
?? _tmp_mg_audit.py
?? _tmp_mg_audit2.py
?? _tmp_mg_audit3.py
?? _tmp_mg_audit4.py
?? _tmp_mg_audit5.py
?? _tmp_mg_audit6.py
?? _tmp_score_review.py
?? _tmp_snack_orig.py
?? _tmp_snack_review.py
?? _tmp_tink_detail.py
?? _tmp_v8_analysis.py
?? _tmp_v8_check.py
?? _tmp_v8_zinc.py
?? _verify_out.txt
?? affected_set_spine.json
?? bari-web/dev-server-err.log
?? bari-web/dev-server.log
?? bari-web/e2e/magnesium-geometry.spec.ts
?? bari-web/e2e/screenshots/
?? bari-web/e2e/task384-geometry.spec.ts
?? bari-web/geo_content.cjs
?? bari-web/geo_expand.cjs
?? bari-web/geo_full.cjs
?? bari-web/geo_leakage.cjs
?? bari-web/geo_rowhead.cjs
?? bari-web/geo_test.cjs
?? bari-web/geo_test.mjs
?? bari-web/geo_test2.cjs
?? bari-web/geo_test3.cjs
?? bari-web/mag_mobile_390.png
?? bari-web/magnesium-geometry.png
?? bari-web/scripts/measure-dom-structure.mjs
?? bari-web/scripts/measure-granola-geometry.mjs
?? bari-web/scripts/measure-header-breakdown.mjs
?? bari-web/scripts/measure-magnesium-geometry.mjs
?? bari-web/scripts/measure-rows-detail.mjs
?? bari-web/server-err.txt
?? bari-web/server-out.txt
?? bari-web/server.log
?? bari-web/src/app/blog/sugar-alcohols/
?? bari-web/src/app/hashvaot/chocolate-bars/
?? bari-web/src/app/hashvaot/chocolate-tablets/
?? bari-web/src/app/hashvaot/magnesium/
?? bari-web/src/app/hashvaot/supplements/
?? bari-web/src/components/blog/sugar-alcohols-article.tsx
?? bari-web/src/components/blog/sugar-alcohols-chart1.tsx
?? bari-web/src/components/blog/sugar-alcohols-chart2.tsx
?? bari-web/src/components/blog/sugar-alcohols-efsa-card.tsx
?? bari-web/src/components/blog/sugar-alcohols-front-vs-back.tsx
?? bari-web/src/components/comparisons/chocolate-bars-comparison-page.tsx
?? bari-web/src/components/comparisons/chocolate-tablets-comparison-page.tsx
?? bari-web/src/components/comparisons/magnesium-comparison-page.tsx
?? bari-web/src/components/hashvaot/featured-chocolate-bars-intelligence-card.tsx
?? bari-web/src/components/hashvaot/featured-chocolate-tablets-intelligence-card.tsx
?? bari-web/src/components/hashvaot/featured-magnesium-intelligence-card.tsx
?? bari-web/src/components/shared/magnesium-badge-grid.tsx
?? bari-web/src/components/shared/magnesium-safety-box.tsx
?? bari-web/src/data/comparisons/bread_frontend_v2_gates_report.md
?? bari-web/src/data/comparisons/bread_frontend_v3_gates_report.md
?? bari-web/src/data/comparisons/brined_cheeses_frontend_v2_gates_report.md
?? bari-web/src/data/comparisons/cakes_hard_cookies_frontend_v1_gates_report.md
?? bari-web/src/data/comparisons/cheese_frontend_v4_gates_report.md
?? bari-web/src/data/comparisons/chocolate_bars_frontend_v1.json
?? bari-web/src/data/comparisons/chocolate_tablets_frontend_v1.json
?? bari-web/src/data/comparisons/chocolate_tablets_frontend_v1_gates_report.md
?? bari-web/src/data/comparisons/cookies_coffee_frontend_v2_gates_report.md
?? bari-web/src/data/comparisons/granola_frontend_v1_gates_report.md
?? bari-web/src/data/comparisons/granola_frontend_v2.json
?? bari-web/src/data/comparisons/hard_cheeses_frontend_v2_gates_report.md
?? bari-web/src/data/comparisons/hummus_frontend_v5_gates_report.md
?? bari-web/src/data/comparisons/juices_frontend_v3_gates_report.md
?? bari-web/src/data/comparisons/milk_frontend_v1_gates_report.md
?? bari-web/src/data/comparisons/protein_combined_frontend_v2_gates_report.md
?? bari-web/src/data/comparisons/snacks_frontend_v2_gates_report.md
?? bari-web/src/data/comparisons/snacks_frontend_v3_gates_report.md
?? bari-web/src/lib/blog/sugar-alcohols-article-content.ts
?? bari-web/src/lib/comparisons/chocolate-bars-comparison-page-data.ts
?? bari-web/src/lib/comparisons/chocolate-bars-shelf-filters.ts
?? bari-web/src/lib/comparisons/chocolate-tablets-comparison-page-data.ts
?? bari-web/src/lib/comparisons/chocolate-tablets-shelf-filters.ts
?? bari-web/src/lib/comparisons/magnesium-page-data.ts
?? bari-web/tmp_dev_log.txt
?? bari-web/tmp_shots/hashvaot_index_mobile.png
?? bari-web/tmp_shots/mag_mobile_0scroll.png
?? bari-web/tmp_shots/mag_visual_check.cjs
?? bari-web/tmp_shots/oxide_safety_check.cjs
?? bari-web/tmp_shots/oxide_safety_visible.png
?? bari-web/tmp_shots/supp_check.cjs
?? bari-web/tmp_shots/supplements_index.png
?? bari-web/verify-magnesium-clamp.js
?? check_cc_bsip0.py
?? check_cc_carbs.py
?? check_cc_remaining.py
?? check_milk_carbs.py
?? check_remaining_cheese_brined_cereals.py
?? check_unknown_carbs.py
?? check_unknown_carbs_v2.py
?? content_voice/tone_briefs/
?? dev_server_log.txt
?? diag_task371_step1.py
?? integrations/clients/lnhpd.py
?? integrations/clients/tga.py
?? pb_head_tmp.json
?? qa_deep_check.py
?? qa_leakage_voice.py
?? qa_number_fidelity.py
?? qa_superlative_check.py
?? "research/Magnesium Oral Supplements Worldwide Benchmark.pdf"
?? scan_sugar_null.py
?? scan_sugar_null_v2.py
?? tasks/TASK-349.md
?? tasks/TASK-357.md
?? tasks/TASK-358.md
?? tasks/TASK-359.md
?? tasks/TASK-361.md
?? tasks/TASK-361A.md
?? tasks/TASK-364.md
?? tasks/TASK-365.md
?? tasks/TASK-366.md
?? tasks/TASK-367.md
?? tasks/TASK-368.md
?? tasks/TASK-369.md
?? tasks/TASK-370.md
?? tasks/TASK-372.md
?? tasks/TASK-373.md
?? tasks/TASK-379.md
?? tasks/TASK-380.md
?? tasks/TASK-383.md
?? tasks/TASK-384.md
?? tasks/TASK-384A.md
?? tasks/TASK-385.md
?? tasks/TASK-386.md
?? tasks/TASK-387.md
?? tasks/TASK-389.md
?? tasks/TASK-390.md
?? tasks/TASK-391.md
?? tasks/_scratch_mag_labels/
?? tasks/_scratch_naturalness_badges.py
?? tasks/_scratch_naturalness_check.py
?? tasks/_scratch_naturalness_result.json
?? tasks/_scratch_verdict_audit.py
?? tasks/_scratch_verdict_len.py
?? tasks/_task371_layer1_diagnostic.py
?? tasks/_task371_layer1_v2.py
?? tasks/_task371_score_one.py
?? tasks/autonomous_orchestrate.ps1
?? tasks/closed/TASK-388.md
?? tasks/digests/
?? tasks/prompts/P233_c2_goldset_candidate_extract.md
?? tasks/prompts/P234_c3_goldset_methodology_redteam.md
?? tasks/prompts/P235_c1_nutrition_goldset_phase0.md
?? tasks/prompts/P236_c1cursor_goldcheck_harness.md
?? tasks/prompts/P237_c1grok_goldset_seed_encode.md
?? tasks/prompts/P238_c1gemini_goldset_schema_validator_ci.md
?? tasks/prompts/P239_c2_sie_sa_traceability_audit.md
?? tasks/prompts/P240_c3_sie_broaden_sources_research.md
?? tasks/prompts/P241_c2_magnesium_elemental_arithmetic_check.md
?? tasks/prompts/P242_c3_magnesium_benchmark_philosophy_redteam.md
?? tasks/prompts/P243_c2_magnesium_delivery_arithmetic_recheck.md
?? tasks/prompts/P244_c3_eu_magnesium_shelf_hunt.md
?? tasks/prompts/P245_c3_zinc_worldwide_benchmark.md
?? tasks/prompts/P246_c3_magnesium_assumptions_challenge.md
?? tasks/prompts/P280_c3_snacks_challenge.md
?? tasks/prompts/P282_snacks_relief_challenge.md
?? tasks/prompts/P300_c3_magnesium_elemental_challenge.md
?? tasks/prompts/P301_c3_magnesium_recalibration_challenge.md
?? tasks/prompts/P303_c3_magnesium_v3_final_teardown.md
?? tasks/prompts/P304_c3_magnesium_content_gate.md
?? tasks/prompts/P305_c3_magnesium_content_regate.md
?? tasks/prompts/P387_granola_c3_challenge.md
?? tasks/prompts/P388_granola_c3_verify.md
?? tasks/prompts/P389_c3_magnesium_clinical_validity.md
?? tasks/prompts/P392_juices_decite_c3.md
?? tasks/prompts/_done/P283_protein_bars_r3_mechanical.md
?? tasks/prompts/_done/P297_hc_satfat_rule_challenge.md
?? tasks/prompts/_done/P302_c3_magnesium_v3_real_calibration_challenge.md
?? tasks/prompts/_done/P390_granola_decite_c3.md
?? tasks/prompts/_done/P391_cereals_decite_c3.md
?? tasks/returns/P233_return.md
?? tasks/returns/P234_return.md
?? tasks/returns/P239_return.md
?? tasks/returns/P240_return.md
?? tasks/returns/P241_return.md
?? tasks/returns/P242_return.md
?? tasks/returns/P243_return.md
?? tasks/returns/P244_return.md
?? tasks/returns/P245_return.md
?? tasks/returns/P246_return.md
?? tasks/returns/P258_voice_redteam.md
?? tasks/returns/P261_hc_voice_redteam.md
?? tasks/returns/P265_snacks_v3_voice_redteam.md
?? tasks/returns/P268_drift_report.md
?? tasks/returns/P280_return.md
?? tasks/returns/P282_return.md
?? tasks/returns/P297_return.md
?? tasks/returns/P300_return.md
?? tasks/returns/P301_return.md
?? tasks/returns/P302_return.md
?? tasks/returns/P303_return.md
?? tasks/returns/P304_return.md
?? tasks/returns/P305_return.md
?? tasks/returns/P387_return.md
?? tasks/returns/P388_return.md
?? tasks/returns/P389_return.md
?? tasks/returns/P390_return.md
?? tasks/returns/P391_return.md
?? tasks/task368_d4_impact_analysis.py
?? tasks/task368_output.txt
?? test_acceptance.py
```

### After dispatch

```
M 01_framework/editorial/editorial_intelligence_v3.md
 M 02_products/supplements/real_corpus_v3/_addressable_shelf.json
 M 02_products/supplements/real_corpus_v3/cache/7290015318426.json
 M 02_products/supplements/real_corpus_v3/run_full.py
 M 02_products/supplements/real_corpus_v3/skus_full/SP-0033984003101.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-0033984005181.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-0033984010642.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-0033984020573.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-0033984020580.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-0033984037250.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-712179581913.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290001065594.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290001065662.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290001066973.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290001186237.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290001471845.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290001943212.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290001943700.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290006437273.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290006437563.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290008111041.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290010035984.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290010207640.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290010318230.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290011899127.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290011899967.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290012056741.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290012497643.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290012497650.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290012760204.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290012760266.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290012760761.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290012760853.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290012760891.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290013142146.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290013142894.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290013464248.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290013464897.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290013465535.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290015318426.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290015318433.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290015318532.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290015429177.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290015429245.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290015429290.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290015765572.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290015765985.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290016417197.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290016417227.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017218328.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017218366.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017218526.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017218564.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017218809.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017242170.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017243368.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017243450.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017399638.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017490601.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017847122.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290018365243.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290018365359.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290018439043.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290018439579.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290018439623.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290019444183.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290019444206.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290019444312.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290019444374.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290019444480.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290019918011.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290103449414.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290103449421.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290109317199.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290111594342.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290113826052.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290113828728.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290114965279.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290115971873.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290118814061.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290118816065.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290118818205.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-783495578741.json
 M 03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md
 M 03_operations/bsip2/proto_v0/src/constants.py
 M 03_operations/bsip2/proto_v0/src/router_v2.py
 M 03_operations/bsip2/proto_v0/src/score_engine.py
 M 03_operations/page_generator/conform_baseline.py
 M 03_operations/reports/regression/regression_check_001.md
 M 03_operations/reports/regression/router_regression_001.md
 M 03_operations/supplement_engine/proto_v0/evidence_dossiers/iron.yaml
 M 03_operations/supplement_engine/proto_v0/evidence_dossiers/magnesium.yaml
 M 03_operations/supplement_engine/proto_v0/evidence_dossiers/zinc.yaml
 M 03_operations/supplement_engine/proto_v0/evidence_registry/supp_evidence_registry_v1.md
 M 03_operations/supplement_engine/proto_v0/golden_corpus/fixtures.py
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/ARCH-dangerous-d3-50k_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/ARCH-noevidence-creatine-fatloss_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/ARCH-wasted-creatine-1g_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/DOSE-FAIL-creatine-1g_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/DOSE-PASS-creatine-5g_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/EV-FAIL-omega3-brain_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/EV-PASS-omega3-tg_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/FORM-FAIL-mg-oxide_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/FORM-PASS-mg-glycinate_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/HON-FAIL-caffeine-blend_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/HON-PASS-caffeine-200_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/R1-vague-evidenced-mg_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/R2-vague-snakeoil_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/R3-overspecific-false-mg_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/SAFE-CTRL-d3-50k-weekly_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/SAFE-FAIL-d3-50k_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/SAFE-PASS-d3-2000_trace.json
 M 03_operations/supplement_engine/proto_v0/run_golden_validation.py
 M 03_operations/supplement_engine/proto_v0/src/constants.py
 M 03_operations/supplement_engine/proto_v0/src/dossier_loader.py
 M 03_operations/supplement_engine/proto_v0/src/score_engine.py
 M bari-web/next.config.ts
 M bari-web/src/app/globals.css
 M bari-web/src/app/hashvaot/page.tsx
 M bari-web/src/app/sitemap.ts
 M bari-web/src/components/comparisons/bari-product-thumbnail.tsx
 M bari-web/src/components/comparisons/cereals-comparison-page.tsx
 M bari-web/src/components/comparisons/comparison-page.tsx
 M bari-web/src/components/comparisons/granola-comparison-page.tsx
 M bari-web/src/components/comparisons/protein-bars-comparison-page.tsx
 M bari-web/src/components/shared/category-prologue.tsx
 M bari-web/src/components/shared/comparison-metric-column.tsx
 M bari-web/src/components/shared/comparison-row.tsx
 M bari-web/src/components/shared/comparison-table.tsx
 M bari-web/src/components/shared/expansion-section.tsx
 M bari-web/src/data/comparisons/cereals_frontend_v2.json
 M bari-web/src/data/comparisons/juices_frontend_v3.json
 M bari-web/src/lib/blog/blog-index-content.ts
 M bari-web/src/lib/comparisons/cereals-page-data.ts
 M bari-web/src/lib/comparisons/granola-page-data.ts
 M bari-web/src/lib/comparisons/juices-page-data.ts
 M bari-web/src/lib/comparisons/protein-bars-comparison-page-data.ts
 M bari-web/src/lib/comparisons/row-surface.ts
 M bari-web/src/lib/view-models/index.ts
 M integrations/clients/il_supplement_panels.py
 M tasks/DISPATCH_BOARD.md
?? .claude/skills/build-page/
?? .claude/skills/conformance/
?? .claude/skills/corpus/
?? .claude/skills/telemetry/
?? .claude/skills/tone/
?? 01_framework/bsip2_framework/docs/scoring/zoe_additive_quality_d6_design_v1.md
?? 01_framework/editorial/blog_backlog_v1.md
?? 02_products/_parsing_audit/task378_phase2_analytic.py
?? 02_products/_parsing_audit/task378_phase2_analytic_result.txt
?? 02_products/_parsing_audit/task378_phase2_analytic_results.json
?? 02_products/_parsing_audit/task378_phase2_check.py
?? 02_products/_parsing_audit/task378_phase2_rescore_result.txt
?? 02_products/_parsing_audit/task378_phase2_rescore_results.json
?? 02_products/_parsing_audit/task378_phase2_rescore_sim.py
?? 02_products/_parsing_audit/task378_phase2_result.txt
?? 02_products/_parsing_audit/task378_phase3_rescore_results.json
?? 02_products/_parsing_audit/task378_phase3_shufersal_scrape.json
?? 02_products/bread/staging/
?? 02_products/breakfast_cereals/batch_run_cereals_task387_25g.py
?? 02_products/breakfast_cereals/batch_run_granola_task385_25g.py
?? 02_products/breakfast_cereals/bsip2_outputs/run_cereals_task387_25g/
?? 02_products/breakfast_cereals/bsip2_outputs/run_cereals_task387_off/
?? 02_products/breakfast_cereals/bsip2_outputs/run_granola_task385_25g/
?? 02_products/breakfast_cereals/bsip2_outputs/run_granola_task385_off/
?? 02_products/breakfast_cereals/bsip2_outputs/run_granola_task385_on/
?? 02_products/breakfast_cereals/reports/red_team_granola_run_granola_task385_off.md
?? 02_products/breakfast_cereals/reports/task385_ev105_granola_25g_report.json
?? 02_products/breakfast_cereals/reports/task385_granola_rescore_report.json
?? 02_products/breakfast_cereals/reports/task385_run_record.json
?? 02_products/breakfast_cereals/reports/task387_stage1_cereals_25g_report.json
?? 02_products/breakfast_cereals/task385_granola_rescore.py
?? 02_products/breakfast_cereals/task385_rescore_out.txt
?? 02_products/breakfast_cereals/verify_gran_cross_category_isolation.py
?? 02_products/chocolate/_curate.txt
?? 02_products/chocolate/_score_review.txt
?? 02_products/chocolate/_score_run.log
?? 02_products/chocolate/_scrape_run.log
?? 02_products/chocolate/bsip0_outputs/
?? 02_products/chocolate/bsip2_outputs/
?? 02_products/chocolate/build_rich_chocolate.py
?? 02_products/chocolate/choc_fix_task366.py
?? 02_products/chocolate/choc_laibcatalog_ajax.py
?? 02_products/chocolate/choc_laibcatalog_check.py
?? 02_products/chocolate/choc_laibcatalog_debug.py
?? 02_products/chocolate/choc_tablets_fix_task366_20260622T130415.json
?? 02_products/chocolate/choc_tablets_fix_task366b_20260622T131938.json
?? 02_products/chocolate/choc_tablets_fix_task366b_20260622T135657.json
?? 02_products/chocolate/choc_tablets_fix_task366b_20260622T140340.json
?? 02_products/chocolate/choc_tablets_fix_task366b_20260622T141254.json
?? 02_products/chocolate/choc_task366b_finalize.py
?? 02_products/chocolate/choc_task366b_victory_probe.py
?? 02_products/chocolate/choc_victory_api_probe.py
?? 02_products/chocolate/choc_victory_branch_correct.py
?? 02_products/chocolate/choc_victory_branch_direct.py
?? 02_products/chocolate/choc_victory_catalog_probe.py
?? 02_products/chocolate/choc_victory_catalog_probe2.py
?? 02_products/chocolate/choc_victory_datajs.py
?? 02_products/chocolate/choc_victory_datajs_search.py
?? 02_products/chocolate/choc_victory_direct.py
?? 02_products/chocolate/choc_victory_final.py
?? 02_products/chocolate/choc_victory_final_scrape.py
?? 02_products/chocolate/choc_victory_js_api.py
?? 02_products/chocolate/choc_victory_nutr_api.py
?? 02_products/chocolate/choc_victory_product_direct.py
?? 02_products/chocolate/choc_victory_product_page.py
?? 02_products/chocolate/choc_victory_structure.py
?? 02_products/chocolate/choc_victory_targeted_playwright.py
?? 02_products/chocolate/choc_victory_v2_api.py
?? 02_products/chocolate/choc_victory_v3.py
?? 02_products/chocolate/choc_victory_verify.py
?? 02_products/chocolate/compare_task391.py
?? 02_products/chocolate/fresh_rescore_task391.py
?? 02_products/chocolate/fresh_rescore_task391_20260624_113405_manifest.json
?? 02_products/chocolate/score_choc_task362_20260621_114229_manifest.json
?? 02_products/chocolate/score_choc_task362_20260621_114707_manifest.json
?? 02_products/chocolate/score_choc_task362_20260621_114832_manifest.json
?? 02_products/chocolate/score_chocolate_task362.py
?? 02_products/chocolate/selfverify_task391.py
?? 02_products/chocolate/victory_branch_captured.json
?? 02_products/chocolate/victory_branch_found.json
?? 02_products/chocolate/victory_v2_raw.json
?? 02_products/juices/bsip2_outputs/run_task389_rescore_001/
?? 02_products/juices/bsip2_outputs/run_task389_rescore_002/
?? 02_products/juices/debug2.py
?? 02_products/juices/debug3.py
?? 02_products/juices/debug_nova_signals.py
?? 02_products/juices/run_task389_rescore.py
?? 02_products/juices/write_corrected_rr.py
?? 02_products/milk_and_alternatives/patch_task378_almond_milk_sugar.py
?? 02_products/milk_and_alternatives/task378_almond_milk_rescore.json
?? 02_products/milk_and_alternatives/task378_artifact_sha256.py
?? 02_products/milk_and_alternatives/task378_copy_scan.py
?? 02_products/milk_and_alternatives/task378_sha256.py
?? 02_products/snack_bars/_build_return_contract.py
?? 02_products/snack_bars/_check_borderlines.py
?? 02_products/snack_bars/_check_pb008.py
?? 02_products/snack_bars/_check_pb008_deep.py
?? 02_products/snack_bars/_check_v5.py
?? 02_products/snack_bars/_gate_run_379.py
?? 02_products/snack_bars/_gate_run_379_efsa.py
?? 02_products/snack_bars/_gate_run_379_efsa_out.json
?? 02_products/snack_bars/_gate_run_379_out.json
?? 02_products/snack_bars/_gate_run_379_v2_out.json
?? 02_products/snack_bars/_verify_task365_fix.py
?? 02_products/snack_bars/_verify_v5.py
?? 02_products/snack_bars/bsip2_outputs/protein_bars_task365/
?? 02_products/snack_bars/bsip2_outputs/rescore_prot014_20260621_092813/
?? 02_products/snack_bars/bsip2_outputs/run_snacks_task360_phase3_20260620_083413/
?? 02_products/snack_bars/bsip2_outputs/score_bars_task362_20260620_143230/
?? 02_products/snack_bars/bsip2_outputs/score_bars_task362_20260620_143317/
?? 02_products/snack_bars/bsip2_outputs/score_bars_task362_20260620_143502/
?? 02_products/snack_bars/bsip2_outputs/score_bars_task362_20260620_150421/
?? 02_products/snack_bars/fix_task365_discard_truncated.py
?? 02_products/snack_bars/protein_combined_corpus_task365_20260621_115610.json
?? 02_products/snack_bars/protein_combined_corpus_task365_20260621_120233.json
?? 02_products/snack_bars/protein_combined_corpus_task365_20260621_120733.json
?? 02_products/snack_bars/protein_combined_corpus_task365_20260621_121241.json
?? 02_products/snack_bars/protein_combined_corpus_task365_33_20260621_fix.json
?? 02_products/snack_bars/protein_combined_manifest_task365_20260621_115610.json
?? 02_products/snack_bars/protein_combined_manifest_task365_20260621_120233.json
?? 02_products/snack_bars/protein_combined_manifest_task365_20260621_120733.json
?? 02_products/snack_bars/protein_combined_manifest_task365_20260621_121241.json
?? 02_products/snack_bars/rescore_prot014_20260621_092813_run_record.json
?? 02_products/snack_bars/rescore_prot014_task362.py
?? 02_products/snack_bars/rescore_task365_inplace.py
?? 02_products/snack_bars/run_task365_protein_combined.py
?? 02_products/snack_bars/score_bars_task362_20260620_143317_manifest.json
?? 02_products/snack_bars/score_bars_task362_20260620_143502_manifest.json
?? 02_products/snack_bars/sugar_alcohols_blog_copy_v1.md
?? 02_products/snack_bars/sugar_alcohols_blog_embed_candidates_v1.md
?? 02_products/snack_bars/sugar_alcohols_blog_evidence_v1.md
?? 02_products/snack_bars/sugar_alcohols_blog_nutrition_spec_v1.md
?? 02_products/snack_bars/sugar_alcohols_blog_nutrition_spec_v2.md
?? 02_products/snack_bars/sugar_alcohols_polyol_pct_check_v1.md
?? 02_products/supplements/magnesium_citation_correction_v1.md
?? 02_products/supplements/magnesium_clinical_content_spec_v1.md
?? 02_products/supplements/magnesium_clinical_content_spec_v2.md
?? 02_products/supplements/magnesium_label_interpretation_v1.json
?? 02_products/supplements/magnesium_postmortem_v1.md
?? 02_products/supplements/real_corpus_v3/_corpus_run_full_v10.json
?? 02_products/supplements/real_corpus_v3/_corpus_run_full_v4.json
?? 02_products/supplements/real_corpus_v3/_corpus_run_full_v5.json
?? 02_products/supplements/real_corpus_v3/_corpus_run_full_v6.json
?? 02_products/supplements/real_corpus_v3/_corpus_run_full_v7.json
?? 02_products/supplements/real_corpus_v3/_corpus_run_full_v8.json
?? 02_products/supplements/real_corpus_v3/_corpus_run_full_v9.json
?? 02_products/supplements/real_corpus_v3/_qa_report.md
?? 02_products/supplements/real_corpus_v3/magnesium_assumptions_nutrition_v1.md
?? 02_products/supplements/real_corpus_v3/magnesium_assumptions_redteam_v1.md
?? 02_products/supplements/real_corpus_v3/magnesium_corpus_corrections_applied_v1.md
?? 02_products/supplements/real_corpus_v3/magnesium_corrections_v1.md
?? 02_products/supplements/real_corpus_v3/magnesium_elemental_reconciliation_v1.md
?? 02_products/supplements/real_corpus_v3/magnesium_label_audit_v1.md
?? 02_products/supplements/real_corpus_v3/magnesium_ul_ruling_v1.md
?? 02_products/supplements/real_corpus_v3/qa_audit.py
?? 02_products/supplements/real_corpus_v3/red_team_magnesium_page_v1.md
?? 02_products/supplements/real_corpus_v3/red_team_magnesium_page_v2.md
?? 02_products/supplements/real_corpus_v3/red_team_magnesium_page_v3.md
?? 02_products/supplements/real_corpus_v3/red_team_magnesium_page_v3_regate.md
?? 02_products/supplements/real_corpus_v3/red_team_magnesium_page_v4.md
?? 02_products/supplements/real_corpus_v3/red_team_magnesium_value_framing_v1.md
?? 02_products/supplements/real_corpus_v3/red_team_sie_v3.md
?? 02_products/supplements/real_corpus_v3/red_team_sie_v6.md
?? 02_products/supplements/real_corpus_v3/red_team_sie_v7.md
?? 02_products/supplements/real_corpus_v3/red_team_sie_v8.md
?? 03_operations/bsip1/choc_task366_pass2_20260622_135915/
?? 03_operations/bsip1/choc_task366_pass2_20260622_140019/
?? 03_operations/bsip1/choc_task366_pass2_20260622_140047/
?? 03_operations/bsip1/choc_task366_pass2_20260622_140126/
?? 03_operations/bsip1/choc_task366_pass2_20260622_140336/
?? 03_operations/bsip1/choc_tmp/
?? 03_operations/bsip1/fresh_rescore_task391_20260624_113405/
?? 03_operations/bsip1/score_bars_task362_20260620_143230/
?? 03_operations/bsip1/score_bars_task362_20260620_143317/
?? 03_operations/bsip1/score_bars_task362_20260620_143502/
?? 03_operations/bsip1/score_bars_task362_20260620_150421/
?? 03_operations/bsip1/score_choc_task362_20260621_114229/
?? 03_operations/bsip1/score_choc_task362_20260621_114707/
?? 03_operations/bsip1/score_choc_task362_20260621_114832/
?? 03_operations/bsip1/task366_20260622T130415/
?? 03_operations/bsip2/protein_bar_lens_spec_task365.md
?? 03_operations/bsip2/proto_v0/diag_task371_step1/
?? 03_operations/bsip2/proto_v0/reports/glass_box/w2/_verify_d4_bars.py
?? 03_operations/bsip2/proto_v0/src/batch_run_protein_bars_task365.py
?? 03_operations/bsip2/proto_v0/src/run_task371_d4_score.py
?? 03_operations/bsip2/proto_v0/src/run_task388_calibrated_cosmetic_mup.py
?? 03_operations/bsip2/proto_v0/src/run_task388_clean_test.py
?? 03_operations/bsip2/proto_v0/src/run_task388_full_table.py
?? 03_operations/bsip2/proto_v0/src/run_task388_groundtruth.py
?? 03_operations/cc_history_analyzer/
?? 03_operations/shadow/goldset/
?? 03_operations/supplement_engine/proto_v0/benchmark/
?? 03_operations/supplement_engine/proto_v0/golden_corpus/traces/RT7-H1-elemental-form-none-overdose_trace.json
?? 03_operations/supplement_engine/proto_v0/magnesium_benchmark_recalibration_proposal.md
?? 03_operations/supplement_engine/proto_v0/prototype_absorbed_scoring.py
?? 03_operations/tools/task366_r2_verify.py
?? 03_operations/tools/task366_verify.py
?? 03_operations/tools/task366_verify_out.txt
?? 03_operations/tools/task366_wave6_audit.py
?? 03_operations/tools/task366_wave6_out.txt
?? "C\357\200\272Temppb_head.json"
?? _content_r2_verify.txt
?? _devserver.log
?? _fat_check.txt
?? _granola_audit.txt
?? _granola_content_verify.txt
?? _granola_rec.txt
?? _granola_render.html
?? _granola_score.txt
?? _granola_score2.txt
?? _granola_trace.txt
?? _granola_verify.txt
?? _meeting/
?? _milk_deploy_check.txt
?? _milk_final.txt
?? _milk_ranks.txt
?? _milk_verify.txt
?? _naturalness_result.json
?? _nut_xcheck.txt
?? _p282_dispatch.log
?? _prov_check.txt
?? _r3_final.txt
?? _r3_remaining.txt
?? _r3_verify.txt
?? _r_snacks.html
?? _render_result.txt
?? _snk_patch.py
?? _snk_verdicts_for_c3.txt
?? _task388_groundtruth.json
?? _tmp_hc_fields.py
?? _tmp_hc_orig.py
?? _tmp_mg_audit.py
?? _tmp_mg_audit2.py
?? _tmp_mg_audit3.py
?? _tmp_mg_audit4.py
?? _tmp_mg_audit5.py
?? _tmp_mg_audit6.py
?? _tmp_score_review.py
?? _tmp_snack_orig.py
?? _tmp_snack_review.py
?? _tmp_tink_detail.py
?? _tmp_v8_analysis.py
?? _tmp_v8_check.py
?? _tmp_v8_zinc.py
?? _verify_out.txt
?? affected_set_spine.json
?? bari-web/dev-server-err.log
?? bari-web/dev-server.log
?? bari-web/e2e/magnesium-geometry.spec.ts
?? bari-web/e2e/screenshots/
?? bari-web/e2e/task384-geometry.spec.ts
?? bari-web/geo_content.cjs
?? bari-web/geo_expand.cjs
?? bari-web/geo_full.cjs
?? bari-web/geo_leakage.cjs
?? bari-web/geo_rowhead.cjs
?? bari-web/geo_test.cjs
?? bari-web/geo_test.mjs
?? bari-web/geo_test2.cjs
?? bari-web/geo_test3.cjs
?? bari-web/mag_mobile_390.png
?? bari-web/magnesium-geometry.png
?? bari-web/scripts/measure-dom-structure.mjs
?? bari-web/scripts/measure-granola-geometry.mjs
?? bari-web/scripts/measure-header-breakdown.mjs
?? bari-web/scripts/measure-magnesium-geometry.mjs
?? bari-web/scripts/measure-rows-detail.mjs
?? bari-web/server-err.txt
?? bari-web/server-out.txt
?? bari-web/server.log
?? bari-web/src/app/blog/sugar-alcohols/
?? bari-web/src/app/hashvaot/chocolate-bars/
?? bari-web/src/app/hashvaot/chocolate-tablets/
?? bari-web/src/app/hashvaot/magnesium/
?? bari-web/src/app/hashvaot/supplements/
?? bari-web/src/components/blog/sugar-alcohols-article.tsx
?? bari-web/src/components/blog/sugar-alcohols-chart1.tsx
?? bari-web/src/components/blog/sugar-alcohols-chart2.tsx
?? bari-web/src/components/blog/sugar-alcohols-efsa-card.tsx
?? bari-web/src/components/blog/sugar-alcohols-front-vs-back.tsx
?? bari-web/src/components/comparisons/chocolate-bars-comparison-page.tsx
?? bari-web/src/components/comparisons/chocolate-tablets-comparison-page.tsx
?? bari-web/src/components/comparisons/magnesium-comparison-page.tsx
?? bari-web/src/components/hashvaot/featured-chocolate-bars-intelligence-card.tsx
?? bari-web/src/components/hashvaot/featured-chocolate-tablets-intelligence-card.tsx
?? bari-web/src/components/hashvaot/featured-magnesium-intelligence-card.tsx
?? bari-web/src/components/shared/magnesium-badge-grid.tsx
?? bari-web/src/components/shared/magnesium-safety-box.tsx
?? bari-web/src/data/comparisons/bread_frontend_v2_gates_report.md
?? bari-web/src/data/comparisons/bread_frontend_v3_gates_report.md
?? bari-web/src/data/comparisons/brined_cheeses_frontend_v2_gates_report.md
?? bari-web/src/data/comparisons/cakes_hard_cookies_frontend_v1_gates_report.md
?? bari-web/src/data/comparisons/cheese_frontend_v4_gates_report.md
?? bari-web/src/data/comparisons/chocolate_bars_frontend_v1.json
?? bari-web/src/data/comparisons/chocolate_tablets_frontend_v1.json
?? bari-web/src/data/comparisons/chocolate_tablets_frontend_v1_gates_report.md
?? bari-web/src/data/comparisons/cookies_coffee_frontend_v2_gates_report.md
?? bari-web/src/data/comparisons/granola_frontend_v1_gates_report.md
?? bari-web/src/data/comparisons/granola_frontend_v2.json
?? bari-web/src/data/comparisons/hard_cheeses_frontend_v2_gates_report.md
?? bari-web/src/data/comparisons/hummus_frontend_v5_gates_report.md
?? bari-web/src/data/comparisons/juices_frontend_v3_gates_report.md
?? bari-web/src/data/comparisons/milk_frontend_v1_gates_report.md
?? bari-web/src/data/comparisons/protein_combined_frontend_v2_gates_report.md
?? bari-web/src/data/comparisons/snacks_frontend_v2_gates_report.md
?? bari-web/src/data/comparisons/snacks_frontend_v3_gates_report.md
?? bari-web/src/lib/blog/sugar-alcohols-article-content.ts
?? bari-web/src/lib/comparisons/chocolate-bars-comparison-page-data.ts
?? bari-web/src/lib/comparisons/chocolate-bars-shelf-filters.ts
?? bari-web/src/lib/comparisons/chocolate-tablets-comparison-page-data.ts
?? bari-web/src/lib/comparisons/chocolate-tablets-shelf-filters.ts
?? bari-web/src/lib/comparisons/magnesium-page-data.ts
?? bari-web/tmp_dev_log.txt
?? bari-web/tmp_shots/hashvaot_index_mobile.png
?? bari-web/tmp_shots/mag_mobile_0scroll.png
?? bari-web/tmp_shots/mag_visual_check.cjs
?? bari-web/tmp_shots/oxide_safety_check.cjs
?? bari-web/tmp_shots/oxide_safety_visible.png
?? bari-web/tmp_shots/supp_check.cjs
?? bari-web/tmp_shots/supplements_index.png
?? bari-web/verify-magnesium-clamp.js
?? check_cc_bsip0.py
?? check_cc_carbs.py
?? check_cc_remaining.py
?? check_milk_carbs.py
?? check_remaining_cheese_brined_cereals.py
?? check_unknown_carbs.py
?? check_unknown_carbs_v2.py
?? content_voice/tone_briefs/
?? dev_server_log.txt
?? diag_task371_step1.py
?? integrations/clients/lnhpd.py
?? integrations/clients/tga.py
?? pb_head_tmp.json
?? qa_deep_check.py
?? qa_leakage_voice.py
?? qa_number_fidelity.py
?? qa_superlative_check.py
?? "research/Magnesium Oral Supplements Worldwide Benchmark.pdf"
?? scan_sugar_null.py
?? scan_sugar_null_v2.py
?? tasks/TASK-349.md
?? tasks/TASK-357.md
?? tasks/TASK-358.md
?? tasks/TASK-359.md
?? tasks/TASK-361.md
?? tasks/TASK-361A.md
?? tasks/TASK-364.md
?? tasks/TASK-365.md
?? tasks/TASK-366.md
?? tasks/TASK-367.md
?? tasks/TASK-368.md
?? tasks/TASK-369.md
?? tasks/TASK-370.md
?? tasks/TASK-372.md
?? tasks/TASK-373.md
?? tasks/TASK-379.md
?? tasks/TASK-380.md
?? tasks/TASK-383.md
?? tasks/TASK-384.md
?? tasks/TASK-384A.md
?? tasks/TASK-385.md
?? tasks/TASK-386.md
?? tasks/TASK-387.md
?? tasks/TASK-389.md
?? tasks/TASK-390.md
?? tasks/TASK-391.md
?? tasks/_scratch_mag_labels/
?? tasks/_scratch_naturalness_badges.py
?? tasks/_scratch_naturalness_check.py
?? tasks/_scratch_naturalness_result.json
?? tasks/_scratch_verdict_audit.py
?? tasks/_scratch_verdict_len.py
?? tasks/_task371_layer1_diagnostic.py
?? tasks/_task371_layer1_v2.py
?? tasks/_task371_score_one.py
?? tasks/autonomous_orchestrate.ps1
?? tasks/closed/TASK-388.md
?? tasks/digests/
?? tasks/prompts/P233_c2_goldset_candidate_extract.md
?? tasks/prompts/P234_c3_goldset_methodology_redteam.md
?? tasks/prompts/P235_c1_nutrition_goldset_phase0.md
?? tasks/prompts/P236_c1cursor_goldcheck_harness.md
?? tasks/prompts/P237_c1grok_goldset_seed_encode.md
?? tasks/prompts/P238_c1gemini_goldset_schema_validator_ci.md
?? tasks/prompts/P239_c2_sie_sa_traceability_audit.md
?? tasks/prompts/P240_c3_sie_broaden_sources_research.md
?? tasks/prompts/P241_c2_magnesium_elemental_arithmetic_check.md
?? tasks/prompts/P242_c3_magnesium_benchmark_philosophy_redteam.md
?? tasks/prompts/P243_c2_magnesium_delivery_arithmetic_recheck.md
?? tasks/prompts/P244_c3_eu_magnesium_shelf_hunt.md
?? tasks/prompts/P245_c3_zinc_worldwide_benchmark.md
?? tasks/prompts/P246_c3_magnesium_assumptions_challenge.md
?? tasks/prompts/P280_c3_snacks_challenge.md
?? tasks/prompts/P282_snacks_relief_challenge.md
?? tasks/prompts/P300_c3_magnesium_elemental_challenge.md
?? tasks/prompts/P301_c3_magnesium_recalibration_challenge.md
?? tasks/prompts/P303_c3_magnesium_v3_final_teardown.md
?? tasks/prompts/P304_c3_magnesium_content_gate.md
?? tasks/prompts/P305_c3_magnesium_content_regate.md
?? tasks/prompts/P387_granola_c3_challenge.md
?? tasks/prompts/P388_granola_c3_verify.md
?? tasks/prompts/P389_c3_magnesium_clinical_validity.md
?? tasks/prompts/P392_juices_decite_c3.md
?? tasks/prompts/_done/P283_protein_bars_r3_mechanical.md
?? tasks/prompts/_done/P297_hc_satfat_rule_challenge.md
?? tasks/prompts/_done/P302_c3_magnesium_v3_real_calibration_challenge.md
?? tasks/prompts/_done/P390_granola_decite_c3.md
?? tasks/prompts/_done/P391_cereals_decite_c3.md
?? tasks/returns/P233_return.md
?? tasks/returns/P234_return.md
?? tasks/returns/P239_return.md
?? tasks/returns/P240_return.md
?? tasks/returns/P241_return.md
?? tasks/returns/P242_return.md
?? tasks/returns/P243_return.md
?? tasks/returns/P244_return.md
?? tasks/returns/P245_return.md
?? tasks/returns/P246_return.md
?? tasks/returns/P258_voice_redteam.md
?? tasks/returns/P261_hc_voice_redteam.md
?? tasks/returns/P265_snacks_v3_voice_redteam.md
?? tasks/returns/P268_drift_report.md
?? tasks/returns/P280_return.md
?? tasks/returns/P282_return.md
?? tasks/returns/P297_return.md
?? tasks/returns/P300_return.md
?? tasks/returns/P301_return.md
?? tasks/returns/P302_return.md
?? tasks/returns/P303_return.md
?? tasks/returns/P304_return.md
?? tasks/returns/P305_return.md
?? tasks/returns/P387_return.md
?? tasks/returns/P388_return.md
?? tasks/returns/P389_return.md
?? tasks/returns/P390_return.md
?? tasks/returns/P391_return.md
?? tasks/task368_d4_impact_analysis.py
?? tasks/task368_output.txt
?? test_acceptance.py
```

### Delta

*(no changes detected)*
