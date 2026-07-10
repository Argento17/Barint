# P514 / Yogurt copy editorial-philosophy consult (route: C3)

route: C3 — independent challenge/consult only. You do NOT author copy, do NOT edit files, do NOT close. You give a reasoned editorial ruling the orchestrator will fold into a Content Agent spec.

## Situation
Bari ranks Israeli supermarket products and writes short Hebrew consumer verdicts per product on a comparison page. The owner rejected the yogurt pages' copy. The Content Agent re-authored all 98 products' copy; the independent Adversarial QA gate then FAILED it again — the re-author fixed the specific rejected *phrases* but not the *pattern*. Two of the failures are genuine editorial-philosophy forks I want an independent read on BEFORE I send Content back, because a naive re-dispatch will just fail a third time.

Context on the scoring: each product gets a 0-100 score + letter grade (A-E), shown as a chip in the UI with a protein/calorie bar. Many yogurts are genuinely SIMILAR — e.g. ~25 plain additive-free products (goat/sheep/Greek/lactose-free) whose real differentiator is small. A common real situation: a clean 2-ingredient yogurt scores "only" A (not higher) because the ingredient data came from page-text with no label scan, so the processing-level (NOVA) classification carries a confidence cap. So the honest limiting driver for many products IS a framework-internal mechanism (a provenance/confidence cap), not a visible product flaw.

## The two forks — rule on each with reasoning

### FORK A — mechanism honesty vs framework-invisibility (QA finding RT-2)
65/98 verdicts explain the SCORE MECHANISM, e.g. "נשאר ב-A כי רשימת הרכיבים מבוססת על טקסט העמוד בלבד, ולכן רמת העיבוד אינה מאומתת" ("stays at A because the ingredient list is based on page text only, so processing level is unverified"). Bari's editorial law says copy must be "framework-invisible" — the algorithm should never narrate itself; write about the FOOD, not the scoring. But the honest reason many products are capped IS this provenance mechanism.
**Rule:** When a product's real limiting driver is a provenance/confidence cap (not a product property), what should the one-line verdict say? Options: (i) omit it entirely — describe the food's actual composition, let the grade stand without justifying it; (ii) translate the cap into food-language without naming the machine; (iii) something else. Give the principle AND a concrete Hebrew example of a good line for a "clean 2-ingredient yogurt, A, capped by page-text provenance."

### FORK B — de-templating vs manufactured differentiation (QA finding RT-3)
22/78 takeaways are byte-identical; only 34/78 distinct insightLines. QA calls this "templated at the rejected scale." BUT Bari has a hard, owner-backed rule against MANUFACTURING differentiation between genuinely-similar products (precedent: butter clustering was ruled an honest finding — "never add signals to manufacture differentiation"; a fabricated-identity incident where fake distinguishing detail was invented is a standing scar). If 25 plain yogurts really are compositionally near-identical, forcing 25 distinct "insightful" descriptions risks inventing differences that aren't real.
**Rule:** Where is the honest line between (a) legitimately-varied per-product copy and (b) manufactured differentiation? For a shelf where a large subset is genuinely similar, is structured near-repetition actually the HONEST output (and the QA "templating" finding partly a false expectation), or is there a real, non-fabricated axis (brand, milk source, texture, use-case, price) that justifies distinct copy without inventing facts? Give the test Content should apply per-product to decide "vary it" vs "let it read similar because it IS similar."

## Return
A crisp ruling on FORK A and FORK B — the principle, the honest line, and one concrete Hebrew example each. Flag if you think either QA finding is partly wrong (over-demanding differentiation that would force fabrication). This routes into a Content re-author spec; be decisive, not a menu. End with the machine-readable return contract JSON.
