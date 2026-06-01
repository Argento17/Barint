# Bari Architecture Map v1

**Type:** System overview — current state only  
**Authority:** Frontend Architect  
**Last verified:** 2026-05-30  
**Reading time:** ~12 minutes  

This document describes the Bari system as it exists today. It does not propose changes.

---

## System Overview

Bari is two repositories that do not share code. They communicate through a single interface: JSON files copied from the data workspace into the website repo.

```
C:\Bari                          C:\Users\HP\bari
(data workspace)                 (Next.js website)
        │                                │
        │  {category}_frontend_vN.json   │
        │ ──────────────────────────────>│
        │     (manual copy)              │
```

Every other boundary — tooling, Python packages, scoring logic, framework docs — lives exclusively in one repo or the other. There is no shared runtime dependency.

---

## 1. Repositories

### C:\Bari — Data Workspace

Purpose: scoring pipeline, product research, category data, framework governance.

```
C:\Bari\
  .claude\                   Claude Code config for this repo
    hooks\                   check-forbidden-terms.ps1, remind-bsip2-regression.ps1
    skills\                  6 Claude skill files (canonical source)
    settings.json            permissions + hook config
    settings.local.json      session-specific permissions (not committed)
  .venv\                     Python virtual environment (pip packages)
  01_framework\              Design docs, scoring theory, governance — no code
    bsip2_framework\         BSIP2 methodology, signals, caps, categories
    frontend\                Frontend specs consumed by website implementation
    governance\              Constitutional documents, registries
    editorial\               Writing standards
  02_products\               Category-specific workspaces (data, not code)
    snack_bars\
    maadanim\
    milk_and_alternatives\
    bread_retail_001/002/003\
    breakfast_cereals\
    yogurt_system\
    bread_light\             Stress-test corpus (not production)
  03_operations\             Executable Python pipeline
    bsip0\                   Scrapers and acquisition
    bsip1\                   Enrichment engine
    bsip2\proto_v0\src\      Scoring engine (48 Python files)
    reports\                 Analysis outputs
    tools\
  99_archive\                Superseded code — read only
```

### C:\Users\HP\bari — Website

Purpose: Next.js frontend, served pages, comparison UI.

```
C:\Users\HP\bari\
  .claude\                   Claude Code config for this repo
    hooks\                   guard-generated-json.ps1, check-forbidden-terms.ps1
    skills\                  Mirror of C:\Bari\.claude\skills\ (not canonical)
    settings.json            hook config + Playwright MCP approval
    bari-qa-validate.js      Playwright route validation script
    playwright-screenshots\  Screenshot output from QA script
  .mcp.json                  Playwright MCP server definition
  src\
    app\                     Next.js routes
      hashvaot\              Comparison page routes
        bread\
        maadanim\
        snacks\
        yogurts\
        milk-comparison\     Legacy route
        bread-comparison\    Legacy route
        snack-bars\          Legacy route
      blog\                  Editorial articles
      compare\               Legacy comparison routes
    components\
      shared\                Gen 1 canonical components (10 files)
      comparisons\           Page assemblies + Gen 0 legacy (25 files)
      snack\                 Gen 0 legacy (quarantined)
      ui\                    Shadcn-style primitives
    data\
      comparisons\           Generated JSON — do not hand-edit
    lib\
      comparisons\           Data modules, page data, filters, registry
        registry\            Category registry (4 categories)
      design\                Design tokens
      view-models\           BariProductVM — the UI type contract
```

---

## 2. Data Flow

The full pipeline from retail shelf to rendered page:

```
RETAIL SHELF
     │
     ▼
BSIP0 — Scraping
  C:\Bari\03_operations\bsip0\
  Retailers: Shufersal, Yohananof, Carrefour, Wolt
  Output: raw HTML/JSON/images per product
     │
     ▼  observations_bsip0/{retailer}/
     │
BSIP1 — Semantic Enrichment
  C:\Bari\03_operations\bsip1\core\ingredient_enricher.py
  Hebrew term detection, additive classification, NOVA markers,
  fermentation detection, trust level assignment
  Output: canonical_bsip1/{product}.json (one per product)
     │
     ▼  canonical_bsip1/
     │
BSIP2 — Structural Scoring
  C:\Bari\03_operations\bsip2\proto_v0\src\
  batch_run_{category}.py → score_engine.py
  Output: intelligence_bsip2/{product}_trace.json (one per product)
     │
     ▼  intelligence_bsip2/
     │
build_frontend_dataset.py
  Reads all trace JSONs for a category.
  Transforms: BSIP2 trace → consumer-facing fields only.
  Output: {category}_frontend_vN.json
     │
     ▼  MANUAL COPY
     │
C:\Users\HP\bari\src\data\comparisons\{category}_frontend_vN.json
     │
     ▼
corpus.ts  loadComparisonCorpus()
  Reads JSON, validates, produces BariProductVM[]
     │
     ▼
{category}-page-data.ts
  Assembles: products, hero, prologue, methodology, filters
     │
     ▼
{category}-comparison-page.tsx
  Renders: CategoryHero → CategoryPrologue → ProductTable → MethodologyFooter
     │
     ▼
BROWSER — Consumer
```

**The JSON copy step is manual.** There is no automated sync between repos. When BSIP2 scores change, `build_frontend_dataset.py` must be re-run, and the output must be copied to the website repo.

---

## 3. BSIP2 Scoring Engine

**Location:** `C:\Bari\03_operations\bsip2\proto_v0\src\`

### Core engine files

| File | Role |
|---|---|
| `score_engine.py` | Entry point. Orchestrates all 6 scoring stages. |
| `signal_extractor.py` | L1–L6 signal extraction from BSIP1 records |
| `constants.py` | All thresholds, weights, grade bounds, cap values |
| `router_v2.py` | Product category routing (3-stage: anchor → context gates → resolution) |
| `matrix_integrity.py` | Matrix Integrity Engine v2 (structural food composition) |
| `nova_proxy.py` | NOVA classification inferred from Hebrew ingredient text |
| `structural_classifier.py` | Structural class assignment (A–F) |
| `input_loader.py` | Reads BSIP1 JSON records |
| `trace_writer.py` | Writes BSIP2 trace JSON output |
| `evaluation_scope.py` | Scope assignment, imported by all batch runners |

### Batch runners (one per category)

| File | Category |
|---|---|
| `batch_run_snack_bars_001.py` | Snack bars |
| `batch_run_cereals_001.py` | Breakfast cereals |
| `batch_run_yogurt_001.py` | Yogurt |
| `batch_run_milk_004.py` | Milk (canonical run) |
| `batch_run_maadanim_001.py` | Maadanim (dairy desserts) |
| `batch_run_bread_retail_003.py` | Bread retail |

### Validation scripts (must pass after any engine change)

| Script | What it tests |
|---|---|
| `run_regression_check.py` | 12-case golden corpus regression |
| `run_router_regression.py` | 12-case router v2 regression |
| `generate_router_validation.py` | 163-product router analysis |

**Rule:** After any edit to `score_engine.py`, `constants.py`, `matrix_integrity.py`, `router_v2.py`, `signal_extractor.py`, `nova_proxy.py`, or `structural_classifier.py` — run both regression scripts. Both must pass 12/12 before outputs are treated as valid.

The `remind-bsip2-regression.ps1` hook enforces this as a reminder (PostToolUse).

### Frontend dataset builder

`build_frontend_dataset.py` reads all BSIP2 traces for a category and produces a single JSON file in the format consumed by the website. This is the only file that crosses the repo boundary.

---

## 4. Shared Comparison Architecture (Gen 1)

Gen 1 is the current canonical architecture. All new category pages must use it.

### Canonical components

All 10 files in `src/components/shared/` are Gen 1. They are the only components that should be used in new category builds.

| Component | Role | Hard rules |
|---|---|---|
| `score-chip.tsx` | Score + grade display | Neutral tint background only; left border accent; never saturated by grade |
| `product-row.tsx` | Single product row, mobile + desktop | 72px collapsed; inline expansion only; full-row tap target |
| `product-table.tsx` | Table container + state | One expanded row at a time; products pre-sorted by backend |
| `product-table-header.tsx` | Desktop column headers | Hidden on mobile; matches row grid exactly |
| `expansion-section.tsx` | Expandable detail panel | Inline only; content order: interpretive → technical → footer |
| `category-hero.tsx` | Page hero (eyebrow / h1 / metadata) | One h1 per page; no images; no statistics |
| `category-prologue.tsx` | Introductory prose | 3–5 sentences; no bullets |
| `category-shelf-lenses.tsx` | Filter pill group | Single-select; Hebrew labels; 2–3 dimensions max |
| `methodology-footer.tsx` | Bottom plain text | `<footer>` only; no card; 11px #8A908B |
| `milk-orbit-visual.tsx` | Animated SVG illustration | Milk category only; not reusable for other categories |

### Category registry

`src/lib/comparisons/registry/index.ts` is the routing table for comparison categories.

**Registered categories (4):**

| ID | Hebrew name | Route |
|---|---|---|
| `maadanim` | מעדנים | `/hashvaot/maadanim` |
| `bread` | לחם | `/hashvaot/bread` |
| `snacks` | חטיפים | `/hashvaot/snacks` |
| `yogurts` | יוגורטים | `/hashvaot/yogurts` |

Each category registration consists of four artifacts:

```
src/lib/comparisons/registry/categories/{category}.ts  ← registry entry
src/lib/comparisons/{category}-page-data.ts            ← data assembly
src/lib/comparisons/{category}-shelf-filters.ts        ← filter definitions
src/data/comparisons/{category}_frontend_vN.json       ← generated data
```

### View model contract

`src/lib/view-models/index.ts` is the only type file the UI imports for product data. This is an inviolable boundary.

```
BariProductVM
  id: string
  name: string
  imageUrl: string | null
  score: number | null          0–100, pre-rounded. null = unscored → chip shows "—"
  grade: BariGrade | null       A | B | C | D | E
  insightLine: string           pre-authored Hebrew, ≤12 words
  confidence: BariConfidence    verified | partial | insufficient
  expansion: BariExpansionVM
    nutrition: BariNutritionVM | null
    ingredients: string | null
    confidenceLabel: string     pre-rendered Hebrew — UI renders verbatim
    servingNote: string         e.g. "ל-100 גרם"
    positiveSignals?: string[]  1–3 observable strengths
    limitingFactors?: string[]  0–2 compositional limits
    bottomLine?: string         editorial synthesis
    comparisonContext?: string  shelf-relative context
```

**The boundary rule:** UI components receive `BariProductVM` and nothing else. No raw BSIP fields, no scoring fields, no routing metadata crosses this boundary.

### Design tokens

`src/lib/design/bari-comparison-tokens.ts` is the single source of all visual constants: colours, spacing, font sizes, grid column definitions. Any component that hardcodes a value that exists in this file is in violation. The file emits a dev-mode console warning when this happens.

### Canonical reference implementation

When implementing a new category, copy the maadanim pattern:

```
src/components/comparisons/maadanim-comparison-page.tsx
src/lib/comparisons/maadanim-page-data.ts
src/lib/comparisons/maadanim-shelf-filters.ts
src/lib/comparisons/registry/categories/maadanim.ts
src/data/comparisons/maadanim_frontend_v2.json
```

---

## 5. Legacy Systems (Gen 0)

Gen 0 is the exploratory phase. It is quarantined, not deleted. Do not import Gen 0 components into Gen 1 pages.

**Governed by:** `C:\Bari\01_framework\frontend\legacy_isolation_policy_v1.md`

### Quarantined files

| File / Directory | Why quarantined |
|---|---|
| `src/components/comparisons/milk-comparison-page.tsx` | Custom layout, uses Gen 0 components |
| `src/components/comparisons/milk-editorial/` | Full editorial film-style page (8 files) |
| `src/components/comparisons/bread-comparison-dashboard.tsx` | Card grid layout, framework exposure |
| `src/components/comparisons/snack-comparison-engine.tsx` | Card grid, NOVA label rendering |
| `src/components/snack/` | Gen 0 snack card components |
| `src/components/comparisons/bari-grade-badge.tsx` | Saturated grade colour encoding |
| `src/components/comparisons/bari-interpretation-panel.tsx` | Dimension bars, pillar labels |
| `src/components/comparisons/dimension-bars.tsx` | Renders dimension names and scores |
| `src/components/comparisons/matrix-integrity-badge.tsx` | Renders "שלמות מטריצה" + degradation score |

### Legacy routes

| Route | Status | Notes |
|---|---|---|
| `/hashvaot/milk-comparison` | Live, legacy | Uses Gen 0 MilkComparisonPage; not a template |
| `/hashvaot/bread-comparison` | Live, legacy | Bread comparison dashboard |
| `/hashvaot/snack-bars` | Live, legacy | Gen 0 snack engine |

### Gen 0 defining traits (do not reproduce)

- Score chip colour encodes grade (green A, red E)
- Grade label text beside chip: "B · גבוה"
- Product cards with border and shadow in a grid layout
- Expansion opens as a bottom sheet (modal), not inline
- NOVA rendered as a consumer-visible string: "NOVA4"
- Dimension bars visible on expanded rows: `DimensionBars`
- MatrixIntegrityBadge rendered on row
- Methodology in a collapsible `<details>` card
- Score attribution exposed: "מה מעלה / מוריד את הציון"

---

## 6. Governance Layer

### Document hierarchy

```
C:\Bari\01_framework\
  governance\
    governance_v1.md                   Constitutional — all else is subordinate to this
    evidence_registry_v1.md            Nutrition rulings + all accepted positions (77 entries)
    exception_registry_v1.md           Approved architecture deviations (1 active: EXCEPTION-001)
    comparison_governance_v1.md        Category launch standards
    consumer_usecase_guardrails_v2.md  Consumer communication rules
    category_audit_*.md                Per-category audit records
  frontend\
    comparison_template_v1.md          Canonical page structure (authority)
    comparison-template-standard-v1.md Design standard (current approved state)
    architecture_generations_registry_v1.md  Gen 0 vs Gen 1 definitions
    legacy_isolation_policy_v1.md      Quarantine rules for Gen 0
    component_build_sequence_v1.md     Build gate order
    comparison_view_model_v1.md        View model spec
    design_token_governance_v1.md      Token file ownership rules
    cursor_handoff_protocol_v1.md      Session startup protocol
```

### Evidence Registry

**File:** `C:\Bari\01_framework\governance\evidence_registry_v1.md`

The Evidence Registry is Bari's institutional memory for all accepted scientific positions, nutritional rulings, and scoring decisions. It contains 77 entries (BEV-001 to BEV-077) across 10 sections: core framework, scoring architecture, processing science, nutritional science, category calibrations, hard cap rules, product rulings, known distortions, future architecture, and language/editorial rulings.

**Relationship to scoring:** Every cap, floor, weight, and category threshold in `constants.py` has a corresponding BEV entry that records why it exists. When a scoring constant is changed, the associated BEV entry must be updated.

**Relationship to content:** Every approved and forbidden UI language term in `ui_language.md` is captured in BEV-071 through BEV-077. These entries are the authoritative source for the `check-forbidden-terms.ps1` hook's term list.

**Append-only rule:** Entries are never deleted or overwritten. Superseded positions are amended by adding a successor entry that references the original.

### Exception Registry

**File:** `C:\Bari\01_framework\governance\exception_registry_v1.md`

Documents deliberate deviations from the frozen architecture rules. One active exception:

- **EXCEPTION-001** — Bread fermentation filter tooltip. A ⓘ icon on one specific filter label ("ללא מחמצת מזוהה") in the bread category. The only tooltip permitted anywhere in the system. No other element may have a tooltip until a new exception is registered.

Any UI element that violates a template rule without a registered exception is an architecture violation.

### Claude skills

Six skills live in `C:\Bari\.claude\skills\` (canonical source):

| Skill | Role |
|---|---|
| `head-of-product` | Product strategy, MVP scoping, prioritisation |
| `chief-nutrition-officer` | Nutrition science, scoring philosophy, BSIP methodology |
| `frontend-architect` | Website implementation, components, routes, build |
| `design-director` | Visual design, component standards, design tokens |
| `research-analyst` | Research synthesis, evidence inventory |
| `qa-audit-lead` | QA execution, data verification, audit |

A mirror lives at `C:\Users\HP\bari\.claude\skills\` so skills load as slash commands in both repos. The mirror is a copy — edit canonical, then re-copy:

```powershell
Copy-Item "C:\Bari\.claude\skills\*.md" "C:\Users\HP\bari\.claude\skills\" -Force
```

---

## 7. QA Infrastructure

### Playwright MCP

**Config:** `C:\Users\HP\bari\.mcp.json` (server definition) + `C:\Users\HP\bari\.claude\settings.json` (approval)

```json
{
  "mcpServers": {
    "playwright": {
      "type": "stdio",
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    }
  }
}
```

The MCP is pre-approved via `"enabledMcpjsonServers": ["playwright"]` in settings.json. It connects automatically when Claude Code starts in the website repo.

**Available after session restart:** `browser_navigate`, `browser_snapshot`, `browser_take_screenshot`, `browser_console_messages`, `browser_click`, `browser_type`

### Playwright validation script

**File:** `C:\Users\HP\bari\.claude\bari-qa-validate.js`

Node.js script using the project's `playwright` devDependency. Runs headless Chromium against the local dev server. Tests 4 routes and checks:

- HTTP 200 response
- RTL layout (`dir="rtl"` or `lang="he"`)
- Comparison table/grid present (`bari-zebra-rows`, `bari-shelf`)
- Product rows present (`bari-shelf-row`)
- Zero JavaScript console errors
- Screenshot captured to `.claude/playwright-screenshots/`

**Usage:**
```powershell
# Dev server must be running on localhost:3000
cd C:\Users\HP\bari
node .claude/bari-qa-validate.js
```

**Routes tested:** `/hashvaot/milk-comparison`, `/hashvaot/snacks`, `/hashvaot/bread`, `/hashvaot/maadanim`

### Browser version

Playwright v1.60.0 (in `devDependencies`) requires Chromium 1223. Installed at `%LOCALAPPDATA%\ms-playwright\chromium-1223`. If missing: `npx playwright install chromium`.

---

## 8. Hooks and Enforcement Layer

Three hooks enforce architectural constraints automatically. They run in the Claude Code harness — not in Claude's context — so they fire even when Claude forgets the rules.

### Website repo hooks (`C:\Users\HP\bari\.claude\`)

**Hook 1: guard-generated-json.ps1**

| Property | Value |
|---|---|
| Event | `PreToolUse` on `Write \| Edit` |
| Condition | `file_path` matches `\src\data\comparisons\*.json` |
| Action | Exits 2 (hard block). Prints instructions to run pipeline instead. |
| Purpose | Prevents hand-edits to generated JSON, which create silent lineage divergence |

**Hook 2: check-forbidden-terms.ps1**

| Property | Value |
|---|---|
| Event | `PostToolUse` on `Write \| Edit` |
| Condition | File extension is `.tsx`, `.ts`, or `.md` |
| Action | Greps for 14 forbidden term patterns. Prints warnings with line numbers. Exit 0 (warn, not block). |
| Purpose | Prevents editorial violations (healthy/unhealthy, detox, AI-powered, etc.) |

### Data workspace hooks (`C:\Bari\.claude\`)

**Hook 2 (mirror): check-forbidden-terms.ps1**

Same script as website repo. Fires on `.tsx`, `.ts`, `.md` edits in the data workspace.

**Hook 3: remind-bsip2-regression.ps1**

| Property | Value |
|---|---|
| Event | `PostToolUse` on `Write \| Edit` |
| Condition | Path contains `\bsip2\proto_v0\` AND filename is one of the 7 engine files |
| Action | Prints regression run commands. Exit 0 (remind, not block). |
| Purpose | Prevents scoring outputs being used before regression checks pass |

### Hook wiring

```
C:\Users\HP\bari\.claude\settings.json
  PreToolUse  → guard-generated-json.ps1   [Write|Edit]
  PostToolUse → check-forbidden-terms.ps1  [Write|Edit]

C:\Bari\.claude\settings.json
  PostToolUse → check-forbidden-terms.ps1  [Write|Edit]
  PostToolUse → remind-bsip2-regression.ps1 [Write|Edit]
```

---

## 9. What Varies vs. What Is Frozen

### Frozen across all categories

- Four-section page structure (Hero → Prologue → Table → Footer)
- Score chip: tint background, left border accent, never saturated
- Row height: 72px collapsed minimum
- Expansion: inline only, single-row at a time
- Desktop grid: `[2.25rem 4.5rem minmax(0,1fr) 5.25rem]`
- View model boundary: `BariProductVM` is the only type the UI consumes
- Forbidden rendered terms: NOVA, BSIP, cap, floor, structural_class, matrix_integrity, pillar, dimension
- Design token source: `bari-comparison-tokens.ts` — no hardcoded duplicates

### Varies per category

- Category name, hero title, prologue copy, methodology copy
- Filter dimensions and labels
- Product JSON source file
- Component file names and routes
- Number of products

---

## 10. Active Data State (2026-05-30)

| Category | Route | Status | Products | Data source |
|---|---|---|---|---|
| מעדנים | `/hashvaot/maadanim` | Live | ~90 | `maadanim_frontend_v2.json` |
| לחם | `/hashvaot/bread` | Live | ~80 | `bread_frontend_v2.json` |
| חטיפים | `/hashvaot/snacks` | Live (needs rescore) | 18 scored | `snacks_frontend_v2.json` |
| יוגורטים | `/hashvaot/yogurts` | Live | ~45 | `yogurts_frontend_v1.json` |
| חלב | `/hashvaot/milk-comparison` | Live (legacy) | 18 | `milk-comparison.json` ¹ |

¹ Milk uses a custom data file not built by the standard `build_frontend_dataset.py` pipeline.

**Snacks note:** The snacks dataset has null nutrition values for all products — BSIP0 captured the data but it was not ingested. Scores reflect structural/processing signals only.

---

## 11. Key Files Reference

The 15 files most important to understand before doing any work in Bari:

| File | Location | Why it matters |
|---|---|---|
| `governance_v1.md` | `C:\Bari\01_framework\governance\` | Constitutional — everything else is subordinate |
| `evidence_registry_v1.md` | `C:\Bari\01_framework\governance\` | All accepted nutritional positions and rulings |
| `exception_registry_v1.md` | `C:\Bari\01_framework\governance\` | All approved architecture deviations |
| `constants.py` | `C:\Bari\03_operations\bsip2\proto_v0\src\` | Every threshold, weight, and cap value |
| `score_engine.py` | `C:\Bari\03_operations\bsip2\proto_v0\src\` | Scoring pipeline orchestrator |
| `build_frontend_dataset.py` | `C:\Bari\03_operations\bsip2\proto_v0\src\` | The only script that produces website-ready JSON |
| `index.ts` (view-models) | `C:\Users\HP\bari\src\lib\view-models\` | The contract between scoring and UI |
| `index.ts` (registry) | `C:\Users\HP\bari\src\lib\comparisons\registry\` | Category routing table |
| `bari-comparison-tokens.ts` | `C:\Users\HP\bari\src\lib\design\` | All visual constants |
| `product-row.tsx` | `C:\Users\HP\bari\src\components\shared\` | The core rendering unit |
| `score-chip.tsx` | `C:\Users\HP\bari\src\components\shared\` | Score/grade display rules |
| `maadanim-comparison-page.tsx` | `C:\Users\HP\bari\src\components\comparisons\` | Canonical Gen 1 page reference |
| `comparison_template_v1.md` | `C:\Bari\01_framework\frontend\` | Page structure authority document |
| `architecture_generations_registry_v1.md` | `C:\Bari\01_framework\frontend\` | Gen 0 vs Gen 1 catalogue |
| `legacy_isolation_policy_v1.md` | `C:\Bari\01_framework\frontend\` | Quarantine rules |

---

*End of Architecture Map v1.*
