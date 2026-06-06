# Run Record — run_cereals_multiretailer_001 (TASK-184)

**Run ID:** run_cereals_multiretailer_001
**Date:** 2026-06-05
**Owner agent:** data-agent
**Engine:** BSIP2 proto_v0, `BARI_RECAL_P0=on` + nova_proxy EV-044 — **byte-identical to run_cereals_005**
(no score/engine change; acquisition + curation only).
**Gate status:** GATE 3 (first-batch owner consult) APPLIES — **NOT promoted to live**; produced for owner review.
**Frozen invariants:** untouched (milk run_005_headpin, snack 70/B, bread provenance). Shufersal run_005 corpus left intact.

## Configuration hash inputs
- Acquisition: `03_operations/bsip0/scrape/multiretailer_cereals/01_acquire_multiretailer.py`
- Curation (ruling under test, imported UNCHANGED): `shufersal_cereals/02_build_bsip1_cereals.py::_curate` (EV-045/045b)
- BSIP1 wrapper: `multiretailer_cereals/02_build_bsip1_multiretailer.py`
- Merge/dedup: `multiretailer_cereals/03_merge_dedup.py`
- BSIP2: `bsip2/proto_v0/src/batch_run_cereals_multiretailer_001.py`

## Acquisition model (honest — no scraping, no fabrication)
Israeli price-transparency law publishes full per-chain SKU catalogs (barcode + Hebrew name + brand +
price). Used as the IDENTITY layer; each barcode paired with an Open Food Facts (OFF) **candidate**
panel for nutrition + ingredients (documented `il_prices → open_food_facts` pairing). A barcode miss in
OFF = "no panel", never an invented panel. Provenance stamped per EDPG; all panels remain `candidate`
(no live promotion, GATE 3).

## Retailer reachability (probed live 2026-06-05)
| Retailer | Path | Result |
|---|---|---|
| **Carrefour** (7290055700007) | self-hosted `prices.carrefour.co.il` (inline `files` JSON + .gz transparency XML) | **REACHABLE** — PriceFull parsed, 11,418 catalog SKUs |
| **Yochananof** (7290455000004) | `laibcatalog.co.il` publisher portal (confirmed via StoresFull branch names: Netivot/Sderot) | **REACHABLE** — PriceFull parsed |
| **Rami-Levy** | `prices.rami-levy.co.il`, `publishedprices.co.il`, `url.publishedprices.co.il` | **BLOCKED** — all portals ConnectionError/DNS-dead; storefront is a login-gated SPA with no public catalog API. (Consistent with prior-run documentation that the central Cerberus host died 2026-06-03.) |

## Counts (acquired → curated → scored)
| Retailer | Catalog SKUs | Name-gate cereal candidates | OFF panel (macros) | Curated IN | Excluded | New (dedup) |
|---|---|---|---|---|---|---|
| Carrefour | 11,418 | 217 | 133 (61%) | 54 | 163 | — |
| Yochananof | (PriceFull) | 94 | 17 (18%, OFF rate-limited) | 6 | 88 | — |
| **Combined** | | 311 | 150 | **60** | 251 | **42 new** |

Dedup vs Shufersal baseline (run_005, 66 barcodes): **16 duplicates vs baseline** (same EAN, different
retailer — cross-retailer identity match confirmed), **2 Carrefour∩Yochananof duplicates**, **42 genuinely
new products** (23 standard cereal + 19 granola/muesli). 40/42 scored (2 insufficient).

Note on the lower Yochananof panel rate: OFF (no-auth, crowd-sourced) began dropping connections
("Remote end closed connection") partway through the Yochananof batch — an IP throttle, not a data
absence (an earlier hand-sample on these same barcodes returned panels). Carrefour ran first and got its
panels before throttling. Recovery pass with retry/backoff recovered 0 (throttle persisted). This is an
infrastructure limit of the free OFF endpoint, documented not worked around.

---

# EV-045 / EV-045b VALIDATION on UNSEEN data

The ruling was imported and run **unchanged** on Carrefour + Yochananof (data never seen by the rule's
authors). Exclusion tally:

| Reason | Carrefour | Yochananof |
|---|---|---|
| bar_excluded_snack_overlap | 35 | 15 |
| non_cereal_excluded (bread/drink/cracker/dessert/capsule) | 22 | 17 |
| chocolate_confection_excluded | 4 | 1 |
| drink_excluded | 1 | 0 |
| energy_implausible_for_dry_cereal (<150 kcal floor) | 5 | 0 |
| not_cereal (no cereal token) | 48 | 11 |
| no_usable_nutrition (OFF panel gap) | 48 | 44 |

## Precision (are exclusions correct?) — HELD
Every contaminant-class exclusion inspected was a genuine non-cereal: bars (חטיף/בר/Corny/Crunchy Bar/
cookies עוגיות), breads (לחם מלא, לחם מחמצת sourdough), oat **drinks** (משקה שיבולת שועל, Foamable oat
drink, Bebida de avena), crackers/rice cakes (קרקר, Rice Cakes, פריכיות), supplement capsules (קפסולות),
dairy desserts (מעדן), chocolate confections (שוקולד מריר, Click). **No false-positive exclusion of a
genuine cereal was found.** The Hebrew word-boundary yeast guard (שמרים ≠ משמרים) was not stress-tested
on this data because OFF ingredient coverage was thin (only 44 of the 311 candidates carried an
ingredient panel) — the trap therefore could not re-fire, but neither was it exercised. **Flag for the
next storefront-sourced run (richer ingredient panels) to re-confirm the yeast guard.**

## Recall (did contaminants slip into the included set?) — ONE NEW CLASS FOUND
60 included products audited. 58 are clean breakfast cereals / granola / muesli. **A new contaminant
class leaked through:** Nestlé **Fitness savory crackers / crispbreads** ("פיטנס מלח פלפל", "Fitness
Thin/Thins", several bare "Fitness" SKUs). They evade EV-045b because (a) they carry no `קרקר` token in
the name, (b) they are not chocolate, and (c) they enter via the broad `fitness`/`פיטנס` include token.
Their macro signature distinguishes them: **fat ≥ ~13 g/100g** (476 kcal/22.4g fat salt-pepper; 458/15.8g;
461/17g) vs genuine Fitness *cereals* at 5–10 g fat. The router caught most of these as misroutes
(→ `default`/`beverage`, 10 of them), so they are flagged, not silently scored as cereals — but the
curation filter itself did not exclude them.

### Recommended ruling extension (EV-045c candidate — for owner/Nutrition review, NOT implemented)
A "Fitness-brand non-cereal" guard: for SKUs whose only cereal signal is the `fitness/פיטנס` brand token,
exclude when **fat ≥ 13 g/100g** OR a savory descriptor is present (מלח/פלפל/רוזמרין/סלק/בטטה/זיתים/
"קרקר"/"קראנצי"/Thin/Thins). Keep as **flag-not-drop** initially (per TASK-183 §2 #5 brand-line policy) to
avoid a `חומוס גרגרים`-style false positive. This is curation (contamination ≠ calibration), not a score
change.

## Structural note — category-code anchoring is NOT available on the price-feed path
TASK-183's #2 recommendation (anchor on Shufersal category codes A2502/A2803/A2808) cannot be applied
here: the **transparency XML carries identity + price ONLY, with no category code** on the line. This is
exactly why the name-gate over-included the Fitness crackers — there is no origin code to anchor on.
TASK-183's #1 pre-scan (the EV-045b classifier) is therefore the *only* available door-gate on the
price-feed path, and it held except for the brand-token class above. **Code-anchoring remains valuable
but is storefront-specific; the price-feed acquisition path needs the brand-token guard instead.**

## Scoring outcome (byte-identical engine)
40 scored. Grades: 1 A · 14 B · 17 C · 7 D · 1 E. Median 60.2 (run_005 was median 58.7, range 41.4–79.9,
**no A**). The single A (81.2 — "גרנולה בתוספת חלבון", Carrefour) is a **new category-high on fresh
data**, earned on real OFF macros (24.8 g protein, 15.4 g fiber, 7.2 g sugar, 46 mg sodium per 100g) by
the unchanged engine — i.e. a better product than Shufersal stocked, not a scoring drift. Surfaced to
Nutrition Agent as an FYI under Hard Rule 7 (above-baseline high), not a halt.

## Verdict
EV-045/045b **generalized to unseen multi-retailer data** — high precision, strong recall, no false drops
of real cereals. One new contaminant class (Fitness savory crackers) identified with a concrete, ready
extension. The ruling is sound; the recommended additions are incremental curation, not scoring changes.

---

# EV-045c — IMPLEMENTED (TASK-184 follow-up, owner-adopted 2026-06-05)

The owner ADOPTED EV-045c. Implemented as a **flag-not-drop** Fitness-brand savory-cracker guard in the
canonical curation filter `shufersal_cereals/02_build_bsip1_cereals.py::fitness_noncereal_flag()`,
imported UNCHANGED by the multiretailer wrapper. Scoped to the fitness/פיטנס brand line; fires on a
savory descriptor OR (fat ≥ 13 g/100g AND no sweet/granola signal). Hebrew word-boundary discipline
applied (מלח guarded vs מלא; זית as construct head of זיתים).

- **Curation re-run:** Carrefour 54 IN / 163 OUT, Yochananof 6 IN / 88 OUT — **identical** to the
  pre-EV-045c counts (flag-not-drop changes no membership).
- **Dedup re-run:** 42 new / 16 dup-vs-baseline / 2 cross-retailer — **42-set UNCHANGED.**
- **Flags raised:** 7 SKUs (6 Carrefour + 1 Yochananof); 6 are in the 42-new set, 1 is a
  duplicate-vs-baseline.
- **False-positive check PASS:** the genuine Fitness granola פיטנס גרנולה חמוציות (14.8 g fat, 18.7 g
  sugar) is NOT flagged — the sweet-signal carve-out held.
- **Net value:** `Fitness Thin` (7290112968807) had routed to `cereal` and scored C (router did NOT
  catch it); EV-045c now flags it at curation. The other 5 in-set flags were already router-misroutes.
- **No score/engine change** — curation only; per-retailer curation reports now carry an
  `ev_045c_fitness_flag_count` + `ev_045c_flagged` list.

Full per-product GO/NO-GO and provenance/dedup/engine sign-off: `DATA_SIGNOFF.md` (this directory).
