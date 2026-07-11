# Supplement Guides — Concrete Plan v1 (TASK-504)

**Author:** Orchestrator (C4), synthesizing all four consults.
**Inputs:** brief (`supplement_guides_redirection_brief_v1.md`) · Product co-sign
(`03_operations/reports/product/supplement_guides_product_cosign_v1.md`) · Nutrition science
co-sign (`01_framework/nutrition/supplement_guides_science_cosign_v1.md`) · Strategy red-team
(`tasks/returns/TASK-504_strategy_redteam_v1.md`, 2 CRITICAL / 4 HIGH / 4 MEDIUM) · C3
challenge (`tasks/returns/P500_return.md`, support-with-changes).
**Status:** AWAITING OWNER APPROVAL. Nothing builds until the owner accepts.

---

## 0. Consult scoreboard + two corrections

- **Convergence (all four, independently):** retire ORDINAL ranking; keep VERDICTS; express
  them as explicit per-attribute bar-states; magnesium keeps form-tier bands + UL flags
  (fully-flat there would be less honest, since its form-absorption gap is real where
  creatine's isn't).
- **Correction 1 (orchestrator):** C3 and Product both reported "no creatine frontend
  exists" — an artifact of the stale local tree. `/hashvaot/creatine` IS live on
  origin/master (PR #86, render-verified on bari.digital). Their format judgments survive;
  their asset-inventory claims were corrected here.
- **Correction 2 (red-team CRITICAL, absorbed honestly):** GA4 shows ~zero real-user
  evidence on both pages (magnesium 8 pageviews / creatine 0 since 2026-06-01). This pivot
  is a product-judgment call, which is the owner's strategic lane and legitimate — but it
  means (a) any "prove the format via engagement vs baseline" metric is meaningless today,
  and (b) migration risk is near-zero (nothing to lose). The plan reflects both.

## 1. The verdict layer (the core design decision — single recommendation)

Per-product, per-attribute **bar-states**: **PASS / FLAG / FAIL / CANNOT-VERIFY** (Nutrition +
C3 converged on identical semantics). Page-level, products group into the resulting buckets:

- **עובר את כל ספי הקנייה** (clears every bar) — unordered. This IS the owner's shortlist,
  honestly labeled as a threshold verdict, with the inclusion criteria stated on-page
  ("any product meeting these bars appears here"), per red-team's stealth-endorsement guard.
- **עובר עם דגל** (passes with a flag) · **לא עובר** (fails) · **לא ניתן להעריך**
  (cannot be assessed — e.g., undisclosed dose, unresolved form).
- **Plus ONE transparent default pick** (Product's decisiveness amendment): "הבחירה
  הפשוטה" — the cheapest per effective unit among all-bar-clearers, its single criterion
  stated inline. Not a rank; one auditable arithmetic fact.

Anti-drift guard (Nutrition): the bar rubric ships as a **versioned config file**, never
prose, and a CI-style check asserts no composite score is ever computed from bar-states.

## 2. The six bars (Nutrition's amended attribute set)

1. **Dose adequacy** (vs literature-derived effective range, hedged as such)
2. **Form / absorption** (tier by form class; blend rule below)
3. **Third-party verification** (two-tier: directory-confirmed / manufacturer-stated)
4. **Price fairness** (₪ per effective unit / absorbed-mg)
5. **Safety** (UL crossing = visible bar-level FAIL, never a tooltip; scoped
   contraindication notes attach to claims, not products)
6. **Label transparency** (dose disclosure honesty; undisclosed → CANNOT-VERIFY, never
   assumed low — missing-data discard discipline)

**Blend rule (closes red-team RT-A5, live inconsistency Solgar-D/49 vs TRIOMAG-null):**
blended/multi-form products with no per-form split → form bar = CANNOT-VERIFY, stated
identically for every blend. Nutrition writes the one-line rule into the versioned rubric.

## 3. Page shape (C3's order, owner's 4 layers, all earn v1 per Product)

H1 frame = **"איך לבחור [מגנזיום]"** (buying-guidance voice, C3) under the hub label
**מדריכים** (owner's word, Product-confirmed). Order:
1. **The buying rule** — what actually matters, in one read (the 6 bars in plain Hebrew).
2. **The products** — bar-state table, buckets, default pick, benchmark placement, pricing,
   buy button.
3. **The education spine** — what it does (evidence-tiered per the creatine co-sign method),
   forms explained, safety, FAQ-grade depth.
4. **Benchmark rendering rule (red-team RT-A3):** product vs **external standard** (the
   effective-dose range, the verified-cert bar, the benchmark median price) — never
   product-vs-field ordering, which recreates ranking by stealth.

**Copy gates add a banned-word check:** "דירוג/מדורג/מקום N" and grade-letter forms are
banned in guide copy (the live creatine page still says "דירוג" 3× — the habit is sticky).

## 4. Buy button (v1) — structural governance, not policy

- Plain retailer link, **no affiliate params**; dormant-style visual treatment per the
  existing `/catalog` buyUrl precedent (red-team RT-A1).
- Button on **every listed product** (Product's amendment — verdict-gating would re-couple
  verdicts and links). Missing link ≠ missing product.
- **Mechanical separation:** verdict data and buy-links live in separate files; the rubric
  config is versioned; on-page rule states "קישור קנייה אינו משפיע על הכללה, על דגלים או
  על סדר הצגה" (C3's wording).
- When real affiliate agreements appear: owner-gated (tripwire 4), with versioned disclosure
  + changelogged commercial policy as the entry bar.

## 5. Migration (single PR, zero overlap window)

- New hub **`/madrichim`** with the existing card structure; supplements REMOVED from
  /hashvaot in the same PR.
- 301s: `/hashvaot/magnesium` → `/madrichim/magnesium`, `/hashvaot/creatine` →
  `/madrichim/creatine`, `/hashvaot/supplements` → `/madrichim`. Sitemap swapped same PR.
- Both live pages stay untouched until the guide replacements ship.

## 6. Build order + gates

1. **Pre-build (parallel):** Research Agent PMID pull for the 3 magnesium form-ladder
   citations (Nutrition's gap — must land before copy) · Nutrition writes the versioned bar
   rubric config (incl. blend rule) · Frontend spikes the guide template skeleton.
2. **Golden guide = magnesium** (the disputed page and the harder case: tiers + UL flags +
   3/18 unresolved products displayed honestly).
3. **Creatine guide** stamps the proven template (its rulings are already closed).
4. **Ship together with the hub + migration PR** — no one-guide hub, no half-state.
5. **Gates per guide:** two-gate content (author + Adversarial QA render red-team, incl.
   banned-word check) · Nutrition co-sign on every bar threshold · Design vision-critic on
   the new template · C0 build/sitemap checks · Product go/no-go · **owner confirmation at
   the public flip** (consumer deploy, tripwire-2).
6. **Format-success metric (replacing Product's baseline-relative metric, per the GA4
   finding):** no meaningful baseline exists. The morph-to-other-areas decision is DEFERRED
   until the marketing push (Item 8) produces real traffic; then measure shortlist
   engagement + buy-button CTR over 4–6 weeks. Until then, "morph" stays parked.

## 7. Loose ends folded in

- TASK-503 (hub card): close-as-superseded when /madrichim ships; its NO-GO findings
  (blurb needs Content sign-off; count-scope coincidence; theme photo) become build inputs.
- TASK-492B (functional-dairy blog): unaffected in substance; after this plan is approved,
  re-frame check (its /hashvaot/creatine links become /madrichim/creatine) + full re-gate.
- Magnesium numeric score/rank removal supersedes the magnesium page's current model
  DISPLAY only — the absorbed-mg machinery survives as the form/absorption bar's engine.
- Frozen-veg precedent warning (red-team RT-A7): that band-based redesign stalled post-spec.
  Mitigation: this plan ships in ONE build wave (template → 2 guides → migration), no
  spec-then-stall gap.

## 8. What the owner is asked to approve

1. This plan as the execution contract (verdict layer §1, six bars §2, page shape §3,
   buy-button governance §4, migration §5, build order §6).
2. The one aesthetic call kept for the owner: hub label stays **מדריכים** with page-level
   "איך לבחור X" framing (recommendation), or rename the hub itself to **מדריכי קנייה**.
3. Confirmation that the magnesium page's numeric scores/ranking come DOWN as part of the
   migration (its tiers/flags survive as bar-states).
