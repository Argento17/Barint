# Red-Team Challenge Report — Creatine Comparison (TASK-492C, content package v2)
Date: 2026-07-03   Scope: 31 products (18 Israeli + 13 worldwide), proposed route `/hashvaot/creatine`   Challenger: adversarial-qa-agent

Package under review: `03_operations/reports/content/creatine_comparison_content_package_v2.md`
Verified directly against: `creatine_benchmark_solid_v1.md`, `creatine_supplement_shelf_scrape_v1.md`,
`creatine_evidence_cosign_v1.md`, `creatine_evidence_verification_v1.md`, `creatine_page_model_decision_v1.md`,
plus independent PubMed/CrossRef re-verification of every cited PMID/DOI in the Hebrew consumer copy.

## Opening Finding

No data-absent scoring issue (score/grade are correctly null everywhere, per ruling 1 — this
does not trigger Hard Rule 12's null-nutrition/null-ingredient trap since there is no BSIP2
scoring surface on this page at all). The opening structural problem instead is a **certification
count/list defect that runs through the entire document**: the worldwide-benchmark product table
badges **7** rows `אומת מול מאגר` (directory-verified) — Thorne (B1), Momentous (B2), Klean
Athlete (B3), BPN (B4), MegaFood (B5), **Sports Research (B6)**, BioSteel (B8) — but every prose
summary, every count, and the Return Contract's own `certs_directory_verified` field say **"6"**
and name only "Thorne, Momentous, Klean Athlete, BPN, MegaFood, BioSteel," omitting Sports
Research from the list while its table row still carries the badge. This is not a rounding
nuance; it is an internally inconsistent certification claim on a page whose entire "no A-E
grade, trust our transparency instead" pitch depends on the two-tier cert badge being exactly
right (Hard Rule 10 / mandatory check 2). The error is inherited verbatim from the source
benchmark report's own summary miscount (`creatine_benchmark_solid_v1.md` line 133-134) rather
than introduced fresh in v2, but the content package's job was to fold the benchmark in
correctly, and it propagated the arithmetic bug instead of catching it.

## Product-by-Product Assessment (spot-check sample)

| ID | Product | Score/Grade | RT Assessment | Confidence | Critical Notes |
|---|---|---|---|---|---|
| IL-3 | All In (Shufersal) | null | Matches scrape exactly (3.0g/83/₪99.90/₪1.20) | Verified | None |
| IL-5 | MyProtein Impact | null | Matches scrape exactly | Verified | None |
| IL-8 | MyProtein Elite (Israeli) | null | 3.0g matches Israeli scrape; correctly NOT conflated with worldwide 3.4g Elite (B10), though the two "Elite" rows carrying different doses with zero inline cross-reference is a latent confusion risk | Verified | MEDIUM — see finding RT-4 |
| IL-11/12 | Optimum Nutrition / Thorne | null | Match scrape exactly incl. price-per-3g | Verified | None |
| IL-15/17/18 | California Gold / Kaged / Con-Cret | null | Match scrape exactly (750mg pattern, HCl multiplier) | Verified | None |
| B1-B5 | Thorne/Momentous/Klean Athlete/BPN/MegaFood | null | Transcribed cleanly from benchmark table, cert-tier correct | Verified | None |
| B6 | Sports Research | null | Table badge correct (directory-confirmed) per benchmark row 6; **prose/count everywhere else omits it from the "6 directory-confirmed" list** | Contradicted by page's own summary | **CRITICAL — RT-1** |
| B8 | BioSteel | null | 2.5g sub-floor framing accurate and appropriately isolated from 5g rows | Verified | None |
| B10/B11 | MyProtein Elite/Creapure (worldwide) | null | Correction carried faithfully (Elite=generic 3.4g, Creapure=separate SKU); matches benchmark exactly | Verified | None |
| B12 | Switch Nutrition | null | Correctly downgraded to מוצהר על-ידי היצרן in v2 (supersedes stale Ruling 2 text, which still names it as one of the 3 original directory-verified — ruling doc itself is now stale, not a package defect) | Verified, but see RT-6 | MEDIUM |
| Dairy | Yoplait GO (2 SKUs) | N/A (annotation lane) | 0.6%-no-serving-size / no-figure-at-all pattern matches co-sign exactly; Tnuva correctly reframed as collagen | Verified against co-sign (primary 492B scrape not in my source set — chain-of-custody gap) | MEDIUM |

## Summary Assessment

**Plausible-but-unverifiable** on the dairy annotation chain of custody (I could not read the
underlying `functional_dairy_shelf_scrape_v1.md`). **Justified** on the core Israeli-shelf and
worldwide-benchmark product data — every spot-checked row transcribes cleanly with correct
figures, and the price-per-3g / dose-honesty arithmetic is verifiably load-bearing, not
decorative. **Weak confidence** on the certification-tier accounting specifically (RT-1) —
this is the one place where the page's own self-description does not match its own table.
**Overriding structural problem: the cert-count defect (RT-1)**, because it undermines the exact
claim (verified-vs-manufacturer-stated honesty) that replaces the missing A-E grade as this
page's whole credibility mechanism.

## Findings by Severity

### CRITICAL — must resolve before launch

**RT-1: Directory-verified certification count and named list are wrong / internally inconsistent.**
Evidence: `creatine_comparison_content_package_v2.md` table row B6 (line 163) badges Sports
Research `אומת מול מאגר` with a live NSF ID (nsfsport.com id 1751614), matching
`creatine_benchmark_solid_v1.md` row 6 which independently confirms "NSF Certified for
Sport — directory-confirmed." But every prose count in the same package (lines 24-25, 152-153,
173, 361, 394, and the Return Contract's `certs_directory_verified` field, line 419's
self-check) states "6/13" or "6/31" and names the six as "Thorne, Momentous, Klean Athlete,
BPN, MegaFood, BioSteel" — Sports Research is never once named in any of these six lists despite
its row carrying the exact same badge. The true count in the actual table is 7 (adding Sports
Research), or the table is over-badging Sports Research and it should read 6 with Sports
Research downgraded. Implication: any consumer-facing methodology copy that says "six worldwide
brands verified against NSF's own registry" is either undercounting a real verified product
(understating Bari's own diligence) or, worse, the table is wrongly badging a 7th product as
directory-confirmed that the page's own accounting doesn't recognize — a claim a competitor or
NSF itself could challenge for precision. Either direction is a factual-accuracy defect in a
cert claim, which Hard Rule 10/13 treat as a hard stop, not a style note. Routes to: data-agent
(to reconcile the table against `creatine_benchmark_solid_v1.md`'s own per-row cert column,
which is itself the authoritative source and is internally correct — the summary prose in both
the source benchmark report and the v2 package is what's wrong) and content-agent (to fix every
downstream prose count once the true number is settled).

### HIGH — should resolve before launch

**RT-2: Consumer-facing prologue and dose-honesty explainer overclaim the channel concentration of undisclosed-dose products.**
Evidence: `creatine_comparison_content_package_v2.md` line 200 ("ארבעה מוצרים נושאים את המילה
קריאטין... **וכולם מהמדף של רשתות המזון בישראל**" — "and all of them are from Israel's grocery
chain shelves") and line 281 ("...ארבעה מוצרים במדף הישראלי נמצאים כאן, **וכולם מרשתות המזון**"
— "and all of them are from the grocery chains"). Contradicted by:
`creatine_supplement_shelf_scrape_v1.md` line 266 (Return Contract counts) and line 119-121
(prose), both stating explicitly: "4/4 undisclosed products are Shufersal-channel (**3
powders**) **+ 1 MyProtein tablet SKU**" — and MyProtein is documented throughout the same
report as an **import e-commerce channel**, not a grocery chain (§1: "MyProtein Israel
(myprotein.co.il — import brand, direct e-commerce"). The content package's own product table
(row 9, line 125: "Creatine Monohydrate Tablets | MyProtein | MyProtein-IL | ... | undisclosed")
correctly channels this product as MyProtein-IL two sections above the prose that then claims
"all of them" are grocery-chain. Implication: a reader who cross-references the table against
the prose finds a factual contradiction in the same document — exactly the kind of "does the
consumer copy claim more than the data supports" failure this gate exists to catch. This is not
a rounding error; "all" (כולם) is a total claim contradicted by the document's own data. Routes
to: content-agent (rewrite "וכולם מרשתות המזון" to something like "שלושה מרשת שופרסל ואחד מיבוא"
or drop the channel-concentration claim to "רוב" / a correctly-scoped 3-of-4 statement).

### MEDIUM — should document or monitor

**RT-3: Hebrew leakage gate false-positive on the DOI fragment — worth a documented exception, not a fix, but flag before automated gating is trusted blind.**
Evidence: running `integrations/clients/hebrew_readability.py`'s `analyze()` on the "what
creatine does" Hebrew block (content package §2.3, lines 212-225) returns `is_clean=False` with
a `score_mechanic` flag on the substring `"10.2903"` (from the EFSA DOI
`10.2903/j.efsa.2024.9100`). This is a genuine false trigger — the gate's numeric-pattern
heuristic is misreading part of a citation DOI as a raw score/percentage mechanic (its own
documented failure mode: "only `is_clean` is a hard gate; the readability number is
heuristic"). A second false trigger fires on the dairy-annotation block (§3, line 316): the
`framework` leak-kind matches the substring "נובה" (Hebrew for "NOVA") inside "**ת**נובה" (the
brand name Tnuva) — an unrelated substring collision, not an actual NOVA-classification leak.
Implication: if this package is later run through the deterministic Hebrew leakage gate as a
go-live check per the mandatory-instrument rule, it will show 2/8 blocks failing `is_clean` for
reasons that are not real framework leaks — someone needs to either accept these as documented,
named exceptions before the gate result is read literally, or the gate needs a citation-DOI/
proper-noun exclusion rule. Neither block contains an actual BSIP2 term, pillar name, or raw
Bari score. Routes to: frontend-agent / whoever owns the Hebrew leakage gate tooling (not a
content defect — the copy itself is fine; the gate's pattern-matching needs a documented
exception or a fix).

**RT-4: The same product name ("Creatine Monohydrate Elite," MyProtein) appears twice with two different doses (3.0g Israeli vs 3.4g worldwide) with zero inline note connecting them.**
Evidence: content package row 8 (Israeli, line 124: 3.0 g) vs. row B10 (worldwide, line 167:
3.4 g). Both are individually correct against their respective sources (Israeli scrape captured
3.0g on myprotein.co.il at scrape time; the fresher worldwide benchmark pass re-confirmed 3.4g
on myprotein.com's UK/EU listing) — this is legitimately two different regional listings scraped
in two different passes, not an error. But nothing in the rendered product table (per the VM
contract in §4) flags for a reader that "MyProtein Creatine Monohydrate Elite" is the *same
branded SKU* showing two different doses across the Israeli and worldwide tables. A sharp reader
who notices the name match and the dose mismatch has no explanation available on-page. This is a
defensibility gap, not a data error. Routes to: content-agent (a one-line footnote on one or
both rows would close this — not proposing the fix, just naming the gap).

**RT-5: Dairy-annotation chain of custody could not be independently verified — outside my provided source set.**
Evidence: `creatine_comparison_content_package_v2.md` §3 cites `functional_dose_ingredient_ruling_v1.md`
§3.2 and the co-sign as its authority for the Yoplait/Tnuva copy, and the co-sign in turn cites
`functional_dairy_shelf_scrape_v1.md` (TASK-492B) as the primary scrape. That primary scrape
report was not included in my verification scope for this gate. Everything I could check (the
co-sign's transcription of the 0.6%-no-serving-size figure, the Tnuva-is-collagen correction, the
barcode 7290116935607, the collagen 1.48% figure) is internally consistent across the co-sign and
the content package, and the correction chain (PDF claim → contradicted by direct scrape →
co-sign resolves in scrape's favor) is well-documented and traceable. But I have not read the
primary scrape file myself, so this is "consistent with what I could read," not "independently
re-verified against the primary source" in the same sense as the supplement-shelf and worldwide
benchmark tables. Routes to: data-agent (confirm `functional_dairy_shelf_scrape_v1.md` is the
correct, current, and only primary source for this claim before go-live) — flagged for
completeness, not because I found a contradiction.

**RT-6: Ruling 2 (Product Agent decision document) is now stale and does not match the shipped v2 cert data — not a package defect, but a documentation-drift risk.**
Evidence: `creatine_page_model_decision_v1.md` line 66-67 names the 3 originally directory-
verified products as "Thorne (NSF), Momentous (NSF), **Switch Nutrition (HASTA)**" — reflecting
the earlier 5-product benchmark. The v2 package correctly supersedes this with the more
rigorous re-check (`creatine_benchmark_solid_v1.md`), which found HASTA's directory was never
actually cross-checked for Switch Nutrition, and correctly downgrades it to
`מוצהר על-ידי היצרן`. This is the right call by the package — better evidence overriding a
stale ruling — but the ruling document itself is not marked superseded anywhere, so a future
reader consulting Ruling 2 in isolation would get a wrong answer about Switch Nutrition's cert
status. Routes to: product-agent (add a superseded-by note to Ruling 2, or fold the correction
into a Ruling 2 addendum) — informational, not a launch blocker for the page itself since the
package already applied the correct, newer data.

**RT-7: Bipolar citation (PMID 17988366) ships as a settled fact in consumer copy despite the co-sign explicitly flagging it as an unverified candidate.**
Evidence: `creatine_evidence_cosign_v1.md` §2.4's own YAML recommendation states
`verification_status: "candidate — recommend Research Agent PMID pull before this ships as a
cited fact"`, and the co-sign's own `not_done` list (line 334) says the bipolar-contraindication
source "were not independently re-pulled in this pass." Yet the content package's Hebrew safety
copy (line 258) cites it inline as settled: "(Roitman ואחרים 2007, PMID 17988366)." I
independently re-verified this PMID directly against PubMed (title: "Creatine monohydrate in
resistant depression: a preliminary study," journal *Bipolar disorders*, 2007, authors including
Suzana Roitman) — **it is real, on-topic, and its abstract directly supports the claim** ("Both
bipolar patients developed hypomania/mania" in an n=10 open-label study). So the citation is
correct and defensible on the merits, but the package shipped it as if the ship-gate-flagged
verification step had already happened, when it hadn't been documented as done anywhere in the
provided source chain. This is a process gap (an un-recorded verification), not a factual error
— I closed it myself during this review, but the package should not have presented an
explicitly-flagged-as-unverified citation as settled without a visible verification trail.
Routes to: nutrition-agent / research-agent (record the verification that in fact makes this
citation safe, since it does check out) — not a blocking finding since the underlying fact is
correct, but a process-integrity note.

## Verdict

**GO_WITH_FINDINGS**

Rationale: no CRITICAL finding challenges the underlying product data's accuracy, the evidence
base, or the safety framing — every cited PMID/DOI I independently re-verified (28615996,
39074168, 33631721, 41189312, 17988366, EFSA DOI 10.2903/j.efsa.2024.9100) resolved to real,
on-topic, correctly-attributed sources with figures matching the Hebrew copy exactly (12 studies/
+1.14kg, SMD -0.34/MID 3.0, "developed hypomania/mania" for the bipolar flag). No A-E grade
leaks anywhere, no NIH attribution, no Creapure-for-Momentous, no Tnuva-creatine claim, no
dairy percentage invented, no fabricated product/price/PMID found anywhere in the 31-product
set on spot-check. However, **RT-1 (the cert-count/list inconsistency) is a CRITICAL-class
defect** under Hard Rule 10 because it is a factual, checkable, currently-wrong claim about
which and how many products are directory-verified — the exact category of claim this page's
"no grade, but here's honest verification tiering" pitch cannot afford to get wrong, and it is
visible on inspection (table vs. prose disagree within the same document). **This alone blocks
GO** until reconciled. RT-2 (grocery-channel overclaim) is HIGH and should also be fixed before
publication — it is a checkable factual overstatement ("all" when the true figure is 3-of-4) in
consumer-facing prose. The MEDIUM findings (RT-3 through RT-7) are documentation/process/gate-
hygiene items that do not block launch on their own but should be tracked.

```json
{"verdict":"GO_WITH_FINDINGS","critical":1,"high":1,"medium":5}
```

---

## RE-GATE 2026-07-04 @ c5ab9b09

Scoped delta re-verification only (per delegation) — the evidence base, PMIDs/DOIs, safety
framing, product data, and prices from the full pass above were NOT re-audited; this section
covers only whether RT-1 and RT-2 are resolved and whether commit `c5ab9b09`
(branch `fix/task492c-redteam`, worktree `C:\bari_wt_t492c`) introduced any new defect. Fix
scope confirmed narrow: `git diff f0b5c886 c5ab9b09` touches exactly one file,
`bari-web/src/lib/comparisons/creatine-page-data.ts` (21 insertions, 12 deletions), all within
the Sports Research (`wb-sports-research-creatine`) row plus three prose/comment locations
(header ruling comment, `creatineCategoryNote`, worldwide-array-order comment).

### RT-1 (was CRITICAL) — RESOLVED

Ground truth confirmed directly against `03_operations/reports/research/creatine_benchmark_solid_v1.md`
row 6 (line ~30): Sports Research's primary SKU (Creatine Monohydrate Unflavored) is stated
without hedge as "NSF Certified for Sport — directory-confirmed (nsfsport.com id 1751614, active,
450 g)," with a same-row footnote isolating the *separate* Creapure sub-SKU as brand-claim-only.
The correct directory-confirmed set is 7/13, not 6/13 — the benchmark's own §3 summary prose
(line 133-138) is the party that undercounts, omitting Sports Research from its named list while
its own row 6 confirms it. The page now follows the authoritative row-level evidence, not the
summary arithmetic.

Verified in the worktree at `c5ab9b09`:
- `wb-sports-research-creatine` (`creatine-page-data.ts:782-807`): `certTier` is now
  `"directory_verified"`, `cert_label` = `"אומת מול מאגר (NSF, id 1751614)"`. `insightLine` and
  `rowVerdict` both state the NSF directory verification and separately flag the Creapure
  sub-SKU as "טענת דף בלבד" (page-claim only) "ולא אומתה מול מאגר בנפרד" — the two-SKU
  distinction from the benchmark's footnote is carried through, not conflated.
- Full-page scan for residual "6" in any count/list context (`Grep` for `directory_verified`,
  `manufacturer_stated`, "6", "שש", "שישה" across `creatine-page-data.ts`,
  `creatine-badge-grid.tsx`, `creatine-evidence-section.tsx`, `creatine-comparison-page.tsx`):
  **zero residual "6 directory-confirmed" references remain.** Every prose count now reads 7:
  header ruling comment (line 15-17: "the 7 NSF-directory-confirmed worldwide rows (Thorne,
  Momentous, Klean Athlete, BPN, MegaFood, Sports Research, BioSteel)"), `creatineCategoryNote`
  (line 100: "שבע מנות ייחוס עולמיות אומתו מול מאגר NSF" — was "שש"), and the worldwide-array
  comment (line 651: "Sorted: 7 directory-verified (NSF) first" — was "6"). The only surviving
  literal "6" tokens in the file are (a) the RT-1 fix comment itself narrating the *historical*
  benchmark miscount for provenance (lines 19-23, correctly framed as past-tense explanation,
  not a live claim), and (b) two unrelated numeric facts never in scope — "פי שש עד פי עשר"
  (six-to-tenfold HCl price multiplier, lines 82/175, unchanged by this fix) and "6 מדינות"
  (worldwide section label, line 181/650, pre-existing region-count label, untouched by this
  commit's diff). None of these three disagree with the cert count.
  - **New observation (not RT-1, not introduced by this commit, not blocking):** the "6 מדינות"
    region-count label appears to undercount by one relative to the 5 distinct region values
    actually present in the benchmark table (US, Canada, UK/EU, AU, Germany/EU = 5, not 6) —
    or overcounts if UK and EU are meant to be split. This predates `c5ab9b09` (absent from the
    diff) and is outside RT-1/RT-2 scope; flagging for a separate pass, not counted against this
    re-gate.
- `git grep` confirms the directory-verified set is now exactly 7 rows (lines 667, 691, 718, 742,
  766, 790, 817 = Thorne, Momentous, Klean Athlete, BPN, MegaFood, Sports Research, BioSteel) and
  no other row was touched: Naked Nutrition (`wb-naked-creatine`, benchmark row 7),
  Applied Nutrition (`wb-applied-nutrition-creatine`, row 9), and both MyProtein worldwide rows
  (Elite `wb-myprotein-elite`, Creapure `wb-myprotein-creapure`, rows 10-11) all remain
  `"manufacturer_stated"` — none was wrongly promoted. All 18 Israeli-shelf rows remain
  `certTier: null` or `"manufacturer_stated"` — 0/18 directory-confirmed, unchanged, matches
  ruling.

**RT-1 status: RESOLVED.**

### RT-2 (was HIGH) — CONFIRMED RESOLVED (no change needed, verified independently)

Checked both locations the original finding cited the pattern in: `creatinePrologueSentences`
(line 81: "שלושה מהם נמכרים ברשת המזון שופרסל, והרביעי הוא מוצר טבליות מיובא של MyProtein" — three
from Shufersal, the fourth an imported MyProtein tablet) and the dose-honesty-tiers evidence
section (line 159: "ארבעה מוצרים במדף הישראלי נמצאים כאן: שלושה מרשת המזון שופרסל ואחד מוצר
טבליות מיובא של MyProtein"). Neither location contains "כולם" ("all") or any total-claim overreach
— both correctly state the accurate 3-Shufersal + 1-MyProtein-import split. No grocery-channel
overclaim exists in this file at either location the prior finding named.

**RT-2 status: RESOLVED** (independently reconfirmed; the fix commit's claim of "no change
needed" checks out against the live file, not just the commit message).

### New-defect scan on the changed text

- No antithesis banned pattern ("X, ולא Y" define-by-negation) introduced — the Creapure
  sub-SKU disambiguation ("היא טענת דף בלבד ואינה מעורבבת עם הרישום המאומת הזה") is a factual
  two-SKU distinction, not a stylistic negation, and mirrors the disambiguation pattern already
  used for Momentous's Creapure caveat (line 704-706) which passed the full prior red-team pass.
- Em-dash usage in the new/changed text (`rowVerdict` line 794, `confidenceLabel` line 799,
  `limitingFactors` line 802) is verbatim-identical boilerplate already used for the Klean
  Athlete and MegaFood rows ("מבוסס על מאגר NSF — מחיר לא נאסף בסבב זה" / "מחיר לא נאסף בסבב
  איסוף זה — לא ניתן לחשב מחיר לגרם אפקטיבי") — reused template phrasing, not a new instance of
  em-dash proliferation.
- No engine/BSIP2 jargon, no invented facts, no PMID/DOI touched.
- Score/grade: `score: null, grade: null` unchanged on the Sports Research row (and confirmed
  unchanged file-wide — no A-E grade token anywhere in `creatine-page-data.ts`, consistent with
  Product Ruling 1). Dose (5 גרם), price (`price_per_3g_label: null`, unchanged — still "מחיר לא
  נאסף בסבב זה") and `confidence: "partial"` are unchanged from the pre-fix version — diff
  confirms only `certTier`, `cert_label`, `insightLine`, `rowVerdict`,
  `expansion.confidenceLabel`, `expansion.positiveSignals`, `expansion.limitingFactors`, and
  `expansion.caveats` changed on this row.

### Build validation

- `cd C:\bari_wt_t492c\bari-web && npx tsc --noEmit` — exit 0, no output.
- `npm run build` — exit 0. `next build` (Turbopack) compiled successfully, static generation
  264/264 pages, `/hashvaot/creatine` listed as a compiled dynamic route (`ƒ /hashvaot/creatine`)
  with no build error.
- `node_modules` already present in the worktree; no install was required.

### RE-GATE Verdict

**GO.** Both prior blockers are resolved: RT-1 (CRITICAL, cert-count/list inconsistency) is
fixed with the count, badge, and every prose reference now agreeing at 7/13, correctly naming
Sports Research and correctly preserving its footnoted Creapure-sub-SKU caveat; RT-2 (HIGH,
grocery-channel overclaim) is confirmed correctly stated as 3-of-4, with no "all" overreach. No
new defect was introduced by commit `c5ab9b09`; the diff is narrowly scoped to exactly the two
findings it claims to fix. Build is clean (tsc + next build both exit 0). The benchmark
document's own summary-line miscount (`creatine_benchmark_solid_v1.md` line ~134, "6 of 13")
remains uncorrected in that source report — tracked as a benchmark-doc inconsistency, not a page
defect, not blocking (the page correctly ignores the stale summary arithmetic in favor of the
row-level evidence). RT-3, RT-5, RT-6, RT-7 (MEDIUM) remain open and out of scope for this
re-gate per delegation — not re-litigated here.

```json
{"re_gate_verdict":"GO","re_gate_date":"2026-07-04","commit":"c5ab9b09","rt1_status":"RESOLVED","rt2_status":"RESOLVED","new_defects_found":0,"open_mediums_not_relitigated":["RT-3","RT-5","RT-6","RT-7"],"tracked_not_blocking":["creatine_benchmark_solid_v1.md line ~134 summary miscount (6 vs true 7)","creatineWorldwideSectionLabel '6 מדינות' region-count label appears off-by-one vs 5 distinct region values in benchmark table — pre-existing, untouched by c5ab9b09, out of RT-1/RT-2 scope"],"build":{"tsc_noemit_exit":0,"next_build_exit":0,"route_compiled":"/hashvaot/creatine"}}
```
