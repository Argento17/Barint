# Bari Skills Roadmap

**Document:** ROADMAP.md
**Owner:** Frontend Architect
**Status:** ACTIVE
**Created:** 2026-05-31
**Task:** TASK-050

---

## Current State

As of 2026-05-31, four workflow skills and six persona files are active. The existing skills cover the full category production pipeline: category construction, scoring governance, QA validation, and frontend UI standards.

The gaps in the current coverage:
- No skill governs product comparison content (hero, prologue, insight lines, methodology text)
- No skill governs the research-to-evidence-registry pipeline
- No skill covers retailer data acquisition and scraper lifecycle
- No skill governs category launch wave planning across multiple simultaneous categories
- No skill covers the comparison page experience as a cross-category product surface

---

## Planned Skills

---

### PLANNED-001 — bari-comparison-factory

**Purpose:**
Governs the production of the consumer-facing comparison page experience as a complete product — combining data packaging, content structure, filtering logic, and ranking presentation into a single governed workflow. Distinct from `bari-category-factory` (which governs the data pipeline) and `bari-frontend-ui` (which governs UI compliance). The comparison factory governs the *product experience* of a category page: what comparisons are surfaced, in what order, and with what editorial framing.

**Owner:** Head of Product / Frontend Architect

**Trigger conditions:**
- A new category is ready for its first consumer-facing comparison page
- An existing comparison page is being restructured or significantly updated
- The comparison dimension set for a category is being revised
- Filter logic for a category is being redesigned
- Product ranking presentation is being changed for a live category
- User asks: "design the comparison experience for X", "which dimensions to compare for Y", "how should we rank Z products"

**Expected value:**
- Creates a clear handoff protocol between the data pipeline (BSIP2 output) and the consumer product (comparison page)
- Prevents ad-hoc comparison design decisions that drift over time
- Enforces consistency across categories in how comparisons are structured and framed
- Provides a documented record of why each category's comparison dimensions were selected
- Reduces rework by catching dimension selection errors before frontend implementation begins

---

### PLANNED-002 — bari-content-factory

**Purpose:**
Governs the production of all non-scoring editorial content on Bari: category hero sentences, prologue copy, product insight lines, methodology text, and filter label display names. Currently no skill prevents inconsistent or generic content from entering the site. This skill defines the content workflow: from category context to approved Hebrew copy, with review gates and prohibited patterns.

**Owner:** Chief Nutrition Officer / Head of Product

**Trigger conditions:**
- A new category is entering frontend packaging and requires hero, prologue, and methodology copy
- Existing product insight lines are being refreshed
- A new scoring signal requires an updated methodology explanation
- Hebrew copy is being reviewed for accuracy or tone
- Filter display labels are being assigned for a new category
- User asks: "write the hero sentence for X", "draft the insight line for product Y", "what should the methodology section say for Z"

**Expected value:**
- Eliminates generic AI-generated copy from the site (the current gap that `bari-frontend-ui` flags but cannot resolve)
- Ensures every insight line is derived from the product's actual BSIP2 signal, not a template
- Provides a consistent voice and register for all category copy in Hebrew
- Creates a reviewable content artifact before any copy enters the frontend
- Prevents methodology text from exposing framework terminology (NOVA, BSIP, cap, floor) to consumers
- Directly addresses the most consumer-visible quality gap in the current skill coverage

---

### PLANNED-003 — bari-research-governance

**Purpose:**
Governs the flow of scientific research findings into the BSIP2 evidence registry. Currently, research outputs from the Research Analyst flow informally to the Chief Nutrition Officer for interpretation. This skill creates a formal protocol: evidence submission format, minimum evidence tier for registry entry, CNO review gate, and the path from registered evidence to signal candidacy. Prevents the evidence registry from accumulating low-quality findings that cannot support scoring decisions.

**Owner:** Chief Nutrition Officer / Research Analyst

**Trigger conditions:**
- A new scientific finding is proposed for inclusion in the BSIP2 evidence registry
- An existing registry entry is being challenged, updated, or deprecated
- A new signal candidate (BSIP2-06x or later) requires evidence registration before entering EXPERIMENTAL status
- The evidence registry is being audited for quality or coverage
- User asks: "add this finding to the registry", "is there evidence for X signal", "what does the evidence say about Y", "register this research"

**Expected value:**
- Creates a traceable chain from published science to scoring rule — currently informal
- Prevents low-confidence evidence from reaching the scoring governance skill without CNO review
- Defines the minimum evidence tier for a finding to qualify as a BSIP2 signal candidate (currently undefined)
- Creates a formal deprecation mechanism for evidence entries that are superseded or contradicted
- Reduces the risk of rule accumulation by ensuring only strong evidence can sponsor a new signal

---

### PLANNED-004 — bari-retailer-acquisition

**Purpose:**
Governs the lifecycle of retailer data acquisition: scraper configuration, data freshness rules, corpus update triggers, and the handling of scraper failures or product data anomalies. The current scraper issues (Shufersal fat field extraction errors, TASK-039) reveal the absence of a governed scraper lifecycle. This skill would define what triggers a scraper fix, what constitutes a corpus-level data anomaly requiring a flag, and what the re-run protocol is after a data correction.

**Owner:** Data Architecture

**Trigger conditions:**
- A new retailer is being added to the data acquisition pipeline
- A scraper anomaly is detected (wrong field extraction, missing data, encoding issues)
- A corpus re-run is required after a scraper fix
- Product data from a retailer is being audited for freshness or completeness
- A new product category is being scraped for the first time
- User asks: "fix the scraper for X", "add retailer Y to the pipeline", "investigate data anomaly for Z", "re-run corpus after scraper fix"

**Expected value:**
- Creates a formal protocol for scraper defect detection and resolution (the Shufersal fat field anomaly is a live example of the gap)
- Defines when a corpus re-run is required vs. when scores can remain at a flagged state
- Prevents scraper fixes from triggering uncontrolled corpus changes that affect live scores without QA review
- Documents the canonical field mappings per retailer so scraper changes are versioned and reviewable
- Enables the QA & Audit Lead to formally track known data anomalies rather than per-task notes

---

### PLANNED-005 — bari-wave-planning

**Purpose:**
Governs the planning and coordination of category launch waves — when multiple categories are moving through the pipeline simultaneously and require sequenced resource allocation, dependency management, and launch timing. As Bari scales beyond its first two or three categories, ad-hoc sprint planning will break down. This skill defines how to structure a wave, sequence its categories, manage cross-category dependencies, and define wave completion criteria.

**Owner:** Head of Product

**Trigger conditions:**
- More than two categories are being developed simultaneously
- A launch wave is being planned for a product milestone
- Category dependencies across a wave need to be mapped (e.g., a shared signal vocabulary needed by multiple categories)
- Resource allocation across categories needs to be formalized
- A wave retrospective is being run
- User asks: "plan the next category wave", "sequence the upcoming launches", "what's the dependency order for X and Y", "define wave completion criteria"

**Expected value:**
- Prevents individual category tasks from advancing out of sequence relative to wave constraints
- Creates a formal dependency map that surfaces cross-category blockers before they stall a wave
- Defines wave-level completion criteria so launch decisions are made against consistent standards
- Enables the Head of Product to manage multiple parallel tracks without losing governance integrity
- Documents wave rationale for retrospective review and future sequencing decisions

---

## Recommended Next Skill

**Recommendation: PLANNED-002 — bari-content-factory**

Rationale:

Every category currently shipped or in pipeline requires editorial content before it can go live: a hero sentence, a prologue, product insight lines, and methodology text. This content is currently produced without a governing skill. The `bari-frontend-ui` skill explicitly blocks generic AI copy patterns and prevents hardcoded placeholder text — but it offers no workflow for producing correct content in its place. The gap is real and active on every category launch.

The content factory is also the only planned skill that affects every other skill's output at the consumer-facing layer. Data quality, scoring accuracy, and UI compliance all exist below the content surface. The consumer reads the insight line, not the BSIP2 trace. A skill that governs content quality is therefore the highest-leverage addition to the current set.

PLANNED-003 (research governance) and PLANNED-004 (retailer acquisition) are both urgently needed for the data infrastructure, but they serve internal workflows. PLANNED-001 (comparison factory) and PLANNED-005 (wave planning) are scale-planning skills that gain value as category count grows. PLANNED-002 is immediately needed, is consumer-facing, and is currently completely ungoverned.

**Implementation prerequisite:** None. The skill can be designed and tested against the existing hummus category content before any new category launches.

---

## Roadmap Status Table

| ID | Skill Name | Owner | Priority | Dependency | Status |
|----|-----------|-------|----------|------------|--------|
| PLANNED-001 | bari-comparison-factory | Head of Product / Frontend Architect | Medium | bari-category-factory operational | Planned |
| PLANNED-002 | bari-content-factory | Chief Nutrition Officer / Head of Product | **High** | None | **Recommended next** |
| PLANNED-003 | bari-research-governance | Chief Nutrition Officer / Research Analyst | High | BSIP2 evidence registry mature | Planned |
| PLANNED-004 | bari-retailer-acquisition | Data Architecture | High | Scraper defect pattern documented (TASK-039) | Planned |
| PLANNED-005 | bari-wave-planning | Head of Product | Medium | >2 simultaneous active categories | Planned |

---

*Bari Skills Roadmap — TASK-050 — Frontend Architect — 2026-05-31*
*Update this document when a planned skill enters active development or when new skills are proposed.*
