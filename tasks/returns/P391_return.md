# Return: P391

> ⚠️ **STATUS: RETURNED-UNVERIFIED.** Raw agent output captured by the router.
> Nothing here is accepted, closed, or true until the ORCHESTRATOR verifies every
> claim against artifacts (Return Contract v1). The router never closes.
> (Law added after P35 was face-value-closed with contradictions inside it.)

| Field | Value |
|---|---|
| Prompt file | `tasks\prompts\P391_cereals_decite_c3.md` |
| Model | `openai/gpt-5.5` |
| Started | 2026-06-24T05:13:56.546837+00:00 |
| Finished | 2026-06-24T05:15:50.477408+00:00 |
| Exit code | 0 |

---

## Output

```
**(a) Intro**
Ship after tightening line 1. It is stronger than a generic methodology open and readable in one pass, but line 1 is still a little broad/expected.

Sharper line 1:
`רוב דגני הבוקר כאן מוכרים דגן מלא, סיבים וויטמינים — אבל בפועל הרבה מהם מוכרים בעיקר סוכר באריזת בריאות.`

Line 5 is strong and memorable. Keep it.

**(b) New False / Coherence Flags**
1. **#19 EU warning claim: high risk of overstatement.**
`שלושה צבעי מאכל סינתטיים שאסורים בשימוש באירופה ללא אזהרה` reads as if all three named dyes individually require the same EU warning. The Southampton warning applies to specific colors, including Allura Red AC and Sunset Yellow FCF, but **Brilliant Blue is not one of the classic six warning-label colors**.  
Fix:
`שני צבעים מתוך הרשימה מחייבים באירופה אזהרת לייבל על השפעה אפשרית על קשב ילדים; יחד עם צבע סינתטי נוסף זו בחירת רכיבים חריגה למוצר ילדים.`

2. **#16 “רמת הסוכר הגבוהה ביותר בין כל הטבעות” is not verifiable from the provided table.**
If the product-shape mapping confirms all “טבעות” products, it may be true. From the data table alone, it cannot be challenged or confirmed. Safer:
`רמת סוכר גבוהה במיוחד גם בתוך קבוצת הטבעות`

3. **#20 “הבסיס היה יכול להוליד ציון ב-C; הבחירות הורידו אותו ל-E” reads like a scoring counterfactual/apology.**
It implies a hypothetical score path not evidenced by the table and softens the E. Better as a finding:
`הבסיס נראה מבטיח, אבל הבחירות סביבו — סוכר שני, פרוקטוז נוסף, קינמון זניח וצפיפות קלורית חריגה — הן מה שממקם אותו בתחתית.`

**(c) Under-Justified Verdicts**
1. **#5 C is borderline too generous in tone.**
The verdict says “הבסיס עובד” and “מצדיקים את הציפייה,” but sugar is very high for a C-cluster product. It carries the split, but should sharpen the penalty:
`הבסיס עובד, אבל המתיקות לא שולית: סוכר וסירופ גלוקוזה מגיעים מוקדם מדי בשביל מוצר שמנסה להישען על חיטה מלאה.`

2. **#8 C needs a clearer “why not D” signal.**
It says sugar red-label, high sodium, long ingredients; only “הסיבים מחזיקים אותו מעל לתחתית” explains the C. That is probably enough, but glancing consumers may read it as D/E. Add one balancing phrase:
`הדגן והסיבים מצילים אותו מנפילה לתחתית, אבל...`

3. **#20 E carries the grade if the counterfactual is removed.**
The E is justified by sugar second, fructose fifth, cinnamon only 0.6%, highest kcal, high sodium. The current final sentence is the weak point, not the evidence.

**(d) Residual Panel Recitation**
Drop or rephrase:
1. **#7 insightLine:** `9.4 גרם חלבון` should go.  
Fix:
`71% דגנים נשמע טוב; הסוכר רכיב שני ברשימה, והנתרן הגבוה ביותר בין דגני הילדים.`

2. **#14:** `פקאן אמיתי (8.5%) ושקדים (7%)` repeats ingredient percentages, not nutrition-panel numbers. It is probably acceptable because it supports label-vs-reality, but if the new style avoids all numeric clutter, soften:
`פקאן ושקדים אמיתיים ברשימה — יתרון שמגיע עם סוכר, כי הפקאן מגיע מקורמל.`

3. **#15/#16/#20:** Percentages like `2.4%`, `2%`, `0.6%`, `42%` are ingredient-list evidence, not panel recitation. Keep if the page’s rule only bans sugar/protein/fiber/kcal/sodium recitation.

**(e) Hebrew / Naturalness Fixes**
1. **“מקורות סוכר שמוסף”** is awkward. Use:
`מקורות סוכר מוסף` or better `מקורות של סוכר מוסף`.

2. **#6:**  
`שני מקורות סוכר שמוסף בראש הרשימה` → `שני מקורות של סוכר מוסף מוקדם ברשימה`

3. **#9:**  
`חמישה מקורות סוכר שמוסף` → `חמישה מקורות של סוכר מוסף`

4. **#13:**  
`ארבע מקורות` → `ארבעה מקורות`

5. **#5:**  
`עמוק ברשימה` is wrong for third/fourth; they are early, not deep.  
Fix:
`מוקדם ברשימה`

6. **#8:**  
`לפני גיל הבית ספר` is a little odd/colloquial here.  
Fix:
`במוצר שמיועד לילדים צעירים`

7. **#15:**  
`הסוכר הוסף` is grammatical but stiff.  
Fix:
`סוכר נוסף בנפרד כרכיב שלישי`

**(f) Ship / Fix-First**
Fix first, then ship.

Blocking fixes:
1. #19 EU warning overclaim.
2. #20 counterfactual C sentence.
3. #7 residual protein grams.
4. #5 “עמוק ברשימה”.
5. Hebrew agreement/naturalness: `מקורות סוכר מוסף`, `ארבעה מקורות`.

After those, the rewrite is directionally strong: insight-first, less panel-recitation, and mostly grade-coherent.

--- SSE Events ---
  server.connected: {}
  session.created: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "info": {"id": "ses_107f34cd6ffevEjYqkofs0M9eL", "slug": "jolly-tiger", "projectID": "e7f90f8a5abbaca924c7d1983e3ba702c9bbf643", "directory": "C:\\Bari"
  session.next.agent.switched: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cb967001CophiNysciuKu3", "timestamp": "2026-06-24T05:14:04.007Z", "agent": "build"}
  message.updated: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "info": {"id": "msg_ef80cb967001X6zl22TQ0C7ya4", "role": "user", "sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "time": {"created": 1782278044007}, "age
  message.part.updated: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "part": {"type": "text", "text": "You are the independent challenger (ChatGPT). Advice/critique ONLY \u2014 never build, never close. The breakfast-cere
  session.updated: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "info": {"id": "ses_107f34cd6ffevEjYqkofs0M9eL", "slug": "jolly-tiger", "projectID": "e7f90f8a5abbaca924c7d1983e3ba702c9bbf643", "directory": "C:\\Bari"
  session.status: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "status": {"type": "busy"}}
  message.updated: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "info": {"id": "msg_ef80cbb4a001g1xMERcG9m1C1q", "parentID": "msg_ef80cb967001X6zl22TQ0C7ya4", "role": "assistant", "mode": "build", "agent": "build", "
  session.updated: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "info": {"id": "ses_107f34cd6ffevEjYqkofs0M9eL", "slug": "jolly-tiger", "projectID": "e7f90f8a5abbaca924c7d1983e3ba702c9bbf643", "directory": "C:\\Bari"
  session.updated: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "info": {"id": "ses_107f34cd6ffevEjYqkofs0M9eL", "slug": "jolly-tiger", "projectID": "e7f90f8a5abbaca924c7d1983e3ba702c9bbf643", "directory": "C:\\Bari"
  session.diff: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "diff": []}
  message.updated: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "info": {"role": "user", "time": {"created": 1782278044007}, "agent": "build", "model": {"providerID": "openai", "modelID": "gpt-5.5"}, "id": "msg_ef80c
  session.status: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "status": {"type": "busy"}}
  message.part.updated: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "part": {"id": "prt_ef80ccea60017PaDGaVP9VCk6f", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "snapshot
  message.part.updated: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "part": {"id": "prt_ef80ce79d001R8vN6tMN44sIHS", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "type": "
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80ce79d001R8vN6tMN44sIHS", "field": "text", "delta": "**Evaluating answer critique**\n\n
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80ce79d001R8vN6tMN44sIHS", "field": "text", "delta": " think"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80ce79d001R8vN6tMN44sIHS", "field": "text", "delta": " I"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80ce79d001R8vN6tMN44sIHS", "field": "text", "delta": " need"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80ce79d001R8vN6tMN44sIHS", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80ce79d001R8vN6tMN44sIHS", "field": "text", "delta": " focus"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80ce79d001R8vN6tMN44sIHS", "field": "text", "delta": " solely"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80ce79d001R8vN6tMN44sIHS", "field": "text", "delta": " on"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80ce79d001R8vN6tMN44sIHS", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80ce79d001R8vN6tMN44sIHS", "field": "text", "delta": " critique"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80ce79d001R8vN6tMN44sIHS", "field": "text", "delta": " without"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80ce79d001R8vN6tMN44sIHS", "field": "text", "delta": " using"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80ce79d001R8vN6tMN44sIHS", "field": "text", "delta": " any"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80ce79d001R8vN6tMN44sIHS", "field": "text", "delta": " tools"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80ce79d001R8vN6tMN44sIHS", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80ce79d001R8vN6tMN44sIHS", "field": "text", "delta": " Maybe"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80ce79d001R8vN6tMN44sIHS", "field": "text", "delta": " I'll"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80ce79d001R8vN6tMN44sIHS", "field": "text", "delta": " need"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80ce79d001R8vN6tMN44sIHS", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80ce79d001R8vN6tMN44sIHS", "field": "text", "delta": " reason"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80ce79d001R8vN6tMN44sIHS", "field": "text", "delta": " through"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80ce79d001R8vN6tMN44sIHS", "field": "text", "delta": " things"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80ce79d001R8vN6tMN44sIHS", "field": "text", "delta": " manually"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80ce79d001R8vN6tMN44sIHS", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80ce79d001R8vN6tMN44sIHS", "field": "text", "delta": " The"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80ce79d001R8vN6tMN44sIHS", "field": "text", "delta": " user"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80ce79d001R8vN6tMN44sIHS", "field": "text", "delta": " wants"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80ce79d001R8vN6tMN44sIHS", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80ce79d001R8vN6tMN44sIHS", "field": "text", "delta": " answers"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80ce79d001R8vN6tMN44sIHS", "field": "text", "delta": " ranked"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80ce79d001R8vN6tMN44sIHS", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80ce79d001R8vN6tMN44sIHS", "field": "text", "delta": " so"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80ce79d001R8vN6tMN44sIHS", "field": "text", "delta": " I"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80ce79d001R8vN6tMN44sIHS", "field": "text", "delta": " should"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80ce79d001R8vN6tMN44sIHS", "field": "text", "delta": " incorporate"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80ce79d001R8vN6tMN44sIHS", "field": "text", "delta": " that"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80ce79d001R8vN6tMN44sIHS", "field": "text", "delta": " into"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80ce79d001R8vN6tMN44sIHS", "field": "text", "delta": " my"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80ce79d001R8vN6tMN44sIHS", "field": "text", "delta": " process"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80ce79d001R8vN6tMN44sIHS", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80ce79d001R8vN6tMN44sIHS", "field": "text", "delta": " I"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80ce79d001R8vN6tMN44sIHS", "field": "text", "delta": " also"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80ce79d001R8vN6tMN44sIHS", "field": "text", "delta": " need"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80ce79d001R8vN6tMN44sIHS", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80ce79d001R8vN6tMN44sIHS", "field": "text", "delta": " avoid"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80ce79d001R8vN6tMN44sIHS", "field": "text", "delta": " any"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80ce79d001R8vN6tMN44sIHS", "field": "text", "delta": " coding"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80ce79d001R8vN6tMN44sIHS", "field": "text", "delta": " or"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80ce79d001R8vN6tMN44sIHS", "field": "text", "delta": " technical"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80ce79d001R8vN6tMN44sIHS", "field": "text", "delta": " jargon"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80ce79d001R8vN6tMN44sIHS", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80ce79d001R8vN6tMN44sIHS", "field": "text", "delta": " Moreover"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80ce79d001R8vN6tMN44sIHS", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80ce79d001R8vN6tMN44sIHS", "field": "text", "delta": " I"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80ce79d001R8vN6tMN44sIHS", "field": "text", "delta": " should"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80ce79d001R8vN6tMN44sIHS", "field": "text", "delta": " analyze"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80ce79d001R8vN6tMN44sIHS", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80ce79d001R8vN6tMN44sIHS", "field": "text", "delta": " Hebrew"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80ce79d001R8vN6tMN44sIHS", "field": "text", "delta": " copy"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80ce79d001R8vN6tMN44sIHS", "field": "text", "delta": " in"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80ce79d001R8vN6tMN44sIHS", "field": "text", "delta": " comparison"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80ce79d001R8vN6tMN44sIHS", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80ce79d001R8vN6tMN44sIHS", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80ce79d001R8vN6tMN44sIHS", "field": "text", "delta": " data"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80ce79d001R8vN6tMN44sIHS", "field": "text", "delta": " available"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80ce79d001R8vN6tMN44sIHS", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80ce79d001R8vN6tMN44sIHS", "field": "text", "delta": " It's"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80ce79d001R8vN6tMN44sIHS", "field": "text", "delta": " essential"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80ce79d001R8vN6tMN44sIHS", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80ce79d001R8vN6tMN44sIHS", "field": "text", "delta": " get"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80ce79d001R8vN6tMN44sIHS", "field": "text", "delta": " this"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80ce79d001R8vN6tMN44sIHS", "field": "text", "delta": " right"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80ce79d001R8vN6tMN44sIHS", "field": "text", "delta": "!"}
  message.part.updated: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "part": {"id": "prt_ef80ce79d001R8vN6tMN44sIHS", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "type": "
  message.part.updated: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "part": {"id": "prt_ef80d302b0013uZlStmKiWExuC", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "type": "
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": "**Checking superlatives**\n\nI"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " need"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " verify"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " super"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": "l"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": "atives"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " in"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " data"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " For"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " first"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " point"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " both"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " fiber"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " protein"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " are"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " among"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " highest"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " I"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " shouldn"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": "\u2019t"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " rec"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": "ite"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " specific"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " numbers"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " There's"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " false"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " claim"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " about"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " sodium"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " being"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " lowest"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": "\u05e0\u05e7"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": "\u05d9\u05d9\u05d4"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " \u05d9\u05d5\u05ea\u05e8"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": "\""}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " seems"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " acceptable"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " \n\nWhen"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " looking"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " at"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " children's"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " cereals"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " one"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " brand"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " has"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " lowest"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " sodium"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " good"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " protein"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " fiber"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " content"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " Another"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " has"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " highest"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " sodium"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " decent"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " protein"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " Lastly"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " I"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " should"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " clarify"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " what"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " meant"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " by"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": "rings"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " whether"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " they"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " include"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " honey"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " rings"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " other"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": " variations"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d302b0013uZlStmKiWExuC", "field": "text", "delta": "."}
  message.part.updated: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "part": {"id": "prt_ef80d302b0013uZlStmKiWExuC", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "type": "
  message.part.updated: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "part": {"id": "prt_ef80d4804001HKa9RC3AXUarvR", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "type": "
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": "**Assessing product data**\n\nI"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " see"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " that"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " Sug"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": "28"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " higher"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " than"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " #"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": "17"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " at"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " 25"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": "6"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " it"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " might"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " be"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " relevant"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " note"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " #"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": "20"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " as"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " squares"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " rings"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " I"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " think"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " if"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " all"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " rings"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " include"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " #"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": "12"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " #"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": "16"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " #"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": "17"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " then"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " #"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": "16"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " could"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " be"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " considered"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " high"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " as"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " well"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " However"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " phrase"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": "\u05db\u05dc"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " \u05d4\u05d8"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": "\u05d1\u05e2"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": "\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " \u05e9\u05d1"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": "\u05e1\u05e7"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": "\u05d9\u05e8\u05d4"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": "\""}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " suggests"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " I"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " need"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " clear"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " taxonomy"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " product"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " shapes"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " which"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " isn"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": "\u2019t"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " present"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " in"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " current"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " data"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " I"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " should"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " flag"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " any"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " unsupported"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " claims"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " from"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " table"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " unless"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " source"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " can"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " confirm"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": " them"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d4804001HKa9RC3AXUarvR", "field": "text", "delta": "."}
  message.part.updated: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "part": {"id": "prt_ef80d4804001HKa9RC3AXUarvR", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "type": "
  message.part.updated: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "part": {"id": "prt_ef80d52300019fwsqsI5uDFD1g", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "type": "
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "("}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "a"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ")"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " Intro"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "**\n"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "Ship"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " after"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " tightening"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " line"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " It"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " stronger"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " than"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " generic"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " methodology"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " open"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " readable"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " in"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " one"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " pass"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " line"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " still"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " little"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " broad"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "expected"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "Sharper"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " line"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ":\n"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "`"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05e8"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d5\u05d1"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d3"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d2"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05e0\u05d9"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d4\u05d1"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d5\u05e7\u05e8"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05db\u05d0\u05df"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05de\u05d5\u05db"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05e8\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d3"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d2\u05df"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05de\u05dc\u05d0"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05e1"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d9\u05d1\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d5"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d5\u05d9\u05d8"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05de"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d9\u05e0\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u2014"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d0\u05d1\u05dc"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d1\u05e4"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d5\u05e2\u05dc"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d4\u05e8\u05d1\u05d4"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05de\u05d4\u05dd"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05de\u05d5\u05db"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05e8\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d1\u05e2\u05d9\u05e7\u05e8"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05e1"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d5\u05db\u05e8"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d1\u05d0\u05e8"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d9\u05d6"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05ea"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d1\u05e8"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d9\u05d0\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ".`"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\n\n"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "Line"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "5"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " strong"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " memorable"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " Keep"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " it"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "("}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "b"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ")"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " New"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " False"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " /"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " Co"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "herence"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " Flags"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "**\n"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "#"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "19"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " EU"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " warning"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " claim"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " high"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " risk"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " of"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " over"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "statement"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "**\n"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "`"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05e9\u05dc"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d5\u05e9\u05d4"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05e6\u05d1\u05e2"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d9"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05de\u05d0"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05db\u05dc"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05e1"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d9\u05e0\u05ea"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d8"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d9\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05e9\u05d0"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05e1"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d5\u05e8\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d1\u05e9"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d9\u05de\u05d5\u05e9"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d1\u05d0"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d9\u05e8"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d5\u05e4\u05d4"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05dc\u05dc\u05d0"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d0"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d6\u05d4"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05e8\u05d4"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "`"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " reads"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " as"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " if"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " all"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " three"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " named"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " dyes"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " individually"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " require"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " same"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " EU"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " warning"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " The"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " Southampton"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " warning"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " applies"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " specific"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " colors"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " including"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " All"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "ura"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " Red"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " AC"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " Sunset"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " Yellow"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " F"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "CF"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "Br"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "illiant"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " Blue"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " one"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " of"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " classic"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " six"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " warning"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "-label"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " colors"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "  \n"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "Fix"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ":\n"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "`"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05e9"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05e0\u05d9"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05e6\u05d1\u05e2"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05de\u05ea\u05d5\u05da"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d4\u05e8\u05e9"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d9\u05de\u05d4"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05de\u05d7"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d9\u05d9\u05d1"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d1\u05d0"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d9\u05e8"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d5\u05e4\u05d4"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d0"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d6\u05d4"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05e8\u05ea"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05dc"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d9\u05d9\u05d1"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05dc"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05e2\u05dc"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d4\u05e9"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05e4"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05e2\u05d4"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d0\u05e4\u05e9\u05e8"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d9\u05ea"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05e2\u05dc"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05e7\u05e9"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d1"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d9\u05dc\u05d3\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ";"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d9\u05d7\u05d3"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05e2\u05dd"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05e6\u05d1\u05e2"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05e1"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d9\u05e0\u05ea"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d8\u05d9"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05e0\u05d5\u05e1\u05e3"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d6\u05d5"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d1\u05d7"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d9\u05e8\u05ea"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05e8\u05db"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d9\u05d1\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d7\u05e8"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d9\u05d2\u05d4"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05dc\u05de"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d5\u05e6\u05e8"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d9\u05dc\u05d3\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ".`"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\n\n"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "#"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "16"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05e8"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05de\u05ea"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d4\u05e1"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d5\u05db\u05e8"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d4\u05d2\u05d1"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d5\u05d4"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d4"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d1\u05d9\u05d5\u05ea\u05e8"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d1\u05d9\u05df"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05db\u05dc"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d4\u05d8"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d1\u05e2"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " ver"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "ifiable"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " from"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " provided"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " table"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "**\n"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "If"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " product"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "-sh"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "ape"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " mapping"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " confirms"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " all"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d8"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d1\u05e2"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " products"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " it"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " may"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " be"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " true"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " From"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " data"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " table"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " alone"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " it"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " cannot"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " be"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " challenged"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " or"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " confirmed"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " Sa"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "fer"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ":\n"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "`"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05e8"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05de\u05ea"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05e1"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d5\u05db\u05e8"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d2\u05d1\u05d5\u05d4\u05d4"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d1\u05de\u05d9\u05d5\u05d7\u0
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d2\u05dd"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d1\u05ea\u05d5\u05da"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05e7\u05d1\u05d5\u05e6"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05ea"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d4\u05d8"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d1\u05e2"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "`\n\n"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "3"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "#"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "20"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d4"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d1\u05e1"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d9\u05e1"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d4\u05d9\u05d4"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d9\u05db\u05d5\u05dc"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05dc\u05d4"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d5\u05dc"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d9\u05d3"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05e6"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d9\u05d5\u05df"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d1"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "-C"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ";"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d4\u05d1\u05d7"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d9\u05e8\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d4\u05d5\u05e8"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d9\u05d3"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d5"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d0\u05d5\u05ea\u05d5"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05dc"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "-E"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " reads"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " like"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " scoring"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " counter"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "f"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "actual"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "/ap"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "ology"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "**\n"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "It"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " implies"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " hypothetical"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " score"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " path"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " evidenced"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " by"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " table"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " soft"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "ens"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " E"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " Better"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " as"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " finding"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ":\n"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "`"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d4"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d1\u05e1"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d9\u05e1"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05e0\u05e8\u05d0\u05d4"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05de\u05d1"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d8"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d9\u05d7"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d0\u05d1\u05dc"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d4\u05d1\u05d7"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d9\u05e8\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05e1\u05d1\u05d9\u05d1"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d5"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u2014"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05e1"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d5\u05db\u05e8"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05e9\u05e0\u05d9"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05e4\u05e8"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d5\u05e7\u05d8"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d5\u05d6"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05e0\u05d5\u05e1\u05e3"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05e7\u05d9\u05e0"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05de\u05d5\u05df"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d6"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05e0"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d9\u05d7"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d5\u05e6"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05e4"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d9\u05e4\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05e7\u05dc"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d5\u05e8"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d9\u05ea"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d7\u05e8"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d9\u05d2\u05d4"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u2014"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d4\u05df"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05de\u05d4"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05e9\u05de"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05de\u05e7"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05dd"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d0\u05d5\u05ea\u05d5"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d1\u05ea"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d7\u05ea"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d9\u05ea"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ".`"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\n\n"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "("}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "c"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ")"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " Under"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "Just"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "ified"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " Verdict"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "s"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "**\n"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "#"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "5"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " C"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " borderline"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " too"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " generous"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " in"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " tone"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "**\n"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "The"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " verdict"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " says"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d4"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d1\u05e1"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d9\u05e1"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05e2\u05d5\u05d1\u05d3"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05de\u05e6"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d3\u05d9\u05e7"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d0\u05ea"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d4\u05e6"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d9\u05e4"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d9\u05d9\u05d4"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ",\u201d"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " sugar"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " very"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " high"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " C"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "-cl"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "uster"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " product"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " It"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " carries"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " split"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " should"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " sharpen"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " penalty"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ":\n"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "`"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d4"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d1\u05e1"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d9\u05e1"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05e2\u05d5\u05d1\u05d3"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d0\u05d1\u05dc"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d4\u05de\u05ea"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d9\u05e7\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05dc\u05d0"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05e9\u05d5\u05dc"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d9\u05ea"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05e1"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d5\u05db\u05e8"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d5\u05e1"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d9\u05e8"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d5\u05e4"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d2\u05dc"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d5\u05e7"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d5\u05d6"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d4"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05de\u05d2\u05d9\u05e2"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05de\u05d5\u05e7"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d3\u05dd"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05de\u05d3\u05d9"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d1\u05e9\u05d1\u05d9\u05dc"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05de\u05d5\u05e6\u05e8"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05e9\u05de"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05e0\u05e1\u05d4"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05dc\u05d4"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d9\u05e9"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05e2\u05df"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05e2\u05dc"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d7"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d9\u05d8\u05d4"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05de\u05dc\u05d0\u05d4"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ".`"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\n\n"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "#"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "8"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " C"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " needs"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " clearer"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "why"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " D"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " signal"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "**\n"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "It"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " says"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " sugar"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " red"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "-label"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " high"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " sodium"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " long"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " ingredients"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ";"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " only"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d4"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05e1"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d9\u05d1\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05de\u05d7"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d6"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d9\u05e7\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d0\u05d5\u05ea\u05d5"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05de\u05e2\u05dc"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05dc\u05ea"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d7\u05ea"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d9\u05ea"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " explains"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " C"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " That"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " probably"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " enough"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " gl"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "ancing"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " consumers"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " may"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " read"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " it"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " as"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " D"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "/E"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " Add"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " one"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " balancing"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " phrase"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ":\n"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "`"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d4"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d3"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d2\u05df"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d5\u05d4"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05e1"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d9\u05d1\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05de\u05e6"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d9\u05dc\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d0\u05d5\u05ea\u05d5"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05de\u05e0"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05e4"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d9\u05dc\u05d4"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05dc\u05ea"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d7\u05ea"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d9\u05ea"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d0\u05d1\u05dc"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "..."}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "`\n\n"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "3"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "#"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "20"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " E"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " carries"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " grade"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " if"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " counter"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "f"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "actual"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " removed"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "**\n"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "The"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " E"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " justified"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " by"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " sugar"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " second"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " fruct"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "ose"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " fifth"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " cinnamon"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " only"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "0"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "6"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "%,"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " highest"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " kcal"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " high"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " sodium"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " The"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " current"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " final"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " sentence"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " weak"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " point"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " evidence"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "("}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "d"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ")"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " Resid"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "ual"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " Panel"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " Rec"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "itation"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "**\n"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "Drop"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " or"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " re"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "phrase"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ":\n"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "#"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "7"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " insight"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "Line"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ":**"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "9"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "4"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d2\u05e8"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05dd"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d7"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05dc\u05d1"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d5\u05df"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "`"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " should"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " go"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "  \n"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "Fix"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ":\n"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "`"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "71"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "%"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d3"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d2"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05e0\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05e0\u05e9"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05de\u05e2"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d8\u05d5\u05d1"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ";"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d4\u05e1"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d5\u05db\u05e8"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05e8\u05db"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d9\u05d1"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05e9\u05e0\u05d9"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d1\u05e8"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05e9"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d9\u05de\u05d4"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d5\u05d4"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05e0\u05ea"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05e8\u05df"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d4\u05d2\u05d1"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d5\u05d4"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d1\u05d9\u05d5\u05ea\u05e8"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d1\u05d9\u05df"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d3"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d2"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05e0\u05d9"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d4\u05d9\u05dc\u05d3\u05d9\u0
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ".`"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\n\n"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "#"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "14"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ":**"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05e4\u05e7"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d0\u05df"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d0\u05de"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d9\u05ea\u05d9"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " ("}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "8"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "5"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "%)"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d5\u05e9"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05e7"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d3\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " ("}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "7"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "%)"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "`"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " repeats"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " ingredient"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " percentages"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " nutrition"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "-panel"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " numbers"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " It"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " probably"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " acceptable"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " because"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " it"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " supports"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " label"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "-v"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "s"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "-re"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "ality"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " if"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " new"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " style"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " avoids"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " all"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " numeric"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " clutter"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " soften"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ":\n"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "`"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05e4\u05e7"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d0\u05df"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d5\u05e9"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05e7"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d3\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d0\u05de"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d9\u05ea"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d9\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d1\u05e8"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05e9"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d9\u05de\u05d4"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u2014"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d9\u05ea\u05e8"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d5\u05df"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05e9\u05de"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d2\u05d9\u05e2"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05e2\u05dd"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05e1"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d5\u05db\u05e8"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05db\u05d9"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d4\u05e4"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05e7"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d0\u05df"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05de\u05d2\u05d9\u05e2"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05de\u05e7\u05d5\u05e8"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05de\u05dc"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ".`"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\n\n"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "3"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "#"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "15"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "/#"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "16"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "/#"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "20"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ":**"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " Percent"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "ages"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " like"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "4"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "%"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "`,"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "%"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "`,"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "0"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "6"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "%"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "`,"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "42"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "%"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "`"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " are"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " ingredient"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "-list"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " evidence"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " panel"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " rec"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "itation"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " Keep"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " if"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " page"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u2019s"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " rule"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " only"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " bans"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " sugar"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "/pro"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "tein"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "/f"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "iber"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "/k"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "cal"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "/s"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "odium"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " rec"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "itation"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "("}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "e"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ")"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " Hebrew"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " /"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " Natural"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "ness"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " Fix"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "es"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "**\n"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u201c"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05de\u05e7"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d5\u05e8\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05e1"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d5\u05db\u05e8"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05e9\u05de"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d5\u05e1\u05e3"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " awkward"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " Use"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ":\n"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "`"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05de\u05e7"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d5\u05e8\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05e1"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d5\u05db\u05e8"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05de"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d5\u05e1\u05e3"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "`"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " or"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " better"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05de\u05e7"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d5\u05e8\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05e9\u05dc"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05e1"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d5\u05db\u05e8"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05de"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d5\u05e1\u05e3"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "`.\n\n"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "#"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "6"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ":**"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "  \n"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "`"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05e9"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05e0\u05d9"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05de\u05e7"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d5\u05e8\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05e1"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d5\u05db\u05e8"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05e9\u05de"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d5\u05e1\u05e3"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d1\u05e8\u05d0\u05e9"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d4\u05e8\u05e9"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d9\u05de\u05d4"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "`"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u2192"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05e9"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05e0\u05d9"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05de\u05e7"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d5\u05e8\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05e9\u05dc"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05e1"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d5\u05db\u05e8"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05de"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d5\u05e1\u05e3"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05de\u05d5\u05e7"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d3\u05dd"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d1\u05e8"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05e9"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d9\u05de\u05d4"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "`\n\n"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "3"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "#"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "9"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ":**"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "  \n"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "`"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d7"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05de"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d9\u05e9\u05d4"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05de\u05e7"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d5\u05e8\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05e1"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d5\u05db\u05e8"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05e9\u05de"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d5\u05e1\u05e3"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "`"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u2192"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d7"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05de"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d9\u05e9\u05d4"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05de\u05e7"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d5\u05e8\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05e9\u05dc"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05e1"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d5\u05db\u05e8"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05de"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d5\u05e1\u05e3"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "`\n\n"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "4"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "#"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "13"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ":**"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "  \n"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "`"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d0\u05e8"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d1\u05e2"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05de\u05e7"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d5\u05e8\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "`"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u2192"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d0\u05e8"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d1\u05e2"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d4"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05de\u05e7"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d5\u05e8\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "`\n\n"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "5"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "#"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "5"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ":**"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "  \n"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "`"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05e2\u05de"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d5\u05e7"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d1\u05e8"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05e9"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d9\u05de\u05d4"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "`"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " wrong"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " third"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "/f"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "our"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "th"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ";"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " they"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " are"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " early"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " deep"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "  \n"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "Fix"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ":\n"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "`"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05de\u05d5\u05e7"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d3\u05dd"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d1\u05e8"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05e9"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d9\u05de\u05d4"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "`\n\n"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "6"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "#"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "8"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ":**"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "  \n"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "`"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05dc\u05e4"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05e0\u05d9"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d2\u05d9\u05dc"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d4\u05d1\u05d9\u05ea"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05e1\u05e4\u05e8"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "`"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " little"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " odd"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "col"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "lo"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "quial"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " here"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "  \n"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "Fix"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ":\n"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "`"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d1"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05de"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d5\u05e6\u05e8"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05e9\u05de"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d9"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d5\u05e2\u05d3"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05dc\u05d9\u05dc"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d3\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05e6\u05e2"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d9\u05e8\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "`\n\n"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "7"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "#"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "15"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ":**"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "  \n"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "`"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d4"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05e1"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d5\u05db\u05e8"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d4"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d5\u05e1\u05e3"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "`"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " grammatical"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " stiff"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "  \n"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "Fix"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ":\n"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "`"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05e1"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d5\u05db\u05e8"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05e0\u05d5\u05e1\u05e3"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d1\u05e0"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05e4\u05e8"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d3"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05db\u05e8"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05db"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d9\u05d1"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05e9\u05dc"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d9\u05e9\u05d9"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "`\n\n"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "("}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "f"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ")"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " Ship"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " /"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " Fix"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "First"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "**\n"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "Fix"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " first"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " then"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " ship"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "Blocking"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " fixes"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ":\n"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " #"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "19"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " EU"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " warning"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " over"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "claim"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " #"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "20"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " counter"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "f"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "actual"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " C"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " sentence"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "3"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " #"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "7"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " residual"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " protein"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " grams"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "4"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " #"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "5"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05e2\u05de"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d5\u05e7"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05d1\u05e8"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05e9"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d9\u05de\u05d4"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u201d.\n"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "5"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " Hebrew"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " agreement"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "/n"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "atural"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "ness"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05de\u05e7"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d5\u05e8\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05e1"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d5\u05db\u05e8"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05de"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d5\u05e1\u05e3"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "`,"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d0\u05e8"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d1\u05e2"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d4"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " \u05de\u05e7"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "\u05d5\u05e8\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "`.\n\n"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "After"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " those"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " rewrite"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " direction"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "ally"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " strong"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " insight"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "-first"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " less"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " panel"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "-rec"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "itation"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " mostly"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": " grade"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "-co"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "herent"}
  message.part.delta: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "partID": "prt_ef80d52300019fwsqsI5uDFD1g", "field": "text", "delta": "."}
  message.part.updated: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "part": {"id": "prt_ef80d52300019fwsqsI5uDFD1g", "messageID": "msg_ef80cbb4a001g1xMERcG9m1C1q", "sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "type": "
  message.part.updated: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "part": {"id": "prt_ef80e3e03001D8i6EIKD6SjMZl", "reason": "stop", "snapshot": "e965ea43a1587691cb7d1de98b7dd439d1062d4a", "messageID": "msg_ef80cbb4a00
  message.updated: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "info": {"id": "msg_ef80cbb4a001g1xMERcG9m1C1q", "parentID": "msg_ef80cb967001X6zl22TQ0C7ya4", "role": "assistant", "mode": "build", "agent": "build", "
  message.updated: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "info": {"id": "msg_ef80cbb4a001g1xMERcG9m1C1q", "parentID": "msg_ef80cb967001X6zl22TQ0C7ya4", "role": "assistant", "mode": "build", "agent": "build", "
  session.status: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "status": {"type": "busy"}}
  session.status: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "status": {"type": "idle"}}
  session.idle: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL"}
  session.updated: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "info": {"id": "ses_107f34cd6ffevEjYqkofs0M9eL", "slug": "jolly-tiger", "projectID": "e7f90f8a5abbaca924c7d1983e3ba702c9bbf643", "directory": "C:\\Bari"
  session.diff: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "diff": []}
  message.updated: {"sessionID": "ses_107f34cd6ffevEjYqkofs0M9eL", "info": {"role": "user", "time": {"created": 1782278044007}, "agent": "build", "model": {"providerID": "openai", "modelID": "gpt-5.5"}, "summary": {"dif
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
 M bari-web/src/lib/blog/blog-index-content.ts
 M bari-web/src/lib/comparisons/cereals-page-data.ts
 M bari-web/src/lib/comparisons/granola-page-data.ts
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
?? 02_products/chocolate/score_choc_task362_20260621_114229_manifest.json
?? 02_products/chocolate/score_choc_task362_20260621_114707_manifest.json
?? 02_products/chocolate/score_choc_task362_20260621_114832_manifest.json
?? 02_products/chocolate/score_chocolate_task362.py
?? 02_products/chocolate/victory_branch_captured.json
?? 02_products/chocolate/victory_branch_found.json
?? 02_products/chocolate/victory_v2_raw.json
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
?? affected_set_spine.json
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
?? bari-web/tmp_shots/hashvaot_index_mobile.png
?? bari-web/tmp_shots/mag_mobile_0scroll.png
?? bari-web/tmp_shots/mag_visual_check.cjs
?? bari-web/tmp_shots/oxide_safety_check.cjs
?? bari-web/tmp_shots/oxide_safety_visible.png
?? bari-web/tmp_shots/supp_check.cjs
?? bari-web/tmp_shots/supplements_index.png
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
?? tasks/prompts/P391_cereals_decite_c3.md
?? tasks/prompts/_done/P283_protein_bars_r3_mechanical.md
?? tasks/prompts/_done/P297_hc_satfat_rule_challenge.md
?? tasks/prompts/_done/P302_c3_magnesium_v3_real_calibration_challenge.md
?? tasks/prompts/_done/P390_granola_decite_c3.md
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
 M bari-web/src/lib/blog/blog-index-content.ts
 M bari-web/src/lib/comparisons/cereals-page-data.ts
 M bari-web/src/lib/comparisons/granola-page-data.ts
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
?? 02_products/chocolate/score_choc_task362_20260621_114229_manifest.json
?? 02_products/chocolate/score_choc_task362_20260621_114707_manifest.json
?? 02_products/chocolate/score_choc_task362_20260621_114832_manifest.json
?? 02_products/chocolate/score_chocolate_task362.py
?? 02_products/chocolate/victory_branch_captured.json
?? 02_products/chocolate/victory_branch_found.json
?? 02_products/chocolate/victory_v2_raw.json
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
?? affected_set_spine.json
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
?? bari-web/tmp_shots/hashvaot_index_mobile.png
?? bari-web/tmp_shots/mag_mobile_0scroll.png
?? bari-web/tmp_shots/mag_visual_check.cjs
?? bari-web/tmp_shots/oxide_safety_check.cjs
?? bari-web/tmp_shots/oxide_safety_visible.png
?? bari-web/tmp_shots/supp_check.cjs
?? bari-web/tmp_shots/supplements_index.png
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
?? tasks/prompts/P391_cereals_decite_c3.md
?? tasks/prompts/_done/P283_protein_bars_r3_mechanical.md
?? tasks/prompts/_done/P297_hc_satfat_rule_challenge.md
?? tasks/prompts/_done/P302_c3_magnesium_v3_real_calibration_challenge.md
?? tasks/prompts/_done/P390_granola_decite_c3.md
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
?? tasks/task368_d4_impact_analysis.py
?? tasks/task368_output.txt
?? test_acceptance.py
```

### Delta

*(no changes detected)*
