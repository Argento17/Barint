# Return: P390

> ⚠️ **STATUS: RETURNED-UNVERIFIED.** Raw agent output captured by the router.
> Nothing here is accepted, closed, or true until the ORCHESTRATOR verifies every
> claim against artifacts (Return Contract v1). The router never closes.
> (Law added after P35 was face-value-closed with contradictions inside it.)

| Field | Value |
|---|---|
| Prompt file | `tasks\prompts\P390_granola_decite_c3.md` |
| Model | `openai/gpt-5.5` |
| Started | 2026-06-23T19:10:24.453509+00:00 |
| Finished | 2026-06-23T19:11:56.149549+00:00 |
| Exit code | 0 |

---

## Output

```
**(a) Intro Verdict**
The new intro is stronger than the prior direction: clearer stakes, concrete distribution, and a useful “same shelf, big gap” frame. It passes the one-read test better.

Still, line 1 is not sharp enough. It says something true, but “נבנה על שמן, ממתיק ופריכות” is a little abstract and soft. It critiques the category, but does not yet create the immediate consumer jolt.

Sharper line 1 option:

> גרנולה נראית כמו ארוחת בוקר בריאה — אבל על המדף היא הרבה פעמים דגנים עם שמן, סירופ ופירות מסוכרים.

Why stronger: it names the consumer illusion, uses plain shelf language, and lands the core pattern without sounding slogan-like.

Line 4 also has a small wording issue: “השמן שמציעים” sounds odd. Better:

> מה שמפריד בין B ל-D הוא לא האריזה: זה סוג השמן, סוג הממתיק, והאם הפירות כבר הגיעו מסוכרים.

**(b) Under-Justified Verdicts**
Rank 5, C: mostly lands, but “שומן גבוה” and “צפיפות” may feel abstract without kcal/fat numbers. The inversion is important and should be a touch more explicit.

One-line fix:
> הסוכר נמוך כי אין סוכר מוסף, אבל האגוזים, הזרעים והטחינה מרימים מאוד את צפיפות האנרגיה — לכן זו גרנולה נקייה, לא בהכרח קלה.

Rank 6, C: under-justified for a glancing consumer. It lists issues, but does not clearly explain why a high-protein, 55% oats product stays C rather than B.

One-line fix:
> החלבון והשיבולת עובדים לטובתה, אבל שמן בתוך החמוציות, כמה ממתיקים ורשימה ארוכה משאירים אותה באמצע המדף.

Rank 8, C: slightly under-justified. “סופרפוד בשם” is good, but the grade rationale depends on implied average bars. Needs one clearer grade anchor.

One-line fix:
> השם נשמע פרימיום, אבל בפועל יש כאן סילאן, רכז תפוחים, פצפוצי אורז ותמצית טעם — מספיק כדי להשאיר אותה ב-C.

Rank 10, C: close to under-justified. It explains the C, but “חלבון גבוה” plus 51% oats plus nuts may make C feel harsh unless the sugar/list-length penalty is made more decisive.

One-line fix:
> הבסיס טוב, אבל החלבון מגיע מתוספת סויה, והרשימה הארוכה עם שני ממתיקים מונעת ממנה לטפס ל-B.

Rank 11, C: justified. Sugar bar is 15.6, so “צפופה ומתוקה מהממוצע” feels earned.

Rank 12, C: justified, but “וזה כל הטוב שיש” is a bit too absolute. It may read more editorial than evidentiary.

One-line fix:
> שוקולד מריר אמיתי 7.5% הוא נקודת הזכות המרכזית — אבל סוכר חום כרכיב שני, שמן צמחי ופצפוצי אורז מושכים אותה למטה.

Rank 13, D inversion: lands well. The “low sugar but D” explanation is clear enough without numbers. I would soften “הרכיבים המעובדים הם הציון” because it sounds like a slogan rather than causal explanation.

One-line fix:
> לכן הסוכר הנמוך לא מציל את המוצר: העיבוד, השומנים והתוספים הם מה שמחזיק אותו ב-D.

**(c) Over-Attribution / Coherence Flags**
Rank 3: “צפופה ומתוקה מהממוצע” is borderline. Sugar 11.9 is not especially high versus the category, and score is B. “מתוקה מהממוצע” may overstate if the visible sugar bar looks mid-range.

Fix:
> זו עדיין גרנולה צפופה יחסית, עם מייפל כרכיב מרכזי — גם אם הרשימה נאה יותר מרוב המדף.

Rank 4: “שיא הסיבים בקטגוריה” conflicts with rank 1 saying “מובילה בסיבים במדף” unless both are somehow true on different definitions. This needs one winner only.

Fix:
> סיבים גבוהים מאוד בקטגוריה

Rank 5: “זה מה שמוריד ל-C” may over-attribute if sodium also matters. The rowVerdict mentions salt/נתרן, so the insightLine should not imply density alone explains everything.

Fix:
> וזה חלק גדול ממה שמשאיר אותה ב-C.

Rank 7: “הנדסת מרכיבים, לא דגן שלם” risks sounding like processing alone caused C. Since score is still C, not D/E, this is okay but slightly harsh. Also “מהונדס” is loaded.

Fix:
> חיזוק מרכיבים, לא יתרון שמגיע מהדגן עצמו.

Rank 12: “מאפה מתוק שמחופש לגרנולה” is rhetorically strong but may be too accusatory for a C product, especially with sugar 13.4, not D/E territory. It risks over-punishing.

Fix:
> יותר מוצר דגנים מתוק מגרנולה נקייה.

Rank 20: coherent. Sugar bar highest, E, two sweeteners, preservative. No issue.

Rank 21: “כל הפירות... מסוכרים בנפרד עם חומרי שימור” is strong but okay if label-true. No contradiction with E.

Rank 22: coherent, but “הנמוכה ביותר בקטגוריה” is score-based and visible; fine.

**(d) Repetition Fixes**
The [1]/[9] “עולש מוסף + רכז תפוחים” repetition is noticeable because the structure is nearly identical. Since the facts are the same, keep both facts but vary the angle.

For [1]:
> הסיבים הגבוהים נראים מרשימים, אבל חלק משמעותי מהם מגיע מעולש מוסף; גם החמוציות לא מגיעות נקיות, אלא עם רכז תפוחים.

For [9]:
> אגוזים וסיבים נותנים לה פתיחה טובה, אבל מאחורי הסיבים יש עולש מוסף, ומאחורי החמוציות יש רכז תפוחים.

“מהונדס/הנדסה” appears too often and can start to feel like a house tic. Keep it where it matters most, especially [13], but vary [1], [2], [7].

Suggested swaps:
[1] “הנדסת סיבים בפועל” → “סיבים מחוזקים, לא יתרון טבעי של הדגן.”
[2] “בידוד תעשייתי” is enough; no need for another engineering phrase.
[7] “הרכב מהונדס” → “הרכב מחוזק בתוספים חלבוניים ושומניים.”

[21]/[22] “שתי שכבות” repetition is acceptable because both products apparently have layered processed structures, but [22] should not echo [21] too closely.

For [22]:
> כאן הבעיה מצטברת כבר מהבסיס: שמן דקלים, סירופ גלוקוז וסוכר חום — ואז פירות מסוכרים מעל.

**(e) Remaining Translationese / Hebrew Issues**
“השמן שמציעים” in intro line 4 is unnatural. Use “סוג השמן”.

“חלבון ממשי” in [4] sounds slightly odd. Better: “חלבון גבוה” or “מקור חלבון משמעותי”.

“מהגבוהים בחלבון” in [7] is understandable but stiff. Better: “מהמוצרים העשירים בחלבון בקטגוריה”.

“שני שכבות” in [21] should be “שתי שכבות”.

“חומר משמר על הפירות היבשים” in [20] is understandable but a little compressed. Better: “חומר משמר שמופיע עם הפירות היבשים”.

“ממתיק מונק-פרוט במקום מלאכותי” in [3] may be confusing. It implies “not artificial” as a virtue, but consumers may not know what monk fruit is. Better:
> ממתיק מונק-פרוט במקום ממתיק מלאכותי נפוץ

**Ship / Fix-First**
Fix-first, but not because the rewrite failed. The copy is broadly in the right direction and much closer to the desired style. The main fixes before ship are:

1. Sharpen intro line 1 and fix “השמן שמציעים”.
2. Strengthen grade rationale for [6], [8], [10], and slightly [5].
3. Remove/soften overstatements in [3], [12], and the possible fiber contradiction in [4].
4. Vary “עולש מוסף + רכז תפוחים” and reduce “מהונדס/הנדסה” recurrence.

Return status: RETURNED for content revision, not closed.

--- SSE Events ---
  server.connected: {}
  session.created: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "info": {"id": "ses_10a1be802ffea3tiiBYz6OBVZP", "slug": "tidy-cabin", "projectID": "e7f90f8a5abbaca924c7d1983e3ba702c9bbf643", "directory": "C:\\Bari",
  session.next.agent.switched: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41d86001eAtz0ehyhrOEFS", "timestamp": "2026-06-23T19:10:28.230Z", "agent": "build"}
  message.updated: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "info": {"id": "msg_ef5e41d86001DSowSCIG0XVeSB", "role": "user", "sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "time": {"created": 1782241828230}, "age
  message.part.updated: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "part": {"type": "text", "text": "You are the independent challenger (ChatGPT). Advice/critique ONLY \u2014 never build, never close. You reviewed this 
  session.updated: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "info": {"id": "ses_10a1be802ffea3tiiBYz6OBVZP", "slug": "tidy-cabin", "projectID": "e7f90f8a5abbaca924c7d1983e3ba702c9bbf643", "directory": "C:\\Bari",
  session.status: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "status": {"type": "busy"}}
  message.updated: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "info": {"id": "msg_ef5e41f3c0018HpdtICC37dWpK", "parentID": "msg_ef5e41d86001DSowSCIG0XVeSB", "role": "assistant", "mode": "build", "agent": "build", "
  session.updated: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "info": {"id": "ses_10a1be802ffea3tiiBYz6OBVZP", "slug": "tidy-cabin", "projectID": "e7f90f8a5abbaca924c7d1983e3ba702c9bbf643", "directory": "C:\\Bari",
  session.diff: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "diff": []}
  message.updated: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "info": {"role": "user", "time": {"created": 1782241828230}, "agent": "build", "model": {"providerID": "openai", "modelID": "gpt-5.5"}, "id": "msg_ef5e4
  session.status: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "status": {"type": "busy"}}
  session.updated: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "info": {"id": "ses_10a1be802ffea3tiiBYz6OBVZP", "slug": "tidy-cabin", "projectID": "e7f90f8a5abbaca924c7d1983e3ba702c9bbf643", "directory": "C:\\Bari",
  message.part.updated: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "part": {"id": "prt_ef5e42ca2001wUL4ubRPlUaxj1", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "snapshot
  message.part.updated: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "part": {"id": "prt_ef5e42e11001sKXGT6T3iEWJpl", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "type": "
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": "**Assessing return block critique*
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": " need"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": " focus"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": " strictly"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": " on"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": " answering"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": " critique"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": " without"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": " using"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": " any"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": " tools"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": " It"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": " seems"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": " like"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": " user"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": " wants"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": " nuanced"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": " answer"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": " that"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": " might"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": " involve"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": " Hebrew"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": " language"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": " elements"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": " They"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": " mentioned"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": " something"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": " about"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": " closing"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": " return"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": " block"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": " possibly"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": " including"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": "fix"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": "-first"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": "\""}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": " approach"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": " The"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": " user's"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": " request"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": " seems"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": " rank"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": " advice"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": " of"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": " challenger"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": " without"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": " closing"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": " off"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": " options"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": " I'll"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": " make"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": " sure"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": " keep"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": " my"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": " response"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": " open"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": " flexible"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e42e11001sKXGT6T3iEWJpl", "field": "text", "delta": "."}
  message.part.updated: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "part": {"id": "prt_ef5e42e11001sKXGT6T3iEWJpl", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "type": "
  message.part.updated: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "part": {"id": "prt_ef5e44a89001Eg4gc9zUXMORMM", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "type": "
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "("}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "a"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ")"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " Intro"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " Verdict"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "**\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "The"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " new"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " intro"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " stronger"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " than"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " prior"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " direction"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " clearer"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " stakes"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " concrete"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " distribution"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " useful"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "same"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " shelf"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " big"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " gap"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " frame"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " It"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " passes"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " one"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "-read"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " test"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " better"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "Still"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " line"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " sharp"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " enough"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " It"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " says"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " something"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " true"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e0"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e0\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05e2\u05dc"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05e9\u05de"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05df"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05de"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05de\u05ea"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05e7"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d5"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e4\u05e8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05db\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " little"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " abstract"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " soft"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " It"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " critiques"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " category"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " does"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " yet"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " create"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " immediate"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " consumer"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " j"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "olt"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "Sharper"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " line"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " option"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ":\n\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ">"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d2\u05e8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e0"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05dc\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05e0"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e8\u05d0"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05ea"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05db\u05de\u05d5"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d0\u05e8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05d7"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05ea"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05e7\u05e8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d1\u05e8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05d0\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u2014"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d0\u05d1\u05dc"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05e2\u05dc"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d4\u05de\u05d3"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e3"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d4\u05d9\u05d0"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d4\u05e8\u05d1\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05e4\u05e2\u05de\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d3"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d2"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e0\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05e2\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05e9\u05de"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05df"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05e1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05e8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05e4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d5\u05e4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05e8\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05de\u05e1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05db"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e8\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "Why"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " stronger"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " it"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " names"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " consumer"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " illusion"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " uses"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " plain"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " shelf"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " language"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " lands"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " core"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " pattern"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " without"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " sounding"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " slogan"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "-like"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "Line"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " also"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " has"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " small"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " wording"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " issue"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d4\u05e9"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05de\u05df"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05e9\u05de"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e6\u05d9\u05e2"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " sounds"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " odd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " Better"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ":\n\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ">"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05de\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05e9\u05de"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e4\u05e8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05d3"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d1\u05d9\u05df"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " B"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05dc"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "-D"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d4\u05d5\u05d0"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05dc\u05d0"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d4\u05d0\u05e8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05d6\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d6\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05e1\u05d5\u05d2"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d4\u05e9"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05de\u05df"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05e1\u05d5\u05d2"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d4\u05de"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05de\u05ea"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05e7"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d5\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d0\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d4\u05e4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05e8\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05db\u05d1\u05e8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d4\u05d2\u05d9\u05e2"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05de\u05e1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05db"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e8\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "("}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "b"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ")"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " Under"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "Just"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "ified"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " Verdict"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "s"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "**\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "Rank"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "5"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " C"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " mostly"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " lands"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e9"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05de\u05df"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d2\u05d1\u05d5\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e6"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05e4\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " may"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " feel"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " abstract"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " without"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " kcal"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "/f"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "at"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " numbers"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " The"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " inversion"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " important"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " should"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " be"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " touch"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " more"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " explicit"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "One"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "-line"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " fix"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ":\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ">"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d4\u05e1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05db\u05e8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05e0\u05de"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05da"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05db\u05d9"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d0\u05d9\u05df"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05e1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05db\u05e8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05de"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05e1\u05e3"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d0\u05d1\u05dc"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d4\u05d0"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d2"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05d6"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d6\u05e8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e2\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d5\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d8\u05d7"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05e0\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05de\u05e8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05de\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05de\u05d0\u05d5\u05d3"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d0\u05ea"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05e6\u05e4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05e4\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d4\u05d0\u05e0"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e8\u05d2"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u2014"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05dc\u05db\u05df"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d6\u05d5"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d2\u05e8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e0"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05dc\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05e0\u05e7"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05d9\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05dc\u05d0"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d1\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05db\u05e8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d7"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05e7"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05dc\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "Rank"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "6"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " C"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " under"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "just"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "ified"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " gl"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "ancing"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " consumer"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " It"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " lists"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " issues"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " does"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " clearly"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " explain"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " why"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " high"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "-pro"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "tein"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "55"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "%"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " oats"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " product"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " stays"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " C"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " rather"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " than"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " B"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "One"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "-line"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " fix"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ":\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ">"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d4\u05d7"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05dc\u05d1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05df"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d5\u05d4\u05e9"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05d1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05dc\u05ea"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05e2\u05d5\u05d1\u05d3\u05d9\u0
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05dc\u05d8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05d1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05ea\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d0\u05d1\u05dc"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05e9\u05de"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05df"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d1\u05ea\u05d5\u05da"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d4\u05d7"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05de"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05e6"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05db\u05de\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05de"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05de\u05ea"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05e7\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d5\u05e8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e9"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05de\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d0\u05e8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05db\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05de\u05e9"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d0"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05e8\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d0\u05d5\u05ea\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d1\u05d0\u05de\u05e6"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e2"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d4\u05de\u05d3"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e3"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "Rank"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " C"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " slightly"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " under"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "just"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "ified"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05e4\u05e8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05d3"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d1\u05e9\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " good"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " grade"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " rationale"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " depends"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " on"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " implied"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " average"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " bars"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " Needs"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " one"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " clearer"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " grade"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " anchor"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "One"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "-line"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " fix"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ":\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ">"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d4\u05e9"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05e0\u05e9"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05de\u05e2"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05e4\u05e8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05de"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05d5\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d0\u05d1\u05dc"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d1\u05e4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05e2\u05dc"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d9\u05e9"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05db\u05d0\u05df"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05e1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05dc"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d0\u05df"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05e8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05db\u05d6"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05ea\u05e4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05d7\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05e4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e6"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05e6"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d0\u05d5\u05e8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d6"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05de\u05e6"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05ea"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e2\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u2014"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05de\u05e1\u05e4\u05d9\u05e7"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05db\u05d3\u05d9"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05dc\u05d4\u05e9"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d0\u05d9\u05e8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d0\u05d5\u05ea\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "-C"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "Rank"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "10"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " C"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " close"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " under"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "just"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "ified"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " It"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " explains"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " C"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d7"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05dc\u05d1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05df"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d2\u05d1\u05d5\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " plus"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "51"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "%"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " oats"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " plus"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " nuts"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " may"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " make"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " C"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " feel"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " harsh"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " unless"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " sugar"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "/list"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "-length"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " penalty"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " made"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " more"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " decisive"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "One"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "-line"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " fix"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ":\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ">"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d4\u05d1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05e1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d8\u05d5\u05d1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d0\u05d1\u05dc"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d4\u05d7"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05dc\u05d1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05df"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05de\u05d2\u05d9\u05e2"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05de\u05ea"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05e1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e4\u05ea"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05e1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05d9\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d5\u05d4\u05e8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e9"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05de\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d4\u05d0\u05e8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05db\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05e2\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05e9\u05e0\u05d9"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05de"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05de\u05ea"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05e7\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05de"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05e0"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e2\u05ea"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05de\u05de"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e0\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05dc\u05d8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e4\u05e1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05dc"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "-B"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "Rank"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "11"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " C"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " justified"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " Sugar"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " bar"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "15"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "6"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " so"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e6"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05e4\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d5\u05de\u05ea"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05e7\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05de\u05d4\u05de"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05de"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05e6"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e2"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " feels"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " earned"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "Rank"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "12"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " C"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " justified"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05d6"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05db\u05dc"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d4\u05d8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05d1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05e9\u05d9\u05e9"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " bit"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " too"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " absolute"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " It"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " may"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " read"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " more"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " editorial"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " than"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " evid"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "enti"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "ary"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "One"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "-line"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " fix"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ":\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ">"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05e9"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05e7"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05dc\u05d3"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05de\u05e8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05e8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d0\u05de"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05ea\u05d9"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "7"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "5"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "%"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d4\u05d5\u05d0"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05e0\u05e7"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05d3\u05ea"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d4\u05d6"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05db\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d4\u05de\u05e8\u05db\u05d6"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05ea"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u2014"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d0\u05d1\u05dc"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05e1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05db\u05e8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d7"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05db\u05e8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05db"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05d1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05e9\u05e0\u05d9"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05e9\u05de"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05df"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05e6"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05de\u05d7"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d5\u05e4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e6"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05e6"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d0\u05d5\u05e8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d6"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05de\u05d5\u05e9"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05db\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d0\u05d5\u05ea\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05dc\u05de"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d8\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "Rank"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "13"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " D"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " inversion"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " lands"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " well"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " The"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "low"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " sugar"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " D"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " explanation"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " clear"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " enough"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " without"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " numbers"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " I"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " would"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " soften"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d4\u05e8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05db"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05d1\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d4\u05de\u05e2"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05d1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d3\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d4\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d4\u05e6"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05d5\u05df"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " because"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " it"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " sounds"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " like"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " slogan"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " rather"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " than"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " causal"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " explanation"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "One"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "-line"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " fix"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ":\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ">"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05dc\u05db\u05df"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d4\u05e1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05db\u05e8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d4\u05e0"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05de"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05da"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05dc\u05d0"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05de\u05e6"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05dc"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d0\u05ea"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d4\u05de"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05e6\u05e8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d4\u05e2"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05d1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05d3"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d4\u05e9"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05de"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e0\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d5\u05d4\u05ea"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05e1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e4\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d4\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05de\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05e9\u05de"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d7\u05d6"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05e7"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d0\u05d5\u05ea\u05d5"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "-D"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "("}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "c"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ")"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " Over"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "At"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "tribution"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " /"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " Co"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "herence"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " Flags"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "**\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "Rank"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "3"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e6"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05e4\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d5\u05de\u05ea"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05e7\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05de\u05d4\u05de"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05de"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05e6"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e2"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " borderline"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " Sugar"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "11"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "9"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " especially"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " high"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " versus"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " category"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " score"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " B"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05de\u05ea"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05e7\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05de\u05d4\u05de"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05de"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05e6"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e2"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " may"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " over"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "state"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " if"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " visible"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " sugar"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " bar"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " looks"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " mid"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "-range"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "Fix"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ":\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ">"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d6\u05d5"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05e2\u05d3\u05d9\u05d9\u05df"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d2\u05e8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e0"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05dc\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05e6\u05e4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05e4\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d9\u05d7\u05e1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05ea"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05e2\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05de"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05d9\u05e4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05dc"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05db\u05e8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05db"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05d1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05de\u05e8\u05db\u05d6"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u2014"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d2\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d0\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d4\u05e8\u05e9"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05de\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05e0"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d0\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d9\u05d5\u05ea\u05e8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05de\u05e8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05d1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d4\u05de\u05d3"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e3"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "Rank"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e9"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05d0"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d4\u05e1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05d1\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e7\u05d8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d2\u05d5\u05e8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " conflicts"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " with"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " rank"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " saying"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05de"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05d1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05dc\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d1\u05e1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05d1\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d1\u05de\u05d3"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e3"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " unless"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " both"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " are"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " somehow"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " true"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " on"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " different"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " definitions"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " This"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " needs"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " one"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " winner"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " only"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "Fix"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ":\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ">"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05e1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05d1\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d2\u05d1\u05d5\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05de\u05d0\u05d5\u05d3"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e7\u05d8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d2\u05d5\u05e8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\n\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "Rank"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "5"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d6\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05de\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05e9\u05de"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05e8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05d3"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05dc"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "-C"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " may"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " over"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "attribute"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " if"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " sodium"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " also"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " matters"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " The"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " row"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "Verd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "ict"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " mentions"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " salt"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e0\u05ea"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e8\u05df"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " so"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " insight"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "Line"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " should"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " imply"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " density"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " alone"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " explains"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " everything"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "Fix"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ":\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ">"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d5\u05d6\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d7\u05dc\u05e7"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d2\u05d3\u05d5\u05dc"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05de"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05de\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05e9\u05de\u05e9"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d0\u05d9\u05e8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d0\u05d5\u05ea\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "-C"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "Rank"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "7"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e0\u05d3"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e1\u05ea"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05de\u05e8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05db"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05d1\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05dc\u05d0"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d3"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d2\u05df"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05e9\u05dc"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " risks"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " sounding"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " like"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " processing"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " alone"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " caused"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " C"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " Since"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " score"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " still"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " C"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " D"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "/E"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " this"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " okay"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " slightly"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " harsh"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " Also"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05de\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05e0\u05d3"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " loaded"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "Fix"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ":\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ">"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d7"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05d6"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05e7"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05de\u05e8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05db"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05d1\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05dc\u05d0"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d9\u05ea\u05e8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05df"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05e9\u05de"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d2\u05d9\u05e2"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05de\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d3"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d2\u05df"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05e2\u05e6\u05de\u05d5"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "Rank"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "12"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05de\u05d0"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e4\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05de\u05ea"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05e7"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05e9\u05de"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d7"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05e4\u05e9"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05dc\u05d2\u05e8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e0"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05dc\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " rhet"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "or"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "ically"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " strong"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " may"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " be"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " too"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " accus"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "atory"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " C"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " product"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " especially"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " with"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " sugar"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "13"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " D"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "/E"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " territory"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " It"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " risks"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " over"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "-p"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "un"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "ishing"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "Fix"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ":\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ">"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d9\u05d5\u05ea\u05e8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05de\u05d5\u05e6\u05e8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d3"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d2"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e0\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05de\u05ea"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05e7"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05de"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d2\u05e8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e0"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05dc\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05e0\u05e7"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05d9\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "Rank"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "20"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " coherent"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " Sugar"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " bar"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " highest"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " E"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " two"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " sweet"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "eners"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " preserv"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "ative"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " No"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " issue"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "Rank"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "21"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05db\u05dc"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d4\u05e4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05e8\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "..."}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05de\u05e1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05db"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e8\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d1\u05e0"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e4\u05e8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d3"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05e2\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d7\u05d5\u05de\u05e8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05e9"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05de"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05e8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " strong"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " okay"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " if"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " label"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "true"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " No"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " contradiction"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " with"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " E"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "Rank"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "22"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " coherent"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e0"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05de"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05db\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d1\u05d9\u05d5\u05ea\u05e8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e7\u05d8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d2\u05d5\u05e8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " score"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "-based"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " visible"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ";"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " fine"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "("}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "d"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ")"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " Re"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "petition"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " Fix"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "es"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "**\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "The"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " ["}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "]/"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "["}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "9"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "]"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e2"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05dc"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e9"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05de"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05e1\u05e3"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " +"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05e8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05db\u05d6"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05ea\u05e4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05d7\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " repetition"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " noticeable"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " because"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " structure"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " nearly"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " identical"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " Since"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " facts"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " are"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " same"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " keep"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " both"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " facts"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " vary"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " angle"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "For"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " ["}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "]:\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ">"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d4\u05e1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05d1\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d4\u05d2\u05d1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05d4\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05e0"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e8\u05d0"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05de\u05e8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e9"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05de\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d0\u05d1\u05dc"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d7\u05dc\u05e7"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05de\u05e9\u05de\u05e2\u05d5\u0
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05de\u05d4\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05de\u05d2\u05d9\u05e2"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05de\u05e2"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05dc"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e9"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05de"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05e1\u05e3"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ";"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d2\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d4\u05d7"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05de"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05e6"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05dc\u05d0"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05de\u05d2\u05d9\u05e2"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05e0\u05e7"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d0\u05dc\u05d0"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05e2\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05e8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05db\u05d6"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05ea\u05e4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05d7\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "For"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " ["}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "9"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "]:\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ">"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d0\u05d2"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05d6"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d5\u05e1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05d1\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05e0\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e0\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05dc\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05e4\u05ea"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05d7\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d8\u05d5\u05d1\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d0\u05d1\u05dc"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05de\u05d0"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d7"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05e8\u05d9"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d4\u05e1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05d1\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d9\u05e9"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05e2"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05dc"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e9"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05de"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05e1\u05e3"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d5\u05de"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d0"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d7"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05e8\u05d9"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d4\u05d7"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05de"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05e6"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d9\u05e9"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05e8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05db\u05d6"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05ea\u05e4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05d7\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u201c"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05de\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05e0\u05d3"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e0\u05d3"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e1\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " appears"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " too"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " often"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " can"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " start"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " feel"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " like"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " house"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " tic"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " Keep"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " it"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " where"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " it"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " matters"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " most"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " especially"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " ["}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "13"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "],"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " vary"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " ["}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "],"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " ["}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "],"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " ["}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "7"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "].\n\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "Suggested"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " swaps"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ":\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "["}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "]"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e0\u05d3"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e1\u05ea"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05e1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05d1\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d1\u05e4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05e2\u05dc"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u2192"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05d1\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05de\u05d7"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05d6"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e7\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05dc\u05d0"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d9\u05ea\u05e8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05df"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d8\u05d1\u05e2"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05e9\u05dc"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d4\u05d3"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d2\u05df"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ".\u201d\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "["}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "]"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05d3"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05d3"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05ea"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e2\u05e9"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05d9\u05ea"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " enough"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ";"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " no"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " need"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " another"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " engineering"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " phrase"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "["}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "7"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "]"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d4\u05e8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05db\u05d1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05de\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05e0\u05d3"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u2192"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d4\u05e8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05db\u05d1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05de\u05d7"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05d6"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e7"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d1\u05ea"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05e1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e4\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d7"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05dc\u05d1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05e0\u05d9\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d5\u05e9"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05de"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e0\u05d9\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ".\u201d\n\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "["}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "21"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "]/"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "["}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "22"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "]"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e9"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05ea\u05d9"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05e9\u05db"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d1\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " repetition"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " acceptable"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " because"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " both"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " products"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " apparently"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " have"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " layered"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " processed"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " structures"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " ["}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "22"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "]"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " should"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " echo"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " ["}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "21"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "]"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " too"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " closely"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "For"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " ["}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "22"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "]:\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ">"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05db\u05d0\u05df"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d1\u05e2\u05d9\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05de\u05e6"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d1\u05e8\u05ea"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05db\u05d1\u05e8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05de\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d1\u05e1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05e1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05e9\u05de"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05df"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d3"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e7"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05dc\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05e1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05e8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05e4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d2\u05dc"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05e7"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05d6"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d5\u05e1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05db\u05e8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d7"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u2014"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d5\u05d0\u05d6"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05e4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05e8\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05de\u05e1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05db"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e8\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05de\u05e2\u05dc"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "("}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "e"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ")"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " Remaining"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " Translation"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "ese"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " /"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " Hebrew"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " Issues"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "**\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u201c"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d4\u05e9"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05de\u05df"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05e9\u05de"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e6\u05d9\u05e2"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " in"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " intro"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " line"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " unnatural"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " Use"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05d2"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d4\u05e9"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05de\u05df"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u201d.\n\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u201c"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d7"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05dc\u05d1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05df"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05de\u05de\u05e9"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " in"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " ["}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "]"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " sounds"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " slightly"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " odd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " Better"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d7"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05dc\u05d1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05df"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d2\u05d1\u05d5\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " or"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05de\u05e7"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05e8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d7"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05dc\u05d1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05df"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05de\u05e9\u05de\u05e2\u05d5\u0
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u201d.\n\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u201c"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05de\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d2\u05d1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05d4\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d1\u05d7"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05dc\u05d1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05df"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " in"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " ["}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "7"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "]"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " understandable"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " stiff"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " Better"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05de\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05de"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05e6\u05e8\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d4\u05e2"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e9"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05e8\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d1\u05d7"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05dc\u05d1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05df"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e7\u05d8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d2\u05d5\u05e8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u201d.\n\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u201c"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e9"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e0\u05d9"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05e9\u05db"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d1\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " in"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " ["}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "21"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "]"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " should"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " be"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e9"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05ea\u05d9"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05e9\u05db"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d1\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u201d.\n\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u201c"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d7"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05de\u05e8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05de\u05e9"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05de\u05e8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05e2\u05dc"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d4\u05e4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05e8\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05d1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e9\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " in"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " ["}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "20"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "]"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " understandable"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " little"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " compressed"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " Better"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d7"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05de\u05e8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05de\u05e9"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05de\u05e8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05e9\u05de"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05e4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05e2"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05e2\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d4\u05e4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05e8\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05d1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e9\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u201d.\n\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u201c"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05de"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05de\u05ea"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05e7"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05de"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05e0"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e7"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e4\u05e8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05d8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d1\u05de\u05e7\u05d5\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05de\u05dc\u05d0"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05db\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " in"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " ["}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "3"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "]"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " may"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " be"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " confusing"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " It"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " implies"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "not"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " artificial"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " as"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " virtue"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " consumers"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " may"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " know"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " what"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " monk"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " fruit"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " Better"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ":\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ">"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05de"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05de\u05ea"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05e7"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05de"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05e0"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e7"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e4\u05e8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05d8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05d1\u05de\u05e7\u05d5\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05de"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05de\u05ea"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05e7"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05de\u05dc\u05d0"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05db\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05e0\u05e4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05e5"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\n\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "Ship"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " /"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " Fix"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "First"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "**\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "Fix"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "-first"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " because"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " rewrite"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " failed"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " The"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " copy"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " broadly"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " in"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " right"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " direction"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " much"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " closer"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " desired"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " style"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " The"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " main"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " fixes"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " before"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " ship"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " are"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ":\n\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " Shar"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "pen"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " intro"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " line"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " fix"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d4\u05e9"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05de\u05df"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05e9\u05de"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e6\u05d9\u05e2"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u201d.\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " Strength"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "en"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " grade"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " rationale"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " ["}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "6"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "],"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " ["}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "],"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " ["}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "10"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "],"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " slightly"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " ["}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "5"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "].\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "3"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " Remove"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "soft"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "en"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " over"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "stat"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "ements"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " in"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " ["}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "3"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "],"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " ["}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "12"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "],"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " possible"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " fiber"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " contradiction"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " in"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " ["}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "].\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " V"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "ary"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e2"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05dc"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e9"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05de"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05e1\u05e3"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " +"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05e8"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05db\u05d6"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u05ea\u05e4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05d7\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " reduce"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05de\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d5\u05e0\u05d3"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e1"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e0\u05d3"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u05e1\u05d4"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " recurrence"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "Return"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " status"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " RETURN"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "ED"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " content"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " revision"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": " closed"}
  message.part.delta: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "partID": "prt_ef5e44a89001Eg4gc9zUXMORMM", "field": "text", "delta": "."}
  message.part.updated: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "part": {"id": "prt_ef5e44a89001Eg4gc9zUXMORMM", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "type": "
  message.part.updated: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "part": {"id": "prt_ef5e559a1001QuQlWnC6EVgK06", "reason": "stop", "snapshot": "f8e1e69f5adc4acbbebfee6e2d8bd08b7e572c8a", "messageID": "msg_ef5e41f3c00
  message.updated: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "info": {"id": "msg_ef5e41f3c0018HpdtICC37dWpK", "parentID": "msg_ef5e41d86001DSowSCIG0XVeSB", "role": "assistant", "mode": "build", "agent": "build", "
  message.part.updated: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "part": {"id": "prt_ef5e55efc001bY9gdsYbj1MhrF", "messageID": "msg_ef5e41f3c0018HpdtICC37dWpK", "sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "type": "
  message.updated: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "info": {"id": "msg_ef5e41f3c0018HpdtICC37dWpK", "parentID": "msg_ef5e41d86001DSowSCIG0XVeSB", "role": "assistant", "mode": "build", "agent": "build", "
  session.status: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "status": {"type": "busy"}}
  session.status: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "status": {"type": "idle"}}
  session.idle: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP"}
  session.updated: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "info": {"id": "ses_10a1be802ffea3tiiBYz6OBVZP", "slug": "tidy-cabin", "projectID": "e7f90f8a5abbaca924c7d1983e3ba702c9bbf643", "directory": "C:\\Bari",
  session.diff: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "diff": []}
  message.updated: {"sessionID": "ses_10a1be802ffea3tiiBYz6OBVZP", "info": {"role": "user", "time": {"created": 1782241828230}, "agent": "build", "model": {"providerID": "openai", "modelID": "gpt-5.5"}, "summary": {"dif
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
 M bari-web/src/components/comparisons/comparison-page.tsx
 M bari-web/src/components/comparisons/granola-comparison-page.tsx
 M bari-web/src/components/comparisons/protein-bars-comparison-page.tsx
 M bari-web/src/components/shared/category-prologue.tsx
 M bari-web/src/components/shared/comparison-metric-column.tsx
 M bari-web/src/components/shared/comparison-row.tsx
 M bari-web/src/components/shared/comparison-table.tsx
 M bari-web/src/lib/blog/blog-index-content.ts
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
?? 02_products/breakfast_cereals/batch_run_granola_task385_25g.py
?? 02_products/breakfast_cereals/bsip2_outputs/run_granola_task385_25g/
?? 02_products/breakfast_cereals/bsip2_outputs/run_granola_task385_off/
?? 02_products/breakfast_cereals/bsip2_outputs/run_granola_task385_on/
?? 02_products/breakfast_cereals/reports/red_team_granola_run_granola_task385_off.md
?? 02_products/breakfast_cereals/reports/task385_ev105_granola_25g_report.json
?? 02_products/breakfast_cereals/reports/task385_granola_rescore_report.json
?? 02_products/breakfast_cereals/reports/task385_run_record.json
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
?? bari-web/e2e/task384-geometry.spec.ts
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
?? bari-web/src/data/comparisons/bread_frontend_v2_gates_report.md
?? bari-web/src/data/comparisons/bread_frontend_v3_gates_report.md
?? bari-web/src/data/comparisons/brined_cheeses_frontend_v2_gates_report.md
?? bari-web/src/data/comparisons/cakes_hard_cookies_frontend_v1_gates_report.md
?? bari-web/src/data/comparisons/cereals_frontend_v2_gates_report.md
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
?? tasks/_scratch_citation_report.txt
?? tasks/_scratch_citation_v2.txt
?? tasks/_scratch_mag_labels/
?? tasks/_scratch_naturalness_check.py
?? tasks/_scratch_naturalness_mag.py
?? tasks/_scratch_naturalness_result.json
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
?? tasks/prompts/P390_granola_decite_c3.md
?? tasks/prompts/_done/P283_protein_bars_r3_mechanical.md
?? tasks/prompts/_done/P297_hc_satfat_rule_challenge.md
?? tasks/prompts/_done/P302_c3_magnesium_v3_real_calibration_challenge.md
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
 M bari-web/src/components/comparisons/comparison-page.tsx
 M bari-web/src/components/comparisons/granola-comparison-page.tsx
 M bari-web/src/components/comparisons/protein-bars-comparison-page.tsx
 M bari-web/src/components/shared/category-prologue.tsx
 M bari-web/src/components/shared/comparison-metric-column.tsx
 M bari-web/src/components/shared/comparison-row.tsx
 M bari-web/src/components/shared/comparison-table.tsx
 M bari-web/src/lib/blog/blog-index-content.ts
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
?? 02_products/breakfast_cereals/batch_run_granola_task385_25g.py
?? 02_products/breakfast_cereals/bsip2_outputs/run_granola_task385_25g/
?? 02_products/breakfast_cereals/bsip2_outputs/run_granola_task385_off/
?? 02_products/breakfast_cereals/bsip2_outputs/run_granola_task385_on/
?? 02_products/breakfast_cereals/reports/red_team_granola_run_granola_task385_off.md
?? 02_products/breakfast_cereals/reports/task385_ev105_granola_25g_report.json
?? 02_products/breakfast_cereals/reports/task385_granola_rescore_report.json
?? 02_products/breakfast_cereals/reports/task385_run_record.json
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
?? bari-web/e2e/task384-geometry.spec.ts
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
?? bari-web/src/data/comparisons/bread_frontend_v2_gates_report.md
?? bari-web/src/data/comparisons/bread_frontend_v3_gates_report.md
?? bari-web/src/data/comparisons/brined_cheeses_frontend_v2_gates_report.md
?? bari-web/src/data/comparisons/cakes_hard_cookies_frontend_v1_gates_report.md
?? bari-web/src/data/comparisons/cereals_frontend_v2_gates_report.md
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
?? tasks/_scratch_citation_report.txt
?? tasks/_scratch_citation_v2.txt
?? tasks/_scratch_mag_labels/
?? tasks/_scratch_naturalness_check.py
?? tasks/_scratch_naturalness_mag.py
?? tasks/_scratch_naturalness_result.json
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
?? tasks/prompts/P390_granola_decite_c3.md
?? tasks/prompts/_done/P283_protein_bars_r3_mechanical.md
?? tasks/prompts/_done/P297_hc_satfat_rule_challenge.md
?? tasks/prompts/_done/P302_c3_magnesium_v3_real_calibration_challenge.md
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
?? tasks/task368_d4_impact_analysis.py
?? tasks/task368_output.txt
?? test_acceptance.py
```

### Delta

*(no changes detected)*
