# BSIP2 Future UI Direction — v2 Architecture

**Status:** Design specification  
**Version:** 2.0-draft  
**Date:** 2026-05-18  
**Companion:** layer_architecture.md, orchestration_v2.md, framework_philosophy.md

---

## Preamble

The current BSIP2 output is a trace file with a final score and a grade letter. It is an engineering artifact. It is complete for validation purposes, deeply incomplete for communication purposes.

The v2 architecture produces richer, more structured output — four layer assessments, contradiction annotations, tension descriptions, and orchestration traces. This document specifies how that richer output should be presented to users.

The design principle: **every screen must be honest, but most screens need not be complete**.

---

## The Presentation Problem

The core tension in food intelligence UI is:

> Completeness produces overwhelm.  
> Simplicity produces dishonesty.

A single number (73) is easy to consume but hides everything that makes it meaningful.  
A full trace dump is honest but incomprehensible.

The v2 UI resolves this through **progressive disclosure**: a compact primary view, an interpretive summary layer, and a full analytical trace — each serving a different user need.

---

## Level 0 — The Card (Primary / At-a-Glance)

The product card is the default UI element. It appears in lists, search results, and comparison screens.

**Contents:**
```
┌─────────────────────────────────┐
│  [product image]                │
│                                 │
│  Product Name                   │
│  Brand                          │
│                                 │
│        73  B                    │
│        ■■■■■■■░░░               │
│                                 │
│  ⬡ Structural   ●●●○○           │
│  ◈ Nutritional  ●●●●○           │
│  ≋ Metabolic    ●●○○○           │
│  ⚠ Engineered   ●○○○○           │
│                                 │
│  NOVA 2 · Dairy                 │
└─────────────────────────────────┘
```

**Design notes:**
- Score (73) and grade (B) are primary
- The four-layer dot indicators give at-a-glance layer health without numbers
- NOVA and category are metadata, not primary judgment
- Tensions are NOT shown at this level — they appear on tap/click

**Dot scale:** 5 dots, filled proportionally to layer index (each dot ≈ 20 points).

---

## Level 1 — The Interpretation Panel (Default Expanded)

On tap/click, the card expands to the Interpretation Panel — the primary user destination.

```
Product Name
─────────────────────────────────────────

    73  B — Good                          
    ■■■■■■■░░░░░░░░░░░░░ 

─────────────────────────────────────────
Bari's Reading

    Whole dairy with intact matrix and meaningful
    protein contribution. No detected engineering
    for overconsumption. Metabolically stable profile.

─────────────────────────────────────────
Layer Summary

  ⬡ Structural Integrity         ●●●●○
    Intact whole-food matrix. Minimal processing.
    NOVA 1 (single-ingredient dairy).

  ◈ Nutritional Contribution     ●●●●○  
    3.4g protein per 100g, present in whole-food
    context. Meaningful fat contribution.

  ≋ Metabolic Stability          ●●●○○  
    No significant fiber. High fat moderates glucose
    response. Liquid form reduces satiety anchoring.

  ⚠ Consumption Engineering      ●○○○○  
    No engineering signals detected.

─────────────────────────────────────────
Key Facts
  Energy    66 kcal
  Protein   3.4g
  Fiber     0g
  Fat       3.6g
  NOVA      1
  
─────────────────────────────────────────
↓ Full Analysis
```

**Design notes:**
- "Bari's Reading" is a 1–2 sentence natural language summary (20–40 words) that captures the dominant signal
- Each layer has a 1-line description plus its dominant signal
- Key Facts are raw nutrition, not reinterpreted
- Full Analysis is progressive — expandable, not the default

---

## Level 2 — The Tension View (When Contradictions Exist)

When a product carries an active tension (C-1 through C-4 from orchestration_v2.md), the Interpretation Panel shows a tension callout:

```
⚡ TENSION DETECTED

    This product delivers exceptional protein (Layer 2: 
    strong) within a heavily reconstructed matrix (Layer 1: 
    limited). Bari scored these independently. The score 
    reflects the net outcome; the tension is real.
    
    Structural integrity: Limited [32/100]
    Nutritional contribution: Strong [78/100]
```

**Design principle:** Tensions are not hidden, averaged, or smoothed. A product with a C-1 tension (nutritional excellence + structural failure) explicitly shows this to the user. The user should understand that "44 [D]" in this case means "very strong nutrition inside a heavily reconstructed product" — not a mediocre product across the board.

---

## Level 3 — The Full Analytical Trace

Accessible via "Full Analysis" expansion. Intended for:
- Research users
- Product comparison with analytical depth
- Bari internal review and QA

**Contents:**
- All four layer indices with sub-signal breakdown
- Orchestration stages (ceiling, floor, adjustment, pressure, regulatory, confidence)
- Contradiction annotations
- Signal-level evidence (what triggered each assessment)
- NOVA inference evidence for/against
- Confidence reductions enumerated
- Raw score before floors/caps

This is the current `bsip2_trace.json` content, rendered for human reading.

---

## Radar Evolution

The current architecture supports radar charts comparing dimension scores across products. The v2 radar evolves to show **four quadrants** corresponding to the four layers, with sub-signals within each quadrant:

```
        Structural
       ┌────────────┐
       │  NOVA·Addi-│
Metab  │  tives·    │ Nutritional
 olic  │  Matrix    │ Contribu-
Stabi  │            │ tion
 lity  │ Glycemic·  │ Protein·
       │ Satiety·   │ Fiber·
       │ Calorie    │ Fortification
       └────────────┘
         Engineering
```

**Why this is better than the current 10-dimension radar:**
- Groups related signals visually (all structural signals in one quadrant)
- Shows layer balance at a glance (is the product balanced across layers, or strong in one and weak in another?)
- Makes tensions visible: a product with a large Structural quadrant and a small Nutritional quadrant is immediately readable as "structurally intact, nutritionally limited"

---

## Comparison View Evolution

The comparison UI should evolve from "two numbers side by side" to "two architectural profiles side by side":

```
Whole Milk 3.4%      │  Oat Barista Drink
        75 B         │        49 D
                     │
⬡ Structural  ●●●●●  │  ⬡ Structural  ●●●○○
◈ Nutritional ●●●●○  │  ◈ Nutritional ●●○○○
≋ Metabolic   ●●●○○  │  ≋ Metabolic   ●●○○○
⚠ Engineered  ●○○○○  │  ⚠ Engineered  ●●○○○
                     │
The gap               │
─────────────────     │
Layer 1: +32 pts      │  (Whole milk intact; oat drink
Layer 2: +18 pts      │   moderately reconstructed)
Layer 3: -2 pts       │  (Similar metabolic profiles)
Layer 4: -3 pts       │  (Oat drink slightly more
                     │   engineered)
Final delta: +26 pts  │
```

**Design principle:** In a comparison, show WHERE the gap comes from, not just that the gap exists.

---

## Language Direction

### Vocabulary for layers

| Layer | Icon | Short name | Human phrasing |
|-------|------|-----------|----------------|
| Structural Integrity | ⬡ | Structure | "intact / reconstructed / fragmented" |
| Nutritional Contribution | ◈ | Nourishment | "nutritious / depleted / fortified" |
| Metabolic Stability | ≋ | Stability | "stable / volatile / moderate" |
| Consumption Engineering | ⚠ | Engineering | "plain / engineered / heavily engineered" |

### Language principles

**Do not say:** "This product is healthy / unhealthy."  
**Say instead:** "This product carries a strong structural profile." / "This product shows evidence of engineering for palatability."

**Do not say:** "Avoid this product."  
**Say instead:** "This product scores D on Bari's structural assessment."

**Do not say:** "High in [nutrient] = bad."  
**Say instead:** "The fat in this product is predominantly saturated, in a natural whole-food matrix."

**Do not say:** "NOVA 4 means ultra-processed junk."  
**Say instead:** "NOVA 4 indicates significant processing. Within Bari's architecture, this is one signal among several."

**Do not say:** "This is a healthy choice."  
**Say instead:** "This product scores B — structurally intact, nutritionally meaningful, metabolically stable."

---

## Score Presentation

The current single-number + letter format (75 B) is preserved. It is simple, universal, and communicable.

In v2, the grade carries a richer meaning because it emerges from negotiation, not averaging. The **grade descriptions** should reflect the layer negotiation outcome:

| Grade | Score | Meaning in v2 |
|-------|-------|--------------|
| A | 85–100 | All four layers coherent: strong integrity, real nourishment, metabolic stability, no engineering concern |
| B | 70–84 | Structurally sound with meaningful nutritional contribution; minor concerns may be present |
| C | 55–69 | One or two layers show moderate concern; tension present but not dominant |
| D | 40–54 | Significant concern in at least one layer; possibly strong in another (tension likely active) |
| E | 0–39 | Dominant concern from one or more layers; structural emptiness, severe engineering, or negligible nutrition |

**Important:** D does not mean "bad food." It means "Bari's architecture detects a significant concern, often alongside a real strength." A whey protein isolate drink may be D for structural reasons while being genuinely nutritious. The D grade should always link to the dominant concern and the active tension.

---

## What Not to Do in the UI

**Do not reduce to stars:** Stars imply a simpler, linear judgment than Bari makes. Stars collapse the multi-layer interpretation into a consumer rating. Bari grades, not rates.

**Do not show comparative rankings prominently:** "Ranked #3 in dairy alternatives" creates the impression that Bari is a preference ranking system, not a structural assessment system.

**Do not hide tensions:** The temptation to show only the final score and omit the C-1 tension annotation undermines Bari's honesty commitment. Tensions must be accessible, even if not primary.

**Do not use alarmist language:** "Warning," "dangerous," "toxic," "avoid" are not Bari vocabulary. Bari is analytical, not prescriptive.

**Do not over-precision:** A score of 73.47 should be displayed as 73. The false precision of decimal scores suggests measurement confidence that doesn't exist.

---

*Next: See `transition_strategy.md` for how the current BSIP2 architecture evolves into v2 without breaking existing outputs.*
