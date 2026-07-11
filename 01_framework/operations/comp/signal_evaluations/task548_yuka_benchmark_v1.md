# TASK-548 — Yuka Benchmark vs BSIP: Positioning Memo

**Prepared:** 2026-07-09 · **Owner:** marketing-agent · **Reviewer:** product-agent
**Status:** Competitive-intelligence + positioning memo — NOT consumer copy, NOT a scoring proposal, NOT a shipped campaign.
**Scope guardrails:** No scoring/methodology change is authorized by this document (Hard Rule: signal, not evidence — Project Comp discipline). OFF (`gl-002` in the source registry) is a *monitored competitor* only — never a Bari data source (project-wide OFF ban, absolute). Positioning lines in §3 are concepts routed to Content Agent (two-gate: Content + Adversarial QA) before any consumer-facing use — Marketing does not author or publish final Hebrew copy. Any content/campaign action naming Yuka is a public product claim and requires Product Agent approval (D14) before publication, per the Decision Rights table.
**Precedent:** builds on `C:\Bari\reports\comp_brief_kaspenu_yuka_v1.md` (2026-06-13, Kaspenu+Yuka threat brief) — this memo updates the Yuka half with the 2026-07-09 signal and narrows to the specific deliverable: mechanism benchmark, positioning angles, one recommended next step.

---

## 1. The signal (as relayed by Project Comp, 2026-07-09 — signal, not independently re-verified by Marketing this pass)

Sources named in the dispatch: PRNewswire (LatAm launch), FoodNavigator (Yuka drives reformulation), Washington Post, ceotodaymagazine. Facts as given:
- Yuka launched in **Brazil + Mexico, July 8, 2026**; now claims **~85M users across 15 countries** (up from ~80M/14 countries reported by FoodNavigator on 2026-02-09 per the 2026-06-13 brief — consistent growth trajectory, not a step-change).
- Its **"message-the-brand" feature** drove **Chobani to remove dipotassium phosphate** from an oat-milk product — a concrete, named reformulation event (the same pressure-loop mechanism FoodNavigator already documented at scale: −13% high-risk additives in Yuka's French DB since 2019, −58% in breakfast cereals).
- **Public formula confirmed: 60% nutritional value / 30% additives / 10% organic bonus**, output 0–100. This matches the 2026-02-09 FoodNavigator methodology already on file — no formula change, just reconfirmation at LatAm-launch visibility.
- **Growing criticism that it oversimplifies** — notably from brands that score *well* under Yuka, questioning whether one rank number can represent a food. This is new emphasis vs the June brief (which had dietitian/cocktail-effect and hazard-vs-dose critiques); the "even winners are uncomfortable with one number" framing is the sharpest new opening.

---

## 2. Mechanism benchmark — Yuka's 60/30/10 vs how BSIP actually works

This section is checked against `.claude/scoring.md` (BSIP2 Prototype v0, algorithm 0.4.1) — not marketing description.

| Dimension | Yuka | BSIP2 (Bari) |
|---|---|---|
| **Formula shape** | 3 fixed weighted buckets (nutrition 60% / additives 30% / organic 10%), same formula for every product in every category, worldwide. | **10 weighted dimensions** (processing_quality 15%, nutrient_density 15%, calorie_density 15%, glycemic_quality 12%, protein_quality 10%, additive_quality 10%, fat_quality 8%, satiety_support 6%, regulatory_quality 5%, whole_food_integrity 4%) — a finer-grained composite, not a 3-bucket average. |
| **Category awareness** | None documented — same score meaning applied globally (a "72" reads the same whether it's a cracker or a beverage). | **Category-relative by construction.** `calorie_density` alone runs against per-category tables (e.g. beverage normal range ≈10–100 kcal vs whole_food_fat ≈350–900 kcal) — the same raw number is interpreted differently depending on what it's being compared to. Router v2 assigns category before scoring runs. |
| **Guardrails beyond the weighted sum** | Not documented beyond the 3-bucket weighting. | **Caps, floors, vetoes, and a 4-pattern hyperpalatability detector** (fat-sugar, fat-sodium, refined-carb-fat, crunch-sweet) layered on top of the weighted dimensions, plus **concern coordination** — a family-budget mechanism that stops the same root issue (e.g. sodium) from being penalized twice through two different dimensions. |
| **Data source for the underlying label logic** | Nutri-Score + a proprietary additive-risk list (per FoodNavigator/June brief). | **Direct product scrape only** (Shufersal/Yohananof/Carrefour/Wolt) → BSIP1 Hebrew ingredient enrichment → BSIP2 trace. OFF is explicitly banned as a source at every stage. No resold third-party score is ever a Bari input. |
| **When data is incomplete** | Not documented — the app appears to score whatever is in its database. | **3 explicit confidence states, always shown, never blank:** Verified (score as-is), Partial (score + qualifier + a sentence naming exactly what's unverified), Insufficient (no score, one sentence explaining why). `CONFIDENCE_INSUFFICIENT_CEILING` / `CONFIDENCE_LOW_CEILING` mean a low-confidence product structurally **cannot** score high regardless of what the signals say. |
| **Consumer-facing display** | 0–100 score with color-coded rating (per prior brief). | **`[score] / [grade]` only** — a 6-grade S–E letter as a range marker, explicitly **no colored good/bad backgrounds** (Score Presentation v1, Rule: "colored score backgrounds... encode judgment invisibly, same problem as a text label"). The row itself is a **2-line human verdict** (standing → why → catch → earned grade), not a bare number. |
| **Traceability** | Black box to consumers and to manufacturers — Yuka declines all manufacturer requests to discuss/improve scores (FoodNavigator). | Per-product BSIP2 trace JSON records which of the 10 dimensions fired, which caps/floors/vetoes applied, and why — inspectable in principle at the trace level, not just a final number. |

**Honest read:** Yuka's 60/30/10 is not "wrong," it's a **deliberately simple, portable formula** — that simplicity is exactly what let it scale to 85M users across 15 countries with one engine. BSIP's category-relative, multi-dimension, confidence-gated design is **more accurate per product** but **structurally harder to explain in one sentence and harder to port to a new category** (new category = new calorie-density table, new router anchors, new context gates — evidenced by the documented router gaps for bread/cracker archetypes). That trade-off is real and should not be marketed away.

---

## 3. Where each is genuinely ahead (honest, both directions)

**Yuka is stronger on:**
1. **Reach and the in-aisle moment.** 85M users, barcode-scan-in-store use case. Bari is a web comparison destination — a different, slower-to-reach moment of need (already flagged in the June Kaspenu brief; still true).
2. **The brand-pressure loop.** "Message the brand" turned consumer attention into a documented reformulation (Chobani, dipotassium phosphate) — a live distribution/product-influence mechanism Bari has no analog for today.
3. **One-sentence explainability.** 60/30/10 is easy to say out loud. BSIP's 10-dimension category-relative model is not — that's a real marketing cost, not just a technical nuance.

**Bari is genuinely differentiated on:**
1. **Category-relative math vs one universal formula** — a mechanism difference (§2), not a branding claim.
2. **Confidence as a first-class, always-shown state** — "insufficient data → no score, and we say why" vs an app that (as documented) scores whatever's in its database without a visible confidence signal.
3. **Judgment over a bare number** — the human verdict row + explicit ban on color-as-judgment is Bari's structural answer to the *exact* "oversimplifies to one rank" criticism Yuka's own well-scoring critics are now raising. This is not a marketing spin invented for this memo — it is already the standing editorial and presentation law (`comparison_row_verdict_model`, `score_presentation_v1` Rule 5 and the color-backgrounds prohibition), predates this signal, and is simply worth surfacing now that the market is asking the question.

---

## 4. The oversimplification opening — 3 positioning angle concepts

**These are concept directions for Content Agent to draft into real Hebrew copy through the two-gate (Content + Adversarial QA). They are not final consumer strings. Each is checked true against §2/§3 above — no puffery, no claim BSIP can't back at the trace level.**

1. **"One formula, every food, everywhere" vs "a score that knows what category it's judging."**
   Concept: Yuka runs the identical 60/30/10 weighting on a cracker, a beverage, and a jar of tahini. BSIP's calorie-density and dimension weighting are category-relative by construction — the number means something different, on purpose, depending on the shelf. This is the most mechanically defensible angle because it is a direct, checkable architecture difference (§2 row 2).

2. **"We say when we don't know" vs a score that's silent about what it's missing.**
   Concept: Bari's 3 confidence states (verified / partial / insufficient) are always shown, never blank — an "insufficient" product gets **no score and a stated reason**, not a number computed on incomplete data. Direct counter to the exact critique now surfacing about Yuka: "even brands that score well question boiling food down to one rank" — Bari's answer is structural, not rhetorical: it declines to rank rather than guess.

3. **"A verdict, not just a color."**
   Concept: Bari never shows a red/yellow/green badge — that is an explicit written rule (Score Presentation v1), because color-coding a score is functionally the same judgment-collapse the app-critics are naming. Every product gets a 2-line human verdict (what's true, what limits it, the earned grade) instead of a color. This is the sharpest "we already built the fix for the criticism you're reading about Yuka" line — but it must be phrased as *description of how Bari works*, never as a direct dig at Yuka by name in a way Content/QA would need to fact-check for fairness and legal exposure.

**Guardrail carried forward from the June brief:** angle 1 and 2 only hold if BSIP's category tables and confidence gating stay genuinely enforced in the engine — these are descriptions of what the engine already does, not aspirational claims. If either drifts, the positioning breaks with it.

---

## 5. Actionable takeaway — pulled number + recommended next step

**Pulled (real, this pass):** Hebrew-language search interest for **"יוקה"** (Yuka) in Israel, via `integrations/clients/google_trends.py` (`interest_over_time`, geo=IL, hl=he, timeframe=today 12-m). Tool status: DORMANT/fenced, unofficial Google Trends endpoint, relative 0–100 index, directional only — used here strictly for **content-sequencing signal**, never for scoring or a product verdict (hard fence per the client's own docstring, honored).

- **recent_avg = 48.9, baseline_avg = 36.6, momentum = +33.6%, is_rising = True, n = 53 weekly points.**
- Read: Hebrew search interest in "יוקה" inside Israel is real and **rising**, not flat or fading — there is already a live, growing Hebrew-speaking audience searching the brand name Bari would be positioning against.
- Attempted `rising_queries('יוקה')` (related Hebrew query breakdown) — **failed, HTTP 429** (rate-limited; documented as expected behavior of this unofficial endpoint). Not retried this pass to avoid burning the fenced tool's goodwill; retry is cheap and low-risk if this becomes a live work item.
- **GSC** (Search Console) status: NEEDS-ENV-VERIFY — `GSC_ACCESS_TOKEN`/`GSC_SITE_URL` not set as of 2026-07-09. Not pulled this pass. No Yuka-adjacent Hebrew query data exists in GSC today because Bari has no page targeting that intent yet.
- **GA4**: not pulled — there is no existing Bari landing page or content addressing Yuka, so there is no behavior number to report yet (not applicable pre-content, not a gap in this memo).

**Recommendation (single best next step, not a menu):** commission a **Hebrew-language explainer/FAQ page** (content brief only, via the `bari-seo` GEO/near-page-one loop and `content-strategy`) answering the rising Hebrew query intent around "מה זה יוקה" / "יוקה" / "אפליקציית סריקת מזון" — built around positioning angles 1 and 2 from §4 (category-relative math, confidence-as-first-class-state), explicitly honest that **Bari is a web comparison destination, not an in-aisle barcode scanner** (do not imply parity Bari doesn't have — §3 weak points stand). This is a **site-wide positioning/explainer asset**, not a new category launch, so it does not trip the category go-live gate — but naming a named competitor and making a mechanism comparison **is a public product claim**, so it requires **Product Agent approval under D14** before Content/QA drafting begins, and both gates (Content + Adversarial QA) before any Hebrew string ships.

**Falsifiability checks + leading indicators (Hard Rule 8):**
1. **Demand persistence** — re-run `google_trends.py interest_over_time('יוקה', geo='IL')` on **2026-08-06** (4 weeks out). If `recent_avg` has fallen below 40 or `momentum` has gone negative, the rising-demand premise weakened and this should demote from priority P1 to P3 (watch), stated plainly rather than shipped anyway.
2. **Ranking success** — once published and indexed, GSC average position for the target Hebrew query cluster ("יוקה" + "מה זה יוקה" + "אפליקציית סריקת מזון") should reach **avg position ≤10 within 8 weeks of publish**. Source: Search Console (manual GSC UI export until `GSC_ACCESS_TOKEN` is wired — flagged NEEDS-ENV-VERIFY above). If it doesn't reach page-1 visibility in that window, say so — don't keep the page quietly in the editorial calendar as a win.
3. **Engagement once live** — GA4 `run_report` on the new page's `landingPage`, `engagementRate` vs site median, first 30 days of real traffic. **Mandatory caveat: GA4 covers the consenting subset only and undercounts cold/bouncing search traffic — the exact segment this SEO bet targets** — so this is a secondary confirmation signal, not the primary falsifiability check (GSC position is).

---

## 6. Routing summary

| Action | Owner | Gate |
|---|---|---|
| Approve/reject the Yuka-explainer content brief as a public product claim | **product-agent** | D14 — required before Content drafting starts |
| Draft actual Hebrew copy from angles 1–3 | **content-agent** | Two-gate: Content + Adversarial QA before any consumer-facing use |
| Adversarial fact-check of every comparative claim against §2 (fairness, defensibility, no fabricated Yuka detail) | **adversarial-qa-agent** | Before publish |
| Re-run Trends check 2026-08-06 | **marketing-agent** | Self — leading indicator #1 above |
| GSC credential wiring (`GSC_ACCESS_TOKEN`/`GSC_SITE_URL`) | outside this memo's scope — flagged NEEDS-ENV-VERIFY, not actioned here | — |

---

## Sources (as relayed by Project Comp, 2026-07-09 dispatch — outlet names as given, not independently re-fetched by Marketing this pass)

- PRNewswire — Yuka Brazil + Mexico launch, July 8, 2026; ~85M users / 15 countries.
- FoodNavigator — Yuka drives reformulation via "message the brand" (Chobani / dipotassium phosphate); reconfirms 60/30/10 formula; growing oversimplification criticism. (Consistent with FoodNavigator 2026-02-09 article already on file in `reports/comp_brief_kaspenu_yuka_v1.md` — 80M/14 countries, same methodology, same reformulation mechanism at smaller scale.)
- Washington Post — referenced re: oversimplification criticism (not independently re-fetched this pass).
- ceotodaymagazine — referenced re: LatAm launch / criticism (not independently re-fetched this pass).
- Internal: `C:\Bari\.claude\scoring.md` (BSIP2 mechanism, verified 2026-06-01), `C:\Bari\01_framework\editorial\score_presentation_v1.md`, `C:\Bari\memory-archive\comparison_row_verdict_model.md`, `C:\Bari\reports\comp_brief_kaspenu_yuka_v1.md` (2026-06-13 precedent), `C:\Bari\01_framework\operations\comp\source_registry_v1.yaml` (gl-001 Yuka, gl-002 OFF).
- Pulled live 2026-07-09: `integrations/clients/google_trends.py::interest_over_time('יוקה', geo='IL', hl='he', timeframe='today 12-m')`.
