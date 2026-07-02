---
name: corpus
description: Build or refresh a Bari category corpus — shelf mapping → corpus filter → BSIP enrichment → QA gate — with source-selection, OFF ban, and the missing-data discard rule enforced. Use to assemble the product set a category scores from.
---

# /corpus — Shelf-map → filter → BSIP enrich → QA

**Owner lane:** Data Architecture / Category Team. This is the corpus-assembly slice of the
factory (stages 1–5 of `bari-category-factory`); use `build-page` for the full page cycle and
`bari-qa-audit` for the QA runner detail.

## Use this when
- "Build the <category> corpus", "filter the corpus for <category>", "refresh the corpus",
  "map shelves for <category>".

## Stages (in order — do not skip the gate)

### 1. Shelf mapping
Identify the canonical shelf slug(s); verify each exists in the registry; no duplicate
shelf→category assignments. Output `shelf_map.json` (`shelf_slug · category_slug · rationale`).

### 2. Corpus filter
Apply filter rules to scope the corpus to this category; confirm no overlap with other active
categories; confirm the minimum corpus-size threshold (do not proceed if too sparse). Output
`corpus_filter.json` with a product-count estimate.
- **Raw-vs-prepared boundary** (when relevant) = tahini + sodium + energy, **never** protein or "סלט".

### 3. BSIP enrichment
Attribute extraction, `ingredients_text_he`, label assignment, comparison-dimension selection.
Validate enrichment coverage meets threshold. Output `bsip1_enrichment_report.json`
(coverage, label distribution, flagged products).

### 4. QA gate
Run the QA runner (`bari-qa-audit`). Hard fails block promotion; warnings must be explicitly
accepted or resolved. Output `qa_gate_result.json`.

## Data rules (non-negotiable)
- **OFF is banned project-wide** — ingredients + nutrition come ONLY from the direct scrape;
  unknown is acceptable, OFF is not.
- **Source selection:** never one retailer — Shufersal → Victory → Yochananof → Rami-Levy,
  use the reachable ones, cross-check nutrition, document blocked retailers.
- **Missing-data discard rule:** product data not found one-shot → discard it. Never punish or
  cap, never over-invest in re-sourcing (the brined 48→36 lesson).
- **Tzameret is directional only** — never authoritative; prefer USDA FDC + the BSIP0 panel.

## Return contract
Report the count at each stage (shelf → filtered → enriched → QA-passed) with the command that
produced each number, plus the cross-corpus baseline diff on any scope/keyword change.

## Related
`build-page` (consumes the corpus), `bari-category-factory`, `bari-qa-audit`, `rescore`.
