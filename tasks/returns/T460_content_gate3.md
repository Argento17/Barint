# TASK-460 Gate 3 — Content fix pass on Gate-2 findings (RT-1 / RT-2 / RT-3)

Executor: content fix pass (direct, no subagents)
Date: 2026-07-02
Base: commit `f1bca7b0` (Gate-2 adversarial QA report) on branch `fix/task460-stale-adapter-prose`, worktree `C:\bari_wt_t461`
Input: `tasks\returns\T460_redteam_gate2.md` (RT-1/RT-2/RT-3 rulings, all HIGH/live)

Scope: fix exactly the three HIGH live numeric defects RT-2 ruled must be fixed on this branch. RT-4 and RT-5 (MEDIUM, latent/pre-existing) are left untouched — routed separately per the gate-2 report.

---

## RT-1 — chocolate-tablets ceiling claim

File: `bari-web/src/lib/comparisons/chocolate-tablets-comparison-page-data.ts` (`chocolateTabletsCategoryNote`, first sentence — renders on `/hashvaot/chocolate-tablets`)

### Deriving command (independent re-verification against `chocolate_tablets_frontend_v1.json`)
```python
import json
from collections import Counter
with open(r"C:\bari_wt_t461\bari-web\src\data\comparisons\chocolate_tablets_frontend_v1.json", encoding="utf-8") as f:
    d = json.load(f)
prods = d["products"]
print("n =", len(prods))                                   # n = 35
print(dict(Counter(p.get("grade") for p in prods)))         # {'B': 2, 'C': 6, 'D': 10, 'E': 17}
sp = sorted(prods, key=lambda p: -p.get("score", -999))
for p in sp[:6]:
    print(p.get("score"), p.get("grade"), p.get("name_he") or p.get("name"))
```
Output:
```
n = 35
grade counts: {'B': 2, 'C': 6, 'D': 10, 'E': 17}
Top 6 by score:
65.8 B  שוקולד מריר
65.1 B  שוקולד מריר 90%
55.3 C  שוקולד מריר ללת"ס 72%
54.3 C  טוסו שוקולד מריר 62%
54.1 C  טוסו שוקולד מריר
53.7 C  שוקולד מריר לינדט 78%
```
Confirms gate-2: top 2 products = B (65.8, 65.1); 10-point gap to the first C (55.3). No product reaches A or scores above 65.8.

### Old → New
- OLD: "המוצר הטוב ביותר במדף הזה מדורג C — וזה ממצא אמיתי. שוקולד הוא ממתק צפוף בשומן וסוכר, וגם הטבלה הנקייה ביותר לא מתחמקת מזה. ה-C הוא הצד הנכון של מדף הממתקים; לא מוצר בריאות."
- NEW: "רק שתי טבלאות במדף הזה מגיעות ל-B, ואחריהן פער של עשר נקודות עד הבאה בתור. שוקולד הוא ממתק צפוף בשומן וסוכר, וגם שתי הטבלאות שמובילות את המדף לא מתחמקות מזה. ה-B הוא הצד הנכון של מדף הממתקים; לא מוצר בריאות."

Thesis preserved (chocolate is a dense treat; even the shelf-topping tablets don't escape that; the ceiling sits on the treat side of the shelf) — only the false factual anchor ("best = C") is corrected to the true finding (2 tablets reach B, 10-pt gap to C). No em-dash added; no "X not Y" negation introduced; no health claim.

Companion consistency fix (same file, third categoryNote sentence, required by the same defect — leaving it would have reintroduced "reach C" one paragraph later):
- OLD: "'ללא סוכר' לא מדרג לבד: כשהקקאו גבוה והתחליפים לא משתלטים, הטבלה יכולה להגיע ל-C; כשהממתיק ראשון ברשימה, אחוז הקקאו נמוך, או הנוסחה עמוסה בממתיקים ומתחלבים — היא יורדת ל-D ואף E."
- NEW: "'ללא סוכר' הוא רק חלק מהתמונה: כשהקקאו גבוה והתחליפים נשארים ברקע, טבלה ממותקת בתחליפים יכולה להגיע גם ל-B; כשהממתיקים משתלטים על הרשימה ואחוז הקקאו נמוך, היא יורדת ל-D ואף ל-E."
Verified against the same JSON recount above: both B-grade tablets carry sugar ≈2g/100g (one via erythritol/stevia replacers, one via 90% cocoa mass with minimal added sugar) — i.e. genuinely low-sugar/high-cocoa formulas, consistent with "sugar-free/low-sugar with high cocoa can reach B."

---

## RT-2 — protein-bars maltitol count

File: `bari-web/src/lib/comparisons/protein-bars-comparison-page-data.ts` (`proteinBarsPrologueSentences[2]` — renders on `/hashvaot/protein-bars`)

### Deriving command (independent re-verification against `protein_combined_frontend_v2.json`, field `expansion.ingredients`)
```python
import json
with open(r"C:\bari_wt_t461\bari-web\src\data\comparisons\protein_combined_frontend_v2.json", encoding="utf-8") as f:
    d = json.load(f)
prods = d["products"]
print("n =", len(prods))          # n = 32

hit = 0
for p in prods:
    txt = (p.get("expansion") or {}).get("ingredients")
    txt = txt if isinstance(txt, str) else ""
    if "מלטיטול" in txt:
        hit += 1
print("maltitol hits (expansion.ingredients contains 'מלטיטול'):", hit)   # 16
```
Output: `n = 32`, `maltitol hits = 16`. Matches gate-2's authoritative recount (16/32) exactly — independently re-derived from the same structured field, not copied from the report. (I also checked an "any polyol" superset for comparison — 18/32 contain any of maltitol/xylitol/sorbitol/erythritol/mannitol/isomalt/lactitol — but the claim in the prose names maltitol specifically, so 16 is the correct, defensible number for this sentence; did not use the count.)

### Old → New
- OLD: "ב-24 מתוך 32 המוצרים בדף הזה הסוכר לא הופחת אלא הוחלף במלטיטול, ..."
- NEW: "ב-16 מתוך 32 המוצרים בדף הזה הסוכר לא הופחת אלא הוחלף במלטיטול, ..."

(Rest of the sentence — Pangea/69-B contrast, "least engineered ≠ health food" caveat — unchanged; it was already accurate and durable.) Chose the corrected exact count over a vaguer reframe because the field cleanly supports a precise, checkable number and the sentence's rhetorical structure ("X מתוך 32... הוחלף במלטיטול") depends on a specific count to land.

---

## RT-3 — cookies-coffee prologue denominator/E-count

File: `bari-web/src/data/comparisons/cookies_coffee_frontend_v2.json` → `page_copy.prologue.sentences[0]` (renders on `/hashvaot/cookies-coffee` via `cookies-coffee-page-data.ts:78`, `cookiesCoffeePrologueSentences = _pageCopy.prologue.sentences`). Edited the JSON string only — no other field in the file touched (confirmed: `git diff --stat` shows 1 file, 1 line changed).

### Deriving command (independent re-verification against `cookies_coffee_frontend_v2.json:products`)
```python
import json
from collections import Counter
with open(r"C:\bari_wt_t461\bari-web\src\data\comparisons\cookies_coffee_frontend_v2.json", encoding="utf-8") as f:
    d = json.load(f)
prods = d["products"]
print("products.length =", len(prods))                       # 117
print(dict(Counter(p.get("grade") for p in prods)))           # {'C': 9, 'D': 27, 'E': 81}
```
Output: `products.length = 117`, grade counts `C=9, D=27, E=81`. Matches gate-2 exactly (117 products, 81 at E). Confirmed `page_copy.hero.productCount`/`scoredCount` are still 119 (also stale) but do NOT render — the adapter reads `_pageCopy.hero.tagline` (qualitative, no count) for the hero, not `productCount`/`scoredCount`. Per gate-2 routing and the task instruction, only the rendered prologue string was edited; the unused hero counts were left alone (out of this pass's scope — a separate data-agent regen item, not a live defect).

### Old → New (page_copy.prologue.sentences[0])
- OLD: "ביסקוויטים לקפה הם לא אוכל בריאות; השאלה היא מי מהם פחות גרוע, ולמה. 83 מתוך 119 המוצרים שנבחנו מקבלים ציון E, ו-C הוא תקרת הקטגוריה הזו. זה לא בגלל רכיב אחד ספציפי — זה פרופיל השומן הרווי והסוכר שאפיין את רוב המדף."
- NEW: "ביסקוויטים לקפה הם לא אוכל בריאות; השאלה היא מי מהם פחות גרוע, ולמה. 81 מתוך 117 המוצרים שנבחנו מקבלים ציון E, ו-C הוא תקרת הקטגוריה הזו. זה לא בגלל רכיב אחד ספציפי — זה פרופיל השומן הרווי והסוכר שאפיין את רוב המדף."

("C is the category ceiling" claim was already correct — top grade in the corpus is C=9, confirmed above — left unchanged.)

---

## Build verification

```
cd C:\bari_wt_t461\bari-web
npx tsc --noEmit     → exit 0, no output
npm run build         → exit 0; all routes compiled, including
                         /hashvaot/chocolate-tablets, /hashvaot/protein-bars,
                         /hashvaot/cookies-coffee (all listed ƒ dynamic, no errors)
```

## Scope check
```
git status --short
 M bari-web/src/data/comparisons/cookies_coffee_frontend_v2.json
 M bari-web/src/lib/comparisons/chocolate-tablets-comparison-page-data.ts
 M bari-web/src/lib/comparisons/protein-bars-comparison-page-data.ts
```
(`bari-web/src/lib/comparisons/juices-page-data.ts` had a pre-existing uncommitted modification from before this pass started — not touched, not staged, not committed by this fix.)

RT-4 (orphaned duplicate copy in `comparison-pages.json`) and RT-5 (granola prologue score-mechanic leakage) are untouched per the task's explicit instruction — both are MEDIUM/latent-or-pre-existing and routed separately.

## Bottom line
All three HIGH live numeric defects from gate-2 (RT-1, RT-2, RT-3) are fixed with independently re-derived numbers, confined to the exact flagged strings, voice rules held (no new em-dash overuse, no "X not Y" negation, no health-outcome claim, no un-rank-checked superlative). `tsc --noEmit` and `npm run build` both exit 0. No push/PR/deploy. `C:\Bari` untouched (worktree-only). OFF ban not implicated.
