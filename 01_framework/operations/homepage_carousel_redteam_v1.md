# Homepage Carousel — Adversarial QA / Red-Team Report

Date: 2026-06-27
Reviewer: adversarial-qa-agent
Scope: micro-comparison-snapshots.ts (LIVE) and homepage-carousel-data.json (generated 2026-06-27, NOT wired)
Audit type: Track V (data propagation) + Track C (claim challenge)

---

## OPENING FINDING

home-comparisons.tsx line 11 imports exclusively from micro-comparison-snapshots.ts, which contains four factually wrong product counts, one wrong score, and one invented brand string.

homepage-carousel-data.json (generated 2026-06-27) is NOT imported by any component. Live carousel is powered by stale data.

---

## File Disposition

File                              | Consumed? | Verdict
micro-comparison-snapshots.ts     | YES        | FAIL — 3 CRITICAL, 1 HIGH, 3 MEDIUM
homepage-carousel-data.json       | NO         | PASS on data quality; unused

---

## Card-by-Card Verdict — micro-comparison-snapshots.ts

CARD 1 — bread-investigation
  Product count: claims "32" / bread_frontend_v3.json product_count=29, scored_count=31 → FAIL
  href /hashvaot: route live → PASS (bread page is at /hashvaot/bread)
  Health claims: none → PASS
  OFF data: none → PASS
  VERDICT: FAIL — "32" matches neither 29 (displayed) nor 31 (scored)

CARD 2 — cereals-report
  Product count: claims "24" / cereals_frontend_v2.json product_count=20 → FAIL
  Archetype count "4 ארכיטיפים": no archetype field in JSON → UNVERIFIED
  href /hashvaot: route live → PASS (cereals page at /hashvaot/breakfast-cereals)
  Health claims: none → PASS
  VERDICT: FAIL — "24" does not match published JSON (20 products)

CARD 3 — snack-bars-report (granola)
  Product count: claims "14" / granola_frontend_v2.json product_count=22; v1 also 22 → FAIL
  Archetype count "6 ארכיטיפים": no archetype field in JSON → UNVERIFIED
  href /hashvaot: route live → PASS (granola page at /hashvaot/granola)
  Title "המחיר השקט של בריא" in scare-quotes: adversarial framing, not endorsement → PASS
  VERDICT: FAIL — "14" is wrong for all versions of granola JSON. No artifact traces to 14.

CARD 4 — sugar-names
  "12 שמות לסוכר": specific factual claim, no EV-### evidence entry confirmed → UNVERIFIED
  href /hashvaot: route live → PASS
  Health claims: none → PASS
  VERDICT: CONDITIONAL — requires evidence citation. Routes to: research-agent

CARD 5 — bari-methodology
  stat "8 אותות": scoring.md line 81 says "10 dimensions"; lines 93-100 show L1-L6 layers → MISMATCH
  href /#methodology: HomeMethodology has id="methodology" (line 527) → PASS
  BSIP vocabulary on card: not named → PASS
  VERDICT: FAIL (MEDIUM) — "8" unattested in scoring docs. Routes to: nutrition-agent

CARD 6 — protein-products
  Product count: claims "26" / protein_combined=32, protein_bars=16 → FAIL
  Disclaimer "בקרוב במלואם": appropriate hedging → PASS
  VERDICT: FAIL — "26" matches no published protein dataset

CARD 7 — dairy-vs-plant (comparison card)
  Left score (whole milk barcode 7290000051352): claims 85 / JSON: 85 → PASS
  Right score (soy barcode 7290116936116): claims 67 / JSON: 63.9 → FAIL (delta 3.1)
  Left imageUrl api.yochananof.co.il...7290000051352: matches JSON imageUrl → PASS
  Right imageUrl api.yochananof.co.il...7290116936116: matches JSON imageUrl → PASS
  Right brand "תחליף צמחי · סויה": JSON has real brand; this is invented label → FAIL
  href /hashvaot/milk-comparison: route exists → PASS
  Images from yochananof scrape CDN, not OFF → PASS
  Health claims: none → PASS
  VERDICT: FAIL (2 issues)
    1. Score 67 vs published 63.9 — live score propagation error
    2. Brand "תחליף צמחי · סויה" — invented metadata

---

## homepage-carousel-data.json — sole card verified

CARD — bread-tahini-vs-green
  Left score 94.8 / grade S: bread_frontend_v3.json bsip1_bread_7290016245325 score=94.8, grade=S → PASS
  Right score 92.7 / grade S: bread_frontend_v3.json bsip1_bread_3268429 score=92.7, grade=S → PASS
  "חלבון 27.5 גרם" in tradeoff copy: value 27.5 confirmed in bread_frontend_v3.json → PASS
  "סיבים 18.5 גרם" in tradeoff copy: value 18.5 confirmed in bread_frontend_v3.json → PASS
  Left imageUrl Shufersal CDN barcode 7290016245325: matches JSON imageUrl → PASS
  Right imageUrl Shufersal CDN barcode 3268429: matches JSON imageUrl → PASS
  href /hashvaot/bread: route exists → PASS
  off_used=false → PASS
  Health claims: none → PASS
  Leakage: none → PASS
  VERDICT: PASS — all checked data points verified against bread_frontend_v3.json

  Gaps:
  - _meta.item_count=9 but items array has only 1 entry; 8 planned cards not yet authored
  - File not imported by any component; correct data has zero consumer effect until wired

---

## Findings by Severity

### CRITICAL — must resolve before homepage can ship

RT-1: Four stale product counts in live carousel
  bread "32" vs published 29 (bread_frontend_v3.json product_count=29)
  cereals "24" vs published 20 (cereals_frontend_v2.json product_count=20)
  granola "14" vs published 22 (granola_frontend_v2.json product_count=22; no version ever had 14)
  protein "26" vs published 32 (protein_combined) or 16 (protein_bars)
  Implication: four false statistics on the live homepage
  Routes to: frontend-agent

RT-2: Live soy score 67 contradicts published 63.9
  micro-comparison-snapshots.ts line 126: score 67
  milk_frontend_v1.json milk_7290116936116 score: 63.9. Delta = 3.1
  Implication: score propagation failure — displayed number contradicts authoritative JSON
  Routes to: frontend-agent

RT-3: homepage-carousel-data.json not wired — defective .ts file remains active
  home-comparisons.tsx line 11 imports only from micro-comparison-snapshots.ts
  homepage-carousel-data.json has zero importers; verified data has no consumer effect
  Routes to: frontend-agent

### HIGH — should resolve before launch

RT-4: Invented brand string in live comparison card
  micro-comparison-snapshots.ts line 124: brand "תחליף צמחי · סויה"
  milk_frontend_v1.json carries a real brand for milk_7290116936116
  Violates no-invention rule
  Routes to: frontend-agent

### MEDIUM — should document or monitor

RT-5: "8 אותות" misstates scoring architecture
  scoring.md: 10 dimensions (line 81), L1-L6 signal layers (lines 93-100)
  "8" unattested in any scoring artifact
  Routes to: nutrition-agent (confirm consumer-facing number) then frontend-agent

RT-6: "12 שמות לסוכר" lacks evidence citation
  Specific factual claim with no EV-### entry confirmed in this review
  Routes to: research-agent then content-agent

RT-7: Editorial cards href to /hashvaot instead of specific category pages
  /hashvaot/bread, /hashvaot/granola, /hashvaot/breakfast-cereals all exist
  homepage-carousel-data.json already uses correct deep-link hrefs
  Routes to: frontend-agent

---

## OFF and Invented Data Summary

off_used in homepage-carousel-data.json: false — PASS
Milk images: api.yochananof.co.il — retailer scrape CDN — PASS
Bread images: res.cloudinary.com/shufersal — Shufersal CDN — PASS
Nutrition values: none in micro-comparison-snapshots.ts; verified values in .json — PASS
Soy brand "תחליף צמחי · סויה": invented label — FAIL (RT-4)

---

## Route Availability

/hashvaot              → exists (generic listing)
/hashvaot/milk-comparison → exists
/hashvaot/bread        → exists (.ts file does not link here — RT-7)
/hashvaot/granola      → exists (.ts file does not link here — RT-7)
/hashvaot/breakfast-cereals → exists (.ts file does not link here — RT-7)
/#methodology          → exists (HomeMethodology id="methodology" confirmed)

---

## Overall Verdict

micro-comparison-snapshots.ts (LIVE): FAIL
  3 open CRITICAL, 1 HIGH, 3 MEDIUM — all open
  Homepage carousel cannot ship in this state

homepage-carousel-data.json (unused): PASS on data quality for single completed card
  8 of 9 declared items missing; not wired

Fastest unblock: wire homepage-carousel-data.json instead of micro-comparison-snapshots.ts,
complete remaining 8 cards from published JSONs.
This resolves RT-1, RT-2, RT-3, RT-4, and RT-7 in one step.

---

MACHINE-READABLE VERDICT

agent: adversarial-qa-agent
timestamp: 2026-06-27
scope: homepage carousel
track_v: FAIL
track_c: FAIL
verdict: FAIL
open_critical: 3
open_high: 1
open_medium: 3
findings:
  RT-1 CRITICAL four stale product counts (bread:32vs29, cereals:24vs20, granola:14vs22, protein:26vs32) routes-to frontend-agent
  RT-2 CRITICAL soy score 67 vs published 63.9 routes-to frontend-agent
  RT-3 CRITICAL homepage-carousel-data.json not wired routes-to frontend-agent
  RT-4 HIGH invented brand string routes-to frontend-agent
  RT-5 MEDIUM 8 aotot contradicts 10 dimensions in scoring.md routes-to nutrition-agent
  RT-6 MEDIUM 12 sugar names no EV citation routes-to research-agent
  RT-7 MEDIUM editorial hrefs not deep-linked routes-to frontend-agent
pass:
  off_used=false
  images from scrape CDNs only (yochananof / shufersal)
  no health claims (bari in scare-quotes only, adversarial framing)
  methodology anchor id=methodology confirmed
  milk-comparison route live
  bread comparison scores 94.8 and 92.7 match bread_frontend_v3.json
  bread nutrition values 27.5g protein and 18.5g fiber confirmed in JSON
  whole milk score 85 matches milk_frontend_v1.json
