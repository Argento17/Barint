# Creatine Guide — Recommendation Tier Mapping (Product decision doc)

**Task:** TASK-504 Wave 2 (מדריכים) — apply the ALREADY-ESTABLISHED 4-tier
`recommendation_tier_mapping` + `dose_adequacy_sole_caveat` split predicate
(`01_framework/nutrition/supplement_guides_bar_rubric_v1.yaml`, co-signed on the magnesium
guide 2026-07-04) to the creatine corpus. This is an APPLICATION of a standing rule, not a
re-litigation — see `magnesium_guide_recommendation_tiers_v1.md` for the mechanism's own
anti-drift ruling and defensibility argument, which are not repeated here.
**Author:** Product Agent · **Date:** 2026-07-04
**Status:** PROPOSAL. Rule mechanism = already co-signed (Nutrition D7 + Product, magnesium
doc). The bar-STATE ASSIGNMENTS for creatine's 31 products below are Product's own derivation
from the pulled data file and the rubric's creatine-specific thresholds — **these specific
assignments require a fresh Nutrition D7 accuracy check** before they govern copy (see §9).
No code, rubric, or data file is edited by this doc.

---

## 0. Premise check (Hard Rule 10 — verify before ruling)

- **Data source:** `bari-web/src/lib/comparisons/creatine-page-data.ts` on `origin/master`
  commit `9546878cf90f069fe12c1467d8d12966b40221cf` (PR #86), NOT present in the local
  worktree at authoring time — pulled via
  `git show origin/master:bari-web/src/lib/comparisons/creatine-page-data.ts`. Read in full:
  18 Israeli-shelf `buildProduct()`-equivalent entries (`creatineIsraeliProductsRaw`) + 13
  worldwide-benchmark entries (`creatineWorldwideProductsRaw`) = 31 total, matching the file's
  own header comment and `creatineMetadataLine` ("18 מוצרים מהמדף הישראלי · 13 מותגי ייחוס
  עולמיים"). 18 + 13 = 31 — confirmed against the artifact, not taken on the brief's assertion.
- **Rule source:** `01_framework/nutrition/supplement_guides_bar_rubric_v1.yaml` —
  `bars` (6 definitions incl. creatine-specific thresholds), `display_suppression_rule`,
  `recommendation_tier_mapping`, `passes_with_flag_split_rule` (`dose_adequacy_sole_caveat`).
  Both files were validated against each other by Nutrition at rubric-authoring time (rubric
  header line 13-16); this doc re-derives the creatine bar states independently against the
  same two artifacts rather than trusting that validation pass secondhand.
- **Every bar-state and price figure below is computed from the file's literal `mkBadge(...)`
  arguments** (dose figure, `doseHonesty`, `certTier`, `price_per_3g_label`) — none is
  eyeballed or remembered. Price-pool medians are shown with their arithmetic in §2 so the
  computation is independently checkable.

---

## 1. Displayed bar set for creatine — suppression check (deliverable 1)

Per `display_suppression_rule`: a bar suppresses from per-product display **only if** it is
100% CANNOT-VERIFY across every displayed product in the guide's corpus (31/31 here). Checked
each of the 6 bars against all 31 pulled rows:

| Bar | States present across 31 products | Uniform CANNOT-VERIFY (31/31)? | Displays? |
|---|---|---|---|
| `dose_adequacy` | PASS, FLAG, FAIL, CANNOT-VERIFY (all four) | No | **Yes** |
| `form_absorption` | PASS (monohydrate, 29/31), FLAG (HCl, 2/31 — Kaged, Con-Cret) | No | **Yes** |
| `third_party_verification` | PASS (7/31, all worldwide NSF-directory rows), FLAG (many), CANNOT-VERIFY (several), FAIL (1/31 — Naked Nutrition) | No | **Yes** |
| `price_fairness` | PASS, FLAG, FAIL (2/31 — Kaged, Con-Cret), CANNOT-VERIFY | No | **Yes** |
| `safety` | PASS — **31/31 uniform**, but uniform state is PASS, not CANNOT-VERIFY | No (wrong state for the trigger) | **Yes** — per the rubric's own guardrail, a uniform PASS is a determinate positive finding and stays visible unconditionally; only uniform CANNOT-VERIFY suppresses. |
| `label_transparency` | PASS, FLAG (1/31 — California Gold Nutrition capsules), FAIL (4/31 — the undisclosed-dose products) | No | **Yes** |

**Result: all 6 bars display for the creatine guide — none suppressed.** This matches the
rubric's own forward statement (`display_suppression_rule.re_evaluated_per_build`): "the same
bar renders normally wherever it discriminates: `third_party_verification` and
`price_fairness` both stay fully visible on the creatine guide today (7/N NSF-directory-verified
rows; real `price_per_3g_label` variance)." Confirmed directly against the pulled data, not
taken on the rubric's own forward-looking assertion alone. `safety`'s uniform-PASS state is a
genuine finding worth stating in copy ("no established upper limit exists for creatine — every
product on this page passes this bar by definition"), not a suppression case.

**Practical consequence for the split predicate:** because all 6 bars display for creatine
(unlike magnesium's 4), the `dose_adequacy_sole_caveat` caveat set below is computed over all
6 bars, not 4. This is the "creatine-specific wrinkle" the delegation named — a product whose
sole caveat is `third_party_verification` or `price_fairness` now routes to **טוב**, not
**מומלץ**, exactly as it would for a `form_absorption` or `safety` caveat.

---

## 2. Price-fairness pool medians (creatine-specific, per-currency)

Per `price_fairness.boundary_method`: separate, same-currency medians (₪ Israeli shelf vs $
worldwide benchmark), thresholds PASS ≤1.25× median, FLAG ≤2.0× median, FAIL >2.0× median,
range prices at arithmetic midpoint.

**Israeli ₪/3g pool** (10 price-disclosed rows, pulled directly from `price_per_3g_label`):
0.52, 0.61, 0.65, 0.77, 0.89, 0.97, 1.03, 1.20, 4.75, 5.38 → median (avg of 5th/6th) =
**₪0.93**. Matches the rubric's own cited snapshot (line 321: "0.93 ₪/3g Israeli creatine
pool… dated 2026-07-04") — independently re-derived, not copied. PASS ≤ ₪1.1625, FLAG
₪1.1625–1.86, FAIL > ₪1.86.

> **Flag for Nutrition (premise question, not resolved here):** the ₪0.97 row belongs to
> California Gold Nutrition's capsule product, whose `dose_adequacy` is **CANNOT-VERIFY**
> (per-unit dose, undisclosed daily count — see §5). The rubric's own `price_fairness`
> CANNOT-VERIFY definition says a CANNOT-VERIFY `dose_adequacy` should **cascade** to
> `price_fairness` = CANNOT-VERIFY, not a computed figure — yet ₪0.97 is computed and appears
> to be in the rubric's own median snapshot too (it reproduces cleanly only if that row is
> included). This doesn't change any tier outcome in this doc — California Gold's bucket is
> already forced to `cannot_assess` by the dose rule alone, and excluding the ₪0.97 row moves
> the IL median to ₪0.89, which does not flip any other product's PASS/FLAG/FAIL band. Flagging
> for Nutrition to settle which pool definition is authoritative before this ships in copy.

**Worldwide $/3g pool** (9 price-disclosed rows, range prices at midpoint): 0.165, 0.185,
0.195, 0.205, 0.225, 0.27, 0.34, 0.37, 0.44 → median = **$0.225**. Matches the rubric's own
cited snapshot exactly. PASS ≤ $0.28125, FLAG $0.28125–0.45, FAIL > $0.45.

---

## 3. The 4 tier definitions (carried over, unchanged mechanism)

| Tier | Maps from | Definition |
|---|---|---|
| **מומלץ מאוד** | `clears_all_bars` | All 6 bars = PASS. |
| **מומלץ** | `passes_with_flag`, split A | No FAIL; non-PASS set is EXACTLY `{dose_adequacy}`. |
| **טוב** | `passes_with_flag`, split B | No FAIL; non-PASS set contains any bar OTHER than `dose_adequacy` (whether or not dose is also in it). |
| **לא מומלץ** | `fails` | At least one bar = FAIL. |
| *(outside)* **לא ניתן להעריך** | `cannot_assess` | `dose_adequacy` = CANNOT-VERIFY and no bar = FAIL. |

Evaluation order (unchanged, mechanical, first match wins): FAIL anywhere → fails, checked
**before** the CANNOT-VERIFY dose check — a known-bad finding is never hidden behind an
"insufficient data" framing.

---

## 4. Per-product tier table — all 31 (deliverable 2)

Legend: P=PASS, FL=FLAG, FA=FAIL, CV=CANNOT-VERIFY. "Caveat set" = displayed bars ≠ PASS.

### Israeli shelf (18)

| # | Product | dose | form | 3rd-party | price | safety | label | Caveat set | Tier |
|---|---|---|---|---|---|---|---|---|---|
| 1 | NOW Foods — Sports Micronized Creatine (4.2g) | P | P | CV (no claim) | P (₪0.52) | P | P | {3rd-party} | **טוב** |
| 2 | ABE — Creatine Monohydrate Micronized (4.25g) | P | P | FL (Informed Sport, unchecked) | P (₪0.65) | P | P | {3rd-party} | **טוב** |
| 3 | MuscleTech — Platinum 100% Creatine (5.0g) | P | P | CV (HPLC claim ≠ 3rd-party cert) | P (₪0.77) | P | P | {3rd-party} | **טוב** |
| 4 | MyProtein — Impact Creatine 250g (3.0g) | P | P | FL (Informed Choice, unchecked) | P (₪1.03) | P | P | {3rd-party} | **טוב** |
| 5 | All In — אבקת קריאטין (3.0g) | P | P | CV (no claim) | FL (₪1.20) | P | P | {3rd-party, price} | **טוב** |
| 6 | Optimum Nutrition — Micronized Creatine Powder (5.0g) | P | P | FL (Informed Choice, unchecked) | P (₪0.61) | P | P | {3rd-party} | **טוב** |
| 7 | Thorne (IL/iHerb) — Creatine (5.0g) | P | P | FL (NSF claimed; US registry verified, this IL SKU not separately checked) | P (₪0.89) | P | P | {3rd-party} | **טוב** |
| 8 | California Gold Nutrition — Sport Pure Creatine capsules (0.75g/capsule, daily count undisclosed) | **CV** (per-unit dose, no daily count) | P | FL (iTested, unchecked) | ⚠ inconsistent (see §2) | P | FL (per-unit disclosed, no daily instruction) | n/a — dose CV routes bucket directly | **לא ניתן להעריך** (outside tiers) |
| 9 | MyProtein — Creatine Gummies (3.0g = 3×1g) | P | P | CV (no claim) | CV (not collected) | P | P | {3rd-party, price} | **טוב** |
| 10 | MyProtein — Creatine Monohydrate Elite, IL (3.0g, general) | P | P | FL (Informed Choice, unchecked) | CV (not disclosed) | P | P | {3rd-party, price} | **טוב** |
| 11 | MyProtein — THE Creatine Creapure, IL (3.0g) | P | P | FL (Informed Choice, unchecked) | CV (not disclosed) | P | P | {3rd-party, price} | **טוב** |
| 12 | Kaged — Creatine HCl (0.75g) | **FA** (<1.5g floor) | FL (alt form, no evidenced advantage) | FL (Informed Sport, unchecked) | FA (₪4.75, >1.86 cap) | P | P | n/a — FAIL present | **לא מומלץ** |
| 13 | Con-Cret — Creatine HCl (0.75g) | **FA** | FL | FL (NSF claimed, IL SKU not separately verified) | FA (₪5.38) | P | P | n/a | **לא מומלץ** |
| 14 | MyProtein — Creapure Micronised Capsules (2.8g) | FL (1.5≤2.8<3.0) | P | CV (no claim) | CV (not disclosed) | P | P | {dose, 3rd-party, price} | **טוב** |
| 15 | Super Effect — קריאטין מונוהידראט ענבים (undisclosed) | CV | P (monohydrate named) | CV | CV | P | **FA** (creatine named, zero quantification) | n/a — FAIL present | **לא מומלץ** |
| 16 | Super Effect — קריאטין מונוהידראט פירות (undisclosed) | CV | P | CV | CV | P | **FA** | n/a | **לא מומלץ** |
| 17 | Sport GS — אבקת קריאטין מונוהידראט (undisclosed) | CV | P | CV | CV | P | **FA** | n/a | **לא מומלץ** |
| 18 | MyProtein — Creatine Monohydrate Tablets (undisclosed) | CV | P | CV | CV | P | **FA** | n/a | **לא מומלץ** |

### Worldwide benchmark (13)

| # | Product | dose | form | 3rd-party | price | safety | label | Caveat set | Tier |
|---|---|---|---|---|---|---|---|---|---|
| 19 | Thorne (worldwide) — Creatine Micronized (5.0g, NSF id 1204244) | P | P | P (directory-verified) | P ($0.27) | P | P | {} | **מומלץ מאוד** |
| 20 | Momentous — Creatine Monohydrate (5.0g, NSF id 1285010) | P | P | P | P ($0.225) | P | P | {} | **מומלץ מאוד** |
| 21 | Klean Athlete — Klean Creatine (5.0g, NSF id 1121640) | P | P | P | CV (not collected) | P | P | {price} | **טוב** |
| 22 | BPN — Creatine Monohydrate (5.0g, NSF id 1635096) | P | P | P | P ($0.185) | P | P | {} | **מומלץ מאוד** |
| 23 | MegaFood — Micronized Creatine Monohydrate (5.0g, NSF directory) | P | P | P | CV (not collected) | P | P | {price} | **טוב** |
| 24 | Sports Research — Creatine Monohydrate Unflavored (5.0g, NSF id 1751614) | P | P | P | CV (not collected) | P | P | {price} | **טוב** |
| 25 | BioSteel — Creatine, 72 servings (2.5g, NSF id 1292599) | FL (1.5≤2.5<3.0) | P | P | P ($0.205, dose-normalized to 3g) | P | P | {dose} | **מומלץ** |
| 26 | Naked Nutrition — Naked Creatine (5.0g, "NSF-certified" claimed) | P | P | **FA** (checked against NSF registry, not found) | P ($0.195) | P | P | n/a — FAIL present | **לא מומלץ** |
| 27 | Applied Nutrition — Creatine Monohydrate 100% (5.0g, Informed-Sport) | P | P | FL (checker site blocked every attempt) | P ($0.165) | P | P | {3rd-party} | **טוב** |
| 28 | MyProtein (worldwide) — Creatine Monohydrate Elite (3.4g, general) | P | P | FL (Informed-Sport, unchecked) | FL ($0.37) | P | P | {3rd-party, price} | **טוב** |
| 29 | MyProtein (worldwide) — THE Creatine Creapure (3.4g) | P | P | FL (Informed Choice, unchecked) | FL ($0.44) | P | P | {3rd-party, price} | **טוב** |
| 30 | Switch Nutrition — Perform Purest Creatine (3.0g, HASTA) | P | P | FL (registry not checked this round) | CV (not collected) | P | P | {3rd-party, price} | **טוב** |
| 31 | ESN — Ultrapure Creatine Monohydrate (3.5g, no claim) | P | P | CV (no claim) | FL ($0.34) | P | P | {3rd-party, price} | **טוב** |

---

## 5. `cannot_assess` ruling — California Gold Nutrition capsules (unique case, deliverable 2/3)

**Tier: לא ניתן להעריך, OUTSIDE the 4 ranked tiers — same ruling as magnesium's TRIOMAG.**

This is the exact per-unit-dose-with-undisclosed-daily-count pattern the rubric names
*verbatim* as the reason `dose_adequacy` CANNOT-VERIFY exists ("a PER-UNIT dose is stated…
but the required daily serving count is not disclosed… see California Gold Nutrition
capsules"). The live copy's own `limitingFactors` confirms it in Hebrew: "כמות הכמוסות
היומית הנדרשת לא מפורטת על התווית" (the required daily capsule count is not specified on the
label). Per `bucket_logic.evaluation_order`, this routes to `cannot_assess` because **no bar
on this product is FAIL** — `label_transparency` is FLAG (a real number is disclosed, just not
resolvable to a daily total), not FAIL, and everything else is PASS or FLAG. Contrast with
rows 15–18 (Super Effect ×2, Sport GS, MyProtein Tablets): those carry **zero** quantification
anywhere, which the rubric distinguishes as `label_transparency` = FAIL — a known labeling
defect, not a data gap — so they correctly route to `fails` (checked first in evaluation
order) rather than `cannot_assess`, even though all four also have `dose_adequacy` = CANNOT-VERIFY.
This is the same "Tink Oxide-520 vs TRIOMAG" distinction the magnesium precedent doc names —
a known-bad finding is never hidden behind an "insufficient data" framing, and a genuine
unknowable is never presented as an actionable negative.

---

## 6. Tier distribution (deliverable 3)

| Tier | Israeli (of 18) | Worldwide (of 13) | Combined (of 31) |
|---|---|---|---|
| מומלץ מאוד | 0 | 3 (Thorne, Momentous, BPN) | **3** |
| מומלץ | 0 | 1 (BioSteel) | **1** |
| טוב | 11 | 8 | **19** |
| לא מומלץ | 6 | 1 (Naked Nutrition) | **7** |
| לא ניתן להעריך (outside) | 1 (California Gold Nutrition) | 0 | **1** |
| **Total** | 18 | 13 | **31** |

Denominators: 0+0+11+6+1 = 18/18 (Israeli); 3+1+8+1+0 = 13/13 (worldwide); 3+1+19+7+1 = 31/31
(combined). Every count above traces to a named row in §4, not an estimate.

**Notable findings:**

1. **The Israeli shelf structurally cannot reach מומלץ or מומלץ מאוד today.** 0/18 Israeli
   products are NSF-directory-verified (`third_party_verification` is never PASS for an
   Israeli row — only FLAG or CANNOT-VERIFY), which means `third_party_verification` is
   *always* in the non-PASS set for every Israeli product that isn't already `fails` or
   `cannot_assess`. Since the split rule routes any caveat set containing a non-dose bar to
   **טוב**, no Israeli product can land above טוב regardless of how clean its dose, form, and
   label are. This is a mechanical consequence of the certification data, not a Product
   judgment call — worth stating plainly in guide copy (it is itself the headline finding, the
   same way magnesium's empty מומלץ מאוד tier was its headline finding).
2. **Naked Nutrition — Naked Creatine → לא מומלץ.** The only product in the entire 31-row
   corpus with a `third_party_verification` FAIL: a manufacturer "NSF-certified" claim that
   was actively checked against the NSF registry and found to have no matching entry. This is
   a label-integrity finding, not a "just hasn't been checked yet" case — it renders in the
   most severe tier despite an otherwise clean dose/form/price profile, exactly as the rubric's
   FAIL-vs-FLAG distinction requires.
3. **Two HCl products (Kaged, Con-Cret) double-fail** — dose (<1.5g floor) AND price
   (6–10× the effective-gram cost of an honest monohydrate, per the file's own prologue
   framing). Their `form_absorption` state is correctly **FLAG, never FAIL** — the rubric
   explicitly bans a "HCl is unsafe/lower-quality" framing; the dose and price bars carry the
   actionable finding, not the form bar.
4. **No loading-phase product exists in the 31-product corpus** — the rubric's
   `loading_phase_exception` is defined for forward compatibility only and does not fire on
   any current row. Confirmed by reading all 31 dose labels; none states a ~20g/day, 4×5g
   protocol.
5. **BioSteel is the sole מומלץ** — 2.5g, below the 3.0g PASS floor but within the FLAG band,
   with every other bar (including third-party, directory-verified) clean. It is the single
   product in the corpus that demonstrates the split rule's intended positive case: "the only
   open question is dose quantity, which a consumer can self-correct."

---

## 7. Creatine-specific display notes for the build (deliverable 4)

- **Bars shown:** all 6 (`dose_adequacy`, `form_absorption`, `third_party_verification`,
  `price_fairness`, `safety`, `label_transparency`) — none suppressed (§1). This differs from
  the magnesium guide (4 of 6 shown) and must not be built by copying magnesium's suppressed-bar
  list; it is a build-time computation per corpus, not a hardcoded per-guide list (rubric's own
  standing rule).
- **Safety — "always PASS" framing:** creatine has no established UL; every one of the 31
  products passes this bar by construction. Copy should state this once, plainly, as a
  genuine finding ("no upper limit is established for creatine; every product here clears
  this bar") — not as a suppressed/redundant badge (per §1, uniform PASS stays visible,
  unlike uniform CANNOT-VERIFY).
- **Monohydrate vs. alternative-form handling:** `form_absorption` = PASS for monohydrate in
  *any* branded sub-line (general, Creapure, "Elite" naming) — form identity, not brand
  marketing, drives the state. HCl and any future alternative form (buffered/alkaline, ethyl
  ester, citrate, malate) = FLAG, **never FAIL** — the evidence base calls these
  "evidence-orphaned for a premium claim," explicitly not inferior or unsafe. No creatine form
  in the current corpus reaches FAIL on this bar; FAIL is reserved and unpopulated at v1.
- **Bipolar scoped note:** attaches **only** where mood/depression framing appears in copy —
  never as a per-product bar or blanket flag. In the current 31-row corpus, **no product's
  `insightLine`/`rowVerdict` carries mood/depression framing**; that content lives only in the
  category-level `creatineEvidenceSections` "safety" topic (a general educational paragraph).
  The build should render the caution there, at the category level, and must not attach it to
  any individual product row unless and until a product's own copy makes a mood/depression
  claim.
- **Two-tier certification language:** "אומת מול מאגר" (PASS) reserved for the 7
  NSF-directory-confirmed worldwide rows; "מוצהר על-ידי היצרן" (FLAG or FAIL depending on
  whether a check was attempted) for everything else; "no claim" (CANNOT-VERIFY) carries zero
  penalty per the missing-data-discard doctrine — ESN's honest no-claim framing is the
  existing, correct precedent to reuse, not rewrite.

---

## 8. Anti-drift confirmation (Hard Rule 1, carried over — not re-litigated)

No new numeric field, sum, average, or percentage is introduced by this doc. Every tier
assignment in §4 is a lookup over the 6 already-defined bar states using the
`dose_adequacy_sole_caveat` set-identity predicate already co-signed at the mechanism level
(magnesium doc §2/§6). This doc applies that mechanism to a second, larger, differently-shaped
corpus (real third-party and price variance vs. magnesium's suppressed pair) and finds it
holds without modification — no new predicate, no new bucket, no new bar-state was needed to
handle creatine's data shape. The price-pool medians (§2) are computed values used only to
place a product in a PASS/FLAG/FAIL band, never displayed as a number to the consumer and
never summed across bars.

---

## 9. Required sign-offs before Frontend builds (deliverable 5)

1. **Nutrition D7 co-sign — bar-state accuracy — OUTSTANDING, requesting now.** The
   *mechanism* (`dose_adequacy_sole_caveat`, bucket_logic, display suppression) is already
   co-signed at the rubric level. What is **not yet co-signed** is whether Product correctly
   *applied* it to these 31 specific products. Please verify specifically:
   - The `third_party_verification` PASS/FLAG/FAIL calls — especially Naked Nutrition's FAIL
     (checked-and-not-found) vs. every FLAG (unchecked or blocked), and the Thorne IL-vs-worldwide
     split (same brand, different verification status per regional SKU).
   - The price-pool median computation in §2, including the California Gold Nutrition
     cascade-vs-computed-value flag (does not change any tier outcome, but the pool
     definition should be settled).
   - California Gold Nutrition's `dose_adequacy` = CANNOT-VERIFY / `cannot_assess` placement
     (the creatine analogue of the magnesium precedent) and the `label_transparency` FAIL calls
     on the 4 fully-undisclosed products.
   - The HCl products' `form_absorption` = FLAG (never FAIL) framing, to confirm no
     inferiority/unsafety language leaks into copy built from this table.
2. **C3 challenge** — recommend one independent pass on this doc's specific bar-state
   assignments (not the already-settled mechanism), per the standing C3-at-forks discipline.
3. **Content + Adversarial QA two-gate** on all consumer-facing strings once the above land —
   fully outstanding; no creatine tier-related consumer string is drafted by this doc.

---

## 10. What this doc does NOT decide

- Exact Hebrew copy for tier labels, sub-captions, or the California Gold Nutrition
  cannot-assess explanation — Content Agent drafts, both gates sign off.
- Whether/how to word the price-pool median flag (§2) in consumer copy, if at all — that is a
  Nutrition + Content call once the pool-definition question is settled.
- Implementation (component, prop, computed field) — Frontend Agent's call once scope is
  approved; Product approves scope only (D11).
- Whether the creatine guide ships before or after the outstanding sign-offs in §9 close —
  that is an orchestrator sequencing call, not decided here.

---

## Return Contract

```json
{
  "task": "TASK-504-creatine-4tier-recommendation",
  "agent": "Product Agent",
  "artifacts": [
    {
      "path": "C:\\Bari\\03_operations\\reports\\product\\creatine_guide_recommendation_tiers_v1.md",
      "sha256": "618b30431fa06eb1c898a7f2af43f1f226277b0be8a990e50360a6da45836c84"
    }
  ],
  "counts": {
    "total_products_in_corpus": 31,
    "israeli_of_31": 18,
    "worldwide_of_31": 13,
    "bars_displayed_of_6": 6,
    "bars_suppressed_of_6": 0,
    "tier_distribution_of_31": {
      "מומלץ מאוד": 3,
      "מומלץ": 1,
      "טוב": 19,
      "לא מומלץ": 7,
      "לא ניתן להעריך (outside tiers)": 1
    },
    "tier_distribution_israeli_of_18": {
      "מומלץ מאוד": 0,
      "מומלץ": 0,
      "טוב": 11,
      "לא מומלץ": 6,
      "לא ניתן להעריך (outside tiers)": 1
    },
    "tier_distribution_worldwide_of_13": {
      "מומלץ מאוד": 3,
      "מומלץ": 1,
      "טוב": 8,
      "לא מומלץ": 1,
      "לא ניתן להעריך (outside tiers)": 0
    },
    "third_party_directory_verified_of_31": 7,
    "third_party_fail_checked_not_found_of_31": 1,
    "price_pool_median_israeli_ils_per_3g": 0.93,
    "price_pool_median_worldwide_usd_per_3g": 0.225,
    "source": "git show origin/master:bari-web/src/lib/comparisons/creatine-page-data.ts @ 9546878cf90f069fe12c1467d8d12966b40221cf (31 product entries, read in full); cross-checked against 01_framework/nutrition/supplement_guides_bar_rubric_v1.yaml bars + display_suppression_rule + recommendation_tier_mapping"
  },
  "commands_run": [
    {"cmd": "git show origin/master:bari-web/src/lib/comparisons/creatine-page-data.ts > scratchpad/creatine-page-data.ts", "exit_code": 0},
    {"cmd": "git log -1 --format=%H origin/master -- bari-web/src/lib/comparisons/creatine-page-data.ts", "exit_code": 0}
  ],
  "not_done": [
    "Nutrition D7 co-sign on the 31 specific bar-state assignments in this doc — outstanding, requested in §9",
    "C3 independent challenge pass on this doc's assignments (not the already-settled mechanism)",
    "Content Agent + Adversarial QA two-gate on any consumer-facing tier copy — not drafted here",
    "Resolution of the California Gold Nutrition price-pool inclusion question (§2) — flagged for Nutrition, not resolved unilaterally; does not change any tier outcome in this doc",
    "No code, rubric, or data file edited — proposal/decision-record only"
  ],
  "acceptance_test": {
    "spec": "Produce a decision doc: displayed-bar set, per-product tier table (all 31), tier distribution, creatine-specific display notes, and the Nutrition co-sign flag, every number traced to the pulled data file or the rubric YAML.",
    "result": "PASS — all elements present; every count in `counts` above traces to a named artifact (creatine-page-data.ts at the cited commit, or the rubric YAML); zero numbers invented; two premise-check flags raised (California Gold Nutrition price cascade, price-pool inclusion question) rather than silently resolved, per Hard Rule 10 and the Spec-Conflict Duty."
  }
}
```
