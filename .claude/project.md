# Bari — Project Context

**Repository:** `C:\Bari`  
**Frontend:** `C:\Users\HP\bari` (Next.js)  
**Last verified:** 2026-05-30

---

## Mission

Bari evaluates the **nutritional architecture** of Israeli retail food products and presents the findings as shelf-native comparisons. The user should feel "someone carefully investigated this supermarket shelf for me" — not "I am using food analytics software."

Bari informs. It does not prescribe, recommend, or moralize.

---

## Bari Repository Map — TWO SEPARATE LOCATIONS

Bari spans **two distinct repositories**. Never conflate them. `C:\Bari` is **not** the website.

| Repo | Path | Contains | Use for |
|------|------|----------|---------|
| **Website repo** | `C:\Users\HP\bari` | Next.js app, React components, Tailwind, routes, `src/`, `package.json`, the comparison frontend JSON the site consumes | Frontend implementation, routes, components, UI work, `npm run lint`, `npm run build` |
| **Product / data workspace** | `C:\Bari` | BSIP scoring assets, product research, CE handoffs, reports, scoring documentation, category analysis, MVP/rollout plans, Python pipelines | Scoring research, BSIP outputs, CE reports, nutrition docs, category rollout |

### Working rules

- Website implementation, routes, components, frontend JSON, lint, build → **`C:\Users\HP\bari`**
- CE documents, BSIP reports, scoring research, product handoffs, rollout docs → **`C:\Bari`**
- **Never assume `C:\Bari` is the website repo** — no Next.js source lives there.
- **Never modify website source files under `C:\Bari`** unless explicitly verified.
- Before any frontend implementation, **confirm the working directory is `C:\Users\HP\bari`**.
- The frontend JSON the site renders lives in `C:\Users\HP\bari\src\data\comparisons\`. It is **generated** from BSIP2 outputs in `C:\Bari` and **copied** into the website repo.

These two trees do not cross. The data workspace produces JSON outputs that the website consumes as static data files.

---

## Intelligence Repo Folder Structure (`C:\Bari`)

```
01_framework/       Design docs, scoring theory, framework decisions (no code)
  bsip0_framework/    Extraction layer design (early/placeholder)
  bsip1_framework/    Consolidation layer design (early/placeholder)
  bsip2_framework/    Scoring layer design — 30+ documents, primary reference
    ui_language.md      Hebrew grade labels, tone rules, forbidden terms
    methodology.md      Scoring pipeline explanation (public-facing)
    comparison_logic.md Comparison and signal logic
    signal_system.md    Signal taxonomy
    validation/         Golden product suite, edge case catalog, failure modes
    v3_architecture/    V3 universal core + archetype system (design phase)
  frontend/           Frontend spec documents (canonical reference for Cursor builds)
    comparison_template_v1.md       Frozen page architecture (4 sections)
    component_build_sequence_v1.md  Build order with hard gates
    cursor_handoff_protocol_v1.md   Session startup protocol for Cursor
    comparison_view_model_v1.md     Backend→UI data contract
    design_token_governance_v1.md   Token file rules
    legacy_isolation_policy_v1.md   Legacy pages are quarantined
    architecture_generations_registry_v1.md  Gen 0 vs Gen 1 patterns
  editorial/          Writing standards (assertive writing, insight line spec)
  governance/         Category audits, comparison governance
  operations/         Operating model, org chart

02_products/        Category-first product workspaces
  snack_bars/         53 products, fully scored (canonical reference category)
  breakfast_cereals/  45 products
  yogurt_system/      45 products
  milk_and_alternatives/ 20 products
  bread_light/        32 synthetic products (stress-test corpus, not production)
  {category}/
    raw_sources/           Pre-scrape reference materials
    observations_bsip0/    Scraper outputs (per retailer)
    canonical_bsip1/       Enriched canonical records
    intelligence_bsip2/    BSIP2 scored traces
    reports/               Category-level analysis

03_operations/      Python scripts and execution artifacts
  bsip0/              Scrapers (Yohananof, Carrefour, Wolt, Shufersal)
  bsip1/              Enrichment engine + batch runners
    core/
      ingredient_enricher.py   Active enrichment engine (Hebrew term detection)
      enrich_runner.py         Batch runner
  bsip2/
    proto_v0/src/              13 Python source files — active scoring engine

99_archive/         Historical/superseded code (read-only)
```

---

## Pipeline Flow

```
Retail scrape (BSIP0)
    ↓  raw HTML/JSON/images → observations_bsip0/
Semantic enrichment (BSIP1)
    ↓  canonical BSIP1 records with Hebrew ingredient detection
Structural scoring (BSIP2)
    ↓  scored traces (bsip2_trace.json) per product
build_frontend_dataset.py
    ↓  JSON dataset (maadanim_frontend_v2.json, etc.)
Frontend (Next.js)
    ↓  static data → /hashvaot/[category] pages
Consumer
```

---

## Active Categories (Production)

| Category | Products | Frontend route |
|----------|----------|----------------|
| מעדנים (dairy desserts) | ~90 | `/hashvaot/maadanim` |
| לחם (bread) | ~80 | `/hashvaot/bread` |
| חטיפים (snack bars) | 53 | `/hashvaot/snack-bars` |
| יוגורטים (yogurts) | 45 | `/hashvaot/yogurts` |
| חלב (milk) | 20 | `/hashvaot/milk-comparison` (legacy) |

---

## Major Workflows

### Adding a new category

1. Create `02_products/{category}/` workspace
2. Run BSIP0 scraper → populate `observations_bsip0/`
3. Run BSIP1 enricher → produce `canonical_bsip1/`
4. Run BSIP2 batch runner → produce `intelligence_bsip2/`
5. Run `build_frontend_dataset.py` → produce `{category}_frontend_vN.json`
6. Copy JSON to `C:\Users\HP\bari\src\data\comparisons\`
7. Add category definition to `src/lib/comparisons/registry/categories/`
8. Add route page at `src/app/hashvaot/{category}/page.tsx`
9. Build canonical frontend components following `component_build_sequence_v1.md`

### Updating an existing category's data

1. Re-run BSIP0 scrape (if new products)
2. Re-run BSIP1 enrichment
3. Re-run BSIP2 batch runner
4. Regenerate frontend JSON
5. Copy to frontend repo

---

## Ownership Boundaries

| Role | Responsibility |
|------|---------------|
| Tom | Category launch decisions, final approvals |
| ChatGPT | Strategy specs, category briefs |
| Claude CE (this) | Pipeline execution (BSIP0–BSIP2), editorial, frontend JSON |
| Cursor IDE | Frontend component implementation |
| OpenAI Codex | QA and audit layer |

Claude CE does not modify `C:\Users\HP\bari` frontend component files. That is Cursor's domain. Claude CE produces the JSON data that feeds the frontend and maintains the `01_framework/` documentation.

---

## Key Design Invariants

1. BSIP1 is the canonical cross-retailer layer. Never write BSIP2 traces into BSIP1 directories.
2. Matrix Integrity does NOT replace NOVA. It adds structural composition signals.
3. Score formula: `100 − deg×0.55 − eng×0.30 − hp×0.15 − assembly_drag`. No nutrition panel used.
4. All Israeli product data is Hebrew-primary.
5. Fermentation protects traditional foods. `live_cultures` → 0.40 factor cap on degradation reduction.
6. No category-specific hacks. All matrix integrity logic must generalize.

---

## Claude Skills

The six Bari skills live in **`C:\Bari\.claude\skills\`** — this is the **canonical source**:
`chief-nutrition-officer`, `head-of-product`, `frontend-architect`, `design-director`, `research-analyst`, `qa-audit-lead`.

A **mirror** exists at `C:\Users\HP\bari\.claude\skills\` so the skills load as slash commands when working in the website repo. The mirror is a copy, not a second source of truth.

- Edit skills **here** (`C:\Bari\.claude\skills\`), never in the website mirror.
- After any skill change, re-copy to the website repo:

```powershell
Copy-Item "C:\Bari\.claude\skills\*.md" "C:\Users\HP\bari\.claude\skills\" -Force
```

---

## Sources

- `C:\Bari\ARCHITECTURE.md`
- `C:\Bari\REPO_MAP.md`
- `C:\Bari\01_framework\README.md`
- `C:\Bari\01_framework\operations\operating_model_v2.md`
- `C:\Bari\01_framework\operations\org_chart_v2.md`
