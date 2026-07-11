# TASK-598 — BSIP0 full audit, round 1 (audit only)

## Scope and evidence caveat

No source, product, score, builder, or served artifact was changed and no network was used. Evidence is in `task598_probes/audit_probe.py` and its JSON output. The prompt's denominator of **893 captures is not reproducible from the stated paths and key**: structural enumeration finds 2,321 objects carrying `nutrition_raw_source` in 104 JSON containers. Merged corpora, rejected arrays, and repeated raw-source copies create duplicates. Therefore I do not present occurrence counts as “captures”; doing so would be false precision. The output records every file/object/source path and makes the discrepancy independently auditable.

## Part A — known malfunction and acceptance specification

### Blast radius

`_to_float` converts every comma to a decimal point (`03_operations/bsip0/scrape/_shared/bsip0_nutrition.py:543-557`). Thus `1,628` becomes `1.628`. The structural scan found 102 string occurrences matching comma-thousands, but these are duplicated representations (row, table row, HTML) and duplicated corpus versions—not 102 products. Real examples include sodium `1,230` for GTIN 7290113192393 and `1,300` for 7290113193406 in `02_products/yogurt_system/bsip0_task515/shufersal_yogurt_bsip0_raw_FINAL_20260705T053213.json`; the requested brined-cheese case is GTIN/product 3075805 with `1,628`. All numeric fields routed through `parse_num` are exposed: energy, fat, saturated fat, carbohydrates, sugars, fiber, and protein (`bsip0_nutrition.py:502-514`), plus sodium via `parse_sodium_mg`. A comma-thousands energy value would be exposed, though this audit found no verified real >=1,000 kcal food row and does not invent one.

The small-sodium defect arises because unit propagation recognizes only an exact, fragile token set (`bsip0_nutrition.py:318-331`), while `parse_sodium_mg` falls back to `value <= 10 => grams => ×1000` (`:462-482`). The scan's Unicode literal regex did not reliably match the repository's mixed/garbled encodings; this is itself evidence that substring/token spelling is the wrong boundary. The real acceptance cases supplied by the owner remain authoritative: snacks GTIN 7290019297208 `0.2` + mem-gimel must be 0.2 mg; TASK-190 granola rows near 7 + genuine mg unit must remain about 7 mg, not 7,000 mg.

### Recommended rule (fix-session acceptance spec)

Parse value and unit as separate normalized inputs; never infer the unit from magnitude when a unit is present. Normalize Unicode (NFKC), bidi controls, NBSP/narrow-NBSP, Hebrew geresh/gershayim variants, and whitespace. Number rule: a comma between one-to-three leading digits and exactly three trailing digits, with no other decimal separator, is a thousands separator; a comma with one or two trailing digits is decimal; mixed separators use the rightmost separator as decimal only when its trailing group is not three, otherwise reject ambiguity rather than guess. Unit rule: normalized `mg`, `milligram(s)`, `מג`, `מ״ג`, `מ"ג`, `מ׳ג` means milligrams; normalized `g`, `gram(s)`, `גרם` means grams and converts ×1000. Missing or unrecognized sodium unit must return unknown/flagged, not use the `<=10` heuristic.

Required outcomes: brined product 3075805 (`1,628` plus mg token) → 1628 mg; snack 7290019297208 (`0.2` plus mg token) → 0.2 mg; genuine TASK-190 granola `~7` plus mg token → ~7 mg. Strongest objection: older captures often omit units, so removing magnitude inference converts previously usable sodium values to NULL and reduces coverage. That is preferable to a silent three-order-of-magnitude error; a retailer/schema-specific declared-unit default may be allowed only when provenance proves that schema's column unit.

## Part B — findings

| Defect | Code evidence | Real evidence | Severity | Fix direction |
|---|---|---|---|---|
| Comma semantics conflate decimal and thousands | `bsip0_nutrition.py:543-557` | 3075805 `1,628`; probe also records 7290113192393 `1,230` | Critical | Grammar above; ambiguity fails closed |
| Sodium unit detection depends on exact tokens and then magnitude | `:318-331`, `:462-482` | 7290019297208 `0.2`+mg; TASK-190 ~7mg rows | Critical | Separate normalized value/unit; no magnitude fallback |
| Single-table unknown basis is accepted | `:215-250` | Comment admits missing-header legacy panels | High | Require explicit per-100g or retailer schema proof; persist decision |
| Multiple per-100g tables silently first-win | `:252-259` | selection code, no collision comparison | High | Compare panels; fail on materially different duplicates |
| Nutrient duplicates silently first-win | `:299-332` | implementation explicitly first-value-wins | High | Record collisions and require equality/tolerance; do not discard evidence |
| Label classifier is broad substring matching | `:65-100` | `sugar` precedes carbs; generic language stems | Medium | Token/boundary-aware multilingual label registry; unknown subrows retained |
| “of which” handling is fat-specific at the final guard | `:97-99` | classifier only blocks generic fat subrows | Medium | Represent parent/subrow relation; cover polyols/starch and other carbohydrate subrows |
| Bound semantics are optional and commonly lost | `:436-459`, `:485-538` | only fat/saturated flags reach `_integrity` | High | Typed quantity `{value, unit, relation}` for every nutrient |
| Integrity checks are narrow/inconsistently wired | `:516-537`, `:560-611` | only sat>fat, sodium ceiling, special fat-energy gap | High | Central validator: sugars<=carbs, sat<=fat, fiber relation policy, energy/macros, range/bounds |
| Sodium ceiling claim is scientifically overbroad | `:523-535`, `:574-577` | code calls >2000 physically impossible although salt-rich foods exist | High | Treat as category-aware review flag, not universal impossibility |
| Capture provenance has no canonical selection key | `extract_nutrition_raw :384-413` stores source but not run identity | repeated raw source in FINAL/MERGED/corpus files in probe | High | Manifest keyed by retailer+GTIN+scrape timestamp+content hash; mtime never authoritative |
| 893 denominator is unversioned | prompt vs probe output | 2,321 objects/104 containers by structural query | High | Commit capture manifest defining membership and dedup policy |
| Percent/range/RTL handling lacks a formal lexical layer | `_NUM_RE :432-433`; `_to_float :551-557` | probe records percent occurrence; range search found none under selected objects | Medium | Unicode normalization and typed lexer before nutrient parsing |
| Raw capture completeness cannot be asserted repository-wide | only 104 containers actually carry key | paths listed in probe | High | Acquire gate requires raw source for every accepted record |
| GTIN verification is retailer-dependent | Shufersal acquire verifies LD+JSON at `scrape/shufersal/01_acquire_shufersal.py:159-174` | no common interface-enforced proof | High | Per-retailer conformance contract returning requested/resolved GTIN evidence |
| Bare→raw adapter remains opt-in | `bsip0_nutrition.py:346-381` | comments identify two prior silent-all-None callers | High | Make numeric parser accept one typed object; forbid manual adapters |
| Test coverage is concentrated, not module-wide | tests exist for shared parser/gate/QA, while most acquisition, raw-store, pipeline, and category scripts have no paired tests | file inventory command | Medium | Coverage map and conformance suite; prioritize acquire and replay paths |

### Missing-integrity quantification

The first probe could not quantify parsed-row trips because the 2,321 raw-source-bearing objects do not share a canonical parsed nutrition key alongside the source (`parsed_nutrition_candidates=0`). Reporting zeros would incorrectly mean “no violations.” This reinforces the v2/manifest proposal: replay raw sources through one parser and emit a flat verification table. The current universal rules also need careful semantics: sugars<=carbs is strong; satFat<=fat is strong with bound awareness; fiber<=carbs is not universally valid because labeling conventions differ; 4/9/4 needs tolerance for fiber/polyols/organic acids and rounding; sodium bounds must be category-aware.

### Static retailer-acquire review

Shufersal now verifies the resolved GTIN and maps bare keys explicitly (`01_acquire_shufersal.py:159-202`). The repository does not contain a coherent set of four equivalent acquire modules named Shufersal/Hazi Hinam/Yohananof/Tiv Taam under one interface: Hazi Hinam is represented by an exploratory test, Yohananof by several category-specific scripts/raw-store fetcher, and no canonical Tiv Taam peer was found in the BSIP0 Python inventory. Consequently, equivalence against stale-URL and bare/raw mapping classes cannot be certified. This is a finding, not permission to infer compliance from unrelated scripts.

## Part C — ranked enhancement proposals

1. **Replay-everything regression harness — ACCEPT (L).** Manifest-selected captures; parse every capture; emit flat GTIN/retailer/basis/raw/parsed/flags table; diff against committed baseline on every parser change. Risk: baseline legitimizes existing defects. Strongest argument against: a large noisy golden file becomes review theater. Mitigation: explicit approved deltas and invariant summaries.
2. **Capture provenance manifest — ACCEPT (M).** Membership, retailer, requested/resolved GTIN, scrape/run timestamp, source URL, content hash, parser version, supersession. Risk: migration burden. Against: content hashes plus directory convention may suffice. They do not solve authoritative membership or duplicates.
3. **Unit-annotated capture v2 — ACCEPT (L).** Preserve raw text plus normalized value/unit/relation/basis and source DOM coordinates. Risk: schema complexity. Against: raw HTML is replayable. Raw HTML is not stable across parser/runtime dependencies and does not encode acquisition identity.
4. **Per-retailer parser conformance tests — ACCEPT (M).** Shared contract fixtures for GTIN mismatch, stale URL, basis, units, raw/bare mapping, collision behavior. Risk: fixtures drift. Against: retailer markup changes make fixtures stale; still valuable as regression, complemented by canaries.
5. **Wire `nutrition_implausible` into every acquire path — ACCEPT WITH REDESIGN (M).** One typed validation result, persisted and gate-enforced; warnings distinct from blockers. Risk: false rejects. Against: acquisition should preserve data, not interpret it. Preserve always, but block promotion rather than capture.
6. **Energy–macros consistency validator — ACCEPT AS REVIEW SIGNAL (M).** Interval calculation using 4/9/4 plus declared fiber/polyols and rounding tolerance; category/schema calibration. Risk: false positives. Against: Atwater factors and labeling conventions make a universal equality invalid.
7. **Relational nutrient invariants — ACCEPT (S).** Bound-aware sugars<=carbs and sat<=fat; fiber relationship schema-specific. Risk: label definitions vary. Against: fiber may be outside carbohydrate under some conventions.
8. **Per-category sodium plausibility bounds — ACCEPT AS NONBLOCKING FIRST (M).** Learn review ranges from verified direct-scrape corpus; never substitute values. Risk: circularly learning corrupted data. Against: unusual legitimate salt-rich foods defeat category bounds. Require provenance and manual review before blocking.
9. **Collision-preserving classification — ACCEPT (M).** Store all candidate rows and classification rationale; promotion only after collision resolution. Risk: downstream complexity. Against: most duplicates are harmless. Silent disagreement is precisely the dangerous minority.

## WEAKEST POINTS OF MY OWN AUDIT

1. I could not reconstruct the owner's 893-member set; therefore the requested exact blast-radius denominator and integrity trip counts are not honestly available. The adversary can fairly demand the missing manifest/query.
2. Mixed mojibake/Unicode in console and stored HTML prevented a reliable literal count of mem-gimel variants; named real cases are acceptance anchors, not a complete census.
3. Static inspection covered the full BSIP0 Python inventory but not binary browser-session caches; those are not parser source, yet could contain additional capture evidence.
4. The retailer comparison is partly an absence finding because the alleged four canonical peer scripts are not discoverable as such; an owner may know an out-of-tree or differently named source.
5. Energy/macro and relational trip counts remain unquantified because captures lack a uniform adjacent parsed panel; treating the probe's zero candidates as zero defects would be wrong.

